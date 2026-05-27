# CLAUDE.md

Entry point. **Load the durable context before doing anything that touches code or specs.**

This file is intentionally lean. The always-true background, rules, and conventions live in [`docs/specs/`](docs/specs/) — load them per session rather than caching them here. Task-specific scope and step lists arrive in the prompt I paste; the spec files describe what's true regardless of the task.

## Read first, every session

In this order:

1. [`docs/specs/guardrails.md`](docs/specs/guardrails.md) — non-negotiables: branch hygiene, never-commit-to-main, never-push, scope discipline, working standards.
2. [`docs/specs/session_workflow.md`](docs/specs/session_workflow.md) — the stage-commit (no-push) flow, handoff / notes lifecycles, session-start checklist.
3. [`docs/specs/project_context.md`](docs/specs/project_context.md) — the project, the thesis direction, the codebase lineage. What "load-bearing" means here.
4. [`docs/specs/repo_conventions.md`](docs/specs/repo_conventions.md) — where everything lives in this repo, plus the environment.

## Spec files (load when relevant to the task)

- [`docs/specs/architecture.md`](docs/specs/architecture.md) — L0→L4 pipeline, substrate seam, methodological positioning, decisions log. Pass 1 scaffold; methodological positioning still to flesh.
- [`docs/specs/mtdsim_spec.md`](docs/specs/mtdsim_spec.md) — the conformance spec; row-level dispositions against the baseline.
- [`docs/specs/metrics_semantics.md`](docs/specs/metrics_semantics.md) — internal MTTC definition, divergences (C7, ATK-04), comparability boundary.
- [`docs/specs/provenance.md`](docs/specs/provenance.md) — load-bearing constants → source → code → disposition.

## Session-start checks

- `git branch --show-current` → not `main`. If on `main`, create a session branch first.
- `ls docs/handoffs/` → is there an open handoff matching today's task? If so, read it cold.

## Open handoffs

<!-- When a handoff is created or closed, update this section to reflect the live state. Format: `- [topic](docs/handoffs/YYYY-MM-DD_topic.md) — one-line status.` -->

- [Architecture & methodology prepopulation](docs/handoffs/2026-05-27_architecture_prepopulation.md) — partially shipped; Pass 1 scaffold landed at [`docs/specs/architecture.md`](docs/specs/architecture.md) (seeded from pre-lit-review *Current State* + *Methodology Carry-Forward*). Pass 2 owes: §(j) methodological positioning flesh against `LIT_REVIEW.md`, adjacent-paper extraction stubs, and the §(l) open-questions sweep.
- [Docs / `.claude` / `CLAUDE.md` audit](docs/handoffs/2026-05-27_docs_audit.md) — open; produce a findings document critiquing the doc system across 8 dimensions (structure, consistency, coverage, drift, claim-justification, entry-point quality, `.claude` alignment, handoff hygiene). Read-only audit; findings only, no fixes.
