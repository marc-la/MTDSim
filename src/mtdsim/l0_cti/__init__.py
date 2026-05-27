"""L0 — raw CTI acquisition (Attack Flow corpus + ATT&CK Enterprise STIX).

Stage L0 of the L0->L4 contribution pipeline: materialise the gitignored
upstream inputs that L1 (:mod:`mtdsim.l1_construction`) consumes. See this
package's ``README.md`` and ``docs/specs/architecture.md`` §(c).

Run as a module::

    PYTHONPATH=src python -m mtdsim.l0_cti [--force]
"""

from mtdsim.l0_cti.fetch import fetch_corpus

__all__ = ["fetch_corpus"]
