---
status: proposal — awaiting Marc's rulings R1–R12 (nothing in tex, floats or generators edited)
created: 2026-10-02
answers: docs/handoffs/2026-10-02_c_agg_ablation.md
---

# Attack profiles as §5.4's ablation: design and change proposal

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
