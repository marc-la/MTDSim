---
status: durable
chapter: ch7_discussion
created: 2026-08-09
updated: 2026-08-09
---

# Persistence is two claims, and an episodic simulation grants one of them by construction

## Position in the dissertation

The discussion chapter's honest-scope statement for the persistence property of
the APT attacker model: which half of the literature's definition this
evaluation can measure at all, why every duration-shaped measure saturated by
design rather than by accident, and why the one comparator that would complete
the measurement was declined on evidence. Feeds the consolidated limitations
synthesis.

## The idea

The literature defines the persistent attacker with two components, and they
fail differently as measurement targets. Cho et al. (2020) name persistence as
operation across multiple stages, aligned with campaigns rather than one-off
intrusions; the NIST clause quoted by Alshamrani et al. (2019) states it
behaviourally — the actor "pursues its objectives repeatedly over an extended
period of time". Extended *duration* is one component; repeated, staged
*pursuit* is the other. An evaluation that conflates them will find persistence
either trivially present or unfairly absent, and this one, until the
distinction was drawn, found both at once.

Duration is a premise of the evaluation design, not a behaviour of either
attacker. An episodic simulator runs its attacker to a fixed horizon: the
campaign lasts as long as the run because the run *is* the campaign, and this
holds for the campaign-structured movement attacker and for the incumbent
attacker alike, since both inherit the same episode structure. A measure of
whether the campaign continues therefore has no variation to explain — there is
no non-persistent arm anywhere in the design for it to separate from. The
record bears this out: every depth-of-progression measure built for the
persistence criterion returned an identical value for every attacker profile
(the first across all profiles under both stage mappings, its successor across
all eight hundred runs of the second experiment). Those saturations were first
read as instrument failures; read against the premise, they are its predicted
consequence. One further honesty condition rides with the premise: simulated
seconds carry no calibrated mapping to real campaign durations, so a run
horizon "represents" a months-long campaign only in the sense any abstraction
represents its referent — as a stated modelling premise, never as a measured
correspondence.

What the premise does not grant is pursuit — sustained staged advance that
survives the defender's interference — and pursuit is measurable, because its
comparator is not a second attacker but the defence condition. Whether progress
survives disruption is a question with a real contrast class: the same attacker
with the defence off, and across defence mechanisms. The evaluation ran
persistence-shaped measures with exactly that contrast — retention of position
across defensive mutations, coverage of campaign stages over time, projected
campaign effort under each defence — and what they returned is a measured
negative. The campaign structure traverses end to end, but effort does not
convert into breadth of compromise; retention of position against the defences
that actually contest position is near zero at the operating mutation rate; and
the movement attacker's projected campaign effort is dominated by its own low
progress rate, so its abandonment cannot be attributed to anything the defence
does. The persistence property is accordingly claimed as designed and not as
demonstrated: the campaign structure exists and runs; sustained pursuit under
contest is not on record.

One comparator the design does admit was deliberately not built: an attacker
that abandons its campaign. Its absence is a decision with an evidence trail,
not an oversight. The disengagement measure was built reader-first — projecting,
after every action, where a run *would have* abandoned, while stopping nothing —
precisely so that a null arm could falsify the defence's contribution. On the
incumbent attacker the instrument validated completely: unimpeded runs never
project abandonment, and every defence condition induces it. On the movement
attacker it discriminated almost nothing, for the progress-rate reason above.
Building the attacker that actually stops was gated on that discrimination, and
the gate held: wiring an attacker to stop under defensive pressure, when the
instrument cannot attribute the pressure, would make "the defence causes
disengagement" true by construction. Abandonment does exist in the model at two
other scopes — the incumbent attacker's per-host give-up threshold, inherited
from Brown et al. (2023), and patience as a reporting axis, read off the
disengagement frontier rather than declared as a constant. What is unconditional
is campaign-scope persistence specifically, and the literature's own
campaign-level give-up threshold — specified but never valued by its source
(*citation anchor to reconcile*: Zhang's interruption threshold) — remains the
open item it was.

## What this does not claim

It does not claim that persistence is captured by construction. A criterion
satisfied by the harness's own episode structure would be the rubric
reverse-fitted to the model, and the project's scoring instrument explicitly
bars that reading; the design premise explains why duration cannot be
*measured*, not why it should be *credited*. It does not claim the saturated
measures were well-conceived — two were adopted before the premise was
articulated, and one saturated a second time for a separate, mapping-induced
reason. And it does not claim pursuit is unmeasurable: the coverage-over-time
measure still discriminates in exactly the band the depth measures cannot see,
and a positive result there remains available to future measurement. The claim
is narrower. The duration component cannot be a finding of any evaluation
sharing this episode structure — including every baseline this work compares
against — and the pursuit component, which can be, was measured and returned
the negative the model's scorecard honestly carries.

## Evidence and repo anchors

- The persistence row, its saturation history, and the 2026-08-09 write-up
  amendment this note lands:
  [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md)
  §(d) axis 1, §(f), §(f2), §(h).
- The saturated measures and the mapping-induced second saturation:
  [`../../implementation/pipeline/ogasp/measurement_suite.md`](../../implementation/pipeline/ogasp/measurement_suite.md)
  §(c).
- Effort-to-breadth (finding 2) and the 0/100 objective reaches:
  [`../../implementation/pipeline/ogasp/experiment_01_findings.md`](../../implementation/pipeline/ogasp/experiment_01_findings.md).
- The disengagement instrument, its validation arm, the gate that declined the
  stopping attacker, and the patience axis:
  [`../../implementation/pipeline/ogasp/attacker_disengagement.md`](../../implementation/pipeline/ogasp/attacker_disengagement.md)
  §1.3, §3, §4, §7.
- Foothold retention (0.0–1.6 % against contesting defences) is carried in the
  axis-1 context retired by this note's commit; its permanent home is the
  measurement suite's axis-1 rows.
- Source extractions:
  [`../../sources/extractions/cho2020.md`](../../sources/extractions/cho2020.md)
  (§V-A), [`../../sources/extractions/alshamrani2019.md`](../../sources/extractions/alshamrani2019.md)
  (§II-A, the NIST clause). The Zhang interruption-threshold clause (IS-INT-06)
  and Brown's per-host threshold (IS-SCN-04) are anchored in
  [`../../implementation/mtdsim_intent_spec.md`](../../implementation/mtdsim_intent_spec.md);
  D-09 in [`../../implementation/intent_conformance_audit.md`](../../implementation/intent_conformance_audit.md)
  is the open ruling.
- Sibling note: [`procedural_mismatch_artefact.md`](procedural_mismatch_artefact.md)
  (the progress-rate finding this note's attribution argument leans on).

## Revisit conditions

Three things would reframe this note. If the coverage-over-time measure
separates defence conditions on a pre-registered bar, the pursuit component
moves from measured negative to demonstrated and this note's second half becomes
a results statement rather than a limitation. If the open ruling on the
campaign-level give-up threshold lands and a campaign-scope disengaging attacker
is built and swept, the "declined comparator" paragraph is superseded by
whatever that ablation shows — including the possibility that it vindicates the
gate by producing the definitional result the gate predicted. And if the
project ever adopted a calibrated mapping from simulated to real time (it will
not, within this work), the duration-premise argument would need re-stating in
calendar terms rather than horizon terms.
