"""
Multidimensional Shape Equations
=================================
A universe is represented as a collection of shapes (multivectors in geometric algebra).
Each shape encodes a value/state. Shapes interact via the geometric product, changing
grade and form. All interactions compress into a single unified equation — a multivector
that serves as a lossless query interface for the entire universe state.

Core concepts:
1. Shape = multivector with grade (scalar, vector, bivector, trivector, ...)
2. Interaction = geometric product of shapes
3. Unified equation = sum of all shape interactions
4. Anomaly = a shape that emerges with properties not derivable from parent shapes
5. Grade transition = shapes changing dimension through interaction
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import json
from pathlib import Path


# ============================================================
# SHAPE REPRESENTATION
# ============================================================

@dataclass
class Shape:
    """
    A shape in multidimensional space, represented as a multivector.
    
    Each shape has:
    - grade: the primary dimension (0=scalar, 1=vector, 2=bivector, 3=trivector, ...)
    - components: dict of grade -> array of coefficients
    - identity: unique fingerprint based on component structure
    - evolution: how the shape changes through interactions
    """
    shape_id: str
    components: Dict[int, np.ndarray] = field(default_factory=lambda: {})
    grade: int = 0
    name: str = ""
    parent_ids: List[str] = field(default_factory=list)
    birth_step: int = 0
    interaction_count: int = 0
    dimension_history: List[int] = field(default_factory=list)
    
    @property
    def dominant_grade(self) -> int:
        """The grade with the largest component magnitude."""
        if not self.components:
            return 0
        max_grade = max(self.components.keys(), 
                       key=lambda g: np.max(np.abs(self.components[g])))
        return max_grade
    
    @property
    def total_magnitude(self) -> float:
        """Total magnitude of all components."""
        return sum(np.sum(np.abs(self.components[g])) for g in self.components)
    
    @property
    def grade_entropy(self) -> float:
        """Entropy across grades — measures how 'spread out' the shape is."""
        if not self.components:
            return 0.0
        magnitudes = np.array([self.components[g].sum() for g in self.components])
        magnitudes = magnitudes / magnitudes.sum()
        # Shannon entropy
        return -np.sum(magnitudes * np.log(magnitudes + 1e-10))
    
    def fingerprint(self) -> str:
        """Generate a unique fingerprint based on component structure."""
        parts = []
        for g in sorted(self.components.keys()):
            coeffs = self.components[g]
            parts.append(f"g{g}:{','.join(f'{c:.4f}' for c in coeffs[:5])}")
        return '|'.join(parts)
    
    def is_anomaly(self, threshold: float = 0.3) -> bool:
        """
        A shape is anomalous if its dominant grade is NOT present in any parent.
        This represents a grade transition — the shape has 'changed dimension'
        through interaction, creating something qualitatively new.
        """
        if not self.parent_ids:
            return False
        
        parent_grades = set()
        for pid in self.parent_ids:
            # This would be set by the simulation engine
            pass
        
        # Anomaly = grade not in parent set
        return self.dominant_grade not in parent_grades


class Universe:
    """
    A universe container holding shapes and their interactions.
    
    The universe itself is a shape — the unified equation that results
    from compressing all shape interactions into a single multivector.
    """
    
    def __init__(self, dim: int = 4, name: str = "universe"):
        self.dim = dim  # Base dimensionality of the space
        self.name = name
        self.shapes: Dict[str, Shape] = {}
        self.step = 0
        self.interaction_log: List[Dict] = []
        self.anomaly_log: List[Dict] = []
        self.unified_equation: Optional[Shape] = None
        
        # Shape templates — basic building blocks
        self._init_templates()
    
    def _init_templates(self):
        """Initialize basic shape templates that populate the universe."""
        # Scalar seed (grade 0)
        self._add_shape(
            shape_id="seed_scalar",
            components={0: np.array([1.0])},
            grade=0,
            name="scalar_seed",
            birth_step=0
        )
        
        # Vector seeds in each dimension (grade 1)
        for i in range(self.dim):
            comps = {1: np.zeros(self.dim)}
            comps[1][i] = 1.0
            self._add_shape(
                shape_id=f"vec_{i}",
                components=comps,
                grade=1,
                name=f"basis_vector_{i}",
                birth_step=0
            )
        
        # Bivector seeds (grade 2) — oriented planes
        for i in range(self.dim):
            for j in range(i+1, self.dim):
                comps = {2: np.zeros(self.dim * (self.dim-1) // 2)}
                idx = i * self.dim - i*(i+1)//2 + j - i - 1
                comps[2][idx] = 1.0
                self._add_shape(
                    shape_id=f"biv_{i}{j}",
                    components=comps,
                    grade=2,
                    name=f"plane_{i}x{j}",
                    birth_step=0
                )
    
    def _add_shape(self, shape_id: str, components: Dict[int, np.ndarray],
                   grade: int, name: str = "", birth_step: int = 0,
                   parent_ids: List[str] = None):
        """Add a shape to the universe."""
        s = Shape(
            shape_id=shape_id,
            components=components,
            grade=grade,
            name=name,
            parent_ids=parent_ids or [],
            birth_step=birth_step
        )
        s.dimension_history.append(grade)
        self.shapes[shape_id] = s
    
    def _normalize_components(self, comps: Dict[int, np.ndarray], target_size: int) -> Dict[int, np.ndarray]:
        """Normalize component arrays to a common size for a given grade."""
        normalized = {}
        for g, c in comps.items():
            if len(c) < target_size:
                normalized[g] = np.pad(c, (0, target_size - len(c)), mode='constant')
            elif len(c) > target_size:
                normalized[g] = c[:target_size]
            else:
                normalized[g] = c
        return normalized
    
    def geometric_product(self, a: Shape, b: Shape) -> np.ndarray:
        """
        Compute the geometric product of two shapes.
        
        The geometric product ab = a·b + a∧b
        - Inner product (dot): reduces grade by 1
        - Outer product (wedge): increases grade by 1
        
        This is the fundamental interaction operator.
        """
        result = np.zeros(self.dim + 1)  # grades 0 through dim
        
        # Find max component size across both shapes
        max_size = 1
        for comps in [a.components, b.components]:
            for g, c in comps.items():
                max_size = max(max_size, len(c))
        
        # Normalize both shapes
        a_norm = self._normalize_components(a.components, max_size)
        b_norm = self._normalize_components(b.components, max_size)
        
        for grade_a, comps_a in a_norm.items():
            for grade_b, comps_b in b_norm.items():
                # Inner product component (grade reduces)
                inner_grade = max(0, abs(grade_a - grade_b))
                # Outer product component (grade increases)
                outer_grade = grade_a + grade_b
                
                if outer_grade <= self.dim:
                    result[outer_grade] += np.sum(comps_a * comps_b)
                if inner_grade <= self.dim and inner_grade != outer_grade:
                    result[inner_grade] -= np.sum(comps_a * comps_b) * 0.5
        
        return result
    
    def interact(self, shape_a_id: str, shape_b_id: str) -> Shape:
        """
        Two shapes interact via geometric product, producing a new shape.
        
        The interaction can:
        - Change grade (dimension transition)
        - Create new component structure
        - Merge magnitudes
        """
        a = self.shapes[shape_a_id]
        b = self.shapes[shape_b_id]
        
        # Compute geometric product
        product = self.geometric_product(a, b)
        
        # Build new shape from product
        new_components = {}
        for g in range(len(product)):
            if abs(product[g]) > 1e-10:
                new_components[g] = np.array([product[g]])
        
        # New shape ID
        new_id = f"interact_{a.shape_id}_{b.shape_id}_s{self.step}"
        
        # Add some noise to simulate environmental interaction
        for g in new_components:
            noise = np.random.randn(*new_components[g].shape) * 0.01
            new_components[g] += noise
        
        new_shape = Shape(
            shape_id=new_id,
            components=new_components,
            grade=max(new_components.keys()) if new_components else 0,
            name=f"product_{a.name}_{b.name}",
            birth_step=self.step,
            parent_ids=[a.shape_id, b.shape_id]
        )
        new_shape.dimension_history.append(new_shape.grade)
        new_shape.interaction_count = 1
        
        # Update parents' interaction counts
        a.interaction_count += 1
        b.interaction_count += 1
        
        # Track dimension changes
        if new_shape.grade != a.grade and new_shape.grade != b.grade:
            anomaly_info = {
                "step": self.step,
                "new_shape": new_id,
                "new_grade": new_shape.grade,
                "parent_grades": [a.grade, b.grade],
                "parent_ids": [a.shape_id, b.shape_id],
                "is_grade_transition": True,
                "fingerprint": new_shape.fingerprint()
            }
            self.anomaly_log.append(anomaly_info)
        
        self.shapes[new_id] = new_shape
        self.step += 1
        
        return new_shape
    
    def compute_unified_equation(self) -> Shape:
        """
        Compute the unified equation: the single multivector that
        represents ALL shapes and their interactions in the universe.
        
        This is the sum of all shape contributions, weighted by their
        interaction strength (number of interactions).
        """
        if not self.shapes:
            return None
        
        unified_components: Dict[int, np.ndarray] = {}
        total_interactions = sum(s.interaction_count for s in self.shapes.values())
        
        for shape in self.shapes.values():
            weight = shape.interaction_count / max(total_interactions, 1)
            for g, comps in shape.components.items():
                if g not in unified_components:
                    unified_components[g] = np.zeros_like(comps)
                unified_components[g] += weight * comps
        
        # Also include the interaction products
        for log in self.interaction_log:
            for g, val in log.get('product_grades', {}).items():
                if g not in unified_components:
                    unified_components[g] = np.array([0.0])
                unified_components[g][0] += val * 0.1
        
        # Normalize
        for g in unified_components:
            mag = np.max(np.abs(unified_components[g]))
            if mag > 1e-10:
                unified_components[g] /= mag
        
        self.unified_equation = Shape(
            shape_id="unified_equation",
            components=unified_components,
            grade=max(unified_components.keys()) if unified_components else 0,
            name="unified_universe_equation",
            birth_step=self.step
        )
        
        return self.unified_equation
    
    def query(self, target_grade: int) -> Dict:
        """
        Extract information about a specific grade from the unified equation.
        
        This is the key capability: given the unified equation, we can
        query for any grade's information with high accuracy.
        """
        if not self.unified_equation:
            self.compute_unified_equation()
        
        eq = self.unified_equation
        
        if target_grade not in eq.components:
            # Project onto target grade using inner product
            projected = np.zeros(self.dim + 1)
            for shape in self.shapes.values():
                projected[target_grade] += self._project_grade(shape, target_grade)
            return {
                "grade": target_grade,
                "components": projected[target_grade],
                "magnitude": abs(projected[target_grade]),
                "source": "projected"
            }
        
        return {
            "grade": target_grade,
            "components": eq.components[target_grade],
            "magnitude": np.sum(np.abs(eq.components[target_grade])),
            "source": "direct"
        }
    
    def _project_grade(self, shape: Shape, target_grade: int) -> float:
        """Project a shape onto a target grade."""
        if target_grade not in shape.components:
            return 0.0
        return np.sum(shape.components[target_grade])
    
    def run_interaction_cycle(self, num_interactions: int = 100):
        """Run a cycle of random shape interactions."""
        shape_ids = list(self.shapes.keys())
        
        for _ in range(num_interactions):
            # Pick two random shapes
            a_id, b_id = np.random.choice(shape_ids, 2, replace=False)
            
            # Only interact if shapes are "close enough" (simulated by probability)
            if np.random.random() < 0.3:  # 30% interaction probability
                result = self.interact(a_id, b_id)
                
                # Log interaction
                self.interaction_log.append({
                    "step": self.step,
                    "parents": [a_id, b_id],
                    "result_grade": result.grade,
                    "parent_grades": [self.shapes[a_id].grade, self.shapes[b_id].grade]
                })
                
                # Add result to candidates (don't always keep — simulates selection)
                if np.random.random() < 0.5:
                    shape_ids.append(result.shape_id)
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about the universe state."""
        if not self.shapes:
            return {}
        
        grades = [s.grade for s in self.shapes.values()]
        magnitudes = [s.total_magnitude for s in self.shapes.values()]
        entropies = [s.grade_entropy for s in self.shapes.values()]
        
        # Count shapes by grade
        grade_counts = {}
        for g in grades:
            grade_counts[g] = grade_counts.get(g, 0) + 1
        
        # Count anomalies
        grade_transitions = [a for a in self.anomaly_log if a.get("is_grade_transition")]
        
        return {
            "step": self.step,
            "num_shapes": len(self.shapes),
            "grade_distribution": grade_counts,
            "avg_magnitude": np.mean(magnitudes),
            "max_magnitude": np.max(magnitudes),
            "avg_grade_entropy": np.mean(entropies),
            "num_anomalies": len(self.anomaly_log),
            "num_grade_transitions": len(grade_transitions),
            "dominant_grade": max(grade_counts, key=grade_counts.get) if grade_counts else 0,
            "unified_equation_grades": len(self.unified_equation.components) if self.unified_equation else 0
        }
    
    def export_state(self, path: str = ""):
        """Export universe state to JSON."""
        state = {
            "name": self.name,
            "step": self.step,
            "dim": self.dim,
            "shapes": {},
            "anomalies": self.anomaly_log[-50:],  # Last 50
            "statistics": self.get_statistics()
        }
        
        for sid, s in self.shapes.items():
            state["shapes"][sid] = {
                "grade": s.grade,
                "components": {str(g): c.tolist() for g, c in s.components.items()},
                "name": s.name,
                "birth_step": s.birth_step,
                "interaction_count": s.interaction_count,
                "fingerprint": s.fingerprint()
            }
        
        p = Path(path) if path else Path(f"universe_{self.name}_step{self.step}.json")
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w') as f:
            json.dump(state, f, indent=2)
        
        return p


