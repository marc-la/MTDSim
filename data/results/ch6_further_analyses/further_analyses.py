#!/usr/bin/env python3
"""Appendix F, Further analyses: the numbers behind F.1, F.2, F.3 and F.5.

Registry rows B1 (+B2), B9, B10 and B14 (+B8) of the further-analyses registry
at the end of chapter 6 (triaged by Marc 2026-10-09; handoff
2026-10-09_ch7_conclusion_and_appendix_structure sections 8-9). Every analysis
here was chosen after the results were seen, while chapter 6 was written. Each
is a pure read of corpora already on disk: no simulation is run.

F.1 Where each attacker succeeds with no MTD (B1, B2)
    ch5_s531_unopposed/runs_reported.jsonl, the corpus of Table 5.2. Success is
    Table 5.2's rule: the APT attacker model reaches its objective with a target
    host held (reached_objective and database_hosts_reached > 0); the baseline
    attacker compromises a target host in its own record. Per attack profile:
    ASP on the seeds where the baseline attacker succeeds and on the seeds where
    it fails; per pair of attack profiles, the seeds on which both succeed
    against the count independence predicts (n_a n_b / n). B2, from the reported
    corpus's summaries: under service diversity at 200 s, each attack profile's
    successful runs, how many sit on seeds where it also succeeds with no MTD,
    and the MTD interruptions per 1 000 s of successful and of failed runs.
F.2 Runs with no foothold under the host layer (B9)
    The reported corpus's summaries (runs_reported_summaries.pkl, written by
    ch5_defended/analyse.py with CORPUS=reported): the share of runs that
    compromise no host, per attacker, with no MTD and under each host-layer MTD
    mechanism at every deployment interval. The APT attacker model pools its four
    attack profiles (4 000 runs per cell), as chapter 5 does.
F.3 Accounts reused under user shuffle (B10)
    ch5_defended/runs_reported.jsonl, the rows with no MTD and under user
    shuffle. A compromise by a held account is the port scan that compromises a
    host: the APT attacker model's (SCAN_PORT, TRUE) record, one of statistics.py
    COMPROMISE_EVENTS; the baseline attacker's SCAN_PORT record with a host
    compromised (attack_operation.py _do_scan_port: can_auto_compromise_with_users).
    Per attacker and deployment interval: compromises by a held account per run,
    and hosts compromised per run, each with a 95 % percentile bootstrap interval
    over runs.
F.4 One run under MTD, traced (B18)
    One stored run pair from ch5_defended/runs_reported.jsonl, no re-run: c1 on
    the lowest seed on which it reaches a target host with no MTD (the rule,
    fixed before any run was looked at), with no MTD and under IP shuffle at
    200 s. Its records and MTD executions are copied for the figure.
F.5 Attack profiles against random groups of the same size (B14, B8)
    partition_control_numbers.json (NCR per group, per random partition, written
    by ch5_defended/partition_control.py) and, for ASP, the partition-control
    streams (runs_partition_control.jsonl; the redrawn partitions from
    runs_partition_control_redraw.jsonl, as partition_control.py reads them).
    With no MTD only. Per slot (the sizes of c1 to c4: 19, 7, 7 and 5 attack
    flows): the attack profile's NCR and ASP, and the median, minimum and
    maximum over the ten random groups of that size.

Usage:   PYTHONPATH=src python data/results/ch6_further_analyses/further_analyses.py [f1 f2 f3 f5]
Output:  further_analyses_numbers.json beside this file (sections not run keep
         their previous values).
"""
from __future__ import annotations

import json
import pickle
import re
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
UNOPPOSED = RESULTS / "ch5_s531_unopposed" / "runs_reported.jsonl"
DEFENDED = RESULTS / "ch5_defended" / "runs_reported.jsonl"
SUMMARIES = RESULTS / "ch5_defended" / "runs_reported_summaries.pkl"
PC_NUMBERS = RESULTS / "ch5_defended" / "partition_control_numbers.json"
PC_RUNS = RESULTS / "ch5_defended" / "runs_partition_control.jsonl"
PC_REDRAW = RESULTS / "ch5_defended" / "runs_partition_control_redraw.jsonl"
PC_MANIFEST = RESULTS.parent / "ogasp" / "partition_control" / "partitions.json"
OUT = HERE / "further_analyses_numbers.json"

