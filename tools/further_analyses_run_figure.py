"""Figure F.1 of Appendix F (app:fa-traced-run): one run of the APT attacker
model with no MTD and under IP shuffle, drawn from its stored records.

Registry row B18 (Marc 2026-10-08: an example run showing adaptivity; triaged
2026-10-09). No re-run: the two runs are rows of the reported corpus
(ch5_defended/runs_reported.jsonl), copied by
`data/results/ch6_further_analyses/further_analyses.py f4` into
`further_analyses_numbers.json`. The run is chosen by a rule fixed before any
run was looked at: c1, the attack profile with the most attack flows, on the
lowest seed on which it reaches a target host with no MTD.

Takeaway: the two runs share the seed's draws, so they are the same run until
the first MTD deployment that lands on an attack action; from there, under IP
shuffle, the attack actions are refused for a missing precondition and the
attacker compromises one host where, with no MTD, the same Petri net takes
eleven and a target host.

Design: one lane per attack action in the baseline attacker's order (Figure
2.3), and one for the tactics with no attack action, so the lanes read in
chapter 2's words (chapter 5 groups tactics the same way, Figure 5.1). A record
is a bar from its start to its end: dark where the attack action ran, mid grey
where it was refused for a missing precondition, light grey where the tactic
dispatches no attack action; hatched where an MTD deployment interrupted it.
The one accent marks a host compromised. A thin grey line marks each MTD
deployment. Panels (a) and (b) give the whole run; (c) and (d) its first
1 000 s. Greys and one accent (thesis figure pipeline).

Usage:  python tools/further_analyses_run_figure.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import ACTIVITY, FONT, PREAMBLE, REPO, compile_fig, write_fig  # noqa: E402

NUMBERS = REPO / "data" / "results" / "ch6_further_analyses" / "further_analyses_numbers.json"
STEM = "fig_FA-4_traced_run"
COMPROMISE = {("EXPLOIT_VULN", "EXPLOIT_COMPROMISED"), ("BRUTE_FORCE", "TRUE"), ("SCAN_PORT", "TRUE")}
LANES = ("SCAN_HOST", "ENUM_HOST", "SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE", "SCAN_NEIGHBOR", "")
LANE_NAME = {v: ACTIVITY[v] for v in LANES[:-1]} | {"": "no attack action"}

X0, W = 3.1, 12.5      # plot left edge and width (cm)
LANE_H = 0.34
PLOT_H = LANE_H * len(LANES)
PANEL_GAP = 1.35       # plot bottom to the next panel's plot top: ticks, x title, next title


def draw_panel(w, run: dict, ytop: float, t1: float, letter: str, title: str, ticks: list[float]) -> float:
    y0 = ytop - PLOT_H
    sx = W / t1

    def x(t: float) -> float:
        return X0 + min(t, t1) * sx

    w(r"\node[anchor=south west,inner sep=0] at (%.3f,%.3f) {\textbf{(%s)} %s};" % (X0, ytop + 0.12, letter, title))
    # MTD deployments
    for e in run["mtd_executions"]:
        if e[1] <= t1:
            w(r"\draw[black!28,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x(e[1]), y0, x(e[1]), ytop))
    # lanes
    for i, v in enumerate(LANES):
        yc = ytop - (i + 0.5) * LANE_H
        w(r"\node[anchor=east,inner sep=0] at (%.3f,%.3f) {%s};" % (X0 - 0.12, yc, LANE_NAME[v]))
        if i:
            w(r"\draw[black!10,line width=0.2pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, ytop - i * LANE_H, X0 + W, ytop - i * LANE_H))
    comps = []
    for r in run["records"]:
        place, verb, outcome, verdict, blocked, interrupted, dwell, start, end, cls = r
        if start >= t1:
            break
        i = LANES.index(verb)
        yb, yt = ytop - (i + 0.8) * LANE_H, ytop - (i + 0.2) * LANE_H
        fill = "black!15" if not verb else ("black!35" if blocked else "black!85")
        xa, xb = x(start), max(x(end), x(start) + 0.02)  # a visible sliver for an instant record
        w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fill, xa, yb, xb, yt))
        if interrupted:
            w(r"\fill[pattern=north east lines,pattern color=black] (%.3f,%.3f) rectangle (%.3f,%.3f);"
              % (xa, yb, max(xb, xa + 0.08), yt))
        if (verb, outcome) in COMPROMISE and end <= t1:
            comps.append((x(end), ytop - (i + 0.5) * LANE_H))
    for cx, cy in comps:
        w(r"\fill[cexf] (%.3f,%.3f) circle (0.075);" % (cx, cy))
        w(r"\draw[white,line width=0.3pt] (%.3f,%.3f) circle (0.075);" % (cx, cy))
    # frame and axis
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (X0, y0, X0 + W, ytop))
    for t in ticks:
        w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x(t), y0, x(t), y0 - 0.08))
        lab = f"{int(t):,}".replace(",", r"\,")
        w(r"\node[anchor=north,inner sep=1pt] at (%.3f,%.3f) {%s};" % (x(t), y0 - 0.1, lab))
    w(r"\node[anchor=north,inner sep=0] at (%.3f,%.3f) {Time (s)};" % (X0 + W / 2, y0 - 0.48))
    return y0 - PANEL_GAP


def main() -> None:
    d = json.loads(NUMBERS.read_text())["f4"]
    none, ip = d["runs"]["none|0"], d["runs"]["ip_shuffle|200"]
    lines = list(PREAMBLE) + [r"\begin{tikzpicture}[font=%s]" % FONT]
    w = lines.append
    whole = [0, 2500, 5000, 7500, 10000, 12500, 15000]
    early = [0, 200, 400, 600, 800, 1000]
    y = 0.0
    y = draw_panel(w, none, y, 15000, "a", "No MTD, the whole run", whole)
    y = draw_panel(w, ip, y, 15000, "b", r"IP shuffle every 200\,s, the whole run", whole)
    y = draw_panel(w, none, y, 1000, "c", r"No MTD, the first 1\,000\,s", early)
    y = draw_panel(w, ip, y, 1000, "d", r"IP shuffle every 200\,s, the first 1\,000\,s", early)
    # key
    ky = y + PANEL_GAP - 0.95
    kx = X0
    for fill, label in (("black!85", "attack action ran"), ("black!35", "refused for a missing precondition"),
                        ("black!15", "no attack action")):
        w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fill, kx, ky - 0.1, kx + 0.35, ky + 0.1))
        w(r"\node[anchor=west,inner sep=0] at (%.3f,%.3f) {%s};" % (kx + 0.45, ky, label))
        kx += 0.45 + 0.16 * len(label) + 0.5
    ky -= 0.42
    kx = X0
    w(r"\fill[black!35] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (kx, ky - 0.1, kx + 0.35, ky + 0.1))
    w(r"\fill[pattern=north east lines,pattern color=black] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (kx, ky - 0.1, kx + 0.35, ky + 0.1))
    w(r"\node[anchor=west,inner sep=0] at (%.3f,%.3f) {interrupted by MTD};" % (kx + 0.45, ky))
    kx += 0.45 + 0.16 * len("interrupted by MTD") + 0.5
    w(r"\draw[black!28,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (kx + 0.17, ky - 0.15, kx + 0.17, ky + 0.15))
    w(r"\node[anchor=west,inner sep=0] at (%.3f,%.3f) {MTD deployment};" % (kx + 0.45, ky))
    kx += 0.45 + 0.16 * len("MTD deployment") + 0.5
    w(r"\fill[cexf] (%.3f,%.3f) circle (0.075);" % (kx + 0.17, ky))
    w(r"\node[anchor=west,inner sep=0] at (%.3f,%.3f) {host compromised};" % (kx + 0.45, ky))
    lines += [r"\end{tikzpicture}", r"\end{document}"]
    write_fig(STEM, lines)
    compile_fig(STEM)


if __name__ == "__main__":
    main()
