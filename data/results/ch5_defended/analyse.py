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
  shield   MTDShield's decisions and the training-input check
  sweep    NCR reduction against the six deployment intervals, per attacker,
           profile and layer
  ranking  §5.3.2's table: per interval and attacker, every ranked condition's
           metrics and its Scott-Knott ESD rank (sk_esd.py), and Spearman's
           rho between the two attackers' NCR reductions

    PYTHONPATH=src python data/results/ch5_defended/analyse.py

CORPUS=reported reads the reported corpus (runs_reported.jsonl: 1 000 seeds,
the vulnerability memory on; run_corpus.py REPORTED=1) and writes
numbers_reported.json with the sections §5.3's floats read: sanity, sweep,
sweep_asp and ranking. Its summaries keep only the fields those read, so the
cache stays small. RUNS=path and OUT=path override the two files (a pilot).
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from mtdsim.l3_simulation.movement import measures as M
from mtdsim.l3_simulation.movement.attacker import MovementRecord
from mtdsim.l3_simulation.movement.statistics import MovementRunResult, MTDExecution
from sk_esd import sk_esd

HERE = Path(__file__).resolve().parent
REPORTED = os.environ.get("CORPUS") == "reported"
RUNS = Path(os.environ["RUNS"]) if os.environ.get("RUNS") else HERE / ("runs_reported.jsonl" if REPORTED else "runs.jsonl")
NUMBERS = Path(os.environ["OUT"]) if os.environ.get("OUT") else HERE / ("numbers_reported.json" if REPORTED else "numbers.json")
CACHE = HERE / "summaries.pkl" if RUNS == HERE / "runs.jsonl" else RUNS.with_name(RUNS.stem + "_summaries.pkl")
# what the reported sections and the sanity block read of a run summary
LEAN = ("seed", "hosts", "hosts_positional", "reached_target", "target_time", "terminal",
        "blocked_fraction", "n_executed", "n_suspended", "n_interrupted", "substrate_interrupted")

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
# MTDShield and random over its four (2026-09-25, appended to the core group
# only), so the lineage and regime reads stay on the corpus's nine.
SHIELD = ("random_four", "mtdshield")
CORPUS9 = SINGLES + SCHEMES
DEFENDED = CORPUS9 + SHIELD
# the conditions the floats report and rank (Marc 2026-09-25: random over
# MTDShield's four is run but reported nowhere, so it takes no rank)
RANKED = tuple(c for c in DEFENDED if c != "random_four")
# the input-definition check: the same agent through Tay's training builder
SHIELD_CHECK = ("mtdshield_train",)
ACTION_NAME = {0: "no-op", 1: "complete_topology", 2: "ip_shuffle", 3: "os_diversity", 4: "service_diversity"}
SHORT = {
    "none": "none", "ip_shuffle": "IP", "complete_topology": "topology",
    "host_topology": "host", "port_shuffle": "port", "user_shuffle": "user",
    "os_diversity": "OS", "service_diversity": "service", "random": "random",
    "alternative": "alternative", "random_four": "random (four)", "mtdshield": "MTDShield",
    "mtdshield_train": "MTDShield (training inputs)",
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
# §5.2.2 (2026-09-22 redesign): the lifecycle stage of every tactic-place, from
# the ratified consensus artefact (chapter 4's four stages), and the offsets
# either side of a disruption the position read is taken at.
STAGE_OF = M.load_stage_of()
STAGES = (0, 1, 2, 3)
STAGE_NAME = {0: "preparation", 1: "intrusion", 2: "post-intrusion", 3: "objective"}
OFFSETS = tuple(range(-WINDOW, 0)) + tuple(range(1, WINDOW + 1))
# the baseline attacker's phases, for its like-for-like "what it does next" read
PHASES = ("SCAN_HOST", "ENUM_HOST", "SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE", "SCAN_NEIGHBOR")


def _censored(observed, censored) -> dict:
    """Summary of a censored-duration set: the mean over the durations that
    completed, with its interval, and the share that were cut off at the time
    limit (a censored recovery is the strongest non-recovery, never dropped)."""
    n = len(observed) + len(censored)
    return {
        "n": n, "observed": len(observed), "censored_share": (len(censored) / n) if n else None,
        "mean_observed": (_iv(observed) if observed else None),
        "median_observed": (float(np.median(observed)) if observed else None),
    }


def _around(seq, idx, key=lambda x: x) -> dict:
    """Counts of ``key(item)`` at each offset in OFFSETS around each index in
    ``idx`` (the disruption itself is offset 0 and belongs to no window)."""
    out = {o: Counter() for o in OFFSETS}
    n = len(seq)
    for i in idx:
        for o in OFFSETS:
            j = i + o
            if 0 <= j < n:
                out[o][key(seq[j])] += 1
    return {o: dict(c) for o, c in out.items()}


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
        # a target host compromised (ASP, section 4.5), read from the attacker's own
        # record as the baseline row's `hit` is: the end event also fires on the
        # inherited 80 % compromise-ratio stop, which is not a target reached; and
        # database_hosts_reached is read at the horizon, after later deployments
        # may have undone the hold, so it misses targets that were taken
        "reached_target": bool(run.reached_objective and run.first_database_reach_time is not None),
        # MTTC (section 4.5.2, ruling H1, 2026-09-30): the time a target host falls
        "target_time": (run.first_database_reach_time
                        if run.reached_objective and run.first_database_reach_time is not None else None),
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
        "decisions": _ledger(row),
        "mix": None,
        "interrupt_idx": [i for i, r in enumerate(visits) if r.interrupted],
    }
    if mix is not None:
        out["mix"] = {"n": mix.n_interrupts, "before": mix.before_verbs, "after": mix.after_verbs}
    if row["condition"] == "none":  # kept for the placebo null only
        out["visit_verbs"] = [r.verb for r in visits]
        out["visit_stages"] = [STAGE_OF[r.place] for r in visits]
    # §5.2.2 position and recovery reads (2026-09-22): where the token sits, by
    # lifecycle stage and by tactic, either side of each disruption; how many
    # of the visits after it are actions the substrate refuses; and how long
    # from the disruption to the next success and to the next compromise.
    idx = out["interrupt_idx"]
    out["stage_off"] = _around(visits, idx, key=lambda r: STAGE_OF[r.place])
    out["place_off"] = _around(visits, idx, key=lambda r: r.place)
    out["blocked_off"] = _around(visits, idx, key=lambda r: ("blocked" if r.blocked else
                                                          "action" if r.verb else "dwell"))
    out["place_counts"] = dict(Counter(r.place for r in visits))
    rec = M.recovery_times(run)
    out["rec_success"] = (list(rec.observed), list(rec.censored))
    obs, cen = [], []
    records = run.records
    for i, r in enumerate(records):
        if not r.interrupted:
            continue
        nxt = next((s for s in records[i + 1:] if M.is_compromise(s)), None)
        if nxt is None:
            cen.append(run.termination_time - r.end_time)
        else:
            obs.append(nxt.end_time - r.end_time)
    out["rec_comp"] = (obs, cen)
    out["comp_times"] = [r.end_time for r in records if M.is_compromise(r)]
    return out


