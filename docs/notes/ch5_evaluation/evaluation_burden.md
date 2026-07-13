---
status: durable
chapter: ch5_evaluation
created: 2026-07-07
updated: 2026-07-13
lineage: distilled from 2026-07-07_cross_sectional_review.md (the process review itself is retired; git history retains it)
---

# The evaluation's burden of proof — ranking stability and ranking divergence

## Position in the dissertation

The evaluation chapter's organising requirement: the two results the experiments must produce for the thesis's central claim to stand, and the disposition if they do not. The methodology chapter promises this test; this note specifies it.

## The idea

The thesis's central claim is that behavioural fidelity in the attacker model *changes the answer* an MTD evaluation returns — that the ranking of defence mechanisms produced against a slow, objective-driven, behaviourally-grounded attacker differs from the ranking produced against the fast procedural attacker the simulator inherits. Two objections, each strong enough to fail the claim at examination, follow directly from how the profiled attacker was built, and both are answered by the same pair of experimental results.

**The first objection: the novel behaviour rests on invented parameters.** The profiled attacker differs from the procedural baseline through exactly two families of introduced parameters — the per-tactic durations and the per-tactic reset fractions (how much of a tactic's progress one defensive mutation destroys). Neither family is measured; both are declared from mechanism arguments and assigned sweep bands. Strip those parameters and nothing separates the profiled attacker from the generic one. The defence — that declare-and-sweep is the established practice in timed attack modelling, and that the bands are mechanism-bounded rather than free — is genuine but incomplete until the sweep is actually run: a declared parameter is defensible only while the conclusion is shown not to hinge on where in its band the value sits.

**The second objection: "fidelity changes the answer" is indistinguishable from parameter noise.** A ranking difference between the two attackers means nothing if the profiled attacker's own ranking wobbles across its uncertainty bands — any observed divergence could then be an artefact of where the declared values were pointed, not of behavioural fidelity. The claim is only evidenced when the divergence is *larger than* the profiled attacker's own sensitivity.

Both objections therefore reduce to one two-part burden on the evaluation:

1. **Stability.** The MTD ranking produced by the profiled attacker must be stable across the declared sweep bands — the same ordering (or an ordering whose changes are characterised and bounded) at the extremes of every swept duration and reset fraction.
2. **Divergence.** That stable ranking must differ from the (also stable) ranking produced by the procedural baseline attacker under identical conditions.

Stability without divergence means behavioural fidelity was not worth modelling — the generic attacker was a sufficient evaluation instrument. Divergence without stability means the result is an artefact of declared parameters. Only the conjunction supports the thesis's claim; the experiments are designed to test the conjunction directly, not either half alone.

**The negative result is a result.** If the conjunction fails, the honest disposition is not to soften the claim but to report the failure as a finding about the limits of CTI-derived behavioural grounding on a corpus of this size: the profiles constitute a defended design whose behavioural distinctions do not survive their own uncertainty, and the contribution retreats to the construction method and the negative demonstration. This disposition is stated in advance — before the experiments run — precisely so the result cannot be quietly reframed after the fact.

Until these experiments run, every statement of the central claim in earlier chapters is a *defended design*, not a demonstrated result, and is worded as such.

## Evidence and repo anchors

- The declared-parameter families and their bands: the per-tactic profiles at [`../ch3_design/tactic_profiles/`](../ch3_design/tactic_profiles/) (§5 blocks) and the shipped catalogue [`../../../data/ogasp/tactic_durations.json`](../../../data/ogasp/tactic_durations.json).
- The declare-and-sweep precedent: [`../ch2_background/tactic_duration_precedent_survey.md`](../ch2_background/tactic_duration_precedent_survey.md); extractions [`timed_attack_models`](../../sources/extractions/timed_attack_models.md), [`bland2020`](../../sources/extractions/bland2020.md), [`mcqueen2006`](../../sources/extractions/mcqueen2006.md).
- The validity framework the sweep discipline belongs to: [`../ch3_design/operational_validation.md`](../ch3_design/operational_validation.md).
- The claim being protected: [`../../implementation/architecture.md`](../../implementation/architecture.md) §(j) (*fidelity changes the answer*).
- The experiment's substrate: the timeline runner and weighted nets under [`../../../data/ogasp/`](../../../data/ogasp/); open L3 handoffs in [`../../handoffs/`](../../handoffs/).

## Revisit conditions

- When the sweep and discrimination experiments run: this note is rewritten around the observed result (positive or negative), and the "defended design" wording in earlier chapters is upgraded or the negative-result disposition applied.
- If the sweep bands themselves change (a profile's mechanism argument is revised), the stability half of the burden must be re-run against the new bands.
