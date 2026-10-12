"""Re-run the reported rows the inherited 80 % stop ended under the targeted
attack scenario, and splice them into their ledgers (handoff
2026-10-06_ch5_results_prose_redraft.md §14; Marc's disposition 2026-10-06).

The stop is a pure read of the share compromised, so a run changes only after
it would have stopped: the affected rows are the targeted rows with more than
40 of 50 hosts compromised (the stop fires above 0.8). Every re-run row must
carry the old row's record stream as a prefix, or the splice is refused. The
old ledger is kept beside the new one as ``*.pre_ratio_fix``.

    PYTHONPATH=src WORKERS=3 nice -n 19 python data/results/ratio_fix/rerun_ratio_fix.py
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LEDGERS = {
    "unopposed": ROOT / "data/results/ch5_s531_unopposed",
    "defended": ROOT / "data/results/ch5_defended",
}
COMP = re.compile(rb'"compromised": (\d+)')
WORKERS = int(os.environ.get("WORKERS", 3))


def _module(name: str, where: Path):
    spec = importlib.util.spec_from_file_location(f"rc_{name}", where / "run_corpus.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(where))
    spec.loader.exec_module(mod)
    return mod


def _affected(head: bytes) -> bool:
    if b'"arm": "baseline"' not in head and b'"profile": "baseline"' not in head:
        return False
    if b'"objective": "targeted"' not in head:
        return False
    m = COMP.search(head)
    return bool(m) and int(m.group(1)) > 40


def _job(row: dict) -> dict:
    # a row is {**job, "termination_time": ..., results}: the job is every key before it
    job = {}
    for k, v in row.items():
        if k == "termination_time":
            return job
        job[k] = v
    raise ValueError("row without termination_time")


def _key(job: dict) -> str:
    return json.dumps(job, sort_keys=True)


def _dispatch(args):
    name, job = args
    return MODS[name].dispatch(job)


MODS = {n: _module(n, p) for n, p in LEDGERS.items()}


def main() -> int:
    t0 = time.time()
    for name, where in LEDGERS.items():
        path = where / "runs_reported.jsonl"
        old = {}
        with open(path, "rb") as f:
            for line in f:
                if _affected(line[:800]):
                    row = json.loads(line)
                    old[_key(_job(row))] = row
        print(f"{name}: {len(old)} affected rows found ({time.time() - t0:.0f}s)", flush=True)
        jobs = [(name, _job(r)) for r in old.values()]
        new = {}
        with ProcessPoolExecutor(WORKERS) as pool:
            for i, row in enumerate(pool.map(_dispatch, jobs, chunksize=4), 1):
                if "error" in row:
                    print(f"  ERROR {row['error']} {_job(row)}", flush=True)
                    return 1
                k = _key(_job(row))
                o = old[k]["records"]
                if row["records"][: len(o)] != o:
                    print(f"  PREFIX BROKEN {k}", flush=True)
                    return 1
                new[k] = row
                if i % 100 == 0:
                    print(f"  {i}/{len(jobs)} re-run ({time.time() - t0:.0f}s)", flush=True)
        print(f"{name}: {len(new)} re-run, every old record stream a prefix ({time.time() - t0:.0f}s)", flush=True)
        tmp = path.with_suffix(".jsonl.ratio_fix_tmp")
        replaced = 0
        with open(path, "rb") as f, open(tmp, "wb") as g:
            for line in f:
                if _affected(line[:800]):
                    k = _key(_job(json.loads(line)))
                    g.write((json.dumps(new[k]) + "\n").encode())
                    replaced += 1
                else:
                    g.write(line)
        if replaced != len(new):
            print(f"{name}: SPLICE COUNT {replaced} != {len(new)}; ledger untouched", flush=True)
            tmp.unlink()
            return 1
        os.replace(path, path.with_suffix(".jsonl.pre_ratio_fix"))
        os.replace(tmp, path)
        print(f"{name}: spliced {replaced} rows; old ledger kept as {path.name}.pre_ratio_fix "
              f"({time.time() - t0:.0f}s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
