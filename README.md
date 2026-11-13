# mandi-net-return

True net return maths for Indian mandi sales: sell today, hold, or travel to
a better mandi.

A mandi price is not what the farmer keeps. Spoilage in transit and in
storage eats part of the crop, the commission agent takes a cut, and
transport plus any surcharge come off the top. This package computes what is
left per quintal, and breaks it down so each cost is visible.

The maths was first written for
[Kissan Saathi](https://github.com/swastiktawate/Kissan-Saathi), an agri-tech
decision assistant for Indian farmers. It is pure calculation: no network
calls, no database, no API keys, no dependencies.

## Install

```bash
pip install mandi-net-return
```

## Use

```python
from mandi_net_return import calculate_net_return, calculate_scenarios, calculate_cost_of_waiting

result = calculate_net_return(
    price=2000,              # mandi price per quintal, in rupees
    qty_quintals=10,
    s_transit=0.05,          # share lost in transit (5%)
    s_hold=0.02,             # share lost in storage (2%)
    commission_rate=0.06,    # commission share (6%)
    transport_cost_per_quintal=50,
    surcharge_per_quintal=20,
)
print(result["net_return_per_quintal"])  # 1680.28
print(result["drivers"])
# {'base_price': 2000, 'spoilage_cost': -138.0, 'commission': -111.72,
#  'transport': -50, 'surcharge': -20}

# Pessimistic, median and optimistic prices in one call:
scenarios = calculate_scenarios(1800, 2000, 2200, 10, {
    "s_transit": 0.05,
    "s_hold": 0.02,
    "commission_rate": 0.06,
    "transport_cost_per_quintal": 50,
    "surcharge_per_quintal": 20,
})
```

Rain multiplies transit spoilage: pass `rain_mult=2.0` and transit spoilage
doubles (capped at total loss).

`calculate_cost_of_waiting(results, home_mandi_id)` compares holding the
crop across several horizons against selling today, and names the best day
to sell. See the docstrings for the result format it expects.

## Develop

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT. See LICENSE.
