---
status: durable
created: 2026-05-28
topic: L2 partition — operator-aggregation concern + candidate mitigations
---

# Operator-aggregation in the L2 corpus — what it means and how to mitigate

> **Provenance banner.** This note records the investigation that produced
> GASP. The canonical spec is now at
> [`../specs/02_gasp_schema.md`](../specs/02_gasp_schema.md) — read this
> for *why* GASP exists and *how* the decision was reached; read the spec
> for *what GASP is*.

## Why this is worth recording

The L2 partition verdict at
[`./2026-05-28_l2_partition_decision.md`](./2026-05-28_l2_partition_decision.md)
and its per-flow defence at
[`./2026-05-28_l2_per_flow_justifications.md`](./2026-05-28_l2_per_flow_justifications.md)
treat the 38 active flows as if each were an independent draw from the
population of *operations* the GAP claims to model. **The corpus is not
operator-uniformly distributed.** Several operators appear under multiple
flow files; if those over-represented operators dominate the per-class
discrimination signal at L4 / in the simulator, the class behaviour the
thesis claims to model is *operator-specific* rather than
*operation-class-specific*.

This is not a verdict-changing concern — the JSD on revised P6 (mean 0.317
across 6 pairs) is well above the null calibration p95 of 0.148 even
*before* considering operator weighting. But it is a *defensibility*
concern for examiners who ask *"how do you know the four classes are
classes-of-operation rather than classes-of-operator?"*. This note lays out
the concern and four candidate mitigations so a future session can pick
the right one if and when the question is asked.

## The shape of operator-aggregation in the active corpus (n = 38)

### Operator clusters across the corpus

| Cluster | Flows (count) | Members | Notes |
|---|--:|---|---|
| Conti (G0102) | 3 | `conti_cisa_alert`, `conti_pwc`, `conti_ransomware` | Three independent analyst views of the same RaaS operator family — all classified `double_extortion`. |
| Turla (G0010) | 2 | `turla_carbon_emulation_plan`, `turla_snake_emulation_plan` | Two CTID-authored *emulation plans* for the same actor; both classified `pure_steal`. Plus the scope=`emulation-plan` distinction (only 2 such flows in the corpus). |
| FIN13 (G1016) | 2 | `fin13_case_1`, `fin13_case_2` | Mexican-bank + Peruvian-bank cases; both classified `pure_steal`. Two different operations of the same actor. |
| CISA AA22-138B | 3 | `cisa_aa22_138b_vmware_workspace_alt`, `_ta1`, `_ta2` | Three threat-actor variants under one CISA advisory — split across `pure_steal` (TA1) and `infrastructure_setup` (Alt, TA2). |
| OceanLotus / APT32 (G0050) | 2 | `cobalt_kitty_campaign`, `oceanlotus` | Two views of the same actor — Cybereason-authored campaign + CTID-authored operations-flow. Both `pure_steal`. |
| Sandworm (G0034) | 2 | `notpetya`, `whispergate` | Same destructive-wiper actor across two campaigns (2017 Ukraine, 2022 Ukraine). Both `pure_impediment`. |
| Lazarus / APT38 (G0032 / G0082) | 2 | `sony_malware`, `swift_heist` | Same DPRK actor cluster (G0032 is parent, G0082 is the financial-cybercrime sub-cluster) across two operations. Different classes (impediment / steal). |

**Aggregate concentration.** The 38 active flows include **8 clusters
covering 16 flows** (42 %) where ≥2 flows share an operator. The
remaining 22 flows are operator-singletons (one operation per actor in
the corpus).

### Per-class operator concentration

| Class | n flows | Largest operator-cluster share | Cluster |
|---|--:|--:|---|
| pure_steal (n=19) | 19 | 2/19 (10.5 %) each for FIN13, Turla, OceanLotus | none dominant |
| pure_impediment (n=8) | 8 | 2/8 (25 %) for Sandworm | small but visible |
| double_extortion (n=6) | 6 | **3/6 (50 %) for Conti** | **load-bearing** |
| infrastructure_setup (n=5) | 5 | 2/5 (40 %) for CISA AA22-138B (`_alt` + `_ta2`) | visible |

**The load-bearing case is `double_extortion`**: half of its six flows
are Conti variants (G0102). If the per-class discrimination signal on
this class is dominated by Conti's specific tradecraft (which is
heavy on Cobalt Strike, lateral movement via PsExec / WMI,
credential harvesting via Mimikatz), what the simulator would see is
*"Conti behaves differently from the other classes"* — not necessarily
*"double-extortion behaves differently from pure-steal / pure-
impediment / infrastructure_setup"*.

