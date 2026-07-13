---
status: durable
chapter: ch3_design
created: 2026-05-28
updated: 2026-07-13
lineage: 2026-05-28_filtering_heterogeneous_classes.md
---

# Comparing unequally-sized profiles fairly — uniform thresholds, level-aware filters, complementary views

## Position in the dissertation

The methodology chapter's defence of how the per-profile figures are filtered and presented. The same three principles govern any later figure that puts several instances side by side — defence mechanisms, attacker profiles, metric panels — so they are stated once, here.

## The idea

The four objective-conditioned profiles are built from very different sample sizes — nineteen incidents down to five, a four-fold spread — and the naive expectation is that comparing them fairly requires tuning filter thresholds per profile. Empirically it does not, and the reasons why not are themselves methodological commitments worth defending.

**Uniform thresholds keep differences interpretable.** When rendering comparable instances side by side, a single filter threshold across all of them is the default, and per-instance tuning needs positive justification. The instinct that larger classes need stricter recurrence filters (more incidents, more noise edges) turned out to be wrong: under the same "seen in ≥ 2 incidents" cutoff, all four profiles collapse into a similar band (21–34 techniques, 31–54 edges). Uniformity was the data's choice, not an aesthetic one. Had the smallest class been given a looser filter "for equal visual weight", cross-panel differences would have read as filter artefacts rather than workflow differences — per-instance tuning is editorial work the reader must reverse-engineer, so it is done only when uniform filtering demonstrably fails, and then said aloud.

**Thresholds do not transfer across aggregation levels.** A "≥ 2 observations" bar on a specific technique-to-technique edge is a strong recurrence test; the same bar on a tactic-to-tactic transition is a weak one, because each tactic transition aggregates many technique edges. Filters must be recalibrated to the unit they apply to — whenever edges roll up to transitions, techniques to tactics, or incidents to classes, ask what the threshold *means* at the new level. The tactic-level figures accordingly carry a higher cutoff, scaled from the corpus-wide reference views.

**Recurrence filters reveal shared structure and hide uniformly-diverse content — so complementary views are epistemically necessary.** The starkest case: the *double extortion* profile's defining impact stage vanishes from its technique subgraph under the recurrence filter, because every incident in the class reaches impact through a *different* encryption technique. No single view can answer both "what recurs across class members?" and "what does each member reach?" — they are different questions needing different machinery. The figure set is therefore structured as a subgraph view (where does the workflow converge), a share view (which stages does the class emphasise, however its members get there), and a delta view (how does the class deviate from the corpus-wide baseline). The class's double objective stays visible across the set even where it is absent from any single panel. When defending a classification with figures, the views should answer non-overlapping questions.

## Evidence and repo anchors

- The filter sweep and per-class counts: [`../../implementation/pipeline/gasp/partition_decision.md`](../../implementation/pipeline/gasp/partition_decision.md) §"Visualisation iteration outcomes"; regenerable figures under `data/gasp/_viz/`.
- The impact-vanishes observation as a corpus finding: [`objective_partition_findings.md`](objective_partition_findings.md) finding 2.
- The surface-vs-ancestor subgraph distinction the third principle builds on: [`../../implementation/pipeline/gap/gap_schema.md`](../../implementation/pipeline/gap/gap_schema.md).

## Revisit conditions

- If a later comparison (e.g. across defence mechanisms at the evaluation stage) genuinely requires per-instance thresholds — the first principle gains a qualification, not a reversal, and the justification is recorded.
- If a single view is found that captures both recurrence and reach — the third principle is restated against it.
