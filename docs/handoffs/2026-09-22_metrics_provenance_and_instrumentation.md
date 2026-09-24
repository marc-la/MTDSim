---
status: open                  # THE DESIGN, consolidated 2026-09-24 from the three passes of 23–24 Sep (history in git: f6c4a493, e2d634d9, 630d574e, 10ab99b6); implementation not started; four rulings owed (§8)
created: 2026-09-22
updated: 2026-09-24
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E3, §E4, E10(i)'s set-up; E8's Figure 5.1 fixes
companions: ../sources/extractions/mtd_metric_catalogue.md (the evidence behind every Source cell below; the six census tables in ../sources/extractions/metric_census/), ../workflows/terminology.md, 2026-09-22_ch4_overview_figure_family.md (draws Figure 5.1 to §4's design), 2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md (the analyser and the 1 000-seed runs), 2026-09-20_ch5_s52_s54_results_context.md (the chapter 5 wording bars)
---

# The metrics design: a source for every metric, a split of our own, and §5.2 made whole

## 0. The bar this design is built to

Jin, 22 Sep (E3): for every metric, the reference — "MTTC or NCR, especially if it's well-known ones" — and a new metric only with the full detail of how it is calculated and *why*, "it should explain something new"; *suppression* failed, as the attack success rate before and after pushed into one number. E4: the stealth readings go beside the numbers that read as "worse". E10(i): on the existing metrics the model looks slower and less successful, but it is much harder to detect — "which the methodology must explain well".

Marc, 23–24 Sep: strictly conventional — the field's name and its acronym where it has one, so a supervisor can place every metric in the field; never an invented name for the sake of it; no false attribution; anything we adapt or invent is **flagged and discussed in §4.5**; everything in §5.2 motivated or cut; the numbers may barely move — the labels are what place the work in the field; and our own split, not the effectiveness / efficiency split any MTD paper can supply.

**The test for this document:** read as the supervisor, every metric on the page either carries a citation to a paper that defines it, or points to §4.5, where its definition, what it adapts and why it is needed are written out.

## 1. The split: three metric classes, one per job in the results

The field's split (Cho's purpose axis, Table 3.1) sorts metrics by what they do for a *defender's* budget. This thesis is read from the attacker's side (E1), so its metrics are sorted by the question each answers about the attacker, and each class motivates a part of the results:

| Class (Table 5.2 row group) | The question it answers | Where it is read |
|---|---|---|
| **Attacker behaviour** | What does the attacker *do*? | §5.2, Figure 5.1 |
| **Attack outcome** | What does the attacker *achieve*? | §5.2, Table 5.3 (the no-defence reference); §5.3, as the quantity each defence changes |
| **MTD effectiveness** | What does a defence *do to* the attacker? | §5.3 |

Why three and not the two phases: the outcome metrics are read in both phases, so a phase grouping would split them or repeat them. Why "MTD effectiveness" keeps Cho's word: that one class *is* the field's effectiveness question, and naming it so is the tie-back; there is no efficiency class because the thesis does not model defence cost. §5.1's Metrics unit says this in a sentence (Marc's prose), replacing "grouped by effectiveness and efficiency, as Table 3.x groups the field's".

**Ruling owed (§8.1):** the three labels. Alternatives: *Behaviour / Outcome / Defence effect*; *What it does / What it achieves / What a defence does to it*.

## 2. Table 5.2 as it will read

Columns: Metric | Definition | Source. The Source column is the audit: a citation means the field defines it; "Section 4.5" means we adapt or introduce it and §4.5 says how and why. No acronym is invented; the field's acronym appears where the field has one.

| | Metric | Definition | Source |
|---|---|---|---|
| **Attacker behaviour** | Share of steps per tactic | the share of an attacker's steps that fall in each tactic, pooled over its runs; a step is a tactic entered (a phase entered, for the baseline attacker) | Section 4.5 |
| | Runs leaving the commonest opening | for an opening of *k* steps, the share of runs whose first *k* steps differ from the attacker's commonest *k*-step opening | Section 4.5 |
| | Attack rate | the attacker's actions per 1 000 s of its active time | Zhan et al.; Section 4.5 |
| | Attack confidentiality | the share of the attacker's actions taken while a detector that counts its recent actions is below its alarm level | adapted from Zaffarano et al.; Section 4.5 |
| **Attack outcome** | Attack success probability (ASP) | the share of runs in which the attacker compromises a database host (the targeted attack scenario) | Cho et al.; Zaffarano et al. |
| | Network compromise ratio (NCR) | the hosts compromised by the end of a run, over the network's 50 | Zhang; Ho |
| | Mean time to compromise (MTTC) | the mean time from the start of a run to its first compromised host, over the runs that compromise one | McQueen et al.; Zhang; Section 4.5 |
| **MTD effectiveness** | NCR reduction | $1 - \mathrm{NCR}_{\text{defence}} / \mathrm{NCR}_{\text{no defence}}$ | Zhang; Ho; the form of Alavizadeh et al.'s mitigation factor |
| | Attack actions blocked | the share of the attacker's actions that fail because a precondition is not met | adapted from Brown et al.; Section 4.5 |
| | Recovery time | the time from a disruption to the attacker's next compromise, as a multiple of its own mean gap between compromises with no defence | Section 4.5 |

