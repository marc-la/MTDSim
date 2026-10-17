"""The tactic-durations ablation (Marc 2026-10-12; handoff
docs/implementation/run_plans/2026-10-11_ch6_1_redraft_scrutiny.md §24.2) — the run half.

Section 6.1 explains most of the APT attacker model's differences from the
baseline attacker with no MTD by two causes, its tactic durations and the order
of its tactics, and no run had removed either. The order of its tactics is the
Petri net, so it is not removed; the baseline attacker is the run without it.
This script removes the tactic durations in two steps, everything else at the
reported corpus's pins (ch5_s531_unopposed/run_corpus.py REPORTED=1: v2_partial,
the failure-only overlay, retrace on, the targeted attack scenario, 15 000 s,
no MTD, the vulnerability memory at rate 2, seeds 0-999):

  centre          the declared catalogue, passed explicitly; seeds 0-19 only, to
                  check the runs are bit-identical to runs_reported.jsonl before
                  anything is read (the override path changes nothing by itself)
  unmapped_zero   Arm A: the seven unmapped tactics take no time (mean 0, an
                  immediate transition); the mapped tactics keep their declared
                  means
  baseline_pace   Arm B: Arm A, and each mapped tactic's mean set to the
                  baseline attacker's mean time for the attack action it
                  dispatches (from its own records in the reported corpus,
                  further_analyses_numbers.json f7.baseline_mean_time_s). The
                  APT attacker model then runs at the baseline attacker's pace;
                  what remains of the gap comes from the order of its tactics
                  (with the failure matrix and the vulnerability memory, which
                  Section 5.4 finds negligible on NCR). The draw stays
                  exponential about that mean; the baseline attacker's times are
                  fixed per attack action (EXPLOIT_VULN per vulnerability).

The movement layer's draw IS the attack action's time (attacker.py docstring,
S3-R: the substrate's ATTACK_DURATION is not consumed on this arm; checked on
the reported records, end - start - dwell = 0 for every action-bearing record),
so setting a mapped tactic's mean sets its attack action's time.

Four attack profiles (c1-c4); the aggregate is in no §6.1 claim. The baseline
attacker is not re-run: it consumes no tactic duration, so its rows in
runs_reported.jsonl are its rows here.

    PYTHONPATH=src python experiments/ch6_further_analyses/run_duration_ablation.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "runs_duration_ablation.jsonl"
REPORTED = ROOT / "experiments/ch5_s531_unopposed/runs_reported.jsonl"
NUMBERS = HERE / "further_analyses_numbers.json"

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
)
SEEDS = tuple(range(1_000))
CENTRE_SEEDS = tuple(range(20))
MAPPING = "v2_partial"
OVERLAY = "v4_failure_only"
MEMORY_RATE = 2.0
HORIZON = 15_000


def catalogues() -> dict[str, dict[str, float]]:
    """centre / unmapped_zero / baseline_pace, each tactic -> mean seconds."""
    from mtdsim.l3_simulation.controller import load_controller
    from mtdsim.l3_simulation.movement import load_dwell_catalogue

    declared = load_dwell_catalogue()
    controller = load_controller(version=MAPPING)
    verb_of = {t: controller.phase_for(t) for t in declared}
    unmapped = {t for t, v in verb_of.items() if v is None}
    assert unmapped == {
        "resource-development", "persistence", "stealth", "defense-impairment",
        "collection", "exfiltration", "impact",
    }, unmapped
    base_time = json.loads(NUMBERS.read_text())["f7"]["baseline_mean_time_s"]
    a = {t: (0.0 if t in unmapped else m) for t, m in declared.items()}
    b = {t: (0.0 if t in unmapped else float(base_time[verb_of[t]])) for t in declared}
    return {"centre": dict(declared), "unmapped_zero": a, "baseline_pace": b}


def _movement(job: dict) -> dict:
    from mtdsim.l3_simulation.movement.run import run_movement

    r = run_movement(
        job["profile"],
        seed=job["seed"],
        with_synthetic_overlay=True,
        horizon=HORIZON,
        mapping_version=MAPPING,
        overlay_version=OVERLAY,
        retrace_sinks=True,
        mtd_scheme=None,
        mtd_interval=None,
        attack_objective="targeted",
        target_layer=None,
        exploit_learning_rate=MEMORY_RATE,
        dwell_catalogue=job["catalogue"],
    )
    return {
        "arm": "movement", "variant": job["variant"], "profile": job["profile"],
        "objective": "targeted", "horizon": HORIZON, "seed": job["seed"],
        "exploit_learning_rate": MEMORY_RATE,
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


_CATALOGUES: dict | None = None


def job_from_row(row: dict) -> dict:
    """The job a recorded row came from (rows do not carry the duration catalogue);
    used by experiments/verify_ledgers.py."""
    global _CATALOGUES
    if _CATALOGUES is None:
        _CATALOGUES = catalogues()
    return {"variant": row["variant"], "profile": row["profile"], "seed": row["seed"],
            "catalogue": _CATALOGUES[row["variant"]]}


def dispatch(job: dict) -> dict:
    try:
        return _movement(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {"error": f"{type(exc).__name__}: {exc}",
                **{k: v for k, v in job.items() if k != "catalogue"}}


def check_centre(rows: list[dict]) -> None:
    """The centre rows must equal runs_reported.jsonl's on every recorded field."""
    want = {(r["profile"], r["seed"]): r for r in rows}
    keys = ("compromised", "reached_objective", "database_hosts_reached",
            "first_database_reach_time", "termination_time", "records")
    seen = 0
    with REPORTED.open() as fh:
        for line in fh:
            ref = json.loads(line)
            k = (ref["profile"], ref["seed"])
            if ref["arm"] == "baseline" or k not in want:
                continue
            got = want[k]
            for f in keys:
                if got[f] != ref[f]:
                    raise SystemExit(f"centre differs from the reported corpus at {k}, field {f}")
            seen += 1
    if seen != len(want):
        raise SystemExit(f"centre: {seen} of {len(want)} rows matched in the reported corpus")
    print(f"centre: {seen} runs bit-identical to runs_reported.jsonl", flush=True)


def main() -> int:
    cats = catalogues()
    print(json.dumps({k: v for k, v in cats.items() if k != "centre"}, indent=1), flush=True)
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    seeds = range(int(os.environ.get("SEEDS", len(SEEDS))))

    centre_jobs = [{"variant": "centre", "profile": p, "seed": s, "catalogue": cats["centre"]}
                   for s in CENTRE_SEEDS for p in PROFILES]
    with ProcessPoolExecutor(workers) as pool:
        centre = list(pool.map(dispatch, centre_jobs, chunksize=4))
    if any("error" in r for r in centre):
        raise SystemExit(f"centre errors: {[r for r in centre if 'error' in r][:3]}")
    check_centre(centre)

    jobs = [{"variant": v, "profile": p, "seed": s, "catalogue": cats[v]}
            for v in ("unmapped_zero", "baseline_pace") for s in seeds for p in PROFILES]
    print(f"{len(jobs)} runs on {workers} workers -> {OUT}", flush=True)
    started = time.time()
    done = errors = 0
    with OUT.open("w", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(dispatch, jobs, chunksize=8):
            fh.write(json.dumps(row) + "\n")
            done += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if done % 500 == 0:
                print(f"  {done}/{len(jobs)}  {time.time() - started:.0f}s", flush=True)
    print(f"done: {done} runs, {errors} errors, {time.time() - started:.0f}s")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
