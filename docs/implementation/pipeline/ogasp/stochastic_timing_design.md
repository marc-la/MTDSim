---
status: durable
created: 2026-07-28
topic: "L3 stochastic timing (S3) — the design record (BUILT 2026-07-28): the GSPN formalism, where the clock lives (the movement layer supplies the time, SimPy spends it), the per-tactic exponential parameterisation, the ruling that the confusion penalty STAYS substrate-side on portability grounds, the comparability argument against the untouched baseline, and the determinism / migration / rollback scheme. Written as planning only (no code, test, or data artefact changed to produce it); the build it specifies landed on 2026-07-28 and is recorded in the banner below."
updated: 2026-07-28
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

> **§2's central ruling was REVERSED by Marc on 2026-07-28, after the first build.**
> The version below — the movement layer supplies the tactic dwell, each dispatched
> action *additionally* keeps its native substrate cost — is superseded. The ruling
> now in force, **S3-R**:
>
> > **The movement layer supplies every unit of the attacker's time.** A tactic's
> > draw *is* the dispatched action's duration, imposed on whatever verb the mapping
> > invokes; the substrate's own `ATTACK_DURATION` and `exploit_time` are no longer
> > consumed on the movement arm. Every place visit costs its tactic's time — the
> > action ran, the action was blocked, or the place dispatches nothing. The MTD
> > confusion penalty is the sole exception and stays substrate-side (§4 unchanged),
> > because it models what a *defender* does to an attacker rather than what the
> > attacker does.
>
> **Why the reversal, in Marc's terms.** The hybrid put two pricing authorities on
> one action. The movement layer is meant to be liftable onto another simulator, and
> a duration that lives in MTDSim's constants cannot travel with it — so a portable
> layer that nonetheless depends on the substrate to price its actions is not
> portable. The same argument that keeps the confusion penalty *inside* MTDSim (it
> is the simulator's model of thwarting) keeps action timing *outside* it (it is the
> attacker's behaviour). §2's ontology section was already right about where time
> lives; the hybrid contradicted it.
>
> **The objections §2 raised against this option, and their disposition.** Two are
> answered and one is accepted rather than answered. (a) *It changes the frozen
> action layer.* It does not: the native FSM prices its verbs in
> `_execute_attack_action`, a separate function from the driven `step()`, and the
> exploit core already branches on `driven`. The native path is untouched and its
> golden reproduces. (b) *It contradicts the wave-1 fix `53c5e5d`.* It does not:
> that fix made the movement arm pay the **confusion penalty**, which S3-R keeps
> exactly as it is. (c) *It breaks internal MTTC's cross-arm comparability.*
> **Accepted, and overruled on purpose.** Marc's ruling: internal MTTC is a metric
> baked into MTDSim and belongs inside it; the movement layer supplies timings and
> does not own the substrate's metrics. Comparability with prior published numbers
> is explicitly not a goal — a faithful comparison, when wanted, is obtained by
> running prior work on the final simulator rather than by holding this model's
> metrics still. **§5's comparability argument is therefore withdrawn, not
> repaired.**
>
> **What the reversal changed in the code:** `step(verb, duration=...)` charges the
> supplied time instead of `ATTACK_DURATION[verb]`; the driven exploit path charges
> once for the action rather than per vulnerability; a blocked attempt now consumes
> its tactic's time where it previously consumed none; and one consequence to note —
> since the exploit core's per-vulnerability pricing is what expressed the complexity
> scaling, the OS-mismatch multiplier and the per-instance re-exploit discount
> (ATK-04), all three are now inert on the movement arm. They remain live on the
> native arm.

> **Built, 2026-07-28 (first build, under the now-superseded §2).** The draw
> ([`movement/timing.py`](../../../../src/mtdsim/l3_simulation/movement/timing.py)),
> the single `_walk` timing seam, the catalogue metadata inversion, and the
> docstring correction §4 called for. Four things the build found, recorded here
> because §9 says a hole in the record is itself a finding:
>
> 1. **§5's golden figure was stale.** The record says the baseline arm's golden
>    headline is "692 records / 41 hosts". The no-MTD golden was intentionally
>    re-baselined to **1541 records / 41 hosts** by the vulnerability-contagion fix
>    ([`../../../../baseline/CHANGELOG.md`](../../../../baseline/CHANGELOG.md)); the
>    host count is unchanged. The *claim* was verified against the live golden and
>    holds — the baseline arm reproduces byte-for-byte.
> 2. **Single-charge needs a one-event tolerance.** The penalty is charged exactly
>    once per interrupt, but a run can end with one charge *in flight*: the horizon
>    cuts the simulation mid-penalty, so the charge is consumed and its event never
>    reaches the record. Measured at one seed of eight (112 charges against 111
>    recorded interrupts, the excess contributing ~2.4 s of a ~20.5 s draw before the
>    clock stopped). The guard permits that single in-flight charge and nothing more.
> 3. **§7 item 3 was already discharged.** Dwell-only places already consumed time,
>    dispatched nothing, raised no verdict and were distinguishable in the record —
>    the controller rebuild landed that. What S3 added is that their time is now a
>    draw, which matters more for them than for anyone else: a dwell-only place's
>    dwell is its *entire* cost.
> 4. **Internal MTTC is unmoved, measured rather than argued.** Across four seeds the
>    movement arm's mean per-action duration is 14.75 s before the regime change and
>    14.79 s after, and on the shared prefix of a no-MTD walk the substrate's
>    per-action costs are identical event for event.

The one governing constraint, from the supervisor, frames the whole record: **the
numbers are inherently arbitrary, so the justification is the deliverable, not the
values.** This work therefore sits *inside* the existing operational-validation
discipline ([`../../../notes/ch4_methods/operational_validation.md`](../../../notes/ch4_methods/operational_validation.md))
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
B3 and F1). **Consequence for the design:** the "world we are in" (per the
handoff's decision 4) is the **both-arms-pay-once** world, so the penalty needs no
build at all — which, with the portability argument, is why §4 rules it stays
substrate-side.

**Fact 3 — two different quantities are both called "MTTC", and they differ by
~26×.** This is the finding that drives §2 and §5, and it was not visible from the
handoff. The project has **two** metrics under one name:

| | **Internal MTTC** | **Time-to-compromise (elapsed)** |
|---|---|---|
| Definition | mean *duration* of the `SCAN_PORT` / `EXPLOIT_VULN` / `BRUTE_FORCE` rows in `attack_record` ([`../../metrics_semantics.md`](../../metrics_semantics.md) §(a)) | sim-clock time at which the first compromise lands |
| Answers | "what does one attack action cost?" | "how long until this attacker breaks in?" |
| Golden value (no-MTD) | **9.11 s** (`evaluation.json`, last checkpoint) | — |
| Experiment 1 reported | *not reported* | **238 s** baseline · **5294 s** movement |
| Does the tactic dwell enter it? | **No** — the dwell writes no `attack_record` row | **Yes** — it advances the shared sim clock |

Verified: the movement reader's `mttc` is `first_compromise_time()`
([`statistics.py`](../../../../src/mtdsim/l3_simulation/movement/statistics.py)),
and the baseline arm's is `float(compromised_rows.iloc[0]["finish_time"])`
(`data/results/exp01_movement_vs_baseline/run_experiment.py:101`) — **both elapsed
sim time, identical in definition on both arms**, exactly as the experiment-1 setup
table claims. Neither arm's reported number is the internal MTTC of
`metrics_semantics.md` §(a).

**The consequence, and it inverts an earlier draft of this record.** The
per-tactic dwell **does** feed the metric the experiments actually compare on,
because it advances the same SimPy clock both arms are measured against. It does
*not* feed internal MTTC, because that is a mean over per-action durations and the
dwell is not part of any action. So the timing regime is **not** invisible to the
headline — it lands squarely on it. §2 rules on this and §5 argues it.

**A flag, not a change (scope discipline).**
[`../../../workflows/project_context.md`](../../../workflows/project_context.md)
and [`../../metrics_semantics.md`](../../metrics_semantics.md) §(a) both name
**internal MTTC** the primary metric, while every head-to-head comparison run to
date reports **elapsed time-to-compromise** under the same name. That is a
nomenclature collision in the canonical specs, and reconciling them is Marc's call,
not this record's. What this record does is refuse to add to it: §2 and §5 name the
two quantities distinctly and never write bare "MTTC".

---

## 1. Decision — the formalism: a generalised stochastic Petri net (GSPN), executed not solved

**Ruling.** Adopt **GSPN** semantics: a place's per-tactic dwell is a **timed
transition** with **exponential** firing; the verdict-conditioned routing choice
among a place's out-edges is a **weighted immediate transition** (zero simulated
time). The net is **executed by Monte-Carlo inside SimPy**, exactly as today — the
GSPN is a *vocabulary and a discipline*, **not** a commitment to the CTMC
closed-form solve.

