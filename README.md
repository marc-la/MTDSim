# MTDSim with an APT attacker model

Code, data and results for the UWA honours dissertation *Evaluating moving target
defence against advanced persistent threat attackers modelled on documented
intrusion campaigns* (Marc Labouchardiere, 2026; supervisor Jin B. Hong).
The dissertation is [`docs/dissertation.pdf`](docs/dissertation.pdf); the seminar
slides are [`docs/seminar.pdf`](docs/seminar.pdf).

MTDSim is a discrete-event simulator in which an attacker works through a
generated enterprise network while moving target defence (MTD) mechanisms
reshuffle it. It was built by Brown, Zhang, Ho and Tay ([`docs/lineage/`](docs/lineage/)).
This repository adds an **APT attacker model**: 38 documented intrusion campaigns
(MITRE CTID Attack Flow) aggregated into an attack graph of ATT&CK techniques, cut
into four attack profiles by objective, compiled into Petri nets, and run inside
MTDSim in place of its baseline attacker. Chapter 5 compares the two attackers
under seven MTD mechanisms, two deployment strategies and MTDShield over 1 000 seeds.

## Layout

| Path | What it holds |
|---|---|
| [`src/mtdnetwork/`](src/mtdnetwork/) | the simulator inherited from the lineage, with the defects we repaired |
| [`src/mtdsim/`](src/mtdsim/) | the APT attacker model; its README maps each dissertation section to a package |
| [`data/`](data/) | inputs: the Attack Flow snapshot, the attack graph, attack profiles, Petri nets, tactic durations, the MTDShield agent |
| [`experiments/`](experiments/) | one folder per experiment: runner, analyser, and the numbers files the floats read |
| [`tools/`](tools/) | the figure and table generators (`build_floats.py` runs them all) and developer tools |
| [`tests/`](tests/), [`baseline/`](baseline/) | unit and regression tests; golden event streams that pin the simulator's behaviour |
| [`docs/thesis/`](docs/thesis/) | the dissertation's LaTeX source, figures and tables |
| [`docs/implementation/`](docs/implementation/) | design records: architecture, data schemas, pre-registrations and findings for each design choice |

## Install

Python 3.11 on Linux (the runs used 3.11.15). With conda:

```sh
conda env create -f environment.yml && conda activate mtdsim
python -m playwright install chromium        # only for the figures
```

or with a virtual environment: `python3.11 -m venv .venv && . .venv/bin/activate && make install`.
`requirements-lock.txt` pins the exact environment; `pyproject.toml` declares the
direct dependencies (`pip install -e .[all]` for a looser install). The figures
also need TeX Live (`pdflatex`) and Ghostscript.

## Quick start

```sh
make test      # fetches the ATT&CK bundle, then 1 024 tests, ~5-10 min (make test-all adds the slow grid)
make smoke     # re-run seed 0 of both reported corpora and compare with the recorded rows, ~2 min
```

Watch one run of the APT attacker model, event by event, under IP shuffle every 200 s:

```sh
PYTHONPATH=src python -m mtdsim.l3_simulation.trace objective_exfiltration \
  --mapping v2_partial --overlay-version v4_failure_only --retrace \
  --attack-objective targeted --scheme single --mtd IPShuffle --interval 200 --seed 0
```

`python -m mtdnetwork.trace` does the same for the baseline attacker.

## Reproducing the dissertation

Every run is seeded: the same commit, inputs and seed give the same run, byte for
byte. Reproduction comes in four levels, from cheapest:

