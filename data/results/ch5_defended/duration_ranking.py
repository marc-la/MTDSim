#!/usr/bin/env python3
"""Reads run_duration_ranking.py's corpus (registry B19): the 200 s ranking with
the 45 s mean duration at both ends of its band, against the baseline
attacker's reported ranking.

The ranking is computed exactly as analyse.section_ranking computes Section
5.3's (Scott-Knott ESD on the mean hosts compromised per seed, the four attack
profiles averaged within a seed; Spearman's rho between the two attackers' NCR
reductions with a seed-resampled 95 % interval), at three points: the declared
45 s (from the reported corpus's summaries, the check that this reader
reproduces Table 5.3) and x0.25 and x4 (from runs_duration_ranking.jsonl).

The criterion is the one fixed in run_duration_ranking.py's docstring before
the run: the headline HOLDS at a band end if (a) the APT attacker model's rank
1 shares no member with the baseline attacker's rank 1, and (b) the host layer
ranks above the service layer for the APT attacker model (every host-layer
mechanism's rank number below every service-layer mechanism's).

    python data/results/ch5_defended/duration_ranking.py   (writes duration_ranking_numbers.json)
"""
from __future__ import annotations

import json
import pickle
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from sk_esd import sk_esd  # noqa: E402

RUNS = HERE / "runs_duration_ranking.jsonl"
SUMMARIES = HERE / "runs_reported_summaries.pkl"
OUT = HERE / "duration_ranking_numbers.json"
FOUR = ("objective_exfiltration", "objective_impact", "objective_exfiltration_impact", "objective_none_c2")
RANKED = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle", "user_shuffle",
          "os_diversity", "service_diversity", "random", "alternative", "mtdshield")
HOST = ("ip_shuffle", "complete_topology", "host_topology")
SERVICE = ("port_shuffle", "os_diversity", "service_diversity")
INTERVAL = 200
N_BOOT = 2000


def per_seed(rows) -> np.ndarray:
    by = defaultdict(list)
    for seed, hosts in rows:
        by[seed].append(float(hosts))
    return np.array([np.mean(by[k]) for k in sorted(by)], dtype=float)


def reduction(none, cond, idx=None) -> float:
    n = none if idx is None else none[idx]
    c = cond if idx is None else cond[idx]
    return float(1.0 - c.mean() / n.mean())


def reported():
    cells, _ = pickle.load(SUMMARIES.open("rb"))

    def get(arm, profile, cond, iv):
        return cells[("core", arm, profile, "targeted", cond, iv, "shifted", "v4_failure_only")]

    base = {c: per_seed((r["seed"], r["hosts"]) for r in get("baseline", "baseline", c, INTERVAL)) for c in RANKED}
    base["none"] = per_seed((r["seed"], r["hosts"]) for r in get("baseline", "baseline", "none", 0))
    apt = {c: per_seed((r["seed"], r["hosts"]) for p in FOUR for r in get("movement", p, c, INTERVAL)) for c in RANKED}
    apt["none"] = per_seed((r["seed"], r["hosts"]) for p in FOUR for r in get("movement", p, "none", 0))
    return base, apt


def band_ends():
    rows = defaultdict(list)
    errors = 0
    with RUNS.open() as fh:
        for line in fh:
            r = json.loads(line)
            if "error" in r:
                errors += 1
                continue
            rows[(r["factor"], r["condition"])].append((r["seed"], r["compromised"]))
    out = {}
    for f in sorted({k[0] for k in rows}):
        out[f] = {c: per_seed(rows[(f, c)]) for c in ("none",) + RANKED}
        n = {c: len(rows[(f, c)]) for c in ("none",) + RANKED}
        out[f]["_n"] = n
    return out, errors


def block(apt, base, rng) -> dict:
    sk = sk_esd({c: apt[c] for c in RANKED}, best="low")
    rank = sk["rank"]
    red = {c: reduction(apt["none"], apt[c]) for c in RANKED}
    pts_a = [red[c] for c in RANKED]
    pts_b = [reduction(base["none"], base[c]) for c in RANKED]
    rho = float(spearmanr(pts_a, pts_b).statistic)
    n = len(apt["none"])
    assert n == len(base["none"]), (n, len(base["none"]))
    boots = []
    for _ in range(N_BOOT):
        idx = rng.integers(0, n, n)
        r_ = spearmanr([reduction(apt["none"], apt[c], idx) for c in RANKED],
                       [reduction(base["none"], base[c], idx) for c in RANKED]).statistic
        if np.isfinite(r_):
            boots.append(r_)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    rank1 = sorted(c for c in RANKED if rank[c] == 1)
    return {"ncr_none": float(apt["none"].mean() / 50), "ncr_reduction": red, "rank": rank,
            "rank1": rank1, "rho": {"point": rho, "lo": float(lo), "hi": float(hi)},
            "host_above_service": max(rank[c] for c in HOST) < min(rank[c] for c in SERVICE)}


def main() -> int:
    rng = np.random.default_rng(20261009)
    base, apt_declared = reported()
    sk_b = sk_esd({c: base[c] for c in RANKED}, best="low")
    base_rank1 = sorted(c for c in RANKED if sk_b["rank"][c] == 1)
    ends, errors = band_ends()
    out = {"baseline": {"rank": sk_b["rank"], "rank1": base_rank1,
                        "ncr_reduction": {c: reduction(base["none"], base[c]) for c in RANKED}},
           "errors": errors, "points": {}}
    points = {"1.0 (declared, reported corpus)": apt_declared}
    points.update({f"{f:g}": v for f, v in ends.items()})
    for name, apt in points.items():
        n = apt.pop("_n", None)
        complete = n is None or all(v == 4 * len(base["none"]) for v in n.values())
        if not complete:
            print(f"  {name}: incomplete {n}; skipped")
            continue
        b = block(apt, base, rng)
        b["holds"] = {"rank1_disjoint": not set(b["rank1"]) & set(base_rank1),
                      "host_above_service": b["host_above_service"]}
        out["points"][name] = b
        print(f"{name}: NCR none {b['ncr_none']:.3f}; rank 1 {b['rank1']}; "
              f"rho {b['rho']['point']:+.2f} [{b['rho']['lo']:+.2f}, {b['rho']['hi']:+.2f}]; holds {b['holds']}")
        print("   ranks", {c: b["rank"][c] for c in RANKED})
    print("baseline rank 1", base_rank1)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
