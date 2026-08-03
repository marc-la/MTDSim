"""The FSM-succession overlay (composition-register factor 9).

The factor scores no axis. What these tests pin is the declared relation's
fidelity to the thing it transcribes, and the two properties that decide whether
the dial is usable.

The hard gate is the one every modulator carries: the null arm (``α = 0``)
reproduces today bit for bit across every profile, several seeds, both mappings
and both MTD conditions.

The load-bearing gate is different from any previous factor's, and it is the
**runtime cross-examination**: the declared succession must explain every verb
transition the *native* attacker actually performs, under no MTD and under MTD.
That check caught a real omission during the build — ``ENUM_HOST → SCAN_HOST``,
reachable through the empty-stack guard on ENUM_HOST's own loop branch — which no
amount of reading the dispatch wrappers had surfaced.

Relation: ``data/ogasp/controller/fsm_succession.json``.
Design record: ``docs/implementation/pipeline/ogasp/fsm_succession_overlay.md``.
"""
from __future__ import annotations

import dataclasses
import random
from collections import Counter

import numpy as np
import pytest
import simpy

from mtdsim.l3_simulation.movement.alignment import AlignmentError
from mtdsim.l3_simulation.movement.learning_readiness import (
    PreconditionModel,
    load_tactic_to_verb,
)
from mtdsim.l3_simulation.movement.net import PROFILES
from mtdsim.l3_simulation.movement.run import run_movement
from mtdsim.l3_simulation.movement.state import AttackerState
from mtdsim.l3_simulation.movement.succession import (
    FsmSuccession,
    FsmSuccessionModulator,
    load_succession_parameters,
    succession_stall_report,
)

SEEDS = (0, 7, 42, 1234, 9001)
MAPPINGS = (None, "v2_partial")

#: One dispatched EXPLOIT_VULN phase appends one statistics row **per
#: vulnerability** (attack_operation.py, the loop in ``_do_exploit_vuln``), so the
#: native record stream carries a self-loop the FSM does not have. The movement
#: layer takes one outcome per place visit and never sees it. Excluded by name,
#: with the reason, rather than by widening the declared relation — widening it
#: would license the dial to hold the token on exploitation indefinitely.
_RECORD_GRANULARITY_ARTEFACT = {("EXPLOIT_VULN", "EXPLOIT_VULN")}


def _fields(records):
    return [dataclasses.asdict(r) for r in records]


def _modulator(alpha, mapping=None, **kwargs):
    return FsmSuccessionModulator(
        alpha=alpha, tactic_to_verb=load_tactic_to_verb(mapping), **kwargs
    )


def _state(alpha, seed, mapping=None, **kwargs):
    return AttackerState(seed=seed, modulators=(_modulator(alpha, mapping, **kwargs),))


@pytest.fixture(scope="module")
def fsm() -> FsmSuccession:
    return FsmSuccession.load()


# --- 1. the null arm is bit-identical to today ------------------------------


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("mapping", MAPPINGS)
def test_alpha_zero_reproduces_the_current_record_stream_field_for_field(
    profile, mapping
) -> None:
    """At α = 0 the modulator tracks the FSM state and the capability cursor and
    acts on neither, so the walk must be the walk that has always run."""
    for seed in SEEDS:
        for scheme in (None, "simultaneous"):
            kwargs = dict(seed=seed, mapping_version=mapping, mtd_scheme=scheme)
            without = run_movement(profile, horizon=3_000, **kwargs)
            null = run_movement(
                profile,
                horizon=3_000,
                attacker_state=_state(0.0, seed, mapping),
                **kwargs,
            )
            assert _fields(null.records) == _fields(without.records), (
                f"alpha=0 perturbed {profile}/{mapping}/seed={seed}/mtd={scheme}"
            )
            assert null.compromised_count == without.compromised_count
            assert null.termination_time == without.termination_time


# --- 2. the runtime cross-examination — the load-bearing gate ---------------


