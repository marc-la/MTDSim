#!/usr/bin/env python3
"""Chapter 5 sensitivity figure: the outcome measure against the one declared
input that moved (fig:sens-dwell-anchor).

The figure exists by convention — one line chart per declared input whose band
ends separate from its centre (evaluation_conventions.md §c: x = the swept
input, y = the outcome, series = a second factor at two to four levels,
marker per series, legend inside the axes). WHICH input it draws is the
sweep's result, not this tool's: the anchor is a command-line choice and the
record's provenance puts it at the low-and-slow anchor
(rate_feasibility_study.md §10).

Data: the rate feasibility study's per-run table. Pooled across the five
profiles at the seed set the workspace holds; the interval is a 95 % normal
interval on the pooled mean. Nothing is typed here — every plotted value and
every number a caption may quote is computed from the CSV and printed.

PROVENANCE, stated once: the default workspace is the S3-R re-run
(data/results/rate_feasibility_study/numbers/, ten seeds, the random
multi-mechanism scheme, pre-restoration substrate). Until the sweep is re-run
at the configuration chapter 5 reports (design handoff §3.2), the figure it
draws is the record's, not the chapter's — the tex comment beside the float
says so. Re-point --csv at the re-run's table and regenerate; the caption's
numbers are re-read from stdout.

Usage:
  python tools/ch5_sensitivity_figure.py
      [--csv data/results/rate_feasibility_study/numbers/per_run.csv]
      [--anchor stealth] [--reference-interval 200] [--no-compile]

Writes docs/thesis/figures/fig_5-1a_sens_dwell_anchor.{tex,pdf}.

Style (figure_table_conventions.md): TikZ standalone at 12 pt, Helvetica
(helvet 0.92), greys + the one accent, no title, no chart junk. Natural width
~11.5 cm at \\footnotesize so an inclusion at 0.78\\textwidth prints labels at
~10 pt against the 12 pt body (§h arithmetic).
"""
from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
FIG_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_5-1a_sens_dwell_anchor"
ACCENT_RGB = "31,84,140"

ANCHORS = {  # command-line name -> (csv column, prose name); "family" is the body's word (2026-09-17)
    "scan": ("m_scan", "scan-shaped family"),
    "exploit": ("m_exploit", "exploit-shaped family"),
    "stealth": ("m_stealth", "low-and-slow family"),
    "objective": ("m_objective", "objective family"),
}


def aggregate(csv: Path, anchor_col: str, reference_interval: float) -> pd.DataFrame:
    d = pd.read_csv(csv)
    d = d[(d.arm == "movement") & (d.family == "exponential")]
    others = [c for c, _ in ANCHORS.values() if c != anchor_col]
    for c in others:
        d = d[d[c] == 1.0]
    off = d[d.mtd_interval.isna()].assign(condition="none")
    on = d[d.mtd_interval == reference_interval].assign(condition="reference")
    a = pd.concat([off, on])
    g = a.groupby(["condition", anchor_col]).compromised_count.agg(["mean", "std", "count"]).reset_index()
    g["ci"] = 1.96 * g["std"] / g["count"].pow(0.5)
    g = g.rename(columns={anchor_col: "mult"})
    return g.sort_values(["condition", "mult"])


