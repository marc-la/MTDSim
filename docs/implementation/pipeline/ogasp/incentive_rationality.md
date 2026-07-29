---
status: durable
created: 2026-07-29
topic: "Criterion axis 6 (incentive-driven rationality) — the attacker utility modulator: a declared per-tactic benefit over the already-declared duration catalogue, entering routing as a rationality exponent whose zero recovers today's model exactly. Records the model, the one new declared family and why it is not a restatement of the distance kernel, the pre-registered sweep conclusions, and the honest size of the claim."
updated: 2026-07-29
---

# The attacker utility modulator — design, declared values, and the pre-registered sweep (axis 6)

**Status:** durable design-and-build record. It ships the first modulator with a
declared value on the attacker-state seam
([`attacker_state_seam.md`](attacker_state_seam.md)), and it consumes the cost
ledger from [`measurement_suite.md`](measurement_suite.md), which the criterion
names as the prerequisite measurement for any claim on this axis. It discharges
the handoff `2026-07-28_axis6_incentive_rationality.md`.

**The governance question is the seam's, and it is still open.** The seam record
§7 asks Jin to confirm that a within-run, movement-layer, null-equivalent
attacker state is refinement of the movement layer under M7 rather than the
attacker-state change S2 defers. This build inherits that argument and does not
re-litigate it. What is safe to *build* under the null-equivalence guarantee is
built here; what is gated on the confirmation is wiring a non-zero λ into a
reported experiment.

## 1. The axis, and what the model scored before this

Cho et al. model the sophisticated attacker as "a rational actor that is
sensitive to incentives, such as attack success with minimum cost", and name the
asymmetry as an under-developed dimension: the rational-actor framing is applied
to defenders and seldom to attackers. Every model in the criterion's
cross-section scores negative on it, and this one added nothing — the movement
layer's transition weights are flow-proportion frequencies (evidence of what
campaigns did, not a cost/benefit calculation) and the outcome overlay is a
declared policy, not a utility. The RoA-ordered exploit selection survives inside
the inherited action layer, so the model inherited exactly the partial credit the
lit review gives Brown and Tay, which that review calls **rationality without
capability**: a defender-computed ordering the attacker optimises without being
able to sequence, adapt, or remember.

Why it matters beyond the rubric: MTD's economic argument *is* raising attacker
cost, and that is only measurable against an attacker that has a cost model and
conditions decisions on it. Every result this project had produced measured MTD's
effect on an attacker to whom cost was invisible.

## 2. The mechanism

One modulator on the seam. At a routing decision from place `a`, the factor
applied to destination `b` is

```
    m(a→b)  =  ( u(b) / ū )^λ        where    u(b) = benefit(b | profile) / max(cost(b), cost_floor_s)
```

with `ū` the mean utility over the source's out-set. It multiplies the composed
distribution and the composition renormalises, exactly as the seam's §2 rule
specifies — multiplicative, never additive, for the reason the overlay design
won on: multiply-then-renormalise conditions the grounded proportions without
inventing a magnitude or inverting the corpus's within-class ordering.

Three properties of that expression are load-bearing:

- **λ is the rationality exponent, and λ = 0 recovers today exactly.** `x ** 0.0`
  is exactly 1.0 in IEEE arithmetic for any finite positive `x`, so at λ = 0 the
  product is exactly 1 and the arithmetic reduces to the current two-factor rule.
  The current model is therefore the λ = 0 *special case* of this one, which
  gives the ablation for free and makes the comparison honest: the conditioned
  and unconditioned arms differ by one declared parameter, never by wiring. The
  implementation deliberately does **not** special-case zero — the identity is a
  property of the maths, and testing it that way is a stronger claim than
  short-circuiting it.
- **Normalising by the out-set mean is what makes λ scale a ratio** rather than
  an absolute magnitude. It is behaviourally free (the composition renormalises,
  so any common rescaling cancels); it is there for the parameter's meaning and
  for the legibility of the state's per-decision log, where a factor then reads
  as "how much this destination beat the local average".
- **No factor can reach zero.** Benefit is `rho^(1+gap)` with `0 < rho < 1` and
  cost is floored above zero, so utility is strictly positive. The seam's stall
  rule — a modulator may not return 0.0 without declaring `may_zero` and re-running
  the no-stall check — is therefore never engaged, and the modulator can suppress
  an out-edge's share but never remove it. This is asserted over every profile's
  every out-set at both ends of both declared bands, not argued.

