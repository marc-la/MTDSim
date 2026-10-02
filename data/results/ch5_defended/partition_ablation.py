#!/usr/bin/env python3
"""§5.4 Ablation of the attack profiles: the APT attacker model on c_1 to c_4
against the same model on the attack graph before it is partitioned (profile
``aggregate`` in the corpora). Design: docs/handoffs/2026-10-02_c_agg_ablation_proposal.md
(Marc 2026-10-02: "we're just winding back a step, so there will be overlap").

NO RUNS. The attack graph ran beside the profiles in every cell of the reported
corpora (1 000 seeds, the vulnerability memory on, the failure matrix on):
  outcome    runs_reported_summaries.pkl (per-run hosts, by cell), every cell;
  behaviour  ../ch5_s531_unopposed/runs_reported.jsonl, no MTD.

ARMS. "with" is c_1 to c_4 averaged with equal weight per seed, as every pooled
value of chapter 5 is; "without" is the attack graph's run on the same seed.
Check 1: the profiles weighted by the attack flows that carry weight
(Equation base-weight's operator rule: 14, 6, 5 and 4 of 29), the like-for-like
mixture of the attack graph's own construction.

EFFECT SIZE. Section 5.4's Cohen's d, with minus without, the pooled SD of the
two arms' per-seed values, as ablation.py computes it. Here one arm's per-seed
value is a mean of four runs and the other's one run, so this SD is the smaller
and d the larger: conservative for a negligible verdict. Check 2, the
per-campaign d (each arm's SD over single runs; the mixture's includes the
spread between profiles), is kept beside it. Bootstrap: seeds resampled, all
five runs of a seed together, 2 000 resamples, 95 % percentile intervals.

BEHAVIOUR (the manipulation check, no MTD). Distinct attack paths over the
first k steps (Figure 5.1(b)'s measure), counted on equal numbers of runs: the
attack graph's against one profile per seed, the profiles in turn (seed mod 4),
because the count is capped by the runs counted. Relative tactic occurrence:
the attack graph's against the four profiles' runs pooled.

Usage: PYTHONPATH=src python data/results/ch5_defended/partition_ablation.py
Output: partition_ablation_numbers.json beside it (n = 100 and n = 1 000), and
Appendix F's table of d at every MTD condition and interval (n = 1 000),
docs/thesis/tables/tab_F-3_ablation_attack_profiles.tex. TABLE_ONLY=1 rewrites
the table from the JSON without recomputing.
"""
from __future__ import annotations

import json
import pickle
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CACHE = HERE / "runs_reported_summaries.pkl"
UNOPPOSED = HERE.parent / "ch5_s531_unopposed" / "runs_reported.jsonl"
OUT = HERE / "partition_ablation_numbers.json"
FOUR = ("objective_exfiltration", "objective_impact", "objective_exfiltration_impact", "objective_none_c2")
AGG = "aggregate"
FLOW_WEIGHT = {"objective_exfiltration": 14, "objective_impact": 6,
               "objective_exfiltration_impact": 5, "objective_none_c2": 4}  # of 29, operator rule
N_HOSTS = 50
SHARED = (("none", 0), ("ip_shuffle", 200), ("ip_shuffle", 2_000), ("os_diversity", 200), ("os_diversity", 2_000))
NOT_REPORTED = ("random_four",)  # MTDShield's matched control, read nowhere in chapter 5
N_BOOT = 2_000
SEED = 20261002
K_MAX = 8


def load_outcome() -> dict:
    """(condition, interval) -> {profile: NCR per seed, seeds 0..999 in order}."""
    with CACHE.open("rb") as fh:
        summaries, _ = pickle.load(fh)
    cells: dict = {}
    for key, rows in summaries.items():
        group, arm, profile, objective, cond, interval, regime, overlay = key
        if arm != "movement" or (profile not in FOUR and profile != AGG):
            continue
        assert [r["seed"] for r in rows] == list(range(len(rows))), key
        cells.setdefault((cond, interval), {})[profile] = np.array([r["hosts"] for r in rows], float) / N_HOSTS
    return cells


def _d(w: np.ndarray, wo: np.ndarray) -> float:
    sp = np.sqrt((w.var(ddof=1) + wo.var(ddof=1)) / 2)
    return float((w.mean() - wo.mean()) / sp) if sp > 0 else 0.0


def _d_campaign(x: np.ndarray, wo: np.ndarray, weights: np.ndarray) -> float:
    """d with each arm's SD over single runs: the with arm is the mixture of the
    four profiles' runs (within-profile variance plus the spread of their means)."""
    mu = x.mean(axis=1)
    m = float(weights @ mu)
    var_with = float(weights @ (x.var(axis=1, ddof=1) + (mu - m) ** 2))
    sp = np.sqrt((var_with + wo.var(ddof=1)) / 2)
    return float((m - wo.mean()) / sp) if sp > 0 else 0.0


