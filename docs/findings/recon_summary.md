# Phase 2 — Recon summary

**Date:** 2026-05-25.  **Branch:** `chore/phase2-recon` (off `chore/baseline-spec`).
**Scope:** investigate + report. No changes to `mtdnetwork/**`,
`evaluation.py`, or `environment.yml`. No pushes.

---

## Per-finding hooks (one paragraph each)

1. **[crash_6000s.md](crash_6000s.md) — "~6 ks crash" diagnosis.** Not a Python
   exception; a silent integrity failure. Root cause is three interacting
   defects (R1: `is_compromised` hard-codes `> 0.25`; R2: `_mtd_trigger_action`
   `succeed()`s without `return`; R3: `_mtd_execute_action` early-returns
   on `is_compromised` without releasing its resource slot). On the
   PRIMARY config (`total_nodes=100`, seed 42), the chain fires at
   sim_t ≈ 6,500 s; MTD count freezes and 95 % of hosts compromise by
   t=15 ks. Repro is one Python block, reproduced today. **F-06 and F-07
   are not implicated.** Introducing commits are moebuta `6a7a2907`
   (2022-09-25, R3) + `e369b09` (2023-03-19, R2) + Will Ho `6ae1fd4`
   (2024-09-08, R1). Recommended fix locations identified; nothing fixed.
2. **C6 provenance** (folded into [crash_6000s.md](crash_6000s.md) §4).
   Full timeline `0.9 → 0.7 → 0.8 → 0.25` traced; the 0.25 lands in Will
   Ho's commit message-less `debug` commit (2024-09-08), with the previous
   `> 0.8` line left in as a comment. No paper rationale anywhere. **C6 is
   a debug-leftover bug, not a deliberate divergence.**
3. **[replay_viz_inventory.md](replay_viz_inventory.md) — `feat/replay-viz`
   inventory + cherry-pick plan.** 46 commits ahead of `main` categorised
   into substrate-fix (2: `c426f1b`, the substrate slice of `0d1bdae`),
   substrate-hygiene (1: parts of `1efac8f`), reorg (don't pick),
   visualisation (deprioritised through 22 May), GAP/GASP attacker (Stream
   A/B, not substrate), and notebook noise. Explicit apply order for the
   fix session, including which `_emit(...)` / `drain_in_flight()` /
   budget-assert pieces of `0d1bdae` to *exclude* because they presume an
   `EventLogger` the inherited code doesn't have.
4. **[attackflow_schema.md](attackflow_schema.md) — `.afb` schema audit.** No
   local `.afb` files (`notebooks/attack-flow/attack-flow-main/corpus/` is
   gitignored). Audit done against a freshly-downloaded corpus file
   (`Black Basta Ransomware.afb`) and a static read of Marc's parser on
   `feat/replay-viz`. Today's published corpus is still tagged
   `"schema": "attack_flow_v2"` despite v3.0.0 / v3.1.x application
   releases — Marc's parser works on it (41 edges from 38 actions,
   verified). Recommendation: **document, don't migrate**, with three
   small parser hardenings noted for Stream A hygiene.
5. **[tay_rl_feasibility.md](tay_rl_feasibility.md) — Tay RL feasibility.**
   TF 2.21 / Keras 3.14 already in `mtdsim` env; `mtd_ai` imports OK;
   `create_network` builds the two-branch DDQN at the spec'd layer counts;
   Tay's deleted pretrained weights (`main_network_*.h5`) **still load**
   under current TF; a 2 ks `mtd_ai` sim runs end-to-end with a fresh
   random-init model. **C4 resolved** — `_register_mtd_ai` exposes
   Tay's 5-action set (4 + no-op), not Ho's pairwise space. **Load-bearing
   caveat:** Tay's model expects 8 static + 3 time-series features;
   current `Evaluation.get_metrics` returns 7 + 3 (drops `exposed_endpoints`
   and `attack_type`, substitutes `total_number_of_ports`). Replication
   needs to wire those two missing features back in. **Trust caveat:** AI
   surface inherits R1 + R3 from the procedural surface (R2 is correctly
   handled). The env delta (TF) is documented but not committed.
