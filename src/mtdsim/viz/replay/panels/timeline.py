"""Intermediary execution panel (SA L3: Projection).

Three stacked sub-panels sharing a common x-axis:

1. **MTD deployment** swim-lane (one row per mtd_name) — SA-Checklist §3.1.
2. **Resource occupation** strip (network / application) — SA-Checklist §3.2.
3. **Attack actions** swim-lane (one row per phase) — SA-Checklist §2.2,
   with host_compromised red dots and attack_interrupted purple X overlays
   (§3.4).

A moving vertical cursor tracks ``playback.sim_t``; the whole figure is a
single Plotly figure so the cursor line moves without re-drawing the bars.
"""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
MTD_COLOUR_NETWORK = "#06a77d"
MTD_COLOUR_APPLICATION = "#2a9df4"
MTD_COLOUR_OTHER = "#8d99ae"
INTERRUPT_COLOUR = "#9467bd"
COMPROMISE_COLOUR = "#e63946"


def _mtd_color(resource_type: str) -> str:
    return {
        "network": MTD_COLOUR_NETWORK,
        "application": MTD_COLOUR_APPLICATION,
    }.get(resource_type, MTD_COLOUR_OTHER)


def _phase_spans(log: EventLog) -> list[dict[str, Any]]:
    """Pair phase_started with its matching phase_completed/attack_interrupted.

    Multiple parallel phases are unusual in MTDSim but possible (one per host
    chain under interrupt-restart). Match by host_id first, then by FIFO order.
    """
    open_by_host: dict[Any, list[dict[str, Any]]] = {}
    spans: list[dict[str, Any]] = []
    for ev in log.events:
        host_key = ev.get("host_id")
        if ev["type"] == "phase_started":
            open_by_host.setdefault(host_key, []).append(dict(ev))
        elif ev["type"] in ("phase_completed", "attack_interrupted"):
            stack = open_by_host.get(host_key, [])
            if stack:
                started = stack.pop(0)
                spans.append(
                    {
                        "phase": started.get("phase") or "UNKNOWN",
                        "host_id": host_key,
                        "technique_id": started.get("technique_id"),
                        "t_start": float(started["t"]),
                        "t_end": float(ev["t"]),
                        "interrupted": ev["type"] == "attack_interrupted",
                    }
                )
    for stack in open_by_host.values():
        for started in stack:
            spans.append(
                {
                    "phase": started.get("phase") or "UNKNOWN",
                    "host_id": started.get("host_id"),
                    "technique_id": started.get("technique_id"),
                    "t_start": float(started["t"]),
                    "t_end": float(log.t_max),
                    "interrupted": False,
                }
            )
    return spans


