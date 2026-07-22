"""The routing net the movement layer walks — base out-weights per tactic-place.

This is the *movement-layer* view of an OGASP net: the token walks tactic-places
and, at each place, samples the next place from a **base out-distribution**. That
distribution is assembled here, from two tracked artefacts, and is deliberately
kept apart from the *outcome* conditioning (which is the controller's job — the
runtime `overlay.compose(place, verdict, base_out_weights)` conditions what this
module supplies; it never re-derives it, per
``docs/implementation/metrics_semantics.md`` §(f)):

- **Observed base weights (D3).** ``data/ogasp/petri/<profile>_structural.json``
  — the W-A flow-proportion weights (``weights.operator_dedup.weight``, the
  primary corpus variant), already out-edge-normalised so a place's observed
  out-weights sum to 1 (``mtdsim.l3_simulation.petri.weights``).
- **Synthetic overlay (M6).** ``data/ogasp/petri/synthetic_overlay.json`` — the
  declared pre-intrusion connective tissue (forward chain + backward regression
  bridge), composed per its merge rule: a synthetic edge out of a place *with*
  observed out-edges carries a declared ``share``; the observed edges are scaled
  to ``(1 - Σshare)`` (``mtdsim.l3_simulation.petri.synthetic_overlay``). A
  synthetic edge out of an *island* place (no observed out-edges) is that place's
  whole out-mass.

The composition here reproduces that merge rule so the runtime routing net is the
one the synthetic-overlay record describes — the observed ``*_structural.json``
artefacts stay byte-identical; the rescaling lives only in this composed view.

**Schema pinning (validation gate 4).** The loader refuses a net artefact whose
declared ``gap_version`` it does not know, or that is missing the structural keys
it walks — a malformed or future-versioned net fails loud at load, not mid-run.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# …/src/mtdsim/l3_simulation/movement/net.py -> repo root is parents[4].
_REPO_ROOT = Path(__file__).resolve().parents[4]
PETRI_DIR = _REPO_ROOT / "data" / "ogasp" / "petri"

# The five profiles: four GASP classes + the aggregate null profile. Each has a
# ``<profile>_structural.json`` net under PETRI_DIR.
PROFILES: tuple[str, ...] = (
    "pure_steal",
    "pure_impediment",
    "double_extortion",
    "infrastructure_setup",
    "aggregate",
)

# Schema pin. The structural nets carry no dedicated net-schema version, so the
# pin is on the GAP version they were quotiented from plus the structural keys
# the walk reads. A net declaring an unknown gap_version, or missing a required
# key, is refused (gate 4). Widen KNOWN_GAP_VERSIONS deliberately when the GAP
# schema is intentionally revved.
KNOWN_GAP_VERSIONS: frozenset[str] = frozenset({"0.5"})
_REQUIRED_NET_KEYS: frozenset[str] = frozenset(
    {"class_name", "provenance", "places", "entry_marking", "transitions"}
)

# The primary corpus variant (weights.py PRIMARY_VARIANT). The routing net reads
# only the primary weights; ``raw`` is the robustness column, not the runtime
# distribution.
PRIMARY_VARIANT = "operator_dedup"


class NetSchemaError(ValueError):
    """Raised when a net artefact fails the schema pin (unknown version, missing
    key, or a malformed transition) — the class refuses a net it does not know."""


@dataclass(frozen=True)
class RoutingNet:
    """A profile's movement-layer routing net: places, the seed place, and the
    base out-distribution per place (observed D3 weights composed with the
    synthetic overlay). Pure data — no SimPy, no substrate; the base weights the
    controller's ``compose`` conditions at runtime."""

    profile: str
    places: tuple[str, ...]
    entry_place: str
    with_synthetic_overlay: bool
    # place -> {dst_place: base routing weight}; each present place's out-weights
    # sum to 1 (a distribution), or the dict is empty for a sink (a place with no
    # flow-backed observed out-edges and no synthetic out-edge).
    _out: dict[str, dict[str, float]] = field(default_factory=dict)

    def base_out_weights(self, place: str) -> dict[str, float]:
        """The base out-distribution at ``place`` — a copy, so a caller (e.g. the
        overlay composition) can mutate freely. Empty dict for a sink place."""
        if place not in self._out:
            raise KeyError(f"place not in routing net {self.profile!r}: {place!r}")
        return dict(self._out[place])

    def out_places(self, place: str) -> tuple[str, ...]:
        """The destination places reachable from ``place`` under the base net."""
        return tuple(sorted(self._out.get(place, {})))

    def is_sink(self, place: str) -> bool:
        """A place with no base out-edges — the walk cannot leave it on base
        weights alone (the outcome overlay may still suppress it to a stall)."""
        return not self._out.get(place)


def _structural_path(profile: str) -> Path:
    return PETRI_DIR / f"{profile}_structural.json"


def _validate_schema(doc: dict, path: Path) -> None:
    missing = _REQUIRED_NET_KEYS - set(doc)
    if missing:
        raise NetSchemaError(
            f"{path.name}: missing required net keys {sorted(missing)}"
        )
    gap_version = str(doc.get("provenance", {}).get("gap_version"))
    if gap_version not in KNOWN_GAP_VERSIONS:
        raise NetSchemaError(
            f"{path.name}: unknown gap_version {gap_version!r}; this movement "
            f"layer knows {sorted(KNOWN_GAP_VERSIONS)}. Refusing a net artefact "
            "version it does not know (validation gate 4)."
        )
    for t in doc["transitions"]:
        if not {"src_tactic", "dst_tactic", "weights"} <= set(t):
            raise NetSchemaError(
                f"{path.name}: transition {t.get('name')!r} missing "
                "src_tactic / dst_tactic / weights"
            )
        if PRIMARY_VARIANT not in t["weights"]:
            raise NetSchemaError(
                f"{path.name}: transition {t.get('name')!r} has no "
                f"{PRIMARY_VARIANT!r} weight variant"
            )


