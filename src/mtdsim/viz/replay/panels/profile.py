"""Attack Profile view.

A selector rail (mode + value dropdowns) drives both the GAP iframe and a
phase-lane projection. The ``Save`` button writes the current
``SubgraphView`` into ``store-operational-profile`` for the Run Simulator
view to consume.
"""

from __future__ import annotations

from typing import Optional

import dash_bootstrap_components as dbc
from dash import dcc, html

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile, TACTIC_ORDER
from mtdsim.attacker.gap.selectors import (
    PLATFORM_PROFILES,
    PlatformSelector,
    SubgraphView,
    TerminalObjectiveSelector,
    GroupWitnessedTerminalSelector,
    ancestor_subgraph,
)
from mtdsim.viz.replay.panels.gap_iframe import build_gap_panel_body
from mtdsim.viz.replay.panels.phase_lanes import build_phase_lanes_figure


MODE_ALL = "all"
MODE_TACTIC = "terminal_tactic"
MODE_TECHNIQUE = "terminal_technique"
MODE_GROUP_WITNESSED = "group_witnessed"
MODE_PLATFORM = "platform"
MODE_CAMPAIGN = "campaign"

MODE_OPTIONS = [
    {"label": "All techniques (no filter)", "value": MODE_ALL},
    {"label": "Terminal objective · by tactic", "value": MODE_TACTIC},
    {"label": "Terminal objective · by technique", "value": MODE_TECHNIQUE},
    {"label": "Group-witnessed terminal", "value": MODE_GROUP_WITNESSED},
    {"label": "Platform", "value": MODE_PLATFORM},
    {"label": "Campaign", "value": MODE_CAMPAIGN},
]


def _tactic_options(gap: GeneralisedAttackProfile) -> list[dict]:
    seen = {
        gap.nodes[tid].primary_tactic
        for tid in gap.objective_nodes
        if tid in gap.nodes
    }
    return [
        {"label": t.replace("-", " ").title(), "value": t}
        for t in TACTIC_ORDER
        if t in seen
    ]


def _objective_options(gap: GeneralisedAttackProfile) -> list[dict]:
    rows = []
    for tid in gap.objective_nodes:
        node = gap.nodes.get(tid)
        if node is None:
            continue
        label = f"{tid} — {(node.technique_name or '')[:40]}"
        rows.append((node.tactic_layer, tid, label))
    rows.sort()
    return [{"label": lbl, "value": tid} for _, tid, lbl in rows]


def _platform_options() -> list[dict]:
    return [{"label": p, "value": p} for p in PLATFORM_PROFILES]


def _campaign_options(gap: GeneralisedAttackProfile) -> list[dict]:
    rows = []
    for cid, c in gap.campaigns.items():
        n = len(c.technique_ids)
        if n == 0:
            continue
        rows.append((-n, cid, f"{cid} — {c.name} ({n}T)"))
    rows.sort()
    return [{"label": lbl, "value": cid} for _, cid, lbl in rows]


def value_options_for_mode(gap: GeneralisedAttackProfile, mode: str) -> list[dict]:
    if mode == MODE_TACTIC:
        return _tactic_options(gap)
    if mode in (MODE_TECHNIQUE, MODE_GROUP_WITNESSED):
        return _objective_options(gap)
    if mode == MODE_PLATFORM:
        return _platform_options()
    if mode == MODE_CAMPAIGN:
        return _campaign_options(gap)
    return []


def resolve_view(
    gap: GeneralisedAttackProfile,
    mode: str,
    value: Optional[str],
) -> Optional[SubgraphView]:
    """Translate a (mode, value) selector pair into a ``SubgraphView``.

    Returns ``None`` if the selection is incomplete (e.g. a mode that
    requires a value but none was given).
    """
    if mode == MODE_ALL:
        nodes = frozenset(gap.nodes.keys())
        edges = frozenset((e.source_id, e.target_id) for e in gap.edges)
        return SubgraphView(
            node_set=nodes, edge_set=edges,
            provenance={"selector": "all"},
        )
    if not value:
        return None
    if mode == MODE_TACTIC:
        return TerminalObjectiveSelector(tactic=value).select(gap)
    if mode == MODE_TECHNIQUE:
        return TerminalObjectiveSelector(technique=value).select(gap)
    if mode == MODE_GROUP_WITNESSED:
        return GroupWitnessedTerminalSelector(technique=value).select(gap)
    if mode == MODE_PLATFORM:
        return PlatformSelector(profile=value).select(gap)
    if mode == MODE_CAMPAIGN:
        campaign = gap.campaigns.get(value)
        if campaign is None:
            return None
        targets = [t for t in campaign.technique_ids if t in gap.nodes]
        nodes, edges = ancestor_subgraph(gap, targets)
        return SubgraphView(
            node_set=frozenset(nodes),
            edge_set=frozenset(edges),
            provenance={
                "selector": "Campaign",
                "campaign_id": value,
                "n_techniques": len(targets),
            },
        )
    return None


def serialise_view(view: SubgraphView, mode: str, value: Optional[str]) -> dict:
    return {
        "mode": mode,
        "value": value,
        "node_set": sorted(view.node_set),
        "edge_set": [list(e) for e in view.edge_set],
        "provenance": dict(view.provenance),
    }


def build_profile_body(gap: GeneralisedAttackProfile) -> html.Div:
    selector_rail = dbc.Card(
        [
            dbc.CardHeader("Attack profile selector"),
            dbc.CardBody(
                [
                    html.Label("Mode", className="form-label small text-muted"),
                    dcc.Dropdown(
                        id="profile-mode",
                        options=MODE_OPTIONS,
                        value=MODE_ALL,
                        clearable=False,
                    ),
                    html.Label(
                        "Value",
                        className="form-label small text-muted mt-3",
                    ),
                    dcc.Dropdown(
                        id="profile-value",
                        options=[],
                        value=None,
                        placeholder="Select a mode first…",
                    ),
                    html.Div(id="profile-summary", className="small text-muted mt-3"),
                    dbc.Button(
                        "Save profile",
                        id="profile-save",
                        color="primary",
                        className="mt-3 w-100",
                    ),
                    html.Div(id="profile-save-status", className="small text-success mt-2"),
                ],
            ),
        ],
    )

    phase_lanes = dbc.Card(
        [
            dbc.CardHeader("Subgraph → kill-chain phase"),
            dbc.CardBody(
                dcc.Graph(
                    id="profile-phase-lanes",
                    figure=build_phase_lanes_figure(None, gap),
                    config={"displayModeBar": False},
                    style={"height": "380px"},
                ),
                className="p-2",
            ),
        ],
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(selector_rail, md=3),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("GAP (MITRE ATT&CK technique graph)"),
                                dbc.CardBody(
                                    build_gap_panel_body(),
                                    className="p-0",
                                    style={"height": "calc(100vh - 520px)",
                                           "minHeight": "360px"},
                                ),
                            ]
                        ),
                        md=9,
                    ),
                ],
                className="g-3",
            ),
            dbc.Row([dbc.Col(phase_lanes, md=12)], className="g-3 mt-1"),
        ]
    )
