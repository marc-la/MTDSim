---
status: open           # opened 2026-08-30 by the token-hold session; retire when experiment 2 is re-established on the restored substrate and the register/criterion/probe records carry the result
created: 2026-08-30
---

# Re-establish the headline on the restored substrate — the ρ = −0.893 inversion does not reproduce after `d127f443`, on the attacker it was measured on

> **One-line goal.** Find out whether the defence-ranking inversion (experiment
> 2's E5, the project's headline) exists on the current substrate, and if it
> does not, *which* 2026-08-27 repair removed it — before any results prose
> leans on it.
>
> **Run this in a fresh session, cold from this brief.** Report the numbers;
> the thesis-framed return is which claim survives.

## State of play

- **The measurement that opened this.** The token-hold record
  ([`../implementation/pipeline/ogasp/fsm_token_hold_findings.md`](../implementation/pipeline/ogasp/fsm_token_hold_findings.md)
  H0) re-ran experiment 2's E5 statistic at 50 seeds (eight conditions ×
  {inherited, movement-null, movement-loop} × five profiles, 4 400 runs) as a
  pre-registered kill criterion, and it fired: **ρ = −0.071** on the
  *unfixed* movement attacker against the inherited one (record: −0.893 at
  10 seeds; factor 9's contemporaneous null −0.821 at 10 seeds). The movement
  attacker's ordering is unchanged from the record (severance ≫ diversity:
  IP 93 %, CTS 91 %, OS 8 %, Service 29 %). **The inherited attacker's is
  not:** OS Diversity's suppression of it fell 89 % → 58 %, IP Shuffle's rose
  22 % → 68 %, Complete Topology's 18 % → 56 %; Service Diversity alone still
  annihilates it (94 %).
- **Every headline artefact predates the substrate restoration.** Experiment
  2's rows are dated 2026-07-29, factor 9's 2026-08-03, the targeted probe's
  2026-08-25; `d127f443` (2026-08-27) made OS Diversity a selective redraw
  (D-18 repaired), reinstated the OS-gated exploit success channel (D-19),
  restored HTS / UserShuffle / PortShuffle to the pool and withdrew DAP, and
  re-baselined every substrate golden. No record re-measured the inherited
  attacker's defence response after it. The token-hold record is the first,
  and it did so incidentally.
- **Two things changed at once, and the second is a confound of its own.**
  The `single` conditions' meaning is stable (one named mechanism). The
  `random` / `simultaneous` / `alternative` conditions now draw from a
  seven-mechanism pool where experiment 2's drew from four — they are
  different conditions, not re-measurements.
- **What is sayable today.** The movement attacker's severance-vs-diversity
  pattern is robust (to the loop fix, and to the substrate change). The claim
  "the defence ranking inverts between the two attackers" is **not** sayable
  on the current substrate until this brief runs. The fixed attacker
  (`fresh_host_contract`, the reported configuration since 2026-08-30) does
  not change the movement ordering, so this is not about the fix.

## Recommended approach

1. **Decompose `d127f443` on the inherited attacker only** (it is the arm that
   moved): re-run the four single conditions × 50 seeds × 200 s for the
   inherited attacker at each of (a) HEAD, (b) HEAD with D-18's selective
   redraw reverted to the full redraw, (c) HEAD with D-19's OS gate
   commented out again, (d) both — as *diagnostic* toggles on a scratch
   branch, never committed as inputs. Which toggle restores OS Diversity to
   ~89 % and IP Shuffle to ~22 % names the cause. Prior, stated for
   falsification: D-19 (the OS gate refuses exploits the inherited attacker
   used to land, so a topology/IP change now costs it more; OS Diversity's
   selective redraw changes fewer services, so it costs less).
2. **Re-run experiment 2 proper on HEAD** with its own harness
   (`data/results/expo02_ashen_lynx/run_experiment.py`; the movement arms pick
   up the contract by default) at 50 seeds, both intervals, and re-score
   E1–E9 against its pre-registration; record the multi-scheme pool change as
   a declared divergence in the conditions.
3. **Re-baseline the records that quote −0.893**: `experiment_02_findings.md`
   (banner, not rewrite), `fsm_alignment_prereg.md` / `fsm_succession_prereg.md`
   (their B5 nulls were contemporaneous and stand as measured, banner only),
   `hypothesis_tree.md`, `evaluation_predesign.md`, `apt_model_criterion.md`
   row B and axis-3 prose, `demonstration_arms_cross_examination.md`, and the
   ch5 notes / `dissertation.tex` wherever the inversion is stated.
4. **Return the thesis pointer**: does H2 (the inversion) survive as a
   *family* contrast (movement: severance strong / diversity weak; inherited:
   the reverse) on the restored substrate, and at what ρ; if not, what the
   restored substrate says the two attackers disagree about (today: only
   Service Diversity separates them).

Alternatives considered: treating the token-hold record's stage B as the
re-run (no — it has no 2 000 s interval, no verdict-blind / learning arms, and
its multi conditions are the new pool); reverting `d127f443` (no — it repaired
ruled bugs; the question is what the *correct* substrate says).

## Validation gate

The four-toggle table on the inherited attacker; experiment 2's E1–E9 re-scored
on HEAD with CIs; every record in step 3 bannered; the register gains the
ruling trail; `pytest tests/` green; no golden moves without a CHANGELOG entry.

## Hard constraints

- Diagnostic toggles are scratch-only; nothing in `mtdnetwork/` changes
  without a disposition.
- Report the numbers whichever way they fall; the inversion is a finding, not
  a requirement.
- Branch / commit / no-push per [`../workflows/session_workflow.md`](../workflows/session_workflow.md).

## Reading list

1. [`../implementation/pipeline/ogasp/fsm_token_hold_findings.md`](../implementation/pipeline/ogasp/fsm_token_hold_findings.md) H0 (the numbers and tables).
2. `git show d127f443` and the MTD-pool-restoration record it names; `docs/implementation/intent_conformance_audit.md` D-18 / D-19.
3. [`../implementation/pipeline/ogasp/experiment_02_findings.md`](../implementation/pipeline/ogasp/experiment_02_findings.md) §1–§9 (the pre-registration and the headline as recorded).
4. `data/results/expo02_ashen_lynx/{run_experiment,analyse}.py`; `data/results/fsm_token_hold/analyse.py` (the E5 construction, verbatim).
