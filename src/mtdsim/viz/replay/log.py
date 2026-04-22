"""Event log loader + playback state math.

Pure, no Dash imports. The Dash app wires this into ``dcc.Store`` /
``dcc.Interval`` callbacks; keeping the math here makes it unit-testable
without spinning up a server.

Schema enforcement is strict: any event missing or disagreeing with
``SUPPORTED_SCHEMA_VERSION`` is a load-time error. Per §13 of the
implementation plan the loader is not forward-compatible by design.
"""

from __future__ import annotations

import bisect
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional


SUPPORTED_SCHEMA_VERSION = "1.0"
DEFAULT_SNAPSHOT_INTERVAL = 100.0


class UnsupportedSchemaVersion(ValueError):
    """Raised when an event has a schema_version the loader doesn't support."""


@dataclass(frozen=True)
class NetworkSnapshot:
    """Cumulative host-state snapshot at a sim-time checkpoint.

    ``host_states`` maps host_id to one of {"targeted", "compromised"}.
    MTD halos and per-host metadata are layered on top at render time;
    this struct is intentionally minimal so snapshot precompute is fast.
    """

    t: float
    event_index: int
    host_states: dict[int, str]


@dataclass
class EventLog:
    path: Path
    events: list[dict[str, Any]]
    event_ts: list[float]
    t_min: float
    t_max: float
    snapshots: list[NetworkSnapshot]
    hosts_seen: set[int] = field(default_factory=set)
    techniques_seen: set[str] = field(default_factory=set)
    topology: Optional[dict[str, Any]] = None
    sim_meta: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(
        cls,
        path: str | Path,
        *,
        snapshot_every: float = DEFAULT_SNAPSHOT_INTERVAL,
    ) -> "EventLog":
        path = Path(path)
        events: list[dict[str, Any]] = []
        with path.open() as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                ev = json.loads(line)
                version = ev.get("schema_version")
                if version != SUPPORTED_SCHEMA_VERSION:
                    raise UnsupportedSchemaVersion(
                        f"{path}:{lineno}: schema_version={version!r}, "
                        f"expected {SUPPORTED_SCHEMA_VERSION!r}"
                    )
                events.append(ev)

        if not events:
            return cls(
                path=path,
                events=[],
                event_ts=[],
                t_min=0.0,
                t_max=0.0,
                snapshots=[],
            )

        event_ts = [float(ev["t"]) for ev in events]
        t_min = event_ts[0]
        t_max = event_ts[-1]

        hosts_seen = {ev["host_id"] for ev in events if ev["host_id"] is not None and ev["host_id"] >= 0}
        techniques_seen = {ev["technique_id"] for ev in events if ev["technique_id"]}
        snapshots = _precompute_snapshots(events, event_ts, snapshot_every)

        sim_meta: dict[str, Any] = {}
        topology: Optional[dict[str, Any]] = None
        for ev in events:
            if ev["type"] == "sim_started":
                sim_meta = dict(ev.get("meta") or {})
                topology = sim_meta.get("topology")
                break

        return cls(
            path=path,
            events=events,
            event_ts=event_ts,
            t_min=t_min,
            t_max=t_max,
            snapshots=snapshots,
            hosts_seen=hosts_seen,
            techniques_seen=techniques_seen,
            topology=topology,
            sim_meta=sim_meta,
        )

    def index_at_time(self, sim_t: float) -> int:
        """Index of the last event with ``t <= sim_t`` (or -1 before the first)."""
        if not self.event_ts:
            return -1
        return bisect.bisect_right(self.event_ts, sim_t) - 1

    def time_at_index(self, event_index: int) -> float:
        if not self.event_ts:
            return 0.0
        event_index = max(0, min(event_index, len(self.event_ts) - 1))
        return self.event_ts[event_index]


