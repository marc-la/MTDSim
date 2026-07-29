---
status: durable
created: 2026-05-27
updated: 2026-07-29
---

# Metrics — semantics, faithfulness, and comparability

**Status:** authoritative as of the Phase-2c re-baseline (commit
`4d523c9`, branch `feat/metric-faithfulness`). Supersedes any conflicting
phrasing in `baseline/BASELINE.md` or the spec's running-text. The
behavioural oracle is `baseline/golden/`; the substrate is the post-2c
codebase.

This document defines what "MTTC" means *here*, states the substrate's
current faithfulness against the published lineage, names the two
remaining divergences, draws the comparability boundary, and records the
fate of the once-planned `internal`/`lineage` preset split.

---

## (a) Internal MTTC — definition

"**Internal MTTC**" is the mean duration over the **three Ho-defined
attack-action events** (`SCAN_PORT`, `EXPLOIT_VULN`, `BRUTE_FORCE`) for
the rows present in the `attack_record` slice up to a given compromise
checkpoint. The implementation is in
[`mtdnetwork/statistic/evaluation.py`](../../mtdnetwork/statistic/evaluation.py)
`evaluation_result_by_compromise_checkpoint`:

```python
attack_duration_series = sub_record[
    sub_record['name'].isin(['SCAN_PORT', 'EXPLOIT_VULN', 'BRUTE_FORCE'])
]['duration']
time_to_compromise = (
    attack_duration_series.sum() / len(attack_duration_series)
    if len(attack_duration_series) > 0 else 0
)
```

It is reported per compromise checkpoint in
`baseline/golden/<scenario>/evaluation.json` under the field
`time_to_compromise`. The headline number is the value at the last
checkpoint reached (= 0.25 of the host fleet, on the 50-node default; see
the scenario summary tables in [`baseline/CHANGELOG.md`](../../baseline/CHANGELOG.md)).

"Internal" is the operative word. The metric is computed on **this
codebase's substrate** with **this codebase's three-phase action timing
model** — not against Zhang 2023's published `T_Aexploit` formula or
Tay 2024's RL-trained agent. The §c divergences (C7; ATK-04a active +
ATK-04b unimplemented) shift the absolute magnitude of every TTC value,
so the number's meaning is load-bearing only within this substrate.

### The metric belongs to the substrate, and the movement arm does not own it (S3-R, 2026-07-28)

Internal MTTC is a quantity **MTDSim computes about itself**, from the
action durations it observes. That placement is now a ruling rather than
an accident of where the code sits, and it has a consequence worth
stating plainly.

Since S3-R the movement (graph-driven) attacker **supplies its own action
durations**: the tactic the token occupies prices the action, and the
substrate's native `ATTACK_DURATION` / `exploit_time` are not consumed on
that arm. The `attack_record` rows a driven run writes therefore carry
tactic times, not substrate verb costs — so the same verb costs different
amounts on the two arms, and internal MTTC computed over a movement-arm
run is **not** measuring what it measures on the native arm.

**This is not a defect to be argued away, and no attempt is made to
reconcile the two.** The movement layer is designed to be liftable onto a
different simulator, so a simulator-specific metric must not be written
into it; MTDSim keeps its own metric and computes it from whatever
durations it is given. The consequences, stated so nobody re-derives them
later:

- Cross-arm comparison of internal MTTC is **invalid**, on top of the
  cross-paper invalidity §(d) already establishes.
- Movement-arm internal-MTTC figures published before 2026-07-28 are
  superseded; they were computed under the retired hybrid, where the arm
  consumed both a behavioural dwell and the substrate's verb cost.
- Comparability with prior published work is **explicitly not a design
  goal** (Marc, 2026-07-28). Where a faithful comparison is wanted it is
  obtained by running prior work on the final simulator, not by holding
  this model's metrics still — the published numbers carry their own
  defects, so pinning to them buys nothing.

---

## (b) Faithfulness state of the substrate

The corrected post-2c substrate now matches the published lineage on the
two settings that drove the largest pre-2b divergences:

