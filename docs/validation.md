# Validation Framework

## Overview

GlyphOS Kernel v1.0 includes a validation harness designed to test whether MJLOG produces nontrivial geometric and spectral structure, and to guard against self-deception through statistical controls.

## Core Tests

### 1. Gradient Scaling Law

**Hypothesis:** Phase gradients scale linearly with modulator values φ_j

**Test:** For a fixed geometry and node set:
```
G_j ∝ φ_j
```

Where G_j is the mean gradient magnitude for modulator j.

**Implementation:** `validation.py::phase_gradient_proxy()`

**Success criteria:** Linear relationship holds within numerical precision

---

### 2. Minor Regime Statistics

**Hypothesis:** 2×2 determinant statistics change systematically with spectral densification

**Test:** Sample random 2×2 minors from M_ij and compute:
- Magnitude distribution quantiles (q50, q90, q95, q99)
- Phase resultant length R (coherence measure)

**Implementation:** `validation.py::sample_minors()`, `validation.py::mean_resultant_length()`

**Success criteria:** 
- R and magnitude quantiles change predictably with spectrum density
- Structure collapses under fatal controls (see below)

---

## Fatal Controls (Falsification Tests)

These controls destroy expected structure. If results persist after controls, the model is likely detecting spurious patterns.

### Phase Scramble

**Purpose:** Destroy phase coherence while preserving magnitude structure

**Method:** Randomize all θ_ij values independently

**Implementation:** `validation.py::phase_scramble()`

**Expected result:** Mean resultant length R drops significantly (coherence destroyed)

**Failure mode:** If R remains high, phase structure was accidental

---

### τ-Shuffle

**Purpose:** Destroy geometric causality while preserving frequency structure

**Method:** Randomly permute retarded-time delays τ_i across nodes

**Implementation:** `validation.py::tau_shuffle()`

**Expected result:** Minor statistics and gradients lose geometric dependence

**Failure mode:** If structure persists, it's not actually geometry-dependent

---

## Running Validation Tests

### Quick smoke test (random nodes):
```python
python examples/quickstart_random_nodes.py
```

### Full validation (your geometry):
```python
from glyphos_kernel.validation import build_retarded_mjlog, sample_minors

# Your node coordinates, frequencies, modulators
X = [[lat1, lon1], [lat2, lon2], ...]  # Convert to projected meters
nu_i = [432.0, 440.0, ...]
a_j = [1.0, 1.618, 2.618]

# Build MJLOG with retarded phase
M, theta, tau = build_retarded_mjlog(X, nu_i, a_j, nu0=432.0, x_star=[0,0], v=3e8, t=0.0)

# Sample minors
import random
mags, phases = sample_minors(M, n_samples=5000, rng=random.Random(42))

# Check resultant length
R = mean_resultant_length(phases)
print(f"Resultant length R = {R:.4f}")  # Expect R > 0.1 for structured data
```

### Controls:
```python
from glyphos_kernel.validation import phase_scramble, tau_shuffle

# Phase scramble control
M_scrambled = phase_scramble(M, rng=random.Random(0))
_, phases_scr = sample_minors(M_scrambled, n_samples=5000)
R_scr = mean_resultant_length(phases_scr)
print(f"After phase scramble: R = {R_scr:.4f}")  # Should drop significantly

# τ-shuffle control
tau_shuffled = tau_shuffle(tau, rng=random.Random(0))
# Rebuild M with shuffled delays and retest
```

---

## Interpretation

**Pass criteria:**
- Original data shows nontrivial structure (R > threshold, distinctive minor statistics)
- Phase scramble destroys coherence (R drops)
- τ-shuffle destroys geometry-dependence (statistics change)

**Failure modes:**
- High R persists after controls → spurious pattern detection
- No structure in original data → insufficient signal or wrong parameters
- Structure survives τ-shuffle → not actually geometry-driven

---

## Numerical Precision

- Use `float64` throughout
- Expect invariants (like Golden Pi) to hold within ~1e-12 relative error
- Phase values should be in [0, 2π) after modulo operation
- Validate all inputs (finite, positive frequencies)

See `core.py::mjlog()` for input validation examples.
