# Multidimensional Shape Equations: Novel Shape Emergence in Geometric Algebra Universes

**Research by Alex | June 2026**
*Extends the photon billiard container concept to multidimensional shape-based computation*

---

## Abstract

This research investigates a novel computational framework where every value/state in a universe is represented as a multidimensional shape (multivector in geometric algebra). Shapes interact via the geometric product, changing grade and form. All interactions compress into a single **unified equation** — a multivector that serves as a lossless query interface for the entire universe state. We answer three core questions: (1) Can we produce novel shapes? (2) At what point do they appear? (3) Why are they anomalies?

**Key findings:** Novel shapes appear immediately from the first interaction. There is no critical threshold — novelty is inherent to the geometric product algebra. The unified equation's grade distribution is dictated by the container geometry, making the container the "programming language" of the universe.

---

## 1. Introduction

### 1.1 Background

The photon billiard simulation explored how different container geometries (cube, sphere, ellipsoid, etc.) affect photon dynamics under a central governing body. Key finding: container geometry fundamentally determines system behavior.

This research extends that concept: instead of photons as particles, we represent universe states as **shapes in n-dimensional space**. Each shape is a multivector with components across all grades (scalar, vector, bivector, trivector, etc.).

### 1.2 Core Concepts

**Shape:** A multivector `M = m₀ + m₁e₁ + m₂e₂ + ... + m₁₂e₁∧e₂ + ...` where each coefficient encodes a different dimensional aspect of the state.

**Interaction:** The geometric product `ab = a·b + a∧b` combines two shapes, producing components at grades that may not exist in either parent.

**Unified Equation:** The weighted sum of all shape multivectors in the universe, serving as a lossless compression of the entire universe state.

**Anomaly:** A shape whose form cannot be expressed as a linear combination of its parents (>50% reconstruction residual), or whose dominant grade differs from both parents.

---

## 2. Mathematical Framework

### 2.1 Geometric Algebra Representation

For a d-dimensional space, the geometric algebra Cl(d,0) has dimension 2^d. For d=4:

| Grade | Count | Geometric Meaning |
|-------|-------|-------------------|
| 0 | 1 | Scalar (magnitude/energy) |
| 1 | 4 | Vectors (direction/position) |
| 2 | 6 | Bivectors (oriented planes/rotations) |
| 3 | 4 | Trivectors (oriented volumes) |
| 4 | 1 | Pseudoscalar (oriented hypervolume) |

**Total: 16 components per shape**

### 2.2 The Geometric Product

The fundamental interaction operator:

```
Vector (grade 1) × Vector (grade 1)
  → Scalar (grade 0) [inner: dot product]
  → Bivector (grade 2) [outer: wedge product]

Vector (grade 1) × Bivector (grade 2)
  → Vector (grade 1) [inner: contraction]
  → Trivector (grade 3) [outer: wedge]

Bivector (grade 2) × Bivector (grade 2)
  → Scalar (grade 0) [inner]
  → Bivector (grade 2) [middle]
  → 4-vector (grade 4) [outer]
```

**Key insight:** The geometric product ALWAYS produces grades not present in the parents. This is the source of all novelty.

### 2.3 The Unified Equation

```
E_unified = Σ_i (interaction_count_i)^1.5 × multivector_i / normalization
```

This single multivector encodes the entire universe state. Querying it at specific grades recovers grade-specific information.

---

## 3. Simulation Design

### 3.1 Setup

- **Dimensions tested:** 3, 4, 5, 6
- **Containers:** cube, sphere, ellipsoid, torus, open, Sinai
- **Cycles:** 30 per container
- **Interactions per cycle:** 80
- **Selection pressure:** 40% of new shapes retained (simulates natural selection)

### 3.2 Anomaly Detection

Three types detected:

1. **Structural novelty** (75%): Form cannot be reconstructed from parents (>50% residual)
2. **Grade transition** (21%): Dominant grade differs from both parents
3. **Complexity spike** (4%): Form entropy exceeds parent average by 2×

---

## 4. Results

### 4.1 Novel Shape Emergence

| Container | Shapes | Anomalies | Ratio | First Appearance |
|-----------|--------|-----------|-------|------------------|
| cube | 1,939 | 2,561 | 1.321 | Cycle 0 |
| sphere | 1,945 | 2,586 | 1.330 | Cycle 0 |
| ellipsoid | 1,910 | 2,570 | 1.346 | Cycle 0 |
| torus | 1,952 | 2,606 | 1.335 | Cycle 0 |
| open | 1,965 | 2,610 | 1.328 | Cycle 0 |
| Sinai | 1,934 | 2,554 | 1.321 | Cycle 0 |

**Finding 1:** Novel shapes appear from the FIRST interaction. No warmup period.

### 4.2 Anomaly Growth is Linear

All containers show linear anomaly growth (R² > 0.99):

```
y = 84-87 × cycle + 110-140
```

**Finding 2:** There is NO critical threshold. Novelty production is constant.

