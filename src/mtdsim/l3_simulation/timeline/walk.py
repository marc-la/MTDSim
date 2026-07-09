"""The seeded single-token walk — the core of the standalone timeline runner.

Executes D2's v1 model: the Petri net runs **independently** of the simulator.
A single token starts in the entry place, consumes the current tactic's
catalogue dwell, then fires one out-transition chosen by the routing policy,
repeating until an objective condition, a stall, or the step cap. The output
is a timed attacker-state sequence (a cumulative timeline) — the artefact the
replay attacker binds to.

Inputs are the **committed JSONs only**: ``data/ogasp/<profile>_structural.json``
(shape + W-A weights) and ``data/ogasp/tactic_durations.json`` (per-state
dwell). The runner never re-derives the nets and never fires a transition that
is not in them (the no-synthesis invariant, tested), and it never imports
``mtdnetwork`` — the coupling to MTDSim is the replay attacker's job.

Determinism: the walk's only randomness is routing — dwells are deterministic
per duration variant — so (seed, profile, entry, policy, weight variant,
duration variant) fixes the timeline byte-for-byte (SIM-05 discipline
extended to the runner).

Naming discipline (metrics_semantics.md §(a)/(d)): the time statistic a
timeline yields is the **net time-to-objective** — an envelope statistic over
one instantiation of a class envelope. It is not, and must never be labelled,
the DES MTTC.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path

# Deliberately re-derived rather than imported from
# ``mtdsim.l3_simulation.petri.render``: importing through the petri package
# pulls in the SNAKES build machinery, and the runner's contract is to be
# plain Python over the committed JSONs.
_REPO_ROOT = Path(__file__).resolve().parents[4]
OGASP_DIR = _REPO_ROOT / "data" / "ogasp"

SCHEMA_VERSION = "ogasp-timeline/v1"

CLASS_NAMES = (
    "pure_steal",
    "pure_impediment",
    "double_extortion",
    "infrastructure_setup",
)
AGGREGATE = "aggregate"
PROFILE_NAMES = (*CLASS_NAMES, AGGREGATE)

POLICIES = ("weighted", "uniform")
WEIGHT_VARIANTS = ("operator_dedup", "raw")
PRIMARY_WEIGHT_VARIANT = "operator_dedup"
DURATION_VARIANTS = ("central", "sweep_low", "sweep_high")

# Declared step cap: maximum states entered per walk. Generous relative to the
# nets' diameter (the longest committed entry→objective simple path is 15
# places), so a capped run signals genuine wandering, not a tight budget.
# Bounds every walk — the only zero-dwell place (resource-development) cannot
# sustain an unbounded zero-time loop because steps, not time, are capped.
MAX_STEPS = 128

# Objective termination rule per profile — a *visited-set* condition, never a
# marking condition (a single token occupies one place, so multi-objective
# classes like double_extortion can never "hold" both at once):
#   - the four class nets require ALL of their declared objective tactics
#     visited (for the three singleton classes this reduces to first visit;
#     for double_extortion it is the class-semantic "both achieved");
#   - the aggregate terminates on ANY of its declared union set — the null
#     envelope has no single operational objective (data/ogasp/README.md), so
#     achieving *an* objective ends the walk; ``completed_objectives`` records
#     which. A recorded choice.
OBJECTIVE_RULES = {profile: "all" for profile in CLASS_NAMES}
OBJECTIVE_RULES[AGGREGATE] = "any"


@dataclass(frozen=True)
class Transition:
    """One committed inter-tactic transition with its W-A weight layer."""

    name: str
    src: str
    dst: str
    weights: dict  # variant -> {weight, backing_flow_ids, ...}


@dataclass(frozen=True)
class Net:
    """A committed weighted net, loaded read-only for walking."""

    profile: str
    places: tuple[str, ...]
    transitions: tuple[Transition, ...]
    out: dict  # place -> tuple[Transition, ...] in committed file order
    objective_tactics: tuple[str, ...]
    objective_rule: str  # "all" | "any"
    recon_bridged: bool


def load_net(profile: str, ogasp_dir: Path = OGASP_DIR) -> Net:
    """Load ``<profile>_structural.json`` into a walkable read-only view."""
    with open(Path(ogasp_dir) / f"{profile}_structural.json") as f:
        data = json.load(f)
    transitions = tuple(
        Transition(
            name=t["name"],
            src=t["src_tactic"],
            dst=t["dst_tactic"],
            weights=t["weights"],
        )
        for t in data["transitions"]
    )
    out: dict[str, list[Transition]] = {}
    for t in transitions:
        out.setdefault(t.src, []).append(t)
    report = data["report"]
    return Net(
        profile=profile,
        places=tuple(data["places"]),
        transitions=transitions,
        out={p: tuple(ts) for p, ts in out.items()},
        objective_tactics=tuple(report["objective_tactics"]),
        objective_rule=OBJECTIVE_RULES[profile],
        recon_bridged=report["prefix_gap"]["recon_reaches_initial_access"],
    )


def load_catalogue(ogasp_dir: Path = OGASP_DIR) -> dict:
    with open(Path(ogasp_dir) / "tactic_durations.json") as f:
        return json.load(f)


def dwell_table(catalogue: dict, duration_variant: str) -> dict:
    """Per-tactic dwell (simulated seconds) for one duration variant.

    ``central`` reads ``duration_s`` verbatim. The sweep extremes follow the
    catalogue's sweep arithmetic (``meta.sweep_range_units``): ``sweep_range``
    is a band on ``relative_multiplier`` **in group-anchor units**, so the
    extreme dwell is ``anchors[group].duration_s × sweep_bound`` — never
    ``duration_s × sweep_bound``. (Execution: central ×0.5 → 22.5 s; sweep
    [0.1, 2.0] → extremes 4.5 s and 90 s.) ``resource-development`` stays 0 s
    in every variant (degenerate sweep [0, 0]); the token still traverses the
    place visibly — its zero-dwell state appears in the sequence — so no
    nominal transit duration is added (a recorded runner decision against its
    profile's §5 licence).
    """
    if duration_variant not in DURATION_VARIANTS:
        raise ValueError(f"unknown duration variant: {duration_variant}")
    dwells = {}
    for tactic, entry in catalogue["tactics"].items():
        if duration_variant == "central":
            dwells[tactic] = float(entry["duration_s"])
        else:
            anchor_s = float(catalogue["anchors"][entry["anchor"]]["duration_s"])
            bound = entry["sweep_range"][0 if duration_variant == "sweep_low" else 1]
            dwells[tactic] = anchor_s * float(bound)
    return dwells


def _objective_met(visited: set, net: Net) -> bool:
    objectives = set(net.objective_tactics)
    if net.objective_rule == "any":
        return bool(visited & objectives)
    return objectives <= visited


def walk(
    net: Net,
    dwells: dict,
    entry: str,
    policy: str,
    weight_variant: str | None,
    duration_variant: str,
    seed: int,
    run_id: str,
    max_steps: int = MAX_STEPS,
) -> dict:
    """One seeded single-token walk → one timeline record (the v1 artefact).

    ``policy="weighted"`` samples the current place's out-distribution under
    ``weight_variant`` (only weight > 0 transitions are fireable — the W-A
    layer is the routing distribution); ``policy="uniform"`` is the structural
    floor — uniform over *all* committed out-transitions, weights unread
    (``weight_variant`` must be None; ``backing_flow_ids`` then report the
    primary variant's provenance and may be empty for weight-unsupported
    transitions — thinness left visible).

    Outcomes: ``objective`` (visited set satisfies the profile's rule),
    ``stalled`` (no fireable out-transition — a legitimate, recorded envelope
    outcome, not an error), or ``cap`` (``max_steps`` states entered).
    """
    if policy == "weighted":
        if weight_variant not in WEIGHT_VARIANTS:
            raise ValueError(f"weighted policy needs a weight variant, got {weight_variant}")
    elif policy == "uniform":
        if weight_variant is not None:
            raise ValueError("uniform policy reads no weights; weight_variant must be None")
    else:
        raise ValueError(f"unknown policy: {policy}")
    if entry not in net.places:
        raise ValueError(f"entry {entry!r} is not a place of {net.profile}")

    provenance_variant = weight_variant or PRIMARY_WEIGHT_VARIANT
    rng = random.Random(seed)
    objectives = set(net.objective_tactics)

    t = 0.0
    visited: set[str] = set()
    first_visit: dict[str, float] = {}
    sequence: list[dict] = []
    place = entry
    fired: Transition | None = None
    outcome = None
    stall_reason = None
    time_to_objective = None

    while True:
        dwell = dwells[place]
        t_enter = t
        t = t_enter + dwell
        visited.add(place)
        if place in objectives and place not in first_visit:
            first_visit[place] = t
        sequence.append(
            {
                "tactic": place,
                "t_enter_s": t_enter,
                "dwell_s": dwell,
                "t_exit_s": t,
                "transition_fired": fired.name if fired else None,
                "backing_flow_ids": (
                    list(fired.weights[provenance_variant]["backing_flow_ids"])
                    if fired
                    else []
                ),
            }
        )
        if _objective_met(visited, net):
            outcome = "objective"
            time_to_objective = t
            break
        if len(sequence) >= max_steps:
            outcome = "cap"
            break
        structural = net.out.get(place, ())
        if policy == "weighted":
            # weight is null where the variant has no flow-backed
            # out-distribution at the source place — unsupported, like 0.
            candidates = [
                (tr, tr.weights[weight_variant]["weight"])
                for tr in structural
                if (tr.weights[weight_variant]["weight"] or 0) > 0
            ]
            if not candidates:
                outcome = "stalled"
                stall_reason = (
                    "no_weight_supported_out_transitions"
                    if structural
                    else "no_structural_out_transitions"
                )
                break
            total = sum(w for _, w in candidates)
            pick = rng.random() * total
            acc = 0.0
            fired = candidates[-1][0]
            for tr, w in candidates:
                acc += w
                if pick < acc:
                    fired = tr
                    break
        else:
            if not structural:
                outcome = "stalled"
                stall_reason = "no_structural_out_transitions"
                break
            fired = structural[rng.randrange(len(structural))]
        place = fired.dst

    return {
        "schema": SCHEMA_VERSION,
        "run_id": run_id,
        "seed": seed,
        "profile": net.profile,
        "entry": entry,
        "policy": policy,
        "weight_variant": weight_variant,
        "duration_variant": duration_variant,
        "objective_rule": net.objective_rule,
        "objective_tactics": list(net.objective_tactics),
        "outcome": outcome,
        "stall_reason": stall_reason,
        "completed_objectives": sorted(visited & objectives),
        "objective_first_visit_s": first_visit,
        "net_time_to_objective_s": time_to_objective,
        "n_states": len(sequence),
        "total_duration_s": t,
        "sequence": sequence,
    }


def serialise(record: dict) -> str:
    """One JSONL line per run — compact, key order fixed by construction."""
    return json.dumps(record, separators=(",", ":"), ensure_ascii=False)


__all__ = [
    "AGGREGATE",
    "CLASS_NAMES",
    "DURATION_VARIANTS",
    "MAX_STEPS",
    "OBJECTIVE_RULES",
    "OGASP_DIR",
    "PROFILE_NAMES",
    "POLICIES",
    "PRIMARY_WEIGHT_VARIANT",
    "SCHEMA_VERSION",
    "WEIGHT_VARIANTS",
    "Net",
    "Transition",
    "dwell_table",
    "load_catalogue",
    "load_net",
    "serialise",
    "walk",
]
