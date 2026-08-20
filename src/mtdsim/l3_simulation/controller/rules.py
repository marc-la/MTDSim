"""Compile the outcome-overlay rules into the complete 210-pair tables.

The overlay's values are **rule-generated, never hand-set** — the discipline the
declared-value precedent requires of any number reasoned from judgement rather
than measured (``docs/implementation/declared_value_provenance.md`` §1). This
module is the generator that discipline names: it reads the rule set
(``data/ogasp/controller/outcome_rules.json``) and emits the compiled per-pair
views the runtime loads, and it can re-emit any committed view and report the
per-cell diff — the reproduction check that separates "these values follow from
stated rules" from "these values were fitted afterwards".

Three terms decide a pair's value, applied in this order:

1. **The relationship** — forward / lateral / backward, from a signed stage
   offset. Which ordering supplies that offset is a *selected* input
   (:class:`RuleSpec.relationship_source`): the original five-band kill-chain
   prior (``"bands"``, declared), or the four-stage APT-lifecycle consensus
   (``"consensus_stages"``, sourced from five published lifecycle models —
   ``docs/implementation/pipeline/ogasp/lifecycle_consensus.md``).
2. **The first matching rule** — the ordered success / failure rule lists, first
   match wins. Enablement, the foothold gates, and the dampers live here.
3. **The distance kernel** — a geometric decay in how many lifecycle stages the
   transition crosses, forward and backward with separate ratios and a zero
   floor. It multiplies the rule's value; it never replaces it.

So a compiled cell is ``rule_value * d(a, b)``, and with the distance term
switched off (``distance=False``) the compiler reproduces the pre-distance table
exactly — which is how every registered overlay version is generated from one
rule set rather than from two divergent files.

One further switch, ``success_passthrough``, compiles the **success** table to
the constant 1.0 (rule id ``passthrough``) while the failure table is compiled
as usual. Under the composition rule a factor of 1.0 at every destination is a
no-op, so a success verdict then routes on the base flow proportions unchanged
and only a failure verdict conditions the walk — the *failure-only* overlay
variant whose feasibility ``success_null_overlay_feasibility.md`` studies. It is a
compilation option, not a rule edit: the five success rules stay in the rule set
and are simply not consulted, so the variant is rule-generated and reproducible
like every other, and it reverts by flipping the flag.

Determinism: sorted iteration throughout, no clock, no randomness. Same rules +
same spec -> byte-identical tables.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path

# …/src/mtdsim/l3_simulation/controller/rules.py -> repo root is parents[4].
_REPO_ROOT = Path(__file__).resolve().parents[4]
CONTROLLER_DIR = _REPO_ROOT / "data" / "ogasp" / "controller"
RULES_PATH = CONTROLLER_DIR / "outcome_rules.json"
CONSENSUS_PATH = CONTROLLER_DIR / "lifecycle_consensus.json"

VERDICTS: tuple[str, ...] = ("success", "failure")

#: The two orderings a relationship can be read from. ``bands`` is the original
#: declared five-band kill-chain prior; ``consensus_stages`` is the four-stage
#: literature consensus. They disagree on 40 of the 210 pairs, all of them inside
#: the consensus's weakly-ordered post-intrusion middle.
RELATIONSHIP_SOURCES: frozenset[str] = frozenset({"bands", "consensus_stages"})

FORWARD, LATERAL, BACKWARD = "forward", "lateral", "backward"

#: The rule id a success cell carries when the spec compiles the success table
#: as a pass-through (``RuleSpec.success_passthrough``). Its value is always 1.0
#: — the multiplicative identity — so composition leaves the base out-set
#: untouched on a success verdict. It is not a member of the rule set's
#: ``success_rules`` list: the rules are not edited, they are not consulted.
PASSTHROUGH_RULE = "passthrough"


class RuleCompileError(ValueError):
    """Raised when the rule set or the spec cannot produce a table — an unknown
    relationship source, a rule id the compiler does not implement, or a tactic
    the ordering does not seat."""


@dataclass(frozen=True)
class DistanceKernel:
    """The declared lifecycle-distance kernel (``lifecycle_consensus.md`` §6).

    ``gamma`` decays forward travel per extra stage crossed, ``delta_ratio``
    decays backward travel, and ``z`` is the floor below which a value reads as
    exactly zero. Forward and backward are deliberately separate quantities: a
    campaign falling back three stages after a failure is ordinary, whereas one
    leaping forward three stages after a success is the thing being suppressed.

    The floor comparison is **strict** (``d < z``), so a value sitting exactly on
    the floor survives. That matters at one swept corner — ``gamma = 0.1`` puts
    the two-stage forward skip at exactly ``0.1`` — and is stated here rather
    than left to the reader of a float comparison.
    """

    gamma: float = 0.25
    delta_ratio: float = 0.5
    z: float = 0.1

    def raw(self, delta: int) -> float:
        """The kernel before the floor is applied."""
        if delta == 0:
            return 1.0
        if delta > 0:
            return self.gamma ** (delta - 1)
        return self.delta_ratio ** (-delta - 1)

    def __call__(self, delta: int) -> float:
        """The kernel with the floor applied — the factor a pair's value takes."""
        value = self.raw(delta)
        return 0.0 if value < self.z else value

    def as_dict(self) -> dict[str, float]:
        return {"gamma": self.gamma, "delta_ratio": self.delta_ratio, "z": self.z}


