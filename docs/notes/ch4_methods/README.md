# ch4_methods — notes feeding the APT attacker model chapter

## What this chapter does

The attacker-model chapter (ch4 in the structure as restructured 2026-09-04:
introduction, background, literature review, **APT attacker model**, experimental
setup, results, discussion, future work, conclusion; the dir keeps its `methods`
name) does one job: it **defines the attacker model and explains it as simply as
the material allows**. The chapter preamble names the model (the movement
attacker), states the commitments (built beside the simulator, attacker-only
scope, proof of concept), and then the chapter runs the pipeline as four
sections — L0–L1 intelligence to attack graph, L2 objective-conditioned attack
profiles, L3 the Petri-net formalism, L4 the attacker-agent traversal. The
precise problem statement and the fidelity criterion the model is built toward
are **the literature review's** (ch3 §3.3, the research gap and the attacker
model criterion): the former §4.1 restated them and was cut as a duplicate. The
experimental setup is now its own chapter ([`../ch5_experimental_setup/`](../ch5_experimental_setup/)).
The inherited simulator is **not** this chapter's material — it moved to the
background chapter by supervisor ruling (2026-08-11); realisation arguments that
were previously staged for a separate implementation chapter land here, since
the ratified structure has no implementation chapter. Every declared modelling
value carries its validity badge and sweep. (Whole-document guidance:
[`../_writing_guide.md`](../_writing_guide.md).)

What lands here: the *modelling arguments* — how threat intelligence becomes an
executable attacker, the validity defences each step carries, and how the
realisation choices are justified. This is the thickest chapter dir; it also
hosts [`tactic_profiles/`](tactic_profiles/), the 15 per-tactic evidence profiles
with their own [`_rubric.md`](tactic_profiles/_rubric.md). Rubric-gated
([`../../workflows/notes_rubric.md`](../../workflows/notes_rubric.md)).

Reading order for a cold start:
[`technique_graph_construction.md`](technique_graph_construction.md) →
[`objective_partition_rationale.md`](objective_partition_rationale.md) →
[`objective_partition_findings.md`](objective_partition_findings.md) →
[`structure_to_behaviour_binding.md`](structure_to_behaviour_binding.md) →
[`operational_validation.md`](operational_validation.md). Targeted defences:
[`cti_corpus_as_snapshot.md`](cti_corpus_as_snapshot.md),
[`operator_concentration.md`](operator_concentration.md),
[`uniform_filtering_for_comparison.md`](uniform_filtering_for_comparison.md),
[`exponential_as_tractability_choice.md`](exponential_as_tractability_choice.md)
(pairs with `operational_validation.md`: values vs distribution shape),
[`outcome_overlay_directionality.md`](outcome_overlay_directionality.md) (the
success/failure overlay as declared directionality). Realisation arguments:
[`inherited_attacker_flowchart_vs_machine.md`](inherited_attacker_flowchart_vs_machine.md)
(built beside, not inside),
[`host_simulator_contract.md`](host_simulator_contract.md) (the portability
contract), [`bug_or_design_verification.md`](bug_or_design_verification.md)
(the literature-only intent spec as bug/design arbiter). The experimental-design
notes (burden of proof, grading vocabulary, operating-point discrimination) moved
to [`../ch5_experimental_setup/`](../ch5_experimental_setup/) with the chapter.
