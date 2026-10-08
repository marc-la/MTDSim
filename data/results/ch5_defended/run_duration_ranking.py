#!/usr/bin/env python3
"""Does the ranking survive the 45 s band? (Marc 2026-10-08, threat 2 of the
chapter 6 examiners: "the headline isn't tested across the durations set by
judgement"; handoff 2026-10-07_ch6_discussion_assembly.md section 13.)

Appendix C moved each shared mean duration to both ends of its band and read
the APT attacker model's NCR under no MTD and random only; the comparison with
the baseline attacker was not repeated across the bands (Appendix C, the
sentence that says so). This run repeats section 5.3's 200 s cells for the APT
attacker model with the 45 s mean duration (persistence, stealth, command and
control: family "stealth-low-and-slow") at both ends of its band, x0.25 and x4
(11.25 s and 180 s), everything else at the reported corpus's pins
(run_corpus.py REPORTED=1: v2_partial, v4_failure_only, retrace on, targeted,
the shifted regime, 15 000 s, the vulnerability memory at rate 2).

The baseline attacker uses no tactic duration, so its rows in
runs_reported.jsonl are the comparison as they stand; only the APT arm is run.

Cells: the four attack profiles x {no MTD, the nine of DEFENDED, MTDShield} at
200 s x {x0.25, x4} x seeds 0-999 = 88 000 runs, seed-major, resumable.
Rows are slim (no event records): what NCR, NCR reduction and ASP need.

CRITERION, fixed before the run (Marc 2026-10-08): the declared-point ranking
of section 5.3 at 200 s (Scott-Knott ESD on NCR reduction, rho against the
baseline attacker) is re-computed at each band end. The headline HOLDS at a
band end if (a) the MTD mechanisms in the APT attacker model's rank 1 share no
member with the baseline attacker's rank 1, and (b) the host layer ranks above
the service layer for the APT attacker model. Reported either way.

    PYTHONPATH=src WORKERS=7 python data/results/ch5_defended/run_duration_ranking.py [--smoke]
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
OUT = HERE / "runs_duration_ranking.jsonl"
SMOKE_OUT = HERE / "smoke_duration_ranking.jsonl"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


corpus = _load("ch5_defended_run_corpus", HERE / "run_corpus.py")
rate = _load("rate_feasibility_run_study", RESULTS / "rate_feasibility_study" / "run_study.py")

FAMILY = "stealth-low-and-slow"
FACTORS = rate.ANCHOR_BANDS[FAMILY]  # (0.25, 4.0)
INTERVAL = 200
CONDITIONS = ("none",) + corpus.DEFENDED + ("mtdshield",)
SEEDS = range(corpus.REPORTED_SEEDS)
KEEP = ("termination_time", "compromised", "reached_objective", "database_hosts_reached",
        "first_database_reach_time", "retrace_count", "mtd_count", "mtd_attack_interrupted")


def build_jobs(seeds, factors, profiles) -> list[dict]:
    jobs = []
    for seed in seeds:
        for factor in factors:
            for profile in profiles:
                for c in CONDITIONS:
                    i = 0 if c == "none" else INTERVAL
                    jobs.append({**corpus._job("core", "movement", profile, "targeted", c, i,
                                               "shifted", corpus.OVERLAY, seed),
                                 "exploit_learning_rate": corpus.MEMORY_RATE,
                                 "family": FAMILY, "factor": factor})
    return jobs


def run_one(job: dict) -> dict:
    import mtdsim.l3_simulation.movement.run as mrun

    means = rate.scaled_means(rate._load_catalogue(), {job["family"]: job["factor"]})
    original = mrun.run_movement

    def with_durations(*a, **kw):
        return original(*a, dwell_catalogue=means, **kw)

    mrun.run_movement = with_durations  # corpus._movement imports it from the module at call time
    try:
        row = corpus._movement(job)
    finally:
        mrun.run_movement = original
    return {**job, **{k: row.get(k) for k in KEEP}}


def dispatch(job: dict) -> dict:
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return run_one(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {**job, "error": f"{type(exc).__name__}: {exc}"}


def _done(path: Path) -> set:
    if not path.exists():
        return set()
    keys = set()
    with path.open() as fh:
        for line in fh:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue  # a line cut off by a killed run
            keys.add((r["seed"], r["factor"], r["profile"], r["condition"]))
    return keys


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--smoke", action="store_true",
                    help="seed 0, factor 1.0 (the declared point), every profile and condition: "
                         "must match runs_reported.jsonl")
    args = ap.parse_args(argv)
    if args.smoke:
        jobs, out = build_jobs((0,), (1.0,), corpus.FOUR), SMOKE_OUT
        out.unlink(missing_ok=True)
    else:
        jobs, out = build_jobs(SEEDS, FACTORS, corpus.FOUR), OUT
        done = _done(out)
        jobs = [j for j in jobs if (j["seed"], j["factor"], j["profile"], j["condition"]) not in done]
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    print(f"{len(jobs)} runs on {workers} workers -> {out}", flush=True)
    started, n, errors = time.time(), 0, 0
    with out.open("a") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(dispatch, jobs, chunksize=1 if args.smoke else 8):
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            n += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if n % 1000 == 0:
                el = time.time() - started
                print(f"  {n}/{len(jobs)}  {el:.0f}s  (~{el / n * (len(jobs) - n) / 3600:.1f} h left)", flush=True)
    print(f"done: {n} runs, {errors} errors, {time.time() - started:.0f}s", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
