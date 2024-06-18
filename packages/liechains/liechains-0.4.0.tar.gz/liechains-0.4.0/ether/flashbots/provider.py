import json
import logging
import os
import traceback
from typing import Any, Union, Optional, cast

from eth_account import Account, messages
from eth_account.signers.local import LocalAccount
from eth_typing import URI
from web3 import HTTPProvider
from web3._utils.request import make_post_request
from web3.types import RPCEndpoint, RPCResponse
from web3 import Web3


def get_default_endpoint() -> URI:
    return URI(
        os.environ.get("FLASHBOTS_HTTP_PROVIDER_URI", "https://relay.flashbots.net")
    )


class FlashbotProvider(HTTPProvider):
    logger = logging.getLogger("web3.providers.FlashbotProvider")

    def __init__(
        self,
        signature_account: LocalAccount,
        endpoint_uri: Optional[Union[URI, str]] = None,
        request_kwargs: Optional[Any] = None,
        session: Optional[Any] = None,
    ):
        _endpoint_uri = endpoint_uri or get_default_endpoint()
        super().__init__(_endpoint_uri, request_kwargs, session)
        self.signature_account = signature_account

    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        self.logger.debug(
            "Making request HTTP. URI: %s, Method: %s", self.endpoint_uri, method
        )
        request_data = self.encode_rpc_request(method, params)

        message = messages.encode_defunct(
            text=Web3.keccak(text=request_data.decode("utf-8")).hex()
        )
        signed_message = Account.sign_message(
            message, private_key=self.signature_account.key.hex()
        )

        headers = self.get_request_headers() | {
            "X-Flashbots-Signature": f"{self.signature_account.address}:{signed_message.signature.hex()}"
        }

        try:
            raw_response = make_post_request(
                self.endpoint_uri, request_data, headers=headers
            ).decode()
        except Exception as e:
            traceback.print_exc()
            raw_response = str(e)
        # print(raw_response)
        # response = json.loads(response.decode())
        # response = self.decode_rpc_response(raw_response)
        # response = cast(RPCResponse, {'jsonrpc': '2.0', 'id':0, 'result': raw_response.decode()})
        self.logger.debug(
            "Getting response HTTP. URI: %s, " "Method: %s, Response: %s",
            self.endpoint_uri,
            method,
            raw_response,
        )
        return raw_response
