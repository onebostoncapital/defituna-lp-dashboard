# core/strategy/multi_range_engine.py

def generate_multi_ranges(
    current_price,
    volatility_pct,
    direction,
    capital=10000,
    leverage=2
):
    """
    Generates Defensive / Balanced / Aggressive LP ranges.
    ALL inputs are sanitized to floats here (MASTER RULE).
    """

    # -----------------------------
    # SAFETY CASTING (CRITICAL FIX)
    # -----------------------------
    try:
        current_price = float(current_price)
    except Exception:
        current_price = 0.0

    try:
        volatility_pct = float(volatility_pct)
    except Exception:
        volatility_pct = 0.0

    # -----------------------------
    # CONFIG
    # -----------------------------
    MIN_WIDTH = 3.0        # %
    VOL_MULTIPLIER = 1.5   # volatility sensitivity

    base_width = max(MIN_WIDTH, volatility_pct * VOL_MULTIPLIER)

    width_map = {
        "Defensive": base_width * 1.5,
        "Balanced": base_width,
        "Aggressive": base_width * 0.6
    }

    liquidity_floor = {
        "Defensive": 0.50,
        "Balanced": 0.30,
        "Aggressive": 0.15
    }

    allocation = {
        "Defensive": 0.30,
        "Balanced": 0.40,
        "Aggressive": 0.30
    }

    ranges = {}

    for mode, width_pct in width_map.items():
        half_width = (width_pct / 100) * current_price

        if direction == "Bullish":
            low = current_price - half_width
            high = current_price + (half_width * 1.2)
        elif direction == "Bearish":
            low = current_price - (half_width * 1.2)
            high = current_price + half_width
        else:
            low = current_price - half_width
            high = current_price + half_width

        ranges[mode] = {
            "range_low": round(max(low, 0), 2),
            "range_high": round(high, 2),
            "width_pct": round(width_pct, 2),
            "liquidity_floor": liquidity_floor[mode]
        }

    return {
        "ranges": ranges,
        "allocation": allocation
    }