FOUR = ("objective_exfiltration", "objective_impact", "objective_exfiltration_impact", "objective_none_c2")
CODE = dict(zip(FOUR, ("c1", "c2", "c3", "c4")))
HOST_LAYER = ("ip_shuffle", "host_topology", "complete_topology")
INTERVALS = (50, 100, 200, 500, 1000, 2000)
CORE = ("core", "targeted", "shifted", "v4_failure_only")  # group, objective, regime, overlay
N_HOSTS = 50
N_BOOT = 2000
SEED = 20261009


def boot_mean(x, rng) -> dict:
    x = np.asarray(x, float)
    idx = rng.integers(0, len(x), size=(N_BOOT, len(x)))
    b = x[idx].mean(axis=1)
    return {"mean": float(x.mean()), "lo": float(np.percentile(b, 2.5)),
            "hi": float(np.percentile(b, 97.5)), "n": int(len(x))}


def boot_share(flags, rng) -> dict:
    return boot_mean(np.asarray(flags, float), rng)


def load_summaries() -> dict:
    with SUMMARIES.open("rb") as fh:
        cells, errors = pickle.load(fh)
    assert not errors, f"{len(errors)} error rows in the reported corpus"
    out = {}
    for key, rows in cells.items():
        group, arm, profile, objective, cond, interval, regime, overlay = key
        if (group, objective, regime, overlay) != CORE:
            continue
        assert [r["seed"] for r in rows] == list(range(len(rows))), key
        out[(profile, cond, interval)] = rows
    return out


# --- F.1 -------------------------------------------------------------------------


def _baseline_success(row: dict) -> bool:
    targets = set(row["target_hosts"])
    return bool(row["reached_objective"]) and any(
        r[3] is not None and r[3] in targets for r in row["records"])


def _movement_success(row: dict) -> bool:
    return bool(row["reached_objective"]) and row["database_hosts_reached"] > 0


def _rate(rows: list[dict], horizon: float = 15_000.0) -> float | None:
    """MTD interruptions per 1 000 s, pooled over runs: a run lasts until its
    target host falls (target_time) or the time limit."""
    if not rows:
        return None
    t = sum((r["target_time"] if r["target_time"] is not None else horizon) for r in rows)
    return 1000.0 * sum(r["n_interrupted"] for r in rows) / t


def f1(rng) -> dict:
    succ: dict[str, dict[int, bool]] = defaultdict(dict)
    with UNOPPOSED.open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            assert "error" not in row, row
            if row["arm"] == "baseline":
                succ["baseline"][row["seed"]] = _baseline_success(row)
            elif row["profile"] in FOUR:
                succ[row["profile"]][row["seed"]] = _movement_success(row)
    seeds = sorted(succ["baseline"])
    n = len(seeds)
    for k in FOUR:
        assert sorted(succ[k]) == seeds, k
    base = np.array([succ["baseline"][s] for s in seeds])
    vec = {k: np.array([succ[k][s] for s in seeds]) for k in FOUR}
    out = {"n_seeds": n, "baseline_asp": float(base.mean()), "baseline_successes": int(base.sum()),
           "profiles": {}, "pairs": {}}
    for k in FOUR:
        v = vec[k]
        out["profiles"][CODE[k]] = {
            "asp": float(v.mean()), "successes": int(v.sum()),
            "successes_where_baseline_succeeds": int(v[base].sum()),
            "asp_where_baseline_succeeds": float(v[base].mean()),
            "successes_where_baseline_fails": int(v[~base].sum()),
            "asp_where_baseline_fails": float(v[~base].mean()),
        }
    for a, b in combinations(FOUR, 2):
        both = int((vec[a] & vec[b]).sum())
        expected = vec[a].sum() * vec[b].sum() / n
        out["pairs"][f"{CODE[a]}-{CODE[b]}"] = {"both": both, "expected": float(expected),
                                                 "ratio": float(both / expected) if expected else None}
    # B2: service diversity at 200 s, from the reported corpus
    summ = load_summaries()
    b2 = {}
    for k in FOUR:
        none = {r["seed"]: r["reached_target"] for r in summ[(k, "none", 0)]}
        rows = summ[(k, "service_diversity", 200)]
        ok = [r for r in rows if r["reached_target"]]
        bad = [r for r in rows if not r["reached_target"]]
        b2[CODE[k]] = {
            "successes": len(ok),
            "on_seeds_succeeding_with_no_mtd": sum(1 for r in ok if none[r["seed"]]),
            # per 1 000 s of the run, not per run: a successful run ends at the
            # target, a failed one runs to the 15 000 s time limit
            "interrupted_per_ksec_successful": _rate(ok),
            "interrupted_per_ksec_failed": _rate(bad),
        }
    out["service_diversity_200"] = b2
    return out


