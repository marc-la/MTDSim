#!/usr/bin/env python3
"""Dissertation figure: the ATT&CK Enterprise matrix and the hierarchy
beneath one cell (ch3 subsec:attack, fig:attack-matrix).

The meet-in-the-middle design (Marc's ruling trail, 2026-09-02): the BASE
matrix is drawn to the design of attack.mitre.org/matrices/enterprise ---
fifteen tactic columns, bold horizontal sans headers (words stacked, never
slanted) over an "N techniques" count, white bordered cells in a shared-
border stack, a grey side tab on every technique that carries sub-techniques
--- but shape only, no technique names: at page width the reader gets the
familiar silhouette. The ZOOM cascade reuses the site's own gestures at
readable size:

  zoom 1  an accent box marks the zoomed region (Initial Access); a lens
          opens its eleven techniques as site-style named cells
  zoom 2  Valid Accounts' four sub-techniques decompose OUT TO THE RIGHT
          behind the site's dark spine bracket (the click-the-tab expansion)
  zoom 3  Domain Accounts opens into its technique PAGE: the Procedure
          Examples table --- real group rows, Volt Typhoon's first (the
          chapter's recurring illustration) --- the procedure level, which
          has no cell in the matrix

Typography follows the site: sans (Helvetica via helvet, standing in for
MITRE's Roboto). Palette stays the house's: greys, one accent
(RGB 31,84,140) on the worked-example path.

Every tactic name, technique name, count, side tab and procedure example is
read from the pinned Enterprise v19.1 STIX bundle
(data/gap/_attack/enterprise-attack-19.1.json); procedure examples are its
`uses` relationships onto the sub-technique. Nothing is typed. Numbers a
caption may quote are printed to stdout.

Zoom cells are TikZ nodes chained anchor-to-anchor, so LaTeX sizes every
cell to its own text --- no height estimation, nothing clips. Lens fills sit
on the background layer so cells overprint them.

Usage:
  python tools/attack_matrix_figure.py [--no-compile]

Style: TikZ, 12 pt base document; canvas 22 cm wide, included at \\textwidth
(measured 15.45 cm), so drawn text lands at ~0.70x on the page --- the
minutiae are for zooming, the silhouette for the page (Marc's ruling).
Written to docs/thesis/figures/fig_3-1-2a_attack_matrix.tex (+ .pdf).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUNDLE = REPO / "data" / "gap" / "_attack" / "enterprise-attack-19.1.json"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_3-1-2a_attack_matrix"

EXAMPLE_TACTIC = "initial-access"   # TA0001 --- the prose worked example
EXAMPLE_TECHNIQUE = "T1078"         # Valid Accounts
EXAMPLE_SUB = "T1078.002"           # Domain Accounts --- Volt Typhoon's
N_PROC_ROWS = 2                     # procedure-example rows shown on the card

# --- geometry (cm, at drawn scale; canvas is included at ~0.70x) -----------
CANVAS_W = 22.0
COL_GAP = 0.08
CELL_H = 0.15             # a shape-only cell in the base matrix
TAB_W = 0.08              # the sub-technique side tab, base matrix
HDR_LINES = 3             # header band: room for three stacked words
HDR_LINE_H = 0.20
HDR_FONT = r"\fontsize{5pt}{5.6pt}\selectfont\bfseries"
CNT_FONT = r"\fontsize{4.2pt}{4.9pt}\selectfont"
ZOOM_FONT = r"\fontsize{9pt}{10.8pt}\selectfont"
SUBCNT_FONT = r"\fontsize{6.5pt}{7.2pt}\selectfont"
TAG_FONT = r"\fontsize{6.5pt}{7.4pt}\selectfont\itshape"
Z1_X, Z1_W = 1.00, 6.60   # the Initial Access zoom stack
Z1_DROP = 0.60            # gap between matrix bottom and the zoom stack
ZTAB_W = 0.16             # side tab at zoom size
SPINE_W = 0.20            # the dark bracket behind a sub-technique stack
Z2_W = 5.30               # the sub-technique stack
Z2_RISE = 0.85            # stack top above the technique row (straddles it)
Z3_DX, Z3_W = 1.05, 6.60  # the Procedure Examples card
PROC_FONT = r"\fontsize{7.5pt}{8.9pt}\selectfont"
PROC_TITLE_FONT = r"\fontsize{8.5pt}{9.6pt}\selectfont\bfseries"


def ext_id(o: dict) -> str:
    return o["external_references"][0]["external_id"]


def live(o: dict) -> bool:
    return not o.get("revoked") and not o.get("x_mitre_deprecated")


def load():
    bundle = json.loads(BUNDLE.read_text())
    objs = bundle["objects"]
    matrix = next(o for o in objs if o["type"] == "x-mitre-matrix")
    tactics_by_ref = {o["id"]: o for o in objs if o["type"] == "x-mitre-tactic"}
    tactics = [tactics_by_ref[r] for r in matrix["tactic_refs"]]

    techniques = [o for o in objs if o["type"] == "attack-pattern" and live(o)]
    top = [o for o in techniques if not o.get("x_mitre_is_subtechnique")]
    subs_of: dict[str, list[dict]] = {}
    for o in techniques:
        if o.get("x_mitre_is_subtechnique"):
            subs_of.setdefault(ext_id(o).split(".")[0], []).append(o)
    for lst in subs_of.values():
        lst.sort(key=ext_id)

    per_tactic: dict[str, list[dict]] = {t["x_mitre_shortname"]: [] for t in tactics}
    for o in top:
        for ph in o.get("kill_chain_phases", []):
            if ph["kill_chain_name"] == "mitre-attack" and ph["phase_name"] in per_tactic:
                per_tactic[ph["phase_name"]].append(o)
    for lst in per_tactic.values():
        lst.sort(key=lambda o: o["name"])   # the site's order: alphabetical by name

    # procedure examples: `uses` relationships onto the example sub-technique
    by_id = {o["id"]: o for o in objs}
    sub_obj = next(o for o in techniques if o.get("external_references")
                   and ext_id(o) == EXAMPLE_SUB)
    procs = []
    for r in objs:
        if (r["type"] == "relationship" and r["relationship_type"] == "uses"
                and r.get("target_ref") == sub_obj["id"] and live(r)):
            src = by_id.get(r["source_ref"])
            if src is None or not live(src) or not src.get("external_references"):
                continue
            procs.append((ext_id(src), src["name"], src["type"],
                          r.get("description") or ""))
    n_procs = len(procs)
    groups = sorted(p for p in procs if p[2] == "intrusion-set")
    # Volt Typhoon leads the shown rows: the chapter's recurring illustration
    # (Marc's ruling 2026-09-02 --- the same campaign as SS3.1.1 and the
    # Attack Flow exemplar figure)
    lead = [g for g in groups if g[1] == "Volt Typhoon"]
    rest = [g for g in groups if g[1] != "Volt Typhoon"]
    return tactics, per_tactic, subs_of, (lead + rest)[:N_PROC_ROWS], n_procs


def esc(s: str) -> str:
    return (s.replace("&", r"\&").replace("#", r"\#").replace("%", r"\%")
             .replace("_", r"\_").replace("$", r"\$"))


def clean_desc(d: str, limit: int = 92) -> str:
    d = re.sub(r"\(Citation:[^)]*\)", "", d)
    d = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", d)
    d = " ".join(d.split())
    trunc = len(d) > limit
    if trunc:
        d = d[:limit].rsplit(" ", 1)[0].rstrip(",.;")
    return esc(d) + (r"\,\ldots" if trunc else "")


def emit(tactics, per_tactic, subs_of, proc_rows, n_procs) -> tuple[str, dict]:
    n = len(tactics)
    col_w = (CANVAS_W - COL_GAP * (n - 1)) / n
    counts = {s: len(v) for s, v in per_tactic.items()}
    y_count = -HDR_LINES * HDR_LINE_H - 0.08
    y_cells = y_count - 0.26

    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usepackage[scaled=0.92]{helvet}")
    w(r"\renewcommand{\familydefault}{\sfdefault}")
    w(r"\usetikzlibrary{calc,backgrounds}")
    w(r"\definecolor{accent}{RGB}{31,84,140}")
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=0pt},"
      r"zcell/.style={draw=black!30,line width=0.5pt,fill=white,anchor=north west,"
      r"align=left,inner xsep=3.4pt,inner ysep=3.0pt,outer sep=0pt,"
      r"text=black!78,font=" + ZOOM_FONT + r"}]")

    # ---- the base matrix: the site's design, shape only --------------------
    col_x = {}
    for i, t in enumerate(tactics):
        s = t["x_mitre_shortname"]
        x = i * (col_w + COL_GAP)
        col_x[s] = x
        is_ex = s == EXAMPLE_TACTIC
        colour = "accent" if is_ex else "black!82"
        stacked = r"\\".join(esc(p) for p in t["name"].split())
        w(r"\node[anchor=north,align=center,text=%s,font=%s] at (%.3f,0) {%s};"
          % (colour, HDR_FONT, x + col_w / 2, stacked))
        w(r"\node[anchor=north,text=black!55,font=%s] at (%.3f,%.3f) {%d techniques};"
          % (CNT_FONT, x + col_w / 2, y_count, counts[s]))
        for k, tech in enumerate(per_tactic[s]):
            tid = ext_id(tech)
            cy = y_cells - k * CELL_H
            hit = is_ex and tid == EXAMPLE_TECHNIQUE
            fill = "accentlight!60" if hit else "white"
            border = "accent" if hit else "black!30"
            w(r"\draw[%s,line width=%.2fpt,fill=%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
              % (border, 0.6 if hit else 0.35, fill, x, cy - CELL_H, x + col_w, cy))
            if subs_of.get(tid):
                tab = "accent!70" if hit else "black!30"
                w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
                  % (tab, x + col_w - TAB_W, cy - CELL_H, x + col_w, cy))

    # ---- the zoom-region box around Initial Access -------------------------
    ia_x = col_x[EXAMPLE_TACTIC]
    ia_n = counts[EXAMPLE_TACTIC]
    box = (ia_x - 0.06, y_cells + 0.06,
           ia_x + col_w + 0.06, y_cells - ia_n * CELL_H - 0.06)
    w(r"\draw[accent,line width=0.8pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % box)

    matrix_bottom = y_cells - max(counts.values()) * CELL_H
    z1_top = matrix_bottom - Z1_DROP

    # ---- zoom 1: the Initial Access techniques, site-style cells -----------
    phish = None
    for k, tech in enumerate(per_tactic[EXAMPLE_TACTIC]):
        tid = ext_id(tech)
        n_subs = len(subs_of.get(tid, []))
        hit = tid == EXAMPLE_TECHNIQUE
        name = f"z1r{k}"
        style = ("zcell,draw=accent,line width=0.7pt,fill=accentlight!45,text=accent"
                 if hit else "zcell")
        at = ("(%.3f,%.3f)" % (Z1_X, z1_top)) if k == 0 else f"(z1r{k-1}.south west)"
        suffix = (r" {%s(%d)}" % (SUBCNT_FONT, n_subs)) if n_subs else ""
        w(r"\node[%s,text width=%.3fcm] (%s) at %s {%s%s};"
          % (style, Z1_W - 0.34 - ZTAB_W, name, at, esc(tech["name"]), suffix))
        if n_subs:
            tab = "accent!70" if hit else "black!30"
            w(r"\fill[%s] ($(%s.north east)+(-%.3f,0)$) rectangle (%s.south east);"
              % (tab, name, ZTAB_W, name))
        if hit:
            phish = name
    w(r"\node[anchor=south west,text=black!55,font=%s] at ($(z1r0.north west)+(0,0.10)$)"
      r" {the techniques of one tactic};" % TAG_FONT)

    # ---- zoom 2: the sub-techniques decompose out to the right -------------
    # (the site's click-the-tab expansion: the stack sits against the cell,
    # behind a dark spine bracket, straddling the technique row)
    subs = subs_of[EXAMPLE_TECHNIQUE]
    n_sub = len(subs)
    j_hit = next(j for j, sub in enumerate(subs) if ext_id(sub) == EXAMPLE_SUB)
    for j, sub in enumerate(subs):
        hit = ext_id(sub) == EXAMPLE_SUB
        name = f"z2r{j}"
        style = ("zcell,draw=accent,line width=0.7pt,fill=accentlight!45,text=accent"
                 if hit else "zcell")
        at = (r"($(%s.north east)+(%.3f,%.3f)$)" % (phish, SPINE_W, Z2_RISE)) \
            if j == 0 else f"(z2r{j-1}.south west)"
        w(r"\node[%s,text width=%.3fcm] (%s) at %s {%s};"
          % (style, Z2_W - 0.34, name, at, esc(sub["name"])))
    w(r"\fill[black!55] ($(z2r0.north west)+(-%.3f,0.05)$) rectangle"
      r" ($(z2r%d.south west)+(0,-0.05)$);" % (SPINE_W, n_sub - 1))
    w(r"\node[anchor=south west,text=black!55,font=%s] at ($(z2r0.north west)+(0,0.12)$)"
      r" {the sub-techniques of one technique};" % TAG_FONT)

    # ---- zoom 3: the technique page's Procedure Examples table -------------
    tw3 = Z3_W - 0.36
    w(r"\node[anchor=north west,text=accent,font=%s] (p0) at"
      r" ($(z2r%d.north east)+(%.3f,-0.02)$) {Procedure Examples};"
      % (PROC_TITLE_FONT, j_hit, Z3_DX))
    prev = "p0"
    for m, (gid, gname, _typ, desc) in enumerate(proc_rows, start=1):
        w(r"\node[anchor=north west,align=left,text width=%.3fcm,text=black!72,"
          r"font=%s] (p%d) at ($(%s.south west)+(0,-0.16)$)"
          r" {{\color{black!48}%s}\enspace{\bfseries %s}\enspace %s};"
          % (tw3, PROC_FONT, m, prev, esc(gid), esc(gname), clean_desc(desc)))
        prev = f"p{m}"
    w(r"\node[anchor=north west,text=black!55,font=%s] (pend) at"
      r" ($(%s.south west)+(0,-0.16)$)"
      r" {\ldots\enspace %d procedure examples on the technique page,};"
      % (PROC_FONT, prev, n_procs))
    w(r"\node[anchor=north west,text=black!55,font=%s] (pend2) at"
      r" ($(pend.south west)+(0,-0.06)$)"
      r" {alongside its mitigations and detection guidance};" % PROC_FONT)
    w(r"\draw[black!35,line width=0.5pt] ($(p0.north west)+(-0.18,0.14)$) rectangle"
      r" ($(pend2.south west)+(%.3f,-0.14)$);" % (Z3_W - 0.18))
    w(r"\node[anchor=south west,text=black!55,font=%s] at"
      r" ($(p0.north west)+(-0.18,0.24)$)"
      r" {the procedures of one sub-technique: its page};" % TAG_FONT)

    # ---- the lenses, behind everything -------------------------------------
    w(r"\begin{scope}[on background layer]")
    w(r"\fill[black!6] (%.3f,%.3f) -- (%.3f,%.3f) -- (z1r0.north east) --"
      r" (z1r0.north west) -- cycle;" % (box[0], box[3], box[2], box[3]))
    w(r"\draw[black!30,line width=0.4pt] (%.3f,%.3f) -- (z1r0.north west);"
      % (box[0], box[3]))
    w(r"\draw[black!30,line width=0.4pt] (%.3f,%.3f) -- (z1r0.north east);"
      % (box[2], box[3]))
    w(r"\fill[black!6] (z2r%d.north east) -- (z2r%d.south east) --"
      r" ($(p0.north west)+(-0.18,-0.42)$) -- ($(p0.north west)+(-0.18,0.14)$)"
      r" -- cycle;" % (j_hit, j_hit))
    w(r"\end{scope}")

    w(r"\end{tikzpicture}")
    w(r"\end{document}")

    facts = {
        "tactics": n,
        "techniques_total": sum(counts.values()),
        "count_min": min(counts.values()),
        "count_max": max(counts.values()),
        "initial_access": counts[EXAMPLE_TACTIC],
        "example_subs": n_sub,
        "procedure_examples": n_procs,
        "procedure_rows_shown": [f"{g} {nm}" for g, nm, _t, _d in proc_rows],
    }
    return "\n".join(L) + "\n", facts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    tactics, per_tactic, subs_of, proc_rows, n_procs = load()
    tex, facts = emit(tactics, per_tactic, subs_of, proc_rows, n_procs)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUT_DIR / f"{STEM}.tex"
    tex_path.write_text(tex)
    print(f"wrote {tex_path.relative_to(REPO)}")
    for k, v in facts.items():
        print(f"  {k}: {v}")

    if not args.no_compile:
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{STEM}.tex"],
            cwd=OUT_DIR, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:])
            raise SystemExit("pdflatex failed")
        for suffix in (".aux", ".log"):
            (OUT_DIR / f"{STEM}{suffix}").unlink(missing_ok=True)
        print(f"wrote {(OUT_DIR / (STEM + '.pdf')).relative_to(REPO)}")


if __name__ == "__main__":
    main()
