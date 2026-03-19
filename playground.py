#!/usr/bin/env python3
"""Lightweight playground for exploring MTDSim core behavior.

Usage examples:
  python playground.py network --nodes 30
  python playground.py attack --nodes 50 --finish-time 1200
  python playground.py mtd --mtd IPShuffle --nodes 50 --finish-time 1200
  python playground.py compare --nodes 50 --finish-time 1200
"""

from __future__ import annotations

import argparse
import ast
import os
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.mtd.completetopologyshuffle import CompleteTopologyShuffle
from mtdnetwork.mtd.hosttopologyshuffle import HostTopologyShuffle
from mtdnetwork.mtd.ipshuffle import IPShuffle
from mtdnetwork.mtd.osdiversity import OSDiversity
from mtdnetwork.mtd.osdiversityassignment import OSDiversityAssignment
from mtdnetwork.mtd.portshuffle import PortShuffle
from mtdnetwork.mtd.servicediversity import ServiceDiversity
from mtdnetwork.mtd.usershuffle import UserShuffle


OUTPUT_DIR = Path("output") / "playground"

MTD_MAP = {
    "CompleteTopologyShuffle": CompleteTopologyShuffle,
    "IPShuffle": IPShuffle,
    "OSDiversity": OSDiversity,
    "ServiceDiversity": ServiceDiversity,
}

INSPECT_MTD_MAP = {
    "CompleteTopologyShuffle": CompleteTopologyShuffle,
    "HostTopologyShuffle": HostTopologyShuffle,
    "IPShuffle": IPShuffle,
    "OSDiversity": OSDiversity,
    "OSDiversityAssignment": OSDiversityAssignment,
    "PortShuffle": PortShuffle,
    "ServiceDiversity": ServiceDiversity,
    "UserShuffle": UserShuffle,
}


@dataclass
class RunSummary:
    label: str
    total_nodes: int
    compromised_hosts: int
    compromise_ratio: float
    attack_events: int
    mtd_events: int
    interrupted_events: int


def _capture_network_state(network: TimeNetwork) -> dict:
    hosts = network.get_hosts()
    host_state = {}
    for node_id, host in hosts.items():
        service_sig = []
        for svc_node, node_data in host.graph.nodes(data=True):
            if svc_node == host.target_node:
                continue
            service = node_data.get("service")
            if service is None:
                continue
            service_sig.append((service.name, int(service.version)))

        host_state[node_id] = {
            "host_uuid": host.uuid,
            "host_id_field": host.host_id,
            "ip": host.ip,
            "os_type": host.os_type,
            "os_version": host.os_version,
            "ports": tuple(sorted(host.get_ports())),
            "users": tuple(sorted(host.get_users())),
            "services": tuple(sorted(service_sig)),
        }
    return {
        "edges": set(tuple(sorted(e)) for e in network.graph.edges()),
        "host_state": host_state,
    }


def _diff_network_state(before: dict, after: dict) -> dict:
    before_hosts = before["host_state"]
    after_hosts = after["host_state"]
    nodes = sorted(before_hosts.keys())

    changed_host_binding = 0
    changed_ip = 0
    changed_os = 0
    changed_ports = 0
    changed_users = 0
    changed_services = 0
    changed_any = 0

    for n in nodes:
        b = before_hosts[n]
        a = after_hosts[n]
        node_changed = False

        if b["host_uuid"] != a["host_uuid"] or b["host_id_field"] != a["host_id_field"]:
            changed_host_binding += 1
            node_changed = True
        if b["ip"] != a["ip"]:
            changed_ip += 1
            node_changed = True
        if b["os_type"] != a["os_type"] or b["os_version"] != a["os_version"]:
            changed_os += 1
            node_changed = True
        if b["ports"] != a["ports"]:
            changed_ports += 1
            node_changed = True
        if b["users"] != a["users"]:
            changed_users += 1
            node_changed = True
        if b["services"] != a["services"]:
            changed_services += 1
            node_changed = True

        if node_changed:
            changed_any += 1

    before_edges = before["edges"]
    after_edges = after["edges"]
    removed_edges = len(before_edges - after_edges)
    added_edges = len(after_edges - before_edges)

    return {
        "changed_nodes_any": changed_any,
        "changed_host_binding": changed_host_binding,
        "changed_ip": changed_ip,
        "changed_os": changed_os,
        "changed_ports": changed_ports,
        "changed_users": changed_users,
        "changed_services": changed_services,
        "edges_added": added_edges,
        "edges_removed": removed_edges,
    }


