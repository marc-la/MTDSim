"""Do random groups of the same sizes divide their steps among the tactics as
differently as the attack profiles do? (Marc 2026-10-12; handoff
docs/implementation/run_plans/2026-10-11_ch6_1_redraft_scrutiny.md section 24.6.)

Section 6.1 paragraph 1 says that outside actions on objectives the attack
profiles' differences are not shown to come from the objective, because c4,
whose attack flows neither stole data nor impeded systems, differs too. Marc's
reading: those differences may come from the partitioning. The partition
control (ch5_defended/partition_control.py) ran ten random partitions of the
38 attack flows into groups of the attack profiles' sizes (19, 7, 7, 5), with
no MTD on 1 000 seeds, and kept every step; Appendix G.7 reads only their ASP
and NCR. This reads their steps.

Per group (pooled over its 1 000 runs): relative tactic occurrence (Section
4.5.1) over the tactics outside actions on objectives (Collection,
Exfiltration and Impact removed, the rest renormalised). Between two groups:
the share of steps that lie in different tactics, half the sum of the absolute
differences (total variation distance; 0 = the same division, 1 = no tactic in
common). For each partition, the six pairs of its four groups; for the attack
profiles, their six pairs, from the reported corpus (runs_reported.jsonl,
seeds 0-999). Partitions replaced in the redraw of 2026-10-07 are read from the
redraw stream, as partition_control.py reads them.

    python experiments/ch6_further_analyses/partition_step_divergence.py
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent
PC_RUNS = RESULTS / "ch5_defended" / "runs_partition_control.jsonl"
PC_REDRAW = RESULTS / "ch5_defended" / "runs_partition_control_redraw.jsonl"
PC_MANIFEST = RESULTS.parent / "data" / "ogasp" / "partition_control" / "partitions.json"
REPORTED = RESULTS / "ch5_s531_unopposed" / "runs_reported.jsonl"
OUT = HERE / "partition_step_divergence_numbers.json"
FOUR = ("objective_exfiltration", "objective_impact", "objective_exfiltration_impact", "objective_none_c2")
CODE = dict(zip(FOUR, ("c1", "c2", "c3", "c4")))
AOO = {"collection", "exfiltration", "impact"}


def _counts_into(acc: dict, key, records) -> None:
    c = acc[key]
    for rec in records:
        c[rec[0]] += 1


def _stream(path: Path, acc: dict, skip: set, keep: set | None) -> int:
    n = 0
    with path.open() as fh:
        for line in fh:
            r = json.loads(line)
            if "error" in r or r.get("condition") != "none":
                continue
            assert r["horizon"] == 15_000 and r["overlay"] == "v4_failure_only", (r["horizon"], r["overlay"])
            k = r["partition"]
            if k in skip or (keep is not None and k not in keep):
                continue
            _counts_into(acc, (k, r["profile"]), r["records"])
            n += 1
    return n


def shares(c: Counter, drop: set) -> dict:
    kept = {t: v for t, v in c.items() if t not in drop}
    tot = sum(kept.values())
    return {t: v / tot for t, v in kept.items()}


def tv(a: dict, b: dict) -> float:
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in keys)


def pairs(groups: dict) -> dict:
    return {f"{CODE[x]}-{CODE[y]}": tv(groups[x], groups[y]) for x, y in itertools.combinations(FOUR, 2)}


def main() -> int:
    manifest = json.loads(PC_MANIFEST.read_text())
    gone = {r["partition"] for r in manifest.get("redraw_2026_10_07", {}).get("replaced", [])}
    acc: dict = defaultdict(Counter)
    n1 = _stream(PC_RUNS, acc, skip=gone, keep=None)
    n2 = _stream(PC_REDRAW, acc, skip=set(), keep=gone) if gone else 0
    real: dict = defaultdict(Counter)
    with REPORTED.open() as fh:
        for line in fh:
            r = json.loads(line)
            if r["arm"] != "baseline" and r["profile"] in FOUR:
                _counts_into(real, r["profile"], r["records"])

    out: dict = {"runs_read": {"partition_control": n1, "redraw": n2}, "replaced_partitions": sorted(gone)}
    for label, drop in (("outside_actions_on_objectives", AOO), ("all_tactics", set())):
        prof = pairs({p: shares(real[p], drop) for p in FOUR})
        parts = sorted({k for k, _ in acc})
        rnd = {str(k): pairs({p: shares(acc[(k, p)], drop) for p in FOUR}) for k in parts}
        flat = [v for d in rnd.values() for v in d.values()]
        out[label] = {
            "attack_profiles": prof,
            "attack_profiles_mean": float(np.mean(list(prof.values()))),
            "random_partitions": rnd,
            "random_mean_per_partition": {k: float(np.mean(list(d.values()))) for k, d in rnd.items()},
            "random_pairs_median": float(np.median(flat)),
            "random_pairs_range": [float(min(flat)), float(max(flat))],
            "partitions_with_mean_at_or_above_profiles": int(sum(
                np.mean(list(d.values())) >= np.mean(list(prof.values())) for d in rnd.values())),
        }
    # Each group's steps per tactic, so any later reading needs no re-stream.
    out["group_counts"] = {
        "attack_profiles": {CODE[p]: dict(real[p]) for p in FOUR},
        "random_partitions": {str(k): {CODE[p]: dict(acc[(k, p)]) for p in FOUR}
                              for k in sorted({k for k, _ in acc})},
    }
    OUT.write_text(json.dumps(out, indent=1))
    print(f"wrote {OUT}  runs {n1}+{n2}")
    for label in ("outside_actions_on_objectives", "all_tactics"):
        o = out[label]
        print(label)
        print("  attack profiles", {k: round(v, 3) for k, v in o["attack_profiles"].items()},
              "mean", round(o["attack_profiles_mean"], 3))
        print("  random partitions: mean per partition",
              sorted(round(v, 3) for v in o["random_mean_per_partition"].values()),
              "pairs median", round(o["random_pairs_median"], 3), "range",
              [round(x, 3) for x in o["random_pairs_range"]],
              "partitions >= profiles", o["partitions_with_mean_at_or_above_profiles"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
