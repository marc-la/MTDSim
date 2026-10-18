"""Count the punctuation that marks clause stacking in the dissertation, against a
human-written baseline from the field — the mechanical half of the clausing check
(docs/workflows/clausing_check.md).

    python tools/clause_census.py rates
        colons, semicolons, commas and dashes per 1 000 words: each dissertation
        chapter, its captions and headings, beside the pre-2023 field papers
    python tools/clause_census.py flags [--chapter NAME] [--kind prose|caption|heading]
        every unit that trips a flag (a colon; four or more commas; a short trailing
        clause after the last comma), with its line — the work list for the ledger

A flag marks a sentence to read, never a sentence to change: a colon that introduces
a list or an equation is warranted, and the session judges each one (clausing_check.md
§3). Units come from claim_inventory.units(), so the two tools agree on what a
sentence is. A living tool — extend it here rather than re-deriving a count ad hoc.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import claim_inventory as ci  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
TEXTS = REPO / "_workspace" / "sources" / "_text"
TEX = REPO / "docs" / "thesis" / "dissertation.tex"

# Peer-reviewed field papers published before 2023: the human-written baseline.
BASELINE = """alavizadeh2022 alshamrani2019 bland2020 cho2020 chobenasher2018 cremonini2005
holm2014 hong2018 hongkim2012harm hongkim2016 hutchins2011 jung2004 madan2004
manadhatawing2011tse pendleton2016 strom2018mitre zaffarano2015 zhan2013 zhuang2012
sargent2011""".split()

WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
HEAD = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{(.*)\}")
# a short final segment after the last comma: the appended nuance clause
TRAIL_MAX = 7


def marks(text: str) -> dict:
    t = re.sub(r"https?://\S+", " ", text)
    return {
        "words": len(WORD.findall(t)),
        "colon": len(re.findall(r"(?<![\\\d]):(?!\d)", t)),
        "semicolon": len(re.findall(r"(?<!\\);", t)),
        "comma": t.count(","),
        "dash": t.count("---") + t.count("\u2014"),
    }


def plain(tex: str) -> str:
    s = re.sub(r"\\cite[pt]?\*?(\[[^\]]*\])?\{[^}]*\}", "", tex)
    s = re.sub(r"\\(?:ref|cref|Cref|eqref|autoref|label)\{[^}]*\}", "1", s)
    s = re.sub(r"\$[^$]*\$", "x", s)
    return ci.plain(s)


def trailing(text: str) -> bool:
    if text.count(",") < 2:
        return False
    tail = text.rsplit(",", 1)[1]
    return 0 < len(WORD.findall(tail)) <= TRAIL_MAX


def dissertation_units() -> list[dict]:
    rows = [dict(r, text=plain(r["tex"])) for r in ci.units() if r["kind"] in ("prose", "caption")]
    chapter = None
    for i, ln in enumerate(TEX.read_text().split("\n"), 1):
        ln = re.sub(r"(?<!\\)%.*", "", ln)
        m = HEAD.search(ln)
        if m:
            if m.group(1) == "chapter":
                chapter = ci.plain(m.group(2))
            rows.append({"kind": "heading", "origin": f"L{i}", "chapter": chapter,
                         "text": ci.plain(m.group(2))})
    return rows


def baseline_text(key: str) -> str:
    t = (TEXTS / f"{key}.txt").read_text(errors="ignore")
    cut = [m.start() for m in re.finditer(r"\n\s*(R\s?EFERENCES|References|Bibliography)\s*\n", t)]
    if cut:
        t = t[: cut[-1]]
    # drop short lines (running heads, table cells, page numbers, figure labels)
    return " ".join(ln for ln in t.split("\n") if len(WORD.findall(ln)) >= 6)


def per_k(c: dict) -> str:
    w = max(c["words"], 1)
    return "  ".join(f"{k} {1000 * c[k] / w:5.1f}" for k in ("colon", "semicolon", "comma", "dash"))


def add(acc: dict, m: dict) -> None:
    for k, v in m.items():
        acc[k] += v


def cmd_rates(_a) -> None:
    groups: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    for r in dissertation_units():
        if r["chapter"] in (None, "AI Use Declaration"):
            continue
        key = r["kind"] + "s" if r["kind"] != "prose" else r["chapter"]
        add(groups[key], marks(r["text"]))
        if r["kind"] == "prose":
            add(groups["ALL PROSE"], marks(r["text"]))
    base = defaultdict(int)
    missing = [k for k in BASELINE if not (TEXTS / f"{k}.txt").exists()]
    for k in BASELINE:
        if k not in missing:
            add(base, marks(baseline_text(k)))
    print(f"{'per 1 000 words':52s} words")
    for name, c in groups.items():
        print(f"{name[:50]:52s}{c['words']:6d}   {per_k(c)}")
    print(f"{'BASELINE: ' + str(len(BASELINE) - len(missing)) + ' field papers before 2023':52s}"
          f"{base['words']:6d}   {per_k(base)}")
    if missing:
        print("missing baseline texts:", " ".join(missing))


def cmd_flags(a) -> None:
    for r in dissertation_units():
        if a.chapter and (r["chapter"] or "") .lower().find(a.chapter.lower()) < 0:
            continue
        if a.kind and r["kind"] != a.kind:
            continue
        t, m = r["text"], marks(r["text"])
        why = []
        if m["colon"]:
            why.append("colon")
        if m["comma"] >= 4:
            why.append(f"{m['comma']} commas")
        if trailing(t):
            why.append("trailing clause")
        if why:
            print(f"{r['origin']:>7} {r['kind'][:4]} [{', '.join(why)}] {t}")


def main(argv=None) -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("rates").set_defaults(fn=cmd_rates)
    f = sub.add_parser("flags")
    f.add_argument("--chapter")
    f.add_argument("--kind", choices=["prose", "caption", "heading"])
    f.set_defaults(fn=cmd_flags)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
