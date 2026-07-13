---
status: durable
created: 2026-05-29
topic: L2 (GASP) reflective synthesis — what the 19:8:6:5 split *means*
---

# L2 reflective synthesis — weighted overlays, observational bias, and the structural-vs-narrative pivot

> **Provenance banner.** Observation-grounded synthesis. The spec is at
> [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) (*what GASP
> is*); the investigation notes ([partition reasoning](./2026-05-28_l2_partition_reasoning.md),
> [partition decision](./2026-05-28_l2_partition_decision.md),
> [per-flow justifications](./2026-05-28_l2_per_flow_justifications.md),
> [operator-aggregation](./2026-05-28_l2_operator_aggregation_concern.md),
> [assembly audit](./2026-05-28_l2_assembly_audit.md)) record *how the
> decision was reached*; this note records *what it means*. The intended
> reader is Marc-writing-chapter-3 — a working document for methodology
> narrative, not chapter prose. Per the handoff at
> [`../handoffs/2026-05-28_l2_reflective_synthesis.md`](../handoffs/2026-05-28_l2_reflective_synthesis.md).

## The shape of L2 as a finding

L2's job was to slice the GAP into behavioural variants so the thesis's
two-axis comparison (MTD family × attacker profile) has a second axis at
all. Given the artefacts L2 produced, what has been found? L2 has not
produced four crisply separated attacker variants; it has produced four
**operational-objective-conditioned weightings over a shared technique
substrate**. The classes share most of the GAP and diverge in *which
edges are weighted high*, not in *which edges exist* — a fundamentally
different kind of finding than "four disjoint attack graphs", and it
shapes the L3 design problem.

## The numbers, in one place

Five concrete observations that the rest of the note synthesises against.
Each is computed against an artefact opened this session:

1. **The four class node sets union to 100 % of the L1 GAP.** Every one
   of the GAP's 124 techniques appears in at least one class's
   `node_set` ([`../../data/gasp/gasp_pure_steal.json`](../../data/gasp/gasp_pure_steal.json),
   [`gasp_pure_impediment.json`](../../data/gasp/gasp_pure_impediment.json),
   [`gasp_double_extortion.json`](../../data/gasp/gasp_double_extortion.json),
   [`gasp_infrastructure_setup.json`](../../data/gasp/gasp_infrastructure_setup.json)).
   No GAP node is orphaned. The classes *cover* the substrate.
2. **The behavioural backbone is 16 techniques in all four classes.**
   These are tactic-agnostic tradecraft: T1059 (Command-line), T1105
   (Ingress Tool Transfer), T1027 (Obfuscated Files), T1070 (Indicator
   Removal), T1021 (Remote Services), T1218 (System Binary Proxy
   Execution), T1566 (Phishing) and nine more. Every operational
   objective uses this substrate. 52 GAP edges sit in all four edge
   sets.
3. **Pairwise Jaccard on nodes ranges 0.295–0.422** (computed across the
   four JSONs). The pair with the *most* overlap is `double_extortion`
   ↔ `pure_steal` at 0.422 (46 shared nodes); the pair with the *least*
   is `infrastructure_setup` ↔ `pure_impediment` at 0.295 (23 shared).
   None of the pairs is "near-disjoint" — the classes are *overlapping
   substrates*, not partitions of the technique set.
4. **At the `obs ≥ 2` recurrence filter, every class shrinks 46–65 % by
   nodes and 77–87 % by edges.**
   [`../../data/gasp/_viz/gasp_grid_technique.png`](../../data/gasp/_viz/gasp_grid_technique.png)
   reports 98 → 34, 62 → 27, 57 → 21, 39 → 21 (nodes) and 413 → 54,
   254 → 46, 225 → 31, 148 → 34 (edges). The L1 thinness finding (88 %
   single-observation edges,
   [`./2026-05-27_gap_construction.md`](./2026-05-27_gap_construction.md))
   propagates straight into L2: most of each class's surface is
   single-flow detail, not recurring workflow.
