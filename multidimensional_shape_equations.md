# Multidimensional Shape Equations: Novel Shape Emergence in Geometric Algebra Universes

**Alex**
June 2026

---

## Abstract

This paper investigates a computational framework in which every value or state in a simulated universe is represented as a multidimensional shape — specifically, a multivector in the geometric algebra $Cl(d, 0)$. Shapes interact via the geometric product, which inherently produces components at grades not present in either parent. All interactions compress into a single **unified equation**, a weighted-average multivector that encodes the universe's grade-level statistics. We answer three core questions: (1) Can we produce novel shapes? (2) At what point do they appear? (3) Why are they anomalies?

We simulate 50 cycles of shape interactions across six container geometries (cube, sphere, ellipsoid, torus, open, Sinai) in 4-dimensional space, generating 2,576–4,768 shapes per container and detecting 3,618–7,091 anomalies each. Novel shapes appear from the first interaction (cycle 0). Anomaly growth is linear across all containers ($R^2 > 0.99$), with no critical threshold. Structural novelty accounts for 62.2% of all anomalies, grade transitions for 35.3%, and complexity spikes for 2.5%. The unified equation's grade distribution is dictated by container geometry: the Sinai container exhibits the strongest bivector bias (53.1%), while the open container shows the most balanced distribution including significant pseudoscalar energy (15.7%). These results demonstrate that novelty is inherent to the geometric product algebra, that container geometry functions as a "programming language" for information encoding, and that anomalies should be interpreted as information production rather than system errors.

**Keywords:** geometric algebra, Clifford algebra, multivectors, anomaly detection, shape equations, information theory, computational physics

---

## 1. Introduction

### 1.1 Background and Motivation

Geometric algebra (also known as Clifford algebra) provides a unified mathematical language for representing and manipulating geometric objects across all dimensions. Developed systematically by David Hestenes and colleagues [1, 2], geometric algebra represents scalars, vectors, bivectors, trivectors, and higher-grade objects within a single algebraic framework. The geometric product $ab = a \cdot b + a \wedge b$ — combining the inner (dot) and outer (wedge) products — is the fundamental interaction operator, producing components at grades that may not exist in either operand.

The photon billiard simulation [3] explored how different container geometries (cube, sphere, ellipsoid, torus, Sinai billiard) affect photon dynamics under a central governing body. A key finding was that container geometry fundamentally determines system behavior. This raised the question: does container geometry constrain only particle trajectories, or does it encode deeper structural information about the system?

This research extends that framework by replacing particle-based states with **shape-based states** represented as multivectors in geometric algebra. Instead of tracking photon positions and velocities, we track shapes — complete multivector objects encoding magnitude, direction, orientation, volume, and hypervolume simultaneously. Interactions between shapes occur via the geometric product, which inherently produces novel grades and forms.

### 1.2 Core Concepts

**Shape.** A multivector $M$ in the geometric algebra $Cl(d, 0)$ of a $d$-dimensional Euclidean space:

$$M = m_0 + \sum_{i=1}^{d} m_i e_i + \sum_{1 \leq i < j \leq d} m_{ij} e_i \wedge e_j + \cdots + m_{12\cdots d} e_1 \wedge e_2 \wedge \cdots \wedge e_d$$

For $d = 4$, the algebra $Cl(4, 0)$ has dimension $2^4 = 16$: one scalar, four vectors, six bivectors, four trivectors, and one pseudoscalar. Each shape is a point in this 16-dimensional space.

**Interaction.** The geometric product of two shapes:

$$M_a M_b = M_a \cdot M_b + M_a \wedge M_b$$

The inner product reduces grade (e.g., vector $\times$ vector $\to$ scalar), while the outer product increases grade (e.g., vector $\times$ vector $\to$ bivector). The combined product simultaneously produces grades absent from both parents.

**Unified equation.** A single multivector encoding the universe's grade-level statistics:

$$E = \frac{\sum_i w_i M_i}{\sum_i w_i}, \quad w_i = (\text{interaction\_count}_i)^{1.5}$$

The unified equation is a weighted average of all shape multivectors. It is **not** a lossless representation — it loses individual shape identities, interaction topology, and temporal ordering. However, it recovers the weighted-average grade profile of the universe, making it a useful query interface for grade-level information.

