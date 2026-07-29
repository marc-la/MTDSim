"""The learning capability — a within-run belief about which tactics pay on
this terrain, and a defence that destroys it (criterion axis 7).

Cho et al.'s sharpest under-developed dimension is that attackers are assumed to
follow fixed patterns "rather than that they learn and can launch adaptive
attacks", while defenders are routinely granted learning. This module is that
capability, built as one :class:`~mtdsim.l3_simulation.movement.state.Modulator`
on the within-run attacker-state seam, so it composes as the third factor of

    w'(a→b)  ∝  base(a→b) · overlay_v(a→b) · Q(b)^κ

and reduces to today's two-factor rule exactly at ``κ = 0``.

The rule, in three parts
------------------------

**What is learned — the destination place, and nothing longer.** The unit of
credit is the tactic-place, because the thing that succeeds or fails is the
action *at* a place: the attacker learns which tactics pay on this terrain and
biases its next move toward them. Per place ``b`` the learner keeps within-run
counts of the success and failure verdicts observed there and estimates

    Q(b) = (s_b + α) / (s_b + f_b + α + β)          α = β = 1  (Laplace)

so an unvisited place sits at exactly 0.5 and is never zeroed — **exploration
survives by construction**, and the prior is also why the factor can never be
0.0 (``may_zero`` stays False, and a test pins it). Longer credit assignment —
propagating credit backwards along the trajectory — needs an eligibility trace
and a discount factor, which is reinforcement learning proper: more declared
parameters than this work can defend, and the machinery axis 8 is explicitly
deferring.

**How strongly it is acted on — the learning capability κ.** The routing
modulator is ``m(a→b) = Q(b)^κ``. At ``κ = 0`` it is identically 1 (the
ablation arm, and the seam's null guarantee); at ``κ = 1`` the multiplier *is*
the estimated success probability; above that the walk sharpens toward the
best-believed destination and, far enough up the band, collapses onto one route
— which is the trade against strategic plurality this axis has to report rather
than hide.

**What the defence does to it — the forgetting fraction ρ.** MTD's claimed
value is destroying what an attacker has accumulated, so the belief must be
perishable and the perishing must be caused by the defence. On every MTD
interrupt the attacker absorbs,

    s_b, f_b  ←  (1 − ρ) · s_b,  (1 − ρ) · f_b        for all b

with ``ρ = 0`` a learner MTD cannot touch and ``ρ = 1`` total amnesia at every
mutation. The contest between κ and ρ is the attacker's learning rate against
the defender's mutation rate — the same shape as the rate contest the timing
work established the evaluation turns on.

Three boundaries that are part of the design, not omissions
-----------------------------------------------------------

- **Within-run only.** Nothing survives a run. The attacker that studies the
  campaign across engagements is a different claim (M8d, and axis 8's beacon
  primitive), and crossing that line quietly would misstate what is modelled.
- **The learner keeps its own counts.** ``AttackerState.verdicts`` stays the
  faithful raw record of the run; forgetting decays *this object's* copy. The
  record of what happened and the attacker's belief about it are different
  things and are stored as different things.
- **A ``"none"`` verdict is not evidence.** A dwell-only place raises no verdict
  (the distinguished ``"none"``), so it neither confirms nor refutes anything
  and its ``Q`` stays at the 0.5 prior. Counting it as failure would encode a
  claim that non-action does not pay, which is an incentive/stealth claim
  (axes 5–6), not a learning one.

The declared values (κ, ρ), their tiers, bands and rationale live in
``data/ogasp/movement/learning_rules.json``; this module reads them and never
restates them. Running the module compiles the worked view and checks it
reproduces:

    PYTHONPATH=src python -m mtdsim.l3_simulation.movement.learning --check
    PYTHONPATH=src python -m mtdsim.l3_simulation.movement.learning --write

Design record: ``docs/implementation/pipeline/ogasp/learning_capability.md``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_REPO_ROOT = Path(__file__).resolve().parents[4]
RULES_PATH = _REPO_ROOT / "data" / "ogasp" / "movement" / "learning_rules.json"
FACTORS_PATH = _REPO_ROOT / "data" / "ogasp" / "movement" / "learning_factors.json"

#: The two substrate verdicts that are evidence about a place. Everything else
#: — the dwell-only ``"none"``, a terminal record's empty verdict — is silence.
SUCCESS = "success"
FAILURE = "failure"


@dataclass(frozen=True)
class LearningParameters:
    """The declared (κ, ρ) pair with the bands they are swept over."""

    kappa: float
    rho: float
    kappa_band: tuple[float, ...]
    rho_band: tuple[float, ...]
    alpha: float = 1.0
    beta: float = 1.0


def load_learning_parameters(path: Path | str = RULES_PATH) -> LearningParameters:
    """Read the declared parameters from their tracked rules artefact.

    The artefact is the source of truth for the values, their tiers, their
    rationale and their scrutiny record (the declared-value precedent); this
    reads the numbers and nothing else, so a value can never drift between the
    ledger and the code that runs it.
    """
    with Path(path).open(encoding="utf-8") as fh:
        doc = json.load(fh)
    declared = doc["declared_parameters"]
    estimator = doc["model"]["estimator"]
    return LearningParameters(
        kappa=float(declared["kappa"]["value"]),
        rho=float(declared["rho"]["value"]),
        kappa_band=tuple(float(v) for v in declared["kappa"]["sweep"]),
        rho_band=tuple(float(v) for v in declared["rho"]["sweep"]),
        alpha=float(estimator["alpha"]),
        beta=float(estimator["beta"]),
    )


class LearningModulator:
    """The axis-7 modulator: reweights routing by a within-run belief about
    which destinations pay, and forgets that belief when MTD mutates.

    Registered on an :class:`~mtdsim.l3_simulation.movement.state.AttackerState`
    like any other modulator. It observes through the state's fan-out rather
    than reading the state's counters, because it must decay its own copy while
    the state's record of the run stays intact.

    ``κ = 0`` returns no factors at all, so the composition is arithmetically
    the two-factor rule and the run is bit-identical to one without the state.
    """

    name = "learning"
    #: ``Q`` carries a Laplace prior, so ``Q > 0`` for every place at every
    #: point in every run and the factor can never zero an out-edge. Declaring
    #: False is therefore a claim, and ``test_movement_learning.py`` proves it.
    may_zero = False

    def __init__(
        self,
        *,
        kappa: float,
        rho: float,
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
        #: place -> decayed count of success verdicts observed there.
        self.success: dict[str, float] = {}
        #: place -> decayed count of failure verdicts observed there.
        self.failure: dict[str, float] = {}
        #: How many times the defence has degraded the belief.
        self.forgettings: int = 0

    @classmethod
    def declared(cls, path: Path | str = RULES_PATH) -> "LearningModulator":
        """The learner at its declared values — the arm an experiment runs."""
        p = load_learning_parameters(path)
        return cls(kappa=p.kappa, rho=p.rho, alpha=p.alpha, beta=p.beta)

    # -- the belief ----------------------------------------------------------
    def q(self, place: str) -> float:
        """The estimated probability that acting at ``place`` pays, from this
        run's evidence alone. An unvisited place sits at ``α / (α + β)`` = 0.5:
        the attacker has no opinion, not a bad one."""
        s = self.success.get(place, 0.0)
        f = self.failure.get(place, 0.0)
        return (s + self.alpha) / (s + f + self.alpha + self.beta)

    # -- observation (the state fans these in) -------------------------------
    def observe_verdict(self, place: str, verdict: str) -> None:
        if verdict == SUCCESS:
            self.success[place] = self.success.get(place, 0.0) + 1.0
        elif verdict == FAILURE:
            self.failure[place] = self.failure.get(place, 0.0) + 1.0
        # Anything else is silence, not evidence — see the module docstring.

    def observe_mtd_interrupt(self, resource_type: str = "") -> None:
        """The defence degrades the belief: every count is scaled by ``1 − ρ``.

        Uniform across places and across the mutating resource's layer. The
        faithful refinement — a network-layer mutation invalidating position
        knowledge, an application-layer one invalidating service knowledge —
        does not map cleanly onto a belief keyed by tactic-place, so it is named
        as the considered alternative in the design record and left to a later
        cycle rather than approximated here.
        """
        if self.rho <= 0.0:
            return
        self.forgettings += 1
        retained = 1.0 - self.rho
        if retained <= 0.0:
            self.success.clear()
            self.failure.clear()
            return
        for counts in (self.success, self.failure):
            for place in list(counts):
                counts[place] *= retained

    # -- the composition factor ---------------------------------------------
    def factors(
        self, state: Any, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        if self.kappa == 0.0:
            # The ablation arm. Returning no factors rather than a dict of 1.0s
            # keeps the composition arithmetically identical to a run with no
            # state attached at all, which is what gate 1 asserts field for field.
            return {}
        return {dst: self.q(dst) ** self.kappa for dst in base_out_weights}

    def snapshot(self) -> dict[str, Any]:
        """A compact view of the belief, for narration and experiment logs."""
        places = sorted(set(self.success) | set(self.failure))
        return {
            "kappa": self.kappa,
            "rho": self.rho,
            "forgettings": self.forgettings,
            "evidence_places": len(places),
            "q": {place: self.q(place) for place in places},
        }


# ---------------------------------------------------------------------------
# The compiled worked view, and its reproduction check
# ---------------------------------------------------------------------------
#
# The declared-value precedent requires that declared values be rule-generated
# and reproducible rather than hand-set (``declared_value_provenance.md`` §1).
# For a two-parameter family the "set" the generator has to reproduce is not a
# table of authored magnitudes but the *behaviour the rules imply*: what the
# multiplier is after n successes and m failures, at each swept κ, and what
# fraction of the belief survives n mutations at each swept ρ. Compiling that
# and re-deriving it cell for cell is the same guarantee the 210-pair overlay
# table gets — the values follow from the stated rules, and a rule edit is a
# one-line change that moves every cell it should.

#: The evidence grid the worked view is compiled over: successes × failures.
EVIDENCE_GRID = tuple(range(0, 5))
#: How many mutations the forgetting ladder is compiled out to.
FORGETTING_STEPS = tuple(range(0, 9))


def compile_worked_view(params: LearningParameters) -> dict[str, Any]:
    """Compile the declared rules into the worked view — pure, so ``--check``
    can re-derive every cell and compare."""
    factor_cells: dict[str, float] = {}
    q_cells: dict[str, float] = {}
    for s in EVIDENCE_GRID:
        for f in EVIDENCE_GRID:
            q = (s + params.alpha) / (s + f + params.alpha + params.beta)
            q_cells[f"s{s}f{f}"] = q
            for kappa in params.kappa_band:
                factor_cells[f"k{kappa:g}|s{s}f{f}"] = q**kappa
    retention_cells: dict[str, float] = {}
    for rho in params.rho_band:
        for n in FORGETTING_STEPS:
            retention_cells[f"r{rho:g}|n{n}"] = (1.0 - rho) ** n
    return {
        "_meta": {
            "generated_by": "src/mtdsim/l3_simulation/movement/learning.py",
            "rules": "data/ogasp/movement/learning_rules.json",
            "note": (
                "Worked view of the declared learning rules — do not hand-edit. "
                "'q' is the Laplace estimate after s successes and f failures; "
                "'factor' is that estimate raised to each swept kappa; "
                "'retention' is the fraction of the belief surviving n MTD "
                "mutations at each swept rho."
            ),
            "cells": len(q_cells) + len(factor_cells) + len(retention_cells),
        },
        "q": q_cells,
        "factor": factor_cells,
        "retention": retention_cells,
    }


def _cells(view: Mapping[str, Any]) -> dict[str, float]:
    flat: dict[str, float] = {}
    for section in ("q", "factor", "retention"):
        for key, value in view[section].items():
            flat[f"{section}/{key}"] = value
    return flat


def check_worked_view(
    rules_path: Path | str = RULES_PATH, view_path: Path | str = FACTORS_PATH
) -> tuple[int, int, list[str]]:
    """Re-compile the worked view and compare it to what is committed.

    Returns ``(differing, total, examples)`` — the shape the overlay generator's
    ``--check`` reports, so the reproduction claim reads the same way.
    """
    fresh = _cells(compile_worked_view(load_learning_parameters(rules_path)))
    with Path(view_path).open(encoding="utf-8") as fh:
        committed = _cells(json.load(fh))
    keys = sorted(set(fresh) | set(committed))
    differing = [
        key
        for key in keys
        if key not in fresh
        or key not in committed
        or abs(fresh[key] - committed[key]) > 1e-12
    ]
    return len(differing), len(keys), differing[:5]


def write_worked_view(
    rules_path: Path | str = RULES_PATH, view_path: Path | str = FACTORS_PATH
) -> int:
    view = compile_worked_view(load_learning_parameters(rules_path))
    path = Path(view_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(view, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return int(view["_meta"]["cells"])


def _main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--write", action="store_true",
                    help="regenerate the compiled worked view from the rules")
    ap.add_argument("--check", action="store_true",
                    help="re-compile and report any cell differing from what is committed")
    args = ap.parse_args(argv)
    if args.write:
        n = write_worked_view()
        print(f"wrote {FACTORS_PATH.relative_to(_REPO_ROOT)} ({n} cells)")
    if args.check or not args.write:
        differing, total, examples = check_worked_view()
        print(f"{differing} of {total} cells differ")
        for key in examples:
            print(f"  {key}")
        return 1 if differing else 0
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(_main())


__all__ = [
    "RULES_PATH",
    "FACTORS_PATH",
    "LearningParameters",
    "load_learning_parameters",
    "LearningModulator",
    "compile_worked_view",
    "check_worked_view",
    "write_worked_view",
]
