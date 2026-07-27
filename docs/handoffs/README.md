# The open chain — dependency order, 2026-07-27

`ls docs/handoffs/` is the inventory of open work; this file carries only the
thing a directory listing cannot — **what depends on what**. All seven open
handoffs execute the post-experiment-1 supervisor rulings
(`docs/implementation/pipeline/ogasp/supervisor_decision_register.md` §S1–S6).
Delete a handoff in the commit that ships its work, and prune its line here in
the same commit. *(Shipped from this chain: the S6 criterion — now
`docs/implementation/apt_model_criterion.md`, on the read-first list.)*

**Wave 1 — independent; start any of these cold, in parallel.**

2. `2026-07-27_lifecycle_consensus_overlay.md` (**S1**, literature half) — overlay
   the published attack-lifecycle models, take their consensus, express it as a
   tactic-to-tactic distance model. No code.
3. `2026-07-27_action_layer_refinement_under_freeze.md` (**S2**) — audit the six
   inherited verbs for genuine defects and fix only those, so the next
   experiment measures the model rather than the plumbing.

**Wave 2 — after wave 1.**

4. `2026-07-27_controller_v2_partial_mapping.md` (**S4**) — after (3): the verb
   audit tells you what is worth mapping to. Partial mapping, dwell-only tactics,
   versioned mapping registry.
5. `2026-07-27_stochastic_timing_design.md` (**S3**, planning half) — after (4):
   needs the dwell-only tactic set. Design only, no code, deliberately.

**Wave 3 — after wave 2.**

6. `2026-07-27_tactic_weight_sensitivity_study.md` (**S1**, study half) — after
   (2) for its input and after (4) so the sweep is not run against a mapping
   about to change.
7. `2026-07-27_stochastic_timing_implementation.md` (**S3**, build half) — after
   (5), which is its specification.

**Wave 4 — last.**

8. `2026-07-27_sink_retrace_experiment2.md` (**S5** + the comparative run) — its
   design half unblocks after (4); its *run* should consume (6) and (7) or it
   will need repeating. Carries the full defence-family sweep the first
   experiment deferred.

Parked work — parallel or superseded, not on this chain — is in
[`__archive/`](__archive/).
