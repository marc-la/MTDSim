"""Entry point: ``python -m mtdsim.viz.replay [--log PATH]``."""

from __future__ import annotations

import argparse
from pathlib import Path

from mtdsim.viz.replay.app import build_app
from mtdsim.viz.replay.log import EventLog


def main() -> None:
    parser = argparse.ArgumentParser(prog="mtdsim.viz.replay")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8050)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        help="Path to events.jsonl to load at startup.",
    )
    args = parser.parse_args()

    log = EventLog.load(args.log) if args.log else None
    app = build_app(log=log)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
