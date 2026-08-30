"""Golden behaviour streams for the MTD defender pool — capture and check.

    PYTHONPATH=src python tools/mtd_golden_streams.py capture
    PYTHONPATH=src python tools/mtd_golden_streams.py check
    PYTHONPATH=src python tools/mtd_golden_streams.py check --only IPShuffle UserShuffle

The behaviour-preservation gate for the MTD mechanism cost audit
(`docs/handoffs/2026-07-29_mtd_mechanism_cost_audit.md`): any performance change
to the defender side is verified by **field-for-field equality** of these streams,
not by "the numbers look similar". A speed-up that moves a stream is a failed
optimisation.

Per configuration (mechanism x seed x overlay arm) the golden holds three streams:

- the movement-layer ``MovementRecord`` stream (every walk event, all fields),
- the substrate's per-mutation MTD operation record (name / start / finish),
- the substrate's ``AttackStatistics`` rows (every verb the walk dispatched).

Because every mechanism draws from the same seeded global RNGs the attacker uses,
any change to defender draw *count or order* shifts the attacker's stream too —
the three streams jointly fingerprint both sides of the contest.

The wiring below mirrors :func:`mtdsim.l3_simulation.movement.run.run_movement`
statement for statement (the same pattern ``l3_simulation.trace`` uses and pins
with a parity test) so a golden run and a ``run_movement`` run of the same
configuration are RNG-identical. Configuration matches ``tools/mtd_cost_bench.py``
(aggregate profile, v2_partial mapping, 15 000 s horizon, single scheme,
200 s interval) so the goldens guard exactly the runs the cost table times.

Goldens live in ``baseline/golden_movement/`` (gzipped JSON, one file per
configuration, plus ``manifest.json`` with SHA-256 digests). Intentional
re-baselines follow the same rule as ``baseline/golden``: a changelog entry in
``baseline/CHANGELOG.md`` or the diff is a regression to chase.

**The schema follows the input.** A golden document's shape is a function of the
run's declared inputs, never of what fields happen to exist in the code: a run
that does not name the retrace input serialises ``MovementRecord`` in the
pre-retrace shape (no ``retrace`` field), so the legacy goldens stay
byte-identical across capability additions and a digest change always means
behaviour moved. Capabilities that *are* named get their own golden set — the
``*_retrace`` configurations run ``retrace_sinks=True`` on ``objective_exfiltration_impact``
(a sink-bearing net; the cost-bench ``aggregate`` profile has no sinks, so the
policy would be inert there), and their documents carry the ``retrace`` field
plus a ``retraces`` summary count.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

GOLDEN_DIR = REPO / "baseline" / "golden_movement"

from mtdnetwork.mtd.completetopologyshuffle import CompleteTopologyShuffle  # noqa: E402
from mtdnetwork.mtd.hosttopologyshuffle import HostTopologyShuffle  # noqa: E402
from mtdnetwork.mtd.ipshuffle import IPShuffle  # noqa: E402
from mtdnetwork.mtd.osdiversity import OSDiversity  # noqa: E402
from mtdnetwork.mtd.osdiversityassignment import OSDiversityAssignment  # noqa: E402
from mtdnetwork.mtd.portshuffle import PortShuffle  # noqa: E402
from mtdnetwork.mtd.servicediversity import ServiceDiversity  # noqa: E402
from mtdnetwork.mtd.usershuffle import UserShuffle  # noqa: E402

MECHANISMS = {
    "CompleteTopologyShuffle": CompleteTopologyShuffle,
    "HostTopologyShuffle": HostTopologyShuffle,
    "IPShuffle": IPShuffle,
    "PortShuffle": PortShuffle,
    "OSDiversity": OSDiversity,
    "ServiceDiversity": ServiceDiversity,
    "UserShuffle": UserShuffle,
    "OSDiversityAssignment": OSDiversityAssignment,
}

# The cost-bench configuration, held constant here by name.
PROFILE = "aggregate"
MAPPING = "v2_partial"
HORIZON = 15_000
INTERVAL = 200
SEEDS = (0, 1, 2)
ARMS = (True, False)  # with_synthetic_overlay

# The retrace golden set: the S5 policy exercised where it can fire. One
# mechanism per resource class plus the stateful mechanism and the no-MTD
# control, on the net that retraces hardest, overlay arm only.
RETRACE_PROFILE = "objective_exfiltration_impact"
RETRACE_MECHANISMS = (
    "no-mtd", "IPShuffle", "ServiceDiversity", "UserShuffle",
    "OSDiversityAssignment",
)


def _jsonable(value):
    """Coerce numpy scalars to their exact Python equivalents for JSON."""
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return value


def one_golden_run(
    mechanism_cls,
    *,
    seed: int,
    with_synthetic_overlay: bool,
    profile: str = PROFILE,
    retrace_sinks: bool = False,
) -> dict:
    """Run one movement simulation and return its three streams as JSON-ready
    dicts. Mirrors ``run_movement``'s wiring so the RNG stream is identical.

    The document's schema follows the declared inputs (module docstring): with
    ``retrace_sinks`` unnamed the movement records are serialised in the
    pre-retrace shape and the config/summary sections are exactly the legacy
    ones; naming it extends all three."""
    from mtdsim.l3_simulation.controller import (
        load_controller,
        load_outcome_overlay,
        verdict_for,
    )
    from mtdsim.l3_simulation.movement.attacker import (
        MovementAttacker,
        load_dwell_catalogue,
    )
    from mtdsim.l3_simulation.movement.net import load_routing_net
    from mtdsim.l3_simulation.movement.run import _build_sim, _maybe_start_mtd

    env, end_event, network, adversary, attack_op = _build_sim(seed, None)

    routing_net = load_routing_net(
        profile, with_synthetic_overlay=with_synthetic_overlay
    )
    controller = load_controller(version=MAPPING)
    overlay = load_outcome_overlay()
    dwell = load_dwell_catalogue()

    attacker = MovementAttacker(
        env=env,
        end_event=end_event,
        adversary=adversary,
        attack_operation=attack_op,
        routing_net=routing_net,
        controller=controller,
        overlay=overlay,
        verdict_of=verdict_for,
        dwell_catalogue=dwell,
        timing=None,
        seed=seed,
        register_for_interrupts=True,
        max_events=50_000,
        retrace_sinks=retrace_sinks,
        fresh_host_contract=True,
    )
    attacker.start()

    _maybe_start_mtd(
        env=env,
        end_event=end_event,
        network=network,
        adversary=adversary,
        attack_op=attack_op,
        scheme=("single" if mechanism_cls else None),
        mtd_interval=(INTERVAL if mechanism_cls else None),
        custom_strategies=mechanism_cls,
    )

    env.run(until=HORIZON)

    movement_records = [
        {k: _jsonable(v) for k, v in asdict(r).items()} for r in attacker.records
    ]
    if not retrace_sinks:
        # Schema follows the input: a run that did not name the retrace input
        # serialises in the pre-retrace record shape, so the legacy goldens
        # survive the field's existence and only behaviour can move a digest.
        for rec in movement_records:
            rec.pop("retrace", None)
    # ``n_compromised`` is an OBSERVATION, not behaviour: it samples the
    # substrate's compromised-host list per record and influences no decision the
    # attacker takes. It is popped for the same reason ``retrace`` is popped above
    # and on the file's own stated principle — **only behaviour may move a
    # digest** — so the goldens keep catching what they exist to catch. Nothing is
    # lost: ``summary.compromised_count`` already pins the trajectory's endpoint,
    # which is the only part of it a golden could meaningfully guard.
    for rec in movement_records:
        rec.pop("n_compromised", None)
    # ``interrupted_by_name`` is the same kind of field for the same reason (A6,
    # 2026-08-05): it names the mechanism behind an interrupt whose resource
    # class ``interrupted_by`` already records, and nothing in the walk reads it
    # to decide anything. Popping it keeps this file's stated principle intact —
    # the schema follows the *input*, so only behaviour can move a digest — and
    # it is what makes the A6 widening a genuine no-golden-move rather than a
    # re-baseline dressed as one. ``interrupted_by`` itself stays: it was in the
    # shape the goldens were captured with, and the digest should keep guarding
    # everything it already guarded.
    for rec in movement_records:
        rec.pop("interrupted_by_name", None)
    # ``exploitability`` is the third field of the same kind and is popped for the
    # third time on the same principle (axis-5 exposure reader, 2026-08-06): it
    # samples the synthetic CVSS figure of the vulnerabilities an exploit action
    # engaged, and nothing in the walk reads it to decide anything. It is
    # *observation*, so it must not be able to move a digest — the goldens exist
    # to catch behaviour changing, and a widening that moved them would spend
    # their credibility on a field that changes nothing.
    for rec in movement_records:
        rec.pop("exploitability", None)
    # ``on_owned_host`` is the fourth observation-only field (the fresh-host
    # contract, 2026-08-30): whether curr_host was already owned when the verb
    # fired, read before ``step`` and read by nothing the walk decides. Popped on
    # the same principle. ``reselected`` / ``enum_repops`` are NOT popped — they
    # are behaviour (the contract acted), and the contract is a declared input
    # of every golden captured on or after 2026-08-30 (config["fresh_host_contract"]).
    # The three hold fields are popped: no golden attaches a hold rule, so the
    # schema follows that input exactly as it follows ``retrace``.
    for rec in movement_records:
        rec.pop("on_owned_host", None)
        rec.pop("holds", None)
        rec.pop("hold_dwell", None)
        rec.pop("hold_fell_through", None)
    mtd_records = [
        {k: _jsonable(v) for k, v in row.items()}
        for row in network.get_mtd_stats()._mtd_operation_record
    ]
    attack_records = [
        {k: _jsonable(v) for k, v in row.items()}
        for row in adversary.get_attack_stats()._attack_operation_record
    ]
    config = {
        "mechanism": mechanism_cls.__name__ if mechanism_cls else "no-mtd",
        "seed": seed,
        "with_synthetic_overlay": with_synthetic_overlay,
        "profile": profile,
        "mapping": MAPPING,
        "horizon": HORIZON,
        "interval": INTERVAL,
        # The order-independent verb contract, on since 2026-08-30 (Marc's ruling,
        # register T1 annotation). Named in the config so a golden states which
        # attacker it pins; the 2026-08-30 re-baseline is the only time the
        # movement goldens have moved for an attacker-side reason.
        "fresh_host_contract": True,
    }
    summary = {
        "events": len(movement_records),
        "interrupts": sum(1 for r in movement_records if r["interrupted"]),
        "mtd_executions": len(mtd_records),
        "attack_rows": len(attack_records),
        "reached_objective": bool(end_event.triggered),
        "compromised_count": len(adversary.get_compromised_hosts()),
    }
    if retrace_sinks:
        config["retrace_sinks"] = True
        summary["retraces"] = attacker.retrace_count
    return {
        "config": config,
        "summary": summary,
        "movement_records": movement_records,
        "mtd_records": mtd_records,
        "attack_records": attack_records,
    }


def _canonical(doc: dict) -> str:
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def _digest(doc: dict) -> str:
    return hashlib.sha256(_canonical(doc).encode()).hexdigest()


def _config_name(mech_name: str, seed: int, arm: bool, retrace: bool = False) -> str:
    base = f"{mech_name}_seed{seed}_{'overlay' if arm else 'observed'}"
    return f"{base}_retrace" if retrace else base


def _configs(only):
    """Yield (name, cls, seed, arm, retrace) for the legacy set, then the
    retrace set. ``--only`` filters by mechanism name across both."""
    names = ["no-mtd"] + list(MECHANISMS)
    if only:
        names = [n for n in names if n in only]
    for name in names:
        cls = MECHANISMS.get(name)
        for seed in SEEDS:
            for arm in ARMS:
                yield name, cls, seed, arm, False
    for name in RETRACE_MECHANISMS:
        if only and name not in only:
            continue
        cls = MECHANISMS.get(name)
        for seed in SEEDS:
            yield name, cls, seed, True, True


def capture(only=None) -> int:
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = GOLDEN_DIR / "manifest.json"
    manifest = (
        json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    )
    for name, cls, seed, arm, retrace in _configs(only):
        cfg = _config_name(name, seed, arm, retrace)
        start = time.perf_counter()
        doc = one_golden_run(
            cls, seed=seed, with_synthetic_overlay=arm,
            profile=(RETRACE_PROFILE if retrace else PROFILE),
            retrace_sinks=retrace,
        )
        elapsed = time.perf_counter() - start
        payload = _canonical(doc).encode()
        # mtime=0 keeps the archive byte-stable across re-captures of identical
        # behaviour, so `git status` stays quiet unless a stream truly moved.
        (GOLDEN_DIR / f"{cfg}.json.gz").write_bytes(
            gzip.compress(payload, mtime=0)
        )
        manifest[cfg] = {
            "sha256": _digest(doc),
            "events": doc["summary"]["events"],
            "interrupts": doc["summary"]["interrupts"],
            "mtd_executions": doc["summary"]["mtd_executions"],
            "compromised": doc["summary"]["compromised_count"],
        }
        if "retraces" in doc["summary"]:
            manifest[cfg]["retraces"] = doc["summary"]["retraces"]
        print(f"captured {cfg:55s} {elapsed:8.1f}s  "
              f"{doc['summary']['events']:5d} events  "
              f"{doc['summary']['interrupts']:3d} interrupts")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return 0


def _first_diff(golden: dict, fresh: dict) -> str:
    """Human-oriented locator for the first differing field between two docs."""
    for stream in ("movement_records", "mtd_records", "attack_records"):
        g_rows, f_rows = golden[stream], fresh[stream]
        for i, (g, f) in enumerate(zip(g_rows, f_rows)):
            if g != f:
                keys = [k for k in g if g.get(k) != f.get(k)]
                key = keys[0] if keys else "?"
                return (f"{stream}[{i}].{key}: golden={g.get(key)!r} "
                        f"fresh={f.get(key)!r}")
        if len(g_rows) != len(f_rows):
            return (f"{stream} length: golden={len(g_rows)} fresh={len(f_rows)}")
    return "summary-level difference only"


def check(only=None) -> int:
    failures = 0
    for name, cls, seed, arm, retrace in _configs(only):
        cfg = _config_name(name, seed, arm, retrace)
        path = GOLDEN_DIR / f"{cfg}.json.gz"
        if not path.exists():
            print(f"MISSING  {cfg}")
            failures += 1
            continue
        with gzip.open(path, "rb") as fh:
            golden = json.loads(fh.read())
        fresh = one_golden_run(
            cls, seed=seed, with_synthetic_overlay=arm,
            profile=(RETRACE_PROFILE if retrace else PROFILE),
            retrace_sinks=retrace,
        )
        # JSON-roundtrip the fresh doc so both sides carry identical types.
        fresh = json.loads(_canonical(fresh))
        if _digest(golden) == _digest(fresh):
            print(f"OK       {cfg}")
        else:
            print(f"DIFFERS  {cfg}: {_first_diff(golden, fresh)}")
            failures += 1
    if failures:
        print(f"\n{failures} configuration(s) diverged from golden")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["capture", "check"])
    ap.add_argument("--only", nargs="*", default=None,
                    help="subset of mechanism names (or 'no-mtd')")
    args = ap.parse_args()
    return capture(args.only) if args.mode == "capture" else check(args.only)


if __name__ == "__main__":
    raise SystemExit(main())
