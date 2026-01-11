def generate_multi_ranges(
    current_price: float,
    volatility_pct: float,
    confidence: float,
    direction: str,
):
    """
    Generate Defensive, Balanced, and Aggressive LP ranges
    based on STEP 27 master rule book.
    """

    # -----------------------------
    # 1. Base Range Width
    # -----------------------------
    MIN_WIDTH = 0.10          # 10%
    VOL_MULTIPLIER = 2.0

    base_range = max(
        MIN_WIDTH,
        volatility_pct * VOL_MULTIPLIER
    )

    # -----------------------------
    # 2. Confidence Scaling
    # -----------------------------
    confidence_factor = 1.2 - (confidence * 0.6)

    # -----------------------------
    # 3. Mode Multipliers
    # -----------------------------
    modes = {
        "Defensive": {
            "multiplier": 1.5,
            "liquidity_floor": 0.50
        },
        "Balanced": {
            "multiplier": 1.0,
            "liquidity_floor": 0.30
        },
        "Aggressive": {
            "multiplier": 0.6,
            "liquidity_floor": 0.20
        }
    }

    ranges = {}

    # -----------------------------
    # 4. Build Ranges
    # -----------------------------
    for mode, config in modes.items():
        width = base_range * config["multiplier"] * confidence_factor

        if direction == "Bullish":
            lower = current_price * (1 - width * 0.4)
            upper = current_price * (1 + width * 0.6)

        elif direction == "Bearish":
            lower = current_price * (1 - width * 0.6)
            upper = current_price * (1 + width * 0.4)

        else:  # Neutral
            lower = current_price * (1 - width / 2)
            upper = current_price * (1 + width / 2)

        ranges[mode] = {
            "range_low": round(lower, 2),
            "range_high": round(upper, 2),
            "width_pct": round(width * 100, 2),
            "liquidity_floor": config["liquidity_floor"]
        }

    # -----------------------------
    # 5. Capital Allocation Logic
    # -----------------------------
    if confidence < 0.4:
        allocation = {
            "Defensive": 0.60,
            "Balanced": 0.30,
            "Aggressive": 0.10
        }
    elif confidence < 0.7:
        allocation = {
            "Defensive": 0.50,
            "Balanced": 0.35,
            "Aggressive": 0.15
        }
    else:
        allocation = {
            "Defensive": 0.50,
            "Balanced": 0.30,
            "Aggressive": 0.20
        }

    # Enforce liquidity floors
    for mode in allocation:
        allocation[mode] = max(
            allocation[mode],
            ranges[mode]["liquidity_floor"]
        )

    return {
        "ranges": ranges,
        "allocation": allocation
    }
