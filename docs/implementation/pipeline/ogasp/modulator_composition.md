---
status: durable
created: 2026-08-01
updated: 2026-08-30
topic: "The composition register — every routing factor the model carries, which seam each lives on, which are active in the reported configuration, and why that boundary is the portability claim made structural"
---

# The composition register — what conditions the attacker's routing, and where each part lives

**Status:** durable. Part C of the procedural-rigidity handoff. No document
currently states **what the routing factors are, where each lives, and which are
active in the reported configuration**, and that gap is a claim-integrity risk
rather than a tidiness one: axis 3's demonstrated badge was earned with the
modulators null, so a reported configuration that quietly ships one active would
describe a different model than the one the plurality evidence was measured on
([`model_scope_freeze.md`](model_scope_freeze.md) §4). This record is that
statement.

It declares no value and moves no badge. It records structure, the seam rule that
governs it, and the joint-composition measurement that had never been taken.

## 1. The composition rule, in one place

At a source place `a` whose action returned verdict `v`, the routing weight of
each destination `b` is

```
                base(a→b) · overlay_v(a→b) · Π_m  m(a→b | state)
    w'(a→b)  =  ────────────────────────────────────────────────
                Σ_b'  base(a→b') · overlay_v(a→b') · Π_m  m(a→b' | state)
```

renormalised over the source's out-set
([`attacker_state_seam.md`](attacker_state_seam.md) §2). Multiplicative
throughout, never additive — the argument the overlay design made and won:
multiply-then-renormalise conditions the corpus-grounded proportions without
inventing a magnitude or inverting the within-class ordering.

## 2. The register — every factor, its seam, its status

| # | Factor | Seam | Declared values | Null configuration | Active in the reported configuration? |
|---|---|---|---|---|---|
| 1 | **Base transition weights** | movement | corpus flow-proportions (not a declared *family* — measured from the Attack Flow corpus) | — (always present; it *is* the prior) | **yes** — it is the model |
| 2 | **Outcome overlay** (verdict conditioning) | movement | `v3_persistent_backward`, per-verdict value tables | a verdict-blind overlay whose tables are empty passes every destination through at 1.0 | **yes** |
| 3 | **Utility modulator** (axis 6, cost-sensitivity) | movement | benefit family + rationality exponent λ (declared 1.0) | λ = 0 → every factor 1.0, bit-identical | **no** |
| 4 | **Learning modulator** (axis 7, within-run belief) | movement | κ (declared 1.0), ρ (declared 0.5), Laplace α = β = 1; **credit rule selector, default `acceptance`** | κ = 0 → no factors returned, bit-identical | **no** |
| 5 | **Tactic-to-verb mapping** | controller | `v1_ckc_total` / `v2_partial`, versioned registry | not nullable — a mapping is always selected | **yes** (named per experiment) |
| 6 | **Precondition relation** | controller | verb-level requires/produces/clears, versioned (**`v2_achievement`** since 2026-08-02) | consulted only by factor 4; inert when κ = 0 | **no** (rides with factor 4) |
| ~~7~~ | ~~**Iterated utility modulator**~~ | — | **RETIRED 2026-08-02** — built, swept over 4 200 runs, ruled a negative result and deleted ([`iterated_cost_model.md`](iterated_cost_model.md) §0). Its row is struck rather than removed so the register records that the slot was tried | — | **no — the code no longer exists** |
| 8 | **FSM-alignment overlay** (capability-distance dial) | movement | α (declared **0.0**, the null); the objective-productive verb set is a transcription, not a declared magnitude | α = 0 → no factors returned, bit-identical | **no** — **superseded as an instrument by factor 9**, retained with its sweep as a measured negative |
| 9 | **FSM-succession overlay** (the procedural-order dial) | movement | α (declared **0.0**, the null), a float over [0, 1] | α = 0 → no factors returned, bit-identical | **no** |
| 10 | **FSM succession relation** | controller | verdict-conditioned successors + the interrupt table + the objective-productive verb set, versioned (`v1_brown_fig3`) | consulted only by factor 9; inert when α = 0 | **no** (rides with factor 9) |