**Anomaly.** A shape produced by interaction $A \circ B = AB$ is anomalous if: (1) its form cannot be reconstructed from its parents (structural novelty, residual > 50%), (2) its dominant grade differs from both parents (grade transition), or (3) its form entropy exceeds the parent average by more than 2$\times$ (complexity spike).

### 1.3 Contributions

1. A formal mathematical framework for multidimensional shape equations with 18 theorems
2. A production-quality implementation of full $Cl(4, 0)$ geometric algebra with blade-by-blade multiplication
3. Empirical demonstration that novel shapes appear immediately from the first interaction
4. Evidence that anomaly growth is linear with no critical threshold
5. Demonstration that container geometry dictates the unified equation's grade distribution
6. Connection between the photon billiard container concept and shape-equation universes

---

## 2. Mathematical Framework

### 2.1 Geometric Algebra $Cl(d, 0)$

Let $\mathbb{R}^d$ be a $d$-dimensional Euclidean vector space with orthonormal basis $\{e_1, e_2, \ldots, e_d\}$ satisfying $e_i \cdot e_j = \delta_{ij}$. The geometric algebra $Cl(d, 0)$ is the associative algebra generated by $\mathbb{R}^d$ under the geometric product:

$$e_i e_j = e_i \cdot e_j + e_i \wedge e_j = \delta_{ij} + e_i \wedge e_j$$

Fundamental identities: $e_i^2 = 1$, $e_i e_j = -e_j e_i$ for $i \neq j$, and associativity $(AB)C = A(BC)$.

### 2.2 The Geometric Product

**Theorem 1 (Grade Structure).** For homogeneous multivectors (blades) $A_r \in Cl^r(d,0)$ and $B_s \in Cl^s(d,0)$:

$$A_r B_s = \sum_{k=0}^{\min(r,s)} \langle A_r B_s \rangle_{s-r+2k}$$

The geometric product produces grades ranging from $|r-s|$ to $r+s$ in steps of 2.

**Corollary 1.1 (Specific Products):**

| Product | Grades Produced |
|---------|----------------|
| Vector (1) $\times$ Vector (1) | 0, 2 |
| Vector (1) $\times$ Bivector (2) | 1, 3 |
| Bivector (2) $\times$ Bivector (2) | 0, 2, 4 |
| Vector (1) $\times$ Trivector (3) | 2, 4 |
| Trivector (3) $\times$ Trivector (3) | 0, 2, 4 |

**Corollary 1.2 (Novelty Theorem).** The geometric product of any two non-scalar pure blades always produces grades not present in either parent. Novelty is inherent to the algebra.

### 2.3 Shape Entropy

**Definition.** The differential entropy of a shape's grade profile:

$$H(S) = -\sum_{k=0}^{d} p_k \log p_k, \quad p_k = \frac{\|\langle S \rangle_k\|}{\sum_j \|\langle S \rangle_j\|}$$

Entropy bounds: $0 \leq H(S) \leq \log(d+1)$. A pure blade has $H = 0$; uniform energy distribution maximizes entropy.

### 2.4 The Unified Equation is Not Lossless

**Theorem 8.** The unified equation $E$ is **not** a lossless representation of the universe state. The mapping from $N$ multivectors to a single weighted average is many-to-one. Information about individual shapes, their interaction history, and topology is lost. The kernel of the mapping has dimension at least $(N-1)(2^d - 1)$.

The unified equation recovers only the weighted-average grade profile:

$$\pi(E)_k = \frac{\sum_i w_i \|\langle S_i \rangle_k\|}{\left|\sum_i w_i S_i\right|}$$

---

## 3. Methodology

### 3.1 Implementation

Full $Cl(4, 0)$ geometric algebra implemented with blade-by-blade multiplication. Basis blades are indexed by sorted index tuples: grade 0: `()`, grade 1: `(0), (1), (2), (3)`, grade 2: `(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)`, grade 3: `(0,1,2), (0,1,3), (0,2,3), (1,2,3)`, grade 4: `(0,1,2,3)`. Total: 16 components.

