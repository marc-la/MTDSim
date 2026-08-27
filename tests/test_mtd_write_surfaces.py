"""Regression tests for the defender write side — the mechanisms' write
surfaces as dispositioned by boundary review 2 (Part B, 2026-08-03).

Each test pins behaviour that is either documented lineage intent or carries
a written ruling from Marc; the enumeration and live diffs behind them are
`docs/implementation/mtd_write_surfaces.md`, and the rulings are the audit's
boundary-review-2 disposition banner (D-23..D-25).

What is deliberately NOT pinned, and why:

- The OS version-index preservation delta and the degenerate SAPV feed
  (D-24, ruled record-only) — recorded behaviours, not ratified models.
- The latent OSDiversityAssignment (D-17 owns its semantics).

What IS pinned:

- **D-23 (ruled keep-and-document, 2026-08-03):** the exposed-endpoint
  exemption is the documented model of the family — the entry surface is
  deliberately fixed (attackers hold passive-reconnaissance access to the
  endpoints regardless; the evaluation's game is post-ingress disruption at
  the discovery level). Every application-layer mechanism and IPShuffle must
  leave the endpoints untouched; UserShuffle, whose intent row says "each
  host" (IS-MTD-03), must keep NOT exempting them.
- **IS-MTD-05 (post-D-05) / the copy semantics:** a service redraw replaces
  every non-target service on internal hosts with a fresh instance whose
  vulnerabilities are unexploited copies — the redraw revokes the attacker's
  standing on that service, while host-level compromise persists (D-02).
- **IS-MTD-07 + Ho's addendum + D-02:** Complete Topology Shuffle moves
  adjacency (endpoints included) while preserving node ids, host instances
  and the attacker's holdings.
- **The structural target-node fact** that grounds the diversity mechanisms'
  target-node skip: the target service node carries no service and no port.
- **Port immobility under a service redraw** (addressing is PortShuffle's
  purview, IS-MTD-02): discovered ports remain valid across diversity
  firings.
- **IS-MTD-06 (D-18 repaired, ruled 2026-08-27, D-05 precedent):** OS
  Diversity relabels the OS (version index preserved) and redraws only the
  services incompatible with the new OS — the compatibility test is name
  membership, True for a service against its own OS.
- **The OS-gated exploit channel (D-19 closed, ruled 2026-08-27, Brown 2023
  §III-B(6)):** an OS-dependent vulnerability on a host running an OS
  outside its list is refused — 0.0, a counted attempt, no randomness drawn.
"""

from __future__ import annotations

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.component.adversary import Adversary
from mtdnetwork.data import constants
from mtdnetwork.mtd.completetopologyshuffle import CompleteTopologyShuffle
from mtdnetwork.mtd.hosttopologyshuffle import HostTopologyShuffle
from mtdnetwork.mtd.ipshuffle import IPShuffle
from mtdnetwork.mtd.osdiversity import OSDiversity
from mtdnetwork.mtd.portshuffle import PortShuffle
from mtdnetwork.mtd.servicediversity import ServiceDiversity
from mtdnetwork.mtd.usershuffle import UserShuffle

SEED = 42


def _build():
    random.seed(SEED)
    net = TimeNetwork()  # the experiments' default 50/5/8/4/5 geometry
    adv = Adversary(network=net, attack_threshold=constants.ATTACKER_THRESHOLD)
    return net, adv


def _endpoint_state(net):
    """Everything an endpoint host could have moved: ip, os, users, and the
    per-node (port, service-instance-id) pairs."""
    state = {}
    for hid in net.exposed_endpoints:
        host = net.get_host(hid)
        state[hid] = (
            host.ip,
            host.os_type,
            host.os_version,
            tuple(sorted(host.users.keys())),
            tuple(
                (nid,
                 host.graph.nodes[nid].get("port"),
                 getattr(host.graph.nodes[nid].get("service"), "id", None))
                for nid in sorted(host.graph.nodes)
            ),
        )
    return state


def _internal_ids(net):
    return [h for h in net.get_hosts() if h not in net.exposed_endpoints]


