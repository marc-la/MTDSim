---
status: durable
chapter: ch3_design
created: 2026-07-04
updated: 2026-07-13
lineage: 2026-07-04_operational_validation_the_bar.md
---

# Operational validation is the bar — how unobservable per-tactic durations are allowed to be defended, and the claim they license

## Position in the dissertation

The methodology chapter's validity argument for the timing layer: the standard of evidence each per-tactic duration must meet, and what the calibrated catalogue is and is not allowed to claim. Written before the numbers existed, deliberately, so they could not be back-rationalised.

## The idea

A discrete-event simulation needs a time on every attacker state, and this project assigns each MITRE ATT&CK tactic a dwell. For scan- and exploit-shaped tactics the inherited simulator already prices the action, so those values are input-validated by inheritance. The difficulty is the stealthy, low-and-slow tactics — persistence, concealment, command-and-control, execution, exfiltration — which have no native simulator action and no isolated observable in the literature. Nobody publishes "how long defence evasion takes", because it is not a measurable property of the world; it is a micro-parameter of a model. Such values cannot be input-validated, since no ground-truth input exists to match. This is not a defect of this model — it is the generic condition of every mechanistic simulation with unobservable internals. The unglamorous truth is that these numbers are estimated and then tuned so the emergent campaign timelines resemble what breach reporting says real campaigns look like. Left unnamed, that reads as fitting the answer, and a reviewer kills it. Named, it is a recognised simulation-methodology strategy — and naming it converts the weakest-looking part of the executable model into a defensible methodological contribution.

### The bar: validate the output, not the input

