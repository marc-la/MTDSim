"""The chapter 5 defended corpus — the run half, shared by §5.3.2, §5.4 and §5.5.

Design: docs/handoffs/2026-09-17_ch5_s532_s55_defended_runs.md. One corpus at
the chapter's declared configuration (Table 5.3: v2_partial, the failure-only
overlay passed by name, retrace on, fresh-host contract on, modulators off, the
targeted objective on the database set, 100 seeds shared across arms, 15 000 s)
over Table 5.2's defence conditions (no defence; the seven mechanisms alone;
random and alternative over the seven) at both mutation intervals, on six arms
(the baseline attacker; the movement attacker on the four profiles and the
aggregate). Four arm groups, keyed by ``group``:

  core      targeted objective, quasi-periodic ("shifted") regime — every
            §5.4.1, §5.4.2 and §5.5 float
  blind     the verdict-blind control (F_v = identity) on the four profiles
            under the spanning pair (IP shuffle; OS diversity) at both
            intervals, plus no defence — §5.3.2's control and its placebo null
  lineage   the same matrix under the opportunistic ("general") objective —
            §5.4.3's re-run of the prior evaluations at the lineage's objective
  regime    the exponential (memoryless) timing regime at 200 s, targeted —
            Table 5.2's one-at-a-time factor, read in the analysis

The no-defence cell never reads the interval or the regime, so it is run once
per arm and objective (``interval`` 0) and serves as the reference at both.
Every number is computed by ``analyse.py`` off the recorded stream.

    PYTHONPATH=src python data/results/ch5_defended/run_corpus.py
"""
from __future__ import annotations

import json
import re
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "runs.jsonl"
# §5.4's ablation cells at the reported seed count (Marc 2026-09-28): seeds
# 100-999 of the core and blind arms, written beside the corpus so the shared
# stream is never rewritten; ablation.py reads both.
OUT_ABLATION = HERE / "runs_ablation.jsonl"
ABLATION_SEEDS = tuple(range(100, 1_000))

PROFILES = (
    "objective_exfiltration",
    "objective_impact",
    "objective_exfiltration_impact",
    "objective_none_c2",
    "aggregate",
)
FOUR = PROFILES[:4]
SEEDS = tuple(range(100))
INTERVALS = (200, 2_000)
# The interval sweep (E6; Marc 2026-09-25): the four levels between and below
# the corpus's two, so each line has six points from 50 s to 2 000 s.
SWEEP_INTERVALS = (50, 100, 500, 1_000)
# The reported corpus (REPORTED=1; seed-count protocol, Marc 2026-09-30): the
# cells §5.3's floats read, at 1 000 seeds, the APT attacker model with the
# vulnerability memory on (Table 5.1: each earlier success triples the odds;
# code rate 2, factor 1 + 2) and the baseline attacker with none. Written apart
# from runs.jsonl, which the 100-seed record and §5.4.1's ablation still read.
OUT_REPORTED = HERE / "runs_reported.jsonl"
REPORTED_SEEDS = 1_000
MEMORY_RATE = 2.0
HORIZON = 15_000
MAPPING = "v2_partial"
OVERLAY = "v4_failure_only"

# condition -> (scheme, mechanism class or None for the full pool)
CONDITIONS: dict[str, tuple[str | None, str | None]] = {
    "none": (None, None),
    "ip_shuffle": ("single", "IPShuffle"),
    "complete_topology": ("single", "CompleteTopologyShuffle"),
    "host_topology": ("single", "HostTopologyShuffle"),
    "port_shuffle": ("single", "PortShuffle"),
    "user_shuffle": ("single", "UserShuffle"),
    "os_diversity": ("single", "OSDiversity"),
    "service_diversity": ("single", "ServiceDiversity"),
    "random": ("random", None),
    "alternative": ("alternative", None),
    # MTDShield (Marc 2026-09-25; handoff 2026-09-25_mtdshield_preliminary_run.md):
    # Tay's released agent, greedy, over his four mechanisms plus the no-op,
    # through his evaluation builder; random over the same four as its matched
    # control; and the same agent through his training builder, the check on
    # the inputs the two builders define differently (Appendix E).
    "mtdshield": ("mtd_ai", "tay2024_eval"),
    "random_four": ("random", "FOUR"),
    "mtdshield_train": ("mtd_ai", "tay2024_train"),
}
# The 2026-09-17 corpus's nine; build_jobs() is unchanged over them.
DEFENDED = ("ip_shuffle", "complete_topology", "host_topology", "port_shuffle", "user_shuffle",
            "os_diversity", "service_diversity", "random", "alternative")
