---
status: partially shipped
created: 2026-05-27
---

# Capture the L0→L4 architecture as a durable spec (`docs/specs/architecture.md`)

Turn Marc's existing methodological carryover and lit review into a durable architecture spec so future sessions ground architectural reasoning in the spec, not in re-derivation from substrate code or Marc's head.

## Pass 1 — shipped 2026-05-27 (this branch: `feat/lit-review-landing`)

Scaffold landed at [`../specs/architecture.md`](../specs/architecture.md) (484 lines, under the
600-line ceiling). Seeded from the pre-lit-review *Current State* (29 Apr 2026)
and *Methodology Carry-Forward* (20 May 2026) Marc pasted at session start; both
are pasted-only, neither is committed. Stale items (replay-viz visualiser, 6,000s
crash status, GAP v0.4 specifics, lit-review process notes, Apr-29 RQ wording)
were dropped silently per Marc's call. The §(j) methodological-positioning
section is intentionally a two-paragraph stub awaiting Pass 2 against
`LIT_REVIEW.md`. Status markers (designed / partially built / unbuilt) are set
per §(c)–(g). Every architectural decision carries both **Why:** and
**If revisited:** lines.

**Pass 2 still owes:**
- §(j) methodological positioning — flesh against [`../sources/LIT_REVIEW.md`](../sources/LIT_REVIEW.md);
  current two paragraphs are scaffold-only. Pass 2 must retire the **six
  unsupported claims** recorded in
  [`../notes/2026-05-27_docs_audit.md`](../notes/2026-05-27_docs_audit.md) §5
  (Pyramid of Pain, "dominant evaluation pattern", three-literatures
  intersection, ATT&CK Evaluations, Jalowski primitives, Rodríguez
  four-axes comparison) by citing the relevant extractions in §(a) / §(f) /
  §(j).
- ~~Adjacent-paper extraction deep flesh~~ — **shipped** by the Pass-2
  paper-extractions handoff (commits `506722b` / `a7050c9` / `c71eae8`).
  All 19 non-lineage extractions now carry deep artefact sections; the two
  highest-leverage stubs for audit-finding retiral ([`../extractions/jalowski2026.md`](../extractions/jalowski2026.md)
  for the §(f) primitives decision; [`../extractions/rodriguez2024.md`](../extractions/rodriguez2024.md)
  for the §(j) four-axes comparison) are now both fleshed and ready to be
  cited from §(j) prose in Pass 2 of *this* handoff.
- Resolve the §(l) open questions: Attack Flow schema in-tree + parser
  entrypoint (now consolidated into §(c) Parser-contract block), Jalowski
  primitives encoded subset, L1 aggregation parameters,
  motivation-attribution method, network substrate generality, L4
  evaluation matrix shape.
- Confirm whether `architecture.md` and `methodology.md` should split — current
  scaffold keeps both intertwined in one file; the 600-line trigger has not
  fired but the eventual flesh-out may.

**Pass 2 validation gate:**
- §(j) cites at least one extraction per claim in the audit's
  unsupported-claim count (target: 6 retirals).
