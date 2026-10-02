---
status: third pass 2026-10-02 — R1, R4–R6, R8, R9 ruled; R5 control being built; R7 (interval reading, bold marking) recommended
created: 2026-10-02
answers: docs/handoffs/2026-10-02_c_agg_ablation.md
---

# Attack profiles as §5.4's ablation: design and change proposal

## Third pass, 2026-10-02 (Marc's reply to the second)

**Ruled.**
- R5: run the size-matched, label-blind control ("random partitions of the same
  sizes, run the same way ... a defensible way"). Building in a worktree. The
  real partition must reproduce the committed nets exactly, and no runs start
  before the 1,000-seed ablations finish. Design:
  - shuffle the 38 flows into groups of 19/7/7/5;
  - build each group by the same pipeline;
  - K = 10 partitions, at the five shared cells.
- Remove c_agg everywhere listed (R9). Keep Table 5.1's Ablation row, adding the
  partition's clause (Marc: "if you think so").
- 5.4.1 "Attack profiles by objective", in method order (R6). Table 5.5 gets a new
  first block (R4). The rule is preamble text (R1).

**Table 5.5's verdict marking (Marc: the reader must see at once what is
negligible and what is not; the supervisor's "bold your headlines").**
The three readings of one $d$ against the band −0.2 to +0.2:
- the interval lies wholly inside the band: negligible;
- wholly outside: a difference;
- crossing an edge: not resolved at this seed count.

Recommended, on the interval reading (R7):
- **bold** a $d$ whose interval lies wholly outside the band;
- plain where it lies wholly inside;
- a dagger where it crosses an edge;
- one caption clause decodes the marks.

A word column (negligible / difference / unresolved) is the alternative: plainer,
but wider. Print the interval to three decimals wherever an edge rounds onto
0.20. Two cases already do: the partition under OS diversity at 200 s
(upper −0.2003) and the old failure-matrix IP shuffle at 200 s (upper 0.1999).

## Second pass, 2026-10-02 (Marc's reply; supersedes the sections below where they differ)

**Marc's rulings and directions.**
- Run the failure-matrix and vulnerability-memory ablations with the other
  components on; 100 seeds for the preliminary read, then 1,000 in the background
  (R8, yes). Running: `data/results/ch5_defended/run_ablations_1000.sh`.
- Remove c_agg from §4.3's construction, §5.1's Attacker paragraph, Table 5.1's Arm
  row and every figure; where §5.3 needs a name, it is "the APT attacker model"
  (R9, yes).
- The selection rule, in Marc's words: the three are reversible steps of the
  method, high risk to validity, and each contributes a property in Table 3.2.
  The dwell times and the other parts of §4.4 cannot be removed, because the
  model does not run without them (R1, yes).
- §5.4 stays in preliminary-result territory. Marc runs through the six moves
  before any drafting. Keep about 250 words per ablation in mind.
- The overlap is natural ("winding back a step"). Present it conventionally.

**Done in this pass.**
- `dissertation.tex`: the §5.4 preamble placeholder now states the rule.
- **§5.4.1 "Attack profiles by objective"** is added, first, as four placeholders
  (purpose, variant and prediction; manipulation check; outcome; scope and
  verdict). A comment holds the preliminary numbers. Build clean: 102 pages,
  0 undefined.
- `partition_ablation.py` → `partition_ablation_numbers.json` (n = 100 and 1,000).
- V1 passed: `run_corpus.py` runs with the modulators off, so the objective set
  never enters a run.
- `ablation.py MEMORY=1` reads the failure-matrix ablation with the memory on
  (`ablation_numbers_memory.json`).

**Preliminary result: the partition is NOT negligible** (1,000 seeds; d is with
minus without).

| Cell | NCR with | NCR without | d [95 %] | NCR reduction with / without |
|---|---|---|---|---|
| no MTD | 0.171 | 0.189 | −0.28 [−0.35, −0.22] | — |
| IP shuffle 200 s | 0.007 | 0.013 | −0.47 [−0.54, −0.40] | 0.96 / 0.93 |
| IP shuffle 2,000 s | 0.114 | 0.145 | −0.56 [−0.63, −0.49] | 0.33 / 0.24 |
| OS diversity 200 s | 0.159 | 0.174 | −0.26 [−0.33, −0.20] | 0.07 / 0.08 |
| OS diversity 2,000 s | 0.174 | 0.187 | −0.21 [−0.27, −0.14] | −0.02 / 0.01 |

- **Grid:** |d| ≥ 0.2 in 48 of the 61 reported cells. The largest is IP shuffle at
  1,000 s, −0.76.
- **Checks:** flow-weighted d is the same sign and as large or larger (−0.37 with no
  MTD). At the five shared cells, per-campaign d is smaller but still crosses 0.2, except at
  OS diversity at 2,000 s (−0.17).
- **Per profile, no MTD:** c1 0.149, c2 0.209, c3 0.172, c4 0.154, the attack
  graph 0.189. Under IP shuffle at 2,000 s: c1 0.111, c2 0.150, c3 0.088, c4 0.108,
  the attack graph 0.145. The attack graph sits beside c2, the impact profile,
  not at the mixture.
- **Manipulation check:** distinct attack paths over 1,000 runs each, k = 5: 254
  with, 535 without (k = 8: 752 and 978). The prediction holds.
- **Relative tactic occurrence:** within 1.6 points on every tactic.
- **The direction fits the §3 prediction**: without the partition, the attacker
  compromises more, and IP shuffle removes less of it at the longer interval.

**Table 5.5 preview: all three blocks at 100 seeds, one model** (the memory and
the failure matrix on wherever they are not the component removed; the three
no-MTD "with" values now agree at 0.167). Columns are Table 5.5's own. Nothing
is generated yet.

| Block | MTD | NCR with | NCR without | Cohen's d | NCR reduction with / without |
|---|---|---|---|---|---|
| Attack profiles by objective | no MTD | 0.167 | 0.182 | −0.23 [−0.42, −0.03] | — |
| | IP shuffle, 200 s | 0.006 | 0.010 | −0.30 [−0.55, −0.05] | 0.96 / 0.95 |
| | IP shuffle, 2,000 s | 0.110 | 0.137 | −0.51 [−0.76, −0.30] | 0.34 / 0.25 |
| | OS diversity, 200 s | 0.156 | 0.167 | −0.18 [−0.39, +0.02] | 0.07 / 0.08 |
| | OS diversity, 2,000 s | 0.167 | 0.175 | −0.13 [−0.32, +0.05] | 0.00 / 0.04 |
| Failure matrix | no MTD | 0.167 | 0.160 | +0.12 [−0.01, +0.25] | — |
| | IP shuffle, 200 s | 0.006 | 0.006 | +0.04 [−0.18, +0.25] | 0.96 / 0.96 |
| | IP shuffle, 2,000 s | 0.110 | 0.103 | +0.17 [+0.00, +0.35] | 0.34 / 0.36 |
| | OS diversity, 200 s | 0.156 | 0.152 | +0.07 [−0.06, +0.21] | 0.07 / 0.05 |
| | OS diversity, 2,000 s | 0.167 | 0.162 | +0.08 [−0.05, +0.22] | 0.00 / −0.01 |
| Vulnerability memory | no MTD | 0.167 | 0.163 | +0.08 [+0.01, +0.16] | — |
| | service diversity, 200 s | 0.106 | 0.104 | +0.05 [+0.01, +0.11] | 0.36 / 0.36 |
| | OS diversity, 200 s | 0.156 | 0.151 | +0.08 [+0.01, +0.17] | 0.07 / 0.07 |

The table above is Table 5.5 as it would read now. Its sources:
- the failure-matrix block: `ablation_numbers_memory.json` (100 seeds, memory on);
- the memory block: the committed `memory_ablation_numbers.json` (100 seeds);
- the partition block: `partition_ablation_numbers.json` `by_n.100`.

At 100 seeds the partition's point d crosses 0.2 in three of five cells. At
1,000 seeds it crosses 0.2 in all five; the interval lies wholly beyond 0.2 in four (OS diversity at 2,000 s reaches back to −0.14). The
failure matrix, now with the memory on, stays under 0.2 at every point, although
every interval reaches past it at 100 seeds (the point-or-interval ruling, R7; the 1,000-seed run decides).

**What follows from the pre-declared rule (R5).** d ≥ 0.2, so the result cannot
yet be put down to objective conditioning: the attack graph's net is built from
29 flows, each profile's from 4 to 14. Attributing it needs the size-matched,
label-blind control: random partitions of the 29 flows with the profiles' sizes,
run the same way. It now costs about 70 min per cell at the measured
9 runs per second, plus the code to compile a net from any set of flows. **Marc's
ruling: run it at the five shared cells (about 6 h), or report the partition's
effect with the confound named?**

**Answer to "where does 29 come from, we use 38".**
- All 38 attack flows are classified (§4.2: 19, 7, 7, 5).
- §4.3, Equation `eq:base-weight`: "An operator with several attack flows in the
  corpus counts once, through its flow with the most steps ... 29 of the 38 attack
  flows carry weight." So the weights are built from 29: c1 14, c2 6, c3 5, c4 4.
- The confound in plain words: c4's Petri net is built from 4 flows and the attack
  graph's from 29. A net built from fewer flows has fewer edges and fewer paths,
  whatever objective the flows share. So an attacker on a smaller net could behave
  differently because the net is smaller, not because of its objective.
- A random partition of the same sizes has the smaller nets without the
  objectives. If it moves like the profiles, the size explains the difference;
  if it moves like the attack graph, the objective does.

**Table 5.1: the ablations do feature today.** Table 5.1 has an Ablation row, and
both §5.4 subsections cite it for their settings. Two options:
- keep the row: one place where a replicator finds every run (recommended);
- move each ablation's settings into its own subsection, so Table 5.1 is the main
  experiment only.

The partition ablation needs no run settings of its own (it reuses the main
grid), so the row gains at most one clause. Marc rules.

**Not yet done (waits on the parallel session's uncommitted `\grouprow` work in
`dissertation.tex`, `ablation_table.py` and the ch5 generators):**
- the c_agg removals in the tex and generators;
- Table 5.5's new block;
- the Appendix F grid table.

If the tex removals ran before the floats are regenerated, Table 5.2 and Figure 5.4
would show c_agg with no definition left in the thesis.

---

(First pass follows.)

Design only. Content points, never prose; no float drawn, no generator touched, no
run made, and the ablation's contrast not computed (§3, "prediction honesty").

## 0. The answer in six lines

1. **Three ablations, chosen by one rule.** §5.4 removes each component that gives
   the APT attacker model one of the eight properties (Table 3.2,
   `tab:attacker-properties`) and can be switched off with the model still
   running. There are exactly three: the partition into attack profiles
   (property 2, objective conditioning), the failure matrix (4, adaptivity) and the
   vulnerability memory (7, learning). Declared *values* are varied, not removed,
   in Appendix C. Nothing to drop. Nothing else is owed under the rule (§1).
2. **The overlap is the design, not a flaw.** The profiles and the attack graph
   are compiled from the same 29 weight-carrying flows by the same equation. With
   the partition, the objective is fixed for the whole campaign. Without it, it is
   effectively re-drawn at every tactic (§2). That one difference is what the
   ablation removes.
3. **No new runs for this ablation.** The attack graph ran in every cell of both
   reported corpora (1,000 seeds, the memory on). The per-run cache
   (`runs_reported_summaries.pkl`, 22 MB) already holds what the computation needs.
4. **One table block, one appendix table, no figure.** A block in Table 5.5 at the
   five shared cells, plus Appendix F's table of every MTD × interval. The attack
   graph leaves Table 5.2, Figure 5.4, §4 and §5.1. The symbol $c_{\mathrm{agg}}$
   retires: "the attack graph" is chapter 4's own term.
5. **It is §5.4.1, in chapter 4's order.** It goes first because §4.2 comes before
   §4.4.4 and §4.4.5. It is also the model's central design choice.
6. **Integration is owed before §5.4 stands as one design.** The failure-matrix
   ablation ran with the memory off, and the memory ablation ran on 100 seeds
   while its caption says 1,000. Both need rerunning with the memory on at
   1,000 seeds (about 9 h together, §7). Otherwise Table 5.5's three "with" arms
   are three different models.

---

## 1. Why three, and why these three (Marc's "is this the high-value three?")

An examiner asks two things of an ablation set: what rule chose it, and what was
left out and why. The rule above answers both, and it matches the thesis's own
yardstick: Table 6.1 (`tab:fidelity-verdict`) ticks properties, and §6.3 already
reads each tick against its ablation ("property 7 read like property 4").

| Property (Table 3.2) | Component in ch4 | Treatment | Why |
|---|---|---|---|
| 1 Persistence | the Petri net campaign, dwell times | §5.2–§5.3, against the baseline attacker | Removing it removes the model, so the baseline comparison is its test. |
| **2 Objective conditioning** | **the partition into attack profiles (§4.2)** | **ablation, NEW** | Removable: the same construction runs on the attack graph. It is the property the criterion's axis 2 says matters to MTD evaluation ("a defence evaluated against a single collapsed attacker is evaluated against none of them"). |
| 3 Strategic plurality | weighted random choice at each decision place | measured (distinct attack paths), not ablated | A single-path attacker is the baseline attacker's form (fixed order), compared in §5.2–§5.3. Max-weight routing would be a new execution rule, new code and new runs. Considered and not recommended (R2). |
| **4 Adaptivity** | **the failure matrix (§4.4.4)** | **ablation** | Our judgement in every value: a threat to validity. |
| 5 Stealth | — | blank | Not addressed. |
| 6 Incentive | cost modulator, inert in the evaluated runs | blank (§6.3 placeholder) | Not in the evaluated model. **Flag:** Table 6.1 ticks it while §6.3's placeholder says blank. That is a separate ruling, owed. |
| **7 Learning** | **the vulnerability memory (§4.4.5)** | **ablation** | Our addition, and its factor of three is our judgement. |
| 8 Scheme awareness | — | blank | Not addressed. |

**Declared values** (dwell times and their family, the failure matrix's decay rate,
the detector's count and window) cannot be removed, only moved. They are varied in
Appendix C (`app:sensitivity`). §4.4 already says so and names the three values not
tested: the per-tactic dwell multipliers, $\sigma$, and one attack flow per operator.

**Marc's red flag ("reasoning pushed into the appendix").** Appendix C holds values.
The reasoning that it exists, and its verdict, belongs in the body:
- one content point in the §5.4 preamble: "components are removed here; declared
  values are varied in Appendix C";
- the verdict in §6.5 (construct validity), where the placeholder already points.

The rule sentence itself goes in the §5.4 preamble (its placeholder already reads
"every component tested here is our judgement; each is removed in turn").

**Convention.** An ablation set is conventionally the method's own contributions,
plus the components a reviewer would call arbitrary. The partition is the first
kind; the failure matrix and memory are both kinds. Tay's §6.5 is the local
precedent. Three components under a stated rule is defensible. A fourth would have
to meet the same rule, and none does.

**History, named because this overturns part of a ruling.** C31 (2026-09-13,
"ablation is going") kept the attack graph as a Table 5.2 row, "the
objective-conditioning contrast". Ablation returned on 2026-09-26. Moving the
attack graph into §5.4 completes that return and retires the row.

## 2. The overlap (Marc: "the profiles are derived from c_agg, so there will be overlap")

**What the two nets are, from Equation `eq:base-weight`.**
- Every flow is in exactly one profile.
- The attack graph's weight out of tactic $p$ is the profiles' weights at $p$,
  each counted by the number of its flows that leave $p$.
- So the attack graph is the profiles mixed **at every tactic**, while running a
  profile fixes the mix **once per campaign**.

Content point for §5.4.1's variant sentence, in ch4 words: "the APT attacker model on
the attack graph itself (Section 4.1), compiled by Equation (base-weight) over all
the flows. At each tactic it may follow any objective's flows."

**Why the overlap is right.** An ablated variant always holds the full model minus
one step. Here the step is the partition:
- same flows (the 29 weight-carrying flows, the operator rule unchanged);
- same equation, dwell times, failure matrix (verified: `outcome_overlay.json`
  and `synthetic_overlay.json` carry an `aggregate` entry under the same rule);
- same memory and seeds.

It is a paired comparison on the same seeds, so the overlap is not a statistical
problem. What it fixes is the reading: any difference comes from fixing the
objective for a campaign.

**What it does not separate (name it in §5.4.1's scope and §6.5).** The partition
does two things at once: it sorts flows by objective, and it makes each net from
fewer flows (14, 6, 5 and 4 of 29). The thesis comments recorded this on
2026-09-09 ("objective conditioning or corpus size"), and §6.5's placeholder already
lists it. Consequences:
- **If $d$ < 0.2 everywhere** on the outcome measures, the chapter's results do not
  depend on the partition, whichever of the two it is. The one residual is that two
  opposite effects could cancel: one clause in §6.5.
- **If $d \ge 0.2$ anywhere**, attributing it needs the size-matched, label-blind
  control: random partitions keeping the class sizes 14/6/5/4, compiled and run the
  same way. Declare it now as conditional (R5). Cost per cell: 10 partitions × 4
  classes × 1,000 seeds = 40,000 runs, about 2.7 h. It also needs code to compile
  nets from any flow set (`petri/divergence.py` already shuffles labels at the
  structural level).
- **Do not cite** the structural divergence-to-aggregate check
  (`data/ogasp/petri/divergence_report.md`). Its statistic fired its own kill
  criterion (Spearman −1.0 against flow count, recorded in the tex comments), and
  JSD is not thesis vocabulary.

**Verify before computing (V1):** the objective set (`petri/analysis.py`
`OBJECTIVE_TACTICS`; the attack graph's is the union) enters the run only through
`movement/utility.py`, the cost modulator. If that is inert in the reported runs,
the partition is the only difference. If not, it is a second difference and gets
named.

## 3. The six moves (§5.4.1, content points; Marc dictates)

| Move | Content |
|---|---|
| **Purpose** | The partition is our judgement (§4.2: "we have judged this partitioning"; six alternatives in Appendix B). Does fixing the attacker to one objective change what it does, what it achieves, or what MTD achieves against it? Do the chapter's results depend on it? |
| **Variant** | Without the partition: the APT attacker model on the attack graph, compiled by the same equation over all the flows (§2). |
| **Prediction** | Written from construction only. **(a) Manipulation check:** the attack graph carries 114 weight-supported transitions, the largest profile 74. It reaches 15 tactics, the profiles 12 to 14. So without the partition the attacker should take more distinct attack paths. **(b) Outcome, if the partition matters:** NCR and NCR reduction differ. A direction, for Marc to keep or drop: with more paths open, MTD should remove less (smaller NCR reduction). This is Cho's plurality argument, as axis 3 of the criterion records it. |
| **Float** | Table 5.5's block at the five shared cells. Appendix F's table of $d$ at every MTD × interval (§5). |
| **Decision rule** | §5.4's shared Cohen's $d$, negligible below 0.2. The point-versus-interval reading is owed for all three ablations; rule it once in the preamble (R7; the recommendation since 2026-09-28: the interval). |
| **Scope** | Wider than the other two: every MTD mechanism, deployment strategy and interval of §5.3, because the attack graph ran in the whole grid. The scope sentence also names what it does not separate: objective from corpus size (§2). |

**Prediction honesty.** The attack graph's no-MTD values have been printed in
Table 5.2 since 2026-09-15, and Marc has read them. So the prediction is
derived from the nets' structure, not written blind. Say nothing about it in the
thesis. The MTD-cell contrast has not been computed by anyone.

## 4. Measures, the comparison arm, and the computation

**Comparison arm: R3.** I reverse the handoff's recommendation, on merit.
- **Recommended: the "with" arm is c1–c4 averaged with equal weight**, as everywhere
  else in chapter 5 and in Table 5.5's other blocks.
  - The ablation's question is whether *the chapter's results* depend on the
    partition, and those results are the equal-weight pool.
  - The reader meets no new weighting.
  - Once §7's reruns land, Table 5.5's no-MTD "with" row is the same number in all
    three blocks.
- **Check 1 (one clause, or nothing if it agrees):** c1–c4 weighted by the flows
  that carry weight, 14:6:5:4 of 29. This is the like-for-like mixture of the
  attack graph's construction, and it catches a difference that is only
  re-weighting. Use 14:6:5:4, not §4.2's raw 19:7:7:5: Equation `eq:base-weight`
  counts one flow per operator.
- **Check 2 (JSON only): the unit of $d$.** §5.4's $d$ pools the SD of each arm's
  per-seed values. With the partition, a seed's value is the mean of four runs.
  Without it, it is one run of the attack graph, which varies more.
  - The shared definition applied literally therefore shrinks the denominator.
    It overstates $d$, the conservative direction for a "negligible" verdict, so
    no new definition is needed.
  - The per-campaign form (each arm's SD of single runs, the mixture's including
    between-profile spread) goes in the JSON.
  - If the two readings straddle 0.2, Marc rules.

**Measures** (all as Table 4.3 names them; nothing new):
- Outcome: NCR, and $d$ on NCR, at every cell; NCR reduction with and without. These
  are Table 5.5's columns, unchanged.
- Behaviour, as a manipulation check, no MTD, from the unopposed corpus:
  - **distinct attack paths** at the $k$ Figure 5.1(b) reads. §4.5 says it records
    strategic plurality, and the prediction in §3 is directional.
  - **relative tactic occurrence** on exfiltration and impact. §4.5 says it records
    objective conditioning; it is reported, with no direction predicted.
  - Distinct attack paths is capped by the number of runs, so compare equal
    counts: the attack graph's 1,000 runs against 1,000 profile runs, one profile
    per seed, assigned by a fixed rotation.
- Not used: ASP (Table 5.5 has no ASP column; adding one is the memory handoff's
  owed ruling, not this one); MTTC; attack confidentiality; time lost.

**Cells.**
- Table 5.5 uses the five shared cells: no MTD; IP shuffle and OS diversity at
  200 s and 2,000 s.
- Appendix F covers every cell: 11 conditions × 6 intervals plus none, 67 cells.
- The body states the largest $|d|$ anywhere and where it falls.

**Computation (no runs):** `data/results/ch5_defended/partition_ablation.py`, beside
`ablation.py` and `memory_ablation.py`, writing `partition_ablation_numbers.json`.
- Outcome from `runs_reported_summaries.pkl` (verified: per-run `hosts`,
  `reached_target` and `target_time`, keyed by cell, for all 402 cells).
- Behaviour from `ch5_s531_unopposed/runs_reported.jsonl`, reusing that
  analyser's path and step functions.
- Bootstrap: resample seeds, carrying all five runs of a seed together; 2,000
  resamples; percentile intervals, as `ablation.py` does.
- Never open the 28 GB `runs_reported.jsonl` whole.

## 5. Floats: what to present and what not to

**Present.**
- **Table 5.5, a block "Attack profiles by objective"**, first in method order, five
  rows, the same columns.
  - Caption content point: one clause decodes "without" for this block (the
    APT attacker model on the attack graph). Otherwise the caption is unchanged.
  - Generator: `ablation_table.py`, reading the new JSON.
- **Appendix F, a new table:** $d$ on NCR with its interval, MTD in rows, interval
  in columns, for the partition only. It backs the scope sentence; reasoning and
  verdict stay in §5.4.1.
- **Body:** two behaviour numbers (the manipulation check), the largest $|d|$
  anywhere, and the check-1 clause only if it disagrees.

**No figure.** Marc's 2026-10-01 ruling makes Table 5.5 the §5.4 headline. A
"with/without against the interval" figure would redraw Figure 5.3 with one more
line. The other two subsections earn figures only where there is a continuous
dial: 5.4.2 has none since its figure was cut; 5.4.3 has the pool. This one has
none.

**Do not present.**
- The attack graph beside each profile. It is not a fifth objective, and §5.3
  already compares the profiles.
- Its values in Table 5.2 or Figure 5.4.
- Any divergence or JSD statistic.
- The 60,000 s extension for the attack graph.
- Anything that reads it as an attacker type.

## 6. Change list (every site found by search; R = Marc rules, D = Marc dictates)

**Headings.**
- §4.2, §5.4 and chapter 6 headings are unchanged.
- §5.4's subsections become **5.4.1 Attack profiles by objective** (new; named as
  §4.2 under the "named as in chapter 4" convention), **5.4.2 Failure matrix**,
  **5.4.3 Vulnerability memory**.
- Labels are symbolic, so renumbering costs nothing. The new label is
  `subsec:ablation-attack-profiles`.

| Where | Search string | Action |
|---|---|---|
| §4.2 | "which is run beside them as the aggregate $c_{\mathrm{agg}}$" | remove the clause (D for the sentence's new end) |
| §4.2, end | (new) | D: the hypothesis and pointer, as §4.4.4 and §4.4.5 close. Without the partition, the attacker runs on the attack graph and may follow any objective's flows; Section 5.4.1 tests whether this changes any result. No symbol. |
| §4.3 | "and the aggregate $c_{\mathrm{agg}}$ by the same construction" | remove (the construction is stated for a profile's flows; §5.4.1 applies it to all of them) |
| §4.4 intro | "Section~\ref{sec:ablation} removes the failure matrix and reports what changes" | D: name all three removed components (it is already stale: the memory is missing). Consider adding the four-way partition to the "our judgement" list beside it. |
| §5.1 Attacker | "and on the aggregate $c_{\mathrm{agg}}$, the attack graph of" | remove the clause |
| Table 5.1 (hand-written) | "the APT attacker model on the aggregate $c_{\mathrm{agg}}$" (Arm row) | remove; the Ablation row gains: the APT attacker model on the attack graph, without the partition, with no MTD and under every MTD and deployment interval |
| Table 5.1 | Ablation row, failure matrix | after §7: the memory on (D) |
| Table 5.2 | `tools/ch5_unopposed_figures.py` `PROFILES` "aggregate"; caption "and on the aggregate $c_{\mathrm{agg}}$" | remove the row and clause (generator, after the parallel session commits, §8) |
| §5.3 preamble | "$c_{\mathrm{agg}}$ appears separately in Section~\ref{subsec:eff-under-defence}" | remove; "pools $c_1$ to $c_4$ with equal weight" stays |
| Figure 5.4 | `tools/_ch5_style.py` `PROFILES` "aggregate" (used by `ch5_sweep_figures.py`); caption "and the aggregate $c_{\mathrm{agg}}$" | remove the series and clause (generator) |
| §5.4 preamble | the placeholder "[Placeholder --- section preamble" | D: the rule (§1), the three components in order, the Appendix C boundary, the $d$ reading (R7) |
| §5.4.2 (failure matrix) | "and\n$c_{\mathrm{agg}}$ were not run without the failure matrix" | remove "and $c_{\mathrm{agg}}$" |
| §5.4.3 (memory) | "and $c_{\mathrm{agg}}$ were not run\nwithout the memory" | remove "and $c_{\mathrm{agg}}$" |
| Table 5.5 | `ablation_table.py` | new first block, caption clause (R4) |
| Appendix F | (new) | the full-grid table |
| §6.1 placeholder (3) | "bounded by the corpus-size confound" | D: add §5.4.1's reading |
| §6.3 | after the property-7 placeholder | D: a property-2 paragraph read like properties 4 and 7 (§8) |
| §6.4 | placeholder (1) "The attacker model is a variable of the evaluation" | D: §8's claim lands here |
| §6.5 internal | "the profiles may separate on corpus size rather than objective" and "Residual: the claim is that the APT attacker model changes the answer, not which of its parts does" | D: the residual narrows (§8) |
| `docs/workflows/terminology.md` row 48 | "$c_{\mathrm{agg}}$ the aggregate (ruled 2026-09-22)" | retire the symbol; the term is "the attack graph" (one term per thing) |
| `docs/thesis/FLOATS.md` | rows at lines 38, 137, 142 (c_agg as a series or row), plus a new row for the Appendix F table | update |
| `docs/workflows/figure_table_conventions.md` | line 552, "$c_{\mathrm{agg}}$ each keep one hue and one marker" | drop c_agg from the series contract |

Checked and needing no change: Figures 5.1, 5.2, 5.3 and 5.5 (they define the
`cagg` colour but draw no series); Table C.4 (no c_agg column); Tables F.1–F.5; the
§5.2 and §5.3 body text (no sentence quotes a c_agg value); chapters 1 and 7.

## 7. §5.4 as one design: what integration costs

Today the three ablations do not share a model:

| Ablation | Seeds | Memory in the "with" arm | Fix |
|---|---|---|---|
| Attack profiles (new) | 1,000 | on | none: it is the reported corpus |
| Failure matrix | 1,000 | **off** | rerun the "every factor one" arm, memory on: 4 profiles × 5 cells × 1,000 = 20,000 runs, about 1.4 h. The "with" arm is the reported corpus. |
| Vulnerability memory | **100** (caption says 1,000) | on | 1,000 seeds: the off arm, 6 pools × 3 conditions × 4 profiles; the on arm at pools 1–10 (pool 20 is the reported corpus, verified equal 1,200/1,200). About 120,000 runs, about 8 h. The every-exploit-succeeds arm stays at 100 seeds, JSON-only evidence for §6.3. |

At 4.1 runs per second (the reported corpus's rate), all of it fits in one
overnight run of about 9.5 h. After it:
- every "with" value in Table 5.5 is a §5.2–§5.3 value;
- the three no-MTD "with" rows agree;
- the `\owed` mark in §5.4.2 and the memory table's 100-against-1,000 mismatch both
  close.

Whether to run it is R8. The tex mark "owed" says it was intended.

## 8. Chapter 6: where the discussion stands on this ablation

**§6.3, property 2.** One paragraph, read like properties 4 and 7: implemented,
measured (§5.4.1), and whether it changes an outcome. The tick in Table 6.1 stands
either way: it marks what the model implements.

**The transferable claim, §6.4.** It is a claim about method, never about this
network's numbers. Pre-write both branches so neither reads as post hoc:
- **If the partition is negligible** (consistent with the supervisor's observation
  that the profiles move together, apart from the baseline):
  - What changes MTD's measured effect is what every profile and the attack graph
    share: the order and pace of a Petri-net campaign. The objective it pursues
    does not.
  - For an evaluator, the attacker model's execution is the variable that matters.
    A per-objective attacker is not needed to reach the same MTD conclusions on a
    simulator with these attack actions.
  - The bound is the same one §6.3 gives properties 4 and 7: the adopted attack
    actions cap what any routing difference can change.
- **If not negligible:**
  - The criterion's axis-2 claim holds on this simulator: an MTD evaluated against
    an attacker built from the whole corpus misestimates its effect against
    attackers with one objective.
  - So evaluations should name the objective, and the size-matched control (§2)
    decides how much is objective rather than corpus size.

**§6.5 internal validity.** The residual "not which of its parts does" narrows.
Three named parts are removed and their effect measured. What is left unseparated
is the shared core (order, dwell, mapping) and objective against corpus size.

**§6.1 (3) "behaviour differs by objective"** gains one sentence from §5.4.1's
manipulation check, and keeps its corpus-size bound.

## 9. Risks

- **Reading the attack graph as a fifth objective.** No float sets it beside one
  profile, and the comparison is always against the pool.
- **The objective-or-size confound** is named in §5.4.1's scope and in §6.5. The
  conditional control is declared in advance.
- **Unit of $d$** (§4 check 2): the literal shared definition overstates $d$.
  If the two readings straddle 0.2, Marc rules.
- **Antecedent rule.** §5.4.1 uses only "the attack graph", "attack profile" and
  Equation `eq:base-weight`, all chapter 4's, and §4.2 carries the pointer. No new
  term or symbol.
- **Concurrent sessions.**
  - `ablation_table.py`, `memory_ablation.py`, the three ch5 generators and
    `dissertation.tex` hold another session's uncommitted `\grouprow` work.
  - Every generator edit here waits for that work to be committed. Stage by file.
- **Simulator-bound.** Every number stays this network's; only §8's claim about
  method transfers.

## 10. Rulings for Marc

| # | Ruling | Recommendation |
|---|---|---|
| R1 | The selection rule (§1): ablate each property's removable component; vary declared values in Appendix C | adopt; it goes in the §5.4 preamble |
| R2 | A fourth ablation for plurality (max-weight routing) | no: a new execution rule, and the baseline comparison covers a single-path attacker |
| R3 | The "with" arm | equal-weight pool; flow weights (14:6:5:4) as check 1 |
| R4 | Floats | a Table 5.5 block plus an Appendix F table; no figure |
| R5 | The size-matched label-blind control | declare it now; run it only if $d \ge 0.2$ on NCR at some cell |
| R6 | Subsection order and heading | 5.4.1 "Attack profiles by objective", first |
| R7 | Point or interval reading of $d$ < 0.2, once for all three | the interval |
| R8 | The §7 integration reruns (about 9.5 h) | yes, before §5.4's numbers are read |
| R9 | Retire the symbol $c_{\mathrm{agg}}$ | yes; "the attack graph" |
| R10 | The prediction's direction for NCR reduction (§3) | Marc's call; keep if he finds Cho's argument fits |
| R11 | Table 6.1's property-6 tick against §6.3's "blank" (found here, not this ablation's) | a separate ruling |
| R12 | The partition added to §4.4's "our judgement" list | yes; it is now tested, so it should be listed |

## 11. Order of work once ruled

1. **V1:** the objective set is inert in the reported runs (§2).
2. `partition_ablation.py` and its JSON; check every number against the cache by an
   independent recompute.
3. (R8) The integration reruns overnight; refresh `ablation.py` and
   `memory_ablation.py`.
4. Once the parallel `\grouprow` work is committed: `ablation_table.py`'s new block,
   the Appendix F table, and the attack graph removed from Table 5.2's and Figure
   5.4's generators.
5. The tex removals in §6 that are not D. Build check. Then FLOATS.md,
   terminology.md and conventions.
6. Marc dictates the D sites: §4.2 end, §4.4 intro, the §5.4 preamble, §5.4.1,
   chapter 6.
