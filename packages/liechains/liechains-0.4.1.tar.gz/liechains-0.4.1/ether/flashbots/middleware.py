from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import threading
from typing import Callable
from web3 import Web3
from web3.middleware import Middleware
from web3.types import RPCEndpoint, RPCResponse
from typing import Any
from .provider import FlashbotProvider

FLASHBOTS_METHODS = [
    "eth_sendBundle",
]


def construct_flashbots_middleware(
    flashbots_providers: list[FlashbotProvider],
) -> Middleware:
    """Captures Flashbots RPC requests and sends them to the Flashbots endpoint
    while also injecting the required authorization headers

    Keyword arguments:
    flashbots_provider -- An HTTP provider instantiated with any authorization headers
    required
    """

    def flashbots_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], w3: Web3
    ) -> Callable[[RPCEndpoint, Any], RPCResponse]:
        def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
            if method not in FLASHBOTS_METHODS:
                return make_request(method, params)
            else:
                with ThreadPoolExecutor(len(flashbots_providers)) as pool:
                    result = list(
                        pool.map(
                            lambda provider: provider.make_request(method, params),
                            flashbots_providers,
                        )
                    )
                    return {"jsonrpc": "2.0", "id": 0, "result": result}

        return middleware

    return flashbots_middleware
