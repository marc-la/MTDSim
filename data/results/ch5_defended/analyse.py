"""The chapter 5 defended corpus — the reader half.

Pure over ``runs.jsonl``: no simulation, no mutation. One streaming pass turns
every row into a per-run summary through the shipped suite's measures
(``measures.py``: ``interrupt_action_mix``, ``blocked_fraction``,
``cost_ledger``, ``disruption_ledger``, ``mean_ci``), then the five sections'
numbers are computed off the summaries. The only RNG is the seeded bootstrap
on ratio-of-means suppressions, on the rank statistic and on Cliff's delta.

Sections written to ``numbers.json`` (keyed apart):

  sanity   error rows, runs per cell, structural zeros, max_events
  s532     Fig. 5.4 — activity mix before/after each interrupt, treatment vs
           verdict-blind control, {IP shuffle, OS diversity} x {200, 2000};
           the placebo null printed
  s541     Fig. 5.5 / Tab. 5.5 — suppression per profile and condition; delay
           to first compromise with censoring; blocked fraction
  s542     Fig. 5.6 / Tab. 5.6 — suppression per arm; the two orderings;
           Spearman rho with its bootstrap interval; the family contrast
  s543     Tab. 5.7 — the lineage arm (general objective): the three claims
  s55      Fig. 5.7 / 5.8 / Tab. 5.8 — occupancy against suppression; the
           movement arm's time split; effort per host, both arms
  regime   the exponential-regime arm at 200 s, read beside the core

    PYTHONPATH=src python data/results/ch5_defended/analyse.py
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from mtdsim.l3_simulation.movement import measures as M
from mtdsim.l3_simulation.movement.attacker import MovementRecord
from mtdsim.l3_simulation.movement.statistics import MovementRunResult, MTDExecution

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
SINGLES = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle",
           "user_shuffle", "os_diversity", "service_diversity")
SCHEMES = ("random", "alternative")
DEFENDED = SINGLES + SCHEMES
SHORT = {
    "none": "none", "ip_shuffle": "IP", "complete_topology": "topology",
    "host_topology": "host", "port_shuffle": "port", "user_shuffle": "user",
    "os_diversity": "OS", "service_diversity": "service", "random": "random",
    "alternative": "alternative",
}
LAYER = {
    "ip_shuffle": "network", "complete_topology": "network", "host_topology": "network",
    "port_shuffle": "application", "os_diversity": "application", "service_diversity": "application",
    "user_shuffle": "reserve",
}
FAMILY = {"ip_shuffle": "shuffle", "complete_topology": "shuffle", "host_topology": "shuffle",
          "port_shuffle": "shuffle", "user_shuffle": "shuffle",
          "os_diversity": "diversity", "service_diversity": "diversity"}
INTERVALS = (200, 2_000)
SPANNING = ("ip_shuffle", "os_diversity")
ACTIVITIES = ("SCAN_HOST", "ENUM_HOST", "SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE", "SCAN_NEIGHBOR", "")
WINDOW = 5
N_BOOT = 2_000
RNG_SEED = 0


# --- per-run summaries (the one pass over the stream) --------------------------


def _movement_result(row: dict) -> MovementRunResult:
    raw = row["records"]
    records = tuple(
        MovementRecord(
            profile=row["profile"], step_index=i, place=r[0], verb=r[1], outcome=r[2],
            verdict=r[3], interrupted=bool(r[5]), blocked=bool(r[4]),
            next_place=(raw[i + 1][0] if i + 1 < len(raw) else row.get("last_next_place")),
            start_time=r[7], end_time=r[8], dwell=r[6], interrupted_by="", place_class=r[9],
        )
        for i, r in enumerate(raw)
    )
    return MovementRunResult(
        profile=row["profile"], seed=row["seed"], with_synthetic_overlay=True, records=records,
        reached_objective=row["reached_objective"], termination_time=row["termination_time"],
        compromised_count=row["compromised"], retrace_count=row.get("retrace_count", 0),
        mtd_executions=tuple(MTDExecution(name=e[0], start_time=e[1], finish_time=e[2],
                                          duration=e[3], layer=e[4]) for e in row["mtd_executions"]),
        mtd_suspended_count=row["mtd_suspended"], mtd_attack_interrupted=row["mtd_attack_interrupted"],
        database_hosts_reached=row["database_hosts_reached"],
        first_database_reach_time=row["first_database_reach_time"],
        attack_objective=row["objective"], target_hosts=tuple(row["target_hosts"]),
    )


def _key(row: dict) -> tuple:
    return (row["group"], row["arm"], row["profile"], row["objective"], row["condition"],
            row["interval"], row["regime"], row["overlay"])


def summarise_movement(row: dict) -> dict:
    run = _movement_result(row)
    led = M.cost_ledger(run)
    dis = M.disruption_from_run(run)
    mix = M.interrupt_action_mix(run, window=WINDOW)
    visits = M.visit_records(run)
    out = {
        "seed": row["seed"],
        "hosts": run.compromised_count,
        "reached": bool(run.reached_objective),
        "first_compromise": run.first_compromise_time(),
        "elapsed": run.termination_time,
        "terminal": M.terminal_mode(run),
        "blocked_fraction": M.blocked_fraction(run),
        "n_actions": led.n_actions, "n_success": led.n_success,
        "n_interrupted": led.n_interrupted, "n_blocked": led.n_blocked,
        "time_dwell": led.time_dwell, "time_penalty": led.time_mtd_penalty,
        "time_active": led.time_active, "time_interrupted_events": led.time_interrupted_events,
        "n_executed": dis.n_executed, "n_suspended": dis.n_suspended,
        "busy_time": dis.busy_time, "occupancy": dis.occupancy,
        "execs_per_ksec": dis.executions_per_ksec,
        "reconfig_total": dis.reconfig_time_total,
        "substrate_interrupted": row["mtd_attack_interrupted"],
        "mix": None,
        "interrupt_idx": [i for i, r in enumerate(visits) if r.interrupted],
    }
    if mix is not None:
        out["mix"] = {"n": mix.n_interrupts, "before": mix.before_verbs, "after": mix.after_verbs}
    if row["condition"] == "none":  # kept for the placebo null only
        out["visit_verbs"] = [r.verb for r in visits]
    return out


def summarise_baseline(row: dict) -> dict:
    recs = row["records"]
    comps = [r for r in recs if r[3] is not None]
    targets = set(row["target_hosts"])
    hit = [r[2] for r in comps if r[3] in targets]
    execs = [MTDExecution(name=e[0], start_time=e[1], finish_time=e[2], duration=e[3], layer=e[4])
             for e in row["mtd_executions"]]
    dis = M.disruption_ledger(execs, elapsed=row["termination_time"], n_suspended=row["mtd_suspended"])
    return {
        "seed": row["seed"],
        "hosts": row["compromised_uuid"],
        "hosts_positional": row["compromised"],
        "reached": bool(row["reached_objective"]),
        "reached_target": bool(hit),
        "first_compromise": (min(r[2] for r in comps) if comps else None),
        "elapsed": row["termination_time"],
        "blocked_fraction": 0.0,  # structural
        "n_actions": len(recs), "n_success": len(comps),
        "n_interrupted": sum(1 for r in recs if r[5] is not None),
        "n_executed": dis.n_executed, "n_suspended": dis.n_suspended,
        "busy_time": dis.busy_time, "occupancy": dis.occupancy,
        "execs_per_ksec": dis.executions_per_ksec,
        "reconfig_total": dis.reconfig_time_total,
        "substrate_interrupted": row["mtd_attack_interrupted"],
    }


def load() -> tuple[dict, list]:
    """The per-run summaries, cached beside the corpus (``summaries.pkl``) and
    rebuilt whenever the corpus or this file is newer than the cache."""
    import pickle

    cache = HERE / "summaries.pkl"
    if cache.exists() and cache.stat().st_mtime > max(RUNS.stat().st_mtime, Path(__file__).stat().st_mtime):
        with cache.open("rb") as fh:
            return pickle.load(fh)
    cells: dict[tuple, list[dict]] = defaultdict(list)
    errors: list[dict] = []
    with RUNS.open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if "error" in row:
                errors.append(row)
                continue
            s = summarise_baseline(row) if row["arm"] == "baseline" else summarise_movement(row)
            cells[_key(row)].append(s)
    with cache.open("wb") as fh:
        pickle.dump((dict(cells), errors), fh)
    return dict(cells), errors


# --- helpers -------------------------------------------------------------------


def _iv(values) -> dict:
    iv = M.mean_ci([float(v) for v in values])
    return {"n": iv.n, "mean": iv.mean, "ci95": iv.ci95}


def _cell(cells, group, arm, profile, condition, interval, objective="targeted",
          regime="shifted", overlay="v4_failure_only") -> list[dict]:
    if condition == "none":
        interval = 0
    return cells.get((group, arm, profile, objective, condition, interval, regime, overlay), [])


def _pool(cells, group, profiles, condition, interval, **kw) -> list[dict]:
    out = []
    for p in profiles:
        out += _cell(cells, group, "movement", p, condition, interval, **kw)
    return out


def hosts_of(runs) -> np.ndarray:
    return np.array([r["hosts"] for r in runs], dtype=float)


def suppression(none_hosts: np.ndarray, cond_hosts: np.ndarray, rng: np.random.Generator) -> dict:
    """1 - mean(cond) / mean(none), with a seeded bootstrap interval on the
    ratio of means (unpaired: the two cells are resampled independently)."""
    point = 1.0 - cond_hosts.mean() / none_hosts.mean()
    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        n = none_hosts[rng.integers(0, len(none_hosts), len(none_hosts))].mean()
        c = cond_hosts[rng.integers(0, len(cond_hosts), len(cond_hosts))].mean()
        boots[b] = 1.0 - c / n
    lo, hi = np.quantile(boots, [0.025, 0.975])
    diff = M.mean_ci  # noqa: F841  (the absolute difference below uses the suite's interval)
    return {
        "point": float(point), "lo": float(lo), "hi": float(hi),
        "hosts_none": _iv(none_hosts), "hosts_cond": _iv(cond_hosts),
        "absolute_reduction": float(none_hosts.mean() - cond_hosts.mean()),
        "absolute_reduction_ci95": float(1.96 * np.sqrt(none_hosts.var(ddof=1) / len(none_hosts)
                                                        + cond_hosts.var(ddof=1) / len(cond_hosts))),
        "denied_share": float(np.mean(cond_hosts == 0)),
    }


def delay_summary(runs, horizon=15_000) -> dict:
    obs = [r["first_compromise"] for r in runs if r["first_compromise"] is not None]
    return {
        "n": len(runs),
        "observed": _iv(obs) if obs else None,
        "median_observed": (float(np.median(obs)) if obs else None),
        "censored_share": 1 - len(obs) / len(runs),
        "horizon": horizon,
    }


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    """P(x < y) - P(x > y): positive when x sits lower than y."""
    xs = np.sort(x)
    lt = np.searchsorted(xs, y, side="left")     # count of x < y_j
    gt = len(xs) - np.searchsorted(xs, y, side="right")  # count of x > y_j
    return float((lt.sum() - gt.sum()) / (len(x) * len(y)))


def boot_cliff(x, y, rng) -> dict:
    point = cliffs_delta(x, y)
    boots = np.array([cliffs_delta(x[rng.integers(0, len(x), len(x))],
                                   y[rng.integers(0, len(y), len(y))]) for _ in range(N_BOOT // 4)])
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"delta": point, "lo": float(lo), "hi": float(hi)}


# --- §5.3.2 --------------------------------------------------------------------


def mix_block(runs) -> dict:
    """Pooled before/after activity counts and shares, plus the paired
    per-run share shift with its interval (runs without an interrupt drop)."""
    before, after = Counter(), Counter()
    shifts = {a: [] for a in ACTIVITIES}
    n_runs = 0
    n_int = 0
    for r in runs:
        m = r["mix"]
        if m is None:
            continue
        n_runs += 1
        n_int += m["n"]
        before.update(m["before"])
        after.update(m["after"])
        tb, ta = sum(m["before"].values()), sum(m["after"].values())
        for a in ACTIVITIES:
            shifts[a].append((m["after"].get(a, 0) / ta if ta else 0.0)
                             - (m["before"].get(a, 0) / tb if tb else 0.0))
    tb, ta = sum(before.values()), sum(after.values())
    share_b = {a: before.get(a, 0) / tb if tb else 0.0 for a in ACTIVITIES}
    share_a = {a: after.get(a, 0) / ta if ta else 0.0 for a in ACTIVITIES}
    return {
        "runs_with_interrupt": n_runs, "runs": len(runs), "interrupts": n_int,
        "before": share_b, "after": share_a,
        "shift": {a: _iv(v) for a, v in shifts.items() if v},
        "jsd_before_after": M.jsd(M.normalise(dict(before)), M.normalise(dict(after))),
        "unmapped_activities": sorted(set(before) | set(after) - set(ACTIVITIES)),
    }


def placebo_block(defended, unopposed) -> dict:
    """The placebo null: each defended run's interrupt positions applied to the
    same seed's unopposed run of the same arm (a matched, time-confound-free
    control, per the 2026-09-09 inference note)."""
    by_seed = {r["seed"]: r for r in unopposed}
    before, after = Counter(), Counter()
    n = 0
    for d in defended:
        u = by_seed.get(d["seed"])
        if u is None or not d["interrupt_idx"]:
            continue
        verbs = u["visit_verbs"]
        for i in d["interrupt_idx"]:
            if i >= len(verbs):
                continue
            n += 1
            before.update(verbs[max(0, i - WINDOW):i])
            after.update(verbs[i + 1:i + 1 + WINDOW])
    tb, ta = sum(before.values()), sum(after.values())
    return {
        "placebo_interrupts": n,
        "before": {a: before.get(a, 0) / tb if tb else 0.0 for a in ACTIVITIES},
        "after": {a: after.get(a, 0) / ta if ta else 0.0 for a in ACTIVITIES},
        "jsd_before_after": M.jsd(M.normalise(dict(before)), M.normalise(dict(after))) if tb and ta else None,
    }


def section_532(cells) -> dict:
    out = {"window": WINDOW, "activities": list(ACTIVITIES), "panels": {}, "per_profile": {}}
    for mech in SPANNING:
        for interval in INTERVALS:
            treat = _pool(cells, "core", FOUR, mech, interval)
            blind = _pool(cells, "blind", FOUR, mech, interval, overlay="verdict_blind")
            treat_none = _pool(cells, "core", FOUR, "none", 0)
            blind_none = _pool(cells, "blind", FOUR, "none", 0, overlay="verdict_blind")
            key = f"{mech}|{interval}"
            out["panels"][key] = {
                "mechanism": mech, "interval": interval,
                "treatment": mix_block(treat),
                "control": mix_block(blind),
                "placebo_treatment": placebo_block(treat, treat_none),
                "placebo_control": placebo_block(blind, blind_none),
                "hosts_treatment": _iv(hosts_of(treat)),
                "hosts_control": _iv(hosts_of(blind)),
                "interrupts_per_run_treatment": _iv([r["n_interrupted"] for r in treat]),
                "interrupts_per_run_control": _iv([r["n_interrupted"] for r in blind]),
                "executions_per_run": _iv([r["n_executed"] for r in treat]),
            }
            out["per_profile"][key] = {
                p: {"treatment": mix_block(_cell(cells, "core", "movement", p, mech, interval)),
                    "control": mix_block(_cell(cells, "blind", "movement", p, mech, interval,
                                               overlay="verdict_blind"))}
                for p in FOUR
            }
    # the unopposed contrast: does the blind arm differ from the treatment with no defence at all?
    out["unopposed"] = {
        "hosts_treatment": _iv(hosts_of(_pool(cells, "core", FOUR, "none", 0))),
        "hosts_control": _iv(hosts_of(_pool(cells, "blind", FOUR, "none", 0, overlay="verdict_blind"))),
    }
    return out


# --- §5.4.1 --------------------------------------------------------------------


def section_541(cells, rng) -> dict:
    out = {"conditions": list(DEFENDED), "profiles": list(PROFILES), "by_interval": {}}
    for interval in INTERVALS:
        block = {}
        for p in PROFILES:
            none = hosts_of(_cell(cells, "core", "movement", p, "none", 0))
            block[p] = {}
            for c in DEFENDED:
                runs = _cell(cells, "core", "movement", p, c, interval)
                block[p][c] = {
                    **suppression(none, hosts_of(runs), rng),
                    "delay": delay_summary(runs),
                    "blocked": _iv([r["blocked_fraction"] for r in runs if r["blocked_fraction"] is not None]),
                    "target_reach": float(np.mean([r["reached"] for r in runs])),
                    "interrupted_per_run": _iv([r["n_interrupted"] for r in runs]),
                }
            block[p]["none"] = {
                "delay": delay_summary(_cell(cells, "core", "movement", p, "none", 0)),
                "blocked": _iv([r["blocked_fraction"] for r in _cell(cells, "core", "movement", p, "none", 0)
                                if r["blocked_fraction"] is not None]),
                "hosts": _iv(none),
                "target_reach": float(np.mean([r["reached"] for r in _cell(cells, "core", "movement", p, "none", 0)])),
            }
        # the pooled model (the four profiles) for the table's rows
        none4 = hosts_of(_pool(cells, "core", FOUR, "none", 0))
        pooled = {}
        for c in DEFENDED:
            runs = _pool(cells, "core", FOUR, c, interval)
            pooled[c] = {
                **suppression(none4, hosts_of(runs), rng),
                "delay": delay_summary(runs),
                "blocked": _iv([r["blocked_fraction"] for r in runs if r["blocked_fraction"] is not None]),
                "target_reach": float(np.mean([r["reached"] for r in runs])),
            }
        pooled["none"] = {
            "delay": delay_summary(_pool(cells, "core", FOUR, "none", 0)),
            "blocked": _iv([r["blocked_fraction"] for r in _pool(cells, "core", FOUR, "none", 0)
                            if r["blocked_fraction"] is not None]),
            "hosts": _iv(none4),
        }
        # adjacency: conditions ordered by pooled suppression; overlapping neighbours flagged
        order = sorted(DEFENDED, key=lambda c: -pooled[c]["point"])
        overlaps = []
        for a, b in zip(order, order[1:]):
            if pooled[b]["hi"] >= pooled[a]["lo"]:
                overlaps.append([a, b])
        out["by_interval"][str(interval)] = {"per_profile": block, "pooled": pooled,
                                             "order_pooled": order, "overlapping_adjacent": overlaps}
    return out


# --- §5.4.2 --------------------------------------------------------------------


def arm_cells(cells, group, interval, objective="targeted", regime="shifted", none_group=None):
    """hosts arrays per condition for the two arms: movement = the four
    profiles pooled; baseline = the inherited attacker. The no-defence cell
    is regime-unread, so an arm group without one (the regime arm) borrows
    the core's (``none_group``)."""
    ng = none_group or group
    mv = {"none": hosts_of(_pool(cells, ng, FOUR, "none", 0, objective=objective))}
    bl = {"none": hosts_of(_cell(cells, ng, "baseline", "baseline", "none", 0, objective=objective))}
    for c in DEFENDED:
        mv[c] = hosts_of(_pool(cells, group, FOUR, c, interval, objective=objective, regime=regime))
        bl[c] = hosts_of(_cell(cells, group, "baseline", "baseline", c, interval, objective=objective, regime=regime))
    return {"movement": mv, "baseline": bl}


