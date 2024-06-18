"""
The :mod:`fairbalance.metrics` module includes fairness metrics for datasets, as well as the FairnessAnalysis class.
"""

from ._dataset_metrics import DIR, SPD, PMI, balance, balance_index, CBS
from ._fairness_analysis import FairnessAnalysis

__all__ =[
    "DIR",
    "SPD",
    "PMI",
    "balance",
    "balance_index",
    "CBS",
    "FairnessAnalysis"
]