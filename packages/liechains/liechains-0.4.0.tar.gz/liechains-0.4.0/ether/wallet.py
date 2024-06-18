import json
from eth_account import Account
from web3 import Web3
from eth_account.signers.local import LocalAccount


class Wallet:
    def __init__(self, mnemonic) -> None:
        self.mnemonic = mnemonic

    @classmethod
    def load_keystore(cls, password, f="keystore.json"):
        return cls.decrypt_keystore(json.load(open(f)), password)

    @classmethod
    def decrypt_keystore(cls, data, password):
        mn = Account.decrypt(data, password).decode()
        return Wallet(mn)

    def __getitem__(self, index) -> list[LocalAccount]:
        if isinstance(index, slice):
            return [
                Account.from_mnemonic(self.mnemonic, account_path=f"m/44'/60'/0'/0/{i}")
                for i in range(index.start, index.stop)
            ]
        else:
            return Account.from_mnemonic(
                self.mnemonic, account_path=f"m/44'/60'/0'/0/{index}"
            )
