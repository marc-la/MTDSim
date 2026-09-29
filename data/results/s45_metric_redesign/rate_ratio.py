"""Dry run: compromise rate in W s after each deployment over the rate in the W s
before, pooled per cell (ratio of counts to live seconds); same moments on the
no-defence run; time lost = W * (ratio_none - ratio_mtd)."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, "data/results/ch5_defended")
import disruption as D
runs = D.load({2000})
none = {(r["arm"], r["profile"], r["seed"]): r for r in runs if r["cond"] == "none"}
W = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0  # the half interval at 2 000 s
def sums(r, src):
    c, T = src["comp"], src["T"]; out = np.zeros(4)  # pre_n, pre_s, post_n, post_s
    for t in r["landings"]:
        if t >= T or t - W < 0: continue
        for k, (lo, hi) in enumerate(((t - W, t), (t, min(t + W, T)))):
            out[2*k] += np.searchsorted(c, hi, "right") - np.searchsorted(c, lo, "right")
            out[2*k+1] += hi - lo
    return out
iv = 2000
print(f"W = {W:.0f} s each side, interval {iv}")
print(f"{'':28s} {'rate before /h':>14s} {'ratio MTD':>9s} {'ratio none':>10s} {'time lost s':>11s}")
for arm in ("movement", "baseline"):
    for m in D.MECHANISMS:
        rs = [r for r in runs if r["arm"] == arm and r["cond"] == m and r["interval"] == iv]
        a = sum(sums(r, r) for r in rs); b = sum(sums(r, none[(r["arm"], r["profile"], r["seed"])]) for r in rs)
        ra = (a[2]/a[3])/(a[0]/a[1]); rb = (b[2]/b[3])/(b[0]/b[1])
        print(f"{arm:9s} {m:18s} {3600*a[0]/a[1]:14.2f} {ra:9.2f} {rb:10.2f} {W*(rb-ra):11.0f}")
