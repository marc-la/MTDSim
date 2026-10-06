#!/usr/bin/env python3
"""Table 5.6 (tab:ablation), section 5.4's headline float: both ablations in one
form, cited by both subsections (Marc 2026-10-01: "one table 5.6 covering both
ablations in one form"; "the main headline figure of 5.4 [is] the table and
both of the subsections talk about it").

TAKEAWAYS it carries (the scrutiny record, handoff 2026-09-28_vulnerability_memory_on.md):
  T3  neither component moves NCR: every Cohen's d below 0.2;
  T4  neither moves the headline: NCR reduction with and without side by side.
The manipulation checks (T2) are body sentences, not columns: the failure
matrix's is the declared weight read back, and the two components' checks are
different measures, so a shared column would mean two things.

FORM. Rows: a group per component (an italic group row, so no zebra stripes,
figure_table_conventions.md precision section), each "no MTD" first, then its
MTD mechanisms. Columns: NCR with, without and Cohen's d on NCR (its 95 %
bootstrap interval over seeds); NCR reduction with and without. With first,
the model as evaluated. One comparison statistic: the raw difference columns
are gone (their intervals excluded zero where d called the effect negligible,
and the rounded columns did not subtract to them). d on per-seed NCR reduction
was computed and rejected (memory_ablation.py, the comment on
reduction_on_minus_off). The vulnerability memory's rows are at 20 services per
operating system, the network of every other result; its pool sweep is Figure
5.7 and Appendix F's table.

PRECISION. NCR to three decimals (its interval's half-width is 0.0004 to 0.0026
at 1 000 seeds), NCR reduction to two as the chapter's other tables print it,
d to two. Half-up rounding.

KNOWN. The failure-matrix ablation ran with the memory off (its core arm at
seeds 0-99 is bit-identical to the memory ablation's off arm); its 1 000-seed
rerun with the memory on is owed, after which the two no-MTD "with" rows are
the same model and agree.

REBUILT 2026-10-06 (Marc, section 5.4: "lots of gaps"; "I don't know why we added the NCR
reduction column ... that's not what we performed the statistical [test] on"): overturns T4 and
the L4 random column on merit. The NCR reduction columns printed two untested point values side
by side and left the no-MTD rows blank; d on NCR under each MTD already says whether a component
changes what the attacker achieves there. The random-partition control moves to Appendix F's
own table (tab_F-4), which carries each partition's spread, as the 5.4.1 prose needs it; in
Table 5.4 it was blank in two of the three blocks. What is left is with, without and d in every
row, so no cell is blank. Rows under each group row are indented, as Table 5.1's are. The caption
decodes only: the held pool size is Table 5.1's, the attack graph is Section 5.4.1's.

    python data/results/ch5_defended/ablation_table.py
"""
from __future__ import annotations

import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
FM = HERE / "ablation_numbers_memory.json"  # 2026-10-02: the failure-matrix ablation with the memory on, 1 000 seeds
PART = HERE / "partition_ablation_numbers.json"  # 2026-10-02: the attack profiles against the attack graph
MEM = HERE / "memory_ablation_numbers.json"
# 2026-10-06 (L4, Marc "OK"): the size-matched random-partition control as a column, so section 5.4.1
#   reads it from a float: the mean over the ten partitions, NCR and NCR reduction (each partition
#   against its own no-MTD runs), in the attack-profiles block only; blank elsewhere (not applicable).
CTRL = HERE / "partition_control_numbers.json"
TABLE = HERE.parents[2] / "docs" / "thesis" / "tables" / "tab_5-4a_ablation.tex"
CTRL_TABLE = HERE.parents[2] / "docs" / "thesis" / "tables" / "tab_F-4_ablation_random_partitions.tex"
HOSTS = 50
POOL = 20  # services per operating system in every other result of chapter 5


