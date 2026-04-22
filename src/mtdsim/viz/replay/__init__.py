"""MTDSim replay visualiser.

Dash app that loads an ``events.jsonl`` log and plays it back across three
SA-aligned panels (network / GAP iframe / intermediary execution) plus a
signal-flow sub-panel that makes the attacker's data flow legible.

Replay-only by design: simulations run headless and emit the log; the viewer
loads a log and plays back.
"""