@dataclass(frozen=True)
class RuleSpec:
    """One compilation of the rule set: which ordering, and whether distance applies.

    A registered overlay version is exactly a ``RuleSpec`` plus the rule set it
    was compiled from, which is why the overlay registry can regenerate and
    re-check every version it carries.
    """

    relationship_source: str = "consensus_stages"
    distance: bool = True
    kernel: DistanceKernel = DistanceKernel()
    #: Compile the success table as the constant 1.0 (rule ``passthrough``) so a
    #: success verdict routes on the base proportions unchanged; the failure
    #: table is unaffected. The failure-only overlay variant.
    success_passthrough: bool = False

    def __post_init__(self) -> None:
        if self.relationship_source not in RELATIONSHIP_SOURCES:
            raise RuleCompileError(
                f"unknown relationship_source {self.relationship_source!r}; "
                f"expected one of {sorted(RELATIONSHIP_SOURCES)}"
            )

    def with_kernel(self, **params: float) -> "RuleSpec":
        """This spec with some kernel parameters replaced — the sweep's one knob."""
        return replace(self, kernel=replace(self.kernel, **params))


@dataclass(frozen=True)
class RuleSet:
    """The loaded rule set: the model, the ordered rules, and the orderings.

    ``bands`` and ``stage_of`` are both carried so a single rule set compiles
    either relationship source; ``stage_of`` is read from the lifecycle-consensus
    artefact rather than copied into the rules file, so the ordering has one home.
    """

    bands: dict[str, int]
    stage_of: dict[str, int]
    enables: dict[str, tuple[str, ...]]
    pre_foothold: frozenset[str]
    values: dict[str, dict[str, float]]  # verdict -> rule id -> value
    order: dict[str, tuple[str, ...]]  # verdict -> rule ids, in match order
    doc: dict  # the raw rules document (ledger, meta, model)
    consensus: dict  # the raw lifecycle-consensus document

    @property
    def tactics(self) -> tuple[str, ...]:
        return tuple(sorted(self.bands))

    def ordering(self, source: str) -> dict[str, int]:
        if source == "bands":
            return self.bands
        if source == "consensus_stages":
            return self.stage_of
        raise RuleCompileError(f"unknown relationship_source {source!r}")


