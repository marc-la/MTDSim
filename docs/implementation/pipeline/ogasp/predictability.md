---
status: durable
created: 2026-08-10
updated: 2026-08-13
topic: "Strategic plurality measured as effective behavioural breadth — a deterministic-vs-stochastic-policy contrast over both attack models; pre-registration (committed before any trace is read) + census + calibration + declared/realised layers + decompositions. V2 rework 2026-08-13: the 'predictability' name and its [0,1] scalar are RETIRED for MTD-venue accuracy (Ghosh/Jalowski own the term for defender foreseeability); the argument leads with effective behavioural breadth (exp conditional entropy), the baseline established against the code as a deterministic policy = 1 effective behaviour."
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

> **Challenged at the 2026-08-11 supervisor meeting — resolved 2026-08-13
> (§Resolution below), no figure retracted**
> ([`supervisor_decision_register.md`](supervisor_decision_register.md) §V2).
> The meeting challenged the baseline P = 1 pin (the scripted attacker branches
> on the exploit verdict) and asked that the name *predictability* be checked
> against established usage. Both are discharged in §Resolution. **Verdict, up
> front — the maths stands, the framing is corrected, and the name is retired.**
> Formalising the FSM against the code (not the meeting summary) shows the
> scripted attacker is a **deterministic policy**: given its decision state its
> next verb is forced, so it exercises no behavioural choice of its own (R1–R5).
> The challenged phrasing ("the next state can be called from the given state")
> was loose — an exploit outcome is not knowable before acting, on either arm —
> and is dropped. Because *predictability* carries a specific **defender-terrain
> foreseeability** meaning in the MTD literature (which the FSM's outcome-driven
> branching does not satisfy, and which is what the meeting caught), the name is
> **retired in this venue** (R6–R7): the argument leads instead with **effective
> behavioural breadth** — the effective number of next-moves per decision (the
> exponential of the policy's conditional entropy, Hill order 1), on which the
> baseline is a **deterministic policy with one effective behaviour** and the
> movement attacker a **stochastic policy with 2.7–5.9**. The `[0,1]` scalar and
> its inversion are dropped as surplus. **No figure changes**; the
> pre-registration and results sections below are unaltered and §Resolution
> annotates them. (The pre-registered body still says "predictability / P"
> throughout — that is committed-before-results history and stays legible as
> such; §Resolution R7 is the operative naming.)

## Resolution — V2 rework (2026-08-13)

Discharges [`supervisor_decision_register.md`](supervisor_decision_register.md)
§V2 and the `2026-08-11_predictability_rework` handoff. Formalised against
`mtdnetwork/operation/attack_operation.py` zero-trust (not against the challenge
summary), hand-validated under V1's protocol, name checked against the
literature. Nothing here rewrites the pre-registration; the branch conditioning
it defends was fixed at §The two decisions, committed before any trace was read.

### R1. The baseline FSM's decision process, from the code

The inherited attacker is a self-driving deterministic program
(`AttackOperation`). There is no separate *decide* step: each verb's core
`_do_*` performs the action and **returns its branch outcome**, and the matching
`_execute_*` wrapper reads that return value and dispatches to a hard-coded
successor. The policy is therefore exactly the six `_execute_*` dispatch rules,
each a **total function from (its own `_do_*` outcome) to one successor verb**.
Re-derived from the wrappers directly (`_execute_scan_host` …
`_execute_scan_neighbors`), the transition table is identical to §The two
decisions':

| phase | branch (the `_do_*` outcome the succession reads) | successor |
|---|---|---|
| `SCAN_HOST` | hosts found / none | `ENUM_HOST` / terminate |
| `ENUM_HOST` | popped host already-compromised / fresh | `ENUM_HOST` / `SCAN_PORT` |
| `SCAN_PORT` | credential reuse compromise / not | `SCAN_NEIGHBOR` / `EXPLOIT_VULN` |
| `EXPLOIT_VULN` | `EXPLOIT_COMPROMISED` / `EXPLOIT_UNCOMPROMISED` | `SCAN_NEIGHBOR` / `BRUTE_FORCE` |
| `BRUTE_FORCE` | compromise / not | `SCAN_NEIGHBOR` / `ENUM_HOST` |
| `SCAN_NEIGHBOR` | (unconditional) | `ENUM_HOST` |

Every (phase, branch) cell carries exactly one successor.

### R2. Where the exploit verdict sits — the crux, and why it is *both* things

The meeting's objection targets `EXPLOIT_VULN`: `EXPLOIT_COMPROMISED` routes to
`SCAN_NEIGHBOR`, `EXPLOIT_UNCOMPROMISED` routes to `BRUTE_FORCE`
(`_execute_exploit_vuln`). The handoff's step 1 asked which of two things the
verdict is; the code answer is that it is **both**, and being both is not a
contradiction:

- It is **an outcome revealed only after the move is committed.**
  `_do_exploit_vuln` spends the action's time and rolls the exploit
  (`vuln.network(...)`) *inside* the verb; the compromise verdict is a stochastic
  environment output, not knowable before the verb runs. So the supervisor is
  right that the *next state* cannot be called from the *phase before acting* —
  and no attack model can, the movement attacker included.
- It is **a variable the succession rule consults.** The `_execute_*` dispatch
  is literally a branch on that return value. Given the verdict, the successor is
  a deterministic function.

Predictability (§The metric) is defined over the **decision state** *c*, which
by construction is *every variable the policy consults* — for the FSM,
c = (phase, branch), the branch including the verdict. Given *c*, the FSM's next
verb is a point mass: N = 1, D = 1, max_a π(a | c) = 1. Hence **P = 1 exactly,
by construction** — a theorem about a deterministic program, confirmed
operationally by the calibration reader returning P = 1.000 on the transition
table (§Calibration).

### R3. Why conditioning on the verdict is the fair construction, not a thumb on the scale

The move that answers the objection is **symmetric**, and that is what makes it
legitimate rather than a dodge. The movement attacker's policy *also* consults a
verdict drawn by the same environment: its overlay composes on (place, verdict)
and *then samples* the successor (`movement/attacker.py`, `overlay.compose`
followed by the sampled transition). Each arm is granted exactly the variables
its own policy reads, so the distinction the metric isolates is the real one:

- **FSM** — given its decision state, the successor is *computed* (deterministic
  dispatch): zero policy choice, **P = 1**.
- **Movement** — given its decision state, the successor is *sampled* from a
  declared mixture: genuine policy plurality, **P = 0.33–0.57**.

Both arms are subject to *identical* environmental stochasticity — the verdict is
drawn, not chosen, on both. Conditioning on the decision state factors that
shared stochasticity out, leaving only what each *policy* contributes. Refusing
to condition on the verdict would not make the comparison fairer: it would
inflate the FSM's apparent plurality with the hidden verdict (the marginal trap,
design fact 2) *and* understate the movement attacker's, measuring neither
policy. The construction is coherent only at decision-state granularity, and
there the FSM is P = 1.

