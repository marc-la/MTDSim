#!/usr/bin/env python3
"""Dissertation figure: the thesis ladder --- the movement attacker from
campaign intelligence to a traversal inside MTDSim (the ch4 opening figure,
fig:pipeline).

The figure is the *definition* of the thesis ladder (Marc's ruling,
2026-08-16), so it draws thesis numbering only --- L0--L1 intelligence to
graph, L2 attack profiles, L3 the generalised stochastic Petri net, L4 the
attacker-agent traversal in MTDSim --- and never the repo's numbering
(architecture.md (b) records the divergence).

Three bands, top to bottom, on one shared tactic axis:

  MOVEMENT LAYER (built)
    L0  the campaign corpus      --- one row per attack flow, a mark in every
                                     tactic the analyst drew
    L1  the attack graph         --- technique nodes in their tactic column,
                                     edges faded by how many flows drew them
    L2  the attack profiles      --- one row per objective class, forward
                                     transitions above the line and backward
                                     below, the objective tactic accented
    L3  the Petri net            --- tactics become places, moves become
                                     transitions, one token, the pre-intrusion
                                     overlay drawn in dashed
  CONTROLLER LAYER (built)       --- the three declared inputs as glyphs:
                                     dwell times and the exponential draw, the
                                     tactic-to-verb mapping, the failure matrix
  ACTION LAYER (inherited)       --- attacker / network / defender, subdued

and the two-way join between them (tactic down, re-weighting up; verb down,
verdict up).

Every number and every mark is read from a tracked artefact --- the GAP, the
structural nets, the synthetic overlay, the dwell catalogue, the controller
mapping registry and the outcome-overlay rule set. Nothing is typed. The
numbers a caption may quote are printed to stdout.

Deliberately NOT drawn here (they belong to the sibling figures): the runtime
loop's choreography (fig:movement-dataflow), the mapping row by row
(fig:controller-mapping), the failure weights cell by cell
(fig:failure-matrix). This figure is the ladder; those are the mechanics.

Usage:
  PYTHONPATH=src python tools/pipeline_ladder_figure.py [--profile NAME]
      [--mapping v2_partial] [--overlay-version v4_failure_only] [--no-compile]

Style: TikZ at the document's 12 pt base, greys carry the structure, one
accent (RGB 31,84,140) marks what this thesis builds. Written to
docs/thesis/figures/fig_4-0a_pipeline_ladder.tex (+ .pdf unless --no-compile).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from mtdsim.l3_simulation.controller.outcome import load_overlay_registry  # noqa: E402
from mtdsim.l3_simulation.controller.rules import (  # noqa: E402
    compile_pair,
    load_rule_set,
    spec_from_registry_entry,
)

GAP_JSON = REPO / "data" / "gap" / "gap_v0.5.json"
PETRI_DIR = REPO / "data" / "ogasp" / "petri"
OVERLAY_JSON = PETRI_DIR / "synthetic_overlay.json"
DURATIONS_JSON = REPO / "data" / "ogasp" / "tactic_durations.json"
MAPPING_DIR = REPO / "data" / "ogasp" / "controller" / "mappings"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-0a_pipeline_ladder"

# The four objective classes, in the order the chapter names them
# (subsec:attack-profiles). Presentation names are the chapter's own words ---
# never the class identifiers, which are code (conventions §g).
PROFILE_ORDER = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
)
PROFILE_LABEL = {
    "objective_exfiltration": "Exfiltration objective",
    "objective_impact": "Impact objective",
    "objective_exfiltration_impact": "Double extortion",
    "objective_none_c2": "No realised objective",
}
# The declared objective tactic(s) each class is analysed against
# (OBJECTIVE_TACTICS, petri/analysis.py) --- what distinguishes the profiles.
OBJECTIVE_TACTICS = {
    "objective_exfiltration": ("exfiltration",),
    "objective_impact": ("impact",),
    "objective_exfiltration_impact": ("exfiltration", "impact"),
    "objective_none_c2": ("command-and-control",),
}

# --- geometry (cm) ---------------------------------------------------------
GUT_R = 4.95            # right edge of the label gutter (labels right-aligned)
GUT_W = 4.25            # wrapping width of a gutter label
BAND_L = 5.10           # left edge of the content bands
BAND_R = 15.55          # right edge of the content bands
AX0, AX1 = 5.38, 15.25  # the shared tactic axis
ROT_X = 0.16            # x of the rotated band labels

H_AXIS = 0.46           # the tactic-axis strip
H_L0 = 2.20             # 38 flow rows
H_L1 = 2.14             # technique scatter
H_L2_ROW = 0.66         # one profile row
H_L3 = 1.56             # the net
H_ARROW = 0.52          # a between-rung arrow
H_JOIN = 0.94           # a between-band join
H_CTRL = 3.20           # the controller band
H_ACT = 2.34            # the action band
PAD = 0.20              # band padding above the first rung / below the last

ACCENT = "accent"
WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
        7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def esc(s: str) -> str:
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&")
             .replace("%", r"\%").replace("#", r"\#").replace("_", r"\_"))


# ---------------------------------------------------------------- loading --
def load_gap() -> tuple[dict, list[str]]:
    gap = json.loads(GAP_JSON.read_text())
    layer_of = {n["primary_tactic"]: n["tactic_layer"] for n in gap["nodes"].values()}
    order = sorted(layer_of, key=layer_of.get)
    return gap, order


def load_nets() -> dict[str, dict]:
    return {p: json.loads((PETRI_DIR / f"{p}_structural.json").read_text())
            for p in PROFILE_ORDER}


def load_overlay_edges() -> list[tuple[str, str, str]]:
    """The declared pre-intrusion edges, as (src, dst, direction). The guard
    rule adds the same three edges wherever it fires, so the union over the
    profiles is the overlay itself."""
    doc = json.loads(OVERLAY_JSON.read_text())
    seen: dict[tuple[str, str], str] = {}
    for prof in doc["profiles"].values():
        for t in prof.get("synthetic_transitions", []):
            seen[(t["src_tactic"], t["dst_tactic"])] = t["direction"]
    return [(s, d, dirn) for (s, d), dirn in seen.items()]


def load_durations() -> dict[str, float]:
    doc = json.loads(DURATIONS_JSON.read_text())
    return {k: float(v["duration_s"]) for k, v in doc["tactics"].items()}


def load_mapping(version: str) -> tuple[dict[str, str | None], list[str]]:
    """tactic -> verb (or None for dwell-only), plus the verbs in first-use
    order. Refuses a row that is silent without declaring dwell-only (the
    registry's own invariant)."""
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


def failure_cells(order: list[str], version: str) -> dict[tuple[str, str], float]:
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
def bez(w, x1, y1, x2, y2, h, style):
    """A shallow arc from (x1,y1) to (x2,y2) bulging by h (signed)."""
    dx = x2 - x1
    c1 = (x1 + 0.28 * dx, y1 + h)
    c2 = (x2 - 0.28 * dx, y2 + h)
    w(r"\draw[%s] (%.3f,%.3f) .. controls (%.3f,%.3f) and (%.3f,%.3f) .. (%.3f,%.3f);"
      % (style, x1, y1, c1[0], c1[1], c2[0], c2[1], x2, y2))


def band(w, y_top, y_bot, colour, fill=None):
    opt = f"draw={colour},line width=0.4pt,rounded corners=1.6pt"
    if fill:
        opt += f",fill={fill}"
    w(r"\draw[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
      % (opt, BAND_L, y_bot, BAND_R, y_top))


def rot_label(w, y_top, y_bot, text, colour):
    w(r"\node[rotate=90,anchor=center,font=\scriptsize,text=%s] at (%.3f,%.3f) {%s};"
      % (colour, ROT_X, (y_top + y_bot) / 2, text))


def gutter(w, y, title, sub=None):
    body = title if sub is None else r"%s\\[1pt]\color{black!58}%s" % (title, sub)
    # \\ must stay at the node's top brace level, so the colour switch is
    # applied un-grouped rather than wrapped around the whole sub-line.
    w(r"\node[anchor=east,align=right,text width=%.2fcm,font=\scriptsize] "
      r"at (%.3f,%.3f) {%s};" % (GUT_W, GUT_R, y, body))


def foot(w, x, y, width, text):
    """A cell's fact line, centred and wrapped inside the cell."""
    # one centred line; the caller keeps the text inside its cell (checked at
    # render, since a wrap here would hang below the band).
    assert width > 0
    w(r"\node[anchor=north,font=\scriptsize,text=black!58] at (%.3f,%.3f) {%s};"
      % (x, y + 0.10, text))


def down_arrow(w, x, y_from, y_to, label, colour="black!55", side="right"):
    w(r"\draw[->,%s,line width=0.5pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (colour, x, y_from, x, y_to))
    anchor, dx = ("west", 0.10) if side == "right" else ("east", -0.10)
    w(r"\node[anchor=%s,font=\scriptsize,text=black!58] at (%.3f,%.3f) {%s};"
      % (anchor, x + dx, (y_from + y_to) / 2, label))


# ------------------------------------------------------------------ bands --
def emit(gap, order, nets, overlay_edges, durations, mapping, verbs,
         fmatrix, n_rules, profile, mapping_version, overlay_version) -> tuple[str, dict]:
    col = {t: AX0 + i * (AX1 - AX0) / (len(order) - 1) for i, t in enumerate(order)}
    tac_of = {tid: n["primary_tactic"] for tid, n in gap["nodes"].items()}

    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usetikzlibrary{arrows.meta,positioning,calc,decorations.pathreplacing}")
    w(r"\definecolor{accent}{RGB}{31,84,140}")
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,>={Stealth[length=1.5mm]},"
      r" every node/.style={font=\scriptsize,inner sep=0pt}]")

    facts: dict[str, object] = {}
    y = 0.0

    # ============================================== the movement layer band ==
    mv_top = y
    y -= PAD

    # ---- the shared tactic axis -----------------------------------------
    y -= H_AXIS * 0.62
    w(r"\draw[black!30,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (AX0 - 0.12, y, AX1 + 0.12, y))
    for t in order:
        w(r"\draw[black!30,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (col[t], y, col[t], y - 0.07))
    w(r"\node[anchor=south west,font=\scriptsize,text=black!58] at (%.3f,%.3f) {reconnaissance};"
      % (AX0 - 0.10, y + 0.07))
    w(r"\node[anchor=south east,font=\scriptsize,text=black!58] at (%.3f,%.3f) {impact};"
      % (AX1 + 0.10, y + 0.07))
    w(r"\node[anchor=south,font=\scriptsize,text=black!58] at (%.3f,%.3f) "
      r"{the fifteen tactics, in kill-chain order};" % ((AX0 + AX1) / 2, y + 0.07))
    y -= H_AXIS * 0.38

    # ---- L0: one row per attack flow -------------------------------------
    flows: dict[str, set[str]] = defaultdict(set)
    for tid, n in gap["nodes"].items():
        for fid in n["flow_ids"]:
            flows[fid].add(n["primary_tactic"])
    idx = {t: i for i, t in enumerate(order)}
    rows = sorted(flows.items(),
                  key=lambda kv: (min(idx[t] for t in kv[1]),
                                  max(idx[t] for t in kv[1]), kv[0]))
    facts["flows"] = len(rows)
    y0 = y - 0.10
    pitch0 = (H_L0 - 0.20) / (len(rows) - 1)
    for k, (_fid, tset) in enumerate(rows):
        ry = y0 - k * pitch0
        xs = sorted(col[t] for t in tset)
        w(r"\draw[black!30,line width=0.22pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (xs[0], ry, xs[-1], ry))
        for x in xs:
            w(r"\fill[black!72] (%.3f,%.3f) circle (0.55pt);" % (x, ry))
    gutter(w, y0 - (H_L0 - 0.20) / 2, r"\textbf{L0} \enspace Campaign intelligence",
           r"%d attack flows" % len(rows))
    y -= H_L0

    # ---- arrow -----------------------------------------------------------
    down_arrow(w, (AX0 + AX1) / 2, y - 0.06, y - H_ARROW + 0.06, "aggregate")
    y -= H_ARROW

    # ---- L1: the technique-level attack graph ----------------------------
    by_tactic: dict[str, list[str]] = defaultdict(list)
    for tid, t in tac_of.items():
        by_tactic[t].append(tid)
    for t in by_tactic:
        by_tactic[t].sort()
    top, bot = y - 0.14, y - H_L1 + 0.14
    pos: dict[str, tuple[float, float]] = {}
    tall = max(len(v) for v in by_tactic.values())
    pitch1 = (top - bot) / max(tall - 1, 1)
    for t, tids in by_tactic.items():
        n = len(tids)
        y_start = (top + bot) / 2 + (n - 1) * pitch1 / 2
        for k, tid in enumerate(tids):
            pos[tid] = (col[t], y_start - k * pitch1)
    max_obs = max(e["observation_count"] for e in gap["edges"])
    for e in sorted(gap["edges"], key=lambda e: e["observation_count"]):
        s, d = e["source_id"], e["target_id"]
        if s not in pos or d not in pos:
            continue
        f = e["observation_count"] / max_obs
        w(r"\draw[black!%d,line width=%.2fpt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (10 + int(round(46 * f ** 0.45)), 0.10 + 0.55 * f ** 0.6,
             pos[s][0], pos[s][1], pos[d][0], pos[d][1]))
    for tid, (px, py) in pos.items():
        w(r"\fill[black!62] (%.3f,%.3f) circle (0.5pt);" % (px, py))
    facts["techniques"], facts["edges"] = len(pos), len(gap["edges"])
    gutter(w, (top + bot) / 2, r"\textbf{L1} \enspace Attack graph",
           r"%d techniques, %d transitions" % (len(pos), len(gap["edges"])))
    y -= H_L1

    down_arrow(w, (AX0 + AX1) / 2, y - 0.06, y - H_ARROW + 0.06, "condition on objective")
    y -= H_ARROW

    # ---- L2: the four attack profiles ------------------------------------
    gutter_done = False
    prof_row_y: dict[str, float] = {}
    facts["profiles"] = {}
    for pi, prof in enumerate(PROFILE_ORDER):
        ry = y - 0.06 - H_L2_ROW * (pi + 0.5)
        prof_row_y[prof] = ry
        doc = nets[prof]
        n_flows = doc["provenance"]["gasp_source_flow_count"]
        facts["profiles"][PROFILE_LABEL[prof]] = (n_flows, len(doc["transitions"]))
        places = set(doc["places"])
        obj = OBJECTIVE_TACTICS[prof]
        w(r"\draw[black!12,line width=0.2pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (AX0 - 0.10, ry, AX1 + 0.10, ry))
        for tr in doc["transitions"]:
            a, b = tr["src_tactic"], tr["dst_tactic"]
            if a not in col or b not in col:
                continue
            delta = idx[b] - idx[a]
            h = min(0.23, 0.055 + 0.026 * abs(delta)) * (1 if delta >= 0 else -1)
            bez(w, col[a], ry, col[b], ry, h, "black!26,line width=0.16pt")
        for t in order:
            if t not in places:
                continue
            if t in obj:
                w(r"\fill[%s] (%.3f,%.3f) circle (1.05pt);" % (ACCENT, col[t], ry))
            else:
                w(r"\fill[black!48] (%.3f,%.3f) circle (0.62pt);" % (col[t], ry))
        w(r"\node[anchor=east,font=\scriptsize] at (%.3f,%.3f) "
          r"{%s\enspace{\color{black!58}%d}};"
          % (GUT_R, ry, esc(PROFILE_LABEL[prof]), n_flows))
        gutter_done = True
    assert gutter_done
    w(r"\node[anchor=east,font=\scriptsize] at (%.3f,%.3f) {\textbf{L2} \enspace Attack profiles};"
      % (GUT_R, y - 0.06 + 0.20))
    y -= H_L2_ROW * len(PROFILE_ORDER) + 0.12

    # ---- arrow: one profile is made executable ---------------------------
    down_arrow(w, (AX0 + AX1) / 2, y - 0.06, y - H_ARROW + 0.06,
               "give executable semantics")
    y -= H_ARROW

    # ---- L3: the generalised stochastic Petri net -------------------------
    doc = nets[profile]
    places = [t for t in order if t in set(doc["places"])]
    ry = y - H_L3 * 0.46
    for tr in doc["transitions"]:
        a, b = tr["src_tactic"], tr["dst_tactic"]
        if a not in col or b not in col:
            continue
        delta = idx[b] - idx[a]
        h = min(0.30, 0.06 + 0.030 * abs(delta)) * (1 if delta >= 0 else -1)
        bez(w, col[a], ry, col[b], ry, h, "black!22,line width=0.16pt")
    # the declared pre-intrusion overlay, drawn in
    for a, b, dirn in overlay_edges:
        if a not in col or b not in col:
            continue
        delta = idx[b] - idx[a]
        h = (0.34 if delta >= 0 else -0.40)
        bez(w, col[a], ry, col[b], ry, h,
            f"{ACCENT}!70,line width=0.55pt,dashed,dash pattern=on 1.3pt off 1.3pt")
    # transitions as bars on the adjacent-tactic moves the net actually holds
    have = {(t["src_tactic"], t["dst_tactic"]) for t in doc["transitions"]}
    have |= {(a, b) for a, b, _ in overlay_edges}
    for i in range(len(order) - 1):
        a, b = order[i], order[i + 1]
        if (a, b) not in have:
            continue
        mx = (col[a] + col[b]) / 2
        w(r"\fill[black!72] (%.3f,%.3f) rectangle (%.3f,%.3f);"
          % (mx - 0.022, ry - 0.105, mx + 0.022, ry + 0.105))
    for t in places:
        w(r"\draw[black!62,fill=white,line width=0.45pt] (%.3f,%.3f) circle (0.105);"
          % (col[t], ry))
    entry = order[0] if order[0] in places else places[0]
    w(r"\fill[%s] (%.3f,%.3f) circle (0.052);" % (ACCENT, col[entry], ry))
    facts["net"] = (profile, len(places), len(doc["transitions"]), len(overlay_edges))
    gutter(w, ry, r"\textbf{L3} \enspace Petri net",
           r"%d places, %d transitions\\one token, one profile shown"
           % (len(places), len(doc["transitions"])))
    y -= H_L3

    y -= PAD
    band(w, mv_top, y, "accent!45")
    rot_label(w, mv_top, y, "Movement layer", "accent")
    mv_bot = y

    # ================================================== the two-way joins ==
    x_a, x_b = BAND_L + 2.35, BAND_R - 2.35
    y_ctrl_top = mv_bot - H_JOIN
    w(r"\draw[->,accent!70,line width=0.7pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (x_a, mv_bot - 0.08, x_a, y_ctrl_top + 0.08))
    w(r"\node[anchor=east,font=\scriptsize,text=accent] at (%.3f,%.3f) {tactic};"
      % (x_a - 0.10, (mv_bot + y_ctrl_top) / 2))
    w(r"\draw[->,accent!70,line width=0.7pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (x_b, y_ctrl_top + 0.08, x_b, mv_bot - 0.08))
    w(r"\node[anchor=west,font=\scriptsize,text=accent] at (%.3f,%.3f) {re-weighting};"
      % (x_b + 0.10, (mv_bot + y_ctrl_top) / 2))

    # ============================================== the controller layer ==
    y = y_ctrl_top
    ctrl_top = y
    cell_w = (BAND_R - BAND_L - 0.9) / 3
    cx = [BAND_L + 0.45 + cell_w * (i + 0.5) for i in range(3)]
    head_y = y - 0.30
    body_top = y - 0.62
    body_bot = ctrl_top - H_CTRL + 0.46
    foot_y = ctrl_top - H_CTRL + 0.24

    for i in (1, 2):
        sx = BAND_L + 0.45 + cell_w * i
        w(r"\draw[black!22,line width=0.35pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (sx, ctrl_top - 0.18, sx, ctrl_top - H_CTRL + 0.16))

    # (i) dwell times + the exponential draw
    w(r"\node[font=\scriptsize] at (%.3f,%.3f) {Dwell times};" % (cx[0], head_y))
    bar_x0 = cx[0] - cell_w / 2 + 0.30
    bar_max = 1.35
    dmax = max(durations.values())
    bpitch = (body_top - body_bot) / (len(order) - 1)
    for i, t in enumerate(order):
        by = body_top - i * bpitch
        ln = bar_max * durations[t] / dmax
        w(r"\draw[black!45,line width=0.2pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (bar_x0, by, bar_x0 + bar_max, by))
        if ln > 0:
            w(r"\draw[black!68,line width=1.05pt] (%.3f,%.3f) -- (%.3f,%.3f);"
              % (bar_x0, by, bar_x0 + ln, by))
    ex_x0 = bar_x0 + bar_max + 0.42
    ex_w, ex_h = 0.95, (body_top - body_bot)
    ey0 = body_bot
    w(r"\draw[black!30,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);"
      % (ex_x0, ey0 + ex_h, ex_x0, ey0, ex_x0 + ex_w, ey0))
    pts = []
    for k in range(31):
        u = k / 30
        pts.append("(%.3f,%.3f)" % (ex_x0 + u * ex_w, ey0 + ex_h * math.exp(-3.1 * u)))
    w(r"\draw[black!70,line width=0.6pt] " + " -- ".join(pts) + ";")
    w(r"\draw[->,black!45,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (bar_x0 + bar_max + 0.10, (body_top + body_bot) / 2,
         ex_x0 - 0.10, (body_top + body_bot) / 2))
    foot(w, cx[0], foot_y, cell_w, r"%d declared means" % len(durations))

    # (ii) the tactic-to-verb mapping
    w(r"\node[font=\scriptsize] at (%.3f,%.3f) {Tactic-to-verb mapping};" % (cx[1], head_y))
    lx, rx = cx[1] - 0.95, cx[1] + 0.95
    tp = (body_top - body_bot) / (len(order) - 1)
    ty = {t: body_top - i * tp for i, t in enumerate(order)}
    vp = (body_top - body_bot) / max(len(verbs) - 1, 1)
    vy = {v: body_top - i * vp for i, v in enumerate(verbs)}
    for t in order:
        v = mapping.get(t)
        if v:
            w(r"\draw[black!45,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);"
              % (lx, ty[t], rx, vy[v]))
    for t in order:
        if mapping.get(t):
            w(r"\fill[black!68] (%.3f,%.3f) circle (0.9pt);" % (lx, ty[t]))
        else:
            w(r"\draw[black!42,line width=0.35pt] (%.3f,%.3f) circle (0.9pt);" % (lx, ty[t]))
    for v in verbs:
        w(r"\fill[black!68] (%.3f,%.3f) circle (1.1pt);" % (rx, vy[v]))
    w(r"\node[anchor=east,font=\scriptsize,text=black!58] at (%.3f,%.3f) {tactics};"
      % (lx - 0.14, (body_top + body_bot) / 2))
    w(r"\node[anchor=west,font=\scriptsize,text=black!58] at (%.3f,%.3f) {verbs};"
      % (rx + 0.14, (body_top + body_bot) / 2))
    n_mapped = sum(1 for t in order if mapping.get(t))
    n_dwell = len(order) - n_mapped
    facts["mapping"] = (mapping_version, n_mapped, n_dwell, len(verbs))
    foot(w, cx[1], foot_y, cell_w, r"%d mapped, %d dwell-only" % (n_mapped, n_dwell))

    # (iii) the failure matrix
    w(r"\node[font=\scriptsize] at (%.3f,%.3f) {Failure matrix};" % (cx[2], head_y))
    side = min(1.30, body_top - body_bot)
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
    w(r"\draw[black!35,line width=0.3pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"
      % (mx0, my0 - side, mx0 + side, my0))
    facts["failure"] = (overlay_version, len(order), len(order) - 1, n_rules)
    foot(w, cx[2], foot_y, cell_w,
         r"%d $\times$ %d tactic pairs" % (len(order), len(order) - 1))

    y = ctrl_top - H_CTRL
    band(w, ctrl_top, y, "accent!45")
    rot_label(w, ctrl_top, y, "Controller layer", "accent")
    ctrl_bot = y

    # ================================================== join to the action ==
    y_act_top = ctrl_bot - H_JOIN
    w(r"\draw[->,black!55,line width=0.7pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (x_a, ctrl_bot - 0.08, x_a, y_act_top + 0.08))
    w(r"\node[anchor=east,font=\scriptsize,text=black!58] at (%.3f,%.3f) {verb};"
      % (x_a - 0.10, (ctrl_bot + y_act_top) / 2))
    w(r"\draw[->,black!55,line width=0.7pt] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (x_b, y_act_top + 0.08, x_b, ctrl_bot - 0.08))
    w(r"\node[anchor=west,font=\scriptsize,text=black!58] at (%.3f,%.3f) {verdict};"
      % (x_b + 0.10, (ctrl_bot + y_act_top) / 2))

    # ===================================================== the action layer ==
    act_top = y_act_top
    band(w, act_top, act_top - H_ACT, "black!22", "black!4")
    rot_label(w, act_top, act_top - H_ACT, "Action layer", "black!55")
    boxes = [("Attacker", r"%s inherited verbs" % WORD.get(len(verbs), len(verbs))),
             ("Network", r"hosts, services\\and vulnerabilities"),
             ("Defender", r"moving target\\defence")]
    bw = 2.70
    bxs = [BAND_L + 0.55 + bw / 2, (BAND_L + BAND_R) / 2, BAND_R - 0.55 - bw / 2]
    by_c = act_top - H_ACT / 2
    for (title, sub), bx in zip(boxes, bxs):
        w(r"\draw[black!38,fill=white,line width=0.4pt,rounded corners=1.4pt] "
          r"(%.3f,%.3f) rectangle (%.3f,%.3f);" % (bx - bw / 2, by_c - 0.58, bx + bw / 2, by_c + 0.58))
        w(r"\node[font=\scriptsize,align=center,text width=%.2fcm] at (%.3f,%.3f) "
          r"{%s\\[1.5pt]\color{black!58}%s};" % (bw - 0.16, bx, by_c, title, sub))
    for i in (0, 2):
        x1 = bxs[i] + (bw / 2 if i == 0 else -bw / 2)
        x2 = bxs[1] + (-bw / 2 if i == 0 else bw / 2)
        w(r"\draw[<->,black!45,line width=0.5pt] (%.3f,%.3f) -- (%.3f,%.3f);"
          % (x1 + 0.06, by_c, x2 - 0.06 if i == 0 else x2 + 0.06, by_c))
    w(r"\node[anchor=north,font=\scriptsize,text=black!50] at (%.3f,%.3f) {inherited from MTDSim};"
      % ((BAND_L + BAND_R) / 2, act_top - 0.06))
    act_bot = act_top - H_ACT

    # ---- the L4 bracket: the join is the traversal ------------------------
    w(r"\draw[black!45,line width=0.4pt,decorate,"
      r"decoration={brace,amplitude=3pt,mirror}] (%.3f,%.3f) -- (%.3f,%.3f);"
      % (GUT_R + 0.02, ctrl_top, GUT_R + 0.02, act_bot))
    w(r"\node[anchor=east,align=right,font=\scriptsize] at (%.3f,%.3f) "
      r"{\textbf{L4} \enspace Attacker-agent\\traversal in MTDSim};"
      % (GUT_R - 0.14, (ctrl_top + act_bot) / 2))

    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    facts["height_cm"] = abs(act_bot) + 2 * PAD
    facts["width_cm"] = BAND_R - ROT_X
    return "\n".join(L) + "\n", facts


# ------------------------------------------------------------------- main --
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", default="objective_exfiltration", choices=PROFILE_ORDER,
                    help="the profile drawn at L3 (default: the largest class)")
    ap.add_argument("--mapping", default="v2_partial", help="controller mapping version")
    ap.add_argument("--overlay-version", default="v4_failure_only",
                    help="outcome-overlay version the failure matrix is compiled from")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    gap, order = load_gap()
    nets = load_nets()
    overlay_edges = load_overlay_edges()
    durations = load_durations()
    mapping, verbs = load_mapping(args.mapping)
    fmatrix, n_rules = failure_cells(order, args.overlay_version)

    missing = [t for t in order if t not in durations or t not in mapping]
    if missing:
        raise SystemExit(f"tactics absent from the dwell catalogue or the mapping: {missing}")

    tex, facts = emit(gap, order, nets, overlay_edges, durations, mapping, verbs,
                      fmatrix, n_rules, args.profile, args.mapping, args.overlay_version)
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

    # --- the fact sheet a caption may quote ---------------------------------
    print("--- facts (all read from tracked artefacts) ---")
    print(f"L0  attack flows                 : {facts['flows']}")
    print(f"L1  techniques / transitions     : {facts['techniques']} / {facts['edges']}")
    print("L2  profiles (flows, transitions):")
    for name, (nf, nt) in facts["profiles"].items():
        print(f"      {name:<24} {nf:>3} flows, {nt:>4} transitions")
    p, np_, nt, no = facts["net"]
    print(f"L3  net drawn                    : {p} -- {np_} places, {nt} transitions, "
          f"+{no} declared pre-intrusion edges")
    print(f"    dwell catalogue              : {len(durations)} tactics, "
          f"{sum(1 for v in durations.values() if v == 0)} at zero, max {max(durations.values())} s")
    mv, nm, nd, nv = facts["mapping"]
    print(f"    mapping ({mv:<12})       : {nm} mapped, {nd} dwell-only, {nv} verbs")
    ov, nr, nc, nrule = facts["failure"]
    print(f"    failure matrix ({ov})  : {nr} x {nc} ordered pairs, {nrule} rules (A-{chr(ord('A') + nrule - 1)})")
    print(f"drawn size                       : {facts['width_cm']:.2f} x {facts['height_cm']:.2f} cm")


if __name__ == "__main__":
    main()
