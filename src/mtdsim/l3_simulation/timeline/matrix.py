"""The run matrix — which cells exist, how seeds derive, library generation.

The matrix (per the timeline-runner brief): {5 profiles} × {entry:
``initial-access`` always; ``reconnaissance`` where the prefix gap is bridged
(D8 — both entries where possible)} × {policy arms: weighted on the
``operator_dedup`` corpus variant (primary), weighted on ``raw`` (a cheap
robustness arm, included rather than deferred), uniform (the structural
floor)} × {duration variants: catalogue central values; the sweep exercised
at the extremes only — full sensitivity stays deferred, D10}.

For the two classes whose recon place is an island on the observed-only base
(``objective_exfiltration_impact``, ``objective_none_c2``), the recon-seeded arm is
**impossible**, and the matrix records that as a result rather than silently
skipping it (the prefix-bridge overlay stays deferred — GAP Decision 6
Option B).

Seeds derive deterministically from the run id (SHA-256, first 8 bytes), so
the whole library is reproducible from this module alone and no two runs in
the matrix share an RNG stream by accident.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from mtdsim.l3_simulation.timeline.walk import (
    DURATION_VARIANTS,
    MAX_STEPS,
    OBJECTIVE_RULES,
    OGASP_DIR,
    PETRI_DIR,
    PRIMARY_WEIGHT_VARIANT,
    PROFILE_NAMES,
    SCHEMA_VERSION,
    TIMELINE_DIR,
    Net,
    dwell_table,
    load_catalogue,
    load_net,
    serialise,
    walk,
)

TIMELINES_DIR = TIMELINE_DIR / "_timelines"  # gitignored via data/ogasp/timeline/_*

N_RUNS = 100  # seeded runs per cell (the brief's floor; cheap)

ENTRY_INITIAL_ACCESS = "initial-access"
ENTRY_RECON = "reconnaissance"

# (policy, weight_variant) arms. Uniform reads no weights, hence None.
POLICY_ARMS = (
    ("weighted", "operator_dedup"),
    ("weighted", "raw"),
    ("uniform", None),
)


@dataclass(frozen=True)
class Cell:
    """One run-matrix cell — N_RUNS seeded walks share these coordinates."""

    profile: str
    entry: str
    policy: str
    weight_variant: str | None
    duration_variant: str

    @property
    def arm(self) -> str:
        if self.policy == "uniform":
            return "uniform"
        return f"weighted-{self.weight_variant}"

    @property
    def cell_id(self) -> str:
        return f"{self.profile}--{self.entry}--{self.arm}--{self.duration_variant}"

    def run_id(self, index: int) -> str:
        return f"{self.cell_id}--{index:03d}"


def seed_for(run_id: str) -> int:
    """Deterministic per-run seed: first 8 bytes of SHA-256(run_id)."""
    return int.from_bytes(hashlib.sha256(run_id.encode()).digest()[:8], "big")


def entries_for(net: Net) -> list[str]:
    """D8 entries: initial-access always; recon only where bridged."""
    entries = [ENTRY_INITIAL_ACCESS]
    if net.recon_bridged:
        entries.append(ENTRY_RECON)
    return entries


def build_matrix(nets: dict) -> tuple[list[Cell], list[dict]]:
    """All runnable cells, plus the impossible recon arms recorded as results."""
    cells = []
    impossible = []
    for profile in PROFILE_NAMES:
        net = nets[profile]
        for entry in entries_for(net):
            for policy, weight_variant in POLICY_ARMS:
                for duration_variant in DURATION_VARIANTS:
                    cells.append(
                        Cell(profile, entry, policy, weight_variant, duration_variant)
                    )
        if not net.recon_bridged:
            impossible.append(
                {
                    "profile": profile,
                    "entry": ENTRY_RECON,
                    "status": "impossible",
                    "reason": (
                        "reconnaissance is an island on the observed-only base "
                        "(the prefix gap): recon cannot reach initial-access, so "
                        "a recon-seeded token cannot reach the objective. The "
                        "literature-grounded prefix bridge (GAP Decision 6 "
                        "Option B) stays deferred; see data/ogasp/petri/README.md."
                    ),
                }
            )
    return cells, impossible


def generate_cell(net: Net, catalogue: dict, cell: Cell, n_runs: int = N_RUNS) -> list[dict]:
    """N seeded walks for one cell, in run-index order."""
    dwells = dwell_table(catalogue, cell.duration_variant)
    records = []
    for i in range(n_runs):
        run_id = cell.run_id(i)
        records.append(
            walk(
                net,
                dwells,
                entry=cell.entry,
                policy=cell.policy,
                weight_variant=cell.weight_variant,
                duration_variant=cell.duration_variant,
                seed=seed_for(run_id),
                run_id=run_id,
            )
        )
    return records


def generate_library(
    out_dir: Path = TIMELINES_DIR,
    ogasp_dir: Path = OGASP_DIR,
    petri_dir: Path = PETRI_DIR,
    n_runs: int = N_RUNS,
) -> tuple[dict, dict]:
    """Generate the full timeline library: one JSONL per cell + a manifest.

    Returns ``(manifest, records_by_cell_id)`` so the verification report can
    be built from the same in-memory pass. Bulk outputs are regenerable and
    live under the gitignored ``_timelines/``; the committed contract is the
    schema doc + example + report.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    catalogue = load_catalogue(ogasp_dir)
    nets = {p: load_net(p, petri_dir) for p in PROFILE_NAMES}
    cells, impossible = build_matrix(nets)

    library: dict[str, list[dict]] = {}
    cell_index = []
    for cell in cells:
        records = generate_cell(nets[cell.profile], catalogue, cell, n_runs)
        library[cell.cell_id] = records
        path = out_dir / f"{cell.cell_id}.jsonl"
        with open(path, "w") as f:
            for record in records:
                f.write(serialise(record) + "\n")
        outcomes: dict[str, int] = {}
        for record in records:
            outcomes[record["outcome"]] = outcomes.get(record["outcome"], 0) + 1
        cell_index.append(
            {
                "cell_id": cell.cell_id,
                "file": path.name,
                "profile": cell.profile,
                "entry": cell.entry,
                "policy": cell.policy,
                "weight_variant": cell.weight_variant,
                "duration_variant": cell.duration_variant,
                "n_runs": len(records),
                "outcomes": dict(sorted(outcomes.items())),
            }
        )

    manifest = {
        "schema": SCHEMA_VERSION,
        "declared": {
            "n_runs_per_cell": n_runs,
            "max_steps": MAX_STEPS,
            "seed_derivation": "int.from_bytes(sha256(run_id)[:8], 'big')",
            "objective_rules": OBJECTIVE_RULES,
            "primary_weight_variant": PRIMARY_WEIGHT_VARIANT,
            "raw_arm": "included (robustness), not deferred",
            "duration_variants": list(DURATION_VARIANTS),
            "sweep_arithmetic": (
                "extreme dwell = anchors[group].duration_s × sweep_bound "
                "(anchor units; see tactic_durations.json meta.sweep_range_units)"
            ),
        },
        "impossible_arms": impossible,
        "cells": cell_index,
    }
    with open(out_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return manifest, library


__all__ = [
    "Cell",
    "ENTRY_INITIAL_ACCESS",
    "ENTRY_RECON",
    "N_RUNS",
    "POLICY_ARMS",
    "TIMELINES_DIR",
    "build_matrix",
    "entries_for",
    "generate_cell",
    "generate_library",
    "seed_for",
]
