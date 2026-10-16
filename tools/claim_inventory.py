"""Inventory every claim unit of the dissertation for the claim-by-claim check
(docs/workflows/claim_check_protocol.md).

    python tools/claim_inventory.py census
        counts by chapter and kind: units, citing units, source uses, numeric units,
        and the provisional risk tier of each (the protocol's decision tree, rules R1-R9)
    python tools/claim_inventory.py write [--out DIR]
        writes DIR/claims.jsonl (one row per unit) and DIR/packets/<key>.md (one per
        cited source: every unit that cites it, and every uncited unit that names its
        author), the inputs the verification agents read. DIR defaults to
        data/claim_check/

A claim unit is one prose sentence, one caption, one table row, one equation, or one
text node of a TikZ figure. Scope is the submitted text minus the original proposal
(Appendix A, an included PDF with its own references) and the bibliography. Comments
are stripped before anything is read, so a comment trail never counts as a claim.

Nothing here judges a claim: the tier is a routing decision (who checks it, and how
hard), made from surface features only. The verdicts are the agents' and Marc's.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THESIS = ROOT / "docs" / "thesis"
TEX = THESIS / "dissertation.tex"
BIB = THESIS / "references.bib"

# Sources the protocol routes to Marc whatever the claim (R2): the supervisor's own
# papers and the MTDSim lineage he supervised. Read from the bib's author field
# (Hong) plus the lineage keys the bib cannot show are his students'.
LINEAGE = {"brown2023", "zhang2023", "ho2024", "tay2024", "tay2024code"}
# Sources with no full text in docs/sources (INDEX.md, 2026-10-16): an agent cannot
# quote them, so every claim on them is Marc's (R3).
NO_TEXT = {"cai2016", "cohen1988statistical", "efron1994introduction", "marsan1995",
           "engenuitynerve", "uberbreach2022"}
# tay2024code is a code release: its claims are checked against the released code,
# not a text (protocol section 5).

# Floats that carry sourced values or scores (Marc named 2.4, 3.2, 4.3 and 5.1 as
# high-risk vectors, 2026-10-16): every cited cell is Marc's (R4), every uncited cell
# is asked whether it is our choice or a missing source.
HIGH_FLOATS = {"tab:defence-mechanisms", "tab:deployment-strategies", "tab:attacker-objectives",
               "tab:lineage-configurations", "tab:mtd-metrics", "tab:attacker-properties",
               "tab:attacker-cross-section", "tab:dwell-catalogue", "tab:metrics", "tab:experiment",
               "tab:fidelity-verdict", "tab:profile-sources", "tab:attack-action-times",
               "tab:value-bases", "tab:mtdshield-configuration"}

CITE = re.compile(r"\\cite[a-z]*\*?((?:\[[^\]]*\])*)\{([^}]*)\}")
NUM = re.compile(r"(?<![A-Za-z_\\{:-])\d[\d\s,.]*(?:\\,)?\s*(?:\\%|%|per cent|s\b|ms\b|min|h\b|days?|weeks?|months?|years?)"
                 r"|\b\d+\.\d+\b|(?<![\w{:-])\d{2,}(?![\w}])|\bp\s*[<=>]|[±]|\\pm")
# Surface cues for claims that carry most of an examiner's risk.
CUE = {
    "absence": r"\b(no (?:prior|existing|published|MTD|study|work|model)|none of|not yet|remains? (?:unmeasured|open|untested)|first to|only (?:one|study|model)|never)\b",
    "generalisation": r"\b(most|widely|commonly|typically|usually|standard|conventional|well[- ]known|in general|the field|the literature)\b",
    "borrowed": r"\b(follow(?:s|ing)?|after|adapted|adopt(?:s|ed)?|as in|defin(?:e|es|ed|ition)|threshold|rule of thumb|recommend(?:s|ed)?|convention)\b",
    "attribution": r"\b(et al\.|report(?:s|ed)?|found|show(?:s|ed|n)?|argue(?:s|d)?|propose(?:s|d)?|identif(?:y|ies|ied)|classif(?:y|ies|ied)|measure(?:s|d)?)\b",
}


def strip_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*", "", ln) for ln in text.split("\n"))


def bib_authors() -> dict[str, str]:
    out = {}
    for entry in re.split(r"\n@", BIB.read_text()):
        m = re.match(r"\s*\w+\{([^,]+),", entry)
        a = re.search(r"\bauthor\s*=\s*\{(.+?)\},?\s*\n\s*\w+\s*=", entry, re.S)
        if m:
            out[m.group(1).strip()] = re.sub(r"\s+", " ", a.group(1)) if a else ""
    return out


def surnames(author_field: str) -> list[str]:
    names = []
    for a in author_field.split(" and "):
        a = a.strip().strip("{}")
        if not a or a.lower() == "others":
            continue
        last = a.split(",")[0] if "," in a else a.split()[-1]
        last = re.sub(r"[{}\\'\"`^~]", "", last).strip()
        if len(last) > 2 and last[0].isupper():
            names.append(last)
    return names


def plain(s: str) -> str:
    """Readable text: cite keys kept as [key], formatting commands dropped."""
    s = CITE.sub(lambda m: "[" + (m.group(1).strip("[]") + " " if m.group(1) else "") + m.group(2) + "]", s)
    s = re.sub(r"\\(?:ref|cref|Cref|eqref|autoref)\{([^}]*)\}", r"<\1>", s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = re.sub(r"\\(?:emph|textit|textbf|textsc|mathrm|text|operatorname\*?|grouplabel|enquote)\{", "{", s)
    s = re.sub(r"\\(?:,|;|:|!| )", " ", s)
    s = re.sub(r"\\(?:addlinespace|midrule|toprule|bottomrule|rowcolor\{[^}]*\}|quad|qquad|noindent|centering|tablestyle|small|footnotesize)", " ", s)
    s = re.sub(r"\\multicolumn\{[^}]*\}\{[^}]*\}", "", s)
    s = s.replace("~", " ").replace("\\&", "&").replace("\\%", "%").replace("&", " | ")
    s = re.sub(r"[{}]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def scoped_body() -> list[tuple[int, str]]:
    raw = TEX.read_text().split("\n")
    start = next(i for i, ln in enumerate(raw) if "\\begin{document}" in ln)
    out = []
    for i in range(start, len(raw)):
        ln = re.sub(r"(?<!\\)%.*", "", raw[i])
        if "\\bibliography{" in ln:
            break
        out.append((i + 1, ln))
    return out


def units() -> list[dict]:
    rows: list[dict] = []
    ctx = {"chapter": None, "section": None, "subsection": None}
    env_stack: list[str] = []
    float_label = None
    buf: list[tuple[str, str]] = []  # (origin, text)

    def flush_prose():
        nonlocal buf
        if not buf:
            return
        marked = " ".join(f"\x00{o}\x00 {t}" for o, t in buf)
        # sentence split: a full stop/?/! closing a word, number, bracket or brace
        parts = re.split(r"(?<=[a-z0-9\)\}\]%])([.?!])\s+(?=[A-Z\\(\x00])", marked)
        sents, cur = [], ""
        for p in parts:
            if p in ".?!":
                cur += p
                sents.append(cur)
                cur = ""
            else:
                cur += p
        if cur.strip():
            sents.append(cur)
        last_origin = buf[0][0]
        for s in sents:
            origins = re.findall(r"\x00([^\x00]+)\x00", s)
            origin = origins[0] if origins else last_origin
            if origins:
                last_origin = origins[-1]
            text = re.sub(r"\x00[^\x00]+\x00", "", s).strip()
            add("prose", origin, text)
        buf = []

    def add(kind, origin, text, label=None):
        if len(plain(text).split()) < 3 and not CITE.search(text):
            return
        rows.append(dict(kind=kind, origin=origin, label=label, **ctx, tex=text.strip()))

    def walk(lines, prefix=""):
        nonlocal float_label
        in_tabular = False
        row_acc, row_origin = "", None
        cap_acc, cap_origin, cap_depth = None, None, 0
        eq_acc, eq_origin = None, None
        for n, ln in lines:
            origin = f"{prefix}{n}"
            for env in re.findall(r"\\begin\{(table\*?|sidewaystable|figure\*?|longtable)\}", ln):
                flush_prose()
                env_stack.append(env)
                float_label = None
            m = re.search(r"\\(chapter|section|subsection)\*?(?:\[[^\]]*\])?\{(.*)\}", ln)
            if m and not env_stack:
                flush_prose()
                lvl, title = m.group(1), plain(m.group(2))
                ctx[lvl] = title
                if lvl == "chapter":
                    ctx["section"] = ctx["subsection"] = None
                elif lvl == "section":
                    ctx["subsection"] = None
                continue
            if "\\appendix" in ln:
                flush_prose()
            if "includepdf" in ln or "\\addcontentsline" in ln:
                continue
            lab = re.search(r"\\label\{((?:tab|fig):[^}]*)\}", ln)
            if lab and env_stack:
                float_label = lab.group(1)
                for r in rows:
                    if r["label"] == "__pending__":
                        r["label"] = float_label
            inp = re.search(r"\\input\{((?:tables|figures)/[^}]+)\}", ln)
            if inp:
                p = THESIS / (inp.group(1) if inp.group(1).endswith(".tex") else inp.group(1) + ".tex")
                if p.exists():
                    flush_prose()
                    walk(list(enumerate(strip_comments(p.read_text()).split("\n"), 1)), f"{inp.group(1)}:")
                continue
            # equations
            if re.search(r"\\begin\{(equation|align)\*?\}", ln):
                flush_prose()
                eq_acc, eq_origin = "", origin
            if eq_acc is not None:
                eq_acc += " " + ln
                if re.search(r"\\end\{(equation|align)\*?\}", ln):
                    lab2 = re.search(r"\\label\{([^}]*)\}", eq_acc)
                    add("equation", eq_origin, eq_acc, lab2.group(1) if lab2 else None)
                    eq_acc = None
                continue
            if cap_acc is not None:
                # a caption runs over lines until its braces close
                cap_depth += ln.count("{") - ln.count("}")
                cap_acc += " " + ln
                if cap_depth <= 0:
                    add("caption", cap_origin, cap_acc, float_label or "__pending__")
                    cap_acc = None
                continue
            if env_stack:
                cap = re.search(r"\\caption(?:\[[^\]]*\])?\{", ln)
                if cap:
                    rest = ln[cap.end():]
                    cap_depth = 1 + rest.count("{") - rest.count("}")
                    if cap_depth <= 0:
                        add("caption", origin, rest, float_label or "__pending__")
                    else:
                        cap_acc, cap_origin = rest, origin
                    continue
                if re.search(r"\\begin\{(tabular\*?|tabularx|longtable)", ln):
                    in_tabular = True
                    continue
                if re.search(r"\\end\{(tabular\*?|tabularx|longtable)", ln):
                    in_tabular = False
                    continue
                if in_tabular or "\\\\" in ln:
                    if row_origin is None:
                        row_origin = origin
                    row_acc += " " + ln
                    if "\\\\" in ln:
                        add("table-row", row_origin, row_acc.replace("\\\\", ""), float_label or "__pending__")
                        row_acc, row_origin = "", None
                for env in re.findall(r"\\end\{(table\*?|sidewaystable|figure\*?|longtable)\}", ln):
                    if env_stack:
                        env_stack.pop()
                continue
            if ln.strip() == "":
                flush_prose()
            elif not re.match(r"\s*\\(begin|end|item\b|vspace|newpage|clearpage|medskip|bigskip|maketitle|tableofcontents|listof|frontmatter|mainmatter|pagenumbering)", ln) or "\\item" in ln:
                buf.append((origin, re.sub(r"\\item\s*", "", ln)))
        flush_prose()

    walk(scoped_body(), "L")
    # TikZ figures drawn from figures/*.tex carry text too: worded labels only (three
    # or more words), and only for figures the dissertation includes. Data labels and
    # tick values are results, checked with the float they draw.
    included = {m for _, ln in scoped_body() for m in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", ln)}
    for f in sorted((THESIS / "figures").glob("*.tex")):
        if f.stem not in included:
            continue
        for n, ln in enumerate(strip_comments(f.read_text()).split("\n"), 1):
            for node in re.findall(r"\\node\[[^\]]*\][^{;]*\{(.+?)\};", ln):
                t = plain(node)
                if len(re.findall(r"[A-Za-z]{2,}", re.sub(r"\\[a-zA-Z]+", "", node))) >= 3:
                    rows.append(dict(kind="figure-text", origin=f"figures/{f.name}:{n}", label=f.stem,
                                     chapter=None, section=None, subsection=None, tex=node))
    for i, r in enumerate(rows, 1):
        r["id"] = f"U{i:04d}"
    return rows


# Comment-trail markers of how a passage was drafted. A unit inherits the markers of the
# comment block directly above its paragraph: provenance evidence, never a verdict.
PROVENANCE = {
    "session-drafted": r"session[- ]drafted|session[- ]generated|ratify on read",
    "from-memory": r"from memory|session knowledge|VERIFY",
    "redrafted": r"REDRAFT ROUND|ROUND \d+",
}


def provenance(rows: list[dict]) -> None:
    raw = TEX.read_text().split("\n")
    for r in rows:
        r["provenance"] = []
        if not r["origin"].startswith("L"):
            continue
        i = int(r["origin"][1:]) - 1
        # walk up to the paragraph's first line, then through the comment block above it
        while i > 0 and raw[i - 1].strip() and not raw[i - 1].lstrip().startswith("%"):
            i -= 1
        block = []
        while i > 0 and raw[i - 1].lstrip().startswith("%"):
            i -= 1
            block.append(raw[i])
        text = "\n".join(block)
        r["provenance"] = [k for k, pat in PROVENANCE.items() if re.search(pat, text, re.I)]


def annotate(rows: list[dict]) -> list[dict]:
    provenance(rows)
    authors = bib_authors()
    hong = {k for k, a in authors.items() if "Hong, Jin" in a}
    supervisor = hong | LINEAGE
    name_to_keys = collections.defaultdict(set)
    for k, a in authors.items():
        for s in surnames(a)[:1]:
            name_to_keys[s].add(k)
    for r in rows:
        tex = r["tex"]
        r["text"] = plain(tex)
        keys, pins = [], []
        for m in CITE.finditer(tex):
            ks = [k.strip() for k in m.group(2).split(",") if k.strip()]
            keys += ks
            if m.group(1):
                pins.append(m.group(1).strip("[]") + " " + ",".join(ks))
        r["keys"] = list(dict.fromkeys(keys))
        r["pinpoints"] = pins
        stripped = re.sub(r"\\(?:ref|label|cref|eqref)\{[^}]*\}|<[^>]*>|\\cite[a-z]*(?:\[[^\]]*\])*\{[^}]*\}", "", tex)
        r["numeric"] = bool(NUM.search(stripped))
        r["cues"] = [c for c, pat in CUE.items() if re.search(pat, r["text"], re.I)]
        r["names_uncited"] = sorted({k for s, ks in name_to_keys.items()
                                     if re.search(rf"\b{re.escape(s)}\b", r["text"]) for k in ks} - set(r["keys"]))
        r["tier"], r["rules"] = tier(r, supervisor)
    return rows


def tier(r: dict, supervisor: set[str]) -> tuple[str, list[str]]:
    """The protocol's decision tree (claim_check_protocol.md, section 4), surface-only.

    H  = Marc reads the sentence beside the agent's quote, whatever the verdict;
    V2 = two independent agents verify; Marc reads it only if either says other than
         supported, or they disagree;
    V1 = one agent asks whether an uncited claim needs a source; Marc reads it only if
         the answer is yes;
    M  = mechanical: checked against our own floats, data, code or cross-references,
         and reported as a bundle.
    """
    rules = []
    keys = set(r["keys"])
    lab = r.get("label") or ""
    if keys:
        if r["kind"] == "equation" or r["pinpoints"] or (r["numeric"] and "borrowed" in r["cues"]):
            rules.append("R1 borrowed number, rule, equation or pinpoint")
        elif r["numeric"]:
            rules.append("R1 cited number")
        if keys & supervisor:
            rules.append("R2 supervisor or lineage source")
        if keys & NO_TEXT:
            rules.append("R3 source has no text to quote")
        if "absence" in r["cues"] or "generalisation" in r["cues"]:
            rules.append("R5 absence or field-wide claim")
        if rules:
            return "H", rules
        if lab in HIGH_FLOATS:
            return "V2", ["R4 cited cell of a sourced float"]
        return "V2", ["R6 cited qualitative claim"]
    if "absence" in r["cues"] or "generalisation" in r["cues"]:
        return "V1", ["R7 uncited absence or field-wide claim"]
    if r["names_uncited"] or "attribution" in r["cues"]:
        return "V1", ["R8 uncited attribution: names a source or reports a finding"]
    if lab in HIGH_FLOATS:
        return "V1", ["R4 uncited cell of a sourced float: our choice, or a missing source?"]
    return "M", ["R9 own method, own result or cross-reference"]


def census(rows):
    by = collections.defaultdict(lambda: collections.Counter())
    uses = collections.Counter()
    for r in rows:
        ch = (r["chapter"] or ("(figure text)" if r["kind"] == "figure-text" else "(front matter)"))[:44]
        c = by[ch]
        c["units"] += 1
        c[r["kind"]] += 1
        c["citing"] += bool(r["keys"])
        c["uses"] += len(r["keys"])
        c["numeric"] += r["numeric"]
        c["tier " + r["tier"]] += 1
        c["drafted"] += "session-drafted" in r["provenance"]
        for k in r["keys"]:
            uses[k] += 1
    cols = ["units", "prose", "caption", "table-row", "equation", "figure-text", "citing", "uses", "numeric", "tier H", "tier V2", "tier V1", "tier M", "drafted"]
    print(f"{'chapter':45s}" + "".join(f"{c:>11s}" for c in cols))
    tot = collections.Counter()
    for ch, c in by.items():
        tot.update(c)
        print(f"{ch:45s}" + "".join(f"{c[k]:11d}" for k in cols))
    print(f"{'TOTAL':45s}" + "".join(f"{tot[k]:11d}" for k in cols))
    print(f"\ndistinct sources cited: {len(uses)}; source uses: {sum(uses.values())}")
    rc = collections.Counter(x.split(' ')[0] for r in rows for x in r["rules"])
    print("rule firings:", dict(sorted(rc.items())))


def write(rows, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "claims.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k != "tex"} | {"tex": r["tex"]}) + "\n")
    pk = out / "packets"
    pk.mkdir(exist_ok=True)
    keys = sorted({k for r in rows for k in r["keys"]})
    index = {r["id"]: i for i, r in enumerate(rows)}
    for k in keys:
        cited = [r for r in rows if k in r["keys"]]
        named = [r for r in rows if k in r["names_uncited"]]
        lines = [f"# Packet: {k}", "",
                 f"{len(cited)} units cite it; {len(named)} more name its first author without citing it.", "",
                 "## Units that cite it", ""]
        for r in cited:
            loc = " > ".join(x for x in (r["chapter"], r["section"], r["subsection"]) if x)
            i = index[r["id"]]
            # two units either side: a threshold or source is often named a sentence or two away
            def near(js):
                return " ".join(f"[{rows[j]['id']}{' cites ' + ','.join(rows[j]['keys']) if rows[j]['keys'] else ''}] {rows[j]['text']}"
                                for j in js if 0 <= j < len(rows) and rows[j]["kind"] == r["kind"]
                                and rows[j]["chapter"] == r["chapter"])
            before, after = near(range(i - 2, i)), near(range(i + 1, i + 3))
            lines += [f"### {r['id']} ({r['kind']}, {r['origin']}{', ' + r['label'] if r.get('label') else ''}) tier {r['tier']}",
                      f"*{loc}*" + (f" · drafting trail: {', '.join(r['provenance'])}" if r.get("provenance") else ""), "",
                      "> " + r["text"], ""]
            if before or after:
                lines += [f"Context before: {before}", "", f"Context after: {after}", ""]
        if named:
            lines += ["## Units that name the author without citing", ""]
            for r in named:
                lines += [f"### {r['id']} ({r['kind']}, {r['origin']}) cites {', '.join(r['keys']) or 'nothing'}", "", "> " + r["text"], ""]
        (pk / f"{k}.md").write_text("\n".join(lines))
    print(f"wrote {len(rows)} units and {len(keys)} packets to {out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("census")
    w = sub.add_parser("write")
    w.add_argument("--out", type=Path, default=ROOT / "data" / "claim_check")
    a = ap.parse_args(argv)
    rows = annotate(units())
    if a.cmd == "census":
        census(rows)
    else:
        write(rows, a.out)


if __name__ == "__main__":
    sys.exit(main())
