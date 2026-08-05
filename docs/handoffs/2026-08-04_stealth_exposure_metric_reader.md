---
status: open
created: 2026-08-04
updated: 2026-08-05
---

# Build the axis-5 exposure reader — a post-hoc, non-consequential detectability curve; unclaimed since the parent design record recommended it, now re-derived independently in the 2026-08-04 supervisor meeting with two concrete refinements

## This is now the single stealth handoff (2026-08-05)

**Marc's direction:** the latest framing is the major direction, and there should
be **one** handoff for stealth. `2026-07-29_stealth_tempo_via_dwell_channel.md`
— the mtd_ai-consequential route, option 1(b) — is retired into this file; what
is worth keeping from it is §"The 1(b) route" below. This handoff is the whole of
open stealth work.

The order of business is unchanged and is the reason the consolidation is safe:
1(a), the reader, is buildable **now** with no ruling; 1(b) needed a supervisor
ruling that has not been given, and needed an integration that does not exist.
Building the reader first is the same reader-first discipline the disengagement
measure and the measurement suite both follow.

## State of play

**This is not a new design — it is an unclaimed piece of an existing one, now
re-derived independently.**
[`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
§2(a) already names *"stealth as tempo, with exposure reported as a metric"* as
the **recommended buildable baseline** — a state that changes tempo, changes a
*reported* exposure figure, and is consumed by nothing else in the run. No
handoff was ever spun for it: the open chain
([`README.md`](README.md) item 20) only tracks option 1(b), the
mtd_ai-consequential route
(retired into this file — see "The 1(b) route" below),
which needs a supervisor ruling on sanctioning the reactive defender as an
experimental arm. Option 1(a) does not need that ruling and has sat unbuilt.

**The 2026-08-04 meeting (minutes: see the session's other output) reproduces
1(a) from scratch, unprompted, and settles its badge ceiling.** Marc's own
framing — *"would that be like a metric only... you wouldn't pump that into
the MTD... decision... just observing the detectability"* — is 1(a) stated in
plain language, and it resolves §9's open question in 1(a)'s favour: the
supervisor is asking for the metric, not for 1(b)'s mtd_ai integration, this
cycle. That is a reading of the meeting, not a formal disposition — the S2
freeze question §4 of the parent record still gates the *mechanism* half
(below), and this handoff does not treat the meeting as having ruled on it.

**Two things the meeting asked for, and only one is unblocked.** Re-reading
the parent record against what was actually described in the meeting exposes
a distinction the parent record's 1(a) does not itself draw:

1. **A reader.** Marc's own worked description is entirely post-hoc: *"you
   only run the attacks on the network, no MTD... and then you calculate the
   detectability shifts... calculate like a running average... for each
   attack."* Nothing here changes the attacker's behaviour — it is a derived
   statistic over an **unmodified** run's already-recorded action stream,
   exactly the shape of the attacker-disengagement measure
   ([`2026-08-01_attacker_disengagement_measure.md`](2026-08-01_attacker_disengagement_measure.md)):
   pure functions over records, no RNG, no golden move, **no S2 question at
   all**, because no attacker state is added. **This is buildable now, with no
   ruling.**
2. **A mechanism.** The parent record's 1(a), as specced in its §5/§6, is a
   stealth *state* that **scales dwell means** — it changes what the attacker
   actually does, even though the resulting exposure figure is then consumed
   by nothing. That is an attacker-state change and needs the S2 ruling the
   parent record already escalated. **Out of scope for this handoff**, tracked
   where it already is.

This handoff is (1) only. Building the reader first and cheaply, before any
ruling, is the same discipline the disengagement handoff and the measurement
suite both already follow (`measurement_suite.md`'s reader-first precedent).

## Recommended approach

### The quantity

For each attempted action `a_t` in a recorded run (baseline or profiled arm),
maintain a scalar detectability level `D(t)`:

```
D(t) = D(t⁻) · decay(Δt) + d(a_t)
decay(Δt) = exp(−Δt / τ)
```

- `Δt` — simulated time since the previous attempted action.
- `d(a_t)` — the detection increment of the action just taken (below).
- `τ` — a declared, swept decay half-life, in the units the movement layer
  already prices time in (S3-R; sim seconds, shape-not-scale).

This is continuous time-decay, not the parent record's §6 rule (which decays
on the *next noisy action taken*, an event-driven rule). The two express
different intuitions and are **not interchangeable**: event-driven decay says
only the attacker's own loud actions cost it what it built up; time-driven
decay says ambient network noise erodes any signal regardless of what the
attacker does next, which is Marc's own stated reasoning (*"as time passes...
you can't link within the timeframe that people are monitoring"*) and is
recommended as the primary candidate for this reason. **This is a design
choice for the building session to pre-register, not a resolved fact** — if
it is adopted, propose it back into `stealth_conceptualisation.md` §6 as an
amendment rather than forking a second, silently-divergent stealth dynamic;
that record is the parent and should stay the single source of truth for
stealth semantics.

### The detection increment `d(a_t)` — two sources, neither universal

Checked in code: `Service` objects already carry synthetic per-vulnerability
`impact`, `complexity`, `cvss = (complexity + impact) / 2`,
`exploitability = cvss / 5.5`
([`../../mtdnetwork/component/services.py:14-29`](../../mtdnetwork/component/services.py)),
generated uniformly at random per vulnerability instance — exactly the
"synthetic CSV... we normalise it" Marc described. But this quantity exists
**only for the vulnerability actually exploited**, i.e. only at `EXPLOIT_VULN`
dispatch. It has no natural reading for `SCAN_HOST`, `SCAN_PORT`, `ENUM_HOST`,
`BRUTE_FORCE`, or the seven tactics that dispatch nothing at all under
`v2_partial`. A CVSS-sourced rule therefore cannot cover the whole tactic
space the way
[`stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
§7's ordinal tier ranking already does — the two sources are **complementary,
not substitutable**:

- **`EXPLOIT_VULN`-dispatching actions:** `d(a_t)` sourced from the exploited
  vulnerability's `exploitability`, direction **inverse** — Marc's own
  framing (*"we'd use the inverse of that as like a detection [rate]"*): a
  more easily/quietly exploitable vulnerability needs a smaller footprint and
  is harder to notice. This is a declared judgement about *direction*, not a
  fact, and must be swept against the opposite reading (a higher-impact
  exploit is noisier) before either is reported as more than a candidate.
- **Every other dispatched or dwell-only action:** fall back to
  §7's tier ranking (0 = essentially unobservable … 4 = high-signal/noisy),
  mapped to a declared, swept increment band. This is consistent with, not a
  contradiction of, the meeting's own placeholder — *"we can just fix it...
  same weight for all six for now, my scan-host would be almost 0"* reads
  directly onto §7's tier 1–2 placement of scan-shaped tactics near the
  bottom of the ranking.

### Reporting

Per profile, per arm (baseline vs profiled), report `D(t)` as a curve and its
running mean, on the **no-MTD arm first** — Marc's own scoping (*"you only run
the attacks on the network, no MTD"*) and the cleaner comparison, since MTD
churn would otherwise confound tempo with interrupt recovery. This directly
extends the already-established event-wise baseline-vs-profiled contrast
([`stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
§1): the prediction to pre-register is that the baseline's mean `D` sits
higher than every profile's, at every declared `τ`/tier setting, because the
baseline has no non-action dwell to let `D` decay between events (§1.1) —
state this as a **prediction**, not a result, before the reader runs.

## Pre-registered conclusions — commit before any output, house discipline

| | Conclusion | Criterion |
|---|---|---|
| **E1** | Non-degenerate | mean `D` varies across the five profiles by more than its own dispersion, at the declared `τ`/tier setting |
| **E2** | Baseline separates from every profile | baseline mean `D` is higher than each profile's, CI-disjoint, on the no-MTD arm — the prediction above, reported whichever way it falls |
| **E3** | The CVSS-direction question is decided by evidence, not asserted | both directions (inverse and direct) computed; report which one is used and why, and flag it as declared judgement in the value-provenance ledger regardless of which wins |

## Validation gates

1. Unit gate: hand-built action streams with hand-worked `D(t)` — a burst of
   noisy actions (compounds), an idle gap (decays), a stealth-tactic-only run
   (stays low) — in `tests/l3_simulation/test_movement_measures.py` beside the
   existing readers.
2. Reader gate: full `tests/l3_simulation` + substrate/carve/golden suites pass
   **unchanged** — no attacker state added, no golden may move.
3. Determinism: re-derivation from re-created runs is exact.
4. Cross-arm gate: computes field-for-field on one seeded run of each arm,
   same keys both sides.

## Hard constraints

- **Metric only.** `D(t)` is never read by anything else in this build — not
  routing, not dwell, not any MTD selector. The parent record's 1(a)
  *mechanism* (dwell-scaling) and 1(b) (mtd_ai-consequential) stay separately
  tracked and separately blocked; do not fold them in here.
- **No threshold/flag.** A binary "detected" verdict is a follow-on
  decision-rule build (mirrors the disengagement handoff's own §7 reader/
  mechanism split) — report the continuous curve only.
- **No new declared family invented ad hoc.** Reuse `services.py`'s existing
  synthetic CVSS fields and §7's existing tier ranking; any new magnitude
  (τ, the tier→increment band) is tiered, swept, and logged in
  [`../implementation/declared_value_provenance.md`](../implementation/declared_value_provenance.md).
- **Reconcile with the parent record, don't fork it.** If the time-decay rule
  is adopted, amend `stealth_conceptualisation.md` §6 in the same commit
  rather than leaving two stealth dynamics on record.
- Determinism (SIM-05); envelope-not-actor; Australian English; branch per
  session; never push.

## The 1(b) route — absorbed from the retired tempo handoff, kept as the follow-on

Retained because it is the *only* route by which tempo becomes consequential, and
because its case was strengthened rather than weakened by later work. Not
licensed; recorded so the argument is not re-derived.

**The thesis.** No detection model exists to be stealthy against — except for one
defender. The reactive `mtd_ai` selector's decision state is assembled from
**attacker-derived** quantities (host compromise ratio, attack success rate, mean
time to compromise, RoA, risk, and the attacker's current phase). So a slower
attacker generates fewer attack events per unit time, which changes the metrics
the selector reads, which changes which mutation it chooses. The channel is
indirect and **already open**; no new detector is built and the reactive agent
runs unchanged.

**Why the case strengthened.** The cost-model cross-examination established that
under *time-triggered* mutation an attacker minimising declared duration is
already, mechanically, minimising expected mutation encounters (Spearman 0.87
between a tactic's declared cost and its interrupt rate). On a clock, patience is
pure exposure with no compensating benefit — so **a reactive defender is the only
channel through which slowness can ever be rational here**, which is exactly this
route's thesis.

**Four things it needs, in order, and none is cheap.**

1. **A supervisor ruling** sanctioning the reactive defender as an experimental
   arm — that agent is deferred to a later phase by standing project direction.
2. **An integration that does not exist.** The movement arm has never been run
   against the reactive selector at all; the L3 run wiring constructs the
   time-triggered mutation operation directly. This is the real cost.
3. **A defect fixed on that path** — any attacker sensitivity below 1.0 raises an
   unbound-local error, so the documented sensitivity experiment cannot currently
   run. Fix it, or run only at sensitivity 1.0, but decide rather than discover.
4. **A dwell-scaling hook.** The modulator seam is **routing-only**; the timing
   source observes each draw and delegates it unchanged. A dwell-primary stealth
   mechanism needs a seam change, not a new modulator.

**The cheapest form that tests the claim, and it should be run before any
mechanism is built.** Run the profiled attacker against the reactive selector
**as it is**. The profiles already differ in non-action share by more than a
factor of two — a naturally-occurring tempo spread. If the selector's mutation
choices do not differ across that spread, a declared stealth dial will not rescue
the claim and the cheap run has saved the expensive one. If they do differ, that
is the demonstration, obtained with no new attacker mechanism. Report the
**mutation-choice distribution**, not just the outcome: the claim is that tempo
changes *what the defender does*.

**Two constraints that survive with it.** Time-triggered MTD is unaffected by
tempo, so any stealth claim is bounded to the reactive arm and the write-up must
say so. And the attacker's stealth level must **never** be wired into the
defender's sensitivity parameter — that is reverse-modelling detection and
extending the inherited reactive machinery, both ruled out. The coupling stays
indirect: tempo changes the record, the record changes the state, the state
changes the choice.

**The badge boundary, unchanged.** A stealth claim here is a **tempo** claim.
Against the reactive selector a quieter attacker *starves* the defender's signal —
it is not evading detection, because nothing is detecting. Evasion (5b) has no
referent and stays NOT ADDRESSED; conflating them would annex the smart-attacker
work belonging to the learning and scheme-awareness axes.

## Reading list

- [`../implementation/pipeline/ogasp/stealth_conceptualisation.md`](../implementation/pipeline/ogasp/stealth_conceptualisation.md)
  §1 (the baseline-vs-profiled contrast this extends), §2(a), §6, §7, §9 (the
  badge-ceiling logic this build settles at DESIGNED), §13 (the four-item
  decision request the 1(b) route still needs ruled).
- [`../../mtdnetwork/component/services.py:14-29`](../../mtdnetwork/component/services.py)
  — the synthetic CVSS/exploitability fields.
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  and
  [`2026-08-01_attacker_disengagement_measure.md`](2026-08-01_attacker_disengagement_measure.md)
  — the reader-pattern precedent this follows exactly.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  axis 5 — the badge this reader can move to DESIGNED, and cannot move past.

## Out of scope

- The dwell-scaling stealth *mechanism* (1a as originally specced) and the
  mtd_ai-consequential route (1b) — both remain separately tracked, both
  gated on their own rulings.
- Any detection threshold or "detected" flag.
- Any coupling from `D(t)` back into MTD choice, routing, or dwell.
- Dissertation prose.
