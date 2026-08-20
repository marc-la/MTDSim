---
status: open
created: 2026-08-20
---

# The model / data-flow diagram — §4.2's primary figure

**Goal:** design and generate the ruled `[data-flow]` figure (§4.2.4.2, tex
comment ~l.844): the movement attacker's runtime loop drawn as a
process/data-flow diagram, wired at a real label replacing `Figure~[data-flow]`.

## Spec (Marc's 2026-08-20 dictation + the ruled slot comment)

- **Top:** the GSPN / movement layer (a schematic net — places, transitions,
  token — per Petri grammar §d5; *not* a full profile net, which L3 was ruled
  not to draw).
- **Bottom:** the MTDSim substrate, with the attacker model drawn as one of
  three interacting components (attacker / defender / network).
- **Middle — the controller layer:** the three declared inputs as abstract
  glyphs: dwell-time catalogue (data file), failure matrix (small matrix),
  tactic-to-verb mapping (small bipartite graph).
- **Arrows trace the loop:** token selects tactic → mapping resolves dwell-only
  *or* verb → simulator executes and consumes the drawn stochastic time →
  success/failure verdict propagates up → failure weight set multiplied onto
  the token's out-transitions → next tactic.
- Grey ramp + one accent, consistent with `fig:l1-graph` / the failure figures.

## Considerations (surfaced 2026-08-20 — encode in the drawing)

1. **Icon-genre boundary.** Conventions §d9 bans icon/scenario clip-art. Marc's
   "little icons" are fine only as abstract geometric glyphs (a small grid for
   the matrix, a small bipartite pair for the mapping, a bracketed list for the
   catalogue) — nothing pictorial.
2. **Directionality precision.** The tactic-to-verb *mapping* is one-way; what
   makes the join two-way is the **verdict return edge**. Draw the mapping as a
   downward resolve and the verdict as the upward edge — never a bidirectional
   mapping arrow (the dictation's "two-way mapping" compresses the join, and
   the drawing must not repeat the compression).
3. **The dwell-only branch must appear**: mapping resolves to *no verb*, time
   is consumed, **no verdict returns** — the concession the prose owns ("not
   felt by the token"). A loop drawn verdict-always would contradict the text
   beside it.
4. **The confusion penalty stays out of the drawing** (recommended): it is the
   substrate-side timing exception the prose owns; drawing it would clutter the
   loop. If Marc wants it acknowledged, the caption is the place.
5. **Placement is Marc's call**: the ref lives in Mechanics; if the float also
   serves the section opening, the caption does more definitional work — raise
   the caption's stakes accordingly.

## Approach

New `tools/` generator → 12pt standalone TikZ into `docs/thesis/figures/`.
Caption long and self-contained, decoding every glyph and edge class (§b2),
session-drafted and flagged for Marc's voice pass. Cross-cutting rules
(caption pipeline, pins, Australianisation) in the parent inventory handoff.

## Validation gate

`Figure~[data-flow]` replaced by a real `\ref`; figure compiles and passes the
print-size check (no glyph under ~8pt equivalent at inclusion width); the three
considerations above visibly honoured; caption listed for Marc's voice pass.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md) — the ruled inventory + cross-cutting rules
2. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §b, §d1, §d5, §h
3. `docs/thesis/dissertation.tex` — the `[data-flow]` slot comment and the Mechanics prose it must match
4. [`../implementation/architecture.md`](../implementation/architecture.md) §(f) — movement / controller / action layers
5. `docs/thesis/figures/l1_attack_graph.tex` — canonical style block
