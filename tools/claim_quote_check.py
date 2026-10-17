"""Check that every quote a verification agent returns is really in its source: the
deterministic guard against a fabricated or paraphrased "quote" in the claim-by-claim
check (docs/workflows/claim_check_protocol.md, section 5).

    python tools/claim_quote_check.py texts
        builds docs/sources/_text/<key>.txt from each source's PDF (page-marked as
        [[p. N]], N the PDF's page index from 1) or, failing that, its markdown or
        saved HTML. docs/sources/ is gitignored, so the copyrighted text never enters git
    python tools/claim_quote_check.py check VERDICTS.jsonl [...]
        for each verdict row {"unit", "key", "quote", "locator"}, reports FOUND (with the
        page it sits on), FOUND-LOOSE (found once hyphenation, case and punctuation are
        ignored) or MISSING. Exits non-zero if any quote is MISSING

A MISSING quote is never a finding about the dissertation: it means the agent's
evidence cannot be trusted and the unit is re-verified. Matching is on the source's
own words, so a quote an agent "tidied" fails, by design. A locator of the form
``<commit>:<path>[:line]`` is checked against that file at that commit instead (the
code release, tay2024code).
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "docs" / "sources"
TEXT = SOURCES / "_text"

LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl", "’": "'", "‘": "'",
             "“": '"', "”": '"', "–": "-", "—": "-", "−": "-", "­": "", " ": " "}


def norm(s: str, loose: bool = False) -> str:
    s = unicodedata.normalize("NFKC", s)
    for a, b in LIGATURES.items():
        s = s.replace(a, b)
    s = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", s)  # line-break hyphenation
    s = re.sub(r"\s+", " ", s)
    if loose:
        s = re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", ""))
        s = re.sub(r"\s+", " ", s)
    return s.strip()


def norm_map(raw: str) -> tuple[str, list[int]]:
    """The strict normalisation of ``norm``, with each output character's index in
    ``raw``, so a match in normalised text maps back to its page marker."""
    out, idx = [], []
    i, n = 0, len(raw)
    while i < n:
        ch = raw[i]
        m = re.match(r"-\s*\n\s*", raw[i:]) if ch == "-" and i > 0 and raw[i - 1].isalnum() else None
        if m and i + m.end() < n and raw[i + m.end()].isalnum():
            i += m.end()  # line-break hyphenation joins the word
            continue
        rep = LIGATURES.get(ch, unicodedata.normalize("NFKC", ch))
        if ch.isspace() or rep.isspace():
            if out and out[-1] != " ":
                out.append(" ")
                idx.append(i)
        else:
            for c in rep:
                out.append(c)
                idx.append(i)
        i += 1
    return "".join(out), idx


def build_texts() -> None:
    import pypdf  # imported here: only this subcommand needs it

    TEXT.mkdir(exist_ok=True)
    keys = sorted({re.sub(r"\.(preprint\.)?(pdf|md|html)$", "", f.name) for f in SOURCES.iterdir()
                   if f.suffix in (".pdf", ".md", ".html") and f.name != "INDEX.md"})
    for k in keys:
        out = []
        for pdf in (SOURCES / f"{k}.pdf", SOURCES / f"{k}.preprint.pdf"):
            if pdf.exists():
                r = pypdf.PdfReader(str(pdf))
                out.append(f"[[file {pdf.name}]]")
                for i, page in enumerate(r.pages, 1):
                    out.append(f"[[p. {i}]]\n{page.extract_text() or ''}")
        for other in (SOURCES / f"{k}.md", SOURCES / f"{k}.html"):
            if other.exists():
                t = other.read_text(errors="replace")
                if other.suffix == ".html":
                    t = html.unescape(re.sub(r"<(script|style)[^>]*>.*?</\1>|<[^>]+>", " ", t, flags=re.S))
                out.append(f"[[file {other.name}]]\n{t}")
        # control characters from OCR make grep treat the file as binary; drop them
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", "\n".join(out))
        (TEXT / f"{k}.txt").write_text(text)
        print(f"{k}: {sum(len(x) for x in out)} chars")


def page_of(text: str, pos: int) -> str:
    marks = list(re.finditer(r"\[\[(p\. \d+|file [^\]]+)\]\]", text[:pos]))
    files = [m.group(1) for m in marks if m.group(1).startswith("file")]
    pages = [m.group(1) for m in marks if m.group(1).startswith("p.")]
    f = files[-1][5:] if files else "?"
    return f"{f} {pages[-1]}" if pages and f.endswith(".pdf") else f


def check(paths: list[Path]) -> int:
    missing = 0
    cache: dict[str, tuple[str, str, str]] = {}
    for p in paths:
        for ln in p.read_text().splitlines():
            if not ln.strip():
                continue
            row = json.loads(ln)
            key, quote = row.get("key"), (row.get("quote") or "").strip()
            if not quote:
                print(f"{row.get('unit')}\t{key}\tNO-QUOTE\t{row.get('verdict', '')}")
                continue
            code = re.match(r"\s*([0-9a-f]{7,40}):([^\s:]+)", row.get("locator") or "")
            if code:
                # a code release (tay2024code): the quote must be in that file at that commit
                import subprocess
                src = subprocess.run(["git", "-C", str(ROOT), "show", f"{code.group(1)}:{code.group(2)}"],
                                     capture_output=True, text=True).stdout
                ok = all(norm(fr) in norm(src) for fr in re.split(r"\s*(?:\.\.\.|…)\s*", quote) if len(fr) > 3)
                status = "FOUND" if ok and src else "MISSING"
                missing += status == "MISSING"
                print(f"{row.get('unit')}\t{key}\t{status}\t{code.group(1)}:{code.group(2)}\tagent said: {row.get('locator', '')}")
                continue
            if key not in cache:
                f = TEXT / f"{key}.txt"
                raw = f.read_text() if f.exists() else ""
                n, idx = norm_map(raw)
                cache[key] = (raw, n, idx, norm(raw, loose=True))
            raw, n, idx, loose = cache[key]
            # an ellipsis in a quote joins two passages: every fragment must be found
            frags = [x for x in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", quote) if len(x) > 3]
            status, where = "FOUND", []
            for frag in frags:
                target = norm_map(frag)[0].strip()
                hits = [m.start() for m in re.finditer(re.escape(target), n)] if target else []
                if not hits and "-" in target:
                    # a real hyphen broken across a line ("Three-\nlayer") is joined by norm
                    t2 = re.sub(r"(\w)-(\w)", r"\1\2", target)
                    hits = [m.start() for m in re.finditer(re.escape(t2), n)]
                if hits:
                    # every place the passage occurs (a published copy and a preprint both count)
                    where.append(" | ".join(dict.fromkeys(page_of(raw, idx[h]) for h in hits)))
                    continue
                if norm(frag, loose=True) in loose:
                    status = "FOUND-LOOSE" if status == "FOUND" else status
                    where.append("?")
                    continue
                status = "MISSING"
            if status == "MISSING":
                missing += 1
            print(f"{row.get('unit')}\t{key}\t{status}\t{'; '.join(where)}\tagent said: {row.get('locator', '')}")
    return 1 if missing else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("texts")
    c = sub.add_parser("check")
    c.add_argument("verdicts", nargs="+", type=Path)
    a = ap.parse_args(argv)
    if a.cmd == "texts":
        build_texts()
        return 0
    return check(a.verdicts)


if __name__ == "__main__":
    sys.exit(main())
