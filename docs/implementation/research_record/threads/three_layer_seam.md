# Movement / controller / action — the trichotomy, the concession, and the dial

**Span:** 2026-07-16 → 2026-08-03. **Prompts:** #24, #25, #29, #35, #49, #62,
#65, #66. Landed:
[`../../architecture.md`](../../architecture.md),
[`../../pipeline/ogasp/controller.md`](../../pipeline/ogasp/controller.md) and
`controller_mapping_v2.md`, `src/mtdsim/l3_simulation/movement/alignment.py`;
argued for the dissertation in
[`../../../notes/ch4_methods/structure_to_behaviour_binding.md`](../../../notes/ch4_methods/structure_to_behaviour_binding.md)
and [`../../../notes/ch4_methods/host_simulator_contract.md`](../../../notes/ch4_methods/host_simulator_contract.md).

**The trichotomy is Marc's, coined in one prompt.** #24 (2026-07-16) reconceived
the pipeline: GAP→OGASP is "its own unified *movement* layer"; the inherited
six phases are the *action* layer; and between them sits a *controller* — not a
pipeline stage but "the interface", "an arbitrary join between the attack model
of existing MTD work and the movement layer I have created" (#25), keeping the
two "independent components which can be subbed in or out". The same prompt
carries a pre-registered expectation the polished records do not: "I expect the
movement layer to perform the same, or even worse, than the existing MTDSim
FSM, due to strongly connected components" — written a week before experiment 1
confirmed exactly that. The underperformance was *predicted*, not discovered.

**The controller as owned concession.** The phrase that governs the layer:
"the best we can do with the tools at hand" (#24). Every later mechanism placed
there was justified by the same clause — the FSM-objective proxy "in the scope
that this lives in the porting layer … this makes sense", explicitly *not*
generalisable and owned as such (#62). The controller is where fidelity is
traded against the substrate, and the design treats that as a feature: the
trade is confined to one named layer instead of leaking into the model.

**The alignment dial (#65–#66, 2026-08-03).** The concession made tunable: a
float input on [0,1] biasing routing along shortest dwell-only paths toward the
substrate's legal next verbs — "so I can tune the input parameter based on how
much I want the model to succeed", preserving "strategic pluralism, or the
facade of it". Built as `alignment.py`; its null must reproduce the unaligned
finding, making it an ablation instrument for measuring the host's rigidity
(the productive form of the procedural-mismatch diagnosis —
[`../../../notes/ch7_discussion/procedural_mismatch_artefact.md`](../../../notes/ch7_discussion/procedural_mismatch_artefact.md)).

**Abandoned on this thread:** running tactics as genuinely concurrent tokens
(single-token ruling, June); any direct petri→FSM phase mapping as the model
itself (#16 — "has been done before and yields no meaningful results"); Caldera
as the action vocabulary (#16 — "too bulky for direct plugin", only the idea of
tactic operationalisation survived).
