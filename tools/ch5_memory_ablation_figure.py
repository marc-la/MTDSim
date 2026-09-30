"""Figure 5.8 (fig:ablation-memory), §5.4.2 Vulnerability memory: NCR with the
memory on and off, against the number of services per operating system, with
no MTD (a) and under service diversity at 200 s (b). Reads
data/results/ch5_defended/memory_ablation_numbers.json; the table beside it
(tab:ablation-memory) is written by memory_ablation.py from the same JSON.

TAKEAWAY (Marc 2026-09-30: "pool size on the X axis ... network compromise
ratio ... two lines"; "I thought we were comparing memory on and memory off"):
  At every pool the APT attacker model compromises about the same share of the
  network with the memory as without it (every d below 0.2, Table 5.6).

DESIGN RECORD.
  - 2026-09-30, first build: a 2 x 2 (the share of exploits that succeed over
    hosts compromised) with a third arm, every exploit succeeding. Scrutinised
    (two cold readers, context critic, numbers auditor, sceptical examiner).
  - 2026-09-30, rebuilt on Marc's read ("too many things going on"):
      * every exploit succeeding leaves the figure, the table and chapter 5's
        prose; it stays in the JSON as evidence for §6.3's why;
      * the share of exploits that succeed leaves the figure: it is no Table
        4.3 metric, and with the memory off it is flat at 0.70 by
        construction (CVSS complexity does not depend on the pool). It is the
        manipulation check, told in one body sentence with Table 5.6's values;
      * hosts compromised becomes NCR, the chapter 4 metric (hosts / 50),
        as section 5.4.1 reports it.
  - Known and not drawn around: NCR without the memory is lower with one
    service per operating system, because that network has fewer hosts an
    exploit can take (about 39 of 50 against 41 to 43; generated networks,
    40 seeds). The body text says each comparison is within a pool; the
    along-axis shape is the network's, and its reading is chapter 6's.

ENCODING (§o rule 5). The memory on is the APT attacker model as evaluated:
black, filled circle, on top. The memory off: grey, open circle, solid (the
grey dashed square is the baseline attacker's in every figure). Both rows of
the old design started at zero; this axis does too, so the gap is seen at its
true size. Intervals are 95 % bootstrap intervals over runs per arm; the
paired difference is Table 5.6's d.

    python tools/ch5_memory_ablation_figure.py
"""
from __future__ import annotations

import json
import math

from _ch5_style import (FONT, PREAMBLE, REPO, axes, compile_fig, errorbar, key_row, marker,
                        panel_title, write_fig)

STEM = "fig_5-4b_ablation_memory"
NUMBERS = REPO / "data" / "results" / "ch5_defended" / "memory_ablation_numbers.json"
HOSTS = 50
COLS = (("none", "No MTD"), ("service_diversity", "Service diversity"))
SERIES = (  # arm, key label, colour, marker, x dodge (cm); drawn in this order
    ("off", "memory off", "black!45", "ocircle", -0.06),
    ("on", "memory on", "black", "circle", 0.06),
)
LOG_LO, LOG_HI = 0.8, 25.0  # the x domain, so the end markers sit off the frame
YMAX, YTICKS = 0.2, (0.0, 0.05, 0.10, 0.15, 0.20)


def main() -> None:
    J = json.loads(NUMBERS.read_text())
    R, pools = J["reads"], J["pools"]
    L = PREAMBLE[:-1] + [r"\begin{document}", r"\begin{tikzpicture}[font=%s]" % FONT]
    w = L.append

    W, H = 6.55, 4.2
    XA = (1.55, 9.35)                     # each panel's y-axis
    TOP = 0.0
    PT = TOP - 0.55 - 0.55                # below the key and the panel titles
    PB = PT - H

    def xv(x0: float, v: float) -> float:
        return x0 + (math.log(v) - math.log(LOG_LO)) / (math.log(LOG_HI) - math.log(LOG_LO)) * W

    def yv(v: float) -> float:
        return PB + v / YMAX * H

    key_row(w, XA[0], TOP, [(lab, "line", col, mk) for _, lab, col, mk, _ in reversed(SERIES)], gap=0.9)
    for ci, (cond, cname) in enumerate(COLS):
        x0 = XA[ci]
        axes(w, x0, x0 + W, PB, PT,
             xticks=[(p, xv(x0, p)) for p in pools],
             yticks=[(v, yv(v)) for v in YTICKS],
             xlabel=None, ylabel=("NCR" if ci == 0 else None), ylabels=(ci == 0),
             yfmt=lambda v: f"{v:.2f}", ylabel_offset=0.95)
        panel_title(w, x0, PT, cname, "ab"[ci])
        for arm, _, col, mk, dx in SERIES:
            pts = []
            for p in pools:
                a = R[f"{p}|{cond}"]["arms"][arm]
                lo, hi = a["hosts_ci95"]
                pts.append((xv(x0, p) + dx, a["hosts"] / HOSTS, lo / HOSTS, hi / HOSTS))
            w(r"\draw[%s,line width=0.8pt] %s;" % (col, " -- ".join("(%.3f,%.3f)" % (x, yv(v)) for x, v, _, _ in pts)))
            for x, v, lo, hi in pts:
                errorbar(w, x, yv(lo), yv(hi), col=col, cap=0.045)
                marker(w, mk, col, x, yv(v), r=0.07)
    w(r"\node[anchor=north] at (%.3f,%.3f) {Services per operating system (log scale)};"
      % ((XA[0] + XA[1] + W) / 2, PB - 0.5))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    write_fig(STEM, L)
    compile_fig(STEM)
    print("\ncaption facts (NCR off / on):")
    for cond, _ in COLS:
        print(f"  {cond:18s} " + "  ".join(
            f"{p}: {R[f'{p}|{cond}']['arms']['off']['hosts'] / HOSTS:.3f}/{R[f'{p}|{cond}']['arms']['on']['hosts'] / HOSTS:.3f}"
            for p in pools))


if __name__ == "__main__":
    main()
