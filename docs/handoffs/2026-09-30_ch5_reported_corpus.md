---
status: open — the corpus is complete (2026-10-02 00:18: 402 000 runs, 0 errors, every cell at 1 000);
  analysed (numbers_reported.json, time_lost_numbers_reported.json); the §5.3 floats regenerated in the
  working tree but NOT committed: they use \grouprow/\grouplabel, which exist only in a parallel session's
  uncommitted table-style work (dissertation.tex preamble, both generators). Commit them with that work.
  Left: that commit; Marc's \prelim numbers (§5.3.1's baseline time lost is now negative and told apart
  from zero under four mechanisms; port shuffle costs the APT attacker model 26 s, told apart from zero)
created: 2026-09-30
---

# The §5.2–§5.3 floats from the reported corpus (1 000 seeds, vulnerability memory on)

## State of play

- **Marc, 2026-09-30:** "let's run the full 1000 seeds"; "the vulnerability memory
  should be on ... and it's ablated away, so I imagine all the seeds would change";
  "don't worry about the ablation study stuff yet"; "the prose is stale surrounding
  the diagram so we're just updating the diagrams, and then I'll update it once the
  numbers are in".
- **Why every seed is re-run, not 900 appended.** Table 5.1 declares the memory on
  for the APT attacker model (each earlier success triples the odds); both 100-seed
  corpora ran it off (`run_corpus.py` never passed `exploit_learning_rate`). The
  vulnerability-memory handoff's validation gate says the same ("the memory is on in
  the corpus that produces every ch5 number").
- **Running**, detached (`setsid nohup`), from the main checkout:
  `data/results/ch5_defended/run_reported.sh`. First the unopposed corpus
  (6 000 runs, about 8 minutes, log `ch5_s531_unopposed/run_reported.log`), then
  the defended corpus (402 000 runs, about 27 hours at 97 s a seed on 7 workers,
  log `ch5_defended/run_reported.log`, which prints hours left). Both write
  `runs_reported.jsonl` beside the 100-seed `runs.jsonl`, which stays: §5.4.1's
  ablation reads it.
- **What the corpora hold.** Unopposed: both attackers, the targeted objective at
  15 000 s (the 60 000 s extension and the general diagnostic are in no float and
  in no body sentence, only in tex comments). Defended: the core group, both
  attackers (c1-c4 and c_agg), no MTD once and the eleven conditions (seven singles,
  random, alternative, MTDShield, random over its four) at 50, 100, 200, 500,
  1 000 and 2 000 s. Seed-major, so a stopped run leaves whole seeds. Every
  APT row records `"exploit_learning_rate": 2.0`; the baseline's is null.
- **Checked before launch** (scratch probes, 2026-09-30):
  - current code re-runs 77 of 80 sampled 100-seed rows byte-identical; the three
    others are the baseline attacker under MTDShield;
  - cause, confirmed: `_baseline` built Tay's agent after seeding, and loading it in
    a fresh worker draws from the stream, so each worker's first baseline x
    MTDShield run differed (the old runner in a cold worker reproduces each recorded
    row). Fixed: the agent is built before seeding;
  - the agent's forward pass is traced once (`tf.function`, `_Compiled` in
    `run_corpus.py`): Q-values bitwise equal to eager on 1 965 decisions, the
    1 206-run pilot byte-identical; 45 ms a decision down to 1.2 ms (MTDShield was
    48 % of the compute);
  - 3-seed pilot: baseline rows equal the 100-seed corpus except the five cold-load
    rows; memory-on APT rows agree with the memory ablation's "on" arm at pool 20
    (36 of 36 cells); 506 of 1 005 APT rows changed with the memory on;
  - the analysers on the pilots: unopposed 258 MB peak at 40 seeds (2.4 GB at
    1 000, measured); defended 181 MB (lean summaries in reported mode). The
    defended analyser summarises about 5 ms a run on a free CPU (about 35 min for
    the corpus); run it after the corpus ends, not beside it.
  - a 20-seed dry run of §5.3 (analyser, time_lost, both generators, the build)
    passed in the detached worktree; it found the sweep figures' ticks laid from
    a -0.8 floor (fixed, 5db5b623).

## If the run stops

Re-run `data/results/ch5_defended/run_reported.sh`. The defended corpus resumes
from what `runs_reported.jsonl` holds (a line cut off by a kill is dropped); the
unopposed corpus is skipped if its log ends `unopposed exit 0`. Windows sleep
only pauses WSL; a reboot kills the run.

## When the run finishes

1. The logs end `exit 0` with `0 errors`; `wc -l` is 6 000 and 402 000.
2. `CORPUS=reported PYTHONPATH=src python data/results/ch5_s531_unopposed/analyse.py`
   and `CORPUS=reported PYTHONPATH=src:data/results/ch5_defended python
   data/results/ch5_defended/analyse.py`, then `CORPUS=reported python
   data/results/ch5_defended/time_lost.py`. Sanity: seeds 1 000, all cells full,
   0 error rows.
3. §5.2 is DONE (commit 50987f03: Figure 5.1, Table 5.2, Table C.4 from
   `ch5_s531_unopposed/numbers_reported.json`). For §5.3, point `NUMBERS` in
   `tools/ch5_disruption_figure.py` and `tools/ch5_sweep_figures.py` at the
   reported files and regenerate every float they write. A parallel session
   consolidated §5.3 on 2026-09-30 (441c7e6a: the ASP headline figure, the
   schemes figure and Table 5.4 left; `tab_F-0a` added), so take the float list
   from the tex, not from this file; the sweep generator still reads only
   `sweep`, `sweep_asp`, `ranking` and `sanity`, which the reported mode writes.
4. Build (pdflatex x2 + bibtex); render the changed pages; check each float
   against its numbers file.
5. Re-check the baseline rows at seeds 0-99 against `runs.jsonl` (only
   baseline x MTDShield may differ), and the memory-on cells against
   `runs_memory.jsonl` (on, pool 20).
6. Give Marc the old-to-new table for every `\prelim` number in §5.2-§5.3; the
   prose is his.

## Validation gate

Every §5.2-§5.3 float and Appendix C.4 and F drawn from `*_reported.json`; the
build clean; the sanity blocks at 1 000 seeds with no error row.

## Hard constraints

- The checkout's code must not change under the running workers: build and
  review in a worktree (`../MTDSim-k1000`, detached) until the run ends.
- No change to the baseline attacker; the memory off for it.
- Prose is Marc's (`\prelim` numbers stay until he updates them).

## Out of scope

- §5.4's ablations (still on memory-off corpora; the failure-matrix ablation reads
  seeds 0-99 from `runs.jsonl` and 100-999 from `runs_ablation.jsonl`). Flag, do not
  fix.
- §5.1 sensitivity; the effectiveness and efficiency generators (their floats left
  the thesis).

## Reading list

- `data/results/ch5_defended/run_corpus.py` (`build_reported_jobs`, `main_reported`)
- `data/results/ch5_defended/analyse.py` (docstring, `REPORTED`, `LEAN`)
- `docs/handoffs/2026-09-28_vulnerability_memory_on.md` (Marc's rulings; Part A)
- memory `seed_count_protocol`
