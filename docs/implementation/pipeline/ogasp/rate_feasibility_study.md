---
status: durable — pre-registered, run, and reported
created: 2026-07-28
updated: 2026-07-28
topic: "The rate feasibility study (S3, analysis half) — the pre-registered sweep of the four group anchors over their catalogue-derived bands against the MTD mutation interval, plus the same-mean Erlang-k shape check on the low-and-slow group, and its verdicts. §1–§5 were committed BEFORE any sweep output existed (e84bd2a); §6–§9 report 1 728 runs against those committed criteria. Headline: no anchor band inverts any conclusion and the same-mean shape substitution is inert, but the evaluation's operating mutation interval sits inside a degenerate region where ASR cannot discriminate, and the per-profile ordering is a power failure at ten seeds."
---

# The rate feasibility study — does any reported conclusion survive the arbitrariness of the timing numbers?

**Status: run and reported.** §1–§5 — the question, the conclusions in scope, the
acceptance criteria, the parameter space and the grid — were committed at
`e84bd2a` with **no results in hand**, and are unedited below. §6–§9 were appended
after the sweep ran and report 1 728 runs against those committed criteria. The
commit ordering in `git log` is the pre-registration evidence the validity
framework demands
([`../../../notes/ch3_design/operational_validation.md`](../../../notes/ch3_design/operational_validation.md),
anti-circularity rule 3's pre-registration ordering, ratified for this study by the
handoff's step 1).

**Chain position.** The analysis half of S3, executed against the build half's
regime ([`stochastic_timing_design.md`](stochastic_timing_design.md) §3: each
tactic's declared `duration_s` is the mean of an exponential firing time). Sibling
to the S1 transition-weight sweep
([`../../../handoffs/2026-07-27_tactic_weight_sensitivity_study.md`](../../../handoffs/2026-07-27_tactic_weight_sensitivity_study.md));
the two share a reporting shape (per-cell CSV rows, CI-based stability verdicts)
and run against the same controller mapping version.

**The question, fixed before anything runs.** The claim under test is **not** "are
the declared durations right" — they are declared, and a per-tactic duration is not
a measurable property of the world, so they cannot be right. It is:

> **Does any conclusion the timed evaluation reports change its *direction* when
> each group anchor moves across its published band, or when the declared
> distribution family changes at fixed mean?**

A conclusion that survives is reportable as "X, stable across the declared band".
A conclusion that inverts at a named boundary is a *more* valuable result, not a
failure — the evaluation-burden note commits to reporting it as such, and the
anti-circularity rules forbid tuning anything to avoid it.

---

## 1. Conclusions under test (pre-registered)

The scope is the three conclusion families the handoff names, plus the ASR floor
experiment 1 reported. Each is stated as a *direction or ordering*, because that is
what a sensitivity sweep can confirm or invert — magnitudes are parameter choices
under shape-not-scale and are not defended.

- **C1 — profile-vs-baseline tempo ranking.** The profiled movement attacker's
  elapsed time-to-first-compromise exceeds the native baseline attacker's, under
  like MTD conditions. (Experiment 1's 238 s vs 5294 s finding, restated as a
  direction for the timed regime.)
- **C2 — the MTD direction.** Turning MTD on does not *help* the attacker, on
  either arm: MTD-on mean compromised-host count ≤ MTD-off, and MTD-on elapsed
  time-to-first-compromise ≥ MTD-off, per profile.
- **C3a — per-profile ordering.** The ordering of the four class profiles (plus
  the aggregate null) by mean compromised-host count — the breadth metric that
  discriminated in experiment 1 — is stable across the anchor bands: whatever
  ordering the central cell shows, the band does not invert any pair the central
  cell separates.
- **C3b — failure-mode identity is the profile's.** The modal terminal mode of a
  profile's runs (friction / churn / sink-termination / horizon) is a function of
  the profile, not of where in its band an anchor sits. This is the demonstrated
  claim behind the APT-criterion's axis-2 badge
  ([`../../apt_model_criterion.md`](../../apt_model_criterion.md)); if timing
  arbitrariness can flip it, the badge is over-claimed and must be re-scored.
- **C4 — the ASR ordering.** Profiled ASR < baseline ASR under like conditions
  (experiment 1: 0/100 profiled runs reached the objective; the baseline reaches
  it routinely). The sweep asks whether some corner of the declared bands makes
  the profiled attacker reach the objective — which would be a regime change worth
  naming, not an embarrassment.

**Not in scope:** any magnitude claim; the MTD-mechanism ranking (experiment 2's
result, not yet on record); internal MTTC (the per-action metric the timing regime
deliberately does not touch — design record §2).

## 2. Acceptance criteria (pre-registered)

Per conclusion, per cell, the verdict vocabulary is fixed in advance as the
handoff's gate 3 requires:

- **Stable across the band** — the direction/ordering holds in every swept cell,
  and in at least the central and both extreme cells the relevant comparison is
  **CI-separated** (non-overlapping 95 % intervals: normal-approximation for
  means, Wilson for ASR proportions — the experiment-1 conventions).
- **Inverts at a named boundary** — at least one cell shows the *opposite*
  direction with CI separation. The boundary is named in ratio units
  (mutation interval ÷ the swept anchor's mean dwell), and the first-pass grid is
  refined with one extra cell each side of it before the verdict is written.
- **Indeterminate at this sample size** — neither direction achieves CI
  separation in the cells that matter. Recorded as such, never rounded up to
  "stable". With n = 10 seeds per cell, only standardised effects of roughly
  1.3 SD separate; the study is powered for direction changes, not subtleties,
  and says so.

Ordering claims (C3a) use pairwise comparison: a pair counts as *invertible
evidence* only if the central cell separates it (CI-separated) and some band cell
separates it the other way. Pairs never separated anywhere are indeterminate.
Categorical claims (C3b) use the modal terminal mode per (profile, cell) over the
10 seeds: stable means the mode matches the central cell's mode in every swept
cell; any mode flip is reported with its cell.

**Paired seeds.** Every cell runs the same ten seeds (0–7, 42, 1234 — the
experiment-1 set), so cell-to-cell comparisons are paired; a per-seed sign flip
count accompanies each CI verdict as a secondary check.

**Nothing is tuned.** No declared value changes in this study, whatever the
result. If a conclusion is not robust, the negative result is the deliverable
(handoff hard constraint; evaluation-burden note).

## 3. The parameter space — the anchors and their bands, derived not invented

The free parameters are the four group anchors (anti-circularity rule 2: sweep
identifiable group anchors, never fifteen independent dwells). Each anchor gets a
scale factor *m*; every member tactic's dwell mean becomes
`m × relative_multiplier × anchor.duration_s`, so per-tactic multipliers ride
along unchanged and the profiles' relative structure is preserved (handoff step 2).
`prep-off-network` stays 0.0 (degenerate band; immediate transition).

**The anchor's band is taken from the catalogue, two ways that agree.** The
catalogue publishes `sweep_range` per *tactic*, as a band on
`relative_multiplier` in group-anchor units (`meta.sweep_range_units`; the
timeline runner's `dwell_table` already consumes it with exactly this
arithmetic). An anchor-level band must not widen any member's published band, so:

- reading (a): the band of the group's **reference tactic** (the ×1.0 member that
  defines the anchor);
- reading (b): the **intersection** over members of `[lo/mult, hi/mult]` — the
  factor range within which *every* member's effective multiplier stays inside
  its own published band.

| Anchor | Members (mult, band) | (a) reference band | (b) intersection | **Band used** |
|---|---|---|---|---|
| scan-shaped | recon (1.0, [0.5, 2]); discovery (1.0, [0.5, 2]) | [0.5, 2] | [0.5, 2] | **[0.5, 2]** |
| exploit-shaped | initial-access, priv-esc, cred-access (1.0, [0.5, 2]); lateral-movement (1.0, [0.25, 4]) | [0.5, 2] | [0.5, 2] | **[0.5, 2]** |
| stealth-low-and-slow | persistence, stealth, C2 (1.0, [0.25, 4]); execution (0.5, [0.1, 2] → m ∈ [0.2, 4]); defense-impairment (0.5, [0.1, 4] → m ∈ [0.2, 8]) | [0.25, 4] | [0.25, 4] | **[0.25, 4]** |
| objective-execution | collection (1.0, [0.5, 2]); exfiltration (1.0, [0.25, 4]); impact (1.0, [0.1, 5]) | [0.5, 2] | [0.5, 2] | **[0.5, 2]** |

The two readings coincide for all four groups, so the bands are the catalogue's
own with no editorial widening (handoff hard constraint 2). Tier-1 anchors
(scan, exploit) are *swept but never re-declared*: sweeping asks "what if the
substrate priced this differently", it does not tune the substrate constant
(anti-circularity rule 1 concerns tuning, and this study tunes nothing).

**The informative axis is the ratio.** The thesis's contest is tactic dwell
against MTD mutation interval, so the mutation interval — a free experimental
variable under ruling R4 — is the sweep's other axis. Reported ratios use the
stealth anchor's mean (the longest behavioural dwell, 45 s central) as the dwell
reference: interval/dwell from 50/180 ≈ 0.28 up to 800/11.25 ≈ 71 across the
grid, a ~250× span of the contest — wide enough to contain an Anderson-style
degenerate boundary ("the attack can never succeed if the churn rate is faster
than the completion rate") if one lies anywhere near the declared operating
point (interval 200, stealth dwell 45: ratio ≈ 4.4).

## 4. The grid (pre-registered)

All cells: horizon 15 000 s, experiment-1 geometry (50/5/8/4), overlay-on arm
(seeded at reconnaissance), ten seeds (0–7, 42, 1234), all five profiles
(4 classes + aggregate null), MTD scheme `random` where on.

- **Sweep A — anchor robustness (one-at-a-time).** Each anchor at its band's
  {lo, hi} with the other three at 1.0, plus the all-central cell: 9 anchor
  configurations × MTD ∈ {off, random @ 200} × 5 profiles × 10 seeds =
  **900 movement runs**.
- **Sweep B — the ratio axis.** All-central anchors × interval ∈
  {50, 100, 400, 800} × 5 profiles × 10 seeds = **200 movement runs** (200 s and
  off are already in sweep A). Plus the interaction probe at the band corner the
  ratio contest cares about most: stealth anchor at 4.0 (dwell 180 s ≫ interval)
  and at 0.25 (dwell 11.25 s ≪ interval) × interval ∈ {50, 800} × 5 profiles ×
  10 seeds = **200 movement runs**.
- **Sweep C — the distribution family at fixed mean (the §3.2(3) check).** The
  five stealth-low-and-slow tactics draw from a same-mean **Erlang-4**
  (sum of four exponentials each of mean μ/4: CV drops from 1 to 0.5, mass
  concentrates around the mean — the "paced, deliberate" shape §3.1 says the
  group's character wants); every other tactic keeps the declared exponential.
  Cells: all-central × MTD ∈ {off, random @ 200, random @ 50} and
  stealth-anchor-hi (4.0) × random @ 200 — the interrupt-pressure gradient the
  leak prediction needs — × 5 profiles × 10 seeds = **200 movement runs**.
  Pre-registered mechanism check: the design record predicts shape sensitivity
  enters *through the interrupt channel*, so any Erlang-vs-exponential shift
  should grow as the interval shrinks; a shift at interval 50 with none at
  MTD-off is the leak behaving as predicted, a shift at MTD-off falsifies the
  mean-is-load-bearing defence outright.
- **Baseline arm.** Consumes no catalogue value, so it runs once per MTD
  condition: {off, 50, 100, 200, 400, 800} × 10 seeds = **60 runs**, shared
  across all sweeps.
- **Boundary refinement (conditional, pre-declared).** If a first-pass verdict is
  "inverts", one cell each side of the boundary at the same seeds before the
  verdict is written. Refinement cells are labelled as such in the output.

Total ≈ 1 500 movement runs + 60 baseline runs. If measured wall-cost forces the
grid down, the reduction is recorded in §6 with what was dropped — no silent caps.

## 5. Fixed factors and their reasons

- **Controller mapping: `v2_partial`, named.** The go-forward mapping (S4): seven
  dwell-only tactics whose *only* cost is the timing draw — the mapping under
  which the timing regime actually binds — and the version experiment 2 declares.
  `v1_ckc_total` is immutable, consumed, and mediates every tactic through a verb,
  which mutes exactly the dwell-only places this study exists to price. The
  sibling S1 sweep should name the same version (their shared-reporting contract).
- **Outcome overlay: the registry default at run time, named in §6.** The
  overlay values are the S1 sibling's parameter, not this study's; whichever
  version is canonical when the sweep executes is recorded verbatim in the
  results, and if S1's distance fold-in ratifies a new version between this
  pre-registration and the run, the run uses that and says so.
- **Determinism (SIM-05).** Every cell is a pure function of (config, seed); the
  runner writes the full config beside the per-run rows; re-running any cell
  reproduces it bit-for-bit.
- **Analysis-only.** No catalogue value, band, weight, mapping or golden changes
  in this study. The runner lives at `data/results/rate_feasibility_study/`
  (script tracked, `numbers/` untracked, per the experiment-1 convention).

---

## 6. What ran

> **Which timing regime these numbers test (read this first).** The sweep below
> ran against the **first** S3 build — the hybrid regime, in which a place visit
> costs the movement layer's exponential dwell *plus* the dispatched verb's native
> substrate cost. Marc reversed that ruling on the same day (**S3-R**, recorded in
> the design record's banner): the movement layer now supplies *every* unit of the
> attacker's time and the substrate's own action pricing is no longer consumed on
> the movement arm. §7's verdicts are therefore verdicts about the hybrid regime,
> and §10 records the re-run against S3-R.

**1 728 runs, 1 548 from the pre-registered grid plus 180 refinement runs.** No
grid reduction was needed — a movement run costs ~0.2 s wall, so §4's grid took
5.1 min on six workers. §1–§5 above are unedited from the pre-registration commit
(`e84bd2a`); this section and those below were appended after the sweep.

**One correction to §5, recorded here rather than edited in.** §5 said the runner
script would be tracked with `numbers/` untracked. That misread the convention:
`data/results/` is untracked **in its entirety** by design — the reproducible
runner lives with its outputs, and a finished result is *promoted* into `docs/`
if it needs tracking (`.gitignore`, experiment-workspace rationale). This record
is that promotion. The pre-registered text is left verbatim rather than silently
corrected, because a pre-registration that gets tidied after the fact is not one.

Two run-time facts §5 required the run to name:

- **Controller mapping `v2_partial`**, as pre-registered.
- **Outcome overlay `v2_lifecycle_distance`.** §5 pre-declared this contingency
  exactly: S1's distance fold-in landed between the pre-registration and the run
  (`293f742`), so the sweep pairs the go-forward weights with the go-forward
  mapping — the configuration experiment 2 will consume. The registry's *default*
  remains experiment 1's version, for reproducibility of that arm.

**The refinement cells, and why they exist.** The first pass showed MTD
suppressing the baseline attacker's objective at **every** tested interval up to
800 s (ASR 0.8 with MTD off, 0.0 at 800 s and below), which is a boundary sitting
at or beyond the grid's edge rather than inside it. §4's pre-declared rule — one
cell each side of any boundary the first pass reveals — was applied on the
interval axis: intervals 1 600, 3 200 and 6 400 s, both arms, same ten seeds
(180 runs). Nothing else was added, and no cell was dropped.

**One condition changed underneath the comparison, and it must be stated.**
Experiment 1 reported the baseline arm reaching the objective in 10/10 runs under
random MTD at 200 s. On today's substrate it reaches it in **0/10**. The
difference is not this study's doing: the seven-defect repair (`dd8c5ec`) and the
deliberate re-baseline that followed it (`06ed8d9`, recorded there as MTD
techniques now discriminating instead of every run ending at the termination
ratio) both landed after experiment 1's numbers were taken. Every verdict below
is therefore a verdict about the **current** substrate, and experiment 1's
published magnitudes are stale as a comparison target — a finding for the
experiment-2 handoff to absorb, not a defect in either result.

## 7. The verdicts

Applying §2's vocabulary, unmodified.

### C1 — profiled attacker slower than baseline: **stable across the band**

Across all 130 movement cells, the profiled attacker's mean elapsed
time-to-first-compromise **never once** falls below the baseline's, at any anchor
setting, any mutation interval, or either distribution family. The direction is
CI-separated in 107 of 130 cells; 14 cells have no compromising run at all (the
attacker never gets far enough to have a time), and the remaining 9 are
same-direction but not separated. At the central cell with MTD off the profiled
arm takes 1 500–7 200 s against the baseline's 303 s, depending on profile. The
conclusion holds across the declared bands with room to spare.

### C2 — MTD does not help the attacker: **stable across the band**

Across 85 matched MTD-on/MTD-off comparisons, there is **no cell** in which the
attacker compromises more hosts with MTD on than off with CI separation; in 72
the suppression is CI-separated in the expected direction. The effect is large
and monotone in interval, on both arms. This is the study's most robust result.

### C3a — per-profile ordering: **indeterminate at this sample size**

Zero inversions were found — but the criterion is not met from the other side.
At the central MTD-off cell only **2 of 10** profile pairs are CI-separated, and
at the central MTD-on cell **none** are. With so few pairs separated at the
reference cell, "no inversion" carries almost no information: the study is
underpowered to speak to profile ordering, and §2 requires that be reported as
indeterminate rather than rounded up to stable. This independently reproduces the
sibling S1 sweep's finding on the same conclusion, by a different route
(timing arbitrariness rather than weight arbitrariness), and the consequence is
the same: **the evaluation may not claim a per-profile ordering until it is
powered.** Ten seeds is the binding constraint, not the parameter bands.

### C3b — failure-mode identity is the profile's: **stable for four profiles, indeterminate for one**

`pure_impediment`, `double_extortion`, `infrastructure_setup` and `aggregate`
hold their modal terminal mode in every swept cell without exception.
`pure_steal` flips between `horizon` and `sink` in 12 cells — but inspection of
the counts shows why, and it is not a parameter effect: its central cells split
7–3 and 5–5 across the ten seeds, so the *mode* is a coin-toss summary of a
genuinely bimodal distribution, and it flips on seed noise rather than on where
an anchor sits. Recorded as indeterminate for that profile, with the mechanism
named: a modal statistic over ten runs is the wrong instrument for a profile
whose runs are near-evenly split, and the fix is power or a distributional
statistic, not a timing change.

The consequence for the APT-model criterion is mild but real: axis 2's
DEMONSTRATED badge rests partly on failure mode being profile-determined, and
that survives for four of five profiles under timing arbitrariness while the
fifth is unresolvable at this sample size. The badge does not fall; its evidence
is qualified.

### C4 — ASR ordering: **stable where measurable, degenerate elsewhere**

The profiled attacker's ASR is **0.00 in all 130 cells** — no corner of the
declared bands, and no mutation interval, lets it reach the substrate objective.
With MTD off the baseline reaches 0.80 and the comparison is CI-separated in the
expected direction. With MTD on at any interval up to 800 s the baseline is also
0.00, so the two arms **tie at the floor** and 85 cells are not CI-separated —
not because the ordering is in doubt but because the metric has no room to move.
ASR is not a discriminating metric on this substrate under MTD, which is the E1
finding restated and is why the study's other conclusions lean on host breadth
and elapsed time.

### C5 — the regime boundary: **found, and it is on the interval axis, not in the anchor bands**

The handoff required any Anderson-style degenerate boundary inside the declared
bands to be named. **No anchor band contains one**: moving any anchor to either
end leaves every conclusion's direction intact. The boundary is on the *other*
axis, and the refinement cells locate it:

| MTD interval (s) | Baseline ASR | Baseline hosts | Movement hosts (aggregate) | Runs compromising |
|---|---|---|---|---|
| 50 | 0/10 | 7.7 ± 2.6 | 0.2 ± 0.3 | 2/10 |
| 100 | 0/10 | 11.5 ± 2.9 | 0.1 ± 0.2 | 1/10 |
| 200 | 0/10 | 13.1 ± 3.3 | 0.9 ± 0.6 | 6/10 |
| 400 | 0/10 | 25.4 ± 4.1 | 1.5 ± 0.4 | 10/10 |
| 800 | 0/10 | 27.7 ± 4.2 | 2.4 ± 1.0 | 10/10 |
| 1 600 | 3/10 | 34.6 ± 4.3 | 5.7 ± 1.0 | 10/10 |
| 3 200 | 5/10 | 35.0 ± 4.4 | 5.6 ± 0.9 | 10/10 |
| 6 400 | 5/10 | 38.0 ± 2.3 | 5.2 ± 1.0 | 10/10 |
| off | 8/10 | 39.2 ± 2.6 | 4.7 ± 0.8 | 10/10 |

Anderson's degenerate case is real here and the evaluation sits inside it: at the
conventional 200 s interval **neither** attacker can complete the objective, and
the objective only becomes reachable again above roughly 1 600 s — eight times
the interval every published run of this project has used. The consequence is
sharp and belongs in the evaluation's design, not in a caveat: **ASR cannot
discriminate anything at the operating interval, because the operating interval
is inside the degenerate region.** Host breadth and elapsed time remain
informative throughout, and the movement arm's breadth is still responding at
6 400 s where the baseline's has saturated.

A second, subtler feature: the movement arm's breadth is *non-monotone* at the
short end (0.2 at 50 s, 0.1 at 100 s, 0.9 at 200 s). At intervals that short the
attacker is interrupted more often than it completes anything — 130 interrupts
per run against ~4 at 800 s — so the ordering between adjacent short intervals is
noise on a floor, not structure.

### Sweep C — the distribution family at fixed mean: **the mean is load-bearing; §3.2(3)'s defence survives**

Erlang-4 firing for the five low-and-slow tactics (same mean, coefficient of
variation halved) changes nothing measurable. Pooled paired differences over all
50 (profile, seed) pairs, Erlang minus exponential:

| Condition | Hosts | Interrupts | Events |
|---|---|---|---|
| MTD off | 0.0 ± 0.1 | 0.0 ± 0.0 | −0.5 ± 3.4 |
| MTD @ 200 s | −0.1 ± 0.3 | 2.8 ± 2.8 | 3.9 ± 12.7 |
| MTD @ 50 s | −0.0 ± 0.1 | 1.2 ± 6.4 | −13.5 ± 15.3 |
| stealth anchor ×4, MTD @ 200 s | 0.0 ± 0.1 | 0.1 ± 2.5 | — |

Every interval contains zero. ASR is 0.00 under both families in every cell. The
one cell the per-cell analysis flagged as separated — aggregate profile, MTD 200,
elapsed time — rests on **n = 2** compromising runs and is a small-sample
artefact, not evidence; it is reported here so the flag is not silently dropped.

**The pre-registered mechanism check comes back weakly positive and honestly
bounded.** §4 predicted that if shape matters it enters through the interrupt
channel, so any Erlang-vs-exponential difference should grow as the interval
shrinks. The interrupt-count difference is indeed largest at 200 s (2.8, CI just
touching zero) and absent at MTD-off (0.0 ± 0.0) — the predicted direction — but
it never separates from zero, and it does not propagate to any outcome. So: the
leak the design record identified is visible in the mechanism and inert in the
result. The mean is the load-bearing quantity here, as §3.2(3) argued, and the
qualification is that this was tested where compromise events are scarce; a
future run at an interval above the degenerate boundary would test it with more
signal.

## 8. What this feeds back

**To the timing design record §3 — confirmed, with one qualification.** The
declared exponential regime survives its own test: no conclusion changes
direction anywhere in the declared bands, and the same-mean shape substitution is
inert on every outcome. §3.2(3)'s "the mean is load-bearing" defence stands, and
§3.1's worry about the exponential being a poor shape for the low-and-slow group
is now answered empirically — it is a poor *descriptive* shape and an immaterial
*operational* one, at least in the regime tested. The qualification to carry: the
shape check ran mostly inside the degenerate region, so it is a weaker test than
it looks, and §3's honest framing should say so rather than claim the shape
question closed.

**To the operational-validation note — the sensitivity instalment is delivered,
and it is favourable.** The note's revisit condition ("if the sweep shows the
conclusion is *not* robust, operational validation has failed for this model")
does not fire. What does need adding is the narrower true result: robustness
holds for the conclusions the study is powered for (C1, C2), and the conclusions
it is not powered for (C3a, and C3b for one profile) are power failures rather
than parameter failures — the same verdict the weight study reached
independently, which makes the two studies mutually corroborating on the point.

**The one anchor that matters, named.** Of the four group anchors, only
**stealth-low-and-slow** moves any outcome at all: pooled across profiles, host
breadth runs 5.28 ± 0.78 at ×0.25 down to 1.54 ± 0.31 at ×4 with MTD off
(3.56 ± 0.53 central), both ends CI-separated from centre. The scan, exploit and
objective anchors move breadth by less than their confidence intervals at both
band ends, in both MTD conditions. This is a useful identifiability result: the
sweep says the model's timing sensitivity is concentrated in the one anchor the
catalogue already badges Tier 3 with its widest band and its most honest
justification, and the two Tier-1 substrate-priced anchors are inert — exactly
the pattern the tier badges predict, arrived at independently.

**The reportable form, per the handoff's step 5.** Every headline number from
the timed regime is now reportable as *"X, stable across the declared band"* for
C1 and C2; as *"indeterminate at ten seeds"* for the profile ordering; and with
the standing qualification that **the evaluation's operating interval sits inside
a degenerate region where ASR cannot discriminate** — the most consequential
sentence this study produces, and the one experiment 2's design must answer.

**Nothing was tuned.** No declared value, band, weight, mapping or golden changed
in this study, and no cell was chosen or discarded after seeing its result.

## 9. Evidence

- Pre-registration: this file §1–§5, commit `e84bd2a`, before any sweep output.
- Runner: `data/results/rate_feasibility_study/run_study.py`; analysis:
  `analyse.py`; outputs under `numbers/` (untracked): `per_run.csv`
  (1 728 rows), `config.json`, `verdicts.json`, `run.log`, `refinement.log`.
- Substrate condition: mapping `v2_partial`, overlay `v2_lifecycle_distance`,
  horizon 15 000 s, geometry 50/5/8/4, seeds (0–7, 42, 1234), MTD scheme
  `random`.
