import json
import logging
import websocket


class WsClient:
    def __init__(self, url, params) -> None:
        self.params = params
        self.url = url
        self.cli = websocket.WebSocket()

    def start(self):
        self.cli.connect(self.url)
        self.cli.send(
            json.dumps(
                {
                    "id": 1,
                    "jsonrpc": "2.0",
                    "method": "eth_subscribe",
                    "params": self.params,
                }
            )
        )
        response = json.loads(self.cli.recv())
        logging.info(f"start subscription: {self.params[0]}, {response}")
        return self

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, trace):
        self.cli.close()
        logging.info(f"stop subscription: {self.params[0]}")

    def __iter__(self):
        return map(lambda x: json.loads(x)['params']['result'], self.cli)