---
status: partially shipped
created: 2026-09-30
---

# Disruption metrics from the mechanism: apply Marc's 2026-09-30 rulings to §4.5, rebuild Figure 5.3, fix two analyser defects

**Goal:** replace the compromise rate after an MTD deployment with metrics built on
how a deployment actually disrupts each attacker, and fix the analyser defects found
on the way.

## Shipped 2026-09-30 (this branch)

- **§4.5.3:**
  - attack actions blocked, per run, with what counts as blocked;
  - time lost per MTD deployment, re-defined as the extra time to the next
    compromise, with a worked example in round numbers and the restricted mean
    cited (Royston & Parmar 2013, Methods, Eq. 1, verified from PMC3922847);
  - the compromise rate after an MTD deployment retired;
  - the Intervals paragraph now covers time lost.
- **Tables 4.3 and 5.1:** the metric rows updated.
- **"Condition" retired** dissertation-wide, in favour of **deployment strategy**,
  **no MTD** or **cell**:
  - 19 prose sites;
  - 8 generated tables and their generators, plus the lineage YAML;
  - a registry row, RATIFIED.
  - Ordinary English uses stay.
- **Reader:** `data/results/ch5_defended/time_lost.py` replaces `disruption.py`,
  and the baseline's end is now its last action (defect 1, fixed).
  `ablation.py` uses the reader, and its "no MTD" label is fixed at the generator.
- **Figure 5.3 rebuilt:**
  - (a), (b): deployments followed by a compromise within t, with and without
    the MTD. The area between each pair equals the time lost to within 2 s in
    all 14 cells.
  - (c): time lost per mechanism.
- **New Table 5.3** (`tab:disruption`): blocked per run and time lost per
  mechanism.
- **§5.3.1** rewritten as plain description. **§5.4**'s time-lost sentence is
  updated (324 s against 332 s, a difference of −8 s [−20, 4]).
- **Appendix "Robustness of time lost to its window"** deleted with its table and
  tool.
- **Chapter 6 §6.2:** a comment carries the mechanism narrative for points (1)
  and (2).

## Shipped 2026-09-30, second pass (branch chore/s5-results-asp)

Marc's 2026-09-30 walk-through of §4.5 and §5.1–5.3 ("focus your work on 5.1 to
5.3"; the ablations are out of scope):

- **Ruling H1: MTTC is read at a target host,** Zhang's written definition (p. 16),
  over the runs that take one. §4.5.2, Table 5.2, Table 5.5 and Appendix F follow.
  ASP is its coverage, so the bracketed "share of runs" is gone. The attack-outcome
  preamble now says each of ASP, MTTC and NCR is read in the targeted scenario.
- **ASP reduction is chapter 5's headline,** as §4.5.3 already said: Figures 5.3–5.5,
  Table 5.4, Table 5.5 (Scott–Knott on the per-seed share of runs taking a target;
  Spearman's rho on ASP reductions with a seed-resampled interval), Appendix F.
  NCR reduction stays as a Table 5.5 column (the two disagree: APT under random at
  200 s, ASP 1.00 against NCR 0.75). `analyse.py` keeps `sweep_ncr`.
  - **Resolution:** per profile, ASP rests on 5 to 13 successes in 100 runs, so
    Figures 5.4–5.5 have wide intervals (clipped at −1, marked). The pooled
    headline resolves. Regenerate at 1 000 seeds.
  - **Changed findings:** the APT model hits the ceiling under the host layer (no run
    takes a target up to 500 s); at 500 s the host layer *raises* the baseline's ASP
    (−0.22); user shuffle raises it at 1 000 s (−0.29). The profile-level claims of
    the NCR version (c3 at 500 s; c_agg under the strategies) no longer hold and are cut.
  - `suppression()` now drops bootstrap resamples whose no-MTD cell has no success
    and records their share (`boot_undefined_share`, at most 0.009).
- **§5.2:** Figure 5.1 gains (b) distinct attack paths (the count §4.5.1 defines,
  replacing the stale APV share) and (c) attack confidentiality (the count-in-window
  detector); the over-the-run Figure 5.2 is retired. Attack rate per minute in the
  prose. The owed dwell-only note re-measured: 68–83 % against the baseline's 83 %.
- **Appendix C.4 filled:** the detector's count (3, 5, 10) and window (30, 60,
  120 s), `tab_C-4a_detector_memory`.
