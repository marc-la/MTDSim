"""The tactic-durations ablation — the read half (run_duration_ablation.py).

Every number Table 5.2 reports, computed by the chapter 5 analyser's own
functions (ch5_s531_unopposed/analyse.py) on four rows per attack profile:

  reported        the APT attacker model as Table 5.2 reports it (runs_reported.jsonl)
  unmapped_zero   Arm A: the unmapped tactics take no time
  baseline_pace   Arm B: Arm A, and each mapped tactic at the baseline attacker's
                  mean time for its attack action
  baseline        the baseline attacker (runs_reported.jsonl; it consumes no
                  tactic duration, so it is not re-run)

Also, per row: the share of the run spent in unmapped tactics and the share of
dispatched attack actions blocked for a missing precondition (Appendix G.3's
two measures), distinct openings over eight steps, and the runs that hit the
event cap. "Gap closed" is (arm - reported) / (baseline - reported) for ASP and
NCR: the share of the APT attacker model's gap to the baseline attacker that
the arm removes. Intervals: ASP, the shares and the gap closed by a 2 000-
resample percentile bootstrap over seeds (paired: one resample of seeds feeds
the arm, the reported row and the baseline); the rest as the analyser gives
them.

    PYTHONPATH=src python data/results/ch6_further_analyses/analyse_duration_ablation.py
"""
from __future__ import annotations

import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNS = HERE / "runs_duration_ablation.jsonl"
REPORTED = ROOT / "data/results/ch5_s531_unopposed/runs_reported.jsonl"
OUT = HERE / "duration_ablation_numbers.json"
N_BOOT = 2_000
SEED = 20261012
CODE = {
    "objective_exfiltration": "c1",
    "objective_impact": "c2",
    "objective_exfiltration_impact": "c3",
    "objective_none_c2": "c4",
}


