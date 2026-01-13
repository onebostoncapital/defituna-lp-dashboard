def calculate_ma20(price_df):
    close = price_df["close"].astype(float)
    ma20 = close.rolling(20).mean().iloc[-1]
    price = close.iloc[-1]

    if price > ma20:
        return {"score": 0.3, "label": "MA20: Bullish"}
    else:
        return {"score": -0.3, "label": "MA20: Bearish"}
