# CLAUDE.md

Entry point. **Load the durable context before doing anything that touches code or specs.**

This file is intentionally lean. The always-true background, rules, and conventions live in [`docs/specs/`](docs/specs/) — load them per session rather than caching them here. Task-specific scope and step lists arrive in the prompt I paste; the spec files describe what's true regardless of the task.

Harness configuration (permission allowlists, hooks) lives in [`.claude/`](.claude/).

## Read first, every session

If you read only one of these for orientation, read **`project_context.md`** (#3 below) — it's the "what this project is" document. The other three govern behaviour. Read all four, in order:

1. [`docs/specs/guardrails.md`](docs/specs/guardrails.md) — non-negotiables: branch hygiene, never-commit-to-main, never-push, scope discipline, working standards.
2. [`docs/specs/session_workflow.md`](docs/specs/session_workflow.md) — the stage-commit (no-push) flow, handoff / notes lifecycles, session-start checklist.
3. [`docs/specs/project_context.md`](docs/specs/project_context.md) — the project, the thesis direction, the codebase lineage. What "load-bearing" means here.
4. [`docs/specs/repo_conventions.md`](docs/specs/repo_conventions.md) — where everything lives in this repo, plus the environment.

## Spec files (load when relevant to the task)

- [`docs/specs/architecture.md`](docs/specs/architecture.md) — L0→L4 pipeline, substrate seam, methodological positioning, decisions log. See the spec's own frontmatter for current pass status.
- [`docs/specs/01_gap_schema.md`](docs/specs/01_gap_schema.md) — L1 GAP data model: the lossless, Attack-Flow-only technique graph + its construction decisions. The detail under architecture.md §(c)–(d).
- [`docs/specs/mtdsim_spec.md`](docs/specs/mtdsim_spec.md) — the conformance spec; row-level dispositions against the baseline.
- [`docs/specs/metrics_semantics.md`](docs/specs/metrics_semantics.md) — internal MTTC definition, divergences (C7, ATK-04), comparability boundary.
- [`docs/specs/provenance.md`](docs/specs/provenance.md) — load-bearing constants → source → code → disposition.

## Session-start checks

Run the full checklist in [`docs/specs/session_workflow.md`](docs/specs/session_workflow.md#session-start-checklist) (§ session-start checklist). The quick version: not on `main`, clean tree, `ls docs/handoffs/` for open work matching today's task.

