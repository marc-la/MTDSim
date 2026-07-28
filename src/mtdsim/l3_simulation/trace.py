"""The unified L3 trace — one event log across all three layers of a movement run.

The substrate tracer (:mod:`mtdnetwork.trace`) narrates the inherited contest:
attacker verbs, MTD deployments, mutations, interrupts. A movement-layer run adds
two layers above it that the substrate log cannot see — the **token** walking the
class net, and the **controller** deciding what each place dispatches, how each
substrate outcome reads as a verdict, and where the token routes next. This module
narrates all three on the one shared clock, so a single log answers questions no
single layer's records can:

- Where is the token *spending its time* — dwelling (behavioural tempo, S3),
  running verbs (substrate cost), or paying interrupt penalties?
- What did the selected mapping actually do — which tactics dispatched which
  verbs, which were dwell-only, and how often did a dispatch hit an unmet
  substrate precondition (the coupling surface, recorded not silenced)?
- How did each verdict move the token — which out-edges the overlay suppressed,
  whether a failure bounced the token backwards, whether the walk stalled?
- Did the defence interact with the walk — mutations landing mid-dwell vs
  mid-verb, and what each one cost?

Usage (module CLIs on this branch run with ``PYTHONPATH=src``)
--------------------------------------------------------------
    PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate
    PYTHONPATH=src python -m mtdsim.l3_simulation.trace pure_steal --mapping v2_partial
    PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --scheme simultaneous
    PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --only token,controller
    PYTHONPATH=src python -m mtdsim.l3_simulation.trace aggregate --quiet   # verdict only

Reading the log (on top of the substrate actors)
------------------------------------------------
    TOKEN       the net-walker: entered a place, drew its dwell, the per-step
                summary (place -> verb -> verdict -> next), terminal events
    CONTROLLER  the decision layer: tactic -> verb dispatch, the verdict read
                from a substrate outcome, the conditioned routing distribution
    ATTACKER    the dispatched verb running through the carved ``step()``
    COMPROMISE / DEFENDER / MUTATION / INTERRUPT / NETWORK  as in the substrate
                tracer — the same hooks fire, so cross-layer events interleave

How it instruments (and why it cannot perturb)
----------------------------------------------
The driver takes its controller collaborators by injection, so ``phase_for``,
``compose``, ``verdict_of`` and ``timing.draw`` are **wrapped in recording
proxies, not monkeypatched** — each delegates unchanged and only records. Two
substrate seams are class-patched (with undo), because the driven arm bypasses
the ``_execute_*`` seams the substrate tracer hooks: ``AttackOperation.step``
(verb narration) and ``AttackOperation.apply_mtd_interrupt_cost`` (the driven
arm's confusion penalty — it never calls ``_handle_interrupt``). The per-step
TOKEN summary is derived from the driver's own ``MovementRecord`` stream as it
is appended. No wrapper draws randomness or writes simulator state, so a traced
run is identical to the same-seed :func:`run_movement` run — pinned
record-for-record by ``tests/l3_simulation/test_movement_trace.py``.

Like the substrate tracer, this is a **living diagnostic tool** — extend it when
a new seam needs narrating, keeping the two invariants and the parity test green.
See ``docs/implementation/trace_tool.md``.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field

import simpy

from mtdnetwork.operation.attack_operation import (
    EXPLOIT_HALTED,
    STEP_ABORTED,
    AttackOperation,
)
from mtdnetwork.trace import Event, Tracer, _install, _paint

from mtdsim.l3_simulation.controller import (
    load_controller,
    load_outcome_overlay,
    verdict_for,
)
from mtdsim.l3_simulation.movement.attacker import (
    DWELL_ONLY,
    MovementAttacker,
    MovementRecord,
    load_dwell_catalogue,
)
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net
from mtdsim.l3_simulation.movement.run import GEOMETRY, _build_sim, _maybe_start_mtd
from mtdsim.l3_simulation.movement.statistics import MovementRunResult
from mtdsim.l3_simulation.movement.timing import ConstantTiming, TacticTiming

L3_ACTORS = ("TOKEN", "CONTROLLER")


@dataclass
class L3Tracer(Tracer):
    """The substrate tracer plus the movement layer's running tallies."""

    # run identity, for the verdict header
    profile: str = ""
    mapping_version: str = ""
    overlay_version: str = ""
    timing_regime: str = ""
    scheme: str = "none"

    # movement tallies
    steps: int = 0
    dwell_only_steps: int = 0
    blocked_dispatches: int = 0
    verdict_successes: int = 0
    verdict_failures: int = 0
    interrupted_steps: int = 0
    verb_interrupts: int = 0  # interrupts that cut a running verb (rest cut a dwell)
    dwell_time: float = 0.0
    action_time: float = 0.0  # substrate verb cost (end - start - dwell, sans penalty)
    stalled: bool = False
    terminal_tag: str = ""  # SIM_END / MAX_EVENTS / "" (stall, sink or horizon)
    visits_by_place: dict[str, int] = field(default_factory=dict)
    time_by_place: dict[str, float] = field(default_factory=dict)
    dispatches_by_verb: dict[str, int] = field(default_factory=dict)


