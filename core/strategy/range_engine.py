# core/strategy/range_engine.py

def generate_range(price, volatility_pct, direction):
    """
    Generate a single active liquidity range.
    This is intentionally simple and SAFE.
    """

    if price is None or volatility_pct is None:
        return None

    # Fallback volatility
    if volatility_pct <= 0:
        volatility_pct = 2.0

    width = price * (volatility_pct / 100)

    if direction == "Bullish":
        lower = price - width * 0.6
        upper = price + width * 1.4
    elif direction == "Bearish":
        lower = price - width * 1.4
        upper = price + width * 0.6
    else:
        lower = price - width
        upper = price + width

    return {
        "lower": round(lower, 2),
        "upper": round(upper, 2),
        "width_pct": round((upper - lower) / price * 100, 2)
    }
