import numpy as np


def calculate_volatility(price_df):
    returns = price_df["close"].pct_change().dropna()

    vol = returns.std()

    if vol < 0.01:
        regime = "Low"
    elif vol < 0.03:
        regime = "Normal"
    else:
        regime = "High"

    return {
        "volatility": float(vol),
        "regime": regime
    }
