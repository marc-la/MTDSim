---
status: durable
created: 2026-07-29
updated: 2026-07-29
topic: "The attacker-model scope freeze — the per-axis disposition at freeze time, what each axis would still need, which needs are honest and which would be embellishment, and the one mechanism still worth building"
---

# The scope freeze — what the attacker model is, and what it is deliberately not

**Status:** durable decision record. It fixes the boundary of the honours
project's attacker model: what is built, what is frozen, what is future work, and
— for each axis of the APT criterion — whether the gap is a *mechanism* gap, a
*measurement* gap, or a *governance* gap. Those three need very different
responses and have been running together.

The freeze exists because the project has reached the point where further
mechanism buys less than it costs. Every remaining axis is blocked by something
that is not "write the code": a missing detection model, an unresolved supervisor
ruling, a saturated metric, or a credit-assignment redesign that is a research
project in itself. Building thin versions of any of them would produce exactly
the half-cooked implementations that make a contribution harder to defend, not
easier.

## 1. What the model is, stated once

A CTI-derived campaign envelope executed as a token walk over per-objective
Petri-net structure, coupled live to an inherited discrete-event MTD simulator
through a controller layer that maps tactics onto the simulator's action
vocabulary. Routing composes three factors — corpus-derived base weights, a
declared outcome overlay conditioned on the simulator's verdict, and an optional
product of declared modulators carrying cost-sensitivity and within-run learning.
The modulator layer's null configuration is bit-identical to the model without
it, which is what makes every capability ablatable rather than merely present.

**What it is not, and this is the load-bearing sentence of the whole project:**
it is not a better attacker. On the substrate it runs against it compromises
roughly a seventh of what the inherited scripted attacker does and reaches the
simulator's objective zero times in 1 200 runs. The contribution has never been
that this attacker wins; it is that an evaluation conducted against it reaches
different conclusions about the defence.

## 2. The per-axis disposition at freeze

The three gap types: **M** = mechanism missing, **X** = measurement missing (the
mechanism exists and no instrument can score it), **G** = governance (a ruling is
outstanding).

| # | Axis | Badge at freeze | Gap | Disposition |
|---|---|---|---|---|
| 1 | Persistence | DESIGNED | **X** | Freeze. The mechanism runs; both candidate metrics failed. |
| 2 | Objective conditioning | DEMONSTRATED | — | Freeze. |
| 3 | Strategic plurality | DEMONSTRATED | — | Freeze, and **pin the composition configuration** (§4). |
| 4 | Adaptivity | DESIGNED | — | Freeze. The ablation is the finding. |
| 5 | Stealth | NOT ADDRESSED | **M + G** | Future work. Blocked three independent ways. |
| 6 | Incentive rationality | DESIGNED | **G** | Freeze, with the enabling condition named. |
| 7 | Learning | DESIGNED | **M** | Freeze the badge. One mechanism could test its hypothesis (§5). |
| 8 | Scheme awareness | NOT ADDRESSED | — | Ruled out of scope. Freeze. |

**Two demonstrated, four designed, two not addressed.** That is the honest final
shape, and it is a stronger position than eight soft passes: every DESIGNED row
carries a *measured negative* rather than an absence, and the two NOT ADDRESSED
rows are ruled exclusions with stated reasons rather than oversights.

### Axis 1 — a measurement gap, not a mechanism gap

The persistence mechanism is built and has run: the campaign structure executes
end to end and the backward-persistence weighting landed and was exercised. What
does not exist is an instrument that can score it. Both candidate progression
measures failed, and both failures are worth recording because they are the third
and fourth times this has happened:

- Deepest-successfully-actioned stage returned **the same value for every run** of
  the comparative experiment. It was itself the replacement for a measure retired
  for saturation, and it saturated for a structural reason — the mapping's
  objective band dispatches no verb, so no verdict can be recorded there and the
  measure is truncated by construction.
- Foothold retention counts footholds **severed** rather than kept, and the
  mechanisms that never sever position produce total apparent retention by the
  absence of any threat to it.

Restricted to the defences that actually contest position, per-foothold retention
at the operating interval is essentially zero. Persistence is therefore not merely
unevidenced but weakly contradicted, and the honest output is the measurement
finding rather than a badge. Building a third metric to chase the badge would be
scoring-driven design; the criterion's own standing constraint forbids it.

### Axis 4 — closed by evidence, not by omission

The verdict-blind ablation arm — the control this axis had never had — ran across
the full defence matrix on identical seeds and no progression measure separated it
from the conditioned arm. Routing on the simulator's verdict is approximately
free. This is a completed negative, not an open question, and it should be
reported as a result rather than carried as a deficiency.

Note that the mechanism proposed in §5 does **not** move this axis, and it would
be tempting to claim it does. Axis 4 is adaptivity to *defender* resistance;
aligning with the host simulator's procedural order is adaptivity to the
*substrate*. Different thing, different axis, and conflating them would be exactly
the embellishment this freeze exists to prevent.

### Axis 5 — three independent blockers, any one sufficient

There is no detection model for a tempo choice to matter against; the movement
layer's modulators are routing-only and the recommended stealth mechanism is
dwell-primary, so it needs a timing hook that does not exist; and the one defender
in the pool that would make tempo consequential is a trained agent deferred to a
later phase, never yet run against this attacker, and carrying a known defect on
the sensitivity path. Four rulings are outstanding on it.

