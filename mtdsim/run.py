"""Command-line entry point for running a single MTDSim simulation.

Usage (from the repository root, with the environment active):

    python -m mtdsim.run                            # random scheme, defaults
    python -m mtdsim.run --scheme none              # attacker only, no MTD
    python -m mtdsim.run --scheme single --mtd IPShuffle
    python -m mtdsim.run --scheme alternative --mtd IPShuffle --mtd OSDiversity
    python -m mtdsim.run --finish-time 0            # run until the compromise threshold

Each run writes the attack and MTD event records (CSV), the topology and
event figures (PNG) and a ``summary.json`` under ``--out``
(default: ``output/<scheme>/``).
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
import warnings

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)

import numpy as np
import simpy

from mtdsim.component.adversary import Adversary
from mtdsim.component.time_network import TimeNetwork
from mtdsim.data.constants import ATTACKER_THRESHOLD, MTD_TRIGGER_INTERVAL
from mtdsim.mtd.completetopologyshuffle import CompleteTopologyShuffle
from mtdsim.mtd.hosttopologyshuffle import HostTopologyShuffle
from mtdsim.mtd.ipshuffle import IPShuffle
from mtdsim.mtd.osdiversity import OSDiversity
from mtdsim.mtd.osdiversityassignment import OSDiversityAssignment
from mtdsim.mtd.portshuffle import PortShuffle
from mtdsim.mtd.servicediversity import ServiceDiversity
from mtdsim.mtd.usershuffle import UserShuffle
from mtdsim.operation.attack_operation import AttackOperation
from mtdsim.operation.mtd_operation import MTDOperation
from mtdsim.statistic.evaluation import Evaluation
from mtdsim.statistic.security_metric_statistics import SecurityMetricStatistics

STRATEGIES = {
    cls.__name__: cls
    for cls in (
        CompleteTopologyShuffle,
        HostTopologyShuffle,
        IPShuffle,
        OSDiversity,
        OSDiversityAssignment,
        PortShuffle,
        ServiceDiversity,
        UserShuffle,
    )
}

SCHEMES = ("none", "single", "random", "alternative", "simultaneous")


def _seed_all(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def _versions() -> dict:
    import importlib

    out = {"python": sys.version.split()[0]}
    for pkg in ("numpy", "scipy", "networkx", "matplotlib", "pandas", "simpy"):
        try:
            out[pkg] = importlib.import_module(pkg).__version__
        except Exception as exc:  # noqa: BLE001
            out[pkg] = f"err:{exc!s}"
    return out


def _save_gantt(record, label_col: str, out_path: str, ylabel: str, height: float) -> None:
    """Horizontal event timeline (start_time + duration per event)."""
    if len(record) == 0:
        return
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, figsize=(16, 5))
    ax.barh(record[label_col].astype(str), record["duration"],
            left=record["start_time"], height=height)
    ax.set_xlabel("Simulation time")
    ax.set_ylabel(ylabel)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def _save_network_figure(network, out_path: str) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx

    fig = plt.figure(figsize=(15, 12))
    nx.draw(network.graph, pos=network.pos,
            node_color=network.colour_map, with_labels=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def run_simulation(
    scheme: str = "random",
    strategies: list[str] | None = None,
    mtd_interval: float | None = None,
    finish_time: int | None = 3000,
    seed: int = 1234,
    out_dir: str = "output",
    total_nodes: int = 50,
    total_endpoints: int = 5,
    total_subnets: int = 8,
    total_layers: int = 4,
    target_layer: int = 4,
    total_database: int = 2,
    terminate_compromise_ratio: float = 0.8,
    figures: bool = True,
) -> dict:
    """Run one simulation and write its artefacts to ``out_dir``.

    ``finish_time=None`` runs until the network reaches
    ``terminate_compromise_ratio``; otherwise the simulation stops at the
    given simulation time.
    """
    os.makedirs(out_dir, exist_ok=True)
    _seed_all(seed)

    env = simpy.Environment()
    end_event = env.event()
    security_metrics_record = SecurityMetricStatistics()

    time_network = TimeNetwork(
        total_nodes=total_nodes,
        total_endpoints=total_endpoints,
        total_subnets=total_subnets,
        total_layers=total_layers,
        target_layer=target_layer,
        total_database=total_database,
        terminate_compromise_ratio=terminate_compromise_ratio,
    )
    adversary = Adversary(network=time_network, attack_threshold=ATTACKER_THRESHOLD)

    if figures:
        _save_network_figure(time_network, os.path.join(out_dir, "network.png"))

    attack_operation = AttackOperation(env=env, end_event=end_event,
                                       adversary=adversary, proceed_time=0)
    attack_operation.proceed_attack()

    custom = None
    if strategies:
        classes = [STRATEGIES[name] for name in strategies]
        custom = classes[0] if scheme == "single" else classes

    # The published per-scheme intervals only cover the multi-MTD schemes;
    # fall back to the lineage's canonical experiment interval otherwise.
    if mtd_interval is None and scheme not in MTD_TRIGGER_INTERVAL:
        mtd_interval = 200

    if scheme != "none":
        mtd_operation = MTDOperation(
            security_metrics_record=security_metrics_record,
            env=env,
            end_event=end_event,
            network=time_network,
            scheme=scheme,
            attack_operation=attack_operation,
            proceed_time=0,
            mtd_trigger_interval=mtd_interval,
            custom_strategies=custom,
            adversary=adversary,
        )
        mtd_operation.proceed_mtd()

    t0 = time.time()
    if finish_time is not None:
        env.run(until=finish_time)
    else:
        env.run(until=end_event)
    wallclock = time.time() - t0

    evaluation = Evaluation(network=time_network, adversary=adversary,
                            security_metrics_record=security_metrics_record)

    attack_df = adversary.get_attack_stats().get_record()
    mtd_df = time_network.get_mtd_stats().get_record()
    attack_df.to_csv(os.path.join(out_dir, "attack_record.csv"), index=False)
    mtd_df.to_csv(os.path.join(out_dir, "mtd_record.csv"), index=False)

    if figures:
        _save_gantt(attack_df, "name", os.path.join(out_dir, "attack_record.png"),
                    "Attack action", height=0.1)
        _save_gantt(mtd_df, "name", os.path.join(out_dir, "mtd_record.png"),
                    "MTD strategy", height=0.4)

    checkpoint_results = evaluation.evaluation_result_by_compromise_checkpoint()

    compromised = adversary.get_compromised_hosts()
    summary = {
        "params": {
            "scheme": scheme,
            "strategies": strategies,
            "mtd_interval": mtd_interval,
            "finish_time": finish_time,
            "seed": seed,
            "total_nodes": total_nodes,
            "total_endpoints": total_endpoints,
            "total_subnets": total_subnets,
            "total_layers": total_layers,
            "target_layer": target_layer,
            "total_database": total_database,
            "terminate_compromise_ratio": terminate_compromise_ratio,
        },
        "results": {
            "simulated_time": env.now,
            "n_attack_events": int(len(attack_df)),
            "n_mtd_events": int(len(mtd_df)),
            "n_compromised_hosts": int(len(compromised)),
            "host_compromise_ratio": len(compromised) / total_nodes,
            "compromise_checkpoints": checkpoint_results,
            "wallclock_seconds": round(wallclock, 2),
        },
        "versions": _versions(),
    }
    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    return summary


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="python -m mtdsim.run",
        description="Run one MTDSim simulation: a simulated attacker "
                    "progresses through the network while the chosen MTD "
                    "scheme reshapes it.",
    )
    ap.add_argument("--scheme", choices=SCHEMES, default="random",
                    help="MTD deployment scheme (default: random). "
                         "'none' runs the attacker with no defence.")
    ap.add_argument("--mtd", action="append", choices=sorted(STRATEGIES),
                    metavar="STRATEGY", default=None,
                    help="MTD strategy to deploy; repeat the flag for several "
                         "(required for 'single', optional pool otherwise). "
                         f"Choices: {', '.join(sorted(STRATEGIES))}")
    ap.add_argument("--interval", type=float, default=None,
                    help="Mean time between MTD triggers (default: the "
                         "published per-scheme interval)")
    ap.add_argument("--finish-time", type=int, default=3000,
                    help="Simulation time to stop at (default 3000; 0 runs "
                         "until the compromise threshold is reached)")
    ap.add_argument("--seed", type=int, default=1234,
                    help="RNG seed; a given seed reproduces a run exactly")
    ap.add_argument("--out", default=None,
                    help="Output directory (default: output/<scheme>)")
    ap.add_argument("--nodes", type=int, default=50, help="Network size")
    ap.add_argument("--endpoints", type=int, default=5,
                    help="Number of exposed endpoint hosts")
    ap.add_argument("--subnets", type=int, default=8, help="Number of subnets")
    ap.add_argument("--layers", type=int, default=4, help="Number of network layers")
    ap.add_argument("--target-layer", type=int, default=4,
                    help="Layer of the target host (targetted scenarios)")
    ap.add_argument("--databases", type=int, default=2,
                    help="Number of database hosts")
    ap.add_argument("--terminate-ratio", type=float, default=0.8,
                    help="Host-compromise ratio that ends the simulation")
    ap.add_argument("--no-figures", action="store_true",
                    help="Skip writing PNG figures")
    args = ap.parse_args()

    if args.scheme == "single" and (not args.mtd or len(args.mtd) != 1):
        ap.error("--scheme single requires exactly one --mtd STRATEGY")
    if args.scheme == "none" and args.mtd:
        ap.error("--scheme none does not take --mtd")

    summary = run_simulation(
        scheme=args.scheme,
        strategies=args.mtd,
        mtd_interval=args.interval,
        finish_time=args.finish_time if args.finish_time > 0 else None,
        seed=args.seed,
        out_dir=args.out or os.path.join("output", args.scheme),
        total_nodes=args.nodes,
        total_endpoints=args.endpoints,
        total_subnets=args.subnets,
        total_layers=args.layers,
        target_layer=args.target_layer,
        total_database=args.databases,
        terminate_compromise_ratio=args.terminate_ratio,
        figures=not args.no_figures,
    )
    print(json.dumps(summary["results"], indent=2, default=str))


if __name__ == "__main__":
    main()
