"""Tests for calculate_net_return and calculate_scenarios.

Expected values below were worked out by hand from the formula, not copied
from running the code, so the tests check the maths rather than repeat it.
"""

from mandi_net_return import calculate_net_return, calculate_scenarios

PARAMS = {
    "s_transit": 0.05,
    "s_hold": 0.02,
    "commission_rate": 0.06,
    "transport_cost_per_quintal": 50,
    "surcharge_per_quintal": 20,
}


def test_basic_net_return():
    result = calculate_net_return(2000, 10, **PARAMS)
    assert result["net_return_per_quintal"] == 1680.28
    assert result["total_net_return"] == 16802.8
    assert result["gross_realized_price"] == 1862.0
    assert result["spoilage_total_pct"] == 0.069
    assert result["drivers"] == {
        "base_price": 2000,
        "spoilage_cost": -138.0,
        "commission": -111.72,
        "transport": -50,
        "surcharge": -20,
    }


def test_drivers_sum_to_net_return():
    result = calculate_net_return(1850, 4, **PARAMS)
    assert abs(sum(result["drivers"].values()) - result["net_return_per_quintal"]) < 0.01


def test_rain_multiplies_transit_spoilage():
    result = calculate_net_return(2000, 10, rain_mult=2.0, **PARAMS)
    assert result["net_return_per_quintal"] == 1588.16
    assert result["gross_realized_price"] == 1764.0
    assert result["spoilage_total_pct"] == 0.118


def test_transit_spoilage_capped_at_total_loss():
    result = calculate_net_return(
        2000,
        10,
        s_transit=0.8,
        s_hold=0.02,
        commission_rate=0.06,
        transport_cost_per_quintal=50,
        surcharge_per_quintal=20,
        rain_mult=2.0,
    )
    assert result["spoilage_total_pct"] == 1.0
    assert result["gross_realized_price"] == 0.0
    assert result["net_return_per_quintal"] == -70.0


def test_no_costs_keeps_full_price():
    result = calculate_net_return(
        1500,
        2,
        s_transit=0.0,
        s_hold=0.0,
        commission_rate=0.0,
        transport_cost_per_quintal=0,
        surcharge_per_quintal=0,
    )
    assert result["net_return_per_quintal"] == 1500.0
    assert result["total_net_return"] == 3000.0


def test_scenarios_follow_price_order():
    result = calculate_scenarios(1800, 2000, 2200, 10, PARAMS)
    assert result["p50"]["net_return_per_quintal"] == 1680.28
    assert (
        result["p10"]["net_return_per_quintal"]
        < result["p50"]["net_return_per_quintal"]
        < result["p90"]["net_return_per_quintal"]
    )
