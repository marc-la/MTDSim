"""Dry run (2026-09-30, Marc: "an MTD deployment happens, count the time to the next
compromise; the difference from the no-MTD run from the same point is the time lost").

For each deployment of a single MTD mechanism at the 2 000 s interval that completes
while the attacker is still acting: the time from the deployment's completion to the
attacker's next compromised host, and the same from the same moment on the same seed's
no-MTD run. Each is capped at the next deployment (at most the 2 000 s interval), so a
deployment is charged only up to the next one; a wait that reaches the cap counts as
the cap (the restricted mean of survival analysis). Time lost = mean capped wait with
the MTD - mean capped wait with no MTD. A deployment whose no-MTD run had already
ended (its target taken) has no reference and is dropped; the share dropped is shown.
The baseline's end is its last action (its termination_time is always the horizon).
Run from the main checkout root: python <this> [OUT.json]"""
import json, sys
import numpy as np
from collections import defaultdict
RUNS = "data/results/ch5_defended/runs.jsonl"
MECH = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle", "os_diversity", "service_diversity", "user_shuffle")
COMP_M = {("BRUTE_FORCE", "TRUE"), ("SCAN_PORT", "TRUE"), ("EXPLOIT_VULN", "EXPLOIT_COMPROMISED")}

def comp_and_end(r):
    if r["arm"] == "movement":
        c = [x[8] for x in r["records"] if (x[1], x[2]) in COMP_M]
        end = r["termination_time"]
    else:
        c = [x[2] for x in r["records"] if x[3] is not None]
        end = max((x[2] for x in r["records"]), default=0.0)
    return np.sort(np.minimum(np.array(c, float), end)), end

def wait(comp, t, cap):
    j = np.searchsorted(comp, t, "right")
    return min(comp[j] - t, cap) if j < len(comp) else cap

none, runs = {}, []
with open(RUNS) as f:
    for line in f:
        h = line[:400]
        if '"group": "core"' not in h or '"regime": "shifted"' not in h or '"objective": "targeted"' not in h: continue
        r = json.loads(line)
        if r["profile"] == "aggregate": continue
        if r["condition"] == "none":
            none[(r["arm"], r["profile"], r["seed"])] = comp_and_end(r)
        elif r["condition"] in MECH and r["interval"] == 2000:
            c, end = comp_and_end(r)
            runs.append((r["arm"], r["condition"], (r["arm"], r["profile"], r["seed"]), c, end, sorted(e[2] for e in r["mtd_executions"])))
cells = defaultdict(lambda: {"mtd": [], "none": [], "dropped": 0, "deps": 0})
for arm, m, key, c, end, lands in runs:
    nc, nend = none[key]
    for i, t in enumerate(lands):
        if t >= end: continue
        cell = cells[(arm, m)]; cell["deps"] += 1
        cap = min((lands[i + 1] if i + 1 < len(lands) else t + 2000.0) - t, 2000.0)
        if t >= nend:
            cell["dropped"] += 1; continue
        cell["mtd"].append(wait(c, t, cap)); cell["none"].append(wait(nc, t, cap))
out = {}
print("time from a deployment to the next compromise, capped at the next deployment (mean, s)")
for arm in ("movement", "baseline"):
    for m in MECH:
        c = cells[(arm, m)]; a, b = np.array(c["mtd"]), np.array(c["none"])
        rng = np.random.default_rng(20260930); idx = rng.integers(0, len(a), (2000, len(a)))
        boot = (a[idx].mean(1) - b[idx].mean(1))
        out[f"{arm}|{m}"] = {"deployments": c["deps"], "dropped": c["dropped"], "with_mtd": float(a.mean()), "no_mtd": float(b.mean()),
                             "time_lost": float(a.mean() - b.mean()), "ci95": [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
                             "no_compromise_before_next_deployment_mtd": float((a >= 2000 - 1e-6).mean()), "no_compromise_none": float((b >= 2000 - 1e-6).mean())}
        o = out[f"{arm}|{m}"]
        print(f"  {'APT' if arm == 'movement' else 'baseline':8s} {m:18s} with MTD {o['with_mtd']:6.0f}  no MTD {o['no_mtd']:6.0f}  time lost {o['time_lost']:5.0f} [{o['ci95'][0]:5.0f}, {o['ci95'][1]:5.0f}]"
              f"  none before next: {100*o['no_compromise_before_next_deployment_mtd']:3.0f}% vs {100*o['no_compromise_none']:3.0f}%  dropped {c['dropped']}/{c['deps']}")
if len(sys.argv) > 1: json.dump(out, open(sys.argv[1], "w"), indent=1)
