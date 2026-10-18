"""
A8-CongruenceAdapter — Congruence Mapping
Author: Borealis S. Hedling
License: MIT

This module defines the A8 projection from normalized geometric signals
into CAUSA's congruence space:

    valence = f(D, P)
    arousal = g(K, C, T)

The functions f and g are intentionally simple, monotonic, and
Lipschitz-bounded. A8 is an adapter layer, not a model: it provides
architecture-agnostic mapping, not learned behavior.
"""

from typing import Dict
import numpy as np


def _bounded(x: float) -> float:
    """
    Clamp a value into [-1, 1] with altitude-safe sanity checks.
    """
    if np.isnan(x):
        raise ValueError("Congruence mapping produced NaN.")

    if not np.isfinite(x):
        raise ValueError("Congruence mapping produced non-finite value.")

    return max(-1.0, min(1.0, float(x)))


def f_valence(D: float, P: float) -> float:
    """
    Compute valence from normalized spectral drift (D) and phase-energy (P).

    A simple monotonic Lipschitz-safe form:
        valence = 0.6 * (1 - D) + 0.4 * (1 - P)

    Both D and P are in [0, 1], so valence is naturally in [-1, 1].
    """
    raw = 0.6 * (1.0 - D) + 0.4 * (1.0 - P)
    return _bounded(raw)


def g_arousal(K: float, C: float, T: float) -> float:
    """
    Compute arousal from normalized curvature (K), contraction (C),
    and trace deviation (T).

    A simple monotonic Lipschitz-safe form:
        arousal = 0.5 * K + 0.3 * C + 0.2 * T

    All inputs are in [0, 1], so arousal is naturally in [0, 1].
    """
    raw = 0.5 * K + 0.3 * C + 0.2 * T
    return _bounded(raw)


def project_to_congruence(norm: Dict[str, float]) -> Dict[str, float]:
    """
    Compute valence and arousal from normalized signals.

    Parameters
    ----------
    norm : dict
        Dictionary containing normalized signals:
            {
                "D": float,
                "K": float,
                "C": float,
                "T": float,
                "P": float
            }

    Returns
    -------
    dict
        {
            "valence": float in [-1, 1],
            "arousal": float in [-1, 1]
        }
    """

    D = norm["D"]
    K = norm["K"]
    C = norm["C"]
    T = norm["T"]
    P = norm["P"]

    return {
        "valence": f_valence(D, P),
        "arousal": g_arousal(K, C, T),
    }
