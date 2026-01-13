from core.ta.ta_aggregator import aggregate_ta_signals
from core.strategy.range_engine import generate_ranges
from core.strategy.multi_range_engine import generate_multi_ranges
from core.ai.regime_detection import detect_market_regime
from core.ai.confidence_calibration import calibrate_confidence
from core.fa.fa_aggregator import aggregate_fa_signals

def fuse_signals(price_df):
    """
    price_df MUST be a pandas DataFrame with a 'close' column
    """

    # --- SAFETY CHECK (prevents future silent bugs)
    if not hasattr(price_df, "columns") or "close" not in price_df.columns:
        raise ValueError("fuse_signals expects a DataFrame with a 'close' column")

    # --- Technical Analysis
    ta_output = aggregate_ta_signals(price_df)

    # --- Fundamental Analysis
    fa_output = aggregate_fa_signals()

    # --- Market Regime
    regime = detect_market_regime(
        ta_score=ta_output["ta_score"],
        volatility_pct=ta_output["volatility_pct"]
    )

    # --- Confidence
    confidence = calibrate_confidence(
        ta_score=ta_output["ta_score"],
        volatility_pct=ta_output["volatility_pct"],
        regime=regime
    )

    # --- Direction
    if ta_output["ta_score"] > 1:
        direction = "Bullish"
    elif ta_output["ta_score"] < -1:
        direction = "Bearish"
    else:
        direction = "Neutral"

    # --- Current Price (SINGLE SOURCE OF TRUTH)
    current_price = float(price_df["close"].iloc[-1])

    # --- Range Engines
    active_range = generate_ranges(
        current_price=current_price,
        volatility_pct=ta_output["volatility_pct"],
        confidence=confidence,
        direction=direction
    )

    multi_ranges = generate_multi_ranges(
        current_price=current_price,
        volatility_pct=ta_output["volatility_pct"],
        direction=direction
    )

    return {
        "direction": direction,
        "regime": regime,
        "confidence": confidence,
        "active_strategy": active_range,
        "multi_ranges": multi_ranges,
        "ta_score": ta_output["ta_score"],
        "ta_drivers": ta_output["drivers"],
        "fa_drivers": fa_output["drivers"]
    }
