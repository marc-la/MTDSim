"""fig:controller-mapping — the tactic-to-verb mapping the movement layer runs on.

Draws the L3 controller mapping as a bipartite figure: the fifteen ATT&CK
tactics on the left in the shared tactic axis, the six substrate verbs on the
right, edges for the mapping, and an empty slot where a tactic dispatches
nothing. The dwell-only rows are the figure's argument — they are the action
layer's coverage concession, and they carry the one accent this figure spends
(`figure_table_conventions.md` §b2, and the greys + one-accent pipeline ruling).

Everything load-bearing is read, never typed:

* the mapping, its dispositions and its per-row reasons from the selected
  version in `data/ogasp/controller/mappings/` (default `v2_partial`, the
  partial map §4.2.4.1 describes);
* the version's registry entry, so the caption's pin and the coverage claim
  come from the manifest rather than from memory;
* the tactic order, display names and the ATT&CK version pin from the pinned
  bundle, via `_tactic_axis` (§b5, §b6);
* the lifecycle stage bands from `data/ogasp/controller/lifecycle_consensus.json`.

Two classes of string are authored here rather than read, and both are
presentation text, which §g licenses as part of the figure spec:

1. **Verb names.** `SCAN_NEIGHBOR` is a code identifier, and raw identifiers in
   figures are a named anti-pattern (§g, the tay2024 failure). VERB_LABEL maps
   each to its domain term from `attacker_phase_catalogue.md` §§1--6. Note
   "Neighbour reveal": the verb name is the dissertation's own common noun, so
   it takes AU spelling, while the tactic names beside it keep MITRE's US
   spelling because they are looked-up proper names — the two halves of the
   2026-08-20 Australianisation ruling (§i), visible in one figure.
2. **Reasons.** REASON distils each row's `reason` column for the appendix
   table. The generator fails loudly if the mapping carries a tactic with no
   reason, so a new or renamed row cannot ship without one; it cannot, however,
   notice a *reworded* reason, so a substantive edit to the CSV's reason column
   should be re-checked against these entries.

The per-row reasoning is deliberately **not** in the figure (Marc, 2026-08-20):
a diagram carries the mapping, and the reasoning is table material. So this one
generator emits both halves — the figure, and the appendix table that decodes
it — which is also what keeps the two from disagreeing.

One input is **not tracked**: the ATT&CK bundle `_tactic_axis` reads sits under
`data/gap/_attack/`, which `.gitignore` excludes. The mapping, the manifest and
the lifecycle staging all are tracked, so only the axis half has this dependency.
The consequence is worth knowing before a cold session tries to regenerate: the
emitted `.tex`/`.pdf` are committed and the dissertation therefore builds from a
clean checkout, but *re-running this generator* needs the bundle present locally.
It fails loudly rather than falling back to a hard-coded axis, which is the
intended behaviour — a silently restated axis is the drift `_tactic_axis` exists
to prevent.

Usage: `python tools/controller_mapping_figure.py [--version v2_partial]
[--no-compile]` -> `docs/thesis/figures/controller_mapping.{tex,pdf}` and
`docs/thesis/tables/controller_mapping_reasons.tex`.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tactic_axis import load_axis, load_stages  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
MAPPINGS = REPO / "data" / "ogasp" / "controller" / "mappings"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
TAB_DIR = REPO / "docs" / "thesis" / "tables"
STEM = "controller_mapping"

DWELL_ONLY = "dwell-only"

# Substrate verbs in domain terms (attacker_phase_catalogue.md §§1--6). See the
# module docstring on why these are authored and why "Neighbour" is AU.
VERB_LABEL = {
    "SCAN_HOST": "Reachable-host scan",
    "ENUM_HOST": "Host enumeration",
    "SCAN_PORT": "Port scan",
    "EXPLOIT_VULN": "Vulnerability exploit",
    "BRUTE_FORCE": "Credential brute force",
    "SCAN_NEIGHBOR": "Neighbour reveal",
}

# One row's reason, distilled from the mapping's own `reason` column for the
# appendix table (`tab:controller-mapping`). These do NOT appear in the figure:
# per-row reasoning is table material, not diagram material, so the figure shows
# the mapping and the appendix carries why each row holds its value (Marc,
# 2026-08-20). Wording is drafted here and owed a pass, as `tab:experiment-one`
# was; the tactic and action columns beside them are read from the CSV.
REASON = {
    "reconnaissance": "Builds the queue of attackable hosts from the current "
                      "foothold --- the substrate's only survey act.",
    "resource-development": "Acquires capability off-target, and no world outside "
                            "the victim network is modelled.",
    "initial-access": "The only verb whose deliberate effect converts a host the "
                      "attacker does not own into one it does.",
    "execution": "Applies a vulnerability's effect to a service --- the only act "
                 "of running something on a target.",
    "persistence": "A compromised host stays compromised unconditionally, so there "
                   "is no access artefact to plant or maintain.",
    "privilege-escalation": "The substrate has no privilege dimension; the stand-in "
                            "is exploited impact accruing toward the threshold at "
                            "which a host falls.",
    "stealth": "Nothing observes the attacker, so there is no state evasion could "
               "alter --- the model's stealth gap, made explicit.",
    "defense-impairment": "MTD scheduling is a defender-side process the attacker "
                          "can neither observe nor touch.",
    "credential-access": "Attempts a login against the current host from the pool of "
                         "compromised usernames --- T1110 with no interpretation.",
    "discovery": "Enumerates the open ports reachable on the current host (T1046), "
                 "which is what lets a later exploit run at all.",
    "lateral-movement": "Pops the next host, makes it current and sets the pivot --- "
                        "the act of moving to a remote system.",
    "command-and-control": "The one row the inherited design states itself: Brown "
                           "describes this verb as command and control revealing "
                           "connected hosts.",
    "collection": "The substrate has no data --- hosts carry services and "
                  "vulnerabilities, nothing gatherable.",
    "exfiltration": "Neither half exists: nothing to take, and nowhere to send it.",
    "impact": "No verb destroys, encrypts or denies anything, so an objective-band "
              "walk spends time rather than misrepresenting what it is doing.",
}

# --- geometry (cm) ---------------------------------------------------------
# Sized against measured text widths at the two type sizes below. The figure's
# natural width is ~11.6 cm and it is included at 0.78\textwidth (\textwidth is
# 411.4pt = 14.51 cm in cshonours), a scale of ~0.98 -- so the smallest glyph
# prints at ~9.8pt and the names at ~10.7pt: clear of the ~8pt floor (§g), and
# still below body text. Note that the inclusion width is part of the sizing,
# not a layout afterthought: at full \textwidth this figure would be scaled UP
# and its labels would print larger than the prose around them. The type scale
# is a step larger than the older family figures, which at \scriptsize/\tiny
# print around 5--7pt (see figure_table_conventions.md §h, §i).
NAME_FONT = r"\small"          # tactic and verb names (10.95pt natural)
SMALL_FONT = r"\footnotesize"  # headers and stage labels (10pt natural)

# With the reasons moved to the appendix table the figure is narrow enough to
# label its stage bands horizontally, which the earlier reason-column layout had
# no room for: a rotated gutter label ("preparation", ~2.1 cm at SMALL_FONT)
# overruns a two-row band 1.4 cm tall and collides with its neighbour, whereas a
# horizontal label in a left gutter fits any band height.
ROW_PITCH = 0.72
STAGE_X = 0.0               # left edge of the horizontal stage-band labels
STAGE_W = 2.25              # measured width of "post-intrusion" plus a pad
TACTIC_X = STAGE_W + 3.35   # right edge of the tactic names
EDGE_X0 = TACTIC_X + 0.18   # edges and dashes leave here
VERB_L = EDGE_X0 + 1.74     # left edge of the verb column
VERB_W = 4.05
VERB_H = 0.54
VERB_CX = VERB_L + VERB_W / 2
VERB_R = VERB_L + VERB_W
FIG_R = VERB_R
BAND_L = 0.0

ACCENT = "accent"


def _esc(s: str) -> str:
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&")
             .replace("%", r"\%").replace("#", r"\#").replace("_", r"\_"))


def load_mapping(version: str) -> tuple[list[dict], dict]:
    """The mapping's rows and its registry entry, both from tracked artefacts."""
    manifest = json.loads((MAPPINGS / "manifest.json").read_text())
    entry = next((v for v in manifest["versions"] if v["name"] == version), None)
    if entry is None:
        known = ", ".join(v["name"] for v in manifest["versions"])
        raise SystemExit(f"unknown mapping version {version!r}; registry has: {known}")
    with (MAPPINGS / entry["file"]).open() as fh:
        rows = list(csv.DictReader(fh))
    return rows, entry


