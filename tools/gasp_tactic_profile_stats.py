"""The four L2 attack profiles at tactic-to-tactic resolution — verified statistics
under the size-matched (label-shuffle) null.

Why: Marc's rulings of 2026-08-17 — (i) the L2 unit speaks at tactic-to-tactic
resolution, the structure L3 quotients into transitions; (ii) the null the
discrimination claim stands on is the size-matched label shuffle (the strict
one; the null divergence.py already uses at L3), not the L2 gate's half-split.
This tool is an INDEPENDENT re-derivation (own code, not importing
tools/gasp_tactic_restatement.py) that verifies that record's numbers and then
produces the profile statistics the dissertation's L2 unit carries.

Run from the repo root:  PYTHONPATH=src python tools/gasp_tactic_profile_stats.py
Inputs: data/gap/gap_v0.5.json, data/gasp/classification.csv, the operator
dedup rule in mtdsim.l2_subgraph.dedup. Deterministic (seeded).
Record: docs/implementation/pipeline/gasp/tactic_profile_statistics.md

Pooling conventions (each is a choice the handoff asked to be stated):
  * tactic of a technique   = GAP ``primary_tactic`` (the L1 convention;
                              the all-tactics alternative is reported as a
                              sensitivity column for the read-offs)
  * transition              = ordered pair of DIFFERENT primary tactics joined
                              by at least one GAP edge (intra-tactic edges
                              dropped, as L3 build.py drops them)
  * transition share (PRIMARY, "flow-presence") = distinct flows drawing the
                              pair, normalised over all pairs — the count L3's
                              W-A layer is built from (divergence.py
                              quotient_out_dists), so it is the profile.
  * transition share (sensitivity, "edge-occurrence") = (flow, technique-edge)
                              occurrences pooled to the pair — the restatement
                              tool's convention.
  * JSD = scipy jensenshannon(p, q, base 2) ** 2, in [0, 1] (L2 gate / L3).
"""
from __future__ import annotations

import csv
import itertools
import json
import sys
from collections import Counter, defaultdict

import numpy as np
from scipy.spatial.distance import jensenshannon

sys.path.insert(0, "src")
from mtdsim.l2_subgraph.dedup import operator_deduplicated_flows  # noqa: E402

GAP_PATH = "data/gap/gap_v0.5.json"
CLS_PATH = "data/gasp/classification.csv"
CLASSES = [
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
]
SHORT = {c: c.replace("objective_", "") for c in CLASSES}
OBJECTIVE_TACTICS = {"exfiltration", "impact"}
NULL_TRIALS = 2000
NULL_SEED = 20260528  # mirrors the L2 gate
PERM_SEED = 1         # mirrors the restatement's per-pair permutations
HALF_SPLIT_TRIALS = 200  # the gate's calibration, reproduced once for the diff

# --------------------------------------------------------------------------- data

gap = json.load(open(GAP_PATH))
cls_of = {r["flow_id"]: r["class_name"] for r in csv.DictReader(open(CLS_PATH))}
ALL_FLOWS = sorted(cls_of)
DEDUP_FLOWS = sorted(operator_deduplicated_flows())
assert len(ALL_FLOWS) == 38 and len(DEDUP_FLOWS) == 29

primary = {t: n["primary_tactic"] for t, n in gap["nodes"].items()}
all_tactics_of = {t: list(n["tactics"]) for t, n in gap["nodes"].items()}
TACTICS = sorted(set(primary.values()))

# per-flow: technique set; multiset of technique-edges as tactic pairs; set of pairs
flow_techs: dict[str, set[str]] = defaultdict(set)
for t, n in gap["nodes"].items():
    for f in n["flow_ids"]:
        flow_techs[f].add(t)
flow_pair_occ: dict[str, Counter] = defaultdict(Counter)   # (flow) -> Counter{pair: k}
n_intra = 0
for e in gap["edges"]:
    a, b = primary[e["source_id"]], primary[e["target_id"]]
    if a == b:
        n_intra += 1
        continue
    for f in e["flow_ids"]:
        flow_pair_occ[f][(a, b)] += 1
PAIRS = sorted({p for c in flow_pair_occ.values() for p in c})
PIDX = {p: i for i, p in enumerate(PAIRS)}
TIDX = {t: i for i, t in enumerate(TACTICS)}
TECHS = sorted(gap["nodes"])
XIDX = {t: i for i, t in enumerate(TECHS)}


