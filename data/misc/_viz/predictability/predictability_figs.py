"""Predictability study — the two figures.

Both read pred_results.json (deterministic: the analyser's point estimates and
bootstrap CIs), and both are diagnostic evidence figures in the house style — no
accentuation, no arrows, no callouts; shape + grey shade carry the arm distinction
so nothing is colour-alone and the panels survive greyscale/CVD. Conditions are
carried in the figure itself.

  fig_predictability_regime.png — THE headline. Per profile, the realised
    predictability P of the corpus arm and the uniform-weight null with 95 %
    bootstrap CIs, against the scripted baseline's constructed P=1.00 (the upper
    reference line) and the 1/N uniform-dithering floor. The movement attacker sits
    far below the baseline: its next move cannot be called from its own decision
    state at the rate the FSM's can. Predictability, not adaptivity: a
    stationary-policy property.

  fig_calibration_ladder.png — the reader's self-test. The FSM's effective breadth
    D_policy at three conditionings: the marginal (phase) reading (plural — the
    reader is not rigged to return 1), the (phase, branch) reading (the resolvable
    plurality collapses), and the constructed transition table (exactly 1.0). The
    ladder shows apparent plurality collapsing toward the construct as conditioning
    deepens; the movement corpus arm's D_policy is drawn beside it, and it does not
    collapse — it survives full conditioning on every variable its policy consults.

    PYTHONPATH=src python data/misc/_viz/predictability/predictability_figs.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "pred_results.json"

PROFILES = ("objective_exfiltration", "objective_impact",
            "objective_exfiltration_impact", "objective_none_c2", "aggregate")

CORPUS_INK = "#1a1a1a"
UNIFORM_INK = "#9a9a9a"
CORPUS_MK = "o"
UNIFORM_MK = "s"
REF_INK = "#555555"
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


def _pt(ax, x, mean, lo, hi, ink, mk):
    ax.plot([x, x], [lo, hi], color=ink, linewidth=1.1, zorder=2)
    ax.plot([x], [mean], marker=mk, color=ink, markersize=6,
            markerfacecolor=ink, markeredgecolor=ink, zorder=3)


def fig_regime(results):
    real = results["realised"]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.axhline(1.0, color=REF_INK, linewidth=1.0, linestyle="--", zorder=1)
    ax.text(len(PROFILES) - 0.5, 1.0, "  scripted baseline P = 1.00 (constructed)",
            va="center", ha="left", fontsize=7, color=REF_INK)
    for i, profile in enumerate(PROFILES):
        c = real[profile]["corpus"]
        u = real[profile]["uniform_null"]
        _pt(ax, i - 0.11, c["P_seedmean"], c["P_ci"][0], c["P_ci"][1], CORPUS_INK, CORPUS_MK)
        _pt(ax, i + 0.11, u["P_seedmean"], u["P_ci"][0], u["P_ci"][1], UNIFORM_INK, UNIFORM_MK)
    _profile_axis(ax, len(PROFILES))
    ax.set_ylim(0.0, 1.05)
    ax.set_ylabel("predictability  P  (rate the next move can be called)")
    ax.set_title("Predictability per profile — the movement attacker against its "
                 "scripted baseline", fontsize=9)
    from matplotlib.lines import Line2D
    handles = [
        Line2D([0], [0], marker=CORPUS_MK, color=CORPUS_INK, markerfacecolor=CORPUS_INK,
               linestyle="none", markersize=6, label="corpus-weighted (shipped)"),
        Line2D([0], [0], marker=UNIFORM_MK, color=UNIFORM_INK, markerfacecolor=UNIFORM_INK,
               linestyle="none", markersize=6, label="uniform-weight null (topology only)"),
    ]
    ax.legend(handles=handles, fontsize=7, frameon=False, loc="center right")
    fig.text(0.01, 0.01,
             "conditional on each policy's own decision state — movement (place, verdict), "
             "FSM (phase, branch); no MTD, v2_partial, retrace, modulators null. "
             "A lower P is a plural repertoire, not an advantage (experiment 2 §11).",
             fontsize=6, color="#666666")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(HERE / "fig_predictability_regime.png", dpi=150)
    plt.close(fig)


def fig_calibration(results):
    cal = results["calibration"]
    real = results["realised"]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    # the FSM ladder: three conditionings, decreasing apparent breadth
    xs = [0, 1, 2]
    ys = [cal["marginal_phase"]["D_policy"],
          cal["conditioned_phase_branch"]["D_policy"],
          cal["constructed_table"]["D_policy"]]
    ax.plot(xs, ys, marker="s", color=UNIFORM_INK, markerfacecolor=UNIFORM_INK,
            linewidth=1.2, markersize=7, zorder=3, label="scripted baseline (FSM)")
    for x, y in zip(xs, ys):
        ax.text(x, y + 0.12, f"{y:.2f}", ha="center", fontsize=7, color="#333333")
    # the movement corpus arm's D_policy range, drawn as a band on the right
    dvals = [real[p]["corpus"]["D_policy_pooled"] for p in PROFILES]
    ax.axhspan(min(dvals), max(dvals), xmin=0.72, xmax=0.98, color="#dddddd", zorder=1)
    ax.text(2.02, (min(dvals) + max(dvals)) / 2,
            f"  movement corpus arm\n  D_policy {min(dvals):.1f}–{max(dvals):.1f}\n"
            "  (survives full conditioning)",
            va="center", fontsize=7, color=CORPUS_INK)
    ax.axhline(1.0, color=REF_INK, linewidth=0.9, linestyle="--", zorder=1)
    ax.set_xlim(-0.4, 3.4)
    ax.set_xticks(xs)
    ax.set_xticklabels(["marginal\n(phase)", "conditioned\n(phase, branch)",
                        "constructed\ntransition table"], fontsize=7.5)
    ax.set_ylabel("effective breadth  D_policy = 2^H(A|C)")
    ax.set_ylim(0.8, max(max(dvals) + 0.4, 2.0))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#eeeeee", linewidth=0.8)
    ax.set_title("Calibration ladder — apparent FSM plurality collapses under "
                 "conditioning;\nthe movement arm's does not", fontsize=9)
    fig.text(0.01, 0.01,
             "The reader reads the FSM's phase-level plurality (proving it is not "
             "rigged to 1) and collapses it as more of the FSM's consulted state is "
             "conditioned on; residual > 1 is FSM-internal state the attack record "
             "under-exposes, not policy plurality.",
             fontsize=6, color="#666666")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(HERE / "fig_calibration_ladder.png", dpi=150)
    plt.close(fig)


def main() -> int:
    results = load()
    fig_regime(results)
    fig_calibration(results)
    print(f"wrote {HERE / 'fig_predictability_regime.png'}")
    print(f"wrote {HERE / 'fig_calibration_ladder.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
