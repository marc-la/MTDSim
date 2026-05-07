# Current State — Thesis Direction

**Author:** Marc Labouchardiere (23857377)
**Supervisor:** Dr Jin B. Hong (UWA, CSSE)
**Last revised:** 29 April 2026
**Supersedes:** Project Proposal (13 March 2026) — for framing and scope purposes only. Proposal remains the assessed historical record.

> **Revision note (29 April 2026):** Lit review structure collapsed from four sections + two RQs (16 April plan) to three substantive sections + one synthesis section + one RQ. IDS folded into §1.3 of the lit review as an example of observation-driven adaptive MTD, rather than carrying its own section. See `lit_review_plan_v2.md` for the revised structure.

---

## One-paragraph framing

This thesis evaluates Moving Target Defence (MTD) mechanisms against behaviourally-grounded attacker profiles derived from cyber threat intelligence (CTI). The MTD evaluation literature — including the immediate predecessors at UWA (Tay, 2024; Ho, 2024; both building on Brown's MTDSim) — typically uses procedural or parametric attacker models (e.g. fixed `attacker_success` rates, scripted phase progression). These models sit at the bottom of the Pyramid of Pain (hashes, IPs, artefacts), even though MTD's claimed defensive value extends upward toward disrupting attacker tactics, techniques, and procedures (TTPs). By constructing attacker profiles from MITRE ATT&CK Campaigns and the MITRE Attack Flow corpus — aggregated into a Generalised APT Profile (GAP), subgraphed by adversary motivation, and operationalised inside MTDSim — this work asks whether existing MTD mechanisms hold up when evaluated against attackers modelled at behavioural rather than procedural fidelity.

---

## Research question

> **Status:** Single-RQ structure proposed 29 April 2026. Replaces the 16 April two-RQ plan and the 28 April umbrella+sub-RQ proposal. **Pending Jin sign-off** before lit-review drafting.

**RQ:** *How do existing MTD mechanisms perform against behaviourally-grounded adversarial profiles derived from CTI?*

The single-RQ structure follows from the lit-review rework: one consistent gap (behavioural attacker fidelity is absent from MTD evaluation, including from adaptive variants) supports one comparative research question. Sub-questions, if Jin wants more granularity, should be empirical splits of the umbrella (e.g. "does the answer differ across MTD families?", "across attacker motivation profiles?"), not methodology questions.

---

## Contribution claim

Prior literature independently provides (a) CTI-grounded attack profiling, (b) attack-graph operationalisation in simulation, and (c) MTD evaluation methodologies. This work sits at the intersection: a behaviourally-grounded evaluation of *multiple* MTD mechanisms (SDR family + AI-driven selection) against CTI-derived APT profiles, conducted in a network-configuration-agnostic simulator. This combination directly addresses two limitations of the dominant MTD evaluation pattern Jin has characterised — single-mechanism, single-network optimisation against procedurally-scripted attackers — by varying both the defence pool and the attacker behavioural model while holding the network substrate generic.

---

## Conceptual hierarchy

| Level | Artifact | Origin |
|---|---|---|
| L0 | Raw CTI | MITRE ATT&CK Campaigns; MITRE Attack Flow corpus; ATT&CK group descriptions |
| L1 | **GAP** (Generalised APT Profile) | Aggregated attack graph. Nodes = ATT&CK techniques. Edges = dependencies from Attack Flow corpus |
| L2 | **GASP** (Motivation-subgraphed Profile) | Subgraph of GAP. Current proxy = ancestors of motivation-attributed terminal nodes |
| L3 | **OGASP** (Operationalised GASP) | Attacker-agent traversal of GASP within MTDSim. Current bridge = technique → tactic → 6-phase attacker module |
| L4 | Evaluation | OGASP × MTD mechanism × MTDSim → effectiveness metrics (MTTC, ASR, attack-path exposure, RoA) |

> The hierarchy belongs to the **methodology chapter** of the dissertation, not the lit review. The lit review identifies the gap; the methodology argues the design choices that close it.

---

## Work streams

**Stream A — CTI → validated attack profile (L0 → L2).** GAP construction (v0.4 complete); subgraphing strategies; motivation attribution (no clean MITRE field — terminal-node proxy in current use, NLP/group-mediated inference parked); Petri-net formalisation via SNAKES (Jin, 24 April) to enable analytical reliability/dependability evaluation alongside discrete-event simulation.

**Stream B — Profile → operationalised behaviour (L2 → L3).** Tactic-level wiring of GASP into MTDSim attacker. Replaces 6-phase scripted progression with graph-driven traversal. *Precondition: ~6,000s simulator crash resolved.*

**Stream C — Integration & evaluation (L3 → L4).** Plug OGASP into existing MTD mechanisms (SDR family); replicate Tay's RL agent for benchmarking; produce comparative effectiveness measures across attacker profiles, MTD mechanisms, and MTD intervals.

Streams A and B run in parallel through May. C depends on both stabilising.

---

## Pivots from proposal

- **IDS as primary RQ2** → broadened to "MTD against behavioural attackers" generally (Jin, 16 April); IDS now folded into lit-review §1.3 as one example of observation-driven adaptive MTD orchestration, not a standalone section (29 April rework).
- **RL-based adversarial agents** → Petri-net behavioural model for formal tractability and analytical evaluation (Jin, 24 April).
- **MITRE Caldera adversary emulation** → binned; emulation overhead misaligned with simulation-based scope.
- **Defender-mechanism innovation** → de-scoped per Jin (19 March: "large can of worms"; not the focus per proposal).
- **Per-tactic linear amplification of base attacker** (early April PoC) → graph-driven traversal of GASP.
- **Two-RQ → umbrella+sub-RQ → single-RQ** structure (lit review) — collapsed because all proposed sub-questions were either methodology questions (better placed in chapter 3) or empirical splits of the same comparative claim.

---

## Scope

**In scope.** Attacker-side modelling; GAP construction and subgraphing; motivation attribution (with current best-effort proxy); Petri-net formalisation; MTDSim integration of behavioural attacker; comparative MTD effectiveness evaluation against OGASP profiles vs procedural baselines.

**Out of scope.** Defender-mechanism innovation; network-topology design (only varied if RQ requires); training novel RL MTD agents from scratch (Tay's existing model is replicated for benchmarking); real-world deployment; MITRE Caldera adversary emulation; IDS as a standalone research thread.

**Parked / stretch.** Per-host attack/defence timeline-overlay visualisation; weighted GAP edges; per-technique parameter weights (stealth, privilege, etc.) yielding adversary archetypes (espionage / disruption / financial); RL-based attacker; NLP-based motivation attribution.

---

## Implementation status (29 April 2026)

- **GAP v0.4** built and visualised (`gap.html`); 216 techniques, 142 with edges, 383 edges (18 consensus, 112 backward; min_support=0.1, min_confidence=0.6).
- **GASP selection** working via terminal-node proxy + ancestor expansion.
- **Operationalisation visualiser** half-built. Known issues: double-network render bug; replay integration incomplete. **Deprioritised through lit-review deadline (22 May).**
- **MTDSim simulator crash at ~6,000s** unresolved (resource allocation / scheduling). Blocks meaningful end-to-end runs; Tay's baseline ran to 15,000s, so this is a regression in recent changes.
- **Petri-net formalisation** (SNAKES) — design phase only; not implemented.
- **Tay's RL agent** — pulled into repo, integration not trusted; not yet benchmarked.

---

## Open decisions to lock with Jin

1. **Sign off on collapsed lit-review structure** (single RQ, three substantive sections, IDS folded into §1.3). Diagram + RQ in `lit_review_plan_v2.md` is the artifact for this conversation.
2. **Lock RQ wording.** Current phrasing leans descriptive — Jin may want a more comparative form (e.g. "How does the effectiveness of existing MTD mechanisms *differ* when evaluated against behaviourally-grounded vs procedural attacker profiles?").
3. **Confirm whether sub-questions are wanted.** Default position: no sub-questions; if Jin asks for them, frame as empirical splits not methodology choices.
4. **Lock contribution claim wording** for use in lit review §4 (synthesis).
5. **Confirm Stream A vs B priority ordering** for May–July work, given B depends on simulator crash resolution.
