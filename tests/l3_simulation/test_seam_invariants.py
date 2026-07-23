"""Seam invariants for the L3 OGASP runtime — the module-boundary checks that
keep structure / policy / execution separate (verification note
``docs/implementation/pipeline/ogasp/runtime_verification.md``, seams 1 and 2).

These are *static* import-boundary guards: they fail loudly if a future edit blurs
a seam by reaching across a module boundary the layering forbids. The behavioural
seam checks live alongside them —
``test_movement_attacker.py::test_driver_delegates_verdict_and_composition`` (seam
3, driver consumes never forks) and
``test_movement_smoke.py::test_g6_no_behavioural_change_under_substrate_boundary``
(seam 4, attacker-only D5). Between them the four seams each have a check.
"""
from __future__ import annotations

import ast
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src" / "mtdsim" / "l3_simulation"


def _imported_modules(path: Path) -> set[str]:
    """Every module name imported by a source file (both ``import`` forms)."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add(node.module or "")
    return mods


def test_seam1_movement_net_imports_no_controller_and_no_simpy() -> None:
    """Seam 1 (Movement ⊥ Controller). The routing net is pure structure — the
    net's legal-move grammar. It must carry no verdict/compose logic, so it imports
    nothing from ``controller/`` and, being pure data, no SimPy either."""
    mods = _imported_modules(_SRC / "movement" / "net.py")
    assert not any("controller" in m for m in mods), (
        f"net.py reached into the controller sublayer: {sorted(mods)}"
    )
    assert not any(m == "simpy" or m.startswith("simpy.") for m in mods), (
        f"net.py imported SimPy — the routing net must stay pure data: {sorted(mods)}"
    )


def test_seam2_controller_is_simpy_free_and_does_not_import_movement() -> None:
    """Seam 2 (Controller ⊥ Action). The controller sublayer (map, compose, verdict
    adapter) is pure and SimPy-free: it never drives the substrate and never walks
    the net. So no module under ``controller/`` imports ``simpy`` or the movement
    layer. (``verdict.py`` may import the substrate's outcome *constants* —
    ``EXPLOIT_COMPROMISED`` / ``EXPLOIT_HALTED`` — which are plain module-level
    strings, not a SimPy or net dependency.)"""
    for name in ("controller.py", "outcome.py", "verdict.py"):
        mods = _imported_modules(_SRC / "controller" / name)
        assert not any(m == "simpy" or m.startswith("simpy.") for m in mods), (
            f"controller/{name} imported SimPy — the controller must stay pure: "
            f"{sorted(mods)}"
        )
        assert not any("movement" in m for m in mods), (
            f"controller/{name} imported the movement layer — the controller must "
            f"not know how the net is walked: {sorted(mods)}"
        )
