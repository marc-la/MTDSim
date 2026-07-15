---
status: durable
created: 2026-07-03
topic: "L3 execution model — supervisor decision register (D1–D10, R1–R5, M1–M8)"
updated: 2026-07-15
lineage: formerly docs/notes @ 2026-07-03_supervisor_meeting_l3_decisions.md (relocated in the 2026-07-13 docs refactor)
---

# The July-2026 supervisor working sessions — the decision register that fixed the L3 execution model

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
  → **Superseded by M1 (2026-07-14):** pre-generated timelines cannot capture
  substrate feedback (an MTD mutation that severs the attacker's position must
  move the net's state); the net now runs *live* inside the simulation with an
  outcome feedback loop. The standalone timeline library survives as the
  D1 analytical track, not as the MTDSim input.
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

## The 2026-07-14 meeting rulings (M1–M8)

Minuted decisions from the 14-Jul-2026 meeting with Dr Hong (minutes held by
Marc outside the repo, per convention). Numbered **M** to keep the provenance
trail distinct from the 03-Jul minuted decisions (D) and the 10-Jul written
feedback (R). This meeting settled the execution model's remaining structural
questions; **M1 supersedes D2** and **M4 closes the CTI-grounding question**.

- **M1 — Coupling reversed: the net runs live, not replayed.** Pre-generating
  attack timelines and feeding them into MTDSim is a dead end (raised by Marc,
  confirmed by Jin): a fixed timeline cannot capture substrate feedback — e.g.
  an MTD mutation that severs the attacker's foothold must throw the attacker's
  *state* back, and a pre-generated sequence marches on regardless. The Petri
  net becomes a **live object inside the simulation** with an outcome feedback
  loop from the substrate as time passes. This supersedes D2 and promotes the
  two-way coupling from the D10 deferred register — in the *minimal* form of
  M2's conditional weights, not a full capability contract. The timeline
  library is retained for the standalone analytical track (D1) only.
- **M2 — Success model: binary outcome selects between conditional weight
  sets.** When the token sits at a tactic, the attacker calls the substrate's
  **existing** attack machinery on its current position (the
  vulnerability/CVSS-priced exploit path) and gets a **binary success/failure
  outcome** back. That outcome overrides the transition weights at the current
  place: success → one predefined weight set (forward transitions live),
  failure → another (forward zeroed; retry/backward transitions live). Start
  binary; richer outcome classes only if something needs recapturing later.
  The flow-proportion priors (D3) stand as the base weights — the outcome
  *conditions* them, it does not replace the weighting regime. "Worst case, a
  successful and an unsuccessful version of the net" was considered and
  rejected as too complicated — conditional weights are the mechanism.
- **M3 — Direction from the kill chain.** ATT&CK deliberately encodes no
  tactic ordering, so the forward/backward reading M2 needs comes from mapping
  the tactics onto **kill-chain phases**: link the appropriate tactics to make
  the success/failure decision directional (success = eligible to progress,
  failure = fall back / retry). An assumption of this work, recorded as such.
- **M4 — The ontology join is resolved shallow: substrate as outcome oracle.**
  The tactics/techniques layer and the substrate's vulnerability ecosystem are
  **separate concepts and stay separate**: "the vulnerability details are just
  an enabler for you to progress" (Jin). The net supplies *movement/behaviour*
  (which tactic, which direction); the substrate's existing vulnerability-based
  attack simulation supplies *outcomes* ("if you need the success outcome, you
  fetch it from the bottom"). No technique→CAPEC→CWE→CVE→CVSS grounding of the
  vulnerability pool is required — this closes the CTI-grounding program's
  depth question at the shallow end and retires the crosswalk-join
  investigation.
- **M5 — Manual tactic→action influence map.** Enumerate the substrate's
  existing attacker actions, then map **which tactics each action influences**
  — manual, but justified per pair ("exploitation happens in these tactic
  steps"), with a binary in/out decision for each pairing. The existing action
  set is the starting vocabulary; richer behaviours (e.g. an evade or
  persistence action) are enrichment *after* the loop closes, not before.
- **M6 — Recon/resource-development: join synthetically at the front.** The
  corpus is blind to pre-intrusion tactics, but recon logically enables
  initial access ("if you cannot recon anything, you can't gain initial
  access"). Rather than a start-at-initial-access workaround or an
  attacker-knowledge parameter, **connect the detached pre-intrusion tactics
  into the net manually** — a synthetic, logically-correct curation, defensible
  because nothing detects pre-intrusion activity anyway. Supersedes the D8
  entry-point experiment as the operative stance (both entries remain testable).
- **M7 — Architecture: a movement layer on top, existing model untouched.**
  Implement as **a new layer/attacker class for movement** that plugs into the
  existing simulator's action machinery as an interface ("this is your API —
  you get the result out, and it feeds the movement of the attacker"). The
  basic 6-phase attacker is retained unchanged as the baseline; deep edits to
  the well-integrated existing model are explicitly avoided.
- **M8 — Evaluation expectations and the metrics gap.** Shared expectation:
  the profiled/APT attacker will do **no better** than the basic attacker on
  pure security metrics (the basic attacker is geared to this substrate; the
  APT profile spends effort on evasion-shaped behaviour the current metrics
  don't reward). Consequences: (a) run it and see — tuning comes after
  numbers; (b) post-implementation, identify **supplementary measurements**
  (evasion/stealth-shaped) that show where APT behaviour matters — measuring
  stealth is acknowledged tricky; (c) the headline claim stays *MTD is
  effective against APT-style behaviour* (proactive defence changes the attack
  surface regardless); (d) an attacker that *studies the MTD* to overcome it
  is future work / a discussion point — the capability hooks exist, the
  behaviour is not built.

**Standing items ratified in passing:** the flow-proportion weighting regime
(D3) stands — "weighting is difficult in modelling; come up with reasonable
ways to justify it", no additional weighting scheme wanted. Implementation is
the last major piece: once the coupled attacker runs, the remaining work is
pulling numbers and writing the dissertation (October due; on schedule).
Semester 2 starts 20-Jul; meetings ad hoc once Jin's timetable settles, Marc
sends regular updates.

## Still open with the supervisor

- **Nothing structural.** M1–M8 closed the execution-model questions (coupling,
  success semantics, direction, ontology join, pre-intrusion tactics,
  architecture). The cost-only disposition (R5) and the CVE-binding question
  are both moot under M4/M5 — the substrate-as-oracle join never touches them.
- **Post-implementation, by evidence:** the supplementary evasion/stealth
  measurements (M8b) and any weight/success-rate tuning — both explicitly
  sequenced after first numbers, and reviewed against what the numbers show.

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
  - [`../handoffs/2026-07-15_l3_tactic_action_influence_map.md`](../../../handoffs/2026-07-15_l3_tactic_action_influence_map.md)
    — executes **M5** (action inventory + tactic→action influence map) and
    **M6** (pre-intrusion synthetic join), and inventories the **M2/M4**
    outcome-oracle signals.
  - [`../handoffs/2026-07-15_l3_feedback_net_design.md`](../../../handoffs/2026-07-15_l3_feedback_net_design.md)
    — designs the **M1/M2/M3** contract: live net stepping, conditional
    weight sets, kill-chain direction layer.
  - [`../handoffs/2026-07-15_l3_profiled_attacker_build.md`](../../../handoffs/2026-07-15_l3_profiled_attacker_build.md)
    — builds the **M7** movement layer (the profiled attacker class) against
    the two records above; executes **D1/D5** end-to-end.
  - [`../handoffs/2026-07-15_l3_first_numbers.md`](../../../handoffs/2026-07-15_l3_first_numbers.md)
    — the first experiment matrix + the **M8** metrics-gap review.
  - Retired by the 14-Jul meeting (deleted per the handoff lifecycle; git log
    is the record): the deferred replay-attacker build (its one-way replay
    premise died with D2→M1), the MVP-binding investigation + goal (work
    landed as [`binding_design_space.md`](binding_design_space.md); framing
    superseded), the crosswalk-join investigation (mooted by **M4** — the
    join is substrate-as-oracle, no CVE grounding), and the
    tactic-operationalisation conceptualisation (its open questions — success
    model, binding, Caldera-inspired capabilities — were answered by
    **M2/M5/M7**; its surviving passes fold into the four handoffs above).
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
- ~~If the two-way integration is picked up: D2 stops describing the live
  coupling model~~ — happened (M1, 2026-07-14); D2 is annotated in place and
  this note records both regimes.
- If the M2 binary outcome proves too coarse (something needs recapturing),
  the richer-outcome extension Jin sanctioned gets its own ruling.
- If corpus expansion lands: D3's "only quantitative evidence available"
  sparsity acceptance needs re-examination against the larger corpus.
