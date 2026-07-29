"""Per-mechanism cost benchmark for the MTD defender pool.

    PYTHONPATH=src python tools/mtd_cost_bench.py                # the cost table
    PYTHONPATH=src python tools/mtd_cost_bench.py --profile OSDiversityAssignment
    PYTHONPATH=src python tools/mtd_cost_bench.py --seeds 0 1 2 --interval 3200

Reproduces the table in `docs/handoffs/2026-07-29_mtd_mechanism_cost_audit.md`.
Committed because that handoff's validation gate asks for the table to be
re-measured, and a re-measurement that used a different harness would not be
comparable with the numbers the handoff reasons from.

**Measurement, not experiment.** This runs the movement arm purely to time the
defender side; it computes no metric and writes no findings. Nothing here may
become evidence for a claim — the run workspaces under `data/results/` are for
that.

One thing worth knowing before reading its output: wall clock per run is
sensitive to how loaded the machine is, and this project routinely has several
sessions running at once. Run it on an idle machine, or read the ratios rather
than the absolute seconds — the ratio column is what the grid arithmetic uses.
"""
from __future__ import annotations

import argparse
import cProfile
import io
import pstats
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from mtdnetwork.mtd.completetopologyshuffle import CompleteTopologyShuffle  # noqa: E402
from mtdnetwork.mtd.hosttopologyshuffle import HostTopologyShuffle  # noqa: E402
from mtdnetwork.mtd.ipshuffle import IPShuffle  # noqa: E402
from mtdnetwork.mtd.osdiversity import OSDiversity  # noqa: E402
from mtdnetwork.mtd.osdiversityassignment import OSDiversityAssignment  # noqa: E402
from mtdnetwork.mtd.portshuffle import PortShuffle  # noqa: E402
from mtdnetwork.mtd.servicediversity import ServiceDiversity  # noqa: E402
from mtdnetwork.mtd.usershuffle import UserShuffle  # noqa: E402

from mtdsim.l3_simulation.movement.run import run_movement  # noqa: E402

# All eight, in the order the handoff's table reports them. Four of these are
# commented out of MTDScheme's own default pool and are only ever exercised when a
# grid names them explicitly, which is exactly why they are all listed here.
MECHANISMS = {
    "CompleteTopologyShuffle": (CompleteTopologyShuffle, True),
    "HostTopologyShuffle": (HostTopologyShuffle, False),
    "IPShuffle": (IPShuffle, True),
    "PortShuffle": (PortShuffle, False),
    "OSDiversity": (OSDiversity, True),
    "ServiceDiversity": (ServiceDiversity, True),
    "UserShuffle": (UserShuffle, False),
    "OSDiversityAssignment": (OSDiversityAssignment, False),
}


def one_run(mechanism, *, seed, interval, profile, horizon, mapping):
    kwargs = {}
    # The sink-retrace instrument exists only on the demonstration-arms branch
    # (where this tool was first measured). Pass it when the run supports it so
    # the numbers stay comparable there; on branches without it the run is the
    # plain movement arm, which times the defender identically.
    import inspect

    if "retrace_sinks" in inspect.signature(run_movement).parameters:
        kwargs["retrace_sinks"] = True
    return run_movement(
        profile,
        seed=seed,
        horizon=horizon,
        mapping_version=mapping,
        mtd_scheme=("single" if mechanism else None),
        custom_strategies=mechanism,
        mtd_interval=(interval if mechanism else None),
        **kwargs,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0])
    ap.add_argument("--interval", type=int, default=200)
    ap.add_argument("--horizon", type=int, default=15_000)
    ap.add_argument("--profile-arm", default="aggregate", dest="arm")
    ap.add_argument("--mapping", default="v2_partial")
    ap.add_argument(
        "--profile",
        default=None,
        metavar="MECHANISM",
        help="cProfile one run of this mechanism instead of timing the table",
    )
    ap.add_argument("--only", nargs="*", default=None, help="subset of mechanisms")
    args = ap.parse_args()

    if args.profile:
        cls, _ = MECHANISMS[args.profile]
        pr = cProfile.Profile()
        pr.enable()
        one_run(cls, seed=args.seeds[0], interval=args.interval,
                profile=args.arm, horizon=args.horizon, mapping=args.mapping)
        pr.disable()
        buf = io.StringIO()
        pstats.Stats(pr, stream=buf).sort_stats("cumulative").print_stats(20)
        print(buf.getvalue())
        return 0

    wanted = args.only or list(MECHANISMS)
    print(f"profile={args.arm} mapping={args.mapping} horizon={args.horizon} "
          f"interval={args.interval} seeds={args.seeds}")
    print(f"{'mechanism':26s} {'mean s':>9s} {'x no-MTD':>9s} "
          f"{'interrupts':>11s} {'events':>7s}  pool")

    baseline = None
    for name in ["(no MTD)"] + wanted:
        cls, in_pool = (None, None) if name == "(no MTD)" else MECHANISMS[name]
        elapsed, interrupts, events = 0.0, 0, 0
        for seed in args.seeds:
            start = time.perf_counter()
            result = one_run(cls, seed=seed, interval=args.interval,
                             profile=args.arm, horizon=args.horizon,
                             mapping=args.mapping)
            elapsed += time.perf_counter() - start
            interrupts += sum(1 for r in result.records if r.interrupted)
            events += len(result.records)
        mean = elapsed / len(args.seeds)
        if baseline is None:
            baseline = mean
        pool = "" if in_pool is None else ("default" if in_pool else "named-only")
        print(f"{name:26s} {mean:9.2f} {mean / baseline:9.1f} "
              f"{interrupts / len(args.seeds):11.0f} {events / len(args.seeds):7.0f}  {pool}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
