---
status: durable
created: 2026-08-02
updated: 2026-08-02
topic: "The FSM-alignment overlay (composition-register factor 8) — a declared dial from CTI order to the substrate's procedural order, its distance model over the declared capability closure, and the exhaustive no-stall check that decided whether the limiting end of its band is reachable"
---

# The FSM-alignment overlay — a dial, not a capability

**This factor scores no axis of the APT criterion, and nothing it produces may be
reported as one.** Axis 6 (incentive rationality) is closed as DESIGNED with both
attempted implementations recorded as negative results and full incentive
rationality named as future work
([`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 6, final
disposition); nothing here re-opens it. It is not axis 4, because it responds to
the **substrate** rather than to the defender. And it is not learning: there is no
accumulation, no belief and no update from experience — it is a declared bias over
a static lookup. It is an **instrument**, in the sense the scope freeze uses that
word ([`model_scope_freeze.md`](model_scope_freeze.md) §5): a dial whose *sweep*
measures something, where no position on the dial is a claim about anything.

**What it measures is a confound in this project's own headline result.** The
profiled attacker compromises roughly a seventh of what the inherited attacker
does, and an unknown part of that gap is CTI order fighting the substrate's
procedural order rather than anything about the defence. A dial that closes the
gap on purpose and by a declared amount turns that confound into a measured
quantity, with a null arm that reproduces every recorded figure at full strength.

## 1. Why this shape, and why now

The scope freeze shortlisted an FSM-alignment factor as "the one mechanism still
worth building" and then described **two** variants of it. The variant that
shipped in 2026-08-01 was the learner-feeding one: the substrate's procedural
order transcribed into a declared controller artefact and consulted by a learner
keyed on `(destination tactic, precondition-satisfied?)`
([`learning_representation.md`](learning_representation.md)). The variant
described here — **a static declared bias** — was the sibling that was rejected,
and it is being built now because the argument that rejected it does not reach the
use it is being built for.

That argument was: *"The second is the one that generalises the capability… The
first would ship sooner and generalise nothing."* It is an argument about
**generalising the axis-7 learning capability**, and it is correct about that. The
purpose here is **comparability**, not capability. Generalising nothing is not a
defect in an instrument whose entire job is to be a measuring device with a
declared scale.

## 2. The rule

At a routing decision at source place `a`, over the destinations its net gives
strictly positive base mass:

```
    d(b | held)  =  0                       b's verb is objective-productive and
                                            legal in the held capabilities
                 =  1 + D(held ∘ verb(b))   b's verb is legal but unproductive
                 =  1 + D(held)             b's verb is blocked, or b dispatches
                                            no verb at all

    d*           =  min over the out-set

    m(a→b)       =  1.0        d(b) == d*
                 =  (1 − α)    otherwise
```

`D(held)` is the fewest legal verb applications separating the attacker's current
capability state from one in which *some* objective-productive verb would run.
The factor multiplies into the composition as one more term of
`base · overlay_v · Π_m m`, renormalised over the source's out-set, exactly as
factors 3 and 4 do.

- **α = 0 — the declared value, and the null.** The modulator returns no factors
  at all, so the arithmetic is the pre-existing composition and the run is
  bit-identical to one with no state attached.
- **α = 1 — transitions are limited to those on a shortest path to a productive
  action**, given the capabilities the attacker currently holds.
- **Intermediate α** — the attacker still tries other things and tends toward the
  substrate's FSM structure.

**The linear form was preferred over a soft exponent, and the trade was made
knowingly.** A soft form such as `(1/(1+d))^α` never reaches zero and so never
engages the seam's stall rule — but it also loses the reading that makes the dial
interpretable, because at its upper end it means nothing in particular. The
reading *at α = 1 transitions are limited to shortest paths* is the reading a
dose-response curve is reported against, so the stall was handled explicitly
instead of designed around (§5).

### 2.1 The model's one opinion

A blocked verb and a dwell-only place are scored identically: both cost a step and
leave the capability state where they found it. That is deliberate and it is the
whole content of "distance to productive action" — an action the substrate refuses
and an action the mapping never dispatches leave the attacker in the same place
having spent the same step. A legal but unproductive verb is scored **from the
state it produces**, so reconnaissance is cheap exactly when it is enabling and no
cheaper: with nothing held it sits at `d = 2` against everything else's 3, and
with the host cursor already held it sits at 1 alongside them.

## 3. The target, verified rather than assumed

The distance needs a destination, and the substrate supplies one. The
objective-productive verbs were read off the call sites of
`AttackOperation.update_compromise_progress`:

| locator | verb | why it counts |
|---|---|---|
| `attack_operation.py:408` | `SCAN_PORT` | credential reuse compromises the host |
| `attack_operation.py:513` | `EXPLOIT_VULN` | `check_compromised()` on the exploited host |
| `attack_operation.py:547` | `BRUTE_FORCE` | a guessed login compromises the host |

The fourth call site, `attack_operation.py:377` in `_do_enum_host`, is **not** a
target: it is guarded by `if curr_host.compromised`, so it re-reports a host the
attacker already owns and causes no compromise. The objective itself is the
substrate's termination condition — `terminate_compromise_ratio × total_nodes`, a
network state rather than a tactic.

**This set is substrate-specific knowledge, and that makes it a recorded seam
impurity rather than a clean consumption.** By the seam rule
([`modulator_composition.md`](modulator_composition.md) §3) a substrate-coupled
declaration belongs on the **controller** seam, which would mean a field on the
precondition relation. It is not there, because this factor's brief consumes that
artefact *unchanged and unbumped* and adding a field to it would be neither. It
lives instead as a three-element module constant that is also a constructor
argument, so a port states it rather than inheriting it. The impurity is bounded
— one transcription of three verb names, on the same basis as the relation itself
— and it is recorded here rather than hidden. **Whether it should be promoted into
the relation at its next version bump is Marc's ruling, not this record's.**

Note what the target set is *not*: it is not derivable from the relation's
`foothold` capability. `foothold` is produced by `EXPLOIT_VULN` and `BRUTE_FORCE`
only, so a foothold-derived target set would silently drop `SCAN_PORT` and, at
`held = {curr_host}`, would move the minimal set from two destinations to one.
The two-verb variant is reachable by passing `objective_verbs` and is recorded
here so that the three-verb choice reads as a decision rather than as a default.

## 4. The distance table, and MTD as a set contraction

`D` depends only on which capabilities the objective-productive verbs require, so
the closure collapses to three states — and they are the handoff's own table,
recomputed by breadth-first search rather than asserted:

| capabilities held | legal verbs | `D` |
|---|--:|--:|
| — | 1 | 2 |
| `host_stack` | 2 | 1 |
| `curr_host` (any superset) | 4–6 | 0 |

**MTD enters as a set contraction, not a scalar surcharge.** A network-layer
mutation clears `curr_host`, `curr_ports` and `foothold` per the declared
relation, so the legal verb set contracts from six to two and `D` regresses from 0
to 1; an application-layer mutation clears nothing structural and `D` does not
move at all. That asymmetry is the reason this shape is worth building where the
axis-6 utility ratio was not: a normalised ratio is invariant to a proportional
inflation of its denominator, which is precisely how MTD's tax was found to be
levied, and a *set contraction* has no such invariance.

**The boundary that rides with it, and it is a hard one.** Any claim about this
factor's MTD response is confined to the **position-destroying** family. What OS
Diversity and Service Diversity destroy lives outside the guard the capability
vocabulary was transcribed from, so no legal edit to the declared relation gives
them a channel
([`../../../handoffs/2026-08-02_os_service_diversity_indistinguishability.md`](../../../handoffs/2026-08-02_os_service_diversity_indistinguishability.md)).
The dial is structurally blind to half the defence family, and the record says so
rather than implying a coverage it does not have.

## 5. The stall question, settled before the build — and the defect it caught

The brief made this the gating question, because it decides whether α = 1 is
reachable at all. It is, and the check that established it earned its keep.

**The structural half of the argument is not sufficient.** `factors` returns 1.0
for the argmin over the out-set it is handed, so at least one candidate always
survives α = 1 — but the seam multiplies that product into the distribution the
**outcome overlay has already composed**, and the overlay can hard-suppress a pair
with an exact zero. If every minimal-distance destination at some decision is a
pair the overlay zeroed, the surviving candidates are all off-band and α = 1
empties the out-set. That is a stall, and the driver reads a stall as walk
termination.

Because the hazard is a property of declared data rather than of a run, it is
decided by **enumeration rather than by sampling**: every profile net × controller
mapping × overlay registry version × verdict (including the distinguished `none`)
× capability subset × source place, plus each one-shot retrace suppression the S5
policy can apply to an out-set. A run-based check could only ever have said the
stall was not *reached*; this says it is not *reachable*.

**Verdict: 0 offending cells. The declared off-band floor is therefore 0.0, α = 1
is reachable, and the band end is reported as limiting rather than near-limiting.**
`may_zero` is declared **per instance** rather than once for the class, so the
seam's zero guard stays a live proof for every arm of the sweep except the one
that actually needs the licence.

**The first run of that check returned 14 184 offending cells, and it was right
to.** A profile net can carry an out-edge at base weight **zero**. The composition
drops such an edge before this factor's product applies, so it is not a candidate
— but the first implementation computed the minimum over the whole out-set, and a
zero-weight destination that happened to be the unique argmin left every *live*
candidate off-band. At α = 1 that is a stall manufactured by the factor itself.
The fix is one line (restrict to strictly positive base mass) and is pinned by its
own regression test; the point worth recording is that the pre-build gate the
brief insisted on found a real defect rather than merely certifying a design.

## 6. What this factor can structurally do, stated before it is swept

A routing factor can only act where there is a choice to make and where its own
quantity discriminates between the options. Both bounds are computable from the
declared artefacts, and they are reported here so that a small measured effect is
not later mistaken for a small *modelled* effect.

Over each profile's net × the five reachable capability states (place-counted, not
visit-weighted — a run's decisions are distributed over these cells very
unevenly):

| mapping | singleton out-sets | factor uniform (no bias possible) | biasable |
|---|--:|--:|--:|
| `v1_ckc_total` | 0.0–41.7 % | 36.0–70.0 % | 30.0–64.0 % |
| `v2_partial` | 0.0–41.7 % | 25.3–60.0 % | 40.0–74.7 % |

The two ends are `aggregate` (widest out-sets, most headroom) and
`infrastructure_setup` (narrowest). This is the same measurement that bounded
axis 6's closure — between 14 % and 38 % of decision points there sat at singleton
out-sets where the renormalised factor is exactly 1.000 whatever a mechanism
computes — and it says the ceiling here is higher but not unbounded: on the
go-forward mapping between two-fifths and three-quarters of cells offer the dial
anything at all.

## 7. Composition: the bar with factor 4

**No arm may compose this factor with factor 4 (the readiness learner) until a
fresh joint check runs.** The two condition on the *same capability state* against
the *same declared artefact*, and the existing joint check does not transfer.

The reason it does not is the lesson the retired factor 7 left the register
([`modulator_composition.md`](modulator_composition.md) §2): the measured
sub-additivity of factors 3 and 4 was found to hold **because they pull in
opposite directions** — a static declared preference for cheap,
precondition-coupled tactics against a learned discovery that those tactics fail
when attempted unready. This factor removes that disagreement. It prefers
destinations that are ready and productive; the learner under its shipped credit
rule prefers destinations that are *permitted*, which is very nearly the same
ordering. **Two factors that agree may compound where two that disagreed did
not**, so sub-additivity is never inherited across a change in whether two factors
agree. The bar is the register's standing rule applied, not a new one.

The **reported-configuration pin is untouched**: the headline arm still runs
modulators null, and every non-zero-α arm is its own labelled arm with its own
plurality figure ([`model_scope_freeze.md`](model_scope_freeze.md) §4). That is a
claim-integrity rule about which arm owns axis 3's plurality evidence, and this
factor does not reach it.

## 8. The honest limits

The three the freeze record already states, plus one this build adds.

1. **It is not learning.** No accumulation, no belief, no update from experience —
   a declared bias from a static lookup.
2. **It is not axis 4.** It responds to the substrate, not to the defender.
3. **It is not a fidelity improvement — and this is the one a reviewer will press
   on.** It makes the attacker behave more like the host simulator expects, which
   is the opposite of behavioural independence. At α = 1 the attacker has been
   tuned toward the inherited attacker's own procedural order, so any difference
   in conclusions between the two shrinks **by construction**. That is not a
   confound in the study; it is the study's *measurement principle*, and it is
   only defensible because the direction is pre-registered and the null arm is
   exact.
4. **The diversity family is invisible to it** (§4). Any statement about this
   factor's MTD response is confined to the position-destroying family.

## 9. Validation gates

| gate | status |
|---|---|
| α = 0 is bit-identical, asserted over profiles × seeds × mappings × MTD conditions **as a test, not a run** | **held** — 5 profiles × 2 mappings × 5 seeds × 2 MTD conditions, record stream compared field for field |
| the stall question is settled, and the no-stall check re-run across the band | **held** — exhaustive and static (§5); 0 offending cells; the checker is itself checked against a sabotaged overlay |
| no new declared magnitude beyond α, with a tier, a band and a sweep | **held** — one parameter, `declared-judgement`, band `[0, 0.25, 0.5, 0.75, 1]`, sweep pre-registered in [`fsm_alignment_prereg.md`](fsm_alignment_prereg.md) |
| the register gains a row in the same commit, including the composition bar with factor 4 | **held** — [`modulator_composition.md`](modulator_composition.md) row 8 and §7 |
| reader gates unchanged; no golden moves | **held** — this is a movement-layer factor; no substrate file is touched and no measure is redefined |

## 10. Reproduce

```
PYTHONPATH=src python -m mtdsim.l3_simulation.movement.alignment --table v2_partial
PYTHONPATH=src python -m mtdsim.l3_simulation.movement.alignment --check-stalls
PYTHONPATH=src python -m pytest tests/l3_simulation/test_movement_alignment.py
```

## 11. Where this connects

- **Consumes unchanged and unbumped:** the precondition relation (register
  factor 6) and the tactic-to-verb mapping (factor 5).
- **Registered in:** [`modulator_composition.md`](modulator_composition.md) as
  factor 8, with the factor-4 composition bar.
- **Declares:** α, in `data/ogasp/movement/alignment_rules.json`, under the
  precedent in [`../../declared_value_provenance.md`](../../declared_value_provenance.md).
- **Answers to:** [`model_scope_freeze.md`](model_scope_freeze.md) §5, which named
  the instrument and supplied the three claims it may not make.
- **Aimed at:** [`experiment_02_findings.md`](experiment_02_findings.md) §9 — the
  defence-ranking inversion the sweep converts into a dose-response curve.
- **When to update:** when the sweep's verdict lands; if the precondition
  relation, the mapping registry or the overlay registry changes in a way that
  could move the no-stall check (re-run it — it is cheap and exhaustive); if Marc
  rules on promoting the objective-verb set into the relation (§3).
