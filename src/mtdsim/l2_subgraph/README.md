# `l2_subgraph` — L2 GASP construction (stub)

| level | artefact | architecture § | status | code home |
|---|---|---|---|---|
| L2 | GASP (motivation-subgraphed APT Profile) | [§(e)](../../../docs/specs/architecture.md) | **stub** | here |

**What this stage will hold.** The L1→L2 transform: given the lossless GAP
([`mtdsim.l1_construction`](../l1_construction/)) and a motivation specifier
(`{espionage, disruption, financial}`, per architecture §(e)), produce a
motivation-conditioned subgraph — the techniques and edges relevant to that
motivation, traversable end-to-end.

**Prior art (not ported).** A v0.4 implementation — the terminal-node-ancestor
proxy plus platform / terminal selectors — exists on the sibling
`feat/attacker-profiling` branch under its role-based `attacker/` subtree. Per
the project's zero-trust stance, prior code is inspiration only; any build here
is a fresh implementation justified against the spec, not a lift-and-shift.

**Why a stub now.** The pipeline tree is laid out to its architecture levels up
front, so L1's artefact has a clear consumer slot. L2 construction is a later
work item; this package currently holds only this row and its `__init__`.
