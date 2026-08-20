#!/usr/bin/env python3
"""Appendix figures: the generalised attack graph (L1) at both resolutions.

Four appendix figures, laid out here and drawn in TikZ, so the graphs are
typeset in the document's own font at the document's own sizes rather than
screenshotted out of a tool (figure_table_conventions.md §g):

  gap_flow_exemplar    one incident as the analyst drew it --- actions,
                       AND/OR operators, conditions: the L0 input;
  gap_technique_graph  the technique-level aggregate over every flow, every
                       edge --- the resolution we discontinued, where the
                       density is itself the finding;
  gap_technique_core   the same aggregate above a declared observation
                       threshold, where the recurring structure resolves;
  gap_tactic_graph     the tactic-level aggregate above a declared weight
                       threshold --- the L1 attack graph the pipeline uses.

Placement is ours and deterministic: techniques are banded into their tactic
in kill-chain order and packed across the band, tactic states are laid out in
kill-chain reading order. Graphviz is used only to route the edges around the
boxes we have already placed (`neato -n2`), because dot's own ranking reserves
a horizontal channel per edge and blows a 478-edge graph out to poster size.
The exemplar flow, a small DAG, does use dot's ranking.

Nothing about the corpus is hard-coded: counts, thresholds and names come from
the tracked artefacts (data/gap/gap_v0.5.json, data/gap/flows/*.yaml), and the
caption-facing numbers are printed to stdout for cross-checking.

Usage:
  python tools/gap_appendix_figures.py [--only STEM ...] [--min-obs N]
      [--min-weight N] [--flow FLOW_ID] [--no-compile]

Style: greys carry structure and edge weight; one accent carries the one thing
each figure is about (entry and objective techniques; backward transitions).
Each figure is packed to fit its appendix page box at full size, so the body
type stays at the thesis's 8pt \\scriptsize --- the tool prints the effective
size of every figure it writes, and packing, never type, is what gives way.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
GAP_JSON = REPO / "data" / "gap" / "gap_v0.5.json"
FLOWS_DIR = REPO / "data" / "gap" / "flows"
OUT_DIR = REPO / "docs" / "thesis" / "figures"

# ATT&CK v19.1 display names for the tactic ids the GAP carries (sentence case
# for the figure; ATT&CK's own US spelling inside the proper names, per the
# 2026-08-20 Australianisation ruling --- conventions §i).
TACTIC_LABEL = {
    "reconnaissance": "Reconnaissance",
    "resource-development": "Resource development",
    "initial-access": "Initial access",
    "execution": "Execution",
    "persistence": "Persistence",
    "privilege-escalation": "Privilege escalation",
    "stealth": "Stealth",
    "defense-impairment": "Defense impairment",
    "credential-access": "Credential access",
    "discovery": "Discovery",
    "lateral-movement": "Lateral movement",
    "collection": "Collection",
    "command-and-control": "Command and control",
    "exfiltration": "Exfiltration",
    "impact": "Impact",
}

# --- type and page boxes ---------------------------------------------------
# The thesis is 12pt, so \scriptsize is 8pt: the floor for any glyph in a float
# (§g). Graphviz is fed the same sizes in Times metrics, which run slightly
# wide of the document's Computer Modern, so boxes come out generous rather
# than tight --- the safe direction.
NODE_PT = 8.0
EDGE_PT = 8.0
BAND_PT = 8.0

# Usable area for a full-page float, in points. Inside lscape's landscape
# environment the typeblock is rotated, so the wide box is the long side of
# the page; the height allowance leaves room for a decoding caption.
CM = 72 / 2.54
LANDSCAPE_BOX = (23.4 * CM, 13.0 * CM)
PORTRAIT_BOX = (15.6 * CM, 21.2 * CM)

ACCENT = "accent"


def esc(s: str) -> str:
    """TeX-escape a name coming from the corpus."""
    out = []
    for ch in s:
        if ch in "&%#_${}":
            out.append("\\" + ch)
        elif ch == "~":
            out.append(r"\textasciitilde{}")
        elif ch == "^":
            out.append(r"\textasciicircum{}")
        elif ch == "\\":
            out.append(r"\textbackslash{}")
        else:
            out.append(ch)
    return "".join(out)


def wrap(text: str, width: int, break_words: bool = True) -> list[str]:
    return textwrap.wrap(text, width=width,
                         break_long_words=break_words) or [""]


def text_wh(lines: list[str], pt: float = NODE_PT) -> tuple[float, float]:
    """Points for a box holding `lines` at `pt`. Times-Roman runs about
    0.52em per character on mixed-case text; the pad keeps the document's
    (narrower) Computer Modern comfortably inside the reserved box."""
    w = max((len(l) for l in lines), default=1) * 0.52 * pt + 7.0
    h = len(lines) * pt * 1.18 + 5.0
    return w, h


# =====================================================================
# Graphviz: build DOT, get the routed layout back as JSON
# =====================================================================

class RoutingError(RuntimeError):
    """Graphviz could not route this candidate layout."""


class Graph:
    """A DOT source builder carrying a side table of TikZ styling.

    Graphviz sees plain labels and (for placed graphs) explicit positions; the
    TikZ styling travels in `nstyle` / `estyle`, keyed by the integer `tk`
    attribute that survives into the JSON layout. `decor` carries anything we
    draw ourselves that the layout engine never sees --- the tactic bands.
    """

    def __init__(self, **graph_attr):
        self.attrs = graph_attr
        self.lines: list[str] = []
        self.nstyle: dict[int, dict] = {}
        self.estyle: dict[int, dict] = {}
        self.decor: list[dict] = []
        self.placed: dict[str, tuple[float, float]] = {}
        self.natural: tuple[float, float] | None = None
        self._n = 0

    @staticmethod
    def _fmt(attrs: dict) -> str:
        return ", ".join('%s="%s"' % (k, v) for k, v in attrs.items())

    def node(self, name: str, lines: list[str], *, style: dict,
             shape: str = "box", **extra) -> None:
        tk = self._n
        self._n += 1
        self.nstyle[tk] = dict(style, lines=lines)
        if "pos" in extra:
            x, y = extra["pos"].split(",")
            self.placed[name] = (float(x), float(y))
        a = dict(label="\\n".join(lines), shape=shape, tk=str(tk), **extra)
        self.lines.append('  "%s" [%s];' % (name, self._fmt(a)))

    def edge(self, src: str, dst: str, *, style: dict, label: str = "",
             **extra) -> None:
        tk = self._n
        self._n += 1
        self.estyle[tk] = dict(style, label=label)
        a = dict(tk=str(tk), **extra)
        if style.get("invis"):
            a["style"] = "invis"
        self.lines.append('  "%s" -> "%s" [%s];' % (src, dst, self._fmt(a)))

    def band(self, x0: float, y0: float, x1: float, y1: float,
             lines: list[str], count: int) -> None:
        self.decor.append({"kind": "band", "box": (x0, y0, x1, y1),
                           "lines": lines, "count": count})

    def loop(self, at: tuple[float, float], top: float, label: str,
             style: dict) -> None:
        """A self-transition, drawn as a small loop over its own state.
        Graphviz routes these off to the right of the node, where they run
        off the page; over the node they read as what they are."""
        self.decor.append({"kind": "loop", "at": at, "top": top,
                           "label": label, "style": style})

    def source(self) -> str:
        head = "digraph G {\n  " + ";\n  ".join(
            '%s="%s"' % kv for kv in self.attrs.items()) + ";"
        return "\n".join([head] + self.lines + ["}"])

    def layout(self, engine: str = "dot", args: tuple = ()) -> dict:
        cmd = [engine, *args, "-Tjson"]
        out = subprocess.run(cmd, input=self.source(), capture_output=True,
                             text=True)
        if out.returncode:
            # Graphviz's spline router aborts on some geometries (a known
            # upstream fault, not bad input). A candidate packing it cannot
            # route is simply not a candidate --- see choose().
            raise RoutingError("%s exited %d: %s"
                               % (engine, out.returncode,
                                  out.stderr.strip()[-300:] or "no message"))
        return json.loads(out.stdout)


def parse_pos(pos: str) -> tuple[list[tuple[float, float]], tuple | None]:
    """A Graphviz spline -> (B-spline points, arrow endpoint)."""
    head = None
    pts: list[tuple[float, float]] = []
    for tok in pos.replace("\\\n", " ").split():
        if tok.startswith("e,"):
            x, y = tok[2:].split(",")
            head = (float(x), float(y))
        elif tok.startswith("s,"):
            continue
        else:
            x, y = tok.split(",")
            pts.append((float(x), float(y)))
    return pts, head


def bezier_mid(pts: list[tuple[float, float]]) -> tuple[float, float]:
    """Midpoint of a cubic B-spline chain, for our own edge labels."""
    segs = max((len(pts) - 1) // 3, 1)
    i = ((segs - 1) // 2) * 3
    p = pts[i:i + 4]
    if len(p) < 4:
        return pts[len(pts) // 2]
    t = 0.5
    b = [(1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t ** 2, t ** 3]
    return (sum(b[k] * p[k][0] for k in range(4)),
            sum(b[k] * p[k][1] for k in range(4)))


# =====================================================================
# TikZ emission
# =====================================================================

PREAMBLE = [
    r"\documentclass[tikz,12pt,border=2pt]{standalone}",
    r"\usepackage[T1]{fontenc}",
    r"\usetikzlibrary{arrows.meta,shapes.geometric}",
    r"\definecolor{accent}{RGB}{31,84,140}",
    r"\definecolor{accentlight}{RGB}{200,214,232}",
    r"\begin{document}",
]


class Canvas:
    """Emits a standalone TikZ picture from a graphviz JSON layout.

    Every coordinate, dimension and font size is multiplied by `s` at emit
    time, so the emitted file states its own true sizes --- no picture-level
    scale, no `transform shape`.
    """

    def __init__(self, layout: dict, box: tuple[float, float],
                 content: tuple[float, float] | None = None):
        x0, y0, x1, y1 = (float(v) for v in layout["bb"].split(","))
        # the routed layout knows nothing of the bands we draw ourselves, so
        # the figure is measured against whichever is larger
        self.w_pt = max(x1 - x0, content[0] if content else 0.0)
        self.h_pt = max(y1 - y0, content[1] if content else 0.0)
        self.s = min(box[0] / self.w_pt, box[1] / self.h_pt, 1.0)
        self.layout = layout
        self.offset = (0.0, 0.0)
        self.body: list[str] = []

    @property
    def nat_cm(self) -> tuple[float, float]:
        return self.w_pt / CM, self.h_pt / CM

    def font(self, pt: float) -> str:
        return r"\fontsize{%.2f}{%.2f}\selectfont" % (pt * self.s,
                                                      pt * self.s * 1.15)

    def xy(self, p) -> str:
        return "(%.2f,%.2f)" % (p[0] * self.s, p[1] * self.s)

    def emit(self, line: str) -> None:
        self.body.append(line)

    # -- drawing ---------------------------------------------------------
    def band(self, d: dict) -> None:
        dx, dy = self.offset
        x0, y0, x1, y1 = ((v + o) * self.s for v, o in
                          zip(d["box"], (dx, dy, dx, dy)))
        self.emit(r"\draw[rounded corners=%.2fpt,draw=black!15,fill=black!4,"
                  r"line width=%.2fpt] (%.2f,%.2f) rectangle (%.2f,%.2f);"
                  % (2.5 * self.s, 0.4 * self.s, x0, y0, x1, y1))
        label = r"\\".join(esc(l) for l in d["lines"])
        if d["count"]:
            label += (r"\\" if len(d["lines"]) > 1 else r"\,\,") \
                + r"{\itshape %d}" % d["count"]
        self.emit(r"\node[anchor=west,text=black!60,align=left,font=%s] "
                  r"at (%.2f,%.2f) {%s};"
                  % (self.font(BAND_PT), x0 + 4.0 * self.s, (y0 + y1) / 2, label))

    def loop(self, d: dict) -> None:
        dx, dy = self.offset
        x, y = d["at"][0] + dx, d["top"] + dy
        st = d["style"]
        opts = ["draw=%s" % st.get("colour", "black!40"),
                "line width=%.2fpt" % (st.get("lw", 0.4) * self.s),
                "-{Stealth[length=%.2fpt,width=%.2fpt]}"
                % (3.2 * self.s, 2.0 * self.s)]
        if st.get("dash"):
            opts.append("dash pattern=on %.2fpt off %.2fpt"
                        % (1.7 * self.s, 1.3 * self.s))
        r, h = 9.0 * self.s, 17.0 * self.s
        cx, cy = x * self.s, y * self.s
        self.emit(r"\draw[%s] (%.2f,%.2f) .. controls (%.2f,%.2f) and "
                  r"(%.2f,%.2f) .. (%.2f,%.2f);"
                  % (",".join(opts), cx - r, cy, cx - r * 1.6, cy + h,
                     cx + r * 1.6, cy + h, cx + r, cy))
        if d["label"]:                       # centred over the loop's apex
            self.edge_label((x, y + h / self.s * 0.80 + 3.0),
                            d["label"], st.get("lcolour", "black!70"))

    def node(self, pos: str, w_pt: float, h_pt: float, st: dict) -> None:
        x, y = (float(v) for v in pos.split(","))
        shape = {"box": "rectangle", "rounded": "rectangle",
                 "ellipse": "ellipse", "diamond": "diamond"}[st.get("shape", "box")]
        opts = ["draw=%s" % st.get("draw", "black!55"),
                "fill=%s" % st.get("fill", "white"),
                "line width=%.2fpt" % (st.get("lw", 0.5) * self.s),
                "minimum width=%.2fpt" % (w_pt * self.s),
                "minimum height=%.2fpt" % (h_pt * self.s),
                "inner sep=0pt", "align=center",
                "font=%s" % self.font(st.get("pt", NODE_PT)),
                "text=%s" % st.get("text", "black"), shape]
        if st.get("shape") == "rounded":
            opts.append("rounded corners=%.2fpt" % (2.0 * self.s))
        if st.get("shape") == "diamond":
            opts.append("aspect=1.7")
        lines = [esc(l) for l in st["lines"]]
        if st.get("dim_last") and len(lines) > 1:
            lines[-1] = r"{\color{black!60}%s}" % lines[-1]
        label = r"\\".join(lines)
        self.emit(r"\node[%s] at (%.2f,%.2f) {%s};"
                  % (",".join(opts), x * self.s, y * self.s, label))

    def spline(self, pos: str, st: dict) -> None:
        pts, head = parse_pos(pos)
        if not pts:
            return
        opts = ["draw=%s" % st.get("colour", "black!40"),
                "line width=%.2fpt" % (st.get("lw", 0.4) * self.s)]
        if st.get("dash"):
            opts.append("dash pattern=on %.2fpt off %.2fpt"
                        % (1.7 * self.s, 1.3 * self.s))
        if head:
            opts.append("-{Stealth[length=%.2fpt,width=%.2fpt]}"
                        % (3.2 * self.s, 2.0 * self.s))
        path = self.xy(pts[0])
        for i in range(1, len(pts) - 2, 3):
            path += " .. controls %s and %s .. %s" % (
                self.xy(pts[i]), self.xy(pts[i + 1]), self.xy(pts[i + 2]))
        if head:
            path += " -- %s" % self.xy(head)
        self.emit(r"\draw[%s] %s;" % (",".join(opts), path))

    def edge_label(self, at: tuple[float, float], text: str, colour: str) -> None:
        self.emit(r"\node[fill=white,fill opacity=0.9,text opacity=1,"
                  r"inner sep=%.2fpt,font=%s,text=%s] at (%.2f,%.2f) {%s};"
                  % (0.8 * self.s, self.font(EDGE_PT), colour,
                     at[0] * self.s, at[1] * self.s, esc(text)))

    # -- assembly --------------------------------------------------------
    def render(self, g: Graph) -> str:
        # Graphviz translates the drawing to the origin, so anything we place
        # ourselves has to be moved onto the routed layout by the same vector.
        self.offset = (0.0, 0.0)
        for o in self.layout.get("objects", []):
            if "pos" in o and o.get("name") in g.placed:
                lx, ly = (float(v) for v in o["pos"].split(","))
                px, py = g.placed[o["name"]]
                self.offset = (lx - px, ly - py)
                break
        for d in g.decor:
            if d["kind"] == "band":
                self.band(d)
            else:
                self.loop(d)
        for o in self.layout.get("objects", []):
            if o.get("name", "").startswith("cluster") and "bb" in o:
                x0, y0, x1, y1 = (float(v) for v in o["bb"].split(","))
                self.band({"box": (x0, y0, x1, y1),
                           "lines": [o.get("label", "")], "count": 0})
        edges = [e for e in self.layout.get("edges", []) if "pos" in e]
        edges.sort(key=lambda e: g.estyle.get(int(e.get("tk", -1)), {}).get("z", 0))
        drawn = [e for e in edges
                 if not g.estyle.get(int(e.get("tk", -1)), {}).get("invis")]
        for e in drawn:
            self.spline(e["pos"], g.estyle[int(e["tk"])])
        for e in drawn:                       # labels ride on top of the lines
            st = g.estyle[int(e["tk"])]
            if not st.get("label"):
                continue
            pts, _ = parse_pos(e["pos"])
            self.edge_label(bezier_mid(pts), st["label"],
                            st.get("lcolour", "black!70"))
        for o in self.layout.get("objects", []):
            if "pos" not in o or "tk" not in o:
                continue
            self.node(o["pos"], float(o["width"]) * 72, float(o["height"]) * 72,
                      g.nstyle[int(o["tk"])])
        return "\n".join(PREAMBLE
                         + [r"\begin{tikzpicture}[x=1pt,y=1pt]"]
                         + self.body
                         + [r"\end{tikzpicture}", r"\end{document}"])


# =====================================================================
# Shared encodings and data
# =====================================================================

def ramp(value: int, vmax: int, backward: bool) -> dict:
    """Edge weight -> grey (forward) or accent (backward), plus line width.

    One sequential ramp per direction: the recurring core reads dark and
    heavy, the single-incident tail fades to a hairline.
    """
    frac = (value - 1) / max(vmax - 1, 1)
    lw = 0.25 + frac * 1.45
    if backward:
        return {"colour": "%s!%d" % (ACCENT, int(32 + frac * 68)), "lw": lw,
                "z": value, "lcolour": ACCENT}
    return {"colour": "black!%d" % int(13 + frac * 72), "lw": lw,
            "z": value, "lcolour": "black!70"}


def load_gap() -> dict:
    return json.loads(GAP_JSON.read_text())


def tactic_order(gap: dict) -> list[str]:
    layer = {n["primary_tactic"]: n["tactic_layer"] for n in gap["nodes"].values()}
    return sorted(layer, key=lambda t: (layer[t] == -1, layer[t]))


def _rows(items: list, per_row: int) -> list[list]:
    return [items[i:i + per_row] for i in range(0, len(items), per_row)]


# =====================================================================
# Placement (ours; graphviz only routes)
# =====================================================================

GAP_X, GAP_Y, BAND_PAD, BAND_GAP = 4.0, 4.0, 2.5, 3.0


def pack_bands(order: list[str], members: dict[str, list],
               labels: dict[str, list[str]], width_of: dict, item_h: float,
               avail_w: float, label_w: float
               ) -> tuple[dict, list[tuple], tuple[float, float]]:
    """Tactic bands top to bottom in kill-chain order; members packed across
    the band, greedily, to the width the page allows. Chips keep their own
    widths, so a band of short identifiers packs tight and a band of long
    names simply takes another row. Returns positions (points, y up), band
    rectangles and the overall size."""
    down = 0.0
    pos: dict = {}
    bands: list[tuple] = []
    for t in order:
        rows: list[list] = [[]]
        used = 0.0
        for item in members[t]:
            w = width_of[item]
            if rows[-1] and used + GAP_X + w > avail_w:
                rows.append([])
                used = 0.0
            rows[-1].append(item)
            used += w + (GAP_X if len(rows[-1]) > 1 else 0)
        band_h = max(len(rows) * item_h + (len(rows) - 1) * GAP_Y,
                     len(labels[t]) * BAND_PT * 1.18) + 2 * BAND_PAD
        rows_h = len(rows) * item_h + (len(rows) - 1) * GAP_Y
        top = down + (band_h - rows_h) / 2
        for r, row in enumerate(rows):
            x = label_w
            for item in row:
                pos[item] = (x + width_of[item] / 2,
                             top + r * (item_h + GAP_Y) + item_h / 2)
                x += width_of[item] + GAP_X
        bands.append((0.0, down, label_w + avail_w, down + band_h,
                      labels[t], len(members[t])))
        down += band_h + BAND_GAP
    total_h = down - BAND_GAP
    pos = {k: (x, total_h - y) for k, (x, y) in pos.items()}
    bands = [(x0, total_h - y1, x1, total_h - y0, lab, n)
             for (x0, y0, x1, y1, lab, n) in bands]
    return pos, bands, (label_w + avail_w, total_h)


def grid(items: list, chip: tuple[float, float], per_row: int,
         gx: float, gy: float) -> tuple[dict, tuple[float, float]]:
    """Reading-order grid: left to right, wrapping downwards."""
    cw, ch = chip
    rows = _rows(items, per_row)
    width = per_row * cw + (per_row - 1) * gx
    height = len(rows) * ch + (len(rows) - 1) * gy
    pos = {}
    for r, row in enumerate(rows):
        # centre a short last row under the block
        offset = (width - (len(row) * cw + (len(row) - 1) * gx)) / 2
        for c, item in enumerate(row):
            pos[item] = (offset + c * (cw + gx) + cw / 2,
                         height - (r * (ch + gy) + ch / 2))
    return pos, (width, height)


# =====================================================================
# Figure builders
# =====================================================================

def build_technique(gap: dict, min_obs: int, mode: str,
                    box: tuple[float, float]) -> tuple[Graph, dict]:
    """Technique-level aggregate: techniques banded into their tactic in
    kill-chain order, edge weight = the number of incidents that drew the
    edge. `mode` is "id" (identifiers only --- the full view, where 124 boxes
    have to fit) or "inline" (identifier and name on one line)."""
    nodes = gap["nodes"]
    edges = [e for e in gap["edges"] if e["observation_count"] >= min_obs]
    if min_obs > 1:
        keep = {e["source_id"] for e in edges} | {e["target_id"] for e in edges}
        keep = _big_components(keep, edges, floor=3)
        edges = [e for e in edges
                 if e["source_id"] in keep and e["target_id"] in keep]
    else:
        keep = set(nodes)

    by_tac: dict[str, list[str]] = defaultdict(list)
    for tid in sorted(keep):
        by_tac[nodes[tid]["primary_tactic"]].append(tid)
    order = [t for t in tactic_order(gap) if t in by_tac]

    if mode == "id":
        label_of = {tid: [tid] for tid in keep}
    else:
        label_of = {tid: ["%s  %s" % (tid, nodes[tid]["name"])] for tid in keep}
    width_of = {tid: text_wh(label_of[tid])[0] for tid in keep}
    item_h = text_wh(["x"])[1]
    band_lines = {t: [TACTIC_LABEL.get(t, t)] for t in order}
    label_w = max(text_wh(['%s  %d' % (band_lines[t][0], len(by_tac[t]))],
                          BAND_PT)[0] for t in order) + 2.5
    pos, bands, size = pack_bands(order, by_tac, band_lines, width_of, item_h,
                                  box[0] - label_w, label_w)

    g = Graph(splines="true", bgcolor="white", fontname="Times-Roman",
              fontsize=str(NODE_PT))
    for tid in sorted(keep):
        n = nodes[tid]
        st = {"lines": label_of[tid], "shape": "rounded", "pt": NODE_PT}
        if n["is_entry"]:
            st["fill"] = "accentlight"
        if n["is_objective"]:
            st.update(draw=ACCENT, lw=1.0)
        g.node(tid, label_of[tid], style=st, shape="box", fixedsize="true",
               pos="%.2f,%.2f" % pos[tid], width="%.4f" % (width_of[tid] / 72),
               height="%.4f" % (item_h / 72), fontname="Times-Roman",
               fontsize=str(NODE_PT))
    for x0, y0, x1, y1, lab, n in bands:
        g.band(x0, y0, x1, y1, lab, n)
    g.natural = size

    vmax = max((e["observation_count"] for e in edges), default=1)
    for e in edges:
        obs = e["observation_count"]
        st = ramp(obs, vmax, e.get("tactic_delta") == "backward")
        g.edge(e["source_id"], e["target_id"], style=st,
               label=str(obs) if (min_obs > 1 and obs > min_obs) else "",
               arrowsize="0.45")

    facts = {"techniques": len(keep), "edges": len(edges), "tactics": len(order),
             "max_obs": vmax, "placed_cm": "%.1fx%.1f" % (size[0] / CM, size[1] / CM),
             "entries": sum(1 for t in keep if nodes[t]["is_entry"]),
             "objectives": sum(1 for t in keep if nodes[t]["is_objective"]),
             "backward": sum(1 for e in edges
                             if e.get("tactic_delta") == "backward"),
             "once_only": sum(1 for e in edges if e["observation_count"] == 1)}
    return g, facts


def _big_components(keep: set, edges: list, floor: int) -> set:
    adj: dict[str, set] = {n: set() for n in keep}
    for e in edges:
        s, t = e["source_id"], e["target_id"]
        if s in adj and t in adj:
            adj[s].add(t)
            adj[t].add(s)
    seen, big = set(), set()
    for start in keep:
        if start in seen:
            continue
        stack, comp = [start], []
        seen.add(start)
        while stack:
            cur = stack.pop()
            comp.append(cur)
            for nxt in adj[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        if len(comp) >= floor:
            big.update(comp)
    return big


def build_tactic(gap: dict, min_weight: int, per_row: int) -> tuple[Graph, dict]:
    """Tactic-level aggregate: technique edges rolled up to their tactics and
    weighted by summed observations, states in kill-chain reading order."""
    nodes = gap["nodes"]
    tac = lambda tid: nodes[tid]["primary_tactic"]           # noqa: E731
    layer = {n["primary_tactic"]: n["tactic_layer"] for n in nodes.values()}
    techs: Counter = Counter(n["primary_tactic"] for n in nodes.values())

    weight: Counter = Counter()
    for e in gap["edges"]:
        weight[(tac(e["source_id"]), tac(e["target_id"]))] += e["observation_count"]
    shown = {k: v for k, v in weight.items() if v >= min_weight}
    order = tactic_order(gap)

    label_of = {t: [TACTIC_LABEL.get(t, t), "%d techniques" % techs[t]]
                for t in order}
    w, h = text_wh(["x" * max(len(l) for v in label_of.values() for l in v), "x"])
    chip = (w * 1.38, h * 1.50)              # ellipse needs the extra room
    pos, size = grid(order, chip, per_row, gx=chip[0] * 0.40, gy=chip[1] * 1.75)

    g = Graph(splines="true", bgcolor="white", fontname="Times-Roman",
              fontsize=str(NODE_PT))
    for t in order:
        deg = sum(1 for (s, d) in shown if s == t or d == t)
        st = {"lines": label_of[t], "shape": "ellipse", "pt": NODE_PT}
        if deg == 0:                    # no transition survives the threshold
            st.update(draw="black!30", text="black!55")
        g.node(t, label_of[t], style=st, shape="ellipse", fixedsize="true",
               pos="%.2f,%.2f" % pos[t], width="%.4f" % (chip[0] / 72),
               height="%.4f" % (chip[1] / 72), fontname="Times-Roman",
               fontsize=str(NODE_PT))

    vmax = max(shown.values(), default=1)
    for (s, d), wt in sorted(shown.items(), key=lambda kv: kv[1]):
        forward = layer.get(d, 99) >= layer.get(s, -2)
        st = ramp(wt, vmax, not forward)
        if s == d:                       # drawn over the state, not beside it
            st["dash"] = True
            g.loop(pos[s], pos[s][1] + chip[1] / 2, str(wt), st)
            continue
        g.edge(s, d, style=st, label=str(wt), arrowsize="0.5")

    facts = {"states": len(order), "shown": len(shown), "all": len(weight),
             "max_w": vmax, "threshold": min_weight,
             "size_cm": "%.1fx%.1f" % (size[0] / CM, size[1] / CM),
             "isolated": sum(1 for t in order
                             if not any(s == t or d == t for (s, d) in shown)),
             "backward": sum(1 for (s, d) in shown
                             if layer.get(d, 99) < layer.get(s, -2)),
             "self": sum(1 for (s, d) in shown if s == d)}
    return g, facts


def build_flow(flow_id: str) -> tuple[Graph, dict]:
    """One analyst-drawn Attack Flow: actions, AND/OR operators, conditions.
    Small enough for dot's own ranking, which is what draws the dependency."""
    flow = yaml.safe_load((FLOWS_DIR / f"{flow_id}.yaml").read_text())
    starts = set(flow.get("start_refs", []))
    g = Graph(rankdir="TB", splines="spline", nodesep="0.20", ranksep="0.34",
              bgcolor="white", fontname="Times-Roman", fontsize=str(NODE_PT))
    kinds: Counter = Counter()
    for n in flow["nodes"]:
        kind = n.get("kind", "action")
        kinds[kind] += 1
        if kind == "operator":
            lines = [n.get("operator", "?")]
            g.node(n["id"], lines, shape="diamond",
                   style={"lines": lines, "shape": "diamond"},
                   fontname="Times-Roman", fontsize=str(NODE_PT),
                   margin="0.02,0.01")
        elif kind == "condition":
            lines = wrap(n.get("description", "condition"), 24)
            g.node(n["id"], lines, shape="ellipse",
                   style={"lines": lines, "shape": "ellipse"},
                   fontname="Times-Roman", fontsize=str(NODE_PT),
                   margin="0.10,0.04")
        else:
            tid = n.get("sub_technique_id") or n.get("technique_id", "")
            lines = [tid] + wrap(n.get("name", ""), 24)
            tactic = n.get("tactic")
            if tactic:
                lines.append(TACTIC_LABEL.get(tactic, tactic))
            st = {"lines": lines, "shape": "rounded", "dim_last": bool(tactic)}
            if n["id"] in starts:
                st["fill"] = "accentlight"
            g.node(n["id"], lines, shape="box", style=st,
                   fontname="Times-Roman", fontsize=str(NODE_PT),
                   margin="0.06,0.035")
    for e in flow["edges"]:
        st = {"colour": "black!55", "lw": 0.6, "z": 1}
        if e.get("type") not in (None, "effect"):
            st["dash"] = True
        g.edge(e["source"], e["target"], style=st, arrowsize="0.55")
    facts = {"flow": flow["flow_name"], "scope": flow.get("scope"),
             "nodes": len(flow["nodes"]), "edges": len(flow["edges"]),
             "actions": kinds["action"], "operators": kinds["operator"],
             "conditions": kinds["condition"],
             "tactics": len({n.get("tactic") for n in flow["nodes"]
                             if n.get("tactic")})}
    return g, facts