# --- the recording proxies (collaborators consumed, narrated, never altered) --

class _TracedController:
    def __init__(self, inner, tracer: L3Tracer):
        self._inner = inner
        self._tracer = tracer

    def phase_for(self, tactic: str):
        verb = self._inner.phase_for(tactic)
        t = self._tracer
        t.visits_by_place[tactic] = t.visits_by_place.get(tactic, 0) + 1
        t.emit("TOKEN", f"ENTER          {tactic}",
               f"visit {t.visits_by_place[tactic]}")
        if verb is None:
            t.emit("CONTROLLER", f"DISPATCH       {tactic} is dwell-only",
                   "consumes time, fires nothing, raises no verdict")
        else:
            t.dispatches_by_verb[verb] = t.dispatches_by_verb.get(verb, 0) + 1
            t.emit("CONTROLLER", f"DISPATCH       {tactic} -> {verb}",
                   f"mapping {t.mapping_version or 'ad hoc'}")
        return verb

    def __getattr__(self, name):
        return getattr(self._inner, name)


class _TracedOverlay:
    def __init__(self, inner, tracer: L3Tracer):
        self._inner = inner
        self._tracer = tracer

    def compose(self, src, verdict, base_out_weights):
        composed = self._inner.compose(src, verdict, base_out_weights)
        t = self._tracer
        if not composed:
            t.stalled = True
            t.emit("CONTROLLER",
                   f"STALL          {src} | {verdict}: every out-edge suppressed",
                   f"{len(base_out_weights)} base edge(s), all conditioned to 0 — "
                   "the walk terminates here")
            return composed
        suppressed = sum(1 for d in base_out_weights if composed.get(d, 0.0) <= 0)
        total = sum(composed.values())
        top = sorted(composed.items(), key=lambda kv: -kv[1])[:3]
        dist = " · ".join(f"{dst} {w / total:.2f}" for dst, w in top)
        more = f" (+{len(composed) - len(top)} more)" if len(composed) > len(top) else ""
        t.emit("CONTROLLER",
               f"ROUTE          {src} | {verdict}: {len(composed)} candidate(s), "
               f"{suppressed} suppressed",
               f"p(next): {dist}{more}")
        return composed

    def __getattr__(self, name):
        return getattr(self._inner, name)


class _TracedVerdict:
    def __init__(self, inner, tracer: L3Tracer):
        self._inner = inner
        self._tracer = tracer

    def __call__(self, verb, outcome, interrupted):
        verdict = self._inner(verb, outcome, interrupted)
        why = "MTD interrupt reads as failure" if interrupted else f"outcome {outcome!r}"
        self._tracer.emit("CONTROLLER", f"VERDICT        {verb}: {verdict}", why)
        return verdict


