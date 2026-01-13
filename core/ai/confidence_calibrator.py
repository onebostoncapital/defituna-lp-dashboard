# core/ai/confidence_calibration.py

def calibrate_confidence(
    ta_score: float,
    regime: str,
    fa_score: float | None = None
) -> float:
    """
    Calibrates confidence score using TA + optional FA + regime.

    - ta_score: 0 → 1
    - fa_score: 0 → 1 (optional)
    - regime: market regime string
    """

    # Normalize inputs
    ta_score = max(0.0, min(1.0, ta_score))

    if fa_score is None:
        fa_score = 0.5  # Neutral FA fallback

    fa_score = max(0.0, min(1.0, fa_score))

    # Base confidence blend
    confidence = (ta_score * 0.7) + (fa_score * 0.3)

    # Regime adjustment
    if regime in ["High Volatility", "Uncertain"]:
        confidence *= 0.8
    elif regime in ["Trending", "Normal"]:
        confidence *= 1.05

    # Final clamp
    return round(max(0.0, min(1.0, confidence)), 2)
