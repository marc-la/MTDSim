# Dry run (2026-09-30), evidence for docs/implementation/disruption_mechanism.md: the APT model's failed actions per minute double after a host-layer deployment and decay over ~15 min; interrupts happen only at the deployment. Usage: python <this> OUT.json (from the main checkout root).
"""Event rates per minute around each MTD deployment, both attackers, 2 000 s interval.
Bins of 60 s from -300 to +900 s around each deployment's completion; counts pooled over
every deployment of every run, divided by the live minutes in the bin (a run that has
ended adds none). The no-MTD placebo reads the same seed's no-MTD run at the same moments."""
import json, sys
import numpy as np
from collections import defaultdict
RUNS = "data/results/ch5_defended/runs.jsonl"
MECH = ("ip_shuffle", "service_diversity", "port_shuffle", "complete_topology", "host_topology", "os_diversity", "user_shuffle")
EDGES = np.arange(-300, 901, 60)
COMP_M = {("BRUTE_FORCE", "TRUE"), ("SCAN_PORT", "TRUE"), ("EXPLOIT_VULN", "EXPLOIT_COMPROMISED")}
def events(r):
    """list of (start, kind-set) per action; kinds: act, interrupted, failed(movement only), comp"""
    ev = []
    if r["arm"] == "movement":
        for x in r["records"]:
            place, verb, out, verdict, blocked, intr, dwell, s, e, cls = x
            if cls != "action-bearing" or not verb: continue
            k = {"act"}
            if intr: k.add("interrupted")
            if verdict == "failure": k.add("failed")
            if blocked: k.add("blocked")
            if (verb, out) in COMP_M: k.add("comp")
            ev.append((s, e, k))
    else:
        prev = None
        for x in r["records"]:
            name, s, e, comp, uuid, intr = x
            k = set()
            if not (name == "EXPLOIT_VULN" and prev == "EXPLOIT_VULN"): k.add("act")
            if intr: k.add("interrupted")
            if comp is not None: k.add("comp")
            prev = name
            ev.append((s, e, k))
    return ev
runs, none = [], {}
with open(RUNS) as f:
    for line in f:
        h = line[:400]
        if '"group": "core"' not in h or '"regime": "shifted"' not in h or '"objective": "targeted"' not in h: continue
        r = json.loads(line)
        if r["profile"] == "aggregate": continue
        if r["condition"] == "none":
            none[(r["arm"], r["profile"], r["seed"])] = {"T": r["termination_time"], "ev": events(r)}
        elif r["condition"] in MECH and r["interval"] == 2000:
            runs.append({"arm": r["arm"], "profile": r["profile"], "seed": r["seed"], "cond": r["condition"],
                         "T": r["termination_time"], "ev": events(r),
                         "land": [e[2] for e in r["mtd_executions"] if 300 <= e[2] < r["termination_time"]]})
KINDS = ("act", "interrupted", "failed", "blocked", "comp")
def read(rs, placebo):
    cnt = {k: np.zeros(len(EDGES) - 1) for k in KINDS}; live = np.zeros(len(EDGES) - 1)
    for r in rs:
        src = none[(r["arm"], r["profile"], r["seed"])] if placebo else r
        starts = np.array([s for s, _, _ in src["ev"]]); kinds = [k for _, _, k in src["ev"]]
        for t in r["land"]:
            lo = np.clip(t + EDGES[:-1], 0, src["T"]); hi = np.clip(t + EDGES[1:], 0, src["T"])
            live += (hi - lo) / 60
            idx = np.searchsorted(t + EDGES, starts, side="right") - 1
            for i, k in zip(idx, kinds):
                if 0 <= i < len(EDGES) - 1 and starts is not None:
                    for kk in k: cnt[kk][i] += 1
    return {k: cnt[k] / np.where(live > 0, live, np.nan) for k in KINDS}, live
out = {}
for arm in ("movement", "baseline"):
    for m in MECH:
        rs = [r for r in runs if r["arm"] == arm and r["cond"] == m]
        a, live = read(rs, False); p, _ = read(rs, True)
        out[f"{arm}|{m}"] = {"n_deployments": sum(len(r["land"]) for r in rs),
            **{k: a[k].tolist() for k in KINDS}, **{"none_" + k: p[k].tolist() for k in KINDS}}
json.dump({"edges": EDGES.tolist(), "reads": out}, open(sys.argv[1], "w"))
mids = (EDGES[:-1] + EDGES[1:]) / 2
for key in ("movement|ip_shuffle", "baseline|ip_shuffle", "movement|service_diversity", "baseline|service_diversity"):
    o = out[key]; print(key, "deployments", o["n_deployments"])
    for k in ("act", "interrupted", "failed", "comp"):
        print("  %-11s" % k, " ".join("%5.2f" % v for v in o[k]))
        print("  %-11s" % ("none " + k), " ".join("%5.2f" % v for v in o["none_" + k]))
    print("  bins", " ".join("%5d" % m for m in mids))
