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

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
FOUR = PROFILES[:4]
LABEL = {
    "objective_exfiltration": "exfiltration",
    "objective_impact": "impact",
    "objective_exfiltration_impact": "double extortion",
    "objective_none_c2": "no realised objective",
    "aggregate": "aggregate",
    "baseline": "baseline attacker",
    "movement": "attacker model",
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
SHORT = {
    "none": "none", "ip_shuffle": "IP", "complete_topology": "topology",
    "host_topology": "host", "port_shuffle": "port", "user_shuffle": "user",
    "os_diversity": "OS", "service_diversity": "service", "random": "random",
    "alternative": "alternative",
}
LONG = {
    "none": "no defence", "ip_shuffle": "IP shuffle", "complete_topology": "complete topology shuffle",
    "host_topology": "host topology shuffle", "port_shuffle": "port shuffle", "user_shuffle": "user shuffle",
    "os_diversity": "OS diversity", "service_diversity": "service diversity",
    "random": "random", "alternative": "alternative",
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
