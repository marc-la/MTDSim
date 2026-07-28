"""Load and resolve the tactic -> MTDSim-phase controller map.

The controller is the seam between the net (which tactic the token sits on) and
the inherited substrate action set (which verb fires). It is an **input parameter
of the research, not a recovered truth** — there is no correct mapping to
discover, and different mappings are things the evaluation varies.

**The mapping is data, and this layer only reads it.** Every mapping that has
been tried lives in ``data/ogasp/controller/mappings/`` — one file per version
plus a ``manifest.json`` recording each version's rationale, which experiment
consumed it, and what it produced. A caller selects a version *by name*; nothing
here knows or prefers any experiment's mapping. Selecting a different mapping is
a data selection, never a code edit::

    load_controller()                      # the manifest's default
    load_controller(version="v2_partial")  # an explicit selection
    load_controller(path=some_csv)         # an ad-hoc file (tests, one-offs)

The default is the *experiment-1* value rather than the newest one, deliberately:
promoting the newest version to default would re-bake an experiment's choice into
the pipeline, which is the coupling the registry exists to remove.

**A tactic maps to [0, 1] verbs** (supervisor ruling S4). Several tactics may
share a verb, and a tactic for which no verb's real effect is a defensible
stand-in is declared **dwell-only**: :meth:`Controller.phase_for` returns ``None``
and the movement layer consumes time at that place without dispatching anything.
The invariant is that **silence stays an error while declared absence is legal** —
an empty verb without a ``dwell-only`` disposition raises at load.

Ground truth for the mappings' shape:
``docs/implementation/pipeline/ogasp/controller.md`` (version 1) and
``controller_mapping_v2.md`` (version 2).
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

# The six inherited MTDSim attack verbs (the "6 operationalised phases").
# Ground truth: mtdnetwork/operation/attack_operation.py (proceed_attack + the
# six _do_*/_execute_* pairs); catalogued in
# docs/implementation/pipeline/ogasp/attacker_phase_catalogue.md.
SIM_PHASES: frozenset[str] = frozenset(
    {
        "SCAN_HOST",
        "ENUM_HOST",
        "SCAN_PORT",
        "EXPLOIT_VULN",
        "BRUTE_FORCE",
        "SCAN_NEIGHBOR",
    }
)

# A tactic's two legal dispositions. "mapped" names a verb; "dwell-only" names
# none, and must say so rather than leaving the cell blank.
MAPPED = "mapped"
DWELL_ONLY = "dwell-only"
_DISPOSITIONS = frozenset({MAPPED, DWELL_ONLY})

# …/src/mtdsim/l3_simulation/controller/controller.py -> repo root is parents[4].
_REPO_ROOT = Path(__file__).resolve().parents[4]

#: The versioned mapping registry — the home of every mapping that has been tried.
REGISTRY_DIR = _REPO_ROOT / "data" / "ogasp" / "controller" / "mappings"
MANIFEST_PATH = REGISTRY_DIR / "manifest.json"

#: The experiment-1 artefact, retained verbatim at its original path. The
#: registry's ``v1_ckc_total`` is its re-expression in the registry schema, and a
#: test pins the two equal row-for-row so neither can drift.
LEGACY_CSV = _REPO_ROOT / "data" / "ogasp" / "controller.csv"

_REQUIRED_COLUMNS = {"tactic", "sim_phase"}


@dataclass(frozen=True)
class ControllerRow:
    """One tactic's disposition: a single MTDSim verb, or none at all."""

    tactic: str
    sim_phase: str | None  # the dispatched verb, or None for a dwell-only tactic
    disposition: str  # MAPPED | DWELL_ONLY
    attack_tactic_id: str = ""
    ckc_phase: str = ""  # version-1 provenance; empty where a version has no CKC step
    coverage: str = ""  # version-1 provenance: "direct" | "fallback"
    reason: str = ""  # why the row holds this value — the thing a reviewer reads

    @property
    def is_dwell_only(self) -> bool:
        return self.disposition == DWELL_ONLY


