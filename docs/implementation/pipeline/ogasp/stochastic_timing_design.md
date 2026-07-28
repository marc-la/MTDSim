---
status: durable
created: 2026-07-28
topic: "L3 stochastic timing (S3) — the design record: the GSPN formalism, where the clock lives, the per-tactic exponential parameterisation, the confusion-penalty place, the comparability argument against the untouched baseline, and the determinism / migration / rollback scheme. Planning only; no code, test, or data artefact changed."
---

# The stochastic timing regime — design record (S3, planning half)

**Status:** durable design record. It executes the **planning half of S3**
([`supervisor_decision_register.md`](supervisor_decision_register.md) §S3) and is
the **specification** the build half consumes
([`../../../handoffs/2026-07-27_stochastic_timing_implementation.md`](../../../handoffs/2026-07-27_stochastic_timing_implementation.md)).
Every decision below is stated with its rejected alternatives and the reason each
was rejected, so a cold session can build without re-deriving any of it. **No
source file, test, or data artefact was modified to produce this record**; the
current behaviour it rules against was confirmed by a throwaway probe (§0), not by
reading alone.

The one governing constraint, from the supervisor, frames the whole record: **the
numbers are inherently arbitrary, so the justification is the deliverable, not the
values.** This work therefore sits *inside* the existing operational-validation
discipline ([`../../../notes/ch3_design/operational_validation.md`](../../../notes/ch3_design/operational_validation.md))
— the tier badges, the four anti-circularity rules, and shape-not-scale all carry
over; what changes is that a declared value becomes a distribution's **mean**.

---

## 0. State of play — confirmed by probe, and one premise is now stale

The handoff turns on two facts about *today's* movement arm. Both were checked by
running the code (probe at `scratchpad/probe_timing.py`, throwaway), because the
primary metric is a mean over action durations and a wrong reading here would
mis-design the comparability argument.

**Fact 1 — the double charge is real (confirmed).** On the movement arm an
actioned (non-blocked, non-interrupted) step costs the **catalogue dwell** *plus*
the **dispatched verb's native cost**. Measured, no-MTD, over four profiles:
`end_time − start_time − dwell` recovers the verb's native `ATTACK_DURATION`
exactly per verb (`SCAN_NEIGHBOR` 5.0, `BRUTE_FORCE` 20.0, `SCAN_PORT` 25.0,
`EXPLOIT_VULN` mean 13.3 ≈ the complexity-scaled 15), and the dwell charged equals
the catalogue value bit-for-bit (0 mismatches). So **two layers charge time at a
place**: the movement layer's dwell and the substrate's action cost.

**Fact 2 — the inter-arm penalty asymmetry the handoff describes no longer
exists (premise stale).** The handoff's state-of-play says "the movement arm does
**not** pay the simulator's confusion penalty on an MTD interrupt while the
baseline arm does." That was true when the handoff was drafted; it was **closed by
commit `53c5e5d`** (wave-1, *"make the movement arm pay the same price as the
baseline for the same defensive event"*) before this design was picked up. The
probe confirms the current world: under simultaneous MTD, the movement arm pays
**~20.5 t/u of confusion penalty per interrupt, one charge per interrupt** (seeds
0/42/1234: 25/25/26 interrupts → 25/25/26 penalty charges), drawn about the
substrate base `PENALTY = 20`. The same fix also resolved the F1 interrupt-gate
defect ([`action_layer_audit.md`](action_layer_audit.md) §"four decisions", items
B3 and F1). **Consequence for the design:** adding the penalty place must
*preserve* the existing single-charge parity (§4), not *establish* it — the "world
we are in" (per the handoff's decision 4) is the both-arms-pay-once world.

**The structural fact that resolves the double charge into a non-problem (§2/§5).**
The catalogue dwell is consumed as a *separate* `env.timeout(dwell)` in the
movement driver's walk, **before** the verb dispatches; it does **not** write an
`attack_record` row. Only the substrate's `step(verb)` writes `attack_record`, and
it records the verb's *native* cost as the row `duration`. The primary metric —
internal MTTC, the mean over `SCAN_PORT` / `EXPLOIT_VULN` / `BRUTE_FORCE` row
durations ([`../../metrics_semantics.md`](../../metrics_semantics.md) §(a)) — reads
those rows. **So the dwell is invisible to the primary metric today**, and the
double charge is a *wall-clock* double charge, not a *metric* double charge. This
is the hinge the whole comparability argument turns on.

---

## 1. Decision — the formalism: a generalised stochastic Petri net (GSPN), executed not solved

**Ruling.** Adopt **GSPN** semantics: a place's per-tactic dwell is a **timed
transition** with **exponential** firing; the verdict-conditioned routing choice
among a place's out-edges is a **weighted immediate transition** (zero simulated
time). The net is **executed by Monte-Carlo inside SimPy**, exactly as today — the
GSPN is a *vocabulary and a discipline*, **not** a commitment to the CTMC
closed-form solve.

