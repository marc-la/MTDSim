#!/usr/bin/env python3
"""The size-matched, label-blind partition control — the read half (a stub:
numbers only, no figure or table yet).

Question. The attack graph before partitioning (``aggregate``) differs from the
four attack profiles averaged (partition_ablation.py). Is that conditioning on
objective, or corpus size? Each random partition (run_partition_control.py)
splits the same 38 flows into four groups of the profiles' sizes, compiled and
run exactly as the profiles are. Random partitions that sit with the profiles
point at size; random partitions that sit with the aggregate point at objective.

Per cell (no MTD; IP shuffle and OS diversity at 200 s and 2 000 s), for each
random partition and for the real profiles: the equal-weight per-seed network
compromise ratio (NCR, hosts / 50; the four groups' runs on a seed averaged, as
every pooled value of chapter 5 is), its mean over seeds, and Cohen's d against
the aggregate on the same seeds — partition_ablation.py's definition (with minus
without, pooled SD of the two arms' per-seed values; ``_d`` is imported from it).

Inputs: runs_partition_control.jsonl (RUNS=path to override) and the reported
corpus's runs_reported_summaries.pkl (PKL=path), seeds 0..n-1 where n is the
number of seeds every partition and cell has completed.

Usage: PYTHONPATH=src python data/results/ch5_defended/partition_control.py
Output: partition_control_numbers.json beside it.
"""
from __future__ import annotations

import json
import os
import pickle
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from partition_ablation import AGG, FOUR, N_HOSTS, _d  # noqa: E402

RUNS = Path(os.environ.get("RUNS", HERE / "runs_partition_control.jsonl"))
CACHE = Path(os.environ.get("PKL", HERE / "runs_reported_summaries.pkl"))
OUT = HERE / "partition_control_numbers.json"
CELLS = (("none", 0), ("ip_shuffle", 200), ("ip_shuffle", 2_000),
         ("os_diversity", 200), ("os_diversity", 2_000))
# the reported corpus's core configuration, which the control's jobs repeat
CORE = {"group": "core", "objective": "targeted", "regime": "shifted", "overlay": "v4_failure_only"}

_ROW = re.compile(rb'"profile": "(\w+)", "objective": "\w+", "condition": "(\w+)", '
                  rb'"interval": (\d+), .*?"seed": (\d+), "partition": (\d+), .*?"compromised": (\d+)')


def load_control() -> tuple[dict, int]:
    """(partition, slot, condition, interval) -> {seed: hosts}; and the error count."""
    runs: dict = defaultdict(dict)
    errors = 0
    with RUNS.open("rb") as fh:
        for line in fh:
            m = _ROW.search(line[:4096])
            if m:
                pr, c, i, s, k, h = m.groups()
                runs[(int(k), pr.decode(), c.decode(), int(i))][int(s)] = int(h)
                continue
            r = json.loads(line)
            if "error" in r:
                errors += 1
                continue
            runs[(r["partition"], r["profile"], r["condition"], r["interval"])][r["seed"]] = r["compromised"]
    return runs, errors


def load_reference() -> dict:
    """(condition, interval) -> {profile: hosts per seed, seeds 0..999 in order}
    for the real four profiles and the aggregate, the core configuration only."""
    with CACHE.open("rb") as fh:
        summaries, _ = pickle.load(fh)
    cells: dict = defaultdict(dict)
    for key, rows in summaries.items():
        group, arm, profile, objective, cond, interval, regime, overlay = key
        if arm != "movement" or (cond, interval) not in CELLS or profile not in FOUR + (AGG,):
            continue
        if (group, objective, regime, overlay) != tuple(CORE.values()):
            continue
        assert [r["seed"] for r in rows] == list(range(len(rows))), key
        assert profile not in cells[(cond, interval)], ("two corpus keys for one cell", key)
        cells[(cond, interval)][profile] = np.array([r["hosts"] for r in rows], float)
    return cells


def complete_seeds(runs: dict, partitions: list[int]) -> int:
    """The largest n with seeds 0..n-1 present for every partition, slot and cell."""
    n = None
    for k in partitions:
        for slot in FOUR:
            for c, i in CELLS:
                seeds = runs.get((k, slot, c, i), {})
                m = 0
                while m in seeds:
                    m += 1
                n = m if n is None else min(n, m)
    return n or 0


def main() -> int:
    runs, errors = load_control()
    ref = load_reference()
    partitions = sorted({key[0] for key in runs})
    n = complete_seeds(runs, partitions)
    if n < 2:
        raise SystemExit(f"{RUNS}: fewer than two complete seeds across every partition and cell")
    out: dict = {"n_seeds": n, "partitions": partitions, "error_rows": errors, "cells": {}}
    for c, i in CELLS:
        agg = ref[(c, i)][AGG][:n] / N_HOSTS
        real = np.mean([ref[(c, i)][p][:n] for p in FOUR], axis=0) / N_HOSTS
        cell = {
            "aggregate": {"ncr": float(agg.mean())},
            "real_profiles": {"ncr": float(real.mean()), "cohen_d_vs_aggregate": _d(real, agg),
                              "per_profile_ncr": {p: float(ref[(c, i)][p][:n].mean() / N_HOSTS)
                                                  for p in FOUR}},
            "random": {},
        }
        for k in partitions:
            hosts = np.array([[runs[(k, slot, c, i)][s] for s in range(n)] for slot in FOUR], float)
            w = hosts.mean(axis=0) / N_HOSTS
            cell["random"][str(k)] = {
                "ncr": float(w.mean()), "cohen_d_vs_aggregate": _d(w, agg),
                "per_group_ncr": {slot: float(hosts[j].mean() / N_HOSTS) for j, slot in enumerate(FOUR)},
            }
        ds = np.array([v["cohen_d_vs_aggregate"] for v in cell["random"].values()])
        cell["random_summary"] = {"d_mean": float(ds.mean()), "d_min": float(ds.min()),
                                  "d_max": float(ds.max()),
                                  "ncr_mean": float(np.mean([v["ncr"] for v in cell["random"].values()]))}
        out["cells"][f"{c}|{i}"] = cell
    OUT.write_text(json.dumps(out, indent=1))
    print(f"n = {n} seeds, {len(partitions)} partitions, {errors} error rows")
    for key, cell in out["cells"].items():
        rs = cell["random_summary"]
        print(f"  {key:18s} NCR agg {cell['aggregate']['ncr']:.3f}  real {cell['real_profiles']['ncr']:.3f} "
              f"(d {cell['real_profiles']['cohen_d_vs_aggregate']:+.2f})  random {rs['ncr_mean']:.3f} "
              f"(d mean {rs['d_mean']:+.2f}, range [{rs['d_min']:+.2f}, {rs['d_max']:+.2f}])")
    return 0


if __name__ == "__main__":
    sys.exit(main())