**Where the time actually lives — the ontology, stated precisely (Marc,
2026-07-28).** The timing does **not** live *on* the Petri net. The net (with the
duration catalogue) is a **data structure that supplies** the timing parameters;
the clock is only ever **executed in the SimPy loop**, which is the single
discrete-event engine that advances simulated time for both arms. The accurate
telling is therefore *the movement layer supplies the time; SimPy spends it* —
never "the net holds a clock". This matters beyond pedantry: it is why the timing
regime is portable (a different simulator's event loop would spend the same
supplied durations), and it is why §2's ruling is about which *engine-advanced*
quantity the timing lands in rather than about net internals. Where this record
says "a timed transition", read: *the parameter the net supplies for the timeout
the loop executes at that place*.

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

> **SUPERSEDED 2026-07-28 by S3-R (banner at the top of this record).** The ruling
> stated here is the *hybrid*: the movement layer supplies the tactic dwell and the
> dispatched action additionally keeps its native substrate cost. Marc reversed it
> after the first build. The movement layer now supplies **all** attacker time, and
> the substrate's action costs are not consumed on that arm. The section is kept in
> full because its ontology (below) survives the reversal and its rejected
> alternatives are the reasoning the reversal was argued against — but **the boxed
> ruling immediately below is no longer what the code does.**

