---
status: durable
created: 2026-07-23
updated: 2026-08-19
topic: "A precedent for provenance-tracking declared-knowledge values (numbers reasoned from judgement, not measured from a source) and maintaining their justification through adversarial cross-examination — the living value-provenance & scrutiny ledger"
---

# Declared-value provenance — the scrutiny ledger precedent

Some load-bearing numbers in this project are **not measured from a citable
source**. They are **declared knowledge**: values reasoned from domain logic,
practitioner reports, literature, and intuition — an *envelope*, not a recovered
truth. The L3 outcome (policy) overlay is the first of these; there will be more.

Such values cannot be provenance-tracked the way
[`provenance.md`](provenance.md) tracks a constant back to a paper table — there
is no table. Their defensibility instead rests on **the quality of the reasoning
and the adversarial scrutiny it has survived**. This document is the **precedent**
for capturing that: a *living ledger* that travels with the values, records why
each is what it is, at what evidential tier, and how it has been reworked through
successive cross-examinations.

> **Use this when** a value is reasoned/declared (no citable measurement).
> **Use [`provenance.md`](provenance.md) instead when** a value traces to a paper,
> spec row, or the inherited code — that is a different provenance regime
> (source → locator → disposition). The two are complementary, not alternatives.

## 1. The three requirements

A declared value is only defensible if it is **reproducible, tiered, and scrutinised.**

1. **Reproducible, not post-hoc.** Declared values must be **rule-generated from a
   small model**, not hand-set per instance. A generator must reproduce the whole
   set deterministically (e.g. the overlay generator reproduces its 123-pair table
   *0/123* before any edit). This proves the values follow from stated rules rather
   than being fitted after the fact, and it makes a rework a one-line rule change,
   not a mass edit. It also kills the redundancy of storing the same value-and-reason
   per instance: the rationale lives **once per rule**.
2. **Tiered by evidence.** Every value declares its **provenance tier** (below), so
   an examiner sees exactly how grounded each number is. Hiding a weak tier behind a
   confident-looking number is the failure mode this prevents.
3. **Scrutinised adversarially.** Every value carries a **scrutiny record** — which
   review rounds saw it, what was challenged, what survived, and a current
   confidence — plus a **changelog** of how it was reworked. Scrutiny is not a
   one-off sign-off; it is a maintained history.

## 2. Provenance tiers

| Tier | Meaning |
|---|---|
| `corpus-grounded` | derived from CTI / corpus data. *(For a deliberately CTI-independent layer like the overlay, this tier must stay empty — see §5.)* |
| `attested-pattern` | the *behaviour* is documented in reports/literature (get-in/spread sequences, perimeter retry loops); the exact *magnitude* is still declared. Record it as `attested-pattern/declared-magnitude`. |
| `declared-judgement` | reasoned from first-principles logic (here: kill-chain + foothold-dependency); not attested. Reports rarely record it (e.g. what an attacker does *after a step fails*). The honest floor tier. |

Stating the tier is itself a methodological finding, not an apology: a layer whose
weak half is *labelled* weak is more defensible than one that pretends uniform
grounding.

## 3. The ledger schema

The ledger is **machine-readable, embedded with the rules** (rationale sits with
the value it explains). Per rule:

```
id            — the rule identifier (the compiled per-pair view tags each pair with it)
value         — the number
rationale     — why this value; ONE sentence, stored once per rule (never per pair)
provenance_tier — §2
status        — stable | provisional | contested
confidence    — current %, from the latest review round
scrutiny      — which rounds reviewed it, what was challenged, what survived
changelog     — [ round: from → to, and why ] — the rework history
```

**One schema extension, in use since 2026-07-28.** A declared term is sometimes a
small *function* rather than a single number — the overlay's lifecycle-distance
kernel is two decay ratios and a floor. Such an entry carries `parameters`
(a named constant per key) in place of `value`, and every other field unchanged.
The distinction is not cosmetic: a parameterised term's defence is a **sweep over
its declared bands** rather than an argument about one magnitude, so requirement 3
below is discharged differently for it — see §4's last paragraph.

A top-level `ledger_meta` block records the shared context: the tier definitions,
the `review_history` (the ordered list of cross-examination rounds), the
`reproducibility` claim (generator + the 0/N reproduction check), and the
`maintenance` protocol (§4).

## 4. The maintenance protocol — reworking through adversarial review

The ledger is **updated by the cross-examination process**, not frozen:

