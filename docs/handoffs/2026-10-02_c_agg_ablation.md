---
status: proposal written (2026-10-02_c_agg_ablation_proposal.md), awaiting Marc's rulings R1–R12; no tex, figures or generators edited
created: 2026-10-02
---

# The aggregate as an ablation: objective conditioning tested in §5.4, c_agg removed from the method and §5.2–§5.3

**Goal.** Design §5.4's third ablation, the partition of the attack graph into attack
profiles, and propose every change the thesis needs to carry it. The deliverable
is a proposal Marc rules on. Do not draft prose (Marc dictates), and do not generate
or edit figures, tables or tex.

## Why (Marc, 2026-10-02)

- Today c_agg is drawn as a fifth line beside c_1 to c_4 (Table 5.2, Figure 5.4,
  Appendix F), and the reader cannot tell what it is for.
- c_agg differs from the profiles by exactly one design step. The thesis defines it
  as "the attack graph ... before it is partitioned into profiles" (§5.1, search
  "before it is partitioned into profiles"). Same Petri net construction, dwell
  times, failure matrix, vulnerability memory, seeds. So c_1–c_4 against c_agg is an
  ablation of objective conditioning.
- Marc's rulings in the exchange: reframe the thesis if needed ("I can reframe the
  thesis"); c_agg is **introduced in the ablation, not defined in the method**; the
  discussion point (§6) **stands on this ablation**.
- Marc's question, to answer in the proposal: how do you ablate something when the
  profiles are derived from c_agg, so the two overlap?

## The overlap argument (the session's answer, to check and state)

- The overlap is the normal shape of an ablation: the ablated variant holds the
  full model's ingredients minus one step, here the partition.
- It is a paired comparison of two configurations on the same seeds, not two
  independent samples, so the overlap is not a statistical problem.
- What the overlap fixes is the interpretation. Every edge of c_1–c_4 is in c_agg,
  so any difference comes from what partitioning removes:
  - paths that mix objectives (an exfiltration branch running into an impact branch);
  - transition weights pooled over the 38 attack flows instead of conditioned on one
    objective. Verify how W_c is built per profile and for c_agg (§4 GSPN,
    search "by the same construction").

## The design decision that makes it defensible: the "with partition" arm

