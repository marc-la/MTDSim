---
status: durable
created: 2026-07-03
topic: "L3 execution model — supervisor decision register (D1–D10, R1–R5)"
updated: 2026-07-13
lineage: formerly docs/notes @ 2026-07-03_supervisor_meeting_l3_decisions.md (relocated in the 2026-07-13 docs refactor)
---

# The July-2026 supervisor working session — the decision register that fixed the L3 execution model

## Why this is worth recording

A working session with Dr Jin Hong (early July 2026; minutes held by Marc
outside the repo) settled how the OGASP Petri nets become executable attacker
behaviour: the v1 coupling model, the weighting regime, the duration regime,
the scope boundary, and the deferred register. Handoffs are deleted when their
work lands, and the minutes live outside the repo — this note is the durable
in-repo record that the canonical specs and every downstream session cite.
The spec blocks that encode these decisions are listed under *How it
connects*; this note is the register, the specs carry the operative wording.

## The substance — the decision register (D1–D10)

- **D1 — Both tracks.** Not formalism-only: "incorporate the petri net into
  MTDSim so the attack behaviour is dictated by this", *and* examine the
  attack behaviour the net generates on its own.
- **D2 — v1 coupling is one-way.** Run the Petri net independently of the
  simulator. A **single token** moves through the net; record the state at
  each node; each state has a duration; output = a **timed sequence of
  attacker states** (a cumulative timeline) fed into the simulator. Two-way
  interaction (simulator ↔ net each event) is the end goal, **deferred**.
- **D3 — Edge weights.** Derived as the **proportion of attack flows leaving
  each node**, computed at **tactic level** (aggregation up from techniques
  is what makes the weights groundable at this corpus size). The sparsity of
  the ~38-flow corpus is **accepted**: "it's the only quantitative evidence
  available to populate the Petri nets. Looking thin is fine." Dispositioned
  against the [`../specs/metrics_semantics.md`](../../metrics_semantics.md)
  §(f) prohibition — see that section for the operative normalisation +
  closed-world wording.
- **D4 — Durations.** Since the simulator is discrete-event, **every state
  needs a time**. Reuse timing values from relevant work where they exist;
  otherwise assign a **reasonable, justified** number (e.g. for stealth).
  No ready-made MITRE-tactic→time resource exists — define it, with
  justifications.
- **D5 — Scope of MTDSim change: attacker only**, for comparability with
  previous work. HARM / network / MTD mechanisms untouched.
- **D6 — Uncaptured behaviours** (stealth, evasion, access/response
  development): manually define reasonable connections/values as a starting
  point. Detection-rate effects and evasion come later if time allows;
  **attack behaviour is the priority**.
- **D7 — Success model.** Keep the same routes, but let the attack
  behaviour/state decide the outcome (an attacker in a stealth state won't
  launch the exploit the simulator would otherwise expect). Three layers:
  net state → simulator action → outcome. **Scoping only for now.**
