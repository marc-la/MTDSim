"""Tests for the downtime / operational-impact metric.

The metric is this project's construction of Tay's T-TS-02 — a time-series
input his §4.1.2 names and nothing in the inherited code implements, in any
form. The paper supplies no definition, so the definition is ours and is
defended in ``MTDStatistics.downtime_ratio`` and in the rebuild record. These
tests pin the properties that argument leans on:

- **Overlap accounting, not event counting.** The reading is availability lost
  over a trailing window, so a mutation half inside the window is charged half.
  This is what distinguishes it from a per-mechanism weighted count and what
  makes it compose with the substrate's resource seizure.
- **Concurrency survives.** Two mutations on different resource layers running
  at once are charged twice, which is the structure the ``simpy.Resource``
  seizure already models and which a count would discard.
- **In-flight mutations are charged.** Execution records are written only at
  finish, so a reading taken mid-execution would otherwise report a quiet
  network while the network is down — precisely the state the agent needs to
  see.

Nothing here pins a *magnitude* on a real run: the window is a declared
parameter that the calibration ladder sweeps, and pinning a value would freeze
a declared choice as if it were lineage.
"""

import pytest

from mtdnetwork.statistic.mtd_statistics import MTDStatistics


class _FakeMTD:
    def __init__(self, name, priority, resource_type="network"):
        self._name = name
        self._priority = priority
        self._resource_type = resource_type

    def get_name(self):
        return self._name

    def get_priority(self):
        return self._priority

    def get_resource_type(self):
        return self._resource_type


def _stats_with(records):
    stats = MTDStatistics()
    for name, priority, start, finish in records:
        mtd = _FakeMTD(name, priority)
        stats.mark_mtd_started(mtd, start)
        stats.append_mtd_operation_record(mtd, start, finish, finish - start)
    return stats


def test_downtime_ratio_is_zero_with_no_mutations():
    assert MTDStatistics().downtime_ratio(now=1000, window=200) == 0.0


def test_downtime_ratio_charges_a_fully_contained_mutation_in_full():
    stats = _stats_with([("IPShuffle", 1, 900, 1000)])
    # 100 s of a 200 s window.
    assert stats.downtime_ratio(now=1000, window=200) == pytest.approx(0.5)


def test_downtime_ratio_charges_only_the_overlap_of_a_straddling_mutation():
    # Runs 700 -> 900; the window is [800, 1000], so 100 of its 200 s land.
    stats = _stats_with([("CompleteTopologyShuffle", 0, 700, 900)])
    assert stats.downtime_ratio(now=1000, window=200) == pytest.approx(0.5)


def test_downtime_ratio_ignores_mutations_wholly_outside_the_window():
    stats = _stats_with([("IPShuffle", 1, 100, 200)])
    assert stats.downtime_ratio(now=1000, window=200) == 0.0


def test_downtime_ratio_adds_concurrent_mutations_on_separate_layers():
    """Two layers busy at once is twice the operational impact of one.

    This is the property that rules out a weighted event count: the substrate
    already models one mechanism blocking another through resource seizure, and
    the measure has to carry that structure rather than flatten it.
    """
    stats = _stats_with([
        ("IPShuffle", 1, 900, 1000),           # network layer
        ("ServiceDiversity", 3, 900, 1000),    # application layer
    ])
    assert stats.downtime_ratio(now=1000, window=200) == pytest.approx(1.0)


def test_downtime_ratio_charges_a_mutation_still_in_flight():
    """A record is written at finish, so without this the metric reads 0
    exactly while the network is down."""
    stats = MTDStatistics()
    stats.mark_mtd_started(_FakeMTD("OSDiversity", 2, "application"), 950)
    assert stats.downtime_ratio(now=1000, window=200) == pytest.approx(0.25)


def test_finishing_a_mutation_does_not_double_charge_it():
    mtd = _FakeMTD("OSDiversity", 2, "application")
    stats = MTDStatistics()
    stats.mark_mtd_started(mtd, 900)
    stats.append_mtd_operation_record(mtd, 900, 1000, 100)
    assert stats.downtime_ratio(now=1000, window=200) == pytest.approx(0.5)


def test_downtime_ratio_is_bounded_by_the_number_of_busy_layers():
    """Bounded in [0, n_layers] rather than growing with the horizon — the
    property that keeps it conditioned alongside the vector's other ratios."""
    stats = _stats_with([
        ("IPShuffle", 1, 0, 1000),
        ("ServiceDiversity", 3, 0, 1000),
    ])
    assert stats.downtime_ratio(now=1000, window=200) == pytest.approx(2.0)

