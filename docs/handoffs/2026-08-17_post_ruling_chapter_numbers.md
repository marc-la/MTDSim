---
status: open
created: 2026-08-17
---

# Carry the 19 / 7 / 7 / 5 partition and its consequences into §4.2.2 and the ch4 findings note — every number the chapter cites now has one regenerated source

## State of play

On 2026-08-17 the L2 objective classification was validated end to end and
then ruled on: the structural baseline the chapter cites is pinned (terminal
read = Def A via the L1 contraction — 7 / 11 / 1 / 19; **19 of 38** disagree
with the audit under exact match, **15 of 38** under any-overlap; 13 / 13 / 3
is the *reach* read), and Marc's three per-flow rulings moved the partition
from 19 / 8 / 6 / 5 to **19 / 7 / 7 / 5** with the confidence column at **38 / 38
high** (Alt confirmed on Marc's read of AA22-138B). L2 → L3 were rebuilt on the
new membership, every test pin re-derived, the M6 overlay's share rule
generalised, and the records written — all merged to `dev` (`83a6d0b`,
`3c35870`, `f309c07`). The permanent account is
[`../implementation/pipeline/gasp/structural_baseline.md`](../implementation/pipeline/gasp/structural_baseline.md)
(§(b) what the chapter cites; §(d) the re-audit; §(g) the rulings and
everything they moved) and
[`../implementation/pipeline/gasp/tactic_profile_statistics.md`](../implementation/pipeline/gasp/tactic_profile_statistics.md)
§10 (regenerated headline statistics).

**What is not done is the prose.** The §4.2.2 draft in
[`../thesis/dissertation.tex`](../thesis/dissertation.tex) still carries the
pre-ruling trail (13 / 13 / 3 → 19 / 8 / 6 / 5 → 15 of 38, and the withheld
confidence figure), and the ch4 findings note
[`../notes/ch4_methods/objective_partition_findings.md`](../notes/ch4_methods/objective_partition_findings.md)
carries the pre-ruling numbers in its body under a banner. Both belong to the
drafting session (Marc's voice), not to a validation session — hence this
handoff.

## Recommended approach

1. **§4.2.2 number trail — one reading, cited from one tool.** P1 → the
   terminal read ("8 flows terminate on exfiltration, 12 on impact, one on
   both, 19 on neither"; drop or relabel the 13 / 13 / 3 reach sentence);
   P4 → 19 / 7 / 7 / 5; P5 → **19 of 38** if the sentence keeps its literal
   "different category" form, or **15 of 38** if reworded to "silent or
   contradicts", with the 14 silent + 4 impact-only ransomware + 1 contradiction
   composition available either way (§(b)). Confidence sentence: 38 of 38
   high under the composite approach — the appendix table
   [`../thesis/tables/objective_classification_audit.tex`](../thesis/tables/objective_classification_audit.tex)
   is `\input`-ready (booktabs only; labels `tab:objective-audit-*`) and is
   `Appendix~[Y]`. Regenerate it with
   `PYTHONPATH=src python tools/gasp_structural_baseline.py --tex` if the CSV
   ever moves again.
2. **The class name follows the definition.** The compound class now holds six
   ransomware operations and DarthMiner; "double extortion (which we define as
   containing both impact and exfiltration in the same attack flow)" names six
   of seven by its name and all seven by its definition. One sentence, Marc's,
   settles which the chapter leads with; the tactic label
   (`objective_exfiltration_impact`) already follows the definition. "Half of
   double extortion is one operator's variants" → three of seven.
3. **Findings note body pass** — the numbers under the banner (class sizes,
   per-class shares, the operator caveat, the two-misfits concession, and the
   one weakened result: the exfiltration-vs-impact next-tactic pair no longer
   clears *p* = 0.05 — §10). Rubric-gated; bump `updated`; drop the banner
   once the body is right.
4. **Two L3 sentences wherever the none profile's walks are described:**
   `objective_none_c2` now strands at `privilege-escalation` early on most seeds
   without retrace (its sink moved from `defense-impairment`), and
   `objective_impact` now carries a sink at `collection`. The dated L3
   experiment records (`sink_retrace_design.md`, `demonstration_arms_*`,
   `experiment_02_findings.md`) describe the pre-ruling nets and stay as
   written; any re-run re-derives its arms from `load_routing_net(...).is_sink`
   and re-captures its own goldens (the 15 `*_retrace` goldens were re-captured;
   the aggregate-profile goldens are byte-identical).

Alternatives considered: rewrite the findings note's body from a validation
session — rejected (voice contract; the numbers are ready, the prose is
Marc's).

## Validation gate

- Every number in §4.2.2 P1/P4/P5 and the findings note reproduces from
  `tools/gasp_structural_baseline.py --check` (baseline, concordance, tally)
  or `tools/gasp_tactic_profile_stats.py` (statistics) on the current CSV.
- The appendix fragment is `\input` and compiles.
- The findings note's banner is gone and its `updated` is bumped.

## Hard constraints

- Class membership is Marc's; the CSV's `stated_objective` column is not
  touched by drafting. Voice contract for `thesis/` and `notes/`.
- Branch / commit / no-push per [`../workflows/guardrails.md`](../workflows/guardrails.md).

## Reading list

- [`../implementation/pipeline/gasp/structural_baseline.md`](../implementation/pipeline/gasp/structural_baseline.md) §(b), §(g)
- [`../implementation/pipeline/gasp/tactic_profile_statistics.md`](../implementation/pipeline/gasp/tactic_profile_statistics.md) §10
- [`../implementation/pipeline/gasp/gasp_schema.md`](../implementation/pipeline/gasp/gasp_schema.md) §(c)
- [`2026-08-16_drafting_movement_attacker_section.md`](2026-08-16_drafting_movement_attacker_section.md) — the §4.2 rulings this serves

## Out of scope

Re-deciding any membership; the L3 experiment re-runs; the ogasp records.
