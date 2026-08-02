"""The iterated attacker utility model — the axis-6 decision model repaired so it
can express instrumental value.

The gates this file enforces are the ones the design brief names, and the first
three are hard constraints rather than findings:

1. **λ = 0 stays a bit-identical off-switch** for every arm, including the two
   stateful ones. Change A makes the modulator stateful, which is precisely the
   circumstance under which an ablation quietly stops being exact, so the
   identity is re-asserted over the full configuration grid rather than
   inherited from the shipped model's suite.
2. **No new declared value.** The iterated model reads only the duration
   catalogue, the precondition relation, the profile nets and the existing
   ρ / ``cost_floor_s`` / λ. If a new magnitude appears, the brief's central
   claim — that this is *derived* rather than *declared* — has failed.
3. **The laundering check.** Change B measures distance in the same graph the
   base transition weights are measured over, so the benefit family must be
   shown **not** to be monotone in the base out-weight. Without that, the term is
   laundering corpus frequency as value, and the separation the shipped family
   earned in ``incentive_rationality.md`` §4.1 would be lost.

Plus the structural claims the two changes rest on: the ``declared`` arm
reproduces the shipped modulator exactly (so the comparison arms are honest);
the expected cost is zero when ready and strictly positive when not; the MTD
response is layer-specific, because ``mtd_clears`` says a network mutation
destroys position and an application mutation destroys nothing; determinism
survives the modulator becoming stateful; and no factor can reach zero, so the
seam's stall rule is still never engaged.

Design record: docs/implementation/pipeline/ogasp/iterated_cost_model.md.
"""
from __future__ import annotations

import dataclasses
import inspect

import pytest

from mtdsim.l3_simulation.movement.learning_readiness import PreconditionModel
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState
from mtdsim.l3_simulation.movement.utility import (
    load_benefit,
    load_utility_rules,
    stage_gap,
    utility_modulator_for,
)
from mtdsim.l3_simulation.movement.utility_iterated import (
    ARMS,
    CapabilityCostModel,
    IteratedUtilityModulator,
    benefit_values_net,
    iterated_utility_modulator_for,
    net_hops,
)

SEEDS = (0, 7, 42, 1234, 9001)
MAPPINGS = ("v1_ckc_total", "v2_partial")
STATEFUL_ARMS = ("A", "AB")
FULL_CAPABILITY = {"host_stack", "curr_host", "curr_ports"}


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


def _state(profile, seed, arm, lam, mapping):
    return AttackerState(
        seed=seed,
        modulators=(
            iterated_utility_modulator_for(
                profile, arm=arm, lam=lam, mapping_version=mapping
            ),
        ),
    )


# --- gate 1: the ablation is exact, for every arm ---------------------------


@pytest.mark.parametrize("arm", ARMS)
@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_lambda_zero_reproduces_the_unmodulated_record_stream(arm, profile, mapping):
    """U1, as a test rather than a run. ``x ** 0.0`` is exactly 1.0 in IEEE
    arithmetic for any finite positive ``x``, so at λ = 0 the composition reduces
    to the two-factor rule whatever the ratio's value was — which is why the
    changes to cost and benefit cannot disturb it. Asserted rather than
    short-circuited: the identity is a property of the maths, and testing it that
    way is a stronger claim than special-casing zero in the modulator.
    """
    for seed in SEEDS:
        for scheme in (None, "simultaneous"):
            kwargs = dict(seed=seed, mapping_version=mapping, mtd_scheme=scheme)
            without = run_movement(profile, horizon=3_000, **kwargs)
            conditioned = run_movement(
                profile,
                horizon=3_000,
                attacker_state=_state(profile, seed, arm, 0.0, mapping),
                **kwargs,
            )
            assert _fields(conditioned.records) == _fields(without.records), (
                f"lambda=0 perturbed arm={arm} {profile}/{mapping}/seed={seed}/"
                f"mtd={scheme}"
            )
            assert conditioned.reached_objective == without.reached_objective
            assert conditioned.termination_time == without.termination_time


@pytest.mark.parametrize("arm", ARMS)
def test_lambda_zero_logs_no_non_unit_factor(arm):
    """The record stream is not the only witness: the state's own per-decision
    log records no non-unit factor either, so an experiment reading the log
    cannot mistake an ablation arm for a conditioned one."""
    state = _state("aggregate", 42, arm, 0.0, "v2_partial")
    run_movement(
        "aggregate", seed=42, horizon=3_000,
        mapping_version="v2_partial", attacker_state=state,
    )
    assert state.log, "no routing decision was logged"
    assert all(entry["factors"] == {} for entry in state.log)


