"""Figure 5.8 (fig:ablation-memory), §5.4.2 Vulnerability memory: what the
memory changes (exploit success, top row) and what it does not (hosts
compromised, bottom row), against the number of services per operating system.

SCRUTINY 2026-09-30 (cold reader, context critic, numbers auditor, sceptical
examiner). Taken: row 1 from zero, as row 2 (a 0.6 floor inflated the
contrast); "exploit success" had no antecedent in chapters 2-4, so the title
and axis say "exploits that succeed"; the bound's dotted line hid behind the
memory-on line, so it carries a cross; the arm is "every exploit succeeding"
everywhere. Not taken: replacing (c, d) with d against the pool (examiner) ---
Marc ruled the two-line float, and Table 5.6 carries d; the numbers auditor
matched every plotted point to the raw runs.
Reads data/results/ch5_defended/memory_ablation_numbers.json; the table beside
it (tab:ablation-memory) is written by memory_ablation.py from the same JSON.

TAKEAWAYS (Marc 2026-09-30: "the mechanism works but the outcome doesn't
change"; "pool size on the X axis ... hosts compromised on the other ... two
lines"):
  T1 (a, b) the manipulation check. The memory raises the share of exploits
     that succeed, and the rise grows as the pool shrinks.
  T2 (c, d) the outcome. The memory adds under half a host at any pool
     (every d below 0.2, Table 5.6). Reworded after scrutiny: "the same with
     and without" was false (d > 0 in 16 of 18 cells).
  T3 (c, d) the bound. Every exploit succeeding raises hosts compromised by
     under a host at any pool.
  Every d below 0.2 is Table 5.6's; the NCR reduction is a body sentence.

DESIGN. A 2 x 2 grid: columns are the conditions, rows the measures, so each
column reads down from "the mechanism works" to "the outcome does not move".
Service diversity is drawn because it only redraws services from the pool; OS
diversity, which also changes which exploits an operating system rules out,
is in the table. Every exploit succeeding is 1.0 by construction in the top
row, drawn there as the ceiling the key promises, without intervals. The bottom row starts at zero
hosts and the two columns share it (Wilke §21.1), so a difference is seen at
its true size. Intervals are 95 % bootstrap intervals over (profile, seed)
units per arm; the paired difference is Table 5.6's d.

ENCODING (§o rule 5). The memory on is the APT attacker model as evaluated,
so it is black with a filled circle, on top. The memory off is grey with an
open circle, solid: the grey dashed square is the baseline attacker's in every
figure. Every exploit succeeding is a bound, not an attacker: black dotted,
with a cross.

    python tools/ch5_memory_ablation_figure.py
"""
from __future__ import annotations

import json
import math

from _ch5_style import (DOT, FONT, PREAMBLE, REPO, axes, compile_fig, errorbar, key_row, marker,
                        panel_title, write_fig)

STEM = "fig_5-4b_ablation_memory"
NUMBERS = REPO / "data" / "results" / "ch5_defended" / "memory_ablation_numbers.json"
COLS = (("none", "no MTD"), ("service_diversity", "service diversity"))
SERIES = (  # arm, key label, colour, line style, marker, x dodge (cm); drawn in this order
    ("perfect", "every exploit succeeding", "black", DOT, "cross", 0.1),
    ("off", "memory off", "black!45", "", "ocircle", -0.1),
    ("on", "memory on", "black", "", "circle", 0.0),
)
LOG_LO, LOG_HI = 0.8, 25.0  # the x domain, so the end markers sit off the frame


