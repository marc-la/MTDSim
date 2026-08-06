---
status: durable
created: 2026-07-29
topic: "Pre-registration for the axis-1/3/4 demonstration run (experiment 2, folded): the three badge criteria in the criterion's own vocabulary, the claims the run is NOT powered for, the mutation-interval choice with its justification, the declared inputs at the experiment seam, and the analysis plan — committed before any output exists."
updated: 2026-07-29
---

# Pre-registration — the axis-1, axis-3 and axis-4 demonstration run

> **Retired class labels.** This record is investigation history and is left as
> written: it reports the pre-2026-08-06 labels `pure_steal` / `pure_impediment` /
> `double_extortion` / `infrastructure_setup`, which the objective-tactic rename
> replaced with `objective_exfiltration` / `objective_impact` /
> `objective_exfiltration_impact` / `objective_none_c2`. Rewriting them would
> re-attribute evidence to labels that did not exist when it was taken. Crosswalk:
> [`gasp_schema.md`](../gasp/gasp_schema.md) §(c).

> **NOT EXECUTED (2026-07-29).** A parallel session ran the same handoff from the
> same commit and shipped the result on `feat/exp02-ashen-lynx`; this run was
> stopped as a duplicate at 207 of 6 900 rows on Marc's ruling. The document is
> **retained unedited** because its value is now as an independent yardstick: it was
> written without sight of the other derivation, and
> [`demonstration_arms_cross_examination.md`](demonstration_arms_cross_examination.md)
> uses §5's criteria to cross-examine the shipped result. Editing it after the fact
> would destroy exactly the property that makes it useful. One defect in §5 A1.1 —
> the missing tempo guard — is recorded in the cross-examination §5 rather than
> fixed here.

**Status:** durable, and **committed before the first result file exists**. This project
has run two pre-registered studies (the S1 weight sweep, the rate feasibility study) and
the discipline paid off both times — in each, a conclusion moved that a post-hoc analysis
would have been tempted to keep. Nothing below may be edited after the run: a criterion
that turns out to be the wrong criterion is recorded as such and the badge does not move.

Three axes sit at **DESIGNED** — the mechanism exists but has not been shown to change an
outcome ([`../../apt_model_criterion.md`](../../apt_model_criterion.md) §(b)). This run
decides all three, and the honest prior is that **at least one will not move**. Axes 6 and
7 both landed at DESIGNED on exactly this discipline nine days ago, each shown to operate
without conferring adversarial advantage. A measured negative is a stronger statement
about the field's gap than silence, and it is one only a model carrying the capability can
make.

## 1. The declared inputs, named at the seam

An experiment names its own inputs rather than inheriting them; every registry in this
pipeline defaults to experiment 1's value for that reason.

| input | value | why |
|---|---|---|
| controller mapping | `v2_partial` | experiment 2's mapping; the registry default is still experiment 1's `v1_ckc_total` |
| outcome overlay (conditioned arm) | **`v3_persistent_backward`** | the go-forward version per Marc's persistence ruling. **Not** `v2_lifecycle_distance`: the experiment-2 handoff and the chain README both name the older version because they predate the ruling ([`weight_sensitivity_study.md`](weight_sensitivity_study.md) §3b) |
| outcome overlay (ablation arm) | `verdict_blind` (in memory) | §4 |
| sink retrace (S5) | **on** | [`sink_retrace_design.md`](sink_retrace_design.md); off by default, named here |
| horizon | 15 000 s | experiment 1's, unchanged, so the horizon is not a moving part |
| synthetic overlay | on | the D8 arm every published run uses |

## 2. The mutation interval — chosen, not inherited

The rate feasibility study located a degenerate region: at the 200 s interval **every**
published run of this project has used, neither attacker completes the objective, and the
objective only becomes reachable above roughly 1 600 s (§7, C5). Inside it, any
success-rate-shaped measurement is pinned at zero and discriminates nothing.

