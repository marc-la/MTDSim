"""The M6 pre-intrusion prefix join — a declared synthetic overlay, kept apart
from the corpus-derived structure.

The corpus starts at the point of detection, so it is blind to pre-intrusion
activity: in some profiles ``reconnaissance`` is an island (no out-edges) and a
recon-seeded token can never reach ``initial-access``. The 14-Jul-2026 ruling
(supervisor_decision_register.md §M6) is to connect the pre-intrusion tactics
manually at the front — recon enables initial access — defensible because
nothing detects pre-intrusion activity. Specification and the resolved open
judgement: ``docs/implementation/pipeline/ogasp/tactic_action_map.md`` §6.

Shape of the join (recon-only resolution, 2026-07-21):

- **One synthetic transition** ``reconnaissance -> initial-access`` per profile
  where the observed net does not already bridge the pair. ``resource-
  development`` stays a **documented island**: it is off-clock (x0 dwell, no
  mapped action), and a ``resource-development -> initial-access`` edge alone
  would be dead structure — the place has no in-edges and the token seeds at
  ``reconnaissance``, so it would never be visited. The chain shape
  ``reconnaissance -> resource-development -> initial-access`` remains a small,
  declared extension of this module if it is ever wanted.
- **Guard rule.** A synthetic transition is added only where the observed net
  does not bridge recon -> initial-access, and only out of a place with **no
  observed out-transitions** — an observed edge is never overwritten and
  observed weight distributions are never renormalised, so the D3
  flow-proportion regime is untouched.
- **Weight.** No backing flow exists, so the W-A regime does not apply; the
  transition carries a **declared manual weight of 1.0** as the sole
  out-transition of its source place (per-place out-weights still sum to 1).
- **Separation.** The overlay lives in ``StructuralNet.synthetic_transitions``,
  never in ``transitions``; the ``*_structural.json`` artefacts stay
  observed-only and the no-synthesis invariant is untouched. The tracked
  overlay record is ``data/ogasp/petri/prefix_join_overlay.json``; composition
  happens at net construction (``build_all_profiles(with_prefix_join=True)``,
  the default). Overlay off + an initial-access seed remains the D8
  comparison arm.
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
OVERLAY_PATH = _REPO_ROOT / "data" / "ogasp" / "petri" / "prefix_join_overlay.json"

RECONNAISSANCE = "reconnaissance"
INITIAL_ACCESS = "initial-access"
RESOURCE_DEVELOPMENT = "resource-development"

M6_PROVENANCE = (
    "M6 pre-intrusion join (supervisor_decision_register.md §M6; "
    "tactic_action_map.md §6): synthetic, no flow backing; declared manual weight"
)

DECLARED_WEIGHT = 1.0

_GUARD_RULE = (
    "a synthetic transition is added only where the observed net does not "
    "bridge reconnaissance -> initial-access, and only out of a place with no "
    "observed out-transitions; observed edges are never overwritten and "
    "observed weight distributions are never renormalised"
)

_RESOLUTION = (
    "recon-only (tactic_action_map.md §6 open judgement, option (b), resolved "
    "2026-07-21): resource-development stays a documented island — it is "
    "off-clock (x0 dwell, no mapped action), and resource-development -> "
    "initial-access alone would be dead structure (no in-edges; the token "
    "seeds at reconnaissance). The chain reconnaissance -> "
    "resource-development -> initial-access remains a declared extension of "
    "prefix_join.py if later wanted."
)


def curate_prefix_join(snet: StructuralNet) -> tuple[TransitionSpec, ...]:
    """The profile's synthetic prefix-join transitions under the guard rule.

    Empty where the observed corpus already bridges recon -> initial-access
    (or either place is absent). Raises where recon has observed out-edges yet
    cannot reach initial-access — mixing a synthetic edge into an observed
    out-distribution would force renormalising flow-derived weights, which
    needs a new declared decision, not a silent one.
    """
    tactic_set = set(snet.tactics)
    if RECONNAISSANCE not in tactic_set or INITIAL_ACCESS not in tactic_set:
        return ()
    adj = _observed_adjacency(snet)
    if _reaches(adj, RECONNAISSANCE, INITIAL_ACCESS):
        return ()
    if adj.get(RECONNAISSANCE):
        raise ValueError(
            f"{snet.class_name}: reconnaissance has observed out-transitions "
            f"({sorted(adj[RECONNAISSANCE])}) but does not reach "
            "initial-access — the M6 declared-weight rule (sole out-edge, "
            "weight 1.0) does not cover this shape; a new declared decision "
            "is required"
        )
    return (
        TransitionSpec(
            name=_transition_name(RECONNAISSANCE, INITIAL_ACCESS),
            src_tactic=RECONNAISSANCE,
            dst_tactic=INITIAL_ACCESS,
            edges=(),
            synthetic=True,
            declared_weight=DECLARED_WEIGHT,
            provenance=M6_PROVENANCE,
        ),
    )


def apply_prefix_join(snet: StructuralNet) -> StructuralNet:
    """Compose one net with its M6 overlay: a new ``StructuralNet`` whose
    SNAKES net contains observed + synthetic transitions, with the overlay in
    ``synthetic_transitions`` and ``transitions`` untouched. Returns ``snet``
    unchanged where the curation adds nothing."""
    synthetic = curate_prefix_join(snet)
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
    """The tracked overlay record over composed nets: what was added where,
    why, and the with/without-overlay recon -> initial-access reachability.
    A pure function of the nets — no dates, deterministic."""
    profiles = {}
    for name, snet in nets.items():
        observed_adj = _observed_adjacency(snet)
        composed_adj = _observed_adjacency(snet, include_synthetic=True)
        present = (
            RECONNAISSANCE in snet.tactics and INITIAL_ACCESS in snet.tactics
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
                    "declared_weight": s.declared_weight,
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
                else "reconnaissance or initial-access absent"
            )
        profiles[name] = entry
    return {
        "artefact": "M6 pre-intrusion prefix-join overlay (recon-only)",
        "register": (
            "docs/implementation/pipeline/ogasp/supervisor_decision_register.md §M6"
        ),
        "specification": (
            "docs/implementation/pipeline/ogasp/tactic_action_map.md §6"
        ),
        "guard_rule": _GUARD_RULE,
        "weight_regime": (
            "declared manual weight (no flow backing — the D3 W-A "
            "flow-proportion regime does not apply); 1.0 as the sole "
            "out-transition of its source place, so per-place out-weights "
            "still sum to 1"
        ),
        "resolution": _RESOLUTION,
        "resource_development_disposition": "documented island (see resolution)",
        "composition": (
            "composed at net construction — build_all_profiles / build_all "
            "with_prefix_join=True (default), or prefix_join.apply_prefix_join; "
            "the observed *_structural.json artefacts never include the overlay"
        ),
        "profiles": profiles,
    }


def write_overlay(
    nets: dict[str, StructuralNet], out_path: Path = OVERLAY_PATH
) -> Path:
    """Write ``data/ogasp/petri/prefix_join_overlay.json`` from composed nets."""
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
    "DECLARED_WEIGHT",
    "INITIAL_ACCESS",
    "M6_PROVENANCE",
    "OVERLAY_PATH",
    "RECONNAISSANCE",
    "RESOURCE_DEVELOPMENT",
    "apply_prefix_join",
    "curate_prefix_join",
    "overlay_payload",
    "write_overlay",
]
