"""Data model for the Generalised APT Profile (GAP).

Two layers, per ``docs/specs/01_gap_schema.md``:

- **Per-flow extract** (§c) — a lossless, technique-level rendering of a single
  Attack Flow: action / operator / condition nodes + typed edges
  (``effect`` / ``on_true`` / ``on_false``). Committed as YAML; the seam for
  hand-authored incidents.
- **Aggregate GAP** (§d) — the canonical artefact: technique nodes + dependency
  edges, where operator/condition logic survives as edge metadata
  (join-groups + branch). Committed as JSON.

Everything is plain dataclasses with deterministic, hand-reviewable
serialisation. None of the v0.4 co-occurrence / motivation fields survive — the
central invariant (§a) is that every edge traces to a real flow link, so the
provenance carried here is *flow* provenance, never group/campaign statistics.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Reference tables — ATT&CK Enterprise tactic ordering (layout/ordering proxy
# only; per §a it never sets edge direction).
#
# These are **fallback defaults** (the classic 14-tactic Enterprise matrix). The
# build derives the live taxonomy — order, layers, and TA#### -> name — from the
# *pinned* ATT&CK bundle (see ``attack_stix.load_attack_taxonomy``), so that a
# version shift like v19.1 (which splits ``defense-evasion`` into ``stealth`` +
# ``defense-impairment``, 15 tactics) is reflected correctly rather than
# mislayered. The tables below are used only when no bundle is supplied (e.g.
# parsing a hand-authored per-flow extract in isolation).
# ---------------------------------------------------------------------------

# Canonical kill-chain-phase order. Index == tactic_layer. STIX phase names are
# hyphenated.
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

# ATT&CK Enterprise tactic external-id -> kill-chain-phase name. Attack Flow
# actions carry the tactic as ``tactic_id`` (e.g. "TA0002"); the GAP stores the
# phase name to match ATT&CK's ``kill_chain_phases``.
TACTIC_ID_TO_NAME: dict[str, str] = {
    "TA0043": "reconnaissance",
    "TA0042": "resource-development",
    "TA0001": "initial-access",
    "TA0002": "execution",
    "TA0003": "persistence",
    "TA0004": "privilege-escalation",
    "TA0005": "defense-evasion",
    "TA0006": "credential-access",
    "TA0007": "discovery",
    "TA0008": "lateral-movement",
    "TA0009": "collection",
    "TA0011": "command-and-control",
    "TA0010": "exfiltration",
    "TA0040": "impact",
}

# Edge type / branch / operator vocabularies.
EDGE_TYPES = ("effect", "on_true", "on_false")
OPERATORS = ("AND", "OR")
NODE_KINDS = ("action", "operator", "condition")


# ===========================================================================
# Per-flow extract (§c) — the lossless intermediate.
# ===========================================================================


@dataclass
class FlowNode:
    """One action / operator / condition node within a single flow.

    Only the fields relevant to ``kind`` are populated; serialisation emits just
    those (see :meth:`to_compact`).
    """

    id: str                                  # stable local id within this flow
    kind: str                                # action | operator | condition
    # action
    technique_id: Optional[str] = None       # parent-collapsed; None if unmapped
    sub_technique_id: Optional[str] = None   # original id as drawn (may == parent)
    name: Optional[str] = None
    tactic: Optional[str] = None             # kill-chain phase of the action
    confidence: Optional[int] = None         # STIX per-action confidence 0-100
    # operator
    operator: Optional[str] = None           # AND | OR
    # condition
    description: Optional[str] = None

    def to_compact(self) -> dict:
        """Kind-appropriate dict for YAML (drops irrelevant / empty fields)."""
        d: dict = {"id": self.id, "kind": self.kind}
        if self.kind == "action":
            d["technique_id"] = self.technique_id
            if self.sub_technique_id and self.sub_technique_id != self.technique_id:
                d["sub_technique_id"] = self.sub_technique_id
            if self.name:
                d["name"] = self.name
            if self.tactic:
                d["tactic"] = self.tactic
            if self.confidence is not None:
                d["confidence"] = self.confidence
        elif self.kind == "operator":
            d["operator"] = self.operator
        elif self.kind == "condition":
            if self.description:
                d["description"] = self.description
        return d


@dataclass
class FlowEdge:
    source: str
    target: str
    type: str                                # effect | on_true | on_false

    def to_compact(self) -> dict:
        return {"source": self.source, "target": self.target, "type": self.type}


@dataclass
class PerFlowExtract:
    flow_id: str                             # corpus filename slug, or hand-assigned
    flow_name: str
    scope: str                               # incident | campaign | threat-actor | ...
    source: str                              # attack_flow_corpus | hand_curated
    schema_version: str                      # Attack Flow extension schema parsed
    references: list[dict] = field(default_factory=list)
    start_refs: list[str] = field(default_factory=list)
    nodes: list[FlowNode] = field(default_factory=list)
    edges: list[FlowEdge] = field(default_factory=list)

    # -- helpers ----------------------------------------------------------

    def node_by_id(self) -> dict[str, FlowNode]:
        return {n.id: n for n in self.nodes}

    def to_dict(self) -> dict:
        return {
            "flow_id": self.flow_id,
            "flow_name": self.flow_name,
            "scope": self.scope,
            "source": self.source,
            "schema_version": self.schema_version,
            "references": self.references,
            "start_refs": list(self.start_refs),
            "nodes": [n.to_compact() for n in self.nodes],
            "edges": [e.to_compact() for e in self.edges],
        }

    def to_yaml(self) -> str:
        import yaml

        return yaml.safe_dump(self.to_dict(), sort_keys=False, allow_unicode=True)

    @classmethod
    def from_dict(cls, d: dict) -> "PerFlowExtract":
        nodes = [FlowNode(**n) for n in d.get("nodes", [])]
        edges = [FlowEdge(**e) for e in d.get("edges", [])]
        return cls(
            flow_id=d["flow_id"],
            flow_name=d["flow_name"],
            scope=d.get("scope", ""),
            source=d.get("source", ""),
            schema_version=d.get("schema_version", ""),
            references=list(d.get("references", [])),
            start_refs=list(d.get("start_refs", [])),
            nodes=nodes,
            edges=edges,
        )

    @classmethod
    def from_yaml(cls, text: str) -> "PerFlowExtract":
        import yaml

        return cls.from_dict(yaml.safe_load(text))


# ===========================================================================
# Aggregate GAP (§d) — the canonical artefact.
# ===========================================================================


@dataclass
class Join:
    """The operator a contracted edge passed through (None for direct edges)."""

    group_id: str                            # "<flow_id>:<operator_node_id>"
    operator: str                            # AND | OR


@dataclass
class Occurrence:
    """One (flow, contracted-edge) observation, preserving join/branch context."""

    flow_id: str
    edge_type: str                           # effect | on_true | on_false
    join: Optional[Join] = None              # null when action->action, no operator
    branch: Optional[str] = None             # true|false when via a condition; else null


@dataclass
class TechniqueNode:
    technique_id: str                        # parent technique, e.g. T1496
    name: str = ""
    tactics: list[str] = field(default_factory=list)
    primary_tactic: str = ""
    tactic_layer: int = -1
    platforms: list[str] = field(default_factory=list)
    sub_technique_ids: list[str] = field(default_factory=list)
    # flow provenance / structural role
    flow_count: int = 0                      # node multiplicity (# flows containing it)
    flow_ids: list[str] = field(default_factory=list)
    is_entry: bool = False
    is_objective: bool = False


@dataclass
class DependencyEdge:
    source_id: str                           # parent technique ids; direction as drawn
    target_id: str
    observation_count: int = 0               # edge multiplicity (# distinct flows)
    flow_ids: list[str] = field(default_factory=list)
    occurrences: list[Occurrence] = field(default_factory=list)
    tactic_delta: str = "intra"              # forward | backward | intra (descriptive)
    confidence_samples: list[int] = field(default_factory=list)

    def key(self) -> tuple[str, str]:
        return (self.source_id, self.target_id)


@dataclass
class GeneralisedAttackProfile:
    version: str
    build_date: str
    attack_flow_schema_version: str
    corpus_ref: str                          # reproducibility — corpus release pin
    attack_source: str                       # ATT&CK STIX version for node metadata

    nodes: dict[str, TechniqueNode] = field(default_factory=dict)
    edges: list[DependencyEdge] = field(default_factory=list)

    source_flow_count: int = 0
    node_count: int = 0
    edge_count: int = 0
    entry_nodes: list[str] = field(default_factory=list)
    objective_nodes: list[str] = field(default_factory=list)
    layers: dict[int, list[str]] = field(default_factory=dict)

    # -- serialisation ----------------------------------------------------

    def to_dict(self) -> dict:
        d = asdict(self)
        # JSON object keys must be strings; tactic_layer ints -> str.
        d["layers"] = {str(k): v for k, v in self.layers.items()}
        return d

    def to_json(self, path, indent: int = 2) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=indent, ensure_ascii=False)
            f.write("\n")

    @classmethod
    def from_dict(cls, d: dict) -> "GeneralisedAttackProfile":
        nodes = {k: TechniqueNode(**v) for k, v in d.get("nodes", {}).items()}
        edges = []
        for e in d.get("edges", []):
            e = dict(e)
            occ = []
            for o in e.get("occurrences", []):
                o = dict(o)
                j = o.get("join")
                o["join"] = Join(**j) if j else None
                occ.append(Occurrence(**o))
            e["occurrences"] = occ
            edges.append(DependencyEdge(**e))
        layers = {int(k): v for k, v in d.get("layers", {}).items()}
        scalar = {
            k: v for k, v in d.items()
            if k not in ("nodes", "edges", "layers")
        }
        return cls(nodes=nodes, edges=edges, layers=layers, **scalar)

    @classmethod
    def from_json(cls, path) -> "GeneralisedAttackProfile":
        with open(path) as f:
            return cls.from_dict(json.load(f))
