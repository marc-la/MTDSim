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
    drawn in Figure 4.4's marks (no key: Figure 4.4, the page before, carries
    it, and the caption points there); the three declared inputs as
    boxes, named as the subsection headings name them, with the subsection
    number (4.4.1 to 4.4.3), left to right in subsection order; MTDSim, its
    three modules and icons as Figure 2.1 draws them (Attacker, Network, MTD,
    in Figure 2.1's order, so every step drops straight into the Attacker),
    with the vulnerability memory (4.4.4) inside the Attacker;
  * one colour, one meaning (round 3, Marc: "we're tracking dark blue, black
    and dark grey"; "three different meanings for arrows"): blue is the loop
    and nothing else --- the six numbered steps and the arc the token fires,
    so the eye follows one colour round the loop; everything else is ink, and
    the boxes are outlined in ink (in this figure everything above MTDSim is
    built, so a "built" colour told the reader nothing);
  * arrows of two kinds only: the loop's steps (blue, heavy, numbered) and the
    Petri net's arcs (ink, thin, the marks of Figure 4.4); MTDSim's own
    couplings (compromises, reconfigures, disrupts) are not drawn: they are
    Figure 4.1's and Figure 2.1's, not the loop's;
  * step 5 returns to the decision place, where the next tactic is chosen,
    so the blue path runs unbroken from the failure matrix to step 6, which
    sits on the arc it fires;
  * one grid, two lanes (round 2, Marc: "visually overwhelming ... things are
    not really aligned"): what goes down runs on the left, what comes back up
    on the right, the closed-loop convention; each box sits under the element
    of the net it acts on (the failure matrix under the immediate transitions
    it reweights, the verdict's success arm under the decision place); every
    arrow is one straight vertical, bar step 1's fork and the failure arm's
    one turn; one box width; box names at label size, not title size;
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
  .frame  {{ fill:none; stroke:{INK2}; stroke-width:1.4; }}
  .arc    {{ stroke:{INK}; stroke-width:1.4; fill:none; }}
  .loop   {{ stroke:{ACCENT}; stroke-width:2.4; fill:none; }}
  .pl     {{ fill:#fff; stroke:{INK}; stroke-width:1.8; }}
  .dpl    {{ fill:#fff; stroke:{INK}; stroke-width:1.8; stroke-dasharray:4 3; }}
  .timed  {{ fill:#fff; stroke:{INK}; stroke-width:1.8; }}
  .imm    {{ fill:{INK}; stroke:none; }}
  .tok    {{ fill:{INK}; stroke:none; }}
  .badge  {{ fill:#fff; stroke:{ACCENT}; stroke-width:1.8; }}
  .bnum   {{ font-size:15.5px; font-weight:bold; fill:{ACCENT}; }}
  .dot    {{ fill:{ACCENT}; stroke:none; }}
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
    """One grid, two lanes, one colour. Columns: C1 dwell, C2 mapping (the down
    lane, both fed by step 1 from the token's place, midway over them); C3 the
    decision place and the verdict's success arm; C4 the immediate transitions
    and the failure matrix under them (the up lane). Blue is the loop and
    nothing else: the six steps and the arc the token fires; every other
    line is ink."""
    svg = SVG()
    X0, X1 = 8, 892
    C1, C2, C3, C4 = 126, 360, 540, 666
    BOLD = ' font-weight="bold"'

    # ------------------------------------------------------------ Petri net
    py0, py1 = 8, 166
    svg.rect(X0, py0, X1, py1, "frame", rx=7)
    svg.text(X0 + 16, py0 + 28, "Petri net", "title", anchor="start")
    svg.text(X0 + 108, py0 + 28, "§4.3", "xref", anchor="start")
    yc = 96                                    # the net's axis
    xp = (C1 + C2) / 2                         # the token's place, over the fork
    xt = (xp + C3) / 2                         # its timed transition
    xd, xb, xq = C3, C4, C4 + 52               # decision place; immediate transitions; successors
    rp, rq, rd = 20, 16, 18
    ys = [yc - 40, yc, yc + 40]
    svg.add(f'<circle class="pl" cx="{xp}" cy="{yc}" r="{rp}"/>')
    svg.add(f'<circle class="tok" cx="{xp}" cy="{yc}" r="6"/>')
    svg.text(xp - rp - 10, yc + 6, "Initial access", "lbl", anchor="end")
    svg.add(f'<rect class="timed" x="{xt - 6}" y="{yc - 20}" width="12" height="40"/>')
    svg.add(f'<circle class="dpl" cx="{xd}" cy="{yc}" r="{rd}"/>')
    svg.path(f"M{xp + rp + 2},{yc} H{xt - 9}", "arc", marker="mS")
    svg.path(f"M{xt + 7},{yc} H{xd - rd - 3}", "arc", marker="mS")
    for k, (y, name) in enumerate(zip(ys, succ)):
        cls, mk = ("loop", "mA") if k == 0 else ("arc", "mS")   # step 6 fires the first
        dx, dy = xb - 4 - xd, y - yc
        L = (dx * dx + dy * dy) ** 0.5
        svg.path(f"M{xd + rd * dx / L:.1f},{yc + rd * dy / L:.1f} L{xb - 6},{y}", cls, marker=mk)
        svg.add(f'<rect class="imm" x="{xb - 3}" y="{y - 14}" width="6" height="28"/>')
        svg.path(f"M{xb + 4},{y} H{xq - rq - 3}", cls, marker=mk)
        svg.add(f'<circle class="pl" cx="{xq}" cy="{y}" r="{rq}"/>')
        svg.text(xq + rq + 8, y + 6, name, "lbl", anchor="start")
    # step 6 sits on the arc it fires
    bx, by = xd + (xb - xd) * 0.45, yc + (ys[0] - yc) * 0.45
    badge(svg, bx, by, 6)
    svg.text(bx - 18, by - 10, "next tactic", "verb halo", anchor="end")

    # ------------------------------------------------------------ the three declared inputs
    iy0, iy1 = 224, 280
    HW = 110                                   # one width for the three boxes
    for cx, name, sec in ((C1, "Tactic dwell times", "§4.4.1"),
                          (C2, "Tactic-to-action mapping", "§4.4.2"),
                          (C4, "Failure matrix", "§4.4.3")):
        svg.rect(cx - HW, iy0, cx + HW, iy1, "node")
        svg.text(cx, iy0 + 24, name, "lbl", extra=BOLD)
        svg.text(cx, iy0 + 45, sec, "xref")

    # step 1: the tactic leaves the Petri net, to both boxes that read it
    fy = 198
    svg.add(f'<path class="loop" d="M{xp},{yc + rp + 2} V{fy}"/>')
    svg.add(f'<path class="loop" d="M{C1},{fy} H{C2}"/>')
    svg.add(f'<circle class="dot" cx="{xp}" cy="{fy}" r="3.5"/>')
    for x in (C1, C2):
        svg.path(f"M{x},{fy} V{iy0 - 3}", "loop", marker="mA")
    step_label(svg, xp, 152, 1, "tactic")

    # ------------------------------------------------------------ MTDSim
    my0, my1 = 340, 510
    svg.rect(X0, my0, X1, my1, "used", rx=7)
    svg.text(X0 + 16, my0 + 28, "MTDSim", "title", anchor="start")
    at = (16, 600, my0 + 34, my1 - 14)                    # Attacker
    svg.rect(at[0], at[2], at[1], at[3], "module")
    act = (32, 584, at[2] + 14, at[2] + 50)               # attack actions
    svg.rect(act[0], act[2], act[1], act[3], "inner", rx=4)
    svg.text((act[0] + act[1]) / 2, act[2] + 24, "attack actions", "lbl")
    vm = (324, 584, act[3] + 14, act[3] + 46)             # the vulnerability memory
    svg.rect(vm[0], vm[2], vm[1], vm[3], "inner", rx=4)
    svg.text(vm[0] + 14, vm[2] + 22, "+ vulnerability memory", "lbl", anchor="start")
    svg.text(vm[1] - 12, vm[2] + 22, "§4.4.4", "xref", anchor="end")
    svg.add(f'<g transform="translate({at[0] + 30},{vm[2] + 15})"><use href="#hacker"/></g>')
    svg.text(at[0] + 50, vm[2] + 22, "Attacker", "lbl", anchor="start", extra=BOLD)
    # Network and MTD, named as Figure 4.1 names them; their couplings are
    # Figure 4.1's, not the loop's, so none is drawn here
    for (y0, y1), icon, title, w in (((act[2] - 4, act[3] + 4), "netic", "Network", 70),
                                     ((vm[2] - 4, vm[3] + 4), "mtdic", "MTD", 40)):
        x0, x1 = 640, 876
        svg.rect(x0, y0, x1, y1, "module")
        cx, cy = (x0 + x1) / 2 - w / 2 + 6, (y0 + y1) / 2
        svg.add(f'<g transform="translate({cx - 22:.1f},{cy}) scale(0.85)"><use href="#{icon}"/></g>')
        svg.text(cx, cy + 6, title, "lbl", anchor="start", extra=BOLD)

    # the down lane: steps 2 and 3 into the attack actions
    ly = 316
    for x, n, words in ((C1, 2, "dwell time"), (C2, 3, "attack action")):
        svg.path(f"M{x},{iy1 + 3} V{act[2] - 4}", "loop", marker="mA")
        step_label(svg, x, ly, n, words)

    # the up lane: step 4, the verdict, splits; success goes straight to the
    # decision place, failure through the failure matrix, whose reweighted
    # weights (5) reach the decision place too
    jy, my = 310, 186
    svg.add(f'<path class="loop" d="M{C3},{act[2]} V{jy}"/>')
    svg.add(f'<circle class="dot" cx="{C3}" cy="{jy}" r="3.5"/>')
    step_label(svg, C3, my0 + 28, 4, "verdict")
    svg.path(f"M{C3},{jy} V{yc + rd + 3}", "loop", marker="mA")
    svg.text(C3 - 10, iy0 - 14, "success", "verb halo", anchor="end")
    svg.path(f"M{C3},{jy} H{C4} V{iy1 + 3}", "loop", marker="mA")
    svg.text((C3 + C4) / 2 + 8, jy - 10, "failure", "verb halo")
    svg.add(f'<path class="loop" d="M{C4},{iy0} V{my} H{C3}"/>')
    svg.add(f'<circle class="dot" cx="{C3}" cy="{my}" r="3.5"/>')
    step_label(svg, C4, (my + iy0) / 2 + 6, 5, "reweights")

    height = my1 + 8
    head = 'viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="13" markerHeight="13" orient="auto-start-reverse"'
    small = 'viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="10" orient="auto"'
    defs = f"""<defs>
  <marker id="mA" {head}><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>
  <marker id="mS" {small}><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>
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
