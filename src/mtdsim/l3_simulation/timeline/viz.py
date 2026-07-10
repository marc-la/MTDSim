"""Awareness figures for the timeline library — what the walks actually do.

Diagnostic-quality, regenerable, written to the gitignored
``data/ogasp/timeline/_viz/`` (the ``data/gasp/_*`` pattern). Three views over
the seeded library, all on the **primary cell coordinates** (initial-access
entry, central dwells) with uniform scales across profiles so the five
envelopes stay visually comparable — no per-profile tuning, no accentuation;
the marks and a legend carry everything:

- ``walks_<profile>.png`` — the first N seeded runs of the primary cell as
  horizontal timelines, one row per run, segments coloured by tactic
  (hue = kill-chain phase, lightness = position within the phase), the
  outcome written at each row's end. Shared x-scale across all five files.
- ``net_time_to_objective.png`` — the net time-to-objective distribution per
  profile (objective runs only), median marked. An **envelope statistic**,
  never the DES MTTC (metrics_semantics.md §(a)/(d)).
- ``outcomes.png`` — outcome mix (objective / stalled / cap) per profile and
  routing arm, central dwells.

Dwells are the v0 uncalibrated catalogue: absolute seconds are
shape-not-scale placeholders, so read orderings and ratios, not magnitudes.
``resource-development`` dwells 0 s and is therefore invisible in the walk
segments (the state is still in the record).

Needs ``matplotlib`` (a house dependency of ``data/gasp/_viz/gasp_viz.py``);
the runner's library and report never depend on it — ``__main__`` skips these
figures with a note when it is absent.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from mtdsim.l3_simulation.timeline.matrix import TIMELINES_DIR
from mtdsim.l3_simulation.timeline.walk import (
    PROFILE_NAMES,
    TIMELINE_DIR,
    load_catalogue,
)

VIZ_DIR = TIMELINE_DIR / "_viz"

N_WALKS = 20  # runs shown per profile — the first N seeded runs, no selection

PRIMARY_ARM = "weighted-operator_dedup"
ARMS = (PRIMARY_ARM, "weighted-raw", "uniform")
ARM_LABELS = {PRIMARY_ARM: "weighted dedup", "weighted-raw": "weighted raw", "uniform": "uniform"}

# Tactic colour: hue = kill-chain phase (8 phases -> the 8 fixed categorical
# slots, assigned in kill-chain order, never cycled), lightness step = the
# tactic's position within its phase (earlier = lighter). 15 raw hues would
# defeat colour-vision-deficiency separation; the phase/lightness split keeps
# hue pairs validated while the legend recovers exact identity.
PHASE_GROUPS = (
    ("reconnaissance", "resource-development"),
    ("initial-access",),
    ("execution", "persistence", "privilege-escalation"),
    ("stealth", "defense-impairment"),
    ("credential-access", "discovery"),
    ("lateral-movement",),
    ("collection", "command-and-control"),
    ("exfiltration", "impact"),
)
SLOT_HEXES = (  # the validated 8-slot categorical palette, fixed order
    "#2a78d6", "#1baf7a", "#eda100", "#008300",
    "#4a3aa7", "#e34948", "#e87ba4", "#eb6834",
)
# Within-phase tints (blend toward white): earlier member lighter, last = base.
_TINTS = {1: (0.0,), 2: (0.32, 0.0), 3: (0.48, 0.24, 0.0)}

OUTCOME_ORDER = ("objective", "stalled", "cap")
OUTCOME_COLORS = dict(zip(OUTCOME_ORDER, SLOT_HEXES[:3]))

# Chart chrome (the house light-surface ink set).
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"


def _tint(hex_color: str, toward_white: float) -> str:
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: round(c + (255 - c) * toward_white)  # noqa: E731
    return f"#{mix(r):02x}{mix(g):02x}{mix(b):02x}"


def tactic_colors() -> dict:
    """``tactic -> hex``, phases in kill-chain order on the fixed slot order."""
    colors = {}
    for slot, group in zip(SLOT_HEXES, PHASE_GROUPS):
        for tactic, tint in zip(group, _TINTS[len(group)]):
            colors[tactic] = _tint(slot, tint)
    return colors


def _cell_id(profile: str, entry: str, arm: str, variant: str) -> str:
    return f"{profile}--{entry}--{arm}--{variant}"


def _new_axes(figsize):
    fig, ax = plt.subplots(figsize=figsize, facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    return fig, ax


def _tactic_legend(fig, colors: dict, order: list) -> None:
    handles = [
        Patch(facecolor=colors[t], edgecolor="none", label=t)
        for t in order
        if t in colors
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        ncol=5,
        fontsize=7.5,
        frameon=False,
        labelcolor=INK_2,
        bbox_to_anchor=(0.5, 0.0),
    )


def render_walks(
    profile: str,
    records: list,
    colors: dict,
    tactic_order: list,
    xmax: float,
    out_path: Path,
) -> Path:
    """One profile's primary cell as N run-timelines (rows), shared x-scale."""
    sample = records[:N_WALKS]
    fig, ax = _new_axes((11.5, 7.6))
    for i, r in enumerate(sample):
        spans = [(s["t_enter_s"], s["dwell_s"]) for s in r["sequence"]]
        facecolors = [colors[s["tactic"]] for s in r["sequence"]]
        ax.broken_barh(
            spans, (i - 0.36, 0.72),
            facecolors=facecolors, edgecolor=SURFACE, linewidth=0.8,
        )
        if r["outcome"] == "objective":
            label = f"objective · {r['net_time_to_objective_s']:,.0f} s"
        else:
            label = f"{r['outcome']} · {r['n_states']} states"
        ax.text(
            r["total_duration_s"] + xmax * 0.008, i, label,
            va="center", fontsize=7.5, color=INK_2,
        )
    ax.set_ylim(len(sample) - 0.5, -0.5)  # run 000 on top
    ax.set_yticks(range(len(sample)))
    ax.set_yticklabels([r["run_id"].rsplit("--", 1)[-1] for r in sample])
    ax.set_xlim(0, xmax * 1.18)
    ax.set_xlabel(
        "simulated seconds — v0 uncalibrated dwells (shape, not scale); "
        "resource-development dwells 0 s and has no visible width",
        fontsize=8.5, color=INK_2,
    )
    objectives = ", ".join(records[0]["objective_tactics"])
    rule = records[0]["objective_rule"]
    ax.set_title(
        f"{profile} — first {len(sample)} seeded walks of the primary cell\n"
        f"initial-access entry · weighted (operator-dedup) · central dwells · "
        f"objective ({rule}): {objectives}",
        fontsize=11, color=INK, loc="left",
    )
    _tactic_legend(fig, colors, tactic_order)
    fig.tight_layout(rect=(0, 0.09, 1, 1))
    fig.savefig(out_path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return out_path


def render_net_time_to_objective(cells: dict, out_path: Path) -> Path:
    """Net time-to-objective per profile (objective runs), medians marked."""
    fig, ax = _new_axes((10.5, 4.6))
    rng = random.Random(7)  # jitter only; the data are untouched
    for y, profile in enumerate(PROFILE_NAMES):
        records = cells.get(profile, [])
        values = [
            r["net_time_to_objective_s"]
            for r in records
            if r["outcome"] == "objective"
        ]
        ax.scatter(
            values,
            [y + rng.uniform(-0.22, 0.22) for _ in values],
            s=22, color=SLOT_HEXES[0], alpha=0.4, linewidths=0,
        )
        if values:
            values.sort()
            n = len(values)
            median = (
                values[n // 2]
                if n % 2
                else 0.5 * (values[n // 2 - 1] + values[n // 2])
            )
            ax.plot([median, median], [y - 0.3, y + 0.3], color=INK, linewidth=1.6)
            ax.text(
                median, y - 0.38, f"{median:,.0f} s",
                ha="center", fontsize=8, color=INK,
            )
        ax.text(
            1.005, y, f"{len(values)}/{len(records)} objective",
            transform=ax.get_yaxis_transform(),
            va="center", fontsize=8, color=INK_2,
        )
    ax.set_ylim(len(PROFILE_NAMES) - 0.5, -0.6)
    ax.set_yticks(range(len(PROFILE_NAMES)))
    ax.set_yticklabels(PROFILE_NAMES, fontsize=9)
    ax.set_xlim(left=0)
    ax.set_xlabel(
        "net time-to-objective, simulated seconds — an envelope statistic, "
        "not the DES MTTC (v0 uncalibrated dwells)",
        fontsize=8.5, color=INK_2,
    )
    ax.set_title(
        "Net time-to-objective per profile — objective runs of the primary cell\n"
        "initial-access entry · weighted (operator-dedup) · central dwells · "
        "100 seeded runs each · median marked",
        fontsize=11, color=INK, loc="left",
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    return out_path


def render_outcomes(cells: dict, out_path: Path) -> Path:
    """Outcome mix per profile × routing arm (central dwells), stacked shares."""
    fig, ax = _new_axes((10.5, 6.4))
    ys, labels = [], []
    y = 0.0
    for profile in PROFILE_NAMES:
        for arm in ARMS:
            records = cells.get((profile, arm))
            if records is None:
                continue
            n = len(records)
            counts = {o: 0 for o in OUTCOME_ORDER}
            for r in records:
                counts[r["outcome"]] += 1
            left = 0.0
            for outcome in OUTCOME_ORDER:
                share = counts[outcome] / n
                if share == 0:
                    continue
                ax.barh(
                    y, share, left=left, height=0.72,
                    color=OUTCOME_COLORS[outcome],
                    edgecolor=SURFACE, linewidth=1.4,
                )
                if share >= 0.08:  # direct label — the sub-3:1 relief channel
                    ax.text(
                        left + share / 2, y, f"{share:.0%}",
                        ha="center", va="center", fontsize=7.5,
                        color=SURFACE if outcome == "objective" else INK,
                    )
                left += share
            ys.append(y)
            labels.append(f"{profile} · {ARM_LABELS[arm]}")
            y += 1.0
        y += 0.6  # gap between profile blocks
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_ylim(max(ys) + 0.7, -0.7)
    ax.set_xlim(0, 1)
    ax.set_xticks((0, 0.25, 0.5, 0.75, 1.0))
    ax.set_xticklabels(("0%", "25%", "50%", "75%", "100%"))
    ax.set_xlabel(
        "share of 100 seeded runs — `stalled` is a legitimate, recorded "
        "envelope outcome, not an error",
        fontsize=8.5, color=INK_2,
    )
    ax.set_title(
        "Outcome mix per profile and routing arm — initial-access entry, "
        "central dwells",
        fontsize=11, color=INK, loc="left",
    )
    fig.legend(
        handles=[
            Patch(facecolor=OUTCOME_COLORS[o], edgecolor="none", label=o)
            for o in OUTCOME_ORDER
        ],
        loc="lower center", ncol=3, fontsize=8.5, frameon=False,
        labelcolor=INK_2, bbox_to_anchor=(0.5, 0.0),
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(out_path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    return out_path


def render_all(manifest: dict, library: dict, viz_dir: Path = VIZ_DIR) -> list:
    """All awareness figures from an in-memory library (``__main__``'s pass)."""
    viz_dir = Path(viz_dir)
    viz_dir.mkdir(parents=True, exist_ok=True)
    catalogue = load_catalogue()
    tactic_order = list(catalogue["tactics"])  # canonical kill-chain order
    colors = tactic_colors()

    primary = {
        p: library[_cell_id(p, "initial-access", PRIMARY_ARM, "central")]
        for p in PROFILE_NAMES
    }
    # One absolute x-scale across the five walk figures (uniform, comparable).
    xmax = max(
        r["total_duration_s"]
        for records in primary.values()
        for r in records[:N_WALKS]
    )
    figures = [
        render_walks(
            p, primary[p], colors, tactic_order, xmax, viz_dir / f"walks_{p}.png"
        )
        for p in PROFILE_NAMES
    ]
    figures.append(
        render_net_time_to_objective(
            primary, viz_dir / "net_time_to_objective.png"
        )
    )
    arm_cells = {
        (p, arm): library[_cell_id(p, "initial-access", arm, "central")]
        for p in PROFILE_NAMES
        for arm in ARMS
    }
    figures.append(render_outcomes(arm_cells, viz_dir / "outcomes.png"))
    return figures


def _load_cells(timelines_dir: Path, cell_ids: list) -> dict:
    out = {}
    for cell_id in cell_ids:
        path = Path(timelines_dir) / f"{cell_id}.jsonl"
        with open(path) as f:
            out[cell_id] = [json.loads(line) for line in f]
    return out


def main() -> int:
    """CLI: render the figures from the on-disk library (no regeneration)."""
    manifest_path = TIMELINES_DIR / "manifest.json"
    if not manifest_path.exists():
        print(
            f"no library at {TIMELINES_DIR}/ — run "
            "`PYTHONPATH=src python -m mtdsim.l3_simulation.timeline` first"
        )
        return 2
    with open(manifest_path) as f:
        manifest = json.load(f)
    needed = [
        _cell_id(p, "initial-access", arm, "central")
        for p in PROFILE_NAMES
        for arm in ARMS
    ]
    library = _load_cells(TIMELINES_DIR, needed)
    figures = render_all(manifest, library)
    print(f"  -> {VIZ_DIR}/ ({len(figures)} figures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "N_WALKS",
    "PHASE_GROUPS",
    "VIZ_DIR",
    "render_all",
    "render_net_time_to_objective",
    "render_outcomes",
    "render_walks",
    "tactic_colors",
]
