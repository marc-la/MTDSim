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

- :mod:`.panels.network`         — SA L1
- :mod:`.panels.gap_iframe`      — SA L2 (postMessage-driven highlights)
- :mod:`.panels.hosts_timeline`  — hosts x time overlay (MTD coverage,
  per-host phase Gantt, interrupts, compromises)
- :mod:`.panels.attacker`        — kill-chain tracker + technique coverage
- :mod:`.panels.stats`           — run metadata + running metrics sidebar
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

from mtdsim.attacker import AttackerProfile
from mtdsim.attacker.gap.schema import GeneralisedAttackProfile
from mtdsim.attacker.gap.selectors import SubgraphView
from mtdsim.attacker.subgraph_profile import SubgraphAttackerProfile
from mtdsim.viz.replay.config import DEFAULT_EVENTS_DIR, PRIMARY
from mtdsim.viz.replay.gap_source import load_gap, render_gap_html
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
from mtdsim.viz.replay.panels.attacker import build_phase_tracker
from mtdsim.viz.replay.panels.gap_iframe import IFRAME_ROUTE, build_gap_panel_body
from mtdsim.viz.replay.panels.network import (
    build_network_figure,
    build_preview_figure,
    empty_figure,
    host_detail_lines,
)
from mtdsim.viz.replay.panels.phase_lanes import build_phase_lanes_figure
from mtdsim.viz.replay.panels.profile import (
    build_profile_body,
    resolve_view,
    serialise_view,
    value_options_for_mode,
)
from mtdsim.viz.replay.panels.run import (
    build_run_body,
    form_params,
    validate_params,
)
from mtdsim.viz.replay.panels.hosts_timeline import (
    build_hosts_timeline_figure,
    empty_hosts_timeline,
)
from mtdsim.viz.replay.runner import current_run_future, run_canonical_sim_async


APP_TITLE = "MTDSim TTP-driven APT Profile Visualiser"
TICK_MS = 100
# Log-scale stops so the slider reaches 64× without eating UI width. PlaybackState
# still stores speed as a float — this is just the set of snap points.
SPEED_CHOICES = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]
BOOTSTRAP_ICONS_CDN = (
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
)

TAB_PROFILE = "profile"
TAB_RUN = "run"
TABS: list[tuple[str, str]] = [
    (TAB_PROFILE, "Attack Profile"),
    (TAB_RUN, "Run Simulator"),
]

_GAP_HTML_PATH: Optional[Path] = None
_GAP: Optional[GeneralisedAttackProfile] = None
_GAP_RENDERED_HTML: Optional[str] = None

# The current event log is mutable so the Run button can hot-swap it in
# after a background run completes. Callbacks read this reference instead
# of closing over a specific EventLog.
_CURRENT_LOG: Optional[EventLog] = None
_EVENTS_DIR: Path = DEFAULT_EVENTS_DIR
# Optional pre-saved operational profile. Set by build_app(trivial=True)
# so a smoke-boot can ship through the GAP→subgraph→sim pipeline without
# the user clicking through the selector rail.
_INITIAL_PROFILE_DATA: Optional[dict] = None


def _speed_button_id(speed: float) -> dict:
    return {"type": "speed-btn", "speed": speed}


def _icon(name: str) -> html.I:
    return html.I(className=f"bi bi-{name}")


