---
status: open
created: 2026-08-01
---

# Choose the dissertation title from the workshopped candidates — at drafting time, after the abstract

The title is written **last** (after the abstract, per
[`../notes/_writing_guide.md`](../notes/_writing_guide.md)), so this handoff
parks a finished workshop, not an open argument. The session that drafts the
front matter picks from the shortlist below — or beats it, but from this
shortlist, not from scratch.

## State of play

The headline finding is locked in at
[`../notes/ch5_evaluation/defence_ranking_inversion.md`](../notes/ch5_evaluation/defence_ranking_inversion.md)
and scored as the criterion's Row B at the **recommendation** grade
([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
§(d2)). The workshop distilled one rule from it: **the title's verb must be one
the scorecard already earned**, and mechanism-in-brief plus effect is the
ceiling for one line — the *why* (campaign structure, objective conditioning)
belongs to the abstract.

**The rejected original**, recorded so it is not re-proposed: *"M(AP)TD: A
framework of improved attack fidelity to provide robust, portable, and
extensible evaluation of MTD mechanisms"*. Four independent failures:

1. *robust* is on the voice contract's banned-tells list, and *robust,
   portable, and extensible* is the banned rule-of-three triad
   ([`../workflows/voice.md`](../workflows/voice.md) §(h)) — and none of the
   three is evidenced anywhere; portability is closest to *contradicted* (the
   comparability boundary, and the tactic-to-verb mapping remaining a declared
   input).
2. *improved attack fidelity* grades comparatively without naming its baseline;
   the defensible fidelity claim is relative to the project's own constructed
   descriptor (procedural vs the cross-section's parametric/scripted), which a
   title cannot carry — so the title should *describe* ("behaviourally-grounded",
   "CTI-grounded campaign profiles"), never grade ("greater/improved fidelity").
   The circularity flag — *higher fidelity, by whose instrument?* — must travel
   with any comparative use in the body; the descriptor-fixed-before-scoring
   defence is in the criterion §(a), §(e).
3. *attack fidelity* is the wrong noun — the descriptor grades the *attacker
   model*, not attacks.
4. *framework* positions the contribution as a tool; the evidence positions it
   as a finding about the evaluation.

**A purely descriptive title was also rejected, by Marc**: it carries no effect,
mechanism, or outcome. The title is to bear the finding. A finding-bearing
title is licensed despite the headings-state-their-topic ruling because a
dissertation title conventionally carries more than a section heading, and the
claim is pre-registered rather than invented for the title.

**The headline's two calibrated strengths** (both are Row B, worded to its
grades):

- *Safe (ordering grade — holds at both tested intervals):* an attacker model
  grounded in APT campaign behaviour produces a different ranking of MTD
  mechanisms than the scripted attacker the field evaluates against.
- *Sharp (recommendation grade — operating interval only, directional at ten
  seeds):* it near-reverses the ranking (ρ = −0.893) and changes which
  mechanism the evaluation recommends.

Note "different rank order" *undersells*: that is grade 2, and the evidence on
record supports grade 3 at the operating interval.

**On the M(AP)TD device**: genuinely clever — APT spans the parenthesis inside
MTD, and the nesting mirrors the thesis. Costs: parenthesised acronyms cause
citation/search/typesetting friction and will be flattened to "MAPTD"; the
name near-collides with the inherited MTDSim/MTDSimTime lineage (signals
lineage, invites confusion). Keep it only if the subtitle does the honest
descriptive work.

## The shortlist

1. **M(AP)TD: behaviourally-grounded APT profiles change which Moving Target
   Defence an evaluation recommends** — mechanism + object + effect; the verb
   is Row B's grade-3 outcome. Exposure: the recommendation grade is claimed at
   the operating interval only, and the abstract must carry that caveat in the
   same breath.
2. **M(AP)TD: the Moving Target Defence that wins depends on the attacker model
   it is evaluated against** — the paired-opposition form; states the effect
   without the mechanism, claims sensitivity rather than a specific inversion,
   so it is the most caveat-proof of the finding-bearing forms.
3. **M(AP)TD: CTI-grounded APT campaign profiles change the ranking of Moving
   Target Defences under evaluation** — "ranking" is the ordering grade, which
   holds at both tested intervals; nothing in the title is regime-dependent, at
   the cost of the "recommendation" punch.

Workshop's pick: 1 if the abstract owns the interval caveat from its first
breath; 3 if the title must be one no examiner can lean on.

## Validation gate

A title is committed in `docs/thesis/dissertation.tex`, chosen by Marc, that
(a) contains no §(h) banned tell, (b) makes no claim outside the criterion's
scored rows, and (c) survived the drafting-order discipline (written after the
abstract). Delete this handoff in that commit.

## Hard constraints

- The sharp candidates fall back to the safe one if either experiment-2 revisit
  condition fires: the mapping-sensitivity study not preserving the inversion,
  or the retrace-cell re-take moving a ranking position
  ([`../notes/ch5_evaluation/defence_ranking_inversion.md`](../notes/ch5_evaluation/defence_ranking_inversion.md)
  § Revisit conditions).
- Australian English; the voice contract's banned-tells table applies to the
  title as to any prose.
- No internal codename (GASP, OGASP, substrate, …) may appear in the title.

## Reading list

- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d2) Row B — the graded claim the title's verb must not exceed.
- [`../notes/ch5_evaluation/defence_ranking_inversion.md`](../notes/ch5_evaluation/defence_ranking_inversion.md)
  — the headline note the title compresses.
- [`../workflows/voice.md`](../workflows/voice.md) §(h) — banned tells.
- [`../notes/_writing_guide.md`](../notes/_writing_guide.md) — title written
  last; half the writing time to title + abstract + introduction.

## Out of scope (explicitly)

Drafting the abstract or any front matter; re-running the title workshop from
scratch; moving any criterion badge to strengthen a candidate.
