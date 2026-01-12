# =================================================
# TA AGGREGATOR
# Collects all technical indicators
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
    Returns:
    - ta_score
    - volatility_pct
    - ta_drivers (human-readable)
    """

    results = {}
    drivers = []
    score = 0.0

    # -----------------------------
    # Indicators
    # -----------------------------
    ma20 = calculate_ma20(price_series)
    ma200 = calculate_ma200(price_series)
    crossover = calculate_ma_crossover(price_series)
    rsi = calculate_rsi(price_series)
    volatility_pct = calculate_volatility(price_series)
    trend = calculate_trend_strength(price_series)

    results["ma20"] = ma20
    results["ma200"] = ma200
    results["crossover"] = crossover
    results["rsi"] = rsi
    results["trend"] = trend

    # -----------------------------
    # Drivers (text)
    # -----------------------------
    drivers.append(f"MA20: {ma20['signal'].capitalize()}")
    drivers.append(f"MA200: {ma200['signal'].capitalize()}")
    drivers.append(f"Crossover: {crossover['signal'].capitalize()}")
    drivers.append(f"RSI: {rsi['signal'].capitalize()}")
    drivers.append(f"Trend Strength: {trend['signal'].capitalize()}")

    # -----------------------------
    # Scoring
    # -----------------------------
    score += ma20["score"]
    score += ma200["score"]
    score += crossover["score"]
    score += rsi["score"]
    score += trend["score"]

    # Normalize TA score
    ta_score = score / 5.0

    return {
        "ta_score": round(ta_score, 2),
        "volatility_pct": round(volatility_pct, 2),
        "ta_drivers": drivers
    }
