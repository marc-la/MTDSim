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
    CensoredDurations,
    action_records,
    actions_per_distinct_host,
    baseline_ledger,
    comparable_from_baseline,
    comparable_from_movement,
    cost_ledger,
    advanced_after_first_success,
    deepest_successful_stage,
    first_success_stage,
    refoothold_rate,
    refoothold_times,
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

# §8's reader is reached through the module rather than by name: the section is
# new and importing it wholesale keeps the existing import block untouched.
from mtdsim.l3_simulation.movement import measures as M


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
    n_compromised: int = 0,
    exploitability: float = 0.0,
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
        n_compromised=n_compromised,
        exploitability=exploitability,
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


def test_first_success_stage_and_strict_advance():
    """The axis-1 advance predicate: deepest successful stage strictly beyond the
    stage the run first succeeded at. Hand-worked so the semantics are pinned
    independently of any net."""
    advancing = run_of(
        rec("recon", verdict="success"),
        rec("intrude", verdict="failure"),
        rec("operate", verdict="success"),
    )
    assert first_success_stage(advancing, STAGES) == 0
    assert deepest_successful_stage(advancing, STAGES) == 2
    assert advanced_after_first_success(advancing, STAGES) is True

    # Succeeded repeatedly, never deeper — experiment 1's churn shape.
    repeating = run_of(
        rec("operate", verdict="success"),
        rec("operate", verdict="success"),
        rec("recon", verdict="success"),
    )
    assert first_success_stage(repeating, STAGES) == 2
    assert advanced_after_first_success(repeating, STAGES) is False

    # Never succeeded: advance is undefined, not False. Encoding it False would
    # score a run that did nothing as a run that failed to advance, which are
    # different claims.
    barren = run_of(rec("recon", verdict="failure"))
    assert first_success_stage(barren, STAGES) is None
    assert advanced_after_first_success(barren, STAGES) is None


def test_refoothold_times_and_rate():
    """Re-establishing after MTD severs position: from each network-layer
    interrupt to the next *compromise*, censored at run end.

    Deliberately narrower than recovery_times, which counts any success. Here
    the recon success after the second sever must NOT count as a re-foothold.
    """
    run = run_of(
        rec("a", verb="EXPLOIT_VULN", outcome="EXPLOIT_COMPROMISED", start=0, end=10),
        # sever #1, re-footholded at t=30
        rec("b", interrupted=True, interrupted_by="network", start=10, end=20),
        rec("c", verb="EXPLOIT_VULN", outcome="EXPLOIT_COMPROMISED", start=20, end=30),
        # sever #2, only a recon success afterwards -> censored
        rec("d", interrupted=True, interrupted_by="network", start=30, end=40),
        rec("e", verb="SCAN_HOST", verdict="success", start=40, end=50),
        # an application-layer interrupt is not a sever and raises no question
        rec("f", interrupted=True, interrupted_by="application", start=50, end=60),
        termination=60.0,
    )
    times = refoothold_times(run)
    assert times.observed == (10.0,)
    assert times.censored == (20.0,)
    assert refoothold_rate(run) == pytest.approx(0.5)

    # Never severed: the question is undefined rather than answered zero.
    untouched = run_of(rec("a", verb="SCAN_HOST"))
    assert refoothold_rate(untouched) is None
    assert refoothold_times(untouched) == CensoredDurations((), ())


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
    assert (
        terminal_mode(run_of(rec("a", outcome="SINK_EXHAUSTED", next_place=None)))
        == "sink_exhausted"
    )
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
        "objective_none_c2", seed=0, horizon=3_000,
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



# ---------------------------------------------------------------------------
# §5 Defender-side disruption ledger
# ---------------------------------------------------------------------------


def mtd_exec(name, start, finish, layer):
    from mtdsim.l3_simulation.movement.statistics import MTDExecution

    return MTDExecution(
        name=name, start_time=start, finish_time=finish,
        duration=finish - start, layer=layer,
    )


def test_union_time_merges_overlaps():
    from mtdsim.l3_simulation.movement.measures import union_time

    # [0,100] and [50,120] merge to [0,120]; [200,260] is disjoint.
    assert union_time([(0, 100), (50, 120), (200, 260)]) == pytest.approx(180.0)
    # Containment collapses; zero/negative-length spans contribute nothing.
    assert union_time([(0, 100), (10, 20), (30, 30)]) == pytest.approx(100.0)
    assert union_time([]) == 0.0


