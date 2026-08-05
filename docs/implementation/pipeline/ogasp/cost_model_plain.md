---
status: durable
created: 2026-08-01
updated: 2026-08-01
topic: "The attacker's cost model in plain terms (Part 1 of the rational-attacker handoff): what is computed at each routing decision, where every number comes from, a worked decision with real values — the simplification verdict against the handoff's three questions with the reproduction evidence, and (§2.2a) the double-penalty defect the verdict does not answer"
---

# What the cost-sensitive attacker computes — the plain statement, and the simplification verdict

**Status:** companion to
[`incentive_rationality.md`](incentive_rationality.md), which argues the
mechanism to an examiner. That record establishes *why* each piece is
defensible; nothing in it states in one place what the attacker actually
computes and where each number comes from, which is what §1 here does. §2 then
judges the simplification questions the rational-attacker handoff poses, with
the evidence for each answer. Nothing here changes the mechanism; §2's verdict
is to keep it as built, for reasons that are now shown rather than argued.

## 1. The plain statement

**When it happens.** The movement attacker walks a campaign structure: it
occupies one tactic (say, *collection*), spends time there, and must choose
which tactic to try next from the handful its campaign structure allows. The
cost model acts at exactly that moment — every routing decision, and nowhere
else. It does not change what a tactic does, how long it takes, or what the
simulator rules about success; it only changes *where the attacker prefers to
go*.

**What the attacker computes.** Each candidate next-tactic arrives at the
decision with a weight already set by two inherited factors: how often the
observed campaigns made that move (the base weight), adjusted by the declared
success/failure routing policy (the outcome overlay). The cost model multiplies
each candidate's weight by one more number, built in three steps:

1. **How good a deal is this tactic?** `u = benefit ÷ cost`. Benefit is how
   directly the tactic serves *this profile's own* objective; cost is how long
   the tactic is declared to take, in simulated seconds.
2. **Relative to what is on the menu.** Divide `u` by the average `u` of the
   candidates at this decision. A tactic that is twice as good a deal as the
   local average scores 2; a below-average deal scores under 1.
3. **How much the attacker cares — the rationality exponent λ.** Raise that
   ratio to the declared power λ. At λ = 0 every factor becomes exactly 1 and
   the attacker is cost-blind — bit-identical to a run with no cost model at
   all. At λ = 1 preference is proportional to the relative deal. At λ = 4 the
   attacker is near-greedy: the best deal on the menu swamps everything else.

The adjusted weights are renormalised and the next tactic is drawn. That is the
whole mechanism: one multiplier per candidate, `(u ÷ menu average)^λ`,
recomputed at each decision from declared data only. It looks at nothing that
has happened in the run — no memory, no learning, no view of the defence.

**Where every number comes from.**

| Quantity | Value | Source |
|---|---|---|
| `cost` per tactic | 4.5 s for the four exploit-shaped tactics (initial-access, privilege-escalation, credential-access, lateral-movement); 22.5 s for execution and defense-impairment; 35 s for the two scan tactics; 36 s for the three objective acts (collection, exfiltration, impact); 45 s for the low-and-slow three (persistence, stealth, command-and-control) | the declared per-tactic duration catalogue ([`tactic_durations.json`](../../../../data/ogasp/tactic_durations.json)) — the same numbers the simulator already uses as each tactic's mean dwell. Reused, never re-declared, so the cost term cannot drift from the time the simulator actually charges |
| the cost floor | 4.5 s | resource-development is declared 0 s because its real effort (weeks of preparation) happens off the simulator's clock — not because it is free. The ratio cannot divide by zero, so its cost is clamped up to the cheapest *metered* action. A declared, swept parameter (`cost_floor_s`), and the sweep confirmed it load-bearing (C6) |
| `benefit` per tactic, per profile | 1.0 at the profile's own declared objective; otherwise halved once, then halved again per lifecycle stage between the tactic and the nearest objective (decay ρ = 0.5) | rule-generated, never hand-set: objectives from the GASP class semantics, stage seats from the published-lifecycle consensus ordering ([`lifecycle_consensus.json`](../../../../data/ogasp/controller/lifecycle_consensus.json)); compiled table at [`attacker_utility_benefit.json`](../../../../data/ogasp/attacker_utility_benefit.json), reproduced 0-of-75-cells-differ by the tracked generator |
| λ | 1.0 declared | the only value in the band whose reading is not arbitrary (preference proportional to relative utility); swept over {0, 0.5, 1, 2, 4} with conclusions pre-registered. Every declared value here sits at the honest floor tier (declared-judgement) — the sweep, not an argument, is the defence |

**One real decision, worked.** The data-theft profile (`pure_steal`) sits at
*collection*. Its menu, with real numbers:

