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
  - Bumps the label type size so that, included at the measured landscape
    typeblock width (702.78pt), on-page glyphs clear the ~8pt floor (§h). This
    figure is inherently wide (a 5-step top row), so it is a landscape-page
    figure; at portrait \\textwidth its labels would be ~5pt.

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

LABEL_FS = "15"   # -> ~8.05pt at the landscape typeblock (702.78pt / 1310u)
TID_FS = "15"

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


def bump_label_fontsize(block: str) -> str:
    return block.replace('font-size="14"', f'font-size="{LABEL_FS}"')


def restyle_group(block: str) -> str:
    cls = node_class(block)
    if cls == "action":
        block = block.replace(f'fill="{B_ACTION_FILL}"', f'fill="{GREY_FILL}"')
        block = block.replace(f'stroke="{B_ACTION_LINE}"', f'stroke="{GREY_LINE}"')
        block = block.replace(f'fill="{WHITE}"', f'fill="{INK}"')       # label text
        block = bump_label_fontsize(block)
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
        block = bump_label_fontsize(block)
    elif cls == "operator":
        block = block.replace(f'fill="{B_OP_FILL}"', f'fill="{ACCENT}"')
        block = block.replace(f'stroke="{B_OP_LINE}"', f'stroke="{ACCENT_DK}"')
        # keep the white "OR" label on the accent fill; just resize.
        block = bump_label_fontsize(block)
    return block


def main() -> None:
    svg = SRC.read_text()
    # 1) node groups.
    svg = GROUP_RE.sub(lambda m: restyle_group(m.group(0)), svg)
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
    # report printed label size at the landscape typeblock (§h: 702.78pt).
    printed = float(LABEL_FS) * (702.78 / 1310.0)
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"technique-id tags injected: {n_tid}/10")
    print(f"label size {LABEL_FS}u -> {printed:.2f}pt at full landscape width (702.78pt); floor ~8pt")


if __name__ == "__main__":
    main()
