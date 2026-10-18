"""Check that the recorded runs reproduce: re-run a random sample of rows from
each raw ledger with the code at HEAD and compare each new row with the recorded
one, byte for byte.

Every ledger row is ``{**job, "termination_time": ..., results}``: the keys before
``termination_time`` are the run's whole input (arm, profile, condition, interval,
seed, ...). The row's job goes back through the same runner's ``dispatch`` and the
JSON line it produces must equal the recorded line.

    python experiments/verify_ledgers.py                 # 20 rows per ledger
    python experiments/verify_ledgers.py --n 100 --only defended_reported
    python experiments/verify_ledgers.py --runs-dir /path/to/copy/experiments
    python experiments/verify_ledgers.py --smoke         # no raw runs needed (~2 min)

``--smoke`` re-runs every row of the committed fixtures, seed 0 of the two
reported corpora (``experiments/*/smoke_seed0.jsonl.gz``: 6 + 402 rows).

The raw ledgers are not in git (README, "Raw runs"); ``--runs-dir`` points at
wherever they were unpacked, laid out as experiments/<name>/runs*.jsonl.
"""
from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import os
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent

# name -> (ledger path under experiments/, runner script, rows to skip)
_REPLACED = {0, 1, 3, 7, 9}  # partitions redrawn 2026-10-07; their old rows are superseded
LEDGERS = {
    "unopposed_reported": ("ch5_s531_unopposed/runs_reported.jsonl", "ch5_s531_unopposed/run_corpus.py", None),
    "defended_reported": ("ch5_defended/runs_reported.jsonl", "ch5_defended/run_corpus.py", None),
    "ablation_memory": ("ch5_defended/runs_ablation_memory.jsonl", "ch5_defended/run_corpus.py", None),
    "partition_control": ("ch5_defended/runs_partition_control.jsonl", "ch5_defended/run_corpus.py",
                          lambda row: row.get("partition") in _REPLACED),
    "partition_control_redraw": ("ch5_defended/runs_partition_control_redraw.jsonl",
                                 "ch5_defended/run_corpus.py", None),
    "memory": ("ch5_defended/runs_memory.jsonl", "ch5_defended/run_memory_ablation.py", None),
    "duration_ranking": ("ch5_defended/runs_duration_ranking.jsonl", "ch5_defended/run_duration_ranking.py", None),
    "sensitivity": ("ch5_s51_sensitivity/runs.jsonl", "ch5_s51_sensitivity/run_sweep.py", None),
    "duration_ablation": ("ch6_further_analyses/runs_duration_ablation.jsonl",
                          "ch6_further_analyses/run_duration_ablation.py", None),
}

SMOKE = {
    "unopposed_reported": ("ch5_s531_unopposed/smoke_seed0.jsonl.gz", "ch5_s531_unopposed/run_corpus.py"),
    "defended_reported": ("ch5_defended/smoke_seed0.jsonl.gz", "ch5_defended/run_corpus.py"),
}

_MODULES: dict[str, object] = {}


def _runner(script: str):
    """Load a runner by path once per process (runners import their siblings)."""
    if script not in _MODULES:
        path = HERE / script
        sys.path.insert(0, str(path.parent))
        spec = importlib.util.spec_from_file_location(f"runner_{len(_MODULES)}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _MODULES[script] = mod
    return _MODULES[script]


def _job(row: dict) -> dict:
    job = {}
    for k, v in row.items():
        if k == "termination_time":
            return job
        job[k] = v
    raise ValueError("row has no termination_time")


def _rerun(args: tuple[str, str]) -> tuple[bool, str]:
    script, line = args
    row = json.loads(line)
    runner = _runner(script)
    # a runner whose rows do not carry the whole job rebuilds it (run_sweep.py)
    job = runner.job_from_row(row) if hasattr(runner, "job_from_row") else _job(row)
    new = json.dumps(runner.dispatch(job))
    if new == line:
        return True, ""
    fresh = json.loads(new)
    if "error" in fresh:
        return False, f"{_job(row)} raised {fresh['error']}"
    keys = [k for k in {**row, **fresh} if row.get(k, "<absent>") != fresh.get(k, "<absent>")]
    return False, f"{_job(row)} differs in {keys}"


def sample(path: Path, n: int, rng: random.Random, skip) -> list[str]:
    """``n`` whole lines at random byte offsets (the line after each offset)."""
    size = path.stat().st_size
    lines: dict[int, str] = {}
    with path.open("rb") as fh:
        tries = 0
        while len(lines) < n and tries < 50 * n:
            tries += 1
            fh.seek(rng.randrange(size))
            fh.readline()  # finish the partial line
            start = fh.tell()
            raw = fh.readline()
            if not raw.endswith(b"\n"):
                continue
            line = raw.decode().rstrip("\n")
            row = json.loads(line)
            if "error" in row or (skip and skip(row)):
                continue
            lines[start] = line
    return list(lines.values())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=20, help="rows per ledger")
    ap.add_argument("--seed", type=int, default=0, help="sampling seed")
    ap.add_argument("--only", nargs="*", choices=sorted(LEDGERS))
    ap.add_argument("--runs-dir", type=Path, default=HERE, help="where experiments/<name>/runs*.jsonl live")
    ap.add_argument("--workers", type=int, default=min(7, os.cpu_count() or 4))
    ap.add_argument("--smoke", action="store_true", help="re-run every row of the committed seed-0 fixtures")
    args = ap.parse_args()
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

    failures = checked = 0
    for name in (SMOKE if args.smoke else args.only or LEDGERS):
        t0 = time.time()
        if args.smoke:
            rel, script = SMOKE[name]
            with gzip.open(HERE / rel, "rt") as fh:
                lines = [line.rstrip("\n") for line in fh]
        else:
            rel, script, skip = LEDGERS[name]
            path = args.runs_dir / rel
            if not path.exists():
                print(f"{name:26s} missing: {path}")
                failures += 1
                continue
            lines = sample(path, args.n, random.Random(f"{args.seed}:{name}"), skip)
        with ProcessPoolExecutor(args.workers) as pool:
            results = list(pool.map(_rerun, [(script, line) for line in lines]))
        bad = [msg for ok, msg in results if not ok]
        checked += len(lines)
        failures += len(bad)
        print(f"{name:26s} {len(lines) - len(bad):4d}/{len(lines)} rows identical  ({time.time() - t0:.0f}s)",
              flush=True)
        for msg in bad:
            print(f"    {msg}")
    print(f"{checked - failures} of {checked} sampled rows reproduce exactly")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
