import pandas as pd
import time

from data.sources.coingecko import (
    get_sol_price_coingecko,
    get_sol_price_history_coingecko
)

from data.sources.yfinance_source import (
    get_sol_price_yfinance,
    get_sol_price_history_yfinance
)

# =================================================
# SIMPLE IN-MEMORY CACHE (Streamlit-safe)
# =================================================
_CACHE = {
    "price": None,
    "history": None,
    "timestamp": 0
}

CACHE_TTL = 60  # seconds


# =================================================
# CURRENT PRICE
# =================================================
def get_current_price():
    global _CACHE

    now = time.time()

    # Return cached value if fresh
    if _CACHE["price"] is not None and now - _CACHE["timestamp"] < CACHE_TTL:
        return _CACHE["price"]

    # 1️⃣ Try yfinance first
    try:
        price = get_sol_price_yfinance()
        if price is not None:
            _CACHE["price"] = float(price)
            _CACHE["timestamp"] = now
            return _CACHE["price"]
    except Exception:
        pass

    # 2️⃣ Fallback to CoinGecko (MOST RELIABLE ON STREAMLIT)
    try:
        price = get_sol_price_coingecko()
        if price is not None:
            _CACHE["price"] = float(price)
            _CACHE["timestamp"] = now
            return _CACHE["price"]
    except Exception:
        pass

    # ❌ Total failure (very rare)
    return None


# =================================================
# PRICE HISTORY
# =================================================
def get_price_history(days=200):
    global _CACHE

    now = time.time()

    # Return cached history if fresh
    if _CACHE["history"] is not None and now - _CACHE["timestamp"] < CACHE_TTL:
        return _CACHE["history"]

    # 1️⃣ Try yfinance
    try:
        df = get_sol_price_history_yfinance(days=days)
        if isinstance(df, pd.DataFrame) and not df.empty:
            _CACHE["history"] = df
            _CACHE["timestamp"] = now
            return df
    except Exception:
        pass

    # 2️⃣ Fallback to CoinGecko
    try:
        df = get_sol_price_history_coingecko(days=days)
        if isinstance(df, pd.DataFrame) and not df.empty:
            _CACHE["history"] = df
            _CACHE["timestamp"] = now
            return df
    except Exception:
        pass

    # ❌ Total failure
    return None
