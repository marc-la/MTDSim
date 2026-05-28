---
status: draft — canonical GASP construction (v1.0 target). Supersedes the
        v0.4 terminal-node-ancestor proxy and the architecture §(e)
        "motivation specifier {espionage, disruption, financial}" prose.
created: 2026-05-28
scope: L2 (GASP construction) only. L3/L4 are consumers, not in scope here.
---

# 02 — GASP schema (operational-objective-subgraphed APT Profile, class-level)

The data model and construction method for **L2 — GASP**: the operational-
objective-conditioned subgraphs derived from the L1 GAP plus an audit-traced
per-flow class-membership input. This file is the *what it is* (data model
+ invariants + decisions). The *how to build it* will be implemented at
[`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph) (currently a
stub; implementation handoff at
[`../handoffs/2026-05-28_l2_implementation.md`](../handoffs/2026-05-28_l2_implementation.md)).
The class-membership input is committed at
[`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv).

This sits under [`architecture.md`](architecture.md) §(e) (L2 GASP) and
supersedes its terminal-node-ancestor proxy. It does **not** restate the GAP
data model — that lives in [`01_gap_schema.md`](01_gap_schema.md), the
load-bearing input to L2.

---

## (a) Purpose and the central invariant

GASP slices the L1 GAP into a small set of **operational-objective-conditioned
subgraphs**, so downstream stages (L3 attacker traversal, L4 evaluation, and
the eventual Petri-net encoding) read *behaviourally differentiated* attacker
variants rather than the GAP-average. Without the slice, the thesis's research
question — *"how do existing MTD mechanisms perform against behaviourally-
grounded adversarial profiles?"* — collapses to a single-cell comparison.

**Central invariant — every class membership corresponds to an objective the
analyst stated, not an objective inferred from graph structure.** No flow's
class is decided by terminal-node detection, ancestor closure, or any other
structural heuristic over the GAP. An assignment that cannot be traced to a
CTI source — vendor report, ATT&CK Group / Campaign page, or CTID
`example_flows/` blurb — in the audit CSV does not belong in the GASP. This
mirrors the GAP's no-synthesis invariant
([`01_gap_schema.md`](01_gap_schema.md) §(a)) one level up: the GAP refuses
synthesised *edges*; the GASP refuses synthesised *class memberships*.

