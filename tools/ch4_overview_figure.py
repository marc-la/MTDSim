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
  <g id="hacker"><path class="icon f" d="M-10,13 C-10,4 -5,-1 0,-1 C5,-1 10,4 10,13 Z"/><path class="icon f" d="M-7,-3 C-7,-12 -4,-15 0,-15 C4,-15 7,-12 7,-3 C5,-4 3,-5 0,-5 C-3,-5 -5,-4 -7,-3 Z"/><path d="M-4,-3 C-2,-1 2,-1 4,-3 C3,0 -3,0 -4,-3 Z" fill="#fff"/></g>
  <g id="netic"><circle class="icon" cx="-9" cy="-6" r="3.6"/><circle class="icon" cx="9" cy="-6" r="3.6"/><circle class="icon" cx="0" cy="9" r="3.6"/><path class="icon" d="M-6,-4.5 L-2.4,7 M6,-4.5 L2.4,7 M-5.4,-6 H5.4"/></g>
  <g id="shieldic"><path class="icon" d="M0,-14 L11,-9 V0 C11,7 6,12 0,14 C-6,12 -11,7 -11,0 V-9 Z"/><path class="icon" d="M-4.5,0 L-1,3.5 L5,-3.5"/></g>"""

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
    d = (26, 186)                            # Defence
    nw = (266, 426)                          # Network
    at = (536, 882)                          # Attacker
    for (x0, x1), icon, title, sub in ((d, "shieldic", "Defence", "defence mechanisms"),
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
    act = (at[0] + 16, at[0] + 106)
    ay = (iy0 + 56, iy0 + 96)
    ayc = (ay[0] + ay[1]) / 2
    svg.rect(act[0], ay[0], act[1], ay[1], "inner", rx=4)
    svg.text(sum(act) / 2, ayc + 6, "actions", "lbl")
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

    # Figure 2.1's couplings, grey: the defence rewrites the network, the actions compromise it
    cy2 = (iy0 + iy1) / 2 + 10
    svg.path(f"M{d[1] + 3},{cy2} H{nw[0] - 4}", "couples", marker="mG")
    svg.text((d[1] + nw[0]) / 2, cy2 - 10, "rewrites", "sm halo")
    svg.path(f"M{act[0] - 3},{ayc + 8} L{nw[1] + 4},{cy2}", "couples", marker="mG")
    svg.text((nw[1] + at[0]) / 2, cy2 + 26, "compromises", "sm halo")

    # Figure 2.1's fourth coupling: each rewrite interrupts the attacker mid-action
    # (the way MTD holds an attacker back), routed under the modules as there
    ly = iy1 + 22
    svg.path(f"M{sum(d) / 2},{iy1 + 2} V{ly} H{(at[0] + act[1]) / 2} V{iy1 + 5}", "couples", marker="mG")
    svg.text((d[1] + at[0]) / 2 + 40, ly - 6, "interrupts", "sm halo")

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
