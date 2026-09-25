---
status: open                  # executes register E8; scrutinised 2026-09-25 (critique only); rulings F1 (amended), F2–F5 owed
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
4. **Chapter 5 fixes** (same generators, small): Figure 5.1 panel (a) in **colour** — a sequential heat-map fill for the share of steps per tactic (a scoped exception to greys-plus-one-accent, recorded in conventions §i beside the profile-hue exception); panel (b) as a **bar chart**, x = opening length in steps, one colour, y = share of runs that have left the commonest opening (Jin: bars for proportions, lines for correlated points); Figure 5.2 gains a **key** for the hollow circles (each mechanism alone) inside the axes. *Added 2026-09-23 (Marc, at the restructure: "include the baseline, but that's for later"):* Figure 5.1 now opens §5.2 *APT attacker model versus baseline attacker*, so it carries the baseline attacker beside the profiles, drawn in whatever form panel (a)'s tactic axis allows (the baseline walks phases, not tactics).
5. `FLOATS.md` rows for every new or moved figure, in the same commit.

## Rulings owed (Marc)

- **F1** the box set (the names are ruled: L0 the campaign corpus, L1 the attack graph, L2 the attack profiles, L3 the profile nets, L4 the join, then MTDSim — no layer names, no *traversal*; the interim relabelling of the current ladder and of fig:runtime-loop is in git `tools/pipeline_ladder_figure.py` / `tools/runtime_loop_figure.py`, 2026-09-22).
- **F2** the colour exception for Figure 5.1(a).
- **F3** whether the current worked-example ladder survives as an appendix figure or is cut down into the two zooms only.

## Scrutiny 2026-09-25 — critique only, nothing redrawn

Run with the extended `/scrutinise-figure` (schematic variant; design reference
`.claude/skills/scrutinise-figure/diagram_best_practice.md`, corpus evidence
`docs/implementation/evaluation_anatomies/_overview_figures_survey.md`) on the
figure as built 2026-09-08/-24. Marc's relay of the supervisor (2026-09-25):
still too complicated, labels trying to do too much, not intuitive for the
audience; the long caption gives it away; the levels are not levels — is
MTDSim a level? Four independent reviewers: a cold reader with the caption, a
figure-only cold reader, a context critic, a diagram auditor (P1–P21). Every
claim below was checked against the tex or the generator before acceptance.

**Proposed pass criterion (Marc to agree before any redesign).**
- *The one sentence* (the introduction's approach paragraph, l.~335–354, in
  its words): the 38 attack flows are combined into one graph, split into
  attack profiles by objective, and each profile is executed in MTDSim as the
  APT attacker model, beside the baseline attacker, with and without the
  defences, and measured.
