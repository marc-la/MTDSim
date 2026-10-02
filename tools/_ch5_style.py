"""Shared house style for the chapter 5 results generators (§5.3 onward).

Everything here is the contract tools/ch5_unopposed_figures.py set on
2026-09-15 and the later generators reuse rather than re-pick: the TikZ
standalone preamble (12 pt, helvet 0.92, 2 pt border), the series encoding
(one hue and one marker per attack profile; the baseline attacker a dashed
grey line, or a hatched bar where the series is an arm), the presentation
names, the mechanism short names, the axis helper and the compile-and-measure
step that prints the fits / TOO WIDE verdict against \\textwidth.

figure_table_conventions.md §f, §h, §k, §l; thesis-figure-pipeline memory.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIG_DIR = REPO / "docs" / "thesis" / "figures"
TAB_DIR = REPO / "docs" / "thesis" / "tables"
TEXTWIDTH_CM = 455.24 / 28.45  # 16.0 cm, measured
PACK_CM = 15.7                 # natural width a full-width figure packs to
FONT = r"\footnotesize"

# The attack graph before partition (corpus profile "aggregate", once c_agg)
# left every chapter 5 float on 2026-10-02 (Marc): it is Section 5.4.1's
# ablation arm, read there by data/results/ch5_defended/partition_ablation.py.
PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
)
FOUR = PROFILES[:4]
LABEL = {
    # the profile codes chapter 4 declares (§4.3, tab:gspn-notation; Marc's
    # ruling 2026-09-22): c_1 exfiltration, c_2 impact, c_3 double extortion,
    # c_4 no realised objective, c_agg the unpartitioned aggregate
    "objective_exfiltration": "$c_1$",
    "objective_impact": "$c_2$",
    "objective_exfiltration_impact": "$c_3$",
    "objective_none_c2": "$c_4$",
    "aggregate": r"$c_{\mathrm{agg}}$",
    "baseline": "baseline attacker",
    "movement": "APT attacker model",  # registry row 1 as ruled 2026-09-22 (register E2: the model is named by its chapter title; "movement attacker" deprecated)
}
COLOUR = {  # RGB; the chapter's series contract (validated 2026-09-15)
    "objective_exfiltration": "31,84,140",
    "objective_impact": "179,38,30",
    "objective_exfiltration_impact": "168,116,26",
    "objective_none_c2": "111,78,156",
    "aggregate": "58,125,68",
    "baseline": "122,122,122",
    "movement": "31,84,140",
}
CNAME = {
    "objective_exfiltration": "cexf",
    "objective_impact": "cimp",
    "objective_exfiltration_impact": "cdex",
    "objective_none_c2": "cnon",
    "aggregate": "cagg",
    "baseline": "cbase",
    "movement": "cmov",
}
MARK = {
    "objective_exfiltration": "circle",
    "objective_impact": "square",
    "objective_exfiltration_impact": "triangle",
    "objective_none_c2": "diamond",
    "aggregate": "downtriangle",
    "movement": "circle",
    "baseline": "square",
}
# defence conditions: corpus key -> short name on an axis, and long name
SINGLES = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle",
           "user_shuffle", "os_diversity", "service_diversity")
SCHEMES = ("random", "alternative")
DEFENDED = SINGLES + SCHEMES
# MTDShield as released and random over its four mechanisms (2026-09-25;
# handoff 2026-09-25_mtdshield_preliminary_run.md), in the core corpus only
SHIELD = ("random_four", "mtdshield")
# run as MTDShield's matched control but reported in no float (Marc 2026-09-25:
# "a bit vacuous ... we don't talk about MTDShield's four"); it stays in the
# corpus and numbers.json, so a body sentence can still quote it
UNREPORTED = ("random_four",)
SHORT = {
    "none": "none", "ip_shuffle": "IP", "complete_topology": "topology",
    "host_topology": "host", "port_shuffle": "port", "user_shuffle": "user",
    "os_diversity": "OS", "service_diversity": "service", "random": "random",
    "alternative": "alternative", "random_four": "random (four)", "mtdshield": "MTDShield",
}
LONG = {
    "none": "no MTD", "ip_shuffle": "IP shuffle", "complete_topology": "complete topology shuffle",
    "host_topology": "host topology shuffle", "port_shuffle": "port shuffle", "user_shuffle": "user shuffle",
    "os_diversity": "OS diversity", "service_diversity": "service diversity",
    "random": "random", "alternative": "alternative",
    "random_four": "random, MTDShield's four", "mtdshield": "MTDShield",
}
ACTIVITY = {
    "SCAN_HOST": "scan host", "ENUM_HOST": "enumerate host", "SCAN_PORT": "scan port",
    "EXPLOIT_VULN": "exploit", "BRUTE_FORCE": "brute force", "SCAN_NEIGHBOR": "scan neighbours",
    "": "dwell",
}

PREAMBLE = [
    r"\documentclass[tikz,12pt,border=2pt]{standalone}",
    r"\usepackage[T1]{fontenc}",
    r"\usepackage[scaled=0.92]{helvet}",
    r"\renewcommand{\familydefault}{\sfdefault}",
    r"\usetikzlibrary{calc,patterns}",
] + [r"\definecolor{%s}{RGB}{%s}" % (CNAME[k], v) for k, v in COLOUR.items()] + [
    r"\begin{document}",
]


def fmt_thousands(v: float) -> str:
    return f"{int(round(v)):,}".replace(",", r"\,")


def marker(w, kind: str, col: str, x: float, y: float, r: float = 0.075) -> None:
    if kind == "circle":
        w(r"\fill[%s] (%.3f,%.3f) circle (%.3fcm);" % (col, x, y, r))
    elif kind == "square":
        w(r"\fill[%s] (%.3f,%.3f) ++(%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (col, x, y, -r, -r, 2 * r, 2 * r))
    elif kind == "triangle":
        w(r"\fill[%s] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- cycle;" % (col, x - r * 1.1, y - r * 0.9, x + r * 1.1, y - r * 0.9, x, y + r * 1.2))
    elif kind == "downtriangle":
        w(r"\fill[%s] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- cycle;" % (col, x - r * 1.1, y + r * 0.9, x + r * 1.1, y + r * 0.9, x, y - r * 1.2))
    elif kind == "cross":  # a bound, never an attacker (§5.4.2: every exploit succeeding)
        w(r"\draw[%s,line width=0.6pt] (%.3f,%.3f) -- ++(%.3f,%.3f) (%.3f,%.3f) -- ++(%.3f,%.3f);"
          % (col, x - r, y - r, 2 * r, 2 * r, x - r, y + r, 2 * r, -2 * r))
    elif kind == "ocircle":  # open circle: a series that must not read as filled (§5.4.2, memory off)
        w(r"\filldraw[fill=white,draw=%s,line width=0.6pt] (%.3f,%.3f) circle (%.3fcm);" % (col, x, y, r * 0.9))
    elif kind == "diamond":
        w(r"\fill[%s] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- cycle;" % (col, x, y + r * 1.25, x + r * 1.1, y, x, y - r * 1.25, x - r * 1.1, y))


def axes(w, X0, X1, Y0, Y1, *, xticks, yticks, xlabel, ylabel, ylabels=True,
         xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xtick_rotate=0, grid=True,
         ylabel_offset=0.85, xlabel_offset=0.5):
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, Y0, X1, Y0))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, Y0, X0, Y1))
    for v, y in yticks:
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0 - 0.07, y, X0, y))
        if grid and abs(y - Y0) > 1e-6:
            w(r"\draw[black!12,line width=0.2pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, y, X1, y))
        if ylabels:
            w(r"\node[anchor=east] at (%.3f,%.3f) {%s};" % (X0 - 0.1, y, yfmt(v)))
    for v, x in xticks:
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, Y0, x, Y0 - 0.07))
        if xtick_rotate:
            w(r"\node[anchor=north east,rotate=%d] at (%.3f,%.3f) {%s};" % (xtick_rotate, x + 0.05, Y0 - 0.08, xfmt(v)))
        else:
            w(r"\node[anchor=north] at (%.3f,%.3f) {%s};" % (x, Y0 - 0.1, xfmt(v)))
    if xlabel:
        w(r"\node[anchor=north] at (%.3f,%.3f) {%s};" % ((X0 + X1) / 2, Y0 - xlabel_offset, xlabel))
    if ylabel:
        w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {%s};" % (X0 - ylabel_offset, (Y0 + Y1) / 2, ylabel))


def panel_letter(w, x: float, y: float, letter: str) -> None:
    w(r"\node[anchor=south west,font=\footnotesize\bfseries] at (%.3f,%.3f) {(%s)};" % (x, y, letter))


# --- the results-figure layout (figure_table_conventions.md §o, 2026-09-30) -----
# Every panel's title and every key sit in the same place in every chapter 5
# figure, so these two helpers are the only way a generator draws them:
#   figure-wide key  -- the top of the figure, left edge on the first y-axis
#   panel title      -- above its plot, left edge on that panel's y-axis
#   panel-only key   -- directly under that panel's title, the same left edge
TITLE_GAP = 0.08   # plot top to the title's baseline box
TITLE_H = 0.42     # a title line's height, for stacking a key under it
KEY_H = 0.42       # a key row's height
BASE_DASH = "dash pattern=on 2.4pt off 1.4pt"  # the baseline attacker's line, every figure
DOT = "dash pattern=on 0.9pt off 1.3pt"  # a bound, never an attacker (§5.4.2: every exploit succeeds)


def panel_title(w, x: float, ytop: float, title: str, letter: str | None = None) -> float:
    """``(a)  Title`` above a plot whose y-axis is at ``x`` and top at ``ytop``;
    a single-panel figure passes no letter. Returns the y above the title."""
    head = (r"\textbf{(%s)}\enspace " % letter if letter else "") + title
    w(r"\node[anchor=south west,inner sep=0pt] at (%.3f,%.3f) {%s};" % (x, ytop + TITLE_GAP, head))
    return ytop + TITLE_GAP + TITLE_H


def key_row(w, x: float, y: float, entries, *, xmax: float | None = None, gap: float = 0.45) -> float:
    """One key row, left edge at ``x``, centred on ``y``; wraps at ``xmax``.
    ``entries``: (label, kind, colour, marker) where kind is ``line``,
    ``dashed`` (line + marker), ``dotted`` (a bound), ``bar`` (solid swatch), ``hatch`` (the
    baseline's hatched bar) or ``band`` (a shaded region), or two joined by
    ``+`` where one series is drawn both ways (``bar+line``). Returns the last
    row's y."""
    glyph_w = {"line": 0.68, "dashed": 0.68, "dotted": 0.68, "bar": 0.36, "hatch": 0.36, "band": 0.36}
    x0 = x
    for label, kind, col, mark in entries:
        parts = kind.split("+")
        plain = label.replace("$", "").replace(r"\mathrm", "").replace("{", "").replace("}", "")
        width = sum(glyph_w[k] for k in parts) + 0.155 * len(plain) + gap
        if xmax is not None and x > x0 and x + width > xmax:
            x, y = x0, y - KEY_H
        tx = x
        for k in parts:
            if k in ("line", "dashed", "dotted"):
                style = "%s,line width=0.8pt%s" % (col, {"dashed": "," + BASE_DASH, "dotted": "," + DOT}.get(k, ""))
                w(r"\draw[%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (style, tx, y, tx + 0.6, y))
                if mark:
                    marker(w, mark, col, tx + 0.3, y, r=0.065)
            elif k == "hatch":
                w(r"\fill[pattern=north east lines,pattern color=%s] (%.3f,%.3f) rectangle ++(0.30,0.22);" % (col, tx, y - 0.11))
                w(r"\draw[%s,line width=0.3pt] (%.3f,%.3f) rectangle ++(0.30,0.22);" % (col, tx, y - 0.11))
            else:  # bar, band
                w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.30,0.22);" % (col, tx, y - 0.11))
            tx += glyph_w[k]
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (tx, y, label))
        x += width
    return y


