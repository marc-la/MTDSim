"""The readiness-aware learning capability — the axis-7 learner generalised to
express a precondition constraint (Part B of the procedural-rigidity handoff).

The destination-only learner (:mod:`~mtdsim.l3_simulation.movement.learning`)
keys its belief on the tactic alone, so it can represent only the *marginal*
success rate of a tactic — averaged over every phase-context it was tried in.
The friction failure mode turns on a constraint the marginal cannot express:
being blocked is a function of *state* (an exploit fails because the host has not
been scanned yet), and marginalising over state discards exactly the variable the
precondition depends on. The design record proves the point with measurement — an
unmet precondition is a *deterministic* failure (0.000 over 14k+ observations),
so the marginal a destination-only learner sees is a mixture of a genuinely-paying
"ready" regime and a certain-failure "not-ready" one.

This module keys the belief on ``(destination tactic, precondition-satisfied?)``
instead — the smallest key that captures the dependency, and (measured) the
densest of the keys that can. The readiness bit is derived **in-layer**: the
learner tracks a small set of held capabilities from the attacker's own
trajectory against a declared precondition relation
(``data/ogasp/controller/precondition_relation.json``), and reads no substrate
state, so the scheme-awareness exclusion is untouched — the relation declares the
attacker's own tradecraft order, not privileged information about the host.

    w'(a→b)  ∝  base(a→b) · overlay_v(a→b) · Q(b, ready?(b))^κ

Everything else is inherited unchanged from the destination-only learner: the
Laplace estimator (so an unvisited cell sits at 0.5 and exploration survives by
construction, and ``may_zero`` stays False as a proof), the multiplicative
composition, the forgetting fraction ρ decaying the belief on every MTD interrupt,
and the κ = 0 ablation that returns no factors and is bit-identical to a run with
no state attached. Only the cell key gains the bit. The declared (κ, ρ) values,
their tiers and bands, are the same family and are read from the same rules
artefact (``learning_rules.json``) — this is a representation change, not a new
value family.

Design record: ``docs/implementation/pipeline/ogasp/learning_representation.md``.
The mechanism it generalises: ``learning_capability.md``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from mtdsim.l3_simulation.movement.learning import (
    FAILURE,
    RULES_PATH,
    SUCCESS,
    LearningParameters,
    load_learning_parameters,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
PRECONDITION_PATH = (
    _REPO_ROOT / "data" / "ogasp" / "controller" / "precondition_relation.json"
)

# The MTD resource type whose interrupt severs the attacker's position — the
# substrate clears the host cursor only on a network-layer mutation
# (apply_mtd_interrupt_cost, B-INT-01). Matches measures.NETWORK_RESOURCE; kept
# local so this module reads no measurement code.
NETWORK_RESOURCE = "network"

#: The two credit rules. ``ACCEPTANCE`` is the shipped one — a verdict of success
#: is credit — and stays the default so every figure already on record reproduces.
#: ``PROGRESS`` credits the *state change* instead (§ the class docstring), and is
#: the arm the feasibility study recommends.
ACCEPTANCE = "acceptance"
PROGRESS = "progress"
CREDIT_RULES = (ACCEPTANCE, PROGRESS)


@dataclass(frozen=True)
class PreconditionModel:
    """The declared verb-level capability model, loaded from the tracked
    precondition-relation artefact. Pure lookups over the declared relation —
    it reads the artefact once and never touches substrate state."""

    requires: Mapping[str, frozenset[str]]
    produces: Mapping[str, frozenset[str]]
    clears: Mapping[str, frozenset[str]]
    mtd_clears: Mapping[str, frozenset[str]]
    version: str

    @classmethod
    def load(cls, path: Path | str = PRECONDITION_PATH) -> "PreconditionModel":
        with Path(path).open(encoding="utf-8") as fh:
            doc = json.load(fh)
        verbs = doc["verbs"]
        return cls(
            requires={v: frozenset(d["requires"]) for v, d in verbs.items()},
            produces={v: frozenset(d["produces"]) for v, d in verbs.items()},
            clears={v: frozenset(d["clears"]) for v, d in verbs.items()},
            mtd_clears={
                k: frozenset(v) for k, v in doc.get("mtd_clears", {}).items()
            },
            version=str(doc["meta"]["version"]),
        )

    def is_ready(self, verb: str | None, held: frozenset[str] | set[str]) -> bool:
        """Would ``verb`` run in the phase-state ``held``? A dwell-only place
        (``verb is None``) has no precondition and is trivially ready; an unknown
        verb is treated as always ready rather than silently blocked, so a mapping
        naming a verb this relation does not is a loud failure at construction,
        never a quiet miscount here."""
        if verb is None:
            return True
        return self.requires[verb] <= set(held)


class ReadinessLearningModulator:
    """The generalised axis-7 modulator: a within-run belief keyed on
    ``(destination tactic, precondition-satisfied?)``, decaying under MTD.

    Registered on an :class:`~mtdsim.l3_simulation.movement.state.AttackerState`
    exactly as the destination-only learner is. It tracks a set of held
    capabilities across the run, updated from the attacker's own trajectory
    through the state's observation fan-out, and consults the declared
    :class:`PreconditionModel` to compute the readiness bit — no substrate read.

    ``κ = 0`` returns no factors, so the composition is arithmetically the
    two-factor rule and the run is bit-identical to one without the state, which
    is the null-equivalence guarantee re-asserted for this modulator.

    **The credit rule is selectable, and this is the axis's open question rather
    than a convenience.** Under ``credit = ACCEPTANCE`` (the default, and what
    every recorded figure was produced by) a verdict of *success* is credit — the
    substrate permitted the action. Measurement showed what that optimises: the
    learned preference tracks whether an action was **permitted** at rank
    correlation +0.921 and whether it **advanced the attacker** at −0.027, so the
    mechanism rates a tactic with a progress rate of 0.0000 at Q = 0.992 and one
    with a progress rate of 0.448 at Q = 0.302
    (``learning_mechanism_feasibility.md`` §8b).

    Under ``credit = PROGRESS`` the belief is credited by the *state change* the
    action produced: an action that moved the attacker's phase-state scores a
    success, an action the substrate permitted that left the phase-state exactly
    as it found it scores a failure, and a blocked attempt keeps landing in the
    ``(place, not-ready)`` cell where the same measurement shows it belongs (the
    not-ready component costs between 0.0 % and +1.8 % of expected progress — it
    is free and correct). The signal is contemporaneous and one-step: no
    eligibility trace, no horizon, no discount, no value function, so the no-RL
    constraint holds without argument.

    What the rule does mechanically is the reason to prefer it to a new mechanism.
    Scanning while its capability is already held changes nothing and so earns
    nothing, which retires the reconnaissance-farming loop; re-attacking a host
    already footholded changes nothing and so earns nothing, which is the *churn*
    failure mode; and moving the cursor to a fresh host clears the foothold, so
    the next exploit can earn again. Because a verb pays only while it is still
    advancing the attacker, the substrate's procedural order stops having to be
    injected and becomes something the attacker discovers.
    """

    name = "learning-readiness"
    #: Q carries a Laplace prior, so Q > 0 for every cell at every point and the
    #: factor can never zero an out-edge. Declaring False is a claim the tests prove.
    may_zero = False

    def __init__(
        self,
        *,
        kappa: float,
        rho: float,
        tactic_to_verb: Mapping[str, str | None],
        precondition_model: PreconditionModel | None = None,
        alpha: float = 1.0,
        beta: float = 1.0,
        credit: str = ACCEPTANCE,
    ) -> None:
        if kappa < 0.0:
            raise ValueError(f"kappa must be non-negative, got {kappa!r}")
        if not 0.0 <= rho <= 1.0:
            raise ValueError(f"rho must lie in [0, 1], got {rho!r}")
        if alpha <= 0.0 or beta <= 0.0:
            raise ValueError("the Laplace prior must be strictly positive on both sides")
        if credit not in CREDIT_RULES:
            raise ValueError(
                f"credit must be one of {CREDIT_RULES}, got {credit!r}"
            )
        self.credit = credit
        self.kappa = float(kappa)
        self.rho = float(rho)
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.tactic_to_verb = dict(tactic_to_verb)
        self.model = precondition_model or PreconditionModel.load()
        # cell = (place, ready?) -> decayed count.
        self.success: dict[tuple[str, bool], float] = {}
        self.failure: dict[tuple[str, bool], float] = {}
        #: The phase-state: the capabilities the attacker currently holds. Empty
        #: at the start of a run — the token has established nothing yet.
        self.held: set[str] = set()
        #: The readiness bit computed for the place currently being visited,
        #: stashed at ``observe_visit`` and consumed at ``observe_verdict`` so the
        #: credit and the routing decision use the *same* bit (both the predicted
        #: one, never ground truth). There is exactly one token, so one slot.
        self._pending: tuple[str, bool] | None = None
        self.forgettings: int = 0

    @classmethod
    def declared(
        cls,
        *,
        tactic_to_verb: Mapping[str, str | None],
        rules_path: Path | str = RULES_PATH,
        precondition_path: Path | str = PRECONDITION_PATH,
        credit: str = ACCEPTANCE,
    ) -> "ReadinessLearningModulator":
        """The learner at its declared (κ, ρ) values — the arm an experiment runs.
        Reuses the destination-only learner's rules artefact: the readiness
        generalisation is a representation change, not a new value family, and
        the credit rule is a change of *signal* rather than of magnitude, so it
        declares nothing either."""
        p = load_learning_parameters(rules_path)
        return cls(
            kappa=p.kappa,
            rho=p.rho,
            alpha=p.alpha,
            beta=p.beta,
            tactic_to_verb=tactic_to_verb,
            precondition_model=PreconditionModel.load(precondition_path),
            credit=credit,
        )

    # -- the belief ----------------------------------------------------------
    def q(self, place: str, ready: bool) -> float:
        """The estimated probability that acting at ``place`` pays *in this
        readiness state*, from this run's evidence alone. An unobserved cell sits
        at ``α / (α + β)`` = 0.5 — no opinion, not a bad one — so a place tried
        only when ready keeps a neutral belief about trying it when not ready,
        and vice versa."""
        cell = (place, ready)
        s = self.success.get(cell, 0.0)
        f = self.failure.get(cell, 0.0)
        return (s + self.alpha) / (s + f + self.alpha + self.beta)

    # -- observation (the state fans these in) -------------------------------
    def observe_visit(self, place: str) -> None:
        """The token has entered ``place`` and is about to act. Compute the
        readiness bit from the phase-state *before* this place's own effect —
        that is the bit the verdict about to be observed belongs to, and it is
        the same bit ``factors`` used to route here."""
        verb = self.tactic_to_verb.get(place)
        ready = self.model.is_ready(verb, self.held)
        self._pending = (place, ready)

    def observe_verdict(self, place: str, verdict: str) -> None:
        """Apply the place's capability effect, then credit the verdict to the
        ``(place, ready?)`` cell.

        The effect is applied **first** because the ``PROGRESS`` credit rule has
        to see whether it moved anything; under ``ACCEPTANCE`` the credit does
        not read the phase-state at all, so the order is immaterial there and the
        arm remains arithmetically identical to the shipped mechanism.
        """
        ready = self._pending[1] if self._pending and self._pending[0] == place else \
            self.model.is_ready(self.tactic_to_verb.get(place), self.held)
        cell = (place, ready)

        # Apply the capability effect. Gated on the verb having actually run —
        # a dispatch whose precondition was unmet (not ready) is blocked and
        # produces nothing, which is why production hangs off `ready`.
        verb = self.tactic_to_verb.get(place)
        before = frozenset(self.held)
        if verb is not None and ready:
            self.held |= self.model.produces[verb]
            self.held -= self.model.clears[verb]
        # "Did this action move me?" — a change in either direction counts. A
        # clearing action *is* movement: ENUM_HOST drops the foothold and the
        # port knowledge because the cursor has moved to a different host, which
        # is the pivot that makes the next compromise reachable. An action that
        # leaves the phase-state exactly as it found it achieved nothing,
        # whatever the substrate said about it.
        moved = frozenset(self.held) != before

        if self.credit == PROGRESS:
            if verdict == SUCCESS and moved:
                self.success[cell] = self.success.get(cell, 0.0) + 1.0
            elif verdict in (SUCCESS, FAILURE):
                # Permitted but inert counts against the tactic exactly as a
                # refusal does — that is the whole content of crediting progress
                # rather than acceptance.
                self.failure[cell] = self.failure.get(cell, 0.0) + 1.0
        else:  # ACCEPTANCE — the shipped rule, unchanged
            if verdict == SUCCESS:
                self.success[cell] = self.success.get(cell, 0.0) + 1.0
            elif verdict == FAILURE:
                self.failure[cell] = self.failure.get(cell, 0.0) + 1.0
        self._pending = None

    def observe_mtd_interrupt(self, resource_type: str = "") -> None:
        """The defence degrades the belief (the ρ decay, unchanged) and severs the
        phase-state the declared relation says it severs — a network-layer mutation
        clears the host cursor, an application-layer one clears nothing structural.
        The two effects are separate on purpose: the belief is what the attacker
        *knows*, the phase-state is what it currently *holds*, and MTD takes both."""
        # Phase-state severance (position lost), per the declared relation.
        self.held -= self.model.mtd_clears.get(resource_type, frozenset())
        # Belief decay (the forgetting rule, identical to the destination-only
        # learner). Fires on every interrupt regardless of resource, because the
        # confusion cost is charged on every interrupt.
        if self.rho <= 0.0:
            return
        self.forgettings += 1
        retained = 1.0 - self.rho
        if retained <= 0.0:
            self.success.clear()
            self.failure.clear()
            return
        for counts in (self.success, self.failure):
            for cell in list(counts):
                counts[cell] *= retained

    # -- the composition factor ---------------------------------------------
    def factors(
        self, state: Any, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        if self.kappa == 0.0:
            return {}  # the ablation arm — bit-identical to no state (gate 1)
        held = self.held
        model = self.model
        t2v = self.tactic_to_verb
        return {
            dst: self.q(dst, model.is_ready(t2v.get(dst), held)) ** self.kappa
            for dst in base_out_weights
        }

    def snapshot(self) -> dict[str, Any]:
        """A compact view of the belief, for narration and experiment logs."""
        cells = sorted(set(self.success) | set(self.failure))
        return {
            "kappa": self.kappa,
            "rho": self.rho,
            "credit": self.credit,
            "forgettings": self.forgettings,
            "held": sorted(self.held),
            "evidence_cells": len(cells),
            "q": {f"{p}|{'ready' if r else 'unready'}": self.q(p, r) for p, r in cells},
        }


class DeclaredReadinessBias(ReadinessLearningModulator):
    """**A control arm, not a mechanism — never ship it in a reported configuration.**

    The static modulator built from the learner's own *declared* inputs and
    nothing else: it applies ``q_ready`` when the destination's precondition is
    satisfied and ``q_unready`` when it is not, both fixed for the whole run.
    Everything else — the readiness tracking, the phase-state severance, the
    exponent, the composition — is the learner's, inherited unchanged.

    It exists to answer one question, which is the one an examiner asks first:
    **is the learner learning, or is it a lookup with extra steps?** The
    readiness bit is a declared function of the trajectory whose accuracy against
    ground truth is 1.0000 on ``v1_ckc_total``, and an unmet precondition is a
    deterministic failure — so a belief keyed on that bit converges toward a
    deterministic function of a variable the mechanism already computes for free.
    If the learner cannot be distinguished from this control on breadth *and* on
    the realised transition distribution, its accumulated counts are decoration.
    That is criterion C3 of ``learning_mechanism_feasibility.md`` §6, and it had
    never been run.

    The two constants are **arguments, not declared values** — this module
    declares nothing. A sweep states them and owns the choice; the natural
    setting is the pooled ready / not-ready success rates already measured in
    ``learning_representation.md`` §1, with the not-ready side taken at its
    Laplace estimate rather than at the measured 0.000, so the factor stays
    strictly positive and ``may_zero`` remains a proof.
    """

    name = "declared-readiness-bias"
    may_zero = False

    def __init__(self, *, q_ready: float, q_unready: float, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not 0.0 < q_ready <= 1.0 or not 0.0 < q_unready <= 1.0:
            raise ValueError(
                "both declared rates must lie in (0, 1] — a zero would zero an "
                "out-edge, which this control has no licence to do"
            )
        self.q_ready = float(q_ready)
        self.q_unready = float(q_unready)

    def q(self, place: str, ready: bool) -> float:
        """The declared constant for the readiness state. The inherited counts
        still accumulate — they are logged, and keeping them makes the control
        and the learner differ in exactly one respect — but they never reach the
        routing decision."""
        return self.q_ready if ready else self.q_unready

    def snapshot(self) -> dict[str, Any]:
        snap = super().snapshot()
        snap.update(
            {"control": True, "q_ready": self.q_ready, "q_unready": self.q_unready}
        )
        return snap


def load_tactic_to_verb(mapping_version: str | None = None) -> dict[str, str | None]:
    """The ``tactic -> verb | None`` mapping for a controller version — the
    readiness model's other input (the precondition relation is over verbs; the
    mapping says which verb each tactic dispatches). A thin convenience over the
    controller registry so a sweep constructs the modulator without importing the
    controller package directly."""
    from mtdsim.l3_simulation.controller import load_controller

    return load_controller(version=mapping_version).as_dict()


__all__ = [
    "PRECONDITION_PATH",
    "NETWORK_RESOURCE",
    "ACCEPTANCE",
    "PROGRESS",
    "CREDIT_RULES",
    "PreconditionModel",
    "ReadinessLearningModulator",
    "DeclaredReadinessBias",
    "load_tactic_to_verb",
]
