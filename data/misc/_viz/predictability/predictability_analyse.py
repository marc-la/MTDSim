"""Predictability study — the analyser.

Reads pred_runs.jsonl (deterministic per-run records) and computes the five layers
of predictability.md, emitting pred_results.json for the figure script and the
record. Nothing here simulates; every number is a re-read of the recorded runs.

  0. census      — decision-state visitation per profile × arm × state, with the
                   per-verdict count at verdict-carrying places, and the sparsity
                   ruling (cells below the census floor named unestimable).
  1. calibration — the FSM as the reader's self-test: the (phase) marginal reads
                   plural (the reader is not rigged to return 1); the (phase, branch)
                   conditioning collapses the resolvable plurality toward the
                   constructed P=1; the residual is FSM-internal state the attack
                   record under-exposes (design fact 2's trap), and P=1 stands as a
                   construct (the reader returns exactly 1 on the deterministic
                   transition table, checked here).
  2. declared    — run-free: overlay.compose over each profile's net, per state.
  3. realised    — the headline: per profile per arm, aggregate P and D_policy over
                   the pooled conditional composition, with per-seed bootstrap CIs.
  4. decomposition — per-verdict slice JSD (success vs failure composition) against
                   the verdict-blind null; corpus vs uniform-null predictability.

    PYTHONPATH=src python data/misc/_viz/predictability/predictability_analyse.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np

from mtdsim.l3_simulation.controller import load_outcome_overlay
from mtdsim.l3_simulation.movement import measures as M
from mtdsim.l3_simulation.movement.net import load_routing_net

HERE = Path(__file__).resolve().parent
PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
OVERLAY = "v3_persistent_backward"
MOVEMENT_ARMS = ("corpus", "uniform_null", "verdict_blind")
BOOT = 2000
Q_LO, Q_HI = 2.5, 97.5


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------


def load_runs() -> list[dict]:
    rows = [json.loads(ln) for ln in (HERE / "pred_runs.jsonl").read_text().splitlines()]
    return [r for r in rows if "error" not in r]


def _state(key: str) -> tuple[str, str]:
    place, verdict = key.split("|", 1)
    return (place, verdict)


def movement_comp(run: dict) -> dict[tuple, Counter]:
    """One movement run's conditional composition, de-serialised."""
    return {_state(k): Counter(v) for k, v in run["composition"].items()}


def pooled_comp(runs: list[dict]) -> dict[tuple, Counter]:
    pooled: dict[tuple, Counter] = {}
    for r in runs:
        for state, counts in movement_comp(r).items():
            pooled.setdefault(state, Counter()).update(counts)
    return pooled


def by_arm_profile(runs: list[dict]) -> dict[tuple[str, str], list[dict]]:
    groups: dict[tuple[str, str], list[dict]] = {}
    for r in runs:
        groups.setdefault((r["arm"], r["profile"]), []).append(r)
    return groups


# ---------------------------------------------------------------------------
# 0. census
# ---------------------------------------------------------------------------


def census(runs: list[dict]) -> dict:
    groups = by_arm_profile(runs)
    out: dict = {"floor": M._MIN_CELL_VISITS, "cells": {}}
    for arm in ("corpus", "uniform_null", "verdict_blind"):
        for profile in PROFILES:
            comp = pooled_comp(groups.get((arm, profile), []))
            rep = M.predictability_report(comp, arm=arm, profile=profile)
            verdict_carrying = sorted({
                s[0] for s in comp if s[1] in ("success", "failure")
            })
            out["cells"][f"{arm}/{profile}"] = {
                "n_states": rep.n_states,
                "n_decisions": rep.n_decisions,
                "n_unestimable": len(rep.unestimable_states),
                "unestimable": ["|".join(s) for s in rep.unestimable_states],
                "n_verdict_carrying_places": len(verdict_carrying),
                "min_cell": min((c.n for c in rep.cells), default=0),
                "median_cell": int(np.median([c.n for c in rep.cells]))
                if rep.cells else 0,
            }
    return out


# ---------------------------------------------------------------------------
# 1. calibration — the FSM self-test and conditioning ladder
# ---------------------------------------------------------------------------


