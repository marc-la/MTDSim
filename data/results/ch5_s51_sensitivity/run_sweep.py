#!/usr/bin/env python3
"""The §5.1 sensitivity re-run: chapter 4's declared inputs, each moved across its
band, at the configuration chapter 5 reports.

Design: docs/handoffs/2026-09-17_ch5_s51_sensitivity_overhaul.md §D7. The two
sweeps on record (data/results/rate_feasibility_study, data/results/
s1_weight_sensitivity) ran at ten seeds, one scheme, on the pre-restoration
substrate, the second under the superseded fixed-dwell regime and around a
backward decay since re-cut. This run repeats their perturbations at the
defended corpus's pins (data/results/ch5_defended/run_corpus.py: v2_partial,
the failure-only overlay, retrace on, the targeted objective on the database
set, the quasi-periodic regime, 15 000 s, seeds 0-99) so that §5.1's numbers
are the chapter's numbers. Nothing is re-derived: every declared value is read
from the tracked catalogue and the declared kernel; the sweep moves a copy.

The points (22), on the movement arm only — the baseline consumes no declared
value:

  centre        the declared point, run rather than copied from the defended
                corpus so the analyser can check the two are bit-identical
                (SIM-05) before pooling anything
  dwell (8)     each of the four families at both ends of its catalogue band
                (rate_feasibility_study.py ANCHOR_BANDS: x0.5 / x2 for the
                scan-shaped, exploit-shaped and objective families; x0.25 / x4
                for low-and-slow), the family factor multiplying every tactic
                in the family with the per-tactic multipliers riding along
  shape (2)     the same-mean Erlang-4 draw on the low-and-slow family, at the
                centre and at low-and-slow x4 (the corner the record found)
  mapping (1)   the forced-total mapping v1_ckc_total at the declared point
  decay (10)    gamma in {0.1, 0.5}, delta_ratio in {0.1, 0.5}, z in {0, 0.05},
                one at a time from the declared (0.25, 0.25, 0.1); then the
                four corners of (gamma, delta_ratio) with z declared

Conditions: no defence (interval 0, run once); the random scheme over the
seven-mechanism pool at 200 s and at 2 000 s. Five profiles (the four
objectives and the aggregate). 22 x 5 x 100 x 3 = 33 000 runs.

CRITERION, fixed before the first run and not revised after a result is seen
(the record's discipline, weight_sensitivity_study.md §1):

  A point is INERT for a (profile set, condition) when the pooled mean of
  distinct hosts reached at the point lies inside the 95 % bootstrap interval
  of the centre at the same condition. It is MOVED otherwise, and the
  direction, the band-end means and their intervals are reported. The floor z
  is reported ZERO BY STRUCTURE if and only if its rows are bit-identical to
  the centre's (no profile net carries a three-stage edge). A family is inert
  when both its band ends are inert under every condition. The primary
  pooling is the four objective profiles (the chapter's arm set); the
  aggregate is read beside them, never pooled in. Intervals are the chapter's
  (seed bootstrap, 2 000 resamples, _ch5_style conventions).

    PYTHONPATH=src python data/results/ch5_s51_sensitivity/run_sweep.py [--smoke]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
OUT = HERE / "runs.jsonl"
SMOKE_OUT = HERE / "smoke.jsonl"
DESIGN = HERE / "design.json"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


# The three seams, imported rather than copied: the chapter's cell, the anchor
# arithmetic and Erlang source, and (lazily, in the worker) the kernel compiler.
corpus = _load("ch5_defended_run_corpus", RESULTS / "ch5_defended" / "run_corpus.py")
rate = _load("rate_feasibility_run_study", RESULTS / "rate_feasibility_study" / "run_study.py")

PROFILES = corpus.PROFILES
SEEDS = corpus.SEEDS
HORIZON = corpus.HORIZON
MAPPING = corpus.MAPPING
OVERLAY = corpus.OVERLAY
REGIME = "shifted"
OBJECTIVE = "targeted"
FAMILY_BANDS: dict[str, tuple[float, float]] = dict(rate.ANCHOR_BANDS)
LOW_AND_SLOW = "stealth-low-and-slow"
DECLARED_KERNEL = {"gamma": 0.25, "delta_ratio": 0.25, "z": 0.1}  # lifecycle_consensus.json; asserted at start
CONDITIONS: tuple[tuple[str, int], ...] = (("none", 0), ("random", 200), ("random", 2_000))


def build_points() -> list[dict]:
    pts: list[dict] = [{"name": "centre", "kind": "centre"}]
    for family, (lo, hi) in FAMILY_BANDS.items():
        for f in (lo, hi):
            pts.append({"name": f"dwell_{family}_x{f:g}", "kind": "dwell",
                        "family": family, "factor": f, "factors": {family: f}})
    pts.append({"name": "shape_erlang4", "kind": "shape", "timing": "erlang4"})
    pts.append({"name": "shape_erlang4_lowslow_x4", "kind": "shape", "timing": "erlang4",
                "factors": {LOW_AND_SLOW: 4.0}})
    pts.append({"name": "mapping_forced_total", "kind": "mapping", "mapping": "v1_ckc_total"})
    for g in (0.1, 0.5):
        pts.append({"name": f"decay_gamma_{g:g}", "kind": "decay", "kernel": {"gamma": g}})
    for d in (0.1, 0.5):
        pts.append({"name": f"decay_delta_{d:g}", "kind": "decay", "kernel": {"delta_ratio": d}})
    for z in (0.0, 0.05):
        pts.append({"name": f"decay_z_{z:g}", "kind": "decay", "kernel": {"z": z}})
    for g in (0.1, 0.5):
        for d in (0.1, 0.5):
            pts.append({"name": f"corner_gamma_{g:g}_delta_{d:g}", "kind": "corner",
                        "kernel": {"gamma": g, "delta_ratio": d}})
    return pts


def _assert_declared_kernel() -> None:
    """The declared point the sweep moves from must be the chapter's overlay's own
    recipe (the registry check has just shown the committed files follow from it)."""
    from mtdsim.l3_simulation.controller.outcome import load_overlay_registry

    entry = load_overlay_registry().get(OVERLAY)
    spec = entry.spec if isinstance(entry.spec, dict) else entry.spec.__dict__
    kernel = spec.get("kernel") or {}
    found = {k: float(kernel[k]) for k in ("gamma", "delta_ratio", "z")}
    if found != DECLARED_KERNEL:
        raise SystemExit(f"{OVERLAY} kernel {found} != the sweep's assumed centre {DECLARED_KERNEL}")


def _overlay_kwargs(point: dict) -> dict:
    """The chapter's overlay by name, or the same recipe with one kernel parameter moved."""
    kernel = point.get("kernel")
    if not kernel:
        return {"overlay_version": OVERLAY}
    from mtdsim.l3_simulation.controller.outcome import OutcomeOverlay, load_overlay_registry
    from mtdsim.l3_simulation.controller.rules import compile_values, load_rule_set, spec_from_registry_entry

    entry = load_overlay_registry().get(OVERLAY)
    entry_spec = entry.spec if isinstance(entry.spec, dict) else entry.spec.__dict__
    spec = spec_from_registry_entry(entry_spec).with_kernel(**kernel)
    values = compile_values(load_rule_set(), spec)
    return {"overlay": OutcomeOverlay.from_values(values, version=f"{OVERLAY}+{point['name']}")}


