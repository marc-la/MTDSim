---
status: durable
created: 2026-07-27
updated: 2026-07-27
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

## (c) The scorecard

| # | Axis | Literature source | Prior MTD work (lit review §IV-B cross-section) | This model today |
|---|---|---|---|---|
| 1 | Persistence — multi-stage campaign structure | Cho §V-A; Alshamrani §II-A (NIST i), §II-C | absent throughout | **DESIGNED** |
| 2 | Objective conditioning | Alshamrani §II-A, §II-C | absent | **DEMONSTRATED** |
| 3 | Strategic plurality (multi-strategy branching) | Cho §V-D (dim. 2) | absent | **DESIGNED** |
| 4 | Adaptivity to defender resistance | Cho §V-A; Alshamrani §II-A (NIST ii) | He et al. only, partial and design-time | **DESIGNED** |
| 5 | Stealth — low-and-slow tempo and evasion | Cho §V-A; Alshamrani §II-C; Jalowski §4.3 | He et al. only, in a detection-evasion frame | **NOT ADDRESSED** |
| 6 | Incentive-driven rationality | Cho §V-A, §V-D (dim. 3) | partial RoA operationalisation (Brown, Tay) | **NOT ADDRESSED** |
| 7 | Learning capability | Cho §V-D (dim. 1); Jalowski §4.3 | none | **NOT ADDRESSED** |
| 8 | MTD-scheme awareness (three Jalowski primitives) | Jalowski §4.1, §4.3 | none | **NOT ADDRESSED** |

Four of eight axes are not addressed. That ratio is the honest shape of the
contribution: the model advances the *campaign-structure* half of the APT
profile (axes 1–4) and leaves the *smart-attacker* half (axes 5–8) — the half
Cho's §V-D and Jalowski's corrective name most pointedly — open. §(f) states
what that buys anyway.

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
current suite lacks: deepest tactic band reached per run (kill-chain depth),
distinct-tactic coverage over time, foothold-retention duration across MTD
mutations, and the effort-to-breadth conversion ratio (actions per distinct
host) that experiment 1 computed ad hoc. Recommended, not built.

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
flow-proportion weights, not selected across options by any decision rule
(that is axis 6's gap).

**What would evidence a claim (M8b).** Traversal diversity per profile
(distinct tactic-sequences across seeds; path entropy over the net), and the
experiment-2 matrix showing outcomes vary over both the attacker-profile and
defence-family dimensions rather than one.

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
outcome-reactive re-routing over static weight sets; it does not condition on
the defence itself (axis 8) and does not update from experience (axis 7).
S1's eventual direction — attacker-state-conditioned dynamic weights — is the
named next step, currently deferred.

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
defence-evasion places) but carries no stealth semantics. The nearest open
direction is S3's timing regime — per-tactic exponential dwell, non-action
tactics consuming time — which would give the model a *tempo* axis
(CONJECTURED: ruled, with design and build handoffs open); tempo alone is
still not evasion.

**What would evidence a claim (M8b).** The supervisor's own caveat stands:
measuring stealth is acknowledged tricky (M8b). Candidate supplementary
measurements, if stealth is ever claimed: attack-event rate visible to
substrate statistics per unit time (a detectability proxy), dwell fraction in
non-action tactics, and tempo response to MTD frequency. Any of these
requires the S3 timing regime to land first.

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

**This model today — NOT ADDRESSED.** The movement layer's transition weights
are flow-proportion frequencies — evidence of what campaigns did, not a
cost/benefit calculation — and the outcome overlay is a declared policy, not
a utility. The RoA-ordered exploit selection survives inside the inherited
action layer the controller dispatches to, so the model inherits exactly the
partial credit Table II gives Brown and Tay, and adds nothing on this axis.
No design commitment exists; R3's characteristics-based attacker *styles*
(speed, success rate) are the nearest parked direction and are not a utility
model either.

**What would evidence a claim (M8b).** A cost ledger per run (actions, time,
re-work forced by MTD) reported as an attacker-side metric would be the
prerequisite measurement; a claim on this axis additionally needs a decision
rule that consumes it, which is model change beyond the S2 freeze —
explicitly not recommended now.

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

