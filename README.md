# Multidimensional Shape Equations

**Novel shape emergence in geometric algebra universes**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

A computational investigation of universes where every value/state is represented as a **multidimensional shape** — a multivector in geometric algebra $Cl(d, 0)$. Shapes interact via the geometric product, inherently producing novel grades and forms. All interactions compress into a single **unified equation** that encodes the universe's grade-level statistics.

**Research paper:** [multidimensional_shape_equations.md](multidimensional_shape_equations.md)

## Key Findings

1. **Novel shapes appear immediately** from the first interaction (cycle 0)
2. **Anomaly growth is linear** ($R^2 > 0.99$) with no critical threshold
3. **Structural novelty dominates** (62.2%), grade transitions (35.3%), complexity spikes (2.5%)
4. **Container geometry dictates information encoding** — the unified equation's grade distribution varies dramatically across geometries
5. **Trivectors and pseudoscalars have significant energy** — confirming the full richness of $Cl(4, 0)$ is realized
6. **Anomalies are information, not errors** — each anomaly represents unpredictable novelty

## Quick Start

```bash
# Run the experiment
python3 shape_sim/run_experiment.py

# Generate figures
python3 shape_sim/figures.py
```

## Structure

```
.
├── multidimensional_shape_equations.md   # Research paper (4,300 words)
├── mathematical_framework.md             # Formal math: 18 theorems
├── shape_sim/
│   ├── mse.py                            # Full Cl(4,0) implementation (1,241 lines)
│   ├── run_experiment.py                 # Experiment runner
│   ├── figures.py                        # 8 publication-quality figures
│   └── mse_results.json                  # Experiment data
├── figures/                              # 8 figures (PNG + PDF, 300 DPI)
│   ├── fig01_anomaly_timeline.png
│   ├── fig02_anomaly_breakdown.png
│   ├── fig03_energy_distribution.png
│   ├── fig04_grade_evolution.png
│   ├── fig05_anomaly_ratio.png
│   ├── fig06_container_radar.png
│   ├── fig07_interaction_diagram.png
│   └── fig08_phase_space.png
└── README.md
```

## Requirements

- Python 3.10+
- numpy
- matplotlib

```bash
pip install numpy matplotlib
```

## Experimental Setup

- **Algebra:** $Cl(4, 0)$ — 16-component multivectors (scalar, 4 vectors, 6 bivectors, 4 trivectors, 1 pseudoscalar)
- **Containers:** cube, sphere, ellipsoid, torus, open, Sinai
- **Cycles:** 50 per container
- **Interactions:** 100 per cycle
- **Selection pressure:** 40% retention
- **Seed:** 42 (reproducible)

## Container Comparison

| Container | Shapes | Anomalies | G2 (bivector) | G4 (pseudo) |
|-----------|--------|-----------|---------------|-------------|
| cube | 4,767 | 6,895 | 42.7% | 7.6% |
| sphere | 4,751 | 6,943 | 39.1% | 1.1% |
| ellipsoid | 4,219 | 5,922 | 28.7% | 7.5% |
| torus | 4,531 | 6,510 | 38.5% | 0.7% |
| open | 2,576 | 3,618 | 40.7% | 15.7% |
| sinai | 4,768 | 7,091 | 53.1% | 1.2% |

## Mathematical Framework

The formal mathematical framework is documented in [`mathematical_framework.md`](mathematical_framework.md), including:

- 18 theorems with proofs
- Full $Cl(d, 0)$ definitions (geometric product, grades, involutions, duality)
- Anomaly theory (structural novelty, grade transition, complexity spike)
- Conformal GA container representation
- The unified equation as a weighted average (not lossless)

## Related Work

- **Photon Billiard Computation** — Container geometry effects on photon dynamics (precursor research)
- **Geometric Algebra** — Hestenes, Doran & Lasenby, Porteous
- **Hyperdimensional Computing** — High-dimensional vector representation

## Citation

```bibtex
@misc{multidimensional_shape_equations,
  title = {Multidimensional Shape Equations: Novel Shape Emergence in Geometric Algebra Universes},
  author = {Alex},
  year = {2026},
  url = {https://github.com/alexsysctrl/multidimensional-shape-equations}
}
```

## License

MIT
