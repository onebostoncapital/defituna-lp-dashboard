# data/store/price_store.py

import pandas as pd

from data.router.price_router import (
    get_sol_price,
    get_sol_price_history
)

# -------------------------------------------------
# SINGLE SOURCE OF TRUTH FOR PRICE DATA
# -------------------------------------------------

def get_current_price():
    """
    Returns:
        float | None
    """
    try:
        price = get_sol_price()
        if price is None:
            return None
        return float(price)
    except Exception:
        return None


def get_price_history(days=200):
    """
    Returns:
        pandas.DataFrame with a 'close' column
        or None if unavailable
    """
    try:
        df = get_sol_price_history(days=days)

        if df is None or df.empty:
            return None

        # Normalize column name (CRITICAL)
        if "Close" in df.columns:
            df = df.rename(columns={"Close": "close"})

        if "close" not in df.columns:
            return None

        # Ensure numeric & clean
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df = df.dropna(subset=["close"])

        if df.empty:
            return None

        return df

    except Exception:
        return None
