#!/usr/bin/env python3
"""Restyle an Attack Flow Builder *Presentation-mode* SVG export to the thesis
figure house style, keeping it recognisable as an Attack Flow artefact.

Pipeline (option B, ch3 §3.1.2 exemplar):
    data/gap/hand_curated/volt_typhoon_exemplar.afb
      -> (Attack Flow Builder, manual) -> ..._exemplar.presentation.svg
      -> THIS TOOL -> docs/thesis/figures/fig_3-1a_attack_flow_volt_typhoon.svg

What it does, and why (see docs/workflows/figure_table_conventions.md):
  - Recolours to greys + one accent. Recognisability lives in the *grammar*
    (condition boxes with True/False tabs, the OR operator node, effect-edge
    routing), not the palette, so neutralising the Builder's blue/green/red to
    greys + the thesis accent (RGB 31,84,140) keeps it obviously Attack Flow
    while bringing it into the house palette. The OR operator is the one node
    class that carries the accent ("the one thing the figure is about").
  - Injects the ATT&CK technique id above each action box (Presentation mode
    drops it; the §3.1.2 prose cites the ids).
  - Leaves the Builder's native 14u label size untouched (bumping it overflows
    the boxes). This figure is inherently wide (a 5-step top row), so it is a
    landscape-page figure; at the landscape typeblock (702.78pt) labels print
    ~7.5pt, just under the ~8pt guide (§h) — accepted over box overflow.

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

# The figure is wide (viewBox 1310u), so it is a landscape-page figure. Emit the
# PDF sized so its natural width fills the measured landscape typeblock
# (702.78pt, figure_table_conventions.md §h); the .tex then includes it with a
# bare \includegraphics (no width macro), which sidesteps the scaling trap and
# puts native 14u labels on the page at ~7.5pt. cairosvg output_width is in px
# (96dpi); px * 0.75 = pt, so 702.78pt / 0.75 = 937.04px.
LANDSCAPE_PT = 702.78
PDF_OUTPUT_WIDTH_PX = LANDSCAPE_PT / 0.75

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
# (the Builder sizes each box to its 14u text). Consequence: at the landscape
# typeblock (702.78pt / 1310u) labels print ~7.5pt, just under the ~8pt guide;
# clearing the floor would need a Builder relayout (wider boxes), not a font hack.
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
        block = block.replace(f'fill="{B_COND_LINE}"', f'fill="{ACCENT}"')  # T/F letters
        block = block.replace(f'fill="{WHITE}"', f'fill="{INK}"')           # label; circle fills restored below
        # the True/False tab circles were white-filled -> keep them white (not ink).
        block = block.replace(f'fill="{INK}" stroke="{ACCENT}"', f'fill="{WHITE}" stroke="{ACCENT}"')
    elif cls == "operator":
        block = block.replace(f'fill="{B_OP_FILL}"', f'fill="{ACCENT}"')
        block = block.replace(f'stroke="{B_OP_LINE}"', f'stroke="{ACCENT_DK}"')
        # keep the white "OR" label on the accent fill.
    return block


def main() -> None:
    svg = SRC.read_text()
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
    # emit the thesis PDF sized to the landscape typeblock (bare-include ready).
    pdf_note = "skipped (cairosvg not importable)"
    try:
        import cairosvg  # noqa: E402
        cairosvg.svg2pdf(bytestring=svg.encode(), write_to=str(OUT_PDF),
                         output_width=PDF_OUTPUT_WIDTH_PX)
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
            pdf_note = f"{OUT_PDF.relative_to(ROOT)} (~{LANDSCAPE_PT:.0f}pt natural width, PDF 1.5)"
        else:
            pdf_note = f"{OUT_PDF.relative_to(ROOT)} (~{LANDSCAPE_PT:.0f}pt natural width, PDF 1.7 -- gs absent)"
    except Exception as exc:  # pragma: no cover - dev convenience
        pdf_note = f"skipped ({exc})"
    printed = 14.0 * (LANDSCAPE_PT / 1310.0)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {pdf_note}")
    print(f"technique-id tags injected: {n_tid}/10")
    print(f"native 14u labels -> ~{printed:.1f}pt at full landscape width ({LANDSCAPE_PT:.0f}pt)")


if __name__ == "__main__":
    main()