| Setting | Published value | Code (post-2c) | Spec ID | Fix commit |
|---------|-----------------|----------------|---------|------------|
| **Network Compromise Ratio (NCR) termination threshold** | Zhang 2023 §5: `> 0.8` | `> 0.8` (constructor default; `time_network.py:51`) | MET-15 / C6 | Phase-2b R1 (`0855295`) |
| **MTD execution durations** (mean, std) | Zhang 2023 Table 3 verbatim | The **five** techniques Zhang's Table 3 documents (CTS, IPShuffle, OSDiversity, DAP, ServiceDiversity) match verbatim; the Host-Topology/Port/User-Shuffle entries in `constants.MTD_DURATION` are documented in no lineage paper (scope corrected 2026-07-29 by the intent audit — the earlier "all seven" over-claimed) | MTD-14 | Phase-2c (`f767349`) |
| **HCR formula** at checkpoints | Ho 2024 §3.3.2 (#4): `C_t / T_host` | `compromised_num / host_num` (`evaluation.py:126`); bounded in `[0, 1]` and regression-tested | MET-04 / C8 | Phase-2c (`8d4b8c3`) |

The Phase-2b crash-fix bundle (`0855295`, `333ебc4`, `aed80c1`, `a458f9a`)
restored the substrate to a state where it runs cleanly to 15 ks with the
correct termination behaviour, deterministic UUIDs, and no orphaned
SimPy resource slots. Phase 2c rides on top: the metric and timing
fixes here are only meaningful because the underlying simulation is no
longer silently mis-executing.

Goldens captured on this substrate are in
[`baseline/golden/`](../../baseline/golden/). Pre-correction goldens
(Phase-0, captured against the buggy substrate) remain at
[`baseline/golden_phase0_buggy/`](../../baseline/golden_phase0_buggy/) for
provenance.

---

## (c) Remaining divergences — both shift MTTC magnitude

Two named divergences (C7, ATK-04) shift the absolute timing of the
attack-action events that feed into MTTC. C7 is unimplemented relative
to Zhang's published formula. ATK-04 is split into two distinct
mechanisms: one (Brown-era per-instance re-exploit discount) is active
and kept deliberately; the other (Zhang per-type attacker learning) is
unimplemented.

### C7 — exploit-time formula (ATK-03 in the spec) — **substantially overturned 2026-07-29**

> **This section previously said the code implements nothing like Zhang's
> formula. That was wrong, and it was wrong because Eqs 1–2 were omitted
> images in the source conversion — the claim rested on the surrounding
> prose.** Marc supplied the equation images on 2026-07-29; the closed form
> is now in [`mtdsim_intent_spec.md`](mtdsim_intent_spec.md) IS-TIM-06. What
> follows is the corrected disposition. The practical consequence is that
> **C7 is much smaller than recorded**, which widens §(d)'s comparability
> boundary rather than narrowing it.

**Zhang 2023 §4.4.3, Eq 1–2** (recovered):

```
V = V_unexploited + V_exploited                                          (1)
T_Aphase2 = [ Σ_{vi∈V_unexploited} (1 − AC_vi)
            + Σ_{vj∈V_exploited}  (1 − AC_vj)/2 ] · T_Aexploit           (2)
```

**What the code does** (`services.py` `exploit_time`, consumed per
vulnerability in `attack_operation.py` `_do_exploit_vuln`): each attempted
vulnerability costs `exponential_variates((1 − complexity) ·
ATTACK_DURATION['EXPLOIT_VULN'], 0.5)`, and the phase's duration is the sum
over the attempted list.

**Term for term, this *is* Eq 2's unexploited half.** `(1 − AC_v)` is the
code's `(1 - self.complexity)`; `T_Aexploit` is `ATTACK_DURATION['EXPLOIT_VULN']`
(= 15); Eq 2's `Σ` is the per-vulnerability loop; and §4.5's "exponential
time value" is the `exponential_variates` wrapper. The three properties this
document previously called missing — exponential form, ACv-dependence, and
the exploited/unexploited split — are all present.

**What actually diverges is narrower, and precisely locatable.** Two items:

1. **Eq 2's `V_exploited` half is never charged into phase-2 duration.**
   The `/2` branch (`if self.exploited: return exp_time / 2`) exists, but
   candidate selection (`Service.get_vulns`) filters exploited
   vulnerabilities out *before* the timing loop, so the branch is
   unreachable from the duration path. Measured on the no-MTD golden
   (seed 1234) by an entry-state spy tagged with its caller:

   | call site | entry `exploited` | calls |
   |---|---|---|
   | `roa()` | False | 56 486 |
   | `roa()` | **True** | **2 905** |
   | `_do_exploit_vuln()` | False | 1 183 |
   | `_do_exploit_vuln()` | **True** | **0** |

   So the discount fires 2 905 times per run — **all of them inside RoA
   computation, none in the timing path**. Zhang's Eq 2 would have the
   adversary re-pay half-cost for vulnerabilities it already owns on the
   service; this substrate pays nothing for them and instead lets the
   discount perturb *which* vulnerability is selected first.
2. **Where the exponential is drawn.** Eq 2 multiplies one `T_Aexploit` by
   the whole bracket; the code draws independently per vulnerability. Same
   expectation, different variance (n draws of σ = 0.5 rather than one).

**Status:** **substantially implemented**; two located divergences, the
first behavioural and the second distributional. Neither is fixed — see the
D-16 disposition in
[`intent_conformance_audit.md`](intent_conformance_audit.md) §n, which is
open for Marc because charging time for vulnerabilities the adversary is
*not* attempting is a modelling choice, not an obvious repair.

**MTTC effect:** smaller than this document previously asserted. The
unexploited half — which is the whole of the duration in practice — follows
Zhang. The omitted `V_exploited` half means phase-2 durations are
**systematically shorter than Eq 2** wherever the adversary revisits a
service it has partly exploited.

### ATK-04 — re-exploit time halving (two mechanisms; one active, one not)

Two distinct re-exploit-discount mechanisms apply here. The previous
phrasing of this section conflated them; Unit C (provenance pass)
characterised both with a pinned spy test and disambiguated them.

> **Revised 2026-07-29 by the recovered Eq 2.** The a/b split below stands as
> a description of the two *mechanisms*, but its attribution was wrong:
> ATK-04a was characterised as a Brown-era artefact "not a Zhang mechanism".
> Eq 2 shows the halving of already-exploited vulnerabilities **is** Zhang's
> published rule — the `/2` on the `V_exploited` sum — so the Brown-era
> commit implemented (or anticipated) the same idea rather than a rogue one.
> The genuinely load-bearing correction is measurement, not attribution:
> **the discount does not reach the exploit-duration path at all** (0 of
> 1 183 timing calls on the no-MTD golden; all 2 905 fires are inside
> `roa()`), so its effect is on *vulnerability ordering*, not on MTTC
> magnitude. Statements below that ATK-04a "shifts magnitudes" are
> superseded by that measurement; see the C7 section above.

**ATK-04a — Brown-era per-*instance* discount: ACTIVE (kept).**

- **Code** (`mtdnetwork/component/services.py:90-91`,
  `if self.exploited: return exp_time / 2`): when an exploit is attempted
  against a `Vulnerability` instance that is *already exploited*, the
  exploit time is halved. The discount keys on the in-memory
  `Vulnerability` object's `exploited` flag, so it is **per-instance**,
  not per-vuln-type or per-CVE.
- **Provenance:** Brown-era. Introduced by Alex Brown in commit
  `a16db997` (2021-09-04), pre-Zhang. Not a Zhang artefact.
- **Status:** **active and material.** Pinned by
  [`tests/test_atk04_reexploit_discount.py`](../../tests/test_atk04_reexploit_discount.py)
  with an external spy across all 9 goldens. Fire rate ranges from 7.3 %
  of `exploit_time` calls (`no-mtd`) to 41.6 % (`primary-random-15k`);
  the multi-MTD scenarios sit in the 18–32 % band. The spy is
  byte-identity-checked against the golden artefacts; the discount
  applies on the live engine path that feeds `exploit_time` into
  `_execute_exploit_vuln` and into `roa()`/`get_vulns()` filtering.
- **Disposition:** **kept deliberately** (Marc, Unit C). The pinned counts
  above make any future drift visible.
- **If revisited:** Cutting ATK-04a is a behavioural change requiring a
  golden re-baseline — a separate, deliberate decision, not Unit C's. The
  trigger for that decision is a finding that ATK-04a measurably distorts
  within-substrate comparisons in the L4 evaluation (e.g. a re-exploit-heavy
  scenario where the discount swings MTTC by more than the inter-config
  delta being measured).

**ATK-04b — Zhang per-*type* attacker learning: UNIMPLEMENTED.**

- **Zhang 2023 §4.4.3:** "For previously exploited types of
  vulnerabilities, the time to exploit is halved" — an
  attacker-learning rule that keys on **vuln type / CVE**, applying
  the discount whenever the attacker re-encounters a *type* of vuln
  it has previously exploited (even on a fresh `Vulnerability` instance
  on a different host).
- **MTDSim code** (`mtdnetwork/component/services.py:93-98`): a
  commented-out line referencing `exploit_attempt + 1` is the only
  remaining trace; no active implementation. The cross-instance /
  per-type rule is **not** in active code.
- **Status:** **unimplemented / missing** (`missing` in
  [`mtdsim_spec.md`](mtdsim_spec.md) ATK-04 row).

**Divergence from a strict "no attacker learning" assumption.** Earlier
phrasing in this document said "with no learning, every exploit costs
the full base time." That is **incorrect** under ATK-04a: this
substrate *does* halve the cost of re-exploiting the same
`Vulnerability` instance, and that halving fires in 7–42 % of the
exploit-time calls in the goldens. Within-substrate comparison stays
valid (every compared config carries the same ATK-04a bias, identical
under SIM-05 determinism), but the substrate is **not** a faithful
implementation of the "no learning" null. Comparability against Zhang
and Tay numbers remains invalid: ATK-04a shifts magnitudes without
being the same mechanism Zhang published (her halving is per-type,
the active code is per-instance), and ATK-04b is unimplemented.

Neither C7 nor ATK-04b is in 2c's scope to fix. ATK-04a is
substrate-current behaviour, kept and pinned.

---

## (d) Comparability boundary

The combined effect of C7 and ATK-04 is that **absolute MTTC magnitude
on this substrate is not on the same axis as Zhang 2023 or Tay 2024
published numbers**. Two ways to think about what's valid:

| Comparison kind | Valid? | Why |
|-----------------|--------|-----|
| **Within-substrate, across configurations** — e.g. random-multi vs alternative-multi; varying MTD trigger interval; varying network geometry; varying motivation profile (OGASP vs procedural attacker) | **Valid** | Both runs share the same C7/ATK-04 substrate-side bias; the *delta* between them is informative. |
| **Within-substrate, OGASP-driven attacker vs the inherited 6-phase procedural attacker** | **Valid** | Same substrate, same exploit-time model; differences in MTTC trace to the attacker policy, not the substrate. |
| **Cross-paper numeric** — comparing an MTDSim MTTC value to a Zhang Table value or a Tay reported number | **INVALID, but for a smaller reason than before (revised 2026-07-29)** | The original grounds were C7-as-wholesale-divergence plus ATK-04a; the recovered Eq 2 dissolves most of both (see §c). What remains: Eq 2's `V_exploited` half is not charged into duration, so phase-2 times run systematically short wherever a service is revisited; the exponential is drawn per-vulnerability rather than once per phase; and ATK-04b's cross-host scope is still unimplemented. Those still shift absolute level by a scenario-dependent amount — but the gap is now *located and bounded* rather than structural, and D-16 would close the first of the three. |
| **Cross-paper qualitative** — "scheme X yields lower MTTC than scheme Y, consistent with Zhang's qualitative finding" | Conditionally valid | The *direction* of effect is comparable when the relevant mechanism (MTD interruption, re-scan penalty, NCR threshold) is shared; the *magnitude* is not. State the qualification when reporting. |

In §5 of the thesis: **MTTC is reported with this substrate as the
explicit frame of reference**, and any reference to Zhang/Tay numbers is
framed qualitatively or as a published-lineage *target* not yet matched.

**If revisited:** the boundary becomes symmetric only if both C7 (above)
*and* ATK-04b are implemented to match Zhang's published mechanisms;
implementing either alone leaves the asymmetry in place. ATK-04a (the
active per-instance discount) would also need to be either cut or
matched against a Zhang-side equivalent to allow magnitude comparison.

---

## (e) The internal/lineage preset — evaluated and dropped

A two-preset machinery (`internal` and `lineage`) was considered for the
2c work. The intent was to keep a behavioural mode that re-creates
Zhang/Tay-faithful values where cheap (so cross-paper numeric comparison
could be partially recovered) alongside the default `internal` mode.

The disposition for 2c, after the Phase-2b C6 (NCR) repair, was to
**drop the preset split**. After C6 collapsed to 0.8 (= Zhang NCR), the
two presets would differ only by:

- one constant — MTD-14 (the +10 drift on CTS / IPShuffle), which 2c
  has now fixed unconditionally; and
- two unmatched-to-Zhang behaviours — C7 (deterministic exploit-time
  formula) and ATK-04b (per-type attacker learning unimplemented) —
  which a `lineage` preset could not faithfully cover without
  implementing them, and implementing them is explicitly out of scope.
  (ATK-04a, the active Brown-era per-instance discount, is substrate-
  current behaviour and the preset split would have nothing to switch
  on for it either way.)

So there is no longer a meaningful difference to switch between. The
substrate is **single-canonical**: one `MTD_DURATION` table, one HCR
formula, one NCR threshold, one exploit-time model. No
`baseline/golden_lineage/` directory has ever been created; none will be.
This document is the only thing that distinguishes substrate behaviour
from published behaviour, and it does so in prose rather than via a
preset flag.

---

## (f) GAP edge weights — recurrence, not efficacy; and the workflow comparability boundary

Sections (a)–(e) concern the **simulation substrate** (L3/L4) and its MTTC. This
section concerns the **L1 GAP** — a different stage, upstream of the substrate —
and is recorded here because it is the same *genre* of statement: what a number
means, and what comparison it does and does not license. It is forward-looking:
L3/L4 do not yet consume the GAP, but the boundary must be fixed before they do,
so no one reads more into a GAP edge weight than the corpus supports. The GAP data
model is [`01_gap_schema.md`](pipeline/gap/gap_schema.md); the build is at
[`../../src/mtdsim/l1_construction/`](../../src/mtdsim/l1_construction).

### Edge weight (`observation_count`) — what it is

`observation_count` is **the number of distinct incidents in which an analyst
drew that specific technique→technique dependency** in an Attack Flow. It is:

- a **frequency-of-observation / recurrence** signal — "how commonly this
  dependency was *drawn* across reported incidents";
- grounded in the analyst's **sequencing + dependency** judgement (Attack Flow's
  "to do B the adversary first needed A"), so it carries a causal read of an
  *observed* incident.