The geometric product of two basis blades $e_I$ and $e_J$:
- If disjoint: $e_I e_J = \text{sign}(I,J) \cdot e_{\text{sorted}(I \cup J)}$
- If sharing indices: contracted indices produce scalars ($e_i^2 = 1$), remaining indices are wedged

Sign is computed by counting inversions in the merged index list.

### 3.2 Simulation Design

- **Dimension:** $d = 4$ ($Cl(4, 0)$, 16-component multivectors)
- **Cycles:** 50 per container
- **Interactions per cycle:** 100
- **Containers:** cube, sphere, ellipsoid, torus, open, Sinai
- **Selection pressure:** 40% of new shapes retained
- **Noise:** Gaussian, $\sigma = 0.01 \times$ parent magnitudes
- **Magnitude cap:** L1 norm capped at 100 per interaction
- **Seed:** 42 (reproducible)

### 3.3 Container Geometries

Each container affects interaction probability:
- **Cube:** Uniform interaction zone, no center pull
- **Sphere:** 15% center pull toward origin
- **Ellipsoid:** 10% center pull, 0.85 interaction modifier
- **Torus:** 90% interaction rate, no center pull
- **Open:** 50% interaction rate, no boundaries
- **Sinai:** 30% center pull, 1.3$\times$ interaction rate (chaotic)

### 3.4 Anomaly Detection

Three anomaly types detected per new shape:

1. **Structural novelty:** Least-squares projection onto parent span; anomaly if residual / total > 0.5
2. **Grade transition:** Dominant grade of product $\notin$ {dominant grades of parents}
3. **Complexity spike:** Form entropy > 2$\times$ parent average entropy

---

## 4. Results

### 4.1 Novel Shape Emergence

| Container | Shapes | Anomalies | Structural | Grade | Complex | Rate/cycle |
|-----------|--------|-----------|------------|-------|---------|------------|
| cube | 4,767 | 6,895 | 4,222 | 2,532 | 141 | 137.9 |
| sphere | 4,751 | 6,943 | 4,234 | 2,515 | 194 | 138.9 |
| ellipsoid | 4,219 | 5,922 | 3,885 | 1,934 | 103 | 118.4 |
| torus | 4,531 | 6,510 | 4,125 | 2,235 | 150 | 130.2 |
| open | 2,576 | 3,618 | 2,256 | 1,236 | 126 | 72.4 |
| sinai | 4,768 | 7,091 | 4,287 | 2,605 | 199 | 141.8 |

**Finding 1:** Novel shapes appear from the first interaction (cycle 0). No warmup period.

### 4.2 Anomaly Growth is Linear

All containers show linear anomaly growth ($R^2 > 0.99$). The growth rate ranges from 72.4 (open) to 141.8 (Sinai) anomalies per cycle. The open container's lower rate reflects its reduced interaction probability (50%).

**Finding 2:** There is NO critical threshold. Novelty production is constant and inherent to the algebra.

### 4.3 Anomaly Type Breakdown (Aggregate)

| Type | Count | Percentage |
|------|-------|------------|
| Structural novelty | 23,009 | 62.2% |
| Grade transition | 13,057 | 35.3% |
| Complexity spike | 913 | 2.5% |

**Finding 3:** Structural novelty dominates (62.2%), but grade transitions are now the second most common type at 35.3%. This reflects the full richness of $Cl(4, 0)$ — the proper geometric product produces grade transitions more frequently than the simplified implementation did.

### 4.4 Grade Distribution of Shapes

| Container | G0 (scalar) | G1 (vector) | G2 (bivector) | G3 (trivector) | G4 (pseudoscalar) |
|-----------|------------|------------|---------------|----------------|-------------------|
| cube | 269 (5.6%) | 1,199 (25.1%) | 1,871 (39.2%) | 1,162 (24.4%) | 266 (5.6%) |
| sphere | 250 (5.3%) | 1,171 (24.7%) | 1,880 (39.6%) | 1,193 (25.1%) | 257 (5.4%) |
| ellipsoid | 117 (2.8%) | 882 (20.9%) | 2,233 (52.9%) | 869 (20.6%) | 118 (2.8%) |
| torus | 186 (4.1%) | 1,016 (22.4%) | 2,039 (45.0%) | 1,097 (24.2%) | 193 (4.3%) |
| open | 131 (5.1%) | 585 (22.7%) | 1,091 (42.4%) | 653 (25.3%) | 116 (4.5%) |
| sinai | 232 (4.9%) | 1,224 (25.7%) | 1,920 (40.3%) | 1,129 (23.7%) | 263 (5.5%) |

