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


# ---------------------------------------------------------------------------
# The uniform-weight ablation (plural_preference.md's linchpin arm)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("profile", PROFILES)
def test_uniform_variant_flattens_weights_within_each_place(profile: str) -> None:
    """Every place's out-weights become equal, and still sum to 1 (a proper
    distribution) — the corpus preference is stripped, nothing else."""
    from mtdsim.l3_simulation.movement.net import uniform_weight_variant

    net = load_routing_net(profile, with_synthetic_overlay=True)
    uni = uniform_weight_variant(net)
    for place in uni.places:
        out = uni.base_out_weights(place)
        if out:
            weights = set(round(w, 12) for w in out.values())
            assert len(weights) == 1, (place, out)  # all equal
            assert abs(sum(out.values()) - 1.0) < 1e-9, (place, sum(out.values()))


@pytest.mark.parametrize("profile", PROFILES)
def test_uniform_variant_keeps_the_positive_weight_reachable_graph(profile: str) -> None:
    """Support is exactly the corpus arm's *positive*-weight destinations: a
    zero-weight edge (corpus-present, zero mass, un-resurrectable by the overlay)
    is not in the uniform arm's support, so the two arms share one reachable
    graph and differ only in preference."""
    from mtdsim.l3_simulation.movement.net import uniform_weight_variant

    net = load_routing_net(profile, with_synthetic_overlay=True)
    uni = uniform_weight_variant(net)
    assert uni.places == net.places
    for place in net.places:
        corpus_positive = {d for d, w in net.base_out_weights(place).items() if w > 0}
        assert set(uni.base_out_weights(place)) == corpus_positive, place
        # a sink stays a sink
        assert uni.is_sink(place) == (not corpus_positive)


def test_uniform_variant_is_a_pure_data_transform() -> None:
    """Only ``_out`` changes; profile, places, entry, overlay-arm flag are the
    net's, untouched — the ablation is a read of the weights, not a new model."""
    from mtdsim.l3_simulation.movement.net import uniform_weight_variant

    net = load_routing_net("aggregate", with_synthetic_overlay=True)
    uni = uniform_weight_variant(net)
    assert (uni.profile, uni.places, uni.entry_place, uni.with_synthetic_overlay) == (
        net.profile,
        net.places,
        net.entry_place,
        net.with_synthetic_overlay,
    )


def test_uniform_variant_changes_the_realised_walk() -> None:
    """The arm toggle must actually change behaviour: a matched-seed corpus run and
    uniform run visit different place sequences (otherwise the ablation is inert)."""
    from mtdsim.l3_simulation.movement.run import run_movement

    kw = dict(
        seed=1,
        horizon=15_000,
        mapping_version="v2_partial",
        overlay_version="v3_persistent_backward",
        retrace_sinks=True,
    )
    corpus = run_movement("aggregate", uniform_weights=False, **kw)
    uniform = run_movement("aggregate", uniform_weights=True, **kw)
    corpus_seq = tuple(r.place for r in corpus.records)
    uniform_seq = tuple(r.place for r in uniform.records)
    assert corpus_seq != uniform_seq
    # …and the toggle is deterministic (SIM-05): a re-run reproduces it exactly.
    assert tuple(r.place for r in run_movement("aggregate", uniform_weights=True, **kw).records) == uniform_seq
