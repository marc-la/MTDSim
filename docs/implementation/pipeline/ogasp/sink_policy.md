---
status: durable
created: 2026-07-29
updated: 2026-07-29
topic: "L3 sink policy (supervisor S5) — the retrace rule that replaces accept-and-censor: what retrace means, why it cannot oscillate on these nets, what it costs, what it records, the comparability break it creates, and the considered alternatives"
---

# The sink policy — what a token does when it walks into a place it cannot leave

**Status:** durable design-and-build record. It discharges **Part A** of the
experiment-2 handoff, which asked for the thinking before the code: *"the change
is three lines of code and a week of consequences."* §1–§6 were written and
committed **before** the mechanism was built, and §7 records what the build and
its tests then showed.

## 1. What is being replaced, and why it is not merely tidy-up

A place in a profile's routing net can have no outgoing edge, because the
analyst-curated corpus drew none leaving it. Reaching such a place — a **sink** —
currently ends the run. That was ruled deliberately for experiment 1 as the
low-risk default (accept-and-censor), and the cost of the ruling then
materialised exactly as predicted: two of five profiles died at a sink in almost
every run, observing 74–210 actions against roughly 500 for the profiles that ran
to the horizon
([`experiment_01_findings.md`](experiment_01_findings.md) Finding 3).

That is not a small measurement nuisance. A censored walk has a **shorter
denominator for every per-run quantity** — time-to-first-compromise, action
counts, breadth — so a profile that dies early looks different from one that does
not for a reason that has nothing to do with the attacker's behaviour. The
supervisor's ruling (S5) is that a run reaching a sink should not die: the token
**retraces the edge it travelled**.

**Sinks do not go away on their own.** They are a property of the nets. Neither
the partial controller mapping nor the distance-weighted transitions add edges,
and the synthetic pre-intrusion overlay does not reconnect them either — verified
directly in §3 below. Retracing is therefore still required after every other
refinement has landed.

## 2. The rule

Three clauses, and the second is the one that does the work.

1. **On reaching a sink, the token steps back to the place it came from.** One
   step, not more (§5 ranks the alternatives).
2. **The retraced-to place is then an ordinary visit.** The stepping loop does
   there what it does everywhere: draws that tactic's dwell and spends it,
   dispatches its verb, reads the verdict, and composes the next routing decision
   on that verdict. Nothing about the walk downstream of a retrace is special.
3. **If the sink is the entry place** — so there is no edge to retrace — the walk
   falls back to accept-and-censor and records a sink termination. This cannot
   arise with the synthetic overlay on (the entry place is `reconnaissance`, which
   is never a sink there), and it is a defensive clause rather than an expected
   path.

**A clause that was designed in and then removed, because building it exposed the
conflict.** The handoff recommended answering the oscillation question by treating
arrival at a sink as a failure verdict and letting the failure-side weighting
route the token away — attractive because it reuses a declared mechanism instead
of adding a special case. Written out against the time-cost rule in §4, the two
turn out to be incompatible: routing *out* of the retraced-to place under an
imposed verdict means the token passes through it rather than re-occupying it, so
it never pays that place's dwell and the retrace becomes a zero-time teleport —
precisely the hang §4 exists to prevent. Paying the dwell means the place's own
action runs, which produces its own verdict, which is the one the routing must
compose on. The clause was therefore dropped rather than reconciled, and §3 is why
that costs nothing: **the steering was protecting against a failure mode these
nets cannot exhibit.** Adding a routing special case for a problem the structure
does not have would be mechanism for its own sake, which the declared-value
guardrails exist to refuse.

## 3. Why the walk cannot oscillate — the structural answer, measured not assumed

The obvious objection to clause 1 is that the token retraces to a place and then
walks straight back into the same sink, oscillating between two places for the
rest of the run and producing a great many events and no information. Since the
verdict-steering clause has been dropped, this section carries the whole argument,
and it has to be structural rather than reassuring.

Enumerating every sink in every profile, with the out-degree of each place that
can reach it:

