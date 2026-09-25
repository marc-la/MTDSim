#!/usr/bin/env python3
"""Dissertation figure: the section 4.2 figure --- the four attack profiles,
c1-c4, each drawn as a grid of the tactic-to-tactic edges its own attack flows
drew.

Takeaways (the caption carries the rest; Marc 2026-09-25: few words, no
duplication, the caption does not over-explain):

  T1  each attack flow sits in one profile, by its objective (the counts in
      the titles, read from the classification);
  T2  the profiles differ in which edges exist and how often they recur.

The attack graph itself is NOT drawn here: it is the end result of the
section 4.1 figure, which may import `draw_grid` from this module so that the
two figures draw the grid identically.

Words: the attack graph and the profiles have EDGES; "transition" is reserved
for the Petri net (lead-session ruling 2026-09-25). The Petri-net artefacts
are read only for the cross-check.

Form: a 2 x 2 grid of small multiples, one tactic-by-tactic grid per profile
(row = the tactic an edge leaves, column = the tactic it enters, both in
ATT&CK kill-chain order; grey = the number of the profile's attack flows that
drew the edge). Chosen over arc rows because the data is dense (the attack
graph has 122 of the 210 ordered tactic pairs, 57 backward), and a grid keeps
each edge in the same cell in every panel (Ghoniem, Fekete & Castagliola 2004).
Tactic names: once per grid row beside the rows; for the columns, ONE band
between the two grid rows, directly under the top grids and directly over the
bottom row's titles, serving both. Titles above their grids. "from" heads the
row labels, "to" sits beside the column band. Empty cells white on a chrome
grid; the column of the tactic that names the profile's objective
(exfiltration for c1, impact for c2, both for c3, none for c4) outlined in the
one accent. The key: the four greys and the outline, nothing else.

Each grid draws only the edges its own flows drew: the profile as built is the
attack graph induced on its techniques, and the pairs its flows never draw
carry weight zero (section 4.3), so they are not drawn.

The edge sets are computed from the attack graph exactly as section 4.1
builds it: technique edges rolled up to (source tactic, target tactic) pairs,
same-tactic pairs dropped, weight = distinct attack flows drawing the pair ---
restricted to the profile's own flows. Cross-checked against the Petri-net
artefacts (data/ogasp/petri/*_structural.json, the aggregate's included):
the flow-backed transitions (raw numerator > 0) must equal the computed edge
set with the same backing flows, or the build fails; zero-weight transitions
are counted and printed, not drawn.

House style: tools/ch4_overview_figure.py (900 px -> \\textwidth through
Chromium, greys + one accent, type-floor check).

Usage:
  PYTHONPATH=src python tools/ch4_attack_profiles_figure.py
      [--out-dir DIR] [--stem STEM] [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from _tactic_axis import load_axis  # noqa: E402
from pipeline_ladder_figure import (  # noqa: E402  the artefact readers
    OBJECTIVE_TACTICS, PETRI_DIR, PROFILE_CODE, PROFILE_LABEL, PROFILE_ORDER, SUB,
    load_classes, load_gap, load_net,
)

GASP_DIR = REPO / "data" / "gasp"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-2a_attack_profiles"
WIDTH_CM = 16.058          # \textwidth, measured (455.244 pt)
PX = 900
FACE_SCALE = 0.92
FLOOR_PT = 7.95

INK, INK2, FAINT, ACCENT = "#333", "#6e6e6e", "#b0b0b0", "#1f548c"
CHROME = "#ececec"         # the cell grid: fainter than the faintest data
# the recurrence ramp: attack flows that drew the edge
BINS = ((1, 1, "1", "#bdbdbd"), (2, 2, "2", "#8c8c8c"),
        (3, 4, "3–4", "#5c5c5c"), (5, 10 ** 6, "5 or more", "#262626"))

AGG = "aggregate"
# read and cross-checked: the aggregate and c1-c4; drawn: c1-c4 only
PANELS = (AGG,) + PROFILE_ORDER
DRAWN = PROFILE_ORDER
# the objective an attack flow achieved, as a column (c4 achieved none; the
# aggregate is not defined by an objective). OBJECTIVE_TACTICS gives c4
# command and control, the tactic its flows end in, which is not an objective.
OBJ_COLUMNS = {p: (() if p == "objective_none_c2" else OBJECTIVE_TACTICS[p]) for p in PROFILE_ORDER}
OBJ_COLUMNS[AGG] = ()

STYLE = f"""
  html, body {{ margin:0; background:#fff; }}
  svg {{ display:block; font-family: "Nimbus Sans", "TeX Gyre Heros", Helvetica, Arial, sans-serif; }}
  text {{ fill:{INK}; }}
  .title {{ font-size:19px; font-weight:bold; }}
  .lbl   {{ font-size:17px; }}
  .sm    {{ font-size:15.5px; fill:{INK2}; }}
  .tick  {{ font-size:15.5px; }}
  .acc   {{ fill:{ACCENT}; }}
  .obj   {{ fill:none; stroke:{ACCENT}; stroke-width:1.8; }}
"""
SIZES = {"title": 19, "lbl": 17, "sm": 15.5, "tick": 15.5}
# (the codes' subscripts print at 14.5 px = 7.97 pt nominal, just over the floor)


class SVG:
    def __init__(self):
        self.parts: list[str] = []
        self.sizes: list[float] = []

    def add(self, s: str):
        self.parts.append(s)

    def text(self, x, y, s, cls="lbl", anchor="start", extra="", raw=False):
        self.sizes.append(SIZES[cls.split()[0]])
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        if not raw:
            s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}{extra}>{s}</text>')

    def rect(self, x0, y0, w, h, fill, extra=""):
        self.add(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"{extra}/>')


def shade(n: int) -> str:
    for lo, hi, _lab, col in BINS:
        if lo <= n <= hi:
            return col
    raise ValueError(n)


# ------------------------------------------------------------------ the data --
def tactic_edges(gap, flows: set[str]) -> dict[tuple[str, str], set[str]]:
    """Section 4.1's rule, on a subset of the flows: every technique edge a flow
    in `flows` drew, rolled up to its (source tactic, target tactic) pair;
    same-tactic pairs dropped; the pair keeps the set of flows drawing it."""
    nodes = gap["nodes"]
    out: dict[tuple[str, str], set[str]] = defaultdict(set)
    for e in gap["edges"]:
        fs = set(e["flow_ids"]) & flows
        if not fs:
            continue
        a, b = nodes[e["source_id"]]["primary_tactic"], nodes[e["target_id"]]["primary_tactic"]
        if a != b:
            out[(a, b)] |= fs
    return dict(out)


def profiles(gap, cls):
    """panel -> (its flows, its tactic edges), with the drift guards."""
    if set(cls.values()) != set(PROFILE_ORDER):
        raise SystemExit(f"objective classes drifted: {sorted(set(cls.values()))} vs {PROFILE_ORDER}")
    drew = {f for n in gap["nodes"].values() for f in n["flow_ids"]}
    if drew != set(cls):
        raise SystemExit(f"classification and attack graph disagree on the flows: "
                         f"{sorted(drew ^ set(cls))}")
    out = {}
    for p in PANELS:
        flows = set(cls) if p == AGG else {f for f, c in cls.items() if c == p}
        if p != AGG:
            gasp = json.loads((GASP_DIR / f"gasp_{p}.json").read_text())
            if set(gasp["provenance"]["flow_ids"]) != flows:
                raise SystemExit(f"{p}: classification.csv and gasp_{p}.json list different flows")
        out[p] = (flows, tactic_edges(gap, flows))
    return out


def cross_check(prof) -> dict[str, dict]:
    """Against the Petri-net artefacts: the flow-backed transitions (raw
    numerator > 0) must be exactly the computed edge set, backed by the same flows.
    Zero-weight transitions are reported, not failed."""
    report = {}
    for p, (_flows, T) in prof.items():
        net = load_net(p)
        backed, zero = {}, []
        for t in net["transitions"]:
            key = (t["src_tactic"], t["dst_tactic"])
            raw = t["weights"]["raw"]
            if raw["numerator"] > 0:
                backed[key] = set(raw["backing_flow_ids"])
            else:
                zero.append(key)
        if set(backed) != set(T):
            raise SystemExit(f"{p}: flow-backed net transitions disagree with the attack-graph edges: "
                             f"only net {sorted(set(backed) - set(T))}, only graph {sorted(set(T) - set(backed))}")
        bad = [k for k in T if backed[k] != T[k]]
        if bad:
            raise SystemExit(f"{p}: backing flows disagree on {bad[:5]}")
        dedup_zero = sum(1 for t in net["transitions"] if t["weights"]["operator_dedup"]["numerator"] == 0)
        report[p] = {"net": len(net["transitions"]), "backed": len(backed), "zero": len(zero),
                     "zero_dedup": dedup_zero, "places": len(net["places"])}
    return report


# ------------------------------------------------------------------ drawing --
def code(p: str, size: float = 18, sub_size: float = 14.5) -> str:
    """A profile code set as chapter 5 sets it: math-italic c, upright
    subscript. The trailing tspan resets the baseline (it needs a glyph)."""
    sub = "agg" if p == AGG else str(PROFILE_CODE[p])
    serif = "font-family:'Nimbus Roman','Times New Roman',serif"
    return (f'<tspan style="{serif};font-style:italic;font-size:{size}px">c</tspan>'
            f'<tspan dy="4" style="{serif};font-size:{sub_size}px">{sub}</tspan><tspan dy="-4"> </tspan>')


# --------------------------------------------------------------- the grid --
GRID_LABEL_PX = 15.5       # tactic names (8.52 pt nominal at 900 px -> \textwidth)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def column_labels(order: Sequence[str], labels: Mapping[str, str], x0: float, cell: float,
                  y: float, side: str = "above") -> str:
    """The tactic names of a grid's columns, set vertically. side='above': the
    names end at y (the grid's top edge minus a gap); 'below': they start at y;
    'centre': they are centred on y (a band shared by two grids)."""
    anchor = {"above": "start", "below": "end", "centre": "middle"}[side]
    out = []
    for i, t in enumerate(order):
        cx = x0 + (i + 0.5) * cell + GRID_LABEL_PX * 0.34
        out.append(f'<text x="{cx:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{GRID_LABEL_PX}px" '
                   f'fill="{INK}" transform="rotate(-90 {cx:.1f} {y:.1f})">{_esc(labels[t])}</text>')
    return "\n".join(out)


def draw_grid(counts: Mapping[tuple[str, str], int], order: Sequence[str], x0: float, y0: float,
              cell: float, *, labels: Mapping[str, str] | None = None, row_labels: bool = True,
              col_labels: str | None = "above", outline: Iterable[str] = ()) -> tuple[str, list[float]]:
    """ONE tactic grid, as an SVG fragment with every style inline (so any
    figure can drop it in). Row = the tactic an edge leaves, column = the
    tactic it enters, both in `order`; a filled cell's grey = the edge's count
    (BINS); empty cells white on a chrome grid; the diagonal is never filled;
    a thin grey frame; the columns named in `outline` outlined in the accent.

    counts      {(from_tactic, to_tactic): number of attack flows that drew it}
    x0, y0      the grid's top-left corner; it is len(order) * cell square
    labels      tactic -> display name (tools/_tactic_axis.load_axis().label);
                needed only when a label is drawn
    row_labels  draw the names right-aligned left of the rows
    col_labels  'above' / 'below' the grid, or None to omit (e.g. a shared band
                drawn with column_labels())
    Returns (fragment, font sizes used) --- feed the sizes to the caller's
    type-floor check."""
    n = len(order)
    M = n * cell
    idx = {t: i for i, t in enumerate(order)}
    parts, sizes = [], []
    grid = " ".join(f"M{x0 + k * cell:.2f},{y0:.2f} V{y0 + M:.2f} M{x0:.2f},{y0 + k * cell:.2f} H{x0 + M:.2f}"
                    for k in range(1, n))
    parts.append(f'<path d="{grid}" stroke="{CHROME}" stroke-width="1" fill="none"/>')
    g = 1.2                                   # white seam between filled cells
    for (r, c), k in counts.items():
        if k <= 0 or r == c or r not in idx or c not in idx:
            continue
        parts.append(f'<rect x="{x0 + idx[c] * cell + g / 2:.2f}" y="{y0 + idx[r] * cell + g / 2:.2f}" '
                     f'width="{cell - g:.2f}" height="{cell - g:.2f}" fill="{shade(k)}"/>')
    parts.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{M:.2f}" height="{M:.2f}" fill="none" '
                 f'stroke="{FAINT}" stroke-width="1.2"/>')
    for c in outline:
        parts.append(f'<rect x="{x0 + idx[c] * cell:.2f}" y="{y0 - 1:.2f}" width="{cell:.2f}" '
                     f'height="{M + 2:.2f}" fill="none" stroke="{ACCENT}" stroke-width="1.8"/>')
    if row_labels:
        for t in order:
            parts.append(f'<text x="{x0 - 8:.1f}" y="{y0 + (idx[t] + 0.5) * cell + GRID_LABEL_PX * 0.34:.1f}" '
                         f'text-anchor="end" font-size="{GRID_LABEL_PX}px" fill="{INK}">{_esc(labels[t])}</text>')
        sizes.append(GRID_LABEL_PX)
    if col_labels:
        y = y0 - 6 if col_labels == "above" else y0 + M + 6
        parts.append(column_labels(order, labels, x0, cell, y, col_labels))
        sizes.append(GRID_LABEL_PX)
    return "\n".join(parts), sizes


def emit(prof, axis) -> tuple[str, float, float]:
    svg = SVG()
    order = axis.matrix_order
    n = len(order)
    svg.sizes.append(14.5)                    # the codes' subscripts (see code())

    GX = 182                      # right edge of the row labels
    GAP = 20                      # between grid columns
    cell = 17.0                   # >= the 15.5 px vertical names' pitch; fills \\textwidth with the key
    M = n * cell
    COLS = (GX + 8, GX + 8 + M + GAP)
    TITLE_H = 28
    BAND = 172                    # the shared column-name band (longest name ~160 px)
    y_m1 = 4 + TITLE_H
    y_band = y_m1 + M + 4
    y_m2 = y_band + BAND + TITLE_H
    height = y_m2 + M + 4

    for k, p in enumerate(DRAWN):
        x0, ym = COLS[k % 2], (y_m1, y_m2)[k // 2]
        flows, T = prof[p]
        frag, sizes = draw_grid({e: len(f) for e, f in T.items()}, order, x0, ym, cell,
                                labels=axis.label, row_labels=(k % 2 == 0), col_labels=None,
                                outline=OBJ_COLUMNS[p])
        svg.add(frag)
        svg.sizes += sizes
        svg.text(x0, ym - 9, f'{code(p)}<tspan font-weight="bold">{PROFILE_LABEL[p]}</tspan> ({len(flows)} flows)',
                 "lbl", raw=True)
    # the column names, once, in the band both grid rows touch
    yc = y_band + BAND / 2
    for x0 in COLS:
        svg.add(column_labels(order, axis.label, x0, cell, yc, "centre"))
    svg.sizes.append(GRID_LABEL_PX)
    # which way an edge reads: "from" set up the left edge beside each grid
    # row's names (not on the title line, where it read as "from c1 ..."),
    # "to" beside the band of column names
    for ym in (y_m1, y_m2):
        fy = ym + M / 2
        svg.text(14, fy, "from", "sm", anchor="middle",
                 extra=f' font-style="italic" transform="rotate(-90 14 {fy:.1f})"')
    svg.text(GX, yc + 5, "to", "sm", anchor="end", extra=' font-style="italic"')

    # the key: the four greys and the outline
    kx, ky = COLS[1] + M + 26, y_m1
    svg.text(kx, ky + 12, "attack flows", "sm")
    sw = 17
    for k, (_lo, _hi, lab, col) in enumerate(BINS):
        yy = ky + 26 + k * 25
        svg.rect(kx, yy, sw, sw, col)
        svg.text(kx + sw + 8, yy + 13.5, lab, "tick")
    yy = ky + 26 + 4 * 25 + 14
    svg.add(f'<rect class="obj" x="{kx + 4:.1f}" y="{yy:.1f}" width="{sw * 0.6:.1f}" height="{sw + 8}"/>')
    svg.text(kx + sw + 8, yy + 18, "objective", "tick")

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>fig:attack-profiles --- the attack graph split by objective (generated by tools/ch4_attack_profiles_figure.py; do not hand-edit)</title>
<style>{STYLE}
  body {{ width:{PX}px; }}
  @media print {{ @page {{ size:{WIDTH_CM}cm {WIDTH_CM * height / PX:.3f}cm; margin:0; }} body {{ width:{WIDTH_CM}cm; }} svg {{ width:{WIDTH_CM}cm; height:{WIDTH_CM * height / PX:.3f}cm; }} }}
</style></head>
<body>
<svg id="fig" viewBox="0 0 {PX} {height:.1f}" width="{PX}" height="{height:.1f}" xmlns="http://www.w3.org/2000/svg">
{chr(10).join(svg.parts)}
</svg>
</body></html>
"""
    floor = min(svg.sizes) * (WIDTH_CM / 2.54 * 72) / PX / FACE_SCALE
    return html, WIDTH_CM * height / PX, floor


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR, help="mocks go to the scratchpad, not the thesis")
    ap.add_argument("--stem", default=STEM)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    gap, gap_order = load_gap()
    axis = load_axis()
    axis.check_against(gap_order)
    cls = load_classes()
    prof = profiles(gap, cls)
    net = cross_check(prof)

    html, h_cm, floor = emit(prof, axis)
    if floor < FLOOR_PT:
        raise SystemExit(f"smallest type prints at {floor:.2f} pt (< {FLOOR_PT} pt floor)")
    a.out_dir.mkdir(parents=True, exist_ok=True)
    html_path = a.out_dir / f"{a.stem}.html"
    html_path.write_text(html)
    print(f"wrote {html_path}")
    h_px = round(PX * h_cm / WIDTH_CM)
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

    # the facts, for the caption and the prose (the aggregate: read and checked, not drawn)
    order = axis.matrix_order
    print("--- facts")
    for p in PANELS:
        flows, T = prof[p]
        fwd = sum(1 for (s, d) in T if order.index(s) < order.index(d))
        bins = Counter(next(lab for lo, hi, lab, _ in BINS if lo <= len(v) <= hi) for v in T.values())
        tactics = {t for key in T for t in key}
        code = "c_agg" if p == AGG else f"c{PROFILE_CODE[p]}"
        r = net[p]
        print(f"  {code:5s} {len(flows):2d} flows | {len(T):3d} tactic edges ({fwd} forward, {len(T) - fwd} backward) "
              f"over {len(tactics)} tactics | max {max(len(v) for v in T.values())} flows on one edge | "
              + ", ".join(f"{lab}: {bins.get(lab, 0)}" for *_, lab, _c in BINS)
              + f" | Petri net: {r['net']} transitions = {r['backed']} flow-backed (= the edges, same flows) + {r['zero']} zero-weight"
              f" ({r['zero_dedup']} zero under operator_dedup), {r['places']} places")
    print(f"  {WIDTH_CM} x {h_cm:.2f} cm; smallest type {floor:.2f} pt nominal")


if __name__ == "__main__":
    main()
