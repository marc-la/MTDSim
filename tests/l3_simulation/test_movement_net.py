"""Validation-gate tests for the movement-layer routing net.

The routing net supplies the *base* out-distribution the token samples from:
observed D3 weights composed with the M6 synthetic overlay, schema-pinned. These
tests fix: it loads for every profile, each place's out-weights form a
distribution, the synthetic-overlay merge (island forward chain + backward bridge)
composes as specified, the D8 entry arms seed correctly, and a net whose schema
the class does not know is refused (validation gate 4).
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from mtdsim.l3_simulation.movement.net import (
    KNOWN_GAP_VERSIONS,
    PROFILES,
    NetSchemaError,
    load_routing_net,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
PETRI_DIR = REPO_ROOT / "data" / "ogasp" / "petri"


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("overlay", [True, False])
def test_loads_and_out_weights_are_distributions(profile: str, overlay: bool) -> None:
    net = load_routing_net(profile, with_synthetic_overlay=overlay)
    assert net.places
    for place in net.places:
        out = net.base_out_weights(place)
        if out:  # a non-sink place is a proper distribution
            assert all(w >= 0 for w in out.values())
            assert abs(sum(out.values()) - 1.0) < 1e-9, (place, sum(out.values()))


def test_d8_entry_arms() -> None:
    """Overlay arm seeds at reconnaissance (kill-chain head); observed-only arm
    seeds at initial-access (the comparison arm)."""
    on = load_routing_net("objective_exfiltration_impact", with_synthetic_overlay=True)
    off = load_routing_net("objective_exfiltration_impact", with_synthetic_overlay=False)
    assert on.entry_place == "reconnaissance"
    assert off.entry_place == "initial-access"


def test_synthetic_forward_chain_is_the_island_out_mass() -> None:
    """Where recon is an island, the forward chain recon -> resource-development
    -> initial-access carries the whole out-mass (share 1.0)."""
    net = load_routing_net("objective_exfiltration_impact", with_synthetic_overlay=True)
    assert net.base_out_weights("reconnaissance") == {"resource-development": 1.0}
    assert net.base_out_weights("resource-development") == {"initial-access": 1.0}


def test_backward_bridge_merge_rescales_observed_to_0_9() -> None:
    """initial-access has observed out-edges; the backward bridge to reconnaissance
    carries share 0.1, and the observed edges are scaled to 0.9 of their weights.
    The observed-only arm has no such bridge."""
    on = load_routing_net("objective_exfiltration_impact", with_synthetic_overlay=True)
    off = load_routing_net("objective_exfiltration_impact", with_synthetic_overlay=False)

    out_on = on.base_out_weights("initial-access")
    out_off = off.base_out_weights("initial-access")

    assert out_on["reconnaissance"] == pytest.approx(0.1)
    assert "reconnaissance" not in out_off
    # Every observed edge is scaled to 0.9 of its observed-only weight.
    for dst, w_off in out_off.items():
        assert out_on[dst] == pytest.approx(0.9 * w_off)


def test_unknown_profile_raises() -> None:
    with pytest.raises(KeyError):
        load_routing_net("not-a-profile")


def test_schema_pin_refuses_unknown_gap_version(tmp_path: Path) -> None:
    """Validation gate 4: a net artefact declaring a gap_version the class does
    not know is refused at load, not walked."""
    doc = json.loads((PETRI_DIR / "aggregate_structural.json").read_text())
    doc["provenance"]["gap_version"] = "99.9"  # a version this layer does not know
    assert "99.9" not in KNOWN_GAP_VERSIONS

    bad_dir = tmp_path
    (bad_dir / "aggregate_structural.json").write_text(json.dumps(doc))
    # synthetic overlay is read only when composing; copy a real one across.
    (bad_dir / "synthetic_overlay.json").write_text(
        (PETRI_DIR / "synthetic_overlay.json").read_text()
    )

    with pytest.raises(NetSchemaError, match="unknown gap_version"):
        load_routing_net("aggregate", petri_dir=bad_dir)


def test_schema_pin_refuses_missing_keys(tmp_path: Path) -> None:
    doc = json.loads((PETRI_DIR / "aggregate_structural.json").read_text())
    del doc["transitions"]
    (tmp_path / "aggregate_structural.json").write_text(json.dumps(doc))
    with pytest.raises(NetSchemaError, match="missing required net keys"):
        load_routing_net("aggregate", petri_dir=tmp_path)


def test_schema_pin_refuses_transition_without_primary_weight(tmp_path: Path) -> None:
    doc = json.loads((PETRI_DIR / "aggregate_structural.json").read_text())
    doc = copy.deepcopy(doc)
    del doc["transitions"][0]["weights"]["operator_dedup"]
    (tmp_path / "aggregate_structural.json").write_text(json.dumps(doc))
    with pytest.raises(NetSchemaError, match="operator_dedup"):
        load_routing_net("aggregate", petri_dir=tmp_path, with_synthetic_overlay=False)
