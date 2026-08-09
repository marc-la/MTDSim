# Plurality reporting — the nulls reconciled, the kill criterion fired, and the one figure that survived

**Status:** closed 2026-08-09. Executes and retires the
`2026-08-09_strategic_plurality_reporting` handoff. Readers only: nothing here
simulated anything; every number is a re-read of recorded runs.

**The ruling, up front.**

- **(a) The badge's numbers are a table** (§2, first block) — five profiles ×
  (pooled entropy, distinct openings), the baseline as a structural zero. No
  chart; five numbers do not earn one.
- **(b) The profile × mechanism interaction is the figure** —
  `data/misc/_viz/plurality/fig_interaction_rank.png`, drawn from experiment
  2's recorded runs by the committed `plurality_figs.py`. It reproduces the
  recorded verdict exactly (4 of 5 rankings distinct at 200 s, 5 of 5 at
  2 000 s) and it is the demonstrative form of the badge's stronger half.
- **(c) The six-family narrowing fan is NOT drawn.** The pre-registered kill
  criterion P1 **fired**: Spearman ρ = **−0.967** between pooled path entropy
  and maximum single-place visit share across the figure's own 30 cells,
  against a pre-committed |ρ| < 0.90 bar. An entropy fan here would be a
  hub-occupancy chart wearing an entropy axis. The narrowing family is
  reported as the table in §3, and the firing itself is the finding (§4).

The reported-configuration pin holds: the badge's evidence is the
modulators-null arm, and nothing below re-scores axis 3 or any other row. The
honest limit travels with every number here: **variety, not strategy**.

## 1. The reconciliation — every quoted null reproduces, and none of them were comparable

The handoff's blocker was that six sweeps quote six nulls at what looked like
three poolings. Read off the sweep scripts and recomputed from the recorded
runs (`data/misc/_viz/plurality/reconcile.py`, output
`reconciliation.json`), the spread resolves completely: **every quoted number
reproduces under its own record's convention**, and the conventions differ in
*four* independent respects — pooling level, MTD-condition pooling, sink
policy, and the statistic itself.

