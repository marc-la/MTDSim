---
status: durable
created: 2026-07-28
topic: "The within-run attacker-state seam (BUILT 2026-07-28) — a movement-layer-only mutable memory and a generalised modulator composition, the one shared foundation the stealth / incentive / learning axes (criterion axes 5–7) all need. Records the composition rule, the null-equivalence guarantee that keeps it ablatable, the fourth RNG stream and its isolation, the dwell-only routing change and its behaviour-neutrality proof, and — written out for Marc to take to the supervisor — the argument that a within-run movement-layer state is not the attacker-state change the S2 freeze forbids."
updated: 2026-07-28
---

# The within-run attacker-state seam — design record (BUILT 2026-07-28)

**Status:** durable design-and-build record. It ships the foundation the
[`../../apt_model_criterion.md`](../../apt_model_criterion.md) axes 5–7 all
depend on — a within-run attacker state and a third factor in the routing
composition — built so that its **null configuration is bit-identical to a run
without it**. The build landed 2026-07-28: `src/mtdsim/l3_simulation/movement/state.py`
(new), a one-line routing change in
[`movement/attacker.py`](../../../../src/mtdsim/l3_simulation/movement/attacker.py),
a wiring parameter on
[`movement/run.py`](../../../../src/mtdsim/l3_simulation/movement/run.py),
narration in [`trace.py`](../../../../src/mtdsim/l3_simulation/trace.py), and
[`tests/l3_simulation/test_movement_state.py`](../../../../tests/l3_simulation/test_movement_state.py)
(new). It discharges the foundation handoff
`2026-07-28_attacker_state_seam.md`.

**The one governance question is unresolved and flagged for Marc** — see §7. The
mechanism is built because building it is safe under the null-equivalence
guarantee (nothing changes until a modulator with a declared value is
registered, and no such modulator exists yet); *using* it in an experiment is
what the supervisor confirmation gates. This record makes the S2 argument in
full so that confirmation is a yes/no, not a re-derivation.

## 1. What was built, in one paragraph

`AttackerState` is a plain mutable object, constructed once per run and seeded
from the run seed, that accumulates within-run knowledge (per-place visit
counts, per-place verdict counts, the ordered trajectory) and exposes a
`modulate(src, base_out_weights)` hook returning a per-destination multiplier.
It is attached to a run by **wrapping the two collaborators the walk already
consumes** — not by editing the walk. `StatefulTiming` wraps the
`TimingSource`, calling `state.observe_visit(place)` before delegating `draw`;
`ModulatedOverlay` wraps the `OutcomeOverlayLike`, calling
`state.observe_verdict(src, verdict)` before delegating `compose`, then
multiplying the composed distribution by `state.modulate(...)` and
renormalising. Both forward unknown attributes through `__getattr__`, exactly
as the trace tool's `_TracedTiming` / `_TracedOverlay` do — so a stateful
wrapper is not a novel trick, it is the established seam. Stealth, learning and
utility are **modulators** registered on the state, each owned by its own axis
handoff with its own declared parameters; this record declares none.

## 2. The generalised composition rule

With modulators registered, the routing weight at a source `a` whose action
returned verdict `v` becomes

```
                base(a→b) · overlay_v(a→b) · Π_m  m(a→b | state)
    w'(a→b)  =  ────────────────────────────────────────────────────
                Σ_b'  base(a→b') · overlay_v(a→b') · Π_m  m(a→b' | state)
```

renormalised over the source's out-set, exactly as
[`success_failure_overlay_design.md`](success_failure_overlay_design.md) §1
already renormalises the first two factors. Three constraints make this safe,
and each is a mechanism guarantee, not a convention:

- **Every modulator returns 1.0 in its null configuration**, so `Π_m = 1` and
  the arithmetic reduces to the current two-factor rule. This is what makes
  each axis independently ablatable and what defuses the S2 confounding
  objection (§7): the conditioned and unconditioned arms differ by a parameter,
  never by wiring.
- **Multiplicative, never additive** — the same argument the overlay design
  made and won: multiply-then-renormalise conditions the grounded proportions
  without inventing a magnitude or inverting the corpus's within-class
  ordering. An additive third term would need an arbitrary clamp and could
  invert the ordering.
- **No modulator may return 0.0 without declaring `may_zero = True`.** Zeroing
  an out-set is the one way to manufacture a stall, and stalls are currently
  representable but unobserved
  ([`weight_sensitivity_study.md`](weight_sensitivity_study.md) §3). `modulate`
  raises `ValueError` on an undeclared zero (or any negative factor). A
  modulator that does declare `may_zero` **owes a declared rule licensing the
  zero and a re-run of the no-stall check across its parameter space** — the
  mechanism enforces the declaration; the obligation to justify it is the axis
  handoff's.

