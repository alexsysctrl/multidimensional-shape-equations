#!/usr/bin/env python3
"""
Multidimensional Shape Equations — Experiment Runner
=====================================================

Tests all container geometries at dim=4:
  cube, sphere, ellipsoid, torus, open, sinai

Runs 50 cycles with 100 interactions each.
Records full timeline data (every cycle).
Saves comprehensive results as JSON.

Usage:
    python3 shape_sim/run_experiment.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

# Ensure the project root is on the path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from shape_sim.mse import (
    AnomalyDetector,
    Universe,
)

# Configuration
DIM = 4
NUM_CYCLES = 50
INTERACTIONS_PER_CYCLE = 100
CONTAINERS = ["cube", "sphere", "ellipsoid", "torus", "open", "sinai"]
SEED = 42


def run_container_experiment(
    dim: int = DIM,
    num_cycles: int = NUM_CYCLES,
    interactions: int = INTERACTIONS_PER_CYCLE,
    containers: List[str] = CONTAINERS,
    seed: int = SEED,
) -> Dict[str, Any]:
    """Run the full container comparison experiment.

    For each container geometry:
      1. Create a Universe(dim=dim, container=name).
      2. Run `num_cycles` cycles, each with `interactions` interaction attempts.
      3. Record full timeline data every cycle.
      4. Compute the unified equation and run all query types.
      5. Compute final statistics.

    Args:
        dim: Dimensionality of the space.
        num_cycles: Number of interaction cycles.
        interactions: Interaction attempts per cycle.
        containers: List of container geometries to test.
        seed: Random seed for reproducibility.

    Returns:
        Dict mapping container name → experiment results.
    """
    rng = np.random.default_rng(seed)
    all_results: Dict[str, Any] = {}

    print("=" * 72)
    print("MULTIDIMENSIONAL SHAPE EQUATIONS — EXPERIMENT")
    print("=" * 72)
    print(f"Configuration:")
    print(f"  Dimension:     {dim}")
    print(f"  Cycles:        {num_cycles}")
    print(f"  Interactions:  {interactions}/cycle")
    print(f"  Containers:    {', '.join(containers)}")
    print(f"  Seed:          {seed}")
    print("=" * 72)

    for container in containers:
        print(f"\n{'─' * 72}")
        print(f"CONTAINER: {container.upper()}")
        print(f"{'─' * 72}")

        # Create universe with seeded RNG
        uni = Universe(dim=dim, container=container, name=container, rng=rng)
        detector = AnomalyDetector(uni)

        initial_shapes = len(uni.shapes)
        print(f"Initial shapes: {initial_shapes}")

        # Timeline tracking
        stats_timeline: List[Dict] = []
        anomaly_timeline: List[Dict] = []

        for cycle in range(num_cycles):
            # Run interaction cycle
            new_ids = uni.run_cycle(interactions)

            # Detect anomalies in newly created shapes
            cycle_anomalies = 0
            for sid in new_ids:
                if sid in uni.shapes:
                    anomalies = detector.full_detect(uni.shapes[sid])
                    cycle_anomalies += len(anomalies)

            # Record timeline every cycle
            stats = uni.get_statistics()
            stats["cycle"] = cycle
            stats_timeline.append(stats)

            anomaly_timeline.append({
                "cycle": cycle,
                "new_anomalies": cycle_anomalies,
                "total_anomalies": len(uni.anomaly_log),
            })

            # Progress reporting every 10 cycles
            if (cycle + 1) % 10 == 0:
                print(
                    f"  Cycle {cycle + 1:3d}/{num_cycles}: "
                    f"{len(uni.shapes):5d} shapes, "
                    f"{len(uni.anomaly_log):5d} anomalies, "
                    f"{cycle_anomalies:3d} new anomalies"
                )

        # Compute unified equation and queries
        uni.compute_unified_equation()
        full_query = uni.query("full")
        energy_query = uni.query("energy")
        novelty_query = uni.query("novelty")

        # Grade-specific queries
        grade_queries = {}
        for g in range(dim + 1):
            grade_queries[str(g)] = uni.query("grade", grade=g)

        final_stats = uni.get_statistics()

        print(f"\nFinal state:")
        print(f"  Total shapes:      {final_stats['num_shapes']}")
        print(f"  Grade distribution: {final_stats['grade_distribution']}")
        print(f"  Total anomalies:   {final_stats['num_anomalies']}")
        print(f"  Anomaly types:     {final_stats['anomaly_types']}")
        print(f"  Avg magnitude:     {final_stats['avg_magnitude']:.4f}")
        print(f"  Max magnitude:     {final_stats['max_magnitude']:.4f}")
        print(f"  Avg entropy:       {final_stats['avg_entropy']:.4f}")
        print(f"  Unified eq magnitude: {full_query['magnitude']:.4f}")
        print(f"  Energy distribution: {energy_query['distribution']}")

        # Store results
        all_results[container] = {
            "config": {
                "dim": dim,
                "num_cycles": num_cycles,
                "interactions_per_cycle": interactions,
                "seed": seed,
            },
            "final_stats": final_stats,
            "stats_timeline": stats_timeline,
            "anomaly_timeline": anomaly_timeline,
            "queries": {
                "full": {
                    "magnitude": full_query["magnitude"],
                    "grade_profile": full_query["grade_profile"],
                },
                "energy": energy_query,
                "novelty": novelty_query,
                "grade_specific": grade_queries,
            },
        }

    return all_results


def summarize_results(results: Dict[str, Any]) -> None:
    """Print a summary comparison across all containers."""
    print("\n" + "=" * 72)
    print("SUMMARY: CONTAINER COMPARISON")
    print("=" * 72)

    print(f"\n{'Container':<12} {'Shapes':>7} {'Anomalies':>10} {'Struct.':>8} "
          f"{'Grade':>7} {'Complex':>8} {'AvgMag':>8} {'AvgEnt':>8}")
    print(f"{'─'*12} {'─'*7} {'─'*10} {'─'*8} {'─'*7} {'─'*8} {'─'*8} {'─'*8}")

    for container, data in sorted(results.items()):
        fs = data["final_stats"]
        at = fs.get("anomaly_types", {})
        structural = at.get("structural_novelty", 0)
        grade_trans = at.get("grade_transition", 0)
        complexity = at.get("complexity_spike", 0)

        print(
            f"{container:<12} {fs['num_shapes']:>7} {fs['num_anomalies']:>10} "
            f"{structural:>8} {grade_trans:>7} {complexity:>8} "
            f"{fs['avg_magnitude']:>8.4f} {fs['avg_entropy']:>8.4f}"
        )

    # Anomaly type breakdown
    print(f"\n{'─' * 72}")
    print("ANOMALY TYPE BREAKDOWN (aggregate):")
    print(f"{'─' * 72}")

    total_structural = 0
    total_grade = 0
    total_complexity = 0
    total_anomalies = 0

    for container, data in results.items():
        at = data["final_stats"].get("anomaly_types", {})
        total_structural += at.get("structural_novelty", 0)
        total_grade += at.get("grade_transition", 0)
        total_complexity += at.get("complexity_spike", 0)
        total_anomalies += data["final_stats"]["num_anomalies"]

    grand = total_structural + total_grade + total_complexity
    if grand > 0:
        print(f"  Structural novelty:  {total_structural:>6d} ({total_structural/grand*100:5.1f}%)")
        print(f"  Grade transition:    {total_grade:>6d} ({total_grade/grand*100:5.1f}%)")
        print(f"  Complexity spike:    {total_complexity:>6d} ({total_complexity/grand*100:5.1f}%)")

    # Energy distribution comparison
    print(f"\n{'─' * 72}")
    print("ENERGY DISTRIBUTION BY GRADE (unified equation):")
    print(f"{'─' * 72}")

    print(f"\n  {'Container':<12}", end="")
    for g in range(DIM + 1):
        print(f"{'G'+str(g):>8}", end="")
    print()
    print(f"  {'─'*12}", end="")
    for _ in range(DIM + 1):
        print(f"{'─'*8}", end="")
    print()

    for container, data in sorted(results.items()):
        energy = data["queries"]["energy"]["distribution"]
        print(f"  {container:<12}", end="")
        for g in range(DIM + 1):
            val = energy.get(str(g), 0.0)
            print(f"{val:>7.2%}", end="")
        print()

    # Anomaly growth rate
    print(f"\n{'─' * 72}")
    print("ANOMALY GROWTH RATE (per cycle):")
    print(f"{'─' * 72}")

    for container, data in results.items():
        timeline = data["anomaly_timeline"]
        total = timeline[-1]["total_anomalies"]
        rate = total / NUM_CYCLES
        print(f"  {container:<12}: {rate:6.1f} anomalies/cycle (total: {total})")

    print()


def save_results(results: Dict[str, Any], output_path: str = "") -> Path:
    """Save experiment results to JSON.

    Args:
        results: The experiment results dict.
        output_path: Output file path. Defaults to
                     shape_sim/mse_results.json.

    Returns:
        Path to the saved file.
    """
    p = Path(output_path) if output_path else Path("shape_sim/mse_results.json")
    p.parent.mkdir(parents=True, exist_ok=True)

    # Build serializable output
    output: Dict[str, Any] = {
        "experiment": "multidimensional_shape_equations",
        "version": "mse.py",
        "config": {
            "dim": DIM,
            "num_cycles": NUM_CYCLES,
            "interactions_per_cycle": INTERACTIONS_PER_CYCLE,
            "containers": CONTAINERS,
            "seed": SEED,
        },
        "results": results,
    }

    with open(p, "w") as f:
        json.dump(output, f, indent=2)

    return p


def main() -> None:
    """Run the full experiment, print summary, and save results."""
    # Run experiment
    results = run_container_experiment()

    # Print summary
    summarize_results(results)

    # Save results
    output_path = save_results(results)
    print(f"Results saved to {output_path}")

    # Validation: verify key invariants
    print("\n" + "=" * 72)
    print("VALIDATION CHECKS")
    print("=" * 72)

    for container, data in results.items():
        fs = data["final_stats"]

        # Check 1: shapes > 0
        assert fs["num_shapes"] > 0, f"{container}: no shapes!"

        # Check 2: anomalies > 0
        assert fs["num_anomalies"] > 0, f"{container}: no anomalies!"

        # Check 3: grade distribution sums to num_shapes
        grade_sum = sum(fs["grade_distribution"].values())
        assert grade_sum == fs["num_shapes"], (
            f"{container}: grade distribution sum {grade_sum} != "
            f"num_shapes {fs['num_shapes']}"
        )

        # Check 4: anomaly types sum to total anomalies
        type_sum = sum(fs.get("anomaly_types", {}).values())
        assert type_sum == fs["num_anomalies"], (
            f"{container}: anomaly types sum {type_sum} != "
            f"total {fs['num_anomalies']}"
        )

        # Check 5: energy distribution sums to ~1.0
        energy = data["queries"]["energy"]["distribution"]
        energy_sum = sum(energy.values())
        assert abs(energy_sum - 1.0) < 0.01, (
            f"{container}: energy distribution sums to {energy_sum}"
        )

        print(f"  {container}: ✓ all checks passed")

    print("\nAll validation checks passed.")


if __name__ == "__main__":
    main()