Ten rows, from ten today: the four efficiency rows, *runs with no compromise* (now MTTC's note) and *suppression* (now NCR reduction) leave; the four attacker-behaviour metrics come in. Numbers: NCR reduction is the number `analyse.py:304` already computes (the 50 hosts cancel), NCR is hosts ÷ 50, ASP and MTTC are today's *target reached* and *delay*; only the stealth pair is new computation.

## 3. What §4.5 must discuss — the flags

Every metric that is not cited exactly as the field defines it. Three depths:

**A — introduced: full definition, and why it is needed** (no paper in the census has it; catalogue §(a)):
1. *Share of steps per tactic* — why: objective conditioning is claimed, and it is visible only in what the attacker does; no paper measures the composition of an attacker's own behaviour (every variety or unpredictability metric in the field measures the defender's configuration).
2. *Runs leaving the commonest opening* — why: strategic plurality is claimed, and the baseline attacker is one script; same absence.
3. *Recovery time* — why: adaptivity is the one APT property readable only under a defence; the field's recovery metric (MTTR) is the defender's; that the attacker must recover at all is Jafarian's point (a mutation forces reconnaissance to restart).

**B — adapted: the field's name, what differs, and why** (catalogue rows):
4. *Attack confidentiality* (Zaffarano 2015; relayed by Cho 2020 as "the degree of attack behaviors detected by a defender" and by Sengupta 2020 as the "ability to remain undetected"; already in Table 3.1). **The proxy, stated plainly:** the simulator has no detector, so no metric measures detection; what it records is everything the attacker gives a detector to see. The detector is declared: $D(t) = \sum_i e^{-(t-t_i)/\tau}$ over the attacker's past actions, every action weighing one, $\tau$ = 60 s (a detector that counts recent actions and forgets each over about a minute); an action is exposed when $D$, counting it, reaches the alarm level $\theta$; $\theta$ is swept on the figure's axis, so no alarm level is chosen. §4.5 must also say: $\tau$ is the one declared constant (swept in the appendix); a detector that counts time on the network instead would read the slower attacker the other way (Hong 2018's rationale for ACD, "the longer the attack takes, the more likely it will be detected", p.40); and why the reading is wanted — the APT attacker "trades speed for evasion" (Alshamrani 2019), slowing the rate of attack avoids triggering a defence (Ward 2018, §5.18), fast scanning is easy to detect (Jafarian 2015), and the three outcome metrics read only the speed side of that trade.
5. *Attack rate* (Zhan 2013, surveyed by Pendleton 2016 as a measure of an attack's *aggressiveness*). Differs: an attacker's own actions, not attacks arriving at a sensor; over its **active** time (start to its last action), because under the targeted attack scenario the baseline stops when it takes the target (at 0.70 of the time limit on average) and a rate over the whole limit would hide the difference. Why: it is the footprint attack confidentiality reads, with no assumption at all. The unit, for both stealth metrics: an action is one verb invoked — the baseline's per-vulnerability exploit rows count once; a tactic that invokes no verb adds time, not an action.
6. *Attack actions blocked* (Brown 2023, a count, Fig. 4; being "blocked by an MTD technique" is losing the connection to the host, to the service, or the user's access, §III-D). Differs: a share, not a count; Brown's are cut off in flight, these start after the change and find the precondition gone; and it also counts failures with no defence running (0.24, the attacker's own ordering), so §5.3.1 reads its change around a disruption.
7. *Mean time to compromise* — its checkpoint. The name covers at least five quantities in the lineage (McQueen's expected time, Zhang's time to NCR 0.8, Ho's mean event duration, Tay's time to breach, a second code function); here it is the time to compromise the **first** host, because the APT attacker model never reaches Zhang's 80 % (14–20 % by the limit) and takes the target in too few runs (5–17 %) to average over. The share of runs that compromise nothing is printed beside it. It is not the inherited `evaluation.py` quantity (§7).

**C — cited, one clause each:**
8. *ASP* is estimated as the share of runs; it is not Ho's ASR, which is hosts compromised per attempted action.
9. *NCR* is read at the end of the run, where Zhang uses it as the stopping rule.
10. *NCR reduction* carries §5.3 rather than ASP before and after, because the APT attacker model's ASP is 0.00 under most defences and cannot order them.

## 4. §5.2 — the section, float by float

**Its job:** show a general computer-science reader, with no defence running, that the APT attacker model walks a campaign the baseline cannot, goes many ways from one start, and is quieter — and put the field's numbers, which read it as the weaker attacker, beside the reason. Every float is motivated by a property of an APT attacker the literature review names (the properties table, `dissertation.tex` l.~3235); the properties with no float say why in one clause (persistence: campaign duration is an input; incentive rationality and learning: at their inert defaults; MTD-scheme awareness: out of scope; adaptivity: §5.3.1).

**Figure 5.1 — three panels** (shape mock: `data/misc/_viz/stealth_ch5_dryrun/fig51_shape_mock.png`, gitignored, 100 seeds, not house style).

| Panel | Metric | Property | The reader should leave with | Form (Jin, 22 Sep) |
|---|---|---|---|---|
| (a) | share of steps per tactic | objective conditioning | the four profiles weight one campaign vocabulary differently; the baseline attacker has no step in the seven tactics that take no action (26–47 % of the profiles' steps) | colour heat map; tactics down, $c_1$–$c_4$, $c_{\mathrm{agg}}$ and the **baseline attacker** across. The baseline's six activities sit on the tactic that maps to each (§4.4.3); the exploit activity serves initial access, execution and privilege escalation, which persistence separates, so each of the three cells carries the one shared value, marked, counted once. The no-action tactics are marked on the axis |
| (b) | runs leaving the commonest opening | strategic plurality | the model's runs part ways within a few steps; the baseline's open alike | bar chart, opening length on the x-axis (bars for proportions) |
| (c) | attack confidentiality | stealth | the model takes more of its actions below a detector's alarm, at every alarm level | lines against the alarm level (the points are correlated along it), one per attacker |

**Table 5.3 — the numbers.** Rows $c_1$–$c_4$, $c_{\mathrm{agg}}$ (under *APT attacker model*) and the baseline attacker. Column groups *Attack outcome*: ASP, NCR, MTTC (s); *Stealth*: attack rate (per 1 000 s). MTTC's note carries the share of runs that compromise no host (0.00–0.08). Caption: how to read the two groups, nothing more.

**The body** (content points; the prose is Marc's): (1) campaign shape, 5.1(a); (2) not one script, 5.1(b); (3) on the field's three metrics the model has reached less, and more slowly, by the 15 000 s limit, Table 5.3; (4) it acts at a lower rate and takes more of its actions below the alarm, 5.1(c) and the rate column — the tactics that take no action make it both slower and quieter, the trade Alshamrani names; $c_4$, with the fewest of them (26 %), reads with the baseline, and why is chapter 6's.

**Dry-run, for the ruling only** (today's 100-seed no-defence corpus; the reported numbers come from the analyser at 1 000 seeds): attack rate $c_1$–$c_3$ and $c_{\mathrm{agg}}$ 16–21 against the baseline's 28 ($c_4$ 29); attack confidentiality at an alarm of 2, 0.38–0.53 against 0.20 ($c_4$ 0.24). Observation for the prose: $c_3$'s runs mostly open alike (20–32 % leave the commonest opening from length 4). Scripts: `data/misc/_viz/stealth_ch5_dryrun/`.

**Cut from §5.2, with the reason on record:** profile divergence (the heat map shows it; its noise floor could not be failed); effective behavioural breadth (Cho and Jalowski use *unpredictability* for the defender's configuration; the baseline's value is fixed by construction; 5.1(b) carries plurality); the detectability level *D* as a metric in its own right (three hand-set magnitudes and no field name — it survives as the detector inside attack confidentiality, at one constant); disengagement and learning (inert in the reported configuration); path entropy, coverage curves, deepest stage (killed or saturated earlier); the 60 000 s extension (the 15 000 s limit stands).

**Wording ceiling:** observations of the no-defence runs; "acts at a lower rate", "takes more of its actions below the alarm", never "less detectable" in chapter 5; the stealth criterion stays NOT ADDRESSED — a declared detector, not a detection model in the simulator.

## 5. §5.3 — what changes on its floats

Labels only; no number moves.
- *Suppression* → **NCR reduction** on Figures 5.3 and 5.4 (captions, axis labels) and Tables 5.4 and 5.5 (headers); `tools/_ch5_style.py` and the ch5 generators' strings. `python tools/term_screen.py census suppression` lists every site (float files and chapter text).
- Table 5.4's columns → NCR reduction, NCR, MTTC (with the no-compromise share), ASP, attack actions blocked.
- Figure 5.2(a)'s caption names *attack actions blocked*; 5.2(b)'s names *recovery time*.
- E6's interval line chart: Jin asked for "the change in attack success rate against interval"; it will be **NCR reduction** against interval, because ASP is floored under defence. Say so to Jin before week 9 (E11).

## 6. The supervisor's questions, and where the page answers them

| Question | Answer, and where |
|---|---|
| "Where is this metric from?" | Table 5.2's Source column; §4.5 for every flagged row |
| "What is NCR reduction — is that yours?" | NCR is Zhang's and Ho's; the with-and-without form is Alavizadeh's mitigation factor; the number is the old *suppression*, renamed (§3, C10) |
| "Your ASR isn't Ho's." | It is ASP, Cho's, estimated over runs (C8) |
| "MTTC to what?" | the first host, and why (B7) |
| "How can you measure stealth with no detector?" | we measure the footprint (attack rate) and what a declared detector makes of it (attack confidentiality), across every alarm level; the claim is bounded to that (B4, B5; §4 wording ceiling) |
| "Why 60 s?" | the one declared constant, swept in the appendix |
| "Isn't a slow attacker *more* detectable?" | to a detector that counts time on the network, yes (Hong 2018); ours counts recent actions, and §4.5 says so (B4) |
| "Your model is worse." | slower and quieter for the same reason — Table 5.3 beside Figure 5.1(c) |
| "Why does $c_4$ look like the baseline?" | fewest no-action tactics; chapter 6 |

## 7. The internal-MTTC finding (owned here)

`evaluation.py:110–120` computes a mean attack-event duration, which is **Ho 2024's MTTC** (§3.3.2 item 8, p.20); a second function of the same name (`:35–49`) divides total attack time by hosts compromised (`metric_census/B_lineage.md` §e). So the long-unowned finding is most likely one name used for several quantities, not a bug — classify against `mtdsim_intent_spec.md` before calling it anything (*to verify*). The thesis reports neither; `metrics_semantics.md` §(a) and `project_context.md`'s "primary metric is internal MTTC" sentence are corrected when this lands.

## 8. Rulings owed (Marc)

1. The three class labels (§1).
2. The §4.5 flag list (§3) as complete — anything to add or drop.
3. $\tau$ = 60 s as the one declared constant, with its sweep in the appendix.
4. Bib entries to add, each verified against the census before entry: **zhan2013** (IEEE TIFS 8(11), DOI 10.1109/TIFS.2013.2279800), **pendleton2016** (ACM CSUR 49(4), DOI 10.1145/3005714; confirm the published wording), **ward2018** (held: `sources/methodology/ward2018_mit_survey.md`), **jafarian2015** (IEEE TIFS 10(12)). Sengupta 2020 is optional (Cho already relays the same reading).

*Ruled 2026-09-23/24:* ASP, NCR, MTTC at the first host; suppression → NCR reduction, cited; Brown's name for attack actions blocked; recovery time and the stealth pair defined in §4.5; attack confidentiality with no acronym, and *D* as its detector; the efficiency rows, divergence, breadth, disengagement and learning cut; Figure 5.1 as three panels; general and targeted attack scenarios (commit d3d0bfcd).

## 9. Implementation, in order

1. Bib entries (§8.4).
2. The analyser: attack rate and attack confidentiality on both attackers (the dry-run scripts are the reference implementation); rename the output keys.
3. Table 5.2 regenerated from §2 (born generated, as its comment trail asks).
4. Figure 5.1 redrawn to §4 (figure-family brief); Table 5.3 regenerated with the stealth column.
5. §5.3's labels (§5), until the suppression census reads zero.
6. §4.5's content points in the tex comment refreshed to §3 (Marc dictates the prose); §5.1's Metrics sentence (Marc).
7. `metrics_semantics.md`, `project_context.md` (§7).
8. The 1 000-seed numbers through the analyser; build clean.

## Validation gate

Every Table 5.2 row's Source matches the catalogue verdict; every flagged metric has its §4.5 paragraph; the suppression census reads zero in prose and floats; Figure 5.1 has its three panels; Table 5.3 carries the stealth column at 1 000 seeds; every citation resolves; build clean.

## Reading list

- [`../sources/extractions/mtd_metric_catalogue.md`](../sources/extractions/mtd_metric_catalogue.md) — the verdicts and evidence.
- `docs/thesis/tables/tab_5-1b_metrics.tex` — the table this replaces, and its comment trail.
- `~/mtdsim-meeting-minutes/2026-09-22_supervisor_meeting.md` §4–§5.
- `docs/thesis/dissertation.tex` l.~2120 (Table 3.1), l.~3235 (the APT properties), l.~1011 (Alshamrani), §4.5's placeholder.
