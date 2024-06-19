"""
The :mod:`fairbalance.tools` module includes classes for fairness analysis and bais mitigation.
"""

from ._fairness_analysis import FairnessAnalysis
from ._mitigator import Mitigator
from ._processor import Processor

__all__ = [
    "FairnessAnalysis",
    "Mitigator",
    "Processor"
]