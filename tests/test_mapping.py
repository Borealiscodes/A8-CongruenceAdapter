"""
Tests for A8-CongruenceAdapter congruence mapping module.
Author: Borealis S. Hedling
"""

import numpy as np
import pytest

from src.adapter.congruence_mapping import (
    f_valence,
    g_arousal,
    project_to_congruence,
)


# --- Valence tests -----------------------------------------------------------

def test_valence_basic():
    v = f_valence(D=0.2, P=0.3)
    assert isinstance(v, float)
    assert -1.0 <= v <= 1.0
    assert np.isfinite(v)


def test_valence_high_signals():
    # High D and P → low valence
    v = f_valence(D=1.0, P=1.0)
    assert v <= 0.0


def test_valence_low_signals():
    # Low D and P → high valence
    v = f_valence(D=0.0, P=0.0)
    assert v >= 0.9


# --- Arousal tests -----------------------------------------------------------

def test_arousal_basic():
    a = g_arousal(K=0.2, C=0.3, T=0.1)
    assert isinstance(a, float)
    assert -1.0 <= a <= 1.0
    assert np.isfinite(a)


def test_arousal_monotonicity():
    # Increasing inputs should increase arousal
    a1 = g_arousal(K=0.1, C=0.1, T=0.1)
    a2 = g_arousal(K=0.9, C=0.9, T=0.9)
    assert a2 > a1


# --- Full projection tests ---------------------------------------------------

def test_project_to_congruence_basic():
    norm = {"D": 0.2, "K": 0.3, "C": 0.4, "T": 0.1, "P": 0.5}
    out = project_to_congruence(norm)

    assert isinstance(out, dict)
    assert "valence" in out
    assert "arousal" in out

    assert -1.0 <= out["valence"] <= 1.0
    assert -1.0 <= out["arousal"] <= 1.0

    assert np.isfinite(out["valence"])
    assert np.isfinite(out["arousal"])


def test_project_to_congruence_invalid():
    norm = {"D": np.nan, "K": 0.3, "C": 0.4, "T": 0.1, "P": 0.5}
    with pytest.raises(ValueError):
        project_to_congruence(norm)
