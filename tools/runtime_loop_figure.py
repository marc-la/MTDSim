#!/usr/bin/env python3
"""Dissertation figure: the headline of section 4.4 (fig:runtime-loop) --- the
Petri net integrated with MTDSim, as boxes and the six numbered steps of one
iteration of the loop.

Rebuilt 2026-10-04 (Marc: section 4.4 is the "integrate with MTDSim" arrow of
Figure 4.1, enlarged, so it is drawn as a sub-model diagram in Figure 4.1's
boxes; "the big point of this is the arrows and the numbering"). Replaces the
TikZ drawing of 2026-09-08, whose three glyphs (dwell bars, mapping lines,
matrix heat map) were thumbnails of floats the subsections already show, whose
Petri-net fragment dropped the decision place and had no key, and whose
colour carried no single meaning. Prior generator in git (c25d05a5).

The rules it keeps (as tools/ch4_overview_figure.py, its sibling):

  * three groups, one per band, top to bottom: the Petri net (section 4.3),
    drawn in Figure 4.4's marks with a key; the three declared inputs as
    boxes, named as the subsection headings name them, with the subsection
    number (4.4.1 to 4.4.3), left to right in subsection order; MTDSim, its
    three modules and icons as Figure 2.1 draws them (Attacker, Network, MTD,
    in Figure 2.1's order, so every step drops straight into the Attacker),
    with the vulnerability memory (4.4.4) inside the Attacker;
  * one colour, one meaning, as Figure 4.1: a blue outline marks what this
    dissertation builds; all text is ink; the token is ink, as in Figure 4.4;
  * arrows: the loop's steps in ink, each with its number and one word;
    MTDSim's own couplings in grey, as Figures 2.1 and 4.1;
  * no data drawn: the boxes are named, not pictured; the subsections hold
    the values.

The Petri net is the one Figure 4.4(b) draws: initial access in c1, with the
three successors of largest base weight (read from the routing net, never
typed). Step 6 is drawn on the first of them.

Printed through Chromium like the other SVG figures (figure_table_conventions
§(n)), at \\textwidth.

Usage:
  PYTHONPATH=src python tools/runtime_loop_figure.py
      [--out-dir DIR] [--stem STEM] [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tools"))
from _tactic_axis import load_axis  # noqa: E402
from ch4_overview_figure import (  # noqa: E402  one style, one icon set, one type scale
    ACCENT, FACE_SCALE, FLOOR_PT, ICONS, INK, INK2, PX, STYLE, SVG, WIDTH_CM,
)
from mtdsim.l3_simulation.movement.net import load_routing_net  # noqa: E402

OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-4c_runtime_loop"
PROFILE, PLACE, N_SUCC = "objective_exfiltration", "initial-access", 3

EXTRA_STYLE = f"""
  .arc    {{ stroke:{INK2}; stroke-width:1.6; fill:none; }}
  .arcOn  {{ stroke:{INK}; stroke-width:2.4; fill:none; }}
  .pl     {{ fill:#fff; stroke:{INK}; stroke-width:1.8; }}
  .dpl    {{ fill:#fff; stroke:{INK}; stroke-width:1.8; stroke-dasharray:4 3; }}
  .timed  {{ fill:#fff; stroke:{INK}; stroke-width:1.8; }}
  .imm    {{ fill:{INK}; stroke:none; }}
  .tok    {{ fill:{INK}; stroke:none; }}
  .step   {{ stroke:{INK}; stroke-width:2; fill:none; }}
  .badge  {{ fill:#fff; stroke:{INK}; stroke-width:1.5; }}
  .bnum   {{ font-size:15.5px; font-weight:bold; fill:{INK}; }}
  .dot    {{ fill:{INK}; stroke:none; }}
"""


def badge(svg: SVG, x: float, y: float, n: int) -> None:
    """A step number: a circled numeral, big enough to be found."""
    svg.add(f'<circle class="badge" cx="{x:.1f}" cy="{y:.1f}" r="12"/>')
    svg.sizes.append(15.5)
    svg.add(f'<text class="bnum" x="{x:.1f}" y="{y + 5.5:.1f}" text-anchor="middle">{n}</text>')


def step_label(svg: SVG, x: float, y: float, n: int, words: str, side: str = "right") -> None:
    """Badge plus its one word, beside an arrow; `side` is where the pair sits."""
    if side == "right":
        badge(svg, x + 12, y - 6, n)
        svg.text(x + 30, y, words, "verb halo", anchor="start")
    else:
        svg.text(x - 30, y, words, "verb halo", anchor="end")
        badge(svg, x - 12, y - 6, n)


def emit(succ: list[str]) -> tuple[str, float, float]:
    svg = SVG()
    X0, X1 = 8, 892

    # ------------------------------------------------------------ Petri net
    py0, py1 = 8, 226
    svg.rect(X0, py0, X1, py1, "built", rx=7)
    svg.text(X0 + 16, py0 + 28, "Petri net", "title", anchor="start")
    svg.text(X0 + 108, py0 + 28, "§4.3", "xref", anchor="start")

    # the key, Figure 4.4's marks and words, down the band's left edge
    kx, ky = 40, py0 + 62
    key = (("pl", "place"), ("dpl", "decision place"), ("timed", "timed transition"),
           ("imm", "immediate transition"), ("tok", "token"))
    for k, (cls, words) in enumerate(key):
        y = ky + 27 * k
        if cls in ("pl", "dpl"):
            svg.add(f'<circle class="{cls}" cx="{kx}" cy="{y}" r="9"/>')
        elif cls == "timed":
            svg.add(f'<rect class="timed" x="{kx - 4}" y="{y - 10}" width="8" height="20"/>')
        elif cls == "imm":
            svg.add(f'<rect class="imm" x="{kx - 2.5}" y="{y - 10}" width="5" height="20"/>')
        else:
            svg.add(f'<circle class="tok" cx="{kx}" cy="{y}" r="5"/>')
        svg.text(kx + 20, y + 5.5, words, "sm", anchor="start")

    yc = 108                                   # the net's axis
    xp, xt, xd, xb, xq = 300, 440, 590, 668, 714
    rp, rq = 20, 16
    ys = [yc - 52, yc, yc + 52]                # successor rows
    # the token's place
    svg.add(f'<circle class="pl" cx="{xp}" cy="{yc}" r="{rp}"/>')
    svg.add(f'<circle class="tok" cx="{xp}" cy="{yc}" r="6"/>')
    svg.text(xp, yc + rp + 22, "Initial access", "lbl")
    # its timed transition and decision place
    svg.add(f'<rect class="timed" x="{xt - 6}" y="{yc - 20}" width="12" height="40"/>')
    svg.add(f'<circle class="dpl" cx="{xd}" cy="{yc}" r="18"/>')
    svg.path(f"M{xp + rp + 2},{yc} H{xt - 9}", "arc", marker="mS")
    svg.path(f"M{xt + 7},{yc} H{xd - 21}", "arc", marker="mS")
    # immediate transitions and successor places; step 6 fires the first
    for k, (y, name) in enumerate(zip(ys, succ)):
        on = k == 0
        cls, mk = ("arcOn", "mSk") if on else ("arc", "mS")
        dx, dy = xb - 4 - xd, y - yc
        L = (dx * dx + dy * dy) ** 0.5
        sx, sy = xd + 18 * dx / L, yc + 18 * dy / L
        svg.path(f"M{sx:.1f},{sy:.1f} L{xb - 6},{y}", cls, marker=mk)
        svg.add(f'<rect class="imm" x="{xb - 3}" y="{y - 16}" width="6" height="32"/>')
        svg.path(f"M{xb + 4},{y} H{xq - rq - 3}", cls, marker=mk)
        svg.add(f'<circle class="pl" cx="{xq}" cy="{y}" r="{rq}"/>')
        svg.text(xq + rq + 8, y + 6, name, "lbl", anchor="start")
    badge(svg, (xd + xb) / 2 - 8, ys[0] + 6, 6)

    # ------------------------------------------------------------ the three declared inputs
    iy0, iy1 = 268, 348
    boxes = {"dwell": (30, 250), "map": (290, 480), "fm": (640, 880)}
    for key_, lines, sec in (("dwell", ["Tactic dwell times"], "§4.4.1"),
                             ("map", ["Tactic-to-action", "mapping"], "§4.4.2"),
                             ("fm", ["Failure matrix"], "§4.4.3")):
        x0, x1 = boxes[key_]
        svg.rect(x0, iy0, x1, iy1, "nodeA")
        cx = (x0 + x1) / 2
        top = (iy0 + iy1) / 2 - 10 * len(lines) + (1 if len(lines) == 1 else 2)
        for k, ln in enumerate(lines):
            svg.text(cx, top + 21 * k, ln, "title")
        svg.text(cx, top + 21 * len(lines) + 4, sec, "xref")
    xdw = sum(boxes["dwell"]) / 2
    xmp = sum(boxes["map"]) / 2
    xfm = sum(boxes["fm"]) / 2

    # step 1: the tactic leaves the Petri net, to both boxes that read it
    fy = 246
    svg.path(f"M{xp},{yc + rp + 32} V{fy}", "step", marker="")
    svg.add(f'<path class="step" d="M{xdw},{fy} H{xmp}"/>')
    svg.add(f'<circle class="dot" cx="{xp}" cy="{fy}" r="3.5"/>')
    for x in (xdw, xmp):
        svg.path(f"M{x},{fy} V{iy0 - 3}", "step", marker="mI")
    step_label(svg, xp, 200, 1, "tactic")

    # ------------------------------------------------------------ MTDSim
    my0, my1 = 424, 632
    svg.rect(X0, my0, X1, my1, "used", rx=7)
    svg.text(X0 + 16, my0 + 28, "MTDSim", "title", anchor="start")
    # Attacker, Figure 2.1's order: Attacker, Network, MTD
    at = (24, 618, my0 + 40, my1 - 14)
    svg.rect(at[0], at[2], at[1], at[3], "module")
    act = (120, 604, at[2] + 20, at[2] + 60)              # attack actions
    svg.rect(act[0], act[2], act[1], act[3], "inner", rx=4)
    svg.text((act[0] + act[1]) / 2, act[2] + 26, "attack actions", "lbl")
    vm = (300, 560, act[3] + 18, act[3] + 58)             # the vulnerability memory, ours
    svg.rect(vm[0], vm[2], vm[1], vm[3], "peer", rx=4)
    svg.text((vm[0] + vm[1]) / 2 - 22, vm[2] + 26, "+ vulnerability memory", "lbl")
    svg.text(vm[1] - 12, vm[2] + 26, "§4.4.4", "xref", anchor="end")
    svg.add(f'<g transform="translate({at[0] + 30},{at[3] - 28})"><use href="#hacker"/></g>')
    svg.text(at[0] + 50, at[3] - 21, "Attacker", "title", anchor="start")
    # Network and MTD, the right-hand column
    nw = (720, 880, act[2] - 6, act[3] + 6)                # on the attack actions' line
    md = (720, 880, at[3] - 48, at[3])                     # room between for 'reconfigures'
    for (x0, x1, y0, y1), icon, title, w in ((nw, "netic", "Network", 76), (md, "mtdic", "MTD", 44)):
        svg.rect(x0, y0, x1, y1, "module")
        cx, cy = (x0 + x1) / 2 - w / 2 + 6, (y0 + y1) / 2
        svg.add(f'<g transform="translate({cx - 22:.1f},{cy})"><use href="#{icon}"/></g>')
        svg.text(cx, cy + 7, title, "title", anchor="start")
    ya = (act[2] + act[3]) / 2
    svg.path(f"M{act[1] + 3},{ya} H{nw[0] - 4}", "couples", marker="mG")
    svg.text((at[1] + nw[0]) / 2, ya - 10, "compromises", "sm halo")
    xr = (md[0] + md[1]) / 2
    svg.path(f"M{xr},{md[2] - 2} V{nw[3] + 4}", "couples", marker="mG")
    svg.text(xr - 10, (nw[3] + md[2]) / 2 + 6, "reconfigures", "sm halo", anchor="end")
    ymd = (md[2] + md[3]) / 2
    svg.path(f"M{md[0] - 3},{ymd} H{at[1] + 4}", "couples", marker="mG")
    svg.text((at[1] + md[0]) / 2, ymd - 10, "disrupts", "sm halo")

    # steps 2 and 3: down into the attack actions
    svg.path(f"M{xdw},{iy1 + 3} V{act[2] - 4}", "step", marker="mI")
    step_label(svg, xdw, 396, 2, "dwell time")
    svg.path(f"M{xmp},{iy1 + 3} V{act[2] - 4}", "step", marker="mI")
    step_label(svg, xmp, 396, 3, "attack action")

    # step 4: the verdict, up out of the attack actions; failure through the
    # failure matrix, success straight to the choice
    xv, jy = xd, 388
    svg.add(f'<path class="step" d="M{xv},{act[2]} V{jy}"/>')
    svg.add(f'<circle class="dot" cx="{xv}" cy="{jy}" r="3.5"/>')
    step_label(svg, xv, 450, 4, "verdict")
    svg.path(f"M{xv},{jy} H{xfm} V{iy1 + 3}", "step", marker="mI")
    svg.text((xv + xfm) / 2 + 10, jy - 10, "failure", "verb halo")
    # step 5: the weights reach the decision place, from either arm
    my = 246
    svg.add(f'<path class="step" d="M{xv},{jy} V{my}"/>')
    svg.text(xv - 10, (iy0 + iy1) / 2 + 6, "success", "verb halo", anchor="end")
    svg.add(f'<path class="step" d="M{xfm},{iy0} V{my} H{xv}"/>')
    svg.add(f'<circle class="dot" cx="{xv}" cy="{my}" r="3.5"/>')
    svg.path(f"M{xv},{my} V{yc + 21}", "step", marker="mI")
    step_label(svg, xv, 190, 5, "weights")

    height = my1 + 8
    head = 'viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"'
    small = 'viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"'
    defs = f"""<defs>
  <marker id="mI" {head}><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
  <marker id="mG" {head}><path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker>
  <marker id="mS" {small}><path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker>
  <marker id="mSk" {small}><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
{ICONS}
</defs>"""
    h_cm = WIDTH_CM * height / PX
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>fig:runtime-loop --- the Petri net integrated with MTDSim (generated by tools/runtime_loop_figure.py; do not hand-edit)</title>
<style>{STYLE}{EXTRA_STYLE}
  body {{ width:{PX}px; }}
  @media print {{ @page {{ size:{WIDTH_CM}cm {h_cm:.3f}cm; margin:0; }} body {{ width:{WIDTH_CM}cm; }} svg {{ width:{WIDTH_CM}cm; height:{h_cm:.3f}cm; }} }}
</style></head>
<body>
<svg id="fig" viewBox="0 0 {PX} {height}" width="{PX}" height="{height}" xmlns="http://www.w3.org/2000/svg">
{defs}
{chr(10).join(p.replace('marker-end="url(#)"', '') for p in svg.parts)}
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

    axis = load_axis()
    net = load_routing_net(PROFILE, with_synthetic_overlay=True)
    base = net.base_out_weights(PLACE)
    top = sorted((q for q, w in base.items() if w > 0),
                 key=lambda q: (-base[q], axis.matrix_order.index(q)))[:N_SUCC]
    succ = [axis.label[q] for q in top]
    html, h_cm, floor = emit(succ)
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
            # every text inside the figure's width: nothing clipped at the right edge
            right = pg.evaluate("Math.max(...[...document.querySelectorAll('text')].map(t => t.getBBox().x + t.getBBox().width))")
            if right > PX - 4:
                raise SystemExit(f"text runs to x={right:.0f} px, past the figure's width")
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
    print(f"--- facts: {PROFILE} {PLACE}; successors drawn {succ} of {sum(1 for w in base.values() if w > 0)}; "
          f"{WIDTH_CM} x {h_cm:.2f} cm; smallest type {floor:.2f} pt nominal; rightmost text {right:.0f} px")


if __name__ == "__main__":
    main()
