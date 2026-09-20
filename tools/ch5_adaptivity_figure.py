#!/usr/bin/env python3
"""Chapter 5 §5.3.2's one float from the defended corpus: Figure 5.4, what the
attacker does in the visits immediately before and immediately after each
defensive interrupt, the attacker model beside its verdict-blind control, in
the 2 x 2 of the spanning pair (IP shuffle; OS diversity) x tempo (200 s;
2 000 s).

Data: ``data/results/ch5_defended/numbers.json`` §s532 (design:
docs/handoffs/2026-09-17_ch5_s532_s55_defended_runs.md; read:
docs/implementation/pipeline/ogasp/ch5_s532_adaptivity_findings.md). Nothing
is typed here: every bar and every number a caption may quote is read from
that file and printed on stdout.

Each panel: one group per activity (the six verbs and dwell); in each group
the model's before and after shares as two bars in the model's hue (before
lighter), and the control's before and after shares in grey (before lighter).
The paired after-minus-before shift with its 95 % interval is printed per
activity for the caption; the panel prints its two before→after divergences.

Usage:
  python tools/ch5_adaptivity_figure.py [--numbers PATH] [--no-compile]

Writes docs/thesis/figures/fig_5-2-2a_adaptivity.{tex,pdf}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (ACTIVITY, FONT, LONG, PREAMBLE, REPO, axes, compile_fig,  # noqa: E402
                        fmt_thousands, panel_letter, write_fig)

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers.json"
STEM = "fig_5-2-2a_adaptivity"
PANEL_ORDER = ("ip_shuffle|200", "ip_shuffle|2000", "os_diversity|200", "os_diversity|2000")
LETTERS = "abcd"


def emit(s532: dict) -> tuple[str, dict]:
    acts = s532["activities"]
    n_act = len(acts)
    # geometry (cm): 2 x 2 panels, shared y; 15.7 cm packed
    PW, PH = 6.9, 3.3
    X0 = (1.25, 8.75)
    Y0 = (4.95, 0.75)
    ymax = 0.5
    bw = 0.17
    gap = 0.06

    def yv(y0, v):
        return y0 + v / ymax * PH

    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    facts = {}
    for k, key in enumerate(PANEL_ORDER):
        p = s532["panels"][key]
        col, row = k % 2, k // 2
        x0, y0 = X0[col], Y0[row]
        x1, y1 = x0 + PW, y0 + PH
        slot = PW / n_act
        xt = [(a, x0 + (i + 0.5) * slot) for i, a in enumerate(acts)]
        axes(w, x0, x1, y0, y1,
             xticks=[(ACTIVITY[a], x) for a, x in xt] if row == 1 else [],
             yticks=[(v, yv(y0, v)) for v in (0, 0.1, 0.2, 0.3, 0.4, 0.5)],
             xlabel="", ylabel=("share of visits" if col == 0 else ""), ylabels=(col == 0),
             xfmt=lambda v: v, xtick_rotate=35, ylabel_offset=0.8)
        if row == 0:
            for a, x in xt:
                w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, y0, x, y0 - 0.07))
        panel_letter(w, x0 - (1.1 if col == 0 else 0.45), y1 + 0.02, LETTERS[k])
        w(r"\node[anchor=north east,text=black!60] at (%.3f,%.3f) {%s, every %s\,s};" % (
            x1 - 0.05, y1 - 0.05, LONG[p["mechanism"]], fmt_thousands(p["interval"])))
        t, c = p["treatment"], p["control"]
        for a, x in xt:
            vals = [(t["before"][a], "cmov!45"), (t["after"][a], "cmov"),
                    (c["before"][a], "cbase!45"), (c["after"][a], "cbase")]
            for j, (v, fill) in enumerate(vals):
                xl = x - 2 * bw - gap / 2 + j * bw + (gap if j >= 2 else 0)
                w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (fill, xl, y0, xl + bw - 0.015, yv(y0, min(v, ymax))))
        facts[key] = {
            "mechanism": p["mechanism"], "interval": p["interval"],
            "interrupts_model": t["interrupts"], "interrupts_control": c["interrupts"],
            "jsd_model": t["jsd_before_after"], "jsd_control": c["jsd_before_after"],
            "jsd_placebo_model": p["placebo_treatment"]["jsd_before_after"],
            "shift_model": {a: (t["shift"][a]["mean"], t["shift"][a]["ci95"]) for a in acts if a in t["shift"]},
            "shift_control": {a: (c["shift"][a]["mean"], c["shift"][a]["ci95"]) for a in acts if a in c["shift"]},
            "hosts_model": p["hosts_treatment"]["mean"], "hosts_control": p["hosts_control"]["mean"],
        }
    # key, once, under the panels
    ky = Y0[1] - 2.25
    kx = X0[0]
    entries = [("cmov!45", "movement attacker, the five visits before"), ("cmov", "movement attacker, the five visits after"),
               ("cbase!45", "outcome-blind control, before"), ("cbase", "outcome-blind control, after")]
    for i, (fill, text) in enumerate(entries):
        xx = kx + (i % 2) * 7.5
        yy = ky - (i // 2) * 0.4
        w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (fill, xx, yy - 0.11))
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (xx + 0.4, yy, text))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n", facts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()
    data = json.loads(args.numbers.read_text(encoding="utf-8"))
    if not data["sanity"]["all_cells_100"] or data["sanity"]["error_rows"]:
        raise SystemExit("corpus sanity failed; not drawing from it")
    tex, facts = emit(data["s532"])
    write_fig(STEM, tex.splitlines())
    print("caption facts, Fig. 5.4:")
    for k, f in facts.items():
        print(f"  {k:20s} interrupts model {f['interrupts_model']:5d} control {f['interrupts_control']:5d}  "
              f"JSD model {f['jsd_model']:.4f} control {f['jsd_control']:.4f} placebo {f['jsd_placebo_model']}  "
              f"hosts model {f['hosts_model']:.2f} control {f['hosts_control']:.2f}")
        for a, (m, ci) in f["shift_model"].items():
            cm, cci = f["shift_control"].get(a, (0.0, 0.0))
            print(f"      {ACTIVITY[a]:16s} shift model {m:+.3f}±{ci:.3f}  control {cm:+.3f}±{cci:.3f}")
    if not args.no_compile:
        compile_fig(STEM)


if __name__ == "__main__":
    main()
