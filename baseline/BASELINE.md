# Baseline — Phase 0

> **Superseded.** This document captures the Phase-0 state of the substrate
> (buggy NCR=0.25, `finish_time=3000`, F-10 HCR>1, etc.). The goldens in
> [`golden/`](golden/) are the **post-2c** re-baseline on the corrected
> substrate; the matrix below and findings F-10 and F-09 are no longer
> current. For the canonical state, read
> [`CHANGELOG.md`](CHANGELOG.md) (2b and 2c entries) and
> [`../docs/specs/metrics_semantics.md`](../docs/specs/metrics_semantics.md). The
> Phase-0 goldens themselves are archived at
> [`golden_phase0_buggy/`](golden_phase0_buggy/). The text below is kept
> verbatim for provenance.

Status: **running, with the deviations below**. The codebase as it stands on `main`
(commit recorded in each `summary.json`) does not ship a runnable entry point — see
finding F-01. A minimal driver was written under [baseline/run_baseline.py](run_baseline.py)
to exercise one end-to-end simulation per scenario; this is the *absolute minimum* needed
to get one run to execute, per the Phase-0 brief.

All findings here are documented, not fixed. They feed into the Phase-1 spec.

---

## Branch & repo state

- Branch: `chore/baseline-spec` (off `main` at HEAD `c706871 add claude.md`).
- The working tree on `main` carries CRLF↔LF flips across ~40 tracked files (no
  content diff under `git diff -w`). Recorded as finding **F-09**; not committed.
- A pre-existing stash entry (`stash@{0}: On attacker-profiling: wip: .gitignore
  line-ending flip`) was left untouched.

---

## Environment

| Item | Documented (README / `environment.yml`) | Actually used | Deviation |
|---|---|---|---|
| Conda env name | `mtdsimtime` | `mtdsim` (pre-existing on this machine) | yes |
| Python | 3.9.13 | 3.11.15 | yes |
| OS | (unspecified) | Linux WSL2 (Ubuntu) | n/a — Windows-only `pywin32` dep can't install on Linux (finding F-02) |
| simpy | (not pinned in conda deps; pip pinned to 4.0.1) | 4.1.1 | yes |
| networkx | 2.5.1 | 3.6.1 | yes |
| numpy | 1.20.2 | 2.4.3 | yes |
| scipy | 1.6.3 | 1.17.1 | yes |
| pandas | 1.2.4 | 3.0.2 | yes |
| matplotlib | 3.4.1 | 3.10.8 | yes |
| seaborn | 0.12.0 | (not installed in env; imported in `statistic/evaluation.py` but only used inside unreached plot helpers) | n/a |
| tensorflow | (not in `environment.yml`) | (not installed) | the deleted `experiments/run.py` imported it at module top — finding F-03 |

The README's documented setup (`conda env create -f environment.yml`,
`conda activate mtdsimtime`) was not executed; the env it would build is Python
3.9.13 + Windows-only `pywin32` + pins from 2021. The pre-existing `mtdsim` env on
this machine satisfies the actual import surface that the baseline driver exercises.

---

## Entry point

There is no entry point on `main`. Per `git log`:

- `mtdnetwork/run.py` — last existed in commit `1020e6d` (2022-09-09, upstream
  Brown-era), removed in the "Updating folder structures and files" refactor.
- `experiments/run.py`, `experiments/run_trials/run_experiment.py`,
  `batchrun.py`, `playground.py`, `jookai_ddqn_walkthrough.ipynb` — all deleted
  in `e5935ab` "Deleting unnecessary hangover experimental files from previous
  works" (2026-03-27). 734 files removed in that commit.
- `src/mtdsim/` exists as scaffolding (each subdirectory contains only
  `__pycache__/` bytecode; no `.py` sources committed). This appears to be the
  WIP restructure target mentioned in the project memory.

The pre-deletion `experiments/run.py` imported TensorFlow unconditionally at
module top (for the MTD-AI / DDQN code paths), so restoring it verbatim would
require an additional ~hundreds of MB of deps for code paths that aren't
exercised by the no-MTD or rule-based MTD scenarios. Instead,
[baseline/run_baseline.py](run_baseline.py) calls the same modules the deleted
driver did (`TimeNetwork`, `Adversary`, `AttackOperation`, `MTDOperation`,
`Evaluation`) without the TF or threading layer.

The driver exposes six preset scenarios:

| scenario | scheme | mtd_interval | custom_strategies |
|---|---|---|---|
| `no-mtd` | `None` | n/a | n/a |
| `single-ipshuffle` | `single` | 200 | `IPShuffle` |
| `single-osdiversity` | `single` | 200 | `OSDiversity` |
| `random-multi` | `random` | 200 | (default set: CompleteTopologyShuffle, IPShuffle, OSDiversity, ServiceDiversity) |
| `alternative-multi` | `alternative` | 200 | (default set) |
| `simultaneous-multi` | `simultaneous` | 700 | (default set) |