class _TracedTiming:
    def __init__(self, inner, tracer: L3Tracer):
        self._inner = inner
        self._tracer = tracer

    def draw(self, tactic: str) -> float:
        dwell = self._inner.draw(tactic)
        mean = getattr(self._inner, "mean_for", lambda _t: 0.0)(tactic)
        if dwell <= 0.0:
            detail = "immediate transition — no time, no draw consumed"
        elif dwell == mean:
            detail = "constant regime — the catalogue value as a fixed dwell"
        else:
            detail = f"exponential draw about the catalogue mean {mean:.0f}"
        self._tracer.emit("TOKEN", f"DWELL          {tactic}: {dwell:.1f} t/u", detail)
        return dwell

    def __getattr__(self, name):
        return getattr(self._inner, name)


class _NarratingRecords(list):
    """The driver's ``records`` list, emitting one TOKEN summary per appended
    :class:`MovementRecord` and keeping the tracer's tallies. Reading the
    driver's own record stream is the one instrumentation point that cannot
    disagree with what the run records."""

    def __init__(self, tracer: L3Tracer):
        super().__init__()
        self._tracer = tracer

    def append(self, rec: MovementRecord) -> None:
        super().append(rec)
        t = self._tracer
        t.steps += 1
        t.dwell_time += rec.dwell
        t.time_by_place[rec.place] = t.time_by_place.get(rec.place, 0.0) + (
            rec.end_time - rec.start_time
        )
        if rec.interrupted:
            t.interrupted_steps += 1
        if rec.blocked:
            t.blocked_dispatches += 1
        if rec.verdict == "success":
            t.verdict_successes += 1
        elif rec.verdict == "failure":
            t.verdict_failures += 1
        if rec.place_class == DWELL_ONLY:
            t.dwell_only_steps += 1

        if rec.outcome in ("SIM_END", "MAX_EVENTS"):
            t.terminal_tag = rec.outcome
            t.emit("TOKEN", f"END            {rec.outcome} at {rec.place}",
                   "the walk's end is recorded, never an unexplained stop")
            return
        if not rec.blocked and not rec.interrupted:
            t.action_time += max(0.0, rec.end_time - rec.start_time - rec.dwell)

        if rec.place_class == DWELL_ONLY:
            what = f"STEP           {rec.place} (dwell-only)"
        elif rec.blocked:
            what = f"STEP           {rec.place}: {rec.verb} blocked — precondition unmet"
        else:
            what = f"STEP           {rec.place}: {rec.verb} -> {rec.verdict or '—'}"
        dest = rec.next_place if rec.next_place is not None else "(walk ends)"
        t.emit("TOKEN", what,
               f"dwell {rec.dwell:.1f} + verb "
               f"{max(0.0, rec.end_time - rec.start_time - rec.dwell):.1f} t/u "
               f"→ {dest}")


# --- the two driven-arm substrate patches ------------------------------------

