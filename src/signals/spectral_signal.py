"""
A8-CongruenceAdapter — Spectral Drift Signal
Author: Borealis S. Hedling
License: MIT

This module computes the spectral drift magnitude D, defined as:

    D = || Γ(Δ(x)) ||

where:
    Δ(x) is a model-specific state difference,
    Γ is a spectral decomposition or spectral transform,
    || · || is the Euclidean norm.

The function is intentionally system-agnostic: callers must supply
their own Δ(x) and Γ implementations. A8 only enforces altitude-safe
normalization and sanity checks.
"""

from typing import Callable, Any
import numpy as np


def spectral_drift(delta_x: Any, gamma: Callable[[Any], Any]) -> float:
    """
    Compute the spectral drift magnitude D = || Γ(Δ(x)) ||.

    Parameters
    ----------
    delta_x : Any
        A model-specific state difference. A8 does not assume structure.
    gamma : Callable
        A spectral transform applied to delta_x. Must return a numeric array.

    Returns
    -------
    float
        The spectral drift magnitude, guaranteed to be finite and non-negative.

    Raises
    ------
    ValueError
        If gamma(delta_x) is non-numeric, contains NaNs, or cannot be normed.
    """

    # Apply spectral transform
    transformed = gamma(delta_x)

    # Convert to array
    try:
        arr = np.asarray(transformed, dtype=float)
    except Exception as e:
        raise ValueError(f"Spectral transform produced non-numeric output: {e}")

    # Sanity checks
    if np.isnan(arr).any():
        raise ValueError("Spectral drift contains NaNs, violating altitude safety.")

    # Compute Euclidean norm
    drift = float(np.linalg.norm(arr))

    # Enforce altitude-safe non-negativity
    if drift < 0:
        raise ValueError("Spectral drift must be non-negative.")

    return drift