1. **A round runs.** A panel of independent adversarial reviewers (diverse lenses:
   DFIR fidelity, ATT&CK methodology, probabilistic coherence, a hard examiner)
   scrutinises the values, each finding **adversarially refuted** before it counts,
   and grounds claims in re-runnable evidence (routed mass, stepped traces), not
   assertion.
2. **Surviving changes fold in** as **generalising** rule edits — never
   pair-specific or profile-specific hacks (that is overfitting, forbidden). Each
   edit appends a `changelog` entry (round, from → to, evidence) to its rule.
3. **The scrutiny record and confidence update** per rule. A rule whose value moved,
   or that a reviewer contested, is marked `provisional` or `contested` and is
   **re-scrutinised next round** until it earns `stable`.
4. **A confidence panel rates the set** toward an agreed bar (here: 95%). The bar is
   met only when the residuals are *honestly stated in the record* — an unwritten
   limitation is itself a blocker.
5. **Repeat** until a round surfaces no surviving material change and the panel
   clears the bar. Then, and only then, the values are finalised.

This is the same loop whatever the values: fan-out review → adversarial refute →
generalising fold → re-scrutinise → rate. The ledger is its durable memory.

**For a parameterised term, add a sixth step: sweep the bands and record the
verdict.** Adversarial review can establish that a value's *reasoning* is coherent;
it cannot establish that a conclusion does not turn on where in its range the value
sits. Only a sweep can, and the sweep's verdict belongs in the ledger whichever way
it falls — including when it falls badly. Three things learned from the first one
([`pipeline/ogasp/weight_sensitivity_study.md`](pipeline/ogasp/weight_sensitivity_study.md)),
recorded here because they generalise to the next parameterised family:

1. **State each conclusion and its criterion before the numbers exist**, or the
   verdict is unfalsifiable. The one criterion that was a threshold on a
   continuum (a failure-mode classification at 30% blocked) produced the only
   "moved" verdict that needed an anatomy paragraph rather than a number — keep
   thresholds, but report the continuum beside them.
2. **Separate "the parameter has no effect" from "the parameter has no effect
   *here*".** One of three swept parameters moved nothing at all, because the
   corpus contains no structure for it to act on. That is a statement about the
   corpus, and reporting it as a small measured sensitivity would have been
   wrong.
3. **A conclusion can move for reasons the parameter does not control.** An
   ordering that is unstable across a sweep may be unstable because the run count
   cannot separate the things being ordered. Test the separation (disjoint
   confidence intervals) before attributing the instability to the value.

## 5. Guardrails these values must not cross

- **No reverse-engineering from the layers they condition.** A declared layer that
  *conditions* a data-grounded layer (the overlay conditions the CTI-grounded base
  weights) must be authored from declared knowledge **only** — never tuned to fit
  the data it multiplies. Diagnosing a coherence failure *with* the data is allowed;
  choosing a value *to match* the data is reverse-engineering. Keep a bot on this
  (the CTI-independence / scope-creep audit).
- **No overfitting.** Values generalise across instances (pairs) and contexts
  (profiles). Test on a corpus-neutral synthetic case to confirm a value is not
  merely masked by one context's data.
- **Complete coverage.** Author the **whole** value space (every ordered pair), not
  only the cases the current corpus exercises — so a different corpus/CTI that
  introduces a new case is already covered. Which cases *route mass* is a property
  of the data layer, not the declared layer.

## 6. Instances of the precedent

### 6.1 The reference instance — the L3 outcome overlay

The overlay is the worked example of this precedent:

- **Rules (source of truth):**
  [`../../data/ogasp/controller/outcome_rules.json`](../../data/ogasp/controller/outcome_rules.json)
  — the model (the two orderings / enables / foothold / the distance term) + the 5
  success and 9 failure rules and the `distance_rule` entry, each carrying value
  (or `parameters`), rationale, tier, status, confidence, scrutiny, changelog; plus
  the `ledger_meta` block.
- **Compiled views:**
  [`../../data/ogasp/controller/overlays/`](../../data/ogasp/controller/overlays/)
  — a **registry**, one directory per value set that has been run, plus a
  `manifest.json` recording each version's compilation recipe and what consumed it.
  Each version holds `success.json` / `failure.json` over the complete 210-pair
  space (corpus-agnostic). Generated from the rules; do not hand-edit. Versions:
  `v1_band_relationship` (experiment 1's, frozen) and `v2_lifecycle_distance` (the
  S1 fold-in). The default stays at experiment 1's, so an unqualified load
  reproduces what has always run.