def by_class(flows):
    return {c: [f for f in flows if cls_of[f] == c] for c in CLASSES}


def norm(v):
    s = v.sum()
    return v / s if s else v


# ------------------------------------------------------------------ distributions

def tactic_set(flows):
    return {primary[t] for f in flows for t in flow_techs[f]}


def pair_set(flows):
    return {p for f in flows for p in flow_pair_occ[f]}


def tactic_share(flows, pooling="primary"):
    v = np.zeros(len(TACTICS))
    for f in flows:
        for t in flow_techs[f]:
            if pooling == "primary":
                v[TIDX[primary[t]]] += 1
            else:  # all tactics of the technique, each credited 1
                for tac in all_tactics_of[t]:
                    v[TIDX[tac]] += 1
    return norm(v)


def transition_share(flows, pooling="presence"):
    v = np.zeros(len(PAIRS))
    if pooling == "presence":
        for f in flows:
            for p in flow_pair_occ[f]:
                v[PIDX[p]] += 1
    else:  # edge-occurrence
        for f in flows:
            for p, k in flow_pair_occ[f].items():
                v[PIDX[p]] += k
    return norm(v)


def technique_dist(flows):
    v = np.zeros(len(TECHS))
    fs = set(flows)
    for t in TECHS:
        v[XIDX[t]] = len(set(gap["nodes"][t]["flow_ids"]) & fs)
    return norm(v)


def jsd(p, q):
    return float(jensenshannon(p, q, base=2) ** 2)


def jaccard(a, b):
    return len(a & b) / len(a | b)


def mean_pairwise(dist_fn, groups):
    return float(np.mean([jsd(dist_fn(a), dist_fn(b)) for a, b in itertools.combinations(groups, 2)]))


def size_matched_null(dist_fn, flows, sizes, n=NULL_TRIALS, seed=NULL_SEED):
    """Mean pairwise JSD over `n` random relabellings with class sizes preserved."""
    rng = np.random.default_rng(seed)
    pool = list(flows)
    out = np.empty(n)
    for i in range(n):
        rng.shuffle(pool)
        groups, cur = [], 0
        for s in sizes:
            groups.append(pool[cur:cur + s]); cur += s
        out[i] = mean_pairwise(dist_fn, groups)
    return out


def half_split_null(dist_fn, flows, n=HALF_SPLIT_TRIALS, seed=NULL_SEED):
    rng = np.random.default_rng(seed)
    pool = list(flows); h = len(pool) // 2
    out = np.empty(n)
    for i in range(n):
        rng.shuffle(pool)
        out[i] = jsd(dist_fn(pool[:h]), dist_fn(pool[h:]))
    return out


def perm_p(dist_fn, a, b, n=NULL_TRIALS, seed=PERM_SEED):
    """Two-class permutation p: fraction of relabellings with JSD >= observed."""
    obs = jsd(dist_fn(a), dist_fn(b))
    rng = np.random.default_rng(seed)
    pool = list(a) + list(b); na = len(a); cnt = 0
    for _ in range(n):
        rng.shuffle(pool)
        cnt += jsd(dist_fn(pool[:na]), dist_fn(pool[na:])) >= obs
    return obs, cnt / n


def jsd_contributions(p, q):
    """Per-component contribution to JSD (base 2); sums to jsd(p, q)."""
    m = 0.5 * (p + q)
    with np.errstate(divide="ignore", invalid="ignore"):
        cp = np.where(p > 0, 0.5 * p * np.log2(p / m), 0.0)
        cq = np.where(q > 0, 0.5 * q * np.log2(q / m), 0.0)
    return cp + cq


def strip_objective(dist_fn):
    """Same distribution restricted to pairs touching no objective tactic."""
    keep = np.array([not ({a, b} & OBJECTIVE_TACTICS) for a, b in PAIRS])

    def f(flows):
        return norm(dist_fn(flows) * keep)
    return f


def fmt_p(p):
    return f"p={p:.3f}" + (" *" if p < 0.05 else "")


# ============================================================================ run

def section(title):
    print(f"\n{'=' * 78}\n{title}\n{'=' * 78}")


section("0. Corpus and quotient")
print(f"flows {len(ALL_FLOWS)} (dedup {len(DEDUP_FLOWS)}); techniques {len(TECHS)}; "
      f"tactics {len(TACTICS)}; GAP edges {len(gap['edges'])} of which intra-tactic (dropped) {n_intra}; "
      f"inter-tactic transitions {len(PAIRS)}")