6. **Spec hygiene.** All 12 `[IDS-SEAM]` tags in `docs/spec/MTDSIM_SPEC.md`
   retired: SHD-05 / SHD-06 / SHD-10 / SHD-13 → `[TAY-BENCH]`;
   L4 metrics MET-02 (ASR) / MET-05 (APE) → `[EVAL]`; the remaining six
   metric rows (MET-03 MEF / MET-04 HCR / MET-08 TSLM / MET-09 SAPV /
   MET-10 NAV / MET-11 Attack Stage) → `[PERIPH]`. Legend updated with
   provenance pointer back to this document.

---

## Dispositions — what each finding implies

| # | Open disposition (from spec / Marc's queue) | Pre-Phase-2 status | Phase-2 readiness call |
|---|---|---|---|
| **C6** (NCR termination ratio 0.25 vs Zhang 0.8) | "Bug or deliberate change? Top priority to disposition." | **Disposition as bug.** Will Ho's `6ae1fd4` "debug" — no paper basis, no message body, no PR. Fix is one line + storing the constructor arg on `self`. Schedule in the fix session as R1. |
| **C7** (ATK-03 exploit-time formula deterministic vs Zhang's exponential) | "Decide whether to faithfully reimplement or accept inherited reality." | **No new evidence.** Phase 2 did not touch the exploit-time formula. Decision still on Marc — recommendation unchanged from the spec (defer; not blocking the fix session). |
| **C8** (MET-04 HCR field semantics — F-10) | "Field used by downstream code; fixing it small but ripples." | **Schedule after the fix session, not during.** Marc's `1efac8f` zero-division guards preserve the current numerator semantics; an actual semantic flip to `C_t / T_host` would touch the AI feature pipeline (used by Tay's pretrained model). Land R1+R2+R3 first; then disposition C8 against the regenerated goldens. |
| **MTD-14** (Zhang Table 3 vs `MTD_DURATION` constants — `CompleteTopologyShuffle` 120 vs 110, `IPShuffle` 110 vs 100) | Unresolved in spec. | **No new evidence.** Two-line edit in `constants.py` once Marc decides whether to honour Zhang. Not blocking. Recommend bundling with the fix session as a separate trivial commit so the golden diff is attributable. |
| **C4** (MTD action set — Tay 5 vs Ho pairwise) | "Conflict candidate." | **Resolved: Tay's 5-action set.** `_register_mtd_ai` + `MTDAIOperation` smoke-run confirm action_size = `len(strategies) + 1` (= 5 with default 4 strategies, where 0 = no-op). Spec rows SHD-03 `verified`, SHD-04 `out-of-scope`. Updated `[TAY-BENCH]` tag already reflects this. |
| **procedural-attacker-fate** (6-phase scripted attacker retained as baseline alongside GASP) | "Both must work and both must be faithful" (CLAUDE.md). | **Keep, do not deprecate.** Phase-2 evidence is consistent — the 6-phase attacker is the load-bearing baseline for every Phase-0 golden, runs cleanly to 15 ks at PRIMARY once R1+R2+R3 land, and is what Tay's RL agent is trained against. CLAUDE.md framing stands. |

## What this session changed in the tree

- Added `docs/findings/crash_6000s.md`, `replay_viz_inventory.md`, `attackflow_schema.md`, `tay_rl_feasibility.md`, `recon_summary.md` (this file).
- Edited `docs/spec/MTDSIM_SPEC.md` to retire `[IDS-SEAM]` (12 rows + legend).
- Untracked CRLF↔LF churn from finding F-09 was stashed and left untouched (`stash@{0}: On phase2-recon: phase2-tmp-line-endings`); the older `stash@{1}: On attacker-profiling: wip: .gitignore line-ending flip` was also left alone.
- No code changes. `mtdnetwork/**`, `evaluation.py`, `environment.yml` all unchanged.
- Branch `chore/phase2-recon` did not push.
