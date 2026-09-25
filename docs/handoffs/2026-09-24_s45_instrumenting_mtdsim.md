---
status: open                  # the brief for WRITING §4.5 — every metric defined in the method; Marc's plan (2026-09-24): results first, then fit the definitions to the settled list. Work in progress: add entries as metrics are ruled
created: 2026-09-24
updated: 2026-09-25                 # the definition template, structure and statistics subsection added from two research passes; attack actions blocked cut; ranking added
parent: the metrics design handoff (2026-09-22_metrics_provenance_and_instrumentation.md, RETIRED 2026-09-24 into this brief; implementation commits 23624188, e081a49c, 7f8cb105, 8d04fe12; full text in git history)
evidence: ../sources/extractions/mtd_metric_catalogue.md (the verdict and the source behind every entry)
---

# Define every metric in §4.5 *Evaluation metrics* — in the formalism's symbols, with its source, and why where it is ours

## Drafted 2026-09-25: §4.5 is in the tex (DRAFT STATE, for Marc's read)

Marc, 2026-09-25: *"a single agent for each of the metrics ... meticulously fleshes out the best structure, verifying sources, adaptations ... if you're a supervisor this is what you expect to see ... strictly conventional and defensible ... keep it crisp"*; and on Table 4.3: *"purpose, context, audience ... what does it need to carry ... is Class the right word"*.

Twelve agents ran from one shared brief:
- one per metric (ten);
- one for 4.5.4;
- one auditing Table 4.3.

The session merged them, reconciled the symbols, tightened the long drafts (NCR growth rate from about 290 to 230 words; time lost from about 385 to 250) and built. **§4.5 is live on printed pp. 32–38.**

**Every agent's record:** `docs/sources/extractions/s45_metric_definitions/` (tracked). Each holds the draft as written, a verification table (claim, locator, verbatim quote, verdict), the code check (file:line) and its open calls. This section keeps only the rulings and what is Marc's.

### Status per metric (✱ = overturns an earlier ruling; Marc to confirm)

| Metric | Status now | Source verdict | Code |
|---|---|---|---|
| Relative tactic occurrence | ✱ **adapted** from Rodríguez 2024 (was adopted) | Table 3 "Occur. (rel.)" pools events over 21 cases, **repeats in sequence included** (§3.2); a step never repeats | matches; 36 end-of-run markers in 198 524 records counted as steps (share change < 0.00005): filter at the 1 000-seed run |
| APV | adapted from Hong 2018, Eq. 2 (p. 39) | holds. The handoff's "lower APV … more static" quote is **p. 42**, not p. 39 | matches; lives in `ch5_s531_unopposed/analyse.py:186,478` |
| Attack rate | adapted from Zhan 2013 | **Zhan read first-hand** (arXiv 1603.07433 §III-B); Pendleton p. 15 relays it as aggressiveness | reproduces numbers.json exactly. **Active time runs to the end of the last step**, not the last action (the old slot and handoff were wrong). The baseline also stops when nothing is left to scan |
| Attack confidentiality | adapted from Zaffarano 2015 | holds. Cho 2020's relay **inverts the direction**, so it is not cited. The detector is an EWMA rate statistic (Čisar 2010, open). "Trades speed for evasion" is ch2's paraphrase, not Alshamrani's words | **index form** $D_r(j)=\sum_{i\le j}$ matches exactly; the old time form mismatched on 37 tied baseline actions |
| ASP | adopted, Cho 2020 §VII-A | verbatim | **BUG FIXED** (below) |
| NCR | adopted, Zhang 2023 p. 32; Ho 2024 Eq. 10 as "host compromise ratio" | Zhang defines NCR in words as the 0.8 stopping rule; Ho never uses the name NCR, so the prose names his HCR. Both are single-author theses: never "et al." | matches (distinct hosts; none ever lost; N = 50) |
| MTTC | ✱ **adapted** from Zhang 2023, after McQueen 2006 (was adopted) | McQueen's is an analytical expectation and never named MTTC; Zhang reads at 0.8 NCR (§5, p. 32) | matches. The attacker starts holding no host, so the first compromise is its foothold |
| NCR reduction | ✱ **adapted** from Alavizadeh 2022 (was "in the form of") | **the mitigation factor is floored at 0** (Eq. 13, "otherwise 0"); ours goes negative. The catalogue row and entry 8 misquote it without the floor | matches (`analyse.py` `suppression()` ~l.334, ratio of means) |
| NCR growth rate | introduced, "after Bruneau 2003" | the resilience curve; Bruneau 2003 **read from the author's open copy**, pp. 736–737 | matches `disruption.py`. Symbol **$g$** (was $r$, which clashed with the run) |
| Time lost per MTD deployment | introduced, "after Bruneau 2003" (loss of resilience, $R=\int[100-Q(t)]dt$) | holds. "Resilience triangle" is not in Bruneau, so it is not used | matches: ten 125 s bins, pooled before the ratio, same-seed placebo; read at 2 000 s only |
| 4.5.4 | Variant A live (what the code does); Variant B commented | Tantithamthavorn 2017 read (§5.8.1); Arcuri "at least n = 1,000" in the preprint p. 22, "per artifact"; "no lineage paper tests a ranking" holds narrowly (Barach runs a t-test) | intervals are over runs, not seeds; the bootstrap is unpaired; the **Welch/Holm check is not in the repo and holds only at 200 s**, so that sentence is CUT and the pooled variance stated as an assumption |

### Table 4.3, reshaped by the audit

