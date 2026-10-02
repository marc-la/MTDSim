"""The size-matched, label-blind partition control — profile nets from random
groups of attack flows.

Why. The attack graph before partitioning (``aggregate``) differs from the four
attack profiles averaged. Two causes are open: conditioning on objective, and
corpus size (each profile net is built from fewer flows, so it has fewer edges
and paths whatever its objective). The control separates them: the 38 flows are
shuffled into four groups of the profiles' sizes (19 / 7 / 7 / 5) and each group
is compiled and run exactly as a profile is. Random groups that behave like the
profiles point at size; random groups that behave like the aggregate point at
objective.

How. ``build_petri_dir`` takes an assignment ``slot -> flow ids`` and writes a
complete petri directory by the construction the committed nets use, step for
step, reusing every function of that construction:

1. **Structure.** ``OperationalObjectiveSelector.select`` over the group's flows
   (the GASP surface subgraph: the techniques the group's flows hold, and every
   GAP edge between two of them), then ``build_structural_net``.
2. **Weights.** ``compute_all_variants`` over the group's flows: the W-A flow
   proportion, primary variant ``operator_dedup`` under the one global operator
   rule (``mtdsim.l2_subgraph.dedup``, n = 29 over all 38 flows, never re-run per
   group), ``raw`` beside it.
3. **Synthetic overlay.** ``curate_synthetic_overlay`` + ``overlay_payload`` —
   the guard and share rule read each group's own observed net.
4. **Record.** ``persist_summary`` writes ``<slot>_structural.json``;
   ``write_overlay`` writes ``synthetic_overlay.json``.

The four profile names are reused as **slot names** so the runtime runs the
groups unmodified (``run_movement(..., petri_dir=...)``). The runtime reads
nothing else by profile name: the controller mapping, the outcome overlay
(``data/ogasp/controller/overlays/``, all 210 tactic pairs) and the dwell
catalogue are keyed by tactic; the utility modulator, which reads
``OBJECTIVE_TACTICS`` by profile, is off in every chapter 5 run.

Two record-only departures in label-blind mode, both off the runtime path: the
structural report's objective tactics are the declared objective tactics the
group holds (a slot name carries no objective, so the class lookup would test
the wrong set and refuse groups lacking it), and the record carries a
``partition_control`` block naming the group's flows.

Two decisions that do reach the runtime, for Marc's ruling (both recorded in
the manifest):

- **The overlay guard reads the weighted net** (``guard="weighted"``, see
  :data:`GUARDS`). The committed guard reads the structural net; on the five
  committed nets both give the same bytes (tested). On random groups the
  structural guard leaves about a third of groups seeding the token in a
  reconnaissance place with no weighted exit: the run ends at once, no host.
- **Draws are kept only if every group's token can reach initial-access**
  (:func:`token_reaches_initial_access`, which every real profile meets). The
  residual failures are groups with no resource-development place, where the
  overlay's guard never acts. Over the first 60 draws 44 pass (7 under the
  structural guard).

Built with the real partition and ``label_blind=False`` the directory
reproduces the committed ``data/ogasp/petri/`` files byte for byte under
either guard (``tests/l3_simulation/test_partition_control.py``).
``data/ogasp/petri/outcome_overlay.json`` is not rebuilt: no code generates it,
nothing reads it at runtime, and its per-profile pair lists predate the
current nets.

    PYTHONPATH=src python -m mtdsim.l3_simulation.petri.partition_control
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import replace
from pathlib import Path

import numpy as np

from mtdsim.l2_subgraph.dedup import operator_deduplicated_flows
from mtdsim.l2_subgraph.selector import OperationalObjectiveSelector
from mtdsim.l3_simulation.petri.analysis import OBJECTIVE_TACTICS, analyse
from mtdsim.l3_simulation.petri.build import (
    AGGREGATE,
    CLASS_NAMES,
    GAP_PATH,
    build_aggregate_view,
    build_structural_net,
    load_gap_index,
)
from mtdsim.l3_simulation.petri.render import persist_summary
from mtdsim.l3_simulation.petri.synthetic_overlay import (
    curate_synthetic_overlay,
    write_overlay,
)
from mtdsim.l3_simulation.petri.weights import (
    PRIMARY_VARIANT,
    compute_all_variants,
    load_class_flows,
    load_edge_flows,
    weighting_provenance,
)

_REPO_ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = _REPO_ROOT / "data" / "ogasp" / "partition_control"
MANIFEST = OUT_DIR / "partitions.json"

SLOTS: tuple[str, ...] = CLASS_NAMES

# What the synthetic overlay's guard and share rule read. The committed rule
# reads the structural net (every observed transition, weighted or not); the
# runtime walks only the transitions with a positive primary weight. On the
# five committed nets the two agree (the gate builds both and compares bytes).
# On a random group they can differ: a reconnaissance place with structural
# out-edges none of the group's weight-carrying flows backs is, structurally,
# bridged to initial-access (the guard adds nothing) and, to the token, a sink
# it is seeded in (the run cannot start). "weighted" applies the guard's stated
# purpose (a recon-seeded token must be able to reach initial-access) to the
# net the token walks.
GUARDS = {
    "structural": "the committed rule: guard and share read every observed transition",
    "weighted": "guard and share read the transitions with a positive primary weight "
                "(the net the token walks)",
}
PARTITION_SEED = 20261002
K = 10

# The declared objective tactics, any profile (the aggregate's union). In
# label-blind mode a group's report tests the ones it holds.
_ALL_OBJECTIVE_TACTICS = OBJECTIVE_TACTICS[AGGREGATE]


def real_assignment() -> dict[str, tuple[str, ...]]:
    """The real partition, slot -> sorted flow ids, from ``classification.csv``."""
    class_flows = load_class_flows()
    return {slot: tuple(sorted(class_flows[slot])) for slot in SLOTS}


def slot_sizes() -> dict[str, int]:
    """The profiles' sizes, slot -> number of flows (19 / 7 / 7 / 5)."""
    return {slot: len(f) for slot, f in real_assignment().items()}


