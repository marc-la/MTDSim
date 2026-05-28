"""Data model for the GASP — the L2 boundary object.

One ``SubgraphView`` per operational-objective class
(``pure_steal`` | ``pure_impediment`` | ``double_extortion`` |
``infrastructure_setup``). See
[`docs/specs/02_gasp_schema.md`](../../../docs/specs/02_gasp_schema.md) §(d).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

CLASS_NAMES = (
    "pure_steal",
    "pure_impediment",
    "double_extortion",
    "infrastructure_setup",
)


@dataclass(frozen=True)
class SubgraphView:
    class_name: str
    node_set: frozenset[str]
    edge_set: frozenset[tuple[str, str]]
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "class_name": self.class_name,
            "node_set": sorted(self.node_set),
            "edge_set": [list(e) for e in sorted(self.edge_set)],
            "provenance": self.provenance,
        }

    def to_json(self, path, indent: int = 2) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=indent, ensure_ascii=False)
            f.write("\n")

    @classmethod
    def from_dict(cls, d: dict) -> "SubgraphView":
        return cls(
            class_name=d["class_name"],
            node_set=frozenset(d["node_set"]),
            edge_set=frozenset((s, t) for s, t in d["edge_set"]),
            provenance=dict(d.get("provenance", {})),
        )

    @classmethod
    def from_json(cls, path) -> "SubgraphView":
        with open(path) as f:
            return cls.from_dict(json.load(f))
