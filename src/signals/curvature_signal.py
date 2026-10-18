"""
A8-CongruenceAdapter — DEC Holonomy Curvature Signal
Author: Borealis S. Hedling
License: MIT

This module computes the discrete curvature magnitude K, defined as:

    K = || H(c) - I ||_F

where:
    H(c) is a holonomy operator derived from a discrete exterior calculus (DEC)
    formulation, and I is the identity operator.

A8 does not assume any specific DEC implementation. Callers must supply their
own holonomy operator H(c). This module enforces altitude-safe normalization
and sanity constraints.
"""

from typing import Callable, Any
import numpy as np


def dec_curvature(holonomy: Callable[[Any], Any], cell: Any) -> float:
    """
    Compute the DEC holonomy curvature K = || H(c) - I ||_F.

    Parameters
    ----------
    holonomy : Callable
        A function returning a square matrix representing holonomy for a cell c.
    cell : Any
        A model-specific cell or region. A8 does not assume structure.

    Returns
    -------
    float
        The Frobenius norm of (H(c) - I), guaranteed to be finite and non-negative.

    Raises
    ------
    ValueError
        If holonomy(cell) is non-numeric, non-square, contains NaNs, or cannot be normed.
    """

    # Compute holonomy matrix
    try:
        H = np.asarray(holonomy(cell), dtype=float)
    except Exception as e:
        raise ValueError(f"Holonomy operator produced non-numeric output: {e}")

    # Sanity: must be square
    if H.ndim != 2 or H.shape[0] != H.shape[1]:
        raise ValueError("Holonomy matrix must be square.")

    # Identity matrix
    I = np.eye(H.shape[0], dtype=float)

    # Compute deviation
    deviation = H - I

    # Sanity checks
    if np.isnan(deviation).any():
        raise ValueError("Holonomy curvature contains NaNs, violating altitude safety.")

    # Frobenius norm
    curvature = float(np.linalg.norm(deviation, ord="fro"))

    # Enforce altitude-safe non-negativity
    if curvature < 0:
        raise ValueError("Curvature magnitude must be non-negative.")

    return curvature
