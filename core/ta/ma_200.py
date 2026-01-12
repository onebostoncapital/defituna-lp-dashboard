def calculate_ma200(price_df):
    close = price_df["close"]
    ma200 = close.rolling(200).mean().iloc[-1]
    latest = close.iloc[-1]

    if latest > ma200:
        return {"signal": "Bullish", "score": 1.0}
    else:
        return {"signal": "Bearish", "score": -1.0}
