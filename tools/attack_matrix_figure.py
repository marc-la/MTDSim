#!/usr/bin/env python3
"""Dissertation figure: the ATT&CK Enterprise matrix and the hierarchy
beneath one cell (ch3 subsec:attack, fig:attack-matrix).

The meet-in-the-middle design (Marc's ruling trail, 2026-09-02): the BASE
matrix is drawn to the design of attack.mitre.org/matrices/enterprise ---
fifteen tactic columns, each headed by its name over an "N techniques" count,
one cell per technique beneath --- but shape only, no technique names. The
ZOOM cascade reuses the site's own gestures at readable size:

  zoom 1  an accent box marks the zoomed region (Initial Access); a lens
          opens its eleven techniques as site-style named cells
  zoom 2  Valid Accounts' four sub-techniques decompose OUT TO THE RIGHT
          behind the site's dark spine bracket (the click-the-tab expansion)
  zoom 3  Domain Accounts opens into its technique PAGE: the Procedure
          Examples table --- real group rows, Volt Typhoon's first (the
          chapter's recurring illustration) --- the procedure level, which
          has no cell in the matrix

Legibility rework (Marc, 2026-10-01: "the reader sees a bunch of lines but
not the titles ... it doesn't scream MITRE besides the shape"). The canvas is
now the portrait typeblock itself, so the \\textwidth inclusion prints every
size at nominal (~1.0x; it was ~0.72x, tactic names at 3.6 pt). Fifteen
columns leave ~29 pt each, too narrow for "Reconnaissance" (~58 pt at 8 pt
bold) set horizontally, so the headers are ROTATED to read upward: name
(wrapped only at spaces) then count, all at 7.5--8 pt. The silhouette is
light grey texture with no side tabs, so the eye lands on the names and the
accent path; a one-line heading names the source and its totals. Each zoom
level carries a tag naming the level (technique, sub-technique, procedure):
since 2026-10-01 (ch3 redraft round 13) the level name alone, so the tags
are the prose's hierarchy words.

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

Style: TikZ, 12 pt base document; canvas 15.95 cm drawn (~456 pt with the
border), included at \\textwidth (455.24 pt), so drawn sizes are printed sizes.
The run prints every type class's printed size and fails under the 7 pt floor.
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

# --- geometry (cm). The canvas is the portrait typeblock itself (\textwidth =
# 455.24 pt = 16.06 cm), so the float's width=\textwidth inclusion scales it by
# ~1.0 and every size below is the printed size (conventions §h). -----------
TEXTWIDTH_PT = 455.24
CANVAS_W = 15.95          # drawn width; 2 pt standalone border each side
COL_GAP = 0.07
CELL_H = 0.04             # a silhouette cell: texture for "many techniques"
HDR_H = 2.16              # rotated header band: fits "Reconnaissance" at 8 pt bold
HDR_GAP = 0.10            # header band to the first cell
HEAD_GAP = 0.12           # heading line to the header band
Z1_X, Z1_W = 0.00, 5.05   # the Initial Access zoom stack
Z1_DROP = 0.50            # matrix bottom to the zoom stack (holds its tag)
ZTAB_W = 0.16             # side tab at zoom size
SPINE_W = 0.20            # the dark bracket behind a sub-technique stack
Z2_W = 3.05               # the sub-technique stack
Z3_DX = 0.55              # sub-technique stack to the procedure card
CARD_PAD = 0.14           # procedure card inner padding

# --- type (nominal pt; printed size = nominal x the inclusion scale, checked
# against the floor after compiling). Two sizes carry the figure: 8 pt names,
# 7.5 pt secondary text; the heading is 9 pt. --------------------------------
TYPE_FLOOR_PT = 7.0
SIZES = {"heading": 9.0, "tactic": 8.0, "count": 7.5, "zoom": 8.0,
         "subcount": 7.5, "tag": 7.5, "proc": 8.0, "proc_title": 8.5}


def font(key: str, extra: str = "") -> str:
    pt = SIZES[key]
    return r"\fontsize{%gpt}{%gpt}\selectfont%s" % (pt, round(pt * 1.18, 2), extra)


HEAD_FONT = font("heading", r"\bfseries")
HDR_FONT = font("tactic", r"\bfseries")
CNT_FONT = font("count", r"\mdseries")
ZOOM_FONT = font("zoom")
SUBCNT_FONT = font("subcount")
TAG_FONT = font("tag", r"\itshape")
PROC_FONT = font("proc")
PROC_TITLE_FONT = font("proc_title", r"\bfseries")


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
    total = sum(counts.values())

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
    # names are ATT&CK proper names: never hyphenated, wrapped only at spaces
    w(r"\hyphenpenalty=10000\exhyphenpenalty=10000")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,every node/.style={inner sep=0pt},"
      r"zcell/.style={draw=black!30,line width=0.5pt,fill=white,anchor=north west,"
      r"align=left,inner xsep=3.4pt,inner ysep=1.6pt,outer sep=0pt,"
      r"text height=1.5ex,text depth=0.42ex,"
      r"text=black!80,font=" + ZOOM_FONT + r"},"
      r"tag/.style={anchor=south west,align=left,text=black!60,font=" + TAG_FONT + r"}]")

    # ---- heading: the figure names its source ------------------------------
    # y = 0 is the top of the cells; the header band and heading sit above it.
    y_head = HDR_GAP + HDR_H + HEAD_GAP
    w(r"\node[anchor=south west,text=black!85,font=%s] at (0,%.3f)"
      r" {MITRE ATT\&CK Enterprise: %d tactics, %d techniques};"
      % (HEAD_FONT, y_head, n, total))

    # ---- the tactic headers: rotated so every name prints at 8 pt ----------
    # Fifteen columns in 16 cm leave ~29 pt each; "Reconnaissance" alone is
    # ~58 pt at 8 pt bold, so horizontal names cannot clear the floor. Each
    # header reads upward from the cells: the name (TeX wraps two-word names
    # to the band), then the technique count.
    col_x = {}
    for i, t in enumerate(tactics):
        s = t["x_mitre_shortname"]
        x = i * (col_w + COL_GAP)
        col_x[s] = x
        is_ex = s == EXAMPLE_TACTIC
        colour = "accent" if is_ex else "black!85"
        w(r"\node[rotate=90,anchor=west,align=left,text width=%.3fcm,"
          r"text=%s,font=%s] at (%.3f,%.3f) {%s\\{%s\color{black!60}%d techniques}};"
          % (HDR_H, colour, HDR_FONT, x + col_w / 2, HDR_GAP,
             esc(t["name"]), CNT_FONT, counts[s]))

    # ---- the silhouette: one light cell per technique, texture only --------
    for s, x in col_x.items():
        is_ex = s == EXAMPLE_TACTIC
        for k, tech in enumerate(per_tactic[s]):
            hit = is_ex and ext_id(tech) == EXAMPLE_TECHNIQUE
            cy = -k * CELL_H
            w(r"\fill[%s] (%.3f,%.3f) rectangle (%.3f,%.3f);"
              % ("accent" if hit else "black!14", x, cy - CELL_H + 0.008,
                 x + col_w, cy))

    # ---- the zoom-region box around Initial Access -------------------------
    ia_x = col_x[EXAMPLE_TACTIC]
    ia_n = counts[EXAMPLE_TACTIC]
    box = (ia_x - 0.05, 0.05, ia_x + col_w + 0.05, -ia_n * CELL_H - 0.05)
    w(r"\draw[accent,line width=0.8pt] (%.3f,%.3f) rectangle (%.3f,%.3f);" % box)

    # the stack drops below the columns it spans, not below the whole matrix:
    # the tall columns (Stealth, Discovery) sit to its right, over empty space
    spanned = [s for s, x in col_x.items() if x < Z1_X + Z1_W and x + col_w > Z1_X]
    z1_top = -max(counts[s] for s in spanned) * CELL_H - Z1_DROP

    # ---- zoom 1: the Initial Access techniques, site-style cells -----------
    ia = per_tactic[EXAMPLE_TACTIC]
    phish = None
    for k, tech in enumerate(ia):
        tid = ext_id(tech)
        n_subs = len(subs_of.get(tid, []))
        hit = tid == EXAMPLE_TECHNIQUE
        name = f"z1r{k}"
        style = ("zcell,draw=accent,line width=0.7pt,fill=accentlight!45,text=accent"
                 if hit else "zcell")
        at = ("(%.3f,%.3f)" % (Z1_X, z1_top)) if k == 0 else f"(z1r{k-1}.south west)"
        suffix = (r" {%s(%d)}" % (SUBCNT_FONT, n_subs)) if n_subs else ""
        w(r"\node[%s,text width=%.3fcm] (%s) at %s {%s%s};"
          % (style, Z1_W - 0.24 - ZTAB_W, name, at, esc(tech["name"]), suffix))
        if n_subs:
            tab = "accent!70" if hit else "black!30"
            w(r"\fill[%s] ($(%s.north east)+(-%.3f,0)$) rectangle (%s.south east);"
              % (tab, name, ZTAB_W, name))
        if hit:
            phish = name
    w(r"\node[tag,text width=%.3fcm] at ($(z1r0.north west)+(0,0.10)$)"
      r" {techniques};" % (Z1_W - 0.1))

    # ---- zoom 2: the sub-techniques decompose out to the right -------------
    # (the site's click-the-tab expansion: the stack sits against the cell,
    # behind a dark spine bracket; its bottom row aligns with the stack's)
    subs = subs_of[EXAMPLE_TECHNIQUE]
    n_sub = len(subs)
    j_hit = next(j for j, sub in enumerate(subs) if ext_id(sub) == EXAMPLE_SUB)
    z2_anchor = max(0, len(ia) - n_sub)
    for j, sub in enumerate(subs):
        hit = ext_id(sub) == EXAMPLE_SUB
        name = f"z2r{j}"
        style = ("zcell,draw=accent,line width=0.7pt,fill=accentlight!45,text=accent"
                 if hit else "zcell")
        at = (r"($(z1r%d.north east)+(%.3f,0)$)" % (z2_anchor, SPINE_W)) \
            if j == 0 else f"(z2r{j-1}.south west)"
        w(r"\node[%s,text width=%.3fcm] (%s) at %s {%s};"
          % (style, Z2_W - 0.24, name, at, esc(sub["name"])))
    w(r"\fill[black!55] ($(z2r0.north west)+(-%.3f,0.05)$) rectangle"
      r" ($(z2r%d.south west)+(0,-0.05)$);" % (SPINE_W, n_sub - 1))
    w(r"\node[tag] at ($(z2r0.north west)+(0,0.10)$)"
      r" {sub-techniques};")

    # ---- zoom 3: the technique page's Procedure Examples table -------------
    # one bordered card, bottom-aligned with the stacks, rows read from the
    # bundle's `uses` relationships; the worked example's row in the accent
    card_left_x = Z1_X + Z1_W + SPINE_W + Z2_W + Z3_DX
    card_w = CANVAS_W - card_left_x
    rows = [r"{\color{accent}%s Procedure Examples}" % PROC_TITLE_FONT]
    for gid, gname, _typ, desc in proc_rows:
        lead = gname == "Volt Typhoon"
        head = (r"{\color{accent}\bfseries %s\enspace %s}" if lead
                else r"{\color{black!60}%s}\enspace{\bfseries %s}") % (esc(gid), esc(gname))
        rows.append(head + r"\enspace " + clean_desc(desc, 120))
    rows.append(r"{\color{black!60}\ldots\enspace %d procedure examples in all}" % n_procs)
    w(r"\node[draw=black!35,line width=0.5pt,fill=white,anchor=south west,align=left,"
      r"text width=%.3fcm,inner sep=%.3fcm,text=black!80,font=%s] (card) at"
      r" ($(z2r%d.south east)+(%.3f,0)$) {%s};"
      % (card_w - 2 * CARD_PAD - 0.02, CARD_PAD, PROC_FONT, n_sub - 1, Z3_DX,
         r"\\[3pt]".join(rows)))
    w(r"\node[tag,text width=%.3fcm] at ($(card.north west)+(0,0.10)$)"
      r" {procedures};" % (card_w - 0.1))

    # ---- the lenses, behind everything -------------------------------------
    w(r"\begin{scope}[on background layer]")
    w(r"\fill[black!6] (%.3f,%.3f) -- (%.3f,%.3f) -- (z1r0.north east) --"
      r" (z1r0.north west) -- cycle;" % (box[0], box[3], box[2], box[3]))
    w(r"\draw[black!30,line width=0.4pt] (%.3f,%.3f) -- (z1r0.north west);"
      % (box[0], box[3]))
    w(r"\draw[black!30,line width=0.4pt] (%.3f,%.3f) -- (z1r0.north east);"
      % (box[2], box[3]))
    w(r"\fill[black!6] (z2r%d.north east) -- (z2r%d.south east) --"
      r" (card.south west) -- (card.north west) -- cycle;" % (j_hit, j_hit))
    w(r"\end{scope}")

    w(r"\end{tikzpicture}")
    w(r"\end{document}")

    facts = {
        "tactics": n,
        "techniques_total": total,
        "count_min": min(counts.values()),
        "count_max": max(counts.values()),
        "initial_access": counts[EXAMPLE_TACTIC],
        "example_subs": n_sub,
        "procedure_examples": n_procs,
        "procedure_rows_shown": [f"{g} {nm}" for g, nm, _t, _d in proc_rows],
    }
    return "\n".join(L) + "\n", facts


def pdf_size_pt(pdf: Path) -> tuple[float, float]:
    """The compiled figure's natural size: its inked extent (gs bbox, the
    house measure) plus the standalone's 2 pt border on each side, which is
    the page box the inclusion scales."""
    out = subprocess.run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=bbox",
                          str(pdf)], capture_output=True, text=True).stderr
    m = re.search(r"%%HiResBoundingBox:\s+([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", out)
    x0, y0, x1, y1 = (float(v) for v in m.groups())
    return x1 - x0 + 4.0, y1 - y0 + 4.0


def type_check(pdf: Path) -> None:
    """Printed type at the float's width=\\textwidth inclusion (conventions §h)."""
    nat_w, nat_h = pdf_size_pt(pdf)
    scale = TEXTWIDTH_PT / nat_w
    print(f"  natural {nat_w:.1f} x {nat_h:.1f} pt; printed at \\textwidth: "
          f"scale {scale:.3f}, height {nat_h * scale / 28.4527:.2f} cm")
    for key, pt in sorted(SIZES.items(), key=lambda kv: kv[1]):
        print(f"    {key:<11} {pt:>4g} pt nominal -> {pt * scale:.2f} pt printed")
    smallest = min(SIZES.values()) * scale
    if smallest < TYPE_FLOOR_PT:
        raise SystemExit(f"type floor breached: {smallest:.2f} pt < {TYPE_FLOOR_PT} pt")


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
        type_check(OUT_DIR / f"{STEM}.pdf")


if __name__ == "__main__":
    main()