**Determinism (SIM-05).** The factor is a pure function of declared data and the
current place: it reads no history off the state and draws from no random stream,
so the seam's fourth RNG stream is left untouched and a conditioned run
reproduces exactly.

## 3. The cost term — reused, not re-declared

`cost(b)` is the tactic's declared duration from
[`tactic_durations.json`](../../../../data/ogasp/tactic_durations.json). This is
a deliberate reuse rather than a new family: a parallel cost catalogue that could
drift from the durations would be worse than no cost model at all, and reusing
the catalogue means this factor's cost half inherits the durations' tier badges
and their already-completed sensitivity sweep instead of needing a fresh one.
The positioning is the cleanest available: Ho 2024 defines return on attack cost
as reward over attack cost with **cost defined as time to exploit**, so time is
the cost term the lineage already uses — this is its attacker-side,
tactic-granularity analogue.

**The declared floor, and why it is not 1.0.** `resource-development` is declared
`duration_s = 0.0`, so the ratio needs a floor. The floor is a **named declared
parameter** (`cost_floor_s`), reported in the compiled view and in the sweep
design, never a silent `max()` buried in the modulator. Its value follows from
what the catalogue's zero *means*: the tactic's real effort — weeks to months of
tool and infrastructure preparation — happens **off the simulator's clock**, not
for free. A floor chosen to make an un-metered tactic read as costless would
invert exactly the quantity this axis exists to model. The floor is therefore set
at the cheapest *metered* action in the catalogue, the exploit-shaped anchor at
**4.5 s**, so an un-metered tactic reads as no cheaper than the cheapest thing
the simulator does price. The band brackets that between the naive reading of the
zero (1.0 s, effectively free) and the low-and-slow anchor (45.0 s).

The floor is expected to be load-bearing — it alone decides whether the off-clock
tactic sits at the top or the middle of the utility ordering — which is why it is
swept rather than merely declared. That expectation is pre-registered below as
conclusion C6.

## 4. The benefit term — the one new declared family

Fifteen values per profile, rule-generated from a stated model, never hand-set
per tactic. The rule is **objective proximity within the profile**:

- `objective` — a tactic in the profile's own declared objective set carries the
  unit of benefit, 1.0;
- `instrumental` — every other tactic is instrumental, worth `rho^(1 + gap)`,
  where `gap` is the minimum number of consensus lifecycle stages separating it
  from the profile's nearest objective. The `+1` is structure, not a magnitude:
  even a same-stage non-objective sits one decay step below the objective it
  serves, because value accrues *at* the objective.

`gap` is unsigned on purpose — proximity to an objective is a distance, and a
tactic seated past the objective's stage is no closer to achieving it than one
seated the same separation before it.

Every input is read from its own home rather than restated: the objective sets
from the GASP class-semantic declarations (`petri/analysis.OBJECTIVE_TACTICS`),
the stage ordering from
[`lifecycle_consensus.json`](../../../../data/ogasp/controller/lifecycle_consensus.json),
the cost from the duration catalogue.

### 4.1 Why this is not the lifecycle-distance kernel wearing a hat

The most serious design risk on this axis: the routing weights **already** grade
a transition by how far it travels, and if benefit does the same thing again the
model double-counts distance and this factor is not measuring incentive at all.
Two properties separate them, and both are regression-guarded in the test suite
rather than argued in prose:

| | outcome overlay's distance kernel | this benefit family |
|---|---|---|
| what it grades | the **jump**: a signed source→destination stage offset | the **destination**, relative to this profile's objective |
| depends on the source | yes, necessarily | **no** — the utility of arriving at `b` is one number whatever `a` was |
| varies between profiles | **no** — identical for all five | **yes** — that is the whole point |

The sharpest case is `command-and-control`: benefit 1.0 under
`infrastructure_setup`, whose declared objective it *is*, and 0.25 under
`pure_steal`, where it is merely instrumental. `impact` inverts between the two
single-objective profiles the same way. The kernel cannot express either, because
it never sees which profile is walking.

Per-profile is also a necessity, not a refinement: `infrastructure_setup`
contains no exfiltration or impact node at all, so a benefit model keyed on a
universal objective would be meaningless there.