def emit(g: pd.DataFrame, anchor_name: str, reference_interval: float) -> str:
    mults = sorted(g["mult"].unique())
    lo, hi = min(mults), max(mults)
    ymax = float((g["mean"] + g["ci"]).max())
    ytop = math.ceil(ymax / 2.0) * 2.0

    X0, X1 = 1.6, 11.6
    Y0, Y1 = 0.0, 5.0

    def xs(m: float) -> float:
        return X0 + (math.log2(m) - math.log2(lo)) / (math.log2(hi) - math.log2(lo)) * (X1 - X0)

    def ys(v: float) -> float:
        return Y0 + v / ytop * (Y1 - Y0)

    series = [
        ("none", "black!70", "circle", "no MTD"),
        ("reference", "accent", "square", "random, every %d\\,s" % reference_interval),
    ]

    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usepackage[scaled=0.92]{helvet}")
    w(r"\renewcommand{\familydefault}{\sfdefault}")
    w(r"\usetikzlibrary{calc}")
    w(r"\definecolor{accent}{RGB}{%s}" % ACCENT_RGB)
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=\footnotesize}]")
    # axes and gridlines
    w(r"\draw[black!60,line width=0.4pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (X0, Y0, X1, Y0))
    w(r"\draw[black!60,line width=0.4pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (X0, Y0, X0, Y1))
    v = 0.0
    while v <= ytop + 1e-9:
        w(r"\draw[black!60,line width=0.3pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (X0 - 0.08, ys(v), X0, ys(v)))
        w(r"\node[anchor=east] at (%.2f,%.3f) {%g};" % (X0 - 0.12, ys(v), v))
        if v > 0:
            w(r"\draw[black!12,line width=0.2pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (X0, ys(v), X1, ys(v)))
        v += 2.0
    w(r"\node[rotate=90,anchor=south] at (%.2f,%.2f) {distinct hosts reached};" % (X0 - 0.85, (Y0 + Y1) / 2))
    # x ticks at every power of two inside the band, labelled as a multiple of the declared value
    m = lo
    while m <= hi * 1.0001:
        w(r"\draw[black!60,line width=0.3pt] (%.3f,%.2f) -- (%.3f,%.2f);" % (xs(m), Y0, xs(m), Y0 - 0.08))
        lab = ("$\\times%g$" % m) if m != 1 else "$\\times1$ (declared)"
        w(r"\node[anchor=north] at (%.3f,%.2f) {%s};" % (xs(m), Y0 - 0.12, lab))
        m *= 2
    w(r"\draw[black!30,line width=0.3pt,dash pattern=on 1.5pt off 1.5pt] (%.3f,%.2f) -- (%.3f,%.2f);" % (xs(1.0), Y0, xs(1.0), Y1))
    w(r"\node[anchor=north] at (%.2f,%.2f) {%s, as a multiple of its declared value};" % ((X0 + X1) / 2, Y0 - 0.5, anchor_name))
    # series: interval bars, line, marker
    for cond, col, mark, _ in series:
        rows = g[g.condition == cond].sort_values("mult")
        pts = []
        for _, r in rows.iterrows():
            x, y, ci = xs(r["mult"]), ys(r["mean"]), r["ci"] / ytop * (Y1 - Y0)
            w(r"\draw[%s,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x, y - ci, x, y + ci))
            w(r"\draw[%s,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x - 0.08, y - ci, x + 0.08, y - ci))
            w(r"\draw[%s,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x - 0.08, y + ci, x + 0.08, y + ci))
            pts.append((x, y))
        w(r"\draw[%s,line width=0.6pt] %s;" % (col, " -- ".join("(%.3f,%.3f)" % p for p in pts)))
        for x, y in pts:
            if mark == "circle":
                w(r"\fill[%s] (%.3f,%.3f) circle (0.7mm);" % (col, x, y))
            else:
                w(r"\fill[%s] (%.3f,%.3f) ++(-0.65mm,-0.65mm) rectangle ++(1.3mm,1.3mm);" % (col, x, y))
    # legend inside the axes, upper right (breadth falls to the right, so the corner is empty)
    lx, ly = X1 - 4.7, Y1 - 0.25
    for _, col, mark, lab in series:
        w(r"\draw[%s,line width=0.6pt] (%.2f,%.3f) -- (%.2f,%.3f);" % (col, lx, ly, lx + 0.5, ly))
        if mark == "circle":
            w(r"\fill[%s] (%.2f,%.3f) circle (0.7mm);" % (col, lx + 0.25, ly))
        else:
            w(r"\fill[%s] (%.2f,%.3f) ++(-0.65mm,-0.65mm) rectangle ++(1.3mm,1.3mm);" % (col, lx + 0.25, ly))
        w(r"\node[anchor=west] at (%.2f,%.3f) {%s};" % (lx + 0.6, ly, lab))
        ly -= 0.32
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


def main() -> None:
    global STEM
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", type=Path, default=REPO / "data/results/rate_feasibility_study/numbers/per_run.csv")
    ap.add_argument("--anchor", choices=sorted(ANCHORS), default="stealth")
    ap.add_argument("--reference-interval", type=float, default=200.0)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--stem", default=STEM,
                    help="output stem; fig_C-1a_sens_dwell_family when the figure lives in App. C.1 (2026-09-17 ruling)")
    args = ap.parse_args()
    STEM = args.stem

    col, name = ANCHORS[args.anchor]
    g = aggregate(args.csv, col, args.reference_interval)
    if g.empty:
        raise SystemExit(f"no rows for anchor {args.anchor} at interval {args.reference_interval} in {args.csv}")

    tex = emit(g, name, args.reference_interval)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    (FIG_DIR / f"{STEM}.tex").write_text(tex)
    print(f"wrote {(FIG_DIR / (STEM + '.tex')).relative_to(REPO)}")

    print(f"source={args.csv.relative_to(REPO) if args.csv.is_absolute() else args.csv}  anchor={name}  "
          f"reference interval={args.reference_interval:g} s  runs per cell={int(g['count'].iloc[0])}")
    for cond in ("none", "reference"):
        rows = g[g.condition == cond]
        print(f"  {cond:9s}: " + "; ".join(f"x{r['mult']:g} = {r['mean']:.2f} +/- {r['ci']:.2f}" for _, r in rows.iterrows()))

    if not args.no_compile:
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{STEM}.tex"],
                           cwd=FIG_DIR, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            raise SystemExit(f"pdflatex failed on {STEM}")
        for ext in (".aux", ".log"):
            p = FIG_DIR / f"{STEM}{ext}"
            if p.exists():
                p.unlink()
        print(f"wrote {(FIG_DIR / (STEM + '.pdf')).relative_to(REPO)}")
        bb = subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=bbox", f"{STEM}.pdf"],
                            cwd=FIG_DIR, capture_output=True, text=True)
        for line in bb.stderr.splitlines():
            if line.startswith("%%BoundingBox"):
                _, x0, y0, x1, y1 = line.split()
                print(f"natural size: {(int(x1)-int(x0))/28.45:.1f} x {(int(y1)-int(y0))/28.45:.1f} cm")


if __name__ == "__main__":
    main()
