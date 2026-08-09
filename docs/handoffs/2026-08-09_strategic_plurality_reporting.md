---
status: open
created: 2026-08-09
---

# Reconcile the path-entropy nulls, then draw the one figure axis 3's evidence actually needs — the trade-off surface, not the badge

## The question this answers

Axis 3 is DEMONSTRATED and its numbers are on record. What is *not* settled is how
those numbers should be presented: a chart, a table, or nothing beyond the prose
that already carries them. This handoff answers that, and it finds a prerequisite
that has to be discharged first.

**The short version.** The badge's own evidence does not want a chart — it is five
numbers and a count, and a table states it better. The chart-worthy result is a
different one: **every declared modulator this project has built narrows traversal,
except one, and the exception is the numerator change.** That is a dose–response
family across six sweeps, it is the visible form of the criterion's most-argued and
least-shown claim, and it belongs to §(b) of the criterion rather than to axis 3's
row. **But it cannot be drawn yet**, because the six sweeps report six different
nulls at three different poolings (§2).

## State of play

**The badge and its evidence.** Axis 3 moved DESIGNED → DEMONSTRATED on 2026-07-29
against a criterion pre-registered before the run existed
([`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
§12), on both halves: pooled path entropy **1.451–2.714 bits** across the five
profiles with **2–10 distinct five-place opening sequences** over ten seeds; and a
profile × mechanism interaction — the ranking of defence conditions by breadth
suppression is not the same for every profile (**4 of 5 distinct at 200 s, 5 of 5
at 2 000 s**). The honest limit travels with it: **variety, not strategy**. The
branching is drawn from static corpus proportions; no decision rule selects among
options.

**The measures are built and have been run repeatedly.** `path_entropy`,
`path_entropy_from_transitions`, `distinct_sequences`, `distinct_prefixes`,
`place_sequence` in [`measures.py`](../../src/mtdsim/l3_simulation/movement/measures.py)
§2. Unlike axes 2 and 4, nothing here is unrun — axis 3's problem is presentation,
not instrumentation.

**The recorded blind spots, which bear directly on any chart.**
[`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
§(b): `path_entropy` **pools places, and a single high-traffic hub can dominate**;
whole sequences are seed-sensitive, so cross-seed claims should use prefixes. A
chart of entropy that is really a chart of hub occupancy would be the axis-5
failure repeated, and §4 below gives it a kill criterion.

**The narrowing family — six independent sweeps, and this is the substance.**

| declared family | null → limit (bits) | source |
|---|---|---|
| axis 6 utility λ | 2.23 → 0.24 (`pure_steal`); 1.45 → 0.01 (`infrastructure_setup`) | [`incentive_rationality.md`](../implementation/pipeline/ogasp/incentive_rationality.md) C3 |
| axis 7 learner κ | 2.724 → 1.610 (`v1`/`aggregate`); 1.448 → 0.220 (`v2`/`infrastructure_setup`) — falls in **all ten** profile × mapping cells | [`learning_capability.md`](../implementation/pipeline/ogasp/learning_capability.md) §7.5 (L4) |
| factor 8 — alignment | 2.712 → 1.112 at α = 1; cheap over ¾ of the band (0.16), expensive in the last quarter (1.44) | [`modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md) |
| factor 9 — FSM succession | 2.714 → 1.682 at α = 1; materially gentler than factor 8 | [`modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md) |
| iterated cost, change A | falls against the declared arm in **5 of 5** profiles, 0.06–0.31 bits | [`iterated_cost_model.md`](../implementation/pipeline/ogasp/iterated_cost_model.md) |
| **iterated cost, change B** | **rises** 0.05–0.46 bits, 5 of 5, both mappings; holds **1.008** at λ = 4 where the shipped model holds **0.655** | [`iterated_cost_model.md`](../implementation/pipeline/ogasp/iterated_cost_model.md) |
| composition (learner × utility) | **sub-additive**, not compounding — the two pull opposite ways on the same edges | [`modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md) §5 |

Five narrow, one widens, and composition does not compound. That is a result with a
shape, and shape is what a chart is for.

## 1. Which result is ideal — the answer, with reasons

**Three candidate results, and they are not interchangeable.**

**(a) The badge's entropy range and opening counts. Report as a table; do not
chart it.** It is five profiles × two quantities. A bar chart of five numbers
spends a figure to say what a row of a table says better, and the criterion's own
discipline — no ordering claim without disjoint intervals — is expressible in a
table (mean ± CI, separated pairs marked) and awkward in bars. This is the axis's
badge evidence and it is already adequately carried by prose plus a table.

**(b) The profile × mechanism interaction. This is chart-shaped, and it is the
badge's stronger half.** Five profiles × eight defence conditions, cells carrying
rank (or breadth suppression). The finding *is* that the columns are not constant,
and a rank heatmap states that without a summary statistic — the reader sees
non-constant columns directly. It is the natural second figure and it evidences the
badge, which (c) does not.

**(c) The narrowing family. This is the ideal figure, and it does not belong to
axis 3's row.** Entropy against each family's normalised declared parameter, one
line per family, all sharing the null at the left: five lines fanning down, one
rising. It is the only visible form of the criterion §(b) claim that *the rows are
a census, not a scale* — that a model can raise one row by lowering another — which
is currently the most-argued and least-shown statement in the instrument. It also
carries the iterated model's unlooked-for result, that **half the collapse
attributed to cost-sensitivity was the price of measuring value in the wrong
graph**, which is a methodological finding about instrument design and squarely
thesis material.

**Recommendation: build (c) as the primary figure and (b) as the secondary, and
leave (a) as a table.** State in the record that (c) evidences the criterion's
census claim and **not** axis 3's badge — it measures what the *other* axes cost
this one. Filing it under axis 3 would be a category error, and the criterion's own
§(b) is where it lands.

## 2. The prerequisite — the nulls do not agree, and one number appears twice

**This is the blocker, and it is why this handoff leads with reconciliation rather
than with drawing.** Every entropy figure above is quoted at a different pooling
and under different conditions:

| quoted null | what it actually is |
|---|---|
| 1.451–2.714 | the **range across five profiles**, each pooled over seeds (experiment 2 §12) |
| 2.23 / 1.45 | **per profile** at λ = 0 (`pure_steal` / `infrastructure_setup`), axis 6 |
| 2.724 / 1.448 | **per profile × mapping** at κ = 0, ρ = 0.5, no MTD, axis 7 |
| 2.613 | **pooled across profiles**, `v2_partial`, λ = 0, iterated cost |
| 2.712 / 2.714 | "pooled" at α = 0, factors 8 and 9 |

Three different poolings, at least two mappings, and MTD conditions that are stated
in some records and not others. Worse: **2.714 appears as both experiment 2's
per-profile upper bound and factor 9's "pooled" null**, which is either a
coincidence or a sign that "pooled" does not mean the same thing in the two
records. A composite chart superimposing these lines would be drawing six
incomparable baselines on one axis and inviting exactly the misreading that
`interval_report` exists to prevent.

**So the first job is a reconciliation table**, not a figure: for each sweep, the
pooling level, mapping, MTD condition, seed count, ρ/κ setting and the null it
reports, derived from the sweep scripts rather than from the prose that quotes
them. Uniform conditions across families is the comparability bar this project
already applies to multi-instance viz; a composite chart cannot clear it by
assertion.

**Two outcomes, and both are publishable.**

- **The nulls reconcile** (or can be recomputed onto common conditions from
  recorded runs). Draw (c) as designed.
- **They do not.** Then the honest result is a **per-family table, each with its own
  null and conditions stated, and no composite chart** — plus a recorded note that
  the families were never swept on common ground. That is a real finding about the
  project's own instrument, and it is a better outcome than a handsome chart that
  quietly rebases five sweeps onto a sixth's null.

Do not resolve a mismatch by picking whichever null makes the lines meet.

## 3. Recommended approach

1. **Reconcile the nulls** (§2). Read the conditions off the sweep scripts in each
   `data/results/*` workspace, not off the prose. Produce the table first and
   commit it — it is the deliverable that decides everything after it.
2. **Recompute on common ground where the recorded runs allow it.** Every family's
   null arm is ablatable to bit-identity, so a shared null is a re-read rather than
   a re-run wherever the runs exist at matching conditions. Prefer re-reading;
   re-simulate only what is genuinely missing, and say which was which.
3. **Normalise the parameter axis.** λ, κ and α have different bands and different
   meanings. Plot against each family's declared band normalised to [0, 1] — null
   at 0, band end at 1 — and state in the caption that the x-axis is
   position-in-band, never a common magnitude. A shared x-axis of raw parameter
   values would be a fabricated comparison.
4. **Draw (c), then (b).** Then stop.
5. **Record** as `docs/implementation/pipeline/ogasp/plurality_reporting.md`: the
   reconciliation table, the figures with their conditions, and the ruling on which
   result carries which claim.

### Drawing discipline — the fig6 lesson applies directly

[`stealth_spacing_diagnostic.md`](../implementation/pipeline/ogasp/stealth_spacing_diagnostic.md)
§7a records three passes to draw one figure, and the failure was the same each
time: **a chart that shows a level comparison without letting the eye compute
one.** The lesson generalises and should be applied here rather than rediscovered:

- **The comparison must be a position or a vertical distance**, never an integral,
  an area, or an annotation describing a quantity the panel does not show.
- **No accentuation on evidence figures** — no arrows, circles, callouts or
  highlight colours. Let the lines and cells carry it. Accentuation is reserved for
  dissertation chapters, where the argument is already made in prose.
- **Uniform treatment across instances.** Same axis limits, same normalisation,
  same seed count for every family; a per-family adjustment needs stating and
  justifying in the record.
- If a figure needs a sentence explaining why it does not contradict its own
  table, it is the wrong figure. Redraw it.

## 4. Pre-register before drawing

Lighter than a sweep's pre-registration — nothing here is simulated — but the two
that matter are committed before any figure exists:

- **P1 — kill criterion.** The entropy curve is not a re-expression of visit
  concentration at the busiest place: Spearman |ρ| between pooled path entropy and
  the maximum single-place visit share is **below 0.90**, computed across the same
  runs. This is the recorded hub-domination blind spot given a test, at the
  threshold the exposure and disengagement studies both used, so verdicts stay
  comparable. **If it fires, the figure is not drawn** — an entropy chart that is a
  hub-occupancy chart misreports the axis.
- **P2 — direction.** The narrowing direction is committed in advance for all six
  families, including change B's rise. It is already on record in six places, so
  this costs nothing and closes the door on a chart drawn to fit.

## Validation gate

1. **Reconciliation table committed before any figure**, with each sweep's
   conditions sourced to its script and the script path recorded.
2. **P1 computed and reported**, whichever way it lands.
3. **Readers only.** Full `tests/l3_simulation` plus the substrate/carve/golden
   suites pass **unchanged**. Nothing here simulates anything new; a moved golden
   means something was built that should not have been.
4. **Figures regenerate from a committed script** into
   `data/misc/_viz/plurality/`, from recorded runs, deterministically. The axis-5
   record's §7 warning is the precedent: a viz script that drifted onto changed
   defaults silently redrew one study's numbers under another's titles.
5. **Every figure carries its conditions in the figure itself** — mapping, MTD
   condition, seed count, pooling level. A panel that can be pulled into a chapter
   without them will be.
6. **No ordering claim without disjoint intervals**; `interval_report` is the gate.

## Hard constraints

- **No mechanism, no new declared family, no re-sweep to make a line smoother.**
- **Scores move on evidence only** — never change the model, weights, mapping or
  metrics to improve a row (S6;
  [`../workflows/guardrails.md`](../workflows/guardrails.md)).
- **No badge move.** Axis 3 is already DEMONSTRATED and nothing here re-scores it;
  a figure is not evidence the badge did not already have.
- **The reported-configuration pin holds.** The badge's evidence is the
  **modulators-null** arm; any modulator-active arm reports its own plurality
  figure ([`model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
  §4). The chart in (c) is precisely a picture of that rule, and must not be read as
  relaxing it.
- **Variety, not strategy.** The honest limit travels with every figure and caption.
- Determinism (SIM-05); Australian English; branch per session; commit locally;
  **never push**.

## Reading list

- [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  §12 — the badge, both halves of its criterion, and the variety-not-strategy limit.
- [`../implementation/pipeline/ogasp/modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)
  §4–§5 — the reported-configuration pin, factors 8 and 9's bands, and the
  sub-additive composition result.
- [`../implementation/pipeline/ogasp/iterated_cost_model.md`](../implementation/pipeline/ogasp/iterated_cost_model.md)
  — changes A and B, and the λ table that is the one rising line in the family.
- [`../implementation/pipeline/ogasp/stealth_spacing_diagnostic.md`](../implementation/pipeline/ogasp/stealth_spacing_diagnostic.md)
  §7a — three passes to draw one figure, and why. Read before drawing anything.
- [`../implementation/pipeline/ogasp/measurement_suite.md`](../implementation/pipeline/ogasp/measurement_suite.md)
  §(b) — `path_entropy`'s hub-domination blind spot, which P1 tests.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  §(b) and §(d) axis 3 — the census-not-a-scale claim figure (c) makes visible, and
  the badge's standing qualifications.

## Out of scope (explicitly)

- **Any mechanism**, any new modulator, any parameter re-declaration.
- **Re-running the six sweeps.** This is a re-read and a reconciliation; if a
  family's null cannot be recovered from recorded runs, record that rather than
  re-simulating it.
- **Re-scoring axis 3**, or any other row.
- **Dissertation prose and chapter placement.** The record names which figure
  carries which claim; where it lands in the thesis is a separate pass.
- The axis-2 ablation ([`2026-08-09_objective_conditioning_ablation.md`](2026-08-09_objective_conditioning_ablation.md))
  and axis 4's unrun readers — adjacent, separately tracked.
