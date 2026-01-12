import pandas as pd

def calculate_ma20(price_series):
    """
    price_series: pandas Series of prices
    """
    if price_series is None or len(price_series) < 20:
        return {
            "signal": "Neutral",
            "confidence": 0.0,
            "value": None
        }

    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    ma20 = price_series.rolling(window=20).mean().iloc[-1]
    current_price = price_series.iloc[-1]

    if current_price > ma20:
        signal = "Bullish"
        confidence = 0.6
    else:
        signal = "Bearish"
        confidence = 0.6

    return {
        "signal": signal,
        "confidence": confidence,
        "value": round(ma20, 2)
    }
