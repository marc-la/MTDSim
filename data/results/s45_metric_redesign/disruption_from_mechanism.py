"""Dry run (2026-09-30): the two disruption metrics derived from the mechanism in
docs/implementation/disruption_mechanism.md, on the 2 000 s interval, c1-c4 pooled.

ATTACK ACTIONS BLOCKED (Brown 2023, Sec. III-D and IV-A): an action a deployment
cuts off while it runs. APT model: a row with outcome MTD_INTERRUPT (an interrupt on
a dwell-only tactic or on a dispatch whose precondition was unmet stops no action, so
it is not a blocked action). Baseline: a row with interrupted_in set. Reported per
deployment, over the deployments that complete while the attacker is still acting
(the baseline's termination_time is always the horizon, so its last action's end is
used instead: mechanism record, section D).

TIME TO RESUME A BLOCKED ACTION: from the deployment's completion (the landing,
which is when the interrupt happens on both attackers) to the start of the attacker's
next run of the same action (a row that runs on the network: not blocked, not
interrupted). A blocked action never run again is unresumed and counts as longer than
every resumed one. Reference: with no MTD, the attacker's usual time from the end of
one run of an action to the start of its next run of the same action.

Run from the main checkout's root (runs.jsonl is untracked):
    python <this file> OUT.json [PREVIEW.png]
"""
import json, sys
import numpy as np
from collections import defaultdict

RUNS = "data/results/ch5_defended/runs.jsonl"
MECH = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle", "os_diversity", "service_diversity", "user_shuffle")
IV = 2000
GRID = np.arange(0, 1201, 15)


def rows(r):
    """(verb, start, end, runs, blocked) per action row; runs = it ran on the network."""
    out = []
    if r["arm"] == "movement":
        for x in r["records"]:
            if x[9] != "action-bearing" or not x[1]:
                continue
            blocked = x[2] == "MTD_INTERRUPT"
            out.append((x[1], x[7], x[8], not x[4] and not x[5], blocked))
    else:
        prev = None
        for x in r["records"]:
            if x[0] == "EXPLOIT_VULN" and prev == "EXPLOIT_VULN" and out:
                v, s, e, ran, b = out[-1]
                out[-1] = (v, s, x[2], ran and x[5] is None, b or x[5] is not None)
            else:
                out.append((x[0], x[1], x[2], x[5] is None, x[5] is not None))
            prev = x[0]
    return out


def landing_of(end, landings):
    """The deployment completion that interrupted a row ending at `end` (APT rows carry
    the ~20 s penalty past the landing; baseline rows end at it)."""
    c = [t for t in landings if end - 30.0 <= t <= end + 1e-6]
    return max(c) if c else None


cells = defaultdict(lambda: {"deps": 0, "blocked": 0, "waits": [], "gaps": []})
with open(RUNS) as f:
    for line in f:
        h = line[:400]
        if '"group": "core"' not in h or '"regime": "shifted"' not in h or '"objective": "targeted"' not in h:
            continue
        r = json.loads(line)
        if r["profile"] == "aggregate":
            continue
        if r["condition"] != "none" and (r["condition"] not in MECH or r["interval"] != IV):
            continue
        arm = "APT" if r["arm"] == "movement" else "baseline"
        c = cells[(arm, r["condition"])]
        a = rows(r)
        live_end = max((x[2] for x in a), default=0.0)
        if r["condition"] == "none":
            last = {}
            for v, s, e, ran, b in a:
                if not ran:
                    continue
                if v in last:
                    c["gaps"].append(s - last[v])
                last[v] = e
            continue
        landings = [e[2] for e in r["mtd_executions"] if e[2] <= live_end]
        c["deps"] += len(landings)
        for i, (v, s, e, ran, b) in enumerate(a):
            if not b:
                continue
            t0 = landing_of(e, landings)
            if t0 is None:
                continue
            c["blocked"] += 1
            nxt = next((x[1] for x in a[i + 1:] if x[0] == v and x[3]), None)
            c["waits"].append(nxt - t0 if nxt is not None else np.inf)

out = {"grid": GRID.tolist(), "cells": {}}
for (arm, m), c in sorted(cells.items()):
    if m == "none":
        g = np.array(c["gaps"])
        out["cells"][f"{arm}|none"] = {"median_gap": float(np.median(g)), "curve": [float((g <= t).mean()) for t in GRID]}
        continue
    w = np.array(c["waits"])
    out["cells"][f"{arm}|{m}"] = {
        "deployments": c["deps"], "blocked": c["blocked"], "blocked_per_deployment": c["blocked"] / max(1, c["deps"]),
        "median_resume": float(np.median(w)), "resumed": float(np.isfinite(w).mean()),
        "curve": [float((w <= t).mean()) for t in GRID]}
json.dump(out, open(sys.argv[1], "w"), indent=1)

for arm in ("APT", "baseline"):
    print(f"{arm}: usual gap between two runs of the same action, no MTD: median {out['cells'][arm + '|none']['median_gap']:.0f} s")
    for m in MECH:
        o = out["cells"][f"{arm}|{m}"]
        print(f"  {m:18s} deployments {o['deployments']:5d}  blocked per deployment {o['blocked_per_deployment']:.2f}  "
              f"median time to resume {o['median_resume']:5.0f} s  resumed {100 * o['resumed']:3.0f} %")

if len(sys.argv) > 2:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    col = {"APT": "#1f4e8c", "baseline": "#777777"}
    for k, (title, ms) in enumerate((("host layer: IP shuffle", ("ip_shuffle",)), ("service layer: service diversity", ("service_diversity",)))):
        for arm in ("APT", "baseline"):
            for m in ms:
                ax[k].plot(GRID, out["cells"][f"{arm}|{m}"]["curve"], color=col[arm], lw=2, label=f"{arm}, after a block")
            ax[k].plot(GRID, out["cells"][f"{arm}|none"]["curve"], color=col[arm], lw=1, ls="--", label=f"{arm}, usual gap (no MTD)")
        ax[k].set_title(title); ax[k].set_xlabel("time since the deployment completed (s)"); ax[k].set_ylim(0, 1)
        ax[k].set_ylabel("share of blocked actions run again"); ax[k].legend(fontsize=8, loc="lower right")
    x = np.arange(len(MECH)); wdt = 0.38
    for j, arm in enumerate(("APT", "baseline")):
        ax[2].bar(x + (j - 0.5) * wdt, [out["cells"][f"{arm}|{m}"]["median_resume"] for m in MECH], wdt, color=col[arm], label=arm)
        ax[2].axhline(out["cells"][f"{arm}|none"]["median_gap"], color=col[arm], ls="--", lw=1)
    ax[2].set_xticks(x); ax[2].set_xticklabels([m.replace("_", "\n") for m in MECH], fontsize=8)
    ax[2].set_ylabel("median time to resume a blocked action (s)"); ax[2].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(sys.argv[2], dpi=110)
