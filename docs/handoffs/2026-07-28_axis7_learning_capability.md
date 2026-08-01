---
status: shipped — awaiting reconciliation
superseded_note: shipped 2026-07-29 — the mechanism, the 2 400-run sweep and the DESIGNED badge landed on `feat/axis134-demonstration-arms`. Retire on reconciliation (`2026-07-29_reconcile_stranded_axis_work.md`). Generalising this mechanism is now `2026-07-29_learning_under_procedural_rigidity.md`.
created: 2026-07-28
---

# Give the attacker a within-run knowledge state that reweights its own routing from what has worked — the learning capability the literature calls the sharpest missing dimension, and the only axis whose demonstration changes the model's fidelity placement

**Chain position: wave 5, after the attacker-state seam (SHIPPED 2026-07-28 —
`docs/implementation/pipeline/ogasp/attacker_state_seam.md`).** Needs the seam's
`AttackerState`, its modulator composition, and its null-equivalence guarantee. Independent
of the stealth and incentive handoffs, though all three compose on the same seam and the
sweep must eventually cross them.

## State of play

**Why this axis is worth more than the others.** Cho et al.'s first and sharpest
under-developed dimension is that attackers are assumed to follow fixed patterns "rather
than that they learn and can launch adaptive attacks", while defenders are routinely
granted learning — an asymmetry contrary to practice. Jalowski's APT "learns mutation
patterns over time". No paper in the cross-section models attacker learning at all; the
field-wide pattern both surveys name is defender RL everywhere and attacker learning
nowhere. And the criterion's own fidelity placement (§(e)) turns on it: the model sits at
the **procedural** rung carrying two of the behavioural rung's three components, and
*"that rung requires learning this model does not have"*. **Axis 7 is the only axis whose
demonstration would change the placement claim.** That is the prize, and it should be
stated as such in whatever is written.

**Why it is also the mitigation.** Experiment 1's *friction* failure mode is the inherited
substrate's rigid precondition order punishing an attacker that walks CTI tactic-order
instead: `pure_steal` spent 95 % of its action budget on verbs the substrate refused, and
the driver deliberately does **not** re-impose the native order, because doing so would
manufacture the very coupling the evaluation exists to expose. That leaves a real dilemma —
the honest options have looked like "hand-tune the mapping until it works" (which is
modeller-side fitting) or "report that it does not work" (which is what experiment 1 did).
Learning is a third option, and a better one: it converts a modeller-side fitting problem
into a **modelled attacker capability**. An attacker that discovers the substrate's order
by trial and error is doing exactly what Cho asks for, and the discovery is *the model's*,
not the modeller's. Say this plainly in the design record — it is the strongest
methodological argument available on this axis.

**And it is falsifiable, which matters more.** If the blocked fraction falls within runs as
learning strength rises, and is flat when it is switched off, learning works on this
substrate. If it does not, that is a finding about how learnable this terrain is, and it is
publishable either way. Do not build this expecting it to succeed.

**What exists to build on.** The seam handoff supplies `AttackerState`, the two observation
hooks (`observe_visit` on every place entry, `observe_verdict` on every action-bearing
step), and the multiplicative modulator slot. The measurement suite supplies the
within-run signals. Nothing else is needed.

**One tempting dead end, named so it is not rediscovered.** The substrate already contains
a commented-out attacker-learning mechanism: cross-instance vulnerability learning at
`mtdnetwork/component/services.py`, which is exactly the ATK-04 divergence
`metrics_semantics.md` documents as unimplemented. Uncommenting it would be a *substrate*
change, would move the 6-phase baseline and every golden, and would collide squarely with
S2. It is also the wrong kind of learning for this axis — it is a pricing discount, not a
decision capability. Leave it alone; note in the record that it was considered.

## Recommended approach

**1. Decide what is learned, and keep it myopic.** The unit of credit should be the
**destination place**, not the transition and not the verb. The thing that succeeds or
fails is the action at a place, so the attacker learns *which tactics pay on this terrain*
and biases its next move toward them. Per place `b`, maintain within-run counts of success
and failure verdicts observed at `b`, and estimate

```
    Q(b) = (s_b + α) / (s_b + f_b + α + β)          α = β = 1  (Laplace)
```

