"""The verdict adapter — read a dispatched verb's substrate outcome into the
binary success/failure verdict the outcome overlay keys on (``controller.md`` §4).

A pure, SimPy-free reader: it takes a ``_do_*`` return value (the substrate's own
dice, never re-rolled — no double counting, M4) and whether an MTD interrupt
halted the verb, and returns ``"success"`` or ``"failure"``. The movement-layer
driver calls it once per dispatched verb; the overlay then routes the token on the
verdict (``mtdsim.l3_simulation.movement.attacker``).

Mapping (``controller.md`` §4; the outcome types are catalogued in
``attacker_phase_catalogue.md``):

- An **MTD interrupt** (``interrupted``) or an interrupt-halted exploit
  (``EXPLOIT_HALTED``) reads as **failure**, whatever the verb — the net falls
  back (register §M1, Jin's motivating feedback).
- ``EXPLOIT_VULN``: ``EXPLOIT_COMPROMISED`` → success; ``EXPLOIT_UNCOMPROMISED``
  → failure.
- ``SCAN_HOST`` / ``BRUTE_FORCE``: the bare ``bool`` — ``True`` (hosts found /
  host compromised) → success, ``False`` → failure.
- ``ENUM_HOST`` / ``SCAN_PORT`` / ``SCAN_NEIGHBOR``: **success unless
  interrupted** — a documented simplification (attacker handoff §1). Their §4
  "failure" conditions are not visible in the bare ``_do_*`` return
  (``_do_scan_neighbors`` returns ``None``; ``_do_scan_port``'s ``bool`` is
  reuse-only; ``ENUM_HOST`` is a dispatcher). No signal is lost: an empty
  ``SCAN_PORT`` surfaces one step later as an ``EXPLOIT_VULN``
  ``PRECONDITION_UNMET`` failure. A richer adapter reading ``host_stack`` /
  ``curr_ports`` deltas is a named extension, deferred.
"""
from __future__ import annotations

from typing import Any

from mtdnetwork.operation.attack_operation import (
    EXPLOIT_COMPROMISED,
    EXPLOIT_HALTED,
)

Verdict = str  # "success" | "failure" (binary outcome only, M2)

# Verbs whose bare _do_* return is a two-branch bool the verdict reads directly.
_BOOL_VERBS: frozenset[str] = frozenset({"SCAN_HOST", "BRUTE_FORCE"})
# Verbs whose bare _do_* return does not surface a §4 failure condition — treated
# as success unless interrupted (documented simplification; see module docstring).
_SUCCESS_UNLESS_INTERRUPTED: frozenset[str] = frozenset(
    {"ENUM_HOST", "SCAN_PORT", "SCAN_NEIGHBOR"}
)


def verdict_for(verb: str, outcome: Any, interrupted: bool = False) -> Verdict:
    """Read one dispatched verb's outcome into the binary verdict (``controller.md``
    §4). ``outcome`` is a ``_do_*`` return value (``bool`` / ``EXPLOIT_*`` /
    ``None``); ``interrupted`` is True for an MTD interrupt (reads as failure)."""
    if interrupted or outcome == EXPLOIT_HALTED:
        return "failure"
    if verb == "EXPLOIT_VULN":
        return "success" if outcome == EXPLOIT_COMPROMISED else "failure"
    if verb in _BOOL_VERBS:
        return "success" if outcome else "failure"
    if verb in _SUCCESS_UNLESS_INTERRUPTED:
        return "success"
    raise ValueError(
        f"unknown verb for verdict: {verb!r}; expected one of the six MTDSim verbs"
    )


__all__ = ["Verdict", "verdict_for"]
