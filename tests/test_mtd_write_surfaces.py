"""Regression tests for the defender write side — the mechanisms' write
surfaces as dispositioned by boundary review 2 (Part B, 2026-08-03).

Each test pins behaviour that is either documented lineage intent or carries
a written ruling from Marc; the enumeration and live diffs behind them are
`docs/implementation/mtd_write_surfaces.md`, and the rulings are the audit's
boundary-review-2 disposition banner (D-23..D-25).

What is deliberately NOT pinned, and why:

- OS Diversity's service-replacement selectivity (all vs incompatible-only) —
  that is D-18, open and owned by the indistinguishability brief; pinning it
  in either direction would freeze an unclassified divergence.
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


def test_usershuffle_keeps_not_exempting_the_endpoints():
    """The D-23 contrast: IS-MTD-03 says "each host", and UserShuffle
    conforms — endpoint users move too."""
    net, adv = _build()
    before = {
        hid: tuple(sorted(net.get_host(hid).users.keys()))
        for hid in net.exposed_endpoints
    }
    random.seed(SEED + 1)
    UserShuffle(network=net).mtd_operation(adv)
    assert any(
        tuple(sorted(net.get_host(hid).users.keys())) != before[hid]
        for hid in net.exposed_endpoints
    ), "UserShuffle exempted the endpoints — IS-MTD-03's 'each host' no longer holds"


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