**Two 2026-08-30 mechanisms are deliberately *not* rows.** The **fresh-host
contract** (`fresh_host_contract`, on by default — Marc's loop-fix ruling,
register T1 annotation) is a host-selection invariant in the driver's dispatch
and reweights nothing; it changes which host a verb acts on, not the routing
composition above. The **token-hold rule** (`token_hold`, off) holds the token
rather than reweighting, reading the FSM state factor 9 tracks at α = 0; it is a
supervisor-directed band point beside factor 9, not a factor
([`fsm_token_hold_findings.md`](fsm_token_hold_findings.md)). Neither is active
in the routing composition of the reported configuration; the contract *is*
active in the reported configuration as an attacker invariant.

**Factor 4 gained a credit-rule selector and factor 6 gained achievement terms on
2026-08-02** ([`progress_credit.md`](progress_credit.md)). Neither changes this
register's structure and neither is active in the reported configuration. Two
things are worth stating here rather than only in the build record. The selector
defaults to `acceptance`, which is the rule every recorded figure was produced by,
so factor 4 stays reproducible exactly as factor 3 does. And the artefact change
is **verified inert** — `foothold` is produced-only, so `is_ready` is unchanged
(0 disagreements, exhaustively checked on both mappings), which is what keeps the
readiness bit's accuracy figures valid without re-measurement.

**That inertness check also covers the retired factor 7, and this is why its
results still read.** The same property held for `enabling_cost`, factor 7's own
consumer, which is why the axis-6 sweep recorded against `v1_substrate` remains a
valid record of the model it ran under even though the artefact has since moved.
The code is gone; the record is not, and the check is what keeps the two
consistent.

A **control arm** also landed beside factor 4: `DeclaredReadinessBias`, the static
modulator built from factor 4's own declared inputs, which exists to test whether
the learner differs from a lookup. It is a comparison arm, never a factor, and it
must not appear in a reported configuration.

**Factor 8 landed 2026-08-02** ([`fsm_alignment_overlay.md`](fsm_alignment_overlay.md)),
and three things about it belong here rather than only in its own record. It
**scores no axis** — it is an instrument whose sweep measures how much of the
profiled attacker's disadvantage is procedural rigidity, and no position on its
dial is a claim about anything, which is why its declared value is the null.
It is the register's **first factor that may zero an out-edge**, and the licence
was earned rather than asserted: an exhaustive static check over every profile net
× mapping × overlay version × verdict × capability subset × retrace suppression
returns 0 cells in which the limiting end could empty an out-set, so `may_zero` is
declared per *instance* and only at α = 1. And it carries a **composition bar with
factor 4** (§2.1 below), which is the retired factor 7's lesson applied rather
than a new rule.

**Swept 2026-08-02 over 2 080 runs, and the register owes two numbers to any arm
that quotes it.** Pooled path entropy at the declared null is 2.712 bits and falls
monotonically to 1.112 at α = 1 — cheap over three-quarters of the band (0.16
bits) and expensive in the last quarter (1.44) — so a non-zero-α arm reports its
own figure from that table, exactly as §4 requires. And the bar in §2.1 is now
better argued than when it was written: the sweep showed factor 8's limiting end
optimises the attacker toward *permitted* actions, which is what factor 4's
shipped credit rule already does, so the two agree on the very ordering the
sub-additivity result depended on their disagreeing about.

**Factor 9 was swept 2026-08-03 over 2 080 runs, and the register owes any arm two
numbers and one warning.** Pooled path entropy runs 2.714 bits at the null to
1.682 at α = 1 — materially gentler than factor 8's 1.112 — and roughly one
routing decision in eleven is an *abstention*, where the net offered no FSM-legal
move and the factor did nothing. The warning: at α = 1 the attacker spends
**67.6 %** of its visits in dwell-only places against 34.1 % at the null, because
transparency composed with a narrow licensed set shifts mass onto dwell rather
than onto the licensed verb. Both alignment factors have now returned measured
negatives, and no third is licensed.

**Factors 9 and 10 landed 2026-08-03** ([`fsm_succession_overlay.md`](fsm_succession_overlay.md)),
and factor 9 supersedes factor 8 as the alignment instrument. Factor 8's sweep
measured its target to be the wrong one — *able to act* is not *making progress*,
and at its limiting end the attacker owned one host forever — so factor 9
conditions on the **inherited FSM's own succession**, which already pivots after a
compromise because Brown drew it that way. Three things belong in the register
rather than only in the build record. It **scores no axis**: it is a declared
comparability concession and a swept instrument, so its declared value is the
null. Its **stall guarantee is structural rather than enumerated** — where the net
offers no FSM-legal move the factor attenuates nothing, so an out-set can never be
emptied; the exhaustive check returns 47 079 offending cells without that rule and
0 with it. And factor 10 **re-homes the objective-productive verb set** onto the
controller seam, repairing the impurity factor 8 had to carry because its brief
barred touching the precondition relation.