**The ruling, in one sentence a reader cannot misread:**

> The movement layer **supplies** the per-tactic time (an exponential draw whose
> mean is the catalogue value) and the SimPy loop **spends** it on the one shared
> clock, so the tactic timing contributes in full to **elapsed time-to-compromise**
> — the quantity the head-to-head comparison actually reports — while each
> dispatched action keeps its native substrate cost, so **internal MTTC** (the mean
> *per-action* duration) keeps its meaning and stays comparable across arms.

**Consequence for the reported metric (the decisive point, corrected).** Elapsed
time-to-compromise is read off the shared sim clock on both arms (§0, Fact 3).
Every contribution the movement arm makes to that clock — the behavioural dwell, a
dwell-only place's time, the substrate's action costs, the confusion penalty —
lands in it. So the timing regime **is** measured by the headline comparison, which
is what S3 intends: making the movement layer the timing source changes the tempo
of the profiled attacker, and the tempo is what the reported number sees. The
baseline arm has no behavioural dwell, so its number is untouched and its golden
stays byte-identical.

**Why the dwell is nonetheless kept out of the per-action rows.** Marc asked the
right question — why not feed the tactic time into the substrate's records so it
counts toward internal MTTC? Two concrete reasons, both fatal to that variant:

1. **It would silently drop most of the tactic time it set out to capture.** Under
   the version-2 mapping **seven of fifteen tactics are dwell-only** — they
   dispatch no verb, so no `attack_record` row exists to carry their dwell. Folding
   dwell into the dispatched verb's row would count the dwell of the eight mapped
   tactics and discard the other seven entirely. A metric that captures *some* of
   the behavioural time and not the rest is worse than one that cleanly captures
   none of it — and elapsed time-to-compromise already captures **all** of it.
