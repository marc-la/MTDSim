"""The axis-5 exposure family's gate — the declared artefact, not the reader.

The reader that walks a recorded run with this family is exercised in
``test_movement_measures.py`` §9, beside the suite's other readers. What is
pinned here is the declared layer itself: that the committed increment view still
follows from the rules, that the two nulls in the bands are exact rather than
approximate, and that the ranking's contested rows are the ones the record says
they are.
"""
from __future__ import annotations

import pytest

from mtdsim.l3_simulation.movement.exposure import (
    BIMODAL_TACTICS,
    DIRECT,
    INVERSE,
    ExposureCompileError,
    check_view,
    cvss_factor,
    exposure_model,
    load_exposure_rules,
    tier_increment,
    view_cell_count,
)

RULES = load_exposure_rules()

# The fifteen tactics the corpus's ordinal ranking covers. Spelled out rather
# than read from the rules, so a tactic silently dropped from the artefact fails
# here instead of shrinking the test with it.
TACTICS = (
    "reconnaissance", "resource-development", "initial-access", "execution",
    "persistence", "privilege-escalation", "stealth", "defense-impairment",
    "credential-access", "discovery", "lateral-movement", "command-and-control",
    "collection", "exfiltration", "impact",
)


# ---------------------------------------------------------------------------
# The declared artefact
# ---------------------------------------------------------------------------


def test_the_committed_increment_view_reproduces_from_the_rules() -> None:
    """Requirement 1 of the declared-value precedent, enforced by tracked code:
    0 of N cells differ between the committed view and a fresh compilation."""
    problems = check_view(RULES)
    assert problems == [], "\n".join(problems[:20])
    assert view_cell_count(RULES) == 63


def test_the_ranking_is_complete_over_the_fifteen_tactics() -> None:
    """Complete coverage: the ranking must be a total function over the tactic
    space, not only over the tactics the current mapping happens to dispatch. A
    place with no declared tier makes the reader raise rather than guess, so an
    incomplete table would be discovered mid-study."""
    assert set(RULES.tier_of) == set(TACTICS)


def test_every_tactic_sits_at_exactly_one_tier() -> None:
    """The loader refuses a tactic listed twice — the ranking is a function, and
    a tactic in two tiers is the corruption most likely to pass a visual read."""
    doc = dict(RULES.raw)
    tiers = {k: dict(v) for k, v in doc["model"]["tiers"].items()}
    tiers["4"]["tactics"] = list(tiers["4"]["tactics"]) + ["stealth"]
    doc["model"] = {**doc["model"], "tiers": tiers}
    import json
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "sabotaged.json"
        path.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(ExposureCompileError, match="two tiers"):
            load_exposure_rules(path)


def test_the_two_contested_rows_are_the_ones_the_record_names() -> None:
    """§7 ranks reconnaissance and lateral-movement bimodally and the net carries
    one place per tactic, so each takes a single slot and both are swept. Pinning
    the pair here stops a later edit quietly resolving a bimodality the corpus
    did not resolve."""
    assert set(BIMODAL_TACTICS) == {"reconnaissance", "lateral-movement"}
    assert RULES.tier_of["reconnaissance"] == 1     # Marc's ruling, 2026-08-06
    assert RULES.tier_of["lateral-movement"] == 2   # ENUM_HOST dispatches no exploit


# ---------------------------------------------------------------------------
# The two nulls — exact, not approximate
# ---------------------------------------------------------------------------


def test_rho_one_is_the_exact_ablation() -> None:
    """At ρ = 1 every rung scores exactly 1.0, so the ordinal ranking does
    nothing at all and the curve becomes a decayed count of acts. This is the
    placeholder the 2026-08-04 meeting proposed in its own words, and it must be
    bit-exact rather than nearly so — an ablation that is only approximately the
    null cannot attribute a difference to the mechanism."""
    model = exposure_model(RULES, rho=1.0, delta=0.0, score_dwell_only=True)
    assert {model.increment(t) for t in TACTICS} == {1.0}


def test_delta_zero_is_the_exact_cvss_ablation() -> None:
    """At δ = 0 the CVSS term is identically 1.0 whatever the vulnerability
    figure, so the whole term's contribution is measurable by subtraction."""
    for e in (0.0, 0.01, 0.5, 0.99, 1.0):
        assert cvss_factor(e, 0.0, INVERSE) == 1.0
        assert cvss_factor(e, 0.0, DIRECT) == 1.0


