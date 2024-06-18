import logging
from typing import Callable
from web3.types import *
from web3.middleware.signing import *
from eth_utils.toolz import (
    compose,
)

import secrets
import hashlib
import hmac
from Crypto.Cipher import AES
from hashlib import sha512
from binascii import unhexlify
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import requests
import json
from web3 import Web3


def signer_middleware(w3: Web3, url: str, pubkey: str) -> Middleware:
    signer = RemoteSigner(w3.eth.chain_id, url, pubkey)

    def sign_and_send_raw_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], w3: "Web3"
    ) -> Callable[[RPCEndpoint, Any], RPCResponse]:
        format_and_fill_tx = compose(
            format_transaction, fill_transaction_defaults(w3), fill_nonce(w3)
        )

        def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
            if method != "eth_sendTransaction":
                return make_request(method, params)
            else:
                transaction = format_and_fill_tx(params[0])
            if "from" not in transaction:
                return make_request(method, params)
            elif not transaction.get("from"):
                return make_request(method, params)

            fm = transaction['from']
            if 'maxFeePerDataGas' in transaction:
                transaction['type'] = '0x3'
            elif 'maxFeePerGas' in transaction and 'maxPriorityFeePerGas' in transaction:
                transaction['type'] = '0x2'
            elif 'acccessList' in transaction:
                transaction['type'] = '0x1'
            else:
                transaction['type'] = '0x0'
            if 'data' in transaction:
                logging.warning(f"use input instead of data in tx dict: {transaction}")
                transaction['input'] = transaction['data']
                transaction.pop('data')
            
            result = signer.sign_transaction(fm, transaction)
            return make_request(RPCEndpoint("eth_sendRawTransaction"), [result['hex']])

        return middleware

    return sign_and_send_raw_middleware


AES_BLOCK_SIZE = 16


class EncryptOption:
    def __init__(self, iv, ephemPublicKey, ciphertext, mac):
        self.iv = iv
        self.ephemPublicKey = ephemPublicKey
        self.ciphertext = ciphertext
        self.mac = mac

    def __str__(self):
        return f"Iv: {self.iv}, \nEphemPublicKey: {self.ephemPublicKey}, \nCiphertext: {self.ciphertext}, \nMac: {self.mac}"

    def stringify(self):
        compressed_key = compress(self.ephemPublicKey)

        data = bytearray()
        data.extend(bytes.fromhex(self.iv))
        data.extend(compressed_key)
        data.extend(bytes.fromhex(self.mac))
        data.extend(bytes.fromhex(self.ciphertext))

        return data.hex()


def compress(pubkey):
    pub_key = bytes.fromhex(pubkey)

    if pub_key[0] != 0x04 or len(pub_key) != 65:
        raise ValueError("Invalid public key")

    result = bytearray(33)
    if pub_key[64] % 2 == 1:
        result[0] = 0x03
    else:
        result[0] = 0x02

    result[1:] = pub_key[1:33]
    return result


def encrypt_by_key(public_key: str, message: bytes):
    public_key_bytes = Web3.to_bytes(hexstr=public_key)
    # Load public key
    public_key_numbers = ec.EllipticCurvePublicNumbers(
        curve=ec.SECP256K1(),
        x=int.from_bytes(public_key_bytes[1:33], byteorder="big"),
        y=int.from_bytes(public_key_bytes[33:], byteorder="big"),
    )

    public_key = public_key_numbers.public_key(default_backend())

    # Generate ephemeral key
    ephemeral_private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
    ephemeral_public_key = ephemeral_private_key.public_key()

    # ECDH
    shared_secret = ephemeral_private_key.exchange(ec.ECDH(), public_key)
    derived_key = hashlib.sha512(shared_secret).digest()
    key_e = derived_key[:32]
    key_m = derived_key[32:]

    # AES Encrypt
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()

    iv = secrets.token_bytes(16)

    cipher = Cipher(algorithms.AES(key_e), modes.CBC(iv), default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # HMAC
    data_to_mac = (
        iv
        + ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )
        + ciphertext
    )
    hmac_calculator = hmac.new(key_m, data_to_mac, hashlib.sha256)
    mac = hmac_calculator.digest()

    return EncryptOption(
        iv=iv.hex(),
        ephemPublicKey=ephemeral_public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        ).hex(),
        ciphertext=ciphertext.hex(),
        mac=mac.hex(),
    )


