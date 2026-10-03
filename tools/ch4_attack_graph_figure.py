#!/usr/bin/env python3
"""Dissertation figure: the section 4.1 zoom --- how the attack flows are
aggregated into the attack graph (the first arrow of fig:pipeline, "aggregate").

REBUILT 2026-10-03 (Marc: the previous three-band figure, with a second,
38-flow attack graph drawn as a 15 x 15 grid, was "written off as confusing";
the full attack graph lives in Appendix B). The figure is one worked example,
at the abstraction of Figures 2.1--2.3 and 4.1.

What the reader leaves with (section 4.1's points, nothing else):

  T1  each technique in an attack flow stands for its tactic (the technique
      boxes sit in their tactic's column, under the tactic's name);
  T2  a step between two techniques of the same tactic is not an edge (one
      such step inside the Collection band, and nothing for it once the band
      narrows to its one tactic box; the dash that marked it was CUT
      2026-10-03 --- Marc: a pattern the caption must decode is not intuitive);
  T3  aggregating counts: two attack flows that step from collection to
      stealth through different techniques give that edge weight 2;
  (T4, the 88 %/39 % bars, CUT 2026-10-03, Marc: section 4.1's prose already
      says it; the example's two technique edges becoming one tactic edge is
      the picture of it. The facts are still printed below.)

Two encodings, each read without a key (Marc 2026-10-03): line WIDTH is the
edge weight in every row (an edge one attack flow draws is thin, the edge two
draw is twice as thick); the one colour, blue, is the edge both attack flows
draw --- the two thin technique steps and the one thick tactic edge they
become. Each tactic's band narrows by an arrow to its one tactic box: that is
the aggregation. Everything else is ink or grey.

The example is chosen by rule, never by name:
  * the pair --- among attack flows whose techniques form one connected
    drawing and number at most MAX_TECHNIQUES, the pair that shares no
    technique edge and shares the most tactic edges (fewest techniques on
    ties);
  * the excerpt --- the first shared tactic edge (p, q), in ATT&CK matrix
    order, for which one attack flow of the pair has a same-tactic step into
    its technique of p and a step on from its technique of q to a third
    tactic. That attack flow shows those three steps; the other shows its one
    step from p to q.

Every count is read from the artefacts (data/gap/gap_v0.5.json; the pinned
ATT&CK axis via tools/_tactic_axis.py) and printed; drift guards fail the
build. House style as tools/ch4_overview_figure.py: SVG at 900 px printed to
\\textwidth through Chromium, with the type-floor check.

Usage:
  PYTHONPATH=src python tools/ch4_attack_graph_figure.py
      [--out-dir DIR] [--stem STEM] [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import itertools
import sys
import textwrap
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from _tactic_axis import load_axis  # noqa: E402
from ch4_attack_profiles_figure import tactic_edges  # noqa: E402  the section 4.2 figure's rule, so both count one way
from pipeline_ladder_figure import flow_graphs, load_gap  # noqa: E402

OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-1a_attack_graph_construction"
WIDTH_CM = 16.058          # \textwidth, measured (455.244 pt)
PX = 900
FACE_SCALE = 0.92
FLOOR_PT = 7.95

MAX_TECHNIQUES = 10        # per attack flow, for the example pair
MIN_SHARED_TACTIC = 1

INK, INK2, FAINT, CHROME, ACCENT = "#333", "#6e6e6e", "#9a9a9a", "#ececec", "#1f548c"
SIZES = {"title": 19, "lbl": 17, "sm": 15.5, "name": 15.5}

STYLE = f"""
  html, body {{ margin:0; background:#fff; }}
  svg {{ display:block; font-family: "Nimbus Sans", "TeX Gyre Heros", Helvetica, Arial, sans-serif; }}
  text {{ fill:{INK}; }}
  .title {{ font-size:19px; font-weight:bold; }}
  .lbl   {{ font-size:17px; }}
  .sm    {{ font-size:15.5px; fill:{INK2}; }}
  .name  {{ font-size:15.5px; }}
  .tech  {{ fill:#fff; stroke:{INK}; stroke-width:1.4; }}
  .tac   {{ fill:#fff; stroke:{INK}; stroke-width:1.8; }}
  .band  {{ fill:#f3f3f3; }}
  .halo  {{ paint-order:stroke; stroke:#fff; stroke-width:5px; stroke-linejoin:round; }}
"""

# geometry, px at 900 wide
GUT = 160                  # the left gutter: row names
BOX_W, BOX_H = 140, 48     # a technique box
SLOT_GAP = 36              # between two boxes in one tactic column
COL_GAP = 56               # between tactic columns
TAC_W, TAC_H = 140, 48     # a tactic box in the aggregate
LINE_W = 2.0               # an edge one attack flow draws; the line width is the weight


# ------------------------------------------------------------------ the data --
def connected(f, tech, edges) -> bool:
    """Every technique of the attack flow joined into one drawing (weakly connected)."""
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
    """The attack-graph edges one attack flow draws (same-tactic pairs are not edges)."""
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
        raise SystemExit("pair rule found no two attack flows: relax MAX_TECHNIQUES")
    _, a, b = best
    return a, b, tactic_pairs(a, edges, tac_of) & tactic_pairs(b, edges, tac_of)


def pick_excerpt(pair, shared, edges, tac_of, order):
    """The shared tactic edge and the technique steps each attack flow shows."""
    for p, q in sorted(shared, key=lambda e: (order.index(e[0]), order.index(e[1]))):
        for full, other in (pair, pair[::-1]):
            for s, d in sorted(e for e in edges[full] if tac_of[e[0]] == p and tac_of[e[1]] == q):
                into = sorted(u for u, v in edges[full] if v == s and tac_of[u] == p)
                on = sorted(w for v, w in edges[full] if v == d and tac_of[w] not in (p, q))
                if into and on:
                    mine = [(into[0], s), (s, d), (d, on[0])]
                    theirs = [sorted(e for e in edges[other] if tac_of[e[0]] == p and tac_of[e[1]] == q)[0]]
                    return (p, q), {full: mine, other: theirs}
    raise SystemExit("excerpt rule found no shared tactic edge with a same-tactic step before it")


# ---------------------------------------------------------------- the drawing --
class SVG:
    def __init__(self):
        self.parts: list[str] = []
        self.sizes: list[float] = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, cls="lbl", anchor="middle"):
        self.sizes.append(SIZES[cls.split()[0]])
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.parts.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}>{s}</text>')

    def rect(self, x0, y0, x1, y1, cls, rx=5):
        self.parts.append(f'<rect class="{cls}" x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" '
                          f'height="{y1 - y0:.1f}" rx="{rx}"/>')

    def arrow(self, x0, y0, x1, y1, hot=False, weight=1):
        """Line width is edge weight, the same rule in every row: one attack flow
        draws a thin line; the edge two draw is twice as thick (Marc 2026-10-03:
        the two thin blue steps become one thick blue edge)."""
        col = ACCENT if hot else INK
        w = LINE_W * weight
        m = f"{'hot' if hot else 'ink'}{weight}"
        self.parts.append(f'<path d="M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}" stroke="{col}" stroke-width="{w}" '
                          f'fill="none" marker-end="url(#{m})"/>')


def boxed_name(svg, cx, cy, name, cls="tech", w=BOX_W, h=BOX_H, text_cls="name"):
    svg.rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, cls)
    lines = textwrap.wrap(name, 17) or [name]
    lead = SIZES[text_cls] * 1.15
    y0 = cy - (len(lines) - 1) * lead / 2 + SIZES[text_cls] * 0.35
    for k, ln in enumerate(lines):
        svg.text(cx, y0 + k * lead, ln, text_cls)


def emit(gap, axis, pair, excerpt, flow_name, facts):
    tac_of = {tid: n["primary_tactic"] for tid, n in gap["nodes"].items()}
    name_of = {tid: n["name"] for tid, n in gap["nodes"].items()}
    (p, q), steps = excerpt
    order = axis.matrix_order
    # columns in the order the attack flows step through them (the longer excerpt first), so
    # every edge reads left to right; the tactic names over the columns carry the mapping
    tactics: list[str] = []
    for f in sorted(steps, key=lambda f: -len(steps[f])):
        for tid in [steps[f][0][0]] + [d for _, d in steps[f]]:
            if tac_of[tid] not in tactics:
                tactics.append(tac_of[tid])

    # a tactic column holds as many slots as the most techniques one attack flow shows in it
    slots = {t: max(len({x for e in st for x in e if tac_of[x] == t}) for st in steps.values()) for t in tactics}
    col_w = {t: slots[t] * BOX_W + (slots[t] - 1) * SLOT_GAP for t in tactics}
    span = sum(col_w.values()) + COL_GAP * (len(tactics) - 1)
    x = GUT + (PX - 22 - GUT - span) / 2
    col_x0 = {}
    for t in tactics:
        col_x0[t] = x
        x += col_w[t] + COL_GAP
    col_cx = {t: col_x0[t] + col_w[t] / 2 for t in tactics}

    svg = SVG()
    y_head = 24
    y_rows = [78, 152]                  # the two attack flows
    y_agg = 272                         # the aggregate

    # the header row: the attack flows, by tactic; each tactic a light band down
    # through the attack flows, so the techniques in it read as that tactic
    svg.text(GUT - 12, y_head + 2, "Attack flows", "title", anchor="end")
    for t in tactics:
        svg.rect(col_x0[t] - 10, y_head + 10, col_x0[t] + col_w[t] + 10, y_rows[-1] + BOX_H / 2 + 10, "band", rx=4)
        svg.text(col_cx[t], y_head + 2, axis.label[t].capitalize(), "lbl")

    # the two attack flows: each technique in a slot of its tactic's column,
    # the slots filled from the right so a single technique sits nearest the next column
    rows = sorted(steps, key=lambda f: len(steps[f]))          # the one-step attack flow on top
    for f, y in zip(rows, y_rows):
        st = steps[f]
        seq = [st[0][0]] + [d for _, d in st]
        in_col: dict[str, list[str]] = defaultdict(list)
        for tid in seq:
            if tid not in in_col[tac_of[tid]]:
                in_col[tac_of[tid]].append(tid)
        pos = {}
        for t, tids in in_col.items():
            for k, tid in enumerate(reversed(tids)):
                pos[tid] = col_x0[t] + col_w[t] - BOX_W / 2 - k * (BOX_W + SLOT_GAP)
        nm = flow_name[f]
        for k, ln in enumerate(nm):
            svg.text(GUT - 12, y + 5 + (k - (len(nm) - 1) / 2) * 18, ln, "name", anchor="end")
        for s, d in st:
            hot = (tac_of[s], tac_of[d]) == (p, q)
            svg.arrow(pos[s] + BOX_W / 2 + 2, y, pos[d] - BOX_W / 2 - 4, y, hot=hot)
        for tid in seq:
            boxed_name(svg, pos[tid], y, name_of[tid])

    # the step between: each tactic's band narrows to its one tactic box
    ya, yb = y_rows[-1] + BOX_H / 2 + 10, y_agg - TAC_H / 2
    for t in tactics:
        svg.add(f'<path d="M{col_cx[t]:.1f},{ya + 3:.1f} V{yb - 5:.1f}" stroke="{INK2}" stroke-width="1.8" '
                f'fill="none" marker-end="url(#down)"/>')
    svg.text(GUT - 12, (ya + yb) / 2 + 6, "aggregate", "lbl", anchor="end")

    # the aggregate: one box per tactic, each edge weighted by the attack flows that draw it
    W = tactic_edges(gap, set(steps))                   # the whole pair, then restricted to the excerpt
    shown = {(tac_of[s], tac_of[d]) for st in steps.values() for s, d in st if tac_of[s] != tac_of[d]}
    weight = {e: sum(1 for st in steps.values() if any((tac_of[s], tac_of[d]) == e for s, d in st)) for e in shown}
    for e in shown:
        if not weight[e] <= len(W.get(e, ())):
            raise SystemExit(f"excerpt weight {weight[e]} exceeds the pair's {len(W.get(e, ()))} on {e}")
    svg.text(GUT - 12, y_agg + 6, "Attack graph", "title", anchor="end")
    for a, b in sorted(shown, key=lambda e: order.index(e[0])):
        hot = (a, b) == (p, q)
        x0, x1 = col_cx[a] + TAC_W / 2 + 2, col_cx[b] - TAC_W / 2 - 4
        svg.arrow(x0, y_agg, x1, y_agg, hot=hot, weight=weight[(a, b)])
        svg.text((x0 + x1) / 2, y_agg - 10, str(weight[(a, b)]), "title acc" if hot else "title")
    for t in tactics:
        boxed_name(svg, col_cx[t], y_agg, axis.label[t].capitalize(), cls="tac", w=TAC_W, h=TAC_H, text_cls="lbl")

    height = y_agg + TAC_H / 2 + 4

    defs = "".join(f'<marker id="{m}" viewBox="0 0 10 10" refX="8" refY="5" markerUnits="userSpaceOnUse" '
                   f'markerWidth="{sz}" markerHeight="{sz}" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                   for m, c, sz in (("ink1", INK, 11), ("hot1", ACCENT, 11), ("ink2", INK, 16), ("hot2", ACCENT, 16),
                                    ("down", INK2, 11)))
    style = STYLE + f"  .acc {{ fill:{ACCENT}; }}\n"
    h_cm = WIDTH_CM * height / PX
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{style}'
            f'@page {{ size:{WIDTH_CM}cm {h_cm:.3f}cm; margin:0; }}</style></head><body>'
            f'<svg id="fig" xmlns="http://www.w3.org/2000/svg" width="{PX}" height="{height:.0f}" '
            f'viewBox="0 0 {PX} {height:.0f}" style="width:{WIDTH_CM}cm;height:{h_cm:.3f}cm">'
            f'<defs>{defs}</defs>{"".join(svg.parts)}</svg></body></html>')
    floor = min(svg.sizes) * (WIDTH_CM / 2.54 * 72) / PX / FACE_SCALE
    return html, h_cm, floor, round(height)


def short_name(flow_name: str) -> list[str]:
    """The attack flow's corpus name, on at most two lines of the gutter."""
    lines = textwrap.wrap(flow_name, 16)
    return lines[:2]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
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
        raise SystemExit(f"attack flow count drifted: {len(tech)} carry techniques, header says {gap['source_flow_count']}")
    if len(gap["edges"]) != gap["edge_count"]:
        raise SystemExit("edge count drifted from the GAP header")
    if set(tac_of.values()) - set(axis.matrix_order):
        raise SystemExit("techniques mapped outside the pinned tactic axis")

    W = tactic_edges(gap, set(tech))          # the attack graph
    n_tech = len(gap["edges"])
    tech_single = sum(1 for e in gap["edges"] if len(set(e["flow_ids"])) == 1)
    tac_single = sum(1 for v in W.values() if len(v) == 1)
    fa, fb, shared = pick_pair(tech, edges, tac_of)
    excerpt = pick_excerpt((fa, fb), shared, edges, tac_of, axis.matrix_order)
    names = {}
    # the pair is drawn from the whole corpus, unattributed attack flows included:
    # section 4.1 discloses the corpus's make-up rather than curate the example
    for f in (fa, fb):
        y = (REPO / "data" / "gap" / "flows" / f"{f}.yaml").read_text()
        names[f] = short_name(next(ln.split(":", 1)[1].strip() for ln in y.splitlines() if ln.startswith("flow_name:")))
    facts = {
        "n_flows": len(tech),
        "tech_single_pct": round(100 * tech_single / n_tech),
        "tac_single_pct": round(100 * tac_single / len(W)),
    }
    html, h_cm, floor, h_px = emit(gap, axis, (fa, fb), excerpt, names, facts)
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

    (p, q), steps = excerpt
    print("--- facts (read from the artefacts; the caption and prose may quote them) ---")
    print(f"ATT&CK axis       : v{axis.version}, {len(axis.matrix_order)} tactics")
    print(f"technique level   : {n_tech} edges, {tech_single} drawn by one attack flow only ({100 * tech_single / n_tech:.1f}%)")
    print(f"tactic level      : {len(W)} edges, {tac_single} drawn by one attack flow only ({100 * tac_single / len(W):.1f}%)")
    print(f"pair              : {fa} / {fb}; shared tactic edges {sorted(shared)}")
    print(f"excerpt edge      : {p} -> {q}")
    for f, st in steps.items():
        print(f"  {f:<38}: " + "; ".join(f"{s} {gap['nodes'][s]['name']} -> {d} {gap['nodes'][d]['name']}" for s, d in st))
    print(f"size / type       : {WIDTH_CM} x {h_cm:.2f} cm; smallest type {floor:.2f} pt nominal")


if __name__ == "__main__":
    main()
