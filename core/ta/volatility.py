def calculate_volatility(price_df):
    if "close" not in price_df or len(price_df) < 2:
        return {"value": None, "signal": "Unavailable"}

    returns = price_df["close"].pct_change().dropna()
    vol = returns.std() * 100

    return {
        "value": round(vol, 2),
        "signal": "High" if vol > 3 else "Normal"
    }
