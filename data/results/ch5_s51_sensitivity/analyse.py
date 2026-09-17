#!/usr/bin/env python3
"""The §5.1 sensitivity re-run — the read half. A pure reader over runs.jsonl.

Applies the criterion fixed in run_sweep.py's docstring to every point, under
every condition, and emits:

  numbers.json                       every number a float or the findings
                                     record may quote, keyed by section
  sim05_check.json                   the centre cells against the defended
                                     corpus, run by run (must be identical)
  per_run.csv                        the figure tool's contract
                                     (tools/ch5_sensitivity_figure.py --csv)
  docs/thesis/tables/tab_5-1a_declared_inputs.tex       the body table
  docs/thesis/tables/tab_C-1a_family_sensitivity.tex    App. C.1
  docs/thesis/tables/tab_C-2a_shape_substitution.tex    App. C.2
  docs/thesis/tables/tab_C-3a_decay_sensitivity.tex     App. C.3
  preview_families.png               matplotlib, for direction only

Interval convention: the chapter's (the suite's mean_ci — mean ± 1.96 SEM),
the same interval every §5.3–§5.5 table prints. The runner's docstring named
a seed bootstrap; both are computed and both verdicts are recorded, the
mean_ci one is primary because it is the chapter's, and the findings record
says whether any verdict differs between them (it must not, or the record says
where). Pooling is the four objective profiles; the aggregate is read beside.

    PYTHONPATH=src python data/results/ch5_s51_sensitivity/analyse.py [--partial]
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from mtdsim.l3_simulation.movement import measures as M

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
REPO = RESULTS.parent.parent
RUNS = HERE / "runs.jsonl"
DEFENDED = RESULTS / "ch5_defended" / "runs.jsonl"
NUMBERS = HERE / "numbers.json"
SIM05 = HERE / "sim05_check.json"
PER_RUN = HERE / "per_run.csv"
TAB_DIR = REPO / "docs" / "thesis" / "tables"
N_BOOT = 2_000
SEED = 20260917


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


sweep = _load("ch5_s51_run_sweep", HERE / "run_sweep.py")
POINTS = {p["name"]: p for p in sweep.build_points()}
FOUR = tuple(sweep.PROFILES[:4])
AGG = ("aggregate",)
CONDITIONS = tuple(sweep.CONDITIONS)
FAMILIES = ("scan-shaped", "exploit-shaped", "stealth-low-and-slow", "objective-execution")
FAMILY_NAME = {
    "scan-shaped": "scan-shaped",
    "exploit-shaped": "exploit-shaped",
    "stealth-low-and-slow": "low-and-slow",
    "objective-execution": "objective execution",
}
FAMILY_VALUE = {"scan-shaped": 35.0, "exploit-shaped": 4.5,
                "stealth-low-and-slow": 45.0, "objective-execution": 36.0}
COND_LABEL = {("none", 0): "no defence", ("random", 200): "defended, 200\\,s",
              ("random", 2000): "defended, 2\\,000\\,s"}
IDENTITY_FIELDS = ("compromised", "termination_time", "n_actions", "n_blocked",
                   "n_success", "n_interrupted", "mtd_count", "reached_objective")


# --- load and sanity -------------------------------------------------------------
def load(partial: bool) -> tuple[dict, dict]:
    cells: dict[tuple, list[dict]] = defaultdict(list)
    errors = []
    with RUNS.open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if "error" in row:
                errors.append(row)
                continue
            cells[(row["point"], row["profile"], row["condition"], row["interval"])].append(row)
    counts = {len(v) for v in cells.values()}
    sanity = {
        "rows": sum(len(v) for v in cells.values()), "error_rows": len(errors),
        "cells": len(cells), "runs_per_cell": sorted(counts),
        "points_seen": len({k[0] for k in cells}), "points_designed": len(POINTS),
        "max_events_terminations": sum(1 for v in cells.values() for r in v if r["n_records"] >= 50_000),
    }
    if not partial:
        expected = len(POINTS) * len(sweep.PROFILES) * len(CONDITIONS)
        if sanity["cells"] != expected or counts != {len(sweep.SEEDS)}:
            raise SystemExit(f"corpus incomplete: {sanity}; pass --partial to read anyway")
    if errors:
        print(f"WARNING {len(errors)} error rows: {errors[:3]}", file=sys.stderr)
    return cells, sanity


def sim05_check(cells: dict) -> dict:
    """The centre must be the defended corpus, run for run."""
    want = {}
    for (point, profile, cond, interval), runs in cells.items():
        if point != "centre":
            continue
        for r in runs:
            want[(profile, cond, interval, r["seed"])] = (
                r["compromised"], round(r["termination_time"], 6), r["n_actions"])
    found: dict = {}
    if not DEFENDED.exists():
        return {"status": "defended corpus absent", "compared": 0}
    with DEFENDED.open(encoding="utf-8") as fh:
        for line in fh:
            if '"group": "core"' not in line or '"arm": "movement"' not in line:
                continue
            if '"condition": "none"' not in line and '"condition": "random"' not in line:
                continue
            r = json.loads(line)
            k = (r["profile"], r["condition"], r["interval"], r["seed"])
            if k in want and r["objective"] == "targeted" and r["regime"] == "shifted":
                found[k] = (r["compromised"], round(r["termination_time"], 6),
                            len([x for x in r["records"] if x[1]]))
    mismatch = [list(k) + [list(want[k]), list(found[k])] for k in want if k in found and want[k] != found[k]]
    out = {"compared": len([k for k in want if k in found]), "centre_rows": len(want),
           "mismatches": len(mismatch), "first_mismatches": mismatch[:5]}
    SIM05.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


# --- helpers ---------------------------------------------------------------------
def _iv(values) -> dict:
    iv = M.mean_ci([float(v) for v in values])
    return {"n": iv.n, "mean": iv.mean, "ci95": iv.ci95}


def _boot(values, rng) -> dict:
    x = np.asarray(values, dtype=float)
    boots = np.array([x[rng.integers(0, len(x), len(x))].mean() for _ in range(N_BOOT)])
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"lo": float(lo), "hi": float(hi)}


def pool(cells, point, profiles, cond, interval) -> list[dict]:
    out = []
    for p in profiles:
        out += cells.get((point, p, cond, interval), [])
    return out


def hosts(runs) -> list[float]:
    return [float(r["compromised"]) for r in runs]


def identical(a: list[dict], b: list[dict]) -> bool:
    """Bit-identical on every recorded field, over the (profile, seed) pairs both
    cells carry (a partial corpus has uneven seed sets; a complete one has
    identical key sets, which load() has already checked)."""
    ka = {(r["profile"], r["seed"]): tuple(r[f] for f in IDENTITY_FIELDS) for r in a}
    kb = {(r["profile"], r["seed"]): tuple(r[f] for f in IDENTITY_FIELDS) for r in b}
    keys = set(ka) & set(kb)
    return bool(keys) and all(ka[k] == kb[k] for k in keys)


def verdict(point_runs, centre_runs, rng, *, structural_point: bool) -> dict:
    """The criterion: inert when the point's pooled mean sits inside the centre's
    interval; moved otherwise. Recorded beside it: whether the two intervals are
    disjoint (the appendix's stricter 'CI-separated'), and the bootstrap form."""
    c, p = _iv(hosts(centre_runs)), _iv(hosts(point_runs))
    cb = _boot(hosts(centre_runs), rng)
    if structural_point and identical(point_runs, centre_runs):
        status = "zero by structure"
    else:
        status = "inert" if abs(p["mean"] - c["mean"]) <= c["ci95"] else "moved"
    inert_boot = cb["lo"] <= p["mean"] <= cb["hi"]
    separated = (p["mean"] - p["ci95"] > c["mean"] + c["ci95"]) or (p["mean"] + p["ci95"] < c["mean"] - c["ci95"])
    return {
        "status": status, "direction": ("up" if p["mean"] > c["mean"] else "down" if p["mean"] < c["mean"] else "same"),
        "point": p, "centre": c, "centre_boot": cb,
        "inert_by_bootstrap": bool(inert_boot) if status != "zero by structure" else True,
        "ci_separated": bool(separated),
        "delta": p["mean"] - c["mean"],
        "reached_share": float(np.mean([r["reached_objective"] for r in point_runs])),
        "blocked_fraction": float(sum(r["n_blocked"] for r in point_runs) / max(1, sum(r["n_actions"] for r in point_runs))),
        "actions_mean": float(np.mean([r["n_actions"] for r in point_runs])),
    }


def paired(a_runs, b_runs) -> dict:
    """a - b, paired by (profile, seed): the shape substitution's form."""
    ka = {(r["profile"], r["seed"]): r for r in a_runs}
    kb = {(r["profile"], r["seed"]): r for r in b_runs}
    keys = sorted(set(ka) & set(kb))
    d = [float(ka[k]["compromised"] - kb[k]["compromised"]) for k in keys]
    da = [float(ka[k]["n_actions"] - kb[k]["n_actions"]) for k in keys]
    return {
        "pairs": len(keys), "a": _iv([ka[k]["compromised"] for k in keys]),
        "b": _iv([kb[k]["compromised"] for k in keys]), "difference": _iv(d),
        "signs": {"lower": sum(1 for x in d if x < 0), "tied": sum(1 for x in d if x == 0),
                  "higher": sum(1 for x in d if x > 0)},
        "actions_difference": _iv(da),
    }


# --- the read --------------------------------------------------------------------
def analyse(cells: dict) -> dict:
    rng = np.random.default_rng(SEED)
    out: dict = {"conditions": [list(c) for c in CONDITIONS], "points": {}, "families": {},
                 "shape": {}, "mapping": {}, "decay": {}, "floor": {}, "profiles": {}}
    for pooling, profs in (("four", FOUR), ("aggregate", AGG)):
        out["points"][pooling] = {}
        for name, point in POINTS.items():
            if name == "centre":
                continue
            out["points"][pooling][name] = {}
            for cond, interval in CONDITIONS:
                pr, cr = pool(cells, name, profs, cond, interval), pool(cells, "centre", profs, cond, interval)
                if not pr or not cr:
                    continue
                out["points"][pooling][name][f"{cond}@{interval}"] = verdict(
                    pr, cr, rng, structural_point=name.startswith("decay_z_"))
    # per-profile readings at the family band ends (App. C.1's per-profile column, if wanted)
    for name in POINTS:
        if name == "centre":
            continue
        out["profiles"][name] = {}
        for p in sweep.PROFILES:
            for cond, interval in CONDITIONS:
                pr, cr = cells.get((name, p, cond, interval), []), cells.get(("centre", p, cond, interval), [])
                if pr and cr:
                    out["profiles"][name][f"{p}|{cond}@{interval}"] = {
                        "point": _iv(hosts(pr)), "centre": _iv(hosts(cr))}
    # family verdicts: inert iff both ends inert under every condition (four-profile pooling)
    four = out["points"]["four"]
    for fam in FAMILIES:
        lo, hi = sweep.FAMILY_BANDS[fam]
        ends = {f"x{lo:g}": four.get(f"dwell_{fam}_x{lo:g}", {}), f"x{hi:g}": four.get(f"dwell_{fam}_x{hi:g}", {})}
        statuses = [v["status"] for e in ends.values() for v in e.values()]
        # magnitude beside the verdict: hosts lost per doubling of the family's
        # dwell across its band, under each condition (a descriptive slope, so
        # the concentration of sensitivity in one family can be stated as a
        # number rather than as a count of verdicts)
        per_doubling = {}
        for key in ends[f"x{lo:g}"]:
            e_lo, e_hi = ends[f"x{lo:g}"][key], ends[f"x{hi:g}"].get(key)
            if e_hi:
                per_doubling[key] = (e_lo["point"]["mean"] - e_hi["point"]["mean"]) / float(np.log2(hi / lo))
        out["families"][fam] = {
            "value_s": FAMILY_VALUE[fam], "band": [lo, hi], "ends": ends,
            "verdict": "inert" if statuses and all(s == "inert" for s in statuses) else "moved",
            "moved_under": sorted({k for e in ends.values() for k, v in e.items() if v["status"] == "moved"}),
            "hosts_lost_per_doubling": per_doubling,
        }
    # the shape substitution, paired
    for label, erl, exp in (("centre", "shape_erlang4", "centre"),
                            ("lowslow_x4", "shape_erlang4_lowslow_x4", "dwell_stealth-low-and-slow_x4")):
        out["shape"][label] = {}
        for pooling, profs in (("four", FOUR), ("aggregate", AGG)):
            for cond, interval in CONDITIONS:
                a, b = pool(cells, erl, profs, cond, interval), pool(cells, exp, profs, cond, interval)
                if a and b:
                    out["shape"][label][f"{pooling}|{cond}@{interval}"] = paired(a, b)
    # the mapping swap
    for cond, interval in CONDITIONS:
        a, b = pool(cells, "mapping_forced_total", FOUR, cond, interval), pool(cells, "centre", FOUR, cond, interval)
        if a and b:
            out["mapping"][f"{cond}@{interval}"] = {
                "forced_total": {"hosts": _iv(hosts(a)), "reached_share": float(np.mean([r["reached_objective"] for r in a])),
                                 "blocked_fraction": float(sum(r["n_blocked"] for r in a) / max(1, sum(r["n_actions"] for r in a))),
                                 "actions": _iv([r["n_actions"] for r in a])},
                "partial": {"hosts": _iv(hosts(b)), "reached_share": float(np.mean([r["reached_objective"] for r in b])),
                            "blocked_fraction": float(sum(r["n_blocked"] for r in b) / max(1, sum(r["n_actions"] for r in b))),
                            "actions": _iv([r["n_actions"] for r in b])},
            }
    # the decay parameters and the corners
    for param, key in (("gamma", "decay_gamma"), ("delta", "decay_delta"), ("z", "decay_z")):
        out["decay"][param] = {n: four[n] for n in four if n.startswith(key + "_")}
    out["decay"]["corners"] = {n: four[n] for n in four if n.startswith("corner_")}
    out["decay"]["ranking"] = sorted(
        ((n, max(abs(v["delta"]) for v in four[n].values())) for n in four if n.startswith(("decay_", "corner_"))),
        key=lambda t: -t[1])
    # verdict agreement between the two interval forms
    disagreements = [(pooling, n, k) for pooling in out["points"] for n, d in out["points"][pooling].items()
                     for k, v in d.items() if v["status"] != "zero by structure"
                     and (v["status"] == "inert") != v["inert_by_bootstrap"]]
    out["interval_form_disagreements"] = disagreements
    return out


# --- fragments -------------------------------------------------------------------
def _pm(iv: dict, nd: int = 1) -> str:
    return f"${iv['mean']:.{nd}f} \\pm {iv['ci95']:.{nd}f}$"


def _hdr(tool: str) -> str:
    return (f"% GENERATED by {tool} from\n%   data/results/ch5_s51_sensitivity/numbers.json (the §5.1 re-run at the\n"
            f"%   chapter's pins; the attacker model pooled over its four profiles, 400 runs\n"
            f"%   per cell). Do not hand-edit; regenerate.\n")


def frag_body(out: dict) -> str:
    four = out["points"]["four"]
    fam = out["families"]

    def family_effect(f: str) -> str:
        v = fam[f]
        if v["verdict"] == "inert":
            return "inert"
        lo, hi = v["band"]
        e_lo, e_hi = v["ends"][f"x{lo:g}"]["none@0"], v["ends"][f"x{hi:g}"]["none@0"]
        slope = v["hosts_lost_per_doubling"]["none@0"]
        return (f"moved: {e_lo['point']['mean']:.1f} / {e_lo['centre']['mean']:.1f} / {e_hi['point']['mean']:.1f} hosts "
                f"at $\\times{lo:g}$ / declared / $\\times{hi:g}$ under no defence, {slope:.1f} lost per doubling "
                f"(Appendix~\\ref{{app:dwell-robustness}})")

    def shape_effect() -> str:
        # Every paired difference, at the declared dwell and at the corner, under
        # each condition: inert where its interval covers zero; otherwise the
        # sign and the largest magnitude, so the cell never rests on one
        # borderline cell.
        diffs = {(lab, key.split("|", 1)[1]): v["difference"]
                 for lab in ("centre", "lowslow_x4") for key, v in out["shape"][lab].items() if key.startswith("four|")}
        none_ok = all(abs(d["mean"]) <= d["ci95"] for (lab, k), d in diffs.items() if k == "none@0")
        defended = [d for (lab, k), d in diffs.items() if k != "none@0"]
        sep = [d for d in defended if abs(d["mean"]) > d["ci95"]]
        if none_ok and not sep:
            return "inert (Appendix~\\ref{app:exponential-shape})"
        if none_ok and all(d["mean"] < 0 for d in sep):
            worst = min(d["mean"] for d in sep)
            return (f"inert under no defence; under defence the concentrated draw reaches fewer hosts, "
                    f"by {abs(worst):.1f} at most (Appendix~\\ref{{app:exponential-shape}})")
        return "moved; see Appendix~\\ref{app:exponential-shape}"

    def mapping_effect() -> str:
        m = out["mapping"]["none@0"]
        return (f"the alternative reaches {m['forced_total']['hosts']['mean']:.1f} hosts against "
                f"{m['partial']['hosts']['mean']:.1f}, no defence (Appendix~\\ref{{app:experiment-one}})")

    def decay_effect(param: str, lo_name: str, hi_name: str) -> str:
        st = {k: v["status"] for n in (lo_name, hi_name) for k, v in four[n].items()}
        if all(s == "zero by structure" for s in st.values()):
            return "zero by structure: no profile net carries a jump of three stages"
        if all(s == "inert" for s in st.values()):
            return "inert"
        moved = sorted({k for k, s in st.items() if s == "moved"})
        lo_v, hi_v = four[lo_name]["none@0"], four[hi_name]["none@0"]
        return (f"moved under {', '.join(COND_LABEL[(k.split('@')[0], int(k.split('@')[1]))] for k in moved)}: "
                f"{lo_v['point']['mean']:.1f} / {lo_v['centre']['mean']:.1f} / {hi_v['point']['mean']:.1f} hosts, no defence "
                f"(Appendix~\\ref{{app:decay-robustness}})")

    rows = [
        ("Dwell times", [
            ("scan-shaped family", "35\\,s", "$\\times0.5$ to $\\times2$", family_effect("scan-shaped")),
            ("exploit-shaped family", "4.5\\,s", "$\\times0.5$ to $\\times2$", family_effect("exploit-shaped")),
            ("low-and-slow family", "45\\,s", "$\\times0.25$ to $\\times4$", family_effect("stealth-low-and-slow")),
            ("objective family", "36\\,s", "$\\times0.5$ to $\\times2$", family_effect("objective-execution")),
            ("the draw's shape", "exponential", "same-mean, concentrated", shape_effect()),
        ]),
        ("Mapping", [
            ("tactic to verb", "partial", "forced total", mapping_effect()),
        ]),
        ("Failure matrix", [
            ("forward rate", "0.25", "0.1 to 0.5", decay_effect("gamma", "decay_gamma_0.1", "decay_gamma_0.5")),
            ("backward rate", "0.25", "0.1 to 0.5", decay_effect("delta", "decay_delta_0.1", "decay_delta_0.5")),
            ("floor", "0.1", "0, 0.05", decay_effect("z", "decay_z_0", "decay_z_0.05")),
            ("the nine rules", "argued values", "held", "---"),
        ]),
    ]
    L = [_hdr("data/results/ch5_s51_sensitivity/analyse.py")]
    w = L.append
    w(r"\begin{table}[htbp]")
    w(r"  \centering")
    w(r"  % CAPTION DRAFT STATE 2026-09-17 --- voice pass owed.")
    w(r"  \caption[The declared inputs and what moved]{Each value the attacker model was given rather than derived, "
      r"grouped by the three inputs of Section~\ref{sec:execution}: the value declared, the range it was moved across "
      r"with the other inputs held at their declared values, and what happened to distinct hosts reached, read against "
      r"the interval at the declared value under no defence and under the random scheme at both intervals. "
      r"The dwell ranges follow the evidence tiers of Appendix~\ref{app:dwell-derivation}; the failure-matrix ranges "
      r"bracket the declared value on both sides (Appendix~\ref{app:weight-sets}). The draw's shape and the mapping "
      r"have no range and are compared against the alternative that was tried; the nine failure rules are single argued "
      r"values and are held. In the notation of Chapter~\ref{ch:attacker-model} the rows are $\mu_p$, $\tau_p$, "
      r"$\varphi$, $\gamma$, $\delta$, $z$ and $R$. Pooled over the four profiles, 400 runs per cell; the per-value "
      r"readings are Appendix~\ref{app:sensitivity}.}")
    w(r"  \label{tab:parameter-register}")
    w(r"  \tablestyle\setlength{\tabcolsep}{4pt}")
    w(r"  \begin{tabular}{@{}cP{3.0cm}P{2.0cm}P{2.6cm}P{6.6cm}@{}}")
    w(r"    \toprule")
    w(r"    & Input & Declared & Moved across & What moved \\")
    w(r"    \midrule")
    for gi, (group, items) in enumerate(rows):
        for ii, (name, val, band, eff) in enumerate(items):
            lead = f"\\rowgroup{{{len(items)}}}{{{group}}}" if ii == len(items) - 1 else ""
            w(f"    {lead} & {name} & {val} & {band} & {eff} \\\\")
        if gi < len(rows) - 1:
            w(r"    \midrule")
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def frag_families(out: dict) -> str:
    L = [_hdr("data/results/ch5_s51_sensitivity/analyse.py")]
    w = L.append
    w(r"\begin{table}[htbp]")
    w(r"\centering\footnotesize")
    w(r"% CAPTION DRAFT STATE 2026-09-17 --- voice pass owed.")
    w(r"\caption[Hosts reached at each family's band ends against its declared value]{Distinct hosts reached "
      r"at each dwell family's band ends against its declared value, the family moved as a whole with the "
      r"other three held, under no defence and under the random scheme at each interval. Pooled over the four "
      r"profiles, 400 runs per cell; intervals are 95\,\%. A family is inert when both ends sit inside the "
      r"interval at the declared value under every condition; the verdict column reads the criterion fixed "
      r"before the run.}")
    w(r"\label{tab:anchor-sensitivity}")
    w(r"\tablestyle\setlength{\tabcolsep}{4pt}")
    w(r"\begin{tabular}{@{}cP{3.2cm}>{\centering\arraybackslash}p{2.2cm}>{\centering\arraybackslash}p{2.2cm}>{\centering\arraybackslash}p{2.2cm}P{2.4cm}@{}}")
    w(r"\toprule")
    w(r"& Family & Band low & Declared & Band high & Verdict \\")
    w(r"\midrule")
    for ci, (cond, interval) in enumerate(CONDITIONS):
        key = f"{cond}@{interval}"
        for fi, fam in enumerate(FAMILIES):
            lo, hi = sweep.FAMILY_BANDS[fam]
            e_lo = out["families"][fam]["ends"][f"x{lo:g}"].get(key)
            e_hi = out["families"][fam]["ends"][f"x{hi:g}"].get(key)
            if not e_lo or not e_hi:
                continue
            st = {e_lo["status"], e_hi["status"]}
            verdict_txt = "inert" if st == {"inert"} else ("moved, both ends" if st == {"moved"} else "moved, one end")
            lead = f"\\rowgroup{{{len(FAMILIES)}}}{{{COND_LABEL[(cond, interval)]}}}" if fi == len(FAMILIES) - 1 else ""
            w(f"{lead} & {FAMILY_NAME[fam]} ($\\times{lo:g}$, $\\times{hi:g}$) & {_pm(e_lo['point'])} & {_pm(e_lo['centre'])} & {_pm(e_hi['point'])} & {verdict_txt} \\\\")
        if ci < len(CONDITIONS) - 1:
            w(r"\midrule")
    w(r"\bottomrule")
    w(r"\end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def frag_shape(out: dict) -> str:
    L = [_hdr("data/results/ch5_s51_sensitivity/analyse.py")]
    w = L.append
    w(r"\begin{table}[htbp]")
    w(r"\centering\footnotesize")
    w(r"% CAPTION DRAFT STATE 2026-09-17 --- voice pass owed.")
    w(r"\caption[The same-mean shape substitution]{Distinct hosts reached under a same-mean Erlang-4 draw on the "
      r"low-and-slow family against the declared exponential, paired by profile and seed, at the declared dwell and "
      r"at the top of the family's band. Pooled over the four profiles, 400 pairs per cell; intervals are 95\,\%. "
      r"The sign column counts the pairs in which the concentrated draw reached fewer, the same, and more hosts.}")
    w(r"\label{tab:shape-substitution}")
    w(r"\tablestyle\setlength{\tabcolsep}{4pt}")
    w(r"\begin{tabular}{@{}cP{2.8cm}>{\centering\arraybackslash}p{2.0cm}>{\centering\arraybackslash}p{2.0cm}>{\centering\arraybackslash}p{2.2cm}>{\centering\arraybackslash}p{2.6cm}@{}}")
    w(r"\toprule")
    w(r"& Condition & Erlang-4 & Exponential & Difference & Pairs lower / tied / higher \\")
    w(r"\midrule")
    for li, (label, title) in enumerate((("centre", "declared dwell"), ("lowslow_x4", "low-and-slow $\\times4$"))):
        rows = [(cond, interval, out["shape"][label].get(f"four|{cond}@{interval}")) for cond, interval in CONDITIONS]
        rows = [r for r in rows if r[2]]
        for ri, (cond, interval, v) in enumerate(rows):
            lead = f"\\rowgroup{{{len(rows)}}}{{{title}}}" if ri == len(rows) - 1 else ""
            s = v["signs"]
            w(f"{lead} & {COND_LABEL[(cond, interval)]} & {_pm(v['a'], 2)} & {_pm(v['b'], 2)} & {_pm(v['difference'], 2)} & {s['lower']} / {s['tied']} / {s['higher']} \\\\")
        if li == 0:
            w(r"\midrule")
    w(r"\bottomrule")
    w(r"\end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def frag_decay(out: dict) -> str:
    four = out["points"]["four"]
    L = [_hdr("data/results/ch5_s51_sensitivity/analyse.py")]
    w = L.append
    w(r"\begin{table}[htbp]")
    w(r"\centering\footnotesize")
    w(r"% CAPTION DRAFT STATE 2026-09-17 --- voice pass owed.")
    w(r"\caption[Hosts reached across the failure matrix's distance parameters]{Distinct hosts reached at each "
      r"distance parameter's band ends against its declared value, one at a time with the others held, and then "
      r"at the four corners of the two rates with the floor declared, under no defence and under the random scheme "
      r"at each interval. Pooled over the four profiles, 400 runs per cell; intervals are 95\,\%. The floor's rows "
      r"are bit-identical to the declared point: no profile net carries a jump of three stages, so its sensitivity "
      r"is zero by structure rather than by measurement.}")
    w(r"\label{tab:decay-sensitivity}")
    w(r"\tablestyle\setlength{\tabcolsep}{4pt}")
    w(r"\begin{tabular}{@{}cP{3.4cm}>{\centering\arraybackslash}p{2.1cm}>{\centering\arraybackslash}p{2.1cm}>{\centering\arraybackslash}p{2.1cm}P{2.6cm}@{}}")
    w(r"\toprule")
    w(r"& Parameter & Band low & Declared & Band high & Verdict \\")
    w(r"\midrule")
    params = (("forward rate $\\gamma$ (0.1, 0.5)", "decay_gamma_0.1", "decay_gamma_0.5"),
              ("backward rate $\\delta$ (0.1, 0.5)", "decay_delta_0.1", "decay_delta_0.5"),
              ("floor $z$ (0, 0.05)", "decay_z_0", "decay_z_0.05"))
    for ci, (cond, interval) in enumerate(CONDITIONS):
        key = f"{cond}@{interval}"
        block = []
        for title, lo_n, hi_n in params:
            lo_v, hi_v = four.get(lo_n, {}).get(key), four.get(hi_n, {}).get(key)
            if lo_v and hi_v:
                st = {lo_v["status"], hi_v["status"]}
                vt = ("zero by structure" if st == {"zero by structure"} else "inert" if st == {"inert"}
                      else "moved, both ends" if st == {"moved"} else "moved, one end")
                block.append((title, _pm(lo_v["point"]), _pm(lo_v["centre"]), _pm(hi_v["point"]), vt))
        corners = [(n, four[n].get(key)) for n in sorted(four) if n.startswith("corner_")]
        for n, v in corners:
            if v:
                g, d = n.split("_")[2], n.split("_")[4]
                block.append((f"corner $\\gamma={g}$, $\\delta={d}$", "---", _pm(v["centre"]), _pm(v["point"]), v["status"]))
        for bi, (title, a, b, c, vt) in enumerate(block):
            lead = f"\\rowgroup{{{len(block)}}}{{{COND_LABEL[(cond, interval)]}}}" if bi == len(block) - 1 else ""
            w(f"{lead} & {title} & {a} & {b} & {c} & {vt} \\\\")
        if ci < len(CONDITIONS) - 1:
            w(r"\midrule")
    w(r"\bottomrule")
    w(r"\end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def per_run_csv(cells: dict) -> None:
    """tools/ch5_sensitivity_figure.py's contract: arm, family, m_scan, m_exploit,
    m_stealth, m_objective, mtd_interval (blank for none), compromised_count."""
    cols = ["arm", "family", "profile", "seed", "point", "m_scan", "m_exploit", "m_stealth",
            "m_objective", "mtd_interval", "compromised_count"]
    with PER_RUN.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh)
        wr.writerow(cols)
        for (name, profile, cond, interval), runs in cells.items():
            point = POINTS[name]
            if point["kind"] not in ("centre", "dwell", "shape"):
                continue
            f = point.get("factors", {})
            fam = "erlang4" if point.get("timing") == "erlang4" else "exponential"
            for r in runs:
                wr.writerow(["movement", fam, profile, r["seed"], name,
                             f.get("scan-shaped", 1.0), f.get("exploit-shaped", 1.0),
                             f.get("stealth-low-and-slow", 1.0), f.get("objective-execution", 1.0),
                             "" if cond == "none" else interval, r["compromised"]])


def preview(out: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), sharey=True)
    for ax, fam in zip(axes, FAMILIES):
        lo, hi = sweep.FAMILY_BANDS[fam]
        for (cond, interval), style in zip(CONDITIONS, ("k-o", "b-s", "g-^")):
            key = f"{cond}@{interval}"
            xs, ys, es = [], [], []
            for mult, name in ((lo, f"dwell_{fam}_x{lo:g}"), (1.0, None), (hi, f"dwell_{fam}_x{hi:g}")):
                v = out["points"]["four"].get(name or f"dwell_{fam}_x{lo:g}", {}).get(key)
                if not v:
                    continue
                iv = v["centre"] if name is None else v["point"]
                xs.append(mult); ys.append(iv["mean"]); es.append(iv["ci95"])
            if xs:
                ax.errorbar(xs, ys, yerr=es, fmt=style, capsize=3, label=COND_LABEL[(cond, interval)].replace("\\,", " "))
        ax.set_xscale("log", base=2); ax.set_title(FAMILY_NAME[fam]); ax.set_xlabel("multiple of declared")
    axes[0].set_ylabel("distinct hosts reached"); axes[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(HERE / "preview_families.png", dpi=110)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partial", action="store_true", help="read an incomplete corpus (no fragments written)")
    parser.add_argument("--no-sim05", action="store_true", help="skip the scan of the defended corpus")
    args = parser.parse_args(argv)
    cells, sanity = load(args.partial)
    print("sanity:", json.dumps(sanity))
    out = {"sanity": sanity}
    if not args.no_sim05:
        out["sim05"] = sim05_check(cells)
        print("sim05:", json.dumps({k: v for k, v in out["sim05"].items() if k != "first_mismatches"}))
    out.update(analyse(cells))
    for fam, v in out["families"].items():
        slope = {k: round(x, 2) for k, x in v["hosts_lost_per_doubling"].items()}
        print(f"family {FAMILY_NAME[fam]:20s} {v['verdict']:6s} moved under {v['moved_under']} hosts lost per doubling {slope}")
    for n, mag in out["decay"]["ranking"]:
        print(f"decay {n:32s} max |delta| {mag:.2f}")
    print("interval-form disagreements:", out["interval_form_disagreements"])
    NUMBERS.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    per_run_csv(cells)
    preview(out)
    if not args.partial:
        (TAB_DIR / "tab_5-1a_declared_inputs.tex").write_text(frag_body(out), encoding="utf-8")
        (TAB_DIR / "tab_C-1a_family_sensitivity.tex").write_text(frag_families(out), encoding="utf-8")
        (TAB_DIR / "tab_C-2a_shape_substitution.tex").write_text(frag_shape(out), encoding="utf-8")
        (TAB_DIR / "tab_C-3a_decay_sensitivity.tex").write_text(frag_decay(out), encoding="utf-8")
        print("fragments written to", TAB_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