5. **Mean technique JSD = 0.317 vs null p95 = 0.148** across all six
   class pairs ([`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md)
   §(g)). All six pairs sit in 0.284–0.351 — modest, not stark. The
   operator-deduplicated re-check survives null on the n=29
   deduplicated corpus, so the per-class signal is operator-robust at
   the corpus level. Signal is real; signal is not dramatic.

## Findings

### F1 — The classes are *weighted overlays over a shared substrate*, not disjoint behavioural variants

The 16-technique backbone and the 100 %-of-GAP union are the load-bearing
observations here. Every class uses Command-line, Ingress Tool Transfer,
Remote Services, Phishing, Obfuscated Files, Indicator Removal, and a
dozen more — these are not optional. Pairwise overlap on edges runs as
high as 0.479 (`pure_impediment` ↔ `pure_steal`,
[gasp_pure_impediment.json](../../data/gasp/gasp_pure_impediment.json) ∩
[gasp_pure_steal.json](../../data/gasp/gasp_pure_steal.json)); even the
*least*-similar pair shares 86 edges out of a 461-edge union.

The differentiation is in *tactic-share emphasis*, not in *which
techniques are present*. Computed from the GAP's per-node tactic
mapping ([`data/gap/gap_v0.5.json`](../../data/gap/gap_v0.5.json) `nodes`):

| Class | discovery | impact | exfiltration | C2 |
|---|--:|--:|--:|--:|
| `pure_steal` (98 nodes) | 17.3 % | 1.0 % | 5.1 % | 9.2 % |
| `double_extortion` (57) | 22.8 % | 10.5 % | 3.5 % | 7.0 % |
| `pure_impediment` (62) | 14.5 % | 11.3 % | 0.0 % | 8.1 % |
| `infrastructure_setup` (39) | 20.5 % | 0.0 % | 0.0 % | 12.8 % |

The `impact` column moves from 0 % to 11.3 %; the `exfiltration` column
appears only where the operation extracts data. But discovery is
dominant in every class (14.5 %–22.8 %) and the substrate of
command-execution, lateral-movement, and stealth is broadly shared.

[`gasp_comparison.png`](../../data/gasp/_viz/gasp_comparison.png)
visualises the same pattern at the *action-share* (observation-weighted)
level: small per-tactic deltas around a shared baseline, not four
distinct silhouettes.

**Implication for L3.** A class-parameterised attacker should not
differ in *which techniques are available* — the technique pool is
largely shared. It differs in *which transitions are weighted high* on
traversal. The L3 substrate L2 hands forward is *graph + edge-frequency
profile*, not *four disjoint graphs*. Detail in *What L3 inherits*
below.

### F2 — The `obs ≥ 2` filter exposes the corpus's thin-generalisation seam, and the *impact-drops-out* finding is the cleanest demonstration

At the full subgraph level, `double_extortion` carries six impact
techniques (T1485, T1486, T1489, T1490, T1491, plus T1657, visible in
[gasp_double_extortion_obs1.png](../../data/gasp/_viz/gasp_double_extortion_obs1.png)
under the rightmost `impact` column). At the `obs ≥ 2` filter
([gasp_double_extortion.png](../../data/gasp/_viz/gasp_double_extortion.png),
21 techniques / 31 edges), the **entire `impact` tactic column
disappears**. Each of the six ransomware families in the class uses its
own encryption variant; no single impact technique appears in two or
more flows. The class shares the *theft-prep workflow* (discovery,
stealth, execution, lateral movement) but diverges on the specific
mechanism of impact. The partition-decision note flagged this as the
*Notable finding from the eyeball pass*
([`./2026-05-28_l2_partition_decision.md`](./2026-05-28_l2_partition_decision.md) §"Visualisation iteration outcomes");
the data confirms it.

This is a per-class instance of the corpus-wide thinness L1 already
documented: 88 % of GAP edges are single-observation
([`./2026-05-27_gap_construction.md`](./2026-05-27_gap_construction.md)).
At L2 the same property surfaces at the tactic level — the *defining*
behaviour of `double_extortion` (impact-and-exfil) is fragmented across
flow-specific tool choices, not consolidated into a recurring impact
technique.

A surprising side-effect: at `obs ≥ 2`, `double_extortion` (21 nodes)
and `infrastructure_setup` (21 nodes) collapse to the *same node count*,
and their edge counts are close too (31 vs 34). Their full subgraphs
differ sharply (57 vs 39 nodes; impact column present vs absent), but
their *recurring* tradecraft converges. This is consistent with F1:
the class differentiation is in the per-flow long tail, not in the
recurring core.

**Implication.** L2's recurring-behaviour signal is concentrated in a
small fraction of the surface subgraph. Downstream L3/L4 evaluation that
operates on the *full* surface inherits the long tail; evaluation that
operates on the *recurring* core (`obs ≥ 2`) is interpreting a much
smaller substrate. The threshold choice is a methodological lever the
thesis should name, not a viz-only knob.

### F3 — The partition does two jobs at once: slices the GAP for traversal, *and* surfaces the CTI corpus's observational bias

The `infrastructure_setup` class is the cleanest case. Per the audit's
per-flow justifications
([`./2026-05-28_l2_per_flow_justifications.md`](./2026-05-28_l2_per_flow_justifications.md)
§"infrastructure_setup"), all five flows are documented as *evicted
before completing their mission* (Hancitor, BumbleBee, Gootloader) or
*pre-positioning structure with no observed payload* (the two CISA
AA22-138B variants). The class has **zero `impact` tactic
techniques** and **zero `exfiltration` tactic techniques** — visible
directly in [gasp_infrastructure_setup.json](../../data/gasp/gasp_infrastructure_setup.json)
when joined to the GAP's tactic map, and in
[gasp_infrastructure_setup.png](../../data/gasp/_viz/gasp_infrastructure_setup.png)
where the `impact` and `exfiltration` columns simply do not appear.

This is not a class about *what some attackers do*. It is a class about
*what the corpus records when defenders intervene early*. The class's
defining property — pre-mission posture, no mission-stage telemetry — is
literally a defender-eviction signature, not an attacker intent. The
partition has therefore done two jobs simultaneously: it has carved out
a behaviourally-coherent subgraph (consistent with F1's weighted-overlay
reading), *and* it has named a corpus-level observability boundary in
operational-CTI vocabulary. The naming is deliberate — the partition
decision rejected Alshamrani's `position_for_future` precisely because
that label implies *intended* surveillance, which these flows are not
([`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(b)
Decision 5).

**Implication.** The 5-class size of `infrastructure_setup` is not just
a partition-size minimum; it is the corpus's own statement of how often
defenders evict attackers pre-objective. For the thesis methodology
chapter, this is more valuable as a *finding about CTI data* than as
just one more L2 class — the L2 partition is doing observational-bias
work the GAP alone could not.

### F4 — The structural-vs-narrative pivot is the load-bearing methodology choice, and it is itself a finding about Attack Flow corpora

P1 (structural-terminal classification) agrees with the audit-traced
classification on 23 of 38 flows = 61 %
([`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(b)
Decision 3). The 40 % disagreement is not noise: it is *truncated breach
reports*. Of `pure_steal`'s 19 flows, only 9 reach an exfiltration
terminal structurally — the other 10 (Equifax, JP Morgan, Marriott,
Cobalt Kitty, FIN13 Case 1, MITRE NERVE, Uber, SWIFT, Ivanti, plus
revised flows) are *visibly truncated* in the per-flow YAMLs: the
analyst drew the operation up to the point of detection and stopped
before drawing the exfil step
([`./2026-05-28_l2_per_flow_justifications.md`](./2026-05-28_l2_per_flow_justifications.md)
§"pure_steal", which marks each truncation case "TRUNCATED report" in
the per-flow notes).

The audit CSV
([`./2026-05-28_l2_metadata_audit.csv`](./2026-05-28_l2_metadata_audit.csv))
captures this directly: for `cobalt_kitty_campaign`,
`reaches_exfiltration` is `false`, yet the audit's `stated_objective` is
`steal_data` with confidence `high`, sourced from Cybereason's explicit
*"goal of stealing proprietary business information"*. The structural
mechanism would have classified Cobalt Kitty as `position_for_future`;
the audit calls it correctly.

A second mechanism failure: of the six canonical double-extortion
operators, P1 structural-terminal identifies only REvil correctly as
multi-class (terminals include both T1041 and T1486). Black Basta,
Conti × 3, and Ragnar Locker have terminals at intermediate tactics; the
audit catches all six
([`./2026-05-28_l2_partition_decision.md`](./2026-05-28_l2_partition_decision.md) §"Cross-tab P1 ↔ audit").

**The pivot is itself a finding about Attack Flow corpora.** Attack Flow
records *what the analyst drew*; the analyst draws *up to the point of
detection*. The corpus systematically under-runs the kill chain on the
back end, just as it under-runs it on the front end (10/38 flows mention
reconnaissance —
[`./2026-05-27_gap_construction.md`](./2026-05-27_gap_construction.md)).
The structural mechanism mistakes that under-run for surveillance intent;
the narrative mechanism recovers the operational objective the corpus
undershot in the graph. *Attack Flow corpora cannot be read structurally
for operational objective; the analyst's narrative is the load-bearing
source* — a fact about CTI-data-as-evidence, not just this partition.

### F5 — Honest-edge `low`-confidence flows expose a *scheme* limit, not a *data* limit; JSD signal is real but thin

Six of 38 flows = 15.8 % carry `metadata_confidence == low`
([`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(c)).
Four are CISA AA22-138B variants where `WebFetch` returned 403 and the
audit relied on structural + in-flow content (a data-source limit). The
other two are **honest edges within the scheme**:
`mac_malware_steals_crypto` (Unit 42 frames it as credential/cookie
theft + cryptomining — genuinely both-objective at the malware level,
no clean 4-class home) and `searchawesome_adware` (Malwarebytes:
*"doesn't directly exfiltrate user data"* — sits between
integrity-compromise and nuisance/monetisation;
[per-flow justifications](./2026-05-28_l2_per_flow_justifications.md)).

Both have authoritative vendor sources — they are *scheme-fit failures*,
not *data-source failures*. The 4-class compound-disjoint partition is
the *lightest* scheme that names the corpus's empirical shape; a
5-class scheme with a `monetisation` / `multi-purpose` category would
re-classify them
([`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) §(h)
open question 3). The honest move was to keep them with confidence
downgraded rather than force-fit; the downgrade is part of the
partition's contribution, not a hole in it.

The JSD margin is the load-bearing caveat behind F5's stronger framing.
Mean technique JSD = 0.317; null p95 = 0.148 — ratio ~2.1×, not ~10×.
The operator-deduplicated re-check (collapsing 3 Conti, 2 Sandworm,
2 Turla, 2 FIN13 to one representative each) survives null at n=29
([`./2026-05-28_l2_operator_aggregation_concern.md`](./2026-05-28_l2_operator_aggregation_concern.md))
but 50 % of `double_extortion` is Conti, 25 % of `pure_impediment` is
Sandworm. If L3/L4's simulator-level discrimination sits on top of a
thin corpus signal *and* a thin dedup margin, the operator-stratified
holdout (Mitigation 3) becomes the load-bearing test, not a hedge. The
defensible scope at thesis defence is *the class structure the corpus
contains*, not *the class structure a class-of-operations naturally
has*.

## Strengths and limitations, in one place

**Can defend.** (i) Per-flow audit trace —
[per-flow justifications](./2026-05-28_l2_per_flow_justifications.md)
carry vendor/ATT&CK/CTID citations end-to-end. (ii)
Operational-objective grounding — slice axis is what the operation
*did* per analyst narrative, sidestepping STIX's empty
`primary_motivation`. (iii) Corpus-empirical class set — the 4 classes
are the lightest scheme naming the corpus's shape (0 surveillance,
6 double-extortion operators a 3-class scheme could not name without
multi-membership). (iv) Deterministic JSD null at n=29 re-check
([`./2026-05-28_l2_assembly_audit.md`](./2026-05-28_l2_assembly_audit.md) §5).

**Cannot defend.** (i) Thinness — L1's 88 % single-observation share
inherits into L2; per-class recurring behaviour collapses to 21–34
nodes at `obs ≥ 2`. (ii) Operator-aggregation margin — 50 % of
`double_extortion` is Conti; dedup JSD survives null but at ~2× ratio,
not 10×. (iii) Modest JSD pair range (0.284–0.351) reads in
[gasp_comparison.png](../../data/gasp/_viz/gasp_comparison.png) as
small per-tactic deltas, not stark silhouettes. (iv) Scheme has no
clean home for 2/38 honest-edge flows; partition keeps them with
`low` confidence rather than force-fit. (v) Petri-net tractability —
min class is 39 nodes vs the primer's 10–20 bound; a Petri-net L4
column would need hand-curated slices.

## What L3 inherits — informational, not design

L3 inherits a *graph plus an edge-frequency profile*, not four
disjoint graphs. The four class subgraphs share 16 backbone techniques
and union to the full L1 GAP; differentiation lives in tactic-share
weighting and per-class long tails. A class-parameterised attacker
selects transitions from the full GAP weighted by the class's
edge-frequency profile, rather than choosing between disjoint graphs —
a different L3 design problem than earlier framings assumed.

The Jalowski primitives at
[`architecture.md`](../specs/architecture.md) §(f) — state-collision
recognition, defender-behaviour conditioning, metadata invariance —
encode *how* an attacker decides; L2 encodes *which* techniques are
available + weighted. Independent axes; L3 will need to compose them.
The operator-aggregation question (F5) resurfaces at L3/L4:
operator-stratified holdout (Mitigation 3 in the
[operator-aggregation note](./2026-05-28_l2_operator_aggregation_concern.md))
is the test the defence would point to if pressed on
class-vs-operator. Petri-net at L4
([`architecture.md`](../specs/architecture.md) §(f)) is
parallel-not-primary; per-class node counts (39–98) exceed the
primer's 10–20 bound, so promotion would need hand-curated per-class
slices, not full class subgraphs.

## Parking lot — items for future handoffs

- **L3 design.** Edge-frequency-weighted traversal over the full GAP,
  parameterised by class; composition with Jalowski primitives.
- **L4 evaluation matrix.** Operator-stratified holdout; the
  `obs ≥ 2` threshold as a methodological lever.
- **5-class scheme.** A `monetisation` / `multi-purpose` class would
  re-classify the two honest-edge flows; corpus growth is the
  precondition.
- **Petri-net per-class slices** + **toolshell flow-split** —
  out-of-scope here, flagged in
  [`02_gasp_schema.md`](../specs/02_gasp_schema.md) §(h) open
  questions 1 & 4.

## How it connects

- **Above the spec, not amending it.** No spec gaps surfaced; no edits
  to [`02_gasp_schema.md`](../specs/02_gasp_schema.md) proposed.
- **Picks up the partition-decision note's *Notable finding from the
  eyeball pass*** ([impact-drops-out at obs ≥ 2](./2026-05-28_l2_partition_decision.md))
  and consolidates it into F2.
- **Reads L1 thinness as L2 inheritance.** The 88 %-single-observation
  finding at [`gap_construction`](./2026-05-27_gap_construction.md) is
  the parent of F2's per-class collapse.
- **Substrate for chapter 3.** F4 (structural-vs-narrative pivot as a
  finding about Attack Flow corpora) is the candidate methodology-
  chapter claim; F1, F2, F3 are background.
