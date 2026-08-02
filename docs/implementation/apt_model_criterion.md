---
status: durable
created: 2026-07-27
updated: 2026-08-01
topic: "The APT-attacker-model criterion (supervisor S6) — a literature-derived rubric of what an APT attacker model should capture, this model scored against it honestly, and the measurement recommendations (M8b) that ride with each claimed axis"
---

# The APT-attacker-model criterion — what an APT attacker model should capture, and what this one does

**Status:** durable, and **loaded into every session** — it sits on the
read-first list in [`CLAUDE.md`](../../CLAUDE.md) by supervisor direction
([`pipeline/ogasp/supervisor_decision_register.md`](pipeline/ogasp/supervisor_decision_register.md)
§S6). This is the yardstick the post-experiment-1 work is scored and
benchmarked against: the project's headline finding is *what this model
captures about APT attackers that prior models do not*, and until this
criterion existed that headline was an argument without a yardstick
([`architecture.md`](architecture.md) §(l)).

Two constraints are part of the artefact, not tone preferences:

1. **It does not promise the world.** The model does not satisfy every axis,
   and the not-addressed rows below are as visible as the positives. The claim
   is that the model captures the *missing essence* the reviewed literature
   names — CTI-grounded campaign structure and objective conditioning — not
   that it closes the attacker-modelling gap.
2. **The modest-claim ceiling holds.** The defensible claim remains
   *behavioural fidelity changes the answer*, never *the attacker model is
   true* ([`architecture.md`](architecture.md) §(j)). Every scored row is
   **envelope-relative**: a run is one instantiation of a behavioural envelope
   under a declared policy, not a named actor's campaign.

## (a) How the axes were derived

The axis set was fixed from the literature **before** the model was scored, so
the rubric cannot be reverse-fitted to flatter it. Three reviewed sources
supply the material, each read from its tracked extraction (locators are the
extraction's, never invented):

- **Cho 2020** ([`../sources/extractions/cho2020.md`](../sources/extractions/cho2020.md))
  — §V-A's four sophisticated-attacker characteristics (persistent, adaptive,
  stealthy, incentive-driven; source lines 375–400) are the spine; §V-D's
  three under-developed dimensions (smart/learning attacker seldom modelled;
  multi-strategy scenarios scarce; rational-actor framing applied to defenders
  but not attackers; source lines 454–464) are the gap the axes must expose.
- **Alshamrani 2019** ([`../sources/extractions/alshamrani2019.md`](../sources/extractions/alshamrani2019.md))
  — the three-property APT definition and the NIST behavioural clauses (§II-A,
  p. 1853), the "what is NOT an APT" boundary (§II-B, p. 1853), and the
  five-phase lifecycle with its invariant prefix and objective-conditioned
  suffix (§II-C, p. 1854) supply the enumeration of APT behaviour the axes
  must cover.
- **Jalowski 2026** ([`../sources/extractions/jalowski2026.md`](../sources/extractions/jalowski2026.md))
  — names the attacker model "the most glaring flaw in the MTD literature"
  (§4.3, p. 8), rejects Nmap-style active-scanning baselines as too naive for
  APT, and prescribes an attacker that reasons about the MTD scheme itself;
  its §4.1 primitives (pp. 6–7) supply the scheme-awareness axis's three
  sub-rows.

The instrument extends — it does not replace — the cross-section built in the
lit review's §IV-B (`docs/sources/lit_review/LIT_REVIEW.md`, gitignored):
Table II there scores five recent MTD evaluations against Cho's four
characteristics plus a **fidelity descriptor** (parametric / scripted /
procedural / behavioural) constructed for that review. The four
characteristics reappear here as axes 1 and 4–6; the fidelity descriptor
returns in §(e) as the summary placement. Axis selection, the axis names, and
the merge of the NIST clauses onto Cho's characteristics are **this project's
editorial synthesis**, flagged as such; every *content* claim inside an axis
carries its paper and locator.

## (b) The epistemic badges

Every axis carries exactly one of:

| Badge | Meaning |
|---|---|
| **DEMONSTRATED** | evidenced by a run or artefact on record in this repo |
| **DESIGNED** | the mechanism exists (built or specified in the architecture) but has not been shown to change an outcome |
| **CONJECTURED** | a ruled direction with no mechanism yet (design or build outstanding) |
| **NOT ADDRESSED** | absent, with no design commitment |

The badge answers "what can be claimed *today*"; the fifth field of each axis
(*what would evidence a claim*) is the M8b measurement-gap recommendation —
what supplementary measurement would move the badge, recorded as a
recommendation only (nothing is built here, per the S2 freeze and the S6
scope).

**The rows are a census, not a scale (recorded 2026-08-01).** The eight axes
are not independent, and two are in measured tension: both built modulators
narrow traversal, so improving the incentive row (axis 6) or the learning row
(axis 7) provably degrades the plurality row (axis 3 — path entropy collapses
as either capability rises, and the composition study measured the two
narrowings as sub-additive rather than compounding, §(d) axis 3). Any
row-counting summary — "2 DEMONSTRATED / 4 DESIGNED / 2 NOT ADDRESSED" — is
therefore an inventory of what may be claimed, never an additive scale on which
more badges is a better model: on this instrument a model can raise one row
*by* lowering another.

**One distinction the badge vocabulary does not encode, recorded rather than
resolved.** The four DESIGNED rows do not sit there for the same reason: axis 1
records an *absence* (a structure that runs, with no outcome ever shown), while
axes 4, 6 and 7 record *measured negatives* (a built, swept, ablatable
mechanism shown to operate without conferring advantage). A measured negative
is a result and an unevidenced outcome is not, and one badge currently covers
both — each axis's prose argues the distinction the badge cannot. Encoding it
as a fifth badge would re-label existing rows, which is a re-decision this
instrument reserves for Marc; the option is recorded here so the flattening is
a known cost rather than an oversight.

**A standing constraint on what evidence can move a badge — the degenerate
region (recorded 2026-07-28).** At the 200 s mutation interval every
published run of this project has used, *neither* the profiled attacker nor
the baseline completes the substrate objective, and the objective only
becomes reachable above roughly 1 600 s
([`pipeline/ogasp/rate_feasibility_study.md`](pipeline/ogasp/rate_feasibility_study.md)
§7, C5). Inside that region any success-rate-shaped measurement — ASR
included — is pinned at zero and cannot discriminate anything, so it cannot
evidence a badge move in either direction. Evidence offered at the operating
interval must be breadth- or time-shaped, which remain informative
throughout; success-rate evidence must come from outside the region, and say
so. Several M8b fields and §(f) reason in ASR-adjacent terms — read them
under this constraint.

## (c) The scorecard

| # | Axis | Literature source | Prior MTD work (lit review §IV-B cross-section) | This model today |
|---|---|---|---|---|
| 1 | Persistence — multi-stage campaign structure | Cho §V-A; Alshamrani §II-A (NIST i), §II-C | absent throughout | **DESIGNED** |
| 2 | Objective conditioning | Alshamrani §II-A, §II-C | absent | **DEMONSTRATED** |
| 3 | Strategic plurality (multi-strategy branching) | Cho §V-D (dim. 2) | absent | **DEMONSTRATED** |
| 4 | Adaptivity to defender resistance | Cho §V-A; Alshamrani §II-A (NIST ii) | He et al. only, partial and design-time | **DESIGNED** |
| 5 | Stealth — low-and-slow tempo and evasion | Cho §V-A; Alshamrani §II-C; Jalowski §4.3 | He et al. only, in a detection-evasion frame | **NOT ADDRESSED** |
| 6 | Incentive-driven rationality | Cho §V-A, §V-D (dim. 3) | partial RoA operationalisation (Brown, Tay) | **DESIGNED** |
| 7 | Learning capability | Cho §V-D (dim. 1); Jalowski §4.3 | none | **DESIGNED** |
| 8 | MTD-scheme awareness (three Jalowski primitives) | Jalowski §4.1, §4.3 | none | **NOT ADDRESSED** |

Two of eight axes are not addressed. That ratio is the honest shape of the
contribution: the model advances the *campaign-structure* half of the APT
profile (axes 1–4) and leaves much of the *smart-attacker* half (axes 5–8) —
the half Cho's §V-D and Jalowski's corrective name most pointedly — open; on
axis 8 the absence is now a ruled exclusion rather than a default (§(d)). The
exceptions are axes 6 and 7, where a cost/benefit decision rule and a learning
mechanism are now built, declared and swept, and both are held at DESIGNED for
the same reason: each was shown to operate **without** conferring adversarial
advantage. A measured negative is a stronger statement about the field's gap
than silence was, and it is one only a model carrying the capability can make.
§(f) states what all of this buys anyway.

