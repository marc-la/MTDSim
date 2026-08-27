"""`tab:preliminary-extraction` (app:cooccurrence) --- the preliminary extraction runs.

The appendix entry behind one sentence in §4.2.1: *other approaches were
considered ... co-occurrence mining gave low coverage and keyword mining poor
fidelity*. The question the entry answers is the one the project opened with ---
**how is dependency between tactics obtained?** --- so the table is a list of
attempted modes, one row each, and the row says what a dependency rested on,
where its direction came from, how much tactic structure it recovered, and why
it was not used.

Two registers, on Marc's abstraction ruling (2026-08-20). The April parameters
moved around during exploration and the threshold he remembers is not in
committed history, so **nothing threshold-sensitive is printed**: no support,
no confidence, no median cut, no lift, no corroboration counts. What is printed
either cannot move with any parameter (what an edge rests on; where direction
comes from) or is a relative comparison read at the resolution the dissertation
ships at (tactic transitions recovered), stamped to its build in the caption.

Provenance. The two abandoned modes exist in exactly one built artefact and
always will: `gap_v0.4_latest.json`, which is where they were merged before
Decision 1 (`gap_schema.md`) removed them. `gap_v0.5.json` --- the shipped L1 ---
carries no evidence-type field at all, because it is the artefact that *resulted*
from the abandonment. So v0.4 supplies the like-for-like three-way comparison in
the table body, and v0.5 supplies the endpoint quoted in the caption.

The table body is a same-build comparison on purpose: all three modes ran that
day off one ATT&CK parse, so the coverage column compares modes rather than
corpus vintages.

Every number is computed here from the artefacts. Every word comes from
`data/gap/archive/preliminary_extraction_labels.json`. Neither is typed into
this file.

Usage:  python tools/preliminary_extraction_table.py
        python tools/preliminary_extraction_table.py --check   (recompute, emit nothing)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LABELS = REPO / "data" / "gap" / "archive" / "preliminary_extraction_labels.json"
EVIDENCE = REPO / "data" / "gap" / "archive" / "v0_4_extraction_run.json"
SHIPPED = REPO / "data" / "gap" / "gap_v0.5.json"
OUT = REPO / "docs" / "thesis" / "tables" / "tab_D-0a_preliminary_extraction.tex"

# The v0.4 GAP is not on `dev` --- it is the superseded artefact, held on the
# archive branches. Both carry byte-identical copies (checked 2026-08-20); the
# branch is named, and the commit it resolves to is recorded in the emitted
# evidence file so a later reader can pin what was read.
V04_BRANCH = "archive/attacker-profiling"
V04_PATH = "data/gap/gap_v0.4_latest.json"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO), *args],
        check=True, capture_output=True, text=True,
    ).stdout


def load_v04() -> tuple[dict, str]:
    """The superseded v0.4 GAP, read out of the archive branch, with its sha."""
    sha = _git("rev-parse", V04_BRANCH).strip()
    return json.loads(_git("show", f"{sha}:{V04_PATH}")), sha


def tactic_of(nodes: dict, tid: str, fold: dict | None = None) -> str | None:
    node = nodes.get(tid)
    if not node:
        return None
    t = node.get("primary_tactic")
    return (fold or {}).get(t, t)


def cross_tactic_pairs(nodes: dict, edges: list, fold: dict | None = None) -> set[tuple[str, str]]:
    """Distinct ordered tactic->tactic transitions, self-transitions excluded.

    Collapsing to tactics is what makes the comparison legible: the dissertation
    resolves at tactic granularity, so this counts the structure each mode
    actually contributes to the graph that ships.
    """
    pairs = set()
    for e in edges:
        a = tactic_of(nodes, e["source_id"], fold)
        b = tactic_of(nodes, e["target_id"], fold)
        if a and b and a != b:
            pairs.add((a, b))
    return pairs


def evidence_types(edge: dict) -> set[str]:
    return {ev["source_type"] for ev in edge.get("evidence", [])}


def measure() -> dict:
    labels = json.loads(LABELS.read_text())
    v04, sha = load_v04()
    shipped = json.loads(SHIPPED.read_text())

    nodes04 = v04["nodes"]
    tactics = sorted({n["primary_tactic"] for n in nodes04.values() if n.get("primary_tactic")})
    # The denominator the coverage column is read against: ordered pairs of
    # distinct tactics. Derived from the axis, never typed.
    possible = len(tactics) * (len(tactics) - 1)

    modes = []
    for spec in labels["modes"]:
        edges = [e for e in v04["edges"] if spec["evidence_source"] in evidence_types(e)]
        pairs = cross_tactic_pairs(nodes04, edges)
        modes.append({
            **{k: v for k, v in spec.items() if not k.startswith("_")},
            "technique_edges": len(edges),
            "tactic_transitions": len(pairs),
        })

    # The shipped L1 resolves on this project's 15-tactic axis; v0.4 resolves on
    # stock ATT&CK's 14. Fold the split back so the caption's shipped figure is
    # read against the same denominator as the table body --- otherwise the two
    # coverage fractions are quoted against different axes and do not compare.
    fold = {k: v for k, v in labels["shipped_axis_fold"].items() if not k.startswith("_")}
    shipped_nodes = shipped["nodes"]
    shipped_tactics = {tactic_of(shipped_nodes, t, fold) for t in shipped_nodes}
    shipped_tactics = {t for t in shipped_tactics if t}
    if shipped_tactics != set(tactics):
        raise SystemExit(
            "axis mismatch after folding: shipped-only "
            f"{sorted(shipped_tactics - set(tactics))}, v0.4-only "
            f"{sorted(set(tactics) - shipped_tactics)}. Update shipped_axis_fold."
        )
    shipped_pairs = cross_tactic_pairs(shipped_nodes, shipped["edges"], fold)

    return {
        "_generated_by": "tools/preliminary_extraction_table.py",
        "_what": "Counts behind tab:preliminary-extraction. Regenerate; do not hand-edit.",
        "source": {
            "v0_4": {"branch": V04_BRANCH, "commit": sha, "path": V04_PATH,
                     "build_date": v04.get("build_date"),
                     "technique_source": v04.get("technique_source"),
                     "total_techniques": v04.get("total_techniques"),
                     "edge_count": v04.get("edge_count")},
            "v0_5": {"path": str(SHIPPED.relative_to(REPO)),
                     "build_date": shipped.get("build_date"),
                     "corpus_ref": shipped.get("corpus_ref"),
                     "attack_source": shipped.get("attack_source"),
                     "source_flow_count": shipped.get("source_flow_count"),
                     "node_count": shipped.get("node_count"),
                     "edge_count": shipped.get("edge_count")},
        },
        "tactic_count": len(tactics),
        "possible_cross_tactic_transitions": possible,
        "modes": modes,
        "shipped": {
            "axis_fold": fold,
            "tactic_transitions": len(shipped_pairs),
            "technique_edges": shipped.get("edge_count"),
            "flows": shipped.get("source_flow_count"),
        },
        "display": {k: v for k, v in labels["display"].items() if not k.startswith("_")},
        "not_attempted": labels["not_attempted"],
    }


def tex_escape(s: str) -> str:
    return s.replace("&", r"\&").replace("%", r"\%")


def pct(n: int, d: int) -> str:
    return f"{round(100 * n / d)}\\,\\%"


def render(m: dict) -> str:
    possible = m["possible_cross_tactic_transitions"]
    v4, v5 = m["source"]["v0_4"], m["source"]["v0_5"]
    ship = m["shipped"]

    rows = []
    for mode in m["modes"]:
        name = tex_escape(mode["name"])
        if mode.get("adopted"):
            name = f"\\textbf{{{name}}}"
        rows.append(
            f"{name} & {tex_escape(mode['rests_on'])} & "
            f"{tex_escape(mode['direction_from'])} & "
            f"{mode['tactic_transitions']} ({pct(mode['tactic_transitions'], possible)}) & "
            f"{tex_escape(mode['why_not'])} \\\\"
        )

    untried = "; ".join(tex_escape(x) for x in m["not_attempted"]["modes"])
    disp = m["display"]
    caption_short = "Modes of obtaining tactic dependency that were tried"
    caption = (
        f"The modes of obtaining dependency between tactics that were attempted, and "
        f"what each returned. \\emph{{Direction from}} is the column the entry turns on: "
        f"a mode that takes its direction from an assumed tactic ordering cannot learn an "
        f"ordering, and can express no loop at all, since a total order admits no backward "
        f"edge --- where the graph that ships preserves loops deliberately. "
        f"\\emph{{Tactic transitions}} counts distinct ordered transitions between two "
        f"different tactics, of the {possible} that {m['tactic_count']} tactics admit, with "
        f"techniques collapsed onto their primary tactic --- the granularity the model "
        f"works at. All three rows are measured on a single build, the superseded v0.4 "
        f"profile of {v4['build_date']} ({disp['v0_4_attack_source']}, "
        f"{v4['total_techniques']} parent techniques): it is the only artefact in which the "
        f"two abandoned modes were ever merged, and the shared build is what makes the "
        f"final column a comparison between modes rather than between corpus vintages. "
        f"Carried forward alone, Attack Flow reaches {ship['tactic_transitions']} of the "
        f"{possible} transitions ({pct(ship['tactic_transitions'], possible)}) in the graph "
        f"this dissertation uses --- {ship['technique_edges']} technique edges over "
        f"{ship['flows']} incidents ({disp['v0_5_corpus']}, {disp['v0_5_attack_source']}) "
        f"--- quoted over the same {possible} transitions, with the split that model makes "
        f"within defence evasion folded back so the two figures share an axis. "
        f"No threshold is reported anywhere in the table: the mining parameters were varied "
        f"throughout the exploratory period, and the table is built on what does not move "
        f"with them. Not attempted, and so absent here: {untried} --- "
        f"{tex_escape(m['not_attempted']['note'])}"
    )

    body = "\n".join(rows)
    return f"""% GENERATED by tools/preliminary_extraction_table.py --- do not hand-edit.
