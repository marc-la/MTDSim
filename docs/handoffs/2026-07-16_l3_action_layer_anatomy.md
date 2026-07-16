---
status: open
created: 2026-07-16
---

# Anatomise the action layer — map the FSM's coupling graph and implicit preconditions, establish what is actually callable by a controller and in what orders, survey the tunable affordances and hard limits, and pre-register the coupling-performance hypothesis

> **Now first in the post-meeting chain — the influence map and feedback-net
> design consume this.** Motivation (Marc, 2026-07-16): the inherited attack
> module is suspected to be a strongly-coupled FSM — phases that depend on
> and coexist with each other — so a movement layer driving them in a
> different, net-imposed order may simply break, or degenerate back toward
> the FSM's own sequence. Confirmed at first glance:
> `_execute_scan_host` calls `self._enum_host()` directly; `ENUM_HOST` pops
> a `host_stack` only `SCAN_HOST` fills; the MTD interrupt handler
> hard-codes its restart phases. The controller layer will be **"the best we
> can do with the tools at hand"** — this record establishes, before any
> mapping or design, what the tools at hand actually are. Read-only
> investigation; the action layer is not modified.

## State of play

- **The vocabulary (runtime view, being formalised by the layer-reframe
  audit):** the **movement layer** is the live class net — token, conditional
  weights, kill-chain direction (M1/M2/M3). The **action layer** is the
  inherited attack module — six verbs (SCAN_HOST / ENUM_HOST / SCAN_PORT /
  SCAN_NEIGHBOR / EXPLOIT_VULN / BRUTE_FORCE) plus their chaining, state,
  interrupt and bookkeeping machinery
  ([`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py),
  [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)).
  The **controller layer** sits between them: the tactic→action dispatch,
  parameterisation, and outcome reading (M5/M7). This handoff is the
  controller's site survey.
- **The coupling is structural, not incidental.** Each `_execute_*` method
  tail-calls the next phase; phases communicate through shared adversary
  state (`host_stack`, `curr_host`, `pivot_host_id`, attack counters,
  `curr_ports`/vulns); preconditions are enforced *only* by the call order.
  Nothing documents which verb can be invoked standalone, from which states,
  with what setup.
- **The affordance question is open.** Beyond calling phases: what is
  parameterised (ATTACK_DURATION table, attempt limits, brute-force chance,
  penalty draw…) vs hard-coded (scan orderings, the interrupt restart
  targets, the compromise test)? Could a controller, without editing the
  action layer, express "boosted scanning at recon" or "slower, careful
  exploitation" — or is per-tactic tuning impossible until future work? The
  limitations register this produces is the honest ceiling of the M5 map and
  direct dissertation material (ch4 design constraints / ch6 future work).
- **Two performance hypotheses now exist and must not be conflated.** M8's
  registered expectation: the profiled attacker underperforms because *the
  metrics don't reward APT-shaped behaviour*. Marc's new hypothesis
  (2026-07-16): it underperforms because *the action layer resists
  reordering* — coupling forces the controller toward the FSM's native
  sequence, eroding the very distinguishability the pipeline exists to add
  (the binding record's anti-goal, via the back door). Distinct mechanisms,
  distinct signatures in the results; pre-register both so first numbers can
  be read against them.
- **What exists already:**
  [`../implementation/substrate_primer.md`](../implementation/substrate_primer.md)
  covers the substrate attacker's-eye and non-implementation-specific — this
  record is its implementation-deep complement, not a rewrite.

## Recommended approach

**Deliverable = one implementation record**
(`docs/implementation/pipeline/ogasp/action_layer_anatomy.md`), four parts:

1. **The coupling graph.** Per verb: what it reads, what it mutates, what it
   tail-calls, and its implicit preconditions (what must already be true or
   populated). Draw the actual phase-transition graph the code implements —
   including the interrupt handler's hard-coded restarts and the give-up /
   terminate paths — so "strongly connected" becomes a diagram with named
   edges, not a suspicion.
2. **The callable surface.** For each verb: can a controller invoke it
   standalone? If not, what minimal context would have to be synthesised,
   or what carve (separating the verb's executable core from its
   call-the-next-phase tail) would be needed — *specified, not performed*.
   Classify each verb: callable-as-is / callable-with-context /
   chain-bound. Then the ordering analysis: which verb orderings are safe,
   which no-op, which break — the reordering-freedom result that feeds the
   hypothesis in part 4.
3. **The affordance and limitations register.** Every tunable the action
   layer exposes (constants, durations, chances, limits) with where it
   lives and what a per-tactic controller could legitimately do with it
   without behaviour edits; and every wanted-but-absent affordance (e.g.
   per-invocation scan boosting) as a named limitation with its future-work
   cost sketch. This register is the M5 map's vocabulary of *parameters*,
   not just actions.
4. **Pre-register the two hypotheses.** State M8's metric-mechanism and the
   coupling-mechanism side by side, each with the result signature that
   would implicate it (e.g. profiled ≈ baseline *and* action sequences
   near-identical → coupling; profiled < baseline *with* distinct sequences
   → metrics). First numbers get read against this section.

*Alternatives considered:* folding this into the influence-map handoff (its
step 1 was a lighter version of this) — rejected: Marc's coupling question
makes the anatomy load-bearing for *feasibility*, not just mapping, and the
map's per-pair verdicts are only meaningful once callability is known.
Carving the verbs now and testing empirically — rejected: no-code
constraint; the carve is specified here and lands, if approved, with the
build.

## Validation gate

Done when:
1. The coupling graph exists — per-verb reads/mutations/tail-calls/
   preconditions and the full phase-transition diagram including interrupt
   and termination paths.
2. Every verb carries a callable-as-is / callable-with-context / chain-bound
   classification, with the synthesis-or-carve requirement specified for the
   non-trivial ones.
3. The ordering analysis states, concretely, how much reordering freedom a
   controller actually has — the honest ceiling, stated as such.
4. The affordance/limitations register exists: tunables with locations and
   legitimate controller uses; absent affordances as named future-work
   limitations.
5. The two performance hypotheses are pre-registered with distinguishing
   result signatures.
6. Marc has reviewed the record. **No code changes anywhere; the action
   layer is read, never edited.**

## Hard constraints

- **Read-only** — no edits to `mtdnetwork/` anything; carves and context
  synthesis are specified for the build, not performed.
- **Attacker-only boundary (D5) still frames future changes** — the
  limitations register may name substrate-side wants, but flags them as
  out-of-boundary future work.
- **Don't conflate the hypotheses** — M8's is supervisor-registered; the
  coupling hypothesis is Marc's, recorded as such (provenance discipline).
- Branch hygiene; **never push without an explicit ask**; Australian
  English.

## Reading list

- [`../../mtdnetwork/operation/attack_operation.py`](../../mtdnetwork/operation/attack_operation.py)
  — the chain itself, in full; the interrupt handler especially.
- [`../../mtdnetwork/component/adversary.py`](../../mtdnetwork/component/adversary.py)
  — the shared state the phases communicate through.
- [`../../mtdnetwork/data/constants.py`](../../mtdnetwork/data/constants.py)
  — the tunable-constants surface (ATTACK_DURATION and kin).
- [`../implementation/substrate_primer.md`](../implementation/substrate_primer.md)
  §(d)/(e) — the attacker's-eye account this record deepens.
- [`../implementation/pipeline/ogasp/binding_design_space.md`](../implementation/pipeline/ogasp/binding_design_space.md)
  — the anti-goal / distinguishability bar the reordering analysis speaks to.

## Out of scope (explicitly)

- The tactic→action influence map itself
  ([`./2026-07-15_l3_tactic_action_influence_map.md`](./2026-07-15_l3_tactic_action_influence_map.md)
  — consumes this record).
- Any carve, wrapper, or new action — build-phase work, gated on this
  record and Marc's review. **Now spun out to
  [`./2026-07-16_l3_action_layer_carve.md`](./2026-07-16_l3_action_layer_carve.md)**,
  which folds in this build-phase component (Marc's ask, 2026-07-16).
- The layer-vocabulary docs audit
  ([`./2026-07-16_l3_layer_reframe_docs_audit.md`](./2026-07-16_l3_layer_reframe_docs_audit.md))
  — parallel, independent.
- R2/R3 tuning design; detection/IDS; anything substrate-behavioural.
