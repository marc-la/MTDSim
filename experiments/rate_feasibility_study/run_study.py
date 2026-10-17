"""The rate feasibility study — the pre-registered sweep, executed.

Runs the grid pre-registered in
``docs/implementation/pipeline/ogasp/rate_feasibility_study.md`` §4 (committed
before this script produced any output; the commit ordering is the
pre-registration evidence):

- **Sweep A** — each group anchor at its catalogue-derived band ends, others
  central, MTD ∈ {off, random @ 200}.
- **Sweep B** — central anchors across the mutation-interval axis, plus the
  stealth-anchor × interval interaction corners.
- **Sweep C** — same-mean Erlang-4 firing for the stealth-low-and-slow group
  (every other tactic keeps the declared exponential), on the
  interrupt-pressure gradient.
- **Baseline arm** — the native 6-phase attacker, once per MTD condition (it
  consumes no catalogue value, so anchor cells share it).

Analysis only: nothing here changes a declared value. Anchor scaling happens by
handing ``run_movement`` a *scaled copy* of the duration catalogue —
``m[group] × relative_multiplier × anchor.duration_s`` — so per-tactic
multipliers ride along unchanged and the tracked catalogue is never touched.
The Erlang arm passes a study-local ``TimingSource`` (same protocol, same
derived-seed discipline as the declared regime) rather than editing the build.

Determinism (SIM-05): every run is a pure function of (cell config, seed); the
full config is written beside the rows. Rows append incrementally, so an
interrupted sweep resumes by skipping already-recorded (cell_id, arm, profile,
seed) rows.

Reproduce:  PYTHONPATH=src python experiments/rate_feasibility_study/run_study.py --sweep all
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import time
import warnings
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import simpy

_HERE = Path(__file__).resolve().parent
_NUMBERS = _HERE / "numbers"
_REPO = _HERE.parents[2]

# --- pre-registered design constants (record §4–§5) --------------------------
HORIZON = 15_000
SEEDS = (0, 1, 2, 3, 4, 5, 6, 7, 42, 1234)
MAPPING_VERSION = "v2_partial"
# The record §5 pre-declared this contingency: if S1's distance fold-in landed a
# new overlay version before the sweep ran, the sweep uses it and says so. It
# landed (293f742, v2_lifecycle_distance) between the pre-registration commit and
# this run, so the sweep pairs the go-forward weights with the go-forward mapping
# — the configuration experiment 2 will consume. The registry default stays at
# experiment 1's version for reproducibility and is not a canonicity statement.
OVERLAY_VERSION = "v2_lifecycle_distance"
MTD_SCHEME = "random"
CENTRAL_INTERVAL = 200

# Catalogue-derived anchor bands (record §3 — intersection == reference band).
ANCHOR_BANDS = {
    "scan-shaped": (0.5, 2.0),
    "exploit-shaped": (0.5, 2.0),
    "stealth-low-and-slow": (0.25, 4.0),
    "objective-execution": (0.5, 2.0),
}
SWEPT_ANCHORS = tuple(ANCHOR_BANDS)  # prep-off-network stays 0.0 (immediate)

INTERVAL_AXIS = (50, 100, 400, 800)          # sweep B (200 and off live in sweep A)
STEALTH_CORNER_INTERVALS = (50, 800)         # sweep B interaction corners
ERLANG_K = 4                                 # sweep C: same-mean Erlang-4, CV 0.5


def _load_catalogue() -> dict:
    with open(_REPO / "data" / "ogasp" / "tactic_durations.json") as fh:
        return json.load(fh)


def scaled_means(catalogue: dict, factors: dict[str, float]) -> dict[str, float]:
    """``tactic -> m[group] × relative_multiplier × anchor.duration_s``.

    The anchor-sweep arithmetic of record §3: the factor moves the *group
    anchor*, per-tactic multipliers ride along unchanged. A group not named in
    ``factors`` sits at 1.0, which reproduces the declared catalogue exactly.
    """
    means: dict[str, float] = {}
    for tactic, entry in catalogue["tactics"].items():
        anchor_s = float(catalogue["anchors"][entry["anchor"]]["duration_s"])
        m = float(factors.get(entry["group"], 1.0))
        means[tactic] = m * float(entry["relative_multiplier"]) * anchor_s
    return means


def stealth_tactics(catalogue: dict) -> frozenset[str]:
    return frozenset(
        t for t, e in catalogue["tactics"].items()
        if e["group"] == "stealth-low-and-slow"
    )


class ErlangGroupTiming:
    """Sweep C's timing source: same-mean Erlang-k for the stealth group, the
    declared exponential for everything else.

    Implements the movement layer's ``TimingSource`` protocol and uses the same
    derived-seed discipline as the declared regime (``derive_timing_seed``), so
    it is a drop-in same-stream-shape substitution — what changes is only the
    distribution family at fixed mean, which is exactly what §4's sweep C tests.
    An Erlang-k draw is the sum of k exponentials of mean μ/k, so its mean is μ
    by construction and its CV is 1/√k.
    """

    def __init__(self, means: dict[str, float], erlang_places: frozenset[str],
                 *, seed: int = 0, k: int = ERLANG_K) -> None:
        from mtdsim.l3_simulation.movement.timing import derive_timing_seed

        self._means = {t: float(v) for t, v in means.items()}
        self._erlang = erlang_places
        self._k = int(k)
        self._rng = random.Random(derive_timing_seed(seed))

    def mean_for(self, tactic: str) -> float:
        return max(0.0, self._means.get(tactic, 0.0))

    def draw(self, tactic: str) -> float:
        mean = self.mean_for(tactic)
        if mean <= 0.0:
            return 0.0
        if tactic in self._erlang:
            rate = self._k / mean
            return sum(self._rng.expovariate(rate) for _ in range(self._k))
        return self._rng.expovariate(1.0 / mean)


# --- the cells ---------------------------------------------------------------
def build_cells() -> dict[str, dict]:
    """Every movement-arm cell of the pre-registered grid, keyed by cell_id.

    A cell is (anchor factors, mtd interval or None, timing family). Overlaps
    between sweeps (e.g. the all-central × 200 cell) collapse onto one id, and
    the id encodes the config so a resumed run recognises its rows.
    """
    cells: dict[str, dict] = {}

    def add(sweep: str, factors: dict[str, float], interval: int | None,
            family: str = "exponential") -> None:
        fac = {g: float(factors.get(g, 1.0)) for g in SWEPT_ANCHORS}
        key = "_".join(f"{g.split('-')[0]}{fac[g]:g}" for g in SWEPT_ANCHORS)
        cell_id = f"{key}__mtd{interval if interval is not None else 'off'}__{family}"
        if cell_id not in cells:
            cells[cell_id] = {
                "cell_id": cell_id, "sweeps": [], "factors": fac,
                "mtd_interval": interval, "family": family,
            }
        if sweep not in cells[cell_id]["sweeps"]:
            cells[cell_id]["sweeps"].append(sweep)

    # Sweep A: OAT anchor ends + all-central, × {off, 200}.
    for interval in (None, CENTRAL_INTERVAL):
        add("A", {}, interval)
        for anchor in SWEPT_ANCHORS:
            for bound in ANCHOR_BANDS[anchor]:
                add("A", {anchor: bound}, interval)

    # Sweep B: central × interval axis, + stealth-corner interactions.
    for interval in INTERVAL_AXIS:
        add("B", {}, interval)
    for bound in ANCHOR_BANDS["stealth-low-and-slow"]:
        for interval in STEALTH_CORNER_INTERVALS:
            add("B", {"stealth-low-and-slow": bound}, interval)

    # Sweep C: Erlang-4 on the stealth group, interrupt-pressure gradient.
    for interval in (None, CENTRAL_INTERVAL, 50):
        add("C", {}, interval, family=f"erlang{ERLANG_K}")
    add("C", {"stealth-low-and-slow": ANCHOR_BANDS["stealth-low-and-slow"][1]},
        CENTRAL_INTERVAL, family=f"erlang{ERLANG_K}")

    return cells


# --- one run per arm ---------------------------------------------------------
_TERMINAL_TAGS = {"SIM_END", "MAX_EVENTS"}


def _movement_terminal_reason(res) -> str:
    if res.reached_objective:
        return "objective"
    if not res.records:
        return "empty"
    last = res.records[-1]
    if last.outcome == "MAX_EVENTS":
        return "max_events"
    if last.outcome == "SIM_END":
        return "sim_end"
    if last.next_place is None:
        return "sink"
    return "horizon"


def run_movement_cell(cell: dict, profile: str, seed: int) -> dict:
    from mtdsim.l3_simulation.controller.outcome import load_outcome_overlay
    from mtdsim.l3_simulation.movement.run import run_movement
    from mtdsim.l3_simulation.movement.statistics import _COMPROMISE_EVENTS

    catalogue = _load_catalogue()
    means = scaled_means(catalogue, cell["factors"])
    timing = None
    if cell["family"].startswith("erlang"):
        timing = ErlangGroupTiming(means, stealth_tactics(catalogue), seed=seed)

    interval = cell["mtd_interval"]
    res = run_movement(
        profile, seed=seed, with_synthetic_overlay=True, horizon=HORIZON,
        mapping_version=MAPPING_VERSION, dwell_catalogue=means, timing=timing,
        overlay=load_outcome_overlay(version=OVERLAY_VERSION),
        mtd_scheme=(MTD_SCHEME if interval is not None else None),
        mtd_interval=interval,
    )
    recs = [r for r in res.records if r.outcome not in _TERMINAL_TAGS]
    action_recs = [r for r in recs if r.verb]
    dwell_only_recs = [r for r in recs if r.place_class == "dwell-only"]
    n_events = len(action_recs)
    blocked = sum(1 for r in action_recs if r.blocked)
    interrupts = sum(1 for r in recs if r.interrupted)
    successes = sum(1 for r in action_recs if r.verdict == "success")
    compromise_success = sum(
        1 for r in action_recs
        if r.verdict == "success" and (r.verb, r.outcome) in _COMPROMISE_EVENTS
    )
    return {
        "arm": "movement",
        "profile": profile,
        "seed": seed,
        "reached_objective": bool(res.reached_objective),
        "compromised_count": res.compromised_count,
        "first_compromise_time": res.first_compromise_time(),
        "n_events": n_events,
        "n_dwell_only": len(dwell_only_recs),
        "blocked_count": blocked,
        "blocked_fraction": (blocked / n_events) if n_events else 0.0,
        "n_interrupts": interrupts,
        "n_success": successes,
        "n_compromise_success": compromise_success,
        "terminal_reason": _movement_terminal_reason(res),
    }


def run_baseline_cell(interval: int | None, seed: int) -> dict:
    """One native-attacker run — the experiment-1 construction, verbatim."""
    from mtdnetwork.component.adversary import Adversary
    from mtdnetwork.component.time_network import TimeNetwork
    from mtdnetwork.data.constants import ATTACKER_THRESHOLD
    from mtdnetwork.operation.attack_operation import AttackOperation
    from mtdsim.l3_simulation.movement.run import GEOMETRY

    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary,
                                proceed_time=0)
    attack_op.proceed_attack()
    if interval is not None:
        from mtdnetwork.operation.mtd_operation import MTDOperation
        from mtdnetwork.statistic.security_metric_statistics import (
            SecurityMetricStatistics,
        )
        MTDOperation(
            security_metrics_record=SecurityMetricStatistics(), env=env,
            end_event=end_event, network=network, scheme=MTD_SCHEME,
            attack_operation=attack_op, proceed_time=0,
            mtd_trigger_interval=interval, custom_strategies=None,
            adversary=adversary,
        ).proceed_mtd()
    env.run(until=HORIZON)

    record = adversary.get_attack_stats().get_record()
    first = None
    interrupts = 0
    if len(record):
        compromised = record[record["compromise_host"] != "None"]
        if len(compromised):
            first = float(compromised.iloc[0]["finish_time"])
        interrupts = int((record["interrupted_in"] != "None").sum())
    return {
        "arm": "baseline",
        "profile": "baseline",
        "seed": seed,
        "reached_objective": bool(end_event.triggered),
        "compromised_count": len(adversary.get_compromised_hosts()),
        "first_compromise_time": first,
        "n_events": len(record),
        "n_dwell_only": 0,
        "blocked_count": 0,
        "blocked_fraction": 0.0,
        "n_interrupts": interrupts,
        "n_success": None,
        "n_compromise_success": None,
        "terminal_reason": "objective" if end_event.triggered else "horizon",
    }


# --- job table, resume, and execution ----------------------------------------
FIELDS = ["cell_id", "sweeps", "m_scan", "m_exploit", "m_stealth", "m_objective",
          "mtd_interval", "family", "arm", "profile", "seed",
          "reached_objective", "compromised_count", "first_compromise_time",
          "n_events", "n_dwell_only", "blocked_count", "blocked_fraction",
          "n_interrupts", "n_success", "n_compromise_success", "terminal_reason"]


def _cell_meta(cell: dict) -> dict:
    f = cell["factors"]
    return {
        "cell_id": cell["cell_id"],
        "sweeps": "+".join(cell["sweeps"]),
        "m_scan": f["scan-shaped"],
        "m_exploit": f["exploit-shaped"],
        "m_stealth": f["stealth-low-and-slow"],
        "m_objective": f["objective-execution"],
        "mtd_interval": cell["mtd_interval"],
        "family": cell["family"],
    }


def _baseline_cell_meta(interval: int | None) -> dict:
    return {
        "cell_id": f"baseline__mtd{interval if interval is not None else 'off'}",
        "sweeps": "baseline", "m_scan": "", "m_exploit": "", "m_stealth": "",
        "m_objective": "", "mtd_interval": interval, "family": "",
    }


def _run_job(job: tuple) -> dict:
    kind, meta, payload, profile, seed = job
    t0 = time.perf_counter()
    row = (run_movement_cell(payload, profile, seed) if kind == "movement"
           else run_baseline_cell(payload, seed))
    row.update(meta)
    row["_wall_s"] = round(time.perf_counter() - t0, 2)
    return row


def build_jobs(cells: dict[str, dict], profiles: tuple[str, ...],
               sweeps: set[str]) -> list[tuple]:
    jobs: list[tuple] = []
    if sweeps & {"A", "B", "C"}:
        for cell in cells.values():
            if not (set(cell["sweeps"]) & sweeps):
                continue
            meta = _cell_meta(cell)
            for profile in profiles:
                for seed in SEEDS:
                    jobs.append(("movement", meta, cell, profile, seed))
    if "baseline" in sweeps:
        for interval in (None, 50, 100, 200, 400, 800):
            meta = _baseline_cell_meta(interval)
            for seed in SEEDS:
                jobs.append(("baseline", meta, interval, "baseline", seed))
    return jobs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sweep", default="all",
                    help="comma list of A,B,C,baseline or 'all'")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=None,
                    help="run at most N jobs (sizing probe)")
    args = ap.parse_args()
    sweeps = ({"A", "B", "C", "baseline"} if args.sweep == "all"
              else set(args.sweep.split(",")))

    from mtdsim.l3_simulation.movement.net import PROFILES

    _NUMBERS.mkdir(parents=True, exist_ok=True)
    cells = build_cells()
    jobs = build_jobs(cells, PROFILES, sweeps)

    # Resume: skip rows already on disk (identity = cell_id, arm, profile, seed).
    per_run = _NUMBERS / "per_run.csv"
    done: set[tuple] = set()
    if per_run.exists():
        with per_run.open() as fh:
            for r in csv.DictReader(fh):
                done.add((r["cell_id"], r["arm"], r["profile"], r["seed"]))
    todo = [j for j in jobs
            if (j[1]["cell_id"], j[0] if j[0] == "baseline" else "movement",
                j[3], str(j[4])) not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(jobs)} jobs in scope, {len(done)} rows already done, "
          f"{len(todo)} to run", flush=True)

    # The run-time environment facts the record must name (record §5).
    config = {
        "pre_registration": "docs/implementation/pipeline/ogasp/rate_feasibility_study.md",
        "horizon": HORIZON, "seeds": list(SEEDS),
        "mapping_version": MAPPING_VERSION, "overlay_version": OVERLAY_VERSION,
        "mtd_scheme": MTD_SCHEME, "anchor_bands": ANCHOR_BANDS,
        "interval_axis": [50, 100, 200, 400, 800], "erlang_k": ERLANG_K,
        "cells": {cid: _cell_meta(c) for cid, c in cells.items()},
    }
    with (_NUMBERS / "config.json").open("w") as fh:
        json.dump(config, fh, indent=2)

    new_file = not per_run.exists()
    t0 = time.perf_counter()
    with per_run.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS + ["_wall_s"])
        if new_file:
            writer.writeheader()
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(_run_job, j) for j in todo]
            for i, fut in enumerate(as_completed(futures), 1):
                row = fut.result()
                writer.writerow({k: row.get(k) for k in FIELDS + ["_wall_s"]})
                fh.flush()
                if i % 25 == 0 or i == len(todo):
                    rate = i / (time.perf_counter() - t0)
                    print(f"  {i}/{len(todo)} rows "
                          f"({rate:.2f}/s, ~{(len(todo) - i) / rate / 60:.0f} min left)",
                          flush=True)
    print(f"done in {(time.perf_counter() - t0) / 60:.1f} min -> {per_run}")


if __name__ == "__main__":
    main()