### R4. What was actually wrong, and the corrected claim

The sentence challenged in the meeting — "the next state can be called from the
given state" — was loose, and the concession stands: read as *call the next
state from the phase, before acting*, it is false, because the verdict has not
been drawn yet. The claim the record makes and defends is the different, correct
one:

> **The scripted attacker's policy is a deterministic function of its decision
> state — it exercises no choice; given the decision state, its next verb is
> forced. Its run-to-run trace variation is entirely environmental (exploit
> rolls, host draws), shared with the movement attacker, and is not policy
> plurality.**

So the meeting outcome is a **presentation fix that states the conditioning
explicitly**, not a retraction of "by construction". The P = 1 pin is retained;
every downstream figure (movement P = 0.33–0.57, CI-separated below 1.00) stands
unchanged. This is the first of the two branches the pre-registration banner
left open — *the verdict as a conditioning variable answers the challenge* — now
closed on the code.

The one honest residual, already recorded at §Calibration and unchanged: the
reader reads P = 0.868 at (phase, branch) *from traces*, not 1.000, because three
cells (`ENUM_HOST|fresh`, `ENUM_HOST|already_compromised`, `BRUTE_FORCE|not`)
carry unmodelled enumeration/environment state the attack record under-exposes —
not policy plurality. The 1.000 is the theorem over the policy's transition
table; the trace residual is a limit of trace reconstruction, and it lies on the
*predictable* side (residual P > constructed-marginal P), so it cannot
manufacture spurious plurality against the movement arm.

