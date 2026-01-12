import pandas as pd

def calculate_rsi(price_df, period=14):
    close = price_df["close"]

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    latest = rsi.iloc[-1]

    if latest < 30:
        signal = "Bullish"
        score = 1.0
    elif latest > 70:
        signal = "Bearish"
        score = -1.0
    else:
        signal = "Neutral"
        score = 0.0

    return {
        "value": round(float(latest), 2),
        "signal": signal,
        "score": score
    }
