"""Dry run: share of actions NOT flagged by a count-in-window alarm: an action is
flagged when it is at least the Nth action in the W s up to and including it."""
import sys
import numpy as np
sys.path.insert(0, "data/results/ch5_s531_unopposed"); sys.path.insert(0, "src")
import analyse as A
mov, base, _ = A.load()
CORE = A.CORE
def flags(starts, N, W):
    s = np.asarray(starts)
    if not len(s): return np.zeros(0, bool)
    cnt = np.arange(1, len(s) + 1) - np.searchsorted(s, s - W, "right")  # actions in (t-W, t]
    return cnt >= N
groups = {A.LABEL.get(p, p): [A._actions_movement(r)[0] for r in mov[("targeted", CORE, p)]] for p in A.FOUR}
groups["baseline"] = [A._actions_baseline(row)[0] for row in base[CORE]]
print(f"{'rule':22s}" + "".join(f"{k:>10s}" for k in groups))
for N, W in ((3, 60), (4, 60), (5, 60), (10, 60), (5, 90), (5, 600)):
    row = []
    for k, acts in groups.items():
        f = np.concatenate([flags(a, N, W) for a in acts])
        row.append(100 * (1 - f.mean()))
    print(f"N>={N:<3d} in {W:4d} s      " + "".join(f"{v:9.0f}%" for v in row))
# median gap between consecutive actions (Zhan's inter-arrival time)
print("median gap s ", "".join(f"{np.median(np.concatenate([np.diff(a) for a in acts if len(a)>1])):10.1f}" for acts in groups.values()))