def test_disruption_ledger_hand_worked():
    from mtdsim.l3_simulation.movement.measures import disruption_ledger

    led = disruption_ledger(
        [
            mtd_exec("IPShuffle", 0.0, 100.0, "network"),
            mtd_exec("OSDiversity", 50.0, 120.0, "application"),
            mtd_exec("IPShuffle", 200.0, 260.0, "network"),
        ],
        elapsed=1_000.0,
        n_suspended=2,
    )
    assert led.n_executed == 3 and led.n_suspended == 2
    # Sum counts the overlap twice; the union does not.
    assert led.reconfig_time_total == pytest.approx(230.0)
    assert led.busy_time == pytest.approx(180.0)
    assert led.occupancy == pytest.approx(0.18)
    assert led.executions_per_ksec == pytest.approx(3.0)
    assert led.reconfig_time_by_layer == pytest.approx(
        {"network": 160.0, "application": 70.0}
    )
    assert led.reconfig_time_by_mechanism == pytest.approx(
        {"IPShuffle": 160.0, "OSDiversity": 70.0}
    )
    assert led.n_by_mechanism == {"IPShuffle": 2, "OSDiversity": 1}


def test_disruption_from_run_and_the_no_mtd_zero():
    from mtdsim.l3_simulation.movement.measures import disruption_from_run

    # A run with no MTD carries the default empty snapshot: the ledger is the
    # explicit zero, not an error.
    bare = run_of(rec("recon", start=0, end=10, dwell=10))
    led = disruption_from_run(bare)
    assert led.n_executed == 0 and led.occupancy == 0.0

    with_mtd = MovementRunResult(
        profile="test", seed=0, with_synthetic_overlay=True,
        records=(rec("recon", start=0, end=10, dwell=10),),
        reached_objective=False, termination_time=500.0, compromised_count=0,
        mtd_executions=(mtd_exec("IPShuffle", 100.0, 200.0, "network"),),
        mtd_suspended_count=1, mtd_attack_interrupted=0,
    )
    led = disruption_from_run(with_mtd)
    assert led.occupancy == pytest.approx(0.2)
    assert led.n_suspended == 1
    assert led.elapsed == 500.0


def test_disruption_snapshot_against_a_seeded_run(seeded_movement_run):
    """Integration: the run result's defender-side snapshot is the substrate's
    own record, and the derived ledger is internally coherent on a real MTD
    run — windows are consistent, the union never exceeds the sum or the
    elapsed time, and occupancy is a genuine fraction."""
    from mtdsim.l3_simulation.movement.measures import disruption_from_run

    execs = seeded_movement_run.mtd_executions
    assert execs, "seeded MTD run recorded no executed mutation"
    for e in execs:
        assert e.finish_time - e.start_time == pytest.approx(e.duration)
        assert e.layer in ("network", "application", "reserve")
    led = disruption_from_run(seeded_movement_run)
    assert led.n_executed == len(execs)
    assert 0.0 < led.busy_time <= led.reconfig_time_total + 1e-9
    assert led.busy_time <= led.elapsed + 1e-9
    assert 0.0 < led.occupancy <= 1.0
    # The substrate's own interrupt tally and the movement records' interrupted
    # count are the same event stream seen from the two sides.
    assert seeded_movement_run.mtd_attack_interrupted == sum(
        1 for r in seeded_movement_run.records if r.interrupted
    )


# ---------------------------------------------------------------------------
# §8 attacker disengagement — the projected-effort reader
#
# The gate the design record sets: hand-built streams with hand-worked expected
# values, so the arithmetic is pinned rather than trusted. Five shapes, each
# chosen because it exercises a property the measure is claimed to have — steady
# progress lowers the projection, a stall raises it, no progress at all rises
# from the prior alone, a run that crosses and recovers reports the FIRST
# crossing, and a run that never crosses is censored rather than sentinel-valued.
# ---------------------------------------------------------------------------


def _progress_run(*counts: int) -> MovementRunResult:
    """A run of action-bearing records whose progress trajectory is ``counts``."""
    return run_of(
        *(rec("p", step=i, n_compromised=c) for i, c in enumerate(counts)),
        hosts=counts[-1] if counts else 0,
    )


def test_progress_trajectory_reads_the_recorded_host_count() -> None:
    """Progress is read off the record, never re-derived from compromise events —
    the record carries no host identity, so events over-count distinct hosts
    through re-compromise (measured at 5.40x, and itself MTD-dependent)."""
    run = _progress_run(0, 0, 1, 1, 2)
    assert M.progress_trajectory(run) == (0, 0, 1, 1, 2)


def test_progress_trajectory_excludes_dwell_only_visits() -> None:
    """Effort is attempted actions, so a dwell-only visit contributes no point —
    the same denominator the cost ledger's ``n_actions`` uses."""
    run = run_of(
        rec("p", step=0, n_compromised=0),
        rec("p", step=1, verb="", place_class=DWELL_ONLY, verdict="", n_compromised=0),
        rec("p", step=2, n_compromised=1),
        hosts=1,
    )
    assert M.progress_trajectory(run) == (0, 1)


def test_steady_progress_lowers_the_projection() -> None:
    """A compromise raises both the level and the rate, so T falls — an attacker
    close to the objective rationally persists through a stall that would send an
    empty-handed one away."""
    run = _progress_run(1, 2, 3, 4, 5)
    curve = M.projected_effort_curve(run)
    assert all(b < a for a, b in zip(curve, curve[1:])), curve