Other simulation parameters (defaults from the deleted driver's
`execute_simulation`): `total_nodes=50, total_endpoints=5, total_subnets=8,
total_layers=4, target_layer=4, total_database=2,
terminate_compromise_ratio=0.8`. Simulated `finish_time=3000`.

---

## Commands run

From the repo root, with the `mtdsim` conda env on the PATH:

```bash
PYTHONPATH=. /home/marc/miniconda3/envs/mtdsim/bin/python -u baseline/run_baseline.py \
    --scenario no-mtd            --seed 1234 --finish-time 3000
PYTHONPATH=. ... --scenario single-ipshuffle    --seed 1234 --finish-time 3000
PYTHONPATH=. ... --scenario single-osdiversity  --seed 1234 --finish-time 3000
PYTHONPATH=. ... --scenario random-multi        --seed 1234 --finish-time 3000
PYTHONPATH=. ... --scenario alternative-multi   --seed 1234 --finish-time 3000
PYTHONPATH=. ... --scenario simultaneous-multi  --seed 1234 --finish-time 3000

# determinism check (same seed, separate run):
PYTHONPATH=. ... --scenario no-mtd --seed 1234 --finish-time 3000 \
    --out-root baseline/golden_repeat       # → baseline/golden/no-mtd_seed1234_repeat/
PYTHONPATH=. ... --scenario no-mtd --seed 9999 --finish-time 3000 \
    --out-root baseline/golden_seed9999     # → baseline/golden/no-mtd_seed9999/
```

The `PYTHONPATH=.` is required because the package is installed only via
`setup.py` with `find_packages()` from the repo root; nothing on `main` ships a
proper `src/`-layout install or a console-script entry point.

---

## Seeds & determinism

Two RNG sources are seeded by the driver before constructing the network:

- `random.seed(1234)` — controls all `random.*` calls in `network.py`,
  `host.py`, `mtd_scheme.py`, `mtd/*.py`, `time_network.py`.
- `numpy.random.seed(1234)` — controls `scipy.stats.*` distributions used by
  `time_generator.py` (exponential / normal / uniform / weibull / poisson rvs)
  and by `MTDOperation` interval sampling.

The codebase contains no centralised seed hook (no `set_seed`/`seed=` is
threaded through `TimeNetwork.__init__`, even though the base `Network` class
has a `seed=None` parameter that's only honoured if the caller passes it
through; `TimeNetwork.__init__` does not — **finding F-04**).

**Determinism result (no-MTD scenario, seed=1234, two consecutive runs):**

- `summary.json` differs only in `sim_wallclock_seconds` (expected).
- `attack_record.csv` differs in 764 of 769 lines.
- All 764 diff lines contain a UUID4 hex pattern — **the differences are
  exclusively in the per-host `uuid` field**, produced by `uuid.uuid4()`
  (`mtdnetwork/component/host.py:50`), which uses `os.urandom` and is not
  affected by `random.seed`. All timestamps, durations, host IDs, attack
  action sequence, and cumulative compromise counts match byte-for-byte across
  the two runs.

Conclusion: **the simulation is functionally deterministic once
`random.seed` + `numpy.random.seed` are both set**; the non-deterministic
`uuid.uuid4` calls are not load-bearing for any metric or for the action flow.
Recorded as finding **F-05**.

The two-seed sanity check (`no-mtd`, seeds 1234 vs 9999) confirmed the seed has
real effect: 384 vs 361 attack events, 17 vs 22 compromised hosts.

---

## Run matrix — headline results

(`finish_time=3000`, `terminate_compromise_ratio=0.8`, 50-node network,
seed=1234 unless stated. None of the runs hit the compromise threshold within
the sim window — every scenario ran for the full 3000 time units.)

| scenario | attack events | MTD events | compromised hosts | ratio |
|---|---|---|---|---|
| `no-mtd` | 384 | 0 | 17 | 0.34 |
| `single-ipshuffle` | 331 | 15 | 9 | 0.18 |
| `single-osdiversity` | 328 | 15 | 13 | 0.26 |
| `random-multi` | 359 | 15 | 7 | 0.14 |
| `alternative-multi` | 328 | 12 | 16 | 0.32 |
| `simultaneous-multi` | 323 | 16 | 16 | 0.32 |
| `no-mtd` (seed=1234, repeat) | 384 | 0 | 17 | 0.34 |
| `no-mtd` (seed=9999) | 361 | 0 | 22 | 0.44 |

Per-scenario detail: see [golden/<scenario>/summary.json](golden/) and the
CSV/PNG artefacts beside it.

---

## Phase-0 findings

These are the issues encountered while getting one run to execute. They are
documented here, **not fixed** — they feed Phase 1's disposition column.

- **F-01 — No runnable entry point on `main`.** The README still documents
  `python -m mtdnetwork.run -m IPShuffle -n 50 -e 10 -s 5 -l 3 results.json`
  and `python batchrun.py`, but `mtdnetwork/run.py` was removed in 2022 and
  `experiments/run.py` + `batchrun.py` + `playground.py` + the DDQN notebook
  were removed in commit `e5935ab` (2026-03-27). A new driver was written
  under `baseline/run_baseline.py` to drive the existing module surface.
