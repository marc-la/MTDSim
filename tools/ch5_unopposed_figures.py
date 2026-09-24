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


# Rows grouped by the verb each tactic dispatches (§4.4.3, the tactic-to-verb
# mapping), so the baseline attacker's verbs line up with the tactics that use them
# and each of its cells spans its group: no footnote, no repeated value
# (scrutinise-figure round 1, 2026-09-24). The group names are Figure 2.x's words.
GROUPS = (
    ("scan hosts", "SCAN_HOST", ("reconnaissance",)),
    ("enumerate", "ENUM_HOST", ("lateral-movement",)),
    ("scan ports", "SCAN_PORT", ("discovery",)),
    ("exploit", "EXPLOIT_VULN", ("initial-access", "execution", "privilege-escalation")),
    ("brute-force", "BRUTE_FORCE", ("credential-access",)),
    ("neighbours", "SCAN_NEIGHBOR", ("command-and-control",)),
    ("dwell-only", None, ("resource-development", "persistence", "stealth", "defense-impairment",
                          "collection", "exfiltration", "impact")),
)
TACTIC_NAME = dict(TACTICS)
HEAT = ((255, 255, 204), (253, 141, 60), (189, 0, 38))  # sequential, light to dark (E8: colour)


def heat(u: float) -> tuple[str, bool]:
    """Fill for a share scaled to [0, 1]; True when the text should be white."""
    u = max(0.0, min(1.0, u))
    a, b, f = (HEAT[0], HEAT[1], u / 0.5) if u <= 0.5 else (HEAT[1], HEAT[2], (u - 0.5) / 0.5)
    rgb = [round(x + (y - x) * f) for x, y in zip(a, b)]
    return "{rgb,255:red,%d;green,%d;blue,%d}" % tuple(rgb), u > 0.62


def _pct(v: float) -> str:
    return "0" if v == 0 else (r"$<$1" if v < 0.005 else "%d" % round(100 * v))


