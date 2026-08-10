---
status: open
created: 2026-08-09
---

# Axis 6, incentive-driven rationality — context only: the row is closed by ruling, two mechanisms returned negatives, and the named future-work route runs into a substrate that will not construct

## What this document is

**Context only.** The approach arrives in the session prompt; Marc brings the
ideas. No recommended approach, no validation gate, nothing commissioned. What it
supplies is what was tried, what each attempt returned, and the bounds already
established — so a proposal lands against the real bar rather than re-deriving a
wall someone already hit.

Sibling context handoff, same date and same purpose:
[axis 7](2026-08-09_axis7_learning_context.md).

## 1. Read this first — the row is closed, by Marc's own ruling

**FINAL DISPOSITION, 2026-08-02:** *"this row is DESIGNED, and that is where it ends
for this project. Its attempted implementations are recorded as negative results and
full incentive rationality is named as future work."* The ruling closes the axis
rather than parking it.

Any proposal here therefore either **accepts the closure** — treating the row as
settled and working on something adjacent — or **deliberately reopens it**.
Reopening is legitimate; doing it by accident is not. §4 states what the reopening
bar actually is, and it is not a mechanism.

## 2. Two mechanisms, both built, both swept, both negative

**The declared-duration utility modulator** (2026-07-29, 1 800 runs). The routing
weight of a destination multiplied by `(u(b)/ū)^λ`, with `u(b)` a declared
per-tactic benefit over that tactic's declared duration. λ declared, never fitted,
swept over its band against six conclusions committed before the sweep ran; at
λ = 0 the mechanism is **bit-identical** to the model without it.

It operates and changes behaviour — visit share moves onto cheap exploit-shaped
tactics, and at the near-greedy band end pooled path entropy collapses from 2.23
bits to 0.24. It changes an outcome in the unflattering direction — blocked attempts
rise from 49 % to 99 %, distinct hosts fall. **What did not reproduce is the result
the axis exists to produce:** MTD's measured effect does not change when the attacker
can see cost.

**The anatomy is the finding, and it is the transferable part.** MTD's tax **is**
strongly differentiated across tactics — an 18-fold spread in interrupt rate — but
it is levied in near-proportion to a tactic's declared dwell, a roughly uniform ~9 %
surcharge. **A normalised utility ratio is invariant to a proportional inflation of
its denominator.** The mechanism cannot see the defence because of the shape of the
defence's cost, not because of a defect in the mechanism.

**The iterated model** (2026-08-02, 4 200 runs). A state-conditioned expected cost
over the declared precondition relation's capability closure, plus a benefit
measuring distance through the profile's own routing net — both derived from
artefacts already on disk, **with no new declared magnitude**.

It repaired the known R2 double-penalty defect measurably: 73–89 % of the
blocked-fraction rise undone in the pooled `v2_partial` cells, successes per action
roughly doubled. **And the badge still did not move, for a reason worth more than
the repair.** U3 — the conclusion written to move this row, taking the earlier
criterion verbatim so verdicts would be comparable — *passes* on the bare threshold.
It also passes for the **`declared` arm**, which was proved by spike to be unable to
see MTD at all: its factor table precomputes to 30/30 bit-identical and the MTD
condition is not among its inputs. **A criterion passed by a negative control is not
measuring the property it tests.** U3 was recorded moved and the row stayed DESIGNED.
The iterated implementation has since been deleted; the shipped model stays, because
it is what the row describes.

**One result from that sweep belongs to axis 3 and is worth knowing.** The
benefit-through-the-net change is the **first modulator configuration this project
has measured that does not narrow traversal** — pooled path entropy *rises* against
the shipped model in 5 of 5 profiles on both mappings, holding 1.008 bits at the
near-greedy band end where the shipped family collapses to 0.655. Half the entropy
collapse attributed to cost-sensitivity turned out to be the price of measuring
value in the wrong graph.

## 3. Why the row closed rather than waited — the substantive reason

The binding constraint stopped being a mechanism, became an **instrument**, and then
became something harder. A time-free successor was designed and cross-examined at
length before being declined, and the reason is recorded against the axis:

**On this substrate the attacker has something to be rational *about* but nothing to
be rational *toward*.** Readiness — whether the next action can run — is real,
state-dependent and conditionable, but it is **competence, not incentive**. Incentive
requires a payoff to weigh, and this attacker has none: it reaches the simulator's
objective **zero times in 1 200 runs**, and the verbs that cause compromise produce
nothing in the capability vocabulary, so nothing is ever banked. A decision rule
built on readiness would be a competence model wearing this row's name.

**Three measured facts bound any future attempt.**

- **The routing limb has little room.** Under the profiles' own nets, `aggregate`
  places every tactic within one hop of an objective, and **14–38 % of decision
  points sit at singleton out-sets** where the renormalised factor is exactly 1.000
  whatever a mechanism computes.
- **The capability channel resolves the whole defence to a two-bit register**, so
  any readiness-derived quantity takes three values and a position-destroying
  mutation moves it by one.
