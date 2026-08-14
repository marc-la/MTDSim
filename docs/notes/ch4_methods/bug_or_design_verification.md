---
status: durable
chapter: ch4_methods
created: 2026-08-14
updated: 2026-08-14
---

# Separating a bug from a design choice needs an independent yardstick, because AI-assisted maintenance of inherited code cannot supply one

## Position in the dissertation

The methodology chapter's account of a validity threat specific to this work's
circumstances: the attacker model is built on an inherited simulator whose code the
researcher did not write and cannot fully vet, maintained with AI assistance more
fluent in that code than any available human reviewer. The note explains why a
literature-only specification of the simulator was constructed as a precondition
for changing it, and why that specification is itself a methodological contribution
rather than housekeeping. It belongs where the chapter accounts for the integrity
of the inherited substrate the experiments run on.

## The idea

A study that extends someone else's simulator inherits its faults along with its
capabilities, and must at some point decide, for each surprising behaviour, whether
it is a bug to fix or a design choice to preserve. Getting that decision wrong is
not a cosmetic error. Fix a genuine design choice and the substrate no longer
matches the published lineage the results are compared against; preserve a genuine
bug and the results describe broken software. The decision is therefore a validity
gate, and this project met it under conditions that make the gate unusually hard to
hold: the inherited code was written in the early days of AI-assisted development
and is dense with defects, the researcher is not its author, and the assistant
proposing fixes is, by construction, better at reading the code than at knowing what
the code was *meant* to do.

That last asymmetry is the crux, and naming it plainly is part of the argument. An
assistant asked "is this a bug?" while looking at the code can only answer from the
code — and the code is the very artefact whose correctness is in question. It will
find inconsistencies, propose repairs, and each newer model will find more, because
fluency at spotting anomalies rises with capability while knowledge of original
intent does not come from the source at all. A fix justified by "this line
contradicts that line" is circular when both lines are suspect: the thing that
would break the circle — what the simulator was *supposed* to do — is not in the
code, and cannot be recovered from it.

### The instrument: a specification the code cannot contaminate

The resolution is to build the yardstick from a source the code cannot influence.
This project constructed a specification of the simulator's intended behaviour from
the substrate *literature alone* — the paper that introduced the simulator read as
the primary authority, its successors admitted only where they extended the core —
deliberately excluding all code-derived reasoning. The published numbers were not
treated as ground truth, because a paper's reported results can themselves be wrong;
what was extracted was the *intent*: the behaviours, mechanisms and invariants the
authors specified the simulator to have. An intent specification uncontaminated by
the implementation can then arbitrate, because it and the code are genuinely
independent witnesses. A behaviour is classified against it in one of a few ways:
it conforms to the specified intent; it conforms to a superseded version of the
intent that a later paper revised; or it is documented nowhere in the literature at
all. Only the last is even a candidate bug, and a candidate is not a verdict — the
disposition of a genuine ambiguity remains a judgement the researcher makes and
owns, not one the assistant makes from the code.

This inverts the failure mode. Before the specification existed, a behaviour was
judged a bug because it looked wrong against the code; after it, a behaviour is a
candidate bug only because it is *absent from the independent record of intent* —
and a behaviour that conforms to the literature is protected from a well-meaning
"fix" precisely when it looks anomalous, which is exactly when it is most at risk.
The specification does not make the researcher an expert in the inherited code. It
makes the code answerable to something outside itself.

### Why this is a contribution and not merely diligence

The obvious objection is that reading the source paper carefully is just good
practice, not a method worth reporting. It becomes a method because of what it is
built to withstand: a maintenance process in which the most capable participant is
structurally biased toward code-internal reasoning, and grows more so with each
model generation. Under those conditions, the ordinary discipline of "understand the
code before changing it" fails silently, because understanding drawn from the code
cannot distinguish intended behaviour from a long-standing defect. Pinning intent to
an external, immutable record — and forbidding code evidence from entering it — is
the specific control that keeps the bug-versus-design decision honest when the tool
doing most of the reading cannot supply the intent itself. That control is
transferable to any study that extends inherited research software with AI
assistance, which is an increasingly common circumstance and a rarely examined
validity threat.

## Evidence and repo anchors

- The literature-only intent specification and the audit that applies it:
  [`../../implementation/mtdsim_intent_spec.md`](../../implementation/mtdsim_intent_spec.md),
  [`../../implementation/intent_conformance_audit.md`](../../implementation/intent_conformance_audit.md).
- The standing rule this note argues for:
  [`../../workflows/guardrails.md`](../../workflows/guardrails.md) ("bug is a
  verdict, not a first impression").
- The intent arc, in Marc's own words:
  [`../../implementation/research_record/threads/bug_vs_design.md`](../../implementation/research_record/threads/bug_vs_design.md).
- The primary substrate source the specification is built from: [`brown2023`](../../sources/extractions/brown2023.md); its extending successors [`zhang2023`](../../sources/extractions/zhang2023.md), [`tay2024`](../../sources/extractions/tay2024.md).
- Sibling: [`inherited_attacker_flowchart_vs_machine.md`](inherited_attacker_flowchart_vs_machine.md) (the specification-versus-realisation gap for the inherited attacker specifically).

## Revisit conditions

- If the intent specification is found to disagree with itself across the lineage
  papers on a load-bearing behaviour, the arbitration is no longer clean and the
  note must address how conflicts within the record are resolved.
- If a behaviour classified "documented nowhere" is later found in a source the
  specification missed, the specification's completeness claim weakens and the note
  reframes around the specification as a living, revisable instrument.
- If the simulator is replaced rather than inherited, the entire validity threat
  dissolves and this note becomes background rather than method.