Three corollaries:
- **Structural-terminal is the dropped P1 candidate, not a fallback.** P1
  (3-class structural-terminal) and the GAP's `is_objective` property are
  descriptive metadata only; they never assign a flow's class. P1 disagrees
  with the audit on 15 of 38 flows (40 %) — see
  [`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md).
- **The class subgraph is computed by *surface*, not ancestor closure.**
  Every class's ancestor cone pulls in 87–97 % of the GAP's 124 techniques
  (the GAP is densely connected through `command-and-control` ↔ `discovery`
  hub structure), so ancestor closure is non-discriminating. Surface =
  techniques actually present in the class's flows.
- **Class membership is sourced from the audit CSV at build time.** The CSV
  is the load-bearing input the L2 builder reads. Re-deriving class
  membership from the per-flow YAMLs in
  [`../../data/gap/flows/`](../../data/gap/flows/) is not how L2 works —
  the per-flow YAMLs do not carry `stated_objective`; the audit CSV does.

---

## (b) The five design decisions (with Marc)

**Decision 1 — slice axis is operational objective, not motivation.**
Motivation (espionage / financial / disruption) is rarely written down in
structured CTI; STIX's `primary_motivation` field is empty across all 187
ATT&CK groups and all 52 ATT&CK campaigns (verified 2026-04-16). Operational
objective — what the operation *did* by the analyst-stated narrative — is
observable directly from CTI text.
**Why:** Slicing on inference (motivation) requires defending the inference
layer; slicing on observation (operational objective) does not. Alshamrani
2019 ([`../extractions/alshamrani2019.md`](../extractions/alshamrani2019.md))
also locates objective-conditioned behavioural divergence at APT phases 3–5,
which is where it matters for an MTD evaluation — phases 1–2 are invariant.
**If revisited:** If a corpus emerges with structured motivation attribution
(STIX `primary_motivation` populated), motivation re-enters as a comparable
axis; the GASP would then carry both.

**Decision 2 — class set is `{pure_steal, pure_impediment, double_extortion,
infrastructure_setup}`, an empirical refinement of Alshamrani's 3-goal NIST
baseline.**
Alshamrani names *steal_data* / *damage* / *position_for_future*. This corpus
contains **zero surveillance flows** (`position_for_future`-as-Alshamrani-
names-it does not appear) and **six explicit double-extortion operations**
(Conti × 3, REvil, Ragnar Locker, Black Basta) that a 3-class scheme cannot
name without forcing multi-membership.
**Why:** STIX's 10-category `attack-motivation-ov` spreads too thin (Marc's
hand-labelled 47-campaign sample collapsed onto 3 categories). The v0.4
30-bucket terminal-technique scheme fragments (most buckets *n* < 3). The
4-class compound-disjoint partition is the lightest scheme that names the
empirical shape of the corpus — *double-extortion* is in active operational
CTI usage (CrowdStrike, Mandiant, CISA) even if not in standards-grounded
taxonomies.
**If revisited:** A future framework with a `monetisation` / `multi-purpose`
class would re-classify two `low`-confidence flows
(`mac_malware_steals_crypto`, `searchawesome_adware`) that the 4-class scheme
retains with explicit confidence downgrades. A corpus expansion that adds
surveillance operations would re-instate Alshamrani's `position_for_future`
distinct from `infrastructure_setup`.

**Decision 3 — class membership is sourced from the audit-traced CSV, not
the GAP's graph structure.**
Each of the 38 flows is classified by reading **(i)** the CTID
`example_flows/` index page's per-flow blurb, **(ii)** the ATT&CK Group /
Campaign page where the flow maps to a G-ID or C-ID, and **(iii)** the most
authoritative vendor URL in the flow's `references[]` (Mandiant, Unit 42,
CrowdStrike, Microsoft, Talos, DFIR Report, CISA — though CISA URLs return
403 to `WebFetch`). The result is the audit CSV's `stated_objective` column
([`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv));
`metadata_confidence` records audit confidence; `source_used` records which
CTI source the classification was read from.
**Why:** The candidate alternative — P1 structural-terminal classification —
agrees with the audit on only 23 of 38 flows (61 %). The 40 % disagreement
is not noise: it is *truncated breach reports* (Equifax, JP Morgan, Marriott,
Uber, SWIFT, Cobalt Kitty, MITRE NERVE, FIN13 Case 1, Ivanti UTA0178, mac,
muddy) where the analyst stopped drawing before the exfil step appeared as a
structural terminal. The structural mechanism mis-classifies the corpus's
most common pattern (truncation) systematically.
**If revisited:** If a future analyst-side encoding standard appends explicit
operational-objective tags to per-flow STIX bundles (Attack Flow v4+?), the
CSV becomes a build cache rather than a committed artefact, but the
audit-traced provenance stays.

**Decision 4 — the class subgraph is the *surface* subgraph — techniques
actually present in the class's flows, no ancestor closure.**
For class *C*, `nodes(C) = ⋃ techniques(flow_i) ∀ flow_i ∈ C` (union of
per-flow technique sets); `edges(C) = {(u,v) ∈ GAP.edges : u ∈ nodes(C) ∧
v ∈ nodes(C)}` (GAP edges where both endpoints land in `nodes(C)`).
**Why:** The architecture §(e) ancestor-closure proxy fails on this GAP:
every class's ancestor cone pulls in 87–97 % of the GAP's 124 techniques.
Distinctiveness is structurally near-zero for every scheme under closure
(every candidate scored ≤ 1/5 on the rubric's distinctiveness axis until
the canonical subgraph was switched to surface). The architecture §(e) prose
itself flags ancestor closure as *"a proxy ... broader than this"* — surface
is the defensible narrower variant the spec calls for.
**If revisited:** If L3 traversal needs *reachability-closed* subgraphs
(e.g. an attacker should be able to traverse from an entry node to its
objective using only class-resident techniques and their GAP dependencies),
the class definition would re-introduce a bounded closure step. The current
posture is that L3 reads the surface subgraph directly.

