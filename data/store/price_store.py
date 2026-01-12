# data/store/price_store.py

import pandas as pd
import requests
from datetime import datetime, timedelta


# ======================================================
# INTERNAL HELPERS
# ======================================================

def _fetch_coingecko(symbol: str, days: int):
    try:
        url = "https://api.coingecko.com/api/v3/coins/solana/market_chart"
        params = {"vs_currency": "usd", "days": days}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()

        prices = r.json()["prices"]
        df = pd.DataFrame(prices, columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        df["close"] = df["close"].astype(float)

        return df

    except Exception:
        return None


def _fetch_yfinance(symbol: str, days: int):
    try:
        import yfinance as yf

        ticker = yf.Ticker(f"{symbol}-USD")
        hist = ticker.history(period=f"{days}d")

        if hist.empty:
            return None

        df = hist[["Close"]].copy()
        df.columns = ["close"]
        df.index = pd.to_datetime(df.index)

        return df

    except Exception:
        return None


# ======================================================
# PUBLIC API (USED BY APP)
# ======================================================

def get_price_history(symbol: str, days: int = 7) -> pd.DataFrame:
    """
    Returns DataFrame with:
    - index: datetime
    - column: close (float)
    """

    # 1️⃣ Try CoinGecko first
    df = _fetch_coingecko(symbol, days)
    if df is not None and not df.empty:
        return df

    # 2️⃣ Fallback to Yahoo Finance
    df = _fetch_yfinance(symbol, days)
    if df is not None and not df.empty:
        return df

    # 3️⃣ HARD FAIL (controlled)
    return pd.DataFrame(columns=["close"])


def get_current_price(symbol: str) -> float | None:
    """
    Returns latest price as float or None
    """

    df = get_price_history(symbol, days=1)

    if df.empty:
        return None

    try:
        return float(df["close"].iloc[-1])
    except Exception:
        return None
