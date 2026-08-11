---
status: durable
chapter: ch5_evaluation
created: 2026-08-11
updated: 2026-08-11
---

# The evaluation's grading instrument — magnitude, ordering, recommendation

## Position in the dissertation

The methodology chapter's experimental-setup section: how each comparison the
evaluation reports is scored, and the two families of comparison the scoring is
applied to. It sits beside the burden-of-proof requirement (which fixes *what*
the evaluation must show) and supplies the vocabulary in which the headline
result is stated.

## The idea

An evaluation that substitutes one attacker for another needs a fixed vocabulary
for what "the answer changed" means, committed before any comparison is scored;
without one, every difference can be talked up into a finding or down into noise
after the numbers are seen. This note fixes that vocabulary as three graded
outcomes and names the two experiment families it grades. The grading is to the
experiment what the fidelity axes are to the attacker model — the yardstick the
work is scored against, written down first so it cannot be reverse-fitted to
flatter the result.

The instrument has three grades, each strictly stronger than the last. The first
is **magnitude**: the same defences win, but by different margins — the evaluation
agrees on what to deploy and disagrees only on how much it helps. The second is
**ordering**: the ranking of the defences changes, so a practitioner comparing
mechanisms would read a different table depending on which attacker the
evaluation carried. The third is **recommendation**: the single top-ranked
mechanism changes, so the one deployment decision an evaluation exists to inform
is itself a function of the threat model. A comparison is scored at the highest
grade its evidence carries and no higher, and the grade is stated with the
mutation tempo and sample size it was taken at, because a ranking taken where no
attacker can complete its objective grades nothing.

Three grades rather than a binary verdict, because "fidelity affects the
evaluation" is unfalsifiable as stated — everything affects everything — and an
examiner is right to reject it. A graded instrument says exactly how far the
answer moved and refuses to round a magnitude shift up into a changed
recommendation; it makes the modest reading and the strong reading distinguish
themselves on the evidence rather than on the phrasing.

The instrument grades two families of comparison, and the split is the design's
organising cut. The first is **prior-model comparison**: the published
evaluations this work descends from are re-run on one simulator against both
attackers, so that each lineage headline — network-shuffling dominates
diversification \citep{zhang2023}, the best single mechanism roughly equals the
best combination \citep{brown2023}, diversification dominates at long intervals
\citep{ho2024} — becomes a claim the evaluation can test rather than cite. That
the lineage already disagrees with itself on the first and third of these is not
an embarrassment to reconcile but the phenomenon to explain: different attacker
behaviours reward different mechanism families, which is the thesis in one
sentence. The second family is **fresh evaluation**: a crossing of attacker,
defence, network scale, connection density and mutation tempo, designed so that
each fidelity extension the attacker carries has at least one cell in which its
intended effect should appear — network scale for the within-run learning
capability, a defence whose cost is not proportional to dwell for the cost
sensitivity — which turns "does this extension matter to an evaluation" from an
assumption into a measured question. The two families answer one research
question: what greater attacker fidelity implies for current methods of
evaluating moving target defence.

One concession is load-bearing and is made here rather than left for a reader to
find. The comparative run that anchors the first family has already been taken,
so one cell of the evaluation is an observed result and not a prediction, and
genuine pre-registration is available only for the robustness questions built on
top of it — whether the observed divergence survives changes of scale, density
and tempo. The honest response is to partition the two: the anchor is reported as
what motivated the sweep, and the pre-registration claim attaches only to the
frontier that was genuinely unseen when its criteria were fixed. A robustness
programme built to stress a known result is a stronger design than a fabricated
prediction of it, and the strength and the limitation here are the same fact.

At the operating tempo the anchor already reaches the top grade: the recommended
mechanism changes with the attacker, with the two defence orderings very nearly
reversed. The reading is directional at the sample size run rather than
significance-tested, it is a property of the high-pressure tempo and weakens as
mutations are spaced further apart, and it is bounded by the mapping from
campaign tactics to simulator actions remaining a chosen input rather than a
recovered fact. Those caveats travel with the grade, in the row, not in a
footnote. What the instrument scores throughout is what substituting the attacker
*reveals about the evaluation*, never the realism of either attacker — the
envelope discipline that governs every claim in this project governs this one.

## Evidence and repo anchors

- The three-grade instrument as scored, with its evidence bar and travelling
  caveats: [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md)
  §(d2) Row B.
- The anchor result the top grade rests on:
  [`defence_ranking_inversion.md`](defence_ranking_inversion.md) and its source
  run [`../../implementation/pipeline/ogasp/experiment_02_findings.md`](../../implementation/pipeline/ogasp/experiment_02_findings.md)
  §9.
- What the evaluation must demonstrate (the stability ∧ divergence burden this
  note supplies the scoring for): [`evaluation_burden.md`](evaluation_burden.md).
- The degenerate operating region that gates which grades a tempo can carry:
  [`operating_point_discrimination.md`](operating_point_discrimination.md).
- The fresh-family cell designed to let the learning capability show its intended
  effect: [`../../handoffs/2026-08-11_learning_scale_dependence.md`](../../handoffs/2026-08-11_learning_scale_dependence.md).
- The lineage headlines re-run as prior-model comparisons: extractions
  [`zhang2023`](../../sources/extractions/zhang2023.md),
  [`brown2023`](../../sources/extractions/brown2023.md),
  [`ho2024`](../../sources/extractions/ho2024.md).
- The claim the grading protects:
  [`../../implementation/architecture.md`](../../implementation/architecture.md)
  §(j) (*fidelity changes the answer*).

## Revisit conditions

- When the fresh-family sweep runs, the pre-registered robustness rows are scored
  against this instrument and this note gains their verdicts; the anchor/frontier
  partition above is the audit trail for which rows may claim pre-registration.
- When a seed count that supports a significance claim is run, the top grade's
  "directional" qualifier is re-decided.
- When the mapping-sensitivity study lands, the mapping caveat bounding the top
  grade is tightened or discharged.
- If the lineage-replication rows overturn a published headline under both
  attackers rather than one, that is a finding about the prior work's generality
  and is reported as such, not folded into the fidelity claim.
