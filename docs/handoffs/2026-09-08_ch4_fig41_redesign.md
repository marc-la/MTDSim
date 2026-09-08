---
status: open
created: 2026-09-08
---

# Rebuild Figure 4.1 (fig:pipeline) as a schematic a general computer-science reader can follow

## State of play

**The supervisor's verdict (relayed by Marc, 2026-09-08).** Figure 4.1 is
"terrible": a reader with a general computer-science background sees a mess on
the page. It is too small and at too low a level of abstraction. What survives
the verdict: the layer bands are right, and the pipeline (the rung-to-rung
descent) is legible. What he asked for, rung by rung:

- **L0** — do not show all 38 flows. Show one or two attack flows side by side,
  one green and one yellow.
- **L1** — show those same two flows *coming together* in the attack graph, so
  the green and the yellow are visibly merged.
- **L2** — the profiles need neither names nor counts; "Profile 1 … Profile 4"
  is enough.
- **L3** — do not draw the whole net; show "a little bit of the magic
  happening".
- **Bottom band (controller / action, the numbered loop)** — he understands it
  and it is good, but it could go back to being a separate figure and be
  inflated.
- Overall: take the full page, go up a level of abstraction, and convey *more*
  by drawing less.

**What the figure is now** (`tools/pipeline_ladder_figure.py`, 678 lines,
TikZ, 462 × 521 pt, `[p]` float at `\textwidth`). It is a *data-faithful
thumbnail ladder*: every rung draws the real artefact at reduced scale. L0 is
38 flow rows with a mark per tactic; L1 is all 124 techniques and 478
transitions on the tactic axis; L2 is four bands of the profile subgraphs;
L3 is the 15-place, 109-transition net of one profile. Below it, since
2026-09-05, the runtime loop (six badges, controller band with three glyphs,
inherited action band) is folded in from the retired fig:movement-dataflow.
The design rule it was built to — "every mark is read from a tracked
artefact, nothing typed" — is the right rule for an *evidence* figure and the
wrong rule for a *definition* figure. Rendered at page width, L1 and L2 are
grey hairball texture: the eye reads "dense", not "aggregate" or "condition
on objective". The verbs on the between-rung arrows are the whole argument,
and the drawing shows before-and-after states at a scale where neither is
readable, so the transformation is never seen.

