"""
Centralized Price Store
Single source of truth for price data
"""

from typing import Optional, Tuple
from datetime import datetime, timedelta

from data.router.price_router import (
    get_sol_price,
    get_sol_price_history
)

# -----------------------------
# INTERNAL CACHE
# -----------------------------
_cached_price: Optional[float] = None
_cached_history = None
_last_updated: Optional[datetime] = None

CACHE_TTL_SECONDS = 60


# -----------------------------
# HELPERS
# -----------------------------
def _is_cache_valid() -> bool:
    if _last_updated is None:
        return False
    return (datetime.utcnow() - _last_updated) < timedelta(seconds=CACHE_TTL_SECONDS)


# -----------------------------
# PUBLIC API
# -----------------------------
def get_current_price() -> Optional[float]:
    global _cached_price, _last_updated

    if _is_cache_valid() and _cached_price is not None:
        return _cached_price

    price = get_sol_price()
    if price is not None:
        _cached_price = float(price)
        _last_updated = datetime.utcnow()

    return _cached_price


def get_price_history(days: int = 200):
    global _cached_history, _last_updated

    if _is_cache_valid() and _cached_history is not None:
        return _cached_history

    history = get_sol_price_history(days=days)
    if history is not None:
        _cached_history = history
        _last_updated = datetime.utcnow()

    return _cached_history