def _precompute_snapshots(
    events: list[dict[str, Any]],
    event_ts: list[float],
    step: float,
) -> list[NetworkSnapshot]:
    """Walk the event stream once, emitting a snapshot every ``step`` seconds."""
    snapshots: list[NetworkSnapshot] = []
    if not events:
        return snapshots

    compromised: set[int] = set()
    targeted: set[int] = set()
    next_i = 0
    t = 0.0
    t_end = event_ts[-1]

    while True:
        while next_i < len(events) and event_ts[next_i] <= t:
            ev = events[next_i]
            host_id = ev["host_id"]
            etype = ev["type"]
            if host_id is not None and host_id >= 0:
                if etype == "host_compromised":
                    compromised.add(host_id)
                elif etype == "phase_started":
                    targeted.add(host_id)
            next_i += 1

        host_states: dict[int, str] = {}
        for h in targeted | compromised:
            host_states[h] = "compromised" if h in compromised else "targeted"

        snapshots.append(
            NetworkSnapshot(
                t=t,
                event_index=max(next_i - 1, 0),
                host_states=host_states,
            )
        )

        if t >= t_end:
            break
        t += step

    return snapshots


# --------------------------------------------------------------------------- #
# Playback state math
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class PlaybackState:
    """Serialisable playback state; mirrors the contents of ``dcc.Store``.

    Playing is driven by *elapsed wall time × speed*, not by incrementing the
    event index on each tick. This is §10 of the plan's mitigation for timer
    drift: an interval that occasionally skips a tick doesn't fall behind.

    - ``playing``: whether the clock is running.
    - ``speed``: playback speed multiplier (sim-seconds per wall-second).
    - ``anchor_wall``: wall-clock timestamp (seconds) captured at the moment
       the user last hit play or scrubbed.
    - ``anchor_sim``: sim time captured at the same moment.
    - ``sim_t``: derived sim time at the last tick (for display).
    - ``event_index``: derived event index at the last tick.
    """

    playing: bool
    speed: float
    anchor_wall: float
    anchor_sim: float
    sim_t: float
    event_index: int


def tick(
    state: PlaybackState,
    *,
    now_wall: float,
    event_ts: list[float],
    t_max: float,
) -> PlaybackState:
    """Advance playback state to ``now_wall``; returns a new state."""
    if not event_ts:
        return state

    if state.playing:
        sim_t = state.anchor_sim + state.speed * (now_wall - state.anchor_wall)
        if sim_t >= t_max:
            sim_t = t_max
            playing = False
        else:
            playing = True
    else:
        sim_t = state.sim_t
        playing = False

    sim_t = max(0.0, min(sim_t, t_max))
    event_index = bisect.bisect_right(event_ts, sim_t) - 1

    return PlaybackState(
        playing=playing,
        speed=state.speed,
        anchor_wall=state.anchor_wall,
        anchor_sim=state.anchor_sim,
        sim_t=sim_t,
        event_index=event_index,
    )


def seek_to_index(
    state: PlaybackState,
    *,
    event_index: int,
    event_ts: list[float],
    now_wall: float,
) -> PlaybackState:
    """Jump to a specific event index (e.g. from scrubber drag or step button).

    Scrubbing pauses playback — the user is driving the clock, not the timer.
    """
    if not event_ts:
        return state
    event_index = max(0, min(event_index, len(event_ts) - 1))
    sim_t = event_ts[event_index]
    return PlaybackState(
        playing=False,
        speed=state.speed,
        anchor_wall=now_wall,
        anchor_sim=sim_t,
        sim_t=sim_t,
        event_index=event_index,
    )


def start(
    state: PlaybackState,
    *,
    now_wall: float,
) -> PlaybackState:
    """Begin playing from the current sim_t."""
    return PlaybackState(
        playing=True,
        speed=state.speed,
        anchor_wall=now_wall,
        anchor_sim=state.sim_t,
        sim_t=state.sim_t,
        event_index=state.event_index,
    )


def pause(state: PlaybackState) -> PlaybackState:
    return PlaybackState(
        playing=False,
        speed=state.speed,
        anchor_wall=state.anchor_wall,
        anchor_sim=state.sim_t,
        sim_t=state.sim_t,
        event_index=state.event_index,
    )


def set_speed(
    state: PlaybackState,
    *,
    speed: float,
    now_wall: float,
) -> PlaybackState:
    """Change speed without jumping sim time. Re-anchor at the current instant."""
    return PlaybackState(
        playing=state.playing,
        speed=float(speed),
        anchor_wall=now_wall,
        anchor_sim=state.sim_t,
        sim_t=state.sim_t,
        event_index=state.event_index,
    )


def initial_state() -> PlaybackState:
    return PlaybackState(
        playing=False,
        speed=1.0,
        anchor_wall=0.0,
        anchor_sim=0.0,
        sim_t=0.0,
        event_index=-1,
    )
