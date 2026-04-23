"""Attacker view: kill-chain phase tracker + MITRE technique coverage.

Three blocks:

1. **Phase tracker** — the six MTDSim phases as chevrons; the current one is
   highlighted, past ones dimmed, future ones greyed. SA-Checklist §2.1.
2. **Technique frequency bar** — horizontal bars of MITRE ATT&CK technique
   use so far at the cursor. SA-Checklist §2.4 (heatmap equivalent for one
   run; a true tactic×technique heatmap needs the GAP node catalog, which
   is the attacker subgraph view's job and stays in the GAP iframe).
3. **Per-host compromise list** — hosts the attacker has touched, with the
   technique that compromised each.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

from mtdsim.viz.replay.log import EventLog


PHASE_ORDER = [
    "SCAN_HOST",
    "ENUM_HOST",
    "SCAN_PORT",
    "EXPLOIT_VULN",
    "BRUTE_FORCE",
    "SCAN_NEIGHBOR",
]
PHASE_COLOURS = {
    "SCAN_HOST": "#6a4c93",
    "ENUM_HOST": "#1982c4",
    "SCAN_PORT": "#8ac926",
    "EXPLOIT_VULN": "#ffca3a",
    "BRUTE_FORCE": "#ff924c",
    "SCAN_NEIGHBOR": "#ff595e",
}


def technique_counts(log: EventLog, event_index: int) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    end = min(event_index + 1, len(log.events))
    for ev in log.events[:end]:
        if ev["type"] != "phase_started":
            continue
        tid = ev.get("technique_id")
        if not tid:
            continue
        counts[tid] = counts.get(tid, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: -kv[1])
    return ordered


def compromised_hosts_rollup(log: EventLog, event_index: int) -> list[dict[str, Any]]:
    rolls: list[dict[str, Any]] = []
    seen: set[int] = set()
    end = min(event_index + 1, len(log.events))
    for ev in log.events[:end]:
        if ev["type"] != "host_compromised":
            continue
        host_id = ev.get("host_id")
        if host_id is None or host_id in seen:
            continue
        seen.add(host_id)
        rolls.append(
            {
                "host_id": host_id,
                "t": float(ev["t"]),
                "phase": ev.get("phase"),
                "technique_id": ev.get("technique_id"),
            }
        )
    rolls.sort(key=lambda r: r["t"])
    return rolls


def build_phase_tracker(active_phase: str | None) -> go.Figure:
    fig = go.Figure()
    for i, phase in enumerate(PHASE_ORDER):
        is_active = phase == active_phase
        fig.add_trace(
            go.Scatter(
                x=[i],
                y=[0],
                mode="markers+text",
                marker=dict(
                    size=54 if is_active else 40,
                    color=PHASE_COLOURS[phase] if is_active else "#e9ecef",
                    line=dict(
                        color=PHASE_COLOURS[phase],
                        width=3 if is_active else 1,
                    ),
                ),
                text=[phase.replace("_", "\n")],
                textposition="middle center",
                textfont=dict(
                    color="white" if is_active else "#495057",
                    size=10,
                    family="system-ui",
                ),
                hoverinfo="text",
                hovertext=phase,
                showlegend=False,
            )
        )
    for i in range(len(PHASE_ORDER) - 1):
        fig.add_annotation(
            x=i + 0.5,
            y=0,
            ax=i + 0.1,
            ay=0,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            arrowhead=2,
            arrowsize=1.2,
            arrowcolor="#adb5bd",
            showarrow=True,
        )
    fig.update_layout(
        height=120,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        xaxis=dict(visible=False, range=[-0.5, len(PHASE_ORDER) - 0.5]),
        yaxis=dict(visible=False, range=[-0.6, 0.6]),
    )
    return fig


def build_technique_bar(log: EventLog, event_index: int, max_rows: int = 18) -> go.Figure:
    counts = technique_counts(log, event_index)[:max_rows]
    if not counts:
        fig = go.Figure()
        fig.update_layout(
            height=260,
            margin=dict(l=10, r=10, t=30, b=20),
            plot_bgcolor="white",
            annotations=[
                dict(
                    text="No techniques executed yet.",
                    showarrow=False,
                    font=dict(color="#6c757d"),
                )
            ],
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        return fig
    tids, ns = zip(*counts)
    fig = go.Figure(
        go.Bar(
            x=list(ns),
            y=list(tids),
            orientation="h",
            marker=dict(color="#1f77b4"),
            hovertemplate="%{y}: %{x} phase entries<extra></extra>",
        )
    )
    fig.update_layout(
        height=max(260, 22 * len(counts) + 60),
        margin=dict(l=10, r=20, t=30, b=30),
        plot_bgcolor="white",
        title="Technique frequency (cumulative at cursor)",
        xaxis=dict(title="count"),
        yaxis=dict(autorange="reversed"),
    )
    return fig
