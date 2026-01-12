from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.ma_crossover import calculate_ma_crossover
from core.ta.rsi import calculate_rsi
from core.ta.trend_strength import calculate_trend_strength
from core.ta.volatility import calculate_volatility

def aggregate_ta_signals(price_df):
    ma20 = calculate_ma20(price_df)
    ma200 = calculate_ma200(price_df)
    crossover = calculate_ma_crossover(price_df)
    rsi = calculate_rsi(price_df)
    trend = calculate_trend_strength(price_df)
    volatility = calculate_volatility(price_df)

    ta_score = (
        ma20["score"] +
        ma200["score"] +
        crossover["score"] +
        rsi["score"] +
        trend["score"]
    )

    drivers = [
        f"MA20: {ma20['signal']}",
        f"MA200: {ma200['signal']}",
        f"Crossover: {crossover['signal']}",
        f"RSI: {rsi['signal']}",
        f"Trend Strength: {trend['signal']}",
    ]

    return {
        "ta_score": ta_score,
        "volatility_pct": volatility,
        "drivers": drivers
    }