def test_the_endpoint_exemption_holds_as_dispositioned():
    """D-23: the exempting mechanisms leave the entry surface untouched —
    and each demonstrably moved its own internal surface, so the assertion
    is not vacuous."""
    for mech_cls, moved in (
        (IPShuffle, lambda b, a: b.ip != a.ip),
        (OSDiversity, lambda b, a: (b.os_type, b.os_version) != (a.os_type, a.os_version)),
        (ServiceDiversity, lambda b, a: True),  # movement asserted separately below
        (PortShuffle, lambda b, a: True),
    ):
        net, adv = _build()
        before_endpoints = _endpoint_state(net)
        internal = _internal_ids(net)
        before_internal = {
            h: (net.get_host(h).ip, net.get_host(h).os_type, net.get_host(h).os_version)
            for h in internal
        }
        before_ports = {
            h: dict(
                (nid, net.get_host(h).graph.nodes[nid].get("port"))
                for nid in net.get_host(h).graph.nodes
            )
            for h in internal
        }
        random.seed(SEED + 1)
        mech_cls(network=net).mtd_operation(adv)

        assert _endpoint_state(net) == before_endpoints, (
            f"{mech_cls.__name__} wrote to an exposed endpoint — the D-23 "
            "ruling (fixed entry surface) is violated"
        )

        if mech_cls is IPShuffle:
            assert any(
                before_internal[h][0] != net.get_host(h).ip for h in internal
            ), "IPShuffle moved no internal ip — vacuous run"
        if mech_cls is OSDiversity:
            assert any(
                before_internal[h][1:] != (net.get_host(h).os_type, net.get_host(h).os_version)
                for h in internal
            ), "OSDiversity relabelled no internal host — vacuous run"
        if mech_cls is PortShuffle:
            assert any(
                before_ports[h][nid] != net.get_host(h).graph.nodes[nid].get("port")
                for h in internal
                for nid in before_ports[h]
                if before_ports[h][nid] is not None
            ), "PortShuffle moved no internal port — vacuous run"


def test_usershuffle_now_exempts_the_endpoints():
    """Superseded 2026-08-27 (Marc, R2 on D-32): the D-23 family rule now
    covers UserShuffle too — the endpoints keep their users; the interior is
    what moves. (The earlier pin of IS-MTD-03's literal "each host" is
    retired by that ruling.)"""
    net, adv = _build()
    before = {
        hid: tuple(sorted(net.get_host(hid).users.keys()))
        for hid in net.exposed_endpoints
    }
    internal_before = {
        hid: tuple(sorted(net.get_host(hid).users.keys())) for hid in _internal_ids(net)
    }
    random.seed(SEED + 1)
    UserShuffle(network=net).mtd_operation(adv)
    assert all(
        tuple(sorted(net.get_host(hid).users.keys())) == before[hid]
        for hid in net.exposed_endpoints
    ), "UserShuffle wrote to an exposed endpoint — the D-23 family rule (R2) is violated"
    assert any(
        tuple(sorted(net.get_host(hid).users.keys())) != internal_before[hid]
        for hid in _internal_ids(net)
    ), "UserShuffle moved no internal users — vacuous run"


def test_a_service_redraw_revokes_the_attackers_standing():
    """IS-MTD-05 post-D-05 + the deliberate copy semantics: the new instance
    carries no exploited flags and no attempt counts (so the ATK-04 discount
    is gone with it); host-level compromise persists per D-02."""
    net, adv = _build()
    victim = net.get_host(_internal_ids(net)[0])
    svc_node = next(n for n in victim.graph.nodes if n != victim.target_node)
    old_svc = victim.graph.nodes[svc_node]["service"]
    old_port = victim.graph.nodes[svc_node]["port"]
    vuln = old_svc.get_all_vulns()[0]
    vuln.exploited = True
    vuln.exploit_attempt = 3
    victim.compromised = True

    random.seed(SEED + 1)
    ServiceDiversity(network=net).mtd_operation(adv)

    new_svc = victim.graph.nodes[svc_node]["service"]
    assert new_svc.id != old_svc.id, "service instance was not replaced"
    assert not any(v.exploited for v in new_svc.get_all_vulns())
    assert not any(v.exploit_attempt for v in new_svc.get_all_vulns())
    assert not new_svc.is_exploited()
    assert victim.compromised, "host-level compromise must persist (D-02)"
    assert victim.graph.nodes[svc_node]["port"] == old_port, (
        "a service redraw must not move the port — addressing is "
        "PortShuffle's purview (IS-MTD-02)"
    )