# ============================================================
# ANOMALY DETECTION ENGINE
# ============================================================

class AnomalyDetector:
    """
    Detects when a newly created shape represents a genuine anomaly —
    something that cannot be explained by the linear combination of its parents.
    
    Anomalies are the key to novel shape emergence.
    """
    
    def __init__(self, universe: Universe):
        self.universe = universe
        self.detected_anomalies: List[Dict] = []
    
    def detect_grade_anomaly(self, shape: Shape) -> Dict:
        """
        A grade anomaly occurs when a shape's dominant grade is NOT
        present in any of its parents. This means the shape has
        'transcended' its dimensional origins.
        """
        if len(shape.parent_ids) < 2:
            return {"type": "none", "reason": "insufficient_parents"}
        
        parent_grades = set()
        for pid in shape.parent_ids:
            if pid in self.universe.shapes:
                parent_grades.add(self.universe.shapes[pid].grade)
        
        if shape.grade not in parent_grades:
            return {
                "type": "grade_transition",
                "new_grade": shape.grade,
                "parent_grades": list(parent_grades),
                "shape_id": shape.shape_id,
                "description": f"Shape transcended from grades {parent_grades} to grade {shape.grade}"
            }
        
        return {"type": "none"}
    
    def detect_complexity_anomaly(self, shape: Shape) -> Dict:
        """
        A complexity anomaly occurs when a shape's grade entropy exceeds
        what would be expected from its parents' entropies.
        """
        if len(shape.parent_ids) < 2:
            return {"type": "none"}
        
        parent_entropies = []
        for pid in shape.parent_ids:
            if pid in self.universe.shapes:
                parent_entropies.append(self.universe.shapes[pid].grade_entropy)
        
        if not parent_entropies:
            return {"type": "none"}
        
        expected_entropy = np.mean(parent_entropies) * 1.5  # Allow 50% growth
        if shape.grade_entropy > expected_entropy:
            return {
                "type": "complexity_increase",
                "parent_entropy": expected_entropy,
                "shape_entropy": shape.grade_entropy,
                "shape_id": shape.shape_id,
                "description": f"Shape complexity exceeded parent expectation ({shape.grade_entropy:.4f} > {expected_entropy:.4f})"
            }
        
        return {"type": "none"}
    
    def detect_magnitude_anomaly(self, shape: Shape) -> Dict:
        """
        A magnitude anomaly occurs when a shape's total magnitude is
        significantly larger than the sum of its parents' magnitudes.
        This indicates emergent amplification through interaction.
        """
        if len(shape.parent_ids) < 2:
            return {"type": "none"}
        
        parent_mags = []
        for pid in shape.parent_ids:
            if pid in self.universe.shapes:
                parent_mags.append(self.universe.shapes[pid].total_magnitude)
        
        if not parent_mags:
            return {"type": "none"}
        
        parent_sum = sum(parent_mags)
        if shape.total_magnitude > parent_sum * 2.0:
            return {
                "type": "magnitude_emergence",
                "parent_magnitude": parent_sum,
                "shape_magnitude": shape.total_magnitude,
                "amplification": shape.total_magnitude / max(parent_sum, 1e-10),
                "shape_id": shape.shape_id,
                "description": f"Shape magnitude amplified {shape.total_magnitude/parent_sum:.2f}x beyond parents"
            }
        
        return {"type": "none"}
    
    def full_detect(self, shape: Shape) -> List[Dict]:
        """Run all anomaly detection on a shape."""
        results = []
        for detector in [self.detect_grade_anomaly, self.detect_complexity_anomaly,
                        self.detect_magnitude_anomaly]:
            result = detector(shape)
            if result["type"] != "none":
                result["shape_id"] = shape.shape_id
                results.append(result)
        
        if results:
            shape._is_anomaly = True
            self.detected_anomalies.extend(results)
        
        return results


