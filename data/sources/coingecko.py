import requests
import pandas as pd


def get_sol_price_coingecko():
    """
    Fetch current SOL price from CoinGecko.
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "solana",
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return float(data["solana"]["usd"])
    except Exception:
        return None


def get_sol_price_history_coingecko(days: int = 200):
    """
    Fetch historical SOL prices from CoinGecko.
    Returns DataFrame with 'close' column.
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/solana/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        prices = data.get("prices", [])
        if not prices:
            return None

        df = pd.DataFrame(prices, columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        return df
    except Exception:
        return None
