---
status: durable
created: 2026-07-04
topic: operational validation — the epistemic bar for the state-duration catalogue and its calibration
---

# Operational validation is the bar — how per-tactic durations are allowed to be defended, and the claim they license

## Why this is worth recording

The L3 state-duration work
([`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md))
attaches a dwell time to every ATT&CK tactic, and no ready-made resource maps
tactics to durations — Hong's D4 explicitly authorises "a reasonable, justified
number" where none exists. The unglamorous truth is that most of these numbers
will be **estimated and then tuned** so the emergent Petri-net timelines look
like what the breach literature says APT campaigns look like. Left unnamed, that
reads as "fitting the answer" and a reviewer kills it. **Named, it is a
recognised simulation-methodology strategy** — and naming it is the move that
converts the weakest-looking part of the executable track into a defensible
methodological contribution, which is exactly the register Hong asked for
("define this yourself, with justifications"). This note fixes *the bar*: what
standard of evidence each duration must meet, and — just as important — what
claim the calibrated catalogue is and is not allowed to make. It is the
methodology-chapter paragraph on validity, written before the numbers exist so
they cannot be back-rationalised.

## The substance

### The problem restated honestly

A discrete-event simulator needs a time on every attacker state (D4). For the
scan/exploit-shaped tactics the substrate already prices the action
(`ATTACK_DURATION`, `exploit_time`) — those are *input-validated* by inheritance
and not in question here. The difficulty is the stealth/low-and-slow tactics —
defence-evasion, persistence, execution, command-and-control, exfiltration —
which have **no substrate verb and no isolated observable in the literature**.
Nobody publishes "how long does defence-evasion take" as a quantity, because it
is not one: it is a micro-parameter of a model, not a measurable property of the
world. So it cannot be *input-validated* (there is no ground-truth input to
match). This is not a defect of our model — it is the generic condition of every
mechanistic simulation with unobservable internals.

### The bar: validate the output, not the input

The recognised answer is **operational validation** (Sargent's simulation
validation taxonomy) / **pattern-oriented modelling** (Grimm et al., in the
agent-based-modelling literature): when a model's internal parameters cannot be
measured directly, you **calibrate them so that the model's *observable output*
reproduces observed real-world patterns**, then report the sensitivity of the
conclusion to those parameters. The unobservable dwell times are the free
parameters; the *observable* is the campaign timeline shape — dwell time,
breakout time, time-to-impact — which the breach literature **does** report.
Tuning the former to reproduce the latter is a named, defended strategy, not a
hack.

So the bar for a duration value is one of three tiers, in descending strength:

1. **Input-validated** — the value is fixed by the substrate (Tier 1). Not
   tuned. The anchor.
2. **Output-validated (calibrated)** — the value is a free parameter chosen so
   the emergent timeline matches a *literature-reported campaign pattern it was
   fitted to*. Defensible, but weak on its own (see circularity, below).
3. **Face-valid + swept** — no calibration target exists even at the macro
   level; the value is a stated estimate with a written justification and a
   declared sweep range, and the conclusion is shown robust across the range.

Every entry in `tactic_durations.json` must be honestly badged as one of these.
The tier badge *is* the validity claim.

### The four rules that keep operational validation from becoming circularity

"We tuned the durations to match literature timelines, and look — our timelines
match the literature" is circular if presented as validation. Four disciplines,
all cheap, convert it into a genuine (if weak) claim. These are load-bearing —
they are the difference between a method and a fit:

1. **Don't tune the anchor.** Tier-1 substrate-sourced values stay fixed.
   Calibration only moves the non-substrate tactics.
2. **Group, don't free-fit.** Tune a small number of *class multipliers*
   (scan-shaped / exploit-shaped / stealth-low-and-slow / objective-execution),
   not ~14 independent dwells. Fewer free parameters against the same targets is
   less overfit and more identifiable, and the per-tactic profile files justify
   which group each tactic joins — a *qualitative* claim the literature can
   support even where numbers don't exist.
3. **Hold out an observable.** Calibrate on one pattern (e.g. dwell-time shape),
   then check a *different, un-targeted* pattern (e.g. breakout-time shape)
   emerges approximately right. One held-out pattern is the difference between
   fitting and predicting.
4. **Keep the claim modest.** The output is "plausible, literature-bounded,
   sensitivity-swept" — never "a validated APT timing model".

### Shape, not scale — the time-scale resolution this depends on

Operational validation here is deliberately of **timeline shape** (orderings and
ratios), not absolute duration. The substrate prices actions in tens-to-hundreds
of simulated seconds; the literature observables live in hours-to-months. You
cannot match both absolute real-world timelines *and* keep substrate-comparable
MTTC — if persistence dwells for literature-months while an exploit takes
substrate-seconds, the timeline degenerates to pure stealth-dwell and the MTD
comparison dies. So the literature supplies *relative structure* (e.g.
"stealth-dwell is ~10³× an exploit action"), absolute scale is anchored to the
substrate's Tier-1 values, and the calibrated claim is "the emergent timeline
*shape* reproduces reported APT campaign structure". This is also the only
honest claim available — the substrate network is synthetic, so absolute realism
was never on the table — and it is sufficient for the thesis punchline, which is
itself a ratio game (MTD shuffle interval vs tactic dwell, per
[`./2026-06-18_cti_to_executable_behaviour.md`](./2026-06-18_cti_to_executable_behaviour.md)
§6).

### What "the corpus supplies no timing" does and does not forbid

The hard constraint "timing never comes from the corpus" is about the **Attack
Flow corpus and `observation_count`** — structure and chaining are CTI's
contribution, `observation_count` is "how often the analyst drew it", not a rate
([`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(f)). It does
**not** forbid using breach-report *statistics* (M-Trends dwell, breakout time,
DBIR, ransomware time-to-impact) as calibration targets — those are Tier-2
literature, and they are exactly the observable patterns operational validation
calibrates against. The two must not be confused; the catalogue header should say
so in a sentence.

### Why this is a contribution, not an apology

The gap Hong named — no resource maps tactics to durations — makes the sparse
precedent survey a *result*, not a failure: the absence is the citable gap
statement. That survey is now done
([`./2026-07-04_tactic_duration_precedent_survey.md`](./2026-07-04_tactic_duration_precedent_survey.md))
and confirms it: **no prior work assigns justified per-ATT&CK-*tactic* durations**
— the one tactic-level ATT&CK Petri-net model (Rodríguez 2024) is untimed, and
every timed APT model that carries ATT&CK labels attaches timing at the
*technique/CVE* level or declares its rates outright. Supplying a **transparent,
tiered, calibrated-with-declared-limits** tactic→duration layer, with the
validity of each number badged and the conclusion shown robust to it, is a
methodological artefact the field does not currently have.

The same survey also found that this method *extends* the field norm rather than
falling short of it. The dominant practice in timed APT/MTD models is
**declare-the-rate + sensitivity-sweep** (Bland 2020's SPN rates are stated
"arbitrary … later determined by subject-matter experts", with the net structure
*face-validated* by 14 SMEs; McQueen 2006 sets a stage mean "somewhat
arbitrarily" and anchors another empirically; enterpriseLang/MAL ships
expert-declared per-technique TTC distributions). Genuine empirical timing exists
only at exploit/CVE granularity (Ling & Ekstedt 2023). So Tier 3 (declared +
justified + swept) is not a concession — it is *exactly what the field already
does*, and calibrating the declared values to macro observables is a step further
than the norm. The honest framing throughout is the same as the project's
governing claim (architecture §(j)): *fidelity changes the answer*, never "the
model is true".

## How it connects

- To open work: this note *is* the validity rationale for
  [`../handoffs/2026-07-03_l3_state_durations.md`](../handoffs/2026-07-03_l3_state_durations.md)
  (the tier hierarchy, the calibration step, the sweep ranges) and constrains
  the per-tactic profile files that feed its Tier-2/3 entries. The calibration
  loop consumes the timeline runner
  ([`../handoffs/2026-07-03_l3_timeline_runner.md`](../handoffs/2026-07-03_l3_timeline_runner.md)),
  so ordering is: profile files → catalogue v0 (uncalibrated priors + ranges) →
  runner → calibrate within ranges → catalogue v1 (frozen).
- To the spec: sits under the D4/D10 duration regime recorded in
  [`../specs/provenance.md`](../specs/provenance.md) and
  [`../specs/architecture.md`](../specs/architecture.md); the "shape-not-scale"
  comparability boundary is governed by
  [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md) §(d)/§(f).
- To the lit review: the calibration-source survey (Bland 2020, Mendonça 2023,
  Rodríguez 2024 for *where transition rates come from*; M-Trends / breakout /
  Sophos AAR for macro targets) is compiled in
  [`./2026-07-04_tactic_duration_precedent_survey.md`](./2026-07-04_tactic_duration_precedent_survey.md);
  new extraction candidates it surfaced (Ling & Ekstedt 2023, McQueen 2006, Xiong
  2021) go under [`../extractions/`](../extractions/) after reconciliation.
- To the methodology chapter: this is the "threats to validity / how the timing
  layer is defended" section, drafted early so the numbers can't be
  back-rationalised.

## When this would need updating

- If the **substrate adopts real (NVD) CVEs** — more tactics become
  input-validated (Tier 1) and the calibrated surface shrinks.
- If a **precedent that assigns per-tactic durations with justification** turns
  up in the survey — the gap statement weakens and this note reframes around
  positioning against that precedent rather than filling a void.
- If the **timeline runner shows the conclusion is *not* robust** to the swept
  durations — operational validation has failed for this model and the finding
  itself (the MTD ranking) inherits that fragility; the note is rewritten around
  the negative result rather than the method.
- If Marc/Hong **reject shape-not-scale** in favour of absolute-time realism —
  the time-scale clash re-opens and the two-regime alternative (rejected here)
  must be revisited.
