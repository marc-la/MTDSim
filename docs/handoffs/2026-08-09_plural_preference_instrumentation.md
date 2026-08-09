---
status: open
created: 2026-08-09
---

# Instrument plural preference across the attack model's dimensions — turn "there is no fixed strategy" into "the attacker favours a success-weighted mixed set over one rule"

## The claim this exists to support

The dissertation argues the model demonstrates **strategic plurality**. Variety
is already demonstrated and instrumented
([`../implementation/pipeline/ogasp/plurality_reporting.md`](../implementation/pipeline/ogasp/plurality_reporting.md)
§5, `fig_opening_variety.png`): the attacker admits 2–10 distinct five-place
openings per profile where the inherited FSM admits exactly one. But **variety
is only the prerequisite** — a model can be various and strategically empty
(uniform random branching produces many openings and prefers none of them). The
open job is to instrument the *positive* claim: the attacker does not follow one
strict rule (the negative, largely shown), **and** it favours a *mixed set of
behaviours* — a plural, preferential, success-aligned mixture — over that one
rule (the positive, not yet shown). That mixture-with-preference is what
"strategic plurality" has to mean here, and it has to be measured, not asserted.

**The honesty ceiling, fixed before any work starts.** What is in reach is a
statement about the model's **stationary policy**: it is a success-weighted
plural mixture, categorically unlike the baseline's single deterministic rule.
That is *not* a claim of within-run adaptive selection (axis 4 is DESIGNED and
the verdict-blind ablation showed routing approximately free; axis 6/7 dials
narrow rather than steer, and P1 fired). Strategic plurality in this handoff =
**variety with purpose in the policy**, never dynamic strategy. Every figure and
caption carries that boundary.

## State of play

**Demonstrated and banked.** Variety at the opening level (the figure), pooled
path entropy 1.451–2.714 bits, 2–10 distinct openings, and the profile ×
mechanism interaction — all in `plurality_reporting.md`, none re-scored here.
Axis 3 is already DEMONSTRATED; **this handoff does not move it** — it builds the
evidence the *thesis argument* leans on, which is a superset of the badge.

**The gap, quantified.** The distinction is operational: variety is the
**support** of the behaviour distribution (how many behaviours can appear);
plural preference is the **shape of the mass over that support**. The signature
that separates the three regimes, per behavioural dimension:

| regime | support N | effective number D = 2^H | evenness D/N | reading |
|---|--|--|--|--|
| baseline FSM | 1 | 1 | — | one strict rule |
| uniform variety (noise) | large | ≈ N | ≈ 1 | various, not strategic |
| **plural preference** | > 1 | 1 < D < N | < 1 | favours a mixed subset |

**Why the current figure cannot carry the positive claim (measured, not
assumed).** At the opening level with 10 seeds, `objective_exfiltration` reads
10 distinct openings at evenness **1.00** — indistinguishable from uniform noise
because 10 draws cannot populate a distribution over openings; while the
concentrated profiles read D = 1.38 (`objective_exfiltration_impact`, one
opening carrying 9/10) to 2.56 (`objective_none_c2`). So where variety is high
the preference is undersampled, and where preference is visible the plurality is
low. The opening-level, 10-seed data proves variety and **cannot separate plural
preference from either noise or near-monostrategy.** (Numbers reproducible from
`expo02_ashen_lynx/runs.jsonl`; the computation is in this session's chat and
belongs in the new record.)

**Why the transition level is not a shortcut.** Step-level entropy gives 2.7–6.6
effective next-places, which *looks* like plural preference — but P1 fired
(Spearman ρ = −0.97 between pooled entropy and max single-place visit share:
`plurality_reporting.md` §4), so at the step level entropy is entangled with
hub-occupancy and cannot carry the claim alone. **Measure at the behaviour
(strategy) level and across several dimensions**, where a single hub cannot
manufacture the result.

## Recommended approach

Three moves, in order. The third is the one that turns variety into strategic
plurality; the first two make it estimable and honest.

### 1. Define the behavioural dimensions of the "full attack model"

Plural preference is a property of the *policy*, so instrument it on several
independent slices of behaviour, not just openings — a preference that holds
across dimensions is a policy property; one that appears on a single dimension is
a suspected artefact. Candidate dimensions, each already present in the recorded
runs or derivable from them:

