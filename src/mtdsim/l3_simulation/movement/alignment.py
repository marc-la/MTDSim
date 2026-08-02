"""The FSM-alignment overlay — a declared dial from CTI order to the substrate's
procedural order (routing factor 8 in the composition register).

**This factor scores no axis of the APT criterion, and its record says so in its
own first paragraph.** Axis 6 (incentive rationality) is closed as DESIGNED with
both attempted implementations recorded as negative results, and nothing here
re-opens it; axis 4 is adaptivity to the *defender* and this responds to the
*substrate*; and it is not a fidelity improvement, because at the limiting end it
tunes the attacker toward the host simulator's own procedural order, which is the
opposite of behavioural independence. It is an **instrument**: a dial whose sweep
converts the coupling finding — that walking CTI order manufactures failure the
inherited attacker never meets — into a measured quantity, on this project's own
substrate, with a null arm that reproduces every recorded figure at full strength
(``model_scope_freeze.md`` §5).

The rule, at a routing decision at ``src`` over its out-set:

    d(b | held)  =  0                       if b's verb is objective-productive
                                            and legal in the held capabilities
                 =  1 + D(held ∘ verb(b))   if b's verb is legal but not productive
                 =  1 + D(held)             if b's verb is blocked, or b dispatches
                                            no verb at all
    d*           =  min over the out-set
    m(a→b)       =  1.0        if d(b) == d*
                 =  (1 − α)    otherwise

where ``D(held)`` is the number of legal verb applications separating the
attacker's current capability state from one in which *some* objective-productive
verb would run. At **α = 0** every factor is 1.0, the modulator returns nothing at
all, and the run is bit-identical to one with no state attached. At **α = 1**
every non-minimal candidate is zeroed, so transitions are limited to those on a
shortest path to a productive action. Intermediate α still tries other things and
tends toward the substrate's FSM structure.

**MTD enters as a set contraction, not a scalar surcharge.** A network-layer
mutation clears ``curr_host``, ``curr_ports`` and ``foothold`` per the declared
relation, so the legal verb set contracts from six to two and ``D`` regresses from
0 to 1. That is the non-proportional response a normalised utility *ratio* could
not see, and it is the reason this shape is worth building where the ratio was
not.

**What is consumed, and what is declared here.**

- The **precondition relation** (composition-register factor 6,
  ``data/ogasp/controller/precondition_relation.json``) supplies the capability
  closure the distance is computed over. Consumed unchanged and unbumped.
- The **tactic-to-verb mapping** (factor 5) says which verb a place dispatches.
  Consumed unchanged.
- The **objective-productive verb set** (:data:`OBJECTIVE_VERBS`) is transcribed
  from the substrate, exactly as the relation itself was, with its locators
  below. It declares no magnitude.
- **α** is the one declared parameter, with a tier, a band and a sweep, in
  ``data/ogasp/movement/alignment_rules.json``.

**The claims this factor may not carry**, repeated because each is one a reader
will be tempted to make: it is not learning (no accumulation, no belief, no update
from experience — a declared bias over a static lookup); it is not axis 4; and it
is not a fidelity improvement. Any statement about its MTD response is confined to
the **position-destroying** defence family — what OS and Service Diversity destroy
lives outside the guard the capability vocabulary was transcribed from, so the
declared relation gives them no channel at all
(``docs/handoffs/2026-08-02_os_service_diversity_indistinguishability.md``).

**Determinism (SIM-05).** The factor is a deterministic function of the declared
artefacts and the attacker's own trajectory. It draws from no random stream, so
the state's fourth stream stays unused.

Design record: ``docs/implementation/pipeline/ogasp/fsm_alignment_overlay.md``.
Rules and ledger: ``data/ogasp/movement/alignment_rules.json``.
"""
from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from mtdsim.l3_simulation.movement.learning_readiness import (
    PRECONDITION_PATH,
    PreconditionModel,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
ALIGNMENT_RULES_PATH = (
    _REPO_ROOT / "data" / "ogasp" / "movement" / "alignment_rules.json"
)

#: The substrate verbs whose success is a step toward the simulator's own
#: termination condition (``terminate_compromise_ratio × total_nodes``). Read off
#: the call sites of ``AttackOperation.update_compromise_progress``:
#:
#:   * ``attack_operation.py:408`` — ``_do_scan_port``, on a credential-reuse hit;
#:   * ``attack_operation.py:513`` — ``_do_exploit_vuln``, on ``check_compromised()``;
#:   * ``attack_operation.py:547`` — ``_do_brute_force``, on a guessed login.
#:
#: The fourth call site, ``attack_operation.py:377`` in ``_do_enum_host``, is
#: guarded by ``if curr_host.compromised`` — it re-reports a host the attacker
#: already owns and causes no compromise, so ``ENUM_HOST`` is deliberately **not**
#: a target.
#:
#: **This set is substrate-specific knowledge, and by the seam rule
#: (``modulator_composition.md`` §3) that makes it a controller-seam declaration
#: living in movement-layer code.** It is here rather than in the precondition
#: relation because this factor's brief consumes that artefact *unchanged and
#: unbumped*, and adding a field to it would be neither. The impurity is recorded
#: rather than hidden, and it is bounded: it is one three-element transcription an
#: adopter re-declares alongside factors 5 and 6, and it is a constructor argument
#: so a port states it rather than inheriting it.
OBJECTIVE_VERBS: frozenset[str] = frozenset(
    {"SCAN_PORT", "EXPLOIT_VULN", "BRUTE_FORCE"}
)

#: Returned by :meth:`ObjectiveDistance.steps_to_capable` when no sequence of legal
#: verbs reaches a state in which any objective-productive verb would run. Not
#: reachable under the declared relation (``SCAN_HOST`` requires nothing, so the
#: closure is connected from every state), but handled rather than assumed away —
#: an adopter's relation may not have that property.
UNREACHABLE = 1_000_000


class AlignmentError(ValueError):
    """Raised when the declared artefacts cannot produce a distance — an
    objective verb the relation does not carry, or a mapping naming a verb the
    relation does not know."""


# --- the distance model -----------------------------------------------------


@dataclass(frozen=True)
class ObjectiveDistance:
    """Shortest-path distance to a productive action over the declared
    precondition relation's capability closure.

    A pure function of two declared artefacts and a capability set. It reads no
    substrate state and holds no run state, so it is shared, cached and trivially
    testable; the *cursor* that tracks what the attacker holds is
    :class:`CapabilityCursor`, and the two are separate on purpose.
    """

    model: PreconditionModel
    objective_verbs: frozenset[str]

    @classmethod
    def load(
        cls,
        *,
        precondition_path: Path | str = PRECONDITION_PATH,
        objective_verbs: Iterable[str] = OBJECTIVE_VERBS,
    ) -> "ObjectiveDistance":
        return cls.of(
            PreconditionModel.load(precondition_path), objective_verbs=objective_verbs
        )

    @classmethod
    def of(
        cls,
        model: PreconditionModel,
        *,
        objective_verbs: Iterable[str] = OBJECTIVE_VERBS,
    ) -> "ObjectiveDistance":
        verbs = frozenset(objective_verbs)
        unknown = verbs - set(model.requires)
        if unknown:
            raise AlignmentError(
                f"objective verb(s) {sorted(unknown)} are not carried by the "
                f"precondition relation (version {model.version!r}); the target "
                "set and the closure must be stated over the same vocabulary"
            )
        if not verbs:
            raise AlignmentError(
                "the objective verb set is empty — every candidate would sit at "
                "the same distance and the dial would do nothing"
            )
        return cls(model=model, objective_verbs=verbs)

    # -- the closure ---------------------------------------------------------
    def apply(self, verb: str, held: frozenset[str]) -> frozenset[str]:
        """The capability state after ``verb`` runs in ``held`` — produce, then
        clear, in the relation's own order."""
        return (held | self.model.produces[verb]) - self.model.clears[verb]

    def legal_verbs(self, held: frozenset[str]) -> tuple[str, ...]:
        """The verbs whose declared precondition ``held`` satisfies."""
        return tuple(
            sorted(v for v in self.model.requires if self.model.requires[v] <= held)
        )

    def is_capable(self, held: frozenset[str]) -> bool:
        """Would *some* objective-productive verb run right now?"""
        return any(self.model.requires[v] <= held for v in self.objective_verbs)

    def steps_to_capable(self, held: frozenset[str]) -> int:
        """``D(held)`` — the fewest legal verb applications separating ``held``
        from a state in which some objective-productive verb would run; 0 when one
        already would. Breadth-first over the capability closure, which is finite
        (2^|capabilities|) and tiny."""
        start = frozenset(held)
        if self.is_capable(start):
            return 0
        seen = {start}
        frontier: deque[tuple[frozenset[str], int]] = deque([(start, 0)])
        while frontier:
            state, depth = frontier.popleft()
            for verb in self.legal_verbs(state):
                nxt = self.apply(verb, state)
                if nxt in seen:
                    continue
                if self.is_capable(nxt):
                    return depth + 1
                seen.add(nxt)
                frontier.append((nxt, depth + 1))
        return UNREACHABLE

    def distance(self, verb: str | None, held: frozenset[str]) -> int:
        """``d(b | held)`` for a candidate whose place dispatches ``verb``.

        Three cases, and the third is the one that carries the model's opinion. A
        productive verb that would run *now* is at distance 0. A legal but
        unproductive verb costs its own step and is then scored from the state it
        produces, so reconnaissance is cheap exactly when it is enabling. A verb
        the substrate would refuse, and a place that dispatches nothing at all,
        both cost a step and leave the state where it was — which is what makes a
        blocked attempt strictly worse than any move that advances, and a
        dwell-only place no better than a blocked one.
        """
        if verb is None:
            return 1 + self.steps_to_capable(held)
        if verb not in self.model.requires:
            raise AlignmentError(
                f"the mapping dispatches {verb!r}, which the precondition "
                f"relation (version {self.model.version!r}) does not carry"
            )
        if not self.model.requires[verb] <= held:
            return 1 + self.steps_to_capable(held)
        if verb in self.objective_verbs:
            return 0
        return 1 + self.steps_to_capable(self.apply(verb, held))

    def table(self, tactic_to_verb: Mapping[str, str | None]) -> dict[
        frozenset[str], dict[str, int]
    ]:
        """The complete ``held -> tactic -> d`` table over every subset of the
        declared capabilities — the artefact the design record reports and the
        stall check reads. Complete rather than reachable-only, for the same
        reason the declared families author their whole value space."""
        capabilities = sorted(
            {c for s in self.model.produces.values() for c in s}
            | {c for s in self.model.requires.values() for c in s}
        )
        states: list[frozenset[str]] = []
        for mask in range(1 << len(capabilities)):
            states.append(
                frozenset(c for i, c in enumerate(capabilities) if mask >> i & 1)
            )
        return {
            held: {
                tactic: self.distance(verb, held)
                for tactic, verb in tactic_to_verb.items()
            }
            for held in states
        }


# --- the capability cursor --------------------------------------------------


class CapabilityCursor:
    """What the attacker currently holds, tracked from its own trajectory.

    Deliberately a **separate copy** of the tracking rule the readiness learner
    carries inline (``learning_readiness.py``), not a refactor of it: that
    mechanism's figures are on record, and every factor being self-contained is
    what keeps each one independently ablatable. The drift risk that duplication
    creates is answered by a test that drives both over the same run and asserts
    the two cursors agree at every step, which is a stronger guarantee than shared
    code would give — it checks agreement of *behaviour*, not of source.

    Nothing here reads substrate state. The cursor advances against the declared
    relation and the attacker's own dispatches, which is what keeps the
    scheme-awareness exclusion untouched.
    """

    def __init__(
        self, model: PreconditionModel, tactic_to_verb: Mapping[str, str | None]
    ) -> None:
        self.model = model
        self.tactic_to_verb = dict(tactic_to_verb)
        self.held: frozenset[str] = frozenset()
        self._pending: tuple[str, bool] | None = None

    def observe_visit(self, place: str) -> None:
        """The token has entered ``place`` and is about to act. Stash the
        readiness bit computed *before* this place's own effect — an MTD interrupt
        can land between the visit and the verdict, and the verb either ran or did
        not in the state it was dispatched from."""
        verb = self.tactic_to_verb.get(place)
        self._pending = (place, self.model.is_ready(verb, self.held))

    def observe_verdict(self, place: str, verdict: str) -> None:
        """Apply the place's capability effect. Gated on the verb having actually
        run: a dispatch whose precondition was unmet is blocked and produces
        nothing, which is why production hangs off the stashed readiness bit."""
        ready = (
            self._pending[1]
            if self._pending and self._pending[0] == place
            else self.model.is_ready(self.tactic_to_verb.get(place), self.held)
        )
        verb = self.tactic_to_verb.get(place)
        if verb is not None and ready:
            self.held = (self.held | self.model.produces[verb]) - self.model.clears[
                verb
            ]
        self._pending = None

    def observe_mtd_interrupt(self, resource_type: str = "") -> None:
        """The defence severs what the declared relation says it severs — a
        network-layer mutation clears the host cursor and the foothold, an
        application-layer one clears nothing structural."""
        self.held -= self.model.mtd_clears.get(resource_type, frozenset())


# --- the declared parameter -------------------------------------------------


@dataclass(frozen=True)
class AlignmentParameters:
    """The declared parameter and its band, read from the rules artefact."""

    alpha: float
    sweep: tuple[float, ...]
    off_floor: float
    version: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "alpha": self.alpha,
            "sweep": list(self.sweep),
            "off_floor": self.off_floor,
            "version": self.version,
        }