The recognised answer is **operational validation** (Sargent's simulation-validation taxonomy) — in the agent-based-modelling literature, **pattern-oriented modelling** (Grimm et al.): when a model's internal parameters cannot be measured directly, calibrate them so the model's *observable output* reproduces observed real-world patterns, then report the sensitivity of the conclusion to those parameters. Here the unobservable dwells are the free parameters, and the observable is the campaign-timeline shape — dwell time, breakout time, time-to-impact — which breach reporting does publish. Every duration in the catalogue is badged with one of three validity tiers, in descending strength, and the badge *is* the validity claim:

1. **Input-validated (Tier 1)** — fixed by the inherited simulator's own pricing. Never tuned; these are the anchors.
2. **Output-validated / calibrated (Tier 2)** — a free parameter chosen so the emergent timeline reproduces a literature-reported campaign pattern it was fitted to. Defensible, but weak alone (see circularity, below).
3. **Face-valid and swept (Tier 3)** — no calibration target exists even at the macro level; the value is a stated estimate with a written justification and a declared sweep range, and the conclusion is shown robust across the range.

### Four rules that keep calibration from becoming circularity

"We tuned durations to match literature timelines, and behold — our timelines match the literature" is circular if presented as validation. Four cheap disciplines convert it into a genuine, if modest, claim; they are the difference between a method and a fit:

1. **Never tune the anchor.** Tier-1 simulator-priced values stay fixed; calibration moves only the non-native tactics.
2. **Group, don't free-fit.** Tune a small number of timing-group anchors (scan-shaped, exploit-shaped, stealth, objective-execution) rather than fifteen independent dwells. Fewer free parameters against the same targets is less overfit and more identifiable — and each tactic's group membership is a *qualitative* claim the behavioural literature can support even where numbers do not exist.
3. **Hold out an observable.** Calibrate on one pattern (dwell-time shape), then check that a different, untargeted pattern (breakout-time shape) emerges approximately right. One held-out pattern is the difference between fitting and predicting.
4. **Keep the claim modest.** The output is "plausible, literature-bounded, sensitivity-swept" — never "a validated APT timing model".

### Shape, not scale

The calibration is deliberately of **timeline shape** — orderings and ratios — not absolute duration. The simulator prices actions in tens to hundreds of simulated seconds; the literature's observables run from hours to months. Both cannot be satisfied: if persistence dwelt for literature-months while an exploit took simulator-seconds, the campaign would degenerate into pure stealth dwell and the defence comparison would die, along with comparability to the inherited baseline attacker. So the literature supplies *relative* structure (for example, "stealth dwell is orders of magnitude longer than an exploit action"), absolute scale stays anchored to the simulator's native values, and the calibrated claim is that the emergent timeline *shape* reproduces reported campaign structure — never its absolute length. This is also the only honest claim available, since the simulated network is synthetic and absolute realism was never on offer; and it suffices for the thesis's punchline, which is itself a ratio game between mutation interval and tactic dwell.

Project supervision has since ratified this stance in writing (July 2026), and the ratification sharpens it in three ways. First, timing-specific literature is not expected to exist, and practical incident reporting is the sanctioned qualitative source — the directive "observations are long-term, execution is very quick" is itself a ratio claim, exactly the relative structure this section says the literature supplies. Second, calibration is sequenced *after* the working pipeline: the durations proceed as declared, swept estimates for the MVP, and their justification against practical reporting is a post-MVP verification step, not a precondition. Third, simulation settings (horizon, mutation intervals) are experimental design variables that may be set to suit the experiments, which formally dissolves the residual worry that the model's timeline scale must be reconciled with the inherited simulator's run length. None of this relaxes the tier badges or the four anti-circularity rules — the pre-registration ordering in particular survives the re-sequencing: acceptance criteria are still committed before any scoring is looked at, whenever that scoring happens.

One boundary keeps a related confusion out: the prohibition on taking timing from the incident-flow corpus concerns the corpus's *observation counts* (how often analysts drew a step — a recurrence measure, not a rate). It does not forbid using breach-report *statistics* (dwell, breakout, time-to-ransomware) as calibration targets; those are exactly the observable patterns operational validation calibrates against.

### Why this is a contribution, not an apology

The precedent survey (background chapter) confirms that no prior work assigns justified per-tactic durations, and that the field norm for timed adversary models is to declare rates and sweep them — with face-validation of declared structure as accepted practice (Bland et al. 2020; McQueen et al. 2006; the MAL/SPN/CTMC modelling family, with Madan et al. 2004 as the landmark that a mean-time result can depend only on the sojourn means — the licence behind shape-not-scale). Tier 3 is therefore not a concession but exactly what the field already does, and calibrating declared values to macro observables goes a step *further* than the norm. The honest framing throughout matches the project's governing claim: behavioural *fidelity changes the answer* — never "the model is true".

## Evidence and repo anchors

- The gap and precedent evidence: [`../ch2_background/tactic_duration_precedent_survey.md`](../ch2_background/tactic_duration_precedent_survey.md); extractions [`timed_attack_models`](../../sources/extractions/timed_attack_models.md), [`bland2020`](../../sources/extractions/bland2020.md), [`mcqueen2006`](../../sources/extractions/mcqueen2006.md), [`ling2023`](../../sources/extractions/ling2023.md).
- The catalogue this note is the validity rationale for: [`../../../data/ogasp/tactic_durations.json`](../../../data/ogasp/tactic_durations.json); its evidence layer is [`tactic_profiles/`](tactic_profiles/).
- Governing spec boundaries: [`../../implementation/metrics_semantics.md`](../../implementation/metrics_semantics.md) §(d)/§(f) (comparability; observation counts are not rates); duration-regime provenance in [`../../implementation/provenance.md`](../../implementation/provenance.md) and [`../../implementation/architecture.md`](../../implementation/architecture.md).
- The July-2026 written ratification (R1 timing regime, R4 free simulation settings): [`../../implementation/pipeline/ogasp/supervisor_decision_register.md`](../../implementation/pipeline/ogasp/supervisor_decision_register.md).
- The ratio-game punchline this suffices for: [`structure_to_behaviour_binding.md`](structure_to_behaviour_binding.md).

## Revisit conditions

- If the simulator adopts real (NVD) CVEs, more tactics become input-validated and the calibrated surface shrinks.
- If a precedent assigning justified per-tactic durations surfaces, the gap statement weakens and this note reframes as positioning.
- If the sweep shows the conclusion is *not* robust to the declared durations, operational validation has failed for this model; the note is rewritten around the negative result (see [`../ch5_evaluation/evaluation_burden.md`](../ch5_evaluation/evaluation_burden.md)).
- ~~If the supervisor rejects shape-not-scale in favour of absolute-time realism, the time-scale clash re-opens.~~ **Closed 2026-07-10:** the written feedback ratified shape-not-scale (rulings R1/R4 in the decision register — practical reports as the qualitative source; simulation settings as free experimental variables). The condition would only re-open if that ruling were reversed.