### R5. Hand-validation (V1 protocol) — P by hand agrees with the reader

A worked trace on a four-host line network (exposed endpoint + h1, h2, h3),
following one FSM trajectory and tallying the decision states c = (phase, branch)
it visits with their forced successors:

| decision state c = (phase, branch) | successor | visits | max_a π(a\|c) |
|---|---|--:|--:|
| `SCAN_HOST`, found | `ENUM_HOST` | 1 | 1 |
| `ENUM_HOST`, fresh | `SCAN_PORT` | 3 | 1 |
| `ENUM_HOST`, already | `ENUM_HOST` | 1 | 1 |
| `SCAN_PORT`, no-reuse | `EXPLOIT_VULN` | 3 | 1 |
| `EXPLOIT_VULN`, compromised | `SCAN_NEIGHBOR` | 2 | 1 |
| `EXPLOIT_VULN`, uncompromised | `BRUTE_FORCE` | 1 | 1 |
| `SCAN_NEIGHBOR`, — | `ENUM_HOST` | 2 | 1 |
| `BRUTE_FORCE`, not | `ENUM_HOST` | 1 | 1 |

Fourteen decisions; every cell is a point mass, so by hand
**P = Σ_c p(c)·max_a π(a | c) = 1.000** and **D_policy = 2^{H(A|C)} = 2^0 = 1.00**
— independent of the visitation distribution. Collapsing to phase-only
conditioning reproduces the marginal trap by hand: at `EXPLOIT_VULN` the observed
successors are {`SCAN_NEIGHBOR` ×2, `BRUTE_FORCE` ×1} ⇒ max = 2/3, and at
`ENUM_HOST` {`SCAN_PORT` ×3, `ENUM_HOST` ×1} ⇒ max = 3/4, giving marginal
P = 12/14 = **0.857 < 1**. The by-hand numbers match the calibration reader's
recorded regime exactly in structure and ordering (decision-state 1.000;
marginal < 1 — the reader recorded 1.000 and 0.766 on its own trace); the
absolute marginal differs only because it is an illustrative trajectory, not the
100-seed trace. The invariant — decision-state P = 1.000 — is exact and matches.
This clears the pin for the V1 instrument-validation pass.

### R6. The name check — the collision that retires the term

"Predictability" is an established term in two neighbouring literatures, and the
two pull opposite ways:

- **RL / control — established with essentially this meaning.** Policy entropy
  *is* the standard measure of an agent's action predictability (low entropy ⇒
  predictable), and the word is used directly (*Predictability-Aware RL* via the
  trajectory entropy rate; Trajectory-Entropy RL for "predictable" control). So
  in that lineage the metric is a real object, not a coined score.
- **MTD — established, but with the *defender* as subject; a genuine collision.**
  In the MTD literature "predictability" is a property of the *defender's cyber
  terrain*: MTD wins by *decreasing the predictability of our systems* (Ghosh
  2009), and low-entropy MTD "rotates within a predictable set of vulnerabilities"
  (Jalowski 2026, on record in the extractions). It is a *foreseeability* notion
  about the defender, not a concentration property of the attacker's policy.

**Verdict (settled 2026-08-13 with Marc): retire the term in this venue.**
Qualifying it (*behavioural / policy predictability*) was considered and
rejected. Two reasons. First, *guessable* and *predictable* are synonyms, so no
qualifier escapes the foreseeability reading — and that reading is exactly the
one the `EXPLOIT_VULN` branch falsifies (you cannot foresee the FSM's next move,
because the exploit outcome is not yet drawn). Second, this dissertation sits
*inside* the MTD literature, which already owns the word for defender
foreseeability; quietly repurposing it for a property of the attacker's policy
reads as an error to a reader in the field, which is precisely what the meeting
caught. The name is dropped; R7 is the reframing.

