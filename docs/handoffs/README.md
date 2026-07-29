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

8. `2026-07-27_sink_retrace_experiment2.md` (**S5** + the comparative run) — its
   design half is **unblocked**; its *run* should consume the two shipped wave-3 studies or it will need
   repeating, and must name **both** its declared inputs at its own seam:
   `v2_partial` as its mapping version and — **corrected 2026-07-28** —
   `v3_persistent_backward` as its overlay version, not `v2_lifecycle_distance`.
   The handoff body and the wave-3 note above both predate Marc's persistence
   ruling; the weight study §3b is the later statement and v3 is the go-forward
   version. It now also
   runs on the stochastic timing regime, so its elapsed-time results carry the
   behavioural tempo and must be reported under the shape-not-scale discipline —
   a ranking that survives the sweep is a result, a magnitude is a parameter
   choice. Carries the full defence-family sweep the first experiment deferred.
   Two further inheritances, both from wave 5: it must **choose its mutation
   interval deliberately** rather than inherit 200 s (which the rate study placed
   inside a degenerate region where ASR cannot discriminate), and its run should
   carry the arms and reporting in (10) below rather than being repeated for them.

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

10. `2026-07-28_axis134_demonstration_arms.md` — pre-registers the badge criteria
    for **persistence, strategic plurality and adaptivity**, and adds the
    verdict-blind ablation arm that separates *reacts* from *adapts usefully*.
    Its measurement dependency has shipped (the suite above); **folds into
    (8)'s run** rather than running its own matrix.
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
15. `2026-07-28_criterion_maintenance_and_axis8_closure.md` — rules **MTD-scheme
    awareness** out as future work rather than leaving it merely absent, and
    discharges three fired re-score triggers and four stale cross-references in
    the criterion. Documentation only, independent of everything, and worth doing
    early because the criterion is loaded into every session.

Parked work — parallel or superseded, not on this chain — is in
[`__archive/`](__archive/).