def errorbar(w, x: float, lo: float, hi: float, col: str = "black!70", cap: float = 0.05) -> None:
    w(r"\draw[%s,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x, lo, x, hi))
    w(r"\draw[%s,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x - cap, lo, x + cap, lo))
    w(r"\draw[%s,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x - cap, hi, x + cap, hi))


def write_fig(stem: str, lines: list[str]) -> Path:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    p = FIG_DIR / f"{stem}.tex"
    p.write_text("\n".join(lines) + "\n")
    return p


def compile_fig(stem: str) -> None:
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"],
                       cwd=FIG_DIR, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:])
        raise SystemExit(f"pdflatex failed on {stem}")
    for ext in (".aux", ".log"):
        p = FIG_DIR / f"{stem}{ext}"
        if p.exists():
            p.unlink()
    bb = subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=bbox", f"{stem}.pdf"],
                        cwd=FIG_DIR, capture_output=True, text=True)
    for line in bb.stderr.splitlines():
        if line.startswith("%%BoundingBox"):
            _, x0, y0, x1, y1 = line.split()
            wcm, hcm = (int(x1) - int(x0)) / 28.45, (int(y1) - int(y0)) / 28.45
            print(f"wrote figures/{stem}.pdf  natural size {wcm:.1f} x {hcm:.1f} cm  "
                  f"(textwidth {TEXTWIDTH_CM:.1f} cm; {'fits' if wcm <= TEXTWIDTH_CM + 0.05 else 'TOO WIDE'})")


