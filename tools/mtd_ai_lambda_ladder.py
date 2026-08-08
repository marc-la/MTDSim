"""The λ ladder — the calibration run that decides whether `mtd_ai` is worth
any large-scale training time.

The claim under test is a single sentence: *an agent that moves smartly moves
less when moving costs more.* So the ladder varies **only** the reward's cost
weight λ, holding the seed, the geometry, the horizon, the architecture and the
exploration schedule fixed, and reports the greedy no-op share against it.

Per λ and per seed the script trains one agent from scratch and then evaluates
it under a strictly greedy policy (ε = 0) on fresh networks. Training-time
statistics are reported too but are not the verdict: at any ε above zero the
no-op share is floored by ε/5 regardless of what the policy learned, so a ladder
read off the training share would report the exploration schedule.

Two floors bound what the greedy share can be, and both are reported rather than
subtracted out:

- the **static-degrade guard** forces a deployment whenever the network has gone
  `static_degrade_factor` seconds without one, so a policy that never chooses to
  deploy still deploys once every `static_degrade_factor / mtd_interval`
  decisions;
- the **action space** has one no-op among five actions, so a uniform random
  selector — which is what every figure in Tay's paper actually characterises —
  sits at 0.2.

Usage:

    PYTHONPATH=. python tools/mtd_ai_lambda_ladder.py \
        --out data/results/mtd_ai_lambda_ladder/ladder.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mtd_ai_run import (  # noqa: E402
    ACTION_SIZE,
    DEFAULT_GEOMETRY,
    MTD_STRATEGIES,
    run_evaluation_episode,
    train_agent,
)

# Ladder points. Sized from a pilot at λ = 0: the mean |reward| per transition
# is ~46, and the mean Δdowntime separation between a no-op (-0.35) and a
# deployment (+0.15) is ~0.5, so λ · 0.5 spans ~12 (clearly sub-dominant) to
# ~200 (clearly dominant) over this range. A ladder that did not bracket the
# security reward's own magnitude could not distinguish "the agent ignores cost"
# from "the cost was never large enough to notice".
DEFAULT_LAMBDAS = [0.0, 25.0, 50.0, 100.0, 200.0, 400.0]

# Execution durations, for the mutation-mix reading. Cheap and expensive are
# defined by MTD_DURATION, which is provenance-badged faithful against Zhang
# 2023 Table 3 and is an input here, never tuned.
MECHANISM_DURATION = {
    "CompleteTopologyShuffle": 110,
    "IPShuffle": 100,
    "OSDiversity": 80,
    "ServiceDiversity": 70,
}


def _mix_stats(mix: dict) -> dict:
    """Mean execution duration of the mutations actually fired, and the share
    of them drawn from the two cheap mechanisms."""
    total = sum(mix.values())
    if not total:
        return {"mean_duration": float("nan"), "cheap_share": float("nan")}
    weighted = sum(MECHANISM_DURATION.get(name, 0) * n for name, n in mix.items())
    cheap = sum(n for name, n in mix.items()
                if MECHANISM_DURATION.get(name, 999) <= 80)
    return {"mean_duration": weighted / total, "cheap_share": cheap / total}


def evaluate(main_network, *, episodes, finish_time, mtd_interval,
             static_degrade_factor, attacker_sensitivity, downtime_window,
             geometry) -> dict:
    per_episode = []
    mix = Counter()
    for _ in range(episodes):
        summary = run_evaluation_episode(
            main_network,
            finish_time=finish_time,
            mtd_interval=mtd_interval,
            epsilon=0.0,
            static_degrade_factor=static_degrade_factor,
            attacker_sensitivity=attacker_sensitivity,
            downtime_window=downtime_window,
            geometry=geometry,
        )
        log = summary.pop("decision_log")
        chosen = [d for d in log if d["source"] == "greedy"]
        summary["n_forced"] = sum(1 for d in log if d["source"] == "forced")
        summary["forced_share"] = summary["n_forced"] / len(log) if log else float("nan")
        # The share over decisions the policy actually made, with the forced
        # deployments excluded: the guard's floor is reported beside it rather
        # than folded into it.
        summary["chosen_noop_share"] = (
            sum(1 for d in chosen if d["action"] == 0) / len(chosen)
            if chosen else float("nan")
        )
        mix.update(summary["mutation_mix"])
        per_episode.append(summary)

    def mean(key):
        values = [e[key] for e in per_episode if e[key] == e[key]]
        return float(np.mean(values)) if values else float("nan")

    return {
        "n_episodes": episodes,
        "noop_share": mean("noop_share"),
        "chosen_noop_share": mean("chosen_noop_share"),
        "forced_share": mean("forced_share"),
        "mutation_rate_per_1000s": mean("mutation_rate_per_1000s"),
        "downtime_ratio_final": mean("downtime_ratio_final"),
        "n_compromised_hosts": mean("n_compromised_hosts"),
        "n_decisions": mean("n_decisions"),
        "mutation_mix": dict(mix),
        **_mix_stats(dict(mix)),
        "per_episode": per_episode,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="the mtd_ai cost-calibration ladder")
    ap.add_argument("--lambdas", type=float, nargs="+", default=DEFAULT_LAMBDAS)
    ap.add_argument("--seeds", type=int, nargs="+", default=[11, 22, 33])
    ap.add_argument("--episodes", type=int, default=150)
    ap.add_argument("--eval-episodes", type=int, default=5)
    ap.add_argument("--finish-time", type=int, default=5000)
    ap.add_argument("--mtd-interval", type=int, default=200)
    ap.add_argument("--total-nodes", type=int, default=100)
    ap.add_argument("--gamma", type=float, default=0.95)
    ap.add_argument("--epsilon", type=float, default=1.0)
    ap.add_argument("--epsilon-min", type=float, default=0.05)
    ap.add_argument("--epsilon-decay", type=float, default=0.999)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--train-start", type=int, default=200)
    ap.add_argument("--memory-size", type=int, default=2000)
    ap.add_argument("--target-sync-every", type=int, default=5)
    ap.add_argument("--static-degrade-factor", type=float, default=2000)
    ap.add_argument("--attacker-sensitivity", type=float, default=1.0)
    ap.add_argument("--downtime-window", type=float, default=200.0)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    geometry = dict(DEFAULT_GEOMETRY)
    geometry["total_nodes"] = args.total_nodes

    cells = []
    t_start = time.time()
    for downtime_lambda in args.lambdas:
        for seed in args.seeds:
            t0 = time.time()
            print(f"[λ={downtime_lambda:g} seed={seed}] training "
                  f"{args.episodes} episodes...", flush=True)
            main_network, episodes = train_agent(
                episodes=args.episodes,
                seed=seed,
                finish_time=args.finish_time,
                mtd_interval=args.mtd_interval,
                gamma=args.gamma,
                epsilon=args.epsilon,
                epsilon_min=args.epsilon_min,
                epsilon_decay=args.epsilon_decay,
                epsilon_decay_per="step",
                batch_size=args.batch_size,
                train_start=args.train_start,
                memory_size=args.memory_size,
                target_sync_every=args.target_sync_every,
                static_degrade_factor=args.static_degrade_factor,
                attacker_sensitivity=args.attacker_sensitivity,
                downtime_lambda=downtime_lambda,
                downtime_window=args.downtime_window,
                geometry=geometry,
                verbose=False,
            )
            evaluation = evaluate(
                main_network,
                episodes=args.eval_episodes,
                finish_time=args.finish_time,
                mtd_interval=args.mtd_interval,
                static_degrade_factor=args.static_degrade_factor,
                attacker_sensitivity=args.attacker_sensitivity,
                downtime_window=args.downtime_window,
                geometry=geometry,
            )
            cell = {
                "lambda": downtime_lambda,
                "seed": seed,
                "train_wallclock_s": time.time() - t0,
                "train_tail": episodes[-10:],
                "evaluation": evaluation,
            }
            cells.append(cell)
            print(f"    -> greedy no-op {evaluation['noop_share']:.3f} "
                  f"(chosen {evaluation['chosen_noop_share']:.3f}, "
                  f"forced {evaluation['forced_share']:.3f})  "
                  f"mutations/1000s {evaluation['mutation_rate_per_1000s']:.2f}  "
                  f"cheap share {evaluation['cheap_share']:.3f}  "
                  f"[{time.time() - t0:.0f}s]", flush=True)

            os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
            with open(args.out, "w") as f:
                json.dump({"args": vars(args), "cells": cells}, f,
                          indent=2, default=str)

    print(f"\ntotal wallclock {time.time() - t_start:.0f}s -> {args.out}")

    # A terse ladder table, so the verdict is legible without post-processing.
    print(f"\n{'lambda':>8} {'noop':>7} {'chosen':>7} {'forced':>7} "
          f"{'mut/1ks':>8} {'meandur':>8} {'cheap':>7} {'comp':>6}")
    for downtime_lambda in args.lambdas:
        rows = [c["evaluation"] for c in cells if c["lambda"] == downtime_lambda]
        if not rows:
            continue
        def m(key):
            values = [r[key] for r in rows if r[key] == r[key]]
            return float(np.mean(values)) if values else float("nan")
        print(f"{downtime_lambda:8g} {m('noop_share'):7.3f} "
              f"{m('chosen_noop_share'):7.3f} {m('forced_share'):7.3f} "
              f"{m('mutation_rate_per_1000s'):8.2f} {m('mean_duration'):8.1f} "
              f"{m('cheap_share'):7.3f} {m('n_compromised_hosts'):6.1f}")
    print(f"\nreference floors: uniform random selector = {1/ACTION_SIZE:.3f} no-op; "
          f"static-degrade guard forces one deployment per "
          f"{args.static_degrade_factor / args.mtd_interval:.0f} decisions; "
          f"{len(MTD_STRATEGIES)} mechanisms in the action space")


if __name__ == "__main__":
    main()
