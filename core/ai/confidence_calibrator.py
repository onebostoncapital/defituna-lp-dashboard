def calibrate_confidence(ta_score: float, fa_score: float, regime: str) -> float:
    """
    Calibrate final confidence score based on TA, FA, and market regime.
    Returns a value between 0.0 and 1.0
    """

    # Base confidence from signal strength
    base_confidence = abs(ta_score) * 0.6 + abs(fa_score) * 0.4

    # Regime adjustment
    if regime == "Trending":
        regime_multiplier = 1.1
    elif regime == "Ranging":
        regime_multiplier = 0.9
    else:  # Uncertain / High risk
        regime_multiplier = 0.75

    confidence = base_confidence * regime_multiplier

    # Clamp between 0 and 1
    confidence = max(0.0, min(round(confidence, 2), 1.0))

    return confidence