- **F-02 — `environment.yml` is Windows-only.** Lists `pywin32` as a top-level
  dep, which has no Linux/macOS wheel. The README's documented setup will fail
  on the user's actual platform (WSL2). The pre-existing `mtdsim` env (Python
  3.11) was used instead.
- **F-03 — Hidden TensorFlow dependency in the deleted driver.** The last-known
  `experiments/run.py` imported `tensorflow.keras.models.load_model` at module
  top, so the rule-based / no-MTD code paths couldn't be exercised without
  installing TF. The new driver imports only what each scenario needs.
- **F-04 — Seeding is not centrally plumbed.** `Network.__init__` accepts a
  `seed=None` kwarg and calls `random.seed(seed)` only if it's passed
  (`network.py:45–46`); `TimeNetwork.__init__` does not forward `seed`, so
  there's no way to seed through the public constructor. `numpy.random` is
  never seeded anywhere in the package. The driver seeds both explicitly.
- **F-05 — Determinism is "byte-deterministic apart from UUIDs"** (see the
  Determinism section). The `uuid.uuid4()` call in `Host.__init__` uses
  `os.urandom`, so per-host UUIDs vary between runs even with both `random`
  and `numpy.random` seeded; nothing else does.
- **F-06 — Infinite loop in `Network.gen_graph` on poorly-chosen parameters.**
  With `total_subnets < total_layers + 1` or similar, the condition at
  `network.py:124` (`total_subnets - (sum + l_subnets) > layers - len`)
  cannot be satisfied — `l_subnets ∈ [1,5]` keeps shrinking the LHS below the
  RHS. A 10-node `(total_subnets=3, total_layers=2)` config hangs at 95% CPU
  with no progress message. No input validation guards this; the failure mode
  is silent. Defaults `(50, 5, 8, 4)` work in ~80 ms.
- **F-07 — `Evaluation.__init__` has unconditional filesystem side-effect.**
  `Evaluation.create_directories` (`statistic/evaluation.py:21`) calls
  `os.makedirs(directory + '/experimental_data/plots/', exist_ok=True)`
  using `directory = os.getcwd()` captured at *module import time*. Just
  constructing an `Evaluation` mkdirs into `<cwd>/experimental_data/plots/`
  unconditionally — see the new `experimental_data/plots/` directory left
  behind by the baseline runs. Not fixed.
- **F-08 — `Evaluation.visualise_*` methods have hard-coded path-join bugs
  and call `plt.show()`.** Lines such as `plt.savefig(directory +
  '/experimental_data/plots/',+ '/network.png')` (note the comma — that's a
  tuple passed to `savefig`) appear in `visualise_attack_operation`,
  `visualise_mtd_operation`, `draw_network`. These methods would crash if
  called. The driver writes its own figures around the broken helpers.
- **F-09 — Working tree carries CRLF↔LF flips across ~40 tracked files.** No
  content diff under `git diff -w`. Not committed by Phase 0. Origin is
  likely a Windows ↔ WSL editor round-trip; mirrors the existing stash entry.
- **F-10 — `Evaluation.evaluation_result_by_compromise_checkpoint` returns
  `host_compromise_ratio` values > 1.** The computation is
  `compromised_num(sub_record) / comp_num`, where `comp_num = host_num * comp_ratio`
  (so e.g. `50 * 0.05 = 2.5` for the 5 % checkpoint). It's the ratio of
  compromised hosts to the checkpoint *threshold*, not to the network size,
  yet the field is named like the latter. Multiple papers cite this column;
  worth flagging when extracting Ho's MTTC + ratio definitions.
- **F-11 — Two `MTDStatistics` classes live in the codebase.** One in
  `mtdnetwork/statistic/mtd_statistics.py` (used by `TimeNetwork`,
  `MTDOperation`), another in `mtdnetwork/statistic/scorer.py:103`. The
  scorer copy isn't reached by any baseline run but the dual definition is a
  rename-conflict trap for Phase 1+ work.

---

## Directory layout

```
baseline/
├── BASELINE.md                              ← this file
├── run_baseline.py                          ← Phase-0 driver
└── golden/
    ├── no-mtd/                              ← canonical baseline (seed=1234)
    │   ├── summary.json
    │   ├── attack_record.csv
    │   ├── attack_record.png
    │   ├── mtd_record.csv                   ← empty for no-mtd
    │   ├── evaluation.json
    │   └── network_initial.png
    ├── no-mtd_seed1234_repeat/              ← determinism check
    ├── no-mtd_seed9999/                     ← seed-sensitivity sanity check
    ├── single-ipshuffle/
    ├── single-osdiversity/
    ├── random-multi/
    ├── alternative-multi/
    └── simultaneous-multi/
```

The contents of `golden/` are the behavioural oracle for Phase 1 dispositioning
and any future faithfulness tests.
