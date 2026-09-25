"""fig:gspn-gadget — one tactic of a profile net, drawn as a GSPN.

The formalism section (§4.3) states the net as a tuple; this figure shows the
shape the tuple names, for a reader who has never seen a Petri net. Two
panels, Marsan's drawing convention, decoded in an in-figure legend:

* **(a)** the generic gadget of one tactic ``p``: the tangible tactic place
  with the token, the timed transition ``tau_p`` (hollow bar, rate ``1/mu_p``),
  the vanishing decision place ``p-hat`` (dashed circle), and the fan of
  weighted immediate transitions ``t_pq`` (solid bars) to the successors;
* **(b)** the same gadget on one real place of one profile net, with two
  ledger columns beside the successor places: the base weight ``w_c(p,q)``
  of Eq. base-weight and, in the accent, the failure-verdict weight
  ``W_c(t_pq | failure)`` of Eq. routing. The accent column is the one thing
  the figure is about — the verdict-conditioned reweighting the section adds
  to the GSPN.

Everything numeric is read, never typed:

* the place's out-transitions and base weights from the profile's routing net
  (``mtdsim.l3_simulation.movement.net.load_routing_net`` — the composed net
  the movement layer walks, primary corpus variant, synthetic overlay as run);
* the failure-verdict column from the same ``OutcomeOverlay.compose`` the
  controller calls at runtime (never a re-implementation of Eq. routing);
* ``mu_p`` from ``data/ogasp/tactic_durations.json``;
* tactic display names and the ATT&CK version pin from the pinned bundle via
  ``_tactic_axis``.

Ruling R7 (2026-09-08): ``T_I`` is the positive-weight pair set, so only
transitions with ``w_c > 0`` are drawn; the routing net carries the wider L2
pair set with zero weights that never fire, and the two are behaviourally
identical (handoff 2026-09-08_ch4_s43_gspn_formalism.md §8.3).

Words live in the caption, not the panel (Marc, 2026-09-08): the figure
carries symbols, names, numbers and the legend only.

Usage: ``python tools/gspn_gadget_figure.py [--profile objective_exfiltration]
[--place initial-access] [--overlay v4_failure_only] [--no-compile]``
-> ``docs/thesis/figures/fig_4-3a_gspn_gadget.{tex,pdf}``. Prints every
number the caption quotes.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "tools"))

from _tactic_axis import load_axis  # noqa: E402
from mtdsim.l3_simulation.controller.outcome import load_outcome_overlay  # noqa: E402
from mtdsim.l3_simulation.movement.net import load_routing_net  # noqa: E402

OUT_DIR = REPO / "docs" / "thesis" / "figures"
STEM = "fig_4-3a_gspn_gadget"
DURATIONS = REPO / "data" / "ogasp" / "tactic_durations.json"

# House style (figure_table_conventions.md §h, §l; canonical block in
# gap_appendix_figures.py): 12pt standalone, helvet 0.92, greys + one accent.
PREAMBLE = r"""\documentclass[tikz,12pt,border=2pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage[scaled=0.92]{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usetikzlibrary{arrows.meta,positioning}
\definecolor{accent}{RGB}{31,84,140}
\definecolor{accentlight}{RGB}{200,214,232}
\begin{document}
\begin{tikzpicture}[
  font=\scriptsize,
  place/.style={circle,draw=black,thick,minimum size=7mm,inner sep=0pt},
  vplace/.style={circle,draw=black,thick,dashed,minimum size=7mm,inner sep=0pt},
  timed/.style={rectangle,draw=black,thick,fill=white,minimum width=2.6mm,minimum height=7mm,inner sep=0pt},
  imm/.style={rectangle,draw=black,fill=black,minimum width=1.2mm,minimum height=6mm,inner sep=0pt},
  arc/.style={-{Stealth[length=2mm]},thick,black!70},
  lab/.style={black!60,font=\scriptsize},
  head/.style={font=\scriptsize\bfseries},
]
"""

# x-positions (cm) shared by both panels so the gadget lines up
X_P, X_TAU, X_PHAT, X_BAR, X_Q = 0.0, 2.0, 4.0, 6.0, 7.6
# panel (b) ledger columns
X_NAME, X_W, X_WF = 8.1, 11.1, 12.6
ROW = 0.76  # cm pitch of the successor rows in (b)


def tex_escape(s: str) -> str:
    return (s.replace("\\", r"\textbackslash{}").replace("&", r"\&")
             .replace("%", r"\%").replace("#", r"\#").replace("_", r"\_"))


def panel_a() -> list[str]:
    y = 1.5
    out = [
        rf"\node[head,anchor=west] at ({X_P-0.6},{y+1.9}) {{(a)\enspace One tactic $p$ of a Petri net $\mathcal{{N}}_c$}};",
        rf"\node[place] (p) at ({X_P},{y}) {{}}; \fill (p) circle (0.9mm);",
        rf"\node[below=2pt of p,lab,align=center] {{$p$}};",
        rf"\node[timed] (tau) at ({X_TAU},{y}) {{}};",
        rf"\node[above=2pt of tau,lab] {{$\tau_p$}};",
        rf"\node[below=2pt of tau,lab] {{$1/\mu_p$}};",
        rf"\node[vplace] (ph) at ({X_PHAT},{y}) {{}};",
        rf"\node[below=2pt of ph,lab] {{$\hat{{p}}$}};",
        r"\draw[arc] (p) -- (tau); \draw[arc] (tau) -- (ph);",
    ]
    for i, (dy, q) in enumerate(((1.4, "q_1"), (0.0, "q_2"), (-1.4, "q_k")), 1):
        out += [
            rf"\node[imm] (t{i}) at ({X_BAR},{y+dy}) {{}};",
            rf"\node[place] (q{i}) at ({X_Q+0.6},{y+dy}) {{}};",
            rf"\node[right=2pt of q{i},lab] {{${q}$}};",
            rf"\draw[arc] (ph) -- (t{i}); \draw[arc] (t{i}) -- (q{i});",
            rf"\node[lab,anchor=south west,inner sep=1pt] at ({X_BAR+0.12},{y+dy+0.06}) {{$t_{{p{q}}}$}};",
            rf"\node[lab,anchor=north west,inner sep=1pt] at ({X_BAR+0.12},{y+dy-0.06}) {{$w_c(p,{q})$}};",
        ]
    out.append(rf"\node[lab] at ({X_Q+0.6},{y-0.7}) {{$\vdots$}};")
    # legend, inside the figure (genre convention)
    lx, ly = 10.1, y + 1.4
    out += [
        rf"\node[place,minimum size=4mm] (lp) at ({lx},{ly}) {{}}; \node[right=2pt of lp,lab] {{place (tangible: the token dwells)}};",
        rf"\node[vplace,minimum size=4mm] (lv) at ({lx},{ly-0.55}) {{}}; \node[right=2pt of lv,lab] {{decision place (vanishing: zero time)}};",
        rf"\node[timed,minimum height=4mm,minimum width=2mm] (lt) at ({lx},{ly-1.1}) {{}}; \node[right=2pt of lt,lab] {{timed transition, exponential delay}};",
        rf"\node[imm,minimum height=4mm] (li) at ({lx},{ly-1.65}) {{}}; \node[right=2pt of li,lab] {{immediate transition, weighted}};",
        rf"\fill ({lx},{ly-2.2}) circle (0.9mm); \node[lab,anchor=west] at ({lx+0.2},{ly-2.2}) {{the token ($M_0$: one)}};",
    ]
    return out


def panel_b(place: str, rows: list[tuple[str, float, float]], mu: float,
            axis, profile_label: str, attack_id: str) -> list[str]:
    n = len(rows)
    y_top = -2.3
    y_mid = y_top - ROW * (n - 1) / 2
    out = [
        rf"\node[head,anchor=west] at ({X_P-0.6},{y_top+0.9}) {{(b)\enspace The same gadget on \emph{{{tex_escape(axis.label[place].lower())}}} in the {tex_escape(profile_label)} profile}};",
        rf"\node[place] (bp) at ({X_P},{y_mid}) {{}}; \fill (bp) circle (0.9mm);",
        rf"\node[below=2pt of bp,lab,align=center] {{{tex_escape(axis.label[place])}\\{attack_id}}};",
        rf"\node[timed] (btau) at ({X_TAU},{y_mid}) {{}};",
        rf"\node[above=2pt of btau,lab] {{$\tau_p$}};",
        rf"\node[below=2pt of btau,lab] {{$\mu_p = {mu:g}$\,s}};",
        rf"\node[vplace] (bph) at ({X_PHAT},{y_mid}) {{}};",
        rf"\node[below=2pt of bph,lab] {{$\hat{{p}}$}};",
        r"\draw[arc] (bp) -- (btau); \draw[arc] (btau) -- (bph);",
        rf"\node[lab,anchor=west] at ({X_W},{y_top+0.5}) {{$w_c(p,q)$}};",
        rf"\node[lab,anchor=west,accent] at ({X_WF},{y_top+0.5}) {{$W_c(t_{{pq}}\mid\mathrm{{failure}})$}};",
    ]
    for i, (q, w, wf) in enumerate(rows, 1):
        y = y_top - ROW * (i - 1)
        out += [
            rf"\node[imm] (bt{i}) at ({X_BAR},{y}) {{}};",
            rf"\node[place] (bq{i}) at ({X_Q},{y}) {{}};",
            rf"\node[lab,anchor=west] at ({X_NAME},{y}) {{{tex_escape(axis.label[q])}}};",
            rf"\node[lab,anchor=west] at ({X_W},{y}) {{{w:.3f}}};",
            rf"\node[lab,anchor=west,accent] at ({X_WF},{y}) {{{wf:.3f}}};",
            rf"\draw[arc] (bph) -- (bt{i}); \draw[arc] (bt{i}) -- (bq{i});",
        ]
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", default="objective_exfiltration")
    ap.add_argument("--place", default="initial-access")
    ap.add_argument("--overlay", default="v4_failure_only",
                    help="outcome-overlay version from the registry")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    axis = load_axis()
    net = load_routing_net(args.profile, with_synthetic_overlay=True)
    if args.place not in net.places:
        raise SystemExit(f"{args.place!r} is not a place of {args.profile}")
    base = net.base_out_weights(args.place)
    overlay = load_outcome_overlay(version=args.overlay)
    routed = overlay.compose(args.place, "failure", base)

    # R7: T_I is the positive-weight pair set; zero-weight pairs are not drawn.
    dropped = sorted(q for q, w in base.items() if w <= 0)
    positive = {q: w for q, w in base.items() if w > 0}
    rows = sorted(((q, w, routed.get(q, 0.0)) for q, w in positive.items()),
                  key=lambda r: (-r[1], axis.matrix_order.index(r[0])))

    durations = json.loads(DURATIONS.read_text())["tactics"]
    mu = float(durations[args.place]["duration_s"])
    attack_id = durations[args.place]["attack_tactic_id"]
    profile_label = args.profile.removeprefix("objective_").replace("_", " + ")

    body = PREAMBLE.splitlines()
    body += panel_a()
    body += panel_b(args.place, rows, mu, axis, profile_label, attack_id)
    body += [r"\end{tikzpicture}", r"\end{document}", ""]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUT_DIR / f"{STEM}.tex"
    tex_path.write_text("\n".join(body))
    print(f"wrote {tex_path.relative_to(REPO)}")

    # the numbers the caption quotes
    print(f"profile={args.profile}  place={args.place}  ATT&CK={axis.version}  "
          f"overlay={args.overlay}  variant=primary  mu={mu:g} s")
    print(f"out-transitions in the routing net: {len(base)}; drawn (w_c > 0): "
          f"{len(rows)}; zero-weight, not drawn: {len(dropped)} "
          f"({', '.join(dropped) or 'none'})")
    for q, w, wf in rows:
        print(f"  {axis.label[q]:22s} w_c={w:.3f}  W_c|failure={wf:.3f}")
    top = max(rows, key=lambda r: r[2])
    print(f"failure verdict: mass to {axis.label[top[0]]} = {top[2]:.3f} "
          f"(base {top[1]:.3f})")

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
