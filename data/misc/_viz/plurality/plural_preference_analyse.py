"""Plural-preference study — the analyser.

Reads pp_runs.jsonl (the three-arm run record) and computes, per profile per
dimension, the plurality signature and the strategic-content verdict:

  - D (effective number), evenness, support N — corpus vs uniform-null vs baseline,
    each with a bootstrap-over-seeds 95 % CI (the handoff's interval requirement:
    no "more concentrated" claim without disjoint intervals).
  - the CI-separation verdict (P1-strategic): is the corpus arm's evenness CI
    disjoint from the uniform null's, and which direction?
  - jsd(corpus, uniform) against the within-corpus split-half noise floor — the
    direction-agnostic magnitude of strategic content.
  - the field-success alignment (edge mass vs the corpus success prior), corpus vs
    uniform, with CIs — the step that makes preference strategic.
  - the substrate-success alignment (verb mass vs substrate success rate) — the
    committed honesty check (axis 7: substrate success is not a progress signal).
  - the plurality_reporting.md §2 reproduction on the overlapping seeds 0-9.

The maths is measures.py's (hill_diversity, jsd, spearman_rho, corpus_edge_weights);
this script only pools the persisted per-run counters and resamples seeds.

    PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_analyse.py
"""
from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path

from mtdsim.l3_simulation.movement import measures as M
from mtdsim.l3_simulation.movement.net import load_routing_net

HERE = Path(__file__).resolve().parent

# The 2026-08-06 objective-tactic rename (label-drift trap; plurality_reporting §7).
# This runner wrote current labels, but normalise defensively off the corpus.
RENAME = {
    "pure_steal": "objective_exfiltration",
    "pure_impediment": "objective_impact",
    "double_extortion": "objective_exfiltration_impact",
    "infrastructure_setup": "objective_none_c2",
    "aggregate": "aggregate",
}
PROFILES = (
    "objective_exfiltration", "objective_impact",
    "objective_exfiltration_impact", "objective_none_c2", "aggregate",
)
# The four dimensions whose distribution shape the convergence check certified
# stable at the seed budget; opening's shape is WITHHELD (support unsaturated at
# k=5, P3), so it carries variety (support count) only, not a preference verdict.
SHAPE_DIMENSIONS = ("transition", "verb", "visit", "terminal")
K = 5
N_BOOT = 2000
BOOT_SEED = 0
Q_LO, Q_HI = 2.5, 97.5


def load() -> list[dict]:
    rows = []
    for line in (HERE / "pp_runs.jsonl").read_text().splitlines():
        r = json.loads(line)
        if "error" in r:
            continue
        if r.get("profile") in RENAME:
            r["profile"] = RENAME[r["profile"]]
        rows.append(r)
    return rows


def sel(rows, **kw):
    return [r for r in rows if all(r.get(k) == v for k, v in kw.items())]


# -- pooling per dimension from persisted per-run counters --------------------


def dim_counter(run_rows, dimension: str) -> Counter:
    """Pooled behaviour counts for a dimension over a set of persisted run rows."""
    c: Counter = Counter()
    for r in run_rows:
        if dimension == "opening":
            c[tuple(r["sequence"][:K])] += 1
        elif dimension == "terminal":
            c[r["terminal"]] += 1
        elif dimension == "verb":
            c.update(r["verb_attempts"])
        elif dimension == "visit":
            c.update(r["visits"])
        elif dimension == "transition":
            c.update(r["edges"])
        else:
            raise ValueError(dimension)
    return c


def edge_mass(run_rows) -> dict[str, float]:
    c = dim_counter(run_rows, "transition")
    total = sum(c.values())
    return {e: n / total for e, n in c.items()} if total else {}


def percentile(xs, q):
    xs = sorted(xs)
    if not xs:
        return float("nan")
    idx = (q / 100.0) * (len(xs) - 1)
    lo = int(idx)
    frac = idx - lo
    if lo + 1 < len(xs):
        return xs[lo] * (1 - frac) + xs[lo + 1] * frac
    return xs[lo]


def bootstrap_ci(run_rows, statistic, *, n_boot=N_BOOT, seed=BOOT_SEED):
    """Percentile CI of a pooled ``statistic(run_rows)`` under resampling of the
    runs (== seeds; one run per seed per cell) with replacement."""
    point = statistic(run_rows)
    if not run_rows:
        return point, float("nan"), float("nan")
    rng = random.Random(seed)
    n = len(run_rows)
    draws = []
    for _ in range(n_boot):
        sample = [run_rows[rng.randrange(n)] for _ in range(n)]
        val = statistic(sample)
        if val == val:  # drop NaN draws (undefined statistic on a degenerate resample)
            draws.append(val)
    return point, percentile(draws, Q_LO), percentile(draws, Q_HI)


