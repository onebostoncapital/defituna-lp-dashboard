# core/scenario/scenario_engine.py

def run_scenario_engine(
    fusion_output,
    capital_usd=10000,
    leverage=2,
    horizon_days=7
):
    """
    Scenario-based capital intelligence.
    No predictions. No impermanent loss.
    """

    exposure = capital_usd * leverage
    direction = fusion_output["final_direction"]
    confidence = fusion_output["final_confidence"]

    ranges = fusion_output["multi_ranges"]["ranges"]
    allocation = fusion_output["multi_ranges"]["allocation"]

    results = {}

    for mode in ["Defensive", "Balanced", "Aggressive"]:
        alloc_pct = allocation[mode]
        range_info = ranges[mode]

        allocated_usd = exposure * alloc_pct
        liquidity_floor_usd = allocated_usd * range_info["liquidity_floor"]

        # -----------------------------
        # Fee estimation (simple model)
        # -----------------------------
        width = range_info["width_pct"]

        fee_factor = (
            0.003 if mode == "Defensive"
            else 0.005 if mode == "Balanced"
            else 0.008
        )

        estimated_fees_7d = allocated_usd * fee_factor
        estimated_fees_24h = estimated_fees_7d / horizon_days

        # -----------------------------
        # Price appreciation scenario
        # -----------------------------
        appreciation_usd = 0.0

        if direction == "Bullish":
            assumed_move = 0.03  # +3% scenario
            appreciation_usd = allocated_usd * assumed_move * confidence

        elif direction == "Bearish":
            assumed_move = -0.02  # stress scenario
            appreciation_usd = allocated_usd * assumed_move * confidence

        # Neutral → 0

        results[mode] = {
            "allocated_usd": round(allocated_usd, 2),
            "liquidity_floor_usd": round(liquidity_floor_usd, 2),
            "fees_24h": round(estimated_fees_24h, 2),
            "fees_7d": round(estimated_fees_7d, 2),
            "price_appreciation": round(appreciation_usd, 2),
            "net_scenario": round(
                estimated_fees_7d + appreciation_usd, 2
            )
        }

    return results
