---
name: dissect-paper
description: >
  Deep, multi-pass dissection of an APT / adversary-simulation / MTD / MITRE-ATT&CK
  paper into (1) a docs/sources/extractions/<key>.md record and (2) targeted evidence edits
  across the 15 docs/notes/ch3_design/tactic_profiles/. Use when the user wants to extract, dissect,
  mine, or "properly read" a valuable paper for per-tactic dwell / behaviour / MTD
  evidence. Counters GenAI skim-loss with a value-triaged, section-by-section,
  page-anchored protocol that preserves fine grain AND emergent ideas. Triggers:
  "dissect this paper", "extract <paper>", "mine <paper> into the tactic profiles",
  "read <paper> properly", "add <paper> to the lit review".
---

# Dissect a paper into tactic profiles

The job: turn one valuable paper into durable, page-anchored evidence in this
repo's two homes — the per-paper **extraction** and the per-tactic **profiles** —
without the losses a one-shot summary produces. The user's explicit concern is
that GenAI parsing loses (a) fine grain (exact numbers, rates, locators) and
(b) main / emergent ideas (the argument, the methodological move, the caveat).
This protocol is built to counter both. **Effort scales to value: a valuable
paper gets the full multi-pass treatment; a thin one gets a short extraction that
records *why* it's thin.**

## The anti-loss rule (read this first — it is the whole point)

**You, the main agent, read the whole source yourself, in full.** Do **not** hand
the reading to a subagent that returns a summary — that summary *is* the lossy
compression the user is complaining about. Subagents are allowed only as an
*additive completeness critic* (a second reader that lists what your draft
missed), never as the primary reader. Consequences:

- **The parsed markdown is the single source of truth** — original PDFs are not
  retained. Read the `.md` in `docs/sources/` in full. This is an accepted
  trade: the method is **shape-not-scale** (relative structure, orderings,
  order-of-magnitude anchors — not exact digits), and all of that survives md
  parsing, as does the prose that carries the real value (does the paper assign
  timing, *where* its numbers came from, whether a tactic is low-and-slow). What
  md parsing damages — the last digits of a number in a garbled table — is
  precisely what shape-not-scale calibration does not need.
- **The real risk is laundered precision, not lost precision.** When a table,
  equation, or number looks garbled, misaligned, or OCR-mangled in the md, flag it
  `[parse-uncertain]` and record what you can actually read — **never invent a
  tidy value** to replace a broken one. A flagged fuzzy number is honest; a
  confident wrong one poisons the catalogue.
- Read the whole thing — do not stop at the abstract/intro. If no parsed `.md` is
  present in `docs/sources/` (gitignored), ask the user for it; **never dissect
  from a web snippet or memory**.
- Every number, rate, dwell, or per-tactic claim is captured **verbatim with a
  locator** — the section heading (md loses page numbers). No paraphrased number
  without a locator.
- Tables and appendices are where timing/parameters hide — read and transcribe
  them explicitly; they are the first casualty of both skimming *and* md parsing,
  so read them slowly and flag any that are structurally broken.
- Keep two streams separate and both first-class: **"what it says"** (fine grain)
  and **"what it means / implies"** (emergent ideas, the methodological move, what
  the authors leave implicit). Emergent ideas get their own list — they are not
  reconstructable later from the fine-grain notes.

## Before you start

