"""The axis-5 exposure family — the declared model behind the detectability curve.

Criterion axis 5 scores this model NOT ADDRESSED on stealth, and the reason is
narrow: the substrate offers the movement attacker **no detection model to be
stealthy against**, so tempo has no consequence and tempo without a consequence
is not evasion. What the model *does* have is a tempo axis — seven of fifteen
tactics consume time and dispatch nothing — and what it lacks is any observable
that tempo moves. This module supplies that observable.

It declares the increment family; the reader that walks a recorded run with it is
``measures.py`` §9. The split follows the two precedents it sits beside: a
declared family lives in its own module with a ``--write`` / ``--check``
reproduction check (``learning.py``, ``utility.py``, ``alignment.py``), and a
reader over records lives in the measurement suite.

**Metric only, and that is a design commitment rather than a stage.** ``D`` is
read by nothing in the run — not routing, not dwell, not any mutation selector.
No attacker state is added, so no S2 freeze question arises, and the runs it
scores are runs that would have happened anyway. That is what stops the measure
building in its own conclusion, and it is also the ceiling: a metric nothing
responds to has not been shown to change an outcome, so this reaches DESIGNED and
stops there (``stealth_conceptualisation.md`` §9).

**What is grounded and what is declared, kept apart.** The tier *order* over the
fifteen tactics is transcribed from the corpus's own quoted observability
evidence (``stealth_conceptualisation.md`` §7) and from nothing else. Every
*magnitude* — the ratio between rungs, the weight on the CVSS term, the decay
constant — is declared, swept, and carries a null inside its band. The corpus
contains no per-tactic detection probability anywhere, so no amount of reading
could have supplied those numbers; saying so is the point of the split rather
than an apology for it.

**``D`` carries no units.** Its scale is set by ``rho`` and ``tau``, neither
calibrated against anything outside this model, so no absolute figure is
reportable. A ratio between two arms or two profiles at a common setting is.

Rules and ledger: ``data/ogasp/movement/exposure_rules.json``.
Compiled view: ``data/ogasp/movement/exposure_increments.json`` (generated).
Pre-registration: ``docs/implementation/pipeline/ogasp/stealth_exposure_prereg.md``.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

_REPO_ROOT = Path(__file__).resolve().parents[4]
EXPOSURE_RULES_PATH = _REPO_ROOT / "data" / "ogasp" / "movement" / "exposure_rules.json"
INCREMENTS_VIEW_PATH = (
    _REPO_ROOT / "data" / "ogasp" / "movement" / "exposure_increments.json"
)

#: The two directions the CVSS term can be read in. Neither is attested — the
#: pre-registration's E3 fixes what the study does with the pair rather than
#: letting the build pick one silently.
INVERSE = "inverse"
DIRECT = "direct"
DIRECTIONS = (INVERSE, DIRECT)

#: The tiers a tactic can sit at (``stealth_conceptualisation.md`` §7).
MIN_TIER = 0
MAX_TIER = 4

#: The two tactics §7 ranks bimodally. The net carries one place per tactic and
#: no mode dimension to split them on, so each takes one slot and both are swept
#: — these are the names the sweep moves.
BIMODAL_TACTICS = ("reconnaissance", "lateral-movement")


class ExposureCompileError(ValueError):
    """The declared artefact does not describe a usable increment family."""


@dataclass(frozen=True)
class ExposureRules:
    """The authored artefact: the tier assignment plus the declared parameters."""

    tier_of: dict[str, int]          # tactic -> declared tier
    verb_preimage: dict[str, tuple[str, ...]]   # native verb -> tactics mapping to it
    tau: float
    rho: float
    delta: float
    tau_sweep: tuple[float, ...]
    rho_sweep: tuple[float, ...]
    delta_sweep: tuple[float, ...]
    raw: dict = field(repr=False, default_factory=dict)

    @property
    def tactics(self) -> tuple[str, ...]:
        return tuple(sorted(self.tier_of))

    @property
    def verbs(self) -> tuple[str, ...]:
        return tuple(sorted(self.verb_preimage))


def load_exposure_rules(path: Path | str = EXPOSURE_RULES_PATH) -> ExposureRules:
    """Read the declared artefact. Loader, not a measure."""
    with Path(path).open(encoding="utf-8") as fh:
        doc = json.load(fh)
    tiers = doc["model"]["tiers"]
    tier_of: dict[str, int] = {}
    for tier_key, block in tiers.items():
        for tactic in block["tactics"]:
            if tactic in tier_of:
                raise ExposureCompileError(
                    f"{tactic!r} is assigned to two tiers ({tier_of[tactic]} and "
                    f"{tier_key}); the ranking must be a function"
                )
            tier_of[tactic] = int(tier_key)
    params = doc["declared_parameters"]
    preimage = doc["model"]["baseline_verb_tiers"]["preimage"]
    return ExposureRules(
        tier_of=tier_of,
        verb_preimage={v: tuple(ts) for v, ts in preimage.items()},
        tau=float(params["tau"]["value"]),
        rho=float(params["rho"]["value"]),
        delta=float(params["delta"]["value"]),
        tau_sweep=tuple(float(x) for x in params["tau"]["sweep"]),
        rho_sweep=tuple(float(x) for x in params["rho"]["sweep"]),
        delta_sweep=tuple(float(x) for x in params["delta"]["sweep"]),
        raw=doc,
    )


def tier_increment(tier: int, rho: float) -> float:
    """``rho ^ (4 − tier)`` — the geometric increment for one observability rung.

    Geometric rather than linear because the ranking is **ordinal**: it fixes the
    order of the rungs and says nothing about the distance between them, so the
    only honest parameterisation is one where a single declared number states what
    a one-rung step is worth. At ``rho = 1`` every rung scores 1.0 and the ranking
    does nothing at all — the family's exact ablation, and the placeholder the
    2026-08-04 meeting proposed in its own words.
    """
    if not 0.0 < rho <= 1.0:
        raise ExposureCompileError(f"rho must lie in (0, 1], got {rho!r}")
    if not MIN_TIER <= tier <= MAX_TIER:
        raise ExposureCompileError(
            f"tier must lie in [{MIN_TIER}, {MAX_TIER}], got {tier!r}"
        )
    return float(rho ** (MAX_TIER - tier))


def cvss_factor(exploitability: float, delta: float, direction: str) -> float:
    """The CVSS modulation ``m`` for one visit — 1.0 where no vulnerability was
    attempted, so the term is inert everywhere it has no reading.

        m = 1 − δ + 2δ·x ,     x = 1 − e (inverse)  or  x = e (direct)

    ``exploitability`` is the mean **initial** exploitability (``cvss / 5.5``) over
    the vulnerabilities the action attempted, and 0.0 encodes *none attempted*
    unambiguously: the substrate's ``complexity`` is floored strictly above zero
    and ``cvss = (complexity + impact) / 2``, so a real vulnerability's figure is
    strictly positive.

    **Direction is a declared judgement with no attestation on either side.** The
    inverse reading is the meeting's ("a more easily exploitable vulnerability
    needs a smaller footprint"); the direct reading is its equally arguable
    opposite. Both are computed at every setting and the pre-registration's E3
    decides what may be said about the pair.
    """
    if direction not in DIRECTIONS:
        raise ExposureCompileError(
            f"direction must be one of {DIRECTIONS}, got {direction!r}"
        )
    if delta < 0.0:
        raise ExposureCompileError(f"delta must be non-negative, got {delta!r}")
    if exploitability <= 0.0:
        return 1.0
    e = min(1.0, float(exploitability))
    x = (1.0 - e) if direction == INVERSE else e
    return 1.0 - delta + 2.0 * delta * x


@dataclass(frozen=True)
class ExposureModel:
    """One fully-resolved point of the declared family — everything the reader
    needs, with no further lookups.

    ``tier_overrides`` is how the sweep moves the two bimodal tactics
    (:data:`BIMODAL_TACTICS`): the net carries one place per tactic, so
    reconnaissance and lateral-movement each take a single slot and the
    alternative placement is a swept setting rather than a second table.
    """

    tau: float
    rho: float
    delta: float
    direction: str
    tier_of: dict[str, int]
    verb_tier_of: dict[str, int]
    #: **R1 (Marc, 2026-08-06).** The increment fires on a tactic's *invocation of
    #: a verb*; a dwell-only visit contributes elapsed time and no increment. The
    #: superseded convention — every visit scores — stays reachable because the
    #: comparison between the two is itself a reported result, but it is not the
    #: default: under it, 56-62 % of four profiles' exposure came from tactics the
    #: simulator never executes.
    score_dwell_only: bool = False
    #: **R2 (Marc, 2026-08-06).** Score the movement arm at *verb* tiers rather
    #: than tactic tiers. Off within an arm, where the corpus grounding is the
    #: point; **on** for any arm-versus-arm reading, so that both sides are scored
    #: by one identical rule and a cross-arm difference can only be *when*, never
    #: *what*.
    verb_level: bool = False

    def __post_init__(self) -> None:
        if self.tau <= 0.0:
            raise ExposureCompileError(
                f"tau must be positive, got {self.tau!r} — a non-positive decay "
                "constant makes the level either undefined or perfectly memoryless, "
                "and the memoryless case is reached by a small positive tau instead"
            )
        tier_increment(MAX_TIER, self.rho)     # validates rho
        cvss_factor(0.5, self.delta, self.direction)  # validates delta / direction

    #: ``tactic -> the verb it invokes``, empty string for a dwell-only tactic.
    #: Derived from the declared artefact's own verb preimage rather than
    #: hard-coded, so R1's dispatch test and the mapping stay one fact.
    verb_of: dict[str, str] = field(default_factory=dict)

    # -- the two increment tables the reader consumes ------------------------
    def invokes(self, place: str) -> bool:
        """Does this tactic invoke a substrate verb? R1's test."""
        return bool(self.verb_of.get(place, ""))

    def increment(self, place: str, exploitability: float = 0.0) -> float:
        """``d`` for one movement-arm visit.

        **Zero for a dwell-only visit under R1** — it consumes the attacker's time
        and dispatches nothing, so it contributes decay and no signal. That is the
        whole of the low-and-slow mechanism: silence is what lets the level fall.
        """
        if place not in self.tier_of:
            raise ExposureCompileError(
                f"no declared observability tier for place {place!r}; the ranking "
                "is complete over the fifteen tactics, so an unranked place means "
                "the net and the declared family have diverged"
            )
        verb = self.verb_of.get(place, "")
        if not verb and not self.score_dwell_only:
            return 0.0
        if verb and self.verb_level:
            tier = self.verb_tier_of[verb]
        else:
            tier = self.tier_of[place]
        return tier_increment(tier, self.rho) * cvss_factor(
            exploitability, self.delta, self.direction
        )

    def verb_increment(self, verb: str) -> float:
        """``d`` for one baseline-arm action. **No CVSS term**, structurally: the
        native attack record carries no vulnerability figure, which is why
        cross-arm figures are primary at ``delta = 0``."""
        try:
            tier = self.verb_tier_of[verb]
        except KeyError:
            raise ExposureCompileError(
                f"no declared observability tier for native verb {verb!r}"
            ) from None
        return tier_increment(tier, self.rho)

    def decay(self, gap: float) -> float:
        """``exp(−Δt / τ)`` — the fraction of the level that survives a gap."""
        return math.exp(-max(0.0, float(gap)) / self.tau)