def load_rule_set(
    rules_path: Path | str = RULES_PATH,
    consensus_path: Path | str = CONSENSUS_PATH,
) -> RuleSet:
    """Read the rule set and the lifecycle-consensus ordering it folds in.

    Loud on disagreement: the two artefacts must seat exactly the same tactic
    set, so a tactic added to one and not the other fails here rather than
    compiling to a silently wrong table.
    """
    doc = json.loads(Path(rules_path).read_text(encoding="utf-8"))
    consensus = json.loads(Path(consensus_path).read_text(encoding="utf-8"))
    model = doc["model"]
    bands = {k: int(v) for k, v in model["bands"].items()}
    stage_of = {k: int(v) for k, v in consensus["stage_of"].items()}
    if set(bands) != set(stage_of):
        raise RuleCompileError(
            "the rules' band map and the consensus stage map seat different "
            f"tactics: only-in-bands={sorted(set(bands) - set(stage_of))}, "
            f"only-in-consensus={sorted(set(stage_of) - set(bands))}"
        )
    return RuleSet(
        bands=bands,
        stage_of=stage_of,
        enables={k: tuple(v) for k, v in model["enables_on_success"].items()},
        pre_foothold=frozenset(model["pre_foothold"]),
        values={
            "success": {r["id"]: float(r["value"]) for r in doc["success_rules"]},
            "failure": {r["id"]: float(r["value"]) for r in doc["failure_rules"]},
        },
        order={
            "success": tuple(r["id"] for r in doc["success_rules"]),
            "failure": tuple(r["id"] for r in doc["failure_rules"]),
        },
        doc=doc,
        consensus=consensus,
    )


def kernel_from_consensus(consensus: dict) -> DistanceKernel:
    """The declared kernel parameters, read from the consensus artefact.

    The parameters are declared *there* — they are the literature half's output —
    so the compiler reads them rather than restating them.
    """
    declared = consensus["declared_parameters"]
    return DistanceKernel(
        gamma=float(declared["gamma"]["value"]),
        delta_ratio=float(declared["delta_ratio"]["value"]),
        z=float(declared["z"]["value"]),
    )


def relationship(src: str, dst: str, ordering: dict[str, int]) -> str:
    """Forward / lateral / backward, by the sign of the stage offset."""
    delta = ordering[dst] - ordering[src]
    if delta > 0:
        return FORWARD
    if delta < 0:
        return BACKWARD
    return LATERAL


def _success_rule(rs: RuleSet, src: str, dst: str, ordering: dict[str, int]) -> str:
    """The first matching success rule for a pair. Order is the rules file's.

    The enablement tier leads: a destination the source's success specifically
    confers the capability for is the modal next move whatever the relationship
    says. Below it the relationship decides, with a sharper penalty for
    regressing all the way to a preparation-stage tactic.
    """
    if dst in rs.enables.get(src, ()):
        return "enabled"
    rel = relationship(src, dst, ordering)
    if rel == FORWARD:
        return "forward"
    if rel == LATERAL:
        return "lateral"
    if ordering[dst] == 0:
        return "backward_to_prep"
    return "backward"


def _failure_rule(rs: RuleSet, src: str, dst: str, ordering: dict[str, int]) -> str:
    """The first matching failure rule for a pair. Order is the rules file's.

    The two dependency gates come first (a failed intrusion cannot be followed by
    a move that needs the foothold it did not win), then the two dampers, then
    the plain relationship ladder — backward dominant, lateral next, forward
    soft-suppressed.
    """
    if src == "initial-access" and dst not in rs.pre_foothold:
        return "ia_gate_foothold"
    if src == "reconnaissance" and dst == "initial-access":
        return "recon_gate_initial_access"
    if src == "reconnaissance" and dst not in rs.pre_foothold:
        return "recon_gate_deep"
    rel = relationship(src, dst, ordering)
    if src not in rs.pre_foothold and dst in rs.pre_foothold and rel == BACKWARD:
        return "preintrusion_damper"
    if dst == "execution" and rel == BACKWARD:
        return "execution_damper"
    if rel == BACKWARD:
        return "backward"
    if rel == LATERAL:
        return "lateral"
    return "forward_from_foothold" if src not in rs.pre_foothold else "forward_from_prep"


_RULE_FOR = {"success": _success_rule, "failure": _failure_rule}


