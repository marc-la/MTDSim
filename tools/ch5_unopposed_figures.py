#!/usr/bin/env python3
"""Chapter 5 no-MTD floats from the no-MTD corpus: the campaign figure
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
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (BASE_DASH, IV_BOOT, IV_MEAN, IV_PROP, XTITLE_H, clopper_pearson, key_below,  # noqa: E402
                        mttc_dash_decode, mttc_unreported, panel_title)  # noqa: E402  (the layout, conventions §o)

REPO = Path(__file__).resolve().parents[1]
FIG_DIR = REPO / "docs" / "thesis" / "figures"
TAB_DIR = REPO / "docs" / "thesis" / "tables"
# the reported corpus (1 000 seeds, the vulnerability memory on; 2026-09-30)
NUMBERS = REPO / "data" / "results" / "ch5_s531_unopposed" / "numbers_reported.json"
STEM_A = "fig_5-2-1a_campaign_openings"
STEM_T = "tab_5-2-1a_unopposed_summary"

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
)  # the attack graph before partition left Table 5.2 on 2026-10-02 (Section 5.4.1's ablation arm)
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
    r"\usetikzlibrary{calc,patterns}",
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
from _ch5_style import ACTIVITY  # plain phase names (2026-09-30)
GROUPS = (
    (ACTIVITY["SCAN_HOST"], "SCAN_HOST", ("reconnaissance",)),
    (ACTIVITY["ENUM_HOST"], "ENUM_HOST", ("lateral-movement",)),
    (ACTIVITY["SCAN_PORT"], "SCAN_PORT", ("discovery",)),
    (ACTIVITY["EXPLOIT_VULN"], "EXPLOIT_VULN", ("initial-access", "execution", "privilege-escalation")),
    (ACTIVITY["BRUTE_FORCE"], "BRUTE_FORCE", ("credential-access",)),
    (ACTIVITY["SCAN_NEIGHBOR"], "SCAN_NEIGHBOR", ("command-and-control",)),
    ("unmapped", None, ("resource-development", "persistence", "stealth", "defense-impairment",
                          "collection", "exfiltration", "impact")),
)
TACTIC_NAME = dict(TACTICS)
HEAT = ((255, 255, 204), (253, 141, 60), (189, 0, 38))  # sequential, light to dark (E8: colour)


def fmt_thousands(n: int) -> str:
    """12\,000, the thesis's numerals rule (thin space from 1 000 up)."""
    return f"{n:,}".replace(",", r"\,") if n >= 1000 else str(n)


def heat(u: float) -> tuple[str, bool]:
    """Fill for a share scaled to [0, 1]; True when the text should be white."""
    u = max(0.0, min(1.0, u))
    a, b, f = (HEAT[0], HEAT[1], u / 0.5) if u <= 0.5 else (HEAT[1], HEAT[2], (u - 0.5) / 0.5)
    rgb = [round(x + (y - x) * f) for x, y in zip(a, b)]
    return "{rgb,255:red,%d;green,%d;blue,%d}" % tuple(rgb), u > 0.62


def _pct(v: float) -> str:
    return "0" if v == 0 else (r"$<$1" if v < 0.005 else "%d" % round(100 * v))