Running at 200 s alone reports the region rather than the attacker. Running above the
boundary alone abandons the interval every prior result is stated at, so nothing new could
be compared with anything old. **Both are carried, as a declared tempo dimension**, because
the boundary is itself a result worth showing:

- **200 s** — the operating interval. Breadth-, event- and time-shaped measures stay
  informative here and the whole measurement suite was built to be. ASR is not reported at
  all at this tempo.
- **3 200 s** — outside the region. 1 600 s is the boundary itself (baseline ASR 3/10 and
  still climbing), so it would report the boundary rather than the regime beyond it; at
  3 200 s the baseline sits at 5/10 with breadth plateaued (35.0 ± 4.4 against 34.6 ± 4.3
  at 1 600 s). ASR-shaped evidence may be offered **only** from these cells, and must say
  so.

## 3. The grid

| dimension | levels | n |
|---|---|--:|
| profile | `pure_steal`, `pure_impediment`, `double_extortion`, `infrastructure_setup`, `aggregate` | 5 |
| attacker arm | verdict-conditioned, verdict-blind | 2 |
| defence condition | no-MTD; 8 single mechanisms; 3 schemes (`simultaneous`, `alternative`, `random`) — every MTD-bearing condition at both tempos | 1 + 11×2 = 23 |
| seed | 0–29, identical across every cell | 30 |

**6 900 movement runs**, plus the baseline arm re-measured in the same run across the same
23 defence conditions × 30 seeds (690 runs). Experiment 1's published baseline magnitudes
are stale — the substrate was re-baselined (`dd8c5ec`, `06ed8d9`) and the timing regime
became S3-R after they were taken — so they are not a valid comparison target and the
baseline is re-measured rather than quoted.

**Two things about the defence dimension that must travel with any reading of it.**

1. **The inherited pool is four mechanisms, not eight.** `MTDScheme` carries
   `HostTopologyShuffle`, `PortShuffle`, `OSDiversityAssignment` and `UserShuffle`
   commented out of its default strategy list, so the scheme arms exercise only
   `CompleteTopologyShuffle`, `IPShuffle`, `OSDiversity` and `ServiceDiversity`. The
   single-mechanism arms name all eight explicitly, which is a configuration choice and
   not a substrate edit. Any statement of the form "eight mechanisms under four schemes"
   is false of the scheme arms and true only of the single arms.
2. **Tay's `mtd_ai` selection is excluded, and the reason is recorded rather than
   silently dropped.** It raises `TypeError: _register_mtd_ai() missing 1 required
   positional argument: 'mtd_technique'` in this wiring — the scheme expects the RL agent
   to supply the technique, and that agent is deferred to the evaluation/ablation phase by
   standing scope. This is an inherited integration gap, not a finding about MTD, and
   fixing it is out of scope for this run.

## 4. The verdict-blind arm

The composition rule is `w' ∝ base · overlay_v`, renormalised, and `compose` treats an
**absent** pair as a passthrough at factor 1.0. An overlay carrying no values therefore
reduces composition to the renormalised base weights at every place under every verdict:
the token still walks the net, still dispatches verbs and still reads verdicts, and the
verdicts simply have no consequence for where it goes next. That is "the adaptive loop
off", and it is the control the axis-4 claim has always lacked — every run on record has
had the loop switched on, so nothing separates *the loop operates* (evidenced) from *the
loop helps* (not evidenced).

Built as an **empty value table, not a driver branch**, so both arms run the same code
down the same path and differ only in the data they read; a code-path ablation would make
the contrast two-factor. Test-pinned as a genuine null at every place of every profile net
under every verdict, and end to end against a run driven by an independently-constructed
no-overlay object (`tests/l3_simulation/test_verdict_blind_arm.py`). It stays an in-memory
arm and is **not** registered in `overlays/manifest.json` until a published run consumes
it, per the registry's own immutability rule.

Everything else is held identical between the arms: same seeds, same mapping version, same
timing regime, same geometry, same retrace policy.

