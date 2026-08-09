---
status: durable
created: 2026-07-29
updated: 2026-08-06
topic: "The attacker-model scope freeze — the per-axis disposition at freeze time, what each axis would still need, which needs are honest and which would be embellishment; perimeter narrowed 2026-08-02: axes 6 and 7 are out of the freeze and open while their scope is finalised"
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

## 0. Perimeter amendment (2026-08-02) — axes 6 and 7 leave the freeze

**Ruling (Marc, 2026-08-02): the freeze was taken before the scope of incentive
rationality (axis 6) and learning capability (axis 7) was finalised, and those
two rows leave its perimeter.** The record's own history is the evidence: both
axes have been substantially reworked since freeze day — the learner re-keyed
and swept 2026-08-01, the iterated cost model ruled on, built and swept
2026-08-02 — and each amendment has had to argue that it "does not re-open the
freeze". A freeze that must be argued around on every touch is not functioning
as a freeze for those rows; it is functioning as friction on a scope that was
never final.

**What this changes.**

- Axes 6 and 7 are **open**. Their §2 rows read as *status at last update*, not
  as frozen dispositions, and work on them needs no re-open argument against
  this record. The open scope decisions were consolidated in a
  scope-finalisation handoff, which has since been retired: **all nine of its
  items are settled** — items 5 and 7–9 by dated rulings and by evidence
  (2026-08-02), and items 1–4 and 6 by Marc's axis-6 closure the following day,
  which retired the iterated cost model outright. The durable homes are
  [`../../apt_model_criterion.md`](../../apt_model_criterion.md)'s axis-6 row
  (the final disposition, with what was attempted and why the row closes rather
  than waits) and `git log`.
- When their scope is declared final, both rows re-enter the freeze by a dated
  closure amendment here (§6).

**What this does not change.**

- **Axes 1–5 and 8 stay frozen as written.** The preamble's rationale — further
  mechanism buys less than it costs — continues to hold for them.
- **The §4 pin is untouched.** The reported headline configuration runs
  modulators null whatever the open axes decide; that is a claim-integrity rule
  about which arm owns the plurality evidence, not a scope rule.
