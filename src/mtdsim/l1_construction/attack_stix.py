"""Read MITRE ATT&CK Enterprise STIX for **technique node metadata** and the
**tactic taxonomy**.

The GAP's edges come entirely from Attack Flow (§a invariant); ATT&CK is used
*only* to attach human-readable attributes to the technique nodes those edges
connect — canonical name, tactics, platforms, tactic layer — and to supply the
kill-chain ordering used by the layout/ordering views.

Two things are read here:

- :func:`load_attack_taxonomy` — the ordered tactic list + ``TA####`` -> shortname
  map, derived from the bundle's ``x-mitre-matrix`` / ``x-mitre-tactic`` objects.
  Deriving (rather than hardcoding) keeps the build correct across ATT&CK
  releases: e.g. v19.1 splits the classic ``defense-evasion`` into ``stealth`` +
  ``defense-impairment`` (15 tactics), which a hardcoded 14-tactic table would
  mislayer. The hardcoded tables in ``schema.py`` are only standalone fallbacks.
- :func:`load_attack_techniques` — per parent technique: name, tactics,
  primary_tactic, tactic_layer, platforms, sub_technique_ids.

This is the legitimate half of the v0.4 ``stix_parser`` re-derived from scratch.
The v0.4 group/campaign/``uses`` provenance path is deliberately **absent** — it
fed the co-occurrence miner that Decision 1 removes.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

from mtdsim.l1_construction.schema import (
    TACTIC_ID_TO_NAME,
    TACTIC_LAYERS,
    TACTIC_ORDER,
)

BundleOrPath = Union[str, Path, dict]


def _load(bundle_or_path: BundleOrPath) -> dict:
    if isinstance(bundle_or_path, dict):
        return bundle_or_path
    with open(bundle_or_path) as f:
        return json.load(f)


def _external_id(obj: dict) -> str:
    for ref in obj.get("external_references", []):
        if ref.get("source_name") == "mitre-attack":
            return ref.get("external_id", "")
    return ""


@dataclass
class AttackTaxonomy:
    """The pinned ATT&CK version's tactic ordering + id mapping."""

    order: list[str] = field(default_factory=lambda: list(TACTIC_ORDER))
    layers: dict[str, int] = field(default_factory=lambda: dict(TACTIC_LAYERS))
    id_to_name: dict[str, str] = field(default_factory=lambda: dict(TACTIC_ID_TO_NAME))

    def primary(self, tactics: list[str]) -> str:
        """Earliest kill-chain phase present (lowest layer)."""
        ranked = [t for t in tactics if t in self.layers]
        return min(ranked, key=lambda t: self.layers[t]) if ranked else ""


def load_attack_taxonomy(bundle_or_path: BundleOrPath) -> AttackTaxonomy:
    """Derive the tactic order + ``TA####`` -> shortname map from the bundle.

    Falls back to the ``schema.py`` classic-14 defaults if the matrix/tactic
    objects are absent (e.g. a trimmed bundle).
    """
    bundle = _load(bundle_or_path)
    objects = bundle.get("objects", [])

    tactics = {o["id"]: o for o in objects if o.get("type") == "x-mitre-tactic"}
    if not tactics:
        return AttackTaxonomy()

    id_to_name = {
        _external_id(o): o.get("x_mitre_shortname", "")
        for o in tactics.values()
        if _external_id(o) and o.get("x_mitre_shortname")
    }

    matrix = next((o for o in objects if o.get("type") == "x-mitre-matrix"), None)
    if matrix and matrix.get("tactic_refs"):
        order = [
            tactics[r]["x_mitre_shortname"]
            for r in matrix["tactic_refs"]
            if r in tactics and tactics[r].get("x_mitre_shortname")
        ]
    else:  # no matrix: fall back to a stable alphabetical-by-id ordering
        order = [id_to_name[k] for k in sorted(id_to_name)]

    return AttackTaxonomy(
        order=order,
        layers={t: i for i, t in enumerate(order)},
        id_to_name=id_to_name,
    )


def _tactics(obj: dict) -> list[str]:
    return [
        p.get("phase_name", "")
        for p in obj.get("kill_chain_phases", [])
        if p.get("kill_chain_name") == "mitre-attack"
    ]


def load_attack_techniques(
    bundle_or_path: BundleOrPath,
    taxonomy: Optional[AttackTaxonomy] = None,
) -> dict[str, dict]:
    """Return ``{parent_technique_id: {name, tactics, primary_tactic,
    tactic_layer, platforms, sub_technique_ids}}``.

    Sub-techniques are collapsed into their parent; their ids accumulate in
    ``sub_technique_ids``. Revoked / deprecated patterns are skipped.
    """
    bundle = _load(bundle_or_path)
    taxonomy = taxonomy or load_attack_taxonomy(bundle)

    patterns = [
        o for o in bundle.get("objects", [])
        if o.get("type") == "attack-pattern"
        and not o.get("revoked")
        and not o.get("x_mitre_deprecated")
    ]

    out: dict[str, dict] = {}

    def _blank() -> dict:
        return {
            "name": "",
            "tactics": [],
            "primary_tactic": "",
            "tactic_layer": -1,
            "platforms": [],
            "sub_technique_ids": [],
        }

    # Parents first, so sub-technique handling can rely on the parent slot.
    for is_sub in (False, True):
        for ap in patterns:
            raw_tid = _external_id(ap)
            if not raw_tid:
                continue
            sub = "." in raw_tid
            if sub != is_sub:
                continue
            parent = raw_tid.split(".", 1)[0]
            meta = out.setdefault(parent, _blank())
            if not sub:
                tactics = _tactics(ap)
                primary = taxonomy.primary(tactics)
                meta["name"] = ap.get("name", meta["name"])
                meta["tactics"] = tactics
                meta["primary_tactic"] = primary
                meta["tactic_layer"] = taxonomy.layers.get(primary, -1)
                meta["platforms"] = list(ap.get("x_mitre_platforms", []) or [])
            elif raw_tid not in meta["sub_technique_ids"]:
                meta["sub_technique_ids"].append(raw_tid)

    for meta in out.values():
        meta["sub_technique_ids"].sort()
    return out
