# `feat/replay-viz` inventory & cherry-pick plan

**Phase:** 2 (recon).  **Date:** 2026-05-25.
**Branches surveyed:** `feat/replay-viz` (46 commits ahead of `main`).
**Companion branch:** `feat/attacker-profiling` (subset of the same chain, fewer late commits).

> "Substrate" here = anything that, if cherry-picked onto `chore/baseline-spec`,
> would change the *behaviour or correctness* of a Phase-0 baseline scenario
> (no-MTD or single/multi-MTD on `mtdnetwork/`). It explicitly excludes
> visualisation, the `src/mtdsim/` package reorg, and the GAP/GASP attacker
> code — those are Stream A/B work that needs the substrate stable before
> being meaningful.

---

## Categorisation summary

| Bucket | Commits | Action this session |
|---|---|---|
| **A. Substrate fix** — fixes a bug in inherited Tay-era code; equally applicable to `mtdnetwork/` | **2 commits** (one direct, one bundled inside a "kitchen-sink" commit) | **Cherry-pick in the fix session.** |
| **B. Substrate hygiene** — robustness/division-by-zero guards on `Evaluation` + `MTDAIOperation` math | **1 commit** (parts of `1efac8f`) | Cherry-pick with care — overlaps F-10 (HCR semantics). |
| **C. Reorg** — moves `mtdnetwork/` → `src/mtdnetwork/` → `src/mtdsim/`. No behaviour change beyond import paths. | **2 commits** | **Do not cherry-pick** for the substrate session. Reorg is Phase 3 scope. |
| **D. Visualisation / replay UI** — Dash app, replay viewer, network panel, event-log schema | **~12 commits** | **Deprioritised** per Marc's 29 April brief ("half-built … deprioritised through lit-review deadline"). |
| **E. GAP/GASP attacker** — Stream A/B work (graph construction, subgraphing, motivation enrichment, SubgraphAttackerProfile) | **~20 commits** | **Stream A/B**, not substrate. Out of scope for the fix session. |
| **F. Notebook noise** — notebook output refreshes, kernel-spec bumps, docs-only commits, GAP edge updates | **~9 commits** | Ignore. |

---

## A. Substrate fixes — cherry-pick

### `c426f1b` "Ensure MTD resource release and cleanup" (2026-04-23, single-file)