**Why GSPN — how much of the current loop survives.** The runtime is already
structurally a GSPN; the ruling only *names* what it does. The stepping loop
([`../../../../src/mtdsim/l3_simulation/movement/attacker.py`](../../../../src/mtdsim/l3_simulation/movement/attacker.py)
`_walk`) is: **dwell** (`env.timeout`) → dispatch verb → read verdict → compose →
**sample** the next edge → move the token. The *place holds the time* (the dwell),
and the *routing choice among enabled transitions* is already a weighted immediate
selection over the composed out-weights (`_sample`, zero `env.timeout`). Under
GSPN: the dwell **is** the timed transition, the sample **is** the immediate
transition, and `resource-development` (dwell `0.0`) **is** a pure immediate
transition. The change is one line — a constant dwell becomes an exponential draw
— because the loop was GSPN-shaped from the start.

**Rejected — SPN (every transition exponentially timed).** An SPN would put an
exponential clock on the *routing choice* too, replacing dwell-then-sample with a
race of exponentials among enabled out-transitions. That conflates *how long the
tactic takes* with *which edge is taken* — the two things the current design keeps
apart (dwell = time at the place; sample = routing under the outcome overlay). It
is more expressive in a direction we do not need and it dissolves the clean
place-holds-time / edge-is-immediate split. Rejected: buys nothing, costs the
separation.

**Rejected — DSPN / deterministic-and-stochastic hybrid.** A DSPN adds a
*deterministic* transition class (fixed delay). Its natural use is a **periodic**
event — and MTD here *is* periodic (the SDR scheduler fires on a fixed interval),
which is exactly why the closest analytical precedent chose DSPN over SPN
([`petri_feasibility.md`](petri_feasibility.md) §6.3, Mendonça 2023). But the MTD
scheduler lives in the **frozen substrate** (D5/S2), **not** in the movement net;
the net never contains the mutation trigger. The only new duration S3 adds is the
confusion **penalty**, which is a *draw*, not a fixed interval. So the movement net
needs no deterministic transition, and a DSPN would buy fidelity to an event the
net does not model while forfeiting the exponential tractability. Rejected: solves
a problem that lives on the other side of the freeze.

**The relationship to the analytical track, stated so it is not over-read.** The
CTMC / closed-form payoff of an SPN/GSPN ([`petri_feasibility.md`](petri_feasibility.md)
§2) belongs to the **standalone analytical (D1) track**, which is a *separate*
substrate and is **not** what S3 builds. S3's GSPN is the *live* (M1) net, sampled
in SimPy. Adopting GSPN vocabulary keeps the two tracks conceptually aligned (both
are GSPNs; one is solved, one is executed) without claiming the executed net is
analytically solved — the same analytic-vs-executed distinction the feasibility
study already draws.

---

## 2. Decision — where the clock lives (the central ruling)

**The ruling, in one sentence a reader cannot misread:**

> The movement layer owns the **per-tactic behavioural dwell** (an exponential
> draw); the substrate keeps pricing each dispatched action at its **native cost**,
> which is the only time that enters the internal MTTC — so the primary security
> metric is defined identically on both arms, and the behavioural dwell is a
> **separate movement-arm tempo quantity**, never folded into the internal MTTC.

**Consequence for the primary metric (the decisive point).** Internal MTTC is the
mean over the three action-event *durations* in `attack_record`
([`../../metrics_semantics.md`](../../metrics_semantics.md) §(a)). Those durations
are the substrate's native verb costs, written by `step(verb)`, and are **identical
in definition on both arms for the same verb**. The exponential dwell is a
movement-layer `env.timeout` that writes **no** `attack_record` row (§0). Therefore
S3 **does not perturb the primary metric's definition on either arm**, and the
baseline arm — which has no behavioural dwell at all — stays byte-identical. The
dwell shapes the **wall-clock campaign timeline**, which is the
operational-validation target, and it is reported as its own quantity (§5).