**The value is already banked without the build.** The comparative experiment
measured the contrast the stealth work exists to produce: the profiled attacker
spends 17–43 % of its visits in tactics that dispatch nothing and generates a
fifth to a third of the inherited attacker's observable event rate, against a
baseline whose non-action share is *structurally zero*. That is a stealth-shaped
result the model produces with no stealth mechanism at all, and it is reportable
as characterisation. What is not claimable is a badge, because a tempo with no
consequence is not evasion — which is this axis's own argument.

### Axis 6 — a governance gap with a named enabling condition

The mechanism is built, declared, swept and ablatable, and the result it exists to
produce did not reproduce: cost-sensitivity does not change the defence's measured
effect, because the tax is levied in near-proportion to a tactic's declared dwell
and a normalised utility ratio cannot see a proportional surcharge.

The comparative experiment then located the missing condition. At the operating
mutation interval every mechanism is dwell-proportional; **above it, four of seven
are not**. So a defence whose cost is not proportional to dwell — the condition the
axis's own record named as one of two routes to a stronger badge — exists in the
defence family, outside the interval every prior run used. Acting on it needs one
targeted arm at a non-zero rationality exponent, and that is gated by the
outstanding freeze ruling, not by effort. Recorded as the named next step; not
taken here.

### Axis 7 — the gap is the credit signal, and it is a real research problem

The learner works in the precise sense the axis asked for and in no other: it
drives its own blocked fraction down sharply within runs, monotonically in the
capability, against an ablation arm that barely improves. And compromise breadth
falls as it does so, because the binary routing verdict it updates on is not a
progress signal — reconnaissance succeeds far more often than exploitation, so a
confident learner correctly concludes that scanning pays and stops attacking.

The axis's own record states what would move it: a credit signal carrying
progress rather than the routing verdict, which is a credit-assignment redesign
rather than a parameter change. That redesign is future work. §5 describes the one
cheap experiment that tests its hypothesis without claiming its badge.

## 3. What is future work, and for whom

Stated concretely enough that a successor does not have to re-derive it.

1. **A progress-carrying credit signal for the learner** (axis 7). The single
   highest-value item, because it is the one axis whose demonstration would move
   the model's fidelity placement.
2. **A stealth state with a consequence** (axis 5) — which realistically means
   integrating the reactive defender first, and fixing the defect on its
   sensitivity path.
3. **The three scheme-awareness primitives** (axis 8), ruled out on timeframe
   rather than on principle. The observation channel exists and is unwired.
4. **Reworking the inherited attacker's phase layer.** The model's ceiling is not
   its own: the host simulator's six-verb action vocabulary and rigid phase order
   bound how much fidelity any attacker driving it can express. A finer-grained
   attacker sitting above the same six verbs gains sequencing resolution and no
   behavioural resolution.
5. **Technique-level execution.** The upstream graph is already technique-grained;
   the execution layer coarsens it to tactics. Re-expanding is a net-construction
   and mapping change rather than an architectural one — but the mapping is the
   acknowledged weak input, and expanding it multiplies the number of declared
   cells without a principled rule to fill them. Cheap architecturally, expensive
   epistemically.

## 4. The composition configuration is part of the freeze

A subtle risk that is easy to miss. **Axis 3's demonstrated badge was earned with
the modulators off.** Both built modulators narrow traversal — the learner reduces
path entropy in every profile-and-mapping cell tested, and rising cost-sensitivity
collapses it severely. If the model's reported configuration ships with either
modulator active, the plurality evidence was measured on a different model than the
one being described.

The freeze therefore fixes the **reported configuration**, not just the code: the
headline arm runs with modulators null, and any modulator-active arm is reported
as its own labelled arm with its own plurality figure. This is a claim-integrity
rule, not tidiness.

The same reasoning bars a further composition that has never been run: the three
modulator families have never been exercised *together*, and the stealth design
record already warns that a slower attacker makes every tactic look more expensive,
which is either an emergent coupling or a hidden double-count. No combined
configuration is claimed at freeze.

## 5. The one mechanism still worth building, and what it is not

An FSM-alignment factor: at places where the mapping dispatches no verb, bias
routing toward tactics whose verb is the host simulator's declared successor to
the attacker's current phase. The full design brief is
[`../../handoffs/2026-07-29_controller_composition_unification.md`](../../handoffs/2026-07-29_controller_composition_unification.md).

**Three things it is not, recorded here because each is a claim someone will be
tempted to make:**

- **It is not learning.** There is no accumulation, no belief, no update from
  experience — it is a declared bias from a static lookup. The model already has a
  learner, and it is stronger than this.
- **It is not axis 4.** It responds to the substrate, not to the defender.
- **It is not a fidelity improvement.** It makes the attacker behave more like the
  host simulator expects, which is the opposite of behavioural independence.

**What it is** is an instrument. Its strength is a dial running from pure
CTI-derived order to the host's native procedural order, and sweeping that dial
measures how much a simulator's procedural rigidity penalises a differently-shaped
attacker. That converts the coupling finding — currently a categorical observation
that walking CTI order manufactures failure the inherited attacker never meets —
into a measured quantity, on the project's own substrate, with a null arm that
reproduces the finding at full strength. It is the instrument for the
methodological claim rather than a capability for the scorecard, and it should be
justified, reported and named that way.

## 6. When to re-open this record

When the outstanding freeze ruling is resolved (axes 6 and 7 both wait on it);
when a successor takes up any item in §3; and if the reported configuration in §4
changes for any reason. Not otherwise — the point of a freeze is that it is not
revisited because a row reads badly.
