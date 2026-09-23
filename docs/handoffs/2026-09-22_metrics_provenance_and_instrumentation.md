---
status: open                  # executes register E3 and E4; re-cut 2026-09-23 on Marc's direction (efficiency out, grouping by phase, the field's names); Marc's disposition pass on §1 and the §4 rulings owed; owns the internal-MTTC finding the README carried unowned since 2026-08-05
created: 2026-09-22
updated: 2026-09-23
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E3, §E4 (and E10(i)'s set-up)
companions: ../workflows/terminology.md (the word *suppression* — its PROPOSED row; `python tools/term_screen.py census suppression` lists every site: Table 5.2's row, the captions of Figures 5.3–5.4, the headers of Tables 5.4–5.5, `tools/_ch5_style.py` and the ch5 generators' axis labels), 2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md (the analyser that computes every row), 2026-09-20_ch5_s52_s54_results_context.md (the §5.2 wording bars — no "less detectable", no badge words in chapter 5)
---

# Give every metric a source — a citation, or a methodology definition with why it is needed — and put stealth back beside the no-defence numbers

## State of play

**The ruling (E3, E4).** For each metric the supervisor wants the reference (MTTC, NCR and the like, formulas referenced); a new metric must be in the methodology with the full detail of how it is calculated and *why* — it must explain something the existing metrics cannot. Stealth is the licensed exemplar (no simulator computes it; APTs are defined by remaining undetected). *Suppression* fails the test (attack success rate before and after). The stealth readings return to Table 5.3, grouped with hosts reached and delay to first compromise so the "worse" numbers are read with the property that explains them. E10(i) is the discussion this sets up: on the existing metrics the model looks poor, but it is much harder to detect — "which the methodology must explain well".

**Marc's direction, 2026-09-23 (spoken, this session).** (1) The effectiveness / efficiency split in Table 5.2 is vacuous and goes: the thesis does not model efficiency, so no efficiency row survives. (2) The reasonable split is the chapter's own — the APT attacker model against the baseline attacker, then the APT attacker model against the defences. (3) The gap efficiency leaves is filled by the fidelity metrics built while the model was built (supervisor updates 03 and 09 Aug, [`../implementation/supervisor-updates.md`](../implementation/supervisor-updates.md) §6.1, §7.1), ported only where they earn it — the literature review is the inspiration, not the list. (4) Terminology: the field's name wherever the quantity is the field's, faithful even if not one-to-one. (5) A chapter 4 heading for the unit, not drafted.

**Done this session.** The heading: §4.5 *Instrumenting MTDSim* (`sec:instrumenting`), placeholder plus per-metric content points in its comment, no prose; build clean at 85 pages. §1 below re-cut to Marc's direction; §4 new (what §5.2 carries for the fidelity claim, with a dry-run on the current corpus).

### 1. The provenance triage, re-cut — Marc's disposition pass

Table 5.2 today is `docs/thesis/tables/tab_5-1b_metrics.tex` (ten rows, two groups, no source column; its comment trail records every prior ruling). Locators below are from Table 3.1 (`dissertation.tex` l.~2120) and the extractions; the literature agent's pass is folded in at §1c, and any locator marked *verify* must be checked before it reaches the tex.

**1a. Row by row.**

| Table 5.2 row now | Disposition | Field name and source | Read in |
|---|---|---|---|
| Target reached | **cite**, renamed | *attack success rate*, as an estimate of Cho's *attack success probability* ("the probability that attacks are successfully performed", e.g. a target found; cho2020 §VII-A p.727; Zaffarano's *attack success*, p.9, is the same shape). **Not Ho's ASR**: Ho's Eq. 11 (p.20) is hosts compromised over attempted actions, a per-attempt quantity with the same name. Tay names ASR without defining it (§5.1 p.19) | §5.2, §5.3 |
| Hosts reached | **cite**, renamed, reported as a ratio | *network compromise ratio* — Zhang (compromised over total hosts, used as the 0.8 stopping checkpoint, §5 p.32); Ho's HCR, Eq. 10 p.19; Tay §4.1.1 p.15 (no formula). The checkpoint here is the end of the run | §5.2, §5.3 |
| Delay to first compromise | **cite**, renamed, checkpoint declared | *mean time to compromise* — McQueen (time to reach a privilege level on a component, Eq. 6); Zhang ("the time it takes for an attacker to compromise a target host", §3.4 p.16, reported at NCR 0.8); Cho ("how long an attacker takes to compromise an entire system", p.727). This thesis reads it at the first host: the lineage's checkpoint is one the APT attacker model never reaches (0.14–0.20 at the limit), and the target is reached in too few of its runs (0.05–0.17) to average over. **The lineage disagrees on the quantity** — see §2 | §5.2, §5.3 |
| Runs with no compromise | **fold** into the MTTC row: it is the share of runs the mean is not taken over, and has to be stated beside the mean anyway | — | with MTTC |
| Suppression | **retire the name**; keep the quantity as what it is — the relative reduction in the compromise ratio, $1 - \mathrm{NCR}_{\text{defence}}/\mathrm{NCR}_{\text{none}}$, an operator on a cited metric | NCR's sources | §5.3.2, §5.3.3 |
| Blocked fraction | **define** in §4.5 (Figure 5.2(a) and Table 5.4 read it); plain name, e.g. *failed-precondition share*. Brown's *attack actions blocked* is the MTD interrupt, not this (attribution removed 2026-09-20) | new | §5.3.1, Table 5.4 |
| Actions per host reached | **drop** — Brown's *attempts required* is its source, but no surviving float reads it (it was an efficiency row) | — | — |
| Successes per host reached | **drop** — efficiency, no counterpart, no float | — | — |
| Time lost to MTD | **drop** with efficiency (Figures 5.5–5.6 and Table 5.7 retired, E1) | — | — |
| Share of run under reconfiguration | **drop** with efficiency | — | — |

