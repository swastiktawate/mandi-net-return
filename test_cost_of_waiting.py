"""Tests for calculate_cost_of_waiting."""

from mandi_net_return import calculate_cost_of_waiting


def _result(mandi_id, horizon, nr_p50, nr_p10, nr_p90, base_price):
    return {
        "mandi_id": mandi_id,
        "horizon": horizon,
        "nr_p50": nr_p50,
        "nr_p10": nr_p10,
        "nr_p90": nr_p90,
        "nr_scenarios": {
            "p50": {
                "drivers": {
                    "base_price": base_price,
                    "spoilage_cost": -100,
                    "commission": -50,
                    "transport": -30,
                    "surcharge": -20,
                }
            }
        },
    }


def test_gain_curve_and_optimal_day():
    results = [
        _result("VASHI", 7, 1050, 950, 1150, 1250),
        _result("VASHI", 0, 1000, 900, 1100, 1200),
        _result("PUNE", 7, 9999, 9999, 9999, 9999),
    ]
    out = calculate_cost_of_waiting(results, "VASHI")
    assert out["optimal_day"] == 7
    assert [c["horizon"] for c in out["curve"]] == [0, 7]
    today, later = out["curve"]
    assert today["gain_p50"] == 0
    assert later["gain_p50"] == 50
    assert later["gain_p10"] == 50
    assert later["gain_p90"] == 50
    assert later["drivers"]["price_effect"] == 50
    assert later["drivers"]["spoilage_diff"] == 0
    assert later["drivers"]["commission_diff"] == 0
    assert later["drivers"]["transport_diff"] == 0
    assert later["drivers"]["storage_diff"] == 0


def test_empty_or_unknown_mandi_returns_empty_dict():
    assert calculate_cost_of_waiting([], "VASHI") == {}
    assert calculate_cost_of_waiting([_result("PUNE", 0, 1000, 900, 1100, 1200)], "VASHI") == {}
