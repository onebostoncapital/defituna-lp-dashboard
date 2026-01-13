def calculate_trend_strength(price_df):
    close = price_df["close"].astype(float)

    if len(close) < 20:
        return {"score": 0.0, "label": "Trend: Unavailable"}

    momentum = close.iloc[-1] - close.iloc[-20]

    if momentum > 0:
        return {"score": 0.3, "label": "Trend: Bullish"}
    else:
        return {"score": -0.3, "label": "Trend: Bearish"}