def partition_stream(seed: int = PARTITION_SEED) -> Iterator[dict[str, tuple[str, ...]]]:
    """Random partitions of the 38 flows into the slots, at the profiles' sizes,
    without end. One generator draws the permutations in turn, so draw i is
    fixed by ``seed`` alone; the flows are sorted before shuffling and the slots
    filled in order."""
    sizes = slot_sizes()
    flows = sorted(f for fs in real_assignment().values() for f in fs)
    rng = np.random.default_rng(seed)
    while True:
        perm = [flows[i] for i in rng.permutation(len(flows))]
        assignment, at = {}, 0
        for slot in SLOTS:
            assignment[slot] = tuple(sorted(perm[at : at + sizes[slot]]))
            at += sizes[slot]
        yield assignment


def random_partitions(
    k: int = K, seed: int = PARTITION_SEED
) -> list[dict[str, tuple[str, ...]]]:
    """The first ``k`` draws of :func:`partition_stream` (no selection)."""
    stream = partition_stream(seed)
    return [next(stream) for _ in range(k)]


def token_reaches_initial_access(petri_dir: Path | str, slot: str) -> bool:
    """The runnability criterion: on the runtime routing net (the observed
    weights composed with the synthetic overlay, as ``load_routing_net`` builds
    it) the token seeded at the entry place can reach ``initial-access`` over
    positive-weight edges. Every real profile meets it (the overlay exists to
    make it so); a group that fails it never leaves the pre-intrusion places,
    and its run ends at once with no host compromised."""
    from mtdsim.l3_simulation.movement.net import load_routing_net

    net = load_routing_net(slot, petri_dir=petri_dir)
    seen, stack = set(), [net.entry_place]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack += [v for v, w in net.base_out_weights(u).items() if w > 0]
    return "initial-access" in seen


def _load_gap(gap_path: Path = GAP_PATH) -> dict:
    with open(gap_path) as f:
        return json.load(f)