It is emphatically **not**:

- **efficacy / success probability** — Attack Flow records what happened in
  incidents notable enough to report; failed attempts and abandoned branches are
  not in the corpus, so weight cannot speak to whether a step "works";
- a **transition probability** — weights are unnormalised counts, not a stochastic
  matrix; a node's out-edges sum to nothing, and the graph is not a Markov chain;
- **causal-effect strength** — it is observed co-dependency, not a measured
  intervention.

One-line gloss: **weight = how often analysts drew this dependency across reported
incidents — a popularity/recurrence measure of observed workflow, biased toward
successful and well-documented campaigns, not a measure of how likely or how
effective the step is.**

### The workflow-not-efficacy comparability boundary (L3/L4)

The GAP is built from incident-derived CTI, which is a **survivorship-/
observability-biased** sample (notable, well-documented, largely-successful
campaigns; early kill-chain phases under-observed — see
[`../notes/2026-05-27_gap_construction.md`](../notes/ch3_design/technique_graph_construction.md)).
Two consequences bound any GAP-driven evaluation:

| GAP-driven reading | Valid? | Why |
|---|---|---|
| **MTD-efficacy as "how much MTD perturbs *typical observed attack workflow*"** | **Valid (with this framing stated)** | If L3 samples GAP edges by weight, it samples what is frequently *documented* (biased toward successful, well-reported campaigns), not what is *optimal* against a given MTD configuration. The number measures disruption of commonly-reported workflow — say so when reporting it. |
| **MTD-efficacy as "how much MTD defeats an *optimal/worst-case* adversary"** | **INVALID** | The corpus contains observed, not optimal, behaviour; weights carry no adversary-optimality signal. |
| **Seeding L3 transition probabilities directly from edge weights** | **INVALID as-is** | Weights are unnormalised counts. Any stochastic traversal needs an *explicit, documented* normalisation + closed-world assumption the corpus does not itself justify. Flag before anyone treats the GAP as a Markov chain. **The sanctioned normalisation now exists — see the D3 disposition below**; raw-count seeding stays invalid. |

