#!/usr/bin/env python3
"""Chapter 5 §5.3.1's floats: Figure 5.3, what an MTD deployment costs each
attacker, and Table 5.x beside it.

REBUILT 2026-09-30 on the metrics Section 4.5.3 now defines (Marc's rulings;
record docs/implementation/disruption_mechanism.md; handoff
docs/handoffs/2026-09-30_disruption_metrics.md). The compromise rate after an MTD
deployment is retired with its reader, disruption.py; time_lost.py is the reader.

  (a) attack actions blocked per run and (b) time lost per MTD deployment, for
      each MTD mechanism deployed alone, both attackers, on one mechanism axis
      (2026-09-30, Marc: the former (a), (b), the share of deployments followed by
      a compromise within t, is no metric of Table 4.3, so it went).
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
import math
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (BASE_DASH, FONT, KEY_H, LABEL, LONG, PREAMBLE, REPO, axes, compile_fig,  # noqa: E402
                        errorbar, fmt_thousands, key_row, marker, panel_title, write_fig)
from ch5_effectiveness_figures import LAYER, PANEL_SINGLES, TICK  # noqa: E402

# the reported corpus (1 000 seeds, the vulnerability memory on; 2026-10-02)
NUMBERS = REPO / "data" / "results" / "ch5_defended" / "time_lost_numbers_reported.json"
TABLE = REPO / "docs" / "thesis" / "tables" / "tab_5-3-1b_disruption.tex"
STEM = "fig_5-2-2a_disruption_response"
INTERVAL = 2000
ARMS = (("movement", "cmov", "circle"), ("baseline", "cbase", "square"))


def signed(v: float) -> str:
    return (r"$-$" + fmt_thousands(-v)) if v < 0 else fmt_thousands(v)


def _bars(w, tl, X0, X1, BY0, BH, key: str, lohi, *, step: float, fmt, ylabel: str, facts: list[str], tag: str) -> None:
    """One panel of paired bars per mechanism (the APT attacker model solid, the
    baseline attacker hatched), 95 % whiskers, zero line; ``key`` reads the value
    and ``lohi`` its interval from a cell."""
    by1 = BY0 + BH
    lo_v = min(lohi(v)[0] for v in tl.values())
    hi_v = max(lohi(v)[1] for v in tl.values())
    Y0 = -step * (int(-lo_v // step) + 1) if lo_v < 0 else 0.0
    Y1 = step * math.ceil(round(hi_v / step, 6))  # no empty tick above the data (a count per deployment tops at 1)

    def yb(v):
        return BY0 + (max(Y0, min(Y1, v)) - Y0) / (Y1 - Y0) * BH

    slot = (X1 - X0) / len(PANEL_SINGLES)
    bw = 0.34
    xt = [(m, X0 + (i + 0.5) * slot) for i, m in enumerate(PANEL_SINGLES)]
    n = int(round((Y1 - Y0) / step))
    axes(w, X0, X1, BY0, by1,
         xticks=[("", x) for _, x in xt],
         yticks=[(Y0 + k * step, yb(Y0 + k * step)) for k in range(n + 1)],
         xlabel="", ylabel="", xfmt=lambda v: v, yfmt=fmt)
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {%s};" % (X0 - 0.85, (BY0 + by1) / 2, ylabel))
    if Y0 < 0:
        w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, yb(0), X1, yb(0)))
    for m, x in xt:
        for j, (arm, col, _) in enumerate(ARMS):
            v = tl[(arm, m)]
            s_, (lo, hi) = key(v), lohi(v)
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
            facts.append(f"({tag}) {arm:9s} {m:18s} {s_:8.2f} [{lo:8.2f}, {hi:8.2f}]")


def emit(d: dict) -> tuple[str, list[str]]:
    """Figure 5.3 (rebuilt 2026-09-30 on Marc's read: the share of deployments
    followed by a compromise is no metric of Table 4.3, so its two panels go):
    (a) attack actions blocked and (b) time lost per MTD deployment, each for
    every MTD mechanism deployed alone, both attackers, on one mechanism axis."""
    C = d["cells"]
    tl = {(a, m): C[f"{a}|{m}|{INTERVAL}"] for a, _, _ in ARMS for m in PANEL_SINGLES}
    X0, X1 = 1.45, 16.0   # packs to the chapter's 15.7 cm (conventions §h)
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    facts: list[str] = []

    # ---- (a) attack actions blocked (top), (b) time lost (bottom) ----
    # (a) attack actions blocked per MTD deployment, the metric as section 4.5.3
    # defines it (Marc 2026-09-30: "we define these metrics ... then we present
    # something that doesn't even exist"); the same unit as (b)
    BY0, BH = 1.55, 3.0
    AY0 = BY0 + BH + 0.95
    _bars(w, tl, X0, X1, AY0, BH,
          key=lambda v: v["blocked_per_deployment"]["point"],
          lohi=lambda v: (v["blocked_per_deployment"]["lo"], v["blocked_per_deployment"]["hi"]),
          step=0.25, fmt=lambda v: ("%.2f" % v).rstrip("0").rstrip("."), ylabel=r"Actions blocked",
          facts=facts, tag="a")
    a_top = panel_title(w, X0, AY0 + BH, "Attack actions blocked per MTD deployment", "a")
    _bars(w, tl, X0, X1, BY0, BH,
          key=lambda v: v["time_lost"], lohi=lambda v: tuple(v["time_lost_ci95"]),
          step=200.0, fmt=signed, ylabel=r"Time lost (s)", facts=facts, tag="b")
    panel_title(w, X0, BY0 + BH, "Time lost per MTD deployment", "b")
    # the mechanism names once, under (b), with the layer brackets
    slot = (X1 - X0) / len(PANEL_SINGLES)
    for i, m in enumerate(PANEL_SINGLES):
        w(r"\node[anchor=north] at (%.3f,%.3f) {%s};" % (X0 + (i + 0.5) * slot, BY0 - 0.1, TICK[m]))
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

    # ---- the figure-wide key at the top (conventions §o): both panels share it
    key_row(w, X0, a_top + 0.1 + KEY_H / 2,
            [(LABEL["movement"], "bar", "cmov", None),
             (LABEL["baseline"], "hatch", "cbase", None)], xmax=X1)
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    for m in PANEL_SINGLES:
        for a, _, _ in ARMS:
            v = tl[(a, m)]
            facts.append(f"    {a:9s} {m:18s} wait {v['wait_with_mtd']:.0f} vs {v['wait_no_mtd']:.0f} s  dropped {v['dropped']}")
    return "\n".join(L) + "\n", facts


def _r10(x: float) -> str:
    """Whole tens of seconds: the precision rule (a value to the place of its
    interval's first significant figure; time lost's half-widths are 30-70 s)."""
    v = "%d" % (10 * round(x / 10))
    return ("$-$" + v[1:]) if v.startswith("-") else v


def emit_table(d: dict) -> str:
    """Table 5.3: the two metrics of Figure 5.2 with their intervals, rows in the
    figure's order and grouped by layer as its brackets are (2026-09-30)."""
    C = d["cells"]

    def tl(c):
        lo, hi = c["time_lost_ci95"]
        return r"%s [%s, %s]" % (_r10(c["time_lost"]), _r10(lo), _r10(hi))

    def bl(c):
        b = c["blocked_per_deployment"]
        return r"%.2f [%.2f, %.2f]" % (b["point"], b["lo"], b["hi"])

    L = [
        "% GENERATED by tools/ch5_disruption_figure.py from data/results/ch5_defended/time_lost_numbers.json",
        "% (time_lost.py). Do not hand-edit; regenerate. 2026-09-30, the disruption metrics of Section 4.5.3;",
        "% headers are the metrics' names as Table 4.3 gives them; rows as Figure 5.2 orders them.",
        "% DRAFT STATE --- ratify on read.",
        r"\begin{table}[tp]",
        r"  \centering",
        r"  \caption[What each MTD mechanism costs each attacker]{Attack actions blocked per MTD deployment and time lost per MTD deployment (Section~\ref{subsec:metrics-effectiveness}) for each MTD mechanism deployed alone at the 2\,000\,s deployment interval, for the APT attacker model averaged over its four attack profiles and for the baseline attacker, in the order of Figure~\ref{fig:aio-adaptivity}. Brackets are 95\,\% bootstrap intervals over runs.}",
        r"  \label{tab:disruption}",
        r"  \tablestyle\rowcolors{1}{}{}",  # the layer rows separate the rows; zebra would stripe them
        r"  \begin{tabular}{@{}P{4.4cm}*{4}{>{\centering\arraybackslash}p{2.55cm}}@{}}",
        r"    \toprule",
        r"    & \multicolumn{2}{c}{APT attacker model} & \multicolumn{2}{c}{Baseline attacker} \\",
        r"    \cmidrule(lr){2-3}\cmidrule(lr){4-5}",
        # the metrics' names, verbatim from Table 4.3 (Marc 2026-09-30: "blocked per run ... I don't recognise")
        r"    MTD mechanism & Attack actions blocked per MTD deployment & Time lost per MTD deployment (s) & Attack actions blocked per MTD deployment & Time lost per MTD deployment (s) \\",
    ]
    layer = None
    for m in PANEL_SINGLES:
        if LAYER[m] != layer:
            layer = LAYER[m]
            L.append(r"    \midrule")
            L.append(r"    \multicolumn{5}{@{}l}{\textit{%s}} \\" % layer)
        a, b = C[f"movement|{m}|{INTERVAL}"], C[f"baseline|{m}|{INTERVAL}"]
        L.append(r"    \quad %s & %s & %s & %s & %s \\" % (LONG[m], bl(a), tl(a), bl(b), tl(b)))
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
