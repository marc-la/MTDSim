# Experiments

One folder per experiment. Each holds the runner (`run_*.py`, `run_*.sh`), the
analyser that summarises its raw runs (`analyse.py` and similar), and the
`*numbers*.json` summaries the figure and table generators read. The raw runs
(`runs*.jsonl`, 75 GB in all) are not in git; see "Raw runs" below.

Every row a runner writes is `{**job, "termination_time": ..., results}`: the
row records its own inputs (arm, profile, MTD condition, deployment interval,
seed, ...), so any row can be re-run on its own and compared.

## What feeds the dissertation

| Folder | Dissertation | Runs | Run time | Runner → analyser → numbers |
|---|---|--:|--:|---|
| `ch5_s531_unopposed/` | §5.2, no MTD | 6 000 | 9 min | `run_corpus.py` (`REPORTED=1`) → `analyse.py` (`CORPUS=reported`) → `numbers_reported.json` |
| `ch5_defended/` | §5.3, both attackers under MTD | 402 000 | ≈ 28 h | `run_reported.sh` → `analyse.py`, `time_lost.py`, `time_lost_first_deployment.py` → `numbers_reported.json`, `time_lost_numbers_reported.json` |
| `ch5_defended/` | §5.4 ablations, failure matrix | 39 600 | 1.1 h | `run_ablations_1000.sh` → `ablation.py` (`MEMORY=1`) → `ablation_numbers_memory.json` |
| `ch5_defended/` | §5.4 / Table D.8, vulnerability memory | 129 600 | 5.5 h | `run_ablations_1000.sh` → `memory_ablation.py` → `memory_ablation_numbers.json` |
| `ch5_defended/` | §5.4 / Tables D.6–D.7, attack profiles and random partitions | 94 500 + redraw | 2.7 h + redraw | `run_partition_control.sh`, `run_partition_control_redraw.sh` → `partition_control.py`, `partition_ablation.py` |
| `ch5_defended/` | Table D.10, ranking across the 45 s band | 88 000 | 4.2 h | `run_duration_ranking.sh` → `duration_ranking.py` → `duration_ranking_numbers.json` |
| `ch5_s51_sensitivity/` | Appendix D, tactic-duration sensitivity | 33 000 | 1.3 h | `run_sweep.py` → `analyse.py` → `numbers.json` |
| `ch6_further_analyses/` | Appendix D.6, tactic-duration ablation | 8 000 | 16 min | `run_duration_ablation.py` → `analyse_duration_ablation.py`, `further_analyses.py` |

Run times are on one laptop (Intel i7-1360P, 7 worker processes, 13 GB RAM,
WSL2), from each runner's log. The shell wrappers log the commit each run
started from. `make runs` runs them all in order; `make numbers` re-runs every
analyser.

`ratio_fix/` is a repair applied to the two reported ledgers on 2026-10-06: the
1 110 baseline-attacker rows that the inherited 80 % stop had cut short were
re-run under the targeted scenario and spliced in, each new row required to
extend the old one's record stream. A fresh `run_reported.sh` at the current
code produces the spliced ledgers; `make verify` checks this on sampled rows.

`rate_feasibility_study/run_study.py` holds the duration-catalogue helpers the
sensitivity and duration-ranking runners import. `s45_metric_redesign/`,
`targeted_attacker_build/` and `vulnerability_memory_mechanism/` are the
design studies behind §4.5, the targeted scenario and §4.4.4; their records are
in `docs/implementation/pipeline/ogasp/`. The `numbers.json`, `ablation_numbers.json`
and `time_lost_numbers.json` files in `ch5_defended/` and `ch5_s531_unopposed/`
are the 100-seed preliminary reads; the dissertation reports the 1 000-seed
`*_reported` files.

## Checking that the runs reproduce

```sh
make smoke     # seed 0 of both reported corpora (408 runs), against the committed rows; ~2 min
make verify    # 20 random rows of each of the nine raw ledgers; needs the raw runs
```

`verify_ledgers.py` re-runs each sampled row's job at the current commit and
compares the new JSON line with the recorded one, byte for byte. At the
submitted commit: 408 of 408 smoke rows, 180 of 180 sampled rows across the nine
ledgers, and 400 of 400 across the two reported corpora reproduced exactly.

## Raw runs

The ledgers are too large for git (the defended corpus alone is 27 GB). Their
SHA-256 sums are in [`RAW_RUNS.sha256`](RAW_RUNS.sha256). The archive's DOI is
added here when it is published; unpack it so the files sit at
`experiments/<folder>/runs*.jsonl` and run `make check-raw`, or pass `--runs-dir`
to `verify_ledgers.py`.
Without them, `make smoke` and `make floats` still run: the first re-runs
committed rows, the second draws every float from the committed numbers files.