def _native_transitions(seeds, scheme=None, mechanism=None, horizon=15_000):
    """The native attacker's own observed verb transitions — ground truth."""
    from mtdnetwork.component.adversary import Adversary
    from mtdnetwork.component.time_network import TimeNetwork
    from mtdnetwork.data.constants import ATTACKER_THRESHOLD
    from mtdnetwork.operation.attack_operation import AttackOperation

    from mtdsim.l3_simulation.movement.run import GEOMETRY

    observed: Counter = Counter()
    for seed in seeds:
        random.seed(seed)
        np.random.seed(seed)
        env = simpy.Environment()
        end_event = env.event()
        network = TimeNetwork(**GEOMETRY)
        adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
        operation = AttackOperation(
            env=env, end_event=end_event, adversary=adversary, proceed_time=0
        )
        operation.proceed_attack()
        if scheme:
            from mtdnetwork.operation.mtd_operation import MTDOperation
            from mtdnetwork.statistic.security_metric_statistics import (
                SecurityMetricStatistics,
            )

            MTDOperation(
                security_metrics_record=SecurityMetricStatistics(),
                env=env,
                end_event=end_event,
                network=network,
                scheme=scheme,
                attack_operation=operation,
                proceed_time=0,
                mtd_trigger_interval=200,
                custom_strategies=mechanism,
                adversary=adversary,
            ).proceed_mtd()
        env.run(until=horizon)
        sequence = list(adversary.get_attack_stats().get_record()["name"])
        for a, b in zip(sequence, sequence[1:]):
            observed[(a, b)] += 1
    return observed


@pytest.mark.parametrize("scheme", (None, "simultaneous"))
def test_the_declared_succession_explains_every_native_transition(fsm, scheme) -> None:
    """The relation is a transcription, so the substrate is its oracle. Every verb
    transition the inherited attacker actually performs must be licensed by the
    declared relation — under MTD too, where the interrupt table takes over."""
    observed = _native_transitions((0, 1, 2), scheme=scheme)
    assert observed, "the native attacker produced no transitions to check against"
    interrupt_successors = {v for s in fsm.interrupt.values() for v in s}
    unexplained = []
    for (source, destination), count in observed.items():
        if (source, destination) in _RECORD_GRANULARITY_ARTEFACT:
            continue
        row = fsm.succession.get(source, {})
        licensed = row.get("success", frozenset()) | row.get("failure", frozenset())
        if scheme is not None:
            licensed = licensed | interrupt_successors
        if destination not in licensed:
            unexplained.append(((source, destination), count))
    assert not unexplained, f"native transitions the relation cannot explain: {unexplained}"


def test_the_relation_does_not_license_the_record_granularity_self_loop(fsm) -> None:
    """The most common transition in the native record stream is intra-phase and
    must stay out of the relation — licensing it would let the dial hold the token
    on exploitation for as long as it liked."""
    assert "EXPLOIT_VULN" not in fsm.succession["EXPLOIT_VULN"]["success"]
    assert "EXPLOIT_VULN" not in fsm.succession["EXPLOIT_VULN"]["failure"]


# --- 3. the relation against Brown Fig 3 (the intent side) ------------------


def test_the_relation_matches_the_transcribed_flowchart(fsm) -> None:
    """Brown Fig 3, from the intent spec §j, box by box. Cross-examined against
    the intent rather than only against the code, because the two are allowed to
    disagree and the disagreements must be the recorded ones, not new ones."""
    # box 1 -> box 2
    assert fsm.entry == "SCAN_HOST"
    assert fsm.succession["SCAN_HOST"]["success"] == frozenset({"ENUM_HOST"})
    # box 7 Success -> box 9 ; Failure -> box 8
    assert fsm.succession["EXPLOIT_VULN"]["success"] == frozenset({"SCAN_NEIGHBOR"})
    assert fsm.succession["EXPLOIT_VULN"]["failure"] == frozenset({"BRUTE_FORCE"})
    # box 8 Success -> box 9 ; Failure -> box 10 (another host -> 2, else -> 1)
    assert fsm.succession["BRUTE_FORCE"]["success"] == frozenset({"SCAN_NEIGHBOR"})
    assert fsm.succession["BRUTE_FORCE"]["failure"] == frozenset(
        {"ENUM_HOST", "SCAN_HOST"}
    )
    # box 9 -> box 2, and the intent spec flags that 9 returns to 2, not to 10
    assert fsm.succession["SCAN_NEIGHBOR"]["success"] == frozenset({"ENUM_HOST"})
    # Fig 3 draws box 4 -> box 5 unconditionally while the prose branches on
    # stuffing's failure; the declared set contains both, so it is compatible
    # with either reading (the intent spec records the tension unresolved).
    assert fsm.succession["SCAN_PORT"]["success"] == frozenset(
        {"SCAN_NEIGHBOR", "EXPLOIT_VULN"}
    )


