"""
Tests for A8-CongruenceAdapter reinforcement projection module.
Author: Borealis S. Hedling
"""

import numpy as np
import pytest

from src.adapter.reinforcement_projection import project_signals


# --- Basic normalization tests ----------------------------------------------

def test_projection_basic():
    norm = project_signals(
        D=5.0,
        K=2.0,
        C=1.0,
        T=0.5,
        P=3.0,
        max_values={"D": 10, "K": 5, "C": 3, "T": 2, "P": 10},
    )

    assert isinstance(norm, dict)
    for key in ["D", "K", "C", "T", "P"]:
        assert key in norm
        assert 0.0 <= norm[key] <= 1.0
        assert np.isfinite(norm[key])


# --- Clamping tests ----------------------------------------------------------

def test_projection_clamping():
    # Values exceeding max should clamp to 1.0
    norm = project_signals(
        D=999,
        K=999,
        C=999,
        T=999,
        P=999,
        max_values={"D": 10, "K": 5, "C": 3, "T": 2, "P": 10},
    )

    assert all(v == 1.0 for v in norm.values())


# --- Negative value tests ----------------------------------------------------

def test_projection_negative_value():
    with pytest.raises(ValueError):
        project_signals(
            D=-1.0,
            K=0.0,
            C=0.0,
            T=0.0,
            P=0.0,
            max_values={"D": 10, "K": 5, "C": 3, "T": 2, "P": 10},
        )


# --- Invalid max_values tests ------------------------------------------------

def test_projection_invalid_max_values():
    with pytest.raises(ValueError):
        project_signals(
            D=1.0,
            K=1.0,
            C=1.0,
            T=1.0,
            P=1.0,
            max_values={"D": 0, "K": 5, "C": 3, "T": 2, "P": 10},
        )
