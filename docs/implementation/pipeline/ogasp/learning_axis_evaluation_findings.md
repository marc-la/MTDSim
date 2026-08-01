---
status: durable
created: 2026-07-29
updated: 2026-08-01
topic: "Findings ledger from the axis-7 session, re-read under the thesis framing: what a learning-capable attacker exposed about the evaluation apparatus — chiefly that the substrate's success verdict, the atom every metric in this lineage is built on, is not a progress signal. Includes the design post-mortem on why a per-place scalar could not carry a workflow claim."
---

# What a learning-capable attacker exposed about the evaluation apparatus — findings preserved, under the thesis framing they should have been produced under

> **Relocated from `docs/handoffs/` on 2026-08-01, unchanged in substance.** It
> was filed as a handoff and is not one: it asks for no work and sets no
> validation gate, so it would never be shipped and deleted. By the placement
> criterion in [`../../../workflows/docs_map.md`](../../../workflows/docs_map.md)
> it is an investigation record. The body below is preserved as written.
>
> **Its forward-looking half is discharged.** §5's diagnosis — that a per-place
> scalar cannot represent a precondition constraint, because the quantity that
> would have to be learned is success *conditioned on the attacker's phase-state*
> — was taken up and built. The readiness generalisation ran, was swept, and is
> recorded in [`learning_readiness_prereg.md`](learning_readiness_prereg.md),
> [`learning_readiness_findings.md`](learning_readiness_findings.md) and
> [`learning_representation.md`](learning_representation.md). The verdict: the
> readiness key repairs the learner's self-inflicted damage and still does not
> beat not-learning, so **axis 7 holds at DESIGNED**. This record's reasoning was
> therefore validated and its recommendation executed; what remains is its value
> as history.
>
> **One decision remains open for Marc** — whether the shipped axis-7 records are
> re-framed in *property* rather than *performance* terms, and whether the badge
> is re-pre-registered under a property criterion (§ end of this file). It is
> pointed at from `docs/handoffs/README.md` so it stays visible now that this file
> no longer sits in that directory.

**This record deliberately does not follow the handoff template.** It asks for no
work and sets no validation gate. It exists because a session built a mechanism,
swept it, shipped it, and only afterwards arrived at the framing under which its
results are worth something — and the reasoning that got there is more valuable
than the mechanism, and would be expensive to reconstruct. Read it as a record
with options attached, not as a brief.

**There is a sibling record.** A concurrent session working criterion axis 6
produced [`fidelity_implications.md`](fidelity_implications.md) under the same
framing correction, carrying that axis's 1 800-run findings. The two are
complementary rather than overlapping — that one is the incentive/cost ledger,
this one is the learning ledger plus the design post-mortem — and they should be
read together, because two independent axes arriving at the same class of
conclusion about the measurement apparatus is stronger evidence than either
alone.

## The framing, which is the point

The thesis is: **what does greater attack fidelity imply for current evaluation
methods of MTD?**

Everything below is a statement about *evaluation methods*. The attacker is the
instrument, not the subject. This session spent most of its length reasoning as
though the attacker were the subject — asking whether learning made the attacker
better, whether it could be brought into line with the inherited baseline,
whether it beat anything — and every one of those questions is the wrong one.
Two framings were entertained and both are now rejected:

- **Empirical comparison against the inherited baseline.** The baseline is the
  procedural substrate the goldens rest on and the stand-in for the field's
  attacker models in the lit review's cross-section. What matters is that those
  models *cannot express* campaign structure, objective conditioning or
  learning, and this one can. That is a comparison of expressive capacity, and
  it is settled by demonstrating the representation and showing it is
  consequential within the model's own frame. It is never settled by
  outperforming anything.
- **Bringing the profiled attacker "in line with" the baseline.** This is
  calibrating the treatment arm to the control arm. If a CTI-derived attacker is
  engineered until it behaves like a scripted one, the difference the project
  exists to measure has been destroyed and the null result was manufactured.

The correct reading of every finding below is therefore *not* "the attacker did
or did not do well". It is "a more faithful attacker made the following property
of the evaluation apparatus visible, and a less faithful one could not have".

## What is on record in the repo

