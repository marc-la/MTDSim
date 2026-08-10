---
status: superseded by 2026-08-10_predictability_instrument.md
created: 2026-08-09
---

> **Superseded 2026-08-10** by
> [`2026-08-10_predictability_instrument.md`](2026-08-10_predictability_instrument.md)
> (Marc's reframe: the missing instrument is a detectability-grade scalar for
> strategic plurality itself — predictability — and this brief's
> failure-conditioned reading survives inside it as the per-verdict
> decomposition, layer 4). The census gate, both free nulls, the M1/M2
> separation and the advantage ceiling are carried forward wholesale; delete
> this file on the next sweep.

# Instrument plural recovery on axis 4 — turn "reacts, without advantage" into "a demonstrated plural recovery repertoire", measured on the failure column

## The claim this exists to support

The dissertation frames robustness in two halves. On a **success** verdict the
attacker progresses on objectives as a function of the out-transitions available
to it — the tactic parameterisation set's half, largely banked (§State of play).
On a **failure** signal, the model does not fall back on one fixed rule: it has
a **plurality of preferred bounce-back routes** for recovering from the
temporary setback. That second half is the claim this handoff instruments. It is
currently assertable only from the design; nothing on record measures it.

**The honesty ceiling, fixed before any work starts.** Experiment 2's
verdict-blind ablation stands: routing on the substrate's verdict is
approximately free in *outcome* terms, on 1 600 paired runs
([`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
§11). Nothing here may claim the model "adapts usefully" or that recovery
confers advantage. But experiment 2 tested **progression measures only** — it
showed the redirection is outcome-free, not that redirection is absent. The
claim in reach is **distributional**: after a failure signal the model redirects
into a preferred *mixed set* of routes, demonstrated by contrast against the
verdict-blind and uniform nulls, with the outcome negative reported alongside in
every record and caption. The claim is also **conditional-stationary-policy**:
the failure column is a static declared weight set, and the verdict selects
between two static mixtures — this is not learning (axis 7) and not within-run
strategy revision. "Plural recovery repertoire", never "useful adaptation".

## State of play

**Built and verified.** The M2 loop: the substrate's verdict selects between the
success and failure columns of the outcome overlay
(`OutcomeOverlay.compose(place, verdict, base_out)` in
[`outcome.py`](../../src/mtdsim/l3_simulation/controller/outcome.py), design in
[`success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md));
M1, the severing MTD interrupt, throws position back. Both operate
([`runtime_verification.md`](../implementation/pipeline/ogasp/runtime_verification.md)).
The **verdict-blind arm already exists as a value change** — an overlay with
empty value tables, composition passing everything through at 1.0 (experiment 2
§11) — and the **uniform-weight null** shipped on
`feat/plural-preference-instrumentation` as `uniform_weight_variant`
([`net.py`](../../src/mtdsim/l3_simulation/movement/net.py)).

**Why the reported axis-4 readers cannot carry the framing.** The framing's
load-bearing noun is *plurality* — a claim about the **shape of a distribution**
over recovery behaviours — and all three readers are scalars:

- `recovery_times` says *how long* until any success, not *which way* or *how
  many ways*; its recorded blind spot ("recovery" = any success, not recovery of
  what was lost) makes it worse for this claim, not better.
- `interrupt_action_mix` conditions on MTD interrupts rather than failure
  verdicts, and measures *change* in mix before versus after — a rigid
  single-fallback rule also changes the mix, so it cannot distinguish one strict
  bounce-back rule from a preferred mixture. No support/concentration reading.
- `failure_routing_rate` counts how often the failure column is consulted,
  nothing about the mixture it induces once consulted.