### 4.2 Tier, honestly

Every value in this family sits at **`declared-judgement`** — the honest floor
tier of [`declared_value_provenance.md`](../../declared_value_provenance.md) §2.
No source in the corpus assigns a per-tactic benefit. What the literature
supplies is a *mechanism* and not a magnitude:

- **FlipIt** (via [`persistence_reset_models.md`](../../../sources/extractions/persistence_reset_models.md))
  gives the citable cost/benefit mechanism — each player's benefit is the
  fraction of time controlling the resource minus the average move cost, and at
  the periodic-game equilibrium **the player with the higher move cost has
  benefit zero**. This is the anchor for "cost is decisive to an attacker", and
  a far stronger citation than a general appeal to rationality.
- **RoA / RoAC** ([`ho2024.md`](../../../sources/extractions/ho2024.md)) is the
  positioning precedent already inside the lineage, cited and deliberately **not
  consumed** — see §7.
- **MAL / coreLang** is the published precedent for assigning each attack step a
  declared distribution for the effort to complete it.
- **Maleki 2016** gives the one row linking attacker expenditure to outcome:
  MTD-defeat probability rises with attacker time and cost.

None of these fixes a number. Because the tier is the floor tier, the **sweep,
not the argument, is what these values' defence rests on** — and unlike the
outcome overlay, which carries review rounds R0–R4, this family has had **no
adversarial cross-examination round at all**. That gap is stated in the ledger
rather than implied, and a cross-examination round is the obvious next
maintenance step.

### 4.3 The three requirements, discharged

The declared-value precedent asks that a declared family be reproducible, tiered
and scrutinised.

1. **Reproducible.** The table is rule-generated by a tracked generator,
   `mtdsim.l3_simulation.movement.utility`, with `--write` / `--check` mirroring
   the overlay compiler's contract: **0 of 75 cells differ** between a fresh
   compilation and what is committed, checked in the test suite rather than by an
   in-session script. Coverage is complete — every seated tactic under every
   profile, including tactics a profile's net has no place for, because the
   declared layer authors the whole space and the data layer decides which cells
   route mass.
2. **Tiered.** §4.2; every entry `declared-judgement`, stated as such.
3. **Scrutinised.** §5's sweep, with the conclusions committed before any output
   existed. The absent cross-examination round is recorded as the gap it is.

## 5. The pre-registered sweep — conclusions committed before the numbers

**This section was written and committed before the sweep was run.** The git
history is the audit trail; `data/results/axis6_rationality/run_sweep.py` carries
the same conclusions and criteria, and `analyse.py` computes a held/moved verdict
per conclusion from the rows rather than asserting one.

This is where the axis is most exposed. A cost-sensitive attacker that gets
further is a nicer result, and choosing λ because of that is exactly the
reverse-engineering the declared-value guardrails forbid
([`declared_value_provenance.md`](../../declared_value_provenance.md) §5). So λ's
band is declared from what the parameter *means* — λ = 0 is indifference, λ = 1
is preference proportional to normalised utility (the canonical rational-actor
reading and the only value in the band whose interpretation is not arbitrary),
and large λ is near-greedy — and the conclusions are fixed in advance.