### R7. The reframing — effective behavioural breadth (deterministic vs stochastic policy)

The argument leads with the quantity the maths already computes on the
uncontested side, under the standard names the two source fields give it:

- **The measure is effective behavioural breadth** — the exponential of the
  policy's conditional Shannon entropy, `2^{H(A|C)}` (the record's `D_policy`).
  This is the Hill number of order 1 / Jost's "effective number of types" in
  ecology, and the identical "effective number of actions, `e^{H}`" used for
  exploration in reinforcement learning. Higher means a broader repertoire; it
  needs no inversion and carries no loaded term.
- **The contrast is the textbook RL distinction** between a **deterministic
  policy** (one action per state) and a **stochastic policy** (a distribution
  over actions per state). R1–R5 establish, against the code, that the scripted
  baseline is a deterministic policy and the movement attacker a stochastic one.

So the honest, venue-safe statement is: **the scripted baseline is a
deterministic policy — one effective behaviour per decision, which is a
definitional fact about a deterministic controller, not a claim that its runs are
foreseeable; the movement attacker is a stochastic policy carrying 2.7–5.9
effective behaviours per decision.** The property this evidences is unchanged —
**strategic plurality** — and so is the honesty ceiling: a broader repertoire is
not an advantage ([`experiment_02_findings.md`](experiment_02_findings.md) §11).

**What is dropped, and what is kept.** The `[0,1]` scalar `P` (the order-∞ /
guessing-probability member) and its "predictability" branding leave the
argument. `P` stays in the tables below only as an already-computed companion
statistic; it is no longer the headline, and the word does not travel with it.
The baseline's role becomes the clean one it should always have been — *a
deterministic policy has one effective behaviour* — with no "perfectly
predictable / call its next move" phrasing anywhere, since that is the reading
the `EXPLOIT_VULN` branch correctly falsifies. Nothing numerical changes: the
effective breadths (baseline 1; movement 2.7–5.9) are the same figures the
results section already carries, relabelled and led with rather than inverted.

## The vocabulary, fixed once (downstream prose inherits these terms)

> **▸ Superseded by §Resolution R6–R7 (2026-08-13).** Everything from here down is
> the pre-registration, committed before any trace was read, and is kept verbatim
> as history. Its metric name — *predictability*, and the scalar *P* — is
> **retired**: the operative term is **effective behavioural breadth** (the
> `D_policy` below), and the baseline is described as a *deterministic policy with
> one effective behaviour*, never as "perfectly predictable". Read the body for
> the construction; read R7 for what the metric is now called and claimed.

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

**The statistic is a standard object, three times over — the framing is this
project's, the maths is not.** P is not a bespoke score; it is a well-established
quantity wearing three names in three fields, which is stronger provenance for the
methods text than "we defined a predictability score":

- **Per decision state**, `max_a π(a|c)` is the **Berger–Parker dominance index**
  from ecology (the proportional share of the most-used next move), and its
  reciprocal is the **Hill number of order ∞** — the q → ∞ member of the same Hill
  family §10 already uses for N and D.
- **The aggregate** `Σ_c p(c)·max_a π(a|c)` is exactly the **average guessing
  probability** of information-theoretic security — the chance an optimal adversary
  calls A in one try given side-information C — which equals `2^{−H_∞(A|C)}`, the
  **conditional min-entropy** (Arimoto/Rényi order ∞). It is identically **1 minus
  the Bayes error**: the accuracy of the best possible predictor of the next action
  from the decision state.

So D_policy (order 1, exponentiated Shannon conditional entropy) and P (order ∞,
guessing probability) are the two ends of one Rényi/Hill ladder over the same
conditional distribution. What the project supplies is the *framing* — naming it
predictability, pinning the FSM at 1.00 by construction, and the pre-registered
decision-state conditioning — never the estimator.

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

