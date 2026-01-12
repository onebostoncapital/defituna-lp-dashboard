import requests
import pandas as pd

BASE_URL = "https://api.coingecko.com/api/v3"

def fetch_sol_price():
    try:
        url = f"{BASE_URL}/simple/price"
        params = {
            "ids": "solana",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["solana"]["usd"])
    except Exception as e:
        print("CoinGecko price error:", e)
        return None


def fetch_sol_price_history(days=200):
    try:
        url = f"{BASE_URL}/coins/solana/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        prices = data.get("prices", [])
        if not prices:
            return None

        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        return df["price"]

    except Exception as e:
        print("CoinGecko history error:", e)
        return None