`infrastructure_setup`'s 40 % CISA-share is less concerning because
the two CISA variants are *different threat-actor encodings under one
advisory* (TA2 + Alt), not three views of the same operator. Still
worth noting.

## Risks to the verdict

The corpus-level JSD discrimination check already showed P6 separates
above chance. But the JSD is **operator-and-operation-weighted** — every
flow contributes equally to its class's pooled distribution, so an
over-represented operator contributes more to its class's signal than
an operator-singleton does. Three specific risks follow:

1. **Class signature reads as operator signature.** The
   `double_extortion` class's tactic-distribution signature is plausibly
   *the Conti signature* with two non-Conti flows (REvil, Ragnar
   Locker) added. If the simulator surfaces a `double_extortion`-class
   MTD response, it may be a *Conti-class* response, not a generalised
   double-extortion-class one.
2. **Cross-class leakage.** Lazarus appears in *two different classes*
   (`sony_malware` in pure_impediment, `swift_heist` in pure_steal). If
   Lazarus's tradecraft is more similar across operations than across
   classes, this *reduces* the inter-class JSD (because the same actor
   appears on both sides). The corpus's JSD is therefore a *lower
   bound* on the discrimination — counterintuitively, operator-
   aggregation *understates* class separation when the same operator
   straddles classes.
3. **L4 generalisation gap.** The thesis's RQ is *"how do existing MTD
   mechanisms perform against behaviourally-grounded adversarial
   profiles"*. If the profiles are operator-specific in disguise, L4
   conclusions generalise to *those operators* rather than to *those
   operational-objective classes*. The simulator-verification sub-handoff
   needs to address this directly.

## Four candidate mitigations

In order of cost vs payoff. None require corpus-edits per se; the
first three operate on the existing corpus + classification, the fourth
is a longer-term suggestion.

### Mitigation 1 — Operator-deduplicated re-check (cheap, recommended)

Re-run the corpus-level JSD discrimination *after* collapsing
multi-flow operators to one representative each (e.g. pick the
highest-`n_actions` flow per operator). The corpus shrinks from 38 to
~28 flows; if the JSD signal *survives*, the per-class behaviour is not
operator-driven. If the JSD signal *collapses* (mean JSD drops below
the null p95), it is operator-driven and the verdict needs revising.

**Implementation cost:** ~30 minutes of analysis (one Python script,
re-render of the comparison chart).

**Decisiveness:** **high**. This single check tells us whether the
verdict is operator-robust or operator-fragile.

### Mitigation 2 — Operator-weighted JSD (cheap, complementary)

Instead of pooling per-flow technique counts equally into a class
distribution, weight each flow by `1 / n_flows_for_its_operator`. So
the three Conti flows each contribute `1/3` to the `double_extortion`
pooled distribution, REvil + Ragnar Locker each contribute `1` (their
own operator-singletons), and the cluster sums to a class distribution
where each operator has weight 1. The JSD is then computed on
*operator-weighted* distributions, which removes the over-representation
effect without dropping any data.

**Implementation cost:** ~15 minutes (modify the `class_distribution`
function in the existing script).

**Decisiveness:** **medium**. Doesn't *resolve* the concern but
*quantifies* it: the delta between flow-weighted and operator-weighted
JSD is exactly the amount of signal attributable to operator-
aggregation.

### Mitigation 3 — Operator-stratified discrimination at the simulator step

When the simulator-verification sub-handoff runs (class × ≥2 MTD ×
≥3 seeds), add **operator-stratified holdout**: for each class with
operator-clustering (notably `double_extortion`), run the
discrimination check with the dominant operator's flows held out
of the class definition, and again with *only* the dominant operator's
flows. If MTTC / ASR / tactic-time-share converge between the two
holdouts, the class is operator-robust. If they diverge, the class is
operator-specific and the simulator's response is to the operator's
tradecraft, not the operational-objective class.

**Implementation cost:** moderate — adds 6–8 extra simulator runs to
the existing matrix (Conti-only / non-Conti for `double_extortion`,
Sandworm-only / non-Sandworm for `pure_impediment`, etc.). One extra
notebook section.

**Decisiveness:** **highest**. This is the test the thesis defence
would actually need to point to if pressed on the operator-vs-class
question.

### Mitigation 4 — Corpus expansion (long-term)

The honest mitigation: extend the corpus with hand-curated flows
(per the GAP's per-flow seam,
[`../specs/01_gap_schema.md`](../specs/01_gap_schema.md) Decision 4)
that **fill in operator-singletons** for the under-represented classes.
Specifically:

- `double_extortion` would benefit most from more non-Conti
  double-extortion operators (LockBit, BlackCat, Cl0p, Royal,
  BlackByte, etc.) — currently dominated by 3 Conti variants out of 6.