- **Generator and reproduction check:**
  [`../../src/mtdsim/l3_simulation/controller/rules.py`](../../src/mtdsim/l3_simulation/controller/rules.py)
  — `--write` regenerates every registered version, `--check` re-compiles each and
  reports any cell that differs from what is committed (0 of 420 per version). This
  is requirement 1 enforced by tracked code rather than by an in-session script.
- **Loader:**
  [`../../src/mtdsim/l3_simulation/controller/outcome.py`](../../src/mtdsim/l3_simulation/controller/outcome.py)
  (`load_outcome_overlay`, `load_overlay_registry`, `rule_for`).
- **Design + decision record:**
  [`pipeline/ogasp/success_failure_overlay_design.md`](pipeline/ogasp/success_failure_overlay_design.md),
  [`pipeline/ogasp/weight_sensitivity_study.md`](pipeline/ogasp/weight_sensitivity_study.md)
  (the S1 fold-in, the re-examined caveats, and the sweep verdict),
  [`pipeline/ogasp/supervisor_decision_register.md`](pipeline/ogasp/supervisor_decision_register.md).
- **Presentation on the page (2026-08-19):**
  [`pipeline/ogasp/failure_weight_decomposition.md`](pipeline/ogasp/failure_weight_decomposition.md)
  — the failure set drawn as (rule kernel) × (distance kernel) → committed
  matrix, every cell printed, with a two-pair walkthrough; generated by
  `tools/failure_weight_decomposition_figure.py` from the rules + consensus
  through the tracked compiler. The reproducibility requirement, made visible.

Its ledger reads: reproducible (0/420 per registered version, by tracked
generator), review history **R0→R4 complete** (~90 agents: initial cross-exam →
branching red-team → composed-net validation → stepwise simulation), all rules
`stable`, final finetune synthesis an **empty change set** (values converged).
**R2 finalised 2026-07-23** (Marc greenlit) at a certified 82%; the 82→95%
remainder was recorded as the dissertation defence of the reasoning rather than
value uncertainty.

**Then S1 reopened it, and the reopening is the more instructive half of the
precedent.** Supervision named one defect the four review rounds had not found —
the values graded a transition by direction and not by distance — which is a
standing lesson about what adversarial review of *internal coherence* can and
cannot catch. The fold-in landed as one new parameterised ledger entry
(`distance_rule`, tier `attested-pattern/declared-magnitude`) with **no R2 rule
value changed**, and the magnitudes now carry a sweep verdict rather than only an
argument: **two of four tested conclusions held across the declared bands and two
moved**, with one of the three parameters found to be behaviourally inert on this
corpus. That mixed verdict is recorded as the result, not softened
([`pipeline/ogasp/weight_sensitivity_study.md`](pipeline/ogasp/weight_sensitivity_study.md)).

So the precedent now runs end to end *including the failure case*: a
declared-knowledge layer carried from authoring, through adversarial rework, to a
finalised evidence-tiered artefact — and then through an externally-named defect,
a versioned re-derivation that keeps the superseded values reproducible, and a
sensitivity verdict that does not flatter it.

### 6.2 The second instance — the within-run learning capability (criterion axis 7)

The learning family is the first to adopt the precedent from scratch rather than
inherit it mid-life, and it is instructive for a different reason: **it is a
two-parameter family, so almost all of its defensibility rests on the sweep**
rather than on an argument about magnitudes. There is no table of 210 authored
values to cross-examine — there are two numbers and a rule.

- **Rules (source of truth):**
  [`../../data/ogasp/movement/learning_rules.json`](../../data/ogasp/movement/learning_rules.json)
  — the rule model (credit assignment, the Laplace estimator, the routing
  exponent, the forgetting rule) plus the two declared parameters, each carrying
  value, sweep band, tier, status, confidence, rationale, an explicit *band
  argument*, and its scrutiny/changelog fields.
- **Compiled view and reproduction check:**
  [`../../data/ogasp/movement/learning_factors.json`](../../data/ogasp/movement/learning_factors.json),
  generated by
  [`../../src/mtdsim/l3_simulation/movement/learning.py`](../../src/mtdsim/l3_simulation/movement/learning.py)
  (`--write` / `--check`, 0 of 186 cells differing, pinned by a test).
- **Design + sweep record:**
  [`pipeline/ogasp/learning_capability.md`](pipeline/ogasp/learning_capability.md).

