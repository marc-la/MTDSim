"""
Generalised Attack Profile (GAP) construction.

Implements the Attack Graph Design Schema v0.4: a global, technique-level
dependency graph derived from MITRE ATT&CK via co-occurrence mining plus
tactic-ordering directionality, with supplementary edges from the MITRE
Attack Flow corpus and ontology extraction from STIX descriptions. v0.4
adds ``GroupProfile`` / ``CampaignProfile`` enrichment and a Cytoscape.js
viewer that makes motivation- and campaign-based filtering first-class.

See notebooks/2026-04-08_MTDSim_AttackGraphDesignSchema.md for the full
design rationale.
"""

from mtdsim.attacker.gap.schema import (
    MOTIVATION_CATEGORIES,
    TACTIC_LAYERS,
    TACTIC_ORDER,
    CampaignProfile,
    DependencyEdge,
    Evidence,
    GeneralisedAttackProfile,
    GroupProfile,
    TechniqueNode,
)
from mtdsim.attacker.gap.stix_parser import parse_stix_bundle
from mtdsim.attacker.gap.cooccurrence_miner import (
    build_usage_matrix,
    mine_cooccurrence_edges,
)
from mtdsim.attacker.gap.edge_importer import (
    import_attack_flow_corpus,
    extract_ontology_edges,
)
from mtdsim.attacker.gap.enrichment import enrich_group_profiles
from mtdsim.attacker.gap.gap_builder import build_gap
from mtdsim.attacker.gap.viz import (
    MITRETechniqueDependencyVisualiser,
    build_payload,
)

__all__ = [
    "MOTIVATION_CATEGORIES",
    "TACTIC_LAYERS",
    "TACTIC_ORDER",
    "CampaignProfile",
    "DependencyEdge",
    "Evidence",
    "GeneralisedAttackProfile",
    "GroupProfile",
    "TechniqueNode",
    "parse_stix_bundle",
    "build_usage_matrix",
    "mine_cooccurrence_edges",
    "import_attack_flow_corpus",
    "extract_ontology_edges",
    "enrich_group_profiles",
    "build_gap",
    "MITRETechniqueDependencyVisualiser",
    "build_payload",
]
