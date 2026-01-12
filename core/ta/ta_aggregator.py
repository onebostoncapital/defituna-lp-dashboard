# =================================================
# TA AGGREGATOR (CONTRACT-STABLE)
# =================================================

import pandas as pd

from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.ma_crossover import calculate_ma_crossover
from core.ta.rsi import calculate_rsi
from core.ta.volatility import calculate_volatility
from core.ta.trend_strength import calculate_trend_strength


def aggregate_ta_signals(price_series: pd.Series):
    """
    STANDARD RETURN CONTRACT:
    {
        ta_score: float,
        volatility_pct: float,
        drivers: list[str]
    }
    """

    drivers = []
    score = 0.0

    # -----------------------------
    # Individual indicators
    # -----------------------------
    ma20 = calculate_ma20(price_series)
    ma200 = calculate_ma200(price_series)
    crossover = calculate_ma_crossover(price_series)
    rsi = calculate_rsi(price_series)
    trend = calculate_trend_strength(price_series)
    volatility_pct = calculate_volatility(price_series)

    # -----------------------------
    # Human-readable drivers
    # -----------------------------
    drivers.append(f"MA20 signal: {ma20['signal']}")
    drivers.append(f"MA200 signal: {ma200['signal']}")
    drivers.append(f"MA crossover: {crossover['signal']}")
    drivers.append(f"RSI: {rsi['signal']}")
    drivers.append(f"Trend strength: {trend['signal']}")

    # -----------------------------
    # Scoring
    # -----------------------------
    score += ma20["score"]
    score += ma200["score"]
    score += crossover["score"]
    score += rsi["score"]
    score += trend["score"]

    ta_score = round(score / 5.0, 2)

    return {
        "ta_score": ta_score,
        "volatility_pct": volatility_pct,
        "drivers": drivers
    }