def summarise_baseline(row: dict) -> dict:
    recs = row["records"]
    comps = [r for r in recs if r[3] is not None]
    targets = set(row["target_hosts"])
    hit = [r[2] for r in comps if r[3] in targets]
    execs = [MTDExecution(name=e[0], start_time=e[1], finish_time=e[2], duration=e[3], layer=e[4])
             for e in row["mtd_executions"]]
    dis = M.disruption_ledger(execs, elapsed=row["termination_time"], n_suspended=row["mtd_suspended"])
    # §5.2.2 (2026-09-22): the baseline attacker's own disruption reads, on its
    # phases. A record is [phase, start, end, compromised host or None, _, the
    # interrupting resource type or None]. Landing = the phase it restarts in.
    idx = [i for i, r in enumerate(recs) if r[5] is not None]
    landing = Counter()
    obs, cen = [], []
    for i in idx:
        nxt = recs[i + 1][0] if i + 1 < len(recs) else "END"
        landing[(recs[i][5], nxt)] += 1
        comp = next((r for r in recs[i + 1:] if r[3] is not None), None)
        if comp is None:
            cen.append(row["termination_time"] - recs[i][2])
        else:
            obs.append(comp[2] - recs[i][2])
    return {
        "landing": {f"{k[0]}|{k[1]}": v for k, v in landing.items()},
        "phase_off": _around(recs, idx, key=lambda r: r[0]),
        "rec_comp": (obs, cen),
        "comp_times": [r[2] for r in comps],
        "seed": row["seed"],
        "hosts": row["compromised_uuid"],
        "hosts_positional": row["compromised"],
        "reached": bool(row["reached_objective"]),
        "reached_target": bool(hit),
        "target_time": (min(hit) if hit else None),
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
        "decisions": _ledger(row),
    }


def _ledger(row: dict) -> dict | None:
    """MTDShield's per-decision ledger, reduced to counts per run."""
    led = row.get("mtd_decisions")
    if led is None:
        return None
    return {"n": len(led), "actions": dict(Counter(d[1] for d in led)),
            "sources": dict(Counter(d[2] for d in led)),
            "forced_actions": dict(Counter(d[1] for d in led if d[2] == "forced"))}


def load() -> tuple[dict, list]:
    """The per-run summaries, cached beside the corpus (``summaries.pkl``) and
    rebuilt whenever the corpus or this file is newer than the cache."""
    import pickle

    cache = CACHE
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
            if REPORTED:
                s = {k: s[k] for k in LEAN if k in s}
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


def success_of(runs) -> np.ndarray:
    """1 where the run compromises a target host (ASP's numerator), else 0."""
    return np.array([r["reached_target"] for r in runs], dtype=float)


# the per-run quantity each MTD effectiveness metric compares (section 4.5.3)
FIELD_OF = {"asp": success_of, "ncr": hosts_of}


def mttc_of(runs) -> dict | None:
    """MTTC (section 4.5.2): the mean time a target host falls, over the runs
    that take one; None where none does."""
    t = [r["target_time"] for r in runs if r["target_time"] is not None]
    return _iv(t) if t else None


