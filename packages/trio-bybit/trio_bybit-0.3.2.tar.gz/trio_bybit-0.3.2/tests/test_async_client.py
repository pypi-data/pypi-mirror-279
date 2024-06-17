import os
import trio
import pytest_trio

from trio_bybit.client import AsyncClient


async def test_get_public():
    client = await AsyncClient.create()
    async with client:
        server_time = await client.get_server_time()
        assert isinstance(server_time, dict)
        assert server_time["retCode"] == 0
        assert server_time["retMsg"] == "OK"
        assert "timeSecond" in server_time["result"]
        assert "timeNano" in server_time["result"]
        assert "time" in server_time

        symbol_info = await client.get_symbol_info(category="linear", symbol="BTCUSDT")
        assert isinstance(symbol_info, dict)
        assert symbol_info["retCode"] == 0
        assert symbol_info["retMsg"] == "OK"
        assert symbol_info["result"]["category"] == "linear"
        assert symbol_info["result"]["list"][0]["symbol"] == "BTCUSDT"
        assert symbol_info["result"]["list"][0]["contractType"] == "LinearPerpetual"
        assert symbol_info["result"]["list"][0]["status"] == "Trading"
        assert symbol_info["result"]["list"][0]["baseCoin"] == "BTC"
        assert symbol_info["result"]["list"][0]["quoteCoin"] == "USDT"

        orderbook = await client.get_orderbook(category="linear", symbol="BTCUSDT")
        assert orderbook["retCode"] == 0
        assert orderbook["retMsg"] == "OK"


async def test_get_private():
    client = await AsyncClient.create(
        api_key=os.getenv("BYBIT_API_KEY"),
        api_secret=os.getenv("BYBIT_API_SECRET"),
        # alternative_net="demo",
    )

    async with client:
        wallet = await client.get_wallet_balance(accountType="UNIFIED")
        assert wallet["retCode"] == 0
        assert wallet["retMsg"] == "OK"
        assert wallet["result"]["list"][0]["accountType"] == "UNIFIED"
        position = await client.get_position_info(category="linear", settleCoin="USDT")
        assert position["retCode"] == 0
        assert position["retMsg"] == "OK"
