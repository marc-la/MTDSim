"""Screen the dissertation's surface for terms that cost the reader — the mechanical
half of the voice pass's reader-overhead sweep (register E2, 2026-09-22: no invented
terms, every name on a needs basis).

    python tools/term_screen.py census "movement attacker" "controller layer"
        per-term counts split into body / headings / captions / float files / comments,
        with line numbers — the validation gate of a terminology sweep
    python tools/term_screen.py acronyms [--chapter N]
        every ALL-CAPS token in the prose: first use, and whether an expansion
        "... (ACRO)" precedes or accompanies it — unexpanded acronyms first
    python tools/term_screen.py phrases --chapter N [--min 3] [--max-words 3]
        multi-word phrases that first appear in chapter N and recur there at least
        --min times: the candidates for "a name this chapter introduced" — each is
        then either a field term, a term defined at first use, or a term to remove
    python tools/term_screen.py variants [--chapter N]
        one concept spelt two ways — hyphen, case and plural variants of the same
        two-word phrase, with each spelling's count (voice.md §e: no synonym rotation)

Nothing here knows the thesis's vocabulary: terms arrive as arguments and every
other report is derived from the text (mechanism, not exception). Reads
``docs/thesis/dissertation.tex`` and the generated floats under ``tables/`` and
``figures/``; comments are stripped before anything is counted, so a comment
trail never counts against the prose. A living tool — extend it here rather than
re-deriving a census in an ad-hoc grep.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEX = REPO / "docs" / "thesis" / "dissertation.tex"
FLOAT_DIRS = (REPO / "docs" / "thesis" / "tables", REPO / "docs" / "thesis" / "figures")

HEADING_RE = re.compile(r"\\(chapter|section|subsection|subsubsection|paragraph)\*?\s*[\[{]")
CHAPTER_RE = re.compile(r"^\\chapter\*?\s*(?:\[[^\]]*\])?\{(.*)\}")
COMMENT_RE = re.compile(r"(?<!\\)%.*$")
CMD_STRIP_RE = re.compile(
    r"\\(cite[pt]?|ref|label|eqref|includegraphics|input|texttt|url|autoref|nameref)\*?(\[[^\]]*\])?\{[^}]*\}"
)
MATH_RE = re.compile(r"\$[^$]*\$")
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z\-']*")
ACRO_RE = re.compile(r"(?<![A-Za-z\\])([A-Z][A-Z&]{1,6}\d?)(?![A-Za-z])")

STOP = set(
    """a an the and or but of in on at to for from by with as is are was were be been being
    this that these those it its we our their his her they them there here then than which who
    whose what when where how not no nor so if into onto over under between against through
    per each every any all some such same other another one two three four five six seven
    eight nine ten first second third both either neither only also very more most less least
    can may might will would should could must do does did done has have had having
    because while whether about above below before after during since until within without
    up down out off again further once own via using used use""".split()
)


# ----------------------------------------------------------------------------- text --
def strip_comments(lines: list[str]) -> list[str]:
    """Full-line and trailing comments blanked (line count preserved)."""
    out = []
    for ln in lines:
        if ln.lstrip().startswith("%"):
            out.append("")
        else:
            out.append(COMMENT_RE.sub("", ln))
    return out


def classify(lines: list[str]) -> list[str]:
    """Per line: 'heading' | 'caption' | 'body' (captions tracked across lines by braces)."""
    kinds, depth, in_cap = [], 0, False
    for ln in lines:
        if HEADING_RE.search(ln):
            kinds.append("heading")
            continue
        if not in_cap and "\\caption" in ln:
            in_cap, depth = True, 0
            ln = ln[ln.index("\\caption"):]
        if in_cap:
            kinds.append("caption")
            depth += ln.count("{") - ln.count("}")
            if depth <= 0:
                in_cap = False
            continue
        kinds.append("body")
    return kinds


def chapters(lines: list[str]) -> list[tuple[str, int, int]]:
    """(title, start, end) per \\chapter, numbered 1.. before \\appendix and A.. after."""
    marks, appendix = [], False
    for i, ln in enumerate(lines):
        if ln.startswith("\\appendix"):
            appendix = True
        m = CHAPTER_RE.match(ln)
        if m and "*" not in ln.split("{")[0]:
            marks.append((m.group(1), i, appendix))
    out, n, a = [], 0, 0
    for k, (title, start, app) in enumerate(marks):
        end = marks[k + 1][1] if k + 1 < len(marks) else len(lines)
        if app:
            key = chr(ord("A") + a)
            a += 1
        else:
            n += 1
            key = str(n)
        out.append((f"{key}  {title}", start, end))
    return out


def chapter_range(lines: list[str], want: str | None) -> tuple[int, int]:
    if want is None:
        return 0, len(lines)
    for key, start, end in chapters(lines):
        if key.split()[0] == str(want):
            return start, end
    sys.exit(f"no chapter {want!r}; have {[c[0] for c in chapters(lines)]}")


def plain(ln: str) -> str:
    """Prose words only: commands with arguments, math and remaining macros removed."""
    ln = CMD_STRIP_RE.sub(" ", ln)
    ln = MATH_RE.sub(" ", ln)
    ln = re.sub(r"\\[A-Za-z]+\*?", " ", ln)
    return ln.replace("~", " ").replace("{", " ").replace("}", " ")


# --------------------------------------------------------------------------- census --
def cmd_census(a):
    raw = TEX.read_text().splitlines()
    text = strip_comments(raw)
    kinds = classify(text)
    lo, hi = chapter_range(raw, a.chapter)
    for term in a.terms:
        rx = re.compile(re.escape(term), re.I)
        by = defaultdict(list)
        for i in range(lo, hi):
            n = len(rx.findall(text[i]))
            if n:
                by[kinds[i]].append((i + 1, n))
            if raw[i] != text[i] and rx.search(raw[i][len(text[i]):] if raw[i].startswith(text[i]) else raw[i]):
                by["comment"].append((i + 1, len(rx.findall(raw[i])) - n))
        floats = []
        for d in FLOAT_DIRS:
            for f in sorted(d.glob("*.tex")):
                n = sum(len(rx.findall(l)) for l in strip_comments(f.read_text().splitlines()))
                if n:
                    floats.append((f.name, n))
        tot = sum(n for k in ("body", "heading", "caption") for _, n in by[k])
        print(f"{term!r}: prose {tot}  (body {sum(n for _, n in by['body'])}, headings "
              f"{sum(n for _, n in by['heading'])}, captions {sum(n for _, n in by['caption'])}); "
              f"float files {sum(n for _, n in floats)}; comments {sum(n for _, n in by['comment'])}")
        for k in ("heading", "caption", "body"):
            if by[k]:
                print(f"    {k:8s} " + ", ".join(f"l.{l}" + (f"×{n}" if n > 1 else "") for l, n in by[k]))
        for name, n in floats:
            print(f"    float    {name} ×{n}")


# ------------------------------------------------------------------------- acronyms --
def cmd_acronyms(a):
    raw = TEX.read_text().splitlines()
    text = strip_comments(raw)
    lo, hi = chapter_range(raw, a.chapter)
    first, count, expanded_at = {}, Counter(), {}
    for i in range(lo, hi):
        ln = plain(text[i])
        for m in ACRO_RE.finditer(ln):
            acro = m.group(1)
            if re.fullmatch(r"L\d|[IVX]+", acro):
                continue  # the L-labels and roman numerals are not acronyms
            count[acro] += 1
            first.setdefault(acro, i + 1)
            if acro not in expanded_at and re.search(r"\(\s*" + re.escape(acro) + r"s?\s*\)", ln):
                expanded_at[acro] = i + 1
    rows = sorted(count, key=lambda k: (k in expanded_at, first[k]))
    print(f"{'acronym':10s} {'uses':>5s} {'first':>6s} {'expanded':>9s}")
    for acro in rows:
        exp = expanded_at.get(acro)
        tag = "never" if exp is None else ("here" if exp == first[acro] else f"l.{exp} (late)" if exp > first[acro] else f"l.{exp}")
        print(f"{acro:10s} {count[acro]:5d} {first[acro]:6d} {tag:>9s}")


# -------------------------------------------------------------------------- phrases --
def ngrams(words: list[str], n: int):
    for k in range(len(words) - n + 1):
        g = words[k:k + n]
        if g[0] in STOP or g[-1] in STOP or any(len(w) < 3 for w in g):
            continue
        yield " ".join(g)


def words_of(lines: list[str], lo: int, hi: int) -> list[str]:
    out = []
    for i in range(lo, hi):
        out.extend(w.lower() for w in TOKEN_RE.findall(plain(lines[i])))
        out.append(".")  # sentence-ish boundary so n-grams do not cross lines
    return out


def cmd_phrases(a):
    raw = TEX.read_text().splitlines()
    text = strip_comments(raw)
    lo, hi = chapter_range(raw, a.chapter)
    before = Counter()
    for n in range(2, a.max_words + 1):
        before.update(ngrams(words_of(text, 0, lo), n))
    here = Counter()
    for n in range(2, a.max_words + 1):
        here.update(ngrams(words_of(text, lo, hi), n))
    rows = [(p, c) for p, c in here.items() if c >= a.min and before[p] == 0 and "." not in p]
    # drop a phrase wholly contained in a longer phrase with the same count
    longer = {p for p, _ in rows}
    rows = [(p, c) for p, c in rows if not any(p != q and p in q and here[q] == c for q in longer)]
    rows.sort(key=lambda pc: (-pc[1], pc[0]))
    print(f"phrases first appearing in chapter {a.chapter}, used >= {a.min} times there ({len(rows)}):")
    for p, c in rows:
        print(f"  {c:4d}  {p}")


# ------------------------------------------------------------------------- variants --
def cmd_variants(a):
    raw = TEX.read_text().splitlines()
    text = strip_comments(raw)
    lo, hi = chapter_range(raw, a.chapter)
    forms = defaultdict(Counter)
    for i in range(lo, hi):
        toks = TOKEN_RE.findall(plain(text[i]))
        for k in range(len(toks) - 1):
            w1, w2 = toks[k], toks[k + 1]
            if w1.lower() in STOP or w2.lower() in STOP:
                continue
            key = re.sub(r"s$", "", (w1 + w2).lower().replace("-", ""))
            forms[key][f"{w1} {w2}"] += 1
        for t in toks:
            if "-" in t:
                key = re.sub(r"s$", "", t.lower().replace("-", ""))
                forms[key][t] += 1
    rows = [(k, c) for k, c in forms.items() if len(c) > 1 and sum(c.values()) >= a.min]
    rows.sort(key=lambda kc: -sum(kc[1].values()))
    print(f"two-word concepts spelt more than one way ({len(rows)}):")
    for _, c in rows:
        print("  " + "  |  ".join(f"{f} ×{n}" for f, n in c.most_common()))


# ----------------------------------------------------------------------------- main --
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("census"); p.add_argument("terms", nargs="+"); p.add_argument("--chapter")
    p.set_defaults(fn=cmd_census)
    p = sub.add_parser("acronyms"); p.add_argument("--chapter"); p.set_defaults(fn=cmd_acronyms)
    p = sub.add_parser("phrases"); p.add_argument("--chapter", required=True); p.add_argument("--min", type=int, default=3)
    p.add_argument("--max-words", type=int, default=3); p.set_defaults(fn=cmd_phrases)
    p = sub.add_parser("variants"); p.add_argument("--chapter"); p.add_argument("--min", type=int, default=2)
    p.set_defaults(fn=cmd_variants)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