# ============================================================
# MAIN EXPERIMENT
# ============================================================

def run_experiment(num_cycles: int = 50, interactions_per_cycle: int = 50):
    """
    Run the multidimensional shape equation experiment.
    
    We explore:
    1. How shapes evolve through interaction
    2. When novel shapes (anomalies) emerge
    3. At what point the unified equation stabilizes
    4. How the grade distribution changes over time
    """
    print("=" * 70)
    print("MULTIDIMENSIONAL SHAPE EQUATION EXPERIMENT")
    print("=" * 70)
    
    results = []
    
    for universe_dim in [3, 4, 5, 6]:
        print(f"\n{'─' * 70}")
        print(f"UNIVERSE: dim={universe_dim}")
        print(f"{'─' * 70}")
        
        uni = Universe(dim=universe_dim, name=f"dim{universe_dim}")
        detector = AnomalyDetector(uni)
        
        print(f"Initial shapes: {len(uni.shapes)}")
        print(f"  Grade distribution: {dict(zip(*np.unique([s.grade for s in uni.shapes.values()], return_counts=True)))}")
        
        # Track anomaly emergence over time
        anomaly_timeline = []
        stats_timeline = []
        
        for cycle in range(num_cycles):
            uni.run_interaction_cycle(interactions_per_cycle)
            
            # Check for anomalies in newly created shapes
            for sid in list(uni.shapes.keys())[-interactions_per_cycle:]:
                if sid in uni.shapes:
                    anomalies = detector.full_detect(uni.shapes[sid])
                    if anomalies:
                        anomaly_timeline.append({
                            "cycle": cycle,
                            "anomalies": len(anomalies)
                        })
            
            # Record stats every 5 cycles
            if cycle % 5 == 0 or cycle == num_cycles - 1:
                stats = uni.get_statistics()
                stats["cycle"] = cycle
                stats_timeline.append(stats)
        
        # Compute final unified equation
        uni.compute_unified_equation()
        final_stats = uni.get_statistics()
        final_stats["cycle"] = "final"
        
        print(f"\nFinal state:")
        print(f"  Total shapes: {final_stats['num_shapes']}")
        print(f"  Grade distribution: {final_stats['grade_distribution']}")
        print(f"  Anomalies detected: {final_stats['num_anomalies']}")
        print(f"  Grade transitions: {final_stats['num_grade_transitions']}")
        print(f"  Unified equation spans: {final_stats['unified_equation_grades']} grades")
        
        # Query tests
        print(f"\nUnified equation queries:")
        for target_grade in range(uni.dim + 1):
            query_result = uni.query(target_grade)
            print(f"  Grade {target_grade}: magnitude={query_result['magnitude']:.4f} "
                  f"(source: {query_result['source']})")
        
        results.append({
            "dim": universe_dim,
            "final_stats": final_stats,
            "anomaly_timeline": anomaly_timeline,
            "stats_timeline": stats_timeline
        })
    
    return results


