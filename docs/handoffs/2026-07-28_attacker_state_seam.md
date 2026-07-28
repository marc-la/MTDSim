---
status: open
created: 2026-07-28
---

# Give the movement layer a within-run attacker state and a generalised modulator composition — the one shared foundation stealth, incentive and learning all need, built so that its null configuration is bit-identical to today

**Chain position: wave 5, foundation.** Blocks `2026-07-28_axis7_learning_capability.md`,
`2026-07-28_axis6_incentive_rationality.md` and the build half of
`2026-07-28_axis5_stealth_conceptualisation.md`. Independent of the measurement suite and
of experiment 2 — it can be built in parallel with either. **Do not build it three times.**
Three axes each want a mutable attacker state and a third factor in the routing
composition; if each handoff grows its own, they collide in `compose` and in the RNG
discipline, and none of them will be ablatable against the others.

## State of play

**The movement attacker has no memory.** `MovementAttacker`'s entire mutable per-run state
is `records` (a log), `_rng` (the token sampler), `timing`, and `_proc`. The walk's own
state is two local variables in `_walk`'s frame: `place` and `step_index`. The substrate's
`Adversary` carries more — `compromised_hosts`, `compromised_users`, `_attack_counter`,
`_stop_attack` — but `curr_ports` and `curr_vulns` are wiped at every hop, and there is no
record of *what was tried and how it went*. The criterion states the consequence twice:
axis 4's adaptation "does not update from experience", and axis 7 is NOT ADDRESSED because
"the movement attacker carries no memory across runs and no within-run knowledge
accumulation beyond the token's position and the binary verdict at the current place".

**The composition is a pure function and the injection points are Protocols.**
`OutcomeOverlay` is a frozen dataclass and `compose(src, verdict, base_out_weights)` reads
nothing but its own table — no clock, no RNG, no globals. Both collaborators the walk
consumes are **structural** `Protocol`s, not concrete types:

- `OutcomeOverlayLike.compose(src, verdict, base_out_weights) -> dict[str, float]`,
  injected at `run_movement(overlay=...)`, called once per action-bearing step from
  `MovementAttacker._route`.
- `TimingSource.draw(tactic) -> float`, injected at `run_movement(timing=...)`, called
  **once per place visit** — before the verb/dwell-only branch, so it fires on *every*
  place the token enters, whatever the place does.

**That pairing is the whole observation surface a stateful attacker needs, and it already
exists.** `draw(place)` sees every visit; `compose(place, verdict, …)` sees every verdict.
Together they reconstruct the trajectory without the driver knowing anything about it.

**And the pattern is already in the repo.** `src/mtdsim/l3_simulation/trace.py` wraps
*both* — `_TracedOverlay` and `_TracedTiming` hold mutable tracer state, delegate to an
inner object, and forward everything else through `__getattr__`. The S1 sweep drives its
own overlay points the same way, through `OutcomeOverlay.from_values` passed into
`run_movement`. So a stateful wrapper is not a novel trick here; it is the established
seam, and it means this foundation costs **no edit to the walk at all**.

**One real gap.** A dwell-only place never calls `compose` — the driver samples
`base_out_weights(place)` directly. Under `v2_partial` that is **7 of 15 tactics**,
including `stealth`. So a state-conditioned modulator would silently not apply at exactly
the places axis 5 cares about most, and a learning attacker could not learn to avoid a
dwell-only place. This is the one thing that must change in the driver, and it changes
nothing behaviourally — see step 3.

**The governance question, which must be answered before building.** S2 freezes the
attacker action set: "No attacker action, ability, or **attacker state** is added, removed,
or altered; **do not change the MTDSim code yet**". A within-run attacker state looks like
exactly what that forbids. The argument that it is not, which the next session should make
explicitly rather than assume:

- The freeze's stated *reason* is confounding — experiment 1's two failure modes are
  attributable to the inherited phases' tight integration and to the coarse tactic→verb
  collapse, and changing the action set while both are in play would confound which one the
  numbers measure. That reasoning is about the **action layer**.
- M7 is the countervailing ruling: the movement layer is "a new layer/attacker class …
  that plugs into the existing simulator's action machinery as an interface", with deep
  edits to the existing model explicitly avoided. State that lives in the movement layer
  and reaches the substrate only through the same six verbs adds no action, no ability, and
  no substrate state.
- The confounding risk is eliminated by construction here, because every modulator has a
  null parameter at which the run is **bit-identical** to today. The conditioned and
  unconditioned arms are both measurable in the same experiment, which is the opposite of
  confounding.

