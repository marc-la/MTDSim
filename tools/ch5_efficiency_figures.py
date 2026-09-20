#!/usr/bin/env python3
"""Chapter 5 §5.5 floats from the defended corpus.

  Fig. 5.7  the frontier: attacker-side suppression against defender-side
            reconfiguration occupancy, one labelled marker per condition,
            marker shape = attacker arm; two lettered panels, one per
            interval, sharing the y axis
  Fig. 5.8  where the attacker model's time goes under each condition:
            stacked bars of the share of elapsed time on activity that
            completed, activity a deployment cut short, and the imposed delay,
            values printed in the segments; one panel per interval
  Tab. 5.8  cost by condition and attacker: actions and successes per host
            reached (event-wise, both arms), reconfiguration occupancy and
            (deployments per 1 000 s dropped 2026-09-20: it is one over the declared
            interval on every defended condition; handoff s52 critique §AK8)

Data: ``data/results/ch5_defended/numbers.json`` §s55 (design:
docs/handoffs/2026-09-17_ch5_s532_s55_defended_runs.md; read:
docs/implementation/pipeline/ogasp/ch5_s55_efficiency_findings.md). Nothing is
typed here.

Usage:
  python tools/ch5_efficiency_figures.py [--numbers PATH] [--no-compile] [--only STEM]

Writes
  docs/thesis/figures/fig_5-4a_frontier.{tex,pdf}
  docs/thesis/figures/fig_5-4b_time_split.{tex,pdf}
  docs/thesis/tables/tab_5-4a_cost.tex
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (DEFENDED, FONT, LABEL, LONG, PREAMBLE, REPO, SHORT, TAB_DIR,  # noqa: E402
                        axes, compile_fig, errorbar, fmt_thousands, marker, panel_letter, pm, write_fig)

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers.json"
STEM_F57 = "fig_5-4a_frontier"
STEM_F58 = "fig_5-4b_time_split"
STEM_T58 = "tab_5-4a_cost"
INTERVALS = ("200", "2000")
ARMS = (("baseline", "cbase", "square"), ("movement", "cmov", "circle"))


def _spread(ys: list[float], gap: float, lo: float, hi: float) -> list[float]:
    """Push label centres apart to at least ``gap`` (cm), keeping their order
    and staying inside [lo, hi]; the input order is by y ascending."""
    out = list(ys)
    for i in range(1, len(out)):
        if out[i] - out[i - 1] < gap:
            out[i] = out[i - 1] + gap
    if out and out[-1] > hi:
        shift = out[-1] - hi
        out = [y - shift for y in out]
        for i in range(len(out) - 2, -1, -1):
            if out[i + 1] - out[i] < gap:
                out[i] = out[i + 1] - gap
    if out and out[0] < lo:
        out = [y + (lo - out[0]) for y in out]
    return out


def emit_fig57(s55: dict) -> tuple[str, list]:
    """The frontier. The x range is per panel because the tempo sets the
    occupancy (0.35–0.55 at 200 s, 0.01–0.06 at 2 000 s); the y axis is
    shared. Model labels sit to the right of their marker and baseline labels
    to the left, spread apart within each side so no two collide, with a
    leader where a label had to move."""
    pts = {i: s55["by_interval"][i]["frontier"] for i in INTERVALS}
    XMAX = {}
    for i in INTERVALS:
        m = max(p["occupancy"]["mean"] + p["occupancy"]["ci95"] for p in pts[i].values())
        XMAX[i] = next(v for v in (0.05, 0.08, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0) if v >= m * 1.05)
    ys = [p["suppression"][k] for i in INTERVALS for p in pts[i].values() for k in ("lo", "hi")]
    ymin = -0.4 if min(ys) < -0.2 else (-0.2 if min(ys) < 0 else 0.0)
    ymax = 1.0
    PW, PH = 6.4, 6.2
    X0 = (1.35, 9.05)   # packs to 15.6 cm; 6.5 / 9.15 was 0.7 pt overfull
    Y0 = 0.95
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    facts = []
    for k, interval in enumerate(INTERVALS):
        x0, y0 = X0[k], Y0
        x1, y1 = x0 + PW, y0 + PH
        xmax = XMAX[interval]

        def xv(v):
            return x0 + v / xmax * PW

        def yv(v):
            return y0 + (v - ymin) / (ymax - ymin) * PH

        step = 0.1 if xmax >= 0.4 else 0.02
        xt = [round(j * step, 2) for j in range(int(round(xmax / step)) + 1)]
        yt = [round(v, 2) for v in [ymin + j * 0.2 for j in range(int(round((ymax - ymin) / 0.2)) + 1)]]
        axes(w, x0, x1, y0, y1, xticks=[(v, xv(v)) for v in xt], yticks=[(v, yv(v)) for v in yt],
             xlabel="share of the run under reconfiguration", ylabel=("suppression of hosts reached" if k == 0 else ""),
             ylabels=(k == 0), xfmt=lambda v: f"{v:.2f}" if xmax < 0.4 else f"{v:.1f}", yfmt=lambda v: f"{v:.1f}")
        if ymin < 0:
            w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, yv(0), x1, yv(0)))
        panel_letter(w, x0 - (1.2 if k == 0 else 0.5), y1 + 0.02, "ab"[k])
        w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {every %s\,s};" % (x0 + 0.05, y1 + 0.04, fmt_thousands(int(interval))))
        for arm, cname, mk in ARMS:
            rows = []
            for c in DEFENDED:
                p = pts[interval][f"{arm}|{c}"]
                x, y = p["occupancy"]["mean"], p["suppression"]["point"]
                w(r"\draw[%s!70,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (
                    cname, xv(max(0, x - p["occupancy"]["ci95"])), yv(y), xv(min(xmax, x + p["occupancy"]["ci95"])), yv(y)))
                w(r"\draw[%s!70,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (
                    cname, xv(x), yv(max(ymin, p["suppression"]["lo"])), xv(x), yv(min(ymax, p["suppression"]["hi"]))))
                marker(w, mk, cname, xv(x), yv(y), r=0.085)
                rows.append((yv(y), xv(x), c))
                facts.append((interval, arm, c, x, y))
            rows.sort()
            lab_y = _spread([r[0] for r in rows], 0.34, y0 + 0.15, y1 - 0.15)
            right = arm == "movement"
            for (my, mx, c), ly in zip(rows, lab_y):
                lx = mx + (0.16 if right else -0.16)
                if abs(ly - my) > 0.06:
                    w(r"\draw[%s!50,line width=0.25pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (cname, mx, my, lx, ly))
                w(r"\node[anchor=%s,text=%s,font=\scriptsize] at (%.3f,%.3f) {%s};" % (
                    "west" if right else "east", cname, lx, ly, SHORT[c]))
    # key, once, below the panels
    ky = Y0 - 1.05
    for j, (arm, cname, mk) in enumerate(ARMS):
        kx = X0[0] + j * 4.2
        marker(w, mk, cname, kx + 0.1, ky, r=0.085)
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (kx + 0.3, ky, LABEL[arm]))
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {whiskers: 95\,\%% intervals on both axes; label left of a marker: baseline attacker, right: movement attacker};" % (X0[0], ky - 0.4))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n", facts


def emit_fig58(s55: dict) -> tuple[str, list]:
    conds = ("none",) + DEFENDED
    PW, PH = 6.9, 4.0
    X0 = (1.35, 8.75)
    Y0 = 1.25
    segs = (("activity_completed", "cmov", "white", "activity that completed"),
            ("activity_cut_short", "cmov!35", "black", "activity a deployment cut short"),
            ("imposed_delay", "cbase!80", "white", "delay a deployment imposed"))
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    facts = []
    for k, interval in enumerate(INTERVALS):
        ts = s55["by_interval"][interval]["time_split"]
        x0, y0 = X0[k], Y0
        x1, y1 = x0 + PW, y0 + PH
        slot = PW / len(conds)
        bw = slot * 0.7
        xt = [(c, x0 + (i + 0.5) * slot) for i, c in enumerate(conds)]
        axes(w, x0, x1, y0, y1, xticks=[(SHORT[c], x) for c, x in xt],
             yticks=[(v, y0 + v * PH) for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0)],
             xlabel="", ylabel=("share of elapsed time" if k == 0 else ""), ylabels=(k == 0),
             xfmt=lambda v: v, yfmt=lambda v: f"{v:.1f}", xtick_rotate=45, grid=False)
        panel_letter(w, x0 - (1.2 if k == 0 else 0.5), y1 + 0.02, "ab"[k])
        w(r"\node[anchor=south,text=black!60] at (%.3f,%.3f) {every %s\,s};" % ((x0 + x1) / 2, y1 + 0.05, fmt_thousands(int(interval))))
        for c, x in xt:
            base = 0.0
            for key, fill, txt, _ in segs:
                v = ts[c][key]["mean"]
                w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fill, x - bw / 2, y0 + base * PH, x + bw / 2, y0 + (base + v) * PH))
                if v >= 0.045:
                    w(r"\node[text=%s,font=\scriptsize] at (%.3f,%.3f) {%.2f};" % (txt, x, y0 + (base + v / 2) * PH, v))
                base += v
                facts.append((interval, c, key, v))
    # key, once, under the 45-degree tick labels (they reach 1.2 cm below the axis)
    ky = Y0 - 1.55
    xx = X0[0]
    for key, fill, _, text in segs:
        w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (fill, xx, ky - 0.11))
        w(r"\draw[black!30,line width=0.2pt] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (xx, ky - 0.11))
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (xx + 0.4, ky, text))
        xx += 0.4 + 0.135 * len(text) + 0.7
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n", facts


def _ratio(v, ci, nd=1) -> str:
    if v is None:
        return "---"
    return "$%.*f$ [%.*f, %.*f]" % (nd, v, nd, ci[0], nd, ci[1])


def emit_tab58(s55: dict) -> str:
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_efficiency_figures.py from")
    w("%   data/results/ch5_defended/numbers.json §s55 (the defended corpus at 200 s;")
    w("%   the model pooled over its four profiles). Do not hand-edit; regenerate.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[The cost of each condition, on both sides]{The attacker's effort per host it manages to reach, and the defender's reconfiguration burden, for each condition and each attacker at the inherited interval. The attacker-side columns are counts of events rather than durations, which is what makes them comparable across two attackers that price time differently; the defender-side columns are derived from the simulator's own record of when each deployment was executing and are priced identically on both arms. The intention is to report both sides of the exchange on one page, and to state plainly which quantities may be compared across attackers and which may not.}")
    w(r"  \label{tab:eff-cost}")
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"  \begin{tabular}{@{}cP{3.4cm}>{\centering\arraybackslash}p{3.2cm}>{\centering\arraybackslash}p{3.2cm}>{\centering\arraybackslash}p{2.6cm}@{}}")
    w(r"    \toprule")
    w(r"    & Condition & Actions per host reached & Successes per host reached & Share of run under reconfiguration \\")
    w(r"    \midrule")
    cost = s55["by_interval"]["200"]["cost"]
    conds = ("none",) + DEFENDED
    for arm in ("baseline", "movement"):
        for i, c in enumerate(conds):
            d = cost[f"{arm}|{c}"]
            # \rowgroup's \multirow centres a ten-row label about 0.55 cm too
            # high on single-line \scriptsize rows, so the label is set here with
            # multirow's vertical fixup rather than through the macro
            group = (r"\multirow{-%d}{*}[-0.55cm]{\smash{\rotatebox{90}{\emph{%s}}}}" % (len(conds), LABEL[arm])
                     if i == len(conds) - 1 else "")
            w("    %s & %s & %s & %s & %s \\\\" % (
                group, LONG[c],
                _ratio(d["actions_per_host_celltotal"], d["actions_per_host_celltotal_ci"]),
                _ratio(d["successes_per_host_celltotal"], d["successes_per_host_celltotal_ci"]),
                pm(d["occupancy"], 2)))
        w(r"    \midrule" if arm == "baseline" else r"    \bottomrule")
    w(r"    \addlinespace[2pt]")
    w(r"    \multicolumn{5}{@{}p{0.96\textwidth}@{}}{\scriptsize Actions and successes per host are cell totals (all attempted actions, or all successes, over all hosts reached in the 100 runs, or 400 for the pooled model) with a seeded bootstrap interval, so a run that reaches one host does not dominate; a success is a verdict of success on the model and a compromise event on the baseline attacker, whose record carries no other verdict. The reconfiguration share is the union of the deployment windows over the run's elapsed time, mean $\pm$ 95\,\% interval. Time-denominated attacker-side quantities are not comparable across arms and are not in this table.}\\")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--only", default=None, help="fig57 | fig58 | tab58")
    args = ap.parse_args()
    data = json.loads(args.numbers.read_text(encoding="utf-8"))
    if not data["sanity"]["all_cells_100"] or data["sanity"]["error_rows"]:
        raise SystemExit("corpus sanity failed; not drawing from it")
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    want = lambda k: args.only is None or args.only == k  # noqa: E731
    s55 = data["s55"]
    if want("fig57"):
        tex, facts = emit_fig57(s55)
        write_fig(STEM_F57, tex.splitlines())
        print("Fig. 5.7 facts (interval, arm, condition, occupancy, suppression):")
        for f in facts:
            print("   %s %-10s %-18s %.3f %+.3f" % f)
        for i in INTERVALS:
            b = s55["by_interval"][i]
            print(f"   spearman(occupancy, suppression) @ {i}: movement {b['spearman_occupancy_suppression_movement']:.2f}, "
                  f"baseline {b['spearman_occupancy_suppression_baseline']:.2f}")
        if not args.no_compile:
            compile_fig(STEM_F57)
    if want("fig58"):
        tex, facts = emit_fig58(s55)
        write_fig(STEM_F58, tex.splitlines())
        print("Fig. 5.8 facts (interval, condition, segment, share):")
        for f in facts:
            print("   %s %-18s %-20s %.3f" % f)
        if not args.no_compile:
            compile_fig(STEM_F58)
    if want("tab58"):
        (TAB_DIR / f"{STEM_T58}.tex").write_text(emit_tab58(s55))
        print(f"wrote tables/{STEM_T58}.tex")


if __name__ == "__main__":
    main()