def test_zhang_fig7_interrupt_scoping(fsm) -> None:
    """Zhang Fig 7: the network-layer enclosure spans every action and returns to
    Scan Host; the application-layer enclosure spans Phases 1-3 and returns to
    Phase 1. The reserve row is Brown §III-D(3) as Marc's D-07 disposition."""
    assert fsm.after_interrupt("network") == frozenset({"SCAN_HOST"})
    assert fsm.after_interrupt("application") == frozenset({"SCAN_PORT"})
    assert fsm.after_interrupt("reserve") == frozenset({"EXPLOIT_VULN"})
    # An unrecorded resource restarts at the entry verb rather than licensing all.
    assert fsm.after_interrupt("unknown-layer") == frozenset({"SCAN_HOST"})


def test_the_progressive_verbs_are_re_homed_onto_the_controller_seam(fsm) -> None:
    """Factor 8 had to carry this set as a movement-layer constant because its
    brief barred touching the precondition relation. It is substrate-specific, so
    it belongs on the controller seam, and here it is."""
    assert fsm.progressive == frozenset({"SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE"})
    assert "ENUM_HOST" not in fsm.progressive


def test_a_relation_over_a_foreign_vocabulary_is_refused(fsm) -> None:
    model = PreconditionModel.load()
    rogue = dataclasses.replace(
        fsm, succession={**fsm.succession, "TELEPORT": {"success": frozenset(), "failure": frozenset()}}
    )
    with pytest.raises(AlignmentError):
        rogue.validate_against(model)


# --- 4. the factor's arithmetic ---------------------------------------------


def test_dwell_only_destinations_are_never_attenuated() -> None:
    """Transparency: a place that fires no verb cannot violate the succession, so
    it keeps full weight even at the limiting end."""
    modulator = _modulator(1.0, "v2_partial")
    modulator.targets = frozenset({"BRUTE_FORCE"})
    modulator.cursor.held = frozenset({"host_stack", "curr_host"})
    out = {"credential-access": 0.4, "collection": 0.3, "command-and-control": 0.3}
    factors = modulator.factors(None, "discovery", out)
    assert factors["credential-access"] == 1.0  # the FSM target
    assert factors["collection"] == 1.0  # dwell-only, transparent
    assert factors["command-and-control"] == 0.0  # SCAN_NEIGHBOR, off-target


@pytest.mark.parametrize("alpha, off", [(0.25, 0.75), (0.5, 0.5), (0.9, 0.1)])
def test_alpha_is_a_float_dial_not_a_switch(alpha, off) -> None:
    modulator = _modulator(alpha, "v2_partial")
    modulator.targets = frozenset({"BRUTE_FORCE"})
    modulator.cursor.held = frozenset({"host_stack", "curr_host"})
    factors = modulator.factors(
        None, "discovery", {"credential-access": 0.5, "command-and-control": 0.5}
    )
    assert factors["credential-access"] == 1.0
    assert factors["command-and-control"] == pytest.approx(off)


def test_may_zero_is_claimed_only_at_the_limiting_end() -> None:
    assert _modulator(0.0).may_zero is False
    assert _modulator(0.75).may_zero is False
    assert _modulator(1.0).may_zero is True
    assert _modulator(1.0, off_floor=0.02).may_zero is False


def test_the_abstention_rule_makes_a_stall_structurally_impossible() -> None:
    """Where the net offers no FSM-legal move, the factor attenuates nothing —
    which is both what keeps it a concession rather than a replacement, and what
    makes an emptied out-set unreachable by construction."""
    modulator = _modulator(1.0, "v2_partial")
    modulator.targets = frozenset({"BRUTE_FORCE"})
    modulator.cursor.held = frozenset({"host_stack", "curr_host"})
    # An out-set of purely off-target verb-firing places.
    factors = modulator.factors(
        None, "discovery", {"command-and-control": 0.5, "reconnaissance": 0.5}
    )
    assert factors == {}
    assert modulator.abstentions == 1


def test_alpha_outside_the_unit_interval_is_refused() -> None:
    for bad in (-0.01, 1.01):
        with pytest.raises(ValueError):
            _modulator(bad)


# --- 5. the FSM state advances the way the substrate's does -----------------


def test_a_dwell_only_visit_does_not_advance_the_fsm_state() -> None:
    modulator = _modulator(1.0, "v2_partial")
    modulator.targets = frozenset({"SCAN_PORT"})
    modulator.observe_visit("collection")  # dwell-only
    modulator.observe_verdict("collection", "none")
    assert modulator.targets == frozenset({"SCAN_PORT"})


