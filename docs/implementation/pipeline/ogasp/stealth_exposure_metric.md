---
status: durable
created: 2026-08-06
topic: "The axis-5 exposure reader — built, validated, and it inverts the prediction it was written to test: the inherited attacker reads QUIETER than every profile, because the tempo contrast the design rested on was an artefact of per-vulnerability row counting. The measure discriminates; the low-and-slow story does not survive it"
---

# Stealth exposure — the measure works, and it says the profiled attacker is the loud one

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

> **SUPERSEDED IN ITS SCORING CONVENTION, 2026-08-06 — read this record as
> history.** Marc ruled the same day that **the increment fires on a tactic's
> invocation of a verb**, so a dwell-only visit contributes elapsed time and no
> increment (R1), and that arm-versus-arm readings are scored at **verb-level
> tiers on both sides** (R2). Every figure below was computed under the opposite
> convention — every visit scores, tactic-level tiers throughout — which is what
> §5 already flagged as carrying 56–62 % of four profiles' exposure on tactics the
> simulator never executes.
>
> **What that does to this record.** E1–E5 stand as scored: they were answered
> against the instrument as it then was, and the pre-registration and the verdicts
> are the audit trail. But the headline sentence — *the profiled attacker is the
> loud one* — **must not be quoted forward**: it is an artefact of the superseded
> convention, and under R1 three of five profiles fall below the baseline on the
> same statistic.
>
> **What survives unchanged**, because none of it depends on the convention: the
> 3.75× per-vulnerability inflation of the baseline's attack record (§3), the
> qualification it forces on the parent record's §1.1 tempo claim, and the
> measured inertness of the CVSS term (§1.1).
>
> The successor is [`stealth_dutycycle.md`](stealth_dutycycle.md), which rebuilds
> the measure on both rulings — and whose own kill criterion then fired, for a
> different and more fundamental reason.

**Status:** durable results record. It discharges the axis-5 exposure-metric
handoff. Conclusions and criteria were fixed in
[`stealth_exposure_prereg.md`](stealth_exposure_prereg.md) and committed
(`34a892e`) before the reader existed, let alone a reported row.

**The headline. E2 — the prediction this study was written around — MOVED, and
inverted completely.** The pre-registration predicted the inherited attacker
would read *louder* than every profile, because it has no non-action dwell to let
the level decay between events. It reads **quieter than all five, at every decay
constant in the band and at both pre-registered tier placements — ten cells of
ten, CI-disjoint, with no cell going the other way.**

The reason is not a subtlety of the measure. It is that **the tempo premise was
false**, and false for a reason the study had to correct before it could measure
anything: the inherited attacker's apparent speed is an artefact of the substrate
writing one attack-record row **per vulnerability tried** rather than per action.
Counted as actions, it takes **371 steps per run against the profiles' 463–674**.
The fast-and-loud attacker is neither, once its own record is read as actions.

Two other things follow, and the second is the one that bounds what may be
claimed. The reader itself is sound: it discriminates between profiles (E1) and
is not a decayed event counter (E4, the kill criterion, held decisively). But the
arm separation it reports is **mix-borne, not tempo-borne** (E5 moved), so axis 5
may not claim it as a tempo result — and the mix that produces it lives largely in
tactics that dispatch no substrate action at all.

## 1. What was built

A reader over the visit stream, in `measures.py` §9. At each place visit:

```
    D(i) = D(i−1) · exp(−Δ(i) / τ)  +  d(i) ,     d(i) = ρ^(4 − tier) · m(i)
```

The tier is the corpus's ordinal observability ranking over all fifteen tactics
([`stealth_conceptualisation.md`](stealth_conceptualisation.md) §7), which is the
**only grounded part of the family**; `ρ`, `τ` and the CVSS weight `δ` are
declared, swept, and each carries a null in its band
([`../../declared_value_provenance.md`](../../declared_value_provenance.md) §6.6).

**It reports; it changes nothing.** `D` is read by no routing rule, no dwell
draw and no mutation selector. No attacker state was added, so no S2 question
arises, and the runs it scores are runs that would have happened anyway.

**The unit is the place visit, not the attempted action**, because the ranking's
three loudest tactics — exfiltration, defence-impairment, impact — are dwell-only
under `v2_partial`. Scoring only attempted actions would have left the ranking's
top rung inert. §5 records what that decision costs in interpretation.

### 1.1 One instrumentation change, and it bought nothing

