# Repo conventions

**Status:** durable. Update when the docs tree or environment changes.

## Documentation tree

The `docs/` tree has four subtrees, each with its own lifecycle. Putting a doc in the wrong subtree breaks the workflow — readers and future sessions will look in the wrong place.

| Subtree | Lifecycle | Contents |
|---|---|---|
| [`specs/`](.) | durable, slowly-changing canonical truth | this file, [`project_context.md`](project_context.md), [`guardrails.md`](guardrails.md), [`session_workflow.md`](session_workflow.md), [`mtdsim_spec.md`](mtdsim_spec.md), [`metrics_semantics.md`](metrics_semantics.md), [`provenance.md`](provenance.md) |
| [`../handoffs/`](../handoffs/) | live intra-session state; deleted when shipped | `YYYY-MM-DD_<topic>.md` — open work briefs for follow-up sessions |
| [`../notes/`](../notes/) | durable, kept | `YYYY-MM-DD_<topic>.md` — dissertation-worthy observations in plain English |
| [`../extractions/`](../extractions/) | durable, slowly-changing | per-paper extracts under copyright fair-use (`brown2023.md`, `zhang2023.md`, `ho2024.md`, `tay2024.md`) |
| [`../sources/`](../sources/) | **gitignored** | external source papers + lit review (verification targets); read from here, never commit them |

Each of `handoffs/`, `notes/`, `extractions/` has a `_template.md` to start from.

## Specs

- [`mtdsim_spec.md`](mtdsim_spec.md) — the conformance spec; verify-and-extend, dispositioned against the baseline. Row-level extract notes live per-paper in [`../extractions/`](../extractions/).
- [`metrics_semantics.md`](metrics_semantics.md) — definition of internal MTTC, the two divergences (C7, ATK-04), comparability boundary. (Authored in Phase 2c.)
- [`provenance.md`](provenance.md) — cross-link table: load-bearing constants and rules → source → code → disposition.

## Baseline

- [`../../baseline/golden/`](../../baseline/golden/) — the **canonical** seeded golden outputs (corrected substrate; the behavioural oracle; re-baselined in Phase 2c).
- [`../../baseline/golden_phase0_buggy/`](../../baseline/golden_phase0_buggy/) — superseded Phase-0 goldens from the 0.25 buggy substrate, kept for provenance.
- [`../../baseline/BASELINE.md`](../../baseline/BASELINE.md); [`../../baseline/CHANGELOG.md`](../../baseline/CHANGELOG.md) — every intentional re-baseline (what / why / spec-IDs).

## Environment

- Active env: `mtdsim` (Python 3.11.15). Note: [`../../environment.yml`](../../environment.yml) still nominally specifies `mtdsimtime` / 3.9.13 — the working env diverged (recorded in `baseline/BASELINE.md`); reconciling `environment.yml` to reality is an open housekeeping item.
- The Tay RL / benchmark path (`mtdnetwork/mtdai/`, `operation/mtd_ai_*.py`) runs under the current env (TF 2.21 / Keras 3.14; Tay's recovered pretrained weights load; mtd_ai smoke run completes). R1/R3 — which the AI surface had inherited — are fixed as of Phase 2b. Reuse-vs-retrain disposition lives in [`architecture.md`](architecture.md) §(a) Tay decision block (authoritative).
