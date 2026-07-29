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
# mechanism whose checkpoint cache the re-instantiation fix restored.
SUBSET = [
    ("IPShuffle", 0, True),
    ("ServiceDiversity", 0, True),
    ("UserShuffle", 0, True),
    ("OSDiversityAssignment", 0, True),
]


@pytest.mark.parametrize(
    "mechanism,seed,arm",
    SUBSET,
    ids=[f"{m}_seed{s}_{'overlay' if a else 'observed'}" for m, s, a in SUBSET],
)
def test_golden_stream_is_bit_identical(mechanism, seed, arm):
    cfg = gs._config_name(mechanism, seed, arm)
    path = gs.GOLDEN_DIR / f"{cfg}.json.gz"
    assert path.exists(), (
        f"golden missing: {path} — run `PYTHONPATH=src python "
        "tools/mtd_golden_streams.py capture`"
    )
    golden = json.loads(gzip.open(path).read())
    fresh = gs.one_golden_run(
        gs.MECHANISMS[mechanism], seed=seed, with_synthetic_overlay=arm
    )
    fresh = json.loads(gs._canonical(fresh))
    assert gs._digest(golden) == gs._digest(fresh), gs._first_diff(golden, fresh)