**Status: complete 2026-08-10.** Everything above this line is the pre-registration
(committed at git `9475ec8`, before any trace or run output was read). Everything
below is the run that followed: 100 matched seeds × four arms × five profiles
(1 600 runs, 0 errors), plus a 600-run convergence check. Seed count fixed at 100 by
the convergence check (§Census). Configuration exactly the plural-preference arm:
v2_partial, overlay `v3_persistent_backward`, no MTD, modulators null, sink policy
retrace, horizon 15 000 s.

**The result, up front.** The movement attacker's realised predictability is
**P = 0.33 to 0.57** across the five profiles, every value CI-separated far below the
scripted baseline's **constructed P = 1.00** — its next move cannot be called from
its own decision state at anything approaching the rate the FSM's can, and it carries
**D_policy = 2.7 to 5.9 effective next-moves per state against the FSM's one**. The
verdict genuinely splits the composition (M2 produces two distinct static mixtures)
in **four of five** profiles, CI-separated from the verdict-blind null — yet this is
a property of the **stationary policy**, and the experiment-2 outcome negative
travels with it unchanged: two distinct mixtures, no shown advantage.

## Census (§0) — every headline cell is estimable

Decision-state visitation, corpus arm, pooled over 100 seeds:

| profile | states | decisions | verdict-carrying places | min cell | median cell | unestimable |
|---|--:|--:|--:|--:|--:|--:|
| `objective_exfiltration` | 21 | 51 294 | 8 | 35 | 1 095 | 0 |
| `objective_impact` | 21 | 47 247 | 8 | 24 | 1 540 | 0 |
| `objective_exfiltration_impact` | 20 | 47 013 | 8 | 4 | 1 635 | 0 |
| `objective_none_c2` | 20 | 66 179 | 8 | 6 | 2 690 | 0 |
| `aggregate` | 22 | 51 493 | 8 | 5 | 1 719 | 1 |

The per-event conditional composition is richly sampled — median cell above a
thousand decisions — so unlike the per-run opening dimension of
[`plural_preference.md`](plural_preference.md), no shape verdict is withheld for
undersampling. The convergence check confirmed it: all five profiles' aggregate P and
D_policy stabilise on the pooled growth ladder well inside 120 seeds
(last-rung |ΔP| ≤ 0.003, |ΔD_policy| ≤ 0.01). Two cells fall below the census floor of
8 visits and are **named, not dropped** — `aggregate`'s `resource-development|`
(a dwell-only `VERDICT_NONE` state) and the verdict-blind arm's
`objective_impact` `credential-access|success` — their visitation still counts toward
p(c); only their per-cell shape is not asserted.

## Calibration (§1) — the reader passes its self-test, and reads the FSM's marginal trap

**The reader returns exactly P = 1.000, D = 1.000 on the deterministic FSM transition
table** (§The two decisions), which is what "P = 1 by construction" means
operationally: the reader is not rigged, and it agrees with the code fact.

Over the baseline traces the reader reads the FSM's plurality at the wrong
granularity and collapses it toward 1 as conditioning deepens — the marginal trap of
design fact 2, made concrete:

| conditioning | P | D_policy |
|---|--:|--:|
| marginal `(phase)` | 0.766 | 1.618 |
| `(phase, branch)` | 0.868 | 1.304 |
| constructed transition table | **1.000** | **1.000** |

At the phase level the reader reads four plural cells (`ENUM_HOST`, `SCAN_PORT`,
`EXPLOIT_VULN`, `BRUTE_FORCE` each show two–three successors) — proof it is *not*
rigged to return 1. Conditioning on the branch resolves `SCAN_PORT` and
`EXPLOIT_VULN` to exact point masses; the **three residual plural cells are exactly
the FSM-internal state the attack record under-exposes** — `ENUM_HOST|fresh` and
`ENUM_HOST|already_compromised` (the popped host's prior-compromise status is set
*during* the core, after the row is appended) and `BRUTE_FORCE|not` (whose successor
routes through `_enum_host`, which itself branches to `SCAN_HOST` on an empty visible
host-stack). These are unmodelled *environment/enumeration* state, not policy
plurality: the FSM is a deterministic program, its P = 1 is a theorem, and the reader
recovers it exactly from the policy and asymptotically from the traces. The residual
is a limit of trace reconstruction, recorded honestly rather than reconstructed
circularly from the observed successor.

