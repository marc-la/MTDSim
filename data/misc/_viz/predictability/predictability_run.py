"""Predictability study — the arms runner.

Executes the predictability.md design (pre-registered before this file produced a
row): the conditional composition, per decision state, of each attack model's own
policy, on matched seeds, modulators null, no MTD, v2_partial, sink policy retrace
(the plural_preference configuration; §The reported-configuration pin). Nothing here
chooses a value — the design, the pins and the predictions are fixed in
docs/implementation/pipeline/ogasp/predictability.md. This runner only simulates and
records the per-run conditional compositions; predictability_analyse.py reads the
record and computes N/D/E/P, D_policy, the census, the calibration ladder, the
declared layer and the decompositions.

The four arms:

  - baseline    : the inherited 6-phase FSM. Its conditional composition is
                  reconstructed from attack-operation rows (measures.fsm_*). P=1 is a
                  constructed fact (deterministic policy); this arm is the reader's
                  self-test and the marginal-trap demonstration.
  - corpus      : the shipped movement attacker (corpus-weighted routing). The headline.
  - uniform_null: the movement attacker with each place's out-distribution flattened
                  over its reachable set — topology kept, corpus preference stripped.
  - verdict_blind: the movement attacker with an empty overlay, so the verdict never
                  conditions routing — the null for the per-verdict decomposition
                  (its success and failure slices are identical by construction).

Per movement run we persist the conditional composition keyed "place|verdict" ->
{next_place: count}; for the baseline we persist the FSM decision stream. The
analysis re-slices without re-simulating (the plural_preference pattern).

    PYTHONPATH=src python data/misc/_viz/predictability/predictability_run.py --mode convergence --max-seeds 120
    PYTHONPATH=src python data/misc/_viz/predictability/predictability_run.py --mode arms --seeds 100 --workers 6
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

# -- the design (pre-registration; predictability.md) -------------------------
MAPPING = "v2_partial"
OVERLAY = "v3_persistent_backward"
HORIZON = 15_000
RETRACE = True
PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
MOVEMENT_ARMS = ("corpus", "uniform_null", "verdict_blind")


def _movement_composition(result) -> dict[str, dict[str, int]]:
    """The per-run realised conditional composition, JSON-safe: the tuple state
    key (place, verdict) flattened to "place|verdict". Only routed records (a
    next-move choice was made) contribute — measures.conditional_composition."""
    from mtdsim.l3_simulation.movement import measures as M

    comp = M.conditional_composition(result)
    out: dict[str, dict[str, int]] = {}
    for (place, verdict), counts in comp.items():
        out[f"{place}|{verdict}"] = dict(counts)
    return out


def _movement_retrace_stats(result) -> dict:
    """Retrace bookkeeping: how many routed records were retrace steps, whose
    realised next-place is drawn from a base out-set with one edge suppressed
    (the one hidden variable beyond (place, verdict); reported, not hidden)."""
    routed = [r for r in result.records if r.next_place is not None]
    return {
        "n_routed": len(routed),
        "n_retrace": sum(1 for r in routed if r.retrace),
    }


def run_movement_cell(job: dict) -> dict:
    from mtdsim.l3_simulation.controller import verdict_blind_overlay
    from mtdsim.l3_simulation.movement.run import run_movement

    arm = job["arm"]
    kwargs = dict(
        seed=job["seed"],
        horizon=HORIZON,
        mapping_version=MAPPING,
        retrace_sinks=RETRACE,
    )
    if arm == "verdict_blind":
        # the ablation is an overlay object, not a registry version name
        kwargs["overlay"] = verdict_blind_overlay()
    else:
        kwargs["overlay_version"] = OVERLAY
        kwargs["uniform_weights"] = (arm == "uniform_null")
    result = run_movement(job["profile"], **kwargs)
    return {
        "arm": arm, "profile": job["profile"], "seed": job["seed"],
        "composition": _movement_composition(result),
        "retrace": _movement_retrace_stats(result),
        "n_records": len(result.records),
        "reached": bool(result.reached_objective),
        "hosts": int(result.compromised_count),
    }


def run_baseline_cell(job: dict) -> dict:
    """The inherited 6-phase attacker (no MTD), constructed exactly as
    plural_preference's baseline arm. Persist its FSM decision stream so the
    analyser reads the (phase) marginal and the (phase, branch) conditioning
    ladder without re-simulating."""
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
    decisions = M.fsm_decisions(rows)
    stream = [
        {"phase": d.phase, "branch": d.branch, "successor": d.successor}
        for d in decisions
    ]
    return {
        "arm": "baseline", "profile": "baseline", "seed": seed,
        "decisions": stream,
        "n_records": len(rows),
        "reached": bool(end_event.triggered),
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
# Mode: convergence (P3) — how many seeds does the conditional signature need?
# ---------------------------------------------------------------------------

_P_TOL = 0.02        # predictability must have settled on the last two rungs
_DPOLICY_TOL = 0.1   # ... and the effective breadth


def convergence(max_seeds: int, workers: int, step: int = 20) -> dict:
    """P3: is the corpus arm's aggregate predictability stable by the seed budget,
    per profile, on the pooled growth ladder (the plural_preference P3 discipline —
    a pooled ladder, not a two-halves crossing that false-passes an undersampled
    process)?"""
    from mtdsim.l3_simulation.movement import measures as M

    jobs = [{"arm": "corpus", "profile": p, "seed": s}
            for p in PROFILES for s in range(max_seeds)]
    rows = _map(jobs, workers)
    rows = [r for r in rows if "error" not in r]
    by_profile: dict[str, list[dict]] = {}
    for r in rows:
        by_profile.setdefault(r["profile"], []).append(r)

    def pooled_report(subset):
        pooled: dict[tuple, Counter] = {}
        for r in subset:
            for key, counts in r["composition"].items():
                place, verdict = key.split("|", 1)
                pooled.setdefault((place, verdict), Counter()).update(counts)
        return M.predictability_report(pooled, arm="corpus", profile="_")

    ladder = list(range(step, max_seeds + 1, step))
    report: dict = {
        "max_seeds": max_seeds, "arm": "corpus",
        "criterion": "pooled growth ladder; stabilised = last-two-rung "
                     "|ΔP| ≤ 0.02 AND |ΔD_policy| ≤ 0.1",
        "ladder": ladder, "profiles": {},
    }
    for profile, subset in by_profile.items():
        subset.sort(key=lambda r: r["seed"])
        series = []
        for n in ladder:
            rep = pooled_report(subset[:n])
            series.append({"n": n, "P": round(rep.predictability, 4),
                           "D_policy": round(rep.d_policy, 4),
                           "states": rep.n_states})
        stabilised = (
            len(series) >= 2
            and abs(series[-1]["P"] - series[-2]["P"]) <= _P_TOL
            and abs(series[-1]["D_policy"] - series[-2]["D_policy"]) <= _DPOLICY_TOL
        )
        report["profiles"][profile] = {
            "stabilised": stabilised,
            "P_full": series[-1]["P"], "D_policy_full": series[-1]["D_policy"],
            "last_step_dP": round(abs(series[-1]["P"] - series[-2]["P"]), 4),
            "last_step_dD": round(abs(series[-1]["D_policy"] - series[-2]["D_policy"]), 4),
            "series": series,
        }
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("convergence", "arms"), required=True)
    ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--max-seeds", type=int, default=120)
    ap.add_argument("--workers", type=int,
                    default=max(1, (os.cpu_count() or 4) - 2))
    args = ap.parse_args()

    if args.mode == "convergence":
        report = convergence(args.max_seeds, args.workers)
        (HERE / "pred_convergence.json").write_text(json.dumps(report, indent=2))
        print("convergence (corpus) — pooled growth ladder:")
        for profile, d in report["profiles"].items():
            flag = "STABLE  " if d["stabilised"] else "DRIFTING"
            print(f"  {profile:32} {flag}  P={d['P_full']:.4f}  "
                  f"D_policy={d['D_policy_full']:.3f}  "
                  f"(last ΔP={d['last_step_dP']:.4f}, ΔD={d['last_step_dD']:.3f})")
        print(f"\nwrote {HERE / 'pred_convergence.json'}")
        return 0

    jobs = build_jobs(range(args.seeds))
    print(f"{len(jobs)} runs ({args.seeds} seeds × "
          f"[baseline + {len(MOVEMENT_ARMS)}×{len(PROFILES)}]) "
          f"over {args.workers} workers", flush=True)
    rows = _map(jobs, args.workers)
    errors = [r for r in rows if "error" in r]
    with (HERE / "pred_runs.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    (HERE / "pred_design.json").write_text(json.dumps({
        "study": "predictability",
        "mapping_version": MAPPING, "overlay_version": OVERLAY,
        "horizon": HORIZON, "sink_policy": "retrace",
        "modulators": "null", "mtd": "none",
        "seeds": args.seeds, "profiles": list(PROFILES),
        "arms": ["baseline", *MOVEMENT_ARMS],
        "pre_registration":
            "docs/implementation/pipeline/ogasp/predictability.md",
        "total_runs": len(jobs), "errors": len(errors),
    }, indent=2))
    print(f"wrote {HERE / 'pred_runs.jsonl'} ({len(rows)} rows, "
          f"{len(errors)} errors)", flush=True)
    if errors:
        print("ERRORS:", errors[:3])
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
