"""The within-run attacker state and the generalised modulator composition.

This is the one shared foundation the smart-attacker axes (stealth, incentive,
learning — criterion axes 5–7) all need: a **movement-layer-only** mutable
memory of the run so far, and a third factor in the routing composition that
conditions on it. It is built so that its **null configuration is bit-identical
to a run without it** — no modulators registered means every factor is 1.0,
the product is 1, and the arithmetic reduces exactly to the current rule:

    w'(a→b)  ∝  base(a→b) · overlay_v(a→b) · Π_m  m(a→b | state)

renormalised over the source's out-set, exactly as ``OutcomeOverlay.compose``
already does. Multiplicative, never additive — the same argument the overlay
design made and won (``success_failure_overlay_design.md`` §1): conditioning
the grounded proportions without inventing a magnitude or inverting the
corpus's within-class ordering.

**How the state observes without the driver knowing.** The walk consumes two
structural Protocols — ``TimingSource.draw`` fires once per place visit (before
the verb/dwell-only branch), and ``OutcomeOverlayLike.compose`` fires once per
routing decision, after the verdict. Together they see the whole trajectory, in
causal order (visit first, verdict second). So the state is attached by
**wrapping those collaborators**, exactly as the trace tool's recording proxies
do — :class:`StatefulTiming` and :class:`ModulatedOverlay` delegate everything
and only observe, and the driver is not edited at all.

A **third** observation exists for the same reason and by the same idiom:
:class:`StatefulAttackOperation` wraps the substrate attack operation and
reports every MTD interrupt the attacker absorbs, because the routing seams
cannot see one — an interrupt reaches ``compose`` already flattened into an
ordinary failure verdict, indistinguishable from an unmet precondition. It
hooks ``apply_mtd_interrupt_cost``, which is the single call every interrupt
path in the driver funnels through, and it fires *before* the substrate serves
the penalty and therefore before the routing decision that follows. This is
what lets a modulator model MTD destroying accumulated knowledge (axis 7's
forgetting rule) rather than merely costing time.

**Modulators may observe too.** A modulator that needs its own view of the run
— decayed counts, a cost ledger, a tempo history — declares any of
``observe_visit`` / ``observe_verdict`` / ``observe_mtd_interrupt`` and the
state fans its own observations out to it. The state's counters stay a faithful
raw log of what happened; a modulator that transforms them (by decaying them,
say) keeps its transformed copy, so the record of the run and the modulator's
belief about it never get confused for one another.

**What lives here and what does not.** :class:`AttackerState` holds within-run
knowledge (visit counts, verdict counts, the ordered history) and has no
opinions about what the knowledge means. Stealth, learning and utility are
**modulators** registered on it, each owned by its own axis handoff with its
own declared parameters — nothing in this module declares a value. The one
modulator defined here, :class:`RevisitAversionDemo`, is deliberately
artificial: it exists to prove the seam live, never to model anything.

**Determinism (SIM-05).** A modulator needing randomness draws from the
state's own stream — a **fourth** stream, seeded by the same pure-XOR pattern
as the timing stream (``derive_timing_seed``), so it neither reads nor
advances the token sampler, the dwell stream, or the substrate's global dice.
Prefer modulators that are deterministic functions of the run's own history,
which need no stream at all.

**The zero rule.** A modulator factor of zero removes an out-edge, and zeroing
an out-set is the one way to manufacture a stall — currently representable but
unobserved (``weight_sensitivity_study.md`` §3). So a factor of zero is
**refused loudly** unless the modulator declares ``may_zero = True``, and any
modulator that declares it owes a declared rule and a re-run of the no-stall
check across its parameter space.

Design record: ``docs/implementation/pipeline/ogasp/attacker_state_seam.md``.
"""
from __future__ import annotations

import random
from typing import Any, Mapping, Protocol

from mtdsim.l3_simulation.movement.timing import TimingSource

# The run seed is XOR-ed with this constant to seed the state's stream — the
# fourth stream, by the same pattern (and for the same reasons) as the timing
# stream's ``TIMING_STREAM_XOR``: a bijection with no fixed point, fixed rather
# than derived so a seed reproduces forever. The constant is ASCII "STAT".
STATE_STREAM_XOR = 0x53544154


def derive_state_seed(seed: int) -> int:
    """The run seed's state-stream counterpart — pure, so a run is reproducible."""
    return int(seed) ^ STATE_STREAM_XOR


class Modulator(Protocol):
    """One state-conditioned factor in the routing composition.

    ``factors`` returns a per-destination multiplier for the routing decision
    at ``src``; a destination it does not name multiplies by 1.0. Its **null
    configuration must return 1.0 everywhere** — that is what keeps each axis
    independently ablatable and the composed run bit-identical to today when
    nothing is registered. A modulator that can return 0.0 must set
    ``may_zero = True`` and carry the declared rule that licenses it.

    The three ``observe_*`` methods are **optional**: declare one and the state
    forwards its own observations to it (module docstring). A modulator that
    reads ``state`` directly inside ``factors`` needs none of them.
    """

    name: str

    def factors(
        self, state: "AttackerState", src: str, base_out_weights: Mapping[str, float]
    ) -> Mapping[str, float]: ...