def _label_for_inspect(host, node: int, layer: int, mtd_name: str) -> str:
    if mtd_name == "HostTopologyShuffle":
        return f"H{node} L{layer}\\nuuid={host.uuid[:8]}"
    if mtd_name == "IPShuffle":
        return f"H{node} L{layer}\\n{host.ip}"
    if mtd_name in ("OSDiversity", "OSDiversityAssignment"):
        return f"H{node} L{layer}\\n{host.os_type}:{host.os_version}"
    if mtd_name == "PortShuffle":
        ports = sorted(host.get_ports())
        preview = ",".join(str(p) for p in ports[:3])
        return f"H{node} L{layer}\\nports={preview}"
    if mtd_name == "UserShuffle":
        users = sorted(host.get_users())
        preview = ",".join(users[:2]) if users else "none"
        return f"H{node} L{layer}\\nusers={preview}"
    if mtd_name == "ServiceDiversity":
        services = []
        for svc_node, node_data in host.graph.nodes(data=True):
            if svc_node == host.target_node:
                continue
            service = node_data.get("service")
            if service is None:
                continue
            services.append(f"{service.name}:{service.version}")
        preview = ",".join(sorted(services)[:2]) if services else "none"
        return f"H{node} L{layer}\\nsvc={preview}"
    return f"H{node} L{layer}\\n{host.ip}"


def _save_labeled_network(
    network: TimeNetwork,
    output_path: Path,
    title: str,
    max_labels: int = 120,
    mtd_name: str = "",
) -> None:
    layer_map = network.get_layers()
    endpoint_set = set(network.get_exposed_endpoints())

    node_colors = []
    labels = {}
    for idx, node in enumerate(network.graph.nodes):
        layer = layer_map.get(node, -1)
        host = network.get_host(node)
        if node in endpoint_set:
            node_colors.append("green")
        else:
            node_colors.append("lightgray")
        if idx < max_labels and host is not None:
            labels[node] = _label_for_inspect(host, node, layer, mtd_name)

    plt.figure(figsize=(14, 10))
    nx.draw(
        network.graph,
        pos=network.pos,
        with_labels=True,
        labels=labels,
        node_color=node_colors,
        node_size=450,
        font_size=7,
    )
    plt.title(title)
    plt.savefig(output_path)
    plt.close()


def _try_build_gif(frame_paths: list[Path], gif_path: Path) -> bool:
    try:
        from PIL import Image
    except Exception:
        return False

    images = []
    for frame in frame_paths:
        if frame.exists():
            images.append(Image.open(frame))
    if not images:
        return False

    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        duration=900,
        loop=0,
    )
    for img in images:
        img.close()
    return True


def _ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _save_network_plot(network: TimeNetwork, output_path: Path) -> None:
    plt.figure(figsize=(12, 8))
    nx.draw(network.graph, pos=network.pos, node_color=network.colour_map, with_labels=True, node_size=250)
    plt.title("Generated Network Topology")
    plt.savefig(output_path)
    plt.close()


def _execute_simulation_lazy(**kwargs):
    # Delay importing experiments.run so lightweight commands avoid TensorFlow startup overhead.
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    from experiments.run import execute_simulation

    return execute_simulation(**kwargs)


def _save_attack_timeline(attack_record: pd.DataFrame, output_path: Path) -> None:
    if attack_record.empty:
        return

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.barh(attack_record["name"], attack_record["duration"], left=attack_record["start_time"], height=0.2)
    ax.set_xlabel("Time")
    ax.set_ylabel("Attack Action")
    ax.set_title("Attack Timeline")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def _save_mtd_timeline(mtd_record: pd.DataFrame, output_path: Path) -> None:
    if mtd_record.empty:
        return

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(mtd_record["name"], mtd_record["duration"], left=mtd_record["start_time"], height=0.35)
    ax.set_xlabel("Time")
    ax.set_ylabel("MTD")
    ax.set_title("MTD Timeline")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def _parse_users(cell) -> list[str]:
    if isinstance(cell, list):
        return [str(x) for x in cell]
    if isinstance(cell, str):
        text = cell.strip()
        if not text:
            return []
        try:
            value = ast.literal_eval(text)
            if isinstance(value, list):
                return [str(x) for x in value]
        except (ValueError, SyntaxError):
            return []
    return []


