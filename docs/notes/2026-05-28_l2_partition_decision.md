---
status: durable
created: 2026-05-28
topic: L2 (GASP) operational-objective classification — decision
---

# L2 partition decision — compound-class disjoint (P6), conditional on simulator verification

> **Provenance banner.** This note records the investigation that produced
> GASP. The canonical spec is now at
> [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) — read this
> for *why* GASP exists and *how* the decision was reached; read the spec
> for *what GASP is*.

## Why this is worth recording

The L2 classification is the step the thesis's RQ depends on. Without an
operational-objective axis, the two-axis comparison the lit review names
(SDR-family × profiles) collapses to a single cell. This file is the
**verdict on which classification to adopt** at L2, against six candidate
schemes scored on a rubric, an empirical metadata audit, and a corpus-level
discrimination check. It supersedes the open question in
[`../specs/architecture.md`](../specs/architecture.md) §(e) about the L2 mechanism.

The verdict is **recommended-but-conditional**: the rubric + audit + corpus-level
discrimination all converge on **P6 (compound-class disjoint)** as the
working scheme, but the handoff-specified simulator-level discrimination check
(MTTC / ASR / event traces) was *not* run in this session. The simulator step
lands as a sub-handoff
([`../handoffs/2026-05-28_l2_simulator_verification.md`](../handoffs/2026-05-28_l2_simulator_verification.md)).

## The decision

| Class | n flows | Working definition |
|---|--:|---|
| `pure_steal` | 19 | analyst-stated objective is data theft only — no impediment in the flow narrative |
| `pure_impediment` | 8 | analyst-stated objective is disruption / destruction only — no data theft in the flow narrative |
| `double_extortion` | 6 | flow narrative explicitly pursues both data theft *and* impediment, simultaneously |
| `infrastructure_setup` | 5 | flow narrative is pre-payload (loader, C2 setup, eviction before objective) — *not* surveillance, *not* truncated breach |

