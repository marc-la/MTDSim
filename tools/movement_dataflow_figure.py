#!/usr/bin/env python3
"""Dissertation figure: the movement attacker's runtime loop
(fig:movement-dataflow, the Mechanics subsection's primary figure).

The figure draws the runtime choreography of the movement attacker --- the
loop the Mechanics prose walks in one sentence --- as a data-flow diagram
across the three runtime layers:

  MOVEMENT LAYER    a schematic generalised stochastic Petri net: places,
                    transitions, the token on its current tactic-place and
                    its weighted out-transitions. Schematic by ruling
                    (2026-08-20, L3 carries no figure): NOT a profile's net.
  CONTROLLER LAYER  the three declared inputs as abstract glyphs, in the
                    order the loop consults them: dwell times (file + the
                    exponential curve), the tactic-to-verb mapping (a small
                    bipartite pair with one unconnected tactic --- the
                    dwell-only motif), the failure matrix (a small grid).
  ACTION LAYER      the inherited simulator: attacker / network / defender,
                    with the attacker model the loop's anchor.

Six numbered edges trace the loop, downward on the left and upward on the
right, matching the prose's order: (1) the token's tactic enters the
controller; (2) the drawn dwell time goes down to the simulator and is
consumed; (3) the mapping resolves a verb --- or dwell-only: nothing is
dispatched and no verdict will return; (4) the verdict comes up from the
attacker model; (5) on failure the matrix re-weights the token's
out-transitions (the success arm bypasses the controller band entirely ---
drawn around it, the base proportions stand); (6) the token fires and the
loop repeats.

Directionality is deliberate (the component brief's considerations): the
mapping edge is one-way down, the verdict is its own upward edge --- never a
bidirectional arrow --- and the dwell-only branch is visible twice (the open
dot in the mapping glyph, the "no verdict returns" line at edge 3), because
a loop drawn verdict-always would contradict the prose beside it. The
20-second confusion penalty is deliberately NOT drawn: it is the
substrate-side timing exception the prose owns.

Deliberately not drawn here (the sibling figures own them): the controller
inputs' anatomy --- real bars, real mapping rows, real matrix cells --- is
fig:pipeline's and fig:controller-mapping's; every glyph here is an abstract
emblem carrying no artefact values, so nothing on the face is typed. The
artefacts are still loaded at build time: the drawing's claims (a partial
mapping with dwell-only tactics, a declared dwell catalogue, a failure rule
set) are validated against the tracked artefacts, and the caption's pins are
printed as a fact sheet rather than remembered.

Usage:
  PYTHONPATH=src python tools/movement_dataflow_figure.py
      [--mapping v2_partial] [--overlay-version v4_failure_only]
      [--no-compile]

Style: TikZ at the document's 12 pt base, greys carry the structure, one
accent (RGB 31,84,140); movement-bound edges take the accent, action-bound
edges stay grey (the fig:pipeline join convention). Written to
docs/thesis/figures/fig_4-2-4c_movement_dataflow.tex (+ .pdf unless --no-compile).
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

from mtdsim.l3_simulation.controller.outcome import load_overlay_registry  # noqa: E402
from mtdsim.l3_simulation.controller.rules import load_rule_set  # noqa: E402

GAP_JSON = REPO / "data" / "gap" / "gap_v0.5.json"
DURATIONS_JSON = REPO / "data" / "ogasp" / "tactic_durations.json"
MAPPING_DIR = REPO / "data" / "ogasp" / "controller" / "mappings"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-2-4c_movement_dataflow"

# --- geometry (cm) ---------------------------------------------------------
ROT_X = 0.30            # x of the rotated band labels
BAND_L = 0.85           # left edge of the content bands
BAND_R = 14.80          # right edge of the content bands
BYP_X = 15.20           # the success bypass runs outside the bands

MV_TOP, MV_BOT = 0.00, -3.10        # movement band
CTRL_TOP, CTRL_BOT = -4.70, -7.35   # controller band
ACT_TOP, ACT_BOT = -8.85, -11.05    # action band

ACCENT_EDGE = "accent!75"           # movement-bound loop edges
GREY_EDGE = "black!55"              # action-bound loop edges
LABEL = "black!58"                  # secondary text


# ------------------------------------------------------------------ loading --
def load_order() -> list[str]:
    gap = json.loads(GAP_JSON.read_text())
    layer_of = {n["primary_tactic"]: n["tactic_layer"] for n in gap["nodes"].values()}
    return sorted(layer_of, key=layer_of.get)


def load_durations(order: list[str]) -> dict[str, float]:
    doc = json.loads(DURATIONS_JSON.read_text())
    out = {k: float(v["duration_s"]) for k, v in doc["tactics"].items()}
    missing = [t for t in order if t not in out]
    if missing:
        raise SystemExit(f"tactics absent from the dwell catalogue: {missing}")
    return out


def load_mapping(version: str) -> tuple[int, int, int]:
    """(mapped, dwell-only, verbs). Refuses the registry-invariant break, and
    refuses a mapping that would falsify a drawn branch: both the verb branch
    and the dwell-only branch appear in the figure, so both must exist."""
    rows = list(csv.DictReader((MAPPING_DIR / f"{version}.csv").open(encoding="utf-8")))
    verbs: set[str] = set()
    n_mapped = n_dwell = 0
    for r in rows:
        verb = (r["sim_phase"] or "").strip()
        if verb:
            n_mapped += 1
            verbs.add(verb)
        elif r["disposition"].strip() == "dwell-only":
            n_dwell += 1
        else:
            raise SystemExit(f"{version}: {r['tactic']} is silent without a "
                             "dwell-only disposition -- the registry invariant is broken")
    if not n_mapped or not n_dwell:
        raise SystemExit(f"{version}: both drawn branches must exist "
                         f"(mapped={n_mapped}, dwell-only={n_dwell})")
    return n_mapped, n_dwell, len(verbs)


def count_failure_rules(version: str) -> int:
    reg = load_overlay_registry()
    if not any(v.name == version for v in reg.versions):
        raise SystemExit(f"unknown overlay version {version!r}")
    return len(load_rule_set().order["failure"])


# ------------------------------------------------------------- primitives --
def band(w, y_top, y_bot, colour, fill=None):
    opt = f"draw={colour},line width=0.4pt,rounded corners=1.6pt"
    if fill:
        opt += f",fill={fill}"
    w(r"\draw[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
      % (opt, BAND_L, y_bot, BAND_R, y_top))


def rot_label(w, y_top, y_bot, text, colour):
    w(r"\node[rotate=90,anchor=center,font=\scriptsize,text=%s] at (%.3f,%.3f) {%s};"
      % (colour, ROT_X, (y_top + y_bot) / 2, text))


def badge(w, x, y, n):
    w(r"\node[circle,draw=black!60,text=black!70,inner sep=0.5pt,"
      r"minimum size=8.5pt,line width=0.35pt,font=\scriptsize] at (%.3f,%.3f) {%d};"
      % (x, y, n))


def note(w, x, y, text, anchor="west", colour=LABEL, align=None):
    a = f",align={align}" if align else ""
    w(r"\node[anchor=%s,font=\scriptsize,text=%s%s] at (%.3f,%.3f) {%s};"
      % (anchor, colour, a, x, y, text))


def edge(w, pts, colour, arrow=True, lw=0.7):
    head = "->" if arrow else "-"
    path = " -- ".join("(%.3f,%.3f)" % p for p in pts)
    w(r"\draw[%s,%s,line width=%.2fpt,rounded corners=3pt] %s;" % (head, colour, lw, path))


# ------------------------------------------------------------------ bands --
def emit() -> tuple[str, dict]:
    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usetikzlibrary{arrows.meta,positioning,calc}")
    w(r"\definecolor{accent}{RGB}{31,84,140}")
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,>={Stealth[length=1.7mm]},"
      r"every node/.style={font=\scriptsize}]")

    # =============================================== the movement layer ==
    band(w, MV_TOP, MV_BOT, "accent!45")
    rot_label(w, MV_TOP, MV_BOT, "Movement layer", "accent")
    note(w, (BAND_L + BAND_R) / 2, MV_TOP - 0.06,
         "a profile's generalised stochastic Petri net, drawn schematically",
         anchor="north", colour="black!50")

    # the schematic net: prev place -> fired transition -> current place
    # (token) -> three weighted out-transitions -> candidate places
    ny = -1.78
    p0, t0, cur = (4.60, ny), (5.85, ny), (7.10, ny)
    outs = [(9.40, -1.03), (9.40, ny), (9.40, -2.53)]
    cands = [(11.40, -1.03), (11.40, ny), (11.40, -2.53)]
    r_pl = 0.14

    def place(x, y, colour="black!62"):
        w(r"\draw[%s,fill=white,line width=0.45pt] (%.3f,%.3f) circle (%.3f);"
          % (colour, x, y, r_pl))

    def trans(x, y, colour="black!72"):
        w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
          % (colour, x - 0.030, y - 0.13, x + 0.030, y + 0.13))

    # travelled history, faded
    w(r"\draw[black!35,line width=0.4pt,->] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (p0[0] + r_pl, p0[1], t0[0] - 0.05, t0[1]))
    w(r"\draw[black!35,line width=0.4pt,->] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (t0[0] + 0.05, t0[1], cur[0] - r_pl, cur[1]))
    place(*p0, colour="black!40")
    trans(*t0, colour="black!45")
    # the current place and its weighted out-arcs
    for (tx, ty), lw_ in zip(outs, (0.95, 0.55, 0.30)):
        w(r"\draw[black!55,line width=%.2fpt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (lw_, cur[0] + r_pl * 0.85, cur[1] + (0.09 if ty > ny else -0.09 if ty < ny else 0),
             tx - 0.05, ty))
    for (tx, ty), (px, py) in zip(outs, cands):
        w(r"\draw[black!45,line width=0.4pt,->] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (tx + 0.05, ty, px - r_pl, py))
    place(*cur)
    for o in outs:
        trans(*o)
    for c in cands:
        place(*c)
    # the net continues both ways
    for x0 in (3.55, 12.00):
        for k in range(3):
            w(r"\fill[black!35] (%.3f,%.3f) circle (0.35pt);" % (x0 + 0.22 * k, ny))
    # the token
    w(r"\fill[accent] (%.3f,%.3f) circle (0.055);" % cur)
    note(w, cur[0], cur[1] + r_pl + 0.05, "token", anchor="south", colour="accent")
    note(w, cur[0], cur[1] - r_pl - 0.05, "current tactic", anchor="north")
    note(w, outs[1][0], -2.78, "weighted out-transitions", anchor="north")
    # (6) the token fires the chosen transition
    edge(w, [(cur[0] + r_pl * 0.85, cur[1] + 0.09), outs[0],
             (cands[0][0] - r_pl, cands[0][1])], ACCENT_EDGE, lw=0.75)
    badge(w, 10.30, -0.62, 6)
    note(w, 10.52, -0.62, "next tactic")

    # ==================================== gap 1: tactic down, weights up ==
    fan_y = -3.95
    x_dwell, x_map, x_mat = 3.48, 7.83, 12.18
    # (1) the selected tactic enters the controller (both lookups)
    edge(w, [(cur[0], MV_BOT - 0.08), (cur[0], fan_y), (x_dwell, fan_y),
             (x_dwell, CTRL_TOP + 0.08)], ACCENT_EDGE)
    edge(w, [(cur[0], fan_y), (x_map, fan_y), (x_map, CTRL_TOP + 0.08)],
         ACCENT_EDGE)
    badge(w, cur[0] + 0.28, -3.52, 1)
    note(w, cur[0] + 0.46, -3.52, "tactic")
    # (5) failure re-weights the out-transitions
    edge(w, [(x_mat, CTRL_TOP - 0.08), (x_mat, MV_BOT + 0.08)], ACCENT_EDGE)
    badge(w, x_mat - 0.28, fan_y, 5)
    note(w, x_mat - 0.46, fan_y, r"re-weighted, renormalised", anchor="east")
    # the success arm: base weights stand, the controller is bypassed
    edge(w, [(BYP_X, -8.05), (BYP_X, -3.60), (14.30, -3.60),
             (14.30, MV_BOT + 0.08)], ACCENT_EDGE)
    w(r"\node[rotate=90,anchor=center,font=\scriptsize,text=%s] at (%.3f,%.3f) "
      r"{success: base proportions stand};" % (LABEL, BYP_X + 0.22, -5.85))

    # ============================================== the controller layer ==
    band(w, CTRL_TOP, CTRL_BOT, "accent!45")
    rot_label(w, CTRL_TOP, CTRL_BOT, "Controller layer", "accent")
    cell_w = (BAND_R - BAND_L - 0.9) / 3
    for i in (1, 2):
        sx = BAND_L + 0.45 + cell_w * i
        w(r"\draw[black!22,line width=0.35pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (sx, CTRL_TOP - 0.18, sx, CTRL_BOT + 0.16))
    head_y = CTRL_TOP - 0.32
    body_top, body_bot = CTRL_TOP - 0.62, CTRL_BOT + 0.72
    foot_y = CTRL_BOT + 0.44

    # (i) dwell times: a flat file + the exponential curve, as emblems
    note(w, x_dwell, head_y, "Dwell times", anchor="center", colour="black")
    fx0, fy0, fw, fh = x_dwell - 1.15, body_bot + 0.10, 0.95, body_top - body_bot - 0.20
    w(r"\draw[black!40,line width=0.35pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"
      % (fx0, fy0, fx0 + fw, fy0 + fh))
    for k in range(4):
        ly = fy0 + fh - 0.24 * (k + 1)
        w(r"\draw[black!45,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (fx0 + 0.14, ly, fx0 + fw - 0.14, ly))
    ex0, ey0, ew, eh = x_dwell + 0.35, body_bot + 0.12, 1.00, body_top - body_bot - 0.28
    w(r"\draw[black!30,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);"
      % (ex0, ey0 + eh, ex0, ey0, ex0 + ew, ey0))
    pts = ["(%.3f,%.3f)" % (ex0 + u / 30 * ew, ey0 + eh * math.exp(-3.1 * u / 30))
           for u in range(31)]
    w(r"\draw[black!70,line width=0.6pt] " + " -- ".join(pts) + ";")
    note(w, x_dwell, foot_y, "per-tactic mean, exponential draw",
         anchor="north", align="center")

    # (ii) the mapping: a small bipartite pair, one tactic unconnected
    note(w, x_map, head_y, "Tactic-to-verb mapping", anchor="center", colour="black")
    lx, rx = x_map - 0.85, x_map + 0.85
    lys = [body_top - 0.10 - 0.30 * k for k in range(5)]
    rys = [body_top - 0.22 - 0.44 * k for k in range(3)]
    for i, j in ((0, 0), (1, 1), (3, 1), (4, 2)):
        w(r"\draw[black!45,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (lx, lys[i], rx, rys[j]))
    for k, ly in enumerate(lys):
        if k == 2:  # the dwell-only motif: connected to nothing
            w(r"\draw[black!42,line width=0.35pt] (%.3f,%.3f) circle (1.0pt);" % (lx, ly))
        else:
            w(r"\fill[black!68] (%.3f,%.3f) circle (1.0pt);" % (lx, ly))
    for ry in rys:
        w(r"\fill[black!68] (%.3f,%.3f) circle (1.2pt);" % (rx, ry))
    note(w, lx - 0.16, (body_top + body_bot) / 2, "tactics", anchor="east")
    note(w, rx + 0.16, (body_top + body_bot) / 2, "verbs", anchor="west")
    note(w, x_map, foot_y, "partial: some tactics dwell-only",
         anchor="north", align="center")

    # (iii) the failure matrix: a small grid, as an emblem
    note(w, x_mat, head_y, "Failure matrix", anchor="center", colour="black")
    n, cs = 5, 0.27
    mx0, my0 = x_mat - n * cs / 2, (body_top + body_bot) / 2 + n * cs / 2
    for i in range(n):
        for j in range(n):
            if i == j:
                fill = "black!8"
            else:
                fill = ("black!55", "black!30", "black!14", "black!42")[(i + 2 * j) % 4]
            w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
              % (fill, mx0 + j * cs, my0 - (i + 1) * cs, mx0 + (j + 1) * cs, my0 - i * cs))
    w(r"\draw[black!35,line width=0.3pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"
      % (mx0, my0 - n * cs, mx0 + n * cs, my0))
    note(w, x_mat, foot_y, "applied on failure only", anchor="north", align="center")

    # ================================ gap 2: time and verb down, verdict up ==
    # (2) the drawn dwell time is consumed by the simulator
    edge(w, [(x_dwell, CTRL_BOT - 0.08), (x_dwell, ACT_TOP + 0.08)], GREY_EDGE)
    badge(w, x_dwell - 0.28, -8.10, 2)
    note(w, x_dwell - 0.46, -8.10, "drawn dwell time", anchor="east")
    # (3) the mapping resolves one way, downward
    edge(w, [(x_map, CTRL_BOT - 0.08), (x_map, ACT_TOP + 0.08)], GREY_EDGE)
    badge(w, x_map - 0.28, -7.78, 3)
    w(r"\node[anchor=east,align=right,font=\scriptsize,text=%s] at (%.3f,%.3f) "
      r"{verb\\dwell-only: none ---\\no verdict returns};" % (LABEL, x_map - 0.46, -8.16))
    # (4) the verdict comes up from the attacker model
    x_verd = 8.75
    verd_y = -8.05
    edge(w, [(x_verd, ACT_TOP + 0.08), (x_verd, verd_y), (x_mat - 0.06, verd_y)],
         GREY_EDGE, arrow=False)
    w(r"\fill[black!55] (%.3f,%.3f) circle (1.1pt);" % (x_mat, verd_y))
    badge(w, 10.35, -7.82, 4)
    note(w, 10.57, -7.82, "verdict")
    # the split: failure into the matrix, success around the band
    edge(w, [(x_mat, verd_y), (x_mat, CTRL_BOT - 0.08)], GREY_EDGE)
    note(w, x_mat + 0.14, -7.60, "failure")
    edge(w, [(x_mat + 0.06, verd_y), (BYP_X, verd_y)], ACCENT_EDGE, arrow=False)
    note(w, 13.90, verd_y - 0.09, "success", anchor="north", colour=LABEL)

    # ================================================== the action layer ==
    band(w, ACT_TOP, ACT_BOT, "black!22", "black!4")
    rot_label(w, ACT_TOP, ACT_BOT, "Action layer", "black!55")
    note(w, (BAND_L + BAND_R) / 2, ACT_TOP - 0.06,
         "inherited from MTDSim, the discrete-event simulator",
         anchor="north", colour="black!50")
    by_c = -10.10
    boxes = [
        ("Attacker", "executes the verb over the drawn time", 2.40, 8.90),
        ("Network", r"hosts, services,\\vulnerabilities", 9.55, 11.85),
        ("Defender", r"moving target\\defence", 12.30, 14.50),
    ]
    for title, sub, xl, xr in boxes:
        w(r"\draw[black!38,fill=white,line width=0.4pt,rounded corners=1.4pt] "
          r"(%.3f,%.3f) rectangle (%.3f,%.3f);" % (xl, by_c - 0.58, xr, by_c + 0.58))
        w(r"\node[font=\scriptsize,align=center,text width=%.2fcm] at (%.3f,%.3f) "
          r"{%s\\[1.5pt]\color{black!58}%s};"
          % (xr - xl - 0.16, (xl + xr) / 2, by_c, title, sub))
    for x1, x2 in ((8.90, 9.55), (11.85, 12.30)):
        w(r"\draw[<->,black!45,line width=0.5pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (x1 + 0.05, by_c, x2 - 0.05, by_c))

    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    facts = {"width_cm": BYP_X + 0.45 - ROT_X, "height_cm": abs(ACT_BOT) + 0.3}
    return "\n".join(L) + "\n", facts


# ------------------------------------------------------------------- main --
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mapping", default="v2_partial", help="controller mapping version")
    ap.add_argument("--overlay-version", default="v4_failure_only",
                    help="outcome-overlay version behind the failure-matrix glyph")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    order = load_order()
    durations = load_durations(order)
    n_mapped, n_dwell, n_verbs = load_mapping(args.mapping)
    n_rules = count_failure_rules(args.overlay_version)

    tex, facts = emit()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{STEM}.tex"
    path.write_text(tex)
    print(f"wrote {path.relative_to(REPO)}")

    if not args.no_compile:
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                            f"-output-directory={OUT_DIR}", str(path)],
                           capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-3000:])
            raise SystemExit("pdflatex failed")
        for ext in (".aux", ".log"):
            (OUT_DIR / f"{STEM}{ext}").unlink(missing_ok=True)
        print(f"wrote {(OUT_DIR / (STEM + '.pdf')).relative_to(REPO)}")

    # --- the fact sheet the caption's pins come from ------------------------
    print("--- facts (validated against tracked artefacts; none drawn) ---")
    print(f"dwell catalogue         : {len(durations)} tactics, all declared")
    print(f"mapping ({args.mapping})   : {n_mapped} mapped, {n_dwell} dwell-only, "
          f"{n_verbs} verbs")
    print(f"failure rules ({args.overlay_version}): {n_rules} rules")
    print(f"drawn size              : {facts['width_cm']:.2f} x {facts['height_cm']:.2f} cm")


if __name__ == "__main__":
    main()
