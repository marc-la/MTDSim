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
from _ch5_style import (BASE_DASH, IV_BOOT, bounded, FONT, LABEL, LONG, PREAMBLE, REPO, axes, compile_fig,  # noqa: E402
                        errorbar, fmt_thousands, key_below, marker, panel_title, write_fig)
from ch5_effectiveness_figures import LAYER, PANEL_SINGLES, TICK  # noqa: E402

# the reported corpus (1 000 seeds, the vulnerability memory on; 2026-10-02)
NUMBERS = REPO / "data" / "results" / "ch5_defended" / "time_lost_numbers_reported.json"
TABLE = REPO / "docs" / "thesis" / "tables" / "tab_5-3-1b_disruption.tex"
STEM = "fig_5-2-2a_disruption_response"
INTERVAL = 2000
# the series contract (conventions §o rule 5; Marc 2026-10-05): the APT attacker
# model pooled is black, the baseline attacker a solid grey bar, as every figure
ARMS = (("movement", "black", "circle"), ("baseline", "cbase", "square"))


def signed(v: float) -> str:
    return (r"$-$" + fmt_thousands(-v)) if v < 0 else fmt_thousands(v)


def _bars(w, tl, X0, X1, BY0, BH, key: str, lohi, *, step: float, fmt, ylabel: str, facts: list[str], tag: str) -> None:
    """One panel of paired bars per mechanism (the APT attacker model black, the
    baseline attacker grey), 95 % whiskers, zero line; ``key`` reads the value
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
            w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xl, bot, xl + bw - 0.03, top))
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
          step=0.25, fmt=lambda v: ("%.2f" % v).rstrip("0").rstrip("."), ylabel=r"Attack actions blocked",
          facts=facts, tag="a")
    panel_title(w, X0, AY0 + BH, "Attack actions blocked per MTD deployment", "a")
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

    # ---- the figure's one key, at its foot, under the layer brackets (conventions §o)
    key_below(w, X0, ybk - 0.03 - 0.40,
              [(LABEL["movement"], "bar", "black", None),
               (LABEL["baseline"], "bar", "cbase", None)], xmax=X1)
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


# The two metrics' reading, shared by Table 5.3 and Figure 5.2's caption (standard
# T1, T2, N3; Marc 2026-10-02: the captions alone should explain the float). The
# layer clause is the simulator's disruption rule (mtd_operation._interrupt_adversary;
# Section 2.2 states it): a deployment's layer and the attacker's current action
# decide a disruption, never the mechanism, so a layer's mechanisms block nearly
# the same share by construction.
DECODE_BLOCKED = (r"Attack actions blocked per MTD deployment is 1 when every deployment disrupts an attack "
                  r"action and 0 when none does; a deployment's layer, not its mechanism, decides which attack "
                  r"actions it can disrupt (Section~\ref{subsec:attacker-model}), so the mechanisms of one layer "
                  r"block nearly the same share.")


def decode_time_lost(C: dict) -> str:
    """Time lost's reading, with the smallest share of deployments it is taken over (N3)."""
    kept = min(c["deployments"] / (c["deployments"] + c["dropped"])
               for k, c in C.items() if k.endswith("|%s" % INTERVAL) and "deployments" in c)
    return (r"Time lost per MTD deployment is the delay to the attacker's next compromise against the same "
            r"seed with no MTD; below zero, the next compromise came sooner. It is taken over the deployments "
            r"that complete while the same seed's run with no MTD is still going, at least %d\,\%% of each "
            r"cell's." % int(100 * kept))


def _place(hw: float) -> int:
    """The precision rule (Marc 2026-09-30): the place of a half-width's first
    significant figure (the second when that figure is a 1)."""
    import math
    place = math.floor(math.log10(hw)) if hw > 0 else 0
    if hw > 0 and int(round(hw / 10.0 ** place, 6)) == 1:
        place -= 1
    return place


