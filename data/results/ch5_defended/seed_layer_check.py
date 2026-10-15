"""Layer order with seeds as the resampling unit (read-only; 2026-10-15).

Section 6.5's statistics threat: the reduction intervals of Table D.3 resample
runs, so they treat the four attack profiles' runs on one seed's network as
independent. Here the seed is the unit: per seed, hosts compromised are
averaged over the APT attacker model's four attack profiles and over each
layer's three MTD mechanisms; seeds are resampled (paired across conditions)
and the host-minus-service difference in NCR reduction gets a 95 % percentile
interval. Run from the repo root: PYTHONPATH=src python3 data/results/ch5_defended/seed_layer_check.py
Output: seed_layer_check.log (printed lines) and seed_layer_check_numbers.json."""
import os, sys, pickle, json
from collections import defaultdict
import numpy as np
os.environ["CORPUS"] = "reported"
sys.path.insert(0, "data/results/ch5_defended")
import analyse as A
cells, _ = pickle.load(open("data/results/ch5_defended/runs_reported_summaries.pkl", "rb"))
rng = np.random.default_rng(20261015)
B = 2000
host = [c for c in A.SINGLES if A.LAYER_WORD.get(A.LAYER[c]) == "host"]
serv = [c for c in A.SINGLES if A.LAYER_WORD.get(A.LAYER[c]) == "service"]
print("host", host, "service", serv)
def runs(arm, c, i):
    return A._pool(cells, "core", A.FOUR, c, i) if arm == "movement" else A._cell(cells, "core", "baseline", "baseline", c, i)
def seedmeans(rs):
    by = defaultdict(list)
    for r in rs: by[r["seed"]].append(float(r["hosts"]))
    return by
out = {}
for arm in ("movement", "baseline"):
    none = seedmeans(runs(arm, "none", 0))
    for i in A.sweep_intervals(cells):
        hb = [seedmeans(runs(arm, c, i)) for c in host]
        sb = [seedmeans(runs(arm, c, i)) for c in serv]
        seeds = sorted(set(none) & set.intersection(*[set(d) for d in hb + sb]))
        S = np.array(seeds)
        N = np.array([np.mean(none[s]) for s in S])
        H = np.array([[np.mean(d[s]) for s in S] for d in hb]).mean(0)
        V = np.array([[np.mean(d[s]) for s in S] for d in sb]).mean(0)
        def red(idx):
            n = N[idx].mean(); return 1 - H[idx].mean()/n, 1 - V[idx].mean()/n
        ph, pv = red(np.arange(len(S)))
        bh, bv = np.empty(B), np.empty(B)
        for b in range(B):
            idx = rng.integers(0, len(S), len(S)); bh[b], bv[b] = red(idx)
        d = bh - bv
        out[f"{arm}|{i}"] = {"seeds": len(S), "host": ph, "service": pv, "diff": ph - pv, "diff_lo": float(np.quantile(d, .025)), "diff_hi": float(np.quantile(d, .975))}
        print(f"{arm:9s} {i:5d}s seeds={len(S)} host={ph:.3f}[{np.quantile(bh,.025):.3f},{np.quantile(bh,.975):.3f}] "
              f"service={pv:.3f}[{np.quantile(bv,.025):.3f},{np.quantile(bv,.975):.3f}] "
              f"diff={ph-pv:+.3f}[{np.quantile(d,.025):+.3f},{np.quantile(d,.975):+.3f}]")
json.dump(out, open("data/results/ch5_defended/seed_layer_check_numbers.json", "w"), indent=1)