**Decision 5 — the renamed residual class is `infrastructure_setup`, not
Alshamrani's `position_for_future`.**
Alshamrani's `position_for_future` framing implies *ongoing surveillance* —
APT actors maintaining footholds for future re-engagement. The five flows
in the residual class are **not** that. They are pre-payload / loader /
C2-setup operations whose analyst-stated narrative names them as **not-yet-
objective-realised** (DFIR Report's *"evicted before completing their
mission"* signature is canonical here: Hancitor DLL, BumbleBee Round 2,
Gootloader; plus two CISA AA22-138B variants with C2 / webshell terminals
and no observed payload).
**Why:** `position_for_future` as Alshamrani names it would imply
*intended-surveillance* operations, which the corpus does not contain.
Renaming to `infrastructure_setup` is faithful to what the corpus actually
shows. This is *not* a synthetic analytical category — *"pre-payload"*,
*"initial-access broker positioning"*, and *"evicted before mission
complete"* are operational CTI vocabulary.
**If revisited:** A corpus expansion that surfaces surveillance operations
(persistent APT footholds with no observed exfil/impact, no eviction
narrative — e.g. group-witnessed dormancy) would split `infrastructure_setup`
into `infrastructure_setup` + `surveillance`. The current 5 flows would all
stay in `infrastructure_setup`.

**Investigation provenance.** During the investigation that produced this
spec, the accepted construction was named **P6 (compound-class disjoint)**
in [`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md) —
chosen from a rubric over seven candidates (P1 structural-terminal, P2
terminal-technique 15-class, P3 group-witnessed, P4 hand-labels, P5
metadata-attested 3-class multi-member, **P6** compound-class disjoint, P7
reach-based). Dropped-candidate detail and per-criterion scoring live in the
partition-decision note. *Future spec text should reference "the GASP
construction" — not "P6"; the P6 framing is investigation-time terminology.*

---

## (c) Class-membership input — the audit CSV (committed)

One row per flow at [`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv).
38 rows; `stated_objective` is the load-bearing column.

| Column | Notes |
|---|---|
| `flow_id` | Corpus filename stem; joins to [`../../data/gap/flows/<flow_id>.yaml`](../../data/gap/flows/) and `gap_v0.5.json` `flow_ids` |
| `flow_name` | Human-readable name from the flow's STIX bundle |
| `scope` | `incident` \| `campaign` \| `malware` \| `threat-actor` \| `emulation-plan` — STIX `attack-flow.scope` |
| `n_actions` | Action-node count in the per-flow YAML (descriptive) |
| `terminal_techniques`, `terminal_tactics` | Structural metadata (descriptive — *not* the class mechanism, per Decision 3) |
| `reaches_exfiltration`, `reaches_impact` | Structural reach (descriptive) |
| **`stated_objective`** | **`steal_data` \| `impediment` \| `double_extortion` \| `position_for_future`** — the class assignment; mapping to spec labels below |
| `attribution` | ATT&CK G-ID / C-ID where the flow maps; `unknown` where attribution is undocumented |
| `metadata_confidence` | `high` \| `medium` \| `low` — audit confidence |
| `source_used` | Which CTI source(s) the classification was read from (CTID blurb, ATT&CK Group page, vendor URL) |
| `notes` | Free-text justification — pointer to detailed per-flow defence in [`../notes/2026-05-28_l2_per_flow_justifications.md`](../notes/2026-05-28_l2_per_flow_justifications.md) |

**CSV label ↔ spec label mapping.** The audit CSV's `stated_objective` column
uses Alshamrani's original labels plus `double_extortion`; the spec uses
this file's Decision 2 / Decision 5 renames. The L2 builder applies the
mapping at read time:

| CSV value | Spec class |
|---|---|
| `steal_data` | `pure_steal` |
| `impediment` | `pure_impediment` |
| `double_extortion` | `double_extortion` |
| `position_for_future` | `infrastructure_setup` |

(If revisited: re-issue the CSV with renamed labels. The rename is
mechanical and would touch only the CSV; investigation notes that reference
`steal_data` etc. preserve their provenance value as written.)

**Per-class distribution (the 19:8:6:5 split, post-verification round
2026-05-28):**

| Class | n flows | Conf: high | medium | low |
|---|--:|--:|--:|--:|
| `pure_steal` | 19 | 14 | 2 | 3 |
| `pure_impediment` | 8 | 7 | 0 | 1 |
| `double_extortion` | 6 | 6 | 0 | 0 |
| `infrastructure_setup` | 5 | 3 | 0 | 2 |
| **total** | **38** | **30** | **2** | **6** |

