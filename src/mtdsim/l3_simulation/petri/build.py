"""Build the four un-weighted *structural* tactic-place Petri nets (L3a MVP).

One ordinary Petri net per GASP class, in SNAKES, with a single moving black
token. The locked P/T/F/M mapping (handoff
``docs/handoffs/2026-06-18_l3a_petri_mvp.md``):

- **Places (P)** — one per ATT&CK tactic present in the class ``node_set``
  (distinct ``gap_v0.5.json`` ``primary_tactic``). Counts: 15 / 14 / 14 / 13.
- **Transitions (T)** — one per inter-tactic *tactic-pair* ``a -> b`` with
  ``a != b`` (the legible tactic-FSM granularity). Each carries the contributing
  GASP technique-edges as provenance, so every transition traces to >=1 real
  edge (the no-synthesis invariant). Intra-tactic edges become self-loops and
  are **dropped**.
- **Flow (F)** — bipartite ``place[a] -> T -> place[b]``; a GASP edge becomes a
  transition plus two arcs, never a place->place arc.
- **Marking (M)** — one black token in ``reconnaissance`` (else
  ``initial-access``).

Structural only — no rates, timing, weights, rewards, MTD or CTMC (later
stages). The build is deterministic: sorted iteration throughout, same inputs
-> same net.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import snakes.plugins

from mtdsim.l2_subgraph.schema import CLASS_NAMES, SubgraphView

# Load the graphviz plugin once, at import. ``load`` returns the augmented
# module; we take the names off it rather than ``from nets_gv import ...`` so
# the build does not depend on the synthetic module being registered under a
# fixed name. ``net.draw(...)`` (render.py) needs this plugin.
_nets = snakes.plugins.load("gv", "snakes.nets", "nets_gv")
PetriNet = _nets.PetriNet
Place = _nets.Place
Transition = _nets.Transition
Value = _nets.Value

_REPO_ROOT = Path(__file__).resolve().parents[4]
GAP_PATH = _REPO_ROOT / "data" / "gap" / "gap_v0.5.json"
GASP_DIR = _REPO_ROOT / "data" / "gasp"

# The single black token. ``1`` is the moving token's value (handoff sketch);
# its identity does not matter — only that exactly one token moves.
BLACK_TOKEN = 1

# Marking rule (handoff M-row): seed ``reconnaissance`` if the class has it,
# else ``initial-access``. Tried in this order.
PREFERRED_ENTRY_TACTICS = ("reconnaissance", "initial-access")

# The fifth net: the aggregate (null) profile over the union of all flows —
# the full GAP tactic-quotient (supervisor decision D9 / Marc's aggregate-
# profile proposal). Built from the flow union, not an average of the four
# class nets (classes overlap in flows), so the null is corpus-grounded.
AGGREGATE = "aggregate"
PROFILE_NAMES = CLASS_NAMES + (AGGREGATE,)


@dataclass(frozen=True)
class GapIndex:
    """The slice of ``gap_v0.5.json`` the structural build needs.

    ``tactic_of`` maps every GAP technique to its ``primary_tactic``;
    ``entry_techniques`` / ``objective_techniques`` are the ``is_entry`` /
    ``is_objective`` node sets (consumed unchanged — no re-derivation).
    """

    tactic_of: dict[str, str]
    entry_techniques: frozenset[str]
    objective_techniques: frozenset[str]


@dataclass(frozen=True)
class TransitionSpec:
    """One inter-tactic transition and its GASP provenance.

    ``edges`` are the contributing inter-tactic technique-edges ``(u, v)`` with
    ``tactic_of[u] == src_tactic`` and ``tactic_of[v] == dst_tactic``; non-empty
    by construction for observed transitions, which is what the no-synthesis
    test checks. A **synthetic** transition (the synthetic overlay,
    ``synthetic_overlay.py``) has ``edges == ()`` and carries a declared routing
    share in ``declared_weight`` instead — it never enters
    ``StructuralNet.transitions``.
    """

    name: str
    src_tactic: str
    dst_tactic: str
    edges: tuple[tuple[str, str], ...]
    synthetic: bool = False
    declared_weight: float | None = None
    provenance: str = ""


@dataclass
class StructuralNet:
    """A built structural net plus the metadata the analyses and the
    no-synthesis check consume. ``net`` is the live SNAKES ``PetriNet``."""

    class_name: str
    net: Any  # the SNAKES PetriNet (gv-augmented)
    tactics: tuple[str, ...]  # places, sorted
    transitions: tuple[TransitionSpec, ...]  # observed only, sorted by (src, dst)
    entry_tactic: str  # the place holding the single black token
    selfloops_dropped: int  # intra-tactic edges dropped (recorded, not built)
    # The synthetic overlay (synthetic_overlay.py): kept apart from the observed
    # ``transitions`` so the no-synthesis invariant and the *_structural.json
    # record stay observed-only. Empty on an observed-only build.
    synthetic_transitions: tuple[TransitionSpec, ...] = ()
    provenance: dict = field(default_factory=dict)


def load_gap_index(gap_path: Path = GAP_PATH) -> GapIndex:
    """Read ``gap_v0.5.json`` into the technique -> tactic / entry / objective
    index the structural build needs."""
    with open(gap_path) as f:
        gap = json.load(f)
    nodes = gap["nodes"]
    return GapIndex(
        tactic_of={tid: n["primary_tactic"] for tid, n in nodes.items()},
        entry_techniques=frozenset(
            tid for tid, n in nodes.items() if n["is_entry"]
        ),
        objective_techniques=frozenset(
            tid for tid, n in nodes.items() if n["is_objective"]
        ),
    )


def load_gasp_view(class_name: str, gasp_dir: Path = GASP_DIR) -> SubgraphView:
    """Load one canonical ``gasp_<class>.json`` ``SubgraphView``."""
    return SubgraphView.from_json(Path(gasp_dir) / f"gasp_{class_name}.json")


def build_aggregate_view(gap_path: Path = GAP_PATH) -> SubgraphView:
    """The aggregate (null) profile as a ``SubgraphView``: the union of all
    flows = every GAP node and edge (the full GAP tactic-quotient). Same
    boundary object as the four class views, so the same net construction
    applies unchanged."""
    with open(gap_path) as f:
        gap = json.load(f)
    flow_ids = sorted(
        {fid for n in gap["nodes"].values() for fid in n["flow_ids"]}
    )
    return SubgraphView(
        class_name=AGGREGATE,
        node_set=frozenset(gap["nodes"]),
        edge_set=frozenset(
            (e["source_id"], e["target_id"]) for e in gap["edges"]
        ),
        provenance={
            "flow_ids": flow_ids,
            "source_flow_count": gap["source_flow_count"],
            "gap_version": gap["version"],
            "construction": "union of all flows (full GAP tactic-quotient)",
        },
    )


def load_profile_view(
    profile: str, gasp_dir: Path = GASP_DIR, gap_path: Path = GAP_PATH
) -> SubgraphView:
    """One of the five profile views: a GASP class, or the aggregate."""
    if profile == AGGREGATE:
        return build_aggregate_view(gap_path)
    return load_gasp_view(profile, gasp_dir)


def build_structural_net(view: SubgraphView, gap: GapIndex) -> StructuralNet:
    """Build the structural tactic-place Petri net for one GASP class.

    Deterministic: places are the sorted distinct tactics over ``node_set``;
    transitions are the sorted inter-tactic tactic-pairs, each grouping its
    contributing technique-edges in sorted order; one black token seeds the
    entry place.
    """
    tactic_of = gap.tactic_of

    tactics = tuple(sorted({tactic_of[t] for t in view.node_set}))
    entry_tactic = _choose_entry_tactic(tactics)

    # Group inter-tactic edges by tactic-pair; drop intra-tactic self-loops.
    # Sorted iteration over the edge_set makes the grouped ``edges`` order, and
    # hence everything downstream, deterministic.
    pairs: dict[tuple[str, str], list[tuple[str, str]]] = {}
    selfloops_dropped = 0
    for u, v in sorted(view.edge_set):
        a, b = tactic_of[u], tactic_of[v]
        if a == b:
            selfloops_dropped += 1  # intra-tactic -> self-loop, dropped
            continue
        pairs.setdefault((a, b), []).append((u, v))

    transitions = tuple(
        TransitionSpec(
            name=_transition_name(a, b),
            src_tactic=a,
            dst_tactic=b,
            edges=tuple(sorted(edges)),
        )
        for (a, b), edges in sorted(pairs.items())
    )

    net = make_snakes_net(view.class_name, tactics, entry_tactic, transitions)

    provenance = {
        "class_name": view.class_name,
        "granularity": "inter-tactic tactic-pair",
        "gap_path": str(GAP_PATH.relative_to(_REPO_ROOT)),
        "gasp_source_flow_count": view.provenance.get("source_flow_count"),
        "gap_version": view.provenance.get("gap_version"),
        "build_date": date.today().isoformat(),
    }
    return StructuralNet(
        class_name=view.class_name,
        net=net,
        tactics=tactics,
        transitions=transitions,
        entry_tactic=entry_tactic,
        selfloops_dropped=selfloops_dropped,
        provenance=provenance,
    )


def make_snakes_net(
    name: str,
    tactics: tuple[str, ...],
    entry_tactic: str,
    specs: tuple[TransitionSpec, ...],
) -> Any:
    """The SNAKES net for a place/transition-spec set: one black token in the
    entry place, bipartite ``place[src] -> T -> place[dst]`` per spec."""
    net = PetriNet(name)
    for tac in tactics:
        net.add_place(Place(tac, [BLACK_TOKEN] if tac == entry_tactic else []))
    for spec in specs:
        net.add_transition(Transition(spec.name))
        net.add_input(spec.src_tactic, spec.name, Value(BLACK_TOKEN))
        net.add_output(spec.dst_tactic, spec.name, Value(BLACK_TOKEN))
    return net


def build_all(
    gap_path: Path = GAP_PATH,
    gasp_dir: Path = GASP_DIR,
    with_synthetic_overlay: bool = True,
) -> dict[str, StructuralNet]:
    """Build all four class nets, keyed by class name (canonical order).

    Composed with the synthetic overlay by default — consumers get the
    connected net unless they explicitly ask for the observed-only build
    (``with_synthetic_overlay=False``: the artefact record and the no-synthesis
    invariant tests)."""
    gap = load_gap_index(gap_path)
    nets = {
        cls: build_structural_net(load_gasp_view(cls, gasp_dir), gap)
        for cls in CLASS_NAMES
    }
    return _maybe_join(nets, with_synthetic_overlay)


def build_all_profiles(
    gap_path: Path = GAP_PATH,
    gasp_dir: Path = GASP_DIR,
    with_synthetic_overlay: bool = True,
) -> dict[str, StructuralNet]:
    """All five nets — the four classes plus the aggregate null profile.
    Composed with the synthetic overlay by default (see ``build_all``)."""
    gap = load_gap_index(gap_path)
    nets = {
        profile: build_structural_net(
            load_profile_view(profile, gasp_dir, gap_path), gap
        )
        for profile in PROFILE_NAMES
    }
    return _maybe_join(nets, with_synthetic_overlay)


def _maybe_join(
    nets: dict[str, StructuralNet], with_synthetic_overlay: bool
) -> dict[str, StructuralNet]:
    if not with_synthetic_overlay:
        return nets
    # Imported here: synthetic_overlay imports this module at top level.
    from mtdsim.l3_simulation.petri.synthetic_overlay import apply_synthetic_overlay

    return {name: apply_synthetic_overlay(snet) for name, snet in nets.items()}


def _choose_entry_tactic(tactics: tuple[str, ...]) -> str:
    """First of ``PREFERRED_ENTRY_TACTICS`` present in the class."""
    for tac in PREFERRED_ENTRY_TACTICS:
        if tac in tactics:
            return tac
    raise ValueError(
        "class has neither reconnaissance nor initial-access tactic; "
        f"cannot seed the token. tactics={tactics}"
    )


def _transition_name(src_tactic: str, dst_tactic: str) -> str:
    return f"{src_tactic}__to__{dst_tactic}"


__all__ = [
    "AGGREGATE",
    "BLACK_TOKEN",
    "CLASS_NAMES",
    "GAP_PATH",
    "GASP_DIR",
    "PREFERRED_ENTRY_TACTICS",
    "PROFILE_NAMES",
    "GapIndex",
    "StructuralNet",
    "TransitionSpec",
    "build_aggregate_view",
    "build_all",
    "build_all_profiles",
    "build_structural_net",
    "load_gap_index",
    "load_gasp_view",
    "load_profile_view",
    "make_snakes_net",
]