The state's `modulate` composes the registered modulators' factors into one
product per destination; `ModulatedOverlay` applies that product to the inner
overlay's already-composed distribution. The two steps are separate on purpose:
the inner overlay stays the sole owner of verdict/composition semantics
(consume, never fork), and the wrapper adds exactly the third factor.

## 3. The null-equivalence guarantee — the load-bearing property

The whole line of work rests on one claim: **attach a null-configured state and
the run is bit-identical to a run without it.** It is tested as the first and
hardest gate in `test_movement_state.py`:
`test_a_null_configured_state_leaves_the_walk_bit_identical` runs every one of
the five profiles at five seeds under both MTD conditions and both mappings, and
asserts the record streams are equal field for field
(`dataclasses.asdict`-level), plus `reached_objective` and `termination_time`.
A null state still *observes* the whole trajectory
(`test_the_null_state_still_observed_the_whole_trajectory`) — bit-identical does
not mean inert; it means the accumulated knowledge is never acted on, because
`Π_m = 1`.

Why bit-identical rather than distributionally-equal: the state must not perturb
the token sampler's or the dwell stream's sequences. If it drew from either, or
advanced either, the walk would reorder. Bit-identity across seeds and profiles
is the falsifiable form of "the state is inert until a modulator fires".

## 4. Determinism — the fourth stream (SIM-05)

Three seeded streams already exist and are deliberately isolated: the token
sampler (`MovementAttacker._rng`), the per-tactic dwell
([`timing.py`](../../../../src/mtdsim/l3_simulation/movement/timing.py),
`derive_timing_seed(seed) = seed ^ 0x54494D45`), and the substrate's global
`random`/`numpy` dice. A modulator needing randomness draws from a **fourth**
stream — `AttackerState.rng`, seeded by `derive_state_seed(seed) = seed ^
0x53544154` ("STAT") — by the identical pure-XOR pattern. The XOR is a bijection
with no fixed point, and the constant differs from the timing stream's, so the
state's dice never coincide with the run seed, the timing stream, or another
run's state stream (`test_the_state_seed_is_a_pure_transform_and_distinct...`).
The stream is constructed even with no modulators, and constructing it draws
nothing from anywhere. **Prefer modulators that are deterministic functions of
the run's own history** (as the demonstration modulator is) — they need no
stream at all and keep SIM-05 trivially intact.

## 5. The dwell-only routing change — the one driver edit, proven neutral

A dwell-only place previously bypassed `compose` entirely: the driver sampled
`base_out_weights(place)` directly. Under `v2_partial` that is 7 of 15 tactics,
including `stealth` — so a state-conditioned modulator would silently not apply
at exactly the places axis 5 cares about most, and a learning attacker could not
learn to avoid a dwell-only place. The edit routes the dwell-only branch through
the same `_route(place, verdict)` the action-bearing branch uses, passing the
distinguished verdict `VERDICT_NONE = "none"`.

It is **provably behaviour-neutral** because `compose` looks up
`by_verdict.get(verdict, {})`: no overlay registers `"none"`, so the per-source
table is empty, every destination is an unconditioned passthrough at factor 1.0,
and the result is the base weights renormalised — which `_sample` normalises by
the total anyway, so the sampled distribution is identical. Proven, not
asserted:

- **Captured before/after evidence.** The record streams of 100 configurations
  (5 profiles × 5 seeds × 2 mappings × 2 MTD conditions) were captured before
  the edit and again after; **all 100 are equal field for field** (0 differ).
  The capture script is a throwaway
  (`scratchpad/capture_records.py`), the evidence is this count.
- **In-suite guard.** `test_dwell_only_routing_through_compose_matches_base_weight_sampling`
  keeps it true, exercised on `v2_partial` where dwell-only places exist.

A consequence worth noting: the state now observes a `"none"` verdict at every
dwell-only place (visible in `snapshot()["verdicts"]`), which is exactly the
observation a stealth or learning modulator wants — a dwell-only place is a
routing decision like any other, now that it flows through the one seam.

## 6. Persisting the trajectory — the state's own log, not the record schema

A modulator that changes routing invisibly is unanalysable. The state carries
its own per-step `log` (one entry per routing decision: the source, the verdict,
and the non-unit factors it applied) that an experiment persists **alongside**
the `MovementRecord` stream. The record schema itself is **untouched**: it is
consumed by the trace tool and every reader, and a schema change ripples further
than this seam should. A null-configured run logs empty `factors` dicts, so the
log's presence never implies an effect the run did not have.

## 7. The S2 argument — written out for the supervisor

**The question.** S2 freezes the attacker action set: "No attacker action,
ability, or **attacker state** is added, removed, or altered; do not change the
MTDSim code yet"
([`supervisor_decision_register.md`](supervisor_decision_register.md) §S2). A
within-run attacker state names exactly what that clause forbids. The argument
that this build is nonetheless inside the freeze — which Marc should put to Jin
explicitly rather than assume:

