#!/usr/bin/env python3
"""Dissertation figure: the thesis ladder --- the movement attacker from
campaign intelligence to a traversal inside MTDSim (the ch4 opening figure,
fig:pipeline). Full portrait page, drawn as a SCHEMATIC WORKED EXAMPLE.

Rebuilt 2026-09-08 on the supervisor's verdict (relayed by Marc; handoff
docs/handoffs/2026-09-08_ch4_fig41_redesign.md): the previous data-faithful
thumbnail ladder (38 flow rows, the 478-edge graph, the 109-transition net)
read as texture, not as a mechanism. This drawing keeps the layer bands and
the rung-to-rung descent (the parts that survived) and replaces every rung
with the smallest example that shows its transformation:

  L0  two real attack flows, side by side on the shared tactic axis, one in
      the accent and one in the second hue --- chosen BY RULE, never by name;
  L1  the same two flows merged into one graph: shared techniques drawn once
      in both hues, edges both flows drew heavier; a faint ghost of the rest
      of the graph says the real one is larger;
  L2  one row per objective class: the same graph conditioned on the
      objective --- the objective tactic banded, the flow whose class it is
      keeps its hue, the rest fall to grey;
  L3  a fragment of one profile's net, firing: the token in a tactic-place,
      its timed dwell and the weighted routing out of it, then the token one
      place on;
  L4  one box: the traversal, whose runtime loop is its own figure
      (fig:runtime-loop, tools/runtime_loop_figure.py).

The thesis numbering only (L0--L4 as the chapter defines them; the repo's
own numbering diverges, architecture.md (b)). Counts are printed to stdout
for the caption, never drawn (the supervisor's "no numbers").

Every structural fact is read from a tracked artefact --- the GAP (which
techniques and edges each flow drew), the objective classification, the
structural nets --- and the tactic axis from the pinned ATT&CK bundle
(tools/_tactic_axis.py), so a drift in any of them fails the build instead
of shipping a stale drawing. The pair rule: among flows with at most
MAX_TECHNIQUES techniques whose GAP edge count is at least techniques - 1
(so each draws as a connected chain), the pair from DIFFERENT objective
classes sharing the most techniques (at least MIN_SHARED), smallest total
first on ties.

Authoring route: SVG assembled here, printed to PDF through headless
Chromium at natural size (the fig:mtdsim-model pattern, Marc's 2026-08-27
ruling for free-layout schematics). Type: house figure sans at 0.92 of
nominal; the floor is 8 pt nominal = 18.4 px at 1100 px -> 16 cm. Greys carry
structure; the accent marks flow A and what the thesis builds; the SECOND
HUE is a scoped exception to the one-accent rule, ruled by Marc on
2026-09-08 for this figure only (figure_table_conventions.md §i).

Usage:
  PYTHONPATH=src python tools/pipeline_ladder_figure.py [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from _tactic_axis import load_axis  # noqa: E402

GAP_JSON = REPO / "data" / "gap" / "gap_v0.5.json"
CLASS_CSV = REPO / "data" / "gasp" / "classification.csv"
PETRI_DIR = REPO / "data" / "ogasp" / "petri"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-0a_pipeline_ladder"

WIDTH_CM = 16.0
PX = 1100
FACE_SCALE = 0.92
FLOOR_PX = 18.4          # 8.0 pt nominal at 1100 px -> 16 cm

MAX_TECHNIQUES = 9
MIN_SHARED = 2
GHOST_NODES = 14         # faint marks standing for the rest of the graph
GHOST_EDGES = 12
FRAGMENT = 4             # places in the L3 window

# The four objective classes in the order the chapter names them; the
# presentation names are the chapter's own words, never the identifiers.
PROFILE_ORDER = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
)
PROFILE_LABEL = {
    "objective_exfiltration": "Exfiltration objective",
    "objective_impact": "Impact objective",
    "objective_exfiltration_impact": "Double extortion",
    "objective_none_c2": "No realised objective",
}
# the profile codes chapter 4 declares (§4.3; Marc's ruling 2026-09-22): this
# figure precedes the declaration, so each L2 row carries the code AND the name
SUB = {1: "\u2081", 2: "\u2082", 3: "\u2083", 4: "\u2084"}
PROFILE_CODE = {
    "objective_exfiltration": 1,
    "objective_impact": 2,
    "objective_exfiltration_impact": 3,
    "objective_none_c2": 4,
}
OBJECTIVE_TACTICS = {
    "objective_exfiltration": ("exfiltration",),
    "objective_impact": ("impact",),
    "objective_exfiltration_impact": ("exfiltration", "impact"),
    "objective_none_c2": ("command-and-control",),
}

# --- palette -----------------------------------------------------------------
INK, INK2, MUTE, HAIR = "#111", "#444", "#7a7a7a", "#d4d4d4"
ACCENT, ACCENT_L = "#1f548c", "#c8d6e8"       # flow A, what the thesis builds
SECOND, SECOND_L = "#c0761a", "#f1dcc1"       # flow B (scoped exception, §i)
BOTH = "#333"
GHOST = "#b9b9b9"

# --- geometry (px at 1100 wide) ------------------------------------------------
GUT_R = 292              # right edge of the label gutter
CL, CR = 312, 1082       # the content region
AX0, AX1 = 352, 1050     # the shared tactic axis (column centres)
NODE_W, NODE_H = 30, 20  # a technique box
STACK = 27               # vertical pitch of techniques sharing a column


# ------------------------------------------------------------------ loading --
def load_gap():
    gap = json.loads(GAP_JSON.read_text())
    layer_of = {n["primary_tactic"]: n["tactic_layer"] for n in gap["nodes"].values()}
    order = sorted(layer_of, key=layer_of.get)
    return gap, order


def load_classes() -> dict[str, str]:
    return {r["flow_id"]: r["class_name"] for r in csv.DictReader(CLASS_CSV.open(encoding="utf-8"))}


def load_net(prof: str) -> dict:
    return json.loads((PETRI_DIR / f"{prof}_structural.json").read_text())


# ---------------------------------------------------------------- the rules --
def flow_graphs(gap):
    """flow -> (technique set, edge list) as the GAP records them."""
    tech: dict[str, set[str]] = defaultdict(set)
    edges: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for tid, n in gap["nodes"].items():
        for f in n["flow_ids"]:
            tech[f].add(tid)
    for e in gap["edges"]:
        for f in e["flow_ids"]:
            edges[f].append((e["source_id"], e["target_id"]))
    return tech, edges


def pick_pair(tech, edges, cls) -> tuple[str, str, set[str]]:
    cands = [f for f in tech
             if len(tech[f]) <= MAX_TECHNIQUES and len(edges[f]) >= len(tech[f]) - 1]
    best = None
    for a, b in itertools.combinations(sorted(cands), 2):
        if cls.get(a) == cls.get(b) or a not in cls or b not in cls:
            continue
        shared = tech[a] & tech[b]
        if len(shared) < MIN_SHARED:
            continue
        key = (len(shared), -(len(tech[a]) + len(tech[b])), a, b)
        if best is None or key > best[0]:
            best = (key, a, b, shared)
    if best is None:
        raise SystemExit("pair rule found no two flows: relax MAX_TECHNIQUES / MIN_SHARED")
    _, a, b, shared = best
    # flow A is the one whose class the chapter names first
    if PROFILE_ORDER.index(cls[a]) > PROFILE_ORDER.index(cls[b]):
        a, b = b, a
    return a, b, shared


def net_window(net: dict, order: list[str]) -> list[str]:
    """The first FRAGMENT consecutive places (axis order) joined by forward
    moves, so the token has somewhere to go at every step."""
    places = [t for t in order if t in set(net["places"])]
    have = {(t["src_tactic"], t["dst_tactic"]) for t in net["transitions"]}
    for i in range(len(places) - FRAGMENT + 1):
        win = places[i:i + FRAGMENT]
        if all((win[k], win[k + 1]) in have for k in range(FRAGMENT - 1)):
            return win
    raise SystemExit("no window of consecutive forward moves in the net")


# ------------------------------------------------------------------ drawing --
class SVG:
    def __init__(self):
        self.parts: list[str] = []
        self.sizes: list[float] = []

    def add(self, s: str):
        self.parts.append(s)

    def text(self, x, y, s, size=19, anchor="start", fill=INK, weight=None, style=None, rotate=None):
        self.sizes.append(size)
        attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-size="{size}px"', f'fill="{fill}"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if style:
            attrs.append(f'font-style="{style}"')
        if rotate is not None:
            attrs.append(f'transform="rotate({rotate} {x:.1f} {y:.1f})"')
        self.add(f"<text {' '.join(attrs)}>{esc(s)}</text>")

    def dump(self) -> str:
        return "\n".join(self.parts)


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def edge_path(x1, y1, x2, y2, back: bool, lift: float) -> str:
    """A shallow quadratic arc; forward arcs bulge up, backward arcs down."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    h = -lift if not back else lift
    return f"M{x1:.1f},{y1:.1f} Q{mx:.1f},{my + h:.1f} {x2:.1f},{y2:.1f}"


