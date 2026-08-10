---
status: in-progress
created: 2026-08-10
updated: 2026-08-10
topic: "Predictability — one detectability-grade scalar for strategic plurality, applied to both attack models, with the scripted baseline pinned at P=1 by construction; pre-registration (committed before any trace is read) + census + calibration + declared/realised layers + decompositions"
---

# Predictability — the rate at which an attack model's next move can be called from its own decision state

**Status.** The §Pre-registration below (alphabet, conditioning variable, and
predictions P1–P4) is committed **before any trace or run output is read**, so its
git commit predates every results section. Executes the
`2026-08-10_predictability_instrument` handoff. **A reader study over recorded
runs: the arms simulate, but every *measure* is a re-read, and nothing here moves a
badge** — axis 3 is DEMONSTRATED and axis 4 is DESIGNED, and this builds the
thesis-argument evidence their prose leans on (a superset of the badge), exactly as
[`plural_preference.md`](plural_preference.md) did.

## The vocabulary, fixed once (downstream prose inherits these terms)

- **Strategic plurality** — the *property* claimed (as *stealth* is a property).
- **Behaviour composition** — the *object* measured: the support and proportions
  of a policy's next-action distribution, per decision state.
- **Predictability** — the *metric* (as *detectability* is a metric). The ratified
  one-sentence form: **predictability is the rate at which an attack model's next
  move can be called from its own decision state.**

The metric sits inside the thesis's own premise: MTD rests on denying the attacker
a predictable defence, yet the adversary it is canonically evaluated against — the
inherited six-phase scripted attacker — is itself perfectly predictable.
Predictability names the property the movement attacker changes, and only that.

## The honesty ceiling (fixed before any number exists, unmovable by any result)

**The experiment-2 outcome negative travels with every figure**
([`experiment_02_findings.md`](experiment_02_findings.md) §11, 1 600 paired runs):
a lower P claims a plural repertoire, **not an advantage**. What the model gains in
breadth of behaviour it has not been shown to gain in outcome, and no figure or
sentence in this record carries the first half without the second. This is a
statement about the model's **stationary policy** — a plural mixture, categorically
unlike one deterministic rule — **never** within-run adaptive selection (axis 4 is
DESIGNED; the verdict-blind ablation measured routing approximately free). Every
caption carries that boundary.

## The metric

An attack model fixes a policy π(a | c): a distribution over next actions *a*
conditional on the model's own decision state *c*. Per decision state, the
composition's three numbers are the existing Hill family (`hill_diversity`,
[`measures.py`](../../../../src/mtdsim/l3_simulation/movement/measures.py) §10):
support **N**, effective number **D = 2^H**, evenness **E = D/N**. Two aggregates
over decision states, visitation-weighted p(c):

- **Effective behavioural breadth** — D_policy = 2^{H(A|C)}, the exponentiated
  conditional entropy of the policy (Hill order 1), where
  H(A|C) = Σ_c p(c)·H(a|c).
- **Predictability** — **P = Σ_c p(c)·max_a π̂(a | c)** (Hill order ∞, as 1/P per
  state): how often an observer granted every variable the policy itself consults
  can call the next move.

The pre-registered regime map, which is the whole argument in one table:

| policy | N | D | E | P |
|---|---|---|---|---|
| scripted baseline (FSM) | 1 | **1.00 exactly, by construction** | — | **1.00 exactly** |
| uniform dithering | N | ≈ N | ≈ 1 | 1/N |
| **preferred mixture** (the claim) | N | 1 < D < N | < 1 | between |

Three design facts make this detectability-grade rather than a diversity import,
carried verbatim from the handoff:

1. **The baseline pins the boundary with zero estimation noise.** A deterministic
   policy has zero conditional entropy in any sample of any size, so the FSM's
   P = 1 is a constructed fact, not a measurement (§Calibration establishes it from
   the *code*, and the reader self-test confirms it over traces). The contrast with
   the movement attacker carries no estimation caveat on the baseline side.
2. **The conditioning is maximally charitable to determinism.** Each model is
   conditioned on **every variable its own policy consults** (§The two decisions).
   Spread that survives full conditioning cannot be apparent variety inherited from
   unmodelled state; it is plurality in the policy itself. The trap this kills:
   *marginal* (pooled, unconditioned) action diversity, on which even the FSM
   scores above 1 because mixing over situations imitates a mixture of choices.
3. **Both estimators err toward the baseline's side.** Plug-in entropy is biased
   low (so D̂ understates plurality) and empirical p̂_max is biased high (so P̂
   overstates predictability). Undersampling makes the movement attacker look
   *more* FSM-like, so any measured plurality survives the scepticism — the inverse
   of the 10-draw evenness-1.00 failure recorded in
   [`plural_preference.md`](plural_preference.md).

**The caveat the methods text owes.** The baseline's realised *traces* still vary
run to run. That variation lives in the environment's transition function (exploit
rolls, host draws), not in π — the definition survives, but an examiner will ask
why a perfectly predictable attacker produces different runs, and the answer is
that the branch outcome the FSM conditions on is drawn by the environment, not
chosen by the policy.

