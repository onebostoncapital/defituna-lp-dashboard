# =================================================
# VOLATILITY INDICATOR (SAFE VERSION)
# Always returns ONE float
# =================================================

import pandas as pd
import numpy as np


def calculate_volatility(price_series: pd.Series, window: int = 14) -> float:
    """
    Returns volatility as a single percentage float.
    No Pandas objects escape this function.
    """

    if price_series is None or len(price_series) < window:
        return 0.0

    # Ensure numeric
    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    if len(price_series) < window:
        return 0.0

    returns = price_series.pct_change().dropna()

    if len(returns) < window:
        return 0.0

    volatility_series = returns.rolling(window).std()

    # FORCE scalar extraction
    latest = volatility_series.iloc[-1]

    try:
        latest_float = float(latest)
    except Exception:
        return 0.0

    if np.isnan(latest_float):
        return 0.0

    return round(latest_float * 100, 2)