def _verb_tiers(
    tier_of: Mapping[str, int], preimage: Mapping[str, tuple[str, ...]]
) -> dict[str, int]:
    """A native verb's tier is the **minimum** over the tactics that map to it.

    Charitable to the baseline on purpose. The minimum is the quietest reading
    available, so if the inherited attacker still reads louder than the profiled
    one, the finding is stronger than the construction that produced it. Taking
    the mean or the maximum would hand the prediction its own result.
    """
    out: dict[str, int] = {}
    for verb, tactics in preimage.items():
        if not tactics:
            raise ExposureCompileError(f"native verb {verb!r} has an empty preimage")
        out[verb] = min(tier_of[t] for t in tactics)
    return out


def exposure_model(
    rules: ExposureRules | None = None,
    *,
    tau: float | None = None,
    rho: float | None = None,
    delta: float | None = None,
    direction: str = INVERSE,
    tier_overrides: Mapping[str, int] | None = None,
    score_dwell_only: bool = False,
    verb_level: bool = False,
) -> ExposureModel:
    """Resolve one point of the declared family.

    Every parameter defaults to its declared value; each is overridable so the
    sweep can move one at a time. ``tier_overrides`` moves a bimodal tactic to its
    alternative rung — the movement-arm and baseline-arm tables are both rebuilt
    from it, so the two arms can never be scored against different tier
    assignments by accident.

    ``score_dwell_only`` (R1) and ``verb_level`` (R2) default to the **ruled**
    semantics of 2026-08-06: dwell-only visits do not score, and arm-versus-arm
    readings pass ``verb_level=True`` so both sides are scored by one rule. The
    superseded convention is reachable with ``score_dwell_only=True``, because the
    comparison between the two is itself a reported result.
    """
    rules = rules if rules is not None else load_exposure_rules()
    tiers = dict(rules.tier_of)
    for tactic, tier in (tier_overrides or {}).items():
        if tactic not in tiers:
            raise ExposureCompileError(
                f"cannot override the tier of {tactic!r}: it carries no declared tier"
            )
        tiers[tactic] = int(tier)
    return ExposureModel(
        tau=rules.tau if tau is None else float(tau),
        rho=rules.rho if rho is None else float(rho),
        delta=rules.delta if delta is None else float(delta),
        direction=direction,
        tier_of=tiers,
        verb_tier_of=_verb_tiers(tiers, rules.verb_preimage),
        score_dwell_only=bool(score_dwell_only),
        verb_level=bool(verb_level),
        verb_of={
            tactic: verb
            for verb, tactics in rules.verb_preimage.items()
            for tactic in tactics
        },
    )


