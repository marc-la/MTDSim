"""The axis-measurement suite's unit gate (measurement-suite handoff, gate 1).

Every measure is exercised on a hand-constructed record stream whose expected
value is worked out by hand in the test — no simulation behind the unit tests.
The two seeded *integration* tests at the bottom are the exceptions the handoff
names: the MTD-confusion-penalty derivation must be tested against a known
seeded run (step 5), and the cross-arm subset must compute on both arms from
one seeded run of each (gate 4b).
"""
from __future__ import annotations

import math

import pytest

from mtdsim.l3_simulation.movement.attacker import (
    ACTION_BEARING,
    DWELL_ONLY,
    MovementRecord,
)
from mtdsim.l3_simulation.movement.measures import (
    ActionMixShift,
    action_records,
    actions_per_distinct_host,
    baseline_ledger,
    comparable_from_baseline,
    comparable_from_movement,
    cost_ledger,
    deepest_successful_stage,
    deepest_visited_stage,
    distinct_place_count,
    distinct_place_curve,
    distinct_prefixes,
    distinct_sequences,
    failure_routing_rate,
    foothold_retentions,
    interrupt_action_mix,
    interval_report,
    is_compromise,
    jsd,
    load_stage_of,
    mean_ci,
    mtd_penalty,
    n_successes,
    normalise,
    path_entropy,
    profile_divergence,
    recovery_times,
    successes_per_distinct_host,
    terminal_mode,
    terminal_place_distribution,
    visit_distribution,
    visit_records,
)
from mtdsim.l3_simulation.movement.statistics import MovementRunResult


# ---------------------------------------------------------------------------
# Record / run factories (hand-built streams)
# ---------------------------------------------------------------------------


def rec(
    place: str,
    *,
    step: int = 0,
    verb: str = "SCAN_HOST",
    outcome: str = "NONE",
    verdict: str = "success",
    interrupted: bool = False,
    blocked: bool = False,
    next_place: str | None = "somewhere",
    start: float = 0.0,
    end: float = 10.0,
    dwell: float = 10.0,
    interrupted_by: str = "",
    place_class: str = ACTION_BEARING,
) -> MovementRecord:
    return MovementRecord(
        profile="test",
        step_index=step,
        place=place,
        verb=verb,
        outcome=outcome,
        verdict=verdict,
        interrupted=interrupted,
        blocked=blocked,
        next_place=next_place,
        start_time=start,
        end_time=end,
        dwell=dwell,
        interrupted_by=interrupted_by,
        place_class=place_class,
    )


def run_of(
    *records: MovementRecord,
    profile: str = "test",
    seed: int = 0,
    reached: bool = False,
    termination: float | None = None,
    hosts: int = 0,
) -> MovementRunResult:
    return MovementRunResult(
        profile=profile,
        seed=seed,
        with_synthetic_overlay=True,
        records=tuple(records),
        reached_objective=reached,
        termination_time=(
            termination
            if termination is not None
            else (records[-1].end_time if records else 0.0)
        ),
        compromised_count=hosts,
    )


STAGES = {"recon": 0, "intrude": 1, "operate": 2, "objective": 3}


# ---------------------------------------------------------------------------
# Record views
# ---------------------------------------------------------------------------


def test_action_and_visit_views_split_the_stream():
    a = rec("recon", start=0, end=5, dwell=5)
    d = rec("think", verb="", verdict="", outcome="DWELL_ONLY",
            place_class=DWELL_ONLY, start=5, end=9, dwell=4)
    # bare terminal marker: no verb, zero dwell — a visit that never served
    t = rec("operate", verb="", verdict="", outcome="SIM_END",
            next_place=None, start=9, end=9, dwell=0.0)
    run = run_of(a, d, t)
    assert action_records(run) == (a,)
    assert visit_records(run) == (a, d)  # marker excluded, dwell-only kept


