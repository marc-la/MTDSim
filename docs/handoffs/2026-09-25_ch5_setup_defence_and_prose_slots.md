---
status: open                  # 2026-09-25: audit + slots delivered; every item below is a PROPOSAL awaiting Marc's ruling; nothing applied to the tex
created: 2026-09-25
companions: ../workflows/evaluation_conventions.md (§j, §k added in the same commit — the guidance this file applies), ../workflows/figure_table_conventions.md, ../workflows/voice.md, ../workflows/drafting_pipeline.md
---

# Chapter 5 — §5.1 defended row by row, and the connective prose §5.2–§5.3 owes

**Goal.** (1) Every value §5.1 and Table 5.1 state is strictly defensible and
strictly conventional, and §5.1 sets up every object §5.2–§5.3 later reads.
(2) The prose that chapter 5 still owes — the chapter preamble, the text
around §5.2's floats, the §5.3 preamble, §5.3.1–§5.3.3 — has a slot plan
(job + facts + ceiling, no content), grounded in the field's conventions and
the genre literature, so Marc can dictate it.

**Marc's brief (2026-09-25, dictated):** "make sure 5.1 sets up for everything
else that follows … all these values that we state in the experimental setup
… defensible … strictly conventional … seek some guidance on best formatting
this … how do you defend your experimental setup. The structure is nice and
tight already … Table 5.1 is very tight." Then: "seek guidance on how you
structure evaluation prose … the preamble … is there a text that we need to
say after [Figure 5.1] (a)(b) and Table 5.2 and Figure 5.2 … what do the
captions need to say … 5.3 there's a placeholder preamble … 5.3.2 and onwards
… common pitfalls … everything should be strongly connected."

**Standing constraints.** §5.1's structure (the five run-in units) and Table
5.1's shape are ratified and liked — nothing here restructures them; every
§5.1 proposal is a value, a citation or a clause. The prose is Marc's (the
drafting pipeline; slot-generator drafting): this file gives slots, never
sentences. Numbers quoted below are provenance at 100 seeds; none may be
transcribed.

---

## Part A — Table 5.1 and §5.1, row by row

**The defence rule these rows are tested against** (evaluation conventions
§c, register E5; the formatting guidance behind it is conventions §k): every
value carries a citation to a study that ran it, or is the simulator's
default with a pointer to where chapter 2 states it, or is argued in §5.1's
prose. A value with none of the three is the gap an examiner finds first. A
default is itself only as good as its source, so a default should be cited to
the released code where one exists.

Verdicts: **holds** · **fix** (a fact or citation is wrong, and the evidence
decides it) · **Marc** (a choice, with a recommendation).