- **D8 — Entry point.** Test **both**: seed at `initial-access` (the
  corpus's real entry) and the recon-back curation — "straightforward to
  test".
- **D9 — Structural sparsity at node level is fine** so long as there is a
  coherent path from start nodes to end nodes.
- **D10 — Priority & deferrals.** Working implementation **before Semester 2
  starts**; the scoped implementation is already distinction-level.
  **Deferred:** two-way integration, sensitivity analysis on net weights,
  evasion/detection-rate modelling, timed Petri nets (GSPN/SPN/TPN firing
  semantics), aggregated cross-profile variation analysis. (The closed-form
  CTMC solve of the retired 2026-06-18 implementation handoff joins this
  register — Monte-Carlo over the standalone runner is the v1 way the nets
  are examined.)

## Follow-up resolutions (Marc, 2026-07-04)

The four questions the meeting left open were resolved by Marc when this
register was encoded:

- **5th aggregate/null profile — include it.** "No harm in trying." It
  doubles as the "do the classes differ" verification: the four class nets
  are measured as divergence from the aggregate.
- **Corpus expansion — deferred.** Get the pipeline running end-to-end
  before considering other MITRE-based databases or GenAI-sequenced
  campaign cross-verification.
- **CVE↔synthetic-CVSS binding — explore, don't commit.** The binding-scoping
  handoff evaluates it as *a potential binding*, not a confirmed approach.
- **The `metrics_semantics.md` §(f) crux — confirmed.** Seeding transition
  probabilities from raw edge weights stays INVALID as-is; the D3
  flow-proportion regime (explicit normalisation + closed-world assumption,
  at tactic level) is the sanctioned escape, now dispositioned in §(f).

## The 2026-07-10 written feedback (R1–R5)

Jin's written response to Marc's 10-Jul-2026 progress update (the update and
response held by Marc outside the repo). These rulings extend the D-register;
they were given in writing, not minuted, and are numbered separately (R) to
keep the two provenance trails distinct.

- **R1 — Timing evidence regime.** Timing-related papers are not expected to
  exist ("likely"); where they don't, **assume based on practical reports**.
  The sanctioned qualitative shape: **observations are long-term, execution is
  very quick.** This ratifies the shape-not-scale / tiered-validity discipline
  already in place and *lowers the calibration bar*: no literature-fitting
  exercise is required before the pipeline MVP; number-justification against
  practical reports is sequenced after it.
- **R2 — Success-rate axis.** APT-ness is to be encoded partly through a
  per-action **attack success rate**, "tuned higher in execution actions for
  APTs" — a new profile parameter that no prior decision covers. To be
  investigated during implementation (open handoff), not designed up front.
- **R3 — Attacker styles.** "Make some predefined profiles of attackers based
  on some characteristics we define, observed from practical reports etc." —
  a characteristics-based *style* dimension (speed, success rate) distinct
  from the L2 operational-objective classes; "we can also try different
  styles to show how they work against MTD" is an intended result axis.
  Whether styles compose with or replace the objective classes is unresolved
  (meeting question). Investigated further down the line.
- **R4 — Simulation settings are free experimental variables.** "Simulation
  settings can be updated to suit the experiments." This dissolves the
  timeline-scale coupling concern (inherited runs at ~5000 s vs net timelines
  reaching their objective in ~200–500 s): the horizon and MTD intervals are
  experiment design choices, not fidelity constraints.
- **R5 — MTD coverage gaps are acceptable.** "If we don't have MTD that
  influence the tactic, that's fine and we can let it be" — tactics no MTD
  mechanism can touch are left as-is; layering MTD techniques to cover them
  is explicitly future work for someone else. This confirms the cost-only
  disposition for the tactics with no network-state to act on.

## Still open with the supervisor

- **Cost-only vs proto-IDS for stealth tactics — effectively resolved by R5.**
  [`../specs/project_context.md`](../../../workflows/project_context.md) already rules
  out building IDS, and R5 accepts tactics that MTD cannot influence;
  cost-only proceeds as the confirmed MVP disposition. Residual: formal
  ratification at the next meeting alongside the CVE-binding confirmation.

## How it connects

- To the specs — the operative encodings of this register:
  [`../specs/metrics_semantics.md`](../../metrics_semantics.md) §(f)
  (D3 disposition); [`../specs/architecture.md`](../../architecture.md)
  §(f) (D1/D2 coupling model, working-layer ledger, deferred register) and
  §(j) (envelope-not-actor framing);
  [`../specs/provenance.md`](../../provenance.md) (weighting + duration
  regime rows); [`../specs/02_gasp_schema.md`](../gasp/gasp_schema.md)
  §(a) (envelope one-liner).
- To open work — which handoff executes which decision (handoffs are deleted
  as they land; git log is the permanent record):
  - the weighted nets [`../../data/ogasp/`](../../../../data/ogasp) (shipped; see its README)
    — executed **D3, D9** + the aggregate-profile resolution.
  - the state-duration catalogue [`../../data/ogasp/tactic_durations.json`](../../../../data/ogasp/tactic_durations.json) (shipped 2026-07-09)
    — executes **D4** (under the D10 timed-net deferral: plain per-state
    dwell, not stochastic firing rates).
  - `handoffs/2026-07-03_l3_timeline_runner.md` (shipped & deleted per handoff lifecycle; see git log)
    — executes **D2** and D1's standalone-examination half, plus **D8**
    (both entries).
  - [`../handoffs/2026-07-13_l3_mvp_binding_investigation.md`](../../../handoffs/2026-07-13_l3_mvp_binding_investigation.md)
    — executes **D5, D6, D7** (scoping only) + the CVE-binding exploration,
    under the R1/R4/R5 rulings. Supersedes the 2026-07-03 binding-scoping
    handoff, whose recommended stance pre-committed to a verb-wrapping
    binding; the investigation re-opens the design space impartially.
  - [`../handoffs/2026-07-13_l3_tactic_operationalisation.md`](../../../handoffs/2026-07-13_l3_tactic_operationalisation.md)
    — conceptualises the tactic-as-action implementation and carries **R2**
    (success-rate axis) and **R3** (styles); sequenced after the binding
    investigation is signed off.
  - [`../handoffs/2026-07-03_l3_replay_attacker.md`](../../../handoffs/2026-07-03_l3_replay_attacker.md)
    — executes **D1/D2/D5** end-to-end; the capstone. **Deferred** until the
    binding investigation and tactic-operationalisation scaffolds are signed
    off (Marc, 2026-07-13).
  - The governance handoff that encoded this register
    (`2026-07-03_l3_governance_meeting_decisions.md`) was deleted in the
    commit that landed this note, per the handoff lifecycle.
- To the rationale: the envelope framing is
  [`./2026-06-18_cti_to_executable_behaviour.md`](../../../notes/ch3_design/structure_to_behaviour_binding.md)
  §1; the MVP cut the meeting largely ratified is §11 of the same note.

## When this would need updating

- If Jin answers the cost-only/proto-IDS question differently, or reverses
  any follow-up resolution (e.g. the aggregate profile turns out
  uninformative and is cut).
- If the two-way integration is picked up: D2 stops describing the live
  coupling model and this note becomes the record of the v1 baseline.
- If corpus expansion lands: D3's "only quantitative evidence available"
  sparsity acceptance needs re-examination against the larger corpus.
