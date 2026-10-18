"""
A8-CongruenceAdapter — Altitude Guard
Author: Borealis S. Hedling
License: MIT

The altitude guard enforces invariant constraints required for safe operation
of the A8 layer. It ensures that:

    - all signals are numeric
    - all values are finite
    - no negative magnitudes appear
    - no domain violations occur
    - congruence outputs remain in [-1, 1]

This guard is intentionally strict and minimal. It is not a model; it is a
firewall between A7.2 and CAUSA.
"""

from typing import Dict
import numpy as np


def _check_numeric(name: str, value: float):
    """Ensure the value is numeric and finite."""
    if np.isnan(value):
        raise ValueError(f"{name} is NaN — altitude violation.")
    if not np.isfinite(value):
        raise ValueError(f"{name} is non-finite — altitude violation.")


def _check_non_negative(name: str, value: float):
    """Ensure the value is non-negative."""
    if value < 0:
        raise ValueError(f"{name} is negative — altitude violation.")


def _check_unit_interval(name: str, value: float):
    """Ensure the value lies within [-1, 1]."""
    if value < -1.0 or value > 1.0:
        raise ValueError(f"{name} = {value} outside [-1, 1] — altitude violation.")


def validate_signals(signals: Dict[str, float]):
    """
    Validate raw or normalized geometric signals.

    Parameters
    ----------
    signals : dict
        {
            "D": float,
            "K": float,
            "C": float,
            "T": float,
            "P": float
        }
    """
    for name, value in signals.items():
        _check_numeric(name, value)
        _check_non_negative(name, value)


def validate_congruence(congruence: Dict[str, float]):
    """
    Validate valence/arousal outputs.

    Parameters
    ----------
    congruence : dict
        {
            "valence": float,
            "arousal": float
        }
    """
    for name, value in congruence.items():
        _check_numeric(name, value)
        _check_unit_interval(name, value)