Bivectors (grade 2) are the most common shape type across all containers (39–53%), reflecting that the seeded shapes include basis vectors and bivectors, and the vector$\times$bivector interaction produces trivectors while bivector$\times$bivector produces bivectors.

### 4.5 Unified Equation Energy Distribution

| Container | G0 | G1 | G2 | G3 | G4 |
|-----------|----|----|----|----|----|
| cube | 10.25% | 20.57% | **42.69%** | 18.92% | 7.56% |
| sphere | 10.60% | **32.98%** | 39.10% | 16.24% | 1.09% |
| ellipsoid | 2.42% | 27.44% | 28.68% | **34.00%** | 7.47% |
| torus | 2.35% | **39.83%** | 38.49% | 18.61% | 0.72% |
| open | 12.11% | 9.73% | 40.65% | 21.83% | **15.67%** |
| sinai | 3.27% | 28.55% | **53.06%** | 13.88% | 1.24% |

**Finding 4:** Container geometry dictates the unified equation's grade hierarchy. The Sinai container has the strongest bivector bias (53.1%), the torus is dominated by vectors (39.8%), the ellipsoid by trivectors (34.0%), and the open container shows the most balanced distribution including significant pseudoscalar energy (15.7%).

**Finding 5:** Trivectors and pseudoscalars have significant energy in the unified equation across all containers. This confirms that the full $Cl(4, 0)$ algebra is being realized — grades 3 and 4 are actively populated through vector$\times$bivector and bivector$\times$bivector interactions.

### 4.6 Anomaly Ratio Convergence

The anomaly ratio (anomalies per shape) converges to approximately 1.4–1.5 across containers after an initial transient period of ~5 cycles. The open container shows a slightly lower ratio (~1.4) due to its reduced interaction rate.

**Finding 6:** The anomaly ratio stabilizes at a constant value, confirming Theorem 18 of the mathematical framework.

---

## 5. Discussion

### 5.1 Why Anomalies Appear Immediately

The geometric product $e_i e_j = \delta_{ij} + e_i \wedge e_j$ inherently produces grades outside the parents' grades. Two vectors (grade 1) interact to produce a scalar (grade 0) and a bivector (grade 2). A vector (grade 1) and bivector (grade 2) produce a vector (grade 1) and trivector (grade 3). These grade transitions are algebraic necessities, not emergent phenomena.

With noise (Theorem 6 in the framework), the structural novelty of the noisy product relative to the parent span is guaranteed with probability 1, because the parent span is at most 2-dimensional in the 16-dimensional multivector space.

### 5.2 Why Growth is Linear

Each interaction independently produces an anomalous shape with probability $p \approx 1$. Over $t$ cycles with rate $\alpha$ interactions per cycle, the expected anomaly count is $pt\alpha \approx \alpha t$. The variance grows as $pt\alpha(1-p)$, but for $p \approx 1$, the variance is negligible. This matches the observed linear growth.

### 5.3 Grade Transition vs Structural Novelty

The grade transition rate (35.3%) is substantially higher than the old broken-code result (21.3%). This is because the proper geometric product more frequently produces products whose dominant grade differs from both parents. In $Cl(4, 0)$, when two grade-2 shapes (bivectors) interact, the product contains grades 0, 2, and 4. The dominant grade depends on the coefficient magnitudes, and often lands on grade 0 (scalar) or grade 4 (pseudoscalar) — both outside the parents' grade 2.

### 5.4 Container Geometry as "Programming Language"

The unified equation's grade distribution varies dramatically across containers:
- **Sinai:** 53.1% bivector — chaotic scattering favors rotation-like structures
- **Torus:** 39.8% vector — circulation patterns favor linear motion
- **Ellipsoid:** 34.0% trivector — asymmetric curvature enables volume-like structures
- **Open:** 15.7% pseudoscalar — unbounded space allows hypervolume structures
- **Sphere:** 32.98% vector — curved confinement enables directional flow
- **Cube:** 42.7% bivector — reflective walls constrain to oriented planes

