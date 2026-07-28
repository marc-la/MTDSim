"""The mapping is an input parameter — the end-to-end gate.

Two things are proven here that the loader tests cannot:

1. **A dwell-only place works end to end.** In a seeded run under the partial
   mapping, a dwell-only tactic advances simulated time, fires no verb, produces
   no verdict, routes on the base weights, and *says so* in the record. Without
   the last part an analysis cannot tell "spent time thinking" from "did nothing",
   and the action-budget decomposition that made experiment 1 legible would count
   dwell-only steps as failed actions.

2. **Selecting the mapping is a data selection.** The same profile, seed, and
   substrate under two registered mapping versions produce two different walks,
   and each is individually reproducible (SIM-05). That is what makes the mapping
   an experimental input rather than a property of the pipeline.
"""
from __future__ import annotations

import pytest

from mtdsim.l3_simulation.controller import load_controller
from mtdsim.l3_simulation.movement.attacker import ACTION_BEARING, DWELL_ONLY
from mtdsim.l3_simulation.movement.run import run_movement

HORIZON = 2500
SEED = 1234
PROFILE = "aggregate"


def _run(version: str, seed: int = SEED, mtd: str | None = None):
    return run_movement(
        PROFILE,
        seed=seed,
        with_synthetic_overlay=True,
        horizon=HORIZON,
        mapping_version=version,
        mtd_scheme=mtd,
        mtd_interval=150,
        register_for_interrupts=(mtd is not None),
    )


@pytest.fixture(scope="module")
def v2_run():
    return _run("v2_partial")


# --- (1) a dwell-only place, demonstrated end to end ------------------------


def test_dwell_only_places_are_actually_visited(v2_run) -> None:
    dwell_only = [r for r in v2_run.records if r.place_class == DWELL_ONLY]
    assert dwell_only, "the seeded walk never reached a dwell-only place"
    declared = set(load_controller(version="v2_partial").dwell_only_tactics)
    assert {r.place for r in dwell_only} <= declared


def test_a_dwell_only_step_consumes_time_and_dispatches_nothing(v2_run) -> None:
    """The whole definition, asserted on the record: time passes, no verb fires,
    no verdict is produced, and nothing is mistaken for a blocked action."""
    served = [
        r for r in v2_run.records if r.place_class == DWELL_ONLY and r.dwell > 0
    ]
    assert served, "no dwell-only place with a non-zero dwell was reached"
    for record in served:
        assert record.verb == ""
        assert record.verdict == ""
        assert record.outcome == "DWELL_ONLY"
        assert record.blocked is False
        assert record.end_time > record.start_time
        # The event occupied exactly its dwell — a dwell-only place adds no verb
        # time, because no verb ran.
        assert record.end_time - record.start_time == pytest.approx(record.dwell)


def test_the_walk_continues_through_a_dwell_only_place(v2_run) -> None:
    """Routing falls back to the base weights rather than stalling: a dwell-only
    place that is not a sink hands the token on."""
    onward = [
        r
        for r in v2_run.records
        if r.place_class == DWELL_ONLY and r.next_place is not None
    ]
    assert onward, "every dwell-only visit terminated the walk"


def test_mapped_places_are_unaffected(v2_run) -> None:
    """Action-bearing places still dispatch a verb and still produce a verdict."""
    acting = [r for r in v2_run.records if r.place_class == ACTION_BEARING]
    assert acting
    for record in acting:
        if record.outcome in {"SIM_END", "MAX_EVENTS"}:
            continue  # terminal records carry no verdict by design
        assert record.verb
        assert record.verdict in {"success", "failure"}


def test_version_1_produces_no_dwell_only_records() -> None:
    """Version 1 is total, so the new path must stay entirely dormant under it —
    which is why experiment 1's numbers are untouched by this change."""
    records = _run("v1_ckc_total").records
    assert records
    assert all(r.place_class == ACTION_BEARING for r in records)
    assert all(r.outcome != "DWELL_ONLY" for r in records)


def test_a_dwell_only_place_under_live_mtd_pays_but_does_not_route_on_it() -> None:
    """An MTD mutation during a dwell-only dwell is felt in cost, not in routing.

    No verb ran, so there is no substrate outcome for the verdict adapter to read
    and none is fabricated; the interrupt is still recorded, so the event is not
    invisible. (Overlay design §5 states this scope boundary.)
    """
    interrupted_dwells = []
    for seed in (1234, 7, 42, 99):
        records = _run("v2_partial", seed=seed, mtd="simultaneous").records
        interrupted_dwells += [
            r for r in records if r.place_class == DWELL_ONLY and r.interrupted
        ]
    if not interrupted_dwells:
        pytest.skip("no MTD mutation landed during a dwell-only dwell in these seeds")
    for record in interrupted_dwells:
        assert record.verdict == ""
        assert record.verb == ""


# --- (2) the mapping behaves as an experimental input -----------------------


def test_the_two_versions_produce_different_walks() -> None:
    """If swapping the mapping changed nothing observable, it would not be an
    experimental variable."""
    a = _run("v1_ckc_total").records
    b = _run("v2_partial").records
    assert [(r.place, r.verb) for r in a] != [(r.place, r.verb) for r in b]


@pytest.mark.parametrize("version", ["v1_ckc_total", "v2_partial"])
def test_determinism_holds_per_version(version: str) -> None:
    """SIM-05, per mapping version: same seed and same version, same walk."""
    assert _run(version).records == _run(version).records


def test_controller_and_mapping_version_together_are_a_contradiction() -> None:
    """The run seam takes the choice one way or the other, never ambiguously."""
    with pytest.raises(ValueError):
        run_movement(
            PROFILE,
            seed=SEED,
            horizon=HORIZON,
            controller=load_controller(version="v1_ckc_total"),
            mapping_version="v2_partial",
        )
