"""
The :mod:`fairbalance._tools` module should not be used. it includes different useful classes and functions internal to the process,
as well as depcrecated features.
"""

# from ._fairness_analysis import FairnessAnalysis
from ._mitigator import Mitigator
from ._utils import sanity_checker, binarize_columns

__all__ = [
    # "FairnessAnalysis",
    "Mitigator",
    "sanity_checker",
    "binarize_columns"

]