def test_is_compromise_uses_the_three_substrate_pairs():
    assert is_compromise(rec("x", verb="EXPLOIT_VULN", outcome="EXPLOIT_COMPROMISED"))
    assert is_compromise(rec("x", verb="BRUTE_FORCE", outcome="TRUE"))
    assert is_compromise(rec("x", verb="SCAN_PORT", outcome="TRUE"))
    assert not is_compromise(rec("x", verb="SCAN_PORT", outcome="FALSE"))
    assert not is_compromise(rec("x", verb="SCAN_HOST", outcome="TRUE"))


def test_mtd_penalty_derivation_on_hand_records():
    # Interrupted: dwell served 4 s, event closed at 9 s => penalty 5 s.
    hit = rec("x", interrupted=True, verdict="failure",
              start=0, end=9, dwell=4)
    assert mtd_penalty(hit) == pytest.approx(5.0)
    # Non-interrupted events derive no penalty by definition.
    clean = rec("x", start=9, end=15, dwell=6)
    assert mtd_penalty(clean) == 0.0


# ---------------------------------------------------------------------------
# §1 Progression
# ---------------------------------------------------------------------------


def test_distinct_place_curve_and_count():
    run = run_of(
        rec("recon", start=0, end=5, dwell=5, next_place="intrude"),
        rec("intrude", start=5, end=12, dwell=7, next_place="recon"),
        rec("recon", start=12, end=20, dwell=8, next_place=None),
    )
    assert distinct_place_curve(run) == ((0.0, 1), (5.0, 2))
    assert distinct_place_count(run) == 2


def test_deepest_visited_saturates_where_success_gated_does_not():
    # The token walks to the objective stage but only ever *succeeds* at
    # stage 0 — visiting saturates at 3, success-gated depth reads 0.
    run = run_of(
        rec("recon", verdict="success"),
        rec("operate", verdict="failure"),
        rec("objective", verdict="failure"),
    )
    assert deepest_visited_stage(run, STAGES) == 3
    assert deepest_successful_stage(run, STAGES) == 0


def test_deepest_stages_none_when_nothing_qualifies():
    no_success = run_of(rec("objective", verdict="failure"))
    assert deepest_successful_stage(no_success, STAGES) is None
    unmapped = run_of(rec("not-a-stage", verdict="success"))
    assert deepest_visited_stage(unmapped, STAGES) is None
    assert deepest_successful_stage(unmapped, STAGES) is None


def test_foothold_retentions_sever_vs_censor():
    run = run_of(
        # compromise at end=10
        rec("a", verb="BRUTE_FORCE", outcome="TRUE", start=0, end=10, dwell=10),
        # application-layer interrupt does NOT sever the foothold
        rec("b", verdict="failure", interrupted=True, interrupted_by="application",
            start=10, end=15, dwell=3),
        # network-layer interrupt severs at end=25
        rec("c", verdict="failure", interrupted=True, interrupted_by="network",
            start=15, end=25, dwell=6),
        # second compromise at end=30, never severed, run ends at 50
        rec("d", verb="SCAN_PORT", outcome="TRUE", start=25, end=30, dwell=5),
        termination=50.0,
    )
    ret = foothold_retentions(run)
    assert ret.observed == (15.0,)   # 25 - 10, past the application interrupt
    assert ret.censored == (20.0,)   # 50 - 30
    assert ret.n == 2


def test_effort_to_breadth_ratios():
    run = run_of(
        rec("a", verdict="success"),
        rec("b", verdict="success"),
        rec("c", verdict="failure"),
        hosts=2,
    )
    assert n_successes(run) == 2
    assert successes_per_distinct_host(run) == pytest.approx(1.0)
    assert actions_per_distinct_host(run) == pytest.approx(1.5)
    zero_hosts = run_of(rec("a", verdict="success"), hosts=0)
    assert successes_per_distinct_host(zero_hosts) is None
    assert actions_per_distinct_host(zero_hosts) is None


def test_load_stage_of_reads_the_ratified_consensus():
    stages = load_stage_of()
    assert stages["reconnaissance"] == 0
    assert stages["impact"] == 3
    assert len(stages) == 15


# ---------------------------------------------------------------------------
# §2 Diversity
# ---------------------------------------------------------------------------


