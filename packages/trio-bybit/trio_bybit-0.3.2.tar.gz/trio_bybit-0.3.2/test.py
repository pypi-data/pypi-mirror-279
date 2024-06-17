import trio
import os

from trio_bybit import AsyncClient
from trio_bybit.streams import BybitSocketManager


async def main():
    socket = BybitSocketManager(
        endpoint="private",
        api_key="oJwzV0le5qsjkfslCf",
        api_secret="p2UKmTzwkkY4buKgr8ROr0SGhrp2sWd3XL2h",
    )
    async with socket.connect():
        subscription = {
            "op": "subscribe",
            "args": ["order"],
        }
        await socket.subscribe(subscription)

        async for msg in socket.get_next_message():
            print(msg)


if __name__ == "__main__":
    trio.run(main)
