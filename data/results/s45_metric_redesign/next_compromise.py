"""Dry run: time from each MTD deployment's completion to the attacker's next
compromised host, censored at the next deployment or the run's end; the same
from the same moments on the same seed's no-defence run."""
import sys
import numpy as np
sys.path.insert(0, "data/results/ch5_defended")
import disruption as D

runs = D.load({2000, 200})
none = {(r["arm"], r["profile"], r["seed"]): r for r in runs if r["cond"] == "none"}

def waits(r, src):
    out = []  # (wait, observed)
    L = r["landings"]
    for i, t in enumerate(L):
        if t >= src["T"]:
            continue
        stop = min(L[i + 1] if i + 1 < len(L) else np.inf, src["T"])
        c = src["comp"]
        j = np.searchsorted(c, t, "right")
        if j < len(c) and c[j] <= stop:
            out.append((c[j] - t, True))
        else:
            out.append((stop - t, False))
    return out

def summ(ws, window):
    w = np.array([x for x, _ in ws]); o = np.array([y for _, y in ws])
    n = len(w)
    # median: censored waits sort as "longer than any observed"
    key = np.where(o, w, np.inf)
    med = np.median(key) if n else np.nan
    within = o.mean() if n else np.nan
    # restricted mean, capped at the window
    rm = np.minimum(np.where(o, w, window), window).mean() if n else np.nan
    return n, med, within, rm

for iv in (2000,):
    print(f"\n=== interval {iv} s ===   median wait (s) | share followed by a compromise before next deployment | restricted mean")
    for arm in ("movement", "baseline"):
        for m in D.MECHANISMS:
            rs = [r for r in runs if r["arm"] == arm and r["cond"] == m and r["interval"] == iv]
            wd = [w for r in rs for w in waits(r, r)]
            wp = [w for r in rs for w in waits(r, none[(r["arm"], r["profile"], r["seed"])])]
            a, b = summ(wd, iv), summ(wp, iv)
            print(f"{arm:9s} {m:18s} n={a[0]:6d}  MTD: {a[1]:7.0f} {a[2]*100:5.1f}% {a[3]:6.0f}   none: {b[1]:7.0f} {b[2]*100:5.1f}% {b[3]:6.0f}")