| candidate | base weight | benefit | cost (s) | u = b ÷ c | factor at λ = 1 | resulting share (λ = 1) |
|---|---|---|---|---|---|---|
| exfiltration (the objective) | 0.571 | 1.0 | 36.0 | 0.0278 | 1.18 | 62 % |
| command-and-control | 0.286 | 0.25 | 45.0 | 0.0056 | 0.24 | 6 % |
| credential-access | 0.143 | 0.25 | 4.5 | 0.0556 | 2.35 | 31 % |
| stealth | 0.000 | 0.25 | 45.0 | 0.0056 | 0.24 | 0 % |

The menu average utility is 0.0236. Exfiltration is a slightly-above-average
deal (worth the most, but expensive), so its share barely moves (57 % → 62 %).
Credential-access is the standout deal — a quarter of the benefit at an eighth
of the cost — and more than doubles its share (14 % → 31 %). Command-and-control
is an expensive low-payoff detour and collapses (29 % → 6 %). At λ = 4 the same
numbers give credential-access factor 30.7 and about 80 % of the share: the
greedy attacker abandons its own objective's neighbourhood to farm the cheap
tactic. This one decision *is* the sweep's headline in miniature — see below.

**What the sweep found, honestly.** Three things, recorded in full in
[`incentive_rationality.md`](incentive_rationality.md) §6. The mechanism is
live and behaves exactly as designed: the attacker visibly moves its effort
onto the cheap exploit-shaped tactics and off the expensive low-and-slow ones,
and by λ = 4 traversal diversity collapses (pooled path entropy 2.23 → 0.24
bits). It does **not** produce the result the axis exists for: MTD's measured
effect is unchanged when the attacker can see cost, because on this substrate
MTD's tax is levied in near-proportion to a tactic's declared dwell (a roughly
uniform ~9 % surcharge) and a *normalised ratio* cannot see a proportional
inflation of its denominator. And cost-sensitivity *costs* the attacker
progress: blocked attempts rise from 49 % to 99 % of actions across the band,
because the cheapest tactics on this substrate are precisely the most
precondition-coupled — the attacker that optimises declared cost optimises its
way into a wall. **Read that last sentence under §2.2a**, which records why the
wall may be a property of the denominator rather than of the terrain: the
enabling tactics are penalised by both terms at once, and neither can represent
instrumental necessity.

## 2. The simplification, judged

The handoff poses three questions. Each is answered with evidence, not
preference; the net verdict is that the mechanism is already at its simplest
defensible form, and the one component that looked like excess complexity — the
graded benefit family — was tested for removal and shown to be load-bearing.

### 2.1 Is the benefit family carrying its weight? — Yes, shown by attempted removal

The suspicion was legitimate: the family is 75 declared cells at the floor
provenance tier, and the sweep found its own shape parameter (ρ) the *less*
influential of the two declared magnitudes (C6). So the simplification was
actually attempted, as a pre-registered reproduction check
(`data/results/axis6_rationality/simplify_benefit_check.py`): replace the
graded family with binary objective-membership — benefit 1.0 at the profile's
own objectives, 0.5 (the declared ρ, one decay step, fixed in advance)
everywhere else — and require the pooled visit-distribution JSD between the
graded and binary attackers to stay under 0.01, the same bar the sweep used to
certify the mechanism live, in every mapping × profile × condition cell at
λ = 1 and λ = 4. One thousand fresh runs (600 graded across λ ∈ {0, 1, 4},
400 binary), ten seeds per cell, both mappings, both MTD conditions.

**The binary family does not reproduce: 31 of 40 cells exceed the bar** (15 of
20 at the declared λ = 1, 16 of 20 at the band end; median JSD 0.018, maximum
0.180). By the sweep's own standard, a swap that moves the distribution by more
than the liveness bar is a different live mechanism, not a reparameterisation.
And the direction of the difference is exactly the property the family exists
to encode. At the declared λ the binary attacker re-inflates the early-stage
tactics the proximity rule discounts — initial-access, reconnaissance and
execution each gain two to five points of visit share in nearly every failing
cell — and drains the objective's neighbourhood (exfiltration, collection,
command-and-control and defense-impairment each lose two to five points under
the profiles that own them). Removing the stage-gap term removes the tilt
toward the campaign's own goal; what is left prefers cheap tactics wherever
they sit in the lifecycle, which is a cost model with no campaign in it. The
per-profile pattern seals the diagnosis: the one profile that reproduces in
all eight of its cells is `infrastructure_setup` (JSD 0.0003–0.0098), whose
objective sits mid-lifecycle so every stage gap is small and the grading is
nearest to flat by construction — exactly where the rule predicts the gap term
has the least to do. The strongest divergence is `double_extortion`'s (JSD up
to 0.18 at λ = 4, its walk reshaped wholesale), the profile the sweep already
records as this family's outlier (C4, C6). The family's complexity is doing
measurable, profile-specific work precisely where its rule says it should.