Record that argument in the design record; flag it for Marc to confirm with the supervisor.
It is cheap to confirm and expensive to get wrong, and it is the single governance question
common to three handoffs.

## Recommended approach

**1. `AttackerState` — one plain object, movement-layer only.** A small mutable class
holding within-run knowledge, constructed per run, seeded from the run seed, with two
observation methods and no opinions about what the knowledge means:

- `observe_visit(place)` — called on every place entry.
- `observe_verdict(place, verdict)` — called on every action-bearing routing decision.
- a `modulate(src, base_out_weights) -> dict[str, float]` hook returning a per-destination
  multiplier, defaulting to all-1.0.

It knows nothing about stealth, learning, or utility. Those are **modulators** registered on
it, each with its own declared parameters. This keeps three handoffs from fighting over one
class.

**2. Wire it through the two existing Protocols, not through the driver.** A
`StatefulTiming` wrapping the real `TimingSource` calls `state.observe_visit(tactic)` then
delegates `draw`; a `ModulatedOverlay` wrapping the real overlay calls
`state.observe_verdict(src, verdict)`, delegates `compose`, then multiplies the result by
`state.modulate(src, …)` and renormalises. Both forward unknown attributes via
`__getattr__`, exactly as the traced wrappers do. `run_movement(timing=…, overlay=…)`
wires them. **Zero edits to `MovementAttacker`.**

Note the per-step ordering and rely on it deliberately: `draw` fires before the dispatch,
`compose` after it. So within a step the state sees the visit first and the verdict second,
which is the causal order and the one a modulator wants.

**3. Route dwell-only places through `compose` too, with a distinguished verdict.** This is
the one driver edit, and it is provably behaviour-neutral. At
`MovementAttacker._walk`'s dwell-only branch, replace the direct
`self._sample(self.routing.base_out_weights(place))` with the same `self._route(place, …)`
call the action-bearing branch uses, passing a verdict of `"none"`. Because `compose` looks
up `self.by_verdict.get(verdict, {})`, an unregistered verdict yields an empty per-source
table, every destination gets factor 1.0, and the result is the base weights renormalised —
and `_sample` normalises by the total anyway, so the sampled distribution is identical.

**Prove it rather than assert it:** a test that runs every profile at several seeds before
and after the change and asserts the record streams are equal field for field. If they are
not, something else was assumed wrong and it is better to find out here.

**4. The generalised composition.** With modulators registered, the routing weight becomes

```
w'(a→b)  ∝  base(a→b) · overlay_v(a→b) · Π_m  m(a→b | state)
```

renormalised over the source's out-set, exactly as today. Constraints that make this safe:

- **Every modulator returns 1.0 in its null configuration**, so the product is 1 and the
  arithmetic reduces to the current rule. This is what makes each axis independently
  ablatable and what defuses the S2 confounding objection.
- **Multiplicative, never additive** — the same argument the overlay design already made
  and won: multiply-then-renormalise conditions the grounded proportions without inventing
  a magnitude or inverting the corpus's within-class ordering.
- **A modulator may not return 0 without a declared rule saying so**, because zeroing an
  out-set is the one way to manufacture a stall, and stalls are currently representable but
  unobserved. If a modulator can zero an edge, the stall check must be re-run.

**5. Determinism.** Any modulator needing randomness derives a **fourth** stream by the
established pattern — a pure XOR transform of the run seed, as
`derive_timing_seed(seed) = seed ^ 0x54494D45` does — so it neither reads nor advances the
token sampler, the dwell stream, or the substrate's global dice. Prefer modulators that are
**deterministic functions of the run's own history**, which need no stream at all and keep
SIM-05 trivially intact.

**6. Persist the state's trajectory into the records, or not at all.** A modulator that
changes routing invisibly is unanalysable. Either add one field to `MovementRecord`
carrying the state summary at that step, or have the state expose its own per-step log that
the experiment persists alongside the records. **Prefer the second**: the record schema is
consumed by the trace tool and by every reader, and a schema change ripples further than
this handoff should.

**7. Extend the trace tool.** `python -m mtdsim.l3_simulation.trace` is the project's first
reach for verifying a change, and it wraps the same two Protocols. A stateful run whose
narration does not show the state moving is a run nobody can debug. This is small and it is
not optional.