## Declared layer (§2) — the model declares a preferred mixture

Run-free, off each profile's net and the `v3_persistent_backward` overlay,
`compose(place, verdict, base_out)` per decision state:

| profile | states | plural states (N > 1) | median E of plural states |
|---|--:|--:|--:|
| `objective_exfiltration` | 28 | 24 | — |
| `objective_impact` | 28 | 24 | — |
| `objective_exfiltration_impact` | 26 | 20 | — |
| `objective_none_c2` | 24 | 14 | — |
| `aggregate` | 30 | **30** | 0.762 (range 0.358–0.917) |

Every declared plural state carries D > 1 with E < 1 — the model's own tables
*declare* a preferred mixture (mass on a subset, not a flat spread), at almost every
decision state. There is no baseline counterpart, which is the point: the declared
layer cannot carry the cross-model contrast; only the realised layer can.

## Realised layer — the headline (§3)

Per-seed aggregate P and D_policy, mean over 100 seeds with the 95 % bootstrap
interval (the seed is the resampling unit); the scripted baseline is the constructed
boundary, not a measurement:

| profile | arm | P | D_policy |
|---|---|--:|--:|
| `objective_exfiltration` | **corpus** | **0.419 [0.415, 0.423]** | **4.19** |
| | scripted baseline | **1.000 (constructed)** | **1.00** |
| `objective_impact` | corpus | 0.404 [0.401, 0.408] | 3.80 |
| `objective_exfiltration_impact` | corpus | 0.414 [0.410, 0.418] | 3.74 |
| `objective_none_c2` | corpus | 0.570 [0.562, 0.577] | 2.73 |
| `aggregate` | corpus | 0.327 [0.324, 0.330] | 5.85 |

**The regime map is populated, and the movement attacker sits between the two
degenerate poles in every profile.** Its predictability is CI-separated below the
scripted baseline's 1.00 by a wide margin — the next move can be called at best 57 %
of the time (`objective_none_c2`) and at worst 33 % (`aggregate`) from the full set of
variables the policy consults, against 100 % for the FSM. Equivalently the policy is
worth 2.7 to 5.9 effective next-moves per decision state where the FSM is worth one.
This is P1's core prediction met on **five of five** profiles: realised 1 < D < N,
P < 1, CI-separated below the constructed boundary. (The pooled-decision aggregate,
which weights by decisions rather than by seed, runs 0.30–0.56 — the same regime; the
per-seed mean is reported as the headline because it carries the inferential unit.)

## Decompositions and nulls (§4)

### Corpus against the uniform-weight null — the direction is profile-dependent

Predictability P, corpus arm against the topology-only null (same reachable graph,
corpus preference stripped):

| profile | corpus P | uniform-null P | CI-separated | what the weights do |
|---|--:|--:|:-:|---|
| `objective_exfiltration` | 0.419 | 0.341 | **yes** | concentrate (more predictable) |
| `objective_impact` | 0.404 | 0.385 | **yes** | concentrate |
| `objective_exfiltration_impact` | 0.414 | 0.432 | **yes** | broaden (less predictable) |
| `objective_none_c2` | 0.570 | **0.779** | **yes** | broaden strongly |
| `aggregate` | 0.327 | 0.328 | no | prefer nothing (at the P scale) |

