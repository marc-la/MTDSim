---
status: durable
created: 2026-05-28
topic: filtering methodology for comparing heterogeneously-sized class subgraphs
---

# Filtering thresholds for comparing heterogeneously-sized class subgraphs — uniform-when-possible, level-aware, complementary views

## Why this is worth recording

The L2 / GASP visualisation iteration produced three coupled methodological
choices that I'll need to defend in chapter 3 (where the per-class subgraph
figures live). The classes range from 5 to 19 flows — a 4× spread in
sample size — and a naive expectation is that per-class filter tuning is
necessary to compare them fairly. Empirically it isn't, but the *reasoning*
why isn't is dissertation-worthy: it's the same reasoning that applies to
L4 metric comparisons across MTD schemes, attacker-profile trace overlays,
and any chapter figure that puts N instances side-by-side. These three
principles travel together and reinforce each other.

## The substance

### Principle 1: uniform-when-possible filtering preserves cross-panel comparability

When rendering N comparable instances side-by-side, default to a **uniform
filter threshold across all instances**. Per-instance tuning is only
justified when uniform filtering visibly fails for one or more instances.

Worked example from the GASP iteration: the 4 classes vary 4× in flow
count (`pure_steal` 19 flows, `infrastructure_setup` 5). The instinct
that bigger classes need stricter filters (because more flows → more
noise edges) turned out to be wrong empirically. A `--stats` sweep
showed:

| Class | flows | obs≥1 (n/e) | **obs≥2 (n/e)** | obs≥3 (n/e) |
|---|--:|--:|--:|--:|
| pure_steal | 19 | 98/413 | **34/54** | 6/6 |
| pure_impediment | 8 | 62/254 | **27/46** | 6/6 |
| double_extortion | 6 | 57/225 | **21/31** | 4/4 |
| infrastructure_setup | 5 | 39/148 | **21/34** | 5/5 |

Every class collapses to a similar 21–34 node / 31–54 edge range at the
same `obs ≥ 2` threshold. Going uniform was *the data's choice*, not
mine. If I had per-tuned (e.g. obs=2 for the 3 big classes, obs=1 for
the small one to "give it equal visual weight"), cross-panel visual
differences would have read as filter-threshold artefacts rather than
workflow differences. The uniform choice is more conservative *and*
more informative.

The general rule: **uniform thresholds make differences interpretable
as differences in the underlying data; per-instance thresholds make
differences uninterpretable until the reader audits the tuning table**.
Per-tuning is editorial work that the reader must reverse-engineer; do
it only when uniform demonstrably fails.

### Principle 2: filter thresholds don't transfer naively across aggregation levels

`obs ≥ 2` at the *technique-edge* level (a specific T-ID-to-T-ID edge
seen in ≥2 flows) is a strong recurrence bar. The same `obs ≥ 2` at the
*tactic-FSM transition* level (summed observation count across all
technique edges between a tactic pair) is a much weaker bar, because
tactic transitions aggregate many technique edges (e.g. a single
discovery → stealth transition can be backed by 5+ different
technique-pair edges).

The chosen tactic-FSM threshold was `obs ≥ 3`, mirrored from
[`../../data/gap/_viz/gap_viz.py`](../../data/gap/_viz/gap_viz.py)'s
`obs ≥ 4` cutoff for the GAP-wide tactic FSM (scaled down for the
smaller per-class transition counts). This brings each per-class panel
to 26–53 of 61–118 transitions — comparable density to the GAP-wide
reference, where the equivalent threshold gives 52/132.

The general rule: **when filtering aggregated data, recalibrate the
threshold to match the aggregated unit**. A common threshold across
aggregation levels is almost always wrong — it either over-filters the
aggregate (cutting backbone) or under-filters it (showing noise).

Where this re-surfaces: anywhere edges get rolled up to transitions,
techniques to tactics, flows to classes, time-steps to windows. Always
ask: "what does *the threshold* mean at *this* level?".

### Principle 3: recurrence filters reveal shared structure, hide uniformly-diverse content — complementary views are epistemically necessary

The starkest finding from the iteration: `double_extortion`'s `impact`
tactic disappears from the technique subgraph at `obs ≥ 2`. Every flow
in the class reaches impact (it's part of the class definition —
"ransomware that both exfiltrates *and* encrypts"). But each ransomware
family uses a different encryption technique variant (T1486 Data
Encrypted for Impact in some, T1490 Inhibit System Recovery in others,
T1565 Data Manipulation, etc.). No specific edge into the impact tactic
*recurs* across two members of the class. The recurrence filter hides
what's uniformly-diverse.

This isn't a viz bug. It's a property of recurrence filtering, and it
has a methodological consequence: **a single view can never capture
both "what recurs across class members" and "what each class member
reaches"**. Different questions; different machinery.

The GASP viz set is structured around this:

- **Subgraph view** (`gasp_grid_technique.png`): "what edges recur".
  Answers: where does the class's workflow converge?
- **Heatmap view** (`gasp_comparison.png` top panel): "what tactic
  shares are present per flow". Answers: which tactics does the class
  emphasise, even if its members reach them via different techniques?
- **Delta view** (`gasp_comparison.png` bottom-left): "where does each
  class deviate from the GAP-wide baseline". Answers: what's
  *distinctive* about this class's tactic mix?

For double_extortion, the impact share remains *visible* in the heatmap
(13% impact share, top of the column among classes) even though the
impact *tactic* is absent from the obs≥2 subgraph. The class's defining
double-objective is preserved across the viz set — just not in any
single panel.

The general rule: **when defending a classification scheme with
visualisation, use complementary views that answer non-overlapping
questions**. The reviewer who asks "but does class X actually reach
tactic Y?" needs a flow-share view; the reviewer who asks "what's the
workflow shape?" needs a subgraph view. Sub-questions of the same
high-level question ("are these classes distinct?") need orthogonal
visual evidence.

## How it connects

- To the spec:
  [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) defines the
  surface vs ancestor subgraph distinction that Principle 3 builds on
  (surface subgraphs preserve recurrence-filter discoverability of
  workflow shape; ancestor cones don't).
- To the partition decision:
  [`./2026-05-28_l2_partition_decision.md`](./2026-05-28_l2_partition_decision.md)
  §"Visualisation iteration outcomes" records the specific cutoffs
  chosen and the double_extortion impact-loss observation; this note
  captures the underlying *methodological* principles those choices
  exemplify.
- To future work: when the L4 metrics comparisons across MTD schemes
  (architecture §(h)) land, the same principles apply: uniform metric
  thresholds across schemes, level-aware aggregation (e.g. per-step
  vs per-episode statistics), and multiple complementary metrics
  (MTTC, ASR, executed-set Jaccard) for non-overlapping questions.
- To the lit review: connects to the *small-N-class-comparison* problem
  Marc's metadata-audit instinct kept flagging — the L2 has classes as
  small as 5 flows, and these principles are what justifies treating
  small classes as comparable to large ones (with appropriate caveats).

## When this would need updating

- If the L4 metrics framework ends up requiring per-scheme thresholds
  for non-trivial reasons (i.e. uniform demonstrably fails) — Principle
  1 would need a qualification, not a reversal.
- If a future class-comparison method (e.g. a flow-distinct edge count
  instead of obs-sum) makes Principle 2's level-aware recalibration
  redundant — re-evaluate.
- If chapter 3 ends up replacing the heatmap+delta with a single
  alternative view that captures both "what recurs" and "what's
  reached", Principle 3 would need to be restated to the new view's
  framing.
