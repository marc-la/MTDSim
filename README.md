# MTDSim

A simulator for evaluating moving target defence (MTD) techniques, with a Dash-based replay UI and attack graph visualiser.

## Quick start (Linux)

Requires [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) (or Anaconda).

```bash
conda env create -f environment.yml
conda activate mtdsim
pip install -e src
```

## Run the replay + attack graph visualiser

```bash
conda activate mtdsim
python -m mtdsim.viz.replay
```

Then open <http://127.0.0.1:8050>. The first launch auto-runs the default sim (`primary` config, `random` scheme) and caches the event log.

Useful flags:

- `--config {primary,demo}` — named config to auto-run
- `--scheme {no_mtd,random,alternative,simultaneous}`
- `--log PATH` — replay an existing `events.jsonl` instead of auto-running
- `--force-rerun` — regenerate the cached log
- `--port N` — change port (default 8050)

## Notebooks

```bash
python -m ipykernel install --user --name mtdsim --display-name "Python (mtdsim)"
```

Open any notebook in `notebooks/` and select the **Python (mtdsim)** kernel.

## Updating dependencies

```bash
conda env update --name mtdsim --file environment.yml --prune
```