@dataclass(frozen=True)
class Controller:
    """The resolved tactic -> MTDSim-phase dispatch map, as selected."""

    rows: tuple[ControllerRow, ...]
    version: str = ""  # the registry version name, or "" for an ad-hoc file
    source: Path | None = None

    @property
    def tactics(self) -> tuple[str, ...]:
        return tuple(r.tactic for r in self.rows)

    @property
    def mapped_tactics(self) -> tuple[str, ...]:
        """The tactics that dispatch a verb."""
        return tuple(r.tactic for r in self.rows if not r.is_dwell_only)

    @property
    def dwell_only_tactics(self) -> tuple[str, ...]:
        """The tactics that dispatch nothing and consume time only."""
        return tuple(r.tactic for r in self.rows if r.is_dwell_only)

    def row_for(self, tactic: str) -> ControllerRow:
        for row in self.rows:
            if row.tactic == tactic:
                return row
        raise KeyError(f"tactic not in controller map: {tactic!r}")

    def phase_for(self, tactic: str) -> str | None:
        """The single MTDSim verb this tactic dispatches, or ``None`` if the
        tactic is dwell-only.

        ``None`` is a declared answer, not a lookup miss: an *unknown* tactic
        raises ``KeyError``, because the movement layer must only ask about
        tactics the net carries.
        """
        return self.row_for(tactic).sim_phase

    def is_dwell_only(self, tactic: str) -> bool:
        """Whether this tactic consumes time without dispatching a verb."""
        return self.row_for(tactic).is_dwell_only

    def as_dict(self) -> dict[str, str | None]:
        """``tactic -> sim_phase`` for every tactic, ``None`` where dwell-only."""
        return {r.tactic: r.sim_phase for r in self.rows}

    def dispatch_map(self) -> dict[str, str]:
        """``tactic -> sim_phase`` for the mapped tactics only."""
        return {r.tactic: r.sim_phase for r in self.rows if r.sim_phase is not None}


@dataclass(frozen=True)
class MappingVersion:
    """One registered mapping version and its provenance."""

    name: str
    path: Path
    created: str = ""
    coverage: str = ""
    rationale: str = ""
    consumed_by: tuple[str, ...] = ()
    produced: str = ""
    record: str = ""
    immutable: bool = False


@dataclass(frozen=True)
class MappingRegistry:
    """The mapping registry — every version tried, and which is the default."""

    versions: tuple[MappingVersion, ...]
    default: str

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(v.name for v in self.versions)

    def get(self, name: str) -> MappingVersion:
        for version in self.versions:
            if version.name == name:
                return version
        raise KeyError(
            f"unknown controller mapping version {name!r}; "
            f"registered: {sorted(self.names)}"
        )


def load_registry(manifest_path: Path | str | None = None) -> MappingRegistry:
    """Load the mapping registry's manifest.

    Validation is loud: an unreadable manifest, a version whose file is missing,
    or a declared default that names no registered version all raise here rather
    than surfacing mid-run.
    """
    path = Path(manifest_path) if manifest_path is not None else MANIFEST_PATH
    with path.open(encoding="utf-8") as fh:
        doc = json.load(fh)

    entries = doc.get("versions")
    if not isinstance(entries, list) or not entries:
        raise ValueError(f"{path}: missing or empty 'versions' block")

    versions: list[MappingVersion] = []
    for entry in entries:
        name = str(entry["name"])
        mapping_path = path.parent / str(entry["file"])
        if not mapping_path.is_file():
            raise ValueError(
                f"{path}: version {name!r} names a missing file: {mapping_path}"
            )
        versions.append(
            MappingVersion(
                name=name,
                path=mapping_path,
                created=str(entry.get("created", "")),
                coverage=str(entry.get("coverage", "")),
                rationale=str(entry.get("rationale", "")),
                consumed_by=tuple(entry.get("consumed_by", ())),
                produced=str(entry.get("produced", "")),
                record=str(entry.get("record", "")),
                immutable=bool(entry.get("immutable", False)),
            )
        )

    default = str(doc.get("default", ""))
    registry = MappingRegistry(versions=tuple(versions), default=default)
    if default not in registry.names:
        raise ValueError(
            f"{path}: default {default!r} names no registered version "
            f"(registered: {sorted(registry.names)})"
        )
    return registry


