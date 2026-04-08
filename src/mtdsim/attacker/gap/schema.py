"""
Data classes for the Generalised Attack Profile (GAP).

Mirrors Section 4 of the Attack Graph Design Schema v0.3.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Optional


# Canonical ATT&CK Enterprise tactic ordering (Section 4.1, Table).
# Index == tactic_layer. The kill-chain-phase names in STIX use hyphens.
TACTIC_ORDER = [
    "reconnaissance",
    "resource-development",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "defense-evasion",
    "credential-access",
    "discovery",
    "lateral-movement",
    "collection",
    "command-and-control",
    "exfiltration",
    "impact",
]

TACTIC_LAYERS: dict[str, int] = {t: i for i, t in enumerate(TACTIC_ORDER)}


@dataclass
class Evidence:
    source_type: str           # co_occurrence | attack_flow | caldera_sequence | ontology | documentation | cti_report
    source_url: str = ""
    description: str = ""
    campaigns: list[str] = field(default_factory=list)


@dataclass
class TechniqueNode:
    technique_id: str
    technique_name: str
    tactics: list[str] = field(default_factory=list)
    primary_tactic: str = ""
    tactic_layer: int = -1
    platforms: list[str] = field(default_factory=list)

    # Provenance
    campaign_count: int = 0
    campaign_ids: list[str] = field(default_factory=list)
    group_count: int = 0
    group_ids: list[str] = field(default_factory=list)
    software_ids: list[str] = field(default_factory=list)

    # Sub-techniques collapsed to parent
    sub_technique_ids: list[str] = field(default_factory=list)

    description: str = ""


@dataclass
class DependencyEdge:
    source_id: str
    target_id: str
    evidence_type: str
    confidence: float
    support: Optional[float] = None
    lift: Optional[float] = None
    evidence: list[Evidence] = field(default_factory=list)
    source_count: int = 1
    is_backward: bool = False

    def key(self) -> tuple[str, str]:
        return (self.source_id, self.target_id)


@dataclass
class GeneralisedAttackProfile:
    version: str
    build_date: str
    technique_source: str

    nodes: dict[str, TechniqueNode] = field(default_factory=dict)
    edges: list[DependencyEdge] = field(default_factory=list)

    entry_nodes: list[str] = field(default_factory=list)
    objective_nodes: list[str] = field(default_factory=list)
    layers: dict[int, list[str]] = field(default_factory=dict)

    total_techniques: int = 0
    techniques_with_edges: int = 0
    orphan_techniques: int = 0
    edge_count: int = 0
    consensus_edge_count: int = 0
    intra_tactic_unresolved: int = 0
    backward_edge_count: int = 0

    min_support: float = 0.0
    min_confidence: float = 0.0
    confidence_threshold: float = 0.0

    # ---- Serialisation ----

    def to_dict(self) -> dict:
        d = asdict(self)
        # layers keys must be stringified for JSON
        d["layers"] = {str(k): v for k, v in self.layers.items()}
        return d

    def to_json(self, path: str, indent: int = 2) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=indent, default=str)

    @classmethod
    def from_dict(cls, d: dict) -> "GeneralisedAttackProfile":
        nodes = {k: TechniqueNode(**v) for k, v in d.get("nodes", {}).items()}
        edges = []
        for e in d.get("edges", []):
            e = dict(e)
            e["evidence"] = [Evidence(**ev) for ev in e.get("evidence", [])]
            edges.append(DependencyEdge(**e))
        layers = {int(k): v for k, v in d.get("layers", {}).items()}
        scalar_fields = {
            k: v for k, v in d.items()
            if k not in ("nodes", "edges", "layers")
        }
        return cls(nodes=nodes, edges=edges, layers=layers, **scalar_fields)
