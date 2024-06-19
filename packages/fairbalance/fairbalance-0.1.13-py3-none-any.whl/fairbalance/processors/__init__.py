"""
The :mod:`fairbalance.processor` module includes different processors to use in mitigation strategies.
"""

from ._processors import RandomOverSamplerProcessor, RandomUnderSamplerProcessor, SMOTENCProcessor

__all__ = [
    "RandomOverSamplerProcessor",
    "RandomUnderSamplerProcessor",
    "SMOTENCProcessor"
]
