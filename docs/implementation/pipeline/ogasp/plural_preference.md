---
status: durable
created: 2026-08-09
updated: 2026-08-09
topic: "Plural preference across the attack model's behavioural dimensions — instrumenting strategic plurality (variety WITH purpose in the stationary policy) past the variety already banked, via the uniform-weight ablation; pre-registration + three-arm results + per-dimension verdicts"
---

# Plural preference — turning demonstrated variety into demonstrated strategic plurality, or reporting the honest boundary where it stays variety

**Status:** complete 2026-08-09. Executes and retires the
`2026-08-09_plural_preference_instrumentation` handoff. **The §Pre-register
predictions were committed (git `1da2e7a`) before the hypothesis-testing arms
ran**; §Results and §Verdicts were filled by the run that followed. A reader study
over recorded runs: the three arms simulate, but every *measure* is a re-read, and
**nothing here moves a badge** — axis 3 is DEMONSTRATED and this builds the
thesis-argument evidence its prose leans on, a superset of the badge.

**The result, up front.** The model demonstrates **plural preference — strategic
plurality as a stationary-policy property** — on **three of four** shape-certified
behavioural dimensions (realised transitions, place-visits, verb mix), CI-separated
from a topology-only null in four or five of five profiles by two independent
statistics, with the favoured subset tracking the documented-campaign success prior
(field-success alignment CI-separated in 4/5 profiles). **Terminal behaviour is a
reported negative** (P2 fired); **opening shape is withheld** (undersampled at
k = 5, P3) with its variety count intact. The boundary holds hard: this is
field-success alignment **not** substrate-success alignment (axis 7), and a
**stationary-policy property, never adaptivity**.

## The claim, and the ceiling fixed before any number exists

Axis 3 is DEMONSTRATED on **variety** —
[`plurality_reporting.md`](plurality_reporting.md) counts 2–10 distinct
five-place openings per profile where the inherited FSM admits one. Variety is
the **support** of the behaviour distribution (how many behaviours can appear).
It is only the *prerequisite* for strategic plurality: a model can be various and
strategically empty — uniform branching produces many openings and prefers none
of them. This record instruments the *positive* claim the dissertation leans on:
that the attacker favours a **mixed subset** of behaviours (the **shape of the
mass** over the support), and that the favoured subset is the field-successful
one — a plural, preferential, success-aligned mixture, contrasted with the
baseline's one deterministic rule.

**The honesty ceiling (fixed before work started, unmovable by any result).**
What is in reach is a statement about the model's **stationary policy**: it is a
success-weighted plural mixture, categorically unlike one deterministic rule.
That is **not** a claim of within-run adaptive selection — axis 4 is DESIGNED and
the verdict-blind ablation measured routing approximately free; both modulators
narrow traversal (§4 pin). Strategic plurality here = **variety with purpose in
the policy**, never dynamic strategy. Every figure and caption carries that
boundary. This record does **not** re-score axis 3; it builds the thesis-argument
evidence the badge's prose leans on, which is a superset of the badge.

## The measure — a signature that separates three regimes per dimension

For each behavioural dimension the empirical distribution is taken over runs
(pooled per profile), and three quantities are read off it
([`measures.py`](../../../../src/mtdsim/l3_simulation/movement/measures.py) §10):

- **Effective number of behaviours** `D = 2^H` (Hill number of order 1; H the
  Shannon entropy in bits). D = 1 is one behaviour; D = N is a flat distribution.
- **Evenness** `D/N` (Pielou). Below 1 is preference (mass on a subset); at 1 is
  uniform. Interpretable only for N > 1 (at N = 1 it is trivially 1.0 — the
  one-rule case reads off the support count, not the evenness).
- **Success-alignment** — the step that makes preference *strategic* rather than
  merely concentrated: whether the favoured behaviours are the successful ones.

| regime | support N | D = 2^H | evenness D/N | reading |
|---|--|--|--|--|
| baseline FSM | 1 | 1 | — | one strict rule |
| uniform variety (noise) | large | ≈ N | ≈ 1 | various, not strategic |
| **plural preference** | > 1 | 1 < D < N | < 1 | favours a mixed subset |

