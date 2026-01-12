from core.ta.ta_aggregator import aggregate_ta_signals
from core.fa.fa_aggregator import aggregate_fa_signals
from core.ai.regime_detector import detect_market_regime
from core.ai.confidence_calibrator import calibrate_confidence
from core.strategy.multi_range_engine import generate_multi_ranges


def fuse_signals(price_series):
    """
    Central brain:
    Combines TA + FA + AI into one decision.
    """

    # ============================
    # 1. TECHNICAL ANALYSIS
    # ============================
    ta_output = aggregate_ta_signals(price_series)

    ta_score = ta_output.get("ta_score", 0.0)
    ta_drivers = ta_output.get("drivers", [])

    # ============================
    # 2. FUNDAMENTAL ANALYSIS
    # ============================
    fa_output = aggregate_fa_signals()

    fa_score = fa_output.get("fa_score", 0.0)
    fa_drivers = fa_output.get("drivers", [])
    fa_news = fa_output.get("news", [])

    # ============================
    # 3. MARKET REGIME (AI)
    # ============================
    regime = detect_market_regime(price_series)

    # ============================
    # 4. CONFIDENCE ENGINE
    # ============================
    confidence = calibrate_confidence(
        ta_score=ta_score,
        fa_score=fa_score,
        regime=regime
    )

    # ============================
    # 5. DIRECTION LOGIC
    # ============================
    if ta_score > 0.25:
        direction = "Bullish"
    elif ta_score < -0.25:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # ============================
    # 6. MULTI-RANGE ENGINE
    # ============================
    volatility_proxy = abs(ta_score) * 10

    multi_range_output = generate_multi_ranges(
        current_price=float(price_series.iloc[-1]),
        volatility_pct=volatility_proxy,
        confidence=confidence,
        direction=direction
    )

    active_mode = multi_range_output["active_mode"]
    active_range = multi_range_output["ranges"][active_mode]
    active_allocation = multi_range_output["allocation"][active_mode]

    # ============================
    # 7. FINAL OUTPUT (EXPOSE ALL)
    # ============================
    return {
        "final_direction": direction,
        "risk_mode": regime,
        "final_confidence": round(confidence, 2),

        "ta_score": round(ta_score, 2),
        "ta_drivers": ta_drivers,

        "fa_score": round(fa_score, 2),
        "fa_drivers": fa_drivers,
        "fa_news": fa_news,

        "multi_ranges": multi_range_output,
        "active_mode": active_mode,
        "active_range": active_range,
        "active_allocation": active_allocation
    }
