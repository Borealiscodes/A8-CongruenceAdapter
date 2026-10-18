"""
A8-CongruenceAdapter — Signal Sanity Validator
Author: Borealis S. Hedling
License: MIT

This module performs low-level sanity checks on raw geometric signals
before they enter the A8 adapter pipeline. It ensures:

    - numeric convertibility
    - finite values
    - no NaNs
    - non-negative magnitudes
    - domain-safe norms
    - correct array structure when applicable

This validator is intentionally strict and minimal. It catches malformed
inputs early, preventing altitude violations downstream.
"""

from typing import Any
import numpy as np


def ensure_numeric(name: str, value: Any):
    """
    Ensure a value is numeric and finite.
    """
    try:
        v = float(value)
    except Exception:
        raise ValueError(f"{name} must be numeric — sanity violation.")

    if np.isnan(v):
        raise ValueError(f"{name} is NaN — sanity violation.")

    if not np.isfinite(v):
        raise ValueError(f"{name} is non-finite — sanity violation.")

    return v


def ensure_array(name: str, value: Any):
    """
    Ensure a value can be converted to a numeric array.
    """
    try:
        arr = np.asarray(value, dtype=float)
    except Exception:
        raise ValueError(f"{name} must be convertible to a numeric array.")

    if arr.size == 0:
        raise ValueError(f"{name} is empty — sanity violation.")

    if np.isnan(arr).any():
        raise ValueError(f"{name} contains NaNs — sanity violation.")

    if not np.isfinite(arr).all():
        raise ValueError(f"{name} contains non-finite values — sanity violation.")

    return arr


def ensure_non_negative(name: str, value: float):
    """
    Ensure a numeric value is non-negative.
    """
    if value < 0:
        raise ValueError(f"{name} is negative — sanity violation.")
    return value


def ensure_norm_domain(name: str, arr: Any, max_norm: float = None):
    """
    Ensure the norm of an array is domain-safe.

    Parameters
    ----------
    name : str
        Name of the signal.
    arr : Any
        Numeric array.
    max_norm : float, optional
        Maximum allowed norm. If None, no upper bound is enforced.
    """
    norm = float(np.linalg.norm(arr))

    if np.isnan(norm) or not np.isfinite(norm):
        raise ValueError(f"{name} norm is invalid — sanity violation.")

    if norm < 0:
        raise ValueError(f"{name} norm is negative — sanity violation.")

    if max_norm is not None and norm > max_norm:
        raise ValueError(
            f"{name} norm {norm} exceeds domain limit {max_norm} — sanity violation."
        )

    return norm
