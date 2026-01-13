def calculate_rsi(price_df, period=14):
    if "close" not in price_df or len(price_df) < period + 1:
        return {"value": None, "score": 0, "signal": "Unavailable"}

    delta = price_df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean().iloc[-1]
    avg_loss = loss.rolling(period).mean().iloc[-1]

    if avg_loss == 0:
        return {"value": 100, "score": -1, "signal": "Overbought"}

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    if rsi < 30:
        signal, score = "Oversold", 1
    elif rsi > 70:
        signal, score = "Overbought", -1
    else:
        signal, score = "Neutral", 0

    return {
        "value": round(rsi, 2),
        "score": score,
        "signal": signal
    }