All **38 active flows** (corpus excluding `example_attack_tree` — CTID
Builder test fixture, dropped pre-verdict — and `openclaw` — HiddenLayer
security-research demonstration, dropped after the
[verification round](./2026-05-28_l2_per_flow_justifications.md#verification-round-2026-05-28))
are mono-class; the partition is genuinely disjoint. Membership is sourced
from the audit-traced CSV at
[`./2026-05-28_l2_metadata_audit.csv`](./2026-05-28_l2_metadata_audit.csv).
Per-flow justifications + critique + citations live at
[`./2026-05-28_l2_per_flow_justifications.md`](./2026-05-28_l2_per_flow_justifications.md).

The reasoning note at
[`./2026-05-28_l2_partition_reasoning.md`](./2026-05-28_l2_partition_reasoning.md)
argued the *partition axis* (operational objective vs motivation); this note
records the *classification scheme* the next session implements at
[`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph/).

## Rubric (six surviving schemes, surface subgraph as canonical GASP)

The architecture §(e) "ancestor closure" proxy fails on this GAP — every
class's cone pulls in 87–97 % of the GAP's techniques, so Distinctiveness is
structurally near-zero for every scheme. Switched to **surface subgraph**
(techniques actually present in the class's flows, no closure), a defensible
deviation since the spec calls ancestor closure "a proxy ... broader than this".

Petri-net tractability is **informational only** per
[`../specs/architecture.md`](../specs/architecture.md) §(f) ("a Petri-net
encoding of GASP would sit *parallel* to MTDSim/DES execution as an
alternative substrate for L4 analytical evaluation — not inside L1/L2");
the criterion was retained in the table but excluded from the ranking,
per Branch-point C of the investigation. All five surviving schemes fail
the per-class tractability bound (min class is 39+ techniques vs the
primer's 10–20 bound).

| Scheme | Canon | Cover | Distinct | Balance | ValPath | MetaAtt | **Total** |
|---|--:|--:|--:|--:|--:|--:|--:|
| P1 — structural-terminal 3-class | 5 | 5 | 1 | 2 | 5 | 3 | **21** |
| P2 — terminal-technique 15-class | 4 | 5 | 4 | 1 | 5 | 1 | **20** |
| P5 — metadata-attested 3-class (multi-member) | 5 | 5 | 2 | 2 | 3 | 5 | **22** |
| **P6 — compound-class disjoint** *(winner)* | 2 | 5 | 2 | 2 | 3 | 5 | **19** |
| P7 — reach-based 3-class structural | 3 | 5 | 1 | 4 | 5 | 3 | **21** |

P3 (group-witnessed terminal) and P4 (reduced STIX 3-cat hand-labels) were
dropped without scoring — P3 because ATT&CK Group attribution is sparse
across this corpus (18/38 flows, all G-codes; no C-codes for P4's hand-label
cross-walk), P4 because the 47-campaign hand-labels are at ATT&CK-Campaign
(C-ID) granularity and 0/39 corpus flows resolve to C-IDs via the audit's
attribution column (≤6/39 even with manual cross-walk attempt). Rationale
recorded.

**Why P6 wins despite P5 outscoring on the rubric.** The handoff is explicit
that the rubric is unweighted — "supervisor is the weighting function" — and
that discrimination is the load-bearing finding ("if buckets don't produce
distinguishably different traces, that partition has failed *regardless of
rubric score*"). P6 wins discrimination (next section); also wins the
bias-agnostic clause (P5 is the handoff author's named lean; P6 contradicts
it — per the clause, a verdict that contradicts the named leans is stronger
evidence the investigation reasoned from data, *if* the discrimination
evidence supports it, which it does by a modest margin).

P6's low Canonicity score (2/5) is the principal mark against it — compound
classes are not in standards-grounded taxonomies (NIST SP 800-39, STIX
`attack-motivation-ov`). The defence: *double-extortion* is in active
operational CTI usage (CrowdStrike, Mandiant, CISA all use the term); it
names a recognised compound objective, not a synthetic analytical category.
The Canonicity score could reasonably be 3 (operational-CTI canonical, not
standards canonical); the total then becomes 20 — still under P5's 22 but
the gap narrows.

## Discrimination evidence (corpus-level proxy)

Pairwise **Jensen-Shannon divergence** on per-class technique frequency
distributions. Higher = more separated. Null calibration is the JSD between
random 19:19 partitions of the same 38 flows (n=50 trials).

| Distribution | null median | null p95 |
|---|--:|--:|
| Tactic-level | 0.018 | 0.031 |
| Technique-level | 0.125 | 0.148 |

| Scheme | mean tactic JSD | mean technique JSD |
|---|--:|--:|
| P1 — 3-class | 0.052 | 0.213 |
| P2 — 15-class | 0.350 † | 0.767 † |
| P5 — 3-class multi | 0.067 | 0.271 |
| **P6 — 4-class compound (revised)** | **0.073** | **0.317** |
| P7 — 3-class reach | 0.065 | 0.192 |

(The revised P6 technique JSD of 0.317 — *up* from the first-draft 0.302 —
reflects the verification round's classification revisions: three flows
moved from impediment / double_extortion to pure_steal, openclaw dropped.
The class separation tightened. All 6 P6 pairs now sit in the 0.284–0.351
range, well above the null p95 of ~0.15.)

† P2's JSD is inflated by singleton classes (per-class n=1 most cases) —
mathematically high, methodologically meaningless per the handoff's stated
"per-class sample sizes may be too small for the discrimination check to
separate signal from noise" caveat.

**Reading:** all 3-class and 4-class schemes separate **above the null p95**
at the technique level (mean JSD 0.19–0.30 vs null p95 0.150) — modest but
real signal. Tactic-level separation is weak in absolute terms (0.05–0.07,
~3–4× the null but bounded by the GAP's near-clique tactic graph per the
construction note). **P6 has the highest mean technique JSD (0.302)**
among interpretable schemes, with its strongest separating pair
`infrastructure_setup` ↔ `pure_steal` at 0.367.

**This is a corpus-level proxy, not the simulator-driven test the handoff
specifies.** Schemes that separate at the technique-frequency level should
plausibly separate at the simulator output (MTTC, ASR, technique-sequence
trace) level, but the *magnitude* of separation under simulator dynamics is
not directly inferrable from corpus-level JSD. The simulator-level test
remains as a sub-handoff, in line with handoff §"Refuse" / §"Sub-investigate"
authority clauses.

## Metadata audit summary

38-row audit at
[`./2026-05-28_l2_metadata_audit.csv`](./2026-05-28_l2_metadata_audit.csv);
populated via the hybrid strategy (CTID `example_flows/` index + ATT&CK
Group/Campaign back-fill + ~14 vendor URL WebFetches + manual fallback for
CISA-blocked endpoints), then reviewed in a verification round (2026-05-28)
that revised three flows and dropped one (openclaw).

- `metadata_confidence == low`: **6 / 38 = 15.8 %** (3 are the
  CISA-403 cluster, 3 are flows where the verification round surfaced
  source-tensions: `mac_malware_steals_crypto`, `searchawesome_adware`,
  `toolshell_vulnerability_in_sharepoint`) — still within the handoff's
  20 % gate.
- Distribution (post-verification):
  - 19 pure_steal (50 %) — *up from first-draft 16 (41 %); mac + muddy + toolshell revised in*
  - 8 pure_impediment (21 %) — *down from 9; mac revised out*
  - 6 double_extortion (16 %) — *down from 8; muddy + toolshell revised out*
  - 5 infrastructure_setup (13 %) — *down from 6; openclaw dropped from corpus*
  - 0 surveillance
  - 0 unknown

The "no surveillance flows in this corpus" finding is itself a result worth
recording — it sharpens the Alshamrani 3-goal taxonomy against incident-
derived CTI: *position for future* as Alshamrani names it does not appear
in the corpus, and the residual class is **uniformly pre-payload /
infrastructure-setup operations**, not surveillance. The handoff's framing
of `position_for_future` as "ongoing-surveillance" is misnamed for this
corpus; renaming the class as `infrastructure_setup` is part of P6's
contribution and is reflected in the class label above.

**Discrepancy with the handoff's recorded split.** The handoff (as updated
in `bec89fc` for the 40 → 39 flow corpus) cites an **11 : 7 : 21**
structural-terminal split with 3 overlap. The fresh recomputation here
(Def A — terminal = action with no downstream action reachable through
operators/conditions) yields **8 : 12 : 20** with 1 overlap. Cross-checked
against two other defensible terminal definitions (B — strict zero
out-degree: 6 : 10 : 23 : 0; D — any-occurrence/reach: 13 / 13 / — / 3),
none reproduce the handoff's table — though D reproduces the [GAP
construction note's](./2026-05-27_gap_construction.md) 13/13/3 *reach*
finding exactly. The recomputation is from `gap_v0.5.json` directly and
the YAMLs in [`../../data/gap/flows/`](../../data/gap/flows/); the
handoff's 11:7:21 appears to inherit from v0.4 prior art under a
different terminal definition the recomputation could not reproduce.
This investigation uses **Def A** as P1's structural mechanic — terminal
= action with no downstream action reachable through any operator /
condition path. The qualitative finding (most flows in position_for_future,
few multi-class under structural) holds; the exact numbers shift. See
the `If revisited` clause below for the conditions under which the
discrepancy reverses the ranking.

**Cross-tab P1 ↔ audit (concordance):** P1 structural-terminal agrees with
the audit's `stated_objective` on **23 / 38 = 61 %** of flows under an
*any-overlap* matching rule. (The first-draft concordance was 14 / 39 =
36 % under the same rule; the verification round both raised it — by
removing the 8-flow double_extortion class's 2-element multi-membership
which had been *inflating* P1's match rate via easy overlap — and lowered
it — by revising mac / muddy / toolshell to `pure_steal` where P1's
structural terminals don't put them. The 61 % is the more honest number.)

The remaining 15 / 38 (40 %) of flows where P1 disagrees with the audit are
the load-bearing pattern: **P1's `position_for_future` bucket includes
flows the audit classifies as `pure_steal`** (truncated breach reports
where the analyst stopped before the exfil step) — Equifax, JP Morgan,
Marriott, Uber, SWIFT, Cobalt Kitty, MITRE NERVE, FIN13 Case 1, Ivanti
UTA0178, mac, muddy. P5 and P6 resolve this by sourcing membership from
analyst-stated narrative, not from the analyst-drawn graph topology.

Three textbook **double-extortion** ransomware operations
(`black_basta_ransomware`, `ragnar_locker`, `revil`) reach both exfil and
impact actions in the flow but P1's structural-terminal mechanism only
identifies `revil` correctly as multi-class. The other two — Black Basta
classified `position_for_future`, Ragnar Locker classified `impediment`-only
— are within-corpus evidence that the structural mechanism under-credits
multi-objective campaigns. P6's `double_extortion` class captures all six
correctly.

## Petri-net tractability check (dropped from ranking, retained as note)

Per Branch-point C of the investigation (a decision made against
[`../specs/architecture.md`](../specs/architecture.md) §(f)'s positioning of
Petri-nets as a *parallel* L4 analytical substrate, not a primary one), the
Petri-net tractability criterion was reduced to *informational, not ranking
input*. The primer's per-class size bound is ~10–20 techniques, low-tens of
transitions. Under surface subgraph (the canonical GASP definition adopted
here), every surviving scheme's smallest class exceeds the bound:

| Scheme | min class size | passes 10–20 bound? |
|---|--:|:--|
| P1 | 78 | no |
| P2 | 1 | yes for singletons, no for residual (107) |
| P5 | 39 | no |
| P6 | 39 (infrastructure_setup) | no |
| P7 | 82 | no |

**No scheme is tractable for end-to-end Petri-net encoding at full
class-GASP scale.** This does not contradict P6 as the L2 winner — the
Petri-net substrate is parallel-not-primary; the primary L3 substrate is
graph-driven traversal inside MTDSim/DES (per architecture §(f)), which is
*not* bounded by Petri-net reachability-set size. If the Petri-net
workstream is pursued later at L4, it will need to operate on
manually-curated *slices* of each class (e.g. the primer's 6-node hand-pick
within the T1486 cone), not on full class subgraphs.

## Residual class breakdown — `infrastructure_setup` (n = 5)

Required per handoff gate item 5 (residual classes defined by what they
*are not* must be unpacked with citations).

| Flow | Vendor citation | What the report says |
|---|---|---|
| `hancitor_dll` | [DFIR Report, *From Zero to Domain Admin*, 2021-11-01](https://thedfirreport.com/2021/11/01/from-zero-to-domain-admin/) | Cobalt Strike positioning; *"threat actors were evicted before completing their mission"* |
| `dfir_bumblebee_round_2` | [DFIR Report, *BumbleBee: Round Two*, 2022-09-26](https://thedfirreport.com/2022/09/26/bumblebee-round-two/) | *"pre-ransomware activity"*; *"evicted from the network before any further impact"* |
| `gootloader` | [DFIR Report, *SEO Poisoning – A Gootloader Story*, 2022-05-09](https://thedfirreport.com/2022/05/09/seo-poisoning-a-gootloader-story/) | Multi-stage loader; *"no further impact before evicted"* |
| `cisa_aa22_138b_vmware_workspace_alt` | [CISA AA22-138B](https://www.cisa.gov/uscert/ncas/alerts/aa22-138b) (URL 403 to WebFetch; classified from CTID blurb + in-flow content) | Alternative exploitation method described; no observed payload; pre-positioning structure |
| `cisa_aa22_138b_vmware_workspace_ta2` | [CISA AA22-138B](https://www.cisa.gov/uscert/ncas/alerts/aa22-138b) (URL 403 to WebFetch; classified from in-flow content) | C2 setup structure only; no observed payload |

All five are *genuine* pre-payload / infrastructure-setup operations per
the analyst-stated narrative. None are truncated breach reports; none are
surveillance / espionage; none are unknown. The class is well-formed
under P6.

**Note on the `openclaw` drop.** The first draft of this decision included
`openclaw` (HiddenLayer prompt-injection PoC) in this class with the note
*"the only non-incident in `infrastructure_setup`"*. The verification round
applied the same criterion to OpenClaw that justified dropping
`example_attack_tree` from the L1 corpus (CTID Builder tutorial fixture):
OpenClaw is a security-research *demonstration* of a hypothetical
capability, not analyst-curated CTI of a real adversary operation. All 18
OpenClaw actions are ATLAS `AML.T*` (zero Enterprise techniques —
contributed zero nodes / edges to `gap_v0.5.json`), so dropping it leaves
the canonical Enterprise GAP unchanged in shape; only `source_flow_count`
moves 39 → 38. See
[the per-flow doc's *Dropped from corpus* section](./2026-05-28_l2_per_flow_justifications.md#dropped-from-corpus-after-verification-n--1)
for the full reasoning.

## If revisited

The decision changes if any of these hold:

- **A simulator-driven discrimination run (the sub-handoff) shows P6's
  classes do *not* produce distinguishable MTTC / ASR distributions.**
  Corpus-level technique-JSD evidence is supportive but not definitive;
  if the simulator-level test fails, the verdict shifts to refusal with
  L1-only contribution (matches handoff §"Stopping rule" clause 2).
- **The operator-aggregation re-check (Mitigation 1 in
  [`./2026-05-28_l2_operator_aggregation_concern.md`](./2026-05-28_l2_operator_aggregation_concern.md))
  shows the per-class JSD signal collapses under operator-deduplication.**
  Half of the `double_extortion` class is Conti variants (G0102); if
  the class's discrimination signal is in fact a *Conti signature*
  rather than a *double-extortion signature*, the verdict is reframed
  to operator-specific rather than class-specific behavioural fidelity.
- **The corpus grows such that `infrastructure_setup` becomes
  disambiguatable into surveillance / pre-payload / RaaS-as-a-service
  sub-classes.** Current corpus is 6 flows of one (loader / pre-payload)
  shape; a richer corpus may justify splitting the class. The
  partition decision is recomputed.
- **A hand-curated incident (per the GAP per-flow seam, Decision 4)
  materially changes the steal_data : impediment : double_extortion :
  infrastructure_setup ratio.** Current 16 : 9 : 8 : 6 is the corpus-
  faithful split; any large deviation re-opens whether the 4-class
  cardinality is right.
- **Petri-net at L4 becomes the primary substrate** (architecture §(f)
  revisit). Currently parallel-not-primary; if pivoted to primary, the
  per-class tractability bound becomes ranking-input and P6 fails it —
  recompute with a coarser cardinality (likely binary
  `pure_steal ∪ double_extortion` vs `pure_impediment ∪ infrastructure_setup`).
- **The discrepancy with the handoff's recorded 11 : 7 : 22 split** turns
  out to reflect a different terminal definition that, when reconciled,
  reverses the P1-vs-P6 discrimination ordering. The recomputation in
  the investigation used three definitions (A walked / B strict / D
  any-occurrence); none reproduce the handoff's table. If a fourth
  definition reproduces it and changes the ranking, revisit.

## What the next session implements

The sub-handoff at
[`../handoffs/2026-05-28_l2_simulator_verification.md`](../handoffs/2026-05-28_l2_simulator_verification.md)
covers two coupled tasks:

1. **Simulator-driven discrimination** — build a fresh `SubgraphAttackerProfile`-
   style wrapper in MTDSim (zero-trust against the v0.4 implementation on
   `feat/replay-viz`), run (class × ≥2 MTD schemes × ≥3 seeds) for P6's
   four classes, report MTTC / ASR / technique-frequency / executed-set
   Jaccard / event-count diagnostic. Discriminates ⇒ this verdict
   stands; does not discriminate ⇒ refusal with L1-only contribution.
2. **L2 implementation** — given a simulator-confirmed P6, implement
   [`../../src/mtdsim/l2_subgraph/`](../../src/mtdsim/l2_subgraph/) as a
   stub-to-real upgrade: the L2 contract is
   `(gap, operational_objective) → SubgraphView`, where
   `operational_objective ∈ {pure_steal, pure_impediment, double_extortion, infrastructure_setup}`.
   The class subgraph is the *surface* subgraph (per this investigation's
   working definition), not the ancestor cone the v0.4 selectors used.

## How it connects

- To the architecture: closes [`../specs/architecture.md`](../specs/architecture.md)
  §(e) (was: terminal-node ancestor proxy with NLP parked; now:
  operational-objective compound-class disjoint, surface-subgraph,
  audit-attested). The §(e) prose should be updated when the next session's
  implementation lands.
- To the GAP: no changes to L1.
  [`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) is unchanged. The
  surface-subgraph definition is an L2-internal choice that doesn't touch
  the canonical GAP.
- To the lit review: closes the §V "operational objective" axis. The
  classification adopted is **compound-class disjoint** sourced from
  metadata audit. The Alshamrani 3-goal taxonomy is the *anchor* (16 +
  8 = 24 steal_data-ish + 9 + 8 = 17 impediment-ish + 6 residual);
  P6 names the compound (double_extortion) and re-labels the residual
  (infrastructure_setup, not surveillance) to match the empirical shape
  of the corpus.
- To the L2 README:
  [`../../src/mtdsim/l2_subgraph/README.md`](../../src/mtdsim/l2_subgraph/README.md)
  language is updated from "motivation specifier `{espionage,
  disruption, financial}`" to "operational-objective specifier
  `{pure_steal, pure_impediment, double_extortion, infrastructure_setup}`",
  pending implementation.
- To the reasoning note:
  [`./2026-05-28_l2_partition_reasoning.md`](./2026-05-28_l2_partition_reasoning.md)
  framed *why* L2 exists and *which axis* it slices on. This note records
  *which classification*; the reasoning note's "Alshamrani three goals as
  the candidate to beat" phrasing should now be read as *the anchor* for
  the compound-class refinement P6 makes, not the final scheme.

## Investigation artefacts

- This file (verdict): [`./2026-05-28_l2_partition_decision.md`](./2026-05-28_l2_partition_decision.md)
- Audit CSV (38 rows, audit-traced `stated_objective` per flow):
  [`./2026-05-28_l2_metadata_audit.csv`](./2026-05-28_l2_metadata_audit.csv)
- Per-flow justifications + critique + verification round outcomes +
  citations:
  [`./2026-05-28_l2_per_flow_justifications.md`](./2026-05-28_l2_per_flow_justifications.md)
- Operator-aggregation concern (3 Conti, 2 Turla, 2 FIN13, 3 CISA
  AA22-138B variants — risks + 4 candidate mitigations):
  [`./2026-05-28_l2_operator_aggregation_concern.md`](./2026-05-28_l2_operator_aggregation_concern.md)
- Reasoning note (framing — *why* L2 exists, *which axis*):
  [`./2026-05-28_l2_partition_reasoning.md`](./2026-05-28_l2_partition_reasoning.md)
- Sub-handoff (simulator verification + L2 implementation):
  [`../handoffs/2026-05-28_l2_simulator_verification.md`](../handoffs/2026-05-28_l2_simulator_verification.md)

No notebook was produced — the analysis ran as in-session Python scripts;
all load-bearing outputs are in this notes file, the audit CSV, and the
per-flow / operator-aggregation companion notes. The reproducibility seam
is the audit CSV (the analyst-stated objectives are the audit-traced
load-bearing input the scheme materialisation reads from). Visualisations
(GASP class subgraphs at technique + tactic levels + a 4-panel comparison
chart) live at `data/gap/_viz/gasp_*` — gitignored, regenerable via
`python data/gap/_viz/gasp_viz.py`.
