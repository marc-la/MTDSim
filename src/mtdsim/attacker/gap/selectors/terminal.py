"""Strategy A — terminal-objective / goal partition.

Subgraph = ancestors of any objective technique matching the selector's
tactic or technique criterion. Grounded in MITRE CTID Attack Flow v3,
where the terminal node of a flow is a defensible proxy for the goal.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile
from mtdsim.attacker.gap.selectors.base import SubgraphView, ancestor_subgraph


@dataclass
class TerminalObjectiveSelector:
    tactic: Optional[str] = None
    technique: Optional[str] = None

    def select(self, gap: GeneralisedAttackProfile) -> SubgraphView:
        if self.technique is not None:
            targets = [self.technique]
            mode = "technique"
        elif self.tactic is not None:
            targets = [
                tid for tid in gap.objective_nodes
                if gap.nodes[tid].primary_tactic == self.tactic
            ]
            mode = "tactic"
        else:
            targets = list(gap.objective_nodes)
            mode = "all"

        nodes, edges = ancestor_subgraph(gap, targets)

        provenance = {
            "selector": "TerminalObjective",
            "mode": mode,
            "tactic": self.tactic,
            "technique": self.technique,
            "n_objectives": len(targets),
        }
        return SubgraphView(
            node_set=frozenset(nodes),
            edge_set=frozenset(edges),
            provenance=provenance,
        )