| quoted null (record) | reproduced | its actual construction | sink policy | script |
|---|---|---|---|---|
| 1.451–2.714 bits, 2–10 openings (experiment 2 §12) | **exact** (1.451 `objective_none_c2` … 2.714 `aggregate`; prefixes 2, 4, 7, 9, 10) | per-profile pooled transitions, movement arm, no MTD, 10 seeds, v2_partial; identical under both interval labels — no-MTD runs never read the interval | retrace | `expo02_ashen_lynx/run_experiment.py` |
| 2.23 → 0.24 / 1.45 → 0.01 (incentive_rationality C3 §6.2) | **exact** (2.232 → 0.244; 1.452 → 0.012) | per-profile pooled transitions, **both MTD conditions pooled**, v2_partial. (C3's *criterion* used mean per-run entropy — 1.553 → 0.242 / 1.427 → 0.011 — the §6.2 prose quotes the pooled form) | censor | `axis6_rationality/run_sweep.py` |
| 2.724 → 1.610 / 1.448 → 0.220 (learning_capability §7.5 L4) | **exact** | per-profile × mapping pooled transitions, κ ladder at ρ = 0.5, no MTD | censor | `axis7_learning/run_sweep.py` |
| 2.712 → 1.112 (factor 8, A4) | **exact** | pooled across **5 profiles × all 8 defence conditions**, v2_partial | retrace | `fsm_alignment/run_sweep.py` |
| 2.714 → 1.682 (factor 9, B4) | **exact** | same construction as factor 8 | retrace | `fsm_succession/run_sweep.py` |
| 2.613 null; 0.655 declared; 1.008 change B at λ = 4 (iterated_cost) | **exact** | pooled across profiles, **both MTD conditions pooled**, v2_partial | censor | `iterated_cost/run_sweep.py` |

**The 2.714 double appearance is a numerical coincidence.** Experiment 2's
2.714 is `aggregate`'s per-profile pooled entropy (no MTD, retrace); factor
9's 2.714 is pooled across all profiles *and* all defence conditions
(retrace). Different constructions, same three decimals. Related but not the
same number: the iterated-cost/censor `aggregate` cell also lands on 2.714.

**Null identity, tested exactly.** Pooled per-profile transition *tallies* at
each family's zero point, compared for dict equality within each sink-policy
group:

- `iterated_cost` λ = 0 **is bit-identical** to experiment 2's censor-policy
  no-MTD sub-study — same walks, same code state.
- Every other pair differs: utility and learner nulls are *near* the
  iterated/experiment-2 tallies (per-profile entropies within ±0.06 bits) but
  not identical; alignment and succession likewise sit within ±0.03 bits of
  experiment 2's retrace cells without matching them. Each family's null is
  internally exact (its ablation criterion held at run time); across
  workspaces the shipped model drifted between run dates. **The families were
  never swept on literally common ground**, and the composite chart the
  handoff contemplated could not have cleared the comparability bar even
  before P1 killed it.
- The sink-policy gap is profile-localised, exactly as the E6 record predicts:
  retrace vs censor differ materially only where sinking is common —
  `objective_exfiltration_impact` reads 1.972 (retrace) against 1.699
  (censor); the other four profiles are near-unchanged.

## 2. The badge's numbers, as the table the handoff ruled they should be

Experiment 2, movement arm (modulators null), v2_partial, no MTD, sink policy
retrace, 10 seeds, horizon 15 000 s. Pooled path entropy is visit-weighted
Shannon entropy of the realised out-transitions — the walk taken, not the
declared branching.

| attacker | pooled path entropy (bits) | distinct 5-place openings / 10 seeds |
|---|--:|--:|
| inherited baseline FSM | **0 (structural)** — a deterministic scripted order admits exactly one out-transition per state | **1 (structural)** |
| `objective_exfiltration` | 2.195 | 10 |
| `objective_impact` | 2.033 | 9 |
| `objective_exfiltration_impact` | 1.972 | 2 |
| `objective_none_c2` | 1.451 | 4 |
| `aggregate` | 2.714 | 7 |

The baseline row is a **structural zero, not a measurement** — the baseline
arm has no place vocabulary and path entropy is a movement-arm measure
(measurement suite §(d) keeps it out of the cross-arm subset). It is stated
the way `EventWiseComparable` states `blocked_fraction = 0.0`: the zero and
its reason, never a bar beside measured values.

## 3. The narrowing family — reported as a table, per P1

Common-ground re-read: v2_partial, **no MTD only**, seeds 0–9, pooled
transitions across the five profiles. Sink policy is the one each family ran
under and is not unifiable by re-reading (censor truncates the walk), so the
two groups are stated apart. x is position in each family's declared band,
normalised to [0, 1].

| family (declared dial) | policy | null (x = 0) | x = 0.25 | x = 1 (band end) | hub share, null → end |
|---|---|--:|--:|--:|--:|
| utility λ (axis 6, shipped) | censor | 2.575 | 1.881 | 0.678 | 0.16 → 0.46 |
| learner κ (axis 7) | censor | 2.614 | 2.271 | 1.242 | 0.15 → 0.22 |
| iterated cost, change A (λ) | censor | 2.621 | 1.715 | 0.315 | 0.15 → 0.49 |
| iterated cost, change B (λ) | censor | 2.621 | 2.194 | 0.999 | 0.15 → 0.40 |
| alignment α (factor 8) | retrace | 2.707 | 2.695 | 0.876 | 0.14 → 0.34 |
| succession α (factor 9) | retrace | 2.708 | 2.728 | 1.772 | 0.14 → 0.21 |

**P2, held as committed:** every family narrows from its own null — including
change B, whose recorded "rise" is *relative to the declared arm at matched
λ* (0.999 against 0.655–0.659 at the band end), never absolute. Five dials
buy their capability from plurality at steep dose–response rates; the
numerator repair (B) pays roughly a third of the shipped family's price. The
composition result stands as recorded: learner × utility is sub-additive
(modulator_composition.md §5).

## 4. P1 fired, and the firing is the finding

Pre-registered before any figure existed: the entropy curve must not be a
re-expression of visit concentration at the busiest place — Spearman |ρ|
between pooled path entropy and maximum single-place visit share below 0.90,
across the figure's own cells, at the threshold the exposure and
disengagement studies used.

Computed across the 30 family × sweep-point cells above (cell-level — the
granularity the figure would have plotted): **ρ = −0.967. Fired decisively.**

What it means, stated within what was measured: across every declared dial
this project has built, **the entropy collapse and the rise of the modal
place's visit share are rank-wise almost the same axis**. Narrowing is not a
redistribution among alternatives — it is a funnelling of the walk onto the
dominant place. The recorded hub-domination blind spot (measurement_suite
§(b)) is therefore not a hypothetical for this family of results: an entropy
fan would have been a hub-occupancy fan, and it is not drawn. The narrowing
family's evidential content survives in §3's table, which now carries the hub
share beside the entropy so the coupling is visible rather than hidden.

## 5. The figure that was drawn

`fig_interaction_rank.png` (script `plurality_figs.py`, deterministic from
`expo02_ashen_lynx/runs.jsonl`): within each profile, the seven defence
conditions ranked by breadth suppression (1 = fewest mean distinct hosts),
one panel per mutation interval, rank annotated in every cell over a single
grey ramp. **4 of 5 rankings distinct at 200 s; 5 of 5 at 2 000 s** —
reproducing §12's verdict from the raw rows. The reader sees non-constant
columns directly: which defence works best depends on which attacker profile
is asked. Conditions are carried in the figure itself (movement arm,
modulators null, v2_partial, retrace, 10 seeds, horizon 15 000 s).

This figure evidences the badge's interaction half. The §3 table evidences
the criterion's §(b) census claim — that the rows are an inventory, not a
scale, because capability dials measurably lower this row. Neither moves any
badge.

## 6. Discussion point — emergent strategic conditioning (for the dissertation's discussion chapter)

Recorded here so the chapter-placement pass finds it shaped; wording is
constrained by three measured results.

The claim the evidence *licenses*: the movement layer's plurality is
**emergent from the weighted transition structure alone** — the corpus-derived
out-transition weights, realised as branching, produce campaign variety
(§2) that a scripted FSM structurally cannot, and that variety is
consequential: it changes which defence ranks best (§5). The conditioning
dynamics — success/failure routing, utility, learning, alignment —
demonstrably *reshape* that distribution, with lawful dose–response curves
across four independent declared dials (§3).

The claim the evidence *bars*: that the dynamics amount to emergent
**strategy**. Three results close that door. (1) The badge's reported
configuration is modulators-null — the headline plurality contains no
dynamics by construction (model_scope_freeze §4). (2) The axis-4 ablation
showed verdict-conditioned routing to be approximately free across 1 600
paired runs — the signal operates without changing outcomes. (3) P1's firing
(§4) shows what the dials actually do to the traversal distribution:
concentrate it onto the modal place. Conditioning, as built, is
**convergence, not choice** — it narrows toward a dominant tactic rather
than selecting among alternatives.

The honest dissertation sentence is therefore shaped like: *plurality is
emergent; strategy is not — the model's conditioning mechanisms trade
plurality for their capability, and the one measured exception (the
benefit-through-the-net repair, change B) shows the trade is an instrument
choice rather than a law*. That framing converts three measured negatives
into the discussion chapter's contribution: a census instrument on which a
model can raise one row only by lowering another, demonstrated on its own
attacker.

## 7. Reproduction drift, flagged not fixed

Re-running `expo02_ashen_lynx/analyse.py` today reports E3 **MOVED** with
0.000-bit entropies for four profiles — contradicting its own recorded
verdict. Cause: the runs carry the pre-2026-08-06 profile labels
(`pure_steal`, …) and the script's `PROFILES` tuple was edited to the new
names after the run, so four selections are empty. The same post-hoc renaming
appears in `axis6_rationality/analyse.py` and both `fsm_*/run_sweep.py`
constants. This is the axis-5 §7 trap verbatim — a script drifting onto
changed labels silently redraws a study's numbers — and it is why
`reconcile.py` and `plurality_figs.py` normalise labels read off the corpus
and refuse empty cells. Fixing the workspace scripts is out of this
handoff's scope; flagged for a disposition.

## 8. Regeneration

```
PYTHONPATH=src python data/misc/_viz/plurality/reconcile.py       # table + P1
PYTHONPATH=src python data/misc/_viz/plurality/plurality_figs.py  # the figure
```

Both read recorded `runs.jsonl` files only; both are committed (narrow
`.gitignore` exception for `data/misc/_viz/plurality/*.py` — outputs stay
untracked, per the workspace convention).
