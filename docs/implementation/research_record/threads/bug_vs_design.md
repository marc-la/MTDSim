# Bug or design choice — the verification problem AI-assisted maintenance created, and the instrument that answers it

**Span:** 2026-04-22 (first hang) → 2026-07-28/29 (instrument). **Prompts:** #4,
#40, #46, #47. Landed:
[`../../mtdsim_intent_spec.md`](../../mtdsim_intent_spec.md),
[`../../intent_conformance_audit.md`](../../intent_conformance_audit.md),
[`../../../workflows/guardrails.md`](../../../workflows/guardrails.md) ("bug is a
verdict, not a first impression"); argued for the dissertation in
[`../../../notes/ch4_methods/bug_or_design_verification.md`](../../../notes/ch4_methods/bug_or_design_verification.md).

**The problem, in Marc's words (#46, 2026-07-28).** "MTDSim has many bugs. I
have historically pointed you at the codebase and asked you to fix these bugs,
but maybe I don't necessarily understand the implementation or have the capacity
to know if what you are fixing is actually a bug. **This is my biggest
concern.**" And #47: "each new AI model that is released seems to be picking up
more and more bugs. How can I verify that MTDSim conforms completely to the
intent of Brown …?" — the epistemic situation of a researcher maintaining
inherited research code with an assistant more fluent in the codebase than any
available human reviewer.

**The instrument.** #46 commissions it in one move: build the spec sheet **from
the substrate literature only** — Brown 2023 primary, line by line; Zhang/Tay as
secondary extensions; "no need to verify using Brown's numbers, they may be
wrong, but the documented specs … is what is critical". The intent spec is
deliberately uncontaminated by code-side reasoning so it can arbitrate: conforms
/ conforms-to-superseded-lineage / documented-nowhere, with only
documented-nowhere behaviours *candidate* bugs and only Marc's disposition
making one fixable. #40 shows the rule in operation days earlier (vulnerability
object sharing ruled a bug against brown2023; "I am happy for you to fix
verified bugs … this is not the code changes I mean").

**Prehistory.** #4 (2026-04-22, "there still exists a hang somewhere") is the
first sighting of what Phase 2b later diagnosed as the silent integrity failure
(R1–R3) — three months between symptom and diagnosis, which is itself part of
the argument for spec-anchored verification over spot-fixing.

**Negative space:** the earlier fix-on-sight era (pre-instrument bug fixes,
some of which made the baseline attacker *less* potent — #47 records the
copy-by-reference cluster) is what the instrument exists to prevent recurring;
it was not undone, it was audited (`intent_conformance_audit.md`).