def test_a_visit_that_attempted_no_vulnerability_is_never_modulated() -> None:
    """0.0 encodes *none attempted* unambiguously — the substrate floors
    complexity strictly above zero, so a real vulnerability's figure is strictly
    positive — and such a visit takes its tier value untouched at every δ."""
    for delta in (0.0, 0.25, 0.5, 1.0):
        for direction in (INVERSE, DIRECT):
            assert cvss_factor(0.0, delta, direction) == 1.0
    model = exposure_model(RULES, delta=1.0)
    # an INVOKING tier-1 tactic: `stealth` is dwell-only and scores 0 under R1
    assert model.increment("command-and-control") == tier_increment(1, RULES.rho)


# ---------------------------------------------------------------------------
# The increment arithmetic
# ---------------------------------------------------------------------------


def test_the_tier_increment_is_geometric_and_ordered() -> None:
    """A one-rung step multiplies by ρ, and the ranking's order survives into the
    increments — which is the only property the ordinal evidence actually
    supports."""
    rho = 0.5
    assert [tier_increment(t, rho) for t in range(5)] == [
        0.0625, 0.125, 0.25, 0.5, 1.0
    ]
    values = [tier_increment(t, rho) for t in range(5)]
    assert values == sorted(values)


def test_the_two_cvss_directions_are_mirror_images() -> None:
    """Neither direction is attested, so the build must not privilege one in its
    arithmetic: at the same δ the two readings are reflections about m = 1."""
    for e in (0.1, 0.4, 0.75, 1.0):
        inv = cvss_factor(e, 0.5, INVERSE)
        dir_ = cvss_factor(e, 0.5, DIRECT)
        assert inv + dir_ == pytest.approx(2.0)


def test_delta_one_lets_the_cvss_term_silence_an_action_entirely() -> None:
    """The band's far end is a reductio and must be reachable: at δ = 1 a
    maximally exploitable vulnerability under the inverse reading contributes
    nothing at all. A band that could not reach it would leave the term's weight
    assumed rather than tested."""
    assert cvss_factor(1.0, 1.0, INVERSE) == 0.0
    assert cvss_factor(1.0, 1.0, DIRECT) == 2.0
    assert exposure_model(RULES, delta=1.0, direction=INVERSE).increment(
        "initial-access", 1.0
    ) == 0.0


def test_the_increment_is_the_tier_value_times_the_cvss_factor() -> None:
    """Hand-worked: initial-access sits at tier 3, so at ρ = 0.5 its tier value is
    0.5; an exploitability of 0.25 under the inverse reading at δ = 0.5 gives
    m = 1 − 0.5 + 2(0.5)(0.75) = 1.25; the increment is 0.625."""
    model = exposure_model(RULES, rho=0.5, delta=0.5, direction=INVERSE)
    assert model.increment("initial-access", 0.25) == pytest.approx(0.625)


# ---------------------------------------------------------------------------
# The baseline arm's tier assignment
# ---------------------------------------------------------------------------


def test_the_native_verb_tier_is_the_minimum_over_its_preimage() -> None:
    """Charitable to the baseline on purpose: EXPLOIT_VULN's preimage spans tiers
    2 and 3 and it takes 2, the quietest reading available. If the inherited
    attacker still reads louder, the finding is stronger than the construction
    that produced it — and taking the mean or the maximum would hand the
    prediction its own result."""
    model = exposure_model(RULES)
    assert model.verb_tier_of["EXPLOIT_VULN"] == 2
    assert model.verb_tier_of["SCAN_HOST"] == 1        # reconnaissance, declared
    assert model.verb_tier_of["SCAN_NEIGHBOR"] == 1    # command-and-control


def test_the_swept_recon_placement_moves_both_arms_together() -> None:
    """The override rebuilds the native verb table as well as the tactic one, so
    the two arms can never be scored against different tier assignments by
    accident — which would silently decide the very comparison the sweep exists
    to test."""
    swept = exposure_model(RULES, tier_overrides={"reconnaissance": 3})
    assert swept.tier_of["reconnaissance"] == 3
    assert swept.verb_tier_of["SCAN_HOST"] == 3


# ---------------------------------------------------------------------------
# Refusals
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rho", [0.0, -0.5, 1.5])
def test_a_rho_outside_its_domain_is_refused(rho) -> None:
    with pytest.raises(ExposureCompileError, match="rho"):
        exposure_model(RULES, rho=rho)


@pytest.mark.parametrize("tau", [0.0, -1.0])
def test_a_non_positive_decay_constant_is_refused(tau) -> None:
    """A zero or negative τ makes the level undefined or a gain rather than a
    decay. The memoryless regime is reached by a *small positive* τ, which is
    what the band's low end does."""
    with pytest.raises(ExposureCompileError, match="tau"):
        exposure_model(RULES, tau=tau)