def build_petri_dir(
    assignment: Mapping[str, Iterable[str]],
    out_dir: Path | str,
    *,
    include_aggregate: bool = False,
    label_blind: bool = True,
    build_date: str | None = None,
    provenance: dict | None = None,
    guard: str = "structural",
) -> dict[str, dict]:
    """Write a complete petri directory for ``assignment`` (slot -> flow ids) and
    return per-slot structure statistics (see :func:`net_stats`).

    ``include_aggregate`` adds the aggregate net over every GAP flow (needed to
    reproduce the committed overlay record, which lists all five). ``build_date``
    fixes the record's build date (default: today, as the committed build).
    ``label_blind`` selects the two departures in the module docstring;
    ``provenance`` is merged into each record's ``partition_control`` block.

    ``guard`` names the net the synthetic overlay's guard and share rule read:
    ``"structural"`` (the committed rule, every observed transition) or
    ``"weighted"`` (only the transitions with a positive primary weight, the net
    the token walks). See :data:`GUARDS`.
    """
    if guard not in GUARDS:
        raise ValueError(f"guard must be one of {tuple(GUARDS)}, got {guard!r}")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    gap_dict = _load_gap()
    gap = load_gap_index()
    edge_flows = load_edge_flows()
    groups = {slot: frozenset(flows) for slot, flows in assignment.items()}
    unknown = set().union(*groups.values()) - {
        fid for n in gap_dict["nodes"].values() for fid in n["flow_ids"]
    }
    if unknown:
        raise ValueError(f"flows not in the GAP: {sorted(unknown)}")

    views, flow_sets = {}, {}
    for slot, flows in groups.items():
        views[slot] = OperationalObjectiveSelector(slot).select(
            gap_dict, {fid: slot for fid in flows}
        )
        flow_sets[slot] = flows
    if include_aggregate:
        views[AGGREGATE] = build_aggregate_view()
        flow_sets[AGGREGATE] = frozenset().union(*groups.values())

    nets, weights, stats = {}, {}, {}
    for slot, view in views.items():
        snet = build_structural_net(view, gap)
        if build_date is not None:
            snet.provenance["build_date"] = build_date
        objectives = None
        if label_blind and slot != AGGREGATE:
            objectives = tuple(
                o for o in _ALL_OBJECTIVE_TACTICS if o in snet.tactics
            )
        report = analyse(snet, view, gap, objective_tactics=objectives)
        w = compute_all_variants(snet, edge_flows, flow_sets[slot])
        path = persist_summary(
            snet,
            report,
            weights_by_variant=w,
            weighting=weighting_provenance(flow_sets[slot], w),
            out_dir=out_dir,
        )
        if label_blind:
            _add_block(path, {
                "slot": slot,
                "flow_ids": sorted(flow_sets[slot]),
                "objective_tactics": "the declared objective tactics the group "
                "holds (label-blind: the slot name carries no objective)",
                **(provenance or {}),
            })
        nets[slot], weights[slot] = snet, w
        stats[slot] = net_stats(snet, w, flow_sets[slot])

    # The overlay record is a function of each net's observed transitions and
    # its curated synthetic ones; the composed SNAKES net is not part of it.
    # Composing it would refuse a group whose observed net already holds one of
    # the three synthetic pairs (a shape no profile has: SNAKES rejects the
    # duplicate transition name), so the record is built from the curation
    # directly. The guard and share rule are unchanged; at runtime the
    # synthetic share adds onto the observed edge of the same pair
    # (movement/net.py ``_compose_out``), as the merge rule's sum reads.
    joined = {}
    for slot, snet in nets.items():
        read = _guard_net(snet, weights[slot], guard)
        joined[slot] = replace(read, synthetic_transitions=curate_synthetic_overlay(read))
    write_overlay(joined, out_dir / "synthetic_overlay.json")
    for slot, s in joined.items():
        observed = {(t.src_tactic, t.dst_tactic) for t in nets[slot].transitions}
        stats[slot]["synthetic_transitions"] = [t.name for t in s.synthetic_transitions]
        stats[slot]["synthetic_pairs_also_observed"] = [
            t.name for t in s.synthetic_transitions
            if (t.src_tactic, t.dst_tactic) in observed
        ]
        stats[slot]["guard"] = guard
        stats[slot]["overlay_differs_under_structural_guard"] = (
            curate_synthetic_overlay(nets[slot]) != s.synthetic_transitions
        )
    return stats


def _guard_net(snet, weights_by_variant, guard: str):
    """The net the overlay's guard and share rule read (see :data:`GUARDS`)."""
    if guard == "structural":
        return snet
    primary = weights_by_variant[PRIMARY_VARIANT]
    return replace(
        snet, transitions=tuple(t for t in snet.transitions if primary[t.name].weight)
    )


def _add_block(path: Path, block: dict) -> None:
    """Append the ``partition_control`` block to a written record, in the
    record's own format."""
    with open(path) as f:
        doc = json.load(f)
    doc["partition_control"] = block
    with open(path, "w") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")


def net_stats(snet, weights_by_variant, flows: frozenset[str]) -> dict:
    """The structure statistics the control is read against: flows, weight-
    carrying flows (the global operator rule), places, transitions, weight-
    supported transitions (positive primary weight), and the places the token
    cannot leave on primary weights (before the synthetic overlay)."""
    primary = weights_by_variant[PRIMARY_VARIANT]
    supported = [n for n, tw in primary.items() if tw.weight]
    has_out = {n.split("__to__")[0] for n in supported}
    return {
        "flow_ids": sorted(flows),
        "n_flows": len(flows),
        "n_weight_carrying": len(flows & operator_deduplicated_flows()),
        "n_places": len(snet.tactics),
        "n_transitions": len(snet.transitions),
        "n_weight_supported_transitions": len(supported),
        "places_without_weighted_exit": sorted(set(snet.tactics) - has_out),
        "objective_tactics_held": [o for o in _ALL_OBJECTIVE_TACTICS if o in snet.tactics],
        "entry_marking": snet.entry_tactic,
    }


