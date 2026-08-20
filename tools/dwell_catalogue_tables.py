"""The dwell-time catalogue tables --- chapter parameter table + appendix derivation.

Two floats from one declared family, emitted from `data/ogasp/tactic_durations.json`
so no value is ever typed (`figure_table_conventions.md` §h):

* `tab:dwell-catalogue` (§4.2.4.1) --- the **what**. Two panels in one float:
  (a) the anchor families and the null, (b) the fifteen tactics that resolve
  onto them. Panel (a) is what makes the identifiability argument visible ---
  four free timing parameters, not fifteen --- and it is where the evidence
  badges live, since a badge is constant within a family.
* `tab:dwell-derivation` (`app:dwell-derivation`) --- the **why**: per-tactic
  sweep bands and the short justification, dense on purpose.

The what/why split is Marc's ruling (2026-08-20); the badge *decode* lives in
the chapter caption rather than the table, which is conventions §b2 (the caption
decodes every encoding) rather than a dodge.

Axis: `_tactic_axis.matrix_order` --- these tables draw no lifecycle bands, and
matrix order is what `fig:l1-graph` takes, so the §b6 cross-figure contract
holds. Display names and the ATT&CK version pin come from the pinned bundle
through that module, never from a local map.

Usage:  python tools/dwell_catalogue_tables.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tactic_axis import load_axis  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CATALOGUE = REPO / "data" / "ogasp" / "tactic_durations.json"
OUT_DIR = REPO / "docs" / "thesis" / "tables"

# Presentation names for the anchor families and for where each family's shape
# came from. Names only --- every *value* is read from the catalogue
# (conventions §g: presentation names are part of the spec and are mapped here,
# never raw identifiers in the float; §h: no value typed).
FAMILY_LABEL = {
    "scan-shaped": "Scan-shaped",
    "exploit-shaped": "Exploit-shaped",
    "stealth-low-and-slow": "Low-and-slow",
    "objective-execution": "Objective execution",
    "prep-off-network": "Off-network prep",
}

# For the two families the simulator prices, this names the action whose cost
# the value inherits. It is the value's *shape source*, not the verb the tactic
# dispatches at run time --- the caption says so, because the two differ.
PRICED_FROM = {
    "scan-shaped": "MTDSim's scan verbs, one enumeration pass",
    "exploit-shaped": "MTDSim's exploit time, at median complexity",
    "prep-off-network": "no in-simulator dwell",
}

BADGE_ORDER = ["Priced by MTDSim", "Declared and swept", "Declared, off-clock"]


def esc(s: str) -> str:
    """LaTeX-escape a presentation string."""
    for a, b in (("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")):
        s = s.replace(a, b)
    return s


def badge_for(anchor_name: str, anchor: dict, members: list[dict]) -> str:
    """The evidence badge, derived from the catalogue rather than declared here.

    Three badges, not four: under `v0-uncalibrated` the Tier-2 and Tier-3
    families make the *same* validity claim --- both declared, both swept,
    neither calibrated --- so collapsing them is the honest chapter face. The
    tier number and the named macro target stay in the appendix, where the
    distinction is prospective. (Marc, 2026-08-20.)
    """
    if all(m["tier"] == 1 for m in members):
        return "Priced by MTDSim"
    if anchor["duration_s"] == 0:
        return "Declared, off-clock"
    return "Declared and swept"


def priced_from(anchor_name: str, anchors: dict) -> str:
    """Where the family's shape came from --- derived where it is arithmetic."""
    if anchor_name in PRICED_FROM:
        return PRICED_FROM[anchor_name]
    base = anchors["exploit-shaped"]["duration_s"]
    k = anchors[anchor_name]["duration_s"] / base
    return rf"{k:g}$\times$ the exploit shape"


def num(x: float) -> str:
    return f"{x:.1f}"


