"""
A8-CongruenceAdapter — Phase-Energy Signal
Author: Borealis S. Hedling
License: MIT

This module computes the phase-energy magnitude P, defined as:

    P = || Im(z) ||

where:
    z is a model-specific complex-valued signal,
    Im(z) extracts the imaginary component.

A8 does not assume any specific structure for z beyond numeric
convertibility. This module enforces altitude-safe sanity checks.
"""

from typing import Any
import numpy as np


def phase_energy(z: Any) -> float:
    """
    Compute the phase-energy magnitude:
        P = || Im(z) ||

    Parameters
    ----------
    z : Any
        A model-specific complex-valued signal. Must be convertible to
        a numeric array or complex array.

    Returns
    -------
    float
        The magnitude of the imaginary component, guaranteed finite and
        non-negative.

    Raises
    ------
    ValueError
        If z is non-numeric, contains NaNs, or cannot be normed.
    """

    # Convert to array (allow complex dtype)
    try:
        arr = np.asarray(z)
    except Exception as e:
        raise ValueError(f"Phase-energy received non-numeric input: {e}")

    # Extract imaginary component
    try:
        imag = np.imag(arr).astype(float)
    except Exception as e:
        raise ValueError(f"Failed to extract imaginary component: {e}")

    # Sanity checks
    if np.isnan(imag).any():
        raise ValueError("Phase-energy contains NaNs, violating altitude safety.")

    # Compute Euclidean norm
    energy = float(np.linalg.norm(imag))

    # Must be non-negative and finite
    if energy < 0 or not np.isfinite(energy):
        raise ValueError("Phase-energy produced invalid value.")

    return energy
