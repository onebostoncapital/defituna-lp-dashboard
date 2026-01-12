import pandas as pd
import numpy as np


def calculate_volatility(price_series, lookback=20):
    """
    Returns volatility as a FLOAT percentage.
    MASTER RULE: no Pandas objects leave this function.
    """

    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    if len(price_series) < lookback + 1:
        return 0.0

    # Log returns for stability
    log_returns = np.log(price_series / price_series.shift(1)).dropna()

    if log_returns.empty:
        return 0.0

    volatility = log_returns[-lookback:].std()

    # Convert to percentage
    volatility_pct = float(volatility * 100)

    if np.isnan(volatility_pct) or np.isinf(volatility_pct):
        return 0.0

    return round(volatility_pct, 2)
