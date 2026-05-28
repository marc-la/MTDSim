---
status: open
created: 2026-05-28
---

# Audit the assembled L2 work — connections, locations, project context, simplifications

After the three load-bearing L2 handoffs land (viz iteration, spec
consolidation, implementation), the L2 work is **done in pieces but not
necessarily well-connected**. The notes were written iteratively, the
spec consolidates them, the implementation realises them, but nobody
has gone through the assembled set and asked *"would a cold reader find
this coherent? do the cross-links resolve? is there anything stale,
duplicated, or in the wrong directory?"*. This handoff is that pass.

**Run this last.** It depends on the other three having landed (or at
least having been substantially attempted) so the audit has a stable
target.

## State of play

**What should exist when this handoff runs:**

- `docs/specs/02_gasp_schema.md` — canonical L2 spec (from
  [`./2026-05-28_l2_spec_consolidation.md`](./2026-05-28_l2_spec_consolidation.md)).
- `src/mtdsim/l2_subgraph/` built out as a real package (from
  [`./2026-05-28_l2_implementation.md`](./2026-05-28_l2_implementation.md)).
- `data/gasp/_viz/` populated with iterated viz outputs (from
  [`./2026-05-28_l2_viz_iteration.md`](./2026-05-28_l2_viz_iteration.md));
  `data/gasp/` populated with the L2 build outputs.
- 5 investigation notes in `docs/notes/` with provenance banners.
- [`../specs/architecture.md`](../specs/architecture.md) §(e) updated
  to name the new spec.
- The three handoffs above deleted on their respective land commits.

**What this handoff checks:** everything ties together and is in the
right place.

## Recommended approach

A focused audit session. Treat the L2 work as the target; the audit
output is a checklist of *what's already coherent* and *what needs a
small fix*. Use small commits to land each fix; don't bundle this
handoff's work into a single mega-commit — that loses the audit-trail
value.

### Audit checklist

For each item below, the session records *PASS* / *FIX (with link
to the commit)* / *DEFER (with reason)* in the assembled-audit note
the validation gate requires.

#### 1. Cross-links resolve

- [ ] Every relative link in `docs/specs/02_gasp_schema.md` resolves.
  (`grep -oE '\]\([^)]+\)' docs/specs/02_gasp_schema.md` then check
  each.)
- [ ] Every relative link in the five investigation notes resolves
  (especially the new provenance-banner pointer to the spec).
- [ ] The L2 README (`src/mtdsim/l2_subgraph/README.md`) points to
  the spec at `docs/specs/02_gasp_schema.md`, not at the verdict
  note.
- [ ] [`../specs/architecture.md`](../specs/architecture.md) §(e) and
  §(m) reference the new spec.
- [ ] [`../specs/repo_conventions.md`](../specs/repo_conventions.md) §"Specs"
  table includes `02_gasp_schema.md` if the convention is to list each
  spec there (it currently lists `01_gap_schema.md`).
- [ ] CLAUDE.md "Spec files (load when relevant to the task)" section
  mentions `02_gasp_schema.md`.

#### 2. File locations are right

- [ ] `data/gasp/` exists with `classification.csv` + per-class JSONs
  + `_viz/` + README.
- [ ] `data/gap/_viz/gasp_*` is removed (the viz iteration handoff
  was supposed to move these — confirm no leftovers).
- [ ] No `2026-05-28_l2_*` files in `notebooks/` (the investigation
  decided no notebook; check no stray one was created during
  implementation).
- [ ] No L2 artefacts under `src/mtdsim/l2_subgraph/` that should be
  data (e.g. CSVs or JSONs accidentally committed alongside the code).
- [ ] No `data/gap/` files that should be `data/gasp/` (specifically
  check for stragglers from the viz move).

#### 3. Project context is current

- [ ] [`../specs/project_context.md`](../specs/project_context.md) L16
  pipeline summary mentions L2 GASP — currently it says *"L2 GASP
  (motivation subgraph)"*; should be updated to *"L2 GASP
  (operational-objective subgraph)"* per the new spec.
- [ ] [`../specs/architecture.md`](../specs/architecture.md) §(e)
  uses operational-objective language throughout (not motivation),
  and the §(e) decision block reflects the accepted GASP construction
  rather than the proxy.
- [ ] [`../specs/architecture.md`](../specs/architecture.md) §(j)
  methodology positioning prose acknowledges the L2 partition is
  audit-traced from CTI narrative (the *behaviourally-grounded* claim
  now has a concrete mechanism — point to it).
