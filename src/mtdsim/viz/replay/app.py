"""Dash app for the replay visualiser.

Full-screen tabbed layout:

- **navbar** (tabs)  Overview · Network (SA L1) · Attacker · Defender · GAP (SA L2) · Timeline (SA L3)
- **main**          active tab content (flex-fills viewport height)
- **sidebar**       run metadata + running metrics + host-detail drawer
- **transport**     sticky bottom bar: transport, speed buttons, scrubber

All tab contents are mounted once at layout time and hidden via ``display: none``
when not active. This keeps every panel's Input/Output valid so callbacks can
read ``store-playback`` without having to re-mount their components on every
tab switch. The postMessage bridge (step 5) is preserved verbatim.

Panels:

- :mod:`.panels.network`     — SA L1
- :mod:`.panels.gap_iframe`  — SA L2 (postMessage-driven highlights)
- :mod:`.panels.timeline`    — SA L3 (MTD + resource + attack Gantt)
- :mod:`.panels.attacker`    — kill-chain tracker + technique coverage
- :mod:`.panels.stats`       — run metadata + running metrics sidebar
"""

from __future__ import annotations

import dataclasses
import time
from dataclasses import asdict
from pathlib import Path
from typing import Optional

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, ctx, dcc, html, no_update

from mtdsim.viz.replay.log import (
    EventLog,
    PlaybackState,
    initial_state,
    pause,
    seek_to_index,
    set_speed,
    start,
    tick,
)
from mtdsim.viz.replay.panels import stats as stats_panel
from mtdsim.viz.replay.panels.attacker import (
    build_phase_tracker,
    build_technique_bar,
    compromised_hosts_rollup,
)
from mtdsim.viz.replay.panels.gap_iframe import IFRAME_ROUTE, build_gap_panel_body
from mtdsim.viz.replay.panels.network import (
    build_network_figure,
    empty_figure,
    host_detail_lines,
)
from mtdsim.viz.replay.panels.timeline import build_timeline_figure, empty_timeline


APP_TITLE = "MTDSim Replay Visualiser"
TICK_MS = 100
SPEED_CHOICES = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

TAB_OVERVIEW = "overview"
TAB_NETWORK = "network"
TAB_ATTACKER = "attacker"
TAB_DEFENDER = "defender"
TAB_GAP = "gap"
TAB_TIMELINE = "timeline"
TABS: list[tuple[str, str]] = [
    (TAB_OVERVIEW, "Overview"),
    (TAB_NETWORK, "Network (SA L1)"),
    (TAB_ATTACKER, "Attacker"),
    (TAB_DEFENDER, "Defender"),
    (TAB_GAP, "GAP (SA L2)"),
    (TAB_TIMELINE, "Timeline (SA L3)"),
]

_GAP_HTML_PATH: Optional[Path] = None


def _speed_button_id(speed: float) -> dict:
    return {"type": "speed-btn", "speed": speed}


def _navbar(log: Optional[EventLog]) -> dbc.Navbar:
    meta = (log.sim_meta if log else {}) or {}
    config_name = meta.get("config") or (log.path.name if log else "no log")
    scheme = meta.get("scheme") or "—"
    seed = meta.get("seed")
    subtitle_parts = [config_name, f"scheme={scheme}"]
    if seed is not None:
        subtitle_parts.append(f"seed={seed}")
    subtitle = " · ".join(str(p) for p in subtitle_parts)

    tab_buttons = dbc.Nav(
        [
            dbc.NavLink(
                label,
                id={"type": "tab-link", "tab": tab_id},
                href="#",
                active=(tab_id == TAB_OVERVIEW),
                className="px-3",
            )
            for tab_id, label in TABS
        ],
        pills=True,
        className="ms-auto",
    )

    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(APP_TITLE, className="ms-2"),
                html.Span(subtitle, className="text-white-50 small ms-3"),
                tab_buttons,
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-2",
    )