**Alternatives considered.** *Widen the `compose` signature to take a state argument
(Route B)* — cleaner to read, but it moves four call sites in lockstep (`outcome.py`, the
Protocol, `_route`, `_TracedOverlay`) plus every test double, and it forces every overlay
to know about state whether it uses one or not. Recommended fallback if the wrapper
composition turns contorted, not the starting point. *Put the state on the substrate's
`Adversary`* — rejected: it is the S2 collision made real, it would be visible to the
baseline arm, and `Adversary.observed_changes` (an empty dict at `adversary.py:23`, never
read or written by anything) is a warning about how such hooks age. *Mutate the
`RoutingNet`'s weights per run* — rejected: it is a frozen dataclass handing out copies by
design, and mutating structure to express policy confuses the two layers the verification
record was careful to separate.

## Validation gate

Done when:

1. **The null-equivalence test passes**: with the state attached and every modulator at its
   null parameter, a seeded run produces a record stream equal field for field to a run
   without the state — across all five profiles and at least five seeds, both MTD
   conditions.
2. **The dwell-only routing change is proven neutral** by its own before/after equality
   test, independently of (1).
3. A trivial demonstration modulator (something obviously artificial — say, halving the
   weight of any destination already visited twice) is shown to change the walk, so the seam
   is proven live and not merely wired.
4. The RNG-isolation property holds: attaching the state does not perturb the token
   sampler's or the dwell stream's sequences. Test the way the S3 stream isolation was
   tested.
5. `python -m mtdsim.l3_simulation.trace` narrates the state's evolution on a stateful run,
   and the existing trace parity gate against `run_movement` still passes.
6. The four seam invariants still hold — in particular that the controller sublayer stays
   SimPy-free and the movement net imports no controller.
7. A design record under `docs/implementation/pipeline/ogasp/` carrying the composition
   rule, the null-equivalence guarantee, the RNG discipline, the dwell-only routing
   argument, and **the S2 argument written out** for Marc to take to the supervisor.

## Hard constraints

- **Null configuration is bit-identical to today.** This is not a nicety; it is what makes
  the whole line of work ablatable and what answers the confounding objection S2 rests on.
- **No substrate change.** No new attacker action, ability, or `Adversary` field. The
  movement layer reaches the substrate only through the existing six verbs.
- **Consume, never fork.** The driver's contract is that it carries zero dispatch,
  composition or verdict semantics of its own. A wrapper must delegate, not reimplement.
- **Determinism / SIM-05.** Three seeded streams exist (token sampler, dwell, substrate
  globals) and are deliberately isolated. Add a fourth by the same pattern or add none.
- **No modulator may zero an out-edge** without a declared rule, and if one can, the
  no-stall check must be re-run across the declared parameter space.
- **This handoff declares no values.** It builds the mechanism. Every declared parameter
  belongs to the axis handoff that needs it, under the declared-value discipline
  (rule-generated, tiered, adversarially scrutinised, swept).
- Australian English; branch and commit rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.

## Reading list

- `src/mtdsim/l3_simulation/trace.py` — `_TracedOverlay`, `_TracedTiming`, `_TracedVerdict`.
  This is the pattern to copy; read it before designing anything.
- `src/mtdsim/l3_simulation/movement/attacker.py` — `_walk` (the per-step order: `phase_for`
  → `draw` → dispatch → `_route`), the dwell-only branch that bypasses `compose`, the two
  collaborator Protocols, and the RNG comments.
- `src/mtdsim/l3_simulation/controller/outcome.py` — `compose`'s absent-pair passthrough
  (the property the dwell-only change relies on) and `from_values`.
- `docs/implementation/pipeline/ogasp/success_failure_overlay_design.md` §1 and §6 — the
  composition rule this generalises, the alternatives already killed (substitute weight
  sets, additive bias, solving the nets), and the determinism contract.
- `docs/implementation/pipeline/ogasp/supervisor_decision_register.md` §S2 and §M7 — the
  freeze and the layer ruling, which is the governance argument this handoff must make.
- `src/mtdsim/l3_simulation/movement/timing.py` — `derive_timing_seed` and the
  stream-isolation argument to copy for a fourth stream.

## Out of scope (explicitly)

- **Any declared value.** No stealth level, no learning rate, no utility. This handoff
  ships a mechanism whose null behaviour is the current behaviour, and nothing else.
- Cross-run memory. Everything here is within-run; a state that persists between runs is a
  different claim (the attacker that studies the campaign, M8d) and a different handoff.
- Changing the overlay rules, the mapping, the nets or the timing values.
- Running any experiment or moving any badge.
- Widening the `compose` signature, unless the wrapper composition is tried first and found
  wanting — and if so, say why in the record.
