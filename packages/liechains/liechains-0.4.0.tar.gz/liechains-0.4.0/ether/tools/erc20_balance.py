from ether.client import *
from ether.abis import erc20
from ether.wallet import Wallet

def get_erc20_balance(client: Web3Client, token, address):
    contract = client.eth.contract(token, abi = erc20)
    return contract.functions.balanceOf(address).call()


if __name__ == '__main__':
    client = Web3Client['bsc']
    wallet = Wallet(mn)[1:100]
    for i in wallet:
        print(get_erc20_balance(client, '0x555296de6A86E72752e5C5DC091FE49713Aa145C',i.address))
