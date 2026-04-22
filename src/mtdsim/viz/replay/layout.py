"""Cached network layout helper.

Computes ``networkx.spring_layout`` once per (nodes, edges, seed) and caches
to ``data/viz_cache/layout_{hash}.json``. Keyed on the canonical hash so a
fresh sim run with the same topology reuses the existing layout — first run
slow, the rest instant, per §5.1 and the risks table in §10.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable


DEFAULT_CACHE_DIR = Path("data/viz_cache")
DEFAULT_SEED = 0


def layout_key(nodes: Iterable[int], edges: Iterable[Iterable[int]], seed: int) -> str:
    """Stable hash of (nodes, edges, seed). Edges are treated as unordered."""
    canonical_nodes = sorted(int(n) for n in nodes)
    canonical_edges = sorted(tuple(sorted(int(x) for x in e)) for e in edges)
    payload = json.dumps(
        {"nodes": canonical_nodes, "edges": canonical_edges, "seed": int(seed)},
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha1(payload).hexdigest()[:16]


def compute_layout(
    nodes: list[int],
    edges: list[tuple[int, int]],
    *,
    seed: int = DEFAULT_SEED,
    cache_dir: Path | None = DEFAULT_CACHE_DIR,
) -> dict[int, tuple[float, float]]:
    key = layout_key(nodes, edges, seed)
    cache_file: Path | None = None
    if cache_dir is not None:
        cache_file = cache_dir / f"layout_{key}.json"
        if cache_file.exists():
            raw = json.loads(cache_file.read_text())
            return {int(k): (float(v[0]), float(v[1])) for k, v in raw.items()}

    import networkx as nx

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    raw = nx.spring_layout(g, seed=seed)
    pos = {int(n): (float(p[0]), float(p[1])) for n, p in raw.items()}

    if cache_file is not None:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({str(k): list(v) for k, v in pos.items()}))

    return pos
