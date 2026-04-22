"""Minimal simulation event log.

Shared contract between the simulator and the replay visualiser. Events
are plain dicts matching the schema in ``docs/event_log.md``; the logger
is a passive sink that can be wired into ``AttackOperation`` /
``MTDOperation`` / ``MTDAIOperation`` via an optional constructor kwarg.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional


class EventLogger:
    def __init__(self, env=None):
        self.env = env
        self.events: list[dict[str, Any]] = []

    def emit(
        self,
        event_type: str,
        host_id: Optional[int] = None,
        phase: Optional[str] = None,
        technique_id: Optional[str] = None,
        tactic: Optional[str] = None,
        t: Optional[float] = None,
        **meta,
    ) -> None:
        if t is None:
            t = float(self.env.now) if self.env is not None else 0.0
        self.events.append({
            "t": float(t),
            "type": event_type,
            "host_id": host_id,
            "phase": phase,
            "technique_id": technique_id,
            "tactic": tactic,
            "meta": meta,
        })

    def to_jsonl(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w") as f:
            for e in self.events:
                f.write(json.dumps(e) + "\n")

    def to_json(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
        with open(path, "w") as f:
            json.dump(self.events, f, indent=2)

    @classmethod
    def load_jsonl(cls, path: str) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events