def emit_table(d: dict) -> str:
    """Table 5.3: the two metrics of Figure 5.2 with their intervals, rows in the
    figure's order and grouped by layer as its brackets are (2026-09-30)."""
    C = d["cells"]

    # the precision rule (standard P1), per column: each value to the place of its
    # column's widest interval's half-width (Cole 2015); a true minus in math mode
    cells = {arm: [C[f"{arm}|{m}|{INTERVAL}"] for m in PANEL_SINGLES] for arm in ("movement", "baseline")}
    tl_place = {arm: _place(max((c["time_lost_ci95"][1] - c["time_lost_ci95"][0]) / 2 for c in cs))
                for arm, cs in cells.items()}
    # a bound that rounds to 0 without being 0 hides whether the interval includes
    # zero; such a column goes one place finer (standard P2)
    for arm, cs in cells.items():
        q = 10.0 ** tl_place[arm]
        if any(b != 0 and round(b / q) == 0 for c in cs for b in c["time_lost_ci95"]):
            tl_place[arm] -= 1
    bl_place = {arm: _place(max((c["blocked_per_deployment"]["hi"] - c["blocked_per_deployment"]["lo"]) / 2 for c in cs))
                for arm, cs in cells.items()}

    def num(v, place):
        nd = max(0, -place)
        t = "%.*f" % (nd, round(v / 10.0 ** place) * 10.0 ** place)
        return "$0$" if float(t) == 0 else "$%s$" % t

    def tl(c, arm):
        lo, hi = c["time_lost_ci95"]
        pl = tl_place[arm]
        return r"%s [%s, %s]" % (num(c["time_lost"], pl), num(lo, pl), num(hi, pl))

    def bl(c, arm):
        b = c["blocked_per_deployment"]
        # a share of deployments, bounded by 0 and 1, never prints a bound it does not reach (P2)
        nd = max(0, -bl_place[arm])
        f = lambda v: bounded(v, nd, lo=0.0, hi=1.0)
        return r"%s [%s, %s]" % (f(b["point"]), f(b["lo"]), f(b["hi"]))

    runs = {arm: C[f"{arm}|{PANEL_SINGLES[0]}|{INTERVAL}"]["runs"] for arm in ("movement", "baseline")}
    # a printed 1.00 is said to be exact, when the table has one (P2)
    EXACT = (" A printed %s is exact." % ("1." + "0" * max(0, -min(bl_place.values())))) if any(c["blocked_per_deployment"]["point"] == 1.0
                                              for cs in cells.values() for c in cs) else ""
    L = [
        "% GENERATED by tools/ch5_disruption_figure.py from " + str(NUMBERS.relative_to(REPO)),
        "% (time_lost.py). Do not hand-edit; regenerate. 2026-09-30, the disruption metrics of Section 4.5.3;",
        "% headers are the metrics' names as Table 4.3 gives them; rows as Figure 5.2 orders them.",
        "% DRAFT STATE --- ratify on read.",
        r"\begin{table}[tp]",
        r"  \centering",
        r"  \caption[What each MTD mechanism costs each attacker]{What an MTD deployment costs each attacker: each MTD mechanism deployed alone every 2\,000\,s, against the APT attacker model, its attack profiles $c_1$ to $c_4$ combined, and against the baseline attacker, in the order of Figure~\ref{fig:aio-adaptivity} (metrics in Section~\ref{subsec:metrics-effectiveness}). " + DECODE_BLOCKED + " " + decode_time_lost(C) + " Each cell is over %s runs for the APT attacker model (1\\,000 per attack profile) and %s for the baseline attacker. Brackets: a %s; each column is rounded to the precision of its widest interval, or one place finer where an interval bound would otherwise round to 0.%s}" % (fmt_thousands(runs["movement"]), fmt_thousands(runs["baseline"]), IV_BOOT, EXACT),
        r"  \label{tab:disruption}",
        # scriptsize, 3 pt gaps: at footnotesize the 3-decimal brackets exceed the text width (conventions, "Table size")
        r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}",  # group rows keep the stripes (Marc, 2026-10-01)
        r"  \begin{tabular}{@{}P{3.8cm}*{2}{>{\centering\arraybackslash}p{3.0cm}>{\centering\arraybackslash}p{2.4cm}}@{}}",
        r"    \toprule",
        r"    & \multicolumn{2}{c}{APT attacker model} & \multicolumn{2}{c}{Baseline attacker} \\",
        r"    \cmidrule(lr){2-3}\cmidrule(lr){4-5}",
        # the metrics' names, verbatim from Table 4.3 (Marc 2026-09-30: "blocked per run ... I don't recognise")
        r"    \rowcolor{white}MTD mechanism & Attack actions blocked per MTD deployment & Time lost per MTD deployment (s) & Attack actions blocked per MTD deployment & Time lost per MTD deployment (s) \\",
    ]
    layer = None
    for m in PANEL_SINGLES:
        if LAYER[m] != layer:
            layer = LAYER[m]
            L.append(r"    \midrule")
            L.append(r"    \grouprow{5}{%s} \\" % layer)
        a, b = C[f"movement|{m}|{INTERVAL}"], C[f"baseline|{m}|{INTERVAL}"]
        L.append(r"    \quad %s & %s & %s & %s & %s \\" % (LONG[m], bl(a, "movement"), tl(a, "movement"),
                                                     bl(b, "baseline"), tl(b, "baseline")))
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
