"""Load and resolve the tactic -> MTDSim-phase controller map.

Reads ``data/ogasp/controller.csv`` (the CKC-mediated position map, experiment
1) and exposes it as a plain ``tactic -> sim_phase`` lookup for the movement
layer. No net, no substrate, no simulation here — just the mapping, so it can be
swapped (it is an input parameter of the research, not a fixed truth).

Ground truth for the mapping's *shape*:
``docs/implementation/pipeline/ogasp/controller.md``.
"""
from __future__ import annotations

import csv
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

# Default artefact location, relative to the repo root (…/src/mtdsim/l3_simulation/
# controller/controller.py -> repo root is parents[4]).
DEFAULT_CSV = Path(__file__).resolve().parents[4] / "data" / "ogasp" / "controller.csv"

_REQUIRED_COLUMNS = {
    "tactic",
    "attack_tactic_id",
    "ckc_phase",
    "sim_phase",
    "coverage",
}


@dataclass(frozen=True)
class ControllerRow:
    """One tactic's route through the CKC to a single MTDSim verb."""

    tactic: str
    attack_tactic_id: str
    ckc_phase: str
    sim_phase: str
    coverage: str  # "direct" (tactic's CKC phase owns the verb) | "fallback"
    note: str = ""


@dataclass(frozen=True)
class Controller:
    """The resolved tactic -> MTDSim-phase dispatch map."""

    rows: tuple[ControllerRow, ...]

    @property
    def tactics(self) -> tuple[str, ...]:
        return tuple(r.tactic for r in self.rows)

    def phase_for(self, tactic: str) -> str:
        """Return the single MTDSim verb the given tactic dispatches.

        Raises ``KeyError`` if the tactic is not in the map — the movement layer
        must only ask about tactics the net carries.
        """
        for row in self.rows:
            if row.tactic == tactic:
                return row.sim_phase
        raise KeyError(f"tactic not in controller map: {tactic!r}")

    def as_dict(self) -> dict[str, str]:
        """The bare ``tactic -> sim_phase`` mapping the attacker consumes."""
        return {r.tactic: r.sim_phase for r in self.rows}


def load_controller(path: Path | str | None = None) -> Controller:
    """Load and validate the controller map from ``controller.csv``.

    Validation is loud, not silent: unknown ``sim_phase`` values, missing
    columns, duplicate tactics, or a tactic resolving to more than one verb all
    raise, so a malformed input parameter fails at load rather than mid-run.
    """
    csv_path = Path(path) if path is not None else DEFAULT_CSV
    with csv_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = set(reader.fieldnames or [])
        missing = _REQUIRED_COLUMNS - header
        if missing:
            raise ValueError(f"controller.csv missing columns: {sorted(missing)}")

        rows: list[ControllerRow] = []
        seen: set[str] = set()
        for raw in reader:
            tactic = raw["tactic"].strip()
            if tactic in seen:
                raise ValueError(f"duplicate tactic in controller.csv: {tactic!r}")
            seen.add(tactic)

            sim_phase = raw["sim_phase"].strip()
            if sim_phase not in SIM_PHASES:
                raise ValueError(
                    f"tactic {tactic!r} maps to unknown sim_phase {sim_phase!r}; "
                    f"expected one of {sorted(SIM_PHASES)}"
                )
            rows.append(
                ControllerRow(
                    tactic=tactic,
                    attack_tactic_id=raw["attack_tactic_id"].strip(),
                    ckc_phase=raw["ckc_phase"].strip(),
                    sim_phase=sim_phase,
                    coverage=raw["coverage"].strip(),
                    note=raw.get("note", "").strip(),
                )
            )

    if not rows:
        raise ValueError(f"controller.csv is empty: {csv_path}")
    return Controller(rows=tuple(rows))
