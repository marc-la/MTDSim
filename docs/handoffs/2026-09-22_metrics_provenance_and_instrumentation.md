---
status: open                  # executes register E3 and E4; second pass 2026-09-23 (the strict pass Marc asked for: a census of every metric in the corpus, a verdict per metric, §5.2's shape); rulings owed in one sitting; owns the internal-MTTC finding
created: 2026-09-22
updated: 2026-09-23
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E3, §E4 (and E10(i)'s set-up); E8's Figure 5.1 fixes, as they bear on §5.2's shape
companions: ../sources/extractions/mtd_metric_catalogue.md (THE lookup — every verdict below rests on it; the six census tables are in ../sources/extractions/metric_census/), ../workflows/terminology.md (the word *suppression*; `python tools/term_screen.py census suppression` lists every site), 2026-09-22_ch4_overview_figure_family.md (owns Figure 5.1's redraw — colour heat map, bars; the shape in §4 here is what it redraws to), 2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md (the analyser), 2026-09-20_ch5_s52_s54_results_context.md (the §5.2 wording bars — no "less detectable", no badge words in chapter 5)
---

# Give every metric a source — the field's name and citation, or a §4.5 definition with why it is needed — and give §5.2 the stealth reading that explains its "worse" numbers

## State of play

**The rulings.** E3: every metric cited, or defined in the methodology with how it is computed and why it is needed — it must explain something the existing metrics cannot; stealth is the licensed example; *suppression* fails the test. E4: the stealth readings go back beside the no-defence numbers that read as "worse". E10(i): on the existing metrics the model looks slower and less successful but is much harder to detect, "which the methodology must explain well". E8: Figure 5.1(a) in colour as a heat map, 5.1(b) as a bar chart (minutes, 22 Sep: "a line graph is for quantities correlated from one point to the next").

**Marc's direction, 23 Sep (two passes, spoken).** The effectiveness / efficiency split goes — the thesis does not model efficiency. Every metric is strictly conventional, named as the field names it, acronym where it has one, *"look me in the eye: this exists, or this doesn't and we are inventing it for this reason"*; nothing made up to fix a problem ("intensity sounds made up"); no false attribution. Group Table 5.2 by what each metric measures. Everything in §5.2 is motivated or cut, however strong. The 15 000 s horizon stands. Get the *shape* of Table 5.2 and §5.2 right first; full values after.

**Done 2026-09-23.**
- §4.5 *Instrumenting MTDSim* placed in the tex (heading, placeholder, content points; no prose). Build clean, 85 pages.
- **The census**: six passes, one paper per pass, ~1 100 metric rows over every paper held plus an open-access web pass → [`mtd_metric_catalogue.md`](../sources/extractions/mtd_metric_catalogue.md) and `metric_census/`.
- **A correction to the first pass (commit f6c4a493).** *Attack intensity, adapted from He's relative intensity* is withdrawn: RI is He's **maliciousness** metric; his evasiveness metric is ADR, which needs a detector. Using RI as stealth reverses his reading.

### 1. The verdict on every metric — Table 5.2's rows and everything the chapter reads

Full evidence per row: catalogue §(a). *Exists* = a paper names and defines it (or its faithful abstraction); *does not exist* = no paper in the census has it.

| Current name | Verdict | Name to use | Cite | If kept, why |
|---|---|---|---|---|
| Target reached | **exists** | attack success probability (**ASP**) | Cho 2020 §VII-A; Zaffarano 2015; run-level estimate as Zhuang 2012 | — (not "ASR": Ho's ASR is per attempt; no paper defines a per-run success *rate*) |
| Hosts reached | **exists** | network compromise ratio (**NCR**) | Zhang 2023 §5; Ho 2024 Eq. 10 (HCR); Cheng 2014 (CHP) outside the lineage | — |
| Delay to first compromise | **exists**, checkpoint ours | mean time to compromise (**MTTC**) | McQueen 2006; Zhang 2023 §3.4 | — the checkpoint is stated (below) |
| Runs with no compromise | **not a metric** | — | — | becomes MTTC's note: the share of runs its mean is not taken over |
| Suppression | **does not exist, not needed** | — (NCR with and without the defence) | NCR's | — |
| Blocked fraction | **exists, adapted** (Marc's ruling — catalogue row) | attack actions blocked, as a share | Brown 2023 §III-D, §IV-A, Fig. 4 | adaptivity (§5.3.1) |
| Recovery time (Figure 5.2(b)) | **does not exist** attacker-side | recovery time (plain) | — (MTTR is defender-side); why the attacker must recover: Jafarian 2015 | adaptivity — the one APT property readable only under a defence |
| Actions per host reached | exists (Brown's *attempts required*) | — | — | **cut**: no float reads it; it re-reads "worse" |
| Successes per host reached | does not exist | — | — | **cut** |
| Time lost to MTD | does not exist as named | — | — | **cut** with efficiency |
| Share of run under reconfiguration | exists (downtime family) | — | — | **cut** with efficiency |
| *new* — attacker actions per unit of its active time | **exists** | **attack rate** (with **attack inter-arrival time**) | Zhan, Xu & Xu 2013 §III; Pendleton 2016 §5.1 | stealth: the field reads rate as aggressiveness; the thesis's *lower rate → quieter* reading is argued in §4.5 from Ward 2018 §5.18, Jafarian 2015 §VII, He 2025 §VI-D, Alshamrani 2019 |
| *new* — share of actions a rate detector would not flag | **exists, adapted** | **attack confidentiality** | Zaffarano 2015 Table 4, §4.3; relayed by Cho 2020, Sengupta 2020; already in Table 3.1 | stealth, as detectability: Zaffarano's exposure rule was plaintext visibility; ours is a declared rate threshold, shown at every window |
| Share of steps per tactic (Figure 5.1(a)) | **does not exist** | share of steps per tactic (plain) | — | objective conditioning is claimed and is visible only in what the attacker does |
| Runs leaving the commonest opening (Figure 5.1(b)) | **does not exist** | (plain) | — | strategic plurality is claimed; the baseline attacker is one script |
| Profile divergence (body text) | does not exist (the statistic does) | — | — | **cut**: the colour heat map shows it, and its null is a construction fact (ruled 2026-09-21) |

**Mean time to compromise, in plain words.** Every MTTC is "the time until the attacker has compromised *X*", and a paper has to say what *X* is. Zhang's *X* is 80 % of the hosts. The APT attacker model never gets there (15–20 % by the time limit), and it takes the database target in only 5–17 % of its runs, too few to average over. So this thesis's *X* is **its first host**: MTTC = the mean, over the runs that compromise a host, of the time from the start of the run to the first compromise, with the share of runs that compromise none printed beside it. The lineage uses the name for at least five quantities (catalogue §(b)2); §4.5 says which one this is.

**Why NCR, and not ASP, carries phase two.** Jin's test for *suppression* was ASP before and after. Under a defence the APT attacker model's ASP is 0.00 on most conditions (Table 5.4), so it cannot order the defences; NCR can. One clause in §4.5, and worth telling Jin before week 9 (E11).

**What this overturns, named.** (1) The 2026-09-18 ruling that kept the §5.2 instruments out of Table 5.2 — E3 needs a source for every metric the chapter reads, so they come in, marked. (2) The 2026-09-20 removal of Brown's attribution from *blocked fraction* — on Brown's own §III-D wording (catalogue row); Marc's to confirm. (3) This brief's own first pass (*attack intensity*).

### 1b. The proposed Table 5.2 (a mock for the ruling)

Grouped by what each measures, per Marc: what the attacker **does** (read in §5.2) and what it **achieves** — the field's effectiveness metrics, read in §5.2 as the no-defence reference and in §5.3 against each defence. No efficiency group.

| | Metric | Definition | Source |
|---|---|---|---|
| *Attacker behaviour* | Share of steps per tactic | … | Section 4.5 |
| | Runs leaving the commonest opening | … | Section 4.5 |
| | Attack rate | the attacker's actions per 1 000 s of its active time | Zhan et al.; Section 4.5 for the stealth reading |
| | Attack confidentiality | share of the attacker's actions a detector with window *w* would not flag | adapted from Zaffarano et al.; Section 4.5 |
| *Effectiveness* | Attack success probability (ASP) | share of runs that compromise a database host | Cho et al.; Zaffarano et al. |
| | Network compromise ratio (NCR) | hosts compromised by the end of the run, over the 50 hosts | Zhang; Ho |
| | Mean time to compromise (MTTC) | mean time to the first compromised host, over the runs that compromise one | McQueen et al.; Zhang |
| | Attack actions blocked | share of the attacker's actions that fail on a precondition the defence removed | adapted from Brown et al. |
| | Recovery time | time from a disruption to the next compromise, as a multiple of the attacker's own pace | Section 4.5 |

"Effectiveness" is Table 3.1's own word, so the tie-back is literal; it stands alone now, not as half of a split.

### 1c. The metrics we built before, and what becomes of each

From the supervisor updates (03 and 09 Aug, [`../implementation/supervisor-updates.md`](../implementation/supervisor-updates.md) §6.1, §7.1) and the records. Each is judged on E3's test: does it explain something the cited metrics cannot, and does a paper name it?

| Built as | Property | Verdict | Why |
|---|---|---|---|
| Attack profile divergence (Jensen–Shannon) | objective conditioning | **cut** | the colour heat map shows the difference directly; the number's null band is a construction fact (four nets, different tactic sets) and can't be failed |
| Predictability → effective behavioural breadth | strategic plurality | **cut** | *unpredictability* is Cho's and Jalowski's name for the defender's configuration (a collision Jin would catch); the baseline's value of 1 is a theorem, not a measurement; plurality is already shown by Figure 5.1(b) |
| Opening variety | strategic plurality | **keep** (Figure 5.1(b)) | no field metric exists; plurality is claimed; one definition in §4.5 |
| Detectability *D* (decaying exposure level) | stealth | **replace** by attack confidentiality | *D* carries three hand-set magnitudes (tier ratio, decay constant, CVSS weight) and no field name; its time-average is the attack rate times a near-constant, by identity |
| Inter-invocation spacing | stealth | **becomes** attack rate / inter-arrival time (the field's names for exactly this) | — |
| Disengagement time / abandonment effort | incentive rationality | **cut** | the capability sits at its inert default in the reported configuration; its kill criterion fired; its budget came from the retired 0.8 objective; no field metric |
| Learning effect (exploit memory) | learning | **cut** | inert default in the reported configuration; the measured effect was null |
| Path entropy; coverage curves; deepest stage | plurality; persistence | **cut** (already) | killed (hub occupancy) or saturated |
| Re-compromise churn | — | **not a metric** | a diagnosis |
| Blocked fraction | adaptivity | **keep**, as *attack actions blocked* | Brown's metric, adapted (§1) |

### 2. The internal-MTTC finding, owned here

`evaluation.py:110–120` computes a mean attack-event duration; the lineage census shows that is **Ho 2024's MTTC** (§3.3.2 item 8, p.20), and a second function of the same name (`:35–49`) divides total attack time by hosts compromised (`metric_census/B_lineage.md` §e). So the unowned finding is most likely *one name, several quantities* rather than a bug — classify against `mtdsim_intent_spec.md` before calling it anything (*to verify*). The disposition holds: the thesis reports the time to its first compromised host, computed by the chapter's analyser on both attackers, and never either inherited function; `metrics_semantics.md` §(a) and `project_context.md`'s "primary metric is internal MTTC" sentence are corrected when this brief lands.

### 3. The chapter 4 unit — heading placed

§4.5 *Instrumenting MTDSim* (`sec:instrumenting`), its own section after §4.4.4 (the metrics are not part of the join; one line to move under §4.4). Per metric: the field's name and acronym; its definition in the formalism's symbols where one applies; what it captures; why the cited metrics do not; the citation, or the reason it is new. For the two stealth metrics, §4.5 also states the detector it assumes (a rate threshold) and that a time-at-risk detector would read the slower attacker the other way (Hong 2018's rationale for ACD, "the longer the attack takes, the more likely it will be detected", p.40). Every introduced metric gets a hand trace (V1). §5.1's Metrics unit points to §4.5 only and loses "grouped by effectiveness and efficiency".

### 4. §5.2's shape — every float motivated by an APT property the literature review names

The motivation for each float is the property it shows, from the literature review's table of APT properties (`dissertation.tex` l.~3235: Cho, Alshamrani, NIST, Jalowski). That is the rule "motivated or cut", made checkable.

| Property (ch3) | Where §5.2 shows it | Metric |
|---|---|---|
| objective conditioning | Figure 5.1(a) | share of steps per tactic |
| strategic plurality | Figure 5.1(b) | runs leaving the commonest opening |
| stealth | **Figure 5.1(c)** and a Table 5.3 column — **new** | attack confidentiality; attack rate |
| what the field measures | Table 5.3 | ASP, NCR, MTTC |
| persistence | no float | campaign duration is an input (09 Aug); said in one clause, or in chapter 6 |
| adaptivity | §5.3.1, not §5.2 | attack actions blocked; recovery time |
| incentive rationality, learning | no float | at their inert defaults in the reported configuration; chapter 6 |
| MTD-scheme awareness | no float | ruled out of scope |

So the only gap in §5.2 is stealth, and it is the one Jin named. Nothing else is owed a float.

**Figure 5.1, three panels.**
- **(a) Heat map, in colour** (E8): tactics down the side, $c_1$–$c_4$ and $c_{\mathrm{agg}}$ across, **plus a baseline attacker column**. The baseline walks six activities, not tactics, so its column places each activity on the tactic that maps to that verb (§4.4.3), labelled as such. The exploit verb serves three tactics, so that cell is one merged cell across initial access, execution and privilege escalation. Dry-run (100 seeds, baseline activities with its per-vulnerability exploit rows counted once): lateral movement 31 %, discovery 23 %, the merged exploit cell 21 %, credential access 15 %, command and control 8 %, reconnaissance 2 %. **The seven non-action tactics are empty for the baseline** — the rows it has no vocabulary for, carrying about 40 % of most profiles' steps. This panel sets up (c).
- **(b) Bar chart** (E8): opening length on the x-axis, one colour, the share of runs that have left the commonest opening, profiles and baseline.
- **(c) Attack confidentiality against the detector's window** — **new**. x = the window *w* (a few seconds to a few minutes), y = the share of actions a detector that flags two actions within *w* would miss, one line per attacker (lines, because the points are correlated along *w* — Jin's rule). It shows every choice of *w*, so no constant has to be defended (E5), and it shows the finding honestly:

  Dry-run (100 seeds, 15 000 s, no defence; preliminary — for the ruling only):

  | *w* (s) | $c_1$ | $c_2$ | $c_3$ | $c_4$ | $c_{\mathrm{agg}}$ | baseline |
  |--:|--:|--:|--:|--:|--:|--:|
  | 5 | 0.80 | 0.80 | 0.82 | 0.72 | 0.78 | **1.00** |
  | 10 | 0.69 | 0.69 | 0.73 | 0.59 | 0.68 | 0.58 |
  | 30 | **0.48** | **0.48** | **0.56** | 0.37 | **0.46** | 0.19 |
  | 60 | **0.29** | **0.30** | **0.39** | 0.20 | **0.29** | 0.16 |
  | 120 | 0.11 | 0.12 | 0.17 | 0.06 | 0.11 | 0.09 |
  | 300 | 0.01 | 0.01 | 0.02 | 0.00 | 0.01 | 0.01 |

  **What it says:** against a detector that looks at tens of seconds to a couple of minutes, the APT attacker model leaves two to three times as many of its actions unflagged as the baseline; against one that looks at bursts under ten seconds, the baseline reads as the quieter, because its shortest activity takes 5 s while the profiles' drawn dwells can be shorter; beyond a few minutes they converge. *Quieter* therefore needs its timescale stated, and the text says it. **The ablation** (non-action tactics removed from the record) erases the margin at 60 s (0.11–0.13 against 0.16) but not at 30 s (0.25–0.30 against 0.19), so the August claim that the non-action tactics are *all* of the margin holds at the minute scale only; the sentence is scoped to that.

**Table 5.3.** The effectiveness group — ASP, NCR, MTTC (with the no-compromise share in its note) — and one stealth column, **attack rate** (actions per 1 000 s of active time; no parameter to defend). Dry-run: $c_1$ 21.4, $c_2$ 20.3, $c_3$ 16.2, $c_{\mathrm{agg}}$ 21.0, $c_4$ 28.7, baseline 28.4. *Active* time matters: over the whole horizon the baseline reads 19.6, level with the profiles, because under the targeted objective it stops when it takes the target (0.70 of the horizon on average). §4.5 declares the denominator and says why.

**The body, in order** (content points; Marc's prose): (1) campaign shape, 5.1(a); (2) not one script, 5.1(b); (3) on the field's metrics the model is slower and has reached less by the time limit, Table 5.3; (4) it acts at a lower rate and leaves more of its actions unflagged at the minute scale, 5.1(c) and the rate column — the non-action tactics that make it slower are what make it quieter, which is Alshamrani's "trades speed for evasion"; $c_4$, with the fewest non-action tactics, is level with the baseline, the mechanism showing. E10(i)'s method point is chapter 6's.

**Ceilings.** Observations of the no-defence arm; axis 5 stays NOT ADDRESSED (a declared detector, not a detection model in the simulator); in chapter 5 "leaves more of its actions unflagged by a rate detector" or "acts at a lower rate", never "less detectable"; the detector is declared and its opposite (time-at-risk) is named.

## Rulings owed (Marc) — one sitting

1. The verdict table (§1), row by row — especially: **ASP** over "ASR"; MTTC at the first host; Brown's *attack actions blocked* restored (the in-flight difference); the cuts.
2. Table 5.2's grouping — *attacker behaviour* / *effectiveness* (§1b).
3. The stealth pair: attack rate in Table 5.3 and attack confidentiality in Figure 5.1(c) — or one of them. And its framing: a declared rate detector, with the timescale stated.
4. Figure 5.1's baseline column: the mapped, merged-cell form (§4) — or a separate verb-level strip.
5. §1c: the retrospective cuts (divergence, breadth, *D*, disengagement, learning).
6. The download list (catalogue §c) — Jafarian 2014 and Hong & Kim 2016 first.

## Validation gate

Every Table 5.2 row has a Source that matches the catalogue verdict; every *does not exist* row has a §4.5 definition-and-why; *suppression* appears nowhere in the tex or floats; Figure 5.1 has three panels as ruled, in colour where ruled; Table 5.3 carries the stealth column at 1 000 seeds; each introduced metric has a hand trace; `metrics_semantics.md` and `project_context.md` corrected; bib entries added for every new citation (zhan2013, jafarian2015, cheng2014, pendleton2016 as used); build clean.

## Hard constraints

- The claim ceiling above. Numbers reach the page only through the analyser and a generator at the reported seed count; every figure in this brief is a dry-run (scripts in session scratch; the method is stated in each paragraph so the analyser can reproduce it).
- The field's name where the quantity is the field's; the difference stated where it is adapted; no name borrowed for a quantity it does not describe (the RI lesson).

## Reading list

- [`../sources/extractions/mtd_metric_catalogue.md`](../sources/extractions/mtd_metric_catalogue.md) — the verdicts and their evidence.
- `docs/thesis/tables/tab_5-1b_metrics.tex` — the comment trail of every prior ruling on Table 5.2.
- `docs/implementation/pipeline/ogasp/stealth_spacing_diagnostic.md` §2–§6 — the August stealth reading this supersedes in its numbers.
- `~/mtdsim-meeting-minutes/2026-09-22_supervisor_meeting.md` §4–§5 — Jin's words on Figure 5.1, Table 5.3 and metrics.
- `docs/thesis/dissertation.tex` l.~2120 (Table 3.1), l.~3235 (the APT properties table), l.~1011 (Alshamrani).

## Out of scope

The runs (corpus handoff); drawing Figure 5.1 (figure-family handoff, to this shape once ruled); the tex of Table 5.2 and §4.5's prose (after the rulings; the prose is Marc's).
