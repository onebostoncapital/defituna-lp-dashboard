# =================================================
# VOLATILITY INDICATOR (ULTRA SAFE)
# Accepts Series OR DataFrame
# Always returns ONE float
# =================================================

import pandas as pd
import numpy as np


def calculate_volatility(price_input, window: int = 14) -> float:
    """
    Calculates volatility percentage.
    Accepts:
    - pd.Series
    - pd.DataFrame with 'close' or 'price' column
    Returns:
    - float
    """

    if price_input is None:
        return 0.0

    # ---------------------------------------------
    # STEP 1: Extract Series safely
    # ---------------------------------------------
    if isinstance(price_input, pd.DataFrame):
        if "close" in price_input.columns:
            price_series = price_input["close"]
        elif "price" in price_input.columns:
            price_series = price_input["price"]
        else:
            return 0.0
    elif isinstance(price_input, pd.Series):
        price_series = price_input
    else:
        return 0.0

    # ---------------------------------------------
    # STEP 2: Clean data
    # ---------------------------------------------
    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    if len(price_series) < window:
        return 0.0

    # ---------------------------------------------
    # STEP 3: Compute volatility
    # ---------------------------------------------
    returns = price_series.pct_change().dropna()

    if len(returns) < window:
        return 0.0

    volatility_series = returns.rolling(window).std()

    latest = volatility_series.iloc[-1]

    try:
        latest_float = float(latest)
    except Exception:
        return 0.0

    if np.isnan(latest_float):
        return 0.0

    return round(latest_float * 100, 2)