def pm(iv: dict, nd: int = 1) -> str:
    return "$%.*f \\pm %.*f$" % (nd, iv["mean"], nd, iv["ci95"])


def interval_str(point: float, lo: float, hi: float, nd: int = 2) -> str:
    return "$%.*f$ [%.*f, %.*f]" % (nd, point, nd, lo, nd, hi)


# --- reporting thresholds shared by every chapter 5 table -----------------------
# An MTTC is reported only over enough runs (docs/workflows/results_presentation_
# standard.md N1, Marc 2026-10-02), after the NCHS standard for rates from 2023
# data (Kochanek et al. 2024, s. 3, p. 18): at least 10 events, and a 95 %
# interval no wider than 160 % of the estimate. MTTC is a mean over the runs
# that compromise a target host, not a rate, so the threshold is borrowed by
# declared analogy.
MTTC_MIN_RUNS = 10
MTTC_MAX_REL_WIDTH = 1.6


def mttc_unreported(iv: dict | None) -> str | None:
    """Why an MTTC (``{"n", "mean", "ci95"}``) is not reported, or None when it is."""
    if not iv or iv["n"] < MTTC_MIN_RUNS:
        return "runs"
    if 2 * iv["ci95"] / iv["mean"] > MTTC_MAX_REL_WIDTH:
        return "width"
    return None


