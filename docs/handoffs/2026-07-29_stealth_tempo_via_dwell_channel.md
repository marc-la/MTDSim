---
status: open
created: 2026-07-29
---

# Make stealth consequential through the one channel that already exists — dwell alters the network metrics the reactive selector reads, so a slower attacker changes which mutations fire

**Chain position: unblocked 2026-08-01** — the stranded-axis reconciliation it
waited on landed on `dev` that day and its handoff was deleted with it. What
still gates this brief is the supervisor ruling named below, not a dependency.

**Its case strengthened 2026-08-01, from an unrelated direction.** The cost-model
cross-examination established that under *time-triggered* mutation an attacker
minimising declared duration is already, mechanically, minimising expected
mutation encounters — the correlation between a tactic's declared cost and its
interrupt rate is Spearman 0.87. So on a clock, patience is pure exposure with no
compensating benefit, and any rational attacker is a fast attacker. That makes
the anti-APT incentive a property of *time-triggered* MTD rather than of the
attacker model, and it means **a reactive defender is the only channel through
which slowness can ever be rational here** — which is exactly this brief's
thesis. Reasoning:
[`../implementation/pipeline/ogasp/cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md).

Governed by
[`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md),
which currently lists stealth as future work — **this handoff is the argument for
moving it back inside the freeze**, and it should be read as a proposal that the
supervisor rules on rather than as sanctioned work.

**Sibling, unblocked, opened 2026-08-04:**
[`2026-08-04_stealth_exposure_metric_reader.md`](2026-08-04_stealth_exposure_metric_reader.md)
builds the cheaper option 1(a) — a post-hoc detectability *reader* with no
mtd_ai integration and no ruling gate — independently requested in that day's
supervisor meeting. Do that one first; it does not discharge this handoff's
1(b) ruling.

## State of play

**The blocking premise has an exception, and it was verified in code.** The
standing reason stealth is not addressed is that there is nothing to be stealthy
against: no detection model, no alert, IDS culled by project direction. That
premise is too strong for exactly one defender in the pool. The reactive selector's
decision state is assembled from **attacker-derived** quantities — host compromise
ratio, attack success rate, mean time to compromise, return on attack, risk, and
the attacker's current phase — with defender-side and topology features sitting
alongside them but not carrying the signal.

**So the channel is indirect and it is already open.** A slower attacker generates
fewer attack events per unit time, which changes the network security metrics the
selector reads, which changes which mutation it chooses. No new detector is built,
no new coupling is invented, and the reactive agent runs unchanged.

**The tempo exists already and is large.** Under the current mapping seven of
fifteen tactics dispatch no verb at all: they consume their drawn dwell and fire
nothing. Measured, the profiled attacker spends between 17 % and 43 % of its visits
in those non-action tactics and generates roughly a fifth to a third of the
inherited attacker's observable event rate, against a baseline whose non-action
share is **structurally zero**. The model has its tempo axis; what it has never had
is a consequence attached to it.

**The honest boundary, and it decides what may be claimed.** Against the reactive
selector a quieter attacker **starves** the defender's signal — it is not evading
detection, because nothing is detecting. That distinction is why the design record
proposes splitting the axis into tempo (5a, evidenceable) and evasion (5b, no
referent), and the split should be settled before any run, not after.

## The four things this needs, in order

1. **A ruling.** Sanctioning the reactive defender as an experimental arm is a
   supervisor decision, because that agent is a trained network deferred to a later
   phase by standing project direction. It is also the only route to a demonstrated
   claim on the tempo half. Ask before building.
2. **An integration that does not exist.** The movement arm has never been run
   against the reactive selector at all — there is no reference to it anywhere in
   the L3 run wiring, which constructs the time-triggered mutation operation
   directly. This is the real cost of the handoff and it should be scoped honestly
   before the mechanism is designed.
3. **A defect fixed on that path.** The conformance audit records that any attacker
   sensitivity below 1.0 raises an unbound-local error, so the documented
   sensitivity experiment cannot currently run. Whether it is fixed or the arm runs
   only at sensitivity 1.0 is a decision, not an oversight to discover mid-run.
4. **A dwell-scaling hook.** The modulator seam is **routing-only** — it multiplies
   destination weights. The timing source observes each draw and delegates it
   unchanged, so there is currently no way for a declared state to scale a dwell.
   A dwell-primary stealth mechanism needs that hook, and adding it is a seam
   change rather than a new modulator.

## Recommended approach

5. **Prefer the cheapest form that tests the claim.** Before building a stealth
   state at all, run the profiled attacker against the reactive selector **as it
   is**. The profiles already differ in non-action share by more than a factor of
   two, which is a naturally-occurring tempo spread. If the selector's mutation
   choices do not differ across that spread, a declared stealth dial will not
   rescue the claim, and the cheap run has saved the expensive one. If they do
   differ, that is the demonstration, obtained with no new attacker mechanism.
6. **Only then declare a stealth state**, if the cheap run justifies it: a within-run
   scalar that rises on visits to non-action tactics and decays on noisy actions,
   scaling dwell means by an ordinal exposure rule. The corpus carries no per-tactic
   detection probability anywhere — checked across all fifteen tactic profiles — so
   the rule can only be ordinal, and three of its placements are judgement calls
   with no supporting quote and should be the first thing a sweep perturbs.
7. **Report the mutation-choice distribution, not just the outcome.** The claim is
   that tempo changes *what the defender does*. Show the selector's chosen-technique
   distribution against attacker tempo; a breadth difference alone would leave the
   mechanism unidentified.
8. **Never wire the attacker's stealth level into the defender's sensitivity
   parameter.** That is reverse-modelling detection and extending the inherited
   reactive machinery, both ruled out. The coupling must stay indirect: tempo
   changes the record, the record changes the state, the state changes the choice.

## Validation gate

Done when: the supervisor ruling is recorded; the cheap run in (5) has been done and
reported whichever way it fell; the tempo/evasion split is settled and the criterion
edited only if a pre-registered criterion was met; any declared magnitudes are
tiered and swept; the mutation-choice distribution is reported against tempo; and a
tracked record exists.

## Hard constraints

- **Time-triggered MTD is unaffected by tempo, and the write-up must say so.** Any
  stealth claim is bounded to the reactive arm; against the rest of the defence
  family a slower attacker simply absorbs more mutations.
- **A stealth claim is a tempo claim.** Evasion has no referent here and 5b stays
  not addressed; conflating them would annex the smart-attacker work that belongs
  to the learning and scheme-awareness axes.
- **The reactive agent runs unchanged** — replicate, never extend.
- **Do not compose stealth with the cost model until each is validated alone.** A
  slower attacker makes every tactic look more expensive, which is either an
  emergent coupling or a hidden double-count, and nobody has looked.
- Declared magnitudes are ordinal-grounded, tiered and swept; determinism;
  envelope-not-actor; Australian English; never push.

## Reading list

- `docs/implementation/pipeline/ogasp/stealth_conceptualisation.md` — the three
  candidate semantics, the verified reactive-selector finding, the ordinal exposure
  rule, and the four-item decision request.
- `docs/implementation/pipeline/ogasp/experiment_02_findings.md` §16 — the measured
  tempo contrast this builds on.
- `docs/implementation/intent_conformance_audit.md` — the defect on the sensitivity
  path, and the reactive arm's other recorded divergences.

## Out of scope

- Building a detection model or an IDS.
- Extending the reactive agent, or wiring stealth into its sensitivity parameter.
- Any claim about detection-evasion.
- Dissertation prose.
