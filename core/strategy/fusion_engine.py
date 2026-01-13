from core.ta.ta_aggregator import aggregate_ta_signals
from core.fa.fa_aggregator import aggregate_fa_signals

# Optional engines (import safely)
try:
    from core.strategy.multi_range_engine import generate_multi_ranges
except Exception:
    generate_multi_ranges = None


def fuse_signals(price_df):
    """
    MASTER FUSION ENGINE
    - Never crashes
    - Always returns full contract
    """

    # -----------------------------
    # SAFETY: Validate price input
    # -----------------------------
    if price_df is None or price_df.empty or "close" not in price_df.columns:
        return _empty_fusion_output(reason="Invalid or missing price data")

    # -----------------------------
    # TECHNICAL ANALYSIS
    # -----------------------------
    try:
        ta_output = aggregate_ta_signals(price_df)
    except Exception as e:
        return _empty_fusion_output(reason=f"TA failure: {e}")

    # -----------------------------
    # FUNDAMENTAL ANALYSIS
    # -----------------------------
    try:
        fa_output = aggregate_fa_signals()
    except Exception:
        fa_output = {
            "fa_score": 0,
            "drivers": []
        }

    # -----------------------------
    # DIRECTION LOGIC
    # -----------------------------
    ta_score = ta_output.get("ta_score", 0)

    if ta_score > 1:
        direction = "Bullish"
    elif ta_score < -1:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # -----------------------------
    # CONFIDENCE (simple & safe)
    # -----------------------------
    confidence = min(abs(ta_score) / 5, 1.0)

    # -----------------------------
    # CURRENT PRICE
    # -----------------------------
    try:
        current_price = float(price_df["close"].iloc[-1])
    except Exception:
        current_price = 0.0

    # -----------------------------
    # MULTI-RANGE ENGINE (SAFE)
    # -----------------------------
    ranges = {}
    if generate_multi_ranges:
        try:
            ranges = generate_multi_ranges(
                current_price=current_price,
                volatility_pct=ta_output.get("volatility_pct", 0.0),
                direction=direction
            )
        except Exception:
            ranges = {}

    # -----------------------------
    # ACTIVE MODE SELECTION
    # -----------------------------
    active_mode = "Balanced"
    active_reason = "Default balanced allocation"

    if confidence > 0.7:
        active_mode = "Aggressive"
        active_reason = "High confidence signal"
    elif confidence < 0.3:
        active_mode = "Defensive"
        active_reason = "Low confidence signal"

    # -----------------------------
    # FINAL CONTRACT (ALL KEYS)
    # -----------------------------
    return {
        # Core state
        "direction": direction,
        "regime": "Normal",
        "confidence": round(confidence, 2),

        # Strategy selection
        "active_mode": active_mode,
        "active_reason": active_reason,
        "capital_pct": 100,
        "liquidity_floor_pct": 20,

        # Ranges
        "ranges": ranges,

        # Technical outputs
        "ta_score": ta_score,
        "ta_drivers": ta_output.get("drivers", []),
        "volatility_regime": "Normal",
        "trend_strength": "Neutral",

        # Fundamental outputs
        "fa_drivers": fa_output.get("drivers", []),
    }


# ======================================================
# SAFE FALLBACK (NEVER CRASHES DASHBOARD)
# ======================================================

def _empty_fusion_output(reason="Unknown"):
    return {
        "direction": "Neutral",
        "regime": "Unavailable",
        "confidence": 0.0,

        "active_mode": "Defensive",
        "active_reason": reason,
        "capital_pct": 0,
        "liquidity_floor_pct": 0,

        "ranges": {},

        "ta_score": 0,
        "ta_drivers": [],
        "volatility_regime": "Unavailable",
        "trend_strength": "Unavailable",

        "fa_drivers": [],
    }