SHIELD = ("mtdshield", "random_four")
SHIELD_CHECK = ("mtdshield_train",)
# Tay's highest-scoring agent (epsilon 0.5, decay 0.99; his commit f13ed49a).
AGENT = HERE.parents[2] / "mtdsim-weights-archive" / "main_network_epsilon_0.5_decay_0.99__0848c2e2d5b7.h5"
MTDAI_EPSILON = 0.0
MTDAI_SENSITIVITY = 1.0
SPANNING = ("ip_shuffle", "os_diversity")
MODULES = {
    "CompleteTopologyShuffle": "completetopologyshuffle",
    "HostTopologyShuffle": "hosttopologyshuffle",
    "IPShuffle": "ipshuffle",
    "OSDiversity": "osdiversity",
    "PortShuffle": "portshuffle",
    "ServiceDiversity": "servicediversity",
    "UserShuffle": "usershuffle",
}


def _strategies(condition: str):
    """``custom_strategies`` for the seam: one class for a single mechanism,
    the full seven-mechanism pool (Table 5.2: "random and alternative over the
    seven") for a scheme, None for no defence. The substrate's default pool
    is the lineage four, so the seven are passed explicitly."""
    import importlib

    scheme, mech = CONDITIONS[condition]
    if scheme is None:
        return None, None
    if scheme == "mtd_ai" or mech == "FOUR":
        # Tay's four, in the order his agent's action indices point at.
        from mtdnetwork.mtdai.mtd_ai import mtd_action_space

        return scheme, mtd_action_space()
    if mech is not None:
        return scheme, getattr(importlib.import_module(f"mtdnetwork.mtd.{MODULES[mech]}"), mech)
    return scheme, [
        getattr(importlib.import_module(f"mtdnetwork.mtd.{MODULES[m]}"), m) for m in MODULES
    ]


_AGENT = None


def _agent():
    """Tay's agent, loaded once per worker process."""
    global _AGENT
    if _AGENT is None:
        os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
        import keras
        import tensorflow as tf

        tf.config.threading.set_intra_op_parallelism_threads(1)
        tf.config.threading.set_inter_op_parallelism_threads(1)
        _AGENT = _Compiled(keras.saving.load_model(str(AGENT), compile=False))
    return _AGENT


class _Compiled:
    """The agent's forward pass traced once as a graph (tf.function) instead of
    run layer by layer in eager mode: 1.2 ms a decision against 45 ms, which
    was half the corpus's compute. Checked 2026-09-30 before adoption: Q-values
    bitwise equal to eager on 1 965 decisions, and 108 MTDShield runs
    byte-identical. Everything but the call is the model's own."""

    def __init__(self, model):
        import tensorflow as tf

        self._model = model
        self._fn = tf.function(lambda x: model(x, training=False), reduce_retracing=True)

    def __call__(self, inputs, training=False):
        assert not training
        return self._fn(inputs)

    def __getattr__(self, name):
        return getattr(self._model, name)


def _mtd_ai_config(condition: str):
    from mtdsim.l3_simulation.movement.run import MTDAIConfig

    scheme, layout = CONDITIONS[condition]
    if scheme != "mtd_ai":
        return None
    _, strategies = _strategies(condition)
    return MTDAIConfig(main_network=_agent(), epsilon=MTDAI_EPSILON,
                       attacker_sensitivity=MTDAI_SENSITIVITY,
                       strategies=strategies, feature_layout=layout)


def _decisions(ledger) -> dict:
    return {"mtd_decisions": [[round(float(d.time), 6), int(d.action), str(d.source)] for d in ledger]}