### 4.3 Anomaly Type Breakdown (Aggregate)

| Type | Count | Percentage |
|------|-------|------------|
| Structural novelty | 11,546 | 74.6% |
| Grade transition | 3,294 | 21.3% |
| Complexity spike | 647 | 4.2% |

**Finding 3:** Structural novelty dominates. Most anomalies are qualitatively new forms, not just grade shifts.

### 4.4 Unified Equation Energy Distribution

| Container | Scalar | Vector | Bivector | Trivector |
|-----------|--------|--------|----------|-----------|
| cube | 26.7% | **50.2%** | 23.1% | 0.0% |
| sphere | 7.7% | 45.1% | **47.1%** | 0.0% |
| ellipsoid | 7.0% | 27.9% | **65.1%** | 0.0% |
| torus | 6.4% | 39.3% | **54.3%** | 0.0% |
| open | 13.4% | 35.9% | **50.7%** | 0.0% |
| Sinai | 12.7% | **48.5%** | 38.8% | 0.0% |

**Finding 4:** Container geometry DICTATES the grade hierarchy. The cube preserves the most scalar information (27%). The ellipsoid has the strongest bivector bias (65%).

---

## 5. Answers to Core Questions

### Q1: Can we produce a novel shape?

**YES.** Every interaction produces structurally novel shapes. 99% of new shapes cannot be reconstructed from their parents. Novelty is not rare — it's the default state of the system.

### Q2: At what point does it appear?

**Immediately.** From cycle 0, the first interactions produce anomalies. The growth is linear with no acceleration phase. There is no threshold — novelty is inherent to the geometric product algebra.

The stabilization point is at ~5 cycles, where the anomaly ratio (anomalies per new shape) becomes constant at ~1.33.

### Q3: Why is it an anomaly?

Three mechanisms:

1. **Grade creation** (structural novelty): The geometric product creates components at grades not present in parents. Vector×Vector → Scalar+Bivector. The new grades are inherently novel.

2. **Dominant grade shift** (grade transition): The product's largest component may be at a different grade than either parent. Two vectors (grade 1) → product dominated by scalar (grade 0).

3. **Information amplification** (complexity spike): The shape's energy spreads across more grades than expected, representing genuine dimensional expansion.

**Anomalies are not errors — they are information.** Each anomaly represents a novel piece of information that could not be predicted from the parents alone.

---

## 6. Theoretical Implications

### 6.1 The Universe as a Shape Equation System

If the universe operates on multidimensional shape equations:

- **Every physical interaction** produces novel shapes (information)
- **The unified equation** IS the wave function of the universe
- **Measurement** = querying the unified equation at a specific grade
- **Anomalies** = quantum events (unpredictable novelty)
- **Container geometry** = the laws of physics (determines which grades dominate)

### 6.2 The Cube as a Stable Information Container

The cube container has the highest scalar component (27%) among all geometries. In the photon billiard simulation, the cube had 100% survival but low energy growth. Combined, these suggest the cube is a "stable information container" — it preserves low-grade (scalar/fundamental) information while allowing complex shape evolution at higher grades.

### 6.3 Novelty = Information Rate

The anomaly rate (~84 per cycle) IS the information production rate of the universe. In a shape-equation universe, novelty is not a bug — it's the fundamental output.

---

## 7. Connection to Photon Billiard

| Aspect | Photon Billiard | Shape Equations |
|--------|----------------|-----------------|
| Container role | Constrains photon paths | Dictates grade hierarchy |
| Cube behavior | 100% survival, low energy | Highest scalar (27%) |
| Sphere behavior | Best energy (G=333) | Strong bivector (47%) |
| Sinai behavior | Death trap (0% survival) | Moderate anomaly rate |
| Governing body | Central energy source | Not needed — interaction is intrinsic |

The cube's special role carries across both frameworks: it's the most information-stable container.

---

## 8. Conclusion

Multidimensional shape equations provide a framework where:

1. **Shapes are the fundamental units** of universe state
2. **Interaction produces novelty** inherently (via geometric product)
3. **The unified equation is a universal query interface**
4. **Container geometry determines information encoding**
5. **Anomalies are information, not errors**

The cube emerges as a special container — stable, information-preserving, and structurally rich. This connects directly to the photon billiard findings and suggests the cube may be a fundamental "stable state" geometry across different computational frameworks.

---

## Files

- `shape_sim/universe.py` — Phase 1: Basic shape interaction framework
- `shape_sim/universe_phase2.py` — Phase 2: Container comparison with full multivector
- `shape_sim/analysis.py` — Phase 3: Deep analysis and findings
- `shape_sim/results.json` — Phase 1 results
- `shape_sim/results_phase2.json` — Phase 2 results

## Related Work

- Geometric Algebra (Clifford Algebra): Hestenes, Doran
- Conformal Geometric Algebra: Lasenby, Lasenby
- Photon Billiard Computation: alexsysctrl/photon-billiard-computation
- Hyperdimensional Computing: Kanter, Westley

## License

MIT
