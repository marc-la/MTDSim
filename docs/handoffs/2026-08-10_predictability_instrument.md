---
status: open
created: 2026-08-10
supersedes: 2026-08-09_axis4_adaptivity_context.md, 2026-08-09_axis4_plural_recovery_instrumentation.md
---

# Instrument predictability — one scalar for strategic plurality, applied to both attack models, with the scripted baseline at the boundary by construction

## The claim this exists to support

The thesis contrasts two attack models on the same substrate: the inherited
six-phase scripted attacker (the procedural baseline) and the movement attacker.
The baseline has **one behaviour** — its policy is a function, encoded in the
FSM. The movement attacker's policy is a **preferred mixture** of behaviours.
Nothing on record measures that contrast with one instrument applied to both
models; the tempo/stealth axis has its readers, strategic plurality has none.

**Fix the vocabulary once, and hold it** (downstream notes inherit these terms):

- **Strategic plurality** — the *property* claimed (as *stealth* is a property).
- **Behaviour composition** — the *object* measured: the support and
  proportions of a policy's next-action distribution, per decision state (the
  per-state mixture figure).
- **Predictability** — the *metric* (as *detectability* is a metric). The
  ratified one-sentence form: **predictability is the rate at which an attack
  model's next move can be called from its own decision state.**

The metric sits inside the thesis's own premise: MTD rests on denying the
attacker a predictable defence, yet the adversary it is canonically evaluated
against is itself perfectly predictable. Predictability names the property the
movement attacker changes — and only that. **The honesty ceiling travels from
experiment 2 unchanged**
([`experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
§11, 1 600 paired runs): a lower P claims a plural repertoire, **not an
advantage** — what the model gains in breadth of behaviour it has not been
shown to gain in outcome, and no figure or sentence carries the first half
without the second.

## The metric

An attack model fixes a policy π(a | c): a distribution over next actions *a*
conditional on the model's own decision state *c*. Per decision state, the
composition's three numbers are the existing Hill family
(`hill_diversity`, [`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py)
§10): support **N**, effective number **D = 2^H**, evenness **E = D/N**. Two
aggregates over decision states, visitation-weighted:

- **Effective behavioural breadth** — D_policy = 2^{H(A|C)}, the exponentiated
  conditional entropy of the policy (Hill order 1).
- **Predictability** — **P = Σ_c p(c) · max_a π̂(a | c)** (Hill order ∞, as
  1/P per state): how often an observer granted every variable the policy
  itself consults can call the next move.

The pre-registered regime map, which is the whole argument in one table:

| policy | N | D | E | P |
|---|---|---|---|---|
| scripted baseline (FSM) | 1 | **1.00 exactly, by construction** | — | **1.00 exactly** |
| uniform dithering | N | ≈ N | ≈ 1 | 1/N |
| **preferred mixture** (the claim) | N | 1 < D < N | < 1 | between |

Three design facts make this detectability-grade rather than a diversity
import:

1. **The baseline pins the boundary with zero estimation noise.** A
   deterministic policy has zero conditional entropy in any sample of any size,
   so the FSM's P = 1 is a constructed fact, not a measurement. The contrast
   with the movement attacker carries no estimation caveat on the baseline
   side.
2. **The conditioning is maximally charitable to determinism.** Each model is
   conditioned on **its own declared decision state** — the FSM's phase for the
   baseline, the (place, verdict) pair the overlay composition consults for the
   movement attacker. Spread that survives full conditioning cannot be apparent
   variety inherited from unmodelled state; it is plurality in the policy
   itself. The trap this kills: *marginal* (pooled, unconditioned) action
   diversity, on which even the FSM scores above 1 because mixing over
   situations imitates a mixture of choices.
3. **Both estimators err toward the baseline's side.** Plug-in entropy is
   biased low (so D̂ understates plurality) and empirical p̂_max is biased high
   (so P̂ overstates predictability). Undersampling makes the movement attacker
   look *more* FSM-like, so any measured plurality survives the scepticism —
   the inverse of the 10-draw evenness-1.00 failure recorded in
   [`plural_preference.md`](../implementation/pipeline/ogasp/plural_preference.md).

