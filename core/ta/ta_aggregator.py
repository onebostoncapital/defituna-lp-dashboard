from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.ma_crossover import calculate_ma_crossover
from core.ta.rsi import calculate_rsi
from core.ta.volatility import calculate_volatility
from core.ta.trend_strength import calculate_trend_strength


def aggregate_ta_signals(price_series):
    """
    Aggregate all TA indicators into one TA signal.
    """

    ta_results = {
        "ma20": calculate_ma20(price_series),
        "ma200": calculate_ma200(price_series),
        "crossover": calculate_ma_crossover(price_series),
        "rsi": calculate_rsi(price_series),
        "volatility": calculate_volatility(price_series),
        "trend_strength": calculate_trend_strength(price_series),
    }

    total_score = sum(item["score"] for item in ta_results.values())

    # -----------------------------
    # Direction decision
    # -----------------------------
    if total_score > 20:
        direction = "Bullish"
    elif total_score < -20:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # -----------------------------
    # Confidence calculation (centralized)
    # -----------------------------
    max_possible_score = 95  # sum of max scores
    confidence = min(abs(total_score) / max_possible_score, 1.0)

    # -----------------------------
    # AI-style confidence multiplier
    # -----------------------------
    if abs(total_score) > 50:
        confidence_multiplier = 1.2
    elif abs(total_score) < 20:
        confidence_multiplier = 0.8
    else:
        confidence_multiplier = 1.0

    drivers = [item["driver"] for item in ta_results.values() if item["driver"]]

    return {
        "direction": direction,
        "score": total_score,
        "confidence": round(confidence, 2),
        "confidence_multiplier": confidence_multiplier,
        "drivers": drivers,
        "raw": ta_results
    }
