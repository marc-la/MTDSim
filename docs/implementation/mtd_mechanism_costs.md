---
status: reference
created: 2026-07-29
---

# What a grid costs — per-mechanism defender overhead, measured

The "what a grid costs" reference the 2026-07-29 MTD mechanism cost audit asked
for: per-mechanism wall-clock for one movement run, so the next experiment can
size itself instead of discovering the bill at row 207. Re-measure with
**`PYTHONPATH=src python tools/mtd_cost_bench.py --seeds 0 1 2`** on an idle
machine; if the harness needs changing to answer a new question, change it there
so the next measurement stays comparable.

## The table (post-fix, 2026-07-29)

Three seeds (0–2), idle machine, movement arm: `aggregate` profile, `v2_partial`
mapping, 15 000 s horizon, `single` scheme, 200 s interval. Mean seconds per run.

| mechanism | mean s | × no-MTD | in default pool |
|---|--:|--:|:--|
| *(no MTD)* | 0.11 | 1.0 | — |
| HostTopologyShuffle | 0.12 | 1.1 | no |
| IPShuffle | 0.12 | 1.1 | yes |
| PortShuffle | 0.14 | 1.3 | no |
| UserShuffle | 0.14 | 1.3 | no |
| ServiceDiversity | 0.50 | 4.6 | yes |
| OSDiversity | 0.63 | 5.7 | yes |
| CompleteTopologyShuffle | 1.03 | 9.5 | yes |
| **OSDiversityAssignment** | **2.13** | **19.6** | no |

**Read the absolute seconds, not the ratios, below ~1 s** — the no-MTD baseline is
~0.1 s, so sub-second ratios are load-noise (the audit handoff measured IP Shuffle
anywhere from 1.0× to 3.2× under contention). The structure that matters: every
mechanism now sits within ~20× of no-MTD, and the worst row is seconds, not
minutes.

## What changed — 128 s → 2.1 s for OSDiversityAssignment

The audit's headline defect: `MTDScheme._mtd_register` constructed a **fresh
mechanism instance on every registration**, so `OSDiversityAssignment`'s
checkpoint cache (`last_result` / `_checkpoint`) reset every cycle and its MIP
was built, serialised (243 000-line MPS) and solved on **all 75 mutations** of a
15 000 s run — ~128 s/run — when its own design intends ≤ 8 solves. The fix is a
per-scheme instance cache (`mtd_scheme.py`), plus hoisting the assignment-problem
construction (a full graph copy) into the solve branch
(`osdiversityassignment.py`); measured runs now solve 1–2 times. The fix is
general: any future mechanism carrying cross-mutation state gets the same
persistence.

Verification was field-for-field, not "numbers look similar":
`tools/mtd_golden_streams.py` (goldens in `baseline/golden_movement/`, subset in
the suite via `tests/test_mtd_golden_streams.py`) shows the seven stateless
mechanisms + no-MTD **bit-identical** across all 48 configs before/after; the six
OSDiversityAssignment configs moved as expected (cached vs per-mutation
assignments) and were re-baselined — `baseline/CHANGELOG.md` 2026-07-29.

**What was *not* changed.** The solve itself still decides nothing — the DAP
formulation's assignment binaries are uncoupled from its flow variables and CBC
presolve deletes the model (intent audit §m3, disposition **D-17**, awaiting
Marc). The 2.1 s figure is the cost of the *degenerate* solve at checkpoint
frequency; option (a) of D-17 (repairing the formulation) would raise it, option
(b)/(c) would remove it. The sub-second mechanisms were left untouched: their
candidate micro-optimisations (the `seen`-list membership in
HostTopologyShuffle, the per-host `max()` recompute in the DAP scorer) buy
milliseconds against a churn risk the goldens would have to re-arbitrate —
recorded, not taken.

## Grid arithmetic

On the 23-condition × 5-profile × 2-arm × 30-seed demonstration-arms matrix, the
300 OSDiversityAssignment runs cost **~10.6 minutes** at 2.13 s (they were
**~10.7 hours** at ~128 s — the mechanism alone was ~85 % of the grid bill). A
full eight-mechanism single-scheme sweep now costs, per 30 seeds and per arm,
roughly `30 × Σ(mean s) ≈ 30 × 4.9 s ≈ 2.5 min` of defender-side overhead — the
grid's cost is back to being dominated by run count, not by one defective
mechanism.

## Provenance

- Pre-fix numbers (single seed, loaded machine): the table in the audit handoff,
  preserved in git history with `docs/handoffs/2026-07-29_mtd_mechanism_cost_audit.md`.
- Profile evidence for where the 128 s went (75× `objective()`, ~200 s PuLP model
  build under profiler, 42 s `writeMPS`, CBC "0 rows, 0 columns"): same handoff,
  §"Why OSDiversityAssignment is slow".
- Classification of every finding against the intent spec:
  `intent_conformance_audit.md` §m3 (IS-MTD-08 → D-17; §l item 10 for the seam).
