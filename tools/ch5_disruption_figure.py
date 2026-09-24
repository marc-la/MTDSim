#!/usr/bin/env python3
"""Chapter 5 §5.3.1's one float, Figure 5.3: what an MTD deployment does to each
attacker, and what it costs each.

REBUILT 2026-09-24 on Marc's ruling and two review rounds (results context
handoff §8g-5). The takeaways it is built to carry, and nothing else:
  R1  a deployment knocks each attacker down: its compromise rate drops when
      the deployment completes;
  R2  the mechanism that knocks an attacker down hardest also keeps it down
      longest (recovery follows the mechanism, not the attacker: pooled over
      mechanisms the baseline attacker looked quick to recover, which review
      round 1 showed was the mix of mechanisms, not the attacker);
  R3  the mechanism that costs one attacker most is not the one that costs the
      other most.

  (a), (b) NCR growth rate around a deployment of the mechanism that costs
      each attacker most (chosen by rule from (c), never typed): hosts
      compromised per unit of live time, 750 s before to 1 250 s after the
      deployment completes, as a percentage of the attacker's own rate before;
      both attackers in each panel; the shaded band is the deployment running
      (its median duration), 0 is when it completes.
  (c) Time lost per MTD deployment (the name ruled 2026-09-24), per mechanism, both attackers, with seeded
      bootstrap intervals (the area of the dip, as seconds at the attacker's
      own pace, less the same read at the same moments with no defence).

Both at the 2 000 s deployment interval (at 200 s the next deployment lands
inside the window; that interval is a body sentence, printed below).

Data: data/results/ch5_defended/disruption_numbers.json (disruption.py beside
the corpus). Nothing is typed. Earlier forms are in git history.

Usage:
  python tools/ch5_disruption_figure.py [--numbers PATH] [--no-compile]

Writes docs/thesis/figures/fig_5-2-2a_disruption_response.{tex,pdf}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (FONT, LABEL, LONG, PREAMBLE, REPO, axes, compile_fig, errorbar,  # noqa: E402
                        fmt_thousands, marker, panel_letter, write_fig)
from ch5_effectiveness_figures import LAYER, PANEL_SINGLES, TICK  # noqa: E402

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "disruption_numbers.json"
STEM = "fig_5-2-2a_disruption_response"
INTERVAL = 2000
ARMS = (("movement", "cmov", "circle"), ("baseline", "cbase", "square"))


def signed(v: float) -> str:
    return (r"$-$" + fmt_thousands(-v)) if v < 0 else fmt_thousands(v)


def emit(d: dict) -> tuple[str, list[str]]:
    edges = d["edges"]
    mids = [(a + b) / 2 for a, b in zip(edges[:-1], edges[1:])]
    R = d["reads"]
    tl = {(a, m): R[f"{a}|{m}|{INTERVAL}"]["time_lost"] for a, _, _ in ARMS for m in PANEL_SINGLES}
    worst = {a: max(PANEL_SINGLES, key=lambda m: tl[(a, m)]["seconds"]) for a, _, _ in ARMS}
    X0, X1 = 1.45, 15.2
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    facts: list[str] = []

    # ---- (a), (b): the curve around a deployment of each attacker's worst mechanism
    AY0, AH, YMAX = 6.55, 3.7, 125.0
    ay1 = AY0 + AH
    GAP = 0.9
    PW = (X1 - X0 - GAP) / 2
    tmin, tmax = edges[0], edges[-1]
    for k, (arm_worst, letter) in enumerate((("movement", "a"), ("baseline", "b"))):
        m = worst[arm_worst]
        x0 = X0 + k * (PW + GAP)
        x1 = x0 + PW

        def xa(t, x0=x0, x1=x1):
            return x0 + (t - tmin) / (tmax - tmin) * (x1 - x0)

        def ya(v):
            return AY0 + max(0.0, min(v, YMAX)) / YMAX * AH

        axes(w, x0, x1, AY0, ay1,
             xticks=[(t, xa(t)) for t in range(-500, 1001, 500)],
             yticks=[(v, ya(v)) for v in (0, 25, 50, 75, 100, 125)],
             xlabel="", ylabel="", ylabels=(k == 0), xfmt=signed)
        dur = R[f"movement|{m}|{INTERVAL}"]["deployment_seconds_median"]
        w(r"\fill[black!10] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xa(-dur), AY0, xa(0), ay1))
        # the band is named from above, over the band itself (Marc 2026-09-24: a label
        # to its left read as "the deployment happens before the band")
        w(r"\node[anchor=south,text=black!60] at (%.3f,%.3f) {MTD deployment};" % (xa(-dur / 2), ay1 + 0.04))
        w(r"\draw[black!55,line width=0.4pt,dash pattern=on 1pt off 1.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, ya(100), x1, ya(100)))
        panel_letter(w, x0 - (1.35 if k == 0 else 0.5), ay1 + 0.02, letter)
        w(r"\node[anchor=south east] at (%.3f,%.3f) {%s};" % (x1, ay1 + 0.04, LONG[m]))
        # the dip, shaded under the 100 % line from the moment the deployment
        # completes: (c)'s bar is this area (Marc 2026-09-24: read as a point on the
        # time axis, the seconds in (c) did not match anything in (a)/(b)). Drawn
        # before the lines so they sit on top; clipped to below the line.
        for arm, col, _ in ARMS:
            c = R[f"{arm}|{m}|{INTERVAL}"]
            tv = list(zip(mids, c["relative_pct"]))
            i0 = next(i for i, (t, _) in enumerate(tv) if t > 0)
            (ta, va), (tb, vb) = tv[i0 - 1], tv[i0]
            v0 = va + (vb - va) * (0 - ta) / (tb - ta)  # the curve at t = 0
            poly = [(xa(0), ya(100)), (xa(0), ya(v0))] + [(xa(t), ya(v)) for t, v in tv[i0:]] + [(xa(tv[-1][0]), ya(100))]
            w(r"\begin{scope}\clip (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x0, AY0, x1, ya(100)))
            w(r"\fill[%s,opacity=%s] %s -- cycle;" % (col, "0.16" if arm == "movement" else "0.22",
                                                    " -- ".join("(%.3f,%.3f)" % p for p in poly)))
            w(r"\end{scope}")
        for arm, col, mk in ARMS:
            c = R[f"{arm}|{m}|{INTERVAL}"]
            pts = [(xa(t), ya(v)) for t, v in zip(mids, c["relative_pct"])]
            dash = ",dash pattern=on 3pt off 1.8pt" if arm == "baseline" else ""  # the chapter's contract: the baseline is dashed grey
            w(r"\draw[%s,line width=0.8pt%s] %s;" % (col, dash, " -- ".join("(%.3f,%.3f)" % p for p in pts)))
            for x, y in pts:
                marker(w, mk, col, x, y, r=0.06)
            after = [v for t, v in zip(mids, c["relative_pct"]) if t > 0]
            facts.append(f"({letter}) {LONG[m]:18s} {arm:9s} deployments {c['deployments']:5d}  first 125 s {after[0]:.0f} %  "
                         f"at 1 000-1 250 s {after[-1]:.0f} %  rate before {c['pre_rate_per_ksec']:.2f} per 1 000 s  "
                         f"(deployment runs {dur:.0f} s)")
    w(r"\node[anchor=north] at (%.3f,%.3f) {time since the MTD deployment completed (s)};" % ((X0 + X1) / 2, AY0 - 0.42))
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {NCR growth rate (\%% of\\pre-deployment rate)};" % (X0 - 0.85, (AY0 + ay1) / 2))

    # ---- (c) time lost per deployment, per mechanism ------------------------
    BY0, BH = 1.55, 2.9
    by1 = BY0 + BH
    lo_v = min(v["lo"] for v in tl.values())
    hi_v = max(v["hi"] for v in tl.values())
    YB0 = -200.0 * (int(-lo_v // 200) + 1) if lo_v < 0 else 0.0
    YB1 = 200.0 * (int(hi_v // 200) + 1)

    def yb(v):
        return BY0 + (max(YB0, min(YB1, v)) - YB0) / (YB1 - YB0) * BH

    slot = (X1 - X0) / len(PANEL_SINGLES)
    bw = 0.34
    xt = [(m, X0 + (i + 0.5) * slot) for i, m in enumerate(PANEL_SINGLES)]
    axes(w, X0, X1, BY0, by1,
         xticks=[(TICK[m], x) for m, x in xt],
         yticks=[(v, yb(v)) for v in range(int(YB0), int(YB1) + 1, 200)],
         xlabel="", ylabel="", xfmt=lambda v: v, yfmt=signed)
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {time lost per\\MTD deployment (s)};" % (X0 - 0.85, (BY0 + by1) / 2))
    w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (X0, yb(0), X1, yb(0)))
    panel_letter(w, X0 - 1.35, by1 + 0.02, "c")
    for m, x in xt:
        for j, (arm, col, _) in enumerate(ARMS):
            v = tl[(arm, m)]
            xl = x - bw + j * bw
            top, bot = yb(max(v["seconds"], 0)), yb(min(v["seconds"], 0))
            if arm == "movement":
                w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xl, bot, xl + bw - 0.03, top))
            else:
                w(r"\fill[pattern=north east lines,pattern color=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xl, bot, xl + bw - 0.03, top))
                w(r"\draw[%s,line width=0.3pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (col, xl, bot, xl + bw - 0.03, top))
            if top - bot < 0.03:  # a value near zero: a stub at it, so it does not read as missing
                w(r"\draw[%s,line width=0.8pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, xl, yb(v["seconds"]), xl + bw - 0.03, yb(v["seconds"])))
            errorbar(w, xl + (bw - 0.03) / 2, yb(v["lo"]), yb(v["hi"]), col="black!70", cap=0.035)
            facts.append(f"(c) {arm:9s} {m:18s} time lost {v['seconds']:5.0f} s [{v['lo']:5.0f}, {v['hi']:5.0f}]  "
                         f"({v['hosts_per_deployment']:.3f} hosts; uncorrected {v['uncorrected_seconds']:.0f}, placebo {v['placebo_seconds']:.0f})")
    ybk = BY0 - 1.35   # under three-line ticks
    i = 0
    while i < len(PANEL_SINGLES):
        j = i
        while j + 1 < len(PANEL_SINGLES) and LAYER[PANEL_SINGLES[j + 1]] == LAYER[PANEL_SINGLES[i]]:
            j += 1
        xa_, xb_ = X0 + i * slot + 0.12, X0 + (j + 1) * slot - 0.12
        w(r"\draw[black!50,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);" % (
            xa_, ybk + 0.08, xa_, ybk, xb_, ybk, xb_, ybk + 0.08))
        w(r"\node[anchor=north,text=black!60] at (%.3f,%.3f) {%s};" % ((xa_ + xb_) / 2, ybk - 0.03, LAYER[PANEL_SINGLES[i]]))
        i = j + 1

    # ---- key, once, between the rows (both rows share the encoding) --------
    ky = AY0 - 1.05
    xx = X0
    for arm, col, mk in ARMS:
        if arm == "movement":
            w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (col, xx, ky - 0.11))
        else:
            w(r"\fill[pattern=north east lines,pattern color=%s] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (col, xx, ky - 0.11))
            w(r"\draw[%s,line width=0.3pt] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (col, xx, ky - 0.11))
        w(r"\draw[%s,line width=0.8pt%s] (%.3f,%.3f) -- ++(0.5,0);" % (col, ",dash pattern=on 3pt off 1.8pt" if arm == "baseline" else "", xx + 0.42, ky))
        marker(w, mk, col, xx + 0.67, ky, r=0.06)
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (xx + 1.0, ky, LABEL[arm]))
        xx += 4.4
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    facts.insert(0, "worst mechanism by rule (largest time lost): " + ", ".join(f"{a} -> {m}" for a, m in worst.items()))
    return "\n".join(L) + "\n", facts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    d = json.loads(args.numbers.read_text(encoding="utf-8"))
    tex, facts = emit(d)
    write_fig(STEM, tex.splitlines())
    print(f"caption and body facts, Fig. 5.3 (§5.3.1), drawn at {INTERVAL} s:")
    for f in facts:
        print("  " + f)
    R = d["reads"]
    n_before = len([e for e in d["edges"][:-1] if e < 0])
    for key in ("all", "host", "service"):
        for a, _, _ in ARMS:
            c = R[f"{a}|{key}|{INTERVAL}"]
            print(f"  body: {a:9s} {key:8s} first 125 s {c['relative_pct'][n_before]:.0f} %")
    print("  no-defence compromise rate per 1 000 s: " + ", ".join(f"{a} {v:.2f}" for a, v in d["none_rate_per_ksec"].items()))
    if "movement|host|200" in R:
        print("  at 200 s (body sentence: the rate before each deployment, against no defence):")
        for a, _, _ in ARMS:
            for key in ("host", "service"):
                c = R[f"{a}|{key}|200"]
                print(f"    {a:9s} {key:8s} {c['pre_rate_per_ksec']:.2f} per 1 000 s "
                      f"({100 * c['pre_rate_per_ksec'] / d['none_rate_per_ksec'][a]:.0f} % of no defence)")
    if not args.no_compile:
        compile_fig(STEM)


if __name__ == "__main__":
    main()
