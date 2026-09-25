#!/usr/bin/env python3
"""Chapter 5 §5.4 floats from the defended corpus.

  §5.4.1  Fig. 5.5  suppression of host breadth by defence condition, per
                    profile (2 x 2 lettered panels: singles / schemes at each
                    interval; series = profile, the chapter's hues)
          Tab. 5.5  the conditions against the attacker model on Table 4.3's
                    outcome and effectiveness metrics, in its order (2026-09-25)
                    (reworked 2026-09-22: caption decode-only, no footnote,
                    no dagger; overlap is read from the printed intervals)
  §5.4.2  Fig. 5.6  the same defences against both attackers (series = arm;
                    the baseline hatched, the model solid)
          Tab. 5.6  the two orderings side by side, the model as the base
                    (reworked 2026-09-25, E7): its columns first, rows in its
                    rank order; no footnote, no rank statistic
  §5.4.3  Tab. 5.7  the prior evaluations' headline findings under both
                    attackers, from the lineage-objective arm

Data: ``data/results/ch5_defended/numbers.json`` §s541, §s542, §s543
(design: docs/handoffs/2026-09-17_ch5_s532_s55_defended_runs.md; read:
docs/implementation/pipeline/ogasp/ch5_s54_effectiveness_findings.md).
Nothing is typed here: every bar, cell and caption number is read from that
file and printed on stdout.

Usage:
  python tools/ch5_effectiveness_figures.py [--numbers PATH] [--no-compile] [--only STEM]

Writes
  docs/thesis/figures/fig_5-3-1a_suppression_profiles.{tex,pdf}
  docs/thesis/figures/fig_5-3-2a_cross_arm.{tex,pdf}
  docs/thesis/tables/tab_5-3-1a_conditions.tex
  docs/thesis/tables/tab_5-3-2a_orderings.tex
  docs/thesis/tables/tab_5-3-3a_lineage.tex
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (CNAME, DEFENDED, FONT, LABEL, LONG, MARK, PREAMBLE, PROFILES,  # noqa: E402
                        REPO, SCHEMES, SHIELD, SHORT, SINGLES, TAB_DIR, UNREPORTED, axes, compile_fig, errorbar,
                        fmt_thousands, marker, panel_letter, pm, write_fig)

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers.json"
STEM_F55 = "fig_5-3-1a_suppression_profiles"
STEM_F56 = "fig_5-3-2a_cross_arm"
STEM_T55 = "tab_5-3-1a_conditions"
STEM_T56 = "tab_5-3-2a_orderings"
STEM_T57 = "tab_5-3-3a_lineage"
INTERVALS = ("200", "2000")
# Table 5.4 at one interval (2026-09-25, results context §8j, Q13): the
# interval lines carry the sweep, the table the other metrics at the interval
# MTDShield was trained at; the six-interval grid goes to an appendix table.
TAB55_INTERVALS = ("200",)
# the execution-scheme columns: random and alternative over the seven, then
# MTDShield's matched control and MTDShield (2026-09-25)
PANEL_SCHEMES = SCHEMES + SHIELD
CONDS = DEFENDED + SHIELD
# tick names for the singles, the full names of Table 2.2 (three lines for the two
# topology shuffles, Marc 2026-09-24: "they should be shuffle, that's the full name");
# was two-line (scrutinise-figure pass 2026-09-22,
# results context §8h: "topology" / "host" were ambiguous between the two
# topology shuffles; Table 2.4's names, split over two lines to fit the slot)
TICK = {
    "ip_shuffle": r"\shortstack{IP\\shuffle}", "complete_topology": r"\shortstack{complete\\topology\\shuffle}",
    "host_topology": r"\shortstack{host\\topology\\shuffle}", "port_shuffle": r"\shortstack{port\\shuffle}",
    "user_shuffle": r"\shortstack{user\\shuffle}", "os_diversity": r"\shortstack{OS\\diversity}",
    "service_diversity": r"\shortstack{service\\diversity}",
    "random_four": r"\shortstack{random,\\MTDShield's\\four}",
}
# the singles panel is grouped by the layer each mechanism rewrites (Table
# 2.4's "what to move" column; Marc's ruling 2026-09-22: brackets under the
# ticks), so its x order is the layer order, not Table 2.4's row order
PANEL_SINGLES = ("ip_shuffle", "complete_topology", "host_topology",
                 "port_shuffle", "os_diversity", "service_diversity", "user_shuffle")
LAYER = {"ip_shuffle": "host layer", "complete_topology": "host layer", "host_topology": "host layer",
         "port_shuffle": "service layer", "os_diversity": "service layer", "service_diversity": "service layer",
         "user_shuffle": "credentials"}


# --- the grouped-bar 2 x 2 shared by Fig. 5.5 and Fig. 5.6 --------------------


def _yrange(values: list[float]) -> tuple[float, float]:
    lo = min(0.0, min(values))
    hi = max(values)
    ymin = -0.2 if lo < -0.05 else 0.0
    if lo < -0.2:
        ymin = -0.4
    ymax = 1.0 if hi > 0.8 else 0.8
    return ymin, ymax


def grouped_panels(series: list[tuple[str, str, bool]], get, *, key_title: str, key_labels: dict,
                   sup_key=lambda blk, s, c: blk) -> tuple[str, list]:
    """``series``: (name, colour name, hatched). ``get(interval, name, cond)``
    -> (point, lo, hi). Four panels, y shared: (a) and (b) the single
    mechanisms at each interval, full width; (c) and (d) the execution schemes
    at each interval, side by side; one key.

    Restacked 2026-09-25 from the 2 x 2 (interval rows x singles | schemes
    columns): with MTDShield and its matched control the schemes panel holds
    four conditions, and eleven slots across one row leave ~1.2 cm per tick,
    under the measured widths of "alternative" (1.5 cm) and "MTDShield"
    (1.6 cm) at the figure face.
    """
    allv = [v for i in INTERVALS for s, _, _ in series for c in CONDS for v in get(i, s, c)]
    ymin, ymax = _yrange(allv)
    PH = 2.05  # panel height; kept from the 2 x 2 so the bars keep their scale
    XS0, XS1 = 1.3, 15.8                      # singles panels, full width
    XC = ((1.3, 8.3), (8.8, 15.8))            # the two schemes panels
    KY = 0.25                                  # key baseline
    YC = KY + 1.55                             # schemes row: three-line ticks + key below
    YS = (YC + PH + 2.3 + PH + 0.95, YC + PH + 2.3)   # singles rows: 200 s over 2 000 s
    n_s = len(series)
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    facts = []
    yticks_v = [round(v, 2) for v in [ymin + k * 0.2 for k in range(int(round((ymax - ymin) / 0.2)) + 1)]]
    # (letter, interval, conditions, x0, x1, y0, ticks drawn, y labels, title)
    panels = [
        ("a", INTERVALS[0], PANEL_SINGLES, XS0, XS1, YS[0], False, True,
         "single mechanisms, every %s\\,s" % fmt_thousands(int(INTERVALS[0]))),
        ("b", INTERVALS[1], PANEL_SINGLES, XS0, XS1, YS[1], True, True,
         "single mechanisms, every %s\\,s" % fmt_thousands(int(INTERVALS[1]))),
    ] + [
        (letter, interval, PANEL_SCHEMES, x0, x1, YC, True, col == 0,
         "execution schemes, every %s\\,s" % fmt_thousands(int(interval)))
        for col, (letter, interval, (x0, x1)) in enumerate(zip("cd", INTERVALS, XC))
    ]
    for letter, interval, conds, x0, x1, y0, ticked, ylab, title in panels:
        y1 = y0 + PH

        def yv(v, y0=y0):
            return y0 + (v - ymin) / (ymax - ymin) * PH

        slot = (x1 - x0) / len(conds)
        bw = min(0.22, slot * 0.8 / n_s)
        xt = [(c, x0 + (i + 0.5) * slot) for i, c in enumerate(conds)]
        axes(w, x0, x1, y0, y1,
             xticks=[(TICK.get(c, SHORT[c]), x) for c, x in xt] if ticked else [],
             yticks=[(v, yv(v)) for v in yticks_v],
             xlabel="", ylabel=("NCR reduction" if ylab else ""),
             ylabels=ylab, xfmt=lambda v: v, yfmt=lambda v: f"{v:.1f}", ylabel_offset=0.85)
        if not ticked:
            for c, x in xt:
                w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, y0, x, y0 - 0.07))
        if ymin < 0:
            w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, yv(0), x1, yv(0)))
        panel_letter(w, x0 - (1.25 if ylab else 0.5), y1 + 0.02, letter)
        # "execution schemes", never bare "scheme" (the §5 Never list, 2026-09-22)
        w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {%s};" % (x0 + 0.05, y1 + 0.04, title))
        for c, x in xt:
            for j, (name, cname, hatched) in enumerate(series):
                point, lo, hi = get(interval, name, c)
                xl = x - n_s * bw / 2 + j * bw
                ytop, ybot = yv(max(point, 0)), yv(min(point, 0))
                if hatched:
                    w(r"\fill[pattern=north east lines,pattern color=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (cname, xl, ybot, xl + bw - 0.02, ytop))
                    w(r"\draw[%s,line width=0.3pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (cname, xl, ybot, xl + bw - 0.02, ytop))
                else:
                    w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (cname, xl, ybot, xl + bw - 0.02, ytop))
                errorbar(w, xl + (bw - 0.02) / 2, yv(max(ymin, lo)), yv(min(ymax, hi)), col="black!70", cap=0.035)
                facts.append((interval, name, c, point, lo, hi))
    # layer brackets under the singles' ticks (Marc, 2026-09-22): one grey
    # bracket and label per contiguous layer group in PANEL_SINGLES
    slot = (XS1 - XS0) / len(PANEL_SINGLES)
    yb = YS[1] - 1.39   # under three-line ticks (the full names, Marc 2026-09-24)
    i = 0
    while i < len(PANEL_SINGLES):
        j = i
        while j + 1 < len(PANEL_SINGLES) and LAYER[PANEL_SINGLES[j + 1]] == LAYER[PANEL_SINGLES[i]]:
            j += 1
        xa, xb = XS0 + i * slot + 0.12, XS0 + (j + 1) * slot - 0.12
        w(r"\draw[black!50,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);" % (
            xa, yb + 0.08, xa, yb, xb, yb, xb, yb + 0.08))
        w(r"\node[anchor=north,text=black!60] at (%.3f,%.3f) {%s};" % ((xa + xb) / 2, yb - 0.03, LAYER[PANEL_SINGLES[i]]))
        i = j + 1
    # key, once, below; entries wrap inside the panel span so five profile
    # names never run past the page box (the 16.4 cm trap of 2026-09-17)
    ky = KY
    kx = XS0
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {%s};" % (kx, ky, key_title))
    xx = kx + 2.3   # 1.9 ran "attack profile" into the first swatch

    for name, cname, hatched in series:
        width = 0.52 + 0.165 * len(key_labels[name]) + 0.45  # ~0.165 cm per character at footnotesize helvet (2026-09-22: 0.115 overlapped)
        if xx + width > XS1:
            xx, ky = kx + 2.3, ky - 0.4
        if hatched:
            w(r"\fill[pattern=north east lines,pattern color=%s] (%.3f,%.3f) rectangle ++(0.42,0.22);" % (cname, xx, ky - 0.11))
            w(r"\draw[%s,line width=0.3pt] (%.3f,%.3f) rectangle ++(0.42,0.22);" % (cname, xx, ky - 0.11))
        else:
            w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.42,0.22);" % (cname, xx, ky - 0.11))
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (xx + 0.52, ky, key_labels[name]))
        xx += width
    # no formula line under the panels (2026-09-22): Table 5.2 defines
    # suppression and the caption decodes the whisker; the corpus carries no
    # chart-text key of this kind (figure_table_conventions.md §b2, §d)
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n", facts


def emit_fig55(s541: dict) -> tuple[str, list]:
    def get(interval, p, c):
        d = s541["by_interval"][interval]["per_profile"][p][c]
        return d["point"], d["lo"], d["hi"]
    return grouped_panels([(p, CNAME[p], False) for p in PROFILES], get,
                          key_title="attack profile", key_labels={p: LABEL[p] for p in PROFILES})


def emit_fig56(s542: dict) -> tuple[str, list]:
    def get(interval, arm, c):
        d = s542["by_interval"][interval]["suppression"][arm][c]
        return d["point"], d["lo"], d["hi"]
    return grouped_panels([("baseline", "cbase", True), ("movement", "cmov", False)], get,
                          key_title="attacker", key_labels={"baseline": LABEL["baseline"], "movement": LABEL["movement"]})


# --- tables ---------------------------------------------------------------------


def pm_ncr(iv: dict) -> str:
    """Hosts compromised as the network compromise ratio (Table 5.2): over the 50 hosts."""
    return pm({"mean": iv["mean"] / 50, "ci95": iv["ci95"] / 50}, 2)


def _sup(d: dict, nd: int = 2) -> str:
    # bounds in math mode so a negative bound prints a minus, not a hyphen
    # (context critic, 2026-09-22); a value that rounds to zero prints no sign
    # (2026-09-25: "-0.00" in OS diversity's bracket)
    f = lambda v: ("%.*f" % (nd, v)).replace("-0." + "0" * nd, "0." + "0" * nd)  # noqa: E731
    return "$%s$ [$%s$, $%s$]" % (f(d["point"]), f(d["lo"]), f(d["hi"]))


def emit_tab55(s541: dict) -> str:
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_effectiveness_figures.py from")
    w("%   data/results/ch5_defended/numbers.json (the defended corpus; the movement")
    w("%   attacker pooled over its four profiles). Do not hand-edit.")
    w("% REWORKED 2026-09-22 (scrutinise-figure pass, results context §8h): caption")
    w("%   decode-only and pointing at Table 5.2; footnote folded into it; dagger on")
    w("%   the UPPER row of an unseparated adjacent pair, then REMOVED the same day on")
    w("%   Marc's ruling (the printed intervals carry the overlap; the body text names")
    w("%   the separated pairs from numbers.json overlapping_adjacent); scriptsize with")
    w("%   4 pt colsep (conventions §k1). DRAFT STATE --- ratify on read.")
    w("% REWORKED 2026-09-25 (Marc: accepted 1 and 2): columns in Table 4.3's order")
    w("%   under its two class headers, attack outcome (ASP, NCR, MTTC) then MTD")
    w("%   effectiveness (NCR reduction, attack actions blocked); the no-host-compromised")
    w("%   column, which is no metric, folded into the MTTC cell as the share of runs")
    w("%   MTTC is taken over. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[Defence conditions against the APT attacker model]{Each defence condition against the APT attacker model pooled over $c_1$ to $c_4$, deployed every %s\,s, on the attack-outcome and MTD-effectiveness metrics of Table~\ref{tab:metrics}, ordered by NCR reduction; the first row is the no-defence reference. MTTC is over the runs that compromise a host, and its parenthesis is their share of all runs. Brackets: a 95\,\%% percentile bootstrap interval; $\pm$: a 95\,\%% interval on the mean (normal approximation).}" % fmt_thousands(int(TAB55_INTERVALS[0])))
    w(r"  \label{tab:eff-conditions}")
    # widths fill \textwidth (455.24 pt) at 4 pt colsep: 14.28 cm of columns +
    # 6 interior gutters at 8 pt + the rotated key. Two header rows: the
    # stripes restart at row 3 so the first body row is shaded and neither
    # header row is (as tab:eff-orderings).
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{4pt}\rowcolors{3}{black!5}{}")
    w(r"  \begin{tabular}{@{}cP{3.5cm}>{\centering\arraybackslash}p{1.3cm}>{\centering\arraybackslash}p{1.7cm}>{\centering\arraybackslash}p{2.6cm}>{\centering\arraybackslash}p{2.8cm}>{\centering\arraybackslash}p{2.08cm}@{}}")
    w(r"    \toprule")
    w(r"    & & \multicolumn{3}{c}{Attack outcome} & \multicolumn{2}{c}{MTD effectiveness} \\")
    w(r"    \cmidrule(lr){3-5}\cmidrule(lr){6-7}")
    w(r"    & Condition & ASP & NCR & MTTC (s) & NCR reduction & Attack actions blocked \\")
    w(r"    \midrule")

    def mttc(dl):
        # MTTC over the runs that compromise a host, with their share of all runs
        if not dl["observed"]:
            return "---"
        return r"%s (%d\,\%%)" % (pm(dl["observed"], 0), round(100 * (1 - dl["censored_share"])))

    marks = {}
    for interval in TAB55_INTERVALS:
        blk = s541["by_interval"][interval]
        pooled = blk["pooled"]
        none = pooled["none"]
        if interval == TAB55_INTERVALS[0]:
            # pooled no-defence target reach: the four profiles' cells are equal-sized
            four = [q for q in blk["per_profile"] if q != "aggregate"]
            none_tr = sum(blk["per_profile"][q]["none"]["target_reach"] for q in four) / len(four)
            w("    & no defence & %.2f & %s & %s & --- & %s \\\\" % (
                none_tr, pm_ncr(none["hosts"]), mttc(none["delay"]), pm(none["blocked"], 2)))
            w(r"    \midrule")
        rows = [(c, pooled[c]) for c in blk["order_pooled"] if c not in UNREPORTED]
        for i, (c, d) in enumerate(rows):
            # one interval since 2026-09-25: the caption names it, so no rotated
            # group label (context critic: it repeated the caption)
            group = r"\rowgroup{%d}{every %s\,s}" % (len(rows), fmt_thousands(int(interval))) if (
                i == len(rows) - 1 and len(TAB55_INTERVALS) > 1) else ""
            w("    %s & %s & %.2f & %s & %s & %s & %s \\\\" % (
                group, LONG[c], d["target_reach"], pm_ncr(d["hosts_cond"]), mttc(d["delay"]),
                _sup(d), pm(d["blocked"], 2)))
        w(r"    \midrule" if interval != TAB55_INTERVALS[-1] else r"    \bottomrule")
        marks[interval] = blk["overlapping_adjacent"]
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def emit_tab56(s542: dict) -> str:
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_effectiveness_figures.py from")
    w("%   data/results/ch5_defended/numbers.json (the defended corpus; suppression of")
    w("%   hosts reached per condition per arm; the model pooled over four profiles). Do not hand-edit.")
    w("% REWORKED 2026-09-25 (Marc; register E7): the APT attacker model is the base ---")
    w("%   its columns first, rows in its rank order; the footnote and its two")
    w("%   statistics gone (Marc: they do not fit here); caption decode-only; type")
    w("%   size and colsep as Table 5.4, filling \\textwidth. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[The defence ranking under each attacker]{The defence conditions ranked by NCR reduction against the APT attacker model and against the baseline attacker, at each deployment interval, in the APT attacker model's order; rank~1 is the largest reduction. Brackets: a 95\,\% percentile bootstrap interval.}")
    w(r"  \label{tab:eff-orderings}")
    # type size and colsep as tab:eff-conditions (conventions §k rule 1);
    # widths fill \textwidth (455.24 pt): 3.5 + 2 x (3.6 + 1.75) cm of columns
    # + 5 interior gutters at 8 pt + the rotated key. Two header rows: the
    # stripes restart at row 3 so the first body row is shaded and neither
    # header row is.
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{4pt}\rowcolors{3}{black!5}{}")
    w(r"  \begin{tabular}{@{}cP{3.5cm}>{\centering\arraybackslash}p{3.6cm}>{\centering\arraybackslash}p{1.75cm}>{\centering\arraybackslash}p{3.6cm}>{\centering\arraybackslash}p{1.75cm}@{}}")
    w(r"    \toprule")
    w(r"    & & \multicolumn{2}{c}{APT attacker model} & \multicolumn{2}{c}{Baseline attacker} \\")
    w(r"    \cmidrule(lr){3-4}\cmidrule(lr){5-6}")
    w(r"    & Condition & NCR reduction & Rank & NCR reduction & Rank \\")
    w(r"    \midrule")
    for interval in INTERVALS:
        blk = s542["by_interval"][interval]
        order = sorted(CONDS, key=lambda c: blk["ranks"]["movement"][c])
        for i, c in enumerate(order):
            group = r"\rowgroup{%d}{every %s\,s}" % (len(order), fmt_thousands(int(interval))) if i == len(order) - 1 else ""
            b, m = blk["suppression"]["baseline"][c], blk["suppression"]["movement"][c]
            w("    %s & %s & %s & %d & %s & %d \\\\" % (
                group, LONG[c], _sup(m), blk["ranks"]["movement"][c], _sup(b), blk["ranks"]["baseline"][c]))
        w(r"    \midrule" if interval == INTERVALS[0] else r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


# (claim key, claim text, source, family a, family b, named-pair key or None).
# Zhang's and Brown's claims are as attributed in the chapter's design record
# and are not carried as result rows in the extractions (handoff Q5): marked
# to verify. Ho's is ho2024.md "Headline findings" §4.3: diversity over
# shuffling by up to 140 % on the hybrid metric, OS Diversity against IP
# Shuffle, at interval 200 — so it is read at 200 s, the same tempo as Zhang's,
# and the two published directions are opposite.
CLAIMS = [
    ("zhang_shuffle_over_diversity_200",
     r"shuffling suppresses more than diversification (single mechanisms, 200\,s)",
     r"\citep{zhang2023}\textsuperscript{v}", "shuffle", "diversity", None),
    ("brown_best_single_vs_best_scheme_200",
     r"the best single mechanism roughly equals the best combination (200\,s)",
     r"\citep{brown2023}\textsuperscript{v}", "best single", "best scheme", None),
    ("ho_diversity_over_shuffle_200",
     r"diversification suppresses more than shuffling, OS diversity against IP shuffle in particular (200\,s)",
     r"\citep{ho2024}", "diversity", "shuffle", "ho_os_over_ip_200"),
]


def _direction(cl: dict, a_name: str, b_name: str, claim_key: str, pair: dict | None = None) -> tuple[str, str]:
    if claim_key.startswith("brown"):
        # the claim is about the best of each set, so the best-against-best
        # points decide it, not the set means
        if cl["best_intervals_overlap"]:
            verdict = "equal within intervals"
        else:
            verdict = "%s higher" % (a_name if cl["best_a_sup"]["point"] > cl["best_b_sup"]["point"] else b_name)
        detail = "%s %.2f; %s %.2f" % (LONG[cl["best_a"]], cl["best_a_sup"]["point"], LONG[cl["best_b"]], cl["best_b_sup"]["point"])
        return verdict, detail
    a_first = cl["direction"] == "a > b"
    verdict = "%s higher" % (a_name if a_first else b_name)
    detail = "family means %s %.2f, %s %.2f" % ((a_name, cl["mean_a"], b_name, cl["mean_b"]) if a_first
                                              else (b_name, cl["mean_b"], a_name, cl["mean_a"]))
    if pair is not None:
        detail += "; %s %.2f, %s %.2f%s" % (LONG[pair["best_a"]], pair["best_a_sup"]["point"],
                                           LONG[pair["best_b"]], pair["best_b_sup"]["point"],
                                           ", not separated" if pair["best_intervals_overlap"] else "")
    return verdict, detail


def emit_tab57(s543: dict) -> tuple[str, list]:
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_effectiveness_figures.py from")
    w("%   data/results/ch5_defended/numbers.json §s543 (the lineage arm: the same")
    w("%   matrix under the general attack scenario). Do not hand-edit.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[Prior evaluations' headline findings under both attackers]{Each headline comparison reported by the earlier evaluations built on this simulator, re-run here under both attackers at the lineage's general attack scenario, one row per claim: the published direction, the direction this simulator returns under the baseline attacker, and the direction under the APT attacker model. Because the configurations rather than the published numbers are reproduced, cells are read as agreement or disagreement in direction and never as a numerical replication, and the footnote states that boundary. The intention is to make published claims testable rather than merely cited, and to show that where they disagree with one another the disagreement is itself the finding.}")
    w(r"  \label{tab:eff-lineage}")
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"  \begin{tabular}{@{}P{4.6cm}P{1.8cm}P{3.2cm}P{3.2cm}P{2.1cm}@{}}")
    w(r"    \toprule")
    w(r"    Published claim & Source & Baseline attacker & APT attacker model & Agreement in direction \\")
    w(r"    \midrule")
    facts = []
    for key, claim, source, a_name, b_name, pair_key in CLAIMS:
        pb = s543["claims"]["baseline"].get(pair_key) if pair_key else None
        pm_ = s543["claims"]["movement"].get(pair_key) if pair_key else None
        vb, db = _direction(s543["claims"]["baseline"][key], a_name, b_name, key, pb)
        vm, dm = _direction(s543["claims"]["movement"][key], a_name, b_name, key, pm_)
        published = a_name if not key.startswith("brown") else "equal"
        agree_b = (vb.startswith(published) or (published == "equal" and vb.startswith("equal")))
        agree_m = (vm.startswith(published) or (published == "equal" and vm.startswith("equal")))
        agreement = {(True, True): "both agree", (True, False): "inherited only", (False, True): "model only", (False, False): "neither"}[(agree_b, agree_m)]
        if pair_key:
            pair_sep = [arm for arm, pr in (("inherited", pb), ("model", pm_)) if pr and not pr["best_intervals_overlap"]
                        and (pr["direction"] == "a > b")]
            agreement += " on the family; on the pair " + ("neither" if not pair_sep else " and ".join(pair_sep) + " only")
        w("    %s & %s & %s (%s) & %s (%s) & %s \\\\" % (claim, source, vb, db, vm, dm, agreement))
        facts.append((key, vb, db, vm, dm, agreement))
    w(r"    \bottomrule")
    w(r"    \addlinespace[2pt]")
    w(r"    \multicolumn{5}{@{}p{0.96\textwidth}@{}}{\scriptsize Direction is read on NCR reduction ($1 - $ hosts / hosts with no defence, on cell means) over the seven single mechanisms and the two schemes, 100 seeds per cell, the model pooled over its four profiles; ``higher'' means the family's mean suppression is larger, and where the source names a pair the pair is read beside the family. The published evaluations reported mean time to compromise, or a composite of it, on a different network, pool and horizon, so no cell here is a numerical replication: only the direction of each comparison is compared. \textsuperscript{v}~the claim as attributed in the chapter's design record; the source's own statement of it is to be verified against the paper before submission.}\\")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n", facts


# --- main ------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--only", default=None, help="fig55 | fig56 | tab55 | tab56 | tab57")
    args = ap.parse_args()
    data = json.loads(args.numbers.read_text(encoding="utf-8"))
    if not data["sanity"]["all_cells_100"] or data["sanity"]["error_rows"] or "shield" not in data:
        raise SystemExit("corpus sanity failed; not drawing from it")
    TAB_DIR.mkdir(parents=True, exist_ok=True)
    want = lambda k: args.only is None or args.only == k  # noqa: E731

    if want("fig55"):
        tex, facts = emit_fig55(data["s541"])
        write_fig(STEM_F55, tex.splitlines())
        print("Fig. 5.5 facts (interval, profile, condition, point, lo, hi):")
        for f in facts:
            print("   %s %-30s %-18s %+.3f [%+.3f, %+.3f]" % f)
        if not args.no_compile:
            compile_fig(STEM_F55)
    if want("fig56"):
        tex, facts = emit_fig56(data["s542"])
        write_fig(STEM_F56, tex.splitlines())
        print("Fig. 5.6 facts (interval, arm, condition, point, lo, hi):")
        for f in facts:
            print("   %s %-10s %-18s %+.3f [%+.3f, %+.3f]" % f)
        for i in INTERVALS:
            sp = data["s542"]["by_interval"][i]["spearman"]
            print(f"   rho @ {i}: {sp['rho']:.3f} [{sp['lo']:.3f}, {sp['hi']:.3f}]  top: {data['s542']['by_interval'][i]['top']}")
        if not args.no_compile:
            compile_fig(STEM_F56)
    if want("tab55"):
        (TAB_DIR / f"{STEM_T55}.tex").write_text(emit_tab55(data["s541"]))
        print(f"wrote tables/{STEM_T55}.tex")
    if want("tab56"):
        (TAB_DIR / f"{STEM_T56}.tex").write_text(emit_tab56(data["s542"]))
        print(f"wrote tables/{STEM_T56}.tex")
    if want("tab57"):
        tex, facts = emit_tab57(data["s543"])
        (TAB_DIR / f"{STEM_T57}.tex").write_text(tex)
        print(f"wrote tables/{STEM_T57}.tex")
        for f in facts:
            print("   ", f)


if __name__ == "__main__":
    main()
