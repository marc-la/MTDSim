# The open chain — dependency order, 2026-07-28

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
seven handoffs allocate that work. (9) and (11) are the two foundations and
unblock most of the rest; (14) is independent of everything.

9. `2026-07-28_axis_measurement_suite.md` — the M8b measurements the criterion's
   claimed axes need, as a **reader** over the movement records: progression,
   traversal diversity, defender-response, and the cost ledger. No model change,
   no ruling needed. **Blocks (10), supplies (12), and should land before (8)
   runs**, because the run workspace is gitignored and a measurement not computed
   at run time means re-running. Also owns the replacement for the saturated
   lifecycle-depth measure.
10. `2026-07-28_axis134_demonstration_arms.md` — pre-registers the badge criteria
    for **persistence, strategic plurality and adaptivity**, and adds the
    verdict-blind ablation arm that separates *reacts* from *adapts usefully*.
    Needs (9); **folds into (8)'s run** rather than running its own matrix.
11. `2026-07-28_attacker_state_seam.md` — the shared foundation for the three
    axes that need a mutable attacker state: a movement-layer `AttackerState`
    observed through the two Protocols the walk already injects, and a
    generalised modulator composition whose null configuration is bit-identical
    to today. **Blocks (12), (13) and the build half of (14).** Carries the
    governance question common to all three — whether a movement-layer state
    collides with the **S2** freeze on attacker states — which is Marc's to
    confirm with the supervisor.
12. `2026-07-28_axis7_learning_capability.md` — within-run knowledge that
    reweights routing from what has worked, with knowledge perishing on MTD
    mutation. Needs (11), consumes (9). **The highest-value item on this wave**:
    it is the literature's sharpest named gap and the only axis whose
    demonstration would move the model's fidelity placement off the procedural
    rung. Also the candidate mitigation for experiment 1's friction failure mode.
13. `2026-07-28_axis6_incentive_rationality.md` — a declared per-tactic benefit
    against the already-declared duration as cost, entering routing as a
    rationality exponent whose zero recovers today exactly. Needs (11), consumes
    (9)'s cost ledger.
14. `2026-07-28_axis5_stealth_conceptualisation.md` — **design only, and it ends
    in a question.** Settles what stealth can mean on a substrate where detection
    is culled by standing project direction. Can start immediately; its build
    half needs (11) and a ruling from Marc. The one item on this chain whose
    central question is not the assistant's to answer.
15. `2026-07-28_criterion_maintenance_and_axis8_closure.md` — rules **MTD-scheme
    awareness** out as future work rather than leaving it merely absent, and
    discharges three fired re-score triggers and four stale cross-references in
    the criterion. Documentation only, independent of everything, and worth doing
    early because the criterion is loaded into every session.

**Off-chain (independent of the waves):**

16. `2026-07-28_intent_spec_conformance_audit.md` — audit the current substrate
    against the new literature-only intent spec
    (`../implementation/mtdsim_intent_spec.md`), classifying every IS-ID and
    producing a disposition list for Marc. Substrate-side and read-only; depends
    on nothing above and blocks nothing above. Marc intends to run it next.

Parked work — parallel or superseded, not on this chain — is in
[`__archive/`](__archive/).
