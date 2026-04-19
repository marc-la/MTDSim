"""Visual styling constants — palettes, label maps, default presets.

Kept separate from ``payload.py`` so serialisation stays pure data and
style can be themed without touching the payload builder.
"""

from __future__ import annotations


# 14-colour categorical palette for tactic layers (0-13) — ColorBrewer Set3+.
TACTIC_PALETTE: list[str] = [
    "#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462",
    "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f",
    "#1f78b4", "#e31a1c",
]

EVIDENCE_COLOUR: dict[str, str] = {
    "attack_flow":      "#2ca02c",
    "co_occurrence":    "#1f77b4",
    "caldera_sequence": "#ff7f0e",
    "ontology":         "#9467bd",
    "documentation":    "#7f7f7f",
    "cti_report":       "#17becf",
}

EVIDENCE_LABEL: dict[str, str] = {
    "attack_flow":      "Attack Flow (MITRE CTID)",
    "co_occurrence":    "Co-occurrence (mined)",
    "ontology":         "Ontology (STIX descriptions)",
    "documentation":    "Documentation",
    "cti_report":       "CTI report",
    "caldera_sequence": "CALDERA sequence",
}

DEFAULT_VISIBLE_EVIDENCE: set[str] = {"attack_flow"}

# Motivation palette is overlay-only: motivation is a group-level
# attribute kept on ``GroupProfile`` as post-hoc metadata and rendered
# in the group detail panel; it is no longer threaded onto technique
# nodes or dependency edges in the main payload.
MOTIVATION_COLOUR: dict[str, str] = {
    "information_theft_espionage": "#5e81ac",
    "financial_gain":              "#a3be8c",
    "financial_crime":             "#d08770",
    "sabotage_destruction":        "#bf616a",
}

MOTIVATION_LABEL: dict[str, str] = {
    "information_theft_espionage": "Espionage / Information theft",
    "financial_gain":              "Financial gain",
    "financial_crime":             "Financial crime",
    "sabotage_destruction":        "Sabotage / Destruction",
}
