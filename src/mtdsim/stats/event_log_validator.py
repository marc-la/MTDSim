"""Post-hoc invariants over a replay event log.

Used by the regression test (and ad-hoc by the replay viewer) to confirm
that a sim produced a well-formed trace. Catches the class of bug that
was hiding in the simulator before P1: every ``mtd_deployed`` should pair
with a ``mtd_completed`` or ``mtd_aborted``, and no phase should start
after ``sim_ended``.

Returns a list of issue strings rather than raising, so callers can
choose between "fail loud" (assert not issues) and "report and continue".
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


def _load(events_or_path: Iterable[dict[str, Any]] | str | Path) -> list[dict[str, Any]]:
    if isinstance(events_or_path, (str, Path)):
        events: list[dict[str, Any]] = []
        with open(events_or_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events
    return list(events_or_path)


def validate_event_log(events_or_path) -> list[str]:
    """Return a list of human-readable issue strings; empty list = clean."""
    events = _load(events_or_path)
    issues: list[str] = []

    if not events:
        return ["empty event log"]

    if events[0].get("type") != "sim_started":
        issues.append(f"first event is {events[0].get('type')!r}, expected sim_started")
    if events[-1].get("type") != "sim_ended":
        issues.append(f"last event is {events[-1].get('type')!r}, expected sim_ended")

    type_counts = Counter(e.get("type") for e in events)

    deployed = type_counts.get("mtd_deployed", 0)
    completed = type_counts.get("mtd_completed", 0)
    aborted = type_counts.get("mtd_aborted", 0)
    if deployed != completed + aborted:
        issues.append(
            f"mtd_deployed={deployed} but mtd_completed+mtd_aborted={completed + aborted} "
            f"(orphan deploys: {deployed - completed - aborted})"
        )

    phase_started = type_counts.get("phase_started", 0)
    phase_completed = type_counts.get("phase_completed", 0)
    if phase_started > phase_completed:
        issues.append(
            f"phase_started={phase_started} > phase_completed={phase_completed} "
            f"(in-flight phases at sim end: {phase_started - phase_completed})"
        )

    sim_ended_t = next(
        (e["t"] for e in events if e.get("type") == "sim_ended"), None
    )
    if sim_ended_t is not None:
        late = [
            e for e in events
            if e.get("type") in {"phase_started", "mtd_deployed"} and e.get("t", 0) > sim_ended_t
        ]
        if late:
            issues.append(f"{len(late)} phase/mtd events after sim_ended at t={sim_ended_t}")

    return issues


__all__ = ["validate_event_log"]