def emit_fig_a(core: dict) -> tuple[str, dict]:
    """Figure 5.1, three panels, one per attacker-behaviour metric of Table 5.2
    (the metrics design; scrutinise-figure round 1 amendments, 2026-09-24):
    (a) share of steps per tactic, a colour heat map with rows grouped by the verb
    each tactic dispatches and the baseline attacker's verbs spanning their groups;
    (b) attack path variation, vertical bars by opening length (2 to 8; length 1 is
    zero for every attacker by construction); (c) attack confidentiality against
    the alarm level (level 1 is zero by construction and is not drawn)."""
    m = core["metrics"]
    share = {p: m[p]["step_share"] for p in FOUR}
    base = m["baseline"]["step_share"]
    grouped = {t for _, _, ts in GROUPS for t in ts}
    unknown = {k for p in FOUR for k in share[p]} - grouped
    if unknown:
        raise SystemExit(f"tactics in the corpus with no row: {sorted(unknown)}")
    SERIES = (*FOUR, "baseline")
    apv = {p: m[p]["apv"] for p in SERIES}
    kmax = max(int(k) for k in apv["baseline"])
    conf = {p: m[p]["confidentiality"] for p in SERIES}
    vmax = max([v for p in FOUR for v in share[p].values()] + list(base.values()))

    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    BASE_STYLE = "cbase,line width=0.9pt,dash pattern=on 2.5pt off 1.5pt"

    def title(x, y, letter, text):
        w(r"\node[anchor=south west] at (%.3f,%.3f) {\textbf{(%s)}\enspace %s};" % (x, y, letter, text))

    # ---- (a) the heat map, rows grouped by verb -----------------------------------
    ch, GG = 0.40, 0.10               # row height, gap between groups
    GX, LAB = 0.0, 5.35               # group-name x (west), tactic-name x (east)
    cw, GAP, bw = 1.05, 0.25, 1.35
    X0 = LAB + 0.12
    cols = [(p, X0 + j * cw, cw) for j, p in enumerate(FOUR)]
    xb = X0 + len(FOUR) * cw + GAP
    n_rows = sum(len(ts) for _, _, ts in GROUPS)
    MY0 = 8.7
    MY1 = MY0 + n_rows * ch + (len(GROUPS) - 1) * GG
    # headers
    w(r"\node[anchor=south] at (%.3f,%.3f) {%s};" % (X0 + len(FOUR) * cw / 2, MY1 + 0.42, LABEL["movement"]))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0 + 0.05, MY1 + 0.42, X0 + len(FOUR) * cw - 0.05, MY1 + 0.42))
    for p, x, cwid in cols:
        w(r"\node[anchor=south] at (%.3f,%.3f) {%s};" % (x + cwid / 2, MY1 + 0.06, LABEL[p]))
    w(r"\node[anchor=south,align=center] at (%.3f,%.3f) {baseline\\attacker};" % (xb + bw / 2, MY1 + 0.06))
    title(GX, MY1 + 0.95, "a", "Share of steps per tactic (\\%)")
    y = MY1
    for gname, verb, tactics in GROUPS:
        gtop = y
        for t in tactics:
            y -= ch
            w(r"\node[anchor=east] at (%.3f,%.3f) {%s};" % (LAB, y + ch / 2, TACTIC_NAME[t]))
            for p, x, cwid in cols:
                v = share[p].get(t)
                if v is None:
                    w(r"\node[text=black!45] at (%.3f,%.3f) {---};" % (x + cwid / 2, y + ch / 2))
                else:
                    fill, white = heat(v / vmax)
                    w(r"\fill[fill=%s] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (fill, x, y, cwid, ch))
                    w(r"\node[text=%s] at (%.3f,%.3f) {%s};" % ("white" if white else "black", x + cwid / 2, y + ch / 2, _pct(v)))
                w(r"\draw[white,line width=0.8pt] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (x, y, cwid, ch))
        gbot = y
        w(r"\node[anchor=west,text=black!70] at (%.3f,%.3f) {\textit{%s}};" % (GX, (gtop + gbot) / 2, gname))
        # the baseline attacker's cell spans the group
        if verb is None:
            w(r"\node[text=black!45] at (%.3f,%.3f) {---};" % (xb + bw / 2, (gtop + gbot) / 2))
        else:
            v = base.get(verb, 0.0)
            fill, white = heat(v / vmax)
            w(r"\fill[fill=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fill, xb, gbot, xb + bw, gtop))
            w(r"\node[text=%s] at (%.3f,%.3f) {%s};" % ("white" if white else "black", xb + bw / 2, (gtop + gbot) / 2, _pct(v)))
        w(r"\draw[black!55,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xb, gbot, xb + bw, gtop))
        w(r"\draw[black!55,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (X0, gbot, X0 + len(FOUR) * cw, gtop))
        y -= GG

    # ---- the key, right of (a), shared by (b) and (c) -------------------------------
    KX0, ky = 11.9, MY1 - 0.2
    w(r"\node[anchor=west] at (%.3f,%.3f) {\textit{in (b) and (c)}};" % (KX0, ky))
    ky -= 0.55
    for p in SERIES:
        col = CNAME[p]
        w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.22,0.22);" % (col, KX0, ky - 0.11))
        if p == "baseline":
            w(r"\draw[%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (BASE_STYLE, KX0 + 0.35, ky, KX0 + 1.0, ky))
            w(r"\draw[cbase,line width=0.6pt,fill=white] (%.3f,%.3f) circle (0.07cm);" % (KX0 + 0.675, ky))
        else:
            w(r"\draw[%s,line width=0.6pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, KX0 + 0.35, ky, KX0 + 1.0, ky))
            marker(w, MARK[p], col, KX0 + 0.675, ky)
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (KX0 + 1.1, ky, LABEL[p] if p != "baseline" else "baseline attacker"))
        ky -= 0.5

    # ---- (b) attack path variation, vertical bars, full width -------------------------
    XB0, XB1, YB0, YB1 = 1.5, 15.6, 4.4, 7.0
    ks = list(range(2, kmax + 1))
    gw = (XB1 - XB0) / len(ks)
    bwid = gw * 0.8 / len(SERIES)

    def yb(v):
        return YB0 + v * (YB1 - YB0)

    axes(w, XB0, XB1, YB0, YB1,
         xticks=[(k, XB0 + (i + 0.5) * gw) for i, k in enumerate(ks)],
         yticks=[(v, yb(v / 100)) for v in range(0, 101, 25)],
         xlabel="length of the opening (steps)", ylabel="")
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {runs off the most\\common opening (\%%)};" % (XB0 - 0.8, (YB0 + YB1) / 2))
    title(GX, YB1 + 0.2, "b", "Attack path variation")
    for i, k in enumerate(ks):
        x0 = XB0 + (i + 0.5) * gw - len(SERIES) * bwid / 2
        for n, p in enumerate(SERIES):
            v = apv[p][str(k)]
            h = max(v * (YB1 - YB0), 0.0)
            w(r"\fill[%s] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (CNAME[p], x0 + n * bwid, YB0, bwid * 0.9, max(h, 0.025)))

    # ---- (c) attack confidentiality, full width -----------------------------------------
    XC0, XC1, YC0, YC1 = 1.5, 15.6, 0.0, 2.6
    th_all = conf["baseline"]["theta"]
    keep = [i for i, t in enumerate(th_all) if t > 1.0 + 1e-9]  # level 1: zero by construction
    th = [th_all[i] for i in keep]
    t0, t1 = 1.0, th[-1]

    def xc(v):
        return XC0 + (v - t0) / (t1 - t0) * (XC1 - XC0)

    def yc(v):
        return YC0 + v * (YC1 - YC0)

    axes(w, XC0, XC1, YC0, YC1,
         xticks=[(v, xc(v)) for v in range(1, int(t1) + 1)],
         yticks=[(v, yc(v / 100)) for v in range(0, 101, 25)],
         xlabel="alarm level (recent actions the detector counts)", ylabel="")
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {actions below\\the alarm (\%%)};" % (XC0 - 0.8, (YC0 + YC1) / 2))
    title(GX, YC1 + 0.2, "c", "Attack confidentiality")
    for p in SERIES:
        ys = [conf[p]["mean"][i] for i in keep]
        pts = [(xc(a), yc(b)) for a, b in zip(th, ys)]
        style = BASE_STYLE if p == "baseline" else "%s,line width=0.6pt" % CNAME[p]
        w(r"\draw[%s] %s;" % (style, " -- ".join("(%.3f,%.3f)" % q for q in pts)))
        for a, b in zip(th, ys):
            if abs(a - round(a)) < 1e-9:
                if p == "baseline":
                    w(r"\draw[cbase,line width=0.6pt,fill=white] (%.3f,%.3f) circle (0.07cm);" % (xc(a), yc(b)))
                else:
                    marker(w, MARK[p], CNAME[p], xc(a), yc(b))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")

    j2 = th_all.index(2.0)
    dwell = [t for g, v, ts in GROUPS if v is None for t in ts]
    facts = {
        "step_share_dwell_only": {LABEL[p]: sum(share[p].get(t, 0.0) for t in dwell) for p in FOUR},
        "baseline_step_share_by_verb": base,
        "apv_at_kmax": {LABEL[p]: apv[p][str(kmax)] for p in SERIES},
        "confidentiality_at_alarm_2": {LABEL[p]: conf[p]["mean"][j2] for p in SERIES},
        "kmax": kmax, "nruns": core["table"][FOUR[0]]["n"], "tau": core["detector"]["tau"],
    }
    return "\n".join(L) + "\n", facts


def _pm(iv: dict, nd: int = 1) -> str:
    return "$%.*f \\pm %.*f$" % (nd, iv["mean"], nd, iv["ci95"])


def emit_table(core: dict) -> str:
    """Table 5.3 (the metrics design, 2026-09-24): the attack-outcome class of
    Table 5.2 in the field's names (ASP, NCR, MTTC) and, beside it as E4 asked,
    the attack rate — the numbers that read the model as weaker next to the one
    that says why. Attack confidentiality is Figure 5.1(c)'s, not repeated here."""
    m = core["metrics"]
    t = core["table"]
    worst_none = max(m[p]["outcome"]["no_compromise_share"] for p in (*PROFILES, "baseline"))
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_unopposed_figures.py from")
    w("%   data/results/ch5_s531_unopposed/numbers.json (the no-defence corpus,")
    w("%%   %d runs per attacker, %d s horizon). Do not hand-edit; regenerate." % (t[PROFILES[0]]["n"], core["horizon"]))
    w("% Rebuilt 2026-09-24 on the metrics design (Table 5.2's names and classes).")
    w("% Caption session-written, how-to-read only. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[htbp]")
    w(r"  \centering")
    w(r"  \caption[Both attackers with no defence running]{The attack outcome and the attack rate of Table~\ref{tab:metrics} with no defence running, under the network, attack scenario and time limit of Table~\ref{tab:experiment}, for the APT attacker model on each attack profile and on the aggregate, and for the baseline attacker. ASP is a share of runs; the others are means with a 95\,\%% interval. MTTC is over the runs that compromise a host, which is all but at most %d\,\%% of any attacker's.}" % round(100 * worst_none))
    w(r"  \label{tab:unopposed-summary}")
    w(r"  \tablestyle\setlength{\tabcolsep}{4pt}")
    w(r"  \begin{tabular}{@{}P{4.0cm}*{4}{>{\centering\arraybackslash}p{2.6cm}}@{}}")
    w(r"    \toprule")
    w(r"    & \multicolumn{3}{c}{Attack outcome} & Attacker behaviour \\")
    w(r"    \cmidrule(lr){2-4}\cmidrule(l){5-5}")
    w(r"    Attacker & ASP & NCR & MTTC (s) & Attack rate (per 1\,000\,s) \\")
    w(r"    \midrule")

    def row(name: str, p: str) -> str:
        o = m[p]["outcome"]
        return "    %s & %.2f & %s & %s & %s \\\\" % (
            name, o["asp"], _pm(o["ncr"], 2), _pm(o["mttc"]["observed"], 0), _pm(m[p]["attack_rate"], 1))

    w(r"    \emph{%s} & & & & \\" % LABEL["movement"])
    for p in PROFILES:
        w(row(r"\quad " + LABEL[p], p))
    w(r"    \midrule")
    w(row(r"\emph{baseline attacker}", "baseline"))
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
    m = core["metrics"]
    for p in (*PROFILES, "baseline"):
        o = m[p]["outcome"]
        print(f"  {LABEL[p].strip('$'):18s} ASP {o['asp']:.2f}  NCR {o['ncr']['mean']:.3f}  "
              f"MTTC {o['mttc']['observed']['mean']:.0f}  none {o['no_compromise_share']:.2f}  "
              f"rate {m[p]['attack_rate']['mean']:.1f}")
    if not args.no_compile:
        compile_fig(STEM_A)


if __name__ == "__main__":
    main()
