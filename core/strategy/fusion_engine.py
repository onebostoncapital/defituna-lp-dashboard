from core.ta.ta_aggregator import aggregate_ta_signals
from core.fa.fa_aggregator import aggregate_fa_signals
from core.ai.regime_detector import detect_market_regime
from core.ai.confidence_calibrator import calibrate_confidence
from core.strategy.multi_range_engine import generate_multi_ranges


def fuse_signals(price_series):
    # -----------------------------
    # TECHNICAL ANALYSIS
    # -----------------------------
    ta_output = aggregate_ta_signals(price_series)

    # -----------------------------
    # FUNDAMENTAL ANALYSIS
    # -----------------------------
    fa_output = aggregate_fa_signals()

    # -----------------------------
    # REGIME DETECTION
    # -----------------------------
    regime = detect_market_regime(price_series)

    # -----------------------------
    # CONFIDENCE CALIBRATION
    # -----------------------------
    confidence = calibrate_confidence(
        ta_output["ta_score"],
        fa_output["fa_score"],
        regime
    )

    # -----------------------------
    # DIRECTION LOGIC
    # -----------------------------
    if confidence >= 0.7 and ta_output["trend"] == "Bullish":
        direction = "Bullish"
    elif confidence >= 0.7 and ta_output["trend"] == "Bearish":
        direction = "Bearish"
    else:
        direction = "Neutral"

    # -----------------------------
    # MULTI-RANGE ENGINE
    # -----------------------------
    multi_ranges = generate_multi_ranges(
        current_price=float(price_series.iloc[-1]),
        volatility_pct=ta_output["volatility_pct"],
        direction=direction
    )

    # -----------------------------
    # ACTIVE MODE SELECTION
    # -----------------------------
    if confidence >= 0.75:
        active_mode = "Aggressive"
        active_reason = "High confidence with strong directional signals."
    elif confidence >= 0.55:
        active_mode = "Balanced"
        active_reason = "Moderate confidence with mixed but stable signals."
    else:
        active_mode = "Defensive"
        active_reason = "Low confidence or uncertain market regime."

    active_range = multi_ranges["ranges"][active_mode]

    return {
        # CORE
        "final_direction": direction,
        "final_confidence": round(confidence, 2),
        "risk_mode": regime,

        # TA
        "ta_score": ta_output["ta_score"],
        "volatility_regime": ta_output["volatility_pct"],
        "trend_strength": ta_output["trend"],
        "ta_drivers": ta_output["drivers"],

        # FA
        "fa_score": fa_output["fa_score"],
        "fa_drivers": fa_output["drivers"],

        # STRATEGY
        "multi_ranges": multi_ranges,
        "active_mode": active_mode,
        "active_range": active_range,
        "active_allocation": multi_ranges["allocation"][active_mode],
        "active_reason": active_reason
    }
