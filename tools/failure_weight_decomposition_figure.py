#!/usr/bin/env python3
"""Dissertation figures + appendix tables for the outcome-overlay weight sets:
the committed failure matrix (ch4), its decomposition (ch5 sensitivity), the
declared kernel point inside its sweep bands (ch5 sensitivity), and the
appendix tables (the rule ledgers, the kernel parameters, the full sets).

The failure weight set is not authored cell by cell. Every one of its 210
values (15 x 14, no self-loops) is the product of two declared kernels, each
small enough to print on one line:

  (a) the failure kernel    — the value of the first-matching failure rule
                              (nine declared semantics rules: the two
                              foothold gates, the two dampers, the
                              backward / lateral / forward ladder), read from
                              data/ogasp/controller/outcome_rules.json;
  (b) the distance kernel   — d(a,b) over the four-stage APT-lifecycle
                              consensus (gamma, delta, floor z), read from
                              data/ogasp/controller/lifecycle_consensus.json;
  (c) the failure weight set — (a) x (b), which is exactly what the registry
                              version's failure.json holds.

Three figures, each with a home (Marc's split, 2026-08-19):

  --layout matrix         docs/thesis/figures/<verdict>_weight_matrix
      ch4 §4.2.4.2: panel (c) alone — the committed set, every cell printed
      with its value AND the letter of the rule that produced it, so the
      matrix reads as rule-generated on the page; the key is in-figure, the
      rules' rationale/tier live in the appendix ledger table.
  --layout decomposition  docs/thesis/figures/<verdict>_weight_decomposition
      ch5 sensitivity study: (a), (b), (c) as three aligned 15 x 14 matrices
      on one shared stage-grouped axis and ONE uniform 0–1 grey scale — what
      the sweep's parameters touch (b) and what they hold fixed (a).
  --layout bands          docs/thesis/figures/distance_kernel_bands
      ch5 sensitivity study: the declared kernel point inside its declared
      sweep bands — d(Delta) at the declared parameters and at the band
      edges, the floor, the 210-pair count per Delta, and the base-edge
      census per Delta over the five current routing nets (which Delta
      classes the corpus actually exercises).

Everything is computed through the tracked compiler
(mtdsim.l3_simulation.controller.rules) and the tracked net loader
(mtdsim.l3_simulation.movement.net) from the committed artefacts — no value is
typed here, and the numbers a caption may quote are printed to stdout for
cross-checking. Diagnostic register: no arrows, no highlights, no circles; the
one accent marks the declared point in the bands figure.

Usage:
  PYTHONPATH=src python tools/failure_weight_decomposition_figure.py
      [--layout all|matrix|decomposition|bands] [--version v3_persistent_backward]
      [--verdict failure|success] [--walk a->b ...] [--no-compile] [--no-tables]
      [--dry-run-adjacent]

Writes the figures above (+ .pdf via pdflatex) and
  docs/thesis/tables/outcome_overlay_weights.tex  (the appendix wiring: the
      rule ledgers, the kernel parameters, and the full success + failure
      weight sets for the version — unless --no-tables)

Style: TikZ at the document's 12 pt base so \\scriptsize / \\tiny land at
8 pt / 6 pt in the thesis; greys carry the value on one sequential ramp; no
colour carries a category; text in the document font. Same conventions as
tools/l1_attack_graph_figure.py so the figures read as one system.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from dataclasses import replace
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from mtdsim.l3_simulation.controller.outcome import load_overlay_registry  # noqa: E402
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net  # noqa: E402
from mtdsim.l3_simulation.controller.rules import (  # noqa: E402
    DistanceKernel,
    RuleSet,
    RuleSpec,
    compile_pair,
    load_rule_set,
    spec_from_registry_entry,
)

FIG_DIR = REPO / "docs" / "thesis" / "figures"
TAB_DIR = REPO / "docs" / "thesis" / "tables"
TABLES_STEM = "outcome_overlay_weights"

# ATT&CK v19.1 display names (the same map fig:l1-graph uses). "Defense
# impairment" keeps ATT&CK's own spelling as the tactic's name.
TACTIC_LABEL = {
    "reconnaissance": "Reconnaissance",
    "resource-development": "Resource development",
    "initial-access": "Initial access",
    "execution": "Execution",
    "persistence": "Persistence",
    "privilege-escalation": "Privilege escalation",
    "stealth": "Stealth",
    "defense-impairment": "Defense impairment",
    "credential-access": "Credential access",
    "discovery": "Discovery",
    "lateral-movement": "Lateral movement",
    "collection": "Collection",
    "command-and-control": "Command and control",
    "exfiltration": "Exfiltration",
    "impact": "Impact",
}
# Short forms for the rotated column headers (rows carry the full name).
TACTIC_SHORT = {
    "reconnaissance": "Recon.",
    "resource-development": "Res. dev.",
    "initial-access": "Init. access",
    "execution": "Execution",
    "persistence": "Persistence",
    "privilege-escalation": "Priv. esc.",
    "stealth": "Stealth",
    "defense-impairment": "Def. imp.",
    "credential-access": "Cred. access",
    "discovery": "Discovery",
    "lateral-movement": "Lat. move.",
    "collection": "Collection",
    "command-and-control": "C2",
    "exfiltration": "Exfiltration",
    "impact": "Impact",
}
STAGE_SHORT = {0: "preparation", 1: "intrusion", 2: "post-intrusion", 3: "objective"}

# --- geometry (cm) ---------------------------------------------------------
CELL_W = 0.78          # column pitch
CELL_H = 0.27          # row pitch
LABEL_X = 4.20         # right edge of the row labels (figure x origin at 0)
STAGE_X = 1.40         # right edge of the row-stage labels; bracket just right of it
COL_LABEL_H = 1.00     # height reserved above each panel for rotated headers
PANEL_GAP = 0.75       # vertical gap between panels (holds the two-line panel header)
HEADER_W = 15.4        # text width of a panel header (== the figure width)
GRID = "black!18"
STAGE_RULE = "black!55"
ACCENT_RGB = "31,84,140"   # the one accent (shared with fig:l1-graph): the declared point


def _esc(s: str) -> str:
    return (s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
             .replace("_", r"\_"))


def _fmt(v: float) -> str:
    """A value as printed in a cell: exact decimals, no trailing zeros."""
    if v == 0:
        return "0"
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s


def _value_letter(v: float, letter: str) -> str:
    """A cell's 'value + rule letter' label. Long values (four decimals) are
    set a touch smaller so the pair stays inside a 0.78 cm cell."""
    txt = _fmt(v)
    if len(txt) >= 6:
        txt = r"\scalebox{0.85}{%s}" % txt
    return "%s\\hspace{0.5pt}{\\color{black!%s}\\scalebox{0.8}{%s}}" % (txt, "70" if v <= 0.5 else "30", letter)


def stage_grouped_order(rs: RuleSet) -> list[str]:
    """Rows/columns: consensus stage, then the ATT&CK reading order within a
    stage (the order fig:l1-graph uses), so the four stage blocks are visible
    and within-block order asserts nothing — the consensus declares the
    post-intrusion middle unordered."""
    attack_order = list(TACTIC_LABEL)
    return sorted(rs.tactics, key=lambda t: (rs.stage_of[t], attack_order.index(t)))


def rule_keys(rs: RuleSet, verdict: str) -> dict[str, str]:
    """Rule id -> one-letter key, in the rules file's match order (A, B, ...)."""
    return {rid: chr(ord("A") + i) for i, rid in enumerate(rs.order[verdict])}


