---
status: durable
created: 2026-07-13
updated: 2026-08-20
---

# Docs map — where every document lives, and why

**Status:** durable. The single source of truth for the `docs/` tree: the role of each subtree, the contract a file must meet to live there, and the placement criterion for new documents. Supersedes `repo_conventions.md` (2026-07-13 docs refactor). Update when a subtree is added or a contract changes — not for incidental work.

## The organising principle

Everything in `docs/` exists to feed **one of two consumers**:

1. **The dissertation** ([`../thesis/dissertation.tex`](../thesis/dissertation.tex)) — the actual deliverable of this project. Prose that will end up in a chapter flows through `notes/`, organised *by chapter*, written to the bar in [`notes_rubric.md`](notes_rubric.md).
2. **Future working sessions** — the assistant (or Marc) cold-starting on this codebase. Everything else (`workflows/`, `implementation/`, `handoffs/`, `sources/`) exists to make those sessions correct and fast.

A document that serves neither consumer should not exist. When writing any doc, know which consumer it serves — that decides its home, its register, and its lifecycle.

## The tree at a glance

| Subtree | Consumer | Lifecycle | Register |
|---|---|---|---|
| [`workflows/`](.) | sessions | durable; changes rarely | terse, imperative |
| [`../implementation/`](../implementation/) | sessions | durable, provenance-dated | technical; repo jargon encouraged; links to code |
| [`../notes/`](../notes/) | **the dissertation** | durable; high entry bar | formal academic prose; supervisor-readable ([rubric](notes_rubric.md)) |
| [`../handoffs/`](../handoffs/) | sessions | live; deleted when shipped | brief for a cold session |
| [`../thesis/`](../thesis/) | the dissertation | the deliverable itself | LaTeX |
| [`../sources/`](../sources/) | sessions (evidence) | **gitignored** (except `extractions/`) | external material |
| [`../sources/extractions/`](../sources/extractions/) | sessions (evidence) | durable, tracked | per-paper fair-use extracts |

## Placement criterion — where does a new document go?

Work down this list; first match wins.

1. **Open work for a future session** (a brief, an audit to run, a deferred build) → [`../handoffs/`](../handoffs/) as `YYYY-MM-DD_<topic>.md`. Deleted when the work lands.
2. **An idea, argument, finding, or defence destined for the dissertation** → [`../notes/<chapter>/`](../notes/) — **only after it clears [`notes_rubric.md`](notes_rubric.md)**. If it can't yet clear the rubric, it isn't ready to be a note; park it in a handoff or keep working.
3. **Something true because of how this codebase is built** — a data model, a constants disposition, a decision register, an investigation record, an audit trail, anything a reader needs the repo open to follow → [`../implementation/`](../implementation/) (under [`pipeline/<stage>/`](../implementation/pipeline/) if specific to GAP / GASP / OGASP).
4. **A rule about how sessions work in this repo** → here, [`workflows/`](.).
5. **Literature** → the source itself (PDF / converted markdown) in [`../sources/`](../sources/) (gitignored); its extract in [`../sources/extractions/`](../sources/extractions/) (tracked), via the `dissect-paper` skill or the extraction `_template.md`.
6. **LaTeX for the dissertation itself** → [`../thesis/`](../thesis/).

The most common misfile, historically, is 2-vs-3: an investigation record (rubric tables, commit hashes, per-file dispositions, JSD sweeps) drafted as a "note". The test: **could Marc's supervisor read it without the repo?** If no, it is implementation material, however dissertation-relevant its conclusions — distil the conclusion into a rubric-clearing note and keep the record in `implementation/`.

## Per-subtree contracts

### `workflows/` — session context and working rules

The always-loaded layer. Every session reads all of it (see [`../../CLAUDE.md`](../../CLAUDE.md)):

