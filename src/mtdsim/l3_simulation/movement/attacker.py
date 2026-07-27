"""The movement-layer attacker — a live SimPy net-walker inside MTDSim.

This is the second seam of L3 OGASP: a new attacker class that walks the class
net's single token **live inside a running MTDSim simulation**, *alongside* the
inherited 6-phase :class:`~mtdnetwork.component.adversary.Adversary` /
:class:`~mtdnetwork.operation.attack_operation.AttackOperation` (architecture
§(f); per-run selection, no inheritance — both keep working). Where the native
FSM is a self-driving machine you start once, this driver owns the succession:
the net supplies *movement*, and the carved substrate supplies *outcome* (M4).

Per-place lifecycle, per the M7 handoff, all through the controller library:

    enter place -> dwell (D4 duration) -> controller.phase_for(tactic)
      -> attack_op.step(verb) -> verdict adapter -> overlay.compose(place, verdict)
      -> sample the next transition -> enter the next place

**Consumes, never forks (hard constraint).** Dispatch (``controller.phase_for``),
outcome composition (``overlay.compose``) and the success/failure verdict adapter
are the controller sublayer's surface — this driver *calls* them. They are passed
in as collaborators (``controller``, ``overlay``, ``verdict_of``) so the driver
carries zero dispatch / composition / verdict semantics of its own, and so a run
wires the real controller library while a test can drive the loop with controlled
routing. The production wiring lives in :mod:`mtdsim.l3_simulation.movement.run`.

**The substrate as the outcome oracle.** A dispatched verb runs through the
carved ``step(verb)`` (anatomy §3), which performs one verb with its native time
cost and returns its ``_do_*`` outcome without succession. The binary verdict is
*read* from that outcome (never re-rolled — no double counting), and it routes the
token: a success and a failure at the same place select different out-sets, so net
state moves with substrate outcomes (the two-way demonstration).

**Coupling surfaces as data, not silence.** The action layer is strongly coupled
(anatomy §§2–3): a verb the net dispatches may lack the shared adversary state its
core assumes (``curr_host`` / ``curr_ports``). Rather than re-impose the native
order to satisfy it — which would manufacture the very coupling the evaluation
tests for (anatomy §6, H-coupling) — the driver reads an unmet precondition as a
**failure verdict** (recorded ``PRECONDITION_UNMET``) and lets the overlay route
it. Every such block is visible in the records.

**Interrupt scope.** For **all six** verbs an MTD interrupt propagates out of
``step`` as ``simpy.Interrupt``; the driver catches it, reads it as a failure
verdict (``MTD_INTERRUPT``) and routes — the interrupt-as-failure feedback Jin's
motivating example wanted. ``EXPLOIT_VULN`` is no longer special: the carve runs
its core with ``driven=True`` (``attack_operation.step``), so an interrupt
re-raises rather than self-catching into the native ``_handle_interrupt``
recovery — no rogue native chain runs behind the driver. The one remaining
``EXPLOIT_HALTED`` return is the sim-end case (``end_event`` triggered mid-vuln),
handled as ``_SIM_END``, not an interrupt.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol

import simpy

from mtdnetwork.operation.attack_operation import (
    EXPLOIT_HALTED,
    STEP_ABORTED,
    ActionContextError,
)

Verdict = str  # "success" | "failure" (binary outcome only, M2)

_REPO_ROOT = Path(__file__).resolve().parents[4]
DURATIONS_PATH = _REPO_ROOT / "data" / "ogasp" / "tactic_durations.json"


# --- The two injected controller collaborators (consumed, never forked) -----
class VerdictAdapter(Protocol):
    """Reads a dispatched verb's substrate outcome (and whether an MTD interrupt
    halted it) into the binary verdict — the controller-finalisation handoff's
    verdict adapter (controller.md §4). ``outcome`` is a ``_do_*`` return value
    (``bool`` / ``EXPLOIT_*`` / ``None``); ``interrupted`` is True for an MTD
    interrupt (which reads as failure)."""

    def __call__(self, verb: str, outcome: Any, interrupted: bool) -> Verdict: ...


class OutcomeOverlayLike(Protocol):
    """Conditions a base out-distribution on the verdict and renormalises — the
    controller sublayer's ``OutcomeOverlay.compose`` (M2 composition rule). Returns
    the renormalised out-weights; an empty dict signals a stall (failure suppressed
    every out-edge)."""

    def compose(
        self, src: str, verdict: Verdict, base_out_weights: dict[str, float]
    ) -> dict[str, float]: ...


def load_dwell_catalogue(path: Path | str = DURATIONS_PATH) -> dict[str, float]:
    """``tactic -> per-place dwell (simulated seconds)`` from the D4 catalogue."""
    with Path(path).open(encoding="utf-8") as fh:
        doc = json.load(fh)
    return {t: float(v["duration_s"]) for t, v in doc["tactics"].items()}


@dataclass(frozen=True)
class MovementRecord:
    """One per-event record of the walk — the movement layer's own record type,
    read by :mod:`mtdsim.l3_simulation.movement.statistics` (a reader; the
    inherited ``AttackStatistics`` maths is untouched)."""

    profile: str
    step_index: int
    place: str  # the tactic-place the token sat on
    verb: str  # the dispatched MTDSim verb (== sim_phase)
    outcome: str  # normalised outcome tag (see _outcome_tag)
    verdict: str  # "success" | "failure" | "" (terminal, no verb ran)
    interrupted: bool  # an MTD interrupt halted the verb
    blocked: bool  # the verb's precondition was unmet (PRECONDITION_UNMET)
    next_place: str | None  # the sampled next place, or None (stall / sink / terminal)
    start_time: float  # sim time the event began (BEFORE the dwell)
    end_time: float  # sim time the event finished
    # The dwell actually CONSUMED at this place, which is the catalogue value except
    # when an MTD interrupt cut the dwell short — then it is the partial time served.
    # (`end_time - start_time - dwell` is therefore the verb's own time cost, and is
    # never negative; it is 0 for a blocked or dwell-interrupted event.)
    dwell: float
    interrupted_by: str  # MTD resource type, or "" — record enrichment only


# The verdict the movement layer assigns an un-actionable dispatch (a verb whose
# substrate precondition is unmet — no substrate outcome exists for the controller
# to judge). This is a movement routing policy, not a substrate verdict: it uses
# the controller's binary vocabulary ("failure") but is decided in-layer, so the
# controller's verdict adapter stays the sole authority over *substrate outcomes*.
_UNACTIONABLE_VERDICT: Verdict = "failure"

# Terminal / special outcome tags.
_PRECONDITION_UNMET = "PRECONDITION_UNMET"
_MTD_INTERRUPT = "MTD_INTERRUPT"
_SIM_END = "SIM_END"
_MAX_EVENTS = "MAX_EVENTS"


def _outcome_tag(outcome: Any) -> str:
    """Normalise a ``_do_*`` return value to a stable string tag for the record."""
    if outcome is None:
        return "NONE"
    if outcome is True:
        return "TRUE"
    if outcome is False:
        return "FALSE"
    return str(outcome)


class MovementAttacker:
    """Drives the class net's single token live inside MTDSim, alongside the
    inherited 6-phase attacker (per-run selection). See the module docstring for
    the per-place lifecycle and the consume-never-fork contract.

    A hard cap ``max_events`` backstops a pathological cycle (it is a backstop, not
    a policy — if it fires it is recorded as a ``MAX_EVENTS`` terminal event, never
    a silent truncation).
    """

    def __init__(
        self,
        *,
        env: simpy.Environment,
        end_event: simpy.Event,
        adversary: Any,
        attack_operation: Any,
        routing_net: Any,
        controller: Any,
        overlay: OutcomeOverlayLike,
        verdict_of: VerdictAdapter,
        dwell_catalogue: dict[str, float] | None = None,
        seed: int = 0,
        register_for_interrupts: bool = True,
        max_events: int = 50_000,
    ) -> None:
        import random

        self.env = env
        self.end_event = end_event
        self.adversary = adversary
        self.attack_op = attack_operation
        self.routing = routing_net
        self.controller = controller
        self.overlay = overlay
        self.verdict_of = verdict_of
        self.dwell = dwell_catalogue if dwell_catalogue is not None else load_dwell_catalogue()
        # A dedicated RNG so token sampling is reproducible (SIM-05) and does not
        # perturb the substrate's global random / numpy draws.
        self._rng = random.Random(seed)
        self.register_for_interrupts = register_for_interrupts
        self.max_events = max_events
        self.records: list[MovementRecord] = []
        self._proc: simpy.Process | None = None

    # -- lifecycle ----------------------------------------------------------
    def start(self) -> simpy.Process:
        """Launch the walk as a SimPy process. Registers the process so an MTD
        mutation interrupts *this* driver (not a native chain) when
        ``register_for_interrupts`` is set."""
        self._proc = self.env.process(self._walk())
        if self.register_for_interrupts:
            self.attack_op.set_attack_process(self._proc)
        return self._proc

    @property
    def process(self) -> simpy.Process | None:
        return self._proc

    # -- the walk -----------------------------------------------------------
    def _walk(self):
        place = self.routing.entry_place
        step_index = 0
        while True:
            if self.end_event.triggered:
                self._emit_terminal(place, step_index, _SIM_END)
                return
            if step_index >= self.max_events:
                self._emit_terminal(place, step_index, _MAX_EVENTS)
                return

            verb = self.controller.phase_for(place)
            dwell = float(self.dwell.get(place, 0.0))
            start_time = self.env.now

            # The dwell is interruptible: an MTD mutation while the token sits at
            # a place, before its verb dispatches, reads as a failure at that
            # place (same interrupt-as-failure feedback as a verb interrupt).
            dwell_interrupted = False
            try:
                if dwell > 0:
                    yield self.env.timeout(dwell)
            except simpy.Interrupt:
                dwell_interrupted = True
                # The interrupt cut the dwell short, so the catalogue value was NOT
                # consumed. Record what was actually served, or the record asserts
                # more elapsed time than the event occupied.
                dwell = self.env.now - start_time
            if self.end_event.triggered:
                self._emit_terminal(place, step_index, _SIM_END, verb=verb,
                                    dwell=dwell, start_time=start_time)
                return

            if dwell_interrupted:
                outcome_tag, verdict, interrupted, blocked, interrupted_by = (
                    self._read_interrupt(verb, None)
                )
            else:
                outcome_tag, verdict, interrupted, blocked, interrupted_by = (
                    yield from self._dispatch(verb)
                )
                if outcome_tag == _SIM_END:
                    self._emit_terminal(place, step_index, _SIM_END, verb=verb,
                                        dwell=dwell, start_time=start_time)
                    return

            next_place = self._route(place, verdict)
            self.records.append(
                MovementRecord(
                    profile=self.routing.profile,
                    step_index=step_index,
                    place=place,
                    verb=verb,
                    outcome=outcome_tag,
                    verdict=verdict,
                    interrupted=interrupted,
                    blocked=blocked,
                    next_place=next_place,
                    start_time=start_time,
                    end_time=self.env.now,
                    dwell=dwell,
                    interrupted_by=interrupted_by,
                )
            )
            step_index += 1
            if next_place is None:
                return  # stall (overlay suppressed every out-edge) or sink
            place = next_place

    def _dispatch(self, verb: str):
        """Run one dispatched verb through the carved substrate and read the
        verdict. Returns ``(outcome_tag, verdict, interrupted, blocked,
        interrupted_by)``; ``outcome_tag == _SIM_END`` means the sim ended
        mid-verb (the caller emits a terminal record and stops)."""
        # Unmet precondition: the substrate cannot run this verb from its current
        # state, so there is NO substrate outcome for the controller's verdict
        # adapter to judge. This is a movement-layer routing condition, not a
        # substrate verdict — the movement layer records it a failure directly (an
        # un-actionable dispatch retries/backs off) rather than fabricating a
        # substrate signal for the controller. It does NOT re-impose the native
        # order to satisfy the precondition (that would manufacture the very
        # coupling the evaluation tests for — anatomy §6, H-coupling). No substrate
        # time is consumed — the verb never ran.
        try:
            self.attack_op.assert_action_context(verb)
        except ActionContextError:
            return _PRECONDITION_UNMET, _UNACTIONABLE_VERDICT, False, True, ""

        interrupted = False
        try:
            outcome = yield from self.attack_op.step(verb)
        except simpy.Interrupt:
            interrupted = True
            outcome = None

        if not interrupted and (outcome is STEP_ABORTED or outcome == EXPLOIT_HALTED):
            # The sim ended DURING the verb, so it never acted: step() returns the
            # STEP_ABORTED sentinel, or EXPLOIT_HALTED on the exploit path (not an
            # interrupt — that re-raises now that step() drives it driven=True).
            #
            # This must be read off the OUTCOME, not off end_event.triggered. Three
            # cores (_do_exploit_vuln, _do_scan_port, _do_brute_force) call
            # update_compromise_progress, which fires end_event when the objective is
            # met — so a verb that ran and *succeeded* leaves end_event triggered.
            # Inferring the abort from that flag discarded exactly the compromise that
            # completed the run, leaving ASR scoring it a success while MTTC dropped it
            # for having no compromise event.
            return _SIM_END, "", False, False, ""

        # Every verb — EXPLOIT_VULN included — propagates an MTD interrupt out of
        # step() as simpy.Interrupt (the carve's driven=True re-raise), caught
        # above. Read it as an interrupt-halt failure and let the overlay route.
        if interrupted:
            return self._read_interrupt(verb, outcome)

        verdict = self.verdict_of(verb, outcome, False)
        return _outcome_tag(outcome), verdict, False, False, ""

    def _read_interrupt(self, verb: str, outcome: Any):
        """Build the interrupt result tuple: read the interrupting MTD's resource
        type (record enrichment), clear it, and read the interrupt as a failure
        verdict via the injected adapter. Shared by the dwell-interrupt and the
        verb-interrupt paths."""
        interrupted_by = ""
        mtd = getattr(self.attack_op, "_interrupted_mtd", None)
        if mtd is not None:
            try:
                interrupted_by = mtd.get_resource_type()
            except Exception:  # noqa: BLE001 - record enrichment only
                interrupted_by = ""
            self.attack_op.set_interrupted_mtd(None)
        verdict = self.verdict_of(verb, outcome, True)
        return _MTD_INTERRUPT, verdict, True, False, interrupted_by

    def _route(self, place: str, verdict: str) -> str | None:
        """Condition the base out-distribution on the verdict (overlay.compose)
        and sample the next place. None on a stall (empty composed distribution)
        or a sink (no base out-edges)."""
        base_out = self.routing.base_out_weights(place)
        if not base_out:
            return None
        composed = self.overlay.compose(place, verdict, base_out)
        return self._sample(composed)

    def _sample(self, distribution: dict[str, float]) -> str | None:
        """Draw one destination from a ``{place: weight}`` distribution with the
        driver's seeded RNG. Deterministic: destinations are sorted before the
        cumulative draw. None for an empty distribution (stall)."""
        items = sorted(distribution.items())
        total = sum(w for _, w in items if w > 0)
        if total <= 0:
            return None
        threshold = self._rng.random() * total
        cumulative = 0.0
        for dst, weight in items:
            if weight <= 0:
                continue
            cumulative += weight
            if threshold < cumulative:
                return dst
        return items[-1][0]

    def _emit_terminal(
        self,
        place: str,
        step_index: int,
        tag: str,
        *,
        verb: str = "",
        dwell: float = 0.0,
        start_time: float | None = None,
    ) -> None:
        """Record a terminal event (sim end / max-events backstop) so the walk's
        end is visible in the records rather than an unexplained stop."""
        now = self.env.now
        self.records.append(
            MovementRecord(
                profile=self.routing.profile,
                step_index=step_index,
                place=place,
                verb=verb,
                outcome=tag,
                verdict="",
                interrupted=False,
                blocked=False,
                next_place=None,
                start_time=start_time if start_time is not None else now,
                end_time=now,
                dwell=dwell,
                interrupted_by="",
            )
        )


__all__ = [
    "Verdict",
    "VerdictAdapter",
    "OutcomeOverlayLike",
    "MovementRecord",
    "MovementAttacker",
    "load_dwell_catalogue",
    "DURATIONS_PATH",
]