def _save_host_compromise_network(network: TimeNetwork, attack_record: pd.DataFrame, output_path: Path) -> None:
    if network is None:
        return

    compromised = {}
    if not attack_record.empty and "compromise_host" in attack_record.columns:
        comp_rows = attack_record[attack_record["compromise_host"] != "None"]
        for _, row in comp_rows.iterrows():
            try:
                host_id = int(row["compromise_host"])
            except (TypeError, ValueError):
                continue
            compromised[host_id] = min(compromised.get(host_id, float("inf")), float(row["finish_time"]))

    layer_map = network.get_layers()
    endpoint_set = set(network.get_exposed_endpoints())

    node_colors = []
    labels = {}
    for node in network.graph.nodes:
        layer = layer_map.get(node, -1)
        if node in compromised:
            node_colors.append("red")
            labels[node] = f"H{node} L{layer}\nC@{compromised[node]:.0f}s"
        elif node in endpoint_set:
            node_colors.append("green")
            labels[node] = f"H{node} L{layer}\nendpoint"
        else:
            node_colors.append("lightgray")
            labels[node] = f"H{node} L{layer}"

    plt.figure(figsize=(14, 10))
    nx.draw(
        network.graph,
        pos=network.pos,
        with_labels=True,
        labels=labels,
        node_color=node_colors,
        node_size=500,
        font_size=7,
    )
    plt.title("Host Compromise Map (red=compromised, green=exposed endpoint)")
    plt.savefig(output_path)
    plt.close()


def _save_host_compromise_progress(attack_record: pd.DataFrame, output_path: Path) -> None:
    if attack_record.empty or "cumulative_compromised_hosts" not in attack_record.columns:
        return

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(attack_record["finish_time"], attack_record["cumulative_compromised_hosts"], color="tab:red")
    ax.set_xlabel("Time")
    ax.set_ylabel("Cumulative Compromised Hosts")
    ax.set_title("Host Compromise Progress")
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def _save_compromised_users_chart(attack_record: pd.DataFrame, output_path: Path) -> None:
    if attack_record.empty or "compromise_users" not in attack_record.columns:
        return

    users = []
    for cell in attack_record["compromise_users"]:
        users.extend(_parse_users(cell))

    if not users:
        return

    counts = Counter(users)
    top_items = counts.most_common(20)
    labels = [name for name, _ in top_items]
    values = [count for _, count in top_items]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(labels, values, color="tab:blue")
    ax.set_xlabel("Compromised Username")
    ax.set_ylabel("Count")
    ax.set_title("Top Compromised Users")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def _summarize(label: str, evaluation) -> RunSummary:
    attack_record = evaluation._attack_record
    mtd_record = evaluation._mtd_record

    total_nodes = evaluation.get_network().get_total_nodes()
    compromised_hosts = int(attack_record["cumulative_compromised_hosts"].max()) if not attack_record.empty else 0
    compromise_ratio = compromised_hosts / total_nodes if total_nodes else 0.0

    interrupted_events = 0
    if not attack_record.empty and "interrupted_in" in attack_record.columns:
        interrupted_events = int((attack_record["interrupted_in"] != "None").sum())

    return RunSummary(
        label=label,
        total_nodes=total_nodes,
        compromised_hosts=compromised_hosts,
        compromise_ratio=compromise_ratio,
        attack_events=len(attack_record),
        mtd_events=len(mtd_record),
        interrupted_events=interrupted_events,
    )


