"""Hosts x time overlay (Jin's recommendation).

Y-axis: hosts (one row per host). X-axis: simulation time. Layered on a
single plane so the analyst can read which MTD operations thwarted which
techniques on which hosts at a glance — the dissertation's central
research question.

Layers, top to bottom in z-order:

1. MTD coverage shading (per-host tint while resource-typed MTDs are
   active).
2. Per-host attack-phase Gantt (one bar per phase span on each host).
3. ``attack_interrupted`` X markers on the offending host's row.
4. ``host_compromised`` filled circles on the offending host's row.
5. Vertical playback cursor at ``sim_t``.

Span and per-host MTD coverage are derived from the loaded ``EventLog``
on each call. For the canonical primary log (~100 hosts, ~3-5k events)
the figure builds in well under 100 ms.
"""

from __future__ import annotations

from typing import Any, Optional

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
SUBNET_PALETTE = [
    "#7f3c8d", "#11a579", "#3969ac", "#f2b701", "#e73f74",
    "#80ba5a", "#e68310", "#008695", "#cf1c90", "#f97b72",
]
INTERRUPT_COLOUR = "#9467bd"
COMPROMISE_COLOUR = "#e63946"
MTD_NETWORK_TINT = "rgba(6, 167, 125, 0.10)"
MTD_APPLICATION_TINT = "rgba(42, 157, 244, 0.10)"


def _subnet_colour(subnet: int) -> str:
    if subnet < 0:
        return "#c5cad1"
    return SUBNET_PALETTE[subnet % len(SUBNET_PALETTE)]


def _per_host_phase_spans(
    events: list[dict[str, Any]],
    t_max: float,
) -> list[dict[str, Any]]:
    """Pair phase_started with phase_completed/attack_interrupted per host.

    Mirrors timeline.py's _phase_spans but keeps host_id as the primary
    grouping. Open spans at end-of-run are capped at t_max.
    """
    open_by_host: dict[Any, list[dict[str, Any]]] = {}
    spans: list[dict[str, Any]] = []
    for ev in events:
        host_key = ev.get("host_id")
        if ev["type"] == "phase_started":
            open_by_host.setdefault(host_key, []).append(dict(ev))
        elif ev["type"] in ("phase_completed", "attack_interrupted"):
            stack = open_by_host.get(host_key, [])
            if stack:
                started = stack.pop(0)
                spans.append({
                    "host_id": host_key,
                    "phase": started.get("phase") or "UNKNOWN",
                    "technique_id": started.get("technique_id"),
                    "t_start": float(started["t"]),
                    "t_end": float(ev["t"]),
                    "interrupted": ev["type"] == "attack_interrupted",
                    "interrupted_by": (ev.get("meta") or {}).get("mtd_name"),
                })
    for host_key, stack in open_by_host.items():
        for started in stack:
            spans.append({
                "host_id": host_key,
                "phase": started.get("phase") or "UNKNOWN",
                "technique_id": started.get("technique_id"),
                "t_start": float(started["t"]),
                "t_end": float(t_max),
                "interrupted": False,
                "interrupted_by": None,
            })
    return spans


def _ordered_host_axis(
    log: EventLog,
    spans: list[dict[str, Any]],
) -> tuple[list[str], dict[int, str], dict[int, int]]:
    """Pick which hosts to show, ordered by first-activity time.

    Returns (host_labels, label_for_id, subnet_for_id). Only hosts that
    appear in spans, interrupts, or host_compromised are included —
    listing every untouched host on a 100-node primary run drowns out
    the figure.

    Ordering by first-activity time makes the figure read like a
    swim-graph: hosts touched earliest sit at the top, propagation flows
    down the y-axis as the attacker pivots through subnets. This is the
    ordering that maps most cleanly to the dissertation's "which MTDs
    thwart which techniques on which hosts" question.
    """
    first_seen: dict[int, float] = {}
    for span in spans:
        h = span.get("host_id")
        if isinstance(h, int) and h >= 0:
            t = float(span["t_start"])
            if h not in first_seen or t < first_seen[h]:
                first_seen[h] = t
    for ev in log.events:
        if ev["type"] in ("host_compromised", "attack_interrupted"):
            h = ev.get("host_id")
            if isinstance(h, int) and h >= 0:
                t = float(ev["t"])
                if h not in first_seen or t < first_seen[h]:
                    first_seen[h] = t

    subnet_for_id: dict[int, int] = {}
    if log.topology:
        for n in log.topology.get("nodes", []):
            subnet_for_id[int(n["id"])] = int(n.get("subnet", -1))

    ordered = sorted(first_seen, key=lambda h: (first_seen[h], h))
    label_for_id = {h: f"h{h}" for h in ordered}
    host_labels = [label_for_id[h] for h in ordered]
    return host_labels, label_for_id, subnet_for_id


