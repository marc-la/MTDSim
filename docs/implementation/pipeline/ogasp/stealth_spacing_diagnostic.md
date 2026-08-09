---
status: durable
created: 2026-08-09
topic: "The spacing diagnostic — the axis-5 contrast stated at the level it survives at. Four of five profiles space their substrate verb invocations 1.5–1.8× further apart than the inherited attacker, CI-disjoint, and an ablation attributes the entire margin to the non-action tactics. Not pre-registered: a re-read of the existing corpus, reported as a diagnostic"
---

# Inter-invocation spacing — the low-and-slow contrast holds, and the non-action tactics are all of it

**Status:** durable investigation record. It is **not** a pre-registered study and
carries no conclusions committed in advance, so nothing here scores or rescores
E1–E5 or D1–D5. It is a diagnostic re-read of the corpus the two exposure studies
already wrote, prompted by a question those studies did not ask.

**The question.** Both studies compared the arms on the *level* of `D` — its mean,
its time-average, its p90/p50 concentration. Neither reported the quantity the
low-and-slow argument is actually about: **how far apart the attacker puts the
acts the substrate can see**. The design record's §1 states the contrast as a
tempo one; this measures the tempo directly, in the unit `D`'s decay integrates.

**The headline.** Under R1 (a dwell-only tactic consumes time and scores nothing)
and with the baseline collapsed to invocations, **four of five profiles space
their verb invocations 1.5–1.8× further apart than the inherited attacker**, with
seed-level confidence intervals disjoint from the baseline's. The fifth,
`objective_none_c2`, is **denser** than the baseline, also CI-disjoint. And an
ablation attributes **the whole of the margin** to the non-action tactics: delete
them from the recorded stream and every profile falls under the baseline.

## 1. What was measured, and in what unit

The unit is the **gap between consecutive verb-invoking visits** — the interval
across which `D` decays. It is not a new statistic: it is `ExposureCurve.gaps`,
already computed by the shipped reader, read at the R1/R2 configuration.

The baseline is scored **collapsed to invocations**, which is the like-for-like
unit: the movement arm's dispatch runs the same vulnerability loop internally.
The per-vulnerability reading is reported alongside, because the S3-R pricing
asymmetry is the confound the duty-cycle study's D4 fired on and it does not stop
being a confound here. Four readings, none requiring a re-simulation:

1. the **gap distribution** per arm
2. the **composition** behind it — what share of visits, and of gap time, is
   dwell-only
3. the **ablation** — delete the dwell-only visits and re-measure the same
   invocations
4. the **substrate re-pricing** — charge every invoking visit the substrate's own
   `ATTACK_DURATION` for the verb it dispatches, instead of the declared duration
   catalogue

Both counterfactuals hold routing fixed. They re-price a recorded trajectory, so
they say what the *same walk* would have looked like under different pricing —
not what a differently-designed attacker would have done. That bounds §4 in
particular.