- **Not touched:** §5.4 ablations (still NCR), the regime-arm owed note (still NCR,
  flagged in its owed text), chapter 6 placeholders.

## Second read, 2026-09-30 (branch chore/s5-ncr-headline): NCR reduction back as the headline

Marc: the ASP figures were "a colourful mess"; "NCR reduction was chosen because
it's a finer-grain tool"; "in 5.3.2 you could have ASP reduction and NCR reduction".

- **The rule:** ASP is one bit per run. With no MTD the APT model reaches a target
  in 36 of 400 runs pooled, 5 to 13 of 100 per profile, so ASP reduction resolves
  only pooled, and it saturates at 1.00 whenever no run reaches a target. NCR
  reduction records the hosts every run takes. So: **§5.3.2 carries both** (Figure 5.3
  NCR, Figure 5.4 ASP, pooled; Table 5.5 both columns), **§5.3.3 NCR only**. §4.5.3
  says NCR reduction is the headline and why; §5.1 ranks by NCR.
- The NCR prose of §5.3 is restored verbatim (numbers.json `sweep` identical to the
  verified version, 0 of 498 cells differ); ρ now has its interval (−0.03, −0.19 to
  0.05), so that owed note is closed. `sweep_asp` holds the ASP sweep.
- **Attack actions blocked is a percentage of the attacker's actions** (Marc: "divide
  by"): §4.5.3, Figure 5.2(a), Table 5.3, §5.3.1. Host layer 1.5–1.7 % (APT) against
  1.9–2.0 % (baseline); service layer 0.5 % against 1.9–2.0 %. `time_lost.py`
  gains `blocked_share` (own RNG stream; time lost unchanged in every cell).
- **Asked, not applied:** distinct attack paths saturates at the number of runs (the
  count is bounded by it and grows with the seed count); time lost scaled by the
  no-MTD wait.

## Scrutiny round, 2026-09-30 (branch chore/s5-floats-scrutiny)

Nine reviewers on §5.2-5.3 (four cold readers, four context critics, one convention
reader), then three fresh ones on the changed floats. Marc's rulings applied:

- **"MTD mechanism" dissertation-wide** (terminology row 72 overturned): 43 prose
  sites, the §2.2.2 and §5.3.3 headings, the generated tables, Figure 4.1's label.
  Kept: "defence mechanisms such as MTD" (ch3, the concept) and labels.
- **Attack actions blocked per MTD deployment** (§4.5.3, Table 4.3, Figure 5.2(a),
  Table 5.3): interrupts over the deployments that complete while the attacker is
  acting. Host layer 0.35-0.39 (APT) against 1.00; service layer 0.15-0.16 against
  0.95-0.96. `time_lost.py` `blocked_per_deployment`; time lost unchanged.
- **Time lost:** one sentence in §4.5.3 and one in §5.3.1 on why it can fall below
  the penalty or zero (the penalty is paid only by interrupting deployments and is
  small beside a 1 280 s / 430-470 s wait). The cause of the host layer's cost (the
  lost position) has no chapter 4 antecedent, so it is not stated in chapter 5.
- **Figure 5.1:** (b) axis "(of 100 runs)" from the run count, and §4.5.1 says each
  float gives the number of runs; (c) a dot plot on a truncated axis, the baseline
  its dashed line; one key under both titles.
- **Precision rule** (figure_table_conventions.md): a column rounds to its widest
  interval's half-width at one significant figure (two when it is a 1). Table 5.2
  (MTTC to 1 000 s at 100 seeds), Table 5.3 (time lost to 10 s), Table 5.5 MTTC.
- **Table 5.2** natural width with a group row; c_agg kept (Marc: its higher ASP is
  interesting). **Table 5.3** in the figure's order, grouped by layer.
- **Figure 5.4** ticks every 0.5; caption decodes a whiskerless 1. **Figure 5.5** the
  y-axis title on every row.
- **Prose fixes (verified by a numbers auditor, no mismatches):** the §5.3.3 c_agg
  sentence (0.69 was 0.67; outside the range under service diversity) replaced by
  the deployment strategies' split; "not simply reversed" -> "unrelated"; "and more
  slowly" cut in §5.2 (c2 and c3 MTTC overlap the baseline's).
