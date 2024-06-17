import os

import trio
import pytest_trio

from trio_bybit.streams import BybitSocketManager


async def pub_stream_check(socket):
    async for msg in socket.get_next_message():
        assert "ts" in msg
        assert "type" in msg
        assert "data" in msg


async def pub_unsub(socket):
    unsub = {
        "op": "unsubscribe",
        "args": ["orderbook.1.BTCUSDT", "publicTrade.BTCUSDT"],
    }
    await socket.subscribe(unsub)


async def test_public_stream():
    socket = BybitSocketManager()
    with trio.move_on_after(12):
        async with socket.connect():
            subscription = {
                "op": "subscribe",
                "args": ["orderbook.1.BTCUSDT", "publicTrade.BTCUSDT"],
            }
            await socket.subscribe(subscription)
            async with trio.open_nursery() as nursery:
                nursery.start_soon(pub_stream_check, socket)
                await trio.sleep(10)
                nursery.start_soon(pub_unsub, socket)


async def test_public_linear_stream():
    socket = BybitSocketManager(endpoint="linear")
    with trio.move_on_after(30):
        async with socket.connect():
            subscription = {
                "op": "subscribe",
                "args": ["orderbook.1.BTCUSDT", "publicTrade.BTCUSDT"],
            }
            await socket.subscribe(subscription)

            async for msg in socket.get_next_message():
                if msg.get("topic") == "orderbook.1.BTCUSDT":
                    assert "topic" in msg
                    assert "type" in msg
                    assert "data" in msg
                    assert "s" in msg["data"]
                    assert "a" in msg["data"]
                    assert "b" in msg["data"]
                elif msg.get("topic") == "publicTrade.BTCUSDT":
                    assert "topic" in msg
                    assert "type" in msg
                    assert "data" in msg
                    assert "S" in msg["data"][0]
                    assert "v" in msg["data"][0]
                    assert "p" in msg["data"][0]


async def test_private_stream():
    socket = BybitSocketManager(
        endpoint="private",
        api_key=os.getenv("BYBIT_API_KEY"),
        api_secret=os.getenv("BYBIT_API_SECRET"),
    )
    with trio.move_on_after(100):
        async with socket.connect():
            subscription = {
                "op": "subscribe",
                "args": ["order"],
            }
            await socket.subscribe(subscription)

            async for msg in socket.get_next_message():
                print(msg)


async def test_private_stream_by_rsa_sig():
    socket = BybitSocketManager(
        endpoint="private",
        api_key=os.getenv("BYBIT_RSA_API_KEY"),
        api_secret=os.getenv("BYBIT_RSA_PRIVATE_KEY_PATH"),
        sign_style="RSA",
    )
    with trio.move_on_after(100):
        async with socket.connect():
            subscription = {
                "op": "subscribe",
                "args": ["order"],
            }
            await socket.subscribe(subscription)

            async for msg in socket.get_next_message():
                print(msg)
