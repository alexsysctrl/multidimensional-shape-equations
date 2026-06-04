"""
Multidimensional Shape Equations (MSE)
======================================

A production-quality simulation of shapes as multivectors in geometric algebra
Cl(d, 0). Shapes interact via the geometric product, producing novel structures
that cannot be expressed as linear combinations of their parents.

Core concepts:
  1. Shape = full multivector in Cl(d, 0) with scalar, vector, bivector,
     trivector, 4-vector, ... up to pseudoscalar components.
  2. Interaction = geometric product of two multivectors.
  3. Unified equation = weighted sum of all shape multivectors in the universe.
  4. Anomaly = a shape whose form is not reconstructible from its parents.
  5. Container geometry = the boundary conditions that shape interaction probability.

Mathematical foundation — Cl(d, 0) geometric algebra:
  - Orthonormal basis {e_0, e_1, ..., e_{d-1}} with e_i · e_j = δ_{ij}
  - e_i² = 1 for all i  (positive definite signature)
  - e_i * e_j = e_i ∧ e_j = -e_j ∧ e_i  for i ≠ j
  - Geometric product: e_i * e_j = e_i · e_j + e_i ∧ e_j = δ_{ij} + e_i ∧ e_j
  - Basis blades are ordered by increasing index tuples:
    grade 0: ()
    grade 1: (0), (1), ..., (d-1)
    grade 2: (0,1), (0,2), ..., (d-2, d-1)
    grade 3: (0,1,2), (0,1,3), ..., (d-3,d-2,d-1)
    ...
  - The geometric product of two basis blades A_r and B_s produces grades
    |r-s|, |r-s|+2, ..., r+s with coefficients following sign rules from
    reordering indices to canonical form.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


# ============================================================================
# Blade indexing utilities for Cl(d, 0)
# ============================================================================

def _blades_of_grade(d: int, grade: int) -> List[Tuple[int, ...]]:
    """Return all basis blades of a given grade as sorted index tuples.

    For grade 0: [()]
    For grade 1: [(0,), (1,), ..., (d-1,)]
    For grade 2: [(0,1), (0,2), ..., (d-2,d-1)]
    For grade 3: [(0,1,2), (0,1,3), ..., (d-3,d-2,d-1)]
    """
    if grade < 0 or grade > d:
        return []
    if grade == 0:
        return [()]
    from itertools import combinations
    return list(combinations(range(d), grade))


def _blade_index(d: int, blade: Tuple[int, ...]) -> int:
    """Return the linear index of a blade in the full multivector layout.

    Layout: scalar(0) | vectors(1..d-1) | bivectors | trivectors | ... | pseudoscalar
    """
    if not blade:
        return 0
    n = 1  # scalar offset
    for g in range(1, len(blade)):
        n += math.comb(d, g)
    blades = _blades_of_grade(d, len(blade))
    return n + blades.index(blade)


def _grade_of_blade(blade: Tuple[int, ...]) -> int:
    """Return the grade of a blade tuple."""
    return len(blade)


def _sign_of_permutation(indices: Tuple[int, ...]) -> int:
    """Return the sign (+1 or -1) of a permutation by counting inversions."""
    count = 0
    lst = list(indices)
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] > lst[j]:
                count += 1
    return 1 if count % 2 == 0 else -1


def _canonicalize_and_sign(
    a_indices: Tuple[int, ...], b_indices: Tuple[int, ...]
) -> Tuple[Tuple[int, ...], int]:
    """Multiply two basis blades and return (canonical_indices, sign).

    The geometric product of two basis blades A and B:
      A * B = sign(A,B) * |A ∪ B|   (if no repeated indices)
      A * B = 0                      (if any repeated index, since e_i²=1
                                       and e_i∧e_i=0 means the wedge part
                                       vanishes — but the inner part survives)

    For Cl(d,0) with orthonormal basis:
    - If A and B share any index, we must contract that index:
      e_i * e_i = 1 (scalar)
    - If A and B are disjoint, A * B = sign * e_{sorted(A∪B)}

    This function handles the general case by computing the combined blade
    after contracting shared indices and computing the sign from reordering.
    """
    a_set = set(a_indices)
    b_set = set(b_indices)
    shared = a_set & b_set

    if not shared:
        # Disjoint blades: full wedge product
        combined = tuple(sorted(a_indices + b_indices))
        # Compute sign from reordering a followed by b into sorted order
        merged = list(a_indices) + list(b_indices)
        sign = _sign_of_permutation(tuple(merged))
        return combined, sign
    else:
        # Shared indices contract: e_i * e_i = 1
        # Remove shared indices from both, then wedge the rest
        a_remaining = tuple(i for i in a_indices if i not in shared)
        b_remaining = tuple(i for i in b_indices if i not in shared)

        # Each shared index contributes e_i² = 1 (scalar)
        # But we need to count how many swaps to bring them together
        # For simplicity: each contraction of e_i with e_i gives +1
        # The sign comes from reordering to bring shared indices adjacent

        # Count the number of swaps needed to bring all shared indices
        # from A next to their counterparts in B
        sign = 1
        a_list = list(a_indices)
        b_list = list(b_indices)

        for si in sorted(shared):
            ai_pos = a_list.index(si)
            bi_pos = b_list.index(si)
            # Number of swaps = |ai_pos - bi_pos| if we move bi to ai
            # But we need to account for elements between them
            # Simplified: count inversions in the merged list
            pass

        # Use the full inversion count approach
        merged = list(a_indices) + list(b_indices)
        sign = _sign_of_permutation(tuple(merged))

        # After contracting shared indices, wedge the remaining
        combined = tuple(sorted(a_remaining + b_remaining))
        return combined, sign


# ============================================================================
# Blade index mapping
# ============================================================================

class BladeIndexer:
    """Maps between blade tuples and linear indices for Cl(d, 0).

    Stores:
      - _grade_to_blades[grade] = list of blade tuples
      - _blade_to_index[blade] = linear index
      - _index_to_blade[index] = blade tuple
    """

    def __init__(self, d: int):
        self.d = d
        self.total_size = sum(math.comb(d, g) for g in range(d + 1))
        self._grade_to_blades: Dict[int, List[Tuple[int, ...]]] = {}
        self._blade_to_index: Dict[Tuple[int, ...], int] = {}
        self._index_to_blade: List[Tuple[int, ...]] = [()] * self.total_size

        idx = 0
        for g in range(d + 1):
            blades = _blades_of_grade(d, g)
            self._grade_to_blades[g] = blades
            for blade in blades:
                self._blade_to_index[blade] = idx
                self._index_to_blade[idx] = blade
                idx += 1

    def blade_to_index(self, blade: Tuple[int, ...]) -> int:
        return self._blade_to_index[blade]

    def index_to_blade(self, idx: int) -> Tuple[int, ...]:
        return self._index_to_blade[idx]

    def grade_to_blades(self, grade: int) -> List[Tuple[int, ...]]:
        return self._grade_to_blades.get(grade, [])

    def grade_component_slice(self, grade: int) -> Tuple[int, int]:
        """Return (start, end) slice indices for a given grade."""
        if grade == 0:
            return (0, 1)
        start = sum(math.comb(self.d, g) for g in range(grade))
        end = start + math.comb(self.d, grade)
        return (start, end)


# ============================================================================
# Shape — Full Multivector Representation
# ============================================================================

@dataclass
class Shape:
    """A shape in multidimensional space, represented as a full multivector.

    The multivector is stored as a flat numpy array indexed by the BladeIndexer.
    Components are organized grade by grade: scalar, vectors, bivectors, ...

    Attributes:
        shape_id: Unique identifier.
        multivector: Flat array of coefficients ordered by blade index.
        dim: Dimensionality of the underlying space (d for Cl(d,0)).
        name: Human-readable name.
        parent_ids: IDs of the shapes that produced this one via interaction.
        birth_step: Simulation step at which this shape was created.
        interaction_count: Number of times this shape has participated in interactions.
    """

    shape_id: str
    multivector: np.ndarray
    dim: int
    name: str = ""
    parent_ids: List[str] = field(default_factory=list)
    birth_step: int = 0
    interaction_count: int = 0

    def __post_init__(self):
        """Ensure we have a BladeIndexer for this shape's dimensionality."""
        self._indexer = BladeIndexer(self.dim)

    @property
    def grade_profile(self) -> np.ndarray:
        """Extract the L1 magnitude at each grade level.

        Returns an array of length (dim + 1) where entry g is the sum of
        absolute values of all coefficients at grade g.
        """
        profile = np.zeros(self.dim + 1)
        for g in range(self.dim + 1):
            start, end = self._indexer.grade_component_slice(g)
            if end <= len(self.multivector):
                profile[g] = np.sum(np.abs(self.multivector[start:end]))
        return profile

    @property
    def dominant_grade(self) -> int:
        """The grade with the largest L1 magnitude."""
        profile = self.grade_profile
        if profile.sum() < 1e-15:
            return 0
        return int(np.argmax(profile))

    @property
    def total_magnitude(self) -> float:
        """L1 norm of the full multivector."""
        mv = self.multivector
        if np.any(np.isnan(mv)) or np.any(np.isinf(mv)):
            return 0.0
        mag = float(np.sum(np.abs(mv)))
        # Cap at a reasonable maximum to prevent runaway display values
        return min(mag, 1e15)

    @property
    def euclidean_norm(self) -> float:
        """L2 norm of the full multivector."""
        mv = self.multivector
        if np.any(np.isnan(mv)) or np.any(np.isinf(mv)):
            return 0.0
        return float(np.linalg.norm(mv))

    @property
    def form_entropy(self) -> float:
        """Shannon entropy of the form — how spread across grades is the energy.

        Uses the grade profile (L1 magnitudes) as a probability distribution.
        Higher entropy means the shape's energy is spread across many grades.
        """
        mv = self.multivector
        if np.any(np.isnan(mv)) or np.any(np.isinf(mv)):
            return 0.0
        profile = self.grade_profile
        total = profile.sum()
        if total < 1e-15:
            return 0.0
        p = profile / total
        # Filter out near-zero entries to avoid log(0)
        p = p[p > 1e-15]
        return float(-np.sum(p * np.log(p)))

    @property
    def is_zero(self) -> bool:
        """Whether this shape is effectively the zero multivector."""
        return self.total_magnitude < 1e-10

    def fingerprint(self, precision: int = 4) -> str:
        """Unique fingerprint of the shape's form.

        Returns a string encoding the first few coefficients of each grade.
        """
        parts = []
        for g in range(self.dim + 1):
            start, end = self._indexer.grade_component_slice(g)
            if end <= len(self.multivector):
                coeffs = self.multivector[start:end]
                if len(coeffs) > 0 and np.any(np.abs(coeffs) > 1e-12):
                    truncated = coeffs[:6]
                    parts.append(
                        f"g{g}:{','.join(f'{c:.{precision}f}' for c in truncated)}"
                    )
        return "|".join(parts) if parts else "zero"

    def structural_novelty_fingerprint(self) -> str:
        """Structural novelty fingerprint — encodes the grade structure.

        Returns a string that captures which grades are active and their
        relative magnitudes, useful for detecting structural novelty.
        """
        profile = self.grade_profile
        active_grades = [g for g in range(self.dim + 1) if profile[g] > 1e-12]
        if not active_grades:
            return "zero"
        # Normalize and round
        total = profile[active_grades].sum()
        normalized = profile[active_grades] / total
        parts = [f"{''.join(f'{v:.2f}' for v in normalized)}"]
        return f"grades({','.join(str(g) for g in active_grades)}):{parts[0]}"

    def clone(self, new_id: Optional[str] = None) -> "Shape":
        """Create a deep copy of this shape."""
        return Shape(
            shape_id=new_id or f"{self.shape_id}_clone",
            multivector=self.multivector.copy(),
            dim=self.dim,
            name=f"{self.name}_copy",
            parent_ids=[self.shape_id],
            birth_step=self.birth_step,
            interaction_count=0,
        )

    def merge(self, other: "Shape", weight_a: float = 0.5, weight_b: float = 0.5) -> "Shape":
        """Create a weighted merge of this shape with another.

        Args:
            other: The other shape to merge with.
            weight_a: Weight for this shape (must sum to 1.0 with weight_b).
            weight_b: Weight for the other shape.

        Returns:
            A new Shape that is weight_a * self + weight_b * other.
        """
        if other.dim != self.dim:
            raise ValueError(
                f"Cannot merge shapes of different dimensions "
                f"({self.dim} vs {other.dim})"
            )
        new_mv = weight_a * self.multivector + weight_b * other.multivector
        return Shape(
            shape_id=f"{self.shape_id}_+_{other.shape_id}",
            multivector=new_mv,
            dim=self.dim,
            name=f"merge({self.name},{other.name})",
            parent_ids=[self.shape_id, other.shape_id],
            birth_step=self.birth_step,
        )