- **Not done, by ruling:** Figures 5.5-5.6 whiskers (revisit at 1 000 seeds); the
  dwell-only confidentiality caveat (stale text, later). **Open:** table captions sit
  on the top rule (class-level caption skip); Table 5.5 geometry at 2.2 pt.

## Still open

- **Ruling I, MTD mechanism for defence mechanism:** still unruled. Marc uses
  "MTD mechanism" in speech, but the registry has *defence mechanism* ratified,
  so the new text uses *defence mechanism*. One sweep once ruled; it is in
  `2026-09-29_ch4_consolidation.md` §I.
- **Time to resume a blocked action:** kept as chapter 5 depth, not a metric
  (recommendation). Not yet used in the prose.
- **Every number in §5.3.1 and Table 5.3 is on the 100-seed corpus.** Regenerate
  at 1 000 seeds with the rest of chapter 5.
- **Defect 3 (the tracer's "ran for all of it")** is not fixed.

## State of play

- **Mechanism record:** [`../implementation/disruption_mechanism.md`](../implementation/disruption_mechanism.md),
  with its dry runs in `data/results/s45_metric_redesign/`.
- **The mechanism in one line:** a deployment blocks only the action in flight, then
  costs the attacker time to get back to its work, and on the service layer it can
  undo the attacker's progress on a host.
- **The narrative per layer:**
  - **host layer:** the attacker loses its position (the host it was working on);
  - **service layer:** the attacker's progress on a host is undone;
  - **user shuffle:** credentials change, so brute force is affected.
  - IP shuffle's own change (the host's address) reaches nothing the attacker
    does. Its whole effect is the interrupt and the lost position.
- **This branch** (`chore/disruption-mechanism`) is built on
  `chore/s45-metrics-round3` (another session's, not yet merged). **Merge that
  one first**, then this one.
- **§4.5 is held by the other session.** Apply the rulings below only once §4.5
  is free.

## Marc's rulings (2026-09-30)

- **Attack actions blocked:** Brown's count, **per run** (Marc: per deployment
  is "too much confusion"). A blocked action is one a deployment cuts off while
  it runs:
  - APT model: outcome `MTD_INTERRUPT`;
  - baseline: `interrupted_in` set;
  - an interrupt on a dwell-only tactic, or on a dispatch that could not run
    anyway, is not an action blocked.