The CVSS half of the design needed a figure that **cannot be recovered post hoc**:
`MovementRecord` carries no vulnerability identity, the adversary's `curr_vulns`
is overwritten by the next exploit action, and the substrate's scorer channel
sees only compromise-causing vulnerabilities. The record therefore gained one
float, `exploitability` — the mean **initial** `cvss / 5.5` over the
vulnerabilities an action engaged, initial because the substrate mutates the live
attribute upward on compromise while `cvss` is never touched. It is an
observation, popped from the golden serialisation exactly as `n_compromised` and
`interrupted_by_name` are; **no golden moved** and the full suite passes
unchanged (776 passed, 240 skipped).

**And the term it enabled is inert.** Sweeping `δ` across its entire declared band
— 0 to 1.0, from ablation to the reductio where a maximally exploitable
vulnerability contributes nothing at all — moves every profile's mean exposure by
**less than 0.1 %** (`pure_steal` 0.49777 → 0.49749). Two measured reasons compound:

- **Reach.** Visits at exploit-dispatching places are 18.6 % of all visits, but
  **73 % of them engage no vulnerability at all** — blocked on an unmet
  precondition, or finding nothing above the substrate's own RoA threshold. Only
  **5.0 % of visits** carry a figure for the term to act on.
- **Centring.** Across those 1 306 visits the mean exploitability is **0.4955**,
  within half a percent of the fixed point at which the modulation is exactly
  1.0. The term is not merely small on average; it is centred on doing nothing.

This is recorded as a **negative result about the design, not suppressed**. The
handoff proposed the CVSS source and the meeting named it; it was built, swept in
both directions, and it does not move the measure on this substrate. The record
widening stays, because the field is what allows that to be *known* rather than
assumed, and because a future increment rule with a different shape can use it —
but no result here rests on it, and E3's verdict below says so formally.

## 2. Verdicts

50 movement runs (5 profiles × 10 seeds, `v2_partial`, retrace on, **no MTD**,
15 000 s horizon) and 10 baseline runs. One run set yielded the entire sweep: every
declared parameter is read off the recorded stream, so no cell required its own
simulation.

| | Conclusion | Verdict |
|---|---|---|
| **E1** | the curve is non-degenerate across profiles | **held** — 2 of 4 adjacent pairs CI-disjoint |
| **E2** | the baseline separates from every profile, and reads louder | **MOVED — inverted, 10/10 cells** |
| **E3** | the CVSS direction is decided by evidence | **held** — the two directions agree on every verdict; inverse adopted, and recorded **inconsequential** |
| **E4** | **KILL CRITERION** — not a repackaged event counter | **held** — Spearman −0.529 against a threshold of 0.90 |
| **E5** | any arm separation is tempo-borne, not mix-borne | **MOVED — mix-borne** |

**E1 held, and modestly.** Mean exposure runs from 0.4936 (`infrastructure_setup`)
to 0.6451 (`double_extortion`), a spread of 1.31×, with `pure_steal`↔`aggregate`
and `pure_impediment`↔`double_extortion` CI-disjoint. The full ordering is **not**
supported at ten seeds, exactly as the criterion anticipated and declined to
require.

**E4 held decisively, and its sign is the interesting part.** The correlation
between a run's mean exposure and its visit count is **negative** (−0.529): the
attacker that acts *most* is the quietest. `infrastructure_setup` takes 674 visits
per run and reads lowest; `double_extortion` takes 463 and reads highest. A
decayed event counter would have produced a strong positive correlation, so the
measure is carrying the ranking rather than the tally — which is the whole reason
the kill criterion was committed in that direction.

## 3. Why E2 inverted — the tempo premise was an accounting artefact

**The correction the study had to make first.** `_do_exploit_vuln` appends one
attack-record row **per vulnerability tried**, not per action. Over these ten
baseline runs that is **1 394 rows against 371 actions — an inflation of 3.75×**.
Left uncorrected, the inherited attacker would have been handed a nearly fourfold
louder campaign by bookkeeping, and E2 would have been won by an artefact. The
collapse is exact rather than heuristic: the native FSM never dispatches
`EXPLOIT_VULN` twice in succession, so a run of consecutive exploit rows is one
action by construction.

**Counted correctly, the profiled attacker is the busier one.**

| arm | events per run |
|---|--:|
| baseline — attack-record **rows** | 1 393.8 |
| baseline — **actions** | **371.3** |
| `double_extortion` | 463.3 |
| `pure_impediment` | 464.8 |
| `aggregate` | 490.2 |
| `pure_steal` | 508.4 |
| `infrastructure_setup` | 674.2 |

