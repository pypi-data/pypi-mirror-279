configs = {
    "local": {
        "node": {
            "rpc": "http://localhost:8545",
            "ws": "ws://localhost:8545",
        },
    },
    "goerli": {
        "node": {
            "rpc": "https://ethereum-goerli.publicnode.com",
            "ws": "wss://ethereum-goerli.publicnode.com",
        },
    },
    "ethereum": {
        "node": {
            "rpc": "https://eth-hk1.csnodes.com/v1/973eeba6738a7d8c3bd54f91adcbea89",
            "ws": "wss://eth-hk1.csnodes.com/ws/v1/973eeba6738a7d8c3bd54f91adcbea89",
        },
    },
    "bsc": {
        "node": {
            "rpc": "https://bsc-dataseed1.binance.org",
            "ws": "",
        },
        "is_poa": True,
    },
    "arb": {
        "node": {
            # "rpc": "https://arb-mainnet.g.alchemy.com/v2/7FWmkZwir8-miybmueaw9Nd-hHu0rOO3",
            "rpc": "https://arb1.arbitrum.io/rpc",
            "ws": "wss://arb-mainnet.g.alchemy.com/v2/7FWmkZwir8-miybmueaw9Nd-hHu0rOO3",  # 官方不支持ws
        },
    },
    "zkSync": {
        "node": {
            # "rpc": "https://mainnet.era.zksync.io",
            "rpc": "https://mainnet.era.zksync.io",
            "ws": "wss://mainnet.era.zksync.io/ws",
        },
    },
    "zkFair": {
        "node": {
            # "rpc": "https://mainnet.era.zksync.io",
            "rpc": "https://rpc.zkfair.io",
            "ws": "",
        },
    },
    "avax": {
        "node": {
            "rpc": "https://avalanche-mainnet.core.chainstack.com/ext/bc/C/rpc/021e382ae670cdb8a3b413c463d57763",
            "ws": "wss://avalanche-mainnet.core.chainstack.com/ws/ext/bc/C/ws/021e382ae670cdb8a3b413c463d57763",
        }
    },
    "manta": {
        "node": {
            "rpc": "https://pacific-rpc.manta.network/http",
            "ws": "wss://pacific-rpc.manta.network/ws",
        }
    },
}


uni_config = {
    "v2": {
        "factory": "0x5c69bee701ef814a2b6a3edd4b1652cb9cc5aa6f",
        "init_code": "0x96e8ac4277198ff8b6f785478aa9a39f403cb768dd02cbee326c3e7da348845f",
    },
    "v3": {
        "factory": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
        "init_code": "0xe34f199b19b2b4f47f68442619d555527d244f78a3297ea89325f843f87b8b54",
    },
}
