"""Canonical replay fixtures.

A single trivial profile is exposed so the GAP -> SubgraphView -> 6-phase
mapping -> network config -> simulator run -> static replay pipeline can
be exercised end-to-end (CLI, tests, demo notebooks) without the analyst
clicking through the selector rail.

The choice of ``exfiltration`` as the trivial tactic is deliberate: it
sits late in the kill chain so its ancestor subgraph spans every phase,
and the GAP snapshot reliably has at least one terminal objective in
that tactic. ``initial-access`` would be smaller but is rarely tagged
as a terminal objective in the snapshot.
"""

from __future__ import annotations

from typing import Optional

from mtdsim.attacker.attacker_profile import AttackerProfile
from mtdsim.attacker.gap.schema import GeneralisedAttackProfile
from mtdsim.attacker.gap.selectors import (
    SubgraphView,
    TerminalObjectiveSelector,
)
from mtdsim.attacker.subgraph_profile import SubgraphAttackerProfile


TRIVIAL_TACTIC = "exfiltration"
TRIVIAL_SELECTOR_TAG = f"trivial-{TRIVIAL_TACTIC}"


def trivial_subgraph_view(gap: GeneralisedAttackProfile) -> SubgraphView:
    """Resolve the canonical trivial selector against ``gap``.

    Falls back to ``impact`` if the snapshot has no terminal nodes for
    ``TRIVIAL_TACTIC``; if that also yields nothing, returns a view of
    every objective ancestor (i.e. ``mode='all'`` in TerminalObjective
    terms). Designed not to silently produce an empty subgraph.
    """
    view = TerminalObjectiveSelector(tactic=TRIVIAL_TACTIC).select(gap)
    if view.node_set:
        return view
    fallback = TerminalObjectiveSelector(tactic="impact").select(gap)
    if fallback.node_set:
        return fallback
    return TerminalObjectiveSelector().select(gap)


def trivial_profile(
    gap: GeneralisedAttackProfile,
    base_profile: Optional[AttackerProfile] = None,
) -> SubgraphAttackerProfile:
    base = base_profile or AttackerProfile.default()
    view = trivial_subgraph_view(gap)
    return SubgraphAttackerProfile.from_subgraph_view(
        view=view,
        gap=gap,
        base_profile=base,
        selector_tag=TRIVIAL_SELECTOR_TAG,
    )


def trivial_profile_payload(gap: GeneralisedAttackProfile) -> dict:
    """Serialise the trivial view in the shape ``store-operational-profile`` expects.

    Matches :func:`mtdsim.viz.replay.panels.profile.serialise_view` so the
    Run tab's profile pill, save status, and ``_materialise_profile`` all
    treat a CLI-injected trivial profile identically to a UI-saved one.
    """
    view = trivial_subgraph_view(gap)
    return {
        "mode": "terminal_tactic",
        "value": TRIVIAL_TACTIC,
        "node_set": sorted(view.node_set),
        "edge_set": [list(e) for e in view.edge_set],
        "provenance": dict(view.provenance) or {"selector": TRIVIAL_SELECTOR_TAG},
    }
