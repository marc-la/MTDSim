"""L3 controller sublayer — the tactic -> MTDSim-phase dispatch map.

The controller is the seam between the net (which tactic the attacker token
sits on) and the inherited substrate action set (which of the six MTDSim attack
verbs fires). It is a swappable **input parameter**, *not* a recovered ground
truth, and this package holds no experiment's mapping of its own: it reads
whichever version it is given.

**The mappings are data.** Every version that has been tried lives in
``data/ogasp/controller/mappings/``, one file per version plus a manifest
recording each version's rationale, what it produced, and which experiment
consumed it. Callers select by name — ``load_controller(version="v2_partial")``
— and an unqualified ``load_controller()`` takes the manifest's default, which is
the experiment-1 value so that an unqualified load reproduces what has always
run. The registered versions are:

    v1_ckc_total   experiment 1. A *total* map composed through the Cyber Kill
                   Chain: each verb owns one CKC phase by Brown's Fig-3 flow
                   position, each tactic takes the verb of its own or the nearest
                   covered phase. All 15 tactics onto exactly one of 6 verbs.
    v2_partial     experiment 2. A *partial* map decided per tactic against what
                   each verb actually does: 8 tactics dispatch a verb, 7 are
                   dwell-only (they consume time and dispatch nothing).

A tactic maps to [0, 1] verbs (supervisor ruling S4), so ``phase_for`` may return
``None``. Silence stays an error — a row with no verb must *declare* itself
dwell-only or the load raises.
"""

from mtdsim.l3_simulation.controller.controller import (
    DWELL_ONLY,
    MAPPED,
    SIM_PHASES,
    Controller,
    ControllerRow,
    MappingRegistry,
    MappingVersion,
    load_controller,
    load_registry,
)
from mtdsim.l3_simulation.controller.outcome import (
    OutcomeOverlay,
    load_outcome_overlay,
)
from mtdsim.l3_simulation.controller.verdict import verdict_for

__all__ = [
    "SIM_PHASES",
    "Controller",
    "ControllerRow",
    "load_controller",
    # The versioned mapping registry — mappings are data, selected by name.
    "MAPPED",
    "DWELL_ONLY",
    "MappingRegistry",
    "MappingVersion",
    "load_registry",
    # Success/failure outcome-overlay split + M2 composition (see outcome.py).
    "OutcomeOverlay",
    "load_outcome_overlay",
    # The per-verb verdict adapter (controller.md §4; see verdict.py).
    "verdict_for",
]