def test_an_unknown_direction_is_refused() -> None:
    with pytest.raises(ExposureCompileError, match="direction"):
        exposure_model(RULES, direction="whichever")


def test_an_unranked_place_raises_rather_than_scoring_zero() -> None:
    """A place with no declared tier means the net and the declared family have
    diverged. Scoring it zero would report a silently incomplete curve; raising
    surfaces the divergence at the first visit."""
    model = exposure_model(RULES)
    with pytest.raises(ExposureCompileError, match="no declared observability tier"):
        model.increment("not-a-tactic")


def test_overriding_an_unranked_tactic_is_refused() -> None:
    with pytest.raises(ExposureCompileError, match="carries no declared tier"):
        exposure_model(RULES, tier_overrides={"not-a-tactic": 2})


# ---------------------------------------------------------------------------
# The two rulings of 2026-08-06 (R1: dwell-only does not score; R2: verb-level
# tiers across arms) — stealth_dutycycle_prereg.md §1
# ---------------------------------------------------------------------------


def test_r1_a_dwell_only_visit_scores_nothing() -> None:
    """The ruled default. A tactic that dispatches no substrate verb raises no
    detectability — it contributes elapsed time and nothing else, which is the
    whole of the low-and-slow mechanism: silence is what lets the level fall."""
    model = exposure_model(RULES)
    for tactic in ("impact", "exfiltration", "stealth", "persistence",
                   "collection", "defense-impairment", "resource-development"):
        assert not model.invokes(tactic)
        assert model.increment(tactic) == 0.0


def test_r1_the_superseded_convention_stays_reachable() -> None:
    """The comparison between the two conventions is itself a reported result, so
    the old behaviour must remain computable rather than be deleted."""
    old = exposure_model(RULES, score_dwell_only=True)
    assert old.increment("impact") == tier_increment(4, RULES.rho)


def test_r1_leaves_invoking_tactics_untouched() -> None:
    """The ruling changes which visits score, never what an invoking visit is
    worth — so the eight dispatching tactics keep exactly their declared tiers."""
    ruled = exposure_model(RULES)
    old = exposure_model(RULES, score_dwell_only=True)
    invoking = [t for t in TACTICS if ruled.invokes(t)]
    assert len(invoking) == 8
    for tactic in invoking:
        assert ruled.increment(tactic) == old.increment(tactic)


def test_r1_narrows_the_realised_tier_range_to_one_through_three() -> None:
    """The ruling's stated cost, asserted rather than trusted: tier 0 and the
    whole of tier 4 are dwell-only under v2_partial, so the corpus ranking is
    exercised over a narrowed range and no claim may rest on its extremes."""
    ruled = exposure_model(RULES)
    realised = {ruled.tier_of[t] for t in TACTICS if ruled.invokes(t)}
    assert realised == {1, 2, 3}


def test_r2_verb_level_scoring_makes_the_arms_identical_on_what() -> None:
    """R2's point. Under verb-level tiers every dispatching tactic scores exactly
    what the baseline's corresponding verb scores, so a cross-arm difference can
    only be WHEN the attacker acts, never what it did."""
    cross = exposure_model(RULES, verb_level=True)
    for tactic in TACTICS:
        if not cross.invokes(tactic):
            continue
        verb = cross.verb_of[tactic]
        assert cross.increment(tactic) == cross.verb_increment(verb)


def test_r2_is_off_within_an_arm_so_the_corpus_grounding_survives() -> None:
    """Within the movement arm the tactic-level tiers are the entire point: the
    three exploit-dispatching tactics must NOT collapse to one value, or the
    between-profile comparison would be scored on the substrate's verb vocabulary
    rather than on the corpus's."""
    within = exposure_model(RULES)
    assert within.increment("initial-access") == tier_increment(3, RULES.rho)
    assert within.increment("execution") == tier_increment(2, RULES.rho)
    assert within.increment("initial-access") != within.increment("execution")


def test_the_verb_map_is_derived_from_the_declared_preimage() -> None:
    """R1's dispatch test and the cross-arm mapping are one fact, not two: both
    read the artefact's own verb preimage, so they cannot drift apart."""
    model = exposure_model(RULES)
    for verb, tactics in RULES.verb_preimage.items():
        for tactic in tactics:
            assert model.verb_of[tactic] == verb
            assert model.invokes(tactic)
