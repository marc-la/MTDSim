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

12. `2026-07-28_axis7_learning_capability.md` — within-run knowledge that
    reweights routing from what has worked, with knowledge perishing on MTD
    mutation. The seam it needs has shipped (above); consumes the shipped
    measurement suite. **The highest-value item on this wave**:
    it is the literature's sharpest named gap and the only axis whose
    demonstration would move the model's fidelity placement off the procedural
    rung. Also the candidate mitigation for experiment 1's friction failure mode.
13. `2026-07-28_axis6_incentive_rationality.md` — a declared per-tactic benefit
    against the already-declared duration as cost, entering routing as a
    rationality exponent whose zero recovers today exactly. The seam it needs has
    shipped (above); consumes the shipped suite's cost ledger.
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
18. `2026-07-29_learning_under_procedural_rigidity.md` — generalise the learner so
    it can represent a precondition constraint, without RL. Absorbs the
    FSM-alignment factor and the composition/seam-split brief. Unblocked
    2026-08-01 by the reconciliation.
19. `2026-07-29_rational_attacker_and_mtd_tradeoff.md` — explain the cost model
    plainly, simplify it, and pair it with a calibrated disruption metric so the
    run carries cost-of-moving against risk-of-not-moving. Unblocked 2026-08-01
    by the reconciliation.
20. `2026-07-29_stealth_tempo_via_dwell_channel.md` — the only route by which tempo
    becomes consequential: dwell alters the metrics the reactive selector reads.
    **Needs a supervisor ruling before anything is built.**
21. `2026-07-29_criterion_consequence_and_provenance_rows.md` — the two rows the
    criterion cannot currently score, because the project's largest result (the
    defence-ranking inversion) scores on none of the existing eight. Cheap,
    documentation only.
22. `2026-07-29_dissertation_notes_from_the_frozen_model.md` — the five notes the
    frozen model has earned. No new results; this is writing. Unblocked
    2026-08-01 by the reconciliation.

Parked work — parallel or superseded, not on this chain — is in
[`__archive/`](__archive/).