Two honest riders. First, the sweep's headline *negative* is robust to the
family's shape: the binary arm still shows the shift onto cheap tactics, the
entropy collapse, the blocked-fraction rise, and no MTD-conditional shift — so
no recorded conclusion depended on the grading. Second, this check is the
family's first adversarial cross-examination round (the gap §4.2 of the design
record states openly), and it is logged as such in the value ledger
(`attacker_utility.json`).

**A finding from the check's freshness gate, recorded because it outranks the
check.** The check first tried to reuse the 2026-07-29 sweep rows and found
they no longer reproduce on today's substrate: two ruled fixes landed after
those rows were captured (`6181305`, the intent-audit dispositions, 16:08 that
day; `816b300`, the MTD instance-registration fix, 18:53), and together they
move most MTD-arm rows and a minority of no-MTD rows. Both arms of this check
were therefore run fresh, and the fresh graded arm doubles as a re-verification
of the recorded sweep on the current substrate: every qualitative verdict
reproduces — entropy collapse in all ten profile × mapping cells, blocked
fraction rising to ~99 % at the band end (ledger means 263 → 2 196 attempted,
126 → 2 165 blocked, 1.26 → 0.12 hosts), and the MTD-conditional shift absent
within ±15 % on eight of ten cells with `double_extortion` again the exception.
The recorded sweep's magnitudes describe the pre-fix substrate; its
conclusions survive on the current one.

### 2.2 Should cost stay as declared duration? — Yes *for this pass*, and the scope of that answer is narrower than first written

> **Corrected 2026-08-01, on Marc's objection, and the correction is
> load-bearing.** This subsection was written to answer the handoff's second
> question as posed — which framed the cost term as the reason MTD's measured
> effect did not change (C4) — and the three grounds below address exactly
> that. They do **not** establish that declared duration is a defensible model
> of attacker cost, and the verdict was presented as though they did. The
> ground that actually carries the "keep it" decision is the third one, which
> is a **scope** argument (a realised-outcome cost is a different capability,
> under freeze) rather than a claim that time is the right denominator. Read
> §2.2a first; it states the defect the three grounds do not answer.

### 2.2a The defect the verdict does not answer — instrumental tactics are penalised twice

Pairing **cost = declared duration** with **benefit = objective proximity**
produces a systematic bias that neither term can see, and it falls hardest on
exactly the tactics this substrate makes mandatory.

