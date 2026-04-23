"""GAP iframe panel.

The iframe renders the Cytoscape viewer served at ``/gap.html``. This
module is thin on purpose: all interaction happens via postMessage and a
clientside callback in ``app.py`` posts messages when the replay cursor
advances. The Python side never mutates the iframe's DOM.

Since Phase 3 the route is always registered from the committed GAP
snapshot (see :mod:`mtdsim.viz.replay.gap_source`), so this panel never
falls back to a placeholder.
"""

from __future__ import annotations

from dash import html


IFRAME_ROUTE = "/gap.html"


def build_gap_panel_body() -> html.Iframe:
    return html.Iframe(
        id="gap-iframe",
        src=IFRAME_ROUTE,
        style={
            "width": "100%",
            "height": "100%",
            "minHeight": "360px",
            "border": "none",
        },
    )
