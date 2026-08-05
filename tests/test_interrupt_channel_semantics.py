"""Regression tests pinning the direct attacker/defender channel semantics
ruled in boundary review 3 (D-20/D-21/D-22, Marc, 2026-08-03 — options (a)
throughout; the review record is
``docs/implementation/boundary_attacker_defender_channels.md``).

What each guards:

- **D-20, class-level pricing ratified.** Channels 1-3 are functions of the
  mutating resource class alone: the interrupt gate keys on
  (resource class x ``curr_process``) with no per-mechanism term, the confusion
  penalty is one flat draw for every class, and the cursor clear is
  network-class only. The truth-table test pins the ratified grid exactly, so
  any future per-mechanism differentiation is a deliberate re-decision (it
  would land here first), never drift.
- **D-21, the movement arm's exposure profile ratified as mapping policy.**
  The ``DWELL`` sentinel a dwell-only place announces is judged interruptible
  by the network and application classes — a dwell-only place is not a
  cost-free hiding spot from MTD — and immune to reserve. The recon verbs
  (SCAN_HOST / ENUM_HOST / SCAN_NEIGHBOR) stay application-immune, which is
  the documented gate semantics (IS-INT-05) the profiled attacker's greater
  recon share is priced under.
- **D-22, overlap semantics kept.** A second interrupt landing mid-penalty is
  absorbed, never stacked or restarted, so a fast mutation schedule cannot
  freeze the attacker; the native arm's equivalent is the ``is_alive`` guard
  (its interrupted process is dead for the penalty window). Both are pinned.

These tests execute the real deciding methods (``_interrupt_adversary``,
``apply_mtd_interrupt_cost``) against stub collaborators — the same instrument
the review used — so they run in milliseconds and touch no golden.
"""

from __future__ import annotations

import os
import random
import sys

import simpy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtdnetwork.data.constants import ATTACK_DURATION
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.operation.mtd_operation import MTDOperation


class _StubMTD:
    def __init__(self, resource_type):
        self._rt = resource_type

    def get_resource_type(self):
        return self._rt

    def get_name(self):
        return "Stub"


class _StubStats:
    def __init__(self):
        self.count = 0

    def add_total_attack_interrupted(self):
        self.count += 1


class _StubNetwork:
    def __init__(self):
        self.stats = _StubStats()

    def get_mtd_stats(self):
        return self.stats


class _StubAdversary:
    """Only what the two real methods consult."""

    def __init__(self, curr_process):
        self._curr_process = curr_process
        self._curr_host_id = 7
        self.curr_host = object()

    def get_curr_process(self):
        return self._curr_process

    def set_curr_host_id(self, v):
        self._curr_host_id = v

    def set_curr_host(self, v):
        self.curr_host = v

    def get_curr_host_id(self):
        return self._curr_host_id

    def get_curr_host(self):
        return self.curr_host


class _GateHarness:
    """Carries only the attributes _interrupt_adversary reads on `self`."""

    def __init__(self, attack_operation, network):
        self.attack_operation = attack_operation
        self.network = network
        self.logging = False
        self._proceed_time = 0


def _fire_gate(curr_process, resource_class, *, alive=True):
    """Run the real gate once; return True if it interrupted."""
    env = simpy.Environment()
    adversary = _StubAdversary(curr_process)
    attack_op = AttackOperation(env, env.event(), adversary)

    def victim():
        try:
            yield env.timeout(1000)
        except simpy.Interrupt:
            pass

    proc = env.process(victim())
    attack_op.set_attack_process(proc)
    env.run(until=0.1)  # let the victim start so is_alive holds
    if not alive:
        proc.interrupt()
        env.run(until=0.2)  # the victim exits; the process is now dead
    harness = _GateHarness(attack_op, _StubNetwork())
    MTDOperation._interrupt_adversary(harness, env, _StubMTD(resource_class))
    return harness.network.stats.count == 1


# The ratified grid (D-20/D-21): curr_process -> classes that interrupt.
# DWELL is the movement arm's dwell-only sentinel; the six verbs are shared.
TRUTH_TABLE = {
    "SCAN_HOST": {"network"},
    "ENUM_HOST": {"network"},
    "SCAN_PORT": {"network", "application"},
    "SCAN_NEIGHBOR": {"network"},
    "EXPLOIT_VULN": {"network", "application"},
    "BRUTE_FORCE": {"network", "application", "reserve"},
    "DWELL": {"network", "application"},
}


def test_the_interrupt_gate_matches_the_ratified_truth_table() -> None:
    for curr_process, interrupting in TRUTH_TABLE.items():
        for resource_class in ("network", "application", "reserve"):
            fired = _fire_gate(curr_process, resource_class)
            expected = resource_class in interrupting
            assert fired == expected, (
                f"{resource_class} x {curr_process}: expected "
                f"{'interrupt' if expected else 'no interrupt'}, got the opposite"
            )


def test_a_dead_attack_process_is_never_interrupted() -> None:
    """The native arm's penalty-window immunity: the gate guards on is_alive."""
    for resource_class in ("network", "application", "reserve"):
        assert not _fire_gate("EXPLOIT_VULN", resource_class, alive=False)


def test_the_cursor_is_cleared_only_by_the_network_class() -> None:
    random.seed(42)
    for resource_class, cleared in (
        ("network", True), ("application", False), ("reserve", False),
    ):
        env = simpy.Environment()
        adversary = _StubAdversary("EXPLOIT_VULN")
        attack_op = AttackOperation(env, env.event(), adversary)
        mtd = _StubMTD(resource_class)

        def pay():
            yield from attack_op.apply_mtd_interrupt_cost(mtd)

        env.process(pay())
        env.run()
        got = adversary.get_curr_host_id() == -1 and adversary.curr_host is None
        assert got == cleared, resource_class
        # The penalty itself is the same flat draw whatever the class.
        assert env.now >= ATTACK_DURATION["PENALTY"]


def test_a_second_interrupt_mid_penalty_is_absorbed_not_stacked() -> None:
    random.seed(42)
    env = simpy.Environment()
    adversary = _StubAdversary("EXPLOIT_VULN")
    attack_op = AttackOperation(env, env.event(), adversary)
    mtd = _StubMTD("application")
    done = {}

    def pay():
        yield from attack_op.apply_mtd_interrupt_cost(mtd)
        done["t"] = env.now

    proc = env.process(pay())

    def second_hit():
        yield env.timeout(1.0)
        if proc.is_alive:
            proc.interrupt()

    env.process(second_hit())
    env.run()
    # Absorbed: the payer completes where the second interrupt landed (t = 1.0)
    # and no exception escapes. A restarted penalty would complete at >= 21, a
    # stacked one at >= 40 — both beyond the single-draw floor asserted here.
    # (env.now itself drifts to the orphaned first timeout, so the payer's own
    # completion time is what is measured.)
    assert done["t"] < ATTACK_DURATION["PENALTY"]
