#!/usr/bin/env python3
"""Dissertation figure: the L0–L1 transformation, from one analyst-drawn
Attack Flow to the aggregate APT attack graph (methodology §4.2.1).

Three panels, one shared row-per-tactic axis (kill-chain order, top to bottom):

  (a) one incident as the analyst drew it — a per-flow extract from
      data/gap/flows/, technique nodes carrying their tactic, AND/OR
      operators kept, procedures/notes already stripped;
  (b) the technique-level aggregate over every flow — one dot per technique
      in its tactic's row, one curve per technique->technique edge, faded by
      how many incidents drew it (the "88 % single-incident" thinness);
  (c) the tactic-level aggregate — one node per tactic, arcs weighted by the
      summed observation count of the technique edges that roll up into that
      transition (forward transitions bulge right, backward bulge left,
      self-loops drawn as small loops), node area by the number of flows in
      which the tactic occurs (the pre-intrusion sparsity).

The exemplar flow's own edges are tinted through (b) and (c) so the reader
can see where one incident lands in the aggregate.

Everything is computed from the artefacts — no corpus numbers are hard-coded
(the numbers the caption quotes are printed to stdout for cross-checking).

Usage:
  python tools/l1_attack_graph_figure.py [--flow <flow_id>] [--min-obs N]
      [--no-compile]

Style: TikZ at the document's 12 pt base so \scriptsize / \tiny land at
8 pt / 6 pt in the thesis; greys carry weight (one sequential ramp), one
accent tints the exemplar; no colour carries a category. Text is set in
the document font, so the figure reads as part of the page.

Writes docs/thesis/figures/l1_attack_graph.tex (TikZ, standalone) and, unless
--no-compile, docs/thesis/figures/l1_attack_graph.pdf via pdflatex.
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
GAP_JSON = REPO / "data" / "gap" / "gap_v0.5.json"
FLOWS_DIR = REPO / "data" / "gap" / "flows"
OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "l1_attack_graph"

# ATT&CK v19.1 display names for the tactic ids the GAP carries. Sentence
# case for the figure; "Defense Impairment" keeps ATT&CK's own spelling as
# the name of the tactic (it is looked up, not translated).
TACTIC_LABEL = {
    "reconnaissance": "Reconnaissance",
    "resource-development": "Resource development",
    "initial-access": "Initial access",
    "execution": "Execution",
    "persistence": "Persistence",
    "privilege-escalation": "Privilege escalation",
    "stealth": "Stealth",
    "defense-impairment": "Defense impairment",
    "credential-access": "Credential access",
    "discovery": "Discovery",
    "lateral-movement": "Lateral movement",
    "collection": "Collection",
    "command-and-control": "Command and control",
    "exfiltration": "Exfiltration",
    "impact": "Impact",
}

# --- geometry (cm) ---------------------------------------------------------
ROW_PITCH = 0.64            # vertical distance between tactic rows
A_X = 1.95                  # centre of the (a) node column
A_W = 3.9                   # (a) node width
LABEL_X = 6.95              # right edge of the tactic labels
COUNT_X = 7.32              # centre of the flows-present count column
B_X0, B_X1 = 7.7, 11.15     # (b) dot band
C_X = 12.85                 # (c) node column
C_FWD_BULGE = 2.95          # max rightward bulge of a forward arc
C_BWD_BULGE = 1.45          # max leftward bulge of a backward arc

ACCENT = "accent"           # tikz colour name for the exemplar tint


def _esc(s: str) -> str:
    return (s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
             .replace("_", r"\_"))


def _short(name: str, n: int) -> str:
    return name if len(name) <= n else name[: n - 1].rstrip() + "\\ldots"


def load() -> tuple[dict, list[str]]:
    gap = json.loads(GAP_JSON.read_text())
    layer_of: dict[str, int] = {}
    for n in gap["nodes"].values():
        layer_of[n["primary_tactic"]] = n["tactic_layer"]
    order = sorted(layer_of, key=layer_of.get)
    return gap, order


def stats(gap: dict, order: list[str]) -> dict:
    nodes = gap["nodes"]
    tac = lambda t: nodes[t]["primary_tactic"]  # noqa: E731
    techs_by_tactic: dict[str, list[str]] = defaultdict(list)
    flows_by_tactic: dict[str, set] = defaultdict(set)
    for tid, n in nodes.items():
        techs_by_tactic[n["primary_tactic"]].append(tid)
        flows_by_tactic[n["primary_tactic"]].update(n["flow_ids"])
    for t in techs_by_tactic:   # neutral, reproducible order (technique id)
        techs_by_tactic[t].sort()
    trans_obs: Counter = Counter()
    trans_flows: dict[tuple, set] = defaultdict(set)
    for e in gap["edges"]:
        k = (tac(e["source_id"]), tac(e["target_id"]))
        trans_obs[k] += e["observation_count"]
        trans_flows[k].update(e["flow_ids"])
    single = sum(1 for e in gap["edges"] if e["observation_count"] == 1)
    return {
        "techs_by_tactic": techs_by_tactic,
        "flows_by_tactic": {t: len(s) for t, s in flows_by_tactic.items()},
        "trans_obs": trans_obs,
        "trans_flows": {k: len(v) for k, v in trans_flows.items()},
        "n_nodes": len(nodes), "n_edges": len(gap["edges"]),
        "n_single": single, "n_flows": gap["source_flow_count"],
        "n_tactics": len(order), "n_trans": len(trans_obs),
        "n_trans_single": sum(1 for v in trans_obs.values() if v == 1),
        "n_trans_multi_flow": sum(1 for v in trans_flows.values() if len(v) >= 2),
        "obs_total": sum(trans_obs.values()),
    }


def load_flow(flow_id: str) -> dict:
    return yaml.safe_load((FLOWS_DIR / f"{flow_id}.yaml").read_text())


def flow_rows(flow: dict) -> list[list[str]]:
    """Topological rows for the (a) chain: a list of rows, each a list of node
    ids, longest-path layering from the start refs. Kept generic so a
    different exemplar lays out without hand placement."""
    nodes = {n["id"]: n for n in flow["nodes"]}
    pred: dict[str, list[str]] = defaultdict(list)
    for e in flow["edges"]:
        pred[e["target"]].append(e["source"])
    depth: dict[str, int] = {}
    # longest-path layering (the flow extracts are DAGs bar one; guard cycles)
    def d(n: str, seen: frozenset) -> int:
        if n in depth:
            return depth[n]
        if n in seen:
            return 0
        v = 0 if not pred[n] else 1 + max(d(p, seen | {n}) for p in pred[n])
        depth[n] = v
        return v
    for n in nodes:
        d(n, frozenset())
    rows: dict[int, list[str]] = defaultdict(list)
    for n, v in depth.items():
        rows[v].append(n)
    # parallel branches at one depth are stacked as sub-rows (full width each)
    # so technique names stay legible in a narrow column
    out: list[list[str]] = []
    for k in sorted(rows):
        for nid in sorted(rows[k], key=lambda x: (nodes[x]["kind"] != "action", x)):
            out.append([nid])
    return out


def edge_style(obs: int, max_obs: int) -> tuple[float, int]:
    """(line width in pt, grey level 0..100 where 100 = black) — a single
    sequential ramp so weight reads as one variable."""
    frac = (obs - 1) / max(max_obs - 1, 1)
    frac = math.sqrt(min(max(frac, 0.0), 1.0))  # lift the mid-weights
    return 0.25 + frac * 1.6, int(16 + frac * 74)


def emit(gap: dict, order: list[str], st: dict, flow: dict, min_obs: int) -> str:
    nodes = gap["nodes"]
    tac = lambda t: nodes[t]["primary_tactic"]  # noqa: E731
    row_y = {t: -i * ROW_PITCH for i, t in enumerate(order)}
    y_top, y_bot = row_y[order[0]], row_y[order[-1]]

    ex_id = flow["flow_id"]
    ex_tech_edges = {(e["source_id"], e["target_id"]) for e in gap["edges"]
                     if ex_id in e["flow_ids"]}
    ex_trans = {(tac(s), tac(t)) for s, t in ex_tech_edges}
    ex_techs = {tid for tid, n in nodes.items() if ex_id in n["flow_ids"]}

    L: list[str] = []
    w = L.append
    w(r"\documentclass[tikz,12pt,border=2pt]{standalone}")
    w(r"\usepackage[T1]{fontenc}")
    w(r"\usetikzlibrary{arrows.meta,positioning,calc,shapes.geometric}")
    w(r"\definecolor{accent}{RGB}{31,84,140}")     # one tint, print-safe
    w(r"\definecolor{accentlight}{RGB}{200,214,232}")
    w(r"\begin{document}")
    w(r"\begin{tikzpicture}[x=1cm,y=1cm,>={Stealth[length=1.6mm]},"
      r" every node/.style={font=\scriptsize}]")

    # ---- shared row axis: labels + flows-present count -------------------
    w(r"\node[anchor=south east,font=\tiny,text=black!60] at (%.2f,%.2f) {tactic};"
      % (LABEL_X, y_top + 0.28))
    w(r"\node[anchor=south,font=\tiny,text=black!60,align=center] at (%.2f,%.2f) {flows\\of %d};"
      % (COUNT_X, y_top + 0.28, st["n_flows"]))
    for t in order:
        y = row_y[t]
        w(r"\node[anchor=east] at (%.2f,%.2f) {%s};" % (LABEL_X, y, _esc(TACTIC_LABEL[t])))
        w(r"\node[font=\scriptsize,text=black!60] at (%.2f,%.2f) {%d};"
          % (COUNT_X, y, st["flows_by_tactic"][t]))
        # faint row rule under the dot band, so a row reads as a row
        w(r"\draw[black!12,line width=0.2pt] (%.2f,%.2f) -- (%.2f,%.2f);"
          % (B_X0 - 0.15, y, B_X1 + 0.15, y))

    # ---- (b) technique-level aggregate ---------------------------------
    pos: dict[str, tuple[float, float]] = {}
    for t in order:
        techs = st["techs_by_tactic"][t]
        n = len(techs)
        span = B_X1 - B_X0
        pitch = span / max(n - 1, 1) if n > 1 else 0
        pitch = min(pitch, 0.6)                    # do not spread a short row
        x0 = B_X0 + (span - pitch * (n - 1)) / 2
        for k, tid in enumerate(techs):
            pos[tid] = (x0 + k * pitch, row_y[t])
    max_obs_tech = max(e["observation_count"] for e in gap["edges"])
    edges_sorted = sorted(gap["edges"], key=lambda e: e["observation_count"])
    for e in edges_sorted:                          # light first, dark on top
        s, t = e["source_id"], e["target_id"]
        if e["observation_count"] < min_obs:
            continue
        (xs, ys), (xt, yt) = pos[s], pos[t]
        lw, grey = edge_style(e["observation_count"], max_obs_tech)
        col = "black!%d" % grey
        if (s, t) in ex_tech_edges:
            col, lw = ACCENT, max(lw, 0.6)
        if s == t:
            w(r"\draw[%s,line width=%.2fpt] (%.3f,%.3f) .. controls +(0.14,0.28) and +(-0.14,0.28) .. (%.3f,%.3f);"
              % (col, lw, xs, ys, xt, yt))
        elif ys == yt:                              # same tactic, other technique
            bulge = 0.10 + 0.05 * abs(xt - xs)
            w(r"\draw[%s,line width=%.2fpt] (%.3f,%.3f) .. controls +(0,%.3f) and +(0,%.3f) .. (%.3f,%.3f);"
              % (col, lw, xs, ys, bulge, bulge, xt, yt))
        else:
            dy = (yt - ys) * 0.45
            w(r"\draw[%s,line width=%.2fpt] (%.3f,%.3f) .. controls +(0,%.3f) and +(0,%.3f) .. (%.3f,%.3f);"
              % (col, lw, xs, ys, dy, -dy, xt, yt))
    for tid, (x, y) in pos.items():
        if tid in ex_techs:
            w(r"\fill[%s] (%.3f,%.3f) circle (0.55mm);" % (ACCENT, x, y))
        else:
            w(r"\fill[black!70] (%.3f,%.3f) circle (0.42mm);" % (x, y))

    # ---- (c) tactic-level aggregate --------------------------------------
    trans = {k: v for k, v in st["trans_obs"].items() if v >= min_obs}
    max_obs = max(trans.values())
    idx = {t: i for i, t in enumerate(order)}
    max_span = len(order) - 1
    for (s, t), obs in sorted(trans.items(), key=lambda kv: kv[1]):
        ys, yt = row_y[s], row_y[t]
        lw, grey = edge_style(obs, max_obs)
        col = "black!%d" % grey
        tinted = (s, t) in ex_trans
        if s == t:
            w(r"\draw[%s,line width=%.2fpt] (%.3f,%.3f) .. controls +(0.42,0.30) and +(0.42,-0.30) .. (%.3f,%.3f);"
              % (col, lw, C_X, ys, C_X, yt))
            if tinted:
                w(r"\draw[%s,line width=0.5pt] (%.3f,%.3f) .. controls +(0.42,0.30) and +(0.42,-0.30) .. (%.3f,%.3f);"
                  % (ACCENT, C_X, ys, C_X, yt))
            continue
        span = abs(idx[t] - idx[s]) / max_span
        forward = idx[t] > idx[s]
        bulge = (C_FWD_BULGE if forward else -C_BWD_BULGE) * (0.25 + 0.75 * span)
        w(r"\draw[%s,line width=%.2fpt] (%.3f,%.3f) .. controls (%.3f,%.3f) and (%.3f,%.3f) .. (%.3f,%.3f);"
          % (col, lw, C_X, ys, C_X + bulge, ys, C_X + bulge, yt, C_X, yt))
        if tinted:
            w(r"\draw[%s,line width=0.5pt] (%.3f,%.3f) .. controls (%.3f,%.3f) and (%.3f,%.3f) .. (%.3f,%.3f);"
              % (ACCENT, C_X, ys, C_X + bulge, ys, C_X + bulge, yt, C_X, yt))
    # arrowheads only on the heaviest few so direction is legible without clutter
    top = sorted(trans.items(), key=lambda kv: -kv[1])[:6]
    for (s, t), obs in top:
        if s == t:
            continue
        ys, yt = row_y[s], row_y[t]
        span = abs(idx[t] - idx[s]) / max_span
        forward = idx[t] > idx[s]
        bulge = (C_FWD_BULGE if forward else -C_BWD_BULGE) * (0.25 + 0.75 * span)
        # label at the apex of the arc
        w(r"\node[font=\tiny,fill=white,inner sep=0.4pt] at (%.3f,%.3f) {%d};"
          % (C_X + bulge * 0.75, (ys + yt) / 2, obs))
    max_flows = max(st["flows_by_tactic"].values())
    for t in order:
        r = 0.55 + 1.35 * math.sqrt(st["flows_by_tactic"][t] / max_flows)   # mm
        w(r"\filldraw[fill=white,draw=black,line width=0.5pt] (%.3f,%.3f) circle (%.2fmm);"
          % (C_X, row_y[t], r))

    # ---- (a) one incident as drawn ---------------------------------------
    fn = {n["id"]: n for n in flow["nodes"]}
    rows = flow_rows(flow)
    a_pitch = min(0.74, (y_top - y_bot) / max(len(rows) - 1, 1))
    a_y0 = y_top - ((y_top - y_bot) - a_pitch * (len(rows) - 1)) / 2
    apos: dict[str, tuple[float, float]] = {}
    for i, row in enumerate(rows):
        for nid in row:
            apos[nid] = (A_X, a_y0 - i * a_pitch)
    for nid, (x, y) in apos.items():
        nd = fn[nid]
        if nd["kind"] == "action":
            tl = TACTIC_LABEL.get(nd.get("tactic") or "", nd.get("tactic") or "")
            w(r"\node[draw=%s,line width=0.5pt,rounded corners=1pt,inner xsep=2pt,inner ysep=1.4pt,"
              r"minimum width=%.2fcm,align=center,font=\tiny] (a%s) at (%.3f,%.3f) "
              r"{%s\\[-1.5pt]{\color{black!55}%s\ $\cdot$\ %s}};"
              % (ACCENT, A_W, nid, x, y, _esc(_short(nd["name"], 44)),
                 nd["technique_id"], _esc(tl)))
        elif nd["kind"] == "operator":
            w(r"\node[draw=%s,line width=0.5pt,diamond,inner sep=0.5pt,font=\tiny] (a%s) at (%.3f,%.3f) {%s};"
              % (ACCENT, nid, x, y, nd["operator"]))
        else:
            w(r"\node[draw=%s,line width=0.5pt,dashed,rounded corners=3pt,inner sep=1.6pt,"
              r"minimum width=%.2fcm,align=center,font=\tiny] (a%s) at (%.3f,%.3f) {%s};"
              % (ACCENT, A_W, nid, x, y, _esc(_short(nd.get("description", "condition"), 44))))
    for e in flow["edges"]:
        s, t = e["source"], e["target"]
        (xs, ys), (xt, yt) = apos[s], apos[t]
        rows_apart = round(abs(ys - yt) / a_pitch)
        if rows_apart <= 1:
            w(r"\draw[->,%s,line width=0.45pt] (a%s) -- (a%s);" % (ACCENT, s, t))
        else:                                       # skips a row: bow out to the side
            side = A_W / 2 + 0.13 * rows_apart
            w(r"\draw[->,%s,line width=0.45pt] (a%s.east) .. controls (%.3f,%.3f) and (%.3f,%.3f) .. (a%s.east);"
              % (ACCENT, s, A_X + side, ys - 0.1, A_X + side, yt + 0.1, t))
    if flow.get("start_refs"):
        sx, sy = apos[flow["start_refs"][0]]
        w(r"\draw[->,%s,line width=0.45pt] (%.3f,%.3f) -- (a%s);" % (ACCENT, sx, sy + 0.42, flow["start_refs"][0]))

    # ---- panel letters + headers ---------------------------------------
    hy = y_top + 0.66
    def header(x: float, letter: str, text: str) -> None:
        w(r"\node[anchor=south west,font=\scriptsize] at (%.2f,%.2f) {\textbf{%s}\ %s};" % (x, hy, letter, text))
    header(A_X - A_W / 2, "(a)", "one incident, as the analyst drew it")
    w(r"\node[anchor=north west,font=\tiny,text=black!55] at (%.2f,%.2f) {%s};"
      % (A_X - A_W / 2, hy - 0.02, _esc(flow["flow_name"])))
    header(B_X0 - 0.15, "(b)", "all incidents, technique level")
    w(r"\node[anchor=north west,font=\tiny,text=black!55] at (%.2f,%.2f) {%d flows: %d techniques, %d edges};"
      % (B_X0 - 0.15, hy - 0.02, st["n_flows"], st["n_nodes"], st["n_edges"]))
    header(C_X - 0.85, "(c)", "all incidents, tactic level")
    w(r"\node[anchor=north west,font=\tiny,text=black!55] at (%.2f,%.2f) {%d tactics, %d transitions};"
      % (C_X - 0.85, hy - 0.02, st["n_tactics"], st["n_trans"]))

    # ---- key ------------------------------------------------------------
    def key_row(x: float, y: float, title: str, samples: list[int], mx: int, unit: str) -> float:
        w(r"\node[anchor=west,font=\tiny,text=black!55] at (%.2f,%.2f) {%s};" % (x, y, title))
        x += 3.15
        for o in samples:
            lw, grey = edge_style(o, mx)
            w(r"\draw[black!%d,line width=%.2fpt] (%.2f,%.2f) -- (%.2f,%.2f);" % (grey, lw, x, y, x + 0.32, y))
            w(r"\node[anchor=west,font=\tiny,text=black!55] at (%.2f,%.2f) {%d};" % (x + 0.34, y, o))
            x += 0.68 if o < 10 else 0.78
        w(r"\node[anchor=west,font=\tiny,text=black!55] at (%.2f,%.2f) {%s};" % (x - 0.05, y, unit))
        return x
    kx = A_X - A_W / 2
    ky = y_bot - 0.62
    key_row(kx, ky, "(b) technique edge, drawn in", sorted({1, 2, max_obs_tech}), max_obs_tech, "incidents")
    key_row(kx, ky - 0.30, "(c) tactic transition, weight", sorted({1, 4, 12, max_obs}), max_obs, "summed observations")
    kx2 = B_X0 + 1.7
    w(r"\draw[%s,line width=0.6pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (ACCENT, kx2, ky, kx2 + 0.32, ky))
    w(r"\node[anchor=west,font=\tiny,text=black!55] at (%.2f,%.2f) {the incident in (a), wherever it lands};" % (kx2 + 0.36, ky))
    w(r"\node[anchor=north west,font=\tiny,text=black!55,text width=6.3cm,align=left,inner sep=0pt] at (%.2f,%.2f) "
      r"{(c) forward transitions bulge right, backward transitions left; node area $\propto$ incidents containing the tactic};" % (kx2, ky - 0.18))

    w(r"\end{tikzpicture}")
    w(r"\end{document}")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--flow", default="cisa_aa22_138b_vmware_workspace_ta1",
                    help="flow_id of the exemplar for panel (a)")
    ap.add_argument("--min-obs", type=int, default=1,
                    help="hide edges/transitions observed fewer than N times (default: show all)")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    gap, order = load()
    st = stats(gap, order)
    flow = load_flow(args.flow)
    tex = emit(gap, order, st, flow, args.min_obs)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUT_DIR / f"{STEM}.tex"
    tex_path.write_text(tex)
    print(f"wrote {tex_path.relative_to(REPO)}")

    # numbers the caption quotes — print for cross-checking, never hard-code
    print(f"flows={st['n_flows']}  techniques={st['n_nodes']}  technique-edges={st['n_edges']}"
          f"  single-incident={st['n_single']} ({100*st['n_single']/st['n_edges']:.0f}%)")
    print(f"tactics={st['n_tactics']}  transitions={st['n_trans']}  observations={st['obs_total']}"
          f"  single-observation transitions={st['n_trans_single']}"
          f"  transitions seen in >=2 flows={st['n_trans_multi_flow']}")
    fb = st["flows_by_tactic"]
    print("flows containing tactic: " + ", ".join(f"{t}={fb[t]}" for t in order))
    top = sorted(st["trans_obs"].items(), key=lambda kv: -kv[1])[:6]
    print("heaviest transitions: " + "; ".join(f"{s}->{t}={o}" for (s, t), o in top))
    print(f"exemplar flow: {flow['flow_id']} ({flow['flow_name']}), "
          f"{sum(1 for n in flow['nodes'] if n['kind']=='action')} actions, "
          f"{sum(1 for n in flow['nodes'] if n['kind']=='operator')} operators, {len(flow['edges'])} edges")

    if not args.no_compile:
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
                           cwd=OUT_DIR, capture_output=True, text=True)
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
