"""A step debugger for the MTDSim discrete-event simulation — gdb for SimPy.

The simulator is a SimPy discrete-event loop, so "what actually happened" is a
sequence of scheduled events, not a stack trace. Ordinary debugging bounces you
between generator frames with no view of simulated time or of the adversary state
the verbs communicate through. This tool gives the DES-native view instead:

    step        advance exactly one scheduled event
    continue    run until a breakpoint or the horizon
    break       stop when a condition on the world becomes true
    print       the adversary's shared state at this instant

**How it works.** SimPy exposes its event queue as ``env._queue`` and steps it with
``env.step()``. This wraps that loop, and after each step samples the adversary and
network state that the attack verbs read and mutate — ``curr_process``,
``curr_host``, the ``host_stack`` work queue, the give-up list, the attempt counter,
and the compromised set. It also instruments the substrate's own seams (verb cores,
compromise recording, MTD interrupts and the confusion penalty) so each event is
labelled with what the simulator was *doing*, not just which generator resumed.

Nothing here changes simulation behaviour: the probes are read-only wrappers and
the RNG is untouched, so a traced run is identical to an untraced one (asserted by
``tests/test_des_step.py``).

Usage
-----
    python tools/des_step.py --seed 1234 --until 400          # trace the native arm
    python tools/des_step.py --mtd simultaneous --break-on interrupt
    python tools/des_step.py --arm movement --profile aggregate --break-on compromise

Programmatic:
    from tools.des_step import DESDebugger
    dbg = DESDebugger.native(seed=1234)
    dbg.run_until(lambda w: w.compromised_count >= 1)
    print(dbg.format_trace())
"""
from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import numpy as np
import simpy

