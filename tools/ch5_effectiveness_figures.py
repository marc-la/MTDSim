#!/usr/bin/env python3
"""Chapter 5 §5.4 floats from the defended corpus.

  §5.4.1  Fig. 5.5  suppression of host breadth by defence condition, per
                    profile (2 x 2 lettered panels: singles / schemes at each
                    interval; series = profile, the chapter's hues)
          Tab. 5.5  the conditions against the attacker model: suppression,
                    delay to first compromise with censoring, blocked fraction
  §5.4.2  Fig. 5.6  the same defences against both attackers (series = arm;
                    the baseline hatched, the model solid)
          Tab. 5.6  the two orderings side by side, the rank statistic and
                    its interval, the family contrast in the footnote
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
  docs/thesis/figures/fig_5-4-1a_suppression_profiles.{tex,pdf}
  docs/thesis/figures/fig_5-4-2a_cross_arm.{tex,pdf}
  docs/thesis/tables/tab_5-4-1a_conditions.tex
  docs/thesis/tables/tab_5-4-2a_orderings.tex
  docs/thesis/tables/tab_5-4-3a_lineage.tex
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _ch5_style import (CNAME, DEFENDED, FONT, LABEL, LONG, MARK, PREAMBLE, PROFILES,  # noqa: E402
                        REPO, SCHEMES, SHORT, SINGLES, TAB_DIR, axes, compile_fig, errorbar,
                        fmt_thousands, marker, panel_letter, pm, write_fig)

NUMBERS = REPO / "data" / "results" / "ch5_defended" / "numbers.json"
STEM_F55 = "fig_5-4-1a_suppression_profiles"
STEM_F56 = "fig_5-4-2a_cross_arm"
STEM_T55 = "tab_5-4-1a_conditions"
STEM_T56 = "tab_5-4-2a_orderings"
STEM_T57 = "tab_5-4-3a_lineage"
INTERVALS = ("200", "2000")


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
    -> (point, lo, hi). Two rows (intervals) x two columns (singles, schemes),
    y shared across the row, one key."""
    allv = [v for i in INTERVALS for s, _, _ in series for c in DEFENDED for v in get(i, s, c)]
    ymin, ymax = _yrange(allv)
    PH = 3.4
    XS0, XS1 = 1.3, 11.9   # singles panel
    XC0, XC1 = 12.4, 15.2   # schemes panel (packs to 15.7 cm; 15.4 was 2.6 pt overfull)
    Y0 = (5.05, 0.85)
    n_s = len(series)
    L: list[str] = []
    w = L.append
    L += PREAMBLE
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=1pt,font=%s}]" % FONT)
    letters = iter("abcd")
    facts = []
    yticks_v = [round(v, 2) for v in [ymin + k * 0.2 for k in range(int(round((ymax - ymin) / 0.2)) + 1)]]
    for row, interval in enumerate(INTERVALS):
        y0 = Y0[row]
        y1 = y0 + PH

        def yv(v):
            return y0 + (v - ymin) / (ymax - ymin) * PH

        for col, (conds, x0, x1) in enumerate(((SINGLES, XS0, XS1), (SCHEMES, XC0, XC1))):
            slot = (x1 - x0) / len(conds)
            bw = min(0.22, slot * 0.8 / n_s)
            xt = [(c, x0 + (i + 0.5) * slot) for i, c in enumerate(conds)]
            axes(w, x0, x1, y0, y1,
                 xticks=[(SHORT[c], x) for c, x in xt] if row == 1 else [],
                 yticks=[(v, yv(v)) for v in yticks_v],
                 xlabel="", ylabel=("suppression" if col == 0 else ""),
                 ylabels=(col == 0), xfmt=lambda v: v, yfmt=lambda v: f"{v:.1f}", ylabel_offset=0.85)
            if row == 0:
                for c, x in xt:
                    w(r"\draw[black!60,line width=0.3pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x, y0, x, y0 - 0.07))
            if ymin < 0:
                w(r"\draw[black!60,line width=0.4pt] (%.3f,%.3f) -- (%.3f,%.3f);" % (x0, yv(0), x1, yv(0)))
            panel_letter(w, x0 - (1.25 if col == 0 else 0.5), y1 + 0.02, next(letters))
            w(r"\node[anchor=south west,text=black!60] at (%.3f,%.3f) {%s, every %s\,s};" % (
                x0 + 0.05, y1 + 0.04, "single mechanisms" if col == 0 else "schemes", fmt_thousands(int(interval))))
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
    # key, once, below; entries wrap inside the panel span so five profile
    # names never run past the page box (the 16.4 cm trap of 2026-09-17)
    ky = Y0[1] - 0.95
    kx = XS0
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {%s};" % (kx, ky, key_title))
    xx = kx + 1.9
    for name, cname, hatched in series:
        width = 0.52 + 0.115 * len(key_labels[name]) + 0.45
        if xx + width > XC1:
            xx, ky = kx + 1.9, ky - 0.4
        if hatched:
            w(r"\fill[pattern=north east lines,pattern color=%s] (%.3f,%.3f) rectangle ++(0.42,0.22);" % (cname, xx, ky - 0.11))
            w(r"\draw[%s,line width=0.3pt] (%.3f,%.3f) rectangle ++(0.42,0.22);" % (cname, xx, ky - 0.11))
        else:
            w(r"\fill[%s] (%.3f,%.3f) rectangle ++(0.42,0.22);" % (cname, xx, ky - 0.11))
        w(r"\node[anchor=west] at (%.3f,%.3f) {%s};" % (xx + 0.52, ky, key_labels[name]))
        xx += width
    w(r"\node[anchor=west,text=black!60] at (%.3f,%.3f) {bar: $1 - $ hosts reached / hosts reached with no defence; whisker: 95\,\%% interval};" % (kx, ky - 0.4))
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


def _sup(d: dict, nd: int = 2) -> str:
    return "$%.*f$ [%.*f, %.*f]" % (nd, d["point"], nd, d["lo"], nd, d["hi"])


def emit_tab55(s541: dict) -> str:
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_effectiveness_figures.py from")
    w("%   data/results/ch5_defended/numbers.json (the defended corpus; the attacker")
    w("%   model pooled over its four profiles, 400 runs per cell). Do not hand-edit.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[Defence conditions measured against the attacker model]{Each defence condition scored on the three channels through which a defence can reach an attacker: whether it prevents compromise at all, how long it postpones the first one, and what fraction of the attacker's actions fail on a missing precondition, the attacker model pooled over its four profiles at each deployment interval. Intervals accompany every figure; delay to first compromise is the mean over the runs in which a compromise occurred, with the share of runs in which none occurred beside it, since that share is where a defence that denies the attacker every host shows; and adjacent conditions whose suppression intervals overlap are marked as indistinguishable rather than ranked. The intention is to state what each mechanism does on its own terms before any two are compared.}")
    w(r"  \label{tab:eff-conditions}")
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"  \begin{tabular}{@{}cP{3.4cm}>{\centering\arraybackslash}p{2.5cm}*{4}{>{\centering\arraybackslash}p{1.9cm}}@{}}")
    w(r"    \toprule")
    w(r"    & Condition & Suppression & Hosts reached & Delay to first compromise (s) & Runs with no compromise & Blocked fraction \\")
    w(r"    \midrule")
    marks = {}
    for interval in INTERVALS:
        blk = s541["by_interval"][interval]
        pooled = blk["pooled"]
        flagged = {c for pair in blk["overlapping_adjacent"] for c in pair}
        none = pooled["none"]
        if interval == INTERVALS[0]:
            dl = none["delay"]
            w("    & no defence & --- & %s & %s & %.2f & %s \\\\" % (
                pm(none["hosts"]), pm(dl["observed"], 0) if dl["observed"] else "---",
                dl["censored_share"], pm(none["blocked"], 2)))
            w(r"    \midrule")
        rows = [(c, pooled[c]) for c in blk["order_pooled"]]
        for i, (c, d) in enumerate(rows):
            group = r"\rowgroup{%d}{every %s\,s}" % (len(rows), fmt_thousands(int(interval))) if i == len(rows) - 1 else ""
            dl = d["delay"]
            mark = r"\textsuperscript{\dag}" if c in flagged else ""
            w("    %s & %s%s & %s & %s & %s & %.2f & %s \\\\" % (
                group, LONG[c], mark, _sup(d), pm(d["hosts_cond"]),
                pm(dl["observed"], 0) if dl["observed"] else "---", dl["censored_share"], pm(d["blocked"], 2)))
        w(r"    \midrule" if interval == INTERVALS[0] else r"    \bottomrule")
        marks[interval] = blk["overlapping_adjacent"]
    w(r"    \addlinespace[2pt]")
    w(r"    \multicolumn{7}{@{}p{0.96\textwidth}@{}}{\scriptsize Conditions are ordered by suppression within each interval; the no-defence reference is one cell, read against both. \textsuperscript{\dag}~the suppression interval overlaps a neighbour's in this ordering: the two are not separated at 100 seeds per profile. Suppression is $1 - $ hosts reached / hosts reached with no defence, on cell means, with a seeded bootstrap interval; delay to first compromise is undefined in a run that compromises nothing, so the share of such runs (censored at the horizon) is reported beside the mean over the rest; the blocked fraction is the share of attempted actions refused on an unmet precondition.}\\")
    w(r"  \end{tabular}")
    w(r"\end{table}")
    return "\n".join(L) + "\n"