def _install_driven(tracer: L3Tracer) -> list:
    """Patch the two seams the driven arm uses that the substrate tracer's
    ``_install`` does not narrate: ``step`` (verbs bypass ``_execute_*``) and
    ``apply_mtd_interrupt_cost`` (the driven arm's penalty path — it never calls
    ``_handle_interrupt``). Same contract: delegate unchanged, record only."""
    undo = []

    def patch(owner, name, factory):
        orig = getattr(owner, name)
        setattr(owner, name, factory(orig))
        undo.append(lambda: setattr(owner, name, orig))

    def step(orig):
        def w(self_ao, verb):
            t0 = self_ao.env.now
            try:
                outcome = yield from orig(self_ao, verb)
            except simpy.Interrupt:
                tracer.verb_interrupts += 1
                tracer.emit("ATTACKER",
                            f"{verb:<14} interrupted after "
                            f"{self_ao.env.now - t0:.1f} t/u",
                            "an MTD mutation cut the verb mid-run")
                raise
            spent = self_ao.env.now - t0
            if outcome is STEP_ABORTED or outcome == EXPLOIT_HALTED:
                tracer.emit("ATTACKER", f"{verb:<14} halted by simulation end",
                            tracer._standing())
            else:
                tracer.emit("ATTACKER",
                            f"{verb:<14} ran for {spent:.1f} t/u",
                            f"outcome {outcome!r} · {tracer._standing()}")
            return outcome
        return w

    patch(AttackOperation, "step", step)

    def penalty(orig):
        def w(self_ao, interrupted_mtd):
            t0 = self_ao.env.now
            yield from orig(self_ao, interrupted_mtd)
            cost = self_ao.env.now - t0
            tracer.penalty_time += cost
            layer = interrupted_mtd.get_resource_type() if interrupted_mtd else "?"
            tracer.emit("INTERRUPT",
                        f"SETBACK        attacker pays {cost:.1f} t/u confusion penalty",
                        f"{layer}-layer mutation · {tracer._standing()}")
        return w

    patch(AttackOperation, "apply_mtd_interrupt_cost", penalty)
    return undo


# --- run ---------------------------------------------------------------------

def run_l3_trace(
    profile: str = "aggregate",
    *,
    mapping_version: str | None = None,
    overlay_version: str | None = None,
    seed: int = 0,
    horizon: float = 15_000,
    with_synthetic_overlay: bool = True,
    constant_timing: bool = False,
    mtd_scheme: str | None = None,
    mtd_interval: int | None = 200,
    custom_strategies=None,
    geometry: dict | None = None,
    max_events: int = 50_000,
) -> tuple[L3Tracer, MovementRunResult]:
    """Run one movement-layer simulation with unified tracing on.

    Mirrors :func:`mtdsim.l3_simulation.movement.run.run_movement`'s wiring
    (same builders, same construction order, same RNG discipline) so a traced
    run and an untraced run of the same configuration are identical — the parity
    test pins this. Returns ``(tracer, MovementRunResult)``.
    """
    env, end_event, network, adversary, attack_op = _build_sim(seed, geometry)

    routing_net = load_routing_net(profile, with_synthetic_overlay=with_synthetic_overlay)
    controller = load_controller(version=mapping_version)
    overlay = load_outcome_overlay(version=overlay_version)
    dwell = load_dwell_catalogue()
    timing_cls = ConstantTiming if constant_timing else TacticTiming
    timing = timing_cls(dwell, seed=seed)

    tracer = L3Tracer(
        env=env, adversary=adversary, network=network,
        profile=profile,
        mapping_version=getattr(controller, "version", "") or "default",
        overlay_version=getattr(overlay, "version", "") or "default",
        timing_regime="constant" if constant_timing else "exponential (S3)",
        scheme=mtd_scheme or "none",
    )

    attacker = MovementAttacker(
        env=env,
        end_event=end_event,
        adversary=adversary,
        attack_operation=attack_op,
        routing_net=routing_net,
        controller=_TracedController(controller, tracer),
        overlay=_TracedOverlay(overlay, tracer),
        verdict_of=_TracedVerdict(verdict_for, tracer),
        dwell_catalogue=dwell,
        timing=_TracedTiming(timing, tracer),
        seed=seed,
        max_events=max_events,
    )
    attacker.records = _NarratingRecords(tracer)
    attacker.start()

    mtd_op = _maybe_start_mtd(
        env=env,
        end_event=end_event,
        network=network,
        adversary=adversary,
        attack_op=attack_op,
        scheme=mtd_scheme,
        mtd_interval=mtd_interval,
        custom_strategies=custom_strategies,
    )

    # Nothing has executed yet (SimPy runs processes only inside env.run), so
    # installing the substrate hooks here keeps run_movement's construction
    # order — and therefore its RNG stream — exactly.
    undo = _install(tracer, attack_op, mtd_op) + _install_driven(tracer)
    try:
        geo = geometry or GEOMETRY
        tracer.emit("NETWORK",
                    f"Network generated: {geo['total_nodes']} hosts, "
                    f"{geo['total_endpoints']} internet-facing",
                    f"objective is {geo['terminate_compromise_ratio']:.0%} "
                    "of the network")
        tracer.emit("TOKEN",
                    f"Walk begins: profile {profile}, entry at "
                    f"{routing_net.entry_place}",
                    f"mapping {tracer.mapping_version} · overlay "
                    f"{tracer.overlay_version} · timing {tracer.timing_regime}")
        env.run(until=horizon)
        if end_event.triggered:
            tracer.emit("COMPROMISE",
                        "OBJECTIVE      the attacker reached its compromise "
                        "threshold — simulation ends", tracer._standing())
    finally:
        for u in reversed(undo):
            u()

    records = tuple(attacker.records)
    termination_time = records[-1].end_time if records else float(env.now)
    result = MovementRunResult(
        profile=profile,
        seed=seed,
        with_synthetic_overlay=with_synthetic_overlay,
        records=records,
        reached_objective=bool(end_event.triggered),
        termination_time=termination_time,
        compromised_count=len(adversary.get_compromised_hosts()),
    )
    return tracer, result


