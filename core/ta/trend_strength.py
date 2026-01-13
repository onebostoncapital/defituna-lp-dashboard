def calculate_trend_strength(price_df):
    if "close" not in price_df or len(price_df) < 20:
        return {"value": None, "score": 0, "signal": "Unavailable"}

    momentum = price_df["close"].iloc[-1] - price_df["close"].iloc[-20]

    if momentum > 0:
        return {"value": round(momentum, 2), "score": 1, "signal": "Bullish"}
    elif momentum < 0:
        return {"value": round(momentum, 2), "score": -1, "signal": "Bearish"}
    else:
        return {"value": 0, "score": 0, "signal": "Neutral"}
