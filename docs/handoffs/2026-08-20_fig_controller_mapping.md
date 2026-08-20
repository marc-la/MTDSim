---
status: open
created: 2026-08-20
---

# The controller-mapping figure — tactic-to-verb bipartite (§4.2.4.1)

**Goal:** generate the tactic→verb mapping figure for the ruled slot at
§4.2.4.1 (tex comment ~l.730) and wire the prose's existing "You can see this
in the diagram provided" to a real `\ref`. **(Ruled 2026-08-20: in — the
mapping diagram adds to the argument.)**

## Source and state

- **The tracked artefact:** `data/ogasp/controller/mappings/v2_partial.csv`
  (+ `manifest.json`) — 8 mapped tactics / 7 dwell-only of 15; per-row
  disposition and reason columns.
- `data/misc/_viz/controller_mapping/*.png` are diagnostic-grade —
  **composition reference only**, never promoted.

## Spec

- Bipartite: the 15 tactics on one side **in the shared tactic-axis order**
  (never reordered, conventions §b6), the substrate verbs on the other; edges
  = the mapping.
- **The dwell-only tactics are the figure's argument** — the visible gaps are
  what the prose leans on ("there are many dwell-only tactics" — the action
  layer's coverage concession). Render them unmistakably (grey class or absent
  edge), decoded in the caption. This is the one legitimate use of emphasis:
  the thing the figure is about.
- Caption states the mapping pin (`v2_partial`) and the zero-or-one constraint
  in a sentence; multi-sentence decode expected (§b2).

## Considerations

1. **Australianisation ruling first** — tactic labels appear verbatim here;
   the open "Defense impairment" ruling (2026-08-17) must be taken once before
   this and every other tactic-labelled figure is generated.
2. **Presentation names in the generator spec, never hard-coded corpus facts**
   (the mechanism-not-exception ruling applies to figure tooling).
3. **Verb names are presentation names too** — `SCAN_HOST` etc. are raw code
   identifiers, a named corpus anti-pattern (§g); map to domain terms in the
   generator (e.g. "host scan"), decoded in the caption if abbreviated.
4. The mapping-swap-as-experiment point stays in `sec:experimental-setup`
   (already ruled) — this figure does not carry it.

## Validation gate

Figure wired at a real label from the §4.2.4.1 prose sentence; `v2_partial`
pinned in the caption; no raw identifier in the figure; print-size check
passed; caption listed for Marc's voice pass.

## Reading list

1. [`2026-08-20_section42_figures_tables_appendix.md`](2026-08-20_section42_figures_tables_appendix.md)
2. [`../workflows/figure_table_conventions.md`](../workflows/figure_table_conventions.md) §b, §g
3. `data/ogasp/controller/mappings/v2_partial.csv` + `manifest.json`
4. [`../implementation/pipeline/ogasp/controller.md`](../implementation/pipeline/ogasp/controller.md) — the mapping's record
