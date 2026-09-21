"""The §5.3.1 no-defence corpus — the reader half.

Pure over ``runs.jsonl``: no simulation, no mutation; the only RNG is the seeded
split-half null inside the shipped suite. Every measure is ``measures.py``'s.
Computes every number the three §5.3.1 floats could quote (Fig. 5.2 coverage +
opening variety; the pairwise divergence, demoted to body-text content 2026-09-21; Tab. 5.4 summary), the same table
at the 60 000 s extension, and the general-objective diagnostic arm's deltas.
Writes ``numbers.json``, ``preview_tab54.md``, ``preview_fig52.png`` and
``preview_fig53.png`` beside itself. Previews are for reading the direction —
not the house style; the TikZ generators follow acceptance.

    PYTHONPATH=src python data/results/ch5_s531_unopposed/analyse.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from statistics import median

import numpy as np

from mtdsim.l3_simulation.movement.attacker import MovementRecord
from mtdsim.l3_simulation.movement import measures as M
from mtdsim.l3_simulation.movement.statistics import MovementRunResult

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs.jsonl"

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
FOUR = PROFILES[:4]
LABEL = {
    "objective_exfiltration": "exfiltration",
    "objective_impact": "impact",
    "objective_exfiltration_impact": "double extortion",
    "objective_none_c2": "no realised objective",
    "aggregate": "aggregate",
    "baseline": "baseline attacker",
}
# Fixed series order and hue, validated (dataviz six checks, light surface).
COLOUR = {
    "objective_exfiltration": "#1f548c",
    "objective_impact": "#b3261e",
    "objective_exfiltration_impact": "#a8741a",
    "objective_none_c2": "#6f4e9c",
    "aggregate": "#3a7d44",
    "baseline": "#7a7a7a",
}
MARKER = {
    "objective_exfiltration": "o",
    "objective_impact": "s",
    "objective_exfiltration_impact": "^",
    "objective_none_c2": "D",
    "aggregate": "v",
    "baseline": "",
}
CORE = 15_000
EXT = 60_000
GRID_STEP = 250
K_MAX = 8
K_TABLE = 5
N_SPLITS = 200
Q = 0.975


# --- loading ---------------------------------------------------------------


def _movement_result(row: dict) -> MovementRunResult:
    raw = row["records"]
    records = tuple(
        MovementRecord(
            profile=row["profile"],
            step_index=i,
            place=r[0],
            verb=r[1],
            outcome=r[2],
            verdict=r[3],
            interrupted=bool(r[5]),
            blocked=bool(r[4]),
            next_place=(raw[i + 1][0] if i + 1 < len(raw) else row.get("last_next_place")),
            start_time=r[7],
            end_time=r[8],
            dwell=r[6],
            interrupted_by="",
            place_class=r[9],
        )
        for i, r in enumerate(raw)
    )
    return MovementRunResult(
        profile=row["profile"],
        seed=row["seed"],
        with_synthetic_overlay=True,
        records=records,
        reached_objective=row["reached_objective"],
        termination_time=row["termination_time"],
        compromised_count=row["compromised"],
        retrace_count=row.get("retrace_count", 0),
        database_hosts_reached=row["database_hosts_reached"],
        first_database_reach_time=row["first_database_reach_time"],
        attack_objective=row["objective"],
        target_hosts=tuple(row["target_hosts"]),
    )


def load() -> tuple[dict, dict, list]:
    """movement[(objective, horizon, profile)] -> runs; baseline[horizon] -> rows; errors."""
    movement: dict[tuple, list[MovementRunResult]] = {}
    baseline: dict[int, list[dict]] = {}
    errors: list[dict] = []
    with RUNS.open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if "error" in row:
                errors.append(row)
                continue
            if row["arm"] == "baseline":
                baseline.setdefault(row["horizon"], []).append(row)
            else:
                movement.setdefault((row["objective"], row["horizon"], row["profile"]), []).append(
                    _movement_result(row)
                )
    return movement, baseline, errors


# --- Fig. 5.2(a): coverage against simulated time ---------------------------


def coverage_grid(runs: list[MovementRunResult], horizon: int) -> dict:
    """Mean distinct places by sim time on a common grid, held at the final
    value after a run terminates (right-censored; no new place can appear)."""
    grid = np.arange(0, horizon + GRID_STEP, GRID_STEP, dtype=float)
    per_run = np.zeros((len(runs), len(grid)))
    for i, run in enumerate(runs):
        firsts = np.array([t for t, _ in M.distinct_place_curve(run)])
        per_run[i] = np.searchsorted(firsts, grid, side="right")
    mean = per_run.mean(axis=0)
    ci = 1.96 * per_run.std(axis=0, ddof=1) / np.sqrt(len(runs))
    return {"t": grid.tolist(), "mean": mean.tolist(), "ci95": ci.tolist()}


def baseline_coverage_grid(rows: list[dict], horizon: int) -> dict:
    """The reference: distinct verbs reached against time (activities, not
    tactics — the baseline has no tactic vocabulary)."""
    grid = np.arange(0, horizon + GRID_STEP, GRID_STEP, dtype=float)
    per_run = np.zeros((len(rows), len(grid)))
    for i, row in enumerate(rows):
        seen: set[str] = set()
        firsts = []
        for name, start, *_ in row["records"]:
            if name not in seen:
                seen.add(name)
                firsts.append(start)
        per_run[i] = np.searchsorted(np.array(firsts), grid, side="right")
    mean = per_run.mean(axis=0)
    ci = 1.96 * per_run.std(axis=0, ddof=1) / np.sqrt(len(rows))
    return {"t": grid.tolist(), "mean": mean.tolist(), "ci95": ci.tolist()}


# --- Tab. 5.4 rows ---------------------------------------------------------


def _iv(values) -> dict:
    iv = M.mean_ci(list(values))
    return {"n": iv.n, "mean": iv.mean, "ci95": iv.ci95}


def commonest_opening_share(seqs: list[tuple], k: int) -> float:
    """Share of runs that follow the most common length-``k`` opening. Unlike a
    count of distinct openings it is not capped by the number of runs."""
    return Counter(s[:k] for s in seqs).most_common(1)[0][1] / len(seqs)


def tactic_entry_share(runs: list[MovementRunResult]) -> dict:
    """``tactic -> share of runs that enter it``; a tactic no run entered is absent."""
    entered = Counter(t for r in runs for t in {rec.place for rec in r.records})
    return {t: c / len(runs) for t, c in sorted(entered.items())}


def tactic_visit_share(runs: list[MovementRunResult], profile: str) -> dict:
    """``tactic -> share of the profile's steps spent in it``, pooled over the
    runs (the distribution the divergence matrix is computed over). A tactic
    the profile holds and never enters reads 0.0; one it does not hold is absent."""
    from mtdsim.l3_simulation.movement.net import load_routing_net

    visits = Counter(rec.place for r in runs for rec in r.records)
    total = sum(visits.values())
    held = load_routing_net(profile, with_synthetic_overlay=True).places
    return {t: visits.get(t, 0) / total for t in sorted(set(held) | set(visits))}


def movement_row(runs: list[MovementRunResult], stage_of: dict) -> dict:
    depth = [
        (d if (d := M.deepest_successful_stage(r, stage_of)) is not None else -1) for r in runs
    ]
    ended = Counter(M.terminal_mode(r) for r in runs)
    reach_times = [
        (r.first_database_reach_time if r.first_database_reach_time is not None else r.termination_time)
        for r in runs
        if r.reached_objective
    ]
    return {
        "n": len(runs),
        "distinct_tactics": _iv(M.distinct_place_count(r) for r in runs),
        "deepest_successful_stage": _iv(depth),
        "no_success_share": sum(1 for d in depth if d < 0) / len(runs),
        # the axis-1 progression measure: did the run act successfully at a
        # stage strictly deeper than the one it first succeeded at (None = no
        # success at all, counted as not advanced)
        "advanced_after_first_success": sum(
            1 for r in runs if M.advanced_after_first_success(r, stage_of)
        ) / len(runs),
        "first_success_stage": _iv(
            (s if (s := M.first_success_stage(r, stage_of)) is not None else -1) for r in runs
        ),
        "distinct_openings": {str(k): M.distinct_prefixes(runs, k) for k in range(1, K_MAX + 1)},
        "commonest_opening_share": {
            str(k): commonest_opening_share([M.place_sequence(r) for r in runs], k)
            for k in range(1, K_MAX + 1)
        },
        "tactic_entry_share": tactic_entry_share(runs),
        "tactic_visit_share": tactic_visit_share(runs, runs[0].profile),
        "path_entropy": M.path_entropy(runs),
        "hub_share": max(M.visit_distribution(runs).values()),
        "hosts": _iv(r.compromised_count for r in runs),
        # repetition — the persistence-in-outcome measure (measures.py §(c)):
        # successful actions per distinct host; None at zero hosts is excluded
        # and its count reported
        "successes_per_host": _iv(
            v for r in runs if (v := M.successes_per_distinct_host(r)) is not None
        ),
        "zero_host_runs": sum(1 for r in runs if r.compromised_count == 0),
        "n_successes": _iv(M.n_successes(r) for r in runs),
        "ended": {k: v / len(runs) for k, v in sorted(ended.items())},
        "target_reach": sum(1 for r in runs if r.reached_objective) / len(runs),
        "time_to_target_median": (median(reach_times) if reach_times else None),
        "database_hosts_reached": _iv(r.database_hosts_reached for r in runs),
        "retrace_count": _iv(r.retrace_count for r in runs),
        "records_per_run": _iv(len(r.records) for r in runs),
    }


def baseline_row(rows: list[dict]) -> dict:
    verbs = [len({rec[0] for rec in row["records"]}) for row in rows]
    reached = [row for row in rows if row["reached_objective"]]

    def _ttt(row: dict) -> float | None:
        # The baseline keeps running to the horizon after the target falls, so
        # time to target is the first compromise of a target host in its record.
        targets = set(row["target_hosts"])
        hits = [rec[2] for rec in row["records"] if rec[3] is not None and rec[3] in targets]
        return min(hits) if hits else None

    ttts = [t for row in reached if (t := _ttt(row)) is not None]
    n_target = len(ttts)
    n_ratio = len(reached) - n_target  # end_event fired on the inherited 80 % compromise ratio
    # The baseline is measured the way the profiles are, over its recorded
    # activity sequence (Marc, 2026-09-20): its ordering branches where an
    # exploit fails, so "one opening at every length" is not a structural fact.
    # A step is a phase ENTERED, the unit the profiles are counted in (a profile
    # record is a tactic entered and never repeats its predecessor), so the
    # baseline's consecutive repeats of one phase are collapsed.
    seqs = [
        tuple(n for i, n in enumerate(names) if i == 0 or n != names[i - 1])
        for names in ([rec[0] for rec in row["records"]] for row in rows)
    ]
    out_counts: dict[str, Counter] = {}
    for seq in seqs:
        for a, b in zip(seq, seq[1:]):
            out_counts.setdefault(a, Counter())[b] += 1
    return {
        "n": len(rows),
        "distinct_verbs": _iv(verbs),
        "distinct_tactics": None,  # structural: no tactic vocabulary
        "deepest_successful_stage": None,
        "distinct_openings": {str(k): len({q[:k] for q in seqs}) for k in range(1, K_MAX + 1)},
        "commonest_opening_share": {
            str(k): commonest_opening_share(seqs, k) for k in range(1, K_MAX + 1)
        },
        "path_entropy": M.path_entropy_from_transitions(out_counts),
        "hosts": _iv(row["compromised"] for row in rows),
        "ended": {
            "objective": n_target / len(rows),
            "compromise_ratio": n_ratio / len(rows),
            "horizon": 1 - len(reached) / len(rows),
        },
        "target_reach": n_target / len(rows),
        "time_to_target_median": (median(ttts) if ttts else None),
        "ended_on_compromise_ratio": n_ratio,
        "database_hosts_reached": _iv(row["database_hosts_reached"] for row in rows),
        "records_per_run": _iv(len(row["records"]) for row in rows),
    }


# --- Fig. 5.3 ----------------------------------------------------------------


def _place_shares(runs: list[MovementRunResult]) -> dict:
    """``place -> share of every record``: the denominator of ``tactic_visit_share``."""
    visits = Counter(rec.place for r in runs for rec in r.records)
    total = sum(visits.values())
    return {t: c / total for t, c in visits.items()}


def _jsd_terms(p: dict, q: dict) -> dict:
    """Each tactic's term of the squared Jensen-Shannon distance (base 2) between
    two share distributions; the terms sum to the divergence."""
    keys = set(p) | set(q)
    out = {}
    for k in keys:
        a, b = p.get(k, 0.0), q.get(k, 0.0)
        m = (a + b) / 2
        term = 0.0
        if a > 0:
            term += 0.5 * a * np.log2(a / m)
        if b > 0:
            term += 0.5 * b * np.log2(b / m)
        out[k] = float(term)
    return out


def divergence_matrix(runs: list[MovementRunResult]) -> dict:
    """Pairwise divergence between the four profiles' pooled share of steps in
    each tactic (the distribution Fig. 5.1(a) prints, every record counted --
    reconciled 2026-09-21: the suite's ``divergence_report`` counts only records
    with a verb or a positive dwell, which drops the zero-second resource
    development entries on two profiles), against each profile's split-half
    null on the same denominator. Also the share of each pair's divergence
    carried by tactics that only one profile of the pair ever entered. DEMOTED
    from a figure to body-text content 2026-09-21 (results context §8d); the
    terminal-tactic half is kept from the suite as it was."""
    report = M.divergence_report(runs, n_splits=N_SPLITS, seed=0, q=Q)
    by_profile = {p: [r for r in runs if r.profile == p] for p in FOUR}
    shares = {p: _place_shares(by_profile[p]) for p in FOUR}
    rng = np.random.default_rng(0)
    out = {"profiles": list(FOUR), "q": Q, "n_splits": N_SPLITS, "denominator": "every record"}
    cells = {}
    for a in FOUR:
        for b in FOUR:
            if a == b:
                rs = by_profile[a]
                draws = []
                for _ in range(N_SPLITS):
                    idx = rng.permutation(len(rs))
                    half = len(rs) // 2
                    draws.append(sum(_jsd_terms(_place_shares([rs[i] for i in idx[:half]]),
                                                _place_shares([rs[i] for i in idx[half:]])).values()))
                cells[f"{a}|{b}"] = {
                    "null_ceiling": float(np.quantile(draws, Q)),
                    "null_median": float(np.median(draws)),
                }
            else:
                terms = _jsd_terms(shares[a], shares[b])
                jsd = sum(terms.values())
                absent = [k for k in terms if shares[a].get(k, 0.0) == 0.0 or shares[b].get(k, 0.0) == 0.0]
                cells[f"{a}|{b}"] = {
                    "jsd": float(jsd),
                    "absent_tactic_share": float(sum(terms[k] for k in absent) / jsd) if jsd else 0.0,
                    "absent_tactics": sorted(absent),
                    "largest_term": max(terms, key=terms.get),
                }
    out["visit_stream"] = cells
    out["terminal"] = {}
    cleared = report.cleared("terminal")
    for a in FOUR:
        for b in FOUR:
            if a == b:
                draws = np.array(report.nulls[a].terminal)
                out["terminal"][f"{a}|{b}"] = {
                    "null_ceiling": float(np.quantile(draws, Q)),
                    "null_median": float(np.median(draws)),
                }
            else:
                pair = (a, b) if a < b else (b, a)
                out["terminal"][f"{a}|{b}"] = {
                    "jsd": report.divergence.terminal[pair],
                    "pair_ceiling": report.pair_ceiling(*pair, half="terminal"),
                    "clears_pair_ceiling": cleared[pair],
                }
    # the former caption's rule: a pair is separated where its cell exceeds BOTH diagonals it meets
    sep = {}
    for a in FOUR:
        for b in FOUR:
            if a < b:
                v = cells[f"{a}|{b}"]["jsd"]
                sep[f"{a}|{b}"] = bool(v > cells[f"{a}|{a}"]["null_ceiling"] and v > cells[f"{b}|{b}"]["null_ceiling"])
    out["visit_stream_separated_by_caption_rule"] = sep
    off = [c["jsd"] for k, c in cells.items() if "jsd" in c]
    diag = [c["null_ceiling"] for k, c in cells.items() if "null_ceiling" in c]
    pairs = {k: c["jsd"] for k, c in cells.items() if "jsd" in c and k.split("|")[0] < k.split("|")[1]}
    out["body_facts"] = {
        "min_pair": min(pairs, key=pairs.get), "min_jsd": min(off),
        "max_pair": max(pairs, key=pairs.get), "max_jsd": max(off),
        "max_null_ceiling": max(diag), "min_ratio_to_null": min(off) / max(diag),
        "mean_to_others": {p: float(np.mean([cells[f"{p}|{q}"]["jsd"] for q in FOUR if q != p])) for p in FOUR},
    }
    return out


# --- previews -----------------------------------------------------------------


def preview_fig52(cov: dict, openings: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (a, z, b) = plt.subplots(1, 3, figsize=(15, 4.2))
    for ax in (a, z, b):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#e5e5e5", linewidth=0.5)
        ax.set_axisbelow(True)
    for p in PROFILES:
        c = cov[p]
        t = np.array(c["t"])
        m = np.array(c["mean"])
        e = np.array(c["ci95"])
        a.plot(t, m, color=COLOUR[p], linewidth=1.6, label=LABEL[p],
               marker=MARKER[p], markevery=8, markersize=4)
        a.fill_between(t, m - e, m + e, color=COLOUR[p], alpha=0.12, linewidth=0)
    c = cov["baseline"]
    a.plot(c["t"], c["mean"], color=COLOUR["baseline"], linewidth=1.4, linestyle="--",
           label="baseline attacker (distinct verbs)")
    a.set_xlabel("simulated time (s)")
    a.set_ylabel("distinct tactics reached")
    a.set_xlim(0, CORE)
    a.legend(frameon=False, fontsize=8, loc="lower right")
    a.set_title("(a)", loc="left", fontsize=10)
    for p in PROFILES:
        c = cov[p]
        t = np.array(c["t"]); m = np.array(c["mean"]); e = np.array(c["ci95"])
        z.plot(t, m, color=COLOUR[p], linewidth=1.6, marker=MARKER[p], markevery=1, markersize=4)
        z.fill_between(t, m - e, m + e, color=COLOUR[p], alpha=0.12, linewidth=0)
    z.plot(cov["baseline"]["t"], cov["baseline"]["mean"], color=COLOUR["baseline"], linewidth=1.4, linestyle="--")
    z.set_xlim(0, 3000)
    z.set_xlabel("simulated time (s), first 3 000 s")
    z.set_title("(a, zoom)", loc="left", fontsize=10)

    ks = list(range(1, K_MAX + 1))
    for p in PROFILES:
        b.plot(ks, [100 * openings[p][str(k)] for k in ks], color=COLOUR[p], linewidth=1.6,
               marker=MARKER[p], markersize=5, label=LABEL[p])
    b.plot(ks, [100 * openings["baseline"][str(k)] for k in ks], color=COLOUR["baseline"],
           linewidth=1.4, linestyle="--", label="baseline attacker (measured, activities)")
    b.set_xlabel("length of the opening (steps)")
    b.set_ylabel("runs following the commonest opening (%)")
    b.set_xticks(ks)
    b.set_title("(b)", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def preview_fig53(div: dict, path: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n = len(FOUR)
    vals = np.zeros((n, n))
    for i, a in enumerate(FOUR):
        for j, b in enumerate(FOUR):
            cell = div["visit_stream"][f"{a}|{b}"]
            vals[i, j] = cell["null_ceiling"] if i == j else cell["jsd"]
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    ax.imshow(vals, cmap="Greys", vmin=0, vmax=vals.max() * 1.15)
    for i in range(n):
        for j in range(n):
            txt = f"{vals[i, j]:.4f}" if i == j else f"{vals[i, j]:.3f}"
            ax.text(j, i, txt, ha="center", va="center", fontsize=9,
                    color="white" if vals[i, j] > vals.max() * 0.6 else "black")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels([LABEL[p] for p in FOUR], rotation=25, ha="right", fontsize=8)
    ax.set_yticklabels([LABEL[p] for p in FOUR], fontsize=8)
    ax.set_title("visit-stream JSD; diagonal = own split-half null ceiling (q=0.975)",
                 fontsize=8, loc="left")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def _fmt_iv(d: dict | None, nd: int = 2) -> str:
    if d is None:
        return "—"
    return f"{d['mean']:.{nd}f} [{d['mean'] - d['ci95']:.{nd}f}, {d['mean'] + d['ci95']:.{nd}f}]"


def table_md(rows: dict[str, dict], title: str) -> str:
    lines = [
        f"### {title}",
        "",
        "| attacker | distinct tactics | deepest stage acted on | no-success share | openings k=5 /100 | path entropy (hub share) | hosts reached | ended: objective / horizon / other | database hosts | median time to target (s) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for p in (*PROFILES, "baseline"):
        if p not in rows:
            continue
        r = rows[p]
        ended = r["ended"]
        other = 1 - ended.get("objective", 0) - ended.get("horizon", 0)
        if p == "baseline":
            dt = f"{_fmt_iv(r['distinct_verbs'])} verbs (structural)"
            depth = "—"
            nos = "—"
            ent = f"{r['path_entropy']:.2f} (over activities)"
        else:
            dt = _fmt_iv(r["distinct_tactics"])
            depth = _fmt_iv(r["deepest_successful_stage"])
            nos = f"{r['no_success_share']:.2f}"
            ent = f"{r['path_entropy']:.3f} ({r['hub_share']:.2f})"
        ttt = "—" if r["time_to_target_median"] is None else f"{r['time_to_target_median']:.0f}"
        lines.append(
            f"| {LABEL[p]} | {dt} | {depth} | {nos} | {r['distinct_openings'][str(K_TABLE)]} | {ent} | "
            f"{_fmt_iv(r['hosts'])} | {ended.get('objective', 0):.2f} / {ended.get('horizon', 0):.2f} / {other:.2f} | "
            f"{_fmt_iv(r['database_hosts_reached'])} | {ttt} |"
        )
    return "\n".join(lines) + "\n"


def divergence_md(div: dict, title: str) -> str:
    lines = [f"### {title}", "", "| | " + " | ".join(LABEL[p] for p in FOUR) + " |", "|---|" + "---|" * len(FOUR)]
    for a in FOUR:
        cells = []
        for b in FOUR:
            c = div["visit_stream"][f"{a}|{b}"]
            if a == b:
                cells.append(f"**{c['null_ceiling']:.4f}**")
            else:
                cells.append(f"{c['jsd']:.3f}")
        lines.append(f"| {LABEL[a]} | " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("Separated by the caption's rule (cell > both diagonals): "
                 + ", ".join(f"{k} = {v}" for k, v in div["visit_stream_separated_by_caption_rule"].items()))
    lines.append("")
    lines.append("Terminal-tactic half (not drawn): "
                 + "; ".join(f"{k}: jsd {v['jsd']:.3f} vs ceiling {v['pair_ceiling']:.3f} ({'clears' if v['clears_pair_ceiling'] else 'inside null'})"
                             for k, v in div["terminal"].items() if "jsd" in v and k.split("|")[0] < k.split("|")[1]))
    return "\n".join(lines) + "\n"


def main() -> int:
    movement, baseline, errors = load()
    stage_of = M.load_stage_of()
    out: dict = {"sanity": {}, "core": {}, "extension": {}, "diagnostic": {}}

    # sanity block
    counts = {f"{k[0]}/{k[1]}/{k[2]}": len(v) for k, v in sorted(movement.items())}
    counts.update({f"targeted/{h}/baseline": len(v) for h, v in sorted(baseline.items())})
    out["sanity"] = {
        "error_rows": len(errors),
        "runs_per_cell": counts,
        "all_cells_100": all(v == 100 for v in counts.values()),
        "max_events_hit": sum(
            1 for runs in movement.values() for r in runs if M.terminal_mode(r) == "max_events"
        ),
    }

    # core: the three floats
    cov = {p: coverage_grid(movement[("targeted", CORE, p)], CORE) for p in PROFILES}
    cov["baseline"] = baseline_coverage_grid(baseline[CORE], CORE)
    rows = {p: movement_row(movement[("targeted", CORE, p)], stage_of) for p in PROFILES}
    rows["baseline"] = baseline_row(baseline[CORE])
    four = [r for p in FOUR for r in movement[("targeted", CORE, p)]]
    div = divergence_matrix(four)
    hosts_report = M.interval_report(
        {p: [r.compromised_count for r in movement[("targeted", CORE, p)]] for p in PROFILES}
    )
    tactics_report = M.interval_report(
        {p: [M.distinct_place_count(r) for r in movement[("targeted", CORE, p)]] for p in PROFILES}
    )
    out["core"] = {
        "horizon": CORE,
        "coverage": cov,
        "table": rows,
        "divergence": div,
        "hosts_ordering_supported": hosts_report.ordering_supported,
        "hosts_unseparated_adjacent": hosts_report.unseparated_adjacent_pairs,
        "tactics_ordering_supported": tactics_report.ordering_supported,
        "tactics_unseparated_adjacent": tactics_report.unseparated_adjacent_pairs,
    }

    # extension: same table at 60 000 s, plus the coverage grid at that horizon
    rows_ext = {p: movement_row(movement[("targeted", EXT, p)], stage_of) for p in PROFILES}
    rows_ext["baseline"] = baseline_row(baseline[EXT])
    cov_ext = {p: coverage_grid(movement[("targeted", EXT, p)], EXT) for p in PROFILES}
    cov_ext["baseline"] = baseline_coverage_grid(baseline[EXT], EXT)
    out["extension"] = {"horizon": EXT, "table": rows_ext, "coverage": cov_ext}

    # diagnostic: general objective at the core horizon
    rows_gen = {p: movement_row(movement[("general", CORE, p)], stage_of) for p in PROFILES}
    four_gen = [r for p in FOUR for r in movement[("general", CORE, p)]]
    div_gen = divergence_matrix(four_gen)
    deltas = {
        p: {
            "hosts": rows[p]["hosts"]["mean"] - rows_gen[p]["hosts"]["mean"],
            "distinct_tactics": rows[p]["distinct_tactics"]["mean"] - rows_gen[p]["distinct_tactics"]["mean"],
            "path_entropy": rows[p]["path_entropy"] - rows_gen[p]["path_entropy"],
            "openings_k5": rows[p]["distinct_openings"][str(K_TABLE)] - rows_gen[p]["distinct_openings"][str(K_TABLE)],
            "target_reach": rows[p]["target_reach"] - rows_gen[p]["target_reach"],
        }
        for p in PROFILES
    }
    out["diagnostic"] = {"objective": "general", "horizon": CORE, "table": rows_gen,
                         "divergence": div_gen, "targeted_minus_general": deltas}

    (HERE / "numbers.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")

    md = ["# §5.3.1 preliminary read — behaviour without defence", "",
          f"Sanity: error rows {out['sanity']['error_rows']}; all cells at 100 runs: {out['sanity']['all_cells_100']}; "
          f"max_events terminations: {out['sanity']['max_events_hit']}.", "",
          table_md(rows, f"Tab. 5.4 at the core horizon ({CORE} s), targeted objective, database target"),
          f"Hosts ordering supported: {hosts_report.ordering_supported}; unseparated adjacent: {hosts_report.unseparated_adjacent_pairs}",
          f"Distinct-tactics ordering supported: {tactics_report.ordering_supported}; unseparated adjacent: {tactics_report.unseparated_adjacent_pairs}",
          "",
          divergence_md(div, "Fig. 5.3 — pairwise visit-stream divergence, four profiles (core)"),
          table_md(rows_ext, f"Extension: the same table at {EXT} s"),
          table_md(rows_gen, f"Diagnostic: the same table under the general objective at {CORE} s (not a chapter cell)"),
          "### Targeted minus general, per profile", "",
          "| profile | Δ hosts | Δ distinct tactics | Δ path entropy | Δ openings k=5 | Δ target reach |", "|---|---|---|---|---|---|",
          *[f"| {LABEL[p]} | {d['hosts']:+.2f} | {d['distinct_tactics']:+.2f} | {d['path_entropy']:+.3f} | {d['openings_k5']:+d} | {d['target_reach']:+.2f} |"
            for p, d in deltas.items()],
          "",
          divergence_md(div_gen, "Diagnostic divergence under the general objective"),
          ]
    (HERE / "preview_tab54.md").write_text("\n".join(md), encoding="utf-8")
    preview_fig52(cov, {p: rows[p]["commonest_opening_share"] for p in (*PROFILES, "baseline")}, HERE / "preview_fig52.png")
    preview_fig53(div, HERE / "preview_fig53.png")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