### Disposition — the D3 tactic-level flow-proportion regime (supervisor-authorised, July 2026)

The escape hatch the row above names — "an *explicit, documented* normalisation
+ closed-world assumption" — was authorised by supervisor decision **D3**
(working session with Dr Jin Hong, early July 2026; register in
[`../notes/2026-07-03_supervisor_meeting_l3_decisions.md`](pipeline/ogasp/supervisor_decision_register.md)).
The regime, in full:

- **Aggregation level: tactic, not technique.** Technique→technique GAP edges
  aggregate up to **tactic-pair transitions** (the transitions of the L3a
  tactic-place nets). Aggregation up from techniques is what makes the weights
  groundable at this corpus size (~38 flows); the sparsity is accepted as "the
  only quantitative evidence available to populate the Petri nets".
- **Weight = out-edge-normalised flow proportion.** A tactic-pair transition's
  weight is the **proportion of attack flows leaving the source tactic** along
  it. It is *not* a raw `observation_count` magnitude — the technique-level
  count stays recorded and un-normalised, with the meaning given at the top of
  this section unchanged.
- **The closed-world assumption, stated.** The corpus's observed out-edges at
  each tactic are treated as the **complete choice set** at that tactic. This
  is an assumption the corpus does not itself justify; it is adopted
  explicitly, not implied.
