---
status: durable
created: 2026-07-29
topic: "The sink-retrace policy (S5) — design record written before the build. Why the handoff's recommended route cannot fire where it was aimed, the predecessor-side rule that replaces it, the one-shot edge suppression that answers the oscillation question, and the three consequences (time cost, record semantics, comparability break) the supervisor asked to see thought through before three lines of code were written."
updated: 2026-07-29
---

# Sink retrace — the design, and its consequences, before the build

**Status:** durable design record, written under the S5 ruling and **before the
implementation**, because the meeting asked for the thinking rather than the patch.
It supersedes the accept-and-censor behaviour recorded at
[`runtime_verification.md`](runtime_verification.md) §P7, which stands as
experiment 1's arm and is not re-run.

## 1. The ruling, and what it replaces

A walk that reaches a **sink** — a tactic-place with no base out-edges — currently
stops, and the run is censored ([`attacker.py`](../../../../src/mtdsim/l3_simulation/movement/attacker.py)
returns at `next_place is None`). Marc ruled on 2026-07-21 that the token should
instead **retrace the edge it travelled**; routing to some other node was raised in
the same meeting as an alternative (§7).

The cost of the current behaviour is on record and is not hypothetical:
`pure_steal` terminated at the `impact` sink in 9 of 10 runs and
`double_extortion` at `credential-access` in 10 of 10, so those profiles observed
74–210 actions per run against roughly 500 for the profiles that ran to the horizon
([`experiment_01_findings.md`](experiment_01_findings.md) §5). Their per-profile
timing denominator is shorter than everyone else's for a reason that has nothing to
do with the attacker.

**The sink set is current.** Enumerated against today's nets rather than quoted from
the older table, and it reproduces §P7 exactly:

| profile | sinks (overlay-on) | sinks (observed-only) |
|---|---|---|
| `aggregate` | — | — |
| `pure_steal` | `impact` | `impact` |
| `pure_impediment` | — | — |
| `double_extortion` | `credential-access` | `credential-access`, `reconnaissance`, `resource-development` |
| `infrastructure_setup` | `defense-impairment` | `defense-impairment`, `reconnaissance`, `resource-development` |

Sinks are corpus structure — a place has no out-edge because the analyst-drawn flows
drew none leaving it — so neither the partial mapping nor the distance-weighted
transitions remove them. The policy handles them at runtime; nothing is added to the
nets.

## 2. Where the handoff's recommended route fails, and why that matters

The handoff recommended, in preference order, that arrival at a sink be *treated as a
failure verdict so the failure-side weighting routes the token away*, on the grounds
that it reuses a mechanism that already exists rather than adding a special case.

**That rule cannot fire where it is aimed.** The overlay conditions a base
out-distribution; `compose` multiplies base weights by per-pair factors and
renormalises. At a sink the base out-set is *empty*, so there is nothing to condition:
every verdict — success, failure, or `VERDICT_NONE` — yields `{}` at that place. No
weighting, however aggressive, routes a token out of a place the corpus gave no exits.

The recommendation is repairable rather than wrong, and the repair is the design: the
verdict-shaped re-route has to act at the **predecessor**, which does have an out-set,
not at the sink. Recording this is worth more than quietly doing something else — the
handoff's reasoning was that the verdict route "reuses a mechanism that already
exists", and the mechanism it reuses turns out to be the ordinary place visit, not the
overlay.

## 3. The design

**Definition.** When the token's routing at place `s` yields no destination *and* `s`
is a sink, the token moves back to `p`, the place it arrived from, and `p` is visited
in the ordinary way. The edge `p → s` is suppressed **for that one selection only**.

Stated as the four things the handoff asked to be decided:

### 3.1 What stops it walking straight back into the sink

The one-shot suppression of `p → s`, and nothing else. The next selection at `p` is
drawn from `p`'s composed distribution with that single destination removed and the
remainder renormalised; every later visit to `p` sees the full out-set again, because
returning to the same tactic on a later occasion is ordinary behaviour, not
oscillation.

**This is the one genuinely new policy in the design, and it is declared as such**
rather than presented as reuse. Everything else here is an existing mechanism.

**It cannot strand the token.** Checked against the nets rather than assumed — every
predecessor of every sink, with its out-degree and its alternatives once the sink edge
is removed:

| profile | sink | predecessor | P(sink) at base | out-degree | positive mass remains? |
|---|---|---|---:|---:|---|
| `pure_steal` | `impact` | `discovery` | 0.000 | 9 | yes |
| | | `execution` | 0.059 | 11 | yes |
| | | `stealth` | 0.000 | 12 | yes |
| `double_extortion` | `credential-access` | `command-and-control` | 0.111 | 9 | yes |
| | | `execution` | 0.000 | 8 | yes |
| | | `initial-access` | 0.000 | 7 | yes |
| | | `lateral-movement` | 0.000 | 6 | yes |
| `infrastructure_setup` | `defense-impairment` | `command-and-control` | 0.000 | 8 | yes |