def _mtd_fields(result_like) -> dict:
    return {
        "mtd_executions": [
            [e.name, round(float(e.start_time), 6), round(float(e.finish_time), 6),
             round(float(e.duration), 6), e.layer]
            for e in result_like["mtd_executions"]
        ],
        "mtd_suspended": int(result_like["mtd_suspended_count"]),
        "mtd_attack_interrupted": int(result_like["mtd_attack_interrupted"]),
    }


def _movement(job: dict) -> dict:
    from mtdsim.l3_simulation.controller import verdict_blind_overlay
    from mtdsim.l3_simulation.movement.run import run_movement

    scheme, strategies = _strategies(job["condition"])
    mtd_ai = _mtd_ai_config(job["condition"])
    if mtd_ai is not None:
        strategies = None  # the agent's pool travels in its config
    overlay_kw = (
        {"overlay": verdict_blind_overlay()} if job["overlay"] == "verdict_blind"
        else {"overlay_version": job["overlay"]}
    )
    r = run_movement(
        job["profile"],
        seed=job["seed"],
        with_synthetic_overlay=True,
        horizon=job["horizon"],
        mapping_version=MAPPING,
        retrace_sinks=True,
        mtd_scheme=scheme,
        mtd_interval=(job["interval"] or None),
        custom_strategies=strategies,
        substrate_timing_regime=job["regime"],
        attack_objective=job["objective"],
        target_layer=None,
        # the vulnerability memory (Section 4.4.5); absent from the 100-seed
        # corpus's jobs, so those re-run byte-identical with it off
        exploit_learning_rate=job.get("exploit_learning_rate"),
        **({"mtd_ai": mtd_ai} if mtd_ai is not None else {}),
        **overlay_kw,
    )
    return {
        **job,
        "termination_time": float(r.termination_time),
        "compromised": int(r.compromised_count),
        "reached_objective": bool(r.reached_objective),
        "database_hosts_reached": int(r.database_hosts_reached),
        "first_database_reach_time": r.first_database_reach_time,
        "target_hosts": list(r.target_hosts),
        "retrace_count": int(r.retrace_count),
        "last_next_place": (r.records[-1].next_place if r.records else None),
        "records": [
            [
                x.place, x.verb, x.outcome, x.verdict, int(x.blocked), int(x.interrupted),
                round(float(x.dwell), 6), round(float(x.start_time), 6),
                round(float(x.end_time), 6), x.place_class,
            ]
            for x in r.records
        ],
        **_mtd_fields({
            "mtd_executions": r.mtd_executions,
            "mtd_suspended_count": r.mtd_suspended_count,
            "mtd_attack_interrupted": r.mtd_attack_interrupted,
        }),
        **(_decisions(r.mtd_decisions) if mtd_ai is not None else {}),
    }