The measure reuses the suite's entropy the one way (the Shannon formula
`path_entropy_from_transitions` owns), `jsd`, `mean_ci` and `interval_report`; the
new §10 adds only `hill_diversity`, the per-dimension distributions, and the
alignment/Spearman readers.

### Why the current variety figure cannot carry the positive claim

Measured, not assumed (the handoff's §State-of-play, reproduced from
`expo02_ashen_lynx` at ten seeds): at the opening level `objective_exfiltration`
reads 10 distinct openings at evenness **1.00** — indistinguishable from uniform
noise, because ten draws cannot populate a distribution over openings — while the
concentrated profiles read D = 1.38 to 2.56. Where variety is high the preference
is undersampled; where preference is visible the plurality is low. Ten seeds at
the opening level prove variety and **cannot separate plural preference from
either noise or near-monostrategy**. Hence: more seeds (P3), the behaviour level
across several dimensions (not the P1-entangled step level), and the ablation.

## The five behavioural dimensions

A preference that holds across independent slices is a policy property; one on a
single slice is a suspected artefact (the P1 defence — a single hub must not
manufacture the result). Each already present in the recorded walk:

1. **opening** — the k-place opening prefix (k = 5; the variety figure's unit).
   *Per-run* (one observation per run — sparse, seed-count-sensitive).
2. **transition** — realised out-edges `place>next_place`, flat over edge types
   (the path shape). *Per-event.* Hub-sensitive, but the ablation shares the hub,
   so the *contrast* is hub-controlled.
3. **verb** — dispatched-verb mix. *Per-event.* The **one dimension with a
   baseline counterpart** (both attackers dispatch the same six verbs), so its
   plurality is comparable across arms rather than a structural zero.
4. **visit** — place-visit distribution (the L2 action-stream convention).
   *Per-event.*
5. **terminal** — terminal place. *Per-run.*

## The three arms (matched seeds; modulators null, no MTD, v2_partial, retrace)

- **baseline FSM** — the inherited 6-phase attacker. **Structural D = 1** on the
  four movement-vocabulary dimensions (it has no place vocabulary — stated the way
  `plurality_reporting.md` §2 states the entropy zero, never a measured bar); a
  real verb-mix D on dimension 3.
- **uniform-weight null** — the movement attacker with each place's
  out-distribution flattened to equiprobable over *its own reachable
  (positive-weight) destination set* (`uniform_weight_variant`,
  [`net.py`](../../../../src/mtdsim/l3_simulation/movement/net.py)). Same
  reachable graph, corpus preference stripped. The topology-only control.
- **corpus-weighted** — the shipped movement attacker, as reported.

**The gap between the corpus arm and the uniform null IS the strategic content**
(the concentration the *weights* buy, isolated from the concentration the
*topology* forces). The uniform null shares the hubs, preconditions and reachable
graph, so a corpus-vs-uniform difference is attributable to the weighting alone.

**A methodological finding from the design smoke test, disclosed for integrity
(see §Pre-register):** the direction of the gap is **dimension-dependent** — the
corpus weighting concentrates some distributions and, where uniform weights trap
the walk in a shallow reconnaissance↔initial-access cycle, *spreads* others. So
the direction-agnostic magnitude of strategic content is CI-separation +
`jsd(corpus, uniform)`; the signed evenness gap is the descriptive detail on top.

## Pre-register (committed before the hypothesis-testing arms)

**Integrity disclosure.** Before this section was committed, a *design-validation
smoke test* was run — the corpus and uniform arms on the `aggregate` profile at
≤ 30 seeds — for two purposes only: to validate the `uniform_weight_variant`
transform (support preserved, weights flattened, walk changed) and to confirm the
arms diverge at all (a study on two indistinguishable arms would be moot). It
established both, and additionally revealed that the evenness gap's *direction* is
dimension-dependent. It did **not** touch the other four profiles, the CIs, the
alignment battery or the convergence check. The predictions below are committed
before the full five-profile, P3-seeded, bootstrap-CI'd arms are run; **P1 is
recorded exactly as the handoff wrote it, not weakened**, and the substantive
battery (P1-strategic) is added rather than substituted.

- **P1 — the handoff's directional prediction, verbatim.** Corpus-weighted
  evenness < uniform-null evenness on **≥ 3 of the 5** dimensions (the attacker
  concentrates more than the graph forces); baseline D = 1 on the four
  movement-vocabulary dimensions; success-alignment correlation positive. *Tested
  and reported whichever way it lands; the smoke test suggests the evenness half
  may land below 3/5 because the direction is dimension-dependent, which is a
  reported outcome, not a massaged one.*

- **P1-strategic — the substantive, direction-agnostic battery.** A dimension
  carries strategic content iff the corpus arm is **CI-separated from the uniform
  null on evenness** (bootstrap over seeds, 2.5/97.5 percentile, disjoint) —
  *either direction*. Strategic *preference* (not merely structural difference)
  additionally requires the **corpus-weight alignment** (edge dimension, against
  the field-success prior) to be positive **and** its CI above the uniform null's.
  Committed direction: CI-separation on ≥ 3/5 dimensions, and the alignment gap
  positive.

- **P2 — kill criterion.** A dimension where the corpus and uniform evenness CIs
  **overlap** carries **no** strategic preference beyond topology — reported as a
  negative for that dimension, never massaged. A claim that survives on 1 of 5
  dimensions is a weak claim and is reported as one.

- **P3 — seed count.** Fixed by a convergence check *before* the full arms: the
  smallest N at which the per-run dimensions' D is stable across two disjoint seed
  halves (|ΔD| ≤ 0.2), on the corpus arm of the richest profile (`aggregate`). A
  per-run dimension that does **not** converge inside the budget has its
  distribution-*shape* verdict withheld (its variety *count* still stands).

- **Substrate-success honesty check (committed as a check, not a pass/fail).** The
  substrate-success alignment (verb mass vs substrate success rate) **may be
  non-positive even where the field-success alignment is positive**, because
  substrate success is not a progress signal here (axis 7: scanning succeeds far
  more than exploiting). Reported as the known limit, not the policy's failure.

## Results

Run 2026-08-09, three arms × five profiles × **100 matched seeds** (1 100 runs,
0 errors), modulators null, no MTD, v2_partial, retrace, horizon 15 000 s.

### P3 — the seed count, and one dimension withheld

The convergence check (pooled growth ladder on the corpus arm of `aggregate`,
20-seed rungs to 120) settles the seed count and, more importantly, **which
dimensions can carry a distribution-shape verdict at all**:

| dimension | N at 120 | D at 120 | evenness at 120 | last-rung ΔD / Δevenness | verdict |
|---|--:|--:|--:|--|---|
| transition | 113 | 81.98 | 0.725 | 0.181 / 0.001 | **STABLE** |
| verb | 6 | 5.40 | 0.900 | 0.002 / 0.001 | **STABLE** |
| visit | 14 | 12.25 | 0.875 | 0.005 / 0.001 | **STABLE** |
| terminal | 13 | 11.06 | 0.851 | 0.003 / 0.000 | **STABLE** (by 100) |
| opening | **72** | 43.21 | 0.600 | **5.546 / 0.028** | **DRIFTING** |

`opening`'s support is unsaturated at k = 5 (N climbs 13→25→40→50→60→72 across the
ladder; evenness slides 0.814→0.600 and is still falling), so its
distribution-*shape* verdict is **withheld per P3** — its variety *count* stands
(that is the existing `fig_opening_variety.png`). The seed count is fixed at
**100** (terminal is stable there; the per-event dimensions by 20). Changing k to
force opening to converge was refused — k = 5 is the pre-registered unit, and
re-choosing it for a result is exactly the reverse-fitting the integrity rule
bars. **The preference claim therefore rests on the four shape-certified
dimensions**, of which one (terminal) then returns a negative.