# --- F.2 -------------------------------------------------------------------------


def f2(rng) -> dict:
    summ = load_summaries()
    out: dict = {"conditions": {}}
    for cond in ("none",) + HOST_LAYER:
        ivs = (0,) if cond == "none" else INTERVALS
        for iv in ivs:
            cell = {}
            base = [r["hosts"] == 0 for r in summ[("baseline", cond, iv)]]
            cell["baseline"] = boot_share(base, rng)
            per = {CODE[k]: float(np.mean([r["hosts"] == 0 for r in summ[(k, cond, iv)]])) for k in FOUR}
            pooled = [r["hosts"] == 0 for k in FOUR for r in summ[(k, cond, iv)]]
            cell["apt"] = boot_share(pooled, rng)
            cell["apt_per_profile"] = per
            out["conditions"][f"{cond}|{iv}"] = cell
    return out


# --- F.3 -------------------------------------------------------------------------

_HEAD = re.compile(rb'"group": "(\w+)", "arm": "(\w+)", "profile": "(\w+)", "objective": "(\w+)", '
                   rb'"condition": "(\w+)", "interval": (\d+), "regime": "(\w+)", "overlay": "(\w+)"')


def _reuse(row: dict) -> int:
    if row["arm"] == "baseline":
        return sum(1 for r in row["records"] if r[0] == "SCAN_PORT" and r[3] is not None)
    return sum(1 for r in row["records"] if r[1] == "SCAN_PORT" and r[2] == "TRUE")


def f3(rng) -> dict:
    reuse: dict = defaultdict(list)
    hosts: dict = defaultdict(list)
    errors = 0
    with DEFENDED.open("rb") as fh:
        for line in fh:
            m = _HEAD.match(line, 1)
            if m is None:
                row = json.loads(line)
                errors += "error" in row
                continue
            group, arm, profile, objective, cond, iv, regime, overlay = (x.decode() for x in m.groups())
            if (group, objective, regime, overlay) != CORE or cond not in ("none", "user_shuffle"):
                continue
            if arm == "movement" and profile not in FOUR:
                continue
            row = json.loads(line)
            if "error" in row:
                errors += 1
                continue
            who = "baseline" if arm == "baseline" else "apt"
            key = (who, cond, int(iv))
            reuse[key].append(_reuse(row))
            hosts[key].append(row["compromised_uuid"] if arm == "baseline" else row["compromised"])
    out: dict = {"error_rows": errors, "cells": {}}
    for (who, cond, iv), xs in sorted(reuse.items()):
        out["cells"][f"{who}|{cond}|{iv}"] = {
            "reuse_per_run": boot_mean(xs, rng),
            "hosts_per_run": boot_mean(hosts[(who, cond, iv)], rng),
        }
    return out


# --- F.5 -------------------------------------------------------------------------

_PC = re.compile(rb'"profile": "(\w+)", "objective": "\w+", "condition": "(\w+)", '
                 rb'"interval": (\d+), .*?"seed": (\d+), "partition": (\d+), .*?"compromised": (\d+), '
                 rb'"reached_objective": (true|false), "database_hosts_reached": (\d+)')


def _pc_load(path: Path, skip: set, keep: set | None) -> dict:
    succ: dict = defaultdict(dict)
    with path.open("rb") as fh:
        for line in fh:
            m = _PC.search(line[:4096])
            if m is None:
                r = json.loads(line)
                assert "error" in r, "unparsed partition-control row"
                continue
            pr, c, i, s, k, h, reached, dbh = m.groups()
            k = int(k)
            if c != b"none" or k in skip or (keep is not None and k not in keep):
                continue
            succ[(k, pr.decode())][int(s)] = (reached == b"true") and int(dbh) > 0
    return succ