def rank_block(arms: dict, rng) -> dict:
    """Suppression per condition per arm, the two orderings, Spearman rho
    with a seed-bootstrap interval, and the family contrast (network-layer
    vs application-layer hosts) as Cliff's delta per arm."""
    sup = {arm: {c: suppression(h["none"], h[c], rng) for c in DEFENDED} for arm, h in arms.items()}
    pts = {arm: [sup[arm][c]["point"] for c in DEFENDED] for arm in arms}
    rho = float(spearmanr(pts["movement"], pts["baseline"]).statistic)
    boots = np.empty(N_BOOT // 2)
    for b in range(len(boots)):
        vec = {}
        for arm, h in arms.items():
            none = h["none"][rng.integers(0, len(h["none"]), len(h["none"]))].mean()
            vec[arm] = [1 - h[c][rng.integers(0, len(h[c]), len(h[c]))].mean() / none for c in DEFENDED]
        boots[b] = spearmanr(vec["movement"], vec["baseline"]).statistic
    lo, hi = np.quantile(boots, [0.025, 0.975])
    ranks = {arm: {c: int(r) for c, r in zip(DEFENDED, (-np.array(pts[arm])).argsort().argsort() + 1)}
             for arm in arms}
    top = {arm: max(DEFENDED, key=lambda c: sup[arm][c]["point"]) for arm in arms}
    family = {}
    for arm, h in arms.items():
        net = np.concatenate([h[c] for c in SINGLES if LAYER[c] == "network"])
        app = np.concatenate([h[c] for c in SINGLES if LAYER[c] == "application"])
        family[arm] = {
            "network_hosts": _iv(net), "application_hosts": _iv(app),
            "cliff_network_below_application": boot_cliff(net, app, rng),
            "suppression_network": float(1 - net.mean() / h["none"].mean()),
            "suppression_application": float(1 - app.mean() / h["none"].mean()),
        }
    return {"suppression": sup, "ranks": ranks, "top": top,
            "spearman": {"rho": rho, "lo": float(lo), "hi": float(hi), "n_boot": len(boots)},
            "share_of_bootstraps_negative": float(np.mean(boots < 0)),
            "family": family}


def section_542(cells, rng) -> dict:
    return {"conditions": list(DEFENDED),
            "by_interval": {str(i): rank_block(arm_cells(cells, "core", i), rng) for i in INTERVALS}}


# --- §5.4.3 --------------------------------------------------------------------


def _claim(sup, arm, a_set, b_set, rng_boots=None) -> dict:
    a = float(np.mean([sup[arm][c]["point"] for c in a_set]))
    b = float(np.mean([sup[arm][c]["point"] for c in b_set]))
    best_a = max(a_set, key=lambda c: sup[arm][c]["point"])
    best_b = max(b_set, key=lambda c: sup[arm][c]["point"])
    return {"mean_a": a, "mean_b": b, "best_a": best_a, "best_b": best_b,
            "best_a_sup": sup[arm][best_a], "best_b_sup": sup[arm][best_b],
            "best_intervals_overlap": bool(sup[arm][best_a]["lo"] <= sup[arm][best_b]["hi"]
                                           and sup[arm][best_b]["lo"] <= sup[arm][best_a]["hi"]),
            "direction": ("a > b" if a > b else "b > a")}


def section_543(cells, rng) -> dict:
    shuffle = [c for c in SINGLES if FAMILY[c] == "shuffle"]
    diversity = [c for c in SINGLES if FAMILY[c] == "diversity"]
    out = {"objective": "general", "by_interval": {}, "claims": {}}
    blocks = {i: rank_block(arm_cells(cells, "lineage", i, objective="general"), rng) for i in INTERVALS}
    out["by_interval"] = {str(i): b for i, b in blocks.items()}
    for arm in ("baseline", "movement"):
        out["claims"][arm] = {
            "zhang_shuffle_over_diversity_200": _claim(blocks[200]["suppression"], arm, shuffle, diversity),
            "brown_best_single_vs_best_scheme_200": _claim(blocks[200]["suppression"], arm, list(SINGLES), list(SCHEMES)),
            # Ho's headline is at interval 200 (ho2024.md "Headline findings":
            # diversity over shuffling by up to 140 %, OS Diversity against IP
            # Shuffle, hybrid metric), so the family claim and the named pair
            # are both read at 200 s; the 2 000 s reading is kept for the record
            "ho_diversity_over_shuffle_200": _claim(blocks[200]["suppression"], arm, diversity, shuffle),
            "ho_os_over_ip_200": _claim(blocks[200]["suppression"], arm, ["os_diversity"], ["ip_shuffle"]),
            "ho_diversity_over_shuffle_2000": _claim(blocks[2000]["suppression"], arm, diversity, shuffle),
        }
    # the lineage's own ending: how many runs hit the 80 % ratio (the general objective's criterion)
    out["ratio_reached"] = {
        "baseline_none": float(np.mean([r["reached"] for r in _cell(cells, "lineage", "baseline", "baseline", "none", 0, objective="general")])),
        "movement_none": float(np.mean([r["reached"] for r in _pool(cells, "lineage", FOUR, "none", 0, objective="general")])),
    }
    return out


# --- §5.5 ----------------------------------------------------------------------


def effort(runs) -> dict:
    hosts = sum(r["hosts"] for r in runs)
    acts = sum(r["n_actions"] for r in runs)
    succ = sum(r["n_success"] for r in runs)
    per_run_a = [r["n_actions"] / r["hosts"] for r in runs if r["hosts"]]
    per_run_s = [r["n_success"] / r["hosts"] for r in runs if r["hosts"]]
    # seeded bootstrap on the cell-total ratios (the record's form: cell
    # actions / cell hosts, so a one-host run does not dominate)
    rng = np.random.default_rng(RNG_SEED + 1)
    A = np.array([r["n_actions"] for r in runs], dtype=float)
    S = np.array([r["n_success"] for r in runs], dtype=float)
    H = np.array([r["hosts"] for r in runs], dtype=float)
    ba, bs = [], []
    for _ in range(N_BOOT // 2):
        idx = rng.integers(0, len(runs), len(runs))
        h = H[idx].sum()
        if h:
            ba.append(A[idx].sum() / h)
            bs.append(S[idx].sum() / h)
    return {
        "actions_per_host_celltotal": (acts / hosts if hosts else None),
        "actions_per_host_celltotal_ci": ([float(q) for q in np.quantile(ba, [0.025, 0.975])] if ba else None),
        "successes_per_host_celltotal": (succ / hosts if hosts else None),
        "successes_per_host_celltotal_ci": ([float(q) for q in np.quantile(bs, [0.025, 0.975])] if bs else None),
        "actions_per_host": _iv(per_run_a) if per_run_a else None,
        "successes_per_host": _iv(per_run_s) if per_run_s else None,
        "zero_host_runs": sum(1 for r in runs if not r["hosts"]),
        "occupancy": _iv([r["occupancy"] for r in runs]),
        "execs_per_ksec": _iv([r["execs_per_ksec"] for r in runs]),
        "suspended_per_run": _iv([r["n_suspended"] for r in runs]),
        "actions_per_run": _iv([r["n_actions"] for r in runs]),
    }


def time_split(runs) -> dict:
    """Mean per-run shares of elapsed time. The ledger's split is served dwell
    + derived MTD penalty + residual, and the residual is ~0 under S3-R (the
    token is always in a place), so "remainder" is structurally empty. The
    informative three-way split is therefore: dwell served on events that
    completed (activity), dwell served on events a mutation cut short (the
    ledger's re-work: ``time_interrupted_events`` less the penalty), and the
    penalty itself (imposed delay). Both splits are reported."""
    dw, pen, rem, done, cut = [], [], [], [], []
    for r in runs:
        e = r["elapsed"] or 1.0
        cut_dwell = max(0.0, r["time_interrupted_events"] - r["time_penalty"])
        dw.append(r["time_dwell"] / e)
        pen.append(r["time_penalty"] / e)
        rem.append(max(0.0, 1 - (r["time_dwell"] + r["time_penalty"]) / e))
        cut.append(cut_dwell / e)
        done.append(max(0.0, r["time_dwell"] - cut_dwell) / e)
    return {"activity": _iv(dw), "imposed_delay": _iv(pen), "remainder": _iv(rem),
            "activity_completed": _iv(done), "activity_cut_short": _iv(cut),
            "actions_per_run": _iv([r["n_actions"] for r in runs]),
            "interrupted_per_run": _iv([r["n_interrupted"] for r in runs])}


def section_55(cells, rng, s542: dict) -> dict:
    out = {"by_interval": {}}
    for interval in INTERVALS:
        sup = s542["by_interval"][str(interval)]["suppression"]
        block = {"frontier": {}, "cost": {}, "time_split": {}}
        for arm in ("movement", "baseline"):
            for c in ("none",) + DEFENDED:
                runs = (_pool(cells, "core", FOUR, c, interval) if arm == "movement"
                        else _cell(cells, "core", "baseline", "baseline", c, interval))
                block["cost"][f"{arm}|{c}"] = effort(runs)
                if c != "none":
                    block["frontier"][f"{arm}|{c}"] = {
                        "occupancy": block["cost"][f"{arm}|{c}"]["occupancy"],
                        "suppression": sup[arm][c],
                    }
        for c in ("none",) + DEFENDED:
            block["time_split"][c] = time_split(_pool(cells, "core", FOUR, c, interval))
        # spearman(occupancy, suppression) per arm — the frontier record's T3 criterion
        for arm in ("movement", "baseline"):
            occ = [block["frontier"][f"{arm}|{c}"]["occupancy"]["mean"] for c in DEFENDED]
            sp = [block["frontier"][f"{arm}|{c}"]["suppression"]["point"] for c in DEFENDED]
            block[f"spearman_occupancy_suppression_{arm}"] = float(spearmanr(occ, sp).statistic)
        out["by_interval"][str(interval)] = block
    return out


# --- the regime arm ------------------------------------------------------------


def section_regime(cells, rng, s542: dict) -> dict:
    core = s542["by_interval"]["200"]
    exp = rank_block(arm_cells(cells, "regime", 200, regime="exponential", none_group="core"), rng)
    delta = {arm: {c: exp["suppression"][arm][c]["point"] - core["suppression"][arm][c]["point"]
                   for c in DEFENDED} for arm in ("movement", "baseline")}
    execs = {arm: {c: {
        "core": _iv([r["n_executed"] for r in (_pool(cells, "core", FOUR, c, 200) if arm == "movement"
                                              else _cell(cells, "core", "baseline", "baseline", c, 200))]),
        "exponential": _iv([r["n_executed"] for r in (_pool(cells, "regime", FOUR, c, 200, regime="exponential") if arm == "movement"
                                                     else _cell(cells, "regime", "baseline", "baseline", c, 200, regime="exponential"))]),
        "suspended_exponential": _iv([r["n_suspended"] for r in (_pool(cells, "regime", FOUR, c, 200, regime="exponential") if arm == "movement"
                                                                else _cell(cells, "regime", "baseline", "baseline", c, 200, regime="exponential"))]),
    } for c in DEFENDED} for arm in ("movement", "baseline")}
    return {"regime": "exponential", "interval": 200, "rank_block": exp,
            "suppression_exponential_minus_core": delta, "executions": execs}


# --- previews ------------------------------------------------------------------


def previews(out: dict) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    COL = {"objective_exfiltration": "#1f548c", "objective_impact": "#b3261e",
           "objective_exfiltration_impact": "#a8741a", "objective_none_c2": "#6f4e9c",
           "aggregate": "#3a7d44", "baseline": "#7a7a7a"}
    acts = [a or "dwell" for a in ACTIVITIES]

    # Fig 5.4
    fig, axes = plt.subplots(2, 2, figsize=(12, 7), sharey=True)
    for ax, (key, p) in zip(axes.flat, out["s532"]["panels"].items()):
        x = np.arange(len(ACTIVITIES))
        w = 0.2
        t, c = p["treatment"], p["control"]
        ax.bar(x - 1.5 * w, [t["before"][a] for a in ACTIVITIES], w, color="#1f548c", alpha=0.45, label="model, before")
        ax.bar(x - 0.5 * w, [t["after"][a] for a in ACTIVITIES], w, color="#1f548c", label="model, after")
        ax.bar(x + 0.5 * w, [c["before"][a] for a in ACTIVITIES], w, color="#9a9a9a", alpha=0.45, label="blind, before")
        ax.bar(x + 1.5 * w, [c["after"][a] for a in ACTIVITIES], w, color="#9a9a9a", label="blind, after")
        ax.set_xticks(x)
        ax.set_xticklabels(acts, rotation=30, ha="right", fontsize=8)
        ax.set_title(f"{SHORT[p['mechanism']]} @ {p['interval']} s  (JSD model {t['jsd_before_after']:.3f}, blind {c['jsd_before_after']:.3f})", fontsize=9)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0, 0].legend(fontsize=7, frameon=False)
    axes[0, 0].set_ylabel("share of visits")
    fig.tight_layout()
    fig.savefig(HERE / "preview_fig54.png", dpi=140)
    plt.close(fig)

    # Fig 5.5
    fig, axes = plt.subplots(2, 2, figsize=(13, 7), sharey="row", gridspec_kw={"width_ratios": [7, 2]})
    for row, interval in enumerate(INTERVALS):
        blk = out["s541"]["by_interval"][str(interval)]["per_profile"]
        for col, conds in enumerate((SINGLES, SCHEMES)):
            ax = axes[row, col]
            x = np.arange(len(conds))
            w = 0.16
            for i, p in enumerate(PROFILES):
                vals = [blk[p][c]["point"] for c in conds]
                err = [[blk[p][c]["point"] - blk[p][c]["lo"] for c in conds],
                       [blk[p][c]["hi"] - blk[p][c]["point"] for c in conds]]
                ax.bar(x + (i - 2) * w, vals, w, yerr=err, color=COL[p], label=LABEL[p], error_kw={"lw": 0.6})
            ax.set_xticks(x)
            ax.set_xticklabels([SHORT[c] for c in conds])
            ax.axhline(0, color="black", lw=0.5)
            ax.set_title(f"{'singles' if col == 0 else 'schemes'} @ {interval} s", fontsize=9)
            ax.spines[["top", "right"]].set_visible(False)
        axes[row, 0].set_ylabel("suppression of hosts reached")
    axes[0, 0].legend(fontsize=7, frameon=False, ncol=3)
    fig.tight_layout()
    fig.savefig(HERE / "preview_fig55.png", dpi=140)
    plt.close(fig)

    # Fig 5.6
    fig, axes = plt.subplots(2, 2, figsize=(13, 7), sharey="row", gridspec_kw={"width_ratios": [7, 2]})
    for row, interval in enumerate(INTERVALS):
        sup = out["s542"]["by_interval"][str(interval)]["suppression"]
        for col, conds in enumerate((SINGLES, SCHEMES)):
            ax = axes[row, col]
            x = np.arange(len(conds))
            for i, arm in enumerate(("baseline", "movement")):
                vals = [sup[arm][c]["point"] for c in conds]
                err = [[sup[arm][c]["point"] - sup[arm][c]["lo"] for c in conds],
                       [sup[arm][c]["hi"] - sup[arm][c]["point"] for c in conds]]
                ax.bar(x + (i - 0.5) * 0.36, vals, 0.36, yerr=err, color="#7a7a7a" if arm == "baseline" else "#1f548c",
                       hatch="//" if arm == "baseline" else None, label=arm, error_kw={"lw": 0.6})
            ax.set_xticks(x)
            ax.set_xticklabels([SHORT[c] for c in conds])
            ax.axhline(0, color="black", lw=0.5)
            rho = out["s542"]["by_interval"][str(interval)]["spearman"]
            ax.set_title(f"{'singles' if col == 0 else 'schemes'} @ {interval} s   rho={rho['rho']:.2f} [{rho['lo']:.2f}, {rho['hi']:.2f}]", fontsize=9)
            ax.spines[["top", "right"]].set_visible(False)
        axes[row, 0].set_ylabel("suppression of hosts reached")
    axes[0, 0].legend(fontsize=8, frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / "preview_fig56.png", dpi=140)
    plt.close(fig)

    # Fig 5.7 + 5.8
    fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5))
    fr = out["s55"]["by_interval"]["200"]["frontier"]
    for arm, mk in (("baseline", "s"), ("movement", "o")):
        for c in DEFENDED:
            p = fr[f"{arm}|{c}"]
            a.errorbar(p["occupancy"]["mean"], p["suppression"]["point"],
                       yerr=[[p["suppression"]["point"] - p["suppression"]["lo"]], [p["suppression"]["hi"] - p["suppression"]["point"]]],
                       xerr=p["occupancy"]["ci95"], fmt=mk, color="#7a7a7a" if arm == "baseline" else "#1f548c", ms=6, lw=0.6)
            a.annotate(SHORT[c], (p["occupancy"]["mean"], p["suppression"]["point"]), fontsize=7, xytext=(3, 3), textcoords="offset points")
    a.set_xlabel("occupancy (share of run under reconfiguration)")
    a.set_ylabel("suppression")
    a.set_title("frontier @ 200 s (square = baseline, circle = movement)", fontsize=9)
    ts = out["s55"]["by_interval"]["200"]["time_split"]
    conds = ("none",) + DEFENDED
    x = np.arange(len(conds))
    act = np.array([ts[c]["activity"]["mean"] for c in conds])
    dl = np.array([ts[c]["imposed_delay"]["mean"] for c in conds])
    rm = np.array([ts[c]["remainder"]["mean"] for c in conds])
    b.bar(x, act, color="#1f548c", label="activity")
    b.bar(x, dl, bottom=act, color="#b3261e", label="imposed delay")
    b.bar(x, rm, bottom=act + dl, color="#c8c8c8", label="remainder")
    b.set_xticks(x)
    b.set_xticklabels([SHORT[c] for c in conds], rotation=30, ha="right")
    b.legend(fontsize=8, frameon=False)
    b.set_title("movement arm time split @ 200 s", fontsize=9)
    for ax in (a, b):
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(HERE / "preview_fig57_58.png", dpi=140)
    plt.close(fig)


