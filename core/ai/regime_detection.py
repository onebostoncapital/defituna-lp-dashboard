import pandas as pd


def detect_market_regime(price_series: pd.Series):
    """
    Detect market regime: Trending, Ranging, or Transition.

    Input:
        price_series: pandas Series of closing prices (latest last)

    Output (dict):
        - regime: Trending / Ranging / Transition
        - score: int (-30 to +30)
        - confidence: float (0 to 1)
        - explanation: str
    """

    # Safety check
    if price_series is None or len(price_series) < 200:
        return {
            "regime": "Transition",
            "score": 0,
            "confidence": 0.0,
            "explanation": "Insufficient data to determine market regime."
        }

    # Moving averages
    ma20 = price_series.rolling(window=20).mean()
    ma200 = price_series.rolling(window=200).mean()

    ma_spread = (ma20 - ma200) / ma200 * 100
    spread_latest = ma_spread.iloc[-1]

    # Price slope (trend persistence)
    slope = price_series.diff().rolling(window=20).mean().iloc[-1]

    # Volatility
    returns = price_series.pct_change().dropna()
    recent_vol = returns.rolling(window=20).std().iloc[-1] * 100
    long_vol = returns.rolling(window=60).std().iloc[-1] * 100

    # Regime logic
    if abs(spread_latest) > 1.0 and abs(slope) > 0 and recent_vol >= long_vol:
        regime = "Trending"
        score = 30
        confidence = min(abs(spread_latest) / 3, 1.0)
    elif abs(spread_latest) < 0.5 and recent_vol < long_vol:
        regime = "Ranging"
        score = -20
        confidence = min((long_vol - recent_vol) / long_vol, 1.0)
    else:
        regime = "Transition"
        score = 0
        confidence = 0.5

    # Explanation
    explanation = (
        f"MA spread is {spread_latest:.2f}%, "
        f"recent volatility is {recent_vol:.2f}%, "
        f"indicating a {regime.lower()} market regime."
    )

    return {
        "regime": regime,
        "score": score,
        "confidence": round(confidence, 2),
        "explanation": explanation
    }