def run_one(job: dict) -> dict:
    from mtdsim.l3_simulation.movement.run import run_movement

    point = job["point"]
    scheme, strategies = corpus._strategies(job["condition"])
    kwargs: dict = {}
    if point.get("factors") or point.get("timing"):
        catalogue = rate._load_catalogue()
        means = rate.scaled_means(catalogue, point.get("factors", {}))
        kwargs["dwell_catalogue"] = means
        if point.get("timing") == "erlang4":
            kwargs["timing"] = rate.ErlangGroupTiming(
                means, rate.stealth_tactics(catalogue), seed=job["seed"], k=4)
    r = run_movement(
        job["profile"],
        seed=job["seed"],
        with_synthetic_overlay=True,
        horizon=HORIZON,
        mapping_version=point.get("mapping", MAPPING),
        retrace_sinks=True,
        mtd_scheme=scheme,
        mtd_interval=(job["interval"] or None),
        custom_strategies=strategies,
        substrate_timing_regime=REGIME,
        attack_objective=OBJECTIVE,
        target_layer=None,
        **_overlay_kwargs(point),
        **kwargs,
    )
    recs = r.records
    action = [x for x in recs if x.verb]
    return {
        "point": point["name"], "kind": point["kind"],
        "profile": job["profile"], "condition": job["condition"],
        "interval": job["interval"], "seed": job["seed"],
        "termination_time": float(r.termination_time),
        "compromised": int(r.compromised_count),
        "reached_objective": bool(r.reached_objective),
        "database_hosts_reached": int(r.database_hosts_reached),
        "first_database_reach_time": r.first_database_reach_time,
        "n_records": len(recs),
        "n_actions": len(action),
        "n_blocked": sum(1 for x in action if x.blocked),
        "n_success": sum(1 for x in action if x.verdict == "success"),
        "n_interrupted": sum(1 for x in recs if x.interrupted),
        "retrace_count": int(r.retrace_count),
        "mtd_count": len(r.mtd_executions),
        "mtd_attack_interrupted": int(r.mtd_attack_interrupted),
    }


