"""
Scenario Math Engine
--------------------
Purpose:
- Compute capital appreciation scenarios for LP positions
- Cost-aware (DefiTuna-style leverage)
- Scenario-based, not predictive

Assumptions:
- Margin = base capital
- Borrowed portion = (leverage - 1) * margin
- Funding cost applies ONLY to borrowed portion
"""

from typing import Dict


def compute_scenarios(
    *,
    current_price: float,
    ranges: Dict[str, Dict],
    capital_usd: float = 10_000.0,
    leverage: float = 2.0,
    funding_rate_daily: float = 0.0005,  # 0.05% per day (example, configurable later)
    horizon_days: int = 7
) -> Dict[str, Dict]:
    """
    Returns scenario projections per LP mode.

    Parameters
    ----------
    current_price : float
        Current SOL price
    ranges : dict
        Output from multi-range engine
    capital_usd : float
        User margin capital (default $10,000)
    leverage : float
        Leverage used (default 2x)
    funding_rate_daily : float
        Daily funding rate applied to borrowed portion
    horizon_days : int
        Scenario horizon (default 7 days, optional 1 day)

    Returns
    -------
    dict
        Scenario projections per mode
    """

    effective_notional = capital_usd * leverage
    borrowed_usd = capital_usd * (leverage - 1)

    funding_cost = round(
        borrowed_usd * funding_rate_daily * horizon_days,
        2
    )

    scenarios = {}

    for mode, data in ranges.items():
        range_low = data["range_low"]
        range_high = data["range_high"]
        liquidity_floor_pct = data["liquidity_floor"]

        # Liquidity floor in USD
        liquidity_floor_usd = round(
            liquidity_floor_pct * effective_notional,
            2
        )

        # Price move percentages
        upside_pct = (range_high - current_price) / current_price
        downside_pct = (range_low - current_price) / current_price

        # Directional inventory value change (simplified, transparent)
        upside_value = effective_notional * (1 + upside_pct)
        downside_value = effective_notional * (1 + downside_pct)

        # Net outcomes after funding
        upside_net = round(upside_value - funding_cost, 2)
        downside_net = round(downside_value - funding_cost, 2)

        scenarios[mode] = {
            "liquidity_floor_pct": liquidity_floor_pct,
            "liquidity_floor_usd": liquidity_floor_usd,
            "horizon_days": horizon_days,
            "funding_cost_usd": funding_cost,
            "scenario_upper": {
                "target_price": range_high,
                "projected_value": round(upside_value, 2),
                "net_value": upside_net
            },
            "scenario_lower": {
                "target_price": range_low,
                "projected_value": round(downside_value, 2),
                "net_value": downside_net
            }
        }

    return scenarios
