# core/scenario/scenario_engine.py

def run_scenario_engine(
    fusion_output,
    capital_usd=10000,
    leverage=2,
    horizon_days=7
):
    """
    OPTION C: Capital Scenario Engine

    - Fee estimation (scenario-based)
    - Price appreciation (scenario-based)
    - Risk-aware, NO impermanent loss
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
        # Fee Estimation (7d baseline)
        # -----------------------------
        if mode == "Defensive":
            fee_rate_7d = 0.003
        elif mode == "Balanced":
            fee_rate_7d = 0.005
        else:
            fee_rate_7d = 0.008

        fees_7d = allocated_usd * fee_rate_7d
        fees_24h = fees_7d / horizon_days

        # -----------------------------
        # Price Appreciation (Scenario)
        # -----------------------------
        price_appreciation = 0.0

        if direction == "Bullish":
            assumed_move = 0.03   # +3% scenario
            price_appreciation = allocated_usd * assumed_move * confidence

        elif direction == "Bearish":
            assumed_move = -0.02  # stress scenario
            price_appreciation = allocated_usd * assumed_move * confidence

        # Neutral → 0

        net_scenario = fees_7d + price_appreciation

        results[mode] = {
            "allocated_usd": round(allocated_usd, 2),
            "liquidity_floor_usd": round(liquidity_floor_usd, 2),
            "fees_24h": round(fees_24h, 2),
            "fees_7d": round(fees_7d, 2),
            "price_appreciation": round(price_appreciation, 2),
            "net_scenario": round(net_scenario, 2),
        }

    return results