> **Disclosed operationalisation change, in the conservative direction.** P3's
> pre-registered text named "two disjoint seed halves (|ΔD| ≤ 0.2)". Implemented
> literally, that criterion **false-passes** a growing-support dimension: two
> equal-size samples of the same undersampled process always roughly agree (low
> variance), so `opening` registered a spurious first crossing at n = 18 while its
> pooled estimate kept drifting to N = 72 / D = 43 at n = 120. The honest check is
> the **pooled growth ladder** used above (stabilised = the last two rungs move
> less than |ΔD| ≤ 0.2 *and* |Δevenness| ≤ 0.02), which is **stricter**: it
> **withholds** `opening`, the one dimension the literal halves criterion would
> have (misleadingly) admitted. The change tightens the gate, never loosens it —
> which is the only direction an operationalisation may move after
> pre-registration.

### The clincher — corpus arm vs the topology-only null, per dimension

Two independent statistics, both pre-registered, agree: **evenness CI-separation**
(bootstrap over seeds, 2.5/97.5, disjoint) and **`jsd(corpus, uniform)` clearing
the within-corpus split-half noise floor**. Counted over the five profiles:

| dimension | evenness CI-separated | JSD clears floor | direction | verdict |
|---|--:|--:|---|---|
| **transition** | **5 / 5** | **5 / 5** | concentrate ×4, spread ×1 | strategic content |
| **visit** | **5 / 5** | **5 / 5** | concentrate ×4, spread ×1 | strategic content |
| **verb** | **4 / 5** | **5 / 5** | concentrate ×3, spread ×1 | strategic content |
| terminal | 0 / 5 | 1 / 5 | — | **negative (P2 fires)** |