def main() -> int:
    """Draw and build the K partitions under ``data/ogasp/partition_control/``
    and write the manifest: per partition and slot, the flows and the structure
    statistics, beside the same statistics for the real profiles and the
    aggregate (built to a scratch directory, never over ``data/ogasp/petri/``).

    Draws are taken from :func:`partition_stream` in order and a draw is kept
    only if every group meets :func:`token_reaches_initial_access`; rejected
    draws are recorded with the slots that failed. ``GUARD`` (env; default
    ``weighted``) names the overlay guard (:data:`GUARDS`). Over the first 60
    draws, 44 meet the criterion under ``weighted`` and 7 under ``structural``.
    """
    import os
    import shutil
    import tempfile

    guard = os.environ.get("GUARD", "weighted")
    real = real_assignment()
    real_label = {f: slot for slot, fs in real.items() for f in fs}
    with tempfile.TemporaryDirectory() as tmp:
        reference = build_petri_dir(real, tmp, include_aggregate=True, label_blind=False,
                                    guard=guard)
        assert all(token_reaches_initial_access(tmp, s) for s in SLOTS)

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    partitions, rejected = [], []
    for draw, assignment in enumerate(partition_stream()):
        if len(partitions) == K:
            break
        i = len(partitions)
        d = OUT_DIR / f"p{i:02d}"
        stats = build_petri_dir(
            assignment, d, guard=guard,
            provenance={"partition": i, "draw": draw, "partition_seed": PARTITION_SEED,
                        "guard": guard},
        )
        failed = [s for s in SLOTS if not token_reaches_initial_access(d, s)]
        if failed:
            shutil.rmtree(d)
            rejected.append({"draw": draw, "slots_failing": failed,
                             "flow_ids": {s: list(assignment[s]) for s in failed}})
            continue
        kept = sum(real_label[f] == slot for slot, fs in assignment.items() for f in fs)
        partitions.append({
            "partition": i,
            "draw": draw,
            "petri_dir": str(d.relative_to(_REPO_ROOT)),
            "flows_keeping_real_label": kept,
            "groups": stats,
        })
        print(f"  p{i:02d} (draw {draw:>2})  kept-label {kept:>2}/38  " + "  ".join(
            f"{s[:6]}:{v['n_flows']}f/{v['n_weight_carrying']}w/{v['n_places']}p/"
            f"{v['n_weight_supported_transitions']}t" for s, v in stats.items()
        ))
    manifest = {
        "design": "size-matched, label-blind partition control "
                  "(src/mtdsim/l3_simulation/petri/partition_control.py docstring)",
        "partition_seed": PARTITION_SEED,
        "k": K,
        "guard": {"used": guard, "options": GUARDS},
        "slot_sizes": slot_sizes(),
        "rng": "numpy.random.default_rng(partition_seed).permutation over the sorted "
               "38 flow ids, one draw after another; slots filled in order",
        "selection": "a draw is kept only if, in every group, the token seeded at the "
                     "entry place can reach initial-access on the runtime routing net "
                     "(token_reaches_initial_access; every real profile meets it)",
        "draws_taken": len(partitions) + len(rejected),
        "rejected": rejected,
        "expected_flows_keeping_real_label": sum(n * n for n in slot_sizes().values()) / 38,
        "reference": reference,
        "partitions": partitions,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"  rejected draws: {[r['draw'] for r in rejected]}")
    print("  reference  " + "  ".join(
        f"{s[:6]}:{v['n_flows']}f/{v['n_weight_carrying']}w/{v['n_places']}p/"
        f"{v['n_weight_supported_transitions']}t" for s, v in reference.items()
    ))
    print(f"  -> {OUT_DIR.relative_to(_REPO_ROOT)}/")
    return 0


__all__ = [
    "GUARDS",
    "K",
    "OUT_DIR",
    "PARTITION_SEED",
    "SLOTS",
    "build_petri_dir",
    "net_stats",
    "partition_stream",
    "random_partitions",
    "real_assignment",
    "slot_sizes",
    "token_reaches_initial_access",
]


if __name__ == "__main__":
    sys.exit(main())
