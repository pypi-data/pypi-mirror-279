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


class BloxProvider(HTTPProvider):
    def __init__(
        self,
        endpoint_uri="https://mev.api.blxrbdn.com",
        auth="",
        request_kwargs=None,
        session=None,
    ) -> None:
        if not auth:
            raise Exception("require blox auth header")
        self.auth = auth
        super().__init__(endpoint_uri, request_kwargs, session)

    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        params = params[0]
        self.logger.debug(
            "Making request HTTP. URI: %s, Method: %s", self.endpoint_uri, method
        )

        params = {
                "transaction": [i[2:] for i in params["txs"]],
                "block_number": params["blockNumber"],
                "mev_builders": {
                    "bloxroute": "",
                    "all": "",
                },
            }
        rpc_dict = {
            "jsonrpc": "2.0",
            "method": "blxr_submit_bundle",
            "params": params or [],
            "id": str(next(self.request_counter)),
        }

        try:
            raw_response = make_post_request(
                self.endpoint_uri,
                None,
                json=rpc_dict,
                headers={"Authorization": self.auth},
            ).decode()
        except Exception as e:
            traceback.print_exc()
            raw_response = str(e)
        self.logger.debug(
            "Getting response HTTP. URI: %s, " "Method: %s, Response: %s",
            self.endpoint_uri,
            method,
            raw_response,
        )
        return raw_response
