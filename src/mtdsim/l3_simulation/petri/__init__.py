"""L3a — OGASP structural Petri nets (the un-weighted MVP).

Four ordinary Petri nets, one per GASP class, built in SNAKES with a single
moving black token: **places = ATT&CK tactics**, **transitions = inter-tactic
GASP tactic-pairs** (each tracing to >=1 real technique-edge — the no-synthesis
invariant), **flow bipartite**, **marking = one token in reconnaissance (else
initial-access)**. Structural only — no rates, timing, weights, rewards, MTD or
CTMC (later stages of the workstream).

Design / feasibility: ``docs/implementation/pipeline/ogasp/petri_feasibility.md`` (sec.8:
the structural base is GO-unconditional). Build brief:
``docs/handoffs/2026-06-18_l3a_petri_mvp.md``. Outputs land under
``data/ogasp/petri/``. Entry point: ``PYTHONPATH=src python -m mtdsim.l3_simulation.petri``.
"""

from mtdsim.l3_simulation.petri.analysis import (
    OBJECTIVE_TACTICS,
    StructuralReport,
    analyse,
)
from mtdsim.l3_simulation.petri.build import (
    CLASS_NAMES,
    GapIndex,
    StructuralNet,
    TransitionSpec,
    build_all,
    build_structural_net,
    load_gap_index,
    load_gasp_view,
)

__all__ = [
    "CLASS_NAMES",
    "OBJECTIVE_TACTICS",
    "GapIndex",
    "StructuralNet",
    "StructuralReport",
    "TransitionSpec",
    "analyse",
    "build_all",
    "build_structural_net",
    "load_gap_index",
    "load_gasp_view",
]
