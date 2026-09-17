"""The chapter 5 defended corpus — the run half, shared by §5.3.2, §5.4 and §5.5.

Design: docs/handoffs/2026-09-17_ch5_s532_s55_defended_runs.md. One corpus at
the chapter's declared configuration (Table 5.3: v2_partial, the failure-only
overlay passed by name, retrace on, fresh-host contract on, modulators off, the
targeted objective on the database set, 100 seeds shared across arms, 15 000 s)
over Table 5.2's defence conditions (no defence; the seven mechanisms alone;
random and alternative over the seven) at both mutation intervals, on six arms
(the baseline attacker; the movement attacker on the four profiles and the
aggregate). Four arm groups, keyed by ``group``:

  core      targeted objective, quasi-periodic ("shifted") regime — every
            §5.4.1, §5.4.2 and §5.5 float
  blind     the verdict-blind control (F_v = identity) on the four profiles
            under the spanning pair (IP shuffle; OS diversity) at both
            intervals, plus no defence — §5.3.2's control and its placebo null
  lineage   the same matrix under the opportunistic ("general") objective —
            §5.4.3's re-run of the prior evaluations at the lineage's objective
  regime    the exponential (memoryless) timing regime at 200 s, targeted —
            Table 5.2's one-at-a-time factor, read in the analysis

The no-defence cell never reads the interval or the regime, so it is run once
per arm and objective (``interval`` 0) and serves as the reference at both.
Every number is computed by ``analyse.py`` off the recorded stream.

    PYTHONPATH=src python data/results/ch5_defended/run_corpus.py
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

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
FOUR = PROFILES[:4]
SEEDS = tuple(range(100))
INTERVALS = (200, 2_000)
HORIZON = 15_000
MAPPING = "v2_partial"
OVERLAY = "v4_failure_only"

# condition -> (scheme, mechanism class or None for the full pool)
CONDITIONS: dict[str, tuple[str | None, str | None]] = {
    "none": (None, None),
    "ip_shuffle": ("single", "IPShuffle"),
    "complete_topology": ("single", "CompleteTopologyShuffle"),
    "host_topology": ("single", "HostTopologyShuffle"),
    "port_shuffle": ("single", "PortShuffle"),
    "user_shuffle": ("single", "UserShuffle"),
    "os_diversity": ("single", "OSDiversity"),
    "service_diversity": ("single", "ServiceDiversity"),
    "random": ("random", None),
    "alternative": ("alternative", None),
}
DEFENDED = tuple(c for c in CONDITIONS if c != "none")
SPANNING = ("ip_shuffle", "os_diversity")
MODULES = {
    "CompleteTopologyShuffle": "completetopologyshuffle",
    "HostTopologyShuffle": "hosttopologyshuffle",
    "IPShuffle": "ipshuffle",
    "OSDiversity": "osdiversity",
    "PortShuffle": "portshuffle",
    "ServiceDiversity": "servicediversity",
    "UserShuffle": "usershuffle",
}


def _strategies(condition: str):
    """``custom_strategies`` for the seam: one class for a single mechanism,
    the full seven-mechanism pool (Table 5.2: "random and alternative over the
    seven") for a scheme, None for no defence. The substrate's default pool
    is the lineage four, so the seven are passed explicitly."""
    import importlib

    scheme, mech = CONDITIONS[condition]
    if scheme is None:
        return None, None
    if mech is not None:
        return scheme, getattr(importlib.import_module(f"mtdnetwork.mtd.{MODULES[mech]}"), mech)
    return scheme, [
        getattr(importlib.import_module(f"mtdnetwork.mtd.{MODULES[m]}"), m) for m in MODULES
    ]


def _mtd_fields(result_like) -> dict:
    return {
        "mtd_executions": [
            [e.name, round(float(e.start_time), 6), round(float(e.finish_time), 6),
             round(float(e.duration), 6), e.layer]
            for e in result_like["mtd_executions"]
        ],
        "mtd_suspended": int(result_like["mtd_suspended_count"]),
        "mtd_attack_interrupted": int(result_like["mtd_attack_interrupted"]),
    }


def _movement(job: dict) -> dict:
    from mtdsim.l3_simulation.controller import verdict_blind_overlay
    from mtdsim.l3_simulation.movement.run import run_movement

    scheme, strategies = _strategies(job["condition"])
    overlay_kw = (
        {"overlay": verdict_blind_overlay()} if job["overlay"] == "verdict_blind"
        else {"overlay_version": job["overlay"]}
    )
    r = run_movement(
        job["profile"],
        seed=job["seed"],
        with_synthetic_overlay=True,
        horizon=job["horizon"],
        mapping_version=MAPPING,
        retrace_sinks=True,
        mtd_scheme=scheme,
        mtd_interval=(job["interval"] or None),
        custom_strategies=strategies,
        substrate_timing_regime=job["regime"],
        attack_objective=job["objective"],
        target_layer=None,
        **overlay_kw,
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
        **_mtd_fields({
            "mtd_executions": r.mtd_executions,
            "mtd_suspended_count": r.mtd_suspended_count,
            "mtd_attack_interrupted": r.mtd_attack_interrupted,
        }),
    }


def _baseline(job: dict) -> dict:
    """The inherited attacker, wired as the Gate 0 harness and the frontier
    study wired it: the shared ``AttackOperation``, the objective installed
    through the same ``_install_objective`` seam, the defence through the
    substrate's own ``MTDOperation`` on the same ``end_event``."""
    import random

    import numpy as np
    import simpy

    from mtdnetwork.component.adversary import Adversary
    from mtdnetwork.component.time_network import TimeNetwork
    from mtdnetwork.data.constants import ATTACKER_THRESHOLD
    from mtdnetwork.operation.attack_operation import AttackOperation
    from mtdsim.l3_simulation.movement.run import GEOMETRY, _install_objective, mtd_snapshot
    from mtdnetwork.component.time_generator import set_exponential_regime

    seed = job["seed"]
    random.seed(seed)
    np.random.seed(seed)
    set_exponential_regime(job["regime"])
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary, proceed_time=0)
    target_hosts, _, _ = _install_objective(
        attack_op, network, job["objective"], target_layer=None, seed=seed
    )
    attack_op.proceed_attack()
    scheme, strategies = _strategies(job["condition"])
    if scheme:
        from mtdnetwork.operation.mtd_operation import MTDOperation
        from mtdnetwork.statistic.security_metric_statistics import SecurityMetricStatistics

        MTDOperation(
            security_metrics_record=SecurityMetricStatistics(), env=env,
            end_event=end_event, network=network, scheme=scheme,
            attack_operation=attack_op, proceed_time=0,
            mtd_trigger_interval=job["interval"],
            custom_strategies=strategies, adversary=adversary,
        ).proceed_mtd()
    env.run(until=job["horizon"])

    rows = adversary.get_attack_stats().get_record()
    database = set(int(h) for h in network.get_database())
    compromised = set(adversary.get_compromised_hosts())
    recs = rows.to_dict("records")
    distinct_uuid = len({str(x["compromise_host_uuid"]) for x in recs
                         if str(x["compromise_host"]) != "None"})
    return {
        **job,
        "termination_time": float(env.now),
        "compromised": int(len(compromised)),
        "compromised_uuid": int(distinct_uuid),
        "reached_objective": bool(end_event.triggered),
        "database_hosts_reached": int(len(compromised & database)),
        "first_database_reach_time": None,
        "target_hosts": sorted(int(h) for h in target_hosts),
        "records": [
            [
                str(x["name"]), round(float(x["start_time"]), 6),
                round(float(x["finish_time"]), 6),
                None if str(x["compromise_host"]) == "None" else int(x["compromise_host"]),
                str(x["compromise_host_uuid"]),
                None if str(x["interrupted_in"]) == "None" else str(x["interrupted_in"]),
            ]
            for x in recs
        ],
        **_mtd_fields(mtd_snapshot(network)),
    }