**Why this is the same failure as fig:l1-graph (2026-08-20).** Marc deleted
that figure for the same reason: a dense graph compressed into a `\textwidth`
float "doesn't communicate anything to the reader". The remedy then was to
give the real graphs full appendix pages (fig_B-1a–d). The remedy here is
different: the chapter-opening figure is not evidence, it is the definition of
the ladder, so it should be drawn as a schematic worked example — the genre
fig:mtdsim-model (fig_2-2a) already uses and Marc ratified on 2026-08-27
("don't constrain yourself to TikZ … replace words with symbols — only
component names should be text").

**Two figures are competing for one float.** The ladder (L0→L3, a
construction) and the runtime loop (L4, a cycle) have different grammars — a
descent and a loop. Folding the loop in on 2026-09-05 made the float carry
both, and the supervisor's "put the bottom into a separate item and inflate
it" is the direct reversal. The fold-in was a session-level tidy, not a
ruling on the argument, so reversing it costs nothing.

## Recommended approach

Split into two floats and rebuild the first as a schematic.

### Figure 4.1 (fig:pipeline) — the build ladder, L0 → L3 → L4, full portrait page

One `[p]` float, packed by the generator to the page box (455 pt wide; measure
the usable height in the build — the current 521 pt tall figure fits with its
caption, so there is room to roughly double the rung heights). Four rungs plus
a terminal L4 box, on the shared tactic axis (conventions §b6 — keep the
fifteen tactics in kill-chain order as faint column bands behind every rung so
the axis is *seen*, not read off a header). Each rung is a **worked example
at readable size**, not the artefact:

1. **L0 — two real attack flows, side by side.** Each drawn as a short chain of
   technique boxes (no IDs, no names — the supervisor's "you don't need
   names") placed in their tactic columns, flow A in the accent and flow B in
   the second mark (ruling R2 below). Pick the pair *by rule* in the
   generator, never by name (mechanism-not-exception): the smallest pair of
   flows, at most nine techniques each, that share at least two techniques and
   belong to different objective classes. On the current GAP that rule yields
   `tesla_kubernetes_breach` (9 techniques, impact objective) and
   `uber_breach` (6 techniques, exfiltration objective), sharing T1078 and
   T1552; a same-class alternative with more overlap is the two CISA
   AA22-138B flows (8 and 7 techniques, five shared). A ghosted "… and 36
   more" stack behind the pair says the corpus is bigger without drawing it.
2. **Arrow "aggregate"**, then **L1 — the two flows merged.** The same boxes,
   now one graph: shared techniques drawn once and marked as both flows, edges
   drawn by both flows heavier than edges drawn by one. This *is* the
   supervisor's "now the green and the yellow are together". A faint ghost of
   the rest of the graph (a few grey nodes and edges, not the 478) says the
   real graph is larger.
3. **Arrow "condition on objective"**, then **L2 — four profile cards.** Four
   small identical silhouettes of the L1 shape, each with a *different*
   objective column accented (exfiltration; impact; both; command-and-control
   for the no-realised-objective class). Same graph, different objective —
   that is what "condition" means, and it needs no counts. Label with the
   chapter's objective names (ruling R3), not "Profile n".
4. **Arrow "give executable semantics"**, then **L3 — a fragment of the net,
   firing.** Three or four places (tactics) with the transitions between
   them, drawn in the Marsan convention fig_4-3a already uses, and the "magic"
   shown as two states: the token in one place, then the token moved after a
   transition fires, with the weight glyph on the transition and the dwell
   draw on the place. Nothing else from the net. The full net stays where it
   belongs (fig_4-3a and the appendix ledgers).
5. **L4 — one box:** "attacker-agent traversal in MTDSim", with a pointer to
   the runtime-loop figure. The tactic-down / re-weighting-up arrows that
   today cross into the controller band become one labelled edge into this
   box.

Drop every count from the rungs (38 / 124 / 478 / 15 / 109). They move to the
caption or the section prose, where a number belongs; the fact sheet the
generator prints still supplies them.

### Figure 4.x (fig:runtime-loop) — the numbered loop, at `\textwidth`, in §4.4

Restore the bottom third of the current figure as its own float at the
mechanics section (`subsec:mechanics-join`): the controller band (dwell
draw, tactic-to-verb mapping, failure matrix as glyphs), the inherited action
band (attacker / network / defender), and the six badges — tactic down,
drawn dwell time and verb down, verdict up splitting into failure (into the
matrix) and success (bypassing), re-weighting up, next tactic. Inflate to the
full text width so the glyphs read; the supervisor said this part already
communicates, so change the scale, not the drawing. The L3 rung it needs at
the top becomes the same net fragment as Figure 4.1's rung 4, so the two
figures share one visual vocabulary. The existing `emit()` code for the
controller and action bands can be lifted almost verbatim into the new
generator.

### Authoring route

The HTML/SVG route (`tools/mtdsim_model_figure.py` + `.html` is the pattern):
hand-authored SVG for the pictograms and free layout, printed to PDF through
headless Chromium at natural size, with the build script doing what the
current generator does well — validating every fact the drawing depends on
against the artefacts (the pair-selection rule against the GAP, the tactic
order against the pinned bundle, the objective tactics against
`OBJECTIVE_TACTICS`, the net fragment against the structural JSON) and
printing the fact sheet. Same greys + accent, house sans, 8 pt floor. TikZ is
workable too, but Marc ruled on 2026-08-27 that free-layout schematics go the
HTML route because TikZ is token-expensive and hard to iterate on visually.

### Rulings owed to Marc (one question each, recommendation first)

- **R1 — Split into two floats.** Recommend yes; it reverses the 2026-09-05
  fold-in on the supervisor's explicit ask.
- **R2 — The second mark for flow B.** The greys ruling permits one accent.
  Options: (a) a second hue for this figure only, recorded in
  `figure_table_conventions.md` §i as a scoped exception — recommended,
  because the supervisor asked for exactly two colours and the two-flow trace
  *is* the message; (b) stay mono: flow A accent-filled, flow B accent-outlined,
  shared nodes filled with a ring. (b) keeps the rule but is subtler than the
  audience he is designing for.
- **R3 — Profile labels.** Recommend the chapter's objective names without
  counts; "Profile 1–4" would put a name in the figure that the prose never
  uses.
- **R4 — Pair selection.** Recommend the by-rule pick above (real flows,
  chosen by a stated rule) over invented schematic flows, so the figure stays
  artefact-backed and the caption can name the two incidents.
- **R5 — Authoring route.** Recommend HTML/SVG per the 2026-08-27 ruling.
- **R6 — Page.** Recommend a portrait `[p]` page for the ladder (it is
  vertical) and `\textwidth` for the loop; landscape buys width the ladder
  does not need.

## Validation gate

- Both PDFs build at natural size with no glyph under 8 pt (the generator
  prints the smallest size, as `mtdsim_model_figure.py` does).
- The generator refuses to build if the selected flow pair no longer
  satisfies the rule, if the tactic order differs from the GAP's, or if the
  net fragment's places and transitions are not in the structural JSON.
- `dissertation.tex` builds clean with `fig:pipeline` still resolving (the
  label and the four `\ref`s at lines ~3575, ~3732, ~4551 survive) and the new
  `fig:runtime-loop` referenced from `subsec:mechanics-join`.
- `docs/thesis/FLOATS.md` updated: fig_4-0a rebuilt, the new 4-4 letter
  assigned, `pipeline_ladder_figure.py` retired or reduced to the fact sheet.
- The test that matters is not in the build: Marc shows the page to someone
  outside the project and they can say what each arrow does.

## Hard constraints

- Thesis ladder numbering only (L0–L4 as the chapter defines them, evaluation
  carries no number); never the repo's numbering
  (`architecture.md` (b)).
- Shared tactic axis in kill-chain order, never reordered (§b6).
- No hard-coded corpus facts in the tool: flow choice by rule, names mapped
  in the generator, numbers from artefacts.
- Greys + one accent unless R2(a) is ruled; house figure sans; 8 pt floor;
  caption decodes every encoding (§b2) and states the pins (§b5).
- The caption is Marc's to write (his own prompt, per the tex comment above
  the float); a session may leave a minimal accurate stand-in.
- Branch, commit locally, never push.

## Reading list

- `tools/pipeline_ladder_figure.py` — the current generator; `emit()`'s
  controller and action bands are reusable for the loop figure.
- `tools/mtdsim_model_figure.py` + `tools/mtdsim_model_figure.html` — the
  HTML/SVG pattern (validation, floor check, Chromium print).
- `docs/thesis/dissertation.tex` lines ~3530–3577 — the float, its preamble
  comments and the caption slot; ~4551 for the joins cross-reference.
- `docs/workflows/figure_table_conventions.md` §b, §d, §g, §h, §j, §l.
- `docs/handoffs/__archive/2026-08-27_ch2_model_diagram_plan.md` —
  the rulings that shaped fig_2-2a.
- `data/gap/gap_v0.5.json` (`flow_ids` on nodes and edges),
  `data/gasp/classification.csv` (objective class per flow),
  `data/ogasp/petri/*_structural.json` (net fragment).

## Out of scope (explicitly)

- Redrawing fig_4-3a (the GSPN gadget), fig_4-4a/b, or the appendix graphs.
- Rewriting the §4 preamble prose; only the figure sentence and the new
  cross-reference to the loop figure change.
- Writing the two captions beyond a stand-in.
