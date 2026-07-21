"""Idea-conveying renderings of the L3a structural nets.

The raw SNAKES ``net.draw()`` (``render.draw_net``) is a faithful but illegible
hairball — it shows the formal bipartite object, not the *ideas*. These
renderings convey the tranche's ideas instead, in the L2 ``gasp_viz`` house
style (tactic-clustered left-to-right by ATT&CK layer, entry = green, objective
= orange, edge weight = evidence, backward edges muted red — let the structure
speak, no highlights pointing at things):

- the **single moving token** in its seed place (``● n`` in the seed label);
- the **prefix gap** — recon sits at the far left and, where it is an island,
  is *visibly* disconnected (layout speaks; unreachable-from-token places are
  dashed-grey as a restrained data cue);
- **entry / objective / sink (absorbing)** places;
- transition weight (how many GASP technique-edges back each tactic-pair).

Because each transition is one inter-tactic tactic-pair, the tactic-state
diagram is *isomorphic* to the Petri net — every edge is exactly one transition.

Rendering needs graphviz (``dot``) and the ``graphviz`` Python package; the grid
montage needs ``matplotlib``. Both are house dependencies (``gasp_viz`` uses
them) but, like SNAKES, are not yet in ``environment.yml``.
"""

from __future__ import annotations

import json
from pathlib import Path

import graphviz

from mtdsim.l2_subgraph.schema import SubgraphView
from mtdsim.l3_simulation.petri.analysis import StructuralReport
from mtdsim.l3_simulation.petri.build import GAP_PATH, GapIndex, StructuralNet

# House palette (verbatim from data/gasp/_viz/gasp_viz.py so the L3a figures sit
# beside the L2 ones).
ENTRY_FILL = "#bfe3b6"  # green  — a place holding an is_entry technique
OBJECTIVE_FILL = "#f6c177"  # orange — the class-semantic objective tactic
PLAIN_FILL = "#f4f4f4"
UNREACHABLE_BORDER = "#bbbbbb"
FORWARD_EDGE = "#444444"
BACKWARD_EDGE = "#c0504d"  # muted red — a transition that runs back up the chain


def load_tactic_layers(gap_path: Path = GAP_PATH) -> dict[str, int]:
    """``tactic -> ATT&CK layer index`` (the canonical kill-chain order)."""
    with open(gap_path) as f:
        gap = json.load(f)
    return {n["primary_tactic"]: n["tactic_layer"] for n in gap["nodes"].values()}


def _technique_counts(view: SubgraphView, gap: GapIndex) -> dict[str, int]:
    counts: dict[str, int] = {}
    for t in view.node_set:
        tac = gap.tactic_of[t]
        counts[tac] = counts.get(tac, 0) + 1
    return counts


def _node_label(tactic: str, n_tech: int, *, token: bool) -> str:
    head = f"● {tactic}" if token else tactic
    return f"{head}\n({n_tech} tech)"


