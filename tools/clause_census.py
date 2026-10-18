"""Count the punctuation that marks clause stacking in the dissertation, against a
human-written baseline from the field — the mechanical half of the clausing check
(docs/workflows/clausing_check.md).

    python tools/clause_census.py rates
        colons, semicolons, commas and dashes per 1 000 words: each dissertation
        chapter, its captions and headings, beside the pre-2023 field papers
    python tools/clause_census.py flags [--chapter NAME] [--kind prose|caption|heading]
        every unit that trips a flag (a colon; four or more commas; a short trailing
        clause after the last comma), with its line — the work list for the ledger
    python tools/clause_census.py worklist [--out DIR]
        every unit assigned to exactly one cluster by the thresholds of
        clausing_check.md §5 (floats and headings > colons > comma jobs > words),
        written as one JSONL work list per cluster for the cluster agents

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
                         "text": ci.plain(m.group(2)), "tex": ln})
    return rows


def baseline_text(key: str) -> str:
    t = (TEXTS / f"{key}.txt").read_text(errors="ignore")
    cut = [m.start() for m in re.finditer(r"\n\s*(R\s?EFERENCES|References|Bibliography)\s*\n", t)]
    if cut:
        t = t[: cut[-1]]
    # drop short lines (running heads, table cells, page numbers, figure labels)
    return " ".join(ln for ln in t.split("\n") if len(WORD.findall(ln)) >= 6)


# ---- thresholds (clausing_check.md §5) ---------------------------------------------
APPOS = re.compile(r"\b[A-Za-z][\w\-]*, (?:a|an|the) [^,.;:]{3,60}?(?:,|\.$)")
PART_TAIL = re.compile(r", (?:[a-z]+ly )?[a-z]+ing\b[^,;:]{0,60}\.?$")
FIGURATIVE = re.compile(r"\b(deeper|opened|opens up|unfold\w*|journey|pool of|stands? (?:for|in for)|lands?|"
                        r"walks?|behind|sits?|lives?|drives?|feeds?|fuels?|shapes?|paints?|picture|lens|"
                        r"backbone|heart of|toolbox|arsenal|landscape|footprint|window into|sheds? light|"
                        r"carr(?:y|ies) (?:the|its)|speaks?|tells?|answers?)\b", re.I)
UNNEEDED = re.compile(r"\b(none|does not state|do not state|not stated|nothing|no such)\b", re.I)
EMPH = re.compile(r"\\emph\{([^{}]{2,60})\}")
COUNT_LEAD = re.compile(r"\b(two|three|four|five|six|seven|eight|nine|ten|\d+|following|as follows|both)\b[^:]*:", re.I)
CALIBRATION_LINES = [(723, 726), (806, 808), (1229, 1229), (1593, 1596), (1706, 1709), (2195, 2197), (3578, 3580)]
CALIBRATION_LABELS = {"fig:mtdsim-model", "fig:network-model", "tab:defence-mechanisms",
                      "tab:deployment-strategies", "tab:attacker-objectives",
                      "tab:lineage-configurations", "fig:attack-matrix"}
CALIBRATION_HEADS = re.compile(r"^(Properties an MTD attacker model|APT attacker model versus MTD attacker|"
                               r"Predicate tests|The attack graph with|The sources behind|Edges of the|"
                               r"Tactic durations against|The rules and the|Where each value|MTDShield as run|"
                               r"Disruption per MTD|MTD ranking against|Sensitivity analysis of|Ablation studies|"
                               r"Ablation of the tactic)")
FRONT = ("Introduction", "Background", "Literature review", "APT attacker model")


def rare_terms(rows: list[dict]) -> dict[str, int]:
    """Emphasised (defined) terms and their uses in the body after the definition."""
    body = " ".join(r["text"].lower() for r in rows if r["kind"] == "prose")
    out = {}
    defs = {m.group(1) for r in rows if r["kind"] == "prose" for m in EMPH.finditer(r.get("tex", ""))}
    for t in defs:
        t2 = re.sub(r"\s+", " ", re.sub(r"[{}\\]", "", t)).strip().lower()
        if t2 and not t2.startswith("$"):
            out[t2] = max(body.count(t2) - 1, 0)
    return {k: v for k, v in out.items() if v <= 2}


def assign(r: dict, rare: dict) -> tuple[str | None, list[str]]:
    t, m = r["text"], marks(r["text"])
    why = []
    if m["colon"]:
        why.append("colon" + (" after a count" if COUNT_LEAD.search(t) else ""))
    if m["comma"] >= 4:
        why.append(f"{m['comma']} commas")
    if trailing(t) or PART_TAIL.search(t.strip()):
        why.append("trailing clause")
    if APPOS.search(t):
        why.append("appositive")
    for f in FIGURATIVE.findall(t):
        why.append(f"figurative? '{f}'")
    if UNNEEDED.search(t):
        why.append("unneeded?")
    for term in rare:
        if f"\\emph{{{term}" in re.sub(r"\s+", " ", r.get("tex", "")).lower():
            why.append(f"defined '{term}', reused {rare[term]}x")
    if r["kind"] in ("caption", "heading"):
        return "F_floats_headings", why or ["read in full"]
    if not why:
        return None, why
    if m["colon"]:
        return "C_colons", why
    if any(w.startswith(("trailing", "appositive")) or w.endswith("commas") for w in why):
        return ("A1_commas_ch1-4" if r["chapter"] in FRONT or r["chapter"] is None else "A2_commas_ch5-app"), why
    return "D_words", why


def calibrated(r: dict) -> bool:
    if r["kind"] == "heading":
        return bool(CALIBRATION_HEADS.match(r["text"]))
    if r.get("label") in CALIBRATION_LABELS and r["kind"] == "caption":
        return True
    o = r["origin"]
    if o.startswith("L"):
        n = int(o[1:].split("-")[0])
        return any(a <= n <= b for a, b in CALIBRATION_LINES)
    return False


def cmd_worklist(a) -> None:
    import json
    rows = [r for r in dissertation_units() if r["chapter"] != "AI Use Declaration"]
    rare = rare_terms(rows)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    lists: dict[str, list] = defaultdict(list)
    for r in rows:
        if calibrated(r):
            continue
        cl, why = assign(r, rare)
        if cl:
            lists[cl].append({"origin": r["origin"], "chapter": r["chapter"], "kind": r["kind"],
                              "label": r.get("label"), "flags": why, "text": r["text"]})
    for cl, items in sorted(lists.items()):
        (out / f"{cl}.jsonl").write_text("".join(json.dumps(i) + "\n" for i in items))
        print(f"{cl:22s}{len(items):4d}")
    print("rare defined terms:", ", ".join(f"{k} ({v})" for k, v in sorted(rare.items())))


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
    w = sub.add_parser("worklist")
    w.add_argument("--out", default=str(REPO / "data" / "clausing_check" / "worklists"))
    w.set_defaults(fn=cmd_worklist)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