**And on tempo alone the arms do not separate at all.** At `ρ = 1` every act
scores 1.0, so the ranking does nothing and the curve is pure event tempo. There
the inherited attacker sits **fourth of six**:

| at ρ = 1 (tempo only) | mean exposure |
|---|--:|
| `double_extortion` | 1.611 ± 0.038 |
| `pure_impediment` | 1.633 ± 0.029 |
| `aggregate` | 1.664 ± 0.039 |
| `pure_steal` | 1.690 ± 0.024 |
| **baseline** | **1.733 ± 0.022** |
| `infrastructure_setup` | 2.073 ± 0.062 |

Mid-pack, above three profiles and below one, with overlapping intervals on either
side. **The whole of the arm separation at the declared `ρ` is created by the tier
ranking**, i.e. by *which tactics* each attacker engages — which is precisely what
E5 was written to detect, and it moved: the arms' mean-increment intervals are
themselves disjoint (baseline 0.2197 ± 0.0011 against the profiles' 0.3259 ±
0.0157).

**This qualifies a claim on record.** The parent design record's §1.1 characterises
the inherited attacker as turning "~815 successful actions into ~40 distinct hosts
(~20 actions per host)" and the profiled attacker as low-and-slow against it. That
figure counts attack-record rows, so its action count — and the actions-per-host
ratio built on it — is inflated by the same per-vulnerability accounting measured
above. The event-wise contrast §1 rests on is **not wrong in every part** (the
non-action dwell fraction and the terminal-mode contrast are unaffected; both are
properties the baseline structurally lacks), but the *tempo* half of it does not
survive a per-action reading. Flagged here rather than actioned: correcting it
touches `baseline_ledger`, `EventWiseComparable.n_events` and
`actions_per_distinct_host`, and would move figures already reported in experiment
1 and experiment 2. That is a disposition, not a session's call — see §6.

## 4. The inversion is robust in direction across every setting tried

| placement | profiles reading above the baseline, per τ cell |
|---|---|
| **declared** (recon tier 1, lateral tier 2) | 5/5 at every τ in {3.75, 15, 60, 240, 960} |
| **recon active** (recon → tier 3) | 5/5 at every τ |
| lateral exploit (lateral → tier 3) — *swept, outside E2's criterion* | 5/5, 4/5, 3/5, 4/5, 4/5 |

The third row is reported although E2's criterion named only the first two: moving
lateral-movement to its exploit reading lifts the baseline most, because
`ENUM_HOST` carries 38 % of its increment mass. Even there the baseline is **never
above any profile in any cell** — the inversion weakens and never reverses.

## 5. What this does not license, and the caveat that matters most

**The profiled attacker's loudness is concentrated where the simulator does
nothing.** Decomposing each profile's total increment mass by tactic:

| profile | top contributors | share from **dwell-only** tactics |
|---|---|--:|
| `double_extortion` | impact 34 %, persistence 12 %, discovery 12 % | **62 %** |
| `pure_impediment` | impact 29 %, persistence 16 %, defence-impairment 10 % | **61 %** |
| `aggregate` | impact 17 %, persistence 14 %, exfiltration 14 % | **59 %** |
| `pure_steal` | exfiltration 22 %, persistence 15 %, execution 9 % | **56 %** |
| `infrastructure_setup` | lateral-movement 25 %, execution 15 %, priv-esc 11 % | **17 %** |
| baseline | ENUM_HOST 38 %, SCAN_PORT 26 %, EXPLOIT_VULN 23 % | — (no such concept) |

Four of five profiles draw the **majority** of their exposure from tactics that,
under `v2_partial`, consume time and **dispatch no substrate verb at all**. This is
consistent with the model's stated position — engaging a tactic is behaviour
whether or not a verb fires, which is the same argument `visit_distribution` rests
on — and it is *not* a defect of the reader. But it means the sentence "the
profiled attacker is louder" is a claim about **modelled behaviour**, not about
anything the substrate executed, and a reader who took it as the latter would be
wrong. The one profile that draws its exposure from dispatching tactics,
`infrastructure_setup`, is also the one that sits closest to the baseline.

Explicitly **not licensed**:

- **No badge move.** Axis 5 stays **NOT ADDRESSED**, and this record does not
  propose otherwise. The parent record's §9 reserves DESIGNED for the stealth
  *state* of option 1(a) — a mechanism that changes what the attacker does — and
  this is a reader, which changes nothing. The shipped disengagement measure
  declined a badge move on the identical reasoning, and the same reasoning applies
  here. What this discharges is the axis's **M8b measurement field**, which is a
  different thing and is updated as such (§6).
- **No tempo claim.** E5 moved: the separation is mix-borne. On tempo alone the
  arms are unseparated (§3).
- **No detection claim.** `D` is a declared observable, not a probability of being
  detected, and no threshold on it is computed. `D` carries no units; only
  comparisons at a common setting mean anything.
- **No cross-arm time claim without its caveat.** Under S3-R the two arms are
  priced by different clocks. `ExposureCurve` carries its clock name and
  `comparable_with` refuses the pairing, so the asymmetry travels with the figure;
  every cross-arm number above is at `δ = 0`, where both arms are scored by the
  identical rule.
- **No claim from the CVSS term.** It is inert (§1.1), and E3's "inconsequential"
  verdict is a statement that the unattested direction did not matter here — not
  that either direction is correct.

## 6. What a successor should do

**Three dispositions, all Marc's; none is a build.**

- **The per-vulnerability row count (§3).** `baseline_ledger` and everything built
  on it count rows, so the baseline arm's event count is inflated 3.75× wherever
  it is compared to the movement arm's per-action records. Whether the suite's
  cross-arm event definition is corrected — and whether experiment 1's and
  experiment 2's affected figures are restated — is a disposition. **Recommend
  raising it as an audit row**; the correction is three lines and the restatement
  is not.
- **Whether the M8b field is discharged.** Axis 5's field asks for "attack-event
  rate visible to substrate statistics per unit time (a detectability proxy),
  dwell fraction in non-action tactics, and tempo response to MTD frequency". The
  first is now built in a stronger form and has run; the third is untouched,
  because this study is no-MTD by design. The field is updated to say so and the
  badge is left alone.
- **Whether the dwell-only increment convention stands (§5).** Scoring a
  dwell-only visit as a tier-4 noisy event is defensible and is defended above,
  but it is a modelling choice with a large measured consequence — it carries the
  majority of four profiles' exposure. An alternative reader that scored only
  dispatching visits would be a different measure, not a fix, and would report the
  opposite headline. **Recommend it be ruled rather than inherited.**

**Not** re-specify E2 and re-run. The stopping rule was honoured: no criterion was
relaxed, no band re-centred, no arm added, and the inverted result is reported as
the negative it is. The pre-registration predicted the direction and was wrong,
which is the outcome pre-registration exists to make visible.

**The live question** is whether the tempo contrast the parent record's §1 claims
survives *any* per-action instrument. This study says it does not survive this
one. That is one instrument, on the no-MTD arm, at ten seeds — but §1 is the
argument the whole axis-5 design rests on, and it now has a measured
counter-example rather than an argument against it.

## 7. Evidence

- [`stealth_exposure_prereg.md`](stealth_exposure_prereg.md) — the five
  conclusions and their criteria, committed before any reported row (`34a892e`).
- [`stealth_conceptualisation.md`](stealth_conceptualisation.md) — the parent
  design record; §6 carries the amendment this build's decay rule required.
- `data/ogasp/movement/exposure_rules.json` — the declared family and its ledger;
  `exposure_increments.json` its compiled view, reproducing 0 of 63 cells.
- `data/results/stealth_exposure/` (untracked/regenerable) — `run_study.py`,
  `analyse.py` computing every verdict from the recorded streams, `decompose.py`
  for §3 and §5, `verdict.txt`, `verdicts.json`.
- `data/misc/_viz/stealth_exposure/` (untracked/regenerable) — three figures and
  the script that draws them, re-running the shipped reader over the same
  recorded runs: the per-arm trajectories (`fig1`), the arm means at the declared
  ranking beside the tempo-only null (`fig2` — the pair that shows the separation
  is created by the ranking rather than by tempo), and the decay-constant sweep
  (`fig3`).
- `measures.py` §9 and its unit gate in
  `tests/l3_simulation/test_movement_measures.py` — hand-worked streams pinning
  the recursion, the closed-form time average, the baseline collapse and the
  cross-clock guard; the declared family's own gate is
  `tests/l3_simulation/test_movement_exposure.py`.
- [`../../apt_model_criterion.md`](../../apt_model_criterion.md) axis 5 — the M8b
  field this discharges and the badge it does not move.
