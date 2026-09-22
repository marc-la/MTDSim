---
status: findings — preliminary read 2026-09-22 on the 100-seed defended corpus; the §6 changes APPLIED the same day (fig_5-2-2a_disruption_response via tools/ch5_disruption_figure.py); caption DRAFT STATE; scrutinise-figure pass recorded in the results context §8g
created: 2026-09-22
topic: "The §5.2.2 read of the defended corpus at the tactic level: what a disruption does to the movement attacker (its actions fail until it holds a host again), how long it takes to compromise a host again beside the baseline attacker, and the reads that stay sentences (position by stage unchanged; the control indistinguishable; the credential layer too rare)"
supersedes: the §5.2.2 half of ch5_s532_adaptivity_findings.md (the verb-level activity mix, kept as the record of that instrument)
---

# §5.2.2 Response to disruption — the tactic-level read

**Design:** [`../../../handoffs/2026-09-20_ch5_s52_s54_results_context.md`](../../../handoffs/2026-09-20_ch5_s52_s54_results_context.md)
§8g (takeaways T5–T8, the mechanism fact, the redesign). **Workspace:**
`data/results/ch5_defended/` (gitignored), the same corpus as the §5.3–§5.4
floats (`runs.jsonl`, 30 200 runs at 100 seeds); `analyse.py` `section_522`
→ `numbers.json` §s522, `preview_fig522.png` (matplotlib, direction only),
`preview_fig522_tikz.png` (the drawn figure). Every measure is the shipped
suite's or a reader over its record fields (`visit_records`, `is_compromise`,
`recovery_times`, `load_stage_of`, `jsd`, `mean_ci`).

## 1. Why the verb-level figure was retired

Marc's read of the 2026-09-17 figure (four panels that look the same, no
visible response) is upheld by its own record (largest shift 2.5 points of
share; the control inside the model's interval in 26 of 28 cells). The
defect under it is resolution: the verb is downstream of the tactic-to-verb
mapping and the distance term keeps the campaign near its lifecycle order,
so a verb-level activity mix inherits the baseline attacker's shape by
construction. The response is read here where the model lives: on the
tactic-level record (place, verb, verdict, blocked, interrupted per visit).

## 2. The mechanism fact (verified from code, §8g)

The baseline attacker is restarted in a phase set by the mechanism's layer,
whatever phase it was in (host layer → scan host; service layer → scan port,
and only from scan port / exploit / brute force; credentials → exploit, only
from brute force). Measured on the defended corpus: 99.97 % of host-layer
disruptions are followed by scan host (the rest end the run), 100 % of
service-layer by scan port, 100 % of credential-layer by exploit.

The movement attacker's token is never moved. Every mechanism charges the
same substrate price (the confusion penalty; a host-layer mechanism also
clears the host cursor); the disruption is a failure verdict at the place the
token is on and that place's failure-matrix row routes it. The layer shows
underneath: after a host-layer mechanism every verb that acts on the current
host fails its precondition until an enumerate or scan host succeeds.

## 3. The reads

Pooled over the four profiles and over each layer's single-mechanism
conditions (host: IP shuffle, complete topology, host topology; service: port
shuffle, OS diversity, service diversity; credentials: user shuffle). Window:
five steps either side of each disruption (a step is one tactic entered,
Figure 5.1's unit; the analyser's `visit_records`); the disruption's own
step belongs to neither.

### 3a. Position by lifecycle stage — unchanged (a sentence, not a panel)

| layer, interval | disruptions (per run) | preparation | intrusion | post-intrusion | objective | JSD before→after | tactic JSD | whole-run tactic JSD vs no defence |
|---|---|---|---|---|---|---|---|---|
| host, 200 s | 90 000 (75.0) | 0.017→0.014 | 0.136→0.127 | 0.738→0.757 | 0.109→0.103 | 0.0004 | 0.0006 | 0.0010 |
| service, 200 s | 64 299 (53.6) | 0.017→0.016 | 0.147→0.140 | 0.715→0.722 | 0.121→0.123 | 0.0001 | 0.0004 | 0.0000 |
| host, 2 000 s | 9 564 (8.0) | 0.038→0.020 | 0.163→0.137 | 0.687→0.742 | 0.112→0.101 | 0.0037 | 0.0042 | 0.0001 |
| service, 2 000 s | 6 633 (5.5) | 0.033→0.018 | 0.163→0.142 | 0.693→0.719 | 0.111→0.121 | 0.0026 | 0.0037 | 0.0000 |
| credentials, 200 s | 305 (0.8) | 0.026→0.026 | 0.164→0.160 | 0.731→0.721 | 0.079→0.092 | 0.0004 | 0.0128 | 0.0000 |
| credentials, 2 000 s | 39 (0.1) | 0.026→0.021 | 0.099→0.174 | 0.759→0.733 | 0.115→0.072 | 0.0116 | 0.0471 | 0.0000 |

The token does not fall back a stage. What movement there is at 2 000 s is
*forward* (post-intrusion +0.03 to +0.05) and is the campaign's drift (the
after-window is later in the run); at 200 s it is within a point. The
whole-run tactic distribution under defence is the no-defence one (JSD ≤
0.001). The placebo (the same disruption positions on the same seed's
unopposed run) at stage level is in `numbers.json` per condition.

