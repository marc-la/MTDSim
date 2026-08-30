"""Gate 0 re-ask for the targeted attacker (rung 7 of
docs/handoffs/2026-08-30_targeted_attacker_build.md; pre-registered in
docs/implementation/pipeline/ogasp/targeted_attacker_findings.md §2 BEFORE this
file produced a number).

Unopposed, 350 seeds, five movement profiles + the inherited baseline, both
arms running Brown's targeted objective through the SAME seam
(``_install_objective`` on the shared AttackOperation), for four targets: one
host drawn on layer 1, 2 and 3 (Brown's TX) and the database set. Reports per
arm × target: reach rate (BCa CI), time-to-target (censored), footprint at
reach, hosts total. Cross-arm comparisons are unpaired (D-29).

    PYTHONPATH=src python data/results/targeted_attacker_build/run_gate0.py
"""

from __future__ import annotations

import csv
import json
import sys
from multiprocessing import Pool
from pathlib import Path

OUT = Path(__file__).parent
HORIZON = 15_000
SEEDS = tuple(range(350))
PROFILES = ("aggregate", "objective_exfiltration", "objective_impact",
            "objective_exfiltration_impact", "objective_none_c2")
TARGETS = {"L1": 1, "L2": 2, "L3": 3, "db": None}


def run_movement_cell(job: dict) -> dict:
    from mtdsim.l3_simulation.movement.run import run_movement

    r = run_movement(job["profile"], seed=job["seed"], horizon=HORIZON,
                     mapping_version="v2_partial", attack_objective="targeted",
                     target_layer=TARGETS[job["target"]])
    reach_row = next((x for x in r.records if x.target_class == 0), None)
    return {
        "arm": "movement", "profile": job["profile"], "target": job["target"],
        "target_hosts": list(r.target_hosts), "seed": job["seed"],
        "reached_target": bool(r.reached_objective),
        "time_to_target": r.termination_time if r.reached_objective else None,
        "footprint_at_reach": (r.compromised_count if r.reached_objective else None),
        "hosts_total": r.compromised_count,
        "termination_time": r.termination_time,
        "first_target_selection_time": reach_row.start_time if reach_row else None,
    }


def run_baseline_cell(job: dict) -> dict:
    import random

    import numpy as np
    import simpy

    from mtdnetwork.component.adversary import Adversary
    from mtdnetwork.component.time_network import TimeNetwork
    from mtdnetwork.data.constants import ATTACKER_THRESHOLD
    from mtdnetwork.operation.attack_operation import AttackOperation
    from mtdsim.l3_simulation.movement.run import GEOMETRY, _install_objective

    seed = job["seed"]
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary, proceed_time=0)
    target_hosts, _, _ = _install_objective(
        attack_op, network, "targeted", target_layer=TARGETS[job["target"]], seed=seed
    )
    attack_op.proceed_attack()
    env.run(until=HORIZON)

    rows = adversary.get_attack_stats().get_record()
    compromises = rows[rows["compromise_host"].astype(str) != "None"].copy()
    hit = compromises[compromises["compromise_host"].apply(
        lambda h: str(h) != "None" and int(h) in target_hosts)]
    reached = bool(end_event.triggered) and len(hit) > 0
    ttt = float(hit["finish_time"].min()) if reached else None
    footprint = (int(compromises[compromises["finish_time"] <= ttt]["compromise_host"]
                     .astype(int).nunique()) if reached else None)
    return {
        "arm": "baseline", "profile": "-", "target": job["target"],
        "target_hosts": sorted(target_hosts), "seed": seed,
        "reached_target": reached, "time_to_target": ttt,
        "footprint_at_reach": footprint,
        "hosts_total": int(compromises["compromise_host"].astype(int).nunique()),
        "termination_time": float(env.now),
        "first_target_selection_time": None,
    }


def _cell(job):
    return run_baseline_cell(job) if job["arm"] == "baseline" else run_movement_cell(job)


def main() -> int:
    jobs = []
    for target in TARGETS:
        for seed in SEEDS:
            jobs.append({"arm": "baseline", "profile": "-", "target": target, "seed": seed})
            for p in PROFILES:
                jobs.append({"arm": "movement", "profile": p, "target": target, "seed": seed})
    print(f"{len(jobs)} runs", file=sys.stderr)
    with Pool() as pool:
        rows = list(pool.imap_unordered(_cell, jobs, chunksize=8))
    rows.sort(key=lambda r: (r["target"], r["arm"], r["profile"], r["seed"]))
    with open(OUT / "gate0_rows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            r = dict(r)
            r["target_hosts"] = json.dumps(r["target_hosts"])
            w.writerow(r)
    print(f"wrote {OUT / 'gate0_rows.csv'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
