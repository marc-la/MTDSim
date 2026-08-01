---
status: durable
created: 2026-07-29
updated: 2026-07-29
topic: "Experiment 2 (expo02_ashen_lynx) — the comparative run across the defence family: the pre-registered conclusions and badge criteria committed before any output existed, then the verdict as found"
---

# Experiment 2 — the movement attacker across the defence family

**Status:** durable. **§1–§6 are a pre-registration**: the matrix, the declared
inputs, the conclusions, their criteria and the three badge criteria were written
and committed **before a single result file existed**. This project has run three
studies on that discipline and it has paid off every time — twice by producing a
verdict that was unflattering and reportable rather than quietly revised. §7
onward reports what the run found, whichever way it fell.

The run's workspace is `data/results/expo02_ashen_lynx/`, gitignored by design
(regenerable: runner, numbers, figures). This record is the tracked account.

**On the name.** `ashen_lynx` is a deliberately fictional codename in the
adjective-animal idiom threat intelligence uses for real groups. It names *this
run*, not an adversary. The envelope-not-actor discipline holds throughout: every
statement below is about a behavioural envelope under a declared policy, and none
of them is about a named actor's campaign.

## 1. What this run is for

It discharges three things the chain has been accumulating.

**The comparative run experiment 1 deferred.** Experiment 1 covered one corner —
no-MTD against a single scheme — so the question the thesis actually asks, whether
a defence *ranking* shifts under a behaviourally-grounded attacker, has never been
put. This run carries the full defence family, resolved **per mechanism** rather
than only as MTD-on against MTD-off.

**The axis-1/3/4 demonstration arms**, folded in rather than run separately, as
their handoff directs. That contributes the verdict-blind ablation arm — the
control the adaptivity axis has never had, because every run to date has had the
adaptive loop switched on — and a two-dimensional reporting requirement.

**The S5 sink policy, now that it exists.** The policy landed as a two-valued run
input ([`sink_policy.md`](sink_policy.md)); this run consumes it and reports the
paired contrast.

> **Reconciliation note (2026-08-01).** The implementation these runs used is the
> one `sink_policy.md` describes — retrace with no edge suppression. The
> implementation that landed on `dev` is
> [`sink_retrace_design.md`](sink_retrace_design.md)'s (`retrace_sinks`), which
> adds a one-shot suppression of the edge into the sink. The two differ only
> there, but the difference is behavioural: after each retrace the next routing
> draw at the predecessor is taken from a renormalised distribution, so retrace-arm
> traces diverge from what the current code would produce wherever the policy
> fired — the three sink-bearing profiles, in the main matrix as well as the
> paired sub-study (the two sinkless profiles are untouched, and every `censor`
> arm is unaffected). The expected size of the divergence is bounded by the
> lifted inventory (sink in-edge mass ≤ 0.111): small, and in the direction of
> *fewer* immediate sink re-entries. Nothing here has been re-run; the analysis
> was re-executed from the recorded `runs.jsonl` against the reconciled code and
> every verdict reproduced byte-for-byte. **Open ruling for Marc, recorded here
> because this note is where a reader of these numbers will meet it:** whether
> the retrace-arm cells of the three sink-bearing profiles are re-taken under
> the landed implementation, or stand as recorded with this note as their
> caveat. The reconciliation handoff assumed only the 200-run sink sub-study
> would be affected; the main matrix also ran under `retrace`, so a faithful
> re-take is roughly three-fifths of the matrix, which is an experiment rather
> than bookkeeping and was not taken unilaterally.

## 2. The declared inputs, named at this experiment's seam

Every one of these is a choice, and naming them here is what stops a later reader
having to infer them from a runner script.

| input | value | why this and not the default |
|---|---|---|
| controller mapping | `v2_partial` | the go-forward mapping; seven tactics are dwell-only, which is where the attacker compromises anything at all |
| outcome overlay | `v3_persistent_backward` | the go-forward version after the persistence ruling. The registry default is still experiment 1's, so an unqualified run would silently reproduce the old arm |
| sink policy | `retrace` (main matrix), `censor` (paired sub-study) | S5. The default is `censor`, so this is named deliberately |
| timing regime | S3-R stochastic | the movement layer supplies every unit of the attacker's time |
| horizon | 15 000 s | matches experiment 1 and the baseline golden |
| geometry | the standard 50-host network | unchanged, so the substrate is not a variable |
| seeds | 0–9 | ten. See §5 for what that does and does not buy |

