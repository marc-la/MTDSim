"""
Enrich GroupProfile stubs with motivation, region, and alias data from
vendored MISP galaxy + ETDA-compatible overrides.

Join strategy (in precedence order):
    1. overrides.yaml         (authoritative — committed manual attribution)
    2. ETDA JSON              (optional, if user drops it in ``data/``)
    3. MISP galaxy threat-actor (MITRE ID via ``meta.refs``, else name/synonym match)

The MISP ``cfr-type-of-incident`` field is mapped to the ETDA 4-category
taxonomy so all UI filtering uses one vocabulary.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

from mtdsim.attacker.gap.schema import GroupProfile, MOTIVATION_CATEGORIES


_DATA_DIR = Path(__file__).parent / "data"
_MITRE_GID_RE = re.compile(r"attack\.mitre\.org/groups/(G\d{4})", re.IGNORECASE)


# MISP "cfr-type-of-incident" -> ETDA motivation category.
_MISP_INCIDENT_TO_ETDA: dict[str, str] = {
    "espionage": "information_theft_espionage",
    "financial theft": "financial_gain",
    "financial crime": "financial_crime",
    "business email compromise": "financial_crime",
    "extortion": "financial_crime",
    "sabotage": "sabotage_destruction",
    "denial of service": "sabotage_destruction",
    "defacement": "sabotage_destruction",
    # "information operations" has no clean ETDA slot — retained as MISP tag only.
}


# ---------------------------------------------------------------------------
# Loaders


def load_misp_actors(path: Optional[Path] = None) -> list[dict]:
    """Return MISP threat-actor entries (empty list if file missing)."""
    p = path or _DATA_DIR / "misp_threat_actor.json"
    if not p.exists():
        return []
    with open(p) as f:
        return json.load(f).get("values", [])


def load_etda_actors(path: Optional[Path] = None) -> list[dict]:
    """Return ETDA threat-group entries; tolerant to absence."""
    p = path or _DATA_DIR / "etda_threat_groups.json"
    if not p.exists():
        return []
    with open(p) as f:
        data = json.load(f)
    return data.get("groups", data) if isinstance(data, dict) else list(data)


def load_overrides(path: Optional[Path] = None) -> dict[str, dict]:
    """Return ``{group_id: {motivations: [...], regions: [...]}}``."""
    p = path or _DATA_DIR / "overrides.yaml"
    if not p.exists():
        return {}
    try:
        import yaml  # lazy import; only required if overrides file exists
    except ImportError:  # pragma: no cover
        return {}
    with open(p) as f:
        data = yaml.safe_load(f) or {}
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------------------
# Join helpers


def _mitre_id_from_misp(entry: dict) -> Optional[str]:
    for ref in entry.get("meta", {}).get("refs", []) or []:
        m = _MITRE_GID_RE.search(ref or "")
        if m:
            return m.group(1).upper()
    return None


def _name_keys(name: str, synonyms: list[str]) -> set[str]:
    keys = {name.strip().lower()}
    for s in synonyms or []:
        if s:
            keys.add(s.strip().lower())
    return keys


def _misp_index_by_mitre(misp_entries: list[dict]) -> dict[str, dict]:
    """Index MISP entries by MITRE group ID when one can be recovered."""
    out: dict[str, dict] = {}
    for entry in misp_entries:
        gid = _mitre_id_from_misp(entry)
        if gid:
            out[gid] = entry
    return out


def _misp_index_by_name(misp_entries: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for entry in misp_entries:
        for key in _name_keys(entry.get("value", ""), entry.get("meta", {}).get("synonyms", [])):
            out.setdefault(key, entry)
    return out


def _misp_motivations(entry: dict) -> tuple[list[str], list[str]]:
    """Return (etda_categories, misp_sublabels) for a MISP entry."""
    meta = entry.get("meta", {}) or {}
    raw = meta.get("cfr-type-of-incident")
    incidents: list[str] = []
    if isinstance(raw, list):
        incidents = [str(x) for x in raw if x]
    elif isinstance(raw, str) and raw:
        incidents = [raw]
    etda: list[str] = []
    misp_tags: list[str] = []
    for inc in incidents:
        misp_tags.append(inc)
        cat = _MISP_INCIDENT_TO_ETDA.get(inc.strip().lower())
        if cat and cat not in etda:
            etda.append(cat)
    # MISP has a free-text "motive" on some entries — surface it too.
    motive = meta.get("motive")
    if motive:
        for m in (motive if isinstance(motive, list) else [motive]):
            if m and m not in misp_tags:
                misp_tags.append(str(m))
    return etda, misp_tags


# ---------------------------------------------------------------------------
# Main entry point


def enrich_group_profiles(
    profiles: dict[str, GroupProfile],
    data_dir: Optional[Path] = None,
) -> dict[str, GroupProfile]:
    """
    Mutate and return ``profiles`` with motivation/region/source data filled.

    Unmatched groups keep ``motivations == []`` and ``sources == ["mitre"]``
    so the UI can show an "unattributed" bucket distinctly.
    """
    data_dir = data_dir or _DATA_DIR

    overrides = load_overrides(data_dir / "overrides.yaml")
    etda = load_etda_actors(data_dir / "etda_threat_groups.json")
    misp = load_misp_actors(data_dir / "misp_threat_actor.json")
    misp_by_gid = _misp_index_by_mitre(misp)
    misp_by_name = _misp_index_by_name(misp)

    etda_by_gid: dict[str, dict] = {}
    for e in etda:
        gid = (e.get("mitre_id") or e.get("group_id") or "").upper()
        if gid:
            etda_by_gid[gid] = e

    for gid, prof in profiles.items():
        # --- MISP ---
        misp_entry = misp_by_gid.get(gid)
        if misp_entry is None:
            for key in _name_keys(prof.name, prof.aliases):
                if key in misp_by_name:
                    misp_entry = misp_by_name[key]
                    break
        if misp_entry is not None:
            etda_cats, misp_tags = _misp_motivations(misp_entry)
            for cat in etda_cats:
                if cat not in prof.motivations:
                    prof.motivations.append(cat)
            for tag in misp_tags:
                if tag not in prof.misp_motivations:
                    prof.misp_motivations.append(tag)
            country = (misp_entry.get("meta") or {}).get("country")
            if country and country not in prof.regions:
                prof.regions.append(country)
                prof.suspected_origin = prof.suspected_origin or country
            for syn in (misp_entry.get("meta") or {}).get("synonyms", []) or []:
                if syn and syn not in prof.aliases:
                    prof.aliases.append(syn)
            if "misp" not in prof.sources:
                prof.sources.append("misp")

        # --- ETDA ---
        etda_entry = etda_by_gid.get(gid)
        if etda_entry is not None:
            for cat in etda_entry.get("motivations", []) or [etda_entry.get("motivation")]:
                if cat and cat in MOTIVATION_CATEGORIES and cat not in prof.motivations:
                    prof.motivations.append(cat)
            for region in etda_entry.get("regions", []) or []:
                if region not in prof.regions:
                    prof.regions.append(region)
            if "etda" not in prof.sources:
                prof.sources.append("etda")

        # --- Overrides (authoritative) ---
        override = overrides.get(gid) or {}
        for cat in override.get("motivations", []) or []:
            if cat in MOTIVATION_CATEGORIES and cat not in prof.motivations:
                prof.motivations.insert(0, cat)
        for region in override.get("regions", []) or []:
            if region not in prof.regions:
                prof.regions.insert(0, region)
        if override:
            if "override" not in prof.sources:
                prof.sources.append("override")

    return profiles


def coverage_stats(profiles: dict[str, GroupProfile]) -> dict:
    """Return summary stats for quick reporting in the notebook."""
    total = len(profiles)
    if total == 0:
        return {"total": 0, "with_motivation": 0, "coverage": 0.0, "by_motivation": {}}
    with_motive = sum(1 for p in profiles.values() if p.motivations)
    by_cat: dict[str, int] = {c: 0 for c in MOTIVATION_CATEGORIES}
    for p in profiles.values():
        for c in p.motivations:
            by_cat[c] = by_cat.get(c, 0) + 1
    return {
        "total": total,
        "with_motivation": with_motive,
        "coverage": with_motive / total,
        "by_motivation": by_cat,
    }
