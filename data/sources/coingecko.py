import requests
import pandas as pd
from datetime import datetime

COINGECKO_API = "https://api.coingecko.com/api/v3"


def fetch_price_history(symbol: str, days: int = 7) -> pd.DataFrame:
    try:
        url = f"{COINGECKO_API}/coins/{symbol}/market_chart"
        params = {"vs_currency": "usd", "days": days}

        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()

        prices = r.json().get("prices", [])
        if not prices:
            raise ValueError("Empty price data from CoinGecko")

        df = pd.DataFrame(prices, columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        return df[["close"]]

    except Exception as e:
        raise RuntimeError(f"CoinGecko price fetch failed: {e}")
