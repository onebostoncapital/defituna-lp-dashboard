import time
import pandas as pd

# Import modules (NOT function names)
import data.sources.coingecko as coingecko
import data.sources.yfinance_source as yfinance


# =================================================
# SIMPLE CACHE
# =================================================
_CACHE = {
    "price": None,
    "history": None,
    "timestamp": 0
}

CACHE_TTL = 60  # seconds


# =================================================
# CURRENT PRICE (SAFE)
# =================================================
def get_current_price():
    global _CACHE
    now = time.time()

    if _CACHE["price"] is not None and now - _CACHE["timestamp"] < CACHE_TTL:
        return _CACHE["price"]

    # 1️⃣ Try yfinance
    try:
        if hasattr(yfinance, "get_sol_price"):
            price = yfinance.get_sol_price()
            if price is not None:
                _CACHE["price"] = float(price)
                _CACHE["timestamp"] = now
                return _CACHE["price"]
    except Exception:
        pass

    # 2️⃣ Try CoinGecko
    try:
        if hasattr(coingecko, "get_sol_price"):
            price = coingecko.get_sol_price()
            if price is not None:
                _CACHE["price"] = float(price)
                _CACHE["timestamp"] = now
                return _CACHE["price"]
    except Exception:
        pass

    return None


# =================================================
# PRICE HISTORY (SAFE)
# =================================================
def get_price_history(days=200):
    global _CACHE
    now = time.time()

    if _CACHE["history"] is not None and now - _CACHE["timestamp"] < CACHE_TTL:
        return _CACHE["history"]

    # 1️⃣ Try yfinance
    try:
        if hasattr(yfinance, "get_sol_price_history"):
            df = yfinance.get_sol_price_history(days=days)
            if isinstance(df, pd.DataFrame) and not df.empty:
                _CACHE["history"] = df
                _CACHE["timestamp"] = now
                return df
    except Exception:
        pass

    # 2️⃣ Try CoinGecko
    try:
        if hasattr(coingecko, "get_sol_price_history"):
            df = coingecko.get_sol_price_history(days=days)
            if isinstance(df, pd.DataFrame) and not df.empty:
                _CACHE["history"] = df
                _CACHE["timestamp"] = now
                return df
    except Exception:
        pass

    return None