Three things it adds to the precedent, each generalising beyond this family:

1. **A parameter can be excluded from the sweep on principle, and that exclusion
   is itself a declared decision.** The estimator's prior (α = β = 1) is *not*
   swept, because any asymmetric prior asserts a belief about how often tactics
   pay — a belief with no source, settable only by looking at the layer being
   conditioned, which §5's first guardrail forbids outright. Recording *why* a
   knob is not a sweep dimension is as load-bearing as recording the bands of the
   ones that are.
2. **The band must be argued from what the parameter means, including where it
   must be wide enough to contain a failure.** The learning exponent's band runs
   up to a near-greedy value not because that value is plausible but because a
   band that excluded the collapse of traversal plurality could not demonstrate
   the trade-off the axis owes. A band chosen only for plausibility can hide the
   cost of the mechanism it parameterises.
3. **Where a runtime rule generates values, the authored artefact is the rule.**
   This family conditions a CTI-grounded layer at *runtime* rather than at
   authoring time, which looks superficially like the reverse-engineering §5
   forbids. The distinguishing test is whether the null parameter recovers the
   grounded prior exactly — here it does, bit for bit — so the weights that
   emerge during a run are a consequence of the model's behaviour rather than an
   authoring act. Any future runtime-conditioning layer should be held to the same
   test.

### 6.3 The third instance — the attacker benefit family (criterion axis 6)

The overlay is the mature worked example; the attacker's **benefit** family is
instructive for the opposite reason — it is at an early stage and does not
pretend otherwise.

- **Rules and ledger:** [`../../data/ogasp/attacker_utility.json`](../../data/ogasp/attacker_utility.json)
  — two benefit rules (`objective`, `instrumental`), three declared parameters
  (`rho`, `cost_floor_s`, `lambda`), and the `ledger_meta` block.
- **Compiled view:** [`../../data/ogasp/attacker_utility_benefit.json`](../../data/ogasp/attacker_utility_benefit.json)
  — the complete 5 × 15 space, generated, never hand-edited.
- **Generator and reproduction check:**
  [`../../src/mtdsim/l3_simulation/movement/utility.py`](../../src/mtdsim/l3_simulation/movement/utility.py)
  — `--write` / `--check`, reporting **0 of 75** differing cells, guarded by
  `tests/l3_simulation/test_movement_utility.py`.
- **Design record:** [`pipeline/ogasp/incentive_rationality.md`](pipeline/ogasp/incentive_rationality.md).

Three things it adds to the precedent that the overlay did not:

1. **A declared family can be half a reuse.** The utility is a ratio of a new
   declared benefit over the *already-declared* duration catalogue. Reusing the
   cost half rather than declaring a parallel one halves what must be defended
   and inherits that artefact's tiers and completed sweep — and it removes the
   drift risk that two catalogues of the same quantity would carry. When a new
   declared term can be expressed over an existing one, prefer that.
2. **Requirement 3 can be discharged by sweep alone, and the ledger must say
   so.** Every value here sits at `declared-judgement` and the family has
   survived **no adversarial round at all**. The ledger records that absence
   explicitly rather than letting the sweep's presence imply scrutiny it has not
   had. A declared family with a sweep and no review round is a legitimate
   intermediate state; an unlabelled one is not.
3. **Pre-registration is the guardrail when the layer is behavioural.** §5 forbids
   choosing a value to fit the layer it conditions. For a parameter whose effect
   is a *behaviour* rather than a table, that is hard to audit after the fact — so
   the conclusions and their criteria were committed, in a tracked file, before
   the sweep ran, with one conclusion deliberately committed in the direction that
   would embarrass a flattering result. The commit order is the audit trail. Adopt
   this for any future declared parameter whose defence is a behavioural sweep.

### 6.4 The fourth instance — the FSM-alignment dial (no axis)

The smallest family the precedent has taken: **one parameter, and its declared
value is the null**. It is instructive precisely because of that.

- **Rules and ledger:**
  [`../../data/ogasp/movement/alignment_rules.json`](../../data/ogasp/movement/alignment_rules.json)
  — the rule model (the objective-productive target set, the distance over the
  declared capability closure, the routing form, the off-band floor) and the
  single declared parameter α with its band, tier, status and band argument.
