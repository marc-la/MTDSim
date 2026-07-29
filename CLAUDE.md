# CLAUDE.md

Entry point. **Load the durable context before doing anything that touches code, docs, or specs.**

This file is intentionally lean. The always-true background, rules, and conventions live in [`docs/workflows/`](docs/workflows/) — load them per session rather than caching them here. Task-specific scope and step lists arrive in the prompt I paste; the workflow files describe what's true regardless of the task.

Harness configuration (permission allowlists, hooks, skills) lives in [`.claude/`](.claude/).

## Read first, every session

All six, in order. If you read only one for orientation, read **`project_context.md`** (#3) — the "what this project is" document; the others govern behaviour.

1. [`docs/workflows/guardrails.md`](docs/workflows/guardrails.md) — non-negotiables: branch hygiene, never-commit-to-main, never-push, scope discipline, working standards.
2. [`docs/workflows/session_workflow.md`](docs/workflows/session_workflow.md) — the stage-commit (no-push) flow, handoff / notes lifecycles, session-start checklist.
3. [`docs/workflows/project_context.md`](docs/workflows/project_context.md) — the project, the thesis direction, the codebase lineage. What "load-bearing" means here.
4. [`docs/workflows/docs_map.md`](docs/workflows/docs_map.md) — where every document lives and the placement criterion for new ones; repo layout and environment.
5. [`docs/workflows/notes_rubric.md`](docs/workflows/notes_rubric.md) — the quality gate for anything written into `docs/notes/`. Load in full before writing or editing a note.
6. [`docs/implementation/apt_model_criterion.md`](docs/implementation/apt_model_criterion.md) — the APT-attacker-model criterion (supervisor S6): the literature-derived rubric this model is scored against, with the honest per-axis badges. Loaded every session by supervisor direction; it is the yardstick for all current L3 work and the ceiling on what may be claimed.

## The docs system, in one paragraph

Everything in `docs/` feeds one of two consumers: **the dissertation** ([`docs/thesis/dissertation.tex`](docs/thesis/dissertation.tex)) or **future sessions**. Dissertation-bound prose lives in [`docs/notes/`](docs/notes/), organised by dissertation *chapter* (ch1–ch7 subdirs) and gated by the notes rubric — every note is aimed at the chapter it will land in. Codebase-shaped truth (schemas, dispositions, decision registers, investigation records) lives in [`docs/implementation/`](docs/implementation/), with per-stage detail under `implementation/pipeline/{gap,gasp,ogasp}/`. Open work briefs live in [`docs/handoffs/`](docs/handoffs/); literature in [`docs/sources/`](docs/sources/) (gitignored) with tracked extracts in `docs/sources/extractions/`. When creating any document, run the placement criterion in `docs_map.md`. Dissertation-bound prose additionally carries a voice contract — [`docs/workflows/voice.md`](docs/workflows/voice.md): default for `notes/`, hard gate for `thesis/`; load it before drafting either.

## Implementation specs (load when relevant to the task)

- [`docs/implementation/architecture.md`](docs/implementation/architecture.md) — L0→L4 pipeline, substrate seam, methodological positioning, decisions log.
- [`docs/implementation/substrate_primer.md`](docs/implementation/substrate_primer.md) — the inherited simulator as adversarial terrain (attacker's-eye view).
- [`docs/implementation/pipeline/gap/gap_schema.md`](docs/implementation/pipeline/gap/gap_schema.md) — L1 GAP data model + construction decisions.
- [`docs/implementation/pipeline/gasp/gasp_schema.md`](docs/implementation/pipeline/gasp/gasp_schema.md) — L2 GASP data model + partition provenance (sibling files in the same dir).
- [`docs/implementation/pipeline/ogasp/`](docs/implementation/pipeline/ogasp/) — L3 execution-model records (supervisor decision register, Petri feasibility study).
- [`docs/implementation/mtdsim_spec.md`](docs/implementation/mtdsim_spec.md) — the conformance spec; row-level dispositions against the baseline.
- [`docs/implementation/mtdsim_intent_spec.md`](docs/implementation/mtdsim_intent_spec.md) — the **literature-only intent spec** (Brown 2023 primary; Zhang/Ho/Tay extensions). No code-side reasoning in it, by design: it is the independent yardstick for separating *bugs* from *design choices* — load it before classifying any behaviour as a bug, and audit against its IS-IDs rather than against paper memory. The row-by-row audit lives in [`docs/implementation/intent_conformance_audit.md`](docs/implementation/intent_conformance_audit.md) (classifications + open disposition list).
- [`docs/implementation/metrics_semantics.md`](docs/implementation/metrics_semantics.md) — internal MTTC definition, divergences (C7, ATK-04), comparability boundary.
- [`docs/implementation/provenance.md`](docs/implementation/provenance.md) — load-bearing constants → source → code → disposition.
- [`docs/implementation/trace_tool.md`](docs/implementation/trace_tool.md) — the event-log tracers (`python -m mtdnetwork.trace` for the substrate; `PYTHONPATH=src python -m mtdsim.l3_simulation.trace` for a movement run, unified across token / controller / substrate): first reach when verifying changes, pinpointing bugs, or demonstrating a run. Living tools — extend them rather than print-debug.

## Session-start checks

Run the full checklist in [`docs/workflows/session_workflow.md`](docs/workflows/session_workflow.md#session-start-checklist) (§ session-start checklist). The quick version: not on `main`, clean tree, `ls docs/handoffs/` for open work matching today's task.
