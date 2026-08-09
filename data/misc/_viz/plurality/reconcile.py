"""Null reconciliation for the plurality-reporting handoff (2026-08-09).

Six sweep families each quote a path-entropy null, at three different poolings,
two sink policies and mixed MTD conditions. Before any composite figure exists,
this script does two things, both read off the recorded runs — nothing is
re-simulated:

  Part 1 — as-quoted: reproduce each record's quoted null under that record's
           own convention, so every prose number is anchored to a computation.
  Part 2 — common ground: recompute every family at ONE convention — the badge's
           own (experiment 2 E3): v2_partial mapping, no MTD, seeds 0-9,
           pooled-transitions entropy — per profile and pooled across profiles.
           The sink policy CANNOT be unified by re-reading (censor truncates the
           walk), so families are grouped by the policy they ran under, and
           experiment 2's no-MTD cells (recorded under BOTH policies) bridge
           the groups: within a policy group, zero-point transition tallies are
           compared for exact identity.

Output: reconciliation.json (machine) + a printed table (human, pasted into
docs/implementation/pipeline/ogasp/plurality_reporting.md).

    PYTHONPATH=src python data/misc/_viz/plurality/reconcile.py
"""
from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from mtdsim.l3_simulation.movement.measures import (  # noqa: E402
    mean_ci,
    path_entropy_from_transitions,
)

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[2] / "results"

# The 2026-08-06 objective-tactic rename: earlier workspaces recorded the old
# labels. Read off the runs, normalised here, once.
RENAME = {
    "pure_steal": "objective_exfiltration",
    "pure_impediment": "objective_impact",
    "double_extortion": "objective_exfiltration_impact",
    "infrastructure_setup": "objective_none_c2",
    "aggregate": "aggregate",
}
PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)