2. **It would corrupt what an action row means.** An `attack_record` duration
   answers "what does a port scan cost on this substrate?". Adding an unrelated
   behavioural dwell makes the same field answer two questions at once, breaks the
   like-for-like reading of the same verb across arms, and moves every derived
   quantity (the goldens' `time_to_compromise`, and so every prior result) without
   the metric's definition changing — a silent re-baseline.

The alternative variant — emitting *new* dwell rows and widening the metric's name
list to count them — is rejected for the second reason in a sharper form: it
redefines internal MTTC, which breaks comparability with every prior result and
with the goldens, in exchange for a number elapsed time-to-compromise already
reports honestly.

**So the two quantities do different jobs, and both are wanted.** Internal MTTC
prices *an action* (unchanged, cross-arm comparable, substrate-owned). Elapsed
time-to-compromise prices *a campaign* (movement-layer timing included, cross-arm
comparable, the headline). S3 moves the second and deliberately leaves the first
alone.

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

### 3.1 What the exponential assumes, and where it is weak

An exponential dwell assumes **memorylessness** (residual dwell independent of time
already spent), a **mode at zero** (the single most probable dwell is ≈ 0), and a
**long right tail** (coefficient of variation fixed at 1).

- **Defensible for the scan- and exploit-shaped tactics** under a
  retry-until-success reading (memoryless attempts).
- **A poor shape for the low-and-slow group** (`persistence`, `stealth`,
  `command-and-control`, and the slow reading of `exfiltration`). Their defining
  character is *sustained, paced* dwell — probability mass concentrated **around** a
  value — which is the exact opposite of a mode-at-zero exponential, whose most
  likely outcome is a near-instant dwell. A same-mean heavier-shouldered
  distribution (gamma / Erlang / lognormal) would be more faithful: an Erlang-*k* is
  the sum of *k* exponentials and concentrates around its mean as *k* grows, which
  is precisely the "paced, deliberate" behaviour a stealth dwell should show.

### 3.2 The literature grounding — what existing stochastic-net work does about rates

This is a **new front for the dissertation**: it must explain why an arbitrary
number drawn from an arbitrary distribution is a defensible modelling move. A
survey of the tracked extractions settles it, and the answer is favourable — the
field's own register is exactly the one this work is adopting, stated here more
explicitly than most published work states it. Five findings, each citable.

**(1) Rates are declared, not measured — and the best papers say so in their own
text.** The closest executed stochastic-Petri-net attacker precedent is blunt:
Bland et al.'s rates "were notional and randomly selected between one and ten.
Identifying realistic rates is a future effort to enhance this research"
(§2.1) — in a peer-reviewed venue, with the net's *structure* face-validated by a
practitioner panel while its *rates* were uniform random draws. Mendonça et al.
badge the gap inside the parameter table itself: parameters "marked with ? were
reasonably estimated, as they were not found in the literature or product
specifications" (§4.1). McQueen et al. write "somewhat arbitrarily, we decided to
use 8 hours" for a process mean, and concede that "some of the assumptions
associated with our model have not been validated" (§1).

**(2) Nobody justifies the exponential as *realistic*; the formalism is justified,
the distribution is inherited.** Across the surveyed stochastic nets, what gets
defended is solvability, not memorylessness — Mendonça's DSPN is chosen because it
"allows the analysis of systems through numerical solution and simulation methods"
(§2.3). **No paper in the corpus defends memorylessness as faithful to attacker
behaviour.** Sharpest of all, our own substrate's lineage already made this exact
choice unargued: Zhang 2023 switched the inherited uniform MTD interval to an
exponential and recorded no justification for the distribution at all (§4.3.4,
§4.5). Adopting exponential here is therefore not a new liberty — it is the
substrate's own existing convention, now at least declared.

**(3) The strongest defence available — for a mean-based metric the mean is the
load-bearing quantity — and the condition it depends on.** Madan et al.'s landmark
security-Markov paper chose a *semi-Markov* process precisely because "some of the
sojourn time distribution functions may be non-exponential" (§1), and then showed
the analysis "depends only on the **mean sojourn time** and is independent of the
actual sojourn time distributions" (§"mean sojourn time"; the extraction records
this for the **steady-state** analysis). McQueen makes the same move by a different
route, hypothesising beta/gamma/exponential shapes and then reporting that "for
now, the analysis only uses the expected value of the time-to-compromise" (§3.4) —
the shapes are never used.

**The mechanism, because it is also the bound.** Mean time to absorption decomposes
into (expected visits to each state) × (mean dwell in that state), and the visit
counts are a property of the **routing probabilities alone**. So *when routing is
independent of how long each state takes*, the aggregate depends on the declared
means and not on the distributions around them, and the exponential costs nothing.

**Where that independence fails here — state it, do not lean past it.** In this
model routing is **not** fully independent of the dwell: an MTD mutation fires on
its own schedule and **races** the dwell, so a long dwell is more likely to be
interrupted than a short one, and an interrupt changes the verdict and therefore
where the token goes next. **Distribution shape re-enters through the interrupt
channel even though it leaves through the arithmetic** — and it does so precisely
in the regime the thesis is about, since the central contest is the ratio of
mutation interval to tactic dwell. The defensible claim is therefore *conditional*:
the mean is **expected** to be load-bearing, the residual shape-sensitivity runs
through interruption, and that is a **prediction to test** (the feasibility study,
§3.3), not a property to assume. Recording the leak is also what keeps the argument
non-circular: the family was fixed on precedent grounds before any result was
examined, and the check that could falsify it is specified in advance.

