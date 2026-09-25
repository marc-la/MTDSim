#!/usr/bin/env python3
"""Chapter 5 §5.3.2-§5.3.3 line charts: NCR reduction against the deployment
interval (Jin's second pass, relayed by Marc 2026-09-25; design brief in
docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md §8j; spec in
docs/handoffs/2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md
§5.4 and §5.8). They replace the grouped bars of Figures 5.4 and 5.5.

  headline  §5.3.2  2 x 2: columns the attacker (the APT attacker model left),
                    rows the layers (host layer, service layer, user shuffle)
                    over the execution schemes (random, alternative, random
                    over MTDShield's four, MTDShield); greys with one marker
                    per line, dashed = execution scheme, the accent on MTDShield
  mechanisms §5.3.3 the seven mechanisms, one panel each, rows by layer;
                    lines c_1-c_4 and c_agg in the chapter's hues, the baseline
                    attacker the dashed grey reference
  schemes   §5.3.3  the four execution schemes, the same form, 2 x 2

Every panel of the three figures shares one y range and the same log x axis
at the corpus's intervals. Data: ``numbers.json["sweep"]`` from
``data/results/ch5_defended/analyse.py``; nothing is typed here, and every
drawn point is printed on stdout.

Usage:
  python tools/ch5_sweep_figures.py [--numbers PATH] [--no-compile] [--only headline|mechanisms|schemes]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (CNAME, FONT, LABEL, LONG, MARK, PREAMBLE, PROFILES, REPO, TAB_DIR,  # noqa: E402
                        compile_fig, fmt_thousands, marker, write_fig)

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers.json"
STEM_HEAD = "fig_5-3-2b_interval_headline"
STEM_MECH = "fig_5-3-3b_interval_mechanisms"
STEM_SCH = "fig_5-3-3c_interval_schemes"
STEM_RANK = "tab_5-3-2b_rank_grid"
ROWS_MECH = (("host layer", ("ip_shuffle", "complete_topology", "host_topology")),
             ("service layer", ("port_shuffle", "os_diversity", "service_diversity")),
             ("credentials", ("user_shuffle",)))
SCHEMES4 = ("random", "alternative", "random_four", "mtdshield")
ACCENT = "31,84,140"
# the headline's series: (key in numbers, label, colour, marker, dashed)
LAYER_SERIES = (("host", "host layer", "black!85", "circle", False),
                ("service", "service layer", "black!55", "square", False),
                ("credentials", "user shuffle", "black!35", "triangle", False))
SCHEME_SERIES = (("random", "random", "black!80", "circle", True),
                 ("alternative", "alternative", "black!50", "square", True),
                 ("random_four", "random, MTDShield's four", "black!30", "diamond", True),
                 ("mtdshield", "MTDShield", "accent", "triangle", True))


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
                w(r"\node[anchor=east] at (%.3f,%.3f) {%.1f};" % (x0 - 0.1, y, v))
            k += 1
        if self.ymin < 0:  # zero is the no-defence reference
            w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, self.yv(0), x1, self.yv(0)))
        for iv in ivs:
            x = self.xv(iv)
            w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, y0, x, y0 - 0.07))
            if xlabels:
                w(r"\node[anchor=north%s] at (%.3f,%.3f) {%s};" % (
                    ",font=" + tickfont if tickfont else "", x, y0 - 0.1, fmt_thousands(iv)))
        if title or letter:
            head = (r"\textbf{(%s)}~" % letter if letter else "") + (title or "")
            w(r"\node[anchor=south west] at (%.3f,%.3f) {%s};" % (x0 - 0.02, y1 + 0.05, head))
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
        style = "%s,line width=%.2fpt%s" % (col, lw, ",dash pattern=on 2.4pt off 1.4pt" if dashed else "")
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


def _key(w, x, y, entries, xmax, *, dashed_default=False, gap=0.45):
    """One key line: (label, colour, marker, dashed); wraps at ``xmax``."""
    x0 = x
    for label, col, mark, dashed in entries:
        width = 0.75 + 0.16 * len(label.replace("$", "").replace("\\mathrm", "").replace("{", "").replace("}", "")) + gap
        if x + width > xmax:
            x, y = x0, y - 0.42
        style = "%s,line width=0.7pt%s" % (col, ",dash pattern=on 2.4pt off 1.4pt" if dashed else "")
        w(r"\draw[%s] (%.3f,%.3f) -- (%.3f,%.3f);" % (style, x, y, x + 0.6, y))
        marker(w, mark, col, x + 0.3, y, r=0.06)
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (x + 0.68, y, label))
        x += width
    return y


# --- the headline ---------------------------------------------------------------


def emit_headline(sweep, yr):
    ivs = [int(i) for i in sweep["intervals"]]
    L = _preamble()
    w = L.append
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    PH = 3.6
    XC = ((1.3, 8.2), (8.8, 15.7))
    K2 = 0.25                  # the schemes key
    K1 = K2 + 0.45             # the mechanisms key
    Y2 = K1 + 1.35             # schemes row, above the axis title
    Y1 = Y2 + PH + 1.05        # mechanisms row
    TOP = Y1 + PH + 0.55
    facts = []
    for col, arm in enumerate(("movement", "baseline")):
        x0, x1 = XC[col]
        w(r"\node[anchor=south] at (%.3f,%.3f) {\bfseries %s};" % ((x0 + x1) / 2, TOP, LABEL[arm]))
        for y0, series, kind, letter, title in ((Y1, LAYER_SERIES, "layer", "ab"[col], "defence mechanisms, by layer"),
                                                (Y2, SCHEME_SERIES, "attacker", "cd"[col], "deployment strategies")):
            p = Panel(w, x0, x1, y0, y0 + PH, ivs, yr, xlabels=True, ylabels=(col == 0), letter=letter, title=title)
            offs = _offsets(len(series), 0.018)
            for (key, label, colour, mark, dashed), dx in zip(series, offs):
                pts = _pts(sweep, lambda b, key=key, kind=kind: _v(b[kind][arm][key]))
                p.line(pts, colour, mark, dashed, dx=dx, lw=(1.0 if key == "mtdshield" else 0.7))
                facts += [(arm, key, *q) for q in pts]
    w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {NCR reduction};" % (XC[0][0] - 0.75, (Y2 + Y1 + PH) / 2))
    w(r"\node[anchor=north] at (%.3f,%.3f) {deployment interval (s)};" % ((XC[0][0] + XC[1][1]) / 2, Y2 - 0.45))
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {defence mechanisms};" % (XC[0][0] - 1.2, K1))
    _key(w, XC[0][0] + 2.5, K1, [(lb, c, m, d) for _, lb, c, m, d in LAYER_SERIES], XC[1][1] + 0.3)
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {deployment strategies};" % (XC[0][0] - 1.2, K2))
    _key(w, XC[0][0] + 2.5, K2, [(lb, c, m, d) for _, lb, c, m, d in SCHEME_SERIES], XC[1][1] + 0.3, gap=0.25)
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


def _profile_key(w, x, y, xmax):
    entries = [(LABEL[p], CNAME[p], MARK[p], False) for p in PROFILES] + [("baseline attacker", "cbase", "square", True)]
    return _key(w, x, y, entries, xmax, gap=0.3)


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
        w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {%s};" % (X0 - 1.25, y0 + PH + 0.5, layer))
        w(r"\draw[black!25,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0 - 1.25, y0 + PH + 0.48, X0 + 3 * PW + 2 * GAP, y0 + PH + 0.48))
        for k, c in enumerate(conds):
            x0 = X0 + k * (PW + GAP)
            facts += _profile_panel(w, sweep, c, x0, x0 + PW, y0, y0 + PH, yr, ylabels=(k == 0),
                                    title=LONG[c], letter=next(letters), font=FONT)
    # the key in the credentials row's spare slots
    y0 = ytop - len(ROWS_MECH) * ROWH + 0.85
    kx = X0 + PW + GAP + 0.3
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {attack profile};" % (kx, y0 + PH - 0.2))
    _profile_key(w, kx, y0 + PH - 0.75, X0 + 3 * PW + 2 * GAP)
    w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {NCR reduction};" % (X0 - 0.95, (y0 + ytop) / 2))
    w(r"\node[anchor=north] at (%.3f,%.3f) {deployment interval (s)};" % (X0 + 1.5 * PW + GAP, y0 - 0.5))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return L, facts


def emit_schemes(sweep, yr):
    L = _preamble()
    w = L.append
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    XC = ((1.3, 8.2), (8.8, 15.7))
    PH = 3.3
    facts = []
    letters = iter("abcd")
    KY = 0.25
    ys = (KY + 1.2 + PH + 1.1, KY + 1.2)
    for r in range(2):
        for k in range(2):
            c = SCHEMES4[2 * r + k]
            x0, x1 = XC[k]
            facts += _profile_panel(w, sweep, c, x0, x1, ys[r], ys[r] + PH, yr, ylabels=(k == 0),
                                    title=LONG[c], letter=next(letters), font=FONT)
    w(r"\node[rotate=90,anchor=south] at (%.3f,%.3f) {NCR reduction};" % (XC[0][0] - 0.75, (ys[1] + ys[0] + PH) / 2))
    w(r"\node[anchor=north] at (%.3f,%.3f) {deployment interval (s)};" % ((XC[0][0] + XC[1][1]) / 2, ys[1] - 0.5))
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {attack profile};" % (XC[0][0], KY - 0.3))
    _profile_key(w, XC[0][0] + 5.2, KY - 0.3, XC[1][1] + 0.3)
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return L, facts


# --- Table 5.3: the rank grid ---------------------------------------------------


def emit_rank_grid(sweep) -> tuple[str, list]:
    """Ranks by NCR reduction per attacker at every interval, rows in the APT
    attacker model's order at 200 s (or the first interval the corpus has); a
    condition whose interval includes zero is not separated from no defence
    and prints a dash instead of a rank."""
    ivs = [str(i) for i in sweep["intervals"]]
    ref = "200" if "200" in ivs else ivs[0]
    conds = sweep["by_interval"][ref]["conditions"]
    order = sorted(conds, key=lambda c: sweep["by_interval"][ref]["ranks"]["movement"][c])
    n = len(ivs)
    L: list[str] = []
    w = L.append
    facts = []
    w("% GENERATED by tools/ch5_sweep_figures.py from data/results/ch5_defended/numbers.json")
    w("%   (section sweep; the APT attacker model pooled over its four profiles). Do not hand-edit.")
    w("% 2026-09-25 (Marc on Jin's second pass; results context §8j): the rank grid over")
    w("%   every deployment interval replaces the two-interval orderings. DRAFT STATE --- ratify on read.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[The defence ranking under each attacker]{The defence conditions ranked by NCR reduction against the APT attacker model, pooled over $c_1$ to $c_4$, and against the baseline attacker, at each deployment interval, in the APT attacker model's order at %s\,s; rank~1 is the largest reduction. A dash: the condition's 95\,\%% bootstrap interval includes zero, the no-defence reference; italic: the interval lies wholly below zero.}" % fmt_thousands(int(ref)))
    w(r"  \label{tab:eff-orderings}")
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{4pt}\rowcolors{4}{black!5}{}")
    w(r"  \begin{tabular}{@{}P{3.6cm}*{%d}{>{\centering\arraybackslash}p{0.72cm}}@{}}" % (2 * n))
    w(r"    \toprule")
    w(r"    & \multicolumn{%d}{c}{APT attacker model} & \multicolumn{%d}{c}{Baseline attacker} \\" % (n, n))
    w(r"    \cmidrule(lr){2-%d}\cmidrule(lr){%d-%d}" % (n + 1, n + 2, 2 * n + 1))
    w(r"    & \multicolumn{%d}{c}{deployment interval (s)} & \multicolumn{%d}{c}{deployment interval (s)} \\" % (n, n))
    w(r"    Condition & %s & %s \\" % (" & ".join(fmt_thousands(int(i)) for i in ivs), " & ".join(fmt_thousands(int(i)) for i in ivs)))
    w(r"    \midrule")
    for c in order:
        cells = []
        for arm in ("movement", "baseline"):
            for i in ivs:
                b = sweep["by_interval"][i]
                d = b["attacker"][arm][c]
                sep = d["lo"] > 0 or d["hi"] < 0
                r = str(b["ranks"][arm][c])
                cells.append(("\\textit{%s}" % r if d["hi"] < 0 else r) if sep else "--")
                facts.append((arm, c, int(i), b["ranks"][arm][c], d["point"], d["lo"], d["hi"], sep))
        w("    %s & %s \\\\" % (LONG[c], " & ".join(cells)))
    w(r"    \bottomrule")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n", facts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--only", default=None, help="headline | mechanisms | schemes | ranks")
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
    if not args.only or args.only == "ranks":
        tex, facts = emit_rank_grid(sweep)
        (TAB_DIR / f"{STEM_RANK}.tex").write_text(tex)
        print(f"wrote tables/{STEM_RANK}.tex (arm, condition, interval, rank, point, lo, hi, separated):")
        for f in facts:
            print("   %-9s %-18s %5d %2d %+.3f [%+.3f, %+.3f] %s" % f)


if __name__ == "__main__":
    main()