# --- the verdict -------------------------------------------------------------

def _l3_verdict(tracer: L3Tracer, result: MovementRunResult, horizon: float,
                colour: bool) -> str:
    lines = []

    def head(t):
        lines.append("")
        lines.append(_paint(t, "bold", colour))
        lines.append("-" * len(t))

    head("The run")
    lines.append(f"  Profile {tracer.profile} · mapping {tracer.mapping_version} · "
                 f"overlay {tracer.overlay_version}")
    lines.append(f"  Timing {tracer.timing_regime} · MTD scheme {tracer.scheme} · "
                 f"seed {result.seed}")

    head("How the token moved")
    lines.append(f"  {tracer.steps} step(s) across "
                 f"{len(tracer.visits_by_place)} distinct place(s); "
                 f"{tracer.dwell_only_steps} dwell-only.")
    if tracer.terminal_tag == "MAX_EVENTS":
        lines.append("  Terminated by the MAX_EVENTS backstop — a pathological "
                     "cycle, not a policy outcome.")
    elif result.reached_objective:
        lines.append(f"  Reached the compromise objective at "
                     f"t={result.termination_time:.1f} "
                     f"({100 * result.termination_time / horizon:.0f}% of the "
                     "horizon).")
    elif tracer.stalled:
        lines.append("  The walk STALLED: a failure verdict suppressed every "
                     "out-edge. The overlay ended this run, not the horizon.")
    elif tracer.terminal_tag == "SIM_END":
        lines.append("  The simulation ended mid-walk.")
    elif result.records and result.records[-1].next_place is None:
        lines.append("  The token reached a sink (a place with no out-edges).")
    else:
        lines.append(f"  The horizon ({horizon:.0f} t/u) ended the walk "
                     "mid-movement.")
    top_places = sorted(tracer.time_by_place.items(), key=lambda kv: -kv[1])[:3]
    if top_places:
        spent = " · ".join(f"{p} {v:.0f}" for p, v in top_places)
        lines.append(f"  Most time at: {spent} (t/u).")

    head("The controller's decisions")
    if tracer.dispatches_by_verb:
        by_verb = " · ".join(f"{v} ×{n}" for v, n in
                             sorted(tracer.dispatches_by_verb.items(),
                                    key=lambda kv: -kv[1]))
        lines.append(f"  Dispatches: {by_verb}.")
    else:
        lines.append("  No verb was ever dispatched (an all-dwell-only walk).")
    judged = tracer.verdict_successes + tracer.verdict_failures
    if judged:
        lines.append(f"  Verdicts: {tracer.verdict_successes} success / "
                     f"{tracer.verdict_failures} failure "
                     f"({100 * tracer.verdict_successes / judged:.0f}% success "
                     "rate).")
    if tracer.blocked_dispatches:
        lines.append(f"  {tracer.blocked_dispatches} dispatch(es) blocked on an "
                     "unmet substrate precondition — the coupling surface, "
                     "visible as data.")
    if tracer.interrupted_steps:
        dwell_cut = tracer.interrupted_steps - tracer.verb_interrupts
        lines.append(f"  {tracer.interrupted_steps} step(s) interrupted by MTD "
                     f"({tracer.verb_interrupts} mid-verb, {dwell_cut} "
                     "mid-dwell), each read as a failure verdict.")

    head("Where the time went")
    elapsed = result.termination_time if result.records else horizon
    if elapsed > 0:
        parts = (
            ("dwelling (behavioural tempo)", tracer.dwell_time),
            ("running verbs (substrate cost)", tracer.action_time),
            ("interrupt penalties", tracer.penalty_time),
        )
        for label, v in parts:
            lines.append(f"  {label}: {v:.0f} t/u ({100 * v / elapsed:.0f}%).")

    head("How the defence did")
    if tracer.mtd_triggered == 0:
        lines.append("  No MTD was deployed — this run shows the walker unopposed.")
    else:
        lines.append(f"  Deployed {tracer.mtd_completed} mutation(s); "
                     f"{tracer.mtd_suspended} held back by resource contention.")
        lines.append(f"  Caught the walker {tracer.interrupts} time(s); total "
                     f"confusion cost {tracer.penalty_time:.0f} t/u.")

    head("The substrate ground truth")
    owned = result.compromised_count
    total = len(tracer.network.get_graph().nodes())
    if tracer.first_compromise is None:
        lines.append("  No host was compromised.")
    else:
        lines.append(f"  First foothold at t={tracer.first_compromise:.1f}; "
                     f"ended owning {owned} of {total} hosts "
                     f"({100 * owned / total:.0f}%).")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Unified event log of an L3 movement run: token, controller "
                    "and substrate on one clock.",
    )
    ap.add_argument("profile", nargs="?", default="aggregate", choices=PROFILES)
    ap.add_argument("--mapping", default=None, dest="mapping_version",
                    help="controller mapping version (e.g. v1_ckc_total, v2_partial)")
    ap.add_argument("--overlay-version", default=None,
                    help="outcome-overlay version (e.g. v1_band_relationship)")
    ap.add_argument("--scheme", default=None,
                    help="MTD scheme (e.g. simultaneous); omit for unopposed")
    ap.add_argument("--interval", type=int, default=200, dest="mtd_interval")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--horizon", type=float, default=15_000)
    ap.add_argument("--no-synthetic-overlay", action="store_true",
                    help="the observed-only arm (seed at initial-access)")
    ap.add_argument("--constant-timing", action="store_true",
                    help="the pre-S3 fixed-dwell regime (verification arm)")
    ap.add_argument("--only", default=None,
                    help="comma-separated actors, e.g. token,controller")
    ap.add_argument("--no-colour", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="verdict only")
    args = ap.parse_args(argv)

    colour = not args.no_colour and sys.stdout.isatty()

    tracer, result = run_l3_trace(
        args.profile,
        mapping_version=args.mapping_version,
        overlay_version=args.overlay_version,
        seed=args.seed,
        horizon=args.horizon,
        with_synthetic_overlay=not args.no_synthetic_overlay,
        constant_timing=args.constant_timing,
        mtd_scheme=args.scheme,
        mtd_interval=args.mtd_interval,
    )

    if not args.quiet:
        wanted = None
        if args.only:
            wanted = {a.strip().upper() for a in args.only.split(",")}
        header = f"  {'time':>11}  {'actor':<10}  what happened"
        print(header)
        print("  " + "-" * (len(header) - 2))
        for ev in tracer.events:
            if wanted is None or ev.actor in wanted:
                print(ev.render(colour))

    print(_l3_verdict(tracer, result, args.horizon, colour))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
