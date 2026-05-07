"""Entry point: ``python -m mtdsim.viz.replay``.

Default behaviour: load Joo Kai Tay's primary config (``100 nodes / 8 subnets /
4 layers / 2 databases``, ``FINISH_TIME=15000``, ``seed=42``) under the
``random`` MTD scheme. If the canonical log doesn't exist on disk, run the
sim once to produce it. The full config matrix lives in
:mod:`mtdsim.viz.replay.config`.

Flags mirror the original step-3 CLI (``--log``, ``--gap-html``, ``--host``,
``--port``, ``--debug``) and add ``--config {primary,demo}`` and
``--scheme``. Passing an explicit ``--log PATH`` bypasses the auto-run.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from mtdsim.viz.replay.app import build_app
from mtdsim.viz.replay.config import CONFIGS, DEFAULT_EVENTS_DIR, PRIMARY
from mtdsim.viz.replay.log import EventLog
from mtdsim.viz.replay.runner import run_canonical_sim


SUPPORTED_SCHEMES = ("no_mtd", "random", "alternative", "simultaneous")


def main() -> None:
    parser = argparse.ArgumentParser(prog="mtdsim.viz.replay")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8050)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        help="Path to events.jsonl. Overrides --config.",
    )
    parser.add_argument(
        "--config",
        choices=list(CONFIGS),
        default=PRIMARY.name,
        help="Named config to auto-run if no --log is given (default: primary = Tay 2024).",
    )
    parser.add_argument(
        "--scheme",
        choices=SUPPORTED_SCHEMES,
        default="random",
        help="MTD scheme for the auto-run (default: random).",
    )
    parser.add_argument(
        "--force-rerun",
        action="store_true",
        help="Re-run the sim even if the canonical log already exists.",
    )
    parser.add_argument(
        "--events-dir",
        type=Path,
        default=DEFAULT_EVENTS_DIR,
        help="Directory for auto-run logs (default: notebooks/gap_out/events).",
    )
    parser.add_argument(
        "--gap-html",
        type=Path,
        default=None,
        help="Optional: override the bundled GAP snapshot with a pre-rendered gap.html.",
    )
    parser.add_argument(
        "--gap-json",
        type=Path,
        default=None,
        help="Optional: override the bundled GAP snapshot JSON (for dev iteration).",
    )
    parser.add_argument(
        "--trivial",
        action="store_true",
        help=(
            "Boot with the canonical trivial profile pre-saved into "
            "store-operational-profile so the Run tab is one click away "
            "from a full GAP -> subgraph -> sim -> replay round-trip."
        ),
    )
    args = parser.parse_args()

    if args.log is not None:
        log_path = args.log
    else:
        config = CONFIGS[args.config]
        log_path = config.log_path(args.scheme, args.events_dir)
        if args.force_rerun or not log_path.exists():
            print(
                f"[replay] {'rerunning' if args.force_rerun else 'no log at'} "
                f"{log_path} — running {config.name} ({args.scheme}, seed={config.seed})…"
            )
            log_path = run_canonical_sim(
                config,
                scheme=args.scheme,
                events_dir=args.events_dir,
                force=args.force_rerun,
            )
            print(f"[replay] wrote {log_path}")

    log = EventLog.load(log_path)
    app = build_app(
        log=log,
        gap_html_path=args.gap_html,
        gap_json_path=args.gap_json,
        events_dir=args.events_dir,
        trivial=args.trivial,
    )
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
