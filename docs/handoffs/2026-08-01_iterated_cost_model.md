---
status: open
created: 2026-08-01
---

# Repair the attacker's decision model so it can express instrumental value — a state-conditioned expected cost and an enabling-value benefit, both derived from artefacts that already exist

**Blocked on one disposition: Marc's, on whether the axis-6 decision model is
replaced at all.** This is a *mechanism* change to a built, frozen mechanism, so
no session may take it on its own authority. What follows is the design worked
out to the point where the ruling can be made on evidence rather than on
intuition — including the argument for doing nothing, which is not a straw man
(§7).

Governed by
[`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md).
The freeze's axis-6 disposition became **G + M** when this defect was recorded;
this handoff is the M half. The **S2 governance question is still separately
open** and gates wiring any non-zero λ into a reported experiment — clearing D-09
or S2 does not clear this, and clearing this does not clear those.

## 1. The defect, stated once

The current factor is `(u(b)/ū)^λ` with `u(b) = benefit(b) / cost(b)`, where cost
is the tactic's declared duration and benefit is its proximity to the profile's
own objective. Both terms penalise **instrumental** tactics, and in the same
direction, so the penalty compounds:

| | reconnaissance | credential-access |
|---|--:|--:|
| declared duration (cost) | 35.0 s | 4.5 s |
| benefit under `pure_steal` | 0.0625 | 0.25 |
| **utility** | **0.0018** | **0.0556** |

A 31-fold preference against the tactic that satisfies the precondition for the
tactic preferred. Benefit grades proximity to the objective, which scores an
enabling step as though unlocking a later one were worth nothing; cost grades
duration, which penalises the same step again for being slow. **The model has no
term in which "worth its price because of what it unlocks" could be written**, so
this is a defect of the model rather than a mis-setting of ρ, `cost_floor_s` or
λ — no sweep point repairs it. Full diagnosis:
[`../implementation/pipeline/ogasp/cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md)
§2.2a.

It is also, and this is the argument for acting on it, **the obvious first
choice made twice**. Pricing actions by their declared duration and valuing them
by proximity to the goal are what a careful modeller reaches for; that the two
compose into a systematic starvation of the enabling steps is not visible until
it is measured. That is what makes it worth a record rather than a quiet fix.

## 2. The design — two changes, each derived, neither adding a declared family

The governing constraint is the one the current model already honours and must
keep honouring: **no second catalogue, no new declared magnitude.** Both changes
below are computed from artefacts already on disk and already scrutinised.

### 2.1 Change A — cost becomes *expected* cost, conditioned on readiness

Replace the denominator with the cost of actually getting the tactic done from
where the attacker currently stands:

```
    cost*(b | s)  =  duration(b)  +  enabling_cost(verb(b), s)
```

**Read the relation's actual shape before writing this** — it is not a
tactic-prerequisite list, and a formula that sums "the durations of `b`'s
missing prerequisite tactics" cannot be written against it.
`data/ogasp/controller/precondition_relation.json` (v1_substrate) is a
**capability** model at *verb* level: three capabilities (`host_stack`,
`curr_host`, `curr_ports`), and each of the six substrate verbs declares what
it `requires`, `produces` and `clears`. `EXPLOIT_VULN` requires
`curr_host` + `curr_ports`; `SCAN_PORT` produces `curr_ports` but itself
requires `curr_host`; `ENUM_HOST` produces `curr_host`, requires `host_stack`,
and **clears `curr_ports`** — so the enabling chain has ordering effects and
cannot be costed by summing an unordered set.

`enabling_cost` is therefore a **shortest-path search over the capability
closure**: the cheapest ordered verb sequence taking the attacker's current
capability set to the one `verb(b)` requires, priced by mapping each verb back
to the cheapest tactic that dispatches it under the run's controller mapping,
and charging that tactic's declared duration. The search is trivial — three
boolean capabilities is an eight-state space — and it is a pure function of the
declared relation, the declared mapping and the declared catalogue. **Nothing
new is declared.**

The relation predicts the substrate's own block flag exactly on `v1_ckc_total`
(12 281/12 281) and at 92–94 % on `v2_partial`, the residual being a declared
optimism about empty scans
([`../implementation/pipeline/ogasp/learning_representation.md`](../implementation/pipeline/ogasp/learning_representation.md)).
That residual is inherited, not introduced: the cost term is as accurate as the
artefact, and the record must say so rather than implying the expected cost is
exact.

Four properties earn this form:

- **It prices the wall instead of walking into it.** An exploit-shaped tactic
  attempted unready costs 4.5 s *plus* the reconnaissance it needs, so its
  utility falls by roughly an order of magnitude exactly when it would have been
  blocked — and returns to 4.5 s once the prerequisite is met. The attacker stops
  preferring actions that cannot succeed, without being told they fail.