- **No supervisor-level constraint is touched.** S2 remains the supervisor's
  ruling, cleared per-experiment
  ([`supervisor_decision_register.md`](supervisor_decision_register.md)); the
  no-RL hard constraint, the S6 evidence-only badge rule and the
  scheme-awareness exclusion bind exactly as before. An open scope licenses
  *deciding*, not building past a ruling.

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
| 6 | Incentive rationality | DESIGNED | **X** | **CLOSED 2026-08-02 (Marc).** Scope finalised: DESIGNED is final, both attempted implementations are recorded as negative results, the iterated one is deleted, and full incentive rationality is **future work**. The attacker has something to be rational *about* (readiness) and nothing to be rational *toward* — no payoff is reachable or bankable — so the remaining gap is a measurement one and is answered by the disengagement reader, which scores an outcome and does not move this row. **Re-enters the freeze by this closure** (§0). Reasoning: [`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 6, final disposition. |
| 7 | Learning | DESIGNED | **M** | Freeze the badge. ~~One mechanism could test its hypothesis (§5).~~ **Built and swept 2026-08-01 — the badge held; the gap narrowed from two candidate causes to one (the credit signal).** **Out of the freeze perimeter since 2026-08-02 (§0) — scope open.** |
| 8 | Scheme awareness | NOT ADDRESSED | — | Ruled out of scope. Freeze. **Reason strengthened 2026-08-09:** the three §4.1 primitives stay excluded on timeframe, but Jalowski's §4.3 metric-manipulation route was attempted and **closed on evidence** — triggering is clocked in every arm, and the one metric-reading defence converges to constant-action policies that ignore their state. Badge unchanged; the negative is now measured rather than scheduled. Reasoning: [`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 8, amendment 2026-08-09. |

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

**A second gap opened on this axis 2026-08-01, and it is a *mechanism* gap
rather than the governance one above.** The R2 cross-examination of the benefit
family found a structural defect: cost (declared duration) and benefit
(objective proximity) penalise **instrumental** tactics in the same direction,
so the enabling steps are discounted twice and neither term can express that a
tactic is worth its price because of what it unlocks
([`cost_model_plain.md`](cost_model_plain.md) §2.2a). No declared value repairs
it. The consequence for the record is interpretive rather than numerical — the
sweep's C5 measurement stands, its attribution of the attacker's collapse to
the terrain does not — and the consequence for this freeze is that axis 6's
disposition is now **G + M**, not G alone.

**This does not re-open the freeze, and the reason matters.** §6 re-opens this
record when a ruling lands or a successor takes up a §3 item; a defect found in
a built mechanism is neither, and the freeze's own principle is that a row is
not revisited because it reads badly. What the defect earns is a *ruling
request*, not a build: the remedy is designed in full
([`attacker_disengagement.md`](attacker_disengagement.md), shipped as a reader
2026-08-02) and takes nothing on
its own authority. Note that it would also serve the enabling condition named
above, so one disposition could close both halves of this axis.

**The ruling landed 2026-08-02 (option 4, both changes, three arms, S2 cleared),
the remedy was built and swept, and the disposition above is now `X` rather than
`G + M`** ([`iterated_cost_model.md`](iterated_cost_model.md)). Three things
changed and the badge was not among them.

The **mechanism gap is closed**. The defect is repairable without a new declared
magnitude, and the repair measurably reaches it: the blocked-fraction rise the
shipped model caused is 73–89 % undone in the pooled `v2_partial` cells and
successes per attempted action roughly double. What did not happen is the
per-profile CI separation the pre-registration demanded (3 of 30 cells), so U2 is
recorded moved and the stopping rule was honoured — nothing re-specified, no arm
added, no criterion relaxed.

The **governance gap is closed too**, in the sense that mattered: S2 was cleared
for this experiment and a non-zero λ was reported.

**What replaced both is a measurement gap, and it is the substantive result.**
U3 — the conclusion that would have moved this badge, taking C4's criterion
verbatim so the verdicts would be comparable — was passed on the bare threshold
by the **`declared` arm**, which F6 proved by spike cannot see MTD at all. A
statistic a negative control passes is not measuring the property it tests. U3 is
therefore recorded moved on the same reading C4 is recorded moved on, and the
badge is declined rather than taken. That is the axis's third measurement
failure, and it puts axis 6 in the same position as axis 1: the mechanism runs,
and no instrument in hand can score it.

**One finding travels beyond this axis and is worth the freeze noting.** The
repair inverted its own design's ranking. The brief called change A (expected
cost) the recommended minimum and change B (benefit measured through the
profile's own net) weaker on every axis; A fails and B pays. B recovers 36 % of
the host loss under MTD, doubles successes per action, and — unlike every other
modulator configuration this project has measured — **costs no plurality at all**,
holding 1.008 bits of path entropy at the near-greedy band end where the shipped
family collapses to 0.655. §4's pin is unaffected, since the reported
configuration still runs modulators null; but the standing generalisation that
every modulator narrows traversal now has a measured exception.

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

**Updated 2026-08-01 — the gap is now the credit signal *alone*, and that is a
narrowing.** This section named the credit signal as the gap while §5 named the
representation as the reason the learner is *incapable* rather than merely
untuned. Both were true, and they were not distinguished by evidence. The learner
has since been re-keyed on `(destination tactic, precondition-satisfied?)` and
swept over 4 600 runs against both the ablation arm and the destination-only
learner ([`learning_readiness_findings.md`](learning_readiness_findings.md)). The
representational defect was real and is fixed — breadth at the declared capability
recovers 3.38 → 4.52 hosts, the high-capability collapse is arrested 1.02 → 2.40,
exploitation's share of successes returns from 6.0 % to 9.5 %. And the badge does
not move, because the no-learning arm sits at 4.60 and the repaired learner never
passes it. Representation was necessary and is not sufficient; the credit signal is
the sole remaining requirement.

## 3. What is future work, and for whom

Stated concretely enough that a successor does not have to re-derive it.

1. **A progress-carrying credit signal for the learner** (axis 7). The single
   highest-value item, because it is the one axis whose demonstration would move
   the model's fidelity placement. **Sharpened 2026-08-01:** the representation
   this would have had to be paired with is now built and swept, so this is no
   longer half of a two-part requirement — it is the whole of what remains, and it
   would be built on the readiness key rather than on the marginal one
   ([`learning_readiness_findings.md`](learning_readiness_findings.md) §4).
2. **A stealth state with a consequence** (axis 5) — which realistically means
   integrating the reactive defender first, and fixing the defect on its
   sensitivity path.
3. **The three scheme-awareness primitives** (axis 8), ruled out on timeframe
   rather than on principle. The observation channel exists and is unwired.
   **Note (2026-08-09):** this remains true of the primitives, but *not* of the
   §4.3 metric-manipulation route, which was attempted and closed on measured
   evidence — it needs a defence whose *timing* responds to the attacker, and no
   arm in this pool has one. Future work on that route is a defender question
   before it is an attacker one.
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

**The crossed arm has since run, and the compounding this section assumed does not
happen (2026-08-01;
[`learning_readiness_findings.md`](learning_readiness_findings.md) §6).** Composing
the two built modulators is **sub-additive**: the both-active cell holds more path
entropy than the utility-only cell in all four cells tested, and adding the learner
to the utility modulator recovers most of the breadth the utility modulator alone
costs (2.22 → 4.22 hosts). The mechanism is that the two disagree — a static
declared preference for cheap tactics, which on this substrate are the most
precondition-coupled, against a learned discovery that those tactics fail when
attempted unready.

**The rule in this section is unchanged and the reason for it is corrected.** The
pin never needed the compounding claim: every single-modulator configuration
narrows traversal against the null one, which is sufficient on its own to make the
plurality evidence belong to the modulators-null arm. What is withdrawn is the
inference, not the discipline — and it is withdrawn because it was reasoned rather
than measured, which is the same standard this record applies everywhere else. The
register of factors and their seams is
[`modulator_composition.md`](modulator_composition.md).

## 5. The one mechanism still worth building, and what it is not

An FSM-alignment factor: at places where the mapping dispatches no verb, bias
routing toward tactics whose verb is the host simulator's declared successor to
the attacker's current phase. ~~The full design brief is
`2026-07-29_controller_composition_unification.md`.~~

**Built 2026-08-01, in the shape this section's own §5 argument implied rather
than as the brief described it.** That handoff was folded into the
procedural-rigidity one, which ruled — on the reasoning below, that the alignment
factor's value is that it conditions on the state variable the precondition turns
on — that the signal should **feed the learner** rather than sit beside it as a
static declared bias. What shipped is therefore the substrate's procedural order
transcribed into a declared, versioned controller artefact
(`data/ogasp/controller/precondition_relation.json`) consulted by a learner keyed
on `(destination tactic, precondition-satisfied?)`
([`learning_representation.md`](learning_representation.md),
[`learning_readiness_findings.md`](learning_readiness_findings.md)).

**Read the three "what it is not" claims below with that in mind.** The second and
third stand unchanged — what shipped still responds to the substrate rather than
the defender, and still makes the attacker behave more like the host simulator
expects. The **first is now superseded by the design it argued for**: its headline
("it is not learning — a declared bias from a static lookup") describes the
alternative that was *not* built, while its body is the argument that was acted
on, ending in the sentence the build implements — *the alignment factor **feeds**
the learner a state-conditioned signal rather than substituting for it*. The
representational diagnosis in that body is now measured rather than argued: an
unmet precondition is a deterministic failure, so the marginal the destination-only
learner holds conflates a paying regime with a certain-failure one, exactly as
claimed. It was right, and it is why the shipped mechanism has the shape it does.

**Three things it is not, recorded here because each is a claim someone will be
tempted to make:**

- **It is not learning.** There is no accumulation, no belief, no update from
  experience — it is a declared bias from a static lookup. The model already has a
  learner, and on the learning axis that learner is the stronger mechanism: it
  accumulates, updates from evidence, perishes under mutation, is
  substrate-independent and is ablatable.

  **On procedural rigidity, however, the learner is not weaker — it is
  incapable, and the reason is representational rather than a matter of tuning.**
  Whether an action is blocked depends on *state*: an exploit fails because this
  host has not been port-scanned yet. So the quantity that would have to be learned
  is the success probability of a tactic **conditioned on the attacker's current
  phase-state**. The learner is keyed on the destination tactic alone, so what it
  can represent is the marginal, averaged over every context — and marginalising
  over phase-state discards exactly the variable the precondition depends on. No
  quantity of runs repairs that.

  What it does instead is route around the constraint: unable to learn *exploit
  after scanning*, it learns *exploit fails often* and shifts weight onto the
  tactics that always succeed. That is the observed result — blocked fraction
  falling sharply while exploitation falls to a fraction of its successes and
  breadth collapses — and there is a self-reinforcing loop behind its monotonicity,
  since avoiding exploitation drives the phase-state distribution further from the
  states in which exploitation would have worked.

  An FSM-alignment factor is the opposite shape: it conditions on the current
  phase, which is the state variable the precondition turns on, so it can express
  what the learner structurally cannot. The two therefore do not compete on this
  problem, and the honest framing is that the alignment factor **feeds** the
  learner a state-conditioned signal rather than substituting for it.
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

## 5b. The research direction after the freeze (clarified 2026-07-29)

The freeze fixes the *model*. It does not fix what the remaining sessions work on,
and that direction was ambiguous until this point, so it is recorded here rather
than left in conversation. Four threads, and they are deliberately narrow.

1. ~~**Generalise the learning capability to procedural rigidity, without
   reinforcement learning.**~~ **Shipped 2026-08-01.** The key that can express
   *this tactic pays here* was chosen against ranked alternatives on a measured
   observation budget ([`learning_representation.md`](learning_representation.md)),
   built as `(destination tactic, precondition-satisfied?)` with the substrate's
   precondition guard transcribed into a declared controller artefact, and swept
   over 4 600 runs ([`learning_readiness_findings.md`](learning_readiness_findings.md)).
   It stayed inside the no-RL constraint — no eligibility trace, no discount
   factor, no value function. The representational defect was real and is repaired;
   the badge did not move, because repairing it returns the attacker to the
   no-learning arm rather than past it. **The successor item is thread 1 of §3
   below — the progress-carrying credit signal — and it is now the only outstanding
   requirement on this axis rather than one of two.**
2. ~~**Explain the cost model plainly, then simplify it.**~~ **Shipped
   2026-08-01** as [`cost_model_plain.md`](cost_model_plain.md): the plain
   statement with a worked real decision, and the simplification put to the
   test — the benefit family survived attempted removal against a
   pre-registered bar (31 of 40 cells fail reproduction without it), cost
   stays the declared duration, the exponent stays.
3. ~~**Pair it with a calibrated disruption metric**~~ **Shipped 2026-08-01**
   as the §5 disruption ledger in the measurement suite plus
   [`mtd_disruption_frontier.md`](mtd_disruption_frontier.md): defender-side
   reconfiguration occupancy derived entirely from the substrate's own
   per-mutation records (no declared value), paired with the attacker-side
   account over the full defence family at both intervals, reported as a
   frontier and never as a composite score. Threads 2 and 3 shared a brief
   (`2026-07-29_rational_attacker_and_mtd_tradeoff.md`, retired with thread
   3's ship commit).
4. **Stealth through the one channel that already exists.** Most tactics under the
   current mapping dispatch nothing, which raises dwell; the reactive selector
   chooses mutations from attacker-derived network metrics; so a slower attacker
   changes which mutations fire. This is the only route by which tempo becomes
   consequential, it is inert against time-triggered mutation, and it needs a
   supervisor ruling before anything is built. The brief that carried it retired
   2026-08-06 when its metric half shipped; the route now lives in
   [`stealth_conceptualisation.md`](stealth_conceptualisation.md) §17. **Its
   premise needs restating**: the measured evidence says the profiled attacker is
   not slower per action, so this is a low-*yield* channel rather than a tempo one
   ([`stealth_exposure_metric.md`](stealth_exposure_metric.md) §3).

**What the direction is *for*, since the freeze makes it easy to lose.** None of
these threads is chasing a badge. Threads 1 and 2 refine mechanisms that already
score their axes; thread 3 adds a defender-side measurement that scores no axis at
all; thread 4 is the only one that could move a badge and it is gated on a ruling.
They are here because each sharpens the evaluation, which is what the attacker
model exists to serve.

## 6. When to re-open this record

~~When the outstanding freeze ruling is resolved (axes 6 and 7 both wait on
it);~~ **axes 6 and 7 no longer gate on this clause — they left the perimeter
(§0), and their scope closes through the finalisation handoff rather than
through a re-open.** The record re-opens when a successor takes up any item in
§3; if the reported configuration in §4 changes for any reason; and to take the
dated closure amendment when the axis-6/7 scope is declared final. Not
otherwise — the point of a freeze is that it is not revisited because a row
reads badly.
