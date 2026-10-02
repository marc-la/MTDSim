#!/usr/bin/env python3
"""Dissertation figure: the chapter 4 head figure (fig:pipeline) --- the method
in one picture, as boxes and how they link.

Designed 2026-09-25 from the Figure 4.1 scrutiny (the E8 handoff,
docs/handoffs/2026-09-22_ch4_overview_figure_family.md, Part A). Replaces the
worked-example ladder (tools/pipeline_ladder_figure.py, which becomes the
source of the section 4.1 zoom). The rules it keeps, each from the design
reference (.claude/skills/scrutinise-figure/diagram_best_practice.md):

  * four groups only: the input; what this dissertation builds (framed, the
    one accent); MTDSim (framed as existing, drawn as Figure 2.1 draws it:
    Attacker, Network, Defence); the output;
  * artefacts are boxes, processes are the arrows between them, labelled with
    the introduction's verbs and the section that describes them (the way
    Figure 2.1 names the figure that opens each module);
  * two arrow kinds: BECOMES (thin, ink) and DRIVES (heavy: the join in the
    accent, the baseline attacker in ink); nothing else is an arrow;
  * no data drawn, no legend; the only counts are the corpus size and the
    profiles' objective classes, both read from the artefacts below.

Sibling of fig:mtdsim-model (tools/ch2_fig21_mtdsim_model.html): same width
(900 px -> \\textwidth), type classes, palette and icons, so the MTDSim row
reads as Figure 2.1 zoomed out. Printed through Chromium like the other SVG
figures (figure_table_conventions.md §(n)).

Layout: the built row above MTDSim, the metrics below (the scrutiny's
round 1 chose it over a compact U whose leftward "measure" arrow ended the
method under its input). MTDSim's modules run mirror-wise to Figure 2.1 so the
join drops straight into the Attacker module.

Usage:
  PYTHONPATH=src python tools/ch4_overview_figure.py 
      [--out-dir DIR] [--stem STEM] [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from pipeline_ladder_figure import (  # noqa: E402  the artefact readers and drift guards
    PROFILE_ORDER, flow_graphs, load_classes, load_gap,
)

OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-0a_method_overview"
WIDTH_CM = 16.058          # \textwidth, measured (455.244 pt); as ch2_model_figures.py
PX = 900
FACE_SCALE = 0.92
FLOOR_PT = 7.95

INK, INK2, FAINT, CHROME, ACCENT = "#333", "#6e6e6e", "#b0b0b0", "#e6e6e6", "#1f548c"

ICONS = """
  <!-- icons: hooded attacker, wired network, moving target (the attack lands on the target's stale position, dotted; the target has moved, solid); each centred on the origin, ~28 px -->
  <g id="hacker"><g transform="scale(0.062) translate(-256,-256)" fill="#333"><path d="M475.3571,413.24a69.9,69.9,0,0,0-39.8845-57.4407l-39.9287-18.7987,21.5791-44.5621a89.4527,89.4527,0,0,0,.0025-77.9684L359.7988,96.0682C317.7933,9.3105,194.2088,9.31,152.2019,96.0666L94.87,214.4745a89.445,89.445,0,0,0,.0049,77.9692l21.581,44.5569L76.5256,355.8a69.898,69.898,0,0,0-39.8831,57.439l-3.612,43.3773a22.5157,22.5157,0,0,0,22.4381,24.3842H456.5337A22.5134,22.5134,0,0,0,478.97,456.6187ZM364,260.1205a107.9746,107.9746,0,0,1-98.1035,107.5V341.1249a9.8965,9.8965,0,0,0-19.793,0v26.4957A107.9746,107.9746,0,0,1,148,260.1205V203.44a28.8192,28.8192,0,0,1,28.8193-28.8193H335.1806A28.8193,28.8193,0,0,1,364,203.44Z"/><path d="M321.8213,275.9979a9.91,9.91,0,0,0-12.3135,6.6709,13.5776,13.5776,0,0,1-26.0156,0,9.9026,9.9026,0,1,0-18.9844,5.6426,33.3877,33.3877,0,0,0,63.9844,0A9.9125,9.9125,0,0,0,321.8213,275.9979Z"/><path d="M240.8213,275.9979a9.8908,9.8908,0,0,0-12.3135,6.6709,13.5776,13.5776,0,0,1-26.0156,0,9.9026,9.9026,0,1,0-18.9844,5.6426,33.3877,33.3877,0,0,0,63.9844,0A9.9125,9.9125,0,0,0,240.8213,275.9979Z"/><path d="M319,227.4384H283a9.8965,9.8965,0,1,0,0,19.7929h36a9.8965,9.8965,0,1,0,0-19.7929Z"/><path d="M193,247.2313h36a9.8965,9.8965,0,1,0,0-19.7929H193a9.8965,9.8965,0,1,0,0,19.7929Z"/></g></g>
  <g id="netic"><g transform="scale(1.35) translate(-12,-12)" fill="none" stroke="#333" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12H21M12 8V12M6.5 12V16M17.5 12V16M10.1 8H13.9C14.4601 8 14.7401 8 14.954 7.89101C15.1422 7.79513 15.2951 7.64215 15.391 7.45399C15.5 7.24008 15.5 6.96005 15.5 6.4V4.6C15.5 4.03995 15.5 3.75992 15.391 3.54601C15.2951 3.35785 15.1422 3.20487 14.954 3.10899C14.7401 3 14.4601 3 13.9 3H10.1C9.53995 3 9.25992 3 9.04601 3.10899C8.85785 3.20487 8.70487 3.35785 8.60899 3.54601C8.5 3.75992 8.5 4.03995 8.5 4.6V6.4C8.5 6.96005 8.5 7.24008 8.60899 7.45399C8.70487 7.64215 8.85785 7.79513 9.04601 7.89101C9.25992 8 9.53995 8 10.1 8ZM15.6 21H19.4C19.9601 21 20.2401 21 20.454 20.891C20.6422 20.7951 20.7951 20.6422 20.891 20.454C21 20.2401 21 19.9601 21 19.4V17.6C21 17.0399 21 16.7599 20.891 16.546C20.7951 16.3578 20.6422 16.2049 20.454 16.109C20.2401 16 19.9601 16 19.4 16H15.6C15.0399 16 14.7599 16 14.546 16.109C14.3578 16.2049 14.2049 16.3578 14.109 16.546C14 16.7599 14 17.0399 14 17.6V19.4C14 19.9601 14 20.2401 14.109 20.454C14.2049 20.6422 14.3578 20.7951 14.546 20.891C14.7599 21 15.0399 21 15.6 21ZM4.6 21H8.4C8.96005 21 9.24008 21 9.45399 20.891C9.64215 20.7951 9.79513 20.6422 9.89101 20.454C10 20.2401 10 19.9601 10 19.4V17.6C10 17.0399 10 16.7599 9.89101 16.546C9.79513 16.3578 9.64215 16.2049 9.45399 16.109C9.24008 16 8.96005 16 8.4 16H4.6C4.03995 16 3.75992 16 3.54601 16.109C3.35785 16.2049 3.20487 16.3578 3.10899 16.546C3 16.7599 3 17.0399 3 17.6V19.4C3 19.9601 3 20.2401 3.10899 20.454C3.20487 20.6422 3.35785 20.7951 3.54601 20.891C3.75992 21 4.03995 21 4.6 21Z"/></g></g>
  <g id="mtdic"><g transform="scale(1.35) translate(-11.75,-12)" fill="none" stroke="#333" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="16.5" cy="7.5" r="4.5"/><circle cx="16.5" cy="7.5" r="1"/><circle cx="10" cy="16.5" r="4.5" stroke-width="2.2" stroke-dasharray="0.01 3.5343" transform="rotate(22.5 10 16.5)"/><path d="M2.5 9L10 16.5M7 16.5H10V13.5"/></g></g>"""

STYLE = f"""
  html, body {{ margin:0; background:#fff; }}
  svg {{ display:block; font-family: "Nimbus Sans", "TeX Gyre Heros", Helvetica, Arial, sans-serif; }}
  text {{ fill:{INK}; }}
  .title {{ font-size:19px; font-weight:bold; }}
  .lbl   {{ font-size:17px; }}
  .sm    {{ font-size:15.5px; fill:{INK2}; }}
  .xref  {{ font-size:15.5px; fill:{INK2}; font-style:italic; }}
  .verb  {{ font-size:17px; }}
  .acc   {{ fill:{ACCENT}; }}
  .node  {{ fill:#fff; stroke:{INK}; stroke-width:1.6; }}
  .inner {{ fill:#fff; stroke:{INK2}; stroke-width:1.6; }}
  .card  {{ fill:#fff; stroke:{FAINT}; stroke-width:1.3; }}
  .built {{ fill:none; stroke:{ACCENT}; stroke-width:1.8; }}
  .used  {{ fill:#fafafa; stroke:{FAINT}; stroke-width:1.4; }}
  .module {{ fill:#fff; stroke:{INK}; stroke-width:1.6; }}
  .icon  {{ fill:none; stroke:{INK}; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round; }}
  .icon.f {{ fill:{INK}; stroke:none; }}
  .becomes {{ stroke:{INK}; stroke-width:1.8; fill:none; }}
  .becomes.acc {{ stroke:{ACCENT}; }}
  .drives  {{ stroke:{INK2}; stroke-width:2.4; fill:none; }}
  .couples {{ stroke:{INK2}; stroke-width:1.6; fill:none; }}
  .peer  {{ fill:#fff; stroke:{ACCENT}; stroke-width:1.6; }}
  .halo  {{ paint-order:stroke; stroke:#fff; stroke-width:6px; stroke-linejoin:round; }}
"""


class SVG:
    def __init__(self):
        self.parts: list[str] = []
        self.sizes: list[float] = []

    def add(self, s: str):
        self.parts.append(s)

    def text(self, x, y, s, cls="lbl", anchor="middle", extra=""):
        size = {"title": 19, "lbl": 17, "sm": 15.5, "xref": 15.5, "verb": 17}[cls.split()[0]]
        self.sizes.append(size)
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}{extra}>{s}</text>')

    def rect(self, x0, y0, x1, y1, cls, rx=5):
        self.add(f'<rect class="{cls}" x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" rx="{rx}"/>')

    def path(self, d, cls, marker="mI"):
        self.add(f'<path class="{cls}" d="{d}" marker-end="url(#{marker})"/>')


def process_label(svg, x, y_top, lines, section, below_y):
    """A process: its verb (one or two lines) above the arrow, its section below."""
    for k, ln in enumerate(lines):
        svg.text(x, y_top + k * 19, ln, "verb halo", extra=f' style="fill:{ACCENT}"')
    svg.text(x, below_y, section, "xref")


def stack(svg, x0, y0, x1, y1, depth=2):
    """A box with cards behind it: 'several of these' (the flows, the profiles,
    the nets). The one way a count is drawn on this figure."""
    for k in range(depth, 0, -1):
        svg.rect(x0 + 6 * k, y0 - 6 * k, x1 + 6 * k, y1 - 6 * k, "card")
    svg.rect(x0, y0, x1, y1, "node")


def emit(n_flows: int) -> tuple[str, float, float]:
    svg = SVG()
    # ---------------------------------------------------------------- row 1
    ny0, ny1 = 60, 144
    nyc = (ny0 + ny1) / 2
    # the input, outside the built frame: the attack flows were drawn by
    # CTID's analysts, not by this dissertation
    inp = (12, 168)
    stack(svg, inp[0], ny0, inp[1], ny1)
    svg.text(sum(inp) / 2, nyc - 8, f"{n_flows} attack flows", "title")
    svg.text(sum(inp) / 2, nyc + 16, "cyber threat", "sm")
    svg.text(sum(inp) / 2, nyc + 34, "intelligence", "sm")

    # the built frame: the APT attacker model, this dissertation's part
    fx0, fx1, fy0, fy1 = 250, 894, 8, 166
    svg.rect(fx0, fy0, fx1, fy1, "built", rx=7)
    svg.text(fx0 + 16, fy0 + 26, "Building the APT attacker model", "title acc", anchor="start")

    g = (268, 398)          # attack graph
    p = (492, 652)          # attack profiles
    n = (756, 872)          # profile nets
    svg.rect(g[0], ny0, g[1], ny1, "node")
    svg.text(sum(g) / 2, nyc + 6, "Attack graph", "title")
    stack(svg, p[0], ny0, p[1], ny1)
    svg.text(sum(p) / 2, nyc + 6, "Attack profiles", "title")
    stack(svg, n[0], ny0, n[1], ny1)
    svg.text(sum(n) / 2, nyc + 6, "Petri nets", "title")   # Marc 2026-09-25: one term, the Petri net (was "profile net")

    # the three processes inside row 1 (BECOMES)
    for (x0, x1), lines, sec in (((inp[1], g[0]), ["combine"], "§4.1"),
                                 ((g[1], p[0]), ["split by", "objective"], "§4.2"),
                                 ((p[1], n[0]), ["make", "executable"], "§4.3")):
        svg.path(f"M{x0 + 4},{nyc} H{x1 - 4}", "becomes acc", marker="mA")
        xm = (x0 + min(x1, fx0)) / 2 if x0 < fx0 else (x0 + x1) / 2
        top = nyc - 10 - 19 * len(lines) + 4
        process_label(svg, xm, top, lines, sec, nyc + 26)

    # ---------------------------------------------------------------- row 2
    # MTDSim, existing: the three modules of Figure 2.1, mirrored so that the
    # Attacker module sits under the profile nets and the join drops straight in;
    # Figure 2.1's own couplings (rewrites, compromises) in grey
    my0 = fy1 + 62
    iy0 = my0 + 40
    iy1 = iy0 + 140
    my1 = iy1 + 36
    mx0, mx1 = 12, 894
    svg.rect(mx0, my0, mx1, my1, "used", rx=7)
    svg.text(mx0 + 16, my0 + 26, "MTDSim", "title", anchor="start")
    svg.text(mx0 + 16 + 84, my0 + 26, "the simulator of Chapter 2", "xref", anchor="start")
    d = (26, 170)                            # MTD (narrowed 2026-10-02 so the
    nw = (270, 426)                          # Network  "reconfigures" label fits)
    at = (536, 882)                          # Attacker
    for (x0, x1), icon, title, sub in ((d, "mtdic", "MTD", "MTD mechanisms"),
                                       (nw, "netic", "Network", "hosts and services")):
        svg.rect(x0, iy0, x1, iy1, "module")
        cx = (x0 + x1) / 2
        svg.add(f'<g transform="translate({cx - 44:.1f},{iy0 + 30})"><use href="#{icon}"/></g>')
        svg.text(cx - 26, iy0 + 37, title, "title", anchor="start")
        first, rest_ = sub.split(" ", 1)
        svg.text(cx, iy0 + 84, first, "lbl")
        svg.text(cx, iy0 + 104, rest_, "lbl")
    svg.rect(at[0], iy0, at[1], iy1, "module")
    svg.add(f'<g transform="translate({at[0] + 26},{iy0 + 30})"><use href="#hacker"/></g>')
    svg.text(at[0] + 46, iy0 + 37, "Attacker", "title", anchor="start")

    # the two attackers, peers: MTDSim runs one or the other (ch4 opener:
    # "MTDSim can run either the APT attacker model or the baseline attacker");
    # both drive the same actions. The APT attacker model sits under the join.
    ac = sum(n) / 2
    drv = (ac - 58, ac + 58)
    apt = (iy0 + 10, iy0 + 56)
    bas = (iy0 + 86, iy0 + 132)
    svg.rect(drv[0], apt[0], drv[1], apt[1], "peer", rx=4)
    svg.text(ac, apt[0] + 20, "APT attacker", "lbl", extra=f' style="fill:{ACCENT};font-weight:bold"')
    svg.text(ac, apt[0] + 39, "model", "lbl", extra=f' style="fill:{ACCENT};font-weight:bold"')
    svg.text(ac, (apt[1] + bas[0]) / 2 + 6, "or", "lbl", extra=' font-style="italic"')
    svg.rect(drv[0], bas[0], drv[1], bas[1], "inner", rx=4)
    svg.text(ac, bas[0] + 20, "baseline", "lbl", extra=' font-weight="bold"')
    svg.text(ac, bas[0] + 39, "attacker", "lbl", extra=' font-weight="bold"')
    act = (at[0] + 10, at[0] + 112)   # wide enough for "attack actions"
    ay = (iy0 + 56, iy0 + 96)
    ayc = (ay[0] + ay[1]) / 2
    svg.rect(act[0], ay[0], act[1], ay[1], "inner", rx=4)
    svg.text(sum(act) / 2, ayc + 6, "attack actions", "lbl")
    for y in ((apt[0] + apt[1]) / 2, (bas[0] + bas[1]) / 2):
        x0_, y0_, x1_, y1_ = drv[0] - 3, y, act[1] + 5, ayc + (8 if y > ayc else -8)
        L = ((x1_ - x0_) ** 2 + (y1_ - y0_) ** 2) ** 0.5
        k = (L - 13) / L                      # the head (13 px) hangs past the line's end
        svg.path(f"M{x0_},{y0_} L{x0_ + (x1_ - x0_) * k:.1f},{y0_ + (y1_ - y0_) * k:.1f}", "drives", marker="mD")
    # (drive is run-time, drawn in the grey of the other in-simulator relations)
    svg.text((drv[0] + act[1]) / 2 + 6, ayc + 6, "drive", "sm halo")

    # the join: a step of this dissertation (thin, the accent), into the APT attacker model
    svg.path(f"M{ac},{ny1 + 3} V{apt[0] - 4}", "becomes acc", marker="mA")
    svg.text(ac - 14, fy1 + 30, "join to MTDSim", "verb halo", anchor="end", extra=f' style="fill:{ACCENT}"')
    svg.text(ac - 14, fy1 + 48, "one Petri net per run", "sm halo", anchor="end")
    svg.text(ac + 14, fy1 + 30, "§4.4", "xref halo", anchor="start")

    # Figure 2.1's couplings, grey: MTD reconfigures the network, the actions compromise it
    cy2 = (iy0 + iy1) / 2 + 10
    svg.path(f"M{d[1] + 3},{cy2} H{nw[0] - 4}", "couples", marker="mG")
    svg.text((d[1] + nw[0]) / 2, cy2 - 10, "reconfigures", "sm halo")  # registry row 64 (2026-09-30), as Figure 2.1
    svg.path(f"M{act[0] - 3},{ayc + 8} L{nw[1] + 4},{cy2}", "couples", marker="mG")
    svg.text((nw[1] + at[0]) / 2, cy2 + 26, "compromises", "sm halo")

    # Figure 2.1's fourth coupling: each rewrite interrupts the attacker mid-action
    # (the way MTD holds an attacker back), routed under the modules as there
    ly = iy1 + 22
    svg.path(f"M{sum(d) / 2},{iy1 + 2} V{ly} H{(at[0] + act[1]) / 2} V{iy1 + 5}", "couples", marker="mG")
    svg.text((d[1] + at[0]) / 2 + 40, ly - 6, "disrupts", "sm halo")

    # ---------------------------------------------------------------- output
    xm = (at[0] + at[1]) / 2
    oy0, oy1 = my1 + 52, my1 + 52 + 56
    ox0, ox1 = xm - 120, xm + 120
    svg.rect(ox0, oy0, ox1, oy1, "node")
    svg.text(xm, (oy0 + oy1) / 2 - 3, "Evaluation metrics", "title")
    svg.text(xm, (oy0 + oy1) / 2 + 19, "per attacker", "sm")
    svg.path(f"M{xm},{my1 + 3} V{oy0 - 4}", "becomes")
    svg.text(xm + 14, my1 + 22, "measure", "verb halo", anchor="start")
    svg.text(xm + 14, my1 + 41, "§4.5", "xref", anchor="start")
    height = oy1 + 8

    # one arrowhead size for every arrow (markerUnits in user space, so the
    # head does not grow with the line: the auditor's P20 finding, 2026-09-25)
    head = 'viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"'
    defs = f"""<defs>
  <marker id="mI" {head}><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
  <marker id="mA" {head}><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>
  <marker id="mD" viewBox="0 0 10 10" refX="0" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker>
  <marker id="mG" {head}><path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker>
{ICONS}
</defs>"""
    h_cm = WIDTH_CM * height / PX
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>fig:pipeline --- the method in one picture (generated by tools/ch4_overview_figure.py; do not hand-edit)</title>
<style>{STYLE}
  body {{ width:{PX}px; }}
  @media print {{ @page {{ size:{WIDTH_CM}cm {h_cm:.3f}cm; margin:0; }} body {{ width:{WIDTH_CM}cm; }} svg {{ width:{WIDTH_CM}cm; height:{h_cm:.3f}cm; }} }}
</style></head>
<body>
<svg id="fig" viewBox="0 0 {PX} {height}" width="{PX}" height="{height}" xmlns="http://www.w3.org/2000/svg">
{defs}
{chr(10).join(svg.parts)}
</svg>
</body></html>
"""
    floor = min(svg.sizes) * (WIDTH_CM / 2.54 * 72) / PX / FACE_SCALE
    return html, h_cm, floor


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR, help="mocks go to the scratchpad, not the thesis")
    ap.add_argument("--stem", default=STEM)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    # the two counts the figure shows, read from the artefacts, never typed
    gap, _order = load_gap()
    tech, _edges = flow_graphs(gap)
    cls = load_classes()
    if set(cls.values()) != set(PROFILE_ORDER):
        raise SystemExit(f"objective classes drifted: {sorted(set(cls.values()))} vs {PROFILE_ORDER}")
    missing = set(tech) - set(cls)
    if missing:
        raise SystemExit(f"{len(missing)} flows have no objective class")
    html, h_cm, floor = emit(len(tech))
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
    print(f"--- facts: {len(tech)} attack flows; {len(PROFILE_ORDER)} objective classes; "
          f"{WIDTH_CM} x {h_cm:.2f} cm; smallest type {floor:.2f} pt nominal")


if __name__ == "__main__":
    main()
