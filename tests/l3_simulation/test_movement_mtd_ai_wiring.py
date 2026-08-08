"""The movement attacker against the reactive `mtd_ai` defender — the wiring.

This is the arm the axis-8 falsifier needs and which did not exist: the
`mtd_ai` driver builds the *inherited* adversary, so there was no configuration
in which the movement walk faced a defender that chooses rather than fires on a
timer. What is pinned here is the seam, not the defender's behaviour:

- a run under any other scheme carries an **empty** decision ledger, so the new
  field cannot quietly imply a decision was taken where none was;
- selecting `mtd_ai` without an agent fails **loudly**, rather than running with
  an untrained or absent policy and producing figures anyway;
- the action space and the feature head both come from one place, so a run
  cannot re-point action 1 at a different mechanism than the agent was trained
  to deploy — a silent mislabelling that no downstream figure would reveal;
- `decision_summary` separates the **greedy** share from the pooled one, which
  is the whole reason the ledger records a source at all: a pooled no-op share
  is floored by the exploration rate and would report the schedule rather than
  the policy.

TensorFlow is deliberately *not* imported here. The end-to-end run against a
built agent is exercised by hand and recorded in the axis-8 handoff §0.5; these
tests cover the wiring's own logic, and they stay fast enough to run always.
"""

import pytest

from mtdsim.l3_simulation.movement.run import MTDAIConfig, decision_snapshot
from mtdsim.l3_simulation.movement.statistics import MTDDecision, decision_summary


class _FakeOperation:
    """Stands in for ``MTDAIOperation``'s ledger surface only."""

    def __init__(self, log):
        self._log = log

    def get_decision_log(self):
        return self._log


def _result(decisions):
    """A MovementRunResult carrying just the field under test."""
    from mtdsim.l3_simulation.movement.statistics import MovementRunResult

    return MovementRunResult(
        profile="p",
        seed=0,
        with_synthetic_overlay=True,
        records=(),
        reached_objective=False,
        termination_time=0.0,
        compromised_count=0,
        mtd_decisions=decisions,
    )


def test_no_ledger_without_a_deciding_defender():
    """Timer-driven schemes take no decision, so the ledger must stay empty —
    not be absent, and not be fabricated from the executed mutations."""
    assert decision_snapshot(None) == ()
    assert decision_snapshot(object()) == ()


def test_ledger_is_snapshotted_verbatim():
    operation = _FakeOperation(
        [
            {"time": 200.1, "action": 0, "source": "greedy"},
            {"time": 400.2, "action": 3, "source": "random"},
        ]
    )
    snapshot = decision_snapshot(operation)
    assert snapshot == (
        MTDDecision(time=200.1, action=0, source="greedy"),
        MTDDecision(time=400.2, action=3, source="random"),
    )


def test_mtd_ai_scheme_without_an_agent_is_refused():
    """An absent policy must fail loudly. Running anyway would produce a
    mutation series that looks like a defender's choices and is not."""
    from mtdsim.l3_simulation.movement.run import _maybe_start_mtd

    with pytest.raises(ValueError, match="needs an MTDAIConfig"):
        _maybe_start_mtd(
            env=None,
            end_event=None,
            network=None,
            adversary=None,
            attack_op=None,
            scheme="mtd_ai",
            mtd_interval=200,
            custom_strategies=None,
            mtd_ai=None,
        )


def test_mtd_ai_config_on_a_timer_scheme_is_refused():
    """The config applies to one scheme; passing it with another means the run
    is not the run the caller thinks it is."""
    from mtdsim.l3_simulation.movement.run import _maybe_start_mtd

    with pytest.raises(ValueError, match="applies to"):
        _maybe_start_mtd(
            env=None,
            end_event=None,
            network=None,
            adversary=None,
            attack_op=None,
            scheme="simultaneously",
            mtd_interval=200,
            custom_strategies=None,
            mtd_ai=MTDAIConfig(main_network=object()),
        )


def test_config_defaults_to_a_greedy_policy():
    """Tay's harness never overrode ``epsilon=1.0``, so no published figure
    consulted the network. A run that asks what the policy does must default to
    asking the policy."""
    assert MTDAIConfig(main_network=object()).epsilon == 0.0


def test_summary_separates_the_greedy_share_from_the_pooled_one():
    decisions = (
        MTDDecision(time=1.0, action=0, source="greedy"),
        MTDDecision(time=2.0, action=2, source="greedy"),
        MTDDecision(time=3.0, action=0, source="random"),
        MTDDecision(time=4.0, action=1, source="forced"),
    )
    summary = decision_summary([_result(decisions)])

    assert summary["n_decisions"] == 4
    # Pooled: two no-ops in four decisions.
    assert summary["noop_share"] == pytest.approx(0.5)
    # Greedy: one no-op in the two decisions the policy actually made.
    assert summary["greedy_noop_share"] == pytest.approx(0.5)
    assert summary["n_greedy"] == 2
    assert summary["n_forced"] == 1
    assert summary["action_counts"] == {0: 2, 1: 1, 2: 1}


def test_summary_distinguishes_an_empty_ledger_from_an_inactive_defender():
    """A run set with no ledger at all is not a defender that chose to do
    nothing, and the summary must not report it as a no-op share of zero."""
    summary = decision_summary([_result(())])
    assert summary["n_runs"] == 1
    assert summary["n_runs_with_ledger"] == 0
    assert summary["greedy_noop_share"] != summary["greedy_noop_share"]  # NaN


def test_one_owner_for_the_action_space_and_the_feature_head():
    """The driver and the movement runner must read both from the same place;
    a divergence would silently relabel every action index."""
    from mtdnetwork.mtdai.mtd_ai import (
        CANONICAL_FEATURES,
        STATE_FEATURE_ORDER,
        TIME_FEATURE_ORDER,
        mtd_action_space,
    )

    assert [c.__name__ for c in mtd_action_space()] == [
        "CompleteTopologyShuffle",
        "IPShuffle",
        "OSDiversity",
        "ServiceDiversity",
    ]
    assert CANONICAL_FEATURES["static"] == STATE_FEATURE_ORDER
    assert CANONICAL_FEATURES["time"] == TIME_FEATURE_ORDER