def test_path_entropy_hand_worked():
    # Transitions: a->b four times (H=0); b->{a,c} two each (H=1 bit).
    # Visit-weighted: (4/8)*0 + (4/8)*1 = 0.5 bits.
    runs = [
        run_of(
            rec("a", next_place="b"), rec("b", next_place="a"),
            rec("a", next_place="b"), rec("b", next_place="c"),
        ),
        run_of(
            rec("a", next_place="b"), rec("b", next_place="a"),
            rec("a", next_place="b"), rec("b", next_place="c"),
        ),
    ]
    assert path_entropy(runs) == pytest.approx(0.5)
    assert path_entropy([run_of(rec("a", next_place=None))]) == 0.0


def test_distinct_sequences_and_prefixes():
    r1 = run_of(rec("a"), rec("b"), rec("c"))
    r2 = run_of(rec("a"), rec("b"), rec("d"))
    r3 = run_of(rec("a"), rec("b"), rec("c"))
    assert distinct_sequences([r1, r2, r3]) == 2
    assert distinct_prefixes([r1, r2, r3], k=2) == 1
    assert distinct_prefixes([r1, r2, r3], k=3) == 2


def test_jsd_l2_convention_bounds():
    assert jsd({"a": 0.5, "b": 0.5}, {"a": 0.5, "b": 0.5}) == pytest.approx(0.0)
    # Disjoint supports: divergence 1 in base 2.
    assert jsd({"a": 1.0}, {"b": 1.0}) == pytest.approx(1.0)
    # Symmetric.
    p, q = {"a": 0.9, "b": 0.1}, {"a": 0.2, "b": 0.8}
    assert jsd(p, q) == pytest.approx(jsd(q, p))


def test_visit_and_terminal_distributions():
    r1 = run_of(rec("a"), rec("b"))
    r2 = run_of(rec("a"), rec("a"))
    assert visit_distribution([r1, r2]) == {"a": 0.75, "b": 0.25}
    assert terminal_place_distribution([r1, r2]) == {"b": 0.5, "a": 0.5}


def test_profile_divergence_disjoint_streams_read_one():
    def prun(profile: str, *places: str) -> MovementRunResult:
        rs = [rec(p) for p in places]
        return run_of(*rs, profile=profile)

    results = [prun("p1", "a", "b"), prun("p2", "c", "d")]
    div = profile_divergence(results)
    assert div.visit_stream[("p1", "p2")] == pytest.approx(1.0)
    assert div.terminal[("p1", "p2")] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# §3 Defender response
# ---------------------------------------------------------------------------


def test_interrupt_action_mix_windows():
    run = run_of(
        rec("a", verb="SCAN_HOST"),
        rec("b", verb="SCAN_PORT"),
        rec("c", verb="EXPLOIT_VULN", verdict="failure", interrupted=True),
        rec("d", verb="SCAN_HOST"),
        rec("e", verb="", verdict="", outcome="DWELL_ONLY",
            place_class=DWELL_ONLY),
    )
    shift = interrupt_action_mix(run, window=2)
    assert isinstance(shift, ActionMixShift)
    assert shift.n_interrupts == 1
    assert shift.before_verbs == {"SCAN_HOST": 1, "SCAN_PORT": 1}
    assert shift.after_verbs == {"SCAN_HOST": 1, "": 1}  # dwell-only counted as ""
    assert shift.after_class == {ACTION_BEARING: 1, DWELL_ONLY: 1}
    # JSD over the normalised mixes is computable and positive here.
    assert jsd(normalise(shift.before_verbs), normalise(shift.after_verbs)) > 0
    assert interrupt_action_mix(run_of(rec("a")), window=2) is None


def test_recovery_times_observed_and_censored():
    run = run_of(
        rec("a", verdict="failure", interrupted=True, start=0, end=10, dwell=6),
        rec("b", verdict="failure", start=10, end=14, dwell=4),
        rec("c", verdict="success", start=14, end=18, dwell=4),
        rec("d", verdict="failure", interrupted=True, start=18, end=30, dwell=8),
        termination=40.0,
    )
    rt = recovery_times(run)
    assert rt.observed == (8.0,)    # 18 - 10
    assert rt.censored == (10.0,)   # 40 - 30


