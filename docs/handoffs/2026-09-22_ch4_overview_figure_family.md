---
status: open                  # executes register E8; Marc's day of drawing; rulings F1–F3 owed
created: 2026-09-22
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E8
companions: ../workflows/terminology.md (what the boxes are called — RULED 2026-09-22: the profile net, the join, MTDSim; no layer names; the L-labels as signage), ../workflows/figure_table_conventions.md §(n) (the SVG route), the scrutinise-figure skill
---

# The chapter 4 overview as a family — one high-level box figure at the chapter head, a zoom per section — and the three chapter 5 figure fixes the supervisor named

## State of play

**The ruling (E8).** "Getting this figure right is like explaining half of your work." The current Figure 4.1 (`fig_4-0a_pipeline_ladder`, `tools/pipeline_ladder_figure.py`; rebuilt 2026-09-08 on the previous supervisor verdict as a schematic worked example tracing two real flows through L0–L4 in two hues) still does too much: arrows standing for relationships are not intuitive, "aggregate" cannot be read, and the L3 fragment is a sub-component drawn inside the overview. Ruling: a **high-level box figure** — the boxes and how they link, nothing else — at the chapter head, and each sub-component as a **zoom in its own subsection**, reusing the section figures. Profiles labelled by code; flow names deleted. Marc: a day's work. This is the 2026-09-09 family ruling (dense figures get a family at descending abstraction) applied to the figure the family was meant for.

**What exists to reuse.**

| Level | Zoom figure today | Gap |
|---|---|---|
| L0 → L1 | none in the chapter; App. B has `fig_B-1a_gap_flow_exemplar` and the technique-graph figures | a chapter zoom: two flows merged into one graph — the worked-example half of the current ladder is exactly this and can be cut down to it |
| L2 | none | the partition of the graph into $c_1$–$c_4$ and the aggregate — the "aggregate" Jin could not read is this step |
| L3 | Figure 4.2, the GSPN gadget (`fig_4-3a`) | stands |
| L4 | Figures 4.3 (tactic-to-verb mapping), 4.4 (failure matrix), 4.5 (runtime loop) | stand |
| MTDSim | chapter 2's model figures (`fig_2-2a` … `fig_2-2-3a`) | referenced, not redrawn |

## Recommended approach

1. **The head figure** (`fig_4-0a`, same label `fig:pipeline` so refs stand): boxes for L0 the campaign corpus → L1 the attack graph → L2 the attack profiles $c_1 … c_4$ and $c_{\mathrm{agg}}$ → L3 the profile nets → L4 the join (its three declared inputs named on the arrow or inside the box) → MTDSim (network, defence mechanisms, the attacker's actions). One accent, greys; no data drawn; the L-labels as Marc's signage; whatever the terminology ruling keeps as names is what the boxes say — the figure *is* the definition Jin asked for ("in your figure you box them, this is the X, this is the Y, then you show how they're linked"). SVG route per conventions §(n) (`tools/ch2_model_figures.py` is the working pattern), printed to PDF; counts in the caption only.
2. **The zooms**: cut the current ladder's L0–L2 half into two chapter figures (L0→L1 merge; L2 partition with the aggregate shown as the un-partitioned graph), placed at §4.1 and §4.2; Figures 4.2–4.5 stay where they are. The two-hue exception (conventions §i, 2026-09-08) travels to the L0→L1 zoom, which is where the two flows are traced; the head figure takes none.
3. **Scrutinise** the head figure the standard way: a cold reader given only the figure, caption and one sentence must restate the pipeline in one sentence; repeat until no blocking defect.
4. **Chapter 5 fixes** (same generators, small): Figure 5.1 panel (a) in **colour** — a sequential heat-map fill for the share of steps per tactic (a scoped exception to greys-plus-one-accent, recorded in conventions §i beside the profile-hue exception); panel (b) as a **bar chart**, x = opening length in steps, one colour, y = share of runs that have left the commonest opening (Jin: bars for proportions, lines for correlated points); Figure 5.2 gains a **key** for the hollow circles (each mechanism alone) inside the axes.
5. `FLOATS.md` rows for every new or moved figure, in the same commit.

## Rulings owed (Marc)

- **F1** the box set (the names are ruled: L0 the campaign corpus, L1 the attack graph, L2 the attack profiles, L3 the profile nets, L4 the join, then MTDSim — no layer names, no *traversal*; the interim relabelling of the current ladder and of fig:runtime-loop is in git `tools/pipeline_ladder_figure.py` / `tools/runtime_loop_figure.py`, 2026-09-22).
- **F2** the colour exception for Figure 5.1(a).
- **F3** whether the current worked-example ladder survives as an appendix figure or is cut down into the two zooms only.

## Validation gate

The head figure passes a cold read (the reader restates the pipeline in one sentence with no term they had to look up); each of L0→L1, L2, L3 and L4 has a zoom in its section; Figure 5.1 is in colour with panel (b) as bars; Figure 5.2 has its key; conventions §i records the exceptions; `FLOATS.md` current; build clean.

## Hard constraints

- Figures generated by `tools/` into `docs/thesis/figures/` (the figure pipeline); Helvetica figure face; pack-to-page-box.
- No accentuation beyond the encoding (no arrows or highlights for emphasis in evidence figures).
- Labels unchanged so every `\ref` stands.

## Reading list

- `tools/pipeline_ladder_figure.py` — the current drawing and its data reads (keep the drift guards).
- `docs/workflows/figure_table_conventions.md` §d, §h, §i, §(n).
- `docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md` §8b–§8c (Figure 5.1's design record), §8g (Figure 5.2's).
- `tools/ch5_unopposed_figures.py`, `tools/ch5_disruption_figure.py`.

## Out of scope

Chapter 2's figures (Marc is editing them in the working tree today — `tools/ch2_fig23_*`, `ch2_fig24_*`, `ch2_model_figures.py` — leave them to him); the chapter 5 effectiveness figures (the restructure and corpus handoffs redraw them).