def evenness_of(dimension):
    return lambda rr: M.hill_diversity(dim_counter(rr, dimension)).evenness


def d_of(dimension):
    return lambda rr: M.hill_diversity(dim_counter(rr, dimension)).effective_number


def alignment_of(reference):
    def stat(rr):
        mass = edge_mass(rr)
        edges = sorted(reference)
        xs = [mass.get(e, 0.0) for e in edges]
        ys = [reference[e] for e in edges]
        return M.spearman_rho(xs, ys)
    return stat


def substrate_align(rr):
    attempts: Counter = Counter()
    successes: Counter = Counter()
    for r in rr:
        attempts.update(r["verb_attempts"])
        successes.update(r["verb_successes"])
    rates = {v: successes.get(v, 0) / n for v, n in attempts.items() if n}
    total = sum(attempts.values())
    if not total or not rates:
        return float("nan")
    verbs = sorted(rates)
    xs = [attempts.get(v, 0) / total for v in verbs]
    ys = [rates[v] for v in verbs]
    return M.spearman_rho(xs, ys)


def disjoint(ci_a, ci_b) -> bool:
    (_, a_lo, a_hi), (_, b_lo, b_hi) = ci_a, ci_b
    return a_hi < b_lo or b_hi < a_lo


def jsd_norm(counter_a: Counter, counter_b: Counter) -> float:
    ta, tb = sum(counter_a.values()), sum(counter_b.values())
    pa = {k: v / ta for k, v in counter_a.items()} if ta else {}
    pb = {k: v / tb for k, v in counter_b.items()} if tb else {}
    return M.jsd(pa, pb)


def split_half_floor(run_rows, dimension, *, n=200, seed=0, q=97.5):
    """Within-arm split-half JSD null for a dimension — the seed-noise floor the
    cross-arm JSD must clear (the ProfileDivergence machinery, per dimension)."""
    if len(run_rows) < 4:
        return float("nan")
    rng = random.Random(seed)
    idx = list(range(len(run_rows)))
    half = len(run_rows) // 2
    draws = []
    for _ in range(n):
        rng.shuffle(idx)
        a = [run_rows[i] for i in idx[:half]]
        b = [run_rows[i] for i in idx[half:]]
        draws.append(jsd_norm(dim_counter(a, dimension), dim_counter(b, dimension)))
    return percentile(draws, q)