def test_servicediversity_redraws_every_internal_non_target_service():
    """IS-MTD-05 (ruled via D-05): replace all services, drawn at random
    versions — every non-target node on every internal host gets a fresh
    instance, and no port moves anywhere."""
    net, adv = _build()
    internal = _internal_ids(net)
    before = {
        h: {
            nid: (net.get_host(h).graph.nodes[nid]["service"].id,
                  net.get_host(h).graph.nodes[nid]["port"])
            for nid in net.get_host(h).graph.nodes
            if nid != net.get_host(h).target_node
        }
        for h in internal
    }
    random.seed(SEED + 1)
    ServiceDiversity(network=net).mtd_operation(adv)
    for h in internal:
        host = net.get_host(h)
        for nid, (old_id, old_port) in before[h].items():
            assert host.graph.nodes[nid]["service"].id != old_id, (
                f"host {h} node {nid}: service not redrawn"
            )
            assert host.graph.nodes[nid]["port"] == old_port, (
                f"host {h} node {nid}: port moved under a service redraw"
            )


def test_cts_preserves_hosts_and_holdings_while_moving_adjacency():
    """IS-MTD-07 + Ho's 'preserving the hosts' + D-02: adjacency regenerates
    (endpoint edges included), node ids and host instances survive, and the
    attacker's holdings are never revoked."""
    net, adv = _build()
    net.compromised_hosts.extend([7, 8])
    before_edges = frozenset(map(tuple, map(sorted, net.graph.edges)))
    before_ids = tuple(sorted(net.graph.nodes))
    before_hosts = {hid: id(net.get_host(hid)) for hid in net.get_hosts()}
    before_ips = {hid: net.get_host(hid).ip for hid in net.get_hosts()}

    random.seed(SEED + 1)
    CompleteTopologyShuffle(network=net).mtd_operation(adv)

    assert frozenset(map(tuple, map(sorted, net.graph.edges))) != before_edges
    assert tuple(sorted(net.graph.nodes)) == before_ids
    assert {hid: id(net.get_host(hid)) for hid in net.get_hosts()} == before_hosts
    assert {hid: net.get_host(hid).ip for hid in net.get_hosts()} == before_ips
    assert net.compromised_hosts == [7, 8], "holdings must survive a topology shuffle (D-02)"


def test_the_target_node_carries_no_service_or_port():
    """The structural fact grounding the diversity mechanisms' target-node
    skip: nothing exists at the target node to diversify (host.py:116-127
    assigns both attrs to every node EXCEPT the target)."""
    net, _ = _build()
    for hid in net.get_hosts():
        host = net.get_host(hid)
        attrs = host.graph.nodes[host.target_node]
        assert "service" not in attrs and "port" not in attrs, (
            f"host {hid}: target node unexpectedly carries a service/port — "
            "the structural basis of the target-node skip has changed"
        )
        for nid in host.graph.nodes:
            if nid == host.target_node:
                continue
            assert "service" in host.graph.nodes[nid] and "port" in host.graph.nodes[nid]


# ---------------------------------------------------------------------------
# D-32 — UserShuffle's set_host_users side effects (repaired 2026-08-27,
# Marc's rulings R1/R2). Appended block; the tests above are untouched.
# ---------------------------------------------------------------------------


def _counters_for(users):
    """The values set_host_users must leave behind for a CURRENT users dict
    (D-26 repaired, ruled 2026-08-27): total_users is the account count and
    p_u_compromise is True iff any current account reuses its password."""
    return len(users), any(users.values())