def _observed_out(doc: dict) -> dict[str, dict[str, float]]:
    """place -> {dst: primary weight} over observed transitions with a defined
    (non-null) primary weight. A null weight means the source place has no
    flow-backed out-edge under the primary variant — dropped here (the place is
    an observed sink unless the synthetic overlay reconnects it)."""
    out: dict[str, dict[str, float]] = {}
    for t in doc["transitions"]:
        w = t["weights"][PRIMARY_VARIANT].get("weight")
        if w is None:
            continue
        out.setdefault(t["src_tactic"], {})[t["dst_tactic"]] = float(w)
    return out


def _synthetic_out(profile: str, overlay_path: Path) -> dict[str, list[tuple[str, float]]]:
    """place -> [(dst, declared_share)] for the profile's synthetic overlay
    edges. Empty for a profile the overlay adds nothing to."""
    with overlay_path.open(encoding="utf-8") as fh:
        overlay = json.load(fh)
    entry = overlay.get("profiles", {}).get(profile, {})
    out: dict[str, list[tuple[str, float]]] = {}
    for s in entry.get("synthetic_transitions", []):
        out.setdefault(s["src_tactic"], []).append(
            (s["dst_tactic"], float(s["declared_share"]))
        )
    return out


def _compose_out(
    places: tuple[str, ...],
    observed: dict[str, dict[str, float]],
    synthetic: dict[str, list[tuple[str, float]]],
) -> dict[str, dict[str, float]]:
    """Compose observed + synthetic into one base out-distribution per place, per
    the synthetic-overlay merge rule.

    - Island source (no observed out-edges): the synthetic edges are the whole
      out-mass (the forward-chain edges carry share 1.0).
    - Source with observed out-edges + a synthetic (backward-bridge) edge: the
      synthetic edge keeps its declared share ``s``; the observed edges are scaled
      to ``(1 - Σs)`` of their weights. Observed weights already sum to 1, so the
      composed out-mass stays 1.
    - Source with only observed edges: unchanged (already a distribution).
    """
    out: dict[str, dict[str, float]] = {}
    for place in places:
        obs = dict(observed.get(place, {}))
        syn = synthetic.get(place, [])
        if not syn:
            out[place] = obs
            continue
        share_total = sum(share for _, share in syn)
        if not obs:
            # Island source: synthetic edges are the whole out-mass.
            composed = {dst: share for dst, share in syn}
        else:
            composed = {dst: w * (1.0 - share_total) for dst, w in obs.items()}
            for dst, share in syn:
                composed[dst] = composed.get(dst, 0.0) + share
        out[place] = composed
    return out


def _choose_entry(places: tuple[str, ...], with_synthetic_overlay: bool, entry_marking: str) -> str:
    """Entry-point selection (D8). Overlay arm seeds at reconnaissance (the
    kill-chain head the overlay connects forward from); the observed-only
    comparison arm seeds at initial-access (the observed corpus's own head).
    Falls back to the net's structural entry_marking if the preferred place is
    absent from the profile."""
    preferred = "reconnaissance" if with_synthetic_overlay else "initial-access"
    if preferred in places:
        return preferred
    if entry_marking in places:
        return entry_marking
    raise NetSchemaError(
        f"cannot seed the token: neither {preferred!r} nor the structural "
        f"entry_marking {entry_marking!r} is a place in this net"
    )


def load_routing_net(
    profile: str,
    with_synthetic_overlay: bool = True,
    petri_dir: Path | str = PETRI_DIR,
) -> RoutingNet:
    """Load and compose a profile's routing net (validation gate 4: schema-pinned).

    ``with_synthetic_overlay`` is the D8 arm toggle: True composes the M6
    synthetic overlay and seeds at reconnaissance; False loads the observed net
    only and seeds at initial-access (the comparison arm).
    """
    petri_dir = Path(petri_dir)
    if profile not in PROFILES:
        raise KeyError(f"unknown profile {profile!r}; expected one of {PROFILES}")
    path = petri_dir / f"{profile}_structural.json"
    with path.open(encoding="utf-8") as fh:
        doc = json.load(fh)
    _validate_schema(doc, path)

    places = tuple(doc["places"])
    observed = _observed_out(doc)
    synthetic = (
        _synthetic_out(profile, petri_dir / "synthetic_overlay.json")
        if with_synthetic_overlay
        else {}
    )
    composed = _compose_out(places, observed, synthetic)
    entry_place = _choose_entry(places, with_synthetic_overlay, doc["entry_marking"])

    return RoutingNet(
        profile=profile,
        places=places,
        entry_place=entry_place,
        with_synthetic_overlay=with_synthetic_overlay,
        _out=composed,
    )


__all__ = [
    "PROFILES",
    "PETRI_DIR",
    "KNOWN_GAP_VERSIONS",
    "PRIMARY_VARIANT",
    "NetSchemaError",
    "RoutingNet",
    "load_routing_net",
]
