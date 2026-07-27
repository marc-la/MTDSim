---
status: durable
created: 2026-07-03
topic: "L3 execution model — supervisor decision register (D1–D10, R1–R5, M1–M8, S1–S6)"
updated: 2026-07-27
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
  → **Three deferrals have since been lifted:** two-way integration by **M1**
  (2026-07-14, and built); **sensitivity analysis on the weights** by **S1**
  and **timed-net firing semantics** by **S3** (both 2026-07-21). What remains
  deferred: evasion/detection-rate modelling, aggregated cross-profile
  variation analysis, the closed-form CTMC solve.

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

## The post-experiment-1 rulings (S1–S6)

Provenance: Marc's written supervisor update dated **21 July 2026** and the
meeting it drove (late July 2026); both held by Marc outside the repo, per
convention. Numbered **S** to keep this trail distinct from the 03-Jul minuted
decisions (D), the 10-Jul written feedback (R) and the 14-Jul meeting (M).
Recorded 2026-07-27.

**What these rulings are responding to.** The end-to-end loop ran, and
experiment 1 produced a stark result: the profiled attacker reached the
substrate objective **0 out of 100 runs** against a baseline ASR of 0.90–1.00,
failing in two distinct ways (*friction* — blocked on substrate preconditions;
*churn* — busy successes that never spread), with MTD leaving the verdict
unchanged on both arms. The full record is
[`experiment_01_findings.md`](experiment_01_findings.md). The meeting read this
as **an expected consequence of two things that are ours to fix** — the
inherited phases' tight integration and the deliberately coarse tactic→verb
collapse — not as a failure of the movement layer, and the rulings below
allocate the response.

**Layer vocabulary ratified.** The update presented, and the meeting used, the
three-layer runtime naming: **movement layer** = everything from the CTI
(Attack Flow) through to the attack profiles (the Petri nets); **controller
layer** = the mapping/join between the movement layer and MTDSim (or any MTD
simulator); **action layer** = the predefined attack behaviour inherited from
MTDSim. This is now the operative vocabulary — encoded in
[`../../architecture.md`](../../architecture.md) §(f) as the runtime view
alongside the L0–L4 build-time view, and it discharges the vocabulary half of
the parked layer-reframe handoff.

- **S1 — Tactic-pair weights need literature-grounded dependency and a
  sensitivity study.** The current tactic-tactic values are "not realistic",
  the named defect being **large jumps in tactics** — a pair like
  `reconnaissance → impact` still carries appreciable mass. The direction:
  assert a **literature-based dependency** on the weights so that *close* jumps
  weight higher and *far* jumps (recon → impact being the canonical example)
  weight close to, or exactly, zero. The grounding is to be built by
  **overlaying APT lifecycle models and taking their consensus** before that
  consensus is folded into the weights: the **Cyber Kill Chain** is the primary
  overlay (its seven phases are sequential and ATT&CK maps onto them),
  **Alshamrani 2019**'s five-phase APT lifecycle is a second, and other
  published APT lifecycles are candidates for the same treatment. Two scope
  statements ride with this: the present weights are an explicit **initial
  trial of static weights**, and **dynamic weights conditioned on attacker
  state** are the eventual direction, deferred. Standing constraint: the
  weights are not to be reverse-engineered to make any particular net traverse
  well (the CTI-independence boundary in
  [`success_failure_overlay_design.md`](success_failure_overlay_design.md) §1).
- **S2 — The attacker action set is frozen, short term.** No adding, removing,
  or altering attacker actions, abilities, or attacker states; **"do not change
  the MTDSim code yet"**. What remains licensed is **refinement of existing code
  and bug fixes**. This freezes, for now, the open questions the update raised
  about new capabilities (an evasion action, a tooling/endowment state, a
  privilege level, a durability parameter) — they are the *note* at the end of
  the update, not current work.
- **S3 — Timing moves onto the Petri nets, exponentially distributed.** Timing
  may be taken from either layer and currently comes from MTDSim, but the
  direction is for the **movement layer to be the timing source**: a time per
  tactic, drawn from an **exponential distribution**, with **non-action tactics
  consuming time in the simulation and doing nothing else**. The substrate's
  MTD **confusion penalty** is to be replicable the same way — a place in the
  net carrying the same base duration under the same stochastic regime. The
  supervisor's caveat is the operative constraint: the numbers are
  **inherently arbitrary, so justifying them is the key** — which puts this
  work under the existing operational-validation discipline rather than beside
  it. Reverses the D10 deferral of timed-net (GSPN/SPN) firing semantics.
