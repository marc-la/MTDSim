# Project context

**Status:** durable. Slowly-changing background about what this repo is and the research it serves. Update when the thesis pivots, not for incidental work.

## Project

- Repo: a fork of **MTDSimTime** (`main`), a discrete-event simulator for evaluating Moving Target Defence (MTD).
- Owner: Marc Labouchardiere — UWA honours (CSSE), supervised by Dr Jin Hong.
- Thesis (current — **supersedes the proposal**): evaluate *existing* MTD mechanisms against behaviourally-grounded adversarial profiles derived from CTI. **Single RQ. No sub-problems.**
- IDS is **not** a research thread (culled; folded into lit-review §1.3 only). Do **not** build IDS/detection features. Tay's RL agent and its detection-sensitivity machinery are retained only as an inherited **benchmark defence mechanism to replicate** — never to extend, and **deferred to the evaluation/ablation phase** (later in semester), not current work.

## Direction & scope

Governs all prioritisation.

- The simulator is the **L3/L4 execution substrate** for: L0 raw CTI → L1 GAP (attack graph; nodes = ATT&CK techniques) → L2 GASP (motivation subgraph) → L3 OGASP (attacker-agent traversal in MTDSim) → L4 evaluation.
- Load-bearing seam = the **attacker module**: graph-driven (GASP) traversal is added *alongside* the inherited 6-phase scripted attacker, which is **retained as the procedural baseline** (the substrate Tay's RL trained against and the basis of every golden). Both must work; both must be internally consistent.
- Defence side = **existing mechanisms only** (SDR family + Tay's AI selection). No new defender mechanisms; no training novel RL agents from scratch.
- Evaluation metrics that matter: **MTTC, ASR, attack-path exposure, RoA.** Prioritise faithfulness fixes that feed these. (E1 finding from Phase 3: end-of-sim compromise fraction is a poor discriminator at long horizons — MTTC/attacker-effort discriminate.)
- **Primary metric is internal MTTC** on the corrected substrate (post-2b). C6 (compromise ratio) was a debug-commit bug, fixed to 0.8 (= Zhang NCR) — **not** a divergence. The `internal`/`lineage` preset was **evaluated and DROPPED**: after C6→0.8 it would distinguish only MTD durations (MTD-14, fixed to Zhang's values in 2c) plus two *unimplemented* behaviours, so there is **one canonical substrate**. The only substrate divergences from the published lineage are **C7** (deterministic exploit time) and **ATK-04** (no attacker learning) — both unimplemented and documented in [`metrics_semantics.md`](metrics_semantics.md). Within-substrate comparison is valid; cross-paper numeric comparison to Zhang/Tay is **INVALID**.
- **~6,000s "crash" — RESOLVED (Phase 2b):** diagnosed as a *silent integrity failure* (R1 hardcoded compromise ratio, R2 missing return, R3 simpy resource leak), not an exception. Fixed; substrate runs clean to 15 ks (75 MTDs, no premature end), SIM-05 determinism verified, baseline re-captured on the corrected substrate.

## Codebase lineage

So cross-paper overlap reads as evolution, not contradiction.

Brown 2023 (foundational MTDSim) → Zhang 2023 (MTDSimTime: time domain, MTTC, MTD execution schemes, adversary profiles) → Ho 2024 (metrics suite + RL) → Tay 2024 (MTDShield: reactive RL plugin).

Brown is the reference implementation; the rest are systematic updates to it.

Per-paper extraction notes live in [`../extractions/`](../extractions/).
