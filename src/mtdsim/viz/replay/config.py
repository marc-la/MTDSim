"""Canonical replay configurations.

``PRIMARY`` reproduces Joo Kai Tay's flagship network + finish time from
[2024-Tay MTDShield, §5] — see .context/notebooks/2026-03-29_MTDSim_RetrainMTDAI.md
(``total_nodes=100, total_endpoints=5, total_subnets=8, total_layers=4,
total_database=2, terminate_compromise_ratio=0.8``; ``FINISH_TIME=15000``).

``DEMO`` is the smaller 30-node graph used by the GAP-subgraph notebook.
Kept only so the viewer boots quickly in CI / on a laptop without the
full primary run (~30 s sim).

Why a separate module and not a dict in ``__main__``: other surfaces
(runner, demo notebook, tests) need to pin the same numbers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReplayConfig:
    name: str
    finish_time: int
    network_params: dict[str, Any] = field(default_factory=dict)
    seed: int = 42

    def log_path(self, scheme: str, root: Path) -> Path:
        return root / f"{self.name}_{scheme}_{self.seed}.jsonl"


PRIMARY = ReplayConfig(
    name="primary",
    finish_time=15000,
    network_params=dict(
        total_nodes=100,
        total_endpoints=5,
        total_subnets=8,
        total_layers=4,
        total_database=2,
        terminate_compromise_ratio=0.8,
    ),
    seed=42,
)

DEMO = ReplayConfig(
    name="demo",
    finish_time=5000,
    network_params=dict(
        total_nodes=30,
        total_endpoints=3,
        total_subnets=6,
        total_layers=3,
        total_database=1,
        terminate_compromise_ratio=0.8,
    ),
    seed=42,
)

CONFIGS: dict[str, ReplayConfig] = {PRIMARY.name: PRIMARY, DEMO.name: DEMO}

DEFAULT_EVENTS_DIR = Path("notebooks/gap_out/events")
