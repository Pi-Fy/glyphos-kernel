# GlyphOS Physics Kernel v1.0

A computational physics framework implementing π–φ–432 harmonic structure for modeling coupled wave-network interactions with explicit phase and geometry binding.

**Core principle:** Falsifiable mathematical predictions testable in physical systems.

[![License](https://img.shields.io/badge/License-GlyphOS_v1.0-blue.svg)](LICENSE)
[![arXiv](https://img.shields.io/badge/arXiv-pending-red.svg)]()

## Overview

GlyphOS Kernel provides a deterministic coupling matrix (MJLOG) for modeling harmonic systems with geometric constraints. The framework incorporates:

- π–φ–432 harmonic relationships
- Retarded-time phase dynamics
- Dimensional consistency throughout
- Falsifiable predictions with statistical controls

## Mathematical Framework

The MJLOG (Modular-Jones-Logarithmic) coupling matrix is defined as:

```
M_ij = log((ν_i/ν_0) · a_j) · exp(i·θ_ij)
```

**Components:**
* **i** - Node index, running over N local frequencies ν_i (Hz)
* **j** - Modulator index, running over K dimensionless modulators a_j  
* **ν_0** - Reference frequency (Hz), typically 432 Hz
* **θ_ij** - Phase term (rad), supports retarded-time geometry

**Key Properties:**
- Dimensionally consistent (log argument dimensionless)
- Complex-valued (amplitude × phase)
- Supports geometric phase relationships
- Incorporates light-travel delays

## Geometric Constants

**Golden Pi (π_φ)**  
Unique bridge between circular and golden ratio geometries:
```
π_φ = 4/√φ ≈ 3.1446
```

**Bridge Frequency**  
Harmonic anchor derived from π_φ:
```
f_b = 432 · (π/φ) ≈ 838.776 Hz
```

**Reference Tone**  
432 Hz (conventional harmonic reference)

**Validation Gates**  
11, 22, 33, 44 Hz (φ-based tier markers for input validation)

These constants are **geometrically derived**, not empirically fitted.

## Installation

### Requirements
- Python 3.8+
- NumPy
- Pytest (for validation suite)

### Install from source

```bash
git clone https://github.com/Pi-Fy/glyphos-kernel.git
cd glyphos-kernel

python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# or: .venv\Scripts\activate  # Windows

pip install -U pip pytest
pip install -e .
```

### Verify installation

```bash
pytest -v
```

All tests should pass. If any fail, please open an issue with system details.

## Quick Start

### Basic usage

```python
from glyphos_kernel import golden_pi, bridge_frequency, harmonic_ladder

# Compute geometric constants
pi_phi = golden_pi()              # π_φ = 4/√φ ≈ 3.1446
f_b = bridge_frequency()          # 838.776 Hz
f_10 = harmonic_ladder(432, 1, 0) # Harmonic computation

print(f"Golden Pi: {pi_phi:.6f}")
print(f"Bridge frequency: {f_b:.3f} Hz")
```

### MJLOG computation

```python
from glyphos_kernel import mjlog
import numpy as np

# Define system
nu_i = [432.0, 440.0, 528.0]  # Node frequencies (Hz)
a_j = [1.0, 1.618, 2.618]      # φ-based modulators
nu0 = 432.0                     # Reference frequency

# Compute coupling matrix
M = mjlog(nu_i, a_j, nu0)

print(f"M shape: {M.shape}")     # (3, 3)
print(f"M dtype: {M.dtype}")     # complex128
```

### With retarded-time phase

```python
from glyphos_kernel.validation import build_retarded_mjlog

# Node positions (2D, in meters)
X = [[0, 0], [1000, 0], [500, 866]]

# Observer position
x_star = [500, 289]

# Speed of light (m/s)
v = 3e8

# Observation time
t = 0.0

# Build MJLOG with retarded phase
M, theta, tau = build_retarded_mjlog(
    X, nu_i, a_j, nu0, x_star, v, t
)

print(f"Phase matrix shape: {theta.shape}")
print(f"Light-travel delays: {tau}")
```

## Validation Framework

The kernel includes falsification tests to distinguish real structure from spurious patterns.

### Core Tests

**1. Phase Gradient Scaling**
```python
from glyphos_kernel.validation import phase_gradient_proxy

# For a fixed geometry, gradients should scale with modulators
G_j = phase_gradient_proxy(theta, a_j)
# G_j ∝ a_j (testable via linear regression)
```

**2. Minor Statistics**
```python
from glyphos_kernel.validation import sample_minors, mean_resultant_length

# Sample random 2×2 minors
mags, phases = sample_minors(M, n_samples=5000)

# Measure phase coherence
R = mean_resultant_length(phases)
print(f"Resultant length: {R:.4f}")  # Expect R > 0.1 for structured data
```

### Fatal Controls

**Phase Scramble** - Destroys phase coherence:
```python
from glyphos_kernel.validation import phase_scramble
import random

M_scrambled = phase_scramble(M, rng=random.Random(42))
_, phases_scr = sample_minors(M_scrambled, n_samples=5000)
R_scr = mean_resultant_length(phases_scr)

# R_scr should drop significantly if structure is real
```

**τ-Shuffle** - Destroys geometric causality:
```python
from glyphos_kernel.validation import tau_shuffle

tau_shuffled = tau_shuffle(tau, rng=random.Random(42))
# Rebuild M with shuffled delays and retest
# Statistics should change if geometry-dependent
```

### Running Examples

```bash
# Quick smoke test with random nodes
python examples/quickstart_random_nodes.py

# Test with predefined Bloom geometry
python examples/quickstart_bloom_nodes.py
```

## Documentation

Detailed documentation in `docs/`:

* **[mjlog.md](docs/mjlog.md)** - Mathematical specification of MJLOG coupling matrix
* **[scope.md](docs/scope.md)** - Framework boundaries and version policy
* **[validation.md](docs/validation.md)** - Validation framework and falsification tests
* **[ONTOLOGY.md](docs/ONTOLOGY.md)** - Ontological status for academic reviewers

## Repository Structure

```
glyphos-kernel/
├── src/glyphos_kernel/      # Core implementation
│   ├── __init__.py          # Public API
│   ├── core.py              # MJLOG computation
│   ├── phase.py             # Phase utilities
│   └── validation.py        # Statistical validation
├── tests/                   # Pytest validation suite
│   ├── test_kernel_vectors.py        # Core constant and ladder regression tests
│   └── test_validation_harness.py    # End-to-end validation & falsification tests
├── examples/                # Runnable demonstrations
│   ├── quickstart_random_nodes.py
│   └── quickstart_bloom_nodes.py
├── docs/                    # Documentation
│   ├── mjlog.md
│   ├── scope.md
│   ├── validation.md
│   └── ONTOLOGY.md
├── LICENSE                  # GlyphOS Kernel License v1.0
├── README.md                # This file
├── CHANGELOG.md             # Version history
├── CITATION.cff             # Citation metadata
├── VERSION                  # Current version (1.0.0)
└── pyproject.toml          # Python package metadata
```

## Testing

### Run full validation suite

```bash
pytest -v
```

### Run specific test modules

```bash
pytest tests/test_core.py -v
pytest tests/test_validation.py -v
```

### Check coverage

```bash
pytest --cov=glyphos_kernel --cov-report=html
```

## Academic Status

**Current State:**
- ✅ Mathematical framework complete and dimensionally consistent
- ✅ Reference implementation with validation harness
- ✅ Falsification tests designed and implemented
- ⏳ Empirical validation pending (framework ready for testing)

**Ontological Category:** Computational physics framework

**Appropriate for:**
- Modeling coupled harmonic systems
- Exploring π–φ geometric relationships
- Testing predictions in physical systems

**Not claiming:**
- Replacement for established physics (QM, GR, thermodynamics)
- Validated applications to specific technologies
- Performance guarantees for commercial use

See [ONTOLOGY.md](docs/ONTOLOGY.md) for detailed ontological status.

## License

**GlyphOS Kernel License v1.0**

Academic and research use: Free with attribution  
Commercial use: Requires licensing agreement

Contact: licensing@glyphos.ai

See [LICENSE](LICENSE) for full terms.

## Version Policy

**Semantic Versioning:**
- v1.0.x - Bug fixes only, no semantic changes
- v1.1+ - New features, backward compatible
- v2.0+ - Breaking changes (if ever needed)

**v1.0 is immutable** - Core semantics frozen to ensure reproducible research.

## Citation

If you use GlyphOS Kernel in academic work, please cite:

```bibtex
@software{glyphos_kernel_2025,
  title = {GlyphOS Physics Kernel},
  version = {1.0.0},
  author = {Richard Place},
  year = {2026},
  url = {https://github.com/Pi-Fy/glyphos-kernel},
  doi = {pending},
  note = {Computational framework for π–φ–432 harmonic systems}
}
```

Machine-readable citation: [CITATION.cff](CITATION.cff)

## Contributions

v1.0 core is **feature-complete** - semantics are frozen.

**Bug reports welcome:**
- Open an issue with minimal reproduction case
- Include system details (OS, Python version, etc.)
- Provide expected vs. actual behavior

**Extensions and applications:**
- Fork the repository for derived work
- Build as separate module/package
- Cite core framework appropriately
- Clearly indicate original vs. derived work

## Future Work

**Extensions planned (separate modules):**
- Biological rhythm modeling (EEG, HRV, circadian systems)
- Acoustic resonance optimization
- Quantum coherence applications (if validated)
- Additional geometric frameworks (beyond π–φ–432)

**Empirical validation priorities:**
- Time-series analysis of candidate systems
- Statistical comparison to null models
- Cross-validation across multiple datasets
- Independent replication studies

**Not planned for core:**
- Device specifications
- Commercial applications
- Metaphysical interpretations
- Historical archaeology

See [scope.md](docs/scope.md) for detailed boundaries.

## Contact

**Technical Support:** [GitHub Issues](https://github.com/Pi-Fy/glyphos-kernel/issues)  
**Academic Inquiries:** [Contact email TBD]  
**Commercial Licensing:** licensing@glyphos.ai  

**Website:** [www.glyphos.ai](https://www.glyphos.ai)

---

## Acknowledgments

Development supported by collaborative AI research partnerships.

Framework motivated by observations of harmonic relationships in natural and engineered systems, with rigorous mathematical formalization and falsification protocols.

## Disclaimer

This framework is provided for research and educational purposes. No claims are made about:
- Performance in commercial applications
- Medical or therapeutic efficacy
- Technological viability
- Metaphysical implications

All applications require independent validation in relevant domains.
