"""L3 controller sublayer — the tactic -> MTDSim-phase dispatch map.

The controller is the seam between the net (which tactic the attacker token
sits on) and the inherited substrate action set (which of the six MTDSim attack
verbs fires). It is a **CKC-mediated position map**, and — for this first
experiment — a deliberately simple, swappable **input parameter**, *not* a
recovered ground truth (see ``docs/implementation/pipeline/ogasp/controller.md``):

    MITRE ATT&CK tactic  --(ATT&CK->CKC crosswalk)-->  CKC phase
    MTDSim attack verb   --(Brown Fig-3 flow position)->  CKC phase
    tactic -> CKC -> the verb sharing that CKC phase (nearest covered on a gap)

Many tactics collapse onto one verb (1:M), and every one of the 15 tactics
resolves to exactly one of the 6 verbs — complete coverage by construction.

The mapping itself lives in ``data/ogasp/controller.csv``; this package loads
it and hands the resolved ``tactic -> sim_phase`` function to the (not-yet-
built) profiled attacker / movement layer.
"""

from mtdsim.l3_simulation.controller.controller import (
    SIM_PHASES,
    Controller,
    load_controller,
)
from mtdsim.l3_simulation.controller.outcome import (
    OutcomeOverlay,
    load_outcome_overlay,
)
from mtdsim.l3_simulation.controller.verdict import verdict_for

__all__ = [
    "SIM_PHASES",
    "Controller",
    "load_controller",
    # Success/failure outcome-overlay split + M2 composition (see outcome.py).
    "OutcomeOverlay",
    "load_outcome_overlay",
    # The per-verb verdict adapter (controller.md §4; see verdict.py).
    "verdict_for",
]