def _mtd_resource_coverage(
    log: EventLog,
) -> list[tuple[float, float, str, str]]:
    """List of (t_start, t_end, resource_type, mtd_name) intervals.

    Mirrors network panel's _mtd_targets_at heuristic: coverage is by
    resource_type, not per-host. Network MTDs cover all hosts; application
    MTDs cover non-endpoint hosts.
    """
    out: list[tuple[float, float, str, str]] = []
    for iv in log.mtd_intervals:
        out.append((iv.t_start, iv.t_end, iv.resource_type, iv.mtd_name))
    return out


def empty_hosts_timeline(message: str = "No events loaded.") -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        height=420,
        margin=dict(l=80, r=20, t=30, b=40),
        plot_bgcolor="white",
        annotations=[dict(
            text=message, showarrow=False, font=dict(color="#6c757d"),
            xref="paper", yref="paper", x=0.5, y=0.5,
        )],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig


def build_hosts_timeline_figure(
    log: Optional[EventLog],
    *,
    sim_t: float = 0.0,
) -> go.Figure:
    if log is None or not log.events:
        return empty_hosts_timeline()

    spans = _per_host_phase_spans(log.events, log.t_max)
    host_labels, label_for_id, subnet_for_id = _ordered_host_axis(log, spans)
    if not host_labels:
        return empty_hosts_timeline("No host activity in this run.")

    fig = go.Figure()

    # ---- Layer 1: MTD coverage shading -----------------------------------
    # One full-height rectangle per interval. Per-host application tinting
    # is approximated by full-height because per-host shapes scale O(hosts ×
    # intervals) and Plotly chokes well before the canonical primary run.
    # Network and application both tint the same band; only the colour
    # differs so the two resource types remain legible.
    for t0, t1, rtype, _mtd_name in _mtd_resource_coverage(log):
        tint = MTD_NETWORK_TINT if rtype == "network" else MTD_APPLICATION_TINT
        fig.add_shape(
            type="rect",
            xref="x", yref="paper",
            x0=t0, x1=t1, y0=0, y1=1,
            fillcolor=tint,
            line=dict(width=0),
            layer="below",
        )

    # ---- Layer 2: Per-host phase Gantt -----------------------------------
    # Bucket by (phase, interrupted) and emit ONE trace per bucket with
    # ``None``-separated segments. With 2k+ events on a 100-host run a
    # trace-per-span design grinds Plotly to a halt.
    by_phase: dict[tuple[str, bool], dict[str, list]] = {}
    for span in spans:
        host = span["host_id"]
        if host not in label_for_id:
            continue
        key = (span["phase"], bool(span["interrupted"]))
        bucket = by_phase.setdefault(key, {"x": [], "y": [], "text": []})
        label = label_for_id[host]
        bucket["x"].extend([span["t_start"], span["t_end"], None])
        bucket["y"].extend([label, label, None])
        bucket["text"].append(
            f"<b>{span['phase']}</b><br>"
            f"host: {host}<br>"
            f"technique: {span['technique_id'] or '—'}<br>"
            f"{span['t_start']:.1f}s → {span['t_end']:.1f}s"
            f"{(' · interrupted by ' + (span['interrupted_by'] or 'mtd')) if span['interrupted'] else ''}"
        )

    seen_phase_legend: set[str] = set()
    # Render in PHASE_ORDER so the legend reads kill-chain top-to-bottom.
    bucket_keys = sorted(
        by_phase.keys(),
        key=lambda k: (PHASE_ORDER.index(k[0]) if k[0] in PHASE_ORDER else 99, k[1]),
    )
    for key in bucket_keys:
        phase, interrupted = key
        bucket = by_phase[key]
        legend = phase not in seen_phase_legend
        seen_phase_legend.add(phase)
        fig.add_trace(go.Scattergl(
            x=bucket["x"],
            y=bucket["y"],
            mode="lines",
            line=dict(
                color=PHASE_COLOURS.get(phase, "#888"),
                width=11,
            ),
            opacity=0.40 if interrupted else 0.92,
            hoverinfo="skip",
            name=phase if legend else None,
            legendgroup=phase,
            showlegend=legend,
        ))

    # Single invisible-marker trace per phase carrying span hover. One
    # marker per span midpoint, all in a single trace, so hover stays cheap.
    hover_xs: list[float] = []
    hover_ys: list[str] = []
    hover_text: list[str] = []
    for span in spans:
        host = span["host_id"]
        if host not in label_for_id:
            continue
        hover_xs.append(0.5 * (span["t_start"] + span["t_end"]))
        hover_ys.append(label_for_id[host])
        hover_text.append(
            f"<b>{span['phase']}</b><br>"
            f"host: {host}<br>"
            f"technique: {span['technique_id'] or '—'}<br>"
            f"{span['t_start']:.1f}s → {span['t_end']:.1f}s"
            f"{(' · interrupted by ' + (span['interrupted_by'] or 'mtd')) if span['interrupted'] else ''}"
        )
    if hover_xs:
        fig.add_trace(go.Scattergl(
            x=hover_xs,
            y=hover_ys,
            mode="markers",
            marker=dict(size=12, color="rgba(0,0,0,0)"),
            hovertext=hover_text,
            hoverinfo="text",
            showlegend=False,
        ))

    # ---- Layer 3: attack_interrupted X markers ---------------------------
    interrupt_xs: list[float] = []
    interrupt_ys: list[str] = []
    interrupt_hover: list[str] = []
    for iv in log.interrupts:
        host = iv.host_id
        if host not in label_for_id:
            continue
        interrupt_xs.append(iv.t)
        interrupt_ys.append(label_for_id[host])
        interrupt_hover.append(
            f"interrupted by {iv.interrupted_by or 'mtd'} on host {host}<br>"
            f"phase: {iv.phase or '—'} · technique: {iv.technique_id or '—'}<br>"
            f"t = {iv.t:.1f}s"
        )
    if interrupt_xs:
        fig.add_trace(go.Scatter(
            x=interrupt_xs, y=interrupt_ys,
            mode="markers",
            marker=dict(
                color=INTERRUPT_COLOUR, size=11, symbol="x-thin",
                line=dict(width=2),
            ),
            hovertext=interrupt_hover,
            hoverinfo="text",
            name="interrupted",
        ))

    # ---- Layer 4: host_compromised dots ----------------------------------
    compromise_xs: list[float] = []
    compromise_ys: list[str] = []
    compromise_hover: list[str] = []
    for ev in log.events:
        if ev["type"] != "host_compromised":
            continue
        host = ev.get("host_id")
        if host not in label_for_id:
            continue
        compromise_xs.append(float(ev["t"]))
        compromise_ys.append(label_for_id[host])
        compromise_hover.append(
            f"host {host} compromised<br>"
            f"technique: {ev.get('technique_id') or '—'}<br>"
            f"t = {ev['t']:.1f}s"
        )
    if compromise_xs:
        fig.add_trace(go.Scatter(
            x=compromise_xs, y=compromise_ys,
            mode="markers",
            marker=dict(color=COMPROMISE_COLOUR, size=10, symbol="circle"),
            hovertext=compromise_hover,
            hoverinfo="text",
            name="compromised",
        ))

    # ---- Layer 5: playback cursor ----------------------------------------
    fig.add_vline(
        x=sim_t,
        line=dict(color="#212529", width=1.5, dash="dot"),
        opacity=0.85,
    )

    # ---- Subnet stripe on the left margin --------------------------------
    # Single coloured tick per host on the left margin. Conveys subnet
    # grouping without the full-width band that fights the phase bars.
    if subnet_for_id:
        ordered_ids = [int(label[1:]) for label in host_labels]
        stripe_x: list[float] = []
        stripe_y: list[str] = []
        stripe_colours: list[str] = []
        for hid, label in zip(ordered_ids, host_labels):
            stripe_x.append(log.t_min)
            stripe_y.append(label)
            stripe_colours.append(_subnet_colour(subnet_for_id.get(hid, -1)))
        fig.add_trace(go.Scatter(
            x=stripe_x,
            y=stripe_y,
            mode="markers",
            marker=dict(symbol="square", size=10, color=stripe_colours),
            hoverinfo="skip",
            showlegend=False,
            xaxis="x",
            yaxis="y",
        ))

    fig.update_layout(
        height=max(420, 14 * len(host_labels) + 80),
        margin=dict(l=70, r=20, t=30, b=40),
        plot_bgcolor="white",
        hovermode="closest",
        uirevision="hosts-timeline",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
    )
    fig.update_xaxes(
        title_text="simulation time (s)",
        showgrid=True,
        gridcolor="#eef0f3",
        range=[log.t_min, max(log.t_max, log.t_min + 1)],
    )
    fig.update_yaxes(
        title_text="host (ordered by first activity)",
        categoryorder="array",
        categoryarray=list(reversed(host_labels)),
        showgrid=False,
        showline=True,
        linecolor="#cdd1d6",
        linewidth=1,
        tickfont=dict(size=10),
    )
    return fig
