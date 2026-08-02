"""The iterated attacker utility model — the axis-6 decision model repaired so it
can express **instrumental value**.

The shipped model (:mod:`~mtdsim.l3_simulation.movement.utility`) prices a
candidate tactic by its declared duration and values it by its proximity to the
profile's objective. Both terms penalise an *enabling* tactic, and in the same
direction, so the penalty compounds: reconnaissance is the slowest declared tier
(35.0 s against the exploit-shaped 4.5 s) **and** the furthest from any
objective, giving ``pure_steal`` a 31-fold preference against the very tactic
that satisfies the precondition for the tactic it prefers. Neither term has a
place in which "worth its price because of what it unlocks" could be written, so
no setting of ρ, ``cost_floor_s`` or λ repairs it — the defect is the model's,
not the values'. Diagnosis: ``cost_model_plain.md`` §2.2a.

Two changes, each derived from artefacts already on disk. **No second catalogue
and no new declared magnitude**: ρ, ``cost_floor_s`` and λ keep their declared
values and their swept bands; what changes is what they are applied to.

**Change A — cost becomes expected cost, conditioned on readiness.**

    cost*(b | s)  =  duration(b)  +  enabling_cost(verb(b), s)

``enabling_cost`` is a shortest-path search over the **capability closure** of
the declared precondition relation (``precondition_relation.json``, the same
artefact the readiness learner consults): the cheapest ordered verb sequence
taking the attacker's currently-held capabilities to a set satisfying
``requires[verb(b)]``, each verb priced by the cheapest tactic that dispatches it
under the run's controller mapping. It is a search rather than a sum because the
relation has ordering effects — ``ENUM_HOST`` *clears* ``curr_ports`` while
producing ``curr_host``, so an unordered set of missing prerequisites cannot be
costed. Three boolean capabilities make the state space eight states, so the
search is exhaustive and exact.

Two properties earn this form. It **prices the wall instead of walking into it**
— an exploit-shaped tactic attempted unready costs its 4.5 s *plus* the
reconnaissance it needs, and returns to 4.5 s the moment the prerequisite is
met. And it **responds to MTD in a way declared duration structurally cannot**:
the relation's ``mtd_clears`` field declares that a *network*-layer mutation
destroys ``curr_host`` and ``curr_ports`` while an *application*-layer one
destroys nothing, so after a position-destroying mutation the enabling chain
must be re-walked and ``cost*`` rises — by an amount set by which capabilities
were lost, not by the interrupted tactic's dwell. That is a non-proportional
response, which is the one thing a normalised ratio over declared durations
cannot see (``incentive_rationality.md`` §6.3).

**What change A gives up, deliberately.** The modulator stops being a pure
function of declared data and the current place, so the precomputable-factor-table
property (F6 of the fidelity ledger, proven 30/30 bit-identical by the collapse
spike) is surrendered. That property is what F6 uses to argue the mechanism is
"structurally a third static overlay"; surrendering it *is* the point, because a
factor that cannot see attacker state cannot see MTD either.

**Change B — benefit becomes enabling value.** The numerator's stage-gap term is
replaced by distance measured **through the profile's own routing net** rather
than through the lifecycle-stage ordering:

    benefit*(b | P)  =  1.0 at an objective of P; else rho^(1 + hops(b -> nearest
                        objective of P, along P's net))

``hops`` is the shortest directed path in the routing net the profile already
carries. Reconnaissance that genuinely leads to the objective now scores as near
to it; reconnaissance in a profile where it leads nowhere still does not. The
change is *which graph the distance is measured in*, and nothing is declared.

**The fallback, which is load-bearing rather than defensive.** Every profile has
at least one tactic with no directed net path to its objective (``impact`` under
``pure_steal``, ``credential-access`` under ``double_extortion``,
``defense-impairment`` under ``infrastructure_setup``), and the benefit table is
complete over all 75 cells including tactics a profile's net has no place for at
all. Those cells take **the current stage-gap value**, never zero — a zero would
make this a ``may_zero`` modulator under the seam's stall rule and would need the
no-stall check re-run.

**λ = 0 stays exactly bit-identical.** Only the ratio's value changes; the factor
is still raised to λ, and ``x ** 0.0`` is exactly 1.0 in IEEE arithmetic for any
finite positive ``x``. As in the shipped model the implementation deliberately
does **not** special-case zero: the identity is a property of the maths, and
testing it that way is a stronger claim than short-circuiting it.

**Composition hazard.** Change A conditions on readiness, and so does the axis-7
readiness learner — against the same artefact. Composing both would apply one
signal twice through two factors. No arm may run this modulator's expected-cost
form together with :class:`ReadinessLearningModulator` until the joint check has
re-run; the register entry is ``modulator_composition.md`` factor 7.

Design record: ``docs/implementation/pipeline/ogasp/iterated_cost_model.md``.
The model this iterates: ``incentive_rationality.md`` / ``cost_model_plain.md``.
"""
from __future__ import annotations

