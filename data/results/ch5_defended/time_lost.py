#!/usr/bin/env python3
"""§5.3.1 Response to disruption: the two disruption metrics of Section 4.5.3,
on both attackers by one rule. Replaces disruption.py (retired 2026-09-30 with the
compromise rate after an MTD deployment; record:
docs/implementation/disruption_mechanism.md; rulings:
docs/handoffs/2026-09-30_disruption_metrics.md).

ATTACK ACTIONS BLOCKED (Brown 2023), per run: the actions a deployment cuts off
while they run. APT attacker model: a record whose outcome is MTD_INTERRUPT (an
interrupt that lands on a tactic with no action, or on an action whose
precondition was already unmet, cuts off no action). Baseline attacker: a record
with interrupted_in set, its consecutive per-vulnerability EXPLOIT_VULN rows read
as one action.

TIME LOST PER MTD DEPLOYMENT (Marc 2026-09-30): for each deployment that completes
while the attacker is still acting, the time from its completion to the attacker's
next compromised host, and the same from the same moment on the same seed's
no-MTD run. Each is capped at the next deployment (at most one interval), so a
deployment is charged only up to the next; a wait that reaches the cap counts as
the cap. Time lost = the mean of (wait with the MTD - wait with no MTD) over the
deployments. The mean of capped waits is the restricted mean of survival analysis.
A deployment whose no-MTD run had already ended (its target taken) has no
reference and is dropped; the count is kept.

THE BASELINE'S END. Its termination_time is always the horizon, even when its
target fell earlier (mechanism record, section D), so its end is its last
action's end. The APT attacker model's termination_time is its true end.

INTERVAL. Seeded bootstrap over runs (a run brings its deployments and its no-MTD
pair), 2 000 resamples, 95 % percentile interval.

CURVES (Figure 5.3 (a), (b)): the share of deployments followed by a compromise
within t, with the MTD and with no MTD, over the same deployments.

Usage: python data/results/ch5_defended/time_lost.py
Output: time_lost_numbers.json beside the corpus.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs.jsonl"
OUT = HERE / "time_lost_numbers.json"
COMPROMISE = {("BRUTE_FORCE", "TRUE"), ("SCAN_PORT", "TRUE"), ("EXPLOIT_VULN", "EXPLOIT_COMPROMISED")}
MECHANISMS = ("ip_shuffle", "complete_topology", "host_topology",
              "port_shuffle", "os_diversity", "service_diversity", "user_shuffle")
INTERVALS = (2000, 200)
N_BOOT = 2_000
SEED = 20260930
GRID_STEP = 25.0


def view(r: dict) -> dict:
    """What the two metrics read from one run record."""
    if r["arm"] == "movement":
        comp = [x[8] for x in r["records"] if (x[1], x[2]) in COMPROMISE]
        end = float(r["termination_time"])
        blocked = sum(1 for x in r["records"] if x[2] == "MTD_INTERRUPT")
    else:
        comp = [x[2] for x in r["records"] if x[3] is not None]
        end = max((float(x[2]) for x in r["records"]), default=0.0)
        blocked, prev_exploit_blocked, prev = 0, False, None
        for x in r["records"]:
            hit = x[5] is not None
            if x[0] == "EXPLOIT_VULN" and prev == "EXPLOIT_VULN":
                if hit and not prev_exploit_blocked:
                    blocked += 1
                prev_exploit_blocked = prev_exploit_blocked or hit
            else:
                blocked += hit
                prev_exploit_blocked = hit
            prev = x[0]
    return {
        "arm": r["arm"], "profile": r["profile"], "seed": r["seed"], "cond": r["condition"],
        "interval": r["interval"], "end": end, "blocked": blocked,
        "comp": np.sort(np.minimum(np.array(comp, float), end)),
        "landings": sorted(float(e[2]) for e in r["mtd_executions"]),
    }


def _wait(comp: np.ndarray, t: float, cap: float) -> float:
    j = np.searchsorted(comp, t, "right")
    return float(min(comp[j] - t, cap)) if j < len(comp) else cap


def pairs(run: dict, twin: dict, interval: float) -> tuple[list, int]:
    """(wait with the MTD, wait with no MTD, cap) per deployment kept, and the
    number dropped because the no-MTD run had already ended."""
    out, dropped = [], 0
    L = run["landings"]
    for i, t in enumerate(L):
        if t >= run["end"]:
            continue
        if t >= twin["end"]:
            dropped += 1
            continue
        cap = min((L[i + 1] if i + 1 < len(L) else t + interval) - t, interval)
        out.append((_wait(run["comp"], t, cap), _wait(twin["comp"], t, cap), cap))
    return out, dropped


def time_lost(per_run: list[list]) -> float:
    d = [a - b for ps in per_run for a, b, _ in ps]
    return float(np.mean(d)) if d else float("nan")


def boot_time_lost(per_run: list[list], rng: np.random.Generator) -> list[float]:
    s = np.array([sum(a - b for a, b, _ in ps) for ps in per_run])
    n = np.array([len(ps) for ps in per_run])
    idx = rng.integers(0, len(per_run), size=(N_BOOT, len(per_run)))
    b = s[idx].sum(1) / np.maximum(n[idx].sum(1), 1)
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


def curves(per_run: list[list], interval: float) -> dict:
    ps = [p for q in per_run for p in q]
    grid = np.arange(0.0, interval + GRID_STEP / 2, GRID_STEP)
    a = np.array([w for w, _, c in ps if True]); ca = np.array([c for _, _, c in ps])
    b = np.array([w for _, w, _ in ps])
    hit_a, hit_b = a < ca, b < ca
    return {"t": grid.tolist(),
            "with_mtd": [float(np.mean(hit_a & (a <= t))) for t in grid],
            "no_mtd": [float(np.mean(hit_b & (b <= t))) for t in grid]}


def load() -> list[dict]:
    """Targeted, core, shifted runs of the four profiles and the baseline attacker:
    no MTD, and each MTD mechanism alone (the single deployment strategy)."""
    out = []
    with RUNS.open() as f:
        for line in f:
            head = line[:400]
            if '"group": "core"' not in head or '"regime": "shifted"' not in head or '"objective": "targeted"' not in head:
                continue
            r = json.loads(line)
            if r["profile"] == "aggregate":
                continue
            if r["condition"] != "none" and (r["condition"] not in MECHANISMS or r["interval"] not in INTERVALS):
                continue
            if "error" in r:
                raise SystemExit("an error row in the disruption cells; refusing to read")
            out.append(view(r))
    return out


def main() -> None:
    runs = load()
    none = {(r["arm"], r["profile"], r["seed"]): r for r in runs if r["cond"] == "none"}
    rng = np.random.default_rng(SEED)
    out = {"definition": "time lost per MTD deployment = mean over deployments of (time to the next compromise "
                         "with the MTD - the same from the same moment with no MTD), each capped at the next deployment",
           "cells": {}}
    for arm in ("movement", "baseline"):
        nr = [r for r in runs if r["arm"] == arm and r["cond"] == "none"]
        out["cells"][f"{arm}|none"] = {"runs": len(nr), "blocked_per_run": {"mean": 0.0, "ci95": 0.0}}
        for iv in INTERVALS:
            for m in MECHANISMS:
                rs = [r for r in runs if r["arm"] == arm and r["cond"] == m and r["interval"] == iv]
                if not rs:
                    continue
                per_run, dropped = [], 0
                for r in rs:
                    ps, d = pairs(r, none[(arm, r["profile"], r["seed"])], iv)
                    per_run.append(ps)
                    dropped += d
                bl = np.array([r["blocked"] for r in rs], float)
                flat = [p for q in per_run for p in q]
                cell = {
                    "runs": len(rs), "deployments": len(flat), "dropped": dropped,
                    "blocked_per_run": {"mean": float(bl.mean()), "ci95": float(1.96 * bl.std(ddof=1) / np.sqrt(len(bl)))},
                    "wait_with_mtd": float(np.mean([a for a, _, _ in flat])),
                    "wait_no_mtd": float(np.mean([b for _, b, _ in flat])),
                    "time_lost": time_lost(per_run), "time_lost_ci95": boot_time_lost(per_run, rng),
                }
                if iv == 2000:
                    cell["curves"] = curves(per_run, iv)
                out["cells"][f"{arm}|{m}|{iv}"] = cell
    OUT.write_text(json.dumps(out, indent=1))
    print(f"wrote {OUT.relative_to(HERE.parents[2])}")
    for iv in INTERVALS:
        print(f"\n{iv} s: time lost per MTD deployment (s) [95 %], wait with / no MTD, attack actions blocked per run, dropped")
        for arm in ("movement", "baseline"):
            for m in MECHANISMS:
                c = out["cells"].get(f"{arm}|{m}|{iv}")
                if c:
                    print(f"  {arm:9s} {m:18s} {c['time_lost']:6.0f} [{c['time_lost_ci95'][0]:5.0f}, {c['time_lost_ci95'][1]:5.0f}]"
                          f"  {c['wait_with_mtd']:5.0f} / {c['wait_no_mtd']:5.0f}  blocked {c['blocked_per_run']['mean']:5.2f}"
                          f" ± {c['blocked_per_run']['ci95']:.2f}  dropped {c['dropped']}/{c['deployments'] + c['dropped']}")


if __name__ == "__main__":
    main()