def suppression(none_hosts: np.ndarray, cond_hosts: np.ndarray, rng: np.random.Generator) -> dict:
    """1 - mean(cond) / mean(none), with a seeded bootstrap interval on the
    ratio of means (unpaired: the two cells are resampled independently)."""
    point = 1.0 - cond_hosts.mean() / none_hosts.mean()
    boots = np.empty(N_BOOT)
    for b in range(N_BOOT):
        n = none_hosts[rng.integers(0, len(none_hosts), len(none_hosts))].mean()
        c = cond_hosts[rng.integers(0, len(cond_hosts), len(cond_hosts))].mean()
        boots[b] = 1.0 - c / n if n > 0 else np.nan
    # a resample whose no-MTD cell holds no success leaves the reduction undefined
    # (ASP on a single attack profile: 5 of 100 runs for c_3); such resamples are
    # dropped and counted, so the interval is conditional on a defined reduction
    undefined = float(np.mean(~np.isfinite(boots)))
    # a no-MTD cell with no success at all leaves every resample undefined (a
    # pilot of a few seeds); the interval is then undefined too
    lo, hi = (np.quantile(boots[np.isfinite(boots)], [0.025, 0.975]) if undefined < 1.0
              else (np.nan, np.nan))
    diff = M.mean_ci  # noqa: F841  (the absolute difference below uses the suite's interval)
    return {
        "point": float(point), "lo": float(lo), "hi": float(hi),
        "hosts_none": _iv(none_hosts), "hosts_cond": _iv(cond_hosts),
        "absolute_reduction": float(none_hosts.mean() - cond_hosts.mean()),
        "absolute_reduction_ci95": float(1.96 * np.sqrt(none_hosts.var(ddof=1) / len(none_hosts)
                                                        + cond_hosts.var(ddof=1) / len(cond_hosts))),
        "denied_share": float(np.mean(cond_hosts == 0)),
        "boot_undefined_share": undefined,
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


# --- §5.2.2 (2026-09-22 redesign: position and recovery, not the verb mix) -----


def _share_by_offset(runs, field, keys) -> dict:
    """Pooled share of each key at each offset around the disruptions."""
    tot = {o: Counter() for o in OFFSETS}
    for r in runs:
        for o, c in r[field].items():
            tot[o].update(c)
    out = {}
    for o in OFFSETS:
        n = sum(tot[o].values())
        out[str(o)] = {str(k): (tot[o].get(k, 0) / n if n else 0.0) for k in keys}
        out[str(o)]["n"] = n
    return out


def _before_after(runs, field, keys) -> dict:
    """Pooled before (offsets < 0) and after (offsets > 0) shares of each key,
    and the paired per-run share shift with its interval."""
    before, after = Counter(), Counter()
    shifts = {k: [] for k in keys}
    n_runs = 0
    for r in runs:
        b, a = Counter(), Counter()
        for o, c in r[field].items():
            (b if o < 0 else a).update(c)
        if not b or not a:
            continue
        n_runs += 1
        before.update(b)
        after.update(a)
        tb, ta = sum(b.values()), sum(a.values())
        for k in keys:
            shifts[k].append(a.get(k, 0) / ta - b.get(k, 0) / tb)
    tb, ta = sum(before.values()), sum(after.values())
    return {
        "runs": n_runs,
        "before": {str(k): before.get(k, 0) / tb if tb else 0.0 for k in keys},
        "after": {str(k): after.get(k, 0) / ta if ta else 0.0 for k in keys},
        "shift": {str(k): _iv(v) for k, v in shifts.items() if v},
        "jsd_before_after": (M.jsd(M.normalise({str(k): v for k, v in before.items()}),
                                   M.normalise({str(k): v for k, v in after.items()})) if tb and ta else None),
    }


def _pool_durations(runs, field) -> dict:
    obs, cen = [], []
    for r in runs:
        o, c = r[field]
        obs += o
        cen += c
    return _censored(obs, cen)


def movement_disruption_block(runs, none_runs) -> dict:
    """The movement attacker's response to disruption, read on the tactic-level
    record: where the token sits by stage and by tactic either side of each
    disruption, what share of the visits after it are refused actions, and how
    long to the next success and the next compromise. ``none_runs`` gives the
    whole-run tactic distribution the defended one is compared with."""
    if not runs:
        return {"runs": 0}
    places = sorted(set(STAGE_OF))
    with_int = [r for r in runs if r["interrupt_idx"]]
    dist_def = Counter()
    dist_none = Counter()
    for r in runs:
        dist_def.update(r["place_counts"])
    for r in none_runs:
        dist_none.update(r["place_counts"])
    return {
        "runs": len(runs), "runs_with_interrupt": len(with_int),
        "interrupts": sum(len(r["interrupt_idx"]) for r in runs),
        "interrupts_per_run": _iv([len(r["interrupt_idx"]) for r in runs]),
        "stage_by_offset": _share_by_offset(with_int, "stage_off", STAGES),
        "stage": _before_after(with_int, "stage_off", STAGES),
        "tactic": _before_after(with_int, "place_off", places),
        "refused_by_offset": _share_by_offset(with_int, "blocked_off", ("blocked", "action", "dwell")),
        "recovery_to_success": _pool_durations(with_int, "rec_success"),
        "recovery_to_compromise": _pool_durations(with_int, "rec_comp"),
        "hosts": _iv(hosts_of(runs)),
        "whole_run_tactic_jsd_vs_none": (M.jsd(M.normalise(dict(dist_def)), M.normalise(dict(dist_none)))
                                         if dist_def and dist_none else None),
        "whole_run_tactic_share": {p: dist_def.get(p, 0) / sum(dist_def.values()) for p in places} if dist_def else {},
        "whole_run_tactic_share_none": {p: dist_none.get(p, 0) / sum(dist_none.values()) for p in places} if dist_none else {},
    }


def placebo_stage_block(defended, unopposed) -> dict:
    """The placebo null at stage level: each defended run's disruption
    positions applied to the same seed's unopposed run."""
    by_seed = {r["seed"]: r for r in unopposed}
    fake = []
    for d in defended:
        u = by_seed.get(d["seed"])
        if u is None or not d["interrupt_idx"]:
            continue
        stages = u["visit_stages"]
        idx = [i for i in d["interrupt_idx"] if i < len(stages)]
        fake.append({"stage_off": _around(stages, idx)})
    return _before_after(fake, "stage_off", STAGES)


def baseline_disruption_block(runs) -> dict:
    """The baseline attacker's response, on its phases: where it restarts after
    each disruption (by the interrupting resource), its phase mix either side,
    and the time to its next compromise."""
    if not runs:
        return {"runs": 0}
    landing = Counter()
    for r in runs:
        landing.update(r["landing"])
    by_res = defaultdict(Counter)
    for k, v in landing.items():
        res, nxt = k.split("|")
        by_res[res][nxt] += v
    return {
        "runs": len(runs),
        "interrupts": sum(len(r["rec_comp"][0]) + len(r["rec_comp"][1]) for r in runs),
        "landing": {res: {nxt: v / sum(c.values()) for nxt, v in c.items()} for res, c in by_res.items()},
        "phase": _before_after(runs, "phase_off", PHASES),
        "phase_by_offset": _share_by_offset(runs, "phase_off", PHASES),
        "recovery_to_compromise": _pool_durations(runs, "rec_comp"),
        "hosts": _iv(hosts_of(runs)),
    }


def _gap_block(runs) -> dict:
    """The pace anchor for the recovery read: the gap between consecutive
    compromises in these runs (observed gaps only, pooled over runs), and the
    share of runs with fewer than two compromises (no gap to read)."""
    gaps = []
    lt2 = 0
    for r in runs:
        t = sorted(r["comp_times"])
        if len(t) < 2:
            lt2 += 1
            continue
        gaps += [b - a for a, b in zip(t, t[1:])]
    return {"runs": len(runs), "runs_without_gap_share": lt2 / len(runs) if runs else None,
            "n_gaps": len(gaps), "mean": (_iv(gaps) if gaps else None),
            "median": (float(np.median(gaps)) if gaps else None)}


def recovery_ratio(runs, none_runs, rng, n_boot: int = N_BOOT) -> dict:
    """Panel (b)'s ratio: mean recovery to the next compromise (over the
    recoveries that completed, pooled over the runs' disruptions) divided by
    the same attacker's mean gap between consecutive compromises with no
    defence (pooled over the unopposed runs), with a seeded bootstrap interval
    on the ratio: both pools are resampled by run, independently."""
    rec = [r["rec_comp"][0] for r in runs if r["rec_comp"][0]]
    gaps = []
    for r in none_runs:
        t = sorted(r["comp_times"])
        gaps.append([b - a for a, b in zip(t, t[1:])])
    gaps = [g for g in gaps if g]
    if not rec or not gaps:
        return {"point": None}
    def mean_of(pools, idx):
        tot = 0.0
        n = 0
        for i in idx:
            tot += sum(pools[i])
            n += len(pools[i])
        return tot / n
    point = mean_of(rec, range(len(rec))) / mean_of(gaps, range(len(gaps)))
    boots = np.empty(n_boot)
    for k in range(n_boot):
        ir = rng.integers(0, len(rec), len(rec))
        ig = rng.integers(0, len(gaps), len(gaps))
        boots[k] = mean_of(rec, ir) / mean_of(gaps, ig)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"point": float(point), "lo": float(lo), "hi": float(hi), "n_boot": n_boot,
            "runs_with_recovery": len(rec), "unopposed_runs_with_gap": len(gaps)}


