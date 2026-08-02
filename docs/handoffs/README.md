# The open chain — dependency order, 2026-07-29

`ls docs/handoffs/` is the inventory of open work; this file carries only the
thing a directory listing cannot — **what depends on what**. Waves 1–4 execute
the post-experiment-1 supervisor rulings
(`docs/implementation/pipeline/ogasp/supervisor_decision_register.md` §S1–S6).
**Wave 5 executes the criterion those rulings produced** — it works axis by axis
through `docs/implementation/apt_model_criterion.md`, moving what can honestly be
moved and ruling out what cannot.
Delete a handoff in the commit that ships its work, and prune its line here in
the same commit. *(Shipped from this chain: the S6 criterion — now
`docs/implementation/apt_model_criterion.md`, on the read-first list; the S1
lifecycle consensus — now
`docs/implementation/pipeline/ogasp/lifecycle_consensus.md` +
`data/ogasp/controller/lifecycle_consensus.json`; the S2 action-layer audit —
now `docs/implementation/pipeline/ogasp/action_layer_audit.md`.)*

**Waves 1 and 2 are clear.** All five of their handoffs have shipped.

> **Four decisions from the S2 audit are waiting on Marc**, and three of them
> block trusting experiment 2's numbers rather than blocking a handoff. Read
> [`../implementation/pipeline/ogasp/action_layer_audit.md`](../implementation/pipeline/ogasp/action_layer_audit.md)
> § "The four decisions this audit cannot make" before starting the comparative
> run in (8). Two of them (the confusion penalty and the dwell-time interrupt
> gate) land squarely in (5)/(7)'s scope, so pick them up there.

**Wave 2 is clear**, so waves 3 and 4 are open.

*(Shipped from wave 2: the **S4 partial mapping** —
`2026-07-27_controller_v2_partial_mapping.md`, landed 2026-07-28 as
`../implementation/pipeline/ogasp/controller_mapping_v2.md` plus the versioned
registry at `data/ogasp/controller/mappings/`. Mappings are now selectable data:
the controller layer reads a version by name, `v1_ckc_total` stays the default so
experiment 1 reproduces unqualified, and experiment 2 names `v2_partial` at its
own seam. Seven tactics are dwell-only and run end to end. — And the S3 timing
**design**: `2026-07-27_stochastic_timing_design.md`, landed 2026-07-28 as
`../implementation/pipeline/ogasp/stochastic_timing_design.md`, ruling the GSPN
formalism, where the clock lives (the movement layer supplies the time, SimPy
spends it), the exponential rates and their literature defence, that the confusion
penalty **stays substrate-side** on portability grounds, the comparability
argument, and the determinism/migration/rollback scheme. — And the S3 timing
**build**: `2026-07-27_stochastic_timing_implementation.md`, landed 2026-07-28.
Each tactic's dwell is now a draw whose mean is its declared catalogue value, from
a third, isolated random stream; the catalogue's metadata declares the movement
layer's stochastic reading alongside the timeline runner's unchanged point
reading; and the confusion penalty stayed where it was, with its single-charge
property tightened into a guard rather than re-homed. — **Then S3-R, the same day:**
Marc reversed the design record's §2 and retired the hybrid it had ruled. The
movement layer now supplies **every** unit of the attacker's time — a tactic's draw
*is* the dispatched action's duration, so the same verb costs different amounts
under different tactics — and the substrate's `ATTACK_DURATION` / `exploit_time` are
no longer consumed on that arm, taking the complexity scaling, the OS-mismatch
multiplier and the ATK-04 re-exploit discount out of play there. A blocked attempt
now costs its tactic's time rather than being free. Internal MTTC is ruled a
substrate-owned metric that the portable layer does not own, and cross-arm
comparability of it is withdrawn rather than defended.)*

**Wave 3 — shipped.**

