import pandas as pd


def detect_market_regime(price_input) -> str:
    """
    Robust market regime detection.
    Works with Series or DataFrame.
    """

    # -----------------------------
    # Normalize input to Series
    # -----------------------------
    if isinstance(price_input, pd.DataFrame):
        # Try common column names
        for col in ["close", "Close", "price", "Price"]:
            if col in price_input.columns:
                price_series = price_input[col]
                break
        else:
            return "Unknown"
    else:
        price_series = pd.Series(price_input)

    price_series = price_series.astype(float).dropna()

    if len(price_series) < 60:
        return "Unknown"

    # -----------------------------
    # Moving averages
    # -----------------------------
    ma_fast = price_series.rolling(20).mean()
    ma_slow = price_series.rolling(50).mean()

    ma_spread = ma_fast - ma_slow

    spread_latest = float(ma_spread.iloc[-1])
    spread_prev = float(ma_spread.iloc[-5])

    # -----------------------------
    # Volatility analysis
    # -----------------------------
    returns = price_series.pct_change().dropna()

    recent_vol = float(returns.iloc[-20:].std())
    long_vol = float(returns.iloc[-60:].std())

    # -----------------------------
    # Regime rules (simple & robust)
    # -----------------------------
    if abs(spread_latest) > abs(spread_prev) and recent_vol <= long_vol:
        return "Trending"

    if recent_vol > long_vol * 1.5:
        return "High-Risk"

    return "Choppy"