def _print_summary(summary: RunSummary) -> None:
    print(f"\n=== {summary.label} ===")
    print(f"Total nodes: {summary.total_nodes}")
    print(f"Compromised hosts: {summary.compromised_hosts} ({summary.compromise_ratio:.2%})")
    print(f"Attack events: {summary.attack_events}")
    print(f"MTD events: {summary.mtd_events}")
    print(f"Interrupted attack events: {summary.interrupted_events}")


def _run_single(
    label: str,
    scheme: str,
    total_nodes: int,
    finish_time: int,
    mtd_interval: int,
    mtd_cls=None,
):
    evaluation = _execute_simulation_lazy(
        start_time=0,
        finish_time=finish_time,
        scheme=scheme,
        mtd_interval=mtd_interval,
        custom_strategies=mtd_cls,
        total_nodes=total_nodes,
        new_network=True,
    )

    attack_record = evaluation._attack_record
    mtd_record = evaluation._mtd_record

    attack_csv = OUTPUT_DIR / f"{label}_attack.csv"
    mtd_csv = OUTPUT_DIR / f"{label}_mtd.csv"
    attack_record.to_csv(attack_csv, index=False)
    mtd_record.to_csv(mtd_csv, index=False)

    _save_attack_timeline(attack_record, OUTPUT_DIR / f"{label}_attack_timeline.png")
    _save_mtd_timeline(mtd_record, OUTPUT_DIR / f"{label}_mtd_timeline.png")
    _save_host_compromise_progress(attack_record, OUTPUT_DIR / f"{label}_host_compromise_progress.png")
    _save_host_compromise_network(evaluation.get_network(), attack_record, OUTPUT_DIR / f"{label}_host_compromise_map.png")
    _save_compromised_users_chart(attack_record, OUTPUT_DIR / f"{label}_compromised_users.png")

    try:
        checkpoints = evaluation.evaluation_result_by_compromise_checkpoint([0.05, 0.1, 0.15, 0.2, 0.25])
        pd.DataFrame(checkpoints).to_csv(OUTPUT_DIR / f"{label}_checkpoints.csv", index=False)
    except Exception as exc:
        print(f"Checkpoint export skipped for {label}: {exc}")

    summary = _summarize(label, evaluation)
    _print_summary(summary)
    return summary


def cmd_network(args: argparse.Namespace) -> None:
    _ensure_dirs()
    net = TimeNetwork(total_nodes=args.nodes)
    output = OUTPUT_DIR / f"network_{args.nodes}n.png"
    _save_network_plot(net, output)
    print(f"Saved network plot: {output}")


def cmd_attack(args: argparse.Namespace) -> None:
    _ensure_dirs()
    _run_single(
        label="attack_only",
        scheme="None",
        total_nodes=args.nodes,
        finish_time=args.finish_time,
        mtd_interval=args.mtd_interval,
        mtd_cls=None,
    )


def cmd_mtd(args: argparse.Namespace) -> None:
    _ensure_dirs()
    mtd_cls = MTD_MAP[args.mtd]
    try:
        _run_single(
            label=f"single_{args.mtd}",
            scheme="single",
            total_nodes=args.nodes,
            finish_time=args.finish_time,
            mtd_interval=args.mtd_interval,
            mtd_cls=mtd_cls,
        )
    except Exception as exc:
        print(f"Run failed for {args.mtd}: {exc}")


def cmd_compare(args: argparse.Namespace) -> None:
    _ensure_dirs()
    rows = []

    baseline = _run_single(
        label="compare_nomtd",
        scheme="None",
        total_nodes=args.nodes,
        finish_time=args.finish_time,
        mtd_interval=args.mtd_interval,
        mtd_cls=None,
    )
    rows.append(baseline.__dict__)

    for mtd_name, mtd_cls in MTD_MAP.items():
        try:
            summary = _run_single(
                label=f"compare_{mtd_name}",
                scheme="single",
                total_nodes=args.nodes,
                finish_time=args.finish_time,
                mtd_interval=args.mtd_interval,
                mtd_cls=mtd_cls,
            )
            rows.append(summary.__dict__)
        except Exception as exc:
            print(f"Skipping {mtd_name} due to error: {exc}")

    out_csv = OUTPUT_DIR / "compare_summary.csv"
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print(f"Saved comparison summary: {out_csv}")