def check(rows: list[dict], axis, stage_of: dict[str, int]) -> None:
    """Fail loudly on any drift between the mapping, the axis and the glosses."""
    axis.check_against(sorted({r["tactic"] for r in rows},
                              key=lambda t: axis.matrix_order.index(t)
                              if t in axis.matrix_order else 99))
    missing = [r["tactic"] for r in rows if r["tactic"] not in REASON]
    if missing:
        raise SystemExit(f"no appendix reason for: {', '.join(missing)}")
    unstaged = [r["tactic"] for r in rows if r["tactic"] not in stage_of]
    if unstaged:
        raise SystemExit(f"no lifecycle stage for: {', '.join(unstaged)}")
    for r in rows:
        mapped = r["disposition"] != DWELL_ONLY
        if mapped and not r["sim_phase"]:
            raise SystemExit(f"{r['tactic']}: mapped but names no verb")
        if mapped and r["sim_phase"] not in VERB_LABEL:
            raise SystemExit(f"{r['tactic']}: no domain name for verb {r['sim_phase']!r}")
        if not mapped and r["sim_phase"]:
            raise SystemExit(f"{r['tactic']}: dwell-only but names a verb")


def emit(rows: list[dict], entry: dict, axis, stage_of, stage_name) -> str:
    by_tactic = {r["tactic"]: r for r in rows}
    order = axis.stage_grouped_order(stage_of)
    y_of = {t: -i * ROW_PITCH for i, t in enumerate(order)}

    # A verb sits at the mean height of the tactics it serves, so its edges fan
    # symmetrically. The verb column therefore reads in the order of the tactics
    # it serves, not in the substrate's own call order -- under this mapping the
    # two no longer agree (controller_mapping_v2.md §1), which the caption says.
    served: dict[str, list[str]] = {}
    for t in order:
        verb = by_tactic[t]["sim_phase"]
        if verb:
            served.setdefault(verb, []).append(t)
    verb_y = {v: sum(y_of[t] for t in ts) / len(ts) for v, ts in served.items()}

    dwell = [t for t in order if by_tactic[t]["disposition"] == DWELL_ONLY]
    L: list[str] = []
    w = L.append

    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usetikzlibrary{arrows.meta,positioning,calc}")
    w(r"\definecolor{accent}{RGB}{31,84,140}")
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,>={Stealth[length=1.6mm]},"
      r"every node/.style={font=%s}]" % NAME_FONT)

    # --- lifecycle stage bands (alternating, behind everything) -------------
    y_bot = y_of[order[-1]]
    for stage in sorted({stage_of[t] for t in order}):
        members = [t for t in order if stage_of[t] == stage]
        top = y_of[members[0]] + ROW_PITCH / 2
        bot = y_of[members[-1]] - ROW_PITCH / 2
        if stage % 2 == 1:
            w(r"\fill[black!4] (%.2f,%.2f) rectangle (%.2f,%.2f);"
              % (BAND_L, top, FIG_R, bot))
        w(r"\node[anchor=west,font=%s,text=black!60] at (%.2f,%.3f) {%s};"
          % (SMALL_FONT, STAGE_X + 0.08, (top + bot) / 2, _esc(stage_name[stage])))

    # --- the key, then the column headers ------------------------------------
    # The empty slot is a drawn symbol, so it gets a symbol legend inside the
    # figure (§d2) as well as the caption decode (§b2).
    ky = ROW_PITCH * 1.75
    w(r"\draw[%s,line width=0.4pt,dash pattern=on 1.1pt off 1.3pt] "
      r"(%.2f,%.3f) -- (%.2f,%.3f);" % (ACCENT, 0.16, ky, 0.99, ky))
    w(r"\draw[%s,line width=0.4pt] (%.2f,%.3f) rectangle (%.2f,%.3f);"
      % (ACCENT, 0.99, ky - 0.11, 1.21, ky + 0.11))
    w(r"\node[anchor=west,font=%s,text=%s] at (%.2f,%.3f) "
      r"{no verb: the tactic dwells and dispatches nothing (%d of %d)};"
      % (SMALL_FONT, ACCENT, 1.33, ky, len(dwell), len(order)))

    hy = ROW_PITCH * 0.80
    w(r"\node[anchor=west,font=%s,text=black!60] at (%.2f,%.2f) {lifecycle stage};"
      % (SMALL_FONT, STAGE_X + 0.08, hy))
    w(r"\node[anchor=east,font=%s,text=black!60] at (%.2f,%.2f) {ATT\&CK tactic};"
      % (SMALL_FONT, TACTIC_X, hy))
    w(r"\node[anchor=center,font=%s,text=black!60] at (%.2f,%.2f) {substrate action};"
      % (SMALL_FONT, VERB_CX, hy))

    # --- tactic rows ---------------------------------------------------------
    for t in order:
        y = y_of[t]
        is_dwell = by_tactic[t]["disposition"] == DWELL_ONLY
        colour = ACCENT if is_dwell else "black"
        w(r"\node[anchor=east,text=%s] at (%.2f,%.3f) {%s};"
          % (colour, TACTIC_X, y, _esc(axis.label[t])))

    # --- the mapping ---------------------------------------------------------
    for t in order:
        y = y_of[t]
        verb = by_tactic[t]["sim_phase"]
        if not verb:
            # The empty slot lands exactly where a verb would have been, so the
            # concession reads as a declared absence rather than a missing line.
            w(r"\draw[%s,line width=0.4pt,dash pattern=on 1.1pt off 1.3pt] "
              r"(%.2f,%.3f) -- (%.2f,%.3f);" % (ACCENT, EDGE_X0, y, VERB_L + 0.06, y))
            w(r"\draw[%s,line width=0.4pt] (%.2f,%.3f) rectangle (%.2f,%.3f);"
              % (ACCENT, VERB_L + 0.06, y - 0.11, VERB_L + 0.28, y + 0.11))
            continue
        vy = verb_y[verb]
        bulge = min(1.05, 0.34 + abs(vy - y) * 0.55)
        w(r"\draw[black!45,line width=0.45pt] (%.2f,%.3f) .. controls "
          r"+(%.2f,0) and +(-%.2f,0) .. (%.2f,%.3f);"
          % (EDGE_X0, y, bulge, bulge, VERB_L, vy))

    # --- verb nodes ----------------------------------------------------------
    for verb, ts in served.items():
        vy = verb_y[verb]
        w(r"\draw[black!45,line width=0.5pt,fill=white,rounded corners=1.2pt] "
          r"(%.2f,%.3f) rectangle (%.2f,%.3f);"
          % (VERB_L, vy - VERB_H / 2, VERB_R, vy + VERB_H / 2))
        # No "n tactics" line: the fan-in already carries the multiplicity, and
        # only one verb has more than one edge. The caption names that verb.
        w(r"\node[anchor=center] at (%.3f,%.3f) {%s};"
          % (VERB_CX, vy, _esc(VERB_LABEL[verb])))

    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