def emit_fig_a(core: dict) -> tuple[str, dict]:
    """Figure 5.1, two panels (the metrics design; scrutinise-figure round 1
    amendments, 2026-09-24): (a) share of steps per tactic, a colour heat map with
    rows grouped by the verb each tactic dispatches and the baseline attacker's
    verbs spanning their groups; (b) distinct openings by opening length. Attack
    confidentiality, panel (c) until 2026-10-05, is a column of Table 5.2 (Marc:
    "it's literally five numbers")."""
    m = core["metrics"]
    share = {p: m[p]["step_share"] for p in FOUR}
    base = m["baseline"]["step_share"]
    grouped = {t for _, _, ts in GROUPS for t in ts}
    unknown = {k for p in FOUR for k in share[p]} - grouped
    if unknown:
        raise SystemExit(f"tactics in the corpus with no row: {sorted(unknown)}")
    SERIES = (*FOUR, "baseline")
    paths = {p: core["table"][p]["distinct_openings"] for p in SERIES}
    kmax = max(int(k) for k in paths["baseline"])
    vmax = max([v for p in FOUR for v in share[p].values()] + list(base.values()))

    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    BASE_STYLE = "cbase,line width=0.9pt," + BASE_DASH  # the baseline attacker's line, as every figure


    # ---- (a) the heat map, rows grouped by verb -----------------------------------
    ch, GG = 0.40, 0.10               # row height, gap between groups
    GX, LAB = 0.0, 5.75               # group-name x (west), tactic-name x (east)
    cw, GAP, bw = 0.98, 0.22, 1.3
    X0 = LAB + 0.12
    cols = [(p, X0 + j * cw, cw) for j, p in enumerate(FOUR)]
    xb = X0 + len(FOUR) * cw + GAP
    n_rows = sum(len(ts) for _, _, ts in GROUPS)
    MY0 = 4.2   # (b)'s title and plot below; the key is at the figure's foot (conventions §o)
    MY1 = MY0 + n_rows * ch + (len(GROUPS) - 1) * GG
    # headers
    w(r"\node[anchor=south] at (%.3f,%.3f) {%s};" % (X0 + len(FOUR) * cw / 2, MY1 + 0.42, LABEL["movement"]))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0 + 0.05, MY1 + 0.42, X0 + len(FOUR) * cw - 0.05, MY1 + 0.42))
    for p, x, cwid in cols:
        w(r"\node[anchor=south] at (%.3f,%.3f) {%s};" % (x + cwid / 2, MY1 + 0.06, LABEL[p]))
    w(r"\node[anchor=south,align=center] at (%.3f,%.3f) {baseline\\attacker};" % (xb + bw / 2, MY1 + 0.06))
    panel_title(w, 1.5, MY1 + 0.87, "Relative tactic occurrence (\\%)", "a")  # (b)'s y-axis: one left edge per column
    y = MY1
    for gname, verb, tactics in GROUPS:
        gtop = y
        for t in tactics:
            y -= ch
            w(r"\node[anchor=east] at (%.3f,%.3f) {%s};" % (LAB, y + ch / 2, TACTIC_NAME[t]))
            for p, x, cwid in cols:
                v = share[p].get(t)
                if v is None:
                    pass  # a tactic the profile does not have: blank, not applicable (standard S1)
                else:
                    fill, white = heat(v / vmax)
                    w(r"\fill[fill=%s] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (fill, x, y, cwid, ch))
                    w(r"\node[text=%s] at (%.3f,%.3f) {%s};" % ("white" if white else "black", x + cwid / 2, y + ch / 2, _pct(v)))
                w(r"\draw[white,line width=0.8pt] (%.3f,%.3f) rectangle ++(%.3f,%.3f);" % (x, y, cwid, ch))
        gbot = y
        w(r"\node[anchor=west,text=black!70,font=\scriptsize] at (%.3f,%.3f) {%s};" % (GX, (gtop + gbot) / 2, gname if verb else r"\textit{%s}" % gname))
        # the baseline attacker's cell spans the group
        if verb is None:
            pass  # the baseline attacker has no dwell-only tactics: blank, not applicable (S1)
        else:
            v = base.get(verb, 0.0)
            fill, white = heat(v / vmax)
            w(r"\fill[fill=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fill, xb, gbot, xb + bw, gtop))
            w(r"\node[text=%s] at (%.3f,%.3f) {%s};" % ("white" if white else "black", xb + bw / 2, (gtop + gbot) / 2, _pct(v)))
        w(r"\draw[black!55,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xb, gbot, xb + bw, gtop))
        w(r"\draw[black!55,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (X0, gbot, X0 + len(FOUR) * cw, gtop))
        y -= GG

    # ---- (b) distinct openings, full width ----------------------------------------
    # Scrutiny round, 2026-09-30 (Marc; cold readers and critics): the axis names
    # the run count, the count's ceiling. (b) is lines, not bars. Attack
    # confidentiality, beside it as (c) until 2026-10-05, is Table 5.2's column.
    YB0, YB1 = 0.0, 3.0
    XB0, XB1 = 1.5, 15.6
    ks = list(range(1, kmax + 1))
    nruns = core["table"][FOUR[0]]["n"]

    def xb_(k):
        return XB0 + (k - 0.5) / kmax * (XB1 - XB0)

    # 2026-10-06 (Marc, section 5.2 round): a log axis, so the baseline attacker's
    # 1 to 3 and the first four steps, flat on zero on a linear axis, can be read and
    # the caption need not state them.
    def yb(v):
        return YB0 + math.log10(v) / math.log10(nruns) * (YB1 - YB0)

    axes(w, XB0, XB1, YB0, YB1,
         xticks=[(k, xb_(k)) for k in ks],
         yticks=[(10 ** e, yb(10 ** e)) for e in range(0, round(math.log10(nruns)) + 1)],
         xlabel=r"First $k$ steps", ylabel="")
    # the run count is the caption's (1 000: every run its own) (Marc 2026-10-06)
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {Distinct openings\\(log scale)};"
      % (XB0 - 0.8, (YB0 + YB1) / 2))
    for p in SERIES:
        pts = [(xb_(k), yb(paths[p][str(k)])) for k in ks]
        style = BASE_STYLE if p == "baseline" else "%s,line width=0.7pt" % CNAME[p]
        w(r"\draw[%s] %s;" % (style, " -- ".join("(%.3f,%.3f)" % q for q in pts)))
        for x, yv in pts:
            marker(w, "square" if p == "baseline" else MARK[p], CNAME[p], x, yv, r=0.07 if p == "baseline" else 0.08)
    panel_title(w, XB0, YB1, "Distinct openings", "b")

    # the figure's one key, at its foot (conventions §o)
    key_below(w, XB0, YB0 - 0.5 - XTITLE_H,
              [(LABEL[p], "dashed" if p == "baseline" else "line", CNAME[p],
                "square" if p == "baseline" else MARK[p]) for p in SERIES], xmax=XB1)
    w(r"\end{tikzpicture}")
    w(r"\end{document}")

    dwell = [t for g, v, ts in GROUPS if v is None for t in ts]
    facts = {
        "step_share_dwell_only": {LABEL[p]: sum(share[p].get(t, 0.0) for t in dwell) for p in FOUR},
        "baseline_step_share_by_verb": base,
        "distinct_attack_paths": {LABEL[p]: paths[p] for p in SERIES},
        "kmax": kmax, "nruns": core["table"][FOUR[0]]["n"],
    }
    return "\n".join(L) + "\n", facts


def _place(hw: float) -> int:
    """The precision rule (Marc 2026-09-30, every table): a column is rounded to
    the place of its widest interval's half-width at one significant figure (two
    when that figure is a 1), so values within a column align."""
    import math
    place = math.floor(math.log10(hw)) if hw > 0 else -2
    if hw > 0 and int(round(hw / 10.0 ** place, 6)) == 1:
        place -= 1
    return place


def _prec(mean: float, hw: float, place: int) -> str:
    nd = max(0, -place)
    q = 10.0 ** place
    m, h = round(mean / q) * q, round(hw / q) * q
    if nd == 0:
        return "$%s \\pm %s$" % (fmt_thousands(int(round(m))), fmt_thousands(int(round(h))))
    return "$%.*f \\pm %.*f$" % (nd, m, nd, h)


def _pm(iv: dict, nd: int = 1) -> str:
    return "$%.*f \\pm %.*f$" % (nd, iv["mean"], nd, iv["ci95"])


def _pm_thousands(iv: dict | None) -> str:
    """MTTC: whole seconds, thin space from 1 000; a dash where no run takes a target."""
    if iv is None:
        return "---"
    return "$%s \\pm %s$" % (fmt_thousands(round(iv["mean"])), fmt_thousands(round(iv["ci95"])))


def emit_table(core: dict) -> str:
    """Table 5.3 (the metrics design, 2026-09-24): the attack-outcome class of
    Table 5.2 in the field's names (ASP, NCR, MTTC) and, beside it as E4 asked,
    the attack rate — the numbers that read the model as weaker next to the one
    that says why — and attack confidentiality, the attack rate's partner in
    detection avoidance (Figure 5.1(c) until 2026-10-05, Marc: "it's literally
    five numbers"). MTTC is read at a target host (2026-09-30), over the runs ASP
    counts."""
    m = core["metrics"]
    t = core["table"]
    worst_none = max(m[p]["outcome"]["no_compromise_share"] for p in (*PROFILES, "baseline"))
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_unopposed_figures.py from")
    w("%%   %s (the no-MTD corpus," % NUMBERS.relative_to(REPO))
    w("%%   %d runs per attacker, %d s horizon). Do not hand-edit; regenerate." % (t[PROFILES[0]]["n"], core["horizon"]))
    w("% Rebuilt 2026-09-24 on the metrics design (Table 5.2's names and classes).")
    w("% 2026-09-30: MTTC at a target host (section 4.5.2, ruling H1), over the runs that take one.")
    w("% Caption session-written, how-to-read only. DRAFT STATE --- ratify on read.")
    w("% 2026-10-06 (Marc, section 5.2 round): caption decodes only; the definitions, the unit and the default bootstrap cut (Section 4.5, the header, Section 5.1).")
    w("% 2026-10-06 (Marc, round 2): the attackers and the 1 000 runs cut (the rows, Table 5.1), MTTC's runs into the cells, the interval methods to Section 5.1.")
    w(r"\begin{table}[htbp]")
    w(r"  \centering")
    w(r"  \caption[Both attackers with no MTD running]{Attack outcome, attack rate and attack confidentiality with no MTD running (Section~\ref{sec:evaluation-metrics}). In parentheses: the runs MTTC is over.%s}" % mttc_dash_decode({mttc_unreported(m[p]["outcome"]["mttc"]) for p in (*PROFILES, "baseline")} - {None}))
    w(r"  \label{tab:unopposed-summary}")
    # one header row (2026-09-24, Marc: the class headers read loose; Table 4.3
    # carries the classes), full text width
    # natural width, the house table style (scrutiny round 2026-09-30: it was
    # stretched to the text width); the attacker model is a group label row
    w(r"  \tablestyle")  # group rows keep the stripes (Marc, 2026-10-01)
    w(r"  \begin{tabular}{@{}lccccc@{}}")
    w(r"    \toprule")
    w(r"    Attacker & ASP & NCR & MTTC (s) & \shortstack{Attack rate\\(per minute)} & \shortstack{Attack\\confidentiality (\%)} \\")
    w(r"    \midrule")

    def cells(p: str) -> dict:
        o = m[p]["outcome"]
        c = m[p]["attack_confidentiality"]
        n = t[p]["n"]  # ASP: an exact (Clopper-Pearson) interval on a share of runs (standard N4)
        lo, hi = clopper_pearson(round(o["asp"] * n), n)
        return {"asp": (o["asp"], (hi - lo) / 2, lo, hi),
                "ncr": (o["ncr"]["mean"], o["ncr"]["ci95"]),
                "mttc": None if mttc_unreported(o["mttc"]) else (o["mttc"]["mean"], o["mttc"]["ci95"]),
                "rate": (m[p]["attack_rate"]["mean"], m[p]["attack_rate"]["ci95"]),
                # a percentile bootstrap interval over runs, in percent (asymmetric; the
                # half-width that sets the place is the wider side)
                "conf": (100 * c["point"], 100 * max(c["hi"] - c["point"], c["point"] - c["lo"]),
                         100 * c["lo"], 100 * c["hi"])}

    rows = {p: cells(p) for p in (*PROFILES, "baseline")}
    place = {k: _place(max(r[k][1] for r in rows.values() if r[k] is not None))
             for k in ("asp", "ncr", "mttc", "rate", "conf")}

    def bracket(v, _hw, lo, hi, pl):
        nd = max(0, -pl)
        return "$%.*f$ [$%.*f$, $%.*f$]" % (nd, v, nd, lo, nd, hi)

    def row(name: str, p: str) -> str:
        r = rows[p]
        f = {k: ("---" if r[k] is None else (bracket(*r[k], place[k]) if k in ("asp", "conf") else _prec(*r[k], place[k])))
             for k in r}
        if r["mttc"] is not None:  # the runs MTTC is over, in the cell as Table F.1 prints it (Marc 2026-10-06)
            f["mttc"] += " (%d)" % m[p]["outcome"]["mttc"]["n"]
        return "    %s & %s & %s & %s & %s & %s \\\\" % (name, f["asp"], f["ncr"], f["mttc"], f["rate"], f["conf"])

    w(r"    \grouprow{6}{%s} \\" % LABEL["movement"])
    for p in PROFILES:
        w(row(r"\quad " + LABEL[p], p))
    w(r"    \midrule")
    w(row(r"Baseline attacker", "baseline"))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


STEM_D = "tab_C-4a_detector_memory"


def emit_detector_table(core: dict) -> tuple[str, list[str]]:
    """Appendix C.4 (2026-09-30): attack confidentiality at each count and window
    of the scan detector around the declared Snort default (five in 60 s), with
    the share of the baseline attacker's actions the setting flags."""
    SERIES = (*FOUR, "baseline")
    L: list[str] = []
    w = L.append
    facts = []
    w("%% GENERATED by tools/ch5_unopposed_figures.py from %s" % NUMBERS.relative_to(REPO))
    w("%   (core.detector_grid). Do not hand-edit; regenerate. 2026-09-30. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[htbp]")
    w(r"  \centering")
    w(r"  \caption[Attack confidentiality across the detector's count and window]{Attack confidentiality (\%%) with no MTD running at each count and window of the scan detector (Section~\ref{subsec:metrics-behaviour}), for the APT attacker model on the attack profiles $c_1$ to $c_4$ and for the baseline attacker, with the share of the baseline attacker's attack actions each setting flags. The declared setting, five attack actions within 60\,s, is in bold. Every value's %s is within %.1f points.}" % (IV_BOOT,
      100 * max(max(v["hi"] - v["point"], v["point"] - v["lo"]) for g in core["detector_grid"] for v in g["confidentiality"].values())))
    w(r"  \label{tab:detector-memory}")
    w(r"  \tablestyle\setlength{\tabcolsep}{4pt}")
    w(r"  \begin{tabular}{@{}cc*{5}{>{\centering\arraybackslash}p{1.35cm}}>{\centering\arraybackslash}p{2.6cm}@{}}")
    w(r"    \toprule")
    w(r"    Count & Window (s) & %s & Baseline attacker's attack actions flagged (\%%) \\" % " & ".join(
        r"\shortstack{baseline\\attacker}" if q == "baseline" else LABEL[q] for q in SERIES))
    w(r"    \midrule")
    for g in core["detector_grid"]:
        c = g["confidentiality"]
        bold = g["count"] == 5 and g["window"] == 60.0
        cells = ["%.1f" % (100 * c[q]["point"]) for q in SERIES] + ["%.1f" % (100 * (1 - c["baseline"]["point"]))]
        if bold:
            cells = [r"\textbf{%s}" % x for x in cells]
        head = [str(g["count"]), "%d" % g["window"]]
        if bold:
            head = [r"\textbf{%s}" % x for x in head]
        w("    %s \\\\" % " & ".join(head + cells))
        above = all(c[q]["lo"] > c["baseline"]["hi"] for q in FOUR)
        facts.append(f"count {g['count']:2d} window {g['window']:5.0f}: flagged baseline {100 * (1 - c['baseline']['point']):5.1f} %  "
                     f"every profile above baseline (intervals apart): {above}  "
                     + " ".join(f"{LABEL[q].strip('$')} {100 * c[q]['point']:.2f}" for q in SERIES))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n", facts


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
    if not data["sanity"].get("all_cells_full", data["sanity"].get("all_cells_100")) or data["sanity"]["error_rows"]:
        raise SystemExit("corpus sanity failed; not drawing from it")
    core = data["core"]

    tex_a, facts_a = emit_fig_a(core)
    tab = emit_table(core)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    (FIG_DIR / f"{STEM_A}.tex").write_text(tex_a)
    tex_d, facts_d = emit_detector_table(core)
    (TAB_DIR / f"{STEM_D}.tex").write_text(tex_d)
    print(f"wrote tables/{STEM_D}.tex")
    for f in facts_d:
        print("  " + f)
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
              f"MTTC {o['mttc']['mean']:.0f} (n {o['mttc']['n']})  none {o['no_compromise_share']:.2f}  "
              f"rate {m[p]['attack_rate']['mean']:.2f}")
    if not args.no_compile:
        compile_fig(STEM_A)


if __name__ == "__main__":
    main()