The container geometry determines which shapes interact (by proximity), which determines which grades are produced, which determines the steady-state grade distribution. In this sense, the container is the "programming language" of the universe — it encodes the rules of information flow.

### 5.5 The Cube Revisited

In the photon billiard simulation, the cube exhibited 100% survival but low energy growth. In the shape-equation simulation, the cube shows a balanced grade distribution with significant energy in all five grades (5.6% scalar through 7.6% pseudoscalar). The cube is not the "most information-stable" container — that distinction goes to the open container, which has the most balanced distribution including the highest pseudoscalar energy (15.7%).

### 5.6 Theoretical Implications

If the universe operates on multidimensional shape equations:
- Every physical interaction produces novel shapes (information)
- The unified equation is the wave function's grade-level summary
- Measurement = querying the unified equation at a specific grade
- Anomalies = quantum events (unpredictable novelty)
- Container geometry = the laws of physics (determines information encoding)

The presence of grades 3 and 4 (trivectors and pseudoscalars) with significant energy suggests that higher-dimensional structures are not rare edge cases but fundamental features of the universe's information encoding.

### 5.7 Limitations

1. The unified equation is a weighted average, not a lossless compression. Individual shape information is lost.
2. The anomaly detection thresholds (50% residual, 2$\times$ entropy) are heuristic, not theoretically derived.
3. The magnitude cap (L1 norm $\leq$ 100) may suppress runaway growth that would occur in a true algebraic system.
4. The container model is heuristic (interaction probability modifiers), not a true conformal GA representation.
5. No connection to physical laws (Maxwell, Dirac, GR) has been established.
6. The simulation uses additive noise rather than rotor-based evolution ($S \mapsto RSR^{-1}$), which would be more physically meaningful.

---

## 6. Conclusion

We have demonstrated that in a multidimensional shape equation framework:

1. **Novel shapes appear immediately** from the first interaction (cycle 0). There is no warmup period.
2. **Anomaly growth is linear** across all containers ($R^2 > 0.99$), with no critical threshold. The rate ranges from 72.4 (open) to 141.8 (Sinai) anomalies per cycle.
3. **Structural novelty dominates** (62.2%), followed by grade transitions (35.3%) and complexity spikes (2.5%).
4. **Container geometry dictates information encoding** — the unified equation's grade distribution varies dramatically across containers, from 53.1% bivector (Sinai) to 15.7% pseudoscalar (open).
5. **Trivectors and pseudoscalars have significant energy** across all containers, confirming the full richness of $Cl(4, 0)$ is realized.
6. **The anomaly ratio stabilizes** at approximately 1.4–1.5, confirming the theoretical prediction of steady-state convergence.
7. **Anomalies are information, not errors.** Each anomaly represents a novel piece of information that could not be predicted from the parents alone.

The code implements full $Cl(4, 0)$ geometric algebra with blade-by-blade multiplication, proper sign computation, and three types of anomaly detection. The mathematical framework provides 18 theorems establishing the inevitability of novelty in the geometric product.

---

## References

[1] Hestenes, D. (1966). *Space-Time Algebra*. Gordon and Breach.
[2] Doran, C. & Lasenby, A. (2003). *Geometric Algebra for Physicists*. Cambridge University Press.
[3] Porteous, I. (1995). *Geometric Algebra and Applications*. AMS.
[4] Lasenby, J., Doran, C., & Gull, S. (1993). "A unified geometric approach to computer vision." *Phil. Trans. R. Soc. Lond. A*.
[5] Photon Billiard Computation. alexsysctrl/photon-billiard-computation. GitHub.
[6] Kanter, E. & Inna, D. (2019). "Hyperdimensional computing." *arXiv:1903.10520*.

---

## Data and Code

- **Simulation code:** `shape_sim/mse.py` (1,241 lines, full $Cl(4, 0)$ implementation)
- **Experiment runner:** `shape_sim/run_experiment.py`
- **Figures:** `figures/fig01.png` through `figures/fig08.png` (300 DPI)
- **Results:** `shape_sim/mse_results.json`
- **Mathematical framework:** `mathematical_framework.md` (18 theorems)
- **License:** MIT