% Numbers: data/gap/archive/v0_4_extraction_run.json (computed from the v0.4 GAP
%   on {V04_BRANCH} and from data/gap/gap_v0.5.json).
% Wording: data/gap/archive/preliminary_extraction_labels.json.
% Caption SESSION-DRAFTED --- flagged for the voice pass.
% Requires booktabs (already in the preamble).

\\begin{{table}}[htbp]
\\centering
\\footnotesize
\\setlength{{\\tabcolsep}}{{4pt}}
\\caption[{caption_short}]{{{caption}}}
\\label{{tab:preliminary-extraction}}
\\begin{{tabular}}{{@{{}}l >{{\\raggedright\\arraybackslash}}p{{0.18\\textwidth}} >{{\\raggedright\\arraybackslash}}p{{0.12\\textwidth}} r >{{\\raggedright\\arraybackslash}}p{{0.29\\textwidth}}@{{}}}}
\\toprule
Mode & A dependency rests on & Direction from & \\shortstack[r]{{Tactic\\\\transitions}} & Why it was not used \\\\
\\midrule
{body}
\\bottomrule
\\end{{tabular}}
\\end{{table}}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="recompute and report; write nothing")
    args = ap.parse_args()

    m = measure()
    possible = m["possible_cross_tactic_transitions"]

    print(f"v0.4 {m['source']['v0_4']['commit'][:12]} ({m['source']['v0_4']['build_date']}), "
          f"{m['tactic_count']} tactics -> {possible} possible transitions")
    for mode in m["modes"]:
        print(f"  {mode['name']:<22} {mode['technique_edges']:>4} technique edges  "
              f"{mode['tactic_transitions']:>4} transitions  "
              f"{100 * mode['tactic_transitions'] / possible:5.1f}%")
    print(f"  {'shipped L1 (v0.5)':<22} {m['shipped']['technique_edges']:>4} technique edges  "
          f"{m['shipped']['tactic_transitions']:>4} transitions  "
          f"{100 * m['shipped']['tactic_transitions'] / possible:5.1f}%")

    if args.check:
        return 0

    EVIDENCE.write_text(json.dumps(m, indent=2) + "\n")
    OUT.write_text(render(m))
    print(f"\nwrote {EVIDENCE.relative_to(REPO)}\nwrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