Low-confidence share is **6 / 38 = 15.8 %** — within the investigation's
stated 20 % gate. Per-flow citations and critique are in
[`../notes/2026-05-28_l2_per_flow_justifications.md`](../notes/2026-05-28_l2_per_flow_justifications.md).

---

## (d) Class subgraphs — the canonical artefact (computed, not committed)

Four `SubgraphView` objects, one per class. Computed by the L2 builder as
`(gap_v0.5.json, audit_csv) → SubgraphView × 4`. The artefact is **computed,
not committed** — the L1 GAP is the persisted source; the L2 class subgraphs
are deterministic functions of the GAP and the audit CSV, and re-computing
is cheap.

### `SubgraphView` — the L2 boundary object

| Field | Type | Notes |
|---|---|---|
| `class_name` | str | `pure_steal` \| `pure_impediment` \| `double_extortion` \| `infrastructure_setup` |
| `node_set` | set[str] | technique IDs present in the class's flows (surface, §(b) Decision 4) |
| `edge_set` | set[(str,str)] | GAP edges where both endpoints ∈ `node_set` |
| `provenance` | obj | `flow_ids` (list of flow IDs in this class), `audit_csv_ref` (path + git SHA), `gap_ref` (gap_v0.5.json path + version) |

The L1 GAP's lossless edge metadata (operator / branch / `flow_ids` per
edge, [`01_gap_schema.md`](01_gap_schema.md) §(d)) flows through the L2
surface construction unchanged — the L2 step does not synthesise new edges
or rewrite edge attributes; it *subsets*.

### Computation

```python
def class_subgraph(gap: GAP, audit_csv: AuditCSV, class_name: str) -> SubgraphView:
    flows = [row.flow_id for row in audit_csv if remap(row.stated_objective) == class_name]
    node_set = {n.technique_id for n in gap.nodes if any(fid in n.flow_ids for fid in flows)}
    edge_set = {(e.source_id, e.target_id) for e in gap.edges
                if e.source_id in node_set and e.target_id in node_set}
    return SubgraphView(class_name, node_set, edge_set, provenance={...})
```

### Per-class node / edge counts (surface; computed against `gap_v0.5.json`)

| Class | n flows | nodes (of 124 GAP nodes) | edges (of 478 GAP edges) |
|---|--:|--:|--:|
| `pure_steal` | 19 | 98 | 413 |
| `pure_impediment` | 8 | 62 | 254 |
| `double_extortion` | 6 | 57 | 225 |
| `infrastructure_setup` | 5 | 39 | 148 |

The class node sets are not disjoint — a technique drawn by analysts in flows
across multiple classes appears in each class's `node_set`. *Disjointness is
a property of class **memberships** (one flow → one class; §(b) Decision 2),
not of class **node sets**.* This is why `pure_steal`'s 98 nodes plus the
other classes' 62 + 57 + 39 = 256 exceeds the GAP's 124 — techniques recur
across class subgraphs.

The min class size (39 techniques for `infrastructure_setup`) **exceeds the
Petri-net primer's 10–20-technique tractability bound** — see §(h) open
question 4. The L3 substrate (graph-driven traversal inside MTDSim/DES) is
not bounded by Petri-net reachability-set size; the bound applies only if
Petri-net at L4 is later promoted from parallel-not-primary
([`architecture.md`](architecture.md) §(f)) to primary.

---

## (e) Views

L3/L4 consumers read `SubgraphView` objects directly. None mutate the class
subgraph at view time.

