"""Generalised APT Profile (GAP) — L1 of the L0->L4 pipeline.

A lossless, Attack-Flow-only technique-dependency graph aggregated from the
MITRE CTID Attack Flow corpus. See ``docs/specs/01_gap_schema.md`` for the data
model and the four design decisions this implements.

Typical use::

    from mtdsim.attacker.gap import build_gap, support_filter
    extracts, gap = build_gap()
    dag = acyclic_projection(gap)
"""

from mtdsim.attacker.gap.schema import (
    DependencyEdge,
    FlowEdge,
    FlowNode,
    GeneralisedAttackProfile,
    Join,
    Occurrence,
    PerFlowExtract,
    TechniqueNode,
)
from mtdsim.attacker.gap.attack_flow_parser import (
    parse_flow_bundle,
    parse_flow_file,
    slugify,
)
from mtdsim.attacker.gap.attack_stix import (
    AttackTaxonomy,
    load_attack_taxonomy,
    load_attack_techniques,
)
from mtdsim.attacker.gap.aggregate import aggregate_gap, contract_flow
from mtdsim.attacker.gap.views import (
    AcyclicView,
    GapView,
    TacticLayer,
    acyclic_projection,
    support_filter,
    tactic_layering,
)
from mtdsim.attacker.gap.build import build_gap, persist_extracts, persist_gap

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
