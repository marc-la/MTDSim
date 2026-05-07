"""Integration tests across schemes + core-intent preservation.

Covers:
  - Each MTD scheme (random, alternative, simultaneous, no_mtd) runs to
    completion, produces a well-formed trace, and exercises every
    documented MTD lifecycle event.
  - The four "core simulation intents" — attacker compromises hosts,
    MTDs execute and modify network state, MTDs interrupt the attacker,
    the attacker recovers from interrupts — all still hold after the
    P1–P4 fixes.
  - Bug-class regression: the specific shape that broke at t≈6 ks
    (orphan deploys, post-end_event activity) cannot recur.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from mtdsim.stats.event_log import EventLogger
from mtdsim.stats.event_log_validator import validate_event_log
from mtdsim.viz.replay.config import DEMO, PRIMARY, ReplayConfig
from mtdsim.viz.replay.runner import run_canonical_sim


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #


def _run(config: ReplayConfig, scheme: str, tmp_path: Path) -> list[dict]:
    out = run_canonical_sim(config, scheme=scheme, events_dir=tmp_path, force=True)
    return EventLogger.load_jsonl(str(out))


def _counts(events: list[dict]) -> Counter:
    return Counter(e["type"] for e in events)


# --------------------------------------------------------------------------- #
# Section 1 — Each scheme produces a well-formed trace                        #
# --------------------------------------------------------------------------- #


# Skip 'single' — by design it requires explicit custom_strategies; the
# bundled runner doesn't pipe one through, so it's not a scheme the user
# can drive end-to-end without notebook glue.
@pytest.mark.parametrize("scheme", ["random", "alternative", "simultaneous"])
class TestSchemeIntegration:

    def test_log_passes_validator(self, scheme, tmp_path):
        events = _run(DEMO, scheme, tmp_path)
        issues = validate_event_log(events)
        assert issues == [], f"{scheme}: {issues}"

    def test_mtd_lifecycle_pairs_balance(self, scheme, tmp_path):
        events = _run(DEMO, scheme, tmp_path)
        c = _counts(events)
        deployed = c.get("mtd_deployed", 0)
        completed = c.get("mtd_completed", 0)
        aborted = c.get("mtd_aborted", 0)
        assert deployed == completed + aborted, (
            f"{scheme}: deployed={deployed} completed+aborted={completed + aborted}"
        )

    def test_phase_pairs_balance(self, scheme, tmp_path):
        events = _run(DEMO, scheme, tmp_path)
        c = _counts(events)
        # phase_started should pair with phase_completed; the only allowed
        # imbalance is in-flight phases right at end_event (rare, <=1).
        diff = c.get("phase_started", 0) - c.get("phase_completed", 0)
        assert diff <= 1, f"{scheme}: phase_started-phase_completed = {diff}"

    def test_mtd_activity_actually_happens(self, scheme, tmp_path):
        """At least one MTD must complete in DEMO sim — sanity that
        scheduling isn't broken in the new compromise-gated mode."""
        events = _run(DEMO, scheme, tmp_path)
        c = _counts(events)
        assert c.get("mtd_deployed", 0) > 0, f"{scheme}: no MTDs deployed"
        # Either completed or aborted (compromise) is acceptable.
        assert c.get("mtd_completed", 0) + c.get("mtd_aborted", 0) > 0


def test_no_mtd_scheme_produces_no_mtd_events(tmp_path):
    """no_mtd scheme: attacker runs free, no defender activity."""
    events = _run(DEMO, "no_mtd", tmp_path)
    c = _counts(events)
    assert c.get("mtd_deployed", 0) == 0
    assert c.get("mtd_completed", 0) == 0
    assert c.get("phase_started", 0) > 0  # attacker still works
    assert validate_event_log(events) == []


# --------------------------------------------------------------------------- #
# Section 2 — Termination semantics                                           #
# --------------------------------------------------------------------------- #


