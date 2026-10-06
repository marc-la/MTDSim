#!/usr/bin/env python3
"""Redraw the random partitions that hold a group which compromises nothing (2026-10-07).

Why. The size-matched control (src/mtdsim/l3_simulation/petri/partition_control.py) keeps
a draw when every group's token can reach initial-access. That test passes trivially for a
group with no reconnaissance place, whose token starts at initial-access, and it passes for
a group that reaches initial-access only rarely. At 1 000 seeds six of the forty groups
compromise nothing with no MTD (NCR 0.000): five with no reconnaissance place (partitions
p00, p01, p03, p07, p09) and p00's objective_impact slot, whose reconnaissance has its own
edge to command-and-control, so the overlay's bridge carries one-tenth of the weight and the
token wanders the post-intrusion tactics without a foothold (initial-access attempted 5 times
in 50 runs). A group that can never compromise is not "the same attack flows, grouped by
chance": it tests the build, not the grouping. Marc ruled the redraw (option 2) on 2026-10-06.

Rule. A draw is kept only if every group meets the existing criterion and two more, which
every real profile meets:
  1. its token starts at reconnaissance, as every real profile's does (the pre-intrusion
     overlay's entry);
  2. it compromises at least one host in at least one of SCREEN screening runs with no MTD,
     on seeds 1 000 to 1 099, outside the reported seeds 0 to 999 so the screen never reads
     the runs it admits.
Rule 2 is the minimal one that removes the defect: it rejects only a group that never
compromises, and admits a weak group as it stands.

What changes. Only the five partitions that hold a dead group are replaced, each by the next
draw of the same seeded stream (partition_stream, after the last draw the original build took)
that passes the rule, in index order; the five clean partitions (p02, p04, p05, p06, p08)
keep their nets and their 1 000-seed runs. Each replacement is built into its original index
directory (the superseded nets stay in git history), and the manifest records the superseded
draws, the screened draws with the reason each failed, and the rule.

    PYTHONPATH=src python data/results/ch5_defended/redraw_partition_control.py
Then run the replacements into their own stream (the original rows of these partitions stay in
runs_partition_control.jsonl and partition_control.py drops them):
    PYTHONPATH=src SEEDS=1000 PARTITIONS=0,1,3,7,9 OUT=data/results/ch5_defended/runs_partition_control_redraw.jsonl \\
        python data/results/ch5_defended/run_partition_control.py
"""
from __future__ import annotations

import json
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_corpus as rc  # noqa: E402

from mtdsim.l3_simulation.movement.net import load_routing_net  # noqa: E402
from mtdsim.l3_simulation.petri import partition_control as pc  # noqa: E402

REPO = HERE.parents[2]
MANIFEST = pc.MANIFEST
REPLACE = (0, 1, 3, 7, 9)
SCREEN_SEEDS = range(1_000, 1_100)
STAGE = REPO / "data" / "ogasp" / "partition_control" / "_screen"


def _screen_job(petri_dir: str, slot: str, seed: int) -> dict:
    return {**rc._job("partition_control_screen", "movement", slot, "targeted", "none", 0,
                      "shifted", rc.OVERLAY, seed),
            "petri_dir": petri_dir, "exploit_learning_rate": rc.MEMORY_RATE}