On transition, visit and verb the corpus policy produces a realised behaviour
distribution the topology alone does not, in ≥ 4 of 5 profiles, corroborated by
both statistics. **Terminal is a reported negative** — its per-run distribution is
within seed noise of the null in four of five profiles (the fifth, `objective_
none_c2`, the sole exception), exactly the kill P2 was written to surface.

**The direction is dimension- and profile-dependent, and that is a finding, not a
wrinkle.** For four profiles the corpus weighting *concentrates* the distribution
(evenness below the null). For `objective_none_c2` it *spreads* it: under uniform
weights that profile's walk collapses into a shallow reconnaissance↔initial-access
funnel (transition evenness **0.390**), and the corpus weighting pulls it back out
(**0.768**). Both are purposeful departures from what topology forces — which is
why the load-bearing measure is the *direction-agnostic* CI-separation + JSD, and
the signed evenness gap is the descriptive detail on top.

Representative cells (corpus vs uniform evenness, 95 % bootstrap CI):

- `objective_none_c2` transition: **0.768 [0.762, 0.772]** vs 0.390 [0.354, 0.425]
  — the null funnels, the weights broaden (JSD 0.185, floor 0.002).
- `aggregate` visit: **0.874 [0.870, 0.879]** vs 0.958 [0.956, 0.960] — the weights
  concentrate the visit stream below the near-uniform null.
- `objective_exfiltration` transition: **0.689 [0.683, 0.695]** vs 0.813
  [0.808, 0.817] — concentration, cleanly separated.
- `aggregate` terminal: 0.851 [0.753, 0.915] vs 0.900 [0.792, 0.938] — overlapping,
  the negative.

### The strategic step — the favoured subset is the field-successful subset

Field-success alignment (Spearman between realised edge mass and the
documented-campaign corpus prior), corpus arm vs the null that has the prior
stripped:

| profile | corpus | uniform null | CI-separated? |
|---|--:|--:|:-:|
| objective_exfiltration | **0.517** [0.503, 0.526] | 0.294 [0.280, 0.318] | **yes** |
| objective_impact | **0.192** [0.167, 0.210] | 0.102 [0.060, 0.125] | **yes** |
| objective_exfiltration_impact | 0.223 [0.217, 0.275] | 0.217 [0.193, 0.246] | no |
| objective_none_c2 | **0.508** [0.492, 0.522] | 0.210 [0.193, 0.236] | **yes** |
| aggregate | **0.446** [0.434, 0.451] | 0.149 [0.128, 0.168] | **yes** |