## 5. The badge criteria

Reporting convention throughout: the suite's `mean_ci` (mean ± 1.96·SEM) and
`interval_report`; `ordering_supported` is the gate for any ordering claim, never sorted
means. Arm and condition contrasts are **paired per seed** — the same seed differing in
one factor — which is both better powered and more honest than two independent intervals.

### Axis 4 — adaptivity. Amended from the handoff, deliberately.

The handoff's wording was that the arms must "differ". **Amendment: the difference must be
in the direction of more progression for the verdict-conditioned arm.** Left as "differs",
a large *negative* effect would promote the badge — an attacker whose adaptive loop
reliably makes it worse would score as adaptive. That is the reverse-fitting the criterion
exists to prevent, and the amendment is recorded here rather than applied quietly.

- **Primary measure (single, pre-specified): distinct hosts compromised.**
- **Why not `deepest_successful_stage`**, the adopted axis-1 progression measure: under
  `v2_partial` the objective band is dwell-only, so a stage-3 place can hold no verdict and
  the measure's ceiling drops to 2 — and a check across all five profiles finds every run
  first succeeding at stage 0 and reaching stage 2, so it is saturated on this mapping and
  cannot discriminate anything. Recorded now, before the run, so it cannot look like a
  measure swapped out after seeing a row.
- **Secondary, reported but never badge-deciding:** `distinct_place_count`,
  `successes_per_distinct_host`, `blocked_fraction`, `failure_routing_rate`.
- **Statistic:** paired per-seed difference (conditioned − blind) within a cell; 95 % CI
  excluding zero counts as separated.
- **DEMONSTRATED iff** the primary measure's paired difference is **positive and
  CI-separated** in **≥ 2 profiles** and **≥ 2 defence conditions**.
- **Otherwise DESIGNED**, and the reportable finding is that the loop reacts and does not
  adapt usefully.

### Axis 3 — strategic plurality. Two necessary conditions.

- **(a) Traversal diversity is non-degenerate**, per profile: `path_entropy` mean with a
  95 % CI **lower bound above zero**, and `distinct_prefixes` at k = 3 **greater than one**
  across the 30 seeds.
- **(b) An interaction, not a single main effect.** Pre-specified outcome measure: distinct
  hosts compromised. The criterion is a **crossover**: there exist two defence conditions
  *i, j* and two profiles *P, Q* such that the paired difference (*i* − *j*) is
  CI-separated **positive in P and negative in Q**. A ranking that merely differs in
  magnitude between profiles is a main effect plus noise; a sign reversal is an
  interaction, and it is the only form of (b) this run is powered to claim (§6).
- **DEMONSTRATED iff both.** If (a) holds and (b) fails, attacker-side variety and
  defender-side plurality are reported separately, the badge stays DESIGNED, and the
  write-up states plainly that a defence ranking identical for every profile evidences
  defender plurality only.
- The honest limit travels into whatever is claimed either way: the branching is drawn from
  static flow proportions, not chosen by a decision rule — **variety, not strategy**.

### Axis 1 — persistence. The criterion most in need of a guard against a soft pass.

The obvious reading — "deepest successfully-actioned stage ≥ 2 in a non-trivial fraction of
runs" — is **already satisfied** and must be rejected. Under `v2_partial` the measure's
ceiling *is* 2 (the objective band is dwell-only), four profiles sit at 2.0 ± 0.0, and a
check across all five finds every run advancing 0 → 2. Scoring persistence captured on a
truncated ceiling is precisely the reverse-fitting the badge is held to avoid.

What holds the badge is not shallowness but **repetition**: 0/100 objective reaches, and
effort that does not convert to breadth — hundreds of successful actions landing on the
same couple of hosts. Persistence in outcome terms therefore means *the campaign holds and
regains ground under a moving target*. Three necessary conditions:

- **A1.1 — re-establishment after severance.** `refoothold_rate` (time from each
  position-severing network-layer interrupt to the attacker's next host compromise,
  censored at run end) has a 95 % CI **lower bound above 0.5** in ≥ 2 profiles, in at least
  one MTD condition. The threshold is 0.5 because that is where the measure's *meaning*
  turns — the attacker re-establishes more often than not — and not because of any observed
  value.
- **A1.2 — breadth beyond a single foothold.** Distinct hosts compromised has a 95 % CI
  **lower bound above 1** in the same ≥ 2 profiles, in at least one MTD condition.
- **A1.3 — the guard against the retrace confound.** At least one of the qualifying
  profiles must be **`aggregate` or `pure_impediment`** — the two whose nets carry no sink,
  and which are therefore bit-identical with the retrace policy on and off. Without this,
  a badge could move purely because the censoring regime changed under S5 rather than
  because the attacker persisted. This condition is the reason the retrace was built with
  its own internal control.
- **Otherwise DESIGNED**, with "the structure runs and does not convert to progress on this
  substrate" recorded as the finding.

**On the measure's provenance, stated plainly.** `refoothold_rate` and
`refoothold_times` did not exist and were written for this run, alongside
`first_success_stage` / `advanced_after_first_success`. The measurement suite's own
lifecycle anticipates this ("extend when the demonstration-arms handoff pre-registers its
badge criteria"), and the order is the discipline: the measures are committed **before**
any run of this experiment exists. A six-seed smoke check was run to verify the new measure
*discriminates at all* rather than saturating like the stage measures — the same validation
gate `deepest_successful_stage` had to pass — and it spans 0.15–0.91 across profiles. Those
numbers are a discrimination check, not the basis of the 0.5 threshold, which is fixed on
meaning above.

## 6. Claims this run is **not** powered for

Two independent studies have now found that ten seeds cannot separate adjacent profiles
(S1 §5 C3; rate study §7 C3a). Thirty seeds improves this and does not fix it.

- **Not claimed: any ordering of the five profiles** by progress, breadth or depth.
  `interval_report.ordering_supported` will be reported and is expected to be false.
- **Not claimed: a full ranking of MTD mechanisms** against one another. This is why axis
  3's criterion (b) is built on a sign reversal between two conditions rather than on a
  ranking, and why the ~90 % suppression is to be confirmed or withdrawn **per mechanism**
  as a suppression-versus-no-MTD contrast, not as a league table.
- **Not claimed: anything ASR-shaped at 200 s.** Degenerate by construction (§2).
- **Not claimed: any cross-paper magnitude comparison**, and no pooling with experiment 1 —
  the substrate was re-baselined, the timing regime changed, and the retrace changed the
  censoring regime ([`sink_retrace_design.md`](sink_retrace_design.md) §4).
- **Better powered than the priors:** the within-cell paired contrasts (arm vs arm, MTD vs
  no-MTD, mechanism vs mechanism *within* a profile), because the seed is held.

## 7. Analysis plan, fixed in advance

1. Primary measures are the ones named above and are not substituted after the fact. A
   secondary measure that separates where the primary does not is **reported as such** and
   does not move a badge.
2. No measure, weight, mapping, overlay or parameter is adjusted in reaction to a row.
   Parameter adjustment is reviewed work with its own handoff (S6).
3. Censoring is reported, never pooled away: `CensoredDurations.observed` and `.censored`
   separately.
4. Every badge verdict — moved or held — is written with the numbers behind it and a
   pointer to the criterion above, including the ones that do not move.
5. The retrace count per cell is reported, so the §3.4 no-budget argument stays falsifiable.

## 8. What would falsify the run itself

Recorded so a broken run is not read as a negative result: if the two sinkless profiles'
numbers differ between retrace-on and retrace-off, or if `time_residual` returns non-zero
on non-interrupted events (the S3-R regime tripwire), or if the verdict-blind arm's routing
diverges from the base-weight identity, the run is invalid and no badge moves in either
direction.