- **It responds to MTD in a way declared duration structurally cannot, and the
  artefact already says exactly how.** The relation's `mtd_clears` field
  declares that a **network**-layer mutation clears `curr_host` and
  `curr_ports`, while an **application**-layer mutation clears **nothing**. So
  after a network-layer mutation the enabling chain must be re-walked and
  `cost*` rises — by an amount set by which capabilities were destroyed, not by
  the interrupted tactic's dwell. That is precisely the non-proportional
  response the axis-6 M8b field names as a route to DEMONSTRATED, and **the C4
  negative and this defect therefore have one remedy** — the strongest single
  argument for the change.

  **It also makes a falsifiable prediction, which is worth pre-registering.**
  Because the response is confined to the network layer, the iterated model
  should show a cost-sensitivity effect under the position-destroying family
  (Complete Topology, IP Shuffle) and **little or none** under the diversity
  family (OS, Service) — which is the same mechanism split the project's
  headline ranking-inversion result turns on
  ([`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  §9). A model that responded uniformly across the two families would be
  suspicious rather than reassuring, and U3 should be reported per mechanism
  family for that reason.
- **It is stateful but not learned.** `cost*` reads the attacker's own
  trajectory against a declared relation; it estimates nothing and updates
  nothing. The seam already carries per-decision state
  ([`../implementation/pipeline/ogasp/attacker_state_seam.md`](../implementation/pipeline/ogasp/attacker_state_seam.md)),
  and no substrate state is read, so the axis-8 scheme-awareness exclusion is
  untouched.
- **λ = 0 stays exactly bit-identical.** The factor is still raised to λ; only
  the denominator's value changes. The IEEE identity the ablation rests on is
  unaffected, and must be re-asserted rather than assumed.

**Its cost:** the modulator stops being a pure function of declared data and the
current place, so the precomputable-factor-table property (F6 of the fidelity
ledger, proven 30/30 bit-identical by the collapse spike) is **deliberately
given up**. That property is what F6 uses to argue the mechanism is "structurally
a third static overlay"; a session shipping this must say plainly that F6's
verdict applies to the superseded model, because giving up the property is the
point — a factor that cannot see attacker state cannot see MTD either.

### 2.2 Change B — benefit becomes enabling value

Replace the numerator's stage-gap term with distance measured **through the
profile's own net** rather than through the lifecycle-stage ordering:

```
    benefit*(b | P)  =  ρ^(1 + hops(b → nearest objective of P, in P's net))
```

`ρ` is the existing declared decay, unchanged and already swept; `hops` is the
shortest path in the routing net the profile already carries. Reconnaissance
that genuinely leads to the objective now scores as near to it; reconnaissance
in a profile where it leads nowhere still does not. **Nothing new is declared**
— the change is *which graph the distance is measured in*.

Two hazards to discharge before this ships, both regression-guardable, and the
first is the serious one:

- **It must not become a restatement of the base weights.** The base transition
  weights are corpus flow *proportions* — how often analysts drew this move —
  and `hops` is a distance to the objective, which is a different quantity over
  the same graph. The separation is real but thinner than the current rule's,
  because both now read the net. The existing §4.1 test (benefit is
  source-independent and profile-varying; the overlay's kernel is neither) still
  passes, but a session must add a third assertion: **benefit* must not be
  monotone in the base out-weight**, checked over all 75 cells, or the term is
  laundering frequency as value.
- **Unreachable objectives.** A tactic with no path to any objective in its
  profile's net has undefined `hops`. Define it as the current stage-gap value
  rather than zero — a zero would be a `may_zero` modulator under the seam's
  stall rule and would need the no-stall check re-run.

### 2.3 The ranked alternatives, and why these two

The house discipline is to rank candidates coarsest to finest and take the
smallest that captures the dependency exactly (the precedent is
`learning_representation.md`). Applied here:

| # | Candidate | Verdict |
|---|---|---|
| 1 | **Do nothing; document the defect** | The floor option, and it is what has shipped today. Costs nothing, and leaves a decision model whose one measured outcome is uninterpretable. |
| 2 | **Change A alone** (expected cost) | The **recommended minimum**. Repairs the wall and opens the MTD channel; leaves benefit unable to credit enabling steps, so recon is still under-valued in absolute terms — but it no longer competes against an *unready* exploit that looks eight times cheaper than it is. |
| 3 | **Change B alone** (enabling benefit) | Repairs the numerator's blindness but leaves cost pricing a blocked attempt as though it succeeded. Does nothing for C4. Weaker than 2 on every axis. |
| 4 | **A + B** | The complete repair, and the one to run if the ruling is for a full replacement. Two changes at once means the sweep cannot attribute an effect to either, so it must be run as **three arms** (A, B, A+B) against the current model, or the attribution is lost. |
| 5 | **Cost from *realised* success rate** (the M8b field's literal wording) | **Rejected as primary.** It is an estimate from experience, which is the axis-7 learner's territory; building it here would duplicate that mechanism inside a modulator that is supposed to be declared, and the two would double-count when composed. Change A gets the same non-proportional MTD response from a *declared* relation instead. |
| 6 | **A value function over the net** | **Rejected on the standing no-RL constraint** — no eligibility trace, no discount factor, no value function. `ρ^hops` is a static shortest-path kernel over a declared graph, which is inside the line; a Bellman backup over observed outcomes is not, and a reviewer will ask, so the record must draw the distinction explicitly. |

**Recommendation: rule on 2 or 4, not on 5.** If the ruling is 4, run it as
three arms.

## 3. The composition hazard, which is the biggest risk in this brief

Change A conditions on readiness. **The axis-7 learner also conditions on
readiness** — it is keyed on `(destination tactic, precondition-satisfied?)`
against the same artefact. Composing both would apply the same signal twice
through two factors, which is exactly the hidden double-count the composition
register exists to catch
([`../implementation/pipeline/ogasp/modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)).

Three consequences, all mandatory:

1. **Register change A as a new factor** in that register, with its seam and its
   reported-configuration status, in the commit that builds it.
2. **No arm runs both** the readiness-conditioned cost and the readiness learner
   until a joint check has run — and note that the existing joint check
   (`learning_readiness_findings.md` §6) measured the *declared-duration*
   utility modulator against the learner and found the two pull in **opposite**
   directions. That finding does not transfer: change A makes the utility
   modulator agree with the learner rather than oppose it, so sub-additivity is
   not to be assumed and the check must be re-run.
3. **The freeze's reported-configuration pin is unaffected** — the headline arm
   still runs modulators null, and axis 3's plurality badge still belongs to
   that arm.

## 4. Pre-registered conclusions — commit these in their own commit, before any output

The house discipline, non-negotiable here because the change is motivated by a
defect and there is an obvious temptation to show the repair working. Every
aggregate goes through `interval_report`; `ordering_supported` is the gate.

| | Conclusion | Criterion |
|---|---|---|
| **U1** | The ablation is still exact | at λ = 0 the record stream is field-for-field identical to a run with no modulator, across profiles × seeds × mappings × MTD conditions; zero differing runs. **A hard constraint, not a finding** |
| **U2** | The repair reaches the wall | blocked fraction at the declared λ is **lower** under the iterated model than under the current one, with disjoint 95 % intervals, on ≥ 3 of 5 profiles. This is the defect's own signature and the minimum the change must show |
| **U3** | **The payoff — MTD's measured effect now changes with cost-sensitivity** | the action-mix JSD between λ = 0 and λ = 1 is larger under MTD than without it, on ≥ 3 of 5 profiles — C4's criterion verbatim, so the verdicts are comparable. If U3 holds, axis 6's DEMONSTRATED condition is met by mechanism rather than by operating point |
| **U3b** | The response is layer-specific, as the mechanism predicts | U3's quantity is **larger under the position-destroying family than under the diversity family**, on ≥ 3 of 5 profiles. `mtd_clears` says the cost term can only see network-layer mutations, so a uniform response across families would mean the effect is not coming from the mechanism claimed. Reported whichever way it falls |
| **U4** | **Committed in the direction that would embarrass it** — the repair is not bought with plurality | pooled path entropy at the declared λ under the iterated model is **not lower** than under the current one. A repair that buys progress by collapsing traversal further has traded against axis 3 and must say so |
| **U5** | **Committed in the direction that would embarrass it** — the attacker is not simply better | distinct hosts at the declared λ are reported against **both** the current model and the λ = 0 arm. A rise over λ = 0 is *not* required and must not be sought: the honest outcome may be that the repaired attacker is merely less self-defeating, and C5's original spirit — no performance gain the mechanism is not entitled to — carries over unchanged |

**If U2 moves, stop and report.** A repair that does not reach the defect it was
built for is a finding about the diagnosis, not a licence to re-specify until it
lands — the same rule the disengagement brief puts on its own C2.

## 5. Validation gates

1. **Exactness.** U1 above, as a test rather than a run: the λ = 0 identity
   asserted over the full configuration grid, as the current model's is.
2. **No new declared value.** A test asserting the iterated model reads only
   `tactic_durations.json`, `precondition_relation.json`, the profile nets and
   the existing `ρ` / `cost_floor_s` / `λ`. If a new magnitude appears, it needs
   a tier, a band, a sweep and a ledger entry — and the brief's central claim
   that this is derived rather than declared has failed.
3. **Determinism (SIM-05).** The factor draws from no stream; a conditioned run
   reproduces exactly, re-verified because the modulator is now stateful.
4. **The laundering check.** §2.2's monotonicity assertion over all 75 cells.
5. **Reader gates unchanged.** The full `tests/l3_simulation` suite and the
   substrate/carve/golden suites pass; no golden moves (this is a movement-layer
   modulator, and the substrate is untouched).

## 6. Build order

1. **Get the disposition.** Which option in §2.3, and whether λ ≠ 0 may be
   reported (S2). Nothing below is licensed without both.
2. Re-read §2.2a of `cost_model_plain.md` and §6.2's banner in
   `incentive_rationality.md` — the defect as recorded, so the build is not
   re-derived from this brief alone.
3. Build change A (and/or B) in `movement/utility.py` beside the current model,
   **selectable by version**, not replacing it — the current model must stay
   runnable, because every recorded figure in the project was produced by it and
   the comparison arms need it.
4. Gates 1, 2 and 4 before any experiment.
5. Commit §4's conclusions **in their own commit**.
6. Sweep: λ over its declared band × the arms §2.3 requires × 5 profiles × both
   MTD conditions × 10 seeds, on the current substrate. Check substrate
   freshness first (`6181305`, `816b300` moved the axis-6 rows once already).
7. Analyse with computed held/moved verdicts, never asserted.
8. Write the record as
   `docs/implementation/pipeline/ogasp/iterated_cost_model.md`; update the
   axis-6 badge only if U3 holds; log the R3 round in `attacker_utility.json`;
   register the new factor in `modulator_composition.md`; amend F6 of
   `fidelity_implications.md` (§2.1's given-up property); delete this handoff in
   the commit that ships the work and prune its line from `handoffs/README.md`.

## 7. The case for ruling "no", stated fairly

It deserves to be made properly, because the ruling is genuinely open.

- **The honours timeframe is the real constraint.** This is a mechanism build
  plus a pre-registered sweep plus a record — comparable in size to the axis-7
  readiness work, which consumed a full session and 4 600 runs.
- **The current record is already defensible with the defect documented.** A
  measured negative with a stated limitation is a legitimate result; the
  dissertation can report the mechanism, the C5 measurement, and the reason its
  attribution is uncertain, and that is honest scholarship rather than a gap.
- **The defect is itself a finding**, and arguably a more transferable one than
  the repair would be: *an evaluation that gives its attacker a cost model
  without asking whether that model can express instrumental value will measure
  the attacker defeating itself*. That warning is worth more to a reader than a
  fixed model, and it is already banked (F5, amended).
- **Against all three:** the repair is the same build that would move axis 6 to
  DEMONSTRATED, which no other available work does. That is the one
  consideration that might outweigh the timeframe, and it is the reason this
  brief exists rather than a note.

## 8. Out of scope

- **Any change to the duration catalogue or to `ρ`, `cost_floor_s`, `λ`.** The
  values stay; what changes is what they are applied to.
- **A realised-success cost estimated from experience** (§2.3 candidate 5) —
  that is the axis-7 credit-signal problem and stays with it.
- **Reinforcement learning of any kind.** No value function, no discount factor,
  no eligibility trace.
- **Substrate changes.** The precondition relation is consulted as a declared
  artefact; no substrate state is read.
- **Re-running any recorded experiment** under the iterated model. The frontier,
  experiment 2 and the axis sweeps stand as records of the model they ran under.
- Dissertation prose.

## 9. Reading list

- [`../implementation/pipeline/ogasp/cost_model_plain.md`](../implementation/pipeline/ogasp/cost_model_plain.md)
  §1 (what is computed today), §2.2a (**the defect**), §2.2b (the grounds the
  current model rests on).
- [`../implementation/pipeline/ogasp/incentive_rationality.md`](../implementation/pipeline/ogasp/incentive_rationality.md)
  §2–§4 (the mechanism and the two declared families), §6.2's banner (C5's
  qualified reading), §6.3 (why C4 moved — the other half this repair serves).
- [`../implementation/pipeline/ogasp/learning_representation.md`](../implementation/pipeline/ogasp/learning_representation.md)
  — the precondition relation change A consumes, and the ranking discipline §2.3
  follows.
- [`../implementation/pipeline/ogasp/modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)
  — the register the new factor joins, and §3's double-count hazard.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  axis 6 — the badge, and the M8b field this build's U3 targets.

## 10. Hard constraints

- **The disposition gates everything.** No build before Marc rules.
- **λ = 0 stays a bit-identical off-switch.**
- **No second cost catalogue, and no new declared magnitude** — if one appears,
  the design has failed its own premise (gate 2).
- **No declared value chosen because it improves an outcome**, and no
  re-specification after a moved U2.
- **The current model stays runnable** — every recorded figure depends on it.
- **No arm composes readiness-conditioned cost with the readiness learner**
  until the joint check re-runs (§3).
- Determinism (SIM-05); envelope-not-actor; within-substrate comparability only;
  Australian English; branch per session; never push.
