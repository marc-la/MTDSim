"""Extract Marc's own prompts from the session transcripts, as a dated research corpus.

    python tools/prompt_corpus.py stats                          # the corpus, measured
    python tools/prompt_corpus.py stats --until 2026-08-06        # as it stood on a given day
    python tools/prompt_corpus.py extract --min-words 150 -o corpus.jsonl
    python tools/prompt_corpus.py gate                           # the filter-set regression check
    python tools/prompt_corpus.py extract --root ~/mtdsim-corpus-snapshot/2026-08-08/acc1

Serves `docs/handoffs/2026-08-06_research_record_from_prompt_corpus.md`, whose
premise is that **the prompts are the record of human intent and the assistant's
output is an execution layer** — so where the two disagree about what the
research was, the prompts win. This tool is the only mechanical part of that
brief: it turns ~230 MB of transcript across two account stores into one stable
JSONL of human-authored records, which the mining then triages by hand.

**A living tool**, in the sense `docs/implementation/trace_tool.md` means it.
It will be re-run as sessions accumulate, so extend the filter set here rather
than re-deriving it in an ad-hoc probe. The precedent it replaces is exactly that
mistake: `voice_corpus_prompts_2026-07.txt` was pulled by an uncommitted script,
keyed only by session filename, and its figures cannot now be reproduced (see
`gate` below).

What it emits, per surviving record: ``timestamp``, ``sessionId``, ``uuid``,
``gitBranch``, ``cwd``, ``account``, ``source``, ``words``, ``chars``, ``text``.
The first five are what the voice-corpus pull omitted and what turn a pile of
prompts into a research record — a claim in the annal cannot be dated, or
cross-referenced against the commit that acted on it, without them. Triage
decisions attach to ``uuid``, never to a line number.

**Scope.** Top-level ``*.jsonl`` only. Each session directory also holds nested
subagent transcripts and tool results (355 files); all of it is assistant
execution detail, and none of it is speech. ``--include-nested`` exists for
inspection and should not be used to build a corpus.

**The corpus is unbacked and lives outside the repo.** Snapshot it before
analysing anything: a Claude Code reinstall or a routine ``~/.claude*`` prune
destroys three and a half months of irreplaceable primary source. Pass ``--root``
to read a snapshot rather than the live store.

**Never commit the output.** Transcripts carry absolute home paths, arbitrary
tool output, and pasted third-party material — supervisor emails, meeting
agendas, and at least one full meeting transcript. Paraphrase into the tracked
annal; the verbatim text stays in the untracked snapshot.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

# The two account stores holding this project's transcripts. The account-level
# `history.jsonl` files are ring buffers of ~20 records and are not a recovery
# path for anything missing here.
DEFAULT_ROOTS = [
    Path.home() / ".claude-acc1" / "projects" / "-home-marc-GitHub-MTDSim",
    Path.home() / ".claude-acc2" / "projects" / "-home-marc-GitHub-MTDSim",
]

# The snapshot the gate measures against. The live store is not a fixed corpus:
# on 2026-08-08, nine transcripts were deleted from `acc1` within hours of the
# snapshot being taken (106 files down to 97), which is why a regression check
# pinned to the live store fails for reasons that have nothing to do with the
# filter set. A snapshot is immutable by construction, so that is what `gate`
# reads. See the handoff's § *The corpus is not stable* for the loss event.
SNAPSHOT_ROOTS = [
    Path.home() / "mtdsim-corpus-snapshot" / "2026-08-08" / "acc1",
    Path.home() / "mtdsim-corpus-snapshot" / "2026-08-08" / "acc2",
]

# ---------------------------------------------------------------------------
# The filter set.
#
# Every rule below was derived from a wrapper actually found in this corpus, with
# the count it matched on 2026-08-08. The counts are documentation, not
# assertions: they grow as sessions accumulate. What must not change silently is
# the *set* — a new wrapper form that slips through here reads as Marc's intent
# in the annal, which is the one failure the whole brief is built to avoid.
# ---------------------------------------------------------------------------

# Dropped whole: harness-injected text that reads like prose and is not speech.
# The first three polluted the top of the length ranking on the survey's first
# pass, which is how each was found.
DROP_PREFIXES = (
    "Base directory for this skill:",   # 11 — skill preambles
    "Caveat: The messages below",       # compaction preamble, bare form
    "[Request interrupted",             # 4
    # Compaction *continuation* summaries. Assistant-authored, first-person, and
    # long — the one on 2026-08-05 runs to 2 464 words, which would have entered
    # the >= 150-word band as the fourth-longest "prompt" in the corpus. Found by
    # this tool on 2026-08-08; the handoff's own filter set does not list it.
    "This session is being continued from a previous conversation",
)

# Same, in tag form.
DROP_TAGS = (
    "<local-command-caveat",  # 61 — compaction preamble as the harness now wraps it
    "<task-notification",     # 31 — subagent completions; verified to carry no
                              #      appended human text in any of the 31
)

# Stripped, but the surrounding record is kept and re-tested for emptiness: these
# wrap or accompany something Marc actually typed.
STRIP_TAGS = (
    "system-reminder",
    "local-command-stdout",
    "command-name",
    "command-message",
    "command-args",
    "ide_opened_file",
    "ide_selection",
)

# ---------------------------------------------------------------------------
# The pinned regression check.
#
# The survey that commissioned the brief measured 73 prompts / 63 900 words at
# >= 150 words, by an uncommitted probe script. This tool measures 73 prompts —
# the same count — and 60 399 words over the same date bound.
#
# The 3 501-word difference is accounted for, and the account is worth keeping,
# because it is evidence for the brief's own premise. The two compaction
# continuation summaries this tool now drops carry 2 464 and 1 161 words; adding
# them back gives 64 024, which is within 124 words of the survey's figure. The
# survey therefore counted the assistant summarising itself as part of Marc's
# design-argument corpus — 5.5 % of the word mass it reported, and the single
# longest "prompt" of that April. The residual 124 words is wrapper handling that
# cannot be attributed further, because the probe was never committed. That is the
# defect this tool exists to remove.
#
# So the gate is pinned to what this tool measures, and the survey figure is
# recorded beside it as the superseded measurement rather than as a target to tune
# towards. Re-pin deliberately when the filter set is extended, and say why.
# ---------------------------------------------------------------------------
GATE_UNTIL = "2026-08-06"
GATE_MIN_WORDS = 150
GATE_PROMPTS = 73
GATE_WORDS = 60399
SURVEY_FIGURE = (
    "73 prompts / 63 900 words (2026-08-06 survey, uncommitted probe; its word "
    "mass includes 3 625 words of assistant-authored compaction summary)"
)


def _strip_wrappers(text: str) -> str:
    for tag in STRIP_TAGS:
        text = re.sub(rf"<{tag}>.*?</{tag}>", " ", text, flags=re.S)
        text = re.sub(rf"<{tag}\b[^>]*/>", " ", text)
    return text.strip()


def _transcripts(roots: list[Path], include_nested: bool):
    for root in roots:
        if not root.exists():
            print(f"warning: root does not exist, skipping: {root}", file=sys.stderr)
            continue
        # Which account store a record came from, whether the root is the live
        # store (`~/.claude-acc1/projects/<slug>`) or a snapshot of it
        # (`<snapshot>/acc1`). Reading a snapshot must not silently relabel
        # provenance, so fall back to the root's own name rather than guessing.
        account = next(
            (p.name.replace(".claude-", "") for p in root.parents if p.name.startswith(".claude-")),
            root.name,
        )
        pattern = "**/*.jsonl" if include_nested else "*.jsonl"
        for path in sorted(root.glob(pattern)):
            yield account, path


def _human_text(record: dict) -> str | None:
    """The human-authored text of one transcript record, or None if there is none.

    Two shapes carry text: a bare string, and a block list. A block list whose
    blocks are all ``tool_result`` is tool output rather than speech; a mixed list
    contributes only its ``text`` blocks (``image`` and ``document`` blocks are
    attachments, and their placeholders are not words Marc typed).
    """
    if record.get("type") != "user":
        return None
    # Sidechain records are subagent turns — the assistant talking to itself.
    # Currently always false in the top-level files (subagent traffic lives in the
    # nested directories), kept because that is a harness detail, not a guarantee.
    if record.get("isSidechain"):
        return None

    content = (record.get("message") or {}).get("content")
    if isinstance(content, str):
        parts = [content]
    elif isinstance(content, list):
        if content and all(
            isinstance(b, dict) and b.get("type") == "tool_result" for b in content
        ):
            return None
        parts = [
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        ]
    else:
        return None

    raw = "\n".join(p for p in parts if p).strip()
    if not raw:
        return None
    if raw.startswith(DROP_PREFIXES) or raw.startswith(DROP_TAGS):
        return None
    # A tag can also open the record after a stripped wrapper, so test the head
    # rather than only position 0.
    if any(tag in raw[:200] for tag in DROP_TAGS):
        return None

    text = _strip_wrappers(raw)
    return text or None


def harvest(roots, include_nested=False, since=None, until=None, min_words=0):
    """Every human-authored record in the corpus, in chronological order."""
    out = []
    for account, path in _transcripts(roots, include_nested):
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                text = _human_text(record)
                if text is None:
                    continue
                timestamp = record.get("timestamp") or ""
                day = timestamp[:10]
                if since and day and day < since:
                    continue
                if until and day and day > until:
                    continue
                words = len(text.split())
                if words < min_words:
                    continue
                out.append(
                    {
                        "timestamp": timestamp,
                        "sessionId": record.get("sessionId"),
                        "uuid": record.get("uuid"),
                        "gitBranch": record.get("gitBranch"),
                        "cwd": record.get("cwd"),
                        "account": account,
                        "source": path.name,
                        "words": words,
                        "chars": len(text),
                        "text": text,
                    }
                )
    out.sort(key=lambda r: (r["timestamp"], r["source"]))
    return out


def cmd_extract(args):
    records = harvest(
        args.root or DEFAULT_ROOTS,
        include_nested=args.include_nested,
        since=args.since,
        until=args.until,
        min_words=args.min_words,
    )
    handle = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout
    try:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    finally:
        if args.output:
            handle.close()
            print(
                f"{len(records)} records, {sum(r['words'] for r in records)} words "
                f"-> {args.output}",
                file=sys.stderr,
            )


def cmd_stats(args):
    records = harvest(
        args.root or DEFAULT_ROOTS, include_nested=args.include_nested, since=args.since, until=args.until
    )
    if not records:
        print("no records")
        return
    bands = [(0, "all human-authored records"), (15, "substantive (>= 15 words)"),
             (150, "the design-argument corpus (>= 150 words)")]
    print(f"roots: {', '.join(str(r) for r in (args.root or DEFAULT_ROOTS))}")
    print(f"transcripts: {len(set(r['source'] for r in records))}")
    print(f"date range: {records[0]['timestamp'][:10]} -> {records[-1]['timestamp'][:10]}")
    print(f"branches touched: {len(set(r['gitBranch'] for r in records if r['gitBranch']))}")
    print()
    for floor, label in bands:
        band = [r for r in records if r["words"] >= floor]
        print(f"{len(band):5d}  {sum(r['words'] for r in band):7d} words  {label}")
    print()
    band = [r for r in records if r["words"] >= 150]
    months = collections.Counter(r["timestamp"][:7] for r in band if r["timestamp"])
    print("the >= 150-word band, by month:")
    for month in sorted(months):
        print(f"  {month}  {months[month]:3d}")
    missing = _month_gaps(months)
    if missing:
        print(f"  no records at all in: {', '.join(missing)}")


def _month_gaps(months):
    """Months with no records between the first and last that have some.

    May and June 2026 are expected to be empty against 92 commits on `dev`. That
    window was introduction and literature-review work, so the blackout is a
    boundary to record rather than data to recover.
    """
    if not months:
        return []
    keys = sorted(months)
    first, last = keys[0], keys[-1]
    gaps = []
    year, month = int(first[:4]), int(first[5:7])
    while f"{year:04d}-{month:02d}" <= last:
        key = f"{year:04d}-{month:02d}"
        if key not in months:
            gaps.append(key)
        month += 1
        if month == 13:
            year, month = year + 1, 1
    return gaps


def cmd_gate(args):
    # Measure the snapshot unless a corpus was named explicitly. Pinning a
    # regression check to a mutable store makes the check report data loss as
    # filter drift, which is the opposite of useful.
    roots = args.root or [r for r in SNAPSHOT_ROOTS if r.exists()]
    if not roots:
        print("SKIP — no snapshot at "
              f"{SNAPSHOT_ROOTS[0].parent}. The pinned figure cannot be verified "
              "against the live store, which loses transcripts; re-take a "
              "snapshot (see the snapshot README) or pass --root explicitly.")
        return 1

    records = harvest(roots, until=GATE_UNTIL, min_words=GATE_MIN_WORDS)
    prompts, words = len(records), sum(r["words"] for r in records)
    print(f"corpus: {', '.join(str(r) for r in roots)}")
    print(f"pinned: {GATE_PROMPTS} prompts / {GATE_WORDS} words "
          f"(>= {GATE_MIN_WORDS} words, timestamp <= {GATE_UNTIL})")
    print(f"measured: {prompts} prompts / {words} words")
    print(f"superseded: {SURVEY_FIGURE}")
    if (prompts, words) == (GATE_PROMPTS, GATE_WORDS):
        print("PASS — filter set unchanged")
        return 0
    print("FAIL — the filter set has drifted against a fixed corpus, so this is "
          "a bug in the tool rather than a new finding: a wrapper form has "
          "started or stopped matching.")
    return 1


def main(argv=None):
    # The corpus flags sit on a parent parser so they read naturally after the
    # subcommand, which is where a hand would put them.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--root", type=Path, action="append", metavar="DIR",
        help="a transcript directory; repeatable. Defaults to both account stores. "
             "Point it at a snapshot to analyse a pinned corpus.",
    )
    common.add_argument(
        "--include-nested", action="store_true",
        help="also read nested subagent transcripts. For inspection only — they "
             "are assistant execution detail, not speech.",
    )
    dates = argparse.ArgumentParser(add_help=False)
    dates.add_argument("--since", metavar="YYYY-MM-DD")
    dates.add_argument("--until", metavar="YYYY-MM-DD")

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("extract", parents=[common, dates],
                       help="write one JSONL record per human prompt")
    p.add_argument("--min-words", type=int, default=0)
    p.add_argument("-o", "--output", metavar="FILE",
                   help="never inside the repo — see the module docstring")
    p.set_defaults(func=cmd_extract)

    p = sub.add_parser("stats", parents=[common, dates], help="measure the corpus")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("gate", parents=[common],
                       help="the filter-set regression check")
    p.set_defaults(func=cmd_gate)

    args = parser.parse_args(argv)
    # Each subcommand resolves its own corpus: extract/stats read the live
    # store, gate reads the immutable snapshot.
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