### 2.1 The mutation interval, chosen rather than inherited

The rate feasibility study found that the 200 s interval every published run of
this project has used sits **inside a degenerate region**: neither the profiled
attacker *nor the baseline* completes the substrate objective there, and the
objective only becomes reachable above roughly 1 600 s. Inside that region any
success-rate-shaped measurement is pinned at zero and can discriminate nothing.
Inheriting 200 s silently would mean reporting the region rather than the
attacker.

This run therefore carries the interval as a **dimension**, at two levels:

- **200 s** — the inherited operating point. Kept because it is the only interval
  on which anything in this project is comparable to anything else, and because
  the degenerate boundary is itself a result worth showing rather than a nuisance
  to route around.
- **2 000 s** — above the feasibility threshold, so the objective is reachable and
  success-rate measures can discriminate.

Any claim below states which interval it was measured at. A defence ranking taken
inside the degenerate region means nothing on its own, and is reported beside its
2 000 s counterpart.

### 2.2 The defence family, and the interval normalisation

Eight conditions. The four single mechanisms are the four in the substrate's
active pool; the other four MTD techniques exist in the tree but are commented out
of that pool, and enabling them would be a substrate change rather than a
parameter — the defender side is frozen by scope, so they stay out. (One of them
is independently known to be inert: the conformance audit records that
`UserShuffle` can never interrupt the attacker, because its resource type is
unhandled by the interrupt path.)