def render_tactic_state_diagram(
    snet: StructuralNet,
    report: StructuralReport,
    view: SubgraphView,
    gap: GapIndex,
    tactic_layers: dict[str, int],
    viz_dir: Path,
    weights: dict | None = None,
    filename: str | None = None,
) -> Path:
    """Render one profile's net as a clean tactic-state diagram (PNG + SVG).

    ``weights`` (transition name -> ``TransitionWeights``, the primary corpus
    variant) switches the edge encoding from backing-GASP-edge counts to the
    W-A weight, on a **uniform absolute scale** (weight ∈ [0, 1] maps the same
    everywhere) so the five nets stay visually comparable — no per-net
    normalisation, no accentuation. A composed net's M6 overlay
    (``synthetic_transitions``) is drawn dashed with its declared weight —
    provenance as an encoding, on the same absolute scale. ``filename``
    overrides the output stem (default: the class name), so observed and
    composed renders of one profile can sit side by side."""
    viz_dir = Path(viz_dir)
    viz_dir.mkdir(parents=True, exist_ok=True)

    entry_tactics = set(report.entry_tactics)
    objective_tactics = set(report.objective_tactics)
    sinks = set(report.sink_tactics)
    reachable = set(report.reachable_from_entry_marking)
    tech = _technique_counts(view, gap)

    prefix = report.prefix_gap
    prefix_verdict = (
        "bridged" if prefix.recon_reaches_initial_access else "DISCONNECTED"
    )
    obj_reach = (
        "reachable from token"
        if report.all_objectives_reachable_from_entry
        else (
            "partially reachable from token"
            if report.any_objective_reachable_from_entry
            else "NOT reachable from token"
        )
    )
    kind = "weighted net (W-A flow proportion, operator-dedup)" if weights else "structural net"
    n_syn = len(snet.synthetic_transitions)
    if n_syn:
        kind += " · M6 prefix-join overlay composed"
    syn_note = f" (+{n_syn} synthetic)" if n_syn else ""
    title = (
        f"OGASP {kind} · {snet.class_name}\n"
        f"{report.n_places} places · {report.n_transitions}{syn_note} transitions · "
        f"{report.n_inter_tactic_edges} GASP edges · token seeded in "
        f"{snet.entry_tactic}\n"
        f"objective ({', '.join(report.objective_tactics)}) {obj_reach} · "
        f"recon→initial-access: {prefix_verdict}"
    )

    g = graphviz.Digraph(snet.class_name, format="png")
    g.attr(rankdir="LR", labelloc="t", label=title, fontsize="20", fontname="Helvetica")
    g.attr("node", fontname="Helvetica", fontsize="11")
    g.attr("edge", fontname="Helvetica", fontsize="9")

    present = sorted(snet.tactics, key=lambda t: (tactic_layers.get(t, 99), t))

    for tac in present:
        is_entry = tac in entry_tactics
        is_obj = tac in objective_tactics
        is_token = tac == snet.entry_tactic
        is_sink = tac in sinks
        is_reach = tac in reachable

        attrs = {
            "shape": "ellipse",
            "style": "filled",
            "fillcolor": PLAIN_FILL,
            "color": "#666666",
            "penwidth": "1.0",
        }
        if is_entry and is_obj:  # both — green→orange gradient fill
            attrs["fillcolor"] = f"{ENTRY_FILL}:{OBJECTIVE_FILL}"
        elif is_entry:
            attrs["fillcolor"] = ENTRY_FILL
        elif is_obj:
            attrs["fillcolor"] = OBJECTIVE_FILL
        if is_sink:  # absorbing marking — double outline (automaton convention)
            attrs["peripheries"] = "2"
        if is_token:  # the marked place — bold border
            attrs["penwidth"] = "2.6"
        if not is_reach:  # token cannot get here — dashed grey (the prefix gap)
            attrs["style"] = attrs["style"] + ",dashed"
            attrs["color"] = UNREACHABLE_BORDER

        g.node(tac, label=_node_label(tac, tech.get(tac, 0), token=is_token), **attrs)

    # Invisible kill-chain rail pins the L→R layer order; real transitions
    # overlay with constraint=false so cycles do not distort the layout.
    for a, b in zip(present, present[1:]):
        g.edge(a, b, style="invis", weight="100")

    # Every inter-tactic transition is drawn (the no-synthesis invariant — no
    # edge dropped). Penwidth *and* opacity carry the quantitative signal, so
    # the backbone reads over the haze (the gasp_viz convention). With a
    # weight layer the signal is the W-A routing weight on an absolute [0, 1]
    # scale, identical across the five nets (uniform thresholds — no per-net
    # normalisation); without one it falls back to per-net-scaled backing-edge
    # counts (the pre-weight structural encoding).
    max_w = max((len(t.edges) for t in snet.transitions), default=1)
    for spec in snet.transitions:
        backward = tactic_layers.get(spec.dst_tactic, 99) <= tactic_layers.get(
            spec.src_tactic, 99
        )
        if weights is not None:
            w = weights[spec.name].weight or 0.0
            frac = w
            label = f"{w:.2f}" if w > 0 else ""
        else:
            n_backing = len(spec.edges)
            frac = n_backing / max_w
            label = str(n_backing) if n_backing > 1 else ""
        penwidth = 0.6 + 2.4 * frac
        alpha = int(55 + 200 * frac)  # zero/min -> haze, max -> solid
        base = BACKWARD_EDGE if backward else FORWARD_EDGE
        g.edge(
            spec.src_tactic,
            spec.dst_tactic,
            label=label,
            color=f"{base}{alpha:02x}",
            penwidth=f"{penwidth:.2f}",
            arrowsize="0.7",
            constraint="false",
        )

    # The M6 overlay (composed nets only; empty on an observed-only build):
    # dashed = synthetic provenance class — an encoding, not accentuation. The
    # declared weight rides the same absolute penwidth/opacity scale as the
    # W-A weights, and the edge label says what it is.
    for spec in snet.synthetic_transitions:
        frac = spec.declared_weight or 0.0
        penwidth = 0.6 + 2.4 * frac
        alpha = int(55 + 200 * frac)
        g.edge(
            spec.src_tactic,
            spec.dst_tactic,
            label=f"{frac:.2f} (synthetic)",
            color=f"{FORWARD_EDGE}{alpha:02x}",
            penwidth=f"{penwidth:.2f}",
            style="dashed",
            arrowsize="0.7",
            constraint="false",
        )

    _legend(g)

    stem = viz_dir / (filename or snet.class_name)
    g.render(str(stem), cleanup=True)  # writes <stem>.png
    g.format = "svg"
    g.render(str(stem), cleanup=True)  # writes <stem>.svg
    return stem.with_suffix(".png")


