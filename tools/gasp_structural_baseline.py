"""Pin the ONE structural baseline the L2 chapter cites, and reproduce it.

Why: the §4.2.2 draft's number trail mixed two structural readings of the 38
Attack Flow flows — the REACH read ("13 reach exfiltration / 13 reach impact /
3 both") and the TERMINAL read ("15 of 38 land in a different category than
the terminal tactic alone gives") — and the "15" depends on a concordance
rule that was never written down beside the number. This tool defines the
terminal-tactic-only classifier once, recomputes it from the per-flow YAMLs,
checks that it reproduces the audit CSV's descriptive structural columns, and
prints every number set the chapter could cite, each with its definition.

Definitions (fixed here; the record is
docs/implementation/pipeline/gasp/structural_baseline.md):

  Def A  (terminal, technique-level — the pinned baseline)
      Contract the flow to its technique graph exactly as L1 does
      (mtdsim.l1_construction.aggregate.contract_flow: technique action ->
      through operator/condition glue -> next technique action; a technique-
      less action BREAKS the chain). A technique is TERMINAL when it has no
      contracted out-edge to a different technique. Terminal tactics are the
      tactics of the actions carrying those techniques. Tactic-only actions
      are invisible to L1 aggregation and therefore to this read.
      A flow whose terminals include an `exfiltration`-tactic action reads
      "exfil"; an `impact`-tactic action reads "impact"; both -> "both";
      neither -> "neither".  This is P1 of partition_decision.md and is what
      the audit CSV's `terminal_techniques` / `terminal_tactics` columns hold.

  Reach  (any-occurrence, technique-level — the L1 construction note's read)
      A flow reads "exfil" if ANY technique-bearing action has tactic
      `exfiltration`, "impact" likewise; both / neither as above.  This is
      what the CSV's `reaches_exfiltration` / `reaches_impact` columns hold.

  Concordance rules against the audit's stated_objective
      exact       the 4-way structural read equals the audit class
                  (steal_data<->exfil, impediment<->impact,
                   double_extortion<->both, position_for_future<->neither)
      any-overlap the structural read shares at least one objective tactic
                  with the audit class, or both are empty (the rule
                  partition_decision.md used for its 23/38 = 61 % figure)

Run from the repo root:  PYTHONPATH=src python tools/gasp_structural_baseline.py [--check]
Inputs: data/gap/flows/<flow_id>.yaml (38 active flows), data/gasp/metadata_audit.csv.
--check exits non-zero if the recomputation does not reproduce the CSV columns
or the pinned numbers (used by tests/l2_subgraph/test_structural_baseline.py).
--tex writes docs/thesis/tables/tab_B-2a_objective_classification_audit.tex — the
appendix table section 4.2 points at: the sources that answered each attack flow,
grouped by attack profile; regenerate whenever the CSV changes.
--write-descriptive rewrites the CSV's four descriptive structural columns
(terminal_techniques, terminal_tactics, reaches_exfiltration, reaches_impact)
from this tool, leaving every other column byte-identical. Run once (2026-08-17)
to replace the uncommitted in-session script that first populated them; the
stated_objective / confidence / source columns are never touched by this tool.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT_SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT_SRC))
from mtdsim.l1_construction.aggregate import contract_flow  # noqa: E402
from mtdsim.l1_construction.schema import PerFlowExtract  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FLOWS = ROOT / "data" / "gap" / "flows"
AUDIT = ROOT / "data" / "gasp" / "metadata_audit.csv"

OBJECTIVE_TACTICS = ("exfiltration", "impact")
AUDIT_TO_TACTICS = {
    "steal_data": frozenset({"exfiltration"}),
    "impediment": frozenset({"impact"}),
    "double_extortion": frozenset({"exfiltration", "impact"}),
    "position_for_future": frozenset(),
}

# Pinned numbers (38-flow corpus, post-2026-05-28 verification round).
PINNED = {
    "terminal_split": {"exfil": 7, "impact": 11, "both": 1, "neither": 19},
    "terminal_exact_disagree": 19,
    "terminal_anyoverlap_disagree": 15,
    "reach_split": {"exfil": 10, "impact": 10, "both": 3, "neither": 15},
    "reach_exact_disagree": 14,
    "reach_anyoverlap_disagree": 11,
}


def load_flow(flow_id: str) -> dict:
    with open(FLOWS / f"{flow_id}.yaml") as fh:
        return yaml.safe_load(fh)


def contracted_terminals(flow: dict, *, technique_level: bool = True) -> tuple[list[str], list[str]]:
    """Def A over the flow's technique-projected graph (the L1 contraction).

    Terminal technique = a technique carried by some action of the flow that has
    no outgoing contracted edge to a *different* technique. The contraction is
    :func:`mtdsim.l1_construction.aggregate.contract_flow` itself, so this read is
    by construction the GAP's own view of the flow. Terminal tactics = the union
    of tactics over every action carrying a terminal technique.

    ``technique_level=False`` is the sensitivity variant: technique-less
    (tactic-only) actions are given a synthetic id so they take part in the walk;
    the L1 contraction never does this (they break the chain, aggregate.py §a).
    """
    if technique_level:
        extract = PerFlowExtract.from_dict(flow)
    else:
        f2 = json.loads(json.dumps(flow))
        for n in f2["nodes"]:
            if n["kind"] == "action" and not n.get("technique_id"):
                n["technique_id"] = f"TACTIC:{n.get('tactic')}:{n['id']}"
        extract = PerFlowExtract.from_dict(f2)
    techs = {n.technique_id for n in extract.nodes if n.kind == "action" and n.technique_id}
    has_out = {e.source_id for e in contract_flow(extract) if e.source_id != e.target_id}
    term_techs = sorted(techs - has_out)
    term_tacs = sorted({n.tactic for n in extract.nodes
                        if n.kind == "action" and n.technique_id in term_techs and n.tactic})
    return [t for t in term_techs if not t.startswith("TACTIC:")], term_tacs


def objective_read(tactics: set[str]) -> str:
    e, i = "exfiltration" in tactics, "impact" in tactics
    return "both" if e and i else "exfil" if e else "impact" if i else "neither"


def read_terminal(flow: dict, *, technique_level: bool = True) -> tuple[str, list[str], list[str]]:
    techs, tacs = contracted_terminals(flow, technique_level=technique_level)
    return objective_read(set(tacs)), techs, tacs


def read_reach(flow: dict, *, technique_level: bool = True) -> str:
    tacs = {
        n.get("tactic")
        for n in flow["nodes"]
        if n["kind"] == "action" and (bool(n.get("technique_id")) or not technique_level)
    }
    return objective_read(tacs)


READ_TO_TACTICS = {
    "exfil": frozenset({"exfiltration"}),
    "impact": frozenset({"impact"}),
    "both": frozenset({"exfiltration", "impact"}),
    "neither": frozenset(),
}


def concordance(read: str, audit_class: str) -> tuple[bool, bool]:
    s, a = READ_TO_TACTICS[read], AUDIT_TO_TACTICS[audit_class]
    exact = s == a
    anyoverlap = bool(s & a) or (not s and not a)
    return exact, anyoverlap


def write_descriptive() -> None:
    with open(AUDIT, newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames
        rows = list(reader)
    for r in rows:
        flow = load_flow(r["flow_id"])
        _, techs, tacs = read_terminal(flow)
        r["terminal_techniques"] = ";".join(techs)
        r["terminal_tactics"] = ";".join(tacs)
        reach = read_reach(flow)
        r["reaches_exfiltration"] = "true" if reach in ("exfil", "both") else "false"
        r["reaches_impact"] = "true" if reach in ("impact", "both") else "false"
    with open(AUDIT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


TEX_OUT = ROOT / "docs" / "thesis" / "tables" / "tab_B-2a_objective_classification_audit.tex"
FLOWS_DIR = ROOT / "data" / "gap" / "flows"
# The audit's class labels, in Table 4.1's order, to the attack profile key the
# thesis prints as c1 to c4 (pipeline_ladder_figure.PROFILE_ORDER).
CLASS_ORDER = [
    ("steal_data", "objective_exfiltration"),
    ("impediment", "objective_impact"),
    ("double_extortion", "objective_exfiltration_impact"),
    ("position_for_future", "objective_none_c2"),
]


def _tex(s: str) -> str:
    return (s.replace("\\", "\\textbackslash{}").replace("&", "\\&").replace("%", "\\%")
             .replace("$", "\\$").replace("#", "\\#").replace("_", "\\_"))


def _host(url: str) -> str:
    from urllib.parse import urlparse
    return urlparse(url).netloc.replace("www.", "")


# The corpus's vendor and government reports, keyed by the URL the analyst
# cited, mapped to their entry in docs/thesis/references.bib. These are real
# bibliography entries with titles, authors and dates (verified 2026-08-20 by
# fetch, except the three the bib marks VERIFY) --- a classification cites its
# source the way any other claim in the thesis does, not as a bare link.
# A new vendor URL entering the corpus fails loudly below rather than being
# silently dropped: add the bib entry, then add the key here.
CITE_KEY = {
    "https://unit42.paloaltonetworks.com/threat-assessment-black-basta-ransomware/": "unit42basta2022",
    "https://www.cisa.gov/uscert/ncas/alerts/aa22-138b": "cisaaa22138b",
    "https://www.cybereason.com/blog/operation-cobalt-kitty-apt": "cybereasoncobaltkitty",
    "https://thedfirreport.com/2022/09/26/bumblebee-round-two/": "dfirbumblebee2022",
    "https://www.csoonline.com/article/3444488/equifax-data-breach-faq-what-happened-who-was-affected-what-was-the-impact.html": "csoequifax2020",
    "https://thedfirreport.com/2022/05/09/seo-poisoning-a-gootloader-story/": "dfirgootloader2022",
    "https://thedfirreport.com/2021/11/01/from-zero-to-domain-admin/": "dfirdomainadmin2021",
    "https://www.volexity.com/blog/2024/01/10/active-exploitation-of-two-zero-day-vulnerabilities-in-ivanti-connect-secure-vpn/": "volexityivanti2024",
    "https://unit42.paloaltonetworks.com/mac-malware-steals-cryptocurrency-exchanges-cookies/": "unit42maccookies2019",
    "https://medium.com/mitre-engenuity/technical-deep-dive-understanding-the-anatomy-of-a-cyber-intrusion-080bddc679f3": "engenuitynerve",
    "https://blog.talosintelligence.com/iranian-apt-muddywater-targets-turkey/": "talosmuddywater2022",
    "https://www.malwarebytes.com/blog/news/2018/10/mac-malware-intercepts-encrypted-web-traffic-for-ad-injection": "malwarebytesadware2018",
    "https://www.mcafee.com/blogs/other-blogs/mcafee-labs/shamoon-returns-to-wipe-systems-in-middle-east-europe/": "mcafeeshamoon",
    "https://unit42.paloaltonetworks.com/microsoft-sharepoint-cve-2025-49704-cve-2025-49706-cve-2025-53770/": "unit42sharepoint2025",
    "https://www.uber.com/newsroom/security-update/": "uberbreach2022",
}


def vendor_citations(rows: list[dict]) -> dict[str, str]:
    """flow_id -> the \\citep the audit's vendor source resolves to.

    Sources live in the tracked corpus, one bundle per flow: the per-flow YAML's
    ``references[]`` is the analyst's own citation list, carried through from
    ``data/gap/_corpus_stix/*.json``. The audit CSV's ``source_used`` records
    which of them decided the class. This joins the two on the URL host, then
    resolves the URL to a bibliography key, so what prints beside a
    classification is a citation to the report that was actually read.
    """
    per_flow: dict[str, list[str]] = {}
    for r in sorted(rows, key=lambda x: x["flow_id"]):
        refs = [x for x in (load_flow(r["flow_id"]).get("references") or []) if x.get("url")]
        for tok in r["source_used"].split("+"):
            tok = tok.strip()
            if not tok.startswith("vendor:"):
                continue
            want = tok.split(":", 1)[1].split("(")[0].strip().replace("www.", "")
            match = next((x for x in refs if want.split(".")[0] in _host(x["url"])), None)
            if match is None:
                raise SystemExit(f"unjoinable vendor source {want!r} on {r['flow_id']}")
            key = CITE_KEY.get(match["url"])
            if key is None:
                raise SystemExit(
                    f"no bibliography entry for {match['url']}\n"
                    f"  (cited by {r['flow_id']}). Add the @misc to "
                    f"docs/thesis/references.bib, then its key to CITE_KEY.")
            per_flow.setdefault(r["flow_id"], []).append(key)
    return {k: "\\citep{" + ",".join(dict.fromkeys(v)) + "}" for k, v in per_flow.items()}


def _sources_cell(row: dict, vendor_ids: str | None) -> str:
    """What was read to decide this flow's class, as printable citations."""
    parts: list[str] = []
    for tok in row["source_used"].split("+"):
        tok = tok.strip()
        if tok == "ctid_blurb":
            parts.append("CTID blurb")
        elif tok == "ctid_flow_narrative":
            parts.append("flow narrative")
        elif tok == "in_flow_only":
            parts.append("flow structure")
        elif tok.startswith("attack_group:"):
            parts.append("ATT\\&CK " + _tex(tok.split(":", 1)[1]))
        elif tok.startswith("vendor:"):
            continue  # rendered from the ledger, below
        elif tok.startswith("marc_ruling"):
            parts.append("author adjudication")
        else:
            parts.append(_tex(tok))
    if vendor_ids:
        parts.append(vendor_ids)
    return "; ".join(parts)


def write_tex() -> None:
    """Appendix B: the sources that answered section 4.2's two questions.

    Round 2026-10-04 (Marc: the appendix was drafted before the terms were
    standardised; "is it relevant ... are we answering that question"). Section
    4.2 cites this table for one thing: which sources answered each attack
    flow, and which three the sources left open. So it prints one row per
    attack flow, grouped by attack profile, and one column per source beyond
    the CTID description (read for all 38). Cut from the 2026-08-20 tables: the
    terminal read, terminal tactics and override columns (they argued the
    19-of-38 override count section 4.2 no longer makes), the confidence column
    (all 38 high, so it said nothing), and four repeated captions. The audit's
    "in_flow_only" (six flows) is not printed: the CTID description decided
    those six and the drawn attack flow agreed, and section 4.2 says the answers
    were not read off the attack flow.
    """
    def code(key: str) -> str:  # the c_k Table 4.1 prints, in CLASS_ORDER's order
        return f"$c_{{{[k for _, k in CLASS_ORDER].index(key) + 1}}}$"
    rows = list(csv.DictReader(open(AUDIT)))
    vendor_by_flow = vendor_citations(rows)
    by_class: dict[str, list[dict]] = {k: [] for k, _ in CLASS_ORDER}
    for r in rows:
        if "ctid_blurb" not in r["source_used"]:
            raise SystemExit(f"{r['flow_id']}: no CTID description read; the caption says every one was")
        toks = [t.strip() for t in r["source_used"].split("+")]
        r["_notes"] = "\\propmet" if "ctid_flow_narrative" in toks else ""
        r["_group"] = next((_tex(t.split(":", 1)[1]) for t in toks if t.startswith("attack_group:")), "")
        r["_report"] = vendor_by_flow.get(r["flow_id"], "")
        r["_ours"] = "\\propmet" if any(t.startswith("marc_ruling") for t in toks) else ""
        by_class[r["stated_objective"]].append(r)
    n_ours = sum(1 for r in rows if r["_ours"])

    out = [
        "% GENERATED by tools/gasp_structural_baseline.py --tex from",
        "%   data/gasp/metadata_audit.csv (classification and sources read) and",
        "%   data/gap/flows/*.yaml (the analyst's own citation list, carried through from",
        "%   the tracked corpus bundles in data/gap/_corpus_stix/).",
        "% Do not hand-edit; regenerate. DRAFT STATE (2026-10-04 appendix pass): caption",
        "%   session-drafted, ratify on read.",
        f"% At generation: {len(rows)} attack flows, {n_ours} decided by the author.",
        "",
        "\\begin{table}[htbp]",
        "\\centering",
        "\\caption[The sources that answered each attack flow]{The sources that answered "
        "the two questions of Section~\\ref{sec:attack-profiles} for each attack flow, "
        "grouped by attack profile (Table~\\ref{tab:attack-profiles}). The CTID description "
        "of every attack flow was read \\citep{ctid2025attackflow}; the columns give what else "
        "was. \\emph{Step notes} are the analyst's notes on the steps of the attack flow. "
        "\\emph{ATT\\&CK group} is the group page read \\citep{mitre2026attackv19}. "
        "\\emph{Decided by us} marks the attack flows these sources left open.}",
        "\\label{tab:profile-sources}",
        "\\tablestyle",
        "\\begin{tabular}{@{}P{0.38\\textwidth}ccP{0.17\\textwidth}c@{}}",
        "\\toprule",
        "Attack flow & \\shortstack{Step\\\\notes} & \\shortstack{ATT\\&CK\\\\group} & Threat report & "
        "\\shortstack{Decided\\\\by us} \\\\",
        "\\midrule",
    ]
    for k, (csv_label, key) in enumerate(CLASS_ORDER):
        rs = by_class[csv_label]
        if k:
            out.append("\\midrule")
        out.append(f"\\grouprow{{5}}{{{code(key)} ({len(rs)} attack flows)}} \\\\")
        for r in sorted(rs, key=lambda x: x["flow_name"].lower()):
            out.append(f"{_tex(r['flow_name'])} & {r['_notes']} & {r['_group']} & "
                       f"{r['_report']} & {r['_ours']} \\\\")
    out += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]

    TEX_OUT.parent.mkdir(parents=True, exist_ok=True)
    TEX_OUT.write_text("\n".join(out))
    print(f"wrote {TEX_OUT}")
    print(f"  {len(rows)} attack flows; " + ", ".join(
        f"{code(key)} {len(by_class[c])}" for c, key in CLASS_ORDER) + f"; {n_ours} decided by the author")
    print(f"  cited reports: {len(set(vendor_by_flow.values()))} distinct citations "
          f"over {len(vendor_by_flow)} attack flows")


def main(check: bool = False) -> int:
    rows = list(csv.DictReader(open(AUDIT)))
    assert len(rows) == 38, len(rows)
    ok = True
    results = []
    for r in rows:
        flow = load_flow(r["flow_id"])
        t_read, t_techs, t_tacs = read_terminal(flow)
        r_read = read_reach(flow)
        # reproduce the CSV's descriptive columns
        csv_techs = sorted(x for x in r["terminal_techniques"].split(";") if x)
        csv_tacs = sorted(x for x in r["terminal_tactics"].split(";") if x)
        csv_reach = objective_read(
            ({"exfiltration"} if r["reaches_exfiltration"] == "true" else set())
            | ({"impact"} if r["reaches_impact"] == "true" else set())
        )
        repro = (t_techs == csv_techs) and (t_tacs == csv_tacs) and (r_read == csv_reach)
        if not repro:
            ok = False
            print(f"MISMATCH {r['flow_id']}: recomputed terminals {t_techs}/{t_tacs} reach {r_read} "
                  f"vs CSV {csv_techs}/{csv_tacs} reach {csv_reach}")
        t_read_all, _, t_tacs_all = read_terminal(flow, technique_level=False)
        r_read_all = read_reach(flow, technique_level=False)
        results.append(dict(flow_id=r["flow_id"], audit=r["stated_objective"], conf=r["metadata_confidence"],
                            t_read=t_read, t_tacs=t_tacs, r_read=r_read,
                            t_read_all=t_read_all, t_tacs_all=t_tacs_all, r_read_all=r_read_all))

    def split(key):
        c = Counter(x[key] for x in results)
        return {k: c.get(k, 0) for k in ("exfil", "impact", "both", "neither")}

    def disagree(key, rule):
        idx = 0 if rule == "exact" else 1
        return [x for x in results if not concordance(x[key], x["audit"])[idx]]

    out = {
        "terminal_split": split("t_read"),
        "terminal_exact_disagree": len(disagree("t_read", "exact")),
        "terminal_anyoverlap_disagree": len(disagree("t_read", "anyoverlap")),
        "reach_split": split("r_read"),
        "reach_exact_disagree": len(disagree("r_read", "exact")),
        "reach_anyoverlap_disagree": len(disagree("r_read", "anyoverlap")),
    }
    print("== Def A terminal read (technique-level; the pinned baseline) ==")
    print("  4-way split:", out["terminal_split"],
          "| any-count: exfil", out["terminal_split"]["exfil"] + out["terminal_split"]["both"],
          "impact", out["terminal_split"]["impact"] + out["terminal_split"]["both"],
          "both", out["terminal_split"]["both"])
    print("  disagreements with audit: exact", out["terminal_exact_disagree"],
          "/ any-overlap", out["terminal_anyoverlap_disagree"], "of 38")
    print("== Reach read (technique-level) ==")
    print("  4-way split:", out["reach_split"],
          "| any-count: exfil", out["reach_split"]["exfil"] + out["reach_split"]["both"],
          "impact", out["reach_split"]["impact"] + out["reach_split"]["both"],
          "both", out["reach_split"]["both"])
    print("  disagreements with audit: exact", out["reach_exact_disagree"],
          "/ any-overlap", out["reach_anyoverlap_disagree"], "of 38")
    print("== Sensitivity: including tactic-only (technique-less) actions ==")
    print("  terminal split:", split("t_read_all"), "| reach split:", split("r_read_all"))
    print("  flows whose terminal read changes:",
          [(x["flow_id"], x["t_read"], "->", x["t_read_all"]) for x in results if x["t_read"] != x["t_read_all"]])
    print("  flows whose reach read changes:",
          [(x["flow_id"], x["r_read"], "->", x["r_read_all"]) for x in results if x["r_read"] != x["r_read_all"]])
    print("== Per-flow (terminal read | audit | exact? | any-overlap?) ==")
    for x in results:
        ex, ov = concordance(x["t_read"], x["audit"])
        print(f"  {x['flow_id']:42s} {x['t_read']:8s} {x['audit']:20s} {'=' if ex else '.'} {'~' if ov else 'X'}")
    print("== The 4 flows that any-overlap counts as agreeing but exact does not (terminal read) ==")
    for x in results:
        ex, ov = concordance(x["t_read"], x["audit"])
        if ov and not ex:
            print(f"  {x['flow_id']}: terminal {x['t_read']} vs audit {x['audit']}")

    if out != PINNED:
        ok = False
        print("PINNED NUMBERS DO NOT REPRODUCE:", out, "vs", PINNED)
    if check:
        print("CHECK", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    if "--write-descriptive" in sys.argv:
        write_descriptive()
    if "--tex" in sys.argv:
        write_tex()
        sys.exit(0)
    sys.exit(main(check="--check" in sys.argv))