import heapq
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from mtdsim.l3_simulation.movement.learning_readiness import (
    PRECONDITION_PATH,
    PreconditionModel,
    load_tactic_to_verb,
)
from mtdsim.l3_simulation.movement.net import load_routing_net
from mtdsim.l3_simulation.movement.utility import (
    UtilityCompileError,
    UtilityRules,
    load_utility_rules,
    stage_gap,
)

#: The three arms the sweep separates. ``declared`` is the shipped model, kept
#: reachable through this module so an experiment can run all four arms through
#: one construction path; A, B and AB are the changes above.
ARMS: tuple[str, ...] = ("declared", "A", "B", "AB")


# --- change A: the expected-cost term ---------------------------------------


@dataclass(frozen=True)
class CapabilityCostModel:
    """The cheapest ordered verb sequence from a held capability set to one that
    satisfies a verb's requirement, priced from the declared duration catalogue.

    ``verb_cost`` maps each verb **some tactic dispatches under this run's
    mapping** to the cheapest such tactic's floored declared duration. A verb no
    tactic dispatches is not an available enabling step, which is a property of
    the mapping and not of this model.

    The floor is applied here for the same reason the shipped model applies it to
    the divisor: ``resource-development`` is declared 0.0 s because its real
    effort happens off the simulator's clock, **not** because it is free, and an
    enabling chain that charged it nothing would say the opposite.
    """

    verb_cost: Mapping[str, float]
    model: PreconditionModel

    @classmethod
    def build(
        cls,
        *,
        tactic_to_verb: Mapping[str, str | None],
        cost: Mapping[str, float],
        cost_floor_s: float,
        model: PreconditionModel | None = None,
    ) -> "CapabilityCostModel":
        model = model or PreconditionModel.load()
        verb_cost: dict[str, float] = {}
        for tactic, verb in tactic_to_verb.items():
            if verb is None:
                continue
            if verb not in model.requires:
                raise UtilityCompileError(
                    f"mapping dispatches {verb!r} for {tactic!r}, which the declared "
                    "precondition relation does not describe; the enabling chain "
                    "cannot be priced against a relation that omits the verb"
                )
            priced = max(float(cost.get(tactic, 0.0)), float(cost_floor_s))
            if verb not in verb_cost or priced < verb_cost[verb]:
                verb_cost[verb] = priced
        return cls(verb_cost=verb_cost, model=model)

    @property
    def unreachable_cost(self) -> float:
        """The charge for a verb whose requirement no available sequence can
        establish — the sum of every available verb's price.

        It is a finite upper bound **derived** from the catalogue and the mapping
        rather than a declared magnitude, and it is chosen over infinity because
        an infinite cost drives the utility to zero, which would make this a
        ``may_zero`` modulator under the seam's stall rule. On both shipped
        mappings the closure is fully connected and this value is never charged;
        the test suite asserts that rather than assuming it.
        """
        return sum(self.verb_cost.values())

    def enabling_cost(self, verb: str | None, held: frozenset[str] | set[str]) -> float:
        """The cheapest ordered verb sequence taking ``held`` to a capability set
        satisfying ``requires[verb]``. Zero when the attacker is already ready,
        and zero for a dwell-only place (``verb is None``), which has no
        precondition to satisfy.

        Dijkstra over the capability closure: a state is a frozenset of held
        capabilities, and applying an available verb whose own requirement the
        state meets moves to ``(state | produces) - clears`` at that verb's
        price. Exhaustive — three boolean capabilities give eight states.
        """
        if verb is None:
            return 0.0
        try:
            needed = self.model.requires[verb]
        except KeyError as exc:
            raise UtilityCompileError(
                f"no declared requirement for verb {verb!r}"
            ) from exc
        start = frozenset(held)
        if needed <= start:
            return 0.0

        best: dict[frozenset[str], float] = {start: 0.0}
        queue: list[tuple[float, int, frozenset[str]]] = [(0.0, 0, start)]
        tie = 0
        while queue:
            spent, _, state = heapq.heappop(queue)
            if spent > best.get(state, float("inf")):
                continue
            if needed <= state:
                return spent
            for step, price in self.verb_cost.items():
                if not self.model.requires[step] <= state:
                    continue
                nxt = (state | self.model.produces[step]) - self.model.clears[step]
                cand = spent + price
                if cand < best.get(nxt, float("inf")):
                    best[nxt] = cand
                    tie += 1
                    heapq.heappush(queue, (cand, tie, nxt))
        return self.unreachable_cost


