def calculate_volatility(price_df):
    close = price_df["close"]
    returns = close.pct_change()
    vol = returns.std() * 100

    return round(float(vol), 2)
