---
status: open
created: 2026-08-02
---

# Build the FSM-alignment overlay — a declared dial from CTI order to the substrate's procedural order, so the movement attacker becomes comparable with the other attackers and the coupling finding becomes a measured quantity

**Marc's proposal, 2026-08-02, and it is already this project's own named next
step.** The freeze record calls an FSM-alignment factor "the one mechanism still
worth building" (§5), and the variant it describes — **a static declared bias**,
as opposed to feeding the signal into the learner — is the one that was **never
built**. What shipped in its place was the learner-feeding form
([`../implementation/pipeline/ogasp/learning_representation.md`](../implementation/pipeline/ogasp/learning_representation.md)).
So this is not a new idea being introduced late; it is an existing shortlisted
item whose rejected sibling now has a different purpose.

**Read §5 of the freeze record before anything else**, including its three "what
it is not" claims. Those claims are the framing that keeps this defensible, and
two of them are the reason it must never be reported as a capability.

## 1. What it is, in Marc's terms

A graph overlay parameter `α ∈ [0, 1]` on the movement layer's routing:

- **α = 0 — no change, the default.** Bit-identical to the model without it.
- **α = 1 — transitions are limited to those on a shortest path to a phase that
  advances the substrate objective**, given the capabilities the attacker
  currently holds.
- **Intermediate (e.g. 0.5) — the attacker still tries other things but tends
  toward the FSM structure.**