def cmd_inspect_mtd(args: argparse.Namespace) -> None:
    _ensure_dirs()
    target_mtds = [args.mtd] if args.mtd != "ALL" else list(INSPECT_MTD_MAP.keys())

    for mtd_name in target_mtds:
        mtd_cls = INSPECT_MTD_MAP[mtd_name]
        mtd_dir = OUTPUT_DIR / "inspect_mtd" / mtd_name
        mtd_dir.mkdir(parents=True, exist_ok=True)

        print(f"\nInspecting {mtd_name} on {args.nodes} nodes for {args.steps} step(s)...")

        net = TimeNetwork(total_nodes=args.nodes)
        adversary = Adversary(network=net, attack_threshold=ATTACKER_THRESHOLD)
        mtd = mtd_cls(network=net)

        summary_rows = []
        frame_paths = []

        before = _capture_network_state(net)
        first_frame = mtd_dir / "step_00_before.png"
        _save_labeled_network(net, first_frame, f"{mtd_name} - Before any action", mtd_name=mtd_name)
        frame_paths.append(first_frame)

        for step in range(1, args.steps + 1):
            try:
                mtd.mtd_operation(adversary=adversary)
            except Exception as exc:
                print(f"{mtd_name} failed at step {step}: {exc}")
                summary_rows.append({"step": step, "error": str(exc)})
                break

            after = _capture_network_state(net)
            diff = _diff_network_state(before, after)
            diff["step"] = step
            summary_rows.append(diff)

            frame = mtd_dir / f"step_{step:02d}_after.png"
            _save_labeled_network(net, frame, f"{mtd_name} - After step {step}", mtd_name=mtd_name)
            frame_paths.append(frame)

            before = after

        summary_csv = mtd_dir / "summary.csv"
        pd.DataFrame(summary_rows).to_csv(summary_csv, index=False)
        print(f"Saved summary: {summary_csv}")

        if args.make_gif:
            gif_path = mtd_dir / "animation.gif"
            ok = _try_build_gif(frame_paths, gif_path)
            if ok:
                print(f"Saved animation: {gif_path}")
            else:
                print("GIF skipped: Pillow not available in this environment.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Playground for exploring MTDSim behavior")
    sub = parser.add_subparsers(dest="command", required=True)

    p_net = sub.add_parser("network", help="Generate and save a random network plot")
    p_net.add_argument("--nodes", type=int, default=30)
    p_net.set_defaults(func=cmd_network)

    p_attack = sub.add_parser("attack", help="Run attack-only simulation (no MTD)")
    p_attack.add_argument("--nodes", type=int, default=50)
    p_attack.add_argument("--finish-time", type=int, default=1200)
    p_attack.add_argument("--mtd-interval", type=int, default=200)
    p_attack.set_defaults(func=cmd_attack)

    p_mtd = sub.add_parser("mtd", help="Run one MTD strategy in single scheme")
    p_mtd.add_argument("--mtd", choices=sorted(MTD_MAP.keys()), default="IPShuffle")
    p_mtd.add_argument("--nodes", type=int, default=50)
    p_mtd.add_argument("--finish-time", type=int, default=1200)
    p_mtd.add_argument("--mtd-interval", type=int, default=200)
    p_mtd.set_defaults(func=cmd_mtd)

    p_cmp = sub.add_parser("compare", help="Compare no-MTD vs each available default MTD")
    p_cmp.add_argument("--nodes", type=int, default=50)
    p_cmp.add_argument("--finish-time", type=int, default=1200)
    p_cmp.add_argument("--mtd-interval", type=int, default=200)
    p_cmp.set_defaults(func=cmd_compare)

    p_ins = sub.add_parser("inspect-mtd", help="Apply MTD directly and export before/after visual diff artifacts")
    p_ins.add_argument("--mtd", choices=["ALL"] + sorted(INSPECT_MTD_MAP.keys()), default="ALL")
    p_ins.add_argument("--nodes", type=int, default=50)
    p_ins.add_argument("--steps", type=int, default=3)
    p_ins.add_argument("--make-gif", action="store_true")
    p_ins.set_defaults(func=cmd_inspect_mtd)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