def node_box(svg, x, y, kind: str, small=False):
    w, h = (NODE_W, NODE_H) if not small else (22, 15)
    x0, y0 = x - w / 2, y - h / 2
    if kind == "A":
        svg.add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w}" height="{h}" rx="4" fill="{ACCENT_L}" stroke="{ACCENT}" stroke-width="1.6"/>')
    elif kind == "B":
        svg.add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w}" height="{h}" rx="4" fill="{SECOND_L}" stroke="{SECOND}" stroke-width="1.6"/>')
    else:  # both: split fill, dark outline
        svg.add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w}" height="{h}" rx="4" fill="{ACCENT_L}"/>')
        svg.add(f'<polygon points="{x0 + w:.1f},{y0 + 1:.1f} {x0 + w:.1f},{y0 + h:.1f} {x0 + 1:.1f},{y0 + h:.1f}" fill="{SECOND_L}"/>')
        svg.add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w}" height="{h}" rx="4" fill="none" stroke="{BOTH}" stroke-width="1.8"/>')


def layout_columns(nodes: list[str], tac_of, col, y_mid, pitch=STACK, key=None):
    """Stack the techniques sharing a column around y_mid; returns positions."""
    by_col: dict[str, list[str]] = defaultdict(list)
    for tid in nodes:
        by_col[tac_of[tid]].append(tid)
    pos = {}
    for t, tids in by_col.items():
        tids.sort(key=key or (lambda s: s))
        n = len(tids)
        for k, tid in enumerate(tids):
            pos[tid] = (col[t], y_mid + (k - (n - 1) / 2) * pitch)
    return pos


