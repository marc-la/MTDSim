---
status: open
created: 2026-07-28
---

# Make the attacker cost-sensitive — a declared per-tactic benefit against its already-declared cost, entering routing as a rationality exponent whose zero recovers today's model exactly

**Chain position: wave 5, after the attacker-state seam (SHIPPED 2026-07-28 —
`docs/implementation/pipeline/ogasp/attacker_state_seam.md`).** Needs the seam's
modulator composition. Consumes the cost ledger from
`2026-07-28_axis_measurement_suite.md`, which is the criterion's stated prerequisite for
any claim on this axis. Independent of the learning and stealth handoffs.

## State of play

**The axis, and why the model scores zero on it today.** Cho et al. model the sophisticated
attacker as "a rational actor that is sensitive to incentives, such as attack success with
minimum cost", and name the asymmetry as their third under-developed dimension: the
rational-actor framing is applied to defenders and seldom to attackers. Every model in the
cross-section scores negative on it. This model adds nothing: the transition weights are
flow-proportion frequencies — evidence of what campaigns did, not a cost/benefit
calculation — and the outcome overlay is a declared policy, not a utility. The RoA-ordered
exploit selection survives inside the inherited action layer, so the model inherits exactly
the partial credit the lit review gives Brown and Tay, which that review calls **rationality
without capability**: a defender-computed ordering the attacker optimises without being
able to sequence, adapt, or remember.

**Why it matters for the thesis, not just for the rubric.** MTD's economic argument *is*
raising attacker cost. It is only measurable against an attacker that has a cost model and
conditions decisions on it. Every result this project has produced so far measures MTD's
effect on an attacker to whom cost is invisible — which means the evaluation cannot see the
mechanism MTD's own literature claims.

**The criterion's ruling, and what has changed under it.** §(d) axis 6 says a cost ledger is
the prerequisite measurement, and that a claim additionally needs a decision rule consuming
it, "which is model change beyond the S2 freeze — explicitly not recommended now". Two
things soften that. The ledger is now scoped and costed (the measurement suite handoff), and
the seam handoff supplies a decision rule that lives entirely in the movement layer with a
null configuration identical to today — which is the form of model change the S2 reasoning
was not written against. That argument is the seam handoff's to make; this handoff inherits
it and must not re-litigate it.

**The evidence available, which is better than expected on mechanism and thin on
magnitude.** Four things exist and should be used in this order:

- **FlipIt** (via `docs/sources/extractions/persistence_reset_models.md`) gives a citable
  attacker cost/benefit *mechanism*: each player's benefit is the fraction of time
  controlling the resource minus the average move cost, and at the periodic-game equilibrium
  **the player with the higher move cost has benefit zero**. It is already mapped onto two
  tactic profiles. This is the literature anchor for "cost is decisive to an attacker", and
  it is a much stronger citation than a general appeal to rationality.
- **RoA / RoAC** already exists in the lineage — Ho 2024 defines return on attack cost as
  reward over attack cost with **cost defined as time to exploit**. Framing the new factor
  as the attacker-side, tactic-granularity analogue of a metric the substrate already
  computes defender-side is the cleanest positioning move available, and it converts the
  lit review's "rationality without capability" line into a claim this model answers.
- **MAL / coreLang** is the published precedent for assigning each attack step a declared
  probability distribution for the effort to complete it — the formal shape of a per-step
  cost catalogue, already named in a tactic profile as the precedent to follow.
- **Maleki 2016**, via the privilege-escalation profile, gives the one row directly linking
  attacker expenditure to outcome: MTD-defeat probability rises with attacker time and cost.

What does **not** exist anywhere in the corpus: a per-tactic cost magnitude, an attacker
utility fitted to CTI, or any decision rule consuming one. The one effort-allocation datum
is Carroll 2014's "reconnaissance ≈ 45 % of attacker effort", which is a sanity check, not a
parameter.