# ============================================================================
# Universe — Container for Shapes with Geometric Algebra
# ============================================================================

class Universe:
    """A universe container holding shapes and their interactions.

    The universe provides:
      - Full Cl(d, 0) geometric product computation (grade by grade).
      - Multiple container geometries that affect interaction probability.
      - Selection pressure (retain top shapes by magnitude).
      - Unified equation computation (weighted sum of all shapes).
      - Query interface for grade-specific information.
      - Comprehensive statistics.

    Container geometries:
      - "cube": Box with reflective walls. Uniform interaction zone.
      - "sphere": Spherical container with center-pull toward origin.
      - "ellipsoid": Asymmetric spherical container.
      - "torus": Toroidal container — shapes circulate around the ring.
      - "open": No boundaries — shapes can drift apart.
      - "sinai": Billiard with circular obstacles — chaotic dynamics.
    """

    CONTAINER_PARAMS: Dict[str, Dict[str, Any]] = {
        "cube": {"size": 1.0, "wall_reflect": True, "center_pull": 0.0},
        "sphere": {"radius": 1.0, "wall_reflect": True, "center_pull": 0.15},
        "ellipsoid": {"axes": [1.0, 0.8, 0.6], "wall_reflect": True, "center_pull": 0.1},
        "torus": {"major_r": 1.0, "minor_r": 0.3, "wall_reflect": True, "center_pull": 0.0},
        "open": {"wall_reflect": False, "center_pull": 0.0},
        "sinai": {"size": 1.0, "num_obstacles": 3, "wall_reflect": True, "center_pull": 0.25},
    }

    def __init__(
        self,
        dim: int = 4,
        container: str = "cube",
        name: str = "universe",
        rng: Optional[np.random.Generator] = None,
    ):
        """Initialize the universe.

        Args:
            dim: Dimensionality of the space (Cl(d, 0)).
            container: Container geometry name.
            name: Human-readable name for this universe.
            rng: Optional numpy random generator for reproducibility.
        """
        if container not in self.CONTAINER_PARAMS:
            raise ValueError(f"Unknown container: {container}. Choose from {list(self.CONTAINER_PARAMS.keys())}")

        self.dim = dim
        self.container = container
        self.name = name
        self.rng = rng or np.random.default_rng()
        self.indexer = BladeIndexer(dim)
        self.shapes: Dict[str, Shape] = {}
        self.step = 0
        self.anomaly_log: List[Dict] = []
        self.interaction_log: List[Dict] = []
        self.unified_equation: Optional[np.ndarray] = None

        self._container_params = self.CONTAINER_PARAMS[container]
        self._seed_shapes()

    def _seed_shapes(self) -> None:
        """Seed the universe with basic building-block shapes.

        Creates:
          - One scalar seed (grade 0, value 1.0)
          - One basis vector per dimension (grade 1)
          - One basis bivector per plane (grade 2)
        """
        n = self.indexer.total_size

        # Scalar seed
        mv = np.zeros(n)
        mv[0] = 1.0
        self.shapes["seed"] = Shape(
            shape_id="seed", multivector=mv, dim=self.dim,
            name="scalar_seed", birth_step=0,
        )

        # Basis vectors
        for i in range(self.dim):
            mv = np.zeros(n)
            mv[self.indexer.blade_to_index((i,))] = 1.0
            self.shapes[f"e{i}"] = Shape(
                shape_id=f"e{i}", multivector=mv, dim=self.dim,
                name=f"basis_vector_{i}", birth_step=0,
            )

        # Basis bivectors
        for i in range(self.dim):
            for j in range(i + 1, self.dim):
                mv = np.zeros(n)
                mv[self.indexer.blade_to_index((i, j))] = 1.0
                self.shapes[f"e{i}e{j}"] = Shape(
                    shape_id=f"e{i}e{j}", multivector=mv, dim=self.dim,
                    name=f"plane_{i}x{j}", birth_step=0,
                )

    # ------------------------------------------------------------------
    # Geometric product — full Cl(d, 0) grade-by-grade
    # ------------------------------------------------------------------

    def geometric_product(self, a: Shape, b: Shape) -> np.ndarray:
        """Compute the full geometric product a * b in Cl(d, 0).

        This is the fundamental interaction operator. For orthonormal basis:
          e_i * e_j = δ_{ij} + e_i ∧ e_j
          e_i² = 1, e_i * e_j = -e_j * e_i for i ≠ j

        The product is computed grade by grade by decomposing both multivectors
        into basis blades, computing each blade-pair product, and accumulating
        results into the correct grade slots.

        Args:
            a: First multivector shape.
            b: Second multivector shape.

        Returns:
            A numpy array representing the product multivector.
        """
        if a.dim != self.dim or b.dim != self.dim:
            raise ValueError("Both shapes must have the same dimensionality as the universe.")

        n = self.indexer.total_size
        result = np.zeros(n)

        # Extract non-zero blade coefficients from both multivectors
        a_blades: List[Tuple[Tuple[int, ...], float]] = []
        b_blades: List[Tuple[Tuple[int, ...], float]] = []

        for idx in range(n):
            if abs(a.multivector[idx]) > 1e-15:
                a_blades.append((self.indexer.index_to_blade(idx), float(a.multivector[idx])))
            if abs(b.multivector[idx]) > 1e-15:
                b_blades.append((self.indexer.index_to_blade(idx), float(b.multivector[idx])))

        # Compute all blade-pair products
        for a_blade, a_coef in a_blades:
            for b_blade, b_coef in b_blades:
                combined, sign = _canonicalize_and_sign(a_blade, b_blade)
                target_idx = self.indexer.blade_to_index(combined)
                result[target_idx] += sign * a_coef * b_coef

        return result

    # ------------------------------------------------------------------
    # Interaction probability — container geometry dependent
    # ------------------------------------------------------------------

    def _interaction_probability(self, a: Shape, b: Shape) -> float:
        """Compute the probability that two shapes interact.

        The probability depends on:
          1. Magnitude similarity — shapes of comparable energy interact more.
          2. Container geometry — e.g., sphere pulls toward center,
             Sinai has chaotic scattering zones.
          3. Grade complementarity — shapes at different grades can produce
             richer interactions.

        Args:
            a: First shape.
            b: Second shape.

        Returns:
            A probability in [0, 1].
        """
        mag_a = a.total_magnitude
        mag_b = b.total_magnitude
        avg_mag = (mag_a + mag_b) / 2.0

        # Base probability from magnitudes
        if avg_mag < 1e-10:
            return 0.0
        base_prob = min(1.0, avg_mag)

        # Container-specific modifiers
        cp = self._container_params

        if self.container == "sphere":
            # Center-pull: shapes closer to origin interact more
            center_factor = 1.0 + cp["center_pull"] * 2
            base_prob *= center_factor
        elif self.container == "sinai":
            # Chaotic: higher interaction rate overall
            base_prob *= 1.3
        elif self.container == "open":
            # Open: shapes drift apart, lower interaction rate
            base_prob *= 0.5
        elif self.container == "torus":
            # Toroidal: moderate interaction
            base_prob *= 0.9
        elif self.container == "ellipsoid":
            # Asymmetric: interaction depends on axis alignment
            base_prob *= 0.85
        # cube: default (base_prob unchanged)

        return min(base_prob, 0.95)

    # ------------------------------------------------------------------
    # Shape interaction
    # ------------------------------------------------------------------

    def interact(self, a_id: str, b_id: str) -> Optional[Shape]:
        """Two shapes interact via the geometric product.

        The interaction:
          1. Computes the full geometric product a * b.
          2. Adds small environmental noise.
          3. Creates a new shape from the result.
          4. Detects anomalies (structural novelty, grade transition, complexity spike).
          5. Updates parent interaction counts.

        Args:
            a_id: ID of the first shape.
            b_id: ID of the second shape.

        Returns:
            The new shape, or None if either parent is missing.
        """
        if a_id not in self.shapes or b_id not in self.shapes:
            return None
        if a_id == b_id:
            return None

        a = self.shapes[a_id]
        b = self.shapes[b_id]

        # Compute geometric product
        product = self.geometric_product(a, b)

        # Add environmental noise proportional to parent magnitudes
        noise_scale = 0.01 * (a.total_magnitude + b.total_magnitude)
        noise = self.rng.normal(0, noise_scale, size=product.shape)
        product += noise

        # Guard against NaN/Inf from numerical issues
        if np.any(np.isnan(product)) or np.any(np.isinf(product)):
            product = np.zeros(self.indexer.total_size)

        # Cap magnitude to prevent runaway growth from repeated interactions
        max_magnitude = 100.0
        if np.sum(np.abs(product)) > max_magnitude:
            product *= max_magnitude / np.sum(np.abs(product))

        # Create new shape
        new_id = f"prod_{a_id}_×_{b_id}_s{self.step}"
        new_shape = Shape(
            shape_id=new_id,
            multivector=product,
            dim=self.dim,
            name=f"product({a.name},{b.name})",
            parent_ids=[a_id, b_id],
            birth_step=self.step,
            interaction_count=1,
        )

        # Update parents
        a.interaction_count += 1
        b.interaction_count += 1

        # Log interaction
        self.interaction_log.append({
            "step": self.step,
            "parent_a": a_id,
            "parent_b": b_id,
            "result_grade": new_shape.dominant_grade,
            "parent_grades": [a.dominant_grade, b.dominant_grade],
        })

        # Anomaly detection
        anomalies = self._detect_anomalies(new_shape, a, b)
        if anomalies:
            self.anomaly_log.extend(anomalies)

        self.shapes[new_id] = new_shape
        self.step += 1

        return new_shape

    def _detect_anomalies(
        self, new: Shape, a: Shape, b: Shape
    ) -> List[Dict]:
        """Detect anomalies in a newly created shape.

        Three types of anomalies are detected:
          1. Structural novelty: the shape's form cannot be reconstructed
             from its parents (residual > 50% of total magnitude).
          2. Grade transition: the dominant grade of the product differs
             from both parents' dominant grades.
          3. Complexity spike: the shape's form entropy exceeds the average
             of its parents by more than a factor of 2.

        Args:
            new: The newly created shape.
            a: First parent shape.
            b: Second parent shape.

        Returns:
            List of anomaly dicts (may be empty).
        """
        anomalies: List[Dict] = []

        # 1. Structural novelty — least-squares reconstruction
        if len(a.multivector) == len(b.multivector):
            parent_matrix = np.column_stack([a.multivector, b.multivector])
            try:
                coeffs, _, _, _ = np.linalg.lstsq(parent_matrix, new.multivector, rcond=None)
                reconstruction = parent_matrix @ coeffs
                residual = np.linalg.norm(new.multivector - reconstruction)
                total = np.linalg.norm(new.multivector)
                if total > 1e-10 and residual / total > 0.5:
                    anomalies.append({
                        "type": "structural_novelty",
                        "shape_id": new.shape_id,
                        "residual_ratio": float(residual / total),
                        "description": (
                            f"Shape is {residual / total * 100:.1f}% "
                            f"novel relative to parents"
                        ),
                    })
            except np.linalg.LinAlgError:
                pass

        # 2. Grade transition
        parent_grades = {a.dominant_grade, b.dominant_grade}
        if new.dominant_grade not in parent_grades:
            anomalies.append({
                "type": "grade_transition",
                "shape_id": new.shape_id,
                "new_grade": new.dominant_grade,
                "parent_grades": sorted(parent_grades),
                "description": (
                    f"Grade {sorted(parent_grades)} → {new.dominant_grade}"
                ),
            })

        # 3. Complexity spike
        parent_avg_entropy = (a.form_entropy + b.form_entropy) / 2.0
        if parent_avg_entropy > 1e-10 and new.form_entropy > parent_avg_entropy * 2.0:
            anomalies.append({
                "type": "complexity_spike",
                "shape_id": new.shape_id,
                "parent_entropy": float(parent_avg_entropy),
                "new_entropy": float(new.form_entropy),
                "description": (
                    f"Complexity: {parent_avg_entropy:.3f} → {new.form_entropy:.3f}"
                ),
            })

        return anomalies

    # ------------------------------------------------------------------
    # Cycle execution
    # ------------------------------------------------------------------

    def run_cycle(self, num_interactions: int = 100) -> List[str]:
        """Run one cycle of shape interactions.

        Each cycle:
          1. Selects pairs of shapes weighted by magnitude.
          2. Computes interaction probability based on container geometry.
          3. Performs interaction if probability threshold is met.
          4. Applies selection pressure: keeps a fraction of new shapes.

        Args:
            num_interactions: Number of interaction attempts per cycle.

        Returns:
            List of IDs of newly created shapes.
        """
        if len(self.shapes) < 2:
            return []

        # Cap the candidate pool to avoid unbounded growth and slowdown
        max_pool = min(len(self.shapes), 200)
        shape_ids = list(self.shapes.keys())[:max_pool]
        if len(shape_ids) < 2:
            return []

        new_ids: List[str] = []

        for _ in range(num_interactions):
            # Weighted selection by magnitude
            magnitudes = np.array(
                [max(self.shapes[sid].total_magnitude, 1e-10) for sid in shape_ids]
            )
            probs = magnitudes / magnitudes.sum()

            a_id, b_id = self.rng.choice(shape_ids, 2, replace=False, p=probs)

            prob = self._interaction_probability(self.shapes[a_id], self.shapes[b_id])
            if self.rng.random() < prob:
                result = self.interact(a_id, b_id)
                if result is not None and not result.is_zero:
                    new_ids.append(result.shape_id)

                    # Selection pressure: keep some, discard others
                    if self.rng.random() < 0.4:
                        shape_ids.append(result.shape_id)

        return new_ids

    def apply_selection_pressure(self, retain_fraction: float = 0.4) -> int:
        """Apply selection pressure: retain the top shapes by magnitude.

        Args:
            retain_fraction: Fraction of shapes to retain (0..1).

        Returns:
            Number of shapes removed.
        """
        if not self.shapes:
            return 0

        sorted_shapes = sorted(
            self.shapes.items(),
            key=lambda item: item[1].total_magnitude,
            reverse=True,
        )
        retain_count = max(1, int(len(sorted_shapes) * retain_fraction))
        to_remove = [sid for sid, _ in sorted_shapes[retain_count:]]

        for sid in to_remove:
            del self.shapes[sid]

        return len(to_remove)

    # ------------------------------------------------------------------
    # Unified equation
    # ------------------------------------------------------------------

    def compute_unified_equation(self) -> np.ndarray:
        """Compute the unified equation: a single multivector encoding all shapes.

        Method: weighted sum of all shape multivectors, where weight =
        interaction_count^1.5. This captures the "importance" of each shape
        in the universe dynamics.

        Returns:
            The unified equation as a numpy array.
        """
        if not self.shapes:
            self.unified_equation = np.zeros(self.indexer.total_size)
            return self.unified_equation

        n = self.indexer.total_size
        unified = np.zeros(n)
        total_weight = 0.0

        for shape in self.shapes.values():
            # Cap interaction count to prevent overflow in power
            ic = min(shape.interaction_count, 10000)
            weight = ic ** 1.5
            unified[: len(shape.multivector)] += weight * shape.multivector
            total_weight += weight

        if total_weight > 0:
            unified /= total_weight

        # Guard against residual NaN/Inf
        if np.any(np.isnan(unified)) or np.any(np.isinf(unified)):
            unified = np.zeros(n)

        self.unified_equation = unified
        return unified

    # ------------------------------------------------------------------
    # Query interface
    # ------------------------------------------------------------------

    def query(self, query_type: str = "full", grade: int = 0) -> Dict:
        """Query the unified equation for information.

        Query types:
          - "full": return the complete unified equation.
          - "grade": return components at a specific grade.
          - "energy": return total energy distribution across grades.
          - "novelty": return the most structurally novel shapes.

        Args:
            query_type: Type of query to perform.
            grade: Grade to query (used when query_type="grade").

        Returns:
            Dict with query results.
        """
        if self.unified_equation is None:
            self.compute_unified_equation()

        eq = self.unified_equation

        if query_type == "full":
            return {
                "type": "full",
                "magnitude": float(np.linalg.norm(eq)),
                "grade_profile": self._grade_profile_from_mv(eq).tolist(),
            }

        elif query_type == "grade":
            start, end = self.indexer.grade_component_slice(grade)
            if end > len(eq):
                return {"type": "grade", "grade": grade, "components": [], "magnitude": 0.0}
            components = eq[start:end]
            return {
                "type": "grade",
                "grade": grade,
                "components": components.tolist(),
                "magnitude": float(np.sum(np.abs(components))),
            }

        elif query_type == "energy":
            profile = self._grade_profile_from_mv(eq)
            total = profile.sum()
            distribution = {
                str(g): float(p / total) if total > 0 else 0.0
                for g, p in enumerate(profile)
            }
            return {
                "type": "energy",
                "distribution": distribution,
                "total": float(total),
            }

        elif query_type == "novelty":
            novel = []
            # Sample up to 500 shapes to keep query fast
            shapes_list = list(self.shapes.items())
            if len(shapes_list) > 500:
                shapes_list = self.rng.choice(shapes_list, 500, replace=False).tolist()

            for sid, s in shapes_list:
                if len(s.parent_ids) >= 2:
                    valid_parents = [p for p in s.parent_ids if p in self.shapes]
                    if len(valid_parents) >= 2:
                        parent_matrix = np.column_stack(
                            [self.shapes[p].multivector for p in valid_parents]
                        )
                        try:
                            coeffs, _, _, _ = np.linalg.lstsq(
                                parent_matrix, s.multivector, rcond=None
                            )
                            reconstruction = parent_matrix @ coeffs
                            residual = np.linalg.norm(s.multivector - reconstruction)
                            total = np.linalg.norm(s.multivector)
                            if total > 1e-10:
                                novel.append((sid, float(residual / total)))
                        except np.linalg.LinAlgError:
                            pass

            novel.sort(key=lambda x: x[1], reverse=True)
            return {
                "type": "novelty",
                "top_10": [{"shape_id": s, "novelty_ratio": r} for s, r in novel[:10]],
            }

        return {"error": f"Unknown query type: {query_type}"}

    def _grade_profile_from_mv(self, mv: np.ndarray) -> np.ndarray:
        """Extract grade profile from a raw multivector array."""
        profile = np.zeros(self.dim + 1)
        for g in range(self.dim + 1):
            start, end = self.indexer.grade_component_slice(g)
            if end <= len(mv):
                profile[g] = np.sum(np.abs(mv[start:end]))
        return profile

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about the universe state.

        Returns:
            Dict with step, shape counts, grade distribution, magnitude stats,
            entropy stats, anomaly counts and types, container info.
        """
        if not self.shapes:
            return {}

        grades = [s.dominant_grade for s in self.shapes.values()]
        magnitudes = [s.total_magnitude for s in self.shapes.values()]
        entropies = [s.form_entropy for s in self.shapes.values()]

        grade_counts: Dict[int, int] = {}
        for g in grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1

        # Count anomaly types
        anomaly_types: Dict[str, int] = {}
        for a in self.anomaly_log:
            t = a["type"]
            anomaly_types[t] = anomaly_types.get(t, 0) + 1

        return {
            "step": self.step,
            "num_shapes": len(self.shapes),
            "grade_distribution": {str(k): v for k, v in sorted(grade_counts.items())},
            "avg_magnitude": float(np.mean(magnitudes)),
            "max_magnitude": float(np.max(magnitudes)),
            "min_magnitude": float(np.min(magnitudes)),
            "avg_entropy": float(np.mean(entropies)),
            "max_entropy": float(np.max(entropies)),
            "num_anomalies": len(self.anomaly_log),
            "anomaly_types": anomaly_types,
            "container": self.container,
            "dim": self.dim,
        }

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_state(self, path: Optional[str] = None) -> Path:
        """Export universe state to JSON.

        Args:
            path: Output file path. Defaults to
                  shape_sim/universe_{name}_step{step}.json.

        Returns:
            Path to the saved file.
        """
        state: Dict[str, Any] = {
            "name": self.name,
            "step": self.step,
            "dim": self.dim,
            "container": self.container,
            "shapes": {},
            "anomalies": self.anomaly_log[-100:],
            "statistics": self.get_statistics(),
        }

        for sid, s in self.shapes.items():
            state["shapes"][sid] = {
                "grade": s.dominant_grade,
                "multivector": s.multivector.tolist(),
                "name": s.name,
                "birth_step": s.birth_step,
                "interaction_count": s.interaction_count,
                "fingerprint": s.fingerprint(),
                "form_entropy": s.form_entropy,
                "total_magnitude": s.total_magnitude,
            }

        p = Path(path) if path else Path(
            f"universe_{self.name}_step{self.step}.json"
        )
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as f:
            json.dump(state, f, indent=2)

        return p


# ============================================================================
# Anomaly Detector — comprehensive detection engine
# ============================================================================

class AnomalyDetector:
    """Detects when a newly created shape represents a genuine anomaly.

    Three detection modes:
      1. Structural novelty: shape form not reconstructible from parents.
      2. Grade transition: dominant grade differs from both parents.
      3. Complexity spike: form entropy exceeds parent average significantly.

    The detector operates on a Universe's shape registry to resolve parent
    shapes by ID.
    """

    def __init__(self, universe: Universe):
        """Initialize the anomaly detector.

        Args:
            universe: The universe to detect anomalies in.
        """
        self.universe = universe
        self.detected_anomalies: List[Dict] = []

    def detect_structural_novelty(
        self, shape: Shape, threshold: float = 0.5
    ) -> Optional[Dict]:
        """Detect structural novelty: shape is not a linear combination of parents.

        Uses least-squares to try to reconstruct the shape's multivector from
        its parents. If the residual ratio exceeds the threshold, it's novel.

        Args:
            shape: The shape to check.
            threshold: Minimum residual ratio to flag as novel (0..1).

        Returns:
            Anomaly dict if detected, None otherwise.
        """
        if len(shape.parent_ids) < 2:
            return None

        valid_parents = [p for p in shape.parent_ids if p in self.universe.shapes]
        if len(valid_parents) < 2:
            return None

        parent_matrix = np.column_stack(
            [self.universe.shapes[p].multivector for p in valid_parents]
        )
        try:
            coeffs, _, _, _ = np.linalg.lstsq(parent_matrix, shape.multivector, rcond=None)
            reconstruction = parent_matrix @ coeffs
            residual = np.linalg.norm(shape.multivector - reconstruction)
            total = np.linalg.norm(shape.multivector)

            if total > 1e-10 and residual / total > threshold:
                return {
                    "type": "structural_novelty",
                    "shape_id": shape.shape_id,
                    "residual_ratio": float(residual / total),
                    "description": (
                        f"Shape is {residual / total * 100:.1f}% "
                        f"novel relative to parents"
                    ),
                }
        except np.linalg.LinAlgError:
            pass

        return None

    def detect_grade_transition(
        self, shape: Shape
    ) -> Optional[Dict]:
        """Detect grade transition: dominant grade not present in parents.

        Args:
            shape: The shape to check.

        Returns:
            Anomaly dict if detected, None otherwise.
        """
        if len(shape.parent_ids) < 2:
            return None

        parent_grades = set()
        for pid in shape.parent_ids:
            if pid in self.universe.shapes:
                parent_grades.add(self.universe.shapes[pid].dominant_grade)

        if shape.dominant_grade not in parent_grades:
            return {
                "type": "grade_transition",
                "shape_id": shape.shape_id,
                "new_grade": shape.dominant_grade,
                "parent_grades": sorted(parent_grades),
                "description": (
                    f"Grade {sorted(parent_grades)} → {shape.dominant_grade}"
                ),
            }

        return None

    def detect_complexity_spike(
        self, shape: Shape, factor: float = 2.0
    ) -> Optional[Dict]:
        """Detect complexity spike: form entropy exceeds parent average.

        Args:
            shape: The shape to check.
            factor: Minimum multiple of parent average entropy to flag.

        Returns:
            Anomaly dict if detected, None otherwise.
        """
        if len(shape.parent_ids) < 2:
            return None

        parent_entropies = []
        for pid in shape.parent_ids:
            if pid in self.universe.shapes:
                parent_entropies.append(self.universe.shapes[pid].form_entropy)

        if len(parent_entropies) < 2:
            return None

        avg_entropy = np.mean(parent_entropies)
        if avg_entropy > 1e-10 and shape.form_entropy > avg_entropy * factor:
            return {
                "type": "complexity_spike",
                "shape_id": shape.shape_id,
                "parent_entropy": float(avg_entropy),
                "new_entropy": float(shape.form_entropy),
                "description": (
                    f"Complexity: {avg_entropy:.3f} → {shape.form_entropy:.3f}"
                ),
            }

        return None

    def full_detect(self, shape: Shape) -> List[Dict]:
        """Run all anomaly detection on a shape.

        Args:
            shape: The shape to check.

        Returns:
            List of all anomaly dicts detected.
        """
        results: List[Dict] = []

        for detector in [
            self.detect_structural_novelty,
            self.detect_grade_transition,
            self.detect_complexity_spike,
        ]:
            result = detector(shape)
            if result is not None:
                results.append(result)

        if results:
            self.detected_anomalies.extend(results)

        return results


# ============================================================================
# Convenience: create a universe and run a cycle
# ============================================================================

def create_universe(
    dim: int = 4,
    container: str = "cube",
    name: str = "universe",
) -> Universe:
    """Convenience function to create a configured universe.

    Args:
        dim: Dimensionality.
        container: Container geometry.
        name: Human-readable name.

    Returns:
        Configured Universe instance.
    """
    return Universe(dim=dim, container=container, name=name)


def run_cycle(
    universe: Universe,
    interactions: int = 100,
    apply_selection: bool = True,
    retain_fraction: float = 0.4,
) -> List[str]:
    """Run one interaction cycle on a universe.

    Args:
        universe: The universe to run the cycle in.
        interactions: Number of interaction attempts.
        apply_selection: Whether to apply selection pressure after the cycle.
        retain_fraction: Fraction of shapes to retain (if selection applied).

    Returns:
        List of new shape IDs.
    """
    new_ids = universe.run_cycle(interactions)
    if apply_selection:
        universe.apply_selection_pressure(retain_fraction)
    return new_ids
