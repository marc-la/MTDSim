#!/usr/bin/env python3
"""The ch2 §2.2 figure family --- MTDSim at descending levels of abstraction.

Ruled 2026-09-09 (Marc): one crowded plate becomes a family of floats, each
landing beside the prose that decodes it. Simplified 2026-09-30: Figure 2.3
(execution scheme / defence module) is cut from the thesis; its HTML sources
stay on disk but are no longer built.

  fig:mtdsim-model    §2.2 preamble   the three modules and their coupling
  fig:network-model   §2.2.1          (a) the network by level, (b) one host
  fig:attacker-model  §2.2.3          the attacker's procedure

Each drawing is hand-authored SVG in `tools/ch2_fig2*.html`; this script prints
each through headless Chromium at natural size, so N px in the source is N px on
the page and no inclusion-width edit can push a label under the floor.

Type arithmetic (figure_table_conventions.md §h, §l). The canvas is 900 px wide
and prints at \\textwidth = 16.058 cm = 455.244 pt, so **1 px = 0.5058 pt** --- the
house rule for the SVG route is canvas px ~= 2 x printed pt. The face is Nimbus
Sans (Helvetica metrics) set at 0.92 of nominal, matching `helvet`'s scaled=0.92,
so the floor is counted at NOMINAL size: 8 pt nominal = 14.55 px. Do not go below.

Usage: python tools/ch2_model_figures.py [--only STEM] [--png]
Brief and rulings: docs/handoffs/2026-09-09_ch2_figure_family.md
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
SCHEME_PY = REPO / "mtdnetwork" / "component" / "mtd_scheme.py"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
WIDTH_CM = 16.058          # \textwidth, measured (455.244 pt)
FACE_SCALE = 0.92          # helvet scaled=0.92 equivalent
FLOOR_PT = 7.95            # §g's ~8 pt floor, counted at nominal size

# stem -> (source html, what the roster check applies to)
FIGURES = {
    "fig_2-2a_mtdsim_model":     ("ch2_fig21_mtdsim_model.html",   False),
    "fig_2-2-1a_network_model":  ("ch2_fig22_network_model.html",  False),
    "fig_2-2-3a_attacker_model": ("ch2_fig24_attacker_model.html", False),
}

# code class -> the presentation name the SVG must carry. The roster names must
# match Table 2.2; a pool change in code fails the build rather than shipping stale.
# No figure in FIGURES draws the roster since Figure 2.3 was cut (2026-09-30); the
# check stays so a future roster drawing can set its flag to True.
ROSTER = {
    "IPShuffle": "IP shuffle",
    "CompleteTopologyShuffle": "Complete topology shuffle",
    "HostTopologyShuffle": "Host topology shuffle",
    "OSDiversity": "OS diversity",
    "ServiceDiversity": "Service diversity",
    "PortShuffle": "Port shuffle",
    "UserShuffle": "User shuffle",
}


def _classes(block: str) -> set[str]:
    return {ln.strip().rstrip(",") for ln in block.splitlines()
            if ln.strip() and not ln.strip().startswith("#")}


def _pool(name: str) -> set[str]:
    """The named MTD_POOLS literal. Only 'full' is drawn; the lineage pool's
    membership is a prose fact (Section 2.2.2), so nothing here guards it."""
    src = SCHEME_PY.read_text()
    m = re.search(rf"'{name}':\s*\[(.*?)\]", src, re.S)
    if not m:
        raise SystemExit(f"could not read the {name!r} pool from mtd_scheme.py")
    return _classes(m.group(1))


def validate(stem: str, html: str, check_roster: bool, px: int) -> float:
    """Floor check for every figure; roster check for the one that draws it."""
    if check_roster:
        code = _pool("full")
        if code != set(ROSTER):
            raise SystemExit(f"{stem}: roster drift — code {sorted(code)} vs {sorted(ROSTER)}")
        text = " ".join(re.findall(r">([^<>]+)<", html))
        missing = [n for n in ROSTER.values() if n not in text]
        if missing:
            raise SystemExit(f"{stem}: SVG does not name {missing}")

    # Sizes may be set in CSS or as an SVG attribute; check both, or a size moved
    # to an attribute escapes the floor silently (the old generator's blind spot).
    sizes = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", html)]
    sizes += [float(x) for x in re.findall(r'font-size="([\d.]+)"', html)]
    if not sizes:
        raise SystemExit(f"{stem}: no font sizes found")
    pt_per_px = (WIDTH_CM / 2.54 * 72) / px
    floor = min(sizes) * pt_per_px / FACE_SCALE
    if floor < FLOOR_PT:
        raise SystemExit(f"{stem}: smallest type prints at {floor:.2f} pt nominal (< {FLOOR_PT})")
    return floor


def build(stem: str, src: str, check_roster: bool, want_png: bool) -> None:
    path = REPO / "tools" / src
    html = path.read_text()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', html)
    w_px, h_px = float(vb.group(1)), float(vb.group(2))
    floor = validate(stem, html, check_roster, w_px)
    h_cm = WIDTH_CM * h_px / w_px
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": int(w_px), "height": int(h_px)}, device_scale_factor=2)
        pg.goto(path.as_uri()); pg.wait_for_timeout(250)
        if want_png:
            pg.locator("#fig").screenshot(path=str(OUT_DIR / f"{stem}.png"))
        pg.emulate_media(media="print")
        pg.pdf(path=str(OUT_DIR / f"{stem}.pdf"), width=f"{WIDTH_CM}cm", height=f"{h_cm:.3f}cm",
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
               print_background=True, prefer_css_page_size=False)
        b.close()
    print(f"{stem}: {WIDTH_CM:.2f} x {h_cm:.2f} cm  "
          f"({w_px:.0f}x{h_px:.0f} px, {(WIDTH_CM / 2.54 * 72) / w_px:.4f} pt/px), "
          f"smallest type {floor:.2f} pt nominal ({floor * FACE_SCALE:.2f} pt set)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", action="append", help="build just this stem (repeatable)")
    ap.add_argument("--png", action="store_true", help="also write a PNG preview")
    a = ap.parse_args()
    stems = a.only or list(FIGURES)
    for stem in stems:
        if stem not in FIGURES:
            raise SystemExit(f"unknown stem {stem!r}; known: {sorted(FIGURES)}")
        src, roster = FIGURES[stem]
        if not (REPO / "tools" / src).exists():
            print(f"{stem}: {src} not authored yet — skipped")
            continue
        build(stem, src, roster, a.png)


if __name__ == "__main__":
    main()