def _navbar(log: Optional[EventLog]) -> dbc.Navbar:
    tab_buttons = dbc.Nav(
        [
            dbc.NavLink(
                label,
                id={"type": "tab-link", "tab": tab_id},
                href="#",
                active=(tab_id == TAB_RUN),
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
                tab_buttons,
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-2",
    )


def _expandable_card(
    card_id: str,
    header,
    body,
    *,
    card_body_style: Optional[dict] = None,
) -> html.Div:
    """Wrap body in a card with a fullscreen toggle button.

    Toggling sets the ``mtd-fullscreen`` class on the wrapper div (see
    assets/mtd.css); the body DOM is not re-mounted, so callback wiring and
    the postMessage bridge survive the overlay.
    """
    header_row = dbc.Row(
        [
            dbc.Col(html.Span(header), width=True),
            dbc.Col(
                dbc.Button(
                    "⤢",
                    id={"type": "fs-toggle", "card": card_id},
                    size="sm",
                    color="link",
                    className="p-0 text-muted",
                    title="Toggle fullscreen",
                ),
                width="auto",
            ),
        ],
        align="center",
        className="g-0",
    )
    return html.Div(
        dbc.Card(
            [
                dbc.CardHeader(header_row),
                dbc.CardBody(body, className="p-2", style=card_body_style),
            ]
        ),
        id={"type": "fs-wrapper", "card": card_id},
        className="mtd-card-wrapper",
    )


def _run_body(log: Optional[EventLog]) -> html.Div:
    return html.Div(
        [
            build_run_body(PRIMARY),
            dbc.Row(
                [
                    dbc.Col(
                        _expandable_card(
                            "run-phase",
                            "Kill-chain phase (cursor)",
                            dcc.Graph(
                                id="overview-phase",
                                figure=build_phase_tracker(None),
                                config={"displayModeBar": False},
                                style={"height": "120px"},
                            ),
                        ),
                        md=12,
                    ),
                ],
                className="g-3 mt-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        _expandable_card(
                            "run-hosts-timeline",
                            "Hosts × time — attack phases, MTD coverage, interrupts, compromises",
                            html.Div(
                                dcc.Graph(
                                    id="overview-hosts-timeline",
                                    figure=_initial_hosts_timeline_figure(log),
                                    config={"displayModeBar": False},
                                ),
                                style={
                                    "maxHeight": "560px",
                                    "overflowY": "auto",
                                },
                            ),
                            card_body_style={"padding": "0"},
                        ),
                        md=12,
                    ),
                ],
                className="g-3 mt-2",
            ),
        ]
    )


def _profile_body(log: Optional[EventLog]) -> html.Div:
    # Full profile view: selector rail + GAP iframe + phase-lane projection.
    # Requires _GAP to be loaded (build_app handles this).
    assert _GAP is not None, "build_app must load the GAP before _profile_body()"
    return build_profile_body(_GAP)


def _initial_network_figure(log: Optional[EventLog], *, height: int):
    if log is None or not log.topology:
        return empty_figure()
    return build_network_figure(
        topology=log.topology, events=log.events, event_index=-1, height=height
    )


