---
status: durable
chapter: ch4_methods
created: 2026-05-29
updated: 2026-07-13
lineage: 2026-05-29_l2_synthesis.md
---

# What the objective partition found — weighted overlays, observational bias, and the structural-versus-narrative pivot

## Position in the dissertation

The methodology chapter's account of what partitioning the technique graph by operational objective actually produced — which is not what the design anticipated, and shapes the execution model downstream. Its fourth finding (incident corpora cannot be read structurally for objective) is a candidate stand-alone methodology claim.

## The idea

Partitioning the aggregated technique graph into four objective-conditioned profiles — *exfiltration objective* (19 incidents), *impact objective* (8), *double extortion* (6), and *no realised objective* (5) — was meant to give the evaluation its second axis: distinguishable kinds of attacker. What it produced is subtler: not four crisply separated attacker variants, but four **objective-conditioned weightings over a shared technique substrate**. The classes share most of the parent graph and diverge in *which transitions are emphasised*, not in *which techniques exist* — a fundamentally different kind of finding than "four disjoint attack graphs", with direct consequences for how an attacker should be parameterised. Five findings, each computed against the built artefacts:

### 1. The classes are weighted overlays over a shared substrate

Every one of the parent graph's 124 techniques appears in at least one class; a sixteen-technique backbone — command-line execution, ingress tool transfer, obfuscation, indicator removal, remote services, phishing, and similar tactic-agnostic tradecraft — appears in *all four*. Pairwise node overlap (Jaccard) runs 0.295–0.422: overlapping substrates, not partitions. The differentiation lives in tactic-share emphasis: the impact tactic's share moves from 0% (*no realised objective*) to 11.3% (*impact objective*); exfiltration appears only where the operation extracts data; discovery dominates every class (14.5–22.8%). The implication for the execution model: a class-parameterised attacker should not differ in which techniques are *available* but in which transitions are *weighted high* — the partition hands forward a graph plus per-class edge-frequency profiles, not four disjoint graphs.

### 2. A recurrence filter exposes the corpus's thin-generalisation seam

At a "seen in ≥ 2 incidents" filter, every class shrinks by roughly half in nodes and four-fifths in edges — the parent graph's 88% single-observation share propagates straight into the classes. The cleanest demonstration is that *double extortion*'s entire impact tactic disappears under the filter: every incident in the class reaches impact (it is part of the class's definition), but each ransomware family uses a different encryption technique, so no impact edge recurs. The class shares its theft-preparation workflow and diverges on the mechanism of harm. Downstream evaluation that operates on the full surface inherits the single-incident long tail; evaluation on the recurring core interprets a much smaller substrate — the threshold is a methodological lever the thesis names, not a cosmetic knob (see the companion filtering note).

### 3. The residual class is a finding about the data, not about attackers

All five *no realised objective* incidents are documented as either evicted before completing their mission or pre-positioning with no observed payload; the class contains zero impact and zero exfiltration techniques. It is not a class about what some attackers want; it is a class about *what the corpus records when defenders intervene early* — a defender-eviction signature in operational-CTI vocabulary. The partition therefore does two jobs at once: it carves a behaviourally coherent subgraph, and it names a corpus-level observability boundary. This is deliberate: the label "position for future" from the survey literature was rejected precisely because it implies intended surveillance, which these incidents are not.

### 4. Incident corpora cannot be read structurally for objective — the analyst's narrative is the load-bearing source

A purely structural classification (read the objective off the incident graph's terminal action) agrees with a narrative-sourced audit on only 61% of incidents, and the disagreement is not noise: it is *truncated breach reports*. Of the nineteen theft campaigns, only nine reach an exfiltration step structurally — in the other ten (Equifax, Marriott, Uber, and others), the analyst drew the operation up to the point of detection and stopped, and the structural mechanism mistakes that truncation for pre-positioning even where the report states the theft objective explicitly. The structural reading also under-credits compound campaigns: of six canonical double-extortion operations, it identifies only one as multi-objective. The pivot to narrative-sourced classification is thus itself a finding about Attack Flow corpora: analysts draw *up to detection*, so the corpus systematically under-runs the kill chain at the back end just as it does at the front, and operational objective must be recovered from the analyst's stated narrative, not the drawn graph.

### 5. The separation signal is real, operator-robust — and thin

Distributional divergence between the classes' technique frequencies (mean Jensen-Shannon divergence 0.317 across the six class pairs) sits clearly above a random-partition null (95th percentile 0.148) — about a 2× margin, not 10×. The signal survives collapsing multi-incident operators to one representative each (n = 29), so it is not an artefact of one prolific group at corpus level; but half the *double extortion* class is one operator's variants, and two incidents have no clean home in the four-class scheme and are retained with downgraded confidence rather than force-fitted. The defensible claim at examination is therefore *the class structure this corpus contains*, not *the class structure such operations naturally have*.

### Strengths and limitations, in one place

Defensible: an end-to-end per-incident audit trail with vendor citations behind every class assignment; an observable slicing axis (what the operation did) that sidesteps motivation-as-inference; a corpus-empirical class set (the lightest scheme that names the corpus's shape); a deterministic, null-calibrated separation check that survives operator deduplication. Not defensible, and disclosed: the thinness inherited from the parent graph; the operator concentration in the smallest classes; the modest absolute separation; and the two honest-edge misfits. If the simulator-level discrimination downstream rests on a thin corpus signal *and* a thin deduplication margin, the operator-stratified holdout becomes the load-bearing test rather than a hedge.

## Evidence and repo anchors

- Canonical data model + separation statistics: [`../../implementation/pipeline/gasp/gasp_schema.md`](../../implementation/pipeline/gasp/gasp_schema.md) §(g); artefacts under `data/gasp/` (per-class subgraphs, `metadata_audit.csv` — the load-bearing classification input).
- Decision record and per-incident defence: [`partition_decision.md`](../../implementation/pipeline/gasp/partition_decision.md), [`per_flow_justifications.md`](../../implementation/pipeline/gasp/per_flow_justifications.md) (includes the truncation markings behind finding 4).
- Siblings: [`objective_partition_rationale.md`](objective_partition_rationale.md) (why slice, and on what axis), [`operator_concentration.md`](operator_concentration.md) (finding 5's threat, expanded), [`uniform_filtering_for_comparison.md`](uniform_filtering_for_comparison.md) (finding 2's filter methodology), [`technique_graph_construction.md`](technique_graph_construction.md) (the parent graph's thinness and observability bias).
- Consequence for the execution model: [`structure_to_behaviour_binding.md`](structure_to_behaviour_binding.md).

## Revisit conditions

- If the corpus grows: recompute the overlap, filter-collapse, and divergence numbers; the weighted-overlay reading could sharpen or dissolve.
- If the simulator-level discrimination test runs: finding 5's "thin but real" hedging is replaced by the observed result.
- If a five-class scheme (adding a monetisation/multi-purpose class) is adopted after corpus growth: findings 3 and 5 re-open.
