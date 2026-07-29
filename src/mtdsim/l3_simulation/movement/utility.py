"""The attacker's utility modulator — criterion axis 6, incentive-driven rationality.

Cho et al. model the sophisticated attacker as "a rational actor that is
sensitive to incentives, such as attack success with minimum cost", and name
the asymmetry as an under-developed dimension: the rational-actor framing is
routinely applied to defenders and seldom to attackers. This module is the
movement layer's answer. It registers one :class:`Modulator` on the attacker
state seam (``state.py``), whose factor at a routing decision is

    m(a→b)  =  ( u(b) / ū )^λ        where    u(b) = benefit(b) / cost(b)

with ``ū`` the mean utility over the source's out-set, so **λ scales a ratio
and not an absolute magnitude**. The exponent λ is the **rationality
exponent**: at ``λ = 0`` every factor is exactly 1.0 and the run is
bit-identical to one with no modulator at all, so the current model is the
``λ = 0`` special case of this one — which gives the ablation for free and
makes the comparison honest. As λ rises the attacker increasingly prefers
moves with better payoff per unit cost.

**The cost term is reused, never re-declared.** ``cost(b)`` is the tactic's
declared duration from ``data/ogasp/tactic_durations.json``, clamped up to the
declared ``cost_floor_s`` — needed because ``resource-development`` is declared
0.0 (an off-clock preparation tactic, not a free one) and a ratio cannot divide
by zero. The floor is a **named declared parameter** reported in the compiled
view and the sweep design, not a silent ``max()``. Reusing the catalogue means
this factor's cost half inherits the durations' tier badges and their completed
sensitivity sweep; a parallel cost catalogue that could drift from the
durations would be worse than no cost model at all.

**The benefit term is the one new declared family, and it is rule-generated.**
Fifteen values per profile from a stated model — *objective proximity within
the profile*: the profile's own declared objective carries the unit of benefit,
and every other tactic is instrumental, discounted geometrically by how many
consensus lifecycle stages separate it from the nearest objective. Two
properties keep it from restating the overlay's lifecycle-distance kernel, and
both are asserted in the test suite rather than argued:

- benefit depends on the **destination and the profile**, never on the source,
  whereas the distance kernel is a signed source→destination offset;
- benefit **differs between profiles for the same tactic**, which the distance
  kernel never does.

Were benefit to re-derive the jump's distance, the model would double-count
distance and this factor would not be measuring incentive at all.

**Determinism (SIM-05).** The modulator is a pure function of declared data and
the current place — it reads no history off the state and draws from no random
stream, so the fourth stream stays unused and determinism is trivially intact.

**The claim this supports, exactly.** An attacker that is rational *over its own
declared beliefs about cost and benefit* — a rationality shape, not a
calibrated utility, and not a claim about any real adversary. Envelope, not
actor.

Rules and ledger: ``data/ogasp/attacker_utility.json``.
Compiled view: ``data/ogasp/attacker_utility_benefit.json`` (generated).
Design record: ``docs/implementation/pipeline/ogasp/incentive_rationality.md``.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from mtdsim.l3_simulation.movement.attacker import DURATIONS_PATH, load_dwell_catalogue

# …/src/mtdsim/l3_simulation/movement/utility.py -> repo root is parents[4].
_REPO_ROOT = Path(__file__).resolve().parents[4]
OGASP_DIR = _REPO_ROOT / "data" / "ogasp"
UTILITY_RULES_PATH = OGASP_DIR / "attacker_utility.json"
BENEFIT_VIEW_PATH = OGASP_DIR / "attacker_utility_benefit.json"
CONSENSUS_PATH = OGASP_DIR / "controller" / "lifecycle_consensus.json"


class UtilityCompileError(ValueError):
    """Raised when the declared artefacts cannot produce a benefit table — a
    tactic the stage ordering does not seat, an objective outside the tactic
    set, or a rule id the compiler does not implement."""


# --- the declared model -----------------------------------------------------


@dataclass(frozen=True)
class UtilityModel:
    """The three declared constants, read from the rules artefact.

    ``rho`` decays instrumental benefit per lifecycle stage of separation from
    the profile's objective; ``cost_floor_s`` is the floor the reused duration
    catalogue is clamped up to; ``lam`` is the rationality exponent, whose zero
    recovers today's model exactly.
    """

    rho: float = 0.5
    cost_floor_s: float = 4.5
    lam: float = 1.0

    def as_dict(self) -> dict[str, float]:
        return {"rho": self.rho, "cost_floor_s": self.cost_floor_s, "lambda": self.lam}


@dataclass(frozen=True)
class UtilityRules:
    """The loaded rules artefact plus the two orderings it folds in.

    ``objectives`` and ``stage_of`` are read from their own homes (the GASP
    class-semantic objective sets and the lifecycle-consensus artefact) rather
    than copied into the rules file, so each ordering has exactly one home.
    """

    model: UtilityModel
    stage_of: dict[str, int]
    objectives: dict[str, tuple[str, ...]]
    cost: dict[str, float]
    doc: dict

    @property
    def tactics(self) -> tuple[str, ...]:
        return tuple(sorted(self.stage_of))

    @property
    def profiles(self) -> tuple[str, ...]:
        return tuple(sorted(self.objectives))


def load_utility_rules(
    rules_path: Path | str = UTILITY_RULES_PATH,
    consensus_path: Path | str = CONSENSUS_PATH,
    durations_path: Path | str = DURATIONS_PATH,
) -> UtilityRules:
    """Read the declared model, the stage ordering, the objective sets and the
    reused cost catalogue.

    Loud on disagreement: a profile whose declared objective is not a seated
    tactic, or a tactic the duration catalogue does not price, fails here rather
    than compiling to a silently wrong table.
    """
    from mtdsim.l3_simulation.petri.analysis import OBJECTIVE_TACTICS

    doc = json.loads(Path(rules_path).read_text(encoding="utf-8"))
    consensus = json.loads(Path(consensus_path).read_text(encoding="utf-8"))
    declared = doc["declared_parameters"]
    model = UtilityModel(
        rho=float(declared["rho"]["value"]),
        cost_floor_s=float(declared["cost_floor_s"]["value"]),
        lam=float(declared["lambda"]["value"]),
    )
    stage_of = {k: int(v) for k, v in consensus["stage_of"].items()}
    objectives = {p: tuple(o) for p, o in OBJECTIVE_TACTICS.items()}
    cost = load_dwell_catalogue(durations_path)

    unseated = {o for objs in objectives.values() for o in objs} - set(stage_of)
    if unseated:
        raise UtilityCompileError(
            f"declared objective tactic(s) {sorted(unseated)} are not seated by "
            "the lifecycle consensus ordering"
        )
    unpriced = set(stage_of) - set(cost)
    if unpriced:
        raise UtilityCompileError(
            f"the duration catalogue does not price {sorted(unpriced)}; the cost "
            "term is the catalogue and must cover every seated tactic"
        )
    return UtilityRules(
        model=model, stage_of=stage_of, objectives=objectives, cost=cost, doc=doc
    )


# --- the benefit compiler ---------------------------------------------------


def stage_gap(tactic: str, profile: str, rules: UtilityRules) -> int:
    """``min over o in objectives(profile) of |stage(o) − stage(tactic)|``.

    Unsigned on purpose: proximity to an objective is a distance, and a tactic
    seated past the objective's stage is no closer to achieving it than one
    seated the same separation before it.
    """
    try:
        here = rules.stage_of[tactic]
    except KeyError as exc:
        raise UtilityCompileError(f"tactic not seated by the ordering: {tactic!r}") from exc
    objectives = rules.objectives.get(profile)
    if not objectives:
        raise UtilityCompileError(f"no declared objective set for profile {profile!r}")
    return min(abs(rules.stage_of[o] - here) for o in objectives)


def benefit_cell(tactic: str, profile: str, rules: UtilityRules, rho: float) -> dict:
    """One compiled benefit cell: the rule that fired, its value, and the gap.

    The cell records the rule and the stage gap alongside the value so a reader
    of the compiled table can see *why* a value is what it is without re-running
    the compiler.
    """
    if tactic in rules.objectives[profile]:
        return {"v": 1.0, "rule": "objective", "gap": 0}
    gap = stage_gap(tactic, profile, rules)
    return {"v": round(rho ** (1 + gap), 6), "rule": "instrumental", "gap": gap}


def compile_benefit(rules: UtilityRules, rho: float | None = None) -> dict[str, dict[str, dict]]:
    """The complete ``by_profile[profile][tactic]`` benefit table.

    Complete means every seated tactic under every profile — 75 cells — not the
    subset a profile's net has places for. The declared layer authors the whole
    space; which cells route mass is a property of the data layer
    (``declared_value_provenance.md`` §5).
    """
    rho = rules.model.rho if rho is None else float(rho)
    return {
        profile: {
            tactic: benefit_cell(tactic, profile, rules, rho)
            for tactic in rules.tactics
        }
        for profile in rules.profiles
    }


def benefit_values(rules: UtilityRules, rho: float | None = None) -> dict[str, dict[str, float]]:
    """The benefit table reduced to bare values — what a modulator needs."""
    return {
        profile: {tactic: cell["v"] for tactic, cell in cells.items()}
        for profile, cells in compile_benefit(rules, rho).items()
    }


def view_document(rules: UtilityRules) -> dict:
    """The compiled view, ready to write: the model, its provenance, the table."""
    return {
        "_meta": {
            "artefact": "compiled attacker-benefit table (criterion axis 6)",
            "generated_from": "attacker_utility.json + controller/lifecycle_consensus.json "
            "+ the GASP class-semantic objective sets — DO NOT hand-edit; regenerate "
            "with `PYTHONPATH=src python -m mtdsim.l3_simulation.movement.utility --write`",
            "rule": "objective → 1.0; otherwise instrumental → rho^(1 + gap), gap = "
            "min stage separation from the profile's nearest declared objective",
            "declared_parameters": rules.model.as_dict(),
            "coverage": "complete: 5 profiles x 15 seated tactics = 75 cells "
            "(corpus-agnostic — includes tactics a profile's net has no place for)",
            "format": "by_profile[profile][tactic] = {v: benefit, rule: rule-id, "
            "gap: stage separation}; rationale via attacker_utility.json benefit_rules[rule]",
            "cost_term": "NOT stored here — the cost term is data/ogasp/tactic_durations.json "
            "duration_s, reused rather than re-declared, clamped up to cost_floor_s",
        },
        "by_profile": compile_benefit(rules),
    }


def diff_against(
    rules: UtilityRules, committed: dict, *, tolerance: float = 1e-9
) -> list[str]:
    """Re-compile and diff against the committed view — the reproduction check.

    Returns one human-readable line per differing cell, empty when the
    compilation reproduces the committed table exactly. An empty list is the
    claim "these values follow from the rules"; a non-empty one says the table
    was edited away from its rules, which is the failure mode the check exists
    to catch.
    """
    problems: list[str] = []
    got = compile_benefit(rules)
    want = committed["by_profile"]
    for profile in sorted(set(got) | set(want)):
        gp, wp = got.get(profile, {}), want.get(profile, {})
        for tactic in sorted(set(gp) | set(wp)):
            g, w = gp.get(tactic), wp.get(tactic)
            if g is None or w is None:
                problems.append(f"{profile}/{tactic}: present in only one table")
                continue
            if abs(float(g["v"]) - float(w["v"])) > tolerance:
                problems.append(
                    f"{profile}/{tactic}: value {w['v']} committed vs {g['v']} compiled"
                )
            elif g["rule"] != w["rule"]:
                problems.append(
                    f"{profile}/{tactic}: rule {w['rule']!r} committed vs "
                    f"{g['rule']!r} compiled"
                )
    return problems


def check_view(rules: UtilityRules | None = None, path: Path | str = BENEFIT_VIEW_PATH) -> list[str]:
    """Re-compile the benefit table and diff it against what is committed."""
    rules = rules if rules is not None else load_utility_rules()
    committed = json.loads(Path(path).read_text(encoding="utf-8"))
    return diff_against(rules, committed)


def write_view(rules: UtilityRules | None = None, path: Path | str = BENEFIT_VIEW_PATH) -> Path:
    """Regenerate the compiled benefit view in place."""
    rules = rules if rules is not None else load_utility_rules()
    path = Path(path)
    path.write_text(json.dumps(view_document(rules), indent=2) + "\n", encoding="utf-8")
    return path


def load_benefit(path: Path | str = BENEFIT_VIEW_PATH) -> dict[str, dict[str, float]]:
    """``profile -> tactic -> benefit`` from the committed compiled view."""
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    return {
        profile: {tactic: float(cell["v"]) for tactic, cell in cells.items()}
        for profile, cells in doc["by_profile"].items()
    }


# --- the modulator ----------------------------------------------------------


class UtilityModulator:
    """The routing factor a cost-sensitive attacker applies — the seam's third
    term for criterion axis 6.

    Constructed per profile, because benefit is per-profile: an objective set is
    per-profile (``infrastructure_setup`` contains no exfiltration or impact
    place at all), so a benefit model keyed on a universal objective would be
    meaningless there.

    ``may_zero`` is deliberately absent: benefit is strictly positive by
    construction (``rho^(1+gap)`` with ``0 < rho < 1``) and cost is floored
    above zero, so utility is strictly positive and no factor can reach zero.
    The seam's stall rule is therefore never engaged and the no-stall check
    needs no re-run — the modulator can suppress an out-edge's share, never
    remove it.
    """

    name = "utility"

    def __init__(
        self,
        *,
        profile: str,
        benefit: Mapping[str, float],
        cost: Mapping[str, float],
        lam: float,
        cost_floor_s: float,
    ) -> None:
        self.profile = profile
        self.benefit = dict(benefit)
        self.cost = dict(cost)
        self.lam = float(lam)
        self.cost_floor_s = float(cost_floor_s)
        if self.cost_floor_s <= 0.0:
            raise ValueError(
                f"cost_floor_s must be positive (got {self.cost_floor_s!r}); the "
                "floor exists precisely so the utility ratio cannot divide by the "
                "off-clock tactic's declared zero"
            )

    def utility(self, tactic: str) -> float:
        """``benefit(tactic) / max(cost(tactic), cost_floor_s)`` — the attacker's
        declared payoff per unit of declared cost for arriving at ``tactic``."""
        try:
            benefit = self.benefit[tactic]
        except KeyError as exc:
            raise UtilityCompileError(
                f"no declared benefit for {tactic!r} under profile "
                f"{self.profile!r}; the benefit table is complete over the "
                "place-union, so this is a net/table disagreement"
            ) from exc
        return benefit / max(self.cost.get(tactic, 0.0), self.cost_floor_s)

    def factors(
        self, state, src: str, base_out_weights: Mapping[str, float]
    ) -> dict[str, float]:
        """Per-destination ``(u(b) / ū)^λ`` over the source's out-set.

        Normalising by the out-set's mean utility before exponentiating is what
        makes λ scale a *ratio* rather than an absolute magnitude — and it keeps
        the factors near 1.0, so the state's per-decision log reads as "how much
        this destination beat the local average" rather than as an unanchored
        number. (The normalisation is behaviourally free: the composition
        renormalises afterwards, so any common rescaling cancels. It is for the
        parameter's meaning and the log's legibility.)

        ``state`` is unused: the factor is a pure function of declared data and
        the current place, which is what keeps SIM-05 trivially intact.
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


