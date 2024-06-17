import base64
import hmac
import logging
import time
from contextlib import asynccontextmanager

import trio
import orjson
import trio_websocket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from trio_websocket import open_websocket_url

from trio_bybit.exceptions import BybitWebsocketOpError


class BybitSocketManager:
    URLS = {
        "main": {
            "spot": "wss://stream.bybit.com/v5/public/spot",
            "linear": "wss://stream.bybit.com/v5/public/linear",
            "inverse": "wss://stream.bybit.com/v5/public/inverse",
            "private": "wss://stream.bybit.com/v5/private",
        },
        "test": {
            "spot": "wss://stream-testnet.bybit.com/v5/public/spot",
            "linear": "wss://stream-testnet.bybit.com/v5/public/linear",
            "inverse": "wss://stream-testnet.bybit.com/v5/public/inverse",
            "private": "wss://stream-testnet.bybit.com/v5/private",
        },
        "demo": {
            "private": "wss://stream-demo.bybit.com",
        },
    }

    def __init__(
        self,
        endpoint: str = "spot",
        api_key: str | None = None,
        api_secret: str | None = None,
        api_secret_passphrase: bytes | None = None,
        alternative_net: str = "",
        sign_style: str = "HMAC",
    ):
        self.ws: trio_websocket.WebSocketConnection | None = None
        self.endpoint: str = endpoint
        self.alternative_net: str = alternative_net if alternative_net else "main"
        if self.endpoint == "private" and (api_key is None or api_secret is None):
            raise ValueError("api_key and api_secret must be provided for private streams")
        self.api_key = api_key
        self.api_secret = api_secret
        self.conn_id: str | None = None
        if sign_style != "HMAC":
            with open(api_secret, "rb") as f:
                self.api_secret = load_pem_private_key(f.read(), password=api_secret_passphrase)
        else:
            self.api_secret = api_secret
        self.sign_style = sign_style
        self.cancel_scope: trio.CancelScope | None = None

        self.connected = trio.Condition()
        self.subscribed = set()  # topics subscribed, for re-subscription

    @asynccontextmanager
    async def connect(self):
        """
        Asynchronous context manager to establish and maintain a WebSocket connection.

        This method attempts to connect to the specified WebSocket URL and manages the connection lifecycle.
        If the connection is closed, it will automatically attempt to reconnect.

        Note: this method will not end until forced to. A trio cancel scope could help.

        Yields:
            trio_websocket.WebSocketConnection: The active WebSocket connection.

        Raises:
            ValueError: If the specified endpoint and network combination is not supported.
            RuntimeError: If the connection context manager exits unexpectedly.
        """
        try:
            url = self.URLS[self.alternative_net][self.endpoint]
        except KeyError:
            raise ValueError(f"endpoint {self.endpoint} with net {self.alternative_net} not supported")

        async def _conn(task_status=trio.TASK_STATUS_IGNORED):
            with trio.CancelScope() as scope:
                async with open_websocket_url(url) as websock:
                    self.ws = websock
                    if self.endpoint == "private":
                        await self._send_signature()
                    if self.subscribed:
                        await self.subscribe({"op": "subscribe", "args": list(self.subscribed)})
                    task_status.started(scope)
                    async with self.connected:
                        self.connected.notify_all()
                    await self.heartbeat()

        while True:
            async with trio.open_nursery() as nursery:
                self.cancel_scope = await nursery.start(_conn)
                yield self.ws

            if self.cancel_scope.cancelled_caught:  # connection closed
                logging.info("Connection closed, restarting...")
                continue  # restarting connection
            else:  # should not come here
                raise RuntimeError("Unexpected exit from websocket connection context manager.")

    async def _send_message(self, message: str | bytes):
        """
        Sends a message through the WebSocket connection.

        This method ensures that messages are sent through the WebSocket connection
        and handles the `ConnectionClosed` exception by cancelling the current scope,
        which will trigger a reconnection.

        Parameters:
            message (str | bytes): The message to be sent through the WebSocket.
        """
        try:
            await self.ws.send_message(message)
        except trio_websocket.ConnectionClosed:
            self.cancel_scope.cancel()
            async with self.connected:
                await self.connected.wait()
                await self.ws.send_message(message)

    async def _get_message(self) -> str | bytes:
        """
        Retrieve a message from the WebSocket connection.

        This method attempts to get a message from the WebSocket connection. If the connection
        is closed, it cancels the current scope to trigger a reconnection.

        Returns:
            str | bytes: The message received from the WebSocket connection.
        """
        try:
            return await self.ws.get_message()
        except trio_websocket.ConnectionClosed:
            self.cancel_scope.cancel()
            async with self.connected:
                await self.connected.wait()
                await self.ws.get_message()

    async def heartbeat(self):
        while True:
            with trio.fail_after(5):
                await self._send_message('{"op": "ping"}')
            await trio.sleep(20)

    async def _send_signature(self):
        expires = int((time.time() + 1) * 1000)
        if self.sign_style == "HMAC":
            signature = str(
                hmac.new(
                    self.api_secret.encode("utf-8"), f"GET/realtime{expires}".encode("utf-8"), digestmod="sha256"
                ).hexdigest()
            )
        else:  # RSA
            signature = self.api_secret.sign(
                f"GET/realtime{expires}".encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
            )
            signature = base64.b64encode(signature).decode()
        await self._send_message(orjson.dumps({"op": "auth", "args": [self.api_key, expires, signature]}))
        auth_ret = orjson.loads(await self._get_message())
        if auth_ret["op"] == "auth":
            try:
                assert auth_ret["success"]
            except AssertionError:
                raise BybitWebsocketOpError(auth_ret)
            self.conn_id = auth_ret["conn_id"]

    async def subscribe(self, subscription: dict):
        """
        Subscribe or unsubscribe to a websocket stream.

        Parameters:
            subscription (dict): (un)subscription message, e.g. {"op": "subscribe", "args": ["publicTrade.BTCUSDT"]}
        """
        if subscription["op"] == "subscribe":
            self.subscribed.update(subscription["args"])
        elif subscription["op"] == "unsubscribe":
            self.subscribed.difference_update(subscription["args"])
        else:
            raise ValueError(f"op must be 'subscribe' or 'unsubscribe', but received \'{subscription["op"]}\'")
        await self._send_message(orjson.dumps(subscription))

    async def get_next_message(self):
        """
        Continuously retrieves messages from the WebSocket connection.

        Yields:
            dict: The message received from the WebSocket connection containing "topic" and "data".
        """
        while True:
            raw_message = await self._get_message()
            message = orjson.loads(raw_message)
            if "topic" in message and "data" in message:
                yield message
            elif "op" in message:
                if message["op"] == "pong":
                    continue
                if not message.get("success"):  # probably a subscription error
                    raise BybitWebsocketOpError(raw_message)
