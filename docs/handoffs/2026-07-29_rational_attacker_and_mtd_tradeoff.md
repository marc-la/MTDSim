---
status: open
created: 2026-07-29
---

# Explain the cost model plainly, simplify it to what the proof of concept needs, and pair it with a calibrated disruption metric so the simulation carries MTD's actual trade-off

**Chain position: after
[`2026-07-29_reconcile_stranded_axis_work.md`](2026-07-29_reconcile_stranded_axis_work.md),
which is blocking.** Governed by
[`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md).
Independent of the learning handoff, though both compose on the same seam.

**Two deliverables in one brief, deliberately.** The cost model and the disruption
metric are separable to build and worthless apart. This project has already run
the experiment of shipping a measurement with no decision rule to consume it — the
cost ledger left the axis at NOT ADDRESSED until a rule arrived — and a disruption
metric with nothing to trade against would repeat it in the other direction.

## Part 1 — explain the current cost model plainly, then simplify it

**The first deliverable is an explanation, not a change.** The record that exists
argues the mechanism to an examiner; nothing states in plain terms what the
attacker actually computes and where each number comes from. Write that first, in
one page, because the simplification cannot be judged without it.

What is built today: the routing weight of a candidate tactic is multiplied by
`(u(b) / ū)^λ`, where `u(b) = benefit(b) / cost(b)`, `ū` is the mean utility across
the candidates available at that step, and `λ` is a declared **rationality
exponent** — zero is indifference to cost, and reproduces the model exactly; one is
preference proportional to utility; higher is increasingly greedy. The **cost** term
reuses the declared per-tactic duration catalogue rather than declaring a second
family. The **benefit** term is the one new declared family: rule-generated from how
close a tactic sits to *that profile's own* objective, so it differs between
profiles for the same tactic — the property that keeps it from silently restating
the routing weights' distance kernel.

What the sweep found, and it is the thing to explain honestly: the mechanism
changes behaviour and does not produce the result the axis exists for.
Cost-sensitivity does **not** change MTD's measured effect, because the tax is
levied in near-proportion to each tactic's declared dwell and a *normalised* utility
ratio cannot see a proportional inflation of its denominator. It also costs the
attacker progress — blocked attempts rise from 49 % to 99 % of actions as the
exponent rises, because the cheapest tactics on this substrate are the most
precondition-coupled.

Then simplify, against these questions:

1. **Is the benefit family carrying its weight?** It is fifteen declared cells per
   profile at the floor tier, and the sweep found the cost floor more influential
   than the benefit rule's own shape parameter on four of five profiles. If a
   simpler benefit — objective-band membership as a binary, say — reproduces the
   behaviour, the simpler one is more defensible and cheaper to argue.
2. **Should cost stay as declared duration?** It is the honest reuse, and it is
   also the reason the axis's result did not reproduce, since MTD's tax is
   dwell-proportional and the ratio cancels it. A cost term conditioned on
   *realised* outcome rather than declared time — expected time including the
   attempts that fail — would not cancel, and the axis record already names this as
   one of two routes to a stronger claim.
3. **Is the exponent the right control?** It is interpretable and its zero is an
   exact ablation, which is worth a great deal. Keep unless the simplification
   makes something plainer.

## Part 2 — the disruption metric, calibrated

**The idea.** MTD's real proposition is a trade: mutation raises attacker cost and
imposes defender cost — downtime, disrupted availability, service churn. A
simulation that models only the attacker's half measures one side of a two-sided
decision, and every "MTD works" conclusion it produces is unpriced. Pairing a
calibrated disruption measure with the attacker's cost model puts **cost-of-moving
against risk-of-not-moving** inside one run, which is the trade practitioners
actually face.

4. **Establish what the substrate already exposes before declaring anything.** The
   mutation machinery records per-event mutation data with resource layer and
   timing, a computed execution frequency, currently-running and suspended
   mutations, and cumulative interrupt counts. Some usable form of "service was
   unavailable for this long" may already be derivable; a metric derived from
   existing records is worth far more than a declared one, on the same reasoning
   that made the attacker's confusion penalty a derived quantity rather than a new
   schema field.
5. **Calibrate to the simulator, and say what calibration means.** The measure must
   be dimensionally comparable to the attacker-side cost so the two can be traded
   — the whole point is a ratio or a frontier, not two unrelated numbers. State
   whether it is time-denominated, event-denominated, or normalised, and note that
   under the current timing regime the two arms price time differently, so anything
   time-denominated needs its comparability argued rather than assumed.
6. **Report it as a frontier, not a score.** Across the defence family and the
   mutation-interval dimension, plot attacker cost against defender disruption. A
   mechanism that suppresses the attacker heavily at high disruption and one that
   suppresses it moderately at low disruption are different products, and the
   ranking that experiment 2 produced is silent on which is preferable. This is the
   reporting shape that makes the trade legible.
7. **Do not build a composite score.** Weighting attacker cost against disruption
   into one number requires a declared exchange rate that no source supplies, and
   it would hide exactly the trade-off the metric exists to show. The frontier is
   the deliverable.

**On "the attacker gives up".** It is the right framing for MTD's economic claim
and it is not currently representable — nothing in the model abandons a campaign
on cost grounds, and adding a give-up rule means declaring a threshold with no
source. Two honest options: treat the *measured* collapse in effective progress as
the proxy for disengagement, which the current mechanism already produces; or
declare a threshold openly, tier it as judgement, and sweep it. Rank these in the
record and pick one — do not let a give-up rule arrive unannounced inside the
utility model.

## Validation gate

Done when: the plain-language explanation exists and a reader who has not seen the
mechanism can state what the attacker computes; any simplification is shown to
reproduce or deliberately change behaviour, with the change argued; the disruption
metric is derived from substrate records where possible and declared where not,
with its calibration and comparability stated; the attacker-cost against
disruption frontier is reported across the defence family; and no composite score
exists.

## Hard constraints

- **The exponent's zero stays an exact ablation.** Whatever is simplified, the
  mechanism must still switch off bit-identically.
- **No second cost catalogue.** A parallel family that could drift from the
  durations is worse than no cost model.
- **No declared value chosen because it improves an outcome**, and no give-up
  threshold introduced without being declared, tiered and swept.
- **Do not consume the substrate's own return-on-attack machinery** inside the
  portable layer — cite it as the positioning precedent, as the current record
  does.
- The freeze holds: this refines a built mechanism and adds a defender-side
  measurement. It does not open a new attacker capability.
- Determinism; envelope-not-actor; within-substrate comparability only; Australian
  English; never push.

## Reading list

- `docs/implementation/pipeline/ogasp/incentive_rationality.md` — the mechanism,
  the sweep and §6.6's list of what it does not license. **After reconciliation;
  on `dev` today its verdict section is unwritten.**
- `docs/implementation/pipeline/ogasp/experiment_02_findings.md` §15 — the
  per-mechanism dwell-proportionality result, which locates the condition under
  which cost-sensitivity could matter.
- `docs/implementation/pipeline/ogasp/measurement_suite.md` — the cost ledger this
  consumes, and the derive-rather-than-record precedent for the new metric.
- `docs/implementation/metrics_semantics.md` — the comparability boundary any
  time-denominated measure inherits.

## Out of scope

- Any game-theoretic solve or equilibrium analysis.
- A composite attacker-versus-defender score.
- Changes to the duration catalogue.
- Attacker-side stealth and learning — same seam, different handoffs.
- Dissertation prose.