# --- main ----------------------------------------------------------------------


def main() -> int:
    cells, errors = load()
    rng = np.random.default_rng(RNG_SEED)
    counts = {"|".join(str(x) for x in k): len(v) for k, v in sorted(cells.items())}
    baseline_blocked_ok = all(
        all(r["blocked_fraction"] == 0.0 for r in v) for k, v in cells.items() if k[1] == "baseline"
    )
    sanity = {
        "error_rows": len(errors),
        "cells": len(counts),
        "all_cells_100": all(v == 100 for v in counts.values()),
        "cells_not_100": {k: v for k, v in counts.items() if v != 100},
        "max_events_hit": sum(1 for k, v in cells.items() if k[1] == "movement"
                              for r in v if r["terminal"] == "max_events"),
        "baseline_blocked_structural_zero": baseline_blocked_ok,
        "baseline_uuid_vs_positional_hosts_differ": sum(
            1 for k, v in cells.items() if k[1] == "baseline" for r in v if r["hosts"] != r["hosts_positional"]),
        "interrupt_tally_mismatch_movement": sum(
            1 for k, v in cells.items() if k[1] == "movement" for r in v
            if r["n_interrupted"] != r["substrate_interrupted"]),
        "runs_per_cell": counts,
    }
    out = {"sanity": sanity}
    print(f"sanity: errors {sanity['error_rows']}, cells {sanity['cells']}, all at 100: {sanity['all_cells_100']}, "
          f"max_events {sanity['max_events_hit']}, baseline blocked zero: {baseline_blocked_ok}, "
          f"uuid/positional differ: {sanity['baseline_uuid_vs_positional_hosts_differ']}, "
          f"interrupt tally mismatches: {sanity['interrupt_tally_mismatch_movement']}")
    out["s532"] = section_532(cells)
    out["s541"] = section_541(cells, rng)
    out["s542"] = section_542(cells, rng)
    out["s543"] = section_543(cells, rng)
    out["s55"] = section_55(cells, rng, out["s542"])
    out["regime"] = section_regime(cells, rng, out["s542"])
    (HERE / "numbers.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    previews(out)

    # a short printed read
    for key, p in out["s532"]["panels"].items():
        t, c = p["treatment"], p["control"]
        print(f"\n§5.3.2 {key}: interrupts {t['interrupts']} (model) / {c['interrupts']} (blind); "
              f"JSD before→after model {t['jsd_before_after']:.4f}, blind {c['jsd_before_after']:.4f}, "
              f"placebo model {p['placebo_treatment']['jsd_before_after']}, hosts model {t and p['hosts_treatment']['mean']:.2f} blind {p['hosts_control']['mean']:.2f}")
        for a in ACTIVITIES:
            print(f"   {a or 'dwell':13s} model {t['before'][a]:.3f}→{t['after'][a]:.3f}   blind {c['before'][a]:.3f}→{c['after'][a]:.3f}"
                  f"   shift model {t['shift'].get(a, {}).get('mean', 0):+.3f}±{t['shift'].get(a, {}).get('ci95', 0):.3f}")
    for interval in INTERVALS:
        blk = out["s542"]["by_interval"][str(interval)]
        print(f"\n§5.4 @ {interval} s: rho {blk['spearman']['rho']:.3f} [{blk['spearman']['lo']:.3f}, {blk['spearman']['hi']:.3f}]; "
              f"top {blk['top']}; family δ movement {blk['family']['movement']['cliff_network_below_application']['delta']:.2f}, "
              f"baseline {blk['family']['baseline']['cliff_network_below_application']['delta']:.2f}")
        for c in DEFENDED:
            m, b = blk["suppression"]["movement"][c], blk["suppression"]["baseline"][c]
            print(f"   {SHORT[c]:12s} movement {m['point']:.3f} [{m['lo']:.3f},{m['hi']:.3f}] rank {blk['ranks']['movement'][c]}   "
                  f"baseline {b['point']:.3f} [{b['lo']:.3f},{b['hi']:.3f}] rank {blk['ranks']['baseline'][c]}")
    print("\n§5.4.3 claims:", json.dumps({a: {k: v["direction"] + (" (best intervals overlap)" if v["best_intervals_overlap"] else "")
                                             for k, v in cl.items()} for a, cl in out["s543"]["claims"].items()}, indent=1))
    print("\n§5.5 spearman(occupancy, suppression) @200:", out["s55"]["by_interval"]["200"]["spearman_occupancy_suppression_movement"],
          out["s55"]["by_interval"]["200"]["spearman_occupancy_suppression_baseline"])
    print("regime Δ suppression (exp − core) @200:", json.dumps(out["regime"]["suppression_exponential_minus_core"], indent=0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
