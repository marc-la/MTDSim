"""GAP iframe panel (SA L2: Comprehension).

The iframe renders an unmodified ``gap.html`` produced by
``mtdsim.attacker.gap.viz.renderer.GapRenderer``. This module is thin on
purpose: all interaction happens via postMessage (step 5 of the plan), and
a clientside callback in ``app.py`` posts messages when the replay cursor
advances. The Python side never mutates the iframe's DOM.

If no gap.html is provided via ``--gap-html``, the panel renders an
explanatory placeholder. Catalog-driven regeneration lands in step 7.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from dash import html


IFRAME_ROUTE = "/gap.html"


def build_gap_panel_body(gap_html_path: Optional[Path]) -> html.Div:
    if gap_html_path is None or not gap_html_path.exists():
        return html.Div(
            [
                html.P(
                    "No gap.html bound.",
                    className="text-muted mb-1",
                ),
                html.P(
                    [
                        "Render one with ",
                        html.Code("GapRenderer(gap).render_interactive('gap.html')"),
                        " and pass ",
                        html.Code("--gap-html PATH"),
                        ".",
                    ],
                    className="text-muted small",
                ),
            ],
            className="p-3",
        )

    return html.Iframe(
        id="gap-iframe",
        src=IFRAME_ROUTE,
        style={
            "width": "100%",
            "height": "360px",
            "border": "none",
        },
    )