# ---------------------------------------------------------------------------
# The compiled view and its reproduction check
# ---------------------------------------------------------------------------

#: The alternative placements the view compiles beside the declared ones, so the
#: swept cells are on disk rather than reconstructed by whoever reads the record.
SWEPT_PLACEMENTS: tuple[tuple[str, dict[str, int]], ...] = (
    ("declared", {}),
    ("recon_active", {"reconnaissance": 3}),
    ("lateral_exploit", {"lateral-movement": 3}),
)


def view_document(rules: ExposureRules) -> dict:
    """The compiled increment view: every tactic and every native verb, at the
    declared ``rho``, under each swept tier placement."""
    cells: dict[str, dict] = {}
    for name, overrides in SWEPT_PLACEMENTS:
        model = exposure_model(rules, tier_overrides=overrides)
        cells[name] = {
            "tier_overrides": overrides,
            "tactics": {
                t: {
                    "tier": model.tier_of[t],
                    "increment": round(tier_increment(model.tier_of[t], rules.rho), 10),
                }
                for t in rules.tactics
            },
            "native_verbs": {
                v: {
                    "tier": model.verb_tier_of[v],
                    "increment": round(tier_increment(model.verb_tier_of[v], rules.rho), 10),
                }
                for v in rules.verbs
            },
        }
    return {
        "meta": {
            "generated_by": "python -m mtdsim.l3_simulation.movement.exposure --write",
            "rules": "data/ogasp/movement/exposure_rules.json",
            "note": (
                "Generated. Never hand-edit. Increments are shown at the DECLARED "
                "rho; other rho values rescale every cell by the same rule, so the "
                "view pins the tier assignment rather than one point of the sweep. "
                "The CVSS term is not compiled here: it is per-action, not per-tactic."
            ),
            "rho": rules.rho,
        },
        "placements": cells,
    }


