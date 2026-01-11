def calibrate_confidence(
    base_confidence: float,
    regime: str,
    regime_confidence: float,
    volatility_score: float,
    trend_strength_confidence: float
):
    """
    Calibrate final confidence level based on AI context.

    Inputs:
        base_confidence: float (0 to 1) from TA aggregation
        regime: market regime (Trending / Ranging / Transition)
        regime_confidence: confidence of regime detection (0 to 1)
        volatility_score: volatility score (-100 to +100)
        trend_strength_confidence: confidence from trend strength module (0 to 1)

    Output (dict):
        - confidence_multiplier: float (0.5 to 1.2)
        - final_confidence: float (0 to 1)
        - explanation: str
    """

    confidence = base_confidence
    explanation_parts = []

    # Regime-based adjustment
    if regime == "Trending":
        boost = 0.1 * regime_confidence
        confidence += boost
        explanation_parts.append("Trending regime increases confidence.")
    elif regime == "Ranging":
        penalty = 0.2 * regime_confidence
        confidence -= penalty
        explanation_parts.append("Ranging regime reduces confidence.")
    else:
        explanation_parts.append("Transition regime keeps confidence neutral.")

    # Volatility adjustment (high volatility reduces confidence)
    if abs(volatility_score) > 25:
        volatility_penalty = abs(volatility_score) / 200
        confidence -= volatility_penalty
        explanation_parts.append("High volatility suppresses confidence.")

    # Trend strength adjustment
    confidence += 0.1 * trend_strength_confidence
    explanation_parts.append("Trend strength contributes positively to confidence.")

    # Clamp confidence
    confidence = max(min(confidence, 1.0), 0.0)

    # Confidence multiplier for strategy layer
    if confidence > 0.75:
        multiplier = 1.2
    elif confidence > 0.5:
        multiplier = 1.0
    else:
        multiplier = 0.7

    explanation = " ".join(explanation_parts)

    return {
        "confidence_multiplier": multiplier,
        "final_confidence": round(confidence, 2),
        "explanation": explanation
    }
