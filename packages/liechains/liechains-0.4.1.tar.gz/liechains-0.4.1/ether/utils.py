import secrets
from eth_account import Account
from web3 import Web3
from eth_abi import encode
from eth_abi.packed import encode_packed
# from ether.abis import erc20

FactoryAddrV3 = Web3.to_bytes(hexstr="0x1F98431c8aD98523631AE4a59f267346ea31F984")
FactoryAddrV2 = Web3.to_bytes(hexstr="0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f")

PoolInitCodeV3 = Web3.to_bytes(hexstr="0xe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b54")
PoolInitCodeV2 = Web3.to_bytes(hexstr="0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f")

# 计算v2 v3 pool 地址, 抢开盘需要
def sort_addrs(addr1: str, addr2: str) -> tuple[str,str]:
    b1 = Web3.to_bytes(hexstr=addr1)
    b2 = Web3.to_bytes(hexstr=addr2)
    return (addr1, addr2) if b1 < b2 else (addr2,addr1)


def get_v2_pool_addr(token_a, token_b) -> str:
    token0, token1 = sort_addrs(token_a,token_b)
    token0 = Web3.to_bytes(hexstr=token0)
    token1 = Web3.to_bytes(hexstr=token1)
    head = bytes.fromhex('ff') + FactoryAddrV2 
    with_addrs = head + Web3.keccak(encode_packed(['address', 'address'], [token0,token1]))

    with_initcode = Web3.keccak(with_addrs + PoolInitCodeV2)
    i = with_initcode[12:]
    return Web3.to_checksum_address(i)

def get_v3_pool_addr(token_a, token_b,fee) -> str:
    token0, token1 = sort_addrs(token_a,token_b)
    token0 = Web3.to_bytes(hexstr=token0)
    token1 = Web3.to_bytes(hexstr=token1)
    head = bytes.fromhex('ff') + FactoryAddrV3 
    with_addrs = head + Web3.keccak(encode(['address', 'address', 'uint24'], [token0,token1,fee]))

    with_initcode = Web3.keccak(with_addrs + PoolInitCodeV3)
    i = with_initcode[12:]
    return Web3.to_checksum_address(i)

def random_account():
    key = "0x" + secrets.token_hex(32)
    return Account.from_key(key)

if __name__ == '__main__':
    print(get_v2_pool_addr('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8','0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'))
    print(get_v3_pool_addr('0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8','0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',3000))