def dispatch(job: dict) -> dict:
    import contextlib
    import io

    try:
        # The substrate's metric record prints a line for each mechanism it has
        # no column for (the three restored singles); it is not an error and
        # would otherwise flood the log under the seven-mechanism schemes.
        with contextlib.redirect_stdout(io.StringIO()):
            return _baseline(job) if job["arm"] == "baseline" else _movement(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {"error": f"{type(exc).__name__}: {exc}", **job}


def _job(group, arm, profile, objective, condition, interval, regime, overlay, seed) -> dict:
    return {"group": group, "arm": arm, "profile": profile, "objective": objective,
            "condition": condition, "interval": interval, "regime": regime,
            "overlay": overlay, "horizon": HORIZON, "seed": seed}


def build_jobs() -> list[dict]:
    jobs: list[dict] = []
    arms = [("baseline", "baseline")] + [("movement", p) for p in PROFILES]
    for group, objective in (("core", "targeted"), ("lineage", "general")):
        for seed in SEEDS:
            for arm, profile in arms:
                jobs.append(_job(group, arm, profile, objective, "none", 0, "shifted", OVERLAY, seed))
                for interval in INTERVALS:
                    for c in DEFENDED:
                        jobs.append(_job(group, arm, profile, objective, c, interval, "shifted", OVERLAY, seed))
    for seed in SEEDS:  # the verdict-blind control, §5.3.2
        for p in FOUR:
            jobs.append(_job("blind", "movement", p, "targeted", "none", 0, "shifted", "verdict_blind", seed))
            for interval in INTERVALS:
                for c in SPANNING:
                    jobs.append(_job("blind", "movement", p, "targeted", c, interval, "shifted", "verdict_blind", seed))
    for seed in SEEDS:  # the memoryless regime, one at a time from the core
        for arm, profile in arms:
            for c in DEFENDED:
                jobs.append(_job("regime", arm, profile, "targeted", c, 200, "exponential", OVERLAY, seed))
    return jobs


def main() -> int:
    jobs = build_jobs()
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    print(f"{len(jobs)} runs on {workers} workers -> {OUT}", flush=True)
    started = time.time()
    done = errors = 0
    with OUT.open("w", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(dispatch, jobs, chunksize=16):
            fh.write(json.dumps(row) + "\n")
            done += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if done % 1000 == 0:
                print(f"  {done}/{len(jobs)}  {time.time() - started:.0f}s", flush=True)
    print(f"done: {done} runs, {errors} errors, {time.time() - started:.0f}s")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