- **S4 — The tactic→action mapping need not be total.** **Not every tactic
  needs to be mapped.** A tactic maps to **[0, 1] actions**; multiple tactics
  may map to the **same** action; and where no mapping makes sense the tactic
  becomes a **non-action ("dwell-only") tactic** that consumes time in the
  simulation without dispatching a verb. This is extensible — a tactic gains an
  action when one exists for it. Because the controller layer is the
  **application layer the experiments vary**, the mappings that have been tried
  and what each produced are to be **maintained and version-controlled**, not
  overwritten in place.
- **S5 — A run that hits a sink retraces rather than dies.** For experiment 2,
  the procedural tweak is that a token reaching a sink place **retraces the edge
  it travelled** (an optional alternative raised in the meeting: route to some
  other node) instead of the run being discarded. This supersedes the
  accept-and-censor disposition recorded at
  [`runtime_verification.md`](runtime_verification.md) §P7 — that ruling stands
  as the *experiment-1* behaviour and is retained as the comparison arm.
- **S6 — The project's headline is a criterion question.** The finding this
  work reports is **what this model captures about APT attackers that prior
  models do not**. The direction is to return to the reviewed APT literature —
  **Cho 2020** (axes of what an attacker model should contain), **Jalowski
  2026** (naming the same gap this work targets), **Alshamrani 2019** (the
  enumeration of APT behaviour) — and build a **structured criterion / rubric**
  from it, against which this model is scored and benchmarked over the coming
  weeks. Two constraints on the artefact: it must be **loaded into the context
  of every future session**, and it must **not promise the world** — the model
  will not satisfy every axis, and the claim is that it captures the *missing
  essence* those three sources name, not that it closes the gap.

## Still open with the supervisor

- **Nothing structural in the execution model.** M1–M8 closed the
  execution-model questions (coupling, success semantics, direction, ontology
  join, pre-intrusion tactics, architecture); S1–S6 allocate the
  post-experiment-1 response. The cost-only disposition (R5) and the
  CVE-binding question are both moot under M4/M5 — the substrate-as-oracle
  join never touches them.
- **Scoping the attack-model change, when the freeze lifts (S2).** The update's
  own "major point of guidance" question — *how far to go in reworking the
  action set so that each tactic has a corresponding capability* — is
  deliberately unanswered while S2 holds. The two directions the update named
  (refine the existing connection vs rework the action set) are the decision
  the freeze defers, not a decision already taken.
- **Post-refinement, by evidence:** the supplementary evasion/stealth
  measurements (M8b), now folded into the S6 criterion work as the "what would
  evidence each axis" half; and the dynamic, attacker-state-conditioned weights
  named as the eventual direction in S1.

## 2026-07-23 — outcome-overlay (M2/M3) numbers finalised

