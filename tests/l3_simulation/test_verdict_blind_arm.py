"""The verdict-blind ablation arm — pinned as a genuine null.

The control criterion axis 4 has always lacked. Every run on record has had the
adaptive loop switched on, so nothing separates *the loop operates* (which is
evidenced) from *the loop helps* (which is not). The blind arm switches it off
without switching anything else off: it is an empty value table, so the token
still walks the net, still dispatches verbs and still reads verdicts — the
verdicts simply have no consequence for where it goes next.

The whole value of the arm is that it is **exactly** the base weights and not a
subtly different policy, so that is what these tests assert — at every place of
every profile net, under every verdict, and end to end on a live run.

Pre-registration: docs/implementation/pipeline/ogasp/demonstration_arms_prereg.md.
"""
from __future__ import annotations

import dataclasses

import pytest

from mtdsim.l3_simulation.controller import (
    VERDICT_BLIND,
    load_outcome_overlay,
    verdict_blind_overlay,
)
from mtdsim.l3_simulation.movement.attacker import VERDICT_NONE
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net
from mtdsim.l3_simulation.movement.run import run_movement

VERDICTS = ("success", "failure", VERDICT_NONE)
SEEDS = (0, 7, 42, 1234)


def _renormalised(weights):
    total = sum(w for w in weights.values() if w > 0)
    return {d: w / total for d, w in weights.items() if w > 0}


# --- 1. the identity, at every place of every net ---------------------------


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("overlay_on", (True, False))
def test_blind_composition_is_the_base_weights_renormalised(profile, overlay_on) -> None:
    """The load-bearing assertion. At every place, under every verdict, the
    blind arm's composed distribution equals the base out-weights renormalised —
    which is what a *hypothetical no-overlay run* would sample."""
    net = load_routing_net(profile, with_synthetic_overlay=overlay_on)
    blind = verdict_blind_overlay()
    for place in net.places:
        base = net.base_out_weights(place)
        if not base:
            continue  # a sink has nothing to compose
        expected = _renormalised(base)
        for verdict in VERDICTS:
            assert blind.compose(place, verdict, dict(base)) == pytest.approx(expected)


@pytest.mark.parametrize("profile", PROFILES)
def test_the_verdict_makes_no_difference_under_the_blind_arm(profile) -> None:
    """Stated the other way round, because this is the property the ablation
    *means*: success and failure produce the same distribution, so the
    substrate's verdict cannot steer the token."""
    net = load_routing_net(profile, with_synthetic_overlay=True)
    blind = verdict_blind_overlay()
    for place in net.places:
        base = net.base_out_weights(place)
        if not base:
            continue
        distributions = [blind.compose(place, v, dict(base)) for v in VERDICTS]
        assert all(d == distributions[0] for d in distributions)


def test_the_conditioned_arm_is_not_the_blind_arm() -> None:
    """The contrast is only worth running if the arms differ somewhere. Asserted
    so that a future overlay change collapsing the two would fail loudly here
    rather than silently turning the experiment into a comparison of a thing
    with itself."""
    net = load_routing_net("aggregate", with_synthetic_overlay=True)
    blind = verdict_blind_overlay()
    conditioned = load_outcome_overlay(version="v3_persistent_backward")
    differences = 0
    for place in net.places:
        base = net.base_out_weights(place)
        if not base:
            continue
        for verdict in ("success", "failure"):
            if blind.compose(place, verdict, dict(base)) != conditioned.compose(
                place, verdict, dict(base)
            ):
                differences += 1
    assert differences > 0


# --- 2. the arm carries no values and writes nothing ------------------------


def test_the_blind_arm_is_an_empty_table_not_a_code_path() -> None:
    """Built as data, so the two arms run the same code down the same path and
    differ only in what they read. An arm implemented as a driver branch would
    make the contrast two-factor."""
    blind = verdict_blind_overlay()
    assert blind.by_verdict == {}
    assert blind.by_rule == {}
    assert blind.version == VERDICT_BLIND
    # Absent everywhere, so `value` reports the miss rather than inventing one.
    assert blind.value("failure", "execution", "impact") == 0.0
    assert blind.out_values("failure", "execution") == {}


def test_the_blind_arm_is_not_registered() -> None:
    """It stays an in-memory arm until a published run consumes it — the
    registry's own rule is that a version becomes immutable at that point, and
    registering it earlier would bind a version nothing had run."""
    from mtdsim.l3_simulation.controller.outcome import load_overlay_registry

    assert VERDICT_BLIND not in load_overlay_registry().names


# --- 3. end to end on a live run --------------------------------------------


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("seed", SEEDS)
def test_a_blind_run_equals_a_run_with_no_overlay_at_all(profile, seed) -> None:
    """The end-to-end form of the identity: driving a run with the blind arm
    produces the same record stream, field for field, as driving it with an
    overlay object that carries no values by another construction. If the two
    ever diverged, the blind arm would be doing something of its own."""

    class _NoOverlay:
        """Composes by renormalising the base weights and nothing else."""

        def compose(self, src, verdict, base_out_weights):
            return _renormalised(base_out_weights)

    kwargs = dict(
        seed=seed,
        horizon=3_000,
        mapping_version="v2_partial",
        mtd_scheme=None,
        retrace_sinks=True,
    )
    blind = run_movement(profile, overlay=verdict_blind_overlay(), **kwargs)
    none_at_all = run_movement(profile, overlay=_NoOverlay(), **kwargs)
    assert [dataclasses.asdict(r) for r in blind.records] == [
        dataclasses.asdict(r) for r in none_at_all.records
    ]


@pytest.mark.parametrize("profile", PROFILES)
def test_the_blind_arm_still_dispatches_and_still_reads_verdicts(profile) -> None:
    """The ablation removes the verdict's *consequence*, not the verdict. An arm
    that stopped dispatching, or stopped reading outcomes, would be a different
    attacker rather than the same attacker with its loop off — and the
    H-coupling finding must stay reportable at this arm."""
    run = run_movement(
        profile,
        seed=0,
        horizon=15_000,
        mapping_version="v2_partial",
        mtd_scheme=None,
        retrace_sinks=True,
        overlay=verdict_blind_overlay(),
    )
    assert any(r.verb for r in run.records)
    assert any(r.verdict in ("success", "failure") for r in run.records)


# --- 4. the seam the experiment names its inputs at -------------------------


def test_overlay_version_and_overlay_object_are_exclusive() -> None:
    """Naming a version and passing an object are two ways to say the same
    thing, and saying both is a contradiction rather than a precedence puzzle —
    the same contract `controller` / `mapping_version` already has."""
    with pytest.raises(ValueError):
        run_movement(
            "aggregate",
            overlay=verdict_blind_overlay(),
            overlay_version="v3_persistent_backward",
        )


def test_naming_the_overlay_version_matches_loading_it() -> None:
    """The new parameter is wiring, not policy: naming a version must give the
    same run as constructing that version and passing it."""
    kwargs = dict(seed=0, horizon=3_000, mapping_version="v2_partial", mtd_scheme=None)
    named = run_movement("aggregate", overlay_version="v3_persistent_backward", **kwargs)
    passed = run_movement(
        "aggregate",
        overlay=load_outcome_overlay(version="v3_persistent_backward"),
        **kwargs,
    )
    assert [dataclasses.asdict(r) for r in named.records] == [
        dataclasses.asdict(r) for r in passed.records
    ]
