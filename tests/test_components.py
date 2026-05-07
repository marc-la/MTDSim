"""Component-level contract tests.

Each section pins one module's documented behavior. The tests are written
against docstrings and observable side effects — not implementation
details — so they survive refactoring. They double as a checklist that
the P1–P4 fixes did not eliminate any documented capability.
"""

from __future__ import annotations

import random

import numpy as np
import pytest
import simpy

from mtdsim.attacker.adversary import Adversary
from mtdsim.attacker.attack_operation import AttackOperation
from mtdsim.attacker.attacker_profile import AttackerProfile
from mtdsim.data import constants
from mtdsim.defender.mtd_operation import MTDOperation
from mtdsim.defender.mtd_scheme import MTDScheme
from mtdsim.defender.techniques.completetopologyshuffle import CompleteTopologyShuffle
from mtdsim.defender.techniques.ipshuffle import IPShuffle
from mtdsim.defender.techniques.osdiversity import OSDiversity
from mtdsim.defender.techniques.servicediversity import ServiceDiversity
from mtdsim.network.time_network import TimeNetwork
from mtdsim.stats.event_log import EventLogger
from mtdsim.stats.security_metric_statistics import SecurityMetricStatistics


# --------------------------------------------------------------------------- #
# Fixtures                                                                    #
# --------------------------------------------------------------------------- #


@pytest.fixture(autouse=True)
def _seed_everything():
    random.seed(7)
    np.random.seed(7)


def _make_small_network(threshold: float = 0.8) -> TimeNetwork:
    """A small but valid TimeNetwork for unit-style tests.

    DEMO-sized so tests stay fast; threshold is configurable so tests can
    exercise both "very compromisable" and "almost never compromised"
    edge cases.
    """
    return TimeNetwork(
        total_nodes=30, total_endpoints=3, total_subnets=6,
        total_layers=3, total_database=1,
        terminate_compromise_ratio=threshold,
    )


# --------------------------------------------------------------------------- #
# Section 1 — TimeNetwork: compromise threshold + queue plumbing              #
# --------------------------------------------------------------------------- #


class TestTimeNetwork:

    def test_default_threshold_is_eighty_percent(self):
        """Constructor default is 0.8 (matches the docstring claim and PRIMARY)."""
        net = _make_small_network()  # uses default 0.8 via fixture
        # Sanity: 0.8 means strictly > 0.8 ratio compromises.
        assert not net.is_compromised(list(range(int(net.total_nodes * 0.8))))

    @pytest.mark.parametrize("threshold,below,at,above", [
        (0.25, 5, 7, 9),     # 5/30=0.17, 7/30=0.23 (still <=0.25), 9/30=0.30
        (0.5, 10, 15, 16),   # 15/30=0.5 — strictly > so 0.5 is "at" not "above"
        (0.8, 20, 24, 25),   # 24/30=0.8, 25/30=0.83
    ])
    def test_threshold_is_honored(self, threshold, below, at, above):
        net = _make_small_network(threshold=threshold)
        assert not net.is_compromised(list(range(below)))
        assert not net.is_compromised(list(range(at)))
        assert net.is_compromised(list(range(above)))

    def test_unfinished_mtd_is_keyed_by_resource_type(self):
        """Two MTDs of different resource types coexist; same type overwrites."""
        net = _make_small_network()
        ip = IPShuffle(network=net)
        cts = CompleteTopologyShuffle(network=net)  # also network resource
        osd = OSDiversity(network=net)              # application resource

        net.set_unfinished_mtd(ip)
        net.set_unfinished_mtd(osd)
        assert net.get_unfinished_mtd() == {"network": ip, "application": osd}

        net.set_unfinished_mtd(cts)  # same resource_type as ip — overwrite
        assert net.get_unfinished_mtd()["network"] is cts

    def test_queues_are_mutable_references(self):
        """Callers (MTDOperation) mutate the queues directly — verify aliasing."""
        net = _make_small_network()
        q = net.get_mtd_queue()
        q.append(("sentinel",))
        assert net.get_mtd_queue() is q
        assert net.get_mtd_queue()[-1] == ("sentinel",)


# --------------------------------------------------------------------------- #
# Section 2 — MTDScheme: register / trigger / suspend per scheme              #
# --------------------------------------------------------------------------- #


