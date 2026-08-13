"""Watch a simulation happen — a colour-coded, event-by-event log of the contest.

The batch runners tell you *who won*. This tells you *how it went*: every event,
in simulated-time order, from all three actors — the attacker working through the
network, the defender firing MTD strategies, and the mutations those strategies
make to the network underneath the attacker.

It exists to answer questions the summary statistics cannot:

- Is the attacker struggling to get a foothold, or did it walk straight in?
- Are the MTD strategies actually interrupting the attacker, or firing into empty
  air while it works elsewhere?
- When an MTD does land, how much does it cost the attacker — and does the
  attacker recover the ground it lost?
- Is the defence keeping up, or is the attacker compromising hosts faster than the
  network can be reshuffled?

Usage
-----
    python -m mtdnetwork.trace                          # random scheme, 2000 t/u
    python -m mtdnetwork.trace --scheme none            # attacker alone: how fast unopposed?
    python -m mtdnetwork.trace --scheme single --mtd OSDiversity
    python -m mtdnetwork.trace --scheme simultaneous --finish-time 5000
    python -m mtdnetwork.trace --only attacker,compromise    # filter the stream
    python -m mtdnetwork.trace --no-colour > run.log         # plain text for a file

Every line is ``time · actor · what happened``, so the log reads chronologically
and can be grepped by actor. A verdict section at the end scores the contest.

Reading the log
---------------
    ATTACKER    the six attack phases: discovery, enumeration, port scan,
                exploitation, brute force, lateral movement
    COMPROMISE  the attacker took a host (or harvested credentials)
    DEFENDER    an MTD strategy was triggered, deployed, suspended or completed
    MUTATION    what the strategy actually changed in the network
    INTERRUPT   an MTD caught the attacker mid-action; the confusion penalty
    NETWORK     the attacker's view of the network changed

Instrumentation is read-only and consumes no randomness, so a traced run is
identical to the same seed run untraced (pinned by ``tests/test_trace.py``).

This is a **living diagnostic tool**, not a frozen artefact (ported from the
standalone ``main`` branch, commit 31ce3be). Sessions verifying substrate
changes, chasing a bug, or demonstrating a run should extend it — new hooks for
new seams, new tallies for new questions — keeping the two invariants above:
wrappers delegate unchanged, and draw no randomness. See
``docs/implementation/trace_tool.md``.
"""

from __future__ import annotations

import argparse
import random
import sys
import warnings
from dataclasses import dataclass, field

warnings.filterwarnings(
    "ignore", message="pkg_resources is deprecated as an API.*", category=UserWarning,
)

import numpy as np
import simpy

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_generator import set_exponential_regime
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD, MTD_TRIGGER_INTERVAL
from mtdnetwork.mtd import MTD
from mtdnetwork.operation.attack_operation import AttackOperation
from mtdnetwork.operation.mtd_operation import MTDOperation
from mtdnetwork.statistic.security_metric_statistics import SecurityMetricStatistics

# --- presentation -----------------------------------------------------------

ACTORS = ("ATTACKER", "COMPROMISE", "DEFENDER", "MUTATION", "INTERRUPT", "NETWORK")

_ANSI = {
    "ATTACKER": "\033[38;5;203m",    # red — the offence
    "COMPROMISE": "\033[1;38;5;196m",  # bold red — the offence scoring
    "DEFENDER": "\033[38;5;39m",     # blue — the defence
    "MUTATION": "\033[38;5;51m",     # cyan — the network changing shape
    "INTERRUPT": "\033[1;38;5;214m",  # bold amber — the defence scoring
    "NETWORK": "\033[38;5;108m",     # green — the terrain
    # The two movement-layer actors (emitted only by the L3 unified trace,
    # mtdsim.l3_simulation.trace — kept here so the whole family shares one palette).
    "TOKEN": "\033[38;5;177m",       # orchid — the net-walker moving
    "CONTROLLER": "\033[38;5;179m",  # tan — the dispatch/verdict/routing decisions
    "dim": "\033[2m",
    "bold": "\033[1m",
    "reset": "\033[0m",
}


