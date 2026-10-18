"""
Tests for A8-CongruenceAdapter validator modules.
Author: Borealis S. Hedling
"""

import numpy as np
import pytest

from src.validators.signal_sanity import (
    ensure_numeric,
    ensure_array,
    ensure_non_negative,
    ensure_norm_domain,
)

from src.validators.altitude_guard import (
    validate_signals,
    validate_congruence,
)

from src.validators.hallucination_guard_bridge import hallucination_guard


# --- Signal Sanity Validator -------------------------------------------------

def test_ensure_numeric_basic():
    assert ensure_numeric("x", 3.14) == 3.14


def test_ensure_numeric_nan():
    with pytest.raises(ValueError):
        ensure_numeric("x", np.nan)


def test_ensure_array_basic():
    arr = ensure_array("v", [1.0, 2.0])
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (2,)


def test_ensure_array_nan():
    with pytest.raises(ValueError):
        ensure_array("v", [np.nan])


def test_ensure_non_negative_basic():
    assert ensure_non_negative("x", 0.5) == 0.5


def test_ensure_non_negative_negative():
    with pytest.raises(ValueError):
        ensure_non_negative("x", -1.0)


def test_ensure_norm_domain_basic():
    arr = np.array([1.0, 2.0])
    norm = ensure_norm_domain("v", arr, max_norm=5.0)
    assert norm == np.linalg.norm(arr)


def test_ensure_norm_domain_exceeds():
    arr = np.array([10.0])
    with pytest.raises(ValueError):
        ensure_norm_domain("v", arr, max_norm=1.0)


# --- Altitude Guard ----------------------------------------------------------

def test_validate_signals_basic():
    signals = {"D": 0.1, "K": 0.2, "C": 0.3, "T": 0.4, "P": 0.5}
    validate_signals(signals)  # should not raise


def test_validate_signals_negative():
    signals = {"D": -0.1, "K": 0.2, "C": 0.3, "T": 0.4, "P": 0.5}
    with pytest.raises(ValueError):
        validate_signals(signals)


def test_validate_congruence_basic():
    congruence = {"valence": 0.5, "arousal": -0.2}
    validate_congruence(congruence)  # should not raise


def test_validate_congruence_out_of_bounds():
    congruence = {"valence": 2.0, "arousal": 0.0}
    with pytest.raises(ValueError):
        validate_congruence(congruence)


# --- Hallucination Guard Bridge ---------------------------------------------

def test_hallucination_guard_stable():
    prev = {"valence": 0.1, "arousal": 0.2}
    curr = {"valence": 0.2, "arousal": 0.3}
    hallucination_guard(curr, prev, max_delta=0.5)  # should not raise


def test_hallucination_guard_jump():
    prev = {"valence": 0.1, "arousal": 0.2}
    curr = {"valence": 0.9, "arousal": 0.2}
    with pytest.raises(ValueError):
        hallucination_guard(curr, prev, max_delta=0.25)


def test_hallucination_guard_missing_keys():
    prev = {"valence": 0.1, "arousal": 0.2}
    curr = {"valence": 0.3}  # missing arousal
    with pytest.raises(ValueError):
        hallucination_guard(curr, prev)