- *The parts*, by kind:

  | Part | Kind | Built or used | Section |
  |---|---|---|---|
  | the 38 attack flows (CTI) | input data | used (CTID's analysts drew them) | §4.1 |
  | the attack graph | derived artefact | built | §4.1 |
  | the attack profiles $c_1$–$c_4$, $c_{\mathrm{agg}}$ | derived artefacts | built | §4.2 |
  | the profile nets | executable artefacts | built | §4.3 |
  | the join (dwell times, tactic-to-verb mapping, failure matrix) | runtime coupling | built | §4.4 |
  | MTDSim: network, MTD mechanisms, the attacker actions, the baseline attacker | existing system | used | ch2 |
  | the metrics | output | defined | §4.5 |

**What every reviewer converged on (blocking).**
1. *It is a worked example, not an overview* (P7): over sixty elements below
   method level; five visual grammars (flow graphs on an axis, merged graph,
   banded rows, a firing net, a message loop); ~24 legend entries against a
   ceiling of about six (P9); two in-figure legends; a 136–142-word caption with
   ~14 decodes and at least five encodings never decoded (the blue frame, the
   ring glyph, the clock, the token box's border, the grey L4 panel) against a
   corpus norm of 2–9 words (P10–P12). The cause of most other hits: remove
   the example and they clear together.
2. *The story is half told* (P21): no defences, no baseline attacker, no runs,
   no measure. Both cold readers named "where is MTD, and what comes out?" as
   the first gap, unprompted. The chapter answers a question about MTD
   performance; the figure stops at a loop with nothing leaving it.
3. *L4 contradicts the chapter*: the figure's gutter and caption say L4 is
   MTDSim (l.4001, l.4010); the §4.4 heading says L4 is the join (l.4759) and
   its first line "Everything from L0 to L3 produces the profile net" (l.4779).
   The registry row 47 records the gutter as *MTDSim*, which is wrong on the
   text's own terms. "join" also names both the arrow into L4 and a box inside
   it.
4. *Terms the reader does not have* (P14): ~16 figure words with no antecedent
   before the figure — *aggregate*, *condition on objective*, *give executable
   semantics*, *Petri net* (0 body uses before ch4), *attack graph* (0),
   *token*, *fires*, *dwell*, *verb*, *verdict*, *re-weighting*, *runtime loop*,
   *double extortion*, *no realised objective*, $c_1$–$c_4$, L0–L4. The
   introduction says *combine* and *split by objective*; the figure says
   *aggregate* and *condition on objective*.

**The two questions the supervisor raised.**
- *Are they levels?* No. L0 is input data, L1–L3 are successive artefacts each
  made from the whole of the one before (a pipeline of stages: Garlan & Shaw
  1994 pp. 6–7), L4 is a runtime coupling, MTDSim an existing system. A layer
  is built on and uses the one below (Garlan & Shaw p. 11; Bachmann et al.
  2000 pp. 11–13); a level is a zoom into more detail (Yourdon §9.3; C4). None
  holds here, and both cold readers read "L" as layer or level, then found the
  figure contradicting it ("L2 is finer again than L1", "L4 is a system, not a
  representation"). *Level* is also ratified for network depth (registry
  row 59). The supervisor's *phase* is taken twice (the baseline attacker's
  six phases; the evaluation's two phases, E1); *stage* is taken by the
  lifecycle stages of §4.4. So no class noun is free, and none is needed if
  the parts are named by what they are.
- *Is MTDSim a level?* No. It is the system the work uses, not a product of
  the chain: the introduction calls it "an existing MTD simulator", §4.4 says
  the model is built "beside MTDSim --- not embedded in it". Drawn as the last
  rung it reads as something the thesis built (P18) — the boundary an examiner
  checks first. The lineage draws the simulator as a container with the new
  part beside it (Tay 2024 Fig. 1 p. 13; Ho 2024 Fig. 1), never as a step.

**Also found.** The grey paths in the L2 rows are the whole graph's twelve
most-observed edges filtered by tactic (`tools/pipeline_ladder_figure.py`
~l.367–405), not each profile's own paths, so the rows draw every profile
alike. Blue carries five meanings (flow A, the thesis's work, the objective,
the token, the firing); the objective ring in L2 is the same glyph as a
marked place in L3. The caption still names and cites the two flows (E8 said
delete). $c_{\mathrm{agg}}$ is absent.

**Sound, and should survive** (the auditor's list, checked): the spine of
noun artefacts joined by verb-labelled arrows (Wong's "A to B" form), with the
introduction's verbs; the stacked-cards glyph for "38 flows" as the input
shape; the plain cardinality lines ("one profile, one net"); top-down or
left-to-right with no reversals; the generator's read-from-artefacts
discipline, which moves to the zooms. The worked example itself is sound
material for the §4.1 zoom (F3).

**Recommended box set (for F1).** Ferraz et al. 2024 Fig. 2 (p. 6) is the
closest corpus match — CTI to executable adversary behaviour: input shape,
stage shapes, output shape, the verbs above the arrows, one accent on the
contribution, the platform not drawn as a step. With the lineage's container:
- left: **38 attack flows** (stacked cards; "cyber threat intelligence")
  → *combine* → **attack graph** → *split by objective* → **attack profiles**
  ($c_1$–$c_4$ as four small tiles, names beside) → *make executable* →
  **profile nets** — the part built once, framed and labelled as such;
- right: an **MTDSim** container (drawn as existing: grey or dashed) holding
  *network*, *MTD mechanisms* and *attacker actions*; the profile nets reach
  the attacker actions through **the join** (the one accent: the APT attacker
  model), the **baseline attacker** reaches the same actions from the other
  side;
- out: **metrics, per attacker** (§4.5).
About four groups (flows; graph and profiles; nets and join; MTDSim and
metrics), one arrow meaning in the chain ("becomes", verb-labelled) and one
across the boundary ("drives"), no legend, and a caption of one or two
sentences. Every part a noun the introduction already uses, except *attack
graph* and *profile net*, which the figure defines by boxing them. Section
numbers under the boxes do the job the L-labels did.

**Rulings owed (added 2026-09-25; F1 amended).**
- **F1 (amended)** — the box set above, or Marc's own. The ruled names stand,
  except that L4 is *the join* and MTDSim is not an L-part.
- **F4 — the L-labels.** (a) *Recommended:* drop them from the figure and from
  the four chapter 4 headings (the parts named by what they are: "Cyber threat
  intelligence to attack graph", "Attack profiles", "Profile nets", "Joining
  the profile net to MTDSim"); the parts need no class noun. Overturns the
  2026-09-04 heading convention (keep L0–L4 prefixes) and registry row 47's
  "L-labels as signage", on the supervisor's merit point: the labels name a
  structure the method does not have. (b) Keep them in the headings only, as
  section signage, with nothing on the figure. (c) Keep both, glossed once as
  numbering only. 21 non-comment L-label sites in the tex to sweep under (a).
- **F5 — the figure's scope.** Whether the head figure carries the defences,
  the baseline attacker and the metrics (recommended: yes; the question the
  chapter answers is about MTD, and the cold readers looked for it first).
- **Registry row 47** to correct under any option: L4 is the join; the figure
  gutter *MTDSim* entry is wrong.

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