def _initial_hosts_timeline_figure(log: Optional[EventLog]):
    if log is None:
        return empty_hosts_timeline()
    return build_hosts_timeline_figure(log, sim_t=0.0)


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

    # Log-scale speed slider: integer stops index into SPEED_CHOICES.
    one_idx = SPEED_CHOICES.index(1.0)
    speed_slider = dcc.Slider(
        id="speed-slider",
        min=0,
        max=len(SPEED_CHOICES) - 1,
        step=1,
        value=one_idx,
        marks={i: f"{s:g}×" for i, s in enumerate(SPEED_CHOICES)},
        included=False,
    )

    transport = dbc.ButtonGroup(
        [
            dbc.Button(
                _icon("skip-start-fill"),
                id="btn-step-back", color="secondary", outline=True, size="sm",
                title="Step back",
            ),
            dbc.Button(
                _icon("play-fill"),
                id="btn-playpause", color="primary", size="sm",
                title="Play/pause",
            ),
            dbc.Button(
                _icon("skip-end-fill"),
                id="btn-step-fwd", color="secondary", outline=True, size="sm",
                title="Step forward",
            ),
        ]
    )

    transport_body = dbc.CardBody(
        [
            dbc.Row(
                [
                    dbc.Col(transport, width="auto"),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    "Speed",
                                    className="small text-muted mb-1",
                                ),
                                speed_slider,
                            ],
                            style={"minWidth": "300px"},
                        ),
                        width=True,
                    ),
                    dbc.Col(
                        html.Div(id="playback-readout", className="text-muted small"),
                        className="ms-auto text-end",
                        width="auto",
                    ),
                ],
                align="center",
                className="g-3 mb-2",
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
    )

    # Collapsible wrapper — playback transport. Starts open so the play
    # button is immediately reachable once a log loads.
    return html.Div(
        [
            dbc.Button(
                [_icon("chevron-down"), html.Span(" Playback", className="ms-2")],
                id="transport-collapse-btn",
                color="light",
                size="sm",
                className="mt-2 border",
            ),
            dbc.Collapse(
                dbc.Card(transport_body, className="mt-2"),
                id="transport-collapse",
                is_open=True,
            ),
        ],
        style={
            "position": "sticky",
            "bottom": "0",
            "background": "white",
            "zIndex": 10,
            "paddingBottom": "8px",
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
            dcc.Store(id="store-active-tab", data=TAB_RUN),
            dcc.Store(id="store-selected-host", data=None),
            dcc.Store(id="store-operational-profile", data=_INITIAL_PROFILE_DATA),
            dcc.Store(id="profile-mounted", data=False),
            dcc.Store(
                id="store-run-state",
                data={"status": "idle", "log_path": None, "message": ""},
            ),
            dcc.Interval(id="playback-tick", interval=TICK_MS, n_intervals=0),
            dcc.Interval(id="run-poll", interval=500, n_intervals=0, disabled=True),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            _tab_container(
                                TAB_PROFILE,
                                html.Div(
                                    "Profile selector mounts on first activation.",
                                    id="profile-tab-mount",
                                    className="text-muted small p-3",
                                ),
                                active=False,
                            ),
                            _tab_container(TAB_RUN, _run_body(log), active=True),
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
    def _to_state(data: dict) -> PlaybackState:
        return PlaybackState(**data)

    def _to_dict(state: PlaybackState) -> dict:
        return dataclasses.asdict(state)

    def _event_ts():
        return _CURRENT_LOG.event_ts if _CURRENT_LOG else []

    def _t_max():
        return _CURRENT_LOG.t_max if _CURRENT_LOG else 0.0

    @app.callback(
        Output("store-playback", "data"),
        Input("playback-tick", "n_intervals"),
        Input("btn-playpause", "n_clicks"),
        Input("btn-step-back", "n_clicks"),
        Input("btn-step-fwd", "n_clicks"),
        Input("scrubber", "value"),
        Input("speed-slider", "value"),
        State("store-playback", "data"),
        prevent_initial_call=False,
    )
    def _advance(
        _tick_n,
        _play_clicks,
        _back_clicks,
        _fwd_clicks,
        scrubber_value,
        speed_idx,
        state_data,
    ):
        event_ts = _event_ts()
        if not event_ts:
            return no_update

        state = _to_state(state_data) if state_data else initial_state()
        now = time.monotonic()
        trigger = ctx.triggered_id
        t_max = _t_max()

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
        elif trigger == "speed-slider":
            idx = int(speed_idx or 0)
            if 0 <= idx < len(SPEED_CHOICES):
                state = set_speed(state, speed=SPEED_CHOICES[idx], now_wall=now)
        elif trigger == "playback-tick":
            state = tick(state, now_wall=now, event_ts=event_ts, t_max=t_max)
        else:
            return no_update

        return _to_dict(state)

    @app.callback(
        Output("scrubber", "value"),
        Output("scrubber", "max"),
        Output("scrubber", "disabled"),
        Output("playback-readout", "children"),
        Output("btn-playpause", "children"),
        Input("store-playback", "data"),
        Input("store-run-state", "data"),
    )
    def _render_transport(state_data, _run_state):
        event_ts = _event_ts()
        total = len(event_ts)
        state = _to_state(state_data) if state_data else initial_state()
        scrubber_max = max(total - 1, 0)
        disabled = total == 0
        if total == 0:
            readout = "0/0 events · configure and run a simulation"
        else:
            pct = (state.event_index / max(total - 1, 1)) * 100 if state.event_index >= 0 else 0
            readout = (
                f"t = {state.sim_t:,.1f}s · event {state.event_index + 1}"
                f"/{total} · {pct:.2f}% · {state.speed:g}×"
            )
        play_icon = _icon("pause-fill") if state.playing else _icon("play-fill")
        scrubber_value = state.event_index if state.event_index >= 0 else 0
        return scrubber_value, scrubber_max, disabled, readout, play_icon

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
        selected = trigger.get("tab", TAB_RUN)
        actives = [tid.get("tab") == selected for tid in tab_ids]
        return selected, actives

    # Lazy-mount the Profile tab body the first time the user activates
    # it. Mounting unconditionally on initial layout doubles the boot DOM
    # (and triggers an extra GAP iframe fetch) for users who never visit
    # the Profile tab. The mounted flag prevents re-mount, which would
    # detach the iframe and break its postMessage bridge.
    @app.callback(
        Output("profile-tab-mount", "children"),
        Output("profile-mounted", "data"),
        Input("store-active-tab", "data"),
        State("profile-mounted", "data"),
        prevent_initial_call=True,
    )
    def _mount_profile_tab(active_tab, mounted):
        if mounted or active_tab != TAB_PROFILE or _GAP is None:
            return no_update, no_update
        return build_profile_body(_GAP), True

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

    # Single network surface — one Plotly graph with two modes:
    # (a) preview mode: form params drive build_preview_figure; (b) live
    # mode: loaded log drives build_network_figure. Replaces the legacy
    # split between run-preview (form) and overview-network (log).
    @app.callback(
        Output("run-network", "figure"),
        Output("run-network-header", "children"),
        Output("run-validation", "children"),
        Input("store-playback", "data"),
        Input("store-run-state", "data"),
        Input("run-total-nodes", "value"),
        Input("run-total-endpoints", "value"),
        Input("run-total-subnets", "value"),
        Input("run-total-layers", "value"),
        Input("run-total-database", "value"),
        Input("run-terminate-ratio", "value"),
        Input("run-seed", "value"),
    )
    def _update_run_network(
        state_data, _run_state, n, endpoints, subnets, layers, db, ratio, seed,
    ):
        # Live mode wins when a log is loaded.
        if _CURRENT_LOG is not None and _CURRENT_LOG.topology:
            state = _to_state(state_data) if state_data else initial_state()
            fig = build_network_figure(
                topology=_CURRENT_LOG.topology,
                events=_CURRENT_LOG.events,
                event_index=state.event_index,
                height=540,
            )
            return fig, "Network — live (click a host for detail)", ""
        # Preview mode — form-driven figure with validation feedback.
        try:
            params = form_params(n, endpoints, subnets, layers, db, ratio)
        except (TypeError, ValueError):
            return (
                empty_figure("Fill in all numeric fields."),
                "Network preview",
                "",
            )
        err = validate_params(params)
        if err:
            return empty_figure(err), "Network preview", err
        fig = build_preview_figure(params, seed=int(seed or 0), height=540)
        return fig, "Network preview", ""

    @app.callback(
        Output("store-selected-host", "data"),
        Input("run-network", "clickData"),
        State("store-selected-host", "data"),
        prevent_initial_call=True,
    )
    def _capture_host_click(network_click, current):
        if _CURRENT_LOG is None:
            return no_update
        payload = network_click
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
        if _CURRENT_LOG is None or host_id is None:
            return _host_detail_default()
        state = _to_state(state_data) if state_data else initial_state()
        lines = host_detail_lines(
            topology=_CURRENT_LOG.topology,
            events=_CURRENT_LOG.events,
            host_id=int(host_id),
            event_index=state.event_index,
        )
        return html.Div([html.Div(line, className="small") for line in lines])

    @app.callback(
        Output("overview-hosts-timeline", "figure"),
        Input("store-playback", "data"),
        Input("store-run-state", "data"),
    )
    def _update_overview_hosts_timeline(state_data, _run_state):
        if _CURRENT_LOG is None or not _CURRENT_LOG.events:
            return empty_hosts_timeline()
        state = _to_state(state_data) if state_data else initial_state()
        return build_hosts_timeline_figure(_CURRENT_LOG, sim_t=state.sim_t)

    @app.callback(
        Output("overview-phase", "figure"),
        Input("store-playback", "data"),
        Input("store-run-state", "data"),
    )
    def _update_phase(state_data, _run_state):
        if _CURRENT_LOG is None or not _CURRENT_LOG.events:
            return build_phase_tracker(None)
        state = _to_state(state_data) if state_data else initial_state()
        cursor = _CURRENT_LOG.attacker_cursor(state.event_index)
        phase = cursor.get("phase")
        return build_phase_tracker(phase)

    # Attack Profile selector — mode drives the value picker options; value
    # drives both the phase-lanes figure and the GAP iframe subgraph highlight.
    if _GAP is not None:
        gap = _GAP

        @app.callback(
            Output("profile-value", "options"),
            Output("profile-value", "value"),
            Input("profile-mode", "value"),
        )
        def _update_value_options(mode):
            opts = value_options_for_mode(gap, mode)
            return opts, None

        @app.callback(
            Output("profile-phase-lanes", "figure"),
            Output("profile-summary", "children"),
            Input("profile-mode", "value"),
            Input("profile-value", "value"),
        )
        def _update_profile_view(mode, value):
            view = resolve_view(gap, mode, value)
            if view is None:
                return build_phase_lanes_figure(None, gap), ""
            fig = build_phase_lanes_figure(view, gap)
            summary = (
                f"{len(view.node_set)} techniques · "
                f"{len(view.edge_set)} edges · "
                f"{view.provenance.get('selector', mode)}"
            )
            return fig, summary

        @app.callback(
            Output("store-operational-profile", "data"),
            Output("profile-save-status", "children"),
            Input("profile-save", "n_clicks"),
            State("profile-mode", "value"),
            State("profile-value", "value"),
            prevent_initial_call=True,
        )
        def _save_profile(_n, mode, value):
            view = resolve_view(gap, mode, value)
            if view is None:
                return no_update, "Pick a value before saving."
            data = serialise_view(view, mode, value)
            label = view.provenance.get("selector", mode)
            return data, f"Saved · {label} · {len(data['node_set'])} techniques"

        # Forward the selected subgraph into the iframe so GAP nodes outside
        # the set dim. Pure clientside — the iframe already knows how to
        # filter; we just hand it the node set.
        app.clientside_callback(
            """
            function(data) {
                if (!data) return window.dash_clientside.no_update;
                var iframe = document.getElementById('gap-iframe');
                if (!iframe || !iframe.contentWindow) {
                    return window.dash_clientside.no_update;
                }
                iframe.contentWindow.postMessage(
                    { type: 'SELECT_SUBGRAPH',
                      node_set: data.node_set || [],
                      edge_set: data.edge_set || [] },
                    '*'
                );
                return window.dash_clientside.no_update;
            }
            """,
            Output("profile-save-status", "title"),
            Input("store-operational-profile", "data"),
            prevent_initial_call=True,
        )

    # Run Simulator — Run button enqueues a background sim; interval polls
    # its Future and, on completion, hot-loads the log into _CURRENT_LOG.
    # The form-driven preview is folded into _update_run_network above.
    @app.callback(
        Output("run-profile-pill", "children"),
        Input("store-operational-profile", "data"),
    )
    def _show_profile_pill(profile):
        if not profile:
            return "No saved profile — will use the default attacker profile."
        label = (profile.get("provenance") or {}).get("selector") or profile.get("mode")
        n = len(profile.get("node_set") or [])
        return f"Using saved profile · {label} · {n} techniques"

    @app.callback(
        Output("store-run-state", "data"),
        Output("run-poll", "disabled"),
        Input("run-btn", "n_clicks"),
        Input("run-poll", "n_intervals"),
        State("run-total-nodes", "value"),
        State("run-total-endpoints", "value"),
        State("run-total-subnets", "value"),
        State("run-total-layers", "value"),
        State("run-total-database", "value"),
        State("run-terminate-ratio", "value"),
        State("run-seed", "value"),
        State("run-finish-time", "value"),
        State("run-scheme", "value"),
        State("store-run-state", "data"),
        State("store-operational-profile", "data"),
        prevent_initial_call=True,
    )
    def _run_or_poll(
        _n_clicks,
        _poll_n,
        total_nodes, total_endpoints, total_subnets, total_layers, total_database,
        terminate_ratio,
        seed, finish_time, scheme,
        run_state, saved_profile,
    ):
        global _CURRENT_LOG
        run_state = run_state or {"status": "idle"}
        trigger = ctx.triggered_id

        if trigger == "run-btn":
            if run_state.get("status") == "running":
                return no_update, no_update
            try:
                params = form_params(
                    total_nodes, total_endpoints, total_subnets,
                    total_layers, total_database, terminate_ratio,
                )
            except (TypeError, ValueError):
                return {"status": "idle", "log_path": None,
                        "message": "Fill in all fields before running."}, True
            err = validate_params(params)
            if err:
                return {"status": "idle", "log_path": None, "message": err}, True
            config = PRIMARY.replace(
                name="ui",
                seed=int(seed or 0),
                finish_time=int(finish_time or 1000),
                network_params=params,
            )
            profile = _materialise_profile(saved_profile)
            run_canonical_sim_async(
                config, scheme=scheme or "random",
                profile=profile, events_dir=_EVENTS_DIR, force=True,
            )
            return {"status": "running", "log_path": None,
                    "message": f"Running {scheme} on {params['total_nodes']} nodes…"}, False

        if trigger == "run-poll":
            if run_state.get("status") != "running":
                return no_update, True
            fut = current_run_future()
            if fut is None or not fut.done():
                return no_update, False
            try:
                log_path = Path(fut.result())
            except Exception as exc:
                return {"status": "idle", "log_path": None,
                        "message": f"Run failed: {exc}"}, True
            _CURRENT_LOG = EventLog.load(log_path)
            return {"status": "complete", "log_path": str(log_path),
                    "message": f"Loaded {log_path.name} ({len(_CURRENT_LOG.events)} events)."}, True

        return no_update, no_update

    @app.callback(
        Output("run-status", "children"),
        Output("run-btn", "disabled"),
        Output("run-btn-label", "children"),
        Input("store-run-state", "data"),
    )
    def _render_run_status(run_state):
        run_state = run_state or {"status": "idle"}
        status = run_state.get("status", "idle")
        msg = run_state.get("message", "")
        if status == "running":
            return msg, True, "Running…"
        return msg, False, "Run simulation"

    @app.callback(
        Output("store-playback", "data", allow_duplicate=True),
        Input("store-run-state", "data"),
        prevent_initial_call=True,
    )
    def _reset_playback_on_new_log(run_state):
        """Bump store-playback to initial_state whenever a new log loads."""
        if not run_state or run_state.get("status") != "complete":
            return no_update
        return asdict(initial_state())

    @app.callback(
        Output("transport-collapse", "is_open"),
        Input("transport-collapse-btn", "n_clicks"),
        State("transport-collapse", "is_open"),
        prevent_initial_call=True,
    )
    def _toggle_transport_collapse(_n, is_open):
        return not is_open

    # Fullscreen toggle — flip the mtd-fullscreen class on the wrapper
    # matching the clicked toggle. Runs clientside; the wrapper DOM is not
    # re-mounted so graph / iframe state survives the overlay.
    app.clientside_callback(
        """
        function(nClicksList, wrapperIds, currentClassNames) {
            var ctx = window.dash_clientside.callback_context;
            if (!ctx || !ctx.triggered || !ctx.triggered.length) {
                return window.dash_clientside.no_update;
            }
            var propId = ctx.triggered[0].prop_id;
            var idStr = propId.split('.')[0];
            var tid;
            try { tid = JSON.parse(idStr); }
            catch (e) { return window.dash_clientside.no_update; }
            var card = tid.card;
            return (wrapperIds || []).map(function(wid, i) {
                if (wid && wid.card === card) {
                    var cur = currentClassNames[i] || '';
                    var isFull = cur.indexOf('mtd-fullscreen') !== -1;
                    return isFull ? 'mtd-card-wrapper'
                                  : 'mtd-card-wrapper mtd-fullscreen';
                }
                return currentClassNames[i];
            });
        }
        """,
        Output({"type": "fs-wrapper", "card": dash.ALL}, "className"),
        Input({"type": "fs-toggle", "card": dash.ALL}, "n_clicks"),
        State({"type": "fs-wrapper", "card": dash.ALL}, "id"),
        State({"type": "fs-wrapper", "card": dash.ALL}, "className"),
        prevent_initial_call=True,
    )


def _materialise_profile(saved_profile: Optional[dict]) -> Optional[AttackerProfile]:
    """Turn a serialised ``store-operational-profile`` back into a profile.

    Returns ``None`` if the store is empty, which tells the runner to use
    the default ``AttackerProfile``.
    """
    if not saved_profile or _GAP is None:
        return None
    nodes = frozenset(saved_profile.get("node_set") or [])
    if not nodes:
        return None
    edges = frozenset(
        (a, b) for a, b in (saved_profile.get("edge_set") or [])
    )
    view = SubgraphView(
        node_set=nodes,
        edge_set=edges,
        provenance=saved_profile.get("provenance") or {},
    )
    selector_tag = (saved_profile.get("provenance") or {}).get("selector", "ui")
    return SubgraphAttackerProfile.from_subgraph_view(
        view=view,
        gap=_GAP,
        base_profile=AttackerProfile.default(),
        selector_tag=selector_tag,
    )


def build_app(
    log: Optional[EventLog] = None,
    *,
    gap_html_path: Optional[Path] = None,
    gap_json_path: Optional[Path] = None,
    events_dir: Optional[Path] = None,
    trivial: bool = False,
) -> dash.Dash:
    global _GAP_HTML_PATH, _GAP, _GAP_RENDERED_HTML, _CURRENT_LOG, _EVENTS_DIR
    global _INITIAL_PROFILE_DATA
    _GAP_HTML_PATH = gap_html_path
    _CURRENT_LOG = log
    if events_dir is not None:
        _EVENTS_DIR = events_dir

    # Always make a GAP available server-side; Phase 2 selector translation
    # consumes this. An explicit --gap-html override still wins for the
    # iframe content itself (debug-only use).
    _GAP = load_gap(gap_json_path)
    if gap_html_path is None:
        _GAP_RENDERED_HTML = render_gap_html(_GAP)
    else:
        _GAP_RENDERED_HTML = None

    if trivial:
        from mtdsim.viz.replay.fixtures import trivial_profile_payload
        _INITIAL_PROFILE_DATA = trivial_profile_payload(_GAP)
    else:
        _INITIAL_PROFILE_DATA = None

    app = dash.Dash(
        __name__,
        title=APP_TITLE,
        external_stylesheets=[dbc.themes.BOOTSTRAP, BOOTSTRAP_ICONS_CDN],
        suppress_callback_exceptions=True,
    )
    app.layout = _layout(log)
    _register_callbacks(app, log)
    _register_gap_iframe_bridge(app, log)
    _register_gap_route(app, gap_html_path)
    return app


def _register_gap_route(app: dash.Dash, gap_html_path: Optional[Path]) -> None:
    """Serve the GAP viewer HTML at ``/gap.html``.

    Prefers an explicit ``--gap-html`` file when given; otherwise returns
    the in-memory render of the committed snapshot.
    """
    from flask import Response, send_file

    if gap_html_path is not None:
        resolved = gap_html_path.resolve()

        @app.server.route(IFRAME_ROUTE)
        def _serve_gap_file():
            return send_file(str(resolved), mimetype="text/html")

        return

    @app.server.route(IFRAME_ROUTE)
    def _serve_gap_rendered():
        return Response(_GAP_RENDERED_HTML or "", mimetype="text/html")


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

    # Guard against double-mount. ``build_app`` is normally called once per
    # process, but Dash dev-reload and test fixtures both call it multiple
    # times; without this guard the inserts compound and we end up with
    # duplicate stores breaking the clientside callback bindings.
    existing_ids = {
        getattr(c, "id", None) for c in app.layout.children
    }
    if "store-events-summary" in existing_ids:
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
