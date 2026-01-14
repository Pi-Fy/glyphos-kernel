# GlyphOS Physics Kernel v1.0

A deterministic coupling framework decoded from ancient Egyptian sacred mathematical architecture, implementing the closed π–φ–432 relationship and translated to quantum infrastructure.

**Core principle:** Mathematical predictions testable under any ontological interpretation.

## What It Does

MJLOG is a complex-valued coupling matrix:

```
M_ij = log((ν_i/ν_0) · a_j) · exp(i·θ_ij)
```

Where:
- **i** indexes local node tones ν_i (Hz)
- **j** indexes global, dimensionless modulators a_j
- **ν_0** is a reference frequency (Hz) to keep the log argument dimensionless
- **θ_ij** is a phase term (rad), provided by explicit phase model with retarded-time support

This provides a physically-bound coupling kernel for:
- Frequency-geometry relationships based on π–φ–432 harmonics
- Retarded-time phase dynamics
- Harmonic ladder computation using Golden Pi (π_φ = 4/√φ)
- Bridge frequency calculation (838.776 Hz from 432 Hz base)
- Validation framework with falsifiable predictions

**Key Harmonic Frequencies:**
- **11, 22, 33, 44 Hz** - φ-based harmonic markers (implemented as validation gate tiers)
- **432 Hz** - Reference tone anchor
- **838.776 Hz** - Bridge frequency anchor

## Repo Layout
- `src/glyphos_kernel/` - Core kernel implementation
- `tests/` - Pytest validation suite
- `examples/` - Runnable examples with random and Bloom node configurations
- `docs/` - Mathematical specification and validation notes
- `LICENSE` - GlyphOS Kernel License v1.0
- `VERSION` - v1.0.0 release marker

## Quick Start

### Install
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# or: .venv\Scripts\activate  # Windows
pip install -U pip pytest
pip install -e .
```

### Run validation suite
```bash
pytest -v
```

### Basic usage
```python
from glyphos_kernel import golden_pi, bridge_frequency, harmonic_ladder

pi_phi = golden_pi()              # π_φ = 4/√φ ≈ 3.1446
f_b = bridge_frequency()          # 432×(π/φ) ≈ 838.776 Hz
f_10 = harmonic_ladder(432, 1, 0) # harmonic computation
```

### Run examples
```bash
python examples/quickstart_random_nodes.py
python examples/quickstart_bloom_nodes.py
```

## Documentation
- Mathematical specification: `docs/mjlog.md`
- Framework scope: `docs/scope.md`
- Validation approach: `docs/validation.md`
- License details: `LICENSE`

## License
GlyphOS Kernel License v1.0 - Free for research/academic use. Commercial licensing: licensing@glyphos.ai

## Version Policy
v1.0 semantics are immutable. Extensions and modifications require version increment per semantic versioning.

---

**Planned Extensions (separate modules):**
- Quantum interpretive framework
- Gate33 diagnostic system (operator integrity validation)
- Energy applications (ZPE, electrogravitic)
- Biological/medical applications
- Quantum financial systems (QFS)
