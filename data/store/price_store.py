# data/store/price_store.py

import pandas as pd
from datetime import datetime, timedelta

from data.router.price_router import (
    get_sol_price,
    get_sol_price_history
)

# -----------------------------
# INTERNAL CACHE (IN-MEMORY)
# -----------------------------
_price_cache = {
    "current": None,
    "history": None,
    "last_updated": None
}

CACHE_TTL_SECONDS = 60  # refresh once per minute


# -----------------------------
# HELPERS
# -----------------------------
def _cache_valid():
    if _price_cache["last_updated"] is None:
        return False

    return (datetime.utcnow() - _price_cache["last_updated"]).seconds < CACHE_TTL_SECONDS


# -----------------------------
# PUBLIC API (USED BY APP)
# -----------------------------
def get_current_price():
    """
    Returns: float or None
    """
    if _cache_valid() and _price_cache["current"] is not None:
        return _price_cache["current"]

    price = get_sol_price()

    if price is None:
        return None

    _price_cache["current"] = float(price)
    _price_cache["last_updated"] = datetime.utcnow()

    return _price_cache["current"]


def get_price_history(days: int = 200):
    """
    Returns: pandas Series (price only) or None
    """
    if _cache_valid() and _price_cache["history"] is not None:
        return _price_cache["history"]

    df = get_sol_price_history(days=days)

    if df is None or len(df) == 0:
        return None

    # 🔴 CRITICAL FIX:
    # Ensure TA always receives a CLEAN SERIES
    if isinstance(df, pd.DataFrame):
        if "close" in df.columns:
            series = df["close"].astype(float)
        else:
            series = df.iloc[:, 0].astype(float)
    else:
        series = pd.Series(df).astype(float)

    series = series.dropna()

    _price_cache["history"] = series
    _price_cache["last_updated"] = datetime.utcnow()

    return series
