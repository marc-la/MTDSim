#!/usr/bin/env python3
"""Figure 5.x (fig:ablation), §5.4 Ablation of the failure matrix: what
removing the failure matrix changes (a) and what it does not (b). Reads
data/results/ch5_defended/ablation_numbers.json; the table beside it
(tab:ablation) is written by ablation.py from the same JSON.

TAKEAWAYS (Marc 2026-09-28: "changes where the attacker goes but doesn't
change what it achieves"):
  (a) behaviour, the manipulation check. After a failed initial access, the
      model with the failure matrix goes back to reconnaissance and the model
      without it goes on; the actions it goes on to fail, most before they
      run, or succeed without compromising a host.
  (b) outcome. The difference in hosts compromised, with minus without, as
      Cohen's d with its seed-paired interval, per condition, against the
      band section 4.5.4 calls negligible.

DESIGN RECORD (scrutinise-figure, 2026-09-28; cold reader, context critic,
sceptical examiner):
  - c_2 is left out of (a): its net has no move from initial access back to
    reconnaissance, and the matrix multiplies weights, so its pair is the same
    by construction; drawn, it read as "the matrix does nothing for c_2". One
    sentence in the body carries it.
  - (b) draws the paired difference, not each arm: per-arm intervals overlap
    under IP shuffle at 2 000 s while the paired interval excludes zero, and
    section 4.5.4 judges an ablation on the paired difference. The band shows
    the threshold; the interval shows whether it is met on the interval as
    well as the point.
  - "fails" is split into chapter 4's "fails before it runs" (precondition
    unmet, section 4.5) and "runs and fails", both printed.
  - The share that compromises a host is under the print floor in every row,
    so it is printed in its own column beside n (stacked segments carry
    their values, figure_table_conventions.md §f).

ENCODING. The accent means hosts compromised in both panels: the segment
"compromises a host" in (a), the effect on hosts compromised in (b). The other
kinds of next action are greys, darkest for the move the failure matrix makes.
The key reads in segment order, left to right then down.

    python tools/ch5_ablation_figure.py
"""
from __future__ import annotations

import json
import math

from _ch5_style import FONT, LABEL, PREAMBLE, REPO, compile_fig, panel_letter, write_fig

STEM = "fig_5-4a_ablation"
NUMBERS = REPO / "data" / "results" / "ch5_defended" / "ablation_numbers.json"
DRAWN = ("objective_exfiltration", "objective_exfiltration_impact", "objective_none_c2")  # c_2 left out: see above
ARM = {"core": "with", "blind": "without"}
KINDS = (  # key, legend label, fill, text colour on the fill
    ("reconnaissance", "back to reconnaissance", "black!78", "white"),
    ("unmet", "fails before it runs", "black!52", "white"),
    ("runs_fails", "runs and fails", "black!32", "white"),
    ("succeeds", "succeeds, compromises no host", "black!11", "black"),
    ("compromises", "compromises a host", "accent", "white"),
)
PRINT_FLOOR = 0.06  # segments narrower than this share carry no printed value (0.05 does not fit its text)
BAND = 0.2          # section 4.5.4: negligible below Cohen's d of 0.2
CONDS = (
    ("none", r"no MTD"),
    ("ip_shuffle|200", r"IP shuffle\\200\,s"),
    ("ip_shuffle|2000", r"IP shuffle\\2\,000\,s"),
    ("os_diversity|200", r"OS diversity\\200\,s"),
    ("os_diversity|2000", r"OS diversity\\2\,000\,s"),
)


def fmt_n(n: int) -> str:
    return f"{n:,}".replace(",", r"\,")


def signed(v: float, nd: int = 2) -> str:
    s = f"{v:+.{nd}f}"
    s = s[1:] if float(s) == 0 else s
    return s.replace("-", "$-$")


def shares(b: dict) -> dict:
    s = b["after_failed_initial_access"]
    return {"reconnaissance": s["reconnaissance"], "unmet": s["fails_unmet"],
            "runs_fails": s["fails"] - s["fails_unmet"], "succeeds": s["succeeds"],
            "compromises": s["compromises"]}


