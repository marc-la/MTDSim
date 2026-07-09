"""The behavioural verification report (light) + the committed example.

Summary statistics per run-matrix cell — net time-to-objective distribution,
outcome mix, sequence length, per-tactic occupancy — and the
class-vs-aggregate comparison on those statistics: the **behavioural half**
of "do the four profiles differ" (the structural half is the weighting
stage's divergence report). Summary stats + one computed verdict paragraph
only; the full aggregated variation analysis stays deferred backlog (D10).

Phrasing discipline: every statement is **envelope-relative** — a timeline is
one instantiation of the class envelope, never "an APT's campaign" — and the
time statistic is the **net time-to-objective**, which is not the DES MTTC
(metrics_semantics.md §(a)/(d)).
"""

from __future__ import annotations

import json
from pathlib import Path

from mtdsim.l3_simulation.timeline.matrix import (
    ENTRY_INITIAL_ACCESS,
    ENTRY_RECON,
)
from mtdsim.l3_simulation.timeline.walk import (
    AGGREGATE,
    CLASS_NAMES,
    OGASP_DIR,
    PROFILE_NAMES,
    serialise,
)

REPORT_MD = OGASP_DIR / "timeline_report.md"
REPORT_JSON = OGASP_DIR / "timeline_report.json"
EXAMPLE_PATH = OGASP_DIR / "timeline_example.jsonl"

PRIMARY_ARM = "weighted-operator_dedup"


