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

  * three groups, one per band, top to bottom (round 4, Marc: the failure
    matrix is in the formal definition, so why is it outside the net?): the
    extended Petri net of section 4.3, (P, T, I, O, W, M0, F), drawn in
    Figure 4.4's marks (no key: Figure 4.4, the page before, carries it),
    with the two declared inputs that are part of it inside its frame, each
    under the element it sets (the dwell times, W's rates, under the timed
    transition; the failure matrix, F, under the immediate transitions);
    the tactic-to-action mapping, the one declared input outside the net,
    between the net and MTDSim; MTDSim, its three modules and icons as
    Figure 2.1 draws them, sharing a top and a bottom, the Attacker's two
    rows (attack actions; the vulnerability memory, 4.4.4) level with
    Network and MTD;
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
  * the verdict splits once (round 6, Marc: "what happened to the success?"):
    a failure enters the failure matrix, which reweights the immediate
    transitions (5, Equation 4.4); a success goes straight to the decision
    place, which chooses on the base weights; both routes meet at the
    transition step 6 fires, the successor of largest weight after a failure
    (reconnaissance, as Figure 4.4(b)), read from the overlay, never typed;
  * step 3 points up into the timed transition (round 6, Marc: the dwell time
    is the timed transition's delay), as step 5 points up into the immediate
    transitions: each declared input inside the net points at what it sets;
    the attack action runs for that delay, which 4.4's prose states;
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
from mtdsim.l3_simulation.controller.outcome import load_outcome_overlay  # noqa: E402
from mtdsim.l3_simulation.movement.net import load_routing_net  # noqa: E402

OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-4c_runtime_loop"
PROFILE, PLACE, OVERLAY = "objective_exfiltration", "initial-access", "v4_failure_only"

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
    """The extended Petri net of Section 4.3 is (P, T, I, O, W, M0, F): the dwell
    means set the timed transition's delay (W's rates) and the failure matrix
    reweights the immediate transitions (F), so both are drawn INSIDE the Petri
    net's frame, each directly under the element it sets. The tactic-to-action
    mapping is the one declared input outside the net, between it and MTDSim.
    Three lanes, one per column: the place's (1 tactic, the mapping, 2 attack
    action); the timed transition's (3 dwell time); the immediate transitions'
    (4 verdict, a failure, the failure matrix, 5 reweights). A success changes
    no weight, so it has no arrow (round 5: the success arm and both junction
    dots cut; the caption says what a success does). Blue is the loop and nothing
    else; frame titles sit on the frame's border."""
    svg = SVG()
    X0, X1 = 8, 892
    BOLD = ' font-weight="bold"'
    xp, xt, xd, xb = 200, 360, 500, 640        # place, timed transition, decision place, immediate transitions
    xq = xb + 52
    HW, BH = 110, 52                           # box half-width, box height

    def frame(y0, y1, cls, title, tw, xref=None):
        """A frame whose title sits on its top border, the border broken behind
        it; `tw` is the title's set width at 19 px bold (measured in Chromium)."""
        svg.rect(X0, y0, X1, y1, cls, rx=7)
        w = tw + 12 + (44 if xref else 0)
        svg.add(f'<rect x="{X0 + 10}" y="{y0 - 12}" width="{w:.0f}" height="24" fill="#fff"/>')
        svg.text(X0 + 16, y0 + 6, title, "title", anchor="start")
        if xref:
            svg.text(X0 + 16 + tw + 8, y0 + 6, xref, "xref", anchor="start")

    def box(cx, y0, name, sec):
        svg.rect(cx - HW, y0, cx + HW, y0 + BH, "node")
        svg.text(cx, y0 + 22, name, "lbl", extra=BOLD)
        svg.text(cx, y0 + 42, sec, "xref")

    # ------------------------------------------------------------ Petri net
    py0, py1 = 14, 240
    frame(py0, py1, "frame", "Petri net", 76, "§4.3")
    yc = 74
    rp, rq, rd = 20, 15, 18
    ys = [yc - 38, yc, yc + 38]
    CH = len(ys) - 1                           # step 6 fires the successor nearest the failure matrix
    svg.add(f'<circle class="pl" cx="{xp}" cy="{yc}" r="{rp}"/>')
    svg.add(f'<circle class="tok" cx="{xp}" cy="{yc}" r="6"/>')
    svg.text(xp - rp - 10, yc + 6, "Initial access", "lbl", anchor="end")
    svg.add(f'<rect class="timed" x="{xt - 6}" y="{yc - 20}" width="12" height="40"/>')
    svg.add(f'<circle class="dpl" cx="{xd}" cy="{yc}" r="{rd}"/>')
    svg.path(f"M{xp + rp + 2},{yc} H{xt - 9}", "arc", marker="mS")
    svg.path(f"M{xt + 7},{yc} H{xd - rd - 3}", "arc", marker="mS")
    for k, (y, name) in enumerate(zip(ys, succ)):
        cls, mk = ("loop", "mA") if k == CH else ("arc", "mS")
        dx, dy = xb - 4 - xd, y - yc
        L = (dx * dx + dy * dy) ** 0.5
        svg.path(f"M{xd + rd * dx / L:.1f},{yc + rd * dy / L:.1f} L{xb - 6},{y}", cls, marker=mk)
        svg.add(f'<rect class="imm" x="{xb - 3}" y="{y - 13}" width="6" height="26"/>')
        svg.path(f"M{xb + 4},{y} H{xq - rq - 3}", cls, marker=mk)
        svg.add(f'<circle class="pl" cx="{xq}" cy="{y}" r="{rq}"/>')
        svg.text(xq + rq + 8, y + 6, name, "lbl", anchor="start")
    bx, by = xd + (xb - xd) * 0.6, yc + (ys[CH] - yc) * 0.6
    badge(svg, bx, by, 6)
    svg.text(xd + 10, by + 30, "next tactic", "verb halo", anchor="start")

    # the two declared inputs that are part of the net, directly under what they set
    ry0 = py1 - 12 - BH
    box(xt, ry0, "Tactic dwell times", "§4.4.1")
    box(xb, ry0, "Failure matrix", "§4.4.3")
    # the one outside it, between the net and MTDSim
    my0 = py1 + 40
    box(xp, my0, "Tactic-to-action mapping", "§4.4.2")

    # ------------------------------------------------------------ MTDSim
    sy0 = my0 + BH + 40
    rowh, gap, pad = 36, 8, 16
    ay0 = sy0 + pad
    top = (ay0, ay0 + rowh + 8)                # attack actions | Network
    bot = (top[1] + gap, top[1] + gap + rowh + 8)   # Attacker, memory | MTD
    sy1 = bot[1] + 12
    frame(sy0, sy1, "used", "MTDSim", 76)
    at = (16, 680)
    svg.rect(at[0], top[0], at[1], bot[1], "module")
    act = (32, 664, top[0] + 8, top[1] - 4)
    svg.rect(act[0], act[2], act[1], act[3], "inner", rx=4)
    svg.text((act[0] + act[1]) / 2 - 60, (act[2] + act[3]) / 2 + 6, "attack actions", "lbl")
    vm = (404, 664, bot[0] + 4, bot[1] - 8)
    svg.rect(vm[0], vm[2], vm[1], vm[3], "inner", rx=4)
    vmc = (vm[2] + vm[3]) / 2
    svg.text(vm[0] + 14, vmc + 6, "+ vulnerability memory", "lbl", anchor="start")
    svg.text(vm[1] - 12, vmc + 6, "§4.4.4", "xref", anchor="end")
    svg.add(f'<g transform="translate({at[0] + 30},{vmc - 1})"><use href="#hacker"/></g>')
    svg.text(at[0] + 50, vmc + 6, "Attacker", "lbl", anchor="start", extra=BOLD)
    for (y0, y1), icon, title, w in ((top, "netic", "Network", 70), (bot, "mtdic", "MTD", 40)):
        x0, x1 = 720, 876
        svg.rect(x0, y0, x1, y1, "module")
        cx, cy = (x0 + x1) / 2 - w / 2 + 6, (y0 + y1) / 2
        svg.add(f'<g transform="translate({cx - 22:.1f},{cy}) scale(0.8)"><use href="#{icon}"/></g>')
        svg.text(cx, cy + 6, title, "lbl", anchor="start", extra=BOLD)

    lab1, lab2 = (py1 + my0) / 2 + 6, (my0 + BH + sy0) / 2 + 6   # the gaps between frames
    # the place's lane: step 1 down to the mapping, step 2 on to the attack actions
    svg.path(f"M{xp},{yc + rp + 2} V{my0 - 3}", "loop", marker="mA")
    svg.path(f"M{xp},{my0 + BH + 3} V{act[2] - 4}", "loop", marker="mA")
    step_label(svg, xp, lab1, 1, "tactic")
    step_label(svg, xp, lab2, 2, "attack action")
    # the timed transition's lane: step 3, the drawn dwell time is the timed
    # transition's delay (the attack action runs for that time: 4.4's rule)
    svg.path(f"M{xt},{ry0 - 3} V{yc + 23}", "loop", marker="mA")
    step_label(svg, xt, (yc + 20 + ry0) / 2 + 6, 3, "dwell time")
    # the immediate transitions' lane: step 4, the verdict; a failure enters the
    # failure matrix, which reweights the immediate transitions (5)
    jy = py1 + 38                              # the verdict splits, just below the net
    svg.add(f'<path class="loop" d="M{xb},{act[2]} V{jy}"/>')
    svg.add(f'<circle class="dot" cx="{xb}" cy="{jy}" r="3.5"/>')
    step_label(svg, xb, lab2, 4, "verdict")
    svg.path(f"M{xb},{jy} V{ry0 + BH + 3}", "loop", marker="mA")
    svg.text(xb + 12, jy - 10, "failure", "verb halo", anchor="start")
    # success: straight to the decision place, which chooses on the base weights
    svg.path(f"M{xb},{jy} H{xd} V{yc + rd + 3}", "loop", marker="mA")
    svg.text((xd + xb) / 2, jy + 22, "success", "verb halo")
    svg.path(f"M{xb},{ry0} V{ys[-1] + 16}", "loop", marker="mA")
    step_label(svg, xb, (ys[-1] + 13 + ry0) / 2 + 6, 5, "reweights")
    my1 = sy1
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
    # the successors drawn: the two of largest base weight, then the one of
    # largest weight after a failure, which step 6 fires (Figure 4.4(b): after
    # a failure, most of the weight moves to reconnaissance)
    routed = load_outcome_overlay(version=OVERLAY).compose(PLACE, "failure", base)
    order = lambda q: axis.matrix_order.index(q)
    fail_top = max((q for q in base if base[q] > 0), key=lambda q: (routed.get(q, 0.0), -order(q)))
    top = sorted((q for q in base if base[q] > 0 and q != fail_top),
                 key=lambda q: (-base[q], order(q)))[:2] + [fail_top]
    succ = [axis.label[q] for q in top]
    print(f"fired at step 6: {axis.label[fail_top]} (base {base[fail_top]:.3f}, after a failure {routed[fail_top]:.3f})")
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