### 3b. The response: share of steps whose action fails its precondition (panel a)

| layer, interval | −5 | −4 | −3 | −2 | −1 | +1 | +2 | +3 | +4 | +5 |
|---|---|---|---|---|---|---|---|---|---|---|
| host, 2 000 s | 0.21 | 0.21 | 0.22 | 0.21 | 0.24 | **0.57** | 0.53 | 0.52 | 0.48 | 0.46 |
| service, 2 000 s | 0.15 | 0.16 | 0.16 | 0.18 | 0.18 | 0.17 | 0.16 | 0.17 | 0.15 | 0.16 |
| credentials, 2 000 s (n = 39) | 0.24 | 0.11 | 0.21 | 0.10 | 0.13 | 0.26 | 0.18 | 0.10 | 0.21 | 0.18 |
| host, 200 s | 0.52 | 0.52 | 0.52 | 0.50 | 0.51 | 0.59 | 0.57 | 0.55 | 0.54 | 0.53 |
| service, 200 s | 0.15 | 0.15 | 0.15 | 0.16 | 0.16 | 0.14 | 0.14 | 0.15 | 0.14 | 0.15 |
| control, IP shuffle, 2 000 s | 0.23 | 0.24 | 0.25 | 0.24 | 0.25 | 0.58 | 0.53 | 0.51 | 0.48 | 0.47 |
| model, IP shuffle, 2 000 s | 0.24 | 0.26 | 0.26 | 0.25 | 0.27 | 0.58 | 0.55 | 0.52 | 0.50 | 0.48 |
| control, OS diversity, 2 000 s | 0.15 | 0.17 | 0.17 | 0.19 | 0.21 | 0.18 | 0.16 | 0.18 | 0.17 | 0.18 |
| model, OS diversity, 2 000 s | 0.16 | 0.17 | 0.17 | 0.18 | 0.19 | 0.17 | 0.16 | 0.18 | 0.16 | 0.16 |

Three things are in the table.

1. **The response has a shape, and it is the host layer's.** After a
   host-layer disruption the share of steps at which the attempted action
   fails its precondition rises from about a fifth to well over a half at the
   next step and decays over the following four; it is still above two in
   five at the fifth. Under a service-layer mechanism, which leaves the host,
   the share does not move. The *first* failure after a host-layer disruption
   is a construction fact (the host cursor is cleared); the size of the jump
   and its decay are measured: they are how many steps the routing takes to
   put the token on an enumerate or scan host that succeeds.
2. **At 200 s the windows overlap.** With 75 disruptions per run under a
   host-layer mechanism the before-window of one disruption is the
   after-window of the previous, and the share sits at about one half
   throughout (0.50–0.52 before, 0.59 at +1). The response is there (a
   +0.08 step at +1) but the attacker is never out of it. That is the
   short-interval sentence; the panel is drawn at 2 000 s where the
   disruptions are separated.
3. **The control tracks the model** within 0.025 at every offset under both
   spanning mechanisms (T7). Routing on the verdict changes nothing the
   instrument can see; the response is the substrate's severance and the
   net's ordinary routing back to a host.

### 3c. The recovery: time from a disruption to the next compromise (panel b)

| layer, interval | attacker | n | mean over completed (s) | median | censored share |
|---|---|---|---|---|---|
| host, 2 000 s | movement | 9 564 | 2 051 ± 45 | 1 408 | 0.261 |
| host, 2 000 s | baseline | 1 791 | 425 ± 16 | 332 | 0.022 |
| service, 2 000 s | movement | 6 633 | 1 531 ± 45 | 989 | 0.213 |
| service, 2 000 s | baseline | 1 791 | 575 ± 31 | 350 | 0.085 |
| credentials, 2 000 s | movement | 39 | 1 514 ± 741 | 871 | 0.077 |
| credentials, 2 000 s | baseline | 41 | 641 ± 199 | 477 | 0.049 |
| host, 200 s | movement | 90 000 | 4 776 ± 62 | 4 105 | 0.862 |
| host, 200 s | baseline | 18 292 | 1 079 ± 17 | 708 | 0.131 |
| service, 200 s | movement | 64 299 | 1 689 ± 16 | 1 103 | 0.263 |
| service, 200 s | baseline | 21 201 | 1 233 ± 47 | 748 | 0.757 |