**New rows** (no row today):

| Metric | Disposition | Source | Read in |
|---|---|---|---|
| **Attack intensity** (stealth) | **adapt and define** in §4.5 — the fidelity metric E3 licenses. The name is He's (§1c); the definition is ours: actions per unit of the attacker's active time, read beside the baseline's as He reads his against the original attack | adapted from He's *relative intensity* (he2025 §V-B p.5053); the *why* cites Alshamrani ("a persistent low-and-slow tempo that trades speed for evasion", §3.1.1, `dissertation.tex` l.~1011) and He's finding that evasion came from periodic delays | §5.2, Table 5.3 |
| Share of steps per tactic | **define** (Figure 5.1(a)) | new | §5.2 |
| Share of runs leaving the commonest opening | **define** (Figure 5.1(b)) | new | §5.2 |
| Profile divergence | **define**, the statistic cited as a statistic (Jensen–Shannon; the citation for the statistic is owed) | new use of a standard statistic | §5.2 body text |
| Recovery time after a disruption | **define** (Figure 5.2(b)) | new | §5.3.1 |

**What this overturns, named.** The 2026-09-18 ruling (3) in the table's comment trail took the §5.2 instruments *out* of Table 5.2 on the ground that calling them validation claims a proof a self-chosen set cannot carry. E3 makes that ground moot: every metric the chapter reads needs a source, so they come back in, marked as introduced, and the "observation, not validation" framing does the work the omission was doing. The 2026-09-20 rulings (no direction-of-good marks, one quantity per row, definitions only in words the reader has met) stand.

**1b. The proposed Table 5.2** (a mock for the ruling, not the tex):