**Two lettered rows are appended to the instrument (2026-08-01) — this
project's addition, not derived from the three source surveys**, the same flag
the §(a) synthesis carries. They exist because the eight axes score properties
of an *adversary* and the project's largest result is a property of an
*evaluation*: an attacker could satisfy all eight and change no defence
ranking, and this one satisfies two and inverts it (§(g)). The rows are
lettered rather than numbered so that axes 1–8, which are cited by number
across the implementation records and the experiment findings, are never
renumbered. Definitions and evidence bars are in §(d2); they were committed
before either row was scored, exactly as the eight axes were fixed before the
model was scored, so the additions cannot be reverse-fitted to flatter the
result that prompted them.

| Row | What it scores | This model today |
|---|---|---|
| A | evidential provenance — are the behavioural parameters evidenced, or declared? | **structure corpus-grounded; magnitudes ≈ one-sixth externally fixed, ≈ three-fifths declared judgement** (§(d2)) |
| B | evaluative consequence — does substituting this attacker change the evaluation's answer? | **RECOMMENDATION grade** — at the operating interval, directionally at ten seeds (§(d2)) |

## (d) The axes

### Axis 1 — Persistence: multi-stage campaign structure

**What it is.** Cho et al. name *persistent* attackers as operating across
multiple stages, reconnaissance through exploitation, aligned with APT-style
campaigns rather than one-off intrusions (Cho §V-A, source lines 375–400).
Alshamrani's NIST clause (i) states it behaviourally — the actor "pursues its
objectives repeatedly over an extended period of time" (§II-A, p. 1853) — and
the five-phase lifecycle (§II-C, p. 1854) gives the stage enumeration.

**Why it matters for MTD evaluation.** MTD's claimed value is disrupting the
knowledge an attacker accumulates across stages; Alshamrani's own MTD passage
makes the mechanism explicit — rearrangement "renders the exploratory
knowledge of the attacker useless" (§IV-C-2-B). An evaluation whose attacker
has no multi-stage knowledge to lose cannot register that value.

**Prior MTD work.** Absent across the §IV-B cross-section — "Table II shows
persistence absent throughout"; the lineage's own attacker is a
compromise-loop FSM, not a staged campaign.

**This model today — DESIGNED.** The movement layer executes a 15-tactic-place
Petri-net campaign structure derived from the analyst-curated Attack Flow
corpus, with pre-intrusion structure composed in synthetically
([`pipeline/ogasp/synthetic_overlay.md`](pipeline/ogasp/synthetic_overlay.md),
M6). One hundred coupled runs traversed that structure end-to-end
([`pipeline/ogasp/experiment_01_findings.md`](pipeline/ogasp/experiment_01_findings.md)).
What is *not* demonstrated is persistence in outcome terms: on the evidence of
experiment 1 the profiled attacker achieves no sustained multi-stage
*progress* on this substrate (0/100 runs reach the objective; effort does not
convert to breadth — finding 2). The structure is real and runs; sustained
staged advance is not yet on record, so the badge stays at DESIGNED.

**What would evidence a claim (M8b).** Progression-shaped measurements the
current suite lacks: distinct-tactic coverage over time (the lead
recommendation — it still discriminates inside the degenerate region, §(b)),
foothold-retention duration across MTD mutations, and the effort-to-breadth
conversion ratio (actions per distinct host) that experiment 1 computed ad
hoc. The originally recommended "deepest tactic band reached per run
(kill-chain depth)" is **withdrawn as written** — it is saturated: every
profile traverses to the objective stage of its own campaign structure, so
the measure cannot discriminate (§(h)). The open measurement-suite handoff
carries a success-gated candidate replacement (deepest *successfully
actioned* stage), to be adopted only if it is shown to discriminate; until
then the coverage curve leads. Recommended, not built.

### Axis 2 — Objective conditioning

**What it is.** Alshamrani's *threat* property defines the APT by its
objective, and the NIST objective triad — exfiltration, impediment, or
positioning for future operations — conditions the lifecycle's suffix: stages
1–2 are invariant, stages 3–5 vary with the objective, and the
position-for-future objective may forgo exfiltration entirely (§II-A p. 1853;
§II-C p. 1854).

**Why it matters for MTD evaluation.** If campaigns with different objectives
traverse different structure, a defence evaluated against a single collapsed
attacker is evaluated against none of them. Objective is the dimension along
which APT campaigns vary and which parametric models collapse (lit review
§V-B).