# --- gate 2: no new declared value ------------------------------------------


def test_the_iterated_model_declares_no_new_magnitude():
    """The brief's central claim. Every number the iterated model consumes comes
    from an artefact that already existed and was already scrutinised: the three
    declared parameters, the duration catalogue, the precondition relation, the
    controller mapping and the profile nets. A new magnitude would need a tier, a
    band, a sweep and a ledger entry — and would falsify the premise that this is
    derived rather than declared.
    """
    rules = load_utility_rules()
    mod = iterated_utility_modulator_for(
        "pure_steal", arm="AB", mapping_version="v1_ckc_total"
    )

    assert mod.lam == rules.model.lam
    assert mod.cost_floor_s == rules.model.cost_floor_s
    # The cost catalogue is the durations, passed through untouched.
    assert mod.cost == rules.cost
    # The benefit table is rho-generated: every cell is 1.0 or an integer power
    # of the declared rho. No cell is a free-standing number.
    rho = rules.model.rho
    for value in mod.benefit.values():
        assert value == 1.0 or any(
            value == pytest.approx(rho ** k) for k in range(1, 25)
        ), f"benefit {value!r} is not 1.0 nor a power of the declared rho"
    # The enabling chain is priced from the catalogue, floored — no third scale.
    for verb, price in mod.capability_cost.verb_cost.items():
        assert price in {
            max(c, rules.model.cost_floor_s) for c in rules.cost.values()
        }, f"{verb} priced at {price}, which is not a floored catalogue duration"


def test_the_module_reads_no_artefact_beyond_the_declared_four():
    """A structural companion to the check above: the module's source names no
    data path of its own. Every artefact it consumes arrives through the loaders
    of the modules that already own them, so there is no second home for a value
    and no path by which one could be introduced without a review noticing."""
    from mtdsim.l3_simulation.movement import utility_iterated

    source = inspect.getsource(utility_iterated)
    body = source.split('"""', 2)[-1]  # exclude the module docstring's prose
    assert ".json" not in body, "the module names a data file directly"
    assert "data/ogasp" not in body


# --- gate 3 (the laundering check): benefit* is not the base weights ---------


def test_benefit_star_is_not_monotone_in_the_base_out_weight():
    """The serious hazard in change B. ``hops`` is measured over the same graph
    the base transition weights live on, so the two are closer than the shipped
    family's stage-gap term ever was to them. They remain different quantities —
    the base weights are corpus flow *proportions* (how often analysts drew this
    move), ``hops`` is a distance to the objective — but that must be *shown*,
    not asserted, or the term is laundering frequency as value.

    The check: over every edge of every profile's net, benefit* must invert
    against the base out-weight in **both** directions. A monotone relationship
    would mean the attacker's declared value could be read off the corpus
    frequency, which is the failure mode.
    """
    rules = load_utility_rules()
    table = benefit_values_net(rules)
    checked = 0
    for profile in rules.profiles:
        net = load_routing_net(profile)
        edges = [
            (weight, table[profile][dst])
            for src in net.places
            for dst, weight in net.base_out_weights(src).items()
        ]
        assert len(edges) > 1
        rises = falls = 0
        for i, (w_i, b_i) in enumerate(edges):
            for w_j, b_j in edges[i + 1:]:
                if w_i < w_j and b_i < b_j:
                    rises += 1
                elif w_i < w_j and b_i > b_j:
                    falls += 1
        assert rises and falls, (
            f"{profile}: benefit* is monotone in the base out-weight "
            f"(concordant={rises}, discordant={falls}) — the term restates the "
            "corpus frequency rather than measuring distance to the objective"
        )
        checked += 1
    assert checked == len(rules.profiles)


def test_benefit_star_keeps_the_two_separations_the_shipped_family_earned():
    """§4.1's two properties must survive the change of graph: benefit is a
    property of the **destination and the profile**, never of the source (the
    overlay's distance kernel is a signed source→destination offset), and it
    **differs between profiles for the same tactic** (the kernel never does).
    Change B alters which graph the distance is measured in, not what is graded.
    """
    rules = load_utility_rules()
    table = benefit_values_net(rules)
    # Source-independence is structural: the table is keyed on (profile, tactic).
    assert all(set(cells) == set(rules.tactics) for cells in table.values())
    # Profile-variance, on the sharpest case the shipped record names.
    c2 = {p: table[p]["command-and-control"] for p in rules.profiles}
    assert c2["infrastructure_setup"] == 1.0  # its own declared objective
    assert c2["pure_steal"] < 1.0  # merely instrumental there
    assert len(set(c2.values())) > 1