- **Touches:** `src/mtdsim/defender/mtd_operation.py` (the reorged twin of `mtdnetwork/operation/mtd_operation.py`).
- **What it fixes:** Defect R3 in [crash_6000s.md](crash_6000s.md) — wraps `_mtd_execute_action`'s post-`yield-request` block in `try` / `finally`, releases the simpy resource in the `finally` only if `request in resource.users`, pops `unfinished_mtd[resource_type]`. Pre-emptive against generator interrupts and against the early-return-on-`is_compromised` leak.
- **Why cherry-pick:** Smallest possible diff that closes R3 on `mtdnetwork/`. Adapt by porting the `try`/`finally` shape into [mtdnetwork/operation/mtd_operation.py:156-191](../../mtdnetwork/operation/mtd_operation.py#L156-L191).
- **Pitfall:** Marc's version on `feat/replay-viz` also calls `self._emit(...)` inside the `try` block. The inherited `mtdnetwork/` has no `EventLogger` — strip the `_emit` calls when porting or the cherry-pick will `AttributeError`.

### `0d1bdae` "large set of changes" (2026-05-07, kitchen-sink)

> This commit bundles a doc dump, a Petri-net notebook, replay-viewer UI, **and** three substrate fixes. Cherry-pick only the substrate slice (`src/mtdsim/network/time_network.py` + the `_mtd_trigger_action` `return` in `src/mtdsim/defender/mtd_operation.py` + the `end_event.triggered` gates in `src/mtdsim/attacker/attack_operation.py`). The viewer/notebook portions are bucket D and should be dropped at apply time.

Three substrate slices worth pulling:

1. **R1 fix** (`src/mtdsim/network/time_network.py`) — stores `terminate_compromise_ratio` on `self` and uses it in `is_compromised`. Maps 1:1 to [mtdnetwork/component/time_network.py:10-22, 47-50](../../mtdnetwork/component/time_network.py#L10-L50). Comment in Marc's version: *"Threshold is configurable via the constructor's terminate_compromise_ratio so callers (e.g. ReplayConfig) can match the simulation horizon."* No replay-viz coupling — pure C6 closure.
2. **R2 fix** (`src/mtdsim/defender/mtd_operation.py` `_mtd_trigger_action`) — adds an explicit `return` after `end_event.succeed()`. Marc's inline comment: *"Stop scheduling new MTDs once the end_event has fired; the batch variant already does this. Without the return, every subsequent trigger spawns an _mtd_execute_action that bails out before mtd_completed, producing orphan deploys."* Single-line change at [mtdnetwork/operation/mtd_operation.py:75-80](../../mtdnetwork/operation/mtd_operation.py#L75-L80).
3. **R2-attacker gate** (`src/mtdsim/attacker/attack_operation.py`) — three `if self.end_event.triggered: return` guards in `_execute_attack_action`, `_handle_interrupt`, and the exploit-vuln loop. Stops the *attack* trace from gaining new phases after the sim has ended. Equivalent insertions in [mtdnetwork/operation/attack_operation.py:60, 133, 269](../../mtdnetwork/operation/attack_operation.py).

Three substrate slices to **leave behind** (replay-viz-only):

- `_emit_alloc_state(...)` helper and all `_emit(...)` call sites — they depend on `event_logger`.
- `_in_flight_deployments` dict + `drain_in_flight()` — useful only to a caller that uses `AnyOf(end_event, env.timeout(...))` as the run terminator, which `baseline/run_baseline.py` does not.
- `_MTD_EXECUTION_BUDGET_MULTIPLIER` assert — fine in principle but trips Zhang's exponential MTD-duration tail (5× the mean has non-trivial probability). Re-introduce only with a budget tuned per technique.

---

## B. Substrate hygiene — cherry-pick with care

### `1efac8f` (parts) "Add retrain DDQN notebook; AI/operation fixes" (2026-03-30)

Marc-authored guards that prevent `ZeroDivisionError` on degenerate runs in `src/mtdsim/stats/evaluation.py` and `src/mtdsim/ai/mtd_ai_operation.py`. Specific bits worth porting:

| Marc's diff slice | Equivalent in `mtdnetwork/` | Why |
|---|---|---|
| `mtd_execution_frequency`: `elapsed > 0` guard | [evaluation.py:80](../../mtdnetwork/statistic/evaluation.py#L80) | A sim where no MTDs fire (no-MTD scenario already short-circuited on `len==0`; but the *single*-MTD-that-was-suspended case from R3 ends up with one record only and `finish - start == 0`). |
| `time_to_compromise`: `attack_action_count > 0` guard | [evaluation.py:106-108](../../mtdnetwork/statistic/evaluation.py#L106-L108) | Otherwise divides by 0 when no SCAN_PORT / EXPLOIT_VULN / BRUTE_FORCE actions made it under the checkpoint. |
| `attack_success_rate`: `attack_event_num > 0` guard | [evaluation.py:116](../../mtdnetwork/statistic/evaluation.py#L116) | Same root cause; observable in the golden no-MTD run when early checkpoints have zero SCAN_PORTs. |
| `host_compromise_ratio`: `comp_num > 0` guard | [evaluation.py:124](../../mtdnetwork/statistic/evaluation.py#L124) | Trivial. |
| `host_compromise_ratio` (state metric): `host_count > 0` guard | [evaluation.py:153](../../mtdnetwork/statistic/evaluation.py#L153) | Trivial. |
| Fix typo `plt.savefig(directory + '/experimental_data/plots/',+ '/network.png')` → single concatenated path | [evaluation.py:208, 266](../../mtdnetwork/statistic/evaluation.py#L208) | This is Phase-0 finding **F-08** ("hard-coded path-join bugs in visualise_*"). Marc fixed two of them; check whether all instances are covered. |

**Pitfall:** F-10 (HCR-field semantics divergence from Ho's paper) is *not* fixed by these guards — they only guard against zero-division, they preserve the `comp_num` (= `T_host × checkpoint_ratio`) numerator that diverges from the paper. Don't bundle an F-10 semantic change into the same cherry-pick.

Other parts of `1efac8f` — the DDQN notebook, the `attacker_sensitivity=1.0` default, the duplicate-scorer-registration removal in `mtd_ai_operation.py` — are **MTD-AI scope**, not substrate. Cover them when the Tay-RL feasibility work (see [tay_rl_feasibility.md](tay_rl_feasibility.md)) lands.

---

## C. Reorg — do **not** cherry-pick this session

- `b076645` "Move mtdnetwork package into src/" (2026-03-27).
- `bb2adf5` "Restructure package namespace to mtdsim" (2026-03-29).

These two together move `mtdnetwork/` → `src/mtdnetwork/` → `src/mtdsim/` and split `component/` into `network/` + `attacker/` + `defender/`, and `statistic/` into `stats/`. Once-and-done refactor. **Cherry-picking would invalidate every locator in [MTDSIM_SPEC.md](../spec/MTDSIM_SPEC.md) and every Phase-0 golden path.** Defer until the substrate fixes have landed and the spec line-numbers can be re-validated in one batch.

`9b4fd3d` "Revise README and conda env (mtdsim)" is also reorg-adjacent (env rename `mtdsimtime` → `mtdsim`); already implicit in Phase-0's deviation table, no cherry-pick needed.

---

## D. Visualisation / replay UI — deprioritised

Per `docs/current_state.md` (29 April): *"Operationalisation visualiser half-built. … **Deprioritised through lit-review deadline (22 May).**"*

Commits flagged for **post-22-May** review only:

- `1bca838`, `fb0468b`, `dd7eff0`, `8bcf5cc` — replay viewer (Dash app skeleton, GAP iframe wiring, Run/Profile tabs).
- `146c552` — event-log JSON Schema lock (`docs/event_log.md`, `docs/schemas/event_log.schema.json`, `schema_version: "1.0"` stamp). Useful once the substrate is healthy, but the schema describes events the inherited code doesn't yet emit.
- `0366e35` — adds `EventLogger` sidecar **and** `SubgraphAttackerProfile` in one commit; the SubgraphAttackerProfile portion is bucket E, the EventLogger portion is the prerequisite for D. Splitting this commit when it eventually comes back is non-trivial — note for the visualisation re-prioritisation pass.
- Marc's three `tests/test_*.py` files added in `0d1bdae` (`test_components.py`, `test_integration.py`, `test_replay_sim_regression.py`, `test_layout_render.py`, `test_pipeline_smoke.py`) — test scaffolding that imports `src/mtdsim/` only. Could be re-pointed at `mtdnetwork/` for the substrate fix-session golden-master tests, but that's its own piece of work.

---

## E. GAP/GASP attacker — Stream A/B

Listed for completeness; **none cherry-picked in this session** because they presume `src/mtdsim/`, the GAP/GASP corpus, and the new `AttackerProfile` plumbing.

| Commit | Subject | Stream |
|---|---|---|
| `63aeb32` | Add attacker profiling & MITRE integration | A → B |
| `5dfebbd` | Add MITRE attacker profiles; tweak notebook | A |
| `b2cb4cc`, `ad2c158`, `298687a`, `a078fcc`, `7a9d681`, `94c4abb` | ATT&CK + Attack Graph Design Schema iterations | A |
| `c4cf78c`, `c4e8651` | Co-occurrence index + evidence-scored edges | A |
| `eb33810` | GAP dataset and viz/enrichment modules | A |
| `52dfae3` | ATT&CK motivation exploration notebook | A |
| `786c867` | MTD literature-review notebook | A (lit) |
| `b2812fd`, `b79129d`, `069dfd0`, `244024b`, `fe1029b`, `e54a0bc` | GAP subgraphing + selectors + v0.4 edges | A |
| `0366e35` (partial) | `SubgraphAttackerProfile` + per-phase technique sampling | B |
| `b8060c6` | Refresh notebook outputs and adjust network params | A (output refresh) |

---

## F. Noise / docs-only

`6924be1` "Run notebook" · `0d4867b` "Update .gitignore" · `9ff2c25` "Merge branch …" · `0af1d2b`, `2748f58`, `75e7d0d`, `1915de7`, `54f6d67`, `bd8b27d` — notebook re-execution, deps relaxation, docs-only.

---

## Apply order for the fix session

> One commit per fix, atop `chore/baseline-spec`. Re-run Phase-0 goldens
> between (1) and (2) so any byte-level golden movement is attributable to
> the single fix in flight.

1. **R1** — port C6 fix from `0d1bdae:src/mtdsim/network/time_network.py` onto `mtdnetwork/component/time_network.py`.
2. **R3** — port `c426f1b`'s `try`/`finally` shape onto `mtdnetwork/operation/mtd_operation.py::_mtd_execute_action`, *minus* `_emit(...)` calls.
3. **R2** — single-line `return` after `succeed()` in `_mtd_trigger_action`.
4. **R2-attacker** — three `end_event.triggered` early-returns in `mtdnetwork/operation/attack_operation.py`.
5. **B** — the five zero-division guards from `1efac8f` listed in §B. Smallest blast radius last; ship together if the test surface allows.

Order matters because (1) shifts the trigger time from ~6.5 ks back to ≥ 15 ks at PRIMARY, which means goldens at `finish_time=3000` will not move under (1) alone; (2)/(3)/(4) close the leak path that goldens at `finish_time=3000` also don't hit, so they should be byte-stable in isolation; (5) is observable only on degenerate edge cases.