class AttackerState:
    """The movement attacker's within-run memory — one plain object per run.

    Holds what was tried and how it went, with no opinions about what the
    knowledge means: ``observe_visit`` is called on every place entry (via
    :class:`StatefulTiming`), ``observe_verdict`` on every routing decision
    (via :class:`ModulatedOverlay` — including a dwell-only place's
    distinguished ``"none"`` verdict), and ``modulate`` turns the registered
    modulators' factors into one per-destination multiplier.

    Everything is within-run: constructed per run, seeded from the run seed,
    discarded with it. Cross-run memory is a different claim (M8d) and does
    not live here.
    """

    def __init__(self, *, seed: int = 0, modulators: tuple[Modulator, ...] = ()) -> None:
        self.modulators: tuple[Modulator, ...] = tuple(modulators)
        #: The state's own random stream (SIM-05, fourth stream). Present even
        #: with no modulators — constructing it draws nothing from anywhere.
        self.rng = random.Random(derive_state_seed(seed))
        #: place -> number of entries so far.
        self.visits: dict[str, int] = {}
        #: place -> verdict -> count ("success" / "failure" / "none").
        self.verdicts: dict[str, dict[str, int]] = {}
        #: The ordered trajectory: ("visit", place, "") | ("verdict", place, v)
        #: | ("mtd-interrupt", "", resource_type).
        self.history: list[tuple[str, str, str]] = []
        #: How many MTD interrupts the attacker has absorbed so far.
        self.mtd_interrupts: int = 0
        #: The state's own per-step log — persisted by an experiment alongside
        #: the MovementRecord stream (the record schema itself is untouched).
        #: One entry per routing decision; ``factors`` carries only the
        #: non-unit multipliers, so a null-configured run logs empty dicts.
        self.log: list[dict[str, Any]] = []

    # -- the three observation methods (the whole surface a wrapper calls) ----
    def observe_visit(self, place: str) -> None:
        self.visits[place] = self.visits.get(place, 0) + 1
        self.history.append(("visit", place, ""))
        self._notify("observe_visit", place)

    def observe_verdict(self, place: str, verdict: str) -> None:
        by_verdict = self.verdicts.setdefault(place, {})
        by_verdict[verdict] = by_verdict.get(verdict, 0) + 1
        self.history.append(("verdict", place, verdict))
        self._notify("observe_verdict", place, verdict)

    def observe_mtd_interrupt(self, resource_type: str = "") -> None:
        """One MTD interrupt has landed on the attacker (:class:`StatefulAttackOperation`).

        Reported *before* the substrate serves the confusion penalty, and so
        before the routing decision that follows the interrupted action — which
        is the causal order a forgetting rule needs: the mutation degrades what
        the attacker knows, and only then does it choose where to go next.
        """
        self.mtd_interrupts += 1
        self.history.append(("mtd-interrupt", "", resource_type))
        self._notify("observe_mtd_interrupt", resource_type)

    def _notify(self, hook: str, *args: Any) -> None:
        """Fan one observation out to every modulator that declares the hook.
        A modulator that declares none is never called, so the null
        configuration costs one ``getattr`` over an empty tuple."""
        for modulator in self.modulators:
            observer = getattr(modulator, hook, None)
            if observer is not None:
                observer(*args)

    # -- the composition hook ------------------------------------------------
    def modulate(
        self, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        """The per-destination multiplier for the routing decision at ``src`` —
        the product of every registered modulator's factors, all-1.0 when none
        is registered. Refuses a zero or negative factor from a modulator that
        has not declared ``may_zero`` (the stall rule in the module docstring).
        """
        product: dict[str, float] = {dst: 1.0 for dst in base_out_weights}
        for modulator in self.modulators:
            factors = modulator.factors(self, src, base_out_weights)
            may_zero = bool(getattr(modulator, "may_zero", False))
            for dst, factor in factors.items():
                if dst not in product:
                    continue  # a destination outside this out-set is a no-op
                if factor < 0.0 or (factor == 0.0 and not may_zero):
                    raise ValueError(
                        f"modulator {modulator.name!r} returned factor {factor!r} "
                        f"for {src!r} -> {dst!r} without declaring may_zero — "
                        "zeroing an out-edge needs a declared rule and a re-run "
                        "of the no-stall check"
                    )
                product[dst] *= factor
        return product

    # -- introspection (trace narration, experiment persistence) -------------
    def snapshot(self) -> dict[str, Any]:
        """A compact summary of the state right now, for narration and logs."""
        verdict_totals: dict[str, int] = {}
        for by_verdict in self.verdicts.values():
            for verdict, count in by_verdict.items():
                verdict_totals[verdict] = verdict_totals.get(verdict, 0) + count
        return {
            "visits": sum(self.visits.values()),
            "distinct_places": len(self.visits),
            "verdicts": verdict_totals,
            "mtd_interrupts": self.mtd_interrupts,
        }


class StatefulTiming:
    """A :class:`TimingSource` that tells the state about every place entry,
    then delegates the draw unchanged. ``draw`` fires once per place visit,
    before the verb/dwell-only branch, so the state sees *every* place the
    token enters — whatever the place then does. Forwards everything else to
    the wrapped source, exactly as the trace tool's ``_TracedTiming`` does.
    """

    def __init__(self, inner: TimingSource, state: AttackerState) -> None:
        self._inner = inner
        self._state = state

    def draw(self, tactic: str) -> float:
        self._state.observe_visit(tactic)
        return self._inner.draw(tactic)

    def __getattr__(self, name: str):
        return getattr(self._inner, name)


class ModulatedOverlay:
    """An ``OutcomeOverlayLike`` that tells the state about every verdict,
    delegates the composition unchanged, then multiplies the result by the
    state's modulator product and renormalises.

    The wrapped ``compose`` is the sole owner of verdict/composition semantics
    (consume, never fork); this wrapper adds exactly the third factor of the
    generalised rule and nothing else. With no modulators registered the
    multiplier is 1.0 everywhere and the returned distribution is the inner
    one renormalised — the same distribution, so the sampled walk is
    bit-identical (the driver's ``_sample`` normalises by the total anyway).
    """

    def __init__(self, inner: Any, state: AttackerState) -> None:
        self._inner = inner
        self._state = state

    def compose(
        self, src: str, verdict: str, base_out_weights: dict[str, float]
    ) -> dict[str, float]:
        state = self._state
        state.observe_verdict(src, verdict)
        composed = self._inner.compose(src, verdict, base_out_weights)
        factors = state.modulate(src, base_out_weights)
        modulated = {
            dst: weight * factors.get(dst, 1.0)
            for dst, weight in composed.items()
            if weight * factors.get(dst, 1.0) > 0.0
        }
        state.log.append(
            {
                "decision": len(state.log),
                "src": src,
                "verdict": verdict,
                "factors": {d: f for d, f in factors.items() if f != 1.0},
            }
        )
        total = sum(modulated.values())
        if total <= 0.0:
            # Every out-edge suppressed. With no zero-licensed modulator this
            # can only be the inner overlay's own stall, passed through.
            return {}
        return {dst: weight / total for dst, weight in modulated.items()}

    def __getattr__(self, name: str):
        return getattr(self._inner, name)


class StatefulAttackOperation:
    """An ``AttackOperation`` that tells the state about every MTD interrupt the
    attacker absorbs, then delegates the interrupt cost unchanged.

    It exists because the two routing seams cannot see an interrupt. By the time
    the token routes, an MTD interrupt has become an ordinary failure verdict —
    identical, at ``compose``, to a verb the substrate refused on an unmet
    precondition. A modulator that must respond to *the defence* rather than to
    *failure* therefore needs a signal from the one place the two differ.

    ``apply_mtd_interrupt_cost`` is that place: every interrupt path in the
    driver — mid-verb, mid-dwell, mid-blocked-attempt — funnels through
    ``MovementAttacker._pay_interrupt_cost``, which calls it exactly once per
    interrupt. Wrapping it reports the interrupt with the mutating resource's
    layer and changes nothing else; the substrate's own penalty and lost-cursor
    semantics are consumed, never forked, exactly as the driver consumes them.

    Give this wrapper to the ``MovementAttacker`` only. The MTD operation should
    keep the bare attack operation, so nothing in the defence's own path reads
    through a proxy.
    """

    def __init__(self, inner: Any, state: AttackerState) -> None:
        self._inner = inner
        self._state = state

    def apply_mtd_interrupt_cost(self, interrupted_mtd: Any):
        resource_type = ""
        if interrupted_mtd is not None:
            try:
                resource_type = interrupted_mtd.get_resource_type()
            except Exception:  # noqa: BLE001 - observation enrichment only
                resource_type = ""
        self._state.observe_mtd_interrupt(resource_type)
        return (yield from self._inner.apply_mtd_interrupt_cost(interrupted_mtd))

    def __getattr__(self, name: str):
        return getattr(self._inner, name)


class RevisitAversionDemo:
    """**Demonstration only — obviously artificial, never a declared mechanism.**

    Halves the weight of any destination the token has already entered at
    least ``threshold`` times. It exists to prove the seam is live (validation
    gate 3: a registered modulator visibly changes the walk) and to give the
    trace something to narrate; it models nothing, declares no value tier, and
    must not be wired into any experiment. A deterministic function of the
    run's own history — it needs no random stream.
    """

    name = "revisit-aversion-demo"

    def __init__(self, *, threshold: int = 2, factor: float = 0.5) -> None:
        self.threshold = int(threshold)
        self.factor = float(factor)

    def factors(
        self, state: AttackerState, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        return {
            dst: self.factor
            for dst in base_out_weights
            if state.visits.get(dst, 0) >= self.threshold
        }


__all__ = [
    "STATE_STREAM_XOR",
    "derive_state_seed",
    "Modulator",
    "AttackerState",
    "StatefulTiming",
    "ModulatedOverlay",
    "StatefulAttackOperation",
    "RevisitAversionDemo",
]
