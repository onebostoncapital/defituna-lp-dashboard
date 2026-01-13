import pandas as pd


def calculate_rsi(price_df, period=14):
    close = price_df["close"].astype(float)

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss.replace(0, 1e-9)
    rsi = 100 - (100 / (1 + rs))

    value = rsi.iloc[-1]

    if value > 60:
        return {"score": 0.3, "label": "RSI: Bullish"}
    elif value < 40:
        return {"score": -0.3, "label": "RSI: Bearish"}
    else:
        return {"score": 0.0, "label": "RSI: Neutral"}