| View | Parameter | Use |
|---|---|---|
| **Class subgraph** | `class_name` | one of four; the `SubgraphView` (§d) |
| **All-class union** | — | `⋃ node_set(class) ∀ class` — sanity-check parity against the L1 GAP (the GAP's 124-node total is recovered modulo any technique never appearing in a classified flow) |
| **Per-flow projection** | `flow_id` | `flow_id`'s contribution to its class's node set — useful for operator-aggregation diagnostics (§g) |
| **Discriminative view** | `(class_a, class_b)` | `node_set(a) Δ node_set(b)` — symmetric difference; the techniques distinguishing two classes (basis for the technique-JSD discrimination check) |

The architecture §(e) **motivation specifier** view — `{espionage,
disruption, financial}` — is retired. The live parameter is the four-class
operational-objective specifier above.

---

## (f) Build pipeline (summary; implementation in [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph))

1. **Read inputs.** Load `gap_v0.5.json` ([`01_gap_schema.md`](01_gap_schema.md)
   §(d)) and the audit CSV
   ([`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv)).
2. **Validate CSV ↔ GAP consistency.** Every `flow_id` in the CSV resolves
   to a flow in `gap_v0.5.json`'s flow set; row count matches
   `source_flow_count` (both 38 at v0.5).
3. **Apply label remap.** CSV `stated_objective` → spec class label per the
   §(c) mapping.
4. **Compute class subgraphs.** Apply §(d) `class_subgraph` for each of the
   four class names; produce four `SubgraphView` objects.
5. **Persist (optional).** The four `SubgraphView`s may be serialised to
   [`../../data/gasp/`](../../data/gasp/) if downstream consumers (L3
   notebooks, viz scripts) benefit from a cached artefact; canonical source
   remains the GAP + CSV, re-derivable on demand.

The contract is `(gap, operational_objective) → SubgraphView`. The L2
builder is **not yet implemented**; the stub at
[`../../src/mtdsim/l2_subgraph/README.md`](../../src/mtdsim/l2_subgraph/README.md)
points to the implementation handoff at
[`../handoffs/2026-05-28_l2_implementation.md`](../handoffs/2026-05-28_l2_implementation.md).

**Prior art (not ported).** A v0.4 implementation — terminal-node-ancestor
proxy plus platform / terminal selectors — exists on the
`feat/attacker-profiling` and `feat/replay-viz` branches under their
role-based `attacker/` subtree. Per the project's zero-trust stance, prior
code is inspiration only; the implementation here is built fresh against
this spec + the partition-decision note, not lifted across.

---

## (g) Validation

- **No-synthesis check.** Every class membership has a row in the audit CSV
  with a non-empty `source_used` value. Structural-only assignments
  (`source_used == in_flow_only` with no CTI source) are flagged for
  re-audit. The CISA-403 cluster (three `cisa_aa22_138b_*` flows) is the
  documented exception — `low` confidence and structural fallback against
  a vendor source that returned 403 to `WebFetch`.
- **Enterprise-scope check.** Every node in every class's `node_set`
  resolves in `gap_v0.5.json`'s nodes (the L1 Enterprise scope, §(a)
  corollary; guaranteed by construction since class nodes are subsetted
  from the GAP).
- **CSV ↔ GAP consistency check.** Every `flow_id` in the CSV has a matching
  flow in `gap_v0.5.json`'s flow set; CSV row count equals
  `source_flow_count` (currently both 38).
- **Disjoint-membership check.** Every flow appears in exactly one class
  (the GASP partition is mono-class by construction; the P5 multi-membership
  scheme is the dropped alternative). *Disjointness applies to flow → class
  mappings; class node sets overlap by design — see §(d).*
- **Discrimination-above-null check.** Mean pairwise Jensen-Shannon
  divergence on per-class technique frequency distributions exceeds the
  null p95 calibrated against random 19:19 partitions of the 38 flows (n =
  50 trials). Observed: **mean technique JSD 0.317 vs null p95 0.148** —
  modest but real signal across all six class pairs (range 0.284–0.351).
- **Discrimination-above-null with operator-deduplicated re-check.** The
  load-bearing caveat. Half of `double_extortion`'s six flows are Conti
  variants (G0102); 25 % of `pure_impediment`'s eight are Sandworm; 40 %
  of `infrastructure_setup`'s five are CISA AA22-138B variants. The corpus
  is not operator-uniformly distributed (16 / 38 flows belong to 8
  multi-flow operator clusters). The discrimination-above-null check must
  be re-run *after* collapsing multi-flow operators to one representative
  each (Mitigation 1 in
  [`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md));
  if the JSD signal survives, the per-class behaviour is class-driven, not
  operator-driven. If it collapses below null p95, the verdict reframes to
  operator-specific rather than class-specific behavioural fidelity.
  *This check is unrun as of spec land.*

The simulator-level discrimination check — does the L4 substrate (MTTC /
ASR / event traces) reproduce the corpus-level JSD signal? — is *out of
scope for L2* and is the load-bearing test for the L3/L4 evaluation phase.
Corpus-level JSD is supportive but not definitive.

---

## (h) Open questions (deliberately unresolved)

1. **ToolShell flow-split.** `toolshell_vulnerability_in_sharepoint`
   conflates two threat-actor clusters (CL-CRI-1040 → MachineKey exfil;
   4L4MD4R → ransomware) under one flow file. The audit classifies it
   `pure_steal` (CL-CRI-1040 is the named, attribution-rich actor) with
   critique. Ideally it should be **split** into two flows — but that is a
   corpus-edit (L1-level), not a class-mechanism question. Flagged for the
   L2 implementation session.
2. **Operator-aggregation mitigation choice.** The
   [operator-aggregation concern note](../notes/2026-05-28_l2_operator_aggregation_concern.md)
   names four mitigations (operator-deduplicated re-check, operator-weighted
   JSD, simulator-stratified holdout, corpus expansion). Mitigation 1 is
   cheap and decisive; Mitigation 3 is the test the thesis defence would
   actually need to point to. Picking which to run when belongs to the
   simulator-driven evaluation phase, not here.
3. **Fifth class (`monetisation` / `multi-purpose`)?** Two flows
   (`mac_malware_steals_crypto`, `searchawesome_adware`) sit awkwardly within
   the 4-class scheme — credential/monetisation operations that don't cleanly
   fit `pure_steal` or `pure_impediment`. A 5-class scheme with an explicit
   `monetisation` class would re-classify both, but the current evidence (2
   of 38 flows, both `low`-confidence) does not justify the extra class.
4. **Petri-net per-class tractability.** All four classes exceed the
   10–20-technique tractability bound for end-to-end Petri-net encoding
   (min class is `infrastructure_setup` at 39 nodes). If Petri-net at L4
   promotes from parallel-not-primary to primary
   ([`architecture.md`](architecture.md) §(f) revisit), per-class encoding
   would need manually-curated *slices* (e.g. the primer's 6-node hand-pick
   within the T1486 cone), not full class subgraphs.
5. **Corpus growth thresholds.** The 19:8:6:5 split is corpus-faithful; a
   hand-curated incident addition (per the GAP per-flow seam,
   [`01_gap_schema.md`](01_gap_schema.md) Decision 4) that materially changes
   the ratio re-opens whether the 4-class cardinality is right.

---

## (i) Relationship to other specs

- [`architecture.md`](architecture.md) §(e) — L2 GASP, this file's parent.
  This spec retires §(e)'s terminal-node-ancestor proxy and motivation-
  specifier prose.
- [`01_gap_schema.md`](01_gap_schema.md) — L1 GAP, this file's input. The
  GAP's lossless edge metadata flows through the L2 surface-subgraph
  construction unchanged.
- [`../notes/2026-05-28_l2_partition_decision.md`](../notes/2026-05-28_l2_partition_decision.md) —
  the investigation that produced this spec (the "P6 verdict", rubric +
  discrimination evidence, *If revisited* clauses). Provenance.
- [`../notes/2026-05-28_l2_partition_reasoning.md`](../notes/2026-05-28_l2_partition_reasoning.md) —
  the framing-stage *why-L2 / why-operational-objective* note. Plain-English
  companion; condenses into §(a).
- [`../notes/2026-05-28_l2_per_flow_justifications.md`](../notes/2026-05-28_l2_per_flow_justifications.md) —
  the per-flow defence of every class assignment in the audit CSV.
- [`../notes/2026-05-28_l2_metadata_audit.csv`](../notes/2026-05-28_l2_metadata_audit.csv) —
  the load-bearing class-membership input (§c).
- [`../notes/2026-05-28_l2_operator_aggregation_concern.md`](../notes/2026-05-28_l2_operator_aggregation_concern.md) —
  the operator-aggregation validation caveat (§g).
- [`project_context.md`](project_context.md) — the L0→L4 pipeline GASP sits in.
- Prior art being superseded: the v0.4 terminal-node-ancestor proxy on
  `feat/attacker-profiling` / `feat/replay-viz` (under the role-based
  `attacker/` subtree).
