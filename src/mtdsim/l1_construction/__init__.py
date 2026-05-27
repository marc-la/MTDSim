"""Generalised APT Profile (GAP) — L1 of the L0->L4 pipeline.

A lossless, Attack-Flow-only technique-dependency graph aggregated from the
MITRE CTID Attack Flow corpus. See ``docs/specs/01_gap_schema.md`` for the data
model and the four design decisions this implements.

Typical use::

    from mtdsim.l1_construction import build_gap, support_filter
    extracts, gap = build_gap()
    dag = acyclic_projection(gap)
"""

from mtdsim.l1_construction.schema import (
    DependencyEdge,
    FlowEdge,
    FlowNode,
    GeneralisedAttackProfile,
    Join,
    Occurrence,
    PerFlowExtract,
    TechniqueNode,
)
from mtdsim.l1_construction.attack_flow_parser import (
    parse_flow_bundle,
    parse_flow_file,
    slugify,
)
from mtdsim.l1_construction.attack_stix import (
    AttackTaxonomy,
    load_attack_taxonomy,
    load_attack_techniques,
)
from mtdsim.l1_construction.aggregate import aggregate_gap, contract_flow
from mtdsim.l1_construction.views import (
    AcyclicView,
    GapView,
    TacticLayer,
    acyclic_projection,
    support_filter,
    tactic_layering,
)
from mtdsim.l1_construction.build import build_gap, persist_extracts, persist_gap

__all__ = [
    # schema
    "PerFlowExtract", "GeneralisedAttackProfile", "TechniqueNode",
    "DependencyEdge", "Occurrence", "Join", "FlowNode", "FlowEdge",
    # parsing
    "parse_flow_file", "parse_flow_bundle", "slugify",
    "load_attack_techniques", "load_attack_taxonomy", "AttackTaxonomy",
    # aggregate
    "aggregate_gap", "contract_flow",
    # views
    "support_filter", "acyclic_projection", "tactic_layering",
    "GapView", "AcyclicView", "TacticLayer",
    # build
    "build_gap", "persist_extracts", "persist_gap",
]
