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
  interrupted** on their bare ``_do_*`` return — a documented simplification
  (attacker handoff §1). Their §4 "failure" conditions are not visible in that
  return (``_do_scan_neighbors`` returns ``None``; ``_do_scan_port``'s ``bool``
  is reuse-only; ``ENUM_HOST`` is a dispatcher).

- **The three state-delta rows (the "richer adapter", 2026-08-30 — the
  order-independent verb contract, handoff ``2026-08-30_fsm_token_hold_rule``
  §Design).** The movement layer's fresh-host contract reads each of those
  verbs' §4 failure condition off the substrate's own state after the core ran
  (no re-roll, M4) and surfaces it as a distinguished outcome value, which this
  adapter reads as **failure**:

  - ``ENUM_EXHAUSTED`` — ``ENUM_HOST`` selected no fresh host: every visible
    queued target was already owned and the retry-until-fresh loop ran the
    queue dry. The native "no host → SCAN_HOST" fact becomes a verdict the net
    routes on (Brown Fig 3 box 10 → box 1).
  - ``SCAN_PORT_EMPTY`` — ``SCAN_PORT`` found no open port on the host (and no
    credential reuse). The condition ``EXPLOIT_VULN``'s precondition guard
    would otherwise surface one step later, read where it happens.
  - ``NEIGHBORS_NONE_FRESH`` — ``SCAN_NEIGHBOR`` discovered no neighbour the
    attacker does not already own, so nothing new entered the frontier.

  The driver emits these only when its contract is on; with it off the bare
  outcomes reach here unchanged and the rows above are dormant, so every
  recorded verdict stream is reproducible.
"""
from __future__ import annotations

from typing import Any

from mtdnetwork.operation.attack_operation import (
    EXPLOIT_COMPROMISED,
    EXPLOIT_HALTED,
)

Verdict = str  # "success" | "failure" (binary outcome only, M2)

# The three state-delta outcomes the movement layer's fresh-host contract
# surfaces for the verbs whose bare ``_do_*`` return carries no failure branch
# (module docstring). Distinguishable from every bare outcome (``True`` /
# ``False`` / ``None`` / the ``EXPLOIT_*`` strings) and stringified verbatim into
# ``MovementRecord.outcome``, so the record says *why* the verdict failed.
ENUM_EXHAUSTED = "ENUM_EXHAUSTED"            # ENUM_HOST: no fresh host selectable
SCAN_PORT_EMPTY = "SCAN_PORT_EMPTY"          # SCAN_PORT: no open port, no reuse
NEIGHBORS_NONE_FRESH = "NEIGHBORS_NONE_FRESH"  # SCAN_NEIGHBOR: nothing fresh found
_STATE_DELTA_FAILURES: frozenset[str] = frozenset(
    {ENUM_EXHAUSTED, SCAN_PORT_EMPTY, NEIGHBORS_NONE_FRESH}
)

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
    if isinstance(outcome, str) and outcome in _STATE_DELTA_FAILURES:
        # The fresh-host contract's rows: a §4 failure condition read off the
        # substrate's state after the core ran (see module docstring).
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


__all__ = [
    "ENUM_EXHAUSTED",
    "NEIGHBORS_NONE_FRESH",
    "SCAN_PORT_EMPTY",
    "Verdict",
    "verdict_for",
]