def contrast(prof: dict, n: int, rng: np.random.Generator) -> dict:
    x = np.stack([prof[p][:n] for p in FOUR])  # 4 x n
    wo = prof[AGG][:n]
    eq = np.full(4, 0.25)
    fw = np.array([FLOW_WEIGHT[p] for p in FOUR], float)
    fw /= fw.sum()
    w_eq, w_fw = eq @ x, fw @ x
    idx = rng.integers(0, n, size=(N_BOOT, n))
    boot = np.array([_d(w_eq[i], wo[i]) for i in idx])
    boot_fw = np.array([_d(w_fw[i], wo[i]) for i in idx])
    return {
        "n": n,
        "ncr_with": float(w_eq.mean()), "ncr_without": float(wo.mean()),
        "ncr_with_flow_weighted": float(w_fw.mean()),
        "per_profile": {p: float(prof[p][:n].mean()) for p in FOUR},
        "cohen_d": _d(w_eq, wo),
        "cohen_d_ci95": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
        "check1_flow_weighted_d": _d(w_fw, wo),
        "check1_flow_weighted_d_ci95": [float(np.percentile(boot_fw, 2.5)), float(np.percentile(boot_fw, 97.5))],
        "check2_per_campaign_d": _d_campaign(x, wo, eq),
        "check2_per_campaign_d_flow_weighted": _d_campaign(x, wo, fw),
    }


def outcome(n: int) -> dict:
    cells = load_outcome()
    rng = np.random.default_rng(SEED)
    out = {f"{c}|{i}": contrast(prof, n, rng) for (c, i), prof in sorted(cells.items())}
    none = out["none|0"]
    for key, r in out.items():  # NCR reduction, each arm against its own no-MTD runs (section 4.5)
        if key == "none|0":
            continue
        r["ncr_reduction_with"] = 1 - r["ncr_with"] / none["ncr_with"]
        r["ncr_reduction_without"] = 1 - r["ncr_without"] / none["ncr_without"]
    grid = {k: v for k, v in out.items() if k.split("|")[0] not in NOT_REPORTED}
    top = max(grid, key=lambda k: abs(grid[k]["cohen_d"]))
    return {
        "cells": out,
        "shared": {f"{c}|{i}": out[f"{c}|{i}"] for c, i in SHARED},
        "largest_abs_d": {"cell": top, "d": grid[top]["cohen_d"], "ci95": grid[top]["cohen_d_ci95"]},
        "cells_d_at_least_0_2": sorted(k for k, v in grid.items() if abs(v["cohen_d"]) >= 0.2),
        "cells_interval_past_0_2": sorted(k for k, v in grid.items()
                                          if v["cohen_d_ci95"][0] <= -0.2 or v["cohen_d_ci95"][1] >= 0.2),
        "n_cells_read": len(grid),
    }


def behaviour(n: int) -> dict:
    seqs: dict = {p: {} for p in FOUR + (AGG,)}
    steps: dict = {p: Counter() for p in FOUR + (AGG,)}
    with UNOPPOSED.open(encoding="utf-8") as fh:
        for line in fh:
            if '"arm": "movement"' not in line[:200]:
                continue
            r = json.loads(line)
            if "error" in r:
                raise SystemExit(f"error row in the unopposed corpus: {r['error']}")
            if r["seed"] >= n:
                continue
            places = tuple(rec[0] for rec in r["records"])
            seqs[r["profile"]][r["seed"]] = places
            steps[r["profile"]].update(places)
    for p in seqs:
        assert sorted(seqs[p]) == list(range(n)), (p, len(seqs[p]))
    rotation = [seqs[FOUR[s % 4]][s] for s in range(n)]
    agg = [seqs[AGG][s] for s in range(n)]
    pooled = sum((steps[p] for p in FOUR), Counter())
    tactics = sorted(set(pooled) | set(steps[AGG]))
    share = lambda c: {t: 100 * c.get(t, 0) / sum(c.values()) for t in tactics}  # noqa: E731
    return {
        "n": n,
        "distinct_attack_paths": {
            "with_one_profile_per_seed": {str(k): len({q[:k] for q in rotation}) for k in range(1, K_MAX + 1)},
            "without": {str(k): len({q[:k] for q in agg}) for k in range(1, K_MAX + 1)},
        },
        "relative_tactic_occurrence": {"with_pooled": share(pooled), "without": share(steps[AGG])},
        "tactics_entered": {"with_pooled": len(pooled), "without": len(steps[AGG]),
                            **{p: len(steps[p]) for p in FOUR}},
    }