**The pace anchor** (the same attacker's gap between consecutive compromises
with no defence): movement 1 291 ± 48 s (median 891; 2 866 gaps; 6 % of
runs have fewer than two compromises); baseline 394 ± 14 s (median 309;
2 334 gaps; 0 %).

Read against the anchor at 2 000 s: after a host-layer disruption the
movement attacker's next compromise comes 1.6 times its ordinary gap later
(2 051 against 1 291), the baseline attacker's 1.1 times (425 against 394);
after a service-layer disruption 1.2 times (movement) against 1.5 times
(baseline). So a host-layer disruption costs the movement attacker more,
relative to its own pace, than it costs the baseline attacker; a
service-layer one costs the baseline more. In absolute time the movement
attacker recovers three to five times more slowly, which is its pace (T4).

At 200 s the read is different in kind: under a host-layer mechanism 86 % of
the movement attacker's recoveries never complete (it reaches 0.3 hosts per
run under IP shuffle, §5.3.1's number), and under a service-layer mechanism
76 % of the baseline attacker's never complete because the baseline has
finished (it stops at the target or the compromise ratio) before the next
compromise would fall. A conditional mean at 200 s is therefore not a
recovery time; the 200 s row is the sentence "under a host-layer mechanism at
200 s the movement attacker gets its foothold back after one disruption in
seven".

### 3d. The credential layer

User shuffle disrupts the attacker 0.8 times per run at 200 s and 0.1 at
2 000 s (it bites only during brute force, which this attacker reaches
rarely). Too few disruptions at 2 000 s to read a curve (n = 39); one
sentence in the body text with the count.

## 4. Against the record and the board

| quantity | record | here | what moved it |
|---|---|---|---|
| property 4's instrument | verb-level activity mix, a null (`ch5_s532_adaptivity_findings.md` §4) | tactic-level: position unchanged, precondition failures rise then decay, recovery measured against pace | resolution |
| the control (verdict-blind arm) | indistinguishable at verb level | indistinguishable at stage level and on the response curve (within 0.02) | same finding, stronger instrument |
| board D.2 (the spanning pair spans severance / re-roll) | spans outcome, not behaviour | spans the *response*: the host layer produces the failure curve, the service layer does not | the curve |
| the baseline's disruption rule (chapter 3 prose) | stated from Brown | measured: 99.97 / 100 / 100 % | first measurement |
| axis 4 badge (`apt_model_criterion.md`) | DESIGNED | the loop is inert on this instrument too; nothing re-scores a badge from a preliminary | — |

## 5. Validation

Zero error rows; every cell at 100; the figure fits the page box (15.6 ×
6.8 cm); every caption fact printed by the generator matches `numbers.json`.
The interrupt-tally cross-check of the §5.3.2 record (§1 there) is still
open. The thousand-seed rerun is owed with the rest of the chapter.

## 6. What the float needs changed — for Marc (APPLIED 2026-09-22)

1. Panel (a) is the response curve at 2 000 s, host and service layers; the
   200 s saturation is a sentence.
2. Panel (b) carries the pace anchor as the dashed reference in each
   attacker's colour, and the censored share printed; the 200 s recovery is a
   sentence.
3. The position by stage, the control and the credential layer are
   sentences, with their numbers in §s522.
4. Open for Marc: whether panel (b) should plot the ratio to the pace anchor
   instead of the absolute time (the ratio is the fair form; the absolute
   time is the readable one).

## 7. Content points from the scrutinise-figure pass (2026-09-22; two cold readers, one context critic, the second round on the reworked figure)

Both cold readers' one-sentence messages matched T5 and T6 without being
told them. Content the body text must carry (content, not prose):

1. The instrument: a step's action fails when its precondition is missing;
   after a host-layer mechanism the host is gone, so every host-acting verb
   fails until a scan host or enumerate host succeeds. The first failure is a
   construction fact; the size of the jump and its decay are measured (the
   control decays identically, so the decay is the base routing's chance of
   reaching a discovery tactic, not the failure matrix).
2. The service-layer line is flat by construction: a service-layer mechanism
   clears nothing a precondition reads. What it costs shows only in (b). Say
   this, because the two panels otherwise read as disagreeing.
3. Five steps after a host-layer disruption the failure share is still twice
   its before level; the foothold is not back within five steps.
