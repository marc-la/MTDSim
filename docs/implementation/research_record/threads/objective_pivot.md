# From APT-group profiling to operational objective — the pivot that defined L2

**Span:** April → 2026-06-23 (pivot recorded) → July (audit).
**Prompts:** #0 (first signal), #11, #13. Landed:
[`../../pipeline/gasp/gasp_schema.md`](../../pipeline/gasp/gasp_schema.md),
[`../../../notes/ch4_methods/objective_partition_rationale.md`](../../../notes/ch4_methods/objective_partition_rationale.md).

The April GAP carried **APT-group and campaign filters with "motivation"
chips** — the working theory was profiling attackers by named group. The first
recorded doubt is #0 (2026-04-19): "lingering motivation attached to apt groups —
it is unclear why that is persisting", an instruction to strip motivation from
the group view. By the 23-Jun update (#13) the pivot is explicit and reasoned:
**STIX/ATT&CK/Attack Flow does not maintain motivation for APT groups**, so
grouping by (inferred) operational objective of each Attack Flow replaced
grouping by actor. The same update drops the **process-mining / ontology-regex
ingestion** route ("Attack-Flow-only … at this moment") — a second abandoned
path no shipped record names.

**The verification worry, in Marc's own words.** The four-class split was
"Claude-derived (I am not too confident in it), verification of such a split is
still needed" (#11, #13). That worry drove the later re-grounding: class =
objective **stated by the analyst in the source report, audit-traced (not
inferred)** (#15, 10-Jul update), the `metadata_audit.csv` trail, and the JSD
discrimination check. The distrust-then-audit arc is the record's best example
of the AI-output-verification discipline that later hardened into the
bug-vs-design instrument (see
[`bug_vs_design.md`](bug_vs_design.md)).

**Also considered, not pursued:** GenAI-synthesised Attack Flows to fatten the
38-flow corpus (raised in #11/#13, carried as an open question to Dr Hong,
never executed — the sparse corpus was accepted on the 25-Jun ruling that it is
the only quantitative evidence available). Corpus expansion remains named
future work in the L1/L2 records.