def f5(rng) -> dict:
    pcn = json.loads(PC_NUMBERS.read_text())
    n = pcn["n_seeds"]
    cell = pcn["cells"]["none|0"]
    manifest = json.loads(PC_MANIFEST.read_text())
    gone = {r["partition"] for r in manifest.get("redraw_2026_10_07", {}).get("replaced", [])}
    succ = _pc_load(PC_RUNS, skip=gone, keep=None)
    if gone:
        succ.update(_pc_load(PC_REDRAW, skip=set(), keep=gone))
    summ = load_summaries()
    real_asp = {k: float(np.mean([r["reached_target"] for r in summ[(k, "none", 0)][:n]])) for k in FOUR}
    sizes = manifest.get("slot_sizes")
    out: dict = {"n_seeds": n, "partitions": pcn["partitions"], "slot_sizes": sizes,
                 "aggregate_ncr": cell["aggregate"]["ncr"], "slots": {}}
    for k in FOUR:
        ncr_r = [cell["random"][str(p)]["per_group_ncr"][k] for p in pcn["partitions"]]
        asp_r = []
        for p in pcn["partitions"]:
            seeds = succ[(p, k)]
            assert all(s in seeds for s in range(n)), (p, k)
            asp_r.append(float(np.mean([seeds[s] for s in range(n)])))
        out["slots"][CODE[k]] = {
            "profile_ncr": cell["real_profiles"]["per_profile_ncr"][k],
            "profile_asp": real_asp[k],
            "random_ncr": {"median": float(np.median(ncr_r)), "min": float(min(ncr_r)), "max": float(max(ncr_r)),
                           "values": ncr_r},
            "random_asp": {"median": float(np.median(asp_r)), "min": float(min(asp_r)), "max": float(max(asp_r)),
                           "values": asp_r},
            "random_groups_below_profile_ncr": int(sum(v < cell["real_profiles"]["per_profile_ncr"][k] for v in ncr_r)),
        }
    return out


# --- F.4 -------------------------------------------------------------------------

F4_PROFILE = "objective_exfiltration"  # c1, the attack profile with the most attack flows
F4_CONDITIONS = (("none", 0), ("ip_shuffle", 200))


def f4_seed() -> int:
    """The rule, fixed before any run was looked at: the lowest seed on which c1
    reaches a target host with no MTD."""
    summ = load_summaries()
    return next(r["seed"] for r in summ[(F4_PROFILE, "none", 0)] if r["reached_target"])


def f4(rng) -> dict:
    seed = f4_seed()
    want = {(c, i) for c, i in F4_CONDITIONS}
    runs = {}
    with DEFENDED.open("rb") as fh:
        for line in fh:
            m = _HEAD.match(line, 1)
            if m is None:
                continue
            group, arm, profile, objective, cond, iv, regime, overlay = (x.decode() for x in m.groups())
            if (group, objective, regime, overlay) != CORE or profile != F4_PROFILE or (cond, int(iv)) not in want:
                continue
            if f'"seed": {seed},'.encode() not in line[:2048]:
                continue
            row = json.loads(line)
            if row["seed"] != seed:
                continue
            runs[f"{cond}|{iv}"] = {
                "compromised": row["compromised"], "reached_objective": row["reached_objective"],
                "first_database_reach_time": row["first_database_reach_time"],
                "termination_time": row["termination_time"],
                # [place, verb, outcome, verdict, blocked, interrupted, dwell, start, end, place_class]
                "records": row["records"],
                # [name, start, finish, duration, layer]
                "mtd_executions": row["mtd_executions"],
            }
            if len(runs) == len(want):
                break
    assert len(runs) == len(want), runs.keys()
    return {"profile": "c1", "seed": seed, "runs": runs}


def main(argv: list[str]) -> int:
    which = argv or ["f1", "f2", "f3", "f4", "f5"]
    rng = np.random.default_rng(SEED)
    fns = {"f1": f1, "f2": f2, "f3": f3, "f4": f4, "f5": f5}
    for w in which:
        result = fns[w](rng)
        # re-read just before writing, so sections run in parallel processes
        # keep each other's results
        out = json.loads(OUT.read_text()) if OUT.exists() else {}
        out[w] = result
        tmp = OUT.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(out, indent=1))
        tmp.replace(OUT)
        print(f"{w} done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
