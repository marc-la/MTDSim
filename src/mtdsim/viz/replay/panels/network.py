"""Network state panel (SA L1: Perception).

Plotly scattergl figure: one edge trace + one trace per host-state class
(untouched / targeted / compromised). MTD halo overlay is stubbed for now
and filled in with a live mtd_deployed → mtd_completed pass in step 9.

The panel is driven by two inputs:

- ``topology`` — nodes + edges read from ``sim_started.meta.topology``.
- ``event_index`` from the playback state; the panel derives the cumulative
  host-state set from the event log up to and including that index.

Layout comes from the on-disk cache (see ``layout.py``).
"""

from __future__ import annotations

from typing import Any, Iterable

import plotly.graph_objects as go

from mtdsim.viz.replay.layout import DEFAULT_SEED, compute_layout


STATE_COLORS = {
    "untouched": "#adb5bd",
    "targeted": "#f7b267",
    "compromised": "#e63946",
}
EDGE_COLOR = "#343a40"
MTD_HALO_COLOR = "#06a77d"
ENDPOINT_RING_COLOR = "#2d6a4f"
DATABASE_RING_COLOR = "#7209b7"


def _cumulative_host_states(
    events: list[dict[str, Any]],
    event_index: int,
) -> dict[int, str]:
    compromised: set[int] = set()
    targeted: set[int] = set()
    end = min(event_index + 1, len(events))
    for ev in events[:end]:
        host_id = ev["host_id"]
        if host_id is None or host_id < 0:
            continue
        if ev["type"] == "host_compromised":
            compromised.add(host_id)
        elif ev["type"] == "phase_started":
            targeted.add(host_id)
    states: dict[int, str] = {}
    for h in targeted | compromised:
        states[h] = "compromised" if h in compromised else "targeted"
    return states


def _node_degree_size(nodes: list[int], edges: list[tuple[int, int]]) -> dict[int, int]:
    deg: dict[int, int] = {n: 0 for n in nodes}
    for a, b in edges:
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    return deg


def _host_hover_text(
    host_id: int,
    state: str,
    topology_node: dict[str, Any] | None,
    compromise_time: float | None,
    attack_count: int = 0,
    last_technique: str | None = None,
) -> str:
    parts = [f"<b>host {host_id}</b>", f"state: {state}"]
    if topology_node:
        if "subnet" in topology_node:
            parts.append(f"subnet: {topology_node['subnet']}")
        if "layer" in topology_node:
            parts.append(f"layer: {topology_node['layer']}")
        if topology_node.get("is_endpoint"):
            parts.append("role: exposed endpoint")
        if topology_node.get("is_database"):
            parts.append("role: database")
        if "os" in topology_node and topology_node["os"]:
            os_str = topology_node["os"]
            if topology_node.get("os_version"):
                os_str = f"{os_str} {topology_node['os_version']}"
            parts.append(f"os: {os_str}")
        if "ip" in topology_node and topology_node["ip"]:
            parts.append(f"ip: {topology_node['ip']}")
        if "total_services" in topology_node:
            parts.append(f"services: {topology_node['total_services']}")
    if attack_count:
        parts.append(f"phases seen: {attack_count}")
    if last_technique:
        parts.append(f"last technique: {last_technique}")
    if compromise_time is not None:
        parts.append(f"compromised @ t={compromise_time:.1f}s")
    return "<br>".join(parts)


def _per_host_activity(
    events: list[dict[str, Any]], event_index: int
) -> dict[int, dict[str, Any]]:
    end = min(event_index + 1, len(events))
    info: dict[int, dict[str, Any]] = {}
    for ev in events[:end]:
        host_id = ev.get("host_id")
        if host_id is None or host_id < 0:
            continue
        d = info.setdefault(host_id, {"phases": 0, "last_technique": None})
        if ev["type"] == "phase_started":
            d["phases"] += 1
            if ev.get("technique_id"):
                d["last_technique"] = ev["technique_id"]
    return info