def compile_pair(
    rs: RuleSet, verdict: str, src: str, dst: str, spec: RuleSpec
) -> dict:
    """One compiled cell: the rule that fired, its value, and the distance factor.

    The cell records ``d`` and the signed offset alongside the value so a reader
    of the compiled table can see *why* a value is what it is without
    re-running the compiler.
    """
    delta = rs.stage_of[dst] - rs.stage_of[src]
    if verdict == "success" and spec.success_passthrough:
        # The multiplicative identity, deliberately without the distance term:
        # on a success verdict the walk is the corpus's own routing, nothing
        # declared multiplies it. The offset is still recorded for the reader.
        return {"v": 1.0, "rule": PASSTHROUGH_RULE, "delta": delta}
    ordering = rs.ordering(spec.relationship_source)
    rule_id = _RULE_FOR[verdict](rs, src, dst, ordering)
    base = rs.values[verdict][rule_id]
    factor = spec.kernel(delta) if spec.distance else 1.0
    cell = {"v": round(base * factor, 6), "rule": rule_id}
    if spec.distance:
        cell["d"] = round(factor, 6)
        cell["delta"] = delta
    return cell


def compile_table(rs: RuleSet, verdict: str, spec: RuleSpec) -> dict[str, dict[str, dict]]:
    """The complete ``by_source[src][dst]`` table for one verdict.

    Complete means all 210 ordered pairs (15 x 14, no self-loops) — the whole
    declared space, not the corpus-present subset, so a different corpus that
    introduces an edge is already weighted.
    """
    tactics = rs.tactics
    return {
        src: {
            dst: compile_pair(rs, verdict, src, dst, spec)
            for dst in tactics
            if dst != src
        }
        for src in tactics
    }


def compile_overlay(rs: RuleSet, spec: RuleSpec) -> dict[str, dict[str, dict[str, dict]]]:
    """Both verdict tables, keyed ``verdict -> src -> dst -> cell``."""
    return {v: compile_table(rs, v, spec) for v in VERDICTS}


def compile_values(rs: RuleSet, spec: RuleSpec) -> dict[str, dict[str, dict[str, float]]]:
    """Both verdict tables reduced to bare values — what a sweep point needs.

    Shaped for :class:`~mtdsim.l3_simulation.controller.outcome.OutcomeOverlay`,
    so a swept parameter set can be composed in memory without writing a file.
    """
    return {
        verdict: {
            src: {dst: cell["v"] for dst, cell in dsts.items()}
            for src, dsts in table.items()
        }
        for verdict, table in compile_overlay(rs, spec).items()
    }


def diff_against(
    rs: RuleSet, spec: RuleSpec, committed: dict[str, dict], *, tolerance: float = 1e-9
) -> list[str]:
    """Re-compile and diff against a committed view — the reproduction check.

    ``committed`` is ``verdict -> the view document`` (each with a ``by_source``
    block). Returns one human-readable line per differing cell, empty when the
    compilation reproduces the committed tables exactly. An empty list is the
    claim "these values follow from the rules"; a non-empty one says a table was
    edited away from its rules, which is the failure mode the check exists to
    catch.
    """
    problems: list[str] = []
    for verdict in VERDICTS:
        got = compile_table(rs, verdict, spec)
        want = committed[verdict]["by_source"]
        for src in sorted(set(got) | set(want)):
            gd, wd = got.get(src, {}), want.get(src, {})
            for dst in sorted(set(gd) | set(wd)):
                g, w = gd.get(dst), wd.get(dst)
                if g is None or w is None:
                    problems.append(f"{verdict} {src}->{dst}: present in only one table")
                    continue
                if abs(float(g["v"]) - float(w["v"])) > tolerance:
                    problems.append(
                        f"{verdict} {src}->{dst}: value {w['v']} committed vs {g['v']} compiled"
                    )
                elif g["rule"] != w["rule"]:
                    problems.append(
                        f"{verdict} {src}->{dst}: rule {w['rule']!r} committed vs "
                        f"{g['rule']!r} compiled"
                    )
    return problems


def view_document(rs: RuleSet, verdict: str, spec: RuleSpec, meta: dict) -> dict:
    """One compiled view, ready to write: the verdict, its provenance, the table."""
    return {
        "verdict": verdict,
        "_meta": {
            **meta,
            "generated_from": "outcome_rules.json + lifecycle_consensus.json — "
            "DO NOT hand-edit; regenerate with "
            "`python -m mtdsim.l3_simulation.controller.rules --write`",
            "relationship_source": spec.relationship_source,
            "distance": spec.kernel.as_dict() if spec.distance else None,
            "success_passthrough": spec.success_passthrough,
            "coverage": "complete 210 directed pairs (corpus-agnostic)",
            "format": (
                "by_source[src][dst] = {v: value, rule: rule-id"
                + (", d: distance factor, delta: signed stage offset}" if spec.distance else "}")
                + "; rationale via outcome_rules.json rules[rule]"
            ),
        },
        "by_source": compile_table(rs, verdict, spec),
    }


