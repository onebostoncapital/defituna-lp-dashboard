from core.ta.ta_aggregator import aggregate_ta_signals
from core.fa.fa_aggregator import aggregate_fa_signals
from core.ai.regime_detector import detect_market_regime
from core.ai.confidence_calibrator import calibrate_confidence
from core.strategy.multi_range_engine import generate_multi_ranges


def fuse_signals(price_series):
    """
    Master fusion engine:
    - TA
    - FA
    - AI regime
    - Confidence
    - Range selection
    """

    # -----------------------------
    # TECHNICAL ANALYSIS
    # -----------------------------
    ta_output = aggregate_ta_signals(price_series)

    # -----------------------------
    # FUNDAMENTAL ANALYSIS
    # -----------------------------
    fa_output = aggregate_fa_signals()

    # SAFE DEFAULTS (VERY IMPORTANT)
    fa_score = fa_output.get("fa_score", 0.0)
    fa_drivers = fa_output.get("drivers", [])
    fa_news = fa_output.get("news", [])

    # -----------------------------
    # MARKET REGIME (AI)
    # -----------------------------
    regime = detect_market_regime(price_series)

    # -----------------------------
    # CONFIDENCE CALIBRATION
    # -----------------------------
    confidence = calibrate_confidence(
        ta_output["ta_score"],
        fa_score,
        regime
    )

    # -----------------------------
    # FINAL DIRECTION
    # -----------------------------
    if confidence > 0.6:
        direction = "Bullish"
    elif confidence < 0.4:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # -----------------------------
    # MULTI-RANGE ENGINE
    # -----------------------------
    multi_range_output = generate_multi_ranges(
        current_price=price_series.iloc[-1],
        volatility_pct=ta_output["volatility_pct"],
        confidence=confidence,
        direction=direction
    )

    # -----------------------------
    # FINAL PAYLOAD (VERY IMPORTANT)
    # -----------------------------
    return {
        "final_direction": direction,
        "risk_mode": regime,
        "final_confidence": round(confidence, 2),

        # TA
        "ta_score": ta_output["ta_score"],
        "ta_drivers": ta_output["drivers"],

        # FA
        "fa_score": round(fa_score, 2),
        "fa_drivers": fa_drivers,
        "fa_news": fa_news,

        # RANGE OUTPUT
        "multi_ranges": multi_range_output,
        "active_mode": multi_range_output["active_mode"],
        "active_range": multi_range_output["ranges"][multi_range_output["active_mode"]],
        "active_allocation": multi_range_output["allocation"][multi_range_output["active_mode"]],
    }
