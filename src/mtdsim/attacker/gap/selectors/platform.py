"""Strategy B — platform partition.

Nodes are bucketed by their MITRE-canonical ``platforms`` metadata.
MTD primitives are platform-specific (IP shuffling on Windows/Linux,
container rotation in Cloud, PLC firmware rotation for ICS), so a
platform-scoped subgraph maps directly to a defensive posture.
"""

from __future__ import annotations

from dataclasses import dataclass

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile
from mtdsim.attacker.gap.selectors.base import SubgraphView


# Buckets are checked in order; a node is assigned to "cross-platform"
# when its ``platforms`` list spans multiple buckets.
PLATFORM_BUCKETS: list[tuple[str, set[str]]] = [
    ("Windows",     {"Windows"}),
    ("Linux/macOS", {"Linux", "macOS"}),
    ("Cloud",       {"AWS", "Azure", "GCP", "SaaS", "Office Suite",
                     "Google Workspace", "IaaS", "PRE"}),
    ("Network",     {"Network", "Network Devices"}),
    ("Containers",  {"Containers"}),
    ("ICS",         {"ICS", "Embedded"}),
]

PLATFORM_PROFILES: list[str] = (
    [label for label, _ in PLATFORM_BUCKETS]
    + ["cross-platform", "other", "unspecified"]
)


def platform_profile(node_platforms: list[str]) -> str:
    """Assign a node to a platform bucket label."""
    if not node_platforms:
        return "unspecified"
    covered: list[str] = []
    for label, members in PLATFORM_BUCKETS:
        if set(node_platforms) & members:
            covered.append(label)
    if not covered:
        return "other"
    if len(covered) == 1:
        return covered[0]
    return "cross-platform"


@dataclass
class PlatformSelector:
    profile: str

    def select(self, gap: GeneralisedAttackProfile) -> SubgraphView:
        nodes = {
            tid for tid, n in gap.nodes.items()
            if platform_profile(n.platforms) == self.profile
        }
        edges = {
            (e.source_id, e.target_id)
            for e in gap.edges
            if e.source_id in nodes and e.target_id in nodes
        }
        provenance = {
            "selector": "Platform",
            "profile": self.profile,
            "n_nodes": len(nodes),
        }
        return SubgraphView(
            node_set=frozenset(nodes),
            edge_set=frozenset(edges),
            provenance=provenance,
        )