def spec_from_registry_entry(spec: dict) -> RuleSpec:
    """A :class:`RuleSpec` from a registry manifest's ``spec`` block."""
    kernel = spec.get("kernel") or {}
    return RuleSpec(
        relationship_source=str(spec.get("relationship_source", "consensus_stages")),
        distance=bool(spec.get("distance", True)),
        kernel=DistanceKernel(
            gamma=float(kernel.get("gamma", 0.25)),
            delta_ratio=float(kernel.get("delta_ratio", 0.5)),
            z=float(kernel.get("z", 0.1)),
        ),
        success_passthrough=bool(spec.get("success_passthrough", False)),
    )


def check_registry(rs: RuleSet | None = None) -> dict[str, list[str]]:
    """Re-compile every registered overlay version and diff it against what is
    committed. ``{version name: [differing cells]}`` — all-empty is the pass."""
    from mtdsim.l3_simulation.controller.outcome import load_overlay_registry

    rs = rs if rs is not None else load_rule_set()
    out: dict[str, list[str]] = {}
    for version in load_overlay_registry().versions:
        committed = {
            verdict: json.loads(path.read_text(encoding="utf-8"))
            for verdict, path in version.files().items()
        }
        out[version.name] = diff_against(
            rs, spec_from_registry_entry(version.spec), committed
        )
    return out


def write_registry(rs: RuleSet | None = None) -> list[Path]:
    """Regenerate every registered version's compiled views in place."""
    from mtdsim.l3_simulation.controller.outcome import load_overlay_registry

    rs = rs if rs is not None else load_rule_set()
    written: list[Path] = []
    for version in load_overlay_registry().versions:
        spec = spec_from_registry_entry(version.spec)
        meta = {
            "overlay_version": version.name,
            "status": version.rationale,
            "construction": version.construction,
            "record": version.record,
        }
        for verdict, path in version.files().items():
            path.write_text(
                json.dumps(view_document(rs, verdict, spec, meta), indent=2) + "\n",
                encoding="utf-8",
            )
            written.append(path)
    return written


def _main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Compile the outcome-overlay rules into the registered "
        "210-pair views, or check that what is committed still follows from them."
    )
    parser.add_argument(
        "--write", action="store_true", help="regenerate every registered version"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="re-compile every registered version and report differing cells",
    )
    args = parser.parse_args(argv)
    if not (args.write or args.check):
        parser.error("pass --write or --check")

    rs = load_rule_set()
    if args.write:
        for path in write_registry(rs):
            print(f"wrote {path}")
    if args.check:
        failed = False
        for name, problems in check_registry(rs).items():
            print(f"{name}: {len(problems)} differing cells (of 420)")
            for line in problems[:20]:
                print(f"    {line}")
            if len(problems) > 20:
                print(f"    … and {len(problems) - 20} more")
            failed = failed or bool(problems)
        if failed:
            print("\nREPRODUCTION CHECK FAILED — a committed view no longer follows "
                  "from the rules. Either the rules changed and the views need "
                  "regenerating, or a view was hand-edited.")
            return 1
        print("\nreproduction check passed: every committed view follows from the rules")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI
    raise SystemExit(_main())


__all__ = [
    "CONSENSUS_PATH",
    "CONTROLLER_DIR",
    "RELATIONSHIP_SOURCES",
    "RULES_PATH",
    "VERDICTS",
    "DistanceKernel",
    "PASSTHROUGH_RULE",
    "RuleCompileError",
    "RuleSet",
    "RuleSpec",
    "check_registry",
    "compile_overlay",
    "compile_pair",
    "compile_table",
    "compile_values",
    "diff_against",
    "kernel_from_consensus",
    "load_rule_set",
    "relationship",
    "spec_from_registry_entry",
    "view_document",
    "write_registry",
]
