---
status: open
created: 2026-07-13
---

# Conceptualise the tactic-as-action implementation — each tactic an executable capability with a success/failure model, the prior attacker's good parts kept deliberately, Caldera-inspired but minimal, graded by insight yield rather than attacker strength

> **Sequenced after the binding investigation
> ([`./2026-07-13_l3_mvp_binding_investigation.md`](./2026-07-13_l3_mvp_binding_investigation.md))
> is produced and supervisor-signed-off** — this brief consumes its
> recommended binding and per-tactic ledger scaffold. It carries the two
> axes that investigation explicitly preserves as extension points: the
> **R2 per-action success-rate parameter** (investigated during
> implementation, per Marc 2026-07-13) and the **R3 attacker-style
> dimension** (investigated further down the line — scoped here, designed
> later). Register:
> [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md).
>
> **The grounding rule (anti-fairyland), from Marc — apply it to every
> design choice in this brief:** the goal is *insight from results*, not
> attacker strength. One can always build "a really strong attack model" by
> pushing success rates toward 1.0 and calling it an APT attacker — that is
> the named failure mode, not the project. A design choice earns its place
> only if it makes the simulator's outcomes **behaviourally richer in a way
> results and meaning can be pulled from** — class profiles that separate
> under MTD, mechanism rankings that move with attacker behaviour, exposure
> patterns a defender could act on. Strength without insight is failure;
> when in doubt, choose the design that produces the more interpretable
> difference, not the more fearsome attacker.

## State of play

- **The working experiment shape** is `objective class × style × MTD
  mechanism` (from the 2026-07-10 feedback): the L2 classes supply routing
  and termination; styles (R3) supply behavioural character (speed,
  reliability); MTD mechanisms are the existing set, unmodified. Whether
  styles *compose with* or *replace* the objective classes is a standing
  meeting question — this brief must stay valid under either answer.
  Whether profiles carry **differing action sets** (not just differing
  parameters) is an open design question this brief owns.
- **R2 gives the success-rate directive but not a model.** "Tune the attack
  success rate higher in execution actions for APTs" implies per-action (or
  per-tactic) success probabilities varied by style. Undesigned: what a
  "success" event is per tactic (this depends on the signed-off binding's
  realisation conditions), where the probability acts (action outcome vs
  net transition choice vs both), how failure feeds back (retry, backward
  transition, dwell extension), and how it composes with the substrate's
  *existing* implicit success machinery — complexity-priced exploits,
  brute-force chance, the attempt-limit give-up rule. Double-counting
  chance is a real trap: adding a success layer on top of mechanisms that
  already roll dice must be reasoned out, not layered blindly.
- **The prior attacker has parts worth keeping — identify them
  deliberately, not by inertia.** The inherited 6-phase attacker is being
  replaced as *sequencing logic* (that is the binding investigation's
  anti-goal), but its execution machinery embodies years of working
  decisions: the SimPy interrupt + penalty pattern for MTD disruption, the
  per-host attempt-limit give-up rule, exploit-time pricing off complexity,
  the compromise bookkeeping the statistics pipeline reads. "Keeping the
  good aspects" means an explicit keep/replace/wrap verdict per mechanism,
  with the reason recorded — the same discipline the conformance spec
  applies to inherited divergences.
- **Precedent is thin, and that is the opportunity.** Nobody has really
  operationalised MITRE tactics as executable simulator behaviour except
  MITRE Caldera (real adversary emulation: abilities → adversary profiles →
  operations, with facts/requirements as pre/post-conditions). Caldera is
  far too heavy to plug into a DES — but its *abstractions* may transfer
  (an "ability" as a pre-condition/behaviour/post-condition triple is
  strikingly close to the deferred capability contract). Caldera-inspired
  minimal components is one candidate; a ground-up fresh implementation of
  each tactic purpose-built for attack *modelling* (not emulation) is
  another; there are more. Caldera is **unextracted** — papers-are-claims
  applies; extract before citing design details.
- **What exists to build on:** the 15 per-tactic profiles
  ([`../notes/ch3_design/tactic_profiles/`](../notes/ch3_design/tactic_profiles/),
  §5 blocks = single source of truth for dwell/behaviour evidence), the
  timeline library and schema, the binding investigation's ledger (once
  signed off), and the duration catalogue (v0, calibration re-sequenced
  post-MVP per R1).

## Recommended approach

**Deliverable = a conceptual scaffold for supervisor sign-off before any
implementation** — an implementation-shaped design record
(`docs/implementation/pipeline/ogasp/tactic_operationalisation.md`), built
in four passes:

**1 — Inherited-machinery audit (keep the good parts, on purpose).** Walk
[`attack_operation.py`](../../mtdnetwork/operation/attack_operation.py) /
[`adversary.py`](../../mtdnetwork/component/adversary.py) mechanism by
mechanism (interrupt handling, penalties, attempt limits, exploit pricing,
compromise bookkeeping, event records) and give each a keep / wrap / replace
verdict with rationale. This is the "what did the prior model do well"
question made concrete — and it hard-bounds the greenfield surface.

