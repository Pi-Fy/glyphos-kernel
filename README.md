# GlyphOS Physics Kernel v1.0

A computational physics framework implementing π–φ–432 geometric constraints for modeling coupled harmonic systems with explicit phase and geometry binding.

**Core principle:** Falsifiable mathematical predictions testable in modeled harmonic systems.

[![License](https://img.shields.io/badge/License-GlyphOS_v1.0-blue.svg)](LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv-pending-red.svg)]()

---

## Overview

GlyphOS Kernel provides a deterministic coupling matrix (MJLOG) for modeling harmonic systems under geometric and temporal constraints. The framework incorporates:

- π–φ–432 geometric relationships
- Retarded-time phase dynamics
- Dimensional consistency throughout
- Built-in falsification controls

The kernel is designed as a **computational physics framework**, not a replacement for established physical theories.

---

## Mathematical Framework

The MJLOG coupling matrix is defined as:

```
M_ij = log((ν_i / ν_0) · a_j) · exp(i · θ_ij)
```

Where:
- ν_i are node frequencies (Hz)
- ν_0 is a reference frequency (Hz)
- a_j are dimensionless modulators
- θ_ij are phase terms (rad), supporting retarded-time geometry

The formulation is dimensionally consistent and computationally tractable.

---

## Geometric Constants

- **Golden Pi:** π_φ = 4 / √φ ≈ 3.1446  
- **Bridge Frequency:** f_b = 432 · (π / φ) ≈ 838.776 Hz  
- **Reference Anchor:** 432 Hz  
- **Validation Gates:** 11 / 22 / 33 / 44 Hz (φ-based tier markers)

All constants are geometrically derived, not empirically fitted.

---

## Installation

### Requirements
- Python 3.8+
- NumPy
- Pytest (for validation)

### Install from source

```bash
git clone https://github.com/Pi-Fy/glyphos-kernel.git
cd glyphos-kernel
pip install -e .
```

### Verify installation

```bash
pytest -v
```

---

## Quick Start

### Compute core constants

```python
from glyphos_kernel.core import golden_pi, bridge_frequency, harmonic_ladder

pi_phi = golden_pi()
f_bridge = bridge_frequency()
f_example = harmonic_ladder(432.0, n=1, k=0)

print(pi_phi)
print(f_bridge)
print(f_example)
```

### Build an MJLOG coupling matrix

```python
from glyphos_kernel.core import mjlog
import numpy as np

nu_i = [432.0, 440.0, 528.0]   # node frequencies (Hz)
a_j = [1.0, 1.618, 2.618]      # dimensionless modulators
nu0 = 432.0

M = mjlog(nu_i, a_j, nu0)

print(M.shape)
print(M.dtype)
```

---

## Retarded-Time Phase Binding

```python
from glyphos_kernel.validation import build_retarded_mjlog

X = [[0, 0], [1000, 0], [500, 866]]   # node positions (meters)
x_star = [500, 289]                  # observer position
v = 3e8                              # propagation speed (m/s)
t = 0.0                              # observation time

M, theta, tau = build_retarded_mjlog(
    X, nu_i, a_j, nu0, x_star, v, t
)

print(theta.shape)
print(tau)
```

---

## Validation Framework

GlyphOS Kernel includes falsification controls to distinguish genuine geometric structure from spurious correlations.

### Minor statistics and phase coherence

```python
from glyphos_kernel.validation import sample_minors, mean_resultant_length

mags, phases = sample_minors(M, n_samples=5000)
R = mean_resultant_length(phases)

print(R)
```

### Phase scramble control

```python
from glyphos_kernel.validation import phase_scramble
import random

M_scrambled = phase_scramble(M, rng=random.Random(42))
_, phases_scr = sample_minors(M_scrambled, n_samples=5000)
R_scr = mean_resultant_length(phases_scr)

print(R_scr)
```

### Retarded-time (τ) shuffle control

```python
from glyphos_kernel.validation import tau_shuffle

tau_shuffled = tau_shuffle(tau)
```

---

## Testing

The repository includes a pytest validation suite.

### Run all tests

```bash
pytest -v
```

### Included test modules

- `tests/test_kernel_vectors.py`  
  Verifies core constants and harmonic ladder behavior.

- `tests/test_validation_harness.py`  
  Exercises end-to-end MJLOG construction and falsification controls.

---

## Repository Structure

```
glyphos-kernel/
├── src/glyphos_kernel/
│   ├── core.py
│   ├── phase.py
│   └── validation.py
├── tests/
│   ├── test_kernel_vectors.py
│   └── test_validation_harness.py
├── docs/
│   ├── mjlog.md
│   ├── scope.md
│   ├── validation.md
│   └── ONTOLOGY.md
├── LICENSE
├── CHANGELOG.md
├── CITATION.cff
├── VERSION
└── README.md
```

---

## Academic Status

- Mathematical framework complete
- Dimensional consistency verified
- Validation harness implemented
- Empirical validation pending

**Primary category:** physics.comp-ph  
**Secondary:** math-ph  
**Tertiary:** cs.MS

---

## License

GlyphOS Kernel License v1.0  
Academic and research use permitted with attribution.  
Commercial use requires licensing.

---

## Citation

See `CITATION.cff` for machine-readable citation metadata.

---

## Disclaimer

This software is provided for research and educational purposes only. No claims are made regarding technological, medical, or commercial applicability.
