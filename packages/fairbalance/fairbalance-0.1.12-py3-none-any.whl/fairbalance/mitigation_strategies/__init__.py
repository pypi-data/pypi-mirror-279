"""
The :mod:`fairbalance.mitigation_strategies` module includes classes to mitigate bias using resampling strategies.
"""

from ._mitigation_strategies import BalanceOutput, BalanceAttributes, BalanceOutputForAttributes, CompleteBalance

__all__ = [
    "BalanceOutput",
    "BalanceAttributes",
    "BalanceOutputForAttributes",
    "CompleteBalance"
]