Factors 1–4, 8 and 9 are **routing factors** composing multiplicatively per the rule
in §1. Factors 5–6 and 10 are **controller artefacts**: they do not multiply into the
routing weight, they declare how the movement layer meets *this* substrate. They
are in the register because they are the parts an adopter re-declares, and
because omitting them would make the portability claim in §3 unreadable.

### Factor 7 was tried and is retired — what the slot taught the register

Factor 7 was the repair of factor 3's decision model: a state-conditioned
expected cost and a benefit measured through the profile's own routing net,
declaring no new magnitude. It was built beside factor 3 with an arm selector
whose `declared` arm reproduced factor 3's factors exactly, swept over 4 200
runs against pre-registered conclusions, and **ruled a negative result**
([`iterated_cost_model.md`](iterated_cost_model.md)). The implementation is
deleted; factor 3 stays, because every recorded figure in the project was
produced by it.

Two things it established belong to this register rather than to that record.

**The composition hazard it raised was real and is now moot, but the rule
generalises.** Factor 7's expected-cost arms conditioned on readiness, and so
does factor 4, against the same declared artefact — one signal applied twice
through two multiplicative factors. The bar was that no arm may compose them
until a fresh joint check runs, and the reason the existing check (§5) could not
transfer is the part worth keeping: it found factors 3 and 4 sub-additive
**because they pull in opposite directions**, and factor 7 removed exactly that
disagreement. **Two factors that agree may compound where two that disagreed did
not**, so sub-additivity is never inherited across a change that alters whether
two factors agree. That is a standing rule for any future factor, not a fact
about a deleted one.

### 2.1 The bar between factors 4 and 8 — the same rule, its second application

**No arm may compose factor 8 with factor 4 until a fresh joint check runs.** They
condition on the same capability state against the same declared artefact
(factor 6), which is structurally the hazard factor 7 raised — one signal applied
twice through two multiplicative factors.

What makes the bar bind rather than transfer is the rule above. The §5 check found
factors 3 and 4 sub-additive **because they disagree**; factor 8 removes that
disagreement from the other side. It prefers destinations that are ready and
productive, and factor 4 under its shipped `acceptance` credit rule prefers
destinations that are *permitted* — very nearly the same ordering, arrived at by a
static lookup and by accumulation respectively. Two factors that agree may compound
where two that disagreed did not, so nothing measured about 3 × 4 licenses any
claim about 4 × 8.

There is a second reason to keep them apart that is about *interpretation* rather
than arithmetic, and it is the sharper one. Factor 8's whole purpose is to be a
dial with a declared scale; composed with a factor that pushes the same direction
by an undeclared amount, the scale stops meaning what the sweep reports it to
mean.

**A retired factor still owes its row.** The slot is struck rather than deleted
so a reader can see the register records what was attempted, not only what
survives — the same reasoning that keeps a measured negative in the criterion
rather than an absence.

**The reported-configuration pin (§4) is unaffected.** The headline arm still
runs modulators null, and axis 3's plurality badge still belongs to that arm.

## 3. The seam split, and why it is the portability claim made structural

**The rule.** Portable modulators stay on the **movement seam**; substrate-coupled
declarations go on the **controller seam**.

That boundary is not organisational preference — it is the statement of *which
parts an adopter keeps and which they re-declare for their own simulator*, which
is the whole content of the portability claim. Read down the register: factors 1–4
are statements about how a CTI-derived campaign envelope behaves, and carry over
to any substrate unchanged. Factors 5–6 are statements about *this* simulator's
action vocabulary and *this* simulator's procedural order, and every one of them
must be rewritten to port.

**Moving the learner or the utility model into the controller layer would dissolve
the claim**, because it would say the attacker's cost-sensitivity and its capacity
to learn are properties of MTDSim rather than of the modelled adversary. They are
not. The learner's belief is keyed on tactic-places and readiness, both of which
exist in any substrate with ordered actions; only the *relation* that says which
actions establish which capability is MTDSim-specific, and that is exactly the
piece held on the controller seam as factor 6.

