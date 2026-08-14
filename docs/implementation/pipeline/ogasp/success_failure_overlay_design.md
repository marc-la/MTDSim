---
status: durable
created: 2026-07-21
updated: 2026-07-28
topic: "L3 M2 — the outcome (policy) overlay: a ground-up conditional-likelihood weighting over the whole directed tactic-pair set, composed multiplicatively with the base weights and the substrate's binary verdict at runtime"
---

# The outcome (policy) overlay — a ground-up success/failure conditional-likelihood weighting over the whole tactic-pair set

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

**Status:** durable. The design record that turns the **M2** ruling ("binary
outcome selects between conditional weight treatments";
[`supervisor_decision_register.md`](supervisor_decision_register.md) §M2) into an
implementable contract, in the form Marc directed on 2026-07-21. The direction the
token takes after an action is carried by a **declared policy overlay**: a
**ground-up conditional-likelihood weighting of the whole directed tactic-pair
set**. For every directed pair `a → b` and each verdict `v ∈ {success, failure}`,
the overlay declares a value in `[0, 1]` answering, *per pair*:

> given the attacker's action at tactic `a` came back `v`, how likely is `b` as the
> next move — **0 = will not happen, 1 = the most likely next course of action**.

At runtime these values **manipulate the existing base edges**: the value multiplies
the D3 base weight and the source place's out-set is renormalised, so the observed
structure is tilted live by the success/failure signal the substrate returns.

