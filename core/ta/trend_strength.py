def calculate_trend_strength(price_df):
    close = price_df["close"]
    momentum = close.iloc[-1] - close.iloc[-20]

    if momentum > 0:
        return {"signal": "Bullish", "score": 1.0}
    else:
        return {"signal": "Bearish", "score": -1.0}
