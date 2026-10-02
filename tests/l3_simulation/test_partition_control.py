"""Validation gate of the label-blind partition control
(``mtdsim.l3_simulation.petri.partition_control``).

1. Fed the real partition (``classification.csv``), the builder reproduces the
   committed ``data/ogasp/petri/`` nets and synthetic overlay byte for byte.
2. A real profile run through ``petri_dir`` is bit-identical to the default
   path (records, hosts, termination time).
3. The random partitions are fixed by their seed and have the profiles' sizes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from mtdsim.l3_simulation.petri.build import load_gasp_view
from mtdsim.l3_simulation.petri.partition_control import (
    SLOTS,
    build_petri_dir,
    random_partitions,
    real_assignment,
    slot_sizes,
)

PETRI = Path(__file__).resolve().parents[2] / "data" / "ogasp" / "petri"
FILES = [f"{p}_structural.json" for p in SLOTS + ("aggregate",)] + ["synthetic_overlay.json"]


def _build_real(tmp_path_factory, guard: str) -> Path:
    committed = json.loads((PETRI / "aggregate_structural.json").read_text())
    out = tmp_path_factory.mktemp(f"petri_real_{guard}")
    build_petri_dir(
        real_assignment(), out, include_aggregate=True, label_blind=False,
        build_date=committed["provenance"]["build_date"], guard=guard,
    )
    return out


@pytest.fixture(scope="module")
def real_dir(tmp_path_factory) -> Path:
    return _build_real(tmp_path_factory, "structural")


@pytest.fixture(scope="module")
def real_dir_weighted(tmp_path_factory) -> Path:
    return _build_real(tmp_path_factory, "weighted")


@pytest.mark.parametrize("name", FILES)
def test_real_partition_reproduces_committed_bytes(real_dir, name):
    assert (real_dir / name).read_bytes() == (PETRI / name).read_bytes()


@pytest.mark.parametrize("name", FILES)
def test_weighted_guard_is_a_no_op_on_the_real_profiles(real_dir_weighted, name):
    """The generalised guard changes nothing the committed rule built."""
    assert (real_dir_weighted / name).read_bytes() == (PETRI / name).read_bytes()


@pytest.mark.parametrize("slot", SLOTS)
def test_group_view_equals_committed_gasp_view(slot):
    from mtdsim.l2_subgraph.selector import OperationalObjectiveSelector
    from mtdsim.l3_simulation.petri.partition_control import _load_gap

    flows = real_assignment()[slot]
    view = OperationalObjectiveSelector(slot).select(_load_gap(), {f: slot for f in flows})
    committed = load_gasp_view(slot)
    assert view.node_set == committed.node_set
    assert view.edge_set == committed.edge_set


def test_random_partitions_fixed_and_sized():
    a, b = random_partitions(), random_partitions()
    assert a == b
    sizes = slot_sizes()
    assert sizes == {SLOTS[0]: 19, SLOTS[1]: 7, SLOTS[2]: 7, SLOTS[3]: 5}
    flows = sorted(f for fs in real_assignment().values() for f in fs)
    for part in a:
        assert {s: len(fs) for s, fs in part.items()} == sizes
        assert sorted(f for fs in part.values() for f in fs) == flows


def _summary(r):
    return (r.termination_time, r.compromised_count, r.reached_objective,
            r.database_hosts_reached, r.retrace_count, tuple(r.target_hosts),
            tuple(r.records), tuple(r.mtd_executions))


@pytest.mark.parametrize(
    "seed", [0, pytest.param(1, marks=pytest.mark.slow), pytest.param(2, marks=pytest.mark.slow)]
)
def test_petri_dir_run_is_bit_identical(real_dir, seed):
    from mtdnetwork.mtd.ipshuffle import IPShuffle
    from mtdsim.l3_simulation.movement.run import run_movement

    kw = dict(seed=seed, with_synthetic_overlay=True, horizon=15_000,
              mapping_version="v2_partial", overlay_version="v4_failure_only",
              retrace_sinks=True, mtd_scheme="single", mtd_interval=200,
              custom_strategies=IPShuffle, attack_objective="targeted",
              target_layer=None, exploit_learning_rate=2.0)
    for profile in ("objective_impact", "objective_none_c2"):
        default = run_movement(profile, **kw)
        via_dir = run_movement(profile, petri_dir=real_dir, **kw)
        assert _summary(default) == _summary(via_dir)


# --- the committed partitions ---------------------------------------------

CONTROL = PETRI.parent / "partition_control"


def _manifest() -> dict:
    return json.loads((CONTROL / "partitions.json").read_text())


def test_committed_partitions_are_the_seeded_draws_that_pass():
    from itertools import islice

    from mtdsim.l3_simulation.petri.partition_control import partition_stream

    m = _manifest()
    draws = list(islice(partition_stream(m["partition_seed"]), m["draws_taken"]))
    kept = [p["draw"] for p in m["partitions"]]
    assert sorted(kept + [r["draw"] for r in m["rejected"]]) == list(range(m["draws_taken"]))
    for p in m["partitions"]:
        for slot, g in p["groups"].items():
            assert tuple(g["flow_ids"]) == draws[p["draw"]][slot]


@pytest.mark.parametrize("i", range(10))
def test_committed_partition_rebuilds_byte_identical_and_runs(tmp_path, i):
    from mtdsim.l3_simulation.petri.partition_control import token_reaches_initial_access

    m = _manifest()
    p = m["partitions"][i]
    d = PETRI.parents[2] / p["petri_dir"]
    first = json.loads((d / f"{SLOTS[0]}_structural.json").read_text())
    build_petri_dir(
        {slot: g["flow_ids"] for slot, g in p["groups"].items()}, tmp_path,
        guard=m["guard"]["used"], build_date=first["provenance"]["build_date"],
        provenance={k: first["partition_control"][k]
                    for k in ("partition", "draw", "partition_seed", "guard")},
    )
    for name in [f"{s}_structural.json" for s in SLOTS] + ["synthetic_overlay.json"]:
        assert (tmp_path / name).read_bytes() == (d / name).read_bytes(), name
    assert all(token_reaches_initial_access(d, s) for s in SLOTS)