This record is the design; **no stepping or net-build code is written here.** Both
consumers have since been built (commit `48471b8`): the composition lives in the
controller sublayer (`src/mtdsim/l3_simulation/controller/outcome.py`) and the live
net walk in the movement-layer attacker
(`src/mtdsim/l3_simulation/movement/attacker.py`); their handoffs shipped and were
deleted per the handoff lifecycle.
Its deliverables are this record, the authored overlay
[`../../../../data/ogasp/petri/outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json),
and its provenance row ([`../../provenance.md`](../../provenance.md)).

**What this is, and is not.** It is **structure = the net's legal-move grammar**
(the D3 nets + the synthetic overlay); **policy = which enabled move fires on which
verdict** (*this overlay*); **execution = one seeded walk**
([`../../../notes/ch4_methods/structure_to_behaviour_binding.md`](../../../notes/ch4_methods/structure_to_behaviour_binding.md)).
It is a **declared knowledge layer, not reverse-engineered weights** — real-world
conditional-likelihood knowledge distilled into a file, not weights solved from the
nets to make the token move a certain way. **Envelope, not actor:** it encodes
*plausible* next-move likelihoods, never a real adversary's policy. It **conditions**
the D3 base weights and never re-derives or re-tunes them
([`../../metrics_semantics.md`](../../metrics_semantics.md) §(f)); the per-tactic
binary verdict it keys on is fixed by [`controller.md`](controller.md)
§4 (the per-verb M2/M4 oracle) and read, never re-rolled. It is a **second, distinct** layer
from the *structural* synthetic overlay
([`synthetic_overlay.md`](synthetic_overlay.md)): that one adds edges, this one
weights them by verdict.

---

## 1. The composition rule (M2)

At a source place `a` whose action returned verdict `v`, the overlay conditions the
base out-distribution multiplicatively and renormalises within the source's out-set:

```
                      base(a→b) · overlay_v(a→b)
    w'_v(a→b)  =  ────────────────────────────────────      v ∈ {success, failure}
                   Σ_b'  base(a→b') · overlay_v(a→b')
```

- **Multiply-then-renormalise conditions without re-deriving.** It preserves the
  grounded base proportions *within* any set of edges the overlay treats alike, and
  never invents a fresh magnitude. The overlay changes *which edges carry the mass
  and how it redistributes across the verdict* — not the corpus's within-class
  ordering.
- **`overlay_v = 0` removes an edge under verdict `v`; `(0,1)` down-weights it.** The
  base weight `base(a→b)` is the D3 out-edge-normalised flow proportion (the
  `operator_dedup` variant is primary, `raw` the robustness arm — the overlay is
  variant-agnostic). Synthetic-overlay edges (the pre-intrusion chain and the
  backward regression bridge) are ordinary structure to the composition — they carry
  overlay values like any other pair (the backward bridge `initial-access →
  reconnaissance` is exactly the edge the failure treatment amplifies in the island
  profiles).

**Alternatives named and killed.** *Substitute weight-sets* (two independent
hand-authored out-distributions per place) — rejected: discards the D3 grounding and
is unbounded-parameter. *Additive bias* (`base + overlay`) — rejected: can invert the
grounded ordering and needs an arbitrary clamp; multiplicative conditioning respects
"conditions, never re-derives". *Solving the nets* for weights that move the token
"correctly" — rejected on principle: that is reverse-engineering, not declared
knowledge.

---

## 2. The value semantics and the ground-up authoring model

Each pair's two values are reasoned **from the tactic-pair's semantics — not a coarse
band bucket** — via three named factors, so the value varies pair by pair within any
band. The model is machine-readable in the artefact (`model` block); this is its
rationale.

### 2.1 The three factors

1. **Kill-chain relationship** — the coarse structural prior. Each tactic carries a
   band (0 prep, 1 intrusion, 2 consolidate, 3 expand, 4 objective); `relationship =
   forward / lateral / backward` by band distance. ATT&CK imposes no ordering — the
   band is a declared assumption (M3), used only as a prior a per-pair rule refines.
2. **Capability enablement** (`enables`) — does a **success** at `a` confer the
   capability or position `b` needs next? Each tactic has an `enables` set drawn from
   MITRE tactic semantics and the get-in/spread patterns the DFIR/Sophos incident
   AARs document (e.g. a landed foothold *enables* discovery, credential access,
   execution, escalation — so those are the strong next moves, not a return to
   external recon).
3. **Foothold dependency** — does `b`'s action require an established network
   position? Reconnaissance, resource-development and initial-access do not
   (pre-foothold); every post-intrusion tactic does. Used on the **failure** side: a
   move that needs a foothold the failure just denied is implausible next.

### 2.2 The success treatment — "given success at `a`, how likely is `b` next"

- `b` specifically **enabled** by `a`'s success → **1.0** (the modal next move).
- else **forward** (kill-chain progress) → **0.6**; **lateral** (same-phase sibling)
  → **0.5**; **backward** → **0.25**, and **0.1** if regressing to a *pre-intrusion*
  tactic (you do not re-recon after succeeding deeper).

Success leans on the grounded structure: the base weights already encode
success-biased observed workflow, and the `enables` boost sharpens the specific
next-steps the AARs attest.

### 2.3 The failure treatment — "given failure at `a`, how likely is `b` next"

The R2 rules (finalised). Each constant is set from **declared semantics**; the base
only ever **diagnosed** an incoherence — the routed percentages below are *validation
outputs*, never fitting targets (the CTI-independence boundary turns on this, so read
each change as **diagnosis → semantic re-reading → validation**).

- **Gates (dependency).** If `a = initial-access` failed, every **foothold-dependent**
  `b` → **0.02** — a declared ~45:1 *soft-floor*, not a hard 0 (no foothold, so a
  post-intrusion move is out of reach). This lets the fall-back bridge
  (`initial-access → reconnaissance` = 0.9, the synthetic regression bridge) dominate:
  validated on the composed nets at **83%** of IA-failure mass on the sparse profiles,
  up from a 50% tie under the superseded 0.1. If `a = reconnaissance` failed ("nothing
  found"), a deep post-intrusion `b` → **0.05** and `initial-access` → **0.4** — keep
  preparing.
- **Dampers.** A post-intrusion source regressing **backward to a pre-foothold**
  destination → **0.25** (a full-phase collapse is a minor, not modal, regress; this
  deliberately **exempts** the `initial-access → reconnaissance` = 0.9 bridge, whose
  source is itself pre-foothold). A **backward → execution** move → **0.35** (decoupled
  from `enables`): re-running code against a *held* foothold is a forward-level
  continuation, not a penalised 0.9 regress — this roughly halves the execution-regress
  mass the flat 0.9 over-amplified, and its ordering above the pre-foothold damper
  (0.35 > 0.25) is the deliberate "re-run code beats abandon the foothold" choice.
- **else by relationship: backward** → **0.9** ("back to the drawing board"); **lateral**
  → **0.7** (a same-phase sibling, an alternative route to the objective); **forward**
  → **0.35** (the *default* retry-then-advance; **0.30** only when the source is a
  pre-foothold stage). Forward on failure is soft-suppressed, **not banned**.

### 2.4 Worked examples (per-pair, not band-uniform)

| Pair | rel. | success | failure | reading |
|---|---|--:|--:|---|
| initial-access → discovery | forward | **1.0** | **0.02** | foothold enables discovery; on failure there is no foothold to discover from (soft-floor) |
| initial-access → reconnaissance | backward | **0.1** | **0.9** | do not re-recon after getting in; on failure, fall back to recon (the regression bridge — exempt from the damper) |
| initial-access → lateral-movement | forward | 0.6 | 0.02 | forward but not directly enabled (discover first); foothold-gated on failure |
| command-and-control → execution | backward | **1.0** | 0.35 | C2 enables re-execution; on failure, re-run code on the held foothold (execution damper, not a 0.9 regress) |
| lateral-movement → credential-access | backward | **1.0** | 0.9 | a hop enables credential re-harvest; on failure fall back to the survivor credential path |
| reconnaissance → initial-access | forward | **1.0** | 0.4 | recon enables entry; recon failure weakens (not bans) breaking in |

The values differ *within* the same relationship class (both `initial-access →
discovery` and `initial-access → lateral-movement` are forward, yet 1.0 vs 0.6),
which is the point: the value is the pair's conditional likelihood, reasoned from its
semantics, not its band.

### 2.5 Finalisation, scrutiny, and honest caveats

**R2 finalised 2026-07-23** (Marc greenlit) after **four adversarial cross-examination
rounds (~90 agents)**: an initial cross-exam, a branching red-team, a composed-net
validation on `build_all_profiles(with_synthetic_overlay=True)`, and a **stepwise
simulation** that walked a token through the real Petri nets with the **MTDSim verdict
stubbed** at the action layer, from many start points and competence levels. The final
finetune synthesis proposed **zero value changes** — the numbers converged. Certified
confidence **82%** (panel 82/82/82/84/88); the panel is unanimous that the 82→95%
remainder is the **dissertation defence / write-up of this reasoning**, not value
uncertainty. Decisions ratified: the **C2-hub** `enables` edit is **kept** (with the
inclusion principle in the ledger); the **`enabled = 1.0` tier stays flat** — a graded
"structural 1.0 / plausible-pivot 0.8" scheme was found empirically counterproductive.

Honest caveats an examiner will (rightly) press, recorded rather than hidden:

- **Failure > success to some band-4 objectives.** For a few non-`enabled` objective-band
  destinations, the failure branch routes slightly *more* mass than success — a systemic
  consequence of the flat backward/lateral ladder, not a per-pair defect.
- **`ia_gate` is a soft-floor, not zero.** At 0.02 it leaves a base-proportional residual
  (e.g. `initial-access|failure → execution` ≈ 0.13 aggregate) — intended (~45:1), not a leak.
- **C2-hub `privilege-escalation` arm is base-inert in 3/5 profiles** — the observed C2-hub
  pull is carried mainly by the credential-access / persistence arms.
- **Point masses are non-conditionable.** Sparse-profile single-out-edge sources (e.g.
  `infrastructure_setup: privilege-escalation → execution = 1.0`) renormalise to 1.0 for
  *any* overlay value — a base/corpus property, not an overlay one.
- **Objective sets are per-profile.** `infrastructure_setup` contains no exfiltration/impact
  node, so objective-reachability must be scored per profile (or that profile excluded).
- **The inherent ceiling.** This is a *declared-plausibility* envelope: the specific
  magnitudes are CTI-unvalidated by construction (only within-source ratios are claimed).
  Even with a flawless record an examiner can ask "why this magnitude" — the honest answer
  is the reasoning + the scrutiny it survived, which is what the ledger records.

### 2.6 What S1 changes — an initial trial of static weights, now due external grounding

The supervisor's post-experiment-1 ruling (**S1**, 2026-07-21;
[`supervisor_decision_register.md`](supervisor_decision_register.md)) reframes
everything above without retracting it. R2 is the landed value set and the
experiment-1 arm, and its internal coherence is not in dispute — but it is now on
record as **an initial trial of static weights**, with two directions attached.

**The named defect: large jumps in tactics.** The R2 rules resolve a pair by
*relationship* (forward / lateral / backward from the band prior) and by
`enables`, and neither term is sensitive to **how far** a jump travels.
`reconnaissance → impact` and `reconnaissance → initial-access` are both
"forward", so a jump across the whole lifecycle carries mass comparable to a jump
to the adjacent phase. That is the unrealism the supervisor flagged. The
direction is a **literature-grounded dependency** on lifecycle distance: close
jumps weighted higher, far jumps weighted close to — or exactly — **zero**.

**Where the grounding comes from.** Not from this project's judgement, and not
from the corpus: from **overlaying published APT lifecycle models and taking
their consensus** before any of it reaches the weights. The Cyber Kill Chain is
the primary overlay (seven sequential phases that the ATT&CK tactics already map
onto — the same crosswalk §2.1's band prior uses, but consumed as an *ordering
metric* rather than a coarse band), Alshamrani 2019's five-phase APT lifecycle is
the second, and other published lifecycles are candidates for the same treatment.
The consensus is the artefact; the weights consume it.

**What does not change.** The composition rule (§1) is untouched — a distance
term enters as a factor in the *value*, not as a new runtime mechanism. The
CTI-independence boundary holds: the distance model is declared from literature
and must not be fitted so that any particular profile's net traverses well. The
evidence-tier asymmetry (§4) survives, and the failure side remains the weaker
tier.

**And a sensitivity study is now required, not optional.** The values were
certified at 82% on the strength of their reasoning; S1 asks a different
question — *does the conclusion depend on where in its range each value sits?*
That is a sweep, and it is the discipline the evaluation's burden-of-proof note
already demands of every declared parameter family. Dynamic weights conditioned
on attacker state are named as the eventual direction and stay deferred.

The consensus artefact **landed 2026-07-27**:
[`lifecycle_consensus.md`](lifecycle_consensus.md) (the overlay, the four-stage
consensus, and the declared distance kernel) with its machine-readable model
[`../../../../data/ogasp/controller/lifecycle_consensus.json`](../../../../data/ogasp/controller/lifecycle_consensus.json).
Its verdict on §2.1's band prior: bands 0/1 and the objective band survive as
sourced; the consolidate≺expand split and C2's band-4 seat do not (weakly
ordered middle instead).

### 2.7 S1 executed — the fold-in and the sweep (2026-07-28)

Both halves of S1 have now landed, and the record is
[`weight_sensitivity_study.md`](weight_sensitivity_study.md). What it changes
about everything above:

**The value model gains one term and re-sources another.** No rule value in §2.2
or §2.3 changed. A **distance kernel** now multiplies each rule's value —
geometric decay per consensus stage crossed, `γ = 0.25` forward, `δ = 0.5`
backward, floored at `z = 0.1` — and the `relationship` term of §2.1 is read from
the consensus stages rather than from the five-band prior. That second decision is
the one §5 of the consensus record left open; it was taken so a value's two
ordering-dependent terms cannot disagree about direction (they would on 40 of the
210 pairs), and its cost — the post-intrusion middle flattening into one lateral
class — is stated in the study §1.1 and in the rules artefact. §2.1's bands
survive as the `v1_band_relationship` version's ordering and as the provenance of
the values experiment 1 ran on.

**The compiled views are now versioned.** `success.json` / `failure.json` moved
into `data/ogasp/controller/overlays/<version>/`, a registry in the same shape as
the controller mapping registry, because experiment 1 ran on the pre-distance
values and overwriting them in place would have made a published arm
unreproducible. Both versions compile from this one rule set via a tracked
generator whose `--check` re-derives every committed cell (0 of 420 per version).
The registry default stays at experiment 1's version.

**The caveats of §2.5 have been re-examined**, and the results are not uniform:
the failure-over-success inversion is **confirmed with its cause re-diagnosed**
(the flat enablement tier, not the backward/lateral ladder); the `ia_gate`
residual is **confirmed and slightly worse** in one profile, because multiplying a
gate by distance lets renormalisation hand more mass to the near gated
destination; the flat enablement tier is **replaced** by a positive finding (no
enabled pair crosses two stages, so there is no distance for a graded tier to
see); the point masses and per-profile objective sets are unchanged. Study §3
carries the table.

**And the values now carry a sensitivity verdict, which is mixed.** Two of the
four tested conclusions hold across the whole sweep (ASR zero everywhere; MTD does
not change the verdict) and two move (the *intermediate* profile's failure-mode
classification, and any ordering of profiles by how far they get — the latter for
a reason the weights do not control). Two things the sweep exposed independently:
the floor `z` is **behaviourally inert on this corpus**, because no profile net
carries a three-stage transition at all — which also means the pair that motivated
S1, `reconnaissance → impact`, was a defect in the declared table that never
routed any mass. Study §5–§6.

---

## 3. Whole-space coverage, extensibility, and runtime consumption

**The overlay weights the COMPLETE directed tactic-pair set** — all **210** ordered
pairs (15×14, no self-loops), not only the corpus-present subset. It is **corpus-
agnostic**: a different CTI/corpus that introduces an edge the current union lacks is
already weighted. *Which* pairs route mass is a property of the base/net layer
(base = 0 ⇒ no routing), never of the overlay — so completeness costs nothing at
runtime. (Reconcile flag **resolved**: under the 2026-07-22 controller reframe **every**
tactic dispatches a verb and so carries a verdict — [`controller.md`](controller.md)
§4 — so the whole space is consumed, not just six places; the self-loop "retry the same
tactic" is handled by the stepping layer's bounded-retry, not the overlay.)

**Notation (finalised).** The values are **rule-generated** from a small model, not
enumerated per pair: the canonical artefact is the rule-based
[`../../../../data/ogasp/controller/outcome_rules.json`](../../../../data/ogasp/controller/outcome_rules.json)
(the model + 5 success and 9 failure rules, **one rationale each**, was 246 duplicated
per-pair rationale fields), compiled to the complete 210-pair views `success.json` /
`failure.json`. A deterministic generator reproduces the table **0/123** before any
edit — the values follow the rules, not post-hoc fitting. This file
(`outcome_overlay.json`) is the corpus-scoped 123-pair view of the same rules. The
per-value provenance + scrutiny ledger is
[`../../declared_value_provenance.md`](../../declared_value_provenance.md).

**Runtime consumption tracks verdict availability.** The composition rule fires at a
place only when its action returns a success/failure verdict. A place with no mapped
verb produces no verdict, so it is **not** conditioned and routes on the base weights
— but its overlay values already exist, waiting for the verb. Authoring is
whole-space; consumption grows with the action vocabulary. (This is the reconciliation
of "weight the whole set" with "conditioned by the substrate signal": the values are
universal, the *conditioning event* is per-action.)

---

## 4. The evidence-tier asymmetry

The two treatments sit at **different evidential tiers**, by construction, and the
record says so. **Success** is the more grounded side: the `enables` relations come
from MITRE tactic semantics and the get-in/spread sequences the DFIR/Sophos AARs
([`../../../sources/tactic_profiles/step_c/`](../../../sources/tactic_profiles/step_c/))
document richly — reports say what worked, in what order. **Failure** is declared
judgement: an incident report almost never records what an attacker did when a step
*failed* and it "went back to the drawing board", so the failure treatment is reasoned
from kill-chain and foothold-dependency logic, not attested. This gap is itself a
methodological finding, not a hole to apologise for; the dissertation reports it as
one and the artefact flags it (`evidence_tiers`).

---

## 5. Relationship to the substrate reset model and the MTD interrupt

Two mechanisms move the token on failure, at **different layers**; the build keeps
them coherent. (a) **The substrate's own reset** — a `network`/`application` mutation
throws substrate state (`host_stack`, `curr_ports`) back mechanically, regardless of
the overlay (map §4 interrupt column;
[`action_layer_anatomy.md`](action_layer_anatomy.md) §2.4). (b) **The overlay's
failure treatment** — net-token routing on the verdict.

**Recommended: an MTD interrupt reads as the failure verdict**, so the net falls back
(the feedback Jin's motivating example wanted; register §M1) while the substrate's
mechanical reset applies to substrate state. **Named build prerequisite — discharged (verified 2026-07-27):** the wiring
landed with the movement-layer attacker. An MTD interrupt propagates out of `step()`
for all six verbs and the verdict adapter reads it as failure, so the net does fall
back on a mutation as intended. **Scope boundary:** a mutation during a
dwell-only place's dwell raises no verdict and is not felt by the token — an honest
limitation (ties to the H-coupling hypothesis, anatomy §6).

---

## 6. Live-stepping lifecycle, determinism, and the per-event record

### 6.1 Lifecycle

Per step at the token's place `a`: **enter** and **draw** the tactic's time — since
S3 a draw from `Exponential(mean = duration_s)`, the declared D4 value in
[`tactic_durations.json`](../../../../data/ogasp/tactic_durations.json) read as the
distribution's mean rather than as a constant
([`stochastic_timing_design.md`](stochastic_timing_design.md); the draw lives at
[`movement/timing.py`](../../../../src/mtdsim/l3_simulation/movement/timing.py) and
is taken at one point in `_walk`). If `a`'s action is available, **fire** the mapped
verb via `step(verb, duration=that time)`, **read** the binary verdict, **select**
the `success`/`failure` column, **compose + renormalise** (§1); else route on base
weights. **Sample** the next transition under the run seed and move the token.
**Terminate** on reaching the profile's objective set, or **censor** at the
simulation horizon (R4 makes the horizon a free experimental variable).

Under the GSPN reading, the tactic's time **is** the place's timed transition and
the routing sample **is** its immediate transition (zero simulated time). A tactic
whose declared duration is zero (`resource-development`) is a pure immediate
transition, drawing nothing — and, since S3-R, an action dispatched from such a
tactic runs for no simulated time at all.

**The movement layer supplies every unit of the attacker's time (S3-R).** The
tactic's draw is the *whole* cost of the visit: the dispatched action is priced by
the tactic that invoked it, and the substrate's own action costs are not consumed on
this arm. Three cases, one rule. An action-bearing place spends its draw on the
action. A **dwell-only** place — one the selected controller mapping declares as
dispatching no verb — spends its draw and dispatches nothing, so the draw is its
entire cost. A place whose action is **blocked** by an unmet precondition spends its
draw too: the attacker committed the procedure the tactic represents and it came to
nothing, and charging nothing would make an unsatisfiable place a free move.

Time is **supplied** by the movement layer and **spent** by the SimPy loop; the net
holds no clock. That distinction is what keeps the arrangement portable — another
simulator's event loop would spend the same supplied durations, which it could not
do if the durations lived in MTDSim's constants — and it is the same argument, run
in the opposite direction, that keeps the MTD confusion penalty on the substrate
side of the seam: the penalty models what a *defender* does to an attacker, so it
belongs to the simulator, not to the portable layer (§5;
[`stochastic_timing_design.md`](stochastic_timing_design.md) §4).

**The degenerate case (renormalisation denominator → 0).** Because the composition
renormalises across every out-edge and the verdict values are almost never all zero,
a place with any out-edge keeps positive mass — the elaborate stall machinery an
earlier draft carried is unnecessary. The one residual case: if a verdict genuinely
zeroes every out-edge (no default rule does this today), the driver re-fires in place
(bounded retry) rather than moving — a stepping-loop detail for the build, not a net
edge. This is the only place a "stall" can arise and it is handled by a bounded retry,
not a special structure.

### 6.2 Determinism (SIM-05)

The walk is a deterministic function of **run seed + net (structure + synthetic
overlay) + outcome overlay + substrate seed**. The overlay is static data; composition
and sampling are pure given the seed; `step(verb)` reads the substrate's own seeded
dice (no new randomness on the verdict — map §5). Same inputs → same walk.

S3 adds a **third** random stream — the per-tactic dwell — and it is deliberately
isolated: it is seeded by a pure transform of the run seed, so it neither reads nor
advances the token sampler's stream or the substrate's global dice. The consequence
is testable and is tested: because nothing in a no-MTD run reads the clock to decide
an outcome, switching between the fixed-dwell and drawn-dwell regimes changes *when*
events happen but not *what* happens — the same places, verbs, outcomes, verdicts and
routing decisions, in the same order, with the substrate's per-action costs identical
event for event. A leak into either shared stream would reorder that sequence at once.

### 6.3 Per-event record schema

One record per step so MTTC/ASR and the M8 review compute downstream: `sim_time`,
`place`, `band`, `place_class` (action-bearing / dwell-only), `verb` (or `null`),
`verdict` (`success`/`failure`/`halt`/`none`), `overlay_branch`
(`success`/`failure`/`none`), `out_distribution` (the composed or base out-weights),
`transition_taken`. Raw material for the metrics, not itself a metric.

The record's `dwell` field carries **the time the event actually consumed** — since
S3, this visit's draw, so it differs from visit to visit at the same place, and it is
the partial time served when an MTD interrupt cut the dwell short. Read with
`start_time` / `end_time` it decomposes an event into behavioural dwell and the
dispatched verb's own substrate cost (`end_time − start_time − dwell`), which is what
keeps the two timing layers separable in the analysis rather than fused into one
elapsed figure.

---

## 7. Resolved design questions and hard constraints

**Resolved.** *Combined vs two files* → one
[`outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json) with a
`success` and a `failure` value per pair (shared model + composition). *Per-edge vs
phase-level authoring* → **ground-up per-pair**, reasoned from tactic-pair semantics
(the coarse band rule is retired). *Resource-development* → **in the overlay** and in
the structural synthetic overlay (bridged, not an island — [`synthetic_overlay.md`](synthetic_overlay.md)),
weighted like every other source. *Coverage* → the **whole** directed tactic-pair set
(§3), not a scoped subset.

