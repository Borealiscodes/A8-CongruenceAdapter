"""
Full integration tests for A8-CongruenceAdapter.
Author: Borealis S. Hedling
"""

import numpy as np
import pytest

from src.integration_harness import run_adapter


# --- Identity operators for testing -----------------------------------------

def gamma_identity(x):
    return x

def holonomy_identity(cell):
    return np.eye(3)


# --- Basic end-to-end test ---------------------------------------------------

def test_integration_basic():
    delta_x = np.array([1.0, 2.0, 3.0])
    v = np.array([0.1, 0.2])
    rho = np.eye(3)
    z = np.array([1 + 2j, 3 + 4j])

    out = run_adapter(
        delta_x=delta_x,
        gamma=gamma_identity,
        holonomy=holonomy_identity,
        cell=None,
        v=v,
        rho=rho,
        z=z,
        previous_congruence={"valence": 0.0, "arousal": 0.0},
    )

    assert isinstance(out, dict)
    assert "valence" in out
    assert "arousal" in out

    assert -1.0 <= out["valence"] <= 1.0
    assert -1.0 <= out["arousal"] <= 1.0

    assert np.isfinite(out["valence"])
    assert np.isfinite(out["arousal"])


# --- Stability guard test ----------------------------------------------------

def test_integration_stability_guard():
    delta_x = np.array([1.0])
    v = np.array([0.1])
    rho = np.eye(2)
    z = np.array([1 + 1j])

    prev = {"valence": 0.0, "arousal": 0.0}

    # Small change → allowed
    out = run_adapter(
        delta_x=delta_x,
        gamma=gamma_identity,
        holonomy=holonomy_identity,
        cell=None,
        v=v,
        rho=rho,
        z=z,
        previous_congruence=prev,
    )

    assert -1.0 <= out["valence"] <= 1.0
    assert -1.0 <= out["arousal"] <= 1.0


def test_integration_stability_violation():
    delta_x = np.array([100.0])  # large drift → large valence change
    v = np.array([0.1])
    rho = np.eye(2)
    z = np.array([1 + 1j])

    prev = {"valence": 0.0, "arousal": 0.0}

    with pytest.raises(ValueError):
        run_adapter(
            delta_x=delta_x,
            gamma=gamma_identity,
            holonomy=holonomy_identity,
            cell=None,
            v=v,
            rho=rho,
            z=z,
            previous_congruence=prev,
        )


# --- Invalid input test ------------------------------------------------------

def test_integration_invalid_input():
    delta_x = np.array([np.nan])
    v = np.array([0.1])
    rho = np.eye(2)
    z = np.array([1 + 1j])

    with pytest.raises(ValueError):
        run_adapter(
            delta_x=delta_x,
            gamma=gamma_identity,
            holonomy=holonomy_identity,
            cell=None,
            v=v,
            rho=rho,
            z=z,
            previous_congruence={"valence": 0.0, "arousal": 0.0},
        )