def _overview_body(log: Optional[EventLog]) -> html.Div:
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Network (SA L1)"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="overview-network",
                                        figure=_initial_network_figure(log, height=340),
                                        config={"displayModeBar": False},
                                        style={"height": "340px"},
                                    ),
                                    className="p-2",
                                ),
                            ]
                        ),
                        md=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("GAP (SA L2) — see dedicated tab"),
                                dbc.CardBody(
                                    _gap_overview_summary(log),
                                    className="p-2",
                                    style={"height": "340px", "overflow": "auto"},
                                ),
                            ]
                        ),
                        md=6,
                    ),
                ],
                className="g-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Kill-chain phase"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="overview-phase",
                                        figure=build_phase_tracker(None),
                                        config={"displayModeBar": False},
                                        style={"height": "120px"},
                                    ),
                                    className="p-1",
                                ),
                            ]
                        ),
                        md=5,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Intermediary execution (SA L3)"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="overview-timeline",
                                        figure=_initial_timeline_figure(log),
                                        config={"displayModeBar": False},
                                        style={"height": "360px"},
                                    ),
                                    className="p-1",
                                ),
                            ]
                        ),
                        md=7,
                    ),
                ],
                className="g-3 mt-1",
            ),
        ]
    )


def _network_body(log: Optional[EventLog]) -> html.Div:
    return html.Div(
        [
            dcc.Graph(
                id="network-graph",
                figure=_initial_network_figure(log, height=720),
                config={"displayModeBar": False},
                style={"height": "calc(100vh - 260px)"},
            ),
        ]
    )


def _attacker_body(log: Optional[EventLog]) -> html.Div:
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Kill-chain phase (SA-Checklist §2.1)"),
                    dbc.CardBody(
                        dcc.Graph(
                            id="attacker-phase",
                            figure=build_phase_tracker(None),
                            config={"displayModeBar": False},
                            style={"height": "140px"},
                        ),
                        className="p-2",
                    ),
                ],
                className="mb-2",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Technique frequency (SA-Checklist §2.4)"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="attacker-tech",
                                        figure=build_technique_bar(log, -1) if log else empty_timeline(),
                                        config={"displayModeBar": False},
                                        style={"height": "480px"},
                                    ),
                                    className="p-2",
                                ),
                            ]
                        ),
                        md=7,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("Compromised hosts"),
                                dbc.CardBody(
                                    html.Div(
                                        id="attacker-hosts",
                                        children=_compromised_hosts_list(log, -1),
                                        style={"maxHeight": "480px", "overflowY": "auto"},
                                    ),
                                    className="p-2",
                                ),
                            ]
                        ),
                        md=5,
                    ),
                ],
                className="g-3",
            ),
        ]
    )


def _defender_body(log: Optional[EventLog]) -> html.Div:
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader("MTD + resource + attack (SA-Checklist §3.1 / §3.2 / §2.2)"),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="defender-timeline",
                                        figure=_initial_timeline_figure(log),
                                        config={"displayModeBar": False},
                                        style={"height": "calc(100vh - 340px)"},
                                    ),
                                    className="p-2",
                                ),
                            ]
                        ),
                        md=12,
                    ),
                ]
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Interrupts (SA-Checklist §3.4)"),
                    dbc.CardBody(
                        html.Div(
                            id="defender-interrupts",
                            children=_interrupt_list(log, -1),
                            style={"maxHeight": "160px", "overflowY": "auto"},
                        ),
                        className="p-2",
                    ),
                ],
                className="mt-2",
            ),
        ]
    )


def _gap_body() -> html.Div:
    # Single mount of the gap-iframe. The postMessage bridge targets this
    # element by id; the iframe stays in the DOM even when the tab isn't
    # active so message dispatch keeps working.
    return html.Div(
        children=build_gap_panel_body(_GAP_HTML_PATH),
        style={"height": "calc(100vh - 220px)"},
    )


def _gap_overview_summary(log: Optional[EventLog]) -> html.Div:
    if log is None or not log.events:
        return html.Div(
            "Load a log to enable the GAP view.",
            className="text-muted small",
        )
    techniques = sorted(
        {ev["technique_id"] for ev in log.events if ev.get("technique_id")}
    )
    return html.Div(
        [
            html.P(
                "The GAP subgraph view is rendered in its own tab (large iframe "
                "with per-technique highlights driven by playback).",
                className="small mb-2",
            ),
            html.Div(
                f"techniques seen: {len(techniques)}",
                className="small fw-semibold",
            ),
            html.Div(
                ", ".join(techniques[:30]) + ("…" if len(techniques) > 30 else ""),
                className="small text-muted",
            ),
        ]
    )


def _timeline_body(log: Optional[EventLog]) -> html.Div:
    return html.Div(
        [
            dcc.Graph(
                id="timeline-full",
                figure=_initial_timeline_figure(log),
                config={"displayModeBar": False},
                style={"height": "calc(100vh - 220px)"},
            ),
        ]
    )