- [`guardrails.md`](guardrails.md) — non-negotiables (git, scope, evidence standards).
- [`session_workflow.md`](session_workflow.md) — stage-commit flow, handoff / notes lifecycles, session-start checklist.
- [`project_context.md`](project_context.md) — what the project is; thesis direction; codebase lineage.
- this file — where documents live.
- [`notes_rubric.md`](notes_rubric.md) — the quality gate for `notes/`.
- [`voice.md`](voice.md) — the prose contract for dissertation-bound writing (loaded before drafting `notes/` or `thesis/` prose, not every session).
- [`figure_table_conventions.md`](figure_table_conventions.md) — the visual-artefact counterpart to `voice.md`: MTD-literature figure/table conventions distilled from a page-level survey of the lit-review corpus (per-genre grammars, table genres, caption/decoding rules, corpus anti-patterns). Loaded before generating or revising any dissertation figure or table, or writing a figure generator in `tools/`; sits below the figure-pipeline and no-accentuation rulings.
- [`literature_conventions.md`](literature_conventions.md) — the same survey's **prose/methods** distillation: ATT&CK referencing and version-pinning rules, framework version-stamping, field terminology (SDR, what/when/how-to-move, AU-spelling licence), metric definition-before-use discipline, and the methods-reporting genre checklist (threat-model section, parameter tables, evaluation-ladder positioning, limitations ownership). Loaded before drafting or scrutinising methodology/results prose, or anything naming ATT&CK, CVSS, a kill-chain model, or a security metric.
- [`critique_protocol.md`](critique_protocol.md) — the draft-review contract (edit tiers, verdict vocabulary, sentence diagnostics, reviewer banlist); loaded before critiquing any draft prose. Grey-box by design: usable standalone with exemplars pasted in.
- [`draft_scrutiny.md`](draft_scrutiny.md) — the **content/intent** review contract: checks a draft against the research record, the chapter notes, and the implementation evidence for right argument, right framing, missing arguments, unowned concessions, and overclaims. Carries the corpus map (which documents scrutinise which chapter) and the scrutinise-never-generate rule. Loaded before scrutinising draft content or producing content-point scaffolds; the `scrutinise-draft` skill invokes it. Sits above `critique_protocol.md` (prose quality) and `voice.md` (sentences).
- [`drafting_pipeline.md`](drafting_pipeline.md) — **how every unit of dissertation prose gets written** (ratified on the §4.2.1 pilot, 2026-08-16): the five-pass dictation pipeline (speak → repair+register via the `repair-dictation` skill → Marc's marker walk → `scrutinise-draft` → Marc's compression), plus the section-level **pass 6 voice pass** (the `voice-pass` skill, ruled 2026-08-20 — proposal-only, Marc ratifies item by item), the roles, the sequencing rule, and the gates. No pass after draft 1 writes unratified prose. Loaded before any dissertation drafting session.
- [`academic_register.md`](academic_register.md) — the **target register for pass 6**: the general academic-writing conventions of CS/security prose (register, tense, hedging, economy, the vacuous-sentence test) plus the living spoken-residue inventory dictation leaves behind, with the calibration dial (closer to academic than to speech; never through a voice.md licensed device). Loaded by the `voice-pass` skill; sits between `voice.md` (what must survive) and `literature_conventions.md` (the field-specific layer).
- [`terminology.md`](terminology.md) — the **living terminology registry**: one canonical term per dissertation concept, RATIFIED (enforced) or PROPOSED (awaiting Marc's ruling), with census counts and the no-auto-substitution rule. Grows as drafting meets new clusters; consumed by pass 6 and, post-ruling, by `repair-dictation` and `scrutinise-draft`. Dissertation surface only — repo vocabulary is never renamed by it.

Contract: short, imperative, no duplication of content that lives elsewhere (link instead). A new subtree anywhere in `docs/` **must** be registered in this file in the same commit that creates it.

### `implementation/` — codebase-shaped truth

The canonical record of what is built and why, in whatever register is clearest to a technical reader with the repo open. Internal terminology (GAP, GASP, OGASP, L0–L4, HARM, Tier 1–3) is encouraged here; this is where it is defined and used freely.

- [`architecture.md`](../implementation/architecture.md) — L0→L4 pipeline, substrate seam, decisions log.
- [`apt_model_criterion.md`](../implementation/apt_model_criterion.md) — the APT-attacker-model criterion (supervisor S6): literature-derived axes, this model's honest per-axis scores, and the M8b measurement recommendations. **On the every-session read-first list in [`CLAUDE.md`](../../CLAUDE.md)** by supervisor direction — the one `implementation/` file loaded unconditionally.
- [`substrate_primer.md`](../implementation/substrate_primer.md) — the inherited simulator as adversarial terrain (attacker's-eye, non-implementation-specific).
- [`mtdsim_spec.md`](../implementation/mtdsim_spec.md) — conformance spec; row-level dispositions against the baseline.
- [`mtdsim_intent_spec.md`](../implementation/mtdsim_intent_spec.md) — literature-only intent spec (paper side alone, no code evidence); the uncontaminated yardstick the conformance audit tests the code against. Keep it code-free — audit records cite it, never the reverse.
- [`intent_conformance_audit.md`](../implementation/intent_conformance_audit.md) — the 2026-07-28 audit of the substrate against the intent spec: per-IS-ID four-way classification with code locators, the post-hoc cross-check against `mtdsim_spec.md`, and the open disposition list (D-01..D-15) awaiting Marc's rulings.
- [`metrics_semantics.md`](../implementation/metrics_semantics.md) — internal MTTC, divergences (C7, ATK-04), comparability boundary.
- [`provenance.md`](../implementation/provenance.md) — load-bearing constants → source → code → disposition.
- [`trace_tool.md`](../implementation/trace_tool.md) — the event-log tracer (`mtdnetwork/trace.py`): usage, invariants, and its extension charter (a living diagnostic tool, `status: living`).
- [`research_record/`](../implementation/research_record/) — the annal mined from Marc's own prompts (the transcript-corpus brief): the per-prompt disposition table and the decision-thread files carrying intent, reversals and abandoned paths that no shipped record owns. Prompts are dated evidence, never current truth; conflicts with shipped records are flagged there, not resolved. Re-run via `tools/prompt_corpus.py` against fresh snapshots.
- **The component-boundary records** — the durable output of the 2026-08-02 boundary programme and the disruption-wiring brief that followed it, and the reference for anything touching the attacker/defender/network seams: [`attacker_read_surface.md`](../implementation/attacker_read_surface.md) (what the attacker perceives), [`mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md) (every mechanism's write set, plus the purview/fairness table), [`boundary_attacker_defender_channels.md`](../implementation/boundary_attacker_defender_channels.md) (the six direct disruption channels, priced per class), and [`disruption_wiring.md`](../implementation/disruption_wiring.md) (whether that pricing *arrives* at both driving arms — the per-mechanism truth table and traffic).
- [`pipeline/gap/`](../implementation/pipeline/gap/) · [`pipeline/gasp/`](../implementation/pipeline/gasp/) · [`pipeline/ogasp/`](../implementation/pipeline/ogasp/) — per-stage data models plus the investigation records, audits, and decision registers that produced them.

Contract: **provenance-dated.** Every file carries frontmatter with `status`, `created`, and `updated`; a session that materially edits one bumps `updated` in the same commit. Investigation records are immutable history — annotate with status banners rather than rewriting them.

### `notes/` — the dissertation's staging layer

Chapter-organised, rubric-gated prose. The full contract is [`notes_rubric.md`](notes_rubric.md); the short version: formal academic prose, self-contained, atomic (one idea per file), readable by Marc's supervisor without the repo, repo links confined to an evidence footer. The sentence-level voice is [`voice.md`](voice.md) — default for notes, hard gate for `thesis/`. Chapter subdirs mirror the dissertation:

The subdirs track the **ratified chapter structure** (supervisor register V-series, 2026-08-11; remapped 2026-08-14): introduction (ch1), background (ch2), literature review (ch3), methodology (ch4), results (ch5), discussion (ch6), future work (ch7), conclusion (ch8).

| Subdir | Dissertation chapter | What lands here |
|---|---|---|
| `ch2_background/` | Background (ch2) | the inherited platform: simulator lineage, network/defence/attacker models, described for comprehension (not methodology) |
| `ch3_lit_review/` | Literature review (ch3) | positioning and gap arguments: research-gap statements, precedent surveys, related-work framings — the review's occupying move, distinct from ch2's platform description |
| `ch4_methods/` | Methodology (ch4) | the modelling arguments (corpus → profiles → attacker; validity defences), the realisation arguments (built-beside, portability contract, bug-vs-design verification), and experimental design (burden of proof, grading, discrimination). Includes [`tactic_profiles/`](../notes/ch4_methods/tactic_profiles/) (the 15 per-tactic evidence profiles + their `_rubric.md`) |
| `ch5_results/` | Results (ch5) | sensitivity-analysis and results framing — how a found result is stated and bounded |
| `ch6_discussion/` | Discussion (ch6) | interpretation, limitations synthesis |
| `ch7_future_work/` | Future work (ch7) | the named successor programme; only future-work arguments that are self-contained ideas (smaller candidates ride *Revisit conditions*) |

The Introduction and Conclusion chapters deliberately have **no** notes subdir: both are syntheses written last from the other chapters' material (the introduction's motivation is compressed from `ch3_lit_review/`'s gap statement and the ch4–ch5 contributions). If a note genuinely fits neither maintained chapter, that is a placement smell — re-run the criterion above before inventing a new subdir. Section/subsection structure *below* chapter level is emergent — it will crystallise from the notes themselves, so do not encode sub-chapter numbering into filenames or dirs. Files named with a leading underscore (`_template.md`, `_rubric.md`) are process scaffolding, exempt from the prose register; each chapter dir carries a `README.md` opening with *what that chapter does* (its rhetorical job in the dissertation) and what belongs in it. Whole-document writing guidance — the job of each part including title/abstract/introduction/conclusion, the drafting order, and the refine–forget cycle — is [`../notes/_writing_guide.md`](../notes/_writing_guide.md); load it before drafting chapter prose.

### `handoffs/` — open work

Unchanged from long-standing practice: `YYYY-MM-DD_<topic>.md`, created when work won't fit the current session, deleted **in the commit that ships the work**. `ls docs/handoffs/` is the inventory of open work; see [`session_workflow.md`](session_workflow.md#handoff-workflow). Two files in that directory are not handoffs: `README.md` carries the **dependency order** between the open ones (the one thing a directory listing cannot show — prune a line when its handoff ships), and `__archive/` holds parked work that is deliberately *not* on the active chain.

### `thesis/` — the deliverable

The UWA `cshonours` LaTeX project (`dissertation.tex`, `references.bib`, `figures/`, class file). Chapters are the stable frame the whole docs system points at; notes feed sections into it. Any prose written here must pass the hard gate in [`voice.md`](voice.md) §(f) before commit. Compile with `latexmk -pdf dissertation.tex`. Build artefacts are gitignored.

### `sources/` and `sources/extractions/`

- `sources/` — external papers, reports, and the lit review, converted to markdown where possible. **Gitignored** (copyright); read from here, never commit. The source markdown *is* the citable artefact for non-peer-reviewed material.
- `sources/extractions/` — tracked, per-paper fair-use extracts (paraphrase-heavy, locator-anchored) built from `sources/`. One file per paper, `_template.md` as scaffold; the `dissect-paper` skill maintains these. Sessions cite extractions, not raw sources, wherever an extraction exists.

## Repo layout beyond `docs/` (orientation)

- [`../../baseline/golden/`](../../baseline/golden/) — canonical seeded golden outputs (behavioural oracle; re-baselined Phase 2c). `golden_phase0_buggy/` kept for provenance. [`BASELINE.md`](../../baseline/BASELINE.md) / [`CHANGELOG.md`](../../baseline/CHANGELOG.md) record every intentional re-baseline.
- [`../../data/`](../../data/) — pipeline artefacts: `gap/` (L1 graph + per-flow YAMLs + pinned ATT&CK bundle), `gasp/` (four objective subgraphs + `metadata_audit.csv`, the load-bearing classification input), `ogasp/` (weighted nets, `tactic_durations.json`, the declared-value families and their generated views — `controller/outcome_rules.json`, `attacker_utility.json` — timeline runs).
- [`../../src/mtdsim/`](../../src/mtdsim/) — the fresh pipeline code (l0–l4); [`../../mtdnetwork/`](../../mtdnetwork/) — the inherited substrate.
- Harness configuration (permission allowlists, hooks, skills) lives in [`../../.claude/`](../../.claude/).

## Environment

- Active env: `mtdsim` (Python 3.11.15). Note: [`../../environment.yml`](../../environment.yml) still nominally specifies `mtdsimtime` / 3.9.13 — the working env diverged (recorded in `baseline/BASELINE.md`); reconciling `environment.yml` to reality is an open housekeeping item.
- The Tay RL / benchmark path (`mtdnetwork/mtdai/`, `operation/mtd_ai_*.py`) runs under the current env (TF 2.21 / Keras 3.14; pretrained weights load; smoke run completes). Reuse-vs-retrain disposition: [`architecture.md`](../implementation/architecture.md) §(a) Tay decision block (authoritative).