def test_a_stall_raises_the_projection_monotonically() -> None:
    """An action with no progress increments the effort and decrements the rate,
    so T rises twice over. This is the economically visible signature of MTD on
    this substrate: progress flattens while effort keeps accruing."""
    run = _progress_run(2, 2, 2, 2, 2)
    curve = M.projected_effort_curve(run)
    assert all(b > a for a, b in zip(curve, curve[1:])), curve


def test_no_progress_at_all_rises_from_the_prior_alone() -> None:
    """With h = 0 throughout, the rate is driven entirely by the Laplace prior and
    T rises from its first value. Hand-worked: at t = 1, r = alpha / (1 + alpha/r0)
    and T = 1 + W / r."""
    model = M.DisengagementModel(work_total=40.0, r0=0.02, alpha=1.0)
    run = _progress_run(0, 0, 0)
    curve = M.projected_effort_curve(run, model)
    expected_first = 1.0 + 40.0 / (1.0 / (1.0 + 1.0 / 0.02))
    assert curve[0] == pytest.approx(expected_first)
    assert all(b > a for a, b in zip(curve, curve[1:]))


def test_the_first_crossing_is_taken_not_the_last() -> None:
    """T is deliberately not monotone, and first-crossing is the honest reading:
    an attacker decides in real time and does not get to wait and see whether its
    prospects recover. This run crosses, then recovers below the budget."""
    model = M.DisengagementModel(work_total=10.0, r0=0.5, alpha=1.0)
    run = _progress_run(0, 0, 0, 5, 9)
    curve = M.projected_effort_curve(run, model)
    budget = curve[1]  # crosses at action 3, then recovers as progress lands
    assert curve[2] > budget and curve[-1] < budget, curve
    assert M.abandonment_effort(run, budget, model) == 3


def test_a_run_that_never_crosses_is_censored_not_sentinel_valued() -> None:
    """``None`` means censored at this budget, not "did not abandon". Pooling the
    two into one mean understates every censored run, which is why the suite
    reports them separately."""
    run = _progress_run(1, 2, 3)
    assert M.abandonment_effort(run, 10_000_000.0) is None


def test_one_run_yields_the_whole_budget_family() -> None:
    """The property that makes the reader cheap: T is computed once and every
    budget is a threshold read off the same trajectory, so a frontier over
    patience costs no additional simulation."""
    run = _progress_run(0, 0, 1, 1, 1)
    curve = M.projected_effort_curve(run)
    budgets = [curve[0] - 1.0, curve[0] + 1.0, 10_000_000.0]
    got = M.abandonment_curve(run, budgets)
    assert got[budgets[0]] == 1
    assert got[budgets[1]] == M.abandonment_effort(run, budgets[1])
    assert got[budgets[2]] is None


def test_progress_beyond_the_objective_owes_no_further_effort() -> None:
    """The remaining term clamps at zero rather than going negative — an attacker
    past the objective owes nothing more, and T reduces to the effort spent."""
    model = M.DisengagementModel(work_total=2.0)
    run = _progress_run(5)
    assert M.projected_effort_curve(run, model) == (1.0,)


def test_the_snapshot_reports_the_crossing_without_acting_on_it() -> None:
    """The reader's reporting unit: *the attacker would have given up at X*, with
    the state at that point, and the run's other measures untouched. Nothing here
    stops a run — an attacker that actually stopped would make "MTD causes
    disengagement" definitional and admit no null arm."""
    run = _progress_run(0, 0, 1, 1)
    curve = M.projected_effort_curve(run)
    snap = M.disengagement_snapshot(run, curve[0] - 1.0)
    assert snap["abandoned"] is True and snap["censored"] is False
    assert snap["abandonment_effort"] == 1
    assert snap["actions_total"] == 4 and snap["progress_total"] == 1
    censored = M.disengagement_snapshot(run, 10_000_000.0)
    assert censored["abandoned"] is False and censored["censored"] is True
    assert censored["abandonment_effort"] is None


def test_a_non_positive_prior_rate_is_refused() -> None:
    """A zero prior rate makes the projected remaining effort infinite before any
    evidence exists — refuse loudly rather than return inf."""
    with pytest.raises(ValueError, match="r0 must be positive"):
        M.DisengagementModel(r0=0.0)
    with pytest.raises(ValueError, match="alpha must be positive"):
        M.DisengagementModel(alpha=0.0)
    with pytest.raises(ValueError, match="work_total must be positive"):
        M.DisengagementModel(work_total=0.0)


