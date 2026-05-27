---
status: open
created: 2026-05-27
---

# Capture the L0→L4 architecture as a durable spec (`docs/specs/architecture.md`)

Turn Marc's existing methodological carryover and lit review into a durable architecture spec so future sessions ground architectural reasoning in the spec, not in re-derivation from substrate code or Marc's head.

## State of play

- The docs restructure landed today on `chore/docs-restructure` (commit `f8ed39e`, pending review and merge by Marc). New tree: `docs/specs/`, `docs/handoffs/`, `docs/notes/`, `docs/extractions/`, all with templates.
- **No `docs/specs/architecture.md` exists yet.** The entire L0→L4 framework is captured today in one line in [`docs/specs/project_context.md`](../specs/project_context.md):
  > "L0 raw CTI → L1 GAP (attack graph; nodes = ATT&CK techniques) → L2 GASP (motivation subgraph) → L3 OGASP (attacker-agent traversal in MTDSim) → L4 evaluation."
- That single line is the entire durable record. The actual architecture lives in Marc's head, the proposal, the lit review (`docs/sources/LIT_REVIEW.md`, gitignored), and slide decks. **This is the drift risk this handoff addresses.**
- The four lineage paper extractions exist ([`docs/extractions/{brown2023,zhang2023,ho2024,tay2024}.md`](../extractions/)). Adjacent papers cited in the lit review do **not** yet have extraction files.

## Recommended approach — two passes

Doing both in one session usually produces a half-baked architecture doc. Plan for two.

### Pass 1 — scaffold (this handoff)

Goal: skeletons in place, frontmatter + headings + Marc's bullets. ~1 session. Most of the typing is what Marc already has in his head or in the proposal.