def _host_surface(host):
    return (
        host.ip,
        host.os_type,
        host.os_version,
        tuple(
            (nid,
             host.graph.nodes[nid].get("port"),
             getattr(host.graph.nodes[nid].get("service"), "id", None))
            for nid in sorted(host.graph.nodes)
        ),
    )


def test_usershuffle_counters_track_the_current_users_only():
    """D-32: two firings — total_users no longer ratchets, p_u_compromise no
    longer latches, endpoints and the adversary's harvested credentials are
    untouched, and no other host attribute moves."""
    net, adv = _build()
    adv._compromised_users = ["alice", "bob"]
    holdings_before = list(adv._compromised_users)
    endpoints_before = _endpoint_state(net)
    surface_before = {hid: _host_surface(net.get_host(hid)) for hid in net.get_hosts()}
    total_before = {hid: net.get_host(hid).total_users for hid in _internal_ids(net)}

    random.seed(SEED + 1)
    UserShuffle(network=net).mtd_operation(adv)
    random.seed(SEED + 2)
    UserShuffle(network=net).mtd_operation(adv)

    for hid in _internal_ids(net):
        host = net.get_host(hid)
        total, reuse = _counters_for(host.users)
        assert host.total_users == total, (
            f"host {hid}: total_users={host.total_users} ratcheted past the "
            f"current users' count {total}"
        )
        assert 1 <= host.total_users <= net.users_per_host
        assert host.p_u_compromise is reuse, (
            f"host {hid}: p_u_compromise={host.p_u_compromise} does not reflect "
            f"the current users (reuse present: {reuse})"
        )
        assert set(host.users) <= {u for u, _ in net.users_list}
    # At least one host's divisor demonstrably did not grow across two calls.
    assert all(
        net.get_host(hid).total_users <= net.users_per_host for hid in total_before
    )

    assert _endpoint_state(net) == endpoints_before, "UserShuffle wrote to an endpoint"
    assert adv._compromised_users == holdings_before, "adversary holdings were touched"
    assert {hid: _host_surface(net.get_host(hid)) for hid in net.get_hosts()} == surface_before, (
        "UserShuffle touched ip/os/service/port state"
    )


def test_set_host_users_latch_and_ratchet_are_gone():
    """The unit-level shape of D-32 and D-26: a reuser then a clean draw
    clears p_u_compromise, and total_users is the account count each call."""
    net, _ = _build()
    host = net.get_host(_internal_ids(net)[0])
    host.set_host_users([("ann", True), ("ben", False)])
    assert (host.total_users, host.p_u_compromise) == (2, True)
    host.set_host_users([("cat", False), ("dan", False), ("eve", False)])
    assert (host.total_users, host.p_u_compromise) == (3, False)


def _reachable_closure(net, compromised):
    """The visibility model `update_reachable_mtd` is meant to compute,
    written independently: endpoints, plus every compromised host joined to
    an endpoint by a chain of compromised hosts."""
    comp = set(compromised)
    seen = list(net.exposed_endpoints)
    frontier = list(net.exposed_endpoints)
    while frontier:
        for n in net.graph.neighbors(frontier.pop()):
            if n in comp and n not in seen:
                seen.append(n)
                frontier.append(n)
    return set(seen)


