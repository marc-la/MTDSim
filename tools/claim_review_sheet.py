"""Merge the claim-check verdicts into Marc's review sheets
(docs/workflows/claim_check_protocol.md, sections 5 and 9).

    python tools/claim_review_sheet.py [--run run1]

Reads data/claim_check/verdicts/<run>/ (and verdicts/pilot/ for wave 1): every
<key>[.partN].A.jsonl / .B.jsonl, screen_*.jsonl and mechanical.jsonl. Re-runs the
quote check on every A and B row, so a verdict whose quote is not in its source is
voided, never trusted. Then routes each unit-source pair:

    sheet   any major from either verifier; any minor both raise; any H unit whose
            verdicts are not all SUPPORTED-with-found-quotes; any voided quote;
            any NOT-CHECKABLE
    skim    a minor only one verifier raises (H units included)
    cleared every verdict SUPPORTED, every quote found

and writes data/claim_check/review_sheet.md (sheet + skim + no-text + screen +
mechanical), data/claim_check/review_cleared.md, and data/claim_check/stats.md (the
counts the confidence statement is made from).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claim_quote_check as qc  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CC = ROOT / "data" / "claim_check"
NO_TEXT = {"cai2016", "cohen1988statistical", "efron1994introduction", "marsan1995"}


def load(path: Path) -> list[dict]:
    rows = []
    for ln in path.read_text().splitlines():
        ln = ln.strip()
        if ln:
            try:
                rows.append(json.loads(ln))
            except json.JSONDecodeError:
                rows.append({"_bad": ln[:120]})
    return rows


def quote_status(row: dict, cache: dict) -> str:
    """FOUND / FOUND-LOOSE / MISSING / NO-QUOTE / WEB, by the checker's own rules."""
    quote = (row.get("quote") or "").strip()
    loc = row.get("locator") or ""
    if not quote:
        return "NO-QUOTE"
    if loc.startswith("web:"):
        return "WEB"
    import re
    import subprocess
    code = re.match(r"\s*([0-9a-f]{7,40}):([^\s:]+)", loc)
    frags = [x for x in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", quote) if len(x) > 3]
    if code:
        src = subprocess.run(["git", "-C", str(ROOT), "show", f"{code.group(1)}:{code.group(2)}"],
                             capture_output=True, text=True).stdout
        return "FOUND" if src and all(qc.norm(f) in qc.norm(src) for f in frags) else "MISSING"
    key = row.get("key")
    if key not in cache:
        f = qc.TEXT / f"{key}.txt"
        raw = f.read_text() if f.exists() else ""
        # the page-marked PDF text is the source of record; a markdown or HTML copy
        # appended after it may be a different document (ghosh2009nitrd's is)
        cut = min([i for i in (raw.find("[[file " + key + ".md]]"), raw.find("[[file " + key + ".html]]")) if i > 0] or [len(raw)])
        has_pdf = "[[p. " in raw[:cut]
        cache[key] = (qc.norm(raw), qc.norm(raw, loose=True), qc.norm(raw[:cut]) if has_pdf else None,
                      qc.norm(raw[:cut], loose=True) if has_pdf else None)
    n, loose, npdf, lpdf = cache[key]
    status = "FOUND"
    for frag in frags:
        t = qc.norm_map(frag)[0].strip()
        t2 = re.sub(r"(\w)-(\w)", r"\1\2", t)
        if npdf is not None and not (t in npdf or t2 in npdf) and (t in n or t2 in n):
            if qc.norm(frag, loose=True) in lpdf:
                status = "FOUND-LOOSE" if status == "FOUND" else status  # same words, other extraction
            else:
                status = "COPY-ONLY"  # only in the appended copy, which may be another document
            continue
        if t in n or t2 in n:
            continue
        if qc.norm(frag, loose=True) in loose:
            status = "FOUND-LOOSE"
            continue
        return "MISSING"
    return status


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", default="run1")
    a = ap.parse_args(argv)
    units = {json.loads(l)["id"]: json.loads(l) for l in (CC / "claims.jsonl").read_text().splitlines() if l.strip()}
    vdirs = [CC / "verdicts" / "pilot", CC / "verdicts" / a.run]
    pairs: dict[tuple, dict] = collections.defaultdict(lambda: {"A": [], "B": []})
    cache: dict = {}
    bad = []
    for d in vdirs:
        if not d.exists():
            continue
        for f in sorted(d.glob("*.jsonl")):
            parts = f.name.split(".")
            if len(parts) < 3 or parts[-2] not in ("A", "B"):
                continue
            side = parts[-2]
            for r in load(f):
                if "_bad" in r or "unit" not in r:
                    bad.append((f.name, r.get("_bad", "")))
                    continue
                r["_q"] = quote_status(r, cache)
                r["_file"] = f"{d.name}/{f.name}"
                pairs[(r["unit"], r["key"])][side].append(r)

    sheet, skim, cleared = [], [], []
    for (u, k), v in sorted(pairs.items()):
        tier = units.get(u, {}).get("tier", "?")
        rows = v["A"] + v["B"]
        majors = [r for r in rows if r.get("severity") == "major"]
        voided = [r for r in rows if r["_q"] in ("MISSING", "NO-QUOTE", "COPY-ONLY") and r.get("verdict") != "NOT-CHECKABLE"]
        nc = [r for r in rows if r.get("verdict") == "NOT-CHECKABLE"]
        a_flag = any(r.get("verdict") != "SUPPORTED" for r in v["A"])
        b_flag = any(r.get("verdict") != "SUPPORTED" for r in v["B"])
        all_ok = not a_flag and not b_flag and not voided and rows
        if majors or voided or nc or (a_flag and b_flag and v["A"] and v["B"]) or (tier == "H" and not all_ok and (a_flag and b_flag or not v["B"] or not v["A"])):
            sheet.append((u, k, tier, v))
        elif a_flag or b_flag:
            skim.append((u, k, tier, v))
        else:
            cleared.append((u, k, tier, v))

    def unit_head(u):
        r = units.get(u, {})
        loc = " > ".join(x for x in (r.get("chapter"), r.get("section"), r.get("subsection")) if x)
        return f"`{u}` · {r.get('origin', '?')} · tier {r.get('tier', '?')} · {loc}", r.get("text", "")

    def verdict_line(side, r):
        q = (r.get("quote") or "").replace("\n", " ")
        if len(q) > 400:
            q = q[:400] + " …"
        return (f"- **{side}** {r.get('verdict')} / {r.get('severity')} / {r.get('confidence', '?')} — {r.get('claim', '')}\n"
                f"  - issue: {r.get('issue') or '—'}\n"
                f"  - quote ({r['_q']}, {r.get('locator', '')}): \"{q}\"\n"
                f"  - fix: `{r.get('fix', '')}` {r.get('fix_text') or ''}")

    def block(items, title, intro):
        out = [f"## {title} ({len(items)})", "", intro, ""]
        for i, (u, k, tier, v) in enumerate(items, 1):
            head, text = unit_head(u)
            out += [f"### {title[0]}{i}. {k} — {head}", "", f"> {text}", ""]
            for side in ("A", "B"):
                for r in v[side]:
                    out.append(verdict_line(side, r))
            out += ["", "**Mark:** ok / fix / fix-other / look — ", ""]
        return out

    md = ["# Claim check: Marc's review sheet", "",
          "Generated by `tools/claim_review_sheet.py`; quotes re-checked against the source texts at generation. "
          "Mark each item. `FOUND` = the quote is verbatim in that source; `COPY-ONLY` = found only in an appended markdown copy, not in the PDF of record (re-verify); `NO-QUOTE` = an absence claim or a missing quote; `WEB` = a fetched page, not machine-checked.", ""]
    md += block(sheet, "Sheet", "Majors from either verifier, minors both raise, unverifiable quotes, and high-risk units not cleared by both.")
    md += block(skim, "Skim", "A minor point one verifier raised. Read the issue line; open only if it matters.")

    # no-text sources: Marc's
    nt = [u for u, r in units.items() if set(r.get("keys", [])) & NO_TEXT]
    md += [f"## No saved text: Marc checks against his own copy ({len(nt)})", ""]
    for u in nt:
        head, text = unit_head(u)
        md += [f"- {head} — keys {', '.join(sorted(set(units[u]['keys']) & NO_TEXT))}", f"  > {text}", "  **Mark:** "]
    md.append("")

    # screens
    scr = []
    for d in vdirs:
        for f in sorted(d.glob("screen_*.jsonl")) if d.exists() else []:
            scr += load(f)
    want = [r for r in scr if r.get("answer") in ("needs-source", "mark-ours")]
    counts = collections.Counter(r.get("answer") for r in scr)
    md += [f"## Missing-citation screen: needs-source and mark-ours ({len(want)} of {len(scr)} screened; {dict(counts)})", ""]
    for r in want:
        head, text = unit_head(r.get("unit", ""))
        md += [f"- **{r.get('answer')}** {head} — key {r.get('key') or '—'} ({r.get('confidence', '?')})",
               f"  > {text}", f"  - {r.get('issue') or ''}",
               f"  - quote: \"{(r.get('quote') or '')[:300]}\" {r.get('locator') or ''}",
               f"  - fix: {r.get('fix') or ''} {r.get('fix_text') or ''}", "  **Mark:** "]
    md.append("")

    mech = CC / "verdicts" / a.run / "mechanical.jsonl"
    if mech.exists():
        m = load(mech)
        md += [f"## Mechanical exceptions ({len(m)})", ""]
        for r in m:
            md.append("- " + "; ".join(f"{k}: {v}" for k, v in r.items()) + "  **Mark:** ")
        md.append("")
    (CC / "review_sheet.md").write_text("\n".join(md))

    cl = ["# Cleared: both verifiers SUPPORTED, every quote found", ""]
    for u, k, tier, v in cleared:
        cl.append(f"- `{u}` {k} (tier {tier}): " + " | ".join(f"{s}: {r.get('locator', '')}" for s in "AB" for r in v[s][:1]))
    (CC / "review_cleared.md").write_text("\n".join(cl))

    # stats for the confidence statement
    allrows = [r for v in pairs.values() for s in "AB" for r in v[s]]
    qstat = collections.Counter(r["_q"] for r in allrows)
    vstat = collections.Counter((r.get("verdict"), r.get("severity")) for r in allrows)
    pairs_major = sum(1 for (u, k, t, v) in sheet if any(r.get("severity") == "major" for r in v["A"] + v["B"]))
    st = ["# Claim check statistics", "",
          f"- unit-source pairs verified: {len(pairs)} (of 273 in the inventory)",
          f"- pairs with both verifiers: {sum(1 for v in pairs.values() if v['A'] and v['B'])}",
          f"- sheet {len(sheet)}, skim {len(skim)}, cleared {len(cleared)}",
          f"- pairs carrying a major from either verifier: {pairs_major} ({100 * pairs_major / max(1, len(pairs)):.1f} %)",
          f"- verdict rows: {len(allrows)}; quote status {dict(qstat)}",
          f"- verdict x severity: {dict(vstat)}",
          f"- unparseable rows: {len(bad)} {bad[:5]}"]
    (CC / "stats.md").write_text("\n".join(st))
    print("\n".join(st))


if __name__ == "__main__":
    sys.exit(main())