def test_the_pivot_survives_a_compromise_which_is_what_factor_8_lacked() -> None:
    """The property this factor exists for. After a successful exploit the FSM
    runs SCAN_NEIGHBOR and then ENUM_HOST — it pivots to a fresh host. Factor 8's
    capability-distance target never did, which is why its limiting end owned one
    host forever."""
    modulator = _modulator(1.0, "v2_partial")
    modulator.cursor.held = frozenset({"host_stack", "curr_host", "curr_ports"})
    modulator.observe_visit("execution")  # EXPLOIT_VULN
    modulator.observe_verdict("execution", "success")
    assert modulator.targets == frozenset({"SCAN_NEIGHBOR"})
    modulator.observe_visit("command-and-control")  # SCAN_NEIGHBOR
    modulator.observe_verdict("command-and-control", "success")
    assert modulator.targets == frozenset({"ENUM_HOST"})


def test_an_interrupt_overrides_the_succession(fsm) -> None:
    modulator = _modulator(1.0, "v2_partial")
    modulator.cursor.held = frozenset({"host_stack", "curr_host", "curr_ports"})
    modulator.observe_visit("execution")
    modulator.observe_mtd_interrupt("network")
    modulator.observe_verdict("execution", "failure")
    # Not BRUTE_FORCE (the failure successor) — the interrupt handler wins.
    assert modulator.targets == frozenset({"SCAN_HOST"})
    assert "curr_host" not in modulator.cursor.held  # position severed


def test_the_capability_fallback_fires_when_the_successor_cannot_run() -> None:
    """The seam between the two controller relations: the succession says what
    comes next, the closure says what must happen first when it cannot."""
    modulator = _modulator(1.0, "v2_partial")
    modulator.targets = frozenset({"EXPLOIT_VULN"})  # needs curr_host + curr_ports
    modulator.cursor.held = frozenset()  # holds nothing
    effective = modulator.effective_targets()
    assert effective == frozenset({"SCAN_HOST"}), effective
    assert modulator.fallbacks == 1


# --- 6. the exhaustive no-stall check ---------------------------------------


def test_the_no_stall_check_is_empty_across_the_whole_declared_space() -> None:
    """Quantifies over every non-empty subset of the verb vocabulary — a strict
    superset of every target set any run can reach, including every capability
    fallback — crossed with every profile net, mapping, overlay version, verdict,
    source place and one-shot retrace suppression."""
    assert succession_stall_report() == []


def test_the_no_stall_check_has_teeth() -> None:
    """A checker that cannot fail proves nothing. Without the abstention rule the
    same space contains tens of thousands of emptied out-sets, and `v1_ckc_total`
    is the reason — it maps every tactic to a verb, so it has no transparent
    dwell-only structure to fall back on."""
    from mtdsim.l3_simulation.controller import load_controller
    from mtdsim.l3_simulation.movement.net import load_routing_net

    t2v = load_controller(version="v1_ckc_total").as_dict()
    assert all(v is not None for v in t2v.values()), "v1 gained a dwell-only tactic"
    net = load_routing_net("aggregate", with_synthetic_overlay=True)
    # Some source's whole live out-set fires verbs outside a reachable target set.
    starved = False
    for src in net.places:
        live = {d for d, w in net.base_out_weights(src).items() if w > 0.0}
        if live and not any(t2v.get(d) in {"BRUTE_FORCE"} or t2v.get(d) is None for d in live):
            starved = True
            break
    assert starved, "no source could starve, so the abstention rule guards nothing"


# --- 7. the declared parameter ----------------------------------------------


def test_the_declared_value_is_the_null_and_the_band_reaches_both_poles() -> None:
    params = load_succession_parameters()
    assert params.alpha == 0.0
    assert params.sweep[0] == 0.0 and params.sweep[-1] == 1.0
    assert len(params.sweep) >= 5


def test_the_declared_modulator_is_the_null_unless_an_arm_overrides_it() -> None:
    t2v = load_tactic_to_verb("v2_partial")
    assert FsmSuccessionModulator.declared(tactic_to_verb=t2v).alpha == 0.0
    assert (
        FsmSuccessionModulator.declared(tactic_to_verb=t2v, alpha=0.35).alpha == 0.35
    )


# --- 8. the factor visibly changes the walk ---------------------------------


def test_a_non_zero_alpha_changes_the_walk() -> None:
    kwargs = dict(seed=0, mapping_version="v2_partial", mtd_scheme="simultaneous")
    null = run_movement("pure_steal", horizon=3_000, **kwargs)
    biased = run_movement(
        "pure_steal",
        horizon=3_000,
        attacker_state=_state(1.0, 0, "v2_partial"),
        **kwargs,
    )
    assert [r.place for r in biased.records] != [r.place for r in null.records]