so an unvisited place sits at 0.5 and is never zeroed — exploration survives by
construction. The routing modulator is then

```
    m(a→b)  =  Q(b) ^ κ
```

with `κ` the **learning capability**, the input parameter this handoff introduces. At
`κ = 0` the modulator is identically 1 and the run reproduces today bit for bit, which is
the ablation arm and the seam's null guarantee.

Reject longer credit assignment. Propagating credit backwards along the trajectory needs
an eligibility trace and a discount factor, which is reinforcement learning proper — more
declared parameters than the timeframe can defend, and it drags in the machinery axis 8 is
explicitly deferring.

**2. Decide what MTD does to knowledge. This is the interesting half.** MTD's entire
claimed value is destroying what an attacker has accumulated, and the criterion makes the
point twice: an evaluation whose attacker has no multi-stage knowledge to lose cannot
register that value, and MTD's protection degrades fastest against an attacker that
accumulates knowledge across mutations. So the learning state **must** be perishable, and
the perishing must be caused by the defence:

```
    on an MTD interrupt:   s_b, f_b  ←  (1 − ρ) · s_b,  (1 − ρ) · f_b   for all b
```

with `ρ ∈ [0, 1]` a declared forgetting fraction. `ρ = 0` is a learner MTD cannot touch;
`ρ = 1` is total amnesia at every mutation. **This is where axis 7 and the thesis's central
question meet**, and it is the reason this handoff is worth more than a bandit exercise:
the contest between `κ` and `ρ` is the attacker's learning rate against the defender's
mutation rate, which is the same shape as the rate contest the timing work already
established the evaluation turns on.

A per-layer refinement — a network-layer mutation invalidating position knowledge, an
application-layer one invalidating service knowledge — is more faithful and does not map
cleanly onto a state keyed by tactic-place. Name it as the considered alternative, take the
single `ρ`, and leave the refinement to a later cycle.

