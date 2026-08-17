---
status: superseded by tactic_profile_statistics.md (2026-08-17) — the
        drafting-session restatement, kept as the record that was
        independently verified. Marc ruled: size-matched null, tactic-to-tactic
        resolution. NOTE all JSD values below are in NATS (scipy default base),
        not bits as stated; divide by ln 2 to compare with the verified record.
created: 2026-08-17
updated: 2026-08-17
scope: L2 (GASP) — findings restatement only. Tool: tools/gasp_tactic_restatement.py
---

# The objective partition at tactic resolution — restated numbers, and a null the L2 gate never ran

## Why this exists

The dissertation's §4.2.1 (drafted 2026-08-16) presents the L1 graph at
**tactic** granularity. The recorded L2 findings
([`../../../notes/ch4_methods/objective_partition_findings.md`](../../../notes/ch4_methods/objective_partition_findings.md);
[`gasp_schema.md`](gasp_schema.md) §(g)) and the L2 test gate
([`tests/l2_subgraph/test_gasp.py`](../../../../tests/l2_subgraph/test_gasp.py))
are **technique**-level. Marc's ruling at the §4.2.2 scrutiny
(2026-08-17): the L2 numbers need regenerating at tactic-to-tactic resolution
so the unit tells the same story as L0–L1. This record holds the regenerated
numbers, computed by
[`tools/gasp_tactic_restatement.py`](../../../../tools/gasp_tactic_restatement.py)
(seeded, deterministic; conventions mirror the L2 gate — each flow contributes 1
per technique it uses; JSD = `scipy jensenshannon(...)**2`, base 2).

Two resolutions are reported at tactic level, because "tactic-level" is
ambiguous: **tactic share** — (flow, technique) occurrences pooled to the
technique's `primary_tactic`, row-normalised (the quantity the findings note's
"impact share 0 % → 11.3 %" sentence gestures at); and **transition share** —
(flow, inter-tactic edge) occurrences pooled to the tactic pair, which is the
tactic-to-tactic directed-flow structure §4.2.1 describes and the structure L3
quotients into transitions.

## 1. Structure at tactic resolution

| | exfiltration (19) | impact (8) | exfiltration_impact (6) | none_c2 (5) |
|---|--:|--:|--:|--:|
| tactic places (of 15 in the GAP) | 15 | 14 | 14 | 13 |
| inter-tactic transitions (of 122 in the GAP quotient) | 89 | 54 | 45 | 38 |

Twelve tactics and twelve tactic-pairs appear in **all four** classes.
Pairwise Jaccard on **tactic sets is 0.80–0.93** (the classes are, to a first
approximation, the same tactic vocabulary); on **transition sets 0.24–0.35**
(the same order as the technique-level node Jaccard 0.295–0.422 the findings
note reports). The weighted-overlay reading of finding 1 therefore holds *a
fortiori* at tactic resolution: the classes do not differ in which tactics
exist; the difference is in emphasis and in which tactic-pairs are drawn.

**Tactic-share table (% of (flow, technique) occurrences; full corpus, n = 38):**

| tactic | exfiltration | impact | exfiltration_impact | none_c2 |
|---|--:|--:|--:|--:|
| collection | 7.4 | 1.9 | 1.0 | 3.4 |
| command-and-control | 11.6 | 11.4 | 7.1 | 15.3 |
| credential-access | 9.5 | 4.8 | 4.1 | 6.8 |
| defense-impairment | 1.4 | 1.0 | 0.0 | 1.7 |
| discovery | 13.0 | 13.3 | 19.4 | 22.0 |
| execution | 9.8 | 12.4 | 12.2 | 18.6 |
| exfiltration | 3.9 | 0.0 | 3.1 | 0.0 |
| impact | 0.4 | 14.3 | 16.3 | 0.0 |
| initial-access | 9.8 | 6.7 | 8.2 | 3.4 |
| lateral-movement | 5.6 | 5.7 | 2.0 | 5.1 |
| persistence | 8.8 | 7.6 | 6.1 | 5.1 |
| privilege-escalation | 1.8 | 4.8 | 6.1 | 5.1 |
| reconnaissance | 3.5 | 1.9 | 1.0 | 1.7 |
| resource-development | 1.1 | 1.9 | 2.0 | 1.7 |
| stealth | 12.6 | 12.4 | 11.2 | 10.2 |

Read-offs that carry into the L2 unit: **impact** 0.4 % / 14.3 % / 16.3 % /
0.0 % (the findings note's "0 % → 11.3 %" is superseded by these numbers —
different pooling); **exfiltration** present only in the two classes whose
objective includes theft (3.9 %, 3.1 %) and absent from the other two;
**discovery** the largest or second-largest share in every class
(13.0–22.0 %); `none_c2` is the only class with zero exfiltration *and* zero
impact — the absence that defines it (Decision 5) survives the change of
resolution. The deduplicated (n = 29) table is in the tool output; the
read-offs are the same to within a point or two.

## 2. Separation, and the null it is measured against

The L2 gate calibrates its null as JSD between two random **halves** of the
corpus (19:19; 14:15 on the deduplicated corpus) and compares that against the
**mean pairwise JSD over the four classes**. Those are different statistics: a
class of 5 or 6 flows sits far from any other distribution by sampling alone,
so a half-split null under-states chance separation for a 19:8:6:5 partition.
The size-matched alternative — shuffle class *labels* with class sizes
preserved and recompute the same mean-pairwise statistic — is the null
[`divergence.py`](../../../../src/mtdsim/l3_simulation/petri/divergence.py)
already uses at L3. Both are reported.

