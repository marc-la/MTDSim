"""Pin the L2 structural baseline the dissertation cites (§4.2.2).

The numbers, their definitions and the record are in
``tools/gasp_structural_baseline.py`` and
``docs/implementation/pipeline/gasp/structural_baseline.md``. This test fails
if the audit CSV's descriptive structural columns stop reproducing from the
flow YAMLs under the L1 contraction, or if any pinned number moves.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import gasp_structural_baseline as sb  # noqa: E402


def test_pinned_numbers_reproduce_from_flows_and_csv() -> None:
    assert sb.main(check=True) == 0


def test_terminal_read_is_the_l1_contraction_and_matches_csv_per_flow() -> None:
    rows = list(csv.DictReader(open(sb.AUDIT)))
    assert len(rows) == 38
    for r in rows:
        flow = sb.load_flow(r["flow_id"])
        read, techs, tacs = sb.read_terminal(flow)
        assert techs == sorted(x for x in r["terminal_techniques"].split(";") if x), r["flow_id"]
        assert tacs == sorted(x for x in r["terminal_tactics"].split(";") if x), r["flow_id"]


def test_the_two_concordance_rules_give_15_and_19() -> None:
    rows = list(csv.DictReader(open(sb.AUDIT)))
    exact = anyov = 0
    split: Counter[str] = Counter()
    for r in rows:
        read = sb.objective_read(set(x for x in r["terminal_tactics"].split(";") if x))
        split[read] += 1
        e, o = sb.concordance(read, r["stated_objective"])
        exact += not e
        anyov += not o
    assert dict(split) == {"exfil": 7, "impact": 11, "both": 1, "neither": 19}
    assert (exact, anyov) == (19, 15)


def test_confidence_tally_after_2026_08_17_rulings() -> None:
    """Round 2 re-audit (35 / 1 / 2) followed by Marc's three membership rulings
    the same day: mac -> exfiltration_impact (high), alt -> exfiltration (medium
    until Marc read the advisory, then high), searchawesome -> none_c2 (high)."""
    rows = list(csv.DictReader(open(sb.AUDIT)))
    tally = Counter(r["metadata_confidence"] for r in rows)
    assert dict(tally) == {"high": 38}
    classes = Counter(r["stated_objective"] for r in rows)
    assert dict(classes) == {"steal_data": 19, "impediment": 7, "double_extortion": 7, "position_for_future": 5}