def _initial_network_figure(log: Optional[EventLog], *, height: int):
    if log is None or not log.topology:
        return empty_figure()
    return build_network_figure(
        topology=log.topology, events=log.events, event_index=-1, height=height
    )


def _initial_timeline_figure(log: Optional[EventLog]):
    if log is None:
        return empty_timeline()
    return build_timeline_figure(log, sim_t=0.0)


def _compromised_hosts_list(log: Optional[EventLog], event_index: int) -> html.Div:
    if log is None or not log.events:
        return html.Div("No compromise events.", className="text-muted")
    rolls = compromised_hosts_rollup(log, event_index)
    if not rolls:
        return html.Div("No hosts compromised at this cursor.", className="text-muted")
    return html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("host", className="small text-muted"),
                        html.Th("t", className="small text-muted"),
                        html.Th("phase", className="small text-muted"),
                        html.Th("technique", className="small text-muted"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(r["host_id"]),
                            html.Td(f"{r['t']:.0f}s"),
                            html.Td(r["phase"] or "—"),
                            html.Td(r["technique_id"] or "—"),
                        ],
                        className="small",
                    )
                    for r in rolls
                ]
            ),
        ],
        className="table table-sm",
    )


def _interrupt_list(log: Optional[EventLog], event_index: int) -> html.Div:
    if log is None or not log.interrupts:
        return html.Div("No interrupts recorded.", className="text-muted small")
    cutoff_t = log.time_at_index(event_index) if event_index >= 0 else log.t_min
    visible = [iv for iv in log.interrupts if iv.t <= cutoff_t]
    if not visible:
        return html.Div("No interrupts yet at cursor.", className="text-muted small")
    return html.Ul(
        [
            html.Li(
                f"t={iv.t:.0f}s · {iv.interrupted_by or '—'} interrupted "
                f"{iv.phase or '—'} on host {iv.host_id} ({iv.technique_id or '—'})",
                className="small",
            )
            for iv in visible[-30:]  # tail — most recent 30
        ],
        className="mb-0 ps-3",
    )


def _sidebar(log: Optional[EventLog]) -> html.Div:
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader("Run metadata"),
                    dbc.CardBody(
                        stats_panel.render_kv(stats_panel.run_metadata_rows(log)),
                        className="p-2",
                    ),
                ],
                className="mb-2",
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Live metrics"),
                    dbc.CardBody(
                        html.Div(id="sidebar-metrics"),
                        className="p-2",
                    ),
                ],
                className="mb-2",
            ),
            dbc.Card(
                [
                    dbc.CardHeader("Host detail"),
                    dbc.CardBody(
                        html.Div(id="sidebar-host", children=_host_detail_default()),
                        className="p-2",
                    ),
                ],
                className="mb-2",
            ),
        ],
    )


def _host_detail_default():
    return html.Div("Click a host in the network view.", className="text-muted small")


def _transport_bar(log: Optional[EventLog]) -> dbc.Card:
    max_index = max(0, len(log.events) - 1) if log else 0
    scrubber_disabled = log is None or not log.events
    speed_buttons = dbc.ButtonGroup(
        [
            dbc.Button(
                f"{speed:g}×",
                id=_speed_button_id(speed),
                color="secondary",
                outline=True,
                active=(speed == 1.0),
                size="sm",
            )
            for speed in SPEED_CHOICES
        ],
        className="ms-3",
    )
    transport = dbc.ButtonGroup(
        [
            dbc.Button("⏮", id="btn-step-back", color="secondary", outline=True, size="sm"),
            dbc.Button("▶", id="btn-playpause", color="primary", size="sm"),
            dbc.Button("⏭", id="btn-step-fwd", color="secondary", outline=True, size="sm"),
        ]
    )
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(transport, width="auto"),
                        dbc.Col(speed_buttons, width="auto"),
                        dbc.Col(
                            html.Div(id="playback-readout", className="text-muted small"),
                            className="ms-auto text-end",
                        ),
                    ],
                    align="center",
                    className="g-2 mb-2",
                ),
                dcc.Slider(
                    id="scrubber",
                    min=0,
                    max=max_index,
                    step=1,
                    value=0,
                    disabled=scrubber_disabled,
                    tooltip={"placement": "top", "always_visible": False},
                    marks=None,
                ),
            ]
        ),
        className="mt-2",
        style={
            "position": "sticky",
            "bottom": "0",
            "background": "white",
            "zIndex": 10,
        },
    )