| resolution | corpus | observed mean pairwise JSD | null p95, half-split (L2 gate) | null p95, size-matched shuffle |
|---|---|--:|--:|--:|
| technique | n = 38 | 0.297 | 0.152 | **0.296** |
| technique | n = 29 dedup | 0.315 | 0.185 | **0.344** |
| tactic share | n = 38 | 0.070 | 0.026 | 0.061 |
| tactic share | n = 29 dedup | 0.083 | 0.033 | 0.072 |
| transition share | n = 38 | 0.351 | 0.238 | **0.401** |
| transition share | n = 29 dedup | 0.375 | 0.272 | **0.440** |

(Technique-level observed values differ in the third decimal from the recorded
0.317 / 0.3149; same statistic, this tool's seeding and pooling. The gate's
own number stands as recorded.)

**Reading.** Against the gate's half-split null every row clears, as recorded.
Against the size-matched null: technique-level separation sits *at* p95 on the
full corpus and *below* it on the deduplicated corpus; tactic-share separation
clears narrowly on both; **transition-share separation does not clear on
either.** The recorded "modest but real, operator-robust" claim is therefore
null-dependent — real under the gate's null, marginal-to-absent under the
size-matched one — and it is weakest at exactly the resolution (tactic-pair
transitions) L3/L4 read.

**Per-pair permutation tests** (size-matched, 1 000 shuffles of the two
classes' pooled flows; *p* = fraction of shuffles with JSD ≥ observed):

| pair | technique | tactic share | transition share |
|---|--:|--:|--:|
| exfiltration vs impact | 0.247 (p .064) | 0.077 (**p .004**) | 0.344 (p .090) |
| exfiltration vs exfiltration_impact | 0.270 (p .091) | 0.097 (**p .004**) | 0.355 (p .227) |
| exfiltration vs none_c2 | 0.283 (p .136) | 0.051 (p .147) | 0.274 (p .586) |
| impact vs exfiltration_impact | 0.326 (**p .030**) | 0.027 (p .599) | 0.365 (p .623) |
| impact vs none_c2 | 0.336 (p .107) | 0.067 (p .106) | 0.309 (p .673) |
| exfiltration_impact vs none_c2 | 0.320 (**p .027**) | 0.099 (**p .013**) | 0.460 (p .090) |

Full corpus shown; the deduplicated table (tool output) keeps the same three
tactic-share pairs below .05 and loses both technique-level ones. The pairs
that separate at tactic share are the pairs distinguished by the **impact
tactic's presence or absence** — which is to say the partition's signal at
tactic resolution is the objective tactic itself, plus a discovery/execution
emphasis in the two small classes; pairs on the same side of that line
(impact vs double extortion; exfiltration vs none_c2) do not separate.

## 3. What this does and does not touch

- **No artefact changes.** Class memberships, the audit CSV, the four
  `SubgraphView`s and the L3 nets are untouched; the gate still passes as
  written.
- **The gate's null is a disposition for Marc.** Options on the record: keep
  the half-split null and disclose it as lenient; add the size-matched null to
  the gate and let the technique-level check fail on the deduplicated corpus
  (a real finding, per the gate's own comment); or move the load-bearing
  discrimination claim off corpus structure entirely and onto the
  execution-level result
  ([`../ogasp/profile_divergence_findings.md`](../ogasp/profile_divergence_findings.md),
  P1 held 40–110× — but note its null is within-profile split-half at fixed
  structure, and its own size-matched label-blind control, arm 3, has not run;
  the same null question recurs there).
- **For the L2 unit.** The numbers the unit can carry at tactic resolution:
  15/14/14/13 places, twelve tactics common to all four, tactic-set Jaccard
  0.80–0.93, transition-set Jaccard 0.24–0.35, the impact / exfiltration /
  discovery read-offs above. What it should not carry unqualified is
  "clears the null" — the honest form is that separation is carried by the
  objective tactic and is null-dependent beyond it. Which sentence that becomes
  is Marc's.

## Related

- [`gasp_schema.md`](gasp_schema.md) §(g) — the gate as specified.
- [`../../../notes/ch4_methods/objective_partition_findings.md`](../../../notes/ch4_methods/objective_partition_findings.md)
  findings 1 and 5 — the technique-level statements this restates; the note's
  "0 % → 11.3 %" and its unqualified "clears the null" are the two sentences
  this record bears on (note not edited here; rubric-gated).
- [`../../../notes/ch4_methods/operator_concentration.md`](../../../notes/ch4_methods/operator_concentration.md)
  — the deduplicated re-check this record re-runs under the second null.
- Same-operator-same-class check (Marc's 2026-08-17 reframe of the operator
  clusters as evidence that an operator's motivation translates to a stable
  objective): of the seven clusters, Conti ×3, FIN13 ×2, Turla ×2, OceanLotus
  ×2 and Sandworm ×2 each sit in one class; the Lazarus umbrella straddles two
  (Sony G0032 → impact; SWIFT G0082 → exfiltration); the CISA AA22-138B trio
  is three threat actors under one advisory, split exfiltration / none_c2 ×2.
  Five of five *single-G-ID* clusters are within-class; the umbrella and the
  advisory are the two that are not.
