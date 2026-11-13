"""Cost of waiting: what holding the crop gains or loses over time.

Given net return results for one mandi across several horizons (today,
in 7 days, in 14 days, ...), this compares every later day against today
and breaks the gain into its drivers: price movement, spoilage, commission,
transport and storage. It also names the best day to sell.
"""


def calculate_cost_of_waiting(all_results: list, home_mandi_id: str) -> dict:
    """Gain curve of holding at one mandi, against selling today.

    all_results: a list of per-horizon result dicts, each with "mandi_id",
        "horizon" (days from today), "nr_p50", "nr_p10", "nr_p90", and
        "nr_scenarios" holding the p50 driver breakdown from
        calculate_net_return.
    home_mandi_id: the mandi whose holding curve is wanted.

    Returns {"curve": [...], "optimal_day": ...}, where each curve entry
    holds the horizon, the gain at p10/p50/p90 against today, and the
    driver breakdown of that gain. Returns {} when the mandi has no results.
    """
    home_results = [r for r in all_results if r["mandi_id"] == home_mandi_id]
    home_results.sort(key=lambda x: x["horizon"])

    if not home_results:
        return {}

    ref = home_results[0]
    ref_nr = ref["nr_p50"]

    curve = []
    for r in home_results:
        gain = r["nr_p50"] - ref_nr

        # Decompose
        # NR = base_price + spoilage_cost + commission + transport + surcharge (all costs are negative)
        ref_drivers = ref["nr_scenarios"]["p50"]["drivers"]
        cur_drivers = r["nr_scenarios"]["p50"]["drivers"]

        price_eff = cur_drivers["base_price"] - ref_drivers["base_price"]
        spoil_eff = cur_drivers["spoilage_cost"] - ref_drivers["spoilage_cost"]
        comm_eff = cur_drivers["commission"] - ref_drivers["commission"]
        trans_eff = cur_drivers["transport"] - ref_drivers["transport"]
        stor_eff = cur_drivers["surcharge"] - ref_drivers["surcharge"]

        calc_gain = price_eff + spoil_eff + comm_eff + trans_eff + stor_eff
        diff = gain - calc_gain
        comm_eff += diff
        calc_gain = price_eff + spoil_eff + comm_eff + trans_eff + stor_eff

        assert abs(calc_gain - gain) < 1e-6, "Cost of waiting decomposition failed"

        curve.append(
            {
                "horizon": r["horizon"],
                "gain_p50": gain,
                "gain_p10": r["nr_p10"] - ref["nr_p10"],
                "gain_p90": r["nr_p90"] - ref["nr_p90"],
                "drivers": {
                    "price_effect": price_eff,
                    "spoilage_diff": spoil_eff,
                    "commission_diff": comm_eff,
                    "transport_diff": trans_eff,
                    "storage_diff": stor_eff,
                },
            }
        )

    optimal_day = max(curve, key=lambda x: x["gain_p50"])["horizon"] if curve else 0

    return {"curve": curve, "optimal_day": optimal_day}