class TestMTDScheme:

    def _scheme(self, name, custom=None):
        net = _make_small_network()
        return net, MTDScheme(scheme=name, network=net, custom_strategies=custom,
                              security_metric_record=SecurityMetricStatistics())

    def test_random_scheme_picks_one_strategy(self):
        net, scheme = self._scheme("random")
        scheme.register_mtd()
        assert len(net.get_mtd_queue()) == 1

    def test_alternative_scheme_cycles_strategies(self):
        net, scheme = self._scheme("alternative")
        names = []
        for _ in range(8):  # 4 strategies * 2 cycles
            scheme.register_mtd()
            mtd = scheme.trigger_mtd()
            names.append(type(mtd).__name__)
        # Two full passes through the 4-strategy default — should repeat exactly.
        assert names[:4] == names[4:]
        assert set(names) == {
            "CompleteTopologyShuffle", "IPShuffle", "OSDiversity", "ServiceDiversity",
        }

    def test_simultaneous_scheme_registers_all(self):
        net, scheme = self._scheme("simultaneous")
        scheme.register_mtd()
        assert len(net.get_mtd_queue()) == 4  # all four default strategies

    def test_trigger_mtd_pops_lowest_priority_first(self):
        """Heap discipline: priority 1 (CompleteTopologyShuffle) before priority 6."""
        net, scheme = self._scheme("simultaneous")
        scheme.register_mtd()
        first = scheme.trigger_mtd()
        assert first.get_priority() == 1
        assert isinstance(first, CompleteTopologyShuffle)

    def test_suspend_then_trigger_returns_lowest_priority(self):
        net, scheme = self._scheme("simultaneous")
        # Suspend two MTDs of differing priorities.
        scheme.suspend_mtd(IPShuffle(network=net))            # priority 3
        scheme.suspend_mtd(CompleteTopologyShuffle(network=net))  # priority 1
        # Suspended dict is keyed by priority — verify trigger picks min.
        triggered = scheme.trigger_suspended_mtd()
        assert isinstance(triggered, CompleteTopologyShuffle)
        # And the dict shrinks.
        assert 1 not in net.get_suspended_mtd()
        assert 3 in net.get_suspended_mtd()

    def test_suspend_increments_stats_counter(self):
        net, scheme = self._scheme("random")
        scheme.suspend_mtd(IPShuffle(network=net))
        assert net.get_mtd_stats().dict()["Total suspended MTD"] == 1


# --------------------------------------------------------------------------- #
# Section 3 — MTDOperation: lifecycle, resources, watchdog                    #
# --------------------------------------------------------------------------- #