# --- change A: the expected-cost term ---------------------------------------


@pytest.mark.parametrize("mapping", MAPPINGS)
def test_the_capability_closure_is_fully_connected_on_both_mappings(mapping):
    """The unreachable fallback exists so an unpriceable chain cannot drive the
    utility to zero and engage the seam's stall rule. This asserts it is never
    actually charged: on both shipped mappings every verb's requirement is
    establishable from the empty capability set, so the fallback is a guard and
    not a silent operating value."""
    mod = iterated_utility_modulator_for("pure_steal", arm="A", mapping_version=mapping)
    cc = mod.capability_cost
    for verb in cc.model.requires:
        cost = cc.enabling_cost(verb, set())
        assert cost < cc.unreachable_cost, (
            f"{verb} unreachable from the empty capability set under {mapping}"
        )


@pytest.mark.parametrize("mapping", MAPPINGS)
def test_expected_cost_is_the_declared_duration_once_ready(mapping):
    """The property that makes this a repair rather than a different model: the
    expected cost *is* the declared cost when the attacker is ready to act, so
    the change is confined to the situation the defect concerns. An exploit-shaped
    tactic costs 4.5 s once its prerequisite is met, and more only before."""
    rules = load_utility_rules()
    mod = iterated_utility_modulator_for("pure_steal", arm="A", mapping_version=mapping)
    mod.held = set(FULL_CAPABILITY)
    for tactic in rules.tactics:
        assert mod.cost_of(tactic) == max(rules.cost[tactic], rules.model.cost_floor_s)


@pytest.mark.parametrize("mapping", MAPPINGS)
def test_expected_cost_prices_the_wall_when_unready(mapping):
    """The defect's own signature, inverted. From the empty capability set every
    tactic whose verb needs a prerequisite costs strictly more than its declared
    duration, and the exploit-shaped tactic — the one the shipped model prefers
    31-fold over the reconnaissance that enables it — is among them."""
    rules = load_utility_rules()
    mod = iterated_utility_modulator_for("pure_steal", arm="A", mapping_version=mapping)
    assert mod.held == set()
    raised = [
        t for t in rules.tactics
        if mod.cost_of(t) > max(rules.cost[t], rules.model.cost_floor_s)
    ]
    assert raised, "no tactic's cost rose from the empty capability set"
    # Reconnaissance dispatches SCAN_HOST, which requires nothing: it is the one
    # tactic that is always ready, and it must never be surcharged.
    assert mod.cost_of("reconnaissance") == max(
        rules.cost["reconnaissance"], rules.model.cost_floor_s
    )


def test_the_repair_reverses_the_defects_worked_example():
    """The defect stated once, and undone. ``cost_model_plain.md`` §2.2a records
    ``pure_steal`` at *collection* preferring credential-access over the
    objective it is walking toward, because a 4.5 s tactic looks like a bargain
    even when it cannot run. From the empty capability set the iterated model
    prefers exfiltration instead; once the prerequisites are actually held it
    returns to the shipped preference, because then the bargain is real.
    """
    menu = {
        "exfiltration": 0.571,
        "command-and-control": 0.286,
        "credential-access": 0.143,
        "stealth": 0.0,
    }
    shipped = utility_modulator_for("pure_steal", lam=1.0)
    iterated = iterated_utility_modulator_for(
        "pure_steal", arm="A", lam=1.0, mapping_version="v1_ckc_total"
    )
    shipped_f = shipped.factors(None, "collection", menu)
    assert shipped_f["credential-access"] > shipped_f["exfiltration"]

    unready = iterated.factors(None, "collection", menu)
    assert unready["exfiltration"] > unready["credential-access"]

    iterated.held = set(FULL_CAPABILITY)
    ready = iterated.factors(None, "collection", menu)
    assert ready == pytest.approx(shipped_f)


@pytest.mark.parametrize("mapping", MAPPINGS)
def test_the_mtd_response_is_layer_specific(mapping):
    """The channel the whole repair opens, and the one U3b tests in the sweep.
    ``mtd_clears`` declares that a network-layer mutation destroys ``curr_host``
    and ``curr_ports`` while an application-layer one destroys nothing, so the
    cost term can see the first and structurally cannot see the second. A model
    that responded uniformly across the two would not be responding through the
    mechanism claimed."""
    menu = {"exfiltration": 0.5, "credential-access": 0.5, "command-and-control": 0.5}
    mod = iterated_utility_modulator_for(
        "pure_steal", arm="A", lam=1.0, mapping_version=mapping
    )
    mod.held = set(FULL_CAPABILITY)
    before = mod.factors(None, "collection", menu)

    mod.observe_mtd_interrupt("application")
    assert mod.held == FULL_CAPABILITY
    assert mod.factors(None, "collection", menu) == pytest.approx(before)

    mod.observe_mtd_interrupt("network")
    assert mod.held == {"host_stack"}
    assert mod.factors(None, "collection", menu) != pytest.approx(before)