TABLE = HERE.parents[2] / "docs" / "thesis" / "tables" / "tab_F-3_ablation_attack_profiles.tex"
ROWS = (("ip_shuffle", "IP shuffle"), ("complete_topology", "complete topology shuffle"),
        ("host_topology", "host topology shuffle"), ("port_shuffle", "port shuffle"),
        ("user_shuffle", "user shuffle"), ("os_diversity", "OS diversity"),
        ("service_diversity", "service diversity"), None,
        ("random", "random"), ("mtdshield", "MTDShield"), ("alternative", "alternative"))
INTERVALS = (50, 100, 200, 500, 1_000, 2_000)


def _mark(d: float, ci: list) -> str:
    """d to two places, marked as Table 5.5 marks it: bold where the interval lies
    wholly beyond +-0.2, a dagger where it crosses an edge, plain within."""
    from decimal import ROUND_HALF_UP, Decimal
    q = Decimal(repr(d)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    cell = f"${q:+.2f}$" if q != 0 else "0.00"
    if ci[1] <= -0.2 or ci[0] >= 0.2:
        return r"\bfseries\boldmath " + cell
    if ci[0] <= -0.2 or ci[1] >= 0.2:
        return cell + r"$^{\dagger}$"
    return cell


def write_table(result: dict) -> None:
    cells = result["by_n"]["1000"]["outcome"]["cells"]
    none = cells["none|0"]
    body = []
    for row in ROWS:
        if row is None:
            body.append(r"    \midrule")
            continue
        key, label = row
        body.append("    " + " & ".join([label] + [_mark(cells[f"{key}|{i}"]["cohen_d"], cells[f"{key}|{i}"]["cohen_d_ci95"])
                                         for i in INTERVALS]) + r" \\")
    lo, hi = none["cohen_d_ci95"]
    tex = [
        "% GENERATED by data/results/ch5_defended/partition_ablation.py from partition_ablation_numbers.json",
        "% (n = 1 000); never hand-edit. Section 5.4.1's grid. Caption DRAFT STATE 2026-10-02, ratify on read.",
        r"\begin{table}[tp]",
        r"  \centering",
        (r"  \caption[The APT attacker model with and without the attack profiles, at every MTD and interval]"
         r"{Cohen's $d$ on NCR of the APT attacker model averaged over $c_1$ to $c_4$, minus the same model on the "
         r"attack graph, on the same 1\,000 seeds, for every MTD mechanism and deployment strategy at every "
         rf"deployment interval (with no MTD, ${none['cohen_d']:+.2f}$ [${lo:+.2f}$, ${hi:+.2f}$]). "
         r"Bold: the 95\,\% bootstrap interval over seeds lies wholly beyond $\pm 0.2$; $\dagger$: it crosses "
         r"$\pm 0.2$; otherwise it lies within.}"),
        r"  \label{tab:ablation-attack-profiles}",
        r"  \tablestyle",
        r"  \begin{tabular}{@{}lcccccc@{}}",
        r"    \toprule",
        r"    & \multicolumn{6}{c}{Deployment interval (s)} \\",
        r"    \cmidrule(lr){2-7}",
        r"    MTD & 50 & 100 & 200 & 500 & 1\,000 & 2\,000 \\",
        r"    \midrule",
    ] + body + [r"    \bottomrule", r"  \end{tabular}", r"\end{table}", ""]
    TABLE.write_text("\n".join(tex), encoding="utf-8")
    print(f"wrote {TABLE}")


def main() -> int:
    import os
    if os.environ.get("TABLE_ONLY") == "1":
        write_table(json.loads(OUT.read_text()))
        return 0
    result = {"design": "docs/handoffs/2026-10-02_c_agg_ablation_proposal.md",
              "flow_weights": FLOW_WEIGHT,
              "by_n": {str(n): {"outcome": outcome(n), "behaviour": behaviour(n)} for n in (100, 1_000)}}
    OUT.write_text(json.dumps(result, indent=1))
    write_table(result)
    for n in ("100", "1000"):
        o = result["by_n"][n]["outcome"]
        print(f"n = {n}: largest |d| {o['largest_abs_d']}; cells d >= 0.2: {o['cells_d_at_least_0_2']}")
        for k, r in o["shared"].items():
            red = (f"  red {r['ncr_reduction_with']:.2f} / {r['ncr_reduction_without']:.2f}"
                   if "ncr_reduction_with" in r else "")
            print(f"  {k:18s} {r['ncr_with']:.3f} {r['ncr_without']:.3f}  d {r['cohen_d']:+.2f} "
                  f"[{r['cohen_d_ci95'][0]:+.2f}, {r['cohen_d_ci95'][1]:+.2f}]  flow-w d "
                  f"{r['check1_flow_weighted_d']:+.2f}  per-campaign d {r['check2_per_campaign_d']:+.2f}{red}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
