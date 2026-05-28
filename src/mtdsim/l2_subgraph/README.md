# `l2_subgraph` — L2 GASP construction (stub)

| level | artefact | architecture § | status | code home |
|---|---|---|---|---|
| L2 | GASP (motivation-subgraphed APT Profile) | [§(e)](../../../docs/specs/architecture.md) | **stub** | here |

**What this stage will hold.** The L1→L2 transform: given the lossless GAP
([`mtdsim.l1_construction`](../l1_construction/)) and an operational-objective
specifier (`{pure_steal, pure_impediment, double_extortion, infrastructure_setup}`,
per [the L2 partition decision](../../../docs/notes/2026-05-28_l2_partition_decision.md)),
produce an operational-objective-conditioned subgraph — the techniques and
edges drawn by the analyst in the corpus flows belonging to that class,
traversable end-to-end.

The class subgraph is the **surface subgraph** (techniques actually present in
the class's flows, no ancestor closure). This supersedes the
terminal-node-ancestor proxy that architecture §(e) carried — see the
partition-decision note for the empirical reason (ancestor closure pulls in
87–97 % of the GAP regardless of class, making subgraphs non-distinct).

**Class membership** is sourced from the audit-traced CSV at
[`../../../docs/notes/2026-05-28_l2_metadata_audit.csv`](../../../docs/notes/2026-05-28_l2_metadata_audit.csv) —
not re-derived from the per-flow YAML structure. The CSV is the load-bearing
input.

**Prior art (not ported).** A v0.4 implementation — the terminal-node-ancestor
proxy plus platform / terminal selectors — exists on the sibling
`feat/attacker-profiling` and `feat/replay-viz` branches under their role-based
`attacker/` subtree. Per the project's zero-trust stance, prior code is
inspiration only; any build here is a fresh implementation justified against
the spec + the partition-decision note, not a lift-and-shift.

**Why still a stub.** The partition decision lands the classification scheme;
the implementation lands in a follow-up session governed by
[`../../../docs/handoffs/2026-05-28_l2_simulator_verification.md`](../../../docs/handoffs/2026-05-28_l2_simulator_verification.md),
which couples the implementation to a simulator-driven discrimination check
that confirms the verdict before code lands here.
