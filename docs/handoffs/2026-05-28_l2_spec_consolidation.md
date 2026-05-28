---
status: open
created: 2026-05-28
---

# Consolidate the L2 / GASP investigation into a canonical spec — accept P6 as the GASP construction

The L2 partition investigation has landed five durable notes under
`docs/notes/` and zero canonical specs under `docs/specs/`. The GAP has
both: a spec ([`../specs/01_gap_schema.md`](../specs/01_gap_schema.md))
*and* a construction note
([`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)),
and the symmetry is load-bearing — the spec is what the implementation
points to and what new sessions read; the note is the plain-English
companion that records *how it came to be*. L2 has the notes but is
spec-less.

**Marc has greenlit P6** (compound-class disjoint, surface subgraph,
audit-attested) as the **accepted GASP construction**. The investigation
is over; this handoff consolidates the outcome into one spec and one
companion note, and demotes the investigation-history notes to provenance
status. *Future work should not reference "P6" — it should reference the
GASP construction. The "P6" framing is investigation-time terminology
that has now retired.*

## State of play

**What exists today** (gitignored / committed status as noted):

- [`../notes/2026-05-28_l2_partition_reasoning.md`](../notes/2026-05-28_l2_partition_reasoning.md) —
  why L2 exists and which axis it slices on. *Provenance: framing-stage.*
- [`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md) —
  the P6 verdict with rubric + discrimination + audit + "if revisited".
  *Provenance: decision artefact.*
- [`../notes/2026-05-28_l2_per_flow_justifications.md`](../notes/2026-05-28_l2_per_flow_justifications.md) —
  per-flow class assignments + citations + critique + verification round.
  *Provenance: audit defence.*
- [`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv) —
  the 38-row audit-traced classification data. *Provenance + source of
  truth for L2 implementation membership input.*
- [`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md) —
  the 3-Conti / 2-Turla / 3-CISA operator-clustering concern + four
  candidate mitigations. *Provenance: methodological caveat.*

**What doesn't exist** (what this handoff writes):

- `docs/specs/02_gasp_schema.md` — the canonical L2 spec, mirroring
  [`01_gap_schema.md`](../specs/01_gap_schema.md)'s structure. The
  authoritative *"what GASP is"* document.
- A companion note `docs/notes/<YYYY-MM-DD>_gasp_construction.md` if
  the consolidation surfaces narrative material that doesn't fit the
  spec (mirroring how [`gap_construction.md`](../notes/2026-05-27_gap_construction.md)
  sits alongside `01_gap_schema.md`). **Optional** — only if there's
  material from the investigation notes that's load-bearing for *how*
  the GASP is read but doesn't belong in the spec proper.
- Updates to [`../specs/architecture.md`](../specs/architecture.md) §(e)
  retiring the terminal-node-ancestor proxy language and naming the
  new spec.

## Recommended approach

A single consolidation session. The five notes already contain the
material; this handoff is structural — distil + re-cross-link + retire
investigation-only framing.

### Tasks

1. **Read all five L2 notes end-to-end.** They have overlap; the
   consolidation needs to be explicit about which content stays where.

2. **Draft `docs/specs/02_gasp_schema.md` matching the structure of
   `01_gap_schema.md`.** Suggested sections (adapt as the content
   suggests):

   - `(a)` **Purpose and the central invariant.** GASP slices GAP by
     analyst-stated operational objective, sourced from CTI narrative.
     The central invariant: *every class membership corresponds to an
     objective the analyst stated, not an objective inferred from
     graph structure.* (Mirrors GAP's "every edge corresponds to a
     dependency a human analyst drew" invariant.)
   - `(b)` **The construction decisions.** Five candidate-set / mechanism
     decisions to record, with **Why** and **If revisited** for each:
     1. Slice axis = operational objective (vs motivation).
     2. Class set = `{pure_steal, pure_impediment, double_extortion, infrastructure_setup}` (vs Alshamrani 3-goal NIST baseline).
     3. Class membership mechanism = analyst-stated narrative
        (audit-traced), not structural-terminal.
     4. Class subgraph definition = surface (techniques present in
        class flows; no ancestor closure).
     5. `infrastructure_setup` renames Alshamrani's `position_for_future`
        because this corpus has 0 surveillance flows.
   - `(c)` **Class-membership table.** The 38-row mapping `flow_id → class`.
     Reference the audit CSV as the source of truth; embed the per-class
     flow-list compactly for readability.
   - `(d)` **Class subgraph computation.** The surface-subgraph algorithm
     (union of per-flow technique sets, GAP edges where both endpoints
     are in the union). Reference the L2 implementation when it lands.
   - `(e)` **Views.** What downstream consumers (L3, L4, Petri-net)
     receive from each class. The L2 boundary object is `SubgraphView`
     (`node_set`, `edge_set`, `provenance`) — mirrors L1's lossless
     edge metadata.
   - `(f)` **Build pipeline summary** — pointer to
     `src/mtdsim/l2_subgraph/` once it exists; describes the
     `(gap, operational_objective) → SubgraphView` contract.
   - `(g)` **Validation.** Mirrors GAP's validation: the no-synthesis
     check (every class membership has audit-CSV provenance), the
     Enterprise-scope check (every class subgraph node resolves in
     `gap['nodes']`), and the *discrimination-above-null* check (mean
     pairwise technique-JSD > null p95).
   - `(h)` **Open questions** — the items still unresolved (e.g. the
     ToolShell flow-split question; the operator-aggregation mitigation
     choice; whether to add `monetisation` as a fifth class).
   - `(i)` **Relationship to other specs.** Pointers to architecture
     `§(e)`, the GAP schema, the per-flow audit CSV, the operator-
     aggregation concern note.

3. **Update [`../specs/architecture.md`](../specs/architecture.md) §(e)**
   to reflect the accepted spec:
   - Retire the *"motivation specifier `{espionage, disruption,
     financial}`"* prose; replace with *"operational-objective
     specifier `{pure_steal, pure_impediment, double_extortion,
     infrastructure_setup}`"*.
   - Retire the *"terminal-node-ancestor proxy"* description; the new
     proxy is *surface subgraph from audit-traced membership* — point
     to the new spec.
   - Update the §(e) decision block. The current decision text says
     *"If the comparative pass shows motivation-by-attribution matters
     more than motivation-by-terminal-node, swap in the NLP path"*.
     The decision now is: *audit-traced metadata attestation is the
     accepted mechanism; structural-terminal is documented as the
     dropped P1 candidate (see provenance notes).*
   - Add the new spec to §(m) Related specs.

4. **Demote the five investigation notes to provenance status (don't
   delete).** They retain their dissertation-source value but are no
   longer the *authoritative* source on GASP construction. Two ways to
   do this:
   - **Light touch** (recommended): add a banner at the top of each
     investigation note saying *"This note records the investigation
     that produced GASP. The canonical spec is now at
     [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md). Read
     this for *why* GASP exists / *how* the decision was reached;
     read the spec for *what GASP is*."* — keeps the notes intact for
     provenance, makes the new spec the entry point.
   - **Heavier touch** (not recommended): consolidate the five notes
     into one *"GASP — investigation history"* note. Loses dissertation-
     citation value (the five notes' separate dates + topics are
     citation-relevant). Don't do this.

5. **Consider** writing a thin construction-note companion at
   `docs/notes/<date>_gasp_construction.md` if material from the five
   investigation notes is *plain-English-companion to the spec* (i.e.
   reads as "here's GASP in normal English") rather than *investigation
   history* (i.e. "here's how we decided"). Be selective — only write
   it if there's a clear chunk that fits the
   [`gap_construction.md`](../notes/2026-05-27_gap_construction.md)
   archetype. If everything from the investigation notes is
   "how we decided" / "what was contested", skip this — the spec is
   sufficient.

### Alternatives considered

- *Skip the spec; just leave the notes as authoritative.* Rejected.
  The project's convention (per [`repo_conventions.md`](../specs/repo_conventions.md))
  is that *specs are the canonical layer*; notes are dissertation
  source. Without a GASP spec, L2 implementation has no canonical
  contract to point to; future sessions would chase the notes' overlap.
- *Write the spec from scratch, ignoring the notes.* Rejected. The
  notes already contain the load-bearing material — re-writing risks
  losing the audit-CSV provenance + the per-flow defensibility.
- *Update `01_gap_schema.md` to cover L2 too.* Rejected. The GAP spec
  is L1-scoped by design; conflating L1 + L2 in one spec loses the
  pipeline-stage symmetry.

## Validation gate

Done when:

1. `docs/specs/02_gasp_schema.md` exists, follows the structure above
   (or a defended variation), and reads as a peer of
   `01_gap_schema.md` to a cold reader.
2. The five investigation notes have provenance banners pointing to
   the new spec.
3. [`../specs/architecture.md`](../specs/architecture.md) §(e) is
   updated — motivation prose retired, the new spec named, the
   decision block rewritten.
4. [`../specs/architecture.md`](../specs/architecture.md) §(m) lists
   the new spec.
5. Cross-links from the new spec to the five notes are present (the
   spec doesn't *contain* their content, it *references* them for
   provenance).
6. **The spec carries the L2 corpus numbers** (38 flows, 19:8:6:5 class
   counts, mean technique-JSD 0.317) so a reader gets the headline
   without digging into the audit CSV.
7. The architecture §(e) decision block has the new `If revisited:`
   line — e.g. *"If a corpus expansion or simulator-verification step
   reveals operator-aggregation is dominating per-class discrimination,
   re-open the spec against the operator-aggregation concern note's
   four mitigations."*
8. This handoff is deleted in the same commit that ships the spec.

## Critique

Five potential traps:

- **Don't re-litigate P6 in the spec.** The spec records the *accepted*
  GASP construction. The dropped candidates (P1, P2, P3, P4, P5, P7) go
  in the **decision** block under "Why P6 was chosen / If revisited"
  (one line each), *not* as separately-defended alternatives in the
  body. Provenance for the dropped candidates lives in the
  partition-decision note.
- **Don't drop the operator-aggregation caveat.** The spec's §(g)
  validation block should explicitly carry the *discrimination-above-null
  with operator-deduplicated re-check* gate. Otherwise the spec reads
  as if discrimination is settled when it's settled-on-the-current-
  corpus-with-known-clustering.
- **Don't over-promise on `infrastructure_setup`.** The renamed class
  is *not* Alshamrani's `position_for_future`. It's "pre-payload
  operations the analyst-stated narrative names as not-yet-objective-
  realised". The spec should be precise about this — *not* leave
  readers thinking pre-positioning surveillance APTs land here (none
  in this corpus do).
- **Don't write the construction-companion note if there's nothing to
  put in it.** The temptation is to mirror the GAP's
  spec-plus-construction-note pairing. But the L2 investigation already
  produced FIVE companion notes. Writing a sixth just for symmetry is
  duplication. Skip unless there's plain-English content that doesn't
  fit any existing note.
- **The "future work needn't reference P6" framing risks erasing
  history.** Spec text should say *"the GASP construction"* (no P6).
  But the decision block needs to keep the *"P6 was the
  investigation-time name for this construction"* sentence — otherwise
  the provenance trail from the notes (which heavily reference P6) is
  broken. One sentence, in §(b) decision text.

## Hard constraints

- Branch hygiene as ever — dedicated session branch, no push.
- The spec is the *new* authoritative source. The notes are
  *provenance*. Don't edit the notes' content (only add the
  provenance banner at the top).
- The new spec is `docs/specs/02_gasp_schema.md` (not
  `02_gasp.md` or similar) — mirrors `01_gap_schema.md`.
- Australian English throughout.

## Reading list

In order:

1. **[`../specs/01_gap_schema.md`](../specs/01_gap_schema.md)** —
   the structure template the new spec mirrors.
2. **[`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)** —
   the load-bearing source for the spec body.
