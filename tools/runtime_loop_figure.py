#!/usr/bin/env python3
"""Dissertation figure: the movement attacker's runtime loop (fig:runtime-loop,
§4.4 Mechanics and the join to MTDSim).

Restored 2026-09-08 as its own float on the supervisor's verdict (relayed by
Marc; handoff docs/handoffs/2026-09-08_ch4_fig41_redesign.md): the loop had
been folded into the chapter-opening ladder on 2026-09-05, where it was
understood but too small. This is that lower half, inflated to the text
width and drawn at \\footnotesize --- the drawing is the same, the scale is
not. Three bands on one axis:

  MOVEMENT LAYER (built)     the net, as the fragment fig:pipeline draws at
                             L3 (same window rule, imported from
                             tools/pipeline_ladder_figure.py, so the two
                             figures cannot drift apart): the token in a
                             tactic-place, its timed dwell, the weighted
                             routing out of it
  CONTROLLER LAYER (built)   the three declared inputs as glyphs: dwell times
                             and the exponential draw, the tactic-to-verb
                             mapping, the failure matrix
  ACTION LAYER (inherited)   attacker / network / defender, subdued

and the six numbered joins that trace one iteration: (1) tactic down,
(2) drawn dwell time and (3) verb down into the action layer, (4) verdict
up, splitting into a failure arm that enters the failure matrix and a
success arm that bypasses the controller band on the right, (5) re-weighting
up, (6) the token's next tactic on the net.

Every glyph is drawn from a tracked artefact --- the dwell catalogue, the
controller mapping registry, the outcome-overlay rule set, the structural
net --- and the tactic axis is checked against the pinned bundle. Nothing is
typed. The pins a caption states are printed to stdout.

Usage:
  PYTHONPATH=src python tools/runtime_loop_figure.py
      [--mapping v2_partial] [--overlay-version v4_failure_only] [--no-compile]

Style: TikZ at the document's 12 pt base, house figure sans, greys carry the
structure, one accent marks what this thesis builds. Packed to 16 cm and
included at natural size. Written to docs/thesis/figures/fig_4-4c_runtime_loop.tex
(+ .pdf unless --no-compile).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tools"))

from _tactic_axis import load_axis  # noqa: E402
from pipeline_ladder_figure import (  # noqa: E402
    PROFILE_LABEL, PROFILE_ORDER, load_classes, load_gap, load_net, net_window,
)
from mtdsim.l3_simulation.controller.outcome import load_overlay_registry  # noqa: E402
from mtdsim.l3_simulation.controller.rules import (  # noqa: E402
    compile_pair,
    load_rule_set,
    spec_from_registry_entry,
)

DURATIONS_JSON = REPO / "data" / "ogasp" / "tactic_durations.json"
MAPPING_DIR = REPO / "data" / "ogasp" / "controller" / "mappings"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-4c_runtime_loop"

# --- geometry (cm) ---------------------------------------------------------
WIDTH = 16.0
ROT_X = 0.20            # x of the rotated band labels
GUT_R = 1.75            # right edge of the L3 / L4 labels
BAND_L = 1.95           # left edge of the content bands
BAND_R = 15.12          # right edge (the success bypass runs outside it)
PAD = 0.22

H_MOVE = 3.05           # the net fragment
H_JOIN = 1.45           # a between-band join
H_CTRL = 3.95           # the controller band
H_ACT = 1.95            # the action band

ACCENT = "accent"
F = r"\footnotesize"    # 10 pt at natural size; the floor is 8 pt


# ---------------------------------------------------------------- loading --
def load_durations() -> dict[str, float]:
    doc = json.loads(DURATIONS_JSON.read_text())
    return {k: float(v["duration_s"]) for k, v in doc["tactics"].items()}


def load_mapping(version: str) -> tuple[dict[str, str | None], list[str]]:
    rows = list(csv.DictReader((MAPPING_DIR / f"{version}.csv").open(encoding="utf-8")))
    mapping: dict[str, str | None] = {}
    verbs: list[str] = []
    for r in rows:
        verb = (r["sim_phase"] or "").strip()
        disp = r["disposition"].strip()
        if not verb and disp != "dwell-only":
            raise SystemExit(f"{version}: {r['tactic']} is silent without a dwell-only "
                             "disposition -- the registry invariant is broken")
        mapping[r["tactic"]] = verb or None
        if verb and verb not in verbs:
            verbs.append(verb)
    return mapping, verbs


def failure_cells(order: list[str], version: str):
    rs = load_rule_set()
    reg = load_overlay_registry()
    try:
        entry = next(v for v in reg.versions if v.name == version)
    except StopIteration:
        raise SystemExit(f"unknown overlay version {version!r}")
    spec = spec_from_registry_entry(entry.spec)
    out = {}
    for a in order:
        for b in order:
            if a == b:
                continue
            out[(a, b)] = compile_pair(rs, "failure", a, b, spec)["v"]
    return out, len(rs.order["failure"])


# ------------------------------------------------------------- primitives --
def band(w, y_top, y_bot, colour, fill=None):
    opt = f"draw={colour},line width=0.5pt,rounded corners=2pt"
    if fill:
        opt += f",fill={fill}"
    w(r"\draw[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (opt, BAND_L, y_bot, BAND_R, y_top))


def rot_label(w, y_top, y_bot, text, colour):
    w(r"\node[rotate=90,anchor=center,font=%s,text=%s] at (%.3f,%.3f) {%s};"
      % (F, colour, ROT_X, (y_top + y_bot) / 2, text))


def badge(w, x, y, n):
    w(r"\node[circle,draw=black!60,fill=white,text=black!70,inner sep=0.6pt,minimum size=11pt,"
      r"line width=0.4pt,font=%s] at (%.3f,%.3f) {%d};" % (F, x, y, n))


# ------------------------------------------------------------------ bands --
def emit(order, axis, net, win, durations, mapping, verbs, fmatrix, n_rules,
         mapping_version, overlay_version) -> tuple[str, dict]:
    idx = {t: i for i, t in enumerate(order)}
    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usepackage[scaled=0.92]{helvet}")
    w(r"\renewcommand{\familydefault}{\sfdefault}")
    w(r"\usetikzlibrary{arrows.meta,positioning,calc,decorations.pathreplacing}")
    w(r"\definecolor{accent}{RGB}{31,84,140}")
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,>={Stealth[length=1.8mm]},"
      r" every node/.style={font=%s,inner sep=0pt}]" % F)
    facts: dict[str, object] = {}

    # ============================================== the movement layer band ==
    y = 0.0
    mv_top = y
    # the net fragment: places on a readable pitch, names beneath
    have = {(t["src_tactic"], t["dst_tactic"]) for t in net["transitions"]}
    inner = [(a, b) for a in win for b in win if a != b and (a, b) in have]
    R = 0.24
    pitch = 2.75
    fx = {t: BAND_L + 1.35 + k * pitch for k, t in enumerate(win)}
    ys = mv_top - PAD - 1.12
    tok = win[1]                       # the marking fig:pipeline's "after" state shows
    T_DX, I_DX, I_P = R + 0.36, R + 0.84, 0.26
    for k, t in enumerate(win):
        x = fx[t]
        live = (t == tok)
        pc = "black" if live else "black!45"
        outs = sorted((b for a, b in inner if a == t),
                      key=lambda b: (idx[b] < idx[t], abs(idx[b] - idx[t])))
        if outs:
            tx = x + T_DX
            w(r"\draw[%s,line width=0.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (pc, x + R, ys, tx - 0.07, ys))
            w(r"\draw[%s,fill=white,line width=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
              % (pc, "0.8pt" if live else "0.5pt", tx - 0.07, ys - 0.24, tx + 0.07, ys + 0.24))
            n = len(outs)
            for j, b in enumerate(outs):
                iy = ys + (j - (n - 1) / 2) * I_P
                ix = x + I_DX
                hot = live and b == win[2]
                colr = ACCENT if hot else ("black!70" if live else "black!28")
                lw = "1.0pt" if hot else "0.5pt"
                w(r"\draw[%s,line width=%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (colr, lw, tx + 0.07, ys, ix - 0.05, iy))
                w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (colr, ix - 0.05, iy - 0.15, ix + 0.05, iy + 0.15))
                fwd = idx[b] > idx[t]
                x2 = fx[b] - R - 0.03 if fwd else fx[b] + R + 0.03
                dist = abs(idx[b] - idx[t])
                if fwd and dist == 1:
                    w(r"\draw[->,%s,line width=%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (colr, lw, ix + 0.05, iy, x2, ys))
                else:
                    lift = (0.50 + 0.22 * dist) if fwd else -(0.46 + 0.12 * dist)
                    mid = (ix + x2) / 2
                    w(r"\draw[->,%s,line width=%s] (%.3f,%.3f) .. controls (%.3f,%.3f) and (%.3f,%.3f) .. (%.3f,%.3f);"
                      % (colr, lw, ix + 0.05, iy, ix + 0.05 + 0.3 * (x2 - ix), ys + lift,
                         x2 - 0.3 * (x2 - ix), ys + lift, x2, ys))
                if hot:   # the badge sits on the arrow itself; the caption decodes it
                    badge(w, (ix + x2) / 2, ys, 6)
        w(r"\draw[%s,fill=white,line width=%s] (%.3f,%.3f) circle (%.3f);"
          % (pc, "0.8pt" if live else "0.5pt", x, ys, R))
        w(r"\node[anchor=north,align=center,text=black!58] at (%.3f,%.3f) {%s};"
          % (x, ys - R - 0.50, axis.label[t].replace(" ", r"\\", 1)))
        if live:
            w(r"\fill[%s] (%.3f,%.3f) circle (0.10);" % (ACCENT, x, ys))
            cx_, cy_ = x + T_DX, ys + 0.62
            w(r"\draw[black!60,line width=0.5pt] (%.3f,%.3f) circle (0.15);" % (cx_, cy_))
            w(r"\draw[black!60,line width=0.5pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);"
              % (cx_, cy_ + 0.09, cx_, cy_, cx_ + 0.07, cy_))
            w(r"\node[anchor=west,text=black!58] at (%.3f,%.3f) {dwell};" % (cx_ + 0.24, cy_))
    y = mv_top - H_MOVE
    w(r"\node[anchor=south east,align=right,text=black!58] at (%.3f,%.3f) {one profile's net, a fragment};"
      % (BAND_R - 0.18, y + 0.14))
    band(w, mv_top, y, "accent!45")
    rot_label(w, mv_top, y, "Profile net", "accent")
    w(r"\node[anchor=east,align=right] at (%.3f,%.3f) {\textbf{L3}\\Petri net};" % (GUT_R, (mv_top + y) / 2))
    mv_bot = y
    facts["net"] = (len(net["places"]), len(net["transitions"]), win)

    # ================================================== the two-way joins ==
    x_a, x_b = BAND_L + 2.9, BAND_R - 2.9
    y_ctrl_top = mv_bot - H_JOIN
    jm = (mv_bot + y_ctrl_top) / 2
    w(r"\draw[->,accent!70,line width=0.9pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x_a, mv_bot - 0.08, x_a, y_ctrl_top + 0.08))
    w(r"\node[anchor=east,text=accent] at (%.3f,%.3f) {tactic};" % (x_a - 0.14, jm))
    badge(w, x_a + 0.34, jm, 1)
    w(r"\draw[->,accent!70,line width=0.9pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x_b, y_ctrl_top + 0.08, x_b, mv_bot - 0.08))
    w(r"\node[anchor=west,text=accent] at (%.3f,%.3f) {re-weighting};" % (x_b + 0.14, jm))
    badge(w, x_b - 0.34, jm, 5)

    # ============================================== the controller layer ==
    y = y_ctrl_top
    ctrl_top = y
    cell_w = (BAND_R - BAND_L - 1.0) / 3
    cx = [BAND_L + 0.5 + cell_w * (i + 0.5) for i in range(3)]
    head_y = y - 0.38
    body_top = y - 0.80
    body_bot = ctrl_top - H_CTRL + 0.36
    for i in (1, 2):
        sx = BAND_L + 0.5 + cell_w * i
        w(r"\draw[black!22,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (sx, ctrl_top - 0.2, sx, ctrl_top - H_CTRL + 0.18))

    # (i) dwell times + the exponential draw
    w(r"\node at (%.3f,%.3f) {Dwell times};" % (cx[0], head_y))
    bar_x0 = cx[0] - cell_w / 2 + 0.36
    bar_max = 1.70
    dmax = max(durations.values())
    bpitch = (body_top - body_bot) / (len(order) - 1)
    for i, t in enumerate(order):
        by = body_top - i * bpitch
        ln = bar_max * durations[t] / dmax
        w(r"\draw[black!45,line width=0.25pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (bar_x0, by, bar_x0 + bar_max, by))
        if ln > 0:
            w(r"\draw[black!68,line width=1.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (bar_x0, by, bar_x0 + ln, by))
    ex_x0 = bar_x0 + bar_max + 0.55
    ex_w, ex_h = 1.20, (body_top - body_bot) - 0.62
    ey0 = body_bot + 0.62
    w(r"\draw[black!30,line width=0.35pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);"
      % (ex_x0, ey0 + ex_h, ex_x0, ey0, ex_x0 + ex_w, ey0))
    pts = ["(%.3f,%.3f)" % (ex_x0 + (k / 30) * ex_w, ey0 + ex_h * math.exp(-3.1 * k / 30)) for k in range(31)]
    w(r"\draw[black!70,line width=0.7pt] " + " -- ".join(pts) + ";")
    w(r"\draw[->,black!45,line width=0.45pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (bar_x0 + bar_max + 0.12, (body_top + body_bot) / 2, ex_x0 - 0.12, (body_top + body_bot) / 2))
    w(r"\node[anchor=north,align=center,text=black!58] at (%.3f,%.3f) {exponential\\draw};" % (ex_x0 + ex_w / 2, ey0 - 0.08))

    # (ii) the tactic-to-verb mapping (horizontal: tactics above, verbs below)
    w(r"\node at (%.3f,%.3f) {Tactic-to-verb mapping};" % (cx[1], head_y))
    row_l, row_r = cx[1] - 0.80, cx[1] + 1.75
    ty_row, vy_row = body_top - 0.16, body_bot + 0.16
    tp = (row_r - row_l) / (len(order) - 1)
    tx = {t: row_l + i * tp for i, t in enumerate(order)}
    vp = (row_r - row_l) / max(len(verbs) - 1, 1)
    vx = {v: row_l + i * vp for i, v in enumerate(verbs)}
    for t in order:
        v = mapping.get(t)
        if v:
            w(r"\draw[black!45,line width=0.35pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (tx[t], ty_row, vx[v], vy_row))
    for t in order:
        if mapping.get(t):
            w(r"\fill[black!68] (%.3f,%.3f) circle (1.1pt);" % (tx[t], ty_row))
        else:
            w(r"\draw[black!42,line width=0.4pt] (%.3f,%.3f) circle (1.1pt);" % (tx[t], ty_row))
    for v in verbs:
        w(r"\fill[black!68] (%.3f,%.3f) circle (1.4pt);" % (vx[v], vy_row))
    w(r"\node[anchor=east,text=black!58] at (%.3f,%.3f) {tactics};" % (row_l - 0.20, ty_row))
    w(r"\node[anchor=east,text=black!58] at (%.3f,%.3f) {verbs};" % (row_l - 0.20, vy_row))
    n_mapped = sum(1 for t in order if mapping.get(t))
    facts["mapping"] = (mapping_version, n_mapped, len(order) - n_mapped, len(verbs))

    # (iii) the failure matrix
    w(r"\node at (%.3f,%.3f) {Failure matrix};" % (cx[2], head_y))
    side = min(1.75, body_top - body_bot)
    cs = side / len(order)
    mx0 = cx[2] - side / 2
    my0 = body_top - (body_top - body_bot - side) / 2
    for i, a in enumerate(order):
        for j, b in enumerate(order):
            if a == b:
                w(r"\fill[black!8] (%.3f,%.3f) rectangle (%.3f,%.3f);"
                  % (mx0 + j * cs, my0 - i * cs - cs, mx0 + j * cs + cs, my0 - i * cs))
                continue
            v = fmatrix[(a, b)]
            if v <= 0:
                continue
            lvl = int(round(6 + 68 * min(max(v, 0.0), 1.0)))
            w(r"\fill[black!%d] (%.3f,%.3f) rectangle (%.3f,%.3f);"
              % (lvl, mx0 + j * cs, my0 - i * cs - cs, mx0 + j * cs + cs, my0 - i * cs))
    w(r"\draw[black!35,line width=0.35pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (mx0, my0 - side, mx0 + side, my0))
    facts["failure"] = (overlay_version, len(order), n_rules)

    y = ctrl_top - H_CTRL
    band(w, ctrl_top, y, "accent!45")
    rot_label(w, ctrl_top, y, "Join", "accent")
    ctrl_bot = y

    # ================================================== join to the action ==
    y_act_top = ctrl_bot - H_JOIN
    jm = (ctrl_bot + y_act_top) / 2
    for n, x, text in ((2, cx[0], "drawn dwell time"), (3, cx[1], "verb")):
        w(r"\draw[->,black!55,line width=0.9pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, ctrl_bot - 0.08, x, y_act_top + 0.08))
        badge(w, x + 0.34, jm, n)
        w(r"\node[anchor=west,text=black!58] at (%.3f,%.3f) {%s};" % (x + 0.62, jm, text))
    xv = cx[2]
    y_split = y_act_top + 0.50
    w(r"\draw[->,black!55,line width=0.9pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (xv, y_act_top + 0.08, xv, ctrl_bot - 0.08))
    badge(w, xv - 0.34, y_act_top + 0.26, 4)
    w(r"\node[anchor=east,text=black!58] at (%.3f,%.3f) {verdict};" % (xv - 0.62, y_act_top + 0.26))
    w(r"\node[anchor=east,text=black!58] at (%.3f,%.3f) {failure};" % (xv - 0.14, ctrl_bot - 0.34))
    # The success arm bypasses the controller band on the right, then turns
    # back INTO the movement band and lands beside (5): on success the token
    # routes on the base weights, so the arrow must reach the net, not stop
    # at the band's corner (Marc, 2026-09-08: "make sure the success arrow
    # is drawn and goes to the right place"). It re-enters below the
    # "re-weighting" label so the two never cross.
    byp_x = BAND_R + 0.36
    x_s = BAND_R - 0.45
    y_land = ctrl_top + 0.30
    w(r"\draw[->,black!55,line width=0.9pt,rounded corners=3pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);"
      % (xv, y_split, byp_x, y_split, byp_x, y_land, x_s, y_land, x_s, mv_bot - 0.08))
    w(r"\node[rotate=90,anchor=center,text=black!58] at (%.3f,%.3f) {success};" % (byp_x + 0.26, (y_split + y_land) / 2))

    # ===================================================== the action layer ==
    act_top = y_act_top
    band(w, act_top, act_top - H_ACT, "black!22", "black!4")
    rot_label(w, act_top, act_top - H_ACT, "MTDSim", "black!55")
    boxes = ["Attacker", "Network", "Defender"]
    bw = 3.2
    bxs = [BAND_L + 0.7 + bw / 2, (BAND_L + BAND_R) / 2, BAND_R - 0.7 - bw / 2]
    by_c = act_top - H_ACT / 2 - 0.12
    for title, bx in zip(boxes, bxs):
        w(r"\draw[black!38,fill=white,line width=0.5pt,rounded corners=1.6pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"
          % (bx - bw / 2, by_c - 0.40, bx + bw / 2, by_c + 0.40))
        w(r"\node at (%.3f,%.3f) {%s};" % (bx, by_c, title))
    for i in (0, 2):
        x1 = bxs[i] + (bw / 2 if i == 0 else -bw / 2)
        x2 = bxs[1] + (-bw / 2 if i == 0 else bw / 2)
        w(r"\draw[<->,black!45,line width=0.55pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (x1 + 0.06 * (1 if i == 0 else -1), by_c, x2 + 0.06 * (-1 if i == 0 else 1), by_c))
    w(r"\node[anchor=north,text=black!50] at (%.3f,%.3f) {inherited from MTDSim};" % ((BAND_L + BAND_R) / 2, act_top - 0.08))
    act_bot = act_top - H_ACT

    # ---- the L4 bracket ------------------------------------------------------
    w(r"\draw[black!45,line width=0.45pt,decorate,decoration={brace,amplitude=3.5pt,mirror}] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (GUT_R + 0.04, ctrl_top, GUT_R + 0.04, act_bot))
    w(r"\node[anchor=east,align=right] at (%.3f,%.3f) {\textbf{L4}};"
      % (GUT_R - 0.16, (ctrl_top + act_bot) / 2))

    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    facts["height_cm"] = abs(act_bot) + 0.1
    facts["width_cm"] = byp_x + 0.5 - ROT_X + 0.2
    return "\n".join(L) + "\n", facts


# ------------------------------------------------------------------- main --
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mapping", default="v2_partial")
    ap.add_argument("--overlay-version", default="v4_failure_only")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    gap, order = load_gap()
    axis = load_axis()
    axis.check_against(order)
    # the fragment: the same profile fig:pipeline draws (flow A's class), same window rule
    from pipeline_ladder_figure import flow_graphs, pick_pair
    cls = load_classes()
    tech, edges = flow_graphs(gap)
    fa, _fb, _shared = pick_pair(tech, edges, cls)
    prof = cls[fa]
    net = load_net(prof)
    win = net_window(net, order)
    durations = load_durations()
    mapping, verbs = load_mapping(args.mapping)
    fmatrix, n_rules = failure_cells(order, args.overlay_version)
    missing = [t for t in order if t not in durations or t not in mapping]
    if missing:
        raise SystemExit(f"tactics absent from the dwell catalogue or the mapping: {missing}")

    tex, facts = emit(order, axis, net, win, durations, mapping, verbs, fmatrix, n_rules,
                      args.mapping, args.overlay_version)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{STEM}.tex"
    path.write_text(tex)
    print(f"wrote {path.relative_to(REPO)}")
    if not args.no_compile:
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                            f"-output-directory={OUT_DIR}", str(path)], capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-3000:])
            raise SystemExit("pdflatex failed")
        for ext in (".aux", ".log"):
            (OUT_DIR / f"{STEM}{ext}").unlink(missing_ok=True)
        print(f"wrote {(OUT_DIR / (STEM + '.pdf')).relative_to(REPO)}")

    print("--- facts (all read from tracked artefacts) ---")
    print(f"ATT&CK bundle                : v{axis.version}, {len(order)} tactics")
    np_, nt, win = facts["net"]
    print(f"net drawn                    : {PROFILE_LABEL[prof]} -- {np_} places, {nt} transitions; fragment {win}")
    print(f"dwell catalogue              : {len(durations)} tactics, {sum(1 for v in durations.values() if v == 0)} at zero")
    mv, nm, nd, nv = facts["mapping"]
    print(f"mapping ({mv})       : {nm} mapped, {nd} dwell-only, {nv} verbs")
    ov, nr, nrule = facts["failure"]
    print(f"failure matrix ({ov}) : {nr} x {nr - 1} ordered pairs, {nrule} rules")
    print(f"drawn size                   : ~{facts['width_cm']:.2f} x {facts['height_cm']:.2f} cm (type {F} = 10pt at natural size)")


if __name__ == "__main__":
    main()
