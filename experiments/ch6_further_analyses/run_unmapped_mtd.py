#!/usr/bin/env python3
"""The tactic-duration ablation under MTD (Jin's final feedback, item 13;
Marc approved the setup 2026-10-18; data/supervisor_feedback/item13_setup.md).

Section 6.2 explains why the service layer reduces the APT attacker model's NCR
less than the baseline attacker's: a service-layer deployment disrupts an
attacker only during an attack action, and the APT attacker model's tactic
durations keep it in unmapped tactics, which run none. Appendix D.6 removed the
time in unmapped tactics with no MTD only. This run removes it under MTD.

ONE CHANGE: the seven unmapped tactics take 0 s (D.6's first step, the
``unmapped_zero`` catalogue of run_duration_ablation.py); mapped tactics keep
their declared means. Everything else at the reported corpus's pins
(ch5_defended/run_corpus.py: v2_partial, v4_failure_only, retrace on, targeted,
the shifted regime, 15 000 s, the vulnerability memory at rate 2).

CELLS: c1-c4 x {IP shuffle, service diversity} at 200 s x seeds 0-999 = 8 000
runs, seed-major, resumable. The no-MTD cell is D.6's ``unmapped_zero`` rows
(experiments/ch6_further_analyses/runs_duration_ablation.jsonl). The baseline
attacker uses no tactic durations, so its reported rows stand.

CHECKS, before any number is read (--smoke):
  1. declared durations, seed 0, c1-c4 x {none, IP shuffle, service diversity}
     reproduce the reported corpus (hosts, MTD-interrupted attack actions);
  2. unmapped_zero, no MTD, seeds 0-19 through this harness equal D.6's rows on
     every recorded field (so D.6's no-MTD rows are this run's denominator).

CRITERION, fixed before the run (reported whichever way):
  measures, averaged over c1-c4, seed bootstrap 95 % intervals: NCR reduction
  (1 - mean NCR with MTD / mean NCR with no MTD, same durations) and attack
  actions blocked per MTD deployment (Equation 4.13, time_lost.py's view()).
  (a) SUPPORTED: under service diversity both measures rise above the declared
      durations' values at 200 s, the 95 % intervals apart.
  (b) MECHANISM ONLY: blocked per deployment rises, NCR reduction does not;
      Section 6.2 keeps the mechanism, T2 keeps the outcome as untested.
  (c) The host layer's lead does not depend on the time in unmapped tactics
      if IP shuffle's NCR reduction stays above service diversity's.

    PYTHONPATH=src WORKERS=7 python experiments/ch6_further_analyses/run_unmapped_mtd.py [--smoke]
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
import pickle
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPERIMENTS = ROOT / "experiments"
OUT = EXPERIMENTS / "ch6_further_analyses" / "runs_unmapped_mtd.jsonl"
SMOKE_OUT = EXPERIMENTS / "ch6_further_analyses" / "smoke_unmapped_mtd.jsonl"
D6_ROWS = EXPERIMENTS / "ch6_further_analyses" / "runs_duration_ablation.jsonl"
SUMMARIES = EXPERIMENTS / "ch5_defended" / "runs_reported_summaries.pkl"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


corpus = _load("ch5_defended_run_corpus", ROOT / "experiments/ch5_defended/run_corpus.py")
ablation = _load("ch6_run_duration_ablation", HERE / "run_duration_ablation.py")

INTERVAL = 200
CONDITIONS = ("ip_shuffle", "service_diversity")
SEEDS = range(corpus.REPORTED_SEEDS)
D6_CHECK_SEEDS = range(20)


def build_jobs(seeds, variant, conditions) -> list[dict]:
    jobs = []
    for seed in seeds:
        for profile in corpus.FOUR:
            for c in conditions:
                i = 0 if c == "none" else INTERVAL
                jobs.append({**corpus._job("core", "movement", profile, "targeted", c, i,
                                           "shifted", corpus.OVERLAY, seed),
                             "exploit_learning_rate": corpus.MEMORY_RATE, "variant": variant})
    return jobs


def run_one(job: dict) -> dict:
    import mtdsim.l3_simulation.movement.run as mrun

    means = ablation.catalogues()[job["variant"]]
    original = mrun.run_movement

    def with_durations(*a, **kw):
        return original(*a, dwell_catalogue=means, **kw)

    mrun.run_movement = with_durations  # corpus._movement imports it from the module at call time
    try:
        return corpus._movement(job)
    finally:
        mrun.run_movement = original


def dispatch(job: dict) -> dict:
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return run_one(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {**job, "error": f"{type(exc).__name__}: {exc}"}


def _pool(jobs, workers, chunksize):
    with ProcessPoolExecutor(workers) as pool:
        yield from pool.map(dispatch, jobs, chunksize=chunksize)


def smoke(workers: int) -> int:
    # 1. declared durations reproduce the reported corpus
    jobs = build_jobs((0,), "centre", ("none",) + CONDITIONS)
    rows = list(_pool(jobs, workers, 1))
    cells, _ = pickle.load(SUMMARIES.open("rb"))
    bad = 0
    for r in rows:
        if "error" in r:
            print("ERROR", r["error"]); bad += 1; continue
        key = ("core", "movement", r["profile"], "targeted", r["condition"], r["interval"],
               "shifted", corpus.OVERLAY)
        ref = next(x for x in cells[key] if x["seed"] == r["seed"])
        got = {"hosts": r["compromised"], "substrate_interrupted": r["mtd_attack_interrupted"]}
        want = {"hosts": ref["hosts"], "substrate_interrupted": ref["substrate_interrupted"]}
        ok = got == want
        bad += not ok
        print(f"  check 1 {r['profile']:32s} {r['condition']:18s} {'ok' if ok else f'DIFFERS {got} vs {want}'}")
    # 2. unmapped_zero, no MTD, through this harness == D.6's rows
    jobs = build_jobs(D6_CHECK_SEEDS, "unmapped_zero", ("none",))
    mine = {(r["profile"], r["seed"]): r for r in _pool(jobs, workers, 4)}
    fields = ("compromised", "reached_objective", "termination_time", "records")
    matched = 0
    with D6_ROWS.open() as fh:
        for line in fh:
            if '"variant": "unmapped_zero"' not in line[:200]:
                continue
            ref = json.loads(line)
            k = (ref["profile"], ref["seed"])
            if k not in mine:
                continue
            diff = [f for f in fields if mine[k].get(f) != ref[f]]
            if diff:
                bad += 1
                print(f"  check 2 {k}: DIFFERS on {diff}")
            matched += 1
    print(f"  check 2: {matched} of {len(mine)} no-MTD runs compared with D.6's rows")
    bad += matched != len(mine)
    with SMOKE_OUT.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print("SMOKE PASS" if not bad else f"SMOKE FAIL ({bad})", flush=True)
    return 1 if bad else 0


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
            keys.add((r["seed"], r["profile"], r["condition"]))
    return keys


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--smoke", action="store_true", help="the two checks; nothing else is run")
    args = ap.parse_args(argv)
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    if args.smoke:
        return smoke(workers)
    done = _done(OUT)
    jobs = [j for j in build_jobs(SEEDS, "unmapped_zero", CONDITIONS)
            if (j["seed"], j["profile"], j["condition"]) not in done]
    print(f"{len(jobs)} runs on {workers} workers -> {OUT}", flush=True)
    started, n, errors = time.time(), 0, 0
    with OUT.open("a") as fh:
        for row in _pool(jobs, workers, 8):
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            n += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if n % 500 == 0:
                el = time.time() - started
                print(f"  {n}/{len(jobs)}  {el:.0f}s  (~{el / n * (len(jobs) - n) / 60:.0f} min left)", flush=True)
    print(f"done: {n} runs, {errors} errors, {time.time() - started:.0f}s", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