def empty_timeline(message: str = "No events loaded.") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        height=520,
        margin=dict(l=60, r=20, t=30, b=40),
        plot_bgcolor="white",
        annotations=[dict(text=message, showarrow=False, font=dict(color="#6c757d"))],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def build_timeline_figure(log: EventLog | None, *, sim_t: float = 0.0) -> go.Figure:
    if log is None or not log.events:
        return empty_timeline()

    phase_spans = _phase_spans(log)
    mtd_names = sorted({iv.mtd_name for iv in log.mtd_intervals})

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.10,
        row_heights=[0.38, 0.18, 0.44],
        subplot_titles=(
            "<b>MTD technique</b> (defender deployments)",
            "<b>Resource</b> (occupation)",
            "<b>Attack phase</b> (attacker kill-chain)",
        ),
    )

    # ---- Row 1: MTD deployments Gantt ------------------------------------
    if mtd_names:
        for iv in log.mtd_intervals:
            fig.add_trace(
                go.Scatter(
                    x=[iv.t_start, iv.t_end],
                    y=[iv.mtd_name, iv.mtd_name],
                    mode="lines",
                    line=dict(color=_mtd_color(iv.resource_type), width=18),
                    hovertemplate=(
                        f"<b>{iv.mtd_name}</b><br>"
                        f"resource: {iv.resource_type}<br>"
                        f"t = {iv.t_start:.1f}s → {iv.t_end:.1f}s<br>"
                        f"duration: {iv.t_end - iv.t_start:.1f}s<extra></extra>"
                    ),
                    showlegend=False,
                ),
                row=1,
                col=1,
            )
    else:
        fig.add_annotation(
            xref="x1",
            yref="y1",
            x=log.t_min,
            y=0,
            text="(no MTD events in this run)",
            showarrow=False,
            font=dict(color="#6c757d", size=11),
        )

    # ---- Row 2: Resource occupation -------------------------------------
    for resource in ("network", "application"):
        ivs = [iv for iv in log.mtd_intervals if iv.resource_type == resource]
        for iv in ivs:
            fig.add_trace(
                go.Scatter(
                    x=[iv.t_start, iv.t_end],
                    y=[resource, resource],
                    mode="lines",
                    line=dict(color=_mtd_color(resource), width=22),
                    hovertemplate=(
                        f"{resource} resource busy<br>"
                        f"{iv.mtd_name} ({iv.t_start:.1f}s → {iv.t_end:.1f}s)<extra></extra>"
                    ),
                    showlegend=False,
                ),
                row=2,
                col=1,
            )

    # ---- Row 3: Attack phases Gantt -------------------------------------
    for span in phase_spans:
        phase = span["phase"]
        fig.add_trace(
            go.Scatter(
                x=[span["t_start"], span["t_end"]],
                y=[phase, phase],
                mode="lines",
                line=dict(color=PHASE_COLOURS.get(phase, "#888"), width=10),
                hovertemplate=(
                    f"<b>{phase}</b><br>"
                    f"host: {span['host_id']}<br>"
                    f"technique: {span['technique_id'] or '—'}<br>"
                    f"{span['t_start']:.1f}s → {span['t_end']:.1f}s"
                    f"{' (interrupted)' if span['interrupted'] else ''}"
                    "<extra></extra>"
                ),
                showlegend=False,
                opacity=0.55 if span["interrupted"] else 0.95,
            ),
            row=3,
            col=1,
        )

    interrupt_xs = [iv.t for iv in log.interrupts]
    interrupt_ys = [iv.phase or "UNKNOWN" for iv in log.interrupts]
    if interrupt_xs:
        fig.add_trace(
            go.Scatter(
                x=interrupt_xs,
                y=interrupt_ys,
                mode="markers",
                marker=dict(
                    color=INTERRUPT_COLOUR, size=11, symbol="x-thin", line=dict(width=2)
                ),
                hovertext=[
                    f"interrupted by {iv.interrupted_by} on host {iv.host_id} @ t={iv.t:.1f}s"
                    for iv in log.interrupts
                ],
                hoverinfo="text",
                name="interrupts",
                showlegend=False,
            ),
            row=3,
            col=1,
        )

    compromise_xs = []
    compromise_ys = []
    compromise_hover = []
    for ev in log.events:
        if ev["type"] == "host_compromised":
            compromise_xs.append(float(ev["t"]))
            compromise_ys.append(ev.get("phase") or "EXPLOIT_VULN")
            compromise_hover.append(
                f"host {ev.get('host_id')} compromised @ t={ev['t']:.1f}s "
                f"({ev.get('technique_id') or '—'})"
            )
    if compromise_xs:
        fig.add_trace(
            go.Scatter(
                x=compromise_xs,
                y=compromise_ys,
                mode="markers",
                marker=dict(color=COMPROMISE_COLOUR, size=10, symbol="circle"),
                hovertext=compromise_hover,
                hoverinfo="text",
                name="compromise",
                showlegend=False,
            ),
            row=3,
            col=1,
        )

    # Playback cursor (spans all three rows via `xref='x'` and a vertical
    # line added as a shape, so it re-renders cheaply on every tick).
    fig.add_vline(
        x=sim_t,
        line=dict(color="#212529", width=1.5, dash="dot"),
        opacity=0.85,
    )

    # Per-row background tints so the three swim-lanes read as distinct
    # sections at a glance (the user flagged these as looking undifferentiated).
    fig.update_layout(
        height=520,
        margin=dict(l=80, r=20, t=50, b=40),
        plot_bgcolor="white",
        hovermode="closest",
        uirevision="timeline-panel",
    )
    for row, tint in enumerate(["#f5f8ff", "#fff6ef", "#fff0f0"], start=1):
        fig.update_xaxes(showgrid=True, gridcolor="#eaeaea", row=row, col=1)
        fig.update_yaxes(
            showgrid=False,
            showline=True,
            linecolor="#b5b5b5",
            linewidth=1,
            row=row, col=1,
        )
        # Plotly axis domain refs are "x" (row 1, no suffix), "x2", "x3", ...
        x_suffix = "" if row == 1 else str(row)
        fig.add_shape(
            type="rect",
            xref=f"x{x_suffix} domain",
            yref=f"y{x_suffix} domain",
            x0=0, x1=1, y0=0, y1=1,
            fillcolor=tint,
            line=dict(width=0),
            layer="below",
            row=row, col=1,
        )
    fig.update_yaxes(
        title_text="MTD technique",
        categoryorder="array",
        categoryarray=mtd_names if mtd_names else ["(none)"],
        row=1,
        col=1,
    )
    fig.update_yaxes(
        title_text="resource",
        categoryorder="array",
        categoryarray=["application", "network"],
        row=2,
        col=1,
    )
    fig.update_yaxes(
        title_text="phase",
        categoryorder="array",
        categoryarray=list(reversed(PHASE_ORDER)),
        row=3,
        col=1,
    )
    fig.update_xaxes(
        title_text="simulation time (s)",
        row=3,
        col=1,
        range=[log.t_min, max(log.t_max, log.t_min + 1)],
    )
    return fig