1. **The freeze's stated reason is confounding, and it is about the action
   layer.** Experiment 1's two failure modes are attributable to the inherited
   phases' tight integration and to the coarse tactic→verb collapse; changing
   the *action set* while both are in play would confound which one the numbers
   measure. That reasoning targets the substrate's action machinery — the verbs,
   abilities and `Adversary` fields — not the portable movement layer above it.
2. **M7 is the countervailing ruling.** The movement layer is "a new
   layer/attacker class … that plugs into the existing simulator's action
   machinery as an interface", with deep edits to the existing model explicitly
   avoided (§M7). `AttackerState` lives entirely in the movement layer and
   reaches the substrate only through the same six verbs, via the same two
   Protocol seams the walk already consumed. It adds **no attacker action, no
   ability, and no substrate state**: no new verb, no `Adversary` field, no
   change to what the substrate can do or be asked to do. The literal MTDSim
   code (`mtdnetwork/`) is untouched — every line of this build is under
   `src/mtdsim/l3_simulation/`.
3. **The confounding risk is eliminated by construction.** Every modulator has a
   null parameter at which the run is bit-identical to today (§3). The
   conditioned and unconditioned arms are therefore both measurable in the same
   experiment, differing by one declared parameter — which is the *opposite* of
   confounding. Nothing this build ships changes any number until an axis
   handoff registers a modulator carrying a declared value, and that is the
   point at which the axis handoff, not this one, makes its own case.

**What is being asked of Jin:** confirm that a within-run, movement-layer,
null-equivalent attacker state is refinement of the movement layer under M7
rather than the attacker-state change S2 defers. It is cheap to confirm and
expensive to get wrong, and it is the single governance question common to the
stealth, incentive and learning handoffs. Until it is confirmed, no modulator
with a declared value is wired into any experiment.

## 8. Alternatives considered and rejected

- **Widen the `compose` signature to take a state argument (Route B).** Cleaner
  to read, but it moves four call sites in lockstep (`outcome.py`, the Protocol,
  `_route`, `_TracedOverlay`) plus every test double, and forces every overlay
  to know about state whether it uses one or not. The wrapper composition did
  not turn contorted, so this stays the recommended fallback, not the starting
  point — per the handoff's out-of-scope note.
- **Put the state on the substrate's `Adversary`.** Rejected: it is the S2
  collision made real, it would be visible to the baseline arm, and
  `Adversary.observed_changes` (an empty dict at `adversary.py:23`, never read
  or written) is a standing warning about how such hooks age.
- **Mutate the `RoutingNet`'s weights per run.** Rejected: it is a frozen
  dataclass handing out copies by design, and mutating structure to express
  policy confuses the two layers the verification record was careful to
  separate (structure vs policy).

## 9. Validation gate — status

All seven gates from the handoff are met:

1. **Null-equivalence** — `test_a_null_configured_state_leaves_the_walk_bit_identical`,
   5 profiles × 5 seeds × 2 MTD conditions × 2 mappings, equal field for field. ✓
2. **Dwell-only routing proven neutral** — 100-configuration before/after
   capture (0 differ) plus the in-suite guard. ✓
3. **The seam is live** — `test_a_registered_modulator_visibly_changes_the_walk`:
   the artificial `RevisitAversionDemo` changes the walk relative to the null
   run. ✓
4. **RNG isolation** — `test_attaching_a_null_state_does_not_perturb_the_other_streams`
   (dwells and routing element-for-element) and the distinct-fourth-stream
   test. ✓
5. **Trace narrates the state, parity holds** — `test_a_stateful_run_narrates_the_state_evolving`
   and `test_a_stateful_run_traces_identically_to_run_movement`; the existing
   stateless parity gate still passes. ✓
6. **Seam invariants hold** — `test_seam_invariants.py` green; the controller
   stays SimPy-free and the net imports no controller (state.py imports only
   the timing Protocol, no SimPy). ✓
7. **This record** — carrying the composition rule, the null-equivalence
   guarantee, the RNG discipline, the dwell-only argument, and the S2 argument
   written out. ✓

Full suite: 355 passed.

## 10. What this does not do

- **Declares no value.** No stealth level, no learning rate, no utility — the
  one modulator here (`RevisitAversionDemo`) is deliberately artificial and must
  not be wired into any experiment.
- **No cross-run memory.** Everything is within-run; a state that persists
  between runs is the attacker-that-studies-the-campaign (M8d), a different
  claim and a different handoff.
- **Changes no overlay rule, mapping, net or timing value**, and moves no badge
  on the criterion. The badges move when an axis handoff registers a modulator
  and an experiment shows it changing an outcome — this record only makes that
  possible.