| # | Row / sentence | Value | Evidence checked | Verdict | Proposal |
|---|---|---|---|---|---|
| A1 | Hosts, levels, endpoints | 50, 4, 5 | Zhang Table 2 Net2 = 50 / 0.052 / 5 / 4 (`zhang2023.md` Z-EVAL-07); `TimeNetwork` defaults 50/5/4 (`time_network.py:11`) | **holds** | — |
| A2 | Subnets | 8 | `TimeNetwork` default 8; §2.2.1 states it ("By default … eight subnets"); **and** the lineage's released experiment driver defaults to 8 (below, A3) | **holds; can be cited** | Add `\citep{tay2024code}` after 8 (A3's evidence). Then no network value is uncited. |
| A3 | Target; §5.1 Network ¶ "Every value is the simulator's own default … but one: the target set, narrowed from five database hosts to two" | two database hosts, deepest level | **The [3b] open since 2026-09-18 is answered by evidence, and the sentence is wrong as worded.** The *class* default is 5 (`time_network.py:12`), but the experiment driver released with the simulator, `experiments/run.py::execute_simulation`, defaults to `total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4, target_layer=4, total_database=2, terminate_compromise_ratio=0.8` — verified at the lineage's commit a23b5dda (23 Mar 2023, the time-domain simulator's experiment code; endpoints 3 then) and at **both commits `tay2024code` pins (f13ed49, e6c13c6)**, and still so when the file was deleted here (e5935aba^). This repo's `GEOMETRY` copied it (`baseline/BASELINE.md` l.90: "defaults from the deleted driver's `execute_simulation`"). So two is the lineage's own run configuration, not a narrowing. | **fix** | Re-word the Network unit's second sentence so it says every value is the default of the configuration released with the simulator, cited `\citep{tay2024code}` — and delete "narrowed from five … to two". Table 5.1's Target row takes the same citation. The reason for two is then provenance, which is the strongest defence available and needs no argument. (Marc's words; one sentence.) |
| A4 | Arm | baseline; c1–c4; c_agg | ch2 §2.2.3; ch4 | **holds** for what it lists — but see B4: a seventh arm (the verdict-blind control) is run and used in §5.3.1's prose and is not listed | B4 |
| A5 | Attack scenario | targeted `\citep{brown2023}` | Brown Scenario 2 (B-ATK-01): "compromise a specific host" | **holds** | — (Brown's is one target host; ours two — A3's citation covers the count) |
| A6 | Condition | no defence; seven alone `\citep{brown2023}`; random; alternative `\citep{zhang2023}`; MTDShield `\citep{tay2024}` | Brown ran each mechanism alone against none (p.6), but **six** of the seven (no complete topology shuffle, `brown2023.md` l.50) | **holds, low risk** | The citation sits after "alone", so it sources the one-at-a-time design, which is right. Leave, or move it to "no defence; each … alone" as one design clause. Not worth a ruling unless Marc wants it tidy. |
| A7a | Interval 50, 100 s | `\citep{zhang2023}` | Ho also ran 50; 100; 200 (`ho2024.md` H-EVAL-01) and **Table 2.2 says so**; the 200 s cell cites both, the 50 and 100 cells cite Zhang only | **fix** | Add `ho2024` after 50 s and 100 s. The table then agrees with Table 2.2, which it points to in its caption. |
| A7b | §5.1 Defence ¶ "a range from 50\,s, the shortest the lineage has run" | 50 s | **False against Table 2.2**, the table the same sentence cites: Brown's interval is uniform on 1 000–5 000 ms, 1–5 s (`brown2023.md` B-TRIG-01). An examiner reads the two tables side by side. | **fix** | Scope it: "the shortest Zhang and Ho ran" (both in seconds on the time-domain simulator). Or drop the superlative and cite: "from 50 s \citep{zhang2023, ho2024}". |
| A7c | Interval 500, 1 000, 2 000 s | uncited; argued "so that every effect can be read against the interval" | Marc 2026-09-23: 2 000 s is a range end, not a precedent. The argument given justifies *sweeping*; it does not justify *these levels*. | **Marc** | Two conventional facts defend the levels without fitting them to a result: **(i)** they are the 1–2–5 series, the standard way to space a factor over orders of magnitude, even on the logarithmic axis every §5.3 figure uses (source: conventions §k); **(ii)** the top is ten times the longest interval the lineage ran (200 s), so the sweep adds one decade above the lineage's range. Recommend both, as one clause in §5.1 ("on a 1–2–5 series, from 50 s … to ten times the longest the lineage ran") and nothing in the table. **Not** recommended: tying 2 000 s to §4.5's growth-rate window. The window was sized to the interval, so the argument runs in a circle. |
| A8a | Timing distribution: near-periodic | points to §2.2.2 | §2.2.2 states it at 200 s only ("200 s plus a small exponentially drawn term"); the code draws interval + Exp(0.5) at every interval (`mtd_operation.py:115,160`) | **holds, minor** | §2.2.2 could read "the interval plus …". Optional. |
| A8b | Timing distribution: exponential, same means `\citep{zhang2023}` | Zhang §4.3.4 (Z-TIM-01) | **Its result is reported nowhere** in chapter 5 or any appendix (grep: the only "exponential" after §5.1 is the dwell family, App. C). A declared variation whose result is never shown is the corpus failure conventions §i names (Bland's exploration rate). The data exist (`run_corpus.py` group `regime`, 200 s, nine defended conditions). | **Marc — blocking** | Recommend **report it**: one small appendix table (NCR reduction at 200 s, both attackers, both distributions, nine conditions) and one body sentence in §5.3.3 saying whether any ordering changes. It is cheap, and it answers the question a reader of Zhang asks, since Zhang's design is the exponential. The alternative is to delete the row and the caption clause, but then the near-periodic default goes unexamined. |
| A8c | Table 5.1 caption: "the timing distribution, which governs the interval, the deployment durations **and the delay after an interrupt**" | — | "The delay after an interrupt" is the confusion penalty, and its chapter 2 home (§2.2.3) is still a placeholder (item (i)). The caption uses an object the reader has not met. | **fix** | Either land §2.2.3's placeholder item (i) first, or cut the clause to "which governs the interval and the deployment durations". |
| A9 | Deployment duration | four Zhang's, three the simulator's | `constants.py` MTD_DURATION; provenance IS-TIM-03; §2.2.2 says so | **holds; can be cited** | The three that are the simulator's take `\citep{tay2024code}`, like A2, A3 and A17, so that no value in the table is left as a bare "default". Zhang's four already cite Table 3, p. 34. Every duration there, like the interval, carries a 0.5 s spread, which chapter 2 describes as a "small exponentially drawn term" for the interval only. Fine as it stands; noted in case an examiner asks. |
| A10 | Time limit; early stop | 15 000 s `\citep{ho2024}`; target or > 80 % `\citep{zhang2023}` | Ho H-PAR-08 (unitless; Table 2.2's caption carries the unit); Zhang l.420 | **holds** | — (the inherited 80 % stop under the targeted scenario is declared, not yet classified against the intent spec; that is §4.5's and the README's, not this table's) |
| A11 | Seeds | 1 000, uncited; "argued in the text" | **Two justifications now compete.** §5.1 Runs argues "ten times the 100 runs per condition of Zhang"; §4.5.4 argues "the number Arcuri and Briand recommend". The s45 record flagged the duplication (`11_statistical_analysis.md` l.176). Arcuri & Briand's TR wording is "at least n = 1 000 times" *per artefact*; here each seed is a new network, so one run per network (s45 verdict: "partly"; the STVR wording is still unchecked). | **Marc** | Recommend: the **reason** lives in §4.5.4 (Arcuri) and nowhere else. Table 5.1's row takes `\citep{arcuri2014hitchhiker}` after 1 000 (a cited recommendation, the same defence rule as a cited run). §5.1 Runs keeps the Zhang comparison only if Marc wants the lineage anchor; it is a comparison, not a reason, so it can go. |
| A12 | §5.1 **Metrics** unit | "metrics either adapted from earlier evaluations **or introduced here**, which are outlined in Table 4.3. The defences are ranked on the NCR reduction." | Stale since §4.5 landed: the metrics are introduced and defined in §4.5, not here. The ranking is Scott–Knott on mean hosts compromised per seed, "which orders them as NCR reduction does" (§4.5.4), so "ranked on the NCR reduction" is half the statement. Conventions §a: a setup holds only what the model section did not already carry. | **fix / Marc** | Cut the unit to one pointer sentence (the metrics and the ranking are §4.5's), or cut the unit entirely and let Table 5.1's Metrics row carry the pointer. Recommend the one sentence, since the unit order (network, attacker, defence, metrics, runs) is the "moving parts" frame Marc ruled. |
| A13 | §5.1 **Runs** unit: "Differences are reported as effect sizes with 95 % confidence intervals." | — | **False as worded** (s45 record l.175): the chapter reports means with normal-approximation intervals, NCR reduction and time lost with bootstrap intervals, and ranks. Cliff's δ exists only in `numbers.json`. "On the same seeds, so every attacker starts on the same 1 000 networks" duplicates §4.5.4 ("every cell uses the same seeds, and a seed fixes the network"). | **fix** | Replace both with a pointer to §4.5.4. What survives in the unit: the run count and, if kept, Zhang's comparison (A11). |
| A14 | Caption: "Arm, condition and deployment interval are run in every combination" | — | The no-defence cell is interval-independent and run once (flagged 2026-09-18, left). | **holds** | Leave; no number is affected. |
| A15 | Condition: the random and alternative execution schemes | two of chapter 2's three | Table 2.5 (`tab:deployment-strategies`, tex l.829) lists a third proactive scheme, **simultaneous**, which no row runs, and **no reason is recorded anywhere** (grep over the tex, `implementation/`, `handoffs/`). Zhang ran all three and reports simultaneous as the better scheme at his longer intervals ("the Simultaneous scheme performs better for longer intervals (150, 200)", `evaluation_anatomies/zhang2023.md` l.57). Dropping, without a reason, the scheme the lineage found best at long intervals is the subset an examiner queries (van der Kouwe A2; Rossow B.3). Its released interval is 700 s, not 200 s (`constants.py` MTD_TRIGGER_INTERVAL). | **Marc — blocking** | **(a)** Run it on the sweep: about 3 600 runs at 100 seeds, one more line in Figure 5.6 and one more row in each table. **(b)** Give the reason in one clause of §5.1's Defence unit (for example, that at a shared interval it deploys all seven at once, so it is not comparable with a one-per-interval scheme). Recommend **(a)**: the runs are cheap, and (b) is an argument an examiner can push against, whereas a measured line cannot be argued with. |
| A16 | Run type and stopping condition | Table 5.1 Time-limit row | STRESS-DES 4.1: "Report if the system modelled is terminating or non-terminating … For terminating systems state the stopping condition." Kurkowski et al., on network DES studies, found 58 % did not say (STRESS paper p. 57). Rossow C.4: "describe why the analysis duration they chose suffices". The table states the stopping events. The word *terminating*, the absence of a warm-up, and the share of runs that reach the limit are stated nowhere. | **Marc, minor** | One clause, in the Runs unit or the Time-limit row: each run is a terminating simulation whose stopping events are fixed before it starts, so no warm-up period applies (Law 2015 §3; Currie & Cheng 2016 §4). The share of runs ended by the time limit, per attacker, belongs in §5.2 beside Table 5.2 (it is the NCR cut-short fact already owed there, slot S2-c). |
| A17 | Timing distribution: near-periodic | uncited | STRESS 3.3 asks how a distribution was selected "above other candidate distributions". The near-periodic draw is the released simulator's (`MTD_TRIGGER_INTERVAL = (200, 0.5)` at `tay2024code`'s commit f13ed49, verified). | **fix** | Cite `\citep{tay2024code}` after "near-periodic", the same route as A2 and A3. The exponential then reads as Zhang's stated design, run beside the released default. |

**What A1–A17 amount to.**
- **Wrong, and fixed by evidence:** A3, A7a, A7b, A13.
- **Uncited, but a citation exists:** A2, A3, A17, all to `tay2024code`, the released configuration.
- **Stale against §4.5, so §5.1 repeats the method chapter:** A11, A12, A13.
- **Declared but never reported:** A8b.
- **A roster subset with no reason:** A15.
- **A range whose levels need defending:** A7c.

When these land, every value in Table 5.1 is either cited or argued in one clause of §5.1, and the only argued values are the three intervals above 200 s.

**The table's form needs no change.** STRESS-DES Table 5 is the reporting standard's own model. It sets a *data source* per row, and its sources mix a citation, an observation and "expert opinion". E5's citation after each value, with the caption naming the other kinds of source, is the same idea in less space (conventions §k). Once A2, A3 and A17 land, the caption's "an uncited value is the simulator's default" is true of **no** row. The clause can then shrink to "an uncited value is argued in the text", which is the stronger claim.

---

## Part B — does §5.1 set up what follows?

The test (evaluation conventions §a; the ch5 antecedent rule): every object a
§5.2–§5.3 float or sentence uses is declared in chapters 2–4 or §5.1, or at the
head of the section that first uses it. Objects that §4.5 now declares are
marked as such.

| # | Object used downstream | Where used | Declared? | Proposal |
|---|---|---|---|---|
| B1 | **200 s as the reference interval** (Table 5.4 ranks and the other metrics at 200 s; the exponential variation at 200 s) | Table `tab:eff-cross-arm`; Table 5.1 caption | Used, never declared as the reference or given a reason | One clause, §5.1 Defence unit or §5.3 head: 200 s is where one interval is tabled, because it is the longest Zhang ran, Ho's comparison interval (`ho2024.md` H-EVAL-03) and the tick MTDShield was trained at (App. E, "trained at one decision tick"). Three cited reasons; none is results-fitted. |
| B2 | **2 000 s for §5.3.1** | §5.3.1 head, Fig. 5.3 | §5.3.1 states it; the reason is §4.5's window ("so the growth rate is read at that interval only") | Keep it at §5.3.1's head (first use), as a pointer to §4.5. No setup change. |
| B3 | **"The APT attacker model" = c1–c4 pooled** in every §5.3.2 float; four times the runs; c_agg is excluded because it is its own profile, not an average | Figs 5.4; Tables 5.3, 5.4 captions | Captions only. The 8j-3 record: "Pooling is still owed at the §5.3 head." | §5.3 preamble, one sentence (slot P3 below). |
| B4 | **The verdict-blind control** ("the same attacker with the failure matrix replaced by the identity") | §5.3.1's head (live prose) | Not in Table 5.1's Arm row. Its scope is wrong in the prose: it was run under **IP shuffle and OS diversity only** (`run_corpus.py` group `blind`), and the prose says "under the seven mechanisms". Its result appears in **no float**: the rebuilt Figure 5.3 (R1–R3) does not use it. The sentence also uses *token*, *routes* and *identity*, which the chapter's frame bars (results-context §5). | **Marc — blocking.** **(a)** Report it: compute time lost for the blind arm on its two mechanisms (the `disruption.py` path exists), add it to Table 5.1's Arm row with its scope, and report one sentence. This is the only instrument that separates adaptivity from mechanics, so chapter 6's property-4 row needs it. **(b)** Cut the sentence and the arm. Recommend **(a)**. A declared control that is never reported is the same failure as A8b, and dropping it silently weakens property 4. |
| B5 | Exponential timing | — | See A8b | — |
| B6 | **Deployment saturation below 200 s** (a deployment takes 20–110 s; two on one layer cannot overlap, §2.2.2; at 50 s the service mechanisms complete ~148 of 300 called) | the left end of every §5.3.2–5.3.3 line | The by-construction half is in chapter 2 and Table 5.1 (durations against intervals); the counts are measured | Body sentence in §5.3.2, as the 8j-2 record already rules. It is a construction fact (results-context §3, rule 2), so it belongs in the results and not in §5.1. |
| B7 | Detector, alarm level, opening, step, cell, NCR reduction, time lost, Scott–Knott ESD, Spearman ρ | §5.2, §5.3 floats | **§4.5 declares all of them** | None. Captions should point to the *subsection* (e.g. `subsec:metrics-statistics` for the ranking), not to §4.5 as a whole. |
| B8 | **The confusion penalty**, and what a host-layer against a service-layer rewrite takes from the attacker | Table 5.1 caption (A8c); §5.3.1's reading (R2: "how long an attacker stays down follows the mechanism") | §2.2.3 is still a placeholder | Land §2.2.3's placeholder before §5.3.1 is dictated. §5.3.1's by-construction sentences depend on it. |
| B9 | **Table order in §5.3**: Figure 5.4's caption says "Table `tab:eff-interval-values` lists them", but that table is input **after** §5.3.3's two figures, and the 200 s ranking table (`tab:eff-cross-arm`) sits in §5.3.2 | tex l.~7495–7625 | The 8j design pairs the headline with the values table and puts the 200 s table in the depth. The inputs are the other way round. | **Check with Marc:** move `tab_5-3-2c` (values) into §5.3.2 and `tab_5-3-2d` (200 s ranks and metrics) into §5.3.3. Or rule the current order deliberate. |
| B10 | §5.1's Attacker unit hand-off: why two attackers are run | — | Cut from §5.1 on 2026-09-18, and owed by the chapter preamble since then | Preamble slot C2 below. |

---

## Part C — the slot plan for chapter 5's owed prose

**How to read a slot.** Each slot is one sentence, unless marked otherwise.
- **job**: what the sentence does.
- **facts**: what it may use. Numbers are 100-seed provenance from the named record, never values to transcribe.
- **ceiling**: what it must not say.
- **float**: how it refers to the float.

The paragraph-level rules come from conventions §j (added in this commit) and
results-context §3 (retired; `git show 7435c315^:docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md`).
A paragraph opens on the finding and cites the float in parentheses. The only
"because" allowed is a reason true by construction. An exception is marked,
not explained. The last sentence hands the next section its question.

**Budget.** The chapter has 12 units, about 3 000 words, and floats are
outside the count. §5.1 stands at about 258. The owed prose below comes to
about 1 300, which leaves slack; spend it on nothing.

### D0 — Chapter 5 preamble (one paragraph, ~100 words; replaces the placeholder at tex l.~5663)

| Slot | Job | Facts | Ceiling |
|---|---|---|---|
| C1 | Link from chapter 4 to this chapter. | Chapter 4 built the APT attacker model; this chapter runs it against MTD. | No result. No "validate". No layer number. |
| C2 | Why two attackers are run. This is the sentence §5.1 gave away on 2026-09-18 (B10). | \ref{sq:evaluate}: MTD's performance against the model *compared with the simulator's baseline attacker*. The baseline attacker is the one the lineage's evaluations ran (ch3 §3.3). | Not "realistic". Nothing about real APTs. Refer to SQ3 by reference; do not restate it. |
| C3 | The order, and the reason for it. | §5.1 declares the experiment once. §5.2 runs both attackers with no defence, so the attacker is described apart from any defence and every later effect has its reference. §5.3 runs them under MTD, with the baseline attacker as the reference line: one deployment, then the interval sweep (the headline), then mechanism by mechanism (the depth). | Name what each section *reads*, never what it finds (Reti's stale-roadmap failure, conventions §i). Keep the signposting functional (voice §h): what each part does, not "in this chapter we will". |
| C4 | Where the reading goes. | Chapter 6 interprets what this chapter reports, section by section (Tay's mirror, conventions §h). | One clause. It may merge into C3. |

### D1 — §5.2, around Figure 5.1, Table 5.2 and Figure 5.2 (four short paragraphs, ~300 words; replaces the placeholder)

**Order.** Head, then one paragraph per float in float order (Figure 5.1, Table
5.2, Figure 5.2), and the hand-off closes the last paragraph. The takeaways are
the ratified T1–T4 (results-context §8a, §8i, §8i-5), read at 1 000 seeds.

| Slot | Job | Facts | Ceiling / float |
|---|---|---|---|
| S2-h1 | The section's question. | What the APT attacker model does with no defence running, beside the baseline attacker on the same networks. | Not "validation". Not "realistic". |
| S2-h2 | What is read, and the register. | The attacker-behaviour and attack-outcome metrics of §4.5 (`subsec:metrics-behaviour`, `subsec:metrics-outcome`), with no defence. These are observations of the model; chapter 6 draws the verdict. | Define nothing here; §4.5 has. |
| S2-a1 | T1, claim first. | The model spreads its steps over many tactics, a large part of them dwell-only (ch4's word). The baseline attacker's steps fall on six verbs. | Float: "(Figure 5.1a)". Say nothing about why. |
| S2-a2 | T2. | The four profiles weight that campaign differently. Name the one contrast the reader can see without a legend hunt. | No ranking of the profiles as better or worse. |
| S2-a3 | T3, plus one by-construction clause. | The model's runs part ways within a few steps; the baseline's open alike to length 4, which is its fixed order (ch2). An opening of length 1 is zero for every attacker, since every run opens at its entry. | Float: "(Figure 5.1b)". Never "unpredictable" (Cho's word, which the thesis retired). |
| S2-a4 | The exception, marked and not explained. | $c_3$ sits beside the baseline attacker. | No reason given. The reason, if any, is chapter 6's. |
| S2-b1 | T4, the reference. | With no defence the model compromises fewer hosts, later and at a lower rate than the baseline attacker (Table 5.2's four columns, named as the table names them). | Float: "(Table 5.2)". Do not restate the cells; give one magnitude at most, as a ratio. |
| S2-b2 | By construction: why the pace differs. | The model's pace is set by the dwell times chapter 4 declared (`subsec:dwell-times`). | Not "because it is stealthier". |
| S2-b3 | The cut-short fact (owed 2026-09-20; A16). | A targeted run ends at its target, so the baseline attacker's NCR is cut short in the share of runs it wins (ASP 0.58), and it still reaches more hosts. **"NCR is lower because ASP is lower" was checked and is not upheld** (8i-5). Add the share of runs ended by the time limit, per attacker. | — |
| S2-b4 | The attack-rate concession, owed from §4.5 (its round-2 cut). | A tactic with no mapped action adds time only; an action whose precondition is unmet fails before it runs. | One clause. Its home is here, where the rate is first read. |
| S2-b5 (optional) | $c_{\mathrm{agg}}$ is its own profile. | The attack graph before it is partitioned, not an average; a cold reader read ASP 0.17 above every profile as a contradiction (8i-5). | Or put it in Table 5.2's caption (see D5). |
| S2-c1 | Attack confidentiality, as ONE observation with the rate. | The model keeps more of its actions below the alarm than the baseline attacker does across the run; $c_4$ keeps the fewest. §4.5 already says the reading holds only for a detector that counts actions, so a lower rate stays below it by construction. | Float: "(Figure 5.2)". Never "stealthy", "evades detection" or "undetectable". Never as a second piece of evidence beside the rate (8i). |
| S2-c2 | **Owed ruling (8i-5, examiner's objection 1):** the margin rests on the dwell-only action rule. | Counting dwell-only steps as actions brings the profiles level with the baseline attacker. | Marc rules: state it here as a concession, or carry it in ch6's limitations. It must appear in one of the two. |
| S2-close | The hand-off. | These no-defence runs are the reference that every effect in §5.3 is a difference from. | One sentence. |

### D2 — §5.3 preamble (one paragraph, ~120 words; replaces the placeholder)

| Slot | Job | Facts | Ceiling |
|---|---|---|---|
| P1 | The object changes. | The defences are now what is evaluated: each against the APT attacker model, with the baseline attacker drawn as the reference in every float. | — |
| P2 | The reference. | Every effect is a difference from §5.2's no-defence runs of the same attacker, on the same seeds, read as NCR reduction (`eq:ncr-reduction`). | Never "baseline" for the no-defence runs (conventions §f2). |
| P3 | Pooling (B3). | In §5.3's figures and tables "the APT attacker model" is $c_1$–$c_4$ pooled with equal weight, so its cells hold four times the runs. $c_{\mathrm{agg}}$ is its own profile and appears beside them in §5.3.3. | — |
| P4 | What counts as a separation: criteria before results (voice §c9; conventions §e, He's form). | An effect is separated from zero when its 95 % interval excludes zero (the grey text of Table 5.3); defences in one Scott–Knott group are not told apart (`subsec:metrics-statistics`). | Do not re-define the test; point to §4.5.4. |
| P5 | The order, and the reference interval if §5.1 does not carry it (B1). | §5.3.1 reads one deployment, §5.3.2 the interval sweep, §5.3.3 the mechanisms and strategies. 200 s is where one interval is tabled. | May merge into P1 if the chapter preamble's C3 already names the three. |

### D3 — §5.3.1 Response to disruption (~250 words)

**The head paragraph stands in DRAFT and needs three repairs.** It is session-drafted, ratify on read.
- **(i) The control (B4):** its scope is two mechanisms, not seven, and it is reported in no float. Rewrite it on Marc's ruling, or cut it.
- **(ii) The frame:** *token*, *routes* and *identity* are banned surface words (results-context §5). The control is stated in chapter 4's terms: the failure matrix's rows are ignored and the base weights route every step.
- **(iii) "grouped by the layer each rewrites":** the rebuilt Figure 5.3(c) is per mechanism.

| Slot | Job | Facts (R1–R3, ratified 2026-09-24; 8g-5) | Ceiling / float |
|---|---|---|---|
| S31-h | Why here, which interval, and the control. | Adaptivity cannot be read from the no-defence runs. 2 000 s is the interval over which §4.5 reads the growth rate. At 200 s the next deployment lands before the last is recovered from, so one sentence reports it. | Keep only what B4's ruling leaves. |
| S31-a | R1. | A deployment knocks each attacker down: its compromise rate drops when the deployment completes (six of seven mechanisms per attacker). | Float: "(Figure 5.3a, b)". |
| S31-b | The exception. | User shuffle knocks neither attacker down (credentials are disrupted about 0.1 times per run at 2 000 s). | Mark it; do not explain it. |
| S31-c | R2. | How long an attacker stays down follows the mechanism: after IP shuffle the model is still below its level about 1 000 s on, while the baseline attacker recovers within one bin; after service diversity it is the reverse (baseline at 72 % at 1 250 s; model near its level by about 700 s). | Say "follows the mechanism", not "the model is more resilient". |
| S31-d | By construction: what each rewrite takes (**needs §2.2.3's placeholder landed**, B8). | A host-layer rewrite takes the attacker's connection to the host; a service-layer rewrite takes the service. | Modelling words only; nothing about implementation. |
| S31-e | R3. | The mechanism that costs one attacker most is not the one that costs the other most: the host-layer mechanisms cost the model 429–511 s per deployment; service diversity costs the baseline attacker 593 s, and its other mechanisms' intervals include zero. | Float: "(Figure 5.3c)". |
| S31-close | The hand-off. | One deployment's cost depends on the attacker and the mechanism; §5.3.2 asks whether that carries into the net effect across the intervals. | — |

### D4 — §5.3.2 Effect of the attacker model, the headline (~250 words)

| Slot | Job | Facts (H1–H4, R1, amended 8j-2 / 8j-3) | Ceiling / float |
|---|---|---|---|
| S32-a | **The opener states the swap (H1).** The cold reader called its absence near-blocking (8j-3). | Against the model the host layer reduces NCR most and the service layer least; against the baseline attacker it is the reverse. Separated at 50–200 s. | Float: "(Figure 5.4; Table 5.3)". This sentence *is* the section. |
| S32-b | H2, the trend and where it ends. | Every line falls as the interval grows. Name where two or three lines first include zero; the table carries the rest. | No data dump. |
| S32-c | By construction (B6). | Below 200 s deployments saturate, unequally across layers: at 50 s the service mechanisms complete about half of those called, and user shuffle, at 20 s, nearly all. From 200 s every single mechanism completes 75, 30, 15 and 8. | One sentence. |
| S32-d | H3, as a consequence of H1 and not a second finding (examiner, 8j-2). | MTDShield chooses service diversity at most decisions (App. E.5), so it follows the service layer: above its random control against the baseline attacker, below it against the model. | The appendix's "random over four" is not reported (8j-3), so compare MTDShield with the service layer only. |
| S32-e | H4, the exception, marked. | User shuffle is at or below zero against the model (below at 50–500 s); against the baseline attacker it is +0.47 at 50 s. | Not explained. |
| S32-f | R1, recast (examiner): the rank correlation, not "ranks differently". | Spearman's ρ between the two attackers' NCR reductions at 200 s (`subsec:metrics-statistics`); report ρ with its interval, as measured. At 100 seeds the interval includes zero, so the honest wording is "no positive association", not "uncorrelated", unless 1 000 seeds narrow it. | Float: Table 5.4 (the 200 s ranks) enters here, or in §5.3.3 (B9). |
| S32-g | T9′, if Table 5.4 stays in §5.3.2. | Where the effect shows in the other metrics at 200 s: runs denied every host, a later first compromise. | — |
| S32-close | The hand-off to the depth. | A layer's line averages mechanisms that do not always agree; §5.3.3 takes them apart. | — |

**This section's ceiling.** "The baseline attacker overstates or misleads" is
interpretation and belongs to chapter 6 (§6.3). The results state that the
orderings differ, and by how much.

### D5 — §5.3.3 Defence mechanisms and execution schemes, the depth (~250 words, two paragraphs)

| Slot | Job | Facts (D1–D4, 8j-2) | Ceiling / float |
|---|---|---|---|
| S33-a | D1. | Against the model the three host mechanisms act as one effect up to 200 s and part from 500 s (IP shuffle keeps the most at 2 000 s); against the baseline attacker they are split throughout. | Float: "(Figure 5.5)". |
| S33-b | D3. | The mechanisms that keep an effect at the long intervals are not all the strongest at 200 s (model: IP shuffle over the topology shuffles; baseline: service diversity over port shuffle). | — |
| S33-c | D2, the exception marked. | The profiles agree within their whiskers except $c_3$ from 500 s. | Not explained. |
| S33-d | The strategies. | Random and alternative, by construction: one mechanism per interval, three of the seven host-layer (Table 2.5). D4: against the model MTDShield sits within about 0.1 of service diversity at every interval. | Float: "(Figure 5.6)". |
| S33-e | **Owed (tex note at the section cut, 2026-09-20; Marc).** | The 200 s figure's size is exposed to the low-and-slow dwell (Appendix C). | One sentence here or in ch6's fidelity verdict. |
| S33-f | Conditional on A8b's ruling. | Whether the exponential timing distribution changes any ordering at 200 s. | One sentence plus an appendix pointer. |
| S33-g | Conditional on A15's ruling. | The simultaneous scheme's line. | — |
| (close) | **No chapter summary.** The chapter ends on the last result. Chapter 6's first section mirrors §5.2 (Tay's form), and a summary here would state the verdict early. | — | — |

### D6 — captions: what to change (all small)

The rule is already ruled: a caption decodes, and the text states the finding
(figure conventions §b2 and the ch5 2026-09-09 caption sweep; conventions §j
adds the genre evidence). Checked against that rule:

| Float | Verdict | Change |
|---|---|---|
| Figure 5.1 (`fig:aio-coverage`) | decodes; no finding | none |
| Table 5.2 (`tab:unopposed-summary`) | "under the setup of Table 5.1" is true of every float and does no work. 8i-5 recorded the $c_{\mathrm{agg}}$ clause as applied; it is not in the caption now. | Cut the setup clause. Restore "$c_{\mathrm{agg}}$, the attack graph before partition, is its own profile" here or in S2-b5 (one place, not both). |
| Figure 5.2 (`fig:aio-stealth`) | decodes | Point "Section 4.5 defines the metric" at the paragraph's own anchor if one is added; otherwise none. |
| Figure 5.3 (`fig:aio-adaptivity`) | decodes | "Section 4.5 defines both metrics": fine. |
| Figure 5.4 (`fig:eff-cross-arm`) | decodes | None, beyond B9's table order. |
| Table 5.4 (`tab:eff-cross-arm`) | "Metrics as Table 4.3" | Point the ranking at `subsec:metrics-statistics` (s45 record l.177). |
| Figures 5.5 and 5.6 | decode | none |
| Table 5.1 | see A8c, and the "uncited value is the simulator's default" clause once A2/A3/A17 land | as Part A |

---

## Part D — the thread through the chapter (connectivity)

**What each unit takes and what it hands on.** A link that is missing today is in **bold**.

| Unit | Takes from | Hands on | Carrying sentence |
|---|---|---|---|
| ch5 preamble | ch4 (the model); SQ3 | the order of §5.1–§5.3, and why two attackers | C2, C3 — **both missing** (placeholder) |
| §5.1 | ch2 (the simulator, lineage Table 2.2); §4.5 (metrics, statistics) | every value §5.2–§5.3 reads; the no-defence reference; **the 200 s reference interval (B1)** | the Defence unit's last sentence; **B1 missing** |
| §5.2 | §5.1; §4.5 classes 1–2 | the no-defence reference, now measured | S2-close — **missing** |
| §5.3 head | §5.2's reference | pooling; the separation criterion; the order | P1–P5 — **missing** |
| §5.3.1 | §5.3 head; §4.5 (growth rate, time lost); **§2.2.3 (what a rewrite takes, still a placeholder)** | "one deployment's cost depends on attacker and mechanism" | S31-close — **missing** |
| §5.3.2 | §5.3.1's hand-off; §4.5.4 (ρ, Scott–Knott) | "a layer line averages mechanisms that disagree" | S32-close — **missing** |
| §5.3.3 | §5.3.2's hand-off | chapter 6, §6.1–§6.3, by mirror | none (no summary; D5) |

**Floats with no body-text reference today:** all nine in §5.2–§5.3 (conventions
§j8 item 4). Each slot table above names the sentence that refers to each one.

**One name per concept across §4.5, §5.1, captions and prose.** One live
breach: §5.3.1's head says *token*, *routes* and *identity*. The terminology
registry and the results-context §5 table are the check. The captions already
use *NCR reduction*, *deployment interval* and *deployment strategy*
consistently.

---

## Part E — rulings owed, in one sitting, each with a recommendation

| # | Ruling | Recommendation | Blocks |
|---|---|---|---|
| F1 | A3: the network is the lineage's released run configuration, `\citep{tay2024code}`; delete "narrowed from five to two". | Apply (evidence) | §5.1 Network ¶ |
| F2 | A2, A9, A17: cite `tay2024code` for the subnets, the three simulator durations and the near-periodic draw; the caption then shrinks to "an uncited value is argued in the text". | Apply | Table 5.1 |
| F3 | A7a: Ho on 50 s and 100 s. A7b: "the shortest Zhang and Ho ran". | Apply (evidence) | Table 5.1; §5.1 Defence ¶ |
| F4 | A7c: defend 500–2 000 s as the 1–2–5 series, to ten times the lineage's longest interval. | Adopt, one clause | §5.1 Defence ¶ |
| F5 | A8b: report the exponential timing variation (an appendix table plus one sentence), or remove it. | Report | §5.3.3; Table 5.1 |
| F6 | A8c / B8: land §2.2.3's disruption placeholder, or cut "the delay after an interrupt" from Table 5.1's caption. | Land §2.2.3; it is needed for §5.3.1 anyway | Table 5.1 caption; §5.3.1 |
| F7 | A11–A13: the reasons move to §4.5.4; §5.1's Metrics and Runs units become pointers; delete "effect sizes". | Apply | §5.1 |
| F8 | A15: run the simultaneous scheme, or give one clause of reason. | Run | Table 5.1; Figure 5.6 |
| F9 | A16: *terminating*, no warm-up; the share of runs ended by the time limit in §5.2. | One clause; one sentence | §5.1 Runs; §5.2 |
| F10 | B4: the verdict-blind control, reported (in Table 5.1 with its two-mechanism scope, plus one sentence) or cut. | Report | §5.3.1 head |
| F11 | B1: 200 s as the reference interval, with its three cited reasons, in §5.1 or the §5.3 head. | §5.1 Defence ¶ | Table 5.4 |
| F12 | B9: swap the two §5.3 tables (values to §5.3.2, the 200 s ranks to §5.3.3). | Swap | Figure 5.4's caption reference |
| F13 | S2-c2: the stealth margin rests on the dwell-only rule, stated in §5.2 or in chapter 6's limitations. | §5.2, one clause, beside the rate | §5.2 |
| F14 | D6: the caption form stays decode-only, or the headline float (Figure 5.4) alone gets a one-clause message after 1 000 seeds (conventions §j7). | Decode-only | — |
| F15 | The slot plan (Part C): ratify it, then dictate slot by slot. | — | all owed prose |

---

## Validation gate

- Table 5.1: every value cited, or argued in one clause of §5.1 (Part A's closing paragraph).
- No sentence in §5.1 contradicts Table 2.2, §4.5 or the code.
- Every row declared in Table 5.1 has a result in a float or a sentence (A8b, A15, B4).
- The five placeholders are replaced by Marc's dictated prose, through passes 2–6: the chapter preamble, §5.2, §5.3's head, and the bodies of §5.3.2 and §5.3.3.
- Every float in §5.2–§5.3 is referenced from body text.
- No banned surface word in chapter 5 (results-context §5).
- Build clean.
- Retire this handoff in the commit that lands the last of it, and prune the README line.

## Reading list

- [`../workflows/evaluation_conventions.md`](../workflows/evaluation_conventions.md): §a, §e (scope note), **§j, §k**.
- The retired results-context brief: `git show 7435c315^:docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md`. Its §1 covers the reader, §3 the paragraph shape, §5 the frame and banned words, and §8a–§8j every float's takeaways.
- `dissertation.tex` §4.5 (l.~5363–5617) and §5.1 (l.~6007–6450): the comment trail at each unit records the ruling behind each sentence.
- [`../sources/extractions/s45_metric_definitions/11_statistical_analysis.md`](../sources/extractions/s45_metric_definitions/11_statistical_analysis.md), l.170–185, for the §5.1 knock-ons already found.