def dispatch(job: dict) -> dict:
    import contextlib
    import io

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return run_one(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {"error": f"{type(exc).__name__}: {exc}", "point": job["point"]["name"],
                "profile": job["profile"], "condition": job["condition"],
                "interval": job["interval"], "seed": job["seed"]}


def build_jobs(points: list[dict], seeds, profiles) -> list[dict]:
    return [
        {"point": p, "profile": prof, "condition": c, "interval": i, "seed": s}
        for s in seeds for p in points for prof in profiles for (c, i) in CONDITIONS
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--smoke", action="store_true",
                        help="one seed, one profile, every point and condition; writes smoke.jsonl")
    args = parser.parse_args(argv)

    _assert_declared_kernel()
    points = build_points()
    if args.smoke:
        seeds, profiles, out = (0,), ("objective_impact",), SMOKE_OUT
    else:
        seeds, profiles, out = SEEDS, PROFILES, OUT
        DESIGN.write_text(json.dumps({
            "pins": {"mapping": MAPPING, "overlay": OVERLAY, "regime": REGIME,
                     "objective": OBJECTIVE, "horizon": HORIZON, "seeds": list(SEEDS),
                     "profiles": list(PROFILES), "conditions": list(CONDITIONS),
                     "declared_kernel": DECLARED_KERNEL, "family_bands": FAMILY_BANDS},
            "points": points,
            "criterion": __doc__.split("CRITERION", 1)[1].split("PYTHONPATH", 1)[0].strip(),
        }, indent=2) + "\n", encoding="utf-8")
    jobs = build_jobs(points, seeds, profiles)
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    print(f"{len(jobs)} runs ({len(points)} points) on {workers} workers -> {out}", flush=True)
    started = time.time()
    done = errors = 0
    with out.open("w", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(dispatch, jobs, chunksize=(1 if args.smoke else 16)):
            fh.write(json.dumps(row) + "\n")
            done += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if done % 1000 == 0:
                print(f"  {done}/{len(jobs)}  {time.time() - started:.0f}s", flush=True)
    print(f"done: {done} runs, {errors} errors, {time.time() - started:.0f}s", flush=True)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
