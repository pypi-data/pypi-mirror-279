"""
The :mod:`fairbalance.datasets` module includes loader for dataset
commonly used in fairness studies.
"""

from ._datasets_loader import (load_adult,
                               load_bank_marketing,
                               load_KDD_census,
                               load_ACS)
from ._datasets_constants import (ADULT_METADATA,
                                  BANK_MARKETING_METADATA,
                                  KDD_CENSUS_METADATA,
                                  ACS_METADATA)

__all__ = [
    "load_adult",
    "load_bank_marketing",
    "load_KDD_census",
    "load_ACS",
    "ADULT_METADATA",
    "BANK_MARKETING_METADATA",
    "KDD_CENSUS_METADATA",
    "ACS_METADATA"
]