def test_the_baseline_trajectory_counts_distinct_hosts_exactly() -> None:
    """The baseline arm has no instrumentation problem: its rows carry a stable
    host uuid, so distinct hosts are counted exactly rather than proxied. The
    asymmetry with the movement arm's sampled count is stated, not smoothed."""
    rows = [
        {"compromise_host": "None", "compromise_host_uuid": "z"},  # not a compromise
        {"compromise_host": 3, "compromise_host_uuid": "a"},
        {"compromise_host": 3, "compromise_host_uuid": "a"},  # re-compromise
        {"compromise_host": 7, "compromise_host_uuid": "b"},
    ]
    assert M.baseline_progress_trajectory(rows) == (0, 1, 1, 2)


def test_the_baseline_trajectory_gates_on_compromise_not_on_uuid_presence() -> None:
    """A row can carry a host uuid without being a compromise. Gating on the
    uuid's presence alone over-counted by exactly one on every condition and seed
    measured — systematic, not noise — and would have put this arm's trajectory
    permanently out of step with ``baseline_ledger``'s own distinct-host count."""
    rows = [{"compromise_host": "None", "compromise_host_uuid": f"h{i}"} for i in range(5)]
    assert M.baseline_progress_trajectory(rows) == (0, 0, 0, 0, 0)


# ---------------------------------------------------------------------------
# §9 stealth exposure — the detectability curve (validation gate 1)
#
# Every case below is a hand-constructed visit stream with its expected level
# worked out in the test. The declared family itself (the tier table, the two
# nulls, the reproduction check) is pinned in test_movement_exposure.py; what is
# pinned here is the reader's arithmetic over a record stream.
#
# The model used throughout is deliberately NOT the declared one: τ = 10 and
# ρ = 0.5 with the CVSS term off, so every expected number is short enough to
# write down. Places are chosen from the ranking's ends — `stealth` at tier 1
# (d = 0.125) and `impact` at tier 4 (d = 1.0).
# ---------------------------------------------------------------------------

from mtdsim.l3_simulation.movement.exposure import INVERSE, DIRECT, exposure_model

TAU = 10.0
# Under R1 (2026-08-06) only a tactic that INVOKES a verb scores, so the fixtures
# are drawn from the eight dispatching tactics. That narrows the reachable range
# to tiers 1-3, which is the ruling's stated cost made concrete: `impact` and
# `stealth` are dwell-only and now score exactly nothing.
QUIET = "command-and-control"   # tier 1, invokes SCAN_NEIGHBOR -> d = 0.125
LOUD = "privilege-escalation"   # tier 3, invokes EXPLOIT_VULN  -> d = 0.500
EXPLOITY = "initial-access"     # tier 3, invokes EXPLOIT_VULN  -> d = 0.500
D_LOUD, D_QUIET = 0.5, 0.125


def exposure_test_model(**kwargs):
    """The hand-arithmetic model: τ = 10, ρ = 0.5, CVSS term off unless asked."""
    params = {"tau": TAU, "rho": 0.5, "delta": 0.0}
    params.update(kwargs)
    return exposure_model(**params)


def visits_at(place: str, times, **kwargs):
    """A stream of one-second visits to ``place`` starting at each of ``times``."""
    return [
        rec(place, step=i, start=t, end=t + 1.0, dwell=1.0, **kwargs)
        for i, t in enumerate(times)
    ]


def test_the_level_starts_at_zero_so_the_first_visit_is_its_own_increment() -> None:
    """Before its first act the attacker has generated no signal. That is the
    honest null rather than a choice, and it makes the first level readable
    without reference to anything."""
    curve = M.exposure_curve(run_of(*visits_at(LOUD, [0.0])), exposure_test_model())
    assert curve.levels == (D_LOUD,)
    assert curve.gaps == (0.0,)


def test_a_burst_of_noisy_actions_compounds() -> None:
    """Three loud acts one second apart, τ = 10. Hand-worked:
        D1 = 1
        D2 = 1·e^-0.1 + 1 = 1.904837418
        D3 = D2·e^-0.1 + 1 = 2.723707...
    The level compounds because the decay across one second recovers almost all
    of it — which is what 'a burst is louder than its parts' has to mean."""
    curve = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 1.0, 2.0])), exposure_test_model()
    )
    e = math.exp(-0.1)
    assert curve.levels[0] == pytest.approx(D_LOUD)
    assert curve.levels[1] == pytest.approx(D_LOUD * e + D_LOUD)
    assert curve.levels[2] == pytest.approx((D_LOUD * e + D_LOUD) * e + D_LOUD)
    assert curve.levels[0] < curve.levels[1] < curve.levels[2]


def test_an_idle_gap_decays_the_level() -> None:
    """The same two acts, separated by an idle gap instead of a second. At
    Δ = 50 with τ = 10 the first act has decayed to e^-5 ≈ 0.0067 of itself, so
    the second act arrives at an essentially clean network. This is the whole
    behavioural claim: waiting buys the attacker something."""
    burst = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 1.0])), exposure_test_model()
    )
    patient = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 50.0])), exposure_test_model()
    )
    assert patient.levels[1] == pytest.approx(D_LOUD * math.exp(-5.0) + D_LOUD)
    assert patient.levels[1] < burst.levels[1]


