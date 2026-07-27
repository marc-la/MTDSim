# The open chain — dependency order, 2026-07-27

`ls docs/handoffs/` is the inventory of open work; this file carries only the
thing a directory listing cannot — **what depends on what**. All five open
handoffs execute the post-experiment-1 supervisor rulings
(`docs/implementation/pipeline/ogasp/supervisor_decision_register.md` §S1–S6).
Delete a handoff in the commit that ships its work, and prune its line here in
the same commit. *(Shipped from this chain: the S6 criterion — now
`docs/implementation/apt_model_criterion.md`, on the read-first list; the S1
lifecycle consensus — now
`docs/implementation/pipeline/ogasp/lifecycle_consensus.md` +
`data/ogasp/controller/lifecycle_consensus.json`; the S2 action-layer audit —
now `docs/implementation/pipeline/ogasp/action_layer_audit.md`.)*

**Wave 1 is clear.** All three of its handoffs have shipped, so wave 2 is open.

> **Four decisions from the S2 audit are waiting on Marc**, and three of them
> block trusting experiment 2's numbers rather than blocking a handoff. Read
> [`../implementation/pipeline/ogasp/action_layer_audit.md`](../implementation/pipeline/ogasp/action_layer_audit.md)
> § "The four decisions this audit cannot make" before starting the comparative
> run in (8). Two of them (the confusion penalty and the dwell-time interrupt
> gate) land squarely in (5)/(7)'s scope, so pick them up there.

**Wave 2 — open now.**

4. `2026-07-27_controller_v2_partial_mapping.md` (**S4**) — after (3): the verb
   audit tells you what is worth mapping to. Partial mapping, dwell-only tactics,
   versioned mapping registry.
5. `2026-07-27_stochastic_timing_design.md` (**S3**, planning half) — after (4):
   needs the dwell-only tactic set. Design only, no code, deliberately.

**Wave 3 — after wave 2.**

6. `2026-07-27_tactic_weight_sensitivity_study.md` (**S1**, study half) — its
   input (the lifecycle consensus) has shipped; still after (4) so the sweep is
   not run against a mapping about to change.
7. `2026-07-27_stochastic_timing_implementation.md` (**S3**, build half) — after
   (5), which is its specification.

**Wave 4 — last.**

8. `2026-07-27_sink_retrace_experiment2.md` (**S5** + the comparative run) — its
   design half unblocks after (4); its *run* should consume (6) and (7) or it
   will need repeating. Carries the full defence-family sweep the first
   experiment deferred.

Parked work — parallel or superseded, not on this chain — is in
[`__archive/`](__archive/).