_REPO_ROOT = Path(__file__).resolve().parents[1]
for _p in (str(_REPO_ROOT), str(_REPO_ROOT / "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from mtdnetwork.component.adversary import Adversary  # noqa: E402
from mtdnetwork.component.time_network import TimeNetwork  # noqa: E402
from mtdnetwork.data.constants import ATTACKER_THRESHOLD  # noqa: E402
from mtdnetwork.operation.attack_operation import AttackOperation  # noqa: E402

GEOMETRY = dict(
    total_nodes=50, total_endpoints=5, total_subnets=8, total_layers=4,
    target_layer=4, total_database=2, terminate_compromise_ratio=0.8,
)


@dataclass
class WorldState:
    """The adversary-visible world at one instant of simulated time."""

    step_index: int
    now: float
    note: str = ""              # what the simulator was doing, when known
    curr_process: str = ""
    curr_host_id: int = -1
    host_stack: int = 0         # length of the work queue
    curr_ports: int = 0
    compromised_count: int = 0
    given_up: int = 0
    max_attempt: int = 0
    queued_events: int = 0

    def line(self) -> str:
        return (
            f"[{self.step_index:>5}] t={self.now:>10.3f}  "
            f"{self.curr_process:<14} host={self.curr_host_id:>3}  "
            f"stack={self.host_stack:>3} ports={self.curr_ports:>3}  "
            f"owned={self.compromised_count:>3} gaveUp={self.given_up:>2} "
            f"maxAtt={self.max_attempt:>2}  q={self.queued_events:>2}"
            + (f"   {self.note}" if self.note else "")
        )


@dataclass
class DESDebugger:
    """Wraps a built simulation and steps its SimPy event queue one event at a time."""

    env: simpy.Environment
    end_event: simpy.Event
    network: Any
    adversary: Any
    attack_op: Any
    trace: list[WorldState] = field(default_factory=list)
    _pending_notes: list[str] = field(default_factory=list)
    _step_index: int = 0
    _uninstall: list[Callable[[], None]] = field(default_factory=list)

    # -- construction -------------------------------------------------------
    @staticmethod
    def _build(seed: int, geometry: dict | None = None):
        random.seed(seed)
        np.random.seed(seed)
        env = simpy.Environment()
        end_event = env.event()
        network = TimeNetwork(**(geometry or GEOMETRY))
        adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
        attack_op = AttackOperation(env=env, end_event=end_event,
                                    adversary=adversary, proceed_time=0)
        return env, end_event, network, adversary, attack_op

    @classmethod
    def native(cls, seed: int = 1234, mtd: str | None = None,
               mtd_interval: int = 200, geometry: dict | None = None) -> "DESDebugger":
        """The inherited 6-phase attacker, optionally under MTD."""
        env, end_event, network, adversary, attack_op = cls._build(seed, geometry)
        dbg = cls(env=env, end_event=end_event, network=network,
                  adversary=adversary, attack_op=attack_op)
        dbg._instrument()
        if mtd:
            from mtdnetwork.operation.mtd_operation import MTDOperation
            from mtdnetwork.statistic.security_metric_statistics import (
                SecurityMetricStatistics,
            )
            MTDOperation(
                security_metrics_record=SecurityMetricStatistics(), env=env,
                end_event=end_event, network=network, attack_operation=attack_op,
                scheme=mtd, adversary=adversary, proceed_time=0,
                mtd_trigger_interval=mtd_interval,
            ).proceed_mtd()
        attack_op.proceed_attack()
        return dbg

    @classmethod
    def movement(cls, profile: str = "aggregate", seed: int = 1234,
                 mtd: str | None = None, mtd_interval: int = 200,
                 geometry: dict | None = None) -> "DESDebugger":
        """The L3 movement-layer attacker walking the class net."""
        from mtdsim.l3_simulation.controller import (
            load_controller, load_outcome_overlay, verdict_for,
        )
        from mtdsim.l3_simulation.movement.attacker import (
            MovementAttacker, load_dwell_catalogue,
        )
        from mtdsim.l3_simulation.movement.net import load_routing_net

        env, end_event, network, adversary, attack_op = cls._build(seed, geometry)
        dbg = cls(env=env, end_event=end_event, network=network,
                  adversary=adversary, attack_op=attack_op)
        dbg._instrument()
        attacker = MovementAttacker(
            env=env, end_event=end_event, adversary=adversary,
            attack_operation=attack_op,
            routing_net=load_routing_net(profile, with_synthetic_overlay=True),
            controller=load_controller(), overlay=load_outcome_overlay(),
            verdict_of=verdict_for, dwell_catalogue=load_dwell_catalogue(),
            seed=seed, register_for_interrupts=True,
        )
        attacker.start()
        if mtd:
            from mtdnetwork.operation.mtd_operation import MTDOperation
            from mtdnetwork.statistic.security_metric_statistics import (
                SecurityMetricStatistics,
            )
            MTDOperation(
                security_metrics_record=SecurityMetricStatistics(), env=env,
                end_event=end_event, network=network, attack_operation=attack_op,
                scheme=mtd, adversary=adversary, proceed_time=0,
                mtd_trigger_interval=mtd_interval,
            ).proceed_mtd()
        return dbg

    # -- instrumentation (read-only; never alters behaviour) ----------------
    def _instrument(self) -> None:
        """Label events with what the simulator is doing, by wrapping the substrate
        seams. Every wrapper delegates unchanged and only appends a note."""
        dbg = self
        AO = AttackOperation

        def wrap_core(name: str, label: str):
            orig = getattr(AO, name)

            def wrapped(self_ao, *a, **kw):
                host = self_ao.adversary.get_curr_host_id()
                result = orig(self_ao, *a, **kw)
                dbg._pending_notes.append(f"{label}(host={host}) -> {result}")
                return result

            setattr(AO, name, wrapped)
            dbg._uninstall.append(lambda: setattr(AO, name, orig))

        for core, label in (
            ("_do_scan_host", "SCAN_HOST"), ("_do_enum_host", "ENUM_HOST"),
            ("_do_scan_port", "SCAN_PORT"), ("_do_brute_force", "BRUTE_FORCE"),
            ("_do_scan_neighbors", "SCAN_NEIGHBOR"),
        ):
            wrap_core(core, label)

        # EXPLOIT_VULN's core is a generator — wrap by delegation.
        orig_exploit = AO._do_exploit_vuln

        def wrapped_exploit(self_ao, vulns, driven=False):
            host = self_ao.adversary.get_curr_host_id()
            dbg._pending_notes.append(f"EXPLOIT_VULN(host={host}, vulns={len(vulns)}) start")
            outcome = yield from orig_exploit(self_ao, vulns, driven)
            dbg._pending_notes.append(f"EXPLOIT_VULN(host={host}) -> {outcome}")
            return outcome

        AO._do_exploit_vuln = wrapped_exploit
        self._uninstall.append(lambda: setattr(AO, "_do_exploit_vuln", orig_exploit))

        # The single compromise procedure.
        orig_ucp = AO.update_compromise_progress

        def wrapped_ucp(self_ao, now, proceed_time):
            before = list(self_ao.adversary.get_compromised_hosts())
            result = orig_ucp(self_ao, now, proceed_time)
            after = self_ao.adversary.get_compromised_hosts()
            fresh = [h for h in after if h not in before]
            if fresh:
                dbg._pending_notes.append(f"*** COMPROMISED host {fresh} (total {len(after)})")
            return result

        AO.update_compromise_progress = wrapped_ucp
        self._uninstall.append(lambda: setattr(AO, "update_compromise_progress", orig_ucp))

        # MTD interrupt cost (shared by both arms).
        orig_cost = AO.apply_mtd_interrupt_cost

        def wrapped_cost(self_ao, mtd):
            rtype = mtd.get_resource_type() if mtd is not None else "?"
            t0 = self_ao.env.now
            dbg._pending_notes.append(f"!!! MTD INTERRUPT ({rtype}) — paying confusion penalty")
            yield from orig_cost(self_ao, mtd)
            dbg._pending_notes.append(
                f"    penalty served {self_ao.env.now - t0:.3f} t/u; "
                f"cursor={'cleared' if self_ao.adversary.get_curr_host() is None else 'kept'}"
            )

        AO.apply_mtd_interrupt_cost = wrapped_cost
        self._uninstall.append(lambda: setattr(AO, "apply_mtd_interrupt_cost", orig_cost))

    def close(self) -> None:
        for undo in reversed(self._uninstall):
            undo()
        self._uninstall.clear()

    # -- the debugger surface ----------------------------------------------
    def _sample(self, note: str) -> WorldState:
        adv = self.adversary
        counter = adv.get_attack_counter()
        return WorldState(
            step_index=self._step_index,
            now=float(self.env.now),
            note=note,
            curr_process=adv.get_curr_process(),
            curr_host_id=adv.get_curr_host_id(),
            host_stack=len(adv.get_host_stack()),
            curr_ports=len(adv.get_curr_ports()),
            compromised_count=len(adv.get_compromised_hosts()),
            given_up=len(adv.get_stop_attack()),
            max_attempt=max(counter) if counter else 0,
            queued_events=len(self.env._queue),
        )

    def step(self) -> WorldState | None:
        """Advance exactly one scheduled event. None when the queue is empty."""
        if not self.env._queue:
            return None
        self._pending_notes.clear()
        self.env.step()
        self._step_index += 1
        state = self._sample("; ".join(self._pending_notes))
        self.trace.append(state)
        return state

    def run_until(self, predicate: Callable[[WorldState], bool] | None = None,
                  horizon: float = 15_000.0, max_steps: int = 2_000_000) -> WorldState | None:
        """Step until `predicate` holds (a breakpoint), the horizon, or the queue drains.

        Returns the state that tripped the breakpoint, else None.
        """
        steps = 0
        while steps < max_steps:
            if not self.env._queue or self.env.peek() > horizon:
                return None
            state = self.step()
            steps += 1
            if state is None:
                return None
            if predicate is not None and predicate(state):
                return state
        return None

    def format_trace(self, last: int | None = None, only_noted: bool = False) -> str:
        rows = [s for s in self.trace if (s.note or not only_noted)]
        if last is not None:
            rows = rows[-last:]
        header = (
            "  step        sim-time  phase          host  stack ports  owned "
            "gaveUp maxAtt   q   what happened"
        )
        return "\n".join([header, "-" * len(header)] + [s.line() for s in rows])


# --- breakpoint helpers -----------------------------------------------------
BREAKPOINTS: dict[str, Callable[[WorldState], bool]] = {
    "compromise": lambda w: "COMPROMISED" in w.note,
    "interrupt": lambda w: "MTD INTERRUPT" in w.note,
    "giveup": lambda w: w.given_up > 0,
    "exploit": lambda w: "EXPLOIT_VULN" in w.note,
    "never": lambda w: False,
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--arm", choices=("native", "movement"), default="native")
    ap.add_argument("--profile", default="aggregate", help="movement arm only")
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--mtd", default=None, help="MTD scheme, e.g. simultaneous / random")
    ap.add_argument("--mtd-interval", type=int, default=200)
    ap.add_argument("--until", type=float, default=1000.0, help="sim-time horizon")
    ap.add_argument("--break-on", choices=sorted(BREAKPOINTS), default="never")
    ap.add_argument("--steps-after-break", type=int, default=0,
                    help="continue this many events past the breakpoint")
    ap.add_argument("--only-noted", action="store_true",
                    help="print only events where something identifiable happened")
    ap.add_argument("--last", type=int, default=None, help="print only the last N rows")
    args = ap.parse_args(argv)

    if args.arm == "native":
        dbg = DESDebugger.native(seed=args.seed, mtd=args.mtd,
                                 mtd_interval=args.mtd_interval)
    else:
        dbg = DESDebugger.movement(profile=args.profile, seed=args.seed,
                                   mtd=args.mtd, mtd_interval=args.mtd_interval)

    try:
        hit = dbg.run_until(BREAKPOINTS[args.break_on], horizon=args.until)
        for _ in range(args.steps_after_break):
            if dbg.step() is None:
                break
        print(dbg.format_trace(last=args.last, only_noted=args.only_noted))
        print()
        if hit is not None:
            print(f"breakpoint '{args.break_on}' hit at step {hit.step_index}, "
                  f"t={hit.now:.3f}: {hit.note}")
        else:
            print(f"ran to horizon t={args.until} without hitting '{args.break_on}'")
        print(f"events stepped: {dbg._step_index}   "
              f"compromised: {len(dbg.adversary.get_compromised_hosts())}   "
              f"given up: {len(dbg.adversary.get_stop_attack())}   "
              f"objective reached: {dbg.end_event.triggered}")
    finally:
        dbg.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
