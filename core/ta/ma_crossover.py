import pandas as pd

def calculate_ma_crossover(price_series):
    if price_series is None or len(price_series) < 200:
        return {
            "signal": "Neutral",
            "confidence": 0.0
        }

    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    ma20 = price_series.rolling(20).mean().iloc[-1]
    ma200 = price_series.rolling(200).mean().iloc[-1]

    if ma20 > ma200:
        return {"signal": "Bullish", "confidence": 0.7}
    else:
        return {"signal": "Bearish", "confidence": 0.7}