## The two pre-registration decisions that make or break the instrument (P4)

Both fixed and committed **before any trace is read**. They are where the metric is
won or lost; everything else is mechanics.

### 1. The action alphabet

**Per-model over its native alphabet.** The movement action is the **next place**
(the transition destination the policy samples); the FSM action is the **next
phase/verb** (the successor its succession dispatches). This is legitimate because
P = 1 is alphabet-invariant for a deterministic policy, so the cross-model contrast
compares *positions on a shared scale* (predictability ∈ [1/N_max, 1]), not
distributions on a shared support.

**Target/host selection is excluded from the alphabet on both arms.** It is
environment granularity, and `MovementRecord` carries no host identity (the
movement record's own documented blind spot). A shared verb-level alphabet is an
optional robustness reading (both arms dispatch the same six verbs), never the
headline.

### 2. The conditioning variable — each model's own consulted variables

The operative principle is the metric's own words: *every variable the policy
itself consults.* This resolves the handoff's shorthand ("the FSM's phase") to the
literal set of variables each succession rule reads, which is what makes the
P = 1-by-construction claim true rather than approximate.

- **Movement arm — c = (place, verdict).** The driver routes through
  `overlay.compose(place, verdict, base_out)` then samples
  ([`attacker.py`](../../../../src/mtdsim/l3_simulation/movement/attacker.py)
  `_route`); the base out-weights are a function of `place`, and `verdict` ∈
  {`success`, `failure`, `""`} (the last being the distinguished `VERDICT_NONE` a
  dwell-only place routes under). No other variable enters the composition under
  the pinned modulators-null configuration. Given c, the next place is **sampled** —
  the successor is stochastic.
- **Baseline FSM — c = (phase, branch-outcome).** The `_execute_*` succession
  consults the `_do_*` return value — the full branch (`EXPLOIT_COMPROMISED` vs
  `EXPLOIT_UNCOMPROMISED`; credential reuse vs not; host already-held vs fresh; hosts
  found vs none) — which is *finer* than the binary verdict the movement overlay
  keys on ([`verdict.py`](../../../../src/mtdsim/l3_simulation/controller/verdict.py)
  collapses several of these to `success`). Given c, the successor is a
  **deterministic function** (the transition table below), so the FSM's per-state
  next-action distribution is a point mass: **N = 1, D = 1, P = 1 exactly, by
  construction.**

The asymmetry in *outcome granularity* is the point, and it is the charitable
choice, not a thumb on the scale: each model is granted exactly the variables its
own policy reads, so any residual plurality is the policy's, not the observer's
ignorance. Conditioning both arms on the *same coarse* (place, verdict) would make
the FSM read plural at `ENUM_HOST` and `SCAN_PORT` — not because it is strategically
plural but because the binary verdict hides its deterministic branch — which is
design fact 2's trap biting the wrong arm. **Too coarse manufactures plurality; too
fine makes every cell a singleton.** Any change after the first trace read is a new
pre-registration, stated as such.

**The FSM transition table (from the code, no trace needed) — the constructed
P = 1.** Under the pinned no-MTD configuration the successor is a deterministic
function of (phase, branch):

| phase | branch (the `_do_*` outcome the succession reads) | successor |
|---|---|---|
| `SCAN_HOST` | hosts found / none | `ENUM_HOST` / terminate |
| `ENUM_HOST` | popped host already-compromised / fresh | `ENUM_HOST` / `SCAN_PORT` |
| `SCAN_PORT` | credential reuse compromise / not | `SCAN_NEIGHBOR` / `EXPLOIT_VULN` |
| `EXPLOIT_VULN` | `EXPLOIT_COMPROMISED` / `EXPLOIT_UNCOMPROMISED` | `SCAN_NEIGHBOR` / `BRUTE_FORCE` |
| `BRUTE_FORCE` | compromise / not | `SCAN_NEIGHBOR` / `ENUM_HOST` |
| `SCAN_NEIGHBOR` | (unconditional) | `ENUM_HOST` |

Every (phase, branch) cell carries exactly one successor. The calibration layer
recovers the branch from substrate observables — never from the successor, which
would be circular — and confirms the reader reads exactly 1.

## The five layers (cheapest first) — plan committed before running

### 0. The census (gates everything)

Decision-state visitation counts per profile × arm × state cell, and per verdict at
verdict-carrying places, from recorded runs. A cell whose count cannot support an
estimate is reported **unestimable**, never massaged. The undersampling lesson from
[`plural_preference.md`](plural_preference.md)'s P3 travels: a per-run-sparse cell
is withheld, not rounded up.

### 1. Calibration — the scripted baseline as the instrument's self-test

The reader is run over baseline-arm traces at **two** granularities. At (phase,
branch) it **must read exactly N = 1, D = 1.00, P = 1.00** — a deviation is an
**instrument defect** (the branch reconstruction is missing a variable the FSM
consults) and is repaired before any movement number is quoted. At (phase) alone it
is *expected* to read plural for the branching phases — this proves the reader is
not rigged to return 1, and it makes design fact 2's marginal trap concrete: the
phase-level plurality is *entirely* accounted for by the branch the FSM's own
policy reads. This layer is a self-test, not a finding about the baseline.

### 2. Declared layer — run-free, movement arm only

Per decision state (place, verdict): `hill_diversity` and modal probability of the
**composed** out-distribution `compose(place, verdict, base_out)`, read directly off
the model's own tables (no simulation). Declared D > 1 with E < 1 states the
parameterisation *declares* a preferred mixture. No baseline counterpart exists,
which is the point; the declared layer can never carry the cross-model contrast,
only the realised layer can.

### 3. Realised layer — the headline, both models

From recorded runs: the conditional composition per decision state; the aggregates
P and D_policy per profile per arm; `interval_report` over per-seed values. The
headline table is the regime map populated — baseline at the constructed boundary,
the movement attacker's realised (N, D, E, P) beside its declared values.
Windowed/decision-shaped, never outcome-shaped (the degenerate region binds outcome
measures, not these). Realised numbers must reproduce
[`plural_preference.md`](plural_preference.md) where the unconditional readings
overlap.

### 4. Decompositions and nulls

- **Per-verdict slice** — post-success against post-failure compositions within
  arm, `jsd` between them; the **verdict-blind arm**
  ([`outcome.py`](../../../../src/mtdsim/l3_simulation/controller/outcome.py)
  `verdict_blind_overlay`) gives the null distribution by construction (its two
  slices are identical). Separation ⇒ the verdict splits the composition. **M1
  (severing interrupt) and M2 (failure verdict) stay separate conditioning events,
  never pooled.**
- **Uniform-weight arm** (`uniform_weight_variant`) — same support, preference
  stripped: separates plurality the *weights* prefer from plurality the *graph*
  forces. The shipped arm's E must sit below the uniform arm's for the word
  "preferred" to be used.
- Matched seeds across arms; effort-denominated comparisons; no ordering claim
  without disjoint intervals.

## Pre-register the predictions (P1–P4, committed before running)

- **P1 — direction.** Movement arm, majority of estimable profile cells: realised
  1 < D < N with E < 1 and **P < 1**; the aggregate P CI-separated **below** the
  FSM's constructed 1.00; E CI-below the uniform-weight arm's on ≥ 3 of the
  shape-certified dimensions of state; M2 verdict-slice JSD CI-separated from the
  verdict-blind null.
- **P2 — kill criteria, each a reportable finding, never massaged.**
  (a) Realised D ≈ 1 despite a declared mixture ⇒ **declared-not-realised** — the
  walk collapses to one route in practice, reported as exactly that.
  (b) E ≈ 1 with D ≈ N, indistinguishable from the uniform arm ⇒ the plurality is
  **graph-forced**; the weights prefer nothing; "preferred" is not used.
  (c) Verdict slices indistinguishable from the verdict-blind null ⇒ the verdict
  does not split the composition — the axis-4 negative restated distributionally,
  reported as the axis's second measured negative.
- **P3 — seed count** fixed by a convergence check on the conditional distributions
  (post-census, pre-full-run), shared across arms. A decision cell that does not
  converge inside the budget has its shape verdict withheld (its census count still
  stands).
- **P4 — alphabet and conditioning** (§The two decisions) fixed first; any later
  change is a new pre-registration.

## Hard constraints (carried from the handoff)

- **No advantage phrasing, anywhere, ever.** "A plural preferred repertoire" /
  "less predictable" — never "recovers better", "adapts usefully", or any
  outcome-comparative form. The experiment-2 negative travels with every figure.
- **Conditional-stationary-policy boundary.** Static declared weight sets; the
  verdict selects between two static mixtures. Not learning (axis 7), not within-run
  strategy revision.
- **Readers move no badge.** This is thesis-argument evidence characterising the
  attack model against its procedural baseline — the same superset-of-badge move
  [`plural_preference.md`](plural_preference.md) made.
- **Scores move on evidence only** (S6) — never retune the weight tables to lower P
  or deepen D.
- **The label-drift trap** — recorded runs carry pre-2026-08-06 profile names;
  normalise off the corpus, refuse empty cells (`plurality_reporting.md` §7).
- **The reported-configuration pin** — modulators null is the arm
  ([`model_scope_freeze.md`](model_scope_freeze.md)); no MTD, v2_partial, retrace,
  the plural-preference configuration.
- Determinism (SIM-05); cross-arm comparisons effort-denominated; Australian
  English.

---

## Census

_Pending the run (§0). Committed empty above this line._

## Calibration

_Pending the run (§1)._

## Declared layer

_Pending the run (§2)._

## Realised layer — the headline

_Pending the run (§3)._

## Decompositions and nulls

_Pending the run (§4)._

## Verdicts

_Pending the run._

## Reproduction

_Pending the run._
