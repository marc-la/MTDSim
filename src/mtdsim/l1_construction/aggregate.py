"""Contract per-flow extracts to technique edges, then union across flows (§d).

**Contraction.** Each flow's graph has action / operator / condition nodes.
Operators and conditions are *logic glue*: we walk outward from each technique
action, through any number of operator/condition nodes, until we reach the next
technique action — emitting a single technique->technique edge tagged with the
logic the path passed through:

- ``join`` = the operator nearest the target (``group_id`` namespaced by flow,
  so an AND/OR set is recoverable downstream), or ``None`` for a direct edge.
- ``branch`` = ``true``/``false`` if the path traversed a condition's
  ``on_true``/``on_false`` edge, else ``None``.
- ``edge_type`` = the type of the hop arriving at the target.

Two deliberate properties uphold the §a no-synthesis invariant:

- An action **without** a ``technique_id`` *breaks* the chain (no edge is drawn
  across it — that would invent a dependency the analyst didn't draw).
- A path ending at a condition **sink** (the corpus norm — conditions carry no
  outgoing refs) yields no edge; its text survives only in the per-flow extract.

**Union.** Identical contracted edges are grouped by ``(source, target)``;
``observation_count`` counts *distinct flows* (not occurrences), and every
occurrence is retained with its join/branch context. Cycles are preserved; no
thresholds, no acyclicity — those are views (see :mod:`views`).
"""

from __future__ import annotations

import datetime as _dt
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

from mtdsim.l1_construction.attack_stix import AttackTaxonomy
from mtdsim.l1_construction.schema import (
    DependencyEdge,
    GeneralisedAttackProfile,
    Join,
    Occurrence,
    PerFlowExtract,
    TechniqueNode,
)


@dataclass(frozen=True)
class ContractedEdge:
    """One technique->technique dependency observed in a single flow."""

    source_id: str
    target_id: str
    edge_type: str
    group_id: Optional[str]
    operator: Optional[str]
    branch: Optional[str]
    confidence: Optional[int]


def contract_flow(extract: PerFlowExtract) -> list[ContractedEdge]:
    """Contract one flow's operator/condition glue into technique edges."""
    by_id = extract.node_by_id()

    # adjacency: node id -> [(target node id, edge type)]
    adj: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for e in extract.edges:
        adj[e.source].append((e.target, e.type))

    out: set[ContractedEdge] = set()

    for node in extract.nodes:
        if node.kind != "action" or not node.technique_id:
            continue
        source_tid = node.technique_id
        source_conf = node.confidence

        # DFS through glue. State: (node_id, op_ctx, branch_ctx, last_type, visited)
        stack: list[tuple[str, Optional[tuple[str, str]], Optional[str], str, frozenset[str]]] = []
        for tgt, etype in adj[node.id]:
            stack.append((tgt, None, None, etype, frozenset({node.id})))

        while stack:
            nid, op_ctx, branch_ctx, last_type, visited = stack.pop()
            cur = by_id.get(nid)
            if cur is None or nid in visited:
                continue
            if cur.kind == "action":
                # An action terminates the chain (it is an event, not glue).
                if cur.technique_id and cur.technique_id != source_tid:
                    out.add(ContractedEdge(
                        source_id=source_tid,
                        target_id=cur.technique_id,
                        edge_type=last_type,
                        group_id=(op_ctx[0] if op_ctx else None),
                        operator=(op_ctx[1] if op_ctx else None),
                        branch=branch_ctx,
                        confidence=source_conf,
                    ))
                continue
            nxt_visited = visited | {nid}
            if cur.kind == "operator":
                new_op = (f"{extract.flow_id}:{cur.id}", cur.operator)
                for tgt, etype in adj[nid]:
                    stack.append((tgt, new_op, branch_ctx, etype, nxt_visited))
            elif cur.kind == "condition":
                for tgt, etype in adj[nid]:
                    nb = {"on_true": "true", "on_false": "false"}.get(etype, branch_ctx)
                    stack.append((tgt, op_ctx, nb, etype, nxt_visited))

    return sorted(
        out,
        key=lambda c: (c.source_id, c.target_id, c.group_id or "", c.branch or "", c.edge_type),
    )


def _entry_technique_ids(extract: PerFlowExtract) -> set[str]:
    """Technique ids of actions named in the flow's ``start_refs``."""
    by_id = extract.node_by_id()
    out = set()
    for ref in extract.start_refs:
        n = by_id.get(ref)
        if n and n.kind == "action" and n.technique_id:
            out.add(n.technique_id)
    return out