def emit_table(rows: list[dict], entry: dict, axis, stage_of, stage_name) -> str:
    """The appendix companion: one row per tactic, with the reason the figure
    deliberately does not carry. Ledger genre (§e6), booktabs, no vertical
    rules, rows in the same stage-grouped tactic order the figure draws."""
    by_tactic = {r["tactic"]: r for r in rows}
    order = axis.stage_grouped_order(stage_of)
    n_dwell = sum(1 for r in rows if r["disposition"] == DWELL_ONLY)

    L: list[str] = []
    L.append(r"% GENERATED by tools/controller_mapping_figure.py --- do not hand-edit.")
    L.append(r"\begin{table}[htbp]")
    L.append(r"\centering")
    L.append(r"\caption[Why each tactic maps as it does]{Why each tactic holds the "
             r"value it does under the tactic-to-verb mapping "
             r"\texttt{%s}, drawn as Figure~\ref{fig:controller-mapping}. Rows run "
             r"in the tactic axis of that figure, grouped by lifecycle stage. A "
             r"dash in the action column is a dwell-only tactic: %d of the %d "
             r"consume simulated time and dispatch nothing, and the reason states "
             r"what the substrate would have to model before the row could be "
             r"mapped.}" % (_esc(entry["name"]), n_dwell, len(rows)))
    L.append(r"\label{tab:controller-mapping}")
    # \footnotesize, and the reason column takes the width the two fixed columns
    # leave: at this size "Command and control" is ~98pt and "Credential brute
    # force" ~96pt, which with two 12pt column gaps leaves ~193pt of the 411.4pt
    # \textwidth -- hence 0.46. The size is set by height, not width: fifteen
    # rows of reason run past the text block at \normalsize (33.6pt overfull
    # \hbox) and at \small (60.6pt too tall for the page). \footnotesize both
    # shortens the lines and widens the column, so fewer cells wrap.
    L.append(r"\footnotesize")
    L.append(r"\begin{tabular}{@{}l l p{0.46\textwidth}@{}}")
    L.append(r"\toprule")
    L.append(r"Tactic & Substrate action & Reason \\")
    L.append(r"\midrule")
    prev_stage = None
    for t in order:
        if prev_stage is not None and stage_of[t] != prev_stage:
            L.append(r"\addlinespace")
        prev_stage = stage_of[t]
        verb = by_tactic[t]["sim_phase"]
        action = VERB_LABEL[verb] if verb else "---"
        L.append(r"%s & %s & %s \\" % (_esc(axis.label[t]), _esc(action), REASON[t]))
    L.append(r"\bottomrule")
    L.append(r"\end{tabular}")
    L.append(r"\end{table}")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", default="v2_partial",
                    help="mapping version from the registry (default: v2_partial)")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    axis = load_axis()
    stage_of, stage_name = load_stages()
    rows, entry = load_mapping(args.version)
    check(rows, axis, stage_of)

    tex = emit(rows, entry, axis, stage_of, stage_name)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUT_DIR / f"{STEM}.tex"
    tex_path.write_text(tex)
    print(f"wrote {tex_path.relative_to(REPO)}")

    TAB_DIR.mkdir(parents=True, exist_ok=True)
    tab_path = TAB_DIR / f"{STEM}_reasons.tex"
    tab_path.write_text(emit_table(rows, entry, axis, stage_of, stage_name))
    print(f"wrote {tab_path.relative_to(REPO)}")

    # the numbers and pins the caption quotes -- printed for cross-checking
    mapped = [r for r in rows if r["disposition"] != DWELL_ONLY]
    dwell = [r for r in rows if r["disposition"] == DWELL_ONLY]
    verbs = {r["sim_phase"] for r in mapped}
    multi = {v: sum(1 for r in mapped if r["sim_phase"] == v) for v in verbs}
    print(f"mapping={entry['name']}  ATT&CK={axis.version}  tactics={len(rows)}  "
          f"mapped={len(mapped)}  dwell-only={len(dwell)}  verbs used={len(verbs)}/"
          f"{len(VERB_LABEL)}")
    print("coverage (registry): " + entry["coverage"])
    print("verbs carrying >1 tactic: "
          + (", ".join(f"{VERB_LABEL[v]}={n}" for v, n in multi.items() if n > 1) or "none"))
    print("dwell-only: " + ", ".join(axis.label[r["tactic"]] for r in dwell))
    # the band decode the caption must carry, in the order the figure draws it
    order = axis.stage_grouped_order(stage_of)
    seen = [stage_of[t] for t in order]
    print("stage bands (top to bottom): "
          + ", ".join(stage_name[s] for s in dict.fromkeys(seen)))

    if not args.no_compile:
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                            tex_path.name], cwd=OUT_DIR, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            raise SystemExit("pdflatex failed")
        for ext in (".aux", ".log"):
            p = OUT_DIR / f"{STEM}{ext}"
            if p.exists():
                p.unlink()
        print(f"wrote {(OUT_DIR / (STEM + '.pdf')).relative_to(REPO)}")


if __name__ == "__main__":
    main()