print(f"multi-tactic techniques: {sum(len(v) > 1 for v in all_tactics_of.values())} of {len(TECHS)}")

for label, flows in (("full corpus n=38", ALL_FLOWS), ("operator-deduplicated n=29", DEDUP_FLOWS)):
    c2f = by_class(flows)
    sizes = [len(c2f[c]) for c in CLASSES]

    section(f"1. Structure — {label}  sizes {dict(zip([SHORT[c] for c in CLASSES], sizes))}")
    tsets = {c: tactic_set(v) for c, v in c2f.items()}
    psets = {c: pair_set(v) for c, v in c2f.items()}
    print("tactic places per class:      ", {SHORT[c]: len(tsets[c]) for c in CLASSES}, "of", len(TACTICS))
    print("inter-tactic transitions:     ", {SHORT[c]: len(psets[c]) for c in CLASSES}, "of", len(PAIRS))
    core_t = set.intersection(*tsets.values()); core_p = set.intersection(*psets.values())
    print(f"in all four classes: tactics {len(core_t)}  transitions {len(core_p)}")
    print("  missing tactics per class:", {SHORT[c]: sorted(set(TACTICS) - tsets[c]) for c in CLASSES})
    print("  common transitions:", sorted(core_p))
    uniq = {c: sorted(psets[c] - set.union(*(psets[d] for d in CLASSES if d != c))) for c in CLASSES}
    print("  transitions unique to one class:", {SHORT[c]: len(uniq[c]) for c in CLASSES})
    for c in CLASSES:
        print(f"    {SHORT[c]}: {uniq[c]}")
    print("pairwise Jaccard (tactic sets / transition sets):")
    for a, b in itertools.combinations(CLASSES, 2):
        print(f"  {SHORT[a]:>20} vs {SHORT[b]:<20}  {jaccard(tsets[a], tsets[b]):.3f}   {jaccard(psets[a], psets[b]):.3f}")
    # Is the transition-set overlap any lower than a size-matched relabelling gives?
    obs_j = float(np.mean([jaccard(psets[a], psets[b]) for a, b in itertools.combinations(CLASSES, 2)]))
    rng = np.random.default_rng(NULL_SEED); pool = list(flows); nj = np.empty(NULL_TRIALS)
    for i in range(NULL_TRIALS):
        rng.shuffle(pool); cur = 0; gs = []
        for sz in sizes:
            gs.append(pair_set(pool[cur:cur + sz])); cur += sz
        nj[i] = np.mean([jaccard(x, y) for x, y in itertools.combinations(gs, 2)])
    print(f"mean transition-set Jaccard: observed {obs_j:.3f}; size-matched null p5/p50/p95 "
          f"{np.percentile(nj, 5):.3f}/{np.percentile(nj, 50):.3f}/{np.percentile(nj, 95):.3f}; "
          f"p(null <= observed) = {np.mean(nj <= obs_j):.3f}")

    section(f"2. Tactic-share table (% of (flow,technique) occurrences, primary_tactic) — {label}")
    ts = {c: tactic_share(v) for c, v in c2f.items()}
    ts_all = {c: tactic_share(v, "all") for c, v in c2f.items()}
    print("  tactic".ljust(26) + "".join(SHORT[c][:12].rjust(13) for c in CLASSES) + "   | all-tactics pooling")
    for t in TACTICS:
        row = "".join(f"{100 * ts[c][TIDX[t]]:13.1f}" for c in CLASSES)
        alt = " ".join(f"{100 * ts_all[c][TIDX[t]]:5.1f}" for c in CLASSES)
        print(f"  {t:<24}{row}   | {alt}")

    section(f"3. Transition-share profiles (flow-presence pooling = L3 W-A count) — {label}")
    tp = {c: transition_share(v) for c, v in c2f.items()}
    for c in CLASSES:
        v = tp[c]; order = np.argsort(-v)
        top = [(f"{a}→{b}", round(float(100 * v[i]), 1)) for i in order[:8] for a, b in [PAIRS[i]]]
        into_obj = {o: round(float(100 * sum(v[PIDX[p]] for p in PAIRS if p[1] == o)), 1) for o in sorted(OBJECTIVE_TACTICS)}
        feeders = {o: sorted({p[0] for p in psets[c] if p[1] == o}) for o in sorted(OBJECTIVE_TACTICS)}
        support = Counter()
        for f in c2f[c]:
            for pr in flow_pair_occ[f]:
                support[pr] += 1
        single = sum(1 for k in support.values() if k == 1)
        print(f"  {SHORT[c]} (n={len(c2f[c])}, {len(psets[c])} transitions; "
              f"{single} of them ({100 * single / len(psets[c]):.0f}%) backed by a single flow; "
              f"median flows per transition {int(np.median(list(support.values())))}, max {max(support.values())}):")
        print(f"    top transitions (% of flow-presence mass): {top}")
        print(f"    mass into objective tactics: {into_obj}; feeders: {feeders}")

    section(f"4. Separation — mean pairwise JSD vs nulls — {label}")
    print(f"size-matched null: {NULL_TRIALS} relabellings, seed {NULL_SEED}; half-split: {HALF_SPLIT_TRIALS} trials (gate calibration, for the diff only)")
    stats = [
        ("technique", technique_dist),
        ("tactic share (primary)", tactic_share),
        ("transition share (flow-presence) [PRIMARY]", lambda fl: transition_share(fl, "presence")),
        ("transition share (edge-occurrence)", lambda fl: transition_share(fl, "occurrence")),
        ("transition share, objective tactics stripped", strip_objective(lambda fl: transition_share(fl, "presence"))),
    ]
    print(f"  {'statistic':<46}{'observed':>9}{'null p50':>9}{'null p95':>9}{'p (perm)':>10}{'half p95':>10}")
    for name, fn in stats:
        obs = mean_pairwise(fn, [c2f[c] for c in CLASSES])
        null = size_matched_null(fn, flows, sizes)
        p = float(np.mean(null >= obs))
        hs = half_split_null(fn, flows)
        print(f"  {name:<46}{obs:9.3f}{np.percentile(null, 50):9.3f}{np.percentile(null, 95):9.3f}{p:10.3f}{np.percentile(hs, 95):10.3f}")

    section(f"5. Per-pair permutation tests ({NULL_TRIALS} relabellings, seed {PERM_SEED}) — {label}")
    print(f"  {'pair':<44}{'transition (presence)':>24}{'transition (occurrence)':>26}{'obj-stripped':>18}{'tactic share':>18}{'technique':>18}")
    fns = [lambda fl: transition_share(fl, "presence"), lambda fl: transition_share(fl, "occurrence"),
           strip_objective(lambda fl: transition_share(fl, "presence")), tactic_share, technique_dist]
    for a, b in itertools.combinations(CLASSES, 2):
        cells = []
        for fn in fns:
            o, p = perm_p(fn, c2f[a], c2f[b])
            cells.append(f"{o:.3f} {fmt_p(p):>10}")
        print(f"  {SHORT[a]:>20} vs {SHORT[b]:<20}" + "".join(f"{x:>24}" if i == 0 else f"{x:>26}" if i == 1 else f"{x:>18}" for i, x in enumerate(cells)))

    section(f"6. What carries the transition-share divergence — top contributing transitions per pair — {label}")
    for a, b in itertools.combinations(CLASSES, 2):
        p, q = tp[a], tp[b]
        contrib = jsd_contributions(p, q); tot = contrib.sum()
        order = np.argsort(-contrib)[:6]
        obj_share = contrib[[i for i, pr in enumerate(PAIRS) if set(pr) & OBJECTIVE_TACTICS]].sum() / tot
        items = [f"{PAIRS[i][0]}→{PAIRS[i][1]} {100 * contrib[i] / tot:.0f}%" for i in order]
        print(f"  {SHORT[a]} vs {SHORT[b]} (JSD {tot:.3f}; {100 * obj_share:.0f}% of it on objective-tactic transitions): {items}")

