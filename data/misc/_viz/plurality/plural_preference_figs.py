"""Plural-preference study — the two figures.

Both read pp_results.json (deterministic: the analyser's point estimates and
bootstrap CIs), and both are diagnostic evidence figures in the house style — no
accentuation, no arrows, no callouts; shape + grey shade carry the arm distinction
so nothing is colour-alone and the panels survive greyscale/CVD. Conditions are
carried in the figure itself.

  fig_preference_signature.png — THE clincher. Per shape-certified dimension, the
    corpus arm's evenness against the uniform-weight null's, per profile, with 95 %
    bootstrap CIs. Where the CIs separate (transition / verb / visit) the corpus
    weighting produces a realised distribution topology alone does not; where they
    overlap (terminal) it does not — the negative reported as plainly as the
    positive. Evenness, not adaptivity: a stationary-policy property.

  fig_success_alignment.png — the strategic step. Left: the field-success
    alignment (realised edge mass vs the documented-campaign corpus prior), corpus
    vs the null — the favoured subset tracks the success prior BECAUSE of the
    weighting. Right: the substrate-success alignment, negative — the honesty
    boundary (axis 7: substrate success is not a progress signal).

    PYTHONPATH=src python data/misc/_viz/plurality/plural_preference_figs.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "pp_results.json"

PROFILES = ("objective_exfiltration", "objective_impact",
            "objective_exfiltration_impact", "objective_none_c2", "aggregate")
SHAPE_DIMS = ("transition", "verb", "visit", "terminal")

# arm inks: corpus dark filled circle, uniform mid-grey square (shape + shade, so
# the distinction survives greyscale and every CVD axis).
CORPUS_INK = "#1a1a1a"
UNIFORM_INK = "#9a9a9a"
CORPUS_MK = "o"
UNIFORM_MK = "s"
PROFILE_LABEL = {p: p.replace("objective_", "obj_") for p in PROFILES}


def load():
    return json.loads(RESULTS.read_text())


def _profile_axis(ax, n):
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_xticks(range(n))
    ax.set_xticklabels([PROFILE_LABEL[p] for p in PROFILES], rotation=35,
                       ha="right", fontsize=7)
    ax.grid(axis="y", color="#eeeeee", linewidth=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def fig_signature(res) -> None:
    fig, axes = plt.subplots(1, 4, figsize=(13.6, 4.3), sharey=True)
    for ax, dim in zip(axes, SHAPE_DIMS):
        for i, p in enumerate(PROFILES):
            d = res["profiles"][p]["dimensions"][dim]
            for arm, ink, mk, dx in (("corpus", CORPUS_INK, CORPUS_MK, -0.13),
                                     ("uniform", UNIFORM_INK, UNIFORM_MK, 0.13)):
                a = d[arm]
                lo, hi = a["even_ci"]
                ax.errorbar(i + dx, a["evenness"], yerr=[[a["evenness"] - lo],
                            [hi - a["evenness"]]], fmt=mk, color=ink,
                            markersize=5.5, elinewidth=1.3, capsize=2.6)
        # evenness = 1 reference (uniform mass over the support)
        ax.axhline(1.0, color="#cccccc", linewidth=1.0, linestyle=(0, (4, 3)))
        certified = dim in SHAPE_DIMS
        ax.set_title(dim + ("" if certified else "\n(shape withheld)"), fontsize=10)
        _profile_axis(ax, len(PROFILES))
    axes[0].set_ylabel("evenness  D / N  (Pielou)", fontsize=9)
    axes[0].set_ylim(0.25, 1.02)

    # legend (shape + shade), drawn once
    handles = [
        plt.Line2D([], [], color=CORPUS_INK, marker=CORPUS_MK, linestyle="none",
                   markersize=6, label="corpus-weighted (shipped)"),
        plt.Line2D([], [], color=UNIFORM_INK, marker=UNIFORM_MK, linestyle="none",
                   markersize=6, label="uniform-weight null (topology only)"),
        plt.Line2D([], [], color="#cccccc", linewidth=1.0, linestyle=(0, (4, 3)),
                   label="evenness 1 (uniform mass)"),
    ]
    fig.suptitle(
        "Plural preference: evenness of the realised behaviour distribution, "
        "corpus policy vs the topology-only null",
        y=0.975, fontsize=11)
    fig.legend(handles=handles, loc="upper center", ncol=3, fontsize=8.5,
               frameon=False, bbox_to_anchor=(0.5, 0.925))
    fig.text(0.5, 0.02,
             "movement arm · modulators null · no MTD · v2_partial · retrace · "
             f"{res['seeds']} matched seeds · 95% bootstrap CI · a CI gap between the "
             "arms is preference the weights buy, not the topology (stationary policy, "
             "not adaptivity)",
             ha="center", fontsize=7.4, color="#444444")
    fig.subplots_adjust(top=0.76, bottom=0.24, left=0.055, right=0.99, wspace=0.12)
    out = HERE / "fig_preference_signature.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"wrote {out}")


def fig_alignment(res) -> None:
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(11.2, 4.4))
    n = len(PROFILES)

    # left: field-success alignment, corpus vs uniform
    for i, p in enumerate(PROFILES):
        a = res["profiles"][p]["alignment"]
        for key, ink, mk, dx in (("field_success_corpus", CORPUS_INK, CORPUS_MK, -0.13),
                                 ("field_success_uniform", UNIFORM_INK, UNIFORM_MK, 0.13)):
            pt, lo, hi = a[key]
            axl.errorbar(i + dx, pt, yerr=[[pt - lo], [hi - pt]], fmt=mk, color=ink,
                         markersize=5.5, elinewidth=1.3, capsize=2.6)
    axl.axhline(0.0, color="#cccccc", linewidth=1.0, linestyle=(0, (4, 3)))
    axl.set_title("field-success alignment\n(realised edge mass vs corpus prior)",
                  fontsize=10)
    axl.set_ylabel("Spearman ρ (mass, corpus success prior)", fontsize=9)
    _profile_axis(axl, n)

    # right: substrate-success alignment, corpus — the honesty boundary
    for i, p in enumerate(PROFILES):
        pt, lo, hi = res["profiles"][p]["alignment"]["substrate_success_corpus"]
        axr.errorbar(i, pt, yerr=[[pt - lo], [hi - pt]], fmt=CORPUS_MK,
                     color=CORPUS_INK, markersize=5.5, elinewidth=1.3, capsize=2.6)
    axr.axhline(0.0, color="#cccccc", linewidth=1.0, linestyle=(0, (4, 3)))
    axr.set_title("substrate-success alignment\n(verb mass vs substrate success rate)",
                  fontsize=10)
    axr.set_ylabel("Spearman ρ (mass, substrate success)", fontsize=9)
    _profile_axis(axr, n)

    handles = [
        plt.Line2D([], [], color=CORPUS_INK, marker=CORPUS_MK, linestyle="none",
                   markersize=6, label="corpus-weighted (shipped)"),
        plt.Line2D([], [], color=UNIFORM_INK, marker=UNIFORM_MK, linestyle="none",
                   markersize=6, label="uniform-weight null"),
    ]
    fig.suptitle("The favoured subset is the field-successful subset — but not the "
                 "substrate-successful one", y=0.975, fontsize=11)
    fig.legend(handles=handles, loc="upper center", ncol=2, fontsize=8.5,
               frameon=False, bbox_to_anchor=(0.5, 0.925))
    fig.text(0.5, 0.02,
             "movement arm · modulators null · no MTD · v2_partial · retrace · "
             f"{res['seeds']} matched seeds · 95% bootstrap CI · left: corpus tracks "
             "the campaign prior above the null · right: negative (axis 7)",
             ha="center", fontsize=7.4, color="#444444")
    fig.subplots_adjust(top=0.76, bottom=0.24, left=0.075, right=0.98, wspace=0.28)
    out = HERE / "fig_success_alignment.png"
    fig.savefig(out, dpi=200)
    plt.close(fig)
    print(f"wrote {out}")


def main() -> int:
    res = load()
    fig_signature(res)
    fig_alignment(res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
