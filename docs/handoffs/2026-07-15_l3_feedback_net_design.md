---
status: open
created: 2026-07-15
---

# Design the live feedback-coupled net (M1/M2/M3) — conditional success/failure weight sets per place, the kill-chain direction mapping, live-stepping and termination semantics, ready for the profiled-attacker build to implement without re-deriving a decision

> **Second in the post-meeting chain — consumes the tactic→action map.** The
> 14-Jul meeting replaced timeline replay with a live net (M1): the token
> steps inside the simulation, the substrate's binary outcome (M2, via the
> oracle contract from
> [`./2026-07-15_l3_tactic_action_influence_map.md`](./2026-07-15_l3_tactic_action_influence_map.md))
> selects between predefined success/failure transition-weight sets, and a
> kill-chain mapping supplies the forward/backward reading (M3). This
> handoff turns those rulings into an implementable contract. The kill-chain
> mapping and stepping semantics can start before the action map lands; the
> per-place weight sets need its verdict definitions.

## State of play

- **What the meeting fixed:** binary outcome → two weight sets per place
  (success: forward transitions live; failure: forward zeroed, retry/
  backward live). Jin considered and rejected the successful/unsuccessful
  twin-net alternative as too complicated — conditional weights are the
  mechanism. Richer outcome classes are sanctioned later "if there's
  something we need to capture". Register:
  [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md) §M1–M3.
- **What exists to build on:** the four weighted class nets + aggregate
  ([`../../data/ogasp/README.md`](../../data/ogasp/README.md)) with
  flow-proportion base weights (D3 — these stand; the outcome *conditions*
  them); the per-tactic duration catalogue
  ([`../../data/ogasp/tactic_durations.json`](../../data/ogasp/tactic_durations.json),
  D4 — dwell survives as how long the token holds a place before/while its
  action fires); per-class termination criteria (objective sets) already
  encoded in the nets; backward transitions already present from the flows.
- **What is undesigned:** how base weights and the outcome override compose
  (mask-and-renormalise vs substitute sets); what "retry" is (self-loop,
  re-fire after dwell, attempt cap before forced fallback); which CKC phase
  each of the 15 tactics maps to and therefore which transitions count
  forward vs backward at each place; what an MTD interrupt mid-dwell does to
  the token (the meeting's motivating example — losing a foothold should
  move net state); how per-class termination reads now that a run can also
  end by simulation horizon (R4 makes the horizon a free experimental
  variable); seeding and determinism of the live walk (SIM-05).
- **The MITRE caveat is on record:** ATT&CK deliberately orders nothing;
  imposing CKC direction is an assumption of this work (M3). The design
  record should carry the one-paragraph defence — it will become
  dissertation material.

## Recommended approach

**Deliverable = one design record**
(`docs/implementation/pipeline/ogasp/feedback_net_design.md`) — the contract
the build implements. Sections:

1. **The CKC direction layer (M3).** Map the 15 tactics onto kill-chain
   phases (cite the published CKC↔ATT&CK mappings; extraction stub if one is
   load-bearing). Derive, per place, which outgoing transitions are
   *forward*, *lateral* (same phase), and *backward*. Record the
   no-ordering-in-ATT&CK assumption and its defence.
2. **The conditional weight contract (M2).** Per place: base weights (D3
   priors) and the success/failure masks over them. Recommend one
   composition rule (e.g. outcome masks the eligible transition set, then
   base weights renormalise within it — preserves the grounded proportions
   instead of inventing new numbers) and name the alternatives. Define
   retry semantics and a stall rule (failure at a place whose failure set is
   empty — what happens; the timeline runner's stalled-sink finding is the
   precedent to handle, not repeat).
3. **Live-stepping semantics (M1).** The token's lifecycle inside SimPy:
   enter place → dwell (D4 duration) → fire mapped action(s) via the oracle
   → read binary verdict → select weight set → sample next transition under
   the run seed. Specify what an MTD interrupt mid-dwell/mid-action does
   (recommend: the interrupted action reads as the failure verdict, so the
   net falls back — this is exactly the feedback the meeting wanted
   captured; name alternatives). Specify per-class termination: objective
   set reached, plus horizon end as the R4-governed censoring case.
4. **Determinism and records.** Seeding rule (SIM-05: same net + seed +
   substrate seed → same walk); the per-event record the attacker emits
   (place, action, verdict, weight set used, transition taken, sim time) so
   MTTC/ASR and the M8 metrics review can be computed downstream.

*Alternatives considered:* designing the full capability precondition/effect
contract now (the binding record's C2) — rejected: M1's ruling is the
minimal conditional-weights form; C2 stays the named upgrade path. Skipping
the design record and going straight to code — rejected: the register/spec
convention here is contract-first, and the CKC mapping is a defensible-
assumption argument that needs writing down once, properly.

## Validation gate

Done when:
1. Every place in each class net has: CKC phase, forward/lateral/backward
   partition of its out-transitions, and success/failure weight treatment —
   no place left implicit, stall rule included.
2. One composition rule and one interrupt policy are recommended with
   alternatives named and killed in prose.
3. The stepping lifecycle is specified end-to-end (enter → dwell → act →
   verdict → weights → transition), including termination and censoring.
4. The determinism statement and per-event record schema exist.
5. The record is implementable without further decisions — the build
   handoff's author could code from it cold.
6. Marc has reviewed it. **No code changes anywhere.**

## Hard constraints

- **Binary outcome only (M2)** — richer classes are a named extension, not
  a designed one.
- **D3 base weights stand** — the outcome conditions the grounded
  proportions; never re-derive or hand-tune them
  ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) §(f)).
- **D4 durations are consumed as-is** — calibration stays post-MVP (R1).
- **Attacker-only (D5)** — nothing in the contract may require touching
  network/MTD/statistics behaviour.
- **The MTTC event definition is untouched** for the 6-phase baseline
  ([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) §(a)).
- Envelope-not-actor phrasing; determinism (SIM-05); branch hygiene;
  **never push without an explicit ask**; Australian English.

## Reading list

- [`../implementation/pipeline/ogasp/supervisor_decision_register.md`](../implementation/pipeline/ogasp/supervisor_decision_register.md)
  — §M1–M3 verbatim; the D3/D4 regimes.
- [`./2026-07-15_l3_tactic_action_influence_map.md`](./2026-07-15_l3_tactic_action_influence_map.md)
  → its record — the verdict definitions this design consumes.
- [`../../data/ogasp/README.md`](../../data/ogasp/README.md) +
  [`../../data/ogasp/petri/`](../../data/ogasp/petri/) — the nets, weights,
  objective sets, and the stalled-sink finding.
- [`../implementation/pipeline/ogasp/binding_design_space.md`](../implementation/pipeline/ogasp/binding_design_space.md)
  §5b — the MTTC verb-identity constraint that still binds any dispatch.
- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the SimPy interrupt pattern the stepping semantics must coexist with.

## Out of scope (explicitly)

- Implementation (the build handoff).
- R2 success-rate tuning, R3 styles, the C2 capability layer, richer
  outcome classes — extension hooks to name, not design.
- Re-weighting, duration calibration, corpus expansion.
