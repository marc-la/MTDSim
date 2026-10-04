"""fig:gspn-gadget — one tactic of a profile net, drawn as a GSPN.

The formalism section (§4.3) states the net as a tuple; this figure shows the
shape the tuple names, for a reader who has never seen a Petri net. Two
panels, Marsan's drawing convention, decoded in an in-figure legend:

* **(a)** one tactic ``p`` in general: the tactic place with the token, the
  timed transition ``tau_p`` (hollow bar, rate ``1/mu_p``), the decision place
  ``p-hat`` (dashed circle), and the fan of immediate transitions ``t_pq``
  (solid bars) to the successors;
* **(b)**, **(c)** one real tactic of ``c_1`` each, with two ledger columns
  beside the successor places: the base weight ``W(t_pq)`` of Eq. base-weight
  and, in the accent, the weight after a failure ``W(t_pq | failure)`` of Eq.
  routing. The accent column is what the section adds to the GSPN.
  Symbols follow the 2026-10-04 redraft of section 4.3 (the standard tuple,
  E9): ``w_c`` and ``W_c`` became ``W``; "gadget", "tangible" and "vanishing"
  are off the figure (the text no longer uses them).

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
transitions with ``W(t_pq) > 0`` are drawn; the routing net carries the wider L2
pair set with zero weights that never fire, and the two are behaviourally
identical (handoff 2026-09-08_ch4_s43_gspn_formalism.md §8.3).

Words live in the caption, not the panel (Marc, 2026-09-08): the figure
carries symbols, names, numbers and the legend only.

Usage: ``python tools/gspn_gadget_figure.py [--profile objective_exfiltration]
[--place initial-access] [--place-c credential-access] [--overlay v4_failure_only]
[--no-compile]``
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
from pipeline_ladder_figure import PROFILE_CODE  # noqa: E402  the c_k of Table 4.1
from mtdsim.l3_simulation.controller.outcome import load_outcome_overlay  # noqa: E402
from mtdsim.l3_simulation.movement.measures import load_stage_of  # noqa: E402
from mtdsim.l3_simulation.movement.net import PROFILES, load_routing_net  # noqa: E402

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
        ]
    out.append(rf"\node[lab] at ({X_Q+0.6},{y-0.7}) {{$\vdots$}};")
    # legend, inside the figure (genre convention)
    lx, ly = 10.1, y + 1.4
    out += [
        rf"\node[place,minimum size=4mm] (lp) at ({lx},{ly}) {{}}; \node[right=2pt of lp,lab] {{place (a tactic)}};",
        rf"\node[vplace,minimum size=4mm] (lv) at ({lx},{ly-0.55}) {{}}; \node[right=2pt of lv,lab] {{decision place (zero time)}};",
        rf"\node[timed,minimum height=4mm,minimum width=2mm] (lt) at ({lx},{ly-1.1}) {{}}; \node[right=2pt of lt,lab] {{timed transition (exponential delay)}};",
        rf"\node[imm,minimum height=4mm] (li) at ({lx},{ly-1.65}) {{}}; \node[right=2pt of li,lab] {{immediate transition (weighted)}};",
        rf"\fill ({lx},{ly-2.2}) circle (0.9mm); \node[lab,anchor=west] at ({lx+0.2},{ly-2.2}) {{token}};",
    ]
    return out


def panel_b(place: str, rows: list[tuple[str, float, float]], mu: float,
            axis, profile_label: str, attack_id: str, letter: str = "b",
            y_top: float = -2.3) -> list[str]:
    """One real place of one profile net with its two ledger columns. Drawn
    twice (2026-09-26, Marc: the principle must be visible in the figure the
    chapter keeps): (b) a tactic without a foothold (initial access), where a
    failure sends the token back; (c) a post-intrusion tactic, where a failure
    keeps it in its stage. Node names carry the panel letter."""
    n = len(rows)
    y_mid = y_top - ROW * (n - 1) / 2
    k = letter
    out = [
        rf"\node[head,anchor=west] at ({X_P-0.6},{y_top+0.9}) {{({k})\enspace {tex_escape(axis.label[place])} in {profile_label}}};",
        rf"\node[place] ({k}p) at ({X_P},{y_mid}) {{}}; \fill ({k}p) circle (0.9mm);",
        # the tactic name broken at its spaces so that a long name (credential
        # access) does not widen the figure past \textwidth
        rf"\node[below=2pt of {k}p,lab,align=center] {{{tex_escape(axis.label[place]).replace(' ', chr(92) * 2)}\\{attack_id}}};",
        rf"\node[timed] ({k}tau) at ({X_TAU},{y_mid}) {{}};",
        rf"\node[above=2pt of {k}tau,lab] {{$\tau_p$}};",
        rf"\node[below=2pt of {k}tau,lab] {{$\mu_p = {mu:g}$\,s}};",
        rf"\node[vplace] ({k}ph) at ({X_PHAT},{y_mid}) {{}};",
        rf"\node[below=2pt of {k}ph,lab] {{$\hat{{p}}$}};",
        rf"\draw[arc] ({k}p) -- ({k}tau); \draw[arc] ({k}tau) -- ({k}ph);",
        rf"\node[lab,anchor=west] at ({X_W},{y_top+0.5}) {{$W(t_{{pq}})$}};",
        rf"\node[lab,anchor=west,accent] at ({X_WF},{y_top+0.5}) {{$W(t_{{pq}}\mid\mathrm{{failure}})$}};",
    ]
    for i, (q, w, wf) in enumerate(rows, 1):
        y = y_top - ROW * (i - 1)
        out += [
            rf"\node[imm] ({k}t{i}) at ({X_BAR},{y}) {{}};",
            rf"\node[place] ({k}q{i}) at ({X_Q},{y}) {{}};",
            rf"\node[lab,anchor=west] at ({X_NAME},{y}) {{{tex_escape(axis.label[q])}}};",
            rf"\node[lab,anchor=west] at ({X_W},{y}) {{{w:.3f}}};",
            rf"\node[lab,anchor=west,accent] at ({X_WF},{y}) {{{wf:.3f}}};",
            rf"\draw[arc] ({k}ph) -- ({k}t{i}); \draw[arc] ({k}t{i}) -- ({k}q{i});",
        ]
    return out


def stage_shares(overlay) -> None:
    """The numbers section 4.4.4 quotes for the principle (2026-09-26): per
    attack profile, the mean share of a post-intrusion tactic's base weight on
    moves to another post-intrusion tactic; and, over c1-c4, the mean base and
    failure-routed shares by relation (back / same stage / forward), per stage
    of the tactic that failed. Stages from the ratified lifecycle consensus."""
    stage = load_stage_of()
    rel = lambda p, q: "back" if stage[q] < stage[p] else "same" if stage[q] == stage[p] else "forward"
    pooled = {s: {"n": 0} for s in range(4)}
    for prof in PROFILES:
        net = load_routing_net(prof, with_synthetic_overlay=True)
        shares = []
        for p in net.places:
            base = {q: w for q, w in net.base_out_weights(p).items() if w > 0}
            if not base:
                continue
            if stage[p] == 2:
                shares.append(sum(w for q, w in base.items() if stage[q] == 2))
            if prof == "aggregate":
                continue
            routed = overlay.compose(p, "failure", base)
            acc = pooled[stage[p]]
            acc["n"] += 1
            for q, w in base.items():
                acc[f"base_{rel(p, q)}"] = acc.get(f"base_{rel(p, q)}", 0.0) + w
                acc[f"fail_{rel(p, q)}"] = acc.get(f"fail_{rel(p, q)}", 0.0) + routed.get(q, 0.0)
        print(f"  same-stage share of a post-intrusion tactic's base weight, {prof}: "
              f"{sum(shares) / len(shares):.2f} over {len(shares)} tactics")
    for s_, acc in pooled.items():
        n = acc.pop("n")
        print(f"  stage {s_} ({n} places, c1-c4): " + ", ".join(f"{k} {v / n:.2f}" for k, v in sorted(acc.items())))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--profile", default="objective_exfiltration")
    ap.add_argument("--place", default="initial-access")
    ap.add_argument("--place-c", default="credential-access",
                    help="the post-intrusion tactic panel (c) draws")
    ap.add_argument("--overlay", default="v4_failure_only",
                    help="outcome-overlay version from the registry")
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args()

    axis = load_axis()
    net = load_routing_net(args.profile, with_synthetic_overlay=True)
    overlay = load_outcome_overlay(version=args.overlay)
    durations = json.loads(DURATIONS.read_text())["tactics"]
    profile_label = f"$c_{{{PROFILE_CODE[args.profile]}}}$"

    def ledger(place):
        if place not in net.places:
            raise SystemExit(f"{place!r} is not a place of {args.profile}")
        base = net.base_out_weights(place)
        routed = overlay.compose(place, "failure", base)
        # R7: T_I is the positive-weight pair set; zero-weight pairs are not drawn.
        dropped = sorted(q for q, w in base.items() if w <= 0)
        positive = {q: w for q, w in base.items() if w > 0}
        rows = sorted(((q, w, routed.get(q, 0.0)) for q, w in positive.items()),
                      key=lambda r: (-r[1], axis.matrix_order.index(r[0])))
        return base, rows, dropped, float(durations[place]["duration_s"]), durations[place]["attack_tactic_id"]

    base, rows, dropped, mu, attack_id = ledger(args.place)
    base_c, rows_c, dropped_c, mu_c, attack_id_c = ledger(args.place_c)

    body = PREAMBLE.splitlines()
    body += panel_a()
    body += panel_b(args.place, rows, mu, axis, profile_label, attack_id, "b", -2.3)
    y_top_c = -2.3 - ROW * (len(rows) - 1) - 2.0
    body += panel_b(args.place_c, rows_c, mu_c, axis, profile_label, attack_id_c, "c", y_top_c)
    body += [r"\end{tikzpicture}", r"\end{document}", ""]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = OUT_DIR / f"{STEM}.tex"
    tex_path.write_text("\n".join(body))
    print(f"wrote {tex_path.relative_to(REPO)}")

    # the numbers the caption quotes
    print(f"profile={args.profile}  place={args.place}  ATT&CK={axis.version}  "
          f"overlay={args.overlay}  variant=primary  mu={mu:g} s")
    print(f"out-transitions in the routing net: {len(base)}; drawn (W > 0): "
          f"{len(rows)}; zero-weight, not drawn: {len(dropped)} "
          f"({', '.join(dropped) or 'none'})")
    for q, w, wf in rows:
        print(f"  {axis.label[q]:22s} W={w:.3f}  W|failure={wf:.3f}")
    top = max(rows, key=lambda r: r[2])
    print(f"failure verdict: mass to {axis.label[top[0]]} = {top[2]:.3f} "
          f"(base {top[1]:.3f})")
    print("the principle's numbers (section 4.4.4):")
    stage_shares(overlay)
    print(f"panel (c): place={args.place_c}  mu={mu_c:g} s  drawn {len(rows_c)}; "
          f"zero-weight, not drawn: {len(dropped_c)}")
    for q, w, wf in rows_c:
        print(f"  {axis.label[q]:22s} W={w:.3f}  W|failure={wf:.3f}")

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