One caveat owed in any prose that uses the metric: the baseline's realised
*traces* still vary run to run. That variation lives in the environment's
transition function (exploit rolls, host draws), not in π — the definition
survives, but the methods text needs the sentence, or an examiner will ask why
a perfectly predictable attacker produces different runs.

## What this supersedes, and what survives

- **[`2026-08-09_axis4_adaptivity_context.md`](2026-08-09_axis4_adaptivity_context.md)**
  (context only). Its bounds were always citations: the verdict-blind negative
  is experiment 2 §11's, the four readers' blind spots are
  [`measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(b)'s, the axis-8 wall is the criterion's. This brief cites those permanent
  records directly; the context file is marked superseded.
- **[`2026-08-09_axis4_plural_recovery_instrumentation.md`](2026-08-09_axis4_plural_recovery_instrumentation.md)**
  (the recovery-repertoire brief). The reframe (Marc, 2026-08-10): the missing
  instrument was never recovery-specific — it is a detectability-grade scalar
  for plurality itself, and the failure-conditioned reading is a
  **decomposition of it** (the per-verdict slice, layer 4 below), not its own
  headline. What survives wholesale: the census gate, the two free nulls, the
  M1/M2 separation, the advantage ceiling, and the conditional-stationary-policy
  boundary. What is dropped: the recovery-first framing and the JSD-as-clincher
  structure (JSD is retained as the per-verdict contrast statistic).

## State of play

**Exists, on `dev`.** The Hill machinery (`HillDiversity`, `hill_diversity`,
`dimension_counts`, `jsd`, `normalise`, `interval_report` —
[`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py));
`uniform_weight_variant`
([`net.py`](../../src/mtdsim/l3_simulation/movement/net.py)); the verdict-blind
arm as a value change (experiment 2 §11); the overlay composition the declared
layer reads (`OutcomeOverlay.compose` in
[`outcome.py`](../../src/mtdsim/l3_simulation/controller/outcome.py)); tracers
for both arms ([`trace_tool.md`](../implementation/trace_tool.md)); the
unconditional plurality study whose numbers overlap the realised layer
([`plural_preference.md`](../implementation/pipeline/ogasp/plural_preference.md)).

**Never measured, anywhere:**

- Any **conditional** (per-decision-state) composition — every shipped
  diversity number is pooled/unconditional.
- Anything at all about the **baseline attacker's policy** at decision level —
  the scripted arm has never been behaviourally instrumented this way.
- The **decision-state visitation census** (including the failure-verdict count
  per cell, inherited from the superseded brief and still ungated).

**The one new reader:** a per-decision-state conditional composition (next
action counts keyed by decision state), plus the order-∞ member (modal
probability) beside `HillDiversity`'s order-1. Small, and it belongs in
`measures.py` beside its family — extend the living instrument, never fork it.

## The two pre-registration decisions that make or break the instrument

Both are fixed and committed **before any trace is read** (P4). They are where
this metric is won or lost; everything else is mechanics.

1. **The action alphabet.** The two models act over different native alphabets
   (FSM phase/verb against place/transition). The headline is **per-model over
   its native alphabet** — legitimate because P = 1 is alphabet-invariant for a
   deterministic policy, so the cross-model contrast compares positions on a
   shared scale, not distributions on a shared support. Target/host selection
   is **excluded from the alphabet on both arms** (it is environment
   granularity, and `MovementRecord` carries no host identity). A shared
   verb-level alphabet is an optional robustness reading, never the headline.
2. **The conditioning variable.** Each model's own declared decision state, as
   above. Too coarse manufactures plurality; too fine makes every cell a
   singleton and both models read deterministic. Any change after the first
   trace read is a new pre-registration, stated as such.

## Recommended approach — five layers, cheapest first

### 0. The census (gates everything)

Decision-state visitation counts per profile × arm × state cell — and per
verdict at verdict-carrying places — from recorded runs. Sparsity ruling per
cell on its numbers; an unestimable cell is reported unestimable, never
massaged. The undersampling lesson travels (`plural_preference.md` prereg).