def _paint(text: str, key: str, colour: bool) -> str:
    if not colour or key not in _ANSI:
        return text
    return f"{_ANSI[key]}{text}{_ANSI['reset']}"


@dataclass
class Event:
    time: float
    actor: str
    message: str
    detail: str = ""

    def render(self, colour: bool) -> str:
        stamp = f"t={self.time:>9.1f}"
        actor = f"{self.actor:<10}"
        line = f"  {stamp}  {_paint(actor, self.actor, colour)}  {self.message}"
        if self.detail:
            line += "  " + _paint(self.detail, "dim", colour)
        return line


@dataclass
class Tracer:
    """Collects the event stream and the running score of the contest."""

    env: simpy.Environment
    adversary: object
    network: object
    events: list[Event] = field(default_factory=list)

    # running tallies for the verdict
    mtd_triggered: int = 0
    mtd_completed: int = 0
    mtd_suspended: int = 0
    interrupts: int = 0
    penalty_time: float = 0.0
    positions_lost: int = 0
    give_ups: int = 0
    first_compromise: float | None = None
    compromise_times: list[float] = field(default_factory=list)
    exploit_attempts: int = 0

    def emit(self, actor: str, message: str, detail: str = "") -> None:
        self.events.append(Event(float(self.env.now), actor, message, detail))

    # -- the picture of the attacker's standing ---------------------------
    def _standing(self) -> str:
        owned = len(self.adversary.get_compromised_hosts())
        total = len(self.network.get_graph().nodes())
        return f"owns {owned}/{total}"


