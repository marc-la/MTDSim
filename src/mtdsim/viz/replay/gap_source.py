"""Canonical GAP source for the replay visualiser.

Phase 3 of the refactor stops requiring ``--gap-html`` by loading a
committed ``GeneralisedAttackProfile`` JSON snapshot and rendering the
viewer HTML in-memory. The snapshot lives at ``data/gap/gap_v0.4_latest.json``
in the repo; regenerate by re-running the GAP build notebook and copying
the output.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Optional

from mtdsim.attacker.gap.schema import GeneralisedAttackProfile
from mtdsim.attacker.gap.viz.renderer import MITRETechniqueDependencyVisualiser


# Repo root is parents[4] from this file: replay/ -> viz/ -> mtdsim/ -> src/ -> repo/
_REPO_ROOT = Path(__file__).resolve().parents[4]
_DEFAULT_SNAPSHOT = _REPO_ROOT / "data" / "gap" / "gap_v0.4_latest.json"


def resolve_gap_json(override: Optional[Path] = None) -> Path:
    if override is not None:
        return override
    return _DEFAULT_SNAPSHOT


@lru_cache(maxsize=1)
def _load_cached(path_str: str) -> GeneralisedAttackProfile:
    with open(path_str) as f:
        return GeneralisedAttackProfile.from_dict(json.load(f))


def load_gap(path: Optional[Path] = None) -> GeneralisedAttackProfile:
    """Load the canonical GAP. Cached so repeated calls are free."""
    resolved = resolve_gap_json(path)
    return _load_cached(str(resolved))


def render_gap_html(gap: GeneralisedAttackProfile) -> str:
    """Render the Cytoscape viewer HTML for an in-memory GAP."""
    return MITRETechniqueDependencyVisualiser(gap).render_to_string()
