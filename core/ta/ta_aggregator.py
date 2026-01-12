from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.ma_crossover import calculate_ma_crossover
from core.ta.rsi import calculate_rsi
from core.ta.volatility import calculate_volatility
from core.ta.trend_strength import calculate_trend_strength


def aggregate_ta_signals(price_series):
    """
    Aggregates all TA indicators using price SERIES (master rule).
    """

    ma20 = calculate_ma20(price_series)
    ma200 = calculate_ma200(price_series)
    crossover = calculate_ma_crossover(price_series)
    rsi = calculate_rsi(price_series)
    volatility_pct = calculate_volatility(price_series)
    trend = calculate_trend_strength(price_series)

    drivers = [
        f"MA20: {ma20['signal']}",
        f"MA200: {ma200['signal']}",
        f"Crossover: {crossover['signal']}",
        f"RSI: {rsi['signal']}",
        f"Trend Strength: {trend['signal']}"
    ]

    ta_score = (
        ma20["confidence"]
        + ma200["confidence"]
        + crossover["confidence"]
        + rsi["confidence"]
        + trend["confidence"]
    )

    return {
        "ta_score": round(ta_score, 2),
        "volatility_pct": volatility_pct,
        "trend": trend["signal"],
        "drivers": drivers
    }
