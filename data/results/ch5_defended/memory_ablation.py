#!/usr/bin/env python3
"""§5.4.2 Vulnerability memory — the read half of run_memory_ablation.py.

Reads runs_memory.jsonl and writes memory_ablation_numbers.json, per pool
(services per operating system) and condition:

  manipulation check  exploit success per roll (wins / rolls, the OS check's
                      refusals excluded), the share of attempts the OS check
                      refuses, vulnerabilities won on two or more hosts per
                      run, and the network's distinct vulnerabilities (the
                      pool axis in a reader's unit)
  outcome             hosts compromised per run, per arm with its interval;
                      on minus off and perfect minus off, paired by seed, with
                      Cohen's d in section 5.4.1's form (ablation.py: the four
                      profiles at one seed averaged, pooled SD of the two
                      arms' per-seed means) and its interval; ASP (a run
                      reaching a database host); under each mechanism, NCR
                      reduction and ASP reduction against the same arm's own
                      no-MTD runs at the same pool

Every difference is read WITHIN a pool: a thinner pool changes the network, so
the memory-off attacker also moves across pools. 2 000 resamples of (profile,
seed) units, 95 % percentile intervals, as ablation.py.

Usage: python data/results/ch5_defended/memory_ablation.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs_memory.jsonl"
OUT = HERE / "memory_ablation_numbers.json"
N_BOOT = 2_000
SEED = 20260930
HOSTS = 50


def load():
    cells = defaultdict(dict)  # (memory, pool, condition) -> {(profile, seed): row}
    errors = 0
    with open(RUNS, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if "error" in r:
                errors += 1
                continue
            cells[(r["memory"], r["pool"], r["condition"])][(r["profile"], r["seed"])] = r
    return cells, errors


def _ci(x):
    return [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]


def _per_seed(units, v):
    by = defaultdict(list)
    for k, x in zip(units, v):
        by[k[1]].append(x)
    seeds = sorted(by)
    return seeds, np.array([np.mean(by[s]) for s in seeds])


def _d(a, b):
    sp = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return float((a.mean() - b.mean()) / sp) if sp > 0 else 0.0


def compare(arm, off, units, rng):
    """arm minus off on hosts, paired by (profile, seed)."""
    ha = np.array([arm[k]["compromised"] for k in units], float)
    hb = np.array([off[k]["compromised"] for k in units], float)
    idx = rng.integers(0, len(units), size=(N_BOOT, len(units)))
    _, ma = _per_seed(units, ha)
    _, mb = _per_seed(units, hb)
    sidx = rng.integers(0, len(ma), size=(N_BOOT, len(ma)))
    return {"hosts_diff": float(ha.mean() - hb.mean()),
            "hosts_diff_ci95": _ci(ha[idx].mean(1) - hb[idx].mean(1)),
            "cohen_d": _d(ma, mb),
            "cohen_d_ci95": _ci([_d(ma[i], mb[i]) for i in sidx])}


def describe(c, units, rng):
    rows = [c[k] for k in units]
    hosts = np.array([r["compromised"] for r in rows], float)
    asp = np.array([r["database_hosts_reached"] > 0 for r in rows], float)
    rolls = sum(r["rolls"] for r in rows)
    idx = rng.integers(0, len(units), size=(N_BOOT, len(units)))
    return {"hosts": float(hosts.mean()), "hosts_ci95": _ci(hosts[idx].mean(1)),
            "ncr": float(hosts.mean() / HOSTS), "asp": float(asp.mean()),
            "roll_success": sum(r["wins"] for r in rows) / rolls if rolls else None,
            "refused_share": sum(r["refused"] for r in rows) / max(1, rolls + sum(r["refused"] for r in rows)),
            "types_rewon": float(np.mean([r["types_rewon"] for r in rows])),
            "vuln_types": float(np.mean([r["vuln_types"] for r in rows])),
            "_hosts": hosts, "_asp": asp}


def main() -> None:
    cells, errors = load()
    rng = np.random.default_rng(SEED)
    pools = sorted({k[1] for k in cells})
    order = ("none", "service_diversity", "os_diversity")
    conds = sorted({k[2] for k in cells}, key=order.index)
    out = {"errors": errors, "pools": pools, "conditions": conds, "reads": {}}
    for pool in pools:
        for cond in conds:
            arms = {m: cells.get((m, pool, cond), {}) for m in ("off", "on", "perfect")}
            base = {m: cells.get((m, pool, "none"), {}) for m in arms}
            units = sorted(set.intersection(*(set(a) for a in arms.values()), *(set(b) for b in base.values())))
            if not units:
                continue
            desc = {m: describe(arms[m], units, rng) for m in arms}
            row = {"units": len(units), "seeds": len({s for _, s in units}),
                   "arms": {m: {k: v for k, v in d.items() if not k.startswith("_")} for m, d in desc.items()},
                   "on_minus_off": compare(arms["on"], arms["off"], units, rng),
                   "perfect_minus_off": compare(arms["perfect"], arms["off"], units, rng)}
            if cond != "none":
                idx = rng.integers(0, len(units), size=(N_BOOT, len(units)))
                red = {}
                for m in arms:
                    h = desc[m]["_hosts"]
                    h0 = np.array([base[m][k]["compromised"] for k in units], float)
                    a = desc[m]["_asp"]
                    a0 = np.array([base[m][k]["database_hosts_reached"] > 0 for k in units], float)
                    red[m] = {"ncr_reduction": float(1 - h.mean() / h0.mean()),
                              "ncr_reduction_ci95": _ci(1 - h[idx].mean(1) / h0[idx].mean(1)),
                              "asp_reduction": float(1 - a.mean() / a0.mean()) if a0.mean() > 0 else None}
                row["reduction"] = red
            out["reads"][f"{pool}|{cond}"] = row
    OUT.write_text(json.dumps(out, indent=1))
    print(f"errors {errors}")
    print("pool cond            types  succ(off/on/perf)   rewon(off/on)  hosts off/on/perf     on-off d [ci]            perf-off d        ASP off/on")
    for key, r in out["reads"].items():
        pool, cond = key.split("|")
        a = r["arms"]
        o, p = r["on_minus_off"], r["perfect_minus_off"]
        print(f"{pool:>4} {cond:<16} {a['off']['vuln_types']:5.0f}  "
              f"{a['off']['roll_success']:.2f}/{a['on']['roll_success']:.2f}/{a['perfect']['roll_success']:.2f}    "
              f"{a['off']['types_rewon']:5.1f}/{a['on']['types_rewon']:5.1f}   "
              f"{a['off']['hosts']:5.2f}/{a['on']['hosts']:5.2f}/{a['perfect']['hosts']:5.2f}   "
              f"{o['cohen_d']:+.2f} [{o['cohen_d_ci95'][0]:+.2f},{o['cohen_d_ci95'][1]:+.2f}]   "
              f"{p['cohen_d']:+.2f} [{p['cohen_d_ci95'][0]:+.2f},{p['cohen_d_ci95'][1]:+.2f}]   "
              f"{a['off']['asp']:.2f}/{a['on']['asp']:.2f}")
        if "reduction" in r:
            red = r["reduction"]
            print(f"{'':22}NCR reduction off {red['off']['ncr_reduction']:+.3f} on {red['on']['ncr_reduction']:+.3f} "
                  f"perfect {red['perfect']['ncr_reduction']:+.3f}; ASP reduction off {red['off']['asp_reduction']} on {red['on']['asp_reduction']}")


TABLE = HERE.parents[2] / "docs" / "thesis" / "tables" / "tab_5-4b_ablation_memory.tex"
COND_LABEL = {"none": "no MTD", "service_diversity": "service diversity, 200\\,s",
              "os_diversity": "OS diversity, 200\\,s"}


def _f(x: float, nd: int, sign: bool = False) -> str:
    if sign and round(x, nd) == 0:
        return f"{0:.{nd}f}"
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return s.replace("-", "$-$").replace("+", "$+$") if sign else s


def write_table(out: dict) -> None:
    """Section 5.4.2's table: per condition and pool, exploit success and hosts
    compromised per arm, and Cohen's d against the memory off with its interval."""
    seeds = max(r["seeds"] for r in out["reads"].values())
    body = []
    for cond in out["conditions"]:
        body.append(r"    \addlinespace" if body else "")
        body.append(rf"    \multicolumn{{8}}{{@{{}}l}}{{\emph{{{COND_LABEL[cond]}}}}} \\")
        for pool in out["pools"]:
            r = out["reads"][f"{pool}|{cond}"]
            a, o, p = r["arms"], r["on_minus_off"], r["perfect_minus_off"]
            lo, hi = o["cohen_d_ci95"]
            plo, phi = p["cohen_d_ci95"]
            body.append(
                f"    {pool} & {_f(a['off']['roll_success'], 2)} & {_f(a['on']['roll_success'], 2)} & "
                f"{_f(a['off']['hosts'], 2)} & {_f(a['on']['hosts'], 2)} & {_f(a['perfect']['hosts'], 2)} & "
                f"{_f(o['cohen_d'], 2, True)} [{_f(lo, 2, True)}, {_f(hi, 2, True)}] & "
                f"{_f(p['cohen_d'], 2, True)} [{_f(plo, 2, True)}, {_f(phi, 2, True)}] \\\\")
    tex = "\n".join([
        "% GENERATED by data/results/ch5_defended/memory_ablation.py from memory_ablation_numbers.json;",
        "% never hand-edit. Section 5.4.2; the numbers of fig:ablation-memory.",
        r"\begin{table}[tp]",
        r"  \centering",
        (r"  \caption[The APT attacker model with and without the vulnerability memory]{The APT attacker "
         r"model on $c_1$ to $c_4$ pooled, without the vulnerability memory (off), with it (on) and with "
         r"every exploit succeeding (all), on the same \prelim{%s} seeds, by the number of services per "
         r"operating system. Exploit success is the share of exploits that succeed, those an operating "
         r"system rules out excluded. Cohen's $d$ is on hosts compromised per seed, against the memory off, "
         r"with its 95\,\%% bootstrap interval over seeds.}")
        % (f"{seeds:,}".replace(",", r"\,")),
        r"  \label{tab:ablation-memory}",
        r"  \tablestyle\scriptsize\setlength{\tabcolsep}{4pt}",
        r"  \begin{tabular}{@{}cccccccc@{}}",
        r"    \toprule",
        r"    & \multicolumn{2}{c}{Exploit success} & \multicolumn{3}{c}{Hosts compromised} & "
        r"\multicolumn{2}{c}{Cohen's $d$} \\",
        r"    \cmidrule(lr){2-3}\cmidrule(lr){4-6}\cmidrule(lr){7-8}",
        r"    Services per OS & off & on & off & on & all & on & all \\",
        r"    \midrule",
        *[b for b in body if b],
        r"    \bottomrule",
        r"  \end{tabular}",
        r"\end{table}",
        "",
    ])
    TABLE.write_text(tex, encoding="utf-8")


if __name__ == "__main__":
    main()
    write_table(json.loads(OUT.read_text()))
