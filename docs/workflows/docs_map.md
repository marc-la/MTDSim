---
status: durable
created: 2026-07-13
updated: 2026-07-28
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
- [`pipeline/gap/`](../implementation/pipeline/gap/) · [`pipeline/gasp/`](../implementation/pipeline/gasp/) · [`pipeline/ogasp/`](../implementation/pipeline/ogasp/) — per-stage data models plus the investigation records, audits, and decision registers that produced them.

Contract: **provenance-dated.** Every file carries frontmatter with `status`, `created`, and `updated`; a session that materially edits one bumps `updated` in the same commit. Investigation records are immutable history — annotate with status banners rather than rewriting them.

### `notes/` — the dissertation's staging layer

Chapter-organised, rubric-gated prose. The full contract is [`notes_rubric.md`](notes_rubric.md); the short version: formal academic prose, self-contained, atomic (one idea per file), readable by Marc's supervisor without the repo, repo links confined to an evidence footer. The sentence-level voice is [`voice.md`](voice.md) — default for notes, hard gate for `thesis/`. Chapter subdirs mirror the dissertation:

| Subdir | Dissertation chapter | What lands here |
|---|---|---|
| `ch2_background/` | Background & Literature Review | positioning, gap statements, precedent surveys |
| `ch3_design/` | Design & Methodology | the modelling arguments: corpus → profiles → attacker; validity defences. Includes [`tactic_profiles/`](../notes/ch3_design/tactic_profiles/) (the 15 per-tactic evidence profiles + their `_rubric.md`) |
| `ch4_implementation/` | Implementation | prose about *how* it was realised (rare — most of this is `implementation/` material until the chapter is drafted) |
| `ch5_evaluation/` | Evaluation & Results | experimental-design arguments, what the evaluation must demonstrate, results framing |
| `ch6_discussion/` | Discussion | interpretation, limitations synthesis |

The Introduction and Conclusion chapters deliberately have **no** notes subdir: both are syntheses written last from the other chapters' material (the introduction's motivation lives in `ch2_background/`; future-work candidates ride the *Revisit conditions* of the notes that spawn them). If a note genuinely fits neither maintained chapter, that is a placement smell — re-run the criterion above before inventing a new subdir. Section/subsection structure *below* chapter level is emergent — it will crystallise from the notes themselves, so do not encode sub-chapter numbering into filenames or dirs. Files named with a leading underscore (`_template.md`, `_rubric.md`) are process scaffolding, exempt from the prose register; each chapter dir carries a `README.md` opening with *what that chapter does* (its rhetorical job in the dissertation) and what belongs in it. Whole-document writing guidance — the job of each part including title/abstract/introduction/conclusion, the drafting order, and the refine–forget cycle — is [`../notes/_writing_guide.md`](../notes/_writing_guide.md); load it before drafting chapter prose.

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