The corpus weighting is CI-separated from what topology forces in **four of five**
profiles, and — exactly as [`plural_preference.md`](plural_preference.md) found on
evenness — the *direction* is not universal. For two profiles the weights concentrate
the policy (raise P); for two they broaden it. `objective_none_c2` is the same
broadening case that record reports: under uniform weights the walk collapses into a
shallow reconnaissance↔initial-access funnel (P = 0.779, D_policy = 1.69), and the
corpus weighting pulls it back out (P = 0.570, D_policy = 2.73). Both directions are
purposeful departures from what topology forces, which is why the load-bearing
statement is the CI-separation, not its sign. **`aggregate` is a reported negative at
the predictability scale (P2(b)):** the corpus and uniform arms are indistinguishable
on P, so at that profile the aggregate plurality the *modal* statistic sees is
graph-forced. (This is consistent with the plural-preference record finding
`aggregate` CI-separated on *evenness* — the order-1 and order-∞ statistics need not
agree, and here they do not.)

### The verdict slice — M2 produces two distinct static mixtures, in four of five profiles

Per-place JSD between a place's post-success and post-failure next-distributions,
visitation-weighted over the places carrying both slices (≥ 8 decisions each), corpus
arm against the **verdict-blind null** — an overlay that never lets the verdict
condition routing, so its two per-place slices are samples of the same distribution
by construction:

| profile | corpus per-place JSD | verdict-blind null | CI-separated |
|---|--:|--:|:-:|
| `objective_exfiltration` | 0.059 [0.058, 0.092] | 0.012 [0.013, 0.042] | **yes** |
| `objective_impact` | 0.034 [0.029, 0.052] | 0.004 [0.004, 0.033] | no |
| `objective_exfiltration_impact` | 0.016 [0.011, 0.027] | 0.001 [0.001, 0.008] | **yes** |
| `objective_none_c2` | 0.059 [0.051, 0.073] | 0.002 [0.002, 0.016] | **yes** |
| `aggregate` | 0.072 [0.074, 0.100] | 0.027 [0.027, 0.065] | **yes** |

The corpus arm's verdict slices clear the null on the point estimate in **five of
five** and CI-separate in **four of five** (`objective_impact` overlaps at this seed
count — the reported partial negative). So the failure-conditioned routing (M2) is
**not** a no-op on the composition: the policy declares and realises two genuinely
different static mixtures depending on the substrate's verdict.

**This does not move axis 4, and the distinction is load-bearing.** That the verdict
splits the *composition* is a statement about the shape of the stationary policy; it
is not a statement about *outcome*, which is what axis 4 turns on. The verdict-blind
ablation on record showed no progression measure separating from the conditioned arm
across 1 600 paired runs
([`experiment_02_findings.md`](experiment_02_findings.md) §11) — routing on the
verdict is *approximately free* in outcome terms. Both hold together: **the two
mixtures differ, and switching between them confers no shown advantage.** That is the
precise, and honest, characterisation — a different composition is not a better one.

## Verdicts

**The attack model demonstrates strategic plurality as a single detectability-grade
scalar, applied to both attack models, with the scripted baseline pinned at the
boundary by construction.** The movement attacker's realised predictability is
0.33–0.57 against the scripted baseline's constructed 1.00, CI-separated in every
profile, carrying 2.7–5.9 effective next-moves per decision state against the FSM's
one. The metric sits inside the thesis's own premise — MTD rests on denying the
attacker a predictable defence, and the adversary it is canonically evaluated against
is itself perfectly predictable; this model changes exactly that property, and the
instrument measures the change with one number the baseline pins at 1.00 with zero
estimation noise.

**Reported as findings, whichever way they landed:**

- **`aggregate` shows no preferred concentration at the P scale (P2(b)):** corpus and
  uniform-null predictability are indistinguishable there, so that profile's modal
  plurality is graph-forced. The other four CI-separate, in *both* directions.
- **`objective_impact`'s verdict slice does not CI-separate from the verdict-blind
  null (P2(c), one profile):** the verdict measurably splits the composition in four
  of five profiles, not five.
- **The direction of the corpus-vs-uniform gap is profile-dependent** — concentrate
  ×2, broaden ×2 — so the claim rests on the direction-agnostic CI-separation, never
  the sign. This reproduces the plural-preference record's finding, including the
  `objective_none_c2` broadening, on an independent (order-∞) statistic.

