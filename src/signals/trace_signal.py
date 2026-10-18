"""
A8-CongruenceAdapter — Trace-Class Deviation Signal
Author: Borealis S. Hedling
License: MIT

This module computes the trace-class deviation T, defined as:

    T = | Tr(ρ) - 1 |

where:
    ρ is a model-specific state representation (matrix-like),
    Tr(ρ) is its trace.

A8 does not assume any particular structure for ρ beyond numeric
traceability. This module enforces altitude-safe sanity checks.
"""

from typing import Any
import numpy as np


def trace_deviation(rho: Any) -> float:
    """
    Compute the trace-class deviation:
        T = | Tr(ρ) - 1 |

    Parameters
    ----------
    rho : Any
        A model-specific state representation. Must be convertible to a
        numeric matrix or array.

    Returns
    -------
    float
        The absolute deviation of the trace from 1, guaranteed finite
        and non-negative.

    Raises
    ------
    ValueError
        If rho is non-numeric, contains NaNs, or cannot be traced.
    """

    # Convert to array
    try:
        arr = np.asarray(rho, dtype=float)
    except Exception as e:
        raise ValueError(f"Trace deviation received non-numeric input: {e}")

    # Sanity checks
    if np.isnan(arr).any():
        raise ValueError("Trace deviation matrix contains NaNs.")

    # Trace computation
    try:
        tr = float(np.trace(arr))
    except Exception as e:
        raise ValueError(f"Trace computation failed: {e}")

    # Compute deviation
    deviation = abs(tr - 1.0)

    # Must be non-negative and finite
    if deviation < 0 or not np.isfinite(deviation):
        raise ValueError("Trace deviation produced invalid value.")

    return deviation
