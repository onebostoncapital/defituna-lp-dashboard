from core.ta.rsi import calculate_rsi
from core.ta.ma_20 import calculate_ma20
from core.ta.ma_200 import calculate_ma200
from core.ta.trend_strength import calculate_trend_strength
from core.ta.volatility import calculate_volatility


def aggregate_ta_signals(price_df):
    """
    Aggregates all TA indicators into a unified TA output.
    Safe by design: never raises.
    """

    if price_df is None or len(price_df) < 50:
        return {
            "ta_score": 0.0,
            "volatility_regime": "Unavailable",
            "trend_strength": "Unavailable",
            "drivers": []
        }

    drivers = []

    rsi = calculate_rsi(price_df)
    ma20 = calculate_ma20(price_df)
    ma200 = calculate_ma200(price_df)
    trend = calculate_trend_strength(price_df)
    volatility = calculate_volatility(price_df)

    score = 0.0

    for indicator in [rsi, ma20, ma200, trend]:
        score += indicator["score"]
        drivers.append(indicator["label"])

    return {
        "ta_score": round(score, 2),
        "volatility_regime": volatility["regime"],
        "trend_strength": trend["label"],
        "drivers": drivers
    }