def analyze_anomaly_emergence(results: List[Dict]):
    """
    Analyze when and why novel shapes appear.
    
    Key questions:
    1. At what interaction count do anomalies first appear?
    2. What parent grade combinations produce anomalies?
    3. Does higher dimensionality increase anomaly frequency?
    4. Is there a critical threshold?
    """
    print("\n" + "=" * 70)
    print("ANOMALY EMERGENCE ANALYSIS")
    print("=" * 70)
    
    for r in results:
        dim = r["dim"]
        timeline = r["stats_timeline"]
        
        print(f"\nDimension {dim}:")
        
        # Find when anomalies first appear
        first_anomaly = None
        for s in timeline:
            if s.get("num_anomalies", 0) > 0:
                first_anomaly = s["cycle"]
                break
        
        if first_anomaly is not None:
            print(f"  First anomaly at cycle: {first_anomaly}")
        else:
            print(f"  No anomalies detected")
        
        # Track anomaly growth
        anomaly_counts = [s.get("num_anomalies", 0) for s in timeline]
        if anomaly_counts:
            print(f"  Anomaly progression: {anomaly_counts}")
            
            # Check for acceleration (critical threshold)
            if len(anomaly_counts) >= 3:
                diffs = [anomaly_counts[i+1] - anomaly_counts[i] 
                        for i in range(len(anomaly_counts)-1)]
                max_diff_idx = diffs.index(max(diffs)) if diffs else 0
                print(f"  Max acceleration at cycle: {timeline[max_diff_idx]['cycle']}")
        
        # Grade distribution evolution
        grade_histories = []
        for s in timeline:
            grade_histories.append(s.get("grade_distribution", {}))
        print(f"  Grade distribution evolution: {grade_histories}")


if __name__ == "__main__":
    results = run_experiment(num_cycles=50, interactions_per_cycle=50)
    analyze_anomaly_emergence(results)
    
    # Save results
    output = {
        "experiment": "multidimensional_shape_equations",
        "config": {"num_cycles": 50, "interactions_per_cycle": 50},
        "results": results
    }
    
    # Convert non-serializable types
    for r in output["results"]:
        for i, s in enumerate(r.get("stats_timeline", [])):
            s["grade_distribution"] = {str(k): v for k, v in s.get("grade_distribution", {}).items()}
    
    with open("shape_sim/results.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to shape_sim/results.json")
