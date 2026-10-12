"""The size-matched, label-blind partition control — the run half.

Each of the K random partitions (data/ogasp/partition_control/, built by
``python -m mtdsim.l3_simulation.petri.partition_control``) splits the 38 attack
flows into four groups of the profiles' sizes (19 / 7 / 7 / 5), compiled exactly
as the profiles are and written under the profiles' names as slot names. This
runs every group at the five cells §5.4's profile ablation reads (no MTD; IP
shuffle and OS diversity at 200 s and 2 000 s) under the reported corpus's core
configuration: the APT attacker model, targeted objective on the database set,
quasi-periodic ("shifted") regime, failure-only overlay v4_failure_only,
mapping v2_partial, retrace on, the vulnerability memory on
(run_corpus.MEMORY_RATE), 15 000 s. The run itself is run_corpus.dispatch: the
job's ``petri_dir`` is the only difference from a reported-corpus row.

Seed-major, so a stopped run leaves whole seeds; resumable, keyed by
(partition, slot, condition, interval, seed). Environment:
  SEEDS=N        seeds 0..N-1 (default 100; then 1000)
  WORKERS=N      processes (default min(7, cpu count))
  LIMIT=N        timing probe: the first N jobs, written nowhere
  PARTITIONS=a,b only these partitions (default all K in the manifest)
  OUT=path       the output stream (default runs_partition_control.jsonl)

    PYTHONPATH=src SEEDS=100 python data/results/ch5_defended/run_partition_control.py
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_corpus as rc  # noqa: E402  (the corpus's job shape and dispatch)

REPO = HERE.parents[2]
MANIFEST = REPO / "data" / "ogasp" / "partition_control" / "partitions.json"
OUT = HERE / "runs_partition_control.jsonl"
GROUP = "partition_control"
CELLS = (("none", 0),) + tuple((c, i) for i in rc.INTERVALS for c in rc.SPANNING)


def load_partitions() -> list[dict]:
    manifest = json.loads(MANIFEST.read_text())
    for p in manifest["partitions"]:
        for slot in rc.FOUR:
            path = REPO / p["petri_dir"] / f"{slot}_structural.json"
            if not path.exists():
                raise SystemExit(f"missing {path}: rebuild the partitions first")
    return manifest["partitions"]


def build_jobs(seeds, partitions) -> list[dict]:
    """Seed-major: every partition, slot and cell of a seed before the next."""
    return [
        {**rc._job(GROUP, "movement", slot, "targeted", c, i, "shifted", rc.OVERLAY, seed),
         "partition": p["partition"], "petri_dir": p["petri_dir"],
         "exploit_learning_rate": rc.MEMORY_RATE}
        for seed in seeds for p in partitions for slot in rc.FOUR for c, i in CELLS
    ]


def job_id(row: dict) -> tuple:
    return (row["partition"], row["profile"], row["condition"], row["interval"], row["seed"])


_HEAD = re.compile(rb'"profile": "(\w+)", "objective": "\w+", "condition": "(\w+)", '
                   rb'"interval": (\d+), .*?"seed": (\d+), "partition": (\d+)')


def resume(path: Path) -> set:
    """The jobs already written (error rows included, so a dead cell stays
    visible and is not silently re-run). A line cut off by a killed run is
    dropped; only each row's head is read."""
    if not path.exists():
        return set()
    rc._truncate_cut_line(path)
    done = set()
    with path.open("rb") as fh:
        for line in fh:
            m = _HEAD.search(line[:1024])
            if m:
                pr, c, i, s, k = m.groups()
                done.add((int(k), pr.decode(), c.decode(), int(i), int(s)))
            else:  # an error row's message may push the job past the head
                done.add(job_id(json.loads(line)))
    return done


def main() -> int:
    partitions = load_partitions()
    if os.environ.get("PARTITIONS"):
        keep = {int(x) for x in os.environ["PARTITIONS"].split(",")}
        partitions = [p for p in partitions if p["partition"] in keep]
    jobs = build_jobs(range(int(os.environ.get("SEEDS", 100))), partitions)
    out = Path(os.environ.get("OUT", OUT))
    if os.environ.get("LIMIT"):  # timing probe: the first N jobs, not written
        jobs, out = jobs[: int(os.environ["LIMIT"])], Path(os.devnull)
    done_ids = set() if out == Path(os.devnull) else resume(out)
    todo = [j for j in jobs if job_id(j) not in done_ids]
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    print(f"{len(jobs)} runs ({len(partitions)} partitions x 4 groups x {len(CELLS)} cells x seeds), "
          f"{len(jobs) - len(todo)} already written, {len(todo)} to run on {workers} workers -> {out}",
          flush=True)
    started = time.time()
    done = errors = 0
    with open(out, "a", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(rc.dispatch, todo, chunksize=4):
            fh.write(json.dumps(row) + "\n")
            done += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if done % 500 == 0:
                fh.flush()
                el = time.time() - started
                print(f"  {done}/{len(todo)}  {el:.0f}s  (seed {row['seed']}; "
                      f"~{el / done * (len(todo) - done) / 3600:.1f} h left)", flush=True)
    print(f"done: {done} runs, {errors} errors, {time.time() - started:.0f}s")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
