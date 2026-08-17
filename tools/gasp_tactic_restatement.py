"""Restate the L2 objective-partition findings at TACTIC resolution.

Why: the dissertation presents the L1 graph at tactic granularity (§4.2.1),
while the recorded L2 findings (objective_partition_findings.md; the
tests/l2_subgraph JSD gate) are technique-level. This tool recomputes the
structural and distributional findings at tactic resolution so the L2 unit
can speak in the same units as L0–L1, and adds a size-matched label-shuffle
null (the null divergence.py uses at L3) beside the L2 gate's half-split null.

Run from the repo root:  PYTHONPATH=src python tools/gasp_tactic_restatement.py
Inputs: data/gap/gap_v0.5.json, data/gasp/classification.csv, the operator
dedup rule in mtdsim.l2_subgraph.dedup. Deterministic (seeded).
Record: docs/implementation/pipeline/gasp/tactic_resolution_restatement.md
"""
import json, csv, itertools, sys
import numpy as np
from scipy.spatial.distance import jensenshannon
sys.path.insert(0,'src')
from mtdsim.l2_subgraph.dedup import operator_deduplicated_flows

gap=json.load(open('data/gap/gap_v0.5.json'))
cls={r['flow_id']:r['class_name'] for r in csv.DictReader(open('data/gasp/classification.csv'))}
CLASSES=['objective_exfiltration','objective_impact','objective_exfiltration_impact','objective_none_c2']
tac_of={t:n['primary_tactic'] for t,n in gap['nodes'].items()}
TACTICS=sorted(set(tac_of.values()))
# per-flow technique sets and inter-tactic edge multisets
flow_tech={}
for t,n in gap['nodes'].items():
    for f in n['flow_ids']: flow_tech.setdefault(f,set()).add(t)
flow_pairs={}
for e in gap['edges']:
    a,b=tac_of[e['source_id']],tac_of[e['target_id']]
    for f in e['flow_ids']:
        flow_pairs.setdefault(f,[]).append((a,b))
PAIRS=sorted({p for ps in flow_pairs.values() for p in ps if p[0]!=p[1]})

def tactic_share(flows):  # (flow,technique) occurrences -> primary tactic; row-normalised
    c=np.zeros(len(TACTICS))
    for f in flows:
        for t in flow_tech.get(f,()): c[TACTICS.index(tac_of[t])]+=1
    return c/c.sum() if c.sum() else c
def pair_share(flows):  # (flow, inter-tactic edge) occurrences per tactic pair
    c=np.zeros(len(PAIRS))
    for f in flows:
        for p in flow_pairs.get(f,()):
            if p[0]!=p[1]: c[PAIRS.index(p)]+=1
    return c/c.sum() if c.sum() else c
def tactic_set(flows): return {tac_of[t] for f in flows for t in flow_tech.get(f,())}
def pair_set(flows): return {p for f in flows for p in flow_pairs.get(f,()) if p[0]!=p[1]}
def jsd(p,q): return float(jensenshannon(p,q)**2)
def jac(a,b): return len(a&b)/len(a|b)

def report(flows_all, label):
    c2f={c:[f for f in flows_all if cls[f]==c] for c in CLASSES}
    print(f"\n=== {label} (n={len(flows_all)}) ===")
    print("class sizes:", {c:len(v) for c,v in c2f.items()})
    print("tactic places per class:", {c:len(tactic_set(v)) for c,v in c2f.items()}, "of", len(TACTICS))
    print("inter-tactic transitions per class:", {c:len(pair_set(v)) for c,v in c2f.items()}, "of", len(PAIRS))
    print("tactics in ALL four:", len(set.intersection(*[tactic_set(v) for v in c2f.values()])), "; pairs in ALL four:", len(set.intersection(*[pair_set(v) for v in c2f.values()])))
    print("pairwise Jaccard, tactic sets:", [round(jac(tactic_set(c2f[a]),tactic_set(c2f[b])),3) for a,b in itertools.combinations(CLASSES,2)])
    print("pairwise Jaccard, transition sets:", [round(jac(pair_set(c2f[a]),pair_set(c2f[b])),3) for a,b in itertools.combinations(CLASSES,2)])
    ts={c:tactic_share(v) for c,v in c2f.items()}; ps={c:pair_share(v) for c,v in c2f.items()}
    print("tactic-share table (%):")
    print("  tactic".ljust(26)+"".join(c[10:][:12].rjust(13) for c in CLASSES))
    for i,t in enumerate(TACTICS):
        print(f"  {t:<24}"+"".join(f"{100*ts[c][i]:13.1f}" for c in CLASSES))
    for name,d in (("tactic-share",ts),("transition-share",ps)):
        pj=[jsd(d[a],d[b]) for a,b in itertools.combinations(CLASSES,2)]
        print(f"pairwise JSD {name}: mean {np.mean(pj):.4f} range {min(pj):.3f}-{max(pj):.3f}")
    # null: random half-splits, 200 trials, seed as gate
    rng=np.random.default_rng(seed=20260528); flows=sorted(flows_all); half=len(flows)//2
    nt=[];npair=[]
    for _ in range(200):
        rng.shuffle(flows); A,B=set(flows[:half]),set(flows[half:])
        nt.append(jsd(tactic_share(A),tactic_share(B))); npair.append(jsd(pair_share(A),pair_share(B)))
    print(f"null p95 half-split: tactic-share {np.percentile(nt,95):.4f}, transition-share {np.percentile(npair,95):.4f}")
    # size-preserving shuffled labels null (mean pairwise across 4 shuffled classes)
    rng=np.random.default_rng(seed=20260528); mt=[];mp=[]
    sizes=[len(c2f[c]) for c in CLASSES]
    for _ in range(200):
        rng.shuffle(flows); i=0; groups=[]
        for s in sizes: groups.append(set(flows[i:i+s])); i+=s
        mt.append(np.mean([jsd(tactic_share(a),tactic_share(b)) for a,b in itertools.combinations(groups,2)]))
        mp.append(np.mean([jsd(pair_share(a),pair_share(b)) for a,b in itertools.combinations(groups,2)]))
    print(f"null p95 size-matched label shuffle (mean pairwise): tactic-share {np.percentile(mt,95):.4f}, transition-share {np.percentile(mp,95):.4f}")

