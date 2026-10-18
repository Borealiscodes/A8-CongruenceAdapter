"""
A8-CongruenceAdapter — Hallucination Guard Bridge
Author: Borealis S. Hedling
License: MIT

This module acts as the altitude firewall between A8 and CAUSA. It ensures
that the congruence outputs (valence, arousal) do not exhibit unstable or
hallucination-like behavior, including:

    - discontinuities
    - extreme spikes
    - sudden jumps
    - malformed congruence pairs
    - out-of-altitude drift

The guard is intentionally strict and minimal. It does not interpret signals;
it only enforces stability and continuity constraints.
"""

from typing import Dict
import numpy as np


def _check_stability(name: str, value: float, previous: float, max_delta: float):
    """
    Ensure the change between consecutive values is stable.

    Parameters
    ----------
    name : str
        Name of the congruence dimension.
    value : float
        Current value.
    previous : float
        Previous value.
    max_delta : float
        Maximum allowed change.
    """
    delta = abs(value - previous)

    if delta > max_delta:
        raise ValueError(
            f"{name} changed by {delta}, exceeding stability limit {max_delta} — "
            "hallucination guard violation."
        )


def _check_pair_structure(congruence: Dict[str, float]):
    """
    Ensure the congruence pair is structurally valid.
    """
    if "valence" not in congruence or "arousal" not in congruence:
        raise ValueError("Congruence pair missing required keys — guard violation.")

    v = congruence["valence"]
    a = congruence["arousal"]

    if np.isnan(v) or np.isnan(a):
        raise ValueError("Congruence pair contains NaN — guard violation.")

    if not np.isfinite(v) or not np.isfinite(a):
        raise ValueError("Congruence pair contains non-finite values — guard violation.")

    if v < -1.0 or v > 1.0 or a < -1.0 or a > 1.0:
        raise ValueError("Congruence values outside [-1, 1] — guard violation.")


def hallucination_guard(
    congruence: Dict[str, float],
    previous: Dict[str, float],
    max_delta: float = 0.25
):
    """
    Enforce hallucination guard constraints on congruence outputs.

    Parameters
    ----------
    congruence : dict
        Current congruence output:
            {
                "valence": float,
                "arousal": float
            }
    previous : dict
        Previous congruence output (same structure).
    max_delta : float
        Maximum allowed change between consecutive values.

    Raises
    ------
    ValueError
        If any stability or structural constraint is violated.
    """

    # Structural validity
    _check_pair_structure(congruence)
    _check_pair_structure(previous)

    # Stability checks
    _check_stability("valence", congruence["valence"], previous["valence"], max_delta)
    _check_stability("arousal", congruence["arousal"], previous["arousal"], max_delta)
