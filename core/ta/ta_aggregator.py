from core.ta.rsi import calculate_rsi
from core.ta.ma_20 import ma_20
from core.ta.ma_200 import ma_200
from core.ta.trend_strength import trend_strength

def run_ta(price_df):
    price_series = price_df["price"]
    drivers = []
    score = 50

    rsi = calculate_rsi(price_series)
    if rsi is not None:
        if rsi < 30:
            drivers.append("RSI: Oversold (Bullish)")
            score += 15
        elif rsi > 70:
            drivers.append("RSI: Overbought (Bearish)")
            score -= 15
        else:
            drivers.append("RSI: Neutral")

    ma20 = ma_20(price_series)
    if ma20 is True:
        drivers.append("MA20: Bullish")
        score += 10
    elif ma20 is False:
        drivers.append("MA20: Bearish")
        score -= 10
    else:
        drivers.append("MA20: Insufficient data")

    ma200 = ma_200(price_series)
    if ma200 is True:
        drivers.append("MA200: Bullish")
        score += 10
    elif ma200 is False:
        drivers.append("MA200: Bearish")
        score -= 10
    else:
        drivers.append("MA200: Insufficient data")

    trend = trend_strength(price_series)
    drivers.append(f"Trend: {trend}")

    score = max(0, min(100, score))

    return {
        "ta_score": score,
        "trend": trend,
        "volatility": "Normal",
        "drivers": drivers
    }