def _mtd_targets_at(
    events: list[dict[str, Any]],
    event_index: int,
    topology_nodes: list[dict[str, Any]],
) -> set[int]:
    """Hosts currently covered by an active MTD halo.

    Network-layer MTDs affect *every* host (topology / IP / port shuffle);
    application-layer MTDs cover every host with services (everything except
    exposed endpoints in most configs). We approximate: halo all hosts while
    any network MTD is active; halo non-endpoint hosts while app MTDs are
    active. Meta payloads currently don't carry per-host targets, so this is
    the tightest SA signal we can derive from schema v1.0.
    """
    active_network = False
    active_application = False
    open_counts: dict[str, int] = {"network": 0, "application": 0}
    end = min(event_index + 1, len(events))
    for ev in events[:end]:
        if ev["type"] == "mtd_deployed":
            rt = (ev.get("meta") or {}).get("resource_type") or "other"
            open_counts[rt] = open_counts.get(rt, 0) + 1
        elif ev["type"] == "mtd_completed":
            rt = (ev.get("meta") or {}).get("resource_type") or "other"
            open_counts[rt] = max(0, open_counts.get(rt, 0) - 1)
    active_network = open_counts.get("network", 0) > 0
    active_application = open_counts.get("application", 0) > 0

    if not (active_network or active_application):
        return set()
    targets: set[int] = set()
    for node in topology_nodes:
        nid = int(node["id"])
        if active_network:
            targets.add(nid)
        elif active_application and not node.get("is_endpoint"):
            targets.add(nid)
    return targets


def empty_figure(message: str = "No topology in sim_started.meta.topology") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[dict(text=message, showarrow=False, font=dict(color="#6c757d"))],
        height=360,
    )
    return fig


def build_network_figure(
    *,
    topology: dict[str, Any] | None,
    events: list[dict[str, Any]],
    event_index: int,
    layout_seed: int = DEFAULT_SEED,
    height: int = 720,
) -> go.Figure:
    if not topology or not topology.get("nodes"):
        return empty_figure()

    raw_nodes = topology["nodes"]
    raw_edges = topology.get("edges") or []
    node_ids = [int(n["id"]) for n in raw_nodes]
    edges = [(int(a), int(b)) for a, b in raw_edges]

    pos = compute_layout(node_ids, edges, seed=layout_seed)
    degree = _node_degree_size(node_ids, edges)
    node_meta = {int(n["id"]): n for n in raw_nodes}

    states_now = _cumulative_host_states(events, event_index)
    activity = _per_host_activity(events, event_index)
    mtd_targets = _mtd_targets_at(events, event_index, raw_nodes)

    compromise_ts: dict[int, float] = {}
    end = min(event_index + 1, len(events))
    for ev in events[:end]:
        if ev["type"] == "host_compromised" and ev["host_id"] is not None:
            compromise_ts.setdefault(int(ev["host_id"]), float(ev["t"]))

    edge_x: list[float] = []
    edge_y: list[float] = []
    for a, b in edges:
        if a not in pos or b not in pos:
            continue
        edge_x += [pos[a][0], pos[b][0], None]
        edge_y += [pos[a][1], pos[b][1], None]

    edge_trace = go.Scattergl(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(color=EDGE_COLOR, width=1),
        opacity=0.30,
        hoverinfo="skip",
        showlegend=False,
    )

    traces_by_state: dict[str, dict[str, list]] = {
        name: {"x": [], "y": [], "size": [], "text": [], "ids": []}
        for name in STATE_COLORS
    }

    halo_x: list[float] = []
    halo_y: list[float] = []
    halo_size: list[float] = []

    for nid in node_ids:
        if nid not in pos:
            continue
        state = states_now.get(nid, "untouched")
        bucket = traces_by_state[state]
        bucket["x"].append(pos[nid][0])
        bucket["y"].append(pos[nid][1])
        base_size = 10 + 2.5 * degree.get(nid, 0)
        bucket["size"].append(base_size)
        host_activity = activity.get(nid, {})
        bucket["text"].append(
            _host_hover_text(
                host_id=nid,
                state=state,
                topology_node=node_meta.get(nid),
                compromise_time=compromise_ts.get(nid),
                attack_count=host_activity.get("phases", 0),
                last_technique=host_activity.get("last_technique"),
            )
        )
        bucket["ids"].append(str(nid))

        if nid in mtd_targets:
            halo_x.append(pos[nid][0])
            halo_y.append(pos[nid][1])
            halo_size.append(base_size + 12)

    fig = go.Figure()
    fig.add_trace(edge_trace)

    if halo_x:
        fig.add_trace(
            go.Scattergl(
                x=halo_x,
                y=halo_y,
                mode="markers",
                marker=dict(
                    color="rgba(6, 167, 125, 0.25)",
                    size=halo_size,
                    line=dict(color=MTD_HALO_COLOR, width=2),
                ),
                name="MTD active",
                hoverinfo="skip",
            )
        )

    endpoint_ring_x = []
    endpoint_ring_y = []
    database_ring_x = []
    database_ring_y = []
    for n in raw_nodes:
        nid = int(n["id"])
        if nid not in pos:
            continue
        if n.get("is_endpoint"):
            endpoint_ring_x.append(pos[nid][0])
            endpoint_ring_y.append(pos[nid][1])
        if n.get("is_database"):
            database_ring_x.append(pos[nid][0])
            database_ring_y.append(pos[nid][1])
    if endpoint_ring_x:
        fig.add_trace(
            go.Scattergl(
                x=endpoint_ring_x,
                y=endpoint_ring_y,
                mode="markers",
                marker=dict(
                    color="rgba(0,0,0,0)",
                    size=22,
                    line=dict(color=ENDPOINT_RING_COLOR, width=2),
                ),
                name="exposed endpoint",
                hoverinfo="skip",
            )
        )
    if database_ring_x:
        fig.add_trace(
            go.Scattergl(
                x=database_ring_x,
                y=database_ring_y,
                mode="markers",
                marker=dict(
                    color="rgba(0,0,0,0)",
                    size=22,
                    line=dict(color=DATABASE_RING_COLOR, width=2),
                ),
                name="database",
                hoverinfo="skip",
            )
        )

    for name, color in STATE_COLORS.items():
        bucket = traces_by_state[name]
        fig.add_trace(
            go.Scattergl(
                x=bucket["x"],
                y=bucket["y"],
                mode="markers",
                name=name,
                marker=dict(
                    color=color,
                    size=bucket["size"],
                    line=dict(color="#212529", width=1),
                ),
                text=bucket["text"],
                ids=bucket["ids"],
                hovertemplate="%{text}<extra></extra>",
            )
        )

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0),
        height=height,
        uirevision="network-panel",
    )
    return fig