def emit_tab56(s542: dict) -> str:
    L: list[str] = []
    w = L.append
    w("% GENERATED by tools/ch5_effectiveness_figures.py from")
    w("%   data/results/ch5_defended/numbers.json (the defended corpus; suppression of")
    w("%   hosts reached per condition per arm; the model pooled over four profiles). Do not hand-edit.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[The defence ordering produced by each attacker]{The defences ranked by suppression of hosts reached, once as the inherited attacker ranks them and once as the attacker model does, at each interval, with Spearman's rank correlation between the two orderings and a bootstrap interval on it. Where the evidence supports only a weaker statement than a full ordering the footnote says so: the family contrast, network-layer against application-layer mechanisms, is reported as Cliff's delta per arm, which is the object the seed count can separate. The intention is to state, at the strongest grade the evidence carries and no higher, whether an evaluation's recommendation depends on the attacker it was run against.}")
    w(r"  \label{tab:eff-orderings}")
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"  \begin{tabular}{@{}cP{3.4cm}>{\centering\arraybackslash}p{3.0cm}>{\centering\arraybackslash}p{1.0cm}>{\centering\arraybackslash}p{3.0cm}>{\centering\arraybackslash}p{1.0cm}@{}}")
    w(r"    \toprule")
    w(r"    & Condition & \multicolumn{2}{c}{Baseline attacker} & \multicolumn{2}{c}{Attacker model} \\")
    w(r"    \cmidrule(lr){3-4}\cmidrule(lr){5-6}")
    w(r"    & & Suppression & Rank & Suppression & Rank \\")
    w(r"    \midrule")
    rho, fam = [], []
    for interval in INTERVALS:
        blk = s542["by_interval"][interval]
        order = sorted(DEFENDED, key=lambda c: blk["ranks"]["baseline"][c])
        for i, c in enumerate(order):
            group = r"\rowgroup{%d}{every %s\,s}" % (len(order), fmt_thousands(int(interval))) if i == len(order) - 1 else ""
            b, m = blk["suppression"]["baseline"][c], blk["suppression"]["movement"][c]
            w("    %s & %s & %s & %d & %s & %d \\\\" % (
                group, LONG[c], _sup(b), blk["ranks"]["baseline"][c], _sup(m), blk["ranks"]["movement"][c]))
        w(r"    \midrule" if interval == INTERVALS[0] else r"    \bottomrule")
        sp = blk["spearman"]
        fb, fm = blk["family"]["baseline"]["cliff_network_below_application"], blk["family"]["movement"]["cliff_network_below_application"]
        rho.append(r"%.2f [%.2f, %.2f] at %s\,s" % (sp["rho"], sp["lo"], sp["hi"], fmt_thousands(int(interval))))
        fam.append(r"baseline %.2f [%.2f, %.2f] and model %.2f [%.2f, %.2f] at %s\,s" % (
            fb["delta"], fb["lo"], fb["hi"], fm["delta"], fm["lo"], fm["hi"], fmt_thousands(int(interval))))
    w(r"    \addlinespace[2pt]")
    w(r"    \multicolumn{6}{@{}p{0.96\textwidth}@{}}{\scriptsize Rank 1 is the largest suppression. Spearman's $\rho$ between the two orderings, with a seed-bootstrap interval: " + "; ".join(rho) + r". The family contrast is Cliff's $\delta$ on hosts reached, the network-layer mechanisms (IP shuffle and the two topology shuffles) against the application-layer ones (port shuffle, OS diversity, service diversity), positive when the network layer leaves fewer hosts: " + "; ".join(fam) + r". User shuffle belongs to neither family. Ranks within a family are not separable at this seed count (Table~\ref{tab:factors-fixed}); the rank correlation is a companion to the family contrast, not the primary.}\\")
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
    w("%   matrix under the opportunistic objective). Do not hand-edit.")
    w(r"\begin{table}[H]")
    w(r"  \centering")
    w(r"  \caption[Prior evaluations' headline findings under both attackers]{Each headline comparison reported by the earlier evaluations built on this simulator, re-run here under both attackers at the lineage's opportunistic objective, one row per claim: the published direction, the direction this simulator returns under the inherited attacker, and the direction under the attacker model. Because the configurations rather than the published numbers are reproduced, cells are read as agreement or disagreement in direction and never as a numerical replication, and the footnote states that boundary. The intention is to make published claims testable rather than merely cited, and to show that where they disagree with one another the disagreement is itself the finding.}")
    w(r"  \label{tab:eff-lineage}")
    w(r"  \tablestyle\scriptsize\setlength{\tabcolsep}{3pt}")
    w(r"  \begin{tabular}{@{}P{4.6cm}P{1.8cm}P{3.2cm}P{3.2cm}P{2.1cm}@{}}")
    w(r"    \toprule")
    w(r"    Published claim & Source & Inherited attacker & Attacker model & Agreement in direction \\")
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
    w(r"    \multicolumn{5}{@{}p{0.96\textwidth}@{}}{\scriptsize Direction is read on suppression of hosts reached ($1 - $ hosts / hosts with no defence, on cell means) over the seven single mechanisms and the two schemes, 100 seeds per cell, the model pooled over its four profiles; ``higher'' means the family's mean suppression is larger, and where the source names a pair the pair is read beside the family. The published evaluations reported mean time to compromise, or a composite of it, on a different network, pool and horizon, so no cell here is a numerical replication: only the direction of each comparison is compared. \textsuperscript{v}~the claim as attributed in the chapter's design record; the source's own statement of it is to be verified against the paper before submission.}\\")
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
    if not data["sanity"]["all_cells_100"] or data["sanity"]["error_rows"]:
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
