#!/usr/bin/env python3
"""Chapter 5 §5.3.1's floats: Figure 5.3, what an MTD deployment costs each
attacker, and Table 5.x beside it.

REBUILT 2026-09-30 on the metrics Section 4.5.3 now defines (Marc's rulings;
record docs/implementation/disruption_mechanism.md; handoff
docs/handoffs/2026-09-30_disruption_metrics.md). The compromise rate after an MTD
deployment is retired with its reader, disruption.py; time_lost.py is the reader.

  (a), (b) for the defence mechanism that costs each attacker the most time (chosen by
      rule from (c), never typed): the share of deployments followed by a
      compromised host within t of the deployment's completion, with the MTD and,
      at the same moments of the same seeds, with no MTD. Both attackers in each
      panel. The gap between an attacker's two curves, summed over the interval,
      is its time lost per MTD deployment.
  (c) time lost per MTD deployment for each defence mechanism deployed alone, both
      attackers, with 95 % bootstrap intervals over runs.
  Table: attack actions blocked per run and time lost per MTD deployment, per MTD
      mechanism, both attackers.

At the 2 000 s deployment interval. Nothing is typed.

Usage:
  python tools/ch5_disruption_figure.py [--numbers PATH] [--no-compile]

Writes docs/thesis/figures/fig_5-2-2a_disruption_response.{tex,pdf} and
docs/thesis/tables/tab_5-3-1b_disruption.tex
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (BASE_DASH, FONT, KEY_H, LABEL, LONG, PREAMBLE, REPO, axes, compile_fig,  # noqa: E402
                        errorbar, fmt_thousands, key_row, marker, panel_title, write_fig)
from ch5_effectiveness_figures import LAYER, PANEL_SINGLES, TICK  # noqa: E402

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "time_lost_numbers.json"
TABLE = REPO / "docs" / "thesis" / "tables" / "tab_5-3-1b_disruption.tex"
STEM = "fig_5-2-2a_disruption_response"
INTERVAL = 2000
ARMS = (("movement", "cmov", "circle"), ("baseline", "cbase", "square"))


def signed(v: float) -> str:
    return (r"$-$" + fmt_thousands(-v)) if v < 0 else fmt_thousands(v)


def emit(d: dict) -> tuple[str, list[str]]:
    C = d["cells"]
    tl = {(a, m): C[f"{a}|{m}|{INTERVAL}"] for a, _, _ in ARMS for m in PANEL_SINGLES}
    worst = {a: max(PANEL_SINGLES, key=lambda m: tl[(a, m)]["time_lost"]) for a, _, _ in ARMS}
    X0, X1 = 1.45, 15.2
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    facts: list[str] = []

    # ---- (a), (b): share of deployments followed by a compromise within t
    AY0, AH = 6.55, 3.7
    ay1 = AY0 + AH
    GAP = 0.9
    PW = (X1 - X0 - GAP) / 2
    for k, (arm_worst, letter) in enumerate((("movement", "a"), ("baseline", "b"))):
        m = worst[arm_worst]
        x0 = X0 + k * (PW + GAP)
        x1 = x0 + PW

        def xa(t, x0=x0, x1=x1):
            return x0 + t / INTERVAL * (x1 - x0)

        def ya(v):
            return AY0 + max(0.0, min(v, 1.0)) * AH

        axes(w, x0, x1, AY0, ay1,
             xticks=[(t, xa(t)) for t in range(0, INTERVAL + 1, 500)],
             yticks=[(v, ya(v / 100)) for v in (0, 25, 50, 75, 100)],
             xlabel="", ylabel="", ylabels=(k == 0),
             # (b)'s 0 label would run into (a)'s 2 000 across the gap: the tick stays
             xfmt=(lambda v, k=k: "" if (k == 1 and v == 0) else fmt_thousands(v)))
        head_top = panel_title(w, x0, ay1, LONG[m][:1].upper() + LONG[m][1:], letter)
        for arm, col, mk in ARMS:
            cv = tl[(arm, m)]["curves"]
            t, a, b = cv["t"], cv["with_mtd"], cv["no_mtd"]
            # the gap between the two curves is the time lost: shaded, drawn first
            poly = [(xa(x), ya(y)) for x, y in zip(t, b)] + [(xa(x), ya(y)) for x, y in reversed(list(zip(t, a)))]
            w(r"\fill[%s,opacity=%s] %s -- cycle;" % (col, "0.16" if arm == "movement" else "0.22",
                                                    " -- ".join("(%.3f,%.3f)" % p for p in poly)))
        for arm, col, mk in ARMS:
            cv = tl[(arm, m)]["curves"]
            dash = "," + BASE_DASH if arm == "baseline" else ""  # the chapter's contract: the baseline is dashed grey
            for series, shade in (("no_mtd", "!45"), ("with_mtd", "")):
                pts = [(xa(x), ya(y)) for x, y in zip(cv["t"], cv[series])]
                w(r"\draw[%s%s,line width=%s%s] %s;" % (col, shade, "0.8pt" if shade == "" else "0.6pt", dash,
                                                      " -- ".join("(%.3f,%.3f)" % p for p in pts)))
                if shade == "":
                    for x, y in pts[::10][1:]:
                        marker(w, mk, col, x, y, r=0.06)
            at = {x: (p, q) for x, p, q in zip(cv["t"], cv["with_mtd"], cv["no_mtd"])}
            facts.append(f"({letter}) {LONG[m]:18s} {arm:9s} deployments {tl[(arm, m)]['deployments']:5d}  followed by a compromise "
                         + "  ".join(f"within {int(x)} s {100 * at[x][0]:.0f} % vs {100 * at[x][1]:.0f} %" for x in (250.0, 500.0, 1000.0, 2000.0) if x in at))
    w(r"\node[anchor=north] at (%.3f,%.3f) {Time since the MTD deployment completed (s)};" % ((X0 + X1) / 2, AY0 - 0.42))
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {Deployments followed by\\a compromise (\%%)};" % (X0 - 0.85, (AY0 + ay1) / 2))

    # ---- (c) time lost per deployment, per mechanism ------------------------
    BY0, BH = 1.55, 2.9
    by1 = BY0 + BH
    lo_v = min(v["time_lost_ci95"][0] for v in tl.values())
    hi_v = max(v["time_lost_ci95"][1] for v in tl.values())
    YB0 = -200.0 * (int(-lo_v // 200) + 1) if lo_v < 0 else 0.0
    YB1 = 200.0 * (int(hi_v // 200) + 1)

    def yb(v):
        return BY0 + (max(YB0, min(YB1, v)) - YB0) / (YB1 - YB0) * BH

    slot = (X1 - X0) / len(PANEL_SINGLES)
    bw = 0.34
    xt = [(m, X0 + (i + 0.5) * slot) for i, m in enumerate(PANEL_SINGLES)]
    axes(w, X0, X1, BY0, by1,
         xticks=[(TICK[m], x) for m, x in xt],
         yticks=[(v, yb(v)) for v in range(int(YB0), int(YB1) + 1, 200)],
         xlabel="", ylabel="", xfmt=lambda v: v, yfmt=signed)
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {Time lost per\\MTD deployment (s)};" % (X0 - 0.85, (BY0 + by1) / 2))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, yb(0), X1, yb(0)))
    panel_title(w, X0, by1, "Time lost per MTD deployment, by defence mechanism", "c")
    for m, x in xt:
        for j, (arm, col, _) in enumerate(ARMS):
            v = tl[(arm, m)]
            s_, lo, hi = v["time_lost"], v["time_lost_ci95"][0], v["time_lost_ci95"][1]
            xl = x - bw + j * bw
            top, bot = yb(max(s_, 0)), yb(min(s_, 0))
            if arm == "movement":
                w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xl, bot, xl + bw - 0.03, top))
            else:
                w(r"\fill[pattern=north east lines,pattern color=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xl, bot, xl + bw - 0.03, top))
                w(r"\draw[%s,line width=0.3pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xl, bot, xl + bw - 0.03, top))
            if top - bot < 0.03:  # a value near zero: a stub at it, so it does not read as missing
                w(r"\draw[%s,line width=0.8pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, xl, yb(s_), xl + bw - 0.03, yb(s_)))
            errorbar(w, xl + (bw - 0.03) / 2, yb(lo), yb(hi), col="black!70", cap=0.035)
            facts.append(f"(c) {arm:9s} {m:18s} time lost {s_:5.0f} s [{lo:5.0f}, {hi:5.0f}]  "
                         f"wait {v['wait_with_mtd']:.0f} vs {v['wait_no_mtd']:.0f} s  blocked per run {v['blocked_per_run']['mean']:.2f}"
                         f"  dropped {v['dropped']}")
    ybk = BY0 - 1.35   # under three-line ticks
    i = 0
    while i < len(PANEL_SINGLES):
        j = i
        while j + 1 < len(PANEL_SINGLES) and LAYER[PANEL_SINGLES[j + 1]] == LAYER[PANEL_SINGLES[i]]:
            j += 1
        xa_, xb_ = X0 + i * slot + 0.12, X0 + (j + 1) * slot - 0.12
        w(r"\draw[black!50,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);" % (
            xa_, ybk + 0.08, xa_, ybk, xb_, ybk, xb_, ybk + 0.08))
        w(r"\node[anchor=north,text=black!60] at (%.3f,%.3f) {%s};" % ((xa_ + xb_) / 2, ybk - 0.03, LAYER[PANEL_SINGLES[i]]))
        i = j + 1

    # ---- the figure-wide key at the top (conventions §o): every panel shares it
    key_row(w, X0, head_top + 0.1 + KEY_H / 2,
            [(LABEL["movement"], "bar+line", "cmov", "circle"),
             (LABEL["baseline"], "hatch+dashed", "cbase", "square"),
             ("with no MTD", "line", "black!40", None)], xmax=X1)
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    facts.insert(0, "worst mechanism by rule (largest time lost): " + ", ".join(f"{a} -> {m}" for a, m in worst.items()))
    return "\n".join(L) + "\n", facts


def emit_table(d: dict) -> str:
    C = d["cells"]
    order = sorted(PANEL_SINGLES, key=lambda m: -C[f"movement|{m}|{INTERVAL}"]["time_lost"])

    def tl(c):
        v = "%d" % round(c["time_lost"])
        v = ("$-$" + v[1:]) if v.startswith("-") else v
        lo, hi = ("%d" % round(x) for x in c["time_lost_ci95"])
        lo = ("$-$" + lo[1:]) if lo.startswith("-") else lo
        hi = ("$-$" + hi[1:]) if hi.startswith("-") else hi
        return r"%s [%s, %s]" % (v, lo, hi)

    def bl(c):
        return r"$%.2f \pm %.2f$" % (c["blocked_per_run"]["mean"], c["blocked_per_run"]["ci95"])

    L = [
        "% GENERATED by tools/ch5_disruption_figure.py from data/results/ch5_defended/time_lost_numbers.json",
        "% (time_lost.py). Do not hand-edit; regenerate. 2026-09-30, the disruption metrics of Section 4.5.3.",
        "% DRAFT STATE --- ratify on read.",
        r"\begin{table}[tp]",
        r"  \centering",
        r"  \caption[What each defence mechanism costs each attacker]{Attack actions blocked per run and time lost per MTD deployment (Section~\ref{subsec:metrics-effectiveness}) for each defence mechanism deployed alone at the 2\,000\,s deployment interval, for the APT attacker model averaged over its four attack profiles and for the baseline attacker, ordered by the APT attacker model's time lost. Blocked: mean with a 95\,\% interval; time lost: brackets are a 95\,\% bootstrap interval over runs.}",
        r"  \label{tab:disruption}",
        r"  \tablestyle",
        r"  \begin{tabular}{@{}lcccc@{}}",
        r"    \toprule",
        r"    & \multicolumn{2}{c}{APT attacker model} & \multicolumn{2}{c}{Baseline attacker} \\",
        r"    \cmidrule(lr){2-3}\cmidrule(lr){4-5}",
        r"    Defence mechanism & Blocked per run & Time lost (s) & Blocked per run & Time lost (s) \\",
        r"    \midrule",
    ]
    for m in order:
        a, b = C[f"movement|{m}|{INTERVAL}"], C[f"baseline|{m}|{INTERVAL}"]
        L.append(r"    %s & %s & %s & %s & %s \\" % (LONG[m], bl(a), tl(a), bl(b), tl(b)))
    L += [r"    \bottomrule", r"  \end{tabular}", r"\end{table}", ""]
    return "\n".join(L)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    d = json.loads(args.numbers.read_text(encoding="utf-8"))
    tex, facts = emit(d)
    write_fig(STEM, tex.splitlines())
    TABLE.write_text(emit_table(d))
    print(f"wrote {TABLE.relative_to(REPO)}")
    print(f"caption and body facts, Fig. 5.3 (§5.3.1), drawn at {INTERVAL} s:")
    for f in facts:
        print("  " + f)
    for a, _, _ in ARMS:
        print(f"  body: {a:9s} no MTD, attack actions blocked per run 0 (structural); runs {d['cells'][a + '|none']['runs']}")
    print("  at 200 s (body sentence): time lost is capped at the 200 s to the next deployment:")
    for a, _, _ in ARMS:
        for m in ("ip_shuffle", "service_diversity"):
            c = d["cells"][f"{a}|{m}|200"]
            print(f"    {a:9s} {m:18s} time lost {c['time_lost']:.0f} s, wait {c['wait_with_mtd']:.0f} vs {c['wait_no_mtd']:.0f} s")
    if not args.no_compile:
        compile_fig(STEM)


if __name__ == "__main__":
    main()
