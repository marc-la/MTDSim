---
status: open
created: 2026-07-28
---

# Run the rate feasibility study — sweep the declared per-tactic means over their published bands, and establish whether any reported conclusion survives the arbitrariness of the timing numbers

**Chain position: after the timing build (S3), alongside the weight sensitivity
study (S1).** It needs the exponential regime live to sweep anything. It is the
*analysis* half of the timing work: the design record rules how time is drawn, and
this study establishes what that choice is worth.

## State of play

**The regime widened after this brief was written (S3-R, 2026-07-28) — the sweep
now moves more than it used to.** When this was drafted, a tactic's declared time
was an *additional* behavioural dwell sitting on top of each action's native
substrate cost. Marc has since ruled that the movement layer supplies **all** of the
attacker's time: the tactic's draw *is* the dispatched action's duration, the
substrate's `ATTACK_DURATION` / `exploit_time` are no longer consumed on that arm,
and a blocked attempt costs its tactic's time rather than nothing. Three
consequences for the design of this study, none of which change its question:

1. **The swept parameter is now the only attacker-side timing there is**, so a
   band that moves a conclusion moves it without a fixed substrate cost damping the
   effect. Expect larger sensitivity than the brief anticipated — and note that
   "larger" is not "worse": it makes a surviving conclusion a stronger result and a
   fragile one easier to detect.
2. **The ratio contest is cleaner.** §"punchline" below frames the thesis as tactic
   dwell against MTD mutation interval; that ratio is no longer diluted by a
   third, un-swept timing source.
3. **Blocked attempts are now priced by the same parameter**, so in blocked-heavy
   profiles the sweep moves the cost of churn as well as the cost of progress. Worth
   reporting separately, since those are different mechanisms reaching the same
   metric.

**Why this exists.** The timing design record
([`../implementation/pipeline/ogasp/stochastic_timing_design.md`](../implementation/pipeline/ogasp/stochastic_timing_design.md)
§3) settles the *regime* — each tactic's declared duration becomes the mean of an
exponential draw — and grounds the choice in the literature. What it deliberately
does **not** do is claim the regime is safe: whether any conclusion the evaluation
reports actually survives the declared numbers is an empirical question, and a
design record that answered it would be asserting the thing the study exists to
test. Marc's framing is the operative one: the tactic timings are **inherently
arbitrary — a per-tactic duration is not a measurable property of the world** — and
the GSPN is a tractable formalism laid over that arbitrariness. This study is what
converts that from a concession into a defended position.

**The literature says the sweep *is* the field's substitute for calibration.** The
extraction survey behind §3.2 found interval-sweeping to be near-universal across
the analytic, stochastic-net and discrete-event traditions, and found that the
strongest papers name their un-grounded rates as future work rather than defending
them. So this study is the field-normal move, not a remedial one. Two results in
that survey set the stakes: Evans reports attack-success probability spanning ~6
orders of magnitude across a plausible re-randomisation range (§2.5.5), and Anderson
gives the degenerate boundary outright — "the attack can never succeed if the churn
rate is faster than the completion rate" (§III). **A sweep that is too narrow will
miss a regime change; the bands must be wide enough to find the boundary if one is
inside them.**

**The parameters already carry their own bands.** The catalogue
(`data/ogasp/tactic_durations.json`) publishes a `sweep_range` per tactic in units
of its group anchor, plus a tier badge and a written justification. Those are the
declared bands — the study sweeps *them*, it does not invent new ones. The four
group anchors (scan-shaped, exploit-shaped, stealth-low-and-slow,
objective-execution) are the identifiable free parameters; sweeping fifteen
independent dwells would be both intractable and a violation of anti-circularity
rule 2.

**What makes this tractable rather than a combinatorial explosion.** The thesis's
punchline is a *ratio* contest — tactic dwell against MTD mutation interval — so the
informative axis is that ratio, not the absolute values. A well-chosen sweep varies
the group anchors against the mutation interval and asks whether the *ordering* of
outcomes is stable, which is a far smaller space than a full grid over fifteen
tactics.

## Recommended approach

1. **Fix the question before running anything.** The claim under test is not "are
   the numbers right" — they are declared, and cannot be right. It is **"does any
   reported conclusion change its direction when each anchor moves across its
   published band?"** State the conclusions in scope explicitly (per-profile
   ordering; the MTD-on vs MTD-off direction; any profile-vs-baseline ranking) and
   pre-register the acceptance criterion *before* looking at results — the
   pre-registration ordering the validity framework already demands.