def test_a_stealth_only_run_stays_low() -> None:
    """Five visits to the ranking's quiet end against five to its loud end, on an
    identical timeline. The separation is the ordinal ranking doing its one job,
    and it is exactly the ρ^3 = 8-fold the tier gap declares."""
    times = [0.0, 20.0, 40.0, 60.0, 80.0]
    quiet = M.exposure_curve(run_of(*visits_at(QUIET, times)), exposure_test_model())
    loud = M.exposure_curve(run_of(*visits_at(LOUD, times)), exposure_test_model())
    assert loud.mean_exposure == pytest.approx(4.0 * quiet.mean_exposure)
    assert quiet.peak_exposure < loud.peak_exposure


def test_gaps_are_clamped_at_zero() -> None:
    """Two records can share a start time when the movement layer draws a zero
    dwell. A negative gap would make the decay a *gain*, so it is clamped —
    coincident acts simply add."""
    stream = [
        rec(LOUD, step=0, start=5.0, end=5.0, dwell=0.0),
        rec(LOUD, step=1, start=5.0, end=5.0, dwell=0.0),
    ]
    curve = M.exposure_curve(run_of(*stream, termination=5.0), exposure_test_model())
    assert curve.gaps == (0.0, 0.0)
    assert curve.levels == (D_LOUD, 2 * D_LOUD)


def test_dwell_only_visits_are_present_but_score_nothing() -> None:
    """R1 (2026-08-06). A dwell-only visit stays IN the stream — it occupies the
    attacker's time, so it must keep contributing to the gaps — and contributes no
    increment. Dropping it from the stream instead would be arithmetically
    identical here (the decay composes across a merged gap) and would lose the
    event count, so it is kept and zeroed rather than filtered."""
    stream = [
        rec("impact", step=0, verb="", verdict="", start=0.0, end=1.0, dwell=1.0,
            place_class=DWELL_ONLY),
    ]
    curve = M.exposure_curve(run_of(*stream), exposure_test_model())
    assert curve.increments == (0.0,)
    assert curve.n_events == 1
    assert not M.action_records(run_of(*stream))  # dispatched nothing at all


def test_bare_terminal_markers_are_excluded() -> None:
    """A terminal marker names the place the run ended at; it consumed nothing
    and dispatched nothing, so it must not add a final increment."""
    stream = [
        rec(LOUD, step=0, start=0.0, end=1.0, dwell=1.0),
        rec(LOUD, step=1, verb="", verdict="", outcome="SIM_END",
            next_place=None, start=1.0, end=1.0, dwell=0.0),
    ]
    curve = M.exposure_curve(run_of(*stream), exposure_test_model())
    assert curve.n_events == 1


# -- the CVSS term ----------------------------------------------------------


def test_the_cvss_term_only_touches_visits_that_attempted_a_vulnerability() -> None:
    """Two visits with the same tier, one carrying a vulnerability figure and one
    not. The term modulates the first and leaves the second at its tier value —
    which is what 'complementary, not substitutable' has to mean in arithmetic."""
    model = exposure_test_model(delta=0.5, direction=INVERSE)
    stream = [
        rec(EXPLOITY, step=0, start=0.0, end=1.0, dwell=1.0, exploitability=0.25),
        rec(EXPLOITY, step=1, start=100.0, end=101.0, dwell=1.0),
    ]
    curve = M.exposure_curve(run_of(*stream), model)
    # tier 3 at rho 0.5 -> 0.5; m = 1 - 0.5 + 2(0.5)(1 - 0.25) = 1.25
    assert curve.increments[0] == pytest.approx(0.625)
    assert curve.increments[1] == pytest.approx(0.5)


def test_the_two_cvss_directions_disagree_on_the_same_stream() -> None:
    """E3 exists because the direction is a declared judgement with no
    attestation on either side. The reader must therefore produce *different*
    curves for the two readings on the same recorded run — if it did not, the
    question would be unaskable rather than settled."""
    stream = visits_at(EXPLOITY, [0.0, 5.0, 10.0], exploitability=0.9)
    inverse = M.exposure_curve(
        run_of(*stream), exposure_test_model(delta=0.5, direction=INVERSE)
    )
    direct = M.exposure_curve(
        run_of(*stream), exposure_test_model(delta=0.5, direction=DIRECT)
    )
    assert inverse.mean_exposure < direct.mean_exposure  # a quiet easy exploit


# -- the three summaries ----------------------------------------------------


def test_the_time_average_is_the_closed_form_integral() -> None:
    """One loud act at t = 0 on a run ending at t = 100, τ = 10. The level decays
    from 1.0 for the whole run, so ∫D dt = 1·τ·(1 − e^-10) and the time average
    is that over 100. Worked in closed form rather than sampled: a sampled
    integral would depend on how often the arm happened to act, which is the bias
    this summary exists to avoid."""
    curve = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0]), termination=100.0), exposure_test_model()
    )
    expected = D_LOUD * TAU * (1.0 - math.exp(-10.0)) / 100.0
    assert curve.time_average_exposure == pytest.approx(expected)


