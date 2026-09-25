#!/usr/bin/env python3
"""Dissertation figure: the section 4.1 zoom --- how the attack flows are
combined into the attack graph (the first arrow of fig:pipeline, "combine").

The reader leaves with two things and nothing else:

  T1  an attack flow is one incident's steps, drawn by an analyst as ATT&CK
      techniques; the flows are combined into one graph whose nodes are
      ATT&CK tactics and whose edges carry the number of flows that drew them;
  T2  the combination is at tactic level because technique edges rarely
      recur across incidents, while the same flows mapped to tactics share
      edges.

Three bands over ONE tactic axis (kill-chain order, named once at the top,
a tick from each name down to its column):

  (a) two real attack flows at technique level, one card each (Figure 4.1's
      attack-flow symbol), technique boxes in their tactic columns;
  (b) the same two flows, each technique mapped to its tactic and combined:
      one node per tactic;
  (c) the attack graph itself, all 38 flows, as ONE tactic-by-tactic grid whose
      columns ARE the tactic axis (so the names at the top name them too); rows
      are the tactic an edge leaves, columns the tactic it reaches; a cell's
      grey is the number of attack flows that drew the edge, in the four-grey
      scale and cell style of the section 4.2 figure
      (tools/ch4_attack_profiles_figure.py), whose tactic_edges(), BINS and
      shade() are imported, so both figures count the attack graph one way.
      (Marc 2026-09-25 replaced the "shown in the next figure" box with the
      graph; arcs for all 38 flows had read as texture.) The §4.2 generator
      exposes no one-grid drawing function yet, so the cell drawing below
      duplicates its style: seam 1.2 px, chrome grid, faint frame, diagonal
      white.

Words on the figure, ~5 items (Marc 2026-09-25: too many words): two band
names, two process arrows, one evidence line, "shared" on the two blue edges,
the grid's title, its key and from/to. The caption carries the rest.

One edge rule in (a) and (b): an edge is a light grey line; the edges both
flows draw are the one accent, heavy, so they stand out and the rest recede ---
in (a) the different technique edges beneath them, in (b) the shared tactic
edges (labelled "shared"), in (c) their two cells outlined. Arcs in (b): above
the nodes left to right, below right to left, the arrowhead on the arc,
staggered clear of the others. Same-tactic pairs are not edges of the attack
graph (the section 4.2 figure and the Petri nets drop them), so (b) and (c)
draw none; a technique edge inside one tactic in (a) has no tactic edge.

The pair rule (T2's example, chosen by rule, never by name): among flows whose
techniques are all joined into one connected drawing and that have at most
MAX_TECHNIQUES techniques, the pair that shares NO technique edge (true
of most pairs; the rate is printed) and shares the most tactic edges,
fewest techniques on ties.

Edge weight is the number of DISTINCT flows that drew a technique edge
mapping to the tactic pair --- the count the Petri-net weights use
(src/mtdsim/l3_simulation/petri/weights.py), not the summed observation count
the appendix tactic figure prints (tools/gap_appendix_figures.build_tactic).

Every count is read from the artefacts (data/gap/gap_v0.5.json; the pinned
ATT&CK axis via tools/_tactic_axis.py) and printed; drift guards fail the
build. House style as tools/ch4_overview_figure.py: SVG at 900 px printed to
\\textwidth through Chromium, the type-floor check (technique IDs at 14.5 px,
7.97 pt nominal, the floor size the section 4.2 figure also uses).

Usage:
  PYTHONPATH=src python tools/ch4_attack_graph_figure.py
      [--out-dir DIR] [--stem STEM] [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import itertools
import math
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from _tactic_axis import load_axis  # noqa: E402
from ch4_attack_profiles_figure import BINS, shade, tactic_edges  # noqa: E402  the section 4.2 grid's rule and greys
from pipeline_ladder_figure import flow_graphs, layout_columns, load_gap  # noqa: E402

OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-1a_attack_graph_construction"
WIDTH_CM = 16.058          # \textwidth, measured (455.244 pt)
PX = 900
FACE_SCALE = 0.92
FLOOR_PT = 7.95

MAX_TECHNIQUES = 10        # per flow, for the example pair
MIN_SHARED_TACTIC = 2      # the example must show a shared tactic edge or two

INK, INK2, FAINT, CHROME, ACCENT = "#333", "#6e6e6e", "#b0b0b0", "#ececec", "#1f548c"
EDGE, EDGE_W = "#c4c4c4", 1.2          # every edge: light, so the shared ones stand out
HOT_W = 3.0                            # the shared edges, in the accent

# geometry (px at 900 wide): the grid's columns fix the tactic axis
GUT_R = 176                # right edge of the gutter (band names, grid row names)
GX0, GX1 = 180, 884        # the grid, and so the tactic columns
NT = 15
CW = (GX1 - GX0) / NT      # column pitch
X0, X1 = GX0 + CW / 2, GX1 - CW / 2
ROW_H = 19                 # a grid row
BOX_W, BOX_H, STACK = 44, 22, 32
R = 8                      # tactic node radius

STYLE = f"""
  html, body {{ margin:0; background:#fff; }}
  svg {{ display:block; font-family: "Nimbus Sans", "TeX Gyre Heros", Helvetica, Arial, sans-serif; }}
  text {{ fill:{INK}; }}
  .title {{ font-size:19px; font-weight:bold; }}
  .lbl   {{ font-size:17px; }}
  .sm    {{ font-size:15.5px; fill:{INK2}; }}
  .tick  {{ font-size:15.5px; }}
  .verb  {{ font-size:17px; }}
  .tid   {{ font-size:14.5px; }}
  .acc   {{ fill:{ACCENT}; }}
  .card  {{ fill:#fff; stroke:{FAINT}; stroke-width:1.3; }}
  .tech  {{ fill:#fff; stroke:{INK}; stroke-width:1.4; }}
  .tac   {{ fill:#fff; stroke:{INK}; stroke-width:1.6; }}
  .guide {{ stroke:{CHROME}; stroke-width:1.2; }}
  .becomes {{ stroke:{INK}; stroke-width:1.8; fill:none; }}
  .halo  {{ paint-order:stroke; stroke:#fff; stroke-width:5px; stroke-linejoin:round; }}
"""
SIZES = {"title": 19, "lbl": 17, "sm": 15.5, "tick": 15.5, "verb": 17, "tid": 14.5}


# ------------------------------------------------------------------ the data --
def connected(f, tech, edges) -> bool:
    """Every technique of the flow joined into one drawing (weakly connected)."""
    adj: dict[str, set[str]] = defaultdict(set)
    for s, d in edges[f]:
        adj[s].add(d)
        adj[d].add(s)
    if set(adj) != tech[f]:
        return False
    seen, todo = set(), [next(iter(tech[f]))]
    while todo:
        x = todo.pop()
        if x not in seen:
            seen.add(x)
            todo.extend(adj[x])
    return seen == tech[f]


def tactic_pairs(f, edges, tac_of) -> set[tuple[str, str]]:
    """The attack-graph edges one flow draws (same-tactic pairs are not edges)."""
    return {(tac_of[s], tac_of[d]) for s, d in edges[f] if tac_of[s] != tac_of[d]}


def pick_pair(tech, edges, tac_of):
    cands = sorted(f for f in tech if len(tech[f]) <= MAX_TECHNIQUES and connected(f, tech, edges))
    best = None
    for a, b in itertools.combinations(cands, 2):
        if set(edges[a]) & set(edges[b]):
            continue
        sh = tactic_pairs(a, edges, tac_of) & tactic_pairs(b, edges, tac_of)
        key = (len(sh), -(len(tech[a]) + len(tech[b])), a, b)
        if best is None or key > best[0]:
            best = (key, a, b)
    if best is None or best[0][0] < MIN_SHARED_TACTIC:
        raise SystemExit("pair rule found no two flows: relax MAX_TECHNIQUES / MIN_SHARED_TACTIC")
    _, a, b = best
    return a, b, tactic_pairs(a, edges, tac_of) & tactic_pairs(b, edges, tac_of)


# ---------------------------------------------------------------- the drawing --
class Layer:
    """Drawing ops in band-local coordinates, with their vertical extent."""

    def __init__(self):
        self.parts: list[str] = []
        self.ymin, self.ymax = math.inf, -math.inf
        self.sizes: list[float] = []

    def see(self, *ys):
        self.ymin = min(self.ymin, *ys)
        self.ymax = max(self.ymax, *ys)

    def add(self, s, *ys):
        self.parts.append(s)
        if ys:
            self.see(*ys)

    def text(self, x, y, s, cls="lbl", anchor="middle", extra="", track=True):
        size = SIZES[cls.split()[0]]
        self.sizes.append(size)
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.parts.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}{extra}>{s}</text>')
        if track:
            self.see(y - size * 0.8, y + size * 0.25)


class Markers:
    """One arrowhead per (colour, size), centred on the point it sits on (the
    heads ride at each arc's midpoint, so they never pile up at a node). Heads
    are in user space, so they do not grow with the line (the P20 finding on
    Figure 4.1)."""

    def __init__(self):
        self.defs: dict[tuple[str, int], str] = {}

    def __call__(self, colour: str, size: float) -> str:
        k = (colour, int(round(size)))
        if k not in self.defs:
            mid = f"m{len(self.defs)}"
            self.defs[k] = (f'<marker id="{mid}" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" '
                            f'markerWidth="{k[1]}" markerHeight="{k[1]}" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{colour}"/></marker>')
        return self.defs[k].split('"')[1]


def point_at(pts, frac):
    """The point a fraction of the way along the polyline, and its direction."""
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    goal, run, m = sum(seg) * frac, 0.0, 0
    while m < len(seg) - 1 and run + seg[m] < goal:
        run += seg[m]
        m += 1
    (xa, ya), (xb, yb) = pts[m], pts[m + 1]
    t = (goal - run) / seg[m] if seg[m] else 0
    return (xa + t * (xb - xa), ya + t * (yb - ya)), ((xb - xa) / (seg[m] or 1), (yb - ya) / (seg[m] or 1))


def head_frac(pts, taken, clear=26.0):
    """Where along the arc its head rides: the midpoint, or the nearest
    staggered point clear of heads already placed in the band, so each edge
    can be traced to its own head."""
    for f in (0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.2, 0.8):
        p, _ = point_at(pts, f)
        if all(math.dist(p, q) >= clear for q in taken):
            taken.append(p)
            return f
    taken.append(point_at(pts, 0.5)[0])
    return 0.5


def arc_svg(pts, colour, w, head_id, frac=0.5) -> str:
    """The edge as a polyline, with its arrowhead `frac` of the way along it."""
    d_ = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    (xm, ym), (ux, uy) = point_at(pts, frac)
    return (f'<path d="{d_}" fill="none" stroke="{colour}" stroke-width="{w:.2f}" stroke-linecap="round"/>'
            f'<path d="M{xm - ux:.2f},{ym - uy:.2f} L{xm:.2f},{ym:.2f}" fill="none" stroke="none" marker-end="url(#{head_id})"/>')


def bez(p0, p1, p2, p3, n=48):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


def inside(p, c, pad=2.5):
    return abs(p[0] - c[0]) <= BOX_W / 2 + pad and abs(p[1] - c[1]) <= BOX_H / 2 + pad



def emit(gap, order, axis, tech, edges, fa, fb, shared, W, facts):
    col = {t: X0 + i * CW for i, t in enumerate(order)}
    idx = {t: i for i, t in enumerate(order)}
    tac_of = {tid: n["primary_tactic"] for tid, n in gap["nodes"].items()}
    mk = Markers()
    bands: list[tuple[str, Layer]] = []

    def style(hot):
        return (ACCENT, HOT_W, 12) if hot else (EDGE, EDGE_W, 9)

    # ---- (a) two attack flows, technique level --------------------------------
    def flow_card(f):
        L = Layer()
        # within a column, a technique whose edges mostly run forward (drawn
        # above) sits on top, one whose edges mostly run back (below) at the
        # foot; a blue edge counts ten times, so it keeps the side it has in
        # band (b) (forward above, back below) wherever the stacking allows
        score: dict[str, int] = defaultdict(int)
        for s, d in edges[f]:
            v = (idx[tac_of[d]] > idx[tac_of[s]]) - (idx[tac_of[d]] < idx[tac_of[s]])
            v *= 10 if (tac_of[s], tac_of[d]) in shared else 1
            score[s] += v
            score[d] += v
        pos = layout_columns(sorted(tech[f]), tac_of, col, 0.0, pitch=STACK, key=lambda t: (-score[t], t))
        top = min(py for _, py in pos.values()) - BOX_H / 2
        bot = max(py for _, py in pos.values()) + BOX_H / 2
        colmates: dict[str, list[float]] = defaultdict(list)
        for tid, (_, py) in pos.items():
            colmates[tac_of[tid]].append(py)

        def exposed(tid, side):          # nothing stacked above (side -1) / below (+1) it
            py = pos[tid][1]
            return all((q - py) * side <= 0 for q in colmates[tac_of[tid]])

        paths = []
        heads: list = []
        for s, d in sorted(edges[f], key=lambda e: ((tac_of[e[0]], tac_of[e[1]]) not in shared, e)):
            (x1, y1), (x2, y2) = pos[s], pos[d]
            span = idx[tac_of[d]] - idx[tac_of[s]]
            hot = (tac_of[s], tac_of[d]) in shared
            if span == 0 and abs(y2 - y1) <= STACK + 0.5:     # stacked neighbours: a short drop
                sg = 1 if y2 > y1 else -1
                pts = [(x1, y1 + sg * BOX_H / 2 + sg * 0.5), (x2, y2 - sg * BOX_H / 2 - sg * 0.5)]
            elif span == 0:                  # within the tactic, further apart: a loop to the right
                pts = bez((x1, y1), (x1 + 40, y1), (x2 + 40, y2), (x2, y2))
            else:
                up_ok = exposed(s, -1) and exposed(d, -1)
                dn_ok = exposed(s, 1) and exposed(d, 1)
                up = (span > 0 and up_ok) or (span < 0 and not dn_ok and up_ok) or (not up_ok and not dn_ok and span > 0)
                sg = -1 if up else 1
                h = min(8 + 1.6 * abs(span), 22)
                yc = top - h if up else bot + h
                dx = x2 - x1
                p0, p3 = (x1, y1 + sg * BOX_H / 2), (x2, y2 + sg * BOX_H / 2)
                pts = [p0] + bez(p0, (x1 + 0.15 * dx, yc), (x2 - 0.15 * dx, yc), p3, n=64)[1:]
            if len(pts) > 2:
                pts = [p for p in pts if not any(inside(p, c, pad=0.2) for c in pos.values())]
            if len(pts) < 2:
                continue
            L.see(*(p[1] for p in pts))
            colour, w, hs = style(hot)
            paths.append((hot, arc_svg(pts, colour, w, mk(colour, hs), head_frac(pts, heads))))
        for _, p in sorted(paths, key=lambda t: t[0]):
            L.add(p)
        for tid, (px, py) in pos.items():
            L.add(f'<rect class="tech" x="{px - BOX_W / 2:.1f}" y="{py - BOX_H / 2:.1f}" width="{BOX_W}" height="{BOX_H}" rx="3"/>',
                  py - BOX_H / 2, py + BOX_H / 2)
            L.text(px, py + 5.2, tid, "tid")
        return L

    A = Layer()
    pad = 4
    y = 0.0
    for L in (flow_card(fa), flow_card(fb)):
        dy = y - L.ymin + pad
        A.add(f'<rect class="card" x="{GX0 - 4}" y="{y:.1f}" width="{GX1 - GX0 + 8}" height="{L.ymax - L.ymin + 2 * pad:.1f}" rx="5"/>',
              y, y + L.ymax - L.ymin + 2 * pad)
        A.add(f'<g transform="translate(0,{dy:.1f})">' + "".join(L.parts) + "</g>")
        A.sizes += L.sizes
        y += L.ymax - L.ymin + 2 * pad + 8
    bands.append(("a", A))

    # ---- (b): an arc diagram over tactic nodes -----------------------------------
    def arc_h(span):
        return 2 + 12.5 * math.sqrt(abs(span))     # long spans stay apart, no cap

    trans_b = {k: len(v) for k, v in tactic_edges(gap, {fa, fb}).items()}
    nodes_b = [t for t in order if any(t in k for k in trans_b)]
    B = Layer()
    items = []
    for (s, d), n in trans_b.items():
        hot = (s, d) in shared
        x1, x2 = col[s], col[d]
        span = idx[d] - idx[s]
        up = span > 0
        sgn = -1 if up else 1
        h = arc_h(span)
        xs, xe = (x1 + 3, x2 - 3) if up else (x1 - 3, x2 + 3)
        pts = bez((xs, sgn * R), (xs, sgn * (R + h)), (xe, sgn * (R + h)), (xe, sgn * R))
        B.see(*(p[1] for p in pts))
        items.append((hot, pts))
    heads: list = []
    placed_b = [(hot, pts, head_frac(pts, heads)) for hot, pts in sorted(items, key=lambda t: not t[0])]
    for hot, pts, fr in sorted(placed_b, key=lambda t: t[0]):          # the shared on top
        colour, w, hs = style(hot)
        B.add(arc_svg(pts, colour, w, mk(colour, hs), fr))
    for t in nodes_b:
        B.add(f'<circle class="tac" cx="{col[t]:.1f}" cy="0" r="{R}"/>', -R, R)
    for s, d in sorted(shared, key=lambda k: idx[k[0]]):              # "shared", in place
        span = idx[d] - idx[s]
        ax = (col[s] + col[d]) / 2
        yy = -(R + 0.75 * arc_h(span)) - 9 if span > 0 else R + 0.75 * arc_h(span) + 19
        B.text(ax + 34, yy, "shared", "sm acc halo")
    bands.append(("b", B))

    # ---------------------------------------------------------------- assemble --
    svg: list[str] = []
    sizes: list[float] = []

    def text(x, y, s, cls="lbl", anchor="middle", extra=""):
        sizes.append(SIZES[cls.split()[0]])
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        s = s.replace("&", "&amp;")
        svg.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}{extra}>{s}</text>')

    # the tactic axis, named once, a tick from each name to its column
    ang = 30
    y_ax = 88
    for t in order:
        text(col[t] - 1, y_ax, axis.label[t], "sm", anchor="start",
             extra=f' transform="rotate(-{ang} {col[t] - 1:.1f} {y_ax})"')
        svg.append(f'<line x1="{col[t]:.1f}" y1="{y_ax + 3}" x2="{col[t]:.1f}" y2="{y_ax + 16}" stroke="{INK2}" stroke-width="1.3"/>')
    text(10, y_ax - 16, "ATT&CK", "sm", anchor="start")
    text(10, y_ax + 2, "tactics", "sm", anchor="start")
    y = y_ax + 16
    guide_top = y

    placed = {}
    gaps = {"a": 40, "b": 40}
    for name, L in bands:
        dy = y - L.ymin
        placed[name] = (y, y + L.ymax - L.ymin, dy)
        y = y + L.ymax - L.ymin + gaps[name]
        sizes.extend(L.sizes)

    # ---- (c) the attack graph: one tactic-by-tactic grid --------------------------
    ty = y + 18                                  # its title row
    text(10, ty, f"The attack graph ({facts['n_flows']} attack flows)", "title", anchor="start")
    # its key: the four greys of the section 4.2 figure
    kx = GX1
    sw = 15
    labs = [(lab, c) for _lo, _hi, lab, c in BINS]
    wid = {"1": 26, "2": 26, "3–4": 44, "5 or more": 84}
    for lab, c in reversed(labs):
        kx -= wid.get(lab, 60) + sw + 6
        svg.append(f'<rect x="{kx:.1f}" y="{ty - 12:.1f}" width="{sw}" height="{sw}" fill="{c}"/>')
        text(kx + sw + 5, ty, lab, "tick", anchor="start")
    text(kx - 10, ty, "attack flows that drew the edge:", "sm", anchor="end")
    gy0 = ty + 22
    text(GUT_R - 4, gy0 - 6, "from \u2193", "sm", anchor="end")          # rows: the tactic an edge leaves
    text(GX0 + 4, gy0 - 6, "to \u2192", "sm", anchor="start")            # columns: the tactic it reaches
    for t in order:                               # row names: the tactic an edge leaves
        text(GUT_R, gy0 + (idx[t] + 0.5) * ROW_H + 5.3, axis.label[t], "tick", anchor="end")
    gy1 = gy0 + NT * ROW_H
    for k in range(1, NT):
        svg.append(f'<path d="M{GX0 + k * CW:.2f},{gy0:.2f} V{gy1:.2f} M{GX0:.2f},{gy0 + k * ROW_H:.2f} H{GX1:.2f}" '
                   f'stroke="{CHROME}" stroke-width="1" fill="none"/>')
    g = 1.2                                       # white seam between filled cells (as section 4.2)
    for (r, c), fs in W.items():
        svg.append(f'<rect x="{GX0 + idx[c] * CW + g / 2:.2f}" y="{gy0 + idx[r] * ROW_H + g / 2:.2f}" '
                   f'width="{CW - g:.2f}" height="{ROW_H - g:.2f}" fill="{shade(len(fs))}"/>')
    svg.append(f'<rect x="{GX0}" y="{gy0:.2f}" width="{GX1 - GX0}" height="{gy1 - gy0:.2f}" fill="none" stroke="{FAINT}" stroke-width="1.2"/>')
    for r, c in shared:                           # the two shared edges, where they sit in the graph
        svg.append(f'<rect x="{GX0 + idx[c] * CW - 1:.2f}" y="{gy0 + idx[r] * ROW_H - 1:.2f}" width="{CW + 2:.2f}" height="{ROW_H + 2:.2f}" '
                   f'fill="none" stroke="{ACCENT}" stroke-width="3"/>')
    height = gy1 + 6

    # column guides behind the bands, from the axis to the grid (whose columns they are)
    guides = "".join(f'<line class="guide" x1="{col[t]:.1f}" y1="{guide_top:.1f}" x2="{col[t]:.1f}" y2="{gy0:.1f}"/>' for t in order)
    svg.insert(0, guides)
    for name, L in bands:
        _, _, dy = placed[name]
        svg.append(f'<g transform="translate(0,{dy:.1f})">' + "".join(L.parts) + "</g>")

    # band names in the gutter, and the two processes between the bands
    def band_name(name, lines, sub):
        y0, y1, _ = placed[name]
        yc = (y0 + y1) / 2 - 10 * (len(lines) + len(sub)) + 16
        for k, ln in enumerate(lines):
            text(10, yc + k * 21, ln, "title", anchor="start")
        for k, ln in enumerate(sub):
            text(10, yc + len(lines) * 21 + k * 19, ln, "sm", anchor="start")

    band_name("a", ["Two attack", "flows"], ["techniques"])
    band_name("b", ["Both flows,", "combined"], ["tactics"])

    def process(after, verb, y_end):
        _, y0, _ = placed[after]
        x = 34
        svg.append(f'<path class="becomes" d="M{x},{y0 + 6:.1f} V{y_end - 12:.1f}" marker-end="url(#{mk(INK, 13)})"/>')
        text(x + 16, (y0 + y_end) / 2 + 6, verb, "verb halo", anchor="start")

    process("a", "each technique to its tactic, then combine", placed["a"][1] + gaps["a"])
    process("b", f"add the other {facts['n_flows'] - 2} flows", ty - 18)

    # the one evidence line, by the step it is the reason for
    _, a1, _ = placed["a"]
    text(GX1 + 10, a1 + gaps["a"] / 2 - 3, f"edges drawn by only one of the {facts['n_flows']} flows:", "sm halo", anchor="end")
    text(GX1 + 10, a1 + gaps["a"] / 2 + 15,
         f"{facts['tech_single_pct']}% at technique level, {facts['tac_single_pct']}% at tactic level", "sm halo", anchor="end")

    defs = "<defs>\n" + "\n".join(mk.defs.values()) + "\n</defs>"
    h_cm = WIDTH_CM * height / PX
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>fig:attack-graph-construction --- the section 4.1 zoom (generated by tools/ch4_attack_graph_figure.py; do not hand-edit)</title>
<style>{STYLE}
  body {{ width:{PX}px; }}
  @media print {{ @page {{ size:{WIDTH_CM}cm {h_cm:.3f}cm; margin:0; }} body {{ width:{WIDTH_CM}cm; }} svg {{ width:{WIDTH_CM}cm; height:{h_cm:.3f}cm; }} }}
</style></head>
<body>
<svg id="fig" viewBox="0 0 {PX} {height:.0f}" width="{PX}" height="{height:.0f}" xmlns="http://www.w3.org/2000/svg">
{defs}
{chr(10).join(svg)}
</svg>
</body></html>
"""
    floor = min(sizes) * (WIDTH_CM / 2.54 * 72) / PX / FACE_SCALE
    return html, h_cm, floor, round(height)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR, help="mocks go to the scratchpad, not the thesis")
    ap.add_argument("--stem", default=STEM)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    gap, order = load_gap()
    axis = load_axis()
    axis.check_against(order)
    tech, edges = flow_graphs(gap)
    tac_of = {tid: n["primary_tactic"] for tid, n in gap["nodes"].items()}

    # drift guards: the artefact must say what it says about itself
    if len(tech) != gap["source_flow_count"]:
        raise SystemExit(f"flow count drifted: {len(tech)} flows carry techniques, header says {gap['source_flow_count']}")
    if len(gap["edges"]) != gap["edge_count"]:
        raise SystemExit("edge count drifted from the GAP header")
    bad = [e for e in gap["edges"] if e["observation_count"] != len(set(e["flow_ids"]))]
    if bad:
        raise SystemExit(f"{len(bad)} edges whose observation_count is not their distinct-flow count")
    if set(tac_of.values()) - set(order):
        raise SystemExit("techniques mapped outside the pinned tactic axis")

    W = tactic_edges(gap, set(tech))          # the attack graph, as the section 4.2 figure counts it
    n_tech = len(gap["edges"])
    tech_single = sum(1 for e in gap["edges"] if len(set(e["flow_ids"])) == 1)
    tac_single = sum(1 for v in W.values() if len(v) == 1)
    fa, fb, shared = pick_pair(tech, edges, tac_of)
    # the top card is the flow that starts earlier in the kill chain
    if min(order.index(tac_of[t]) for t in tech[fb]) < min(order.index(tac_of[t]) for t in tech[fa]):
        fa, fb = fb, fa
    flows_with_edges = {f for e in gap["edges"] for f in e["flow_ids"]}
    pairs = list(itertools.combinations(sorted(flows_with_edges), 2))

    def tt(f):
        return tactic_pairs(f, edges, tac_of)
    pair_tech_share = sum(1 for x, y in pairs if set(edges[x]) & set(edges[y])) / len(pairs)
    pair_tac_share = sum(1 for x, y in pairs if tt(x) & tt(y)) / len(pairs)

    facts = {
        "n_flows": len(tech),
        "tech_single_pct": round(100 * tech_single / n_tech),
        "tac_single_pct": round(100 * tac_single / len(W)),
    }
    html, h_cm, floor, h_px = emit(gap, order, axis, tech, edges, fa, fb, shared, W, facts)
    if floor < FLOOR_PT:
        raise SystemExit(f"smallest type prints at {floor:.2f} pt (< {FLOOR_PT} pt floor)")

    a.out_dir.mkdir(parents=True, exist_ok=True)
    html_path = a.out_dir / f"{a.stem}.html"
    html_path.write_text(html)
    print(f"wrote {html_path}")
    if not a.no_pdf or a.png:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={"width": PX, "height": h_px}, device_scale_factor=2)
            pg.goto(html_path.as_uri())
            pg.wait_for_timeout(300)
            if a.png:
                pg.locator("#fig").screenshot(path=str(a.out_dir / f"{a.stem}.png"))
                print(f"preview {a.out_dir / (a.stem + '.png')}")
            if not a.no_pdf:
                pg.emulate_media(media="print")
                pg.pdf(path=str(a.out_dir / f"{a.stem}.pdf"), width=f"{WIDTH_CM}cm", height=f"{h_cm:.3f}cm",
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                       print_background=True, prefer_css_page_size=False)
                print(f"wrote {a.out_dir / (a.stem + '.pdf')}")
            b.close()

    pw_ = tactic_edges(gap, {fa, fb})
    print("--- facts (read from the artefacts; the caption and prose may quote them) ---")
    print(f"ATT&CK axis                  : v{axis.version}, {len(order)} tactics")
    print(f"corpus                       : {len(tech)} attack flows ({len(flows_with_edges)} draw at least one edge; "
          f"{sorted(set(tech) - flows_with_edges)} draw none)")
    print(f"technique level              : {n_tech} edges, {tech_single} drawn by one flow only "
          f"({100 * tech_single / n_tech:.1f}%)")
    print(f"tactic level (the graph)     : {len(W)} edges (same-tactic pairs are not edges; "
          f"{sum(1 for e in gap['edges'] if tac_of[e['source_id']] == tac_of[e['target_id']])} technique edges fall inside one tactic), "
          f"{tac_single} drawn by one flow only ({100 * tac_single / len(W):.1f}%); heaviest {max(len(v) for v in W.values())} flows")
    print(f"flow pairs sharing any       : technique edge {100 * pair_tech_share:.1f}%, "
          f"tactic edge {100 * pair_tac_share:.1f}% (of {len(pairs)} pairs of flows that draw edges)")
    for lab, f in (("flow A (top card)", fa), ("flow B", fb)):
        print(f"{lab:<29}: {f}  ({len(tech[f])} techniques, {len(edges[f])} technique edges, "
              f"{len(tt(f))} tactic edges)")
    print(f"shared by the pair           : {len(set(edges[fa]) & set(edges[fb]))} technique edges, "
          f"{len(shared)} tactic edges {sorted(shared)}; shared techniques {sorted(tech[fa] & tech[fb])}")
    print(f"band (b)                     : {len(pw_)} tactic edges; shared ones' weight in the attack graph: "
          f"{[(k, len(W[k])) for k in sorted(shared)]}")
    print(f"size / type                  : {WIDTH_CM} x {h_cm:.2f} cm; smallest type {floor:.2f} pt nominal")


if __name__ == "__main__":
    main()
