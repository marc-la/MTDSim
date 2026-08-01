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
    ) -> None:
        if kappa < 0.0:
            raise ValueError(f"kappa must be non-negative, got {kappa!r}")
        if not 0.0 <= rho <= 1.0:
            raise ValueError(f"rho must lie in [0, 1], got {rho!r}")
        if alpha <= 0.0 or beta <= 0.0:
            raise ValueError("the Laplace prior must be strictly positive on both sides")
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
    ) -> "ReadinessLearningModulator":
        """The learner at its declared (κ, ρ) values — the arm an experiment runs.
        Reuses the destination-only learner's rules artefact: the readiness
        generalisation is a representation change, not a new value family."""
        p = load_learning_parameters(rules_path)
        return cls(
            kappa=p.kappa,
            rho=p.rho,
            alpha=p.alpha,
            beta=p.beta,
            tactic_to_verb=tactic_to_verb,
            precondition_model=PreconditionModel.load(precondition_path),
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
        """Credit the verdict to the ``(place, ready?)`` cell, then apply the
        place's capability effect — the verb has now run, so what it produces or
        clears joins the phase-state for the routing decision that follows."""
        ready = self._pending[1] if self._pending and self._pending[0] == place else \
            self.model.is_ready(self.tactic_to_verb.get(place), self.held)
        if verdict == SUCCESS:
            cell = (place, ready)
            self.success[cell] = self.success.get(cell, 0.0) + 1.0
        elif verdict == FAILURE:
            cell = (place, ready)
            self.failure[cell] = self.failure.get(cell, 0.0) + 1.0
        # Apply the capability effect. Gated on the verb having actually run —
        # a dispatch whose precondition was unmet (not ready) is blocked and
        # produces nothing, which is why production hangs off `ready`.
        verb = self.tactic_to_verb.get(place)
        if verb is not None and ready:
            self.held |= self.model.produces[verb]
            self.held -= self.model.clears[verb]
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
            "forgettings": self.forgettings,
            "held": sorted(self.held),
            "evidence_cells": len(cells),
            "q": {f"{p}|{'ready' if r else 'unready'}": self.q(p, r) for p, r in cells},
        }


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
    "PreconditionModel",
    "ReadinessLearningModulator",
    "load_tactic_to_verb",
]
