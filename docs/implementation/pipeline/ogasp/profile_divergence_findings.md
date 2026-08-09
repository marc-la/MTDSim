---
status: findings
created: 2026-08-09
updated: 2026-08-09
topic: "Attack-profile divergence, first corpus run — the profile_divergence measure clears its new execution-level null on every between-class pair, and the pre-registered size kill-criterion fires on the divergence-to-aggregate column (Spearman ρ = −1.0), so that column may not be read as objective conditioning. §7 decomposes what carries the divergence: the objective band leads, the invariant early-lifecycle prefix carries least"
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

## 5a. The metric, refined to its reporting form

**Null-relative attack-profile divergence**: the pairwise visit-stream JSD (L2
convention) reported against the within-profile split-half null. The null gives
the number its meaning — a JSD of 0.1 says nothing until the reader knows the
same profile compared with itself across seeds sits at 0.0003–0.0005 (median)
with a 97.5th-percentile ceiling under 0.003. In that form the result is one
sentence: **every pair of objective profiles diverges by at least 53× the
seed-noise ceiling** (worst pair `objective_exfiltration` ↔
`objective_none_c2`, 0.111 against 0.0021; best 152×), and 32× when the
`aggregate` pairs are included.

The headline figure is `fig6_divergence_ranked.png`
(`data/misc/_viz/profile_divergence/headline_viz.py`): the ten between-profile
figures as ranked dots on a log axis, against the shaded **seed-noise band**
(split-half medians to the 97.5th-percentile ceiling) every dot must clear.
The form is redundancy-free — a symmetric matrix states each figure twice and
spends its diagonal restating the null five times, so the matrix
(`fig5_divergence_matrix.png`) is kept as the pairwise-lookup companion, not
the argument. Class pairs carry the headline; the `aggregate` pairs are drawn
muted and never summarised, per §3's kill.

Two calibration anchors travel with the number. **What overlap scores:** two
profiles with genuinely the same behaviour score inside the band —
≤ 0.003 — because the band *is* five same-behaviour comparisons (each profile
against itself across seeds). **What the magnitude means:** JSD *x* is a
difference as large as if fraction *x* of one profile's activity happened at
tactics the other never visits — an equivalence reading, exact for disjoint
mass and conservative for shared-tactic proportion shifts. The observed
0.08–0.24 band therefore says the classes remain mostly overlapping (the
invariant lifecycle prefix) while differing far beyond noise on what they are
for — which is §6's decomposition in one number.

## 6. What behaviour carries the divergence, and how it traces to construction

Decomposition: `behaviour.py` in the workspace (per-tactic visit portraits,
per-tactic JSD contributions, objective-band alignment; tables printed and
`behaviour.json` written). Figures:
`data/misc/_viz/profile_divergence/` (`behaviour_viz.py`; fig1 visit-portrait
heatmap, fig2 divergence carriers, fig3 objective-band engagement, fig4
terminal-tactic heatmap). Primary condition throughout; the portraits are
near-identical under `random_200`, per §4's MTD-invariance.

**The divergence is concentrated exactly where the partition was drawn.**
Averaged over the six class pairs, the largest per-tactic JSD contributions are
the objective band itself — `impact` (37 × 10⁻³) and `exfiltration`
(20 × 10⁻³) — followed by the enabling tactics that differ per objective,
`credential-access` (19.6) and `lateral-movement` (15.7). The smallest are the
lifecycle's invariant prefix: `initial-access` (1.6), `execution` (2.7),
`reconnaissance` (3.3). This is an execution-level echo of the structure the
partition was built from — Alshamrani's lifecycle holds its early stages
invariant and conditions its suffix on the objective, and the runtime walks
reproduce that shape: profiles agree on how campaigns start and diverge on what
they are for.

**Construction reaches behaviour twice over.** First structurally: a class's
net omits the objective places foreign to its label
(`objective_impact` has no `exfiltration` place, `objective_none_c2` neither
`exfiltration` nor `impact`, `objective_exfiltration_impact` no
`defense-impairment`), so those cells are exact behavioural zeros — behaviour
the unpartitioned attacker cannot exhibit, since `aggregate` routes everything
(5.0 % / 5.3 % on exfiltration/impact). Second by weight: within the shared
places, each class leans toward its own objective's enabling tactics —
portraits below.

- **`objective_exfiltration`** — a staging campaign: the highest
  `credential-access` (12.2 %) and `collection` (8.0 %) shares, 7.0 % on
  `exfiltration` itself, and near-nothing on `impact` (0.5 %) though the place
  is present — the one profile whose objective restraint is behavioural rather
  than structural.
- **`objective_impact`** — disruption-shaped: highest `command-and-control`
  (19.9 %) and `defense-impairment` (3.3 %), 10.6 % on `impact`, and almost no
  staging (`collection` 1.2 %, `credential-access` 3.7 %).
- **`objective_exfiltration_impact`** — escalate-and-detonate: highest
  `discovery` (18.8 %), `privilege-escalation` (8.4 %) and `impact` (13.9 %),
  lowest `credential-access` (1.2 %), both objectives engaged.
- **`objective_none_c2`** — the behavioural outlier: 23.6 % `lateral-movement`
  (three times any other profile), the most visits per run (680 against
  467–505), the least dwell-only time (15.1 % against 38–44 %) and the most
  blocked actions (30.1 %) — a fast, noisy positioning attacker, which is the
  same composition the stealth spacing diagnostic identified as its inversion
  case. One honest caveat: its *nominal* objective tactic,
  `command-and-control`, is connective tissue every profile visits heavily
  (10–20 %), and its own share (14.2 %) is not the highest — this class's
  fingerprint is structural absence plus tempo, not C2 share.
- **`aggregate`** sits near the flow-weighted middle of every column — the
  visual restatement of §3's mixture confound.

**Termination tactic correlates with construction, under the horizon caveat.**
All runs are horizon-terminated, so a terminal place is where the walk spends
its late time, not a chosen stop. Read that way: each class's terminal mass
lands in or beside its own objective band — `objective_impact` ends 16 % of
runs at `impact` (against 0 % for every class whose net lacks it),
`objective_exfiltration` ends 22 % at `collection`+`exfiltration` (others
0–4 %), `objective_none_c2` ends 28 % at `lateral-movement` — and no class can
terminate on a place its construction omitted. The terminal-half JSD's failure
to clear its null (§3 P4) is a power statement, not an absence of structure:
the structure is visible in the heatmap and consistent with the visit half,
but one terminal draw per run at 50 runs cannot separate it from noise.

## 7. What this leaves open

The badge question is untouched by design. A2 (classes separate from
`aggregate` on an **outcome** measure with disjoint CIs) is not established
here — distinct-host CIs overlap at 50 seeds. A3 (classes separate from
size-matched label-blind draws) is the deciding arm and still needs its
scratch-net build (handoff § Recommended approach). When that study runs, its
behavioural half should be read through `divergence_report` unchanged, and its
class-versus-control figures judged against the same split-half null — the
instrument this study leaves behind.
