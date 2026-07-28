---
status: pre-registered — results pending
created: 2026-07-28
updated: 2026-07-28
topic: "The rate feasibility study (S3, analysis half) — pre-registered sweep of the four group anchors over their catalogue-derived bands against the MTD mutation interval, plus the same-mean Erlang-k shape check on the low-and-slow group. The conclusions under test and their acceptance criteria are committed here BEFORE any sweep output exists; git history is the witness to that ordering."
---

# The rate feasibility study — does any reported conclusion survive the arbitrariness of the timing numbers?

**Status: pre-registration.** This commit contains the study's question, the
conclusions in scope, the acceptance criteria, the parameter space and the grid —
and deliberately **no results**. The results land in a later commit that appends
§6–§8 without editing §1–§5; the commit ordering in `git log` is the
pre-registration evidence the validity framework demands
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

*Sections 6–8 (results, verdicts, feed-back into the design record §3 and the
operational-validation note) are deliberately absent from this commit. They are
appended by the run session without editing §1–§5; any grid deviation forced by
wall-clock cost or by the boundary-refinement rule is recorded there.*