def check(d: Path, pool: ProcessPoolExecutor) -> dict:
    """slot -> the first failed rule, or None; plus the screen's hosts per slot."""
    rel = str(d.relative_to(REPO))
    out = {}
    for slot in pc.SLOTS:
        if load_routing_net(slot, petri_dir=d).entry_place != "reconnaissance":
            out[slot] = "token starts at initial-access (no reconnaissance place)"
        elif not pc.token_reaches_initial_access(d, slot):
            out[slot] = "token cannot reach initial-access"
    live = [s for s in pc.SLOTS if s not in out]
    jobs = [_screen_job(rel, s, seed) for s in live for seed in SCREEN_SEEDS]
    rows = list(pool.map(rc.dispatch, jobs, chunksize=4))
    errors = [r for r in rows if "error" in r]
    if errors:
        raise SystemExit(f"screen errors: {errors[:2]}")
    hosts = {s: sum(r["compromised"] for r in rows if r["profile"] == s) for s in live}
    for s in live:
        out[s] = None if hosts[s] > 0 else f"compromises nothing in {len(SCREEN_SEEDS)} screening runs"
    return {"failed": {s: v for s, v in out.items() if v}, "screen_hosts": hosts}


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    old = {p["partition"]: p for p in manifest["partitions"]}
    last = manifest["draws_taken"] - 1
    guard, stratified = manifest["guard"]["used"], manifest["shuffle"]["stratified"]
    stream = pc.partition_stream(stratified=stratified)
    for _ in range(last + 1):
        next(stream)
    if STAGE.exists():
        shutil.rmtree(STAGE)
    accepted, screened = [], []
    real_label = {f: slot for slot, fs in pc.real_assignment().items() for f in fs}
    with ProcessPoolExecutor(7) as pool:
        draw = last
        while len(accepted) < len(REPLACE):
            draw += 1
            assignment = next(stream)
            d = STAGE / f"d{draw:03d}"
            pc.build_petri_dir(assignment, d, guard=guard,
                               provenance={"draw": draw, "partition_seed": pc.PARTITION_SEED,
                                           "guard": guard, "stratified": stratified, "screen": True})
            res = check(d, pool)
            screened.append({"draw": draw, **res})
            print(f"  draw {draw}: " + ("kept" if not res["failed"] else f"rejected {res['failed']}")
                  + f"  screen hosts {res['screen_hosts']}", flush=True)
            if not res["failed"]:
                accepted.append((draw, assignment, res["screen_hosts"]))
    shutil.rmtree(STAGE)

    superseded = []
    for i, (draw, assignment, hosts) in zip(REPLACE, accepted):
        d = pc.OUT_DIR / f"p{i:02d}"
        superseded.append({"partition": i, "draw": old[i]["draw"],
                           "groups": {s: old[i]["groups"][s]["n_flows"] for s in pc.SLOTS}})
        shutil.rmtree(d)
        stats = pc.build_petri_dir(
            assignment, d, guard=guard,
            provenance={"partition": i, "draw": draw, "partition_seed": pc.PARTITION_SEED,
                        "guard": guard, "stratified": stratified, "redrawn": "2026-10-07"})
        kept = sum(real_label[f] == slot for slot, fs in assignment.items() for f in fs)
        old[i] = {"partition": i, "draw": draw, "petri_dir": str(d.relative_to(REPO)),
                  "flows_keeping_real_label": kept, "groups": stats,
                  "redrawn": {"date": "2026-10-07", "screen_hosts": hosts}}
        print(f"  p{i:02d} <- draw {draw}")
    manifest["partitions"] = [old[i] for i in sorted(old)]
    manifest["draws_taken"] = draw + 1
    manifest["redraw_2026_10_07"] = {
        "why": "six of forty groups compromised nothing at 1 000 seeds with no MTD: five with no "
               "reconnaissance place (their token starts at initial-access, which the original "
               "criterion passes trivially) and p00 objective_impact (reconnaissance's own edge to "
               "command-and-control leaves the overlay's bridge one-tenth of the weight). Ruled by "
               "Marc 2026-10-06 (option 2: redraw and re-run).",
        "rule": "a draw is kept only if every group (1) seeds its token at reconnaissance, (2) can "
                "reach initial-access (the original criterion), and (3) compromises at least one host "
                f"in at least one of {len(SCREEN_SEEDS)} screening runs with no MTD on seeds "
                f"{SCREEN_SEEDS.start}-{SCREEN_SEEDS.stop - 1} (outside the reported seeds); every real "
                "profile meets all three",
        "replaced": superseded,
        "screened": screened,
        "runs": "data/results/ch5_defended/runs_partition_control_redraw.jsonl; the replaced "
                "partitions' original rows stay in runs_partition_control.jsonl and are dropped by "
                "partition_control.py",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"  manifest -> {MANIFEST.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
