from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.rsi import calculate_rsi
from core.ta.trend_strength import calculate_trend_strength
from core.ta.volatility import calculate_volatility

def aggregate_ta_signals(price_df):
    drivers = []

    ma20 = calculate_ma20(price_df)
    ma200 = calculate_ma200(price_df)
    rsi = calculate_rsi(price_df)
    trend = calculate_trend_strength(price_df)
    volatility = calculate_volatility(price_df)

    for name, obj in [
        ("MA20", ma20),
        ("MA200", ma200),
        ("RSI", rsi),
        ("Trend", trend),
    ]:
        if obj["signal"] != "Unavailable":
            drivers.append(f"{name}: {obj['signal']}")

    ta_score = (
        ma20["score"]
        + ma200["score"]
        + rsi["score"]
        + trend["score"]
    )

    return {
        "ta_score": ta_score,
        "volatility_pct": volatility["value"] or 0.0,
        "trend": trend["signal"],
        "drivers": drivers
    }
