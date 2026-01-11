from core.ta.ta_aggregator import aggregate_ta_signals
from core.fa.fa_aggregator import aggregate_fa_signals


def fuse_signals(price_series):
    """
    Fuse TA + AI + FA into a single master decision.

    Output (dict):
        - final_direction: Bullish / Bearish / Neutral
        - final_score: int (-100 to +100)
        - final_confidence: float (0 to 1)
        - risk_mode: Normal / Defensive / High-Risk
        - active_risk_flags: list
        - explanation: str
    """

    # -----------------------------
    # 1. Collect inputs
    # -----------------------------
    ta = aggregate_ta_signals(price_series)
    fa = aggregate_fa_signals()

    explanation_parts = []

    # -----------------------------
    # 2. Resolve risk mode
    # -----------------------------
    if "HIGH_IMPACT_CALENDAR_EVENT" in fa["risk_flags"] or "GEO_RISK_HIGH" in fa["risk_flags"]:
        risk_mode = "High-Risk"
        explanation_parts.append("High-impact event or geopolitical risk detected.")
    elif fa["fa_bias"] != "Neutral" or ta["confidence"] < 0.4:
        risk_mode = "Defensive"
        explanation_parts.append("Elevated macro or confidence risk detected.")
    else:
        risk_mode = "Normal"
        explanation_parts.append("No elevated external risk detected.")

    # -----------------------------
    # 3. Resolve final direction
    # -----------------------------
    final_direction = ta["direction"]

    if risk_mode == "High-Risk":
        final_direction = "Neutral"
        explanation_parts.append("Direction neutralized due to high-risk environment.")
    elif fa["fa_bias"] == "Bearish" and ta["direction"] == "Bullish":
        final_direction = "Neutral"
        explanation_parts.append("Bullish TA suppressed by bearish FA context.")
    elif fa["fa_bias"] == "Bullish" and ta["direction"] == "Bearish":
        final_direction = "Neutral"
        explanation_parts.append("Bearish TA suppressed by bullish FA context.")

    # -----------------------------
    # 4. Resolve confidence
    # -----------------------------
    final_confidence = ta["confidence"]

    # Apply AI confidence multiplier
    final_confidence *= ta["confidence_multiplier"]

    # Apply FA confidence penalty
    final_confidence *= fa["confidence"]

    final_confidence = max(min(final_confidence, 1.0), 0.0)

    explanation_parts.append(f"Final confidence calibrated to {round(final_confidence, 2)}.")

    # -----------------------------
    # 5. Final score
    # -----------------------------
    final_score = ta["score"] * ta["confidence_multiplier"]
    final_score = max(min(final_score, 100), -100)

    # -----------------------------
    # 6. Output
    # -----------------------------
    return {
        "final_direction": final_direction,
        "final_score": round(final_score, 2),
        "final_confidence": round(final_confidence, 2),
        "risk_mode": risk_mode,
        "active_risk_flags": fa["risk_flags"],
        "ta_drivers": ta["drivers"],
        "explanation": " ".join(explanation_parts)
    }