- **The survivorship framing carries over.** Row 1 of the table governs every
  reading: a weighted traversal samples *typical observed workflow* (biased
  toward successful, well-documented campaigns) — never adversary optimality,
  never step efficacy.
- **The uniform policy is the structural floor.** A uniform-out-edge traversal
  is retained alongside the weighted one as the sensitivity baseline — the
  net's shape with no recurrence signal at all.

One-liner for downstream claims: each class net is read as a **behavioural
envelope for an operational objective**, not an actor's policy; every
weighted-traversal claim is phrased envelope-relative ("under the `pure_steal`
envelope…") — see [`architecture.md`](architecture.md) §(j).

This sits alongside the substrate-side comparability boundary in §(d): there, the
caution is cross-paper *magnitude* comparison; here, it is reading *adversary
optimality* or *transition probability* into observed-workflow recurrence.

This boundary is a **defender-vantage** property, not just a corpus quirk. The GAP
encodes attacker behaviour *as it is observable through CTI*, so a GAP-driven
evaluation measures MTD against the adversary a defender can actually know —
pre-intrusion reconnaissance, which incident-derived CTI is structurally blind to,
is outside it by construction. That blindness is faithful to the defender's
epistemic position rather than a defect, and where it ends is itself a threat-model
input; the reasoning, and why a literature-inferred prefix (Decision 6) extends the
model *within* CTI's limits rather than escaping them, is in
[`../notes/2026-05-27_gap_construction.md`](../notes/ch3_design/technique_graph_construction.md).

## Where to look next

- [`mtdsim_spec.md`](mtdsim_spec.md) — row-level dispositions,
  including the `fixed` / `deferred` markers added in 2c.
- [`baseline/CHANGELOG.md`](../../baseline/CHANGELOG.md) — every intentional
  golden movement attributed to its driving fix.
- [`baseline/golden/`](../../baseline/golden/) — the behavioural oracle.
- [`tests/test_crash_fix_regressions.py`](../../tests/test_crash_fix_regressions.py)
  — R1, R3, and C8 regression assertions.
