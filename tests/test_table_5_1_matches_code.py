"""Table 5.1 (the experimental setup) states the values the runners use.

The table is typed in the dissertation; this test reads the runners' own
constants so the two cannot drift apart unnoticed.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TABLE = REPO / "docs" / "thesis" / "tables" / "tab_5-1a_experiment.tex"


def _load(rel: str):
    path = REPO / rel
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(f"t51_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


corpus = _load("experiments/ch5_defended/run_corpus.py")
memory = _load("experiments/ch5_defended/run_memory_ablation.py")
table = TABLE.read_text()


def test_deployment_intervals():
    assert sorted(corpus.INTERVALS + corpus.SWEEP_INTERVALS) == [50, 100, 200, 500, 1000, 2000]
    assert "50, 100 and 200\\,s" in table and "500, 1\\,000 and 2\\,000\\,s" in table


def test_mtd_conditions():
    singles = [c for c in corpus.DEFENDED if corpus.CONDITIONS[c][0] == "single"]
    assert len(singles) == 7 and "seven MTD mechanisms" in table
    assert {"random", "alternative"} <= set(corpus.DEFENDED)
    assert "mtdshield" in corpus.SHIELD


def test_seeds_horizon_and_scenario():
    jobs = corpus.build_reported_jobs()
    assert corpus.REPORTED_SEEDS == 1000 and {j["seed"] for j in jobs} == set(range(1000))
    assert "1\\,000" in table and "seeds 0 to 999" in table
    assert corpus.HORIZON == 15_000 and "15\\,000\\,s" in table
    assert {j["objective"] for j in jobs} == {"targeted"} and "targeted" in table


def test_network():
    from mtdnetwork.data.constants import SERVICE_NO_OF_SERVICES_PER_OS
    from mtdsim.l3_simulation.movement.run import GEOMETRY

    assert (GEOMETRY["total_nodes"], GEOMETRY["total_layers"], GEOMETRY["total_subnets"],
            GEOMETRY["total_endpoints"]) == (50, 4, 8, 5)
    assert "50 hosts, 4 levels of depth, 8 subnets, 5 exposed endpoints" in table
    assert GEOMETRY["total_database"] == 2 and GEOMETRY["target_layer"] == GEOMETRY["total_layers"]
    assert "2, at the deepest level" in table
    assert SERVICE_NO_OF_SERVICES_PER_OS == 20 and "20 services per operating system" in table


def test_ablations():
    from mtdsim.l3_simulation.petri.partition_control import K

    assert K == 10 and "10 random partitions" in table
    assert set(corpus.SPANNING) == {"ip_shuffle", "os_diversity"}
    assert memory.POOLS == (1, 2, 3, 5, 10, 20) and "1, 2, 3, 5, 10 and 20 services" in table
    assert memory.CONDITIONS == (("none", 0), ("service_diversity", 200), ("os_diversity", 200))