def test_failure_routing_rate_counts_only_verdict_routing():
    run = run_of(
        rec("a", verdict="success", next_place="b"),
        rec("b", verdict="failure", next_place="c"),
        rec("c", verdict="failure", next_place="d"),
        # dwell-only routing is unconditioned: excluded from the denominator
        rec("d", verb="", verdict="", outcome="DWELL_ONLY",
            place_class=DWELL_ONLY, next_place="e"),
        # verdict but no routing (sink): excluded too
        rec("e", verdict="failure", next_place=None),
    )
    assert failure_routing_rate(run) == pytest.approx(2 / 3)
    assert failure_routing_rate(run_of(rec("a", verdict="", next_place="b", verb=""))) is None


def test_terminal_mode_vocabulary():
    assert terminal_mode(run_of(rec("a"), reached=True)) == "objective"
    assert terminal_mode(run_of()) == "empty"
    assert terminal_mode(run_of(rec("a", outcome="MAX_EVENTS", next_place=None))) == "max_events"
    assert terminal_mode(run_of(rec("a", outcome="SIM_END", next_place=None))) == "sim_end"
    assert terminal_mode(run_of(rec("a", next_place=None))) == "sink"
    assert terminal_mode(run_of(rec("a", next_place="b"))) == "horizon"


# ---------------------------------------------------------------------------
# §4 Cost ledger
# ---------------------------------------------------------------------------


def hand_ledger_run() -> MovementRunResult:
    """Four events, worked by hand:
    - success SCAN_HOST: 0→6, dwell 6 (residual 0)
    - blocked SCAN_PORT: 6→10, dwell 4 (failure; residual 0)
    - MTD-interrupted EXPLOIT_VULN: 10→19, dwell served 4 ⇒ penalty 5
    - dwell-only visit: 19→22, dwell 3
    """
    return run_of(
        rec("a", verb="SCAN_HOST", verdict="success",
            start=0, end=6, dwell=6),
        rec("b", verb="SCAN_PORT", verdict="failure", blocked=True,
            outcome="PRECONDITION_UNMET", start=6, end=10, dwell=4),
        rec("c", verb="EXPLOIT_VULN", verdict="failure", interrupted=True,
            interrupted_by="network", outcome="MTD_INTERRUPT",
            start=10, end=19, dwell=4),
        rec("d", verb="", verdict="", outcome="DWELL_ONLY",
            place_class=DWELL_ONLY, start=19, end=22, dwell=3),
        hosts=1,
        termination=22.0,
    )


def test_cost_ledger_hand_worked():
    led = cost_ledger(hand_ledger_run())
    assert led.n_actions == 3
    assert led.n_blocked == 1
    assert led.n_interrupted == 1
    assert led.n_dwell_only == 1
    assert led.n_success == 1
    assert led.n_failure == 2
    assert led.attempts_by_verb == {"SCAN_HOST": 1, "SCAN_PORT": 1, "EXPLOIT_VULN": 1}
    assert led.blocked_by_verb == {"SCAN_PORT": 1}
    assert led.success_by_verb == {"SCAN_HOST": 1}
    assert led.time_active == pytest.approx(22.0)   # 6 + 4 + 9 + 3
    assert led.time_dwell == pytest.approx(17.0)    # 6 + 4 + 4 + 3
    assert led.time_mtd_penalty == pytest.approx(5.0)
    assert led.time_residual == pytest.approx(0.0)
    assert led.time_interrupted_events == pytest.approx(9.0)
    assert led.n_distinct_hosts == 1
    assert led.hosts_per_ksec == pytest.approx(1000.0 / 22.0)


# ---------------------------------------------------------------------------
# §6 Cross-arm subset
# ---------------------------------------------------------------------------


