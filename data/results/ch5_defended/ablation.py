#!/usr/bin/env python3
"""§5.4 Ablation of the failure matrix: the APT attacker model against the same
model with every factor of the failure matrix set to one (run_corpus.py group
``blind``), so that a failure routes on the base weights as a success does.
Plan: Marc 2026-09-26 ("we tried it and it didn't work, here's the ablation
study"); reshaped 2026-09-28 (Marc, chat) into prediction, manipulation check,
outcome: the failure matrix changes where the attacker goes after a failure,
not what it achieves.

SCOPE. The four profiles, targeted, under no defence and the two spanning
mechanisms (IP shuffle, OS diversity) at 200 s and 2 000 s. Seeds 0-99 come
from the shared corpus (runs.jsonl); seeds 100-999 from runs_ablation.jsonl
(run_corpus.py, ABLATION=1), the same code and configuration (seed 0 and seed 3
re-run bit-identical on 2026-09-28). Nothing else is claimed.

READS.
  behaviour (the manipulation check, Figure 5.x(a)), no defence only:
    after a failed initial access, the next action the attacker takes, in four
    kinds: back to reconnaissance; an action that fails (with the subset whose
    precondition is unmet, so it fails before it runs, section 4.5's wording,
    kept apart for the text); an action that succeeds but compromises no host
    (a scan or an enumeration); an action that compromises a host (the
    corpus's COMPROMISE set). Dwell-only tactics between are passed over.
    Per profile: the matrix multiplies weights, so a profile whose net has no
    move from initial access back to reconnaissance (c_2) cannot be sent there
    with or without it; pooling would mix that in.
    After every other failure: the share of next tactics that differ between
    the arms (total variation distance between the two next-tactic
    distributions), per failed tactic with at least 200 failures in each arm.
  outcome (Figure 5.x(b), Table 5.5), per condition, the four profiles pooled:
    hosts   mean hosts compromised per run, read as NCR (hosts / N, N = 50)
    NCR reduction  1 - mean(hosts | defence) / mean(hosts | none), each arm
            against its own no-defence runs (section 4.5)
    time lost per MTD deployment, disruption.py's estimator unchanged, 2 000 s
            only; kept in the JSON, not in the table (its interval has no
            declared bound, so it cannot show an absence of effect)
  per profile: the host difference and its interval, so a pooled null cannot
    hide profiles that move in opposite directions.

DIFFERENCE (with minus without). Every seed and profile runs in both arms, so
the bootstrap resamples (profile, seed) units jointly for both arms: 2 000
resamples, 95 % percentile intervals. EFFECT SIZE. Cohen's d on hosts per seed
(the four profiles at one seed averaged, the seed being the independent unit),
with the pooled SD of the two arms' per-seed means: the form section 4.5.4's
Scott-Knott ESD merge uses and the form Cohen's 0.2 is calibrated on.
Negligible below 0.2. The paired form (d_z, mean difference over the SD of the
differences) is kept in the JSON; it grows with the correlation between arms
on a shared seed and is not comparable with the 0.2 threshold.

Usage: python data/results/ch5_defended/ablation.py
Output: ablation_numbers.json beside the corpus, and the section 5.4 table,
docs/thesis/tables/tab_5-4a_ablation.tex (generated; never hand-edit). The
figure is drawn from the JSON by tools/ch5_ablation_figure.py.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

import disruption as D

HERE = Path(__file__).resolve().parent
OUT = HERE / "ablation_numbers.json"
EXTRA = HERE / "runs_ablation.jsonl"
TABLE = HERE.parents[2] / "docs" / "thesis" / "tables" / "tab_5-4a_ablation.tex"
N_HOSTS = 50
LABEL = {"none": "no defence", "ip_shuffle": "IP shuffle", "os_diversity": "OS diversity"}
FOUR = ("objective_exfiltration", "objective_impact", "objective_exfiltration_impact", "objective_none_c2")
SPANNING = ("ip_shuffle", "os_diversity")
CONDS = ("none",) + SPANNING
INTERVALS = (200, 2_000)
ARMS = {"core": "with the failure matrix", "blind": "every factor set to one"}
KINDS = ("reconnaissance", "fails", "succeeds", "compromises")  # partition; fails_unmet is a subset of fails
MIN_FAILURES = 200
N_BOOT = 2_000
SEED = 20260926


def _behaviour(records: list) -> tuple[Counter, Counter]:
    """The next action after each failed initial access, by kind; and the next
    tactic after every failure, keyed (failed tactic, next tactic)."""
    after_ia, route = Counter(), Counter()
    for i, x in enumerate(records[:-1]):
        if x[3] != "failure":
            continue
        route[(x[0], records[i + 1][0])] += 1
        if x[0] != "initial-access":
            continue
        j = i + 1
        while j < len(records) and records[j][9] != "action-bearing":
            j += 1
        if j == len(records):
            continue
        y = records[j]
        if y[0] == "reconnaissance":
            after_ia["reconnaissance"] += 1
        elif y[3] == "failure":
            after_ia["fails"] += 1
            if y[2] == "PRECONDITION_UNMET":
                after_ia["fails_unmet"] += 1  # a subset of fails: it fails before it runs
        elif (y[1], y[2]) in D.COMPROMISE:
            after_ia["compromises"] += 1
        else:
            after_ia["succeeds"] += 1  # a scan or enumeration: runs, compromises no host
    return after_ia, route


def load() -> list[dict]:
    out, errors = [], 0
    for path in (D.RUNS, EXTRA):
        if not path.exists():
            continue
        with path.open() as f:
            for line in f:
                head = line[:400]
                if not ('"group": "core"' in head or '"group": "blind"' in head):
                    continue
                if '"regime": "shifted"' not in head or '"objective": "targeted"' not in head:
                    continue
                r = json.loads(line)
                if r["arm"] != "movement" or r["profile"] not in FOUR or r["condition"] not in CONDS:
                    continue
                if r["condition"] != "none" and r["interval"] not in INTERVALS:
                    continue
                if r["group"] == "core" and r["overlay"] != "v4_failure_only":
                    continue
                if "error" in r:  # a dead cell must be visible, never silently absent
                    errors += 1
                    continue
                T = r["termination_time"]
                comp = [x[8] for x in r["records"] if (x[1], x[2]) in D.COMPROMISE]
                after_ia, route = _behaviour(r["records"]) if r["condition"] == "none" else (Counter(), Counter())
                out.append({
                    "group": r["group"], "arm": "movement", "profile": r["profile"], "seed": r["seed"],
                    "cond": r["condition"], "interval": r["interval"], "T": T, "hosts": r["compromised"],
                    "comp": np.sort(np.minimum(np.array(comp, float), T)),
                    "landings": [e[2] for e in r["mtd_executions"] if -D.EDGES[0] <= e[2] < T],
                    "durations": [e[3] for e in r["mtd_executions"]],
                    "after_ia": after_ia, "route": route,
                })
    if errors:
        raise SystemExit(f"{errors} error rows in the ablation cells; refusing to read")
    return out


def cell(runs, group, cond, interval):
    rs = [r for r in runs if r["group"] == group and r["cond"] == cond and (cond == "none" or r["interval"] == interval)]
    cell = {(r["profile"], r["seed"]): r for r in rs}
    if len(cell) != len(rs):
        raise SystemExit(f"duplicate (profile, seed) in {group}/{cond}/{interval}")
    return cell


def behaviour(none: dict) -> dict:
    """The manipulation check, per profile, on the no-defence runs."""
    out = {}
    for p in FOUR:
        row = {}
        for g in ARMS:
            ia, route = Counter(), Counter()
            for (prof, _), r in none[g].items():
                if prof == p:
                    ia.update(r["after_ia"])
                    route.update(r["route"])
            n = sum(ia[k] for k in KINDS)
            fails = Counter()
            for (a, _), v in route.items():
                fails[a] += v
            row[g] = {"failed_initial_access": n,
                      "failures": sum(fails.values()),
                      "after_failed_initial_access": {k: ia[k] / n if n else 0.0 for k in KINDS + ("fails_unmet",)},
                      "_route": route, "_fails": fails}
        tv = {}
        for a in set(row["core"]["_fails"]) | set(row["blind"]["_fails"]):
            if a == "initial-access":
                continue
            nw, nb = row["core"]["_fails"][a], row["blind"]["_fails"][a]
            if nw < MIN_FAILURES or nb < MIN_FAILURES:
                continue
            nxt = {b for (x, b) in row["core"]["_route"] if x == a} | {b for (x, b) in row["blind"]["_route"] if x == a}
            tv[a] = 0.5 * sum(abs(row["core"]["_route"][(a, b)] / nw - row["blind"]["_route"][(a, b)] / nb) for b in nxt)
        # weighted by the failures behind each tactic, in the arm with the matrix
        fw = {a: row["core"]["_fails"][a] for a in tv}
        for g in ARMS:
            del row[g]["_route"], row[g]["_fails"]
        row["next_tactic_changed_after_other_failures"] = {
            "by_tactic": dict(sorted(tv.items())),
            "max": max(tv.values()) if tv else None,
            "weighted_mean": float(sum(tv[a] * fw[a] for a in tv) / sum(fw.values())) if tv else None,
        }
        out[p] = row
    return out


def _boot_diff(hw, hb, idx):
    dh = hw[idx].mean(1) - hb[idx].mean(1)
    return [float(np.percentile(dh, 2.5)), float(np.percentile(dh, 97.5))]


def main() -> None:
    runs = load()
    rng = np.random.default_rng(SEED)
    none = {g: cell(runs, g, "none", 0) for g in ARMS}
    units = sorted(set(none["core"]) & set(none["blind"]))
    seeds_all = sorted({s for _, s in units})
    out = {"scope": "four profiles, targeted; no defence, IP shuffle and OS diversity at 200 s and 2 000 s; "
                    f"seeds {seeds_all[0]}-{seeds_all[-1]} ({len(seeds_all)})",
           "arms": ARMS, "units_none": len(units), "seeds": len(seeds_all),
           "behaviour": behaviour(none), "reads": {}}

    rows = {}
    for label, cond, iv in [("none", "none", 0)] + [(f"{c}|{i}", c, i) for c in SPANNING for i in INTERVALS]:
        w, wo = cell(runs, "core", cond, iv), cell(runs, "blind", cond, iv)
        u = sorted(set(w) & set(wo) & set(none["core"]) & set(none["blind"]))
        hw = np.array([w[k]["hosts"] for k in u], float)
        hb = np.array([wo[k]["hosts"] for k in u], float)
        n0w = np.array([none["core"][k]["hosts"] for k in u], float)
        n0b = np.array([none["blind"][k]["hosts"] for k in u], float)
        by_w, by_b = defaultdict(list), defaultdict(list)
        for k, a, b in zip(u, hw, hb):
            by_w[k[1]].append(a)
            by_b[k[1]].append(b)
        seeds = sorted(by_w)
        dz = np.array([np.mean(by_w[s]) - np.mean(by_b[s]) for s in seeds])
        d_z = float(dz.mean() / dz.std(ddof=1)) if dz.std(ddof=1) > 0 else 0.0
        mw = np.array([np.mean(by_w[s]) for s in seeds])
        mb = np.array([np.mean(by_b[s]) for s in seeds])
        sp = np.sqrt((mw.var(ddof=1) + mb.var(ddof=1)) / 2)
        d_pooled = float((mw.mean() - mb.mean()) / sp) if sp > 0 else 0.0
        # the interval on d: the same resample of seeds, d recomputed
        sidx = rng.integers(0, len(seeds), size=(N_BOOT, len(seeds)))
        dboot = []
        for ix in sidx:
            a, b = mw[ix], mb[ix]
            s = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
            dboot.append((a.mean() - b.mean()) / s if s > 0 else 0.0)
        idx = rng.integers(0, len(u), size=(N_BOOT, len(u)))
        row = {"units": len(u), "seeds": len(seeds),
               "hosts_with": float(hw.mean()), "hosts_without": float(hb.mean()),
               "hosts_diff": float(hw.mean() - hb.mean()),
               "hosts_diff_ci95": _boot_diff(hw, hb, idx),
               "cohen_d_per_seed": d_pooled,
               "cohen_d_ci95": [float(np.percentile(dboot, 2.5)), float(np.percentile(dboot, 97.5))],
               "cohen_d_z_per_seed": d_z,
               "hosts_with_ci95": [float(np.percentile(hw[idx].mean(1), 2.5)), float(np.percentile(hw[idx].mean(1), 97.5))],
               "hosts_without_ci95": [float(np.percentile(hb[idx].mean(1), 2.5)), float(np.percentile(hb[idx].mean(1), 97.5))]}
        per = {}
        for p in FOUR:
            pk = [i for i, k in enumerate(u) if k[0] == p]
            a, b = hw[pk], hb[pk]
            pidx = rng.integers(0, len(pk), size=(N_BOOT, len(pk)))
            per[p] = {"hosts_with": float(a.mean()), "hosts_without": float(b.mean()),
                      "hosts_diff": float(a.mean() - b.mean()), "hosts_diff_ci95": _boot_diff(a, b, pidx)}
        row["per_profile"] = per
        if cond != "none":
            rw, rb = 1 - hw.mean() / n0w.mean(), 1 - hb.mean() / n0b.mean()
            br = (1 - hw[idx].mean(1) / n0w[idx].mean(1)) - (1 - hb[idx].mean(1) / n0b[idx].mean(1))
            row.update({"ncr_reduction_with": float(rw), "ncr_reduction_without": float(rb),
                        "ncr_reduction_diff": float(rw - rb),
                        "ncr_reduction_diff_ci95": [float(np.percentile(br, 2.5)), float(np.percentile(br, 97.5))]})
            if iv == 2_000:
                runs_w = [w[k] for k in u]
                runs_b = [wo[k] for k in u]
                plac_w = {("movement", k[0], k[1]): none["core"][k] for k in u}
                plac_b = {("movement", k[0], k[1]): none["blind"][k] for k in u}
                nw, dw = D._stack(runs_w, None)
                pnw, pdw = D._stack(runs_w, plac_w)
                nb, db = D._stack(runs_b, None)
                pnb, pdb = D._stack(runs_b, plac_b)

                def tl(ix, num, den, pnum, pden):
                    return D._time_lost(num[ix].sum(0), den[ix].sum(0)) - D._time_lost(pnum[ix].sum(0), pden[ix].sum(0))

                allix = np.arange(len(u))
                tw, tb = tl(allix, nw, dw, pnw, pdw), tl(allix, nb, db, pnb, pdb)
                bt = np.array([tl(ix, nw, dw, pnw, pdw) - tl(ix, nb, db, pnb, pdb) for ix in idx])
                bw = np.array([tl(ix, nw, dw, pnw, pdw) for ix in idx])
                bb = np.array([tl(ix, nb, db, pnb, pdb) for ix in idx])
                row.update({"time_lost_with": tw, "time_lost_with_ci95": [float(np.percentile(bw, 2.5)), float(np.percentile(bw, 97.5))],
                            "time_lost_without": tb, "time_lost_without_ci95": [float(np.percentile(bb, 2.5)), float(np.percentile(bb, 97.5))],
                            "time_lost_diff": tw - tb,
                            "time_lost_diff_ci95": [float(np.percentile(bt, 2.5)), float(np.percentile(bt, 97.5))]})
        rows[label] = row
    out["reads"] = rows
    OUT.write_text(json.dumps(out, indent=1))
    write_table(rows)
    print(f"wrote {OUT.relative_to(HERE.parents[2])}  ({out['scope']})")
    print("\nBEHAVIOUR (no defence): next action after a failed initial access")
    for p, b in out["behaviour"].items():
        for g in ARMS:
            s = b[g]["after_failed_initial_access"]
            print(f"  {p:31s} {g:5s} n={b[g]['failed_initial_access']:6d} of {b[g]['failures']:7d} failures  "
                  + "  ".join(f"{k} {s[k]:.2f}" for k in KINDS))
        t = b["next_tactic_changed_after_other_failures"]
        print(f"  {'':31s} other failures: next tactic changed max {t['max']:.2f}, weighted mean {t['weighted_mean']:.2f}")
    for label, r in rows.items():
        print(f"\n{label}: units {r['units']}  hosts {r['hosts_with']:.2f} vs {r['hosts_without']:.2f}  "
              f"diff {r['hosts_diff']:+.2f} [{r['hosts_diff_ci95'][0]:+.2f}, {r['hosts_diff_ci95'][1]:+.2f}]  "
              f"d {r['cohen_d_per_seed']:+.2f} [{r['cohen_d_ci95'][0]:+.2f}, {r['cohen_d_ci95'][1]:+.2f}] (d_z {r['cohen_d_z_per_seed']:+.2f})")
        for p, q in r["per_profile"].items():
            print(f"   {p:31s} {q['hosts_with']:.2f} vs {q['hosts_without']:.2f}  diff {q['hosts_diff']:+.2f} "
                  f"[{q['hosts_diff_ci95'][0]:+.2f}, {q['hosts_diff_ci95'][1]:+.2f}]")
        if "ncr_reduction_with" in r:
            print(f"   NCR reduction {r['ncr_reduction_with']:.3f} vs {r['ncr_reduction_without']:.3f}  diff {r['ncr_reduction_diff']:+.3f} "
                  f"[{r['ncr_reduction_diff_ci95'][0]:+.3f}, {r['ncr_reduction_diff_ci95'][1]:+.3f}]")
        if "time_lost_with" in r:
            print(f"   time lost {r['time_lost_with']:.0f} s vs {r['time_lost_without']:.0f} s  diff {r['time_lost_diff']:+.0f} "
                  f"[{r['time_lost_diff_ci95'][0]:+.0f}, {r['time_lost_diff_ci95'][1]:+.0f}]")


def _sg(x: float, nd: int) -> str:
    """A signed value; one that rounds to zero carries no sign."""
    v = f"{x:+.{nd}f}"
    return v[1:] if float(v) == 0 else v


def _s(x: float, nd: int) -> str:
    return "$" + _sg(x, nd) + "$"


def _n(x: float, nd: int) -> str:
    return f"${x:.{nd}f}$"


def _iv(lo: float, hi: float, nd: int) -> str:
    return f"[${_sg(lo, nd)}$, ${_sg(hi, nd)}$]"


def write_table(rows: dict) -> None:
    """Table 5.5: the outcome read of Figure 5.x(b) with its differences. Two
    groups, each the same three columns: what the attacker achieves (NCR) and
    what the defence achieves against it (NCR reduction)."""
    order = [("none", "no MTD"), ("ip_shuffle|200", "IP shuffle, 200\\,s"), ("ip_shuffle|2000", "IP shuffle, 2\\,000\\,s"),
             ("os_diversity|200", "OS diversity, 200\\,s"), ("os_diversity|2000", "OS diversity, 2\\,000\\,s")]
    body = []
    for key, label in order:
        r = rows[key]
        dlo, dhi = (v / N_HOSTS for v in r["hosts_diff_ci95"])
        clo, chi = r["cohen_d_ci95"]
        cells = [label, f"{r['hosts_with'] / N_HOSTS:.3f}", f"{r['hosts_without'] / N_HOSTS:.3f}",
                 _s(r["hosts_diff"] / N_HOSTS, 3) + r"\newline " + _iv(dlo, dhi, 3),
                 _s(r["cohen_d_per_seed"], 2) + r"\newline " + _iv(clo, chi, 2)]
        if "ncr_reduction_diff" in r:
            lo, hi = r["ncr_reduction_diff_ci95"]
            cells += [_n(r["ncr_reduction_with"], 3), _n(r["ncr_reduction_without"], 3),
                      _s(r["ncr_reduction_diff"], 3) + r"\newline " + _iv(lo, hi, 3)]
        else:
            cells += ["---", "---", "---"]
        body.append("    " + " & ".join(cells) + r" \\")
    seeds = rows["none"]["seeds"]
    tex = [
        "% GENERATED by data/results/ch5_defended/ablation.py from ablation_numbers.json;",
        "% never hand-edit. Section 5.4; the outcome read of fig:ablation(b).",
        r"\begin{table}[htbp]",
        r"  \centering",
        (r"  \caption[The APT attacker model with and without the failure matrix]{The APT attacker model, averaged over $c_1$ to $c_4$, "
         r"with the failure matrix and without it, on the same %s seeds: NCR, Cohen's $d$ on hosts compromised per seed, and "
         r"NCR reduction (Section~\ref{sec:evaluation-metrics}). Each difference is with minus without, with its 95\,\%% "
         r"bootstrap interval over runs paired by seed.}") % fmt_seeds(seeds),
        r"  \label{tab:ablation}",
        r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}",
        r"  \begin{tabular}{@{}P{2.4cm}cc>{\centering\arraybackslash}p{2.4cm}>{\centering\arraybackslash}p{2.2cm}cc>{\centering\arraybackslash}p{2.4cm}@{}}",
        r"    \toprule",
        r"    & \multicolumn{4}{c}{NCR} & \multicolumn{3}{c}{NCR reduction} \\",
        r"    \cmidrule(lr){2-5}\cmidrule(lr){6-8}",
        r"    MTD & with & without & difference & $d$ & with & without & difference \\",
        r"    \midrule",
    ] + body + [r"    \bottomrule", r"  \end{tabular}", r"\end{table}", ""]
    TABLE.write_text("\n".join(tex))
    print(f"wrote {TABLE.relative_to(HERE.parents[2])}")


def fmt_seeds(n: int) -> str:
    return f"{n:,}".replace(",", r"\,")


if __name__ == "__main__":
    main()