def _percentile(sorted_values: list, q: float) -> float:
    """Linear-interpolation percentile over a pre-sorted list (q in [0, 1])."""
    if not sorted_values:
        raise ValueError("empty")
    pos = q * (len(sorted_values) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = pos - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def cell_stats(records: list) -> dict:
    """Summary statistics for one cell's records."""
    outcomes: dict[str, int] = {}
    tto = []
    for r in records:
        outcomes[r["outcome"]] = outcomes.get(r["outcome"], 0) + 1
        if r["net_time_to_objective_s"] is not None:
            tto.append(r["net_time_to_objective_s"])
    tto.sort()
    n = len(records)
    occupancy: dict[str, float] = {}
    for r in records:
        total = r["total_duration_s"]
        if total <= 0:
            continue
        for state in r["sequence"]:
            share = state["dwell_s"] / total
            occupancy[state["tactic"]] = occupancy.get(state["tactic"], 0.0) + share
    occupancy = {t: s / n for t, s in occupancy.items()}
    return {
        "n_runs": n,
        "outcomes": dict(sorted(outcomes.items())),
        "objective_rate": outcomes.get("objective", 0) / n if n else 0.0,
        "net_time_to_objective_s": (
            {
                "n": len(tto),
                "median": _percentile(tto, 0.5),
                "mean": sum(tto) / len(tto),
                "p10": _percentile(tto, 0.1),
                "p90": _percentile(tto, 0.9),
            }
            if tto
            else None
        ),
        "mean_n_states": sum(r["n_states"] for r in records) / n if n else 0.0,
        "mean_total_duration_s": (
            sum(r["total_duration_s"] for r in records) / n if n else 0.0
        ),
        "occupancy_mean_dwell_share": dict(
            sorted(occupancy.items(), key=lambda kv: -kv[1])
        ),
    }


def _cell_id(profile: str, entry: str, arm: str, variant: str) -> str:
    return f"{profile}--{entry}--{arm}--{variant}"


def _median(stats: dict, cell_id: str):
    s = stats.get(cell_id)
    if s and s["net_time_to_objective_s"]:
        return s["net_time_to_objective_s"]["median"]
    return None


def _ordering(stats: dict, entry: str, arm: str, variant: str) -> list:
    """Profiles ranked by median net time-to-objective (fastest first);
    profiles without an objective run are excluded (recorded separately)."""
    medians = []
    for profile in PROFILE_NAMES:
        m = _median(stats, _cell_id(profile, entry, arm, variant))
        if m is not None:
            medians.append((m, profile))
    return [p for _, p in sorted(medians)]


def _aggregate_conditional_tto(library: dict, variant: str) -> dict:
    """Aggregate runs terminate on ANY union objective; split their net
    time-to-objective by which objective completed, so each class can be
    compared against the aggregate runs that achieved *its* objective."""
    cell_id = _cell_id(AGGREGATE, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, variant)
    split: dict[str, list] = {}
    for r in library.get(cell_id, []):
        if r["outcome"] != "objective":
            continue
        for objective in r["completed_objectives"]:
            split.setdefault(objective, []).append(r["net_time_to_objective_s"])
    out = {}
    for objective, values in sorted(split.items()):
        values.sort()
        out[objective] = {
            "n": len(values),
            "median": _percentile(values, 0.5),
        }
    return out


def _occupancy_l1_vs_aggregate(stats: dict, variant: str) -> dict:
    """L1 distance between each class's mean-dwell-share vector and the
    aggregate's, on the primary arm at initial-access."""
    agg = stats.get(
        _cell_id(AGGREGATE, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, variant), {}
    ).get("occupancy_mean_dwell_share", {})
    distances = {}
    for profile in CLASS_NAMES:
        occ = stats.get(
            _cell_id(profile, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, variant), {}
        ).get("occupancy_mean_dwell_share", {})
        # sorted so the float summation order (hence the last bit) is
        # process-independent — set order varies with the string hash seed
        tactics = sorted(set(agg) | set(occ))
        distances[profile] = sum(
            abs(occ.get(t, 0.0) - agg.get(t, 0.0)) for t in tactics
        )
    return distances


def _fmt_s(value) -> str:
    return f"{value:,.1f} s" if value is not None else "—"


def _fmt_outcomes(s: dict) -> str:
    return ", ".join(f"{k} {v}" for k, v in s["outcomes"].items())


def _top_occupancy(s: dict, k: int = 3) -> str:
    items = list(s["occupancy_mean_dwell_share"].items())[:k]
    return ", ".join(f"{t} {share:.0%}" for t, share in items)


def build_report(manifest: dict, library: dict) -> dict:
    """All computed numbers the markdown renders (also persisted as JSON)."""
    stats = {cell_id: cell_stats(records) for cell_id, records in library.items()}

    orderings = {
        "central": _ordering(stats, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, "central"),
        "sweep_low": _ordering(stats, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, "sweep_low"),
        "sweep_high": _ordering(stats, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, "sweep_high"),
        "uniform_central": _ordering(stats, ENTRY_INITIAL_ACCESS, "uniform", "central"),
        "raw_central": _ordering(
            stats, ENTRY_INITIAL_ACCESS, "weighted-raw", "central"
        ),
    }
    sweep_stable = (
        orderings["central"] == orderings["sweep_low"] == orderings["sweep_high"]
    )
    policy_stable = orderings["central"] == orderings["uniform_central"]
    raw_stable = orderings["central"] == orderings["raw_central"]

    return {
        "schema": manifest["schema"],
        "declared": manifest["declared"],
        "impossible_arms": manifest["impossible_arms"],
        "cell_stats": stats,
        "orderings_by_median_net_time_to_objective": orderings,
        "ordering_stable_across_sweep_extremes": sweep_stable,
        "ordering_stable_weighted_vs_uniform": policy_stable,
        "ordering_stable_dedup_vs_raw": raw_stable,
        "aggregate_conditional_net_tto_central": _aggregate_conditional_tto(
            library, "central"
        ),
        "occupancy_l1_vs_aggregate_central": _occupancy_l1_vs_aggregate(
            stats, "central"
        ),
    }


def _verdict(report: dict) -> list:
    """The computed verdict paragraph — plain English, envelope-relative."""
    stats = report["cell_stats"]
    order = report["orderings_by_median_net_time_to_objective"]["central"]
    l1 = report["occupancy_l1_vs_aggregate_central"]
    lines = []
    ranked = " < ".join(f"`{p}`" for p in order)
    lines.append(
        f"On the primary cell (initial-access entry, weighted routing on the "
        f"operator-deduplicated corpus, central dwells) the envelopes rank "
        f"{ranked} by median net time-to-objective — an envelope statistic, "
        f"not the DES MTTC."
    )
    if report["ordering_stable_across_sweep_extremes"]:
        lines.append(
            "That ordering **survives the catalogue's own sweep band**: it is "
            "identical at both duration extremes (every dwell at its "
            "anchor-unit sweep bound), so the behavioural separation is not an "
            "artefact of the v0 dwell point-values."
        )
    else:
        lines.append(
            "That ordering does **not** survive the catalogue's sweep band — "
            "it changes at one or both duration extremes "
            f"(low: {', '.join(report['orderings_by_median_net_time_to_objective']['sweep_low'])}; "
            f"high: {', '.join(report['orderings_by_median_net_time_to_objective']['sweep_high'])}) — "
            "so any ranking claim must be quoted with its dwell variant."
        )
    if report["ordering_stable_weighted_vs_uniform"]:
        lines.append(
            "The same ordering holds under the uniform (structural-floor) "
            "policy, so it is carried by net shape at least as much as by the "
            "W-A weight layer."
        )
    else:
        lines.append(
            "Under the uniform (structural-floor) policy the ordering differs "
            f"({', '.join(report['orderings_by_median_net_time_to_objective']['uniform_central'])}), "
            "so the W-A weight layer, not shape alone, carries part of the "
            "behavioural separation."
        )
    if not report["ordering_stable_dedup_vs_raw"]:
        lines.append(
            "The raw-corpus robustness arm reorders the envelopes "
            f"({', '.join(report['orderings_by_median_net_time_to_objective']['raw_central'])}); "
            "the operator-dedup discipline is load-bearing for the ranking."
        )
    else:
        lines.append(
            "The raw-corpus robustness arm preserves the ordering, so the "
            "operator-dedup discipline does not drive the ranking."
        )
    de_cell = stats.get(
        _cell_id("double_extortion", ENTRY_INITIAL_ACCESS, PRIMARY_ARM, "central")
    )
    if de_cell:
        lines.append(
            f"`double_extortion`'s visited-set objective (impact **and** "
            f"exfiltration) completes in {de_cell['objective_rate']:.0%} of "
            f"primary-cell runs (the rest cap or stall) — the single-token "
            f"both-achieved condition is exercisable but demanding on the "
            f"observed-only base."
        )
    if l1:
        hi = max(l1, key=l1.get)
        lo = min(l1, key=l1.get)
        lines.append(
            f"Per-tactic occupancy separates the envelopes from the null "
            f"profile by mean-dwell-share L1 distance "
            f"{l1[lo]:.2f} (`{lo}`) to {l1[hi]:.2f} (`{hi}`); the recon-seeded "
            f"arm exists only where the prefix gap is bridged, and its "
            f"impossibility on `double_extortion` / `infrastructure_setup` is "
            f"itself a recorded envelope result."
        )
    return lines


def write_report_md(report: dict, out_path: Path = REPORT_MD) -> Path:
    """Render the behavioural verification report (numbers also persisted to
    ``timeline_report.json`` for the test gate)."""
    d = report["declared"]
    lines = [
        "# Timeline-runner behavioural verification report — do the four "
        "class envelopes behave differently?",
        "",
        "The behavioural half of the profile-discrimination verification (the",
        "structural half is [`divergence_report.md`](divergence_report.md)).",
        "Summary statistics over the seeded timeline library generated by",
        "`python -m mtdsim.l3_simulation.timeline`; the full aggregated",
        "variation analysis stays deferred backlog (D10).",
        "",
        "**Reading frame:** each timeline is one instantiation of a class",
        "**envelope**, never an actor's campaign. The time statistic is the",
        "**net time-to-objective** — the walk's cumulative clock at objective",
        "completion — which is *not* the DES MTTC and is never comparable to",
        "it (metrics_semantics.md §(a)/(d)). Dwells are the v0 uncalibrated",
        "catalogue; absolute seconds are shape-not-scale placeholders, and",
        "only orderings/ratios carry meaning.",
        "",
        "## Declared run-matrix constants",
        "",
        f"- {d['n_runs_per_cell']} seeded runs per cell; step cap "
        f"{d['max_steps']} states (capped walks are a recorded outcome).",
        f"- Seed derivation: `{d['seed_derivation']}` — the library is fully",
        "  reproducible; no wall-clock anywhere.",
        f"- Duration variants: {', '.join(d['duration_variants'])}; "
        "sweep extremes computed **in group-anchor units** "
        "(`anchors[group].duration_s × sweep_bound`).",
        f"- Weight variants: `{d['primary_weight_variant']}` primary; raw arm "
        f"{d['raw_arm']}.",
        "- Objective rules: the four class nets terminate when the visited",
        "  set covers **all** declared objective tactics (for",
        "  `double_extortion` that is the both-achieved visited-set",
        "  condition); the **aggregate** terminates on **any** of its",
        "  declared union set {command-and-control, exfiltration, impact} —",
        "  the null envelope has no single operational objective (recorded",
        "  choice; `completed_objectives` records which one ended each run).",
        "- `stalled` (no fireable out-transition) is a legitimate, recorded",
        "  outcome of the envelope, not an error.",
        "",
        "## Recon-seeded arm — where it exists and where it cannot",
        "",
        "D8 asks for both entries. On the observed-only base the recon arm",
        "exists only where the prefix gap is bridged:",
        "",
    ]
    for arm in report["impossible_arms"]:
        lines.append(
            f"- **`{arm['profile']}`, entry `reconnaissance` — {arm['status']}.** "
            f"{arm['reason']}"
        )
    lines += [
        "",
        "## Primary cells — initial-access entry, weighted (operator-dedup), "
        "central dwells",
        "",
        "| Profile | outcomes | objective rate | median net t-to-obj | "
        "p10–p90 | mean states | top occupancy (mean dwell share) |",
        "|---|---|--:|--:|--:|--:|---|",
    ]
    stats = report["cell_stats"]
    for profile in PROFILE_NAMES:
        s = stats.get(_cell_id(profile, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, "central"))
        if not s:
            continue
        tto = s["net_time_to_objective_s"]
        lines.append(
            f"| `{profile}` | {_fmt_outcomes(s)} | {s['objective_rate']:.0%} | "
            f"{_fmt_s(tto['median'] if tto else None)} | "
            f"{(_fmt_s(tto['p10']) + '–' + _fmt_s(tto['p90'])) if tto else '—'} | "
            f"{s['mean_n_states']:.1f} | {_top_occupancy(s)} |"
        )
    lines += [
        "",
        "## Recon-seeded cells (bridged profiles only; same arm)",
        "",
        "| Profile | outcomes | objective rate | median net t-to-obj |",
        "|---|---|--:|--:|",
    ]
    for profile in PROFILE_NAMES:
        s = stats.get(_cell_id(profile, ENTRY_RECON, PRIMARY_ARM, "central"))
        if not s:
            continue
        tto = s["net_time_to_objective_s"]
        lines.append(
            f"| `{profile}` | {_fmt_outcomes(s)} | {s['objective_rate']:.0%} | "
            f"{_fmt_s(tto['median'] if tto else None)} |"
        )
    lines += [
        "",
        "## Sweep extremes — does the ranking survive the band? "
        "(initial-access, weighted operator-dedup)",
        "",
        "| Profile | median net t-to-obj @ sweep_low | @ central | @ sweep_high |",
        "|---|--:|--:|--:|",
    ]
    for profile in PROFILE_NAMES:
        row = [f"| `{profile}` "]
        for variant in ("sweep_low", "central", "sweep_high"):
            m = _median(stats, _cell_id(profile, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, variant))
            row.append(f"| {_fmt_s(m)} ")
        lines.append("".join(row) + "|")
    lines += [
        "",
        "## Policy and corpus-variant sensitivity (initial-access, central "
        "dwells)",
        "",
        "| Profile | median net t-to-obj weighted-dedup | weighted-raw | "
        "uniform (structural floor) | objective rate dedup / raw / uniform |",
        "|---|--:|--:|--:|---|",
    ]
    for profile in PROFILE_NAMES:
        cells = {
            arm: stats.get(_cell_id(profile, ENTRY_INITIAL_ACCESS, arm, "central"))
            for arm in (PRIMARY_ARM, "weighted-raw", "uniform")
        }
        medians = {
            arm: (
                s["net_time_to_objective_s"]["median"]
                if s and s["net_time_to_objective_s"]
                else None
            )
            for arm, s in cells.items()
        }
        rates = " / ".join(
            f"{cells[arm]['objective_rate']:.0%}" if cells[arm] else "—"
            for arm in (PRIMARY_ARM, "weighted-raw", "uniform")
        )
        lines.append(
            f"| `{profile}` | {_fmt_s(medians[PRIMARY_ARM])} | "
            f"{_fmt_s(medians['weighted-raw'])} | {_fmt_s(medians['uniform'])} | "
            f"{rates} |"
        )
    lines += [
        "",
        "## Class vs aggregate — same-objective comparison (central dwells)",
        "",
        "The aggregate's any-rule runs are split by which union objective",
        "completed, so each class is compared against the aggregate runs that",
        "achieved *its* objective. `double_extortion` has no aggregate",
        "counterpart — the any-rule walk stops at its first objective and can",
        "never complete the both-achieved pair (recorded limit of the",
        "comparison).",
        "",
        "| Class | class median net t-to-obj | aggregate median "
        "(same objective, n) | occupancy L1 vs aggregate |",
        "|---|--:|--:|--:|",
    ]
    agg_split = report["aggregate_conditional_net_tto_central"]
    l1 = report["occupancy_l1_vs_aggregate_central"]
    class_objective = {
        "pure_steal": "exfiltration",
        "pure_impediment": "impact",
        "double_extortion": None,
        "infrastructure_setup": "command-and-control",
    }
    for profile in CLASS_NAMES:
        m = _median(stats, _cell_id(profile, ENTRY_INITIAL_ACCESS, PRIMARY_ARM, "central"))
        objective = class_objective[profile]
        agg = agg_split.get(objective) if objective else None
        agg_txt = f"{_fmt_s(agg['median'])} (n={agg['n']})" if agg else "—"
        lines.append(
            f"| `{profile}` | {_fmt_s(m)} | {agg_txt} | {l1.get(profile, 0):.2f} |"
        )
    lines += ["", "## Verdict", ""]
    for line in _verdict(report):
        lines.append(line)
        lines.append("")
    out_path.write_text("\n".join(lines))
    with open(REPORT_JSON, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return out_path


def write_example(library: dict, out_path: Path = EXAMPLE_PATH) -> Path:
    """The small committed example: for each outcome kind, the shortest record
    in the library (scan in manifest cell order, ties to the first seen) —
    the schema document's living companion."""
    chosen: dict[str, dict] = {}
    for records in library.values():
        for r in records:
            best = chosen.get(r["outcome"])
            if best is None or r["n_states"] < best["n_states"]:
                chosen[r["outcome"]] = r
    with open(out_path, "w") as f:
        for outcome in ("objective", "stalled", "cap"):
            if outcome in chosen:
                f.write(serialise(chosen[outcome]) + "\n")
    return out_path


__all__ = [
    "EXAMPLE_PATH",
    "PRIMARY_ARM",
    "REPORT_JSON",
    "REPORT_MD",
    "build_report",
    "cell_stats",
    "write_example",
    "write_report_md",
]
