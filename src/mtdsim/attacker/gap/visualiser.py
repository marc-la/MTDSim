"""
Interactive and static visualisation for the Generalised Attack Profile.

``MITRETechniqueDependencyVisualiser`` wraps pyvis for interactive HTML
output and networkx for layout analytics. Visual encoding follows
Section 6.3 of the Attack Graph Design Schema v0.3.
"""

from __future__ import annotations

import json as _json
import re as _re
from typing import Iterable, Optional

import networkx as nx

from mtdsim.attacker.gap.schema import (
    TACTIC_ORDER,
    DependencyEdge,
    GeneralisedAttackProfile,
    TechniqueNode,
)


# Section 6.3: 14-colour categorical palette for tactic layers (0-13).
_TACTIC_PALETTE = [
    "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462",
    "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
    "#1f78b4", "#e31a1c",
]

_EVIDENCE_COLOUR = {
    "co_occurrence":    "#1f77b4",  # blue
    "attack_flow":      "#2ca02c",  # green
    "caldera_sequence": "#ff7f0e",  # orange
    "ontology":         "#9467bd",  # purple
    "documentation":    "#7f7f7f",  # grey
    "cti_report":       "#7f7f7f",
}


class MITRETechniqueDependencyVisualiser:
    """
    Interactive pyvis-based visualiser for a GeneralisedAttackProfile.

    Usage
    -----
    >>> viz = MITRETechniqueDependencyVisualiser(gap)
    >>> viz.render_interactive("gap.html")
    >>> viz.render_interactive("gap_af_only.html", evidence_types={"attack_flow"})

    Visual encoding (Schema v0.3 Section 6.3):
      - Node colour by ``tactic_layer``
      - Node size scaled by ``campaign_count``
      - Orphan nodes rendered with a dashed border
      - Edge colour by primary ``evidence_type``
      - Edge width proportional to confidence
      - Consensus edges (source_count >= 2) emphasised (thicker)
      - Solid edges = forward (tactic-respecting), dashed = backward
    """

    def __init__(self, gap: GeneralisedAttackProfile):
        self.gap = gap
        self._nx_graph: Optional[nx.DiGraph] = None

    # ---------------------------------------------------------------------
    # NetworkX view
    # ---------------------------------------------------------------------

    def to_networkx(self) -> nx.DiGraph:
        """Materialise a NetworkX DiGraph view, caching the result."""
        if self._nx_graph is not None:
            return self._nx_graph
        g = nx.DiGraph()
        for tid, node in self.gap.nodes.items():
            g.add_node(
                tid,
                label=node.technique_name,
                tactic_layer=node.tactic_layer,
                primary_tactic=node.primary_tactic,
                campaign_count=node.campaign_count,
                group_count=node.group_count,
            )
        for e in self.gap.edges:
            g.add_edge(
                e.source_id,
                e.target_id,
                evidence_type=e.evidence_type,
                confidence=e.confidence,
                support=e.support,
                source_count=e.source_count,
                is_backward=e.is_backward,
            )
        self._nx_graph = g
        return g

    # ---------------------------------------------------------------------
    # Filtering helpers
    # ---------------------------------------------------------------------

    def _filtered_edges(
        self,
        evidence_types: Optional[set[str]] = None,
        min_confidence: float = 0.0,
        only_consensus: bool = False,
    ) -> list[DependencyEdge]:
        edges = self.gap.edges
        if evidence_types is not None:
            edges = [
                e for e in edges
                if any(ev.source_type in evidence_types for ev in e.evidence)
            ]
        if min_confidence > 0:
            edges = [e for e in edges if e.confidence >= min_confidence]
        if only_consensus:
            edges = [e for e in edges if e.source_count >= 2]
        return edges

    # ---------------------------------------------------------------------
    # Interactive HTML (pyvis)
    # ---------------------------------------------------------------------

    _X_SPACING = 320
    _Y_SPACING = 70

    def render_interactive(
        self,
        output_path: str,
        evidence_types: Optional[set[str]] = None,
        min_confidence: float = 0.0,
        only_consensus: bool = False,
        hide_isolated: bool = False,
        notebook: bool = False,
        height: str = "900px",
        width: str = "100%",
    ) -> str:
        """
        Write an interactive HTML visualisation to ``output_path`` and return
        the path. Requires pyvis.
        """
        from pyvis.network import Network

        edges = self._filtered_edges(
            evidence_types=evidence_types,
            min_confidence=min_confidence,
            only_consensus=only_consensus,
        )

        active_tids = set()
        for e in edges:
            active_tids.add(e.source_id)
            active_tids.add(e.target_id)

        net = Network(
            height=height,
            width=width,
            directed=True,
            notebook=notebook,
            cdn_resources="in_line",
            bgcolor="#ffffff",
            font_color="#222222",
        )
        net.toggle_physics(False)

        # Layered Sugiyama-style positioning (x = tactic layer, y = stacked).
        per_layer_count: dict[int, int] = {}

        for tid, node in self.gap.nodes.items():
            if hide_isolated and tid not in active_tids:
                continue
            layer = max(node.tactic_layer, 0)
            y_idx = per_layer_count.get(layer, 0)
            per_layer_count[layer] = y_idx + 1

            colour = _TACTIC_PALETTE[layer % len(_TACTIC_PALETTE)]
            is_orphan = tid not in active_tids
            border = "#222222"
            border_width = 3 if is_orphan else 1
            size = 12 + min(node.campaign_count, 25)

            # Title stored as plain text; HTML rendering handled by
            # the custom tooltip injected during post-processing.
            title = (
                f"<b>{tid}: {node.technique_name}</b><br>"
                f"Tactic: {node.primary_tactic} (layer {layer})<br>"
                f"Groups: {node.group_count}, Campaigns: {node.campaign_count}<br>"
                f"Platforms: {', '.join(node.platforms) or '-'}<br>"
                f"Sub-techniques: {len(node.sub_technique_ids)}"
            )
            net.add_node(
                tid,
                label=tid,
                title=title,
                color={"background": colour, "border": border},
                borderWidth=border_width,
                borderWidthSelected=border_width + 2,
                shapeProperties={"borderDashes": [4, 4] if is_orphan else False},
                size=size,
                x=layer * self._X_SPACING,
                y=y_idx * self._Y_SPACING,
                physics=False,
            )

        node_ids = set(net.get_nodes())
        for e in edges:
            if e.source_id not in node_ids or e.target_id not in node_ids:
                continue
            colour = _EVIDENCE_COLOUR.get(e.evidence_type, "#7f7f7f")
            base_width = 1 + 4 * e.confidence
            if e.source_count >= 2:
                base_width += 2
            title = (
                f"<b>{e.source_id} &rarr; {e.target_id}</b><br>"
                f"Evidence: {e.evidence_type} (sources={e.source_count})<br>"
                f"Confidence: {e.confidence:.3f}"
                + (f"<br>Support: {e.support:.3f}" if e.support is not None else "")
                + (f"<br>Lift: {e.lift:.3f}" if e.lift is not None else "")
            )
            net.add_edge(
                e.source_id,
                e.target_id,
                color=colour,
                width=base_width,
                dashes=bool(e.is_backward),
                arrows="to",
                title=title,
            )

        net.set_options(
            """
            var options = {
              "interaction": {"hover": true, "tooltipDelay": 100, "navigationButtons": true},
              "edges": {"smooth": {"type": "cubicBezier", "forceDirection": "horizontal"}},
              "physics": {"enabled": false}
            }
            """
        )
        net.write_html(output_path, notebook=notebook, open_browser=False)
        self._post_process_html(output_path, per_layer_count)
        return output_path

    # ---------------------------------------------------------------------
    # HTML post-processing
    # ---------------------------------------------------------------------

    def _post_process_html(
        self, html_path: str, per_layer_count: dict[int, int]
    ) -> None:
        """Fix loading bar, tooltips, and add tactic-layer visual segregation."""
        with open(html_path, "r") as f:
            html = f.read()

        # -- 1. Expose the vis.js Network as a global so injected JS can use it
        html = html.replace("drawGraph();", "window._gapNetwork = drawGraph();", 1)

        # -- 2. Build tactic layer metadata for the JS overlay
        layer_data = []
        for layer_idx in range(len(TACTIC_ORDER)):
            count = per_layer_count.get(layer_idx, 0)
            if count == 0:
                continue
            label = TACTIC_ORDER[layer_idx].replace("-", " ").title()
            layer_data.append(
                {"x": layer_idx * self._X_SPACING, "count": count,
                 "label": label, "layer": layer_idx}
            )

        max_y = max(
            (c * self._Y_SPACING for c in per_layer_count.values()), default=0
        )

        # -- 3. CSS to inject
        custom_css = """
/* === GAP post-processing overrides === */

/* (a) Kill the loading bar — physics is off, stabilisation events never fire */
#loadingBar { display: none !important; }

/* (b) Hide the default vis.js tooltip (shows raw HTML) */
div.vis-tooltip { display: none !important; }

/* (c) Custom HTML-rendered tooltip */
#gap-tooltip {
    position: absolute;
    display: none;
    background: #1a1a2e;
    color: #e0e0e0;
    border: 1px solid #555;
    border-radius: 8px;
    padding: 12px 16px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 13px;
    line-height: 1.6;
    max-width: 400px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
    z-index: 9999;
    pointer-events: none;
}
#gap-tooltip b { color: #ffffff; font-size: 14px; }
"""

        # -- 4. JS to inject (runs after drawGraph sets window._gapNetwork)
        custom_js = """
<script type="text/javascript">
(function() {
    var network = window._gapNetwork;
    if (!network) return;

    /* ---- Custom tooltip ---- */
    var tooltip = document.createElement('div');
    tooltip.id = 'gap-tooltip';
    document.body.appendChild(tooltip);

    network.on('hoverNode', function(params) {
        var node = network.body.data.nodes.get(params.node);
        if (node && node.title) {
            tooltip.innerHTML = node.title;
            tooltip.style.display = 'block';
        }
    });
    network.on('blurNode', function() { tooltip.style.display = 'none'; });

    network.on('hoverEdge', function(params) {
        var edge = network.body.data.edges.get(params.edge);
        if (edge && edge.title) {
            tooltip.innerHTML = edge.title;
            tooltip.style.display = 'block';
        }
    });
    network.on('blurEdge', function() { tooltip.style.display = 'none'; });

    document.getElementById('mynetwork').addEventListener('mousemove', function(e) {
        if (tooltip.style.display === 'block') {
            tooltip.style.left = (e.pageX + 15) + 'px';
            tooltip.style.top  = (e.pageY + 15) + 'px';
        }
    });

    /* ---- Tactic layer backgrounds & header labels ---- */
    var layers  = """ + _json.dumps(layer_data) + """;
    var maxY    = """ + str(max_y) + """;
    var xSpace  = """ + str(self._X_SPACING) + """;
    var palette = """ + _json.dumps(_TACTIC_PALETTE) + """;

    network.on('afterDrawing', function(ctx) {
        ctx.save();
        var halfW = xSpace / 2 - 10;
        var topY  = -80;
        var botY  = maxY + 40;

        /* alternating tinted background bands */
        layers.forEach(function(lyr) {
            ctx.fillStyle = lyr.layer % 2 === 0
                ? 'rgba(0, 0, 0, 0.025)'
                : 'rgba(0, 0, 0, 0.055)';
            ctx.fillRect(lyr.x - halfW, topY - 60, xSpace - 20, botY - topY + 120);

            /* thin separator line */
            ctx.strokeStyle = '#cccccc';
            ctx.lineWidth = 0.5;
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(lyr.x - halfW, topY - 60);
            ctx.lineTo(lyr.x - halfW, botY + 60);
            ctx.stroke();
            ctx.setLineDash([]);
        });

        /* tactic header labels */
        layers.forEach(function(lyr) {
            var col  = palette[lyr.layer % palette.length];
            var text = lyr.label;
            ctx.font = 'bold 13px "Segoe UI", Tahoma, sans-serif';
            var tw   = ctx.measureText(text).width;
            var boxW = Math.max(tw + 24, 130);
            var boxH = 28;
            var boxX = lyr.x - boxW / 2;
            var boxY = topY - 58 - boxH;

            /* rounded-rect badge */
            var r = 6;
            ctx.beginPath();
            ctx.moveTo(boxX + r, boxY);
            ctx.lineTo(boxX + boxW - r, boxY);
            ctx.quadraticCurveTo(boxX + boxW, boxY, boxX + boxW, boxY + r);
            ctx.lineTo(boxX + boxW, boxY + boxH - r);
            ctx.quadraticCurveTo(boxX + boxW, boxY + boxH, boxX + boxW - r, boxY + boxH);
            ctx.lineTo(boxX + r, boxY + boxH);
            ctx.quadraticCurveTo(boxX, boxY + boxH, boxX, boxY + boxH - r);
            ctx.lineTo(boxX, boxY + r);
            ctx.quadraticCurveTo(boxX, boxY, boxX + r, boxY);
            ctx.closePath();
            ctx.fillStyle = col + 'cc';
            ctx.fill();
            ctx.strokeStyle = col;
            ctx.lineWidth = 1;
            ctx.stroke();

            /* label text */
            ctx.fillStyle = '#111111';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(text, lyr.x, boxY + boxH / 2);

            /* layer number underneath */
            ctx.font = '11px "Segoe UI", Tahoma, sans-serif';
            ctx.fillStyle = '#666666';
            ctx.fillText('Layer ' + lyr.layer, lyr.x, boxY + boxH + 14);
        });

        ctx.restore();
    });

    network.redraw();
})();
</script>
"""

        # Inject CSS right before closing </style>
        html = html.replace("</style>", custom_css + "\n</style>", 1)

        # Inject JS right before closing </body>
        html = html.replace("</body>", custom_js + "\n</body>", 1)

        with open(html_path, "w") as f:
            f.write(html)

    # ---------------------------------------------------------------------
    # Summary / stats
    # ---------------------------------------------------------------------

    def summary(self) -> dict:
        """Return quality metrics + a per-tactic breakdown."""
        g = self.gap
        per_layer = {}
        for layer_idx, tids in sorted(g.layers.items()):
            tactic = TACTIC_ORDER[layer_idx] if 0 <= layer_idx < len(TACTIC_ORDER) else "unknown"
            per_layer[tactic] = len(tids)

        evidence_breakdown: dict[str, int] = {}
        for e in g.edges:
            for ev in e.evidence:
                evidence_breakdown[ev.source_type] = evidence_breakdown.get(ev.source_type, 0) + 1

        return {
            "version": g.version,
            "total_techniques": g.total_techniques,
            "techniques_with_edges": g.techniques_with_edges,
            "orphan_techniques": g.orphan_techniques,
            "edge_count": g.edge_count,
            "consensus_edge_count": g.consensus_edge_count,
            "backward_edge_count": g.backward_edge_count,
            "intra_tactic_unresolved": g.intra_tactic_unresolved,
            "entry_nodes": len(g.entry_nodes),
            "objective_nodes": len(g.objective_nodes),
            "per_tactic_counts": per_layer,
            "evidence_breakdown": evidence_breakdown,
            "co_occurrence_params": {
                "min_support": g.min_support,
                "min_confidence": g.min_confidence,
                "median_threshold": g.confidence_threshold,
            },
        }
