#!/usr/bin/env python3
"""§5.4 Ablation of the failure matrix: the APT attacker model against the same
model with every factor of the failure matrix set to one (run_corpus.py group
``blind``), on the metrics chapter 4 already defines (Marc 2026-09-26: "use what
metrics exist to show that there's no difference"; plan in
docs/handoffs/2026-09-25_ch4_mark_risk_ledger.md, "PLAN for Marc's approval").

SCOPE. The ablation arm was run on the four profiles, targeted, under no defence
and the two spanning mechanisms (IP shuffle, OS diversity) at 200 s and 2 000 s,
on the corpus's seeds. Nothing else is claimed.

MEASURES, each read the way the chapter 5 floats read it:
  hosts        mean hosts compromised per run (NCR x N), per condition
  NCR reduction 1 - mean(hosts | defence) / mean(hosts | none), the same arm's
               own no-defence runs as the reference (section 4.5)
  time lost    per MTD deployment, disruption.py's estimator unchanged (anchor,
               window, placebo on the same seed's no-defence run); 2 000 s only,
               where the window holds one deployment

DIFFERENCE (with minus without). Every seed and profile runs in both arms, so the
bootstrap resamples (profile, seed) units jointly for both arms: 2 000 resamples,
95 % percentile intervals. EFFECT SIZE. Cohen's d on hosts per seed (the four
profiles at one seed averaged, as section_ranking does, the seed being the
independent unit), paired: mean difference over the SD of the differences
(d_z), and Cohen's d with the pooled SD of the two arms' per-seed means, the
form section 4.5.4's Scott-Knott ESD merge uses. Negligible below 0.2 on d, the
threshold section 4.5.4 already uses; d_z is kept in the JSON for the record.

Usage: python data/results/ch5_defended/ablation.py
Output: ablation_numbers.json beside the corpus.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

import disruption as D

HERE = Path(__file__).resolve().parent
OUT = HERE / "ablation_numbers.json"
FOUR = ("objective_exfiltration", "objective_impact", "objective_exfiltration_impact", "objective_none_c2")
SPANNING = ("ip_shuffle", "os_diversity")
CONDS = ("none",) + SPANNING
INTERVALS = (200, 2_000)
ARMS = {"core": "with the failure matrix", "blind": "every factor set to one"}
N_BOOT = 2_000
SEED = 20260926


def load() -> list[dict]:
    out = []
    with D.RUNS.open() as f:
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
            T = r["termination_time"]
            comp = [x[8] for x in r["records"] if (x[1], x[2]) in D.COMPROMISE]
            out.append({
                "group": r["group"], "arm": "movement", "profile": r["profile"], "seed": r["seed"],
                "cond": r["condition"], "interval": r["interval"], "T": T, "hosts": r["compromised"],
                "comp": np.sort(np.minimum(np.array(comp, float), T)),
                "landings": [e[2] for e in r["mtd_executions"] if -D.EDGES[0] <= e[2] < T],
                "durations": [e[3] for e in r["mtd_executions"]],
            })
    return out


def cell(runs, group, cond, interval):
    rs = [r for r in runs if r["group"] == group and r["cond"] == cond and (cond == "none" or r["interval"] == interval)]
    return {(r["profile"], r["seed"]): r for r in rs}


def main() -> None:
    runs = load()
    rng = np.random.default_rng(SEED)
    out = {"scope": "four profiles pooled, targeted; IP shuffle and OS diversity; the corpus's seeds",
           "arms": ARMS, "reads": {}}
    none = {g: cell(runs, g, "none", 0) for g in ARMS}
    units = sorted(set(none["core"]) & set(none["blind"]))
    out["units_none"] = len(units)

    # no defence: does the failure matrix change hosts compromised with no defence running?
    rows = {}
    for label, cond, iv in [("none", "none", 0)] + [(f"{c}|{i}", c, i) for c in SPANNING for i in INTERVALS]:
        w, wo = cell(runs, "core", cond, iv), cell(runs, "blind", cond, iv)
        u = sorted(set(w) & set(wo) & set(none["core"]) & set(none["blind"]))
        hw = np.array([w[k]["hosts"] for k in u], float)
        hb = np.array([wo[k]["hosts"] for k in u], float)
        n0w = np.array([none["core"][k]["hosts"] for k in u], float)
        n0b = np.array([none["blind"][k]["hosts"] for k in u], float)
        # per-seed means (four profiles averaged) for the paired effect size
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
        idx = rng.integers(0, len(u), size=(N_BOOT, len(u)))
        dh = hw[idx].mean(1) - hb[idx].mean(1)
        row = {"units": len(u), "seeds": len(seeds),
               "hosts_with": float(hw.mean()), "hosts_without": float(hb.mean()),
               "hosts_diff": float(hw.mean() - hb.mean()),
               "hosts_diff_ci95": [float(np.percentile(dh, 2.5)), float(np.percentile(dh, 97.5))],
               "cohen_d_per_seed": d_pooled, "cohen_d_z_per_seed": d_z}
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
    print(f"wrote {OUT.relative_to(HERE.parents[2])}")
    for label, r in rows.items():
        print(f"\n{label}: units {r['units']}  hosts {r['hosts_with']:.2f} vs {r['hosts_without']:.2f}  "
              f"diff {r['hosts_diff']:+.2f} [{r['hosts_diff_ci95'][0]:+.2f}, {r['hosts_diff_ci95'][1]:+.2f}]  d {r['cohen_d_per_seed']:+.2f} (d_z {r['cohen_d_z_per_seed']:+.2f})")
        if "ncr_reduction_with" in r:
            print(f"   NCR reduction {r['ncr_reduction_with']:.3f} vs {r['ncr_reduction_without']:.3f}  diff {r['ncr_reduction_diff']:+.3f} "
                  f"[{r['ncr_reduction_diff_ci95'][0]:+.3f}, {r['ncr_reduction_diff_ci95'][1]:+.3f}]")
        if "time_lost_with" in r:
            print(f"   time lost {r['time_lost_with']:.0f} s vs {r['time_lost_without']:.0f} s  diff {r['time_lost_diff']:+.0f} "
                  f"[{r['time_lost_diff_ci95'][0]:+.0f}, {r['time_lost_diff_ci95'][1]:+.0f}]")


if __name__ == "__main__":
    main()