def test_the_enabling_chain_respects_ordering_rather_than_summing():
    """``ENUM_HOST`` produces ``curr_host`` and **clears** ``curr_ports``, so the
    relation has ordering effects and a formula summing the durations of an
    unordered set of missing prerequisites would be wrong. From ``{host_stack}``
    the cheapest route to ``EXPLOIT_VULN`` must therefore run ENUM_HOST *then*
    SCAN_PORT, and cost both — not just the one that is missing."""
    model = PreconditionModel.load()
    assert "curr_ports" in model.clears["ENUM_HOST"]
    rules = load_utility_rules()
    cc = CapabilityCostModel.build(
        tactic_to_verb={"reconnaissance": "SCAN_HOST", "resource-development": "ENUM_HOST",
                        "initial-access": "SCAN_PORT", "execution": "EXPLOIT_VULN"},
        cost=rules.cost,
        cost_floor_s=rules.model.cost_floor_s,
        model=model,
    )
    enum, scan_port = cc.verb_cost["ENUM_HOST"], cc.verb_cost["SCAN_PORT"]
    assert cc.enabling_cost("EXPLOIT_VULN", {"host_stack"}) == pytest.approx(
        enum + scan_port
    )
    # And holding curr_host but not curr_ports costs the port scan alone.
    assert cc.enabling_cost(
        "EXPLOIT_VULN", {"host_stack", "curr_host"}
    ) == pytest.approx(scan_port)


# --- change B: the enabling-value benefit -----------------------------------


def test_net_hops_measures_distance_through_the_profiles_own_net():
    """The change is *which graph the distance is measured in*. An objective sits
    at zero hops from itself, and the counts are the routing net's own directed
    shortest paths rather than the lifecycle ordering's stage separations."""
    rules = load_utility_rules()
    for profile in rules.profiles:
        hops = net_hops(profile, rules.objectives[profile])
        net = load_routing_net(profile)
        for objective in rules.objectives[profile]:
            if objective in net.places:
                assert hops[objective] == 0
        assert set(hops) <= set(net.places)
    # And the two graphs genuinely disagree, or the change would be vacuous.
    disagreements = sum(
        1
        for profile in rules.profiles
        for tactic, hop in net_hops(profile, rules.objectives[profile]).items()
        if hop != stage_gap(tactic, profile, rules)
    )
    assert disagreements > 0


def test_unreachable_cells_take_the_stage_gap_value_never_zero():
    """§2.2's second hazard, and it is not hypothetical: every profile has at
    least one tactic with no directed net path to its objective, and some
    profiles have tactics their net has no place for at all. Those cells keep the
    shipped stage-gap value. A zero would make this a ``may_zero`` modulator
    under the seam's stall rule and would need the no-stall check re-run."""
    rules = load_utility_rules()
    table = benefit_values_net(rules)
    shipped = load_benefit()
    fallbacks = 0
    for profile in rules.profiles:
        hops = net_hops(profile, rules.objectives[profile])
        for tactic in rules.tactics:
            assert table[profile][tactic] > 0.0
            if tactic in rules.objectives[profile] or tactic in hops:
                continue
            fallbacks += 1
            assert table[profile][tactic] == pytest.approx(shipped[profile][tactic])
    assert fallbacks >= len(rules.profiles), (
        "the stage-gap fallback fired for fewer profiles than the nets require"
    )


def test_enabling_value_lifts_reconnaissance_where_it_leads_to_the_objective():
    """The numerator half of the repair. Under ``pure_steal`` reconnaissance is
    two hops from exfiltration through the profile's own net but four lifecycle
    stages away, so grading it by the net raises its value — while a profile in
    which it genuinely is remote keeps it low. The term credits *enabling*, not
    earliness."""
    rules = load_utility_rules()
    net_table = benefit_values_net(rules)
    shipped = load_benefit()
    assert net_table["pure_steal"]["reconnaissance"] > shipped["pure_steal"]["reconnaissance"]
    # Not a blanket promotion: it must remain profile-specific, or it is just a
    # flatter table rather than a different measurement.
    assert any(
        net_table[p]["reconnaissance"] < shipped[p]["reconnaissance"]
        for p in rules.profiles
    )


