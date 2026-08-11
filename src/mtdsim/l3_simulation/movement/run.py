"""Run wiring for the movement-layer attacker — select it *alongside* the native.

Builds one MTDSim simulation (env / network / adversary / carved
``AttackOperation``, optional ``MTDOperation``) and drives it with the
:class:`~mtdsim.l3_simulation.movement.attacker.MovementAttacker` **instead of** the
native ``proceed_attack()`` fire-once kick — per-run selection, no inheritance
(architecture §(f)). The inherited 6-phase attacker is untouched and still selected
by the baseline driver (``baseline/run_baseline.py``); this is the other arm.

The controller library is consumed, not forked: by default the real
``load_controller`` / ``load_outcome_overlay`` and the controller's verdict adapter
are wired in, so the moment the controller-finalisation handoff lands its
``compose`` + verdict adapter this run works unmodified. Until then a caller (e.g. a
test) injects an ``overlay`` and ``verdict_of`` to exercise the loop; calling the
default wiring surfaces a clear pointer to the blocking handoff rather than a bare
``NotImplementedError`` deep in a run.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np
import simpy

from mtdnetwork.component.adversary import Adversary
from mtdnetwork.component.time_network import TimeNetwork
from mtdnetwork.data.constants import ATTACKER_THRESHOLD
from mtdnetwork.operation.attack_operation import AttackOperation

from mtdsim.l3_simulation.controller import load_controller
from mtdsim.l3_simulation.movement.attacker import (
    MovementAttacker,
    OutcomeOverlayLike,
    VerdictAdapter,
    load_dwell_catalogue,
)
from mtdsim.l3_simulation.movement.state import (
    AttackerState,
    ModulatedOverlay,
    StatefulAttackOperation,
    StatefulTiming,
)
from mtdsim.l3_simulation.movement.timing import TacticTiming, TimingSource
from mtdsim.l3_simulation.movement.net import load_routing_net, uniform_weight_variant
from mtdsim.l3_simulation.movement.statistics import (
    MovementRunResult,
    MTDDecision,
    MTDExecution,
)

# Phase-0 default geometry (50/5/8/4), matching baseline/run_baseline.py and the
# carve tests. (10/4/4 trips Finding F-06's gen_graph loop guard.)
GEOMETRY = dict(
    total_nodes=50,
    total_endpoints=5,
    total_subnets=8,
    total_layers=4,
    target_layer=4,
    total_database=2,
    terminate_compromise_ratio=0.8,
)

# MTD scenarios, mirroring baseline/run_baseline.py's SCENARIOS shape.
_BLOCKED_HANDOFF = "docs/handoffs/2026-07-22_l3_controller_success_failure.md"


def _default_overlay(version: str | None = None) -> OutcomeOverlayLike:
    """The success/failure outcome overlay from the controller sublayer, at the
    named registry version (or the registry's declared default when unnamed)."""
    from mtdsim.l3_simulation.controller import load_outcome_overlay

    return load_outcome_overlay(version=version)


def _default_verdict_adapter() -> VerdictAdapter:
    """The controller's verdict adapter (controller.md §4). Owned by the
    controller-finalisation handoff; imported by its expected name so this run
    wires it automatically once it lands."""
    try:
        from mtdsim.l3_simulation.controller import verdict_for  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised once the handoff lands
        raise NotImplementedError(
            "the controller verdict adapter (verdict_for) is not available yet; "
            f"it is delivered by {_BLOCKED_HANDOFF}. Until then, inject a "
            "verdict_of callable into run_movement()."
        ) from exc
    return verdict_for


def _build_sim(seed: int, geometry: dict | None):
    random.seed(seed)
    np.random.seed(seed)
    env = simpy.Environment()
    end_event = env.event()
    network = TimeNetwork(**(geometry or GEOMETRY))
    adversary = Adversary(network=network, attack_threshold=ATTACKER_THRESHOLD)
    attack_op = AttackOperation(
        env=env, end_event=end_event, adversary=adversary, proceed_time=0
    )
    return env, end_event, network, adversary, attack_op


@dataclass(frozen=True)
class MTDAIConfig:
    """The declared parameters for running the reactive `mtd_ai` defender.

    Grouped rather than spread across ``run_movement``'s signature because they
    travel together and because every one of them is a *declared* value that a
    study has to state: an agent, the exploration rate it is consulted at, the
    detection rate it reads the attacker's verb through, the idle period after
    which the substrate forces a mutation regardless, and the window the
    downtime feature is read over.

    ``epsilon`` defaults to **0.0 — strictly greedy**, which is the opposite of
    the inherited harness's default and is deliberate. Tay's runner never
    overrode ``execute_ai_model``'s ``epsilon=1.0``, so no published figure ever
    consulted the network; a movement run that wants to know what the *policy*
    does has to ask the policy. Raise it only to characterise a floor.

    ``features`` and ``strategies`` default to the canonical head and action
    space owned by ``mtdnetwork.mtdai.mtd_ai``, so a run cannot accidentally
    show the agent a different state, or re-point its action indices at a
    different set of mechanisms, than the one it was trained against.
    """

    main_network: Any
    epsilon: float = 0.0
    attacker_sensitivity: float = 1.0
    static_degrade_factor: float = 2000.0
    downtime_window: float = 200.0
    features: dict | None = None
    strategies: list | None = None


def _start_mtd_ai(
    *,
    env,
    end_event,
    network,
    adversary,
    attack_op,
    mtd_interval: int | None,
    config: MTDAIConfig,
):
    """Start the reactive defender against this run's attacker.

    The movement attacker needs no adaptation to be legible to it. The agent
    reads its state from the substrate's own attack record and from
    ``adversary.get_curr_process()``, and the movement attacker drives the same
    verb cores the inherited one does — so the rows that feed
    ``host_compromise_ratio``, the ASR denominator and the MTTC mean are written
    by the same call sites either way, and ``attack_type`` reports the verb the
    walk is currently running.

    One asymmetry is worth knowing rather than discovering. The movement
    attacker spends part of every run *dwelling*, and ``DWELL`` is not in the
    defender's ``attack_dict``, so it reads as 7 — the same "no information"
    value the sensitivity draw produces on a miss. Dwell is therefore
    indistinguishable, on that one feature, from an attacker the defender
    failed to detect. That is a property of the inherited encoding, not
    something this wiring introduces, and it is not repaired here.

    The defender is given the **bare** attack operation, never the state-seam
    proxy: nothing on the defence's own path should read through an attacker's
    wrapper.
    """
    from mtdnetwork.mtdai.mtd_ai import CANONICAL_FEATURES, mtd_action_space
    from mtdnetwork.operation.mtd_ai_operation import MTDAIOperation
    from mtdnetwork.statistic.security_metric_statistics import (
        SecurityMetricStatistics,
    )

    if config.main_network is None:
        raise ValueError(
            "mtd_scheme='mtd_ai' needs a trained agent: pass "
            "MTDAIConfig(main_network=...). Build one with tools/mtd_ai_run.py."
        )

    operation = MTDAIOperation(
        features=config.features if config.features is not None else CANONICAL_FEATURES,
        security_metrics_record=SecurityMetricStatistics(),
        env=env,
        end_event=end_event,
        network=network,
        attack_operation=attack_op,
        scheme="mtd_ai",
        adversary=adversary,
        proceed_time=0,
        mtd_trigger_interval=mtd_interval,
        custom_strategies=(
            config.strategies if config.strategies is not None else mtd_action_space()
        ),
        main_network=config.main_network,
        attacker_sensitivity=config.attacker_sensitivity,
        epsilon=config.epsilon,
        static_degrade_factor=config.static_degrade_factor,
        downtime_window=config.downtime_window,
    )
    operation.proceed_mtd()
    return operation


def _maybe_start_mtd(
    *,
    env,
    end_event,
    network,
    adversary,
    attack_op,
    scheme: str | None,
    mtd_interval: int | None,
    custom_strategies,
    mtd_ai: MTDAIConfig | None = None,
):
    if scheme is None or scheme == "None":
        return None
    if scheme == "mtd_ai":
        if mtd_ai is None:
            raise ValueError(
                "mtd_scheme='mtd_ai' needs an MTDAIConfig — pass mtd_ai=..."
            )
        return _start_mtd_ai(
            env=env,
            end_event=end_event,
            network=network,
            adversary=adversary,
            attack_op=attack_op,
            mtd_interval=mtd_interval,
            config=mtd_ai,
        )
    if mtd_ai is not None:
        raise ValueError(
            f"mtd_ai config passed with scheme={scheme!r}; it applies to "
            "mtd_scheme='mtd_ai' only"
        )
    from mtdnetwork.operation.mtd_operation import MTDOperation
    from mtdnetwork.statistic.security_metric_statistics import (
        SecurityMetricStatistics,
    )

    mtd_operation = MTDOperation(
        security_metrics_record=SecurityMetricStatistics(),
        env=env,
        end_event=end_event,
        network=network,
        scheme=scheme,
        attack_operation=attack_op,
        proceed_time=0,
        mtd_trigger_interval=mtd_interval,
        custom_strategies=custom_strategies,
        adversary=adversary,
    )
    mtd_operation.proceed_mtd()
    return mtd_operation


def run_movement(
    profile: str,
    *,
    seed: int = 0,
    with_synthetic_overlay: bool = True,
    horizon: int = 15_000,
    overlay: OutcomeOverlayLike | None = None,
    overlay_version: str | None = None,
    verdict_of: VerdictAdapter | None = None,
    controller: Any | None = None,
    mapping_version: str | None = None,
    dwell_catalogue: dict[str, float] | None = None,
    timing: TimingSource | None = None,
    attacker_state: AttackerState | None = None,
    mtd_scheme: str | None = None,
    mtd_interval: int | None = 200,
    custom_strategies=None,
    mtd_ai: MTDAIConfig | None = None,
    geometry: dict | None = None,
    register_for_interrupts: bool = True,
    max_events: int = 50_000,
    retrace_sinks: bool = False,
    uniform_weights: bool = False,
    exploit_learning_rate: float | None = None,
) -> MovementRunResult:
    """Run one movement-layer simulation and return its :class:`MovementRunResult`.

    ``with_synthetic_overlay`` selects the D8 arm (True: overlay on, seed at
    reconnaissance; False: observed-only, seed at initial-access). ``overlay`` /
    ``verdict_of`` default to the real controller library (see module docstring);
    inject them to drive the loop before the controller finalisation lands.

    ``mapping_version`` names the controller mapping this run uses — the input
    parameter the experiments vary (``"v1_ckc_total"`` is experiment 1's,
    ``"v2_partial"`` is experiment 2's). Left unset it takes the registry's
    default, which is experiment 1's value, so an unqualified run reproduces what
    has always run. This is the seam the choice belongs at: an experiment names
    its mapping, and no layer below here has a preference.

    ``timing`` overrides the per-tactic timing source, which defaults to the
    declared S3 regime (each catalogue duration read as an exponential mean). It
    exists for **verification**, not for configuring an experiment: passing
    ``ConstantTiming`` reproduces the pre-S3 fixed-dwell arm, which is how the
    tests isolate what the distribution change alone did.

    ``overlay_version`` names the success/failure overlay version this run uses,
    the other half of the pair of declared inputs an experiment names at this seam
    — ``mapping_version`` says how tactics become verbs, this says how a verdict
    conditions the next move. It exists so a run can *name* its overlay rather
    than construct one and pass the object, which is the asymmetry the
    demonstration-arms handoff flagged (the tracer had the parameter; this did
    not). Left unset it takes the registry's default, which is experiment 1's
    value for the same reason ``mapping_version``'s is. Passing both this and a
    constructed ``overlay`` is a contradiction and raises.

    ``retrace_sinks`` selects the S5 sink-retrace policy
    (``sink_retrace_design.md``): a token reaching a place the corpus drew no exit
    from steps back to where it came from, with that edge suppressed for one
    selection, instead of the run being censored there. It defaults **off** for the
    same reason ``mapping_version`` and the overlay registry default to experiment
    1's values — an unqualified run reproduces what has always run, and an
    experiment names its own inputs at this seam rather than inheriting a newer
    behaviour silently. Experiment 2 names it; experiment 1's accept-and-censor arm
    stays reachable by leaving it unset.

    ``uniform_weights`` selects the **uniform-weight ablation arm** of the
    plural-preference study (``plural_preference.md``): each place's corpus
    out-distribution is replaced by equiprobable mass over its own reachable
    destination set (:func:`uniform_weight_variant`), so the reachable graph and
    the synthetic-overlay arm are unchanged and only the corpus *preference* is
    stripped. It defaults **off** for the same reason the other arm toggles do —
    an unqualified run is the shipped corpus-weighted model — and it is the null
    against which corpus concentration is the strategic content. Composes with
    ``with_synthetic_overlay`` (the variant is taken of whichever net that
    selects); leave modulators null when reading plurality, per the §4 pin.

    ``exploit_learning_rate`` enables the substrate-level compound-exploit-learning
    mechanism at the given lambda (the per-success odds multiplier). Left ``None``
    the adversary carries no such memory and the run is byte-identical to before;
    ``0.0`` is the exact ablation arm — enabled but silent, bit-identical to
    ``None``. It is orthogonal to ``attacker_state``: this shapes the ``EXPLOIT_VULN``
    success roll on cross-host re-encounter of an already-exploited vulnerability
    *type*, whereas the modulators on ``attacker_state`` shape routing. See
    ``docs/implementation/pipeline/ogasp/exploit_learning.md``.

    ``attacker_state`` attaches a within-run :class:`AttackerState` by wrapping
    the three collaborators the walk consumes — :class:`StatefulTiming` reports
    every place entry, :class:`ModulatedOverlay` reports every verdict and
    multiplies the composed routing by the state's modulator product, and
    :class:`StatefulAttackOperation` reports every MTD interrupt the attacker
    absorbs (the one signal the routing seams cannot see, since an interrupt
    reaches ``compose`` already flattened into a failure verdict). The driver is
    not touched. With no modulators registered the run is bit-identical to
    ``attacker_state=None`` (the null-equivalence guarantee; see
    ``movement/state.py``).
    """
    env, end_event, network, adversary, attack_op = _build_sim(seed, geometry)

    if exploit_learning_rate is not None:
        # Substrate-level compound-exploit-learning (default-off; see
        # docs/implementation/pipeline/ogasp/exploit_learning.md). Left None the
        # adversary is untouched, so the run is byte-identical; rate == 0 is the
        # exact ablation arm (bit-identical to None). Orthogonal to any routing
        # modulator carried on attacker_state — this shapes the EXPLOIT_VULN
        # success roll, not the routing.
        adversary.enable_exploit_learning(exploit_learning_rate)

    routing_net = load_routing_net(profile, with_synthetic_overlay=with_synthetic_overlay)
    if uniform_weights:
        routing_net = uniform_weight_variant(routing_net)
    if controller is None:
        controller = load_controller(version=mapping_version)
    elif mapping_version is not None:
        raise ValueError("pass either controller or mapping_version, not both")
    if overlay is not None and overlay_version is not None:
        raise ValueError("pass either overlay or overlay_version, not both")
    if overlay is None:
        overlay = _default_overlay(overlay_version)
    verdict_of = verdict_of if verdict_of is not None else _default_verdict_adapter()
    dwell = dwell_catalogue if dwell_catalogue is not None else load_dwell_catalogue()
    driven_attack_op: Any = attack_op
    if attacker_state is not None:
        # Attach the state through the three existing seams. The timing default
        # is constructed here (identically to the driver's own default) so it
        # can be wrapped; the RNG discipline is unchanged either way. Only the
        # driver's view of the attack operation is wrapped — the MTD operation
        # below keeps the bare object, so nothing in the defence's own path
        # reads through a proxy.
        if timing is None:
            timing = TacticTiming(dwell, seed=seed)
        timing = StatefulTiming(timing, attacker_state)
        overlay = ModulatedOverlay(overlay, attacker_state)
        driven_attack_op = StatefulAttackOperation(attack_op, attacker_state)

    attacker = MovementAttacker(
        env=env,
        end_event=end_event,
        adversary=adversary,
        attack_operation=driven_attack_op,
        routing_net=routing_net,
        controller=controller,
        overlay=overlay,
        verdict_of=verdict_of,
        dwell_catalogue=dwell,
        timing=timing,
        seed=seed,
        register_for_interrupts=register_for_interrupts,
        max_events=max_events,
        retrace_sinks=retrace_sinks,
    )
    attacker.start()

    mtd_operation = _maybe_start_mtd(
        env=env,
        end_event=end_event,
        network=network,
        adversary=adversary,
        attack_op=attack_op,
        scheme=mtd_scheme,
        mtd_interval=mtd_interval,
        custom_strategies=custom_strategies,
        mtd_ai=mtd_ai,
    )

    env.run(until=horizon)

    records = tuple(attacker.records)
    termination_time = records[-1].end_time if records else float(env.now)
    return MovementRunResult(
        profile=profile,
        seed=seed,
        with_synthetic_overlay=with_synthetic_overlay,
        records=records,
        reached_objective=bool(end_event.triggered),
        termination_time=termination_time,
        compromised_count=len(adversary.get_compromised_hosts()),
        retrace_count=attacker.retrace_count,
        mtd_decisions=decision_snapshot(mtd_operation),
        **mtd_snapshot(network),
    )


def decision_snapshot(mtd_operation) -> tuple[MTDDecision, ...]:
    """The reactive defender's per-decision ledger, or empty under every other
    scheme. Read-only after the run, exactly as :func:`mtd_snapshot` is."""
    if mtd_operation is None or not hasattr(mtd_operation, "get_decision_log"):
        return ()
    return tuple(
        MTDDecision(
            time=float(entry["time"]),
            action=int(entry["action"]),
            source=str(entry["source"]),
        )
        for entry in mtd_operation.get_decision_log()
    )


def mtd_snapshot(network) -> dict:
    """Snapshot the substrate's defender-side statistics into the run-result
    fields — the per-execution record plus the suspended/interrupted tallies.
    Read-only over ``MTDStatistics`` after the run; shared with any runner that
    wires the substrate inline (the baseline arm), so both arms' defender side
    is read off the identical machinery."""
    stats = network.get_mtd_stats()
    totals = stats.dict()
    return {
        "mtd_executions": tuple(
            MTDExecution(
                name=str(row["name"]),
                start_time=float(row["start_time"]),
                finish_time=float(row["finish_time"]),
                duration=float(row["duration"]),
                layer=str(row["executed_at"]),
            )
            for row in stats.get_record().to_dict("records")
        ),
        "mtd_suspended_count": int(totals["Total suspended MTD"]),
        "mtd_attack_interrupted": int(totals["Total attack interrupted"]),
    }


def run_smoke_matrix(
    profiles: tuple[str, ...],
    seeds: tuple[int, ...],
    *,
    with_synthetic_overlay: bool = True,
    horizon: int = 3_000,
    overlay: OutcomeOverlayLike | None = None,
    overlay_version: str | None = None,
    verdict_of: VerdictAdapter | None = None,
    **kwargs,
) -> list[MovementRunResult]:
    """Run every (profile x seed) cell and collect the results — the smoke matrix
    the numbers handoff consumes, and the validation-gate cell."""
    results: list[MovementRunResult] = []
    for profile in profiles:
        for seed in seeds:
            results.append(
                run_movement(
                    profile,
                    seed=seed,
                    with_synthetic_overlay=with_synthetic_overlay,
                    horizon=horizon,
                    overlay=overlay,
                    verdict_of=verdict_of,
                    **kwargs,
                )
            )
    return results


__all__ = [
    "GEOMETRY",
    "MTDAIConfig",
    "decision_snapshot",
    "mtd_snapshot",
    "run_movement",
    "run_smoke_matrix",
]