- [ ] [`../specs/architecture.md`](../specs/architecture.md) §(l)
  open questions block — *"motivation-attribution method"* and
  *"NLP path"* items are **closed** by the partition decision; remove
  or move to a "resolved" subsection.

#### 4. Notes hygiene

- [ ] All five investigation notes have provenance banners pointing
  to the spec.
- [ ] None of the notes reference *future-tense* L2 work (e.g.
  *"the next session will implement..."*) — by audit time, that work
  has happened. Rewrite future-tense to past-tense or
  current-state where appropriate. (Light touch — the notes are
  provenance, but don't leave them misleading.)
- [ ] No duplication between notes — e.g. the verdict note and the
  per-flow note both record the audit distribution; make sure one
  cites the other rather than recomputing.
- [ ] `MEMORY.md` (if it has entries about L2 being in-progress) is
  current. *Skim user-memory if relevant.*

#### 5. Test + build are clean

- [ ] `PYTHONPATH=src python -m mtdsim.l2_subgraph` runs without
  error and produces the GASP artefacts.
- [ ] `PYTHONPATH=src python -m pytest tests/gap/ tests/l2_subgraph/ -q`
  passes.
- [ ] Re-running the L2 build is byte-stable (deterministic outputs).
- [ ] `data/gasp/_viz/gasp_viz.py` regenerates the viz outputs cleanly.

#### 6. Simplifications + refactors

Look for:

- [ ] *Duplication between `01_gap_schema.md` and `02_gasp_schema.md`*
  — e.g. both describing the per-flow YAML format. The GASP spec
  should *reference* the GAP spec for that, not re-describe it.
- [ ] *Stale references to v0.4 prior art branches.* All `feat/replay-viz`
  and `feat/attacker-profiling` references should either (a) be in
  the per-flow YAML metadata where the historical lineage is
  load-bearing, or (b) be removed because the L2 implementation is
  now fresh-coded.
- [ ] *Naming inconsistency* between the audit CSV's `stated_objective`
  values (`steal_data`, `impediment`, `double_extortion`,
  `position_for_future`) and the spec / code class names
  (`pure_steal`, `pure_impediment`, `double_extortion`,
  `infrastructure_setup`). The mapping is documented but the four
  pairs of names are an avoidable cognitive tax. **Recommendation**:
  either rename the audit CSV columns to match the code class names,
  or rename the code classes to match the audit columns. The
  asymmetry is technical debt; *if* this handoff has session
  budget for the refactor, do it; otherwise add a "rename pass"
  follow-up handoff.
- [ ] *The two `infrastructure_setup` CISA flows with `low`
  confidence* — would the CISA URL be reachable via a non-WebFetch
  fetcher (curl, requests with a User-Agent header)? If yes, retry
  the audit for those two flows and either confirm `low` is the
  right call or upgrade to `medium` / `high`. This is a one-off
  re-verification, not a re-audit; bounded scope.

#### 7. Provenance of dropped candidates

Per Marc's directive — *"investigation of other approaches should
already be documented in docs/ somewhere for the purposes of
provenance"*:

- [ ] The 6 dropped candidates (P1–P7 except P6 — P3 and P4 were
  dropped pre-rubric; P1, P2, P5, P7 were scored and ranked) each
  have a record in the partition-decision note. Verify each
  candidate is named, its mechanism described, and its drop reason
  stated.
- [ ] The 5-criterion rubric provenance (Part 8 hand-assigned vs
  Part 15 data-driven; the v0.4 notebooks at
  `git show origin/feat/replay-viz:notebooks/...`) is recorded
  somewhere — verdict note's rubric section is the natural home.
- [ ] The 4 rejected terminal definitions (A walked, B strict, C
  YAML-tactic, D any-occurrence) and the working choice (A) are
  recorded — verdict note's *Discrepancy with handoff* section.

### Alternatives considered

- *Skip this audit and trust the three preceding handoffs are
  internally consistent.* Rejected. The preceding handoffs each have
  their own scope; cross-cutting consistency is exactly the gap
  this handoff fills. Skipping it leaves the project's L2 layer
  defensible-piece-by-piece but vulnerable to a *"how does this
  hang together?"* defence question.
- *Make this handoff bigger — do simplifications + refactors at
  scale.* Rejected. The audit is for *coherence*, not for
  refactor-as-cleanup. Real refactors (e.g. the class-name
  symmetry) go in dedicated follow-up handoffs if they exceed
  one-line fixes.
- *Roll the audit into the implementation or spec-consolidation
  handoff.* Rejected — those handoffs are already substantial; the
  audit needs to *see* both completed before it can run.

## Validation gate

Done when:

1. Every line on the audit checklist above has a recorded outcome
   (PASS / FIX:<commit> / DEFER:<reason>).
2. The recorded outcomes land in a one-paragraph audit note at
   `docs/notes/<YYYY-MM-DD>_l2_assembly_audit.md`. (Yes, a sixth
   L2-related note — but this is structurally different: it's the
   *audit outcome*, not investigation history.)
3. Any FIX:<commit> items have actually landed as commits.
4. Any DEFER:<reason> items have a follow-up handoff opened (if the
   defer is non-trivial) or a single-line note in the audit note (if
   the defer is "not worth doing").
5. CLAUDE.md no longer has stale L2-references (specifically the
   *"L2 GASP construction is a later work item"* framing in the L2
   README is updated; if CLAUDE.md mentioned the partition
   investigation as in-progress, that's updated too).
6. The user-memory file `MEMORY.md` doesn't carry stale
   work-in-progress entries about L2 (this handoff has authority
   to update memory if relevant — *but only if* there's a stale
   entry; don't add new ones for the sake of it).
7. This handoff is deleted in the final audit commit.

## Critique

Four traps:

- **Audit scope creep into rewrites.** If the audit surfaces "the spec
  could be better organised" or "this code module could be cleaner",
  the *audit* shouldn't refactor it — it should record the finding +
  spin out a follow-up handoff. The audit's job is to *find and link*,
  not to rebuild. The exception is one-line fixes (typos, broken
  links, stale dates) — those land in the audit's own commits.
- **The class-name symmetry refactor (audit checklist §6).** This is
  the largest potential follow-up. Two options: do it now (single
  rename pass across audit-CSV, spec, code, tests) or punt to a
  dedicated handoff. *Recommendation*: punt unless this handoff has
  ≥1 hour of budget — the rename touches enough files that botching
  it would leave the project inconsistent.
- **Failing to notice the things that AREN'T there.** Audits are
  good at checking what *exists*; they often miss what *should
  exist but doesn't*. Specifically: are there any architectural
  decisions that L2 made that ought to be recorded in
  [`../specs/architecture.md`](../specs/architecture.md)'s
  decision-log style but currently live only in note frontmatter?
  (Likely yes — the "operational objective vs motivation"
  framing-axis choice probably belongs in an architecture-level
  decision block, not just in the partition-reasoning note.)
- **The audit produces its own note, which then needs auditing.**
  Avoid recursive doom. The audit note is a checklist outcome,
  not an analysis. Keep it short (≤ 200 words).

## Hard constraints

- **Run last.** This handoff depends on the three preceding L2 handoffs
  having landed (or at least having been substantively attempted).
- **Branch hygiene.** Dedicated session branch
  (`chore/l2-assembly-audit` or similar). Small commits, not one
  big one. Never on `main`. No push without ask.
- **No new content of substance.** This is an audit, not a writing
  session. New writing (e.g. a missing architecture-level decision
  block) is OK but should be focused — one paragraph at a time, with
  clear justification.
- **Memory updates are explicit.** If the session updates
  `MEMORY.md`, the update must be a *removal* of stale state or a
  *correction* of wrong state — not addition of new context.

## Reading list

In order:

1. **All three preceding L2 handoffs** (or their landed outcomes):
   - [`./2026-05-28_l2_viz_iteration.md`](./2026-05-28_l2_viz_iteration.md)
   - [`./2026-05-28_l2_spec_consolidation.md`](./2026-05-28_l2_spec_consolidation.md)
   - [`./2026-05-28_l2_implementation.md`](./2026-05-28_l2_implementation.md)
2. **`docs/specs/02_gasp_schema.md`** — the canonical L2 spec.
3. **[`../specs/architecture.md`](../specs/architecture.md)** —
   the integration target.
4. **[`../specs/project_context.md`](../specs/project_context.md)** —
   the high-level direction the audit checks L2 against.
5. **[`../specs/session_workflow.md`](../specs/session_workflow.md)** —
   handoff-lifecycle + commit conventions the audit enforces.

## Out of scope

- Re-running the audit / discrimination / classification work. The
  audit is structural, not analytical.
- Re-doing the visualisations beyond fixing broken links to them.
- Code refactors that touch more than one module (those go in
  dedicated follow-up handoffs).
- L3 / L4 audit. L1 (GAP) has had its own audits; L3 and L4 will get
  theirs when they exist.
- Anything outside the L2 / GASP scope, even if surfaced by the audit.
  Record as a follow-up; don't action.
