"""Shared pytest configuration — the suite's cost control, in one place.

Two things live here, and both exist for the same reason: **the null-equivalence
tests are the most valuable tests in this repository and the most expensive
ones, and those two facts had started to fight each other.**

Every modulator family this project has added — the bare attacker state, the
utility modulator, the learning belief, the readiness re-key, the alignment
factor, the succession dial — carries the same load-bearing guarantee: *at its
null parameter the run is bit-identical to a run without the mechanism at all*.
That guarantee is what makes each family's ablation exact rather than
approximate, and every axis badge earned against a modulator-null arm rests on
it. Each family therefore pinned it as a test over the same grid — 5 profiles x
2 mappings x 5 seeds x 2 MTD conditions, two simulations per cell.

Six families later that is roughly 1 200 simulations per suite run, and it is
the arithmetic rather than any one test that is the problem: the grids are
identical, so the same un-modulated baseline run is computed once per family
and discarded.

Measured before the change: **728 tests in 503 s**, of which the slowest 25
durations were, without exception, cells of these six grids (5.5-7.3 s each).

Neither fix below weakens a guarantee.

1. ``baseline_run`` memoises the un-modulated half of every null-equivalence
   comparison for the session. The runs are deterministic by construction —
   ``run_movement`` reseeds both global streams from its ``seed`` argument
   before it does anything else — and ``MovementRunResult`` is frozen, so a
   cached result and a fresh one are indistinguishable. The six families now
   share one set of baseline runs instead of computing six.

2. The ``slow`` marker deselects the **exhaustive** seed grid by default while
   keeping a full profile x mapping x MTD-condition slice running on every
   invocation. The complete grid is one flag away (``--runslow``) and belongs in
   the pre-re-baseline gate, which is where it was always doing its real work: a
   full-grid failure is a claim-integrity failure, not a routine regression.

The distinction the marker encodes is deliberate. What varies across seeds in
these tests is *only which walk is sampled*, and the assertion is the same
identity at every one of them; what varies across profiles and mappings is the
structure being exercised. So the seed axis is the one that can be sliced
without losing a kind of coverage, and it is the only one sliced.
"""
from __future__ import annotations

from typing import Any, Callable

import pytest


# --- the slow marker --------------------------------------------------------
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--runslow",
        action="store_true",
        default=False,
        help=(
            "also run the exhaustive seed grids of the null-equivalence tests. "
            "Required before any deliberate re-baseline."
        ),
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "slow: a cell of an exhaustive seed grid. Deselected unless --runslow "
        "is given; the same assertion still runs at the leading seed.",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    if config.getoption("--runslow"):
        return
    skip = pytest.mark.skip(
        reason="exhaustive seed grid; the same assertion ran at the leading "
        "seed. Use --runslow for the full grid."
    )
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip)


# --- the shared baseline runs ----------------------------------------------
@pytest.fixture(scope="session")
def baseline_run() -> Callable[..., Any]:
    """A memoised ``run_movement`` for the **un-modulated** half of a
    null-equivalence comparison — the run every such test compares its null arm
    against.

    Use it *only* for that: the run with no ``attacker_state``, which is
    identical across the six families and therefore worth computing once. A run
    that carries a modulator is a different run per family and is not cached.

    Safe to share because the result is frozen and the call is a pure function
    of its arguments — the global streams are reseeded on entry to
    ``run_movement``, so nothing a previous call left behind can reach this one.
    """
    from mtdsim.l3_simulation.movement.run import run_movement

    cache: dict[tuple, Any] = {}

    def run(profile: str, **kwargs: Any) -> Any:
        assert "attacker_state" not in kwargs, (
            "baseline_run is for the un-modulated arm only; a run carrying a "
            "modulator differs per family and must not be cached"
        )
        key = (profile,) + tuple(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = run_movement(profile, **kwargs)
        return cache[key]

    return run
