"""Multidimensional Shape Equations (MSE) package.

Core module:
  mse.py — Full Cl(d, 0) geometric algebra, Shape, Universe, AnomalyDetector.

Usage:
    from shape_sim.mse import Universe, Shape, AnomalyDetector

    uni = Universe(dim=4, container="cube")
    uni.run_cycle(100)
    stats = uni.get_statistics()
"""

from shape_sim.mse import (
    AnomalyDetector,
    BladeIndexer,
    Shape,
    Universe,
    create_universe,
    run_cycle,
)

__all__ = [
    "AnomalyDetector",
    "BladeIndexer",
    "Shape",
    "Universe",
    "create_universe",
    "run_cycle",
]
