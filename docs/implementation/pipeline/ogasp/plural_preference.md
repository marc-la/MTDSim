---
status: open
created: 2026-08-09
updated: 2026-08-09
topic: "Plural preference across the attack model's behavioural dimensions — instrumenting strategic plurality (variety WITH purpose in the stationary policy) past the variety already banked, via the uniform-weight ablation; pre-registration + three-arm results + per-dimension verdicts"
---

# Plural preference — turning demonstrated variety into demonstrated strategic plurality, or reporting the honest boundary where it stays variety

**Status:** open — **pre-registration committed 2026-08-09 before the
hypothesis-testing arms ran** (this section and §Pre-register are the committed
predictions; §Results and §Verdicts are filled by the run that follows). Executes
the `2026-08-09_plural_preference_instrumentation` handoff. A reader study over
recorded runs: the arms simulate, but every *measure* is a re-read, and nothing
here moves a badge.

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

**PENDING** — filled by the run that follows this commit (P3 convergence, then the
three arms, then the measure table, the per-dimension CI-separation battery, the
alignment gaps, and the reproduction of `plurality_reporting.md` §2 where they
overlap).

## Verdicts

**PENDING** — the per-dimension clincher (CI-separated or not, and which way),
whether the model demonstrates plural preference or only variety, on how many
dimensions, and the ruling on what the thesis may claim.

## Reproduction

```
PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_run.py --mode convergence
PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_run.py --mode arms --seeds <P3>
PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_analyse.py
```

The runner persists per-run summaries to `pp_runs.jsonl` (untracked); the analyser
reads them and emits `pp_results.json` + the figures deterministically. Scripts are
committed (the plurality-workspace gitignore exception); outputs stay untracked.