**Rejected — "the movement layer owns all time; the verb's native cost is
suppressed."** Three independent constraints kill it. (a) Suppressing the verb cost
means suppressing the substrate's own `env.timeout(ATTACK_DURATION[verb])` inside
`step()` — a change to the **frozen action layer** (S2/D5). (b) It would make the
movement arm's `attack_record` durations diverge from the baseline's for the *same
verb*, breaking the one thing that keeps internal MTTC cross-arm comparable. (c) It
directly contradicts the just-landed wave-1 fix (`53c5e5d`), which *deliberately*
made the movement arm consume the substrate's native costs so both arms pay the
same price for the same action. Rejected on all three.

**Rejected as a *distinct* option — "layers own different things only for
dwell-only places; mapped places keep the substrate price."** This is not a third
position; it is the ruling above, stated for the two place classes. A **mapped**
place already keeps the substrate price (native cost in `attack_record`) *and*
carries the behavioural dwell; a **dwell-only** place (S4) dispatches no verb, so
it writes no `attack_record` row and its *only* time is the exponential dwell. The
ruling covers both without a separate case: the substrate prices whatever action
runs, the movement layer prices the tactic's dwell, and where no action runs the
dwell is the whole cost. Adopted as one rule, not two.

---

## 3. Decision — per-tactic rate parameterisation from the existing catalogue