Every predecessor keeps between five and eleven alternatives. The suppression is
therefore never the difference between moving and not moving, on this corpus, today.
Because that is a corpus property and not a guarantee, the build **walks further back**
if suppression ever does empty an out-set (§3.5), and the case is tested rather than
argued away.

### 3.2 What it costs in time — nothing new, which is the point

The handoff is right that a zero-time retrace is an infinite loop in zero simulated
time, which is a hang rather than a result. This design pays time **without declaring a
new parameter**: the retrace's cost is the ordinary cost of visiting `p` again — one
draw from the declared S3 timing source at `p`, exactly as any other visit to `p` draws.

That falls out of the decision to re-*visit* the predecessor rather than merely
re-*route* from it. Re-routing without re-visiting would need a synthetic verdict at
`p` (no verb ran, so there is no substrate outcome), and fabricating a verdict is what
the movement layer refuses to do everywhere else. Re-visiting invents nothing: the
attacker is back at that tactic, so it performs that tactic, the substrate judges it,
and the routing conditions on a **real** verdict. The S3-R rule — the movement layer
supplies every unit of the attacker's time — is untouched.

### 3.3 What it records — an ordinary event, explicitly flagged

Neither of the handoff's two feared options is taken. It does **not** emit nothing (a
retrace invisible to every analysis, when the action-budget decomposition is what made
experiment 1 legible). It does **not** emit an ordinary event silently (which would
inflate the action count and quietly change every per-action metric).

It emits an ordinary event **carrying a `retrace` flag**, so:

- every per-action metric can be computed with retraces in or out, and the write-up
  says which;
- the retrace count per run is itself a measurement — how often a profile is walking
  into its own dead ends is a property of that profile's net worth reporting;
- nothing is quiet. The inflation is real behaviour (the attacker really does perform
  that tactic again), and it is separable.

**The flag is on the record, not a new outcome tag**, so the existing outcome
vocabulary and the `place_class` split are unchanged and no reader breaks. Explicitly
rejected: recording the retrace as `verb=""`. The measurement suite reads a verbless
record as a dwell-only visit, so that choice would silently inflate
`dwell_only_fraction` and every denominator built on it — a bookkeeping decision
corrupting a measure, which is the failure mode this project has already recorded once.

### 3.4 Whether it needs a budget — no, and the reason is checked

The handoff's worry is a walk that "oscillates between two places for the rest of the
run, producing a great many events and no information". Three things bound it, and
none is a new parameter:

1. The one-shot suppression makes the immediate next move something *other* than the
   sink, always.
2. Every retrace costs a full timed visit, so retracing consumes the horizon at the
   same rate as any other behaviour. There is no zero-time cycle to spin in.
3. The existing `max_events` backstop (50 000) still terminates a pathological run.

A separate retrace budget was considered and **declined**: it would be a declared
parameter with no evidence behind its value, added to bound a behaviour that the three
mechanisms above already bound. What the build does instead is **count** retraces and
surface the count, so if the frequency turns out to be high that is data, reported —
not a knob quietly holding it down.

### 3.5 The degenerate cases, handled rather than assumed away

- **Suppression empties the out-set at `p`.** Cannot happen on today's corpus (§3.1).
  If it ever does, the token retraces a further step — `p`'s own predecessor — and so
  on up the visited stack.
- **The stack is exhausted** (the sink is reachable only by a chain that walks back to
  the entry place with nothing left). The walk terminates as it does today, recorded
  distinctly so it is never confused with a plain sink termination.
- **The token's first place is a sink.** No predecessor exists; terminate as today. Not
  reachable on the current nets (every entry place has an out-set) and handled anyway.
- **A stall** — the overlay suppressing every out-edge at a place that *does* have base
  edges — is a different condition and keeps its existing treatment. It remains
  representable and unobserved ([`weight_sensitivity_study.md`](weight_sensitivity_study.md)
  §2); the retrace policy deliberately does not absorb it, because a stall and a sink
  differ in what they mean: one is the verdict speaking, the other is the corpus.

## 4. The comparability break — stated here, not discovered by a reader

Profiles that previously ended early now run to the horizon. Their event counts,
elapsed windows and per-run denominators therefore change **for a reason that has
nothing to do with the attacker being better**.

- **Experiment 2's numbers cannot be pooled with experiment 1's**, and a
  before-and-after table would read as an improvement when it is a change of censoring
  regime. Any such table must carry this paragraph.
- The profiles affected are exactly those §1 enumerates. `aggregate` and
  `pure_impediment` have no sinks and are unaffected, which makes them the internal
  control on the change: if their numbers move, something other than the retrace moved
  them.
- Experiment 1's published magnitudes are **already** stale on other grounds — the
  substrate was re-baselined (`dd8c5ec`, `06ed8d9`) and the timing regime became S3-R
  after those numbers were taken ([`../../apt_model_criterion.md`](../../apt_model_criterion.md)
  §(f)). The retrace is the third reason, not the first, and the standing instruction
  is unchanged: re-measure the baseline in the same run.

## 5. What it does **not** do