| | Metric | Definition | Source |
|---|---|---|---|
| *The two attackers compared (Section 5.2)* | Attack success rate | share of runs that compromise a database host (the targeted objective) | as attack success probability, Cho; Zaffarano |
| | Network compromise ratio | hosts compromised by the end of the run, over the 50 hosts | Zhang; Ho; Tay |
| | Mean time to compromise | mean time from the start of a run to its first compromised host, over the runs that compromise one; the share that compromise none is given beside it | McQueen; Zhang (at a ratio of 0.8) |
| | Attack intensity | actions the attacker takes on the network per 1 000 s of its active time; a tactic that takes no action adds time, not an action | adapted from He; Section 4.5 |
| | Share of steps per tactic | … | Section 4.5 |
| | Runs leaving the commonest opening | … | Section 4.5 |
| *The APT attacker model against MTD (Section 5.3)* | Reduction in compromise ratio | $1 - \mathrm{NCR}_{\text{defence}} / \mathrm{NCR}_{\text{none}}$ | the ratio's sources |
| | Failed-precondition share | share of steps whose action fails on an unmet precondition | Section 4.5 |
| | Recovery time | time from a disruption to the next compromise, over the attacker's own mean gap between compromises with no defence | Section 4.5 |

Grouped by phase, as Marc put it; the three cited outcome metrics are read in both phases and sit where they are first read. The Source column is what answers E3 row by row. The alternative grouping (cited / introduced) says the same thing, because every introduced metric but the last two is a §5.2 metric.

**1c. Naming — the literature pass** (extraction sweep, 2026-09-23; printed page numbers, PDF-checked unless the extraction marks them otherwise; verify before the tex).

