"""The synthetic overlay — a declared structural sublayer, kept apart from the
corpus-derived structure.

The corpus starts at the point of detection, so it is blind to pre-intrusion
activity: in some profiles ``reconnaissance`` and ``resource-development`` are
detached islands and a recon-seeded token can never reach ``initial-access``.
The supervisor ruling (supervisor_decision_register.md §M6) is to connect the
pre-intrusion tactics manually at the front — recon enables initial access —
defensible because nothing detects pre-intrusion activity. This module is that
declared layer, and it is a **sublayer in its own right** (not "the M6 join"):
it composes synthetic, non-corpus edges onto the observed nets at construction.
Specification and the resolved judgements:
``docs/implementation/pipeline/ogasp/synthetic_overlay.md``.

Shape of the overlay (bidirectional pre-intrusion connective tissue,
2026-07-21). For each profile whose observed corpus leaves the pre-intrusion
band detached (``objective_exfiltration_impact``, ``objective_none_c2``), the overlay
adds a **kill-chain-correct pre-intrusion chain plus a backward regression
bridge**, so a successful attacker can traverse recon -> resource-development
-> initial-access and a *failed* one can fall back into the pre-intrusion
tactics:

- **Forward chain.** ``reconnaissance -> resource-development`` and
  ``resource-development -> initial-access``. resource-development becomes a
  genuine forward pass-through (off-clock: x0 dwell, no mapped action yet — the
  action set is extensible, so a verb may later map to it).
- **Backward regression bridge.** ``initial-access -> reconnaissance``. It lets
  a failed attacker route back to the pre-intrusion band (and from recon
  re-enter the forward chain).

Guard + share rule (one rule for every synthetic edge — Marc's ruling
2026-08-17, replacing the island-only forward rule with its single backward
exception):

- **Guard.** The overlay acts only where the observed net leaves recon unable to
  reach initial-access (and the three pre-intrusion places exist). It then adds
  the same three edges in every such profile.
- **Share.** Each synthetic edge's declared share is read off the observed net
  by ``declared_share``: out of an **island** source (no observed
  out-transitions) the synthetic edge is the place's whole out-mass
  (``ISLAND_SHARE = 1.0``, perturbing no observed distribution); out of a source
  **with** observed out-transitions it carries ``MERGE_SHARE`` of that place's
  composed out-mass and the observed edges are scaled to ``(1 - Σs)`` in their
  flow proportions. The observed ``*_structural.json`` artefacts stay
  **byte-identical** — the rescaling exists only in the composed runtime net.
  Historically (2026-07-21 → 2026-08-17) recon and resource-development were
  islands in both bridged profiles, so the forward edges carried 1.0 and the
  backward bridge was the only merged edge; when SearchAwesome's malvertising
  step gave ``objective_none_c2`` an observed ``resource-development ->
  {command-and-control, execution}``, the rule was made uniform rather than
  refusing the shape.
- **Separation.** The overlay lives in ``StructuralNet.synthetic_transitions``,
  never in ``transitions``; the ``*_structural.json`` artefacts stay observed-
  only and the no-synthesis invariant on ``transitions`` is untouched. The
  tracked record is ``data/ogasp/petri/synthetic_overlay.json``; composition
  happens at net construction (``build_all_profiles(with_synthetic_overlay=True)``,
  the default). Overlay off + an initial-access seed remains the comparison arm.
"""

from __future__ import annotations

import json
from pathlib import Path