### 1. Calibration — the scripted baseline as the instrument's self-test

Run the reader over baseline-arm traces
([`attack_operation.py`](../../mtdnetwork/operation/attack_operation.py);
tracer: `python -m mtdnetwork.trace`). It **must read exactly N = 1, D = 1.00,
P = 1.00** at the pre-registered alphabet. A deviation is an **instrument
defect** — the alphabet or conditioning is leaking environment state into the
policy read — and is repaired before any movement-arm number is quoted. This
layer is a self-test, not a finding about the baseline.

### 2. Declared layer — run-free, movement arm only

Per decision state: `hill_diversity` and modal probability of the composed
out-distribution, both overlay columns
(`compose(place, verdict, base_out)`). Declared D > 1 with E < 1 states the
parameterisation *declares* a preferred mixture — read off the model's own
tables. No baseline counterpart exists, which is itself the point; the declared
layer can never carry the cross-model contrast, only the realised layer can.

### 3. Realised layer — the headline, both models

From recorded runs: the conditional composition per decision state; the
aggregates P and D_policy per profile per arm, `interval_report` over per-seed
values. The headline table is the regime map populated: baseline at the
constructed boundary, movement attacker's realised (N, D, E, P) beside its
declared values. Windowed/decision-shaped, never outcome-shaped — the
degenerate region (no attacker completes at 200 s) binds outcome measures, not
these.

### 4. Decompositions and nulls

