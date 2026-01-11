import pandas as pd
import numpy as np


def detect_market_regime(price_series: pd.Series) -> str:
    """
    Detect market regime:
    - Trending
    - Choppy
    - High-Risk
    """

    if len(price_series) < 60:
        return "Unknown"

    # -----------------------------
    # Moving averages
    # -----------------------------
    ma_fast = price_series.rolling(20).mean()
    ma_slow = price_series.rolling(50).mean()

    spread = ma_fast - ma_slow

    spread_latest = float(spread.iloc[-1])

    # -----------------------------
    # Trend slope (last 20 periods)
    # -----------------------------
    recent_prices = price_series.iloc[-20:]
    x = np.arange(len(recent_prices))
    slope = float(np.polyfit(x, recent_prices.values, 1)[0])

    # -----------------------------
    # Volatility comparison
    # -----------------------------
    returns = price_series.pct_change().dropna()

    recent_vol = float(returns.iloc[-20:].std())
    long_vol = float(returns.iloc[-60:].std())

    # -----------------------------
    # Regime rules
    # -----------------------------
    if abs(spread_latest) > 1.0 and abs(slope) > 0.01 and recent_vol <= long_vol:
        return "Trending"

    if recent_vol > long_vol * 1.5:
        return "High-Risk"

    return "Choppy"