def _tab_container(tab_id: str, child: html.Div, *, active: bool) -> html.Div:
    return html.Div(
        child,
        id={"type": "tab-pane", "tab": tab_id},
        style={"display": "block" if active else "none"},
    )


def _layout(log: Optional[EventLog]) -> dbc.Container:
    return dbc.Container(
        [
            _navbar(log),
            dcc.Store(id="store-playback", data=asdict(initial_state())),
            dcc.Store(id="store-active-tab", data=TAB_OVERVIEW),
            dcc.Store(id="store-selected-host", data=None),
            dcc.Interval(id="playback-tick", interval=TICK_MS, n_intervals=0),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            _tab_container(TAB_OVERVIEW, _overview_body(log), active=True),
                            _tab_container(TAB_NETWORK, _network_body(log), active=False),
                            _tab_container(TAB_ATTACKER, _attacker_body(log), active=False),
                            _tab_container(TAB_DEFENDER, _defender_body(log), active=False),
                            _tab_container(TAB_GAP, _gap_body(), active=False),
                            _tab_container(TAB_TIMELINE, _timeline_body(log), active=False),
                        ],
                        md=9,
                    ),
                    dbc.Col(_sidebar(log), md=3),
                ],
                className="g-3",
            ),
            _transport_bar(log),
        ],
        fluid=True,
        style={"minHeight": "100vh", "paddingBottom": "20px"},
    )