from mtdsim.l3_simulation.petri.build import (
    StructuralNet,
    TransitionSpec,
    _transition_name,
    make_snakes_net,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
OVERLAY_PATH = _REPO_ROOT / "data" / "ogasp" / "petri" / "synthetic_overlay.json"

RECONNAISSANCE = "reconnaissance"
INITIAL_ACCESS = "initial-access"
RESOURCE_DEVELOPMENT = "resource-development"

OVERLAY_PROVENANCE = (
    "synthetic overlay (supervisor_decision_register.md §M6; "
    "synthetic_overlay.md): declared, no flow backing; declared routing share"
)

# The sole-out-edge forward chain carries the full routing share of its island
# source place; the backward bridge carries a declared minority share of
# initial-access's composed out-mass (the observed edges keep the remainder in
# their flow proportions).
# One rule for every synthetic edge (Marc's ruling 2026-08-17 — a mechanism,
# not a per-place exception): a synthetic edge out of an ISLAND source (no
# observed out-transitions) is that place's whole out-mass (share 1.0); a
# synthetic edge out of a source WITH observed out-transitions carries the
# declared MERGE_SHARE of that place's composed out-mass and the observed edges
# rescale to (1 - Σshare) in their flow proportions. Before 2026-08-17 the
# forward edges were only ever added out of islands (and the code refused
# otherwise); the backward bridge was the single merged edge. The rule now
# decides the share from the observed net, uniformly.
ISLAND_SHARE = 1.0
MERGE_SHARE = 0.1
# Historical names, kept for callers/tests: the forward chain's island share and
# the backward bridge's merged share.
FORWARD_SHARE = ISLAND_SHARE
BACKWARD_SHARE = MERGE_SHARE

_GUARD_RULE = (
    "the overlay acts only where the observed net leaves reconnaissance unable "
    "to reach initial-access (and all three pre-intrusion places exist); it then "
    "adds the same three edges everywhere — reconnaissance -> resource-development, "
    "resource-development -> initial-access, initial-access -> reconnaissance — "
    "each weighted by the one share rule (see merge_rule), which reads the "
    "observed net to decide island (1.0) or merged (MERGE_SHARE)"
)

_MERGE_RULE = (
    "a synthetic edge out of a place with observed out-edges carries a declared "
    "share s of that place's composed out-mass; the observed edges are scaled to "
    "(1 - Σs) in their flow proportions. The observed *_structural.json artefacts "
    "stay byte-identical — the rescaling exists only in the composed runtime net. "
    "One rule for every synthetic edge (2026-08-17): island source -> share 1.0 "
    "(the whole out-mass); source with observed out-edges -> MERGE_SHARE. Before "
    "2026-08-17 the merge applied to the backward bridge only and forward edges "
    "out of non-island places were refused."
)

_RESOLUTION = (
    "bidirectional pre-intrusion connective tissue (2026-07-21, Marc's "
    "direction, reversing the earlier recon-only resolution): resource-"
    "development is bridged as a forward pass-through on the chain "
    "reconnaissance -> resource-development -> initial-access, and a backward "
    "regression bridge initial-access -> reconnaissance lets a failed attacker "
    "fall back into the pre-intrusion band. resource-development is off-clock "
    "(x0 dwell, no mapped action yet); the action set is extensible."
)


def curate_synthetic_overlay(snet: StructuralNet) -> tuple[TransitionSpec, ...]:
    """The profile's synthetic overlay transitions under the guard + share rule.

    Empty where the observed corpus already bridges recon -> initial-access (or
    any pre-intrusion place is absent). Otherwise returns the forward chain
    (recon -> resource-development -> initial-access) plus the backward
    regression bridge (initial-access -> reconnaissance), each edge's declared
    share decided by :func:`declared_share` from the observed net — 1.0 out of
    an island source, ``MERGE_SHARE`` out of a source with observed out-edges.
    """
    tactic_set = set(snet.tactics)
    for place in (RECONNAISSANCE, INITIAL_ACCESS, RESOURCE_DEVELOPMENT):
        if place not in tactic_set:
            return ()
    adj = _observed_adjacency(snet)
    if _reaches(adj, RECONNAISSANCE, INITIAL_ACCESS):
        return ()
    return tuple(
        _spec(src, dst, declared_share(adj, src))
        for src, dst in (
            (RECONNAISSANCE, RESOURCE_DEVELOPMENT),
            (RESOURCE_DEVELOPMENT, INITIAL_ACCESS),
            (INITIAL_ACCESS, RECONNAISSANCE),
        )
    )


def declared_share(adj: dict[str, set[str]], src: str) -> float:
    """The one share rule: 1.0 out of an island source, ``MERGE_SHARE`` out of a
    source with observed out-transitions."""
    return MERGE_SHARE if adj.get(src) else ISLAND_SHARE


def _spec(src: str, dst: str, share: float) -> TransitionSpec:
    return TransitionSpec(
        name=_transition_name(src, dst),
        src_tactic=src,
        dst_tactic=dst,
        edges=(),
        synthetic=True,
        declared_weight=share,
        provenance=OVERLAY_PROVENANCE,
    )


def apply_synthetic_overlay(snet: StructuralNet) -> StructuralNet:
    """Compose one net with its synthetic overlay: a new ``StructuralNet`` whose
    SNAKES net contains observed + synthetic transitions, with the overlay in
    ``synthetic_transitions`` and ``transitions`` untouched. Returns ``snet``
    unchanged where the curation adds nothing."""
    synthetic = curate_synthetic_overlay(snet)
    if not synthetic:
        return snet
    net = make_snakes_net(
        snet.class_name,
        snet.tactics,
        snet.entry_tactic,
        snet.transitions + synthetic,
    )
    return StructuralNet(
        class_name=snet.class_name,
        net=net,
        tactics=snet.tactics,
        transitions=snet.transitions,
        entry_tactic=snet.entry_tactic,
        selfloops_dropped=snet.selfloops_dropped,
        synthetic_transitions=synthetic,
        provenance=snet.provenance,
    )


def overlay_payload(nets: dict[str, StructuralNet]) -> dict:
    """The tracked overlay record over composed nets: what was added where, why,
    and the with/without-overlay recon -> initial-access reachability. A pure
    function of the nets — no dates, deterministic."""
    profiles = {}
    for name, snet in nets.items():
        observed_adj = _observed_adjacency(snet)
        composed_adj = _observed_adjacency(snet, include_synthetic=True)
        present = all(
            p in snet.tactics
            for p in (RECONNAISSANCE, INITIAL_ACCESS, RESOURCE_DEVELOPMENT)
        )
        observed_bridged = present and _reaches(
            observed_adj, RECONNAISSANCE, INITIAL_ACCESS
        )
        entry: dict = {
            "synthetic_transitions": [
                {
                    "name": s.name,
                    "src_tactic": s.src_tactic,
                    "dst_tactic": s.dst_tactic,
                    "gasp_edges": [],
                    "synthetic": True,
                    "declared_share": s.declared_weight,
                    "direction": "backward"
                    if s.src_tactic == INITIAL_ACCESS
                    else "forward",
                    "provenance": s.provenance,
                }
                for s in snet.synthetic_transitions
            ],
            "recon_reaches_initial_access_observed": observed_bridged,
            "recon_reaches_initial_access_with_overlay": present
            and _reaches(composed_adj, RECONNAISSANCE, INITIAL_ACCESS),
        }
        if not snet.synthetic_transitions:
            entry["reason"] = (
                "observed corpus already bridges reconnaissance -> "
                "initial-access; guard rule adds nothing"
                if observed_bridged
                else "a pre-intrusion place (recon / resource-development / "
                "initial-access) is absent"
            )
        profiles[name] = entry
    return {
        "artefact": "synthetic overlay (declared pre-intrusion structure)",
        "register": (
            "docs/implementation/pipeline/ogasp/supervisor_decision_register.md §M6"
        ),
        "specification": (
            "docs/implementation/pipeline/ogasp/synthetic_overlay.md"
        ),
        "guard_rule": _GUARD_RULE,
        "merge_rule": _MERGE_RULE,
        "weight_regime": (
            "declared routing share (no flow backing — the D3 W-A flow-"
            "proportion regime does not apply). One rule for every synthetic edge: "
            f"share {ISLAND_SHARE} out of an island source (its whole out-mass); "
            f"share {MERGE_SHARE} of the composed out-mass out of a source with "
            "observed out-transitions, the observed edges keeping the remaining "
            f"{round(1 - MERGE_SHARE, 3)} in their flow proportions."
        ),
        "resolution": _RESOLUTION,
        "composition": (
            "composed at net construction — build_all_profiles / build_all "
            "with_synthetic_overlay=True (default), or "
            "synthetic_overlay.apply_synthetic_overlay; the observed "
            "*_structural.json artefacts never include the overlay"
        ),
        "profiles": profiles,
    }


def write_overlay(
    nets: dict[str, StructuralNet], out_path: Path = OVERLAY_PATH
) -> Path:
    """Write ``data/ogasp/petri/synthetic_overlay.json`` from composed nets."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(overlay_payload(nets), f, indent=2, ensure_ascii=False)
        f.write("\n")
    return out_path


def _observed_adjacency(
    snet: StructuralNet, include_synthetic: bool = False
) -> dict[str, set[str]]:
    specs = snet.transitions + (
        snet.synthetic_transitions if include_synthetic else ()
    )
    adj: dict[str, set[str]] = {t: set() for t in snet.tactics}
    for spec in specs:
        adj[spec.src_tactic].add(spec.dst_tactic)
    return adj


def _reaches(adj: dict[str, set[str]], src: str, dst: str) -> bool:
    seen = {src}
    stack = [src]
    while stack:
        u = stack.pop()
        if u == dst:
            return True
        for v in sorted(adj.get(u, ())):
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False


__all__ = [
    "BACKWARD_SHARE",
    "FORWARD_SHARE",
    "INITIAL_ACCESS",
    "OVERLAY_PATH",
    "OVERLAY_PROVENANCE",
    "RECONNAISSANCE",
    "RESOURCE_DEVELOPMENT",
    "apply_synthetic_overlay",
    "curate_synthetic_overlay",
    "overlay_payload",
    "write_overlay",
]