def utility_modulator_for(
    profile: str,
    *,
    lam: float | None = None,
    rho: float | None = None,
    cost_floor_s: float | None = None,
    rules: UtilityRules | None = None,
) -> UtilityModulator:
    """The declared modulator for one profile, from the tracked artefacts.

    Every parameter defaults to its declared value; each is overridable so the
    sweep can move one at a time. ``rho`` recompiles the benefit table in memory
    rather than reading the committed view, so a swept ``rho`` needs no file on
    disk — the committed view stays the declared value's reproduction check.
    """
    rules = rules if rules is not None else load_utility_rules()
    benefit = (
        load_benefit() if rho is None else benefit_values(rules, rho)
    )[profile]
    return UtilityModulator(
        profile=profile,
        benefit=benefit,
        cost=rules.cost,
        lam=rules.model.lam if lam is None else float(lam),
        cost_floor_s=(
            rules.model.cost_floor_s if cost_floor_s is None else float(cost_floor_s)
        ),
    )


def _main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Compile the declared attacker-benefit family into its "
        "75-cell view, or check that what is committed still follows from the rules."
    )
    parser.add_argument("--write", action="store_true", help="regenerate the compiled view")
    parser.add_argument(
        "--check",
        action="store_true",
        help="re-compile the view and report differing cells",
    )
    args = parser.parse_args(argv)
    if not (args.write or args.check):
        parser.error("pass --write or --check")

    rules = load_utility_rules()
    if args.write:
        print(f"wrote {write_view(rules)}")
    if args.check:
        problems = check_view(rules)
        total = len(rules.profiles) * len(rules.tactics)
        print(f"benefit table: {len(problems)} differing cells (of {total})")
        for line in problems[:20]:
            print(f"    {line}")
        if len(problems) > 20:
            print(f"    … and {len(problems) - 20} more")
        if problems:
            print(
                "\nREPRODUCTION CHECK FAILED — the committed benefit view no longer "
                "follows from the rules. Either the rules changed and the view needs "
                "regenerating, or the view was hand-edited."
            )
            return 1
        print("\nreproduction check passed: the committed view follows from the rules")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(_main())


__all__ = [
    "BENEFIT_VIEW_PATH",
    "CONSENSUS_PATH",
    "UTILITY_RULES_PATH",
    "UtilityCompileError",
    "UtilityModel",
    "UtilityModulator",
    "UtilityRules",
    "benefit_cell",
    "benefit_values",
    "check_view",
    "compile_benefit",
    "diff_against",
    "load_benefit",
    "load_utility_rules",
    "stage_gap",
    "utility_modulator_for",
    "view_document",
    "write_view",
]
