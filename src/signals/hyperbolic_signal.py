"""
A8-CongruenceAdapter — Hyperbolic Contraction Signal
Author: Borealis S. Hedling
License: MIT

This module computes the hyperbolic contraction factor C, defined as:

    C = atanh(||v||) / ||v||

where:
    v is a model-specific vector representing a local geometric displacement.

The function is system-agnostic: callers supply v. A8 enforces altitude-safe
sanity checks, including domain constraints for atanh and non-negativity.
"""

from typing import Any
import numpy as np


def hyperbolic_contraction(v: Any) -> float:
    """
    Compute the hyperbolic contraction factor:
        C = atanh(||v||) / ||v||

    Parameters
    ----------
    v : Any
        A model-specific vector. Must be convertible to a numeric array.

    Returns
    -------
    float
        The contraction factor, guaranteed finite, real, and altitude-safe.

    Raises
    ------
    ValueError
        If v is non-numeric, contains NaNs, or ||v|| is outside the valid domain.
    """

    # Convert to array
    try:
        arr = np.asarray(v, dtype=float)
    except Exception as e:
        raise ValueError(f"Hyperbolic contraction received non-numeric input: {e}")

    # Sanity checks
    if np.isnan(arr).any():
        raise ValueError("Hyperbolic contraction vector contains NaNs.")

    # Compute norm
    norm = float(np.linalg.norm(arr))

    if norm < 0:
        raise ValueError("Vector norm must be non-negative.")

    # Domain constraint: atanh(x) is only defined for |x| < 1
    if norm >= 1.0:
        raise ValueError(
            f"Hyperbolic contraction undefined for ||v|| >= 1 (got {norm}). "
            "Altitude-safe domain requires ||v|| < 1."
        )

    # Handle zero norm safely: limit of atanh(x)/x as x→0 is 1
    if norm == 0.0:
        return 1.0

    # Compute contraction factor
    contraction = float(np.arctanh(norm) / norm)

    # Must be non-negative and finite
    if contraction < 0 or not np.isfinite(contraction):
        raise ValueError("Hyperbolic contraction produced invalid value.")

    return contraction