def aggregate_gap(
    extracts: list[PerFlowExtract],
    attack_meta: dict[str, dict],
    taxonomy: AttackTaxonomy,
    *,
    version: str,
    corpus_ref: str,
    attack_source: str,
    attack_flow_schema_version: str,
) -> GeneralisedAttackProfile:
    """Union contracted flows into the canonical GAP. Deterministic output."""
    # technique presence + structural roles across flows
    node_flows: dict[str, set[str]] = defaultdict(set)
    sub_seen: dict[str, set[str]] = defaultdict(set)
    start_techniques: set[str] = set()

    for ex in extracts:
        for n in ex.nodes:
            if n.kind == "action" and n.technique_id:
                node_flows[n.technique_id].add(ex.flow_id)
                if n.sub_technique_id and n.sub_technique_id != n.technique_id:
                    sub_seen[n.technique_id].add(n.sub_technique_id)
        start_techniques |= _entry_technique_ids(ex)

    # contract + union edges
    edge_acc: dict[tuple[str, str], DependencyEdge] = {}
    seen_occ: dict[tuple[str, str], set[tuple]] = defaultdict(set)
    for ex in extracts:
        for c in contract_flow(ex):
            key = (c.source_id, c.target_id)
            edge = edge_acc.get(key)
            if edge is None:
                edge = DependencyEdge(source_id=c.source_id, target_id=c.target_id)
                edge_acc[key] = edge
            # dedup identical occurrences within the same flow
            sig = (ex.flow_id, c.edge_type, c.group_id, c.operator, c.branch)
            if sig in seen_occ[key]:
                continue
            seen_occ[key].add(sig)
            join = Join(group_id=c.group_id, operator=c.operator) if c.group_id else None
            edge.occurrences.append(Occurrence(
                flow_id=ex.flow_id, edge_type=c.edge_type, join=join, branch=c.branch,
            ))
            if c.confidence is not None:
                edge.confidence_samples.append(c.confidence)

    # Enterprise-only scope (Decision 5 / §a): keep only techniques that resolve
    # in the pinned Enterprise ATT&CK; drop non-Enterprise nodes (ATLAS AML.*,
    # ICS T0###) and revoked/absent ids, plus every edge incident to a dropped
    # node — never bridging across it (that would synthesise an unobserved
    # dependency). The per-flow extracts (§c) stay lossless; scope is applied
    # only here, at aggregation.
    valid = {tid for tid in node_flows if tid in attack_meta}
    edge_acc = {
        key: edge for key, edge in edge_acc.items()
        if key[0] in valid and key[1] in valid
    }

    # in/out degree on the Enterprise-scoped graph (for entry/objective)
    indeg: dict[str, int] = defaultdict(int)
    outdeg: dict[str, int] = defaultdict(int)
    for (s, t) in edge_acc:
        outdeg[s] += 1
        indeg[t] += 1

    # build nodes (Enterprise-scoped set only)
    nodes: dict[str, TechniqueNode] = {}
    for tid in sorted(valid):
        meta = attack_meta.get(tid, {})
        flows = sorted(node_flows[tid])
        nodes[tid] = TechniqueNode(
            technique_id=tid,
            name=meta.get("name", ""),
            tactics=list(meta.get("tactics", [])),
            primary_tactic=meta.get("primary_tactic", ""),
            tactic_layer=meta.get("tactic_layer", -1),
            platforms=list(meta.get("platforms", [])),
            sub_technique_ids=sorted(sub_seen.get(tid, set())),
            flow_count=len(flows),
            flow_ids=flows,
            is_entry=(tid in start_techniques) or (indeg[tid] == 0),
            is_objective=(outdeg[tid] == 0),
        )

    # finalise edges deterministically
    edges: list[DependencyEdge] = []
    for key in sorted(edge_acc):
        edge = edge_acc[key]
        edge.flow_ids = sorted({o.flow_id for o in edge.occurrences})
        edge.observation_count = len(edge.flow_ids)
        edge.occurrences.sort(
            key=lambda o: (o.flow_id, o.join.group_id if o.join else "", o.branch or "", o.edge_type)
        )
        edge.confidence_samples.sort()
        edge.tactic_delta = _tactic_delta(nodes, key[0], key[1])
        edges.append(edge)

    layers: dict[int, list[str]] = defaultdict(list)
    for tid, n in nodes.items():
        layers[n.tactic_layer].append(tid)
    layers = {k: sorted(v) for k, v in sorted(layers.items())}

    return GeneralisedAttackProfile(
        version=version,
        build_date=_dt.date.today().isoformat(),
        attack_flow_schema_version=attack_flow_schema_version,
        corpus_ref=corpus_ref,
        attack_source=attack_source,
        nodes=nodes,
        edges=edges,
        source_flow_count=len(extracts),
        node_count=len(nodes),
        edge_count=len(edges),
        entry_nodes=sorted(t for t, n in nodes.items() if n.is_entry),
        objective_nodes=sorted(t for t, n in nodes.items() if n.is_objective),
        layers=layers,
    )


def _tactic_delta(nodes: dict[str, TechniqueNode], src: str, tgt: str) -> str:
    """Descriptive only — derived from tactic layer; never alters direction."""
    ls = nodes[src].tactic_layer if src in nodes else -1
    lt = nodes[tgt].tactic_layer if tgt in nodes else -1
    if ls < 0 or lt < 0:
        return "intra"
    if lt > ls:
        return "forward"
    if lt < ls:
        return "backward"
    return "intra"
