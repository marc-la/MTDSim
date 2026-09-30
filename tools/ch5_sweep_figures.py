#!/usr/bin/env python3
"""Chapter 5 §5.3.2-§5.3.3 line charts: NCR reduction against the deployment
interval (Jin's second pass, relayed by Marc 2026-09-25; design brief in
docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md §8j; spec in
docs/handoffs/2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md
§5.4 and §5.8). They replace the grouped bars of Figures 5.4 and 5.5.

  headline  §5.3.2  one panel per defence, the two attackers its two lines
                    (the APT attacker model pooled over c_1-c_4 solid, the
                    baseline attacker dashed grey, as in the depth figures):
                    the layers (host, service, credentials) over the deployment
                    strategies (random, alternative, MTDShield). Redrawn
                    2026-09-25 on Marc's read of the first draft ("the effect
                    of the attacker model it's not very clear to me"): the
                    attackers were one per column, so the swap had to be read
                    across panels; now it is which line is on top.
  mechanisms §5.3.3 the seven mechanisms, one panel each, rows by layer;
                    lines c_1-c_4 and c_agg in the chapter's hues, the baseline
                    attacker the dashed grey reference
  schemes   §5.3.3  the deployment strategies, the same form, 1 x 3
  values    §5.3.2  Table 5.3: NCR reduction per defence, attacker and interval,
                    the numbers behind the headline (replaces the rank grid:
                    Marc 2026-09-25, "the rankings ... what they mean to me")

Every panel of the three figures shares one y range and the same log x axis
at the corpus's intervals. Data: ``numbers.json["sweep"]`` from
``data/results/ch5_defended/analyse.py``; nothing is typed here, and every
drawn point is printed on stdout.

Usage:
  python tools/ch5_sweep_figures.py [--numbers PATH] [--no-compile] [--only headline|mechanisms|schemes|values]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (BASE_DASH, CNAME, FONT, KEY_H, LABEL, LONG, MARK, PREAMBLE, PROFILES, REPO,  # noqa: E402
                        TAB_DIR, TITLE_H, UNREPORTED, compile_fig, fmt_thousands, key_row, marker,
                        panel_title, write_fig)

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers.json"
STEM_HEAD = "fig_5-3-2b_interval_headline"
STEM_MECH = "fig_5-3-3b_interval_mechanisms"
STEM_SCH = "fig_5-3-3c_interval_schemes"
STEM_VAL = "tab_5-3-2c_attacker_values"
ROWS_MECH = (("host layer", ("ip_shuffle", "complete_topology", "host_topology")),
             ("service layer", ("port_shuffle", "os_diversity", "service_diversity")),
             ("credentials", ("user_shuffle",)))
def _cap(t: str) -> str:
    """Sentence case for a panel title: the first letter up, the rest as named."""
    return t[:1].upper() + t[1:]


STRATEGIES = tuple(c for c in ("random", "alternative", "random_four", "mtdshield") if c not in UNREPORTED)
ACCENT = "31,84,140"
HEAD_STRATEGIES = tuple(c for c in ("random", "mtdshield", "alternative") if c in STRATEGIES)
# the headline's panels: (kind in numbers, key, title), rows layers | strategies
HEAD_ROWS = (("Defence mechanisms, by the layer they rewrite",
              (("layer", "host", "Host layer"), ("layer", "service", "Service layer"),
               ("layer", "credentials", "Credentials: user shuffle"))),
             # MTDShield under the service layer, random under the host layer,
             # so the panels that share a shape share a column (context critic,
             # 2026-09-25 round 2)
             ("Deployment strategies",
              tuple(("attacker", c, _cap(LONG[c])) for c in HEAD_STRATEGIES)))
# the two attackers; the APT attacker model pooled is black, not the chapter's
# movement blue, which is c_1's colour and marker in the depth figures below it
# (context critic, 2026-09-25: the pooled line read as c_1); the baseline as the
# depth figures draw it
ARMS = (("movement", "black", "circle", False), ("baseline", "cbase", "square", True))
# the figure-wide key, one row at the top of every sweep figure (conventions §o)
ARM_KEY = ((LABEL["movement"] + r" (pooled over $c_1$ to $c_4$)", "line", "black", "circle"),
           ("baseline attacker", "dashed", "cbase", "square"))
PROFILE_KEY = tuple((LABEL[p], "line", CNAME[p], MARK[p]) for p in PROFILES) + (
    ("baseline attacker", "dashed", "cbase", "square"),)


def _yrange(values) -> tuple[float, float]:
    """The shared y range: the lowest whisker rounded down to a 0.2 step (so
    no whisker is clipped and the floor tightens as the intervals narrow), and
    1.0 at the top."""
    lo, hi = min(0.0, min(values)), max(values)
    return math.floor(round(lo / 0.2, 6)) * 0.2, (1.0 if hi > 0.8 else 0.8)


class Panel:
    """One line-chart panel: log x over the corpus's intervals, linear y."""

    def __init__(self, w, x0, x1, y0, y1, ivs, yr, *, xlabels=True, ylabels=True, title=None,
                 letter=None, font=FONT, tickfont=None):
        self.w, self.x0, self.x1, self.y0, self.y1 = w, x0, x1, y0, y1
        self.ivs, (self.ymin, self.ymax) = ivs, yr
        pad = 0.07 * math.log10(ivs[-1] / ivs[0]) if len(ivs) > 1 else 0.5
        self.l0, self.l1 = math.log10(ivs[0]) - pad, math.log10(ivs[-1]) + pad
        w(r"\begin{scope}[every node/.style={inner sep=1pt,font=%s}]" % font)
        w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, y0, x1, y0))
        w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, y0, x0, y1))
        k = 0
        while self.ymin + k * 0.2 <= self.ymax + 1e-9:
            v = round(self.ymin + k * 0.2, 2)
            y = self.yv(v)
            w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0 - 0.07, y, x0, y))
            if abs(v) > 1e-9 and abs(y - y0) > 1e-6:
                w(r"\draw[black!12,line width=0.2pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, y, x1, y))
            if ylabels:
                w(r"\node[anchor=east] at (%.3f,%.3f) {%s};" % (x0 - 0.1, y, ("%.1f" % v).replace("-", "$-$")))
            k += 1
        if self.ymin < 0:  # zero is the no-MTD reference
            w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, self.yv(0), x1, self.yv(0)))
        for iv in ivs:
            x = self.xv(iv)
            w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, y0, x, y0 - 0.07))
            if xlabels:
                w(r"\node[anchor=north%s] at (%.3f,%.3f) {%s};" % (
                    ",font=" + tickfont if tickfont else "", x, y0 - 0.1, fmt_thousands(iv)))
        if title:
            panel_title(w, x0, y1, title, letter)
        w(r"\end{scope}")

    def xv(self, iv, dx=0.0) -> float:
        return self.x0 + (math.log10(iv) + dx - self.l0) / (self.l1 - self.l0) * (self.x1 - self.x0)

    def yv(self, v) -> float:
        v = min(max(v, self.ymin), self.ymax)
        return self.y0 + (v - self.ymin) / (self.ymax - self.ymin) * (self.y1 - self.y0)

    def line(self, pts, col, mark, dashed, *, dx=0.0, whiskers=True, lw=0.7, r=0.06):
        """``pts``: [(interval, point, lo, hi)]; ``dx`` a small offset in log10
        units so whiskers at one interval do not overprint."""
        w = self.w
        xy = [(self.xv(iv, dx), self.yv(p)) for iv, p, _, _ in pts]
        style = "%s,line width=%.2fpt%s" % (col, lw, "," + BASE_DASH if dashed else "")
        if len(xy) > 1:
            w(r"\draw[%s] %s;" % (style, " -- ".join("(%.3f,%.3f)" % q for q in xy)))
        for (iv, p, lo, hi), (x, y) in zip(pts, xy):
            if whiskers:
                w(r"\draw[%s,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x, self.yv(lo), x, self.yv(hi)))
            marker(w, mark, col, x, y, r=r)


def _pts(sweep, get):
    return [(int(i), *get(sweep["by_interval"][str(i)])) for i in sweep["intervals"]]


def _v(d):
    return d["point"], d["lo"], d["hi"]


def _all_points(sweep):
    vals = []
    for i in sweep["intervals"]:
        b = sweep["by_interval"][str(i)]
        for arm in ("movement", "baseline"):
            vals += [d[k] for d in b["attacker"][arm].values() for k in ("point", "lo")]
            vals += [d[k] for d in b["layer"][arm].values() for k in ("point", "lo")]
        for p in PROFILES:
            vals += [d[k] for d in b["profile"][p].values() for k in ("point", "lo")]
    return vals


def _preamble():
    return PREAMBLE + [r"\definecolor{accent}{RGB}{%s}" % ACCENT]


def _offsets(n, step):
    return [(j - (n - 1) / 2) * step for j in range(n)]


# --- the headline ---------------------------------------------------------------


def emit_headline(sweep, yr):
    L = _preamble()
    w = L.append
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    PW, GAP, X0 = 4.55, 0.42, 1.3
    PH = 3.0
    ROWH = PH + 1.55
    XR = X0 + 3 * PW + 2 * GAP
    facts = []
    letters = iter("abcdef")
    # the figure-wide key at the top, left edge on the first y-axis (conventions §o)
    key_row(w, X0, 0.6 + ROWH * len(HEAD_ROWS) + 0.35, ARM_KEY, xmax=XR)
    for r, (header, panels) in enumerate(HEAD_ROWS):
        y0 = 0.6 + (len(HEAD_ROWS) - 1 - r) * ROWH + 0.85
        w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {%s};" % (X0, y0 + PH + 0.5, header))
        w(r"\draw[black!25,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, y0 + PH + 0.48, XR, y0 + PH + 0.48))
        for k, (kind, key, title) in enumerate(panels):
            x0 = X0 + k * (PW + GAP)
            p = Panel(w, x0, x0 + PW, y0, y0 + PH, [int(i) for i in sweep["intervals"]], yr, ylabels=(k == 0),
                      title=title, letter=next(letters), tickfont=r"\scriptsize")
            for (arm, col, mark, dashed), dx in zip(ARMS, _offsets(len(ARMS), 0.016)):
                pts = _pts(sweep, lambda b, kind=kind, key=key, arm=arm: _v(b[kind][arm][key]))
                p.line(pts, col, mark, dashed, dx=dx, lw=0.9, r=0.06)
                facts += [(arm, key, *q) for q in pts]
        # one axis label per row, so it cannot cross the next row's header
        w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {NCR reduction};" % (X0 - 0.95, y0 + PH / 2))
    w(r"\node[anchor=north] at (%.3f,%.3f) {Deployment interval (s)};" % ((X0 + XR) / 2, 0.6 + 0.85 - 0.5))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return L, facts


# --- the depth: one panel per condition, profiles + the baseline attacker ------


def _profile_panel(w, sweep, cond, x0, x1, y0, y1, yr, *, ylabels, title, letter, font):
    ivs = [int(i) for i in sweep["intervals"]]
    # the small panels' interval ticks at scriptsize: 1 000 and 2 000 sit
    # ~0.75 cm apart on a 4.55 cm log axis and ran together at footnotesize
    p = Panel(w, x0, x1, y0, y1, ivs, yr, xlabels=True, ylabels=ylabels, title=title, letter=letter, font=font,
              tickfont=r"\scriptsize" if x1 - x0 < 5 else None)
    series = [(pr, CNAME[pr], MARK[pr], False) for pr in PROFILES] + [("baseline", "cbase", "square", True)]
    offs = _offsets(len(series), 0.014)
    facts = []
    for (name, col, mark, dashed), dx in zip(series, offs):
        if name == "baseline":
            pts = _pts(sweep, lambda b, c=cond: _v(b["attacker"]["baseline"][c]))
        else:
            pts = _pts(sweep, lambda b, c=cond, n=name: _v(b["profile"][n][c]))
        p.line(pts, col, mark, dashed, dx=dx, lw=0.6, r=0.05)
        facts += [(cond, name, *q) for q in pts]
    return facts


def emit_mechanisms(sweep, yr):
    L = _preamble()
    w = L.append
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    PW, GAP, X0 = 4.55, 0.42, 1.3
    PH = 3.0
    ROWH = PH + 1.55           # panel + ticks + title + layer header
    facts = []
    letters = iter("abcdefg")
    ytop = 1.0 + ROWH * len(ROWS_MECH)
    for r, (layer, conds) in enumerate(ROWS_MECH):
        y0 = ytop - (r + 1) * ROWH + 0.85
        w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {%s};" % (X0, y0 + PH + 0.5, _cap(layer)))
        w(r"\draw[black!25,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, y0 + PH + 0.48, X0 + 3 * PW + 2 * GAP, y0 + PH + 0.48))
        for k, c in enumerate(conds):
            x0 = X0 + k * (PW + GAP)
            facts += _profile_panel(w, sweep, c, x0, x0 + PW, y0, y0 + PH, yr, ylabels=(k == 0),
                                    title=_cap(LONG[c]), letter=next(letters), font=FONT)
    # the figure-wide key at the top, left edge on the first y-axis (conventions §o)
    key_row(w, X0, ytop + 0.35, PROFILE_KEY, xmax=X0 + 3 * PW + 2 * GAP)
    y0 = ytop - len(ROWS_MECH) * ROWH + 0.85
    w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {NCR reduction};" % (X0 - 0.95, (y0 + ytop) / 2))
    w(r"\node[anchor=north] at (%.3f,%.3f) {Deployment interval (s)};" % (X0 + 1.5 * PW + GAP, y0 - 0.5))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return L, facts


def emit_schemes(sweep, yr):
    """The deployment strategies in the mechanisms figure's form, one row."""
    L = _preamble()
    w = L.append
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    PW, GAP, X0 = 4.55, 0.42, 1.3
    PH = 3.0
    XR = X0 + 3 * PW + 2 * GAP
    y0 = 1.5
    facts = []
    letters = iter("abcdef")
    for k, c in enumerate(HEAD_STRATEGIES):  # the headline's order
        x0 = X0 + k * (PW + GAP)
        facts += _profile_panel(w, sweep, c, x0, x0 + PW, y0, y0 + PH, yr, ylabels=(k == 0),
                                title=_cap(LONG[c]), letter=next(letters), font=FONT)
    w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {NCR reduction};" % (X0 - 0.95, y0 + PH / 2))
    w(r"\node[anchor=north] at (%.3f,%.3f) {Deployment interval (s)};" % ((X0 + XR) / 2, y0 - 0.5))
    # the figure-wide key at the top, left edge on the first y-axis (conventions §o)
    key_row(w, X0, y0 + PH + TITLE_H + 0.1 + KEY_H / 2 + 0.2, PROFILE_KEY, xmax=XR)
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return L, facts


# --- Table 5.3: the numbers behind the headline ----------------------------------


# (header, layer key whose mean Figure 5.4 plots or None, rows)
VALUE_ROWS = (("host layer", "host", ("ip_shuffle", "complete_topology", "host_topology")),
              ("service layer", "service", ("port_shuffle", "os_diversity", "service_diversity")),
              ("credentials", None, ("user_shuffle",)),
              ("deployment strategies", None, HEAD_STRATEGIES))  # the panels' order
GREY = "black!55"  # survives a greyscale print (cold reader, 2026-09-25)


def _val(v: float) -> str:
    # a value that rounds to zero prints no sign
    t = "%.2f" % v
    return "$%s$" % ("0.00" if t == "-0.00" else t)


def emit_value_table(sweep) -> tuple[str, list]:
    """NCR reduction per defence, attacker and deployment interval; rows grouped
    as the headline's panels are (the layers, then the strategies); a cell
    whose 95 % interval includes zero is set grey."""
    ivs = [str(i) for i in sweep["intervals"]]
    n = len(ivs)
    L: list[str] = []
    w = L.append
    facts = []
    w("% GENERATED by tools/ch5_sweep_figures.py from data/results/ch5_defended/numbers.json")
    w("%   (section sweep; the APT attacker model pooled over its four profiles). Do not hand-edit.")
    w("% 2026-09-25 (Marc on the first draft: the rank grid's dashes and italics did not")
    w("%   read): the values themselves, grouped as Figure 5.4's panels. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[NCR reduction under each attacker, by defence and deployment interval]{NCR reduction for each defence against the APT attacker model, pooled over $c_1$ to $c_4$, and against the baseline attacker, at each deployment interval; 1 is no host compromised, 0 is as many as with no MTD, and a negative value is more hosts compromised than with no MTD. Rows grouped as the panels of Figure~\ref{fig:eff-cross-arm}; a layer's row gives the mean it plots. Grey text: the 95\,\% percentile bootstrap interval includes zero; the APT attacker model's cells pool four times as many runs as the baseline attacker's.}")
    w(r"  \label{tab:eff-interval-values}")
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}\rowcolors{1}{}{}")  # the groups' rules separate rows; zebra would stripe the headers
    w(r"  \begin{tabular}{@{}P{3.75cm}*{%d}{>{\centering\arraybackslash}p{0.78cm}}@{}}" % (2 * n))
    w(r"    \toprule")
    w(r"    & \multicolumn{%d}{c}{APT attacker model} & \multicolumn{%d}{c}{Baseline attacker} \\" % (n, n))
    w(r"    \cmidrule(lr){2-%d}\cmidrule(lr){%d-%d}" % (n + 1, n + 2, 2 * n + 1))
    w(r"    Deployment interval (s) & %s & %s \\" % (" & ".join(fmt_thousands(int(i)) for i in ivs),
                                                   " & ".join(fmt_thousands(int(i)) for i in ivs)))
    def cells_of(kind, key, fmt="%s"):
        out = []
        for arm in ("movement", "baseline"):
            for i in ivs:
                d = sweep["by_interval"][i][kind][arm][key]
                sep = d["lo"] > 0 or d["hi"] < 0
                out.append(fmt % (_val(d["point"]) if sep else r"\textcolor{%s}{%s}" % (GREY, _val(d["point"]))))
                facts.append((arm, key, int(i), d["point"], d["lo"], d["hi"], sep))
        return " & ".join(out)

    for header, layer, conds in VALUE_ROWS:
        w(r"    \midrule")
        if layer:  # the plotted mean on the layer's own row
            w(r"    \textit{%s, mean} & %s \\" % (header, cells_of("layer", layer)))
        else:
            w(r"    \multicolumn{%d}{@{}l}{\textit{%s}} \\" % (2 * n + 1, header))
        for c in conds:
            w("    \\quad %s & %s \\\\" % (LONG[c], cells_of("attacker", c)))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n", facts


# --- §5.3.2's table: both attackers ranked, all metrics, one interval -----------

STEM_RANKT = "tab_5-3-2d_attacker_ranking"
STEM_FULL = "tab_F-1_conditions_%s"      # the appendix tables, one per attacker
RANK_INTERVAL = "200"                    # MTDShield's training interval and the lineage's
N_HOSTS = 50                             # NCR = hosts compromised over the network's 50 (Table 5.2)


def _num(v: float, nd: int = 2) -> str:
    t = "%.*f" % (nd, v)
    return "$%s$" % ("0." + "0" * nd if t == "-0." + "0" * nd else t)


def _mttc(delay: dict) -> str:
    # MTTC over the runs that compromise a host, and their share of all runs
    if not delay["observed"]:
        return "---"
    return r"%s (%d)" % (fmt_thousands(delay["observed"]["mean"]), round(100 * (1 - delay["censored_share"])))


def _order(blk) -> list[str]:
    mv = blk["movement"]["rows"]
    return sorted(mv, key=lambda c: (mv[c]["rank"], -mv[c]["point"]))


def emit_ranking_table(ranking) -> tuple[str, list]:
    iv = RANK_INTERVAL if RANK_INTERVAL in ranking["by_interval"] else str(ranking["intervals"][0])
    blk = ranking["by_interval"][iv]
    order = _order(blk)
    facts = []
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_sweep_figures.py from data/results/ch5_defended/numbers.json")
    w("%   (section ranking; ranks by Scott-Knott ESD, data/results/ch5_defended/sk_esd.py). Do not hand-edit.")
    w("% 2026-09-25 (Marc: \"we have to have some ranks ... ranking with ties\"; results context §8j-4):")
    w("%   the two attackers side by side at one interval, all of Table 4.3's metrics. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[The defences ranked against each attacker]{Each defence deployed every %s\,s against the APT attacker model, pooled over $c_1$ to $c_4$, and against the baseline attacker, each ranked by Scott--Knott ESD on the mean hosts compromised per seed (Section~\ref{subsec:metrics-statistics}). Rank~1, in bold, is the fewest hosts compromised; defences that share a rank are not told apart; no MTD is not ranked. Rows in the APT attacker model's order. Metrics as Table~\ref{tab:metrics}; MTTC is over the runs that compromise a host, with their percentage of all runs in brackets. Every value's interval is in Appendix~\ref{app:supplementary-results}.}" % fmt_thousands(int(iv)))
    w(r"  \label{tab:eff-cross-arm}")
    # the stripes restart at row 4 so neither header row is shaded (as Table 5.4 was)
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{2.6pt}\rowcolors{4}{black!5}{}")
    C = r">{\centering\arraybackslash}p{%s}"
    # attack actions blocked cut from the metric set (Marc 2026-09-25), so both
    # attacker blocks carry the same five columns
    cols_m = [C % "0.62cm", C % "0.7cm", C % "0.7cm", C % "1.6cm", C % "1.15cm"]
    cols_b = cols_m
    w(r"  \begin{tabular}{@{}P{3.45cm}%s%s@{}}" % ("".join(cols_m), "".join(cols_b)))
    w(r"    \toprule")
    w(r"    & \multicolumn{5}{c}{APT attacker model} & \multicolumn{5}{c}{Baseline attacker} \\")
    w(r"    \cmidrule(lr){2-6}\cmidrule(lr){7-11}")
    head_m = ["Rank", "ASP", "NCR", "MTTC (s)", r"NCR\newline reduction"]
    w(r"    Defence & %s & %s \\" % (" & ".join(head_m), " & ".join(head_m)))
    w(r"    \midrule")

    def cells(arm, row, none=False):
        rank = "---" if none else (r"\textbf{1}" if row["rank"] == 1 else str(row["rank"]))
        out = [rank, "%.2f" % row["asp"], "%.2f" % (row["hosts"]["mean"] / N_HOSTS),
               _mttc(row["delay"]), "---" if none else _num(row["point"])]
        return out

    w("    no MTD & %s & %s \\\\" % (" & ".join(cells("movement", blk["movement"]["none"], True)),
                                         " & ".join(cells("baseline", blk["baseline"]["none"], True))))
    w(r"    \midrule")
    for c in order:
        m, b = blk["movement"]["rows"][c], blk["baseline"]["rows"][c]
        w("    %s & %s & %s \\\\" % (LONG[c], " & ".join(cells("movement", m)), " & ".join(cells("baseline", b))))
        facts.append((c, m["rank"], m["point"], b["rank"], b["point"]))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n", facts


def emit_full_table(ranking, arm) -> str:
    """The appendix table for one attacker: every metric with its interval, at
    the ranking interval, rows in that attacker's rank order."""
    iv = RANK_INTERVAL if RANK_INTERVAL in ranking["by_interval"] else str(ranking["intervals"][0])
    blk = ranking["by_interval"][iv][arm]
    order = sorted(blk["rows"], key=lambda c: (blk["rows"][c]["rank"], -blk["rows"][c]["point"]))
    who = (r"the APT attacker model, pooled over $c_1$ to $c_4$" if arm == "movement" else "the baseline attacker")
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_sweep_figures.py from data/results/ch5_defended/numbers.json (section ranking).")
    w("%   Do not hand-edit. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[Deployment strategies against %s, with intervals]{Each defence deployed every %s\,s against %s, with the rank of Table~\ref{tab:eff-cross-arm}, on the metrics of Table~\ref{tab:metrics}; the first row is the no-MTD reference. MTTC is over the runs that compromise a host, with their percentage of all runs in brackets. Brackets on NCR reduction: a 95\,\%% percentile bootstrap interval; $\pm$: a 95\,\%% interval on the mean (normal approximation).}" % (LABEL[arm], fmt_thousands(int(iv)), who))
    w(r"  \label{tab:full-%s}" % arm)
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{4pt}")
    C = r">{\centering\arraybackslash}p{%s}"
    extra = False  # attack actions blocked cut from the metric set (Marc 2026-09-25)
    w(r"  \begin{tabular}{@{}P{3.4cm}%s%s%s%s%s%s@{}}" % (C % "0.7cm", C % "1.0cm", C % "1.6cm", C % "2.8cm",
                                                        C % "2.9cm", (C % "1.9cm") if extra else ""))
    w(r"    \toprule")
    w(r"    Defence & Rank & ASP & NCR & MTTC (s) & NCR reduction%s \\" % (" & Attack actions blocked" if extra else ""))
    w(r"    \midrule")

    def pm(d, nd=2, scale=1.0):
        return r"$%.*f \pm %.*f$" % (nd, d["mean"] / scale, nd, d["ci95"] / scale)

    def mttc(delay):
        if not delay["observed"]:
            return "---"
        return r"$%s \pm %s$ (%d)" % (fmt_thousands(delay["observed"]["mean"]), fmt_thousands(delay["observed"]["ci95"]),
                                      round(100 * (1 - delay["censored_share"])))

    n = blk["none"]
    w("    no MTD & --- & %.2f & %s & %s & ---%s \\\\" % (n["asp"], pm(n["hosts"], scale=N_HOSTS), mttc(n["delay"]),
                                                         (" & " + pm(n["blocked"])) if extra else ""))
    w(r"    \midrule")
    for c in order:
        d = blk["rows"][c]
        red = r"%s [%s, %s]" % (_num(d["point"]), _num(d["lo"]), _num(d["hi"]))
        w("    %s & %d & %.2f & %s & %s & %s%s \\\\" % (LONG[c], d["rank"], d["asp"], pm(d["hosts"], scale=N_HOSTS),
                                                    mttc(d["delay"]), red, (" & " + pm(d["blocked"])) if extra else ""))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--only", default=None, help="headline | mechanisms | schemes | values | ranking")
    args = ap.parse_args()
    data = json.loads(args.numbers.read_text(encoding="utf-8"))
    if "sweep" not in data:
        raise SystemExit("numbers.json has no sweep section; run analyse.py")
    if "sanity" in data and (not data["sanity"]["all_cells_100"] or data["sanity"]["error_rows"]):
        raise SystemExit("corpus sanity failed; not drawing from it")
    sweep = data["sweep"]
    yr = _yrange(_all_points(sweep))
    print(f"intervals {sweep['intervals']}; shared y range {yr}")
    for name, stem, fn in (("headline", STEM_HEAD, emit_headline), ("mechanisms", STEM_MECH, emit_mechanisms),
                           ("schemes", STEM_SCH, emit_schemes)):
        if args.only and args.only != name:
            continue
        lines, facts = fn(sweep, yr)
        write_fig(stem, lines)
        print(f"{name} facts (series, key, interval, point, lo, hi):")
        for f in facts:
            print("   %-10s %-30s %5d %+.3f [%+.3f, %+.3f]" % f)
        if not args.no_compile:
            compile_fig(stem)
    if (not args.only or args.only == "ranking") and "ranking" in data:
        tex, facts = emit_ranking_table(data["ranking"])
        (TAB_DIR / f"{STEM_RANKT}.tex").write_text(tex)
        print(f"wrote tables/{STEM_RANKT}.tex (condition, APT rank, point, baseline rank, point):")
        for f in facts:
            print("   %-18s %2d %+.3f   %2d %+.3f" % f)
        for arm in ("movement", "baseline"):
            (TAB_DIR / f"{STEM_FULL % arm}.tex").write_text(emit_full_table(data["ranking"], arm))
            print(f"wrote tables/{STEM_FULL % arm}.tex")
    if not args.only or args.only == "values":
        tex, facts = emit_value_table(sweep)
        (TAB_DIR / f"{STEM_VAL}.tex").write_text(tex)
        print(f"wrote tables/{STEM_VAL}.tex (arm, condition, interval, point, lo, hi, separated):")
        for f in facts:
            print("   %-9s %-18s %5d %+.3f [%+.3f, %+.3f] %s" % f)


if __name__ == "__main__":
    main()
