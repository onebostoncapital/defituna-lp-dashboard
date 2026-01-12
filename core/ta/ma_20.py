def calculate_ma20(price_df):
    close = price_df["close"]
    ma20 = close.rolling(20).mean().iloc[-1]
    latest = close.iloc[-1]

    if latest > ma20:
        return {"signal": "Bullish", "score": 1.0}
    else:
        return {"signal": "Bearish", "score": -1.0}
