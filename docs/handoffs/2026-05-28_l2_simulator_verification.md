---
status: open
created: 2026-05-28
---

# Verify the L2 (GASP) partition verdict against a simulator-driven discrimination check + implement L2

This handoff picks up where the L2 partition investigation
([`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md))
stopped. That investigation produced a **conditional verdict** —
**P6 (compound-class disjoint)** as the working L2 classification — on the
strength of a rubric, an empirical metadata audit, and a *corpus-level*
discrimination check (JSD on per-class technique distributions). The
load-bearing test it did **not** run is the *simulator-level* discrimination
check the original handoff §"Recommended approach" step 5 specified —
(class × ≥2 MTD schemes × ≥3 seeds) inside MTDSim, with MTTC / ASR /
event-trace separation as the criterion. This sub-handoff covers two
coupled tasks: that simulator-level test, and the L2 implementation that
follows if the test confirms P6.

## State of play

**Settled (don't re-derive):**

- L2 axis is operational objective, not motivation
  ([`../notes/2026-05-28_l2_partition_reasoning.md`](../notes/2026-05-28_l2_partition_reasoning.md)).
- 39 active flows in scope (`example_attack_tree` excluded as a CTID test
  fixture).
- Metadata audit at
  [`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv)
  with 7.7 % low-confidence (well under the 20 % handoff gate).
- Candidate set P1–P7 evaluated; P3, P4 dropped with stated reason; P5, P6,
  P7, P1, P2 scored on a 6-criterion rubric (Petri-net dropped as ranking
  input per arch §(f)). P5 wins rubric (22), P6 wins corpus-level
  discrimination (mean technique JSD 0.302 vs null p95 0.150).
- Recommendation: **P6 compound-class disjoint** with classes
  `{pure_steal (16), pure_impediment (9), double_extortion (8),
  infrastructure_setup (6)}` — sourced from the audit CSV's
  `stated_objective` column.
- Working class-GASP definition: **surface subgraph** (techniques actually
  present in the class's flows, no ancestor closure) — a defensible
  deviation from arch §(e)'s "ancestor closure" proxy, since under that
  proxy every class pulls in 87–97 % of the GAP's techniques.

**Unsettled (this sub-handoff resolves):**

- Whether the corpus-level technique-JSD separation (mean 0.302 for P6,
  modestly above the null p95 0.150) survives translation to
  simulator-level (MTTC / ASR / event-trace) separation. The
  bias-agnostic clause from the parent handoff applies: P6 contradicts
  the original author's lean toward P5 — if the simulator-level test
  *confirms* P6 separates, that's evidence-from-data the verdict
  carries; if it *fails*, the verdict reverts to refusal with L1-only
  contribution (parent handoff's stopping-rule clause 2).
- The L2 implementation under
  [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph/) — the
  stub package needs to become a real one with the contract
  `(gap, operational_objective) → SubgraphView`.

## Recommended approach

A single working session covering both tasks, in order.

### Task 1 — Simulator-driven discrimination check

The v0.4 prior art on `feat/replay-viz` includes a
`SubgraphAttackerProfile` wrapper at
`src/mtdsim/attacker/subgraph_profile.py` (read via `git show
origin/feat/replay-viz:src/mtdsim/attacker/subgraph_profile.py`).
Per the project's zero-trust stance, **do not port it** — build a fresh
equivalent. Its API surface (documented in the parent handoff's
orientation notes — *see* the parent handoff at deletion time, or
re-read the source via `git show` since the handoff is gone):

- Wrap-not-subclass: `SubgraphAttackerProfile` duck-types as an
  `AttackerProfile` via `__getattr__` delegation, exposes
  `subgraph_nodes` / `subgraph_edges` / `objective_tid` /
  `selector_tag`, and provides a
  `sample_technique(phase, executed, rng=None, gate_on_predecessors=False)`
  hook that constrains the attacker's per-step technique choice to the
  class's subgraph.
- Construction: a class method
  `from_subgraph_view(view, gap, base_profile, selector_tag="...")`
  binds a `SubgraphView` (the L2 boundary object — `node_set`,
  `edge_set`, `provenance`) to the base profile.
- Duck-type detector: `is_subgraph_profile(profile) -> bool`.

**Run matrix:**

- Classes: P6's four — `pure_steal`, `pure_impediment`,
  `double_extortion`, `infrastructure_setup`. Class membership and
  surface technique sets are derived from the audit CSV at
  [`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv).
- MTD schemes: at least two — recommend `no_mtd` (baseline) and `random`
  (a representative SDR scheme). Adding a third (e.g. Tay's RL) is
  optional and only worth the cost if `no_mtd` / `random` already
  separate the classes — if they don't, more MTD doesn't help.
- Seeds: at least three — `[42, 123, 456]` matches v0.4 convention and
  is sufficient for the discrimination signal-to-noise the corpus can
  support.
- Network: substrate defaults (`50/5/4/8` per
  [`../specs/mtdsim_spec.md`](../specs/mtdsim_spec.md) NET-04 / NET-05).
  Do not vary the network — the L4 question this answers is "do
  classes produce different attacker traces *on the same network*."

**Discrimination measures (per the parent handoff's Branch-point E
decision, replacing v0.4's Jaccard-only check):**

1. **KL divergence on per-class per-run tactic-time-share** — primary
   separator. Compute per-run tactic-time distribution (fraction of
   total run time spent in each tactic), then KL-divergence
   (symmetrised via JSD) pairwise between class means.
2. **Executed-set Jaccard** — secondary. The v0.4 measurement, retained
   for direct comparison; expect Jaccard 0.6–0.8 across class pairs (the
   v0.4 demo's level) and treat that as the *baseline-uninformative*
   region, not a separating signal.
3. **Event-count diagnostic** — third channel. Are per-(scheme, seed)
   row counts and event counts genuinely different across classes, or
   only the labels? In the v0.4 demo, matched-(scheme, seed) row counts
   were *identical* across T1486 / T1567 profiles — the discrimination
   was labels-only. The check is: if your class-paired runs at matched
   (seed, MTD) have row count differences within ±5 %, the
   discrimination is labels-only and you need a richer attacker
   profile (e.g. per-class attack-duration multipliers) to actually
   change the trajectory.
4. **Internal MTTC + ASR** — per
   [`../specs/metrics_semantics.md`](../specs/metrics_semantics.md), the
   primary L4 discriminators. Report per (class, MTD) cell with seed-
   standard-error.

**Verdict criteria:**

- *Discriminates:* mean pairwise tactic-time KL > 0.10 across class
  pairs, with **at least two class pairs** showing KL > 0.15.
  Event-count diagnostic passes (row counts differ meaningfully across
  classes within matched (seed, MTD)). MTTC / ASR show
  cross-class deltas larger than within-class seed-noise.
- *Does not discriminate:* KL ≈ null calibration (random class
  shuffle), or event counts are matched within ±5 %, or MTTC / ASR are
  within seed-noise across classes. Verdict reverts to L1-only
  contribution per parent handoff's stopping-rule clause 2 — i.e.
  *"L2 collapses to the un-partitioned GAP — the contribution lives at
  L1; revisit if a richer corpus changes the discrimination signal."*

### Task 2 — L2 implementation (only if Task 1 confirms P6)

[`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph/) is
currently a stub (README + `__init__`). Promote to real:

- `schema.py` — `SubgraphView` dataclass (`node_set: frozenset[str]`,
  `edge_set: frozenset[tuple[str, str]]`, `provenance: dict` carrying
  selector name + parameters + class label). This is the L2 boundary
  object; L3 reads it.
- `classification.py` — class-membership table from the audit CSV.
  Keep the four classes
  `{pure_steal, pure_impediment, double_extortion, infrastructure_setup}`
  and the 39 flow-membership mapping the audit produced. Do **not**
  re-derive from per-flow YAML; the audit is the source of truth and
  is itself audit-traced via the CSV's `source_used` + `notes`
  columns.
- `selector.py` — `OperationalObjectiveSelector(operational_objective:
  str)` → `SubgraphView`. Constructs the *surface subgraph* for the
  class (union of per-flow technique sets, with GAP edges where both
  endpoints are in the union). Surface, not ancestor cone, per the
  investigation's working definition.
- Test: `tests/l2_subgraph/test_subgraph.py` — assertions on class
  technique counts (P6 surface): pure_steal=94, pure_impediment=63,
  double_extortion=65, infrastructure_setup=39. Counts to be confirmed
  on the next session's run of the materialiser (data may shift
  slightly if the audit table is updated).

**Update [`../specs/architecture.md`](../specs/architecture.md) §(e)**
to reflect the new contract — replace "motivation specifier
`{espionage, disruption, financial}`" with "operational-objective
specifier `{pure_steal, pure_impediment, double_extortion,
infrastructure_setup}`", terminal-node-ancestor proxy is
**superseded** by surface-subgraph from the audit (record the move).

**Update
[`../../src/mtdsim/l2_subgraph/README.md`](../../src/mtdsim/l2_subgraph/README.md)**
language from "motivation" to "operational objective" if the
parent investigation didn't already do it in its commit (verify
on session start).

### Alternatives considered (don't take them — recorded so the next session disagrees from a shortlist)

- *Re-run the rubric with different weights.* The verdict's bias-
  agnostic check already showed the rubric is unweighted by
  convention; supervisor weighting is the supervisor's call, not
  the next session's. If the simulator-level test fails, the
  verdict moves to refusal, not to a different rubric weighting.
- *Use ancestor-cone subgraph (the v0.4 / arch §(e) proxy) instead
  of surface.* Distinctiveness is near-zero under that proxy
  (mean Jaccard > 0.9 for every scheme). The L3 attacker traversing
  ancestor cones would not see class differences. Surface subgraph
  is the working definition for a reason.
- *Implement L2 before running Task 1.* No — if Task 1 fails the
  L2 implementation is wasted work. Run Task 1 first; if it passes,
  proceed to Task 2 in the same session.

## Validation gate

This sub-handoff is **done** when:

1. The simulator-driven discrimination check has run across (P6's 4
   classes × ≥2 MTD schemes × ≥3 seeds), with results reported per the
   four discrimination measures above.
2. A verdict-extension note is written at
   `docs/notes/YYYY-MM-DD_l2_simulator_verdict.md` recording whether
   P6 discriminates at simulator level — *confirms* / *refutes* /
   *inconclusive* — with the data behind the call.
3. If *confirms*: [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph/)
   is implemented (schema, classification, selector, test) and
   [`../specs/architecture.md`](../specs/architecture.md) §(e) is
   updated.
4. If *refutes* or *inconclusive*: the verdict at
   [`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)
   is amended with a refutation note and a follow-up sub-handoff is
   created for whatever next step the refutation implies (richer
   corpus, different attacker model, etc.).
5. This handoff (`2026-05-28_l2_simulator_verification.md`) is
   **deleted** in the same commit that ships Task 1 + (conditionally)
   Task 2, per [`../specs/session_workflow.md`](../specs/session_workflow.md)
   handoff lifecycle.

## Hard constraints

- **Branch hygiene.** Same as parent — work on a dedicated branch
  (`feat/l2-implementation` or similar); never on `main`; never push
  without ask. Per [`../specs/guardrails.md`](../specs/guardrails.md).
- **Zero-trust against prior code.** The v0.4
  `SubgraphAttackerProfile` and selector modules on `feat/replay-viz`
  are *inspiration only*. Build fresh.
- **Determinism.** Seeds at the top of the script; re-running
  reproduces the same results bit-for-bit. Inherits the post-2c
  golden's deterministic substrate.
- **Source CSV is authoritative.** The audit table at
  [`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv)
  is the load-bearing membership input. If the next session re-runs
  the metadata audit and the numbers shift, that's fine — but the
  shift should be recorded against the CSV's diff, not silently
  re-derived.
- **GAP is unchanged.** L1 (`gap_v0.5.json`) is the pinned artefact;
  do not modify it. If the simulator surfaces a GAP-level issue,
  record it as a separate L1-revisit handoff.

## Reading list

In order, before starting:

1. **[`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md)** —
   the verdict this sub-handoff verifies. The §"Discrimination evidence"
   and §"If revisited" sections name what this session is testing and
   what would falsify it.
2. **[`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv)** —
   the audit-traced class memberships. Inspect the
   `metadata_confidence` column and the `notes` column for any flows
   where the classification feels off; flag and address before running
   the simulator (the simulator can't compensate for misclassified
   training input).
3. **[`../notes/2026-05-28_l2_partition_reasoning.md`](../notes/2026-05-28_l2_partition_reasoning.md)** —
   the framing (*why* L2 exists, *which axis*).
4. **[`../specs/architecture.md`](../specs/architecture.md) §(e) +
   §(f)** — the L2 contract this implementation lands; the §(f)
   "Petri-net parallel-not-primary" framing the investigation cited for
   its Branch-point C decision.
5. **`git show origin/feat/replay-viz:src/mtdsim/attacker/subgraph_profile.py`** —
   the v0.4 wrapper's API surface (read, don't port).

## Out of scope

- A full SNAKES Petri-net implementation — informational-only per the
  parent investigation's Branch-point C, and out of scope for this
  sub-handoff explicitly.
- Re-running the metadata audit unless the next session has reason to
  believe the existing one has errors. The audit took ~13 WebFetch
  calls and 7.7 % low-confidence; the cost-benefit of re-running is
  poor.
- Re-evaluating the dropped P3 / P4 candidates. Their drops are
  recorded with reasons; re-derivation is wasted work.
- Network substrate variation. One network, generic, per architecture
  §(a) and the parent investigation's hard constraints.