def decrypt_by_key(opt: EncryptOption, prv_key_str: str):
    if opt is None:
        raise ValueError("EncryptOption data error")

    if not prv_key_str.startswith("0x"):
        prv_key_str = "0x" + prv_key_str

    byte_key = bytes.fromhex(prv_key_str[2:])
    int_key = int.from_bytes(byte_key, byteorder="big")

    # 使用 coincurve 创建私钥和公钥对象
    curve = ec.SECP256K1()
    private_key = ec.derive_private_key(int_key, curve, default_backend())

    # Load the public key
    ephem_public_key_bytes = unhexlify(opt.ephemPublicKey)
    public_key = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256K1(), ephem_public_key_bytes
    )

    # 计算ECDH共享密钥
    ecdh_key = private_key.exchange(ec.ECDH(), public_key)

    derived_key = sha512(ecdh_key).digest()
    key_e = derived_key[:32]
    key_m = derived_key[32:]

    # 先将opt.iv作为第一个元素加入
    data_to_mac = [opt.iv]
    # 将opt.ephemPublicKey和opt.ciphertext拼接
    combined = opt.ephemPublicKey + opt.ciphertext

    # 再将combined作为第二个元素加入
    data_to_mac.append(combined)
    res = "".join(data_to_mac)

    bytes_data_to_mac = bytes.fromhex(res)
    hm = hmac.new(bytes.fromhex(key_m.hex()), bytes_data_to_mac, hashlib.sha256)
    expected_mac = hm.digest()

    if not hmac.compare_digest(opt.mac, expected_mac.hex()):
        raise ValueError("Invalid MAC")

    iv_bytes = bytes.fromhex(opt.iv)
    cipher = AES.new(key_e, AES.MODE_CBC, iv_bytes)
    plain_text = cipher.decrypt(bytes.fromhex(opt.ciphertext))

    # Assuming you have a removePKCSPadding function implemented in Python
    plain = remove_pkcs_padding(plain_text)
    return plain


def remove_pkcs_padding(src):
    length = len(src)
    pad_length = src[-1]

    if pad_length > AES_BLOCK_SIZE or length < AES_BLOCK_SIZE:
        raise ValueError(f"invalid padding length: {pad_length}")
    return src[:-pad_length]


class RemoteSigner:
    SIGNER_PING = "/ping"
    SIGNER_ADDRESS = "/v1/address"
    SIGNER_SIGN_TRANSACTION = "/v1/sign/transaction"
    SIGNER_SIGN_MESSAGE = "/v1/sign/message"
    SIGNER_SIGN_EIP712 = "/v1/sign/eip712"

    def __init__(self, chainId: int, host, pub_key: str):
        self.chain_id = chainId
        self.host = host
        self.pub_key = pub_key

    def ping(self):
        response = requests.get(self.host + self.SIGNER_PING)
        return response.json()

    def get_address(self, index: int):
        param = dict(
            chain_id=self.chain_id,
            index=index,
        )
        body = self.encrypt_body(param)
        host = self.host + self.SIGNER_ADDRESS
        resp = requests.post(host, data=body)
        if resp.status_code != 200:
            raise Exception(f"failed get address {resp.status_code} {resp.text}")
        return resp.json()["data"]

    def sign_message(self, address, message: str):
        param = dict(
            chain_id=self.chain_id,
            account=address,
            message=message,
        )

        body = self.encrypt_body(param)
        host = self.host + self.SIGNER_SIGN_MESSAGE
        resp = requests.post(host, data=body)
        if resp.status_code != 200:
            raise Exception(f"failed sign message {resp.status_code} {resp.text}")

        return resp.json()["data"]

    def sign_transaction(self, address: str, tx: TxParams):

        for k,v in tx.items():
            if isinstance(v, int):
                tx[k] = Web3.to_hex(v)

        transaction_hash = Web3.keccak(b'')
        tx['hash'] = Web3.to_hex(transaction_hash)

        transaction_str = Web3.to_json(tx)
        param = dict(
            chain_id=self.chain_id,
            account=address,
            transaction=transaction_str,
        )

        body = self.encrypt_body(param)
        host = self.host + self.SIGNER_SIGN_TRANSACTION
        resp = requests.post(host, data=body)
        if resp.status_code != 200:
            raise Exception(f"failed sign transaction {resp.status_code} {resp.text}")
        response_json = resp.json()
        return {
            "tx": response_json["tx"],
            "hex": response_json["tx_hex"],
        }

    def sign_eip712(self, address, eip712_data):
        param = dict(
            chain_id=self.chain_id,
            account=address,
            data=eip712_data,
        )

        body = self.encrypt_body(param)
        host = self.host + self.SIGNER_SIGN_EIP712
        resp = requests.post(host, data=body)
        if resp.status_code != 200:
            raise Exception(f"failed sign 712 {resp.status_code} {resp.text}")
        return resp.json()["signature"]

    def encrypt_body(self, req_data):
        data = json.dumps(req_data).encode()
        encrypted_data = encrypt_by_key(self.pub_key, data)
        ed = encrypted_data.stringify()
        body = {"encryptMsg": "0x" + ed}
        return body
