# One entry point for every job. Run `make help` for the list.
# Python is the active environment's; create it with `make install` (or environment.yml).

PY      ?= python
export PYTHONPATH := $(CURDIR)/src
export TF_CPP_MIN_LOG_LEVEL := 3

.PHONY: help install inputs test test-all smoke floats verify numbers runs thesis clean

help:
	@echo "make install    pinned environment (requirements-lock.txt) + this repo, editable + Chromium for figures"
	@echo "make inputs     fetch the ATT&CK 19.1 bundle (SHA-256 checked)                       ~1 min"
	@echo "make test       unit and regression tests (slow grid skipped)                         ~5 min"
	@echo "make test-all   the full grid, including the slow tests                               ~1 h"
	@echo "make smoke      re-run seed 0 of both reported corpora; must match the committed rows ~2 min"
	@echo "make floats     every generated figure and table from the committed numbers files    ~1 min"
	@echo "make verify     re-run 20 random rows of each raw ledger (needs the raw runs, README) ~5 min"
	@echo "make numbers    recompute every numbers file from the raw runs (needs the raw runs)   ~1 h"
	@echo "make runs       every simulation behind Chapters 5 and 6, from scratch                ~45 h on 7 cores"
	@echo "make thesis     build docs/thesis/dissertation.pdf (pdflatex + bibtex)"

install:
	$(PY) -m pip install -r requirements-lock.txt
	$(PY) -m pip install -e . --no-deps
	$(PY) -m playwright install chromium

inputs:
	$(PY) -m mtdsim.l0_cti

test:
	$(PY) -m pytest -q

test-all:
	$(PY) -m pytest -q --runslow

smoke:
	$(PY) experiments/verify_ledgers.py --smoke

floats: inputs
	$(PY) tools/build_floats.py

verify:
	$(PY) experiments/verify_ledgers.py --n 20

# Analysers, in dependency order: each reads raw runs and writes the numbers*.json
# files that `make floats` draws from. Run from the repository root.
numbers:
	CORPUS=reported $(PY) experiments/ch5_s531_unopposed/analyse.py
	CORPUS=reported $(PY) experiments/ch5_defended/analyse.py
	CORPUS=reported $(PY) experiments/ch5_defended/time_lost.py
	$(PY) experiments/ch5_defended/time_lost_first_deployment.py
	MEMORY=1 $(PY) experiments/ch5_defended/ablation.py
	$(PY) experiments/ch5_defended/memory_ablation.py
	$(PY) experiments/ch5_defended/partition_control.py
	$(PY) experiments/ch5_defended/partition_ablation.py
	$(PY) experiments/ch5_defended/duration_ranking.py
	$(PY) experiments/ch5_defended/seed_layer_check.py
	$(PY) experiments/ch5_s51_sensitivity/analyse.py
	$(PY) experiments/ch6_further_analyses/further_analyses.py
	$(PY) experiments/ch6_further_analyses/analyse_duration_ablation.py

# The recorded order (each wrapper logs its commit and timings beside its ledger).
runs:
	bash experiments/ch5_defended/run_reported.sh
	bash experiments/ch5_defended/run_ablations_1000.sh
	bash experiments/ch5_defended/run_partition_control.sh
	bash experiments/ch5_defended/run_partition_control_redraw.sh
	bash experiments/ch5_defended/run_duration_ranking.sh
	$(PY) experiments/ch5_s51_sensitivity/run_sweep.py
	$(PY) experiments/ch6_further_analyses/run_duration_ablation.py

thesis:
	cd docs/thesis && pdflatex -interaction=nonstopmode dissertation.tex >/dev/null && \
	  bibtex dissertation >/dev/null && \
	  pdflatex -interaction=nonstopmode dissertation.tex >/dev/null && \
	  pdflatex -interaction=nonstopmode dissertation.tex >/dev/null && \
	  echo "wrote docs/thesis/dissertation.pdf"

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -f docs/thesis/*.aux docs/thesis/*.bbl docs/thesis/*.blg docs/thesis/*.log docs/thesis/*.out docs/thesis/*.toc docs/thesis/*.lof docs/thesis/*.lot
