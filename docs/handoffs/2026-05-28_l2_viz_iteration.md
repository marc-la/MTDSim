---
status: open
created: 2026-05-28
---

# Tidy the GASP visualisations + add a side-by-side comparison view, moving outputs to `data/gasp/_viz/`

The L2 partition decision
([`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md))
landed with a first cut of class-subgraph visualisations under
`data/gap/_viz/gasp_*` (gitignored). They are diagnostic-quality, not
defence-ready: the technique-level subgraphs are hairball-dense at the
default `min_obs=1`, the per-class tactic FSMs are produced four-apart
rather than in a single comparable frame, and the outputs sit under the
GAP's `_viz/` directory rather than a GASP-dedicated one. The verdict
itself is settled — this handoff is purely **visual iteration** with a
strong human-readability gate.

## State of play

**Settled (don't re-derive):**

- P6 is the accepted L2 classification scheme. Class membership is
  audit-traced at
  [`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv);
  per-flow justifications at
  [`../notes/2026-05-28_l2_per_flow_justifications.md`](../notes/2026-05-28_l2_per_flow_justifications.md).
- Class subgraph definition is **surface** (techniques present in the
  class's flows; no ancestor closure) — see the partition-decision note's
  *Rubric* section for why ancestor closure failed on this graph.
- Existing viz outputs (under `data/gap/_viz/`, gitignored, regenerable
  via `python data/gap/_viz/gasp_viz.py`):
  - 4 × `gasp_p6_<class>.svg/png` — technique-level subgraphs,
    tactic-clustered L→R kill-chain order.
  - 4 × `gasp_p6_<class>_tactic_fsm.svg/png` — per-class tactic FSMs.
  - 1 × `gasp_p6_comparison.png` — heatmap + Δ-vs-baseline + class
    signature panel.
- Existing GAP viz at `data/gap/_viz/gap_viz.py` carries the style
  prior art (entry green, objective orange, edge weight ~observation
  count, backward edges red).

**Unsettled (this handoff resolves):**

- The technique-level class subgraphs are unreadable at `min_obs=1` (the
  pure_steal class has 413 edges across 98 nodes — a hairball).
  Filtering at `min_obs >= 2` should reveal the recurring backbone where
  the workflow differences would shine.
- The per-class tactic FSMs are rendered four-apart. A **2×2 grid**
  side-by-side view, same axes / scale / palette, would make
  workflow-shape comparison visually direct.
- Output location: should move under `data/gasp/_viz/` (a peer to
  `data/gap/_viz/`) so the GAP and GASP artefact families have
  symmetric layouts.

## Recommended approach

A single visualisation-only session — no spec changes, no data changes.

### Tasks

1. **Move the viz layer to `data/gasp/_viz/`.**
   - Create `data/gasp/` and `data/gasp/_viz/`.
   - Add the gitignore pattern `data/gasp/_*` to `.gitignore` (mirrors
     `data/gap/_*`).
   - Move `data/gap/_viz/gasp_viz.py` → `data/gasp/_viz/gasp_viz.py`
     (this is *the* GASP viz script; it doesn't belong under GAP's
     `_viz/`).
   - Update the script's path constants to find the GAP json
     (`../gap/gap_v0.5.json`) and the per-flow YAMLs (`../gap/flows/`)
     from the new location. Output paths land in `data/gasp/_viz/`.
   - Regenerate to confirm: same set of outputs at the new path.

2. **Iterate on technique-level class subgraphs at `min_obs >= 2`.**
   The GAP construction note already showed the *recurring backbone* is
   12 % of edges (59 of 478, obs ≥ 2;
   [`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)).
   The hypothesis: at `min_obs >= 2`, the per-class subgraphs shrink to
   their *generalised* core and the cross-class differences become
   visually legible. Steps:
   - Add `--min-obs` flag to `gasp_viz.py` (mirroring `gap_viz.py`).
   - Render `gasp_p6_<class>_obs2.svg/png` for each of the 4 classes.
   - Apply `_drop_tiny_components` (already used in `gap_viz.py` at
     `floor=3`) to strip isolated dyads — the same legibility
     adjustment.
   - **Human-readability gate**: render, *look at the output*, decide
     whether obs=2 is the right cutoff or whether to try obs=3 / obs=4
     etc. Don't ship without an actual eyeball pass.

3. **Add a 2×2 grid comparison view.**
   - One matplotlib figure (NOT graphviz — graphviz doesn't compose into
     a grid cleanly), each cell a tactic FSM for one class. Same node
     palette, same edge-weight scale, same tactic positions across all
     four cells (use a fixed kill-chain layout so the eye can compare
     tactic-by-tactic).
   - Render at `data/gasp/_viz/gasp_p6_grid_tactic_fsm.{png,svg}`.
   - **Human-readability gate**: look at the grid, decide whether the
     workflow differences are visible at a glance. If not, iterate on
     the colour-mapping / edge-thickness / layout until they are.
   - If the tactic-FSM grid doesn't reveal anything beyond what the
     heatmap in the existing `gasp_p6_comparison.png` already shows,
     consider whether the grid is worth keeping — it may turn out to be
     redundant. Better to ship 1 great viz than 2 mediocre ones.

4. **Critique-and-trim sweep on the existing viz set.**
   - `gasp_p6_comparison.png` (3-panel — heatmap + delta + signature
     table) is the most-useful single-image. Inspect: is the delta
     panel adding signal beyond the heatmap, or duplicating it? Trim if
     duplicating.
   - The per-class tactic FSMs may be redundant once the grid view
     exists. Inspect; trim duplicates.
   - The technique-level subgraphs at `min_obs=1` are likely
     unreadable; consider replacing the default outputs with `obs=2`
     and adding `_obs1` only as an explicit unfiltered diagnostic
     (mirrors how `gap_viz.py` handles min-obs).

### What "human-readable enough" looks like (the gate)

The handoff session is **required** to do at least one *literal* eyeball
pass on the outputs and judge readability. Concretely:

- Open the PNG (Read tool on the image path) and look at it.
- Ask: would I show this to my supervisor unannotated and expect them to
  read the workflow differences off it?
- If no, iterate the script: change `min_obs`, drop tiny components,
  re-order tactics, change the colour palette, adjust label size.
- Don't ship until the answer is yes (or until the session has tried
  three iterations and surfaces "this is as legible as the data
  allows").

### Alternatives considered

- *Stay with graphviz everywhere.* Rejected for the grid view —
  graphviz doesn't compose into a multi-axis figure cleanly. Mix
  matplotlib for the comparison views, graphviz for the single-class
  detail views.
- *Add interactive viz (plotly / pyvis).* Rejected for this handoff —
  static PNG / SVG is the deliverable. Interactive viz is an
  L4-presentation concern, not an L2-classification-check concern.
- *Defer the move-to-`data/gasp/` until L2 implementation lands code
  outputs there.* Rejected — better to do the directory restructure
  now while the data tree is small (one viz dir to move), than after
  the implementation lands its own outputs.

## Validation gate

Done when:

1. `data/gasp/_viz/` exists, contains the moved + iterated viz script,
   and `.gitignore` covers `data/gasp/_*`.
2. The viz script regenerates all outputs cleanly with both `--min-obs=1`
   and `--min-obs=2`.
3. At least one technique-level class subgraph at `min_obs=2` is
   visually legible (eyeball pass passed).
4. The 2×2 grid tactic-FSM view exists *or* the session has documented
   why it didn't make the cut (e.g. "the heatmap already shows this
   more clearly").
5. The session leaves a note recording its eyeball-pass judgements
   (which `min_obs` cutoff, which views kept / trimmed, what the
   workflow differences look like at each cutoff). Note location:
   append to
   [`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)
   under the *Investigation artefacts* section as a one-paragraph
   "Visualisation iteration outcomes". No new notes file.
6. This handoff is deleted in the same commit that ships the viz
   changes (per [`../specs/session_workflow.md`](../specs/session_workflow.md)
   handoff lifecycle).

## Critique

Three pitfalls to avoid:

- **Scope creep into publication-quality.** This is diagnostic viz for
  the analyst's eyes — not a thesis figure. The defence-ready viz lives
  in chapter 3 of the dissertation, generated separately later. If the
  session starts thinking about colourblind-friendly palettes,
  high-DPI export, layout-stability across re-runs — that's chapter-3
  work. Cap the polish at "readable on first glance".
- **Iterating viz to *find* differences that aren't there.** The
  workflow differences between classes are *real but subtle* — Marc's
  own prediction. If at `min_obs=4` everything looks the same, that's
  data, not a viz failure. Don't keep tightening filters to manufacture
  separation; report what the data actually shows.
- **Trimming the wrong views.** The single most useful viz today is
  `gasp_p6_comparison.png` (heatmap-led). Don't trim that in favour of
  the grid view unless the grid genuinely supersedes it. Better to
  *delete* the per-class tactic FSMs (4 files) and *keep* the
  comparison + grid (2 files).

## Hard constraints

- **Branch hygiene.** Dedicated session branch (`viz/l2-tidy` or
  similar); never on `main`; no push.
- **No data changes.** This handoff touches the viz layer only. If the
  session surfaces a per-flow YAML issue that affects classification,
  *record as a follow-up*, don't action.
- **No spec changes.** The L2 spec consolidation is a separate handoff
  ([`./2026-05-28_l2_spec_consolidation.md`](./2026-05-28_l2_spec_consolidation.md));
  this handoff doesn't touch `docs/specs/`.
- **Determinism.** The viz script's RNG-free; outputs should be
  byte-stable across re-runs.

## Reading list

In order:

1. **[`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)** —
   the verdict the viz illustrates. Skim §"Discrimination evidence"
   to know what the viz is supposed to surface.
2. **[`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)
   §"What the assembled graph looks like"** — the 88 % single-observation
   finding that motivates the `min_obs >= 2` iteration.
3. **`data/gap/_viz/gap_viz.py`** — the style prior art. Reuse helpers
   (`_short`, `_node_label`, `_edge_style`, `_drop_tiny_components`,
   the tactic-cluster layout) verbatim — they're already battle-tested
   on the GAP viz.
4. **The current `data/gap/_viz/gasp_viz.py`** — the starting point
   that needs the iteration.

## Out of scope

- Implementation of `src/mtdsim/l2_subgraph/` — that's handoff
  [`./2026-05-28_l2_implementation.md`](./2026-05-28_l2_implementation.md).
- The GASP spec consolidation — handoff
  [`./2026-05-28_l2_spec_consolidation.md`](./2026-05-28_l2_spec_consolidation.md).
- Any change to the audit CSV or the classifications.
- Interactive / web-based visualisations.
- Thesis chapter-3-quality figures.