- **opening sequences** — k-place prefixes (the variety figure's own unit).
- **realised path / tactic-sequence** — the full place walk.
- **action-verb mix** — `verb_mix` per run (fraction of attempts per verb).
- **place-visit distribution** — `visit_distribution` (the L2 convention, reused
  from `profile_divergence`).
- **terminal behaviour** — `terminal_mode` / terminal place distribution.

For each dimension, the empirical distribution is taken over runs (pooled per
profile), and the measure below is computed on it.

### 2. The measure — Hill number + evenness + success-alignment, per dimension per profile

- **Effective number of behaviours** `D = 2^H` (Hill number of order 1; H the
  Shannon entropy of the dimension's empirical distribution). D = 1 is one
  behaviour; D = N is uniform.
- **Evenness** `D/N` (Pielou). Below 1 means preference (concentration on a
  subset); at 1 means uniform.
- **Success-alignment** — the step that makes preference *strategic* rather than
  merely concentrated: rank-correlate the mass on each behaviour against that
  behaviour's realised success (objective progress / distinct hosts / a defined
  success proxy), or against its corpus weight (the corpus is documented
  *successful* campaigns, so corpus weight is a success prior). A positive
  correlation says the favoured subset **is** the successful subset.

Reuse `path_entropy_from_transitions`, `visit_distribution`, `jsd`, `mean_ci`,
`interval_report` from
[`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py) §2 — extend
the suite, do not re-derive the maths (the module owns entropy the one way).

### 3. The linchpin — the uniform-weight ablation (the argument's clincher)

This is what separates *variety from topology* (structural, not strategic) from
*preference from the success-weighting* (strategic). **Feasibility confirmed this
session:** the net stores each place's out-distribution as
`ClassNet._out: place → {dst: weight}`
([`net.py`](../../src/mtdsim/l3_simulation/movement/net.py) §`base_out_weights`);
a uniform-weight variant replaces each place's out-distribution with equiprobable
mass over *its own destination set* — same support N, same reachable graph, the
corpus preference stripped. Clean, no schema change, injectable as a
post-construction transform on `_out` or a `ClassNet` variant.

Run three arms on matched seeds, modulators null, no MTD, v2_partial:

- **baseline FSM** — D = 1 on every dimension (the single rule).
- **uniform-weight null** — the graph's branching with the preference removed:
  variety survives (N ≈ unchanged), and if evenness rises toward 1 / D toward N,
  the concentration in the real arm was weight-driven.
- **corpus-weighted (shipped) arm** — the model as reported.

**The gap between the corpus-weighted arm and the uniform null IS the strategic
content.** If the corpus arm is measurably more concentrated (lower evenness,
lower D) than the uniform null on ≥ most dimensions, *and* its favoured subset is
success-aligned, then the attacker demonstrably favours a mixed set of
successful behaviours over both the baseline's single rule and an unweighted
mixture. That is strategic plurality, demonstrated by contrast rather than
asserted.

### Seed count

Bump seeds until the opening/path-level D and evenness are stable (10 is
provably too few — §State of play). Decide the count in pre-registration from a
convergence check on one profile (e.g. D within ±0.2 across two disjoint seed
halves), not by eye. Every dimension shares the seed set.

### Alternatives considered, and why this wins

- *More seeds alone, no ablation.* Estimates the shape but cannot say the
  preference is strategic rather than structural — the uniform null is the only
  thing that isolates the weights' contribution. Rejected as insufficient.
- *Transition-level entropy only.* Dense but P1-entangled with hub-occupancy;
  cannot carry the claim. Rejected as the primary, kept as a cross-check.
- *Success-alignment via a bespoke within-run success model.* Heavier than
  needed; the corpus weight is already a validated success prior and the
  substrate already reports per-run progress. Prefer the cheap proxies first,
  and say which was used.

## Validation gate

1. **Pre-registration committed before any arm is run** (§Pre-register below),
   git-history-dated.
2. **Three arms on matched seeds**, readers plus the two extra arms; the shipped
   arm's numbers reproduce `plurality_reporting.md` §2 where they overlap.
3. **The measure table**: D, evenness, success-alignment per dimension per
   profile, for all three arms, with `interval_report` intervals — **no ordering
   or "more concentrated" claim without disjoint intervals.**
4. **The clincher stated whichever way it lands**: for each dimension, is the
   corpus arm CI-separated from the uniform null on evenness? Report the
   dimensions where it is *and* where it is not.
5. **Figures regenerate from a committed script** into
   `data/misc/_viz/plurality/`, deterministically, from recorded runs; conditions
   carried in every figure (arm, mapping, MTD, seed count, dimension).
6. **Full `tests/l3_simulation` plus substrate/carve/golden suites pass** — the
   new arms add readers and a net variant; a moved golden means the shipped
   walk changed and must be explained, not accepted.
7. **Record** at
   `docs/implementation/pipeline/ogasp/plural_preference.md`: the measure, the
   three-arm table, the per-dimension clincher verdicts, and the ruling on what
   the thesis may claim.

## Pre-register before running

- **P1 — direction.** Committed in advance: corpus-weighted evenness < uniform-
  null evenness on ≥ 3 of the 5 dimensions (the attacker concentrates more than
  the graph forces); baseline D = 1 on all; success-alignment correlation
  positive. On record before the arms exist.
- **P2 — kill criterion.** If the corpus and uniform arms are CI-indistinguishable
  on evenness for a dimension, that dimension carries **no** strategic preference
  beyond topology — reported as a negative for that dimension, never massaged.
  A claim that survives on 1 of 5 dimensions is a weak claim and is reported as
  one.
- **P3 — seed count** fixed by the convergence check, before the full run.

## Hard constraints

- **Strategic plurality = stationary-policy property, never adaptivity.** The
  claim is a plural, success-weighted *mixture*, contrasted with one rule — not
  within-run selection. Do not let any figure read as axis-4 adaptation. The
  variety-not-strategy limit travels; this handoff sharpens "variety" to "plural
  preference," it does not promote it to "dynamic strategy."
- **The reported-configuration pin holds.** Modulators null is the correct arm —
  this measures the *static corpus weighting*, which is exactly the
  modulators-null policy ([`model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
  §4). Any modulator-active reading is a separate arm with its own figure.
- **No badge move.** Axis 3 is DEMONSTRATED; nothing here re-scores it. This
  builds thesis-argument evidence, not a badge.
- **Scores move on evidence only** (S6;
  [`../workflows/guardrails.md`](../workflows/guardrails.md)) — never retune
  weights, mapping or metrics to deepen the concentration.
- **Measure at the behaviour level and across dimensions** — the P1 lesson: a
  single hub must not be able to manufacture the result. The uniform-weight null
  is the defence against a topology artefact; multiple dimensions are the defence
  against a single-slice artefact.
- **The label-drift trap.** Recorded runs carry the pre-2026-08-06 profile names
  (`pure_steal`, …); read labels off the corpus and normalise, refuse empty
  cells — `plurality_reporting.md` §7 and the axis-5 §7 precedent.
- Determinism (SIM-05); Australian English; branch per session; commit locally;
  **never push**.

## Reading list

- [`../implementation/pipeline/ogasp/plurality_reporting.md`](../implementation/pipeline/ogasp/plurality_reporting.md)
  — the variety evidence, the P1 firing, the null reconciliation, and §6's
  variety-as-prerequisite framing this handoff executes.
- [`../../src/mtdsim/l3_simulation/movement/net.py`](../../src/mtdsim/l3_simulation/movement/net.py)
  §`ClassNet` / `base_out_weights` — where the out-weights live and where the
  uniform-weight variant injects.
- [`../../src/mtdsim/l3_simulation/movement/measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py)
  §2 — the entropy / visit-distribution / interval readers to extend.
- [`../implementation/pipeline/ogasp/weight_sensitivity_study.md`](../implementation/pipeline/ogasp/weight_sensitivity_study.md)
  — the routing-weight provenance and the existing weight-perturbation study, the
  sibling to the uniform-weight ablation.
- [`../implementation/pipeline/gap/gap_schema.md`](../implementation/pipeline/gap/gap_schema.md)
  — the corpus is analyst-curated Attack Flows of documented (successful)
  campaigns; why corpus weight is a success prior.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(b), §(d) axis 3 — the census-not-a-scale claim and the badge's standing
  qualifications, so the thesis claim stays inside them.

## Out of scope (explicitly)

- **Any new mechanism, modulator, or weight re-declaration.** The uniform-weight
  arm is an *ablation* (a read of the existing weights flattened), not a new
  model.
- **Within-run adaptive selection** — that is axis 4, separately tracked and
  DESIGNED. This handoff must not blur into it.
- **Re-scoring axis 3** or any row.
- **Dissertation prose and chapter placement.** The record names what may be
  claimed; where it lands in the thesis is a later pass.
- The axis-2 ablation and axis-4 unrun readers — adjacent, separately tracked.

## Return format

Default (see [`../workflows/session_workflow.md`](../workflows/session_workflow.md#handoff-workflow)):
report back framed in terms of the thesis and succinctly — does the model
demonstrate plural preference (strategic plurality) or only variety, on how many
dimensions, and what may now be claimed versus what stays future work — and point
at the committed `plural_preference.md` for the detail.
