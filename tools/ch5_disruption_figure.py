#!/usr/bin/env python3
"""Chapter 5 §5.2.2's one float: Figure 5.2, the movement attacker's response to
disruption read at the resolution the model lives at (the tactic-level record),
not the six verbs (the 2026-09-17 adaptivity figure, retired 2026-09-22: the
verb is downstream of the mapping, so a verb-level mix inherits the baseline
attacker's shape by construction).

Design: docs/handoffs/2026-09-20_ch5_s52_s54_results_context.md §8g
(takeaways T5-T8, ratified 2026-09-22; the panel definitions amended on the
preliminary read the same day). Data: ``data/results/ch5_defended/numbers.json``
§s522 (analyse.py section_522). Nothing is typed here: every mark and every
number a caption may quote is read from that file and printed.

  (a) the response — the share of the attacker's steps that are refused
      actions (the substrate turns the verb away: no host in hand, no port
      found) at each step from five before to five after a disruption, pooled
      over the four profiles and over the single-mechanism conditions of each
      layer, at the long interval (the short interval's windows overlap: the
      next disruption lands before the last is recovered from);
  (b) the recovery — time from a disruption to the next host compromise as a
      multiple of that attacker's own mean gap between compromises with no
      defence (Marc's ruling 2026-09-22, third scrutinise round: the absolute
      form read as pace, T4, to three cold readers), per layer hit, both
      attackers; the interval is a seeded bootstrap on the ratio, both pools
      resampled by run; the censored share printed over each bar; a hollow
      circle at each mechanism's own ratio, so a layer bar that is one
      mechanism's doing (the baseline attacker under service diversity) reads
      as such. ``--absolute`` restores the first form.

The credential layer is not drawn: it reaches the attacker less than once per
run at this interval (its numbers are printed for the body text). The position
by lifecycle stage and the control at stage level are printed, not drawn: both
are flat (the record's §s522 carries them).

Usage:
  python tools/ch5_disruption_figure.py [--numbers PATH] [--interval 2000] [--no-compile]

Writes docs/thesis/figures/fig_5-2-2a_disruption_response.{tex,pdf}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (FONT, PREAMBLE, REPO, axes, compile_fig, errorbar,  # noqa: E402
                        fmt_thousands, marker, panel_letter, write_fig)

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers.json"
STEM = "fig_5-2-2a_disruption_response"
STAGES = ("0", "1", "2", "3")
STAGE_LABEL = {"0": "preparation", "1": "intrusion", "2": "post-intrusion", "3": "objective"}
DRAWN = (("network", "host"), ("application", "service"))
ALL = DRAWN + (("reserve", "credentials"),)
# panel (a) is the movement attacker only, so it is drawn in greys: the accent
# hue stays the movement attacker's in panel (b) and means one thing in the figure
LAYER_STYLE = {"network": ("black!85", "circle", "solid"), "application": ("black!45", "square", "solid")}


def emit(s522: dict, interval: int, relative: bool = True, band: bool = True, split: bool = False, marks: bool = True) -> tuple[str, dict]:
    offsets = [int(o) for o in s522["offsets"]]
    lay = {k: s522["layers"][f"{k}|{interval}"] for k, _ in ALL}
    gap = s522["unopposed_gap"]
    # geometry (cm), packed to 15.7
    AX0, AW, H, Y0 = 1.45, 7.5, 4.8, 0.9
    BX0, BW = 10.65, 4.55
    if split:
        AX0, AW = 1.45, 6.3
        BX0, BW = 9.0, 2.7        # (b) the movement attacker
        CX0, CW = 12.55, 2.5      # (c) the baseline attacker, its own scale
    ay1 = Y0 + H
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)

    # ---- (a) refused-action share by offset, per layer ----------------------
    slot = AW / (len(offsets) + 1)  # one empty slot at offset 0

    def xa(o: int) -> float:
        i = offsets.index(o)
        return AX0 + (i + 0.5 + (1 if o > 0 else 0)) * slot

    x_zero = AX0 + 5.5 * slot
    ytop_a = 0.6

    def ya(v: float) -> float:
        return Y0 + v / ytop_a * H

    axes(w, AX0, AX0 + AW, Y0, ay1,
         xticks=[(o, xa(o)) for o in offsets],
         yticks=[(v, ya(v)) for v in (0, 0.2, 0.4, 0.6)],
         xlabel="steps from the disruption", ylabel="",
         xfmt=lambda v: f"{v:+d}", xlabel_offset=0.45)
    w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {share of steps whose\\action fails its precondition};" % (AX0 - 0.8, (Y0 + ay1) / 2))
    if band:
        # the disruption's own step, as a shaded slot between the two windows
        w(r"\fill[black!8] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (x_zero - slot / 2, Y0, x_zero + slot / 2, ay1))
        w(r"\node[anchor=north,rotate=90,text=black!60] at (%.3f,%.3f) {disruption};" % (x_zero, ay1 - 0.08))
    else:
        w(r"\draw[black!50,dashed,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x_zero, Y0, x_zero, ay1))
        w(r"\node[anchor=north,rotate=90,text=black!60] at (%.3f,%.3f) {disruption};" % (x_zero + 0.12, ay1 - 0.08))
    panel_letter(w, AX0 - 1.35, ay1 + 0.02, "a")
    refused = {}
    for layer, _ in DRAWN:
        col, mk, _ = LAYER_STYLE[layer]
        m = lay[layer]["movement"]
        refused[layer] = {o: m["refused_by_offset"][str(o)]["blocked"] for o in offsets}
        for side in ((-5, -1), (1, 5)):
            pts = [o for o in offsets if side[0] <= o <= side[1]]
            path = " -- ".join("(%.3f,%.3f)" % (xa(o), ya(refused[layer][o])) for o in pts)
            w(r"\draw[%s,line width=0.7pt] %s;" % (col, path))
            for o in pts:
                marker(w, mk, col, xa(o), ya(refused[layer][o]), r=0.065)

    # ---- (b) recovery to the next compromise, per layer ----------------------
    vals = {}
    conds = {}
    for layer, _ in DRAWN:
        for arm in ("movement", "baseline"):
            rc = lay[layer][arm]["recovery_to_compromise"]
            m = rc["mean_observed"]
            vals[(layer, arm)] = (m["mean"] if m else 0.0, m["ci95"] if m else 0.0, rc["censored_share"] or 0.0, rc["n"])
            conds[(layer, arm)] = [
                (c, s522["conditions"][f"{c}|{interval}"][arm]["recovery_to_compromise"]["mean_observed"]["mean"])
                for c in lay[layer]["conditions"]]
    ref = {arm: gap[arm]["mean"]["mean"] for arm in ("movement", "baseline")}
    ratio_iv = {}
    if relative:
        # the point is the ratio of pooled means; the interval is the seeded
        # bootstrap on the ratio (analyse.py recovery_ratio), both pools by run
        for (l, a), (m, ci, cens, n) in list(vals.items()):
            rr = lay[l]["recovery_ratio"][a]
            point = rr["point"] if rr.get("point") is not None else m / ref[a]
            lo = rr.get("lo", point - ci / ref[a])
            hi = rr.get("hi", point + ci / ref[a])
            ratio_iv[(l, a)] = (point, lo, hi)
            vals[(l, a)] = (point, max(point - lo, hi - point), cens, n)
        conds = {(l, a): [(c, v / ref[a]) for c, v in cs] for (l, a), cs in conds.items()}
        ref = {arm: 1.0 for arm in ref}

    def recovery_panel(x0, width, arms, letter, ylabel_lines, title=None, cond_marks=False):
        ymax = max((vals[(l, a)][0] + vals[(l, a)][1]) for l, _ in DRAWN for a in arms)
        ymax = max(ymax, *(ref[a] for a in arms))
        if cond_marks:
            ymax = max(ymax, *(v for l, _ in DRAWN for a in arms for _, v in conds[(l, a)]))
        if relative:
            step = 0.5
        else:
            step = 1000 if ymax > 2500 else 500 if ymax > 1000 else 200
        ytop = step * (int(ymax // step) + 1)

        def yb(v):
            return Y0 + v / ytop * H

        gslot = width / len(DRAWN)
        nb = len(arms)
        bw = gslot * (0.34 if nb == 2 else 0.42)
        xticks = [(lab, x0 + (i + 0.5) * gslot) for i, (_, lab) in enumerate(DRAWN)]
        axes(w, x0, x0 + width, Y0, ay1,
             xticks=xticks, yticks=[(v, yb(v)) for v in [i * step for i in range(int(round(ytop / step)) + 1)]],
             xlabel="layer rewritten", ylabel="",
             xfmt=lambda v: v, yfmt=(lambda v: f"{v:g}") if relative else (lambda v: fmt_thousands(v)), xlabel_offset=0.45)
        if ylabel_lines:
            w(r"\node[rotate=90,anchor=south,align=center] at (%.3f,%.3f) {%s};" % (x0 - (1.0 if not relative else 0.8), (Y0 + ay1) / 2, ylabel_lines))
        panel_letter(w, x0 - (1.5 if ylabel_lines else 0.85), ay1 + 0.02, letter)
        if title:
            w(r"\node[anchor=north west,text=black!60] at (%.3f,%.3f) {%s};" % (x0 + 0.08, ay1 - 0.05, title))
        if relative:
            w(r"\draw[black!60,dashed,line width=0.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, yb(1.0), x0 + width, yb(1.0)))
        else:
            for a in arms:
                col = "cmov" if a == "movement" else "cbase"
                w(r"\draw[%s,dashed,line width=0.5pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (col, x0, yb(ref[a]), x0 + width, yb(ref[a])))
        for i, (layer, _) in enumerate(DRAWN):
            xc = x0 + (i + 0.5) * gslot
            for j, a in enumerate(arms):
                mean, ci, cens, n = vals[(layer, a)]
                xl = xc + (j - nb / 2) * bw + 0.03
                xr = xl + bw - 0.06
                if a == "movement":
                    w(r"\fill[cmov] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xl, Y0, xr, yb(mean)))
                else:
                    w(r"\fill[pattern=north east lines,pattern color=cbase] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xl, Y0, xr, yb(mean)))
                    w(r"\draw[cbase,line width=0.4pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (xl, Y0, xr, yb(mean)))
                if relative and (layer, a) in ratio_iv:
                    _, lo, hi = ratio_iv[(layer, a)]
                else:
                    lo, hi = mean - ci, mean + ci
                errorbar(w, (xl + xr) / 2, yb(max(0.0, lo)), yb(min(ytop, hi)), col="black!70", cap=0.04)
                top = yb(min(ytop, hi))
                if cond_marks:
                    for _, v in conds[(layer, a)]:
                        # on the bar's own right third, clear of its whisker and of the next bar
                        w(r"\draw[black!75,line width=0.4pt,fill=white] (%.3f,%.3f) circle (0.05cm);" % (xl + 0.78 * (xr - xl), yb(min(ytop, v))))
                w(r"\node[anchor=south,text=black!70,font=\scriptsize] at (%.3f,%.3f) {%d\,\%%};" % (
                    (xl + xr) / 2, top + 0.05, round(100 * cens)))
        return ytop

    if split:
        ylab = ("time to the next compromise,\\\\as a multiple of the gap with no defence" if relative
                else "time to the next\\\\compromise (s)")
        ytop = recovery_panel(BX0, BW, ("movement",), "b", ylab, title="movement attacker", cond_marks=True)
        recovery_panel(CX0, CW, ("baseline",), "c", "", title="baseline attacker", cond_marks=True)
    else:
        ylab = ("time to the next compromise\\\\$\\div$ gap with no defence" if relative
                else "time to the next\\\\compromise (s)")
        ytop = recovery_panel(BX0, BW, ("movement", "baseline"), "b", ylab, cond_marks=marks)

    # ---- key, once, under both panels ---------------------------------------
    ky = Y0 - 1.35
    KX = (AX0, AX0 + 4.4)
    for i, (layer, lab) in enumerate(DRAWN):
        col, mk, _ = LAYER_STYLE[layer]
        xx = KX[i]
        w(r"\draw[%s,line width=0.7pt] (%.3f,%.3f) -- ++(0.45,0);" % (col, xx, ky))
        marker(w, mk, col, xx + 0.225, ky, r=0.065)
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s-layer mechanism};" % (xx + 0.55, ky, lab))
    r2 = ky - 0.42
    w(r"\fill[cmov] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (KX[0], r2 - 0.11))
    w(r"\node[anchor=west] at (%.3f,%.3f) {movement attacker};" % (KX[0] + 0.4, r2))
    w(r"\fill[pattern=north east lines,pattern color=cbase] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (KX[1], r2 - 0.11))
    w(r"\draw[cbase,line width=0.4pt] (%.3f,%.3f) rectangle ++(0.3,0.22);" % (KX[1], r2 - 0.11))
    w(r"\node[anchor=west] at (%.3f,%.3f) {baseline attacker};" % (KX[1] + 0.4, r2))
    r3 = ky - 0.84
    if relative:
        w(r"\draw[black!60,dashed,line width=0.5pt] (%.3f,%.3f) -- ++(0.45,0);" % (AX0, r3))
        w(r"\node[anchor=west] at (%.3f,%.3f) {the attacker's own pace: its mean gap between compromises with no defence};" % (AX0 + 0.55, r3))
    else:
        w(r"\draw[cmov,dashed,line width=0.5pt] (%.3f,%.3f) -- ++(0.45,0);" % (AX0, r3))
        w(r"\draw[cbase,dashed,line width=0.5pt] (%.3f,%.3f) -- ++(0.45,0);" % (AX0 + 0.55, r3))
        w(r"\node[anchor=west] at (%.3f,%.3f) {dashed, in the attacker's colour: its mean gap between compromises with no defence};" % (AX0 + 1.1, r3))
    w(r"\node[anchor=west] at (%.3f,%.3f) {\%%~~share of recoveries not completed by the time limit};" % (AX0, ky - 1.26))
    if split or marks:
        w(r"\draw[black!75,line width=0.4pt,fill=white] (%.3f,%.3f) circle (0.055cm);" % (AX0 + 8.0 + 0.225, ky - 1.26))
        w(r"\node[anchor=west] at (%.3f,%.3f) {each mechanism of the layer alone};" % (AX0 + 8.55, ky - 1.26))
    w(r"\end{tikzpicture}")
    w(r"\end{document}")

    facts = {"interval": interval, "refused": refused, "recovery": {f"{l}|{a}": v for (l, a), v in vals.items()},
             "reference_gap": ref, "ytop": ytop}
    return "\n".join(L) + "\n", facts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--numbers", type=Path, default=NUMBERS)
    ap.add_argument("--interval", type=int, default=2000)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--absolute", action="store_true", help="panel (b) in seconds with each attacker's pace line (the 2026-09-22 first form)")
    ap.add_argument("--no-band", action="store_true", help="panel (a): dashed line at the disruption instead of the shaded slot")
    ap.add_argument("--split", action="store_true", help="one recovery panel per attacker, own scale, per-mechanism marks")
    ap.add_argument("--no-marks", action="store_true", help="drop the per-mechanism marks on the layer bars")
    ap.add_argument("--stem", default=STEM)
    args = ap.parse_args()
    data = json.loads(args.numbers.read_text(encoding="utf-8"))
    if not data["sanity"]["all_cells_100"] or data["sanity"]["error_rows"]:
        raise SystemExit("corpus sanity failed; not drawing from it")
    s522 = data["s522"]
    tex, facts = emit(s522, args.interval, relative=not args.absolute, band=not args.no_band, split=args.split, marks=not args.no_marks)
    write_fig(args.stem, tex.splitlines())
    offsets = [int(o) for o in s522["offsets"]]
    print(f"caption facts, Fig. 5.2 (§5.2.2), drawn at {args.interval} s:")
    for interval in (200, 2000):
        print(f"  refused share by offset at {interval} s (movement; control where run):")
        for layer, lab in ALL:
            m = s522["layers"][f"{layer}|{interval}"]["movement"]
            print(f"    {lab:12s} n/run {m['interrupts_per_run']['mean']:5.1f}  " +
                  " ".join(f"{o:+d}:{m['refused_by_offset'][str(o)]['blocked']:.2f}" for o in offsets))
        for cond in ("ip_shuffle", "os_diversity"):
            c = s522["conditions"][f"{cond}|{interval}"]
            print(f"    control {cond:13s} " + " ".join(f"{o:+d}:{c['control']['refused_by_offset'][str(o)]['blocked']:.2f}" for o in offsets)
                  + f"   model {cond}: " + " ".join(f"{o:+d}:{c['movement']['refused_by_offset'][str(o)]['blocked']:.2f}" for o in offsets))
        print(f"  position by stage at {interval} s (before -> after, JSD):")
        for layer, lab in ALL:
            m = s522["layers"][f"{layer}|{interval}"]["movement"]
            print(f"    {lab:12s} " + "  ".join(f"{STAGE_LABEL[k]} {m['stage']['before'][k]:.3f}->{m['stage']['after'][k]:.3f}" for k in STAGES)
                  + f"  JSD {m['stage']['jsd_before_after']:.4f}  tactic JSD {m['tactic']['jsd_before_after']:.4f}  whole-run tactic JSD vs none {m['whole_run_tactic_jsd_vs_none']:.4f}")
        print(f"  recovery to the next compromise at {interval} s:")
        for layer, lab in ALL:
            for arm in ("movement", "baseline"):
                rc = s522["layers"][f"{layer}|{interval}"][arm]["recovery_to_compromise"]
                m = rc["mean_observed"]
                print(f"    {lab:12s} {arm:9s} n {rc['n']:6d}  mean {m['mean'] if m else 0:8.0f} ± {m['ci95'] if m else 0:5.0f} s  "
                      f"median {rc['median_observed'] or 0:7.0f}  censored {rc['censored_share']:.3f}")
        for layer, lab in ALL:
            b = s522["layers"][f"{layer}|{interval}"]["baseline"]
            print(f"    baseline landing after a {lab} mechanism ({b['interrupts']} disruptions): {b['landing']}")
    g = s522["unopposed_gap"]
    for arm in ("movement", "baseline"):
        print(f"  unopposed gap between compromises, {arm}: mean {g[arm]['mean']['mean']:.0f} ± {g[arm]['mean']['ci95']:.0f} s, "
              f"median {g[arm]['median']:.0f}, gaps {g[arm]['n_gaps']}, runs without a gap {g[arm]['runs_without_gap_share']:.2f}")
    if not args.no_compile:
        compile_fig(args.stem)


if __name__ == "__main__":
    main()