def host_detail_lines(
    *,
    topology: dict[str, Any] | None,
    events: list[dict[str, Any]],
    host_id: int,
    event_index: int,
) -> list[str]:
    """Build a text dump for the host-detail side pane."""
    if not topology:
        return [f"host {host_id}", "(no topology)"]
    node_meta = next((n for n in topology["nodes"] if int(n["id"]) == host_id), None)
    if node_meta is None:
        return [f"host {host_id}", "(not in topology)"]

    lines = [f"host {host_id}"]
    for key, label in (
        ("subnet", "subnet"),
        ("layer", "layer"),
        ("os", "os"),
        ("os_version", "os version"),
        ("ip", "ip"),
        ("total_services", "services"),
    ):
        if node_meta.get(key) is not None:
            lines.append(f"{label}: {node_meta[key]}")
    if node_meta.get("is_endpoint"):
        lines.append("role: exposed endpoint")
    if node_meta.get("is_database"):
        lines.append("role: database")

    # Per-host event history up to cursor.
    end = min(event_index + 1, len(events))
    phases = 0
    compromised_at: float | None = None
    last_tech: str | None = None
    interrupts = 0
    for ev in events[:end]:
        if ev.get("host_id") != host_id:
            continue
        if ev["type"] == "phase_started":
            phases += 1
            if ev.get("technique_id"):
                last_tech = ev["technique_id"]
        elif ev["type"] == "host_compromised":
            compromised_at = float(ev["t"])
        elif ev["type"] == "attack_interrupted":
            interrupts += 1
    lines.append(f"phases observed: {phases}")
    lines.append(f"interrupts: {interrupts}")
    if last_tech:
        lines.append(f"last technique: {last_tech}")
    if compromised_at is not None:
        lines.append(f"compromised at t={compromised_at:.1f}s")
    else:
        lines.append("not compromised at cursor")

    services = node_meta.get("services") or []
    if services:
        lines.append(f"services: {', '.join(services[:6])}{'…' if len(services) > 6 else ''}")
    return lines
