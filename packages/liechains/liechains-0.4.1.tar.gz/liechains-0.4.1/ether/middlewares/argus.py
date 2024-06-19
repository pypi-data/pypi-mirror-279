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

from ether import abis



def argus_middleware(module_addr: str) -> Middleware:
    def sign_and_send_raw_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], w3: "Web3"
    ) -> Callable[[RPCEndpoint, Any], RPCResponse]:
        def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
            if method not in ["eth_sendTransaction"]:
                return make_request(method, params)

            transaction = params[0]
            origin_to = transaction["to"]
            # value写入了data, 交易里不会带有value
            value = transaction.get("value", 0)
            transaction['value'] = 0
            argus = w3.eth.contract(module_addr, abi=abis.argus)
            data = argus.encodeABI(
                fn_name="execTransaction",
                args=({
                    "flag": 0,
                    "to": origin_to,
                    "value": value,
                    "data": w3.to_bytes(hexstr=transaction["data"]),
                    "hint": b"",
                    "extra": b"",
                },),
            )
            transaction["to"] = module_addr
            transaction["data"] = data
            return make_request(method, params)

        return middleware

    return sign_and_send_raw_middleware