def load(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text().splitlines():
        r = json.loads(line)
        if "error" in r:
            continue
        p = r.get("profile")
        if p in RENAME:
            r["profile"] = RENAME[p]
        rows.append(r)
    return rows


def sel(rows, **kw):
    return [r for r in rows if all(r.get(k) == v for k, v in kw.items())]


def tally(rows) -> dict[str, Counter]:
    """Pooled place -> next-place counts over a cell's runs."""
    out: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        for edge, n in r["transitions"].items():
            src, dst = edge.split(">", 1)
            out[src][dst] += n
    return out


def pooled_entropy(rows) -> float:
    return path_entropy_from_transitions(tally(rows))


def per_run_entropy(r) -> float:
    return path_entropy_from_transitions(
        {src: dict(c) for src, c in tally([r]).items()}
    )


def mean_per_run_entropy(rows):
    vals = [per_run_entropy(r) for r in rows]
    i = mean_ci(vals)
    return i.mean, i.ci95


def hub_share(rows) -> float:
    """Maximum single-place visit share, visits taken as the source-side
    marginal of the pooled transition tally (the run's terminal visit is the
    one visit this undercounts — uniform across every family)."""
    t = tally(rows)
    visits = {src: sum(c.values()) for src, c in t.items()}
    total = sum(visits.values())
    return max(visits.values()) / total if total else float("nan")


# ---------------------------------------------------------------------------
# The six families + the badge source, declared once.
# `null_sel` / `point_sel(x)` return row filters; `band` maps sweep points to
# position-in-band on [0, 1]. Conditions are read off each sweep script and
# recorded here as data so the table states its own provenance.
# ---------------------------------------------------------------------------

W = {}  # family -> spec

_ax6 = load(RESULTS / "axis6_rationality" / "numbers" / "sweep_per_run.jsonl")
W["utility_lambda"] = {
    "label": "utility λ (axis 6, shipped)",
    "script": "data/results/axis6_rationality/run_sweep.py",
    "record": "incentive_rationality.md C3",
    "sink_policy": "censor",
    "rows": _ax6,
    "points": [("lam_0", 0.0), ("lam_0.5", 0.125), ("lam_1", 0.25),
               ("lam_2", 0.5), ("lam_4", 1.0)],
    "cell": lambda rows, pt: sel(rows, mapping="v2_partial", point=pt,
                                 condition="no_mtd"),
    "expect": "falls",
}

_ax7 = load(RESULTS / "axis7_learning" / "runs.jsonl")
W["learner_kappa"] = {
    "label": "learner κ (axis 7)",
    "script": "data/results/axis7_learning/run_sweep.py",
    "record": "learning_capability.md §7.5 (L4)",
    "sink_policy": "censor",
    "rows": _ax7,
    "points": [(0.0, 0.0), (0.5, 0.125), (1.0, 0.25), (2.0, 0.5), (4.0, 1.0)],
    "cell": lambda rows, pt: sel(rows, mapping="v2_partial", kappa=pt, rho=0.5,
                                 mtd="none"),
    "expect": "falls",
}

_fsm_a = load(RESULTS / "fsm_alignment" / "runs.jsonl")
W["alignment_alpha"] = {
    "label": "alignment α (factor 8)",
    "script": "data/results/fsm_alignment/run_sweep.py",
    "record": "modulator_composition.md (A4)",
    "sink_policy": "retrace",
    "rows": _fsm_a,
    "points": [(0.0, 0.0), (0.25, 0.25), (0.5, 0.5), (0.75, 0.75), (1.0, 1.0)],
    "cell": lambda rows, pt: sel(rows, arm="movement", alpha=pt,
                                 condition="none"),
    "expect": "falls",
}

_fsm_s = load(RESULTS / "fsm_succession" / "runs.jsonl")
W["succession_alpha"] = {
    "label": "succession α (factor 9)",
    "script": "data/results/fsm_succession/run_sweep.py",
    "record": "modulator_composition.md (B4)",
    "sink_policy": "retrace",
    "rows": _fsm_s,
    "points": [(0.0, 0.0), (0.25, 0.25), (0.5, 0.5), (0.75, 0.75), (1.0, 1.0)],
    "cell": lambda rows, pt: sel(rows, arm="movement", alpha=pt,
                                 condition="none"),
    "expect": "falls",
}

_iter = load(RESULTS / "iterated_cost" / "runs.jsonl")


def _iter_cell(arm):
    def f(rows, pt):
        if pt == 0.0:  # the shared ablation arm IS lambda = 0 for every arm
            return sel(rows, arm="ablation", lam=0.0, mapping="v2_partial",
                       mtd="none")
        return sel(rows, arm=arm, lam=pt, mapping="v2_partial", mtd="none")
    return f


for _arm, _expect in (("A", "falls"), ("B", "rises")):
    W[f"iterated_{_arm}"] = {
        "label": f"iterated cost, change {_arm} (λ)",
        "script": "data/results/iterated_cost/run_sweep.py",
        "record": "iterated_cost_model.md",
        "sink_policy": "censor",
        "rows": _iter,
        "points": [(0.0, 0.0), (0.5, 0.125), (1.0, 0.25), (2.0, 0.5),
                   (4.0, 1.0)],
        "cell": _iter_cell(_arm),
        "expect": _expect,
    }

_exp2 = load(RESULTS / "expo02_ashen_lynx" / "runs.jsonl")


def main() -> int:
    out = {"part1_as_quoted": {}, "part2_common_ground": {},
           "null_identity": {}, "p1_kill_criterion": {}}

    # -- Part 1: each record's quoted null, reproduced under its own convention
    print("=" * 78)
    print("PART 1 — as-quoted nulls, reproduced under each record's own convention")
    print("=" * 78)

    q = {}
    # experiment 2 §12: per-profile pooled entropy + distinct prefix5,
    # movement arm, no MTD, retrace, per interval (10 seeds).
    for interval in (200, 2000):
        for profile in PROFILES:
            cells = sel(_exp2, arm="movement", profile=profile,
                        condition="none", interval=interval,
                        sink_policy="retrace")
            q[f"exp2/{interval}/{profile}"] = {
                "pooled_entropy": round(pooled_entropy(cells), 3),
                "distinct_prefix5": len({tuple(r["prefix5"]) for r in cells}),
                "n": len(cells),
            }
    # axis 6 C3: MEAN PER-RUN entropy per profile, both MTD conditions pooled.
    for mapping in ("v1_ckc_total", "v2_partial"):
        for profile in ("objective_exfiltration", "objective_none_c2"):
            for pt in ("lam_0", "lam_4"):
                rows = [r for c in ("no_mtd", "random_mtd")
                        for r in sel(_ax6, mapping=mapping, point=pt,
                                     condition=c, profile=profile)]
                m, ci = mean_per_run_entropy(rows)
                q[f"axis6/C3/{mapping}/{profile}/{pt}"] = {
                    "mean_per_run_entropy": round(m, 3),
                    "ci95": round(ci, 3), "n": len(rows)}
    # axis 7 L4: pooled per profile x mapping, kappa ladder at rho 0.5, no MTD.
    for mapping in ("v1_ckc_total", "v2_partial"):
        for profile in ("aggregate", "objective_none_c2"):
            for k in (0.0, 4.0):
                rows = sel(_ax7, mapping=mapping, profile=profile, kappa=k,
                           rho=0.5, mtd="none")
                q[f"axis7/L4/{mapping}/{profile}/k{k}"] = {
                    "pooled_entropy": round(pooled_entropy(rows), 3),
                    "n": len(rows)}
    # factors 8/9 A4/B4: pooled across profiles AND all defence conditions.
    for name, rows in (("factor8", _fsm_a), ("factor9", _fsm_s)):
        for a in (0.0, 1.0):
            cells = sel(rows, arm="movement", alpha=a)
            q[f"{name}/A4/alpha{a}"] = {
                "pooled_entropy": round(pooled_entropy(cells), 3),
                "n": len(cells)}
    # iterated cost: pooled across profiles, v2_partial; the quoted 2.613 null.
    for arm, lam in (("ablation", 0.0), ("declared", 4.0), ("B", 4.0)):
        rows = sel(_iter, arm=arm, lam=lam, mapping="v2_partial", mtd="none")
        q[f"iterated/{arm}/lam{lam}"] = {
            "pooled_entropy": round(pooled_entropy(rows), 3), "n": len(rows)}
    out["part1_as_quoted"] = q
    for k, v in q.items():
        print(f"  {k:55s} {v}")

    # -- Part 2: everything on the badge's convention ------------------------
    print()
    print("=" * 78)
    print("PART 2 — common ground: v2_partial, no MTD, seeds 0-9, pooled entropy")
    print("        (families keep the sink policy they ran under — stated per row)")
    print("=" * 78)

    cg = {}
    for name, w in W.items():
        series = []
        for pt, x in w["points"]:
            cells = w["cell"](w["rows"], pt)
            e = pooled_entropy(cells)
            per_prof = {p: round(pooled_entropy(sel(cells, profile=p)), 3)
                        for p in PROFILES}
            series.append({
                "point": str(pt), "x_in_band": x,
                "pooled_entropy": round(e, 4),
                "hub_share": round(hub_share(cells), 4),
                "per_profile": per_prof, "n": len(cells),
            })
        cg[name] = {
            "label": w["label"], "sink_policy": w["sink_policy"],
            "script": w["script"], "record": w["record"],
            "mapping": "v2_partial", "mtd": "none", "seeds": "0-9",
            "expect": w["expect"], "series": series,
        }
        print(f"\n  {w['label']}  [{w['sink_policy']}]  ({w['script']})")
        for s in series:
            print(f"    x={s['x_in_band']:<6} H={s['pooled_entropy']:.4f}  "
                  f"hub={s['hub_share']:.3f}  n={s['n']}")

    # experiment 2's no-MTD cells under both policies — the bridge rows.
    for policy in ("retrace", "censor"):
        series = []
        for interval in (200, 2000):
            cells = sel(_exp2, arm="movement", condition="none",
                        interval=interval, sink_policy=policy)
            series.append({
                "point": f"interval_{interval}", "x_in_band": 0.0,
                "pooled_entropy": round(pooled_entropy(cells), 4),
                "hub_share": round(hub_share(cells), 4),
                "per_profile": {p: round(pooled_entropy(
                    sel(cells, profile=p)), 3) for p in PROFILES},
                "n": len(cells),
            })
        cg[f"exp2_null_{policy}"] = {
            "label": f"experiment 2 no-MTD ({policy})",
            "sink_policy": policy,
            "script": "data/results/expo02_ashen_lynx/run_experiment.py",
            "record": "experiment_02_findings.md §12",
            "mapping": "v2_partial", "mtd": "none", "seeds": "0-9",
            "expect": "null row", "series": series,
        }
        print(f"\n  experiment 2 no-MTD [{policy}]")
        for s in series:
            print(f"    {s['point']:14} H={s['pooled_entropy']:.4f}  "
                  f"hub={s['hub_share']:.3f}  n={s['n']}")
    out["part2_common_ground"] = cg

    # -- Null identity: are the zero points the same walks? ------------------
    print()
    print("=" * 78)
    print("NULL IDENTITY — pooled per-profile transition tallies at each family's")
    print("zero point, compared exactly within each sink-policy group")
    print("=" * 78)
    ident = {}
    groups = {
        "censor": ["utility_lambda", "learner_kappa", "iterated_A",
                   "iterated_B"],
        "retrace": ["alignment_alpha", "succession_alpha"],
    }
    for policy, fams in groups.items():
        tallies = {}
        for name in fams:
            w = W[name]
            pt, _ = w["points"][0]
            cells = w["cell"](w["rows"], pt)
            tallies[name] = {
                p: {s: dict(c) for s, c in
                    sorted(tally(sel(cells, profile=p)).items())}
                for p in PROFILES}
        # exp2 bridge (200 s label; no-MTD runs do not read the interval)
        cells = sel(_exp2, arm="movement", condition="none", interval=200,
                    sink_policy=policy)
        tallies["exp2_bridge"] = {
            p: {s: dict(c) for s, c in
                sorted(tally(sel(cells, profile=p)).items())}
            for p in PROFILES}
        names = list(tallies)
        ref = names[0]
        verdicts = {}
        for other in names[1:]:
            same = tallies[other] == tallies[ref]
            verdicts[f"{other} == {ref}"] = same
            print(f"  [{policy}] {other:20s} == {ref:20s} : {same}")
        ident[policy] = verdicts
    out["null_identity"] = ident

    # -- P1 kill criterion ---------------------------------------------------
    print()
    print("=" * 78)
    print("P1 — Spearman |rho| between pooled path entropy and max single-place")
    print("visit share, across the figure's cells (threshold 0.90, pre-registered)")
    print("=" * 78)
    pts = []
    for name in ("utility_lambda", "learner_kappa", "alignment_alpha",
                 "succession_alpha", "iterated_A", "iterated_B"):
        for s in cg[name]["series"]:
            pts.append((s["pooled_entropy"], s["hub_share"]))

    def spearman(pairs):
        def ranks(vals):
            order = sorted(range(len(vals)), key=lambda i: vals[i])
            rk = [0.0] * len(vals)
            i = 0
            while i < len(order):
                j = i
                while j + 1 < len(order) and \
                        vals[order[j + 1]] == vals[order[i]]:
                    j += 1
                avg = (i + j) / 2 + 1
                for k2 in range(i, j + 1):
                    rk[order[k2]] = avg
                i = j + 1
            return rk
        xs = ranks([p[0] for p in pairs])
        ys = ranks([p[1] for p in pairs])
        mx, my = statistics.fmean(xs), statistics.fmean(ys)
        num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
        dx = sum((a - mx) ** 2 for a in xs) ** 0.5
        dy = sum((b - my) ** 2 for b in ys) ** 0.5
        return num / (dx * dy) if dx and dy else float("nan")

    rho = spearman(pts)
    fired = abs(rho) >= 0.90
    out["p1_kill_criterion"] = {
        "spearman_rho": round(rho, 4), "n_cells": len(pts),
        "threshold": 0.90, "fired": fired,
        "verdict": "FIRED — do not draw the entropy figure" if fired
                   else "clear — the entropy axis is not a hub-share axis",
    }
    print(f"  rho = {rho:.4f} over {len(pts)} cells -> "
          f"{'FIRED' if fired else 'clear'}")

    (HERE / "reconciliation.json").write_text(json.dumps(out, indent=2))
    print(f"\nwrote {HERE / 'reconciliation.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