> **Class labels.** This record is written after the objective-tactic rename and
> uses the current labels. The corpus it reads carries the retired ones
> (`pure_steal` and siblings), which is why the analysis scripts crosswalk rather
> than rewrite; mapping in [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

## 2. The spacing result

50 movement runs (5 profiles × 10 seeds, `v2_partial`, retrace on, **no MTD**,
15 000 s horizon) and 10 baseline runs — the same corpus both studies used.

| | p25 | median | p75 | p90 | mean | 95 % CI (seeds) | %<10 s | %>60 s |
|---|--:|--:|--:|--:|--:|:--|--:|--:|
| objective_exfiltration_impact | 6.1 | 33.1 | 85.7 | 148.2 | **57.0** | [54.5, 60.3] | 31.1 | **35.4** |
| objective_impact | 8.7 | 29.5 | 76.4 | 141.1 | **53.4** | [50.7, 56.9] | 27.4 | 31.8 |
| aggregate | 7.5 | 29.0 | 72.5 | 126.2 | **51.0** | [48.9, 53.5] | 29.7 | 30.9 |
| objective_exfiltration | 7.9 | 29.8 | 66.6 | 117.2 | **47.0** | [45.1, 49.5] | 28.6 | 28.7 |
| objective_none_c2 | 2.7 | 8.5 | 33.7 | 77.5 | **26.2** | [24.9, 27.8] | 53.2 | 14.5 |
| **baseline (invocations)** | 5.0 | 20.0 | 25.0 | 84.9 | **31.1** | [28.8, 34.0] | 48.6 | **12.5** |
| baseline (per-vulnerability) | 3.8 | 5.7 | 9.9 | 20.0 | 8.3 | — | 75.2 | 0.0 |

The run is the independent unit, so the interval is taken across seeds rather
than across gaps.

**The column that matters for a decay measure is the last one.** Four profiles
put **28.7–35.4 %** of their gaps beyond the declared decay constant against the
baseline's **12.5 %** — 2.3–2.8× as many intervals long enough for the level to
fall most of the way to the floor. That is the low-and-slow mechanism expressing
itself in the measure's own currency.

**`objective_none_c2` inverts, and the composition says why.** It is not that the
profile lacks non-action tactics; it is that it has the fewest of them and chains
the cheapest verbs. Its dwell-only share of visits is **15.2 %** against the other
four profiles' 37.3–43.4 %, and 35.6 % of its visits are the two 4.4 s tactics
(lateral-movement at 23.5 %, credential-access at 12.1 %) firing `ENUM_HOST` and
`BRUTE_FORCE` back to back. **The profile with the least dwell is the one that
loses**, which is the mechanism working rather than an anomaly.

**Before any decay is applied**, the same contrast is already present as a rate:
17.5–21.3 invoking events per 1 000 s for the four, against the baseline's 24.8
and `objective_none_c2`'s 38.2. §6 says what this costs the claim.

## 3. The ablation — the non-action tactics are the whole of the margin

Delete the dwell-only visits from the recorded stream and re-measure the spacing
between the same invocations. Each gap is then the invoking tactic's own declared
dwell alone.

| | mean gap | ablated | %>60 s | ablated |
|---|--:|--:|--:|--:|
| objective_exfiltration_impact | 57.0 | **25.3** | 35.4 | 12.8 |
| objective_impact | 53.4 | **26.8** | 31.8 | 14.0 |
| aggregate | 51.0 | **24.2** | 30.9 | 12.0 |
| objective_exfiltration | 47.0 | **23.3** | 28.7 | 10.9 |
| objective_none_c2 | 26.2 | **18.9** | 14.5 | 8.8 |
| **baseline** | 31.1 | 31.1 | 12.5 | 12.5 |

**All five fall below the baseline**, and the long-gap fraction collapses onto it
(8.8–14.0 % against 12.5 %). The result is therefore exactly what it looks like:
*this attacker has non-action tactics and the inherited one does not*.

**That is the framing's strength, not its embarrassment.** It makes the contrast
a **structural** claim about a class of behaviour the baseline cannot represent
at all, and the ablation is the evidence that the effect is attributable to the
modelled construct rather than to a tuned parameter — which is a property very
little else in this model's declared family can claim. What it forecloses is any
reading in which the spacing is an emergent consequence of routing, of the
outcome overlay, or of the terrain. It is not; it is the dwell states, doing what
they were declared to do.

## 4. The catalogue counterfactual — and a hypothesis it kills

The obvious suspicion is that the declared duration catalogue is suppressing the
mechanism: four of the eight verb-invoking tactics carry a 4.5 s mean dwell while
the substrate prices the verbs they dispatch at 15–25 s, so a profile chaining
two action tactics is faster back-to-back than the baseline can structurally be.

**It does not survive the test.** Re-pricing every invoking visit at the
substrate's own `ATTACK_DURATION` **shrinks** the profiles' margin rather than
widening it:

| | median | re-priced | mean | re-priced | %>60 s | re-priced |
|---|--:|--:|--:|--:|--:|--:|
| objective_exfiltration_impact | 33.1 | 25.0 | 57.0 | 46.8 | 35.4 | 26.0 |
| objective_impact | 29.5 | 24.9 | 53.4 | 39.0 | 31.8 | 19.1 |
| aggregate | 29.0 | 21.8 | 51.0 | 40.2 | 30.9 | 20.6 |
| objective_exfiltration | 29.8 | 20.0 | 47.0 | 36.8 | 28.7 | 19.3 |
| objective_none_c2 | 8.5 | 15.0 | 26.2 | 19.1 | 14.5 | 5.8 |
| **baseline** | 20.0 | 20.0 | 31.1 | 31.1 | 12.5 | 12.5 |

The cheap exploit tier is not what pays for the spacing — the catalogue's **long**
invoking tactics are, and substrate pricing strips them: command-and-control
falls from a 45 s declared dwell to `SCAN_NEIGHBOR`'s 5 s, reconnaissance from
35 s to `SCAN_HOST`'s 5 s. So the catalogue is currently *helping*.

**Two things follow.** The ordering **survives** substrate re-pricing for four of
five profiles, which is a robustness result for the claim rather than a
calibration debt. And there is no case here for a calibration sweep on the
exploit tier: the tier is not the mechanism's obstacle, and a sweep aimed at it
would be aimed at the wrong number.

Half the gap time comes from each source, which is the finer version of the same
point: the dwell-only inserts contribute **49.7–55.7 %** of gap time for the four
(27.7 % for `objective_none_c2`), and the invoking tactics' own declared dwell
contributes the rest.

## 5. What this licenses, and what it does not

**Licensed.**

- An **inter-invocation spacing** contrast, cross-arm, stated at invocation
  granularity with the per-vulnerability reading shown beside it — which
  [fig4](../../../../data/misc/_viz/stealth_exposure/fig4_granularity_flip.png)
  already puts on one pair of axes.
- The attribution: the margin is the non-action tactics, by ablation.
- Robustness of the ordering under substrate re-pricing, four of five.

**Not licensed.**

- **No badge move.** Axis 5 stays **NOT ADDRESSED**. This is still a reader, and
  §9 of the parent design record reserves DESIGNED for a stealth *state* — a
  mechanism that changes what the attacker does. Nothing here changes any
  routing rule, dwell draw or mutation selector.
- **No rescoring of D2.** The duty-cycle study's verdict stands as scored. It is
  not in tension with §2: `p90/p50` measures **burstiness**, and the baseline
  genuinely is burstier — 48.6 % of its gaps under 10 s, then a p90 of 85 s. An
  arm can be more tightly clustered *and* more densely spaced than another. §6.
- **No escape from D4.** The granularity confound is unresolved and this record
  does not resolve it; it states its result in the collapsed unit and shows the
  other.
- **No claim that a detector would find this.** There is still no detection model
  for the spacing to matter against, which remains this axis's own argument.

## 6. Which statistic should carry the claim

**Not `p90/p50`.** It is the duty-cycle study's pre-registered primary and it
answers a different question — whether the level *towers over* its own typical
value. The baseline scores high on it because its gap distribution is bimodal,
not because it is quiet. A spacing claim carried on a burstiness statistic will
read as contradicted by D2 when it is not.

**The gap distribution, and the decay-weighted level over time.** The survival
curve is bounded by construction, threshold-free, and it shows the shape of the
disagreement rather than a single number that picks a side —
[fig7](../../../../data/misc/_viz/stealth_exposure/fig7_gap_survival.png).

**And state what the decay adds over a raw event rate**, because §2's last
paragraph shows a large part of the contrast is already present as invoking
events per unit time. The decay's genuine contribution is that it models a
detector that *forgets*: it is what makes the deep-silence-versus-shallow-quiet
crossing ([fig5](../../../../data/misc/_viz/stealth_exposure/fig5_quiet_frontier.png))
a finding about two different shapes of quiet rather than a re-statement of two
different rates. A write-up that does not say this invites the reader to ask what
the exponential bought, and the honest answer is *shape, not separation*.

## 7. Two defects in the figure scripts, found and fixed

Both are audit-trail defects rather than result defects, and both are the kind
that only surface when a figure is regenerated.

- **Neither study's script could reproduce its own figures.** `PROFILES` had been
  updated to the post-rename objective-tactic labels in both
  `stealth_exposure_viz.py` and `dutycycle_viz.py`, while the recorded corpus
  keeps the retired ones. The hard-coded list matched nothing and every figure
  died on an empty-group error. Both scripts now read the class labels off the
  corpus and crosswalk to the current names for display.
- **Study 1's script had silently drifted onto study 2's convention.**
  `exposure_model` defaults to the R1/R2 semantics ruled on 2026-08-06, so
  re-running the study-1 script redrew study-2 numbers under study-1 titles — the
  baseline moving from below all five profiles to mid-pack, which is precisely the
  supersession the record warns about. The script now pins
  `score_dwell_only=True, verb_level=False` explicitly and reproduces the archived
  figures exactly.

`fig1_exposure_trajectory.png` was **retired**: it is the study-1-convention
trajectory, exactly superseded by fig6. fig2 and fig3 are kept as study 1's visual
audit trail and now carry a SUPERSEDED CONVENTION line in the figure itself, so
neither can be pulled into a chapter without it.

## 8. Evidence

- `data/results/stealth_exposure/spacing.py` (untracked/regenerable) — every
  number above, writing `spacing.txt` and `spacing.json`.
- `data/misc/_viz/stealth_exposure/spacing_viz.py` (untracked/regenerable) —
  **fig6** the R1-scored trajectory per arm, **fig7** the gap survival curve
  as-run and ablated.
- [`stealth_dutycycle.md`](stealth_dutycycle.md) — the R1/R2 rulings this reads
  at, D4's granularity flip, and the p90/p50 verdict §5 reconciles with.
- [`stealth_exposure_metric.md`](stealth_exposure_metric.md) — study 1, and the
  per-vulnerability inflation that §2's last row shows.
- [`stealth_conceptualisation.md`](stealth_conceptualisation.md) §1.4 — the
  pricing asymmetry that bounds every time-denominated cross-arm reading, stated
  before either study ran.
- `data/ogasp/tactic_durations.json` and `mtdnetwork/data/constants.py`
  (`ATTACK_DURATION`) — the two duration families §4 puts against each other.