section("7. Same-operator-same-class check (Marc's 2026-08-17 reframe)")
from mtdsim.l2_subgraph.dedup import OPERATOR_CLUSTERS  # noqa: E402
for name, members in OPERATOR_CLUSTERS.items():
    print(f"  {name:<16} {[SHORT[cls_of[m]] for m in members]}")


# ============================================================================
# 8. The "what next" test (Marc, 2026-08-17): the profiles are weighted directed
#    graphs whose weights are PER-PLACE out-transition proportions. Does the
#    conditional P(next tactic | current tactic) differ by class beyond a
#    size-matched relabelling? Two statistics, both permutation-tested:
#      (a) mean per-place JSD between the two classes' out-distributions over
#          comparable places (the L3 divergence.py form, but class-vs-class);
#      (b) the deviance (G) of the class-conditional transition model against
#          the pooled model — a likelihood-ratio statistic that weights each
#          place by its support instead of averaging sparse places equally.
# ============================================================================

def out_counts(flows):
    """place -> {target: number of distinct flows drawing place->target}."""
    c: dict[str, Counter] = defaultdict(Counter)
    for f in flows:
        for (a, b) in flow_pair_occ[f]:
            c[a][b] += 1
    return c


def out_dists(flows):
    return {p: {t: n / sum(d.values()) for t, n in d.items()} for p, d in out_counts(flows).items()}


