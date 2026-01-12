# =================================================
# VOLATILITY INDICATOR
# Returns SINGLE volatility percentage
# =================================================

import pandas as pd


def calculate_volatility(price_series: pd.Series, window: int = 14) -> float:
    """
    Calculates rolling volatility as a percentage.
    Returns ONE float value (not a Series).
    """

    if len(price_series) < window:
        return 0.0

    # Percentage returns
    returns = price_series.pct_change()

    # Rolling standard deviation
    volatility = returns.rolling(window).std()

    # Take the MOST RECENT value
    latest_volatility = volatility.iloc[-1]

    if pd.isna(latest_volatility):
        return 0.0

    # Convert to percentage
    return float(latest_volatility * 100)
