import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()


class BinanceFuturesClient:
    """Wrapper around python-binance Client. Defaults to futures testnet.

    Pass `testnet=False` to use production endpoints.
    """

    def __init__(self, testnet: bool = True):
        api_key = os.getenv("BINANCE_API_KEY")
        secret_key = os.getenv("BINANCE_SECRET_KEY")

        if not api_key or not secret_key:
            raise ValueError("API keys not found in environment variables")

        self.client = Client(api_key, secret_key)

        if testnet:
            # Configure futures testnet endpoint used by python-binance
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def get_client(self):
        return self.client