The mechanism shipped at `e9b5117`, was pre-registered at `876bca2` and reported
at `bca6220`, with the tracked record at
[`learning_capability.md`](learning_capability.md).
The attacker carries a within-run place-keyed Laplace belief over observed
verdicts, entering routing as `Q(b)^κ` and decaying by `ρ` on every MTD
interrupt. Six conclusions and a badge criterion were committed before any run
existed; 2 400 runs were swept over both declared bands on both controller
mappings; axis 7 moved NOT ADDRESSED → DESIGNED.

The seam gained a third wrapper (`StatefulAttackOperation`, hooking the single
`apply_mtd_interrupt_cost` every interrupt path funnels through) and a modulator
observation fan-out. The driver is still not edited.

Note for anyone reading the git log: this session's commits interleave with a
concurrent axis-6 session working the same tree, and three shared documents
carry both sessions' prose. The workspace hazard itself is recorded separately
at `22104f8`.

## The findings, restated as statements about evaluation methods

### 1. The substrate's success signal is not a progress signal, and only a faithful attacker reveals it

The binary success/failure verdict is the atom every metric in this lineage is
built on. It rewards reconnaissance heavily and exploitation rarely, because
scanning succeeds far more often than exploiting does. An attacker faithful
enough to *optimise* that signal therefore learns to stop attacking:
`EXPLOIT_VULN` fell from 13 % of the attacker's successes to 1 % as the learning
capability rose, and compromise breadth fell from 6.5 hosts to 0.8.

This is the session's most transferable result and it is a finding about the
measurement, not about learning. A scripted attacker never reveals it, because a
scripted attacker never optimises anything — it executes an order that was
authored to be correct, so the gap between "returned true" and "made progress"
never has to be crossed by anything. Give the attacker the capacity to respond to
the signal and the gap becomes measurable.

The generalisation worth carrying: **an evaluation that grants an attacker a
learning capability without giving it a progress-carrying reward will measure the
attacker optimising away from the objective.** That applies to anyone building
the learning attacker this literature keeps asking for, which is the point.

### 2. The coupling between an attacker's order and a simulator's order is invisible to the field's attacker models

Blocked fractions of 91–97 % exist only because the movement attacker walks CTI
tactic-order while the substrate enforces a precondition order. Every attacker in
the cross-section *is* the substrate's own order, by construction, so no
evaluation in the field can register this friction at all — there is nothing in
those models capable of being out of order.

The substrate makes the order explicit and machine-readable in
`AttackOperation.assert_action_context`: `SCAN_HOST` has no precondition;
`ENUM_HOST` needs a non-empty host stack; `SCAN_PORT`, `BRUTE_FORCE` and
`SCAN_NEIGHBOR` need `curr_host`; `EXPLOIT_VULN` needs `curr_host` and
`curr_ports`. That is exactly the chain a working attacker must satisfy, and it
is a property of *this simulator's action model*, surfaced as measurable friction
only because a differently-ordered attacker was pointed at it.

### 3. MTD's effect on attacker knowledge cannot be expressed by the current metric suite

Forgetting was severely effective: most of the learner's advantage was gone once
a quarter of the belief was lost per mutation, and at roughly 42 interrupts per
run even gentle decay compounds. No metric in the suite registers this, because
every one of them is defined on an attacker with no knowledge to lose.

So a faithful attacker creates a defence effect that the existing apparatus has
no vocabulary for. Alshamrani's claim that shuffling "renders the exploratory
knowledge of the attacker useless" is, on this evidence, unmeasurable by the
field's own instruments — which is a direct hit on the thesis question.

### 4. Fidelity dimensions trade against one another, and a per-axis rubric cannot see it

Path entropy fell at every capability step in **all ten** profile × mapping
cells. Learning and strategic plurality — criterion axes 7 and 3 — pull against
each other. Any claim on either has to name the capability it was measured at,
and a rubric that scores fidelity one axis at a time will report two
improvements where there is one trade. This is a finding about the criterion
instrument itself.

### 5. The badge criterion committed a category error, and that is also an evaluation finding

The pre-registered criterion was "DEMONSTRATED only if the attacker measurably
improves". That is a **performance test applied to a property axis**, and it does
not belong on this instrument — the criterion's own badge definitions are about
what can be claimed, and every other axis is scored on whether a mechanism
changes the model's behaviour, not on whether it makes the attacker win.