- `jalowski2026.md` and `rodriguez2024.md` extractions are fleshed beyond
  the bibliographic anchor (sections to lift per the stub's TODO block).
- All §(l) open questions either have a Decision block or carry a one-line
  "deferred to evaluation phase" with explicit trigger.

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

## Source-file naming convention (in `docs/sources/`, gitignored)

`docs/sources/` is the working library of full-text PDFs/markdown for the lit review and lineage. The filenames already carry an implicit organisation; this section makes the rule explicit so future sessions don't have to re-derive it from the listing.

**Pattern:** `<lit_section>_<lit_subsection>_<authorYEAR>.md` for non-lineage papers; `<authorYEAR>.md` (no section prefix) for the four UWA lineage papers (`brown2023.md`, `zhang2023.md`, `ho2024.md`, `tay2024.md`).

**Section-prefix mapping** (mirrors the lit-review section numbering):

| Prefix | Lit-review section | Contents |
|---|---|---|
| `1_1_` | §II-A — MTD concept / taxonomy | foundational MTD definitions, SDR taxonomy |
| `1_2_` | §II-B — MTD evaluation paradigms | metrics, HARM, validation methods |
| `1_3_` | §II-C — orchestration & adaptive selection | RL-orchestrated MTD, conflict-resolution rules |
| `2_1_` | §III-A — MITRE ATT&CK + Attack Flow | the technique-level vocabulary and its STIX serialisation |
| `2_2_` | §III-B — Pyramid of Pain | indicator-class cost ranking + TTP durability |
| `2_3_` | §III-C — APTs | APT lifecycle, NIST framing, attribution |
| `2_4_` | §III-D — attack profiling | NLP / process-mining / LLM extraction methods, manual curation |
| `3_1_` | §IV-A — surveys naming the attacker-modelling gap | Cho 2020, Jalowski 2026 |
| `3_2_` | §IV-B — recent MTD evaluation works | papers placed on the fidelity descriptor |
| `4_`   | §V — synthesis / cross-cutting | supporting works used in the synthesis (e.g. RL adversary, defender perspective) |

**UWA lineage exception.** The four lineage papers (Brown 2023, Zhang 2023, Ho 2024, Tay 2024) keep the un-prefixed `<authorYEAR>.md` form because their extraction filenames in [`../extractions/`](../extractions/) also use that form, and matching filenames make the source↔extraction link obvious. Treat them as a special-cased "lineage" category that lives outside the numbered prefix scheme.

**Extraction filenames** (`docs/extractions/<authorYEAR>.md`) **never carry the section prefix.** When stubbing or fleshing an extraction, the filename is the bare `<authorYEAR>`, even when the source file is prefixed. The lit-section organisation is a property of `sources/`, not of the extraction artefact.

**No "keyword" suffix.** Earlier copies carried filename suffixes (e.g. `2024MITRE`, `2024using`, `2023evaluating`). The `<authorYEAR>` token alone is the canonical key; the section prefix already disambiguates same-year authors. Drop the keyword on rename.

**Disambiguation when an author has two papers in the same year:** append a short tag in lowercase (e.g. `zhang2023.md` for the MTDSimTime lineage paper; `zhang2025attackg.md` for the AttacKG+ paper) — but only when ambiguity actually arises in *this* corpus.

**Reading list to stub against (Pass-1 step 3):** the current contents of `docs/sources/` map onto extraction stubs as follows. Each row produces one `docs/extractions/<authorYEAR>.md` stub with citation + relevance line + empty sections per [`../extractions/_template.md`](../extractions/_template.md).

| Source filename | Extraction filename | Category |
|---|---|---|
| `1_1_cho2020toward.md` | `cho2020.md` | §II-A — MTD survey, attacker-modelling-gap source |
| `1_1_ghosh2009NITRD.md` | `ghosh2009.md` | §II-A — foundational MTD (NITRD) |
| `1_2_hong2018dynamic.md` | `hong2018.md` | §II-B — dynamic security models / HARM extension |
| `1_3_masud2025vulnerability.md` | `masud2025.md` | §II-C — orchestration (specified pole) |
| `2_1_al-sada2024MITRE.md` | `al-sada2024.md` | §III-A — ATT&CK |
| `2_1_attackflowdoc.md` | `attackflow.md` | §III-A — CTID Attack Flow specification (not an author paper) |
| `2_2_bianco2013pop.md` | `bianco2013.md` | §III-B — Pyramid of Pain |
| `2_2_sadlek2022current.md` | `sadlek2022.md` | §III-B — TTP-durability |
| `2_3_alshamrani2019survey.md` | `alshamrani2019.md` | §III-C — APT survey |
| `2_4_buechel2025sok.md` | `buechel2025.md` | §III-D — SoK on TTP extraction |
| `2_4_ferraz2024procedural.md` | `ferraz2024.md` | §III-D — procedural attacker modelling |
| `2_4_rahman2024mining.md` | `rahman2024.md` | §III-D — ChronoCTI (NLP-based extraction) |
| `2_4_rodriguez2024process.md` | `rodriguez2024.md` | §III-D — process-mining extraction |
| `2_4_zhang2025attackg_.md` | `zhang2025attackg.md` | §III-D — AttacKG+ (LLM-based extraction) |
| `3_1_jalowski2026rethinking.md` | `jalowski2026.md` | §IV-A — second gap-survey |
| `3_2_he2025MTD-AD.md` | `he2025.md` | §IV-B — MTD-AD, NIDS adversarial defence |
| `3_2_kim2026mtdid.md` | `kim2026.md` | §IV-B — CKC-aware MTD |
| `4_bland2020machine.md` | `bland2020.md` | §V — RL adversary (cross-cutting) |
| `4_outkin2023defender.md` | `outkin2023.md` | §V — defender perspective (cross-cutting) |

Lineage papers (`brown2023`, `zhang2023`, `ho2024`, `tay2024`) already have full extraction files — do not re-stub. The handoff's Pass-1 step 3 above governs the new stubs only.

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
3. ~~A list of adjacent papers to stub extractions for~~ — **superseded.** The papers are already in `docs/sources/` with the section-prefix naming convention encoding their category (see "Source-file naming convention" above). Stubs will be / have been generated against that list rather than against a hand-curated list at session start. Marc only needs to flag papers added to `sources/` *after* the convention landed.
4. Confirmation: branch off `main` or off `chore/docs-restructure`? (Depends on whether the restructure is merged by then.)
5. Anything else Marc has in his head that's load-bearing for the architecture but not yet written down anywhere.
