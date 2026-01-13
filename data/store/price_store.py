from data.sources.coingecko import get_sol_price as cg_price
from data.sources.yfinance_source import get_sol_price as yf_price

import pandas as pd
import yfinance as yf


# =============================
# CURRENT PRICE (MULTI-SOURCE)
# =============================

def get_current_price():
    price = cg_price()
    if price is not None:
        return price

    price = yf_price()
    if price is not None:
        return price

    return None


# =============================
# PRICE HISTORY (7D DEFAULT)
# =============================

def get_price_history(days: int = 7) -> pd.DataFrame:
    try:
        ticker = yf.Ticker("SOL-USD")
        df = ticker.history(period=f"{days}d", interval="1h")

        if df.empty or "Close" not in df:
            return pd.DataFrame()

        return pd.DataFrame({
            "close": df["Close"]
        })
    except Exception:
        return pd.DataFrame()
