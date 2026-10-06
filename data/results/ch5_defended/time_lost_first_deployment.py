"""Diagnostic: is negative time lost per MTD deployment a reference artefact?

Reads runs_reported.jsonl as time_lost.py does (2 000 s, the seven mechanisms, no
MTD). Per deployment kept by time_lost.py's rule, records:
  - d      = wait with MTD - wait on the no-MTD twin from the same clock moment (capped)
  - first  = is this the run's first deployment (both runs identical up to it?)
  - same   = were the two runs' compromise times identical up to the deployment
  - gap    = hosts compromised by t: defended minus twin (progress mismatch)
  - blocked= did this deployment cut off an attack action
Read-only; writes time_lost_first_deployment_numbers.json beside the corpus.
Record: docs/handoffs/2026-10-06_ch5_results_prose_redraft.md section 8 (Marc 2026-10-06: "I don't expect it to speed up").
"""
import json, sys
from collections import defaultdict
from pathlib import Path
import numpy as np

RUNS = Path("/home/marc/GitHub/MTDSim/data/results/ch5_defended/runs_reported.jsonl")
OUT = Path(__file__).with_name("time_lost_first_deployment_numbers.json")
MECH = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle",
        "os_diversity", "service_diversity", "user_shuffle")
IV = 2000
COMP_MOV = {("BRUTE_FORCE", "TRUE"), ("SCAN_PORT", "TRUE"), ("EXPLOIT_VULN", "EXPLOIT_COMPROMISED")}


def view(r):
    if r["arm"] == "movement":
        comp = sorted(float(x[8]) for x in r["records"] if (x[1], x[2]) in COMP_MOV)
        end = float(r["termination_time"])
        # interrupted records: (end time) -- the interrupt lands at the deployment's completion
        ints = sorted(float(x[8]) for x in r["records"] if x[2] == "MTD_INTERRUPT")
        lag = 60.0  # the model's interrupted record ends after the confusion penalty
    else:
        comp = sorted(float(x[2]) for x in r["records"] if x[3] is not None)
        end = max((float(x[2]) for x in r["records"]), default=0.0)
        ints = sorted(float(x[2]) for x in r["records"] if x[5] is not None)
        lag = 1.0
    comp = [min(c, end) for c in comp]
    land = sorted(float(e[2]) for e in r["mtd_executions"])
    return dict(arm=r["arm"], prof=r["profile"], seed=r["seed"], cond=r["condition"],
                iv=r["interval"], end=end, comp=np.array(comp), ints=np.array(ints), lag=lag, land=land)


def wait(comp, t, cap):
    j = np.searchsorted(comp, t, "right")
    return float(min(comp[j] - t, cap)) if j < len(comp) else cap


def main():
    runs = []
    with RUNS.open() as f:
        for line in f:
            h = line[:400]
            if '"group": "core"' not in h or '"regime": "shifted"' not in h or '"objective": "targeted"' not in h:
                continue
            r = json.loads(line)
            if r["profile"] == "aggregate":
                continue
            if r["condition"] != "none" and (r["condition"] not in MECH or r["interval"] != IV):
                continue
            runs.append(view(r))
    none = {(r["arm"], r["prof"], r["seed"]): r for r in runs if r["cond"] == "none"}
    rows = defaultdict(list)
    for r in runs:
        if r["cond"] == "none":
            continue
        tw = none[(r["arm"], r["prof"], r["seed"])]
        L = r["land"]
        for i, t in enumerate(L):
            if t >= r["end"] or t >= tw["end"]:
                continue
            cap = min((L[i + 1] if i + 1 < len(L) else t + IV) - t, IV)
            d = wait(r["comp"], t, cap) - wait(tw["comp"], t, cap)
            a = r["comp"][r["comp"] <= t]; b = tw["comp"][tw["comp"] <= t]
            same = len(a) == len(b) and np.allclose(a, b)
            gap = len(a) - len(b)
            ints = r["ints"]
            blocked = bool(np.any((ints >= t - 1.0) & (ints <= t + r["lag"])))
            rows[(r["arm"], r["cond"])].append((d, i == 0, same, gap, blocked))
    out = {}
    for (arm, m), v in sorted(rows.items()):
        a = np.array(v, dtype=object)
        d = np.array([x[0] for x in v], float)
        first = np.array([x[1] for x in v]); same = np.array([x[2] for x in v])
        gap = np.array([x[3] for x in v]); blk = np.array([x[4] for x in v])
        def mean(mask):
            return [float(d[mask].mean()) if mask.any() else None, int(mask.sum())]
        out[f"{arm}|{m}"] = {
            "all": mean(np.ones_like(first, bool)),
            "first_deployment": mean(first),
            "state_identical": mean(same),
            "state_differs": mean(~same),
            "blocked": mean(blk), "not_blocked": mean(~blk),
            "blocked_and_identical": mean(blk & same),
            "gap<0 (defended behind)": mean(gap < 0), "gap=0": mean(gap == 0), "gap>0": mean(gap > 0),
        }
    OUT.write_text(json.dumps(out, indent=1))
    for k, v in out.items():
        print(k)
        for kk, vv in v.items():
            print(f"   {kk:26s} {('-' if vv[0] is None else round(vv[0],1))!s:>8}  n={vv[1]}")


if __name__ == "__main__":
    main()