def dict_jsd(d1, d2):
    keys = sorted(set(d1) | set(d2))
    p = np.array([d1.get(k, 0.0) for k in keys]); q = np.array([d2.get(k, 0.0) for k in keys])
    return jsd(p, q)


def per_place_jsd_pair(a, b, weighted=False):
    da, db = out_dists(a), out_dists(b)
    ca, cb = out_counts(a), out_counts(b)
    places = sorted(set(da) & set(db))
    if not places:
        return 0.0
    vals = np.array([dict_jsd(da[p], db[p]) for p in places])
    if not weighted:
        return float(vals.mean())
    w = np.array([sum(ca[p].values()) + sum(cb[p].values()) for p in places], float)
    return float((vals * w).sum() / w.sum())


def deviance(groups):
    """G = 2 * sum_c sum_p sum_t n_c(p,t) * ln( P_c(t|p) / P_pool(t|p) )."""
    pooled = out_counts([f for g in groups for f in g])
    pooled_p = {p: {t: n / sum(d.values()) for t, n in d.items()} for p, d in pooled.items()}
    g = 0.0
    for grp in groups:
        cg = out_counts(grp)
        for p, d in cg.items():
            tot = sum(d.values())
            for t, n in d.items():
                g += 2 * n * np.log((n / tot) / pooled_p[p][t])
    return float(g)


def deviance_by_place(groups):
    pooled = out_counts([f for g in groups for f in g])
    pooled_p = {p: {t: n / sum(d.values()) for t, n in d.items()} for p, d in pooled.items()}
    out = Counter()
    for grp in groups:
        cg = out_counts(grp)
        for p, d in cg.items():
            tot = sum(d.values())
            for t, n in d.items():
                out[p] += 2 * n * np.log((n / tot) / pooled_p[p][t])
    return out


def relabel(rng, pool, sizes):
    rng.shuffle(pool); cur = 0; gs = []
    for s in sizes:
        gs.append(pool[cur:cur + s]); cur += s
    return gs


