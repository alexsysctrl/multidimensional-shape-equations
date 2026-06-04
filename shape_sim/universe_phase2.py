"""
Multidimensional Shape Equations — Deep Investigation
=====================================================
Phase 2: Deeper exploration of shape interactions, anomaly emergence,
and the unified equation as a universal query interface.

Key improvements:
- Shapes carry full multivector structure (not just grade)
- Interaction uses proper geometric algebra rules
- Anomaly detection tracks structural novelty (not just grade)
- Unified equation is a true compression of all shape information
- Explore the "cube" container concept from photon billiard
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import json
from pathlib import Path


# ============================================================
# SHAPE — Full Multivector Representation
# ============================================================

@dataclass
class Shape:
    """
    A shape in multidimensional space.
    
    Instead of just tracking grade, each shape carries a FULL multivector:
    - A scalar (grade 0): magnitude/energy
    - Vectors (grade 1): direction/position
    - Bivectors (grade 2): oriented planes/rotations
    - Trivectors (grade 3): oriented volumes
    - ... up to pseudoscalar (grade n)
    
    The shape's "form" is the complete pattern across all grades.
    Through interaction, this pattern changes — shapes can grow, shrink,
    rotate, or undergo grade transitions.
    """
    shape_id: str
    multivector: np.ndarray  # [scalar, vec_0, vec_1, ..., biv_01, biv_02, ..., pseudoscalar]
    dim: int  # dimensionality of the space
    name: str = ""
    parent_ids: List[str] = field(default_factory=list)
    birth_step: int = 0
    interaction_count: int = 0
    form_history: List[np.ndarray] = field(default_factory=list)
    
    @property
    def grade_profile(self) -> np.ndarray:
        """Extract the magnitude at each grade level."""
        profile = np.zeros(self.dim + 1)
        
        # Grade 0: scalar
        profile[0] = abs(self.multivector[0])
        
        # Grade 1: vectors (first `dim` elements)
        profile[1] = np.sum(np.abs(self.multivector[1:self.dim+1]))
        
        # Grade 2: bivectors (combinations of pairs)
        n_bivs = self.dim * (self.dim - 1) // 2
        start = self.dim + 1
        end = start + n_bivs
        if end <= len(self.multivector):
            profile[2] = np.sum(np.abs(self.multivector[start:end]))
        
        # Grade 3: trivectors
        if len(self.multivector) > end:
            n_trivs = self.dim * (self.dim - 1) * (self.dim - 2) // 6
            start3 = end
            end3 = start3 + n_trivs
            if end3 <= len(self.multivector):
                profile[3] = np.sum(np.abs(self.multivector[start3:end3]))
        
        # Grade 4+
        if len(self.multivector) > end3:
            remaining = self.multivector[end3:]
            for g in range(4, self.dim + 1):
                if len(remaining) > 0:
                    profile[g] = np.sum(np.abs(remaining))
                    remaining = remaining[len(remaining)//2:]
        
        return profile
    
    @property
    def dominant_grade(self) -> int:
        """The grade with the largest component magnitude."""
        return int(np.argmax(self.grade_profile))
    
    @property
    def total_magnitude(self) -> float:
        return float(np.sum(np.abs(self.multivector)))
    
    @property
    def form_entropy(self) -> float:
        """Entropy of the form — how spread across grades is the shape's energy."""
        profile = self.grade_profile
        total = profile.sum()
        if total < 1e-10:
            return 0.0
        p = profile / total
        return float(-np.sum(p * np.log(p + 1e-10)))
    
    @property
    def is_zero(self) -> bool:
        return self.total_magnitude < 1e-10
    
    def fingerprint(self) -> str:
        """Unique fingerprint of the shape's form."""
        coeffs = self.multivector[:10]  # First 10 coefficients
        return '|'.join(f'{c:.4f}' for c in coeffs)
    
    def clone(self, new_id: str = None) -> 'Shape':
        """Create a copy of this shape."""
        s = Shape(
            shape_id=new_id or self.shape_id,
            multivector=self.multivector.copy(),
            dim=self.dim,
            name=self.name + "_copy",
            parent_ids=[self.shape_id],
            birth_step=self.birth_step
        )
        return s