def test_comparable_from_movement_fractions():
    cmp = comparable_from_movement(hand_ledger_run())
    assert cmp.arm == "movement"
    assert cmp.n_events == 3
    assert cmp.verb_mix == pytest.approx(
        {"SCAN_HOST": 1 / 3, "SCAN_PORT": 1 / 3, "EXPLOIT_VULN": 1 / 3}
    )
    assert cmp.blocked_fraction == pytest.approx(1 / 3)
    assert cmp.interrupted_fraction == pytest.approx(1 / 3)
    assert cmp.dwell_only_fraction == pytest.approx(1 / 4)  # 1 of 4 visits
    assert cmp.actions_per_distinct_host == pytest.approx(3.0)
    assert cmp.reached_objective is False
    # The comparable type carries no time-denominated field, by construction.
    assert not any("time" in f for f in vars(cmp))


BASELINE_ROWS = [
    {"name": "SCAN_HOST", "duration": 5.0, "interrupted_in": "None",
     "compromise_host": "None", "compromise_host_uuid": "None"},
    {"name": "SCAN_PORT", "duration": 10.0, "interrupted_in": "None",
     "compromise_host": "None", "compromise_host_uuid": "None"},
    {"name": "EXPLOIT_VULN", "duration": 30.0, "interrupted_in": "None",
     "compromise_host": 7, "compromise_host_uuid": "u-7"},
    {"name": "EXPLOIT_VULN", "duration": 25.0, "interrupted_in": "network",
     "compromise_host": "None", "compromise_host_uuid": "None"},
    {"name": "BRUTE_FORCE", "duration": 20.0, "interrupted_in": "None",
     "compromise_host": 7, "compromise_host_uuid": "u-7"},
]


def test_baseline_ledger_hand_worked():
    led = baseline_ledger(BASELINE_ROWS)
    assert led.n_actions == 5
    assert led.n_interrupted == 1
    assert led.attempts_by_verb == {
        "SCAN_HOST": 1, "SCAN_PORT": 1, "EXPLOIT_VULN": 2, "BRUTE_FORCE": 1
    }
    assert led.n_compromise_events == 2
    assert led.n_distinct_hosts == 1     # both compromises hit uuid u-7
    assert led.time_total == pytest.approx(90.0)


def test_comparable_from_baseline_structural_zeros():
    cmp = comparable_from_baseline(BASELINE_ROWS, reached_objective=True)
    assert cmp.arm == "baseline"
    assert cmp.n_events == 5
    assert cmp.blocked_fraction == 0.0       # structural: no precondition to fail
    assert cmp.dwell_only_fraction == 0.0    # structural: no non-action concept
    assert cmp.interrupted_fraction == pytest.approx(1 / 5)
    assert cmp.actions_per_distinct_host == pytest.approx(5.0)
    assert cmp.reached_objective is True
    # Unknown objective is reported as unknown, never guessed.
    assert comparable_from_baseline(BASELINE_ROWS).reached_objective is None


def test_baseline_adapter_accepts_a_dataframe():
    pd = pytest.importorskip("pandas")
    led = baseline_ledger(pd.DataFrame(BASELINE_ROWS))
    assert led.n_actions == 5
    assert led.n_distinct_hosts == 1


# ---------------------------------------------------------------------------
# §7 Interval reporting (gate 4: exercised by a measure's own aggregation)
# ---------------------------------------------------------------------------


def test_mean_ci_convention():
    iv = mean_ci([1.0, 2.0, 3.0])
    assert iv.mean == pytest.approx(2.0)
    assert iv.ci95 == pytest.approx(1.96 * 1.0 / math.sqrt(3))
    assert (iv.lo, iv.hi) == (pytest.approx(iv.mean - iv.ci95),
                              pytest.approx(iv.mean + iv.ci95))
    assert mean_ci([4.0]).ci95 == 0.0
    with pytest.raises(ValueError):
        mean_ci([])