| Command | What it reproduces | Needs | Time |
|---|---|---|---|
| `make floats` | every generated figure and table, from the committed numbers files | this repository | ~1 min |
| `make smoke` | 408 recorded runs (seed 0 of Chapter 5's corpora), compared byte for byte | this repository | ~2 min |
| `make verify` / `make numbers` | sampled runs from all nine raw ledgers; every numbers file from the raw runs | the raw runs (on request) | ~5 min / ~1 h |
| `make runs` | every simulation behind Chapters 5 and 6 (over 800 000 runs) | this repository | ~45 h on 7 cores |

Times are on a laptop (Intel i7-1360P, 13 GB RAM). [`experiments/README.md`](experiments/README.md)
lists each experiment with its run count, time and outputs.

| Dissertation float | Command (`python ...`) |
|---|---|
| Figures 2.1–2.3 | `tools/ch2_model_figures.py` |
| Table 2.4 | `tools/ch2_lineage_configurations_table.py` |
| Figure 3.1 | `tools/attack_matrix_figure.py` |
| Figure 3.2 | `tools/attack_flow_figure.py` |
| Figure 4.1 | `tools/ch4_overview_figure.py` |
| Figure 4.2 | `tools/ch4_attack_graph_figure.py` |
| Figure 4.3 | `tools/ch4_profile_reach_figure.py` |
| Figure 4.4 | `tools/gspn_gadget_figure.py` |
| Figure 4.5 | `tools/runtime_loop_figure.py` |
| Figure 4.6 | `tools/controller_mapping_figure.py` |
| Table 4.2 | `tools/dwell_catalogue_tables.py` |
| Figure 5.1, Table 5.2 | `tools/ch5_unopposed_figures.py` |
| Figure 5.2, Table D.2 | `tools/ch5_disruption_figure.py` |
| Figures 5.3, 5.4, D.1; Tables 5.3, D.3–D.5 | `tools/ch5_sweep_figures.py` |
| Tables 5.4, D.7 | `experiments/ch5_defended/ablation_table.py` |
| Table C.1 | `tools/gasp_structural_baseline.py --tex` |
| Figure C.1 | `tools/gap_appendix_figures.py --only gap_technique_core` |
| Figure C.2 | `tools/ch4_attack_profiles_figure.py` |
| Table C.2 | `tools/attack_action_times_table.py` |
| Table C.3 | `tools/failure_weight_decomposition_figure.py --layout tables` |
| Table C.4 | `tools/value_bases_table.py` |
| Table D.6 | `TABLE_ONLY=1 experiments/ch5_defended/partition_ablation.py` |
| Table D.8 | `experiments/ch5_defended/memory_ablation.py --table-only` |
| Table D.9 | `experiments/ch5_s51_sensitivity/analyse.py --tables-only` |
| Table D.10 | `tools/duration_ranking_table.py` |
| Table D.11 | `tools/further_analyses_tables.py` |

Tables 4.3 and 5.1, and the tables set inline in the text, are typed in
`docs/thesis/dissertation.tex`. `make thesis` builds the PDF.

## Extending it

- **Run the APT attacker model in a new study:** `mtdsim.l3_simulation.movement.run.run_movement(profile, seed=..., mtd_scheme=..., ...)` returns the run's records; `experiments/ch5_defended/run_corpus.py` shows the configuration Chapter 5 reports.
- **Add an MTD mechanism:** subclass `MTD` (`src/mtdnetwork/mtd/__init__.py`) beside the others in `src/mtdnetwork/mtd/`, and pass it through `custom_strategies`.
- **Change behaviour on purpose:** the golden streams in `baseline/` will fail; re-capture them with `PYTHONPATH=src python tools/mtd_golden_streams.py capture` and say why in `baseline/CHANGELOG.md`.
- **Find what something is for:** the design record for each choice is in `docs/implementation/pipeline/ogasp/`. Code comments that cite `docs/handoffs/` point at working notes that are not kept here (they are in the git history).

## Credits, licence, citation

The simulator in `src/mtdnetwork/` is the work of Alex Brown, Wenxiao Zhang, Wai
Him Ho and Joo Kai Tay ([Bsubs/MTDSim](https://github.com/Bsubs/MTDSim)); the
MTDShield agent in `data/mtdshield/` is Tay's. Licensed under MIT ([`LICENSE`](LICENSE)).
To cite this work, see [`CITATION.cff`](CITATION.cff).