- c_agg carries the corpus's proportions. Each profile holds a share of the 38
  attack flows: c_1 19, c_2 7, c_3 7, c_4 5 (§4.3, search "referred to by index";
  verify c_3's count).
- So the like-for-like arm is c_1–c_4 **weighted by their share of the flows**.
  Report the equal-weight mean beside it as a check (§5.3 pools with equal weight;
  search "pools $c_1$ to $c_4$ with equal weight").
- If the two agree, one clause says so. If they differ, Marc rules which arm the
  headline uses.

## What the proposal must contain (top-down)

1. **The six moves**, as §5.4.1 and §5.4.2 use them (purpose, variant, prediction,
   float, decision rule, scope). Read those two subsections first. In particular:
   - Purpose: does conditioning on an objective change what the APT attacker model
     does and achieves, and do §5.3's conclusions depend on it?
   - Prediction, written before the numbers are read. Example shape: c_agg reaches
     targets more often (more paths), and its NCR reduction under MTD is or is not
     different.
   - Decision rule: §5.4's shared Cohen's d, seed-paired, negligible below 0.2 (the
     §5.4 preamble). Note the owed ruling on point versus interval reading of
     d < 0.2 (vulnerability-memory handoff).
2. **Measures**, each named as Table 4.3 names it (no new metric unless §4.5 gains it
   with a reason):
   - attack outcome: ASP, NCR, MTTC;
   - behaviour: relative tactic occurrence, distinct attack paths, attack rate;
   - response to MTD: NCR reduction (and ASP reduction?) at the cells §5.4.1 uses
     (IP shuffle and OS diversity at 200 s and 2 000 s), or at more cells, since
     c_agg runs everywhere. Propose which.
3. **Data.** No new runs. c_agg is in every cell of both reported corpora
   (1 000 seeds, vulnerability memory on):
   - `data/results/ch5_s531_unopposed/runs_reported.jsonl` (profile `aggregate`);
   - `data/results/ch5_defended/runs_reported.jsonl` (402 000 runs, 28 GB; never load
     it whole; read rows by streaming, or from the analyser's summary cache).

   Propose where the computation lives. Recommended: beside the other ablations
   (`ablation.py`, `memory_ablation.py`), with its own numbers file.
4. **The float.** One float for §5.4, in the house style
   (`docs/workflows/figure_table_conventions.md`, and §5.4.1/§5.4.2's floats as
   the pattern). Propose what it plots; do not draw it.
5. **Change list**, every site with its search string, each marked "remove",
   "move" or "reword (Marc dictates)":
   - §4: the c_agg sentences: search "run beside them as the aggregate", and "and the
     aggregate $c_{\mathrm{agg}}$ by the same construction".
   - §5.1 / Table 5.1: the Arm row names c_agg (`tables/tab_5-1a_experiment.tex`,
     search "on the aggregate"); it moves to the Ablation row.
   - §5.1 arm paragraph: search "on the aggregate $c_{\mathrm{agg}}$, the attack graph".
   - §5.3 preamble pooling sentence: search "pools $c_1$ to $c_4$ with equal weight".
   - §5.4 preamble, and the two scope sentences that name c_agg as "not run without"
     (search "were not run without").
   - Floats that carry c_agg today: Table 5.2 (`tools/ch5_unopposed_figures.py`,
     `PROFILES` includes "aggregate"), Figure 5.4 and Appendix F
     (`tools/ch5_sweep_figures.py`, `PROFILES` from `tools/_ch5_style.py`). Check
     Figure 5.1 and Table C.4 as well.
   - Any body sentence quoting c_agg values (§5.2, §5.3, §6). Search `mathrm{agg}`.
   - `docs/thesis/FLOATS.md`, `docs/workflows/terminology.md` if c_agg has a row.
   - §6: where the discussion point lands (§6.3, properties of the APT attacker
     model, or §6.1). One transferable claim, stated as a claim about method.
6. **Risks to name:**
   - c_agg is not a fifth objective. Nothing may read it as one.
   - The comparison is per seed against the weighted profile arm, never c_agg
     against each profile (§5.3 already compares the profiles).
   - Results stay simulator-bound. The transferable claim is about whether objective
     conditioning matters to an evaluation, not about this network's numbers.

## Validation gate

A proposal document (in this handoff or beside it) that Marc can rule on point by
point: the six moves, the comparison arm, the measures and cells, where the
computation lives, the float's specification, and the change list with every site
found by search. No tex, figure, table or generator is edited.

## Hard constraints

- **Prose is Marc's.** Content points and slots only (memory: slot-generator drafting).
- **Antecedent rule:** chapter 5 uses chapter 4's words. "The attack graph" and
  "attack profile" are defined in §4; c_agg's one introducing sentence in §5.4 may
  use only those.
- **No invented terms or acronyms**; metrics as §4.5 defines them.
- **Concurrent sessions edit this checkout.** Before proposing generator changes, run
  `git status` and `git diff tools/`: on 2026-10-02 both §5.3 generators and
  `ch5_unopposed_figures.py` held a parallel session's uncommitted table-style work
  (`\grouprow`, defined only in the uncommitted `dissertation.tex`). Removing c_agg
  from those generators must wait for that work to be committed.
- Branch `feat/ch5-1000-seeds`; stage by file; never push.

## Reading list

- `docs/thesis/dissertation.tex`: §4.3 attack profiles (`sec:attack-profiles`), §4
  GSPN construction, §5.1 experimental setup, §5.4 preamble and both ablations
  (`sec:ablation`, `subsec:ablation-failure-matrix`,
  `subsec:ablation-vulnerability-memory`).
- `docs/handoffs/2026-09-28_vulnerability_memory_on.md`: how the last ablation was
  designed (the six moves, the owed d ruling).
- `docs/handoffs/2026-09-30_ch5_reported_corpus.md`: the reported corpora and their
  files.
- `data/results/ch5_defended/ablation.py` and `memory_ablation.py`: the pattern for
  the computation.
- `docs/workflows/voice.md` §(0) and memory "Measurement vs attribution": a "why" is
  a hypothesis naming a declared choice.

## Out of scope

- Drafting any sentence, caption or heading.
- Generating any figure or table, or editing any generator or analyser.
- Re-running anything.
