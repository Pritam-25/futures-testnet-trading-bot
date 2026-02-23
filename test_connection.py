import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
secret_key = os.getenv("BINANCE_SECRET_KEY")

try:
    client = Client(api_key, secret_key)
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    # simple test call
    account_info = client.futures_account()

    print("✅ Connected Successfully to Binance Futures Testnet")
    print("Available Balance:", account_info["availableBalance"])

except BinanceAPIException as e:
    print("❌ Binance API Error:", e.message)

except Exception as e:
    print("❌ General Error:", str(e))