def section_522(cells, rng=None) -> dict:
    rng = rng or np.random.default_rng(RNG_SEED)
    out = {"window": WINDOW, "stages": {str(k): v for k, v in STAGE_NAME.items()}, "stage_of": STAGE_OF,
           "offsets": list(OFFSETS), "conditions": {}, "layers": {}}
    none_mov = _pool(cells, "core", FOUR, "none", 0)
    none_blind = _pool(cells, "blind", FOUR, "none", 0, overlay="verdict_blind")
    out["unopposed_gap"] = {"movement": _gap_block(none_mov),
                            "baseline": _gap_block(_cell(cells, "core", "baseline", "baseline", "none", 0))}
    for interval in INTERVALS:
        by_layer = defaultdict(lambda: {"movement": [], "baseline": []})
        for cond in DEFENDED:
            mov = _pool(cells, "core", FOUR, cond, interval)
            base = _cell(cells, "core", "baseline", "baseline", cond, interval)
            blind = (_pool(cells, "blind", FOUR, cond, interval, overlay="verdict_blind")
                     if cond in SPANNING else [])
            none_base = _cell(cells, "core", "baseline", "baseline", "none", 0)
            blk = {
                "condition": cond, "interval": interval, "layer": LAYER.get(cond, "mixed"),
                "movement": movement_disruption_block(mov, none_mov),
                "placebo": placebo_stage_block(mov, none_mov),
                "baseline": baseline_disruption_block(base),
                "recovery_ratio": {"movement": recovery_ratio(mov, none_mov, rng),
                                   "baseline": recovery_ratio(base, none_base, rng)},
            }
            if blind:
                blk["control"] = movement_disruption_block(blind, none_blind)
            out["conditions"][f"{cond}|{interval}"] = blk
            if cond in LAYER:
                by_layer[LAYER[cond]]["movement"] += mov
                by_layer[LAYER[cond]]["baseline"] += base
        for layer, d in by_layer.items():
            out["layers"][f"{layer}|{interval}"] = {
                "layer": layer, "interval": interval,
                "conditions": [c for c in SINGLES if LAYER[c] == layer],
                "movement": movement_disruption_block(d["movement"], none_mov),
                "baseline": baseline_disruption_block(d["baseline"]),
                "recovery_ratio": {"movement": recovery_ratio(d["movement"], none_mov, rng),
                                   "baseline": recovery_ratio(d["baseline"],
                                                              _cell(cells, "core", "baseline", "baseline", "none", 0), rng)},
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
                    "target_reach": float(np.mean([r["reached_target"] for r in runs])),
                    "interrupted_per_run": _iv([r["n_interrupted"] for r in runs]),
                }
            block[p]["none"] = {
                "delay": delay_summary(_cell(cells, "core", "movement", p, "none", 0)),
                "blocked": _iv([r["blocked_fraction"] for r in _cell(cells, "core", "movement", p, "none", 0)
                                if r["blocked_fraction"] is not None]),
                "hosts": _iv(none),
                "target_reach": float(np.mean([r["reached_target"] for r in _cell(cells, "core", "movement", p, "none", 0)])),
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
                "target_reach": float(np.mean([r["reached_target"] for r in runs])),
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


def arm_cells(cells, group, interval, objective="targeted", regime="shifted", none_group=None,
              conds=DEFENDED, of=hosts_of):
    """hosts arrays per condition for the two arms: movement = the four
    profiles pooled; baseline = the inherited attacker. The no-defence cell
    is regime-unread, so an arm group without one (the regime arm) borrows
    the core's (``none_group``)."""
    ng = none_group or group
    mv = {"none": of(_pool(cells, ng, FOUR, "none", 0, objective=objective))}
    bl = {"none": of(_cell(cells, ng, "baseline", "baseline", "none", 0, objective=objective))}
    for c in conds:
        mv[c] = of(_pool(cells, group, FOUR, c, interval, objective=objective, regime=regime))
        bl[c] = of(_cell(cells, group, "baseline", "baseline", c, interval, objective=objective, regime=regime))
    return {"movement": mv, "baseline": bl}


def rank_block(arms: dict, rng) -> dict:
    """Suppression per condition per arm, the two orderings, Spearman rho
    with a seed-bootstrap interval, and the family contrast (network-layer
    vs application-layer hosts) as Cliff's delta per arm."""
    conds = [c for c in arms["movement"] if c != "none"]
    sup = {arm: {c: suppression(h["none"], h[c], rng) for c in conds} for arm, h in arms.items()}
    pts = {arm: [sup[arm][c]["point"] for c in conds] for arm in arms}
    rho = float(spearmanr(pts["movement"], pts["baseline"]).statistic)
    boots = np.empty(N_BOOT // 2)
    for b in range(len(boots)):
        vec = {}
        for arm, h in arms.items():
            none = h["none"][rng.integers(0, len(h["none"]), len(h["none"]))].mean()
            vec[arm] = [1 - h[c][rng.integers(0, len(h[c]), len(h[c]))].mean() / none for c in conds]
        boots[b] = spearmanr(vec["movement"], vec["baseline"]).statistic
    lo, hi = np.quantile(boots, [0.025, 0.975])
    ranks = {arm: {c: int(r) for c, r in zip(conds, (-np.array(pts[arm])).argsort().argsort() + 1)}
             for arm in arms}
    top = {arm: max(conds, key=lambda c: sup[arm][c]["point"]) for arm in arms}
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
    blocks = {i: rank_block(arm_cells(cells, "lineage", i, objective="general", conds=CORPUS9), rng)
              for i in INTERVALS}
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


# --- MTDShield (2026-09-25) ------------------------------------------------------


def _ledger_block(runs) -> dict:
    led = [r["decisions"] for r in runs if r.get("decisions")]
    n = sum(d["n"] for d in led)
    acts, srcs, forced = Counter(), Counter(), Counter()
    for d in led:
        acts.update({int(k): v for k, v in d["actions"].items()})
        srcs.update(d["sources"])
        forced.update({int(k): v for k, v in d["forced_actions"].items()})
    return {
        "runs": len(led), "decisions": n,
        "decisions_per_run": _iv([d["n"] for d in led]) if led else None,
        "action_share": {ACTION_NAME[a]: acts.get(a, 0) / n if n else None for a in ACTION_NAME},
        "source_share": {k: v / n for k, v in srcs.items()} if n else {},
        "forced_share": (srcs.get("forced", 0) / n) if n else None,
        "forced_action_share": {ACTION_NAME[a]: v / sum(forced.values()) for a, v in forced.items()} if forced else {},
        "executions_per_run": _iv([r["n_executed"] for r in runs]),
    }


def section_shield(cells, rng) -> dict:
    """What the agent chose (the ledger), per arm and interval, and the input
    check: the same agent through Tay's training builder."""
    out = {"conditions": list(SHIELD), "check": list(SHIELD_CHECK), "by_interval": {}}
    for interval in INTERVALS:
        blk = {"ledger": {}, "check": {}}
        for c in ("mtdshield",) + SHIELD_CHECK:
            blk["ledger"][c] = {
                "baseline": _ledger_block(_cell(cells, "core", "baseline", "baseline", c, interval)),
                "movement": _ledger_block(_pool(cells, "core", FOUR, c, interval)),
                **{p: _ledger_block(_cell(cells, "core", "movement", p, c, interval)) for p in PROFILES},
            }
        arms = arm_cells(cells, "core", interval, conds=("mtdshield",) + SHIELD_CHECK)
        for arm, h in arms.items():
            blk["check"][arm] = {c: suppression(h["none"], h[c], rng) for c in ("mtdshield",) + SHIELD_CHECK}
            blk["check"][arm]["n"] = {c: int(len(h[c])) for c in ("mtdshield",) + SHIELD_CHECK}
        out["by_interval"][str(interval)] = blk
    return out


# --- the interval sweep (E6; §5.3.2-§5.3.3 line charts, 2026-09-25) -----------

# Table 2.4's words for the layer each single rewrites (LAYER above keeps the
# corpus's older keys).
LAYER_WORD = {"network": "host", "application": "service", "reserve": "credentials"}


def sweep_intervals(cells) -> list[int]:
    """Every deployment interval the core group has a defended cell at, so the
    sweep reads whatever the corpus holds (two levels before the sweep, six after)."""
    return sorted({k[5] for k in cells if k[0] == "core" and k[4] in DEFENDED and k[5]})


def section_sweep(cells, rng, metric: str = "asp") -> dict:
    """NCR reduction against the deployment interval for every condition: per
    attacker (the model = the four profiles pooled), per profile, and per layer
    (the mean of the layer's mechanisms each deployed alone, i.e. 1 - pooled
    NCR / no-defence NCR over their runs); ranks per attacker; executions and
    suspensions per run."""
    ivs = sweep_intervals(cells)
    out = {"intervals": ivs, "conditions": list(DEFENDED), "profiles": list(PROFILES),
           "layers": {w: [c for c in SINGLES if LAYER_WORD[LAYER[c]] == w] for w in LAYER_WORD.values()},
           "by_interval": {}}
    of = FIELD_OF[metric]
    out["metric"] = f"{metric} reduction"
    none_p = {p: of(_cell(cells, "core", "movement", p, "none", 0)) for p in PROFILES}
    for i in ivs:
        present = [c for c in DEFENDED if _cell(cells, "core", "baseline", "baseline", c, i)]
        arms = arm_cells(cells, "core", i, conds=present, of=of)
        blk = {"conditions": present, "attacker": {}, "profile": {}, "layer": {}, "ranks": {},
               "executions": {}, "suspended": {}}
        for arm, h in arms.items():
            blk["attacker"][arm] = {c: suppression(h["none"], h[c], rng) for c in present}
            pts = [blk["attacker"][arm][c]["point"] for c in present]
            blk["ranks"][arm] = {c: int(r) for c, r in zip(present, (-np.array(pts)).argsort().argsort() + 1)}
            blk["layer"][arm] = {w: suppression(h["none"], np.concatenate([h[c] for c in cs]), rng)
                                 for w, cs in out["layers"].items() if all(c in present for c in cs)}
        for p in PROFILES:
            blk["profile"][p] = {c: suppression(none_p[p], of(_cell(cells, "core", "movement", p, c, i)), rng)
                                 for c in present}
        for c in present:
            mv, bl = _pool(cells, "core", FOUR, c, i), _cell(cells, "core", "baseline", "baseline", c, i)
            blk["executions"][c] = {"movement": _iv([r["n_executed"] for r in mv]),
                                    "baseline": _iv([r["n_executed"] for r in bl])}
            blk["suspended"][c] = {"movement": _iv([r.get("n_suspended", 0) for r in mv]),
                                   "baseline": _iv([r.get("n_suspended", 0) for r in bl])}
        out["by_interval"][str(i)] = blk
    return out


def per_seed(runs, field: str = "hosts") -> np.ndarray:
    """The mean of ``field`` per seed, in seed order. Every condition and
    attacker runs on the same seeds, and the seed fixes the network, so the
    seed is the independent unit; the APT attacker model's four profiles at one
    seed are averaged into one value (sceptical examiner, 2026-09-25: the four
    are clustered, intraclass correlation up to 0.29)."""
    by = defaultdict(list)
    for r in runs:
        by[r["seed"]].append(float(r[field]))
    return np.array([np.mean(by[k]) for k in sorted(by)], dtype=float)


def per_seed_hosts(runs) -> np.ndarray:
    return per_seed(runs, "hosts")


def _reduction(none_seed: np.ndarray, cond_seed: np.ndarray, idx=None) -> float:
    n = none_seed if idx is None else none_seed[idx]
    c = cond_seed if idx is None else cond_seed[idx]
    return float(1.0 - c.mean() / n.mean()) if n.mean() > 0 else float("nan")


def section_ranking(cells, rng) -> dict:
    """Section 5.3.2's table (Marc 2026-09-25; NCR reduction the headline, ASP
    reduction beside it, 2026-09-30): per deployment interval and attacker,
    the ranked MTD's attack outcome (ASP, NCR, MTTC at a target host) and its
    NCR and ASP reductions with bootstrap intervals, the no-MTD row, and the
    Scott-Knott ESD rank on the mean hosts compromised per seed (within one
    attacker every MTD shares the no-MTD NCR, so the order of NCR reduction is
    the order of that mean; 100 seeds per MTD for both attackers). Spearman's
    rho between the two attackers' NCR reductions, with a
    95 % interval from resampling seeds (the same seeds run every MTD and both
    attackers, so one resample serves all)."""
    out = {"conditions": list(RANKED), "intervals": sweep_intervals(cells), "by_interval": {},
           "headline": "ncr reduction"}
    get = {"movement": lambda c, i: _pool(cells, "core", FOUR, c, i),
           "baseline": lambda c, i: _cell(cells, "core", "baseline", "baseline", c, i)}
    none = {arm: get[arm]("none", 0) for arm in get}
    none_seed = {arm: per_seed(none[arm], "hosts") for arm in get}
    for i in out["intervals"]:
        blk = {}
        seed_succ = {}
        for arm in get:
            runs = {c: get[arm](c, i) for c in RANKED}
            nh, ns = hosts_of(none[arm]), success_of(none[arm])
            rows = {}
            for c in RANKED:
                r = runs[c]
                rows[c] = {
                    "asp": float(success_of(r).mean()),
                    "asp_reduction": suppression(ns, success_of(r), rng),
                    "hosts": _iv(hosts_of(r)),
                    "ncr_reduction": suppression(nh, hosts_of(r), rng),
                    "mttc": mttc_of(r),
                    "blocked": (_iv([x["blocked_fraction"] for x in r if x["blocked_fraction"] is not None])
                                if arm == "movement" else None),
                }
            seed_succ[arm] = {c: per_seed(runs[c], "hosts") for c in RANKED}
            sk = sk_esd(seed_succ[arm], best="low")  # rank 1 = the fewest hosts compromised
            for c in RANKED:
                rows[c]["rank"] = sk["rank"][c]
            blk[arm] = {
                "rows": rows,
                "none": {"hosts": _iv(nh), "asp": float(ns.mean()), "mttc": mttc_of(none[arm]),
                         "blocked": (_iv([x["blocked_fraction"] for x in none[arm] if x["blocked_fraction"] is not None])
                                     if arm == "movement" else None)},
                "sk_esd": {k: v for k, v in sk.items() if k != "rank"},
            }
        pts = {arm: [_reduction(none_seed[arm], seed_succ[arm][c]) for c in RANKED] for arm in get}
        rho = float(spearmanr(pts["movement"], pts["baseline"]).statistic)
        n_seeds = len(none_seed["movement"])
        boots = []
        for _ in range(N_BOOT):
            idx = rng.integers(0, n_seeds, n_seeds)
            v = {arm: [_reduction(none_seed[arm], seed_succ[arm][c], idx) for c in RANKED] for arm in get}
            r_ = spearmanr(v["movement"], v["baseline"]).statistic
            if np.isfinite(r_):
                boots.append(r_)
        lo, hi = np.quantile(boots, [0.025, 0.975])
        blk["spearman_ncr_reduction"] = {"rho": rho, "lo": float(lo), "hi": float(hi), "n_boot": len(boots)}
        blk["spearman_sk_ranks"] = float(spearmanr([blk["movement"]["rows"][c]["rank"] for c in RANKED],
                                                   [blk["baseline"]["rows"][c]["rank"] for c in RANKED]).statistic)
        out["by_interval"][str(i)] = blk
    return out


# --- the regime arm ------------------------------------------------------------


def section_regime(cells, rng, s542: dict) -> dict:
    core = s542["by_interval"]["200"]
    exp = rank_block(arm_cells(cells, "regime", 200, regime="exponential", none_group="core",
                               conds=CORPUS9), rng)
    delta = {arm: {c: exp["suppression"][arm][c]["point"] - core["suppression"][arm][c]["point"]
                   for c in CORPUS9} for arm in ("movement", "baseline")}
    execs = {arm: {c: {
        "core": _iv([r["n_executed"] for r in (_pool(cells, "core", FOUR, c, 200) if arm == "movement"
                                              else _cell(cells, "core", "baseline", "baseline", c, 200))]),
        "exponential": _iv([r["n_executed"] for r in (_pool(cells, "regime", FOUR, c, 200, regime="exponential") if arm == "movement"
                                                     else _cell(cells, "regime", "baseline", "baseline", c, 200, regime="exponential"))]),
        "suspended_exponential": _iv([r["n_suspended"] for r in (_pool(cells, "regime", FOUR, c, 200, regime="exponential") if arm == "movement"
                                                                else _cell(cells, "regime", "baseline", "baseline", c, 200, regime="exponential"))]),
    } for c in CORPUS9} for arm in ("movement", "baseline")}
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

    # §5.2.2 redesign preview: (a) stage share by offset per layer, (b) refused
    # share by offset per layer, (c) recovery to next compromise, both attackers
    s = out["s522"]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    LC = {"network": "#1f548c", "application": "#b3261e", "reserve": "#a8741a"}
    for row, interval in enumerate(INTERVALS):
        ax = axes[row, 0]
        for layer, col in LC.items():
            m = s["layers"][f"{layer}|{interval}"]["movement"]
            for st, ls in zip(STAGES, (":", "-.", "-", "--")):
                ax.plot(OFFSETS, [m["stage_by_offset"][str(o)][str(st)] for o in OFFSETS], ls, color=col,
                        label=f"{layer} / {STAGE_NAME[st]}" if row == 0 else None)
        ax.axvline(0, color="k", lw=0.5)
        ax.set_title(f"stage share by offset @ {interval} s", fontsize=9)
        ax.set_xlabel("visits from the disruption")
        if row == 0:
            ax.legend(fontsize=6, frameon=False, ncol=3)
        ax = axes[row, 1]
        for layer, col in LC.items():
            m = s["layers"][f"{layer}|{interval}"]["movement"]
            ax.plot(OFFSETS, [m["refused_by_offset"][str(o)]["blocked"] for o in OFFSETS], "-o", color=col, ms=3, label=layer)
        for key, c in s["conditions"].items():
            if "control" in c and c["interval"] == interval:
                ax.plot(OFFSETS, [c["control"]["refused_by_offset"][str(o)]["blocked"] for o in OFFSETS], "--", color="#9a9a9a",
                        label=f"control {SHORT[c['condition']]}")
        ax.axvline(0, color="k", lw=0.5)
        ax.set_title(f"refused-action share by offset @ {interval} s", fontsize=9)
        ax.set_xlabel("visits from the disruption")
        ax.legend(fontsize=7, frameon=False)
        ax = axes[row, 2]
        xs = np.arange(3)
        for j, arm in enumerate(("movement", "baseline")):
            vals, cens = [], []
            for layer in LC:
                rc = s["layers"][f"{layer}|{interval}"][arm]["recovery_to_compromise"]
                vals.append(rc["mean_observed"]["mean"] if rc["mean_observed"] else 0)
                cens.append(rc["censored_share"] or 0)
            ax.bar(xs + (j - 0.5) * 0.35, vals, 0.35, color=("#1f548c" if arm == "movement" else "#9a9a9a"), label=arm)
            for x, v, cn in zip(xs + (j - 0.5) * 0.35, vals, cens):
                ax.text(x, v, f"cens {cn:.2f}", ha="center", va="bottom", fontsize=6)
        ax.set_xticks(xs)
        ax.set_xticklabels(list(LC))
        ax.set_title(f"time to next compromise after a disruption @ {interval} s", fontsize=9)
        ax.legend(fontsize=7, frameon=False)
    fig.tight_layout()
    fig.savefig(HERE / "preview_fig522.png", dpi=140)
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
    # The input check (Tay's training builder, verbatim) may die on a run; its
    # dead cells are counted apart so they are reported, not drawn from.
    check = lambda k: k.split("|")[4] in SHIELD_CHECK  # noqa: E731
    n_seeds = len({r["seed"] for v in cells.values() for r in v})
    sanity = {
        "seeds": n_seeds,
        "all_cells_full": all(v == n_seeds for k, v in counts.items() if not check(k)),
        "error_rows": sum(1 for e in errors if e["condition"] not in SHIELD_CHECK),
        "check_error_rows": sum(1 for e in errors if e["condition"] in SHIELD_CHECK),
        "check_errors": dict(Counter(f"{e['arm']}|{e['profile']}|{e['interval']}|{e['error'][:80]}"
                                     for e in errors if e["condition"] in SHIELD_CHECK)),
        "cells": len(counts),
        "all_cells_100": all(v == 100 for k, v in counts.items() if not check(k)),
        "cells_not_full": {k: v for k, v in counts.items() if v != n_seeds},
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
    print(f"sanity: errors {sanity['error_rows']}, cells {sanity['cells']}, seeds {n_seeds}, "
          f"all at {n_seeds}: {sanity['all_cells_full']}, "
          f"max_events {sanity['max_events_hit']}, baseline blocked zero: {baseline_blocked_ok}, "
          f"uuid/positional differ: {sanity['baseline_uuid_vs_positional_hosts_differ']}, "
          f"interrupt tally mismatches: {sanity['interrupt_tally_mismatch_movement']}")
    if REPORTED:
        # §5.3's floats only; the NCR sweep first, as below
        out["sweep"] = section_sweep(cells, rng, "ncr")
        out["sweep_asp"] = section_sweep(cells, rng, "asp")
        out["ranking"] = section_ranking(cells, rng)
        NUMBERS.write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
        print(f"wrote {NUMBERS}")
        return 0
    out["s532"] = section_532(cells)
    out["s522"] = section_522(cells, rng)
    out["s541"] = section_541(cells, rng)
    out["s542"] = section_542(cells, rng)
    out["s543"] = section_543(cells, rng)
    out["s55"] = section_55(cells, rng, out["s542"])
    out["regime"] = section_regime(cells, rng, out["s542"])
    out["shield"] = section_shield(cells, rng)
    # NCR reduction is the headline (Marc 2026-09-30, second read: the ASP version
    # "is just a colourful mess"); run first so its bootstrap stream is the one the
    # NCR prose was verified on. ASP reduction kept beside it for the record.
    out["sweep"] = section_sweep(cells, rng, "ncr")
    out["sweep_asp"] = section_sweep(cells, rng, "asp")
    out["ranking"] = section_ranking(cells, rng)
    NUMBERS.write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    previews(out)

    # a short printed read
    for key, L in out["s522"]["layers"].items():
        m, b = L["movement"], L["baseline"]
        rs, rc, bc = m["recovery_to_success"], m["recovery_to_compromise"], b["recovery_to_compromise"]
        print(f"\n§5.2.2 {key}: movement interrupts {m['interrupts']} ({m['interrupts_per_run']['mean']:.1f}/run), "
              f"stage JSD before→after {m['stage']['jsd_before_after']:.4f}, tactic JSD {m['tactic']['jsd_before_after']:.4f}, "
              f"whole-run tactic JSD vs none {m['whole_run_tactic_jsd_vs_none']:.4f}")
        for s in STAGES:
            sh = m["stage"]["shift"][str(s)]
            print(f"   stage {STAGE_NAME[s]:14s} {m['stage']['before'][str(s)]:.3f}→{m['stage']['after'][str(s)]:.3f}  shift {sh['mean']:+.3f}±{sh['ci95']:.3f}")
        print("   refused share by offset:", " ".join(f"{o:+d}:{m['refused_by_offset'][str(o)]['blocked']:.2f}" for o in OFFSETS))
        print(f"   recovery→success: n {rs['n']} censored {rs['censored_share']:.3f} mean {rs['mean_observed']['mean'] if rs['mean_observed'] else None}"
              f"  →compromise: n {rc['n']} censored {rc['censored_share']:.3f} mean {rc['mean_observed']['mean'] if rc['mean_observed'] else None}")
        print(f"   baseline interrupts {b['interrupts']}, landing {json.dumps(b['landing'])}, "
              f"→compromise: n {bc['n']} censored {bc['censored_share']:.3f} mean {bc['mean_observed']['mean'] if bc['mean_observed'] else None}")
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
    for interval in INTERVALS:
        blk = out["shield"]["by_interval"][str(interval)]
        for c, arms in blk["ledger"].items():
            for arm in ("baseline", "movement"):
                L = arms[arm]
                if not L["decisions"]:
                    continue
                print(f"\nMTDShield {c} @ {interval} s {arm}: runs {L['runs']}, decisions/run {L['decisions_per_run']['mean']:.1f}, "
                      f"execs/run {L['executions_per_run']['mean']:.1f}, forced {L['forced_share']:.3f}, "
                      f"actions {json.dumps({k: round(v, 3) for k, v in L['action_share'].items()})}")
        for arm, chk in blk["check"].items():
            print(f"   check {arm}: " + "  ".join(f"{c} {chk[c]['point']:.3f} [{chk[c]['lo']:.3f},{chk[c]['hi']:.3f}] n={chk['n'][c]}"
                                                for c in ("mtdshield",) + SHIELD_CHECK))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