def _register_callbacks(app: dash.Dash, log: Optional[EventLog]) -> None:
    event_ts = log.event_ts if log else []
    t_max = log.t_max if log else 0.0

    def _to_state(data: dict) -> PlaybackState:
        return PlaybackState(**data)

    def _to_dict(state: PlaybackState) -> dict:
        return dataclasses.asdict(state)

    @app.callback(
        Output("store-playback", "data"),
        Input("playback-tick", "n_intervals"),
        Input("btn-playpause", "n_clicks"),
        Input("btn-step-back", "n_clicks"),
        Input("btn-step-fwd", "n_clicks"),
        Input("scrubber", "value"),
        Input({"type": "speed-btn", "speed": dash.ALL}, "n_clicks"),
        State("store-playback", "data"),
        State({"type": "speed-btn", "speed": dash.ALL}, "id"),
        prevent_initial_call=False,
    )
    def _advance(
        _tick_n,
        _play_clicks,
        _back_clicks,
        _fwd_clicks,
        scrubber_value,
        _speed_clicks_list,
        state_data,
        speed_ids,
    ):
        if not event_ts:
            return no_update

        state = _to_state(state_data) if state_data else initial_state()
        now = time.monotonic()
        trigger = ctx.triggered_id

        if trigger == "btn-playpause":
            state = pause(state) if state.playing else start(state, now_wall=now)
        elif trigger == "btn-step-fwd":
            state = seek_to_index(
                state, event_index=state.event_index + 1, event_ts=event_ts, now_wall=now
            )
        elif trigger == "btn-step-back":
            state = seek_to_index(
                state, event_index=max(state.event_index - 1, 0), event_ts=event_ts, now_wall=now
            )
        elif trigger == "scrubber":
            if scrubber_value is not None and scrubber_value != state.event_index:
                state = seek_to_index(
                    state, event_index=int(scrubber_value), event_ts=event_ts, now_wall=now
                )
        elif isinstance(trigger, dict) and trigger.get("type") == "speed-btn":
            state = set_speed(state, speed=float(trigger["speed"]), now_wall=now)
        elif trigger == "playback-tick":
            state = tick(state, now_wall=now, event_ts=event_ts, t_max=t_max)
        else:
            return no_update

        return _to_dict(state)

    @app.callback(
        Output("scrubber", "value"),
        Output("playback-readout", "children"),
        Output("btn-playpause", "children"),
        Input("store-playback", "data"),
    )
    def _render_transport(state_data):
        state = _to_state(state_data) if state_data else initial_state()
        readout = (
            f"t = {state.sim_t:,.1f}s · event {state.event_index + 1}"
            f"/{len(event_ts)} · {state.speed:g}×"
        )
        play_icon = "⏸" if state.playing else "▶"
        return state.event_index if state.event_index >= 0 else 0, readout, play_icon

    @app.callback(
        Output({"type": "speed-btn", "speed": dash.ALL}, "active"),
        Input("store-playback", "data"),
        State({"type": "speed-btn", "speed": dash.ALL}, "id"),
    )
    def _highlight_speed(state_data, speed_ids):
        state = _to_state(state_data) if state_data else initial_state()
        return [bool(abs(s["speed"] - state.speed) < 1e-9) for s in speed_ids]

    # Tab routing — click a nav pill to switch views.
    @app.callback(
        Output("store-active-tab", "data"),
        Output({"type": "tab-link", "tab": dash.ALL}, "active"),
        Input({"type": "tab-link", "tab": dash.ALL}, "n_clicks"),
        State({"type": "tab-link", "tab": dash.ALL}, "id"),
        prevent_initial_call=True,
    )
    def _switch_tab(_n_clicks, tab_ids):
        trigger = ctx.triggered_id
        if not isinstance(trigger, dict):
            return no_update, no_update
        selected = trigger.get("tab", TAB_OVERVIEW)
        actives = [tid.get("tab") == selected for tid in tab_ids]
        return selected, actives

    @app.callback(
        Output({"type": "tab-pane", "tab": dash.ALL}, "style"),
        Input("store-active-tab", "data"),
        State({"type": "tab-pane", "tab": dash.ALL}, "id"),
    )
    def _show_active_pane(active_tab, pane_ids):
        return [
            {"display": "block" if pid.get("tab") == active_tab else "none"}
            for pid in pane_ids
        ]

    # Sidebar metrics — cheap, fires every playback tick.
    @app.callback(
        Output("sidebar-metrics", "children"),
        Input("store-playback", "data"),
    )
    def _render_metrics(state_data):
        state = _to_state(state_data) if state_data else initial_state()
        rows = stats_panel.running_metric_rows(
            log, sim_t=state.sim_t, event_index=state.event_index
        )
        return stats_panel.render_kv(rows)

    # Network figure updates — used by overview + network tab. Separate
    # callbacks so each fires only when its component exists.
    if log is not None and log.topology:
        topology = log.topology
        events = log.events

        @app.callback(
            Output("network-graph", "figure"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_network(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return build_network_figure(
                topology=topology, events=events, event_index=state.event_index, height=720
            )

        @app.callback(
            Output("overview-network", "figure"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_overview_network(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return build_network_figure(
                topology=topology, events=events, event_index=state.event_index, height=340
            )

        @app.callback(
            Output("store-selected-host", "data"),
            Input("network-graph", "clickData"),
            Input("overview-network", "clickData"),
            State("store-selected-host", "data"),
            prevent_initial_call=True,
        )
        def _capture_host_click(net_click, overview_click, current):
            payload = net_click or overview_click
            if not payload or not payload.get("points"):
                return no_update
            point = payload["points"][0]
            raw_id = point.get("id") or point.get("customdata")
            if raw_id is None:
                return current
            try:
                return int(raw_id)
            except (TypeError, ValueError):
                return current

        @app.callback(
            Output("sidebar-host", "children"),
            Input("store-selected-host", "data"),
            Input("store-playback", "data"),
        )
        def _render_host_detail(host_id, state_data):
            if host_id is None:
                return _host_detail_default()
            state = _to_state(state_data) if state_data else initial_state()
            lines = host_detail_lines(
                topology=topology,
                events=events,
                host_id=int(host_id),
                event_index=state.event_index,
            )
            return html.Div(
                [html.Div(line, className="small") for line in lines],
            )

    # Timeline — three versions wired to the same input.
    if log is not None and log.events:

        @app.callback(
            Output("timeline-full", "figure"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_timeline_full(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return build_timeline_figure(log, sim_t=state.sim_t)

        @app.callback(
            Output("defender-timeline", "figure"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_defender_timeline(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return build_timeline_figure(log, sim_t=state.sim_t)

        @app.callback(
            Output("overview-timeline", "figure"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_overview_timeline(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return build_timeline_figure(log, sim_t=state.sim_t)

        @app.callback(
            Output("defender-interrupts", "children"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_interrupts(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return _interrupt_list(log, state.event_index)

        # Attacker view — phase tracker, technique bar, compromised list.
        @app.callback(
            Output("attacker-phase", "figure"),
            Output("overview-phase", "figure"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_phase(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            cursor = log.attacker_cursor(state.event_index)
            phase = cursor.get("phase")
            fig = build_phase_tracker(phase)
            return fig, fig

        @app.callback(
            Output("attacker-tech", "figure"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_tech(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return build_technique_bar(log, state.event_index)

        @app.callback(
            Output("attacker-hosts", "children"),
            Input("store-playback", "data"),
            prevent_initial_call=True,
        )
        def _update_hosts(state_data):
            state = _to_state(state_data) if state_data else initial_state()
            return _compromised_hosts_list(log, state.event_index)


def build_app(
    log: Optional[EventLog] = None,
    *,
    gap_html_path: Optional[Path] = None,
) -> dash.Dash:
    global _GAP_HTML_PATH
    _GAP_HTML_PATH = gap_html_path

    app = dash.Dash(
        __name__,
        title=APP_TITLE,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )
    app.layout = _layout(log)
    _register_callbacks(app, log)
    _register_gap_iframe_bridge(app, log)
    _register_gap_route(app, gap_html_path)
    return app


def _register_gap_route(app: dash.Dash, gap_html_path: Optional[Path]) -> None:
    if gap_html_path is None:
        return
    resolved = gap_html_path.resolve()

    @app.server.route(IFRAME_ROUTE)
    def _serve_gap():
        from flask import send_file
        return send_file(str(resolved), mimetype="text/html")


def _register_gap_iframe_bridge(app: dash.Dash, log: Optional[EventLog]) -> None:
    """Clientside postMessage bridge — mirror playback state into the iframe.

    Preserved from step 5. The handler is clientside so it runs in the
    browser (which is where ``window.postMessage`` lives). Walks the event
    slice [prev, cur] and emits:

      - HIGHLIGHT_CURRENT for the latest technique_id at the cursor,
      - MARK_EXECUTED for each technique seen since the previous tick,
      - MARK_INTERRUPTED whenever attack_interrupted fires.

    On seeks backwards or to the start, it sends RESET and re-sends the
    executed set up to the cursor.
    """
    if log is None or not log.events:
        return

    _events_summary = [
        {
            "i": i,
            "t": float(ev["t"]),
            "type": ev["type"],
            "tid": ev.get("technique_id"),
            "meta_mtd": (ev.get("meta") or {}).get("mtd_name")
            if ev["type"] == "attack_interrupted"
            else None,
        }
        for i, ev in enumerate(log.events)
    ]

    app.layout.children.insert(
        1,
        dcc.Store(id="store-events-summary", data=_events_summary),
    )
    app.layout.children.insert(
        2,
        dcc.Store(id="store-last-index", data=-1),
    )

    app.clientside_callback(
        """
        function(playbackData, eventsSummary, lastIndex) {
            if (!eventsSummary || !eventsSummary.length) {
                return window.dash_clientside.no_update;
            }
            var iframe = document.getElementById('gap-iframe');
            if (!iframe || !iframe.contentWindow) {
                return window.dash_clientside.no_update;
            }
            var cur = (playbackData && typeof playbackData.event_index === 'number')
                        ? playbackData.event_index : -1;
            var prev = (typeof lastIndex === 'number') ? lastIndex : -1;

            var post = function(msg) {
                iframe.contentWindow.postMessage(msg, '*');
            };

            if (cur < prev) {
                post({ type: 'RESET' });
                for (var j = 0; j <= cur; j++) {
                    var ev = eventsSummary[j];
                    if (ev && ev.tid && ev.type === 'phase_started') {
                        post({ type: 'MARK_EXECUTED', technique_id: ev.tid });
                    } else if (ev && ev.type === 'attack_interrupted' && ev.tid) {
                        post({ type: 'MARK_INTERRUPTED', technique_id: ev.tid,
                               reason: ev.meta_mtd || 'mtd' });
                    }
                }
            } else {
                for (var k = prev + 1; k <= cur; k++) {
                    var e2 = eventsSummary[k];
                    if (!e2) continue;
                    if (e2.type === 'phase_started' && e2.tid) {
                        post({ type: 'MARK_EXECUTED', technique_id: e2.tid });
                    } else if (e2.type === 'attack_interrupted' && e2.tid) {
                        post({ type: 'MARK_INTERRUPTED', technique_id: e2.tid,
                               reason: e2.meta_mtd || 'mtd' });
                    }
                }
            }

            var currentTid = null;
            for (var m = cur; m >= 0; m--) {
                var e3 = eventsSummary[m];
                if (e3 && e3.tid && e3.type === 'phase_started') {
                    currentTid = e3.tid;
                    break;
                }
            }
            if (currentTid) {
                post({ type: 'HIGHLIGHT_CURRENT', technique_id: currentTid });
            }

            return cur;
        }
        """,
        Output("store-last-index", "data"),
        Input("store-playback", "data"),
        State("store-events-summary", "data"),
        State("store-last-index", "data"),
    )