**3. Keep it within-run.** Cross-run memory is a different claim — the attacker that
studies the campaign across engagements — and it is already parked as future work (M8d,
and axis 8's beacon primitive). Within-run learning matches the APT single-campaign framing
the whole model rests on, and it is what the criterion's own M8b field asks for ("does
success probability against a host class rise with exposure?"). State the boundary; do not
quietly cross it.

**4. Declare `κ` and `ρ` under the declared-value discipline, and sweep them.** Both are
declared judgement — there is no measurement of how fast a real intruder updates. That is
fine and it is the same tier the durations and the routing weights sit at; what is not fine
is choosing them by looking at the outcome. Follow the precedent exactly: a small rule
model, rule-generated values, a tier badge, a scrutiny record, and a generator that
reproduces the set. Bands should be argued from what the parameter *means* (κ = 0 is no
learning; κ = 1 is proportional-to-belief; large κ is near-greedy and should be shown to
collapse plurality), not from what produces a nice number.

**5. Report the tension with axis 3 rather than hiding it.** Learning narrows traversal.
A greedy learner converges on one route, which is the opposite of strategic plurality. Run
path entropy at `κ = 0` and at the declared `κ` and report both. If learning buys progress
at the cost of plurality, that is an honest trade and an interesting one; discovering it in
review would be much worse.

**6. Preserve the CTI-independence boundary, in the exact form that survives scrutiny.**
An examiner will say learning tunes the weights to fit the substrate, which is what the
declared-value guardrails forbid. The answer, which should be written down before it is
needed: the **authored artefact is the learning rule, not the resulting weights**. The
corpus supplies the prior, learning is a declared likelihood update applied at runtime, and
`κ = 0` recovers the prior exactly. The weights that emerge during a run are a consequence
of the model's own behaviour, in the same category as the path the token takes — not an
authoring act. What *would* violate the boundary is choosing `κ` or `ρ` because they raise
compromise breadth, and the sweep is what proves that was not done.

**Alternatives considered.** *A full RL agent over the net* — rejected on timeframe and on
scope (the defender-side RL precedent in this lineage is Tay's, retained as a benchmark
never to extend). *Learning the tactic→verb mapping instead of the routing* — interesting,
because the mapping is the acknowledged coarse input, but it changes the controller into a
runtime-mutable object and breaks the versioned-mapping discipline S4 established. *Learning
over `(place, verb)` pairs rather than places* — nearly equivalent under the current
mappings, where several tactics share a verb, and strictly more parameters; revisit only if
the place-keyed version is shown to be too coarse. *Success counts without a prior* —
rejected: an unvisited place would have an undefined or zero estimate and the attacker
would never try it, which silently destroys the net's structure.

## Validation gate

Done when:

1. `κ = 0` reproduces the current record stream field for field, on all five profiles and
   several seeds, both MTD conditions. (The seam's null guarantee, re-checked with this
   modulator specifically attached.)
2. **The learning signal is measured, not assumed.** Within-run blocked fraction is
   reported for the first against the last quartile of events, at `κ = 0` and at the
   declared `κ`. A learner that does not reduce its own blocked fraction is not learning,
   whatever the routing does, and that verdict must be reported rather than explained away.
3. The `κ`/`ρ` contest is swept over declared bands, with per-conclusion held/moved verdicts
   in the shape the two prior sweeps established, and criteria committed **before** any
   output exists.
4. Path entropy is reported at `κ = 0` and at the declared `κ`, so the axis-3 trade is
   visible.
5. Determinism holds: the state is a deterministic function of the run's own history, so no
   new RNG stream should be needed at all; if one is, it derives by the established XOR
   pattern and stream isolation is tested.
6. A tracked record under `docs/implementation/pipeline/ogasp/` carrying the rule, the two
   parameters with tiers and bands, the CTI-independence argument, the within-run boundary,
   and the sweep verdict. A declared-value ledger entry alongside it.
7. The criterion's axis 7 is re-scored **only** if the pre-registered criterion was met —
   and note that DESIGNED is the honest badge for a mechanism that exists and has not been
   shown to change an outcome, exactly as axes 1 and 4 are held today.

## Hard constraints

- **`κ = 0` is bit-identical to today.** Everything about the ablation, the S2 argument and
  the sweep rests on it.
- **Within-run only.** No memory crosses a run.
- **No substrate change.** Do not uncomment the ATK-04 cross-instance vulnerability
  learning; it is a documented unimplemented divergence and touching it moves the baseline.
- **The values are declared, tiered and swept** — never chosen because they improve an
  outcome. The CTI-independence guardrail applies with full force here and the record must
  argue it, not assert it.
- **Do not let learning hide the H-coupling finding.** If the attacker learns its way around
  unmet preconditions, the blocked-fraction finding must still be reportable at `κ = 0` and
  the reduction must be reported as *the learner's* achievement, not as the problem having
  gone away.
- Determinism / SIM-05; envelope-not-actor phrasing; within-substrate comparability only.
- Australian English; branch and commit rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.

## Reading list

- `docs/implementation/apt_model_criterion.md` §(d) axis 7 and §(e) — the literature's
  framing, the M8b measurements, and the placement claim this axis alone can move.
- `docs/implementation/pipeline/ogasp/attacker_state_seam.md` — the mechanism this builds on
  (SHIPPED 2026-07-28): the `AttackerState` observation methods, the modulator Protocol and
  the `Π_m` composition, the fourth RNG stream, and the null-equivalence guarantee. Read it
  before designing the modulator.
- `docs/implementation/pipeline/ogasp/experiment_01_findings.md` §3 — the friction failure
  mode this is the candidate mitigation for, and the reason the driver refuses to re-impose
  native order.
- `docs/implementation/declared_value_provenance.md` §1, §5 — the three requirements a new
  declared family must meet, and the guardrails (especially no reverse-engineering from the
  layer being conditioned).
- `docs/implementation/pipeline/ogasp/weight_sensitivity_study.md` §4 — the sweep-reporting
  shape to copy, including committing the conclusions before any output exists.
- `docs/implementation/metrics_semantics.md` — the ATK-04 divergence row, so the
  commented-out substrate learning is understood as out of bounds rather than as an
  opportunity.

## Out of scope (explicitly)

- Cross-run or cross-campaign memory, and anything that reads the defender's behaviour —
  that is axis 8, ruled future work.
- Changing the tactic→verb mapping at runtime.
- Any substrate edit, including the commented-out vulnerability learning.
- Stealth and incentive modulators. They share the seam; they do not share this handoff.
- Building the measurement suite — this consumes it.
- Dissertation prose.
