from core.ta.ta_aggregator import aggregate_ta_signals
from core.fa.fa_aggregator import aggregate_fa_signals
from core.ai.regime_detector import detect_market_regime
from core.ai.confidence_calibrator import calibrate_confidence

from core.strategy.multi_range_engine import generate_multi_ranges


def select_active_mode(confidence: float) -> str:
    """
    Auto-select LP mode based on confidence.
    """
    if confidence < 0.4:
        return "Defensive"
    elif confidence < 0.7:
        return "Balanced"
    else:
        return "Aggressive"


def fuse_signals(price_series):
    """
    Fuse TA, FA, AI and activate multi-range strategy.
    """

    # -----------------------------
    # Technical Analysis
    # -----------------------------
    ta_output = aggregate_ta_signals(price_series)

    # -----------------------------
    # Fundamental Analysis
    # -----------------------------
    fa_output = aggregate_fa_signals()

    # -----------------------------
    # AI Enhancements
    # -----------------------------
    regime = detect_market_regime(price_series)
    confidence = calibrate_confidence(
        ta_output["ta_score"],
        fa_output["fa_score"],
        regime
    )

    # -----------------------------
    # Direction Logic
    # -----------------------------
    if ta_output["ta_score"] > 0.5 and fa_output["fa_score"] > 0:
        direction = "Bullish"
    elif ta_output["ta_score"] < -0.5 and fa_output["fa_score"] < 0:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # -----------------------------
    # Volatility (annualized %)
    # -----------------------------
    returns = price_series.pct_change().dropna()
    volatility_pct = returns.std() * (252 ** 0.5)

    # -----------------------------
    # Multi-Range Engine
    # -----------------------------
    multi_range_output = generate_multi_ranges(
        current_price=price_series.iloc[-1],
        volatility_pct=volatility_pct,
        confidence=confidence,
        direction=direction
    )

    # -----------------------------
    # Active Mode Selection
    # -----------------------------
    active_mode = select_active_mode(confidence)

    active_range = multi_range_output["ranges"][active_mode]
    active_allocation = multi_range_output["allocation"][active_mode]

    # -----------------------------
    # Final Output
    # -----------------------------
    return {
        "final_direction": direction,
        "risk_mode": regime,
        "final_confidence": round(confidence, 2),

        "ta_score": ta_output["ta_score"],
        "fa_score": fa_output["fa_score"],
        "ta_drivers": ta_output["drivers"],

        "multi_ranges": multi_range_output,

        # 🔑 ACTIVE STRATEGY
        "active_mode": active_mode,
        "active_range": active_range,
        "active_allocation": active_allocation
    }
