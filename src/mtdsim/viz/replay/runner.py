"""One-click simulation runner for the replay viewer.

Wraps the same `TimeNetwork + Adversary + AttackOperation + MTDOperation +
EventLogger` incantation that lives in the GAP-subgraph demo notebook, but
emits a *complete* ``sim_started`` event — including topology + per-host
metadata — so the replay viewer can render the Tay-canonical network without
needing the notebook to be present.

Keeps side effects to one file per run (``<events_dir>/<name>_<scheme>_<seed>.jsonl``).
No pandas / matplotlib imports: the viewer must boot on a fresh machine
that only has dash + plotly.
"""

from __future__ import annotations

import random
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Any, Optional

import numpy as np
import simpy

from mtdsim.attacker import Adversary, AttackOperation, AttackerProfile
from mtdsim.data import constants
from mtdsim.defender.mtd_operation import MTDOperation
from mtdsim.network.time_network import TimeNetwork
from mtdsim.stats.event_log import EventLogger
from mtdsim.stats.security_metric_statistics import SecurityMetricStatistics
from mtdsim.viz.replay.config import DEFAULT_EVENTS_DIR, ReplayConfig


# Single-slot worker so the UI can only ever have one sim running at a time.
# Dash callbacks need to poll via a dcc.Interval; the simplest thing that
# works is stash the in-flight Future at module scope.
_EXECUTOR = ThreadPoolExecutor(max_workers=1)
_CURRENT_FUTURE: Optional[Future] = None


def run_canonical_sim_async(
    config: ReplayConfig,
    *,
    scheme: str = "random",
    profile: Optional[AttackerProfile] = None,
    events_dir: Path = DEFAULT_EVENTS_DIR,
    force: bool = True,
) -> Future:
    """Kick off ``run_canonical_sim`` on a background thread.

    Defaults to ``force=True`` because the UI caller expects each Run click
    to produce a fresh log. The caller is responsible for tracking the
    returned Future (e.g. stashing it for a dcc.Interval poll loop).
    """
    global _CURRENT_FUTURE
    if _CURRENT_FUTURE is not None and not _CURRENT_FUTURE.done():
        return _CURRENT_FUTURE
    _CURRENT_FUTURE = _EXECUTOR.submit(
        run_canonical_sim,
        config,
        scheme=scheme,
        profile=profile,
        events_dir=events_dir,
        force=force,
    )
    return _CURRENT_FUTURE


def current_run_future() -> Optional[Future]:
    return _CURRENT_FUTURE


def _serialise_topology(net: TimeNetwork) -> dict[str, Any]:
    """Flatten ``net.graph`` + per-host metadata for the replay payload.

    Stored on ``sim_started.meta.topology`` as JSON-friendly dicts. Kept flat
    because the replay layout cache key hashes (nodes, edges) — nesting would
    make that hash unstable across reorderings.
    """
    nodes = []
    for nid in sorted(net.graph.nodes):
        attrs = net.graph.nodes[nid]
        host = net.get_host(nid) if hasattr(net, "get_host") else None
        node = {
            "id": int(nid),
            "subnet": int(attrs.get("subnet", -1)),
            "layer": int(attrs.get("layer", -1)),
            "is_endpoint": nid in net.exposed_endpoints,
            "is_database": nid in getattr(net, "_database", []),
        }
        if host is not None:
            node["os"] = getattr(host, "os_type", None)
            node["os_version"] = getattr(host, "os_version", None)
            node["ip"] = getattr(host, "ip", None)
            node["total_services"] = int(getattr(host, "total_services", 0))
            try:
                all_services = host.get_all_services()
                node["services"] = [
                    getattr(s, "name", str(s)) for s in all_services
                ][:20]
            except Exception:
                node["services"] = []
        nodes.append(node)

    edges = [[int(a), int(b)] for a, b in net.graph.edges]
    return {
        "nodes": nodes,
        "edges": edges,
        "exposed_endpoints": [int(n) for n in net.exposed_endpoints],
        "databases": [int(n) for n in getattr(net, "_database", [])],
        "layers": int(getattr(net, "layers", 0)),
        "subnets": int(getattr(net, "total_subnets", 0)),
    }


def run_canonical_sim(
    config: ReplayConfig,
    *,
    scheme: str = "random",
    profile: Optional[AttackerProfile] = None,
    events_dir: Path = DEFAULT_EVENTS_DIR,
    force: bool = False,
) -> Path:
    """Run a single sim with ``config`` + ``scheme``, write the event log, return its path.

    If the output already exists and ``force=False`` the function short-circuits
    — reruns are expensive and the replay viewer only needs the first one.
    """
    events_dir = Path(events_dir)
    events_dir.mkdir(parents=True, exist_ok=True)
    out_path = config.log_path(scheme, events_dir)
    if out_path.exists() and not force:
        return out_path

    random.seed(config.seed)
    np.random.seed(config.seed)

    env = simpy.Environment()
    end_event = env.event()
    net = TimeNetwork(**config.network_params)

    evlog = EventLogger(env)
    topology = _serialise_topology(net)
    sim_meta = {
        "config": config.name,
        "scheme": scheme,
        "seed": config.seed,
        "finish_time": config.finish_time,
        "network_params": dict(config.network_params),
        "topology": topology,
    }
    evlog.emit("sim_started", t=0.0, **sim_meta)

    profile = profile or AttackerProfile.default()
    adv = Adversary(net, constants.ATTACKER_THRESHOLD, profile)
    attack_op = AttackOperation(env, end_event, adv, event_logger=evlog)
    attack_op.proceed_attack()

    if scheme not in ("no_mtd", "None"):
        mtd = MTDOperation(
            SecurityMetricStatistics(),
            env,
            end_event,
            net,
            attack_op,
            scheme=scheme,
            adversary=adv,
            event_logger=evlog,
        )
        mtd.proceed_mtd()

    # Stop at whichever fires first: full compromise (end_event) or wall
    # finish_time. Without the AnyOf, a sim that hits the compromise
    # threshold early (~6 ks for PRIMARY) keeps spinning the trigger loop
    # for the remaining horizon and produces orphan deploys.
    sim_terminator = simpy.events.AnyOf(env, [end_event, env.timeout(config.finish_time)])
    env.run(until=sim_terminator)

    # Processes parked between mtd_deployed and their normal terminal event
    # are abandoned mid-stride when env.run returns — drain them so the
    # trace has a matching close for every deploy.
    if scheme not in ("no_mtd", "None"):
        mtd.drain_in_flight()

    evlog.emit(
        "sim_ended",
        t=float(env.now),
        compromise_ratio=len(adv.get_compromised_hosts()) / config.network_params["total_nodes"],
        compromised_hosts=list(adv.get_compromised_hosts()),
        duration=float(env.now),
        terminated_by=("end_event" if end_event.triggered else "finish_time"),
    )
    evlog.to_jsonl(str(out_path))
    return out_path