**The boundary, unmovable:**

- **No advantage.** A lower P is a plural preferred repertoire, not a better outcome;
  the experiment-2 negative (§11) travels with every figure. The verdict-slice result
  says M2 produces two distinct static mixtures, and says nothing about whether
  switching between them helps — the ablation on record says it does not.
- **Stationary policy, never adaptivity.** Every number is a re-read of the static
  corpus weighting under the modulators-null configuration. Axis 4 stays DESIGNED and
  axis 3 DEMONSTRATED; **no badge moves** — this is the thesis-argument evidence their
  prose leans on, a superset of the badge, exactly as
  [`plural_preference.md`](plural_preference.md) is.
- **The FSM's P = 1 is a construct, not a measurement.** It is a theorem about a
  deterministic program, confirmed by the reader self-test; the trace-based residual
  above 1 is unmodelled enumeration state, not policy plurality.

**What the thesis may now claim.** That the attack model is *less predictable than its
procedural baseline* in a precise, single-scalar sense — its next move cannot be
called from its own decision state at the rate the scripted attacker's can — measured
on both models by one instrument that pins the baseline at 1.00 by construction, with
the movement attacker between the deterministic and the uniform-dithering poles in
every profile, and with the failure verdict shown to split its composition into two
distinct static mixtures in four of five profiles. **What it may not claim:** any
advantage from that plurality, or any within-run adaptive selection — the plurality
is a property of the stationary policy, and it stops exactly there.

## Reconciliation with plural_preference

The two records measure different objects — this one conditions on the decision state,
[`plural_preference.md`](plural_preference.md) pools unconditionally — so they are not
expected to share numbers, but they agree qualitatively where they touch: the corpus
weighting concentrates most profiles and broadens `objective_none_c2` out of a
topological funnel (identical direction, identical profile), and the aggregate
profile's order-1/order-∞ disagreement (evenness-separated there, P-unseparated here)
is the expected behaviour of two different Hill orders on the same distribution. Both
records carry the same boundary: variety-with-purpose in the *policy*, never dynamic
strategy.

## Figures

Both from `predictability_figs.py`, deterministic from `pred_results.json`;
diagnostic house style (no accentuation, shape + grey shade, greyscale/CVD-safe);
conditions carried in the figure.

- **`fig_predictability_regime.png`** — the headline. Per profile, the corpus arm's
  predictability P and the uniform-weight null's with 95 % bootstrap CIs, against the
  scripted baseline's constructed P = 1.00 reference line. The movement attacker sits
  far below the baseline in every profile.
- **`fig_calibration_ladder.png`** — the reader self-test. The FSM's effective breadth
  D_policy at the three conditionings (1.62 → 1.30 → 1.00), collapsing toward the
  construct; the movement corpus arm's D_policy band (2.7–5.9) beside it, surviving
  full conditioning on every variable its policy consults.

## Reproduction

```
PYTHONPATH=src python data/misc/_viz/predictability/predictability_run.py --mode convergence --max-seeds 120
PYTHONPATH=src python data/misc/_viz/predictability/predictability_run.py --mode arms --seeds 100
PYTHONPATH=src python data/misc/_viz/predictability/predictability_analyse.py
PYTHONPATH=src python data/misc/_viz/predictability/predictability_figs.py
```

The runner persists per-run conditional compositions to `pred_runs.jsonl` (untracked);
the analyser emits `pred_results.json`; the figure script reads that and writes the two
PNGs — all deterministic (SIM-05). The four scripts are committed (the
`data/misc/_viz/predictability/` gitignore exception); their outputs stay untracked.

The reader lives in
[`measures.py`](../../../../src/mtdsim/l3_simulation/movement/measures.py) §11
(`modal_probability`, `conditional_composition`, `declared_conditional_composition`,
`predictability_report`, `fsm_decisions`, `fsm_conditional_composition`), covered by
`tests/l3_simulation/test_movement_measures.py`.
