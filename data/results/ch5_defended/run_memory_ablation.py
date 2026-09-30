"""§5.4.2 Vulnerability memory — the run half: memory off / on / every exploit
succeeding, swept over the diversity pool.

Design: Marc 2026-09-30 (chat): "pool size on the X axis ... host compromise or
... ASP reduction on the other ... two lines". The ablation (does the memory
change the attack outcome?) is the pool-20 point, the network every chapter 5
number runs on; the hypothesis of Section 4.4.5 (is its effect larger when the
diversity pool is constrained?) is the same on-minus-off difference read across
pools. Handoff: docs/handoffs/2026-09-28_vulnerability_memory_on.md, Part A.

Grid, the chapter's declared configuration otherwise (run_corpus.py: v2_partial,
the failure-only overlay, retrace on, targeted, 15 000 s):
  memory     off (every exploit at its CVSS probability); on (each earlier
             success triples the odds, Section 4.4.5; code rate 2.0); perfect
             (every exploit the OS check allows succeeds: the most any memory
             acting on the exploit roll could give)
  pool       services per operating system, 1 2 3 5 10 20 (20 is the
             simulator's default and the evaluated network)
  condition  no MTD; service diversity and OS diversity at 200 s, the two
             mechanisms that redraw services from the pool
  profiles   c_1 to c_4; the same seeds on every cell

Read on minus off WITHIN a pool, paired by seed: a thinner pool changes the
network itself, so the memory-off attacker also moves across pools.

The perfect arm replaces ``Adversary.effective_exploit_prob`` with 1.0 for the
job: the OS check still refuses first (services.Vulnerability.network), and the
roll still draws its random number, so the random stream stays aligned with the
other arms. The roll counter is a read-only wrapper. Both patches are undone
after every job, because pool workers are reused.

    PYTHONPATH=src python data/results/ch5_defended/run_memory_ablation.py
    SEEDS=1000 ... (the reported count; default 100, the preliminary pass)
    LIMIT=N ...    (timing probe: the first N jobs, not written)
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_corpus import FOUR, HORIZON, MAPPING, OVERLAY, _strategies  # noqa: E402

OUT = HERE / "runs_memory.jsonl"
POOLS = (1, 2, 3, 5, 10, 20)
MEMORY = ("off", "on", "perfect")
CONDITIONS = (("none", 0), ("service_diversity", 200), ("os_diversity", 200))
RATE_ON = 2.0  # odds x (1 + 2) = x3 per earlier success (Section 4.4.5, Table 5.1)


def _run(job: dict) -> dict:
    from mtdnetwork.component import services
    from mtdnetwork.component.adversary import Adversary
    from mtdsim.l3_simulation.movement import run as run_mod

    V = services.Vulnerability
    orig_network, orig_eep, orig_tn = V.network, Adversary.effective_exploit_prob, run_mod.TimeNetwork
    rolls = Counter()
    wins_by_type = Counter()
    built = {}

    def network(self, host=None, success_prob=None):
        if self.exploited:
            return orig_network(self, host=host, success_prob=success_prob)
        if self.has_os_dependency and host is not None and host.os_type not in self.vuln_os_list:
            rolls["refused"] += 1
            return orig_network(self, host=host, success_prob=success_prob)
        out = orig_network(self, host=host, success_prob=success_prob)
        rolls["rolled"] += 1
        if self.exploited:
            rolls["won"] += 1
            wins_by_type[self.id] += 1
        return out

    class CapturedNetwork(orig_tn):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            built["network"] = self

    V.network = network
    run_mod.TimeNetwork = CapturedNetwork
    if job["memory"] == "perfect":
        Adversary.effective_exploit_prob = lambda self, vuln: 1.0
    try:
        scheme, strategies = _strategies(job["condition"])
        r = run_mod.run_movement(
            job["profile"],
            seed=job["seed"],
            with_synthetic_overlay=True,
            horizon=HORIZON,
            mapping_version=MAPPING,
            retrace_sinks=True,
            mtd_scheme=scheme,
            mtd_interval=(job["interval"] or None),
            custom_strategies=strategies,
            substrate_timing_regime="shifted",
            attack_objective="targeted",
            target_layer=None,
            overlay_version=OVERLAY,
            exploit_learning_rate=(RATE_ON if job["memory"] == "on" else None),
            geometry=dict(run_mod.GEOMETRY, services_per_os=job["pool"]),
        )
    finally:
        V.network, Adversary.effective_exploit_prob, run_mod.TimeNetwork = orig_network, orig_eep, orig_tn

    net = built["network"]
    types = set()
    for host in net.get_hosts().values():
        for _, svc in host.graph.nodes(data="service"):
            if svc is not None:
                types.update(v.id for v in svc.vulnerabilities)
    return {
        **job,
        "termination_time": float(r.termination_time),
        "compromised": int(r.compromised_count),
        "reached_objective": bool(r.reached_objective),
        "database_hosts_reached": int(r.database_hosts_reached),
        "first_database_reach_time": r.first_database_reach_time,
        "vuln_types": len(types),
        "rolls": int(rolls["rolled"]),
        "wins": int(rolls["won"]),
        "refused": int(rolls["refused"]),
        "types_won": len(wins_by_type),
        "types_rewon": sum(1 for c in wins_by_type.values() if c >= 2),
        "mtd_deployments": len(r.mtd_executions),
    }


def dispatch(job: dict) -> dict:
    import contextlib
    import io

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return _run(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {"error": f"{type(exc).__name__}: {exc}", **job}


def build_jobs(seeds) -> list[dict]:
    return [
        {"group": "memory", "memory": m, "pool": pool, "profile": p,
         "condition": c, "interval": i, "seed": s}
        for s in seeds for pool in POOLS for m in MEMORY for p in FOUR for c, i in CONDITIONS
    ]


def main() -> int:
    jobs = build_jobs(range(int(os.environ.get("SEEDS", 100))))
    if os.environ.get("LIMIT"):
        jobs = jobs[: int(os.environ["LIMIT"])]
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    out = os.devnull if os.environ.get("LIMIT") else OUT
    print(f"{len(jobs)} runs on {workers} workers -> {out}", flush=True)
    started = time.time()
    done = errors = 0
    with open(out, "w", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
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
