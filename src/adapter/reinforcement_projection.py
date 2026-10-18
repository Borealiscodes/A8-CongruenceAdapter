"""
A8-CongruenceAdapter — Reinforcement Projection
Author: Borealis S. Hedling
License: MIT

This module normalizes and bounds the five geometric signals used by the
A8 congruence adapter. It ensures altitude-safe behavior by enforcing:

    - non-negativity
    - finite values
    - Lipschitz-safe scaling
    - bounded outputs in [0, 1]

The projection here is NOT the final congruence mapping. It prepares
signals for the A8 valence/arousal projection.
"""

from typing import Dict
import numpy as np


def _safe_float(x: float) -> float:
    """Convert to float and enforce altitude-safe sanity constraints."""
    xf = float(x)

    if np.isnan(xf):
        raise ValueError("Signal contains NaN, violating altitude safety.")

    if not np.isfinite(xf):
        raise ValueError("Signal is not finite, violating altitude safety.")

    if xf < 0:
        raise ValueError("Signal must be non-negative.")

    return xf


def _normalize(x: float, max_value: float) -> float:
    """
    Normalize a signal into [0, 1] using a Lipschitz-safe clamp.

    Parameters
    ----------
    x : float
        Raw signal value.
    max_value : float
        Maximum expected magnitude for normalization.

    Returns
    -------
    float
        Normalized value in [0, 1].
    """
    xf = _safe_float(x)

    if max_value <= 0:
        raise ValueError("max_value must be positive for normalization.")

    return min(1.0, xf / max_value)


def project_signals(
    D: float,
    K: float,
    C: float,
    T: float,
    P: float,
    max_values: Dict[str, float] = None
) -> Dict[str, float]:
    """
    Normalize and bound all five geometric signals.

    Parameters
    ----------
    D, K, C, T, P : float
        Raw geometric signals.
    max_values : dict, optional
        Dictionary specifying normalization bounds for each signal.
        Defaults are altitude-safe heuristics.

    Returns
    -------
    dict
        Normalized signals:
            {
                "D": D_norm,
                "K": K_norm,
                "C": C_norm,
                "T": T_norm,
                "P": P_norm
            }
    """

    # Default altitude-safe normalization bounds
    if max_values is None:
        max_values = {
            "D": 10.0,   # spectral drift rarely exceeds this
            "K": 5.0,    # DEC curvature deviation
            "C": 3.0,    # hyperbolic contraction factor
            "T": 2.0,    # trace deviation
            "P": 10.0    # phase-energy magnitude
        }

    return {
        "D": _normalize(D, max_values["D"]),
        "K": _normalize(K, max_values["K"]),
        "C": _normalize(C, max_values["C"]),
        "T": _normalize(T, max_values["T"]),
        "P": _normalize(P, max_values["P"]),
    }