In **four of five profiles** the corpus arm tracks the field-success prior
materially above the null, CI-separated — the realised behaviour follows the
documented-campaign weighting *because of the weighting*, which the null strips.
The one exception (`objective_exfiltration_impact`) is the profile with only two
distinct openings: already so concentrated that flattening the weights barely
moves where the mass lands. The contrast form sidesteps the circularity of "the
corpus arm walks the corpus weights": the null shares the topology and
preconditions and still scores far lower, so the gap is the weighting's.

### The honesty boundary — field-success, not substrate-success (axis 7)

The committed honesty check fired as predicted. Substrate-success alignment (verb
mass vs the substrate's own per-verb success rate), corpus arm: **−0.600, −0.029,
−0.029, −0.543, −0.257** across the profiles — non-positive throughout. The policy
does **not** spend its actions on the verbs that succeed *on this substrate*,
because substrate success is not a progress signal here (scanning succeeds far
more often than exploiting; axis 7). A policy aligned with *field* success reads as
*un*-aligned with *substrate* success, and that is the substrate's limitation
reported, not the policy's failure. It is also the sharpest possible statement that
this is a **corpus-derived stationary policy**, not a substrate-gaming one.

### The baseline anchor, and the one shared dimension

On the four movement-vocabulary dimensions the baseline is **structural D = 1** (it
has no place vocabulary — stated the way `plurality_reporting.md` §2 states the
entropy zero). On the one dimension it shares — the verb mix — it is a real and
telling measurement: **D = 2.199, evenness 0.366** (it funnels ~79 % of its
dispatches into `EXPLOIT_VULN`). The movement arms carry verb D ≈ 5.4 (evenness
≈ 0.90). So on the only axis where the two are commensurable, **the single-rule
baseline is far more concentrated than the plural attacker** — the "one strict
rule" regime made visible against the "plural mixture" one.

### P1 (the handoff's verbatim directional prediction) — landed mixed, as flagged

P1 predicted corpus evenness < uniform on ≥ 3/5 dimensions (the attacker
*concentrates* more than the graph forces). By point estimate it holds for four
profiles and **inverts for `objective_none_c2`** (which broadens), so the
directional half is not universal — precisely the dimension/profile dependence the
integrity disclosure flagged from the smoke test. The **substantive P1-strategic
battery passes decisively**: CI-separation on three of the four shape-certified
dimensions in ≥ 4/5 profiles, and the field-success alignment gap positive and
CI-separated in 4/5 profiles.

### Reproduction (gate 2) — the shipped arm reproduces the badge's numbers

On the overlapping seeds 0–9, the corpus arm reproduces `plurality_reporting.md`
§2: pooled path entropy 2.185 / 2.027 / 1.947 / 1.460 / 2.723 bits against the
recorded 2.195 / 2.033 / 1.972 / 1.451 / 2.714 (within ±0.03 bits, the tally-
reconstruction rounding), and distinct five-openings 10 / 9 / 2 / 4 / 7 —
**exact**. The configuration described is the configuration measured.

## Verdicts

**The model demonstrates plural preference — strategic plurality as a
stationary-policy property — on three of the four shape-certified behavioural
dimensions, and it is a property the single-rule baseline cannot represent.** On
the realised transitions, the place-visit distribution and the verb mix, the
corpus-weighted policy's behaviour distribution is CI-separated from a topology-
only null (which shares its graph, hubs and preconditions and differs only in
having the corpus preference stripped) in four or five of five profiles, by two
independent statistics. The favoured subset **is** the field-successful subset:
the corpus arm tracks the documented-campaign success prior above the null,
CI-separated, in four of five profiles. That is preference *with purpose in the
policy* — variety sharpened to plural preference — demonstrated by contrast rather
than asserted.

**Reported as negatives, whichever way they landed (gates 3–4, P2):**

- **Terminal behaviour carries no CI-separable preference** beyond topology (0/5
  profiles by evenness, 1/5 by JSD). One dimension of the five is a clean negative.
- **Opening shape is withheld** (P3): its k = 5 support does not saturate inside
  120 seeds, so its distribution-*shape* is undersampled. Its variety *count*
  stands (the existing figure); its preference is not claimed.
- **The directional prediction P1 is not universal**: the corpus weighting
  concentrates four profiles and *broadens* `objective_none_c2` out of a
  topological funnel. Both are purposeful, so the claim rests on the
  direction-agnostic separation, not the sign.

**The boundary, unmovable:**

- **This is field-success alignment, not substrate-success alignment.** The policy
  is aligned with the documented-campaign prior, and measurably *anti*-aligned with
  the substrate's own success signal (axis 7) — reported, not massaged.
- **Stationary policy, never adaptivity.** Every number here is a re-read of the
  static corpus weighting under the modulators-null configuration. Nothing measures
  within-run selection; axis 4 stays DESIGNED, this does not touch it.

**What the thesis may now claim.** That the attacker model demonstrates *strategic
plurality* in the precise sense the discussion needs: it favours a mixed,
success-weighted subset of behaviours over the baseline's one deterministic rule,
shown on multiple independent behavioural dimensions against a null that isolates
the corpus weighting from the topology, with the favoured subset tracking the
field-success prior. The variety-as-prerequisite framing of
`plurality_reporting.md` §6 is discharged: the prerequisite (variety) was banked;
the positive property (plural preference over it) is now measured. **No badge
moves** — axis 3 is DEMONSTRATED and this re-scores nothing; it builds the
thesis-argument evidence axis 3's prose leans on.

**What stays future work / may not be claimed.** That the attacker *chooses* among
the plural options within a run (that is adaptive selection — axis 4, measured
approximately free), that it games substrate success, or that plural preference
holds on the opening or terminal dimensions (undersampled and null respectively).
The claim is variety with purpose in the *policy*, and it stops exactly there.

## Figures

Both from `plural_preference_figs.py`, deterministic from `pp_results.json`
(itself deterministic from `pp_runs.jsonl`); conditions carried in each figure;
diagnostic house style (no accentuation, shape + grey shade, greyscale/CVD-safe).

- **`fig_preference_signature.png`** — the clincher. Per shape-certified dimension,
  corpus vs uniform-null evenness with 95 % bootstrap CIs across the five profiles.
  The CI gaps on transition/verb/visit and the overlap on terminal are read
  directly; `objective_none_c2`'s transition (null 0.39 → corpus 0.77) is the
  broadening case in plain view.
- **`fig_success_alignment.png`** — the strategic step and its boundary. Left: the
  field-success alignment, corpus above the null. Right: the substrate-success
  alignment, negative.

## Reproduction

```
PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_run.py --mode convergence --max-seeds 120
PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_run.py --mode arms --seeds 100
PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_analyse.py
PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_figs.py
```

The runner persists per-run summaries to `pp_runs.jsonl` and `pp_convergence.json`
(untracked); the analyser emits `pp_results.json`; the figure script reads that and
writes the two PNGs — all deterministic (SIM-05). The four scripts are committed
(the plurality-workspace gitignore exception); their outputs stay untracked.

The measure lives in
[`measures.py`](../../../../src/mtdsim/l3_simulation/movement/measures.py) §10
(`hill_diversity`, the per-dimension distributions, `corpus_weight_alignment`,
`substrate_success_alignment`, `spearman_rho`) and the ablation in
[`net.py`](../../../../src/mtdsim/l3_simulation/movement/net.py)
(`uniform_weight_variant`), selected by `run_movement(..., uniform_weights=True)`;
all covered by `tests/l3_simulation/test_movement_net.py` and
`test_movement_measures.py`.