def _f(x: float, nd: int, sign: bool = False) -> str:
    q = Decimal(repr(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    if q == 0:
        return f"{0:.{nd}f}"
    s = f"{q:+.{nd}f}" if sign else f"{q:.{nd}f}"
    return "$" + s + "$" if s.startswith(("+", "-")) else s


# rows whose interval crosses +-0.2, inconclusive under Section 5.1's equivalence
# rule: not bold, and named in the caption, so the reader is not left to ask why
# (Marc 2026-10-05; the three verdicts, Marc 2026-10-06)
NAMED: list = []


def _beyond(ci: list) -> bool:
    return ci[1] <= -0.2 or ci[0] >= 0.2


def _d(d: float, ci: list, where: str = "") -> str:
    """d and its interval at two places, every cell (Marc 2026-10-05: one
    precision in the column; the 2026-10-02 extra places where an edge rounded
    onto 0.2 are gone), bold where the unrounded interval lies wholly beyond
    +-0.2 (Marc 2026-10-02: the reader must see at once what is negligible).
    The dagger for an interval that crosses an edge is gone too: the interval
    is printed, and the one case a reader would query, a d beyond 0.2 that is
    not bold, is named in the caption."""
    cell = f"{_f(d, 2, True)} [{_f(ci[0], 2, True)}, {_f(ci[1], 2, True)}]"
    if _beyond(ci):
        return r"\bfseries\boldmath " + cell
    if (ci[0] <= -0.2 or ci[1] >= 0.2) and where:
        NAMED.append((where, d))
    return cell


def rows() -> list:
    fm, mem = json.loads(FM.read_text())["reads"], json.loads(MEM.read_text())["reads"]
    part = json.loads(PART.read_text())["by_n"]["1000"]["outcome"]["shared"]
    out = [r"\emph{Attack profiles by objective}"]  # first, in chapter 4's order (Marc 2026-10-02)
    for key, label in [("none|0", "no MTD"), ("ip_shuffle|200", r"IP shuffle, 200\,s"),
                       ("ip_shuffle|2000", r"IP shuffle, 2\,000\,s"), ("os_diversity|200", r"OS diversity, 200\,s"),
                       ("os_diversity|2000", r"OS diversity, 2\,000\,s")]:
        r = part[key]
        out.append([label, _f(r["ncr_with"], 3), _f(r["ncr_without"], 3),
                    _d(r["cohen_d"], r["cohen_d_ci95"], f"{label} without the attack profiles")])
    out.append(r"\emph{Failure matrix}")
    for key, label in [("none", "no MTD"), ("ip_shuffle|200", r"IP shuffle, 200\,s"),
                       ("ip_shuffle|2000", r"IP shuffle, 2\,000\,s"), ("os_diversity|200", r"OS diversity, 200\,s"),
                       ("os_diversity|2000", r"OS diversity, 2\,000\,s")]:
        r = fm[key]
        out.append([label, _f(r["hosts_with"] / HOSTS, 3), _f(r["hosts_without"] / HOSTS, 3),
                    _d(r["cohen_d_per_seed"], r["cohen_d_ci95"], f"{label} without the failure matrix")])
    out.append(r"\emph{Vulnerability memory}")
    for cond, label in [("none", "no MTD"), ("service_diversity", r"service diversity, 200\,s"),
                        ("os_diversity", r"OS diversity, 200\,s")]:
        r = mem[f"{POOL}|{cond}"]
        a, o = r["arms"], r["on_minus_off"]
        out.append([label, _f(a["on"]["ncr"], 3), _f(a["off"]["ncr"], 3), _d(o["cohen_d"], o["cohen_d_ci95"], f"{label} without the vulnerability memory")])
    return out


def _named() -> str:
    """The caption's verdicts beyond bold (Section 5.1): the inconclusive rows,
    whose interval crosses +-0.2, by name; every other row negligible. Built
    from the data, so it follows the numbers."""
    # 2026-10-06: decode only; the rule itself is Section 5.1's
    ref = " (Section~\\ref{sec:dimensions})."
    if not NAMED:
        return " Not bold: negligible" + ref
    items = [where.replace(",", " at", 1) for where, _ in NAMED]
    return " Not bold: negligible, but inconclusive for " + (
        items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]) + ref


def main() -> None:
    body = []
    for r in rows():
        if isinstance(r, str):
            if body:
                body.append(r"    \addlinespace")
            body.append(rf"    \grouprow{{4}}{{{r[len(chr(92)+'emph{'):-1]}}} \\")
        else:
            body.append("    " + r"\quad " + " & ".join(r) + r" \\")  # indented under its group row, as Table 5.1
    tex = [
        "% GENERATED by data/results/ch5_defended/ablation_table.py from ablation_numbers.json and",
        "% memory_ablation_numbers.json and partition_ablation_numbers.json; never hand-edit. Section 5.4's headline float,",
        "% cited by all three subsections. The attack-profiles block and its marking added 2026-10-02, DRAFT STATE.",
        "% Caption DRAFT STATE 2026-10-01, ratify on read.",
        r"\begin{table}[!ht]",  # 2026-10-07 (Marc: alone and centred on a float page at the chapter end): here, after 5.4's preamble
        r"  \centering",
        (r"  \caption[The APT attacker model with and without each component]{The APT attacker model "
         r"with and without each component, averaged over $c_1$ to $c_4$. "
         # 2026-10-06 (Marc: "is this something that we already give the reader ... in 5.1";
         #  "why would you judge it on an interval before rounding"; "why do you need to put this
         #  specific example"): decode the one mark only. d, its sign and its interval are Section
         #  5.1's (the sign moved there); the three verdicts are 5.1's rule, read off the printed
         #  interval, so the inconclusive row needs no naming (_named() is kept, unused, as the
         #  check); "before rounding" is how every verdict is computed, said for one cell
         #  (OS diversity at 200 s without the attack profiles, upper end -0.2003, printed -0.20).
         r"Bold: not negligible (Section~\ref{sec:dimensions}).}"),
        r"  \label{tab:ablation}",
        r"  \tablestyle",  # group rows keep the stripes (Marc, 2026-10-01)
        r"  \begin{tabular}{@{}lccc@{}}",
        r"    \toprule",
        r"    & \multicolumn{2}{c}{NCR} & \\",
        r"    \cmidrule(lr){2-3}",
        r"    \rowcolor{white}MTD & with & without & $d$ \\",
        r"    \midrule",
    ] + body + [r"    \bottomrule", r"  \end{tabular}", r"\end{table}", ""]
    TABLE.write_text("\n".join(tex), encoding="utf-8")
    print(f"wrote {TABLE.relative_to(HERE.parents[2])}")
    control_table()


def control_table() -> None:
    """Appendix F's table of the size-matched control (Section 5.4, Table 5.1).
    2026-10-06 (Marc: "is it statistically significant or not is the figure I would bring up"):
    rebuilt from NCR values to the verdict, in Table E.6's form: d on NCR, the attack profiles
    minus each random partition (partition_control.py, Table 5.4's design), one row per
    partition, bold where not negligible. The interval is not printed (five intervals do not
    fit the width), so the caption names the cells that are inconclusive, the one verdict the
    bold leaves open. The NCR values it printed before (mean, lowest, highest) are dropped:
    the prose now reads the verdict, and the attack profiles' and attack graph's NCR are
    Table 5.4's."""
    c = json.loads(CTRL.read_text())
    assert c["n_seeds"] == 1000
    keys = ["none|0", "ip_shuffle|200", "ip_shuffle|2000", "os_diversity|200", "os_diversity|2000"]
    names = {"none|0": "no MTD", "ip_shuffle|200": r"IP shuffle at 200\,s", "ip_shuffle|2000": r"IP shuffle at 2\,000\,s",
             "os_diversity|200": r"OS diversity at 200\,s", "os_diversity|2000": r"OS diversity at 2\,000\,s"}
    parts = sorted(c["cells"]["none|0"]["random"], key=int)
    body, inconclusive, counts = [], [], {"not negligible": 0, "negligible": 0, "inconclusive": 0}
    for k in parts:
        row = [str(int(k) + 1)]
        for key in keys:
            r = c["cells"][key]["random"][k]
            v = r["verdict_profiles_minus"]
            counts[v] += 1
            cell = _f(r["cohen_d_profiles_minus"], 2, True)
            if v == "not negligible":
                cell = r"\bfseries\boldmath " + cell
            elif v == "inconclusive":
                inconclusive.append(f"partition {int(k) + 1} under {names[key]}" if key != "none|0"
                                    else f"partition {int(k) + 1} with no MTD")
            row.append(cell)
        body.append("    " + " & ".join(row) + r" \\")
    rest = (" Not bold: negligible" + (", but inconclusive for " + " and ".join(inconclusive) if inconclusive else "")
            + r" (Section~\ref{sec:dimensions}).")
    print(f"control verdicts over {len(parts) * len(keys)} comparisons: {counts}")
    tex = [
        "% GENERATED by data/results/ch5_defended/ablation_table.py (control_table) from",
        "% partition_control_numbers.json; never hand-edit. Section 5.4's size-matched control:",
        "% 2026-10-06 moved here from Table 5.4's random column, then rebuilt to d and its verdict. DRAFT STATE.",
        r"\begin{table}[tp]",
        r"  \centering",
        (r"  \caption[The attack profiles against random partitions of the attack flows]"
         r"{$d$ on NCR of the APT attacker model averaged over $c_1$ to $c_4$, the attack profiles minus each of "
         r"10 random partitions of the attack flows (Section~\ref{subsec:ablation-attack-profiles}). "
         r"Bold: not negligible." + rest + "}"),
        r"  \label{tab:ablation-random-partitions}",
        r"  \tablestyle",
        r"  \begin{tabular}{@{}cccccc@{}}",
        r"    \toprule",
        r"    & & \multicolumn{2}{c}{IP shuffle} & \multicolumn{2}{c}{OS diversity} \\",
        r"    \cmidrule(lr){3-4}\cmidrule(lr){5-6}",
        r"    \rowcolor{white}Random partition & no MTD & 200\,s & 2\,000\,s & 200\,s & 2\,000\,s \\",
        r"    \midrule",
    ] + body + [r"    \bottomrule", r"  \end{tabular}", r"\end{table}", ""]
    CTRL_TABLE.write_text("\n".join(tex), encoding="utf-8")
    print(f"wrote {CTRL_TABLE.relative_to(HERE.parents[2])}")

if __name__ == "__main__":
    main()