It does not re-impose the substrate's native precondition order, and it must not be
allowed to look as though it does. The H-coupling finding — that walking CTI
tactic-order instead of the substrate's native order manufactures failure the baseline
never meets — is a result this evaluation exists to expose
([`experiment_01_findings.md`](experiment_01_findings.md) §3), and the S2 freeze holds.
A retrace routes around a **structural dead end in the corpus**, never around an
**unmet precondition in the substrate**: a blocked verb still costs its time, still
records `PRECONDITION_UNMET`, and still routes on the failure column exactly as
before. The two conditions are disjoint in the code and the tests pin that they stay so.

## 6. Validation gates for the build

1. No walk loops without consuming time — a seeded run's retrace events each carry a
   positive dwell, and the retrace count is finite.
2. A profile that previously died at a sink now continues: `pure_steal` and
   `double_extortion` reach the horizon where they previously terminated at 74–210
   actions.
3. Determinism holds (SIM-05): same seed → same walk, and no new RNG stream is
   introduced (the policy is deterministic given the walk's own history).
4. The two sinkless profiles (`aggregate`, `pure_impediment`) are **bit-identical** to
   a pre-retrace run — the change reaches only walks that meet a sink.
5. The suppression is one-shot: a test in which the token returns to `p` on a later
   occasion sees the full out-set.
6. Retrace and `PRECONDITION_UNMET` remain disjoint (§5).
7. The stack-walk and stack-exhausted paths are exercised on a constructed net, since
   the corpus cannot reach them.

## 6b. What the build found that the design did not anticipate (2026-07-29)

Two things surfaced while the gates were being written, and both are recorded because
they change how the policy must be *read*, not merely how it is coded.

**Carrying a sink and reaching one are different, and the synthetic overlay is the
difference.** `infrastructure_setup` has `defense-impairment` as a structural sink and
**never walks into it** with the synthetic pre-intrusion overlay on — 0 retraces across
ten seeds. With the overlay off it strands at `reconnaissance` / `resource-development`
and retraces freely (49 over the same seeds). So the overlay reconnects exactly the
places that would otherwise censor that profile, and the S5 policy is, for this profile,
an observed-only-arm mechanism. The consequence for reporting: a claim that "the retrace
un-censors three profiles" would be wrong on the overlay-on arm, where it un-censors
**two** (`pure_steal`, `double_extortion`). §1's table lists which nets carry sinks; it
was never a claim about which walks meet them, and the two must not be conflated.

**The retrace counter counts visits, not decisions.** The flag is set while the *sink's*
record is still being built, so it is consumed one iteration later — it belongs to the
visit the token stepped back *into*, not to the sink it stepped back *from*. The counter
increments on that consumption, which makes "retraces" mean *retraced visits that
actually happened*: a retrace chosen an instant before the sim ends produces no visit
and is not counted. The count and the number of flagged records are therefore equal by
construction rather than by coincidence, and a test pins it. The first implementation
put the flag on the sink's own record, and gate 6 caught it — which is the argument for
having written gate 6 at all.

**Observed magnitude.** On `v2_partial`, no MTD, seed 0: `pure_steal` goes from 14
events terminating at a sink to 479 running to the horizon (4 retraces), and
`double_extortion` from 144 to 427 (4 retraces). Retraces are well under 1 % of steps in
every cell measured, which is the evidence behind §3.4's decision to count rather than
budget. The compromise counts move too — `pure_steal` 0 → 3 hosts, `double_extortion`
3 → 9 — which is the censoring's cost made concrete, and is exactly why experiment 2's
numbers cannot be pooled with experiment 1's (§4).

## 7. Alternatives considered

- **Verdict-side re-route at the sink** (the handoff's first preference). Rejected on
  the mechanics of §2: there is no out-set at a sink to condition. The design keeps its
  *intent* — a verdict-shaped response — by moving it to the predecessor.
- **Route to some other node** (raised in the meeting). Needs a rule for choosing the
  node, and any rule that invents a transition the corpus did not draw breaks the
  no-synthesis discipline the structural layer rests on. If it is ever taken up it
  should reuse the declared pre-intrusion structure
  ([`synthetic_overlay.md`](synthetic_overlay.md)) rather than inventing fresh edges.
  Recorded, not taken.
- **Retrace more than one step by default.** Rejected as unmotivated: one step is the
  ruling, and the multi-step walk exists only as the degenerate-case fallback (§3.5)
  rather than as the normal path.
- **A declared retrace budget.** Rejected — §3.4.
- **Adding transitions to the nets to remove the sinks.** Out of scope by the
  experiment-2 handoff and wrong in principle: sinks are corpus structure, and the
  no-synthesis discipline forbids drawing edges no analyst drew.

## 8. Where this connects

Supersedes [`runtime_verification.md`](runtime_verification.md) §P7's
accept-and-censor ruling for experiment 2 onward. Consumed by the demonstration-arms
run, whose axis-1 and axis-3 measures are read off walks this policy un-censors. The
bounded-retry treatment of a degenerate out-distribution in
[`success_failure_overlay_design.md`](success_failure_overlay_design.md) §6.1 is the
closest existing precedent for handling a place the walk cannot leave, and the stall
half of that treatment is deliberately left alone (§3.5).