*(Shipped from wave 3: the **S1 study half** —
`2026-07-27_tactic_weight_sensitivity_study.md`, landed 2026-07-28 as
`../implementation/pipeline/ogasp/weight_sensitivity_study.md`. The
lifecycle-distance term is folded into the outcome rules with **no R2 rule value
changed**, the `relationship` term is re-sourced from the consensus stages (the
open §5 decision, taken on coherence and provenance grounds), the compiled views
are now a versioned registry at `data/ogasp/controller/overlays/` with experiment
1's version frozen and still the default, and a tracked generator's `--check`
re-derives every committed cell. The sweep verdict is **mixed and reported as
such**: ASR-zero and MTD-invariance hold across the declared bands, the
intermediate profile's failure-mode classification and any profile ordering by
progress move — the latter for want of seeds rather than want of parameter
discipline — and the floor `z` is behaviourally inert because the corpus carries
no three-stage transition, which also means S1's motivating pair never routed any
mass. Three things (8) inherits: the ~90% MTD host-suppression under `v2_partial`
to confirm or withdraw, the seed count an ordering claim needs, and a saturated
progression metric to replace.)*

*(Shipped from wave 3: the **rate analysis** —
`2026-07-28_tactic_rate_feasibility_study.md`, landed 2026-07-28 as
`../implementation/pipeline/ogasp/rate_feasibility_study.md`, with its verdict
folded into the timing design record §3 and the evaluation-burden note's second
instalment. It took the S1 study's reporting shape as directed: conclusions and
criteria committed in their own commit **before any output existed**, one-at-a-time
anchor ends then the ratio corners, per-conclusion held/moved verdicts. The four
group anchors were swept over bands derived from the catalogue two independent ways
that agree, so no band was widened.

**HELD across the declared bands, under both timing regimes:** the profiled attacker
is slower to first compromise than the baseline in every cell, and MTD never helps
the attacker anywhere. **INDETERMINATE:** any profile ordering by progress — the
same power failure the S1 study found, reached by an unrelated parameter family,
which converts a suspicion into a settled constraint. **The identifiability result:**
of the four anchors only `stealth-low-and-slow` moves any outcome; the two Tier-1
substrate-priced anchors are inert across their bands, which is the tier badges'
own prediction arrived at independently.

Two findings (8) inherits, both consequential. **The evaluation's operating mutation
interval sits inside a degenerate region** where *neither* attacker completes the
objective — the baseline included, which was not known — and the objective only
becomes reachable above ~1600 s. ASR cannot discriminate at the operating point, so
experiment 2 must choose its interval deliberately rather than inherit 200 s, and no
defence ranking taken inside that region means anything. **And the distribution
family is a live parameter at one corner:** under S3-R a same-mean Erlang-4 costs
the attacker breadth at long stealth dwells under mutation pressure, so the
mean-is-load-bearing defence is now scope-measured rather than assumed.

Also recorded: the study ran once under the hybrid regime and was re-run in full
under S3-R after the reversal; the baseline arm's behaviour has moved since
experiment 1 published its figures, so those magnitudes are stale as a comparison
target.)*

**Wave 4 — last.**

