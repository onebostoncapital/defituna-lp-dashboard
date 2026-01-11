from typing import Dict


# -----------------------------
# CONFIG
# -----------------------------
MIN_WIDTH = 8.0          # %
VOL_MULTIPLIER = 2.5


# -----------------------------
# ENGINE
# -----------------------------
def generate_multi_ranges(
    current_price: float,
    volatility_pct: float,
    confidence: float,
    direction: str
) -> Dict:
    """
    Generate defensive, balanced, and aggressive LP ranges.
    All inputs MUST be scalars.
    """

    # --- HARD SAFETY CASTS ---
    try:
        current_price = float(current_price)
        volatility_pct = float(volatility_pct)
        confidence = float(confidence)
    except Exception:
        volatility_pct = MIN_WIDTH

    # --- BASE WIDTH LOGIC ---
    base_width = max(
        MIN_WIDTH,
        volatility_pct * VOL_MULTIPLIER
    )

    # --- MODE DEFINITIONS ---
    modes = {
        "Defensive": {
            "width_multiplier": 1.6,
            "liquidity_floor": 0.5
        },
        "Balanced": {
            "width_multiplier": 1.0,
            "liquidity_floor": 0.3
        },
        "Aggressive": {
            "width_multiplier": 0.6,
            "liquidity_floor": 0.2
        }
    }

    ranges = {}
    allocation = {}

    for mode, params in modes.items():
        width_pct = base_width * params["width_multiplier"]
        half_range = (width_pct / 100) * current_price / 2

        ranges[mode] = {
            "range_low": round(current_price - half_range, 2),
            "range_high": round(current_price + half_range, 2),
            "width_pct": round(width_pct, 2),
            "liquidity_floor": params["liquidity_floor"]
        }

        allocation[mode] = params["liquidity_floor"]

    # --- ACTIVE MODE SELECTION ---
    if confidence >= 0.7:
        active_mode = "Aggressive"
    elif confidence >= 0.4:
        active_mode = "Balanced"
    else:
        active_mode = "Defensive"

    return {
        "ranges": ranges,
        "allocation": allocation,
        "active_mode": active_mode
    }