**Hard constraints honoured.** Binary outcome only (M2); base D3 weights stand
(conditioned, never re-derived — §(f)); declared policy layer, not reverse-engineered
weights (envelope-not-actor); CKC is an input (the band prior), not a runtime layer;
attacker-only (D5), baseline MTTC untouched; **no simulator or net-build code changed**
— design record + one authored data file + a provenance row; the composition/stepping
code is the profiled-attacker build.

---

## 8. Where this connects, and when to update

- **Consumes:** [`supervisor_decision_register.md`](supervisor_decision_register.md)
  §M2/M1/R1/R4; [`controller.md`](controller.md) §4 (per-verb verdict oracle);
  [`synthetic_overlay.md`](synthetic_overlay.md) (the structure it weights);
  [`../../metrics_semantics.md`](../../metrics_semantics.md) §(f); the AAR corpus.
- **Feeds:** the profiled-attacker build (composition, lifecycle, record schema) and
  the first-numbers matrix.
- **Artefact:** [`outcome_overlay.json`](../../../../data/ogasp/petri/outcome_overlay.json)
  (value semantics, composition rule, the model, the resolved 123-pair table);
  provenance row in [`../../provenance.md`](../../provenance.md).
- **When to update:** if Marc revises the bands, the `enables` sets, or the
  success/failure rules; if a substrate verb is mapped to a new tactic (that place
  starts consuming its overlay values); if the interrupt→driver wiring lands (§5
  prerequisite done); if the R2 success-rate axis lands (it gates the verb upstream of
  the verdict — map §5 — and does not touch this overlay); if richer outcome classes
  replace the binary verdict (a new ruling). A design snapshot dated in the frontmatter.
