"""The FSM-succession overlay — composition-register factor 9.

**This factor scores no axis of the APT criterion**, for the same three reasons
its predecessor does not
([`fsm_alignment_overlay.md`](../../../../docs/implementation/pipeline/ogasp/fsm_alignment_overlay.md)):
it is not learning, it is not adaptivity to the *defender*, and it is not a
fidelity improvement — at its limiting end it makes the attacker behave more like
the host simulator expects, which is the opposite of behavioural independence. It
is a **declared comparability concession**: the substrate we inherit carries a
rigid finite-state attacker, and a CTI-derived attacker walking a different order
is penalised by that rigidity in ways that have nothing to do with the defence.
α buys that penalty off by a declared amount so the two attackers are relatively
comparable.

**Why this supersedes factor 8.** Factor 8 asked *"how far is this candidate from
being able to act productively?"* over the capability closure. The sweep measured
what that target rewards: at α = 1 the attacker reached a state of permanent
readiness on a single host it already owned, because being *able* to attack is not
the same as getting anywhere. The inherited FSM does not have that defect — its
successor after a compromise is `SCAN_NEIGHBOR` and then `ENUM_HOST`, so it
pivots. Conditioning on the FSM's own succession therefore inherits its progress
structure instead of re-deriving a worse one.

The rule, at a routing decision:

    targets  =  the verbs the inherited FSM licenses next, given the verb just
                run and the verdict it returned (or, if that action was
                interrupted, given the mutating resource's layer)

    m(a→b)   =  1.0        b dispatches no verb at all (dwell-only places are
                           transparent — they fire nothing, so they cannot
                           violate the succession)
             =  1.0        b's verb is in `targets`
             =  (1 − α)    otherwise

At **α = 0** the modulator returns no factors and the run is bit-identical to one
with no state attached. At **α = 1** every destination that would fire an
off-succession verb is zeroed, and the attacker moves only through its own
dwell-only structure and the FSM's licensed next actions. α is a **float** over
[0, 1]; nothing about the mechanism privileges the endpoints.

**Two models compose here, and the seam between them is declared.** The
succession relation says *what comes next*; the precondition relation's capability
closure says *what must happen first* when what comes next cannot run. If none of
the FSM's licensed successors is runnable in the attacker's current capability
state, the target set becomes the verbs on a shortest route to making one of them
runnable. Without that fallback the dial would drive the token at a dispatch the
substrate refuses, which is the failure factor 8's sweep measured at its limiting
end.

**Determinism (SIM-05).** A pure function of the declared artefacts and the
attacker's own trajectory; no random stream is drawn.

Design record: ``docs/implementation/pipeline/ogasp/fsm_succession_overlay.md``.
Relation: ``data/ogasp/controller/fsm_succession.json`` (controller seam).
Rules and ledger: ``data/ogasp/movement/succession_rules.json``.
"""
from __future__ import annotations