**The badge was not re-graded, deliberately.** Re-reading committed numbers
against a criterion invented after seeing them is exactly what pre-registration
exists to prevent. The recorded verdict stands under the criterion as written. If
the property framing is adopted, the correct response is a fresh pre-registration
under it, and the shipped sweep becomes what it honestly is: a well-executed test
of a question that was not the right one.

### 6. Convergence on the simulator's order is the finding, not the failure

If the terrain admits essentially one viable action ordering, every sufficiently
adaptive attacker discovers it, and the ordering stops being informative about
the attacker. What a CTI-derived structure then contributes is everything around
the path — tempo, which tactics are attempted and how often, where effort is
spent, and which points in the campaign are exposed when a mutation lands.

The corollary ties the axis to the thesis: if convergence is inevitable, the
interesting variable is the *rate* of convergence, and MTD's whole effect is a
tax on that rate. An attacker forced to rediscover its workflow after each
mutation is paying precisely the cost the MTD literature claims shuffling
imposes. That is a measurement no baseline is needed to interpret.

## The design post-mortem — reusable reasoning, not a proposal

Why the shipped mechanism could not have produced a workflow claim, recorded so
it is not re-derived:

- **The object cannot represent a workflow.** `Q(b)` is a per-place scalar; a
  workflow is a sequence. There is no expression of "`SCAN_HOST` then
  `ENUM_HOST` worked" in its state. Against the axis's own literature — Cho's
  attackers that "learn and can launch adaptive attacks", Jalowski's APT that
  "learns mutation patterns over time" — this is disqualifying. The handoff that
  commissioned it instructed that credit assignment be kept myopic and longer
  credit be rejected on timeframe grounds; that instruction was implemented
  faithfully rather than tested against what the axis is about, and that was the
  error.
- **A type mismatch, not a layering principle.** The routing weights are over
  *transitions* `a→b`; `Q(b)` is over *places*. Multiplying a place-shaped
  quantity into a transition-shaped layer can only express "avoid arriving at
  b", never "prefer the move a→b" — which is why the behaviour read as flight
  rather than as sequence learning. An earlier claim in this session that
  knowledge should not go into the routing weights was **wrong**: those weights
  are already a perturbation stack (CTI base × verdict overlay × declared
  lifecycle-distance term), and a learned term is the same kind of object as the
  distance term — a declared prior over plausible transitions beside an
  empirical posterior over productive ones, same shape, same composition.
- **The only available lever was avoidance.** With the tactic-to-verb mapping
  frozen, routing was the sole degree of freedom, and the only way to reduce
  friction by routing is to stop visiting the places whose verbs get refused.
- **Two signals were conflated.** `PRECONDITION_UNMET` and a genuine substrate
  `False` both reached the learner as `failure`, so it could not distinguish
  *wrong action* from *wrong time* — and on this substrate almost all of it is
  wrong time.
- **The forgetting rule had nothing worth destroying.** Wiping a per-place
  preference is not "rendering exploratory knowledge useless".

**What is sound and reusable:** the seam, the null-equivalence guarantee, the
declared-value scaffolding with its generator and reproduction check, the sweep
discipline, the observation fan-out, the interrupt wrapper, and the within-run
trend measure. None of that is specific to the modulator hung on it. The plumbing
is sound; the payload was wrong.

## Options if this is ever resumed — offered, not prescribed

Two problems live at two layers and were being conflated. *Which tactic next?*
lives in the routing weights, and workflow knowledge belongs there —
transition-shaped and chain-derived. *How is this tactic realised on this
substrate right now?* lives at dispatch, and precondition knowledge belongs
there.

For the first, the cheapest object that can represent a workflow is a **bounded
success-chain memory**: keep a queue of recent transitions, and when the token
successfully acts at one of *its own profile's* objective places, increment every
transition in the queue and clear it. One parameter rather than two, no discount
factor, no bootstrapping — it is counting which sequences preceded wins, which is
what an analyst would call tradecraft, and it is not the RL agent the project has
ruled out. The horizon is not a free magnitude: it is bounded by the longest
precondition chain in the action model, so on a different simulator it is read
off that simulator's own dependency depth.

