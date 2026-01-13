import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://api.coingecko.com/api/v3"

def fetch_price_history(symbol: str, days: int = 7) -> pd.DataFrame:
    symbol = symbol.lower()
    url = f"{BASE_URL}/coins/{symbol}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    prices = r.json().get("prices", [])
    if not prices:
        return pd.DataFrame()

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    return df
