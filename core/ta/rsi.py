import pandas as pd
import numpy as np


def calculate_rsi(price_series, period=14):
    """
    RSI calculated from a Pandas Series (MASTER RULE).
    """

    price_series = pd.to_numeric(price_series, errors="coerce").dropna()

    if len(price_series) < period + 1:
        return {"signal": "Neutral", "confidence": 0.0}

    delta = price_series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    current_rsi = float(rsi.iloc[-1])

    if current_rsi < 30:
        return {"signal": "Bullish", "confidence": 1.0}
    elif current_rsi > 70:
        return {"signal": "Bearish", "confidence": 1.0}
    else:
        return {"signal": "Neutral", "confidence": 0.5}