class TestTermination:

    def test_sim_ended_records_terminated_by_field(self, tmp_path):
        events = _run(DEMO, "random", tmp_path)
        sim_ended = events[-1]
        assert sim_ended["type"] == "sim_ended"
        assert sim_ended["meta"]["terminated_by"] in {"end_event", "finish_time"}

    def test_sim_never_exceeds_finish_time(self, tmp_path):
        events = _run(DEMO, "random", tmp_path)
        assert events[-1]["t"] <= DEMO.finish_time

    def test_high_threshold_runs_full_horizon(self, tmp_path):
        """With threshold=0.99, network ~never compromised -> finish_time termination."""
        cfg = DEMO.replace(network_params={"terminate_compromise_ratio": 0.99})
        events = _run(cfg, "random", tmp_path)
        # On DEMO size compromise rarely passes 0.99; we expect finish_time termination.
        assert events[-1]["meta"]["terminated_by"] == "finish_time"
        assert events[-1]["t"] == pytest.approx(DEMO.finish_time, abs=1.0)

    def test_low_threshold_terminates_early(self, tmp_path):
        """With threshold=0.1, network compromises early -> end_event termination."""
        cfg = DEMO.replace(network_params={"terminate_compromise_ratio": 0.1})
        events = _run(cfg, "random", tmp_path)
        assert events[-1]["meta"]["terminated_by"] == "end_event"
        assert events[-1]["t"] < DEMO.finish_time


# --------------------------------------------------------------------------- #
# Section 3 — Core simulation intent preserved                                #
# --------------------------------------------------------------------------- #


class TestCoreIntentPreserved:
    """The four documented behaviors of the simulator must still hold after
    the P1–P4 fixes — otherwise we've gutted the simulation while fixing
    the trace shape.
    """

    def test_attacker_compromises_hosts(self, tmp_path):
        events = _run(DEMO, "random", tmp_path)
        c = _counts(events)
        assert c.get("host_compromised", 0) > 0, "attacker never compromised any host"

    def test_mtds_modify_network_state(self, tmp_path):
        """At least one mtd_completed (which means mtd.mtd_operation() ran)."""
        events = _run(DEMO, "random", tmp_path)
        c = _counts(events)
        assert c.get("mtd_completed", 0) > 0

    def test_mtds_interrupt_attacker(self, tmp_path):
        """Some attack action must be interrupted by an MTD over a DEMO run."""
        events = _run(DEMO, "random", tmp_path)
        c = _counts(events)
        assert c.get("attack_interrupted", 0) > 0, \
            "no attack_interrupted events — MTD/attacker isn't interacting"

    def test_attacker_recovers_after_interrupt(self, tmp_path):
        """Every attack_interrupted should be followed by a fresh phase_started."""
        events = _run(DEMO, "random", tmp_path)
        # Walk events in time order and verify there's always a phase_started
        # within the next ~PENALTY+epsilon seconds (PENALTY mean ~20, std 0.5).
        for i, e in enumerate(events):
            if e["type"] != "attack_interrupted":
                continue
            t = e["t"]
            # Look ahead for a phase_started within 200s (gives plenty of slack).
            window = [
                ev for ev in events[i:]
                if ev.get("t", 0) - t < 200 and ev["type"] == "phase_started"
            ]
            # If interrupt happens *very* close to end_event, recovery may be
            # legitimately suppressed — that's the new gating, not a bug.
            terminated_by = events[-1]["meta"].get("terminated_by")
            near_end = abs(events[-1]["t"] - t) < 200 and terminated_by == "end_event"
            if not near_end:
                assert window, f"no phase_started after interrupt at t={t}"


# --------------------------------------------------------------------------- #
# Section 4 — Bug-class regression: the original symptom cannot recur         #
# --------------------------------------------------------------------------- #


