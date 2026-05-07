"""Phase-lane figure for the Attack Profile view.

Takes a ``SubgraphView`` and projects its techniques onto the six MTDSim
simulator phases via the ``TACTIC_TO_PHASE`` mapping. The rendered figure
makes the tactic->phase collapse visually explicit: each phase is a lane,
each technique is a dot coloured by its ATT&CK tactic.

The figure is intentionally read-only; interactions (selection, pan) live
in the GAP iframe alongside.
"""

from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile, TACTIC_LAYERS
from mtdsim.attacker.gap.selectors import SubgraphView
from mtdsim.attacker.profile_generator import PHASES, TACTIC_TO_PHASE


# Stable palette keyed on tactic. Matches the GAP viewer's tactic band hues.
_TACTIC_COLOURS = {
    "reconnaissance":       "#7dcfff",
    "resource-development": "#bb9af7",
    "initial-access":       "#f7768e",
    "execution":            "#e0af68",
    "persistence":          "#9ece6a",
    "privilege-escalation": "#ff9e64",
    "defense-evasion":      "#c0caf5",
    "credential-access":    "#f4d58d",
    "discovery":            "#73daca",
    "lateral-movement":     "#b4f9f8",
    "collection":           "#cfc9c2",
    "command-and-control":  "#9d7cd8",
    "exfiltration":         "#db4b4b",
    "impact":               "#ff5370",
}

_PHASE_Y = {phase: -i for i, phase in enumerate(PHASES)}


def _empty() -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        margin=dict(l=8, r=8, t=8, b=8),
        height=260,
        plot_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                x=0.5, y=0.5, xref="paper", yref="paper",
                text="Select a subgraph to see its kill-chain projection.",
                showarrow=False, font=dict(color="#6c757d"),
            )
        ],
    )
    return fig


def build_phase_lanes_figure(
    view: Optional[SubgraphView],
    gap: GeneralisedAttackProfile,
) -> go.Figure:
    if view is None or not view.node_set:
        return _empty()

    # Bucket techniques by phase, preserving ATT&CK tactic-layer order within
    # each phase so similar tactics cluster together visually.
    buckets: dict[str, list[tuple[str, str]]] = {p: [] for p in PHASES}
    for tid in view.node_set:
        node = gap.nodes.get(tid)
        if node is None:
            continue
        tactic = node.primary_tactic or ""
        phase = TACTIC_TO_PHASE.get(tactic)
        if phase is None:
            continue
        buckets[phase].append((tid, tactic))

    for phase in buckets:
        buckets[phase].sort(
            key=lambda pair: (TACTIC_LAYERS.get(pair[1], 99), pair[0])
        )

    fig = go.Figure()

    # Lane background bands — one per phase, faint alternating fill.
    for i, phase in enumerate(PHASES):
        y = _PHASE_Y[phase]
        fig.add_shape(
            type="rect",
            x0=-0.5, x1=1.5, y0=y - 0.45, y1=y + 0.45,
            xref="paper", yref="y",
            fillcolor="#f5f6fa" if i % 2 == 0 else "#ffffff",
            line=dict(width=0),
            layer="below",
        )

    # Technique dots per lane. Wrap into multiple rows within each lane
    # so high-cardinality phases (e.g. EXPLOIT_VULN under MODE_ALL with
    # ~600 techniques) don't degenerate into a single illegible line.
    max_lane = max((len(v) for v in buckets.values()), default=1)
    per_row = 60  # dots per row before wrapping
    for phase, items in buckets.items():
        if not items:
            continue
        y_base = _PHASE_Y[phase]
        xs: list[float] = []
        ys: list[float] = []
        for i in range(len(items)):
            row = i // per_row
            col = i % per_row
            xs.append(col / max(per_row - 1, 1))
            # Stack rows downward within the lane band (-0.4 .. +0.4).
            n_rows = max(1, (len(items) + per_row - 1) // per_row)
            if n_rows == 1:
                y_off = 0.0
            else:
                y_off = -0.32 + (0.64 * row / max(n_rows - 1, 1))
            ys.append(y_base + y_off)
        colours = [_TACTIC_COLOURS.get(t, "#888") for _, t in items]
        hover = [
            f"<b>{tid}</b><br>{gap.nodes[tid].technique_name}<br>"
            f"tactic: {tac}<br>phase: {phase}"
            for tid, tac in items
        ]
        fig.add_trace(go.Scattergl(
            x=xs, y=ys,
            mode="markers",
            marker=dict(size=7, color=colours, line=dict(color="#2a2f45", width=0.4)),
            hovertext=hover,
            hoverinfo="text",
            showlegend=False,
        ))

    # Lane labels (phase name + count) anchored at the left margin.
    for phase in PHASES:
        y = _PHASE_Y[phase]
        fig.add_annotation(
            x=0, y=y, xref="paper", yref="y",
            text=f"<b>{phase}</b> · {len(buckets[phase])}",
            showarrow=False,
            xanchor="right",
            xshift=-8,
            font=dict(size=11, color="#3b4261"),
        )

    fig.update_layout(
        margin=dict(l=160, r=16, t=8, b=8),
        height=380,
        plot_bgcolor="white",
        xaxis=dict(visible=False, range=[-0.05, 1.05]),
        yaxis=dict(
            visible=False,
            range=[min(_PHASE_Y.values()) - 0.7, max(_PHASE_Y.values()) + 0.7],
        ),
    )
    return fig