# --- change B: the enabling-value benefit -----------------------------------


def net_hops(profile: str, objectives: tuple[str, ...]) -> dict[str, int]:
    """``place -> shortest directed hop count to the nearest objective`` in the
    profile's own routing net. Places with no directed path are absent from the
    result, as are tactics the profile's net has no place for at all — both take
    the stage-gap fallback in :func:`benefit_values_net`.

    Computed by breadth-first search on the reversed net from the objective set,
    which is the same shortest-path question asked once rather than per place.
    """
    net = load_routing_net(profile)
    seats = [o for o in objectives if o in net.places]
    if not seats:
        return {}
    reverse: dict[str, set[str]] = {}
    for src in net.places:
        for dst in net.base_out_weights(src):
            reverse.setdefault(dst, set()).add(src)
    hops = {seat: 0 for seat in seats}
    queue = deque(seats)
    while queue:
        here = queue.popleft()
        for prior in sorted(reverse.get(here, ())):
            if prior not in hops:
                hops[prior] = hops[here] + 1
                queue.append(prior)
    return hops


def benefit_values_net(
    rules: UtilityRules, rho: float | None = None
) -> dict[str, dict[str, float]]:
    """The complete ``profile -> tactic -> benefit*`` table under change B.

    Identical in shape and coverage to the shipped compiler's 75-cell table, and
    identical in rule at the objective (1.0 — value accrues *at* the objective).
    Only the instrumental distance changes graph: lifecycle-stage separation
    becomes net hop count. A cell whose tactic has no directed net path to the
    profile's objective — including a tactic the profile's net has no place for —
    keeps the shipped stage-gap value, never zero.
    """
    rho = rules.model.rho if rho is None else float(rho)
    table: dict[str, dict[str, float]] = {}
    for profile in rules.profiles:
        objectives = rules.objectives[profile]
        hops = net_hops(profile, objectives)
        cells: dict[str, float] = {}
        for tactic in rules.tactics:
            if tactic in objectives:
                cells[tactic] = 1.0
                continue
            gap = hops.get(tactic)
            if gap is None:  # no path through the net — the declared fallback
                gap = stage_gap(tactic, profile, rules)
            cells[tactic] = rho ** (1 + gap)
        table[profile] = cells
    return table


# --- the modulator ----------------------------------------------------------


