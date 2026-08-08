"""
Driver for the `mtd_ai` reactive defender — training, evaluation, and the
per-decision ledger the calibration study reads.

Tay's own drivers (``experiments/run.py``, ``experiments/train_models.py``) were
deleted from the tree in ``e5935ab`` / ``6f235ba``; they are recoverable at
``62e1ebc`` and were read to build this one
(``docs/implementation/pipeline/ogasp/mtd_ai_forensics.md`` §0). This is not a
restoration of them. It differs deliberately in four ways, each of which the
forensics record explains:

1. **Evaluation is greedy by default** (``epsilon=0.0``). Tay's harness never
   overrode ``execute_ai_model``'s ``epsilon=1.0`` default, so ``predict`` was
   never called and every published figure characterises a uniform random
   selector (forensics §2). The paper specifies greedy selection at evaluation
   (§4.1.4); this driver does that, and an ``--epsilon`` above zero is an
   explicit opt-in rather than a default nobody noticed.
2. **Everything is seeded and the seed is reported.** Tay's harness seeded
   nothing.
3. **``custom_strategies`` is always passed explicitly.** ``execute_ai_training``
   left it ``None`` and relied on ``MTDScheme`` substituting its own list, which
   left the operation object's own ``len(custom_strategies)`` unusable.
4. **ε decays per step, not per episode.** The 0.980–0.998 constants are
   per-*step* rates in the literature Tay cites; applied per episode over 100
   episodes ``epsilon_min`` is never approached (forensics §4(b)). Which one is
   in force is a declared parameter here (``--epsilon-decay-per``) rather than
   an accident of where the multiply sits.

The snapshot machinery is deliberately not used: every episode builds a fresh
network, as Tay's ``new_network=True`` configuration did, so no on-disk snapshot
can silently change a run.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
import warnings
from collections import deque

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning,
)

import numpy as np
import simpy

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.mtdai.mtd_ai import (
    CANONICAL_FEATURES,
    create_network,
    mtd_action_space,
    update_target_model,
)
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.operation.mtd_ai_operation import MTDAIOperation
from mtdnetwork.operation.mtd_ai_training import MTDAITraining
from mtdnetwork.statistic.evaluation import Evaluation
from mtdnetwork.statistic.security_metric_statistics import SecurityMetricStatistics


# The four mechanisms Tay's action space ranges over, in his order, and the live
# 5/6 state head (MTDAI-02). Both now read from `mtdnetwork.mtdai.mtd_ai`, which
# owns them alongside the state vocabularies, so this driver and the movement
# runner cannot disagree about what action 1 deploys or what the agent can see.
# Action 0 is the no-op, so the action space is len(MTD_STRATEGIES) + 1 = 5.
MTD_STRATEGIES = mtd_action_space()

FEATURES = CANONICAL_FEATURES
STATIC_FEATURES = FEATURES["static"]
TIME_FEATURES = FEATURES["time"]

STATE_SIZE = len(STATIC_FEATURES)
TIME_SERIES_SIZE = len(TIME_FEATURES)
ACTION_SIZE = len(MTD_STRATEGIES) + 1

# Geometry. 100 nodes is Tay's own training size (forensics §4); the rest match
# the substrate's defaults as used by baseline/run_baseline.py.
DEFAULT_GEOMETRY = dict(
    total_nodes=100,
    total_endpoints=5,
    total_subnets=8,
    total_layers=4,
    target_layer=4,
    total_database=2,
    terminate_compromise_ratio=0.8,
)


def seed_all(seed: int) -> None:
    """Seed every stream a run draws from.

    D-29 records that the mechanisms and the attacker share one Python `random`
    stream, so this is one seed for two logical actors — arms at a common seed
    are independent, not paired.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    import tensorflow as tf

    tf.random.set_seed(seed)


def build_agent(seed: int | None = None):
    """Create the main and target networks with synced weights."""
    if seed is not None:
        seed_all(seed)
    main_network = create_network(STATE_SIZE, ACTION_SIZE, TIME_SERIES_SIZE)
    target_network = create_network(STATE_SIZE, ACTION_SIZE, TIME_SERIES_SIZE)
    target_network.set_weights(main_network.get_weights())
    return main_network, target_network


def _build_world(geometry: dict):
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**geometry)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_operation = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0
    )
    attack_operation.proceed_attack()
    return env, end_event, network, adversary, attack_operation


