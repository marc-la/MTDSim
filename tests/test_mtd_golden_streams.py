"""Movement-arm golden streams stay bit-identical — the cost-audit safety net.

`tools/mtd_golden_streams.py` captures per-mechanism golden behaviour streams
(movement records, MTD operation records, attack rows) under the cost-bench
configuration. This test re-runs a representative subset — one mechanism per
resource class, plus the mechanism that carries cross-mutation state — and
demands field-for-field equality with the committed goldens, so any defender-side
change that moves behaviour fails loudly rather than silently invalidating
published numbers.

The full 54-configuration sweep stays a tool concern
(``python tools/mtd_golden_streams.py check``); this subset keeps suite runtime
sane while still exercising every interrupt class the defender has.
"""
import gzip
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))

import mtd_golden_streams as gs  # noqa: E402

# One per resource class (network / application / reserve), plus the stateful
# mechanism whose checkpoint cache the re-instantiation fix restored. The
# retrace entries exercise the S5 policy's own golden set (sink-bearing
# profile, extended schema); the legacy entries pin the pre-retrace schema.
SUBSET = [
    ("IPShuffle", 0, True, False),
    ("ServiceDiversity", 0, True, False),
    ("UserShuffle", 0, True, False),
    ("OSDiversityAssignment", 0, True, False),
    ("no-mtd", 0, True, True),
    ("UserShuffle", 0, True, True),
    ("OSDiversityAssignment", 0, True, True),
]


@pytest.mark.parametrize(
    "mechanism,seed,arm,retrace",
    SUBSET,
    ids=[gs._config_name(m, s, a, r) for m, s, a, r in SUBSET],
)
def test_golden_stream_is_bit_identical(mechanism, seed, arm, retrace):
    cfg = gs._config_name(mechanism, seed, arm, retrace)
    path = gs.GOLDEN_DIR / f"{cfg}.json.gz"
    assert path.exists(), (
        f"golden missing: {path} — run `PYTHONPATH=src python "
        "tools/mtd_golden_streams.py capture`"
    )
    golden = json.loads(gzip.open(path).read())
    fresh = gs.one_golden_run(
        gs.MECHANISMS.get(mechanism), seed=seed, with_synthetic_overlay=arm,
        profile=(gs.RETRACE_PROFILE if retrace else gs.PROFILE),
        retrace_sinks=retrace,
    )
    fresh = json.loads(gs._canonical(fresh))
    assert gs._digest(golden) == gs._digest(fresh), gs._first_diff(golden, fresh)


def test_schema_follows_the_input():
    """The document's shape is a function of the run's declared inputs: legacy
    goldens carry the pre-retrace record shape, retrace goldens carry the field
    and a non-zero retrace count (a retrace set that never retraces guards
    nothing)."""
    legacy = json.loads(gzip.open(
        gs.GOLDEN_DIR / f"{gs._config_name('UserShuffle', 0, True)}.json.gz"
    ).read())
    assert "retrace" not in legacy["movement_records"][0]
    assert "retraces" not in legacy["summary"]
    assert "retrace_sinks" not in legacy["config"]

    retraced = json.loads(gzip.open(
        gs.GOLDEN_DIR / f"{gs._config_name('UserShuffle', 0, True, True)}.json.gz"
    ).read())
    assert "retrace" in retraced["movement_records"][0]
    assert retraced["config"]["retrace_sinks"] is True
    assert retraced["summary"]["retraces"] > 0
    assert sum(r["retrace"] for r in retraced["movement_records"]) \
        == retraced["summary"]["retraces"]