4. The before level differs between layers (0.21 host, 0.16 service) because
   the host-layer runs carry the tails of earlier disruptions (8 per run);
   the floor of about one in six with no disruption near is the profile mix
   through the mapping (a precondition unmet by the campaign's own order).
5. Position by stage: no fall-back; it stays in its campaign (§3a).
6. The baseline's landing shares (§2), bridged once from chapter 3's
   network / application layer names to Table 2.1's host / service /
   credentials.
7. The control within 0.025 at every step on both spanning mechanisms and
   inside the recovery intervals; its declaration at the head of the
   subsection is owed.
8. The 200 s sentence: median spacing between disruptions 7 steps, so the
   share sits at about one half throughout (0.50–0.52 before, 0.59 at +1);
   the same shape on a raised floor.
9. Credentials: 0.1 disruptions per run at 2 000 s (39 in 400 runs), 0.8 at
   200 s; the mechanism bites only during brute force.
10. Recovery against the pace anchor (§3c): host 1.6× (movement) against
    1.1× (baseline); service 1.2× against 1.5×. The dashed line anchors pace
    and is not a null (a random-time null on the unopposed runs sits within
    ±9 % of it); no bar-minus-line arithmetic in the prose.
11. The inversion (host hits the movement attacker hardest, service the
    baseline hardest) marked as an observation; the reason is chapter 6's.
12. Censored shares differ across attackers by the stopping rule (0.66 of the
    baseline's host-layer runs and 0.49 of its service-layer runs reach the
    target and stop, so every disruption before the target is followed by a
    compromise; its censored recoveries are all in non-target runs cut at the
    time limit), not by behaviour; on the movement side every censored
    host-layer recovery is in a run cut at 15 000 s. Do not compare 26 %
    against 2 %.
13. The movement attacker's mean host-layer recovery (2 051 s) exceeds the
    2 000 s interval, so a recovery typically spans a further disruption; the
    measure counts to the next compromise whatever lands in between. One
    clause.
14. The verb-level null in one sentence; chapter 6 owns the mapping
    limitation.
15. The host-layer pooling range if a number is quoted: IP shuffle 2 221 s
    (33 % censored) against the two topology shuffles 1 985 / 1 970 s
    (22–23 %).
16. Hand-off: hosts reached 6.36 (host layer), 8.06 (service), 8.13 with no
    defence.
17. **The baseline's service-layer cost is service diversity alone** (third
    round, verified per condition): 952 s (2.42×, 18 % censored) against port
    shuffle 370 s (0.94×) and OS diversity 378 s (0.96×), at its no-defence
    pace of 394 s; host-layer conditions 398–442 s (1.01–1.12×). The
    layer-level inversion is an observation for the movement attacker (host
    1 970–2 221 s, 1.53–1.72×, above service 1 490–1 611 s, 1.15–1.25×, in
    every condition) and a one-condition fact for the baseline. State it so.
18. The estimator sentence: means over completed recoveries; the movement
    side's ordering holds on medians (1 408 / 989 s) and on the examiner's
    censoring-aware medians (1 790 / 1 377 s); the baseline's two layers are
    level on medians (332 / 350 s).

### Per-condition recovery at 2 000 s (third round)

| condition | movement mean (×gap) | median | censored | baseline mean (×gap) | median | censored |
|---|---|---|---|---|---|---|
| IP shuffle | 2 221 (1.72) | 1 476 | 0.33 | 398 (1.01) | 320 | 0.05 |
| host topology | 1 970 (1.53) | 1 397 | 0.23 | 442 (1.12) | 349 | 0.01 |
| complete topology | 1 985 (1.54) | 1 380 | 0.23 | 429 (1.09) | 333 | 0.01 |
| port shuffle | 1 490 (1.15) | 953 | 0.23 | 370 (0.94) | 294 | 0.04 |
| OS diversity | 1 493 (1.16) | 934 | 0.21 | 378 (0.96) | 303 | 0.01 |
| service diversity | 1 611 (1.25) | 1 070 | 0.21 | 952 (2.42) | 673 | 0.18 |
| user shuffle (n = 39 / 41) | 1 514 (1.17) | 871 | 0.08 | 641 (1.63) | 477 | 0.05 |

Flagged for Marc, outside this figure's scope: the shared key map
`tools/_ch5_style.py` LABEL["movement"] reads "attacker model", which the
registry reserves for the genre; this figure writes "movement attacker" in
its own key, and the map's other users (`fig_5-3-2a_cross_arm`,
`fig_5-4a_frontier`, the efficiency table) are his ruling.
