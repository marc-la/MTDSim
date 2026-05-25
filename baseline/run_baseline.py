"""
Phase-0 baseline driver for MTDSim.

The original ``experiments/run.py`` entry point was deleted in commit
``e5935ab`` (along with ``mtdnetwork/run.py`` from upstream removal); this
script reproduces the minimum slice of that driver needed to execute one
end-to-end simulation per scenario, with explicit seeding.

It is intentionally tiny: it does *not* reimplement experiment scaffolding,
the threading harness, or any RL / MTD-AI hooks; restoring the deleted
``experiments/run.py`` would also pull in TensorFlow as a hard import.

Outputs (per scenario) are written under ``baseline/golden/<scenario>/``:
    summary.json         - parameters + headline numbers + library versions
    attack_record.csv    - per-attack-action record
    mtd_record.csv       - per-MTD-event record
    evaluation.json      - Evaluation.evaluation_result_by_compromise_checkpoint
    network_initial.png  - network topology figure
    attack_record.png    - attack action gantt
    mtd_record.png       - MTD action gantt (if any MTD events fired)
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

import mtdnetwork
from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.mtd.completetopologyshuffle import CompleteTopologyShuffle
from mtdnetwork.mtd.hosttopologyshuffle import HostTopologyShuffle
from mtdnetwork.mtd.ipshuffle import IPShuffle
from mtdnetwork.mtd.osdiversity import OSDiversity
from mtdnetwork.mtd.portshuffle import PortShuffle
from mtdnetwork.mtd.servicediversity import ServiceDiversity
from mtdnetwork.mtd.usershuffle import UserShuffle
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.operation.mtd_operation import MTDOperation
from mtdnetwork.statistic.evaluation import Evaluation
from mtdnetwork.statistic.security_metric_statistics import SecurityMetricStatistics


SCENARIOS = {
    "no-mtd": {
        "scheme": "None",
        "mtd_interval": None,
        "custom_strategies": None,
    },
    "single-ipshuffle": {
        "scheme": "single",
        "mtd_interval": 200,
        "custom_strategies": IPShuffle,
    },
    "single-osdiversity": {
        "scheme": "single",
        "mtd_interval": 200,
        "custom_strategies": OSDiversity,
    },
    "random-multi": {
        "scheme": "random",
        "mtd_interval": 200,
        "custom_strategies": None,
    },
    "alternative-multi": {
        "scheme": "alternative",
        "mtd_interval": 200,
        "custom_strategies": None,
    },
    "simultaneous-multi": {
        "scheme": "simultaneous",
        "mtd_interval": 700,
        "custom_strategies": None,
    },
}


def _seed_all(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def _versions() -> dict:
    import importlib
    pkgs = ["numpy", "scipy", "networkx", "matplotlib",
            "pandas", "simpy", "seaborn"]
    out = {"python": sys.version.split()[0]}
    for p in pkgs:
        try:
            out[p] = importlib.import_module(p).__version__
        except Exception as e:  # noqa: BLE001
            out[p] = f"err:{e!s}"
    return out


def _save_attack_figure(adversary, out_path: str) -> None:
    """Write a simplified attack-record gantt without using Evaluation.visualise_*
    (those call plt.show and have hard-coded path-join bugs)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    record = adversary.get_attack_stats().get_record()
    if len(record) == 0:
        return
    fig, ax = plt.subplots(1, figsize=(16, 5))
    ax.barh(record["name"], record["duration"],
            left=record["start_time"], height=0.1)
    ax.set_xlabel("Time")
    ax.set_ylabel("Attack action")
    plt.gca().invert_yaxis()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def _save_mtd_figure(network, out_path: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    record = network.get_mtd_stats().get_record()
    if len(record) == 0:
        return
    fig, ax = plt.subplots(1, figsize=(16, 5))
    ax.barh(record["name"].astype(str), record["duration"],
            left=record["start_time"], height=0.4)
    ax.set_xlabel("Time")
    ax.set_ylabel("MTD strategy")
    plt.gca().invert_yaxis()
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
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def run_scenario(
    scenario: str,
    seed: int,
    out_root: str,
    finish_time: int = 3000,
    total_nodes: int = 50,
    total_endpoints: int = 5,
    total_subnets: int = 8,
    total_layers: int = 4,
    target_layer: int = 4,
    total_database: int = 2,
    terminate_compromise_ratio: float = 0.8,
) -> dict:
    cfg = SCENARIOS[scenario]
    out_dir = os.path.join(out_root, scenario)
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

    _save_network_figure(time_network, os.path.join(out_dir, "network_initial.png"))

    attack_operation = AttackOperation(env=env, end_event=end_event,
                                       adversary=adversary, proceed_time=0)
    attack_operation.proceed_attack()

    if cfg["scheme"] != "None":
        mtd_operation = MTDOperation(
            security_metrics_record=security_metrics_record,
            env=env,
            end_event=end_event,
            network=time_network,
            scheme=cfg["scheme"],
            attack_operation=attack_operation,
            proceed_time=0,
            mtd_trigger_interval=cfg["mtd_interval"],
            custom_strategies=cfg["custom_strategies"],
            adversary=adversary,
        )
        mtd_operation.proceed_mtd()

    t0 = time.time()
    env.run(until=finish_time)
    sim_wallclock = time.time() - t0

    evaluation = Evaluation(network=time_network, adversary=adversary,
                            security_metrics_record=security_metrics_record)

    attack_df = adversary.get_attack_stats().get_record()
    mtd_df = time_network.get_mtd_stats().get_record()
    attack_df.to_csv(os.path.join(out_dir, "attack_record.csv"), index=False)
    mtd_df.to_csv(os.path.join(out_dir, "mtd_record.csv"), index=False)

    _save_attack_figure(adversary, os.path.join(out_dir, "attack_record.png"))
    _save_mtd_figure(time_network, os.path.join(out_dir, "mtd_record.png"))

    eval_result = evaluation.evaluation_result_by_compromise_checkpoint(
        [0.05, 0.1, 0.15, 0.2, 0.25])
    with open(os.path.join(out_dir, "evaluation.json"), "w") as f:
        json.dump(eval_result, f, indent=2, default=str)

    compromised = adversary.get_compromised_hosts()
    summary = {
        "scenario": scenario,
        "seed": seed,
        "finish_time": finish_time,
        "params": {
            "total_nodes": total_nodes,
            "total_endpoints": total_endpoints,
            "total_subnets": total_subnets,
            "total_layers": total_layers,
            "target_layer": target_layer,
            "total_database": total_database,
            "terminate_compromise_ratio": terminate_compromise_ratio,
            "scheme": cfg["scheme"],
            "mtd_interval": cfg["mtd_interval"],
            "custom_strategies": (
                cfg["custom_strategies"].__name__
                if isinstance(cfg["custom_strategies"], type) else None),
        },
        "results": {
            "n_attack_events": int(len(attack_df)),
            "n_mtd_events": int(len(mtd_df)),
            "n_compromised_hosts": int(len(compromised)),
            "host_compromise_ratio": len(compromised) / total_nodes,
            "sim_wallclock_seconds": sim_wallclock,
            "mtttc_eval_checkpoints": eval_result,
        },
        "versions": _versions(),
        "git": {
            "branch": _git("rev-parse --abbrev-ref HEAD"),
            "head": _git("rev-parse HEAD"),
            "dirty": _git("status --porcelain") != "",
        },
    }
    with open(os.path.join(out_dir, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    return summary


def _git(args: str) -> str:
    import subprocess
    try:
        out = subprocess.check_output(
            ["git"] + args.split(),
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except Exception:  # noqa: BLE001
        return ""


def main() -> None:
    ap = argparse.ArgumentParser(description="MTDSim Phase-0 baseline driver")
    ap.add_argument("--scenario", required=True, choices=list(SCENARIOS),
                    help="Which preset scenario to run")
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--finish-time", type=int, default=3000)
    ap.add_argument("--out-root", default="baseline/golden")
    args = ap.parse_args()

    summary = run_scenario(args.scenario, args.seed, args.out_root,
                           finish_time=args.finish_time)
    print(json.dumps(summary["results"], indent=2, default=str))


if __name__ == "__main__":
    main()