2. **Sweep the four group anchors, not the fifteen tactics.** Each anchor moves
   across its declared band; per-tactic multipliers ride along unchanged, which
   preserves the relative structure the profiles argue for. Report the sweep in
   units of the anchor so the result reads as shape, not scale.
3. **Put the mutation interval on the other axis.** The ratio is the contest; a
   sweep of dwell alone cannot show where the regime changes. Include at least one
   cell each side of any boundary the first pass reveals.
4. **Test the distribution family, not just its mean — this is the study's second
   half and the one §3 most wants answered.** Re-run the informative cells with a
   **same-mean** heavier-shouldered family (Erlang-*k* / gamma) for the low-and-slow
   anchors. The design record's defence leans on the claim that the *mean* is the
   load-bearing quantity and the shape is largely inert for a mean-based metric
   (Madan's result); this study is what checks whether that holds *here*. If the
   answer changes with the shape, that is a finding that revises §3, and it is
   better found now than by an examiner.
5. **Report bands, never point values.** Every headline number from the timed regime
   should be reportable as "X, stable across the declared band" or "X, but the
   ordering inverts below *y*" — the second being a more valuable result than the
   first.

*Alternatives considered:* calibrating the anchors against breach-report macro
timing instead of sweeping — rejected as the *primary* move, because it is the
separate calibration step the validity framework already sequences post-MVP, and
because calibration without a sensitivity result still leaves "does the conclusion
depend on it?" unanswered. Sweeping all fifteen tactics independently — rejected:
intractable, and it dissolves the group-anchor structure that keeps the parameter
count identifiable.

## Validation gate

Done when a record exists that:

1. States the conclusions under test and the acceptance criterion, pre-registered.
2. Reports the anchor × mutation-interval sweep, with the bands taken from the
   catalogue rather than invented.
3. Answers, for each conclusion in scope: stable across the band / inverts at a
   named boundary / indeterminate at this sample size.
4. Reports the same-mean shape comparison for the low-and-slow anchors, and states
   whether §3's mean-is-load-bearing defence survives it.
5. Names any regime boundary found inside the declared bands (the Anderson-style
   degenerate case), because a boundary inside the band is a threat to every number
   reported without it.
6. Feeds its verdict back into the timing design record §3 and the
   operational-validation note — either confirming the declared regime or forcing
   its re-argument.

## Hard constraints

- **Analysis only — this study changes no declared value.** Recalibrating the
  anchors is separate work; if the sweep shows calibration is needed, that is a
  finding to report, not a change to make here.
- **The bands are the catalogue's**, not the study's. Widening a band is a
  documented decision with a reason, never a convenience.
- **Do not tune anything to make a conclusion survive.** The anti-circularity rules
  hold: if the conclusion is not robust, the negative result is the deliverable, and
  the evaluation-burden note already commits to reporting it as such.
- Determinism (SIM-05) — a sweep is many seeded runs, and each cell must be
  reproducible. Attacker-only (D5); the action-set freeze (S2); Australian English;
  branch hygiene; never push without an explicit ask.

## Reading list

- [`../implementation/pipeline/ogasp/stochastic_timing_design.md`](../implementation/pipeline/ogasp/stochastic_timing_design.md)
  §3 — the regime being tested, its literature grounding, and the mean-is-
  load-bearing defence this study checks.
- `data/ogasp/tactic_durations.json` — the anchors, the per-tactic multipliers, and
  the declared `sweep_range` bands that *are* this study's parameter space.
- [`../notes/ch3_design/operational_validation.md`](../notes/ch3_design/operational_validation.md)
  — the tier badges and the four anti-circularity rules the sweep operates under.
- [`../notes/ch2_background/tactic_duration_precedent_survey.md`](../notes/ch2_background/tactic_duration_precedent_survey.md)
  — the declare-and-sweep precedent, and the macro-timing table if calibration is
  ever taken up.
- [`../handoffs/2026-07-27_tactic_weight_sensitivity_study.md`](./2026-07-27_tactic_weight_sensitivity_study.md)
  — the sibling S1 sweep over transition weights; the two studies share a method and
  should share a reporting shape, and ideally run against the same mapping version.

## Out of scope (explicitly)

- Recalibrating the per-tactic values against breach-report milestones — the
  separate, post-MVP calibration step.
- Changing the distribution family in the build. This study *tests* whether the
  family matters; adopting a different one is a design change back through the
  design record.
- The transition-weight sweep (S1) — its own handoff, though the two should be read
  together when both land.
- Any change to the baseline arm or to the MTD scheduler's own timing.
