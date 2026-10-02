#!/usr/bin/env python3
"""Dissertation figure: the Volt Typhoon flow (ch3 subsec:profiling,
fig:attack-flow-volt-typhoon), drawn natively in TikZ.

Replaces the Attack Flow Builder export (tools/restyle_attackflow_svg.py),
whose labels printed at ~5.4 pt (Marc, 2026-10-01: "the font is below the
acceptable limit ... it stems from trying to portray everything as is").
The takeaway is one campaign's techniques in order, from the condition it
starts in to the objective it ends in; the figure carries only that:

  - every action is drawn, in its order, by its ATT&CK name (no technique
    ids, regular weight);
  - parallel actions (same distance from the start) stack in one column,
    joined by the OR operator, drawn neutral;
  - colour has one meaning: the accent marks the two conditions, and each
    carries a tag naming its role (start condition / end condition), so the
    drawing explains its own colour (Marc, 2026-10-01: "why is it blue ...
    signpost it in the diagram itself");
  - a condition's label is its first clause (a trailing parenthetical and
    anything after ';' are dropped: the example and the negative rider are
    advisory detail, kept in the data and the README);
  - rows read left to right and wrap like text, the wrap drawn as one line
    back to the next row's first node.

Everything is read from the flow's STIX bundle
(data/gap/hand_curated/volt_typhoon_exemplar.json); nothing is typed.

Usage:
  python tools/attack_flow_figure.py [--no-compile]

Style: TikZ, 12 pt base document, Helvetica (helvet 0.92), greys + the
thesis accent; drawn at the portrait typeblock width so drawn sizes are
printed sizes. The run prints every type class's printed size and fails
under the 7 pt floor. Written to
docs/thesis/figures/fig_3-1-3a_attack_flow_volt_typhoon.tex (+ .pdf).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FLOW = REPO / "data" / "gap" / "hand_curated" / "volt_typhoon_exemplar.json"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_3-1-3a_attack_flow_volt_typhoon"

TEXTWIDTH_PT = 455.24
MAX_ROW_W = 14.2      # cm; a row wraps before it passes this width
BOX_W = 2.75          # cm; action and condition boxes
BOX_H = 1.15          # cm; minimum height (three lines of 8 pt)
OR_D = 0.80           # cm; operator diameter
GAP_X = 0.50          # cm; between columns
GAP_STACK = 0.22      # cm; between stacked parallel boxes
GAP_ROW = 0.75        # cm; between rows (holds the wrap line)

TYPE_FLOOR_PT = 7.0
SIZES = {"label": 8.0, "operator": 7.5, "tag": 7.5}


def font(key: str, extra: str = "") -> str:
    pt = SIZES[key]
    return r"\fontsize{%gpt}{%gpt}\selectfont%s" % (pt, round(pt * 1.18, 2), extra)


def esc(s: str) -> str:
    return s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def condition_label(text: str) -> str:
    """A condition's first clause: drop a trailing parenthetical and anything
    after ';'."""
    text = text.split(";")[0]
    return re.sub(r"\s*\([^)]*\)\s*$", "", text).strip()


def load():
    objs = json.loads(FLOW.read_text())["objects"]
    nodes = {o["id"]: o for o in objs
             if o["type"] in ("attack-action", "attack-condition", "attack-operator")}
    succ = {i: list(o.get("effect_refs") or o.get("on_true_refs") or [])
            for i, o in nodes.items()}
    preds = {i: [] for i in nodes}
    for i, ss in succ.items():
        for s in ss:
            preds[s].append(i)
    # column = longest distance from a start node, so parallel actions share one
    level: dict[str, int] = {}

    def lvl(i: str) -> int:
        if i not in level:
            level[i] = 0 if not preds[i] else 1 + max(lvl(p) for p in preds[i])
        return level[i]

    for i in nodes:
        lvl(i)
    cols: list[list[str]] = [[] for _ in range(max(level.values()) + 1)]
    order = [o["id"] for o in objs if o["id"] in nodes]   # bundle order within a column
    for i in order:
        cols[level[i]].append(i)
    return nodes, succ, cols


def label(o: dict) -> str:
    if o["type"] == "attack-action":
        return esc(o["name"])
    if o["type"] == "attack-condition":
        return esc(condition_label(o["description"]))
    return esc(o["operator"])


def col_width(col, nodes) -> float:
    return OR_D if nodes[col[0]]["type"] == "attack-operator" else BOX_W


def col_height(col, nodes) -> float:
    if nodes[col[0]]["type"] == "attack-operator":
        return OR_D
    return len(col) * BOX_H + (len(col) - 1) * GAP_STACK


def emit(nodes, succ, cols) -> str:
    # wrap the columns into rows
    rows: list[list[list[str]]] = [[]]
    width = 0.0
    for col in cols:
        w = col_width(col, nodes)
        need = w if not rows[-1] else width + GAP_X + w
        if rows[-1] and need > MAX_ROW_W:
            rows.append([])
            need = w
        rows[-1].append(col)
        width = need

    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usepackage[scaled=0.92]{helvet}")
    w(r"\renewcommand{\familydefault}{\sfdefault}")
    w(r"\usetikzlibrary{calc,arrows.meta}")
    w(r"\definecolor{accent}{RGB}{31,84,140}")
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\hyphenpenalty=10000\exhyphenpenalty=10000")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,"
      r"box/.style={draw=black!45,line width=0.5pt,fill=white,align=center,"
      r"text width=%.3fcm,minimum height=%.3fcm,inner xsep=3pt,inner ysep=2pt,"
      r"text=black!85,font=%s},"
      r"cond/.style={box,draw=accent,fill=accentlight!60},"
      r"op/.style={circle,fill=white,draw=black!45,line width=0.5pt,minimum size=%.3fcm,"
      r"inner sep=0pt,text=black!85,font=%s},"
      r"tag/.style={anchor=south west,inner sep=0pt,text=accent,font=%s},"
      r"edge/.style={draw=black!60,line width=0.6pt,-{Latex[length=4.5pt,width=3.6pt]}}]"
      % (BOX_W - 0.22, BOX_H, font("label"), OR_D, font("operator", r"\bfseries"),
         font("tag", r"\itshape")))

    name = {}
    y_top = 0.0
    row_of = {}
    row_bottom = {}
    for r, row in enumerate(rows):
        h = max(col_height(c, nodes) for c in row)
        yc = y_top - h / 2
        x = 0.0
        for col in row:
            cw = col_width(col, nodes)
            ch = col_height(col, nodes)
            y = yc + ch / 2
            for k, i in enumerate(col):
                o = nodes[i]
                n = f"n{len(name)}"
                name[i] = n
                row_of[i] = r
                style = {"attack-action": "box", "attack-condition": "cond",
                         "attack-operator": "op"}[o["type"]]
                if o["type"] == "attack-operator":
                    w(r"\node[%s] (%s) at (%.3f,%.3f) {%s};"
                      % (style, n, x + cw / 2, yc, label(o)))
                else:
                    cy = y - BOX_H / 2 - k * (BOX_H + GAP_STACK)
                    w(r"\node[%s] (%s) at (%.3f,%.3f) {%s};"
                      % (style, n, x + cw / 2, cy, label(o)))
                    if o["type"] == "attack-condition":
                        # the colour says itself: name the condition's role
                        role = "end condition" if not succ[i] else "start condition"
                        w(r"\node[tag] at ($(%s.north west)+(0,0.08)$) {%s};" % (n, role))
            x += cw + GAP_X
        row_bottom[r] = y_top - h
        y_top -= h + GAP_ROW

    for i, ss in succ.items():
        for s in ss:
            a, b = name[i], name[s]
            if row_of[i] == row_of[s]:
                # orthogonal: out east, turn at the half gap, in west
                w(r"\draw[edge] (%s.east) -- ++(%.3f,0) |- (%s.west);" % (a, GAP_X / 2, b))
            else:
                # the wrap: down from the row's last node, back, down into the next
                y_mid = row_bottom[row_of[i]] - GAP_ROW / 2
                w(r"\draw[edge] (%s.south) -- (%s.south |- 0,%.3f) -| (%s.north);"
                  % (a, a, y_mid, b))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


def pdf_size_pt(pdf: Path) -> tuple[float, float]:
    out = subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=bbox",
                          str(pdf)], capture_output=True, text=True).stderr
    m = re.search(r"%%HiResBoundingBox:\s+([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", out)
    x0, y0, x1, y1 = (float(v) for v in m.groups())
    return x1 - x0 + 4.0, y1 - y0 + 4.0


def type_check(pdf: Path) -> None:
    """Printed type at the float's natural-size inclusion (no scaling up)."""
    nat_w, nat_h = pdf_size_pt(pdf)
    scale = min(1.0, TEXTWIDTH_PT / nat_w)
    print(f"  natural {nat_w:.1f} x {nat_h:.1f} pt; printed scale {scale:.3f}, "
          f"height {nat_h * scale / 28.4527:.2f} cm")
    for key, pt in sorted(SIZES.items(), key=lambda kv: kv[1]):
        print(f"    {key:<9} {pt:>4g} pt nominal -> {pt * scale:.2f} pt printed")
    smallest = min(SIZES.values()) * scale
    if smallest < TYPE_FLOOR_PT:
        raise SystemExit(f"type floor breached: {smallest:.2f} pt < {TYPE_FLOOR_PT} pt")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    nodes, succ, cols = load()
    tex_path = OUT_DIR / f"{STEM}.tex"
    tex_path.write_text(emit(nodes, succ, cols))
    print(f"wrote {tex_path.relative_to(REPO)}")
    print(f"  actions {sum(o['type'] == 'attack-action' for o in nodes.values())}, "
          f"columns {len(cols)}")
    if not args.no_compile:
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{STEM}.tex"],
            cwd=OUT_DIR, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:])
            raise SystemExit("pdflatex failed")
        for suffix in (".aux", ".log"):
            (OUT_DIR / f"{STEM}{suffix}").unlink(missing_ok=True)
        print(f"wrote {(OUT_DIR / (STEM + '.pdf')).relative_to(REPO)}")
        type_check(OUT_DIR / f"{STEM}.pdf")


if __name__ == "__main__":
    main()