1. **Marc-led verbal walkthrough.** Marc opens the session with: path/excerpts from the proposal or methodology document, any slide decks / diagrams (ASCII-renderable or linkable), and a list of adjacent papers (CTI standards, behavioural-attacker work, adjacent MTD eval work, specific titles).
2. **Author `docs/specs/architecture.md`** as a single file (do not split into `methodology.md` yet — split only if it grows past ~600 lines or develops two distinct lifecycles). Structure:
   - **Top-level goal + scope** — one paragraph, what this system is and what it isn't.
   - **L0→L4 pipeline map.** One section per stage. Each section: stage name, **inputs** (format + where they come from), **outputs** (format + where they're stored), **transformation** (what the stage does, one paragraph), **validation** (how Marc knows the stage is producing what it should). For L3 (OGASP), reference [`mtdsim_spec.md`](../specs/mtdsim_spec.md) for the substrate the stage runs on, not re-describe it.
   - **Glossary.** CTI, GAP, GASP, OGASP, motivation profile, behavioural grounding, procedural attacker (and any other project-specific term that appears in `project_context.md` or the lit review).
   - **ASCII pipeline diagram.** L0 → L1 → L2 → L3 → L4, with arrows and the artefact flowing on each.
   - **Substrate seam map.** Where MTDSim plugs in (the attacker module is the load-bearing seam per `project_context.md`). What gets replaced vs added vs left alone. Reference the spec rows where the seam lives.
   - **Methodological positioning** (synthesised from `docs/sources/LIT_REVIEW.md`). What existing MTD evaluation literature gets right; what it misses; how OGASP-derived adversary traversal fills the gap. The single RQ and how it's operationalised through the pipeline. **Two paragraphs maximum** for the scaffold — full fleshing is Pass 2.
   - **Decisions log (inline).** Each architectural decision gets a `**Decision — Why:**` callout in the section where it pertains. Known decisions to inline now (extract from project_context.md and the now-deleted `direction/build_carryforward.md`, recoverable via git log): Attack Flow schema version, SNAKES env, RL-reuse-vs-retrain, single-canonical substrate (the dropped internal/lineage preset).
   - **Validation strategy.** Which metrics, on which runs, demonstrate that the system works (MTTC, ASR, attack-path exposure, RoA per `project_context.md`). The within-substrate comparability boundary per `metrics_semantics.md` §d.
   - **Status markers.** Each subsection carries an explicit `Status: designed | partially built | unbuilt` marker. **Distinguish design from implementation.** Architecture.md describes the *system*, not the *progress*.
3. **Stub adjacent-paper extractions.** For each paper Marc lists, create `docs/extractions/<authorYEAR>.md` from [`_template.md`](../extractions/_template.md), filled with **only**:
   - Citation block
   - Relevance line (one sentence)
   - Bibliographic anchor (citation key, DOI/URL)
   - Empty "Relevant artefacts" section with `### TODO` placeholder
   - Empty "Open questions" + "Out of scope" sections
   Categories to expect (full title list comes from Marc at session start):
   - **CTI standards** — MITRE ATT&CK (Strom et al.), Attack Flow (CTID), STIX/TAXII where cited
   - **Behavioural attacker / motivation modelling** — the work that motivates moving from procedural to behaviourally-grounded attackers
   - **Adjacent MTD evaluation work** — MTD papers cited beyond the Brown→Tay lineage

### Pass 2 — flesh (separate session(s) per artefact)

Goal: per-artefact deep work. Plan for one session per extraction file plus one per major architecture section. Marc drives; Claude transcribes/structures.

- For each extraction stub: open `docs/sources/<paper>.<ext>`, walk through key sections, extract under fair use following the template. **One paper per session** to prevent cross-attribution (per [`guardrails.md`](../specs/guardrails.md)).
- For methodology positioning in architecture.md: pull from `docs/sources/LIT_REVIEW.md` the gap and contribution claims; integrate as a fully developed section. Cross-link to each extraction file as evidence.

## Validation gate

Pass 1 is done when:
- `docs/specs/architecture.md` exists and a cold session can read it + `project_context.md` and answer: "what does this project do, end-to-end, with what inputs and what outputs?" without needing substrate code or conversation context.
- Every architecture decision in the file has both a `**Why:**` and an `**If revisited, what would change:**` line (so future Marc can judge whether the decision is still load-bearing).
- An extraction file exists (even if stub-only) for every paper Marc named in his list. The four existing lineage extraction files are unchanged.
- CLAUDE.md's "Open handoffs" section is updated to either delete this handoff (if fully shipped) or mark it `status: partially shipped` and note that Pass 2 is outstanding.
- The architecture diagram in `architecture.md` does not contradict the one-liner in `project_context.md`. If reality has drifted, update `project_context.md` in the same commit and note it in the commit message.

Pass 2 has its own gate per extraction file (template completed; quotes locator'd; cross-links to spec/architecture filled in).

## Hard constraints

- **One paper per extraction pass.** Per [`docs/specs/guardrails.md`](../specs/guardrails.md). No cross-attribution.
- **Don't assert any paper is wrong.** Flag for Marc to resolve.
- **All quotes follow fair-use pattern** in [`docs/extractions/_template.md`](../extractions/_template.md) — locator'd, short, blockquoted; paraphrase preferred.
- **Don't restate** content from existing specs. Link to them. The architecture.md describes Marc's system *on top of* the substrate; the substrate has its own specs.
- **Distinguish design from implementation.** Use `Status:` markers per section. Architecture.md is "what the system IS by design"; substrate specs are "what the inherited code currently does".
- **Don't touch** `mtdsim_spec.md`, `metrics_semantics.md`, `provenance.md`, or the 4 lineage extractions. Those describe the *inherited substrate* and are settled.
- **Don't write `docs/notes/*` proactively.** Only if Marc explicitly asks. Notes are for dissertation-narrative material surfaced during the session.
- **Branch + commit + don't push.** Per [`docs/specs/session_workflow.md`](../specs/session_workflow.md). Pass 1 work on `feat/architecture-spec` or similar; commits local for Marc's review.
- **Don't merge `chore/docs-restructure`** — Marc reviews and merges that separately. Branch this handoff's work off `main` or off `chore/docs-restructure` once merged (ask Marc at session start).
- **architecture.md ≤ ~600 lines** for the scaffold. If it would grow past, **stop and ask** about splitting `methodology.md` off.

## Reading list

Must skim cold before doing anything:

- [`CLAUDE.md`](../../CLAUDE.md) — entry point
- [`docs/specs/project_context.md`](../specs/project_context.md) — the L0→L4 one-liner that this work expands
- [`docs/specs/guardrails.md`](../specs/guardrails.md) — the rules
- [`docs/specs/session_workflow.md`](../specs/session_workflow.md) — branch/commit flow
- [`docs/specs/mtdsim_spec.md`](../specs/mtdsim_spec.md) — first 3 sections only (Network / Attacker / MTD module overviews) — for the substrate seam
- [`docs/specs/metrics_semantics.md`](../specs/metrics_semantics.md) §d — comparability boundary, drives the validation strategy
- [`docs/extractions/_template.md`](../extractions/_template.md) — the fair-use extraction pattern
- [`docs/handoffs/_template.md`](../handoffs/_template.md) — the handoff pattern (for the Pass-2 spawn)
- [`docs/sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md) — Marc's lit review (gitignored; read in-session) — primary input for methodological positioning

## Out of scope (explicitly)

- Building or modifying any code. Architecture.md is design; the substrate stays untouched.
- Extending the 4 lineage extractions (`brown2023.md`, `zhang2023.md`, `ho2024.md`, `tay2024.md`).
- Drafting dissertation prose. Architecture.md is technical reference, not narrative.
- Writing `docs/notes/*` files unless Marc explicitly asks.
- Touching `mtdsim_spec.md`, `metrics_semantics.md`, `provenance.md`.
- Merging or pushing any branch.
- Re-deriving the architecture from substrate code. **The architecture comes from Marc.** Claude transcribes and structures, doesn't invent.

## Inputs Marc will provide at session start

1. Path or excerpts from the proposal / methodology document.
2. Path or links to slide decks / diagrams (or verbal walkthrough if not durable yet).
3. **A list of adjacent papers to stub extractions for** — title + author + year + which category (CTI standard / behavioural-attacker / adjacent MTD eval).
4. Confirmation: branch off `main` or off `chore/docs-restructure`? (Depends on whether the restructure is merged by then.)
5. Anything else Marc has in his head that's load-bearing for the architecture but not yet written down anywhere.
