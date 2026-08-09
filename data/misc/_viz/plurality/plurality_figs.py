"""Plurality reporting — the one figure the pre-registration allows.

The handoff (2026-08-09_strategic_plurality_reporting.md) named two candidate
figures. P1 — the pre-registered kill criterion — FIRED on the recorded runs
(Spearman rho = -0.97 between pooled path entropy and maximum single-place
visit share, threshold 0.90; see reconcile.py), so the six-family entropy fan
is NOT drawn: it would be a hub-occupancy chart wearing an entropy axis. The
narrowing family is reported as a table in plurality_reporting.md instead.

What remains chart-shaped is figure (b): the profile x mechanism interaction —
within each profile, the defence conditions ranked by breadth suppression. The
finding IS that the columns are not constant across profiles, and a rank
heatmap lets the eye read that directly. Diagnostic evidence figure: no
accentuation, no arrows, no callouts; a single grey sequential ramp (rank is a
magnitude; grey survives greyscale printing and every CVD axis) with the rank
annotated in every cell so nothing is colour-alone. Conditions are carried in
the figure itself.

Reads data/results/expo02_ashen_lynx/runs.jsonl (recorded runs only — nothing
is simulated). Deterministic: same input, same pixels.

    PYTHONPATH=src python data/misc/_viz/plurality/plurality_figs.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import colors  # noqa: E402

HERE = Path(__file__).resolve().parent
RUNS = HERE.parents[2] / "results" / "expo02_ashen_lynx" / "runs.jsonl"

MECHANISMS = ("complete_topology", "ip_shuffle", "os_diversity",
              "service_diversity")
MULTI = ("random_multi", "simultaneous_multi", "alternative_multi")
DEFENCES = MECHANISMS + MULTI
PROFILES = ("objective_exfiltration", "objective_impact",
            "objective_exfiltration_impact", "objective_none_c2", "aggregate")

# Display labels: line-broken condition names; profiles keep their record ids.
COND_LABEL = {
    "complete_topology": "complete\ntopology",
    "ip_shuffle": "IP\nshuffle",
    "os_diversity": "OS\ndiversity",
    "service_diversity": "service\ndiversity",
    "random_multi": "random\nmulti",
    "simultaneous_multi": "simultaneous\nmulti",
    "alternative_multi": "alternative\nmulti",
}
PROFILE_LABEL = {
    "objective_exfiltration": "objective_exfiltration",
    "objective_impact": "objective_impact",
    "objective_exfiltration_impact": "objective_exfiltration_impact",
    "objective_none_c2": "objective_none_c2",
    "aggregate": "aggregate",
}


# The 2026-08-06 objective-tactic rename: the recorded runs carry the OLD
# labels; read them off the corpus and normalise here. (The workspace's own
# analyse.py was edited to the new names after the run and no longer selects
# these rows — the drift is recorded in plurality_reporting.md.)
RENAME = {
    "pure_steal": "objective_exfiltration",
    "pure_impediment": "objective_impact",
    "double_extortion": "objective_exfiltration_impact",
    "infrastructure_setup": "objective_none_c2",
}


def load() -> list[dict]:
    rows = []
    for line in RUNS.read_text().splitlines():
        r = json.loads(line)
        if "error" in r:
            continue
        r["profile"] = RENAME.get(r.get("profile"), r.get("profile"))
        rows.append(r)
    return rows


def sel(rows, **kw):
    return [r for r in rows if all(r.get(k) == v for k, v in kw.items())]


def mean(rows, field):
    vals = [r[field] for r in rows if r.get(field) is not None]
    return sum(vals) / len(vals) if vals else float("nan")


def rank_matrix(rows, interval):
    """Within-profile rank of each defence by mean distinct hosts (1 = fewest
    hosts = strongest breadth suppression) — experiment 2's E3(b) ordering,
    construction verbatim."""
    ranks = {}
    hosts = {}
    for profile in PROFILES:
        scored = []
        for cond in DEFENCES:
            cells = sel(rows, arm="movement", profile=profile, condition=cond,
                        interval=interval, sink_policy="retrace")
            if not cells:
                raise SystemExit(
                    f"empty cell {profile}/{cond}/{interval} — label drift; "
                    "refusing to rank NaNs")
            m = mean(cells, "hosts")
            scored.append((m, cond))
            hosts[(profile, cond)] = m
        scored.sort()
        for i, (_, cond) in enumerate(scored):
            ranks[(profile, cond)] = i + 1
    return ranks, hosts


def main() -> int:
    rows = load()

    fig, axes = plt.subplots(
        1, 2, figsize=(12.5, 4.5), sharey=True,
        gridspec_kw={"wspace": 0.05},
    )
    cmap = plt.get_cmap("Greys")
    norm = colors.Normalize(vmin=0.0, vmax=len(DEFENCES) + 2)

    distinct = {}
    for ax, interval in zip(axes, (200, 2000)):
        ranks, hosts = rank_matrix(rows, interval)
        orderings = {
            p: tuple(sorted(DEFENCES, key=lambda c: ranks[(p, c)]))
            for p in PROFILES
        }
        distinct[interval] = len(set(orderings.values()))

        for yi, profile in enumerate(PROFILES):
            for xi, cond in enumerate(DEFENCES):
                r = ranks[(profile, cond)]
                # dark = strongest suppression (rank 1)
                shade = cmap(norm(len(DEFENCES) + 1 - r))
                ax.add_patch(plt.Rectangle(
                    (xi, yi), 1, 1, facecolor=shade, edgecolor="white",
                    linewidth=2))
                lum = colors.rgb_to_hsv(shade[:3])[2]
                ink = "white" if lum < 0.55 else "#222222"
                ax.text(xi + 0.5, yi + 0.5, str(r), ha="center", va="center",
                        fontsize=13, color=ink)

        ax.set_xlim(0, len(DEFENCES))
        ax.set_ylim(len(PROFILES), 0)
        ax.set_xticks([i + 0.5 for i in range(len(DEFENCES))])
        ax.set_xticklabels([COND_LABEL[c] for c in DEFENCES], fontsize=7)
        ax.set_yticks([i + 0.5 for i in range(len(PROFILES))])
        ax.set_yticklabels([PROFILE_LABEL[p] for p in PROFILES], fontsize=9)
        ax.set_title(
            f"mutation interval {interval} s — "
            f"{distinct[interval]} of {len(PROFILES)} rankings distinct",
            fontsize=10)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(length=0)

    fig.text(
        0.5, 0.045,
        "Within-profile rank of each defence condition by breadth suppression "
        "(1 = strongest: fewest mean distinct hosts).",
        ha="center", fontsize=8, color="#444444")
    fig.text(
        0.5, 0.012,
        "Movement arm (modulators null), mapping v2_partial, sink policy "
        "retrace, 10 seeds per cell, horizon 15 000 s; recorded runs, "
        "experiment 2 (data/results/expo02_ashen_lynx).",
        ha="center", fontsize=7.5, color="#444444")
    fig.subplots_adjust(left=0.17, right=0.985, top=0.9, bottom=0.26)
    out = HERE / "fig_interaction_rank.png"
    fig.savefig(out, dpi=200)
    print(f"wrote {out}")
    for interval in (200, 2000):
        print(f"  interval {interval}: {distinct[interval]}/5 distinct "
              f"profile rankings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