**Prior MTD work.** Absent — no paper in the cross-section conditions attacker
behaviour on an operational objective; objectives appear only as scenario
labels (Brown's general vs targeted scripts).

**This model today — DEMONSTRATED.** The L2 GASP partition builds four
objective classes, each audit-traced to the analyst-stated operational
objective in the CTI narrative ([`architecture.md`](architecture.md) §(j);
per-flow citations in [`pipeline/gasp/gasp_schema.md`](pipeline/gasp/gasp_schema.md)
§(c)), and the classes are structurally non-trivial (JSD discrimination check,
[`pipeline/gasp/gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(g)).
Experiment 1 then showed the conditioning reaches *runtime behaviour*: which
failure mode a profile lands in — friction, churn, or sink-termination — is a
property of the profile, not the seed
([`pipeline/ogasp/experiment_01_findings.md`](pipeline/ogasp/experiment_01_findings.md)
§3, §5). The demonstrated claim is exactly that: objective conditioning
changes what the attacker does on the substrate. It is *not* a claim that any
profile's behaviour matches a real campaign's (envelope, not actor).

**What would evidence a stronger claim (M8b).** Per-profile behavioural
divergence measures: distributional distance (e.g. JSD) between profiles'
action streams and terminal-tactic distributions at L3, mirroring the L2
corpus-level check at the execution level; and, once experiment 2 runs,
whether MTD *mechanism rankings* differ by profile — the result axis the
supervisor named (R3, S6).

### Axis 3 — Strategic plurality (multi-strategy branching)

**What it is.** Cho et al.'s second under-developed dimension: few scenarios
consider multiple strategies by attackers and defenders — most work pits one
mechanism against one attack path (Cho §V-D, source lines 454–464).

**Why it matters for MTD evaluation.** A single-path attacker cannot reveal
whether an MTD mechanism's value survives the attacker having options; the
multi-strategy regime is where shuffling's combinatorial claims live.

**Prior MTD work.** Absent — the cross-section's attackers execute one scripted
or enumerated path family; the defender side is sometimes plural (Tay's RL
selection), the attacker side is not.

**This model today — DESIGNED.** Attacker-side plurality is structural: each
class net is a behavioural envelope that over-generates by construction — the
union of 5–19 analyst-drawn flows, whose weighted transitions branch across
tactics and techniques per seed ([`architecture.md`](architecture.md) §(j)).
The defender side is plural by design (SDR families + Tay's AI selection,
frozen pool). But the multi-strategy *evaluation* — profiles × defence
families — has not run: experiment 1 deliberately covered one corner (no-MTD
vs one scheme), and the full sweep is carried by the experiment-2 handoff. The
branching also is not *chosen* — transitions are drawn from static
flow-proportion weights, not selected across options by any decision rule —
except to the declared degree axis 6's utility modulator now supplies, which
buys this axis nothing: the same sweep shows path entropy collapsing as the
decision rule sharpens, so cost-sensitivity trades against plurality rather
than adding to it (§(d) axis 6).

**Re-scored DESIGNED → DEMONSTRATED, 2026-07-29, by experiment 2**
([`pipeline/ogasp/experiment_02_findings.md`](pipeline/ogasp/experiment_02_findings.md)
§12), against a criterion pre-registered before the run existed. Both halves the
criterion demanded were met. Traversal diversity is non-degenerate in every
profile — pooled path entropy 1.45 to 2.71 bits, with two to ten distinct
five-tactic opening sequences across ten seeds — so the branching is real rather
than nominal. And outcomes vary over **both** dimensions rather than one: the
ranking of the eight defence conditions by compromise suppression is *not* the
same for every profile (four of five distinct at the operating mutation interval,
five of five at the relaxed one), which is an interaction and not a defender main
effect. A ranking identical for every profile would have evidenced defender
plurality only, and that was the outcome the criterion was written to be able to
report.

**The honest limit travels with the badge, unchanged.** This is **variety, not
strategy**. The branching is drawn from static corpus proportions; no decision rule
selects among options, so the demonstrated claim is that a plural attacker changes
what the defence dimension looks like — never that the attacker chooses between
strategies. The axis-6 qualification above also stands: the one decision rule the
model does carry trades *against* plurality rather than adding to it.

**What would evidence a stronger claim (M8b).** Plurality that is chosen rather
than drawn — a decision rule selecting among branches on something other than
declared frequency, shown to change the interaction above. That is the axis-6 and
axis-7 machinery, and on current evidence both narrow traversal rather than
widening it.

**The badge's dependence on the reported configuration is now measured rather than
inferred (2026-08-01).** This badge was earned with the modulators null, and the
risk that a modulator-active configuration would invalidate it rested on a
precautionary argument that composing the two would compound their narrowing. The
crossed arm has since run (800 runs;
[`pipeline/ogasp/learning_readiness_findings.md`](pipeline/ogasp/learning_readiness_findings.md)
§6), and the compounding **does not happen** — composition is sub-additive, because
the utility model's static preference for cheap tactics and the learner's
state-conditioned discovery that those tactics fail unready pull opposite ways on
the same edges. The claim-integrity rule is unaffected and stands on its other leg:
**every single-modulator configuration still narrows traversal against the null
one**, so this badge's evidence remains the modulators-null arm and any
modulator-active arm reports its own plurality figure
([`pipeline/ogasp/modulator_composition.md`](pipeline/ogasp/modulator_composition.md)
§4). The null cell reproduces the pooled entropy on record, so the configuration
described is the configuration measured.

### Axis 4 — Adaptivity to defender resistance

**What it is.** Cho et al.'s *adaptive* attacker responds to dynamically
changing system and environmental conditions (Cho §V-A); NIST clause (ii) —
the actor "adapts to defenders efforts to resist it" (Alshamrani §II-A,
p. 1853). Alshamrani's §II-B boundary makes it definitional: an attack that
required no adaptation against defender resistance is not an APT.

**Why it matters for MTD evaluation.** MTD *is* defender resistance in motion.
The NIST clause implies MTD provokes re-adaptation rather than permanent
denial (Alshamrani §IV-C-2-B reading); an attacker that cannot adapt at all
overstates MTD's effect, one that adapts freely understates it.

**Prior MTD work.** Only He et al. approach it, and their MTD-aware variant is
design-time configuration (a swept surrogate threshold), not runtime
decision-making; the rest are oblivious to the defence (lit review §IV-B).

**This model today — DESIGNED.** The minimal adaptive loop is built and ran:
the substrate's verdict on each dispatched action selects between success and
failure transition-weight sets at the current place (M2), and an MTD mutation
that severs the attacker's position throws the net's state back (M1 rationale;
built at commit `48471b8`, verified in
[`pipeline/ogasp/runtime_verification.md`](pipeline/ogasp/runtime_verification.md)).
Experiment 1 shows the mechanism *operating* — blocked verbs route the token
back — but not conferring adaptive advantage: the observable consequence was
churn and friction, not recovery (findings 1–2). Adaptation is
outcome-reactive re-routing over static weight sets, and it does not condition
on the defence itself (axis 8).

**One half of that sentence has since been discharged, and it does not move this
badge.** S1's named next step — attacker-state-conditioned dynamic weights — is
now built: the routing weights *do* update from experience, through the axis-7
learner (2026-07-29). What that produced was a sharper version of the same
verdict rather than a different one. The attacker measurably reduces its own
friction as it learns, and its compromise breadth falls as it does so, so the
mechanism operates and still does not confer adaptive *advantage* — which is what
this badge has always turned on. Axis 4 therefore holds at DESIGNED with better
evidence behind it than experiment 1 alone provided.

**What would evidence a claim (M8b).** Response-shaped measurements: change in
the attacker's action mix before vs after an MTD trigger event, recovery time
from an MTD-induced state throw-back, and whether failure-conditioned routing
measurably redirects effort (weight-set switch frequency vs progress). These
discriminate "reacts" from "adapts usefully".

### Axis 5 — Stealth: low-and-slow tempo and evasion

**What it is.** Cho et al.'s *stealthy* attacker does not exhibit identifiable
attack behaviour continuously; it blends in until the moment of most harm
(Cho §V-A). Alshamrani grounds it as the defining "low and slow" tempo —
evasive techniques sustained to elude detection (§II-A, §II-C stage 3) — and
Jalowski's corrective adds the reconnaissance modality: APTs use *passive*
reconnaissance to remain hidden, which is why Nmap-style active-scanning
baselines are too naive (§4.3, p. 8).

**Why it matters for MTD evaluation.** A stealthy attacker trades speed for
observation time — precisely the budget MTD's temporal churn is supposed to
tax. If the attacker model has no tempo choice and no evasion behaviour, the
evaluation cannot see the cost MTD imposes on stealth, nor the stealth an
attacker sacrifices to keep pace with mutations.

**Prior MTD work.** Operationalised only by He et al., and there the frame is
detection-evasion of an ML classifier, not APT-style network compromise; the
cross-section's compromise-oriented attackers have no stealth dimension.

**This model today — NOT ADDRESSED.** The substrate offers the movement
attacker no detection model to be stealthy against (Tay's IDS-sensitivity
machinery is a defender-side benchmark, deferred to the ablation phase), the
S2 freeze rules out an evasion action, and the metrics do not reward
evasion-shaped behaviour — the M8 expectation that experiment 1 confirmed.
Movement through evasion-*named* tactics exists (the nets contain
defence-evasion places) but carries no stealth semantics. The S3 timing
regime is now **built**: per-tactic exponential dwell with non-action tactics
consuming time landed through the timing design and build handoffs, and the
S3-R reversal then made the movement layer the source of every unit of the
profiled attacker's time. The model therefore has its *tempo* axis. The badge
does not move, because tempo without a consequence is still not evasion —
there is no detection model for a tempo choice to matter against, which is
this axis's own argument.

**What would evidence a claim (M8b).** The supervisor's own caveat stands:
measuring stealth is acknowledged tricky (M8b). Candidate supplementary
measurements, if stealth is ever claimed: attack-event rate visible to
substrate statistics per unit time (a detectability proxy), dwell fraction in
non-action tactics, and tempo response to MTD frequency. The S3 timing regime
these require has landed; what still gates a stealth claim is a stealth
semantics for the measurements to speak to.

### Axis 6 — Incentive-driven rationality

**What it is.** Cho et al. model the sophisticated attacker as "a rational
actor that is sensitive to incentives, such as attack success with minimum
cost" (Cho §V-A), and name the asymmetry as their third under-developed
dimension: the rational-actor framing is routinely applied to defenders,
seldom to attackers (§V-D).

**Why it matters for MTD evaluation.** MTD's economic argument is raising
attacker cost; it is only measurable against an attacker that *has* a cost
model and conditions decisions on it.

**Prior MTD work.** Partial operationalisations only: the lineage's RoA
heuristic (Brown, Tay) is a defender-computed cost/impact ordering the
attacker optimises without being able to sequence, adapt, or remember — the
lit review's "rationality without capability" (§V).

**This model today — DESIGNED** (moved from NOT ADDRESSED 2026-07-29;
[`pipeline/ogasp/incentive_rationality.md`](pipeline/ogasp/incentive_rationality.md)).
The base transition weights remain flow-proportion frequencies and the outcome
overlay remains a declared policy, but a cost/benefit decision rule now sits
above both, as a modulator on the attacker-state seam: the routing weight of a
destination is multiplied by `(u(b)/ū)^λ`, where `u(b)` is a declared per-tactic
benefit over that tactic's declared duration. The benefit family is the one new
declared family (rule-generated from objective proximity *within the profile*,
complete over 75 cells, reproducing 0/75); the cost term reuses the duration
catalogue rather than declaring a parallel one. The rationality exponent λ is
declared, never fitted, and swept over its band against six conclusions
committed before the sweep ran; at λ = 0 the mechanism is **bit-identical** to
the model without it, so the ablation is exact rather than approximate.

**Why DESIGNED and not DEMONSTRATED.** The mechanism runs and is on record
changing behaviour — at the declared λ the attacker moves visit share onto the
cheap exploit-shaped tactics and off the expensive low-and-slow ones, and at the
near-greedy end of the band pooled path entropy collapses from 2.23 bits to
0.24. It also changes an *outcome*, in the unflattering direction: blocked
attempts rise from 49 % to 99 % of actions and distinct hosts fall, because the
cheapest tactics on this substrate are the most tightly precondition-coupled —
experiment 1's H-coupling finding in economic terms. What did **not** reproduce
is the result this axis exists to produce: MTD's measured effect does not change
when the attacker can see cost. The anatomy is recorded rather than
explained away — MTD's tax *is* strongly differentiated across tactics (an
18-fold spread in interrupt rate) but is levied in near-proportion to a tactic's
declared dwell (a roughly uniform ~9 % surcharge), and a normalised utility
*ratio* is invariant to a proportional inflation of its denominator. Claiming
DEMONSTRATED would let a reader infer the economic MTD result the evidence does
not support.

> **The unflattering outcome above is qualified 2026-08-01 (R2 on the benefit
> family), and the badge does not move.** "Experiment 1's H-coupling finding in
> economic terms" attributes the attacker's self-defeat to the *terrain*, and
> that attribution is not established. The declared-duration cost and the
> objective-proximity benefit penalise *instrumental* tactics twice over —
> reconnaissance is both the slowest declared tier and the furthest from any
> objective, so the profile that most needs it prefers a 4.5 s exploit-shaped
> tactic over it by a factor of 31 — and neither term can express that a tactic
> is worth its price because of what it unlocks. The collapse may therefore be
> a property of the decision model rather than of the substrate
> ([`pipeline/ogasp/cost_model_plain.md`](pipeline/ogasp/cost_model_plain.md)
> §2.2a). The badge is untouched, because DEMONSTRATED was withheld on C4 and a
> defect that makes the mechanism's one measured outcome *less* interpretable
> cannot raise a row. What it does change is the M8b field below: the second of
> its two candidate routes is now the remedy for a known defect as well as a
> route to the missing result, which raises its priority over the first.

**What would evidence a claim (M8b) — updated.** The prerequisite measurement
(a cost ledger per run and per arm) is built and reported
([`pipeline/ogasp/measurement_suite.md`](pipeline/ogasp/measurement_suite.md)),
and a decision rule consuming it now exists. What remains for DEMONSTRATED is a
condition under which cost-sensitivity changes MTD's measured effect, which the
sweep's anatomy narrows to two candidates: a defence whose cost is **not**
proportional to dwell (one taxing particular tactics rather than particular
durations — reachable inside experiment 2's defence family), or a utility
conditioned on a quantity the proportional surcharge does not cancel, such as
realised success rate per tactic rather than realised time. The seam already
observes both. **The second route is now designed** — a state-conditioned
expected cost and an enabling-value benefit, both derived from artefacts that
already exist rather than from a new declared family
(`docs/handoffs/2026-08-01_iterated_cost_model.md`) — and it is the same build
that would repair the R2 defect above, which is a reason to prefer it over the
first route rather than merely an option beside it. It remains gated on Marc's
disposition and the freeze. Note that the S2 freeze's status is unchanged: the seam record's
§7 question to the supervisor gates *using* a non-zero λ in a reported
experiment, and this badge move rests on the mechanism and the sweep, not on an
experimental claim.

> **The second route was built and swept 2026-08-02, S2 cleared, and the badge
> stays DESIGNED — but the reason has changed, and the new reason is the more
> useful finding**
> ([`pipeline/ogasp/iterated_cost_model.md`](pipeline/ogasp/iterated_cost_model.md);
> 4 200 runs, conclusions pre-registered). The mechanism exists: a
> state-conditioned expected cost over the declared precondition relation's
> capability closure, and a benefit measuring distance through the profile's own
> routing net, both derived from artefacts already on disk with **no new declared
> magnitude**. It repairs the R2 defect measurably — the blocked-fraction rise is
> 73–89 % undone in the pooled `v2_partial` cells and successes per action roughly
> double — though not at the per-profile resolution its own U2 demanded (3 of 30
> cells CI-disjoint), so U2 is recorded moved and the stopping rule was honoured.
>
> **The badge is declined rather than failed, and that distinction is the point.**
> U3 — the conclusion written to move this row, taking C4's criterion verbatim so
> the verdicts would be comparable — *passes* on the bare threshold, at 4 of 5
> profiles, for three of the four arms. It also passes for the **`declared` arm**,
> which is the shipped model that F6 proved by spike cannot see MTD at all (its
> factor table precomputes to 30/30 bit-identical, and the MTD condition is not
> among its inputs). A criterion passed by a negative control is not measuring the
> property it tests, and the per-profile continuum confirms it: four of five
> ratios sit within ±15 % of 1.0 in every arm, with `double_extortion` — this
> family's recorded outlier under both C4 and C6 — carrying the pass. U3 is
> recorded **moved**, on the identical reading C4 is recorded moved on, and this
> row stays DESIGNED. Reporting it as held would move a badge on a statistic that
> cannot discriminate.
>
> **What this leaves the M8b field below.** Route two is no longer a candidate —
> it is built, and it is not what is missing. What is missing is an **instrument**:
> a measure of MTD-conditional attacker response that a mechanism provably blind
> to MTD cannot pass. Until one exists this row cannot be moved by any mechanism,
> because the evidence bar itself is the thing that fails. Route one (a defence
> whose cost is not proportional to dwell, reachable inside experiment 2's family
> at the relaxed interval) is unaffected by this and remains open — but it would
> be scored by the same statistic, so it inherits the same problem.
>
> **A finding from the sweep that belongs to axis 3 rather than this one, recorded
> here because this sweep produced it.** The repair inverted its own design's
> ranking: the expected-cost change (the brief's recommended minimum) fails, and
> the benefit-through-the-net change pays. The latter is the first modulator
> configuration this project has measured that **does not narrow traversal** —
> pooled path entropy *rises* against the shipped model in 5 of 5 profiles on both
> mappings, and holds 1.008 bits at the near-greedy band end where the shipped
> family collapses to 0.655. Axis 3's badge and its reported-configuration pin are
> untouched (the headline arm still runs modulators null), but the standing
> qualification that the model's one decision rule trades *against* plurality now
> has a measured exception, and it is the numerator that supplies it.

### Axis 7 — Learning capability

**What it is.** Cho et al.'s first and sharpest under-developed dimension:
attackers are assumed to follow fixed patterns "rather than that they learn
and can launch adaptive attacks", while defenders are granted learning
capability — an asymmetry contrary to practice (Cho §V-D, source lines
454–464). Jalowski's APT "learns mutation patterns over time" (§4.3, p. 8).

**Why it matters for MTD evaluation.** MTD's protection degrades fastest
against exactly this capability — an attacker that accumulates knowledge
across mutations. An evaluation without attacker learning measures MTD
against the attacker least equipped to defeat it.

**Prior MTD work.** None in the cross-section; the asymmetry is the field-wide
pattern both surveys name (defender RL is common — Tay included — attacker
learning is not).

**This model today — DESIGNED (moved from NOT ADDRESSED, 2026-07-29).** The
movement attacker now carries a within-run belief about which tactics pay on this
terrain — a Laplace estimate over the success and failure verdicts observed at
each tactic-place, entering routing as a declared exponent and perishing by a
declared fraction on every MTD mutation
([`pipeline/ogasp/learning_capability.md`](pipeline/ogasp/learning_capability.md)).
Both magnitudes are declared, tiered, banded and swept over 2 400 runs, and the
zero-capability arm is bit-identical to a run without the mechanism, so the two
arms differ by a parameter rather than by wiring.

The badge is DESIGNED rather than DEMONSTRATED **on a criterion fixed before the
runs existed**, and it lands on exactly the pattern axis 4 sits at: the capability
demonstrably operates and demonstrably does not help. It operates — on experiment
1's mapping the attacker drives its own blocked fraction from 91 % to 21 % as the
capability rises, and does so *within* runs, against an ablation arm that improves
only slightly on its own. It does not help — compromise breadth falls sharply as
the capability rises (6.5 hosts to 0.8 on the mapping where the attacker
compromises anything), effort-to-breadth conversion worsens, and no run at any
parameter point reaches the objective.

Why it does not help is the study's substantive finding, and it is a statement
about the *measurement* rather than about learning: the binary routing verdict the
learner updates on is not a progress signal. Scanning succeeds far more often than
exploiting does, so the belief correctly concludes that reconnaissance pays, and a
confident learner therefore stops attacking — exploitation falls from 13 % of the
attacker's successes to 1 %. Experiment 1's churn failure mode was already the
observation that success verdicts and progress differ; a learner does not create
that gap, it finds it and optimises into it.

Two further results ride with the axis. **MTD is severely effective against this
learner** — most of the advantage is gone once a quarter of the belief is lost per
mutation, and at roughly 42 interrupts per run even gentle forgetting compounds —
which is a defence effect none of the existing security metrics could register,
because what the mutation destroys is an estimate rather than a foothold. And
**learning narrows traversal**: path entropy falls at every capability step in all
ten profile × mapping cells, so axes 3 and 7 pull against each other, and a claim
on either must name the capability it was measured at.

Cross-run memory remains out of scope (M8d, and axis 8's beacon primitive, ruled
future work). The commented-out substrate learning (ATK-04) was considered and
refused: it is a substrate change that would move every golden, and it is a
pricing discount rather than a decision capability.

**What would evidence a claim (M8b) — updated.** The original recommendation is
**partly discharged**: the within-run knowledge measure exists and has run —
blocked fraction over a run's first against its last quarter of attempted actions,
reported against the ablation arm, which is the comparison that matters, since the
substrate's own state accumulation improves the ablation arm too and a bare
within-run decline would "evidence" learning in a model with none. What would move
the badge to DEMONSTRATED is now specific: a learner whose credit signal carries
**progress** (host compromise, stage advance, breadth) rather than the routing
verdict, shown to raise breadth or stage advance against its own ablation arm.
That is a credit-assignment redesign, not a parameter change. Cross-mutation
retention — does the attacker re-acquire targets faster after the nth shuffle? —
remains unbuilt and is the natural companion measurement.

**The representational half of that requirement has since been built, swept and
found insufficient on its own (2026-08-01;
[`pipeline/ogasp/learning_readiness_findings.md`](pipeline/ogasp/learning_readiness_findings.md)).**
The learner was re-keyed from the destination tactic to `(destination tactic,
precondition-satisfied?)` — the smallest key that can express a state-dependent
constraint, chosen against ranked alternatives on a measured observation budget
([`pipeline/ogasp/learning_representation.md`](pipeline/ogasp/learning_representation.md))
— and swept over 4 600 runs against both the ablation arm and the destination-only
learner as controls. **The badge does not move, on the criterion this field
already fixed.**

What the generalisation bought is precisely the damage the marginal key had done,
and nothing beyond it: compromise breadth at the declared capability recovers from
3.38 hosts to 4.52 against the destination-only learner, the collapse at high
capability is arrested (1.02 → 2.40 hosts), and exploitation's share of successes
returns from 6.0 % to 9.5 % — but the **no-learning ablation arm sits at 4.60**,
and the readiness learner does not exceed it at any capability. Stage advance, the
gate's other disjunct, is identical to the destination-only learner's on both
mappings and unseparated from the ablation arm's at ten seeds. An attacker whose
accumulated knowledge returns it to where an attacker with no knowledge already
stood has not been shown to be a better adversary.

Two things follow for this field. The requirement is now **isolated to the credit
signal** — the representation was a genuine blocker, it has been removed, and
removing it recovered exactly the ground the misrepresentation had lost, so a
progress-carrying signal is the sole remaining item rather than one of two. And a
warning rides with the measurement: on every friction-shaped measure the two
representations are indistinguishable to three decimal places, differing only on
breadth, so the within-run blocked-fraction measure recommended above **cannot
discriminate between representations** and must never be read as evidence for one.

### Axis 8 — MTD-scheme awareness (the three Jalowski primitives)

**What it is.** Jalowski et al.'s corrective: research must shift toward
"smart, adaptive attackers who understand the MTD scheme and look for the
mathematical logic behind the movement" (§4.3, p. 8). Their §4.1 supplies
three concrete primitives (pp. 6–7): **(i) state-collision recognition** —
cross-target memory that recognises post-shuffle state repetition in finite
parameter spaces; **(ii) MTD-event-as-beacon** — reading per-host mutation
frequency as a signal of asset value; **(iii) metadata-shadow invariance** —
extracting the side-channel features that do *not* change when the attack
surface does.

**Why it matters for MTD evaluation.** These are the capabilities that turn
MTD's own operation into attacker information — the regime in which MTD can
be net-negative. An evaluation blind to them can only report MTD's best case.

**Prior MTD work.** None; this is the gap half of Jalowski's diagnosis, and no
paper in the cross-section models any of the three.

**This model today — NOT ADDRESSED, by ruled exclusion (Marc, 2026-07-28).**
All three primitives are promoted from *pending encoding* to **out of scope**
in [`architecture.md`](architecture.md) §(f): encoding any of them requires an
inference capability — machine learning or reinforcement learning over
observed defender behaviour — that the remaining timeframe cannot support
building and validating, and none will be implemented. The negative is
therefore deliberate, and it remains the criterion's bluntest: the attacker
keeps no cross-target configuration memory (i), does not observe defender
event frequency (ii), and its observation surface is CVE/CVSS-only (iii).

The future-work statement is correspondingly specific. It is *not* that the
simulator cannot support scheme awareness: the observation channel exists and
is unwired. `Adversary.observed_changes`
([`adversary.py:23`](../../mtdnetwork/component/adversary.py)) is an empty
dictionary nothing in the repository ever reads or writes — the vestigial
hook for exactly the attacker-observes-defender channel primitive (ii) needs
— while the substrate already exposes everything such a primitive would
consume (per-event MTD records with resource layer and timing, a computed
mutation-execution frequency, the currently-running and suspended mutations,
cumulative interrupt counts), all reachable from the adversary's live network
handle without a single substrate change
([`mtd_statistics.py`](../../mtdnetwork/statistic/mtd_statistics.py)). What
is missing is the inference capability and the time to build and validate it.
The one genuinely absent input is per-host mutation counts — no MTD strategy
keeps per-target bookkeeping — so a beacon primitive would additionally have
to derive or instrument them. The encoded subset bounds the contribution
(§(f)); it stays empty on this axis for the life of the project.

**What would evidence a claim (M8b).** Per primitive: (i) repeat-compromise
rate on previously-seen configurations vs unseen; (ii) correlation between
attacker target-selection and defender mutation frequency (the natural
inverse of Tay's IDS-sensitivity experiment, per §(f)); (iii) any
invariant-feature observation channel at all. Each presupposes the primitive
being encoded — a lift of the S2 freeze and a fresh comparability argument,
not current work.

## (d2) Rows A and B — evidential provenance and evaluative consequence

**These two rows are this project's synthesis, not the surveys'.** The eight
numbered axes were derived from Cho, Alshamrani and Jalowski (§(a)); no source
survey supplies these two, and they are flagged accordingly, as the §(a)
editorial synthesis is. They also serve a different reader. The eight axes help
someone **building** an attacker model; these rows help anyone **assessing**
whether an attacker model — this one or their own — is evidenced and is doing
any work, which is the difference between a private development checklist and a
transferable instrument.

**The derivation discipline applies unchanged.** This section's definitions,
graded outcomes and evidence bars are committed *before* either row is scored;
the scores land in a separate, later commit against the evidence as it stands.
The commit order is the audit trail, as it was for the §(a) axis synthesis and
for every pre-registered sweep since.

### Row A — evidential provenance

**What it asks.** What proportion of the model's behavioural parameters is
traceable to an external, dated, third-party artefact, as against declared by
the modeller?

**A rejected phrasing, recorded so it is not re-proposed.** The instinctive
form of this row — *is the CTI-derived model an upgrade on prior worked
examples?* — is rejected on two grounds. It is comparative and self-scored, so
every author answers yes, which is precisely the reverse-fitting this criterion
exists to prevent. And it welds together two things that separate cleanly:
whether the behaviour is *evidenced* (this row) and whether the evidence
*changes anything* (Row B). Provenance without consequence is bookkeeping;
consequence without provenance is a differently-arbitrary attacker. Scored
apart, the pair becomes an argument.

**How it must be scored.** By aggregation only — never by fresh judgement at
scoring time. The declared-value families already carry per-entry tier badges
([`declared_value_provenance.md`](declared_value_provenance.md)), assigned when
each family was authored and before this row existed, and the non-ledger layers
(the corpus-derived structure and weights, the audit-traced objective
partition, the declared controller mapping) carry recorded provenance of their
own. The row's score is those records counted, with the counting basis stated;
a score that required re-judging any value's tier would be the reverse-fitting
the discipline above forbids.

**Evidence bar.** *Externally attested* means fixed by, or traceable to, an
artefact outside this project's modelling judgement: the analyst-curated Attack
Flow corpus, the inherited substrate's constants (via
[`provenance.md`](provenance.md), which traces them to the published lineage),
or a dated literature source. The `attested-pattern/declared-magnitude` tier
counts as attested for the *behaviour* and declared for the *number*, and is
reported as its own category, folded into neither. The result is reported as
counts at ledger-entry level with the non-ledger layers named beside them —
never as a single binary claim of CTI-groundedness, which the tier structure
exists to prevent in both directions.

**Score — 2026-08-01, by aggregation, one commit after the definition.** The
behavioural parameter surface divides into the structural layer, four value
families carrying per-entry tier badges, and two declared choices with no
ledger. Counted at ledger-entry level, the four families hold 38 entries: the
duration catalogue's 15 per-tactic values, the outcome overlay's 15 rules, the
learning family's 3 entries and the benefit/utility family's 5.

- **Corpus-grounded in full — the structural layer.** The campaign structures
  and base transition weights: five class nets built as unions of 5–19
  analyst-drawn flows, with transition weights from flow proportions
  ([`architecture.md`](architecture.md) §(j)); and the objective partition,
  audit-traced per flow to the analyst-stated operational objective
  ([`pipeline/gasp/gasp_schema.md`](pipeline/gasp/gasp_schema.md) §(c)). This
  is the model's single largest input and the layer every declared family
  conditions. One declared exception rides with it: the pre-intrusion
  structure is composed in synthetically
  ([`pipeline/ogasp/synthetic_overlay.md`](pipeline/ogasp/synthetic_overlay.md),
  M6) rather than drawn from the corpus.
- **Externally fixed — 6 of 38.** The six Tier-1 durations, priced by the
  substrate's own constants and traceable through
  [`provenance.md`](provenance.md) to the published lineage.
- **Attested in pattern or target, magnitude declared — 9 of 38.** The five
  outcome-overlay entries at `attested-pattern(/declared-magnitude)`, the
  learning exponent κ, and the three Tier-2 durations — the last carrying a
  named literature calibration milestone the catalogue has not yet been
  calibrated against (its own version string is `v0-uncalibrated`).
- **Declared judgement — 23 of 38.** The ten remaining overlay entries, the
  six Tier-3 durations, the learning estimator and forgetting fraction, and
  all five entries of the benefit/utility family — whose ledger additionally
  records having survived no adversarial round at all.
- **Declared with no ledger.** The tactic-to-verb controller mapping (the
  chosen input parameter every result is already bounded by) and the sink
  policy.

**The honest summary this row exists to force:** the model's *structure* is
corpus-grounded and its *magnitudes* are mostly not — roughly a sixth of the
ledgered values are externally fixed, roughly two-fifths carry an external
anchor of any kind, and three-fifths are declared judgement, labelled as such
and defended by sweep rather than by source. The defensible sentence is
*CTI-grounded structure with declared, tiered, swept magnitudes*; the row makes
the binary sentence — *a CTI-derived attacker model* — unavailable, in either
direction. This is the modest result the row was expected to return, and it is
credible precisely because it is modest.

### Row B — evaluative consequence

**What it asks.** Does substituting this attacker for the incumbent, on the
same substrate, change the evaluation's *ordering* of defences, the *magnitude*
of their measured effect, or the *recommendation* a practitioner would draw?

**Three graded outcomes, fixed before scoring.**

1. **Magnitude** — the same defences win, by different margins.
2. **Ordering** — the ranking of the defence conditions changes.
3. **Recommendation** — the top-ranked mechanism changes.

**Evidence bar.** A graded outcome may be claimed only from a comparative run
on record in which both attackers ran on the same substrate against the same
defence family, with the mutation interval and seed count stated. The caveats
travel with the row, not in a footnote: a seed count that supports a rank
comparison does not support a significance claim and the row must say which it
has; any interval dependence is stated beside the grade, since a ranking taken
inside the degenerate region (§(b)) means nothing on its own; and the row is
bounded by the tactic-to-verb mapping remaining a chosen input parameter rather
than a fidelity claim, for as long as that boundary stands. The envelope
discipline applies here as everywhere: the substituted attacker is one
instantiation of a behavioural envelope under a declared policy, not a named
actor, so the row scores what the substitution *reveals about the evaluation*,
never the realism of the substitute.

**Score — 2026-08-01: RECOMMENDATION, the highest grade, at the operating
interval, directionally at ten seeds.** The comparative run on record
([`pipeline/ogasp/experiment_02_findings.md`](pipeline/ogasp/experiment_02_findings.md)
§9) ran the inherited and the profiled attacker on the same substrate across
the same eight defence conditions. At the 200 s operating interval the two
defence orderings are very nearly reversed — rank correlation ρ = −0.893 — and
the top-ranked mechanism changes: Service Diversity best suppresses the
inherited attacker (90.4 %, OS Diversity close behind at 88.8 %), while the
position-destroying conditions best suppress the profiled one (simultaneous
scheme 89.8 %, Complete Topology Shuffle 89.1 %). An evaluator would deploy a
different mechanism depending solely on which attacker the evaluation carried,
which is grade 3 as defined above.

The caveats, in the row as the bar requires. **Seeds:** ten supports a rank
comparison and not a significance test — a constraint two independent sweeps
established before the run pre-registered it. **Interval:** the grade is
regime-dependent — at 2 000 s the correlation is ρ = +0.286, so the *ordering*
grade still holds there, but the inversion and with it the clean
recommendation contrast are properties of the high-pressure regime, and the
recommendation grade is claimed at the operating interval only. **Mapping:**
the row is bounded by the tactic-to-verb mapping remaining a chosen input
parameter — how much of the inversion is the corpus and how much is the
mapping is not separable from this run (findings §20, which names the
mapping-sensitivity study as the instrument). **And one open ruling touches
the evidence:** the retrace-arm cells of the three sink-bearing profiles ran
under the since-superseded sink implementation (findings §1, reconciliation
note); if Marc rules for a re-take, this row re-scores against it.

## (e) Fidelity placement

The lit review's constructed descriptor (Marc's instrument, §IV-B — labelled
there and here as this project's synthesis, not a paper's claim) orders threat
models by realisation depth: **parametric → scripted → procedural →
behavioural**. The §IV-B cross-section clusters at parametric (Brown, Tay,
He) and scripted (Masud, Kim); none reach procedural.

This model places at **procedural — demonstrated**: rule-based decision-making
within an attack progression at runtime (weighted stochastic branching over a
live net, conditioned per-place on substrate verdicts), on record in
experiment 1. Of the behavioural rung's three components, campaign-level
intent and motivation conditioning are present (axes 1–2).

**The learning component was restated on 2026-07-29 and the placement did not
move.** It had read that the behavioural rung "requires learning this model does
not have", and that is no longer true as written: the model has a learning
mechanism, declared, swept and ablatable
([`pipeline/ogasp/learning_capability.md`](pipeline/ogasp/learning_capability.md)).
But the rung's third component is not *contains a learning mechanism*; it is an
attacker whose accumulated knowledge makes it a better adversary. The model now
has the mechanism and has shown that, on this substrate and with the routing
verdict as its credit signal, the mechanism does not produce that adversary —
the attacker learns to reduce its own friction and loses compromise breadth
doing it.

The placement claim is therefore: **the first model in this cross-section's
frame to reach the procedural rung, carrying two of the three behavioural-rung
components plus a learning mechanism that has been built, declared, swept and
found not to confer adversarial advantage on this terrain — and not a
behavioural model.** That is a stronger statement than the original, because it
rests on a measured negative rather than on an omission, and it names precisely
what a behavioural-rung claim would still need: a credit signal carrying
progress rather than the routing verdict.

**That last sentence was tested on 2026-08-01 and survives, with one clause now
carrying evidence it previously carried on argument.** It named a single missing
ingredient, and there were in fact two candidates — the credit signal and the
representation the signal is keyed on. The representation has since been
generalised and swept, and it is not the ingredient: a learner that can express
*this tactic pays here* recovers what the marginal key lost and still confers no
adversarial advantage
([`pipeline/ogasp/learning_readiness_findings.md`](pipeline/ogasp/learning_readiness_findings.md)).
The placement does not move, and the outstanding requirement is now known to be
the credit signal alone rather than suspected to be.

## (f) Experiment 1 scored against the criterion

The rubric has to discriminate, not merely assert. Applied to the one result
on record ([`pipeline/ogasp/experiment_01_findings.md`](pipeline/ogasp/experiment_01_findings.md)):

- **Axis 2 gains its DEMONSTRATED badge from this run.** Profile identity
  determines failure mode (friction vs churn vs sink) independent of seed —
  runtime behaviour is objective-conditioned. Under the criterion this is the
  experiment's positive finding, invisible to the headline security metrics.

  > **Qualified 2026-07-28 by the S1 sensitivity sweep**
  > ([`pipeline/ogasp/weight_sensitivity_study.md`](pipeline/ogasp/weight_sensitivity_study.md)
  > §5). "Independent of seed" understated what had to be shown: a mode
  > assignment that held across seeds but moved with the declared routing weights
  > would be an artefact. Across 2 600 runs over the declared parameter bands, the
  > assignment holds for the profiles at the **extremes** — `pure_steal` at
  > 96.9–97.5% blocked, `double_extortion` and `infrastructure_setup` at 0.0%,
  > every point, both mappings. It does **not** hold for `pure_impediment`, the
  > profile experiment 1 already recorded as intermediate: its blocked fraction
  > spans 25.0–63.1% across the sweep and crosses the classification threshold.
  > The badge stays DEMONSTRATED, on the narrower claim — objective conditioning
  > changes what the attacker does, robustly where the profiles are behaviourally
  > distinct and not where they are close — and no ordering of profiles by
  > progress may be claimed at all, which the sweep found unsupported at ten
  > seeds.

  > **Qualified again 2026-07-28 by the rate feasibility study**
  > ([`pipeline/ogasp/rate_feasibility_study.md`](pipeline/ogasp/rate_feasibility_study.md)
  > §7, C3b). The same claim was tested against timing arbitrariness rather
  > than weight arbitrariness. The mode assignment holds without exception for
  > four of the five profiles in every swept cell; `pure_steal` flips between
  > horizon and sink termination in twelve cells, and inspection shows why —
  > its central cells split 7–3 and 5–5 across the ten seeds, so its modal
  > mode is a coin-toss summary of a genuinely bimodal distribution, flipping
  > on seed noise rather than on where any anchor sits. The badge does not
  > fall; its evidence narrows again: profile-determined failure mode is
  > established for four profiles and indeterminate for the fifth at this
  > sample size, and the fix is power or a distributional statistic, not a
  > timing change.
- **Axis 1 is held at DESIGNED by this run.** The structure executes, but
  0/100 objective-reaches and an order-of-magnitude worse effort-to-breadth
  ratio mean sustained multi-stage progress is not evidenced; a rubric that
  scored persistence "captured" on structural grounds alone would be
  reverse-fitted.
- **Axis 4 is held at DESIGNED.** The adaptive loop demonstrably operates
  (blocked actions re-route the token) and demonstrably does not yet help
  (churn); reacting is on record, adapting is not.
- **The M8 metrics gap is the criterion's own finding restated.** The one
  metric that responded to MTD (baseline time-to-first-compromise, +50 %
  directional) is defined on the baseline-shaped attacker; the profiled
  attacker never gets far enough for MTD to bite. The measurement suite can
  currently score axes it holds no claim on, and cannot score the axes the
  model claims — which is why every claimed axis above carries its M8b
  measurement recommendation.

  > **Magnitudes marked stale 2026-07-28.** Experiment 1's baseline figures —
  > the +50 % time-to-first-compromise response above, and the baseline
  > success rates that run recorded — are no longer a valid comparison
  > target: the seven-defect repair (`dd8c5ec`) and the deliberate
  > re-baseline that followed it (`06ed8d9`) landed after that run's numbers
  > were taken, and on the current substrate the baseline reaches the
  > objective 0/10 under random MTD at 200 s where experiment 1 recorded
  > 10/10 ([`pipeline/ogasp/rate_feasibility_study.md`](pipeline/ogasp/rate_feasibility_study.md)
  > §6). The findings stand as the record of that run and are deliberately
  > not recomputed; any new comparison re-measures the baseline in the same
  > run.

## (f2) Experiment 2 scored against the criterion

The comparative run across the defence family
([`pipeline/ogasp/experiment_02_findings.md`](pipeline/ogasp/experiment_02_findings.md),
2026-07-29). Added beside §(f) rather than replacing it: experiment 1 remains the
record of its own run, and its magnitudes are stale twice over — the substrate was
re-baselined after it, and the intent-audit dispositions landed after that.

- **Axis 3 gains its DEMONSTRATED badge from this run** (§(d) axis 3), on the
  pre-registered two-part criterion.
- **Axis 2's demonstration reaches a new dimension.** Objective conditioning was
  demonstrated on *failure mode*; it now also determines **which defence works
  best**, with the mechanism ranking differing by profile in four of five cells at
  the operating interval. That is the result axis the supervisor named (R3, S6),
  and it is a stronger form of the same badge rather than a new one.
- **Axis 4 is held at DESIGNED on the control it never had.** Every prior run had
  the adaptive loop switched on. A verdict-blind ablation arm — an overlay whose
  value tables are empty, so composition passes every destination through at 1.0 —
  ran on identical seeds across the full matrix, and **no progression measure
  separates it from the conditioned arm** on the pre-registered bar. Routing on the
  substrate's verdict is approximately free. The badge does not move, and the
  reason it does not has improved: *reacts but does not adapt usefully* is now a
  measured statement rather than an inference from churn.
- **Axis 1 was reported as moving and was withdrawn.** The first pass of the
  analysis scored persistence DEMONSTRATED. Cross-examination of the measures
  against their implementations retracted it, on two independent grounds: the
  deepest-successfully-actioned-stage measure returns the same value for **all 800**
  movement runs (structurally truncated under this mapping, so the *replacement*
  for the saturated depth measure is itself saturated), and the foothold-retention
  measure counts footholds *severed* rather than retained — with the further
  artefact that the two application-layer mechanisms interrupt often and sever
  position never, so retention under them is total by the absence of any threat to
  it. Against the defences that actually contest position, per-foothold retention
  at the operating interval is 0.0–1.6 %. This is the pre-registration discipline
  doing the only job it exists to do, and it is recorded because the near-miss is
  more instructive than the verdict.
- **The headline result is invisible to every axis.** The defence *ranking*
  inverts between the inherited attacker and the profiled one (rank correlation
  −0.893): the diversity family suppresses the vulnerability-exploiting baseline by
  ~90 % and the profiled attacker by ~37–41 %, while the position-destroying family
  does the reverse. No axis scores "the model changes which defence you would
  choose", because the axes score the attacker model and this is a statement about
  what the attacker model *reveals*. It is the clearest evidence yet for the
  project's modest claim — behavioural fidelity changes the answer — and §(g) is
  where it belongs. *(Since 2026-08-01 the instrument can hold it: Row B, §(d2),
  scores it at the recommendation grade.)*

Discrimination check: the criterion separates a result the security metrics
call a uniform failure (ASR 0.00 everywhere) into one demonstrated axis, two
designed axes with named evidence gaps, and an exposed metrics deficit. A
rubric that could not tell those apart would not be worth loading every
session.

## (g) The honest summary — the S6 answer as it stands today

**What this model captures that the prior models in the cross-section do
not:** a multi-stage campaign structure derived from analyst-curated CTI
rather than a scripted compromise loop (axis 1, designed); operational-
objective conditioning that demonstrably changes runtime behaviour (axis 2,
demonstrated); attacker-side branching plurality over an envelope of observed
campaigns, demonstrated by experiment 2 to reach the defence dimension (axis 3,
demonstrated); and a minimal runtime adaptive loop in which
defender resistance feeds back into movement (axis 4, designed) — together
lifting the attacker from the parametric/scripted cluster to the procedural
rung (§(e)).

**What it does not capture:** stealth semantics (axis 5) and MTD-scheme
awareness in any of Jalowski's three forms (axis 8 — ruled out of scope
2026-07-28, not merely absent). These are the remainder of the smart-attacker
half of the literature's diagnosis, and on the current evidence the model also
cannot yet claim persistence or adaptivity in *outcome* terms — the structure
runs, but experiment 1 shows it failing on this substrate in two
profile-determined modes.

**Where axis 7 now sits, which is also neither of those two lists.** A within-run
learning capability exists, is declared and swept, and demonstrably reduces the
attacker's own friction as a run proceeds (axis 7, designed) — so the field-wide
asymmetry Cho names, defender learning everywhere and attacker learning nowhere,
is no longer simply reproduced here. What it cannot claim is that learning makes
the attacker better: compromise breadth *falls* as the capability rises, because
the binary routing verdict the learner updates on is not a progress signal, and a
confident learner correctly concludes that reconnaissance pays and exploitation
does not (§(d) axis 7). That negative is itself a contribution, and a
transferable one — it says that an evaluation which gives an attacker a learning
capability without giving it a progress-carrying reward will measure the attacker
optimising away from the objective, which is a design warning for anyone building
the learning attacker this literature keeps asking for.

**A second experiment has since sharpened that warning into two separable
requirements.** The obvious reading of the negative above is that the reward was
misspecified; the less obvious one is that the belief was keyed on a quantity too
coarse to express the constraint the attacker kept failing. Building the finer key
and sweeping it against both controls separates them
([`pipeline/ogasp/learning_readiness_findings.md`](pipeline/ogasp/learning_readiness_findings.md)):
the representation owned the *collapse* — repair it and the attacker stops
abandoning exploitation and recovers the breadth it had lost — and the reward owns
the *ceiling*, since the repaired learner returns to the no-learning arm's
performance and goes no further. The transferable claim is accordingly stronger
than a single warning: **representation and reward are independent requirements,
and satisfying one buys exactly the part of the failure it owns.** The measurement
warning that rides with it is the sharper practical point — the two representations
are indistinguishable on every friction-shaped measure and separate only on
breadth, so a study scoring attacker learning on the attacker's own friction would
conclude the representation makes no difference, which is the reverse of what it
does.

**Where axis 6 now sits, which is neither of those two lists.** An
incentive/cost decision model exists, is declared and swept, and demonstrably
conditions the attacker's choice of tactic (axis 6, designed) — so the model no
longer inherits the "rationality without capability" diagnosis unqualified. What
it cannot claim is the result that would make the capability *matter* for MTD
evaluation: cost-sensitivity does not change MTD's measured effect on this
substrate, because MTD's tax turns out to be levied in near-proportion to a
tactic's declared dwell and a utility ratio cannot see a proportional surcharge
(§(d) axis 6). That negative is itself a contribution — it is a measured
statement about how this defence distributes cost, which is only sayable at all
because an attacker with a cost model now exists to measure it with.

**And what experiment 2 added, which no axis scores.** The comparative run
across the defence family found that the *ranking* of MTD mechanisms inverts
between the inherited attacker and the profiled one — rank correlation −0.893,
with the diversity family suppressing the vulnerability-exploiting baseline by
roughly 90 % and the profiled attacker by 37–41 %, while the position-destroying
family does the reverse
([`pipeline/ogasp/experiment_02_findings.md`](pipeline/ogasp/experiment_02_findings.md)
§9). The two attackers depend on different substrate properties, so they are
protected by different defences. This is the project's modest claim in its
sharpest form to date: behavioural fidelity does not merely change the magnitude
of an MTD evaluation's answer, it can change **which mechanism the evaluation
recommends**. It is a statement about what the attacker model reveals rather than
about the attacker model itself, which is why it scores on no numbered axis —
since 2026-08-01 the instrument holds it as **Row B**, scored at the
recommendation grade with its caveats in the row (§(d2)). It is directional at ten seeds, and it is bounded by the standing caveat
that the tactic-to-verb mapping remains a chosen input parameter.

The one-sentence form the dissertation can defend: *this model moves MTD
evaluation from scripted attackers to a CTI-grounded, objective-conditioned,
procedurally-adaptive campaign envelope whose plurality demonstrably reaches the
defence dimension — and the criterion records, axis by axis, that the learning,
scheme-aware attacker the literature ultimately calls for remains future work.*

## (h) Lifecycle — when to re-score

Re-score a row (and bump `updated`) when its evidence changes, not on
schedule. Standing triggers: ~~experiment 2 (axes 1–4 badges and the §(f)
demonstration section)~~ **fired 2026-07-29 — axis 3 moved DESIGNED →
DEMONSTRATED on its pre-registered criterion; axes 1 and 4 held, axis 4 on the
verdict-blind control it had never had and axis 1 after a reported move was
withdrawn on cross-examination; axis 2's demonstration extended to the defence
dimension. Scored in §(f2)**; ~~the S3 timing implementation (axis 5's tempo
half)~~ **fired 2026-07-28 — no badge moved; axis 5's body now describes the
built regime, and the badge holds because tempo without a consequence is
still not evasion**; ~~the S1 sensitivity study~~ **fired 2026-07-28 — no
badge moved; axis 2's demonstration is qualified in §(f) and axis 1 gains a
measurement finding** (lifecycle depth reached is saturated: all five
profiles traverse to the objective stage, so the depth measurement the axis-1
M8b recommendation named could not discriminate as written — the
recommendation is corrected in §(d), with the coverage curve leading until
the measurement-suite handoff verifies a replacement); **the rate
feasibility study fired 2026-07-28 — no badge moved; axis 2's evidence is
qualified a second time in §(f), and the study's degenerate-region finding
now stands as a constraint beside the badge definitions in §(b)**; **the
axis-6 utility modulator and its rationality-exponent sweep fired 2026-07-29 —
axis 6 moved NOT ADDRESSED → DESIGNED, and axis 3's branching paragraph is
qualified in §(d), because the decision rule the axis adds trades against
plurality rather than adding to it**; ~~any move
to dynamic weights (axes 4, 7)~~ **fired 2026-07-29 — axis 7 moves NOT
ADDRESSED → DESIGNED on a criterion pre-registered before the runs existed; axis
4 holds, with better evidence than experiment 1 alone gave it, since the routing
weights now do update from experience and still confer no adaptive advantage;
and §(e)'s learning sentence is restated without the placement moving. The badge
stopped short of DEMONSTRATED because the capability was shown to operate
without making the attacker better — and the reason it does not, that the
routing verdict is not a progress signal, is recorded in §(d) as the finding
rather than as a caveat**; **the readiness-keyed generalisation of the learner
fired 2026-08-01 — no badge moved. Axis 7 holds at DESIGNED on the criterion §(d)
already fixed: the generalised learner recovers the breadth the destination-only
key lost and does not exceed the no-learning ablation arm, so the axis-7 M8b field
is updated to record that the representational half of its requirement is
discharged and the credit signal is now the sole remaining item. Axis 3 gains the
measured composition result in §(d) — the modulators' narrowing is sub-additive
rather than compounding, which corrects the reasoning behind the reported-configuration
pin without changing the pin**; any lift of the S2 freeze (axes 6–7, and the
§(e) placement); a defence whose cost is not proportional to a tactic's dwell,
or a utility conditioned on realised success rather than realised time (axis 6
— either is what would move it to DEMONSTRATED, per §(d)); any reversal of the 2026-07-28 ruling that promoted the
three Jalowski primitives to *out of scope* (axis 8 — promotion to *encoded*
would re-open the axis, the S2 freeze's capability candidates, and the §(e)
placement). **The lettered rows (added 2026-08-01) carry their own triggers:**
Row A re-aggregates when any declared family's tier badges change or a new
declared family lands (the ledger precedent's §6 instance list is the
watch-list); Row B re-scores when the comparative evidence on record changes —
the open retrace re-take ruling, the mapping-sensitivity study, or a seed
count that supports a significance claim. Scores move on evidence only — never
change the model, weights, mapping, or metrics to improve a row (S6
constraint; [`../workflows/guardrails.md`](../workflows/guardrails.md)) — and
the constraint binds the lettered rows exactly as it binds the numbered eight.
A distilled, rubric-clearing note for the background or discussion chapter is
the deferred second artefact; this file is the scored instrument it will cite.
