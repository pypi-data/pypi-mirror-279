from typing import Union, Optional

from eth_account.signers.local import LocalAccount
from eth_typing import URI
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3._utils.module import attach_modules

from .blox import BloxProvider

from .flashbots import Flashbots
from .middleware import construct_flashbots_middleware
from .provider import FlashbotProvider

DEFAULT_FLASHBOTS_RELAY = "https://relay.flashbots.net"


def flashbot(
    w3: Web3,
    signature_account: LocalAccount,
    blox_token: str,
    endpoint_uris: list[str],
):
    """
    Injects the flashbots module and middleware to w3.
    """

    flashbots_providers = [FlashbotProvider(signature_account, i) for i in endpoint_uris]
    # flashbots_providers = []
    # bloXroute
    flashbots_providers.append(BloxProvider(auth=blox_token))

    flash_middleware = construct_flashbots_middleware(flashbots_providers)
    w3.middleware_onion.add(flash_middleware)

    # attach modules to add the new namespace commands
    attach_modules(w3, {"flashbots": (Flashbots,)})