import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from mtdsim.l3_simulation.movement.alignment import AlignmentError, CapabilityCursor
from mtdsim.l3_simulation.movement.learning_readiness import (
    PRECONDITION_PATH,
    PreconditionModel,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
SUCCESSION_PATH = (
    _REPO_ROOT / "data" / "ogasp" / "controller" / "fsm_succession.json"
)
SUCCESSION_RULES_PATH = (
    _REPO_ROOT / "data" / "ogasp" / "movement" / "succession_rules.json"
)

#: The verdict a dwell-only place raises — no verb ran, so the FSM did not
#: advance. Kept local so this module reads no driver code.
VERDICT_NONE = "none"


# --- the declared relation (controller seam) --------------------------------


@dataclass(frozen=True)
class FsmSuccession:
    """The inherited attacker's verdict-conditioned successor relation.

    Loaded from the tracked controller artefact. Pure lookups — it reads no
    substrate state and declares what the *host simulator's own* attacker does
    next, which is public in the papers, so the scheme-awareness exclusion is
    untouched.

    Every successor is a **set**, not a single verb, and that is load-bearing
    rather than defensive generality. The movement layer's verdict adapter treats
    ``ENUM_HOST``, ``SCAN_PORT`` and ``SCAN_NEIGHBOR`` as success-unless-
    interrupted, so for two of them the substrate's own branch is *not
    recoverable* from the verdict this modulator sees. Declaring both successors
    in that case is more honest than picking the modal one, and it widens the
    permitted set rather than narrowing it — so the ambiguity cannot manufacture
    an alignment the FSM does not license.
    """

    entry: str
    succession: Mapping[str, Mapping[str, frozenset[str]]]
    interrupt: Mapping[str, frozenset[str]]
    progressive: frozenset[str]
    version: str

    @classmethod
    def load(cls, path: Path | str = SUCCESSION_PATH) -> "FsmSuccession":
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
        succession = {
            verb: {
                verdict: frozenset(row[verdict])
                for verdict in ("success", "failure")
            }
            for verb, row in doc["succession"].items()
        }
        interrupt = {
            key: frozenset(value)
            for key, value in doc["interrupt_succession"].items()
            if isinstance(value, list)
        }
        return cls(
            entry=str(doc["entry"]),
            succession=succession,
            interrupt=interrupt,
            progressive=frozenset(doc["progressive_verbs"]),
            version=str(doc["meta"]["version"]),
        )

    def validate_against(self, model: PreconditionModel) -> None:
        """Refuse a relation stated over a different verb vocabulary than the
        precondition relation's — loud at construction rather than a quiet
        miscount at every routing decision."""
        known = set(model.requires)
        named = {self.entry} | set(self.succession) | self.progressive
        for row in self.succession.values():
            for successors in row.values():
                named |= set(successors)
        for successors in self.interrupt.values():
            named |= set(successors)
        unknown = named - known
        if unknown:
            raise AlignmentError(
                f"the succession relation (version {self.version!r}) names "
                f"verb(s) {sorted(unknown)} that the precondition relation "
                f"(version {model.version!r}) does not carry; the two controller "
                "artefacts must be stated over the same vocabulary"
            )

    def next_verbs(self, verb: str, verdict: str) -> frozenset[str]:
        """The verbs the FSM licenses after ``verb`` returned ``verdict``."""
        try:
            row = self.succession[verb]
        except KeyError as exc:
            raise AlignmentError(
                f"no declared succession for verb {verb!r} in relation "
                f"{self.version!r}"
            ) from exc
        # The binary vocabulary is success/failure; anything else is a movement
        # layer artefact and is read as failure, which is what the driver's own
        # un-actionable policy does.
        return row["success"] if verdict == "success" else row["failure"]

    def after_interrupt(self, resource: str) -> frozenset[str]:
        """The verb the substrate's interrupt handler restarts with, by the
        mutating resource's layer. An unrecorded resource restarts at the entry
        verb rather than silently licensing everything."""
        return self.interrupt.get(resource) or frozenset({self.entry})


# --- the declared parameter -------------------------------------------------


@dataclass(frozen=True)
class SuccessionParameters:
    """The declared parameter and its band, read from the rules artefact."""

    alpha: float
    sweep: tuple[float, ...]
    off_floor: float
    version: str


def load_succession_parameters(
    path: Path | str = SUCCESSION_RULES_PATH,
) -> SuccessionParameters:
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    alpha = doc["declared_parameters"]["alpha"]
    return SuccessionParameters(
        alpha=float(alpha["value"]),
        sweep=tuple(float(a) for a in alpha["sweep"]),
        off_floor=float(doc["model"]["off_band"]["floor"]),
        version=str(doc["meta"]["version"]),
    )


# --- the modulator ----------------------------------------------------------


class FsmSuccessionModulator:
    """Routing factor 9 — the declared concession to the inherited FSM's rigidity.

    Registered on an :class:`~mtdsim.l3_simulation.movement.state.AttackerState`
    exactly as factors 3, 4 and 8 are, and profile-independent for the same reason
    factor 8 is: the succession is a property of the substrate, not of the
    campaign. ``may_zero`` is declared **per instance**, so the seam's stall guard
    stays a live proof for every arm except the one that needs the licence.
    """

    name = "fsm-succession"

    def __init__(
        self,
        *,
        alpha: float,
        tactic_to_verb: Mapping[str, str | None],
        succession: FsmSuccession | None = None,
        precondition_model: PreconditionModel | None = None,
        off_floor: float = 0.0,
    ) -> None:
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"alpha must lie in [0, 1], got {alpha!r}")
        if not 0.0 <= off_floor < 1.0:
            raise ValueError(f"off_floor must lie in [0, 1), got {off_floor!r}")
        self.alpha = float(alpha)
        self.off_floor = float(off_floor)
        self.off = max(1.0 - self.alpha, self.off_floor)
        self.may_zero = self.off <= 0.0

        self.model = precondition_model or PreconditionModel.load()
        self.fsm = succession or FsmSuccession.load()
        self.fsm.validate_against(self.model)
        self.tactic_to_verb = dict(tactic_to_verb)
        unknown = {v for v in self.tactic_to_verb.values() if v is not None} - set(
            self.model.requires
        )
        if unknown:
            raise AlignmentError(
                f"the mapping dispatches {sorted(unknown)}, which the precondition "
                f"relation (version {self.model.version!r}) does not carry"
            )
        self.cursor = CapabilityCursor(self.model, tactic_to_verb)
        #: The verbs the FSM currently licenses. A run opens at the entry verb,
        #: which is where the inherited attacker opens.
        self.targets: frozenset[str] = frozenset({self.fsm.entry})
        self._pending_interrupt: str | None = None
        #: Bookkeeping for narration and the sweep's log.
        self.decisions: int = 0
        self.singleton_decisions: int = 0
        self.suppressed: int = 0
        self.fallbacks: int = 0
        self.abstentions: int = 0

    @classmethod
    def declared(
        cls,
        *,
        tactic_to_verb: Mapping[str, str | None],
        alpha: float | None = None,
        rules_path: Path | str = SUCCESSION_RULES_PATH,
    ) -> "FsmSuccessionModulator":
        """The factor at its declared α — the arm an experiment runs. ``alpha``
        overrides it so a sweep moves the one parameter without a file on disk."""
        params = load_succession_parameters(rules_path)
        return cls(
            alpha=params.alpha if alpha is None else float(alpha),
            tactic_to_verb=tactic_to_verb,
            off_floor=params.off_floor,
        )

    # -- observation (the state fans these in) -------------------------------
    def observe_visit(self, place: str) -> None:
        self.cursor.observe_visit(place)

    def observe_mtd_interrupt(self, resource_type: str = "") -> None:
        """The defence severs what the declared relation says it severs, and the
        substrate's interrupt handler — not its FSM dispatch — decides what runs
        next. Stashed here and consumed at the verdict, which is the causal order
        the substrate uses."""
        self.cursor.observe_mtd_interrupt(resource_type)
        self._pending_interrupt = resource_type

    def observe_verdict(self, place: str, verdict: str) -> None:
        """Advance the capability cursor, then advance the FSM state.

        Three cases, in precedence order. An **interrupt** overrides everything,
        because the substrate's own handler overrides its dispatch. A **dwell-only**
        place fires no verb, so the FSM did not advance and the target set is
        carried forward unchanged — which is exactly what makes such places
        transparent. Otherwise the verb ran and its verdict selects the successor.
        """
        self.cursor.observe_verdict(place, verdict)
        if self._pending_interrupt is not None:
            self.targets = self.fsm.after_interrupt(self._pending_interrupt)
            self._pending_interrupt = None
            return
        verb = self.tactic_to_verb.get(place)
        if verb is None:
            return  # dwell-only: the FSM state is unchanged
        self.targets = self.fsm.next_verbs(verb, verdict)

    # -- the target set, with the capability fallback -------------------------
    def _enabling_verbs(self, targets: frozenset[str]) -> frozenset[str]:
        """The first-step verbs on a shortest route from the held capabilities to
        a state in which some verb of ``targets`` would run.

        Breadth-first over the precondition relation's capability closure, which
        is finite and tiny. Returns every verb that opens *a* shortest route, so
        the fallback is as plural as the closure allows. An empty result means no
        route exists, and the caller then attenuates nothing rather than zeroing
        the whole out-set.
        """
        held = self.cursor.held
        requires, produces, clears = (
            self.model.requires,
            self.model.produces,
            self.model.clears,
        )

        def legal(state: frozenset[str]) -> tuple[str, ...]:
            return tuple(sorted(v for v in requires if requires[v] <= state))

        def satisfied(state: frozenset[str]) -> bool:
            return any(requires[t] <= state for t in targets)

        best: int | None = None
        openers: set[str] = set()
        seen = {held}
        frontier: deque[tuple[frozenset[str], int, str | None]] = deque(
            [(held, 0, None)]
        )
        while frontier:
            state, depth, opener = frontier.popleft()
            if best is not None and depth >= best:
                continue
            for verb in legal(state):
                nxt = (state | produces[verb]) - clears[verb]
                first = opener if opener is not None else verb
                if satisfied(nxt):
                    if best is None or depth + 1 < best:
                        best, openers = depth + 1, {first}
                    elif depth + 1 == best:
                        openers.add(first)
                    continue
                if nxt in seen:
                    continue
                seen.add(nxt)
                frontier.append((nxt, depth + 1, first))
        return frozenset(openers)

    def effective_targets(self, *, count: bool = True) -> frozenset[str]:
        """The verbs this decision actually aims at.

        The FSM's licensed successors when any of them can run; otherwise the
        verbs that make one of them runnable. The fallback is what stops the dial
        driving the token at a dispatch the substrate would refuse.
        """
        return self._resolve(self.targets, count=count)

    def licensed_now(self, *, count: bool = True) -> frozenset[str]:
        """The licensed verbs **as of right now**, for a reader that consults the
        FSM state *between* verdicts — the token-hold rule (T1).

        Identical to :meth:`effective_targets` except that an MTD interrupt
        observed since the last verdict is honoured immediately: the substrate's
        own handler overrides its dispatch the moment it is hit, so a hold that
        is interrupted must aim at the interrupt table's restart verb rather
        than at the stale successors of the verb that ran. ``factors`` never
        sees a pending interrupt (the state consumes it at the verdict that
        precedes every composition), so factor 9's arithmetic is untouched.
        """
        base = (
            self.fsm.after_interrupt(self._pending_interrupt)
            if self._pending_interrupt is not None
            else self.targets
        )
        return self._resolve(base, count=count)

    def _resolve(self, targets: frozenset[str], *, count: bool) -> frozenset[str]:
        held = self.cursor.held
        runnable = {v for v in targets if self.model.requires[v] <= held}
        if runnable:
            return frozenset(runnable)
        if count:
            # `count=False` is how :meth:`snapshot` reads this without moving the
            # counter — an introspection call that mutated bookkeeping would
            # inflate the reported fallback rate by one per snapshot.
            self.fallbacks += 1
        return self._enabling_verbs(targets)

    # -- the composition factor ---------------------------------------------
    def factors(
        self, state: Any, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        if self.alpha == 0.0:
            return {}  # the null arm — bit-identical to no state at all
        live = {dst for dst, weight in base_out_weights.items() if weight > 0.0}
        if not live:
            return {}
        targets = self.effective_targets()
        permitted = {
            dst
            for dst in live
            if self.tactic_to_verb.get(dst) is None
            or self.tactic_to_verb.get(dst) in targets
        }
        self.decisions += 1
        if len(live) == 1:
            self.singleton_decisions += 1
        if not permitted:
            # **The abstention rule.** Where the net offers no FSM-legal move at
            # all, this factor attenuates nothing. Two reasons, and the second is
            # the substantive one. It makes a stall structurally impossible rather
            # than merely unobserved — the out-set can never be emptied, because
            # the only configuration that could empty it is the one in which the
            # factor declines to act. And it is what keeps the mechanism a
            # *concession* rather than a replacement: where the CTI structure
            # offers nothing the inherited FSM would sanction, forcing the token
            # through would not align the attacker, it would silence it.
            self.abstentions += 1
            return {}
        out: dict[str, float] = {}
        for dst in live:
            allowed = dst in permitted
            out[dst] = 1.0 if allowed else self.off
            self.suppressed += 0 if allowed else 1
        return out

    def snapshot(self) -> dict[str, Any]:
        return {
            "alpha": self.alpha,
            "off": self.off,
            "relation": self.fsm.version,
            "held": sorted(self.cursor.held),
            "targets": sorted(self.targets),
            "effective_targets": sorted(self.effective_targets(count=False)),
            "decisions": self.decisions,
            "singleton_decisions": self.singleton_decisions,
            "suppressed_candidates": self.suppressed,
            "capability_fallbacks": self.fallbacks,
            "abstentions": self.abstentions,
        }


# --- the token-hold rule (register T1) --------------------------------------


@dataclass(frozen=True)
class TokenHoldParameters:
    """The hold rule's one declared parameter, read from the rules artefact."""

    max_consecutive_holds: int
    version: str


def load_token_hold_parameters(
    path: Path | str = SUCCESSION_RULES_PATH,
) -> TokenHoldParameters:
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    block = doc["token_hold"]["declared_parameters"]["max_consecutive_holds"]
    return TokenHoldParameters(
        max_consecutive_holds=int(block["value"]),
        version=str(doc["token_hold"]["version"]),
    )


class TokenHoldRule:
    """The token-hold rule — Jin's fix (register **T1**, 2026-08-25) in its
    *opaque* reading, as a declared variant beside factor 9 rather than a
    repair of it.

    **What it is.** When the net's draw lands on a place whose verb the
    inherited FSM does not license from the attacker's current state, the token
    is held where it is: it pays one more dwell draw at the current place and
    draws again, until the draw lands on a place whose verb *is* licensed.
    Dwell-only places are held out too — a draw onto one is a hold, not a
    visit — which is what makes this the opaque hold and not factor 9's α = 1
    point (transparent dwell-only places, measured DEGENERATE at 2 080 runs:
    ``fsm_succession_prereg.md`` B2–B3, §4). The verb chain becomes the FSM's
    chain; the CTI weights choose only *among* licensed successors; the dwell
    regime stays CTI-derived.

    **What it is not.** It is not a modulator: it reweights nothing. It reads
    the FSM state that an :class:`FsmSuccessionModulator` tracks (at α = 0 the
    modulator tracks and acts on nothing, so the hold is the only mechanism in
    play) and the driver applies the hold at its routing decision
    (``MovementAttacker._route_with_hold``). It scores no axis of the APT
    criterion and may never be reported as one, for factor 9's three reasons;
    it is a supervisor-directed band point with its own pre-registration
    (``fsm_token_hold_findings.md``), not a third alignment factor.

    **The two rules it keeps from factor 9** (``fsm_succession_overlay.md``
    §2.1–2.2, and the reasons given there): the abstention rule — where the
    out-set offers no licensed destination at all the rule does nothing, so a
    stall stays structurally impossible; and the capability fallback — a
    licensed successor that cannot run in the current capability state is
    replaced by the first-step verbs that make it runnable, so the hold never
    aims the token at a dispatch the substrate would refuse.

    **The one declared parameter** is the bound on consecutive holds
    (``max_consecutive_holds``, ``succession_rules.json`` §token_hold): after
    that many holds at one decision the plain draw is accepted and the
    fall-through is counted. Every hold costs sim time, so the run cannot spin
    without the bound; the bound exists so a decision with vanishing licensed
    mass cannot consume the horizon, and its rate is reported beside every
    result.
    """

    name = "token-hold"

    def __init__(
        self,
        modulator: FsmSuccessionModulator,
        *,
        max_consecutive: int | None = None,
        rules_path: Path | str = SUCCESSION_RULES_PATH,
    ) -> None:
        if max_consecutive is None:
            max_consecutive = load_token_hold_parameters(rules_path).max_consecutive_holds
        if int(max_consecutive) < 1:
            raise ValueError(
                f"max_consecutive must be >= 1, got {max_consecutive!r}"
            )
        self.modulator = modulator
        self.max_consecutive = int(max_consecutive)
        #: Ledger for the record and the sweep.
        self.decisions = 0        # routing decisions the rule was consulted at
        self.holds = 0            # holds taken across the run
        self.hold_dwell = 0.0     # sim time consumed by holds
        self.fall_throughs = 0    # decisions that hit the bound
        self.abstentions = 0      # decisions with no licensed destination
        #: One entry per consulted decision: the licensed set, the rejected
        #: draws, the accepted one — the hand-trace's evidence (V1).
        self.log: list[dict[str, Any]] = []

    def licensed_destinations(self, composed: Mapping[str, float]) -> frozenset[str]:
        """The destinations in ``composed`` whose verb the FSM licenses right
        now (capability fallback applied). Dwell-only destinations are never
        licensed — the opaque reading."""
        targets = self.modulator.licensed_now()
        t2v = self.modulator.tactic_to_verb
        return frozenset(
            dst
            for dst, weight in composed.items()
            if weight > 0.0 and t2v.get(dst) is not None and t2v.get(dst) in targets
        )

    def snapshot(self) -> dict[str, Any]:
        return {
            "max_consecutive_holds": self.max_consecutive,
            "decisions": self.decisions,
            "holds": self.holds,
            "hold_dwell": self.hold_dwell,
            "fall_throughs": self.fall_throughs,
            "abstentions": self.abstentions,
            "succession": self.modulator.snapshot(),
        }


# --- the no-stall check -----------------------------------------------------


@dataclass(frozen=True)
class SuccessionStallFinding:
    """One cell in which the composed out-set retains no permitted destination —
    so at α = 1 every surviving edge would be zeroed and the walk would stall."""

    profile: str
    mapping_version: str
    overlay_version: str
    verdict: str
    src: str
    targets: tuple[str, ...]
    dropped_edge: str | None
    survivors: tuple[str, ...]

    def __str__(self) -> str:  # pragma: no cover - reporting only
        drop = f" (retrace-suppressed {self.dropped_edge})" if self.dropped_edge else ""
        return (
            f"{self.profile}/{self.mapping_version}/{self.overlay_version} "
            f"{self.src} [{self.verdict}] targets={list(self.targets)}{drop}: "
            f"survivors={list(self.survivors)}"
        )


def succession_stall_report(
    *,
    profiles: Iterable[str] = (
        "aggregate",
        "objective_exfiltration_impact",
        "objective_none_c2",
        "objective_impact",
        "objective_exfiltration",
    ),
    mapping_versions: Iterable[str] = ("v1_ckc_total", "v2_partial"),
    overlay_versions: Iterable[str] | None = None,
    overlays: Mapping[str, Any] | None = None,
    with_synthetic_overlay: bool = True,
    succession_path: Path | str = SUCCESSION_PATH,
    precondition_path: Path | str = PRECONDITION_PATH,
    include_retrace_suppression: bool = True,
) -> list[SuccessionStallFinding]:
    """The exhaustive no-stall check — **static, not sampled**.

    Unlike factor 8's argmin rule, this factor's permitted set is *absolute*
    rather than relative to the out-set, so it carries no structural guarantee
    that a survivor exists: a source whose whole live out-set fires off-target
    verbs would be emptied at α = 1. Whether such a source exists is a property of
    declared data, so it is decided by enumeration.

    The target set at a decision depends on run history, not only on the held
    capabilities, so the check quantifies over **every non-empty subset of the
    verb vocabulary** — a strict superset of the target sets any run can reach,
    including every capability fallback. Crossed with every profile net × mapping
    × overlay version × verdict × source place × one-shot retrace suppression.
    """
    from mtdsim.l3_simulation.controller import load_controller, load_outcome_overlay
    from mtdsim.l3_simulation.controller.outcome import load_overlay_registry
    from mtdsim.l3_simulation.movement.net import load_routing_net

    if overlays is None and overlay_versions is None:
        overlay_versions = load_overlay_registry().names
    model = PreconditionModel.load(precondition_path)
    fsm = FsmSuccession.load(succession_path)
    fsm.validate_against(model)
    verbs = sorted(model.requires)
    # Every non-empty subset of the vocabulary: a superset of every reachable
    # target set, so a clean report is a statement about the mechanism rather
    # than about the trajectories that happened to be sampled.
    target_sets = [
        frozenset(v for i, v in enumerate(verbs) if mask >> i & 1)
        for mask in range(1, 1 << len(verbs))
    ]
    verdicts = ("success", "failure", VERDICT_NONE)

    if overlays is None:
        overlays = {
            name: load_outcome_overlay(version=name) for name in overlay_versions or ()
        }

    findings: list[SuccessionStallFinding] = []
    for mapping_version in mapping_versions:
        t2v = load_controller(version=mapping_version).as_dict()
        for profile in profiles:
            net = load_routing_net(
                profile, with_synthetic_overlay=with_synthetic_overlay
            )
            for src in sorted(net.places):
                full = {
                    dst: weight
                    for dst, weight in net.base_out_weights(src).items()
                    if weight > 0.0
                }
                if not full:
                    continue  # a sink: no out-set, nothing to zero
                candidate_sets: list[tuple[str | None, dict[str, float]]] = [(None, full)]
                if include_retrace_suppression and len(full) > 1:
                    for dropped in sorted(full):
                        candidate_sets.append(
                            (dropped, {d: w for d, w in full.items() if d != dropped})
                        )
                for dropped, base_out in candidate_sets:
                    for targets in target_sets:
                        permitted = {
                            dst
                            for dst in base_out
                            if t2v.get(dst) is None or t2v.get(dst) in targets
                        }
                        if not permitted:
                            continue  # the abstention rule: nothing is attenuated
                        for verdict in verdicts:
                            for name, overlay in overlays.items():
                                composed = overlay.compose(src, verdict, dict(base_out))
                                if not composed:
                                    continue  # the overlay's own stall, not ours
                                if set(composed) & permitted:
                                    continue
                                findings.append(
                                    SuccessionStallFinding(
                                        profile=profile,
                                        mapping_version=mapping_version,
                                        overlay_version=name,
                                        verdict=verdict,
                                        src=src,
                                        targets=tuple(sorted(targets)),
                                        dropped_edge=dropped,
                                        survivors=tuple(sorted(composed)),
                                    )
                                )
    return findings


__all__ = [
    "SUCCESSION_PATH",
    "SUCCESSION_RULES_PATH",
    "VERDICT_NONE",
    "FsmSuccession",
    "FsmSuccessionModulator",
    "SuccessionParameters",
    "SuccessionStallFinding",
    "TokenHoldParameters",
    "TokenHoldRule",
    "load_succession_parameters",
    "load_token_hold_parameters",
    "succession_stall_report",
]