def _install(tracer: Tracer, attack_op, mtd_op) -> list:
    """Wrap the simulator's seams so each meaningful moment emits an event.

    Every wrapper delegates to the original unchanged and only records — no RNG is
    drawn and no state is written, so the traced run matches an untraced one.
    """
    undo = []

    def patch(owner, name, factory):
        orig = getattr(owner, name)
        setattr(owner, name, factory(orig))
        undo.append(lambda: setattr(owner, name, orig))

    adv = tracer.adversary

    # --- attacker: the six phases ------------------------------------------
    def scan_host(orig):
        def w(self_ao):
            before = len(adv.get_host_stack())
            r = orig(self_ao)
            found = len(adv.get_host_stack())
            if found:
                tracer.emit("ATTACKER", f"SCAN_HOST      mapped the reachable network",
                            f"{found} host(s) queued (was {before}) · {tracer._standing()}")
            else:
                tracer.emit("ATTACKER", "SCAN_HOST      found nothing reachable — attack stalls",
                            tracer._standing())
            return r
        return w

    def enum_host(orig):
        def w(self_ao):
            r = orig(self_ao)
            hid = adv.get_curr_host_id()
            attempts = adv.get_attack_counter()[hid] if hid >= 0 else 0
            gave_up = len(adv.get_stop_attack())
            if gave_up > tracer.give_ups:
                tracer.give_ups = gave_up
                tracer.emit("ATTACKER",
                            f"GIVE UP        host {hid} abandoned after "
                            f"{attempts} attempts",
                            "the defence held this one")
            if r:
                tracer.emit("ATTACKER", f"ENUM_HOST      revisited host {hid} (already owned)",
                            f"attempt {attempts}/{adv.get_attack_threshold()}")
            else:
                tracer.emit("ATTACKER", f"ENUM_HOST      picked host {hid} to attack",
                            f"attempt {attempts}/{adv.get_attack_threshold()} · "
                            f"{len(adv.get_host_stack())} left in queue")
            return r
        return w

    def scan_port(orig):
        def w(self_ao):
            r = orig(self_ao)
            hid = adv.get_curr_host_id()
            ports = len(adv.get_curr_ports())
            if r:
                tracer.emit("ATTACKER",
                            f"SCAN_PORT      host {hid}: reused credentials worked",
                            f"{ports} port(s) open — no exploit needed")
            else:
                tracer.emit("ATTACKER", f"SCAN_PORT      host {hid}: {ports} open port(s)",
                            "no credential reuse — must exploit a vulnerability")
            return r
        return w

    def brute_force(orig):
        def w(self_ao):
            r = orig(self_ao)
            hid = adv.get_curr_host_id()
            tracer.emit("ATTACKER",
                        f"BRUTE_FORCE    host {hid}: credential guess "
                        f"{'succeeded' if r else 'failed'}",
                        "last resort after exploitation failed")
            return r
        return w

    def scan_neighbors(orig):
        def w(self_ao):
            before = len(adv.get_host_stack())
            r = orig(self_ao)
            after = len(adv.get_host_stack())
            tracer.emit("ATTACKER",
                        f"SCAN_NEIGHBOR  spread out from host {adv.get_curr_host_id()}",
                        f"queue {before} → {after} · {tracer._standing()}")
            return r
        return w

    for name, factory in (("_execute_scan_host", scan_host),
                          ("_execute_enum_host", enum_host),
                          ("_execute_scan_port", scan_port),
                          ("_execute_brute_force", brute_force),
                          ("_execute_scan_neighbors", scan_neighbors)):
        if hasattr(AttackOperation, name):
            patch(AttackOperation, name, factory)

    # Exploitation is a generator, and the interesting part is how long it took.
    def exploit(orig):
        def w(self_ao, vulns):
            hid = adv.get_curr_host_id()
            t0 = self_ao.env.now
            tracer.exploit_attempts += 1
            tracer.emit("ATTACKER",
                        f"EXPLOIT_VULN   host {hid}: trying {len(vulns)} vulnerabilit"
                        f"{'y' if len(vulns) == 1 else 'ies'}",
                        "each one costs time proportional to its difficulty")
            r = yield from orig(self_ao, vulns)
            spent = self_ao.env.now - t0
            if spent > 0:
                tracer.emit("ATTACKER", f"EXPLOIT_VULN   host {hid}: spent {spent:.1f} t/u",
                            tracer._standing())
            return r
        return w

    for cand in ("_execute_exploit_vuln", "_do_exploit_vuln"):
        if hasattr(AttackOperation, cand):
            patch(AttackOperation, cand, exploit)
            break

    # --- the attacker scoring ---------------------------------------------
    def compromise(orig):
        def w(self_ao, now, proceed_time):
            before = list(adv.get_compromised_hosts())
            r = orig(self_ao, now, proceed_time)
            after = adv.get_compromised_hosts()
            fresh = [h for h in after if h not in before]
            for h in fresh:
                t = float(self_ao.env.now)
                if tracer.first_compromise is None:
                    tracer.first_compromise = t
                    tracer.emit("COMPROMISE",
                                f"FOOTHOLD       host {h} compromised — the attacker is in",
                                f"took {t:.1f} t/u to get its first host")
                else:
                    tracer.emit("COMPROMISE", f"HOST OWNED     host {h} compromised",
                                f"{tracer._standing()} · "
                                f"{len(adv.get_compromised_users())} credential(s) harvested")
                tracer.compromise_times.append(t)
            return r
        return w

    patch(AttackOperation, "update_compromise_progress", compromise)

    # --- the defender: MTD lifecycle ---------------------------------------
    def execute_mtd(orig):
        def w(self_mo, env, mtd):
            tracer.mtd_triggered += 1
            tracer.emit("DEFENDER",
                        f"DEPLOY         {mtd.get_name()} starting "
                        f"({mtd.get_resource_type()} layer)",
                        f"takes ~{mtd.get_execution_time_mean():.0f} t/u to apply")
            t0 = env.now
            yield from orig(self_mo, env, mtd)
            tracer.mtd_completed += 1
            tracer.emit("DEFENDER",
                        f"COMPLETE       {mtd.get_name()} finished in {env.now - t0:.1f} t/u",
                        "the attack surface has moved")
        return w

    patch(MTDOperation, "_mtd_execute_action", execute_mtd)

    def mutate(orig):
        def w(self_mtd, adversary=None):
            r = orig(self_mtd, adversary)
            tracer.emit("MUTATION", f"{self_mtd.get_name()}: {_describe(self_mtd)}",
                        "anything the attacker had learned about this is now stale")
            return r
        return w

    for cls in _mtd_subclasses():
        if "mtd_operation" in cls.__dict__:
            patch(cls, "mtd_operation", mutate)

    def suspend(orig):
        # The parameter name must match the substrate's (mtd_strategy): the
        # scheme is called both positionally and by keyword.
        def w(self_scheme, mtd_strategy):
            tracer.mtd_suspended += 1
            tracer.emit("DEFENDER",
                        f"SUSPEND        {mtd_strategy.get_name()} held back — "
                        f"{mtd_strategy.get_resource_type()} layer already busy",
                        "the defence cannot run two mutations on one resource")
            return orig(self_scheme, mtd_strategy)
        return w

    scheme = getattr(mtd_op, "_mtd_scheme", None) if mtd_op else None
    if scheme is not None and hasattr(type(scheme), "suspend_mtd"):
        patch(type(scheme), "suspend_mtd", suspend)

    # --- the defence scoring ----------------------------------------------
    def interrupt_adv(orig):
        def w(self_mo, env, mtd):
            phase = adv.get_curr_process()
            before = tracer.interrupts
            proc = self_mo.attack_operation.get_attack_process()
            alive = proc is not None and proc.is_alive
            r = orig(self_mo, env, mtd)
            if alive and self_mo.attack_operation._interrupted_mtd is mtd:
                tracer.interrupts += 1
                lost = mtd.get_resource_type() == "network"
                if lost:
                    tracer.positions_lost += 1
                tracer.emit("INTERRUPT",
                            f"CAUGHT         {mtd.get_name()} hit the attacker "
                            f"mid-{phase}",
                            "connection to the host is lost — must re-discover" if lost
                            else "service connection lost — must re-scan ports")
            elif tracer.interrupts == before and mtd.get_resource_type() != "reserve":
                tracer.emit("DEFENDER",
                            f"MISSED         {mtd.get_name()} fired but caught nothing",
                            f"attacker was in {phase} — unaffected by this layer")
            return r
        return w

    patch(MTDOperation, "_interrupt_adversary", interrupt_adv)

    def handle_interrupt(orig):
        def w(self_ao, start_time, name):
            t0 = self_ao.env.now
            yield from orig(self_ao, start_time, name)
            cost = self_ao.env.now - t0
            tracer.penalty_time += cost
            tracer.emit("INTERRUPT",
                        f"SETBACK        attacker confused for {cost:.1f} t/u",
                        f"restarting at {adv.get_curr_process()} · {tracer._standing()}")
        return w

    patch(AttackOperation, "_handle_interrupt", handle_interrupt)

    return undo