def load_controller(
    path: Path | str | None = None,
    *,
    version: str | None = None,
    registry: MappingRegistry | None = None,
) -> Controller:
    """Load and validate one controller mapping.

    Selection, in precedence order: an explicit ``path`` (an ad-hoc file), else a
    named ``version`` from the registry, else the registry's declared default.
    Passing both ``path`` and ``version`` is a contradiction and raises.

    Validation is loud, not silent: missing columns, duplicate tactics, unknown
    verbs, an unknown disposition, a dwell-only row that still names a verb, or —
    the S4 invariant — a row with no verb that does not *declare* itself
    dwell-only, all raise at load rather than mid-run.
    """
    if path is not None and version is not None:
        raise ValueError("pass either path or version, not both")

    name = ""
    if path is not None:
        csv_path = Path(path)
    else:
        reg = registry if registry is not None else load_registry()
        name = version if version is not None else reg.default
        csv_path = reg.get(name).path

    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = set(reader.fieldnames or [])
        missing = _REQUIRED_COLUMNS - header
        if missing:
            raise ValueError(f"{csv_path}: missing columns: {sorted(missing)}")

        rows: list[ControllerRow] = []
        seen: set[str] = set()
        for raw in reader:
            tactic = raw["tactic"].strip()
            if tactic in seen:
                raise ValueError(f"{csv_path}: duplicate tactic: {tactic!r}")
            seen.add(tactic)
            rows.append(_read_row(csv_path, tactic, raw))

    if not rows:
        raise ValueError(f"{csv_path}: no rows")
    return Controller(rows=tuple(rows), version=name, source=csv_path)


def _read_row(csv_path: Path, tactic: str, raw: dict[str, str]) -> ControllerRow:
    """Validate one row and resolve its disposition.

    A file with no ``disposition`` column (the legacy experiment-1 artefact) is
    read as all-mapped — but a blank verb is still an error there, so the
    "no silent rows" invariant holds for every input this layer accepts.
    """
    verb = (raw.get("sim_phase") or "").strip()
    disposition = (raw.get("disposition") or "").strip()

    if not disposition:
        disposition = MAPPED if verb else ""
    if disposition not in _DISPOSITIONS:
        if not disposition:
            # The S4 invariant, and the reason this branch exists at all: a tactic
            # may legally dispatch nothing, but it has to SAY so. An empty cell is
            # indistinguishable from an unfinished one, so it stays an error.
            raise ValueError(
                f"{csv_path}: tactic {tactic!r} names no verb and does not declare "
                f"itself {DWELL_ONLY!r}; a tactic may dispatch nothing, but silently "
                f"dispatching nothing is not allowed"
            )
        raise ValueError(
            f"{csv_path}: tactic {tactic!r} has unknown disposition "
            f"{disposition!r}; expected one of {sorted(_DISPOSITIONS)}"
        )

    if disposition == DWELL_ONLY:
        if verb:
            raise ValueError(
                f"{csv_path}: tactic {tactic!r} is declared {DWELL_ONLY!r} but "
                f"still names a verb ({verb!r})"
            )
        sim_phase: str | None = None
    else:
        if verb not in SIM_PHASES:
            raise ValueError(
                f"{csv_path}: tactic {tactic!r} maps to unknown sim_phase "
                f"{verb!r}; expected one of {sorted(SIM_PHASES)}"
            )
        sim_phase = verb

    return ControllerRow(
        tactic=tactic,
        sim_phase=sim_phase,
        disposition=disposition,
        attack_tactic_id=(raw.get("attack_tactic_id") or "").strip(),
        ckc_phase=(raw.get("ckc_phase") or "").strip(),
        coverage=(raw.get("coverage") or "").strip(),
        reason=(raw.get("reason") or raw.get("note") or "").strip(),
    )
