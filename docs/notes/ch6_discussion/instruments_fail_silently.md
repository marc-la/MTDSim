---
status: durable
chapter: ch6_discussion
created: 2026-08-01
updated: 2026-08-01
---

# Change the attacker's shape and the evaluation's instruments fail — silently, and each in a different way

## Position in the dissertation

A discussion-chapter synthesis across the evaluation's measurement experience:
four measures of attacker progress failed during this project, each for a
structurally different reason, and the pattern they form is a transferable
methodological result that no single failure shows on its own.

## The idea

An evaluation's instruments are validated, usually implicitly, against the
attacker they were built to measure. This project replaced the attacker — a
scripted intruder walking its simulator's native procedure gave way to an
intelligence-derived campaign model with a different shape: slower, staged,
spending much of its time in activity the simulator does not score. Four times,
an instrument that was reasonable against the original attacker returned
well-formed, plausible numbers about the new one that meant something other
than what they appeared to mean. Four failures, three distinct mechanisms:
saturation, twice; an inverted sign; and a misspecified reward. Walked in
order:

The first instrument measured how deep into the campaign lifecycle an attacker
progressed, and it **saturated from above**: every profile traverses to the
final stage of its own campaign structure and then fails against the simulated
network rather than against its own model, so the measure returned its maximum
for every run and could discriminate nothing. The deficiency was invisible in
the aggregate — a full-marks column looks like success — and was only exposed
when a sensitivity sweep needed the measure to vary and found it could not.

The second instrument was the repaired replacement — depth counted only through
stages whose actions the environment *accepted* — and it **saturated from
below**: under the operative mapping, the campaign's late stages dispatch no
scoreable action at all, so no verdict can exist there and the measure is
truncated by construction. It returned the same value for all eight hundred
runs of the comparative experiment. The replacement for a saturated measure was
itself saturated, for a structural reason no inspection of the measure's
definition would reveal — the fault lay in the interaction between the measure
and the mapping, two components that were each sound alone.

The third instrument counted foothold retention across defensive mutations, and
its **sign was backwards**: cross-examined against its implementation, the
quantity counted footholds *severed* by the defence rather than kept against
it. Beneath the inversion sat a second artefact — defences that never contest
position at all produced perfect apparent retention, by the absence of any
threat to it. The first analysis pass reported the attacker's persistence as
demonstrated on this measure, and the claim was withdrawn only because the
pre-registered criterion forced the measure back against its implementation
before the badge moved. This is the failure that came nearest to entering the
record as a result.

The fourth instrument was not a metric but a **reward**: the learning
capability's credit signal, the environment's per-action accept-or-refuse
verdict. The verdict is a well-defined signal and the learner optimised it
exactly as built — and the verdict is not progress. Reconnaissance is accepted
far more often than exploitation, so a learner rewarded on acceptance correctly
concludes that reconnaissance pays, stops attacking, and improves its reward
monotonically while its actual progress collapses. A companion note treats this
failure in full; it belongs in this list because it is the same event in a
different instrument — a measure that tracks something adjacent to progress,
optimised or reported until the adjacency breaks.

One near-miss completes the pattern from the other side: the headline success
metric spent the project's entire early life pinned at zero for both attackers,
because the evaluation's inherited operating point sat in a regime where
neither could complete the objective — a floor indistinguishable from honest
failure until the operating point was moved. That one is a property of the
operating point rather than of an instrument, and has its own note; it is cited
here because it shares the feature that unifies all five: **not one of these
failures announced itself.** A saturated measure returns a clean constant; an
inverted measure returns plausible percentages; a misspecified reward improves
monotonically; a floored metric reports zeros that look like findings. Nothing
crashed. Every failure was found by an active check — a sweep that needed
variance, a cross-examination against the implementation, an ablation arm, a
pre-registered criterion that refused a convenient reading — and on each
occasion the check was the only thing standing between the artefact and the
results chapter.

The transferable claim follows from the pattern, not from any instance. An
instrument validated against one attacker carries no warranty for an attacker
of a different shape, because the validations that matter were implicit: depth
measures assumed failure arrives early, retention measures assumed every
defence contests position, reward signals assumed acceptance tracks progress —
assumptions no one wrote down because the original attacker never tested them.
An evaluation that upgrades its threat model therefore inherits an obligation
it can easily miss: re-validate every measure against the new attacker as if
the measure were new — show it varies, show its sign means what the analysis
assumes, show its optimum coincides with the thing actually wanted — before any
number it returns is reported. On this project's evidence the obligation is not
hypothetical bookkeeping: of the progression measures this evaluation inherited
or first built, *none* survived contact with the new attacker unmodified — and the surveys that
name the attacker model as this field's under-developed half (Cho et al. 2020;
Jalowski et al. 2026) are, read this way, also naming the population of
evaluations about to inherit the obligation. The checks are cheap; any one
silent artefact reaching the record would have cost a false chapter.

The negative scope: this is not an argument that the instruments were badly
built, and not a claim that the pattern's frequency generalises — four failures
on one platform is a case series, not a distribution. What generalises is the
mechanism (implicit validation against the incumbent attacker) and the remedy
(active re-validation on attacker change), both of which are independent of
this simulator.

## Evidence and repo anchors

- Saturation from above (lifecycle depth):
  [`../../implementation/pipeline/ogasp/weight_sensitivity_study.md`](../../implementation/pipeline/ogasp/weight_sensitivity_study.md)
  and the withdrawn recommendation in
  [`../../implementation/apt_model_criterion.md`](../../implementation/apt_model_criterion.md)
  (axis 1, M8b).
- Saturation from below (deepest successfully-actioned stage) and the inverted
  retention measure, including the withdrawn first-pass badge move:
  [`../../implementation/pipeline/ogasp/experiment_02_findings.md`](../../implementation/pipeline/ogasp/experiment_02_findings.md)
  §13, §19; the instrument record:
  [`../../implementation/pipeline/ogasp/measurement_suite.md`](../../implementation/pipeline/ogasp/measurement_suite.md).
- The misspecified reward:
  [`../../implementation/pipeline/ogasp/learning_capability.md`](../../implementation/pipeline/ogasp/learning_capability.md);
  the full argument is the sibling note
  [`learning_without_context.md`](learning_without_context.md).
- The floored headline metric (operating point, not instrument):
  [`../ch4_methods/operating_point_discrimination.md`](../ch4_methods/operating_point_discrimination.md).
- The consolidated measurement-gap disposition at freeze:
  [`../../implementation/pipeline/ogasp/model_scope_freeze.md`](../../implementation/pipeline/ogasp/model_scope_freeze.md)
  §2 (axis 1).
- The surveys cited: extractions
  [`cho2020.md`](../../sources/extractions/cho2020.md) (§V-D) and
  [`jalowski2026.md`](../../sources/extractions/jalowski2026.md) (§4.3).

## Revisit conditions

- If a fifth instrument fails — or, more importantly, if one is shown to have
  failed silently *despite* the active checks — the remedy half of this note is
  weakened and must be restated around what the checks missed.
- If the re-validated measures (the coverage curve above all) later prove to
  carry hidden assumptions of their own, the note's list extends and its claim
  strengthens.
- If a literature survey finds attacker-change re-validation is already
  standard practice in adjacent evaluation fields, the framing shifts from
  proposal to adoption.
