# core/ta/ta_aggregator.py

from core.ta.rsi import calculate_rsi
from core.ta.ma_20 import calculate_ma20
from core.ta.trend_strength import calculate_trend_strength
from core.ta.volatility import calculate_volatility


def _score_signal(signal: str) -> float:
    """
    Convert qualitative signal into numeric score.
    """
    if signal == "Bullish":
        return 1.0
    if signal == "Neutral":
        return 0.5
    if signal == "Bearish":
        return 0.0
    return 0.0


def aggregate_ta_signals(price_df):
    """
    Aggregate TA indicators into:
    - TA Score (0–1)
    - Volatility regime
    - Trend strength
    - Human-readable drivers
    """

    drivers = []

    # --- RSI ---
    rsi_signal = calculate_rsi(price_df)
    rsi_score = _score_signal(rsi_signal["signal"])
    drivers.append(f"RSI: {rsi_signal['signal']}")

    # --- MA20 ---
    ma20_signal = calculate_ma20(price_df)
    ma20_score = _score_signal(ma20_signal["signal"])
    drivers.append(f"MA20: {ma20_signal['signal']}")

    # --- Trend ---
    trend_signal = calculate_trend_strength(price_df)
    trend_score = _score_signal(trend_signal["signal"])
    drivers.append(f"Trend: {trend_signal['signal']}")

    # --- Volatility ---
    volatility = calculate_volatility(price_df)

    # --- Weighted TA Score ---
    ta_score = round(
        (0.30 * rsi_score) +
        (0.30 * ma20_score) +
        (0.40 * trend_score),
        2
    )

    return {
        "ta_score": ta_score,
        "volatility_regime": volatility["regime"],
        "trend_strength": trend_signal["signal"],
        "drivers": drivers,
    }