# =====================================================================
# Driver
# =====================================================================

def choose(builder, candidates: list, box: tuple[float, float],
           engine: str = "neato", args: tuple = ("-n2",)):
    """Lay the figure out at each candidate packing and keep the one that
    fills the page box best. Type size is never traded for fit: the packing
    gives way, the 8pt body does not."""
    best, failed = None, []
    for cand in candidates:
        g, facts = builder(cand)
        try:
            canvas = Canvas(g.layout(engine, args), box, g.natural)
        except RoutingError as exc:
            failed.append("%s (%s)" % (cand, exc))
            continue
        if best is None or canvas.s > best[0].s:
            best = (canvas, g, facts, cand)
    if best is None:
        raise SystemExit("no candidate packing could be routed: "
                         + "; ".join(failed))
    if failed:
        print("     skipped unroutable packing: %s"
              % ", ".join(f.split(" (")[0] for f in failed))
    return best


def write(stem: str, built, compile_pdf: bool) -> None:
    canvas, g, facts, cand = built
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{stem}.tex"
    path.write_text(canvas.render(g) + "\n")
    eff = NODE_PT * canvas.s
    flag = "" if eff >= 7.95 else "   << BELOW THE 8pt FLOOR"
    print(f"  {stem}: {canvas.nat_cm[0]:.1f} x {canvas.nat_cm[1]:.1f} cm"
          f" (pack {cand}) -> scale {canvas.s:.3f}, type {eff:.1f}pt{flag}")
    print("     " + ", ".join(f"{k}={v}" for k, v in facts.items()))
    if compile_pdf:
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode",
                            "-halt-on-error", path.name],
                           cwd=OUT_DIR, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2500:])
            raise SystemExit(f"pdflatex failed on {stem}")
        for ext in (".aux", ".log"):
            (OUT_DIR / f"{stem}{ext}").unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", default=None, metavar="STEM")
    ap.add_argument("--min-obs", type=int, default=2, metavar="N",
                    help="observation threshold for the technique core view")
    ap.add_argument("--min-weight", type=int, default=4, metavar="N",
                    help="weight threshold for the tactic view")
    ap.add_argument("--flow", default="cisa_aa22_138b_vmware_workspace_ta1")
    ap.add_argument("--full-names", action="store_true",
                    help="draw technique names in the full technique graph "
                         "(default: identifiers only, so the glyphs stay at 8pt)")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    want = (lambda s: args.only is None or s in args.only)
    compile_pdf = not args.no_compile
    gap = load_gap()
    print(f"GAP {gap['version']}: {gap['node_count']} techniques / "
          f"{gap['edge_count']} edges over {gap['source_flow_count']} flows")

    if want("gap_flow_exemplar"):
        g, facts = build_flow(args.flow)
        canvas = Canvas(g.layout("dot"), PORTRAIT_BOX, g.natural)
        write("gap_flow_exemplar", (canvas, g, facts, "dot"), compile_pdf)
    if want("gap_technique_graph"):
        write("gap_technique_graph",
              choose(lambda m: build_technique(gap, 1, m, LANDSCAPE_BOX),
                     ["inline", "id"] if args.full_names else ["id"],
                     LANDSCAPE_BOX), compile_pdf)
    if want("gap_technique_core"):
        write("gap_technique_core",
              choose(lambda m: build_technique(gap, args.min_obs, m,
                                               LANDSCAPE_BOX),
                     ["inline"], LANDSCAPE_BOX), compile_pdf)
    if want("gap_tactic_graph"):
        write("gap_tactic_graph",
              choose(lambda pr: build_tactic(gap, args.min_weight, pr),
                     [3, 4, 5, 6], LANDSCAPE_BOX), compile_pdf)


if __name__ == "__main__":
    main()
