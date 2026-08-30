"""The targeted objective — Brown's Scenario 2 on the movement attacker.

Brown 2023 §III-C(1) (intent spec IS-SCN-03 / B-ATK-02) gives the targeted
attacker one rule the general attacker lacks: **host priority toward the
target**. If the target is visible, attack only it; otherwise prefer hosts on
the target's layer; otherwise hosts on other layers, nearer the target's layer
first. Everything else (the six verbs, RoA exploit ordering, credential reuse,
C2 pivoting) is shared by design (IS-SCN-01).

This module holds the *policy*. The *seam* is one attribute on the shared
ENUM_HOST core, ``AttackOperation.host_sorter`` (decision A, Marc 2026-08-30;
``docs/handoffs/2026-08-30_targeted_attacker_build.md`` §1.2): the core sorts
the visible queue through the sorter when one is installed and through the
inherited distance sort otherwise, so the general arm is byte-identical by
construction and every pop path — ``step("ENUM_HOST")``, the fresh-host
retry-until-fresh loop, and the native FSM wrapper — obeys the same rule.

No time-domain spec exists for the targeted scenario (IS-SCN-06); this is an
**extension**, recorded as such.
"""

from __future__ import annotations

import random
from typing import Any

#: The attack objectives the attack model accepts (Brown 2023 §III-C(1)).
ATTACK_OBJECTIVES: tuple[str, ...] = ("general", "targeted")


def choose_target_hosts(
    network: Any, *, target_layer: int | None, seed: int
) -> tuple[frozenset[int], int]:
    """Resolve the target set on the seam, never in ``gen_graph``.

    ``target_layer=None`` → the database (crown-jewel) set,
    ``network.get_database()``, on whatever layer it sits (the deepest on the
    shipped geometry) — the set the targeted-objective probe already measures,
    so every existing reach number stays comparable. An ``int`` → **one** host
    drawn uniformly from that layer with a dedicated stream derived from the
    run seed (never the substrate's global stream, so construction and the
    general arm's draws are untouched). This is Brown's ``TX`` sweep.

    Returns ``(target_hosts, resolved_layer)``; the layer is what the priority
    key measures distance to. Keyed on ``get_layers()``, never the ``db`` tag
    (targeted_objective_probe.md §10.1).
    """
    layers = network.get_layers()
    if target_layer is None:
        hosts = frozenset(int(h) for h in network.get_database())
        if not hosts:
            raise ValueError("the network declares no database hosts to target")
        resolved = max(layers[h] for h in hosts)
        return hosts, int(resolved)
    candidates = sorted(h for h, layer in layers.items() if layer == target_layer)
    if not candidates:
        raise ValueError(
            f"target_layer={target_layer} has no hosts on this geometry "
            f"(layers present: {sorted(set(layers.values()))})"
        )
    rng = random.Random(f"target:{seed}")
    return frozenset({int(rng.choice(candidates))}), int(target_layer)


class TargetedSorter:
    """Brown's priority-then-distance host order, as the core's ``host_sorter``.

    Runs the inherited distance sort **first** over the whole visible queue
    (so the tiebreak draws exactly as many ``random.random()`` values as the
    general arm would — the D-29 shared-stream discipline is unchanged), then
    stable-sorts by priority class, so within a class the order is the general
    attacker's nearest-from-foothold order. Class 0 is the target itself
    (Brown's "attack only the target if found" falls out of it sorting first),
    class 1 the target's layer, class ``d + 1`` a layer ``d`` away.
    """

    def __init__(self, network: Any, target_hosts: frozenset[int], target_layer: int) -> None:
        self.network = network
        self.target_hosts = frozenset(target_hosts)
        self.target_layer = int(target_layer)
        self._layers = dict(network.get_layers())

    def priority(self, host_id: int) -> int:
        if host_id in self.target_hosts:
            return 0
        layer = self._layers.get(host_id)
        if layer is None:  # a host the layer map does not know: last
            return len(set(self._layers.values())) + 1
        return abs(int(layer) - self.target_layer) + 1

    def __call__(self, host_stack, compromised_hosts, pivot_host_id: int = -1):
        by_distance = self.network.sort_by_distance_from_exposed_and_pivot_host(
            host_stack, compromised_hosts, pivot_host_id=pivot_host_id
        )
        return sorted(by_distance, key=self.priority)  # stable: distance order kept within class
