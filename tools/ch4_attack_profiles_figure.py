#!/usr/bin/env python3
"""Dissertation figure: the section 4.2 zoom --- the attack graph split by
objective into four attack profiles, each panel drawing only the edges its
own attack flows drew.

The zoom into Figure 4.1's second arrow ("split by objective", from Attack
graph to Attack profiles). Two takeaways, nothing else:

  T1  each of the 38 attack flows is assigned one objective by what the
      attacker achieved (c1-c4, counts read from the classification);
  T2  each panel draws only the tactic-to-tactic edges its own attack flows
      drew, counted the way section 4.1 counts them for the attack graph, so
      the profiles differ in which edges exist and how often they recur; the
      attack graph is also run as a fifth profile, the aggregate. The
      profile's zero-weight pairs (section 4.3: the attack graph induced on the
      profile's techniques, pairs its own flows never draw) are not drawn.

Words: the attack graph and the profiles have EDGES; "transition" is reserved
for the Petri net (lead-session ruling 2026-09-25), so it appears on no mark
here. The Petri-net artefacts are read only for the cross-check.

Form: small multiples of one tactic-by-tactic matrix per profile (row = the
tactic an attack flow moves from, column = the tactic it moves to, both in
ATT&CK kill-chain order; a cell's grey = the number of the profile's flows
drawing that edge). Chosen over the recommended arc rows because the
data is dense: the aggregate draws 122 of the 210 possible ordered tactic
pairs (58 %), 57 of them backward in the kill chain, and arcs at that density
read as texture; a matrix keeps presence and recurrence cell-for-cell
comparable across panels (Ghoniem, Fekete & Castagliola 2004 on matrices vs
node-link for dense graphs). Identical layout in every panel; tactic labels
once per grid row, and one shared band of column labels between the two grid
rows so every panel has its column names beside it; empty cells white on a
chrome grid; the column of the tactic that names the profile's objective
(exfiltration for c1, impact for c2, both for c3; none for c4 or the attack
graph) outlined in the one accent. Scrutiny rounds 1-2, 2026-09-25.

The edge sets are computed from the attack graph exactly as section 4.1
builds it: technique edges rolled up to (source tactic, target tactic) pairs,
same-tactic pairs dropped, weight = distinct attack flows drawing the pair ---
restricted to the profile's own flows. Cross-checked against the Petri-net
artefacts (data/ogasp/petri/*_structural.json), whose transitions are these
edges: the flow-backed transitions (raw numerator > 0) must equal the computed
edge set with the same backing flows, or the build fails. The nets also carry
zero-weight transitions (the profile's structure is the attack graph induced
on the profile's techniques, so it includes edges only other profiles' flows
drew); those are counted and printed, not drawn.

House style: tools/ch4_overview_figure.py (900 px -> \\textwidth through
Chromium, three type sizes, greys + one accent, type-floor check).

Usage:
  PYTHONPATH=src python tools/ch4_attack_profiles_figure.py
      [--out-dir DIR] [--stem STEM] [--png] [--no-pdf]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
from _tactic_axis import load_axis  # noqa: E402
from pipeline_ladder_figure import (  # noqa: E402  the artefact readers
    OBJECTIVE_TACTICS, PETRI_DIR, PROFILE_CODE, PROFILE_LABEL, PROFILE_ORDER, SUB,
    load_classes, load_gap, load_net,
)

GASP_DIR = REPO / "data" / "gasp"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-2a_attack_profiles"
WIDTH_CM = 16.058          # \textwidth, measured (455.244 pt)
PX = 900
FACE_SCALE = 0.92
FLOOR_PT = 7.95

INK, INK2, FAINT, ACCENT = "#333", "#6e6e6e", "#b0b0b0", "#1f548c"
CHROME = "#ececec"         # the cell grid: fainter than the faintest data
# the recurrence ramp: attack flows that drew the edge
BINS = ((1, 1, "1", "#bdbdbd"), (2, 2, "2", "#8c8c8c"),
        (3, 4, "3–4", "#5c5c5c"), (5, 10 ** 6, "5 or more", "#262626"))

AGG = "aggregate"
# reading order: the attack graph first (the zoom's input), then c1-c4
PANELS = (AGG,) + PROFILE_ORDER
# the objective an attack flow achieved, as a column (c4 achieved none; the
# aggregate is not defined by an objective). OBJECTIVE_TACTICS gives c4
# command and control, the tactic its flows end in, which is not an objective.
OBJ_COLUMNS = {p: (() if p == "objective_none_c2" else OBJECTIVE_TACTICS[p]) for p in PROFILE_ORDER}
OBJ_COLUMNS[AGG] = ()

STYLE = f"""
  html, body {{ margin:0; background:#fff; }}
  svg {{ display:block; font-family: "Nimbus Sans", "TeX Gyre Heros", Helvetica, Arial, sans-serif; }}
  text {{ fill:{INK}; }}
  .title {{ font-size:19px; font-weight:bold; }}
  .lbl   {{ font-size:17px; }}
  .sm    {{ font-size:15.5px; fill:{INK2}; }}
  .tick  {{ font-size:15.5px; }}
  .acc   {{ fill:{ACCENT}; }}
  .obj   {{ fill:none; stroke:{ACCENT}; stroke-width:1.8; }}
"""
SIZES = {"title": 19, "lbl": 17, "sm": 15.5, "tick": 15.5}
# (the codes' subscripts print at 14.5 px = 7.97 pt nominal, just over the floor)


class SVG:
    def __init__(self):
        self.parts: list[str] = []
        self.sizes: list[float] = []

    def add(self, s: str):
        self.parts.append(s)

    def text(self, x, y, s, cls="lbl", anchor="start", extra="", raw=False):
        self.sizes.append(SIZES[cls.split()[0]])
        a = "" if anchor == "start" else f' text-anchor="{anchor}"'
        if not raw:
            s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}"{a}{extra}>{s}</text>')

    def rect(self, x0, y0, w, h, fill, extra=""):
        self.add(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}"{extra}/>')


def shade(n: int) -> str:
    for lo, hi, _lab, col in BINS:
        if lo <= n <= hi:
            return col
    raise ValueError(n)


# ------------------------------------------------------------------ the data --
def tactic_edges(gap, flows: set[str]) -> dict[tuple[str, str], set[str]]:
    """Section 4.1's rule, on a subset of the flows: every technique edge a flow
    in `flows` drew, rolled up to its (source tactic, target tactic) pair;
    same-tactic pairs dropped; the pair keeps the set of flows drawing it."""
    nodes = gap["nodes"]
    out: dict[tuple[str, str], set[str]] = defaultdict(set)
    for e in gap["edges"]:
        fs = set(e["flow_ids"]) & flows
        if not fs:
            continue
        a, b = nodes[e["source_id"]]["primary_tactic"], nodes[e["target_id"]]["primary_tactic"]
        if a != b:
            out[(a, b)] |= fs
    return dict(out)


def profiles(gap, cls):
    """panel -> (its flows, its tactic edges), with the drift guards."""
    if set(cls.values()) != set(PROFILE_ORDER):
        raise SystemExit(f"objective classes drifted: {sorted(set(cls.values()))} vs {PROFILE_ORDER}")
    drew = {f for n in gap["nodes"].values() for f in n["flow_ids"]}
    if drew != set(cls):
        raise SystemExit(f"classification and attack graph disagree on the flows: "
                         f"{sorted(drew ^ set(cls))}")
    out = {}
    for p in PANELS:
        flows = set(cls) if p == AGG else {f for f, c in cls.items() if c == p}
        if p != AGG:
            gasp = json.loads((GASP_DIR / f"gasp_{p}.json").read_text())
            if set(gasp["provenance"]["flow_ids"]) != flows:
                raise SystemExit(f"{p}: classification.csv and gasp_{p}.json list different flows")
        out[p] = (flows, tactic_edges(gap, flows))
    return out


def cross_check(prof) -> dict[str, dict]:
    """Against the Petri-net artefacts: the flow-backed transitions (raw
    numerator > 0) must be exactly the computed edge set, backed by the same flows.
    Zero-weight transitions are reported, not failed."""
    report = {}
    for p, (_flows, T) in prof.items():
        net = load_net(p)
        backed, zero = {}, []
        for t in net["transitions"]:
            key = (t["src_tactic"], t["dst_tactic"])
            raw = t["weights"]["raw"]
            if raw["numerator"] > 0:
                backed[key] = set(raw["backing_flow_ids"])
            else:
                zero.append(key)
        if set(backed) != set(T):
            raise SystemExit(f"{p}: flow-backed net transitions disagree with the attack-graph edges: "
                             f"only net {sorted(set(backed) - set(T))}, only graph {sorted(set(T) - set(backed))}")
        bad = [k for k in T if backed[k] != T[k]]
        if bad:
            raise SystemExit(f"{p}: backing flows disagree on {bad[:5]}")
        dedup_zero = sum(1 for t in net["transitions"] if t["weights"]["operator_dedup"]["numerator"] == 0)
        report[p] = {"net": len(net["transitions"]), "backed": len(backed), "zero": len(zero),
                     "zero_dedup": dedup_zero, "places": len(net["places"])}
    return report


# ------------------------------------------------------------------ drawing --
def code(p: str, size: float = 18, sub_size: float = 14.5) -> str:
    """A profile code set as chapter 5 sets it: math-italic c, upright
    subscript (a digit, or 'agg' for the aggregate)."""
    sub = "agg" if p == AGG else str(PROFILE_CODE[p])
    return (f'<tspan style="font-family:\'Nimbus Roman\',\'Times New Roman\',serif;'
            f'font-style:italic;font-size:{size}px">c</tspan>'
            f'<tspan dy="4" style="font-family:\'Nimbus Roman\',\'Times New Roman\',serif;'
            f'font-size:{sub_size}px">{sub}</tspan><tspan dy="-4"> </tspan>')   # the reset needs a glyph to apply


def emit(prof, axis) -> tuple[str, float, float]:
    svg = SVG()
    order = axis.matrix_order
    n = len(order)
    idx = {t: i for i, t in enumerate(order)}
    svg.sizes.append(14.5)                    # the codes' subscripts (see code())

    GX = 182                      # right edge of the row-label gutter
    GAP = 16                      # between panels
    x_first = GX + 8
    M = (PX - 2 - x_first - 2 * GAP) / 3
    cell = M / n
    COLS = [x_first + k * (M + GAP) for k in range(3)]

    # Layout, top to bottom: grid-row-1 titles; grid row 1; ONE band of column
    # labels shared by both grid rows (below row 1, above row 2: every panel
    # has its column names next to it, for no extra band); grid row 2; its
    # titles beneath it (the labels must touch the matrix they name).
    TITLE1_H = 48                 # two title lines above each top-row panel (room for the agg descenders)
    LAB_H = 170                   # vertical tactic names (longest ~ 160 px)
    y_t1 = 4
    y_m1 = y_t1 + TITLE1_H
    y_lab = y_m1 + M + 6          # top of the shared label band
    y_m2 = y_lab + LAB_H
    y_t2 = y_m2 + M + 4
    height = y_t2 + 48

    slots = [(COLS[0], y_m1), (COLS[1], y_m1), (COLS[2], y_m1), (COLS[0], y_m2), (COLS[1], y_m2)]

    # row labels, once per grid row: the tactic moved FROM
    for ym in (y_m1, y_m2):
        for t in order:
            svg.text(GX, ym + (idx[t] + 0.5) * cell + 5.3, axis.label[t], "tick", anchor="end")
    # column labels, once per grid column, in the shared band: the tactic moved TO
    # (centred in the band so they sit equally close to both rows)
    for x0 in COLS:
        for t in order:
            cx = x0 + (idx[t] + 0.5) * cell + 5.3
            yc = y_lab + LAB_H / 2
            svg.text(cx, yc, axis.label[t], "tick", anchor="middle",
                     extra=f' transform="rotate(-90 {cx:.1f} {yc:.1f})"')
    # the reading of a cell, once, in the gutter beside the label band
    yc = y_lab + LAB_H / 2
    svg.text(GX, yc - 4, "from the row's tactic", "sm", anchor="end")
    svg.text(GX, yc + 16, "to the column's tactic", "sm", anchor="end")

    for p, (x0, ym) in zip(PANELS, slots):
        flows, T = prof[p]
        total = len(prof[AGG][0])
        if p == AGG:
            svg.text(x0, y_t1 + 17, "The attack graph", "lbl", extra=' font-weight="bold"')
            svg.text(x0, y_t1 + 37, f'{len(flows)} attack flows \u00b7 run as {code(p, 16.5)}', "sm", raw=True)
        else:
            head = f'{code(p)}<tspan font-weight="bold">{PROFILE_LABEL[p]}</tspan>'
            sub = f"{len(flows)} of the {total} attack flows"
            if ym == y_m1:
                ty = y_t1 + (TITLE1_H - 44) + 13      # bottom-aligned with the attack graph's
                svg.text(x0, ty, head, "lbl", raw=True)
                svg.text(x0, ty + 20, sub, "sm")
            else:
                svg.text(x0, y_t2 + 17, head, "lbl", raw=True)
                svg.text(x0, y_t2 + 37, sub, "sm")
        obj = set(OBJ_COLUMNS[p])
        # the hairline frame, and a chrome grid so a cell can be found by eye
        for k in range(1, n):
            svg.add(f'<path d="M{x0 + k * cell:.2f},{ym:.2f} V{ym + M:.2f} M{x0:.2f},{ym + k * cell:.2f} H{x0 + M:.2f}" '
                    f'stroke="{CHROME}" stroke-width="1" fill="none"/>')
        g = 1.2                                   # white seam between filled cells
        for r in order:
            for c in order:
                k = len(T.get((r, c), ())) if r != c else 0   # same tactic: never an edge
                if k:
                    x, y = x0 + idx[c] * cell, ym + idx[r] * cell
                    svg.rect(x + g / 2, y + g / 2, cell - g, cell - g, shade(k))
        svg.add(f'<rect x="{x0:.2f}" y="{ym:.2f}" width="{M:.2f}" height="{M:.2f}" fill="none" '
                f'stroke="{FAINT}" stroke-width="1.2"/>')
        for c in obj:                             # edges into exfiltration / impact, outlined
            svg.add(f'<rect class="obj" x="{x0 + idx[c] * cell:.2f}" y="{ym - 1:.2f}" '
                    f'width="{cell:.2f}" height="{M + 2:.2f}"/>')

    # the key, in the sixth slot: the one scale the cells need, and the outline
    kx, ky = COLS[2], y_m2
    svg.text(kx, ky + 17, "Attack flows that", "lbl")
    svg.text(kx, ky + 37, "drew the edge", "lbl")
    sw = 17
    for k, (_lo, _hi, lab, col) in enumerate(BINS):
        xx, yy = kx + (k % 2) * 96, ky + 54 + (k // 2) * 25
        svg.rect(xx, yy, sw, sw, col)
        svg.text(xx + sw + 8, yy + 13.5, lab, "tick")
    yy = ky + 54 + 2 * 25 + 16
    svg.add(f'<rect class="obj" x="{kx + 5:.1f}" y="{yy - 2:.1f}" width="{sw * 0.6:.1f}" height="{sw + 41}"/>')
    for k, ln in enumerate(("outlined: the column of the", "tactic that names the", "profile's objective")):
        svg.text(kx + sw + 8, yy + 13.5 + 19 * k, ln, "tick")
    yy += 13.5 + 19 * 2 + 30
    # the assignment rule, once (the cold readers twice doubted it)
    for k, ln in enumerate(("each attack flow sits in one", "profile, by the objective its", "source reports record")):
        svg.text(kx, yy + 19 * k, ln, "sm")

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>fig:attack-profiles --- the attack graph split by objective (generated by tools/ch4_attack_profiles_figure.py; do not hand-edit)</title>
<style>{STYLE}
  body {{ width:{PX}px; }}
  @media print {{ @page {{ size:{WIDTH_CM}cm {WIDTH_CM * height / PX:.3f}cm; margin:0; }} body {{ width:{WIDTH_CM}cm; }} svg {{ width:{WIDTH_CM}cm; height:{WIDTH_CM * height / PX:.3f}cm; }} }}
</style></head>
<body>
<svg id="fig" viewBox="0 0 {PX} {height:.1f}" width="{PX}" height="{height:.1f}" xmlns="http://www.w3.org/2000/svg">
{chr(10).join(svg.parts)}
</svg>
</body></html>
"""
    floor = min(svg.sizes) * (WIDTH_CM / 2.54 * 72) / PX / FACE_SCALE
    return html, WIDTH_CM * height / PX, floor


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR, help="mocks go to the scratchpad, not the thesis")
    ap.add_argument("--stem", default=STEM)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    gap, gap_order = load_gap()
    axis = load_axis()
    axis.check_against(gap_order)
    cls = load_classes()
    prof = profiles(gap, cls)
    net = cross_check(prof)

    html, h_cm, floor = emit(prof, axis)
    if floor < FLOOR_PT:
        raise SystemExit(f"smallest type prints at {floor:.2f} pt (< {FLOOR_PT} pt floor)")
    a.out_dir.mkdir(parents=True, exist_ok=True)
    html_path = a.out_dir / f"{a.stem}.html"
    html_path.write_text(html)
    print(f"wrote {html_path}")
    h_px = round(PX * h_cm / WIDTH_CM)
    if not a.no_pdf or a.png:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={"width": PX, "height": h_px}, device_scale_factor=2)
            pg.goto(html_path.as_uri())
            pg.wait_for_timeout(300)
            if a.png:
                pg.locator("#fig").screenshot(path=str(a.out_dir / f"{a.stem}.png"))
                print(f"preview {a.out_dir / (a.stem + '.png')}")
            if not a.no_pdf:
                pg.emulate_media(media="print")
                pg.pdf(path=str(a.out_dir / f"{a.stem}.pdf"), width=f"{WIDTH_CM}cm", height=f"{h_cm:.3f}cm",
                       margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                       print_background=True, prefer_css_page_size=False)
                print(f"wrote {a.out_dir / (a.stem + '.pdf')}")
            b.close()

    # the facts, for the caption and the prose
    order = axis.matrix_order
    print("--- facts")
    for p in PANELS:
        flows, T = prof[p]
        fwd = sum(1 for (s, d) in T if order.index(s) < order.index(d))
        bins = Counter(next(lab for lo, hi, lab, _ in BINS if lo <= len(v) <= hi) for v in T.values())
        tactics = {t for key in T for t in key}
        code = "c_agg" if p == AGG else f"c{PROFILE_CODE[p]}"
        r = net[p]
        print(f"  {code:5s} {len(flows):2d} flows | {len(T):3d} tactic edges ({fwd} forward, {len(T) - fwd} backward) "
              f"over {len(tactics)} tactics | max {max(len(v) for v in T.values())} flows on one edge | "
              + ", ".join(f"{lab}: {bins.get(lab, 0)}" for *_, lab, _c in BINS)
              + f" | Petri net: {r['net']} transitions = {r['backed']} flow-backed (= the edges, same flows) + {r['zero']} zero-weight"
              f" ({r['zero_dedup']} zero under operator_dedup), {r['places']} places")
    print(f"  {WIDTH_CM} x {h_cm:.2f} cm; smallest type {floor:.2f} pt nominal")


if __name__ == "__main__":
    main()