- **Time lost per MTD deployment, re-defined (Marc's):**
  - The time from a deployment's completion to the attacker's next compromised
    host, minus the same from the same moment on the same seed's no-MTD run.
  - Both are capped at the next deployment (at most the interval), so each
    deployment is charged only its own cost.
  - The mean of the capped times is the restricted mean of survival analysis,
    and the difference between two restricted means is a standard contrast.
    **To cite:** Royston & Parmar 2013, *BMC Medical Research Methodology* (open
    access; verify the locator before citing).
  - It records both costs in one number, time and undone progress, and replaces
    the compromise rate after an MTD deployment.
- **Time to resume a blocked action:** reasonable (Marc). Recommended as the
  depth reading behind the APT model's host-layer cost, not as a separate §4.5
  metric, unless Marc wants it. See Open.
- **Blocked dispatches (APT only):** allowed if the comparison is fair and both
  attackers go on one graph. The baseline has none by construction, because its
  procedure re-establishes every precondition. Not recommended as a metric: it is
  the reason for the APT model's resume time, so it belongs in the chapter 5
  prose.
- **Dropped (Marc):**
  - time to regain the host cursor;
  - the baseline-only give-up counter;
  - blocked per deployment.
- **"Condition":** use the thesis's own terms from `tab:deployment-strategies`:
  - **no MTD**, or a **deployment strategy** (single, random, alternative,
    simultaneous, MTDShield) over the seven **MTD mechanisms**;
  - a per-mechanism result is the single strategy with that mechanism.
  - Replace *condition* in §4.5 and chapter 5 with *deployment strategy* (or *MTD
    mechanism* where only single strategies are meant). Marc was unsure between
    this and *MTD defence strategy*. The recommendation is the existing term,
    *deployment strategy*, because it is already defined in chapter 2.

## Dry run: time lost per MTD deployment

`time_to_next_compromise.py`, 100 seeds, 2 000 s interval, $c_1$–$c_4$ pooled. Mean
time to the next compromise in seconds, capped at the next deployment; the interval is
a bootstrap over deployments.

| mechanism | APT: with / no MTD | APT: time lost | baseline: with / no MTD | baseline: time lost |
|---|---|---|---|---|
| IP shuffle | 1593 / 1280 | **313** [286, 339] | 473 / 469 | 3 [−41, 46] |
| complete topology | 1487 / 1281 | **206** [175, 236] | 451 / 450 | 1 [−49, 51] |
| host topology | 1492 / 1279 | **212** [183, 242] | 461 / 454 | 7 [−43, 54] |
| port shuffle | 1294 / 1280 | 14 [−9, 37] | 442 / 446 | −3 [−43, 35] |
| OS diversity | 1273 / 1281 | −8 [−33, 16] | 396 / 432 | −36 [−77, 7] |
| service diversity | 1332 / 1280 | 52 [28, 77] | 959 / 441 | **518** [452, 583] |
| user shuffle | 1251 / 1286 | −35 [−58, −11] | 457 / 446 | 11 [−31, 57] |

This matches the mechanism. The APT model pays on the host layer, where it loses its
position and retraces. The baseline restarts at once, so it pays nothing there, and
pays under service diversity, where its exploit progress is undone.

**Stated limit:** a deployment whose no-MTD run had already ended (target taken) has
no reference and is dropped. That is at most 22 % of deployments (baseline, service
diversity), because the defended baseline runs longer than its no-MTD twin. The
bootstrap should resample runs rather than deployments for the reported interval.

## Figure 5.3, rebuilt (now Figure 5.2: the old Figure 5.2 is retired)

- **Second rebuild, 2026-09-30 (Marc):** "panel A is not grounded in a metric
  that we're using". The share of deployments followed by a compromise within $t$ is
  no Table 4.3 metric, so the curves went. Now **(a) attack actions blocked, per run**
  and **(b) time lost per MTD deployment**, one mechanism axis, both attackers
  (`tools/ch5_disruption_figure.py`). Table 5.3's headers are the metrics' names
  verbatim ("blocked per run ... I don't recognise").
- **No acronyms** for attack actions blocked or time lost (Marc asked "AAB?"): the
  supervisor's 2026-09-22 ruling is no invented acronyms; ASP, NCR and MTTC are the
  field's own. Recommendation given; not re-asked.
- **Scaling time lost by attack rate:** not added. It changes no conclusion (dry
  run: APT IP shuffle 5.1 actions' worth against the baseline's 14.7 under service
  diversity); Marc read the seconds panel as "a good figure".

## Analyser defects to fix (found 2026-09-30)

1. **The baseline's `termination_time` is always the 15 000 s horizon,** even when its
   target fell earlier. `disruption.py` treats it as the end of the run, so
   deployments after the baseline finished count as live time: 59 of 157 IP-shuffle
   deployments in the sample. This biases the current Figure 5.3's baseline curves.
   - **Fix:** use the last action's end.
   - **Audit every other reader of the baseline's `termination_time`**, e.g. any
     "share of runs lasting to the time limit".
2. **`blocked_resume.py` measured resume time from the blocked record's end.** That
   end includes the ~20 s penalty on the APT model but not on the baseline.
   `disruption_from_mechanism.py` measures from the deployment's completion instead.
3. **Unified tracer:** `src/mtdsim/l3_simulation/trace.py:387-390` prints "ran for
   all of it" for an interrupted action, which never ran.

## Open (ask Marc once)

- Is time to resume a blocked action a §4.5 metric, or chapter 5 depth only?
  Recommendation: depth only. Two disruption metrics (blocked; time lost) say it.

## Validation gate

- §4.5 defines attack actions blocked (per run) and time lost per MTD deployment
  (as above), with a worked example checkable against the run records. The
  compromise rate after an MTD deployment is gone.
- *Condition* is gone from live text, or defined.
- `disruption.py` retires. Its successor reads the baseline's end from its last
  action, and `ablation.py` is updated.
- Figure 5.3 and the §5.3.1 and §5.4 numbers are regenerated.
- Appendix C.5 is deleted.
- The build is clean.

## Reading list

- `docs/implementation/disruption_mechanism.md`, sections 1–5.
- `data/results/s45_metric_redesign/time_to_next_compromise.py` and
  `disruption_from_mechanism.py`.
- `docs/handoffs/2026-09-29_ch4_consolidation.md`, on the other branch: rulings F′,
  L and round 5.