**The cost half is already declared.** `data/ogasp/tactic_durations.json` is a per-tactic
cost catalogue in everything but name — declared, tiered, sweep-banded, and already the
subject of a completed sensitivity study. Reusing it as the cost term means the new declared
family is only the *benefit* term, which roughly halves what has to be defended.

## Recommended approach

**1. The factor.** Introduce a utility modulator on the seam:

```
    m(a→b)  =  u(b) ^ λ        where    u(b) = benefit(b) / cost(b)
```

normalised across the source's out-set before it multiplies, so `λ` scales a ratio and not
an absolute magnitude. `λ` is the **rationality exponent**: at `λ = 0` the modulator is
identically 1 and the model reproduces today exactly; as `λ` rises the attacker
increasingly prefers moves with better payoff per unit cost. The current model is therefore
the `λ = 0` special case of the new one, which gives the ablation for free and makes the
comparison honest.

**2. The cost term — reuse, do not re-declare.** `cost(b)` is the tactic's declared duration
from the catalogue. Two details: `resource-development` is declared 0.0 (an immediate
transition), so the ratio needs a floor rather than a division by zero — declare the floor,
do not clamp silently. And the durations are already swept, so the cost half of this factor
inherits a sensitivity verdict instead of needing a fresh one.

**3. The benefit term — the one new declared family, and keep it small.** Fifteen values,
rule-generated from a stated model, never hand-set per tactic. The defensible rule is
**objective proximity within the profile**: a tactic in the profile's own objective set
carries the highest benefit, and benefit falls with consensus-lifecycle distance from it.
Two constraints on the rule:

- **It must not restate the distance kernel.** The routing weights already grade a
  transition by how far it travels; if benefit does the same thing again the model
  double-counts distance and the factor is not measuring incentive at all. Benefit is a
  property of the **destination relative to this profile's objective**, not of the jump.
  Make that distinction explicit and check it: benefit should differ between profiles for
  the same tactic, which the distance kernel never does.
- **It must be per-profile**, because objective sets are per-profile — `infrastructure_setup`
  contains no exfiltration or impact node at all, so a benefit model keyed on a universal
  objective would be meaningless there.

Tier it honestly as declared judgement, give it a scrutiny record, and give it a generator
that reproduces the table — the same three requirements every declared family in this
project meets.

**4. Sweep `λ`, and never fit it.** This is where the axis is most exposed. A cost-sensitive
attacker that gets further is a nicer result, and choosing `λ` because of that is exactly
the reverse-engineering the declared-value guardrails forbid. Declare the band from what the
parameter means — `λ = 0` is indifference, `λ = 1` is proportional-to-utility, large `λ` is
near-greedy and should be shown to collapse traversal diversity — commit the conclusions
before any output exists, and report held/moved per conclusion in the established shape.

**5. Report the result that actually answers the RQ.** The interesting question is not
whether a cost-sensitive attacker performs better. It is whether **MTD's measured effect
changes when the attacker can see cost**. MTD raises the cost of some tactics and not others
— an interrupted action pays the confusion penalty and produces nothing — so a cost-sensitive
attacker should shift its action mix away from the tactics MTD is taxing. If it does, the
project has an economic MTD result that no attacker in the cross-section could have produced.
If it does not, that is a finding about how coarsely MTD's costs are distributed on this
substrate. Design the reporting around that contrast, not around the attacker's score.

**6. Keep the claim exactly as large as the evidence.** What this builds is an attacker that
is rational **over its own declared beliefs about cost and benefit** — a rationality *shape*,
not a calibrated utility. It answers Cho's asymmetry and it does not claim the utility is a
real adversary's. The envelope-not-actor framing does the work here, as everywhere else.

