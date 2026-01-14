"""Validation harness primitives for GlyphOS Kernel v1.0."""

from __future__ import annotations

import math
import cmath
import random
from typing import List, Sequence, Tuple

from .core import mjlog
from .phase import retarded_delays, retarded_phase_matrix

def _wrap_pi(x: float) -> float:
    return (x + math.pi) % (2.0 * math.pi) - math.pi

def phase_gradient_proxy(theta_ij: Sequence[Sequence[float]], X: Sequence[Sequence[float]], edges: Sequence[Tuple[int,int]], j: int) -> float:
    acc = 0.0
    n = 0
    for i, k in edges:
        dist2 = 0.0
        for a, b in zip(X[i], X[k]):
            dist2 += (float(a) - float(b)) ** 2
        dist = math.sqrt(dist2)
        if dist <= 0:
            continue
        dth = _wrap_pi(float(theta_ij[i][j]) - float(theta_ij[k][j]))
        acc += abs(dth) / dist
        n += 1
    return acc / n if n else 0.0

def sample_minors(M: Sequence[Sequence[complex]], n_samples: int = 20000, rng: random.Random | None = None) -> Tuple[List[float], List[float]]:
    if rng is None:
        rng = random.Random(0)
    N = len(M)
    K = len(M[0]) if N else 0
    mags: List[float] = []
    phases: List[float] = []
    for _ in range(n_samples):
        i1, i2 = rng.sample(range(N), 2)
        j1, j2 = rng.sample(range(K), 2)
        d = M[i1][j1]*M[i2][j2] - M[i1][j2]*M[i2][j1]
        mags.append(abs(d))
        phases.append(cmath.phase(d))
    return mags, phases

def mean_resultant_length(phases: Sequence[float]) -> float:
    s = sum(cmath.exp(1j*float(p)) for p in phases)
    return abs(s) / len(phases) if phases else 0.0

def phase_scramble(M: Sequence[Sequence[complex]], rng: random.Random | None = None) -> List[List[complex]]:
    if rng is None:
        rng = random.Random(0)
    out: List[List[complex]] = []
    for row in M:
        out_row: List[complex] = []
        for z in row:
            mag = abs(z)
            ph = rng.uniform(-math.pi, math.pi)
            out_row.append(mag * cmath.exp(1j*ph))
        out.append(out_row)
    return out

def tau_shuffle(tau_i: Sequence[float], rng: random.Random | None = None) -> List[float]:
    if rng is None:
        rng = random.Random(0)
    tau = list(map(float, tau_i))
    rng.shuffle(tau)
    return tau

def build_retarded_mjlog(
    X: Sequence[Sequence[float]],
    nu_i_hz: Sequence[float],
    a_j: Sequence[float],
    nu0_hz: float,
    x_star: Sequence[float],
    v: float,
    t: float = 0.0,
) -> Tuple[List[List[complex]], List[List[float]], List[float]]:
    tau = retarded_delays(X, x_star, v)
    theta = retarded_phase_matrix(a_j=a_j, tau_i=tau, nu0_hz=nu0_hz, t=t)
    M = mjlog(nu_i_hz=nu_i_hz, a_j=a_j, nu0_hz=nu0_hz, theta_ij=theta)
    return M, theta, tau
