#!/usr/bin/env python3
"""Chapter 5 §5.3.1 floats from the no-defence corpus: Figure 5.2 (campaign
coverage and opening variety), Figure 5.3 (pairwise divergence against its
split-half null) and Table 5.4 (behaviour without defence, by attacker).

Data: ``data/results/ch5_s531_unopposed/numbers.json``, the analyser's output
over the recorded corpus (design: docs/handoffs/2026-09-15_ch5_s531_unopposed_runs.md;
read: docs/implementation/pipeline/ogasp/ch5_s531_unopposed_findings.md).
Nothing is typed here: every plotted value, every table cell and every number a
caption may quote is read from that file and printed on stdout.

Usage:
  python tools/ch5_unopposed_figures.py [--numbers PATH] [--no-compile]

Writes
  docs/thesis/figures/fig_5-3-1a_coverage_openings.{tex,pdf}
  docs/thesis/figures/fig_5-3-1b_divergence.{tex,pdf}
  docs/thesis/tables/tab_5-3-1a_unopposed_summary.tex

Style (figure_table_conventions.md §f, §h, §k, §l): TikZ standalone at 12 pt,
Helvetica (helvet 0.92), packed to the page box (\\textwidth = 455.24 pt) and
included bare, so 10 pt in the tool is 10 pt on the page. Series encoding is
the chapter's contract: one hue and one marker per attack profile, held in every
figure from §5.3 on; the baseline attacker is a dashed grey line. The five hues
pass the dataviz six-check validator on the light surface (2026-09-15).
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIG_DIR = REPO / "docs" / "thesis" / "figures"
TAB_DIR = REPO / "docs" / "thesis" / "tables"
NUMBERS = REPO / "data" / "results" / "ch5_s531_unopposed" / "numbers.json"
STEM_A = "fig_5-3-1a_coverage_openings"
STEM_B = "fig_5-3-1b_divergence"
STEM_T = "tab_5-3-1a_unopposed_summary"

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
FOUR = PROFILES[:4]
# presentation names, mapped here and never read from the corpus (§g)
LABEL = {
    "objective_exfiltration": "exfiltration",
    "objective_impact": "impact",
    "objective_exfiltration_impact": "double extortion",
    "objective_none_c2": "no realised objective",
    "aggregate": "aggregate",
    "baseline": "baseline attacker",
}
COLOUR = {  # RGB; the chapter's series contract
    "objective_exfiltration": "31,84,140",
    "objective_impact": "179,38,30",
    "objective_exfiltration_impact": "168,116,26",
    "objective_none_c2": "111,78,156",
    "aggregate": "58,125,68",
    "baseline": "122,122,122",
}
CNAME = {
    "objective_exfiltration": "cexf",
    "objective_impact": "cimp",
    "objective_exfiltration_impact": "cdex",
    "objective_none_c2": "cnon",
    "aggregate": "cagg",
    "baseline": "cbase",
}
MARK = {
    "objective_exfiltration": "circle",
    "objective_impact": "square",
    "objective_exfiltration_impact": "triangle",
    "objective_none_c2": "diamond",
    "aggregate": "downtriangle",
}
TEXTWIDTH_CM = 455.24 / 28.45  # 16.0 cm, measured (thesis figure pipeline)
FONT = r"\footnotesize"  # 10 pt at natural size against the 12 pt body

PREAMBLE = [
    r"\documentclass[tikz,12pt,border=2pt]{standalone}",
    r"\usepackage[T1]{fontenc}",
    r"\usepackage[scaled=0.92]{helvet}",
    r"\renewcommand{\familydefault}{\sfdefault}",
    r"\usetikzlibrary{calc}",
] + [r"\definecolor{%s}{RGB}{%s}" % (CNAME[k], v) for k, v in COLOUR.items()] + [
    r"\begin{document}",
]


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


def axes(w, X0, X1, Y0, Y1, *, xticks, yticks, xlabel, ylabel, ylabels=True, xfmt=lambda v: f"{v:g}"):
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, Y0, X1, Y0))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, Y0, X0, Y1))
    for v, y in yticks:
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0 - 0.07, y, X0, y))
        if y > Y0 + 1e-6:
            w(r"\draw[black!12,line width=0.2pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, y, X1, y))
        if ylabels:
            w(r"\node[anchor=east] at (%.3f,%.3f) {%g};" % (X0 - 0.1, y, v))
    for v, x in xticks:
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, Y0, x, Y0 - 0.07))
        w(r"\node[anchor=north] at (%.3f,%.3f) {%s};" % (x, Y0 - 0.1, xfmt(v)))
    w(r"\node[anchor=north] at (%.3f,%.3f) {%s};" % ((X0 + X1) / 2, Y0 - 0.5, xlabel))
    if ylabel:
        w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {%s};" % (X0 - 0.85, (Y0 + Y1) / 2, ylabel))


def emit_fig_a(core: dict) -> tuple[str, dict]:
    cov = core["coverage"]
    openings = {p: core["table"][p]["distinct_openings"] for p in PROFILES}
    horizon = core["horizon"]
    zoom_to = 3000.0
    ymax_cov = 16.0
    kmax = max(int(k) for k in openings[PROFILES[0]])
    nseeds = core["table"][PROFILES[0]]["n"]

    # geometry (cm): two rows; (a) and (b) share the y axis
    H = 4.2
    XA0, XA1 = 1.35, 7.95
    XB0, XB1 = 8.95, 15.5
    YT0, YT1 = 6.15, 6.15 + H
    XC0, XC1 = 1.35, 7.95
    YB0, YB1 = 0.75, 0.75 + H
    KX0 = 9.4

    def ya(v):
        return YT0 + v / ymax_cov * H

    def xa(t):
        return XA0 + t / horizon * (XA1 - XA0)

    def xb(t):
        return XB0 + t / zoom_to * (XB1 - XB0)

    def yc(v):
        return YB0 + v / nseeds * H

    def xc(k):
        return XC0 + (k - 1) / (kmax - 1) * (XC1 - XC0)

    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    # panel (a): full horizon
    axes(w, XA0, XA1, YT0, YT1,
         xticks=[(t, xa(t)) for t in range(0, horizon + 1, 5000)],
         yticks=[(v, ya(v)) for v in range(0, int(ymax_cov) + 1, 4)],
         xlabel="simulated time (s)", ylabel="distinct tactics reached",
         xfmt=lambda v: f"{int(v):,}".replace(",", r"\,"))
    w(r"\node[anchor=south west,font=\footnotesize\bfseries] at (%.3f,%.3f) {(a)};" % (XA0 - 1.2, YT1 + 0.05))
    # panel (b): the zoom
    axes(w, XB0, XB1, YT0, YT1,
         xticks=[(t, xb(t)) for t in range(0, int(zoom_to) + 1, 1000)],
         yticks=[(v, ya(v)) for v in range(0, int(ymax_cov) + 1, 4)],
         xlabel="simulated time (s), the first %s" % f"{int(zoom_to):,}".replace(",", r"\,") + r"\,s",
         ylabel="", ylabels=False,
         xfmt=lambda v: f"{int(v):,}".replace(",", r"\,"))
    w(r"\node[anchor=south west,font=\footnotesize\bfseries] at (%.3f,%.3f) {(b)};" % (XB0 - 0.5, YT1 + 0.05))
    # zoom window marked on (a)
    w(r"\draw[black!30,line width=0.3pt,dash pattern=on 1pt off 1pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (xa(zoom_to), YT0, xa(zoom_to), YT1))

    for panel, xf, tmax, every in (("a", xa, horizon, 8), ("b", xb, zoom_to, 2)):
        # baseline first, so the profile lines sit on top
        c = cov["baseline"]
        pts = [(xf(t), ya(m)) for t, m in zip(c["t"], c["mean"]) if t <= tmax]
        w(r"\draw[cbase,line width=0.6pt,dash pattern=on 2.5pt off 1.5pt] %s;" % " -- ".join("(%.3f,%.3f)" % p for p in pts))
        for p in PROFILES:
            c = cov[p]
            sel = [(t, m, e) for t, m, e in zip(c["t"], c["mean"], c["ci95"]) if t <= tmax]
            band = [(xf(t), ya(m - e)) for t, m, e in sel] + [(xf(t), ya(m + e)) for t, m, e in reversed(sel)]
            w(r"\fill[%s,opacity=0.15] %s -- cycle;" % (CNAME[p], " -- ".join("(%.3f,%.3f)" % q for q in band)))
        for p in PROFILES:
            c = cov[p]
            sel = [(t, m) for t, m in zip(c["t"], c["mean"]) if t <= tmax]
            w(r"\draw[%s,line width=0.6pt] %s;" % (CNAME[p], " -- ".join("(%.3f,%.3f)" % (xf(t), ya(m)) for t, m in sel)))
            for i, (t, m) in enumerate(sel):
                if i % every == 0 and i > 0:
                    marker(w, MARK[p], CNAME[p], xf(t), ya(m))
    # panel (c): opening variety
    axes(w, XC0, XC1, YB0, YB1,
         xticks=[(k, xc(k)) for k in range(1, kmax + 1)],
         yticks=[(v, yc(v)) for v in range(0, nseeds + 1, 25)],
         xlabel="opening length $k$ (tactics)", ylabel="distinct openings, of %d runs" % nseeds)
    w(r"\node[anchor=south west,font=\footnotesize\bfseries] at (%.3f,%.3f) {(c)};" % (XC0 - 1.2, YB1 + 0.05))
    w(r"\draw[cbase,line width=0.6pt,dash pattern=on 2.5pt off 1.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (xc(1), yc(1), xc(kmax), yc(1)))
    for p in PROFILES:
        pts = [(xc(k), yc(openings[p][str(k)])) for k in range(1, kmax + 1)]
        w(r"\draw[%s,line width=0.6pt] %s;" % (CNAME[p], " -- ".join("(%.3f,%.3f)" % q for q in pts)))
        for x, y in pts:
            marker(w, MARK[p], CNAME[p], x, y)
    # key panel (once, hong2018's form), beside (c)
    ky = YB1 - 0.15
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {attack profile};" % (KX0, ky))
    ky -= 0.42
    for p in PROFILES:
        w(r"\draw[%s,line width=0.6pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (CNAME[p], KX0, ky, KX0 + 0.7, ky))
        marker(w, MARK[p], CNAME[p], KX0 + 0.35, ky)
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (KX0 + 0.85, ky, LABEL[p]))
        ky -= 0.42
    ky -= 0.1
    w(r"\draw[cbase,line width=0.6pt,dash pattern=on 2.5pt off 1.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (KX0, ky, KX0 + 0.7, ky))
    w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (KX0 + 0.85, ky, LABEL["baseline"]))
    ky -= 0.42
    w(r"\node[anchor=west,text=black!60,align=left] at (%.3f,%.3f) {shaded band: 95\,\%% interval on the mean};" % (KX0, ky))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")

    facts = {
        "baseline_activities": cov["baseline"]["mean"][-1],
        "coverage_final": {p: cov[p]["mean"][-1] for p in PROFILES},
        "openings_kmax": {p: openings[p][str(kmax)] for p in PROFILES},
        "kmax": kmax, "zoom_to": zoom_to, "nseeds": nseeds,
    }
    return "\n".join(L) + "\n", facts


def emit_fig_b(core: dict) -> tuple[str, dict]:
    div = core["divergence"]["visit_stream"]
    n = len(FOUR)
    cell = 2.35
    lab_w, lab_h = 2.9, 1.1
    vals = [[(div[f"{a}|{b}"]["null_ceiling"] if a == b else div[f"{a}|{b}"]["jsd"]) for b in FOUR] for a in FOUR]
    vmax = max(v for row in vals for v in row)
    two_line = {
        "objective_exfiltration": "exfiltration",
        "objective_impact": "impact",
        "objective_exfiltration_impact": r"double\\extortion",
        "objective_none_c2": r"no realised\\objective",
    }
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    for j, b in enumerate(FOUR):
        w(r"\node[anchor=south,align=center] at (%.3f,%.3f) {%s};" % (lab_w + (j + 0.5) * cell, n * cell + 0.12, two_line[b]))
    for i, a in enumerate(FOUR):
        y = (n - 1 - i) * cell
        w(r"\node[anchor=east,align=right] at (%.3f,%.3f) {%s};" % (lab_w - 0.15, y + cell / 2, two_line[a]))
        for j, b in enumerate(FOUR):
            x = lab_w + j * cell
            v = vals[i][j]
            if i == j:
                fill, txt, text = "white", "black!60", f"{v:.4f}"
            else:
                shade = int(round(8 + 62 * v / vmax))  # black!8 .. black!70
                fill, text = f"black!{shade}", f"{v:.3f}"
                txt = "white" if shade >= 45 else "black"
            w(r"\fill[%s] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (fill, x, y, cell, cell))
            w(r"\draw[white,line width=0.8pt] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (x, y, cell, cell))
            w(r"\node[text=%s] at (%.3f,%.3f) {%s};" % (txt, x + cell / 2, y + cell / 2, text))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,0) rectangle (%.3f,%.3f);" % (lab_w, lab_w + n * cell, n * cell))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    off = [vals[i][j] for i in range(n) for j in range(n) if i != j]
    diag = [vals[i][i] for i in range(n)]
    facts = {"min_offdiag": min(off), "max_offdiag": max(off), "min_diag": min(diag), "max_diag": max(diag),
             "min_ratio": min(off) / max(diag),
             "all_separated": all(core["divergence"]["visit_stream_separated_by_caption_rule"].values())}
    return "\n".join(L) + "\n", facts


def _pm(iv: dict, nd: int = 1) -> str:
    return "$%.*f \\pm %.*f$" % (nd, iv["mean"], nd, iv["ci95"])


def emit_table(core: dict) -> str:
    t = core["table"]
    k = "5"
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_unopposed_figures.py from")
    w("%   data/results/ch5_s531_unopposed/numbers.json (the no-defence corpus,")
    w("%%   %d runs per attacker, %d s horizon). Do not hand-edit; regenerate." % (t[PROFILES[0]]["n"], core["horizon"]))
    w(r"\begin{table}[htbp]")
    w(r"  \centering")
    w(r"  \caption[What each attacker does with no defence running]{Each attacker's behaviour with nothing opposing it, at the lineage horizon: the four attack profiles, the aggregate, which is the same corpus with the objective partition switched off and so the contrast objective conditioning is read against, and the baseline attacker. Means carry a 95\,\% interval; the opening count is the number of distinct length-five openings across the runs; the ending columns are shares of runs. The hosts column is the reference every suppression figure later in the chapter is a difference from, and the target column is what decides the rest of the chapter's shape, because a defence can only be credited with denying an objective the attacker would otherwise reach.}")
    w(r"  \label{tab:unopposed-summary}")
    # \scriptsize + tight padding together, the §k rule-1 fallback for a table
    # that will not fit \textwidth at \footnotesize; centred fixed-width numeric
    # columns so the two-line headers wrap inside the column
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"  \begin{tabular}{@{}P{3.0cm}*{7}{>{\centering\arraybackslash}p{1.5cm}}@{}}")
    w(r"    \toprule")
    w(r"    Attacker & Distinct tactics & Successes per host & Openings, $k=5$ & Path entropy\textsuperscript{\dag} & Hosts reached & Target reached & Ended at horizon \\")
    w(r"    \midrule")
    for i, p in enumerate(PROFILES):
        r = t[p]
        w("    %s & %s & %s & %d & %.2f & %s & %.2f & %.2f \\\\" % (
            LABEL[p], _pm(r["distinct_tactics"]), _pm(r["successes_per_host"]),
            r["distinct_openings"][k], r["path_entropy"], _pm(r["hosts"]),
            r["target_reach"], r["ended"].get("horizon", 0.0)))
    w(r"    \midrule")
    b = t["baseline"]
    w("    %s & %d\\textsuperscript{\\ddag} & --- & 1\\textsuperscript{\\ddag} & 0\\textsuperscript{\\ddag} & %s & %.2f & %.2f\\textsuperscript{\\S} \\\\" % (
        LABEL["baseline"], round(b["distinct_verbs"]["mean"]),
        _pm(b["hosts"]), b["target_reach"], b["ended"].get("horizon", 0.0)))
    w(r"    \bottomrule")
    w(r"    \addlinespace[2pt]")
    w(r"    \multicolumn{8}{@{}p{0.96\textwidth}@{}}{\scriptsize \textsuperscript{\dag}~pooled over the runs, in bits; on this corpus it tracks how much of the walk one place absorbs and is not read as variety on its own. \textsuperscript{\ddag}~structural, not measured: the baseline attacker has six activities and no tactic vocabulary, one opening at every length and no branching. \textsuperscript{\S}~the remaining %.2f of its runs ended on the simulator's inherited compromise-ratio stop with no target host held.}\\" % (
        b["ended"].get("compromise_ratio", 0.0)))
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


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


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    data = json.loads(args.numbers.read_text(encoding="utf-8"))
    if not data["sanity"]["all_cells_100"] or data["sanity"]["error_rows"]:
        raise SystemExit("corpus sanity failed; not drawing from it")
    core = data["core"]

    tex_a, facts_a = emit_fig_a(core)
    tex_b, facts_b = emit_fig_b(core)
    tab = emit_table(core)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    (FIG_DIR / f"{STEM_A}.tex").write_text(tex_a)
    (FIG_DIR / f"{STEM_B}.tex").write_text(tex_b)
    (TAB_DIR / f"{STEM_T}.tex").write_text(tab)
    print(f"wrote tables/{STEM_T}.tex")

    print("caption facts, Fig. 5.2:", json.dumps(facts_a))
    print("caption facts, Fig. 5.3:", json.dumps(facts_b))
    t = core["table"]
    for p in (*PROFILES, "baseline"):
        r = t[p]
        print(f"  {LABEL[p]:22s} hosts {r['hosts']['mean']:.2f}±{r['hosts']['ci95']:.2f}  target {r['target_reach']:.2f}  "
              f"horizon {r['ended'].get('horizon', 0):.2f}")
    if not args.no_compile:
        compile_fig(STEM_A)
        compile_fig(STEM_B)


if __name__ == "__main__":
    main()