- **Design record:** [`pipeline/ogasp/fsm_alignment_overlay.md`](pipeline/ogasp/fsm_alignment_overlay.md).
- **Reproduction:** there is no compiled value table to re-derive — the distance
  model declares nothing per cell. What stands in its place is the exhaustive
  distance table and the exhaustive no-stall check, both pinned by
  `tests/l3_simulation/test_movement_alignment.py`.

Three things it adds to the precedent, each generalising beyond this family:

1. **A declared parameter's value may be the null, and that is a position rather
   than an evasion.** α is a dial on an instrument, not a setting on a mechanism:
   the sweep is the finding and no point on the band is a claim. Declaring the
   null puts the burden of argument on any arm that moves it, and it makes the
   shipped model the α = 0 special case of this one. Where a family's *purpose* is
   measurement rather than capability, prefer this to declaring a plausible
   operating point nobody intends to defend.
2. **A tier row can be argued *empty*, and saying why is load-bearing.** The
   `attested-pattern/declared-magnitude` tier is empty here not by oversight but
   because no literature attests a rate at which an attacker conforms to a
   simulator's procedural order — the quantity is an artefact of *this evaluation*
   rather than a property of any adversary. Recording the reason a tier cannot be
   reached is as informative as recording which tier a value sits at.
3. **A reproduction check can be a reachability proof rather than a value diff,
   and it must be shown to have teeth.** This family's analogue of the 0-of-N
   check is an enumeration over the declared space asserting that the parameter's
   limiting end cannot empty a routing decision. It caught a genuine defect on its
   first run, and it is itself checked against a deliberately sabotaged input —
   because a check that cannot be made to fail evidences nothing, which is a
   standard the earlier 0-of-N checks met only implicitly.

### 6.5 The fifth instance — the FSM-succession dial (no axis)

The immediate successor to §6.4, and it earns its own entry for one reason the
precedent had not previously had to state.

- **Rules and ledger:** [`../../data/ogasp/movement/succession_rules.json`](../../data/ogasp/movement/succession_rules.json)
  — one declared parameter, α, a float over [0, 1] whose declared value is again
  the null.
- **The relation it consumes:** [`../../data/ogasp/controller/fsm_succession.json`](../../data/ogasp/controller/fsm_succession.json)
  — a **transcription**, not a declared family: it carries no magnitudes and no
  tiers, because every row is a statement about what the host simulator's own
  attacker does.
- **Design record:** [`pipeline/ogasp/fsm_succession_overlay.md`](pipeline/ogasp/fsm_succession_overlay.md).