*(Shipped from wave 4: **S5 + the comparative run** —
`2026-07-27_sink_retrace_experiment2.md`, run 2026-07-29 and reconciled to `dev`
2026-08-01. The sink policy landed as
[`../implementation/pipeline/ogasp/sink_retrace_design.md`](../implementation/pipeline/ogasp/sink_retrace_design.md)'s
`retrace_sinks` — two parallel derivations built it independently, and this is
the surviving implementation, with `sink_policy.md` kept beside it as a
superseded record whose §3 inventory is lifted into the survivor. The
comparative run landed as
[`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md):
2 760 runs over the full defence family, the mutation interval carried as a
dimension (the inherited 200 s plus a deliberately-chosen point outside the
degenerate region), both declared inputs named at its seam as this entry
required. Headline: the defence ranking inverts between the inherited and the
profiled attacker (ρ = −0.893); axis 3 moved to DEMONSTRATED on its
pre-registered criterion, axis 1's reported move was withdrawn on
cross-examination. One loose end is recorded rather than resolved: the
retrace-arm cells ran under the superseded sink implementation, and whether they
are re-taken under the landed one is a ruling for Marc — see the findings
record's reconciliation note.)*

**Wave 5 — the criterion, axis by axis.** Eight axes are scored in
`docs/implementation/apt_model_criterion.md`; four of them can move on evidence,
two need a new mechanism, one needs a ruling, and one is now ruled out. These
handoffs allocate that work. (11) is the remaining foundation and unblocks most
of the rest; (14) is independent of everything.

*(Shipped from wave 5: the **axis-measurement suite** —
`2026-07-28_axis_measurement_suite.md`, landed 2026-07-28 as
`src/mtdsim/l3_simulation/movement/measures.py` (reader-only sibling to the
MTTC/ASR reader, with the baseline-arm row adapter and the interval helper) plus
the tracked record `../implementation/pipeline/ogasp/measurement_suite.md`.
All gates ran: the suite re-derives the fresh experiment-1 figures with a
50-run × 5-field exact cross-check; the confusion penalty is **derived** from
interrupted records rather than added to the schema, verified on a seeded run;
the cross-arm subset computes on both arms with event-wise-only comparability
enforced in the API. Gate 3's verdict is split and recorded:
deepest-successfully-actioned stage discriminates under `v1_ckc_total`
(separates `pure_steal`–`aggregate` where visited depth separates nothing) but
is structurally truncated under `v2_partial` (the dwell-only objective band can
hold no verdict, ceiling 2) — adopted with the coverage curve as its mandatory
companion. (10), (12) and (13) consume the shipped module directly; (8) can now
compute these measures at run time.)*

*(Shipped from wave 5: the **axis-1/3/4 demonstration arms** —
`2026-07-28_axis134_demonstration_arms.md`, folded into experiment 2's run as it
directed and deleted with the reconciliation on 2026-08-01. Its pre-registered
badge criteria and its verdict-blind ablation arm are what let that run move axis
3 to DEMONSTRATED, hold axis 4 on the control it had never had, and withdraw
axis 1's reported move on cross-examination — recorded in
[`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md)
§§11–13 and scored in the criterion §(f2).)*
*(Shipped from wave 5: the **attacker-state seam** —
`2026-07-28_attacker_state_seam.md`, landed 2026-07-28 as
`src/mtdsim/l3_simulation/movement/state.py` plus the tracked record
`../implementation/pipeline/ogasp/attacker_state_seam.md`. A movement-layer-only
`AttackerState` observed through the two Protocols the walk already injects
(`StatefulTiming` wraps timing, `ModulatedOverlay` wraps the overlay — zero edits
to the driver), and the generalised three-factor composition
`base · overlay_v · Π_m` whose **null configuration is bit-identical to today** —
proven field-for-field across 5 profiles × 5 seeds × 2 MTD conditions × 2
mappings. The one driver edit — routing dwell-only places through `compose` under
a distinguished `"none"` verdict so the state sees every routing decision — is
proven behaviour-neutral by a 100-configuration before/after capture (0 differ).
A fourth, isolated RNG stream (`derive_state_seed`, XOR "STAT"); a zeroing
modulator refused without a declared rule; the STATE trace actor and `--demo-state`.
**No value is declared and no badge moved** — the seam ships null. (12), (13) and
the build half of (14) consume it directly.

**The governance question rides with it, unresolved:** the record §7 writes out
the argument that a within-run, movement-layer, null-equivalent state is M7
refinement rather than the attacker-state change **S2** freezes — for Marc to
confirm with the supervisor. Until confirmed, no modulator carrying a declared
value is wired into any experiment; the null mechanism is safe regardless.)*

*(Shipped from wave 5: the **axis-7 learning capability** —
`2026-07-28_axis7_learning_capability.md`, landed 2026-07-29 as
`src/mtdsim/l3_simulation/movement/learning.py`, the declared family at
`data/ogasp/movement/learning_rules.json` and the record
`../implementation/pipeline/ogasp/learning_capability.md`. The attacker now
carries a within-run belief about which tactics pay — a place-keyed Laplace
estimate over observed verdicts, entering routing as `Q(b)^κ` — that perishes by a
declared fraction `ρ` on every MTD mutation. `κ = 0` is bit-identical to today.
The seam gained a **third wrapper** (`StatefulAttackOperation`, hooking the one
`apply_mtd_interrupt_cost` every interrupt path funnels through, because an
interrupt reaches `compose` already flattened into an ordinary failure verdict)
plus a modulator observation fan-out; the driver is still not edited.

The six conclusions and the badge criterion were **committed before any run
existed** (`876bca2`), then 2 400 runs were swept over both declared bands on both
mappings. **The mechanism works and does not help.** On experiment 1's mapping the
attacker drives its own blocked fraction from 91 % to 21 %, and does so *within*
runs against an ablation arm that improves only slightly on its own — so the
friction failure mode is substantially self-correcting given an attacker allowed
to adapt to the coupling, and the discovery is the model's rather than the
modeller's. But compromise **breadth collapses** as the capability rises (6.5
hosts → 0.8), because the binary routing verdict is not a progress signal:
scanning succeeds far more often than exploiting, so the learner correctly
concludes reconnaissance pays and stops attacking (`EXPLOIT_VULN` falls from 13 %
of its successes to 1 %). Path entropy falls in all ten profile × mapping cells,
so axes 3 and 7 pull against each other. And MTD is severely effective against the
learner — most of the advantage is gone by ρ = 0.25 — which is a defence effect no
existing metric could register, since what a mutation destroys here is an estimate
rather than a foothold.

