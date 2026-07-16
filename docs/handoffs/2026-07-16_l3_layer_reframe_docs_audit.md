---
status: open
created: 2026-07-16
---

# Reconcile the layer vocabulary — formalise the movement/controller/action runtime decomposition alongside the L0–L4 build pipeline, audit the docs for stale rigid-layer and replay-era encodings, and amend where they now mislead

> **Motivation (Marc, 2026-07-16).** Post-M1, the pipeline reads differently:
> GAP→OGASP is really one unified **movement layer** that controls the attack
> model; the timeline "layer" was never a layer (no two-way communication —
> it was an artefact); and OGASP's live half is really a **controller layer**
> between movement and the inherited **action layer** (the FSM phases).
> Prior docs encoded the layers rigidly around the replay-era shape; some of
> that is now stale. This handoff formalises the new vocabulary, decides how
> it coexists with L0–L4, and sweeps the stale encodings.
>
> **The recommended resolution — two orthogonal views, overlay not renumber.**
> L0–L4 is a **build-time data-flow** view: how the movement layer's
> artefacts are constructed (CTI → GAP → GASP → weighted nets). Movement /
> controller / action / substrate is a **runtime execution** view: how the
> profiled attacker runs. They are views of the same system, not competing
> numberings — GAP/GASP are the movement layer's *provenance*, not separate
> runtime components, and the substrate is not "L5" (evaluation L4 consumes
> runs *on* the substrate; putting a runtime component downstream of
> evaluation muddles the data-flow reading). Recommend: keep L0–L4 for
> construction, introduce the runtime stack as first-class vocabulary in
> architecture §(f), and cross-reference. The renumbering alternative
> (substrate as L5) stays on the table for Marc to overrule — but it touches
> data dirs (`data/gap|gasp|ogasp`), code paths (`l3_simulation`), and every
> chapter note that says "L3", for a mostly nominal gain.

## State of play

- **Already done (2026-07-15 commit):** architecture §(f) status/ledger/
  transformation rewritten for the live coupling; D2 annotated; grounding
  program and binding record bannered; register carries M1–M8. The *replay
  framing* is largely cleaned; the *layer vocabulary* is not yet formalised.
- **The runtime stack, as currently understood:**
  - **movement layer** — the live class net: token, D3 base weights, M2
    conditional sets, M3 direction, termination. Built by L0→L3a.
  - **controller layer** — the new, previously unnamed thing the meeting
    created: tactic→action dispatch (M5), parameterisation over the action
    layer's affordances, and the outcome-oracle adapter (M2/M4). "The best
    we can do with the tools at hand."
  - **action layer** — the inherited attack module: the six verbs, their
    chaining/state/interrupt machinery. Anatomised by
    [`./2026-07-16_l3_action_layer_anatomy.md`](./2026-07-16_l3_action_layer_anatomy.md).
  - **substrate** — network/host/service/vulnerability terrain + MTD
    mechanisms + statistics, unchanged (D5).
- **Known audit surface** (from a first grep; the sweep must be its own,
  fresh): [`../workflows/project_context.md`](../workflows/project_context.md)
  (L16-17 defines L3 OGASP as "attacker-agent traversal" and names the
  attacker-module seam), [`../workflows/docs_map.md`](../workflows/docs_map.md)
  (architecture one-liner), [`../implementation/architecture.md`](../implementation/architecture.md)
  (the L0→L4 spine and §(f) ledger — the natural home of the runtime stack),
  [`../implementation/substrate_primer.md`](../implementation/substrate_primer.md)
  (§(f) contribution boundary), [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md),
  [`../implementation/pipeline/gap/gap_schema.md`](../implementation/pipeline/gap/gap_schema.md) /
  [`../gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) /
  [`../ogasp/petri_feasibility.md`](../implementation/pipeline/ogasp/petri_feasibility.md)
  (stage one-liners), plus `ch3_design` notes that narrate the pipeline
  (`structure_to_behaviour_binding.md` especially — its encoding ledger
  speaks the binding-era language).
- **Investigation records are immutable history** — they get status banners
  where stale, never rewrites (docs_map contract). Living specs
  (architecture, project_context, docs_map, schemas' framing sentences) get
  amended in place with `updated` bumps.

## Recommended approach

1. **Write the vocabulary once, in architecture §(f).** A short "runtime
   stack" block defining movement/controller/action/substrate, their
   contracts, and the sentence reconciling them with L0–L4 (build-time vs
   runtime view). Everything else links here rather than redefining.
2. **Decide overlay-vs-renumber with Marc's sign-off.** The recommendation
   above is overlay; put the renumber option and its blast radius in one
   paragraph so the decision is on the record (architecture decisions log).
3. **Sweep fresh.** Grep-driven pass over `docs/` (excluding `sources/`)
   for: replay/one-way/timeline-as-input residue; "L3" definitions that
   describe OGASP as timeline generation or binding; rigid layer language
   that contradicts the runtime stack. Classify each hit: amend (living
   spec) / banner (investigation record) / leave (historical, already
   bannered, or accurate).
4. **Amend and bump.** Apply the classification; `updated` bumps in the
   same commit; note-level changes must survive the notes rubric if any
   `notes/` file is touched (load it first).

*Alternatives considered:* renumbering to L5 — see banner; kept as the
alternative for Marc to choose against the stated blast radius. Doing the
sweep opportunistically per-session — rejected: exactly how the stale
encodings accumulated; one deliberate pass with a classification table is
cheap and terminal.

## Validation gate

Done when:
1. Architecture §(f) carries the runtime-stack definition and the
   build-vs-runtime reconciliation sentence; the decisions log records the
   overlay-vs-renumber choice with the alternative's cost stated.
2. The sweep's classification table exists (in the handoff-closing commit
   message or a short section of the architecture decisions log — not a new
   doc): every hit → amend / banner / leave, with the leaves justified.
3. All amend-class hits are amended, `updated` bumped, links resolving.
4. No investigation record was rewritten — banners only.
5. Marc has reviewed, and specifically signed the overlay-vs-renumber call.

## Hard constraints

- **Docs only** — no code, no data-dir renames (even if renumber is chosen,
  the rename is separate, sequenced work).
- **Immutable investigation records** — banner, never rewrite
  ([`../workflows/docs_map.md`](../workflows/docs_map.md) implementation
  contract).
- **Notes touched → rubric loaded** ([`../workflows/notes_rubric.md`](../workflows/notes_rubric.md));
  voice contract for any dissertation-bound prose.
- **Register untouched except cross-references** — M1–M8 wording is the
  supervisor record; this reframe is Marc-driven vocabulary, not a ruling.
- Branch hygiene; **never push without an explicit ask**; Australian
  English.

## Reading list

- [`../implementation/architecture.md`](../implementation/architecture.md)
  — the L0→L4 spine and §(f) as-committed 2026-07-15; the home of the fix.
- [`../workflows/project_context.md`](../workflows/project_context.md) +
  [`../workflows/docs_map.md`](../workflows/docs_map.md) — the always-loaded
  definitions that must not drift from architecture.
- [`../notes/ch3_design/structure_to_behaviour_binding.md`](../notes/ch3_design/structure_to_behaviour_binding.md)
  — the most binding-era-shaped note; likely the hardest classification
  call.
- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  §M1–M8 — the rulings the vocabulary must express, not reinterpret.

## Out of scope (explicitly)

- The action-layer anatomy (its own handoff, runs parallel).
- Executing a renumber (dirs/code/notes) if Marc chooses it — separate
  handoff, written then.
- Dissertation chapter prose — the vocabulary lands in specs/notes framing
  only.
