"""The dwell-time catalogue tables --- chapter parameter table + appendix derivation.

Two floats from one declared family, emitted from `data/ogasp/tactic_durations.json`
so no value is ever typed (`figure_table_conventions.md` §h):

* `tab:dwell-catalogue` (§4.4.2) --- the **what**: one panel, tactic and mean
  dwell, nothing else. Marc's ruling 2026-09-08 (pass 5, front-loading): the
  chapter table prescribes what the model runs with; the why belongs to the
  appendix and the sensitivity analysis.
* `tab:dwell-anchors` (`app:dwell-derivation`) --- the former chapter panel
  (a): the anchor families and the null, with the evidence badges (a badge is
  constant within a family) and the four-free-parameters-not-fifteen count.
* `tab:dwell-derivation` (`app:dwell-derivation`) --- the **why**: per-tactic
  family, multiplier, sweep band and the short justification, dense on purpose.

The what/why split is Marc's ruling (2026-08-20); the one-panel chapter table
his ruling of 2026-09-08.

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
    "scan-shaped": "MTDSim's scan attack actions, one enumeration pass",
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
    # ONE PANEL since 2026-09-08 (Marc, pass 5): the chapter table prescribes
    # what the model runs with --- tactic and mean dwell, nothing else. The
    # families, the evidence badges and the multipliers are the appendix's
    # (tab:dwell-anchors, tab:dwell-derivation below).
    short = "Declared per-tactic dwell times"
    caption = (
        "The dwell times declared for each tactic: the mean "
        "dwell $\\mu_p$ of Equation~\\ref{eq:gspn}, the \\emph{mean} of an "
        "exponential draw. Values are emitted from the declared catalogue "
        f"({esc(version)}); tactic names follow ATT\\&CK~v{pin}. How each value "
        "was arrived at is Appendix~\\ref{app:dwell-derivation}."
    )
    L = [banner, r"\begin{table}[htbp]", r"\centering", r"\footnotesize",
         rf"\caption[{short}]{{{caption}}}", r"\label{tab:dwell-catalogue}",
         r"\begin{tabular}{@{}l r@{}}", r"\toprule",
         r"Tactic & Mean dwell $\mu_p$ (s) \\", r"\midrule"]
    for name in axis.matrix_order:
        e = tactics[name]
        L.append(f"{esc(axis.label[name])} & {num(e['duration_s'])} \\\\")
    L += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (OUT_DIR / "tab_4-4a_dwell_catalogue.tex").write_text("\n".join(L))

    # ------------------------------------------- appendix: anchor families ----
    # The former chapter panel (a), moved to the appendix 2026-09-08.
    short_f = "Anchor families of the declared dwell times"
    caption_f = (
        f"The anchor families the {len(tactics)} declared dwell times resolve "
        f"onto, so the model carries {len(anchors) - 1} free timing parameters "
        f"rather than {len(tactics)}. \\emph{{Priced from}} names where a "
        "value's shape came from, which is not the attack action the tactic dispatches "
        "at run time --- for that mapping see Figure~\\ref{fig:controller-mapping}. "
        "The evidence column reads: \\emph{priced by MTDSim}, the value is the "
        "simulator's own attack action cost, inherited and not tuned; \\emph{declared "
        "and swept}, a declared value whose robustness across its band is "
        "reported in Appendix~\\ref{app:sensitivity}; \\emph{declared, off-clock}, "
        "no in-simulator dwell at all --- resource development is an immediate "
        "transition in the sense of Section~\\ref{sec:petri-formalism} rather "
        "than a degenerate $\\mathrm{Exp}(0)$. A tactic's dwell is its family's "
        "value scaled by the multiplier in Table~\\ref{tab:dwell-derivation}."
    )
    F = [banner, r"\begin{table}[htbp]", r"\centering", r"\footnotesize",
         rf"\caption[{short_f}]{{{caption_f}}}", r"\label{tab:dwell-anchors}",
         r"\begin{tabular}{@{}l l r l@{}}", r"\toprule",
         r"Family & Priced from & Value (s) & Evidence \\", r"\midrule"]
    for a in family_order:
        F.append(f"{FAMILY_LABEL[a]} & {esc(priced_from(a, anchors))} & "
                 f"{num(anchors[a]['duration_s'])} & {badges[a]} \\\\")
    F += [r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (OUT_DIR / "tab_B-4b_dwell_anchors.tex").write_text("\n".join(F))

    # --------------------------------------------------------- appendix ----
    short_a = "Derivation of the declared dwell times"
    caption_a = (
        "How each declared dwell was arrived at. \\emph{Family} is the anchor the "
        "value takes its shape from (Table~\\ref{tab:dwell-anchors}); "
        "\\emph{Mult.} is the per-family multiplier that separates tactics "
        "sharing one, which is why two tactics dispatching the same attack action can "
        "hold different dwells. \\emph{Sweep band} "
        "is the declared band the value may take, in units of its family anchor --- "
        "the band is a \\emph{parameter} declared here, while what happened when "
        "the anchors were moved across their bands is reported in "
        "Appendix~\\ref{app:sensitivity}. The catalogue that carries these values "
        "is the chapter's Table~\\ref{tab:dwell-catalogue}."
    )
    A = [banner, r"\begin{table}[htbp]", r"\centering", r"\scriptsize",
         r"\setlength{\tabcolsep}{4pt}",
         rf"\caption[{short_a}]{{{caption_a}}}", r"\label{tab:dwell-derivation}",
         r"\begin{tabular}{@{}l l r r c p{0.355\textwidth}@{}}", r"\toprule",
         r"Tactic & Family & Mult. & Value (s) & Sweep band & Why this value \\",
         r"\midrule"]
    for name in axis.matrix_order:
        e = tactics[name]
        lo, hi = e["sweep_range"]
        band = "---" if lo == hi == 0 else f"[{lo:g}, {hi:g}]"
        mult = "---" if e["anchor"] == "prep-off-network" else f"{e['relative_multiplier']:.1f}"
        A.append(f"{esc(axis.label[name])} & {FAMILY_LABEL[e['anchor']]} & {mult} & "
                 f"{num(e['duration_s'])} & {band} & {esc(e['short_justification'])} \\\\")
    A += [r"\bottomrule",
          r"\addlinespace[2pt]",
          r"\multicolumn{6}{@{}p{0.96\textwidth}@{}}{\scriptsize Values, bands and "
          r"rationales are emitted from the declared catalogue "
          rf"(\texttt{{data/ogasp/tactic\_durations.json}}, {esc(version)}); tactic "
          rf"names follow ATT\&CK~v{pin}. A degenerate band (resource development) "
          r"is shown as a dash: the tactic is off-clock, so there is nothing to "
          r"sweep.}\\",
          r"\end{tabular}", r"\end{table}", ""]
    (OUT_DIR / "tab_B-4a_dwell_derivation.tex").write_text("\n".join(A))

    print(f"wrote {OUT_DIR/'tab_4-4a_dwell_catalogue.tex'}")
    print(f"wrote {OUT_DIR/'tab_B-4b_dwell_anchors.tex'}")
    print(f"wrote {OUT_DIR/'tab_B-4a_dwell_derivation.tex'}")
    print(f"  {len(tactics)} tactics, {len(anchors)} families, "
          f"{len(set(t['duration_s'] for t in tactics.values()))} distinct values; "
          f"catalogue {version}, ATT&CK v{pin}")


if __name__ == "__main__":
    main()