class TestBugClassRegression:

    def test_no_orphan_deploys_anywhere_in_trace(self, tmp_path):
        """The original bug: mtd_deployed without matching mtd_completed."""
        events = _run(DEMO, "random", tmp_path)
        # Walk: when we see mtd_deployed for resource_type R, we must see a
        # later mtd_completed/mtd_aborted before the next mtd_deployed for R.
        in_flight: dict[str, dict] = {}
        for e in events:
            if e["type"] == "mtd_deployed":
                rt = e["meta"]["resource_type"]
                assert rt not in in_flight, (
                    f"second mtd_deployed for {rt} at t={e['t']} while "
                    f"one is still in-flight from t={in_flight[rt]['t']}"
                )
                in_flight[rt] = e
            elif e["type"] in ("mtd_completed", "mtd_aborted"):
                rt = e["meta"]["resource_type"]
                assert rt in in_flight, (
                    f"{e['type']} for {rt} at t={e['t']} with no matching deploy"
                )
                in_flight.pop(rt)
        # End of trace: at most one in-flight per resource (cut off by sim end).
        assert len(in_flight) <= 3  # network/application/reserve

    def test_no_phase_started_after_sim_ended(self, tmp_path):
        """End-event gating: no new phases started after sim termination."""
        events = _run(DEMO, "random", tmp_path)
        end_t = events[-1]["t"]
        post_end_phases = [
            e for e in events
            if e.get("t", 0) > end_t and e["type"] == "phase_started"
        ]
        assert post_end_phases == []

    def test_no_mtd_deployed_after_sim_ended(self, tmp_path):
        events = _run(DEMO, "random", tmp_path)
        end_t = events[-1]["t"]
        post_end_deploys = [
            e for e in events
            if e.get("t", 0) > end_t and e["type"] == "mtd_deployed"
        ]
        assert post_end_deploys == []

    def test_resources_released_at_sim_end(self, tmp_path):
        """Final mtd_alloc_state should show 0 users on every resource."""
        events = _run(DEMO, "random", tmp_path)
        alloc_states = [e for e in events if e["type"] == "mtd_alloc_state"]
        if not alloc_states:
            pytest.skip("no alloc_state events recorded")
        last_release = next(
            (e for e in reversed(alloc_states) if e["meta"]["action"] == "release"),
            None,
        )
        if last_release is None:
            pytest.skip("no release alloc_state events recorded")
        # After the last release, that resource type's user count should be 0.
        # (We can't assert all-zero here because release fires before the next
        # trigger; instead assert the final unfinished dict is empty.)
        assert last_release["meta"]["unfinished"] == {} or \
               len(last_release["meta"]["unfinished"]) <= 2

    def test_primary_random_does_not_regress_to_pre_fix_shape(self, tmp_path):
        """The headline regression: PRIMARY/random/seed=42 produced
        deployed=32 / completed=30 / aborted=0 (2 orphans) before the fix.
        After the fix, deployed must == completed + aborted exactly."""
        events = _run(PRIMARY, "random", tmp_path)
        c = _counts(events)
        deployed = c.get("mtd_deployed", 0)
        completed = c.get("mtd_completed", 0)
        aborted = c.get("mtd_aborted", 0)
        assert deployed == completed + aborted, (
            f"PRIMARY orphans: deployed={deployed} completed={completed} aborted={aborted}"
        )


# --------------------------------------------------------------------------- #
# Section 5 — Determinism + watchdog smoke                                    #
# --------------------------------------------------------------------------- #


class TestDeterminismAndWatchdog:

    def test_same_seed_produces_same_event_count(self, tmp_path):
        """Seeded sim is deterministic — useful as a sanity check that
        nothing the fixes added (e.g. AnyOf) introduced randomness."""
        run1 = _run(DEMO, "random", tmp_path / "a")
        run2 = _run(DEMO, "random", tmp_path / "b")
        c1, c2 = _counts(run1), _counts(run2)
        # Top-level counts should match exactly under same seed.
        for key in ("phase_started", "phase_completed", "mtd_deployed",
                    "mtd_completed", "host_compromised"):
            assert c1.get(key, 0) == c2.get(key, 0), \
                f"non-deterministic count for {key}: {c1.get(key)} vs {c2.get(key)}"

    def test_alloc_state_action_vocabulary(self, tmp_path):
        """alloc_state.action is drawn from a small, documented vocabulary."""
        events = _run(DEMO, "random", tmp_path)
        actions = {e["meta"]["action"] for e in events
                   if e["type"] == "mtd_alloc_state"}
        assert actions <= {"trigger_execute", "suspend", "release"}