- **The diversity family is unreachable by declaration.** What OS and Service
  Diversity destroy lives outside the guard the capability vocabulary was
  transcribed from, so no legal artefact edit gives it a channel.

## 4. What the reopening bar actually is

The criterion names two requirements, and **both are substrate work, not
movement-layer work**:

1. **An attacker with a payoff it can accumulate and weigh** — on this simulator
   that means a located objective: the database set, or a genuinely targeted
   attacker.
2. **An instrument for MTD-conditional response that a mechanism provably blind to
   MTD cannot pass.** Until one exists this row cannot be moved by *any* mechanism,
   because the evidence bar itself is what fails.

**And requirement 1 collides with a feasibility finding.** The targeted attacker was
spiked, and **the targeted network is not merely unexercised — it is not
constructible**
([`targeted_attacker_feasibility.md`](../implementation/pipeline/ogasp/targeted_attacker_feasibility.md)
§4). Five blockers: the targeted network cannot be constructed on the phase-0
geometry (B1); the shipped geometry makes selection impossible even in principle
(B2); construction is seed-dependent for every geometry (B3); there is no targeted
objective because the termination is commented out (B4); and the targeted *strategy*
has no live code path (B5 — corroborated independently by the intent audit at
IS-SCN-03, which records `get_host_id_priority` and `tag_priority` as never called
from the attack chain). **B1–B5 are all substrate changes, and S2 is the live
constraint on them.**

The one remaining open route the criterion leaves untouched: a defence whose cost is
**not** proportional to dwell — one taxing particular tactics rather than particular
durations, reachable inside experiment 2's defence family at the relaxed interval. It
would be scored by the same statistic, so it inherits the instrument problem above.

## 5. What replaced the mechanism, and what it does not license

A **measurement**, not a mechanism: the attacker-disengagement reader. MTD's economic
claim is that cost rises until the attacker goes elsewhere, and the half this
substrate can carry is the second — an effort-denominated reading of when a run's
projected campaign cost exceeds a reservation, reported as a frontier over patience
rather than at a declared threshold.

Ratified vocabulary, to be used rather than re-coined: **Projected Campaign Effort**
(the trajectory), **Abandonment Effort** `A(k)` (the scalar, never quoted without its
`k`), the **Disengagement Frontier** (the report).

**It is explicitly not a badge move for this row.** It scores an *outcome* — where
the attacker would have quit; the row asks whether the attacker *conditions on* cost.
Its own caveats: the conditional mean conditions on abandoning, and the censoring
fraction moves with the defence where the mean does not; the horizon caps observable
patience, so `k ≥ 7.5` is mostly censored and `k = 10` pins at the horizon in every
condition.

## 6. Constraints that bind any proposal here

- **The row is closed by ruling.** Reopening is a decision to state, not to assume.
- **S2 freeze.** Every route in §4 is a substrate change and sits behind it.
- **The degenerate region.** At 200 s no arm completes the objective; success-shaped
  measures discriminate nothing.
- **A criterion a negative control can pass is not an instrument.** This is the
  axis's own hardest-won lesson; a proposal that reuses the old statistic inherits it.
- **Scores move on evidence only** — never change the model, weights, mapping or
  metrics to improve a row (S6;
  [`../workflows/guardrails.md`](../workflows/guardrails.md)).
- Determinism (SIM-05); envelope-not-actor; Australian English; branch per session;
  commit locally; **never push** without an explicit ask.

## Reading list

- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(d) axis 6 — the whole row, including the R2 qualification, the iterated-model
  block and the FINAL DISPOSITION.
- [`../implementation/pipeline/ogasp/incentive_rationality.md`](../implementation/pipeline/ogasp/incentive_rationality.md)
  — the first mechanism, C3's entropy collapse and the MTD-tax anatomy.
- [`../implementation/pipeline/ogasp/iterated_cost_model.md`](../implementation/pipeline/ogasp/iterated_cost_model.md)
  — the second mechanism, the negative control that passed U3, and change B's
  entropy result.
- [`../implementation/pipeline/ogasp/targeted_attacker_feasibility.md`](../implementation/pipeline/ogasp/targeted_attacker_feasibility.md)
  §4 — the five construction blockers on the named future-work route.
- [`../implementation/pipeline/ogasp/attacker_disengagement.md`](../implementation/pipeline/ogasp/attacker_disengagement.md)
  §1.2 — the ratified vocabulary and what the frontier does not license.

**The transferable method** — how to instrument an axis, extracted from all eight and
roughly 30 000 runs — is
[`axis_instrumentation_method.md`](../implementation/pipeline/ogasp/axis_instrumentation_method.md).
Read it before proposing an instrument, a control or a figure.

## Out of scope for this document

It commissions nothing, sets no gate, recommends no build and expresses no
preference. The approach arrives in the prompt.

## Return format

Default ([`../workflows/session_workflow.md`](../workflows/session_workflow.md#handoff-workflow)):
framed in terms of the thesis and succinct — which claim moves, which criterion row
is affected, what is now sayable. A null or inverted result reports the same way.