# --- the arms, the seam, and determinism ------------------------------------


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_the_declared_arm_reproduces_the_shipped_modulator_exactly(profile, mapping):
    """The current model must stay runnable — every recorded figure in the
    project was produced by it, and the comparison arms need it. Running it
    through the iterated construction path must therefore give bit-identical
    factors, or the sweep's baseline arm is not the model on record."""
    shipped = utility_modulator_for(profile, lam=1.0)
    declared = iterated_utility_modulator_for(
        profile, arm="declared", lam=1.0, mapping_version=mapping
    )
    net = load_routing_net(profile)
    compared = 0
    for src in net.places:
        menu = net.base_out_weights(src)
        if not menu:
            continue
        assert declared.factors(None, src, menu) == shipped.factors(None, src, menu)
        compared += 1
    assert compared


@pytest.mark.parametrize("arm", ARMS)
def test_no_factor_is_ever_zero_across_the_declared_bands(arm):
    """``may_zero`` stays absent, and it stays a proof rather than a hope.
    Benefit is strictly positive (1.0 at an objective, a positive power of rho
    elsewhere, the stage-gap value where the net has no path) and cost is a
    floored duration plus a non-negative enabling charge, so the utility is
    strictly positive and the seam's stall rule is never engaged."""
    for profile in PROFILES:
        net = load_routing_net(profile)
        for lam in (0.0, 0.5, 1.0, 2.0, 4.0):
            mod = iterated_utility_modulator_for(
                profile, arm=arm, lam=lam, mapping_version="v2_partial"
            )
            for held in (set(), {"host_stack"}, set(FULL_CAPABILITY)):
                mod.held = set(held)
                for src in net.places:
                    menu = net.base_out_weights(src)
                    if not menu:
                        continue
                    for dst, factor in mod.factors(None, src, menu).items():
                        assert factor > 0.0, f"{profile}/{src}->{dst} zeroed at λ={lam}"
    assert not getattr(IteratedUtilityModulator, "may_zero", False)


@pytest.mark.parametrize("arm", STATEFUL_ARMS)
def test_a_stateful_conditioned_run_is_reproducible(arm):
    """SIM-05, re-verified because the modulator is now stateful. ``cost*`` reads
    the attacker's own trajectory against a declared relation; it draws from no
    random stream and estimates nothing, so the same seed reproduces exactly."""
    for scheme in (None, "simultaneous"):
        runs = [
            run_movement(
                "aggregate", seed=11, horizon=3_000, mapping_version="v2_partial",
                mtd_scheme=scheme,
                attacker_state=_state("aggregate", 11, arm, 1.0, "v2_partial"),
            )
            for _ in range(2)
        ]
        assert _fields(runs[0].records) == _fields(runs[1].records)


@pytest.mark.parametrize("arm", ("A", "B", "AB"))
def test_each_arm_visibly_changes_the_walk_at_the_declared_lambda(arm):
    """The other half of the ablation: at the declared λ = 1 each arm's walk is
    not the λ = 0 walk. An arm that changed nothing would make its half of the
    sweep vacuous, so this is asserted as directly as the null-equivalence is."""
    changed = 0
    for profile in PROFILES:
        null = run_movement(
            profile, seed=3, horizon=3_000, mapping_version="v2_partial",
            attacker_state=_state(profile, 3, arm, 0.0, "v2_partial"),
        )
        live = run_movement(
            profile, seed=3, horizon=3_000, mapping_version="v2_partial",
            attacker_state=_state(profile, 3, arm, 1.0, "v2_partial"),
        )
        changed += _fields(null.records) != _fields(live.records)
    assert changed >= 3, f"arm {arm} changed only {changed} of 5 profiles"


def test_the_expected_cost_arms_track_capability_from_their_own_trajectory():
    """The statefulness is real and it is in-layer. Over a run the modulator's
    held capability set is populated by the attacker's own actions against the
    declared relation — no substrate read — which is what keeps the axis-8
    scheme-awareness exclusion untouched."""
    mod = iterated_utility_modulator_for(
        "aggregate", arm="A", lam=1.0, mapping_version="v2_partial"
    )
    state = AttackerState(seed=5, modulators=(mod,))
    run_movement(
        "aggregate", seed=5, horizon=3_000,
        mapping_version="v2_partial", attacker_state=state,
    )
    assert mod.held, "no capability was ever established over a full run"
    assert mod.held <= FULL_CAPABILITY


def test_an_unknown_arm_is_refused():
    """The arm selector is a closed set: a typo must fail at construction rather
    than silently running the shipped model under an iterated label."""
    with pytest.raises(ValueError, match="unknown arm"):
        iterated_utility_modulator_for("pure_steal", arm="C")
