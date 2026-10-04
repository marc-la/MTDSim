#!/usr/bin/env python3
"""Dissertation figure: Figure 4.3 --- the tactics each attack profile reaches.

Takeaways (Marc 2026-10-04; the grids this replaces were "decoration", and a
bar-chart mock read as "a lot of numbers", "not a natural viewing state"):

  T1  the four attack profiles share the tactics through the middle of an
      attack: execution, stealth and command and control appear in most
      attack flows of every profile;
  T2  they differ at the objective: collection (which the classification does
      not read) as well as exfiltration and impact (which it does);
  T3  every profile is sparse before initial access (section 4.1's gap).

Form, from two cold reads (a CS-student read and a visualisation critique,
2026-10-04) and Wilke, Fundamentals of Data Visualization (2019):
  * one row per tactic, top to bottom in ATT&CK matrix order, so the names
    are horizontal (sec. 6.1: swap the axes for long labels) and the column
    reads as the attack proceeds; one column per attack profile, so comparing
    the profiles at one tactic is one row of four cells;
  * each cell a ring, the whole attack profile, with a disc inside whose AREA
    is the share of the profile's attack flows that reach the tactic
    (Wilke ch. 17: area proportional to the value). Continuous, no bins:
    binning put both objective cells T2 rests on (10/19, 3/7) either side of
    an edge one attack flow wide. An empty ring is none, so absence pops
    (Marc: the dot mock made "the gap ... clearly" visible), and 1/19 is a
    visible dot, not a near-white grey. A continuous grey shade in the same
    layout was built and cold-read beside it, and lost: the 1/19 cell read as
    none, and nobody could rank the middle greys;
  * the rows grouped by the four lifecycle stages the thesis already uses
    (section 4.4's failure matrix; data/ogasp/controller/
    lifecycle_consensus.json), in the band style of the controller-mapping
    figure, the same family: stage name small and grey at the left, a faint
    fill on alternate stages. The three takeaways are then the stages:
    preparation sparse, intrusion and post-intrusion shared, objective
    different. (Marc 2026-10-04: this replaced two unexplained gaps, after
    resource development and before exfiltration);
  * the key a row of five discs labelled only at its ends, so it reads as a
    continuous scale (five labelled anchors read as bins: "do we round
    down?");
  * each column headed by its code and Table 4.1's two questions as rows of
    yes and no (round 3, Marc 2026-10-04: "both" and "neither" could not
    stand alone), above a rule, so the classification sits directly over the
    exfiltration and impact rows it is compared with; never a tactic's name
    (9 of c1's 19 attack flows never draw the exfiltration tactic). No sizes
    and no key title, since Table 4.1 gives the sizes and the caption says
    what the disc is; no counts in the cells (the k/n are printed below, for
    the prose); greys only (Figure 4.1 spends the accent on what this
    dissertation builds).

A tactic is reached by an attack flow when one of its techniques stands for
it (the primary tactic, section 4.1's rule). Every count is read from the
artefacts (data/gap/gap_v0.5.json; the classification via
pipeline_ladder_figure.load_classes, guarded by ch4_attack_profiles_figure.
profiles) and printed. House style as tools/ch4_attack_graph_figure.py.

Usage:
  PYTHONPATH=src python tools/ch4_profile_reach_figure.py
      [--out-dir DIR] [--stem STEM] [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from _tactic_axis import load_axis, load_stages  # noqa: E402
from ch4_attack_profiles_figure import AGG, code, profiles  # noqa: E402  same guards, same code glyph
from pipeline_ladder_figure import PROFILE_ORDER, REPORTS, load_classes, load_gap  # noqa: E402

OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-2b_profile_reach"
WIDTH_CM = 16.058          # \textwidth, measured (455.244 pt)
PX = 900
FACE_SCALE = 0.92
FLOOR_PT = 7.95

INK, INK2, RING = "#333", "#6e6e6e", "#8c8c8c"   # the ring dark enough to tell 4/5 from all
BAND = "#f5f5f5"           # black!4, the controller-mapping figure's stage fill
SIZES = {"lbl": 17, "sm": 15.5}

STYLE = f"""
  html, body {{ margin:0; background:#fff; }}
  svg {{ display:block; font-family: "Nimbus Sans", "TeX Gyre Heros", Helvetica, Arial, sans-serif; }}
  text {{ fill:{INK}; }}
  .lbl {{ font-size:17px; }}
  .sm  {{ font-size:15.5px; fill:{INK2}; }}
"""

# geometry, px at 900 wide
STAGE_X = 6                # stage names start here
NAME_R = 352               # tactic names end here (right-aligned)
COL0, COL_W = 432, 128     # first column's centre; column pitch
ROW_H = 28
R = 11.5                   # the ring: the whole attack profile
HEAD_LINE = 19
KEY = (0, 0.25, 0.5, 0.75, 1)      # labelled at the ends only: a continuous scale


class SVG:
    def __init__(self):
        self.parts: list[str] = []
        self.sizes: list[float] = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, cls="lbl", anchor="middle", raw=False):
        self.sizes.append(SIZES[cls])
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        if not raw:
            s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.parts.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}>{s}</text>')

    def cell(self, cx, cy, share):
        self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R}" fill="none" stroke="{RING}" stroke-width="1.2"/>')
        if share > 0:
            self.parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R * math.sqrt(share):.2f}" fill="{INK}"/>')


def reach(gap, flows: set[str], tactic: str) -> int:
    """Attack flows that reach the tactic: one of their techniques stands for it."""
    return len({f for n in gap["nodes"].values() if n["primary_tactic"] == tactic for f in n["flow_ids"]} & flows)


QUESTIONS = ("Stole data", "Impeded systems")   # Table 4.1's two columns, in its words


def emit(gap, axis, prof):
    stage_of, stage_name = load_stages()
    order = axis.stage_grouped_order(stage_of)
    svg = SVG()
    # the code, then Table 4.1's two questions as rows of yes and no, then a rule
    y_code = HEAD_LINE
    y_q = [y_code + 8 + (j + 0.5) * ROW_H for j in range(len(QUESTIONS))]
    y_rule = y_code + 8 + len(QUESTIONS) * ROW_H + 4
    y_rows = y_rule + 4
    ys = {t: y_rows + (i + 0.5) * ROW_H for i, t in enumerate(order)}
    height = y_rows + len(order) * ROW_H + 4
    # the stage bands: a faint fill on alternate stages, the name at the left
    for st in sorted(set(stage_of.values())):
        rows = [t for t in order if stage_of[t] == st]
        y0, y1 = ys[rows[0]] - ROW_H / 2, ys[rows[-1]] + ROW_H / 2
        if st % 2:
            svg.add(f'<rect x="0" y="{y0:.1f}" width="{COL0 + 3.5 * COL_W:.1f}" height="{y1 - y0:.1f}" fill="{BAND}"/>')
        svg.text(STAGE_X, (y0 + y1) / 2 + 5.5, stage_name[st], "sm", anchor="start")

    for j, q in enumerate(QUESTIONS):
        svg.text(NAME_R, y_q[j] + 6, q, anchor="end")
    svg.add(f'<line x1="0" y1="{y_rule:.1f}" x2="{COL0 + 3.5 * COL_W:.1f}" y2="{y_rule:.1f}" '
            f'stroke="{RING}" stroke-width="1"/>')
    counts = {}
    for k, p in enumerate(PROFILE_ORDER):
        cx = COL0 + k * COL_W
        flows = prof[p][0]
        svg.text(cx, y_code, code(p), raw=True)
        for j, yes in enumerate(REPORTS[p]):
            svg.text(cx, y_q[j] + 6, "yes" if yes else "no")
        for t in order:
            c = reach(gap, flows, t)
            counts[(p, t)] = (c, len(flows))
            svg.cell(cx, ys[t], c / len(flows))
    for t in order:
        svg.text(NAME_R, ys[t] + 6, axis.label[t].capitalize(), anchor="end")

    # the key, under the columns: five discs labelled at the ends only
    mid = COL0 + 1.5 * COL_W
    ky = height - 8                    # no title: the caption says what the disc is
    pitch = 2 * R + 14
    x0 = mid - (len(KEY) - 1) * pitch / 2
    for i, share in enumerate(KEY):
        svg.cell(x0 + i * pitch, ky + 30, share)
    svg.text(x0 - R - 10, ky + 35.5, "none", "sm", anchor="end")
    svg.text(x0 + (len(KEY) - 1) * pitch + R + 10, ky + 35.5, "all", "sm", anchor="start")
    height = ky + 30 + R + 4

    h_cm = WIDTH_CM * height / PX
    html = (f'<!doctype html><html><head><meta charset="utf-8"><style>{STYLE}'
            f'@page {{ size:{WIDTH_CM}cm {h_cm:.3f}cm; margin:0; }}</style></head><body>'
            f'<svg id="fig" xmlns="http://www.w3.org/2000/svg" width="{PX}" height="{height:.0f}" '
            f'viewBox="0 0 {PX} {height:.0f}" style="width:{WIDTH_CM}cm;height:{h_cm:.3f}cm">'
            f'<title>fig:attack-profiles --- the tactics each attack profile reaches (generated by '
            f'tools/ch4_profile_reach_figure.py; do not hand-edit)</title>'
            f'{"".join(svg.parts)}</svg></body></html>')
    floor = min(svg.sizes) * (WIDTH_CM / 2.54 * 72) / PX / FACE_SCALE
    return html, h_cm, floor, round(height), counts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR, help="mocks go to the scratchpad, not the thesis")
    ap.add_argument("--stem", default=STEM)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    gap, gap_order = load_gap()
    axis = load_axis()
    axis.check_against(gap_order)
    prof = profiles(gap, load_classes())
    if sum(len(prof[p][0]) for p in PROFILE_ORDER) != len(prof[AGG][0]):
        raise SystemExit("the attack profiles do not partition the attack flows")

    html, h_cm, floor, h_px, counts = emit(gap, axis, prof)
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

    print("--- facts (read from the artefacts; the caption and prose may quote them) ---")
    print("tactic".ljust(22) + "".join(f"c{k + 1}".rjust(8) for k in range(4)))
    for t in axis.stage_grouped_order(load_stages()[0]):
        print(t.ljust(22) + "".join(f"{counts[(p, t)][0]}/{counts[(p, t)][1]}".rjust(8) for p in PROFILE_ORDER))
    print(f"size / type: {WIDTH_CM} x {h_cm:.2f} cm; smallest type {floor:.2f} pt nominal")


if __name__ == "__main__":
    main()
