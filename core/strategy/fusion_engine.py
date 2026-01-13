# core/strategy/fusion_engine.py

from core.ta.ta_aggregator import aggregate_ta_signals
from core.ai.regime_detection import detect_regime
from core.ai.confidence_calibrator import calibrate_confidence


def fuse_signals(price_df):
    """
    Fuse TA + regime into a single market state.
    """

    # --- Technical Analysis ---
    ta_output = aggregate_ta_signals(price_df)

    ta_score = ta_output.get("ta_score", 0.0)
    volatility_regime = ta_output.get("volatility_regime", "Unavailable")
    trend_strength = ta_output.get("trend_strength", "Unavailable")
    drivers = ta_output.get("drivers", [])

    # --- Direction logic ---
    if ta_score >= 0.7:
        direction = "Bullish"
    elif ta_score <= 0.3:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # --- Regime Detection ---
    regime = detect_regime(
        volatility_regime=volatility_regime,
        trend_strength=trend_strength
    )

    # --- Confidence Calibration ---
    confidence = calibrate_confidence(
        ta_score=ta_score,
        regime=regime
    )

    return {
        "direction": direction,
        "regime": regime,
        "confidence": confidence,
        "ta_score": ta_score,
        "volatility_regime": volatility_regime,
        "trend_strength": trend_strength,
        "drivers": drivers,
    }
