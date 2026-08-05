"""The movement-layer attacker — a live SimPy net-walker inside MTDSim.

This is the second seam of L3 OGASP: a new attacker class that walks the class
net's single token **live inside a running MTDSim simulation**, *alongside* the
inherited 6-phase :class:`~mtdnetwork.component.adversary.Adversary` /
:class:`~mtdnetwork.operation.attack_operation.AttackOperation` (architecture
§(f); per-run selection, no inheritance — both keep working). Where the native
FSM is a self-driving machine you start once, this driver owns the succession:
the net supplies *movement*, and the carved substrate supplies *outcome* (M4).

Per-place lifecycle, per the M7 handoff, all through the controller library:

    enter place -> draw the tactic's time -> controller.phase_for(tactic)
      -> attack_op.step(verb, duration=that time) -> verdict adapter
      -> overlay.compose(place, verdict) -> sample the next transition
      -> enter the next place

**The movement layer owns every unit of the attacker's time (S3-R).** The tactic's
draw — from :mod:`mtdsim.l3_simulation.movement.timing`, with the declared
catalogue duration as its mean — *is* the action's duration, handed to the
substrate and spent there. The substrate's own ``ATTACK_DURATION`` and
``exploit_time`` are **not** consumed on this arm; they remain the native FSM's
pricing and are untouched there. One consequence is the intended one: because many
tactics map to one verb, the same verb costs different amounts depending on which
tactic invoked it, since the price belongs to the modelled behaviour rather than to
the verb.

Every place visit costs its tactic's time, whatever happens at it — the action ran,
the action was blocked by an unmet precondition, or the place dispatches nothing at
all. Charging nothing for a blocked attempt would make an unsatisfiable place a
free move, and the profiles that block most would churn the net at no cost.

The one attacker-side duration this layer does *not* supply is the MTD confusion
penalty, which stays inside the substrate: it is the simulator's model of what a
defender does to an attacker mid-action, so it sits on the defender↔attacker border
rather than in the portable layer.

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
from typing import Any, Callable, NamedTuple, Protocol

import simpy

from mtdnetwork.operation.attack_operation import (
    EXPLOIT_HALTED,
    STEP_ABORTED,
    ActionContextError,
)

from mtdsim.l3_simulation.movement.timing import TacticTiming, TimingSource

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


# The two place classes (overlay design §6.3). A dwell-only place is one the
# selected controller mapping declares as dispatching no verb.
ACTION_BEARING = "action-bearing"
DWELL_ONLY = "dwell-only"

# What the adversary's ``curr_process`` reads as while the token sits on a
# dwell-only place. It is deliberately *not* one of the six verbs: the defender's
# application-layer interrupt gate reads curr_process to decide whether a mutation
# blocks the attacker, and leaving the previous verb there would have the gate
# judging a verb that finished steps ago. A sentinel is judged as a
# surface-dependent process, which is the conservative reading — a dwell-only
# place does not become a cost-free hiding spot from MTD.
DWELL_PROCESS = "DWELL"


class InterruptSource(NamedTuple):
    """Which mechanism interrupted the attacker, in both the vocabularies the
    record carries: its **resource class** and its **name**.

    Threaded through the interrupt paths as one object rather than as two parallel
    strings, so the class and the name cannot drift apart on the way to the
    record. The empty instance means *no interrupt* (or an MTD object that would
    not answer), which is what every non-interrupt path returns."""

    resource_type: str = ""
    name: str = ""


NO_INTERRUPT = InterruptSource()


def load_dwell_catalogue(path: Path | str = DURATIONS_PATH) -> dict[str, float]:
    """``tactic -> declared per-place duration (simulated seconds)`` from the D4
    catalogue.

    The movement layer reads each declared value as the **mean** of that tactic's
    firing time (S3), not as a fixed dwell; the standalone timeline runner reads
    the same field as a point value under its own deterministic discipline. The
    catalogue is neutral between them — it declares a duration, and each consumer
    declares what it does with it.
    """
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
    verb: str  # the dispatched MTDSim verb (== sim_phase); "" if none ran
    outcome: str  # normalised outcome tag (see _outcome_tag)
    verdict: str  # "success" | "failure" | "" (no verb ran: dwell-only or terminal)
    interrupted: bool  # an MTD interrupt halted the verb
    blocked: bool  # the verb's precondition was unmet (PRECONDITION_UNMET)
    next_place: str | None  # the sampled next place, or None (stall / sink / terminal)
    start_time: float  # sim time the event began (BEFORE the dwell)
    end_time: float  # sim time the event finished
    # The dwell actually CONSUMED at this place: this visit's draw (S3 — a draw
    # about the catalogue mean, so it differs from visit to visit), except when an
    # MTD interrupt cut the dwell short — then it is the partial time served.
    # (`end_time - start_time - dwell` is therefore the verb's own time cost, and is
    # never negative; it is 0 for a blocked or dwell-interrupted event.)
    dwell: float
    interrupted_by: str  # MTD resource type, or "" — record enrichment only
    # The **name** of the interrupting mechanism ("IPShuffle", "OSDiversity", …),
    # or "" — the sibling of `interrupted_by` above, which carries only the
    # resource class. Both are record enrichment; neither is read by the walk.
    #
    # The class alone cannot attribute an interrupt to a mechanism, and the two
    # reported class pairs (CompleteTopologyShuffle/IPShuffle on `network`,
    # OSDiversity/ServiceDiversity on `application`) are therefore
    # indistinguishable in this record *by construction* — so the class-level
    # disruption model could not be verified on the arm the headline runs on, only
    # assumed. The suite's standing rule is to extend the reader rather than widen
    # the record; the burden of proof here is that no reader can recover the name,
    # because the driver discards it at the one site that holds it
    # (`_pay_interrupt_cost`). The substrate's own `AttackStatistics` has carried
    # the same pair (`interrupted_in` / `interrupted_by`) since the lineage, so
    # this brings the movement record to parity with the native arm's rather than
    # inventing a field.
    #
    # Schema-only: the value is already in hand at the assignment site, nothing
    # reads it to decide anything, and no golden moves.
    interrupted_by_name: str = ""
    # Whether the place dispatched a verb at all (overlay design §6.3). A
    # dwell-only place consumes time, fires nothing and raises no verdict, so
    # without this an analysis cannot tell "spent time thinking" from "did
    # nothing" — and the action-budget decomposition that made experiment 1
    # legible would silently count dwell-only steps as failed actions.
    place_class: str = ACTION_BEARING
    # This visit is a **retrace** — the token stepped back here from a sink under
    # the S5 policy (sink_retrace_design.md §3.3). It is an ordinary visit in every
    # other respect: it draws its dwell, dispatches its verb and raises a real
    # verdict. The flag exists so every per-action metric can be computed with
    # retraces in or out and the write-up can say which, and so the retrace count
    # is itself readable. Recording a retrace verbless was rejected — the
    # measurement suite reads a verbless record as a dwell-only visit, which would
    # silently corrupt `dwell_only_fraction` and every denominator built on it.
    retrace: bool = False
    # Distinct hosts the adversary held at the moment this record was written —
    # ``len(adversary.get_compromised_hosts())``, the same list whose end-of-run
    # length is ``MovementRunResult.compromised_count``. It is the attacker's
    # **progress trajectory**, and it is here rather than derived because it
    # cannot be derived: the record carries no host identity, so cumulative
    # compromise *events* over-count distinct hosts through re-compromise. That
    # over-count was measured before this field was added — 837 events against
    # 155 distinct hosts over 50 runs, a ratio of **5.40** — and it is worse
    # without MTD (5.4–8.8) than with it (1.8–3.5), so using events as the
    # progress proxy would have biased precisely the MTD-versus-no-MTD comparison
    # the disengagement measure exists to make. The suite's standing preference
    # is to extend the reader rather than widen the record; the burden of proof
    # that sits on a schema change is discharged by that measurement.
    #
    # Verified properties, asserted in the suite rather than assumed: the
    # underlying list holds no duplicates, the count is monotone non-decreasing
    # across a run, and its final value equals ``compromised_count`` exactly. The
    # field is substrate ground truth sampled in-layer, not a movement-layer
    # estimate, and it carries no host identity — only the count.
    n_compromised: int = 0


# The distinguished routing verdict for a place that raised no verdict at all (a
# dwell-only place: no verb ran, so there is no substrate outcome to judge). It is
# NOT a substrate verdict and no overlay registers it, so ``compose`` finds an
# empty per-source table, every destination passes through at factor 1.0, and the
# routed distribution is the base weights renormalised — sampled identically to
# the base weights themselves. What routing through ``compose`` buys is that the
# whole observation surface (every routing decision, dwell-only included) flows
# through the one ``OutcomeOverlayLike`` seam a stateful wrapper attaches to.
VERDICT_NONE: Verdict = "none"

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
# The S5 retrace policy ran out of places to step back to: the token reached a
# sink and every predecessor on its own visited chain was exhausted. Recorded
# distinctly from a plain sink termination so the two are never conflated — a
# sink termination means "the policy was off", this means "the policy ran and had
# nowhere left to go". Unreachable on the current corpus (every sink predecessor
# keeps five to eleven alternatives, sink_retrace_design.md §3.1); it exists so
# the degenerate case is handled rather than assumed away.
_SINK_EXHAUSTED = "SINK_EXHAUSTED"
# A dwell-only place served its dwell and dispatched nothing. Distinct from
# MTD_INTERRUPT even when a mutation cut the dwell short, because the two differ
# in what they cost, not in what they dispatched: see _serve_dwell_only.
_DWELL_ONLY_TAG = "DWELL_ONLY"


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
        timing: TimingSource | None = None,
        seed: int = 0,
        register_for_interrupts: bool = True,
        max_events: int = 50_000,
        # The S5 sink-retrace policy, OFF by default — deliberately, and for the
        # same reason the mapping and overlay registries default to experiment 1's
        # values rather than the newest: promoting a new behaviour to default
        # re-bakes an experiment's choice into the pipeline, and an unqualified run
        # should reproduce what has always run. Experiment 2 names it at the seam,
        # exactly as it names its mapping and its overlay version. The
        # accept-and-censor arm it supersedes stays reachable for the same reason.
        retrace_sinks: bool = False,
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
        # The movement layer's timing source: it supplies each place's dwell (a
        # draw about the catalogue mean), the SimPy loop spends it. Its stream is
        # separately seeded from `_rng` above, so introducing the draws neither
        # reads nor advances the token sampler or the substrate's dice.
        self.timing: TimingSource = (
            timing if timing is not None else TacticTiming(self.dwell, seed=seed)
        )
        self.register_for_interrupts = register_for_interrupts
        self.max_events = max_events
        self.records: list[MovementRecord] = []
        self._proc: simpy.Process | None = None
        # -- the S5 sink-retrace policy (sink_retrace_design.md) ---------------
        self.retrace_sinks = retrace_sinks
        # The chain of places the token walked, so a retrace knows where it came
        # from — and, in the degenerate case, where *that* came from (§3.5).
        self._visited: list[str] = []
        # The one-shot edge suppression: ``(src, dst)`` removed from the NEXT
        # selection at ``src`` and from that selection only. This is the single
        # genuinely new policy in the retrace design; everything else it does is
        # an ordinary place visit.
        self._suppressed_edge: tuple[str, str] | None = None
        # Set when a retrace has just been chosen, consumed by the record the
        # retraced-to visit writes.
        self._retrace_pending = False
        # Counted rather than budgeted (§3.4): the design declines a declared
        # retrace budget and surfaces the frequency instead, so a high count is
        # data rather than something a knob quietly held down.
        self.retrace_count = 0

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
        self._visited.append(place)
        while True:
            # Consumed here, one iteration after the retrace was chosen, so the
            # flag lands on the visit the token stepped back INTO rather than on
            # the sink's own record (_take_retrace_flag).
            is_retrace = self._take_retrace_flag()
            if self.end_event.triggered:
                self._emit_terminal(place, step_index, _SIM_END)
                return
            if step_index >= self.max_events:
                self._emit_terminal(place, step_index, _MAX_EVENTS)
                return

            # [0, 1] verbs per tactic (S4): None means the selected mapping
            # declares this tactic dwell-only — it consumes time and dispatches
            # nothing. Handled on its own path below, because there is no verb to
            # announce, no substrate outcome to read and so no verdict to route on.
            verb = self.controller.phase_for(place)
            # The one point where the movement layer's time is taken (S3). One
            # draw per place visit, whatever the place class — a dwell-only place
            # pays the same behavioural tempo as an action-bearing one, it simply
            # dispatches nothing afterwards.
            dwell = self.timing.draw(place)
            start_time = self.env.now

            if verb is None:
                dwell, interrupted, source = yield from self._serve_dwell_only(
                    dwell, start_time
                )
                if self.end_event.triggered:
                    self._emit_terminal(place, step_index, _SIM_END, dwell=dwell,
                                        start_time=start_time,
                                        place_class=DWELL_ONLY)
                    return
                # No verdict, so no conditioning — but the routing still flows
                # through ``compose`` under the distinguished ``VERDICT_NONE``,
                # which no overlay registers: the composed distribution is the
                # base weights renormalised, sampled identically (overlay design
                # §3 stands — an unconditioned place routes on base weights).
                next_place = self._route(place, VERDICT_NONE)
                next_place, exhausted = self._maybe_retrace(place, next_place)
                self.records.append(
                    MovementRecord(
                        profile=self.routing.profile,
                        step_index=step_index,
                        place=place,
                        verb="",
                        outcome=_DWELL_ONLY_TAG,
                        verdict="",
                        interrupted=interrupted,
                        blocked=False,
                        next_place=next_place,
                        start_time=start_time,
                        end_time=self.env.now,
                        dwell=dwell,
                        interrupted_by=source.resource_type,
                        interrupted_by_name=source.name,
                        place_class=DWELL_ONLY,
                        retrace=is_retrace,
                        n_compromised=self._n_compromised(),
                    )
                )
                step_index += 1
                if next_place is None:
                    if exhausted:
                        self._emit_terminal(place, step_index, _SINK_EXHAUSTED,
                                            place_class=DWELL_ONLY)
                    return  # sink
                place = next_place
                self._visited.append(place)
                continue

            # Announce the verb the token is about to fire, BEFORE any time passes.
            #
            # The defender decides whether an application-layer mutation interrupts
            # by reading the adversary's curr_process (mtd_operation._interrupt_
            # adversary): it interrupts only the surface-dependent phases, per Brown
            # B-INT-02 (a lost service connection blocks port-scanning and
            # exploitation, but not host discovery). Left unset until step() ran,
            # curr_process held the PREVIOUS verb for the whole of the preceding
            # wait, so the gate was routinely judging a verb that had already
            # finished. It flipped 27% of application-layer decisions: interrupts
            # missed while the token sat on a tactic about to exploit, and interrupts
            # fired at one about to discover. The driver's own record already
            # attributed the interrupt to `verb`, so the record and the gate
            # disagreed.
            self.adversary.set_curr_process(verb)

            outcome_tag, verdict, interrupted, blocked, source, dwell = (
                yield from self._dispatch(verb, dwell, start_time)
            )
            if outcome_tag == _SIM_END:
                self._emit_terminal(place, step_index, _SIM_END, verb=verb,
                                    dwell=dwell, start_time=start_time)
                return

            next_place = self._route(place, verdict)
            next_place, exhausted = self._maybe_retrace(place, next_place)
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
                    interrupted_by=source.resource_type,
                    interrupted_by_name=source.name,
                    retrace=is_retrace,
                    n_compromised=self._n_compromised(),
                )
            )
            step_index += 1
            if next_place is None:
                if exhausted:
                    self._emit_terminal(place, step_index, _SINK_EXHAUSTED)
                return  # stall (overlay suppressed every out-edge) or sink
            place = next_place
            self._visited.append(place)

    def _n_compromised(self) -> int:
        """Distinct hosts the adversary currently holds — the progress trajectory
        sampled per record. Read-only over the substrate's own list, so it is
        ground truth rather than a movement-layer tally, and it costs one ``len``
        per record. Defensive against an adversary that does not expose the
        accessor so a test double need not implement it."""
        try:
            return len(self.adversary.get_compromised_hosts())
        except Exception:  # noqa: BLE001 - record enrichment only, never fatal
            return 0

    def _dispatch(self, verb: str, duration: float, start_time: float):
        """Run one dispatched verb through the carved substrate for the time the
        movement layer supplies, and read the verdict. Returns ``(outcome_tag,
        verdict, interrupted, blocked, source, served)``, where ``served``
        is the time the place actually consumed; ``outcome_tag == _SIM_END`` means
        the sim ended mid-verb (the caller emits a terminal record and stops)."""
        # Unmet precondition: the substrate cannot run this verb from its current
        # state, so there is NO substrate outcome for the controller's verdict
        # adapter to judge. This is a movement-layer routing condition, not a
        # substrate verdict — the movement layer records it a failure directly (an
        # un-actionable dispatch retries/backs off) rather than fabricating a
        # substrate signal for the controller. It does NOT re-impose the native
        # order to satisfy the precondition (that would manufacture the very
        # coupling the evaluation tests for — anatomy §6, H-coupling).
        #
        # It still costs the tactic's time. The attacker committed the procedure
        # that tactic represents and it came to nothing; charging nothing would make
        # an unsatisfiable place a free move, and the profiles that block most would
        # churn the net at no cost — which is precisely where the H-coupling finding
        # lives, so it must not be the cheap path.
        try:
            self.attack_op.assert_action_context(verb)
        except ActionContextError:
            served, interrupted, source = yield from self._serve_time(
                duration, start_time
            )
            return (
                _PRECONDITION_UNMET, _UNACTIONABLE_VERDICT, interrupted, True,
                source, served,
            )

        interrupted = False
        served = duration
        try:
            outcome = yield from self.attack_op.step(verb, duration=duration)
        except simpy.Interrupt:
            interrupted = True
            outcome = None
            # Captured BEFORE the confusion penalty is paid, so `served` is the
            # action's own time and the penalty stays outside it.
            served = self.env.now - start_time

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
            return _SIM_END, "", False, False, "", served

        # Every verb — EXPLOIT_VULN included — propagates an MTD interrupt out of
        # step() as simpy.Interrupt (the carve's driven=True re-raise), caught
        # above. Read it as an interrupt-halt failure and let the overlay route.
        if interrupted:
            tag, verdict, was_interrupted, was_blocked, source = (
                yield from self._read_interrupt(verb, outcome)
            )
            return tag, verdict, was_interrupted, was_blocked, source, served

        verdict = self.verdict_of(verb, outcome, False)
        return _outcome_tag(outcome), verdict, False, False, NO_INTERRUPT, served

    def _read_interrupt(self, verb: str, outcome: Any):
        """Handle an MTD interrupt: pay the substrate's price for being blocked, read
        the interrupting MTD's resource class and name (record enrichment), clear it, and read
        the interrupt as a failure verdict via the injected adapter. Shared by the
        dwell-interrupt and the verb-interrupt paths.

        **Pays the confusion penalty** (Brown B-ATK-07, §V-A: a time penalty applies
        *whenever* an attacker is blocked by an MTD) by consuming the substrate's own
        ``apply_mtd_interrupt_cost`` — which also clears the host cursor on a
        network-layer mutation, because B-INT-01 says that connection is gone. The
        driver does not fork either semantics; it consumes them, exactly as it
        consumes ``step``. What it keeps is *succession*: the native FSM would force a
        re-scan here, whereas this driver reads a failure verdict and lets the overlay
        route — the carve's whole purpose.

        Before this, the driven arm consumed **no** penalty and kept exploiting a host
        it had just lost, so MTD was materially cheaper for the movement attacker than
        for the baseline it is compared against.
        """
        source = yield from self._pay_interrupt_cost()
        verdict = self.verdict_of(verb, outcome, True)
        return _MTD_INTERRUPT, verdict, True, False, source

    def _pay_interrupt_cost(self):
        """Consume the substrate's own interrupt cost and report which MTD did it,
        as an :class:`InterruptSource` (resource class **and** name).

        Shared by every interrupt path — including a dwell-only place's, which
        pays the same price for the same defensive event even though it raises no
        verdict. Not paying there would make dwell-only places cost-free under
        MTD, which would flatter the attacker for a reason that has nothing to do
        with its behaviour.
        """
        source = NO_INTERRUPT
        mtd = getattr(self.attack_op, "_interrupted_mtd", None)
        if mtd is not None:
            try:
                source = InterruptSource(mtd.get_resource_type(), mtd.get_name())
            except Exception:  # noqa: BLE001 - record enrichment only
                source = NO_INTERRUPT
        yield from self.attack_op.apply_mtd_interrupt_cost(mtd)
        if mtd is not None:
            self.attack_op.set_interrupted_mtd(None)
        return source

    def _serve_time(self, duration: float, start_time: float):
        """Spend the movement layer's supplied time without dispatching anything.

        Returns ``(served, interrupted, source)``. Used by the two paths
        where the token spends a tactic's time but no substrate action runs: a
        dwell-only place, and an action whose precondition was unmet. An MTD
        mutation during it cuts the time short — ``served`` is then what was
        actually consumed, or the record would claim more elapsed time than the
        event occupied — and the substrate's interrupt price is paid, so neither
        path becomes a cost-free hiding spot from MTD.
        """
        interrupted = False
        source = NO_INTERRUPT
        served = duration
        try:
            if duration > 0:
                yield self.env.timeout(duration)
        except simpy.Interrupt:
            interrupted = True
            served = self.env.now - start_time
            source = yield from self._pay_interrupt_cost()
        return served, interrupted, source

    def _serve_dwell_only(self, dwell: float, start_time: float):
        """Serve a dwell-only place: advance time, dispatch nothing, judge nothing.

        An MTD mutation during the dwell is felt in *cost* — the substrate's
        interrupt price is paid, and the record says an interrupt happened — but
        **not in routing**: no verb ran, so there is no substrate outcome for the
        verdict adapter to read, and fabricating one would put a substrate signal
        in the record that the substrate never produced. The token therefore routes
        on the base weights either way (overlay design §5, the stated scope
        boundary).
        """
        self.adversary.set_curr_process(DWELL_PROCESS)
        return (yield from self._serve_time(dwell, start_time))

    def _route(self, place: str, verdict: str) -> str | None:
        """Condition the base out-distribution on the verdict (overlay.compose)
        and sample the next place. None on a stall (empty composed distribution)
        or a sink (no base out-edges).

        A pending **one-shot retrace suppression** for this place is applied first
        and cleared as it is applied (S5; ``sink_retrace_design.md`` §3.1): the
        edge the token just came back along is removed from *this* selection and
        from no other, so returning to the same tactic on a later occasion sees
        the full out-set again. Suppressing before composing rather than after
        means the renormalisation runs over the remaining destinations, which is
        what makes it a re-drawn choice rather than a reweighted one."""
        base_out = self.routing.base_out_weights(place)
        if not base_out:
            return None
        suppressed = self._suppressed_edge
        if suppressed is not None and suppressed[0] == place:
            base_out.pop(suppressed[1], None)
            self._suppressed_edge = None  # one-shot, consumed here
        composed = self.overlay.compose(place, verdict, base_out)
        return self._sample(composed)

    # -- the S5 sink-retrace policy (sink_retrace_design.md) ------------------
    def _maybe_retrace(self, place: str, next_place: str | None) -> tuple[str | None, bool]:
        """Apply the retrace policy when routing yielded nowhere to go.

        Returns ``(destination, exhausted)``. ``destination`` is the place to move
        to — unchanged when routing already found one, the retrace target when the
        policy fires, and ``None`` when the walk ends. ``exhausted`` is True only
        for the degenerate case the policy ran and could not resolve, so the caller
        records ``SINK_EXHAUSTED`` rather than letting it read as a plain sink.

        A **stall** is deliberately not absorbed here. A stall (the overlay
        suppressing every out-edge at a place that *has* base edges) and a sink
        (the corpus drawing no edge out at all) differ in what they mean — one is
        the verdict speaking, the other is the corpus — so the stall keeps its
        existing treatment (§3.5)."""
        if next_place is not None:
            return next_place, False
        if not self.retrace_sinks:
            return None, False
        if not self.routing.is_sink(place):
            return None, False  # a stall, not a sink — not this policy's business
        target = self._retrace_target(place)
        if target is None:
            return None, True
        self._retrace_pending = True
        return target, False

    def _retrace_target(self, sink: str) -> str | None:
        """The place to step back to, walking the token's own visited chain.

        Normally this is the immediate predecessor. It walks further back only in
        the degenerate case where suppressing the edge just travelled would leave a
        predecessor with no positive mass at all — which no profile net can reach
        today (every sink predecessor keeps five to eleven alternatives, §3.1), but
        which is handled rather than assumed away. Sets the one-shot suppression as
        a side effect; returns None when the chain is exhausted.

        The mass test is against the **base** weights: a predecessor whose base
        out-set survives the suppression can still stall on a verdict, and a stall
        is the other mechanism's to handle."""
        child = sink
        for index in range(len(self._visited) - 2, -1, -1):
            predecessor = self._visited[index]
            base = self.routing.base_out_weights(predecessor)
            remaining = {d: w for d, w in base.items() if d != child and w > 0}
            if remaining:
                self._suppressed_edge = (predecessor, child)
                return predecessor
            child = predecessor
        return None

    def _take_retrace_flag(self) -> bool:
        """Consume the pending retrace flag at the **top** of the next iteration.

        The flag is set while the *sink's* record is still being built, so it must
        not be consumed by that record — it belongs to the visit the token
        retraced *into*. Taking it one iteration later is what makes the record
        stream say "this visit happened because the token stepped back", which is
        the claim the flag exists to support.

        ``retrace_count`` increments here rather than at the decision, so the
        counter means "retraced visits that actually happened": a retrace chosen
        an instant before the sim ends produces no visit and is not counted, and
        the count therefore always equals the number of flagged records."""
        flag = self._retrace_pending
        self._retrace_pending = False
        if flag:
            self.retrace_count += 1
        return flag

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
        place_class: str = ACTION_BEARING,
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
                place_class=place_class,
                n_compromised=self._n_compromised(),
            )
        )


__all__ = [
    "Verdict",
    "VerdictAdapter",
    "OutcomeOverlayLike",
    "MovementRecord",
    "MovementAttacker",
    "InterruptSource",
    "NO_INTERRUPT",
    "TimingSource",
    "load_dwell_catalogue",
    "DURATIONS_PATH",
    "ACTION_BEARING",
    "DWELL_ONLY",
    "DWELL_PROCESS",
]