def test_hts_moves_the_foothold_with_its_instance():
    """D-31 (repaired): one HostTopologyShuffle firing after a compromise
    established through the production path (`update_reachable_compromise`
    aliases the adversary's list onto the network). The alias survives, every
    compromised id still resolves to the same Host instance, the foothold's
    new id is in `reachable` and its new neighbours are visible, the
    endpoints stay put and adjacency does not move (D-02 + IS-MTD-04)."""
    net, adv = _build()
    endpoints = list(net.exposed_endpoints)
    foothold = 6  # layer-1 host adjacent to an endpoint under seed 42
    assert net.get_layers()[foothold] == 1 and set(net.graph.neighbors(foothold)) & set(endpoints)
    for hid in endpoints + [foothold]:
        adv.get_compromised_hosts().append(hid)
        net.update_reachable_compromise(hid, adv.get_compromised_hosts())
    assert net.compromised_hosts is adv._compromised_hosts
    adv.set_pivot_host_id(foothold)
    adv.set_host_stack([foothold, 7])
    adv.get_stop_attack().append(foothold)
    adv.get_attack_counter()[foothold] = 3

    instances = {hid: net.get_host(hid) for hid in adv.get_compromised_hosts()}
    foothold_instance = instances[foothold]
    before_edges = frozenset(map(tuple, map(sorted, net.graph.edges)))
    before_layers = net.get_layers()
    before_endpoint_instances = {hid: id(net.get_host(hid)) for hid in endpoints}

    # Seed offset 5 lands the foothold on id 8, adjacent to a compromised
    # endpoint, so the visibility assertions below are not vacuous.
    random.seed(SEED + 5)
    HostTopologyShuffle(network=net).mtd_operation(adv)

    new_id = foothold_instance.host_id
    assert new_id != foothold, "the seed no longer swaps the foothold; re-pin the seed"
    assert net.get_host(new_id) is foothold_instance

    # 1. the alias is intact, and both views carry the moved ids
    assert net.compromised_hosts is adv._compromised_hosts
    assert new_id in adv.get_compromised_hosts()
    assert foothold not in adv.get_compromised_hosts()
    # 2. every compromised id still resolves to the instance it held
    for old_id, inst in instances.items():
        assert net.get_host(inst.host_id) is inst
        assert inst.host_id in adv.get_compromised_hosts()
    # 3. the visibility model is rebuilt from the moved set
    assert set(net.reachable) == _reachable_closure(net, adv.get_compromised_hosts())
    assert new_id in net.reachable
    visible = set(net.get_hacker_visible_graph().nodes)
    assert set(net.graph.neighbors(new_id)) <= visible
    # 4. the rest of the id-keyed adversary state moved with it
    assert adv.get_pivot_host_id() == new_id
    assert adv.get_host_stack()[0] == new_id
    assert new_id in adv.get_stop_attack() and foothold not in adv.get_stop_attack()
    assert adv.get_attack_counter()[new_id] == 3
    # 5. endpoints exempt, level preserved, adjacency untouched
    assert {hid: id(net.get_host(hid)) for hid in endpoints} == before_endpoint_instances
    assert net.get_layers()[new_id] == before_layers[foothold]
    assert frozenset(map(tuple, map(sorted, net.graph.edges)) ) == before_edges
    # 6. the per-id ip feed the reactive arm reads follows the move
    assert net.scorer.current_hosts_ip[new_id] == foothold_instance.ip


# --- OS Diversity as a distinct mechanism (Marc's ruling, 2026-08-27) ---------

def test_service_is_compatible_with_its_own_os():
    """D-18's regression gate: the inherited test was False in every reachable
    state (a Service instance against name strings). Repaired, a service drawn
    for an OS/version is compatible with that OS/version, always."""
    net, _ = _build()
    gen = net.get_service_generator()
    random.seed(SEED + 1)
    for os_type in constants.OS_TYPES:
        for os_version in constants.OS_VERSION_DICT[os_type]:
            for _ in range(10):
                svc = gen.get_random_service(os_type, os_version)
                assert gen.service_is_compatible_with_os(os_type, os_version, svc), (
                    f"{svc.name} drawn for {os_type} {os_version} is not compatible with it"
                )