**It is explicitly not an incentive-rationality implementation and must never be
reported as one.** Axis 6 is closed as DESIGNED with its attempted
implementations recorded as negative
([`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
axis 6, final disposition), and nothing here re-opens it. This is an extension
that makes the movement model *capable of moving in the right direction
artificially*, so the attacker is comparable with the others — it **mimics** what
learning or rationality would produce without claiming either.

## 2. Why the earlier rejection does not apply

The freeze record's §5 chose the learner-feeding form over the static bias with a
specific argument: *"The second is the one that generalises the capability… The
first would ship sooner and generalise nothing."*

That reasoning was about **generalising the axis-7 learning capability**. Marc's
purpose is different and the rejection does not transfer: the aim is
**comparability**, not capability. The movement attacker compromises roughly a
seventh of what the inherited attacker does, and a large part of that gap is CTI
order fighting the substrate's procedural order rather than anything about the
defence. A dial that closes the gap *on purpose and by a declared amount* turns
that confound into a measured quantity — which is exactly what the freeze record
says the instrument is for.

## 3. The target is now well defined, which it was not when §5 was written

The distance the overlay measures needs a destination, and the substrate supplies
one. Verified by reading the call sites of `update_compromise_progress`:

- **The verbs that genuinely advance the substrate objective are `SCAN_PORT`
  (credential reuse), `EXPLOIT_VULN` and `BRUTE_FORCE`.** `ENUM_HOST` also calls
  the progress hook but is guarded by `if curr_host.compromised` — it re-reports a
  host already owned and causes no compromise, so it is **not** a target.
- The objective itself is the substrate's termination condition,
  `terminate_compromise_ratio × total_nodes` — a network state, not a tactic.

Distance-to-productive is then a shortest path over the declared precondition
relation's eight-state capability closure:

| capabilities held | legal verbs | steps to compromise-capable |
|---|--:|--:|
| — | 1 | 2 |
| `host_stack` | 2 | 1 |
| `curr_host` (any superset) | 4–6 | 0 |

**MTD enters as a set contraction, not a scalar surcharge.** A network-layer
mutation clears `curr_host` and `curr_ports`, so the legal verb set contracts
from six to two and the distance regresses from 0 to 1. That is the
non-proportional response a normalised ratio could not see, and it is the whole
reason this shape is worth building where the utility ratio was not.

## 4. The honest limits, and they are the same three §5 already states

1. **It is not learning.** No accumulation, no belief, no update from experience —
   a declared bias from a static lookup.
2. **It is not axis 4.** It responds to the *substrate*, not to the defender.
3. **It is not a fidelity improvement.** It makes the attacker behave more like
   the host simulator expects, **which is the opposite of behavioural
   independence.** This is the one a reviewer will press on: at α = 1 the
   attacker has been tuned toward the inherited attacker's own procedural order,
   and any difference in conclusions between them shrinks by construction.

**A fourth limit this brief adds.** The diversity family remains invisible —
what OS and Service Diversity destroy lives outside the guard the capability
vocabulary was transcribed from, and no legal artefact edit gives it a channel
([`2026-08-02_os_service_diversity_indistinguishability.md`](2026-08-02_os_service_diversity_indistinguishability.md)).
Any claim about this overlay's MTD response is confined to the
position-destroying family, and the record must say so rather than implying
coverage it does not have.

## 5. What the sweep is actually for — and why a *falling* effect is the result

The instrument's value is the dial, not any operating point. Sweeping α measures
**how much of the profiled attacker's disadvantage is procedural rigidity rather
than behaviour**, on this project's own substrate, with a null arm that
reproduces every recorded finding at full strength.

**The most valuable outcome is one that would look like a negative.** If the
defence-ranking inversion (`experiment_02_findings.md` §9, ρ = −0.893) **weakens
monotonically as α rises and vanishes near α = 1**, that is a strong, quantified
statement that the inversion is caused by the attacker's behavioural shape rather
than by noise or by an artefact of the mapping. It converts the project's
headline from a categorical contrast into a dose-response curve. Pre-register it
that way, and pre-register the direction, so a vanishing inversion reads as
confirmation rather than as damage.

## 6. Recommended approach

Build it as a **fourth routing factor on the movement seam**, consuming the
controller artefacts as factor 4 already does — the mapping (factor 5) and the
precondition relation (factor 6), unchanged and unbumped.

The mechanism, smallest form first per house discipline: at a routing decision,
compute each candidate's distance-to-productive from the attacker's current
capability state; let `d*` be the minimum over the out-set; multiply candidates
at `d*` by 1 and candidates above it by `(1 − α)`. At α = 0 every factor is 1.0
and the run is bit-identical; at α = 1 every non-minimal candidate is zeroed.

**Zeroing engages the seam's stall rule**, so the factor must declare
`may_zero = True` and re-run the no-stall check across its parameter space — or,
if that check fails, the α = 1 end becomes `(1 − α)` floored above zero and the
band end is reported as near-limiting rather than limiting. **Settle this before
building**, because it decides whether α = 1 is reachable at all.

**Alternatives considered.** A soft exponent (`(1/(1+d))^α`) avoids the stall
rule entirely but loses the clean "limits transitions to shortest paths" reading
at α = 1, which is the reading that makes the dial interpretable — prefer the
linear form and handle the stall explicitly. Feeding the signal to the learner
instead is the shipped mechanism and answers a different question. Making it a
controller-seam factor was considered and rejected: the *rule* (prefer moves that
shorten the distance to productive action) is portable and belongs on the
movement seam; only the relation it reads is substrate-specific, and that already
sits on the controller seam as factor 6.

## 7. Validation gates

1. **α = 0 is bit-identical**, asserted over profiles × seeds × mappings × MTD
   conditions as a test, not a run — the standing U1/C1 discipline.
2. **The stall question is settled** (§6) and the no-stall check re-run across the
   α band if `may_zero` is declared.
3. **No new declared magnitude beyond α**, with a tier, a band and a sweep.
4. **The register gains a row** in
   [`../implementation/pipeline/ogasp/modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)
   in the same commit, including the composition bar with factor 4 — both
   condition on the same capability state against the same artefact, and the
   existing joint check does not transfer to two factors that *agree*.
5. **Reader gates unchanged**; no golden moves (this is a movement-layer factor).

## 8. Hard constraints

- **Never reported as incentive rationality or as learning.** Axis 6 is closed;
  this scores no axis and its record must say so in its own first paragraph.
- **α is swept, never chosen because it improves an outcome.**
- **Claims confined to the position-destroying family** (§4).
- **The reported headline configuration still runs modulators null** — the
  freeze's §4 pin is a claim-integrity rule and this factor does not touch it.
- Determinism (SIM-05); envelope-not-actor; Australian English; branch per
  session; never push.

## 9. Reading list

- [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
  §5 — the instrument, and the three "what it is not" claims. **Read first.**
- [`../implementation/pipeline/ogasp/modulator_composition.md`](../implementation/pipeline/ogasp/modulator_composition.md)
  — the seam split, the register this joins, and the retired factor 7's lesson
  that sub-additivity is never inherited across a change in whether two factors
  agree.
- [`../implementation/apt_model_criterion.md`](../implementation/apt_model_criterion.md)
  axis 6 final disposition and axis 4 — what this must not claim.
- `data/ogasp/controller/precondition_relation.json` — the capability closure the
  distance is computed over.
- [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
  §9 — the inversion the sweep is aimed at.

## 10. Out of scope

- **Any change to the precondition relation or the mapping.** Both are consumed
  unchanged and unbumped; widening the relation regresses a predictor measured at
  1.0000 and moves every recorded figure two shipped modulators produced.
- **Any axis-6 or axis-7 badge claim.**
- **Re-running recorded experiments** under a non-zero α. They stand as records of
  the model they ran under; the sweep is its own study with its own null arm.
- Dissertation prose.