def test_the_mean_over_events_and_the_time_average_can_disagree() -> None:
    """The disagreement is the finding, not a defect. A rare-but-loud campaign
    and a frequent-but-quiet one can order one way on the mean over events and
    the other way over the clock, and a tempo claim is exactly about that case."""
    rare_loud = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 400.0]), termination=800.0),
        exposure_test_model(),
    )
    often_quiet = M.exposure_curve(
        run_of(*visits_at(QUIET, [t * 8.0 for t in range(100)]), termination=800.0),
        exposure_test_model(),
    )
    assert rare_loud.mean_exposure > often_quiet.mean_exposure
    assert rare_loud.time_average_exposure < often_quiet.time_average_exposure


def test_mean_increment_ignores_the_clock_entirely() -> None:
    """The clock-free control. Two runs visiting the same places in the same
    order, one dense and one spread, agree exactly on the mean increment and
    differ on the level — which is what separates *what* the attacker does from
    *how fast*. A separation visible in this one is an action-mix claim, and axis
    5 may not report it as tempo."""
    dense = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 1.0, 2.0])), exposure_test_model()
    )
    spread = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 500.0, 1000.0])), exposure_test_model()
    )
    assert dense.mean_increment == spread.mean_increment == D_LOUD
    assert dense.mean_exposure > spread.mean_exposure


def test_an_empty_run_reports_none_rather_than_zero() -> None:
    """No events is not 'silent': it is nothing to read. Reporting 0.0 would let
    a degenerate run be averaged in as the quietest campaign on record."""
    curve = M.exposure_curve(run_of(), exposure_test_model())
    assert curve.mean_exposure is None
    assert curve.mean_increment is None
    assert curve.time_average_exposure is None
    assert curve.peak_exposure is None


# -- the cross-arm guard ----------------------------------------------------


def test_two_curves_on_different_clocks_are_not_time_comparable() -> None:
    """Under S3-R the movement layer prices all of its arm's time while the
    baseline runs on substrate pricing, so the two arms' time-denominated
    summaries are computed against different clocks. The type carries the caveat
    so a consumer cannot drop it — and it returns a verdict rather than raising,
    because the parent record permits the cross-clock figure *with* the asymmetry
    stated."""
    movement = M.exposure_curve(run_of(*visits_at(LOUD, [0.0])), exposure_test_model())
    baseline = M.baseline_exposure_curve(
        [{"name": "EXPLOIT_VULN", "start_time": 0.0, "finish_time": 1.0}],
        exposure_test_model(),
    )
    assert movement.clock == M.MOVEMENT_CLOCK
    assert baseline.clock == M.SUBSTRATE_CLOCK
    assert not movement.comparable_with(baseline)
    assert movement.comparable_with(movement)


def test_a_different_tau_is_also_not_comparable() -> None:
    """τ sets the level's scale, so two curves read at different decay constants
    are two different measures rather than two readings of one."""
    a = M.exposure_curve(run_of(*visits_at(LOUD, [0.0])), exposure_test_model())
    b = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0])), exposure_test_model(tau=60.0)
    )
    assert not a.comparable_with(b)


# -- the baseline arm's event definition ------------------------------------


def test_consecutive_exploit_rows_collapse_into_one_action() -> None:
    """``_do_exploit_vuln`` appends one row per vulnerability tried, not per
    action, inflating this arm's event count 3.81-fold on a measured pilot. The
    collapse is exact rather than heuristic: the native FSM never dispatches
    EXPLOIT_VULN twice in succession, so a run of consecutive exploit rows is one
    action by construction. The first row of each run is kept — the action's
    signal begins where the action does."""
    rows = [
        {"name": "SCAN_PORT", "start_time": 0.0, "finish_time": 1.0},
        {"name": "EXPLOIT_VULN", "start_time": 1.0, "finish_time": 2.0},
        {"name": "EXPLOIT_VULN", "start_time": 2.0, "finish_time": 3.0},
        {"name": "EXPLOIT_VULN", "start_time": 3.0, "finish_time": 4.0},
        {"name": "BRUTE_FORCE", "start_time": 4.0, "finish_time": 5.0},
        {"name": "EXPLOIT_VULN", "start_time": 5.0, "finish_time": 6.0},
    ]
    collapsed = M.baseline_action_rows(rows)
    assert [r["name"] for r in collapsed] == [
        "SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE", "EXPLOIT_VULN"
    ]
    assert [r["start_time"] for r in collapsed] == [0.0, 1.0, 4.0, 5.0]


