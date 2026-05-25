# Build Carry-Forward — threads surfaced during build sessions

**Author:** Marc Labouchardiere (23857377)
**Purpose:** A running register of threads that surfaced while building/fixing the simulator but
belong to a *later* phase (evaluation/ablation, methodology Ch. 3, or build hygiene), plus the
certified substrate state. Complements `methodology_carryforward.md` (lit-review off-cuts); this
captures build-session off-cuts. Marc-maintained — update Status as items move.

**Status legend:** `open` (needs a decision/action) · `deferred` (parked to a named later phase) ·
`ongoing` (a practice to keep) · `done`.

---

## Substrate state — certified post-2c

The inherited substrate is now **stable, faithful (on the items below), deterministic, and tested**,
and runs clean to 15 ks. Per-commit deltas are canonical in `baseline/CHANGELOG.md`; this is the
reference summary.

**Matches the published lineage on:** NCR = 0.8 (Zhang §5; fixed 2b/R1) · `MTD_DURATION` = Zhang
Table 3 verbatim (2c/MTD-14) · HCR = C_t / T_host (Ho 2024 §3.3.2 #4; 2c/C8).

**Two documented divergences remain** — both *unimplemented*, both shift *absolute* MTTC magnitude
(prose in `docs/METRICS_SEMANTICS.md`): C7 — deterministic exploit time `ATTACK_DURATION ×
(1−complexity)` vs Zhang's exponential `T_Aphase2` (`services.py:80`); ATK-04 — attacker-learning
halving missing (`services.py:87`, commented stub). → Within-substrate comparison valid; cross-paper
numeric comparison to Zhang/Tay INVALID.

**2c re-baseline headline (seed=1234, fin=15000):**

| Scenario | attacks 2b→2c | MTDs 2b→2c | summary HCR 2b→2c | driver |
|---|---|---|---|---|
| no-mtd | 692 → 692 | 0 → 0 | 0.82 → 0.82 | — (regression control held) |
| single-ipshuffle | 997 → 1228 | 52 → 75 | 0.82 → 0.70 | MTD-14 (IPShuffle 110→100) |
| random-multi | 994 → 875 | 47 → 42 | 0.82 → 0.82 | MTD-14 |
| primary-random-15k (100n, seed 42) | 1477 → 1366 | 75 → 65 | 0.81 → 0.81 | MTD-14 |

`evaluation.json` HCR column flipped from a >1 shape (~[1.20…1.04], the C8 bug) to ~[0.06…0.26]
across all 9 scenarios — the direct C8 effect. HCR ∈ [0,1] now enforced by
`tests/test_crash_fix_regressions.py::test_c8_host_compromise_ratio_in_unit_interval`.

---

## Phase 3 close-out — done (2026-05-25)

Reframed Phase 3 complete. `src/` relocation **declined** (recorded decision, not a gap — the deleted
`src/mtdsim/` scaffolding was empty of `.py` sources; relocating the live `mtdnetwork/` package was
out of scope for substrate certification). EOL normalised (F-09, commit `76703b0` — closes H2);
working-tree cleanup (`.DS_Store` untracked + gitignored); provenance anchored
(`docs/PROVENANCE.md`, commit `5bfbc42`); ATK-04 disambiguated (commit `ea6daac`,
`docs/METRICS_SEMANTICS.md §c`, `MTDSIM_SPEC.md ATK-04`) — **ATK-04a** per-instance re-exploit
discount **active/kept** (Brown-era `services.py:86–87`, pinned by
`tests/test_atk04_reexploit_discount.py`), **ATK-04b** per-type attacker learning
**unimplemented** (commented stub `services.py:87`; refines D1).

Next gate is the open **Jin decisions** before the Stream B build: Stream A-vs-B priority;
attacker-integration scope (minimal seam vs broader); replay/viz sequencing (D2).

**ATK-04a is now a live input to the attacker-model design** — the CTI/GASP attacker must decide
whether to inherit, replace, or extend the existing per-instance discount.

---

## Evaluation design (methodology Ch. 3 inputs)

| ID | Note | Pick-up trigger / action | Status |
|---|---|---|---|
| E1 | **End-of-sim HCR does not discriminate defences at a 15 ks horizon — now CONFIRMED by the 2c numbers.** `no-mtd` and every multi-MTD scenario land at HCR 0.82 (41/50); only single-ipshuffle moved it (0.70). The signal is in attacker *effort* (692 → 875 → 1228 attack-events) and MTD count/MTTC, not final compromise fraction. | Before locking the Stream C eval harness: use MTTC / attacker-effort / *time-to-threshold* (e.g. time to X% compromise); decide the horizon deliberately. Do NOT build the evaluation around end-of-sim HCR. | open |

## Benchmark / Stream C (Tay RL — deferred to eval/ablation phase)

| ID | Note | Pick-up trigger / action | Status |
|---|---|---|---|
| B1 | **Tay feature-vector mismatch.** Tay's pretrained model expects 8 static + 3 time-series features; the pipeline returns 7 + 3 (missing `exposed_endpoints`, `attack_type`). Any Tay benchmark before reconciling feeds the wrong distribution → measures the wrong thing. | At Stream C / eval phase: reconcile the feature vector, then decide reuse-vs-retrain. Not now. | deferred |
| B2 | **Model→ablation mapping.** Reconciling Tay's recovered `.h5` weights to his ablation configs is extensive git+thesis work. Start from the `siblings` column in `docs/findings/weights_index.md` (co-committed CSVs/configs/plots) — stronger than filenames. `provisional_label` is filename-only, UNVERIFIED. | Eval/ablation phase, if Tay benchmarks are needed. | deferred |
| B3 | **Weights single-point-of-failure.** 17 of 198 `.h5` blobs are history-only; the external archive (`mtdsim-weights-archive/`) is their sole durable copy until an off-disk backup exists. | Make one off-disk/cloud copy of the archive (116 MiB). Until then, never `git gc --prune` / rewrite history. | open |

## Decisions pending (Jin-gated)

| ID | Note | Pick-up trigger / action | Status |
|---|---|---|---|
| D1 | **C7 / ATK-04 implementation.** The two remaining substrate divergences (deterministic exploit time vs Zhang's exponential; no attacker-learning halving). Documented, not implemented. Affect absolute MTTC → cross-paper numeric comparison invalid. | Implement only if a genuinely lineage-faithful (cross-paper numeric) comparison becomes a requirement — Jin call. Else stays documented. | deferred |
| D2 | **Stream A vs B priority; attacker-integration scope.** B (operationalise GASP attacker) is now unblocked. Whether to harden A's output first, and whether the integration is a minimal attacker-seam vs broader, are open (current_state.md open decision #5). | Lock with Jin before committing weeks to the Stream B build. | open |

## Build hygiene

| ID | Note | Pick-up trigger / action | Status |
|---|---|---|---|
| H1 | **Terminal/branch discipline.** Mid-session branch switches from another terminal caused CRLF churn and partial-state risk. | Keep the session's terminal parked on its own branch for the session's duration. | ongoing |
| H2 | **CRLF normalisation (F-09).** Recurs on every entry — 2c hit a 19,356-line CRLF↔LF flip across 90 files (content-identical; `git diff -w` empty). | One-time `.gitattributes` + `--renormalize` chore AND set local `git config core.autocrlf input` (the repo fix alone won't stop recurrence). Prerequisite for Phase 3's byte-identical golden check. | open |
| H3 | **Untracked `tests/` dir.** A `tests/` dir was untracked on arrival (separate from the regression tests added in 2b). | Resolve deliberately — Tay's tests to keep / WIP / noise — before it's swept into an unrelated commit. | open |
| H4 | **`environment.yml` reconciliation.** Active env is `mtdsim` (Python 3.11.15); `environment.yml` still specifies `mtdsimtime` (3.9.13). Recorded in `baseline/BASELINE.md`; used as-is for 2c. | Reconcile `environment.yml` to the real env (and the CLAUDE.md Environment line, which a fresh session reads to activate). | open |
| H5 | **`baseline/BASELINE.md` stale.** Refers to Phase-0 / fin=3000 goldens throughout; diverges from the 2c goldens it describes. | Refresh, or add a one-line "superseded by 2c goldens; see CHANGELOG" pointer. | open |
| H6 | **Spec locator.** The impact-range row is `NET-13` (threshold = `NET-14`), not `NET-07` (= user-count). Fixed in spec during 2c. | Check no other doc/prompt references "NET-07 = impact range". | done |

## Tooling (optional)

| ID | Note | Pick-up trigger / action | Status |
|---|---|---|---|
| T1 | **MTDSim-conventions skill** (`skill-creator`) encoding package layout, dispositions discipline, test patterns — portable across Claude Code and Claude.ai. | Optional; worth it if session-to-session drift becomes a cost. | open |