**Alternatives considered.** *Lift the substrate's RoA into the attacker's routing directly*
— attractive because it is already computed, but it is a defender-computed per-host ordering
inside the action layer, keyed on hosts and vulnerabilities rather than tactics, and reaching
into it would put substrate quantities in the portable layer, which is the boundary S3-R was
careful to draw in the opposite direction. Cite RoA as the positioning precedent, do not
consume it. *A full game-theoretic solve (FlipIt-style equilibrium over the tactic net)* —
rejected: out of scope by project direction, and the extraction that carries FlipIt already
records the apparatus as out of scope while the mechanism is usable. *An additive utility
bias rather than a multiplicative exponent* — rejected for the same reason the overlay design
rejected additive bias: it can invert the grounded ordering and needs an arbitrary clamp.
*A cost ledger with no decision rule* — that is not an alternative, it is the measurement
suite's deliverable, and on its own it leaves the axis at NOT ADDRESSED because nothing
consumes it.

## Validation gate

Done when:

1. `λ = 0` reproduces the current record stream field for field, on all five profiles and
   several seeds, both MTD conditions.
2. The benefit model is rule-generated with a `--check`-style regeneration that reproduces
   every value, and it is shown to **differ between profiles for at least one tactic** —
   the check that it is measuring objective proximity and not re-deriving lifecycle distance.
3. The cost ledger from the measurement suite is reported per run and per arm, so the thing
   the attacker is now optimising is externally visible.
4. `λ` is swept over its declared band with conclusions committed beforehand and
   per-conclusion held/moved verdicts.
5. The action-mix contrast is reported: how the distribution over tactics differs between
   `λ = 0` and the declared `λ`, with and without MTD. This is the result the axis exists to
   produce.
6. Traversal diversity is reported at both ends of the `λ` band, so the axis-3 trade is
   visible rather than incidental.
7. A tracked record and a declared-value ledger entry; the criterion's axis 6 re-scored only
   if the pre-registered criterion was met, and DESIGNED is the honest badge for a mechanism
   that runs without changing an outcome.

## Hard constraints

- **`λ = 0` is bit-identical to today.**
- **The benefit family is declared, tiered, rule-generated and swept** — never chosen because
  it improves an outcome. This axis is the most tempting place in the project to fit a value,
  and the guardrail against reverse-engineering from the conditioned layer applies in full.
- **Reuse the duration catalogue as the cost term.** Do not declare a second cost family; a
  parallel cost catalogue that could drift from the durations is worse than no cost model.
- **No substrate change**, and do not consume the substrate's RoA computation inside the
  portable layer.
- **The claim is a rationality shape over declared beliefs**, not a calibrated utility, and
  not a claim about any real adversary. Envelope, not actor.
- Determinism / SIM-05 — the modulator is a pure function of declared data and the current
  place, so it should need no RNG at all.
- Within-substrate comparability only; Australian English; branch and commit rules from
  [`../workflows/session_workflow.md`](../workflows/session_workflow.md); never push.

## Reading list

- `docs/implementation/apt_model_criterion.md` §(d) axis 6 — the axis, the "rationality
  without capability" diagnosis, and the M8b prerequisite this handoff discharges.
- `docs/implementation/pipeline/ogasp/attacker_state_seam.md` — the mechanism and the S2
  argument this inherits (SHIPPED 2026-07-28): the modulator `Π_m` composition, the
  multiplicative-not-additive and zero rules, and §7's written-out S2 case for Marc.
- `docs/sources/extractions/persistence_reset_models.md` — FlipIt's benefit equation and the
  higher-move-cost-player-gets-zero equilibrium; the mechanism citation.
- `docs/sources/extractions/ho2024.md` — RoAC with cost defined as time to exploit; the
  positioning precedent already inside the lineage.
- `data/ogasp/tactic_durations.json` — the cost term, its tier badges and its sweep bands,
  and the `resource-development` zero that needs a declared floor.
- `docs/implementation/declared_value_provenance.md` — the three requirements and §5's
  guardrails, which govern the benefit family.

## Out of scope (explicitly)

- Any game-theoretic solve or equilibrium analysis. FlipIt supplies a mechanism to cite, not
  an apparatus to build.
- A second cost catalogue, or any change to the durations.
- Consuming or modifying the substrate's RoA machinery.
- Learning and stealth modulators — same seam, different handoffs.
- Building the cost ledger; that is the measurement suite's deliverable and this consumes it.
- Dissertation prose.