**This model today — NOT ADDRESSED.** Attacker learning is a documented
substrate divergence (ATK-04, unimplemented;
[`metrics_semantics.md`](metrics_semantics.md)). The movement attacker carries
no memory across runs and no within-run knowledge accumulation beyond the
token's position and the binary verdict at the current place. Dynamic
attacker-state-conditioned weights (S1's eventual direction) and the
attacker-that-studies-the-MTD (M8d) are both explicitly future work; the
capability hooks exist, the behaviour is not built.

**What would evidence a claim (M8b).** Within-run knowledge metrics (does
success probability against a host class rise with exposure?) and
cross-mutation retention (does the attacker re-acquire targets faster after
the nth shuffle?). Neither is meaningful until some learning mechanism
exists; recorded here so the axis has its yardstick when the freeze lifts.

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

**This model today — NOT ADDRESSED.** All three primitives are recorded as
*pending encoding* in [`architecture.md`](architecture.md) §(f), and none has
been promoted: the attacker keeps no cross-target configuration memory (i),
does not observe defender event frequency (ii), and its observation surface
is CVE/CVSS-only, with metadata invariance likely out of scope for the
encoded subset because it requires extending the substrate's
attacker-observation seam (iii). The encoded subset bounds the contribution
(§(f)); today that subset is empty, and this row is the criterion's
bluntest honest negative.

**What would evidence a claim (M8b).** Per primitive: (i) repeat-compromise
rate on previously-seen configurations vs unseen; (ii) correlation between
attacker target-selection and defender mutation frequency (the natural
inverse of Tay's IDS-sensitivity experiment, per §(f)); (iii) any
invariant-feature observation channel at all. Each presupposes the primitive
being encoded — a lift of the S2 freeze and a fresh comparability argument,
not current work.

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
intent and motivation conditioning are present (axes 1–2); learning capability
is absent (axis 7). The placement claim is therefore: **the first model in
this cross-section's frame to reach the procedural rung, carrying two of the
three behavioural-rung components, and not a behavioural model** — that rung
requires learning this model does not have.

## (f) Experiment 1 scored against the criterion

The rubric has to discriminate, not merely assert. Applied to the one result
on record ([`pipeline/ogasp/experiment_01_findings.md`](pipeline/ogasp/experiment_01_findings.md)):

- **Axis 2 gains its DEMONSTRATED badge from this run.** Profile identity
  determines failure mode (friction vs churn vs sink) independent of seed —
  runtime behaviour is objective-conditioned. Under the criterion this is the
  experiment's positive finding, invisible to the headline security metrics.
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
campaigns (axis 3, designed); and a minimal runtime adaptive loop in which
defender resistance feeds back into movement (axis 4, designed) — together
lifting the attacker from the parametric/scripted cluster to the procedural
rung (§(e)).

**What it does not capture:** stealth semantics (axis 5), an incentive/cost
decision model (axis 6), learning (axis 7), and MTD-scheme awareness in any
of Jalowski's three forms (axis 8). These are precisely the smart-attacker
half of the literature's diagnosis, and on the current evidence the model
also cannot yet claim persistence or adaptivity in *outcome* terms — the
structure runs, but experiment 1 shows it failing on this substrate in two
profile-determined modes.

The one-sentence form the dissertation can defend: *this model moves MTD
evaluation from scripted attackers to a CTI-grounded, objective-conditioned,
procedurally-adaptive campaign envelope — and the criterion records, axis by
axis, that the learning, scheme-aware attacker the literature ultimately
calls for remains future work.*

## (h) Lifecycle — when to re-score

Re-score a row (and bump `updated`) when its evidence changes, not on
schedule. Standing triggers: experiment 2 (axes 1–4 badges and the §(f)
demonstration section); the S3 timing implementation (axis 5's tempo half);
the S1 sensitivity study and any move to dynamic weights (axes 4, 7); any
lift of the S2 freeze or promotion of a Jalowski primitive from *pending*
(axes 6–8, and the §(e) placement). Scores move on evidence only — never
change the model, weights, mapping, or metrics to improve a row (S6
constraint; [`../workflows/guardrails.md`](../workflows/guardrails.md)).
A distilled, rubric-clearing note for the background or discussion chapter is
the deferred second artefact; this file is the scored instrument it will cite.