**(4) Where the field *does* reject the exponential, it is on the defender's
side — which this work does not touch.** Non-exponential choices cluster on
genuinely *periodic* events: Mendonça models the time-based MTD trigger as a
**deterministic** transition, and the FlipIt result is that "a periodic strategy
with a random phase strongly dominates all renewal strategies of the same rate" for
the defender's move. That asymmetry is convenient and should be stated: the
literature's objection to exponential firing is aimed at the MTD scheduler, which
lives in the frozen substrate and keeps its own timing regime (§4), not at the
attacker's per-tactic dwell.

**(5) The counter-evidence, acknowledged rather than buried.** The one large-*n*
empirical study in the corpus contradicts the exponential directly: Holm 2014
(203,025 intrusions across 261,757 systems, 2009–2012) finds a Pareto best fit for
time-to-first-compromise and reports the exponential "a poor choice" for
time-between-compromises and overall time-to-compromise, failing the heavy tail
beyond ~80 days (§5.2.1–§5.2.2). Two qualifications travel with it, both recorded:
its population is opportunistic enterprise malware alarms rather than targeted APT
campaigns, and it measures campaign-level compromise timing rather than per-tactic
dwell. **The honest consequence: the true shape is heavier-tailed than exponential,
so the exponential is presented as a tractable approximation whose *mean* is the
load-bearing quantity, with the tail behaviour named as a limitation** — not as a
fidelity claim.

**And the gap statement survives, narrowed.** No source in the surveyed corpus
grounds a *per-tactic attacker firing rate* in measured data. Where attacker-side
parameters are empirically grounded at all, the granularity is CVE-level exploit
development, vulnerability discovery, worm propagation, detection likelihood, or
aggregate time-to-compromise — never per-tactic dwell. The precedent-survey note's
claim holds, and should be worded at that narrowed granularity.

### 3.3 The position this licenses — the "veneer" stated honestly

The framing to carry into the dissertation, and it is deliberately unglamorous:
**the GSPN and its exponential firing are a tractable, precedented formalism laid
over quantities that are inherently arbitrary, because a true per-tactic duration
is not a measurable property of the world.** That is not a defect peculiar to this
model; it is the condition of every timed adversary model surveyed, and the
strongest of them say so in print. What this work adds over the norm is
*explicitness*: the tier badges say which values are inherited and which declared,
the group anchors keep the free-parameter count identifiable, the sweep bands are
published, and — after §3.2(3) — the record names the mean as the load-bearing
quantity and the distribution family as the tractable choice. The claim is
therefore **not** that attacker dwell is exponentially distributed. It is that
under a declared, swept, mean-anchored regime the *conclusion* is robust — which is
the only claim the evidence supports and the same modest-claim ceiling the rest of
the project operates under.

**A separate feasibility study is warranted, and is not this record's job.**
Whether the conclusion actually survives the rate regime — the sweep over the
declared bands, the sensitivity of any ranking to where in its band each anchor
sits, and whether a same-mean heavier-tailed family changes the answer — is an
*analysis*, not a design decision. It was spun out as its own brief and has since
**run twice**: [`rate_feasibility_study.md`](rate_feasibility_study.md),
pre-registered before any output existed, reported over 1 728 runs under the
hybrid regime this section originally ruled and re-run over 1 740 under **S3-R**
after the reversal. What follows is the S3-R verdict — the settled one.

**Its verdict on this section — the regime is confirmed, and the shape defence is
now scope-measured rather than assumed (2026-07-28).** No conclusion changes
direction anywhere in the declared bands under either regime, so the parameter
choice this record rules is defensible as ruled. Three results bear on §3:

1. **§3.2(3)'s mean-is-load-bearing defence holds across the operating region —
   and stops being sufficient at one corner.** Substituting a same-mean Erlang-4
   for the five low-and-slow tactics — halving the coefficient of variation, which
   is exactly the "paced, deliberate" shape §3.1 says the group's character wants —
   moves no outcome at any central cell, at either MTD-off or the operating
   interval. At the corner where the stealth anchor sits at its band top (×4) *and*
   mutations are running, it does: pooled host breadth falls 0.46 → 0.18, a paired
   difference of −0.28 ± 0.19 over fifty seed-profile pairs, consistent in sign
   (13 lower, 34 tied, 3 higher). The defence therefore survives with its scope
   measured instead of argued.