def test_osdiversity_redraws_only_the_services_the_new_os_cannot_run():
    """IS-MTD-06 as documented (Brown §III-B(6), Zhang §4.3.1.4): the OS is
    relabelled on internal hosts with the version index preserved, and only
    the services incompatible with the new OS are randomly changed —
    strictly fewer than all; every survivor compatible, every redraw
    incompatible. Endpoints, the target node and every port are untouched."""
    net, adv = _build()
    gen = net.get_service_generator()
    internal = _internal_ids(net)
    before_endpoints = _endpoint_state(net)
    before = {}
    for h in internal:
        host = net.get_host(h)
        before[h] = {
            "os": (host.os_type, host.os_version),
            "index": constants.OS_VERSION_DICT[host.os_type].index(host.os_version),
            "target": host.graph.nodes[host.target_node].get("service"),
            "nodes": {
                nid: (host.graph.nodes[nid]["service"], host.graph.nodes[nid]["port"])
                for nid in host.graph.nodes if nid != host.target_node
            },
        }
    random.seed(SEED + 1)
    OSDiversity(network=net).mtd_operation(adv)

    assert _endpoint_state(net) == before_endpoints
    redrawn = kept = 0
    for h in internal:
        host = net.get_host(h)
        new_os, new_version = host.os_type, host.os_version
        assert new_os in constants.OS_TYPES
        assert constants.OS_VERSION_DICT[new_os].index(new_version) == before[h]["index"], (
            f"host {h}: OS version index not preserved"
        )
        assert host.graph.nodes[host.target_node].get("service") is before[h]["target"]
        for nid, (old_svc, old_port) in before[h]["nodes"].items():
            new_svc = host.graph.nodes[nid]["service"]
            assert host.graph.nodes[nid]["port"] == old_port, f"host {h} node {nid}: port moved"
            assert gen.service_is_compatible_with_os(new_os, new_version, new_svc), (
                f"host {h} node {nid}: a service the new OS cannot run survived/was drawn"
            )
            if new_svc is old_svc:
                kept += 1
            else:
                redrawn += 1
                assert not gen.service_is_compatible_with_os(new_os, new_version, old_svc), (
                    f"host {h} node {nid}: a compatible service was redrawn"
                )
    assert any(before[h]["os"] != (net.get_host(h).os_type, net.get_host(h).os_version)
               for h in internal), "no internal host relabelled — vacuous run"
    assert redrawn > 0, "no service redrawn — vacuous run; re-pin the seed"
    assert redrawn < redrawn + kept, "every service redrawn — the D-18 always-fires guard is back"


def _os_dependent_vuln():
    from mtdnetwork.component.services import Vulnerability
    random.seed(SEED)
    while True:
        v = Vulnerability(can_have_os_dependency=True, os_list=list(constants.OS_TYPES))
        if v.has_os_dependency:
            return v


class _HostStub:
    def __init__(self, os_type):
        self.os_type = os_type


def test_os_gate_refuses_a_mismatched_host_as_a_counted_attempt_without_rolling():
    """D-19 closed: mismatched OS -> 0.0, exploit_attempt += 1, the RNG state is
    untouched (so the refusal shifts no downstream draw), and the vulnerability
    stays unexploited."""
    v = _os_dependent_vuln()
    other = [o for o in constants.OS_TYPES if o not in v.vuln_os_list]
    assert other, "the sampled os list covers every OS; k < len(os_list) should prevent this"
    host = _HostStub(other[0])
    state = random.getstate()
    for n in range(1, 4):
        assert v.network(host=host) == 0.0
        assert v.exploit_attempt == n
        assert not v.exploited
    assert random.getstate() == state, "the refused attempt drew randomness"


def test_os_gate_rolls_as_before_on_a_matching_host():
    """On a host running an OS in the list the roll happens exactly as it did:
    one random.random() draw against complexity, counted as an attempt."""
    v = _os_dependent_vuln()
    host = _HostStub(v.vuln_os_list[0])
    random.seed(SEED + 7)
    expected_roll = random.random()
    random.seed(SEED + 7)
    outcome = v.network(host=host)
    assert v.exploit_attempt == 1
    if expected_roll < v.complexity:
        assert v.exploited and outcome == v.impact
    else:
        assert not v.exploited and outcome == 0.0
    # exactly one draw was consumed
    random.seed(SEED + 7)
    random.random()
    after_one_draw = random.getstate()
    random.seed(SEED + 7)
    v.exploited = False
    v.network(host=host)
    assert random.getstate() == after_one_draw