**Ruling.** Each tactic's current declared `duration_s`
([`../../../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json))
becomes the **mean** of an `Exponential(rate = 1 / duration_s)` draw. The value
magnitudes do **not** change — recalibration is separate work under the validity
framework (out of scope). This preserves **every tier badge, every sweep band, and
the group-anchor structure** that keeps the parameter count identifiable (four
group anchors, not fifteen free dwells — anti-circularity rule 2).

**The zero-duration tactics stay immediate, not exponential.**
`resource-development` (`duration_s = 0.0`, the off-network prep null) becomes a
**GSPN immediate transition**, not an `Exponential(mean 0)`, which is degenerate.
`impact`'s "never-reached for espionage" character stays expressed **structurally**
(the tactic is absent from those objective-nets), never as a zero duration — as the
catalogue already does.

**What the exponential assumes, and where it is weak — stated, not papered over.**
An exponential dwell assumes **memorylessness** (residual dwell independent of time
already spent), a **mode at zero** (the single most probable dwell is ≈ 0), and a
**long right tail** (coefficient of variation fixed at 1).

- **Defensible for the scan- and exploit-shaped tactics**, under a
  retry-until-success reading (memoryless attempts), and defensible **everywhere on
  tractability and precedent** grounds — declare-and-sweep exponential firing *is*
  the surveyed field norm ([`../../../notes/ch2_background/tactic_duration_precedent_survey.md`](../../../notes/ch2_background/tactic_duration_precedent_survey.md);
  Bland 2020, the SPN/CTMC family). Moving to exponential moves this work *towards*
  the precedent, which converts "our timings are arbitrary" from an apology into a
  position the literature already occupies.
- **A poor shape for the low-and-slow group** (`persistence`, `stealth`,
  `command-and-control`, and the slow reading of `exfiltration`). Their defining
  character is *sustained, paced* dwell — probability mass concentrated **around** a
  value — which is the exact opposite of a mode-at-zero exponential, whose most
  likely outcome is a near-instant dwell. A heavier-shouldered distribution
  (gamma / Erlang / lognormal) with the **same mean** would be more faithful: an
  Erlang-*k* is the sum of *k* exponentials and concentrates around its mean as *k*
  grows, which is precisely the "paced, deliberate" behaviour a stealth dwell
  should show. **The honest position is recorded rather than hidden: exponential is
  adopted for tractability and precedent, acknowledged as a poor shape for the
  low-and-slow tactics; a phase-type / gamma upgrade with the same means is the
  declared refinement, deferred.** This is the operational-validation honesty
  discipline applied to the distribution family.
- **One property in the exponential's favour beyond tractability:** memorylessness
  makes the interrupt-during-dwell path clean — after an MTD interrupt cuts a dwell
  short, the residual is distributed identically to a fresh dwell, so no
  partial-service state need be tracked. (This dovetails with the D2 audit fix,
  which corrected an interrupted dwell being recorded as if fully served —
  [`action_layer_audit.md`](action_layer_audit.md) §D2.)

**The sweep gains a second dimension** in any tactic whose *spread* is itself
declared (the operational-validation revisit note anticipates this). Under S3 the
spread is fixed by the exponential (CV = 1); the second sweep dimension opens only
if the phase-type refinement lands. Not built here.

---

## 4. Decision — the confusion penalty as a net place, preserving single-charge

**Ruling.** The confusion penalty becomes an **entered-on-interrupt place** in the
movement net, carrying an `Exponential(mean = PENALTY = 20)` draw — "the same base
duration under the same stochastic regime" (S3). The **penalty duration** is
re-homed from the substrate onto the movement layer; the penalty's **other
consequence — the lost host connection** (B-INT-01) — stays a substrate state fact
the driver still applies.

**Why the split, and why it is clean.** The substrate method
`apply_mtd_interrupt_cost`
([`../../../../mtdnetwork/operation/attack_operation.py`](../../../../mtdnetwork/operation/attack_operation.py))
already carries **two** separable responsibilities, and its own docstring
anticipates S3: *"S3 will re-home the penalty onto the movement layer as a net
place under a stochastic firing regime. When it does, this stays the substrate's
definition and the driver stops calling it."* The two halves are:

1. the **penalty timeout** — `env.timeout(exponential_variates(PENALTY, 0.5))`, a
   *duration* → **moves to the net place**, drawn from the movement layer's
   dedicated timing stream (§6);
2. the **lost connection** — clearing the host cursor on a `network`-layer mutation
   (B-INT-01), a *state* consequence → **stays** with the substrate; the driver
   keeps consuming it.

**The single-charge invariant (the trap to design against).** Because *today* the
movement arm already pays the penalty once per interrupt (§0, Fact 2), adding the
net place while the driver **still** consumed `apply_mtd_interrupt_cost`'s timeout
would make the movement arm pay **twice**. The build must therefore, in one change,
(i) add the penalty place and (ii) stop the driver consuming the substrate's
penalty *timeout* — keeping only the lost-connection call. The guard is the cheap
one the implementation handoff already names: **count penalty charges per interrupt
on both arms; each must be exactly one.**

**The baseline arm is untouched.** It keeps its `_handle_interrupt` →
`apply_mtd_interrupt_cost` path with the substrate's own `exponential_variates`
draw. Only the movement arm re-homes the draw to its net place. The two arms draw
the penalty from **different** streams with the **same mean** (20) — comparability
is by distribution, exactly as it already is for every other stochastic quantity
(the arms were always independently seeded). The penalty, like the dwell, writes no
`attack_record` row, so re-homing it does not touch internal MTTC.

---

## 5. The comparability argument, written before any code

The primary metric is defined over the substrate's action durations, and the
baseline arm must remain byte-identical. Here is how a movement-arm run's timing
composes into that metric under the §2 ruling, and what stays comparable.

**What enters the primary metric — and what does not.** Internal MTTC =
mean over `SCAN_PORT` / `EXPLOIT_VULN` / `BRUTE_FORCE` row durations in
`attack_record`. Those durations are the substrate's **native verb costs**,
identical in definition on both arms. The three time contributions S3 introduces or
re-homes on the movement arm — the **exponential dwell**, a **dwell-only** place's
time, and the **penalty place** — are all `env.timeout`s that write **no**
`attack_record` row. Therefore **none of them enters internal MTTC**, and the
metric's definition and cross-arm comparability are **preserved unchanged** by S3.
(Structural fact, verified in §0.)

**The baseline arm.** No behavioural dwell, no dwell-only places, no net penalty
place — the whole S3 change is movement-arm-only. Its golden headline
(692 records / 41 hosts; internal MTTC on record) reproduces byte-for-byte. This is
the contract with every prior result and it is not touched.

**The second reported quantity — the campaign tempo.** The exponential dwells and
the penalty place shape the movement arm's **wall-clock campaign timeline** — how
long, in simulated time, a profile takes to traverse its net and reach its
objective. This *is* the operational-validation target (shape-not-scale over a
*distribution* of timelines now, not a single one). It is a **movement-only**
quantity: the baseline is a mechanical attacker with no behavioural tempo, so a
wall-clock, dwell-inclusive time-to-compromise is **not** cross-arm comparable —
and that non-comparability is **by design, a finding to state, not a defect**. The
rule for the write-up: report internal MTTC as the cross-arm-comparable primary
metric; report the dwell-inclusive campaign tempo as a **separate, explicitly-named
movement-arm metric**, never on the same axis as the baseline's internal MTTC.

**The honest edge case (carried over, not introduced).** A mutation *during a
dwell-only place's dwell* raises no verdict and is not felt by the token
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §5) — an
acknowledged limitation tied to the H-coupling finding, unchanged by S3.

**Net answer to the handoff's decision-5 question.** Cross-arm comparison **remains
valid on the primary metric** (its definition is untouched); it needs **a second
reported quantity** for the behavioural tempo (the movement-only campaign timeline).
The two arms do **not** stop being comparable on the primary metric — the timing
change lands entirely outside it.

---

## 6. Determinism, migration, and rollback

**Determinism (SIM-05) — a new isolated stream.** Add a dedicated
`_timing_rng = random.Random(derived_seed)` on `MovementAttacker`, where
`derived_seed` is a fixed, reproducible transform of the run seed (e.g. a constant
offset or XOR) so the timing stream is **independent of** both existing streams:
the token sampler `_rng` and the substrate's global `random` / `numpy` dice. The
arms stay independently seedable. The dwell is deterministic-constant today, so
this is a *new* stream, not a re-seat of an existing one — it must not perturb the
sampler sequence (pinnable: with timing draws introduced, the sampler's draw
sequence is unchanged).

**The tests that pin each property** (the build's obligations, named here so the
build does not re-derive them):

1. **Distribution.** Over many seeded draws at a fixed mean, the empirical mean
   recovers the declared mean within a stated tolerance — per group anchor.
2. **Determinism.** The same seed reproduces the same dwell **and** penalty
   sequence exactly.
3. **RNG isolation.** Timing draws neither read nor advance `_rng` or the substrate
   dice — the sampler and verdict streams are byte-identical with timing on vs off.
4. **Penalty single-charge.** Penalty charges per interrupt == interrupts, on
   **both** arms (§4).
5. **Baseline golden byte-identical.** The arm is untouched, demonstrably.
6. **The four seam invariants still pass**
   ([`runtime_verification.md`](runtime_verification.md) §"four seams"): putting
   time on the movement layer must not import SimPy into the controller, nor give
   the net verdict knowledge.
7. **Dwell-only places** (S4 dependency): time advances, no verb fires, no verdict
   is produced, routing falls back to base weights, and the record marks it — the
   behaviour the controller rebuild makes legal, now given its cost.

**Migration.**

- **The catalogue metadata is inverted.** `tactic_durations.json`'s `meta.semantics`
  currently declares *"plain per-state dwell … NOT a stochastic firing rate
  (GSPN/SPN/TPN semantics deferred per D10)"* — the exact opposite of S3. It flips
  to declare **per-tactic exponential firing, `duration_s` = the mean**, and the
  guard test [`tests/l3_simulation/test_durations.py`](../../../../tests/l3_simulation/test_durations.py)
  that asserts the shape is updated in the **same commit** (the implementation
  handoff owns this; it is not a tidy-up afterwards).
- **One seam in `_walk`.** `yield self.env.timeout(dwell)` becomes
  `yield self.env.timeout(self._draw_dwell(place))`; the penalty timeout in
  `_read_interrupt` is re-homed to the penalty place's draw (§4). Wiring at the
  single point where time is taken keeps the change one seam and the revert a
  one-line proposition.
- **The shared-catalogue hazard (the one cross-artefact risk).** The standalone
  **timeline runner** ([`../../../../src/mtdsim/l3_simulation/timeline/walk.py`](../../../../src/mtdsim/l3_simulation/timeline/walk.py),
  the D1 analytical track) also reads `tactic_durations.json`, as a **deterministic**
  dwell under its own SIM-05 discipline. S3 is scoped to the **movement layer
  only**. The metadata rewrite must therefore keep `duration_s` meaning "the mean /
  point dwell", and locate the *stochastic interpretation* as the movement layer's,
  declared there — so the timeline runner keeps reading `duration_s` as a point
  value and its determinism is not falsified. Flag before editing the metadata.

**Rollback.** One seam + the metadata/guard flip. Reverting is: restore the
constant dwell (`_draw_dwell` → identity), restore the substrate penalty
consumption, and revert the metadata `semantics` field and its guard. Cost: **one
function, one data field, one guard test, one metadata block** — low, by
construction, because the change is deliberately confined to the single point where
time is taken.

---

## 7. What the implementation handoff must build (the checklist)

In enough detail that a cold session builds it without re-deriving a decision:

1. **A seeded draw helper + its stream.** `Exponential(mean)` from a dedicated
   `_timing_rng` (§6); mean sourced from the catalogue's `duration_s` (§3);
   `duration_s == 0` → immediate (zero-time), no draw (§3).
2. **The `_walk` timing seam.** Replace the constant dwell with the draw at the
   single point time is taken (§6). Build and test the draw *as a distribution*
   before wiring (test 1) so a statistical bug cannot hide behind an integration
   bug.
3. **Dwell-only places pay time and produce no verdict** — the S4-legal behaviour
   given its cost; distinguishable in the event record (§2, §6 test 7).
4. **The confusion-penalty place** with the duration/lost-connection split (§4) and
   the single-charge guard (§6 test 4). Prove the charge is single on both arms.
5. **The metadata + guard inversion** in the same commit as the behaviour (§6),
   worded to preserve the timeline runner's point-value reading (the shared-catalogue
   hazard).
6. **Re-verify comparability empirically** (§5): the baseline golden reproduces
   exactly; the movement arm's internal MTTC composes only from native verb costs;
   the campaign-tempo quantity is reported separately. If code and record disagree,
   the record wins — or the record's argument had a hole, which is itself a finding.
7. **Update the downstream docs** in the same commit: the duration-regime row in
   [`../../provenance.md`](../../provenance.md), the runtime lifecycle in
   [`success_failure_overlay_design.md`](success_failure_overlay_design.md) §6, and
   the revisit condition in
   [`../../../notes/ch3_design/operational_validation.md`](../../../notes/ch3_design/operational_validation.md).

**Out of scope (from the handoff, restated so the build does not drift):**
re-deriving the per-tactic values (they become means at current magnitudes);
changing the distribution family per tactic beyond the recorded gamma-refinement
*flag*; the reset-fraction parameter family; any change to the baseline attacker's
timing; running experiment 2.

---

## 8. How this connects

- **Executes:** [`supervisor_decision_register.md`](supervisor_decision_register.md)
  §S3 (and lifts the D10 timed-net deferral).
- **Specifies:** the build half —
  [`../../../handoffs/2026-07-27_stochastic_timing_implementation.md`](../../../handoffs/2026-07-27_stochastic_timing_implementation.md).
- **Depends on:** S4's dwell-only tactic set for §2/§3's zero-and-dwell-only cases
  ([`../../../handoffs/2026-07-27_controller_v2_partial_mapping.md`](../../../handoffs/2026-07-27_controller_v2_partial_mapping.md));
  that handoff explicitly defers "what a dwell-only tactic costs" to here.
- **Governed by:** the validity framework
  ([`../../../notes/ch3_design/operational_validation.md`](../../../notes/ch3_design/operational_validation.md),
  [`../../../notes/ch2_background/tactic_duration_precedent_survey.md`](../../../notes/ch2_background/tactic_duration_precedent_survey.md))
  and the comparability boundary
  ([`../../metrics_semantics.md`](../../metrics_semantics.md) §(a)/(d)).
- **Consumes formalism groundwork from:** [`petri_feasibility.md`](petri_feasibility.md)
  §3 (how the field uses Petri nets), §6.3 (the DSPN/CTMC fork on the analytical
  track).
- **Scores against:** [`../../apt_model_criterion.md`](../../apt_model_criterion.md)
  axis 5 (the tempo half of stealth that S3's regime would give the model —
  CONJECTURED there, and this record is its design).
- **Figures:** `data/misc/_viz/stochastic_timing_design_viz.py` →
  `stochastic_timing_*.png` (the four design diagrams: where-the-clock-lives, the
  GSPN place lifecycle, the exponential parameterisation with the honesty overlay,
  and the penalty single-charge design).

## 9. When this would need updating

- If the implementation finds the record under-specified: fix the record first,
  then build (the build has no authority to decide).
- If the phase-type / gamma refinement for the low-and-slow group is taken up: §3's
  distribution-family flag becomes a build, and the sweep's second dimension opens.
- If the S2 freeze lifts such that the verb native cost *can* be re-priced: §2's
  rejection of the "movement owns all time" option is revisited.
- If experiment 2's reader reports a dwell-inclusive time-to-compromise: §5's
  "second reported quantity" must be named and its axis kept distinct from the
  baseline's internal MTTC.
