"""Subgraph selectors for the Generalised Attack Profile.

Strategies recommended by the 2026-04-17 subgraph exploration notebook:
``TerminalObjectiveSelector`` (A, primary) and ``PlatformSelector`` (B,
complementary). Both produce ``SubgraphView`` objects consumable by the
visualiser payload without coupling the view to the selector.
"""

from mtdsim.attacker.gap.selectors.base import (
    Selector,
    SubgraphView,
    ancestor_subgraph,
)
from mtdsim.attacker.gap.selectors.platform import (
    PLATFORM_BUCKETS,
    PLATFORM_PROFILES,
    PlatformSelector,
    platform_profile,
)
from mtdsim.attacker.gap.selectors.terminal import TerminalObjectiveSelector

__all__ = [
    "Selector",
    "SubgraphView",
    "ancestor_subgraph",
    "PLATFORM_BUCKETS",
    "PLATFORM_PROFILES",
    "PlatformSelector",
    "platform_profile",
    "TerminalObjectiveSelector",
]