**The machinery to reuse arrived 2026-08-09.** `hill_diversity` /
`HillDiversity` (support N, effective number D = 2^H, evenness D/N),
`dimension_counts`, `jsd`, `normalise`, `interval_report` — all in
[`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py), committed
with [`plural_preference.md`](../implementation/pipeline/ogasp/plural_preference.md).
**This handoff depends on that branch** (`feat/plural-preference-instrumentation`,
`1da2e7a`); build on it or after its merge.

**Never measured, anywhere:** the failure-verdict event count per run per
profile per arm. Everything below is gated on that census coming back dense
enough to estimate a conditional distribution.

## Recommended approach

Three layers, cheapest first. Two conditioning events, **never pooled**: the
failure verdict (M2) and the severing interrupt (M1) are different setbacks with
different physics; instrument both with the same machinery, report them apart.

### 0. The failure-event census (gates everything)

Count failure verdicts and severing interrupts per run per profile per arm from
recorded runs before designing anything. The undersampling lesson travels: 10
opening draws read evenness 1.00 and proved nothing
(`plural_preference.md` prereg; the plural-preference handoff's §State of play).
A profile × event cell too sparse to populate a distribution is reported as
unestimable, not massaged.

### 1. Declared layer — run-free, from the overlay tables

Per verdict-carrying place: `hill_diversity` of the composed **failure-column**
out-distribution (`compose(place, "failure", base_out_weights(place))`),
side by side with the success column. Failure-column D > 1 with evenness < 1
states the *declared* recovery repertoire is a preferred mixture, not a single
fallback — the framing read directly off the model's own parameterisation. The
success column's mean effective out-degree is the same statement for the
progression half (the tactic parameterisation set's breadth, as a Hill number).

### 2. Realised layer — windowed, from recorded runs

For each failure verdict: the next transition taken, and a next-*k* window
signature (verb mix, place-class mix — `interrupt_action_mix`'s window
machinery, re-conditioned). Pool per profile; `hill_diversity` on the
conditional distribution. 1 < D < N with evenness < 1 is realised plural
recovery — the plural-preference table's third regime, conditioned on failure.
Windowed, never outcome-shaped: the degenerate region (no attacker completes at
200 s) binds outcome measures, not these. Sibling reading conditioned on
severing interrupts, reusing `refoothold_times`' event definition.

### 3. Redirect layer — the clincher, with both nulls free

`jsd(post-failure ‖ post-success)` conditional next-step distributions, within
arm. Then the contrast that makes it a finding:

- **Verdict-blind arm** — post-failure ≡ post-success *by construction*, so its
  JSD statistic is the exact null distribution, at zero build cost. If the
  shipped arm CI-separates from it, failure-conditioning demonstrably redirects
  effort into a distinct set of routes — the claim experiment 2 never tested.
- **Uniform-weight arm** — same support, preference stripped: separates
  recovery plurality the *weights* prefer from plurality the *graph* forces
  (the P1 lesson — a hub must not manufacture the result).

Matched seeds across the three arms; `interval_report` on every aggregate; no
ordering claim without disjoint intervals.

### Alternatives considered, and why this wins

- *Extend `interrupt_action_mix` with more mix categories.* Still measures
  change, not shape; cannot separate one fallback rule from a mixture. Rejected.
- *Outcome-shaped recovery measures (success rate after setback).* Dead twice
  over: the degenerate region, and the advantage wall — any positive would
  contradict a 1 600-run control. Rejected.
- *A sixth modulator or any new mechanism.* The axis context's own §1: five
  swept modulators all narrow traversal; the move with the most evidence against
  it. Rejected without reservation.

## Validation gate

1. **Pre-registration committed before any arm is run** (§Pre-register),
   git-history-dated.
2. **The census reported first**, with the sparsity ruling per profile × event
   cell made on its numbers.
3. **The three-arm table**: declared and realised D / evenness and redirect JSD,
   per profile, both conditioning events, `interval_report` intervals
   throughout; the shipped arm's unconditional numbers reproduce
   `plural_preference.md` where they overlap.
4. **The clincher stated whichever way it lands**: is the shipped arm
   CI-separated from the verdict-blind null on redirect JSD, per profile? Report
   where it is *and* where it is not.
5. **Experiment 2's outcome negative quoted next to any positive** — no figure
   or sentence carries the distributional result without the advantage boundary.
6. **Full `tests/l3_simulation` plus substrate/carve/golden suites pass**;
   readers only — a moved golden means the shipped walk changed and must be
   explained, not accepted.
7. **Record** at
   `docs/implementation/pipeline/ogasp/plural_recovery.md`: census, measures,
   three-arm table, clincher verdicts, and the ruling on what the thesis may
   claim — plus a **cross-reference into
   [`plural_preference.md`](../implementation/pipeline/ogasp/plural_preference.md)**:
   its hard constraint reads "do not let any figure read as axis-4 adaptation";
   this work is the axis-4 sibling done *deliberately*, under its own record and
   its own ceiling, and the two records must say so rather than appear to
   contradict.

## Pre-register before running

- **P1 — direction.** Declared failure-column D > 1 on the majority of
  verdict-carrying places; realised post-failure evenness < 1 (a preferred
  subset, not uniform dithering); shipped-arm redirect JSD CI-separated from the
  verdict-blind null on the majority of estimable profiles, for the M2 event.
- **P2 — kill criterion.** Shipped and verdict-blind arms CI-indistinguishable
  on redirect JSD ⇒ "the failure column induces no distinct recovery mixture" —
  reported as the axis's second measured negative, never massaged. A claim
  surviving only at the declared layer is a *declared-not-realised* claim and is
  reported as exactly that.
- **P3 — seed count** fixed by a convergence check on the conditional
  distributions (post-census, pre-run), shared across arms and events.

## Hard constraints

- **No advantage phrasing, anywhere, ever.** The experiment 2 negative is the
  standing boundary and travels with every figure. "Redirects into a distinct
  preferred set" — never "recovers better", "adapts usefully", or any
  outcome-comparative form.
- **Conditional-stationary-policy boundary.** Static failure column; the
  verdict selects between two static mixtures. Not axis 7, not within-run
  strategy revision; read
  [axis 7's context](2026-08-09_axis7_learning_context.md) before touching
  anything experience-shaped.
- **Readers move no badge.** Axis 4's badge turns on advantage and holds on a
  control; expect it to stay DESIGNED. This builds **thesis-argument evidence**,
  the same superset-of-badge move `plural_preference.md` made for axis 3.
- **M1 and M2 windows stay distinct** — under MTD arms, failure-verdict windows
  and interrupt windows overlap; the recorded blind spots (run edges,
  double-counted bursts) travel with any use.
- **The reported-configuration pin** — modulators null is the arm; the shipped
  overlay is the mechanism under measurement
  ([`model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)).
