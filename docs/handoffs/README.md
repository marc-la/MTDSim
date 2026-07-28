# The open chain — dependency order, 2026-07-28

`ls docs/handoffs/` is the inventory of open work; this file carries only the
thing a directory listing cannot — **what depends on what**. All three open
handoffs execute the post-experiment-1 supervisor rulings
(`docs/implementation/pipeline/ogasp/supervisor_decision_register.md` §S1–S6).
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
formalism, where the clock lives, the exponential rates, the penalty place, the
comparability argument, and the determinism/migration/rollback scheme.)*

**Wave 3 — open now.**

6. `2026-07-27_tactic_weight_sensitivity_study.md` (**S1**, study half) —
   **unblocked**: its input, the lifecycle consensus, has shipped, and the mapping
   it would have been swept against is now settled and versioned. Sweep against a
   named mapping version so the result says which one it holds for.
7. `2026-07-27_stochastic_timing_implementation.md` (**S3**, build half) — its
   specification, the timing design record, has **shipped**
   (`../implementation/pipeline/ogasp/stochastic_timing_design.md`); the build is
   now unblocked, and *smaller than drafted*: the confusion penalty **stays
   substrate-side** (Marc, 2026-07-28 — a portability ruling, no net place), so the
   only behavioural change is the one-line dwell seam.
7b. `2026-07-28_tactic_rate_feasibility_study.md` (**the rate analysis**) — after
   (7), which gives it something to sweep. Sibling to (6): both are declared-value
   sensitivity sweeps and should share a reporting shape and a mapping version.
   Tests whether any conclusion survives the arbitrariness of the tactic timings,
   and whether the timing design's "the mean is what matters" defence holds.

**Wave 4 — last.**

8. `2026-07-27_sink_retrace_experiment2.md` (**S5** + the comparative run) — its
   design half is **unblocked**; its *run* should consume (6) and (7) or it will
   need repeating, and must name `v2_partial` as its mapping version. Carries the
   full defence-family sweep the first experiment deferred.

Parked work — parallel or superseded, not on this chain — is in
[`__archive/`](__archive/).