Using the **profile's own declared objective** as the credit trigger keeps the
reward CTI-derived rather than modeller-chosen, which matters because rewarding
compromise breadth would mean optimising the attacker on the metric the
evaluation scores it with. It also makes different profiles learn different
workflows, which strengthens axis 2 rather than threatening it.

**One fact would decide viability cheaply and was not gathered:** how often each
profile successfully acts at its own objective places. If that is too rare to
fire within a run, the credit trigger cannot teach anything and the design is
dead before it is built. It is computable from the sweep data already on disk.

For the second layer, the substrate offers two stubs and **they are not
interchangeable**. The native succession policy is documented per verb (for
example `_do_scan_host`: *"Native succession: True → ENUM_HOST"*) and enacted by
wrappers the carve deliberately bypasses — piping that in imports the control
arm's script into the treatment arm and destroys the experiment. The precondition
contract (`assert_action_context`) is declarative and is about the world rather
than about policy; consulting it is the attacker knowing its own situation, which
is uncontroversial. Only the second is defensible.

An **oracle arm** consulting the precondition contract directly, with no learning
at all, would bound what any learning mechanism could achieve on this terrain and
would answer cheaply whether friction is even the binding constraint. It is a
measurement instrument, not a realism claim.

## The one thing a future session should fix rather than inherit

**The shipped prose is written under the superseded framing.**
`learning_capability.md` §7–8 and the criterion's axis-7 body report the result
in performance terms — "operates and does not help", breadth falling, the
attacker not being made better. Under the thesis framing at the top of this file
those passages *under-report* what was found: the verdict/progress gap is a
finding about the evaluation apparatus, and it is currently written as a
disappointment about the attacker.

This was **not** rewritten in-session, because changing how a shipped result
reads after the fact is a disposition, not a housekeeping task. Marc decides
whether the records are re-framed, and whether axis 7's badge is re-pre-registered
under a property criterion rather than a performance one.

## Hard constraints that survive any resumption

- **The within-run boundary.** No memory crosses a run. Cross-run memory is M8d
  and axis 8, both ruled future work.
- **The axis-7 / axis-8 line.** The attacker's own state — compromised hosts,
  known ports, exploited vulnerabilities — is legitimate axis-7 material and not
  a CTI deviation; an attacker that does not know its own situation is less
  realistic, not more. Anything reading the *defender's* behaviour, including
  `Adversary.observed_changes`, is axis 8 and out of scope for the life of the
  project.
- **No substrate change**, including the commented-out ATK-04 cross-instance
  vulnerability learning.
- **Null-equivalence.** Any modulator's zero configuration must stay bit-identical
  to a run without it; it is what makes each axis independently ablatable and it
  is what defuses the S2 confounding objection.
- **Declared values are never chosen to improve an outcome**, and a new
  credit-assignment rule is a new declared family needing its own
  pre-registration before any sweep scores it.
- Determinism / SIM-05; envelope-not-actor phrasing; within-substrate
  comparability only; Australian English; branch and commit rules from
  [`../../../workflows/session_workflow.md`](../../../workflows/session_workflow.md); never
  push.

## Reading list

- [`learning_capability.md`](learning_capability.md)
  — the shipped design, pre-registration and sweep verdict. Read §7.6 first: it
  is where the verdict/progress finding lives.
- [`attacker_state_seam.md`](attacker_state_seam.md)
  §10 — the third wrapper and the observation fan-out, which any successor
  mechanism inherits.
- `mtdnetwork/operation/attack_operation.py` — `assert_action_context` for the
  precondition contract, and the `_do_*` docstrings for the native succession
  policy that must **not** be consumed.
- [`../../apt_model_criterion.md`](../../apt_model_criterion.md)
  §(b) and axis 7 — the badge definitions the pre-registration should have been
  written against.
- [`../../declared_value_provenance.md`](../../declared_value_provenance.md)
  §6.2 — the ledger entry, including the three things this family added to the
  precedent.

## Out of scope (explicitly)

- Any empirical baseline-versus-movement performance comparison. That framing is
  rejected above and should not be reintroduced.
- Re-grading the shipped badge against a criterion written after the numbers
  existed.
- Cross-run memory, defender observation, and substrate edits.
- Dissertation prose.
