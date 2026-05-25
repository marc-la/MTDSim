# CLAUDE.md

Durable context for this repo. **Task-specific scope and step lists live in the prompt I paste per session** — this file is the always-true background and the rules that hold across every session. Phase-specific constraints from a task prompt (e.g. "audit only, don't change code") refine but never relax anything here.

## Project
- Repo: a fork of **MTDSimTime** (`main`), a discrete-event simulator for evaluating Moving Target Defence (MTD).
- Owner: Marc Labouchardiere — UWA honours (CSSE), supervised by Dr Jin Hong.
- Thesis (current — **supersedes the proposal**): evaluate *existing* MTD mechanisms against behaviourally-grounded adversarial profiles derived from CTI. **Single RQ. No sub-problems.**
- IDS is **not** a research thread (culled; folded into lit-review §1.3 only). Do **not** build IDS/detection features. Tay's RL agent and its detection-sensitivity machinery are retained only as an inherited **benchmark defence mechanism to replicate** — never to extend.

## Direction & scope (governs all prioritisation)
- The simulator is the **L3/L4 execution substrate** for: L0 raw CTI → L1 GAP (attack graph; nodes = ATT&CK techniques) → L2 GASP (motivation subgraph) → L3 OGASP (attacker-agent traversal in MTDSim) → L4 evaluation.
- Load-bearing seam = the **attacker module**: graph-driven (GASP) traversal is added *alongside* the inherited 6-phase scripted attacker, which is **retained as the procedural baseline**. Both must work; both must be internally consistent.
- Defence side = **existing mechanisms only** (SDR family + Tay's AI selection). No new defender mechanisms; no training novel RL agents from scratch.
- Evaluation metrics that matter: **MTTC, ASR, attack-path exposure, RoA.** Prioritise faithfulness fixes that feed these.
- **Primary metric is internal MTTC** — computed on the inherited substrate (`internal` preset). Valid for *within-substrate* comparison only (OGASP vs procedural; across MTD families / intervals / motivation profiles). An optional `lineage` preset re-creates Zhang/Tay-faithful values where cheap (it is lineage-leaning, **not** fully faithful — see the doc). Cross-paper numeric comparison to Zhang/Tay is **INVALID**. Authority: `docs/METRICS_SEMANTICS.md`.
- **Hard precondition** for end-to-end evaluation: resolve the **~6,000s crash** (regression vs Tay's 15,000s runs). Streams B and C block on it.

## Codebase lineage (so cross-paper overlap reads as evolution, not contradiction)
Brown 2023 (foundational MTDSim) → Zhang 2023 (MTDSimTime: time domain, MTTC, MTD execution schemes, adversary profiles) → Ho 2024 (metrics suite + RL) → Tay 2024 (MTDShield: reactive RL plugin). Brown is the reference implementation; the rest are systematic updates to it.

## Always-on guardrails
- **Git:** work on a dedicated branch; never commit to `main`; commit locally for my review; **never push** without asking; never run destructive git (`reset --hard`, `clean -fd`, force-push).
- **Scope:** stay inside the task's defined scope. *Flag* out-of-scope findings — don't action them. Prefer small, reviewable, line-level diffs over wholesale rewrites; ask before expanding scope or restructuring.
- **`feat/replay-viz`:** do not merge it wholesale. Pull only substrate-relevant fixes, as individually reviewed cherry-picks, per `docs/findings/replay_viz_inventory.md`. Visualisation and GAP/GASP commits are deferred (Stream A/B).

## Working standards
- **Papers are claims to reconcile with the code, not ground truth about it.** When a paper and the code disagree, record both; correct neither without a disposition from me.
- Distinguish an **inherited divergence** (the code's reality — e.g. an `internal`-preset value) from a **bug** (unintended; violates an invariant, e.g. a ratio > 1). Fix bugs; parameterise or document inherited divergences.
- **Never guess** a disposition or a locator. If you can't verify it, mark `unverified` / `verify` and state why.
- Don't assert that a paper is wrong (or that one paper contradicts another) — flag it "to verify" for me to resolve.
- When working across multiple papers, extract **one paper per pass** before merging, to prevent cross-attribution.
- Keep **inherited artefacts** distinct from **my own editorial/design choices**; track them separately.

## Repo conventions
- `docs/sources/` — external source papers + my lit review (verification targets). **Gitignored** (copyright); read from here, never commit them.
- `docs/direction/` — **my own** direction/intent docs (`current_state.md`, `methodology_carryforward.md`); tracked. These state what the code is built *toward* — they are NOT specs and NOT verification sources, so never disposition code against them. Build-relevant items: Attack Flow `.afb` schema version (carryforward §3); SNAKES env decision (§5). `current_state.md` is a 29 Apr snapshot — historical build context, superseded in specifics by the lit review.
- `docs/spec/MTDSIM_SPEC.md` — the conformance spec; verify-and-extend, dispositioned against the baseline. `docs/spec/_notes_*.md` — per-paper extraction notes.
- `docs/findings/` — Phase 2 recon outputs (crash, replay-viz inventory, Attack Flow schema, Tay RL feasibility).
- `docs/METRICS_SEMANTICS.md` — definition of internal MTTC, enumerated lineage divergences, comparability boundary.
- `baseline/BASELINE.md` + `baseline/golden/` — running baseline and seeded golden outputs (the behavioural oracle). `baseline/golden_lineage/` — reference goldens under the `lineage` preset. `baseline/CHANGELOG.md` — every intentional re-baseline (what changed, why, which spec item).
- Australian English throughout.

## Environment
- Conda env `mtdsimtime` from `environment.yml` (`conda activate mtdsimtime`); originally Python 3.9.13. Fallback: venv + `python setup.py install` + `requirements.txt`. **Record any deviation needed to build — it's a finding, not a silent fix.**
- The Tay RL / benchmark path (`mtdnetwork/mtdai/`, `operation/mtd_ai_*.py`) needs **TensorFlow**, absent from `environment.yml`. Treat the TF env delta as benchmark-only; do not commit it to `environment.yml` without my say-so.