def decompose(rs: RuleSet, spec: RuleSpec, verdict: str) -> dict[tuple[str, str], dict]:
    """Every pair's (rule, rule value, d, delta, product) through the tracked
    compiler — the decomposition is read off the compiler's own cell, not
    re-derived here."""
    out = {}
    for a in rs.tactics:
        for b in rs.tactics:
            if a == b:
                continue
            c = compile_pair(rs, verdict, a, b, spec)
            out[(a, b)] = {
                "rule": c["rule"],
                "kernel": rs.values[verdict].get(c["rule"], 1.0),
                "d": c.get("d", 1.0),
                "delta": c.get("delta", rs.stage_of[b] - rs.stage_of[a]),
                "v": c["v"],
            }
    return out


def cell_style(v: float) -> tuple[str, str]:
    """(fill, text colour) on ONE uniform 0–1 ramp shared by all panels."""
    if v <= 0:
        return "white", "black!45"
    level = int(round(8 + 72 * min(max(v, 0.0), 1.0)))
    return f"black!{level}", ("white" if v > 0.5 else "black")


def emit_panel(w, y_top: float, order: list[str], rs: RuleSet,
               values: dict[tuple[str, str], float], labels: dict[tuple[str, str], str],
               header: str, show_col_labels: bool) -> float:
    """Draw one 15 x 14 matrix with its top-left at (LABEL_X, y_top) after the
    column-label band. Returns the y of its bottom edge."""
    n = len(order)
    x0 = LABEL_X + 0.12
    y0 = y_top - (COL_LABEL_H if show_col_labels else 0.0)
    # panel header (left-aligned above the column-label band)
    w(r"\node[anchor=south west,font=\scriptsize,align=left,text width=%.1fcm] at (%.2f,%.2f) {%s};"
      % (HEADER_W, 0.0, y_top + 0.06, header))
    # column headers
    if show_col_labels:
        for j, b in enumerate(order):
            xc = x0 + (j + 0.5) * CELL_W
            w(r"\node[anchor=west,rotate=55,font=\tiny] at (%.3f,%.3f) {%s};"
              % (xc - 0.06, y0 + 0.08, _esc(TACTIC_SHORT[b])))
    # cells
    for i, a in enumerate(order):
        yc = y0 - (i + 0.5) * CELL_H
        for j, b in enumerate(order):
            xc = x0 + (j + 0.5) * CELL_W
            if a == b:
                w(r"\draw[%s,line width=0.2pt] (%.3f,%.3f) -- (%.3f,%.3f);"
                  % (GRID, xc - CELL_W / 2, yc - CELL_H / 2, xc + CELL_W / 2, yc + CELL_H / 2))
                continue
            v = values[(a, b)]
            fill, tc = cell_style(v)
            w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
              % (fill, xc - CELL_W / 2, yc - CELL_H / 2, xc + CELL_W / 2, yc + CELL_H / 2))
            w(r"\node[font=\tiny,text=%s] at (%.3f,%.3f) {%s};" % (tc, xc, yc, labels[(a, b)]))
    # grid + stage rules
    for i in range(n + 1):
        y = y0 - i * CELL_H
        col = STAGE_RULE if (0 < i < n and rs.stage_of[order[i]] != rs.stage_of[order[i - 1]]) else GRID
        lw = 0.5 if col == STAGE_RULE else 0.2
        w(r"\draw[%s,line width=%.1fpt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, lw, x0, y, x0 + n * CELL_W, y))
    for j in range(n + 1):
        x = x0 + j * CELL_W
        col = STAGE_RULE if (0 < j < n and rs.stage_of[order[j]] != rs.stage_of[order[j - 1]]) else GRID
        lw = 0.5 if col == STAGE_RULE else 0.2
        w(r"\draw[%s,line width=%.1fpt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, lw, x, y0, x, y0 - n * CELL_H))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);"
      % (x0, y0, x0 + n * CELL_W, y0 - n * CELL_H))
    # row labels + row-stage labels
    for i, a in enumerate(order):
        yc = y0 - (i + 0.5) * CELL_H
        w(r"\node[anchor=east,font=\tiny] at (%.2f,%.3f) {%s};" % (LABEL_X, yc, _esc(TACTIC_LABEL[a])))
    stages = sorted({rs.stage_of[t] for t in order})
    for s in stages:
        rows = [i for i, t in enumerate(order) if rs.stage_of[t] == s]
        yc = y0 - (rows[0] + rows[-1] + 1) / 2 * CELL_H
        y_a, y_b = y0 - rows[0] * CELL_H, y0 - (rows[-1] + 1) * CELL_H
        w(r"\draw[%s,line width=0.4pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (STAGE_RULE, STAGE_X + 0.08, y_a - 0.02, STAGE_X + 0.08, y_b + 0.02))
        w(r"\node[font=\tiny,text=black!60,anchor=east] at (%.2f,%.3f) {%s};"
          % (STAGE_X, yc, _esc(STAGE_SHORT[s])))
    return y0 - n * CELL_H


def emit_figure(rs: RuleSet, spec: RuleSpec, verdict: str, dec: dict, version: str) -> str:
    order = stage_grouped_order(rs)
    keys = rule_keys(rs, verdict)
    k = spec.kernel
    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usetikzlibrary{calc}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt}]")

    y = 0.0
    # (a) the verdict kernel — rule value, keyed by rule letter
    vals_a = {p: c["kernel"] for p, c in dec.items()}
    lab_a = {p: _value_letter(c["kernel"], keys[c["rule"]]) for p, c in dec.items()}
    hdr_a = (r"(a)\; %s kernel: the value of the first-matching declared rule "
             r"(rule key A--%s, below)" % (verdict, keys[rs.order[verdict][-1]]))
    y = emit_panel(w, y, order, rs, vals_a, lab_a, hdr_a, show_col_labels=True) - PANEL_GAP

    # (b) the distance kernel
    vals_b = {p: c["d"] for p, c in dec.items()}
    lab_b = {}
    for p, c in dec.items():
        dl = c["delta"]
        sign = "+" if dl > 0 else ("" if dl == 0 else "-")
        lab_b[p] = "%s$_{%s%d}$" % (_fmt(c["d"]), sign, abs(dl))
    hdr_b = (r"(b)\; lifecycle-distance kernel $d(a,b)$ over the four consensus stages, the signed stage "
             r"offset $\Delta=s(b)-s(a)$ as subscript: "
             r"$d=1$ for $|\Delta|\le 1$, $\gamma^{\Delta-1}$ forward, $\delta^{|\Delta|-1}$ backward, "
             r"$d<z$ reads as 0 ($\gamma=%s$, $\delta=%s$, $z=%s$)" % (_fmt(k.gamma), _fmt(k.delta_ratio), _fmt(k.z)))
    y = emit_panel(w, y, order, rs, vals_b, lab_b, hdr_b, show_col_labels=True) - PANEL_GAP

    # (c) the product — the committed weight set
    vals_c = {p: c["v"] for p, c in dec.items()}
    lab_c = {p: _fmt(c["v"]) for p, c in dec.items()}
    hdr_c = (r"(c)\; the %s weight set $=$ (a)\,$\times$\,(b), as committed "
             r"(\texttt{%s})" % (verdict, _esc(version)))
    y = emit_panel(w, y, order, rs, vals_c, lab_c, hdr_c, show_col_labels=True)

    emit_key(w, rs, verdict, keys, y, "rule key (match order; value $\\times$ $d$ gives the cell in (c)):")
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


