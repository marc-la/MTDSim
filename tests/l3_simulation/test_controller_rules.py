"""The outcome-overlay rule compiler — reproduction, the distance kernel, the registry.

The declared-value precedent requires that these values be *rule-generated and
reproducible, not post-hoc* (``docs/implementation/declared_value_provenance.md``
§1). That requirement is only real if something checks it, so the first test here
is the reproduction check itself: every registered overlay version is re-compiled
from the one rule set and diffed cell by cell against what is committed.

The rest pin the parts of the compiler a future edit could break quietly — the
kernel's shape and its strict floor, the fact that the fold-in changed no rule
value, and the guarantee the versioning exists for: that experiment 1's arm still
compiles to exactly the values experiment 1 ran on.

Ground truth: ``docs/implementation/pipeline/ogasp/weight_sensitivity_study.md``.
"""
from __future__ import annotations

import pytest

from mtdsim.l3_simulation.controller.outcome import (
    OutcomeOverlay,
    load_outcome_overlay,
    load_overlay_registry,
)
from mtdsim.l3_simulation.controller.rules import (
    DistanceKernel,
    RuleCompileError,
    RuleSpec,
    check_registry,
    compile_table,
    compile_values,
    kernel_from_consensus,
    load_rule_set,
    relationship,
    spec_from_registry_entry,
)
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net

V1, V2 = "v1_band_relationship", "v2_lifecycle_distance"
N_PAIRS = 210  # 15 tactics x 14 destinations, no self-loops


@pytest.fixture(scope="module")
def rules():
    return load_rule_set()


# --- requirement 1: reproducible, not post-hoc -------------------------------
def test_every_registered_version_reproduces_from_the_rules(rules) -> None:
    """The reproduction check. A non-empty diff means a committed view no longer
    follows from the rules — either the rules moved without a regeneration, or a
    view was hand-edited, and both are the failure this test exists to catch."""
    problems = check_registry(rules)
    assert set(problems) == {V1, V2}
    for version, diff in problems.items():
        assert diff == [], f"{version} no longer follows from the rules: {diff[:5]}"


def test_both_versions_cover_the_complete_pair_space(rules) -> None:
    for version in (V1, V2):
        spec = spec_from_registry_entry(load_overlay_registry().get(version).spec)
        for verdict in ("success", "failure"):
            table = compile_table(rules, verdict, spec)
            assert sum(len(dsts) for dsts in table.values()) == N_PAIRS
            assert all(src not in dsts for src, dsts in table.items())  # no self-loops


# --- the guarantee the registry exists for ----------------------------------
def test_experiment_1_arm_is_unchanged_by_the_fold_in(rules) -> None:
    """v1 must still be the values experiment 1 ran on. The fold-in adds a term
    and re-sources another; neither may touch the frozen version."""
    v1 = load_outcome_overlay(version=V1)
    v2 = load_outcome_overlay(version=V2)
    spec_v1 = spec_from_registry_entry(load_overlay_registry().get(V1).spec)
    assert spec_v1.distance is False
    assert spec_v1.relationship_source == "bands"
    # And the two versions are genuinely different data, so the test above is not
    # passing vacuously.
    differing = [
        (verdict, src, dst)
        for verdict in ("success", "failure")
        for src in v1.by_verdict[verdict]
        for dst in v1.by_verdict[verdict][src]
        if v1.value(verdict, src, dst) != v2.value(verdict, src, dst)
    ]
    assert len(differing) > 50


def test_no_r2_rule_value_changed(rules) -> None:
    """The fold-in's claim: it multiplies, it does not re-author. Every pair the
    kernel leaves at 1.0 must carry exactly its v1 rule value — for the pairs
    whose relationship class the consensus did not move."""
    v1, v2 = load_outcome_overlay(version=V1), load_outcome_overlay(version=V2)
    bands, stages = rules.bands, rules.stage_of
    kernel = kernel_from_consensus(rules.consensus)
    checked = 0
    for verdict in ("success", "failure"):
        for src in rules.tactics:
            for dst in rules.tactics:
                if src == dst:
                    continue
                same_class = relationship(src, dst, bands) == relationship(src, dst, stages)
                if not (same_class and kernel(stages[dst] - stages[src]) == 1.0):
                    continue
                assert v2.value(verdict, src, dst) == v1.value(verdict, src, dst), (
                    f"{verdict} {src}->{dst} changed value with no re-class and no decay"
                )
                checked += 1
    assert checked > 100  # the untouched majority, not a handful


# --- the kernel -------------------------------------------------------------
def test_kernel_parameters_come_from_the_consensus_artefact(rules) -> None:
    """The magnitudes are declared by the literature half and read, not restated."""
    assert kernel_from_consensus(rules.consensus) == DistanceKernel(0.25, 0.5, 0.1)


@pytest.mark.parametrize(
    "delta, expected",
    [(0, 1.0), (1, 1.0), (2, 0.25), (3, 0.0), (-1, 1.0), (-2, 0.5), (-3, 0.25)],
)
def test_kernel_shape_at_the_declared_parameters(delta, expected) -> None:
    assert DistanceKernel(0.25, 0.5, 0.1)(delta) == expected


def test_the_floor_is_strict_so_a_value_on_it_survives() -> None:
    """Load-bearing at one swept corner: gamma=0.1 puts the two-stage forward skip
    at exactly the floor, and it must survive rather than zero."""
    kernel = DistanceKernel(gamma=0.1, delta_ratio=0.5, z=0.1)
    assert kernel.raw(2) == pytest.approx(0.1)
    assert kernel(2) == pytest.approx(0.1)
    assert kernel(3) == 0.0


