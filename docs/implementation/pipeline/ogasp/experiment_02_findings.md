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
