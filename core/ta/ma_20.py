import pandas as pd

def calculate_ma20(price_df):
    if "close" not in price_df or len(price_df) < 20:
        return {"value": None, "score": 0, "signal": "Unavailable"}

    ma20 = price_df["close"].rolling(20).mean().iloc[-1]
    price = price_df["close"].iloc[-1]

    signal = "Bullish" if price > ma20 else "Bearish"
    score = 1 if signal == "Bullish" else -1

    return {
        "value": round(ma20, 2),
        "score": score,
        "signal": signal
    }
