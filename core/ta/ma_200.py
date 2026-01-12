import pandas as pd

def calculate_ma200(price_series):
    if price_series is None or len(price_series) < 200:
        return {
            "signal": "Neutral",
            "confidence": 0.0,
            "value": None
        }

    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    ma200 = price_series.rolling(window=200).mean().iloc[-1]
    current_price = price_series.iloc[-1]

    if current_price > ma200:
        signal = "Bullish"
        confidence = 0.7
    else:
        signal = "Bearish"
        confidence = 0.7

    return {
        "signal": signal,
        "confidence": confidence,
        "value": round(ma200, 2)
    }
