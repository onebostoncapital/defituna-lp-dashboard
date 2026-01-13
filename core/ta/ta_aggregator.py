import pandas as pd

from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.rsi import calculate_rsi
from core.ta.trend_strength import calculate_trend_strength
from core.ta.volatility import calculate_volatility_regime


def aggregate_ta_signals(price_df: pd.DataFrame) -> dict:
    """
    Aggregates all TA signals into a single normalized output.
    Safe by design: never raises, never breaks dashboard.
    """

    if price_df is None or len(price_df) < 30:
        return {
            "ta_score": 0.0,
            "volatility_regime": "Unavailable",
            "trend_strength": "Unavailable",
            "drivers": []
        }

    close = price_df["close"]

    drivers = []
    score = 0.0

    # MA20
    ma20 = calculate_ma20(close)
    if ma20["signal"] != "Unavailable":
        drivers.append(f"MA20: {ma20['signal']}")
        score += ma20["score"]

    # MA200
    ma200 = calculate_ma200(close)
    if ma200["signal"] != "Unavailable":
        drivers.append(f"MA200: {ma200['signal']}")
        score += ma200["score"]

    # RSI
    rsi = calculate_rsi(close)
    if rsi["signal"] != "Unavailable":
        drivers.append(f"RSI: {rsi['signal']}")
        score += rsi["score"]

    # Trend Strength
    trend = calculate_trend_strength(close)
    if trend["signal"] != "Unavailable":
        drivers.append(f"Trend: {trend['signal']}")

    # Volatility Regime
    volatility = calculate_volatility_regime(close)

    # Normalize score to [-1, +1]
    ta_score = max(min(score / 3.0, 1.0), -1.0)

    return {
        "ta_score": round(ta_score, 2),
        "volatility_regime": volatility,
        "trend_strength": trend["signal"],
        "drivers": drivers
    }