def _mtd_subclasses():
    stack = [MTD]
    seen = []
    while stack:
        cls = stack.pop()
        for sub in cls.__subclasses__():
            if sub not in seen:
                seen.append(sub)
                stack.append(sub)
    return seen


def _describe(mtd) -> str:
    """One plain sentence about what this strategy changes."""
    return {
        "IPShuffle": "every internal host has a new IP address",
        "PortShuffle": "services are listening on different ports",
        "OSDiversity": "hosts are running different operating systems",
        "ServiceDiversity": "hosts are running different service versions",
        "OSDiversityAssignment": "operating systems reassigned to maximise variety",
        "CompleteTopologyShuffle": "the network has been rewired end to end",
        "HostTopologyShuffle": "hosts have swapped places in the topology",
        "UserShuffle": "user accounts and passwords have been rotated",
    }.get(mtd.get_name(), "the attack surface has changed")


# --- the verdict ------------------------------------------------------------

def _verdict(tracer: Tracer, horizon: float, colour: bool) -> str:
    adv = tracer.adversary
    owned = len(adv.get_compromised_hosts())
    total = len(tracer.network.get_graph().nodes())
    lines = []

    def head(t):
        lines.append("")
        lines.append(_paint(t, "bold", colour))
        lines.append("-" * len(t))

    head("How the attacker did")
    if tracer.first_compromise is None:
        lines.append(f"  Never got a foothold in {horizon:.0f} t/u — no host compromised.")
    else:
        lines.append(f"  First foothold at t={tracer.first_compromise:.1f} "
                     f"({100 * tracer.first_compromise / horizon:.0f}% of the run elapsed).")
        lines.append(f"  Ended owning {owned} of {total} hosts "
                     f"({100 * owned / total:.0f}% of the network).")
        if len(tracer.compromise_times) > 1:
            span = tracer.compromise_times[-1] - tracer.compromise_times[0]
            if span > 0:
                rate = (len(tracer.compromise_times) - 1) / span
                lines.append(f"  Averaged one new host every "
                             f"{1 / rate:.0f} t/u once it was inside.")
    if tracer.give_ups:
        lines.append(f"  Gave up on {tracer.give_ups} host(s) after "
                     f"{ATTACKER_THRESHOLD} failed attempts each.")

    head("How the defence did")
    if tracer.mtd_triggered == 0:
        lines.append("  No MTD was deployed — this run shows the attacker unopposed.")
    else:
        lines.append(f"  Deployed {tracer.mtd_completed} mutation(s); "
                     f"{tracer.mtd_suspended} were held back by resource contention.")
        lines.append(f"  Caught the attacker mid-action {tracer.interrupts} time(s), "
                     f"of which {tracer.positions_lost} cost it its position entirely.")
        lines.append(f"  Total attacker time lost to confusion: "
                     f"{tracer.penalty_time:.0f} t/u "
                     f"({100 * tracer.penalty_time / horizon:.0f}% of the run).")
        if tracer.mtd_completed:
            hit_rate = 100 * tracer.interrupts / tracer.mtd_completed
            lines.append(f"  Hit rate: {hit_rate:.0f}% of mutations landed on the "
                         f"attacker rather than firing into empty air.")

    head("Reading the contest")
    if tracer.mtd_triggered == 0:
        # Undefended: there is no contest, so read it as the control case.
        lines.append("  Undefended run — this is the control, not a contest.")
        if tracer.first_compromise is None:
            lines.append("  The attacker did not get in even unopposed, so the horizon")
            lines.append("  is too short to judge any defence against. Raise")
            lines.append("  --finish-time before comparing.")
        elif owned >= total * 0.8:
            lines.append("  The attacker took the network with nothing in its way.")
            lines.append("  Run the same seed with a defence and compare how far it")
            lines.append("  gets and how long it takes.")
        else:
            lines.append(f"  The attacker reached {owned}/{total} hosts in "
                         f"{horizon:.0f} t/u. A defended run that does materially")
            lines.append("  worse than this is being genuinely held back.")
    elif tracer.first_compromise is None:
        lines.append("  The defence won: the attacker never established a foothold.")
        lines.append("  Check the undefended run at the same seed to confirm it")
        lines.append("  could have got in at all — otherwise this proves nothing.")
    elif owned >= total * 0.8:
        lines.append("  The attacker won despite the defence — it took the network.")
        lines.append("  The mutations slowed it down but never broke its momentum.")
    elif owned <= max(1, total * 0.1):
        lines.append("  The defence largely held: the attacker got in but was")
        lines.append("  contained, losing position faster than it could spread.")
    else:
        lines.append("  A genuine contest: the attacker made progress but the")
        lines.append("  defence kept taking it back. Neither side dominated.")

    if tracer.mtd_triggered and tracer.interrupts == 0:
        lines.append("")
        lines.append("  Note: every mutation missed. The defence is firing, but not")
        lines.append("  where the attacker is working — a scheduling problem, not a")
        lines.append("  strength problem. Try a shorter interval.")
    elif tracer.mtd_suspended > tracer.mtd_completed:
        lines.append("")
        lines.append("  Note: more mutations were held back than deployed. The")
        lines.append("  defence is trying to fire faster than the network can absorb.")
    return "\n".join(lines)


