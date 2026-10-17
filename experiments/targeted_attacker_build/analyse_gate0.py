"""Summarise gate0_rows.csv per arm x target: reach rate with a seed-level
bootstrap 95 % CI (BCa via scipy when available, percentile otherwise),
median time-to-target among reached runs, mean footprint at reach, mean hosts
total. Prints a markdown table; no thresholds are decided here (§2 of the
findings record fixed them)."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

import numpy as np

ROWS = Path(__file__).parent / "gate0_rows.csv"


def ci(values, n_boot=2000, seed=0):
    x = np.asarray(values, dtype=float)
    if len(x) == 0:
        return (float("nan"), float("nan"))
    try:
        from scipy.stats import bootstrap
        res = bootstrap((x,), np.mean, n_resamples=n_boot, method="BCa",
                        random_state=seed, confidence_level=0.95)
        return float(res.confidence_interval.low), float(res.confidence_interval.high)
    except Exception:
        rng = np.random.default_rng(seed)
        m = [rng.choice(x, len(x)).mean() for _ in range(n_boot)]
        return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def main() -> int:
    cells = defaultdict(list)
    with open(ROWS) as f:
        for r in csv.DictReader(f):
            cells[(r["target"], r["arm"], r["profile"])].append(r)
    order_t = ["L1", "L2", "L3", "db"]
    print("| target | arm / profile | reach | 95 % CI | n reached | footprint at reach | median TTT (s) | mean hosts |")
    print("|---|---|--:|--|--:|--:|--:|--:|")
    for t in order_t:
        keys = sorted((k for k in cells if k[0] == t), key=lambda k: (k[1] != "baseline", k[2]))
        for k in keys:
            rows = cells[k]
            reached = [r["reached_target"] == "True" for r in rows]
            rate = mean(reached)
            lo, hi = ci([1.0 if v else 0.0 for v in reached])
            fp = [float(r["footprint_at_reach"]) for r in rows if r["footprint_at_reach"] not in ("", "None")]
            ttt = [float(r["time_to_target"]) for r in rows if r["time_to_target"] not in ("", "None")]
            hosts = [float(r["hosts_total"]) for r in rows]
            fp_lo, fp_hi = ci(fp) if len(fp) >= 2 else (float("nan"), float("nan"))
            name = k[1] if k[1] == "baseline" else k[2]
            print(f"| {t} | {name} | {rate:.3f} | [{lo:.3f}, {hi:.3f}] | {sum(reached)} / {len(rows)} | "
                  f"{(mean(fp) if fp else float('nan')):.1f} [{fp_lo:.1f}, {fp_hi:.1f}] | "
                  f"{(median(ttt) if ttt else float('nan')):.0f} | {mean(hosts):.1f} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