The M2 success/failure overlay numbers were **scrutinised and finalised ahead of
first numbers** (Marc's call), through four adversarial cross-examination rounds
(~90 agents): initial cross-exam → branching red-team → composed-net validation →
stepwise simulation (real Petri nets, MTDSim verdict stubbed). Outcome: the **R2**
rule-set, converged (final finetune synthesis = zero changes), certified **82%**
with the 82→95% remainder being the dissertation defence of the reasoning, not value
uncertainty. Ratified: the **C2-hub** `enables` edit is **kept** (with an inclusion
principle); the **`enabled = 1.0` tier stays flat** (a graded scheme was empirically
counterproductive). The values are now **rule-based and complete** (210 pairs,
corpus-agnostic). Records: [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
§2.5, the provenance/scrutiny ledger [`../../declared_value_provenance.md`](../../declared_value_provenance.md).

**Reframed by S1 (2026-07-27) — not retracted.** R2 remains the landed value set
and the experiment-1 arm, but it is now on record as **an initial trial of static
weights**: S1 directs a literature-grounded lifecycle-distance dependency (close
jumps up, far jumps to ≈ 0) and a sensitivity study over the result. The
convergence and the 82% certification describe R2's *internal* coherence, which S1
does not dispute; what S1 adds is an **external** grounding R2 never claimed to
have.

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
  - [`action_layer_anatomy.md`](action_layer_anatomy.md)
    — the site survey under **M5/M7**: the action layer's coupling graph,
    callable surface, affordance/limitations register, and ATT&CK coverage map;
    pre-registers the coupling-performance hypothesis alongside **M8**'s
    metric-mechanism one. *(Was the anatomy handoff, shipped & deleted per the
    handoff lifecycle; see git log.)*
  - **M5 landed and was reframed** (handoff retired 2026-07-22): the tactic→action
    influence map became the **controller** — a swappable CKC-mediated tactic→verb
    dispatch input parameter ([`controller.md`](controller.md),
    [`../../data/ogasp/controller.csv`](../../../../data/ogasp/controller.csv)), not
    a justified one-true mapping; the **M2/M4** outcome-oracle verdicts are its §4.
    **M6 executed 2026-07-21** as the **synthetic overlay** — a maintained
    structural sublayer ([`synthetic_overlay.md`](synthetic_overlay.md),
    [`../../data/ogasp/petri/synthetic_overlay.json`](../../../../data/ogasp/petri/synthetic_overlay.json)):
    bidirectional pre-intrusion connective tissue (forward chain recon →
    resource-development → initial-access + backward regression bridge
    initial-access → reconnaissance).
  - [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
    — designs the **M2** contract as reframed 2026-07-21 (Marc's direction):
    the success/failure outcome overlay as a declared **policy** layer (two
    binary tactic-pair weight treatments composed multiplicatively with the
    substrate verdict at runtime), CKC demoted to the band prior of the
    authoring framework (not a runtime M3 layer). Carries the composition,
    stall, interrupt, and live-stepping semantics; artefact
    [`../../../../data/ogasp/petri/outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json).
    Its runtime composition is implemented in the controller sublayer by the
    finalise handoff below. **Awaits Marc's review.**
  - **The build chain that produced experiment 1 is shipped and its handoffs are
    deleted** (git log is the record): the controller finalisation and the **M7**
    movement-layer attacker landed at commit `48471b8`, and the first-numbers run
    landed at `c27409f`. Its result is
    [`experiment_01_findings.md`](experiment_01_findings.md); the pre-run
    cross-examination is [`runtime_verification.md`](runtime_verification.md).
  - **Forward chain (2026-07-27, executing S1–S6).** Eight handoffs in
    [`../handoffs/`](../../../handoffs/), all dated `2026-07-27`, in four waves —
    the ordering and its rationale are in each handoff's *State of play*:
    (1) `apt_model_criterion` (**S6**), `lifecycle_consensus_overlay` (**S1**,
    literature half) and `action_layer_refinement_under_freeze` (**S2**) run
    independently; (2) `controller_v2_partial_mapping` (**S4**) then
    `stochastic_timing_design` (**S3**, planning half); (3)
    `tactic_weight_sensitivity_study` (**S1**, study half) and
    `stochastic_timing_implementation` (**S3**, build half); (4)
    `sink_retrace_experiment2` (**S5**, and the experiment-2 run that consumes
    the rest).
  - Retired by the 14-Jul meeting (deleted per the handoff lifecycle; git log
    is the record): the deferred replay-attacker build (its one-way replay
    premise died with D2→M1), the MVP-binding investigation + goal (its
    `binding_design_space.md` / `binding_signoff_summary.md` records were removed
    2026-07-22 when the tactic→action map was reframed as the swappable
    controller input parameter — [`controller.md`](controller.md)), the crosswalk-join investigation (mooted by **M4** — the
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
- **When the S2 action-set freeze lifts** — the scoping question it defers (how
  far to rework the action set so each tactic has a capability) becomes a live
  ruling, and the update's capability candidates (evasion, tooling endowment,
  privilege level, durability) re-enter as design work.
- ~~If timed-net firing semantics are picked up: D10's deferral stops
  holding~~ — happened (**S3**, 2026-07-21); D10 is annotated by S3 rather than
  rewritten, and the duration regime moves from plain dwell to exponential
  firing.
- If the S1 sensitivity study shows the conclusion turns on where in its band a
  tactic-pair weight sits, the declared-weight defence in
  [`../../declared_value_provenance.md`](../../declared_value_provenance.md)
  needs re-argument, not just re-certification.