def _baseline(job: dict) -> dict:
    """The inherited attacker, wired as the Gate 0 harness and the frontier
    study wired it: the shared ``AttackOperation``, the objective installed
    through the same ``_install_objective`` seam, the defence through the
    substrate's own ``MTDOperation`` on the same ``end_event``."""
    import random

    import numpy as np
    import simpy

    from mtdnetwork.component.adversary import Adversary
    from mtdnetwork.component.time_network import TimeNetwork
    from mtdnetwork.data.constants import ATTACKER_THRESHOLD
    from mtdnetwork.operation.attack_operation import AttackOperation
    from mtdsim.l3_simulation.movement.run import (GEOMETRY, _install_objective, decision_snapshot,
                                                   mtd_snapshot)
    from mtdnetwork.component.time_generator import set_exponential_regime

    seed = job["seed"]
    # Tay's agent is built BEFORE the seeds are set: loading it in a fresh
    # worker draws from the global random stream, so built after seeding it
    # gave the first MTDShield run in each worker a different stream from the
    # rest (2026-09-30, three of 80 re-run rows; the APT attacker model's path
    # always built it first).
    cfg = _mtd_ai_config(job["condition"])
    random.seed(seed)
    np.random.seed(seed)
    set_exponential_regime(job["regime"])
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary, proceed_time=0)
    target_hosts, _, _ = _install_objective(
        attack_op, network, job["objective"], target_layer=None, seed=seed
    )
    attack_op.proceed_attack()
    scheme, strategies = _strategies(job["condition"])
    operation = None
    if scheme == "mtd_ai":
        # As tools/mtd_ai_run.py builds it, on the same end_event and pins.
        from mtdnetwork.mtdai.mtd_ai import CANONICAL_FEATURES
        from mtdnetwork.operation.mtd_ai_operation import MTDAIOperation
        from mtdnetwork.statistic.security_metric_statistics import SecurityMetricStatistics

        operation = MTDAIOperation(
            features=CANONICAL_FEATURES, security_metrics_record=SecurityMetricStatistics(),
            env=env, end_event=end_event, network=network, attack_operation=attack_op,
            scheme="mtd_ai", adversary=adversary, proceed_time=0,
            mtd_trigger_interval=job["interval"], custom_strategies=cfg.strategies,
            main_network=cfg.main_network, attacker_sensitivity=cfg.attacker_sensitivity,
            epsilon=cfg.epsilon, static_degrade_factor=cfg.static_degrade_factor,
            downtime_window=cfg.downtime_window, feature_layout=cfg.feature_layout,
        )
        operation.proceed_mtd()
    elif scheme:
        from mtdnetwork.operation.mtd_operation import MTDOperation
        from mtdnetwork.statistic.security_metric_statistics import SecurityMetricStatistics

        MTDOperation(
            security_metrics_record=SecurityMetricStatistics(), env=env,
            end_event=end_event, network=network, scheme=scheme,
            attack_operation=attack_op, proceed_time=0,
            mtd_trigger_interval=job["interval"],
            custom_strategies=strategies, adversary=adversary,
        ).proceed_mtd()
    env.run(until=job["horizon"])

    rows = adversary.get_attack_stats().get_record()
    database = set(int(h) for h in network.get_database())
    compromised = set(adversary.get_compromised_hosts())
    recs = rows.to_dict("records")
    distinct_uuid = len({str(x["compromise_host_uuid"]) for x in recs
                         if str(x["compromise_host"]) != "None"})
    return {
        **job,
        "termination_time": float(env.now),
        "compromised": int(len(compromised)),
        "compromised_uuid": int(distinct_uuid),
        "reached_objective": bool(end_event.triggered),
        "database_hosts_reached": int(len(compromised & database)),
        "first_database_reach_time": None,
        "target_hosts": sorted(int(h) for h in target_hosts),
        "records": [
            [
                str(x["name"]), round(float(x["start_time"]), 6),
                round(float(x["finish_time"]), 6),
                None if str(x["compromise_host"]) == "None" else int(x["compromise_host"]),
                str(x["compromise_host_uuid"]),
                None if str(x["interrupted_in"]) == "None" else str(x["interrupted_in"]),
            ]
            for x in recs
        ],
        **_mtd_fields(mtd_snapshot(network)),
        **(_decisions(decision_snapshot(operation)) if operation is not None else {}),
    }


def dispatch(job: dict) -> dict:
    import contextlib
    import io

    try:
        # The substrate's metric record prints a line for each mechanism it has
        # no column for (the three restored singles); it is not an error and
        # would otherwise flood the log under the seven-mechanism schemes.
        with contextlib.redirect_stdout(io.StringIO()):
            return _baseline(job) if job["arm"] == "baseline" else _movement(job)
    except Exception as exc:  # a dead cell must be visible, never silently absent
        return {"error": f"{type(exc).__name__}: {exc}", **job}


def _job(group, arm, profile, objective, condition, interval, regime, overlay, seed) -> dict:
    return {"group": group, "arm": arm, "profile": profile, "objective": objective,
            "condition": condition, "interval": interval, "regime": regime,
            "overlay": overlay, "horizon": HORIZON, "seed": seed}