def main() -> None:
    J = json.loads(NUMBERS.read_text())
    B, R = J["behaviour"], J["reads"]
    L = PREAMBLE[:-1] + [
        r"\definecolor{accent}{RGB}{31,84,140}",
        r"\definecolor{accentlight}{RGB}{200,214,232}",
        r"\begin{document}",
        r"\begin{tikzpicture}[font=%s]" % FONT,
    ]
    w = L.append

    # ---------------- (a) behaviour ----------------
    X0, X1 = 2.2, 12.25           # share 0 .. 1
    CX, NX = 12.95, 13.75         # the compromise column's centre; n's west edge
    BH, GAP_IN, GAP_OUT = 0.34, 0.07, 0.26
    top = 0.0
    KEY_COL = (X0, X0 + 5.6, X0 + 9.3)
    for i, (key, lab, fill, _) in enumerate(KINDS):
        kx, ky = KEY_COL[i % 3], top + 0.13 - 0.40 * (i // 3)
        w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.30,0.22);" % (fill, kx, ky - 0.11))
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (kx + 0.36, ky, lab))
    top -= 0.40
    y = top - 0.75
    w(r"\node[anchor=south,align=center,text=black!60] at (%.3f,%.3f) {compromises a host};" % (CX, y + 0.02))
    for p in DRAWN:
        g0 = y
        for g in ("core", "blind"):
            yb = y - BH
            s = shares(B[p][g])
            x = X0
            for key, _, fill, tcol in KINDS:
                dx = s[key] * (X1 - X0)
                if dx > 0:
                    w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fill, x, yb, x + dx, y))
                    if s[key] >= PRINT_FLOOR:
                        w(r"\node[text=%s] at (%.3f,%.3f) {%.2f};" % (tcol, x + dx / 2, yb + BH / 2, s[key]))
                x += dx
            w(r"\node[anchor=east] at (%.3f,%.3f) {%s};" % (X0 - 0.08, yb + BH / 2, ARM[g]))
            w(r"\node[text=accent] at (%.3f,%.3f) {%.2f};" % (CX, yb + BH / 2, s["compromises"]))
            w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {n\,=\,%s};" % (NX, yb + BH / 2, fmt_n(B[p][g]["failed_initial_access"])))
            y = yb - GAP_IN
        y += GAP_IN
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (0.25, (g0 + y) / 2, LABEL[p]))
        y -= GAP_OUT
    ybot = y + GAP_OUT - 0.08
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, ybot, X1, ybot))
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        xx = X0 + v * (X1 - X0)
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (xx, ybot, xx, ybot - 0.07))
        w(r"\node[anchor=north] at (%.3f,%.3f) {%g};" % (xx, ybot - 0.1, v))
    w(r"\node[anchor=north] at (%.3f,%.3f) {share of the next actions after a failed initial access, no MTD};"
      % ((X0 + X1) / 2, ybot - 0.5))
    panel_letter(w, 0.0, top + 0.42, "a")

    # ---------------- (b) outcome: Cohen's d, with minus without ----------------
    lo_all = min(R[k]["cohen_d_ci95"][0] for k, _ in CONDS)
    hi_all = max(R[k]["cohen_d_ci95"][1] for k, _ in CONDS)
    YMIN = min(-0.3, math.floor((lo_all - 0.02) * 10) / 10)
    YMAX = max(0.3, math.ceil((hi_all + 0.02) * 10) / 10)
    PT = ybot - 1.45
    H = 3.9
    Y0, Y1 = PT - H, PT
    BX0, BX1 = 2.2, 15.4
    gw = (BX1 - BX0) / len(CONDS)

    def yv(v: float) -> float:
        return Y0 + (v - YMIN) / (YMAX - YMIN) * H

    w(r"\fill[black!7] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (BX0, yv(-BAND), BX1, yv(BAND)))
    w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {negligible, $|d| < %g$};" % (BX0 + 0.05, yv(-BAND) + 0.03, BAND))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (BX0, Y0, BX0, Y1))
    t = YMIN
    while t <= YMAX + 1e-9:
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (BX0 - 0.07, yv(t), BX0, yv(t)))
        w(r"\node[anchor=east] at (%.3f,%.3f) {%s};" % (BX0 - 0.1, yv(t), signed(t, 1)))
        t = round(t + 0.1, 10)
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (BX0, yv(0), BX1, yv(0)))
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {Cohen's $d$, with minus without};"
      % (BX0 - 0.85, (Y0 + Y1) / 2))
    for i, (key, lab) in enumerate(CONDS):
        cx = BX0 + gw * (i + 0.5)
        r = R[key]
        d, (lo, hi) = r["cohen_d_per_seed"], r["cohen_d_ci95"]
        w(r"\draw[accent,line width=0.6pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (cx, yv(lo), cx, yv(hi)))
        for yy in (lo, hi):
            w(r"\draw[accent,line width=0.6pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (cx - 0.08, yv(yy), cx + 0.08, yv(yy)))
        w(r"\fill[accent] (%.3f,%.3f) circle (0.075cm);" % (cx, yv(d)))
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (cx + 0.14, yv(d), signed(d)))
        w(r"\node[anchor=north,align=center] at (%.3f,%.3f) {%s};" % (cx, Y0 - 0.1, lab))
    panel_letter(w, 0.0, Y1 + 0.15, "b")

    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    write_fig(STEM, L)
    compile_fig(STEM)
    print("\ncaption facts:")
    print(f"  seeds {J['seeds']}; print floor {PRINT_FLOOR}; band {BAND}; y range {YMIN}..{YMAX}")
    for p in J["behaviour"]:
        for g in ("core", "blind"):
            s = shares(B[p][g])
            print(f"  {LABEL[p]:22s} {ARM[g]:8s} n={B[p][g]['failed_initial_access']:6d}  "
                  + "  ".join(f"{k} {s[k]:.3f}" for k, *_ in KINDS))
    for k, _ in CONDS:
        r = R[k]
        print(f"  {k:18s} d {r['cohen_d_per_seed']:+.3f} [{r['cohen_d_ci95'][0]:+.3f}, {r['cohen_d_ci95'][1]:+.3f}]")


if __name__ == "__main__":
    main()
