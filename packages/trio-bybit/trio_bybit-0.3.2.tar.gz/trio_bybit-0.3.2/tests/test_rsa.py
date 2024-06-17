import os

from trio_bybit.client import AsyncClient

# Generate key pair by 3 steps: generate pairs file, extract pub key and private key
# openssl genrsa -out keypair.pem 2048
# openssl rsa -in keypair.pem -pubout -out publickey.crt
# openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in keypair.pem -out pkcs8.key


async def test_get_wallet():
    client = await AsyncClient.create(
        api_key=os.getenv("BYBIT_API_KEY"),
        api_secret=os.getenv("BYBIT_PRIVATE_KEY_PATH"),
        sign_style="RSA",
    )

    async with client:
        wallet = await client.get_wallet_balance(accountType="UNIFIED")
        assert wallet["retCode"] == 0
        assert wallet["retMsg"] == "OK"
        assert wallet["result"]["list"][0]["accountType"] == "UNIFIED"
        position = await client.get_position_info(category="linear", settleCoin="USDT")
        assert position["retCode"] == 0
        assert position["retMsg"] == "OK"
