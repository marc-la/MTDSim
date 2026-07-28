"""Load the success/failure outcome-overlay split and compose it (M2).

This module reads the success/failure signal back from the substrate and turns
it into net routing:

    docs/implementation/pipeline/ogasp/success_failure_overlay_design.md

Data (rule-based notation — see ``data/ogasp/controller/``):
    outcome_rules.json   — the SOURCE OF TRUTH: the model (bands / enables /
        foothold / the distance term) + the ordered success/failure rules, each
        carrying its value and ONE rationale. Values are rule-generated
        (first-match-wins), compiled by
        :mod:`mtdsim.l3_simulation.controller.rules`.
    overlays/<version>/success.json, failure.json   — COMPILED VIEWS: the
        complete directed tactic-pair space (210 = 15*14, corpus-agnostic) as
        ``by_source[src][dst] = {"v": value, "rule": rule-id, …}``. Generated
        from the rules — do NOT hand-edit; regenerate. The rationale for any pair
        is looked up from ``outcome_rules.json`` by its ``rule`` id (stored once
        per rule, never duplicated per pair).

**The overlay is versioned data, and this layer only reads it.** Every value set
that has been run lives under ``data/ogasp/controller/overlays/``, one directory
per version plus a ``manifest.json`` recording how each version was compiled,
which experiment consumed it, and what it produced. A caller selects a version
*by name*, exactly as it selects a controller mapping::

    load_outcome_overlay()                              # the manifest's default
    load_outcome_overlay(version="v2_lifecycle_distance")   # explicit selection
    load_outcome_overlay(files={...})                    # ad-hoc files (tests)
    OutcomeOverlay.from_values(compile_values(...))      # ad-hoc in memory (sweeps)

The default is the *experiment-1* value rather than the newest, for the same
reason the mapping registry's is: promoting the newest version to default would
re-bake an experiment's choice into the pipeline.

Value semantics (per file ``_meta``):
    overlay_v(src -> dst) in [0, 1] = given the dispatched verb at ``src`` came
    back with verdict ``v``, the conditional likelihood of ``dst`` as the next
    move (0 = will not happen, 1 = the single most likely next course of action).

Composition (M2), implemented in :meth:`OutcomeOverlay.compose`:
    w'(src -> dst) = base(src -> dst) * overlay_v(src -> dst)
                     ------------------------------------------
                     Σ_dst' base(src -> dst') * overlay_v(src -> dst')
    Only within-source ratios are load-bearing; the source out-set renormalises.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

Verdict = str  # "success" | "failure"  (binary outcome only, M2)

_VERDICTS: frozenset[Verdict] = frozenset({"success", "failure"})

# …/src/mtdsim/l3_simulation/controller/outcome.py -> repo root is parents[4].
_DATA_DIR = Path(__file__).resolve().parents[4] / "data" / "ogasp" / "controller"

#: The versioned overlay registry — the home of every value set that has been run.
REGISTRY_DIR = _DATA_DIR / "overlays"
MANIFEST_PATH = REGISTRY_DIR / "manifest.json"


@dataclass(frozen=True)
class OutcomeOverlay:
    """The loaded success/failure overlay, indexed ``verdict -> src -> dst -> value``.

    A read-only lookup over the two split files. The runtime composition
    (multiply the base out-weights by these values and renormalise within a
    source's out-set) is deliberately **not** implemented here yet — see
    :meth:`compose`.
    """

    by_verdict: dict[Verdict, dict[str, dict[str, float]]]
    by_rule: dict[Verdict, dict[str, dict[str, str]]]
    version: str = ""  # the registry version name, or "" for an ad-hoc load

    @classmethod
    def from_values(
        cls,
        by_verdict: dict[Verdict, dict[str, dict[str, float]]],
        *,
        version: str = "",
    ) -> "OutcomeOverlay":
        """An overlay from compiled values held in memory, with no rule tags.

        This is the seam the sensitivity sweep uses: a swept parameter set is
        compiled by :func:`mtdsim.l3_simulation.controller.rules.compile_values`
        and handed straight to a run, so a sweep never writes 210-pair files it
        would then have to clean up — and never hand-edits one.
        """
        return cls(by_verdict=by_verdict, by_rule={}, version=version)

    def value(self, verdict: Verdict, src: str, dst: str) -> float:
        """The overlay value for one directed pair under one verdict.

        Missing pairs return ``0.0`` — a pair the overlay does not carry is not
        a legal conditioned move under that verdict. (With complete coverage the
        overlay carries every ordered pair, so a miss means an unknown tactic.)
        """
        return self.by_verdict.get(verdict, {}).get(src, {}).get(dst, 0.0)

    def out_values(self, verdict: Verdict, src: str) -> dict[str, float]:
        """All ``dst -> value`` overlay entries for a source under a verdict."""
        return dict(self.by_verdict.get(verdict, {}).get(src, {}))

    def rule_for(self, verdict: Verdict, src: str, dst: str) -> str | None:
        """The id of the rule that generated this pair's value; ``None`` if not
        carried. The rationale lives once in ``outcome_rules.json`` under this id
        — never duplicated per pair."""
        return self.by_rule.get(verdict, {}).get(src, {}).get(dst)

    def compose(
        self,
        src: str,
        verdict: Verdict,
        base_out_weights: dict[str, float],
    ) -> dict[str, float]:
        """Condition the base out-distribution on the verdict and renormalise (M2).

        The rule (``success_failure_overlay_design.md`` §1)::

            w'(src->dst) = base(src->dst) * overlay_v(src->dst) / Σ

        Per destination ``dst`` in ``base_out_weights`` the factor is the overlay
        value for ``(src, dst)`` under this verdict **if that pair is present** in
        the overlay's ``by_source[src]``, **else 1.0** — an absent pair is an
        *unconditioned passthrough* (it keeps its base weight), while a pair
        carried with value ``0`` **hard-suppresses** the edge. This absent-vs-
        present-zero distinction is what makes the composition robust to any
        net/overlay pairing (plug-and-play): the complete-coverage overlay carries
        every ordered tactic pair, but a base net edge the overlay does not name
        (e.g. a self-loop) still routes rather than silently vanishing.

        The source out-set renormalises, so only within-source ratios are
        load-bearing (base proportions are conditioned, never re-derived —
        ``metrics_semantics.md`` §(f)). Returns an empty dict — the **stall**
        (design §3) — if the verdict suppressed every out-edge (Σ == 0); the
        movement driver reads that as walk-termination. Under the distance term a
        pair *can* now carry an exact zero (a jump the lifecycle consensus puts
        beyond the floor), so the stall is representable rather than arithmetically
        unreachable — but no place in any profile net loses its whole out-set at
        any swept parameter point, which is checked rather than assumed
        (``weight_sensitivity_study.md`` §3).
        """
        src_overlay = self.by_verdict.get(verdict, {}).get(src, {})
        composed: dict[str, float] = {}
        for dst, base_w in base_out_weights.items():
            factor = src_overlay[dst] if dst in src_overlay else 1.0
            weight = base_w * factor
            if weight > 0:
                composed[dst] = weight
        total = sum(composed.values())
        if total <= 0:
            return {}
        return {dst: weight / total for dst, weight in composed.items()}


@dataclass(frozen=True)
class OverlayVersion:
    """One registered overlay version: its files, and how it was compiled.

    ``spec`` is the compilation recipe — the relationship ordering and the
    distance kernel — so the generator can re-emit this version and diff it
    against what is committed. A version that cannot be regenerated from the
    rules is a version whose values were fitted, which is the thing the
    declared-value precedent forbids.
    """

    name: str
    directory: Path
    spec: dict
    created: str = ""
    construction: str = ""
    rationale: str = ""
    consumed_by: tuple[str, ...] = ()
    produced: str = ""
    record: str = ""
    immutable: bool = False

    def files(self) -> dict[Verdict, Path]:
        return {v: self.directory / f"{v}.json" for v in sorted(_VERDICTS)}


@dataclass(frozen=True)
class OverlayRegistry:
    """The overlay registry — every value set run, and which is the default."""

    versions: tuple[OverlayVersion, ...]
    default: str

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(v.name for v in self.versions)

    def get(self, name: str) -> OverlayVersion:
        for version in self.versions:
            if version.name == name:
                return version
        raise KeyError(
            f"unknown outcome-overlay version {name!r}; "
            f"registered: {sorted(self.names)}"
        )


def load_overlay_registry(manifest_path: Path | str | None = None) -> OverlayRegistry:
    """Load the overlay registry's manifest.

    Validation is loud: a version whose compiled files are missing, or a declared
    default naming no registered version, raises here rather than mid-run.
    """
    path = Path(manifest_path) if manifest_path is not None else MANIFEST_PATH
    with path.open(encoding="utf-8") as fh:
        doc = json.load(fh)

    entries = doc.get("versions")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path}: missing or empty 'versions' block")

    versions: list[OverlayVersion] = []
    for entry in entries:
        name = str(entry["name"])
        directory = path.parent / str(entry["dir"])
        version = OverlayVersion(
            name=name,
            directory=directory,
            spec=dict(entry.get("spec", {})),
            created=str(entry.get("created", "")),
            construction=str(entry.get("construction", "")),
            rationale=str(entry.get("rationale", "")),
            consumed_by=tuple(entry.get("consumed_by", ())),
            produced=str(entry.get("produced", "")),
            record=str(entry.get("record", "")),
            immutable=bool(entry.get("immutable", False)),
        )
        for verdict, file_path in version.files().items():
            if not file_path.is_file():
                raise ValueError(
                    f"{path}: version {name!r} is missing its {verdict} view: {file_path}"
                )
        versions.append(version)

    default = str(doc.get("default", ""))
    registry = OverlayRegistry(versions=tuple(versions), default=default)
    if default not in registry.names:
        raise ValueError(
            f"{path}: default {default!r} names no registered version "
            f"(registered: {sorted(registry.names)})"
        )
    return registry


def load_outcome_overlay(
    files: dict[Verdict, Path] | None = None,
    *,
    version: str | None = None,
    registry: OverlayRegistry | None = None,
) -> OutcomeOverlay:
    """Load one overlay version into an :class:`OutcomeOverlay`.

    Selection, in precedence order: explicit ``files`` (an ad-hoc pair, for tests
    and one-offs), else a named ``version`` from the registry, else the registry's
    declared default. Passing both ``files`` and ``version`` is a contradiction
    and raises.

    Validation is loud: each file's declared ``verdict`` must match its slot and
    be one of the two binary verdicts, and the ``by_source`` block is required.
    """
    if files is not None and version is not None:
        raise ValueError("pass either files or version, not both")

    name = ""
    if files is not None:
        paths = files
    else:
        reg = registry if registry is not None else load_overlay_registry()
        name = version if version is not None else reg.default
        paths = reg.get(name).files()

    by_verdict: dict[Verdict, dict[str, dict[str, float]]] = {}
    by_rule: dict[Verdict, dict[str, dict[str, str]]] = {}
    for verdict, path in paths.items():
        if verdict not in _VERDICTS:
            raise ValueError(
                f"unknown verdict {verdict!r}; expected one of {sorted(_VERDICTS)}"
            )
        with Path(path).open(encoding="utf-8") as fh:
            doc = json.load(fh)
        declared = doc.get("verdict")
        if declared != verdict:
            raise ValueError(
                f"{path}: declared verdict {declared!r} != expected {verdict!r}"
            )
        by_source = doc.get("by_source")
        if not isinstance(by_source, dict):
            raise ValueError(f"{path}: missing or malformed 'by_source' block")
        # Compiled-view cell is ``{"v": value, "rule": rule-id}`` (rule-based
        # notation). Tolerate a bare number too, for forward/backward flexibility.
        def _v(cell: object) -> float:
            return float(cell["v"] if isinstance(cell, dict) else cell)

        def _r(cell: object) -> str:
            return str(cell.get("rule", "")) if isinstance(cell, dict) else ""

        by_verdict[verdict] = {
            src: {dst: _v(cell) for dst, cell in dsts.items()}
            for src, dsts in by_source.items()
        }
        by_rule[verdict] = {
            src: {dst: _r(cell) for dst, cell in dsts.items()}
            for src, dsts in by_source.items()
        }
    return OutcomeOverlay(by_verdict=by_verdict, by_rule=by_rule, version=name)