def emit_key(w, rs: RuleSet, verdict: str, keys: dict[str, str], y: float, lead: str) -> None:
    """The rule key under a matrix: letter, rule id, declared value — two
    columns, read from the rules file. Rationale and tier are NOT here; they
    live in the appendix ledger table the caption points at."""
    rules = {r["id"]: r for r in rs.doc[f"{verdict}_rules"]}
    ids = list(rs.order[verdict])
    half = (len(ids) + 1) // 2
    y_key = y - 0.32
    x_cols = (0.0, 8.2)
    w(r"\node[anchor=north west,font=\tiny,text=black!60] at (%.2f,%.2f) {%s};" % (x_cols[0], y_key + 0.26, lead))
    for col, chunk in enumerate((ids[:half], ids[half:])):
        for r_i, rid in enumerate(chunk):
            r = rules[rid]
            w(r"\node[anchor=north west,font=\tiny] at (%.2f,%.2f) {\textbf{%s}\; \texttt{%s} $=$ %s};"
              % (x_cols[col], y_key - r_i * 0.27, keys[rid], _esc(rid), _fmt(float(r["value"]))))


def emit_matrix_figure(rs: RuleSet, spec: RuleSpec, verdict: str, dec: dict, version: str) -> str:
    """ch4: the committed set alone — panel (c) with the producing rule's
    letter in each cell, so the matrix reads as generated, not typed."""
    order = stage_grouped_order(rs)
    keys = rule_keys(rs, verdict)
    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usetikzlibrary{calc}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt}]")
    vals = {p: c["v"] for p, c in dec.items()}
    lab = {p: _value_letter(c["v"], keys[c["rule"]]) for p, c in dec.items()}
    hdr = (r"the %s weight set (\texttt{%s}): each cell is the value the token's out-transition "
           r"is multiplied by on a %s verdict, with the letter of the declared rule that produced it"
           % (verdict, _esc(version), verdict))
    y = emit_panel(w, 0.0, order, rs, vals, lab, hdr, show_col_labels=True)
    emit_key(w, rs, verdict, keys, y, "rule key (match order; each value is then multiplied by the lifecycle-distance factor):")
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