report(sorted(cls), "full corpus")
report(sorted(operator_deduplicated_flows()), "operator-deduplicated")

# --- technique-level, same two nulls, for apples-to-apples with the L2 gate ---
TIDS=sorted(gap['nodes'])
def tech_dist(flows):
    c=np.array([len(set(gap['nodes'][t]['flow_ids'])&set(flows)) for t in TIDS],float)
    return c/c.sum() if c.sum() else c
def tech_report(flows_all,label):
    c2f={c:[f for f in flows_all if cls[f]==c] for c in CLASSES}
    d={c:tech_dist(v) for c,v in c2f.items()}
    pj=[jsd(d[a],d[b]) for a,b in itertools.combinations(CLASSES,2)]
    rng=np.random.default_rng(seed=20260528); flows=sorted(flows_all); half=len(flows)//2; nh=[]
    for _ in range(200):
        rng.shuffle(flows); nh.append(jsd(tech_dist(flows[:half]),tech_dist(flows[half:])))
    rng=np.random.default_rng(seed=20260528); ms=[]; sizes=[len(c2f[c]) for c in CLASSES]
    for _ in range(200):
        rng.shuffle(flows); i=0; g=[]
        for s in sizes: g.append(flows[i:i+s]); i+=s
        ms.append(np.mean([jsd(tech_dist(a),tech_dist(b)) for a,b in itertools.combinations(g,2)]))
    print(f"\n[{label} n={len(flows_all)}] TECHNIQUE-level: mean pairwise JSD {np.mean(pj):.4f} (range {min(pj):.3f}-{max(pj):.3f}); null p95 half-split {np.percentile(nh,95):.4f}; null p95 size-matched shuffle {np.percentile(ms,95):.4f}")
tech_report(sorted(cls),"full"); tech_report(sorted(operator_deduplicated_flows()),"dedup")

# --- per-pair permutation p-values (size-matched, 1000 shuffles of the two classes' pooled flows) ---
def perpair(flows_all,label):
    c2f={c:[f for f in flows_all if cls[f]==c] for c in CLASSES}
    print(f"\n[{label} n={len(flows_all)}] per-pair permutation p (size-matched, 1000): technique / tactic-share / transition-share")
    for a,b in itertools.combinations(CLASSES,2):
        pool=c2f[a]+c2f[b]; na=len(c2f[a])
        rng=np.random.default_rng(1)
        obs=[jsd(tech_dist(c2f[a]),tech_dist(c2f[b])), jsd(tactic_share(c2f[a]),tactic_share(c2f[b])), jsd(pair_share(c2f[a]),pair_share(c2f[b]))]
        cnt=[0,0,0]
        for _ in range(1000):
            rng.shuffle(pool); A,B=pool[:na],pool[na:]
            s=[jsd(tech_dist(A),tech_dist(B)), jsd(tactic_share(A),tactic_share(B)), jsd(pair_share(A),pair_share(B))]
            for i in range(3): cnt[i]+= s[i]>=obs[i]
        print(f"  {a[10:]:>20} vs {b[10:]:<20}  " + "  ".join(f"{o:.3f} (p={c/1000:.3f})" for o,c in zip(obs,cnt)))
perpair(sorted(cls),"full"); perpair(sorted(operator_deduplicated_flows()),"dedup")