- **Per-verdict slice** (the superseded brief's intent, subsumed): post-success
  against post-failure compositions within arm, `jsd` between them; the
  **verdict-blind arm** gives the null distribution by construction (its two
  slices are identical). Separation ⇒ the verdict splits the composition —
  reported per profile, whichever way it lands. **M1 (severing interrupt) and
  M2 (failure verdict) stay separate conditioning events, never pooled.**
- **Uniform-weight arm** (`uniform_weight_variant`): same support, preference
  stripped — separates plurality the *weights* prefer from plurality the
  *graph* forces. The shipped arm's E must sit below the uniform arm's for the
  word "preferred" to be used.
- Matched seeds across arms; effort-denominated comparisons; no ordering claim
  without disjoint intervals.

### Alternatives considered, and why this wins

- *Marginal (pooled) action diversity.* The FSM scores above 1 on it; mixing
  over states imitates mixture. It is the import-a-diversity-index version of
  this metric and measures the wrong object. Rejected.
- *Trajectory-level diversity* (`path_entropy`, `distinct_sequences`). High for
  both models under a stochastic environment; a property of walks, not of the
  policy. Rejected as the contrast-carrier; stays as context.
- *Extending `interrupt_action_mix`.* Measures change in mix, not shape of
  mixture; a rigid single-fallback rule also changes the mix. Rejected in the
  superseded brief; still rejected.
- *Recovery-specific headline.* A slice, not the scale — see §What this
  supersedes.

## Validation gate

1. **Pre-registration committed before any trace is read** (P1–P4 below),
   git-history-dated.
2. **The census reported first**, sparsity rulings made on its numbers.
3. **Calibration passes exactly** — baseline N = 1, D = 1.00, P = 1.00 — or the
   instrument is repaired and nothing downstream is quoted.
4. **The headline table**: declared and realised (N, D, E, P) per profile per
   arm with `interval_report` intervals; the regime map populated; realised
   numbers reproduce `plural_preference.md` where the unconditional readings
   overlap.
5. **The decomposition verdicts stated whichever way they land**, per profile:
   verdict-slice JSD against the verdict-blind null, evenness against the
   uniform-weight arm.
6. **Experiment 2's outcome negative quoted next to any positive** — no figure
   or sentence carries plurality without the advantage boundary.
7. **Full `tests/l3_simulation` plus substrate/carve/golden suites pass**;
   readers only — a moved golden means the shipped walk changed and must be
   explained, not accepted.
8. **Record** at
   `docs/implementation/pipeline/ogasp/predictability.md`: census, calibration,
   tables, verdicts, and the ruling on what the thesis may claim. Cross-reference
   [`plural_preference.md`](../implementation/pipeline/ogasp/plural_preference.md)
   (whose "do not let any figure read as axis-4 adaptation" constraint travels)
   and the axis-4 records, so the accounts compose rather than appear to
   contradict.

## Pre-register before running

- **P1 — direction.** Movement arm, majority of estimable profile cells:
  realised 1 < D < N with E < 1 and P < 1; E CI-below the uniform-weight arm's;
  M2 verdict-slice JSD CI-separated from the verdict-blind null.
- **P2 — kill criteria, each a reportable finding, never massaged.**
  (a) Realised D ≈ 1 despite declared mixture ⇒ **declared-not-realised** —
  the walk collapses to one route in practice, reported as exactly that.
  (b) E ≈ 1 with D ≈ N, indistinguishable from the uniform arm ⇒ the plurality
  is **graph-forced**; the weights prefer nothing; "preferred" is not used.
  (c) Verdict slices indistinguishable from the verdict-blind null ⇒ the
  verdict does not split the composition — the axis-4 negative restated
  distributionally, reported as the axis's second measured negative.
- **P3 — seed count** fixed by a convergence check on the conditional
  distributions (post-census, pre-run), shared across arms.
- **P4 — alphabet and conditioning** (§The two decisions) fixed first; any
  later change is a new pre-registration.

## Hard constraints

- **No advantage phrasing, anywhere, ever.** "A plural preferred repertoire" /
  "less predictable" — never "recovers better", "adapts usefully", or any
  outcome-comparative form. The experiment-2 negative travels with every
  figure.
- **Conditional-stationary-policy boundary.** Static declared weight sets; the
  verdict selects between two static mixtures. Not learning (axis 7, ~14 000
  runs, separately closed), not within-run strategy revision.
- **Readers move no badge.** Axis 4 turns on advantage and holds on a control;
  expect DESIGNED to stand. This is thesis-argument evidence — the same
  superset-of-badge move `plural_preference.md` made — characterising the
  attack model against its procedural baseline.
- **Scores move on evidence only** (S6;
  [`guardrails.md`](../workflows/guardrails.md)) — never retune the weight
  tables to lower P or deepen D.
- **The label-drift trap** — recorded runs carry pre-2026-08-06 profile names;
  normalise off the corpus, refuse empty cells (`plurality_reporting.md` §7).
- **The reported-configuration pin** — modulators null is the arm
  ([`model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)).
- Determinism (SIM-05); cross-arm comparisons effort-denominated, never
  time-denominated; Australian English; branch per session; commit locally;
  **never push** without an explicit ask.

## Reading list

- [`plural_preference.md`](../implementation/pipeline/ogasp/plural_preference.md)
  + [`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py) §10 —
  the Hill machinery, the regime table, the prereg pattern, the undersampling
  lesson.
- [`experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  §11 — the verdict-blind arm's construction and the outcome negative,
  verbatim.
- [`outcome.py`](../../src/mtdsim/l3_simulation/controller/outcome.py) +
  [`success_failure_overlay_design.md`](../implementation/pipeline/ogasp/success_failure_overlay_design.md)
  — where the declared layer reads.
- [`attack_operation.py`](../../mtdnetwork/operation/attack_operation.py) +
  [`trace_tool.md`](../implementation/trace_tool.md) — the scripted FSM and the
  tracers for both arms (the calibration layer's ground).
- [`measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(b) — the prior axis-4 readers and the blind spots that travel.

## Out of scope (explicitly)

- **Any new mechanism, modulator, or weight re-declaration** — all arms are
  reads of what exists; the verdict-blind arm is experiment 2's, unchanged.
- **Moving any criterion badge**, or re-scoring any row.
- **Learning / experience-conditioned routing** (axis 7) and
  **defence-conditioned variants** (axis 8, closed on evidence).
- **Re-running experiment 2's progression comparisons** — the outcome negative
  is settled and is quoted, not re-litigated.
- **Dissertation prose and chapter placement** — the record names what may be
  claimed; where it lands is a later pass.