def test_the_collapse_changes_the_baseline_level_it_would_otherwise_inflate() -> None:
    """The point of the collapse, in arithmetic: uncollapsed, the three
    per-vulnerability rows of one exploit action each add an increment, so the
    arm is handed a threefold louder action by an accounting artefact."""
    rows = [
        {"name": "EXPLOIT_VULN", "start_time": float(t), "finish_time": t + 1.0}
        for t in range(3)
    ]
    collapsed = M.baseline_exposure_curve(rows, exposure_test_model())
    assert collapsed.n_events == 1
    uncollapsed = M.baseline_exposure_curve(
        [dict(r, name="SCAN_PORT") for r in rows], exposure_test_model()
    )
    assert uncollapsed.n_events == 3
    assert collapsed.mean_exposure < uncollapsed.mean_exposure


def test_the_baseline_arm_has_no_cvss_term_by_construction() -> None:
    """Its rows carry no vulnerability figure, so every increment is its verb's
    tier value alone at every δ. This is the structural asymmetry that makes
    δ = 0 the primary cross-arm setting, where both arms are scored by the
    identical rule."""
    rows = [{"name": "EXPLOIT_VULN", "start_time": 0.0, "finish_time": 1.0}]
    for delta in (0.0, 0.5, 1.0):
        curve = M.baseline_exposure_curve(rows, exposure_test_model(delta=delta))
        assert curve.increments == (0.25,)  # EXPLOIT_VULN -> tier 2 -> 0.5^2


# -- seeded gates 2-4 -------------------------------------------------------


def test_the_curve_re_derives_exactly_from_a_re_created_run(seeded_movement_run) -> None:
    """Gate 3, determinism: the reader is a pure function of the records, so a
    re-created run yields a bit-identical curve. Re-running the simulation rather
    than re-reading the same object is the point — it pins the record stream as
    well as the arithmetic."""
    from mtdsim.l3_simulation.movement.run import run_movement

    again = run_movement(
        "objective_none_c2", seed=0, horizon=3_000,
        mtd_scheme="random", mtd_interval=200,
    )
    model = exposure_test_model()
    first = M.exposure_curve(seeded_movement_run, model)
    second = M.exposure_curve(again, model)
    assert first == second


def test_one_recorded_run_yields_the_whole_sweep(seeded_movement_run) -> None:
    """The reader's cheapness property, inherited from the disengagement measure:
    every declared parameter lives on the model, so a sweep costs no additional
    simulation. If this ever needed re-running, the sweep would cost 40x what it
    does."""
    curves = {
        (tau, rho): M.exposure_curve(
            seeded_movement_run, exposure_test_model(tau=tau, rho=rho)
        ).mean_exposure
        for tau in (3.75, 15.0, 960.0)
        for rho in (1.0, 0.5)
    }
    assert len(set(curves.values())) == len(curves)  # every cell distinct


def test_the_exploitability_field_is_populated_only_by_exploit_dispatches(
    seeded_movement_run,
) -> None:
    """The widening's own gate. A figure on a non-exploit record would mean the
    driver read a stale ``curr_vulns``, which is the one way this field can lie —
    and it would lie *silently*, since a stale figure is a plausible number."""
    for r in seeded_movement_run.records:
        if r.verb != "EXPLOIT_VULN" or r.blocked:
            assert r.exploitability == 0.0, (r.verb, r.blocked, r.exploitability)
        assert 0.0 <= r.exploitability <= 1.0


def test_the_curve_computes_on_both_arms_from_one_seeded_run_each(
    seeded_movement_run,
) -> None:
    """Gate 4, cross-arm: the same fields are present on both sides, and each
    curve names its own clock so the pricing asymmetry travels with the figure
    rather than with the reader's memory."""
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
    AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0
    ).proceed_attack()
    env.run(until=3_000)
    rows = adversary.get_attack_stats().get_record()

    model = exposure_test_model()
    movement = M.exposure_curve(seeded_movement_run, model)
    baseline = M.baseline_exposure_curve(rows, model, elapsed=float(env.now))

    for curve in (movement, baseline):
        assert curve.n_events > 0
        assert curve.mean_exposure is not None
        assert curve.mean_increment is not None
        assert curve.time_average_exposure is not None
    assert movement.clock != baseline.clock
    # the one summary that compares with no caveat at all
    assert movement.mean_increment > 0 and baseline.mean_increment > 0


# ---------------------------------------------------------------------------
# §9b the duty-cycle summaries — stealth_dutycycle_prereg.md §3
#
# These exist because the two summaries above are provably blind to spacing, and
# the tests below assert exactly that before testing what replaces them.
# ---------------------------------------------------------------------------


