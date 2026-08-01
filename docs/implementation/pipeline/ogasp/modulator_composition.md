---
status: durable
created: 2026-08-01
updated: 2026-08-01
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
| 4 | **Learning modulator** (axis 7, within-run belief) | movement | κ (declared 1.0), ρ (declared 0.5), Laplace α = β = 1 | κ = 0 → no factors returned, bit-identical | **no** |
| 5 | **Tactic-to-verb mapping** | controller | `v1_ckc_total` / `v2_partial`, versioned registry | not nullable — a mapping is always selected | **yes** (named per experiment) |
| 6 | **Precondition relation** | controller | verb-level requires/produces/clears, versioned | consulted only by factor 4; inert when κ = 0 | **no** (rides with factor 4) |

Factors 1–4 are **routing factors** composing multiplicatively per the rule in §1.
Factors 5–6 are **controller artefacts**: they do not multiply into the routing
weight, they declare how the movement layer meets *this* substrate. They are in
the register because they are the parts an adopter re-declares, and because
omitting them would make the portability claim in §3 unreadable.

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
another simulator you declare two artefacts and change no movement-layer code:
its **action vocabulary** (factor 5 — which tactic dispatches which of your
verbs, or none) and its **procedural order** (factor 6 — what each verb requires
and produces). The precondition relation was built to that shape deliberately: it
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
  (factor 5).
- **When to update:** whenever a factor is added, its null configuration changes,
  or the reported configuration changes for any reason. A new modulator's axis
  record owes this register a row in the same commit that builds it.