**What it adds to the precedent: a transcription has an oracle, and the ledger
should make you use it.** §6.4's reproducibility clause was a reachability proof
because there was no value table to diff. Here there is something better — the
thing being transcribed is *executable*, so the relation can be checked against
the substrate's own observed behaviour rather than against a reading of its
source. That check caught a genuine omission on its first run (a successor
reachable only through a fallback guard on another verb's loop branch), which
neither reading the dispatch wrappers nor cross-examining two independent
published figures had surfaced. **Where a declared artefact transcribes something
that runs, run it** — and where it transcribes something that does not, say so, so
a reader knows which kind of assurance the entry carries.

### 6.5a A rider on the fifth instance — the token-hold bound (register T1, no axis)

Recorded as a rider rather than a seventh instance because it declares nothing
new about the attacker: it is one backstop integer attached to the same rules
artefact, and the rule it bounds is a *supervisor-directed band point* beside
factor 9, not a factor.

- **Rules and ledger:** [`../../data/ogasp/movement/succession_rules.json`](../../data/ogasp/movement/succession_rules.json)
  §`token_hold` — one declared parameter, `max_consecutive_holds` = 20,
  declared-judgement, provisional.
- **What it bounds:** the opaque token hold (Jin's T1 fix): the token is held
  at its place, paying a re-dwell per hold, until the draw lands on a place
  whose verb the inherited FSM licenses. Holds are geometric in the licensed
  mass of the composed out-distribution, so the bound turns a vanishing
  licensed mass into a counted fall-through rather than a consumed horizon.
- **Record:** [`pipeline/ogasp/fsm_token_hold_findings.md`](pipeline/ogasp/fsm_token_hold_findings.md).

**What it adds to the precedent: a backstop is declared like a value but
defended like a rate.** The number itself carries no claim (no operating
point is a statement about any adversary, exactly as α's is not); what the
ledger owes is the *rate at which the backstop acted*, reported beside every
result the rule produces. A bound whose fall-through rate is material has
become part of the mechanism, and the record must then say so rather than
quote the rule's result as the rule's alone. The stopping rule forbids
re-tuning it on the numbers.

### 6.6 The sixth instance — the axis-5 exposure family (criterion axis 5's metric)

The first family whose **grounded half and declared half sit inside a single
term**, and it earns its entry for what the sweep did to one of its parameters.

- **Rules and ledger:** [`../../data/ogasp/movement/exposure_rules.json`](../../data/ogasp/movement/exposure_rules.json)
  — the recursion, the ordinal tier assignment over all fifteen tactics, the
  native-verb tier rule, and three declared parameters (`tau`, `rho`, `delta`),
  each with its band, band argument, tier and scrutiny fields.
- **Compiled view and reproduction check:**
  [`../../data/ogasp/movement/exposure_increments.json`](../../data/ogasp/movement/exposure_increments.json),
  generated by
  [`../../src/mtdsim/l3_simulation/movement/exposure.py`](../../src/mtdsim/l3_simulation/movement/exposure.py)
  (`--write` / `--check`, **0 of 63** cells differing, pinned by
  `tests/l3_simulation/test_movement_exposure.py`).
- **Pre-registration and results:**
  [`pipeline/ogasp/stealth_exposure_prereg.md`](pipeline/ogasp/stealth_exposure_prereg.md),
  [`pipeline/ogasp/stealth_exposure_metric.md`](pipeline/ogasp/stealth_exposure_metric.md).

Three things it adds to the precedent, each generalising beyond this family:

1. **Grounded *order* and declared *magnitude* can live in one term, and the split
   must then be made in the arithmetic rather than in the prose.** The increment is
   `rho ^ (4 − tier)`: the tier comes from the corpus's quoted observability
   evidence and the ratio between rungs comes from nowhere but judgement. Writing
   it this way makes the boundary auditable — anyone can ask what happens at
   `rho = 1`, where the grounded order does nothing at all — where a table of
   fifteen authored numbers would have fused the two halves beyond separating.
   Prefer this shape wherever an evidence source supplies an *ordering* and not a
   scale, which is the usual case for qualitative CTI.
2. **A sweep can report that a parameter does not matter, and that is a result
   about the design rather than a hole in it.** `delta`, the weight on the
   CVSS-derived term, moves every profile's measure by **under 0.1 % across its
   entire band** — because only 5 % of visits carry a figure for it to act on, and
   across those the mean exploitability sits within half a percent of the exact
   value at which the term is identically 1.0. That term was the meeting's own
   proposal and it required a record-schema widening to compute at all. The
   widening stays, because it is what makes the inertness *knowable*; the ledger
   records the parameter as measured-inert rather than quietly dropping it. **A
   declared parameter shown to do nothing is cheaper to keep labelled than to
   remove and re-argue.**
3. **Anchor a parameter to the thing it must not degenerate against, not to the
   thing it names.** `tau` names a monitoring window, and this substrate has no
   monitor — that absence is axis 5's whole problem, so no honest external anchor
   exists. It is anchored instead to the attacker's own visit tempo, because that
   is the scale at which the instrument is neither memoryless nor a running count,
   and the band spans ×256 so that **both degeneracies are inside it**. Anchoring
   to the MTD interval was rejected outright: it would have made the instrument a
   function of the defence condition being compared. Where a parameter has no
   referent, say so and anchor it to the instrument's own failure modes.

A fourth point is worth recording as a *warning* rather than as a contribution:
this family's `attested-pattern/declared-magnitude` tier is **argued empty**, on
the §6.4 pattern, because no literature attests a per-tactic detection magnitude
transferable to this defence family — the one candidate source's own extraction
records it as non-transferable without a calibration step that does not exist in
the public record. Every parameter here therefore sits at `declared-judgement`,
and the family has survived **no adversarial round at all**. It is the §6.3
intermediate state, labelled as such.

## 7. Where this sits

- Complements [`provenance.md`](provenance.md) (paper/spec-sourced constants) — this
  precedent covers the *declared-knowledge* regime it cannot.
- Feeds, and is fed by, the decision register
  ([`pipeline/ogasp/supervisor_decision_register.md`](pipeline/ogasp/supervisor_decision_register.md)):
  a ratified modelling call (e.g. keep the C2-hub enables edit) lands as a rule
  changelog entry here.
- **When to update:** every cross-examination round (append scrutiny + changelog);
  when a value is finalised (flip `status`); when a new declared-value layer adopts
  the precedent (add its instance to §6).
