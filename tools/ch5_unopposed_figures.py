#!/usr/bin/env python3
"""Chapter 5 no-defence floats from the no-defence corpus: the campaign figure
(share of steps by tactic and profile, and the share of runs that have left
the commonest opening; reworked 2026-09-20, results context §8) and Table 5.3
(behaviour without defence, by attacker). The pairwise divergence matrix that
was Figure 5.2 is DEMOTED to body-text content (2026-09-21, results context
§8d): its numbers are printed on stdout from the analyser's block and drawn
nowhere.

Data: ``data/results/ch5_s531_unopposed/numbers.json``, the analyser's output
over the recorded corpus (design: docs/handoffs/2026-09-15_ch5_s531_unopposed_runs.md;
read: docs/implementation/pipeline/ogasp/ch5_s531_unopposed_findings.md).
Nothing is typed here: every plotted value, every table cell and every number a
caption may quote is read from that file and printed on stdout.

Usage:
  python tools/ch5_unopposed_figures.py [--numbers PATH] [--no-compile]

Writes
  docs/thesis/figures/fig_5-2-1a_campaign_openings.{tex,pdf}
  docs/thesis/tables/tab_5-2-1a_unopposed_summary.tex

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
STEM_A = "fig_5-2-1a_campaign_openings"
STEM_T = "tab_5-2-1a_unopposed_summary"

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
    # the profile codes chapter 4 declares (§4.3, tab:gspn-notation; Marc's
    # ruling 2026-09-22): c_1 exfiltration, c_2 impact, c_3 double extortion,
    # c_4 no realised objective, c_agg the unpartitioned aggregate
    "objective_exfiltration": "$c_1$",
    "objective_impact": "$c_2$",
    "objective_exfiltration_impact": "$c_3$",
    "objective_none_c2": "$c_4$",
    "aggregate": r"$c_{\mathrm{agg}}$",
    "baseline": "baseline attacker",
    "movement": "APT attacker model",  # mirrors _ch5_style.LABEL (register E2, 2026-09-22)
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


# chapter 4's tactic order (the order of the outcome-weight matrix, App. B)
TACTICS = (
    ("reconnaissance", "Reconnaissance"),
    ("resource-development", "Resource development"),
    ("initial-access", "Initial access"),
    ("execution", "Execution"),
    ("persistence", "Persistence"),
    ("privilege-escalation", "Privilege escalation"),
    ("stealth", "Stealth"),
    ("defense-impairment", "Defense impairment"),
    ("credential-access", "Credential access"),
    ("discovery", "Discovery"),
    ("lateral-movement", "Lateral movement"),
    ("command-and-control", "Command and control"),
    ("collection", "Collection"),
    ("exfiltration", "Exfiltration"),
    ("impact", "Impact"),
)
TWO_LINE = {p: LABEL[p] for p in FOUR}  # column heads: the codes, one line


def emit_fig_a(core: dict) -> tuple[str, dict]:
    """Panel (a): where each profile spends its steps, as the share of steps in
    each named tactic (the distribution the divergence matrix summarises).
    Panel (b): the share of runs that have left the attacker's most common
    opening, against the opening's length, over the lengths the baseline
    attacker's six activities cover; the baseline measured. One unit, the step,
    carries both panels."""
    t = core["table"]
    visit = {p: t[p]["tactic_visit_share"] for p in FOUR}
    unknown = {k for p in FOUR for k in visit[p]} - {k for k, _ in TACTICS}
    if unknown:
        raise SystemExit(f"tactics in the corpus with no row in TACTICS: {sorted(unknown)}")
    left = {p: {k: 1.0 - v for k, v in t[p]["commonest_opening_share"].items()} for p in (*FOUR, "baseline")}
    kmax = max(int(k) for k in left["baseline"])
    vmax = max(v for p in FOUR for v in visit[p].values())

    # geometry (cm)
    cw, ch = 1.45, 0.5
    LAB = 3.45
    n_r = len(TACTICS)
    MY0 = 0.0
    MY1 = MY0 + n_r * ch
    XB0, XB1 = 11.3, 15.6
    YB1 = MY1 - 0.1
    YB0 = YB1 - 4.9

    def yb(v):
        return YB0 + v * (YB1 - YB0)

    def xb(k):
        return XB0 + (k - 1) / (kmax - 1) * (XB1 - XB0)

    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    # panel (a): the matrix
    w(r"\node[anchor=south west,font=\footnotesize\bfseries] at (0,%.3f) {(a)};" % (MY1 + 0.3))
    for j, p in enumerate(FOUR):
        w(r"\node[anchor=south,align=center] at (%.3f,%.3f) {%s};" % (LAB + (j + 0.5) * cw, MY1 + 0.1, TWO_LINE[p]))
    for i, (key, name) in enumerate(TACTICS):
        y = MY1 - (i + 1) * ch
        w(r"\node[anchor=east] at (%.3f,%.3f) {%s};" % (LAB - 0.15, y + ch / 2, name))
        for j, p in enumerate(FOUR):
            x = LAB + j * cw
            v = visit[p].get(key)
            if v is None:  # not a tactic of this profile
                w(r"\node[text=black!45] at (%.3f,%.3f) {---};" % (x + cw / 2, y + ch / 2))
            else:
                shade = int(round(70 * v / vmax))
                w(r"\fill[black!%d] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (shade, x, y, cw, ch))
                txt = "0" if v == 0 else ("$<$1" if v < 0.005 else "%d" % round(100 * v))
                w(r"\node[text=%s] at (%.3f,%.3f) {%s};" % ("white" if shade >= 45 else "black", x + cw / 2, y + ch / 2, txt))
            w(r"\draw[white,line width=0.8pt] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (x, y, cw, ch))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (LAB, MY0, LAB + len(FOUR) * cw, MY1))
    w(r"\node[anchor=north,text=black!60] at (%.3f,%.3f) {share of the profile's steps (\%%)};" % (LAB + len(FOUR) * cw / 2, MY0 - 0.12))

    # panel (b): departure from the most common opening
    axes(w, XB0, XB1, YB0, YB1,
         xticks=[(k, xb(k)) for k in range(1, kmax + 1)],
         yticks=[(v, yb(v / 100)) for v in range(0, 101, 25)],
         xlabel="length of the opening (steps)", ylabel="")
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {runs that have left the\\most common opening (\%%)};" % (XB0 - 0.8, (YB0 + YB1) / 2))
    w(r"\node[anchor=south west,font=\footnotesize\bfseries] at (%.3f,%.3f) {(b)};" % (XB0 - 1.75, MY1 + 0.3))
    pts = [(xb(k), yb(left["baseline"][str(k)])) for k in range(1, kmax + 1)]
    w(r"\draw[cbase,line width=0.9pt,dash pattern=on 2.5pt off 1.5pt] %s;" % " -- ".join("(%.3f,%.3f)" % q for q in pts))
    for p in FOUR:
        pts = [(xb(k), yb(left[p][str(k)])) for k in range(1, kmax + 1)]
        w(r"\draw[%s,line width=0.6pt] %s;" % (CNAME[p], " -- ".join("(%.3f,%.3f)" % q for q in pts)))
        for x, y in pts:
            marker(w, MARK[p], CNAME[p], x, y)
    # key, under (b)
    KX0 = XB0 - 0.6
    ky = YB0 - 1.2
    for p in FOUR:
        w(r"\draw[%s,line width=0.6pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (CNAME[p], KX0, ky, KX0 + 0.7, ky))
        marker(w, MARK[p], CNAME[p], KX0 + 0.35, ky)
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (KX0 + 0.85, ky, LABEL[p]))
        ky -= 0.42
    w(r"\draw[cbase,line width=0.9pt,dash pattern=on 2.5pt off 1.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (KX0, ky, KX0 + 0.7, ky))
    w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (KX0 + 0.85, ky, LABEL["baseline"]))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")

    facts = {
        "visit_share_top": {LABEL[p]: max(visit[p].items(), key=lambda kv: kv[1]) for p in FOUR},
        "held_never_entered": {LABEL[p]: [k for k, v in visit[p].items() if v == 0] for p in FOUR},
        "left_commonest_at_kmax": {LABEL[p]: left[p][str(kmax)] for p in (*FOUR, "baseline")},
        "tactics_held": {LABEL[p]: len(visit[p]) for p in FOUR},
        "kmax": kmax, "nruns": t[FOUR[0]]["n"],
    }
    return "\n".join(L) + "\n", facts


def _pm(iv: dict, nd: int = 1) -> str:
    return "$%.*f \\pm %.*f$" % (nd, iv["mean"], nd, iv["ci95"])


def emit_table(core: dict) -> str:
    """The no-defence reference (takeaway T4, results context §8e): Table 5.2's
    effectiveness metrics at no defence, per attacker. Every column is a Table
    5.2 term, so the table carries no footnote; the columns that repeated
    Figure 5.1 (distinct tactics, the commonest opening), path entropy, the
    §5.4 cost metric and the ending column (one minus target reached) were cut
    on Marc's ruling, 2026-09-21."""
    t = core["table"]
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_unopposed_figures.py from")
    w("%   data/results/ch5_s531_unopposed/numbers.json (the no-defence corpus,")
    w("%%   %d runs per attacker, %d s horizon). Do not hand-edit; regenerate." % (t[PROFILES[0]]["n"], core["horizon"]))
    w("% Caption session-written, how-to-read only. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[htbp]")
    w(r"  \centering")
    w(r"  \caption[Both attackers with no defence running]{Four of the effectiveness metrics of Table~\ref{tab:metrics} with no defence running, under the network and time limit of Table~\ref{tab:experiment}, for the APT attacker model on each attack profile and on the aggregate, and for the baseline attacker. Hosts reached and delay to first compromise are means with a 95\,\% interval, the delay over the runs that compromise a host; the other two columns are shares of runs.}")
    w(r"  \label{tab:unopposed-summary}")
    w(r"  \tablestyle\setlength{\tabcolsep}{4pt}")
    w(r"  \begin{tabular}{@{}P{4.2cm}*{4}{>{\centering\arraybackslash}p{2.5cm}}@{}}")
    w(r"    \toprule")
    w(r"    Attacker & Hosts reached (of 50) & Target reached & Delay to first compromise (s) & Runs with no compromise \\")
    w(r"    \midrule")

    def row(name: str, r: dict) -> str:
        d = r["delay"]
        return "    %s & %s & %.2f & %s & %.2f \\\\" % (
            name, _pm(r["hosts"]), r["target_reach"], _pm(d["observed"], 0), d["no_compromise_share"])

    w(r"    \emph{%s} & & & & \\" % LABEL["movement"])
    for p in PROFILES:
        w(row(r"\quad " + LABEL[p], t[p]))
    w(r"    \midrule")
    w(row(r"\emph{baseline attacker}", t["baseline"]))
    w(r"    \bottomrule")
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
    tab = emit_table(core)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    (FIG_DIR / f"{STEM_A}.tex").write_text(tex_a)
    (TAB_DIR / f"{STEM_T}.tex").write_text(tab)
    print(f"wrote tables/{STEM_T}.tex")

    print("caption facts, Fig. 5.1:", json.dumps(facts_a))
    print("body facts, pairwise divergence (demoted 2026-09-21):", json.dumps(core["divergence"]["body_facts"]))
    for k, c in core["divergence"]["visit_stream"].items():
        a, b = k.split("|")
        if a < b:
            print(f"  {LABEL[a].strip('$'):8s} {LABEL[b].strip('$'):8s} {c['jsd']:.3f}  absent-tactic share {c['absent_tactic_share']:.2f}")
    t = core["table"]
    for p in (*PROFILES, "baseline"):
        r = t[p]
        print(f"  {LABEL[p].strip('$'):8s} hosts {r['hosts']['mean']:.2f}±{r['hosts']['ci95']:.2f}  target {r['target_reach']:.2f}  "
              f"delay {r['delay']['observed']['mean']:.0f}±{r['delay']['observed']['ci95']:.0f}  "
              f"no compromise {r['delay']['no_compromise_share']:.2f}")
    if not args.no_compile:
        compile_fig(STEM_A)


if __name__ == "__main__":
    main()