- **Is it conventional?** Only partly. It read as an acronym list because it had lost the description column that every metric table in the corpus has (Zaffarano Table 4, Ho Table 3, Masud Table 3).
- **The shape now:** an unheaded category column | Metric | Description | Source | Equation. It measures 452.6 pt against 455.2 pt.
- **"Class":** no held source uses it for groups of metrics. The header is dropped, as in Table 3.1, and the prose says "categories" (He 2025).
- **Rejected on evidence:** direction marks, a unit column, a "read in" column, and a separate symbols table ("where" clauses instead; the §4.5 symbols-table option is closed).
- **Source grammar:**
  - a citation alone means the metric is defined as used here;
  - "adapted from" means one difference, stated in §4.5;
  - "this thesis, after" means introduced, with the source of its form.

### Fixed in this pass

1. **ASP counted the inherited 80 % stop as a success** (`ch5_defended/analyse.py`, `_metrics` and the ranking's no-defence row). This was found independently by the ASP and NCR agents and confirmed in code.
   - The baseline attacker's end event also fires on the 80 % compromise ratio.
   - Table 5.3 read 0.58 and the ranking table 0.60 for the same cell.
   - **Now:** `reached_target` for both attackers, read from the attacker's own record (the baseline's target hit; the model's `first_database_reach_time`).
   - The session's first attempt used the model's `database_hosts_reached`. That is read at the horizon, after later deployments may have undone the hold, so it missed taken targets. It was rejected.
   - Baseline ASP under defence moves down by 0.01–0.10. **The rankings are unchanged** (they rest on hosts compromised).
   - `section_541`'s `target_reach` also uses the record rule now.
2. **The 80 % stop is declared.** It appears in the NCR definition and in Table 5.1's time-limit cell ("or more than 80 % of the hosts \citep{zhang2023}"). It ends about 2 % of the baseline attacker's no-defence runs. **Marc's disposition is owed**: declare (done) or disable (needs a re-run).
   - It is not yet classified against the intent spec: `targeted_objective_probe.md:575` records Brown's intent as "terminate on target compromise, not on the 80 % ratio".
3. **The ranking table's caption** now points to Section 4.5.4.
4. **Bib keys added** (Crossref-checked): `bruneau2003`, `cisar2010ewma`, `efron1994introduction`, `tantithamthavorn2019impact`.

### Open for Marc (each with the recommendation)

1. **The three ✱ status changes.** Recommend accepting all three; each rests on a quoted difference.
2. **APV keeps Hong's name?** It changes object, axis, form and role, and Hong is the supervisor. Recommend keeping it with the stated difference, **and raising it with Dr Hong** rather than let him find it.
3. **The 80 % stop:** declare (done) or disable. Recommend declare.
4. **4.5.4 Variant B** (by-seed intervals and bootstrap). Recommend yes, with the resampling code, before the 1 000-seed run. The agent found the two current choices wrong in opposite directions, and one changes whether baseline user shuffle's interval includes zero.
5. **The Welch/Holm check:** add it to `analyse.py` and report agreement per interval (then restore the sentence), or leave the pooled variance as a stated assumption (as drafted).
6. **θ ≈ 2.95 in the text** is corpus-derived. Regenerate it at the 1 000-seed run.
7. **Heading "Statistical analysis":** the agent recommends keeping it (Ho §3.4.1 and Barach §4 use it).
8. **Downloads:** see `docs/sources/methodology/download_list.md`, the table "Added 2026-09-25".

### Knock-ons owed elsewhere (not done)

- **Table 5.2** prints MTTC without the share of runs it is taken over. The definition says it is reported with that share. Shares with no defence: 1.00 / 0.99 / 0.92 / 0.95 ($c_1$–$c_4$), 1.00 baseline.
- **Appendix `tab:experiment-one`:**
  - its "ASR" column is ASP's quantity under Ho's name for another quantity: rename it;
  - its MTTC column carries a count, not a share.
- **`tab_5-3-3a_lineage.tex` l.18** still says "mean suppression": change it to NCR reduction.
- **§5.1 Runs paragraph:** check that it no longer claims "effect sizes with 95 % intervals" (4.5.4 agent). Keep Zhang's 100-seed comparison in §5.1 and Arcuri in 4.5.4.
- **ASP's interval** is a Wald interval, poor near 0. A Wilson interval would be more defensible (4.5.4 and Table 5.2).
- **Figure 5.1 caption or body:** one clause that APV at $k$ = 1 is 0 for every attacker (why the figure starts at $k$ = 2).
- **The §5.2 reader** (`ch5_s531_unopposed/analyse.py` `target_reach`) uses the horizon rule. It is safe with no defence, but align it with the record rule.
- **Catalogue** (`mtd_metric_catalogue.md`):
  - l.35 misquotes Alavizadeh without the floor;
  - l.40 has "the same quantity" for Rodríguez;
  - l.41 has APV "does not exist".

  Reconcile all three with the rulings above.
- **Table 3.1:** add the anchors it lacks (Zhan; Bruneau; Alavizadeh's mitigation factor).

## Start here (2026-09-25): how to write each definition, and in what order

Marc, 2026-09-25: *"find guidance for how people define metrics in the field … best practice … common pitfalls … how we should structure it … we have to be strictly conventional … then I'm just going to go through each of the metrics and define it in 4.5 in the required structure."* Two research passes answer it: the corpus (how the papers this thesis cites define their metrics, read from `docs/sources/`) and the methodology literature (web, cited below). Where they agree, it is the rule; where they differ, the corpus wins, because it is the field the examiner reads the thesis against.

### The structure of §4.5 (four subsections)

| Part | Holds | Corpus precedent |
|---|---|---|
| Opener | One sentence: the metrics fall in three classes, one per question the results ask of the attacker (what it does, what it achieves, what a defence does to it); Table 4.3 lists them with their sources | Cho & Ben-Asher 2018 §4.2 ("two metrics measure the attack performance while the other two … the defense performance"); Alavizadeh 2022 §D's opening list |
| 4.5.1 Attacker behaviour | relative tactic occurrence; attack path variation (APV); attack rate; attack confidentiality | one subsection per class: Hong 2018 §5.1–5.2; He 2025 V-B (run-in heads per class); Zaffarano 2015 §4 |
| 4.5.2 Attack outcome | attack success probability (ASP); network compromise ratio (NCR); mean time to compromise (MTTC) | as above |
| 4.5.3 MTD effectiveness | NCR reduction (its last sentence points to 4.5.4 for the ranking); NCR growth rate; time lost per MTD deployment | as above |
| **4.5.4 Statistical analysis** (NEW) | the seed as the unit; what is reported per metric (means; 95 % intervals and how each is computed); the ranking of defences by NCR reduction (Scott–Knott ESD); Spearman's ρ between the two attackers' rankings | **statistics sit apart from the definitions in every paper that declares them** (Ho 2024 §3.4.1; Barach 2026 §4; Zhang 2023 in the paragraph after NCR); Morris et al. 2019 keep performance measures separate from methods |

**Why the ranking is not a metric of its own, nor inside NCR reduction's definition** (Marc asked: bundle with NCR reduction, or its own subsection?). A metric is a quantity read from each run; the rank is computed across runs from one of them, like an interval. That makes it a *statistic*, and both research passes put statistics in their own block. Keeping it apart also lets 4.5.4 hold everything an examiner will attack in one place: the unit, the intervals, the ranking test and its assumptions. NCR reduction's definition ends with one sentence tying them: *defences are ranked by it, Section 4.5.4*. So the ranking still sits under NCR reduction in the reading order.

### The template for one definition (corpus-conventional)

In the corpus's own order (the Alavizadeh mitigation-factor paragraph is the cleanest model: meaning → numbered equation → range → direction, about 60 words):

1. **Name (ACRONYM), cited at the name.** The status goes in the same sentence:
   - **adopted:** "…, as defined by Y";
   - **adapted:** "adapted from Y" (Alavizadeh: "We expand this metric to…"; Sharma: "by modifying the existing models of … for incorporating…");
   - **introduced:** "We define … to measure …" (Sharma: "We propose a … metric for measuring…").
2. **One sentence of what it measures**, with the stock verb ("measures", "is the share of", "quantifies").
3. **The operation in words, then a numbered display equation.** Every symbol is defined in an inline "where …" clause (the corpus's commonest form), or in `tab:gspn-notation` when it is chapter 4's.
4. **Range and direction**, in one sentence ("takes values in [0, 1]; a larger value is better for the defender").
5. **When it is read**, and **the edge case where one exists.** Ho's style: "If no compromised hosts are recorded, …". For example, MTTC when no host falls: the run is left out, and the share left out is reported.
6. **Adapted only:** one clause naming exactly what differs from the source, and why.
7. **Introduced only:** what it captures that no cited metric does, then one sentence of limitation.

**Length:**
- **Adopted:** 2–4 sentences, about 40–80 words (He, Kim, Ho, Alavizadeh, Zhang).
- **Adapted:** plus one clause.
- **Introduced:** about 8–15 sentences. That length is only precedented where the metric is the contribution (Hong's APV, Zaffarano), which is exactly the status of the two introduced here.

**Marc's calls (2026-09-25):**
- **A table of symbols is fine** if it reads better than a "where" clause per definition. It is precedented by Hong 2018 Tables 1–2 and Ho 2024 Table 3. The boilerplate lists the candidate symbols.
- **A brief rationale only where the choice needs motivating;** none otherwise.
- **A worked value only where the reading is not intuitive.** "0 is this, 1 is that" usually does the job.

**The boilerplate is in the tex** (2026-09-25), under §4.5, commented out. It has:
- the opener;
- the symbols list;
- the four subsection headings, with one `\paragraph` run-in head per metric;
- slots S1–S6 per metric, holding the facts from the entries below;
- a DRAFT equation in the proposed symbols for each, with its label (`eq:rto`, `eq:apv`, `eq:attack-rate`, `eq:detector`, `eq:confidentiality`, `eq:asp`, `eq:ncr`, `eq:mttc`, `eq:ncr-reduction`, `eq:ncr-growth`, `eq:time-lost`).

Uncomment a block as it is drafted.

**Sources fixed 2026-09-25:**
- **Hong 2018's 17 equations** were dropped by the converter. They are restored from Marc's PDF into `docs/sources/lit_review/1_2_hong2018dynamic.md`; the ≠ in Eqs. 10–14 is still to check on the typeset page.
- **Pendleton 2016 arXiv v1** is now held (`docs/sources/methodology/pendleton2016_security_metrics_survey.md`; attack rate p. 15).
- **Zhan 2013** (the attack-rate source), and the confirmations owed for Tantithamthavorn 2017, Scott & Knott 1974, Kitchenham 1995 and STRESS, are on Marc's list: `docs/sources/methodology/download_list.md`, §4.5 table.
- **`arcuri2014hitchhiker` is in the bib.**

**Not in a definition** (corpus: nobody does it): statistics, results, or a worked number, except where it clarifies an introduced metric (Hong; He).

### Pitfalls to avoid (and where this thesis stands)

| Pitfall | Source | Status here |
|---|---|---|
| A metric chosen after the results, or not tied to a question | GQM (Basili: "top-down … a bottom-up approach will not work"); Morris et al. 2019 ("justifying their relevance") | each class answers one results question; say so in the opener and in each class's first sentence |
| Measuring what is easy to count, not what matters (construct validity) | Verendel 2009 ("validated … with respect to counting and data gathering" but not against "their practical goals"); Herley & van Oorschot 2017 | the stealth pair is bounded to a declared detector (the wording ceiling below); never "less detectable" |
| A ratio that breaks when its denominator is zero | Kitchenham et al. 1995 (no "unexpected discontinuities") | NCR reduction's denominator is the no-defence NCR, never zero here; say so. Time lost is pooled before the ratio is taken (a ratio of sums). MTTC is taken over the runs that compromise a host |
| A symbol left undefined | Morris ("explicit formulae"); STRESS-DES 1.2 | the "where" clause, and the symbol check against `tab:gspn-notation` (Open 1) |
| The checkpoint not stated | STRESS-DES 1.2 ("how and when they are calculated during the model run"); ODD 2020 | MTTC to the first host; NCR at the end of the run |
| A published name reused with a changed meaning | corpus: MTTC has at least five lineage meanings, and Barach's is *containment*; Ho's ASR is not Cho's ASP | state the checkpoint or meaning at every cited name |
| An invented acronym | ruled 2026-09-24 | none |
| A metric used once, or for no purpose | Marc 2026-09-25 | attack actions blocked CUT for this reason; each of the ten now carries a float |
| No uncertainty reported | Morris: 93 of 100 simulation papers reported no Monte Carlo SE; Arcuri & Briand 2014 | 4.5.4: every value with a 95 % interval |
| A metric (read per run) confused with a statistic (computed across runs) | inference from both passes | the ranking and ρ go in 4.5.4, not Table 4.3 |
| A claim that the metrics measure real-world security | Verendel 2009 | simulation metrics of a simulated network; one clause in the opener or in 4.5.4 |

### 4.5.4 Statistical analysis: the content points

**The unit is the seed.**
- Every condition and both attackers run on the same seeds, and the seed fixes the network (Table 5.1: "the same set on every arm").
- For the ranking, hosts compromised are averaged per seed. The APT attacker model's four profiles at one seed become one value, because they are clustered.
- That gives 1 000 units per condition for both attackers at the reported run.
- The test does not use the seed blocking across conditions, which is conservative.

**Runs.** 1 000 seeds per combination. Arcuri & Briand 2014 recommend "at least n = 1,000" runs of a randomised algorithm, which is the thesis's number; cite it.

**Reported with each metric:**
- **Means:** a 95 % interval on the mean (normal approximation).
- **NCR reduction** (a ratio of means): a 95 % percentile bootstrap interval, 2 000 resamples, seeded.
- **Open (flagged by the examiner 2026-09-25):** the bootstrap resamples the defended and no-defence cells independently, ignoring the shared seeds. The interval is approximate, probably conservative. Decide before the 1 000-seed run whether to resample by seed.

**Ranking defences by NCR reduction: Scott–Knott ESD.**
- **Step 1, Scott & Knott 1974:** sort the means, split where the between-groups sum of squares is largest if the likelihood-ratio test is significant at α = 0.05, and recurse.
- **Step 2, the ESD merge (Tantithamthavorn et al. 2017):** merge adjacent groups whose difference is negligible, |Cohen's d| < 0.2 (Cohen 1988).
- **Ranks:** defences in one group share a rank, 1 for the fewest hosts compromised. No defence is not ranked.
- **Why this test:**
  - it gives non-overlapping groups, so pairwise tests are never chained;
  - it is established in empirical software engineering;
  - its effect-size merge does not depend on the run count.
- **Beyond the lineage:** no MTD paper in the corpus ranks defences with a test (Alavizadeh uses a "Best" row, Zhang a "Max Count" tally). Say so; it is the same move as reporting intervals.
- **Assumptions and checks:**
  - a one-way ANOVA with pooled variance, though the cells' variances differ widely: all-pairs Welch t-tests with Holm correction reproduce the groups (examiner 2026-09-25);
  - no transform, because the ranked quantity is the mean the metric is built on. Herbold's comment on Tantithamthavorn 2017 criticises the package's log transform, and this analysis avoids it;
  - the significance step is kept: this follows the 2017 paper, not ScottKnottESD 2.0.3, which splits on effect size alone. Name the version;
  - d < 0.2 is a convention, and middle neighbours sit near it, so the middle ranks are indicative.
- **Implementation:** `data/results/ch5_defended/sk_esd.py`, cross-checked against the original R code.

**Comparing the two attackers' rankings: Spearman's ρ** between their NCR reductions at each interval (numbers.json `ranking.by_interval.*.spearman_points`), with a seed-bootstrap interval if the body quotes one.

**Which statistic applies to which metric** (the best-practice pass: tag each):

| Metric | Reported as |
|---|---|
| Relative tactic occurrence, APV | shares pooled over runs |
| Attack rate, ASP, NCR, MTTC | mean with its interval |
| Attack confidentiality | a share over the run, in bins |
| NCR reduction | point with a bootstrap interval, and the rank |
| NCR growth rate, time lost | pooled over deployments |

### Research sources (2026-09-25)

**Corpus (read from `docs/sources/`):**
- Zaffarano 2015 §4;
- Hong 2018 §5 (equations via `metric_census/A_hong.md`);
- Cho 2020 §VII;
- Zhang 2023 §3.4, §5;
- Ho 2024 §3.3.2, §3.4.1;
- Alavizadeh 2022 §D (the mitigation factor, l.597–601);
- Sharma 2025 §4;
- Brown 2023 §IV;
- He 2025 V-B;
- Kim 2026 §6.1.3;
- McQueen 2006;
- Cho & Ben-Asher 2018 §4.2;
- Masud 2025 §3.5;
- Barach 2026.

Zhan 2013 and Pendleton 2016 are not held (read through census F only).

**Methodology (web):**
- NIST SP 800-55r1 (the measure template, Table 2);
- Jansen, NISTIR 7564;
- Morris, White & Crowther 2019;
- STRESS-DES item 1.2;
- ODD 2020;
- Verendel 2009;
- Herley & van Oorschot 2017;
- Savola 2013;
- Basili, GQM;
- Kitchenham et al. 1995 (through a secondary summary);
- Arcuri & Briand 2014;
- Herbold's comment on Tantithamthavorn 2017.

Before citing any of these in the thesis, fetch it and confirm the wording; the agent read 10 of 17 in the primary text.

## Goal

§4.5 holds one definition per metric the evaluation reads — all ten of Table 4.3, the cited ones included — so that the table only has to name them and a reader can place every one in the field. This is the convention the field follows and this thesis has adopted (`docs/workflows/literature_conventions.md` §d, anchored in hong2018, which defines its whole metric family in its method with equations, pp. 40–41). Marc, 2026-09-24: "we can define every single metric in the method and then that will make Table 5.2's job easier"; "results first, and then I'll backwards fit once I've got the complete list of metrics down"; "strictly defensible … so anyone reading the paper can be like, oh yeah, that's what they're doing."

**Not this brief's job:** changing any metric, number or float (they landed 2026-09-24); the prose voice (Marc dictates; this brief supplies content points only).

## State of play

- **§4.5 is *Evaluation metrics*** (`\label{sec:evaluation-metrics}`, renamed 2026-09-24 from *Instrumenting MTDSim*), with a placeholder, the metrics table, and **three subsections, one per class, plus a fourth, *Statistical analysis* (`subsec:metrics-statistics`, added 2026-09-25)** — *Attacker behaviour* (`subsec:metrics-behaviour`), *Attack outcome* (`subsec:metrics-outcome`), *MTD effectiveness* (`subsec:metrics-effectiveness`) — each holding a "definitions owed" placeholder. The older comment block with the 2026-09-23 content points sits below; this brief supersedes it.
- **The metrics table moved into §4.5** (Table 5.2 → **Table 4.3**, `tables/tab_4-5a_metrics.tex`, label `tab:metrics` kept): Class · Metric · Source, the class a level first column, no definition column — the definitions are this brief's job. §5.1 now only points to it.
- **§5.2's floats and §5.3's labels** carry these metrics (Figure 5.1's three panels, Table 5.3; NCR reduction, attack actions blocked, recovery time in §5.3). Numbers are 100 seeds until the 1 000-seed run.
- **Appendix C** has the owed sweep's section, `app:detector-memory`, as a placeholder.
- **Bib:** `zhan2013`, `pendleton2016`, `ward2018`, `jafarian2015` added (names as the sources print them; `pendleton2016`'s wording to confirm in the published version). Every other source below is already in the bib.

## What each definition must carry

1. The field's name, and its acronym where the field has one (ASP, NCR, MTTC, APV). No invented acronym: attack rate and attack confidentiality have none; *AC* is taken by attack cost.
2. **A numbered display equation in the formalism's symbols** — the run, its records, the places $p$, the verbs $\varphi(p)$ — so the metric reads as part of the model, not beside it.
3. Its direction (which way is more, or better for the defender).
4. Its source, cited.
5. For an **adapted** metric: the one difference from the source that matters, stated at the definition (convention §d2 — a field name is never reused with a changed meaning silently).
6. For an **introduced** metric: what it captures and why no cited metric does (E3).
7. **Reader level.** The census's finer distinctions (Ho's per-attempt ASR, the five MTTCs of the lineage, Brown's in-flight blocks) stay in the catalogue; the thesis states our definition, its source and the one difference that matters.

### Symbols (proposal; ruling owed, Open 1)

Taken in chapter 4 (`tab:gspn-notation`): $c$, $\mathcal{N}_c$, $p$, $\hat{p}$, **$\tau_p$**, $t_{pq}$, $\mu_p$, $w_c$, $s$, $M_0$, $v$, $F_v$, $\varphi$, $R$, $d$, **$\gamma$, $\delta$**, $z$. So the detector's memory **cannot be $\tau$** as in the records and the analyser (`TAU`); proposed:
- $\kappa$ — the detector's memory, in seconds (60 s);
- $\theta$ — the alarm level;
- $k$ — the opening length (already printed in Table 5.2);
- $A_r = (a_1, a_2, \dots)$ — the start times of run $r$'s actions; $T_r$ — its active time;
- $H_r$ — the hosts run $r$ compromises; $N = 50$ the network's hosts.
Checked free in the tex: $\theta$, $\kappa$, $\lambda$, $\eta$, $\omega$, $h$, $k$.

## The ten entries

### Attacker behaviour — read in §5.2, Figure 5.1

**1. Relative tactic occurrence — cited** (ruled 2026-09-24, third pass).
- *Definition:* the share of an attacker's steps that fall in each tactic, pooled over its runs; a step is a tactic entered (the firing of its timed transition $\tau_p$), or, for the baseline attacker, a verb entered with consecutive repeats collapsed.
- *Source:* Rodriguez et al. 2024 (`rodriguez2024`, already in the literature review): Table 3 reports, per ATT&CK tactic, "Occur. (rel.)" — the share of the attackers' events in each tactic, from process mining of attack logs. The same quantity, so cited, not adapted. (Supersedes the marsan1984 anchor proposed the same morning.)
- *Why steps, not time:* the model's time at a tactic is its declared dwell, which replaces the verb's native cost; time shares would compare two clocks. Steps are counts on both.
- *Numbers now:* dwell-only tactics hold 36/37/47/26 % of $c_1$–$c_4$'s steps; the baseline's six verbs: `ENUM_HOST` 25, `SCAN_PORT` 25, `EXPLOIT_VULN` 23, `BRUTE_FORCE` 16, `SCAN_NEIGHBOR` 9, `SCAN_HOST` 2.

**2. Attack path variation (APV) — adapted** (ruled 2026-09-24).
- *Definition:* for an opening of $k$ tactics, the share of the attacker's runs whose first $k$ tactics differ from its most common first $k$ (for the baseline attacker, activities entered, repeats collapsed). 0: every run opens alike.
- *Source:* Hong et al. 2018 (`hong2018`), APV, Eq. 2, p. 39: "lower APV value means the set of attack paths tends to be more static".
- *Differs:* Hong measures how the attack paths *available* change between network states; this measures how the paths an attacker *takes* vary between its runs.
- *Why:* strategic plurality is claimed; the baseline attacker is one script.

**3. Attack rate — cited name, adapted unit.**
- *Definition:* $1000\,|A_r| / T_r$, averaged over runs: the attacker's actions per 1 000 s of its active time.
- *Source:* Zhan et al. 2013 ("the number of attacks that arrive at unit time"); surveyed by Pendleton et al. 2016 as a measure of an attack's aggressiveness.
- *Differs:* one attacker's own actions, not attacks arriving at a sensor.
- *The action rule, stated once for both stealth metrics:* an action is a verb that **runs** on the network (end-of-run markers, which carry no verb, are not actions either). A tactic that invokes no verb adds time and no action; a verb whose precondition is unmet is checked before it runs and never touches the network (`movement/attacker.py:896`), so it is not an action; the baseline attacker's per-vulnerability exploit rows are one action. **Say that the rule matters:** counting the unmet verbs would put $c_4$ level with the baseline attacker (20.7 against 28.4 per 1 000 s, or 28.7 if counted; `numbers.json`, `attack_rate_counting_blocked`).
- *Why active time:* in the targeted attack scenario a run ends when the target falls; the baseline attacker takes it early (its active time averages 0.70 of the limit), so a rate over the whole limit would hide the difference.
- *Why the metric:* it is the footprint a detector sees, measured with no assumption (entry 4).

**4. Attack confidentiality — adapted.** *The by-proxy stealth metric — the paragraph E10(i) depends on.* **Read over the run (Figure 5.1(c), third pass):** in each 1 500 s bin, the share of actions below the alarm, with the alarm set by one rule — it flags half of the baseline attacker's actions (the median of $D$ over them, $\theta_b$ = 2.95) — a detector tuned on the attacker the defences were built against. So no alarm level is chosen, and the baseline sits near 50 % by construction; the result is the profiles' 70–93 %, flat across the run. §4.5 states the rule and that the baseline's level is set by it. The across-levels curve (the earlier panel) stays in `numbers.json` as a robustness reading.
- *Definition:* the share of the attacker's actions taken while $D < \theta$, where $D(t) = \sum_{a_i \le t} e^{-(t - a_i)/\kappa}$ counts the attacker's recent actions, each fading over about a minute ($\kappa$ = 60 s: an action counts fully when it happens, about a third a minute later, a seventh two minutes later). An action is exposed when $D$, counting it, reaches $\theta$; Figure 5.1(c) shows every $\theta$, so none is chosen.
- *Source:* Zaffarano et al. 2015, attack confidentiality, "how much attacker activity may be visible by detection mechanisms"; relayed in Cho et al. 2020 as "the degree of attack behaviors detected by a defender". Already in Table 3.1.
- *Differs:* Zaffarano's exposure was information visible in network traffic; here it is a declared detector that counts recent actions.
- *Why, and why by proxy:* an APT attacker trades speed for evasion (Alshamrani et al. 2019); slowing the rate of an attack avoids triggering a defence (Ward et al. 2018, §5.18); fast scanning is easy to detect (Jafarian et al. 2015). The three outcome metrics read only the speed side. MTDSim has no detector, so detection cannot be measured; what can be measured is what the attacker gives a detector to see, and this says what a stated detector would make of it.
- *Must also say, once:* a detector that counts time spent on the network would read the slower attacker the other way (Hong et al. 2018, rationale for ACD: "the longer the attack takes, the more likely it will be detected"); the claim is bounded to a detector that counts actions. $\kappa$ is swept in Appendix `app:detector-memory`.

### Attack outcome — read in §5.2 (Table 5.3) and §5.3

**5. Attack success probability (ASP) — cited.** The share of runs in which the attacker compromises a target host of the targeted attack scenario. Lower is better for the defender. Cho et al. 2020 (the dominant effectiveness metric, "the probability that attacks are successfully performed"); Zaffarano et al. 2015 (*attack success*).

**6. Network compromise ratio (NCR) — cited.** $|H_r| / N$ at the end of the run, averaged over runs. Zhang 2023; Ho et al. 2024 (Eq. 10). *One sentence §4.5 owes* (Marc 2026-09-24): the lineage reads NCR with the general attack scenario, where taking the network is the goal; under the targeted attack scenario it reads how much of the network the attacker holds when its run ends — because the target fell or time ran out — and ASP beside it says which. Under a defence the APT attacker model rarely takes the target, so its runs reach the time limit and NCR compares like with like; that is why NCR, not ASP, carries §5.3.

**7. Mean time to compromise (MTTC) — cited, checkpoint stated.** The mean, over the runs that compromise a host, of the time from the start of the run to its first compromise; the share that compromise none is given beside it. McQueen et al. 2006; Zhang 2023. *One sentence:* Zhang reads it when 80 % of the hosts have fallen; the APT attacker model never reaches that (14–20 % by the limit), so here it is the first host.

### MTD effectiveness — read in §5.3

**8. NCR reduction — cited form.** $1 - \overline{\mathrm{NCR}}_{\text{defence}} / \overline{\mathrm{NCR}}_{\text{no defence}}$, a ratio of means with a bootstrap interval: 0 for no effect, 1 for no host compromised, negative if the defence helps the attacker. The form is Alavizadeh et al. 2022's mitigation factor, $1 - \mathrm{ALE}^m / \mathrm{ALE}$, "the ability of the defensive MTD techniques to impair the attack" (Eq. 13). *Why NCR and not ASP:* under a defence the APT attacker model's ASP is zero on most conditions and cannot order them. **Last sentence (2026-09-25):** defences are ranked by NCR reduction, and the ranking is declared in 4.5.4. **Edge case:** the denominator, the no-defence NCR, is never zero here (0.16 and 0.49); say so.

**9. Attack actions blocked: CUT 2026-09-25** (Marc: "all the metrics need to be there for a purpose … if they're not … we have to cut it"). It served one float, for one attacker (structurally zero for the baseline); it read 0.24 with no defence; and its Brown attribution was disputed. Removed from Table 4.3, Table 5.1 and Table 5.3. The old entry is kept for the record: **Attack actions blocked, adapted.** The share of the attacker's actions that fail because something they need is no longer there. Brown et al. 2023, §IV-A "Attack Actions Blocked" (a count of the actions an MTD technique blocked; §III-D: connection to the host or service lost, or the user's access changed). *Differs:* a share, so attackers acting at different rates compare; and it counts such failures with no defence running too (0.24), so §5.3.1 reads its change around a disruption.

**10. Time lost per MTD deployment — introduced (was recovery time; renamed 2026-09-24 with the Figure 5.3 rebuild, results context §8g-5; the full name RULED by Marc the same day: "the name should explicitly describe what it's doing"; notes also sit under §4.5's holder in the tex).** The progress one MTD deployment costs the attacker, as seconds at its own pace: the hosts it would have compromised in the 1 250 s after the deployment completes at its rate in the 750 s before, less those it did, over that rate — less the same quantity read at the same moments on the same seed's no-defence run (the placebo; the attacker's pace drifts within a run). Zero: the deployment cost nothing; it can be negative (a catch-up above its level cancels a dip). It is the dip at the deployment, not the net over the run (NCR reduction is the net); only deployments with a full 750 s before them count; at a 2 000 s interval the window stops at 1 250 s because the next deployment's before-window begins there. Must also define **NCR growth rate** (new Table 4.3 row): hosts compromised per unit of the attacker's live time, read around a deployment as a percentage of its rate before; the curve time lost is the area of. *Why:* adaptivity — responding to a defence — is the one APT property readable only when a defence acts; the field's recovery metric (MTTR) is the defender's; that the attacker must recover at all is Jafarian et al. 2015's point. Three per-event estimators (the wait to the next compromise, against a clock-matched or a progress-matched reference) were tried and rejected on censoring and reference grounds; record in §8g-5. **The equations (Marc 2026-09-24: "can this be expressed in calculus? ... we're measuring the rate of change"): yes, and this is their display form.** With $H(t)$ the hosts compromised by time $t$ ($\mathrm{NCR}(t) = H(t)/50$) and a deployment completing at $t_d$: the NCR growth rate is $r(t) = \mathrm{d}\,\mathrm{NCR}/\mathrm{d}t$, estimated in 125 s bins of live time; relative to the rate before, $\tilde r(t) = r(t_d + t) / \bar r_{-}$ with $\bar r_{-}$ the mean rate over $[t_d - 750, t_d)$; time lost $= \int_0^{1250} (1 - \tilde r(t))\,\mathrm{d}t$, less the same integral on the same seed's no-defence run at the same $t_d$ (pooled over deployments before the ratio is taken, so it is a ratio of sums, not a mean of ratios). The 1 250 s upper limit and the 750 s window are declared constants; say why (the next deployment's window at a 2 000 s interval).

## The "why did you do that" items for §5.1 (Marc, 2026-09-24)

Not §4.5, but the same defensibility pass, and the setup is where a reader asks:
- **The targeted attack scenario.** Brown's general attack scenario is a takeover (compromise as much of the network as possible); his target attack scenario is the one he calls "APT-style" — so the thesis switches it on for both attackers, and it exists in the lineage. One clause at the Attacker unit (currently "Both pursue the targeted attack scenario (Table 2.3)").
- **The metrics sentence.** §5.1's Metrics unit still says "grouped by effectiveness and efficiency, as Table 3.x groups the field's": it becomes the three classes, each named for what it measures, defined in §4.5.

## Open (add as they come)

**Moved out of the §5.2 captions and axes into §4.5 (Marc, 2026-09-24: "define them once ... the figures are self-explanatory"; the floats now name each metric and say how to read it).** §4.5 must therefore carry: what a *step* is (a tactic entered; a verb entered by the baseline attacker, repeats collapsed); what an *opening* of length $k$ is; APV's direction (higher: runs start more differently); what an *action* is (a verb that runs: not dwell-only, not blocked, not end-of-run markers; one exploit activity, not each vulnerability); the detector (recent actions, each fading over about a minute) and the alarm's tuning rule, with the consequence that the baseline attacker's share over the whole run is 50 % and its later bins sit below it because its actions fall early; *active time* (to the last action; a run ends on taking a target) as the attack rate's denominator; MTTC to the first host; and — in §4.3's words, not §4.5's — that $c_{\mathrm{agg}}$ is its own profile (the attack graph before partition), not an average.

**Framing ruled (Marc, 2026-09-24):** chapter 5/6 say the model takes fewer actions above a rate alarm tuned on the baseline attacker, because much of its campaign is in tactics the simulator gives no network action — not "much harder to detect". The four-variant action-rule sensitivity (results context §8i-5) goes to Appendix C.4 as a later item.


0. *Action* now has ONE sense (attack actions blocked, which counted invoked verbs, is cut 2026-09-25): a verb that **runs** (attack rate, attack confidentiality). Define it once, in 4.5.1. Also define *opening*, *alarm level* and *detector*; Figure 5.1's caption points here.

1. The symbols (above), especially $\kappa$ for the detector's memory in place of $\tau$.
2. Table 3.1: add the anchors it lacks — attack rate (Zhan), Outkin's time share, the mitigation factor (Alavizadeh) — so every §4.5 source is on the literature review's map. Attack confidentiality, APV, ASP, NCR, MTTC and attack actions blocked are there already.
3. The sweep for `app:detector-memory` — **the alarm quantile and $\kappa$ together** (round 3: at the 60th percentile $c_4$ drops below the baseline in the first bin; $\theta_b$ depends on $\kappa$); §4.5 must also say **why the median** (a detector tuned to flag half of the known attacker's activity). Was: the $\kappa$ sweep (no-defence corpus, both attackers; the ordering across $\theta$ at each $\kappa$). The 2026-08 sweep was for the older tier-weighted detector and does not carry over.
4. A hand trace for each adapted and introduced metric (V1) — a four-host run, recorded.
5. The ablation sentence for §5.2 (the no-action tactics removed from the record) re-run on this detector: at the minute scale it erased the margin; say it only where it holds.
6. The comment block under §4.5's holders (the 2026-09-23 content points) — replace with a pointer here when the definitions are written.

## Validation gate

Each of the ten has its equation, direction and source in §4.5; every adapted metric states its one difference; every introduced metric states why; the symbols collide with nothing in `tab:gspn-notation`; Table 5.2's Source column and §4.5 agree; the two §5.1 clauses are in; build clean.

## Reading list

- `docs/workflows/literature_conventions.md` §d — the convention.
- `docs/thesis/dissertation.tex` — §4.5's holders; `tab:gspn-notation` (l.~4427); Table 3.1 (l.~2120).
- `docs/sources/extractions/mtd_metric_catalogue.md` — each source, with its locator.
- `data/results/ch5_s531_unopposed/analyse.py` — the implementation each equation must match (the metrics-design block).

## Carried from the retired metrics design (2026-09-24)

**The split, and why it is ours.** Three classes, one per question the results ask of the attacker: *attacker behaviour* (what it does; §5.2), *attack outcome* (what it achieves; §5.2's reference and what §5.3's defences change), *MTD effectiveness* (what a defence does to it; §5.3). Not the phases (the outcome metrics are read in both); not Cho's effectiveness/efficiency (the thesis does not model defence cost). "MTD effectiveness" keeps Cho's word because that class *is* the field's effectiveness question. Labels ruled 2026-09-24.

**Wording ceiling for the stealth pair.** Observations of the no-defence runs: "acts at a lower rate", "takes more of its actions below the alarm"; never "less detectable" in chapter 5; the stealth property stays NOT ADDRESSED (a declared detector, not a detection model in the simulator). Framing ruled 2026-09-24: fewer actions above a rate alarm tuned on the baseline attacker, because much of its campaign is in tactics the simulator gives no network action.

**The supervisor's questions, and where the page answers them.**

| Question | Answer |
|---|---|
| Where is this metric from? | Table 4.3's Source column; §4.5 for every adapted or introduced one |
| What is NCR reduction — is that yours? | NCR is Zhang's and Ho's; the with-and-without form is Alavizadeh's mitigation factor; it is the old *suppression*, renamed |
| Your ASR isn't Ho's. | It is ASP (Cho), estimated over runs; Ho's ASR is hosts compromised per attempted action |
| MTTC to what? | the first host (the lineage's 80 % checkpoint is never reached by the APT attacker model) |
| How can you measure stealth with no detector? | the footprint (attack rate) and what a declared detector makes of it (attack confidentiality); the claim is bounded to that |
| Isn't a slow attacker *more* detectable? | to a detector that counts time on the network, yes (Hong 2018's rationale for ACD); ours counts recent actions |
| Your model is worse. | slower and quieter for the same reason — Table 5.2 beside Figure 5.2 |
| What is time lost per MTD deployment, and why not recovery time? | the area of the dip in NCR growth rate after a deployment, as seconds at the attacker's own pace; the per-event wait to the next compromise failed on censoring and on its reference (results context §8g-5) |

**Cut from §5.2, with the reason** (for the examiner who asks): profile divergence (the heat map shows it; its noise floor could not be failed); effective behavioural breadth (Cho and Jalowski use *unpredictability* for the defender's configuration); the detectability level as a metric of its own (it survives as the detector inside attack confidentiality); disengagement and learning (inert in the reported configuration); path entropy, coverage curves, deepest stage (killed or saturated).

**The internal-MTTC finding** now lives in `docs/implementation/metrics_semantics.md` §(a).
