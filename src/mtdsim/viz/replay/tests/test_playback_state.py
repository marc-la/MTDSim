"""Playback state-machine tests — tick math, scrubbing, speed changes."""

from __future__ import annotations

from mtdsim.viz.replay.log import (
    PlaybackState,
    initial_state,
    pause,
    seek_to_index,
    set_speed,
    start,
    tick,
)


EVENT_TS = [0.0, 10.0, 50.0, 120.0, 230.0, 400.0, 500.0]
T_MAX = 500.0


def _tick(state: PlaybackState, now_wall: float) -> PlaybackState:
    return tick(state, now_wall=now_wall, event_ts=EVENT_TS, t_max=T_MAX)


def test_initial_state_is_paused_at_zero():
    s = initial_state()
    assert not s.playing
    assert s.speed == 1.0
    assert s.sim_t == 0.0
    assert s.event_index == -1


def test_start_anchors_and_tick_advances_by_wall_elapsed():
    s = start(initial_state(), now_wall=1000.0)
    assert s.playing is True
    assert s.anchor_wall == 1000.0
    assert s.anchor_sim == 0.0

    s = _tick(s, now_wall=1015.0)
    assert s.playing is True
    assert s.sim_t == 15.0
    assert s.event_index == 1


def test_tick_is_drift_free_across_skipped_ticks():
    # Simulate a dropped tick: compute from anchor+elapsed, not by incrementing.
    s = start(initial_state(), now_wall=1000.0)
    s = _tick(s, now_wall=1120.0)
    assert s.sim_t == 120.0
    assert s.event_index == 3


def test_speed_2x_doubles_sim_advance():
    s = initial_state()
    s = set_speed(s, speed=2.0, now_wall=2000.0)
    s = start(s, now_wall=2000.0)
    s = _tick(s, now_wall=2060.0)
    assert s.sim_t == 120.0


def test_speed_quarter_x_slows_sim_advance():
    s = set_speed(initial_state(), speed=0.25, now_wall=0.0)
    s = start(s, now_wall=0.0)
    s = _tick(s, now_wall=200.0)
    assert s.sim_t == 50.0


def test_tick_clamps_and_stops_at_t_max():
    s = start(initial_state(), now_wall=0.0)
    s = _tick(s, now_wall=600.0)
    assert s.sim_t == T_MAX
    assert s.event_index == 6
    assert s.playing is False


def test_set_speed_mid_playback_does_not_jump_sim_time():
    s = start(initial_state(), now_wall=0.0)
    s = _tick(s, now_wall=30.0)
    assert s.sim_t == 30.0

    s = set_speed(s, speed=4.0, now_wall=30.0)
    assert s.sim_t == 30.0
    assert s.anchor_wall == 30.0
    assert s.anchor_sim == 30.0

    s = _tick(s, now_wall=40.0)
    assert s.sim_t == 70.0


def test_pause_freezes_sim_time():
    s = start(initial_state(), now_wall=0.0)
    s = _tick(s, now_wall=40.0)
    s = pause(s)
    assert s.sim_t == 40.0

    s = _tick(s, now_wall=200.0)
    assert s.sim_t == 40.0


def test_seek_pauses_and_jumps():
    s = start(initial_state(), now_wall=0.0)
    s = _tick(s, now_wall=5.0)
    s = seek_to_index(s, event_index=3, event_ts=EVENT_TS, now_wall=5.0)

    assert s.playing is False
    assert s.sim_t == 120.0
    assert s.event_index == 3

    s = _tick(s, now_wall=300.0)
    assert s.sim_t == 120.0


def test_seek_clamps_out_of_range_indices():
    s = initial_state()
    s = seek_to_index(s, event_index=99, event_ts=EVENT_TS, now_wall=0.0)
    assert s.event_index == len(EVENT_TS) - 1
    s = seek_to_index(s, event_index=-5, event_ts=EVENT_TS, now_wall=0.0)
    assert s.event_index == 0