def main() -> int:
    rows = load()
    out: dict = {"n_rows": len(rows), "seeds": None, "profiles": {}, "overlap_check": {}}
    seeds = sorted({r["seed"] for r in sel(rows, arm="corpus")})
    out["seeds"] = len(seeds)

    print("=" * 92)
    print(f"PLURAL PREFERENCE — three arms, {len(seeds)} matched seeds, "
          "modulators null, no MTD, v2_partial, retrace")
    print("=" * 92)

    references = {p: M.corpus_edge_weights(load_routing_net(p)) for p in PROFILES}

    # ---- the measure table + CI-separation verdict per profile per dimension ----
    for profile in PROFILES:
        corpus = sel(rows, arm="corpus", profile=profile)
        uniform = sel(rows, arm="uniform_null", profile=profile)
        pblock: dict = {"dimensions": {}}
        print(f"\n--- {profile}  (corpus n={len(corpus)}, uniform n={len(uniform)}) ---")
        print(f"  {'dimension':11} {'corpus even [CI]':26} {'uniform even [CI]':26} "
              f"{'sep?':5} dir")
        for dim in M.PLURAL_DIMENSIONS:
            c_even = bootstrap_ci(corpus, evenness_of(dim))
            u_even = bootstrap_ci(uniform, evenness_of(dim))
            c_d = bootstrap_ci(corpus, d_of(dim))
            u_d = bootstrap_ci(uniform, d_of(dim))
            c_hd = M.hill_diversity(dim_counter(corpus, dim))
            u_hd = M.hill_diversity(dim_counter(uniform, dim))
            floor = split_half_floor(corpus, dim)
            cross_jsd = jsd_norm(dim_counter(corpus, dim), dim_counter(uniform, dim))
            sep = disjoint(c_even, u_even)
            shape_certified = dim in SHAPE_DIMENSIONS
            direction = ("concentrate" if c_even[0] < u_even[0] else "spread") if sep else "-"
            pblock["dimensions"][dim] = {
                "shape_certified": shape_certified,
                "corpus": {"N": c_hd.support_n, "D": round(c_hd.effective_number, 3),
                           "evenness": round(c_hd.evenness, 3),
                           "even_ci": [round(c_even[1], 3), round(c_even[2], 3)],
                           "D_ci": [round(c_d[1], 3), round(c_d[2], 3)]},
                "uniform": {"N": u_hd.support_n, "D": round(u_hd.effective_number, 3),
                            "evenness": round(u_hd.evenness, 3),
                            "even_ci": [round(u_even[1], 3), round(u_even[2], 3)],
                            "D_ci": [round(u_d[1], 3), round(u_d[2], 3)]},
                "evenness_ci_separated": sep,
                "direction": direction,
                "cross_arm_jsd": round(cross_jsd, 4),
                "split_half_floor": round(floor, 4) if floor == floor else None,
                "jsd_clears_floor": bool(cross_jsd > floor) if floor == floor else None,
            }
            tag = "" if shape_certified else "  (shape WITHHELD, P3)"
            print(f"  {dim:11} "
                  f"{c_even[0]:.3f}[{c_even[1]:.3f},{c_even[2]:.3f}]".ljust(26) + " "
                  f"{u_even[0]:.3f}[{u_even[1]:.3f},{u_even[2]:.3f}]".ljust(26) + " "
                  f"{'YES' if sep else 'no':5} {direction}{tag}")

        # alignment: field-success prior (edge dim) corpus vs uniform, + honesty check
        ref = references[profile]
        c_align = bootstrap_ci(corpus, alignment_of(ref))
        u_align = bootstrap_ci(uniform, alignment_of(ref))
        c_sub = bootstrap_ci(corpus, substrate_align)
        pblock["alignment"] = {
            "field_success_corpus": [round(c_align[0], 3), round(c_align[1], 3), round(c_align[2], 3)],
            "field_success_uniform": [round(u_align[0], 3), round(u_align[1], 3), round(u_align[2], 3)],
            "field_success_ci_separated": disjoint(c_align, u_align),
            "corpus_above_uniform": c_align[0] > u_align[0],
            "substrate_success_corpus": [round(c_sub[0], 3), round(c_sub[1], 3), round(c_sub[2], 3)],
        }
        print(f"  field-success alignment: corpus "
              f"{c_align[0]:.3f}[{c_align[1]:.3f},{c_align[2]:.3f}]  vs uniform "
              f"{u_align[0]:.3f}[{u_align[1]:.3f},{u_align[2]:.3f}]  "
              f"sep={'YES' if disjoint(c_align, u_align) else 'no'}")
        print(f"  substrate-success alignment (honesty): corpus "
              f"{c_sub[0]:.3f}[{c_sub[1]:.3f},{c_sub[2]:.3f}]")
        out["profiles"][profile] = pblock

    # ---- baseline verb dimension (the one it shares) ----
    base = sel(rows, arm="baseline")
    b_verb = M.hill_diversity(Counter(
        {v: sum(r["verb_attempts"].get(v, 0) for r in base)
         for v in set().union(*[r["verb_attempts"] for r in base])}))
    out["baseline_verb"] = {"N": b_verb.support_n,
                            "D": round(b_verb.effective_number, 3),
                            "evenness": round(b_verb.evenness, 3),
                            "n_runs": len(base)}
    print(f"\n--- baseline FSM (verb dimension, n={len(base)}) ---")
    print(f"  verb  N={b_verb.support_n}  D={b_verb.effective_number:.3f}  "
          f"evenness={b_verb.evenness:.3f}  "
          f"(structural D=1 on opening/transition/visit/terminal — no place vocabulary)")

    # ---- reproduction: plurality_reporting §2 on the overlapping seeds 0-9 ----
    print("\n" + "=" * 92)
    print("REPRODUCTION — plurality_reporting.md §2 (pooled path entropy + distinct")
    print("5-openings) on the overlapping seeds 0-9, corpus arm")
    print("=" * 92)
    for profile in PROFILES:
        c10 = [r for r in sel(rows, arm="corpus", profile=profile) if r["seed"] < 10]
        # pooled path entropy = visit-weighted per-place entropy over realised edges
        pooled_edges: dict[str, Counter] = {}
        for r in c10:
            for e, nch in r["edges"].items():
                s, d = e.split(">", 1)
                pooled_edges.setdefault(s, Counter())[d] += nch
        pe = M.path_entropy_from_transitions(pooled_edges)
        distinct5 = len({tuple(r["sequence"][:5]) for r in c10})
        out["overlap_check"][profile] = {"pooled_path_entropy": round(pe, 3),
                                         "distinct_5_openings": distinct5}
        print(f"  {profile:31} pooled path entropy={pe:.3f}  distinct 5-openings={distinct5}")

    (HERE / "pp_results.json").write_text(json.dumps(out, indent=2))
    print(f"\nwrote {HERE / 'pp_results.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
