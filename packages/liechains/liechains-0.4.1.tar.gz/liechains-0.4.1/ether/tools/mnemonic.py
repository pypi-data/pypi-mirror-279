from eth_keyfile import decode_keyfile_json, create_keyfile_json
from web3 import Web3

# 先置换， 再加密
def encrypt(mnemonic:str, password: str, exchange = True):
    if exchange:
        mnemonic = mnemonic.strip().split(' ')
        mnemonic[2], mnemonic[8] = mnemonic[8],mnemonic[2]
        mnemonic[7], mnemonic[15] = mnemonic[15],mnemonic[7]
        mn =  " ".join(mnemonic)
    else:
        mn = mnemonic
    return create_keyfile_json(mn.encode(), password.encode())

def decrypt(mnemonic:str, password: str, exchange = True):
    mnemonic = mnemonic.strip().split(' ')
    mnemonic[2], mnemonic[8] = mnemonic[8],mnemonic[2]
    mnemonic[7], mnemonic[15] = mnemonic[15],mnemonic[7]
    return " ".join(mnemonic)


