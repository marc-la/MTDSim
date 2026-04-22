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
) -> str:
    parts = [f"<b>host {host_id}</b>", f"state: {state}"]
    if topology_node:
        if "subnet" in topology_node:
            parts.append(f"subnet: {topology_node['subnet']}")
        if "layer" in topology_node:
            parts.append(f"layer: {topology_node['layer']}")
        if "os" in topology_node:
            parts.append(f"os: {topology_node['os']}")
    if compromise_time is not None:
        parts.append(f"compromised @ t={compromise_time:.1f}s")
    return "<br>".join(parts)


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
        opacity=0.35,
        hoverinfo="skip",
        showlegend=False,
    )

    traces_by_state: dict[str, dict[str, list]] = {
        name: {"x": [], "y": [], "size": [], "text": [], "ids": []}
        for name in STATE_COLORS
    }

    for nid in node_ids:
        if nid not in pos:
            continue
        state = states_now.get(nid, "untouched")
        bucket = traces_by_state[state]
        bucket["x"].append(pos[nid][0])
        bucket["y"].append(pos[nid][1])
        bucket["size"].append(10 + 2.5 * degree.get(nid, 0))
        bucket["text"].append(
            _host_hover_text(
                host_id=nid,
                state=state,
                topology_node=node_meta.get(nid),
                compromise_time=compromise_ts.get(nid),
            )
        )
        bucket["ids"].append(str(nid))

    fig = go.Figure()
    fig.add_trace(edge_trace)
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
        height=360,
        uirevision="network-panel",
    )
    return fig