def test_the_time_average_is_algebraically_a_rate() -> None:
    """The identity that retired it for this question: every event contributes
    ``d*tau`` to the integral WHATEVER its spacing, so the time average is
    ``tau * sum(d) / T`` — a count per unit time, blind to burstiness. Two runs
    with identical events and wildly different spacing must agree."""
    model = exposure_test_model()
    dense = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 1.0, 2.0]), termination=900.0), model
    )
    spread = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 400.0, 800.0]), termination=900.0), model
    )
    predicted = D_LOUD * TAU * 3.0 / 900.0
    assert dense.time_average_exposure == pytest.approx(predicted, rel=1e-3)
    assert spread.time_average_exposure == pytest.approx(predicted, rel=1e-3)


def test_the_concentration_ratio_is_degenerate_on_a_mostly_silent_run() -> None:
    """**The pre-registered primary statistic fails here, and this pins why.**

    ``p90/p50`` divides by a quantile that goes to zero whenever the attacker is
    silent for most of the run — which is the normal case at a short decay
    constant. Both runs below then return astronomically large numbers whose
    ordering reflects how deep the silence got rather than how bursty the process
    was, so the ratio is reporting a numerical artefact and not a duty cycle.

    Recorded as a property of the statistic rather than worked around: the study
    that pre-registered it fell back to the quiet-fraction frontier, which was
    pre-registered alongside it and is bounded by construction (next test).
    """
    model = exposure_test_model()
    dense = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 1.0, 2.0]), termination=900.0), model
    )
    spread = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 400.0, 800.0]), termination=900.0), model
    )
    assert dense.concentration() > 1e5
    assert spread.concentration() > 1e5


def test_the_quiet_fraction_frontier_discriminates_where_the_ratio_cannot() -> None:
    """The bounded statistic on the same two runs. Three acts crammed into three
    seconds leave the rest of the run silent; three acts spread across it do not,
    so the dense run is quiet for MORE of its life at every threshold. Bounded in
    [0, 1] by construction, so it cannot blow up the way the ratio does."""
    model = exposure_test_model()
    dense = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 1.0, 2.0]), termination=900.0), model
    )
    spread = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0, 400.0, 800.0]), termination=900.0), model
    )
    for theta in (0.01, 0.05, 0.25):
        assert dense.quiet_fraction(theta) > spread.quiet_fraction(theta)
        assert 0.0 <= spread.quiet_fraction(theta) <= 1.0


def test_the_time_grid_starts_at_zero_before_the_first_event() -> None:
    """Nothing had happened, so the level is zero — not the first increment
    back-projected."""
    curve = M.exposure_curve(
        run_of(*visits_at(LOUD, [50.0]), termination=100.0), exposure_test_model()
    )
    grid = curve.time_grid(step=1.0)
    assert grid[0] == 0.0 and grid[49] == 0.0
    assert grid[50] == pytest.approx(D_LOUD)


def test_the_time_grid_decays_between_events() -> None:
    """One act at t = 0, tau = 10: the level at t = 10 is exactly 1/e of it."""
    curve = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0]), termination=100.0), exposure_test_model()
    )
    grid = curve.time_grid(step=1.0)
    assert grid[10] == pytest.approx(D_LOUD * math.exp(-1.0))


def test_quiet_fraction_is_self_normalising_and_swept() -> None:
    """The threshold is a reporting axis, not a declared value: it is a fraction
    of the run's OWN peak, so the statistic is a shape rather than a level, and
    it is monotone in the threshold."""
    curve = M.exposure_curve(
        run_of(*visits_at(LOUD, [0.0]), termination=200.0), exposure_test_model()
    )
    fractions = [curve.quiet_fraction(t) for t in (0.01, 0.05, 0.25, 0.5)]
    assert fractions == sorted(fractions)
    assert 0.0 <= fractions[0] <= fractions[-1] <= 1.0


def test_concentration_is_none_rather_than_infinite_on_a_silent_median() -> None:
    """An arm quiet for more than half its run has no defined p90/p50, and
    reporting a huge number there would be an artefact of dividing by nearly
    nothing. None routes the reader to the quiet-fraction frontier instead."""
    empty = M.exposure_curve(run_of(), exposure_test_model())
    assert empty.concentration() is None
    assert empty.time_quantile(0.5) is None


def test_a_dwell_only_visit_contributes_time_but_no_signal() -> None:
    """R1 end to end, through the reader: the dwell-only visit between two acts
    adds no increment, and the gap it occupies still decays the level. That pair
    of facts IS the low-and-slow mechanism."""
    model = exposure_model()  # ruled defaults
    stream = [
        rec(EXPLOITY, step=0, start=0.0, end=1.0, dwell=1.0),
        rec("impact", step=1, verb="", verdict="", start=50.0, end=90.0,
            dwell=40.0, place_class=DWELL_ONLY),
        rec(EXPLOITY, step=2, start=100.0, end=101.0, dwell=1.0),
    ]
    curve = M.exposure_curve(run_of(*stream, termination=200.0), model)
    assert curve.increments[1] == 0.0
    # the level at the third act is its own increment plus almost nothing
    assert curve.levels[2] == pytest.approx(curve.increments[2], rel=1e-2)
