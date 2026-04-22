"""GAP-subgraph-driven attacker profile.

Wraps an ``AttackerProfile`` with a restricted set of MITRE ATT&CK
techniques drawn from a ``SubgraphView`` (produced by a GAP selector).
The simulator reads the same scalar parameters as before — those are
delegated via ``__getattr__`` to the wrapped base profile — and can
additionally call :meth:`SubgraphAttackerProfile.sample_technique` at
each phase entry to sample a concrete technique for event emission.

Design: wrap rather than subclass. No ``isinstance(..., AttackerProfile)``
checks exist in the repo, so delegation is safe. Downstream duck-type
detection is via :func:`is_subgraph_profile`.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional

from mtdsim.attacker.attacker_profile import AttackerProfile
from mtdsim.attacker.gap.schema import (
    DependencyEdge,
    GeneralisedAttackProfile,
    TechniqueNode,
)
from mtdsim.attacker.gap.selectors.base import SubgraphView
from mtdsim.attacker.profile_generator import TACTIC_TO_PHASE


@dataclass
class SubgraphAttackerProfile:
    base: AttackerProfile
    subgraph_nodes: dict[str, TechniqueNode] = field(default_factory=dict)
    subgraph_edges: list[DependencyEdge] = field(default_factory=list)
    objective_tid: Optional[str] = None
    selector_tag: str = ""

    _phase_index: Optional[dict[str, list[str]]] = field(default=None, repr=False)
    _predecessors: Optional[dict[str, set[str]]] = field(default=None, repr=False)

    def __getattr__(self, name):
        # __getattr__ runs only when normal lookup fails, so wrapper-defined
        # fields shadow correctly. Delegate everything else (exploit_success_bonus,
        # brute_force_multiplier, attack_threshold, attack_duration_multipliers,
        # get_attack_duration, etc.) to the base profile.
        base = self.__dict__.get("base")
        if base is None:
            raise AttributeError(name)
        return getattr(base, name)

    def _ensure_caches(self) -> None:
        if self._phase_index is None:
            phase_index: dict[str, list[str]] = {}
            for tid, node in self.subgraph_nodes.items():
                phase = TACTIC_TO_PHASE.get(node.primary_tactic)
                if phase is None:
                    continue
                phase_index.setdefault(phase, []).append(tid)
            self._phase_index = phase_index
        if self._predecessors is None:
            preds: dict[str, set[str]] = {tid: set() for tid in self.subgraph_nodes}
            for edge in self.subgraph_edges:
                if edge.target_id in preds and edge.source_id in self.subgraph_nodes:
                    preds[edge.target_id].add(edge.source_id)
            self._predecessors = preds

    def sample_technique(
        self,
        phase: str,
        executed: set[str],
        rng: Optional[random.Random] = None,
        gate_on_predecessors: bool = False,
    ) -> Optional[str]:
        """Sample one technique ID for ``phase`` from the subgraph.

        Returns ``None`` if the filtered pool is empty; callers fall
        through to legacy phase behaviour.
        """
        self._ensure_caches()
        assert self._phase_index is not None and self._predecessors is not None

        candidates = [tid for tid in self._phase_index.get(phase, []) if tid not in executed]
        if gate_on_predecessors and candidates:
            candidates = [
                tid for tid in candidates
                if not self._predecessors[tid] or (self._predecessors[tid] & executed)
            ]
        if not candidates:
            return None

        weights = [max(1, self.subgraph_nodes[tid].campaign_count) for tid in candidates]
        r = rng or random
        return r.choices(candidates, weights=weights, k=1)[0]

    @classmethod
    def from_subgraph_view(
        cls,
        view: SubgraphView,
        gap: GeneralisedAttackProfile,
        base_profile: AttackerProfile,
        selector_tag: str = "",
    ) -> "SubgraphAttackerProfile":
        nodes = {tid: gap.nodes[tid] for tid in view.node_set if tid in gap.nodes}
        edges = [
            e for e in gap.edges
            if (e.source_id, e.target_id) in view.edge_set
        ]
        objective_tid = view.provenance.get("technique") if view.provenance else None
        tag = selector_tag or (view.provenance.get("selector", "") if view.provenance else "")
        return cls(
            base=base_profile,
            subgraph_nodes=nodes,
            subgraph_edges=edges,
            objective_tid=objective_tid,
            selector_tag=tag,
        )


def is_subgraph_profile(profile) -> bool:
    """Duck-type check usable from lower layers without import cycles."""
    return hasattr(profile, "sample_technique") and hasattr(profile, "subgraph_nodes")


if __name__ == "__main__":
    # Smoke test: build a tiny synthetic GAP and exercise the API.
    node_a = TechniqueNode(
        technique_id="T1486", technique_name="Data Encrypted for Impact",
        tactics=["impact"], primary_tactic="impact", tactic_layer=13,
        campaign_count=4,
    )
    node_b = TechniqueNode(
        technique_id="T1059", technique_name="Command and Scripting Interpreter",
        tactics=["execution"], primary_tactic="execution", tactic_layer=3,
        campaign_count=8,
    )
    edge = DependencyEdge(
        source_id="T1059", target_id="T1486",
        evidence_type="attack_flow", confidence=0.9,
    )
    gap = GeneralisedAttackProfile(
        version="test", build_date="2026-04-22", technique_source="synthetic",
        nodes={"T1486": node_a, "T1059": node_b}, edges=[edge],
        objective_nodes=["T1486"],
    )
    view = SubgraphView(
        node_set=frozenset({"T1486", "T1059"}),
        edge_set=frozenset({("T1059", "T1486")}),
        provenance={"selector": "TerminalObjective", "technique": "T1486"},
    )
    prof = SubgraphAttackerProfile.from_subgraph_view(
        view, gap, AttackerProfile.default(), selector_tag="ransomware",
    )
    # Delegation
    assert prof.exploit_success_bonus == 0.0
    assert prof.brute_force_multiplier == 1.0
    assert prof.get_attack_duration("SCAN_HOST") > 0
    # Sampling
    tid = prof.sample_technique("SCAN_PORT", executed=set())
    assert tid == "T1059", f"expected T1059 (execution→SCAN_PORT), got {tid!r}"
    tid = prof.sample_technique("SCAN_NEIGHBOR", executed=set())
    assert tid == "T1486", f"expected T1486 (impact→SCAN_NEIGHBOR), got {tid!r}"
    # Empty phase returns None
    assert prof.sample_technique("BRUTE_FORCE", executed=set()) is None
    # Gate on predecessors: T1486 should be gated off without T1059 executed
    assert prof.sample_technique(
        "SCAN_NEIGHBOR", executed=set(), gate_on_predecessors=True
    ) is None
    assert prof.sample_technique(
        "SCAN_NEIGHBOR", executed={"T1059"}, gate_on_predecessors=True
    ) == "T1486"
    # Duck-type check
    assert is_subgraph_profile(prof)
    assert not is_subgraph_profile(AttackerProfile.default())
    print("subgraph_profile smoke test passed.")