def _load_analyser():
    path = ROOT / "data/results/ch5_s531_unopposed/analyse.py"
    spec = importlib.util.spec_from_file_location("ch5_unopposed_analyse", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


A = _load_analyser()


def _boot(x, idx) -> dict:
    x = np.asarray(x, float)
    b = x[idx].mean(axis=1)
    return {"mean": float(x.mean()), "lo": float(np.percentile(b, 2.5)),
            "hi": float(np.percentile(b, 97.5))}


def _per_run(row: dict) -> dict:
    recs = row["records"]
    end = max((r[8] for r in recs), default=0.0)
    acts = [r for r in recs if r[9] == "action-bearing" and r[1]]
    nb = sum(1 for r in acts if r[4])
    return {
        "asp": float(row["reached_objective"] and row["database_hosts_reached"] > 0),
        "ncr": row["compromised"] / A.NET_HOSTS,
        "unmapped_share": (sum(r[8] - r[7] for r in recs if r[9] == "dwell-only") / end) if end > 0 else 0.0,
        "blocked_share": (nb / len(acts)) if acts else 0.0,
    }


def summarise(rows: list[dict], rng) -> dict:
    rows = sorted(rows, key=lambda r: r["seed"])
    runs = [A._movement_result(r) for r in rows]
    stage_of = A.M.load_stage_of()
    table = A.movement_row(runs, stage_of)
    stealth = A.stealth_movement(runs)
    per = [_per_run(r) for r in rows]
    idx = rng.integers(0, len(per), size=(N_BOOT, len(per)))
    return {
        "n": len(rows),
        "asp": _boot([p["asp"] for p in per], idx),
        "ncr": _boot([p["ncr"] for p in per], idx),
        "mttc": table["mttc_target"],
        "attack_rate": stealth["attack_rate"],
        "attack_confidentiality": A.confidentiality(
            [A._actions_movement(r)[0] for r in runs], rng),
        "unmapped_time_share": _boot([p["unmapped_share"] for p in per], idx),
        "blocked_share": _boot([p["blocked_share"] for p in per], idx),
        "distinct_openings_8": table["distinct_openings"]["8"],
        "max_events_hit": sum(1 for r in runs if A.M.terminal_mode(r) == "max_events"),
        # the stall reading (c3): when the run's last successful exploit falls,
        # and which seeds reach a target host
        "last_exploit_success_median_s": float(np.median([
            max((x[8] for x in r["records"] if x[1] == "EXPLOIT_VULN" and x[3] == "success"), default=0.0)
            for r in rows])),
        "success_seeds": [r["seed"] for r in rows if r["reached_objective"] and r["database_hosts_reached"] > 0],
        "_asp": [p["asp"] for p in per], "_ncr": [p["ncr"] for p in per],
    }


def summarise_baseline(rows: list[dict], rng) -> dict:
    rows = sorted(rows, key=lambda r: r["seed"])
    table = A.baseline_row(rows)
    stealth = A.stealth_baseline(rows)
    asp = [float(any(rec[3] is not None and rec[3] in set(r["target_hosts"]) for rec in r["records"])
                 and r["reached_objective"]) for r in rows]
    ncr = [r["compromised"] / A.NET_HOSTS for r in rows]
    idx = rng.integers(0, len(rows), size=(N_BOOT, len(rows)))
    return {
        "n": len(rows),
        "asp": _boot(asp, idx), "ncr": _boot(ncr, idx),
        "asp_table_rule": table["target_reach"],
        "mttc": table["mttc_target"],
        "attack_rate": stealth["attack_rate"],
        "attack_confidentiality": A.confidentiality(
            [A._actions_baseline(r)[0] for r in rows], rng),
        "_asp": asp, "_ncr": ncr,
    }


def gap_closed(arm: list, rep: list, base: list, rng) -> dict:
    arm, rep, base = (np.asarray(v, float) for v in (arm, rep, base))
    point = float((arm.mean() - rep.mean()) / (base.mean() - rep.mean()))
    idx = rng.integers(0, len(arm), size=(N_BOOT, len(arm)))
    b = (arm[idx].mean(1) - rep[idx].mean(1)) / (base[idx].mean(1) - rep[idx].mean(1))
    return {"point": point, "lo": float(np.percentile(b, 2.5)), "hi": float(np.percentile(b, 97.5))}


def main() -> int:
    rng = np.random.default_rng(SEED)
    cells: dict[tuple, list] = defaultdict(list)
    errors = 0
    with RUNS.open() as fh:
        for line in fh:
            row = json.loads(line)
            if "error" in row:
                errors += 1
                continue
            cells[(row["variant"], row["profile"])].append(row)
    base_rows = []
    with REPORTED.open() as fh:
        for line in fh:
            row = json.loads(line)
            if row["arm"] == "baseline":
                base_rows.append(row)
            elif row["profile"] in CODE:
                cells[("reported", row["profile"])].append(row)
    assert errors == 0, f"{errors} error rows"
    for k, v in cells.items():
        assert sorted(r["seed"] for r in v) == list(range(1_000)), (k, len(v))

    base = summarise_baseline(base_rows, rng)
    out: dict = {"baseline": {k: v for k, v in base.items() if not k.startswith("_")}}
    keep: dict = {}
    for profile, code in CODE.items():
        out[code] = {}
        rep = None
        for variant in ("reported", "unmapped_zero", "baseline_pace"):
            s = summarise(cells[(variant, profile)], rng)
            if variant == "reported":
                rep = s
            else:
                s["gap_closed"] = {m: gap_closed(s[f"_{m}"], rep[f"_{m}"], base[f"_{m}"], rng)
                                   for m in ("asp", "ncr")}
            out[code][variant] = s
        keep[code] = {v: (s.pop("_asp"), s.pop("_ncr")) for v, s in out[code].items()}
    # The four attack profiles pooled, each weighted equally (1 000 runs each),
    # seed-paired: the APT attacker model as a whole, the unit Section 6.1 reads.
    for code in CODE.values():
        sa, sb, sr = (set(out[code][v]["success_seeds"]) for v in ("unmapped_zero", "baseline_pace", "reported"))
        out[code]["success_seeds_overlap"] = {"unmapped_zero_and_baseline_pace": len(sa & sb),
                                              "unmapped_zero": len(sa), "baseline_pace": len(sb),
                                              "reported_within_both": len(sr & sa & sb), "reported": len(sr)}
    out["pooled"] = {}
    for variant in ("unmapped_zero", "baseline_pace"):
        rep_asp = [x for c in CODE.values() for x in keep[c]["reported"][0]]
        rep_ncr = [x for c in CODE.values() for x in keep[c]["reported"][1]]
        arm_asp = [x for c in CODE.values() for x in keep[c][variant][0]]
        arm_ncr = [x for c in CODE.values() for x in keep[c][variant][1]]
        b_asp, b_ncr = base["_asp"] * 4, base["_ncr"] * 4
        out["pooled"][variant] = {
            "asp_reported": float(np.mean(rep_asp)), "asp": float(np.mean(arm_asp)),
            "ncr_reported": float(np.mean(rep_ncr)), "ncr": float(np.mean(arm_ncr)),
            "gap_closed": {"asp": gap_closed(arm_asp, rep_asp, b_asp, rng),
                           "ncr": gap_closed(arm_ncr, rep_ncr, b_ncr, rng)},
        }
    OUT.write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    print(f"wrote {OUT}")

    def f(d, nd=3):
        return f"{d['mean']:.{nd}f} [{d['lo']:.{nd}f}, {d['hi']:.{nd}f}]"

    print(f"baseline  ASP {f(base['asp'])} (table rule {base['asp_table_rule']:.3f})  "
          f"NCR {f(base['ncr'])}  rate {base['attack_rate']['mean']:.3f}  "
          f"conf {base['attack_confidentiality']['point']:.3f}  "
          f"MTTC {base['mttc']['mean'] if base['mttc'] else None} n={base['mttc']['n'] if base['mttc'] else 0}")
    for code in CODE.values():
        for v, s in out[code].items():
            g = s.get("gap_closed")
            gs = (f"  gap closed ASP {g['asp']['point']:.2f} [{g['asp']['lo']:.2f}, {g['asp']['hi']:.2f}]"
                  f" NCR {g['ncr']['point']:.2f} [{g['ncr']['lo']:.2f}, {g['ncr']['hi']:.2f}]") if g else ""
            m = s["mttc"]
            print(f"{code} {v:14s} ASP {f(s['asp'])}  NCR {f(s['ncr'])}  "
                  f"rate {s['attack_rate']['mean']:.3f}  conf {s['attack_confidentiality']['point']:.3f}  "
                  f"MTTC {(round(m['mean']) if m else None)} n={(m['n'] if m else 0)}  "
                  f"unmapped {s['unmapped_time_share']['mean']:.2f}  blocked {s['blocked_share']['mean']:.2f}  "
                  f"open8 {s['distinct_openings_8']}  cap {s['max_events_hit']}{gs}")
    for v, g in out["pooled"].items():
        print(f"pooled {v:14s} ASP {g['asp_reported']:.3f} -> {g['asp']:.3f}  gap closed "
              f"{g['gap_closed']['asp']['point']:.2f} [{g['gap_closed']['asp']['lo']:.2f}, {g['gap_closed']['asp']['hi']:.2f}]"
              f"  NCR {g['ncr_reported']:.3f} -> {g['ncr']:.3f}  gap closed {g['gap_closed']['ncr']['point']:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
