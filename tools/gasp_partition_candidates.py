"""Emit the rejected-partition appendix table (app:rejected-partitions).

Why: §4.2.2 says "Six other partitions were considered and dismissed" and
points at the appendix for them. This writes that float from a tracked ledger
plus the artefacts themselves, so no number on the page is typed.

Structure of the seam:

  data/gasp/partition_candidates.csv   the ledger — one row per candidate
      scheme (seven, six dismissed plus the adopted one). Carries the PROSE
      (row label, what the scheme slices on, the dismissal clause) and, in
      `outcome_template`, a sentence with {named} placeholders. It carries no
      numbers of its own except where none can be computed (the 47-campaign
      hand-label sample, which has no tracked artefact — flagged TYPED below).

  data/gasp/metadata_audit.csv         the corpus. Every substituted number is
      read or derived from here.

  tools/gasp_structural_baseline.py    Def A, the reach read and the two
      concordance rules are IMPORTED, never re-implemented. That tool emits the
      sibling audit table and pins the same 19-of-38 the chapter cites at
      l.482, so a second copy of the definition would be a second thing to drift.

Freshness gate: the tool refuses to write if the corpus is not the validated
post-ruling one (38 flows, 19/7/7/5, 38 high confidence) or if the ledger does
not hold exactly six dismissed schemes — the chapter's word is "Six".

Run from the repo root:
    PYTHONPATH=src python tools/gasp_partition_candidates.py [--check]
--check computes and prints the fact sheet without writing the .tex.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gasp_structural_baseline import (  # noqa: E402
    AUDIT,
    ROOT,
    concordance,
    load_flow,
    read_reach,
    read_terminal,
)

LEDGER = ROOT / "data" / "gasp" / "partition_candidates.csv"
GAP = ROOT / "data" / "gap" / "gap_v0.5.json"
TEX_OUT = ROOT / "docs" / "thesis" / "tables" / "tab_B-3a_rejected_partitions.tex"

# The corpus state this float is licensed against (structural_baseline.md).
EXPECT_N = 38
EXPECT_SPLIT = {"steal_data": 19, "impediment": 7, "double_extortion": 7,
                "position_for_future": 5}
EXPECT_DISMISSED = 6

# The one figure with no tracked artefact behind it: Marc's hand-label sample,
# recorded in gasp_schema.md Decision 2. Typed, and printed as typed.
TYPED = {"p4_campaigns": 47, "p4_categories": 10, "p4_used": 3}


def pins() -> dict[str, str]:
    """Corpus version pins for the caption, from the GAP artefact itself."""
    g = json.loads(GAP.read_text())
    ref = g["corpus_ref"]
    flow_v = ref.split("@", 1)[1].split(" ", 1)[0] if "@" in ref else ref
    attack = g["attack_source"].replace("enterprise-attack-", "")
    return {"flow_corpus": flow_v, "attack": attack,
            "schema": g["attack_flow_schema_version"]}


def facts() -> dict[str, object]:
    rows = list(csv.DictReader(open(AUDIT)))
    n = len(rows)
    f: dict[str, object] = {"n_flows": n}

    # -- adopted scheme -------------------------------------------------
    split = Counter(r["stated_objective"] for r in rows)
    f.update(a_exfil=split["steal_data"], a_impact=split["impediment"],
             a_both=split["double_extortion"], a_none=split["position_for_future"])
    f["_conf"] = Counter(r["metadata_confidence"] for r in rows)

    # -- attribution (p3) -----------------------------------------------
    attr = [(r.get("attribution") or "").strip() for r in rows]
    f["p3_g"] = sum(1 for a in attr if a.upper().startswith("G"))
    f["p3_c"] = sum(1 for a in attr if a.upper().startswith("C"))
    f["p3_none"] = sum(1 for a in attr if a in ("", "unknown"))
    f["p4_cid"] = f["p3_c"]  # the hand-labels join on Campaign ids; none exist

    # -- structural reads (p1, p7) via the baseline tool ------------------
    t_reads, r_reads, term_sets, term_techs, cyclic = [], [], Counter(), set(), 0
    for r in rows:
        flow = load_flow(r["flow_id"])
        t_read, techs, _ = read_terminal(flow)
        t_reads.append((t_read, r["stated_objective"]))
        r_reads.append((read_reach(flow), r["stated_objective"]))
        term_sets[tuple(techs)] += 1
        term_techs.update(techs)
        if not techs:
            cyclic += 1

    def summarise(pairs, prefix):
        c = Counter(x for x, _ in pairs)
        f[f"{prefix}_exfil"] = c["exfil"]
        f[f"{prefix}_impact"] = c["impact"]
        f[f"{prefix}_both"] = c["both"]
        f[f"{prefix}_neither"] = c["neither"]
        f[f"{prefix}_exact"] = sum(1 for rd, au in pairs if not concordance(rd, au)[0])
        f[f"{prefix}_any"] = sum(1 for rd, au in pairs if not concordance(rd, au)[1])

    summarise(t_reads, "p1")
    summarise(r_reads, "p7")

    # composition of p1's exact disagreements — the chapter's real point
    f["p1_silent"] = sum(1 for rd, au in t_reads
                         if not concordance(rd, au)[0] and rd == "neither")
    f["p1_ransom"] = sum(1 for rd, au in t_reads
                         if not concordance(rd, au)[0] and rd == "impact"
                         and au == "double_extortion")

    # -- terminal-technique fragmentation (p2) ----------------------------
    f["p2_sets"] = len(term_sets)
    f["p2_singletons"] = sum(1 for v in term_sets.values() if v == 1)
    f["p2_techs"] = len(term_techs)
    f["p2_cyclic"] = cyclic

    # -- three-class multi-membership (p5) --------------------------------
    f["p5_exfil"] = split["steal_data"] + split["double_extortion"]
    f["p5_impact"] = split["impediment"] + split["double_extortion"]
    f["p5_none"] = split["position_for_future"]
    f["p5_dual"] = split["double_extortion"]
    f["p5_total"] = f["p5_exfil"] + f["p5_impact"] + f["p5_none"]

    f.update(TYPED)
    return f


def gate(f: dict, ledger: list[dict]) -> None:
    conf = f.pop("_conf")
    problems = []
    if f["n_flows"] != EXPECT_N:
        problems.append(f"corpus is {f['n_flows']} flows, expected {EXPECT_N}")
    got = {"steal_data": f["a_exfil"], "impediment": f["a_impact"],
           "double_extortion": f["a_both"], "position_for_future": f["a_none"]}
    if got != EXPECT_SPLIT:
        problems.append(f"class split {got} != validated {EXPECT_SPLIT}")
    if conf["high"] != EXPECT_N:
        problems.append(f"audit confidence is {dict(conf)}, expected all high")
    n_dis = sum(1 for r in ledger if r["status"] == "dismissed")
    if n_dis != EXPECT_DISMISSED:
        problems.append(f"ledger holds {n_dis} dismissed schemes; the chapter says six")
    if problems:
        print("REFUSING TO EMIT — stop and report, do not regenerate silently:")
        for p in problems:
            print("  -", p)
        sys.exit(1)


def _tex(s: str) -> str:
    return (s.replace("\\", "\\textbackslash{}").replace("&", "\\&")
             .replace("%", "\\%").replace("$", "\\$").replace("#", "\\#")
             .replace("_", "\\_"))


def build(f: dict, ledger: list[dict], p: dict) -> str:
    caption = (
        "Partition schemes considered for the objective-conditioned attack "
        "profiles, and what each produced on this corpus. Rows are ordered by "
        "how far the evidence a scheme reads sits from the analyst's own "
        "statement of what the operation did; the six above the rule were "
        "dismissed, and the row below it is the scheme the pipeline adopts. "
        "For the three schemes read from the incident's dependency graph, a "
        "technique is terminal when it has no outgoing edge to a different "
        "technique, and the disagreement counts are against the attested "
        "objective --- requiring an exact match, then in brackets allowing the "
        "two to share one objective tactic. A tick marks a scheme whose class "
        "membership could still be derived from artefacts this pipeline holds; "
        "an empty cell, one that cannot be built on this corpus at all. "
        f"Attack Flow published export {p['flow_corpus']} (schema "
        f"{p['schema']}), {f['n_flows']} usable incidents, ATT\\&CK Enterprise "
        f"v{p['attack']}. Every count is computed from the classification "
        f"audit at generation; the {f['p4_campaigns']}-campaign hand-label "
        "sample in the first row is the one figure reported from the project "
        "record."
    )
    out = [
        "% GENERATED by tools/gasp_partition_candidates.py from",
        "%   data/gasp/partition_candidates.csv (the prose ledger) and",
        "%   data/gasp/metadata_audit.csv (every number). Def A, the reach read and",
        "%   the concordance rules are imported from tools/gasp_structural_baseline.py,",
        "%   which emits the sibling audit table --- the 19-of-38 count appears in both",
        "%   floats and in the chapter at sec:attack-profiles, so it has one home.",
        "% Do not hand-edit; regenerate. Requires booktabs (already in the preamble).",
        f"% Corpus at generation: {f['n_flows']} flows, "
        f"{f['a_exfil']}/{f['a_impact']}/{f['a_both']}/{f['a_none']}, all high confidence.",
        "",
        "\\begin{table}[htbp]",
        "\\centering",
        "\\scriptsize",
        "\\setlength{\\tabcolsep}{4pt}",
        "\\newcolumntype{R}[1]{>{\\raggedright\\arraybackslash}p{#1}}",
        "\\caption[Partition schemes considered]{" + caption + "}",
        "\\label{tab:rejected-partitions}",
        "\\begin{tabular}{@{}R{0.150\\textwidth}R{0.110\\textwidth}c"
        "R{0.235\\textwidth}R{0.310\\textwidth}c@{}}",
        "\\toprule",
        "Scheme & Slices on & Ref. & On this corpus & Why dismissed & Built? \\\\",
        "\\midrule",
    ]
    for i, r in enumerate(ledger):
        if r["status"] == "adopted":
            out.append("\\midrule")
        name = _tex(r["name"])
        if r["status"] == "adopted":
            name = "\\textbf{" + name + "}"
        ref = f"\\citep{{{r['refs']}}}" if r["refs"] else ""
        tick = "\\checkmark" if r["buildable"] == "true" else ""
        outcome = _tex(r["outcome_template"].format(**f))
        why = _tex(r["dismissal"].format(**f))
        out.append(f"{name} & {_tex(r['slices_on'])} & {ref} & {outcome} & {why} & {tick} \\\\")
        if r["status"] == "dismissed" and i + 1 < len(ledger) \
                and ledger[i + 1]["status"] == "dismissed":
            out.append("\\addlinespace")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(out)


def main() -> int:
    ledger = sorted(csv.DictReader(open(LEDGER)), key=lambda r: int(r["order"]))
    f = facts()
    p = pins()
    gate(f, ledger)

    print("== corpus pins ==")
    print(f"  Attack Flow {p['flow_corpus']} (schema {p['schema']}); "
          f"ATT&CK Enterprise v{p['attack']}; {f['n_flows']} flows")
    print("== substituted values (all computed unless marked TYPED) ==")
    for k in sorted(f):
        mark = "  TYPED" if k in TYPED else ""
        print(f"  {k:16s} {f[k]}{mark}")
    print("== column widths ==")
    widths = [0.150, 0.110, 0.235, 0.310]
    print(f"  p-columns sum to {sum(widths):.3f}\\textwidth, plus two c-columns "
          f"and 12 tabcolsep gaps at 4pt = 48pt")
    print(f"== rows: {sum(1 for r in ledger if r['status'] == 'dismissed')} dismissed "
          f"+ {sum(1 for r in ledger if r['status'] == 'adopted')} adopted ==")

    if "--check" in sys.argv:
        print("CHECK PASS (nothing written)")
        return 0
    TEX_OUT.parent.mkdir(parents=True, exist_ok=True)
    TEX_OUT.write_text(build(f, ledger, p))
    print("wrote", TEX_OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