3. **[`../notes/2026-05-28_l2_partition_reasoning.md`](../notes/2026-05-28_l2_partition_reasoning.md)** —
   the *why* framing the spec's §(a) condenses.
4. **[`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv)** —
   the source of truth for §(c) class-membership.
5. **[`../notes/2026-05-28_l2_per_flow_justifications.md`](../notes/2026-05-28_l2_per_flow_justifications.md)** —
   the *defensibility* of §(c).
6. **[`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md)** —
   the validation-gate caveat for §(g).
7. **[`../specs/architecture.md`](../specs/architecture.md) §(e), §(m)** —
   the integration points to update.

## Out of scope

- Implementation of `src/mtdsim/l2_subgraph/` — handoff
  [`./2026-05-28_l2_implementation.md`](./2026-05-28_l2_implementation.md).
  This handoff defines *what to build*; that handoff builds it.
- Visualisation iteration — handoff
  [`./2026-05-28_l2_viz_iteration.md`](./2026-05-28_l2_viz_iteration.md).
- Project-context-level updates (CLAUDE.md, project_context.md) —
  handoff [`./2026-05-28_l2_assembly_audit.md`](./2026-05-28_l2_assembly_audit.md).
- Re-running the metadata audit or the discrimination check — the
  audit-traced CSV stands.
- Editing the investigation notes' content (banner-only edits OK).