# --- run --------------------------------------------------------------------

def run_trace(*, scheme: str = "random", mtd_interval: int | None = None,
              custom_strategies=None, seed: int = 1234, finish_time: float = 2000.0,
              total_nodes: int = 50, total_endpoints: int = 5, total_subnets: int = 8,
              total_layers: int = 4, target_layer: int = 4, total_database: int = 2,
              terminate_compromise_ratio: float = 0.8,
              timing_regime: str = "shifted") -> tuple[Tracer, float]:
    """Run one simulation with tracing on. Returns (tracer, horizon)."""
    random.seed(seed)
    np.random.seed(seed)
    set_exponential_regime(timing_regime)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(
        total_nodes=total_nodes, total_endpoints=total_endpoints,
        total_subnets=total_subnets, total_layers=total_layers,
        target_layer=target_layer, total_database=total_database,
        terminate_compromise_ratio=terminate_compromise_ratio,
    )
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(env=env, end_event=end_event, adversary=adversary,
                                proceed_time=0)
    mtd_op = None
    if scheme and scheme.lower() != "none":
        # The published per-scheme intervals only cover the multi-MTD schemes; fall
        # back to the lineage's canonical experiment interval otherwise.
        if mtd_interval is None and scheme not in MTD_TRIGGER_INTERVAL:
            mtd_interval = 200
        mtd_op = MTDOperation(
            security_metrics_record=SecurityMetricStatistics(), env=env,
            end_event=end_event, network=network, attack_operation=attack_op,
            scheme=scheme, adversary=adversary, proceed_time=0,
            mtd_trigger_interval=mtd_interval, custom_strategies=custom_strategies,
        )

    tracer = Tracer(env=env, adversary=adversary, network=network)
    undo = _install(tracer, attack_op, mtd_op)
    try:
        tracer.emit("NETWORK", f"Network generated: {total_nodes} hosts, "
                               f"{total_endpoints} internet-facing",
                    f"attacker starts outside · objective is "
                    f"{terminate_compromise_ratio:.0%} of the network")
        if mtd_op is not None:
            mtd_op.proceed_mtd()
        attack_op.proceed_attack()
        env.run(until=finish_time)
        if end_event.triggered:
            tracer.emit("COMPROMISE", "OBJECTIVE      the attacker reached its "
                                      "compromise threshold — simulation ends",
                        tracer._standing())
    finally:
        for u in reversed(undo):
            u()
    return tracer, float(finish_time)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Colour-coded, event-by-event log of an MTDSim run.",
        epilog="Try `--scheme none` first to see the attacker unopposed, then "
               "re-run with a defence and compare.",
    )
    ap.add_argument("--scheme", default="random",
                    help="none | single | random | alternative | simultaneous")
    ap.add_argument("--mtd", action="append", dest="mtds", default=None,
                    help="MTD strategy name (repeatable), for single/alternative")
    ap.add_argument("--interval", type=int, default=None, dest="mtd_interval",
                    help="mean MTD trigger interval")
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--finish-time", type=float, default=2000.0)
    ap.add_argument("--nodes", type=int, default=50, dest="total_nodes",
                    help="network size")
    ap.add_argument("--only", default=None,
                    help="comma-separated actors to show, e.g. attacker,compromise")
    ap.add_argument("--no-colour", action="store_true", help="plain text output")
    ap.add_argument("--quiet", action="store_true", help="verdict only, no event log")
    ap.add_argument("--timing-regime", default="shifted",
                    choices=["shifted", "exponential"],
                    help="exponential_variates regime: 'shifted' (inherited, "
                         "mean + Exp(0.5)) or 'exponential' (true Exp(mean); D-08)")
    args = ap.parse_args(argv)

    colour = not args.no_colour and sys.stdout.isatty()

    strategies = None
    if args.mtds:
        import importlib
        strategies = []
        for name in args.mtds:
            mod = importlib.import_module(f"mtdnetwork.mtd.{name.lower()}")
            strategies.append(getattr(mod, name))
        if len(strategies) == 1:
            strategies = strategies[0]

    tracer, horizon = run_trace(
        scheme=args.scheme, mtd_interval=args.mtd_interval,
        custom_strategies=strategies, seed=args.seed,
        finish_time=args.finish_time, total_nodes=args.total_nodes,
        timing_regime=args.timing_regime,
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

    print(_verdict(tracer, horizon, colour))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
