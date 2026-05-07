"""Run Simulator configuration panel.

Form seeded from the PRIMARY (Tay 2024) preset. Each field is editable; on
``Run`` a ``ReplayConfig`` is built via ``ReplayConfig.replace`` and passed
to ``run_canonical_sim_async``. The network preview on the right uses the
same ``build_network_figure`` renderer the live view uses, so preview and
replay look identical.
"""

from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from mtdsim.viz.replay.config import PRIMARY, ReplayConfig
from mtdsim.viz.replay.panels.network import build_preview_figure


SCHEMES = ["no_mtd", "random", "alternative", "simultaneous"]


# Form field definitions. Kept declarative so the callback set that reads
# them stays straight-line.
#
# gen_graph infinite-loop guard: require total_subnets >= total_layers + 3.
def _num_input(id_: str, value, *, mn=None, mx=None, step=1):
    return dcc.Input(
        id=id_,
        type="number",
        value=value,
        min=mn,
        max=mx,
        step=step,
        debounce=True,
        className="form-control form-control-sm",
    )


def build_run_body(default_config: ReplayConfig = PRIMARY) -> html.Div:
    p = default_config.network_params
    form = dbc.Card(
        [
            dbc.CardHeader("Simulation configuration"),
            dbc.CardBody(
                [
                    dbc.Alert(
                        [
                            html.Strong("Known caveat: "),
                            html.Code("terminate_compromise_ratio"),
                            " is currently ignored by the sim engine — the compromise cutoff is hardcoded at 0.25.",
                        ],
                        color="warning",
                        className="small py-2 mb-3",
                    ),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Total nodes", className="form-label small text-muted"),
                            _num_input("run-total-nodes", p["total_nodes"], mn=6),
                        ], md=6),
                        dbc.Col([
                            html.Label("Exposed endpoints", className="form-label small text-muted"),
                            _num_input("run-total-endpoints", p["total_endpoints"], mn=1),
                        ], md=6),
                    ], className="g-2"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Subnets", className="form-label small text-muted"),
                            _num_input("run-total-subnets", p["total_subnets"], mn=1),
                        ], md=6),
                        dbc.Col([
                            html.Label("Layers", className="form-label small text-muted"),
                            _num_input("run-total-layers", p["total_layers"], mn=1),
                        ], md=6),
                    ], className="g-2 mt-1"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Databases", className="form-label small text-muted"),
                            _num_input("run-total-database", p["total_database"], mn=0),
                        ], md=6),
                        dbc.Col([
                            html.Label(
                                "Terminate compromise ratio",
                                className="form-label small text-muted",
                            ),
                            _num_input(
                                "run-terminate-ratio",
                                p["terminate_compromise_ratio"],
                                mn=0.05, mx=1.0, step=0.05,
                            ),
                        ], md=6),
                    ], className="g-2 mt-1"),
                    html.Hr(className="my-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Seed", className="form-label small text-muted"),
                            _num_input("run-seed", default_config.seed, mn=0),
                        ], md=4),
                        dbc.Col([
                            html.Label("Finish time (s)", className="form-label small text-muted"),
                            _num_input("run-finish-time", default_config.finish_time, mn=100, step=100),
                        ], md=4),
                        dbc.Col([
                            html.Label("MTD scheme", className="form-label small text-muted"),
                            dcc.Dropdown(
                                id="run-scheme",
                                options=[{"label": s, "value": s} for s in SCHEMES],
                                value="random",
                                clearable=False,
                            ),
                        ], md=4),
                    ], className="g-2"),
                    html.Div(id="run-profile-pill", className="small text-muted mt-3"),
                    html.Div(id="run-validation", className="small text-danger mt-2"),
                    dbc.Button(
                        [
                            dbc.Spinner(size="sm", show_initially=False, children="", id="run-spinner"),
                            html.Span("Run simulation", id="run-btn-label"),
                        ],
                        id="run-btn",
                        color="primary",
                        className="mt-3 w-100",
                    ),
                    html.Div(id="run-status", className="small text-muted mt-2"),
                ],
            ),
        ],
    )

    network = dbc.Card(
        [
            dbc.CardHeader(html.Span(id="run-network-header", children="Network preview")),
            dbc.CardBody(
                dcc.Graph(
                    id="run-network",
                    figure=build_preview_figure(p, seed=default_config.seed, height=540),
                    config={"displayModeBar": False},
                    style={"height": "540px"},
                ),
                className="p-2",
            ),
        ],
    )

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(form, md=4),
                    dbc.Col(network, md=8),
                ],
                className="g-3",
            ),
        ]
    )


def form_params(
    total_nodes: int,
    total_endpoints: int,
    total_subnets: int,
    total_layers: int,
    total_database: int,
    terminate_ratio: float,
) -> dict[str, Any]:
    return dict(
        total_nodes=int(total_nodes),
        total_endpoints=int(total_endpoints),
        total_subnets=int(total_subnets),
        total_layers=int(total_layers),
        total_database=int(total_database),
        terminate_compromise_ratio=float(terminate_ratio),
    )


def validate_params(params: dict[str, Any]) -> str:
    """Return an empty string if OK, else a human-readable error.

    Guards against the ``gen_graph`` infinite-loop trap: the current guard
    condition in [mtdsim.network.network.Network.gen_graph](src/mtdsim/network/network.py)
    becomes unsatisfiable when ``total_subnets < total_layers + 3``.
    """
    if params["total_subnets"] < params["total_layers"] + 3:
        return (
            "total_subnets must be at least total_layers + 3 "
            "(sim would hang on network generation)."
        )
    if params["total_endpoints"] >= params["total_nodes"]:
        return "total_endpoints must be less than total_nodes."
    if params["total_database"] >= params["total_nodes"]:
        return "total_database must be less than total_nodes."
    if params["total_nodes"] < 2 * params["total_subnets"]:
        return (
            f"total_nodes={params['total_nodes']} is below 2× total_subnets "
            f"({2 * params['total_subnets']}); engine would silently inflate it."
        )
    return ""
