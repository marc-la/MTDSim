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

---

## (b) Faithfulness state of the substrate

The corrected post-2c substrate now matches the published lineage on the
two settings that drove the largest pre-2b divergences:

| Setting | Published value | Code (post-2c) | Spec ID | Fix commit |
|---------|-----------------|----------------|---------|------------|
| **Network Compromise Ratio (NCR) termination threshold** | Zhang 2023 §5: `> 0.8` | `> 0.8` (constructor default; `time_network.py:51`) | MET-15 / C6 | Phase-2b R1 (`0855295`) |
| **MTD execution durations** (mean, std) | Zhang 2023 Table 3 verbatim | All seven entries match Zhang Table 3 (`constants.MTD_DURATION`) | MTD-14 | Phase-2c (`f767349`) |
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

### C7 — exploit-time formula (ATK-03 in the spec)

- **Zhang 2023 §4.4.3, Eq 1–2:** Phase-2 exploit time `T_Aphase2` is
  drawn from an **exponential** distribution `T_Aexploit`, parameterised
  by counts of previously exploited vs. unexploited vulnerabilities and
  the vuln's attack-complexity `ACv`.
- **MTDSim code** (`mtdnetwork/component/services.py:80`): exploit time
  is computed deterministically as `ATTACK_DURATION['EXPLOIT_VULN'] * (1
  - self.complexity)` — a fixed scaling by complexity, no exponential
  draw, no `V_exploited` / `V_unexploited` factor.
- **Status:** **unimplemented** (`divergent` in
  [`mtdsim_spec.md`](mtdsim_spec.md) ATK-03 row).
- **MTTC effect:** the deterministic form has lower variance and a
  different mean envelope than Zhang's exponential. Absolute TTC values
  are shifted; the direction of any specific TTC delta depends on the
  vuln-complexity mix in the scenario.
- **If revisited:** Implementing Zhang's exponential `T_Aexploit` would
  re-enable a *qualified* cross-paper comparison against Zhang's MTTC
  numbers (still bounded by ATK-04 and substrate-default differences).
  Trigger: a finding that the deterministic-vs-exponential variance gap
  collapses an L4 discriminator that would otherwise separate
  configurations.

### ATK-04 — re-exploit time halving (two mechanisms; one active, one not)

Two distinct re-exploit-discount mechanisms apply here. The previous
phrasing of this section conflated them; Unit C (provenance pass)
characterised both with a pinned spy test and disambiguated them.

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
| **Cross-paper numeric** — comparing an MTDSim MTTC value to a Zhang Table value or a Tay reported number | **INVALID** | C7 (deterministic vs exponential exploit time), ATK-04a (active per-instance re-exploit discount, not Zhang's mechanism), and ATK-04b (Zhang per-type learning, unimplemented) jointly shift the absolute level of every TTC reading by an amount that depends on the scenario's vuln-complexity and reuse pattern. |
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
model is [`01_gap_schema.md`](01_gap_schema.md); the build is at
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
[`../notes/2026-05-27_gap_construction.md`](../notes/2026-05-27_gap_construction.md)).
Two consequences bound any GAP-driven evaluation:

| GAP-driven reading | Valid? | Why |
|---|---|---|
| **MTD-efficacy as "how much MTD perturbs *typical observed attack workflow*"** | **Valid (with this framing stated)** | If L3 samples GAP edges by weight, it samples what is frequently *documented* (biased toward successful, well-reported campaigns), not what is *optimal* against a given MTD configuration. The number measures disruption of commonly-reported workflow — say so when reporting it. |
| **MTD-efficacy as "how much MTD defeats an *optimal/worst-case* adversary"** | **INVALID** | The corpus contains observed, not optimal, behaviour; weights carry no adversary-optimality signal. |
| **Seeding L3 transition probabilities directly from edge weights** | **INVALID as-is** | Weights are unnormalised counts. Any stochastic traversal needs an *explicit, documented* normalisation + closed-world assumption the corpus does not itself justify. Flag before anyone treats the GAP as a Markov chain. |

This sits alongside the substrate-side comparability boundary in §(d): there, the
caution is cross-paper *magnitude* comparison; here, it is reading *adversary
optimality* or *transition probability* into observed-workflow recurrence.

## Where to look next

- [`mtdsim_spec.md`](mtdsim_spec.md) — row-level dispositions,
  including the `fixed` / `deferred` markers added in 2c.
- [`baseline/CHANGELOG.md`](../../baseline/CHANGELOG.md) — every intentional
  golden movement attributed to its driving fix.
- [`baseline/golden/`](../../baseline/golden/) — the behavioural oracle.
- [`tests/test_crash_fix_regressions.py`](../../tests/test_crash_fix_regressions.py)
  — R1, R3, and C8 regression assertions.
