"""True net return maths for Indian mandi sales.

The question this package answers: after spoilage, commission, transport and
storage, what does the farmer actually keep per quintal, and is it better to
sell today, hold for a later day, or travel to a different mandi?

The maths was first written for Kissan Saathi
(https://github.com/swastiktawate/Kissan-Saathi), an agri-tech decision
assistant for Indian farmers. It is pure calculation: no network calls, no
database, no API keys, no dependencies.
"""

from .cost_of_waiting import calculate_cost_of_waiting
from .net_return import calculate_net_return, calculate_scenarios

__all__ = [
    "calculate_cost_of_waiting",
    "calculate_net_return",
    "calculate_scenarios",
]

__version__ = "0.1.0"
