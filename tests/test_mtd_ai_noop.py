"""Regression tests for the three defects that made the do-nothing action
unreachable, plus the double registration that inflated every mutation count.

These are the repairs the calibration study rests on, so each is pinned by the
symptom it produced rather than by its implementation:

- **MTDAI-03.** The trigger yield sat inside the ``if action > 0`` block, so a
  no-op re-entered the loop at an unchanged ``env.now``. Under a greedy policy
  the state is unchanged at zero elapsed time, so the argmax is unchanged, and
  the loop spins forever. The test below runs a *strictly greedy* agent whose
  policy selects action 0 on every state — the exact configuration that used to
  hang — and requires the run to terminate, the clock to advance, and no
  mutation to fire.
- **MTDAI-04.** ``calculate_reward`` was reachable only from
  ``_mtd_execute_action``, so the replay buffer contained deploying actions
  exclusively and the Q-value of action 0 was never a TD target.
- **MTDAI-08.** The scorer registration took ``register_mtd(...)`` as its
  argument, enqueuing a second MTD per decision.

TensorFlow is imported through the driver, so these are slower than the rest of
the suite; they are still cheap enough to keep in it, and they are the only
direct evidence that a greedy agent is runnable at all.
"""

import sys
import os

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))

from mtd_ai_run import (  # noqa: E402
    ACTION_SIZE,
    DEFAULT_GEOMETRY,
    build_agent,
    run_evaluation_episode,
    run_training_episode,
    seed_all,
)


def _small_geometry():
    geometry = dict(DEFAULT_GEOMETRY)
    geometry["total_nodes"] = 30
    return geometry


def _pin_policy_to(main_network, action):
    """Bias the output layer so argmax is `action` for every input."""
    layer = main_network.layers[-1]
    weights, bias = layer.get_weights()
    bias = np.zeros_like(bias)
    bias[action] = 1000.0
    layer.set_weights([np.zeros_like(weights), bias])


def test_a_greedy_no_op_policy_completes_and_advances_the_clock():
    """The direct proof of MTDAI-03: today this hangs.

    An agent that always answers "do nothing" is the degenerate case, and it has
    to be *runnable* before a no-op share means anything — an agent whose only
    reachable behaviour is deploying cannot be said to trade cost against risk.
    """
    seed_all(3)
    main_network, _ = build_agent()
    _pin_policy_to(main_network, 0)

    summary = run_evaluation_episode(
        main_network,
        finish_time=3000,
        mtd_interval=200,
        epsilon=0.0,                    # strictly greedy
        static_degrade_factor=1e9,      # the forced-deploy guard held off
        attacker_sensitivity=1.0,
        downtime_window=200.0,
        geometry=_small_geometry(),
    )

    assert summary["sim_time"] == pytest.approx(3000.0)
    assert summary["n_decisions"] > 0
    assert all(d["source"] == "greedy" for d in summary["decision_log"])
    assert summary["noop_share"] == pytest.approx(1.0)
    # A do-nothing policy mutates nothing, and therefore costs no availability.
    assert summary["n_mtd_executed"] == 0
    assert summary["downtime_ratio_final"] == 0.0


def test_the_no_op_consumes_one_trigger_interval():
    """Decision count is governed by the clock, not by the policy.

    This is what makes the no-op share comparable across the cost ladder: an
    agent that deploys on every decision and one that never does take the same
    number of decisions over the same horizon, so a change in the share is a
    change in the policy rather than in how often the agent was asked.
    """
    seed_all(3)
    always_noop, _ = build_agent()
    _pin_policy_to(always_noop, 0)
    seed_all(3)
    always_deploy, _ = build_agent()
    _pin_policy_to(always_deploy, 1)

    common = dict(finish_time=3000, mtd_interval=200, epsilon=0.0,
                  static_degrade_factor=1e9, attacker_sensitivity=1.0,
                  downtime_window=200.0, geometry=_small_geometry())

    noop_run = run_evaluation_episode(always_noop, **common)
    deploy_run = run_evaluation_episode(always_deploy, **common)

    horizon_decisions = 3000 / 200
    for summary in (noop_run, deploy_run):
        assert abs(summary["n_decisions"] - horizon_decisions) <= 5


def test_a_no_op_stores_a_transition_for_action_zero():
    """MTDAI-04: without this the Q-value of action 0 is never a TD target."""
    from collections import deque

    seed_all(5)
    main_network, target_network = build_agent()
    _pin_policy_to(main_network, 0)
    memory = deque(maxlen=2000)

    run_training_episode(
        main_network, target_network, memory,
        finish_time=3000, mtd_interval=200,
        epsilon=0.0, gamma=0.95, epsilon_min=0.01, epsilon_decay=1.0,
        batch_size=32, train_start=10 ** 9,   # store, never fit
        static_degrade_factor=1e9, attacker_sensitivity=1.0,
        downtime_lambda=0.0, downtime_window=200.0,
        geometry=_small_geometry(),
    )

    assert len(memory) > 0
    assert all(transition[2] == 0 for transition in memory)


def test_one_decision_registers_one_mutation():
    """MTDAI-08: two MTDs used to be enqueued per deploying decision."""
    seed_all(5)
    main_network, _ = build_agent()
    _pin_policy_to(main_network, 1)

    summary = run_evaluation_episode(
        main_network,
        finish_time=3000, mtd_interval=200, epsilon=0.0,
        static_degrade_factor=1e9, attacker_sensitivity=1.0,
        downtime_window=200.0, geometry=_small_geometry(),
    )

    deploying = sum(1 for d in summary["decision_log"] if d["action"] > 0)
    assert deploying > 0
    # Every deploying decision fires at most one mutation; a mutation can still
    # be suspended by resource occupation, so this is an upper bound, not an
    # equality.
    assert summary["n_mtd_executed"] <= deploying
    # A pinned single-mechanism policy can only ever produce that mechanism.
    assert set(summary["mutation_mix"]) <= {"CompleteTopologyShuffle"}


def test_the_action_space_covers_the_four_mechanisms_and_the_no_op():
    assert ACTION_SIZE == 5