**Design.** Nine sweep points (λ ∈ {0, 0.5, 1, 2, 4}; then `rho` and
`cost_floor_s` one at a time at the declared λ = 1), five profiles, both MTD
conditions, both controller mappings, ten seeds — matching experiment 1 and the
S1 sweep exactly, so the verdicts speak to the recorded findings rather than to a
differently-shaped experiment. The inherited baseline attacker rides along so the
cost ledger is reported per *arm* and not only per profile. Two limits are stated
in advance: the study is **not powered** for any ranking of MTD mechanisms under a
cost-sensitive attacker (that is experiment 2's defence-family sweep), and **no
conclusion rests on ASR**, which discriminates nothing at the 200 s operating
interval per the rate feasibility study's degenerate-region finding.

| | Conclusion | Criterion |
|---|---|---|
| **C1** | The ablation is exact | at λ = 0 the record stream is field-for-field identical to a run with no modulator; zero differing runs |
| **C2** | The mechanism is live | pooled visit-distribution JSD between λ = 0 and λ = 1 exceeds 0.01 on ≥ 3 of 5 profiles, in **both** MTD conditions |
| **C3** | Rising λ collapses traversal diversity (the axis-3 trade, shown not assumed) | mean per-run path entropy at λ = 4 below λ = 0 with disjoint 95 % intervals, on ≥ 3 of 5 profiles |
| **C4** | The action-mix shift is **larger under MTD** — the result the axis exists to produce | JSD(λ=0, λ=1 \| MTD) > JSD(λ=0, λ=1 \| no MTD) on ≥ 3 of 5 profiles |
| **C5** | Cost sensitivity does **not** buy progress | no statistic among {distinct hosts, deepest successful stage, distinct places} shows a CI-separated monotone increase across λ on a majority of profiles |
| **C6** | The declared cost floor is load-bearing | action-mix JSD across the `cost_floor_s` band exceeds that across the `rho` band, on ≥ 3 of 5 profiles |

Two of these deserve their reasoning stated, because their direction is the
guardrail:

- **C4 is the question, and C5 is the trap.** The interesting question is not
  whether a cost-sensitive attacker performs better; it is whether **MTD's
  measured effect changes when the attacker can see cost**. MTD raises the cost
  of some tactics and not others — an interrupted action pays the confusion
  penalty and produces nothing — so a cost-sensitive attacker should shift its
  action mix away from the tactics MTD is taxing. If C4 holds, the project has an
  economic MTD result no attacker in the criterion's cross-section could have
  produced. **If it moves, that is a finding about how coarsely MTD's costs are
  distributed on this substrate**, and it is reported as that rather than
  softened.
- **C5 is committed in the direction that would embarrass a flattering result.**
  "The attacker gets further" is the outcome most tempting to reach for, so the
  pre-registration says it is not expected. A held C5 means the mechanism is not
  being sold on a performance gain it was never entitled to claim.

*(Results and per-conclusion verdicts: §6, added by the commit that ran the
sweep.)*

## 6. Results

*(Pending at this commit — the sweep had not been run when §5 was written. This
is the pre-registration boundary.)*

## 7. Alternatives considered and rejected

- **Lift the substrate's RoA into the attacker's routing directly.** Attractive
  because it is already computed, but it is a *defender-computed* per-host
  ordering inside the action layer, keyed on hosts and vulnerabilities rather
  than tactics; reaching into it would put substrate quantities in the portable
  layer, which is the boundary S3-R was careful to draw in the opposite
  direction. RoA is cited as the positioning precedent and deliberately not
  consumed.
- **A full game-theoretic solve (FlipIt-style equilibrium over the tactic net).**
  Out of scope by project direction, and the extraction that carries FlipIt
  already records the apparatus as out of scope while the mechanism is usable.
- **An additive utility bias rather than a multiplicative exponent.** Rejected
  for the reason the overlay design rejected additive bias: it can invert the
  grounded ordering and needs an arbitrary clamp.
- **A second cost catalogue.** Rejected in favour of reuse — see §3.
- **A cost ledger with no decision rule.** Not an alternative: that is the
  measurement suite's deliverable, and on its own it leaves the axis NOT
  ADDRESSED because nothing consumes it.

## 8. The size of the claim

What this builds is an attacker that is rational **over its own declared beliefs
about cost and benefit** — a rationality *shape*, not a calibrated utility. It
answers Cho's asymmetry; it does not claim the utility is a real adversary's, and
it is not a claim about any real adversary at all. Envelope, not actor, as
everywhere else in this project.

Three limits travel with any use of it:

- the benefit family is `declared-judgement` throughout and has survived no
  adversarial review round yet (§4.2);
- the cost term is the duration catalogue, whose own tiers are mixed and whose
  scale is *shape-not-scale* — the utility ratio inherits both;
- λ is declared and swept, never fitted, and the swept band is the defence.

## 9. What this does not do

- **No substrate change.** Every line is under `src/mtdsim/l3_simulation/`; the
  literal MTDSim code is untouched, and the substrate's RoA machinery is neither
  consumed nor modified.
- **No change to the durations**, no second cost family.
- **No cross-run memory.** The modulator does not even use the within-run state —
  it is a pure function of declared data and the current place.
- **No badge moved on the criterion** unless the pre-registered criterion was
  met; see §6 and [`../../apt_model_criterion.md`](../../apt_model_criterion.md)
  §(h).
