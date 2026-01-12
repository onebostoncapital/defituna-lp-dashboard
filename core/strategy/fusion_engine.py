"""
Fusion Engine
-------------
Combines:
- Technical Analysis (TA)
- Fundamental Analysis (FA)
- AI Regime + Confidence
- Multi-Range Strategy
- Scenario Projections (NEW)

This file is the SINGLE SOURCE OF TRUTH
for strategy-level outputs.
"""

from core.ta.ta_aggregator import aggregate_ta_signals
from core.fa.fa_aggregator import aggregate_fa_signals
from core.ai.regime_detector import detect_market_regime
from core.ai.confidence_calibrator import calibrate_confidence
from core.strategy.multi_range_engine import generate_multi_ranges
from core.strategy.scenario_engine import compute_scenarios


def fuse_signals(price_series):
    """
    Master fusion function.
    Returns a complete, stable strategy dictionary.
    """

    # -----------------------------
    # TECHNICAL ANALYSIS
    # -----------------------------
    ta_output = aggregate_ta_signals(price_series)

    # -----------------------------
    # FUNDAMENTAL ANALYSIS
    # -----------------------------
    fa_output = aggregate_fa_signals()

    # -----------------------------
    # MARKET REGIME
    # -----------------------------
    regime = detect_market_regime(price_series)

    # -----------------------------
    # CONFIDENCE CALIBRATION
    # -----------------------------
    confidence = calibrate_confidence(
        ta_output.get("ta_score", 0.0),
        fa_output.get("fa_score", 0.0),
        regime
    )

    # -----------------------------
    # DIRECTION DECISION
    # -----------------------------
    if confidence > 0.6:
        direction = "Bullish"
    elif confidence < -0.6:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # -----------------------------
    # MULTI-RANGE ENGINE
    # -----------------------------
    multi_ranges = generate_multi_ranges(
        current_price=float(price_series.iloc[-1]),
        volatility_pct=ta_output.get("volatility_pct", 0.0),
        direction=direction
    )

    active_mode = multi_ranges.get("active_mode", "Balanced")
    active_range = multi_ranges.get("ranges", {}).get(active_mode, {})
    active_allocation = multi_ranges.get("allocation", {}).get(active_mode, 0.0)

    # -----------------------------
    # SCENARIO PROJECTIONS (NEW)
    # -----------------------------
    scenario_projections = compute_scenarios(
        current_price=float(price_series.iloc[-1]),
        ranges=multi_ranges.get("ranges", {}),
        capital_usd=10_000.0,
        leverage=2.0,
        horizon_days=7
    )

    # -----------------------------
    # FINAL FUSION OUTPUT
    # -----------------------------
    return {
        # Core market state
        "final_direction": direction,
        "risk_mode": regime,
        "final_confidence": round(confidence, 2),

        # TA
        "ta_score": ta_output.get("ta_score", 0.0),
        "ta_drivers": ta_output.get("drivers", []),
        "volatility_pct": ta_output.get("volatility_pct", 0.0),

        # FA
        "fa_score": fa_output.get("fa_score", 0.0),
        "fa_drivers": fa_output.get("fa_drivers", []),

        # Strategy
        "multi_ranges": multi_ranges,
        "active_mode": active_mode,
        "active_range": active_range,
        "active_allocation": active_allocation,
        "strategy_explanation": multi_ranges.get(
            "explanation",
            "Strategy selected based on confidence, volatility, and regime."
        ),

        # Scenario Intelligence (NEW)
        "scenario_projections": scenario_projections
    }
