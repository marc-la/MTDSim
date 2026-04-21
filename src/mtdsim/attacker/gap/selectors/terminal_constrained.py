"""Strategy A-constrained — terminal-objective with constraint parameter.

Extends the plain ``TerminalObjectiveSelector`` ancestor cone with a
group-witnessed constraint: every retained ancestor must share at least one
MITRE ``group_id`` with the terminal technique. Chosen over depth-bound,
campaign-witnessed, and platform-cross-product variants in the 2026-04-17
subgraph exploration notebook (rubric 22/30 vs baseline A = 21/30), because
it anchors the subgraph to an observed APT's behaviour rather than the
looser "techniques that were ever co-seen" criterion.
"""

from __future__ import annotations

from dataclasses import dataclass

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile
from mtdsim.attacker.gap.selectors.base import SubgraphView, ancestor_subgraph


@dataclass
class GroupWitnessedTerminalSelector:
    """Ancestor cone of a terminal, pruned to nodes that share a group with it.

    If ``technique`` is ``None``, the subgraph is the union over every
    objective node in the GAP — useful as a global "group-witnessed" view.
    """

    technique: str | None = None

    def select(self, gap: GeneralisedAttackProfile) -> SubgraphView:
        if self.technique is not None:
            targets = [self.technique]
            mode = "technique"
        else:
            targets = list(gap.objective_nodes)
            mode = "all"

        full_nodes, _ = ancestor_subgraph(gap, targets)

        target_groups: set[str] = set()
        for t in targets:
            node = gap.nodes.get(t)
            if node is not None:
                target_groups.update(node.group_ids)

        if not target_groups:
            kept = {t for t in targets if t in gap.nodes}
        else:
            kept = set()
            for tid in full_nodes:
                node = gap.nodes.get(tid)
                if node is None:
                    continue
                if tid in targets or (set(node.group_ids) & target_groups):
                    kept.add(tid)

        edges = {
            (e.source_id, e.target_id)
            for e in gap.edges
            if e.source_id in kept and e.target_id in kept
        }

        provenance = {
            "selector": "GroupWitnessedTerminal",
            "mode": mode,
            "technique": self.technique,
            "n_targets": len(targets),
            "n_target_groups": len(target_groups),
            "n_nodes": len(kept),
        }
        return SubgraphView(
            node_set=frozenset(kept),
            edge_set=frozenset(edges),
            provenance=provenance,
        )