**2 — Per-tactic capability sketches.** For each of the 15 tactic-places:
what the tactic *attempts* (from its profile's §5 block), what capability
realises the attempt under the signed-off binding, what success and failure
each mean there, and what the capability records for the statistics
pipeline. Where the binding says cost-only (R5-confirmed), the sketch says
what the dwell *represents* and what would upgrade it later. Design the
sketches against the precedent survey (pass 3) rather than in a vacuum —
but the profiles' evidence, not the precedent's machinery, is the
authority on behaviour.

**3 — Precedent survey, Caldera first.** Extract Caldera's operational
model (ability / adversary-profile / operation / fact abstractions) into
`docs/sources/extractions/` per the paper-acquisition split; survey the
smaller adjacent precedents (adversary-emulation planners, MAL-family
attack simulations, anything operationalising ATT&CK) for transferable
abstractions. Verdict per abstraction: adopt-minimal / adapt / reject, with
the DES-overhead argument recorded — "Caldera-inspired, only the necessary
components" is the stance to argue for or against, not assume.

**4 — The success/failure model (R2), options argued.** Design 2–3 candidate
models — e.g. (a) per-action Bernoulli success layered on binding outcomes,
style-parameterised; (b) success expressed through the *net* (forward
transition = success, backward = failure, probabilities style-weighted),
keeping substrate outcomes deterministic; (c) hybrid: substrate mechanisms
keep their native dice, the R2 layer only modulates them per style. For
each: where randomness already lives in the substrate (no double-counting),
determinism/seeding (SIM-05), what the parameter *means* (so a style's
"higher execution success" is a defensible sentence, not a magic number),
and — the grounding rule — what *insight* the knob enables (e.g. does an
MTD mechanism's ranking depend on attacker reliability?). Recommend one.
Then scope, without designing, the **R3 style layer**: which parameters a
style bundles (dwell shape per R1 — observation long, execution quick;
success-rate profile; possibly recon endowment / relative-strength for the
pre-intrusion tactics), how many styles are enough for a claim (two
contrasting styles beat five arbitrary ones), and note the open
compose-vs-replace question for Jin. Style *design* is explicitly further
down the line.

*Alternatives considered:* folding this into the binding investigation —
rejected: that brief must stay impartial about the binding itself, and
loading it with implementation conceptualisation would double its scope and
tempt it toward the design that eases pass 2 here. Designing the style
vectors now — rejected: R3 is "further down the line" (Marc, 2026-07-13),
and style definitions should follow, not precede, the success-model choice.
Implementing incrementally without a signed-off scaffold — rejected: the
sign-off *is* the point; this project's supervision loop works
scaffold-first.

## Validation gate

Done when:
1. The inherited-machinery audit exists with a keep / wrap / replace verdict
   and rationale per mechanism.
2. All 15 per-tactic capability sketches exist, each consistent with its
   profile's §5 block (single-source-of-truth constraint) and with the
   signed-off binding ledger; every cost-only row says what its dwell
   represents.
3. The Caldera extraction exists in `docs/sources/extractions/` and every
   borrowed abstraction has an adopt-minimal / adapt / reject verdict with
   the overhead argument.
4. The success/failure model recommendation exists, with the double-counting
   analysis against the substrate's native chance mechanisms, a
   determinism/seeding statement (SIM-05), and — per candidate — the named
   insight it enables. The style layer is scoped (parameter bundle, open
   questions) but not designed.
5. **Every major choice in the record carries its grounding-rule sentence:**
   the behavioural difference in outcomes it produces and the
   result/meaning that difference would let the evaluation chapter claim.
   Any choice justified only by "more realistic" or "stronger attacker"
   fails the gate.
6. Marc has reviewed the scaffold and it is packaged for Jin's sign-off.
7. **No code changes anywhere** — conceptualisation only.

## Hard constraints

- **Blocked on the binding sign-off** — do not start pass 2 before the
  binding investigation's recommendation is confirmed; passes 1 and 3 can
  run ahead (they are binding-independent).
- **Attacker-only scope (D5)**; the 6-phase attacker and goldens untouched;
  no MTD / network / statistics-maths changes.
- **The grounding rule is a constraint, not a vibe** — see gate 5. Insight
  yield over attacker strength, every time they conflict.
- **No IDS / detection** (D6/D10, R5); **no timing calibration** (R1 —
  post-MVP); simulation settings are free experimental variables (R4) —
  design to that freedom rather than to the inherited 5000 s convention.
- **Papers are claims** — Caldera and any emulation-planner literature get
  extracted before their designs are cited; one source per pass
  ([`../workflows/guardrails.md`](../workflows/guardrails.md)).
- **Consistency constraint** — the tactic_profiles §5 blocks remain the
  single source of truth for per-tactic behaviour evidence; sketches cite
  them, never fork them; any dissertation.tex §3.1 impact lands in the same
  commit.
- Envelope-not-actor phrasing; determinism (SIM-05); Australian English;
  branch hygiene; **never push without an explicit ask**.

## Reading list

- [`./2026-07-13_l3_mvp_binding_investigation.md`](./2026-07-13_l3_mvp_binding_investigation.md)
  → its signed-off record + ledger — the contract this brief fleshes out.
- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  — D1–D10 and R1–R5, especially R2/R3.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  + [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  — the machinery pass 1 audits.
- Two or three [`../notes/ch3_design/tactic_profiles/`](../notes/ch3_design/tactic_profiles/)
  files end-to-end — the §5 evidence convention the sketches must honour.
- [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)
  — what MTTC/ASR mean here; the comparability boundary any success model
  must respect.

## Out of scope (explicitly)

- **Any implementation** — this produces the scaffold the (deferred) replay
  attacker build and its successors implement.
- **Designing the R3 style vectors** — scoped here, designed after the
  success-model choice and Jin's compose-vs-replace answer.
- **Timing calibration / per-class acceptance criteria** — re-sequenced
  post-MVP ([`./2026-07-09_l3_operational_objective_criteria.md`](./2026-07-09_l3_operational_objective_criteria.md)).
- **Detection/IDS, two-way coupling, multi-token concurrency, RL
  retraining** — standing deferrals.
- **Running Caldera or integrating it as software** — its abstractions are
  the material, never the binary.
