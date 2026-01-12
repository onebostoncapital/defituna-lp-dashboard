# =================================================
# PRICE STORE
# Centralized price cache + access layer
# =================================================

from data.router.price_router import (
    get_sol_price,
    get_sol_price_history
)

# -------------------------------------------------
# In-memory cache (simple + safe)
# -------------------------------------------------
_PRICE_CACHE = {
    "current": None,
    "history": None
}

# -------------------------------------------------
# Public API
# -------------------------------------------------
def get_current_price(force_refresh: bool = False):
    """
    Returns latest SOL price (float)
    """
    if _PRICE_CACHE["current"] is None or force_refresh:
        try:
            _PRICE_CACHE["current"] = get_sol_price()
        except Exception:
            _PRICE_CACHE["current"] = None

    return _PRICE_CACHE["current"]


def get_price_history(days: int = 200, force_refresh: bool = False):
    """
    Returns SOL price history (pandas Series)
    """
    if _PRICE_CACHE["history"] is None or force_refresh:
        try:
            _PRICE_CACHE["history"] = get_sol_price_history(days=days)
        except Exception:
            _PRICE_CACHE["history"] = None

    return _PRICE_CACHE["history"]