- `infrastructure_setup` is small and operator-narrow (DFIR Report
  loaders + CISA AA22-138B variants). More IAB-style flows would
  thicken it.

Cost is bounded — each new flow is ~1 hour of analyst time to author
the per-flow YAML — and the seam is already in place. The trade-off is
session time vs corpus thickness; the simulator-verification step
should be run first because if it shows operator-robustness already,
corpus expansion isn't necessary.

**Implementation cost:** ~1 hour per new flow, 5–10 new flows per
under-represented class.

**Decisiveness:** **highest, but slowest**. This is the answer if the
above mitigations show operator-fragility *and* the thesis needs to
claim class-level behavioural fidelity (not operator-level).

## Possible aggregation will smoothen this out — yes, partly

The user's intuition that *"if aggregation / generalisation will
smoothen this out"* is correct in spirit. Two paths:

- **Aggregation at the L1 step (already done).** The GAP already
  aggregates per-flow technique edges by observation count; if Conti
  contributes 3 of the 4 observations of an edge, that edge is in
  `observation_count = 4` but the *signal* per Conti-edge is the same
  as per any other operator's edge. The GAP's lossless edge metadata
  preserves Conti's three contributions distinctly (`flow_ids = [conti_cisa_alert,
  conti_pwc, conti_ransomware]` on the affected edges), so the L1
  artefact retains the disaggregation seam — it's the L2 *class
  subgraph* (surface, this verdict's working definition) that loses it.
- **Generalisation at the L2 step (proposed).** If the class subgraph
  switched from *surface* (techniques actually present in class flows)
  to *operator-weighted surface* (each operator weighted equally
  regardless of n flows), the per-class technique sets would be
  *operator-uniform* and the over-representation washes out. **This is
  Mitigation 2 above, applied at the subgraph-construction stage rather
  than at the discrimination-measurement stage.**

The aggregation-smooths intuition holds if and only if the GAP's
generalisation across operators is *real* (i.e. operators of the same
class share enough tradecraft that the class-level pooled distribution
is meaningful). The current evidence — single-observation share at
88 % of GAP edges
([`./2026-05-27_gap_construction.md`](./2026-05-27_gap_construction.md))
— says the GAP itself is *thin in generalisation*, so aggregation can
only do so much. The honest framing: aggregation smooths within-class
operator variance for *recurring* behaviours (the 12 % obs ≥ 2 backbone)
but cannot synthesise generalisation where the corpus has none.

## What to do next (recommendation)

If the simulator-verification sub-handoff has session-budget for one
additional check, **add Mitigation 1 (operator-deduplicated JSD
re-check)** as the first thing. It's 30 minutes of work, returns a
single decisive number, and either confirms the verdict is
operator-robust or surfaces the need for Mitigations 2–4.

If session-budget is tighter than that, **at minimum cite this note
in any thesis defence text that claims P6 separates the four
operational-objective classes** — the citation is "operator-
aggregation is a documented concern; we run the simulator with
[Mitigation 1 / 2 / 3] to address it". That keeps the verdict honest
without locking in a mitigation choice.

## How it connects

- To the verdict: [`./2026-05-28_l2_partition_decision.md`](./2026-05-28_l2_partition_decision.md) §"If revisited"
  adds the operator-aggregation check as one of the conditions under
  which the decision is re-opened.
- To the per-flow defence:
  [`./2026-05-28_l2_per_flow_justifications.md`](./2026-05-28_l2_per_flow_justifications.md)
  §"Critique" §"Operator-aggregation concern" links here.
- To the sub-handoff:
  [`../handoffs/2026-05-28_l2_simulator_verification.md`](../handoffs/2026-05-28_l2_simulator_verification.md)
  should pick up Mitigation 1 (and optionally 2 / 3) as part of its
  discrimination-check scope.
- To the GAP construction note:
  [`./2026-05-27_gap_construction.md`](./2026-05-27_gap_construction.md)
  §"thin generalisation" — the 88 % single-observation finding is the
  L1-level analogue of the L2-level operator-aggregation issue. The
  honest framing: the L1 corpus is thin in generalisation *and* the L2
  partition has operator-clustering; both are real, both are documented,
  both bound what the thesis can claim about class-level behavioural
  fidelity.

## When this would need updating

- After Mitigation 1 runs: record the operator-deduplicated JSD and
  whether the verdict stands.
- If new flows are added per Mitigation 4: update the operator-cluster
  table at the top.
- If the simulator-verification step runs Mitigation 3: this note
  becomes the citation target for the stratified-holdout results.
