"""L3 movement layer — the graph-driven attacker that walks a class net live
inside MTDSim, alongside the inherited 6-phase attacker.

The token walks the tactic-place net; at each place the controller dispatches one
MTDSim verb through the carved substrate action surface, the substrate returns the
verb's outcome, the verdict adapter reads it as success/failure, and the outcome
overlay routes the token's next transition — the net supplies movement, the
substrate supplies outcome (M4). Build brief:
``docs/handoffs/2026-07-22_l3_attacker_petri_to_mtdsim.md``.

Pieces:
- :mod:`~mtdsim.l3_simulation.movement.net` — the routing net (base out-weights per
  place: observed D3 weights composed with the M6 synthetic overlay; schema-pinned).
- :mod:`~mtdsim.l3_simulation.movement.attacker` — :class:`MovementAttacker`, the
  live SimPy net-walker, and the per-event :class:`MovementRecord`.
- :mod:`~mtdsim.l3_simulation.movement.timing` — the per-tactic timing source: the
  declared catalogue duration read as the mean of an exponential firing time (S3).
  The movement layer supplies the time; the SimPy loop spends it.
- :mod:`~mtdsim.l3_simulation.movement.statistics` — a reader over the records
  (MTTC / ASR per profile); the inherited attack-stats maths is untouched.
- :mod:`~mtdsim.l3_simulation.movement.run` — run wiring (attacker selected
  alongside the native one; D8 arms; the controller library injected).
"""

from mtdsim.l3_simulation.movement.attacker import (
    MovementAttacker,
    MovementRecord,
    load_dwell_catalogue,
)
from mtdsim.l3_simulation.movement.net import (
    PROFILES,
    NetSchemaError,
    RoutingNet,
    load_routing_net,
)
from mtdsim.l3_simulation.movement.run import run_movement, run_smoke_matrix
from mtdsim.l3_simulation.movement.statistics import (
    MovementRunResult,
    ProfileSummary,
    summarise,
    summarise_profile,
)
from mtdsim.l3_simulation.movement.timing import (
    ConstantTiming,
    TacticTiming,
    TimingSource,
)

__all__ = [
    "PROFILES",
    "NetSchemaError",
    "RoutingNet",
    "load_routing_net",
    "MovementAttacker",
    "MovementRecord",
    "load_dwell_catalogue",
    "ConstantTiming",
    "TacticTiming",
    "TimingSource",
    "MovementRunResult",
    "ProfileSummary",
    "summarise",
    "summarise_profile",
    "run_movement",
    "run_smoke_matrix",
]
