# core/strategy/fusion_engine.py

from core.ta.ta_aggregator import aggregate_ta_signals


def fuse_signals(price_df):
    """
    Central fusion engine.
    Combines TA outputs into a unified market state.
    Strategy & range engines depend on this output.
    """

    # =========================
    # 1. TECHNICAL ANALYSIS
    # =========================
    try:
        ta = aggregate_ta_signals(price_df)
    except Exception as e:
        return {
            "direction": "Unavailable",
            "regime": "Unavailable",
            "confidence": 0.0,
            "ta": {},
            "strategy": {},
            "ranges": [],
            "error": f"TA failure: {str(e)}"
        }

    ta_score = ta.get("ta_score", 0.0)
    volatility = ta.get("volatility_regime", "Unavailable")
    trend_strength = ta.get("trend_strength", "Unavailable")
    drivers = ta.get("drivers", [])

    # =========================
    # 2. MARKET DIRECTION
    # =========================
    if ta_score > 0.6:
        direction = "Bullish"
    elif ta_score < -0.6:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # =========================
    # 3. MARKET REGIME
    # =========================
    if volatility == "High" and abs(ta_score) < 0.4:
        regime = "Choppy"
    elif volatility in ["Low", "Normal"] and abs(ta_score) >= 0.4:
        regime = "Trending"
    else:
        regime = "Normal"

    # =========================
    # 4. CONFIDENCE CALIBRATION
    # =========================
    confidence = min(1.0, abs(ta_score))

    # =========================
    # 5. OUTPUT CONTRACT
    # =========================
    return {
        "direction": direction,
        "regime": regime,
        "confidence": round(confidence, 2),
        "ta": {
            "ta_score": round(ta_score, 2),
            "volatility_regime": volatility,
            "trend_strength": trend_strength,
            "drivers": drivers
        },
        "strategy": {
            "mode": "Unavailable",
            "capital_allocation_pct": 0,
            "liquidity_floor_pct": 0
        },
        "ranges": []
    }
