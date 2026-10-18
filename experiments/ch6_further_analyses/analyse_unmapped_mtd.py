#!/usr/bin/env python3
"""Reads run_unmapped_mtd.py's corpus: the tactic-duration ablation under MTD
(Jin's item 13). The criterion is the one fixed in run_unmapped_mtd.py's
docstring before the run.

Both measures are computed exactly as the reported cells compute them:
  NCR reduction       duration_ranking.py: mean hosts compromised per seed, the
                      four attack profiles averaged within a seed,
                      1 - mean(with MTD) / mean(no MTD); 95 % interval by
                      resampling seeds (2 000).
  attack actions      time_lost.py's view() and pooled ratio: attack actions
  blocked per MTD     disrupted / MTD deployments that land before the run
  deployment          ends, over every run; 95 % interval by resampling runs.

Declared durations: the reported corpus (runs_reported_summaries.pkl for NCR,
time_lost_numbers_reported.json for blocked per deployment). Unmapped tactics at
0 s: no MTD from D.6's rows (runs_duration_ablation.jsonl, unmapped_zero), MTD
from runs_unmapped_mtd.jsonl.

    PYTHONPATH=src python experiments/ch6_further_analyses/analyse_unmapped_mtd.py
"""
from __future__ import annotations

import importlib.util
import json
import pickle
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXP = ROOT / "experiments"
RUNS = EXP / "ch6_further_analyses" / "runs_unmapped_mtd.jsonl"
D6_ROWS = EXP / "ch6_further_analyses" / "runs_duration_ablation.jsonl"
SUMMARIES = EXP / "ch5_defended" / "runs_reported_summaries.pkl"
TIME_LOST = ROOT / "experiments/ch5_defended/time_lost_numbers_reported.json"
OUT = HERE / "unmapped_mtd_numbers.json"
FOUR = ("objective_exfiltration", "objective_impact", "objective_exfiltration_impact", "objective_none_c2")
CONDITIONS = ("ip_shuffle", "service_diversity")
INTERVAL = 200
# the attack actions a service-layer deployment disrupts (Section 2.2.3)
SERVICE_DISRUPTABLE = ("SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE")
N_BOOT = 2_000


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


time_lost = _load("ch5_time_lost", ROOT / "experiments/ch5_defended/time_lost.py")


def per_seed(pairs, per=4) -> np.ndarray:
    by = defaultdict(list)
    for seed, hosts in pairs:
        by[seed].append(float(hosts))
    assert all(len(v) == per for v in by.values()), "a seed is missing an attack profile"
    return np.array([np.mean(by[k]) for k in sorted(by)], dtype=float)


def ncr_reduction(none: np.ndarray, cond: np.ndarray, rng) -> dict:
    assert len(none) == len(cond)
    idx = rng.integers(0, len(none), (N_BOOT, len(none)))
    boot = 1.0 - cond[idx].mean(1) / none[idx].mean(1)
    return {"point": float(1.0 - cond.mean() / none.mean()),
            "lo": float(np.percentile(boot, 2.5)), "hi": float(np.percentile(boot, 97.5)),
            "ncr_none_hosts": float(none.mean()), "ncr_mtd_hosts": float(cond.mean())}


def blocked(views: list[dict], rng) -> dict:
    bl = np.array([v["blocked"] for v in views], float)
    nd = np.array([v["deployments_in_run"] for v in views], float)
    idx = rng.integers(0, len(views), (N_BOOT, len(views)))
    boot = bl[idx].sum(1) / nd[idx].sum(1)
    return {"point": float(bl.sum() / nd.sum()),
            "lo": float(np.percentile(boot, 2.5)), "hi": float(np.percentile(boot, 97.5)),
            "runs": len(views)}


def apart(a: dict, b: dict) -> bool:
    return a["lo"] > b["hi"] or b["lo"] > a["hi"]


