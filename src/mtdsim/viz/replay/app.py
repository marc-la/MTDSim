"""Dash app for the replay visualiser.

Steps 1–3 landed the schema lock, the skeleton layout, and the playback
state machine. Later steps fill in the three panels (network / GAP iframe /
intermediary execution) and the catalog + run trigger.

Panels read from ``store-playback`` and ``store-log-summary``; no panel
writes directly to another panel's state.
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
from mtdsim.viz.replay.panels.gap_iframe import IFRAME_ROUTE, build_gap_panel_body
from mtdsim.viz.replay.panels.network import build_network_figure, empty_figure


APP_TITLE = "MTDSim Replay Visualiser"
TICK_MS = 100
SPEED_CHOICES = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

# Module-level so the layout builder can read it without a closure. Set by
# ``build_app(gap_html_path=...)``. Kept out of every callback's signature
# because the iframe src is resolved server-side exactly once at boot.
_GAP_HTML_PATH: Optional[Path] = None


def _speed_button_id(speed: float) -> dict:
    return {"type": "speed-btn", "speed": speed}


def _navbar(log_path: Optional[Path]) -> dbc.Navbar:
    subtitle = (
        f"Log: {log_path.name}" if log_path else "No log loaded — pass --log PATH."
    )
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(APP_TITLE, className="ms-2"),
                html.Span(subtitle, className="text-white-50 small"),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="mb-3",
    )


def _panel(title: str, body, card_id: str) -> dbc.Card:
    return dbc.Card(
        [
            dbc.CardHeader(title),
            dbc.CardBody(body, id=card_id),
        ],
        className="h-100",
    )


def _network_panel_body(log: Optional[EventLog]) -> html.Div:
    if log is None:
        return html.Div(
            "No log loaded — pass --log PATH.",
            className="text-muted",
        )
    fig = build_network_figure(
        topology=log.topology,
        events=log.events,
        event_index=-1,
    )
    return dcc.Graph(
        id="network-graph",
        figure=fig,
        config={"displayModeBar": False},
        style={"height": "360px"},
    )


def _controls_bar(log: Optional[EventLog]) -> dbc.Card:
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
        className="mt-3",
    )


def _log_summary(log: Optional[EventLog]) -> dict:
    if log is None:
        return {
            "loaded": False,
            "n_events": 0,
            "t_min": 0.0,
            "t_max": 0.0,
            "event_ts": [],
        }
    return {
        "loaded": True,
        "n_events": len(log.events),
        "t_min": log.t_min,
        "t_max": log.t_max,
        "event_ts": log.event_ts,
    }


def _layout(log: Optional[EventLog]) -> dbc.Container:
    return dbc.Container(
        [
            _navbar(log.path if log else None),
            dcc.Store(id="store-playback", data=asdict(initial_state())),
            dcc.Store(id="store-log-summary", data=_log_summary(log)),
            dcc.Interval(id="playback-tick", interval=TICK_MS, n_intervals=0),
            dbc.Row(
                [
                    dbc.Col(
                        _panel(
                            "Network state (SA L1)",
                            _network_panel_body(log),
                            "card-network",
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        _panel(
                            "GAP subgraph (SA L2)",
                            build_gap_panel_body(_GAP_HTML_PATH),
                            "card-gap",
                        ),
                        md=4,
                    ),
                    dbc.Col(
                        _panel(
                            "Intermediary execution (SA L3)",
                            html.Div("Empty — step 6.", className="text-muted"),
                            "card-intermediary",
                        ),
                        md=4,
                    ),
                ],
                className="g-3",
            ),
            _controls_bar(log),
        ],
        fluid=True,
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
                topology=topology,
                events=events,
                event_index=state.event_index,
            )


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
    """Clientside postMessage bridge: mirror playback state into the iframe.

    The handler is clientside so it runs in the browser (which is where
    ``window.postMessage`` lives). It walks the event slice [prev, cur] and
    emits:
      - HIGHLIGHT_CURRENT for the latest technique_id at the cursor,
      - MARK_EXECUTED for each technique seen since the previous tick,
      - MARK_INTERRUPTED whenever attack_interrupted fires.
    On seeks backwards or to the start, it sends RESET and re-sends the
    executed set up to the cursor.
    """
    if log is None or not log.events:
        return

    # Bundle the event stream once so the clientside callback can reach it.
    # Dash injects this into the browser via dcc.Store.
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
                // Scrubbed backwards: reset, then re-mark everything up to cur.
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
                // Forward: mark anything newly seen.
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

            // Always flag the most recent technique as "current".
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