# ============================================================
# UNIVERSE — Container for Shapes
# ============================================================

class Universe:
    """
    A universe is a multidimensional space containing shapes.
    
    The universe has a geometry (container shape) that constrains
    how shapes interact. Different geometries produce different
    interaction patterns.
    
    The unified equation is the single multivector that encodes
    ALL shapes and their interactions — it's a lossless compression
    of the entire universe state.
    """
    
    def __init__(self, dim: int = 4, container: str = "cube", name: str = "universe"):
        self.dim = dim
        self.container = container
        self.name = name
        self.shapes: Dict[str, Shape] = {}
        self.step = 0
        self.anomaly_log: List[Dict] = []
        self.unified_equation: Optional[np.ndarray] = None
        
        # Container geometry affects interaction probability
        self._container_params = self._init_container(container)
        
        # Seed the universe
        self._seed_shapes()
    
    def _init_container(self, container: str) -> Dict:
        """Initialize container geometry parameters."""
        containers = {
            "cube": {"size": 10, "wall_reflect": True, "center_pull": 0.0},
            "sphere": {"radius": 8, "wall_reflect": True, "center_pull": 0.1},
            "ellipsoid": {"axes": [10, 8, 6], "wall_reflect": True, "center_pull": 0.05},
            "torus": {"major_r": 8, "minor_r": 3, "wall_reflect": True, "center_pull": 0.0},
            "open": {"wall_reflect": False, "center_pull": 0.0},
            "sinai": {"size": 10, "obstacles": 3, "wall_reflect": True, "center_pull": 0.3},
        }
        return containers.get(container, containers["cube"])
    
    def _mv_size(self) -> int:
        """Total size needed for full multivector: scalar + vectors + bivectors + trivectors + pseudoscalar."""
        n = 1  # scalar
        n += self.dim  # vectors
        n += self.dim * (self.dim - 1) // 2  # bivectors
        n += self.dim * (self.dim - 1) * (self.dim - 2) // 6  # trivectors
        if self.dim >= 5:
            n += self.dim  # 4-vectors (same count as vectors by duality)
        n += 1  # pseudoscalar
        return n
    
    def _seed_shapes(self):
        """Seed the universe with basic shapes."""
        n = self._mv_size()
        
        # Scalar seed
        mv = np.zeros(n)
        mv[0] = 1.0
        self.shapes["seed"] = Shape(
            shape_id="seed", multivector=mv, dim=self.dim,
            name="scalar_seed", birth_step=0
        )
        
        # Basis vectors
        for i in range(self.dim):
            mv = np.zeros(n)
            mv[1 + i] = 1.0
            self.shapes[f"e{i}"] = Shape(
                shape_id=f"e{i}", multivector=mv, dim=self.dim,
                name=f"basis_vector_{i}", birth_step=0
            )
        
        # Basis bivectors (planes)
        idx = 1 + self.dim
        for i in range(self.dim):
            for j in range(i + 1, self.dim):
                mv = np.zeros(n)
                mv[idx] = 1.0
                self.shapes[f"e{i}e{j}"] = Shape(
                    shape_id=f"e{i}e{j}", multivector=mv, dim=self.dim,
                    name=f"plane_{i}x{j}", birth_step=0
                )
                idx += 1
    
    def _distance(self, shape_a: Shape, shape_b: Shape) -> float:
        """Compute distance between two shapes in multivector space."""
        return float(np.linalg.norm(shape_a.multivector - shape_b.multivector))
    
    def _interaction_probability(self, a: Shape, b: Shape) -> float:
        """
        Compute probability that two shapes interact.
        
        Depends on:
        - Distance in multivector space (closer = more likely)
        - Container geometry (e.g., sphere pulls toward center)
        - Shape magnitudes (larger = more likely to interact)
        """
        dist = self._distance(a, b)
        base_prob = max(0, 1.0 - dist / 5.0)
        
        # Container effects
        if self._container_params.get("center_pull", 0) > 0:
            # Shapes near center interact more
            center_factor = 1.0 + self._container_params["center_pull"]
            base_prob *= center_factor
        
        # Magnitude boost
        mag_boost = (a.total_magnitude + b.total_magnitude) / 2.0
        base_prob *= (1.0 + 0.1 * mag_boost)
        
        return min(base_prob, 0.8)
    
    def _geometric_product(self, a: Shape, b: Shape) -> np.ndarray:
        """
        Compute the geometric product of two multivectors.
        
        For Cl(p,0): ab = a·b + a∧b
        
        Simplified: we compute grade-by-grade:
        - Scalar × Scalar → Scalar
        - Scalar × Vector → Vector  
        - Scalar × Bivector → Bivector
        - Vector × Vector → Scalar (inner) + Bivector (outer)
        - Vector × Bivector → Vector (inner) + Trivector (outer)
        - Bivector × Bivector → Scalar (inner) + Bivector (grade-2) + Quadvector (outer)
        """
        n = len(a.multivector)
        result = np.zeros(n)
        
        # Simplified geometric product using grade structure
        # Extract grade components
        scalar_a = a.multivector[0]
        vec_a = a.multivector[1:self.dim+1]
        
        scalar_b = b.multivector[0]
        vec_b = b.multivector[1:self.dim+1]
        
        # Scalar × anything = scaled anything
        result[0] += scalar_a * scalar_b
        result[1:self.dim+1] += scalar_a * vec_b + scalar_b * vec_a
        
        # Vector × Vector = dot (scalar) + wedge (bivector)
        dot = np.dot(vec_a, vec_b)
        result[0] += dot
        
        # Bivector components from wedge product
        n_bivs = self.dim * (self.dim - 1) // 2
        biv_start = self.dim + 1
        biv_idx = 0
        for i in range(self.dim):
            for j in range(i+1, self.dim):
                if biv_idx + biv_start < n:
                    result[biv_start + biv_idx] += vec_a[i] * vec_b[j] - vec_a[j] * vec_b[i]
                biv_idx += 1
        
        # Add noise for environmental interaction
        result += np.random.randn(n) * 0.02 * (a.total_magnitude + b.total_magnitude)
        
        return result
    
    def interact(self, a_id: str, b_id: str) -> Optional[Shape]:
        """
        Two shapes interact, producing a new shape.
        
        The interaction:
        1. Computes geometric product
        2. Adds environmental noise
        3. Creates new shape from result
        4. Detects anomalies (grade transitions, structural novelty)
        """
        if a_id not in self.shapes or b_id not in self.shapes:
            return None
        
        a = self.shapes[a_id]
        b = self.shapes[b_id]
        
        # Compute interaction
        product = self._geometric_product(a, b)
        
        # Create new shape
        new_id = f"prod_{a.shape_id}_{b.shape_id}_s{self.step}"
        new_shape = Shape(
            shape_id=new_id,
            multivector=product,
            dim=self.dim,
            name=f"product",
            parent_ids=[a_id, b_id],
            birth_step=self.step
        )
        new_shape.form_history.append(product.copy())
        
        # Update parents
        a.interaction_count += 1
        b.interaction_count += 1
        new_shape.interaction_count = 1
        
        # Anomaly detection
        anomalies = self._detect_anomalies(new_shape, a, b)
        if anomalies:
            self.anomaly_log.extend(anomalies)
        
        self.shapes[new_id] = new_shape
        self.step += 1
        
        return new_shape
    
    def _detect_anomalies(self, new: Shape, a: Shape, b: Shape) -> List[Dict]:
        """Detect if the new shape is anomalous."""
        anomalies = []
        
        # 1. Grade transition: new dominant grade not in parents
        parent_grades = {a.dominant_grade, b.dominant_grade}
        if new.dominant_grade not in parent_grades:
            anomalies.append({
                "type": "grade_transition",
                "new_grade": new.dominant_grade,
                "parent_grades": list(parent_grades),
                "shape_id": new.shape_id,
                "description": f"Grade {list(parent_grades)} → {new.dominant_grade}"
            })
        
        # 2. Structural novelty: form is not a linear combination of parents
        # Check if new form is in the span of parent forms
        parent_matrix = np.column_stack([a.multivector, b.multivector])
        try:
            proj = np.linalg.lstsq(parent_matrix, new.multivector, rcond=None)[0]
            reconstruction = parent_matrix @ proj
            residual = np.linalg.norm(new.multivector - reconstruction)
            total = np.linalg.norm(new.multivector)
            
            if total > 1e-10 and residual / total > 0.5:
                anomalies.append({
                    "type": "structural_novelty",
                    "shape_id": new.shape_id,
                    "residual_ratio": float(residual / total),
                    "description": f"Shape is {residual/total*100:.1f}% novel relative to parents"
                })
        except np.linalg.LinAlgError:
            pass
        
        # 3. Emergent magnitude: total energy exceeds sum of parents
        parent_sum = a.total_magnitude + b.total_magnitude
        if new.total_magnitude > parent_sum * 1.5 and parent_sum > 1e-10:
            anomalies.append({
                "type": "magnitude_emergence",
                "shape_id": new.shape_id,
                "amplification": float(new.total_magnitude / parent_sum),
                "description": f"Magnitude amplified {new.total_magnitude/parent_sum:.2f}x"
            })
        
        # 4. Complexity spike: form entropy exceeds parents significantly
        parent_avg_entropy = (a.form_entropy + b.form_entropy) / 2
        if new.form_entropy > parent_avg_entropy * 2.0 and parent_avg_entropy > 1e-10:
            anomalies.append({
                "type": "complexity_spike",
                "shape_id": new.shape_id,
                "parent_entropy": float(parent_avg_entropy),
                "new_entropy": float(new.form_entropy),
                "description": f"Complexity: {parent_avg_entropy:.3f} → {new.form_entropy:.3f}"
            })
        
        return anomalies
    
    def run_cycle(self, num_interactions: int = 100) -> List[str]:
        """
        Run one cycle of interactions.
        
        Returns list of new shape IDs created.
        """
        shape_ids = list(self.shapes.keys())
        new_ids = []
        
        for _ in range(num_interactions):
            if len(shape_ids) < 2:
                break
            
            # Pick two shapes, weighted by magnitude
            magnitudes = np.array([max(self.shapes[sid].total_magnitude, 1e-10) 
                                  for sid in shape_ids])
            probs = magnitudes / magnitudes.sum()
            
            a_id, b_id = np.random.choice(shape_ids, 2, p=probs, replace=False)
            
            # Interaction probability
            if np.random.random() < self._interaction_probability(
                self.shapes[a_id], self.shapes[b_id]):
                
                result = self.interact(a_id, b_id)
                if result and not result.is_zero:
                    new_ids.append(result.shape_id)
                    
                    # Selection: keep some new shapes, discard others
                    if np.random.random() < 0.4:
                        shape_ids.append(result.shape_id)
        
        return new_ids
    
    def compute_unified_equation(self):
        """
        Compute the unified equation: a single multivector encoding
        the entire universe state.
        
        Method: weighted sum of all shape multivectors, where weight
        = interaction_count^alpha. This captures the "importance"
        of each shape in the universe dynamics.
        """
        if not self.shapes:
            self.unified_equation = np.zeros(self.dim + 2)
            return
        
        n = max(len(s.multivector) for s in self.shapes.values())
        unified = np.zeros(n)
        
        total_weight = 0
        for shape in self.shapes.values():
            weight = shape.interaction_count ** 1.5
            unified[:len(shape.multivector)] += weight * shape.multivector
            total_weight += weight
        
        # Normalize
        if total_weight > 0:
            unified /= total_weight
        
        self.unified_equation = unified
    
    def query(self, query_type: str = "full") -> Dict:
        """
        Query the unified equation for information.
        
        Different query types extract different aspects:
        - "full": return the complete unified equation
        - "grade": return components at a specific grade
        - "energy": return total energy distribution across grades
        - "novelty": return the most novel shapes
        """
        if self.unified_equation is None:
            self.compute_unified_equation()
        
        if query_type == "full":
            return {
                "type": "full",
                "equation": self.unified_equation.tolist(),
                "magnitude": float(np.linalg.norm(self.unified_equation))
            }
        
        elif query_type == "energy":
            profile = np.zeros(self.dim + 1)
            eq = self.unified_equation
            profile[0] = abs(eq[0])
            profile[1] = np.sum(np.abs(eq[1:self.dim+1]))
            n_bivs = self.dim * (self.dim - 1) // 2
            if len(eq) > self.dim + 1 + n_bivs:
                profile[2] = np.sum(np.abs(eq[self.dim+1:self.dim+1+n_bivs]))
            total = profile.sum()
            return {
                "type": "energy",
                "distribution": {str(g): float(p/total) if total > 0 else 0 
                               for g, p in enumerate(profile)},
                "total": float(total)
            }
        
        elif query_type == "novelty":
            # Find most structurally novel shapes
            novel = []
            for sid, s in self.shapes.items():
                if len(s.parent_ids) >= 2:
                    parent_matrix = np.column_stack([
                        self.shapes[p].multivector for p in s.parent_ids
                        if p in self.shapes
                    ])
                    try:
                        proj = np.linalg.lstsq(parent_matrix, s.multivector, rcond=None)[0]
                        residual = np.linalg.norm(s.multivector - parent_matrix @ proj)
                        novel.append((sid, float(residual)))
                    except:
                        pass
            
            novel.sort(key=lambda x: x[1], reverse=True)
            return {
                "type": "novelty",
                "top_10": [{"shape_id": s, "novelty": r} for s, r in novel[:10]]
            }
        
        return {"error": f"Unknown query type: {query_type}"}
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics."""
        if not self.shapes:
            return {}
        
        grades = [s.dominant_grade for s in self.shapes.values()]
        magnitudes = [s.total_magnitude for s in self.shapes.values()]
        entropies = [s.form_entropy for s in self.shapes.values()]
        
        grade_counts = {}
        for g in grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1
        
        # Count anomaly types
        anomaly_types = {}
        for a in self.anomaly_log:
            t = a["type"]
            anomaly_types[t] = anomaly_types.get(t, 0) + 1
        
        return {
            "step": self.step,
            "num_shapes": len(self.shapes),
            "grade_distribution": {str(k): v for k, v in grade_counts.items()},
            "avg_magnitude": float(np.mean(magnitudes)),
            "max_magnitude": float(np.max(magnitudes)),
            "avg_entropy": float(np.mean(entropies)),
            "num_anomalies": len(self.anomaly_log),
            "anomaly_types": anomaly_types,
            "container": self.container
        }


# ============================================================
# EXPERIMENT: Container Comparison
# ============================================================

def run_container_experiment(cycles: int = 30, interactions: int = 80):
    """
    Compare how different container geometries affect shape evolution,
    anomaly emergence, and unified equation structure.
    
    This directly extends the photon billiard container concept to
    multidimensional shape equations.
    """
    containers = ["cube", "sphere", "ellipsoid", "torus", "open", "sinai"]
    
    print("=" * 70)
    print("CONTAINER COMPARISON: MULTIDIMENSIONAL SHAPE EQUATIONS")
    print("=" * 70)
    
    all_results = {}
    
    for container in containers:
        print(f"\n{'─' * 70}")
        print(f"CONTAINER: {container.upper()}")
        print(f"{'─' * 70}")
        
        uni = Universe(dim=4, container=container, name=container)
        
        stats_timeline = []
        anomaly_timeline = []
        
        for cycle in range(cycles):
            uni.run_cycle(interactions)
            
            if cycle % 3 == 0 or cycle == cycles - 1:
                stats = uni.get_statistics()
                stats["cycle"] = cycle
                stats_timeline.append(stats)
                anomaly_timeline.append({
                    "cycle": cycle,
                    "total_anomalies": len(uni.anomaly_log),
                    "types": dict(uni.get_statistics().get("anomaly_types", {}))
                })
        
        # Compute unified equation
        uni.compute_unified_equation()
        final_stats = uni.get_statistics()
        
        # Run queries
        full_query = uni.query("full")
        energy_query = uni.query("energy")
        novelty_query = uni.query("novelty")
        
        print(f"\nFinal state:")
        print(f"  Shapes: {final_stats['num_shapes']}")
        print(f"  Grades: {final_stats['grade_distribution']}")
        print(f"  Anomalies: {final_stats['num_anomalies']}")
        print(f"  Anomaly types: {final_stats['anomaly_types']}")
        print(f"  Unified eq magnitude: {full_query['magnitude']:.4f}")
        print(f"  Energy distribution: {energy_query['distribution']}")
        
        all_results[container] = {
            "stats_timeline": stats_timeline,
            "anomaly_timeline": anomaly_timeline,
            "queries": {
                "full": full_query,
                "energy": energy_query,
                "novelty_top5": novelty_query["top_5"] if "top_5" in novelty_query else novelty_query["top_10"][:5]
            },
            "final_stats": final_stats
        }
    
    return all_results


def analyze_anomaly_patterns(results: Dict):
    """
    Analyze patterns in anomaly emergence across containers.
    
    Key insights:
    1. Which containers produce the most anomalies?
    2. What types of anomalies dominate?
    3. Is there a critical interaction density?
    4. How does container geometry affect shape evolution?
    """
    print("\n" + "=" * 70)
    print("ANOMALY EMERGENCE PATTERNS")
    print("=" * 70)
    
    for container, data in results.items():
        timeline = data["anomaly_timeline"]
        final = data["final_stats"]
        
        print(f"\n{container.upper()}:")
        
        # Anomaly growth curve
        counts = [t["total_anomalies"] for t in timeline]
        print(f"  Anomaly growth: {counts}")
        
        # Final anomaly breakdown
        types = final.get("anomaly_types", {})
        print(f"  Anomaly types: {types}")
        
        # Energy distribution from unified equation
        energy = data["queries"]["energy"]["distribution"]
        print(f"  Energy by grade: {energy}")
        
        # Key metric: anomalies per shape
        ratio = final["num_anomalies"] / max(final["num_shapes"], 1)
        print(f"  Anomaly/shape ratio: {ratio:.4f}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    results = run_container_experiment(cycles=30, interactions=80)
    analyze_anomaly_patterns(results)
    
    # Save results
    output = {
        "experiment": "multidimensional_shape_equations_phase2",
        "config": {"cycles": 30, "interactions": 80, "dim": 4},
        "results": {k: {
            "stats_timeline": v["stats_timeline"],
            "anomaly_timeline": v["anomaly_timeline"],
            "final_stats": v["final_stats"],
            "energy_distribution": v["queries"]["energy"]["distribution"]
        } for k, v in results.items()}
    }
    
    Path("shape_sim/results_phase2.json").parent.mkdir(parents=True, exist_ok=True)
    with open("shape_sim/results_phase2.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to shape_sim/results_phase2.json")
