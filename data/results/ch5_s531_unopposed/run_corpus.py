"""The §5.3.1 no-defence corpus — the run half.

Design: docs/handoffs/2026-09-15_ch5_s531_unopposed_runs.md §1 (accepted by Marc
2026-09-15). Six arms (the baseline attacker; the movement attacker on the four
profiles and the aggregate), no defence, the targeted objective on the database
set, 100 seeds shared across arms, at the 15 000 s core horizon and the 60 000 s
extension. Plus the diagnostic arm: the five movement arms at 15 000 s under the
general objective, reported in the analysis only.

Every pin of Table 5.3 is passed by name here — in particular the failure-only
overlay, because the registry default is still v1. This script simulates and
records; every number is computed by ``analyse.py`` off the recorded stream.

    PYTHONPATH=src python data/results/ch5_s531_unopposed/run_corpus.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "runs.jsonl"
# The reported corpus (REPORTED=1; seed-count protocol, Marc 2026-09-30): 1 000
# seeds, the APT attacker model with the vulnerability memory on
# (Table 5.1: each earlier success triples the odds; code rate 2, factor 1 + 2)
# and the baseline attacker with none, on the cells §5.2's floats read (the
# targeted objective at 15 000 s; the 60 000 s extension and the general
# diagnostic are in no float). runs.jsonl stays the 100-seed record.
OUT_REPORTED = HERE / "runs_reported.jsonl"
REPORTED_SEEDS = 1_000
MEMORY_RATE = 2.0

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
SEEDS = tuple(range(100))
HORIZONS = (15_000, 60_000)
MAPPING = "v2_partial"
OVERLAY = "v4_failure_only"


def _movement(job: dict) -> dict:
    from mtdsim.l3_simulation.movement.run import run_movement

    r = run_movement(
        job["profile"],
        seed=job["seed"],
        with_synthetic_overlay=True,
        horizon=job["horizon"],
        mapping_version=MAPPING,
        overlay_version=OVERLAY,
        retrace_sinks=True,
        mtd_scheme=None,
        mtd_interval=None,
        attack_objective=job["objective"],
        target_layer=None,
        # the vulnerability memory (Section 4.4.5); absent from the 100-seed
        # corpus's jobs, so those re-run byte-identical with it off
        exploit_learning_rate=job.get("exploit_learning_rate"),
    )
    return {
        **job,
        "termination_time": float(r.termination_time),
        "compromised": int(r.compromised_count),
        "reached_objective": bool(r.reached_objective),
        "database_hosts_reached": int(r.database_hosts_reached),
        "first_database_reach_time": r.first_database_reach_time,
        "target_hosts": list(r.target_hosts),
        "retrace_count": int(r.retrace_count),
        "last_next_place": (r.records[-1].next_place if r.records else None),
        "records": [
            [
                x.place, x.verb, x.outcome, x.verdict, int(x.blocked), int(x.interrupted),
                round(float(x.dwell), 6), round(float(x.start_time), 6),
                round(float(x.end_time), 6), x.place_class,
            ]
            for x in r.records
        ],
    }


def _baseline(job: dict) -> dict:
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
        attack_op, network, job["objective"], target_layer=None, seed=seed
    )
    attack_op.proceed_attack()
    env.run(until=job["horizon"])

    rows = adversary.get_attack_stats().get_record()
    database = set(int(h) for h in network.get_database())
    compromised = set(adversary.get_compromised_hosts())
    return {
        **job,
        "termination_time": float(env.now),
        "compromised": int(len(compromised)),
        "reached_objective": bool(end_event.triggered),
        "database_hosts_reached": int(len(compromised & database)),
        "first_database_reach_time": None,
        "target_hosts": sorted(int(h) for h in target_hosts),
        # The native attack record, the columns the baseline adapter and the
        # coverage reference read: name, times, compromise host (uuid-stable).
        "records": [
            [
                str(x["name"]), round(float(x["start_time"]), 6),
                round(float(x["finish_time"]), 6),
                None if str(x["compromise_host"]) == "None" else int(x["compromise_host"]),
                str(x["compromise_host_uuid"]),
            ]
            for x in rows.to_dict("records")
        ],
    }


def dispatch(job: dict) -> dict:
    try:
        return _baseline(job) if job["arm"] == "baseline" else _movement(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {"error": f"{type(exc).__name__}: {exc}", **job}


def build_jobs(seeds=SEEDS, memory: bool = False) -> list[dict]:
    """``memory`` builds the reported corpus: the core cells only, the
    vulnerability memory's rate on every APT attacker model job. The 100-seed
    corpus's jobs carry none."""
    if memory:
        return [{"arm": "baseline", "profile": "baseline", "objective": "targeted", "horizon": 15_000, "seed": s}
                if p == "baseline" else
                {"arm": "movement", "profile": p, "objective": "targeted", "horizon": 15_000, "seed": s,
                 "exploit_learning_rate": MEMORY_RATE}
                for s in seeds for p in ("baseline",) + PROFILES]
    jobs: list[dict] = []
    for horizon in HORIZONS:
        for seed in seeds:
            jobs.append({"arm": "baseline", "profile": "baseline", "objective": "targeted",
                         "horizon": horizon, "seed": seed})
            for p in PROFILES:
                jobs.append({"arm": "movement", "profile": p, "objective": "targeted",
                             "horizon": horizon, "seed": seed})
    for seed in seeds:  # the diagnostic arm
        for p in PROFILES:
            jobs.append({"arm": "movement", "profile": p, "objective": "general",
                         "horizon": 15_000, "seed": seed})
    return jobs


def main() -> int:
    reported = os.environ.get("REPORTED") == "1"
    out = Path(os.environ.get("OUT", OUT_REPORTED if reported else OUT))
    jobs = (build_jobs(range(int(os.environ.get("SEEDS", REPORTED_SEEDS))), memory=True)
            if reported else build_jobs())
    workers = int(os.environ.get("WORKERS", min(6, os.cpu_count() or 4)))
    print(f"{len(jobs)} runs on {workers} workers -> {out}", flush=True)
    started = time.time()
    done = errors = 0
    with out.open("w", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(dispatch, jobs, chunksize=8):
            fh.write(json.dumps(row) + "\n")
            done += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if done % 200 == 0:
                print(f"  {done}/{len(jobs)}  {time.time() - started:.0f}s", flush=True)
    print(f"done: {done} runs, {errors} errors, {time.time() - started:.0f}s")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
