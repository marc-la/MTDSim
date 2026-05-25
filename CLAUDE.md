## Project
- Repo: a fork of **MTDSimTime** (`main`), a discrete-event simulator for evaluating MTD.
- Owner: Marc Labouchardiere — UWA honours (CSSE), supervised by Dr Jin Hong.
- Thesis (current — **supersedes the proposal**): evaluate *existing* MTD mechanisms against
  behaviourally-grounded adversarial profiles derived from CTI. **Single RQ. No sub-problems.**
- IDS is **not** a research thread (culled; folded into lit-review §1.3 only). Do **not** build
  IDS/detection features. Tay's RL agent and its detection-sensitivity machinery are retained
  only as an inherited **benchmark defence mechanism to replicate** — never to extend.

## Direction & scope (governs all prioritisation)
- The simulator is the **L3/L4 execution substrate** for:
  L0 raw CTI → L1 GAP (attack graph; nodes = ATT&CK techniques) → L2 GASP (motivation subgraph)
  → L3 OGASP (attacker-agent traversal in MTDSim) → L4 evaluation.
- Load-bearing seam = the **attacker module**: graph-driven (GASP) traversal is added *alongside*
  the inherited 6-phase scripted attacker, which is **retained as the procedural baseline**. Both
  must work and both must be faithful.
- Defence side = **existing mechanisms only** (SDR family + Tay's AI selection). No new defender
  mechanisms; no training novel RL agents from scratch.
- Evaluation metrics that matter: **MTTC, ASR, attack-path exposure, RoA.** Prioritise faithfulness
  fixes that feed these.
- **Hard precondition** for end-to-end evaluation: resolve the **~6,000s crash** (regression vs
  Tay's 15,000s runs).