| condition | scheme | mechanisms |
|---|---|---|
| `none` | — | no MTD |
| `complete_topology` | single | CompleteTopologyShuffle |
| `ip_shuffle` | single | IPShuffle |
| `os_diversity` | single | OSDiversity |
| `service_diversity` | single | ServiceDiversity |
| `random_multi` | random | all four (experiment 1's arm) |
| `simultaneous_multi` | simultaneous | all four |
| `alternative_multi` | alternative | all four |

**The trigger interval is set explicitly on every condition**, rather than taken
from the substrate's per-scheme constants. Those constants give the random and
alternative schemes 200 s and the simultaneous scheme 700 s, which is an
undocumented asymmetry appearing in no paper; left in place it would confound
every cross-scheme comparison this run makes with a factor-of-3.5 difference in
mutation tempo. Normalising is the only way the scheme dimension means anything,
and it is recorded here because it is a departure from the substrate's defaults.

**Tay's reactive `mtd_ai` defender is excluded**, and the exclusion is a finding
rather than an oversight — see §6.3.

### 2.3 The attacker arms

| arm | what it is | what it is for |
|---|---|---|
| `baseline` | the inherited 6-phase FSM, untouched | the reference the substrate and its metrics were built around |
| `movement` | the profiled attacker, verdict-conditioned | the main arm |
| `movement_blind` | identical, but with a **verdict-blind** overlay | the axis-4 ablation: the adaptive loop off |
| `movement_learn` | the main arm plus the axis-7 learner at its declared values | exploratory (§6.2) |

The verdict-blind arm is built as an **empty value table**, not a new rule: an
overlay whose per-verdict mapping is empty gives factor 1.0 at every pair, because
composition treats an absent pair as passthrough. The token then routes on
observed structure alone and the substrate's verdict has no consequence. That is
precisely "the adaptive loop off", it needs no branch in the driver, and it is
asserted as a genuine null rather than assumed.

## 3. The matrix

| block | runs |
|---|---|
| 3 movement arms × 5 profiles × 8 defences × 2 intervals × 10 seeds | 2 400 |
| baseline × 8 defences × 2 intervals × 10 seeds | 160 |
| sink sub-study: censor arm, 5 profiles × {none, random_multi} × 2 intervals × 10 seeds | 200 |
| **total** | **2 760** |

The sink sub-study is deliberately *not* a full crossing. The policy fires only at
a sink, and two of the five profiles have none, so crossing it against the whole
defence family would multiply the run for cells in which the two arms are provably
the same run. The paired contrast at fixed seed on the conditions that matter is
what the comparability claim needs.

## 4. The conclusions, each with its criterion fixed in advance

**E1 — the MTD host-suppression survives per mechanism.** The weight study flagged
a ~90 % suppression of compromise breadth under this mapping, stable across its
whole sweep, and handed it to this run to confirm or withdraw *per mechanism*.
Criterion: on the `movement` arm, at least one single mechanism suppresses pooled
distinct-host count below the `none` condition with disjoint 95 % intervals. HELD
if so; the per-mechanism table is reported whichever way it falls.

**E2 — axis 4: the adaptive loop helps, not merely operates.** Criterion, taken
verbatim from the axis-1/3/4 handoff: the verdict-conditioned arm differs from the
verdict-blind arm on at least one progression measure, with disjoint 95 %
intervals, **in at least two profiles and at two or more defence conditions**. If
it holds, axis 4 moves to DEMONSTRATED. If the arms are indistinguishable, the
honest outcome is that the loop reacts and does not adapt usefully, the badge
stays DESIGNED, **and that is a reportable finding** rather than a soft pass.

**E3 — axis 3: strategic plurality.** Two halves, both required. (a) Per-profile
traversal diversity is non-degenerate: path entropy above 0.5 bits and more than
one distinct length-5 place-sequence prefix across seeds. (b) Outcomes vary over
**both** the profile and the mechanism dimensions — an interaction, not a single
main effect: the mechanism ranking by breadth suppression is not identical for
every profile. A ranking identical for every profile evidences defender plurality
only and is reported as such.

**E4 — axis 1: persistence in outcome terms.** Criterion: sustained staged advance
evidenced on the replacement progression measure — deepest *successfully actioned*
stage, or foothold retention across at least one mutation — in more than a quarter
of runs. Otherwise DESIGNED, with "the structure runs and does not convert to
progress on this substrate" recorded as the finding. Note the measure's own known
limit under this mapping: the dwell-only objective band can hold no verdict, so
deepest-successfully-actioned is structurally truncated at 2 here, and the
coverage curve is its mandatory companion.

**E5 — the defence ranking shifts between attacker arms.** The thesis's central
divergence claim in its sharpest testable form. Criterion: the rank order of the
seven MTD conditions by breadth suppression differs between the `baseline` arm and
the `movement` arm. **Reported as a rank comparison with its caveat, never as a
significance claim** — ten seeds cannot support one, and two prior sweeps have
established that at this sample size.

**E6 — the sink policy lengthens the window without changing the verdict.**
Criterion: under `retrace`, profiles that terminated at a sink now terminate at
the horizon, and their breadth and success conclusions are unchanged relative to
`censor` at the same seed. If breadth *changes*, the comparability break becomes
load-bearing rather than bookkeeping, and that is the finding.

**E7 — is any mechanism's tax non-proportional to dwell?** This is the condition
the incentive-rationality study named as one of the two routes that would move
axis 6 to DEMONSTRATED, and it said the route was reachable inside this run's
defence family. Criterion: per mechanism, compute the per-tactic relative MTD tax
(interrupt-attributable time as a fraction of that tactic's own dwell); a
mechanism is **non-proportional** if the ratio of its largest to smallest
per-tactic relative tax exceeds 3. The axis-6 sweep measured that ratio at roughly
3.5 for the pooled random-multi scheme while the *absolute* interrupt rate spread
18-fold, which is why the cost-sensitivity result did not reproduce. **This does
not move axis 6** — that needs a run at a non-zero rationality exponent, which the
S2 governance question gates — it tells the next cycle whether the condition it
needs exists at all.

**E8 — the stealth contrast, event-wise (axis 5a).** The stealth design record's
own leading argument is that the profiled attacker *is* the low-and-slow attacker
and the baseline is not, and that this contrast is a stealth-shaped result the
model already produces without any stealth mechanism. Criterion, as a
characterisation rather than a badge move: the profiled attacker's dwell fraction
in non-action places is bounded away from zero while the baseline's is
**structurally zero**, and the profiled attacker's attack-event rate per unit
simulated time is lower than the baseline's in every cell. Comparisons are
**event-wise only** — cross-arm time comparability was withdrawn under S3-R, and
the two arms run on different clocks.

**E9 — the degenerate region is a property of the region.** Criterion: at 2 000 s,
does either arm reach the objective? If the baseline does and the profiled
attacker does not, the constraint is confirmed as a region property rather than an
artefact of the metric, and every ASR-shaped statement in this project inherits
that reading.

## 5. What this run is not powered for, stated before it runs

Rather than discovering it in the analysis for the fourth time:

- **Any ordering of profiles by progress.** Two independent sweeps have failed
  this conclusion at ten seeds, reached through unrelated parameter families. It
  is not attempted.
- **Any significance claim on the defence ranking (E5).** Ten seeds gives a
  directional rank comparison, not a test.
- **Cross-arm MTTC.** Withdrawn under S3-R: the two arms price time differently,
  so only event-wise quantities are cross-arm safe, and the measurement suite
  enforces that in its API rather than leaving it to discipline.
- **Any cross-paper magnitude claim.** Within-substrate comparison only.
- **Experiment 1's published magnitudes as a comparison target.** They are stale —
  the substrate was re-baselined and the timing regime changed since — so the
  baseline is re-measured inside this run.

## 6. Three things this run deliberately does not do

### 6.1 It does not tune anything in reaction to the numbers

The standing constraint, and it matters more here than anywhere: badges move on
evidence only, and no weight, mapping, metric or parameter is adjusted because a
row read badly. A disappointing arm is a finding.

### 6.2 The learning arm is exploratory, and labelled so

The axis-7 study's own conclusion is that a learning arm is worth running properly
only once the learner's credit signal carries **progress** rather than the routing
verdict — a credit-assignment redesign, not a parameter change. That redesign has
not happened. The arm is carried anyway because it answers a question the axis-7
sweep could not: that sweep ran one defence condition, and its most
defence-relevant finding — that MTD is severely effective against a learner,
because what a mutation destroys is an estimate rather than a foothold — has never
been resolved per mechanism. **No badge moves on this arm**, and its breadth
numbers are expected to be worse than the main arm's, for the reason the axis-7
study established.

### 6.3 It does not run Tay's reactive defender, and that is the axis-5a blocker

The stealth record establishes that `mtd_ai` is the one defender in the pool whose
decisions key on attacker-derived signals, which makes it the only route by which
a stealthy tempo could become consequential — and therefore the only route to a
DEMONSTRATED badge on the tempo half of axis 5. It is excluded here for three
independent reasons, each sufficient: the movement arm has **never been run
against `mtd_ai` at all** and there is no integration for it in the run wiring;
the agent is a trained network whose use is deferred to the ablation phase by
standing project direction; and the conformance audit records a defect on exactly
that path — any attacker-sensitivity below 1.0 raises an unbound-local error, so
the documented sensitivity experiment cannot currently run. Recorded here so the
absence reads as a bounded, known blocker rather than a gap.

## 7. Threats to validity this run inherits from the substrate

The conformance audit landed days before this run and it changes how several
numbers below must be read. The four that bite hardest:

- **Substrate timing is near-deterministic, not exponential.** Every draw is a
  location plus an exponential with σ = 0.5, so MTD intervals and durations vary
  far less than "exponential" suggests. Run-to-run variance in these results is
  therefore not coming from the mutation schedule.
- **MTD is systematically stronger here than in the papers it descends from.**
  Diversity mechanisms install *latest-version* replacements, which reduces
  vulnerability count rather than merely re-rolling it; and every technique exempts
  exposed hosts, so "MTD applies to all nodes" is silently narrowed to all
  non-exposed nodes. Both are live in every condition in §2.2.
- **Compromise is never revoked.** No code path removes a host from the compromised
  set, so breadth is monotone by construction. MTD cannot *take back* a host in
  this substrate — it can only slow acquisition — and "MTD reduced compromise" is
  therefore not a measurable statement here. Every suppression number below means
  *slower acquisition within the horizon*.
- **Effective mutation rate is not the nominal one under the simultaneous scheme.**
  Resource contention serialises same-layer mutations through a queue rather than
  the suspension path, so the realised count differs from the schedule. This run
  therefore **measures realised interrupts per run** rather than assuming the
  interval, and reports them beside every scheme comparison.

## 8. Reproduce

```
PYTHONPATH=src python data/results/expo02_ashen_lynx/run_experiment.py --workers 6
PYTHONPATH=src python data/results/expo02_ashen_lynx/analyse.py
PYTHONPATH=src python data/results/expo02_ashen_lynx/make_figures.py
```

---

# The verdict, as found

*Everything above this line was committed before the run existed
(`a64903d`, rebased to `162602c`). Everything below reports against those
criteria without amending them.*

**The run.** 2 760 runs, zero errored cells, `data/results/expo02_ashen_lynx/`.

**One thing changed between the pre-registration and the run, and it is
material.** The run executes against the substrate **after** the intent-audit
dispositions Marc ruled on landed — the global RoA priority stack, the diversity
mechanisms drawing a random compatible service at a random version instead of the
latest, and the reserve-resource handling. That commit explicitly retires a
behaviour that "had been quietly strengthening the defence", and the diversity
family is one of the two families this run ranks. Running against the older
substrate would have produced a defence ranking known to be wrong in exactly the
place the headline result lives, so the run was rebased onto the fixes before it
was taken. Experiment 1's magnitudes were already stale; they are now stale twice
over.

## 9. The headline — the defence ranking inverts between the two attackers

**E5 HELD, and it is the strongest result this project has produced.** At the
operating interval the rank correlation between the two attackers' defence
orderings is **ρ = −0.893**: not merely different, very nearly reversed.

| mechanism | suppression vs the inherited attacker | vs the profiled attacker |
|---|--:|--:|
| Service Diversity | **90.4 %** | 37.1 % |
| OS Diversity | **88.8 %** | 41.2 % |
| IP Shuffle | 22.1 % | **87.8 %** |
| Complete Topology Shuffle | 18.2 % | **89.1 %** |

(Breadth suppression, 200 s, ten seeds each; no-MTD baselines 38.40 and 5.88
hosts respectively.)

The mechanism is legible and is not a statistical accident. The inherited
attacker is a **vulnerability-exploiting** actor: it walks the substrate's native
precondition order and converts scanned services into compromises, so a defence
that re-rolls the services and their versions destroys precisely what it depends
on. The profiled attacker is a **position-and-reconnaissance-driven** actor: it
spends 37–43 % of its visits in tactics that dispatch nothing and moves by
accumulating position, so a defence that shuffles topology and addresses destroys
precisely what *it* depends on — while re-rolling a service it was never going to
exploit costs it comparatively little.

This is the thesis's central claim in its sharpest available form. It is not that
the profiled attacker is stronger — it is dramatically weaker on every headline
security metric, and 0 of 1 200 movement runs reached the objective. It is that
**an evaluator using the inherited attacker would rank the defence family in
almost exactly the opposite order to one using a CTI-grounded attacker**, and
would therefore deploy a different mechanism. Behavioural fidelity does not merely
change the magnitude of the answer; here it changes which defence you buy.

Two disciplines hold around it. Ten seeds supports a **rank comparison and not a
significance test**, as pre-registered. And the effect is interval-dependent: at
2 000 s the correlation is ρ = +0.286 — still not the same ordering, but the
inversion is a property of the high-pressure regime, because at 2 000 s MTD barely
suppresses the profiled attacker at all (§10).

## 10. E1 — the ~90 % suppression is confirmed, and it belongs to one family

The weight study handed this run a ~90 % host-suppression to confirm or withdraw
per mechanism. **Confirmed, and resolved.** At 200 s all seven conditions suppress
with disjoint intervals, but they do not do so equally:

| condition | hosts | suppression |
|---|--:|--:|
| no MTD | 5.88 | — |
| simultaneous (multi) | 0.60 | 89.8 % |
| Complete Topology | 0.64 | 89.1 % |
| IP Shuffle | 0.72 | 87.8 % |
| alternative (multi) | 1.78 | 69.7 % |
| random (multi) | 1.90 | 67.7 % |
| OS Diversity | 3.46 | 41.2 % |
| Service Diversity | 3.70 | 37.1 % |

The ~90 % figure was never a property of "MTD"; it is a property of the
**position-destroying** mechanisms, and reporting it as a single number — which is
all the MTD-on/MTD-off framing could ever have produced — averaged two effects
that differ by a factor of two and a half.

**And at 2 000 s the effect very largely evaporates**: only IP Shuffle still
suppresses with a disjoint interval (22.4 %), and Complete Topology Shuffle is
nominally negative. Whatever MTD buys against this attacker, it buys at tempo.

**A confound this run measured rather than assumed.** The conformance audit
records that the simultaneous scheme serialises same-layer mutations through a
resource queue, so effective mutation rate need not equal the nominal one. It does
not: the simultaneous condition delivers **127.0 interrupts per run against 75.0**
for the single mechanisms at the same nominal interval. Its first-place ranking is
therefore substantially a *pressure* effect rather than a *composition* effect,
and any reading of it that says "batching mechanisms works best" is unsupported by
this run.

## 11. E2 — axis 4: the adaptive loop reacts, and does not adapt usefully

**MOVED at both intervals; axis 4 holds at DESIGNED.** This is the control the
axis has never had, and it fails cleanly.

At 200 s, *none* of the three progression measures separates the
verdict-conditioned arm from the verdict-blind arm on the pre-registered bar (two
profiles and two defence conditions with disjoint intervals). At 2 000 s breadth
reaches one profile and three conditions — the profile half of the bar is not met.
The point estimates are quietly instructive: conditioning helps nominally on four
of five profiles under no MTD (`double_extortion` 8.10 against 7.50, `aggregate`
6.40 against 5.80) and **hurts** on the fifth (`infrastructure_setup` 4.10 against
5.40), with every interval overlapping.

The honest statement, which the pre-registration committed to reporting as a
finding rather than a soft pass: **routing on the substrate's verdict is
approximately free.** The loop demonstrably operates — that has been on record
since the runtime verification — and after 1 600 paired runs it has not been shown
to change an outcome. Axis 4 has held at DESIGNED on the argument that nothing
separated *reacts* from *adapts usefully*; that argument is now retired, and the
badge stays where it was for a better reason than the absence of a control.

## 12. E3 — axis 3: strategic plurality, DEMONSTRATED

**HELD at both intervals, on both halves.** Traversal diversity is non-degenerate
in every profile — pooled path entropy 1.451 to 2.714 bits, and between 2 and 10
distinct five-place opening sequences across ten seeds. And outcomes vary over
**both** dimensions rather than one: the mechanism ranking by breadth suppression
is **not** the same for every profile (4 of 5 distinct at 200 s, 5 of 5 at
2 000 s). `infrastructure_setup` is best suppressed by IP Shuffle while
`pure_steal` and `aggregate` are best suppressed by the simultaneous scheme.

That is an interaction, not a defender main effect, and it is what the axis asked
for. **Axis 3 moves DESIGNED → DEMONSTRATED**, carrying the boundary the criterion
itself insisted on: this is **variety, not strategy**. The branching is drawn from
static corpus proportions, not chosen by a decision rule, so the claim is that a
plural attacker changes what the defence dimension looks like — never that the
attacker is selecting among strategies.

## 13. E4 — axis 1: persistence, and a measurement finding that outranks it

**MOVED at 200 s, HELD at 2 000 s; axis 1 holds at DESIGNED.** Getting here
required correcting the analysis twice, and both corrections are worth more than
the verdict.

**The depth measure is saturated — again.** `deepest_successful_stage` returns
**2 for all 800 movement runs**. Under this mapping the dwell-only objective band
can hold no verdict, so the measure is structurally truncated at 2 and has no
variance to discriminate with. This is the third progression measure this project
has retired for saturation, and the second time it has happened to the *replacement*
for a saturated measure.

**The retention measure means the opposite of what the criterion assumed.** The
first pass of this analysis reported axis 1 as DEMONSTRATED on foothold retention
in 28–62 % of runs. Cross-examining the measure against its implementation showed
the sign was backwards: the quantity counts footholds *severed* by a later
position-destroying mutation — a duration until loss — while the retained
footholds are the censored ones. And a second artefact sat underneath: OS and
Service Diversity are **application-layer** mutations that interrupt often (52.7
per run) and sever position **never**, so every foothold under them is retained
trivially, by the absence of any threat to it. Counting those cells would have
evidenced persistence from the absence of a challenge to it.

Restricted to the defences that actually contest position, per-foothold retention
at the operating interval is **0.0 % to 1.6 %**. Every foothold the profiled
attacker takes is eventually taken back. At 2 000 s it rises to 3.3–43.6 %, which
is the criterion's bar — but the reading is that retention rises as mutation
pressure falls, which is a statement about the defence's tempo and not about the
attacker's persistence. **The badge does not move on evidence that the attacker
keeps position exactly when the defence stops taking it.**

## 14. E6 — the sink policy, and a comparability break that is load-bearing

**MOVED, and that is the useful answer.** The policy does what it was built to do:
`double_extortion` terminated at a sink in 100 % of censored runs and 0 % of
retraced ones, and `pure_steal` in 38 % against 0 %. But breadth **changes**, and
not marginally:

| profile | policy | sink share | hosts | attempted actions | elapsed |
|---|---|--:|--:|--:|--:|
| `double_extortion` | censor | 100 % | 1.95 | 68 | 3 256 |
| `double_extortion` | retrace | 0 % | **6.42** | 268 | 14 969 |
| `pure_steal` | censor | 38 % | 4.08 | 247 | 11 153 |
| `pure_steal` | retrace | 0 % | 5.10 | 331 | 14 959 |

`double_extortion`'s compromise count more than triples. **Nothing about the
attacker improved** — it was previously being switched off after a fifth of its
horizon. The comparability break the design record warned about is therefore not
bookkeeping: experiment 1's per-profile numbers for the sinking profiles were
measuring a censoring artefact as attacker behaviour, and no experiment-2 figure
may be pooled with them.

The retrace rate confirms the design's structural argument. `double_extortion`
retraces 6.9 times per run and `pure_steal` 0.6 — spread across runs of 268 and
331 actions, against the predicted ~1.1 retraces per sink encounter. No walk
reached the `max_events` backstop. The two profiles with no sinks produce
bit-identical arms, as the null gate requires.

## 15. E7 — the condition axis 6 needs exists, but not where it operates

**All seven mechanisms are dwell-proportional at 200 s** (max/min per-tactic
relative tax 1.53 to 2.90, under the pre-registered threshold of 3). This
reproduces the incentive-rationality study's anatomy per mechanism and explains
its negative result at mechanism resolution: MTD's tax really is levied in
near-proportion to a tactic's declared dwell, so a normalised utility ratio cannot
see it, whichever mechanism is running.

**At 2 000 s four of the seven cross the threshold** — alternative (multi) 5.83,
random (multi) 4.18, simultaneous (multi) 4.13, Complete Topology 3.48. So the
condition the axis-6 record named as a route to DEMONSTRATED does exist in this
defence family, and it exists **outside** the interval every prior run used. That
is a specific, cheap instruction for the next cycle rather than a general
suggestion. It moves nothing today: a claim needs a run at a non-zero rationality
exponent, which the S2 governance question still gates.

## 16. E8 — the stealth contrast the model already produces

**HELD.** Event-wise only, as S3-R requires:

| arm | share of visits in non-action tactics | attack events per 1 000 s |
|---|--:|--:|
| inherited baseline | **0.0 %** (structural) | 92.9 |
| `double_extortion` | 43.3 % | 17.7 |
| `pure_impediment` | 39.4 % | 18.9 |
| `aggregate` | 38.4 % | 21.2 |
| `pure_steal` | 37.0 % | 21.6 |
| `infrastructure_setup` | 17.3 % | 34.6 |

The profiled attacker generates between a fifth and a third of the baseline's
observable event rate, and spends up to 43 % of its visits in tactics that
dispatch nothing at all — against a baseline whose corresponding figure is
**structurally zero**, because the inherited attacker has no non-action state to
occupy. The low-and-slow contrast is a property the model already has, without any
stealth mechanism.

**No badge moves.** Axis 5 stays NOT ADDRESSED, and this run sharpens why rather
than softening it: a tempo with no detection model to be quiet against is a
measurable difference with no adversarial consequence. The route to changing that
is named and blocked (§6.3).

## 17. E9 — the degenerate region is a property of the region

**CONFIRMED.** The baseline reaches the objective in 8 of 80 runs at 200 s and
**33 of 80** at 2 000 s; the profiled attacker reaches it in **0 of 400** at
either. The region behaves exactly as the rate study predicted for the inherited
attacker — relax the mutation pressure and success becomes reachable — and the
profiled attacker's zero is *not* a region artefact, because it survives the relaxation
that rescues the baseline. Every ASR-shaped zero this project has reported for the
profiled attacker should be read as a statement about the attacker on this
substrate, not about the operating point.

## 18. The exploratory learning arm

The axis-7 sweep's verdict reproduces across the whole defence family and at both
intervals: **the learner lowers compromise breadth in every one of the sixteen
condition × interval cells** (5.88 → 5.24 with no MTD; 0.64 → 0.36 under Complete
Topology; 5.02 → 4.56 under Service Diversity at 2 000 s), while lowering its own
blocked fraction (15.3 % → 8.6 % with no MTD). More successes, fewer hosts — the
misspecified-reward finding, now shown to be a property of the learner rather than
of the one defence condition the axis-7 sweep could afford.

The defence-relevant half also resolves per mechanism. Forgetting events track
realised mutation pressure exactly (75.0 per run under the single mechanisms at
200 s, 128.9 under the simultaneous scheme, 5.2–8.0 at 2 000 s), so **the
mechanisms that destroy the learner's belief fastest are the position-destroying
ones** — the same family that suppresses breadth. No badge moves: the arm is
exploratory by pre-registration, and the credit-assignment redesign axis 7 needs
has not happened.

## 19. Scored against the APT criterion

| axis | before | after | why |
|---|---|---|---|
| 1 — persistence | DESIGNED | **DESIGNED** | retention against position-contesting defences is 0.0–1.6 % at the operating interval; the depth measure is saturated (§13) |
| 2 — objective conditioning | DEMONSTRATED | **DEMONSTRATED** (reinforced) | the mechanism ranking differs by profile in 4 of 5 (200 s) and 5 of 5 (2 000 s) cells — objective conditioning now reaches the *defence* dimension, not just the failure mode |
| 3 — strategic plurality | DESIGNED | **DEMONSTRATED** | entropy 1.45–2.71 bits with 2–10 distinct openings, and a profile × mechanism interaction (§12) — as variety, not strategy |
| 4 — adaptivity | DESIGNED | **DESIGNED** | the verdict-blind ablation is indistinguishable from the conditioned arm across 1 600 paired runs (§11) |
| 5 — stealth | NOT ADDRESSED | **NOT ADDRESSED** | the tempo contrast is large and has no consequence; the one route to consequence is blocked (§6.3, §16) |
| 6 — incentive rationality | DESIGNED | **DESIGNED** | E7 locates the missing condition but cannot consume it (§15) |
| 7 — learning | DESIGNED | **DESIGNED** | the arm is exploratory and reproduces the axis-7 negative (§18) |
| 8 — scheme awareness | NOT ADDRESSED | **NOT ADDRESSED** | ruled out of scope; untouched |

**One badge moves, and one nearly did.** Axis 3 to DEMONSTRATED on a
pre-registered criterion. Axis 1 was reported as moving by the first pass of this
analysis and was withdrawn on cross-examination — which is the pre-registration
discipline doing the only job it exists to do.

## 20. What is working, and what is not

**Working.** The model produces a defence ranking that inverts against the
inherited attacker's, with a mechanism behind it that is legible rather than
statistical (§9); objective conditioning reaches the defence dimension (§12,
§19); the measurement suite carried every claim without a new measure being built;
and the pre-registration caught a badge move that the numbers would have supported
and the measures did not (§13).

**Not working.** Adaptivity is free — 1 600 paired runs cannot distinguish
conditioning on the substrate's verdict from ignoring it (§11). Two successive
progression measures have now saturated under this mapping, so axis 1 has no
instrument. The profiled attacker still reaches the objective zero times in 1 200
runs, and that is now known not to be a regime artefact (§17). And three of the
eight axes remain closed by things this run cannot touch: a detection model
(axis 5), a governance ruling (axis 6), and a credit-assignment redesign (axis 7).

**The largest open risk to everything above** is that the whole result rests on a
tactic→verb mapping that remains a chosen input parameter rather than a fidelity
claim. The inversion in §9 says the two attackers depend on different substrate
properties; how much of that difference is the CTI corpus and how much is the
mapping is not separable from this run, and a mapping-sensitivity study is the
obvious next instrument.
