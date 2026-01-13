# data/store/price_store.py

import pandas as pd
from data.sources.coingecko import (
    get_current_price_from_coingecko,
    get_price_history_from_coingecko
)

# ---------------------------------------------
# PUBLIC API — USED BY app/main.py
# ---------------------------------------------

def get_current_price(symbol: str) -> float | None:
    """
    Returns current price as FLOAT
    """
    try:
        price = get_current_price_from_coingecko(symbol)
        return float(price)
    except Exception:
        return None


def get_price_history(symbol: str, days: int = 7) -> pd.DataFrame | None:
    """
    Returns price history as DataFrame with column: close
    """
    try:
        raw = get_price_history_from_coingecko(symbol, days)

        if raw is None or len(raw) == 0:
            return None

        # EXPECTED raw = list of [timestamp, price]
        df = pd.DataFrame(raw, columns=["timestamp", "close"])
        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df = df.dropna().reset_index(drop=True)

        return df

    except Exception:
        return None
