def calculate_ma200(price_df):
    close = price_df["close"].astype(float)

    if len(close) < 200:
        return {"score": 0.0, "label": "MA200: Insufficient data"}

    ma200 = close.rolling(200).mean().iloc[-1]
    price = close.iloc[-1]

    if price > ma200:
        return {"score": 0.4, "label": "MA200: Bullish"}
    else:
        return {"score": -0.4, "label": "MA200: Bearish"}