**Axis 7 moves NOT ADDRESSED → DESIGNED**, stopping short of DEMONSTRATED on the
pre-registered criterion; §(e)'s learning sentence is restated but the fidelity
placement does **not** move. (8) inherits one thing: a learning arm is worth
running only once the learner's credit signal carries progress rather than the
routing verdict, which is a credit-assignment redesign and not a parameter
change.)*
*(Shipped from wave 5: **axis 6, incentive-driven rationality** —
`2026-07-28_axis6_incentive_rationality.md`, landed 2026-07-29 as
`src/mtdsim/l3_simulation/movement/utility.py`, the declared family
`data/ogasp/attacker_utility.json` (+ its generated 75-cell view), and the
tracked record `../implementation/pipeline/ogasp/incentive_rationality.md`.
A utility modulator on the seam — `(u(b)/ū)^λ` with `u = benefit / cost` — where
the **cost half reuses the duration catalogue** and the one new declared family
is the benefit, rule-generated from objective proximity *within the profile* so
it differs between profiles and never depends on the source (the two properties
that keep it from restating the overlay's distance kernel). λ = 0 is
**bit-identical** to today, asserted across 5 profiles × 5 seeds × 2 mappings ×
2 MTD conditions.

**The sweep's verdict is a mixed one, and the negative is the interesting
half.** 1 800 runs against six conclusions committed before it ran: five held,
and **C4 — the result the axis exists to produce — moved**. Cost-sensitivity
does *not* change MTD's measured effect, because MTD's tax on this substrate is
levied in near-proportion to a tactic's declared dwell (a ~9 % surcharge across
an 18-fold absolute spread) and a normalised utility *ratio* cannot see a
proportional surcharge. Two held conclusions are worth carrying forward: rising
λ collapses path entropy (2.23 → 0.24 bits), and cost-sensitivity **costs**
progress — blocked attempts rise from 49 % to 99 % of actions, because the
cheapest tactics are the most precondition-coupled, which is experiment 1's
H-coupling finding in economic terms. Axis 6 moved **NOT ADDRESSED →
DESIGNED**; DEMONSTRATED is withheld and what would earn it is recorded in the
criterion's axis-6 M8b field — a defence whose cost is *not* dwell-proportional
(reachable inside (8)'s defence family), or a utility conditioned on realised
success rather than realised time. (8) should note the first of those.)*
14. **Shipped (design half) 2026-07-28** — the axis-5 stealth design record landed
    as `../implementation/pipeline/ogasp/stealth_conceptualisation.md`. It leads
    with the stealthy-versus-baseline contrast (Jin's framing, characterised on
    event-wise measures), answers all eight questions, and records the Tay
    verification: the reactive `mtd_ai` defender **does** key on attacker-activity
    signals, so option 1(b) is **live** — a stealthy tempo can be made
    consequential against `mtd_ai` unchanged, which is the route to DEMONSTRATED
    on axis 5a. The record proposes a **tempo/evasion badge split** (5a
    evidenceable, 5b NOT ADDRESSED) and carries a four-item decision request for
    Marc (§13). **The build half remains open**; the state seam it needed has
    shipped (above), so it is now gated only on Marc's rulings — chiefly whether
    to sanction the `mtd_ai` defence arm (1b) and the S2 freeze question. No badge
    was moved; the split awaits Marc's agreement.
*(Shipped from wave 5: the **criterion maintenance and axis-8 closure** —
`2026-07-28_criterion_maintenance_and_axis8_closure.md`, landed 2026-07-28
(`871ac9f`). MTD-scheme awareness is ruled out as future work on the
ML/RL-versus-timeframe ruling rather than left merely absent, the S3 and
rate-study re-score triggers are recorded as fired with no badge moved, the
degenerate region stands as a constraint beside the badges, and the lagged
worked examples recompute under δ = 0.25 with zero compiled cells moving.)*

**Off the chain — two findings ledgers, relocated 2026-08-01.**

Entries 16 and 17 were never handoffs: both declared they commissioned no work
and set no validation gate, so neither could ever be "shipped and deleted", and
they made this inventory of *open work* inaccurate. By the placement criterion in
[`../workflows/docs_map.md`](../workflows/docs_map.md) they are investigation
records, and they now live as such:

- [`../implementation/pipeline/ogasp/fidelity_implications.md`](../implementation/pipeline/ogasp/fidelity_implications.md)
  — the axis-6 session's eight findings (F1–F8) re-read under the thesis framing
  *what does greater attack fidelity imply for current evaluation methods of
  MTD?* Read it before designing any new attacker-fidelity mechanism: it says
  which kinds **cannot** change what an evaluation measures. F2 and F5 were
  independently re-measured on the post-disposition substrate on 2026-08-01 and
  reproduce.
- [`../implementation/pipeline/ogasp/learning_axis_evaluation_findings.md`](../implementation/pipeline/ogasp/learning_axis_evaluation_findings.md)
  — the axis-7 session's ledger plus its design post-mortem. Its forward-looking
  half is **discharged**: the per-place-scalar diagnosis was taken up, the
  readiness generalisation was built and swept, and axis 7 holds at DESIGNED
  (`learning_readiness_findings.md`). Its value is now historical.

> **Two decisions sit with Marc and are attached to no handoff**, recorded here
> because this README is where a cold session looks for open work and those
> records no longer sit in this directory:
>
> 1. **Axis-7 framing** — the shipped axis-7 records report the axis in
>    *performance* terms and thereby under-report the finding. Whether they are
>    re-framed, and whether the badge is re-pre-registered under a *property*
>    criterion, are dispositions rather than housekeeping
>    (`learning_axis_evaluation_findings.md`, end).
> 2. **D-09** — whether Zhang's unimplemented MTD-interruption give-up threshold
>    (IS-INT-06) is wanted, and in which form. It blocks (23) entirely; see
>    [`../implementation/intent_conformance_audit.md`](../implementation/intent_conformance_audit.md).

**Wave 6 — the freeze, and what follows it (2026-07-29).** The attacker model is
frozen: [`../implementation/pipeline/ogasp/model_scope_freeze.md`](../implementation/pipeline/ogasp/model_scope_freeze.md)
fixes the per-axis disposition, classifies each remaining gap as **mechanism /
measurement / governance**, and names what is future work for a successor. Two of
eight axes are demonstrated, four are designed with measured negatives, two are
ruled out. Read it before opening anything below.

*(Shipped from wave 6: **the blocking reconciliation** —
`2026-07-29_reconcile_stranded_axis_work.md`, landed 2026-08-01 as two merge
commits on `dev` (`feat/axis134-demonstration-arms`, then
`feat/exp02-ashen-lynx`). Both axis records arrived filled in with their sweep
verdicts, the criterion table reads 2 DEMONSTRATED / 4 DESIGNED / 2 NOT
ADDRESSED with its prose agreeing — verified against the freeze §2 — and the
four shipped handoffs it covered, (8), (10) and the two axis handoffs, were
deleted in those merges. The demonstration-arms sink implementation survived,
per the handoff's ruling; `sink_policy.md` is kept superseded beside it with its
§3 inventory lifted into the survivor, and the experiment-2 analysis was re-run
from the recorded runs against the reconciled code, reproducing every verdict
byte-for-byte. One loose end is recorded rather than resolved: the handoff's
premise that only the sink sub-study ran under the superseded implementation was
wrong — the main matrix's retrace arms did too — so whether those cells are
re-taken is an open ruling for Marc, recorded in the findings record's
reconciliation note. The wave below is unblocked.)*
*(Shipped from wave 6: **learning under procedural rigidity** —
`2026-07-29_learning_under_procedural_rigidity.md`, landed 2026-08-01. The
representation was settled before any code, in the shape the four prior studies
used: four candidate keys ranked coarsest to finest against a **measured**
per-cell observation budget, with the decisive measurement being that an unmet
precondition is a *deterministic* failure (0.000 success over 14 000+
observations), so the marginal a destination-keyed learner holds is a mixture of a
paying regime and a certain-failure one
(`../implementation/pipeline/ogasp/learning_representation.md`). The ruling is the
one-bit `(destination tactic, precondition-satisfied?)` key — the smallest that
captures the dependency exactly, and the densest of those that work; the chain and
phase keys spend 2–4× the evidence per cell on resolution the constraint does not
use. No RL: no eligibility trace, no discount factor, no value function.

The build transcribes the substrate's precondition guard into a declared,
versioned controller artefact (`data/ogasp/controller/precondition_relation.json`)
that the learner consults against its **own trajectory**, reading no substrate
state — so the scheme-awareness exclusion is untouched, and the artefact is what an
adopter re-declares when porting. It predicts the substrate's block flag exactly on
`v1_ckc_total` (12 281/12 281) and at 92–94 % on `v2_partial`, the residual being
the declared optimism about empty scans, left in because closing it would require
the privileged read the in-layer derivation exists to avoid.

**The sweep's verdict is a clean split, and the badge did not move.** 4 600 runs
over seven criteria committed before any output existed (`97c54a5`), with a third
arm — the destination-only learner at the same point — so "the generalisation did
something" is separable from "learning did something". The representational defect
was real and is repaired: breadth recovers 3.38 → 4.52 hosts at the declared
capability, the high-capability collapse is arrested 1.02 → 2.40, exploitation's
share of successes returns from 6.0 % to 9.5 %, and the readiness key costs less
plurality at every step. But the **no-learning ablation arm sits at 4.60** and the
repaired learner never passes it, so R1 moved and **axis 7 holds at DESIGNED** —
the shape the pre-registration named in advance. The contribution is the isolation:
representation and reward are independent requirements, the representation is now
discharged, and a progress-carrying credit signal is the *sole* remaining item on
the axis. One measurement warning rides with it — the two keys are
indistinguishable to three decimals on every friction-shaped measure and separate
only on breadth, so the within-run blocked-fraction measure cannot discriminate
between representations.

Also shipped: the **composition register**
(`../implementation/pipeline/ogasp/modulator_composition.md`) stating every routing
factor, its seam, and whether the reported configuration runs it — the seam split
as the portability claim made structural. And the **joint-composition check** the
three modulator families had never had, which **falsified the freeze's
precautionary inference**: composing the two built modulators is *sub-additive*,
not compounding — they pull opposite ways on the same edges, and the learner
recovers most of the breadth the utility modulator costs. The pin on the reported
configuration stands on its other leg, and the freeze and criterion records are
corrected accordingly.)*
*(Shipped from wave 6: the **rational attacker and the MTD trade-off** —
`2026-07-29_rational_attacker_and_mtd_tradeoff.md`, both halves landed
2026-08-01 and the handoff retired. **Part 1** as
`../implementation/pipeline/ogasp/cost_model_plain.md`: the plain statement of
what the cost-sensitive attacker computes, plus the simplification verdict —
the benefit family survived attempted removal against a pre-registered bar
(31 of 40 cells fail reproduction without it), cost stays the declared
duration, the exponent stays. **Part 2** as the defender-side disruption
ledger in `movement/measures.py` §5 (derived entirely from the substrate's own
per-mutation records — no declared value) plus
`../implementation/pipeline/ogasp/mtd_disruption_frontier.md`: a 960-run
pre-registered matrix over the full defence family at both intervals, reported
as a frontier and never a composite score. Headline: the *shape* of MTD's
trade inverts with the attacker — against the inherited attacker Service
Diversity dominates the whole family (best suppression at lowest disruption,
no trade at all), while against the profiled attacker suppression is bought at
a near-fixed disruption price and six of seven conditions are Pareto-efficient.
The 200 s operating interval is measured as an extreme-disruption regime
(35–70 % of the run under active reconfiguration), and the experiment-2
ranking inversion reproduces on the post-disposition substrate (−0.857 against
the recorded −0.893).)*
20. `2026-07-29_stealth_tempo_via_dwell_channel.md` — the only route by which tempo
    becomes consequential: dwell alters the metrics the reactive selector reads.
    **Needs a supervisor ruling before anything is built.**
*(Shipped from wave 6: the **iterated cost model** —
`2026-08-01_iterated_cost_model.md`, ruled on and landed 2026-08-02 (option 4,
both changes as three arms, S2 cleared). The R2 defect is repairable with no new
declared magnitude and the repair measurably reaches it — the blocked-fraction
rise is 73–89 % undone in the pooled `v2_partial` cells and successes per action
roughly double — but not at the per-profile resolution U2 demanded (3 of 30
cells), so the stopping rule fired and nothing was re-specified. **The axis-6
badge does not move, and the reason is the finding**: U3's criterion, taken
verbatim from C4 for comparability, is passed by the `declared` arm — the model
F6 proved cannot see MTD at all — so the statistic cannot discriminate and the
badge was declined rather than taken on a threshold. Two results travel further
than the axis: the brief's ranking inverted (the recommended expected-cost change
fails; the benefit-through-the-net change is what pays), and that change is the
first modulator configuration measured here that does **not** narrow traversal.
Record: `../implementation/pipeline/ogasp/iterated_cost_model.md`.)*
*(Shipped from wave 6: the **criterion's consequence and provenance rows** —
`2026-07-29_criterion_consequence_and_provenance_rows.md`, landed 2026-08-01 in
two commits — definitions and evidence bars first, scores second, so the
additions cannot be reverse-fitted to the result that prompted them. The
criterion now carries lettered rows A and B beside the eight numbered axes
(§(c), §(d2), unrenumbered): Row A aggregates the existing tier badges to
roughly a sixth of ledgered values externally fixed, two-fifths carrying any
external anchor and three-fifths declared judgement, with the structural layer
corpus-grounded in full — the modest, non-binary provenance answer. Row B
scores the defence-ranking inversion at the **recommendation** grade (the
top-ranked mechanism changes with the attacker) at the operating interval,
directionally at ten seeds, with the interval dependence, the mapping boundary
and the open retrace re-take ruling carried in the row. The badge census is
flagged as non-additive in §(b), and the fifth-badge question — a measured
negative versus an unevidenced absence, both currently DESIGNED — is recorded
there for Marc rather than decided.)*
*(Shipped from wave 6: the **dissertation notes from the frozen model** —
`2026-07-29_dissertation_notes_from_the_frozen_model.md`, landed 2026-08-01.
Five new notes: the defence-ranking inversion and the operating-point
discrimination rule in `../notes/ch5_evaluation/`, the procedural-mismatch
artefact and the silent-instrument-failure synthesis in
`../notes/ch6_discussion/`, and the host-simulator contract in
`../notes/ch4_implementation/`. The handoff's fourth note — the misspecified
learning reward — was already covered by
`../notes/ch6_discussion/learning_without_context.md`, which landed with the
post-freeze direction restructure and states the same transferable claim; it
was verified against the brief rather than duplicated. The measurement-failure
thread the handoff flagged as a deliberate decision became its own note (the
synthesis), with the motif cross-referenced from the notes it runs through.)*

23. `2026-08-01_attacker_disengagement_measure.md` — make attacker *abandonment*
    measurable: a projected-effort reading over existing runs, reported as a
    frontier over the attacker's patience, so MTD's own economic claim (raise the
    cost until they leave) becomes scorable. It generalises **IS-INT-06**, the
    Zhang give-up threshold the audit classifies DIVERGES-DOCUMENTED-NOWHERE, and
    is therefore **blocked on Marc's D-09 ruling** — read that row before
    anything. Design only so far; the build is a reader, so it moves no golden.
    Descends from Part 1 of the rational-attacker brief (shipped; record at
    `../implementation/pipeline/ogasp/cost_model_plain.md`): the cost model
    cannot express abandonment because a normalised ratio has no scale, and MTD
    turns out to destroy productive *capacity* rather than accumulated gains.
    Two things ride on it — it would give the degenerate region a
    discriminating outcome variable where ASR is pinned at zero, and it is the
    natural attacker-side axis to pair with the shipped disruption frontier
    (`../implementation/pipeline/ogasp/mtd_disruption_frontier.md`) in a
    successor reading.

Parked work — parallel or superseded, not on this chain — is in
[`__archive/`](__archive/).