2. **The interrupt-channel leak §3.2(3) predicted is the mechanism, and it reaches
   an outcome under S3-R.** The prediction was that shape re-enters through
   interruption because a long dwell is likelier to be cut short than a short one.
   That is precisely what the corner shows, and the direction is instructive: an
   exponential's most probable dwell is near zero, and *that short-dwell mass is
   what lets the attacker occasionally complete an action between mutations*.
   Concentrating the same mean removes it, so nearly every dwell runs comparable to
   the mutation interval and nearly every dwell is interrupted. The more
   behaviourally faithful shape is **worse for the attacker**, and the
   mode-at-zero §3.1 flagged as the exponential's least realistic feature is doing
   quiet work.
3. **Why the first run missed it, which is itself a finding about the hybrid.**
   Under the hybrid each action also carried a fixed substrate cost no sweep
   touched, damping the behavioural timing's leverage; the same leak was visible in
   the mechanism and inert in every outcome. S3-R removed the damping. Handing the
   movement layer all of the attacker's time did not merely rescale the model — it
   made the declared timing consequential enough for its *shape* to matter at the
   extreme.

**The qualification, stated because it bounds the claim.** The study also found
that the project's operating mutation interval sits inside a *degenerate region*
where neither attacker can complete the objective (the boundary is above ~1 600 s;
study §7 C5, reproduced unchanged under S3-R). The shape check therefore ran where
compromise events are scarce, and the corner effect above is small and close to
the floor. So this section is not read as closing the distribution-family
question: the honest statement is that **the mean is load-bearing across the
region the evaluation operates in, and the family becomes a live parameter at long
dwells under mutation pressure** — which is where any future low-and-slow
refinement (§9's phase-type flag) would have to be argued.
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

## 4. Decision — the confusion penalty **stays on the substrate side**; no net place is built

**Ruling (Marc, 2026-07-28 — reverses this record's first draft).** The MTD
confusion penalty **stays where it is**, on the defender↔attacker border inside
MTDSim. **No penalty place is added to the net, and nothing about the penalty
changes.** S3's requirement is already discharged by the substrate's own
implementation (below), so the correct build action here is **none**.

**The architectural reason, which is the load-bearing one.** How a defender
*thwarts* an attacker — the interrupt, the confusion penalty, the lost connection —
is **simulator-implementation-specific**. It is MTDSim's model of what an MTD
mutation does to an adversary mid-action; another MTD simulator would thwart
differently or not at all. The **movement layer is meant to be portable across
simulators via the controller**: the net supplies campaign structure and tactic
timing, and the controller adapts it onto whatever action layer is underneath.
Pulling a *substrate-specific defensive penalty* into the net would weld
MTDSim-specific defender behaviour into the portable layer, so the net could no
longer be lifted onto another simulator without carrying MTDSim's thwarting model
with it. The penalty belongs to the simulator; the tactic timing belongs to the
movement layer; the border is exactly where it already sits.

**Why this is not a divergence from S3 — its requirement is already met.** S3 asks
that the penalty be "replicable the same way — a place in the net carrying **the
same base duration under the same stochastic regime**". The operative requirement
is the *regime*: the movement arm must experience the penalty as a stochastic draw
about the same base duration as the baseline. That is **already true today**, on
both arms, and has been since commit `53c5e5d`:

- the substrate draws `exponential_variates(ATTACK_DURATION['PENALTY'] = 20, 0.5)`
  — a **shifted exponential**, floor 20 with a small exponential tail, mean 20.5;
- **both arms consume the same call** (`apply_mtd_interrupt_cost`), the native FSM
  via `_handle_interrupt` and the movement driver via `_read_interrupt`;
- the probe measures exactly that: mean **20.54 / 20.57 / 20.55** t/u per interrupt
  across seeds 0/42/1234, **one charge per interrupt** (§0, Fact 2).

So the penalty is already a stochastic draw about the declared base duration,
already applied to the movement arm, already single-charged. Building a net place
would re-home a mechanism that already satisfies the ruling, at the cost of the
portability boundary. **S3's intent is satisfied; its suggested mechanism is
declined, with the reason recorded.**

**What this buys the build.** Everything §4 previously specified disappears: no
penalty place, no split of `apply_mtd_interrupt_cost`, no re-homing, and — most
valuably — **no double-charge risk to design against**. The single-charge property
is not a new invariant to establish but an existing one to *protect*, so the guard
becomes a cheap regression test (§6) rather than a build task.

**One consequence to carry forward.** The substrate docstring at
[`apply_mtd_interrupt_cost`](../../../../mtdnetwork/operation/attack_operation.py)
currently anticipates the re-homing — *"S3 will re-home the penalty onto the
movement layer as a net place… the driver stops calling it"*. That comment is now
**wrong** and must be corrected in the build commit to say the penalty stays
substrate-side by ruling, with the portability reason. It is the only penalty-related
edit the build makes.

---

## 5. The comparability argument, written before any code

> **WITHDRAWN 2026-07-28, not repaired.** This section argues that internal MTTC
> survives S3 unchanged and stays comparable across arms. Under S3-R it does not:
> the movement arm's action durations are the tactic's supplied time, so the same
> verb costs different amounts on the two arms by design. Marc's ruling is that this
> is not a defect to argue away — internal MTTC is a metric baked into MTDSim and
> belongs inside it, the movement layer supplies timings rather than owning the
> substrate's metrics, and comparability with prior published numbers is explicitly
> not a goal (a faithful comparison means running prior work on the final simulator,
> not freezing this model's metrics). The section is retained as the record of an
> argument that was made and then declined, not as a live claim. What does survive:
> the baseline arm is untouched and reproduces its golden, and the honest caveat
> below on never reporting an elapsed magnitude as an inherent property.

Two quantities carry the name "MTTC" (§0, Fact 3) and S3 lands on one of them.
Here is how a movement-arm run's timing composes into each, and what stays
comparable.

**Elapsed time-to-compromise — S3 lands here, and it stays cross-arm comparable.**
Both arms are measured as *the sim-clock time of the first compromise*, on the
**one shared SimPy clock**, from a common `t = 0`, in the same geometry. That is
already how experiment 1 measured both arms (§0, Fact 3), so the definition needs
no change and no second quantity needs inventing. Under S3 the movement arm's
elapsed time composes as:

> per visited place: `Exp(mean = duration_s)` behavioural dwell
> **+** the dispatched verb's native substrate cost (mapped places only)
> **+** the substrate's confusion penalty on each MTD interrupt (unchanged, §4),
> summed over the walk until the first compromise lands.

The baseline arm's composes as the second and third terms only — it has no
behavioural dwell. **Both are the same clock and the same event**, so the
comparison is valid; what changes is that the profiled attacker now carries an
explicit behavioural tempo the baseline does not have. That difference is the
*finding*, not a confound: it is precisely the claim that behaviourally-grounded
timing changes the answer.

**Internal MTTC — untouched, and still cross-arm comparable.** It remains the mean
duration of the three action-event rows. The dwell writes no such row (§0), the
penalty writes none, and dwell-only places write none — so the metric's definition,
its magnitude on the baseline (9.11 s on the no-MTD golden), and its like-for-like
reading of the same verb across arms are all **preserved unchanged**. It continues
to answer "what does one attack action cost on this substrate?", which S3 has no
business changing.

**The baseline arm.** No behavioural dwell, no dwell-only places, no penalty
change — the whole S3 change is movement-arm-only. Its golden headline
(692 records / 41 hosts) reproduces byte-for-byte. This is the contract with every
prior result and it is not touched.

**The honest caveat on the elapsed comparison.** The movement arm is slower partly
*because we declared it so* — the dwell means are the arbitrary values S3's own
caveat names. So the elapsed comparison must never be reported as "the profiled
attacker is inherently N× slower"; it is reported under the
operational-validation discipline: shape-not-scale, the declared means visible, and
the conclusion demonstrated robust across the declared sweep bands. A *ranking* that
survives the sweep is a result; a *magnitude* is a parameter choice. This is the
same discipline the tier badges already impose, now carrying a distribution rather
than a point value.

**The honest edge case (carried over, not introduced).** A mutation *during a
dwell-only place's dwell* raises no verdict and is not felt by the token
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §5) — an
acknowledged limitation tied to the H-coupling finding, unchanged by S3.

**Net answer to the handoff's decision-5 question.** Cross-arm comparison **remains
valid on both quantities**, and **no second reported quantity needs inventing** —
the elapsed measure the experiments already use is exactly where the timing regime
lands. The write-up obligation is **nomenclature, not machinery**: name the two
quantities distinctly and never write a bare "MTTC" (§0's flag).

**The honest edge case (carried over, not introduced).** A mutation *during a
dwell-only place's dwell* raises no verdict and is not felt by the token
([`success_failure_overlay_design.md`](success_failure_overlay_design.md) §5) — an
acknowledged limitation tied to the H-coupling finding, unchanged by S3.

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
2. **Determinism.** The same seed reproduces the same dwell sequence exactly.
3. **RNG isolation.** Timing draws neither read nor advance `_rng` or the substrate
   dice — the sampler and verdict streams are byte-identical with timing on vs off.
   (The penalty keeps drawing from the substrate's own dice, §4, so the *existing*
   penalty sequence must also be unperturbed by the new stream.)
4. **Penalty unchanged and still single-charged.** The existing regression test
   already pins this
   ([`tests/test_action_layer_dispositions.py`](../../../../tests/test_action_layer_dispositions.py)
   `test_movement_arm_pays_the_same_confusion_penalty_as_the_native_arm`); under §4
   it must simply keep passing, and its numbers must not move. This is now a
   *protect*, not a *build*.
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
  `yield self.env.timeout(self._draw_dwell(place))`. That is the *whole* behavioural
  change — `_read_interrupt` is not touched, because the penalty stays substrate-side
  (§4). Wiring at the single point where time is taken keeps the change one seam and
  the revert a one-line proposition.
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
4. **The confusion penalty: build nothing.** §4 rules it stays substrate-side. The
   only edit is correcting the now-wrong `apply_mtd_interrupt_cost` docstring that
   promises the re-homing, and confirming its existing regression test still passes
   unchanged.
5. **The metadata + guard inversion** in the same commit as the behaviour (§6),
   worded to preserve the timeline runner's point-value reading (the shared-catalogue
   hazard).
6. **Re-verify comparability empirically** (§5): the baseline golden reproduces
   exactly; internal MTTC is unmoved on both arms; and the movement arm's *elapsed*
   time-to-compromise moves as the record predicts (it now carries the behavioural
   dwell). If code and record disagree, the record wins — or the record's argument
   had a hole, which is itself a finding.
7. **Update the downstream docs** in the same commit: the duration-regime row in
   [`../../provenance.md`](../../provenance.md), the runtime lifecycle in
   [`success_failure_overlay_design.md`](success_failure_overlay_design.md) §6, and
   the revisit condition in
   [`../../../notes/ch4_methods/operational_validation.md`](../../../notes/ch4_methods/operational_validation.md).

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
  ([`../../../notes/ch4_methods/operational_validation.md`](../../../notes/ch4_methods/operational_validation.md),
  [`../../../notes/ch2_background/tactic_duration_precedent_survey.md`](../../../notes/ch2_background/tactic_duration_precedent_survey.md))
  and the comparability boundary
  ([`../../metrics_semantics.md`](../../metrics_semantics.md) §(a)/(d)).
- **Consumes formalism groundwork from:** [`petri_feasibility.md`](petri_feasibility.md)
  §3 (how the field uses Petri nets), §6.3 (the DSPN/CTMC fork on the analytical
  track).
- **Scores against:** [`../../apt_model_criterion.md`](../../apt_model_criterion.md)
  axis 5 (the tempo half of stealth that S3's regime would give the model —
  CONJECTURED there, and this record is its design).
- **Spins out:** the rate feasibility study
  ([`../../../handoffs/2026-07-28_tactic_rate_feasibility_study.md`](../../../handoffs/2026-07-28_tactic_rate_feasibility_study.md))
  — the sweep that tests whether any conclusion survives §3's declared regime, and
  whether §3.2(3)'s mean-is-load-bearing defence holds under a same-mean heavier-
  tailed family.
- **Figures:** `data/misc/_viz/stochastic_timing/stochastic_timing_design_viz.py` →
  `stochastic_timing_*.png` (the four design diagrams: where-the-clock-lives with
  both MTTC quantities bracketed, the GSPN place lifecycle, the exponential
  parameterisation with the honesty overlay, and the penalty portability boundary).

## 9. When this would need updating

- If the implementation finds the record under-specified: fix the record first,
  then build (the build has no authority to decide).
- If the phase-type / gamma refinement for the low-and-slow group is taken up: §3's
  distribution-family flag becomes a build, and the sweep's second dimension opens.
- If the S2 freeze lifts such that the verb native cost *can* be re-priced: §2's
  rejection of the "movement owns all time" option is revisited.
- If the canonical specs' "primary metric" nomenclature is reconciled (§0's flag —
  `project_context.md` and `metrics_semantics.md` name internal MTTC primary while
  every comparison reports elapsed time-to-compromise), §0/§5 are re-worded to the
  ratified names.
- If the penalty is ever wanted inside the portable layer after all — e.g. a second
  simulator is targeted and a *generic* thwarting model is defined at the controller
  seam — §4's portability argument is the thing to revisit, not its conclusion.