| profile | sink | declared dwell | in-neighbours (out-degree) |
|---|---|--:|---|
| `pure_steal` | `impact` | 36.0 s | `discovery` (9), `execution` (11), `stealth` (12) |
| `double_extortion` | `credential-access` | 4.5 s | `command-and-control` (9), `execution` (8), `initial-access` (7), `lateral-movement` (6) |
| `infrastructure_setup` | `defense-impairment` | 22.5 s | `command-and-control` (8) |
| `pure_impediment` | — | — | *(no sinks)* |
| `aggregate` | — | — | *(no sinks)* |

**The minimum out-degree anywhere in that table is 6.** No place that can reach a
sink has that sink as its only exit, so a hard two-cycle — the failure mode the
handoff worried about — is **structurally impossible on these nets**.

The soft case is better than that bound suggests, because the edges into sinks
carry very little weight. The heaviest is `command-and-control → credential-access`
at 0.111; the others that carry any mass at all are
`execution → impact` at 0.059 and `execution → reconnaissance` at 0.083, and the
remaining in-edges are effectively zero. Returning to the sink is a Bernoulli
draw at those weights, so the number of consecutive retraces at one encounter is
geometric with success probability at least 0.889, giving an expectation of about
**1.1 retraces per encounter** and a probability below 1.4 % of three or more in a
row. Each of those cycles pays a full dwell, so even the tail is bounded in
simulated time rather than merely in probability. The runs measure this rather
than assuming it (§6).

Two further properties fall out of the same enumeration and are worth recording,
because each closes a hole:

- **Every reachable sink has a strictly positive declared dwell** (36.0, 4.5 and
  22.5 s). The one zero-duration tactic in the catalogue, `resource-development`,
  is a sink only in the observed-only arm and has **no in-neighbours at all**
  there — it is unreachable, so it can never be entered, let alone retraced from.
  A zero-simulated-time loop is therefore not representable, which is the
  property §4 needs.
- **The synthetic overlay does not remove a single sink.** The enumeration is
  identical with the overlay on and off for `pure_steal` and
  `infrastructure_setup`'s `defense-impairment`; the overlay-off arm merely adds
  further sinks. This is the measured basis for the claim in §1 that the other
  refinements leave the sink set alone, and it is also what disposes of the
  "route elsewhere" alternative in §5.

This argument is a **check, not a theorem**: it holds for the corpus as it stands.
It must be re-run whenever the corpus, the profile partition, or the synthetic
overlay changes, and the inventory is cheap enough that there is no excuse not to.
A net *could* be drawn in which a sink's only in-neighbour has out-degree 1, and
on such a net the walk would cycle until the `max_events` backstop fired and
recorded itself — the existing behaviour for a pathological cycle, and a loud
failure rather than a silent one. That is also the case in which the
edge-suppression alternative in §5 stops being redundant.

## 4. What it costs

**A retrace must cost time.** A zero-time retrace is an infinite loop in zero
simulated time, which is a hang rather than a result.

The cost is not charged by the retrace event itself. It is charged by **the
re-visit the retrace causes**: the token arrives back at the retraced-to place and
the stepping loop does what it does at every place — draws that tactic's dwell
from the declared catalogue and spends it. A retrace therefore costs **one full
place-visit at the retraced-to place**, which is between 4.5 and 45 simulated
seconds in expectation depending on the tactic, and the retrace record itself is
instantaneous.

This is the right place for the cost to sit, and not only because it needs no new
parameter. The attacker that walks into a dead end and backs out has not spent
time *in the dead end* beyond the dwell it already paid on arrival; what it spends
is the effort of re-establishing itself where it was. Charging the re-visit says
exactly that, in the model's existing vocabulary.

## 5. The alternatives, ranked and recorded

**Suppress the edge that led to the sink for the next selection**, or the softer
form of the same idea, impose a `failure` verdict on the way out. Both make return
impossible or unlikely by fiat. Declined for the reason §2 records — the softer
form is arithmetically incompatible with charging the retrace any time, and the
harder form is a routing special case that exists for one situation — and, more
decisively, because §3 shows neither is needed: the structure already prevents the
failure they would protect against, at an expected 1.1 retraces per encounter.
Recorded as the fallback to adopt if a future corpus revision breaks the §3 check.

**Retrace more than one step.** Declined for want of a rule to fix the number.
Two steps is as arbitrary as three, and the inventory shows one step always lands
somewhere with at least six exits, so the extra steps would buy nothing that can
be argued for.

