---
status: durable
chapter: ch4_implementation
created: 2026-08-01
updated: 2026-08-01
---

# Four channels are what a host simulator must expose for an intelligence-derived attacker to drive it

## Position in the dissertation

The implementation chapter's portability argument: the claim that the attacker
framework can be re-hosted, made concrete enough to be falsifiable — a named
interface, a named integration cost, and a named ceiling — rather than left as
an adjective.

## The idea

The attacker model built in this project is designed to be separable from the
simulator it currently runs against: its campaign structure, routing policy and
behavioural parameters live in their own layer, and the simulator underneath is
treated as an execution environment. That separation is only worth claiming if
it can be stated as a contract — what, exactly, must the next host provide? The
implementation answers with four channels, and the list is exhaustive in both
directions: everything the attacker layer consumes is one of the four, and
removing any one of them disables a named capability.

First, an **action vocabulary**: the host's attacker-side operations, callable
one at a time. The attacker layer decides *what the campaign does next*; the
host executes what that resolves to and must therefore expose its attack
operations as individually invocable steps rather than as a closed loop. Second,
a **per-action verdict**: a readable outcome for each dispatched action, at
minimum success or failure. The verdict is what couples the campaign to the
terrain — without it the attacker can traverse its own structure but never
react, and the entire adaptive layer (outcome-conditioned routing, and the
learning capability built above it) is defined on this channel. Third, an
**interrupt signal**: notice that the defence has acted, distinguishable from
ordinary failure. A moving-target mutation and a failed exploit both interrupt
progress, but they mean different things to an attacker model — one perishes
accumulated knowledge and severs position, the other is information about the
terrain — and a host that folds interrupts into failures silently disables
every capability that responds to the defence as such. Fourth, a **time
channel**: a shared clock into which the attacker layer can spend time that is
not attached to any host action. Campaign behaviour is temporal — much of an
observed campaign is dwell, activity the host has no operation for — and a host
that only advances time when its own actions run cannot express an attacker
whose tempo is part of its behaviour.

The claim that this contract is portable is credible only with its cost
attached, and the cost was not small. The host simulator used here exposed none
of the four channels natively. Its inherited attacker is a self-contained
procedure — decision, action, outcome and timing fused in one loop — so an
action-dispatch surface had to be carved into it: the attack operations
separated into individually callable steps, each returning a readable verdict,
with the interrupt path preserved distinctly through the refactoring. The time
channel cost more. The first integration split timing between the layers — the
attacker layer supplying behavioural dwell on top of the host's native action
costs — and that hybrid did not survive contact with supervision: it was
reversed in favour of the attacker layer supplying *every* unit of the
attacker's time, a re-homing that changed what a blocked attempt costs, retired
the host's action pricing from that arm entirely, and withdrew cross-arm
comparability of the host's native per-action timing metric rather than
defending it. Stating this plainly is the point: a portability claim whose
integration cost is named — two structural interventions, one of them revised
after being built once — is worth more than one that promises a clean adapter,
and a successor porting this framework to another simulator should budget for
the same two interventions there.

The contract also fixes the framework's ceiling, and the ceiling is the host's,
not the intelligence's. Behavioural fidelity downstream of the interface is
bounded by the action vocabulary: this host exposes six attack operations, so
the fifteen adversary tactics the campaign layer traverses resolve onto six
verbs, many-to-one, with seven tactics resolving to no operation at all and
contributing time but no act. Enriching the attacker's side of the interface
cannot raise this bound. The upstream pipeline is already technique-grained — resolving adversary
behaviour at a granularity many times finer than tactics — and executing at technique
granularity over the same six verbs would multiply the mapping's declared cells
without adding one distinguishable behaviour: a technique-grained attacker over
a six-verb host gains sequencing resolution and no behavioural resolution.
Anyone weighing the port should therefore evaluate the target host by its
vocabulary first, because that — not the richness of the threat intelligence —
is what fidelity is bounded by after everything else is done well.

What makes the contract falsifiable is that it can fail in public: a host that
cannot be given the four channels cannot run this attacker, and a port whose
cost greatly exceeds the two named interventions falsifies the cost claim. The
negative scope is equally plain. The contract has been exercised against one
host; four channels are what *this* integration needed, and a host with a
fundamentally different execution model may demand a fifth. Nothing here claims
the port is cheap — only that it is priced.

## Evidence and repo anchors

- The carved action-dispatch surface and per-verb verdict semantics:
  [`../../implementation/pipeline/ogasp/action_layer_anatomy.md`](../../implementation/pipeline/ogasp/action_layer_anatomy.md)
  and [`../../implementation/pipeline/ogasp/controller.md`](../../implementation/pipeline/ogasp/controller.md)
  §3–§4.
- The timing re-homing (hybrid ruled, built, then reversed — S3-R) and the
  withdrawal of cross-arm per-action timing:
  [`../../implementation/pipeline/ogasp/stochastic_timing_design.md`](../../implementation/pipeline/ogasp/stochastic_timing_design.md)
  §2 and its superseding banner.
- The interrupt path's distinct observation (interrupts otherwise arrive
  flattened into failures):
  [`../../implementation/pipeline/ogasp/attacker_state_seam.md`](../../implementation/pipeline/ogasp/attacker_state_seam.md)
  and [`../../implementation/pipeline/ogasp/learning_capability.md`](../../implementation/pipeline/ogasp/learning_capability.md).
- The vocabulary ceiling and the technique-level judgement:
  [`../../implementation/pipeline/ogasp/model_scope_freeze.md`](../../implementation/pipeline/ogasp/model_scope_freeze.md)
  §3 (items 4–5); the dwell-only tactics:
  [`../../implementation/pipeline/ogasp/controller_mapping_v2.md`](../../implementation/pipeline/ogasp/controller_mapping_v2.md).
- The architectural seam this contract formalises:
  [`../../implementation/architecture.md`](../../implementation/architecture.md).

## Revisit conditions

- If the framework is ported to a second host, this note is rewritten against
  the observed cost: the contract either held (and gains its first external
  evidence) or gained a fifth channel (and the "exhaustive" claim falls).
- If the host's action vocabulary is ever widened, the ceiling argument must be
  re-derived — and the technique-level judgement re-opened, since its balance
  rests on six verbs.
- If the inherited attacker's phase layer is reworked (named future work), the
  integration-cost account here becomes partially historical and says so.
