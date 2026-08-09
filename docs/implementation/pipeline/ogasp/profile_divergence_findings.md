---
status: findings
created: 2026-08-09
topic: "Attack-profile divergence, first corpus run — the profile_divergence measure clears its new execution-level null on every between-class pair, and the pre-registered size kill-criterion fires on the divergence-to-aggregate column (Spearman ρ = −1.0), so that column may not be read as objective conditioning"
---

# Attack-profile divergence on a recorded corpus — the measure works, and its `aggregate` column is a flow-share re-expression

**Pre-registration:**
[`profile_divergence_prereg.md`](profile_divergence_prereg.md), committed
(`67dee5f`) before the instrument or any output existed. **Workspace:**
`data/results/profile_divergence/` (`run_study.py` → `runs.jsonl`, 500 runs;
`analyse.py` → `verdicts.json` / `verdict.txt`). All divergence maths is the
shipped suite's (`measures.py` §2); the analysis re-slices by re-invocation
(`--condition`, `--profiles`, `--reference`, `--n-splits`, `--seed`, `--q`), so
a re-drawn corpus or a different slicing reruns in one command.

This is **arms 1–2 of the objective-conditioning ablation**
([`../../handoffs/2026-08-09_objective_conditioning_ablation.md`](../../handoffs/2026-08-09_objective_conditioning_ablation.md)):
the four classes and `aggregate`, measured, with the null band the measure had
never had. The size-matched label-blind control (arm 3) has not run; **no badge
moved, in either direction**, per the pre-registration.

## 1. Corpus

Five profiles × 50 seeds × two conditions (`no_mtd`, primary; `random_200`, the
operating scheme/interval), `v2_partial`, synthetic overlay on, retrace on,
horizon 15 000 s. Every run in every cell terminates at the horizon and none
reaches the objective (degenerate region, as expected), so every figure below is
breadth- or distribution-shaped. Determinism: the corpus was recorded twice
(once before a serialisation fix to the final record's `next_place`, once
after); every divergence figure reproduced exactly.

## 2. The null band (new; closes the suite's recorded blind spot)

`split_half_divergence_null` (`measures.py` §2): within-profile JSD between
random 25/25 half-splits of a profile's 50 runs, 200 seeded draws; a
between-profile figure clears the null when it exceeds the 97.5th percentile of
the pair's pooled draws. On this corpus the **visit-stream** null ceilings are
0.0007–0.0022 — pooled visit distributions at 25 runs are very tight — while the
**terminal-tactic** ceilings are 0.27–0.40: one terminal place per run and 50
runs per profile leaves that half noise-dominated at this sample size.

## 3. Findings against the pre-registered conclusions

**P1 — HELD, decisively.** All six between-class visit-stream JSDs clear the
null, by 40–110×: 0.081 (`objective_exfiltration_impact` ↔ `objective_impact`)
to 0.237 (`objective_exfiltration_impact` ↔ `objective_none_c2`) against
ceilings ≤ 0.0022. Profile identity conditions the runtime visit distribution
far above seed noise — axis 2's stronger-claim measurement, now on a corpus
rather than only in the validation harness.

**P2 — HELD.** Every class clears the null against `aggregate`:
`objective_exfiltration` 0.0234, `objective_impact` 0.0648,
`objective_exfiltration_impact` 0.0674, `objective_none_c2` 0.1221. No class is
behaviourally indistinguishable from the unpartitioned attacker at this sample
size. **Read this only through P3 below.**

**P3 — the kill criterion FIRED.** Spearman ρ between a class's
JSD-to-`aggregate` and its flow count is **exactly −1.0** in both conditions:
19 flows → 0.0234, 8 → 0.0648, 6 → 0.0674, 5 → 0.1221. The mechanism is
arithmetic, not behavioural: `aggregate` is the flow union, so a class holding
more of the union's flows contributes more of the union's routing mass, and
"distance from the union" is largely "share of the union". At n = 4 the
statistic is coarse (a perfect monotone ordering has probability 1/12 under a
random null), but the direction is the handoff's predicted confound and the
pre-registered consequence applies as written: **the divergence-to-`aggregate`
column may not be interpreted as behavioural objective-conditioning anywhere
downstream.** In particular, the reading "low divergence from the unsegregated
net ⇒ ablate the partition" is blocked on this instrument: a class can sit
close to `aggregate` merely by being large. The size-matched label-blind
control arm remains the only instrument that can separate conditioning from
corpus size, exactly as the handoff argued.

**P4 — terminal half reported, not gated.** Two of ten pairs clear in `no_mtd`
(`objective_exfiltration` ↔ `objective_impact`, 0.348 > 0.303;
`objective_exfiltration` ↔ `objective_none_c2`, 0.360 > 0.299); the
`aggregate` pairs all sit inside their null. At 50 terminal draws per profile
the half is underpowered, and any future claim on it needs a larger corpus, not
a smaller ceiling.

## 4. Two side observations, recorded rather than pursued

- **The divergence structure is MTD-invariant.** Every visit-stream figure
  moves by ≤ 0.013 between `no_mtd` and `random_200` (e.g. 0.0234 → 0.0215;
  0.2373 → 0.2426). What a profile visits is set by the profile, not by the
  defence's churn — consistent with the interrupt reaching routing as an
  ordinary failure verdict rather than as structure.
- **The free pre-check's breadth ordering did not reproduce under these
  conditions.** The progress-credit sweep's `v2_partial` no-MTD column had
  `aggregate` top (6.14 distinct hosts) and `objective_exfiltration_impact`
  bottom (1.96); this corpus (retrace **on**, no attacker state) has
  `objective_exfiltration_impact` top on the mean (6.80 ± 0.89) with
  `aggregate` at 6.00 ± 0.43, and `ordering_supported` is False in both
  conditions — adjacent CIs overlap throughout. The two corpora differ in
  configuration (that sweep ran its own arms), so this is a condition
  dependence to note, not a contradiction to resolve; it does further caution
  against leaning on the pre-check's single cell.

## 5. Validation gates

Readers only; no mechanism, no declared value. Full `tests/` suite: 819 passed,
240 skipped (the standing skips), zero failures. Shipped artefacts
byte-identical (`git status`: no tracked file outside the session's own
changes). Determinism exact (§1). Aggregates through `interval_report`;
`ordering_supported` reported wherever an ordering could have been claimed, and
it is False for the outcome half, so no ordering is claimed.

## 6. What this leaves open

The badge question is untouched by design. A2 (classes separate from
`aggregate` on an **outcome** measure with disjoint CIs) is not established
here — distinct-host CIs overlap at 50 seeds. A3 (classes separate from
size-matched label-blind draws) is the deciding arm and still needs its
scratch-net build (handoff § Recommended approach). When that study runs, its
behavioural half should be read through `divergence_report` unchanged, and its
class-versus-control figures judged against the same split-half null — the
instrument this study leaves behind.