def main() -> int:
    rng = np.random.default_rng(20261018)
    cells, _ = pickle.load(SUMMARIES.open("rb"))

    def reported(arm, profile, cond, iv):
        return cells[("core", arm, profile, "targeted", cond, iv, "shifted", "v4_failure_only")]

    tl = json.loads(TIME_LOST.read_text())["cells"]
    declared, baseline = {}, {}
    apt_none = per_seed((r["seed"], r["hosts"]) for p in FOUR for r in reported("movement", p, "none", 0))
    base_none = per_seed(((r["seed"], r["hosts"]) for r in reported("baseline", "baseline", "none", 0)), per=1)
    for c in CONDITIONS:
        apt_c = per_seed((r["seed"], r["hosts"]) for p in FOUR for r in reported("movement", p, c, INTERVAL))
        base_c = per_seed(((r["seed"], r["hosts"]) for r in reported("baseline", "baseline", c, INTERVAL)), per=1)
        declared[c] = {"ncr_reduction": ncr_reduction(apt_none, apt_c, rng),
                       "blocked_per_deployment": tl[f"movement|{c}|{INTERVAL}"]["blocked_per_deployment"]}
        baseline[c] = {"ncr_reduction": ncr_reduction(base_none, base_c, rng),
                       "blocked_per_deployment": tl[f"baseline|{c}|{INTERVAL}"]["blocked_per_deployment"]}

    none_rows = []
    with D6_ROWS.open() as fh:
        for line in fh:
            if '"variant": "unmapped_zero"' in line[:200]:
                r = json.loads(line)
                none_rows.append((r["seed"], r["compromised"]))
    mtd_hosts, mtd_views, errors = defaultdict(list), defaultdict(list), 0
    # where its time goes (Section 6.2's paragraph on the service layer): the share
    # of run time in executed attack actions, by attack action, pooled over runs
    time_in, run_time = defaultdict(lambda: defaultdict(float)), defaultdict(float)
    with RUNS.open() as fh:
        for line in fh:
            r = json.loads(line)
            if "error" in r:
                errors += 1
                continue
            mtd_hosts[r["condition"]].append((r["seed"], r["compromised"]))
            mtd_views[r["condition"]].append(time_lost.view(r))
            run_time[r["condition"]] += float(r["termination_time"])
            for x in r["records"]:
                if x[9] == "action-bearing" and x[1] and not x[4]:
                    time_in[r["condition"]][x[1]] += x[8] - x[7]
    if errors:
        raise SystemExit(f"{errors} error rows; refusing to read")
    unm_none = per_seed(none_rows)
    unmapped = {}
    for c in CONDITIONS:
        n = len(mtd_hosts[c])
        if n != 4 * len(unm_none):
            raise SystemExit(f"{c}: {n} runs of {4 * len(unm_none)}; incomplete")
        share = {v: t / run_time[c] for v, t in time_in[c].items()}
        unmapped[c] = {"ncr_reduction": ncr_reduction(unm_none, per_seed(mtd_hosts[c]), rng),
                       "blocked_per_deployment": blocked(mtd_views[c], rng),
                       "time_share_by_action": share,
                       "time_share_service_layer_disruptable": sum(
                           share.get(v, 0.0) for v in SERVICE_DISRUPTABLE)}

    sd_d, sd_u = declared["service_diversity"], unmapped["service_diversity"]
    rise = {m: sd_u[m]["point"] > sd_d[m]["point"] and apart(sd_u[m], sd_d[m])
            for m in ("ncr_reduction", "blocked_per_deployment")}
    verdict = ("SUPPORTED" if all(rise.values()) else
               "MECHANISM ONLY" if rise["blocked_per_deployment"] else "NOT SUPPORTED")
    lead = unmapped["ip_shuffle"]["ncr_reduction"]["point"] > sd_u["ncr_reduction"]["point"]
    lead_apart = apart(unmapped["ip_shuffle"]["ncr_reduction"], sd_u["ncr_reduction"])
    out = {"criterion": "run_unmapped_mtd.py docstring, fixed before the run",
           "interval_s": INTERVAL, "declared": declared, "unmapped_zero": unmapped,
           "baseline_attacker": baseline,
           "verdict": {"service_diversity_rises": rise, "a_or_b": verdict,
                       "c_host_lead_holds": lead, "c_intervals_apart": lead_apart}}
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    for name, block in (("declared", declared), ("unmapped at 0 s", unmapped), ("baseline", baseline)):
        for c in CONDITIONS:
            n, b = block[c]["ncr_reduction"], block[c]["blocked_per_deployment"]
            print(f"{name:16s} {c:18s} NCR red {n['point']:.3f} [{n['lo']:.3f}, {n['hi']:.3f}]  "
                  f"blocked/dep {b['point']:.3f} [{b['lo']:.3f}, {b['hi']:.3f}]")
    for c in CONDITIONS:
        u = unmapped[c]
        print(f"time share {c}: disruptable {u['time_share_service_layer_disruptable']:.3f}; "
              f"scan neighbours {u['time_share_by_action'].get('SCAN_NEIGHBOR', 0):.3f}")
    print("verdict", out["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