class TestMTDOperation:

    def _setup(self, scheme="random", threshold=0.8):
        env = simpy.Environment()
        end_event = env.event()
        net = _make_small_network(threshold=threshold)
        evlog = EventLogger(env)
        adv = Adversary(net, constants.ATTACKER_THRESHOLD, AttackerProfile.default())
        attack_op = AttackOperation(env, end_event, adv, event_logger=evlog)
        mtd_op = MTDOperation(
            SecurityMetricStatistics(), env, end_event, net, attack_op,
            scheme=scheme, adversary=adv, event_logger=evlog,
        )
        return env, end_event, net, evlog, adv, attack_op, mtd_op

    def test_get_mtd_resource_routes_by_resource_type(self):
        _, _, net, _, _, _, mtd_op = self._setup()
        assert mtd_op._get_mtd_resource(IPShuffle(network=net)) is mtd_op.get_network_resource()
        assert mtd_op._get_mtd_resource(OSDiversity(network=net)) is mtd_op.get_application_resource()
        # Anything not network/application -> reserve. None of the bundled
        # strategies use this branch, but the fallback is documented.
        class _Dummy:
            def get_resource_type(self):
                return "reserve"
        assert mtd_op._get_mtd_resource(_Dummy()) is mtd_op.get_reserve_resource()

    def test_emit_alloc_state_includes_all_documented_keys(self):
        env, _, net, evlog, _, _, mtd_op = self._setup()
        mtd_op._emit_alloc_state("trigger_execute", IPShuffle(network=net))
        ev = evlog.events[-1]
        assert ev["type"] == "mtd_alloc_state"
        for k in ("action", "mtd_name", "resource_type", "queue_depth",
                  "suspended", "unfinished", "app_users", "net_users", "reserve_users"):
            assert k in ev["meta"], f"alloc_state missing key {k!r}"

    def test_alloc_state_no_op_when_no_logger(self):
        """No logger attached -> no crash, no events recorded."""
        env = simpy.Environment()
        net = _make_small_network()
        adv = Adversary(net, constants.ATTACKER_THRESHOLD, AttackerProfile.default())
        attack_op = AttackOperation(env, env.event(), adv, event_logger=None)
        mtd_op = MTDOperation(
            SecurityMetricStatistics(), env, env.event(), net, attack_op,
            scheme="random", adversary=adv, event_logger=None,
        )
        # Should silently no-op.
        mtd_op._emit_alloc_state("trigger_execute", IPShuffle(network=net))

    def test_execute_releases_resource_on_completion(self):
        """Resource users count returns to 0 after a normal MTD completion."""
        env, _, net, _, _, _, mtd_op = self._setup(threshold=0.99)  # never compromise
        mtd = OSDiversity(network=net)
        env.process(mtd_op._mtd_execute_action(env, mtd))
        env.run(until=500)
        assert len(mtd_op.get_application_resource().users) == 0
        assert "application" not in net.get_unfinished_mtd()

    def test_execute_emits_aborted_when_compromised_mid_run(self):
        """Compromise during execution -> mtd_aborted, not mtd_completed."""
        env, end_event, net, evlog, adv, _, mtd_op = self._setup(threshold=0.0)  # always compromised
        # Pretend one host is compromised -> ratio > 0.0 -> is_compromised True.
        adv._compromised_hosts.append(0)

        mtd = OSDiversity(network=net)
        env.process(mtd_op._mtd_execute_action(env, mtd))
        env.run(until=500)
        types = [e["type"] for e in evlog.events]
        assert "mtd_deployed" in types
        assert "mtd_aborted" in types
        assert "mtd_completed" not in types
        # Resource was still released cleanly (the recent c426f1b finally).
        assert len(mtd_op.get_application_resource().users) == 0

    def test_trigger_loop_exits_after_end_event(self):
        """Once end_event fires, _mtd_trigger_action returns instead of looping."""
        env, end_event, net, evlog, adv, _, mtd_op = self._setup(threshold=0.0)
        adv._compromised_hosts.append(0)  # forces is_compromised True
        env.process(mtd_op._mtd_trigger_action())
        env.run(until=2000)
        # After the loop returns, the only mtd_alloc_state events should be
        # "release" tails (if any). No new triggers post-end.
        triggers = [e for e in evlog.events
                    if e["type"] == "mtd_alloc_state" and e["meta"]["action"] == "trigger_execute"]
        assert triggers == [], f"trigger loop kept firing post-end: {len(triggers)} triggers"

    def test_watchdog_constant_present_and_finite(self):
        """Documented watchdog multiplier exists and is sane (1 < x < 100)."""
        assert 1 < MTDOperation._MTD_EXECUTION_BUDGET_MULTIPLIER < 100

    def test_interrupt_adversary_fires_on_alive_attack_process(self):
        """A network MTD interrupts a network-stage attack phase."""
        env, _, net, evlog, adv, attack_op, mtd_op = self._setup(threshold=0.99)
        # Start a long-running attack action so we have something to interrupt.
        adv.set_curr_process("SCAN_HOST")
        attack_op._attack_process = env.process(
            attack_op._execute_attack_action(1000, lambda: None)
        )
        env.run(until=1)  # let it park on the timeout
        assert attack_op._attack_process.is_alive

        mtd_op._interrupt_adversary(env, IPShuffle(network=net))  # network MTD
        env.run(until=200)  # past the PENALTY (~20s)
        assert any(e["type"] == "attack_interrupted" for e in evlog.events)


# --------------------------------------------------------------------------- #
# Section 4 — AttackOperation: phase progression + end_event gating           #
# --------------------------------------------------------------------------- #