def _legend(g: graphviz.Digraph) -> None:
    """A compact key — explanatory, not accentuation."""
    with g.subgraph(name="cluster_legend") as lg:
        lg.attr(label="key", fontsize="11", color="#cccccc", style="rounded")
        lg.attr("node", fontsize="9", shape="ellipse", style="filled", color="#666666")
        lg.node("lg_entry", "entry", fillcolor=ENTRY_FILL)
        lg.node("lg_obj", "objective", fillcolor=OBJECTIVE_FILL)
        lg.node("lg_token", "● token seed", fillcolor=PLAIN_FILL, penwidth="2.6")
        lg.node("lg_sink", "sink (absorbing)", fillcolor=PLAIN_FILL, peripheries="2")
        lg.node(
            "lg_unreach",
            "unreachable\nfrom token",
            fillcolor=PLAIN_FILL,
            style="filled,dashed",
            color=UNREACHABLE_BORDER,
        )
        # Keep the key compact and off the main flow.
        for a, b in zip(
            ["lg_entry", "lg_obj", "lg_token", "lg_sink"],
            ["lg_obj", "lg_token", "lg_sink", "lg_unreach"],
        ):
            lg.edge(a, b, style="invis")


def render_reachability_chart(
    reports: dict[str, StructuralReport], out_path: Path
) -> Path:
    """The headline cross-class figure: how far the single token actually
    travels. Two bars per class — tactics reachable from the recon **token**
    seed vs from **any** entry tactic. Where recon is an island the first bar
    collapses to 1 (the seed itself) while the second spans the net: the gap
    between the bars is exactly what the recon→initial-access prefix gap costs.
    Bars speak; no highlights."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    out_path = Path(out_path)
    order = [
        "pure_steal",
        "pure_impediment",
        "double_extortion",
        "infrastructure_setup",
        "aggregate",
    ]
    classes = [c for c in order if c in reports]
    from_token = [len(reports[c].reachable_from_entry_marking) for c in classes]
    from_any = [len(reports[c].reachable_from_any_entry) for c in classes]
    totals = [reports[c].n_places for c in classes]
    bridged = [reports[c].prefix_gap.recon_reaches_initial_access for c in classes]

    y = np.arange(len(classes))
    h = 0.38
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.barh(y + h / 2, from_token, height=h, color="#6aa84f", label="from the recon token seed")
    ax.barh(y - h / 2, from_any, height=h, color="#c9c9c9", label="from any entry tactic")

    for i in range(len(classes)):
        ax.text(from_token[i] + 0.15, y[i] + h / 2, f"{from_token[i]} / {totals[i]}",
                va="center", fontsize=9)
        ax.text(from_any[i] + 0.15, y[i] - h / 2, f"{from_any[i]} / {totals[i]}",
                va="center", fontsize=9, color="#555555")

    ax.set_yticks(y)
    ax.set_yticklabels(
        [
            f"{c}\n({'recon→IA bridged' if bridged[i] else 'recon→IA island'})"
            for i, c in enumerate(classes)
        ]
    )
    ax.set_xlabel("number of ATT&CK tactics reachable (single moving token)")
    ax.set_xlim(0, max(totals) + 2)
    ax.set_title(
        "Reachability of the single token — the recon→initial-access prefix gap's "
        "cost per profile (four GASP classes + aggregate)",
        fontsize=12,
    )
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2,
              fontsize=9, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


__all__ = [
    "load_tactic_layers",
    "render_reachability_chart",
    "render_tactic_state_diagram",
]