class IteratedUtilityModulator:
    """The repaired axis-6 routing factor — ``(u*(b | s) / ū*)^λ``.

    Selectable by arm, so the shipped model stays runnable through the same
    construction path (every recorded figure in the project was produced by it,
    and the comparison arms need it):

    - ``declared`` — the shipped model. Declared duration, stage-gap benefit,
      stateless. Reproduces :class:`~...utility.UtilityModulator` exactly.
    - ``A`` — expected cost, stage-gap benefit.
    - ``B`` — declared duration, enabling-value benefit. Stateless.
    - ``AB`` — both.

    ``may_zero`` is deliberately absent for the same reason it is in the shipped
    model, and the reason survives both changes: benefit is strictly positive
    (``rho^(1+gap)`` with ``0 < rho < 1``, or 1.0 at an objective, with the
    unreachable fallback taking a stage-gap value rather than zero) and cost is a
    sum of a floored duration and a non-negative enabling charge, so utility is
    strictly positive and no factor can reach zero. The seam's stall rule is
    never engaged and the no-stall check needs no re-run.

    **Statefulness (arms A and AB only).** The modulator tracks the attacker's
    held capabilities from its own trajectory against the declared relation,
    reading no substrate state — the identical derivation the readiness learner
    uses, so the axis-8 scheme-awareness exclusion is untouched. It estimates
    nothing and updates no belief; ``cost*`` is a pure function of the declared
    relation, the declared mapping, the declared catalogue and where the attacker
    stands. Determinism (SIM-05) is intact: no random stream is drawn from.
    """

    name = "utility-iterated"

    def __init__(
        self,
        *,
        profile: str,
        arm: str,
        benefit: Mapping[str, float],
        cost: Mapping[str, float],
        lam: float,
        cost_floor_s: float,
        capability_cost: CapabilityCostModel | None = None,
        tactic_to_verb: Mapping[str, str | None] | None = None,
    ) -> None:
        if arm not in ARMS:
            raise ValueError(f"unknown arm {arm!r}; expected one of {ARMS}")
        if cost_floor_s <= 0.0:
            raise ValueError(
                f"cost_floor_s must be positive (got {cost_floor_s!r}); the floor "
                "exists precisely so the utility ratio cannot divide by the "
                "off-clock tactic's declared zero"
            )
        self.profile = profile
        self.arm = arm
        self.benefit = dict(benefit)
        self.cost = dict(cost)
        self.lam = float(lam)
        self.cost_floor_s = float(cost_floor_s)
        self.expected_cost = arm in ("A", "AB")
        self.capability_cost = capability_cost
        self.tactic_to_verb = dict(tactic_to_verb or {})
        if self.expected_cost and capability_cost is None:
            raise ValueError(
                "arms A and AB price the enabling chain and need a "
                "CapabilityCostModel; construct via iterated_utility_modulator_for"
            )
        #: The phase-state: the capabilities the attacker currently holds. Empty
        #: at the start of a run — the token has established nothing yet. Tracked
        #: for every arm so a log or a snapshot reads the same whichever arm ran;
        #: only the expected-cost arms consult it.
        self.held: set[str] = set()
        self._pending_ready: bool | None = None

    # -- observation (the state fans these in; inert for the stateless arms) --
    def observe_visit(self, place: str) -> None:
        """The token has entered ``place`` and is about to act. Record whether
        its verb would run in the capability state held *before* this place's own
        effect — the same bit the routing decision that arrived here used."""
        if self.capability_cost is None:
            return
        verb = self.tactic_to_verb.get(place)
        self._pending_ready = self.capability_cost.model.is_ready(verb, self.held)

    def observe_verdict(self, place: str, verdict: str) -> None:
        """The verb has now run; apply its capability effect so the routing
        decision that follows sees the state the attacker actually stands in.

        Gated on readiness for the reason the readiness learner gates it: a
        dispatch whose precondition was unmet is blocked by the substrate and
        produces nothing. ``verdict`` is unused — a verb that *ran* establishes
        its capability whether the substrate then ruled the action a success or a
        failure, and the relation models the run, not the outcome.
        """
        if self.capability_cost is None:
            return
        verb = self.tactic_to_verb.get(place)
        ready = (
            self._pending_ready
            if self._pending_ready is not None
            else self.capability_cost.model.is_ready(verb, self.held)
        )
        if verb is not None and ready:
            self.held |= self.capability_cost.model.produces[verb]
            self.held -= self.capability_cost.model.clears[verb]
        self._pending_ready = None

    def observe_mtd_interrupt(self, resource_type: str = "") -> None:
        """The defence severs the capabilities the declared relation says it
        severs — a network-layer mutation destroys the host cursor and the port
        knowledge, an application-layer one destroys nothing structural. This is
        the whole of the channel by which MTD reaches the cost term, and it is
        why the response is expected to be layer-specific rather than uniform.
        """
        if self.capability_cost is None:
            return
        self.held -= self.capability_cost.model.mtd_clears.get(
            resource_type, frozenset()
        )

    # -- the utility ---------------------------------------------------------
    def cost_of(self, tactic: str) -> float:
        """``max(duration, cost_floor_s)`` under the declared arms; that plus the
        enabling chain's price from where the attacker currently stands under the
        expected-cost arms."""
        base = max(self.cost.get(tactic, 0.0), self.cost_floor_s)
        if not self.expected_cost:
            return base
        assert self.capability_cost is not None  # constructor guarantees it
        verb = self.tactic_to_verb.get(tactic)
        return base + self.capability_cost.enabling_cost(verb, self.held)

    def utility(self, tactic: str) -> float:
        """The attacker's declared payoff per unit of *expected* cost for
        arriving at ``tactic`` from where it currently stands."""
        try:
            benefit = self.benefit[tactic]
        except KeyError as exc:
            raise UtilityCompileError(
                f"no declared benefit for {tactic!r} under profile "
                f"{self.profile!r}; the benefit table is complete over the "
                "place-union, so this is a net/table disagreement"
            ) from exc
        return benefit / self.cost_of(tactic)

    def factors(
        self, state: Any, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        """Per-destination ``(u*(b) / ū*)^λ`` over the source's out-set.

        Normalising by the out-set's mean before exponentiating keeps λ scaling a
        *ratio* rather than an absolute magnitude, exactly as in the shipped
        model — and it matters more here, because the expected-cost arms move the
        absolute scale of the denominator around as the attacker's position
        changes. The normalisation is behaviourally free (the composition
        renormalises afterwards) and is there for the parameter's meaning and the
        log's legibility.
        """
        if not base_out_weights:
            return {}
        utilities = {dst: self.utility(dst) for dst in base_out_weights}
        mean = sum(utilities.values()) / len(utilities)
        if mean <= 0.0:  # unreachable by construction; refuse rather than divide
            raise UtilityCompileError(
                f"non-positive mean utility over the out-set of {src!r} — benefit "
                "is strictly positive and cost is floored, so this cannot happen "
                "unless the declared table was corrupted"
            )
        return {dst: (u / mean) ** self.lam for dst, u in utilities.items()}

    def snapshot(self) -> dict[str, Any]:
        """A compact view for narration and experiment logs."""
        return {
            "arm": self.arm,
            "lambda": self.lam,
            "expected_cost": self.expected_cost,
            "held": sorted(self.held),
        }


def iterated_utility_modulator_for(
    profile: str,
    *,
    arm: str = "AB",
    mapping_version: str | None = None,
    lam: float | None = None,
    rho: float | None = None,
    cost_floor_s: float | None = None,
    rules: UtilityRules | None = None,
    precondition_path: Path | str = PRECONDITION_PATH,
) -> IteratedUtilityModulator:
    """The iterated modulator for one profile and arm, from the tracked artefacts.

    Every parameter defaults to its declared value and each is overridable so the
    sweep can move one at a time. ``mapping_version`` names the controller mapping
    the enabling chain is priced against — the expected-cost term is a property of
    the mapping as much as of the catalogue, since which tactic dispatches
    ``SCAN_PORT`` decides what a port scan costs.
    """
    from mtdsim.l3_simulation.movement.utility import benefit_values, load_benefit

    rules = rules if rules is not None else load_utility_rules()
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}; expected one of {ARMS}")

    if arm in ("B", "AB"):
        benefit = benefit_values_net(rules, rho)[profile]
    else:
        benefit = (load_benefit() if rho is None else benefit_values(rules, rho))[profile]

    floor = rules.model.cost_floor_s if cost_floor_s is None else float(cost_floor_s)
    tactic_to_verb = load_tactic_to_verb(mapping_version)
    capability_cost = (
        CapabilityCostModel.build(
            tactic_to_verb=tactic_to_verb,
            cost=rules.cost,
            cost_floor_s=floor,
            model=PreconditionModel.load(precondition_path),
        )
        if arm in ("A", "AB")
        else None
    )
    return IteratedUtilityModulator(
        profile=profile,
        arm=arm,
        benefit=benefit,
        cost=rules.cost,
        lam=rules.model.lam if lam is None else float(lam),
        cost_floor_s=floor,
        capability_cost=capability_cost,
        tactic_to_verb=tactic_to_verb,
    )


__all__ = [
    "ARMS",
    "CapabilityCostModel",
    "IteratedUtilityModulator",
    "benefit_values_net",
    "iterated_utility_modulator_for",
    "net_hops",
]