**What this buys, stated as an adopter would meet it.** To port this framework to
another simulator you declare three artefacts and change no movement-layer code:
its **action vocabulary** (factor 5 — which tactic dispatches which of your
verbs, or none), its **procedural order** (factor 6 — what each verb requires
and produces), and its **succession** (factor 10 — which verb its own attacker
runs next, and where its interrupt handler restarts). The precondition relation was built to that shape deliberately: it
is verb-keyed, not tactic-keyed, so it composes with any mapping rather than
having to be rewritten per mapping.

## 4. The reported configuration is pinned, and this is a claim-integrity rule

**The headline arm runs with modulators null** — factors 3, 4 and 6 off. Any
modulator-active arm is reported as its **own labelled arm with its own plurality
figure**.

The reason is measured, not precautionary. Both built modulators narrow traversal:
the destination-only learner reduced path entropy in all ten profile × mapping
cells tested ([`learning_capability.md`](learning_capability.md) §7.5), and rising
cost-sensitivity collapsed it from 2.23 bits to 0.24 at the near-greedy end
([`incentive_rationality.md`](incentive_rationality.md)). Axis 3's DEMONSTRATED
badge rests on pooled path entropy of 1.45–2.71 bits with the modulators off
([`experiment_02_findings.md`](experiment_02_findings.md) §12). Shipping a
modulator active in the headline arm would therefore report a plurality figure the
headline arm does not have.

This rule is the freeze's and is not revised here (§4 of the freeze record). What
this record adds is the measurement that had never been taken.

## 5. The joint-composition check — the arm that had never run

The three declared families had only ever been swept **one at a time**. Two of
them independently narrow traversal, so composing them should compound the
narrowing — and that had never been measured, which meant the pinned configuration
in §4 rested on an inference rather than on evidence.

**Design.** A crossed arm at the declared values: {learner off, learner declared}
× {utility off, utility declared}, both mappings, all five profiles, ten seeds,
both MTD conditions (800 runs), reporting pooled path entropy and distinct hosts.
Pre-registered as J1 and J2 in
[`learning_readiness_prereg.md`](learning_readiness_prereg.md) §5 before any
output existed.

**Verdicts.** Recorded in §6 of
[`learning_readiness_findings.md`](learning_readiness_findings.md), with the rest
of the sweep's results, so the numbers live with the study that produced them
rather than being restated here. The headline, because it bears directly on §4:
**J1 MOVED in all four cells — the narrowing is sub-additive, not compounding.**
The two modulators pull in opposite directions on the same edges (a static
declared preference for cheap, precondition-coupled tactics, against a learned
state-conditioned discovery that those tactics fail when attempted unready), so
adding the learner to the utility modulator *recovers* most of the breadth the
utility modulator alone costs.

**That falsifies the reasoning in §4 without changing its rule.** The inference
that composing the modulators compounds the narrowing was never measured; it is
now measured and wrong. The pin stands regardless, on the part of §4 that was
always the load-bearing half: **every single-modulator cell still narrows traversal
against the null cell**, so the plurality evidence still belongs to the
modulators-null arm and a modulator-active arm still reports its own figure.

## 6. Where this connects, and when to update

- **Governs:** the reported configuration of every experiment from here.
- **Builds on:** [`attacker_state_seam.md`](attacker_state_seam.md) (the
  composition rule and the null-equivalence guarantee that makes each factor
  ablatable), [`model_scope_freeze.md`](model_scope_freeze.md) §4 (the pin).
- **Registers the factors owned by:**
  [`success_failure_overlay_design.md`](success_failure_overlay_design.md)
  (factor 2), [`incentive_rationality.md`](incentive_rationality.md) (factor 3),
  [`learning_capability.md`](learning_capability.md) and
  [`learning_representation.md`](learning_representation.md) (factors 4 and 6),
  [`controller.md`](controller.md) / [`controller_mapping_v2.md`](controller_mapping_v2.md)
  (factor 5), [`iterated_cost_model.md`](iterated_cost_model.md) (factor 7),
  [`fsm_alignment_overlay.md`](fsm_alignment_overlay.md) (factor 8),
  [`fsm_succession_overlay.md`](fsm_succession_overlay.md) (factors 9 and 10).
- **When to update:** whenever a factor is added, its null configuration changes,
  or the reported configuration changes for any reason. A new modulator's axis
  record owes this register a row in the same commit that builds it.
