def calculate_ma200(price_df):
    if "close" not in price_df or len(price_df) < 200:
        return {"value": None, "score": 0, "signal": "Unavailable"}

    ma200 = price_df["close"].rolling(200).mean().iloc[-1]
    price = price_df["close"].iloc[-1]

    signal = "Bullish" if price > ma200 else "Bearish"
    score = 2 if signal == "Bullish" else -2

    return {
        "value": round(ma200, 2),
        "score": score,
        "signal": signal
    }