def main() -> None:
    J = json.loads(NUMBERS.read_text())
    R, pools = J["reads"], J["pools"]
    L = PREAMBLE[:-1] + [r"\begin{document}", r"\begin{tikzpicture}[font=%s]" % FONT]
    w = L.append

    W = 6.55
    XA = (1.55, 9.35)                     # each column's y-axis
    H1, H2 = 2.9, 3.6                     # row heights
    TOP = 0.0
    ROW1_TOP = TOP - 0.55 - 0.55          # below the key and row 1's titles
    ROW1_BOT = ROW1_TOP - H1
    ROW2_TOP = ROW1_BOT - 1.35            # row 1's tick labels, then row 2's titles
    ROW2_BOT = ROW2_TOP - H2

    def xv(x0: float, v: float) -> float:
        return x0 + (math.log(v) - math.log(LOG_LO)) / (math.log(LOG_HI) - math.log(LOG_LO)) * W

    key_row(w, XA[0], TOP, [(lab, "dotted" if style else "line", col, mk)
                           for _, lab, col, style, mk, _ in reversed(SERIES)], gap=0.9)

    rows = (
        ("roll_success", "Exploits that succeed", "Share of exploits that succeed", ROW1_TOP, ROW1_BOT,
         (0.0, 1.1), (0.0, 0.2, 0.4, 0.6, 0.8, 1.0), lambda v: f"{v:g}"),
        ("hosts", "Hosts compromised", "Hosts compromised per run", ROW2_TOP, ROW2_BOT,
         (0.0, 10.0), (0, 2, 4, 6, 8, 10), lambda v: f"{v:g}"),
    )
    letters = iter("abcd")
    for measure, title, ytitle, yt, yb, (ymin, ymax), yticks, yfmt in rows:
        def yv(v: float) -> float:
            return yb + (v - ymin) / (ymax - ymin) * (yt - yb)
        for ci, (cond, cname) in enumerate(COLS):
            x0 = XA[ci]
            axes(w, x0, x0 + W, yb, yt,
                 xticks=[(p, xv(x0, p)) for p in pools],
                 yticks=[(v, yv(v)) for v in yticks],
                 xlabel=None,
                 ylabel=(ytitle if ci == 0 else None), ylabels=(ci == 0), yfmt=yfmt,
                 ylabel_offset=0.8)
            panel_title(w, x0, yt, f"{title}, {cname}", next(letters))
            for arm, _, col, style, mk, dx in SERIES:
                if measure == "roll_success" and arm == "perfect":
                    # 1.0 by construction: drawn as the ceiling the key promises
                    # (both cold readers, 2026-09-30), without intervals
                    xs = [xv(x0, p) + dx for p in pools]
                    w(r"\draw[%s,line width=0.8pt,%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, style, xs[0], yv(1.0), xs[-1], yv(1.0)))
                    for x in xs:
                        marker(w, mk, col, x, yv(1.0), r=0.07)
                    continue
                pts = []
                for p in pools:
                    a = R[f"{p}|{cond}"]["arms"][arm]
                    v, (lo, hi) = a[measure], a[f"{measure}_ci95"]
                    pts.append((xv(x0, p) + dx, v, lo, hi))
                w(r"\draw[%s,line width=0.8pt%s] %s;" % (col, "," + style if style else "",
                  " -- ".join("(%.3f,%.3f)" % (x, yv(v)) for x, v, _, _ in pts)))
                for x, v, lo, hi in pts:
                    errorbar(w, x, yv(lo), yv(hi), col=col, cap=0.045)
                    if mk:
                        marker(w, mk, col, x, yv(v), r=0.07)

    w(r"\node[anchor=north] at (%.3f,%.3f) {Services per operating system (log scale)};"
      % ((XA[0] + XA[1] + W) / 2, ROW2_BOT - 0.5))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    write_fig(STEM, L)
    compile_fig(STEM)
    print("\ncaption facts:")
    for cond, _ in COLS:
        for p in pools:
            a = R[f"{p}|{cond}"]["arms"]
            print(f"  {cond:18s} {p:3d}  success off {a['off']['roll_success']:.3f} on {a['on']['roll_success']:.3f}  "
                  f"hosts off {a['off']['hosts']:.2f} on {a['on']['hosts']:.2f} all {a['perfect']['hosts']:.2f}")


if __name__ == "__main__":
    main()
