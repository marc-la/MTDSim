"""Persist the L3a structural nets: one diagram + one summary JSON per class,
plus a ``data/ogasp/`` README.

Diagrams go to ``data/ogasp/_viz/`` (gitignored, regenerable). The summary
JSONs and README under ``data/ogasp/`` are tracked -- they are the structural
record (places, transitions, reachability, objective-reachability, prefix gap).
"""

from __future__ import annotations

import json
from pathlib import Path

from mtdsim.l3_simulation.petri.analysis import StructuralReport
from mtdsim.l3_simulation.petri.build import StructuralNet

_REPO_ROOT = Path(__file__).resolve().parents[4]
OGASP_DIR = _REPO_ROOT / "data" / "ogasp"
VIZ_DIR = OGASP_DIR / "_viz"


def draw_net(snet: StructuralNet, viz_dir: Path = VIZ_DIR) -> Path:
    """Render one class net to ``_viz/<class>.png`` via SNAKES/graphviz.

    Needs the graphviz ``dot`` binary on PATH (the ``gv`` plugin is loaded in
    ``build``)."""
    viz_dir = Path(viz_dir)
    viz_dir.mkdir(parents=True, exist_ok=True)
    out = viz_dir / f"{snet.class_name}.png"
    snet.net.draw(str(out))
    return out


def persist_summary(
    snet: StructuralNet, report: StructuralReport, out_dir: Path = OGASP_DIR
) -> Path:
    """Write ``data/ogasp/<class>_structural.json`` -- the net shape + its
    structural report, with every transition's GASP provenance inline."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "class_name": snet.class_name,
        "provenance": snet.provenance,
        "places": list(snet.tactics),
        "entry_marking": snet.entry_tactic,
        "transitions": [
            {
                "name": t.name,
                "src_tactic": t.src_tactic,
                "dst_tactic": t.dst_tactic,
                "gasp_edges": [list(e) for e in t.edges],
            }
            for t in snet.transitions
        ],
        "report": report.to_dict(),
    }
    out = out_dir / f"{snet.class_name}_structural.json"
    with open(out, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return out


def write_readme(
    reports: dict[str, StructuralReport], out_dir: Path = OGASP_DIR
) -> Path:
    """Write ``data/ogasp/README.md`` -- what the artefacts are, how to rebuild,
    and the headline structural findings (incl. the prefix gap per class)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# `data/ogasp/` — L3a OGASP structural Petri nets",
        "",
        "Four un-weighted **structural** tactic-place Petri nets (one per GASP",
        "class), built in SNAKES with a single moving black token. The shape",
        "only — no rates, timing, weights, rewards, MTD or CTMC (those are later",
        "stages). This is Stage 1 (L3a) of the OGASP Petri-net workstream.",
        "",
        "- **Build code:** [`src/mtdsim/l3_simulation/petri/`](../../src/mtdsim/l3_simulation/petri).",
        "- **Design / rationale:** [`docs/notes/2026-06-18_l3_petri_feasibility.md`](../../docs/notes/2026-06-18_l3_petri_feasibility.md)",
        "  (the base structural net is GO-unconditional, sec.8).",
        "- **Locked P/T/F/M mapping:** places = ATT&CK tactics; transitions =",
        "  inter-tactic tactic-pairs (each tracing to >=1 GASP technique-edge — the",
        "  no-synthesis invariant); flow = `place[a] -> T -> place[b]`; marking =",
        "  one black token in `reconnaissance` (else `initial-access`).",
        "",
        "## Rebuild",
        "",
        "```sh",
        "pip install snakes                 # not in environment.yml; needs graphviz `dot` for diagrams",
        "PYTHONPATH=src python -m mtdsim.l3_simulation.petri   # write <class>_structural.json x4 + _viz/<class>.png x4",
        "PYTHONPATH=src python -m pytest tests/l3_simulation/  # validation gate",
        "```",
        "",
        "## Contents",
        "",
        "| Path | Tracked? | What |",
        "|---|---|---|",
        "| `<class>_structural.json` | **computed** | net shape (places, transitions + per-transition GASP provenance) + structural report |",
        "| `_viz/<class>.png` | gitignored | rendered diagram (regenerable; mirrors the `data/gasp/_*` pattern) |",
        "",
        "## Structural summary",
        "",
        "| Class | Places | Transitions | Inter-tactic edges | Self-loops dropped | Objective reachable from recon | recon→initial-access |",
        "|---|--:|--:|--:|--:|---|---|",
    ]
    for cls, r in reports.items():
        obj_reach = (
            "yes"
            if r.all_objectives_reachable_from_entry
            else ("partial" if r.any_objective_reachable_from_entry else "**no**")
        )
        prefix = (
            "bridged"
            if r.prefix_gap.recon_reaches_initial_access
            else "**disconnected**"
        )
        lines.append(
            f"| `{cls}` | {r.n_places} | {r.n_transitions} | "
            f"{r.n_inter_tactic_edges} | {r.n_intra_tactic_selfloops_dropped} | "
            f"{obj_reach} | {prefix} |"
        )

    lines += [
        "",
        "## The prefix gap (inspect-the-base finding)",
        "",
        "The marking seeds the token in `reconnaissance`. On the observed-only",
        "base the corpus starts at the point of detection, so the",
        "`reconnaissance → initial-access` link is near-absent — and it shows up",
        "directly in the single-token reachability:",
        "",
    ]
    for cls, r in reports.items():
        lines.append(f"- **{cls}** — {r.prefix_gap.interpretation}")
    lines += [
        "",
        "Consequence: in the classes where recon is an island, a recon-seeded",
        "token cannot reach the objective; seeding at `initial-access` (the",
        "corpus's dominant real entry) is required. Whether to add the",
        "literature-grounded `recon → initial-access` inferred prefix bridge",
        "(GAP Decision 6 Option B) is the next decision — **deferred by intent**:",
        "inspect this base first. See the feasibility study sec.4 / sec.9.",
        "",
    ]
    out = out_dir / "README.md"
    out.write_text("\n".join(lines) + "\n")
    return out


__all__ = [
    "OGASP_DIR",
    "VIZ_DIR",
    "draw_net",
    "persist_summary",
    "write_readme",
]