Reconnaissance is penalised by both terms at once. It is declared at 35 s
against the exploit-shaped tier's 4.5 s, so the denominator makes it nearly
eight times more expensive; and it sits further from any objective than any
other tactic, so the proximity rule gives it the lowest benefit of the fifteen
(0.0625 under `pure_steal`, against credential-access's 0.25). Compounded, the
data-theft profile values reconnaissance at u = 0.0018 against
credential-access's 0.0556 — a **31-fold preference against the tactic that
satisfies the precondition for the tactic it prefers**.

**Neither term can represent instrumental necessity, and that is the whole of
the defect.** Benefit grades proximity to the objective, which is a proxy for
usefulness that fails precisely for enabling steps: a tactic whose entire value
is unlocking a later one scores as though it had no value. Cost grades
duration, which penalises those same enabling steps again for being slow. The
model has no way to express *this tactic is worth its price because of what it
makes possible*, so a sharper λ routes effort away from the enabling steps and
into the tactics that depend on them.

**Consequences for what may be read off the sweep.** The measured behaviour is
not in doubt — discovery's visit share falls while the exploit-shaped tactics
gain (+0.19 credential-access, +0.16 lateral-movement for `pure_steal` at
λ = 1), and blocked attempts rise from 49 % to 99 % across the band. What is in
doubt is the *reading*. §6.2 of the design record and F5 of the fidelity ledger
present this as "an attacker that optimises declared cost optimises its way
into a wall" — experiment 1's coupling finding in economic terms, and therefore
a statement about this substrate. That reading is only available if the
denominator is a defensible model of attacker cost. The competing reading, not
excluded by anything measured, is that the cost term cannot see that fast
tactics have prerequisites, and the attacker's self-defeat is a property of the
**denominator** rather than of rational attackers or of the terrain. Both
records now carry that qualification, and no claim of the form *cost-sensitivity
costs an attacker progress* may be made without it.

**The fix is one build, and it serves two open problems.** The axis-6 M8b field
already names "a utility conditioned on realised success rather than realised
time" as one of two routes to DEMONSTRATED — arrived at from the
MTD-invariance side. It is the same change this defect asks for, arrived at
from the wall side, which is a reason to think it is the right change rather
than a coincidence. The design is worked out in the iterated-cost-model
handoff, whose surviving account is
[`iterated_cost_model.md`](iterated_cost_model.md); it is a mechanism change under
the freeze and a disposition for Marc, not a session's judgement.

> **Built and swept 2026-08-02, and the diagnosis above is confirmed with one
> substantial correction** ([`iterated_cost_model.md`](iterated_cost_model.md);
> 4 200 runs, conclusions pre-registered). The defect is real and repairable
> without a new declared magnitude: the blocked-fraction rise is 73–89 % undone
> in the pooled `v2_partial` cells and successes per attempted action roughly
> double. It was not repaired at the per-profile resolution the pre-registration
> demanded, so its U2 is recorded moved.
>
> **The correction is to this subsection's own emphasis.** The diagnosis says
> both terms fail in the same direction and the penalty compounds, which is
> true — but it reads as though the *denominator* were the primary offender, and
> the two changes were built and swept separately precisely so that could be
> tested. It is not. Repairing the cost term alone **fails**: it raises the
> blocked fraction in half the cells, recovers no compromise breadth, and is the
> only arm to cost path entropy. Repairing the *benefit* term alone — measuring
> distance through the profile's own routing net rather than the lifecycle-stage
> ordering — recovers 36 % of the host loss under MTD, doubles successes per
> action, and costs no plurality at all. The reading that survives is that
> pricing the wall is not enough on its own: an attacker discouraged from the
> unready exploit needs somewhere better to go, and only the numerator can say
> where. **The graph the benefit is measured in was the load-bearing choice**,
> which is not what §2.2a predicted and is recorded here as a correction to it.

### 2.2b The three grounds, as they stand

They answer the question the handoff asked, and they are unaffected by §2.2a
except where noted:

- **It is the honest reuse.** The duration catalogue is the one family of
  per-tactic time values the model declares; a second, cleverer cost catalogue
  could drift from it, and the record already rules that worse than no cost
  model. The lineage precedent points the same way: Ho 2024's return-on-attack
  defines attack cost as *time*, so declared time is the cost term this
  codebase's ancestry already uses.
- **The C4 negative is not the cost term's fault, and changing the term is not
  the cheap route to *that* result.** The reason MTD's effect did not move is
  that this defence's tax is dwell-proportional *at the 200 s operating
  interval* — and experiment 2 §15 then found the condition under which that
  breaks: at the 2 000 s interval four of seven mechanisms tax tactics out of
  proportion to dwell. The cheaper route to the axis's missing result is
  therefore a run at that existing condition (gated on the outstanding S2
  ruling), not a re-engineered cost term. **This ground is about C4 only.** It
  says nothing about §2.2a's defect, which concerns C5 and would not be
  touched by running at a different interval.
- **A realised-outcome cost is a different capability, not a simplification.**
  Conditioning cost on observed outcomes would make the modulator stateful —
  today it is a pure function of declared data, which is what makes its λ = 0
  ablation exact, its determinism trivial, and its factor table precomputable
  (proven by the collapse spike, 30/30 bit-identical). It would also converge
  on the axis-7 learner's territory (the realised-success channel is exactly
  what the learner estimates), and the freeze bars composing the modulator
  families without a fresh comparability argument. The realised-success route
  stays what the record already names it: the successor work, recorded and not
  taken here.

### 2.3 Is the exponent the right control? — Yes, keep it

λ earns its place on three properties nothing simpler retains: its zero is an
*exact* ablation (a property of IEEE arithmetic, tested rather than
special-cased — the hard constraint every change must preserve); its declared
value is the one non-arbitrary point in the band (preference proportional to
relative utility); and its band ends are interpretable (indifference,
near-greedy) so the sweep's conclusions read as statements about rationality
rather than about a tuning knob. The simplification in §2.1 does not make any
alternative control plainer, so the exponent stands.

## 3. What this leaves standing

The hard constraints all hold: λ = 0 remains a bit-identical off-switch; the
cost term remains the single duration catalogue; no declared value was chosen
because of an outcome it produces (the §2.1 check's candidate value was fixed
from the graded family's own declared ρ before any run); the substrate's
return-on-attack machinery remains cited, not consumed; and the freeze holds —
nothing here opens a new attacker capability, and the reported configuration
still runs with modulators null.

## Evidence

- [`incentive_rationality.md`](incentive_rationality.md) — the argued design
  record: mechanism, declared families, pre-registered sweep, results.
- `data/results/axis6_rationality/simplify_benefit_check.py` (untracked
  experiment workspace) — the §2.1 reproduction check: pre-registered criteria
  in its docstring, outputs in `numbers/simplify_benefit_report.json`.
- [`experiment_02_findings.md`](experiment_02_findings.md) §15 — the
  per-mechanism dwell-proportionality result §2.2 leans on.
- [`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 6 — the
  badge this mechanism holds (DESIGNED) and what would move it.