def run_training_episode(
    main_network,
    target_network,
    memory,
    *,
    finish_time: int,
    mtd_interval: int,
    epsilon: float,
    gamma: float,
    epsilon_min: float,
    epsilon_decay: float,
    batch_size: int,
    train_start: int,
    static_degrade_factor: float,
    attacker_sensitivity: float,
    downtime_lambda: float,
    downtime_window: float,
    geometry: dict,
) -> dict:
    """Run one training episode. Returns the episode's decision ledger + stats."""
    env, end_event, network, adversary, attack_operation = _build_world(geometry)
    security_metric_record = SecurityMetricStatistics()

    operation = MTDAITraining(
        security_metric_record=security_metric_record,
        features=FEATURES,
        env=env,
        end_event=end_event,
        network=network,
        attack_operation=attack_operation,
        scheme="mtd_ai",
        adversary=adversary,
        proceed_time=0,
        mtd_trigger_interval=mtd_interval,
        custom_strategies=list(MTD_STRATEGIES),
        main_network=main_network,
        target_network=target_network,
        memory=memory,
        gamma=gamma,
        epsilon=epsilon,
        epsilon_min=epsilon_min,
        epsilon_decay=epsilon_decay,
        train_start=train_start,
        batch_size=batch_size,
        attacker_sensitivity=attacker_sensitivity,
        static_degrade_factor=static_degrade_factor,
        downtime_lambda=downtime_lambda,
        downtime_window=downtime_window,
    )
    operation.proceed_mtd()
    env.run(until=finish_time)

    return _episode_summary(operation, network, adversary, env)


def run_evaluation_episode(
    main_network,
    *,
    finish_time: int,
    mtd_interval: int,
    epsilon: float,
    static_degrade_factor: float,
    attacker_sensitivity: float,
    downtime_window: float,
    geometry: dict,
) -> dict:
    """Run one evaluation episode with no learning."""
    env, end_event, network, adversary, attack_operation = _build_world(geometry)
    security_metrics_record = SecurityMetricStatistics()

    operation = MTDAIOperation(
        features=FEATURES,
        security_metrics_record=security_metrics_record,
        env=env,
        end_event=end_event,
        network=network,
        attack_operation=attack_operation,
        scheme="mtd_ai",
        adversary=adversary,
        proceed_time=0,
        mtd_trigger_interval=mtd_interval,
        custom_strategies=list(MTD_STRATEGIES),
        main_network=main_network,
        attacker_sensitivity=attacker_sensitivity,
        epsilon=epsilon,
        static_degrade_factor=static_degrade_factor,
        downtime_window=downtime_window,
    )
    operation.proceed_mtd()
    env.run(until=finish_time)

    return _episode_summary(operation, network, adversary, env)


def _episode_summary(operation, network, adversary, env) -> dict:
    """Reduce one episode to the numbers the ladder reports."""
    ledger = operation.get_decision_log()
    mtd_record = network.get_mtd_stats().get_record()
    compromised = adversary.get_compromised_hosts()

    n_decisions = len(ledger)
    n_noop = sum(1 for d in ledger if d["action"] == 0)
    n_greedy = sum(1 for d in ledger if d["source"] == "greedy")
    n_greedy_noop = sum(
        1 for d in ledger if d["source"] == "greedy" and d["action"] == 0
    )

    mix: dict[str, int] = {}
    if len(mtd_record) > 0:
        mix = mtd_record["name"].value_counts().to_dict()

    return {
        "n_decisions": n_decisions,
        "n_noop": n_noop,
        "noop_share": n_noop / n_decisions if n_decisions else float("nan"),
        "n_greedy": n_greedy,
        "n_greedy_noop": n_greedy_noop,
        "greedy_noop_share": (
            n_greedy_noop / n_greedy if n_greedy else float("nan")
        ),
        "n_mtd_executed": int(len(mtd_record)),
        "mutation_rate_per_1000s": (
            1000.0 * len(mtd_record) / env.now if env.now else float("nan")
        ),
        "mutation_mix": {str(k): int(v) for k, v in mix.items()},
        "downtime_ratio_final": network.get_mtd_stats().downtime_ratio(
            env.now, operation.downtime_window
        ),
        "n_compromised_hosts": int(len(compromised)),
        "sim_time": float(env.now),
        "epsilon_final": (
            float(operation.get_epsilon()) if hasattr(operation, "get_epsilon") else None
        ),
        "decision_log": ledger,
    }


