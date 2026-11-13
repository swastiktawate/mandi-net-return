"""Net return of a mandi sale, after every cost the farmer actually pays.

A mandi price is not what the farmer keeps. Spoilage in transit and in
storage eats part of the crop, the commission agent takes a cut, and
transport plus any surcharge come off the top. This module computes what is
left per quintal, and breaks it down so each cost is visible.
"""


def calculate_net_return(
    price: float,
    qty_quintals: float,
    s_transit: float,
    s_hold: float,
    commission_rate: float,
    transport_cost_per_quintal: float,
    surcharge_per_quintal: float,
    rain_mult: float = 1.0,
):
    """Net return for one sale at one mandi.

    price: mandi price per quintal, in rupees.
    qty_quintals: quantity sold, in quintals.
    s_transit: share of the crop lost in transit, 0 to 1.
    s_hold: share lost while holding in storage, 0 to 1.
    commission_rate: commission share of the realised price, 0 to 1.
    transport_cost_per_quintal: transport cost per quintal, in rupees.
    surcharge_per_quintal: any extra charge per quintal, in rupees.
    rain_mult: rain multiplies transit spoilage (1.0 means no rain effect).
        Transit spoilage is capped at total loss.

    Returns a dict with net return per quintal and in total, the realised
    price after spoilage, the total spoilage share, and a driver breakdown
    whose parts sum exactly to the net return.
    """
    effective_s_transit = min(1.0, s_transit * rain_mult)
    s_total = 1 - (1 - effective_s_transit) * (1 - s_hold)

    g = price * (1 - s_total)
    comm = commission_rate * g

    nr = g - comm - transport_cost_per_quintal - surcharge_per_quintal
    total_val = nr * qty_quintals

    spoilage_cost = price - g

    drivers = {
        "base_price": price,
        "spoilage_cost": -spoilage_cost,
        "commission": -comm,
        "transport": -transport_cost_per_quintal,
        "surcharge": -surcharge_per_quintal,
    }

    assert abs(sum(drivers.values()) - nr) < 1e-6, "Drivers do not sum to NR exactly"

    return {
        "net_return_per_quintal": round(nr, 2),
        "total_net_return": round(total_val, 2),
        "gross_realized_price": round(g, 2),
        "spoilage_total_pct": round(s_total, 4),
        "drivers": {k: round(v, 2) for k, v in drivers.items()},
    }


def calculate_scenarios(price_p10, price_p50, price_p90, qty, params):
    """Net return under pessimistic, median and optimistic prices.

    price_p10, price_p50, price_p90: the 10th, 50th and 90th percentile
    prices per quintal. qty: quantity in quintals. params: the same
    keyword arguments calculate_net_return takes, except price and qty.

    Returns {"p10": ..., "p50": ..., "p90": ...}, one result per price.
    """
    return {
        "p10": calculate_net_return(price_p10, qty, **params),
        "p50": calculate_net_return(price_p50, qty, **params),
        "p90": calculate_net_return(price_p90, qty, **params),
    }
