"""
A8-CongruenceAdapter — Integration Harness
Author: Borealis S. Hedling
License: MIT

This module provides the public API for the A8-CongruenceAdapter. It ties
together the entire altitude pipeline:

    1. compute raw geometric signals
    2. validate raw inputs (signal sanity)
    3. normalize and bound signals (reinforcement projection)
    4. compute valence/arousal (congruence mapping)
    5. validate altitude invariants (altitude guard)
    6. enforce stability and continuity (hallucination guard)

This harness is intentionally minimal. It does not interpret signals or
modify behavior; it simply orchestrates the A8 pipeline safely.
"""

from typing import Any, Dict

# --- Signal modules ---
from src.signals.spectral_signal import spectral_drift
from src.signals.curvature_signal import dec_curvature
from src.signals.hyperbolic_signal import hyperbolic_contraction
from src.signals.trace_signal import trace_deviation
from src.signals.phase_signal import phase_energy

# --- Validators ---
from src.validators.signal_sanity import (
    ensure_array,
    ensure_numeric,
    ensure_non_negative,
    ensure_norm_domain,
)
from src.validators.altitude_guard import (
    validate_signals,
    validate_congruence,
)
from src.validators.hallucination_guard_bridge import hallucination_guard

# --- Adapter modules ---
from src.adapter.reinforcement_projection import project_signals
from src.adapter.congruence_mapping import project_to_congruence


def run_adapter(
    delta_x: Any,
    gamma,
    holonomy,
    cell: Any,
    v: Any,
    rho: Any,
    z: Any,
    previous_congruence: Dict[str, float] = None,
) -> Dict[str, float]:
    """
    Run the full A8 adapter pipeline.

    Parameters
    ----------
    delta_x : Any
        Input for spectral drift.
    gamma : Callable
        Spectral transform.
    holonomy : Callable
        DEC holonomy operator.
    cell : Any
        Cell for curvature computation.
    v : Any
        Vector for hyperbolic contraction.
    rho : Any
        Matrix-like state for trace deviation.
    z : Any
        Complex-valued signal for phase-energy.
    previous_congruence : dict, optional
        Previous valence/arousal pair for stability checks.

    Returns
    -------
    dict
        {
            "valence": float,
            "arousal": float
        }
    """

    # --- Sanity validation of raw inputs ---
    arr_delta = ensure_array("delta_x", delta_x)
    arr_v = ensure_array("v", v)
    arr_rho = ensure_array("rho", rho)
    arr_z = ensure_array("z", z)

    ensure_non_negative("norm(delta_x)", ensure_norm_domain("delta_x", arr_delta))
    ensure_non_negative("norm(v)", ensure_norm_domain("v", arr_v))
    ensure_non_negative("norm(rho)", ensure_norm_domain("rho", arr_rho))
    ensure_non_negative("norm(z)", ensure_norm_domain("z", arr_z))

    # --- Compute raw geometric signals ---
    D = spectral_drift(delta_x, gamma)
    K = dec_curvature(holonomy, cell)
    C = hyperbolic_contraction(v)
    T = trace_deviation(rho)
    P = phase_energy(z)

    raw_signals = {"D": D, "K": K, "C": C, "T": T, "P": P}

    # --- Validate raw signals ---
    validate_signals(raw_signals)

    # --- Normalize and bound signals ---
    norm = project_signals(D, K, C, T, P)

    # --- Compute congruence mapping ---
    congruence = project_to_congruence(norm)

    # --- Validate congruence output ---
    validate_congruence(congruence)

    # --- Stability guard (if previous exists) ---
    if previous_congruence is not None:
        hallucination_guard(congruence, previous_congruence)

    return congruence
