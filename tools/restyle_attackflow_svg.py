#!/usr/bin/env python3
"""Restyle an Attack Flow Builder *Presentation-mode* SVG export to the thesis
figure house style, keeping it recognisable as an Attack Flow artefact.

Pipeline (option B, ch3 §3.1.2 exemplar):
    data/gap/hand_curated/volt_typhoon_exemplar.afb
      -> (Attack Flow Builder, manual) -> ..._exemplar.presentation.svg
      -> THIS TOOL -> docs/thesis/figures/fig_3-1a_attack_flow_volt_typhoon.svg

What it does, and why (see docs/workflows/figure_table_conventions.md):
  - Recolours to greys + one accent. Recognisability lives in the *grammar*
    (condition boxes, the OR operator node, effect-edge routing), not the
    palette, so neutralising the Builder's blue/green/red to
    greys + the thesis accent (RGB 31,84,140) keeps it obviously Attack Flow
    while bringing it into the house palette. The OR operator is the one node
    class that carries the accent ("the one thing the figure is about").
  - Drops the True/False outcome tabs on the condition nodes (Marc,
    2026-10-01: the reader does not need Attack Flow's condition-outcome
    notation). An effect edge that left from a tab is re-anchored on the
    box's edge, straightened when its target row lies within the box, so no
    connector stub is left floating where a tab was.
  - Injects the ATT&CK technique id above each action box (Presentation mode
    drops it; the §3.1.2 prose cites the ids).
  - Leaves the Builder's native 14u label size untouched (bumping it overflows
    the boxes). Included portrait at \\textwidth (Marc's ruling: no landscape);
    the figure is wide, so labels land under the ~8pt guide (§h) — an accepted
    legibility trade for portrait. The printed size is a function of the
    export's viewBox width and is reported per run; a tighter Builder relayout
    (narrower canvas) is the lever that grows it.

Palette classes are detected by the Builder's own fills:
    action    fill #5286e7   condition fill #0e662a   operator  fill #ad2a2a

Deterministic and idempotent. Run:
    python3 tools/restyle_attackflow_svg.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "gap" / "hand_curated" / "volt_typhoon_exemplar.presentation.svg"
OUT = ROOT / "docs" / "thesis" / "figures" / "fig_3-1a_attack_flow_volt_typhoon.svg"
OUT_PDF = OUT.with_suffix(".pdf")

# The PDF is emitted at cairosvg's natural size; the .tex includes it portrait at
# \includegraphics[width=\textwidth] (Marc's ruling: no landscape), which scales
# it to the portrait typeblock (455.24pt). Native 14u labels therefore print at
# 14 * 455.24 / <viewBox width> -- the width is parsed from the export and the
# resulting size reported per run against the ~8pt guide
# (figure_table_conventions.md §h); a narrower Builder relayout grows it.
PORTRAIT_PT = 455.24

# --- house palette ----------------------------------------------------------
ACCENT = "#1f548c"        # RGB 31,84,140 (thesis accent)
ACCENT_DK = "#14385f"     # darker accent for the operator outline
ACCENTLIGHT = "#c8d6e8"   # RGB 200,214,232 (condition fill)
GREY_FILL = "#eef0f2"     # action fill
GREY_LINE = "#5b5b5b"     # action / node outline
EDGE_GREY = "#6b6b6b"     # effect edges + arrowheads
INK = "#1a1a1a"           # dark label text on light fills

# Builder hexes (by role).
B_ACTION_FILL, B_ACTION_LINE = "#5286e7", "#4c6fd9"
B_COND_FILL, B_COND_LINE = "#0e662a", "#24a64b"
B_OP_FILL, B_OP_LINE = "#ad2a2a", "#ff5959"
WHITE = "#FFFFFF"

# Font size is left at the Builder's native 14u — bumping it overflows the boxes
# (the Builder sizes each box to its 14u text). Printed size follows the export's
# viewBox width (see above); growing it is a Builder-relayout job, not a font hack.
TID_FS = "14"     # match the native label size

# ATT&CK technique id per action, keyed by the box's visible name.
NAME_TO_TID = {
    "Exploit Public-Facing Application": "T1190",
    "Exploitation for Privilege Escalation": "T1068",
    "Unsecured Credentials": "T1552",
    "Valid Accounts": "T1078",
    "Remote Services: Remote Desktop Protocol": "T1021.001",
    "Direct Volume Access": "T1006",
    "Windows Management Instrumentation": "T1047",
    "OS Credential Dumping: NTDS": "T1003.003",
    "Brute Force: Password Cracking": "T1110.002",
    "Remote Service Session Hijacking": "T1563",
}

GROUP_RE = re.compile(r"<g\b[^>]*>.*?</g>", re.DOTALL)
VIEWBOX_RE = re.compile(r'viewBox="0 0 ([0-9.]+) [0-9.]+"')
TRANSLATE_RE = re.compile(r'transform="translate\(([-0-9.]+),\s*([-0-9.]+)\)"')
RECT_RE = re.compile(r'<rect\b[^>]*\bwidth="([0-9.]+)"[^>]*\bheight="([0-9.]+)"')
CIRCLE_RE = re.compile(r'<circle\b[^>]*/>')
CIRCLE_GEOM_RE = re.compile(r'\bcx="([-0-9.]+)"[^>]*\bcy="([-0-9.]+)"[^>]*\br="([0-9.]+)"')
TAB_TEXT_RE = re.compile(r'<text\b[^>]*>\s*[TF]\s*</text>')
PATH_D_RE = re.compile(r'(<path\b[^>]*\bd=")([^"]*)(")')
TSPAN_RE = re.compile(r"<tspan[^>]*>(.*?)</tspan>", re.DOTALL)
RECTW_RE = re.compile(r'<rect[^>]*\bwidth="([0-9.]+)"')


def node_class(block: str) -> str:
    if f'fill="{B_ACTION_FILL}"' in block:
        return "action"
    if f'fill="{B_COND_FILL}"' in block:
        return "condition"
    if f'fill="{B_OP_FILL}"' in block:
        return "operator"
    return "other"


def visible_name(block: str) -> str:
    txt = " ".join(t.strip() for t in TSPAN_RE.findall(block))
    return re.sub(r"\s+", " ", txt).strip()


def restyle_group(block: str) -> str:
    cls = node_class(block)
    if cls == "action":
        block = block.replace(f'fill="{B_ACTION_FILL}"', f'fill="{GREY_FILL}"')
        block = block.replace(f'stroke="{B_ACTION_LINE}"', f'stroke="{GREY_LINE}"')
        block = block.replace(f'fill="{WHITE}"', f'fill="{INK}"')       # label text
        # inject the technique id above the box, centred.
        name = visible_name(block)
        tid = NAME_TO_TID.get(name)
        if tid:
            m = RECTW_RE.search(block)
            cx = float(m.group(1)) / 2 if m else 80.0
            tag = (f'<text x="{cx:.1f}" y="-9" text-anchor="middle" fill="{ACCENT}" '
                   f'font-family="Inter, Arial, sans-serif" font-size="{TID_FS}" '
                   f'font-weight="700" pointer-events="none">{tid}</text>')
            block = block[: block.rfind("</g>")] + tag + "</g>"
    elif cls == "condition":
        block = block.replace(f'fill="{B_COND_FILL}"', f'fill="{ACCENTLIGHT}"')
        block = block.replace(f'stroke="{B_COND_LINE}"', f'stroke="{ACCENT}"')
        block = block.replace(f'fill="{WHITE}"', f'fill="{INK}"')           # label text
        # the True/False outcome tabs: circles and their T/F letters go.
        block = CIRCLE_RE.sub("", block)
        block = TAB_TEXT_RE.sub("", block)
    elif cls == "operator":
        block = block.replace(f'fill="{B_OP_FILL}"', f'fill="{ACCENT}"')
        block = block.replace(f'stroke="{B_OP_LINE}"', f'stroke="{ACCENT_DK}"')
        # keep the white "OR" label on the accent fill.
    return block


def condition_tabs(svg: str) -> list[tuple[float, float, float, float, float, float, float]]:
    """Absolute geometry of every condition node's outcome tabs, read before
    they are dropped: (tab cx, cy, r, box x0, y0, x1, y1)."""
    tabs = []
    for m in GROUP_RE.finditer(svg):
        block = m.group(0)
        if node_class(block) != "condition":
            continue
        tr, rect = TRANSLATE_RE.search(block), RECT_RE.search(block)
        tx, ty = float(tr.group(1)), float(tr.group(2))
        bw, bh = float(rect.group(1)), float(rect.group(2))
        for c in CIRCLE_RE.findall(block):
            cx, cy, r = (float(v) for v in CIRCLE_GEOM_RE.search(c).groups())
            tabs.append((tx + cx, ty + cy, r, tx, ty, tx + bw, ty + bh))
    return tabs


def reanchor_edges(svg: str, tabs) -> tuple[str, int]:
    """Move every edge end that sat on a dropped tab onto the box's edge.

    An edge leaving a right-hand tab starts at (cx + r, cy). It is re-started
    on the box's right edge; if its final row lies within the box, the elbow
    the tab forced is straightened to one horizontal run at that row."""
    moved = 0

    def fix(m: re.Match) -> str:
        nonlocal moved
        pts = [tuple(float(v) for v in xy) for xy in
               re.findall(r"[ML]\s*([-0-9.]+)\s+([-0-9.]+)", m.group(2))]
        for cx, cy, r, x0, y0, x1, y1 in tabs:
            for end in (0, -1):
                px, py = pts[end]
                if abs(abs(px - cx) - r) < 0.5 and abs(py - cy) < 0.5:
                    edge_x = x1 if px > cx else x0
                    other = pts[-1] if end == 0 else pts[0]
                    if y0 < other[1] < y1:            # straight run at the far row
                        pts = [(edge_x, other[1]), other] if end == 0 else [other, (edge_x, other[1])]
                    else:
                        pts[end] = (edge_x, py)
                    moved += 1
        d = " ".join(("M" if i == 0 else "L") + f" {x:g} {y:g}" for i, (x, y) in enumerate(pts))
        return m.group(1) + d + m.group(3)

    return PATH_D_RE.sub(fix, svg), moved


def main() -> None:
    svg = SRC.read_text()
    # 0) the condition tabs' geometry, then re-anchor any edge that used one.
    tabs = condition_tabs(svg)
    svg, n_moved = reanchor_edges(svg, tabs)
    # 1) node groups.
    svg = GROUP_RE.sub(lambda m: restyle_group(m.group(0)), svg)
    # 1b) font stack. The Builder sized every box to *Inter* metrics, but on a box
    # without Inter installed a renderer matches "Inter"/"sans-serif" to DejaVu Sans,
    # which is wider than Inter and overflows the boxes in the PDF (the browser SVG,
    # with real Inter, fits). Lead with Arial/Helvetica so the SVG->PDF renderer picks
    # a Helvetica-metric font (TeX Gyre Heros), which is close to Inter and fits.
    svg = svg.replace("Inter, Arial, sans-serif", "Arial, Helvetica, sans-serif")
    # 2) edges + arrowheads (top level, outside groups): both use the Builder line hue.
    svg = svg.replace(f'stroke="{B_ACTION_LINE}"', f'stroke="{EDGE_GREY}"')
    svg = svg.replace(f'<polygon data-v-4a541c10="" points', '<polygon data-v-4a541c10="" points')  # noop guard
    svg = re.sub(r'(<polygon\b[^>]*\bfill=")#4c6fd9(")', rf'\g<1>{EDGE_GREY}\g<2>', svg)
    # sanity: no Builder hues survive.
    for hexcode in (B_ACTION_FILL, B_COND_FILL, B_OP_FILL, B_OP_LINE, B_ACTION_LINE, B_COND_LINE):
        assert hexcode not in svg, f"unconverted Builder colour {hexcode} remains"
    n_tid = svg.count(f'font-size="{TID_FS}" font-weight="700"')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg)
    # emit the thesis PDF (natural size; the .tex scales it via width=\\textwidth).
    pdf_note = "skipped (cairosvg not importable)"
    try:
        import cairosvg  # noqa: E402
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(OUT_PDF))
        # cairosvg emits PDF 1.7; dissertation.tex's pdfTeX caps inclusion at 1.5.
        # Downconvert with ghostscript (vectors preserved) so the thesis build is
        # warning-free; if gs is absent, keep the 1.7 PDF (it still includes).
        import shutil
        import subprocess
        if shutil.which("gs"):
            tmp = OUT_PDF.with_suffix(".pdf.tmp")
            subprocess.run(
                ["gs", "-q", "-dBATCH", "-dNOPAUSE", "-dCompatibilityLevel=1.5",
                 "-dAutoRotatePages=/None", "-sDEVICE=pdfwrite",
                 f"-sOutputFile={tmp}", str(OUT_PDF)], check=True)
            tmp.replace(OUT_PDF)
            pdf_note = f"{OUT_PDF.relative_to(ROOT)} (PDF 1.5)"
        else:
            pdf_note = f"{OUT_PDF.relative_to(ROOT)} (PDF 1.7 -- gs absent)"
    except Exception as exc:  # pragma: no cover - dev convenience
        pdf_note = f"skipped ({exc})"
    vb = VIEWBOX_RE.search(svg)
    assert vb, "no viewBox on the export's <svg> root"
    vb_width = float(vb.group(1))
    printed = 14.0 * (PORTRAIT_PT / vb_width)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {pdf_note}")
    print(f"technique-id tags injected: {n_tid}/10")
    print(f"condition outcome tabs dropped: {len(tabs)}; edges re-anchored: {n_moved}")
    print(f"viewBox width {vb_width:.0f}u; native 14u labels -> "
          f"~{printed:.1f}pt at portrait \\textwidth ({PORTRAIT_PT:.0f}pt)")


if __name__ == "__main__":
    main()
