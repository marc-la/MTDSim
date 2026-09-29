"""Dry run (2026-09-29, Marc: "time between successful tactics ... the Petri net
retraces to the equivalent tactic"): per cell at the 2 000 s interval,
(1) attack actions blocked (Brown 2023): actions an MTD deployment interrupts in
    flight, per run and as a share of actions; and the share of deployments that
    block an action;
(2) time to resume: from a blocked action's end to the start of the attacker's
    next run of the same action, censored at the run's end; plus, for reference,
    the attacker's usual gap between two runs of the same action with no MTD."""
import json, sys
from collections import defaultdict
import numpy as np
MECH = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle", "os_diversity", "service_diversity", "user_shuffle")
IV = 2000

def actions(r):
    """(verb, start, end, blocked_by_mtd) per action; baseline consecutive exploits collapsed."""
    out = []
    if r["arm"] == "movement":
        for x in r["records"]:
            if x[9] != "action-bearing" or not x[1] or x[2] == "PRECONDITION_UNMET": continue
            out.append((x[1], x[7], x[8], x[2] == "MTD_INTERRUPT"))
    else:
        for x in r["records"]:
            blk = x[5] is not None
            if out and x[0] == "EXPLOIT_VULN" and out[-1][0] == "EXPLOIT_VULN":
                v, s, e, b = out[-1]; out[-1] = (v, s, x[2], b or blk)
            else:
                out.append((x[0], x[1], x[2], blk))
    return out

def resume(acts, T):
    w = []
    for i, (v, s, e, b) in enumerate(acts):
        if not b: continue
        nxt = next((a[1] for a in acts[i + 1:] if a[0] == v), None)
        w.append((nxt - e, True) if nxt is not None else (T - e, False))
    return w

def usual_gap(acts):
    last, g = {}, []
    for v, s, e, b in acts:
        if v in last: g.append(s - last[v])
        last[v] = e
    return g

cells = defaultdict(lambda: {"runs": 0, "acts": 0, "blocked": 0, "deps": 0, "deps_blocking": 0, "waits": [], "gaps": []})
with open("data/results/ch5_defended/runs.jsonl") as f:
    for line in f:
        h = line[:400]
        if '"group": "core"' not in h or '"regime": "shifted"' not in h or '"objective": "targeted"' not in h: continue
        r = json.loads(line)
        if r["profile"] == "aggregate": continue
        if r["condition"] != "none" and (r["condition"] not in MECH or r["interval"] != IV): continue
        arm = "APT" if r["arm"] == "movement" else "baseline"
        c = cells[(arm, r["condition"])]
        acts = actions(r); T = max((a[2] for a in acts), default=0.0)
        c["runs"] += 1; c["acts"] += len(acts); c["blocked"] += sum(a[3] for a in acts)
        if r["condition"] == "none":
            c["gaps"] += usual_gap(acts); continue
        c["waits"] += resume(acts, max(T, r["termination_time"] if arm == "APT" else T))
        ends = [e[2] for e in r["mtd_executions"]]
        c["deps"] += len(ends)
        c["deps_blocking"] += sum(1 for d in ends if any(a[3] and d - 1.0 <= a[2] <= d + 30.0 for a in acts))  # APT records carry a 20 s confusion penalty past the landing
for arm in ("APT", "baseline"):
    g = cells[(arm, "none")]["gaps"]
    print(f"\n{arm}: usual gap between two runs of the same action, no MTD: median {np.median(g):.0f} s")
    print(f"  {'condition':18s} {'blocked/run':>11s} {'blocked share':>13s} {'deps blocking':>13s} {'resume median':>13s} {'resumed':>8s}")
    for m in MECH:
        c = cells[(arm, m)]
        if not c["runs"]: continue
        w = np.array([x for x, _ in c["waits"]]); o = np.array([y for _, y in c["waits"]])
        med = np.median(np.where(o, w, np.inf)) if len(w) else float("nan")
        print(f"  {m:18s} {c['blocked']/c['runs']:11.2f} {100*c['blocked']/max(1,c['acts']):12.1f}% {100*c['deps_blocking']/max(1,c['deps']):12.1f}% {med:12.0f}s {100*o.mean() if len(o) else 0:7.0f}%")
