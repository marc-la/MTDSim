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

Style: the house results layout (figure_table_conventions.md §o, 2026-10-05):
TikZ standalone at 12 pt, Helvetica (helvet 0.92), packed to 15.7 cm and
included bare, a single-panel title, the key at the foot. The interval is a
95 % interval on the mean (normal approximation) over runs.
"""
from __future__ import annotations

import argparse
import math
import subprocess
from pathlib import Path

import pandas as pd

from _ch5_style import FONT, PREAMBLE, XTITLE_H, axes, errorbar, key_below, marker, panel_title  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
FIG_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_5-1a_sens_dwell_anchor"
# 2026-10-05 (Section 4.4.2 round 9, Marc: "switch it to NCR"): the y-axis is NCR
# (Equation eq:ncr, Section 4.5), hosts compromised over the network's 50 hosts.
N_HOSTS = 50
Y_STEP = 0.05

# command-line name -> (csv column, axis name, declared mean duration in s).
# 2026-10-05 (Section 4.4.2 round 5): the coined family names are cut; each
# shared mean duration is named by its value and its axis printed in seconds.
ANCHORS = {
    "scan": ("m_scan", "mean duration of reconnaissance and discovery", 35.0),
    "exploit": ("m_exploit", "mean duration of initial access and the three tactics set with it", 4.5),
    "stealth": ("m_stealth", "mean duration of persistence, stealth and command and control", 45.0),
    "objective": ("m_objective", "mean duration of collection, exfiltration and impact", 36.0),
}


def aggregate(csv: Path, anchor_col: str, reference_interval: float) -> pd.DataFrame:
    d = pd.read_csv(csv)
    d = d[(d.arm == "movement") & (d.family == "exponential")]
    others = [c for c, _, _ in ANCHORS.values() if c != anchor_col]
    for c in others:
        d = d[d[c] == 1.0]
    off = d[d.mtd_interval.isna()].assign(condition="none")
    on = d[d.mtd_interval == reference_interval].assign(condition="reference")
    a = pd.concat([off, on])
    a = a.assign(ncr=a.compromised_count / N_HOSTS)
    g = a.groupby(["condition", anchor_col]).ncr.agg(["mean", "std", "count"]).reset_index()
    g["ci"] = 1.96 * g["std"] / g["count"].pow(0.5)
    g = g.rename(columns={anchor_col: "mult"})
    return g.sort_values(["condition", "mult"])


def emit(g: pd.DataFrame, anchor_name: str, reference_interval: float, declared_s: float) -> str:
    """The house results layout (figure_table_conventions.md §o, applied
    2026-10-05): a single-panel title with no letter, the y-axis title in
    sentence case, the key at the foot, packed to 15.7 cm and included bare.
    Both series are the APT attacker model averaged over c_1 to c_4: under MTD
    black and filled, with no MTD grey and open (Figure E.1's two arms of one
    model); grey dashed with a square stays the baseline attacker's alone."""
    mults = sorted(g["mult"].unique())
    lo, hi = min(mults), max(mults)
    ymax = float((g["mean"] + g["ci"]).max())
    n_ticks = math.ceil(ymax / Y_STEP - 1e-9)
    ytop = n_ticks * Y_STEP

    X0, X1 = 1.55, 15.9
    Y0, Y1 = 0.0, 4.2

    def xs(m: float) -> float:
        # the end markers sit off the frame, as Figure E.1's
        pad = 0.07 * (math.log2(hi) - math.log2(lo))
        return X0 + (math.log2(m) - math.log2(lo) + pad) / (math.log2(hi) - math.log2(lo) + 2 * pad) * (X1 - X0)

    def ys(v: float) -> float:
        return Y0 + v / ytop * (Y1 - Y0)

    series = [  # condition, colour, marker, key label; drawn in this order (under MTD on top)
        ("none", "black!45", "ocircle", "no MTD"),
        ("reference", "black", "circle", r"random, %d\,s" % reference_interval),
    ]

    L = PREAMBLE[:-1] + [r"\begin{document}",
                         r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT]
    w = L.append
    xt, m = [], lo
    while m <= hi * 1.0001:
        xt.append((m, xs(m)))
        m *= 2
    axes(w, X0, X1, Y0, Y1,
         xticks=xt, yticks=[(k * Y_STEP, ys(k * Y_STEP)) for k in range(n_ticks + 1)],
         xlabel="Mean duration (s)", ylabel="NCR", ylabel_offset=0.95,
         xfmt=lambda v: ("%g" % (v * declared_s)) if v != 1 else "%g (declared)" % declared_s,
         yfmt=lambda v: f"{v:.2f}")
    # the declared value, a reference line, never a series
    w(r"\draw[black!30,line width=0.3pt,dash pattern=on 1.5pt off 1.5pt] (%.3f,%.2f) -- (%.3f,%.2f);"
      % (xs(1.0), Y0, xs(1.0), Y1))
    panel_title(w, X0, Y1, _cap(anchor_name))
    for cond, col, mark, _ in series:
        rows = g[g.condition == cond].sort_values("mult")
        pts = [(xs(r["mult"]), r["mean"], r["ci"]) for _, r in rows.iterrows()]
        w(r"\draw[%s,line width=0.8pt] %s;" % (col, " -- ".join("(%.3f,%.3f)" % (x, ys(v)) for x, v, _ in pts)))
        for x, v, ci in pts:
            errorbar(w, x, ys(v - ci), ys(v + ci), col=col, cap=0.045)
            marker(w, mark, col, x, ys(v), r=0.07)
    key_below(w, X0, Y0 - 0.5 - XTITLE_H, [(lab, "line", col, mk) for _, col, mk, lab in reversed(series)])
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:]


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

    col, name, declared_s = ANCHORS[args.anchor]
    g = aggregate(args.csv, col, args.reference_interval)
    if g.empty:
        raise SystemExit(f"no rows for anchor {args.anchor} at interval {args.reference_interval} in {args.csv}")

    tex = emit(g, name, args.reference_interval, declared_s)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    (FIG_DIR / f"{STEM}.tex").write_text(tex)
    print(f"wrote {(FIG_DIR / (STEM + '.tex')).relative_to(REPO)}")

    print(f"source={args.csv.relative_to(REPO) if args.csv.is_absolute() else args.csv}  anchor={name}  "
          f"reference interval={args.reference_interval:g} s  runs per cell={int(g['count'].iloc[0])}")
    for cond in ("none", "reference"):
        rows = g[g.condition == cond]
        print(f"  {cond:9s}: " + "; ".join(f"x{r['mult']:g} = {r['mean']:.3f} +/- {r['ci']:.3f}" for _, r in rows.iterrows()))

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
