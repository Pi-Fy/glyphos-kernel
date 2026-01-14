"""Core implementation for GlyphOS Kernel v1.0 (MJLOG).

Design goals:
- Typed, deterministic math utilities
- No hidden parameters
- Pure functions (easy to test/audit)

Notes:
- Bridge frequency is locked as f_b = 432 * (pi/phi)
- Ladder ratio uses r = pi/pi_phi (dimensionless)
- 432 Hz and 838.776 Hz are provided as canonical anchor constants
- Gate tiers 11/22/33/44 are labels for validation stages (not literal frequencies)
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence, Tuple

# ---- Constants (read-only) ----
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
PI: float = math.pi
C: int = 299_792_458  # m/s

# CODATA (adequate for v1.0; do not change in-place post-tag)
HBAR: float = 1.054_571_817e-34  # J·s
EPS0: float = 8.854_187_8128e-12  # F/m

# ---- Canonical anchors ----
F_432: float = 432.0
F_838_776: float = 838.776  # often rounded as 838.78
ANCHOR_TOL_HZ: float = 1e-3

# ---- Gate tiers (labels) ----
GATE_11: int = 11
GATE_22: int = 22
GATE_33: int = 33
GATE_44: int = 44

def has_anchor(freqs_hz: Sequence[float], target_hz: float, tol_hz: float = ANCHOR_TOL_HZ) -> bool:
    """Return True if target_hz appears in freqs_hz within tolerance."""
    return any(abs(float(f) - float(target_hz)) <= tol_hz for f in freqs_hz)

# ---- Laws ----
def golden_pi(phi: float = PHI) -> float:
    """π_φ = 4 / sqrt(φ)"""
    return 4.0 / math.sqrt(phi)

def bridge_frequency(base_freq_hz: float = F_432, pi: float = PI, phi: float = PHI) -> float:
    """f_b = 432 * (π/φ) [LOCKED in v1.0]"""
    return float(base_freq_hz) * (float(pi) / float(phi))

def harmonic_ladder(f0_hz: float, n: int, m: int, pi: float = PI, phi: float = PHI) -> float:
    """f_(n,m) = f0 * (pi/pi_phi)^n * phi^m"""
    pi_phi = golden_pi(phi)
    r = float(pi) / float(pi_phi)
    return float(f0_hz) * (r ** int(n)) * (float(phi) ** int(m))

# ---- Geometry ----
def control_path_length(R_m: float, H_m: float) -> float:
    """L0 = 2 * sqrt(R^2 + H^2)"""
    return 2.0 * math.sqrt(float(R_m) ** 2 + float(H_m) ** 2)

def effective_path_length(L0_m: float, a_j: float) -> float:
    """L_eff = L0 * a_j"""
    return float(L0_m) * float(a_j)

# ---- MJLOG ----
def mjlog(
    nu_i_hz: Sequence[float],
    a_j: Sequence[float],
    nu0_hz: float = 1.0,
    theta_ij: Sequence[Sequence[float]] | None = None,
) -> List[List[complex]]:
    """M_ij = log((ν_i/ν0) * a_j) * exp(i θ_ij)."""
    nu0_f = float(nu0_hz)
    if not math.isfinite(nu0_f):
        raise ValueError(f"nu0_hz must be finite (got {nu0_hz!r}).")
    if nu0_f <= 0:
        raise ValueError(f"nu0_hz must be > 0 (got {nu0_hz!r}).")

    nu_i = [float(nu) for nu in nu_i_hz]
    a = [float(aj) for aj in a_j]

    for i, nu in enumerate(nu_i):
        if not math.isfinite(nu):
            raise ValueError(f"nu_i_hz[{i}] must be finite (got {nu_i_hz[i]!r}).")
        if nu <= 0:
            raise ValueError(f"nu_i_hz[{i}] must be > 0 (got {nu_i_hz[i]!r}).")

    for j, aj in enumerate(a):
        if not math.isfinite(aj):
            raise ValueError(f"a_j[{j}] must be finite (got {a_j[j]!r}).")
        if aj <= 0:
            raise ValueError(f"a_j[{j}] must be > 0 (got {a_j[j]!r}).")

    if theta_ij is None:
        theta = [[0.0 for _ in a] for _ in nu_i]
    else:
        if len(theta_ij) != len(nu_i):
            raise ValueError(
                f"theta_ij row count must equal len(nu_i_hz) ({len(theta_ij)} != {len(nu_i)})."
            )
        theta = []
        for i, row in enumerate(theta_ij):
            if len(row) != len(a):
                raise ValueError(
                    f"theta_ij[{i}] length must equal len(a_j) ({len(row)} != {len(a)})."
                )
            row_f: List[float] = []
            for j, th in enumerate(row):
                th_f = float(th)
                if not math.isfinite(th_f):
                    raise ValueError(f"theta_ij[{i}][{j}] must be finite (got {th!r}).")
                row_f.append(th_f)
            theta.append(row_f)

    out: List[List[complex]] = []
    for i, nu in enumerate(nu_i):
        row_out: List[complex] = []
        for j, aj in enumerate(a):
            arg = (nu / nu0_f) * aj
            if (not math.isfinite(arg)) or arg <= 0:
                raise ValueError(
                    "MJLOG log-argument must be finite and > 0 "
                    f"(i={i}, j={j}, nu={nu!r}, nu0={nu0_hz!r}, a_j={aj!r}, arg={arg!r})."
                )
            amp = math.log(arg)
            row_out.append(amp * cmath.exp(1j * theta[i][j]))
        out.append(row_out)
    return out

# ---- Gate validators (pure, deterministic) ----
@dataclass(frozen=True)
class GateResult:
    gate_id: str
    eligible: bool
    reason: str
    details: Dict[str, Any]

def _is_pos_finite(x: float) -> bool:
    return math.isfinite(x) and x > 0.0

def gate_11(
    nu_i_hz: Sequence[float],
    a_j: Sequence[float],
    nu0_hz: float = 1.0,
    require_432: bool = False,
    require_838: bool = False,
) -> GateResult:
    nu0_f = float(nu0_hz)
    if not _is_pos_finite(nu0_f):
        return GateResult("GATE11", False, "nu0_hz must be finite and > 0", {"nu0_hz": nu0_hz})
    if len(nu_i_hz) == 0:
        return GateResult("GATE11", False, "nu_i_hz must be non-empty", {})
    if len(a_j) == 0:
        return GateResult("GATE11", False, "a_j must be non-empty", {})
    for i, nu in enumerate(nu_i_hz):
        if not _is_pos_finite(float(nu)):
            return GateResult("GATE11", False, f"nu_i_hz[{i}] must be finite and > 0", {"value": nu})
    for j, aj in enumerate(a_j):
        if not _is_pos_finite(float(aj)):
            return GateResult("GATE11", False, f"a_j[{j}] must be finite and > 0", {"value": aj})

    details = {
        "has_432": has_anchor(nu_i_hz, F_432),
        "has_838_776": has_anchor(nu_i_hz, F_838_776),
    }
    if require_432 and not details["has_432"]:
        return GateResult("GATE11", False, "432 Hz anchor required but missing", details)
    if require_838 and not details["has_838_776"]:
        return GateResult("GATE11", False, "838.776 Hz anchor required but missing", details)
    return GateResult("GATE11", True, "OK", details)

def gate_22(nu_i_hz: Sequence[float], a_j: Sequence[float], nu0_hz: float = 1.0) -> GateResult:
    g11 = gate_11(nu_i_hz, a_j, nu0_hz)
    if not g11.eligible:
        return GateResult("GATE22", False, f"Prereq {g11.gate_id} failed: {g11.reason}", g11.details)

    pi_phi = golden_pi(PHI)
    fb = bridge_frequency(F_432, PI, PHI)
    if not _is_pos_finite(float(pi_phi)) or not _is_pos_finite(float(fb)):
        return GateResult("GATE22", False, "Invariant computation failed", {"pi_phi": pi_phi, "f_bridge": fb})

    return GateResult("GATE22", True, "OK", {"pi_phi": pi_phi, "f_bridge": fb, **g11.details})

def gate_33(nu_i_hz: Sequence[float], a_j: Sequence[float], nu0_hz: float = 1.0) -> GateResult:
    g22 = gate_22(nu_i_hz, a_j, nu0_hz)
    if not g22.eligible:
        return GateResult("GATE33", False, f"Prereq {g22.gate_id} failed: {g22.reason}", g22.details)
    return GateResult("GATE33", True, "OK", {"stamp": "Gate33 active (minimal)", **g22.details})

def gate_44(nu_i_hz: Sequence[float], a_j: Sequence[float], nu0_hz: float = 1.0) -> GateResult:
    g11 = gate_11(nu_i_hz, a_j, nu0_hz, require_432=True, require_838=True)
    if not g11.eligible:
        return GateResult("GATE44", False, f"Prereq {g11.gate_id} failed: {g11.reason}", g11.details)
    g22 = gate_22(nu_i_hz, a_j, nu0_hz)
    if not g22.eligible:
        return GateResult("GATE44", False, f"Prereq {g22.gate_id} failed: {g22.reason}", g22.details)
    return GateResult("GATE44", True, "OK", {"stamp": "Gate44 publish-ready", **g22.details})

# ---- Spectral predictions ----
def peak_frequency_control(n: int, L0_m: float, c_m_per_s: float = float(C)) -> float:
    return ((2 * int(n) + 1) * float(c_m_per_s)) / (2.0 * float(L0_m))

def peak_frequency_phi(n: int, L0_m: float, phi: float = PHI, c_m_per_s: float = float(C)) -> float:
    return ((2 * int(n) + 1) * float(c_m_per_s)) / (2.0 * float(L0_m) * float(phi))

def peak_frequencies(
    L0_m: float,
    n_values: Iterable[int],
    phi: float = PHI,
    c_m_per_s: float = float(C),
) -> Tuple[List[float], List[float]]:
    ctrl = [peak_frequency_control(n, L0_m, c_m_per_s) for n in n_values]
    gr = [peak_frequency_phi(n, L0_m, phi, c_m_per_s) for n in n_values]
    return ctrl, gr