def edge_census(rs: RuleSet) -> tuple[Counter, dict[str, Counter]]:
    """Base edges with mass on the five current routing nets (synthetic overlay
    on, the reported arm), counted by signed consensus-stage offset — which
    Delta classes the corpus actually exercises. Self-loops are not pairs."""
    total: Counter = Counter()
    per: dict[str, Counter] = {}
    for profile in PROFILES:
        net = load_routing_net(profile, with_synthetic_overlay=True)
        c: Counter = Counter()
        for a in net.places:
            for b, wgt in net.base_out_weights(a).items():
                if wgt > 0 and a != b:
                    c[rs.stage_of[b] - rs.stage_of[a]] += 1
        per[profile] = c
        total.update(c)
    return total, per


def emit_bands_figure(rs: RuleSet, spec: RuleSpec, dec: dict, census: Counter, version: str) -> str:
    """ch5: the declared kernel point inside its declared sweep bands."""
    declared = rs.consensus["declared_parameters"]
    k = spec.kernel
    g_band = [float(x) for x in declared["gamma"]["sweep"]]
    d_band = [float(x) for x in declared["delta_ratio"]["sweep"]]
    z_band = [float(x) for x in declared["z"]["sweep"]]
    deltas = list(range(-3, 4))
    pairs_per = Counter(c["delta"] for c in dec.values())

    def kern(delta: int, gamma: float, dr: float) -> float:
        if delta == 0:
            return 1.0
        return gamma ** (delta - 1) if delta > 0 else dr ** (-delta - 1)

    # geometry
    X0, X1 = 2.6, 11.2          # plot x-range (cm)
    Y0, Y1 = 0.0, 3.6           # plot y-range (cm) for d in [0, 1]
    xs = {d: X0 + (d + 3) * (X1 - X0) / 6 for d in deltas}
    ys = lambda v: Y0 + v * (Y1 - Y0)  # noqa: E731

    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usetikzlibrary{calc}")
    w(r"\definecolor{accent}{RGB}{%s}" % ACCENT_RGB)
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=\tiny}]")
    # floor band (the z sweep set) and the declared floor
    zmax = max(z_band)
    w(r"\fill[black!6] (%.2f,%.3f) rectangle (%.2f,%.3f);" % (X0, ys(0), X1, ys(zmax)))
    w(r"\draw[black!45,line width=0.3pt,dash pattern=on 1pt off 1pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (X0, ys(k.z), X1, ys(k.z)))
    w(r"\node[anchor=south,text=black!55] at (%.2f,%.3f) {floor $z=%s$ (swept \{%s\}); $d<z$ reads as 0};"
      % ((X0 + X1) / 2, ys(zmax) + 0.04, _fmt(k.z), ", ".join(_fmt(v) for v in z_band)))
    # axes
    w(r"\draw[black!60,line width=0.4pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (X0, Y0, X1, Y0))
    w(r"\draw[black!60,line width=0.4pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (X0, Y0, X0, Y1))
    for v in (0.0, 0.25, 0.5, 0.75, 1.0):
        w(r"\draw[black!60,line width=0.3pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (X0 - 0.06, ys(v), X0, ys(v)))
        w(r"\node[anchor=east] at (%.2f,%.3f) {%s};" % (X0 - 0.1, ys(v), _fmt(v)))
        if v > 0:
            w(r"\draw[black!10,line width=0.2pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (X0, ys(v), X1, ys(v)))
    w(r"\node[rotate=90,anchor=south] at (%.2f,%.3f) {distance factor $d$};" % (X0 - 0.75, (Y0 + Y1) / 2))
    for d in deltas:
        sign = "+" if d > 0 else ("" if d == 0 else "$-$")
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.2f) -- (%.3f,%.2f);" % (xs[d], Y0, xs[d], Y0 - 0.06))
        w(r"\node[anchor=north] at (%.3f,%.2f) {%s%d};" % (xs[d], Y0 - 0.1, sign, abs(d)))
    w(r"\node[anchor=north] at (%.2f,%.2f) {signed stage offset $\Delta = s(b)-s(a)$ \quad (backward $\leftarrow$ \ $\delta$ \ $|$ \ $\gamma$ \ $\rightarrow$ forward)};"
      % ((X0 + X1) / 2, Y0 - 0.38))
    # curves: band edges in greys, declared in the accent; only the pre-floor value
    # is drawn (the floor is the shaded strip), so the reader sees what falls under it
    series = []
    greys = ("black!35", "black!70")   # one ramp: lighter = smaller decay ratio
    for (gb, db), grey in zip(zip(g_band, d_band), greys):
        series.append((gb, db, grey, 0.4, "band edge $\\gamma=\\delta=%s$" % _fmt(gb)))
    series.insert(1, (k.gamma, k.delta_ratio, "accent", 0.8, "declared $\\gamma=%s$, $\\delta=%s$" % (_fmt(k.gamma), _fmt(k.delta_ratio))))
    for gamma, dr, col, lw, _ in series:
        pts = " -- ".join("(%.3f,%.3f)" % (xs[d], ys(kern(d, gamma, dr))) for d in deltas)
        w(r"\draw[%s,line width=%.1fpt] %s;" % (col, lw, pts))
        for d in deltas:
            w(r"\fill[%s] (%.3f,%.3f) circle (0.5mm);" % (col, xs[d], ys(kern(d, gamma, dr))))
    # legend (inside the plot, upper left — the region above the rising edge is empty)
    ly = Y1 - 0.12
    lx = X0 + 0.15
    for gamma, dr, col, lw, lab in series:
        w(r"\draw[%s,line width=%.1fpt] (%.2f,%.3f) -- (%.2f,%.3f);" % (col, lw, lx, ly, lx + 0.4, ly))
        w(r"\fill[%s] (%.2f,%.3f) circle (0.5mm);" % (col, lx + 0.2, ly))
        w(r"\node[anchor=west] at (%.2f,%.3f) {%s};" % (lx + 0.5, ly, lab))
        ly -= 0.28
    # the two census rows under the axis: pairs in the 210-set, and base edges on the nets
    ty = Y0 - 0.9
    w(r"\node[anchor=east,text=black!60] at (%.2f,%.3f) {declared pairs (of 210):};" % (X0 - 0.1, ty))
    w(r"\node[anchor=east,text=black!60] at (%.2f,%.3f) {base edges, five nets (of %d):};" % (X0 - 0.1, ty - 0.3, sum(census.values())))
    w(r"\node[anchor=east,text=black!60] at (%.2f,%.3f) {$d$ at the declared point:};" % (X0 - 0.1, ty - 0.6))
    for d in deltas:
        w(r"\node at (%.3f,%.3f) {%d};" % (xs[d], ty, pairs_per.get(d, 0)))
        n = census.get(d, 0)
        w(r"\node[%s] at (%.3f,%.3f) {%d};" % ("text=black!45" if n == 0 else "", xs[d], ty - 0.3, n))
        w(r"\node at (%.3f,%.3f) {%s};" % (xs[d], ty - 0.6, _fmt(k(d))))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
# appendix tables
# --------------------------------------------------------------------------

def _rules_table(rs: RuleSet, verdict: str, label: str) -> list[str]:
    keys = rule_keys(rs, verdict)
    rules = {r["id"]: r for r in rs.doc[f"{verdict}_rules"]}
    L = []
    L.append(r"\begin{table}[htbp]")
    L.append(r"\centering\scriptsize")
    L.append(r"\caption{The %s rules of the outcome overlay, in match order (first match wins), with the "
             r"value each declares, its provenance tier and its one-sentence rationale, as carried in the "
             r"rule ledger. The key letter is the one the decomposition figure prints in each cell.}" % verdict)
    L.append(r"\label{%s}" % label)
    L.append(r"\begin{tabular}{@{}l l r p{0.17\textwidth} p{0.42\textwidth}@{}}")
    L.append(r"\toprule")
    L.append(r"Key & Rule & Value & Tier & Rationale \\")
    L.append(r"\midrule")
    for rid in rs.order[verdict]:
        r = rules[rid]
        tier = _esc(r["provenance_tier"]).replace("/", r"/\allowbreak ")
        L.append(r"%s & \texttt{%s} & %s & %s & %s \\" % (
            keys[rid], _esc(rid), _fmt(float(r["value"])), tier, _esc(r["rationale"])))
    L.append(r"\bottomrule")
    L.append(r"\end{tabular}")
    L.append(r"\end{table}")
    return L


def _kernel_table(rs: RuleSet, spec: RuleSpec, label: str) -> list[str]:
    declared = rs.consensus["declared_parameters"]
    stages = rs.consensus["stages"]
    L = []
    L.append(r"\begin{table}[htbp]")
    L.append(r"\centering\scriptsize")
    L.append(r"\caption{The lifecycle-distance kernel: the four consensus stages the signed offset "
             r"$\Delta = s(b) - s(a)$ is measured over, and the three declared parameters with their "
             r"provenance tier and the band the sensitivity study sweeps. "
             r"$d(a,b) = 1$ for $\Delta = 0$, $\gamma^{\Delta-1}$ for $\Delta \geq 1$, "
             r"$\delta^{|\Delta|-1}$ for $\Delta \leq -1$; a value below $z$ reads as exactly $0$.}")
    L.append(r"\label{%s}" % label)
    L.append(r"\begin{tabular}{@{}c p{0.36\textwidth} p{0.50\textwidth}@{}}")
    L.append(r"\toprule")
    L.append(r"$s$ & Stage & Tactics \\")
    L.append(r"\midrule")
    order = stage_grouped_order(rs)
    for s in sorted(int(x) for x in stages):
        names = ", ".join(TACTIC_LABEL[t].lower() if t != "command-and-control" else "command and control"
                          for t in order if rs.stage_of[t] == s)
        L.append(r"%d & %s & %s \\" % (s, _esc(str(stages[str(s)])), _esc(names)))
    L.append(r"\bottomrule")
    L.append(r"\end{tabular}")
    L.append(r"\par\vspace{0.6em}")
    L.append(r"\begin{tabular}{@{}l r p{0.30\textwidth} l@{}}")
    L.append(r"\toprule")
    L.append(r"Parameter & Value & Tier & Sweep band \\")
    L.append(r"\midrule")
    sym = {"gamma": r"$\gamma$ (forward decay)", "delta_ratio": r"$\delta$ (backward decay)", "z": r"$z$ (zero floor)"}
    for pname in ("gamma", "delta_ratio", "z"):
        p = declared[pname]
        band = ", ".join(_fmt(float(x)) for x in p["sweep"])
        tier = _esc(p["tier"]).replace("/", r"/\allowbreak ")
        L.append(r"%s & %s & %s & \{%s\} \\" % (sym[pname], _fmt(float(p["value"])), tier, band))
    L.append(r"\bottomrule")
    L.append(r"\end{tabular}")
    L.append(r"\end{table}")
    return L


def _matrix_table(rs: RuleSet, dec: dict, verdict: str, version: str, label: str) -> list[str]:
    order = stage_grouped_order(rs)
    L = []
    L.append(r"\begin{table}[htbp]")
    L.append(r"\centering\tiny")
    L.append(r"\setlength{\tabcolsep}{2.2pt}")
    L.append(r"\caption{The complete %s weight set (\texttt{%s}): rows are the source tactic $a$ whose action "
             r"returned the %s verdict, columns the candidate next tactic $b$; every cell is "
             r"rule value $\times$ $d(a,b)$ (decomposition in Figure~\ref{fig:%s-weight-decomposition} "
             r"for the failure set). Stage-grouped axis; the diagonal is not a pair (self-loops are the "
             r"stepping layer's bounded retry, not an overlay cell).}"
             % (verdict, _esc(version), verdict, "failure"))
    L.append(r"\label{%s}" % label)
    L.append(r"\begin{tabular}{@{}l%s@{}}" % ("r" * len(order)))
    L.append(r"\toprule")
    L.append(r"$a \downarrow\quad b \rightarrow$ & " + " & ".join(
        r"\rotatebox{90}{%s}" % _esc(TACTIC_SHORT[b]) for b in order) + r" \\")
    L.append(r"\midrule")
    prev_stage = None
    for a in order:
        if prev_stage is not None and rs.stage_of[a] != prev_stage:
            L.append(r"\addlinespace[2pt]")
        prev_stage = rs.stage_of[a]
        cells = []
        for b in order:
            cells.append(r"--" if a == b else _fmt(dec[(a, b)]["v"]))
        L.append(r"%s & %s \\" % (_esc(TACTIC_LABEL[a]), " & ".join(cells)))
    L.append(r"\bottomrule")
    L.append(r"\end{tabular}")
    L.append(r"\end{table}")
    return L


def emit_tables(rs: RuleSet, spec: RuleSpec, version: str) -> str:
    L = []
    L.append(r"% GENERATED by tools/failure_weight_decomposition_figure.py from")
    L.append(r"%   data/ogasp/controller/outcome_rules.json + lifecycle_consensus.json")
    L.append(r"%   through mtdsim.l3_simulation.controller.rules (overlay version " + version + ").")
    L.append(r"% Do not hand-edit; regenerate. Requires booktabs + graphicx (both in the preamble).")
    L.append("")
    L += _rules_table(rs, "failure", "tab:overlay-failure-rules")
    L.append("")
    L += _rules_table(rs, "success", "tab:overlay-success-rules")
    L.append("")
    L += _kernel_table(rs, spec, "tab:overlay-distance-kernel")
    L.append("")
    L += _matrix_table(rs, decompose(rs, spec, "failure"), "failure", version, "tab:overlay-failure-set")
    L.append("")
    L += _matrix_table(rs, decompose(rs, spec, "success"), "success", version, "tab:overlay-success-set")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
# the candidate re-declaration dry-run (kernel discrepancy, 2026-08-19)
# --------------------------------------------------------------------------

class AdjacentPenaltyKernel(DistanceKernel):
    """The candidate the dictated narrative implies — ONE stage away already
    penalised: gamma^Delta forward, delta^|Delta| backward (exponent shift).
    Not a registered kernel; exists only so the ruling can be costed."""

    def raw(self, delta: int) -> float:
        if delta == 0:
            return 1.0
        if delta > 0:
            return self.gamma ** delta
        return self.delta_ratio ** (-delta)


def dry_run_adjacent(rs: RuleSet, spec: RuleSpec, verdict: str) -> None:
    k = spec.kernel
    alt = replace(spec, kernel=AdjacentPenaltyKernel(gamma=k.gamma, delta_ratio=k.delta_ratio, z=k.z))
    cur, new = decompose(rs, spec, verdict), decompose(rs, alt, verdict)
    changed = [p for p in cur if cur[p]["v"] != new[p]["v"]]
    newly_zero = [p for p in changed if new[p]["v"] == 0 and cur[p]["v"] != 0]
    by_delta = Counter(new[p]["delta"] for p in changed)
    print(f"[dry-run: penalise one stage away (gamma^|Delta|), {verdict}] "
          f"cells changed={len(changed)}/210  newly zero={len(newly_zero)}  "
          f"changed by Delta={dict(sorted(by_delta.items()))}")
    for a, b in (("initial-access", "reconnaissance"), ("reconnaissance", "initial-access"),
                 ("initial-access", "discovery"), ("exfiltration", "execution")):
        print(f"    {a}->{b}: {cur[(a, b)]['v']} -> {new[(a, b)]['v']}  (d {cur[(a, b)]['d']} -> {new[(a, b)]['d']})")


# --------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--layout", default="all", choices=("all", "matrix", "decomposition", "bands"),
                    help="which figure(s) to write (default: all three)")
    ap.add_argument("--version", default="v3_persistent_backward",
                    help="overlay registry version to decompose (default: the reported one)")
    ap.add_argument("--verdict", default="failure", choices=("failure", "success"))
    ap.add_argument("--walk", action="append", default=[], metavar="A->B",
                    help="print one pair's decomposition (repeatable); defaults to two worked pairs")
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--no-tables", action="store_true")
    ap.add_argument("--dry-run-adjacent", action="store_true",
                    help="cost the candidate re-declaration that penalises one stage away")
    args = ap.parse_args()

    rs = load_rule_set()
    reg = load_overlay_registry()
    try:
        version = next(v for v in reg.versions if v.name == args.version)
    except StopIteration:
        raise SystemExit(f"unknown overlay version {args.version!r}; registered: {[v.name for v in reg.versions]}")
    spec = spec_from_registry_entry(version.spec)
    if not spec.distance:
        raise SystemExit(f"{args.version} compiles without the distance term; nothing to decompose")
    verdict = args.verdict
    dec = decompose(rs, spec, verdict)

    # --- the figures ----------------------------------------------------------
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    census, census_per = edge_census(rs)
    figures: list[tuple[str, str]] = []
    if args.layout in ("all", "matrix"):
        figures.append((f"{verdict}_weight_matrix", emit_matrix_figure(rs, spec, verdict, dec, args.version)))
    if args.layout in ("all", "decomposition"):
        figures.append((f"{verdict}_weight_decomposition", emit_figure(rs, spec, verdict, dec, args.version)))
    if args.layout in ("all", "bands"):
        figures.append(("distance_kernel_bands", emit_bands_figure(rs, spec, dec, census, args.version)))
    for stem, tex in figures:
        tex_path = FIG_DIR / f"{stem}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path.relative_to(REPO)}")

    # --- the appendix tables -------------------------------------------------
    if not args.no_tables:
        TAB_DIR.mkdir(parents=True, exist_ok=True)
        tab_path = TAB_DIR / f"{TABLES_STEM}.tex"
        tab_path.write_text(emit_tables(rs, spec, args.version))
        print(f"wrote {tab_path.relative_to(REPO)}")

    # --- the numbers a caption / record may quote ------------------------------
    keys = rule_keys(rs, verdict)
    k = spec.kernel
    print(f"version={args.version}  verdict={verdict}  kernel gamma={k.gamma} delta={k.delta_ratio} z={k.z}"
          f"  relationship_source={spec.relationship_source}")
    by_rule = Counter(c["rule"] for c in dec.values())
    print("pairs per rule: " + ", ".join(f"{keys[r]} {r}={by_rule[r]}" for r in rs.order[verdict]))
    by_d = Counter((c["delta"], c["d"]) for c in dec.values())
    print("pairs per (Delta, d): " + ", ".join(f"Delta={dl:+d}:d={d}:{n}" for (dl, d), n in sorted(by_d.items())))
    kv = sorted(Counter(c["kernel"] for c in dec.values()).items())
    pv = sorted(Counter(c["v"] for c in dec.values()).items())
    print(f"distinct {verdict}-kernel values={len(kv)}: " + ", ".join(f"{_fmt(v)}x{n}" for v, n in kv))
    print(f"distinct product values={len(pv)}: " + ", ".join(f"{_fmt(v)}x{n}" for v, n in pv))
    print(f"cells exactly 0={sum(1 for c in dec.values() if c['v']==0)}  "
          f"cells touched by distance (d<1)={sum(1 for c in dec.values() if c['d']<1)}")

    print("base edges with mass on the five current nets, by Delta: "
          + ", ".join(f"{d:+d}:{census.get(d, 0)}" for d in range(-3, 4))
          + f"  (total {sum(census.values())}; per profile: "
          + "; ".join(f"{p} " + "/".join(str(c.get(d, 0)) for d in range(-3, 4)) for p, c in census_per.items())
          + ")")
    walks = args.walk or ["initial-access->discovery", "exfiltration->execution"]
    for wk in walks:
        a, b = (s.strip() for s in wk.split("->"))
        c = dec[(a, b)]
        print(f"walk {a}->{b}: stage {rs.stage_of[a]}->{rs.stage_of[b]} (Delta={c['delta']:+d}); "
              f"rule {keys[c['rule']]} {c['rule']} = {_fmt(c['kernel'])}; d = {_fmt(c['d'])}; "
              f"value = {_fmt(c['kernel'])} x {_fmt(c['d'])} = {_fmt(c['v'])}")

    if args.dry_run_adjacent:
        dry_run_adjacent(rs, spec, verdict)

    if not args.no_compile:
        for stem, _ in figures:
            r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"],
                               cwd=FIG_DIR, capture_output=True, text=True)
            if r.returncode != 0:
                print(r.stdout[-3000:])
                raise SystemExit(f"pdflatex failed on {stem}")
            for ext in (".aux", ".log"):
                p = FIG_DIR / f"{stem}{ext}"
                if p.exists():
                    p.unlink()
            print(f"wrote {(FIG_DIR / (stem + '.pdf')).relative_to(REPO)}")


if __name__ == "__main__":
    main()
