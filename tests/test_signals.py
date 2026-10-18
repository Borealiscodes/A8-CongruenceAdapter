"""
Tests for A8-CongruenceAdapter geometric signal modules.
Author: Borealis S. Hedling
"""

import numpy as np
import pytest

from src.signals.spectral_signal import spectral_drift
from src.signals.curvature_signal import dec_curvature
from src.signals.hyperbolic_signal import hyperbolic_contraction
from src.signals.trace_signal import trace_deviation
from src.signals.phase_signal import phase_energy


# --- Fixtures ---------------------------------------------------------------

def gamma_identity(x):
    return x  # simplest spectral transform


def holonomy_identity(cell):
    return np.eye(3)  # zero curvature


# --- Tests: Spectral Drift --------------------------------------------------

def test_spectral_drift_basic():
    delta = np.array([1.0, 2.0, 3.0])
    D = spectral_drift(delta, gamma_identity)
    assert isinstance(D, float)
    assert D >= 0
    assert np.isfinite(D)


def test_spectral_drift_nan():
    delta = np.array([np.nan])
    with pytest.raises(ValueError):
        spectral_drift(delta, gamma_identity)


# --- Tests: DEC Curvature ---------------------------------------------------

def test_dec_curvature_zero():
    K = dec_curvature(holonomy_identity, None)
    assert isinstance(K, float)
    assert K == 0.0


def test_dec_curvature_non_square():
    def bad_holonomy(_):
        return np.array([[1, 2, 3]])  # not square
    with pytest.raises(ValueError):
        dec_curvature(bad_holonomy, None)


# --- Tests: Hyperbolic Contraction ------------------------------------------

def test_hyperbolic_contraction_small_vector():
    v = np.array([0.1, 0.2])
    C = hyperbolic_contraction(v)
    assert isinstance(C, float)
    assert C >= 0
    assert np.isfinite(C)


def test_hyperbolic_contraction_domain_violation():
    v = np.array([2.0])  # norm >= 1
    with pytest.raises(ValueError):
        hyperbolic_contraction(v)


# --- Tests: Trace Deviation -------------------------------------------------

def test_trace_deviation_identity():
    rho = np.eye(3)
    T = trace_deviation(rho)
    assert isinstance(T, float)
    assert T == abs(3 - 1)


def test_trace_deviation_nan():
    rho = np.array([[np.nan]])
    with pytest.raises(ValueError):
        trace_deviation(rho)


# --- Tests: Phase Energy ----------------------------------------------------

def test_phase_energy_basic():
    z = np.array([1 + 2j, 3 + 4j])
    P = phase_energy(z)
    assert isinstance(P, float)
    assert P >= 0
    assert np.isfinite(P)


def test_phase_energy_nan():
    z = np.array([np.nan + 1j])
    with pytest.raises(ValueError):
        phase_energy(z)
