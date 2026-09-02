#!/usr/bin/env python3
"""fig:mtdsim-model --- the three modules of MTDSim (ch2 §2.2 preamble).

The drawing lives in `tools/mtdsim_model_figure.html` (hand-authored SVG:
pictograms, the three-layer network with an accented attack trace, the
defence roster with per-mechanism glyphs, the attacker's objective /
knowledge / capability and its procedure as a loop). This script is the
build step around it:

  1. validates the roster the SVG names against the FULL pool in
     `mtdnetwork/component/mtd_scheme.py` (`MTD_POOLS['full']`, seven mechanisms),
     so a roster change in code fails the build instead of shipping stale;
  2. prints the SVG to a 16 cm-wide PDF through headless Chromium (Playwright)
     -> docs/thesis/figures/fig_2-2a_mtdsim_model.pdf, included at natural size;
  3. optionally renders a PNG preview (--png) for iteration.

Type arithmetic: the SVG is 1000 px wide and prints at 16 cm (455 pt), so
1 px = 0.455 pt; the smallest class in the SVG is 17.5 px = 8.0 pt, the
figure-conventions floor. Do not add text below that size.

Plan and rulings: docs/handoffs/2026-08-27_ch2_model_diagram_plan.md.
Usage: python tools/mtdsim_model_figure.py [--png] [--out-png PATH]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parent.parent
SCHEME_PY = REPO / "mtdnetwork" / "component" / "mtd_scheme.py"
HTML = REPO / "tools" / "mtdsim_model_figure.html"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_2-2a_mtdsim_model"
WIDTH_CM = 16.0
PX = 1100

# code class -> the presentation name the SVG must carry (figure spec, §g)
ROSTER = {   # the FULL pool (Marc, 2026-08-30): ch2 describes the platform as restored
    "IPShuffle": "IP shuffle",
    "CompleteTopologyShuffle": "Topology shuffle",
    "HostTopologyShuffle": "Host topology shuffle",
    "OSDiversity": "OS diversity",
    "ServiceDiversity": "Service diversity",
    "PortShuffle": "Port shuffle",
    "UserShuffle": "User shuffle",
}


def default_family() -> set[str]:
    """The 'full' pool in MTD_POOLS (mtd_scheme.py)."""
    m = re.search(r"'full':\s*\[(.*?)\]", SCHEME_PY.read_text(), re.S)
    if not m:
        raise SystemExit("could not find MTD_POOLS['full'] in mtd_scheme.py")
    return {ln.strip().rstrip(",") for ln in m.group(1).splitlines()
            if ln.strip() and not ln.strip().startswith("#")}


def validate(html: str) -> None:
    code = default_family()
    if code != set(ROSTER):
        raise SystemExit(f"roster drift: code {sorted(code)} vs ROSTER {sorted(ROSTER)}")
    text = " ".join(re.findall(r">([^<>]+)<", html))   # visible text, labels may wrap over two <text>s
    missing = [n for n in ROSTER.values() if n not in text]
    if missing:
        raise SystemExit(f"SVG does not name: {missing}")
    sizes = [float(x) for x in re.findall(r"font-size:\s*([\d.]+)px", html)]
    floor = min(sizes) * (WIDTH_CM / 2.54 * 72) / PX
    if floor < 7.95:
        raise SystemExit(f"smallest type prints at {floor:.1f}pt (< 8pt floor)")
    print(f"roster ok; smallest type {min(sizes)}px -> {floor:.1f}pt at {WIDTH_CM} cm")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--out-png", type=Path, default=OUT_DIR / f"{STEM}.png")
    a = ap.parse_args()
    html = HTML.read_text()
    validate(html)
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', html)
    w_px, h_px = int(vb.group(1)), int(vb.group(2))
    h_cm = WIDTH_CM * h_px / w_px
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": w_px, "height": h_px}, device_scale_factor=2)
        pg.goto(HTML.as_uri()); pg.wait_for_timeout(300)
        if a.png:
            pg.locator("#fig").screenshot(path=str(a.out_png))
            print(f"preview {a.out_png}")
        pg.emulate_media(media="print")
        pg.pdf(path=str(OUT_DIR / f"{STEM}.pdf"), width=f"{WIDTH_CM}cm", height=f"{h_cm:.2f}cm",
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
               print_background=True, prefer_css_page_size=False)
        b.close()
    print(f"wrote {OUT_DIR / (STEM + '.pdf')}  ({WIDTH_CM} x {h_cm:.2f} cm)")


if __name__ == "__main__":
    main()