for label, flows in (("full corpus n=38", ALL_FLOWS), ("operator-deduplicated n=29", DEDUP_FLOWS)):
    c2f = by_class(flows); groups = [c2f[c] for c in CLASSES]; sizes = [len(g) for g in groups]
    section(f"8. WHAT-NEXT: per-place out-distribution divergence — {label}")

    # (a) mean pairwise per-place JSD, unweighted and support-weighted, 4-group null
    for weighted in (False, True):
        fn = lambda gs: float(np.mean([per_place_jsd_pair(x, y, weighted) for x, y in itertools.combinations(gs, 2)]))
        obs = fn(groups)
        rng = np.random.default_rng(NULL_SEED); pool = list(flows)
        null = np.array([fn(relabel(rng, pool, sizes)) for _ in range(NULL_TRIALS)])
        print(f"  mean pairwise per-place JSD ({'support-weighted' if weighted else 'unweighted'}): "
              f"observed {obs:.3f}; null p50 {np.percentile(null, 50):.3f} p95 {np.percentile(null, 95):.3f}; "
              f"p = {np.mean(null >= obs):.3f}")

    # (b) deviance of class-conditional model vs pooled
    obs_g = deviance(groups)
    rng = np.random.default_rng(NULL_SEED); pool = list(flows)
    null_g = np.array([deviance(relabel(rng, pool, sizes)) for _ in range(NULL_TRIALS)])
    print(f"  deviance G (class-conditional next-tactic model vs pooled): observed {obs_g:.1f}; "
          f"null p50 {np.percentile(null_g, 50):.1f} p95 {np.percentile(null_g, 95):.1f}; p = {np.mean(null_g >= obs_g):.3f}")

    # (b') per-place deviance and per-place permutation p
    obs_pl = deviance_by_place(groups)
    rng = np.random.default_rng(NULL_SEED); pool = list(flows)
    null_pl = defaultdict(list)
    for _ in range(NULL_TRIALS):
        d = deviance_by_place(relabel(rng, pool, sizes))
        for p in TACTICS:
            null_pl[p].append(d.get(p, 0.0))
    print("  per-place deviance (which 'what next' distributions differ by class):")
    print(f"    {'place':<24}{'G_obs':>8}{'null p95':>10}{'p':>8}   out-transitions by class (flow-presence counts)")
    for p in TACTICS:
        pv = float(np.mean(np.array(null_pl[p]) >= obs_pl.get(p, 0.0)))
        oc = [out_counts(g).get(p, {}) for g in groups]
        summ = " | ".join(",".join(f"{t[:5]}:{n}" for t, n in sorted(c.items(), key=lambda kv: -kv[1])[:4]) or "—" for c in oc)
        print(f"    {p:<24}{obs_pl.get(p, 0.0):8.1f}{np.percentile(null_pl[p], 95):10.1f}{pv:8.3f}{'  *' if pv < .05 else '   '}  {summ}")

    # (c) per-pair permutation on the per-place statistics
    print("  per-pair permutation (unweighted per-place JSD / support-weighted / pairwise deviance):")
    for a, b in itertools.combinations(CLASSES, 2):
        cells = []
        for fn in (lambda x, y: per_place_jsd_pair(x, y, False), lambda x, y: per_place_jsd_pair(x, y, True), lambda x, y: deviance([x, y])):
            obs = fn(c2f[a], c2f[b]); rng = np.random.default_rng(PERM_SEED); pool = c2f[a] + c2f[b]; na = len(c2f[a]); cnt = 0
            for _ in range(NULL_TRIALS):
                rng.shuffle(pool); cnt += fn(pool[:na], pool[na:]) >= obs
            cells.append(f"{obs:.3f} ({fmt_p(cnt / NULL_TRIALS)})")
        print(f"    {SHORT[a]:>20} vs {SHORT[b]:<20}  " + "   ".join(f"{c:>20}" for c in cells))


# 8d. Is the exfiltration-vs-impact "what next" difference more than the objective
#     tactic appearing as a target? Deviance with objective-tactic transitions removed.
def deviance_stripped(groups):
    def oc(flows):
        c: dict[str, Counter] = defaultdict(Counter)
        for f in flows:
            for (a, b) in flow_pair_occ[f]:
                if not ({a, b} & OBJECTIVE_TACTICS):
                    c[a][b] += 1
        return c
    pooled = oc([f for g in groups for f in g])
    pooled_p = {p: {t: n / sum(d.values()) for t, n in d.items()} for p, d in pooled.items()}
    g = 0.0
    for grp in groups:
        for p, d in oc(grp).items():
            tot = sum(d.values())
            for t, n in d.items():
                g += 2 * n * np.log((n / tot) / pooled_p[p][t])
    return float(g)


for label, flows in (("full corpus n=38", ALL_FLOWS), ("operator-deduplicated n=29", DEDUP_FLOWS)):
    c2f = by_class(flows); groups = [c2f[c] for c in CLASSES]; sizes = [len(g) for g in groups]
    section(f"8d. WHAT-NEXT with objective-tactic transitions stripped — {label}")
    obs = deviance_stripped(groups); rng = np.random.default_rng(NULL_SEED); pool = list(flows)
    null = np.array([deviance_stripped(relabel(rng, pool, sizes)) for _ in range(NULL_TRIALS)])
    print(f"  4-class deviance, stripped: observed {obs:.1f}; null p50 {np.percentile(null, 50):.1f} p95 {np.percentile(null, 95):.1f}; p = {np.mean(null >= obs):.3f}")
    a, b = c2f["objective_exfiltration"], c2f["objective_impact"]
    obs = deviance_stripped([a, b]); rng = np.random.default_rng(PERM_SEED); pool = a + b; na = len(a); cnt = 0
    for _ in range(NULL_TRIALS):
        rng.shuffle(pool); cnt += deviance_stripped([pool[:na], pool[na:]]) >= obs
    print(f"  exfiltration vs impact deviance, stripped: observed {obs:.1f}; p = {cnt / NULL_TRIALS:.3f}")
