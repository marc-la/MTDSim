---
status: durable
chapter: ch4_methods
created: 2026-05-28
updated: 2026-08-17
lineage: 2026-05-28_l2_operator_aggregation_concern.md
---

# Operator concentration in the corpus — classes of operation, or classes of operator?

## Position in the dissertation

A threats-to-validity defence for the methodology chapter (with its resolution test deferred to the evaluation chapter): the objective-conditioned profiles treat each incident as an independent draw from a population of *operations*, but the corpus is not operator-uniform, and an examiner will ask how we know the four classes are classes of operation rather than classes of operator.

## The idea

The thirty-eight incidents behind the objective partition include eight clusters — sixteen incidents, 42% of the corpus — in which two or more incidents share an operator: three independent analyst views of the Conti ransomware operation, two Turla emulation plans, two FIN13 cases, two OceanLotus views, two Sandworm campaigns, two Lazarus-cluster operations, and three threat-actor variants under one CISA advisory. If an over-represented operator dominates a class's behavioural signal, then what the evaluation measures is that *operator's* tradecraft, not the *objective class's* behaviour — and conclusions would generalise to those operators rather than to the classes the research question names.

The load-bearing case is the *double extortion* class: half of its six incidents are Conti variants. Its distributional signature is plausibly the Conti signature with two non-Conti incidents added, and a simulator result for the class may be a Conti-class result in disguise. A second, subtler effect runs the other way: the Lazarus cluster appears in *two different classes* (a destructive wiper in *impact objective*, a financial theft in *exfiltration objective*). Where the same operator straddles classes, its shared tradecraft *reduces* measured between-class separation — so operator aggregation partly *understates* class separation even as it inflates within-class coherence. The two effects do not cancel; they mean the corpus-level separation number is neither a clean upper nor lower bound.

Three mitigations of increasing decisiveness were identified, and the first has been run. **Deduplication:** collapse each multi-incident operator to one representative and re-test separation — on the deduplicated corpus (n = 29) the between-class divergence still clears the random-halving null it was first held against, so the class signal is not operator-driven *at corpus level* — with the qualification, added when the null was tightened, that under a size-matched null only the coarse tactic-share separation survives deduplication and the technique-level and transition-level statistics do not (the companion findings note carries the full statement). **Reweighting:** weight each incident by the inverse of its operator's incident count, which quantifies (rather than resolves) how much signal operator concentration contributes. **Stratified holdout at the simulator level** — the decisive one, still open: run the evaluation's discrimination test with the dominant operator's incidents held out of the class, and again with *only* them; convergence between the two means the class is operator-robust where it matters, in simulator outcomes. This is the test a defence would point to if pressed, and it belongs to the evaluation phase.

The honest framing that survives all of this: aggregation across operators can smooth within-class variance only for behaviour the corpus actually observes recurring. Since 88% of the parent graph's edges are single-observation, aggregation cannot synthesise generalisation where the corpus has none — the deduplication result licenses the class labels, and the stratified holdout, once run, bounds what they mean. The long-term mitigation is corpus growth targeted at the concentrated classes (more non-Conti double-extortion operators; more pre-payload incidents), through the hand-curation seam the pipeline deliberately keeps open.

## Evidence and repo anchors

- Operator-cluster table and the four mitigations in full: [`../../implementation/pipeline/gasp/partition_decision.md`](../../implementation/pipeline/gasp/partition_decision.md) and the original concern record in git history (lineage above).
- The deduplicated re-check result: [`../../implementation/pipeline/gasp/gasp_schema.md`](../../implementation/pipeline/gasp/gasp_schema.md) §(g); `data/gasp/README.md`.
- The thinness this interacts with: [`technique_graph_construction.md`](technique_graph_construction.md) (88% single-observation); the separation numbers: [`objective_partition_findings.md`](objective_partition_findings.md) finding 5.
- Where the stratified holdout lands: [`../ch5_experimental_setup/evaluation_burden.md`](../ch5_experimental_setup/evaluation_burden.md).

## Revisit conditions

- When the operator-stratified holdout runs at the evaluation stage — this note's hedge is replaced by the observed result.
- If new incidents are added — recompute the concentration table; the Conti share of *double extortion* is the number to watch.