def mttc_dash_decode(reasons: set) -> str:
    """The caption's decode of the MTTC dash, naming only the reasons that fired."""
    why = []
    if "runs" in reasons:
        why.append("fewer than %d runs compromise a target host" % MTTC_MIN_RUNS)
    if "width" in reasons:
        why.append(r"its 95\,\%% interval is wider than %d\,\%% of its value" % round(100 * MTTC_MAX_REL_WIDTH))
    return (" A dash marks an MTTC not reported: %s." % " or ".join(why)) if why else ""


def bounded(v: float, nd: int = 2, lo: float | None = None, hi: float | None = None) -> str:
    """A value at ``nd`` decimals that never prints a bound of its scale it does
    not reach (results presentation standard P2, Marc 2026-10-02): a reduction
    of 0.997 is "> 0.99", not 1.00; an ASP of 0.0003 is "< 0.01", not 0.00.
    A value that rounds to zero prints no sign."""
    step = 10.0 ** -nd
    if hi is not None and v < hi and round(v, nd) >= hi:
        return r"${>}%.*f$" % (nd, hi - step)  # braced: no relation spacing
    if lo is not None and v > lo and round(v, nd) <= lo:
        return r"${<}%.*f$" % (nd, lo + step)
    t = "%.*f" % (nd, v)
    return "$%s$" % ("0." + "0" * nd if t == "-0." + "0" * nd else t)