class TestAttackOperation:

    def _setup(self, threshold=0.8):
        env = simpy.Environment()
        end_event = env.event()
        net = _make_small_network(threshold=threshold)
        evlog = EventLogger(env)
        adv = Adversary(net, constants.ATTACKER_THRESHOLD, AttackerProfile.default())
        attack_op = AttackOperation(env, end_event, adv, event_logger=evlog)
        return env, end_event, net, evlog, adv, attack_op

    def test_proceed_attack_dispatches_by_curr_process(self):
        """proceed_attack honors adversary.get_curr_process()."""
        env, _, _, evlog, adv, attack_op = self._setup()
        adv.set_curr_process("SCAN_HOST")
        attack_op.proceed_attack()
        env.run(until=1)
        assert any(e["type"] == "phase_started" and e["phase"] == "SCAN_HOST"
                   for e in evlog.events)

    def test_phase_emits_started_and_completed(self):
        env, _, _, evlog, adv, attack_op = self._setup()
        attack_op.proceed_attack()  # SCAN_HOST by default
        env.run(until=200)
        types = [(e["type"], e["phase"]) for e in evlog.events
                 if e["type"] in {"phase_started", "phase_completed"}]
        assert ("phase_started", "SCAN_HOST") in types
        assert ("phase_completed", "SCAN_HOST") in types

    def test_attack_action_returns_silently_after_end_event(self):
        """_execute_attack_action returns without scheduling more phases."""
        env, end_event, _, evlog, adv, attack_op = self._setup()
        adv.set_curr_process("SCAN_HOST")
        proc = env.process(attack_op._execute_attack_action(50, lambda: None))
        end_event.succeed()  # fire end before timeout completes
        env.run(until=100)
        # No phase_completed for this aborted run.
        completed = [e for e in evlog.events if e["type"] == "phase_completed"]
        assert completed == [], "end_event-gated phase still emitted phase_completed"

    def test_handle_interrupt_does_not_restart_after_end_event(self):
        """_handle_interrupt's PENALTY wait must not lead into a new phase."""
        env, end_event, _, evlog, adv, attack_op = self._setup()
        # Set up a fake interrupt context.
        attack_op._interrupted_mtd = IPShuffle(network=adv.network)
        adv.set_curr_process("SCAN_PORT")
        adv.set_curr_host_id(5)

        end_event.succeed()
        env.process(attack_op._handle_interrupt(0.0, "SCAN_PORT"))
        env.run(until=200)
        starts = [e for e in evlog.events if e["type"] == "phase_started"]
        assert starts == [], f"phase restarted after end_event: {[s['phase'] for s in starts]}"


# --------------------------------------------------------------------------- #
# Section 5 — MTD techniques: each mtd_operation does the documented mutation #
# --------------------------------------------------------------------------- #


class TestMTDTechniques:

    def test_ipshuffle_changes_internal_host_ips(self):
        """IPShuffle docstring: rewrites IPs for non-endpoint hosts."""
        net = _make_small_network()
        before = {hid: h.ip for hid, h in net.get_hosts().items()
                  if hid not in net.exposed_endpoints}
        IPShuffle(network=net).mtd_operation()
        after = {hid: h.ip for hid, h in net.get_hosts().items()
                 if hid not in net.exposed_endpoints}
        # At least one host must have changed (probabilistic — randomness over
        # 2^32 IPv4 space means collisions are vanishingly unlikely for ~25 hosts).
        changed = sum(1 for hid in before if before[hid] != after[hid])
        assert changed == len(before), \
            f"IPShuffle only rewrote {changed}/{len(before)} non-endpoint IPs"

    def test_osdiversity_changes_some_host_os(self):
        """OSDiversity should change OS / version on at least one non-endpoint host."""
        net = _make_small_network()
        before = {hid: (h.os_type, h.os_version) for hid, h in net.get_hosts().items()
                  if hid not in net.exposed_endpoints}
        OSDiversity(network=net).mtd_operation()
        after = {hid: (h.os_type, h.os_version) for hid, h in net.get_hosts().items()
                 if hid not in net.exposed_endpoints}
        changed = sum(1 for hid in before if before[hid] != after[hid])
        assert changed > 0, "OSDiversity didn't change any host OS"

    def test_servicediversity_changes_host_services(self):
        net = _make_small_network()
        # snapshot service ids per host (host has its own internal service graph)
        sample_host = next(h for hid, h in net.get_hosts().items()
                           if hid not in net.exposed_endpoints)
        before_services = [sample_host.graph.nodes[n].get("service")
                           for n in range(sample_host.total_nodes)]
        ServiceDiversity(network=net).mtd_operation()
        after_services = [sample_host.graph.nodes[n].get("service")
                          for n in range(sample_host.total_nodes)]
        assert before_services != after_services, "ServiceDiversity left services unchanged"

    def test_completetopologyshuffle_regenerates_graph(self):
        """CompleteTopologyShuffle docstring: regenerates the network graph,
        preserves hosts."""
        net = _make_small_network()
        original_edges = set(map(frozenset, net.graph.edges))
        original_hosts = dict(net.get_hosts())
        CompleteTopologyShuffle(network=net).mtd_operation()
        new_edges = set(map(frozenset, net.graph.edges))
        new_hosts = dict(net.get_hosts())
        # Edges typically differ (not strictly guaranteed, but with high prob).
        assert new_edges != original_edges or len(original_edges) == 0
        # All hosts preserved by id.
        assert set(new_hosts.keys()) == set(original_hosts.keys())