def draw_edges(svg, edges, pos, idx, tac_of, colour, width, marker, opacity=1.0):
    for s, d in edges:
        if s not in pos or d not in pos:
            continue
        (x1, y1), (x2, y2) = pos[s], pos[d]
        delta = idx[tac_of[d]] - idx[tac_of[s]]
        back = delta < 0
        lift = 14 + 4 * abs(delta) if delta != 0 else 22
        # trim to the box edge so the arrowhead is visible
        d_ = edge_path(x1, y1, x2, y2, back, lift)
        svg.add(f'<path d="{d_}" fill="none" stroke="{colour}" stroke-width="{width}" '
                f'marker-end="url(#{marker})" opacity="{opacity}"/>')


def arrow_down(svg, x, y0, y1, verb):
    svg.add(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{INK2}" stroke-width="2.2" marker-end="url(#mI)"/>')
    svg.text(x + 14, (y0 + y1) / 2 + 6, verb, size=19, fill=INK2, style="italic")


def gutter(svg, y, num, title, sub=None):
    svg.text(GUT_R, y, f"{num}  {title}", size=22, anchor="end", weight="bold")
    if sub:
        svg.text(GUT_R, y + 24, sub, size=19, anchor="end", fill=INK2)


def emit(gap, order, axis, cls, tech, edges, fa, fb, shared, nets) -> tuple[str, dict]:
    idx = {t: i for i, t in enumerate(order)}
    col = {t: AX0 + i * (AX1 - AX0) / (len(order) - 1) for i, t in enumerate(order)}
    tac_of = {tid: n["primary_tactic"] for tid, n in gap["nodes"].items()}
    svg = SVG()
    facts: dict[str, object] = {}
    y = 8.0

    # ---- the shared tactic axis: names once, at the top ----------------------
    y_axis = y + 178
    for t in order:
        svg.text(col[t] + 6, y_axis - 12, axis.label[t], size=19, fill=INK2, rotate=-58)
        svg.add(f'<line x1="{col[t]:.1f}" y1="{y_axis - 6}" x2="{col[t]:.1f}" y2="{y_axis + 4}" stroke="{MUTE}" stroke-width="1.2"/>')
    svg.add(f'<line x1="{AX0 - 14}" y1="{y_axis}" x2="{AX1 + 14}" y2="{y_axis}" stroke="{MUTE}" stroke-width="1.2" marker-end="url(#mM)"/>')
    svg.text(GUT_R, y_axis + 5, "ATT&CK tactics, kill-chain order", size=19, anchor="end", fill=INK2)
    y = y_axis + 14
    frame_top = y - 4

    def colguides(y0, y1):
        for t in order:
            svg.add(f'<line x1="{col[t]:.1f}" y1="{y0:.1f}" x2="{col[t]:.1f}" y2="{y1:.1f}" stroke="#ececec" stroke-width="1"/>')

    # ---- L0: two flows, one row each ----------------------------------------
    rows = []
    for f, kind in ((fa, "A"), (fb, "B")):
        stack = max(sum(1 for t in tech[f] if tac_of[t] == c) for c in order)
        rows.append((f, kind, max(2, stack)))
    y0 = y + 22
    l0_top = y0 - 10
    for f, kind, stack in rows:
        h = stack * STACK + 22
        y_mid = y0 + h / 2
        colguides(y0, y0 + h)
        pos = layout_columns(sorted(tech[f]), tac_of, col, y_mid)
        colour, marker = (ACCENT, "mA") if kind == "A" else (SECOND, "mB")
        draw_edges(svg, edges[f], pos, idx, tac_of, colour, 1.8, marker)
        for tid, (px, py) in pos.items():
            node_box(svg, px, py, kind)
        svg.text(CL + 6, y_mid + 6, f"flow {kind}", size=19, fill=colour, weight="bold")
        y0 += h + 10
    # the ghost stack: the flows not drawn
    gy = y0 + 2
    for k in range(3):
        svg.add(f'<rect x="{CL + 40 + k * 6}" y="{gy + k * 5}" width="{CR - CL - 80}" height="18" rx="4" fill="#f3f3f3" stroke="{HAIR}" stroke-width="1"/>')
    n_rest = len(tech) - 2
    svg.text((CL + CR) / 2, gy + 24, f"… and the other {n_rest} flows of the corpus", size=19, anchor="middle", fill=MUTE, style="italic")
    l0_bot = gy + 30
    gutter(svg, (l0_top + l0_bot) / 2 - 4, "L0", "Cyber threat intelligence", "one attack flow per incident")
    # legend under the L0 label
    ly = (l0_top + l0_bot) / 2 + 60
    for k, (kind, lab) in enumerate((("A", "attack flow A"), ("B", "attack flow B"), ("AB", "in both flows"))):
        node_box(svg, GUT_R - 150, ly + k * 26, kind, small=True)
        svg.text(GUT_R - 132, ly + k * 26 + 6, lab, size=19, fill=INK2)
    svg.add(f'<circle cx="{GUT_R - 150}" cy="{ly + 3 * 26}" r="4.5" fill="{GHOST}"/>')
    svg.text(GUT_R - 132, ly + 3 * 26 + 6, "other flows", size=19, fill=INK2)
    y = l0_bot

    # ---- aggregate -> L1 -------------------------------------------------------
    arrow_down(svg, (AX0 + AX1) / 2, y + 6, y + 42, "aggregate")
    y += 50
    union = sorted(tech[fa] | tech[fb])
    kind_of = {t: ("AB" if t in shared else "A" if t in tech[fa] else "B") for t in union}
    stack = max(sum(1 for t in union if tac_of[t] == c) for c in order)
    h1 = max(3, stack) * STACK + 42
    colguides(y, y + h1)
    y_mid = y + h1 / 2
    rank = {"AB": 0, "A": 1, "B": 2}
    pos = layout_columns(union, tac_of, col, y_mid, key=lambda s: (rank[kind_of[s]], s))
    # the ghost of the rest of the graph
    rest_nodes = sorted((n for tid, n in gap["nodes"].items() if tid not in pos),
                        key=lambda n: -n["flow_count"])[:GHOST_NODES]
    gpos = {}
    slots: dict[str, int] = defaultdict(int)
    for n in rest_nodes:
        t = n["primary_tactic"]
        taken = [py for tid, (px, py) in pos.items() if tac_of[tid] == t]
        lo, hi = (min(taken), max(taken)) if taken else (y_mid + STACK / 2, y_mid - STACK / 2)
        k = slots[t]
        # alternate below and above the column's stack, inside the rung
        gy_ = hi + STACK * (k // 2 + 1) * 0.85 if k % 2 == 0 else lo - STACK * (k // 2 + 1) * 0.85
        if not (y + 10 < gy_ < y + h1 - 10):
            continue
        slots[t] += 1
        gpos[n["technique_id"]] = (col[t], gy_)
    allpos = {**pos, **gpos}
    pair_edges = set(edges[fa]) | set(edges[fb])
    rest_edges = sorted((e for e in gap["edges"]
                         if (e["source_id"], e["target_id"]) not in pair_edges
                         and e["source_id"] in allpos and e["target_id"] in allpos),
                        key=lambda e: -e["observation_count"])[:GHOST_EDGES]
    draw_edges(svg, [(e["source_id"], e["target_id"]) for e in rest_edges], allpos, idx, tac_of,
               GHOST, 1.2, "mG", opacity=0.7)
    for tid, (px, py) in gpos.items():
        svg.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{GHOST}"/>')
    # the pair's edges: both-drawn heavier and dark
    ea, eb = set(edges[fa]), set(edges[fb])
    draw_edges(svg, sorted(ea - eb), pos, idx, tac_of, ACCENT, 1.8, "mA")
    draw_edges(svg, sorted(eb - ea), pos, idx, tac_of, SECOND, 1.8, "mB")
    draw_edges(svg, sorted(ea & eb), pos, idx, tac_of, BOTH, 3.2, "mD")
    for tid, (px, py) in pos.items():
        node_box(svg, px, py, kind_of[tid])
    gutter(svg, y_mid - 4, "L1", "Attack graph", "every flow, one graph")
    facts["l1_ghost"] = (len(gpos), len(rest_edges))
    facts["shared_edges"] = len(ea & eb)
    y += h1

    # ---- condition on objective -> L2 ------------------------------------------
    arrow_down(svg, (AX0 + AX1) / 2, y + 6, y + 42, "condition on objective")
    y += 52
    row_h = 58
    l2_top = y
    svg.text(GUT_R, y + 2, "L2  Attack profiles", size=22, anchor="end", weight="bold")
    y += 12
    for prof in PROFILE_ORDER:
        r0, r1 = y, y + row_h
        rm = (r0 + r1) / 2
        svg.add(f'<rect x="{CL}" y="{r0}" width="{CR - CL}" height="{row_h}" rx="4" fill="#fafafa" stroke="{HAIR}" stroke-width="1"/>')
        colguides(r0 + 6, r1 - 6)
        for t in OBJECTIVE_TACTICS[prof]:
            svg.add(f'<rect x="{col[t] - 22:.1f}" y="{r0 + 4}" width="44" height="{row_h - 8}" rx="3" fill="{ACCENT_L}" opacity="0.55"/>')
        # the graph, conditioned: the matching pair flow keeps its hue, the rest grey
        net = nets[prof]
        nplaces = set(net["places"])
        gp = {tid: (px, rm + (py - y_mid) * 0.62) for tid, (px, py) in allpos.items()
              if tac_of[tid] in nplaces}
        grey_nodes = [tid for tid in gp if tid not in tech[fa] | tech[fb] or cls[fa if tid in tech[fa] else fb] != prof]
        draw_edges(svg, [(e["source_id"], e["target_id"]) for e in rest_edges], gp, idx, tac_of,
                   GHOST, 1.0, "mG", opacity=0.6)
        for tid in grey_nodes:
            px, py = gp[tid]
            svg.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.2" fill="{GHOST}"/>')
        for f, kind, colour, marker in ((fa, "A", ACCENT, "mA"), (fb, "B", SECOND, "mB")):
            if cls[f] != prof:
                continue
            fp = {tid: gp[tid] for tid in tech[f] if tid in gp}
            draw_edges(svg, edges[f], fp, idx, tac_of, colour, 1.6, marker)
            for tid, (px, py) in fp.items():
                svg.add(f'<rect x="{px - 10:.1f}" y="{py - 6.5:.1f}" width="20" height="13" rx="3" fill="{ACCENT_L if kind == "A" else SECOND_L}" stroke="{colour}" stroke-width="1.5"/>')
        for t in OBJECTIVE_TACTICS[prof]:
            svg.add(f'<circle cx="{col[t]:.1f}" cy="{rm:.1f}" r="13" fill="none" stroke="{ACCENT}" stroke-width="2.2"/>')
            svg.add(f'<circle cx="{col[t]:.1f}" cy="{rm:.1f}" r="3.2" fill="{ACCENT}"/>')
        svg.text(GUT_R, rm + 6, PROFILE_LABEL[prof], size=19, anchor="end", fill=INK2)
        svg.text(GUT_R, rm - 14, f"c{SUB[PROFILE_CODE[prof]]}", size=19, anchor="end", fill=INK2, style="italic")
        y = r1 + 8
    y -= 8

    # ---- give executable semantics -> L3 -----------------------------------------
    arrow_down(svg, (AX0 + AX1) / 2, y + 6, y + 42, "give executable semantics")
    y += 52
    prof_a = cls[fa]
    net = nets[prof_a]
    win = net_window(net, order)
    facts["fragment"] = (prof_a, win)
    have = {(t["src_tactic"], t["dst_tactic"]) for t in net["transitions"]}
    inner = [(a, b) for a in win for b in win if a != b and (a, b) in have]
    R = 16
    state_h = 98
    l3_top = y
    # zoomed: the fragment is four places, so it is drawn at a readable pitch
    # with the tactic name under each place instead of on the axis columns
    PITCH = 150
    fx = {t: CL + 136 + k * PITCH for k, t in enumerate(win)}
    T_DX, I_DX, I_PITCH = R + 20, R + 46, 15   # timed bar, immediate bars, their stack

    def draw_state(ys, tok_i, fire_to, names):
        """One marking of the fragment: the token at win[tok_i]; after every
        place its timed dwell bar, then the fan of weighted immediate moves
        (Marsan grammar, as fig:gspn-gadget draws it); the move about to
        fire in the accent, the rest of the live place's moves in ink, every
        other place's in grey."""
        for k, t in enumerate(win):
            x = fx[t]
            live = (k == tok_i)
            pc = INK if live else MUTE
            outs = [b for (a, b) in inner if a == t]
            outs.sort(key=lambda b: (idx[b] < idx[t], abs(idx[b] - idx[t])))
            if outs:
                tx = x + T_DX
                svg.add(f'<line x1="{x + R:.1f}" y1="{ys:.1f}" x2="{tx - 4:.1f}" y2="{ys:.1f}" stroke="{pc}" stroke-width="1.4"/>')
                svg.add(f'<rect x="{tx - 4:.1f}" y="{ys - 13:.1f}" width="8" height="26" fill="#fff" stroke="{pc}" stroke-width="{2 if live else 1.4}"/>')
                n = len(outs)
                for j, b in enumerate(outs):
                    iy = ys + (j - (n - 1) / 2) * I_PITCH
                    ix = x + I_DX
                    hot = live and b == fire_to
                    colr = ACCENT if hot else (INK2 if live else GHOST)
                    wid = 2.4 if hot else 1.4
                    mk = "mA" if hot else ("mI" if live else "mG")
                    svg.add(f'<line x1="{tx + 4:.1f}" y1="{ys:.1f}" x2="{ix - 3:.1f}" y2="{iy:.1f}" stroke="{colr}" stroke-width="{wid}"/>')
                    svg.add(f'<rect x="{ix - 3:.1f}" y="{iy - 8:.1f}" width="5" height="16" fill="{colr}"/>')
                    fwd = idx[b] > idx[t]
                    x2 = fx[b] - R - 2 if fwd else fx[b] + R + 2
                    dist = abs(idx[b] - idx[t])
                    if fwd and dist == 1:
                        svg.add(f'<line x1="{ix + 3:.1f}" y1="{iy:.1f}" x2="{x2:.1f}" y2="{ys:.1f}" stroke="{colr}" stroke-width="{wid}" marker-end="url(#{mk})"/>')
                    else:
                        lift = (-34 - 10 * dist) if fwd else (38 + 6 * dist)
                        mid = (ix + x2) / 2
                        svg.add(f'<path d="M{ix + 3:.1f},{iy:.1f} Q{mid:.1f},{ys + lift:.1f} {x2:.1f},{ys:.1f}" fill="none" stroke="{colr}" stroke-width="{wid}" marker-end="url(#{mk})"/>')
            svg.add(f'<circle cx="{x:.1f}" cy="{ys:.1f}" r="{R}" fill="#fff" stroke="{pc}" stroke-width="{2 if live else 1.4}"/>')
            if names:   # two lines, so neighbours never collide
                for j, word in enumerate(axis.label[t].split(" ", 1)):
                    svg.text(x, ys + R + 22 + j * 21, word, size=19, anchor="middle", fill=INK2)
            if live:
                svg.add(f'<circle cx="{x:.1f}" cy="{ys:.1f}" r="6.5" fill="{ACCENT}"/>')
                cx_, cy_ = x + T_DX, ys - 34
                svg.add(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="9" fill="#fff" stroke="{INK2}" stroke-width="1.5"/>')
                svg.add(f'<path d="M{cx_:.1f},{cy_ - 5:.1f} V{cy_:.1f} H{cx_ + 4:.1f}" fill="none" stroke="{INK2}" stroke-width="1.5"/>')
                svg.text(cx_ + 14, cy_ + 6, "dwell", size=19, fill=INK2)

    ys1 = y + 52
    draw_state(ys1, 0, win[1], names=False)
    ys2 = ys1 + state_h
    draw_state(ys2, 1, win[2], names=True)
    xa, xb = fx[win[0]], fx[win[1]]
    svg.add(f'<path d="M{xa:.1f},{ys1 + R + 4:.1f} C{xa:.1f},{ys1 + 70:.1f} {xb:.1f},{ys2 - 70:.1f} {xb:.1f},{ys2 - R - 4:.1f}" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#mA)"/>')
    svg.text((xa + xb) / 2 + 12, (ys1 + ys2) / 2 + 6, "fires", size=19, fill=ACCENT, style="italic")
    svg.text(CL + 6, ys1 - 32, "before", size=19, fill=MUTE, style="italic")
    svg.text(CL + 6, ys2 - 32, "after", size=19, fill=MUTE, style="italic")
    l3_bot = ys2 + R + 40
    # legend for the net grammar, in the gutter under the rung label
    lx = GUT_R - 158
    ly = (l3_top + l3_bot) / 2 + 44
    svg.add(f'<circle cx="{lx + 8}" cy="{ly}" r="8" fill="#fff" stroke="{INK2}" stroke-width="1.5"/>')
    svg.text(lx + 24, ly + 6, "tactic (place)", size=19, fill=INK2)
    svg.add(f'<rect x="{lx + 4}" y="{ly + 26 - 9}" width="7" height="18" fill="#fff" stroke="{INK2}" stroke-width="1.5"/>')
    svg.text(lx + 24, ly + 26 + 6, "timed dwell", size=19, fill=INK2)
    svg.add(f'<rect x="{lx + 5}" y="{ly + 52 - 9}" width="5" height="18" fill="{INK2}"/>')
    svg.text(lx + 24, ly + 52 + 6, "weighted move", size=19, fill=INK2)
    svg.add(f'<circle cx="{lx + 8}" cy="{ly + 78}" r="5.5" fill="{ACCENT}"/>')
    svg.text(lx + 24, ly + 78 + 6, "token", size=19, fill=INK2)
    gutter(svg, (l3_top + l3_bot) / 2 - 30, "L3", "Petri net", "one profile, one net")
    y = l3_bot

    # ---- the movement-layer frame ----------------------------------------------
    frame_bot = y + 4
    svg.add(f'<rect x="{CL - 6}" y="{frame_top}" width="{CR - CL + 12}" height="{frame_bot - frame_top}" rx="6" fill="none" stroke="{ACCENT}" stroke-width="1.3" opacity="0.6"/>')
    # the frame is unlabelled since 2026-09-22 (register E2: the layer names are dissolved; the L-labels are the signage)

    # ---- traverse -> L4 ---------------------------------------------------------
    arrow_down(svg, (AX0 + AX1) / 2, frame_bot + 6, frame_bot + 42, "join")
    y = frame_bot + 50
    box_h = 66
    svg.add(f'<rect x="{CL - 6}" y="{y}" width="{CR - CL + 12}" height="{box_h}" rx="6" fill="#f6f6f6" stroke="{INK2}" stroke-width="1.3"/>')
    cy_ = y + box_h / 2
    chips = (("token", ACCENT), ("join", INK), ("MTDSim", INK))
    cw, gap_ = 158, 122
    x0 = (CL + CR) / 2 - (3 * cw + 2 * gap_) / 2
    for k, (name, colr) in enumerate(chips):
        cx0 = x0 + k * (cw + gap_)
        svg.add(f'<rect x="{cx0:.1f}" y="{cy_ - 20}" width="{cw}" height="40" rx="5" fill="#fff" stroke="{colr}" stroke-width="1.6"/>')
        svg.text(cx0 + cw / 2, cy_ + 7, name, size=20, anchor="middle", fill=colr)
        if k < 2:
            ax0_, ax1_ = cx0 + cw + 6, cx0 + cw + gap_ - 6
            svg.add(f'<line x1="{ax0_:.1f}" y1="{cy_ - 8}" x2="{ax1_:.1f}" y2="{cy_ - 8}" stroke="{INK2}" stroke-width="1.8" marker-end="url(#mI)"/>')
            svg.add(f'<line x1="{ax1_:.1f}" y1="{cy_ + 8}" x2="{ax0_:.1f}" y2="{cy_ + 8}" stroke="{INK2}" stroke-width="1.8" marker-end="url(#mI)"/>')
            top, bot = (("tactic", "re-weighting") if k == 0 else ("verb, dwell", "verdict"))
            svg.text((ax0_ + ax1_) / 2, cy_ - 14, top, size=19, anchor="middle", fill=INK2)
            svg.text((ax0_ + ax1_) / 2, cy_ + 26, bot, size=19, anchor="middle", fill=INK2)
    gutter(svg, cy_ - 4, "L4", "MTDSim", "the runtime loop")
    y += box_h + 10

    height = int(round(y))
    facts["size_px"] = (PX, height)

    defs = f"""<defs>
  <marker id="mA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>
  <marker id="mB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{SECOND}"/></marker>
  <marker id="mD" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BOTH}"/></marker>
  <marker id="mI" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker>
  <marker id="mG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GHOST}"/></marker>
  <marker id="mM" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTE}"/></marker>
</defs>"""
    h_cm = WIDTH_CM * height / PX
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>fig:pipeline --- the APT attacker model end to end (generated; do not hand-edit)</title>
<style>
  html, body {{ margin:0; background:#fff; }}
  body {{ width: {PX}px; }}
  @media print {{ @page {{ size: {WIDTH_CM}cm {h_cm:.2f}cm; margin:0; }} body {{ width:{WIDTH_CM}cm; }} svg {{ width:{WIDTH_CM}cm; height:{h_cm:.2f}cm; }} }}
  svg {{ display:block; font-family: "Nimbus Sans", "TeX Gyre Heros", Helvetica, Arial, sans-serif; }}
</style>
</head>
<body>
<svg id="fig" viewBox="0 0 {PX} {height}" width="{PX}" height="{height}" xmlns="http://www.w3.org/2000/svg">
{defs}
{svg.dump()}
</svg>
</body>
</html>
"""
    facts["min_px"] = min(svg.sizes)
    return html, facts


# --------------------------------------------------------------------- main --
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--png", action="store_true", help="also write a PNG preview next to the PDF")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    gap, order = load_gap()
    axis = load_axis()
    axis.check_against(order)
    cls = load_classes()
    tech, edges = flow_graphs(gap)
    fa, fb, shared = pick_pair(tech, edges, cls)
    nets = {p: load_net(p) for p in PROFILE_ORDER}
    for p in PROFILE_ORDER:
        if set(nets[p]["places"]) - set(order):
            raise SystemExit(f"{p}: places outside the pinned tactic axis")

    html, facts = emit(gap, order, axis, cls, tech, edges, fa, fb, shared, nets)
    floor = facts["min_px"] * (WIDTH_CM / 2.54 * 72) / PX / FACE_SCALE
    if floor < 7.95:
        raise SystemExit(f"smallest type prints at {floor:.1f}pt (< 8pt floor)")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = OUT_DIR / f"{STEM}.html"
    html_path.write_text(html)
    w_px, h_px = facts["size_px"]
    h_cm = WIDTH_CM * h_px / w_px
    print(f"wrote {html_path.relative_to(REPO)}")

    if not a.no_pdf:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": w_px, "height": h_px}, device_scale_factor=2)
            pg.goto(html_path.as_uri())
            pg.wait_for_timeout(300)
            if a.png:
                pg.locator("#fig").screenshot(path=str(OUT_DIR / f"{STEM}.png"))
                print(f"preview {OUT_DIR / (STEM + '.png')}")
            pg.emulate_media(media="print")
            pg.pdf(path=str(OUT_DIR / f"{STEM}.pdf"), width=f"{WIDTH_CM}cm", height=f"{h_cm:.2f}cm",
                   margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                   print_background=True, prefer_css_page_size=False)
            b.close()
        print(f"wrote {(OUT_DIR / (STEM + '.pdf')).relative_to(REPO)}  ({WIDTH_CM} x {h_cm:.2f} cm)")

    print("--- facts (all read from tracked artefacts; the caption may quote them) ---")
    print(f"ATT&CK bundle                 : v{axis.version}, {len(order)} tactics")
    print(f"corpus                        : {len(tech)} attack flows; {len(gap['nodes'])} techniques, {len(gap['edges'])} transitions in the graph")
    for lab, f in (("flow A", fa), ("flow B", fb)):
        print(f"{lab:<30}: {f}  ({PROFILE_LABEL[cls[f]]}; {len(tech[f])} techniques, {len(edges[f])} edges)")
    print(f"shared techniques             : {sorted(shared)}  (edges drawn by both: {facts['shared_edges']})")
    print(f"L1 ghost                      : {facts['l1_ghost'][0]} nodes, {facts['l1_ghost'][1]} edges of the rest")
    p, win = facts["fragment"]
    print(f"L3 fragment                   : {PROFILE_LABEL[p]} net, places {win}")
    print(f"smallest type                 : {facts['min_px']}px -> {floor:.1f}pt nominal ({floor * FACE_SCALE:.1f}pt set)")
    print(f"drawn size                    : {WIDTH_CM} x {h_cm:.2f} cm ({h_cm / 2.54 * 72:.0f} pt tall)")


if __name__ == "__main__":
    main()