def _fsm_comp_from_decisions(runs: list[dict], by: str) -> dict[tuple, Counter]:
    comp: dict[tuple, Counter] = {}
    for r in runs:
        for d in r["decisions"]:
            if d["successor"] is None:
                continue
            key = (d["phase"], d["branch"]) if by == "phase_branch" else (d["phase"],)
            comp.setdefault(key, Counter())[d["successor"]] += 1
    return comp


def calibration(runs: list[dict]) -> dict:
    baseline = [r for r in runs if r["arm"] == "baseline"]
    marginal = _fsm_comp_from_decisions(baseline, "phase")
    branched = _fsm_comp_from_decisions(baseline, "phase_branch")
    rep_marg = M.predictability_report(marginal, arm="baseline", profile="baseline")
    rep_br = M.predictability_report(branched, arm="baseline", profile="baseline")

    # the reader's self-test: fed the deterministic FSM transition table, the reader
    # must return exactly N=1, D=1, P=1 (design fact 1). This is what "P=1 by
    # construction" means operationally.
    table = {
        ("SCAN_HOST", "found"): Counter({"ENUM_HOST": 1}),
        ("ENUM_HOST", "already_compromised"): Counter({"ENUM_HOST": 1}),
        ("ENUM_HOST", "fresh"): Counter({"SCAN_PORT": 1}),
        ("SCAN_PORT", "reuse"): Counter({"SCAN_NEIGHBOR": 1}),
        ("SCAN_PORT", "no_reuse"): Counter({"EXPLOIT_VULN": 1}),
        ("EXPLOIT_VULN", "compromised"): Counter({"SCAN_NEIGHBOR": 1}),
        ("EXPLOIT_VULN", "uncompromised"): Counter({"BRUTE_FORCE": 1}),
        ("BRUTE_FORCE", "compromised"): Counter({"SCAN_NEIGHBOR": 1}),
        ("BRUTE_FORCE", "not"): Counter({"ENUM_HOST": 1}),
        ("SCAN_NEIGHBOR", ""): Counter({"ENUM_HOST": 1}),
    }
    rep_table = M.predictability_report(table, arm="baseline", profile="constructed")

    def plural_cells(comp):
        return {"|".join(s): dict(c) for s, c in comp.items() if len(c) > 1}

    return {
        "constructed_table": {
            "P": round(rep_table.predictability, 6),
            "D_policy": round(rep_table.d_policy, 6),
            "n_states": rep_table.n_states,
            "note": "reader self-test: exactly 1.0 on the deterministic policy",
        },
        "marginal_phase": {
            "P": round(rep_marg.predictability, 4),
            "D_policy": round(rep_marg.d_policy, 4),
            "n_states": rep_marg.n_states,
            "n_decisions": rep_marg.n_decisions,
            "plural_cells": plural_cells(marginal),
        },
        "conditioned_phase_branch": {
            "P": round(rep_br.predictability, 4),
            "D_policy": round(rep_br.d_policy, 4),
            "n_states": rep_br.n_states,
            "n_decisions": rep_br.n_decisions,
            "residual_plural_cells": plural_cells(branched),
        },
    }


# ---------------------------------------------------------------------------
# 2. declared layer
# ---------------------------------------------------------------------------


def declared(runs: list[dict]) -> dict:
    overlay = load_outcome_overlay(version=OVERLAY)
    out: dict = {}
    for profile in PROFILES:
        net = load_routing_net(profile)
        decl = M.declared_conditional_composition(net, overlay)
        rep = M.predictability_report(decl, arm="declared", profile=profile)
        # per-cell: N, D, E, modal
        cells = {
            "|".join(c.state): {
                "N": c.hill.support_n,
                "D": round(c.hill.effective_number, 4),
                "E": round(c.hill.evenness, 4),
                "modal": round(c.modal_p, 4),
            }
            for c in rep.cells
        }
        out[profile] = {
            "P_uniform_over_states": round(rep.predictability, 4),
            "D_policy_uniform_over_states": round(rep.d_policy, 4),
            "n_states": rep.n_states,
            "n_plural_states": sum(1 for c in rep.cells if c.hill.support_n > 1),
            "cells": cells,
        }
    return out


# ---------------------------------------------------------------------------
# 3. realised headline — per-seed values with bootstrap CIs
# ---------------------------------------------------------------------------


