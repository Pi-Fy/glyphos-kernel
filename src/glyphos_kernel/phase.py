"""Phase utilities for GlyphOS Kernel v1.0."""

from __future__ import annotations

import math
from typing import List, Sequence

from .core import C

def phase(nu_hz: float, L_eff_m: float, c_m_per_s: float = float(C)) -> float:
    """θ = (2πν/c) * L_eff  mod 2π"""
    theta = (2.0 * math.pi * float(nu_hz) / float(c_m_per_s)) * float(L_eff_m)
    return theta % (2.0 * math.pi)

def phase_matrix(nu_i_hz: Sequence[float], L_eff_j_m: Sequence[float], c_m_per_s: float = float(C)) -> List[List[float]]:
    """θ_ij = (2πν_i/c) * L_eff_j  mod 2π"""
    return [[phase(nu, L_eff, c_m_per_s) for L_eff in L_eff_j_m] for nu in nu_i_hz]

def retarded_delays(X: Sequence[Sequence[float]], x_star: Sequence[float], v: float) -> List[float]:
    """τ_i = ||x_i - x*|| / v."""
    if v <= 0:
        raise ValueError("v must be > 0")
    tau: List[float] = []
    for xi in X:
        if len(xi) != len(x_star):
            raise ValueError("X and x_star must have same dimension")
        d2 = 0.0
        for a, b in zip(xi, x_star):
            d2 += (float(a) - float(b)) ** 2
        tau.append(math.sqrt(d2) / float(v))
    return tau

def retarded_phase_matrix(
    a_j: Sequence[float],
    tau_i: Sequence[float],
    nu0_hz: float,
    t: float = 0.0,
    psi_j: Sequence[float] | None = None,
) -> List[List[float]]:
    """θ_ij(t) = Ω_j (t - τ_i) + ψ_j, with Ω_j = 2π ν0 a_j."""
    K = len(a_j)
    psi = [0.0] * K if psi_j is None else [float(x) for x in psi_j]
    if len(psi) != K:
        raise ValueError("psi_j length must equal len(a_j)")
    Omega = [2.0 * math.pi * float(nu0_hz) * float(aj) for aj in a_j]
    theta: List[List[float]] = []
    for tau in tau_i:
        row = []
        for Om, ps in zip(Omega, psi):
            row.append(Om * (float(t) - float(tau)) + ps)
        theta.append(row)
    return theta
