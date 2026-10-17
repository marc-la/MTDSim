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
	@echo "make verify     re-run 20 random rows of each raw ledger (needs the raw runs, README) ~15 min"
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
# files that `make floats` draws from.
numbers:
	cd experiments/ch5_s531_unopposed && CORPUS=reported $(PY) analyse.py
	cd experiments/ch5_defended && CORPUS=reported $(PY) analyse.py
	cd experiments/ch5_defended && $(PY) time_lost.py && $(PY) time_lost_first_deployment.py
	cd experiments/ch5_defended && $(PY) ablation.py && $(PY) memory_ablation.py
	cd experiments/ch5_defended && $(PY) partition_ablation.py && $(PY) duration_ranking.py
	cd experiments/ch5_defended && $(PY) seed_layer_check.py
	cd experiments/ch5_s51_sensitivity && $(PY) analyse.py
	cd experiments/ch6_further_analyses && $(PY) further_analyses.py && $(PY) analyse_duration_ablation.py

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
