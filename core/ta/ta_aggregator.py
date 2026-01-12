"""
TA Aggregator

IMPORTANT ARCHITECTURE RULE:
- This module MUST NEVER fetch price data
- It ONLY accepts price_series as input
- Price fetching is handled by data.store.price_store
"""

from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.ma_crossover import calculate_ma_crossover
from core.ta.rsi import calculate_rsi
from core.ta.volatility import calculate_volatility
from core.ta.trend_strength import calculate_trend_strength


def aggregate_ta_signals(price_series):
    """
    Aggregate all TA indicators into a single TA score.
    price_series MUST be a pandas Series of prices.
    """

    if price_series is None or len(price_series) < 50:
        return {
            "ta_score": 0.0,
            "drivers": []
        }

    indicators = {
        "MA20": calculate_ma20(price_series),
        "MA200": calculate_ma200(price_series),
        "Crossover": calculate_ma_crossover(price_series),
        "RSI": calculate_rsi(price_series),
        "Volatility": calculate_volatility(price_series),
        "Trend Strength": calculate_trend_strength(price_series),
    }

    total_score = 0.0
    drivers = []

    for name, result in indicators.items():
        if not isinstance(result, dict):
            continue

        score = float(result.get("score", 0.0))
        confidence = float(result.get("confidence", 0.0))
        signal = result.get("signal", "Neutral")

        total_score += score * confidence

        if signal != "Neutral":
            drivers.append(f"{name}: {signal}")

    return {
        "ta_score": round(total_score, 3),
        "drivers": drivers
    }