Load the discipline (skim, don't re-derive):
- [`docs/workflows/guardrails.md`](../../../docs/workflows/guardrails.md) — **papers are
  claims to reconcile, not ground truth**; never guess a locator or DOI.
- [`docs/sources/extractions/_template.md`](../../../docs/sources/extractions/_template.md) — the
  extraction shape (bibliographic anchor, per-concept locators, disposition).
- [`docs/notes/ch3_design/tactic_profiles/README.md`](../../../docs/notes/ch3_design/tactic_profiles/README.md) and
  [`docs/notes/ch3_design/tactic_profiles/_template.md`](../../../docs/notes/ch3_design/tactic_profiles/_template.md)
  — the 15 tactics (ATT&CK v19.1), the five timing groups, and the two claims each
  profile needs: **dwell character** + **MTD disruption**.
- [`docs/notes/ch3_design/operational_validation.md`](../../../docs/notes/ch3_design/operational_validation.md)
  — what evidence is *for*: group assignment, sweep width, tier badge. Timing
  never comes from the corpus / `observation_count`; breach-report *statistics* are
  allowed Tier-2 literature.

## Pass 0 — Value triage (decide the effort tier)

Read title, abstract, section headings, and every table caption. Score the paper
on what this thesis needs:

- **APT tactic behaviour** — does it describe what an actor does within a tactic,
  low-and-slow vs fast?
- **Timing / rates / dwell** — any numbers, transition rates, mean-times,
  stage durations? And crucially *where the authors got them* (empirical /
  expert / declared / calibrated).
- **MTD → attacker effect** — anything on how a defensive move perturbs an
  attacker (rare and valuable — the genuine unknown).
- **Adversary-simulation / formal model** — SPN/CTMC/attack-graph/DES, and how
  it's parameterised.

Assign a tier and say so to the user:
- **Deep** (hits ≥2 of the above, esp. timing or MTD-effect) → full Pass 1–3,
  per-page read, completeness critic.
- **Targeted** (hits 1) → read only the relevant sections deeply; short extraction.
- **Thin** (structure/CTI only, no timing/behaviour value) → a brief extraction
  recording what it is and **why it's thin** (a documented negative is useful —
  it's gap evidence). Stop; don't force tactic edits.

## Pass 1 — Structural map (Deep/Targeted)

Walk the whole paper quickly to build a section map: for each section, one line on
what it contains and whether it holds value (method / params / timing / per-tactic
behaviour / MTD / caveats). Mark the high-value sections for Pass 2. Note where the
numbers live (usually a parameters/evaluation table or an appendix).

## Pass 2 — Deep read of the value sections (Deep/Targeted)

Read the marked sections in full, at the page level. As you go, capture into a
scratch note:
- **Fine grain:** every value/rate/dwell verbatim + locator; the exact
  parameterisation; the definitions the authors use (their "dwell" may not be
  yours — record their anchors).
- **Provenance of each number:** empirical / expert-elicited / declared-arbitrary
  / calibrated. This is often the single most useful thing for our gap argument —
  capture the sentence that reveals it.
- **Emergent / main ideas:** the argument, the methodological move, the assumption
  that carries the result, what they leave implicit, the caveat they bury. One
  bullet each. These are outputs, not notes.
- **Per-tactic hits:** for each ATT&CK tactic the paper touches, jot the claim and
  which of §2 (behaviour/group) / §3 (MTD) / §4 (timing) it informs.

## Pass 3 — Completeness / adversarial re-read (Deep)

Two moves, both cheap and both required for a Deep paper:
1. **Self-critic sweep:** re-open tables, figures, footnotes, and the appendix and
   ask "what number or caveat did I not capture?" Add what you missed.
2. **Independent completeness critic (subagent):** spawn one general-purpose agent,
   point it at the *same source file* (not your notes), and ask: "Read this paper.
   Here is my draft extraction. List every load-bearing number, per-tactic claim,
   methodological move, or caveat it MISSES, with page locators." Fold in what
   survives. (This is additive verification, not delegated reading — the critic
   reads the primary source, and you reconcile.)

## Produce the two artefacts

**1 — The extraction** `docs/sources/extractions/<key>.md` (key = `lastname-year`, or
`institution year` form). Use the extraction template exactly: bibliographic
anchor, one block per relevant concept with **§/page locator**, sparing quotes,
`Maps to:` cross-links, and a **disposition** (verified / divergent / declared /
adopted-as-baseline / contrasted). Add two lists that the template already invites
and that fight parsing-loss directly: **emergent ideas** (under a dedicated
heading, not folded into concepts) and **open questions / things to verify**.

**2 — The tactic-profile edits.** For each of the 15
`docs/notes/ch3_design/tactic_profiles/NN_<tactic>.md` the paper touches:
- Add a **§4 Timing evidence** row: `Source (extraction §ref + page) | Claim |
  How adapted to this tactic | Confidence`. Flag `[fetched]` (you read it here) vs
  `[search]` (secondary). A "no direct value — confirms gap" row is valid and
  worth recording.
- If the paper informs the **§2 group argument** or **§3 MTD reasoning**, add a
  sentence there citing the extraction — do **not** overwrite the researcher's
  synthesis; append evidence and attribute it.
- **v19.1 split:** allocate any old `defense-evasion` claim across `stealth`
  (hiding/evasion) and `defense-impairment` (disabling defences); don't dump it in
  one. Note the allocation.
- Do **not** write a §5 number from a single paper — §5 is the researcher's
  cross-source synthesis. The skill supplies *evidence rows*, not the verdict.

## Before you call it done (self-check)

- [ ] The full parsed `.md` was read directly — not summarised from abstract or
      web. Any garbled table/number was flagged `[parse-uncertain]`, never
      "cleaned up" into an invented value.
- [ ] Every captured number/rate has a section-heading locator; nothing
      fabricated; `[fetched]`/`[search]` flagged throughout.
- [ ] For a Deep paper, the **emergent-ideas** list is non-empty and the
      completeness-critic pass ran.
- [ ] Extraction and every tactic edit **cross-link** (extraction `Maps to:` the
      tactics; each tactic row cites the extraction + page).
- [ ] Timing claims respect the constraints: nothing from the corpus /
      `observation_count`; the paper's provenance-of-numbers is recorded.
- [ ] Reconciliation debt is explicit: anything `[search]` or uncertain is flagged
      for the researcher, not silently promoted.
- [ ] Australian English in prose; ATT&CK identifiers verbatim; branch hygiene;
      **never push** without an explicit ask.

## Report back

Tell the user, concisely: the value tier you assigned and why; which tactics got
evidence and which the paper is silent on; the most important emergent idea or
number found; and any reconciliation debt left for them. Lead with what the paper
*buys* the tactic profiles, not a process log.