def test_interval_report_on_a_measure_separates_only_disjoint_pairs():
    # Aggregate a real measure (successes per run) across three synthetic
    # profiles: p_lo and p_hi are far apart (disjoint CIs), p_mid overlaps
    # p_hi — the report must expose exactly that, so an ordering over the
    # three cannot be claimed.
    def runs_with_successes(profile: str, counts: list[int]):
        return [
            run_of(*(rec("a", verdict="success") for _ in range(c)),
                   profile=profile)
            if c else run_of(rec("a", verdict="failure"), profile=profile)
            for c in counts
        ]

    groups = {
        "p_lo": [float(n_successes(r)) for r in runs_with_successes("p_lo", [0, 1, 0, 1])],
        "p_mid": [float(n_successes(r)) for r in runs_with_successes("p_mid", [8, 10, 9, 11])],
        "p_hi": [float(n_successes(r)) for r in runs_with_successes("p_hi", [9, 12, 10, 14])],
    }
    report = interval_report(groups)
    assert [g for g, _ in report.rows] == ["p_lo", "p_mid", "p_hi"]
    assert report.separated_adjacent_pairs == (("p_lo", "p_mid"),)
    assert report.unseparated_adjacent_pairs == (("p_mid", "p_hi"),)
    assert not report.ordering_supported


# ---------------------------------------------------------------------------
# Seeded integration checks (the two the handoff names)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def seeded_movement_run():
    from mtdsim.l3_simulation.movement.run import run_movement

    return run_movement(
        "infrastructure_setup", seed=0, horizon=3_000,
        mtd_scheme="random", mtd_interval=200,
    )


def test_penalty_derivation_against_a_seeded_run(seeded_movement_run):
    """Step 5's required check: the confusion penalty is derived from
    ``end - start - dwell`` on interrupted records. Two facts make the
    derivation sound, and both are asserted against a real MTD run rather
    than assumed: (a) non-interrupted records close at start + dwell exactly
    (S3-R: the movement layer's draw IS the whole duration), so the residual
    is zero there; (b) the record stream is gapless (each event starts where
    the previous ended), so the penalty cannot be hiding between records."""
    recs = seeded_movement_run.records
    interrupted = [r for r in recs if r.interrupted]
    assert interrupted, "seeded run produced no MTD interrupt; pick another seed"
    for r in recs:
        if not r.interrupted:
            assert r.end_time - r.start_time - r.dwell == pytest.approx(0.0, abs=1e-9)
    # (b) gapless stream: nothing is charged between records.
    for prev, nxt in zip(recs, recs[1:]):
        assert nxt.start_time == pytest.approx(prev.end_time, abs=1e-9)
    # The derived penalty is non-negative everywhere and positive somewhere:
    # an interrupt can land at the very end of the served dwell, but not
    # every one can.
    penalties = [mtd_penalty(r) for r in interrupted]
    assert all(p >= 0 for p in penalties)
    assert sum(penalties) > 0
    # And the ledger reconciles: active time = dwell + penalty + residual.
    led = cost_ledger(seeded_movement_run)
    assert led.time_active == pytest.approx(
        led.time_dwell + led.time_mtd_penalty + led.time_residual
    )


def test_cross_arm_subset_computes_on_both_arms(seeded_movement_run):
    """Gate 4b: the comparable subset computes on one seeded run of each arm,
    and the two sides expose the same fields with the arms' structural
    differences visible rather than omitted."""
    import random

    import numpy as np
    import simpy

    from mtdnetwork.component.adversary import Adversary
    from mtdnetwork.component.time_network import TimeNetwork
    from mtdnetwork.data.constants import ATTACKER_THRESHOLD
    from mtdnetwork.operation.attack_operation import AttackOperation
    from mtdsim.l3_simulation.movement.run import GEOMETRY

    random.seed(0)
    np.random.seed(0)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**GEOMETRY)
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0
    )
    attack_op.proceed_attack()
    env.run(until=3_000)

    base = comparable_from_baseline(
        adversary.get_attack_stats().get_record(),
        reached_objective=bool(end_event.triggered),
    )
    mov = comparable_from_movement(seeded_movement_run)

    assert base.arm == "baseline" and mov.arm == "movement"
    assert base.n_events > 0 and mov.n_events > 0
    # Same field set on both sides — the comparison is field-for-field.
    assert vars(base).keys() == vars(mov).keys()
    # Structural zeros on the baseline side are reported, not omitted.
    assert base.blocked_fraction == 0.0
    assert base.dwell_only_fraction == 0.0
    # Verb vocabularies overlap (both arms dispatch the six substrate verbs).
    assert set(base.verb_mix) & set(mov.verb_mix)