def build_jobs() -> list[dict]:
    jobs: list[dict] = []
    arms = [("baseline", "baseline")] + [("movement", p) for p in PROFILES]
    for group, objective in (("core", "targeted"), ("lineage", "general")):
        for seed in SEEDS:
            for arm, profile in arms:
                jobs.append(_job(group, arm, profile, objective, "none", 0, "shifted", OVERLAY, seed))
                for interval in INTERVALS:
                    for c in DEFENDED:
                        jobs.append(_job(group, arm, profile, objective, c, interval, "shifted", OVERLAY, seed))
    for seed in SEEDS:  # the verdict-blind control, §5.3.2
        for p in FOUR:
            jobs.append(_job("blind", "movement", p, "targeted", "none", 0, "shifted", "verdict_blind", seed))
            for interval in INTERVALS:
                for c in SPANNING:
                    jobs.append(_job("blind", "movement", p, "targeted", c, interval, "shifted", "verdict_blind", seed))
    for seed in SEEDS:  # the memoryless regime, one at a time from the core
        for arm, profile in arms:
            for c in DEFENDED:
                jobs.append(_job("regime", arm, profile, "targeted", c, 200, "exponential", OVERLAY, seed))
    return jobs


def build_shield_jobs(conditions=SHIELD, intervals=INTERVALS) -> list[dict]:
    """MTDShield and its matched control on the core group, appended to the
    corpus (the no-defence reference is the corpus's own)."""
    arms = [("baseline", "baseline")] + [("movement", p) for p in PROFILES]
    return [_job("core", arm, profile, "targeted", c, interval, "shifted", OVERLAY, seed)
            for seed in SEEDS for arm, profile in arms for interval in intervals for c in conditions]


def build_ablation_jobs(seeds=ABLATION_SEEDS) -> list[dict]:
    """The §5.4 cells, both arms: the four profiles, targeted, under no
    defence and the spanning pair at both intervals."""
    jobs: list[dict] = []
    for seed in seeds:
        for group, overlay in (("core", OVERLAY), ("blind", "verdict_blind")):
            for p in FOUR:
                jobs.append(_job(group, "movement", p, "targeted", "none", 0, "shifted", overlay, seed))
                for interval in INTERVALS:
                    for c in SPANNING:
                        jobs.append(_job(group, "movement", p, "targeted", c, interval, "shifted", overlay, seed))
    return jobs


def build_reported_jobs(seeds=range(REPORTED_SEEDS)) -> list[dict]:
    """§5.3's cells: the core group, both attackers (the four profiles and the
    aggregate), no MTD once and every ranked condition at the six deployment
    intervals, seed-major so a stopped run leaves whole seeds. The memory's
    rate travels in the job, so every row records it."""
    arms = [("baseline", "baseline")] + [("movement", p) for p in PROFILES]
    jobs: list[dict] = []
    for seed in seeds:
        for arm, profile in arms:
            rate = MEMORY_RATE if arm == "movement" else None
            cells = [("none", 0)] + [(c, i) for i in sorted(INTERVALS + SWEEP_INTERVALS) for c in DEFENDED + SHIELD]
            for c, i in cells:
                jobs.append({**_job("core", arm, profile, "targeted", c, i, "shifted", OVERLAY, seed),
                             "exploit_learning_rate": rate})
    return jobs


def _job_id(row: dict) -> tuple:
    return (row["arm"], row["profile"], row["condition"], row["interval"], row["seed"])


def _resume(path: Path) -> set:
    """The jobs already written (error rows included: a dead cell stays visible
    and is not silently re-run). A line cut off by a killed run is dropped."""
    if not path.exists():
        return set()
    # Only the tail is read for the cut, and only each row's head for its job:
    # the corpus outgrows memory (2026-10-01: reading 21.7 GB whole was killed
    # for memory, before any run started).
    with path.open("rb+") as fh:
        end = fh.seek(0, 2)
        pos = end
        while pos > 0:
            step = min(1 << 20, pos)
            fh.seek(pos - step)
            nl = fh.read(step).rfind(b"\n")
            if nl >= 0:
                pos = pos - step + nl + 1
                break
            pos -= step
        if pos < end:
            fh.truncate(pos)
    head = re.compile(rb'"arm": "(\w+)", "profile": "(\w+)", "objective": "\w+", "condition": "(\w+)", '
                      rb'"interval": (\d+), .*?"seed": (\d+)')
    done = set()
    with path.open("rb") as fh:
        for line in fh:
            m = head.search(line[:1024])
            if m:
                a, p, c, i, s = m.groups()
                done.add((a.decode(), p.decode(), c.decode(), int(i), int(s)))
            else:  # an error row's message may push the job past the head
                done.add(_job_id(json.loads(line)))
    return done