- **No paper in the corpus has a stealth metric of the attacker model's own behaviour to cite.** Detection in the field is measured from the defender's side: He's *adversarial detection rate* (share of attacks a detector flags, §V-B p.5053), Zaffarano's *attack confidentiality* (share of tasks visible to detection, formula §4.3 p.10), Cho's survey entries (p.728), Outkin's per-step detection probability (`outkin2022` — note the key; §3.5, pages unverified). Tay's "attacker detection rate" is the share of attacker actions given to the RL defender in training, not a stealth measure (§5.3 p.23). Zhang, Ho and Brown have no detection model. So the thesis **must define** its stealth metric, as E3 foresaw.
- **But the field has the word.** He pairs detection rate with **relative intensity** — the attack's packets per second over the original attack's (§V-B p.5053) — and finds that evasion came from *periodic delays* that turn a flood into an intermittent one. That is the same mechanism as the dwell tactics, measured the same way (rate against a reference attack). He is already cited in Table 3.1. Recommended name: **attack intensity**, adapted (packets → the attacker's actions), with the baseline attacker as the reference He's "original attack" is. Dry-run in those terms: $c_1$ 0.75, $c_2$ 0.71, $c_3$ 0.57, $c_{\mathrm{agg}}$ 0.74 of the baseline's intensity, $c_4$ 1.01.
- **Nearest neighbours to cite for contrast in §4.5:** Zaffarano's *attack productivity* (mean task duration, "how quickly an attacker can perform and complete adversarial tasks", §4.1 p.9) — a tempo metric, but duration per task, not time between tasks; Cho & Ben-Asher (an MTD lengthens reconnaissance and so gives the detector more time, p.151–152). Dwell time in the M-Trends sense (intrusion to detection) is a different quantity and should not lend its name.
- **The other rows:** see §1a — *attack success rate* follows Cho's probability, not Ho's per-attempt ratio; *mean time to compromise* follows McQueen and Zhang's "time to compromise", not Ho's mean event duration; NCR is Zhang's and Ho's Eq. 10. Brown's two metrics are counts with no formula ("attack actions blocked", Fig. 4; "attempts per compromise", Fig. 5; §V-D p.7) and leave with the efficiency rows. No paper measures variety in the attacker's own behaviour (APV, SAPV and Cho's unpredictability are all network-state or defender-side), so the §5.2 descriptive instruments are new, as §1a has them. No paper has a disengagement metric; Brown's give-up-after-ten and Zhang's interruption threshold are behaviours.

**Why the compromise ratio and not the success rate carries phase two.** Jin's test for suppression was "attack success rate before and after". On the current corpus the APT attacker model's success rate is 0.09 with no defence and 0.00 under most defence conditions (Table 5.4), so it cannot order the defences; the compromise ratio can. That is the one clause §4.5 owes the reader for choosing it, and it is a result worth telling Jin before the week-9 meeting (E11).

### 2. The internal-MTTC finding, owned here

`docs/handoffs/README.md` has carried since 2026-08-05 "one finding with no owner": `mtdnetwork/statistic/evaluation.py:110` computes attack-action time over the *number of attack actions* — a mean action duration — and ranks IP shuffle best and OS diversity below no defence (`attacker_read_surface.md` §(m1)).

**New, 2026-09-23 — this may be Ho's definition, not a bug.** The literature pass reads Ho's MTTC (§3.3.2 item 8, p.20, unnumbered equation) as the mean duration of SCAN_PORT, EXPLOIT_VULN and BRUTE_FORCE events over the relevant hosts — which is what `evaluation.py` computes. Zhang's is "the time it takes for an attacker to compromise a target host" (§3.4 p.16), McQueen's the time to reach a privilege level (Eq. 6). If that reading holds, the lineage uses one name for two quantities, and the inherited function is Ho's faithfully; classify against `mtdsim_intent_spec.md` before calling it anything (*to verify* — not asserted here). It does not change the disposition: the thesis's quantity is the time to compromise, and §4.5 says whose.

Disposition proposed: the thesis's MTTC is **defined in §4.5 as the time to the first host compromised**, computed by the chapter's analyser on both attackers, and `evaluation.py`'s quantity is never reported; `metrics_semantics.md` §(a) gains a one-paragraph note that the reported MTTC is not that function, and `project_context.md`'s "primary metric is internal MTTC" sentence is corrected.

### 3. The chapter 4 unit — heading placed

**Placed 2026-09-23** as §4.5 *Instrumenting MTDSim* (`\label{sec:instrumenting}`), its own section after §4.4.4, because the metrics are not part of the join §4.4 declares; moving it under §4.4 is one line. *Metrics* is the alternative heading (parallel to §3.2.2's). The placeholder's comment carries the per-metric content points: field name; definition in the formalism's symbols where one applies; what it captures; why the cited metrics do not; the citation or the reason it is new. Every introduced metric gets a hand trace (V1), recorded in a small validation table in the appendix or the record. §5.1's Metrics unit then points to §4.5 only (the antecedent rule), and its "grouped by effectiveness and efficiency" sentence goes with the split.

### 4. What §5.2 carries for the fidelity claim

**Where it stands.** Figure 5.1 (where each profile's steps fall; how soon runs leave the commonest opening) and Table 5.3 (hosts, target, delay, runs with no compromise). Read cold by a general computer-science reader, the section says: the model walks a richer, less scripted campaign, and it is *worse* — a third of the hosts, a tenth to a third of the success rate, three times slower. Nothing on the page says why the second is not a defect. That is Jin's objection (E4) and it is the section's hole.

**The takeaways it should leave, in order** (content points for Marc's prose, not wording):

1. *Campaign shape* (Figure 5.1(a)) — each profile spreads its steps over a campaign of 12–15 tactics, weighted by its objective; the baseline repeats six activities. Divergence in the body text, as ruled 2026-09-21.
2. *Not one script* (Figure 5.1(b)) — the model's runs leave the commonest opening within a few steps; the baseline's open the same way for four.
3. *Slower, and so behind at the time limit* (Table 5.3) — on the field's three metrics the model has reached less by 15 000 s; the ruled 60 000 s sentence says it is still climbing when the baseline has stopped.
4. *Quieter, for the same reason* (**new**, Table 5.3's added column) — it acts at a lower intensity, leaving more time between its actions, and the non-action tactics that make it slower are what make it quieter. One mechanism, two readings: the trade Alshamrani names. The profile with the fewest non-action tactics ($c_4$) is the exception, and its composition is the mechanism showing, not an anomaly.
5. *For chapter 6, not §5.2:* the field's three metrics read only the speed side of that trade, so an evaluation built on them alone scores a low-and-slow attacker as a weak one (E10(i)).

**Dry-run, current corpus** (`data/results/ch5_s531_unopposed/runs.jsonl`, 100 seeds, targeted, 15 000 s, no defence; the script is session scratch, the method is stated so the analyser can reproduce it — one action = one verb invocation, the baseline's consecutive per-vulnerability `EXPLOIT_VULN` rows collapsed to one; a movement step counts if it is action-bearing; the gap is start to start; the run is the unit, 95 % interval on the mean across runs). **Preliminary — for the design ruling only, not the page:**

| | mean gap (s) | median gap (s) | gaps over 60 s | actions per 1 000 s of own active span | active span / horizon |
|---|--:|--:|--:|--:|--:|
| $c_1$ | 47.1 ± 0.7 | 26.9 | 28.8 % | 21.4 | 0.98 |
| $c_2$ | 49.8 ± 0.8 | 27.1 | 29.2 % | 20.3 | 0.96 |
| $c_3$ | 62.2 ± 1.1 | 38.9 | 38.4 % | 16.2 | 0.99 |
| $c_4$ | 35.1 ± 0.5 | 16.2 | 20.0 % | 28.7 | 0.98 |
| $c_{\mathrm{agg}}$ | 47.9 ± 0.8 | 25.6 | 28.6 % | 21.0 | 0.94 |
| baseline | 35.7 ± 1.0 | 19.8 | 15.2 % | 28.4 | 0.70 |

What moved since the 2026-08-09 diagnostic (10 seeds, general objective, before d127f443): the contrast holds for three profiles and the aggregate (1.3–1.7× the baseline's gap, against 1.5–1.8× then), and $c_4$ moved from *denser* than the baseline to *level* with it. **One trap, found here:** a rate over the whole horizon erases the contrast (baseline 19.6 per 1 000 s, profiles 16–21), because under the targeted objective the baseline stops acting when it takes the target, at 0.70 of the horizon on average. So the intensity has to be taken over the attacker's **active** time (the start of the run to the end of its last action), not the horizon; the mean gap between actions is the same reading with no denominator to choose. §4.5 declares the active-time denominator in a clause and says why.

**What to add, recommended:**

- **(a) Table 5.3 gains one column, attack intensity (actions per 1 000 s of active time), with its interval** — E4 as ruled, grouped with hosts and delay; the ratio to the baseline's (He's form) in the body text. One column, not two: the detectability *level* $D$ carries three declared magnitudes (tier ratio, decay constant, CVSS weight) that nothing outside the model calibrates, so E5's "why that number" would land on each, and its time-average is the action rate times a near-constant increment by identity (`stealth_spacing_diagnostic.md` §2a), so it adds the shape of the quiet, not the separation. Recommend $D$ is declined and the reason recorded.
- **(b) One body sentence, the ablation** — remove the non-action tactics from the recorded stream and every profile's gap falls under the baseline's (diagnostic §3). It is what lets takeaway 4 say *for the same reason* rather than *also*. Re-run on this corpus first.
- **(c) One figure, an example run of each attacker on one time axis** (optional; recommended if a float can be afforded) — one representative seed of the baseline and one profile over the first ~2 000 s: steps as bars coloured by tactic or activity, actions as ticks. It shows a reader what the column measures: the baseline acting back to back, the model's actions separated by the quiet tactics, and the same gaps that put it behind in Table 5.3. It is the *example* the lit-review examiner said was missing (`project_lit_review_result.md`), and nothing else in the chapter shows time. The alternative is the gap-survival curve (share of gaps longer than *t*, per attacker; diagnostic fig7), which measures where the example illustrates, but it repeats the column. Scrutinise before ratifying (`scrutinise-figure`).

**Considered and not recommended:**

- *Effective behavioural breadth* (formerly predictability; baseline 1 by construction, model 2.7–5.9): strategic plurality is already carried by Figure 5.1(b); it predates d127f443, the current baseline records may lack the field its reader needs (`current_host_uuid`, unverified), and it would add a third plurality exhibit. The gap in §5.2 is stealth, not plurality.
- *Detectability level D*: see (a).
- *Disengagement*: its kill criterion fired, its W comes from the retired 0.8 objective, and the ablation subsection that would have held it was removed 2026-09-13 (C31).
- *Path entropy, coverage curves, deepest stage*: killed or saturated (records on file).

**The ceilings that ride with the column.** An observation of the no-defence arm (conventions §f); axis 5 stays NOT ADDRESSED and chapter 6 says so; no "less detectable" in chapter 5 (results-context bar) — "acts at a lower intensity" / "leaves more time between its actions" are the sayable forms; the cross-attacker time caveat (the two attackers' time is priced differently) stated once, with the diagnostic's substrate re-pricing result as the check (it held four of five in August; re-run it).

## Rulings owed (Marc)

1. The §1a dispositions, one pass — especially: MTTC's checkpoint (first host) and folding *runs with no compromise* into it; the drops.
2. The grouping of Table 5.2: by phase (recommended, as proposed in §1b) or cited / introduced.
3. The lineage names on the floats (spelled out, no acronyms, per the 2026-09-20 ruling) or only in Table 5.2's Source column. Recommended: spelled out on the floats — the name *is* the provenance.
4. The phase-two quantity: *reduction in compromise ratio* on the floats (recommended), or the ratio with and without a defence drawn raw.
5. §4 (a)–(c): the one stealth column and declining $D$; the ablation sentence; the example-run figure.
6. The stealth metric's name: *attack intensity*, adapted from He (recommended, §1c), or the plain *time between actions*.

## Validation gate

Every Table 5.2 row has a Source; every row marked *define* has a definition-and-why paragraph in §4.5; *suppression* appears nowhere in the tex body or floats; Table 5.3 carries the stealth column at 1 000 seeds with its caveats in the caption or one body sentence; each introduced metric has a hand-trace record; `metrics_semantics.md` and `project_context.md` corrected; build clean.

## Hard constraints

- The claim ceiling: the stealth column is an observation; no stealth *state* is claimed; the badge does not move.
- Numbers reach the page only through the analyser and a generator at the reported seed count. The §4 dry-run is not one.
- Literature conventions: definition before use; the field's name where the quantity is the field's (`literature_conventions.md`).

## Reading list

- `docs/thesis/tables/tab_5-1b_metrics.tex` — the comment trail is the record of every prior ruling on this table.
- `docs/implementation/pipeline/ogasp/stealth_spacing_diagnostic.md` §2–§6 — the spacing metric, its ablation, its re-pricing check, and why a scale-free statistic cannot carry it.
- `docs/implementation/supervisor-updates.md` §6.1, §7.1 — the fidelity metrics as Jin last saw them (09 Aug).
- `docs/implementation/metrics_semantics.md` §(a), §(d); `docs/implementation/attacker_read_surface.md` §(m1).
- `docs/thesis/dissertation.tex` l.~2120 (Table 3.1) and l.~1011 (Alshamrani's low-and-slow sentence).
- `docs/sources/extractions/{brown2023,zhang2023,ho2024,tay2024,cho2020}.md` — the metric definitions and locators.

## Out of scope

The runs (corpus handoff); the float regeneration (after the rulings); where the columns sit in the chapter (landed with the restructure).
