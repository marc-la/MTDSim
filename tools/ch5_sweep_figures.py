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
                    NCR reduction in the top two rows, ASP reduction in the
                    bottom two (Marc 2026-09-30: the two headlines were one
                    figure drawn twice, so they are one figure)
  mechanisms §5.3.3 the seven mechanisms, one panel each, rows by layer, then
                    the deployment strategies as a fourth row (Marc 2026-09-30:
                    the strategies' own figure merged in); lines c_1-c_4 and
                    c_agg in the chapter's hues, the baseline attacker the
                    dashed grey reference
  values    App. F  NCR reduction and ASP reduction per defence, attacker and
                    interval, the numbers behind the headline, two tables in one
                    fragment (moved from §5.3.2 on Marc's 2026-09-30 ruling: the
                    body keeps the ranking table, whose 200 s column it repeated)

Every panel of the three figures shares one y range and the same log x axis
at the corpus's intervals. Data: ``numbers.json["sweep"]`` from
``data/results/ch5_defended/analyse.py``; nothing is typed here, and every
drawn point is printed on stdout.

Usage:
  python tools/ch5_sweep_figures.py [--numbers PATH] [--no-compile] [--only headline|mechanisms|values|ranking]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (bounded, mttc_dash_decode, mttc_unreported, BASE_DASH, CNAME, FONT, KEY_H, LABEL, LONG, MARK, PREAMBLE, PROFILES, REPO,  # noqa: E402
                        TAB_DIR, TITLE_H, UNREPORTED, compile_fig, fmt_thousands, key_row, marker,
                        panel_title, write_fig)

# the reported corpus (1 000 seeds, the vulnerability memory on; 2026-10-02)
NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers_reported.json"
STEM_HEAD = "fig_5-3-2b_interval_headline"
STEM_MECH = "fig_5-3-3b_interval_mechanisms"
STEM_VAL = "tab_F-0a_interval_values"
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
HEAD_ROWS = (("MTD mechanisms, by the layer they reconfigure",
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
ARM_KEY = ((LABEL["movement"], "line", "black", "circle"),
           ("baseline attacker", "dashed", "cbase", "square"))
PROFILE_KEY = tuple((LABEL[p], "line", CNAME[p], MARK[p]) for p in PROFILES) + (
    ("baseline attacker", "dashed", "cbase", "square"),)


# the headline metric's name on every y-axis, set from numbers.json["sweep"]["metric"]
YLABEL = "NCR reduction"


def _yrange(values) -> tuple[float, float]:
    """The shared y range: the lowest whisker rounded down to a 0.2 step (so
    no whisker is clipped and the floor tightens as the intervals narrow), and
    1.0 at the top."""
    lo, hi = min(0.0, min(values)), max(values)
    # floored at -1 (2026-09-30, ASP reduction): a single profile's no-MTD ASP
    # rests on 5 to 13 successes in 100 runs, and its intervals run to -7; a
    # whisker cut at the floor ends in a triangle (Panel.line), named in the captions
    return max(-1.0, math.floor(round(lo / 0.2, 6)) * 0.2), (1.0 if hi > 0.8 else 0.8)


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
        # at most 8 ticks (scrutiny round 2026-09-30: the -1 to 1 axis had 11),
        # on multiples of the step: the floor drops to one (a -0.8 floor with a
        # 0.5 step ticked -0.8, -0.3, 0.2, 0.7; 20-seed dry run, 2026-09-30)
        step = 0.5 if self.ymax - self.ymin > 1.5 else 0.2
        self.ymin = math.floor(round(self.ymin / step, 6)) * step
        while self.ymin + k * step <= self.ymax + 1e-9:
            v = round(self.ymin + k * step, 2)
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
                if lo < self.ymin - 1e-9:  # cut at the axis floor: a small triangle pointing down
                    yb = self.yv(self.ymin)
                    w(r"\fill[%s] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- cycle;" % (
                        col, x - 0.045, yb + 0.07, x + 0.045, yb + 0.07, x, yb))
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


def emit_headline(blocks):
    """``blocks``: [(metric, sweep, y range)], each drawn as the two rows of
    HEAD_ROWS; the metric heads every row it covers and titles its y-axis."""
    L = _preamble()
    w = L.append
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    PW, GAP, X0 = 4.55, 0.42, 1.3
    PH = 3.0
    ROWH = PH + 1.55
    XR = X0 + 3 * PW + 2 * GAP
    rows = [(metric, sweep, yr, header, panels) for metric, sweep, yr in blocks for header, panels in HEAD_ROWS]
    facts = []
    letters = iter("abcdefghijkl")
    # the figure-wide key at the top, left edge on the first y-axis (conventions §o)
    key_row(w, X0, 0.6 + ROWH * len(rows) + 0.35, ARM_KEY, xmax=XR)
    for r, (metric, sweep, yr, header, panels) in enumerate(rows):
        y0 = 0.6 + (len(rows) - 1 - r) * ROWH + 0.85
        w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {%s: %s};" % (
            X0, y0 + PH + 0.5, metric, header if header[1:2].isupper() else header[:1].lower() + header[1:]))
        w(r"\draw[black!25,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, y0 + PH + 0.48, XR, y0 + PH + 0.48))
        for k, (kind, key, title) in enumerate(panels):
            x0 = X0 + k * (PW + GAP)
            p = Panel(w, x0, x0 + PW, y0, y0 + PH, [int(i) for i in sweep["intervals"]], yr, ylabels=(k == 0),
                      title=title, letter=next(letters), tickfont=r"\scriptsize")
            for (arm, col, mark, dashed), dx in zip(ARMS, _offsets(len(ARMS), 0.016)):
                pts = _pts(sweep, lambda b, kind=kind, key=key, arm=arm: _v(b[kind][arm][key]))
                p.line(pts, col, mark, dashed, dx=dx, lw=0.9, r=0.06)
                facts += [(metric[:3] + " " + arm, key, *q) for q in pts]
        # one axis label per row, so it cannot cross the next row's header
        w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {%s};" % (X0 - 0.95, y0 + PH / 2, metric))
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
    letters = iter("abcdefghij")
    rows = ROWS_MECH + (("deployment strategies", HEAD_STRATEGIES),)  # the headline's order
    ytop = 1.0 + ROWH * len(rows)
    for r, (layer, conds) in enumerate(rows):
        y0 = ytop - (r + 1) * ROWH + 0.85
        w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {%s};" % (X0, y0 + PH + 0.5, _cap(layer)))
        w(r"\draw[black!25,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, y0 + PH + 0.48, X0 + 3 * PW + 2 * GAP, y0 + PH + 0.48))
        for k, c in enumerate(conds):
            x0 = X0 + k * (PW + GAP)
            facts += _profile_panel(w, sweep, c, x0, x0 + PW, y0, y0 + PH, yr, ylabels=(k == 0),
                                    title=_cap(LONG[c]), letter=next(letters), font=FONT)
    # the figure-wide key at the top, left edge on the first y-axis (conventions §o)
    key_row(w, X0, ytop + 0.35, PROFILE_KEY, xmax=X0 + 3 * PW + 2 * GAP)
    y0 = ytop - len(rows) * ROWH + 0.85
    for r in range(len(rows)):  # the axis title on every row (conventions §o rule 6)
        yr0 = ytop - (r + 1) * ROWH + 0.85
        w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {%s};" % (X0 - 0.95, yr0 + PH / 2, YLABEL))
    w(r"\node[anchor=north] at (%.3f,%.3f) {Deployment interval (s)};" % (X0 + 1.5 * PW + GAP, y0 - 0.5))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return L, facts


# --- Appendix F: the numbers behind the headline, one table per reduction --------


# (header, layer key whose mean the headline plots or None, rows)
VALUE_ROWS = (("host layer", "host", ("ip_shuffle", "complete_topology", "host_topology")),
              ("service layer", "service", ("port_shuffle", "os_diversity", "service_diversity")),
              ("credentials", None, ("user_shuffle",)),
              ("deployment strategies", None, HEAD_STRATEGIES))  # the panels' order
GREY = "black!55"  # survives a greyscale print (cold reader, 2026-09-25)


_bounded = bounded  # the shared formatter (_ch5_style; standard P2)


def _val(v: float) -> str:
    # a reduction: its upper bound, 1, is no host (or no run) compromised
    return _bounded(v, hi=1.0)


# per reduction: (label suffix, what 1 is, what a negative value is, the headline's panels)
VALUE_TABLES = (("ncr reduction", "", "no host compromised",
                 "more hosts compromised than with no MTD", "(a) to~(f)"),
                ("asp reduction", "-asp", "no run compromising a target host",
                 "more runs compromising a target host than with no MTD", "(g) to~(l)"))
BOUND_DECODE = r" A value above 0.99 but short of 1 prints as $>0.99$."  # standard P2


def emit_value_table(sweeps: dict) -> tuple[str, list]:
    """One table per reduction (``sweeps`` keyed by metric), each per defence,
    attacker and deployment interval; rows grouped as the headline's panels are
    (the layers, then the strategies); a cell whose 95 % interval includes zero
    is set grey."""
    L: list[str] = []
    w = L.append
    facts = []
    w("%% GENERATED by tools/ch5_sweep_figures.py from %s" % NUMBERS.relative_to(REPO))
    w("%   (sections sweep and sweep_asp; the APT attacker model pooled over its four profiles). Do not hand-edit.")
    w("% 2026-09-25 (Marc on the first draft: the rank grid's dashes and italics did not")
    w("%   read): the values themselves, grouped as the headline figure's panels.")
    w("% 2026-09-30 (Marc): moved from section 5.3.2 to Appendix F, the ASP reduction table beside it;")
    w("%   the body keeps the ranking table. DRAFT STATE --- ratify on read.")
    for metric, suffix, one, neg, panels in VALUE_TABLES:
        sweep = sweeps[metric]
        name = metric.replace("asp", "ASP").replace("ncr", "NCR")
        ivs = [str(i) for i in sweep["intervals"]]
        n = len(ivs)
        w(r"\begin{table}[htbp]")
        w(r"  \centering")
        w(r"  \caption[%s under each attacker, by MTD and deployment interval]{%s for each MTD mechanism and deployment strategy against the APT attacker model, averaged over $c_1$ to $c_4$, and against the baseline attacker, at each deployment interval; 1 is %s, 0 is as many as with no MTD, and a negative value is %s. Rows grouped as panels~%s of Figure~\ref{fig:eff-cross-arm}; a layer's row gives the mean it plots. Grey text: the 95\,\%% percentile bootstrap interval includes zero; the APT attacker model's cells hold four times as many runs as the baseline attacker's.@BOUND@}" % (name, name, one, neg, panels))
        cap_at = len(L) - 1  # the bound decode joins the caption only if a cell needs it
        w(r"  \label{tab:eff-interval-values%s}" % suffix)
        w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}\rowcolors{1}{}{}")  # the groups' rules separate rows; zebra would stripe the headers
        w(r"  \begin{tabular}{@{}P{3.75cm}*{%d}{>{\centering\arraybackslash}p{0.78cm}}@{}}" % (2 * n))
        w(r"    \toprule")
        w(r"    & \multicolumn{%d}{c}{APT attacker model} & \multicolumn{%d}{c}{Baseline attacker} \\" % (n, n))
        w(r"    \cmidrule(lr){2-%d}\cmidrule(lr){%d-%d}" % (n + 1, n + 2, 2 * n + 1))
        w(r"    Deployment interval (s) & %s & %s \\" % (" & ".join(fmt_thousands(int(i)) for i in ivs),
                                                       " & ".join(fmt_thousands(int(i)) for i in ivs)))

        def cells_of(kind, key):
            out = []
            for arm in ("movement", "baseline"):
                for i in ivs:
                    d = sweep["by_interval"][i][kind][arm][key]
                    sep = d["lo"] > 0 or d["hi"] < 0
                    out.append(_val(d["point"]) if sep else r"\textcolor{%s}{%s}" % (GREY, _val(d["point"])))
                    facts.append((name[:3] + " " + arm, key, int(i), d["point"], d["lo"], d["hi"], sep))
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
        w("")
        bound = any("{>}" in x or "{<}" in x for x in L[cap_at + 1:])
        L[cap_at] = L[cap_at].replace("@BOUND@", BOUND_DECODE if bound else "")
    return "\n".join(L), facts


# --- §5.3.2's table: both attackers ranked, all metrics, one interval -----------

STEM_RANKT = "tab_5-3-2d_attacker_ranking"
STEM_FULL = "tab_F-1_conditions_%s"      # the appendix tables, one per attacker
RANK_INTERVAL = "200"                    # MTDShield's training interval and the lineage's
N_HOSTS = 50                             # NCR = hosts compromised over the network's 50 (Table 5.2)


def _num(v: float, nd: int = 2) -> str:
    # a reduction never prints 1.00 short of 1 (standard P2)
    return _bounded(v, nd, hi=1.0)


MTTC_PLACE = 2  # set per table by emit_ranking_table (the precision rule)
_mttc_unreported, _dash_decode = mttc_unreported, mttc_dash_decode  # the shared rule (_ch5_style)


def _place(hw: float) -> int:
    """The precision rule (Marc 2026-09-30): a column to the place of its widest
    interval's half-width at one significant figure (two when that figure is a 1)."""
    place = math.floor(math.log10(hw)) if hw > 0 else 0
    if hw > 0 and int(round(hw / 10.0 ** place, 6)) == 1:
        place -= 1
    return place


def _at_place(x: float, place: int) -> str:
    """``x`` rounded to ``place`` (the precision rule), thin space from 1 000."""
    if place >= 0:
        return fmt_thousands(int(round(x / 10 ** place) * 10 ** place))
    t = "%.*f" % (-place, x)
    return "0." + "0" * -place if t == "-0." + "0" * -place else t


def _mttc(iv: dict | None) -> str:
    # MTTC over the runs that compromise a target host (section 4.5.2); ASP is its coverage
    if _mttc_unreported(iv):
        return "---"
    return _at_place(iv["mean"], max(0, MTTC_PLACE))


def _order(blk) -> list[str]:
    mv = blk["movement"]["rows"]
    return sorted(mv, key=lambda c: (mv[c]["rank"], -mv[c]["ncr_reduction"]["point"]))


def emit_ranking_table(ranking) -> tuple[str, list]:
    iv = RANK_INTERVAL if RANK_INTERVAL in ranking["by_interval"] else str(ranking["intervals"][0])
    blk = ranking["by_interval"][iv]
    order = _order(blk)
    facts = []
    global MTTC_PLACE
    rows = [r for arm in ("movement", "baseline") for r in list(blk[arm]["rows"].values()) + [blk[arm]["none"]]]
    MTTC_PLACE = _place(max(r["mttc"]["ci95"] for r in rows if not _mttc_unreported(r["mttc"])))
    reasons = {_mttc_unreported(r["mttc"]) for r in rows} - {None}
    L: list[str] = []
    w = L.append
    w("%% GENERATED by tools/ch5_sweep_figures.py from %s" % NUMBERS.relative_to(REPO))
    w("%   (section ranking; ranks by Scott-Knott ESD, data/results/ch5_defended/sk_esd.py). Do not hand-edit.")
    w("% 2026-09-25 (Marc: \"we have to have some ranks ... ranking with ties\"; results context §8j-4):")
    w("%   the two attackers side by side at one interval, all of Table 4.3's metrics. DRAFT STATE --- ratify on read.")
    w("% 2026-09-30: ranked on hosts compromised per seed (NCR reduction, the headline); ASP reduction")
    w("%   beside it (section 5.3.2 carries both); MTTC at a target host (ruling H1).")
    w("% 2026-09-30 (Marc): NCR and ASP dropped, each the reduction beside it restated against the no-MTD")
    w("%   row (Tables F.3 and F.4 keep them). At footnotesize it is still wider than the text, so scriptsize (conventions).")
    w("% 2026-10-02 (Marc; docs/workflows/results_presentation_standard.md P2, S1-S2, N1): a blank cell is")
    w("%   not applicable (the reference's rank and reductions), a dash an MTTC not reported, > 0.99 a")
    w("%   reduction short of 1.")
    w(r"\begin{table}[htbp]")
    w(r"  \centering")
    w("@CAPTION@")
    cap_at = len(L) - 1
    w(r"  \label{tab:eff-cross-arm}")
    # the stripes restart at row 4 so neither header row is shaded
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}\rowcolors{4}{black!5}{}")
    C = r">{\centering\arraybackslash}p{%s}"
    cols = [C % "0.8cm", C % "1.3cm", C % "1.3cm", C % "1.1cm"]
    w(r"  \begin{tabular}{@{}P{3.4cm}%s%s@{}}" % ("".join(cols), "".join(cols)))
    w(r"    \toprule")
    w(r"    & \multicolumn{4}{c}{APT attacker model} & \multicolumn{4}{c}{Baseline attacker} \\")
    w(r"    \cmidrule(lr){2-5}\cmidrule(lr){6-9}")
    head = ["Rank", r"NCR\newline reduction", r"ASP\newline reduction", r"MTTC\newline (s)"]
    w(r"    MTD & %s & %s \\" % (" & ".join(head), " & ".join(head)))
    w(r"    \midrule")

    def cells(row, none=False):
        # the reference has no rank and no reduction: blank, not applicable (S1)
        rank = "" if none else (r"\textbf{1}" if row["rank"] == 1 else str(row["rank"]))
        return [rank, "" if none else _num(row["ncr_reduction"]["point"]),
                "" if none else _num(row["asp_reduction"]["point"]), _mttc(row["mttc"])]

    w("    no MTD & %s & %s \\\\" % (" & ".join(cells(blk["movement"]["none"], True)),
                                       " & ".join(cells(blk["baseline"]["none"], True))))
    w(r"    \midrule")
    for c in order:
        m, b = blk["movement"]["rows"][c], blk["baseline"]["rows"][c]
        w("    %s & %s & %s \\\\" % (LONG[c], " & ".join(cells(m)), " & ".join(cells(b))))
        facts.append((c, m["rank"], m["ncr_reduction"]["point"], b["rank"], b["ncr_reduction"]["point"]))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    bound = BOUND_DECODE if any("{>}" in x for x in L[cap_at + 1:]) else ""
    L[cap_at] = (r"  \caption[The MTD mechanisms and deployment strategies ranked against each attacker]{Each MTD mechanism and deployment strategy deployed every %s\,s against the APT attacker model, averaged over $c_1$ to $c_4$, and against the baseline attacker, each ranked by Scott--Knott ESD on the mean hosts compromised per seed (Section~\ref{sec:dimensions}). Rank~1, in bold, is the fewest hosts compromised; rows that share a rank are not told apart. Rows in the APT attacker model's order. Metrics as Table~\ref{tab:metrics}. No MTD is the reference each reduction is taken against, so its rank and reductions are blank.%s%s MTTC is rounded to the precision of its widest interval. The NCR and ASP behind each reduction, and every value's interval, are in Appendix~\ref{app:supplementary-results}.}"
                 % (fmt_thousands(int(iv)), bound, _dash_decode(reasons)))
    return "\n".join(L) + "\n", facts


def emit_full_table(ranking, arm) -> str:
    """The appendix table for one attacker: every metric with its interval, at
    the ranking interval, rows in that attacker's rank order."""
    iv = RANK_INTERVAL if RANK_INTERVAL in ranking["by_interval"] else str(ranking["intervals"][0])
    blk = ranking["by_interval"][iv][arm]
    order = sorted(blk["rows"], key=lambda c: (blk["rows"][c]["rank"], -blk["rows"][c]["ncr_reduction"]["point"]))
    who = (r"the APT attacker model, averaged over $c_1$ to $c_4$" if arm == "movement" else "the baseline attacker")
    rows = [blk["none"]] + [blk["rows"][c] for c in order]
    # the precision rule, per column: NCR and MTTC to the place of the column's widest interval
    ncr_place = _place(max(r["hosts"]["ci95"] / N_HOSTS for r in rows))
    shown = [r["mttc"] for r in rows if not _mttc_unreported(r["mttc"])]
    mttc_place = max(0, _place(max(m["ci95"] for m in shown))) if shown else 0
    reasons = {_mttc_unreported(r["mttc"]) for r in rows} - {None}
    L: list[str] = []
    w = L.append
    w("%% GENERATED by tools/ch5_sweep_figures.py from %s (section ranking)." % NUMBERS.relative_to(REPO))
    w("%   Do not hand-edit. DRAFT STATE --- ratify on read. 2026-09-30: ASP reduction added; MTTC at a target host.")
    w("% 2026-10-02 (results_presentation_standard.md P1, P2, S1-S2, N1): NCR and MTTC to the precision rule;")
    w("%   the reference's rank and reductions blank; a dash an MTTC not reported; > 0.99 and < 0.01 at the bounds.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w("@CAPTION@")
    cap_at = len(L) - 1
    w(r"  \label{tab:full-%s}" % arm)
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}")
    C = r">{\centering\arraybackslash}p{%s}"
    # widths so no cell wraps: "< 0.01" and a negative bracket each on one line (2026-10-02 build)
    w(r"  \begin{tabular}{@{}P{3.0cm}%s%s%s%s%s%s@{}}" % (C % "0.7cm", C % "0.8cm", C % "3.0cm", C % "2.0cm",
                                                        C % "3.0cm", C % "2.0cm"))
    w(r"    \toprule")
    w(r"    MTD & Rank & ASP & ASP reduction & NCR & NCR reduction & MTTC (s) \\")
    w(r"    \midrule")

    def hw(x, place):
        # a half-width that rounds to zero at the column's place is not zero (P2)
        t = _at_place(x, place)
        return "{<}" + _at_place(10.0 ** place, place) if x > 0 and float(t.replace(r"\,", "")) == 0 else t

    def ncr(d):
        return r"$%s \pm %s$" % (_at_place(d["mean"] / N_HOSTS, ncr_place), hw(d["ci95"] / N_HOSTS, ncr_place))

    def mttc(iv_):
        if _mttc_unreported(iv_):
            return "---"
        return r"$%s \pm %s$" % (_at_place(iv_["mean"], mttc_place), hw(iv_["ci95"], mttc_place))

    def asp(v):
        return _bounded(v, lo=0.0, hi=1.0)

    def red(d):
        return r"%s [%s, %s]" % (_num(d["point"]), _num(d["lo"]), _num(d["hi"]))

    n = blk["none"]
    w("    no MTD &  & %s &  & %s &  & %s \\\\" % (asp(n["asp"]), ncr(n["hosts"]), mttc(n["mttc"])))
    w(r"    \midrule")
    for c in order:
        d = blk["rows"][c]
        w("    %s & %d & %s & %s & %s & %s & %s \\\\" % (LONG[c], d["rank"], asp(d["asp"]), red(d["asp_reduction"]),
                                                        ncr(d["hosts"]), red(d["ncr_reduction"]), mttc(d["mttc"])))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    body = L[cap_at + 1:]
    bound = ""
    if any("{>}" in x or "{<}" in x for x in body):
        bound = r" A value short of a bound it rounds to prints as $>0.99$ or $<0.01$."
    L[cap_at] = (r"  \caption[MTD mechanisms and deployment strategies against %s, with intervals]{Each MTD mechanism and deployment strategy deployed every %s\,s against %s, with the rank of Table~\ref{tab:eff-cross-arm}, on the metrics of Table~\ref{tab:metrics}; the first row is the no-MTD reference, whose rank and reductions are blank.%s%s Brackets: a 95\,\%% percentile bootstrap interval; $\pm$: a 95\,\%% interval on the mean (normal approximation).}"
                 % (LABEL[arm], fmt_thousands(int(iv)), who, bound, _dash_decode(reasons)))
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--only", default=None, help="headline | mechanisms | values | ranking")
    args = ap.parse_args()
    data = json.loads(args.numbers.read_text(encoding="utf-8"))
    if "sweep" not in data:
        raise SystemExit("numbers.json has no sweep section; run analyse.py")
    if "sanity" in data and (not data["sanity"].get("all_cells_full", data["sanity"].get("all_cells_100")) or data["sanity"]["error_rows"]):
        raise SystemExit("corpus sanity failed; not drawing from it")
    sweep = data["sweep"]
    global YLABEL
    YLABEL = sweep.get("metric", "ncr reduction").replace("asp", "ASP").replace("ncr", "NCR")
    yr = _yrange(_all_points(sweep))
    print(f"intervals {sweep['intervals']}; shared y range {yr}")
    if "sweep_asp" not in data:
        raise SystemExit("numbers.json has no sweep_asp section; run analyse.py")
    sa = data["sweep_asp"]
    pts_a = [d[k] for i in sa["intervals"] for arm in ("movement", "baseline")
             for kind in ("attacker", "layer") for d in sa["by_interval"][str(i)][kind][arm].values()
             for k in ("point", "lo")]
    yr_a = _yrange(pts_a)
    print(f"ASP reduction y range {yr_a}")
    for name, stem, fn in (("headline", STEM_HEAD, lambda: emit_headline([(YLABEL, sweep, yr), ("ASP reduction", sa, yr_a)])),
                           ("mechanisms", STEM_MECH, lambda: emit_mechanisms(sweep, yr))):
        if args.only and args.only != name:
            continue
        lines, facts = fn()
        write_fig(stem, lines)
        print(f"{name} facts (series, key, interval, point, lo, hi):")
        for f in facts:
            print("   %-12s %-30s %5d %+.3f [%+.3f, %+.3f]" % f)
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
        tex, facts = emit_value_table({"ncr reduction": sweep, "asp reduction": sa})
        (TAB_DIR / f"{STEM_VAL}.tex").write_text(tex)
        print(f"wrote tables/{STEM_VAL}.tex (arm, condition, interval, point, lo, hi, separated):")
        for f in facts:
            print("   %-12s %-18s %5d %+.3f [%+.3f, %+.3f] %s" % f)


if __name__ == "__main__":
    main()
