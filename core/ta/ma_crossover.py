def calculate_ma_crossover(price_df):
    close = price_df["close"]
    ma20 = close.rolling(20).mean()
    ma200 = close.rolling(200).mean()

    if ma20.iloc[-1] > ma200.iloc[-1]:
        return {"signal": "Bullish", "score": 1.0}
    else:
        return {"signal": "Bearish", "score": -1.0}
