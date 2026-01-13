# core/market_state/market_state_engine.py

def derive_market_state(ta_output: dict) -> dict:
    """
    Phase 2 Market State Engine
    ---------------------------
    INPUT (read-only):
        ta_output = {
            "ta_score": int,
            "trend": "Bullish" | "Bearish" | "Neutral",
            "volatility": "Low" | "Normal" | "High",
            "drivers": list[str]
        }

    OUTPUT:
        {
            "direction": str,
            "regime": str,
            "confidence": float
        }
    """

    ta_score = ta_output.get("ta_score", 0)
    trend = ta_output.get("trend", "Neutral")
    volatility = ta_output.get("volatility", "Normal")

    # -----------------------
    # Direction Logic
    # -----------------------
    if ta_score >= 60 and trend == "Bullish":
        direction = "Bullish"
    elif ta_score <= -60 and trend == "Bearish":
        direction = "Bearish"
    else:
        direction = "Neutral"

    # -----------------------
    # Regime Logic
    # -----------------------
    if volatility == "High":
        regime = "Volatile"
    elif trend in ["Bullish", "Bearish"] and volatility in ["Low", "Normal"]:
        regime = "Trending"
    else:
        regime = "Ranging"

    # -----------------------
    # Confidence Logic
    # -----------------------
    confidence = min(abs(ta_score) / 100.0, 1.0)

    return {
        "direction": direction,
        "regime": regime,
        "confidence": round(confidence, 2)
    }
