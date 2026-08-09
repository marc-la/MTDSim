"""Plural-preference study — the three-arm simulation runner.

Executes the plural_preference.md design: three arms on matched seeds, modulators
null, no MTD, v2_partial, sink policy retrace (the reported plurality
configuration; §4 pin). Nothing here chooses a value — the design, the pins and
the pre-registered predictions are fixed in
docs/implementation/pipeline/ogasp/plural_preference.md before this file produced
a row. This runner only simulates and records; plural_preference_analyse.py reads
the record and computes the Hill/evenness/alignment measures, the bootstrap CIs
and the verdicts.

The three arms (the first two are movement-vocabulary; the baseline has none):

  - baseline     : the inherited 6-phase FSM — one deterministic scripted rule.
                   Structural D=1 on the movement-vocabulary dimensions; a real
                   verb-mix (the one dimension it shares with the movement arm).
  - uniform_null : the movement attacker with each place's out-distribution
                   flattened to equiprobable over its reachable set — topology
                   kept, corpus preference stripped (uniform_weight_variant).
  - corpus       : the shipped movement attacker (corpus-weighted routing).

Per-run we persist the counts every dimension and both success-alignments read
from, so the analysis re-slices without re-simulating (the reconcile.py pattern):
place sequence, realised edges, verb attempts+successes, place visits, terminal.

    PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_run.py --mode convergence
    PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_run.py --mode arms --seeds 80 --workers 6
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# -- the design (pre-registration; plural_preference.md §Design) --------------
MAPPING = "v2_partial"
OVERLAY = "v3_persistent_backward"
HORIZON = 15_000
RETRACE = True  # sink policy retrace (experiment 2's, the badge's own convention)
PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
# baseline is profile-independent (the inherited attacker has no profile); it is
# run once per seed and compared as the structural one-rule anchor.
MOVEMENT_ARMS = ("corpus", "uniform_null")


def _summarise_movement(result) -> dict:
    """The per-run behaviour summary the five dimensions + both alignments read."""
    from mtdsim.l3_simulation.movement import measures as M

    sequence = [r.place for r in result.records]
    edges: Counter[str] = Counter()
    for rec in result.records:
        if rec.next_place is not None:
            edges[f"{rec.place}>{rec.next_place}"] += 1
    actions = M.action_records(result)
    verb_attempts = Counter(r.verb for r in actions)
    verb_successes = Counter(r.verb for r in actions if r.verdict == "success")
    visits = Counter(r.place for r in M.visit_records(result))
    terminal = sequence[-1] if sequence else None
    return {
        "sequence": sequence,
        "edges": dict(edges),
        "verb_attempts": dict(verb_attempts),
        "verb_successes": dict(verb_successes),
        "visits": dict(visits),
        "terminal": terminal,
        "hosts": int(result.compromised_count),
        "reached": bool(result.reached_objective),
        "n_records": len(result.records),
    }


def run_movement_cell(job: dict) -> dict:
    from mtdsim.l3_simulation.movement.run import run_movement

    result = run_movement(
        job["profile"],
        seed=job["seed"],
        horizon=HORIZON,
        mapping_version=MAPPING,
        overlay_version=OVERLAY,
        retrace_sinks=RETRACE,
        uniform_weights=(job["arm"] == "uniform_null"),
        # modulators null (attacker_state=None), no MTD (mtd_scheme=None): the
        # §4-pinned reported configuration.
    )
    return {"arm": job["arm"], "profile": job["profile"], "seed": job["seed"],
            **_summarise_movement(result)}


def run_baseline_cell(job: dict) -> dict:
    """The inherited 6-phase attacker, constructed exactly as experiment 2's
    baseline arm (no MTD). It has no place vocabulary, so only its verb mix is a
    real distribution; the movement-vocabulary dimensions are structural for it."""
    import random

    import numpy as np
    import simpy

    from mtdnetwork.component.adversary import Adversary
    from mtdnetwork.component.time_network import TimeNetwork
    from mtdnetwork.data.constants import ATTACKER_THRESHOLD
    from mtdnetwork.operation.attack_operation import AttackOperation

    from mtdsim.l3_simulation.movement import measures as M
    from mtdsim.l3_simulation.movement.run import GEOMETRY

    seed = job["seed"]
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0
    )
    attack_op.proceed_attack()
    env.run(until=HORIZON)

    rows = adversary.get_attack_stats().get_record()
    led = M.baseline_ledger(rows)
    return {
        "arm": "baseline", "profile": "baseline", "seed": seed,
        # the one dimension the baseline shares — its native verb mix (no verdict
        # in the native record, so no per-verb success rate for this arm).
        "verb_attempts": dict(led.attempts_by_verb),
        "verb_successes": {},
        "hosts": int(led.n_distinct_hosts),
        "reached": bool(end_event.triggered),
        "n_records": int(led.n_actions),
    }


def _dispatch(job: dict) -> dict:
    try:
        if job["arm"] == "baseline":
            return run_baseline_cell(job)
        return run_movement_cell(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {"arm": job["arm"], "profile": job.get("profile"),
                "seed": job.get("seed"), "error": f"{type(exc).__name__}: {exc}"}


def build_jobs(seeds: range) -> list[dict]:
    jobs: list[dict] = []
    for seed in seeds:
        jobs.append({"arm": "baseline", "profile": "baseline", "seed": seed})
        for arm in MOVEMENT_ARMS:
            for profile in PROFILES:
                jobs.append({"arm": arm, "profile": profile, "seed": seed})
    return jobs


def _map(jobs, workers):
    if workers <= 1:
        return [_dispatch(j) for j in jobs]
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_dispatch, jobs, chunksize=4))


# ---------------------------------------------------------------------------
# Mode: convergence (P3) — how many seeds does the plurality signature need?
# ---------------------------------------------------------------------------


# P3 stabilisation tolerances on the pooled growth ladder's last two steps.
_D_TOL = 0.2       # the handoff's ±0.2 on the effective number
_EVEN_TOL = 0.02   # evenness must also have settled (D can grow with N while the
                   # ratio stabilises; the ratio is what the contrast reads)


def convergence(max_seeds: int, workers: int, step: int = 20) -> dict:
    """P3: is each dimension's plurality signature *stable* by the seed budget, on
    the corpus arm of the richest profile (aggregate)?

    The honest check is the **pooled growth ladder**, not a two-halves crossing:
    for a per-run dimension whose support keeps growing, two equal-size samples
    always roughly agree (low variance), which reads as false convergence while the
    pooled estimate still drifts. So D and evenness are computed on the pooled
    first-``n`` runs up a ladder, and a dimension is ``stabilised`` when the last
    two rungs move less than the tolerances (|ΔD| ≤ 0.2 AND |Δevenness| ≤ 0.02).
    A per-run dimension that never stabilises inside the budget has its
    distribution-*shape* verdict withheld — its variety *count* still stands."""
    from mtdsim.l3_simulation.movement import measures as M

    jobs = [{"arm": "corpus", "profile": "aggregate", "seed": s}
            for s in range(max_seeds)]
    rows = _map(jobs, workers)
    rows = [r for r in rows if "error" not in r]
    rows.sort(key=lambda r: r["seed"])

    def pooled_hill(subset, dimension, k=5):
        counts: Counter = Counter()
        for r in subset:
            if dimension == "opening":
                counts[tuple(r["sequence"][:k])] += 1
            elif dimension == "terminal":
                counts[r["terminal"]] += 1
            elif dimension == "verb":
                counts.update(r["verb_attempts"])
            elif dimension == "visit":
                counts.update(r["visits"])
            elif dimension == "transition":
                counts.update(r["edges"])
        return M.hill_diversity(counts)

    ladder = list(range(step, max_seeds + 1, step))
    report: dict = {
        "max_seeds": max_seeds, "profile": "aggregate", "arm": "corpus",
        "criterion": "pooled growth ladder; stabilised = last-two-rung "
                     "|ΔD| ≤ 0.2 AND |Δevenness| ≤ 0.02",
        "ladder": ladder, "dimensions": {},
    }
    for dim in M.PLURAL_DIMENSIONS:
        series = []
        for n in ladder:
            hd = pooled_hill(rows[:n], dim)
            series.append({"n": n, "N": hd.support_n,
                           "D": round(hd.effective_number, 3),
                           "evenness": round(hd.evenness, 3)})
        # stabilised iff the last two rungs are within tolerance (and there ARE two)
        stabilised = (
            len(series) >= 2
            and abs(series[-1]["D"] - series[-2]["D"]) <= _D_TOL
            and abs(series[-1]["evenness"] - series[-2]["evenness"]) <= _EVEN_TOL
        )
        report["dimensions"][dim] = {
            "stabilised": stabilised,
            "N_full": series[-1]["N"], "D_full": series[-1]["D"],
            "evenness_full": series[-1]["evenness"],
            "last_step_dD": round(abs(series[-1]["D"] - series[-2]["D"]), 3),
            "last_step_devenness": round(
                abs(series[-1]["evenness"] - series[-2]["evenness"]), 3),
            "series": series,
        }
    return report


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("convergence", "arms"), required=True)
    ap.add_argument("--seeds", type=int, default=80)
    ap.add_argument("--max-seeds", type=int, default=120)
    ap.add_argument("--workers", type=int,
                    default=max(1, (os.cpu_count() or 4) - 2))
    args = ap.parse_args()

    if args.mode == "convergence":
        report = convergence(args.max_seeds, args.workers)
        (HERE / "pp_convergence.json").write_text(json.dumps(report, indent=2))
        print("convergence (corpus / aggregate) — pooled growth ladder:")
        for dim, d in report["dimensions"].items():
            flag = "STABLE  " if d["stabilised"] else "DRIFTING"
            print(f"  {dim:11} {flag}  N={d['N_full']:3}  D={d['D_full']:6.2f}  "
                  f"evenness={d['evenness_full']:.3f}  "
                  f"(last-step ΔD={d['last_step_dD']:.3f}, "
                  f"Δeven={d['last_step_devenness']:.3f})")
        print(f"\nwrote {HERE / 'pp_convergence.json'}")
        return 0

    jobs = build_jobs(range(args.seeds))
    print(f"{len(jobs)} runs ({args.seeds} seeds × "
          f"[baseline + {len(MOVEMENT_ARMS)}×{len(PROFILES)}]) "
          f"over {args.workers} workers", flush=True)
    rows = _map(jobs, args.workers)
    errors = [r for r in rows if "error" in r]
    with (HERE / "pp_runs.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    (HERE / "pp_design.json").write_text(json.dumps({
        "study": "plural_preference",
        "mapping_version": MAPPING, "overlay_version": OVERLAY,
        "horizon": HORIZON, "sink_policy": "retrace",
        "modulators": "null", "mtd": "none",
        "seeds": args.seeds, "profiles": list(PROFILES),
        "arms": ["baseline", *MOVEMENT_ARMS],
        "pre_registration":
            "docs/implementation/pipeline/ogasp/plural_preference.md",
        "total_runs": len(jobs), "errors": len(errors),
    }, indent=2))
    print(f"wrote {HERE / 'pp_runs.jsonl'} ({len(rows)} rows, "
          f"{len(errors)} errors)", flush=True)
    if errors:
        print("ERRORS:", errors[:3])
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
