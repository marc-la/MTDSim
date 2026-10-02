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


def _reached(r) -> bool:
    return bool(r["reached_objective"] and r["first_database_reach_time"] is not None)


def describe(c, units, rng, srng):
    rows = [c[k] for k in units]
    hosts = np.array([r["compromised"] for r in rows], float)
    _, ms = _per_seed(units, hosts / HOSTS)
    sidx = srng.integers(0, len(ms), size=(N_BOOT, len(ms)))
    # ASP as section 4.5 and analyse.py define it: a target host compromised, read
    # from the attacker's own record (database_hosts_reached is read at the horizon
    # and misses targets a later deployment undid; fixed 2026-10-01)
    asp = np.array([_reached(r) for r in rows], float)
    rolls = sum(r["rolls"] for r in rows)
    idx = rng.integers(0, len(units), size=(N_BOOT, len(units)))
    return {"hosts": float(hosts.mean()), "hosts_ci95": _ci(hosts[idx].mean(1)),
            "ncr": float(hosts.mean() / HOSTS), "asp": float(asp.mean()),
            "ncr_ci95_seeds": _ci(ms[sidx].mean(1)),
            "roll_success": sum(r["wins"] for r in rows) / rolls if rolls else None,
            "roll_success_ci95": _ci(np.array([r["wins"] for r in rows], float)[idx].sum(1)
                                     / np.array([r["rolls"] for r in rows], float)[idx].sum(1)),
            "refused_share": sum(r["refused"] for r in rows) / max(1, rolls + sum(r["refused"] for r in rows)),
            "types_rewon": float(np.mean([r["types_rewon"] for r in rows])),
            "vuln_types": float(np.mean([r["vuln_types"] for r in rows])),
            "_hosts": hosts, "_asp": asp}


def main() -> None:
    cells, errors = load()
    rng = np.random.default_rng(SEED)
    srng = np.random.default_rng(SEED + 1)  # the 2026-10-01 additions; rng's draws stay as they were
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
            desc = {m: describe(arms[m], units, rng, srng) for m in arms}
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
                    a0 = np.array([_reached(base[m][k]) for k in units], float)
                    red[m] = {"ncr_reduction": float(1 - h.mean() / h0.mean()),
                              "ncr_reduction_ci95": _ci(1 - h[idx].mean(1) / h0[idx].mean(1)),
                              "asp_reduction": float(1 - a.mean() / a0.mean()) if a0.mean() > 0 else None}
                row["reduction"] = red
                # Cohen's d on NCR reduction per seed (1 - NCR under the mechanism
                # over NCR with no MTD, the four profiles at one seed averaged),
                # on against off. Computed 2026-10-01 as a candidate column for
                # Table 5.6 and REJECTED: a per-seed ratio is noisy (intervals about
                # +-0.15 against +-0.07 for d on NCR) and its mean is not the NCR
                # reduction the table prints (a ratio of cell means), so the section
                # preamble's d would not describe it. In the JSON only.
                per = {}
                for m in ("on", "off"):
                    _, hm = _per_seed(units, desc[m]["_hosts"])
                    _, h0 = _per_seed(units, np.array([base[m][k]["compromised"] for k in units], float))
                    per[m] = 1 - hm / h0
                sidx = srng.integers(0, len(per["on"]), size=(N_BOOT, len(per["on"])))
                row["reduction_on_minus_off"] = {
                    "cohen_d": _d(per["on"], per["off"]),
                    "cohen_d_ci95": _ci([_d(per["on"][i], per["off"][i]) for i in sidx])}
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


TABLE = HERE.parents[2] / "docs" / "thesis" / "tables" / "tab_F-2_ablation_memory.tex"
COND_LABEL = {"none": "no MTD", "service_diversity": "service diversity, 200\\,s",
              "os_diversity": "OS diversity, 200\\,s"}


def _f(x: float, nd: int, sign: bool = False) -> str:
    """Half-up rounding, as the prose rounds (binary floats round 7.755 down)."""
    from decimal import ROUND_HALF_UP, Decimal
    q = Decimal(repr(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    if sign and q == 0:
        return f"{0:.{nd}f}"
    s = f"{q:+.{nd}f}" if sign else f"{q:.{nd}f}"
    return s.replace("-", "$-$").replace("+", "$+$") if sign else s


def write_table(out: dict) -> None:
    """Appendix F's table (moved from section 5.4.2 on Marc's 2026-10-01 ruling):
    the pool sweep behind fig:ablation-memory, in Table 5.6's form (with, then
    without; Cohen's d on NCR, with against without). Per MTD setting and pool:
    the share of exploits that succeed (the manipulation check) and NCR, with
    and without the memory. Every exploit succeeding stays in the JSON only
    (Marc 2026-09-30: compare with and without)."""
    seeds = max(r["seeds"] for r in out["reads"].values())
    if seeds != 1_000:  # the thesis declares 1 000 (seed-count protocol); the numbers are \prelim until then
        print(f"NOTE: table numbers are from {seeds} seeds; the caption declares 1 000")
    body = []
    for cond in out["conditions"]:
        body.append(r"    \addlinespace" if body else "")
        body.append(rf"    \grouprow{{6}}{{{COND_LABEL[cond]}}} \\")
        for pool in out["pools"]:
            r = out["reads"][f"{pool}|{cond}"]
            a, o = r["arms"], r["on_minus_off"]
            lo, hi = o["cohen_d_ci95"]
            body.append(
                f"    {pool} & {_f(a['on']['roll_success'], 2)} & {_f(a['off']['roll_success'], 2)} & "
                f"{_f(a['on']['ncr'], 3)} & {_f(a['off']['ncr'], 3)} & "
                f"{_f(o['cohen_d'], 2, True)} [{_f(lo, 2, True)}, {_f(hi, 2, True)}] \\\\")
    tex = "\n".join([
        "% GENERATED by data/results/ch5_defended/memory_ablation.py from memory_ablation_numbers.json;",
        "% never hand-edit. Appendix F; the pool sweep behind fig:ablation-memory, in tab:ablation's form.",
        r"\begin{table}[tp]",
        r"  \centering",
        (r"  \caption[The APT attacker model with and without the vulnerability memory, by pool]{The APT "
         r"attacker model with and without the vulnerability memory, averaged over $c_1$ to $c_4$, on the "
         r"same 1\,000 seeds, by the number of services per operating system: the share of exploits that "
         r"succeed, NCR, and Cohen's $d$ on NCR, with minus without, with its 95\,\% bootstrap interval over seeds. An exploit "
         r"the host's operating system rules out is not counted.}"),
        r"  \label{tab:ablation-memory}",
        r"  \tablestyle",  # group rows keep the stripes (Marc, 2026-10-01)
        r"  \begin{tabular}{@{}cccccc@{}}",
        r"    \toprule",
        r"    & \multicolumn{2}{c}{Exploits that succeed} & \multicolumn{3}{c}{NCR} \\",
        r"    \cmidrule(lr){2-3}\cmidrule(lr){4-6}",
        r"    \rowcolor{white}Services per OS & with & without & with & without & Cohen's $d$ \\",
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
