"""
The :mod:`fairbalance.metrics` module includes fairness metrics for datasets.
"""

from ._dataset_metrics import DIR, SPD, PMI, balance, balance_index, FS

__all__ =[
    "DIR",
    "SPD",
    "PMI",
    "balance",
    "balance_index",
    "FS"
]