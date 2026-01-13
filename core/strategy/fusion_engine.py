# core/strategy/fusion_engine.py

from core.ta.ta_aggregator import aggregate_ta_signals
from core.ai.regime_detector import detect_market_regime
from core.ai.confidence_calibrator import calibrate_confidence
from core.strategy.range_engine import generate_range
from core.strategy.multi_range_engine import generate_multi_ranges


def _select_active_strategy(confidence, regime, ta_trend):
    """
    Decide LP strategy based on master rule book.
    """

    if confidence < 0.35 or regime == "Choppy":
        return {
            "mode": "Defensive",
            "capital_pct": 50,
            "liquidity_floor_pct": 50,
            "reason": "Low confidence or choppy regime → capital preservation"
        }

    if 0.35 <= confidence <= 0.65:
        return {
            "mode": "Balanced",
            "capital_pct": 30,
            "liquidity_floor_pct": 30,
            "reason": "Moderate confidence → balanced risk allocation"
        }

    if confidence > 0.65 and ta_trend == "Bullish":
        return {
            "mode": "Aggressive",
            "capital_pct": 20,
            "liquidity_floor_pct": 20,
            "reason": "High confidence + bullish trend → aggressive positioning"
        }

    # Fallback (safety)
    return {
        "mode": "Balanced",
        "capital_pct": 30,
        "liquidity_floor_pct": 30,
        "reason": "Fallback balanced allocation"
    }


def fuse_signals(price_df):
    """
    Master fusion engine: TA + Regime + Confidence → Strategy + Ranges
    """

    # --- Technical Analysis ---
    ta_output = aggregate_ta_signals(price_df)
    ta_score = ta_output.get("ta_score", 0)
    ta_trend = ta_output.get("trend_strength", "Neutral")

    # --- Market Regime ---
    regime = detect_market_regime(price_df)

    # --- Confidence ---
    confidence = calibrate_confidence(
        ta_score=ta_score,
        regime=regime
    )

    # --- Direction ---
    direction = "Bullish" if ta_score > 0 else "Bearish" if ta_score < 0 else "Neutral"

    # --- Strategy Selection ---
    strategy = _select_active_strategy(confidence, regime, ta_trend)

    # --- Single Active Range ---
    active_range = generate_range(
        price=float(price_df["close"].iloc[-1]),
        volatility_pct=ta_output.get("volatility_pct", 0),
        direction=direction
    )

    # --- Multi-Range (for comparison table) ---
    multi_ranges = generate_multi_ranges(
        current_price=float(price_df["close"].iloc[-1]),
        volatility_pct=ta_output.get("volatility_pct", 0),
        direction=direction
    )

    return {
        # Market
        "direction": direction,
        "regime": regime,
        "confidence": round(confidence, 2),

        # Strategy
        "active_strategy": strategy["mode"],
        "capital_allocation_pct": strategy["capital_pct"],
        "liquidity_floor_pct": strategy["liquidity_floor_pct"],
        "active_reason": strategy["reason"],

        # Ranges
        "active_range": active_range,
        "multi_ranges": multi_ranges,

        # TA
        "ta_score": ta_score,
        "ta_drivers": ta_output.get("drivers", []),
        "volatility_regime": ta_output.get("volatility_regime", "Normal"),
        "trend_strength": ta_trend,
    }