def _per_seed_P_D(runs: list[dict]) -> tuple[list[float], list[float]]:
    """Per-seed aggregate P and D_policy (one value per run/seed) — the units the
    bootstrap resamples, so the CI reflects seed variance, not pooled counts."""
    ps, ds = [], []
    for r in runs:
        rep = M.predictability_report(movement_comp(r), arm=r["arm"], profile=r["profile"])
        if rep.n_decisions > 0:
            ps.append(rep.predictability)
            ds.append(rep.d_policy)
    return ps, ds


def _boot_ci(values: list[float], seed: int = 0) -> tuple[float, float, float]:
    if not values:
        return (float("nan"), float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    arr = np.array(values)
    means = [rng.choice(arr, size=len(arr), replace=True).mean() for _ in range(BOOT)]
    return (float(arr.mean()), float(np.percentile(means, Q_LO)),
            float(np.percentile(means, Q_HI)))


def realised(runs: list[dict]) -> dict:
    groups = by_arm_profile(runs)
    out: dict = {}
    for profile in PROFILES:
        out[profile] = {}
        for arm in ("corpus", "uniform_null", "verdict_blind"):
            rs = groups.get((arm, profile), [])
            # pooled aggregate (the point value) + per-seed CI
            pooled = M.predictability_report(pooled_comp(rs), arm=arm, profile=profile)
            ps, ds = _per_seed_P_D(rs)
            p_mean, p_lo, p_hi = _boot_ci(ps, seed=1)
            d_mean, d_lo, d_hi = _boot_ci(ds, seed=2)
            out[profile][arm] = {
                "P_pooled": round(pooled.predictability, 4),
                "D_policy_pooled": round(pooled.d_policy, 4),
                "P_seedmean": round(p_mean, 4),
                "P_ci": [round(p_lo, 4), round(p_hi, 4)],
                "D_policy_seedmean": round(d_mean, 4),
                "D_policy_ci": [round(d_lo, 4), round(d_hi, 4)],
                "n_states": pooled.n_states,
                "n_decisions": pooled.n_decisions,
                "n_unestimable": len(pooled.unestimable_states),
            }
        # the baseline anchor: P=1, D=1 by construction (constant, not a measurement)
        out[profile]["baseline"] = {"P": 1.0, "D_policy": 1.0, "note": "constructed"}
    return out


# ---------------------------------------------------------------------------
# 4. decomposition — verdict slice JSD vs the verdict-blind null; corpus vs uniform
# ---------------------------------------------------------------------------


_MIN_SLICE = 8  # a place needs this many of each verdict to compare its two slices


def _verdict_slice_jsd(comp: dict[tuple, Counter]) -> tuple[float, int]:
    """One arm's verdict effect on routing, measured **per place** and aggregated —
    NOT pooled over places, which would conflate *which places carry which verdict*
    with *verdict-conditioned routing at a place*. For every place that carries both
    a success and a failure slice with at least ``_MIN_SLICE`` decisions each, the
    JSD between that place's success next-distribution and its failure
    next-distribution; the visitation-weighted mean over such places.

    Under the verdict-blind overlay both slices at a place are samples from the same
    (base) distribution, so this reads ~sampling-noise by construction — the null
    the corpus arm must clear. Returns (weighted JSD, number of places compared)."""
    by_place_succ: dict[str, Counter] = {}
    by_place_fail: dict[str, Counter] = {}
    for (place, verdict), counts in comp.items():
        if verdict == "success":
            by_place_succ.setdefault(place, Counter()).update(counts)
        elif verdict == "failure":
            by_place_fail.setdefault(place, Counter()).update(counts)
    num = 0.0
    den = 0.0
    n_places = 0
    for place in set(by_place_succ) & set(by_place_fail):
        s, f = by_place_succ[place], by_place_fail[place]
        ns, nf = sum(s.values()), sum(f.values())
        if ns < _MIN_SLICE or nf < _MIN_SLICE:
            continue
        p = {k: v / ns for k, v in s.items()}
        q = {k: v / nf for k, v in f.items()}
        weight = ns + nf
        num += weight * M.jsd(p, q)
        den += weight
        n_places += 1
    return (num / den if den else float("nan"), n_places)


def _boot_jsd_ci(runs: list[dict], seed: int = 0) -> tuple[float, float]:
    """Bootstrap CI for a run set's per-place verdict-slice JSD, resampling runs
    with replacement (the seed is the resampling unit)."""
    if len(runs) < 4:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    idx = np.arange(len(runs))
    draws = []
    for _ in range(400):
        sample = [runs[i] for i in rng.choice(idx, size=len(idx), replace=True)]
        j, _n = _verdict_slice_jsd(pooled_comp(sample))
        if j == j:
            draws.append(j)
    if not draws:
        return (float("nan"), float("nan"))
    return (float(np.percentile(draws, Q_LO)), float(np.percentile(draws, Q_HI)))


def decomposition(runs: list[dict]) -> dict:
    groups = by_arm_profile(runs)
    out: dict = {"verdict_slice": {}, "corpus_vs_uniform": {}}
    for profile in PROFILES:
        corpus = groups.get(("corpus", profile), [])
        blind = groups.get(("verdict_blind", profile), [])
        # per-place verdict-slice JSD, corpus arm, vs the verdict-blind null (its
        # two slices at a place are samples of the same distribution, so its JSD is
        # the by-construction noise floor). Bootstrap over runs for the CIs P1 asks.
        corpus_jsd, corpus_np = _verdict_slice_jsd(pooled_comp(corpus))
        blind_jsd, blind_np = _verdict_slice_jsd(pooled_comp(blind))
        c_lo, c_hi = _boot_jsd_ci(corpus, seed=5)
        b_lo, b_hi = _boot_jsd_ci(blind, seed=6)
        out["verdict_slice"][profile] = {
            "corpus_jsd": round(corpus_jsd, 5) if corpus_jsd == corpus_jsd else None,
            "corpus_jsd_ci": [round(c_lo, 5), round(c_hi, 5)],
            "corpus_n_places": corpus_np,
            "verdict_blind_null_jsd": round(blind_jsd, 5) if blind_jsd == blind_jsd else None,
            "verdict_blind_null_ci": [round(b_lo, 5), round(b_hi, 5)],
            "verdict_blind_n_places": blind_np,
            "ci_separated": bool(c_lo == c_lo and b_hi == b_hi and c_lo > b_hi),
        }
        # corpus vs uniform-null predictability (is the plurality preferred, or
        # graph-forced?) — lower P on the corpus arm than the uniform arm means the
        # weights concentrate; the evenness half is per-cell and reported in declared
        uniform = groups.get(("uniform_null", profile), [])
        pc, _ = _per_seed_P_D(corpus)
        pu, _ = _per_seed_P_D(uniform)
        c_mean, c_lo, c_hi = _boot_ci(pc, seed=3)
        u_mean, u_lo, u_hi = _boot_ci(pu, seed=4)
        out["corpus_vs_uniform"][profile] = {
            "corpus_P": round(c_mean, 4), "corpus_P_ci": [round(c_lo, 4), round(c_hi, 4)],
            "uniform_P": round(u_mean, 4), "uniform_P_ci": [round(u_lo, 4), round(u_hi, 4)],
            "ci_separated": bool(c_hi < u_lo or u_hi < c_lo),
            "direction": "corpus more predictable" if c_mean > u_mean
            else "corpus less predictable",
        }
    return out


def main() -> int:
    runs = load_runs()
    n_seeds = len({r["seed"] for r in runs})
    print(f"loaded {len(runs)} runs across {n_seeds} seeds")
    results = {
        "n_runs": len(runs), "n_seeds": n_seeds,
        "census": census(runs),
        "calibration": calibration(runs),
        "declared": declared(runs),
        "realised": realised(runs),
        "decomposition": decomposition(runs),
    }
    (HERE / "pred_results.json").write_text(json.dumps(results, indent=2))
    print(f"wrote {HERE / 'pred_results.json'}")

    # a terse console digest
    cal = results["calibration"]
    print(f"\ncalibration: constructed table P={cal['constructed_table']['P']}; "
          f"marginal(phase) P={cal['marginal_phase']['P']} "
          f"D={cal['marginal_phase']['D_policy']}; "
          f"conditioned(phase,branch) P={cal['conditioned_phase_branch']['P']} "
          f"D={cal['conditioned_phase_branch']['D_policy']}")
    print("\nrealised P (corpus arm), per profile — baseline is 1.000 by construction:")
    for profile in PROFILES:
        c = results["realised"][profile]["corpus"]
        print(f"  {profile:32} P={c['P_pooled']:.4f} "
              f"CI[{c['P_ci'][0]:.3f},{c['P_ci'][1]:.3f}]  "
              f"D_policy={c['D_policy_pooled']:.3f}  states={c['n_states']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