def write_view(rules: ExposureRules, path: Path | str = INCREMENTS_VIEW_PATH) -> Path:
    """Regenerate the compiled view on disk."""
    path = Path(path)
    path.write_text(
        json.dumps(view_document(rules), indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    return path


def check_view(
    rules: ExposureRules, path: Path | str = INCREMENTS_VIEW_PATH
) -> list[str]:
    """Re-compile the view and report every cell that differs from what is
    committed. An empty list is the 0-of-N reproduction check."""
    path = Path(path)
    if not path.exists():
        return [f"{path} does not exist — run --write"]
    committed = json.loads(path.read_text(encoding="utf-8"))
    fresh = view_document(rules)
    problems: list[str] = []
    for placement, block in fresh["placements"].items():
        old = committed.get("placements", {}).get(placement)
        if old is None:
            problems.append(f"{placement}: missing from the committed view")
            continue
        for group in ("tactics", "native_verbs"):
            for key, cell in block[group].items():
                was = old.get(group, {}).get(key)
                if was != cell:
                    problems.append(
                        f"{placement}/{group}/{key}: committed {was} != compiled {cell}"
                    )
    return problems


def view_cell_count(rules: ExposureRules) -> int:
    """How many cells the reproduction check covers — reported with its verdict,
    so ``0 of N`` is a statement rather than an assertion."""
    return len(SWEPT_PLACEMENTS) * (len(rules.tactics) + len(rules.verbs))


def _main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Compile the declared axis-5 exposure family into its "
        "increment view, or check that what is committed still follows from the rules."
    )
    parser.add_argument("--write", action="store_true", help="regenerate the compiled view")
    parser.add_argument(
        "--check", action="store_true", help="re-compile the view and report differing cells"
    )
    args = parser.parse_args(argv)
    if not (args.write or args.check):
        parser.error("pass --write or --check")

    rules = load_exposure_rules()
    if args.write:
        print(f"wrote {write_view(rules)}")
    if args.check:
        problems = check_view(rules)
        print(
            f"exposure increments: {len(problems)} differing cells "
            f"(of {view_cell_count(rules)})"
        )
        for line in problems[:20]:
            print(f"    {line}")
        if len(problems) > 20:
            print(f"    … and {len(problems) - 20} more")
        if problems:
            print(
                "\nREPRODUCTION CHECK FAILED — the committed increment view no longer "
                "follows from the rules. Either the rules changed and the view needs "
                "regenerating, or the view was hand-edited."
            )
            return 1
        print("\nreproduction check passed: the committed view follows from the rules")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(_main())


__all__ = [
    "BIMODAL_TACTICS",
    "DIRECT",
    "DIRECTIONS",
    "EXPOSURE_RULES_PATH",
    "INCREMENTS_VIEW_PATH",
    "INVERSE",
    "MAX_TIER",
    "MIN_TIER",
    "SWEPT_PLACEMENTS",
    "ExposureCompileError",
    "ExposureModel",
    "ExposureRules",
    "check_view",
    "cvss_factor",
    "exposure_model",
    "load_exposure_rules",
    "tier_increment",
    "view_cell_count",
    "view_document",
    "write_view",
]