- **Scores move on evidence only** (S6;
  [`../workflows/guardrails.md`](../workflows/guardrails.md)) — never retune
  the failure column to deepen its plurality.
- **The label-drift trap** — recorded runs carry pre-2026-08-06 profile names;
  normalise off the corpus, refuse empty cells (`plurality_reporting.md` §7).
- Determinism (SIM-05); cross-arm comparisons effort-denominated, never
  time-denominated; Australian English; branch per session; commit locally;
  **never push** without an explicit ask.

## Reading list

- [`2026-08-09_axis4_adaptivity_context.md`](2026-08-09_axis4_adaptivity_context.md)
  — the axis context this executes against: the measured negative, the four
  readers' blind spots, the constraints.
- [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  §11 — the verdict-blind arm's construction and the outcome negative, verbatim.
- [`../implementation/pipeline/ogasp/plural_preference.md`](../implementation/pipeline/ogasp/plural_preference.md)
  + [`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py) Hill
  section — the measure, the regime table, the prereg pattern to copy.
- [`../implementation/pipeline/ogasp/success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  + [`outcome.py`](../../src/mtdsim/l3_simulation/controller/outcome.py) — where
  the failure column is declared and composed; the declared layer reads here.
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(b) — the four axis-4 readers and the blind spots that travel.

## Out of scope (explicitly)

- **Any new mechanism, modulator, or weight re-declaration.** All three arms are
  reads of what exists; the verdict-blind arm is experiment 2's, unchanged.
- **Moving the axis-4 badge**, or re-scoring any row.
- **Learning / experience-conditioned routing** — axis 7's programme, ~14 000
  runs, separately closed.
- **Defence-conditioned variants** — axis 8 is closed on evidence; the axis
  context's §6 names the wall.
- **Re-running experiment 2's progression comparisons** — the outcome negative
  is settled and is quoted, not re-litigated.
- **Dissertation prose and chapter placement** — the record names what may be
  claimed; where it lands is a later pass.
