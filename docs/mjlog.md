# MJLOG Coupling Matrix

## Mathematical Definition

The MJLOG (Modular-Jones-Logarithmic) coupling matrix is defined as:

```
M_ij = log((ν_i/ν_0) · a_j) · exp(i·θ_ij)
```

## Components

### Indices
- **i** - Node index, running over N local node frequencies ν_i (Hz)
- **j** - Modulator index, running over K global dimensionless modulators a_j

### Parameters
- **ν_i** - Local node tone frequencies (Hz), specific to each spatial node
- **a_j** - Global dimensionless modulators (often φ-based ratios like 1.0, φ, φ², etc.)
- **ν_0** - Reference frequency (Hz), typically 432 Hz, ensures log argument is dimensionless
- **θ_ij** - Phase term (radians), encodes geometric and temporal relationships between nodes

## Physical Interpretation

The logarithmic amplitude `log((ν_i/ν_0) · a_j)` represents:
- Frequency ratio scaling between local tone and reference
- Modulation by dimensionless geometric factors
- Natural scale compression via logarithm

The complex phase `exp(i·θ_ij)` encodes:
- Retarded-time effects (light-travel delays)
- Geometric phase relationships
- Interference patterns between nodes

## Dimensional Analysis

The construction ensures dimensional consistency:
- `(ν_i/ν_0)` is dimensionless (Hz/Hz)
- `a_j` is dimensionless by definition
- `log(dimensionless)` yields a dimensionless amplitude
- `θ_ij` must be in radians
- Result: `M_ij` is complex-valued and dimensionless

## Implementation Notes

See `src/glyphos_kernel/core.py::mjlog()` for reference implementation with:
- Input validation (finite, positive frequencies)
- Dimensional consistency checks
- Error handling with informative messages
- Support for explicit phase matrices or default zero phase
