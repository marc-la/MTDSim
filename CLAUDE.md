# CLAUDE.md

Entry point. **Load the durable context before doing anything that touches code or specs.**

This file is intentionally lean. The always-true background, rules, and conventions live in [`docs/specs/`](docs/specs/) — load them per session rather than caching them here. Task-specific scope and step lists arrive in the prompt I paste; the spec files describe what's true regardless of the task.

Harness configuration (permission allowlists, hooks) lives in [`.claude/`](.claude/). Rules that *should* be enforced by the harness but currently live only in prose are tracked under "Audit findings" below.

## Read first, every session

If you read only one of these for orientation, read **`project_context.md`** (#3 below) — it's the "what this project is" document. The other three govern behaviour. Read all four, in order:

1. [`docs/specs/guardrails.md`](docs/specs/guardrails.md) — non-negotiables: branch hygiene, never-commit-to-main, never-push, scope discipline, working standards.
2. [`docs/specs/session_workflow.md`](docs/specs/session_workflow.md) — the stage-commit (no-push) flow, handoff / notes lifecycles, session-start checklist.
3. [`docs/specs/project_context.md`](docs/specs/project_context.md) — the project, the thesis direction, the codebase lineage. What "load-bearing" means here.
4. [`docs/specs/repo_conventions.md`](docs/specs/repo_conventions.md) — where everything lives in this repo, plus the environment.

## Spec files (load when relevant to the task)

- [`docs/specs/architecture.md`](docs/specs/architecture.md) — L0→L4 pipeline, substrate seam, methodological positioning, decisions log. See the spec's own frontmatter for current pass status.
- [`docs/specs/mtdsim_spec.md`](docs/specs/mtdsim_spec.md) — the conformance spec; row-level dispositions against the baseline.
- [`docs/specs/metrics_semantics.md`](docs/specs/metrics_semantics.md) — internal MTTC definition, divergences (C7, ATK-04), comparability boundary.
- [`docs/specs/provenance.md`](docs/specs/provenance.md) — load-bearing constants → source → code → disposition.

## Session-start checks

Run the full checklist in [`docs/specs/session_workflow.md`](docs/specs/session_workflow.md#session-start-checklist) (§ session-start checklist). The quick version: not on `main`, clean tree, check open handoffs.

## Open handoffs

<!-- When a handoff is created or closed, update this section to reflect the live state. Format: `- [topic](docs/handoffs/YYYY-MM-DD_topic.md) — one-line status.` -->

- [Architecture & methodology prepopulation](docs/handoffs/2026-05-27_architecture_prepopulation.md) — partially shipped; Pass 1 scaffold landed at [`docs/specs/architecture.md`](docs/specs/architecture.md). Pass 2 owes: §(j) methodological-positioning flesh against `LIT_REVIEW.md` (retire the audit's six unsupported claims) and the §(l) open-questions sweep. Per-paper extraction deep-flesh is now governed by the separate Pass-2 paper-extractions handoff below.
- [Pass-2 deep paper extractions](docs/handoffs/2026-05-27_pass2_paper_extractions.md) — open; per-paper flesh of the 19 stub extractions (lineage four are read-only), batched by relevance class. Blocked on `LIT_REVIEW.md` §IV-B continuation + Table II + §V Synthesis for the four §IV-B papers (Masud, He, Kim, Tay).

## Audit findings (drive follow-up fix sessions)

- [Docs / `.claude` / `CLAUDE.md` audit findings](docs/notes/2026-05-27_docs_audit.md) — 39 findings across 8 dimensions (6 must-fix, 27 should-fix, 6 nice-to-have). Heaviest cluster: dimension 5 (critical-evaluation quality) — 12 should-fix items, retired by Pass 2 of the architecture prepopulation handoff above. The other 27 findings (all 6 must-fix, the non-§5 should-fix, all nice-to-have) landed in commit `b83b802`.