def test_forward_is_suppressed_harder_than_backward() -> None:
    """The asymmetry the design turns on: leaping forward is what is suppressed,
    falling back is ordinary campaign behaviour."""
    kernel = DistanceKernel(0.25, 0.5, 0.0)
    for distance in (2, 3):
        assert kernel(distance) < kernel(-distance)


# --- the motivating pairs (study §2) ---------------------------------------
@pytest.mark.parametrize(
    "verdict, src, dst, expected",
    [
        # the canonical long jump collapses to exactly zero, derived from the floor
        ("success", "reconnaissance", "impact", 0.0),
        ("failure", "reconnaissance", "impact", 0.0),
        # the adjacent forward step is untouched
        ("success", "reconnaissance", "initial-access", 1.0),
        # the failure-side regression bridge survives intact
        ("failure", "initial-access", "reconnaissance", 0.9),
        # a two-stage skip is suppressed, not banned
        ("success", "initial-access", "exfiltration", 0.15),
    ],
)
def test_motivating_pairs_behave(verdict, src, dst, expected) -> None:
    assert load_outcome_overlay(version=V2).value(verdict, src, dst) == pytest.approx(expected)


def test_no_enabled_pair_crosses_two_stages(rules) -> None:
    """The independent cross-check the fold-in surfaced: the enables sets were built
    from tactic semantics and incident reports with no lifecycle model in hand, and
    they are adjacency-respecting anyway. If this ever fails, the distance term has
    started grading the enablement tier and the record's §1.3 claim is stale."""
    far = [
        (src, dst)
        for src, dsts in rules.enables.items()
        for dst in dsts
        if abs(rules.stage_of[dst] - rules.stage_of[src]) >= 2
    ]
    assert far == []


# --- the stall guard (study §2) --------------------------------------------
def test_no_place_loses_its_whole_out_set_at_any_swept_point(rules) -> None:
    """A pair can now carry an exact zero, so a stall is representable. It must not
    actually occur anywhere in the declared sweep space."""
    nets = {p: load_routing_net(p, with_synthetic_overlay=True) for p in PROFILES}
    stalls = []
    for gamma in (0.1, 0.25, 0.5):
        for delta_ratio in (0.25, 0.5, 0.75):
            for z in (0.0, 0.05, 0.1):
                spec = RuleSpec(kernel=DistanceKernel(gamma, delta_ratio, z))
                overlay = OutcomeOverlay.from_values(compile_values(rules, spec))
                for profile, net in nets.items():
                    for place in net.places:
                        if net.is_sink(place):
                            continue
                        for verdict in ("success", "failure"):
                            if not overlay.compose(place, verdict, net.base_out_weights(place)):
                                stalls.append((gamma, delta_ratio, z, profile, place, verdict))
    assert stalls == []


# --- the registry and its loud validation ----------------------------------
def test_registry_default_is_the_experiment_1_version() -> None:
    """Promoting the newest version to default would re-bake an experiment's choice
    into the pipeline, which is the coupling the registry removes."""
    registry = load_overlay_registry()
    assert registry.default == V1
    assert set(registry.names) == {V1, V2}
    assert load_outcome_overlay().version == V1


def test_selecting_an_unknown_version_raises() -> None:
    with pytest.raises(KeyError, match="unknown outcome-overlay version"):
        load_outcome_overlay(version="v99_nonexistent")


def test_files_and_version_together_is_a_contradiction() -> None:
    with pytest.raises(ValueError, match="either files or version"):
        load_outcome_overlay(files={}, version=V1)


def test_unknown_relationship_source_raises() -> None:
    with pytest.raises(RuleCompileError, match="unknown relationship_source"):
        RuleSpec(relationship_source="phase_of_the_moon")


def test_in_memory_overlay_composes_like_a_loaded_one(rules) -> None:
    """The seam the sweep runs through: a compiled parameter set must behave exactly
    like the committed version it reproduces, so a sweep point is comparable to a
    registered one."""
    spec = spec_from_registry_entry(load_overlay_registry().get(V2).spec)
    in_memory = OutcomeOverlay.from_values(compile_values(rules, spec))
    on_disk = load_outcome_overlay(version=V2)
    net = load_routing_net("aggregate", with_synthetic_overlay=True)
    for place in net.places:
        if net.is_sink(place):
            continue
        for verdict in ("success", "failure"):
            base = net.base_out_weights(place)
            assert in_memory.compose(place, verdict, base) == pytest.approx(
                on_disk.compose(place, verdict, base)
            )


def test_rules_and_consensus_must_seat_the_same_tactics(tmp_path, rules) -> None:
    """A tactic added to one artefact and not the other must fail at load, not
    compile to a silently wrong table."""
    import json

    from mtdsim.l3_simulation.controller.rules import CONSENSUS_PATH, RULES_PATH

    consensus = json.loads(CONSENSUS_PATH.read_text(encoding="utf-8"))
    consensus["stage_of"].pop("impact")
    broken = tmp_path / "lifecycle_consensus.json"
    broken.write_text(json.dumps(consensus), encoding="utf-8")
    with pytest.raises(RuleCompileError, match="seat different"):
        load_rule_set(RULES_PATH, broken)
