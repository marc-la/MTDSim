# ch4_methods — notes feeding the Methodology chapter

## What this chapter does

The methodology chapter (ch4 in the ratified structure: introduction, background,
literature review, **methodology**, results, discussion, future work, conclusion)
does two jobs, in order. First it **defines the technical problem precisely** — not
"MTD evaluation is unrealistic" (an application complaint) but the specific
technical gaps beneath it: the attacker-fidelity gap, the ontology gap between
intelligence-derived structure and the simulator, the unobservable-timing problem.
A precisely-defined technical problem is more than half solved. Second, it
**explains the solution as simply as the material allows**, along the ratified
spine: *how APT attackers are modelled* (criterion, corpus → technique graph →
objective profiles → the executable movement attacker → fidelity extensions),
then *how the model is evaluated* (instrument validation, experimental setup).
The inherited simulator is **not** this chapter's material — it moved to the
background chapter by supervisor ruling (2026-08-11); realisation arguments that
were previously staged for a separate implementation chapter now land here, since
the ratified structure has no implementation chapter. Every declared modelling
value carries its validity badge and sweep. (Whole-document guidance:
[`../_writing_guide.md`](../_writing_guide.md).)

What lands here: the *modelling and experimental-design arguments* — how threat
intelligence becomes an executable attacker, the validity defences each step
carries, how the realisation choices are justified, and what the evaluation must
demonstrate before results are read. This is the thickest chapter dir; it also
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
(the literature-only intent spec as bug/design arbiter). Experimental design:
[`evaluation_burden.md`](evaluation_burden.md) (the two-part burden of proof),
[`evaluation_grading.md`](evaluation_grading.md) (the scoring vocabulary),
[`operating_point_discrimination.md`](operating_point_discrimination.md) (show
the operating point discriminates before reporting the metric).