def main() -> None:
    cat = json.loads(CATALOGUE.read_text())
    anchors, tactics = cat["anchors"], cat["tactics"]
    axis = load_axis()

    # The axis is a contract: fail loudly if the catalogue's tactic set has
    # drifted from the pinned bundle rather than emitting a table against a
    # tactic set ATT&CK does not carry.
    axis.check_against(list(tactics))

    members: dict[str, list[dict]] = {a: [] for a in anchors}
    for name in axis.matrix_order:
        members[tactics[name]["anchor"]].append(tactics[name])

    # Family row order: badge class first, then first appearance on the axis.
    # Derived, so the null lands last without being placed there by hand.
    first_seen = {a: min(axis.matrix_order.index(t) for t in tactics
                         if tactics[t]["anchor"] == a) for a in anchors}
    badges = {a: badge_for(a, anchors[a], members[a]) for a in anchors}
    family_order = sorted(anchors, key=lambda a: (BADGE_ORDER.index(badges[a]),
                                                  first_seen[a]))

    version, pin = cat["meta"]["version"], axis.version
    banner = (f"% GENERATED by tools/dwell_catalogue_tables.py from\n"
              f"%   data/ogasp/tactic_durations.json ({version}); tactic axis and\n"
              f"%   display names from the pinned ATT&CK bundle (v{pin}).\n"
              f"% Do not hand-edit; regenerate. Requires booktabs (already in the preamble).\n")

    # ---------------------------------------------------------- chapter ----
    short = "Declared per-tactic dwell parameters"
    caption = (
        "The dwell parameters the movement layer declares for each tactic. "
        "Panel~(a) gives the anchor families and the off-network null; "
        f"panel~(b) the {len(tactics)} tactics that resolve onto them, so the "
        f"model carries {len(anchors) - 1} free timing parameters rather than "
        f"{len(tactics)}. A tactic's dwell is its family's value scaled by the "
        "multiplier shown, and that dwell is the \\emph{mean} of an exponential "
        "draw, $\\mathrm{Exp}(\\mu)$; resource development is the one exception, "
        "an immediate transition in the sense of "
        "Section~\\ref{subsec:petri-formalism} rather than a degenerate "
        "$\\mathrm{Exp}(0)$. The evidence column reads: \\emph{priced by MTDSim}, "
        "the value is the simulator's own action cost, inherited and not tuned; "
        "\\emph{declared and swept}, a declared value whose robustness across its "
        "band is reported in Appendix~\\ref{app:sensitivity}; \\emph{declared, "
        "off-clock}, no in-simulator dwell at all. \\emph{Priced from} names where "
        "a value's shape came from, which is not the action the tactic dispatches "
        "at run time --- for that mapping see "
        "Figure~\\ref{fig:controller-mapping}. A drawn dwell \\emph{replaces} the "
        "dispatched action's native cost rather than adding to it: an action "
        f"consumes its tactic's drawn time and nothing further. Values are emitted "
        f"from the declared catalogue ({esc(version)}); tactic names follow "
        f"ATT\\&CK~v{pin}."
    )

    L = [banner, r"\begin{table}[htbp]", r"\centering", r"\footnotesize",
         rf"\caption[{short}]{{{caption}}}", r"\label{tab:dwell-catalogue}",
         r"\begin{tabular}{@{}l l r l@{}}", r"\toprule",
         r"\multicolumn{4}{@{}l}{\emph{(a) Anchor families}}\\[2pt]",
         r"Family & Priced from & Value (s) & Evidence \\", r"\midrule"]
    for a in family_order:
        L.append(f"{FAMILY_LABEL[a]} & {esc(priced_from(a, anchors))} & "
                 f"{num(anchors[a]['duration_s'])} & {badges[a]} \\\\")
    L += [r"\bottomrule", r"\end{tabular}", "", r"\vspace{1em}", "",
          r"\begin{tabular}{@{}l l r r@{}}", r"\toprule",
          r"\multicolumn{4}{@{}l}{\emph{(b) Per tactic}}\\[2pt]",
          r"Tactic & Family & Mult. & Mean dwell (s) \\", r"\midrule"]
    for name in axis.matrix_order:
        e = tactics[name]
        mult = "---" if e["anchor"] == "prep-off-network" else f"{e['relative_multiplier']:.1f}"
        L.append(f"{esc(axis.label[name])} & {FAMILY_LABEL[e['anchor']]} & "
                 f"{mult} & {num(e['duration_s'])} \\\\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (OUT_DIR / "dwell_catalogue.tex").write_text("\n".join(L))

    # --------------------------------------------------------- appendix ----
    short_a = "Derivation of the declared dwell times"
    caption_a = (
        "How each declared dwell was arrived at. \\emph{Family} is the anchor the "
        "value takes its shape from; the per-family multipliers that separate "
        "tactics sharing one are in Table~\\ref{tab:dwell-catalogue}, which is why "
        "two tactics dispatching the same action can hold different dwells. "
        "\\emph{Sweep band} "
        "is the declared band the value may take, in units of its family anchor --- "
        "the band is a \\emph{parameter} declared here, while what happened when "
        "the anchors were moved across their bands is reported in "
        "Appendix~\\ref{app:sensitivity}. The catalogue that carries these values "
        "is the chapter's Table~\\ref{tab:dwell-catalogue}."
    )
    A = [banner, r"\begin{table}[htbp]", r"\centering", r"\scriptsize",
         r"\setlength{\tabcolsep}{4pt}",
         rf"\caption[{short_a}]{{{caption_a}}}", r"\label{tab:dwell-derivation}",
         r"\begin{tabular}{@{}l l r c p{0.40\textwidth}@{}}", r"\toprule",
         r"Tactic & Family & Value (s) & Sweep band & Why this value \\",
         r"\midrule"]
    for name in axis.matrix_order:
        e = tactics[name]
        lo, hi = e["sweep_range"]
        band = "---" if lo == hi == 0 else f"[{lo:g}, {hi:g}]"
        A.append(f"{esc(axis.label[name])} & {FAMILY_LABEL[e['anchor']]} & "
                 f"{num(e['duration_s'])} & {band} & {esc(e['short_justification'])} \\\\")
    A += [r"\bottomrule",
          r"\addlinespace[2pt]",
          r"\multicolumn{5}{@{}p{0.96\textwidth}@{}}{\scriptsize Values, bands and "
          r"rationales are emitted from the declared catalogue "
          rf"(\texttt{{data/ogasp/tactic\_durations.json}}, {esc(version)}); tactic "
          rf"names follow ATT\&CK~v{pin}. A degenerate band (resource development) "
          r"is shown as a dash: the tactic is off-clock, so there is nothing to "
          r"sweep.}\\",
          r"\end{tabular}", r"\end{table}", ""]
    (OUT_DIR / "dwell_derivation.tex").write_text("\n".join(A))

    print(f"wrote {OUT_DIR/'dwell_catalogue.tex'}")
    print(f"wrote {OUT_DIR/'dwell_derivation.tex'}")
    print(f"  {len(tactics)} tactics, {len(anchors)} families, "
          f"{len(set(t['duration_s'] for t in tactics.values()))} distinct values; "
          f"catalogue {version}, ATT&CK v{pin}")


if __name__ == "__main__":
    main()