**Route to some other node** — the alternative raised in the supervisor meeting.
Any such rule needs a way to choose the node, and inventing a transition the
corpus did not draw runs straight into the no-synthesis discipline the whole
structural layer rests on. The one legitimate source of a non-corpus edge is the
declared synthetic pre-intrusion overlay, and §3 settles that empirically: the
overlay **reconnects none of these sinks**, so reusing it supplies no destination
and the alternative has nothing to draw on that would not be freshly invented.
Declined, and declined on evidence rather than on principle alone.

**Keep accept-and-censor.** Retained — as an *arm*, not as the default. It is
experiment 1's behaviour and the only way to measure what the policy change did,
so the policy is a run input with two values rather than a replacement (§6).

## 6. What it records, and the comparability break

**A retrace emits its own record**, tagged `RETRACE`, carrying the sink it
retreated from in `place`, the destination in `next_place`, an empty verb, zero
dwell and its own place class. Two rejected treatments explain the choice. A
retrace that emitted *no* event would be invisible to every analysis, and the
action-budget decomposition is what made experiment 1 legible in the first place.
A retrace that emitted an *ordinary* event would inflate the action count and
quietly change every per-action metric.

The consequence for the metric suite is stated here rather than discovered later:

- **Attempted-action counts, blocked fractions and verb mixes are unaffected.** A
  retrace dispatches nothing, so it enters no action denominator.
- **Step counts rise**, by exactly the number of retraces.
- **Elapsed time rises**, by the re-paid dwells (§4).
- **Terminal-mode distributions change by construction**: runs that used to end
  `sink` now end `horizon` or `sim_end`. That is the intended effect and must not
  be read as the attacker having improved.
- **The number of retraces per run is itself reported**, because §3's no-oscillation
  argument is a claim about these nets that the runs can check, and a policy whose
  own firing rate went unmeasured would be taking §3 on trust.

**The comparability break, stated plainly.** Profiles that previously ended early
now run to the horizon, so their event counts and observation windows change for a
reason that has nothing to do with the attacker being better. **Experiment 2's
numbers under the retrace policy cannot be pooled with experiment 1's**, and any
before-and-after presentation of the two would be reporting a policy change as an
improvement. This is why the policy ships as a two-valued run input: the paired
contrast at fixed seed, `censor` against `retrace`, is the only honest way to say
what the change did, and experiment 2 runs it.

## 7. What the build is verified to do

The mechanism is a run input, `sink_policy`, on `run_movement` and on the driver,
defaulting to `"censor"`. The default is deliberate and follows the registry
convention the mapping and overlay versions already established: **an unqualified
run reproduces what has always run**, and an experiment names the policy it wants
at its own seam.

| gate | evidence |
|---|---|
| `censor` is bit-identical to today | every profile × seed × MTD condition × mapping compared field for field against the pre-change driver |
| retrace fires where the censor arm died | the profiles the inventory names reach the horizon instead of a sink |
| a retrace consumes no time itself | every retrace record has zero dwell and equal start and end times |
| the walk consumes time across a retrace | elapsed time strictly increases across every retrace cycle, because the re-visit pays a dwell |
| no walk loops without consuming time | the `max_events` backstop does not fire on any profile at either policy |
| retraces are rare, as §3 predicts | measured retraces per encounter against the predicted ~1.1 |
| determinism (SIM-05) | the same seed gives the same walk twice under either policy; the policy draws no randomness of its own |
| the entry-place clause is reachable and correct | a synthetic net whose entry place is a sink censors rather than retracing |

## 8. Where this connects, and when to update

- **Supersedes:** the accept-and-censor ruling in
  [`runtime_verification.md`](runtime_verification.md) §P7, which stands as the
  experiment-1 behaviour and is retained as the comparison arm.
- **Consumed by:** [`experiment_02_findings.md`](experiment_02_findings.md), which
  runs the paired policy contrast and reports the comparability break.
- **When to update:** if the corpus, the profile partition or the synthetic
  overlay changes, because §3's inventory is a check against those artefacts and
  not a property of the mechanism; if a net ever appears whose sink in-neighbour
  has out-degree 1, which promotes the edge-suppression alternative in §5 from
  declined to required.
