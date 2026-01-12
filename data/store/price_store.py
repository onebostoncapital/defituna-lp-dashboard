import pandas as pd
from datetime import datetime

from data.router.price_router import (
    get_sol_price,
    get_sol_price_history
)

# =================================================
# INTERNAL CACHE (IN-MEMORY)
# =================================================
_PRICE_CACHE = {
    "current_price": None,
    "history": None,
    "last_updated": None
}

CACHE_TTL_SECONDS = 60  # refresh every 60 seconds


# =================================================
# CURRENT PRICE
# =================================================
def get_current_price(force_refresh: bool = False):
    try:
        if (
            not force_refresh
            and _PRICE_CACHE["current_price"] is not None
            and _PRICE_CACHE["last_updated"] is not None
        ):
            return float(_PRICE_CACHE["current_price"])

        price = get_sol_price()

        if price is None:
            return None

        _PRICE_CACHE["current_price"] = float(price)
        _PRICE_CACHE["last_updated"] = datetime.utcnow()

        return float(price)

    except Exception as e:
        print("Price Store error (current price):", e)
        return None


# =================================================
# HISTORICAL PRICE
# =================================================
def get_price_history(days: int = 200, force_refresh: bool = False):
    try:
        if (
            not force_refresh
            and _PRICE_CACHE["history"] is not None
        ):
            return _PRICE_CACHE["history"]

        history = get_sol_price_history(days=days)

        if history is None or len(history) == 0:
            return None

        # Ensure Pandas Series
        if not isinstance(history, pd.Series):
            history = pd.Series(history)

        history = pd.to_numeric(history, errors="coerce").dropna()

        if history.empty:
            return None

        _PRICE_CACHE["history"] = history
        _PRICE_CACHE["last_updated"] = datetime.utcnow()

        return history

    except Exception as e:
        print("Price Store error (history):", e)
        return None