def load_alignment_parameters(
    path: Path | str = ALIGNMENT_RULES_PATH,
) -> AlignmentParameters:
    """Read α, its sweep band and the off-band floor from the declared rules."""
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    declared = doc["declared_parameters"]
    alpha = declared["alpha"]
    return AlignmentParameters(
        alpha=float(alpha["value"]),
        sweep=tuple(float(a) for a in alpha["sweep"]),
        off_floor=float(doc["model"]["off_band"]["floor"]),
        version=str(doc["meta"]["version"]),
    )


# --- the modulator ----------------------------------------------------------


class FsmAlignmentModulator:
    """Routing factor 8 — the declared bias toward the substrate's procedural order.

    Registered on an :class:`~mtdsim.l3_simulation.movement.state.AttackerState`
    exactly as factors 3 and 4 are. Constructed per run, not per profile: the
    distance model is profile-independent, which is the one respect in which this
    factor is cheaper than the utility one — there is no per-profile table to
    declare and none to reproduce.

    ``may_zero`` is set **per instance** rather than declared once for the class,
    and that is deliberate. Below the limiting end the off-band multiplier is
    strictly positive, so the seam's stall guard stays a live proof for every arm
    of the sweep except the one that actually needs the licence; only at α = 1
    (with no floor) does the instance claim it. The exhaustive check that licenses
    it is :func:`stall_report`.
    """

    name = "fsm-alignment"

    def __init__(
        self,
        *,
        alpha: float,
        tactic_to_verb: Mapping[str, str | None],
        precondition_model: PreconditionModel | None = None,
        objective_verbs: Iterable[str] = OBJECTIVE_VERBS,
        off_floor: float = 0.0,
    ) -> None:
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"alpha must lie in [0, 1], got {alpha!r}")
        if not 0.0 <= off_floor < 1.0:
            raise ValueError(
                f"off_floor must lie in [0, 1), got {off_floor!r}; it exists to "
                "keep the off-band multiplier above zero, not to replace it"
            )
        model = precondition_model or PreconditionModel.load()
        self.alpha = float(alpha)
        self.off_floor = float(off_floor)
        self.distances = ObjectiveDistance.of(model, objective_verbs=objective_verbs)
        self.cursor = CapabilityCursor(model, tactic_to_verb)
        self.tactic_to_verb = dict(tactic_to_verb)
        #: The off-band multiplier — what a candidate off every shortest path is
        #: worth. Zero exactly at α = 1 with no floor, which is the only case
        #: needing the seam's zero licence.
        self.off = max(1.0 - self.alpha, self.off_floor)
        self.may_zero = self.off <= 0.0
        #: Per-decision bookkeeping, for narration and the sweep's own log.
        self.decisions: int = 0
        self.singleton_decisions: int = 0
        self.suppressed: int = 0

    @classmethod
    def declared(
        cls,
        *,
        tactic_to_verb: Mapping[str, str | None],
        alpha: float | None = None,
        rules_path: Path | str = ALIGNMENT_RULES_PATH,
        precondition_path: Path | str = PRECONDITION_PATH,
    ) -> "FsmAlignmentModulator":
        """The factor at its declared α — the arm an experiment runs. ``alpha``
        overrides it so a sweep moves the one parameter without a file on disk."""
        params = load_alignment_parameters(rules_path)
        return cls(
            alpha=params.alpha if alpha is None else float(alpha),
            tactic_to_verb=tactic_to_verb,
            precondition_model=PreconditionModel.load(precondition_path),
            off_floor=params.off_floor,
        )

    # -- observation (the state fans these in) -------------------------------
    def observe_visit(self, place: str) -> None:
        self.cursor.observe_visit(place)

    def observe_verdict(self, place: str, verdict: str) -> None:
        self.cursor.observe_verdict(place, verdict)

    def observe_mtd_interrupt(self, resource_type: str = "") -> None:
        self.cursor.observe_mtd_interrupt(resource_type)

    # -- the composition factor ---------------------------------------------
    def distance_of(self, tactic: str) -> int:
        """``d(tactic | held)`` in the attacker's current capability state."""
        return self.distances.distance(
            self.tactic_to_verb.get(tactic), self.cursor.held
        )

    def factors(
        self, state: Any, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        if self.alpha == 0.0:
            return {}  # the null arm — bit-identical to no state at all (gate 1)
        # Only destinations the net gives positive base mass are candidates. A
        # net can carry an out-edge at weight zero, and such an edge is dropped by
        # the composition before this factor's product is applied — so letting one
        # set the minimum would leave every *live* candidate off-band and, at the
        # limiting end, empty the out-set. The check in :func:`stall_report`
        # found exactly that, which is why the restriction is here rather than in
        # the checker alone.
        live = {dst for dst, weight in base_out_weights.items() if weight > 0.0}
        if not live:
            return {}
        distances = {dst: self.distance_of(dst) for dst in live}
        minimum = min(distances.values())
        self.decisions += 1
        if len(live) == 1:
            # A singleton out-set renormalises to 1.0 whatever any factor
            # computes. Counted rather than special-cased, because the share of
            # decisions with no choice to make bounds what any routing factor can
            # possibly do — the same measurement that bounded axis 6.
            self.singleton_decisions += 1
        self.suppressed += sum(1 for d in distances.values() if d > minimum)
        return {
            dst: (1.0 if d == minimum else self.off) for dst, d in distances.items()
        }

    def snapshot(self) -> dict[str, Any]:
        """A compact view of the factor right now, for narration and logs."""
        return {
            "alpha": self.alpha,
            "off": self.off,
            "held": sorted(self.cursor.held),
            "steps_to_capable": self.distances.steps_to_capable(self.cursor.held),
            "decisions": self.decisions,
            "singleton_decisions": self.singleton_decisions,
            "suppressed_candidates": self.suppressed,
        }


# --- the no-stall check -----------------------------------------------------


@dataclass(frozen=True)
class StallFinding:
    """One (profile, mapping, overlay, verdict, source, held) cell in which the
    composed out-set retains no minimal-distance destination — so at α = 1 every
    surviving edge would be zeroed and the walk would stall."""

    profile: str
    mapping_version: str
    overlay_version: str
    verdict: str
    src: str
    held: tuple[str, ...]
    dropped_edge: str | None
    survivors: tuple[str, ...]
    minimal: tuple[str, ...]

    def __str__(self) -> str:  # pragma: no cover - reporting only
        drop = f" (retrace-suppressed {self.dropped_edge})" if self.dropped_edge else ""
        return (
            f"{self.profile}/{self.mapping_version}/{self.overlay_version} "
            f"{self.src} [{self.verdict}] held={list(self.held)}{drop}: "
            f"survivors={list(self.survivors)} minimal={list(self.minimal)}"
        )


def stall_report(
    *,
    profiles: Iterable[str] = (
        "aggregate",
        "double_extortion",
        "infrastructure_setup",
        "pure_impediment",
        "pure_steal",
    ),
    mapping_versions: Iterable[str] = ("v1_ckc_total", "v2_partial"),
    overlay_versions: Iterable[str] | None = None,
    overlays: Mapping[str, Any] | None = None,
    with_synthetic_overlay: bool = True,
    precondition_path: Path | str = PRECONDITION_PATH,
    objective_verbs: Iterable[str] = OBJECTIVE_VERBS,
    include_retrace_suppression: bool = True,
) -> list[StallFinding]:
    """The exhaustive no-stall check across the α band — **static, not sampled**.

    The structural half of the argument is that ``factors`` returns 1.0 for the
    argmin over the out-set it is handed, so at least one candidate always
    survives α = 1. The half that argument misses is that the seam multiplies the
    factors into the distribution the **outcome overlay** already composed, and
    the overlay can hard-suppress a pair with an exact zero. If every
    minimal-distance destination at some decision is a pair the overlay zeroed,
    the surviving candidates are all off-band and α = 1 empties the out-set.

    That hazard is a property of declared data, not of a run, so it is decided by
    enumeration rather than by sampling: every profile net × mapping × overlay
    version × verdict × source place × capability subset, plus (with
    ``include_retrace_suppression``) each one-shot retrace suppression the S5
    policy can apply to an out-set. A run-based check could only ever say the
    stall was not *reached*; this says it is not *reachable*.

    Returns one :class:`StallFinding` per offending cell — an empty list is the
    licence for ``may_zero`` at the limiting end of the band.

    ``overlays`` injects value tables by name in place of the registry, which is
    how the check is itself checked: a checker that cannot be made to fail proves
    nothing, so the suite hands it an overlay built to suppress exactly the
    destinations the distance model would keep.
    """
    from mtdsim.l3_simulation.controller import load_controller, load_outcome_overlay
    from mtdsim.l3_simulation.controller.outcome import load_overlay_registry
    from mtdsim.l3_simulation.movement.attacker import VERDICT_NONE
    from mtdsim.l3_simulation.movement.net import load_routing_net

    if overlays is None and overlay_versions is None:
        overlay_versions = load_overlay_registry().names
    model = PreconditionModel.load(precondition_path)
    distances = ObjectiveDistance.of(model, objective_verbs=objective_verbs)
    verdicts = ("success", "failure", VERDICT_NONE)

    findings: list[StallFinding] = []
    if overlays is None:
        overlays = {
            name: load_outcome_overlay(version=name) for name in overlay_versions or ()
        }
    for mapping_version in mapping_versions:
        t2v = load_controller(version=mapping_version).as_dict()
        by_held = distances.table(t2v)
        for profile in profiles:
            net = load_routing_net(
                profile, with_synthetic_overlay=with_synthetic_overlay
            )
            for src in sorted(net.places):
                # Zero-weight base edges are not candidates — the composition
                # drops them before this factor's product applies, so a zero-weight
                # destination must not be allowed to set the minimum.
                full = {
                    dst: weight
                    for dst, weight in net.base_out_weights(src).items()
                    if weight > 0.0
                }
                if not full:
                    continue  # a sink: no out-set, nothing to zero
                candidate_sets = [(None, full)]
                if include_retrace_suppression and len(full) > 1:
                    for dropped in sorted(full):
                        candidate_sets.append(
                            (dropped, {d: w for d, w in full.items() if d != dropped})
                        )
                for dropped, base_out in candidate_sets:
                    for held, row in by_held.items():
                        distance = {dst: row[dst] for dst in base_out}
                        minimum = min(distance.values())
                        minimal = {d for d, v in distance.items() if v == minimum}
                        for verdict in verdicts:
                            for name, overlay in overlays.items():
                                composed = overlay.compose(src, verdict, dict(base_out))
                                if not composed:
                                    continue  # the overlay's own stall, not ours
                                if set(composed) & minimal:
                                    continue
                                findings.append(
                                    StallFinding(
                                        profile=profile,
                                        mapping_version=mapping_version,
                                        overlay_version=name,
                                        verdict=verdict,
                                        src=src,
                                        held=tuple(sorted(held)),
                                        dropped_edge=dropped,
                                        survivors=tuple(sorted(composed)),
                                        minimal=tuple(sorted(minimal)),
                                    )
                                )
    return findings


def _main(argv: list[str] | None = None) -> int:  # pragma: no cover - CLI
    import argparse

    parser = argparse.ArgumentParser(
        description="Inspect the FSM-alignment distance model, or run the "
        "exhaustive no-stall check that licenses the limiting end of the band."
    )
    parser.add_argument(
        "--table",
        metavar="MAPPING",
        nargs="?",
        const="v2_partial",
        help="print the held -> tactic distance table for a controller mapping",
    )
    parser.add_argument(
        "--check-stalls",
        action="store_true",
        help="enumerate every cell in which alpha = 1 would empty an out-set",
    )
    args = parser.parse_args(argv)
    if not (args.table or args.check_stalls):
        parser.error("pass --table or --check-stalls")

    if args.table:
        from mtdsim.l3_simulation.controller import load_controller

        t2v = load_controller(version=args.table).as_dict()
        distances = ObjectiveDistance.load()
        table = distances.table(t2v)
        tactics = sorted(t2v)
        for held in sorted(table, key=lambda s: (len(s), sorted(s))):
            legal = distances.legal_verbs(held)
            print(
                f"held={sorted(held) or '—'}  legal={len(legal)}  "
                f"D={distances.steps_to_capable(held)}"
            )
            for tactic in tactics:
                print(f"    {table[held][tactic]}  {tactic} -> {t2v[tactic]}")

    if args.check_stalls:
        findings = stall_report()
        print(f"no-stall check: {len(findings)} offending cell(s)")
        for finding in findings[:20]:
            print(f"    {finding}")
        if len(findings) > 20:
            print(f"    … and {len(findings) - 20} more")
        if findings:
            print(
                "\nNO-STALL CHECK FAILED — alpha = 1 can empty an out-set. The band's "
                "limiting end needs the declared off-band floor, and must be reported "
                "as near-limiting rather than limiting."
            )
            return 1
        print(
            "\nno-stall check passed: every composed out-set retains at least one "
            "minimal-distance destination, so alpha = 1 is reachable"
        )
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(_main())


__all__ = [
    "ALIGNMENT_RULES_PATH",
    "OBJECTIVE_VERBS",
    "UNREACHABLE",
    "AlignmentError",
    "AlignmentParameters",
    "CapabilityCursor",
    "FsmAlignmentModulator",
    "ObjectiveDistance",
    "StallFinding",
    "load_alignment_parameters",
    "stall_report",
]