def main() -> int:
    # SHIELD=1 appends MTDShield, random over its four, and the training-builder
    # check to the existing runs.jsonl; the default rebuilds the 2026-09-17 corpus.
    # SWEEP=1 appends every defended condition at SWEEP_INTERVALS (core group only).
    # REPORTED=1 writes runs_reported.jsonl (SEEDS=N for fewer seeds), resuming
    # from whatever it already holds.
    if os.environ.get("REPORTED") == "1":
        return main_reported()
    shield = os.environ.get("SHIELD") == "1"
    sweep = os.environ.get("SWEEP") == "1"
    ablation = os.environ.get("ABLATION") == "1"
    if ablation:  # ABLATION=1 writes runs_ablation.jsonl, never runs.jsonl
        jobs = build_ablation_jobs()
    elif sweep:
        jobs = build_shield_jobs(DEFENDED + SHIELD, SWEEP_INTERVALS)
    else:
        jobs = (build_shield_jobs() + build_shield_jobs(SHIELD_CHECK)) if shield else build_jobs()
    if os.environ.get("LIMIT"):  # timing probe: the first N jobs, printed, not written
        jobs = jobs[: int(os.environ["LIMIT"])]
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    print(f"{len(jobs)} runs on {workers} workers -> {OUT_ABLATION if ablation else OUT}", flush=True)
    started = time.time()
    done = errors = 0
    out = os.devnull if os.environ.get("LIMIT") else (OUT_ABLATION if ablation else OUT)
    with open(out, "a" if (shield or sweep) else "w", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(dispatch, jobs, chunksize=16):
            fh.write(json.dumps(row) + "\n")
            done += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if done % 1000 == 0:
                print(f"  {done}/{len(jobs)}  {time.time() - started:.0f}s", flush=True)
    print(f"done: {done} runs, {errors} errors, {time.time() - started:.0f}s")
    return 1 if errors else 0


def main_reported() -> int:
    out = Path(os.environ.get("OUT", OUT_REPORTED))
    jobs = build_reported_jobs(range(int(os.environ.get("SEEDS", REPORTED_SEEDS))))
    if os.environ.get("LIMIT"):  # timing probe: the first N jobs, not written
        jobs, out = jobs[: int(os.environ["LIMIT"])], Path(os.devnull)
    done_ids = set() if out == Path(os.devnull) else _resume(out)
    todo = [j for j in jobs if _job_id(j) not in done_ids]
    workers = int(os.environ.get("WORKERS", min(7, os.cpu_count() or 4)))
    print(f"{len(jobs)} runs, {len(jobs) - len(todo)} already written, {len(todo)} to run "
          f"on {workers} workers -> {out}", flush=True)
    started = time.time()
    done = errors = 0
    with open(out, "a", encoding="utf-8") as fh, ProcessPoolExecutor(workers) as pool:
        for row in pool.map(dispatch, todo, chunksize=8):
            fh.write(json.dumps(row) + "\n")
            done += 1
            if "error" in row:
                errors += 1
                print(f"  ERROR {row}", file=sys.stderr, flush=True)
            if done % 1000 == 0:
                fh.flush()
                el = time.time() - started
                print(f"  {done}/{len(todo)}  {el:.0f}s  (seed {row['seed']}; "
                      f"~{el / done * (len(todo) - done) / 3600:.1f} h left)", flush=True)
    print(f"done: {done} runs, {errors} errors, {time.time() - started:.0f}s")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
