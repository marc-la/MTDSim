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
HOSTS = 50
POOL = 20  # services per operating system in every other result of chapter 5


def _f(x: float, nd: int, sign: bool = False) -> str:
    q = Decimal(repr(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    if q == 0:
        return f"{0:.{nd}f}"
    s = f"{q:+.{nd}f}" if sign else f"{q:.{nd}f}"
    return "$" + s + "$" if s.startswith(("+", "-")) else s


# rows whose d lies beyond +-0.2 but whose interval reaches inside it: not bold,
# and named in the caption, so the reader is not left to ask why (Marc 2026-10-05)
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
    if abs(d) >= 0.2 and where:
        NAMED.append((where, d))
    return cell


def rows() -> list:
    fm, mem = json.loads(FM.read_text())["reads"], json.loads(MEM.read_text())["reads"]
    part = json.loads(PART.read_text())["by_n"]["1000"]["outcome"]["shared"]
    ctrl = json.loads(CTRL.read_text())["cells"]
    assert json.loads(CTRL.read_text())["n_seeds"] == 1000

    def rnd(key):
        ncr = [v["ncr"] for v in ctrl[key]["random"].values()]
        if key == "none|0":
            return _f(sum(ncr) / len(ncr), 3), ""
        red = [1 - ctrl[key]["random"][i]["ncr"] / ctrl["none|0"]["random"][i]["ncr"] for i in ctrl[key]["random"]]
        return _f(sum(ncr) / len(ncr), 3), _f(sum(red) / len(red), 2)
    out = [r"\emph{Attack profiles by objective}"]  # first, in chapter 4's order (Marc 2026-10-02)
    for key, label in [("none|0", "no MTD"), ("ip_shuffle|200", r"IP shuffle, 200\,s"),
                       ("ip_shuffle|2000", r"IP shuffle, 2\,000\,s"), ("os_diversity|200", r"OS diversity, 200\,s"),
                       ("os_diversity|2000", r"OS diversity, 2\,000\,s")]:
        r = part[key]
        red = ([_f(r["ncr_reduction_with"], 2), _f(r["ncr_reduction_without"], 2)]
               if "ncr_reduction_with" in r else ["", ""])
        rn, rr = rnd(key)
        out.append([label, _f(r["ncr_with"], 3), _f(r["ncr_without"], 3),
                    _d(r["cohen_d"], r["cohen_d_ci95"], f"{label} without the attack profiles"), rn] + red + [rr])
    out.append(r"\emph{Failure matrix}")
    for key, label in [("none", "no MTD"), ("ip_shuffle|200", r"IP shuffle, 200\,s"),
                       ("ip_shuffle|2000", r"IP shuffle, 2\,000\,s"), ("os_diversity|200", r"OS diversity, 200\,s"),
                       ("os_diversity|2000", r"OS diversity, 2\,000\,s")]:
        r = fm[key]
        red = ([_f(r["ncr_reduction_with"], 2), _f(r["ncr_reduction_without"], 2)]
               if "ncr_reduction_with" in r else ["", ""])
        out.append([label, _f(r["hosts_with"] / HOSTS, 3), _f(r["hosts_without"] / HOSTS, 3),
                    _d(r["cohen_d_per_seed"], r["cohen_d_ci95"], f"{label} without the failure matrix"), ""] + red + [""])
    out.append(r"\emph{Vulnerability memory}")
    for cond, label in [("none", "no MTD"), ("service_diversity", r"service diversity, 200\,s"),
                        ("os_diversity", r"OS diversity, 200\,s")]:
        r = mem[f"{POOL}|{cond}"]
        a, o = r["arms"], r["on_minus_off"]
        red = ([_f(r["reduction"]["on"]["ncr_reduction"], 2), _f(r["reduction"]["off"]["ncr_reduction"], 2)]
               if "reduction" in r else ["", ""])
        out.append([label, _f(a["on"]["ncr"], 3), _f(a["off"]["ncr"], 3), _d(o["cohen_d"], o["cohen_d_ci95"], f"{label} without the vulnerability memory"), ""] + red + [""])
    return out


def _named() -> str:
    """The caption's sentence on the rows a reader would query: d beyond 0.2,
    not bold. Built from the data, so it follows the numbers."""
    if not NAMED:
        return ""
    def one(where, d):
        return r"%s, whose $d$ of $%s$ lies beyond it" % (where.replace(",", " at", 1), _f(d, 2, True).strip("$"))
    items = [one(*x) for x in NAMED]
    return " Every other interval reaches inside $\\pm 0.2$, including " + (
        items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]) + "."


def main() -> None:
    body = []
    for r in rows():
        if isinstance(r, str):
            if body:
                body.append(r"    \addlinespace")
            body.append(rf"    \grouprow{{8}}{{{r[len(chr(92)+'emph{'):-1]}}} \\")
        else:
            body.append("    " + " & ".join(r) + r" \\")
    tex = [
        "% GENERATED by data/results/ch5_defended/ablation_table.py from ablation_numbers.json and",
        "% memory_ablation_numbers.json and partition_ablation_numbers.json; never hand-edit. Section 5.4's headline float,",
        "% cited by all three subsections. The attack-profiles block and its marking added 2026-10-02, DRAFT STATE.",
        "% Caption DRAFT STATE 2026-10-01, ratify on read.",
        r"\begin{table}[tp]",
        r"  \centering",
        (r"  \caption[The APT attacker model with and without each ablated component]{The APT attacker model "
         r"with and without each ablated component, averaged over $c_1$ to $c_4$, on the same 1\,000 seeds, "
         r"with 20 services per operating system; without the attack profiles, the APT attacker model runs on the attack graph: "
         r"NCR, $d$ on NCR, with minus without, with its 95\,\% percentile bootstrap interval "
         r"over seeds, and NCR reduction (Section~\ref{sec:evaluation-metrics}), blank with no MTD, its reference. "
         r"Random: the mean over ten random partitions of the attack flows, each group the size of an attack profile, "
         r"each partition's NCR reduction against its own runs with no MTD; blank outside the attack profiles' ablation. "
         r"Bold: the interval, before rounding, lies wholly beyond $\pm 0.2$." + _named() + "}"),
        r"  \label{tab:ablation}",
        r"  \tablestyle\setlength{\tabcolsep}{4pt}",  # group rows keep the stripes (Marc, 2026-10-01); 4 pt fits the random columns
        r"  \begin{tabular}{@{}lccccccc@{}}",
        r"    \toprule",
        r"    & \multicolumn{4}{c}{NCR} & \multicolumn{3}{c}{NCR reduction} \\",
        r"    \cmidrule(lr){2-5}\cmidrule(lr){6-8}",
        r"    \rowcolor{white}MTD & with & without & $d$ & random & with & without & random \\",
        r"    \midrule",
    ] + body + [r"    \bottomrule", r"  \end{tabular}", r"\end{table}", ""]
    TABLE.write_text("\n".join(tex), encoding="utf-8")
    print(f"wrote {TABLE.relative_to(HERE.parents[2])}")


if __name__ == "__main__":
    main()
