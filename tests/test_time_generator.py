"""The timing-regime seam (D-08 ruling, 2026-08-13).

`exponential_variates` carries two declared regimes:

- 'shifted' (default) — the inherited baseline, `loc + Exp(scale)`. Every
  golden and every recorded figure was produced under it, so the default must
  stay bit-identical to the pre-seam wrapper.
- 'exponential' — a true exponential whose MEAN is the nominal value
  (`Exp(mean)`, sigma = mean, memoryless), Zhang §4.5's µ-as-mean reading,
  opted into per run (`run_baseline.py --timing-regime` /
  `trace.py --timing-regime` / `set_exponential_regime`).

These tests pin the seam's three load-bearing properties: the default is the
shifted construction byte-for-byte; the opt-in regime has exponential moments
about the nominal mean; and both regimes consume exactly one variate per
call, so switching never desynchronises the seeded numpy stream shared with
every other draw site.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from scipy.stats import expon

from mtdnetwork.component.time_generator import (
    exponential_variates,
    get_exponential_regime,
    set_exponential_regime,
)


@pytest.fixture(autouse=True)
def _restore_regime():
    """No test may leak a regime into the rest of the suite."""
    yield
    set_exponential_regime("shifted")


def test_default_regime_is_shifted():
    assert get_exponential_regime() == "shifted"


def test_shifted_default_is_bit_identical_to_the_inherited_wrapper():
    np.random.seed(42)
    ours = [exponential_variates(200, 0.5) for _ in range(50)]
    np.random.seed(42)
    inherited = [expon.rvs(loc=200, scale=0.5, size=1)[0] for _ in range(50)]
    assert ours == inherited
    # And the construction is what the audit says it is: loc-shifted, tiny jitter.
    assert all(200 <= v for v in ours)
    assert max(ours) - 200 < 10


def test_exponential_regime_mean_is_the_nominal_value():
    set_exponential_regime("exponential")
    np.random.seed(7)
    draws = np.array([exponential_variates(200, 0.5) for _ in range(20000)])
    assert abs(draws.mean() - 200) / 200 < 0.03      # mean ~= µ, not µ + 0.5
    assert abs(draws.std() - 200) / 200 < 0.05       # sigma ~= µ (exponential)
    assert (draws < 200).mean() > 0.5                # not loc-shifted: mass below µ
    assert draws.min() < 20                          # short intervals genuinely occur


def test_both_regimes_consume_one_variate_per_call():
    np.random.seed(1234)
    exponential_variates(200, 0.5)
    after_shifted = np.random.random()

    np.random.seed(1234)
    set_exponential_regime("exponential")
    exponential_variates(200, 0.5)
    after_exponential = np.random.random()

    assert after_shifted == after_exponential


def test_regime_setter_round_trips_and_rejects_unknowns():
    set_exponential_regime("exponential")
    assert get_exponential_regime() == "exponential"
    set_exponential_regime("shifted")
    assert get_exponential_regime() == "shifted"
    with pytest.raises(ValueError):
        set_exponential_regime("memoryless")
    assert get_exponential_regime() == "shifted"
