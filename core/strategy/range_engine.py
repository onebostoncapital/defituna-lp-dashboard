def generate_range_and_liquidation(
    current_price: float,
    fusion_output: dict,
    capital_usd: float = 10000.0,
    leverage: float = 2.0
):
    """
    Generate LP range, directional skew, and liquidation risk level
    based on fused intelligence output.

    Inputs:
        - current_price: float (SOL price)
        - fusion_output: dict from fusion_engine
        - capital_usd: default 10,000
        - leverage: default 2x

    Output:
        dict with range, liquidation, and explanation
    """

    direction = fusion_output["final_direction"]
    confidence = fusion_output["final_confidence"]
    risk_mode = fusion_output["risk_mode"]

    explanation_parts = []

    # --------------------------------------------------
    # 1. Base range width by risk mode
    # --------------------------------------------------
    if risk_mode == "Normal":
        base_width = 0.08
        explanation_parts.append("Normal risk mode: base width 8%.")
    elif risk_mode == "Defensive":
        base_width = 0.12
        explanation_parts.append("Defensive risk mode: base width 12%.")
    else:  # High-Risk
        base_width = 0.18
        explanation_parts.append("High-risk mode: base width 18%.")

    # Adjust width by confidence
    effective_width = base_width * (1 + (1 - confidence))
    explanation_parts.append(
        f"Width adjusted by confidence ({round(confidence,2)}): {round(effective_width*100,2)}%."
    )

    # --------------------------------------------------
    # 2. Directional skew
    # --------------------------------------------------
    if direction == "Bullish":
        lower = current_price * (1 - effective_width * 0.6)
        upper = current_price * (1 + effective_width * 1.4)
        explanation_parts.append("Bullish skew applied (upside weighted).")
    elif direction == "Bearish":
        lower = current_price * (1 - effective_width * 1.4)
        upper = current_price * (1 + effective_width * 0.6)
        explanation_parts.append("Bearish skew applied (downside weighted).")
    else:
        lower = current_price * (1 - effective_width)
        upper = current_price * (1 + effective_width)
        explanation_parts.append("Neutral symmetric range applied.")

    # --------------------------------------------------
    # 3. Liquidation risk level (alert, not execution)
    # --------------------------------------------------
    safety_factor = 0.85

    if direction == "Bullish":
        liquidation_level = current_price * (1 - (1 / leverage) * safety_factor)
        explanation_parts.append("Downside liquidation risk calculated (bullish LP).")
    elif direction == "Bearish":
        liquidation_level = current_price * (1 + (1 / leverage) * safety_factor)
        explanation_parts.append("Upside liquidation risk calculated (bearish LP).")
    else:
        liquidation_level = None
        explanation_parts.append("No directional liquidation level (neutral LP).")

    # --------------------------------------------------
    # 4. Position mode classification
    # --------------------------------------------------
    if confidence > 0.7 and risk_mode == "Normal":
        position_mode = "Aggressive"
    elif confidence >= 0.4:
        position_mode = "Balanced"
    else:
        position_mode = "Defensive"

    explanation_parts.append(f"Position mode set to {position_mode}.")

    # --------------------------------------------------
    # 5. Output
    # --------------------------------------------------
    return {
        "range_low": round(lower, 2),
        "range_high": round(upper, 2),
        "range_width_pct": round(effective_width * 100, 2),
        "directional_bias": direction,
        "liquidation_level": round(liquidation_level, 2) if liquidation_level else None,
        "position_mode": position_mode,
        "explanation": " ".join(explanation_parts)
    }
