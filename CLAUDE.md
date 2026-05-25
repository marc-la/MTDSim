# CLAUDE.md

Durable context for this repo. **Task-specific scope and step lists live in the prompt I paste per session** — this file is the always-true background and the rules that hold across every session. Phase-specific constraints from a task prompt (e.g. "audit only, don't change code") refine but never relax anything here.

## Project
- Repo: a fork of **MTDSimTime** (`main`), a discrete-event simulator for evaluating Moving Target Defence (MTD).
- Owner: Marc Labouchardiere — UWA honours (CSSE), supervised by Dr Jin Hong.
- Thesis (current — **supersedes the proposal**): evaluate *existing* MTD mechanisms against behaviourally-grounded adversarial profiles derived from CTI. **Single RQ. No sub-problems.**
- IDS is **not** a research thread (culled; folded into lit-review §1.3 only). Do **not** build IDS/detection features. Tay's RL agent and its detection-sensitivity machinery are retained only as an inherited **benchmark defence mechanism to replicate** — never to extend, and **deferred to the evaluation/ablation phase** (later in semester), not current work.

## Direction & scope (governs all prioritisation)
- The simulator is the **L3/L4 execution substrate** for: L0 raw CTI → L1 GAP (attack graph; nodes = ATT&CK techniques) → L2 GASP (motivation subgraph) → L3 OGASP (attacker-agent traversal in MTDSim) → L4 evaluation.
- Load-bearing seam = the **attacker module**: graph-driven (GASP) traversal is added *alongside* the inherited 6-phase scripted attacker, which is **retained as the procedural baseline** (the substrate Tay's RL trained against and the basis of every golden). Both must work; both must be internally consistent.
- Defence side = **existing mechanisms only** (SDR family + Tay's AI selection). No new defender mechanisms; no training novel RL agents from scratch.
- Evaluation metrics that matter: **MTTC, ASR, attack-path exposure, RoA.** Prioritise faithfulness fixes that feed these. (See `docs/direction/build_carryforward.md` E1: end-of-sim compromise fraction is a poor discriminator at long horizons — MTTC/attacker-effort discriminate.)
- **Primary metric is internal MTTC** on the corrected substrate (post-2b). C6 (compromise ratio) was a debug-commit bug, fixed to 0.8 (= Zhang NCR) — **not** a divergence. The `internal`/`lineage` preset was **evaluated and DROPPED**: after C6→0.8 it would distinguish only MTD durations (MTD-14, fixed to Zhang's values in 2c) plus two *unimplemented* behaviours, so there is **one canonical substrate**. The only substrate divergences from the published lineage are **C7** (deterministic exploit time) and **ATK-04** (no attacker learning) — both unimplemented and documented in `docs/METRICS_SEMANTICS.md`. Within-substrate comparison is valid; cross-paper numeric comparison to Zhang/Tay is **INVALID**.
- **~6,000s "crash" — RESOLVED (Phase 2b):** diagnosed as a *silent integrity failure* (R1 hardcoded compromise ratio, R2 missing return, R3 simpy resource leak), not an exception. Fixed; substrate runs clean to 15 ks (75 MTDs, no premature end), SIM-05 determinism verified, baseline re-captured on the corrected substrate.

## Codebase lineage (so cross-paper overlap reads as evolution, not contradiction)
Brown 2023 (foundational MTDSim) → Zhang 2023 (MTDSimTime: time domain, MTTC, MTD execution schemes, adversary profiles) → Ho 2024 (metrics suite + RL) → Tay 2024 (MTDShield: reactive RL plugin). Brown is the reference implementation; the rest are systematic updates to it.

## Always-on guardrails
- **Git:** work on a dedicated branch; never commit to `main`; commit locally for my review; **never push** without asking; never run destructive git (`reset --hard`, `clean -fd`, `gc --prune`, force-push). Keep the session's terminal parked on its own branch for the session's duration.
- **Scope:** stay inside the task's defined scope. *Flag* out-of-scope findings — don't action them. Prefer small, reviewable, line-level diffs over wholesale rewrites; ask before expanding scope or restructuring.
- **`feat/replay-viz`:** do not merge it wholesale. Pull only substrate-relevant fixes, as individually reviewed cherry-picks, per `docs/findings/replay_viz_inventory.md`. Take only the substrate slice of any pick that drags unrelated hunks. Visualisation and GAP/GASP commits are deferred (Stream A/B).

## Working standards
- **Papers are claims to reconcile with the code, not ground truth about it.** When a paper and the code disagree, record both; correct neither without a disposition from me.
- Distinguish an **inherited divergence** (the code's reality, to parameterise or document) from a **bug** (unintended; violates an invariant, or — as with C6 — entered via an unexplained "debug" commit with no paper basis). Fix bugs; don't preserve them as "inherited reality".
- **Never guess** a disposition or a locator. If you can't verify it, mark `unverified` / `verify` and state why.
- Don't assert that a paper is wrong (or that one paper contradicts another) — flag it "to verify" for me to resolve.
- When working across multiple papers, extract **one paper per pass** before merging, to prevent cross-attribution.
- Keep **inherited artefacts** distinct from **my own editorial/design choices**; track them separately.

## Repo conventions
- `docs/sources/` — external source papers + my lit review (verification targets). **Gitignored** (copyright); read from here, never commit them.
- `docs/direction/` — **my own** direction/intent docs (`current_state.md`, `methodology_carryforward.md`, `build_carryforward.md`); tracked, Marc-maintained. These state what the code is built *toward* and what's deferred — they are NOT specs and NOT verification sources, so never disposition code against them. Build-relevant items: Attack Flow `.afb` schema version (methodology_carryforward §3); SNAKES env decision (§5); deferred eval/benchmark/hygiene threads (build_carryforward). `current_state.md` is a 29 Apr snapshot — historical build context, superseded in specifics by the lit review.
- `docs/MTDSIM_SPEC.md` — the conformance spec; verify-and-extend, dispositioned against the baseline. `docs/spec/_notes_*.md` — per-paper extraction notes.
- `docs/findings/` — recon outputs (crash, replay-viz inventory, Attack Flow schema, Tay RL feasibility, weights_index, recon_summary).
- `docs/METRICS_SEMANTICS.md` — definition of internal MTTC, the two divergences (C7, ATK-04), comparability boundary. (Authored in 2c.)
- `baseline/golden/` — the **canonical** seeded golden outputs (corrected substrate; the behavioural oracle; re-baselined again in 2c). `baseline/golden_phase0_buggy/` — superseded Phase-0 goldens from the 0.25 buggy substrate, kept for provenance. `baseline/BASELINE.md`; `baseline/CHANGELOG.md` — every intentional re-baseline (what / why / spec-IDs).
- Australian English throughout.

## Environment
- Active env: `mtdsim` (Python 3.11.15). Note: `environment.yml` still nominally specifies `mtdsimtime` / 3.9.13 — the working env diverged (recorded in `baseline/BASELINE.md`); reconciling `environment.yml` to reality is an open housekeeping item.
- The Tay RL / benchmark path (`mtdnetwork/mtdai/`, `operation/mtd_ai_*.py`) runs under the current env (TF 2.21 / Keras 3.14; Tay's recovered pretrained weights load; mtd_ai smoke run completes). R1/R3 — which the AI surface had inherited — are fixed as of Phase 2b. **Deferred, low priority — an evaluation/ablation-phase task.** Do **not** retrain Tay's model now, and do **not** chase the known mismatch (model expects 8 static + 3 time-series features; pipeline returns 7 + 3, missing `exposed_endpoints`, `attack_type`) — reuse-vs-retrain belongs to that later phase (build_carryforward B1/B2). When fixing HCR/C8 in 2c, fix for metric correctness only; do **not** preserve fidelity to Tay's feature pipeline.