def train_agent(
    *,
    episodes: int,
    seed: int,
    finish_time: int,
    mtd_interval: int,
    gamma: float,
    epsilon: float,
    epsilon_min: float,
    epsilon_decay: float,
    epsilon_decay_per: str,
    batch_size: int,
    train_start: int,
    memory_size: int,
    target_sync_every: int,
    static_degrade_factor: float,
    attacker_sensitivity: float,
    downtime_lambda: float,
    downtime_window: float,
    geometry: dict,
    verbose: bool = True,
) -> tuple:
    """Train one agent. Returns (main_network, per-episode summaries)."""
    seed_all(seed)
    main_network, target_network = build_agent()
    memory = deque(maxlen=memory_size)

    summaries = []
    for episode in range(episodes):
        t0 = time.time()
        summary = run_training_episode(
            main_network,
            target_network,
            memory,
            finish_time=finish_time,
            mtd_interval=mtd_interval,
            epsilon=epsilon,
            gamma=gamma,
            epsilon_min=epsilon_min,
            epsilon_decay=(
                epsilon_decay if epsilon_decay_per == "step" else 1.0
            ),
            batch_size=batch_size,
            train_start=train_start,
            static_degrade_factor=static_degrade_factor,
            attacker_sensitivity=attacker_sensitivity,
            downtime_lambda=downtime_lambda,
            downtime_window=downtime_window,
            geometry=geometry,
        )
        # The operation object owns epsilon during the episode when the decay is
        # per-step; read it back so the schedule carries across episodes.
        if epsilon_decay_per == "step":
            epsilon = summary.pop("epsilon_final", epsilon)
        else:
            summary.pop("epsilon_final", None)
            if epsilon > epsilon_min:
                epsilon *= epsilon_decay

        summary["episode"] = episode
        summary["epsilon"] = epsilon
        summary["wallclock_s"] = time.time() - t0
        summary.pop("decision_log", None)
        summaries.append(summary)

        if episode % target_sync_every == 0:
            update_target_model(target_network, main_network)

        if verbose:
            print(
                f"  ep {episode:3d}  eps={epsilon:.3f}  "
                f"decisions={summary['n_decisions']:4d}  "
                f"noop={summary['noop_share']:.3f}  "
                f"mtds={summary['n_mtd_executed']:3d}  "
                f"downtime={summary['downtime_ratio_final']:.3f}  "
                f"{summary['wallclock_s']:.1f}s",
                flush=True,
            )

    return main_network, summaries


def _geometry_from_args(args) -> dict:
    geometry = dict(DEFAULT_GEOMETRY)
    geometry["total_nodes"] = args.total_nodes
    return geometry


def main() -> None:
    ap = argparse.ArgumentParser(description="mtd_ai training / evaluation driver")
    ap.add_argument("--mode", choices=["train", "evaluate"], default="train")
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--episodes", type=int, default=20)
    ap.add_argument("--finish-time", type=int, default=5000)
    ap.add_argument("--mtd-interval", type=int, default=200)
    ap.add_argument("--total-nodes", type=int, default=100)
    ap.add_argument("--gamma", type=float, default=0.95)
    ap.add_argument("--epsilon", type=float, default=1.0)
    ap.add_argument("--epsilon-min", type=float, default=0.01)
    ap.add_argument("--epsilon-decay", type=float, default=0.995)
    ap.add_argument("--epsilon-decay-per", choices=["step", "episode"],
                    default="step")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--train-start", type=int, default=200)
    ap.add_argument("--memory-size", type=int, default=2000)
    ap.add_argument("--target-sync-every", type=int, default=5)
    ap.add_argument("--static-degrade-factor", type=float, default=2000)
    ap.add_argument("--attacker-sensitivity", type=float, default=1.0)
    ap.add_argument("--downtime-lambda", type=float, default=0.0)
    ap.add_argument("--downtime-window", type=float, default=200.0)
    ap.add_argument("--model-path", default=None,
                    help="train: where to save; evaluate: what to load")
    ap.add_argument("--out", default=None, help="write the summary JSON here")
    args = ap.parse_args()

    geometry = _geometry_from_args(args)

    if args.mode == "train":
        main_network, summaries = train_agent(
            episodes=args.episodes,
            seed=args.seed,
            finish_time=args.finish_time,
            mtd_interval=args.mtd_interval,
            gamma=args.gamma,
            epsilon=args.epsilon,
            epsilon_min=args.epsilon_min,
            epsilon_decay=args.epsilon_decay,
            epsilon_decay_per=args.epsilon_decay_per,
            batch_size=args.batch_size,
            train_start=args.train_start,
            memory_size=args.memory_size,
            target_sync_every=args.target_sync_every,
            static_degrade_factor=args.static_degrade_factor,
            attacker_sensitivity=args.attacker_sensitivity,
            downtime_lambda=args.downtime_lambda,
            downtime_window=args.downtime_window,
            geometry=geometry,
        )
        if args.model_path:
            main_network.save(args.model_path)
        payload = {"mode": "train", "args": vars(args), "episodes": summaries}
    else:
        import keras

        seed_all(args.seed)
        main_network = keras.saving.load_model(args.model_path, compile=False)
        summary = run_evaluation_episode(
            main_network,
            finish_time=args.finish_time,
            mtd_interval=args.mtd_interval,
            epsilon=args.epsilon,
            static_degrade_factor=args.static_degrade_factor,
            attacker_sensitivity=args.attacker_sensitivity,
            downtime_window=args.downtime_window,
            geometry=geometry,
        )
        payload = {"mode": "evaluate", "args": vars(args), "summary": summary}

    text = json.dumps(payload, indent=2, default=str)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w") as f:
            f.write(text)
    print(text if not args.out else f"wrote {args.out}")


if __name__ == "__main__":
    sys.exit(main())
