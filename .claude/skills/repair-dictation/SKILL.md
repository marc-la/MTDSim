---
name: repair-dictation
description: >
  Take Marc's raw dictated draft (voice-to-text transcript) and return it
  transcription-repaired AND register-swept (pass 2 + pass 3a of the drafting
  pipeline): STT errors fixed with technical vocabulary watched hardest,
  disfluencies and speech pads dropped, run-ons split at conjunctions,
  meta-narration beheaded, every hedge flagged as a [3b] marker for Marc to
  resolve — NEVER resolved by the session, and never a synonym substitution or
  a rewritten sentence. Use when Marc pastes a spoken draft and says "repair
  this dictation", "transcription repair", "run pass 2/3a", "tidy my spoken
  draft", "clean up this transcript". Not for content scrutiny (that is
  scrutinise-draft / pass 4) and never for generating or rewording prose.
---

# Repair a dictated draft — transcription repair + register pass 3a, one move

The job: Marc speaks a draft long (pipeline pass 1); this skill converts the
raw transcript into clean *written-down speech* that is still entirely his —
pass 2 (transcription repair) and pass 3a (the mechanical half of the register
pass) run together, because they are the same mode: **deletion and repair,
never word choice**. Everything requiring a choice of words — hedge
resolutions, replacement nouns, recasts — is flagged for Marc's 3b walk, never
done.

## The one rule

**Deleting Marc's words cannot inject a session's; choosing words can.** So:
delete, split, and make word-level *repairs* freely (each one logged); flag
everything else. A repaired draft in which any sentence was rewritten
wholesale, any synonym substituted, or any hedge resolved has failed — that is
the AI-flatten voice failure arriving through "helpful" repairs
(`docs/workflows/voice.md` owns the rationale; `docs/workflows/draft_scrutiny.md`
§a owns the no-generation rule this inherits).

## Step 1 — transcription repair (pass 2)

- **Fix STT mangles, watching technical vocabulary hardest.** Speech-to-text
  mangles exactly the words that matter, and a wrong technical term that
  survives to later drafts becomes invisible. Use the mangle dictionary and
  minimal-pair list below — the session's project context is what the
  dictation tool lacks, and it makes these repairs cheap and near-certain.
  When a repair changes a technical claim (not just a word), it goes on the
  **verify watchlist**, not silently in.

### The mangle dictionary — observed pairs (append new ones as they occur)

This is a living list; every session that catches a new mangle **adds it
here** rather than leaving the knowledge in chat.

| Heard | Meant |
|---|---|
| apartment (attacker) | APT (attacker) |
| my toe / the MITRE group | MITRE / the MITRE Corporation |
| moderate attack framework / Mitotech | MITRE ATT&CK framework |
| A tag flow / attack close | Attack Flow / attack flows |
| cold current / Co Currency / Co Occurrence | co-occurrence |
| cute word mining | keyword mining |
| a way to (three) | a weight of (three) |
| Ned Tacker | an attacker |
| brunch (under) | branch (under) |
| Cyberstar intelligence | cyber threat intelligence |
| opposite observability | the observability boundary |
| insert Roman (22) | insert reference (22) |
| started detection | start at detection |
| impairable call | empirical |
| repairance | reappearance |
| 8088% | 88% |
| all paths | OR paths |
| the logical end | the logical AND |
| general (the net) | generalised (ruled term: "generalised", never "general") |
| Apgujeet | APT group |
| Alchemrani / Al Shamrani | Alshamrani |
| sticks / the stick starter set | STIX / the STIX (?) set — second half unresolved, flag |
| empty evaluation | MTD evaluation |
| the tech players | threat actors (verify-listed once, 2026-08-17) |
| Jacquard | Jaccard |
| for this joint (graphs) | four disjoint (graphs) |
| attack grass | attack graphs |
| objective condition (attacker/graph) | objective-conditioned |
| Sea appendix | see Appendix |
| attack web corpus / attack bloat corpus / blue corpus | Attack Flow corpus |
| the older floors | whole flows |
| AP2 group | APT group |
| terminal taxi | terminal tactic |
| petitions | partitions |
| a heave against | behave against |
| the six data set | the STIX data set |
| mother (has decided) | MITRE (has decided) |
| attachment motivation | attacker's motivation |
| rich (exfiltration) | reach (exfiltration) |
| attack files (objective-conditioned) | attack profiles |
| Patriots / patronet / patronage | Petri nets / Petri net |
| empty SIM | MTDSim |
| movement lay | movement layer |
| two way joint | two-way join |
| dual times | dwell times |
| (necessary but) not suspicious | not sufficient |
| defence aversion | defence evasion |
| cushion man | question mark (spoken punctuation) |
| still slow and slow | stealth-low-and-slow |
| GSP in | GSPN |
| finite same machine | finite state machine |
| Mitzis (tactics) | MITRE's (tactics) |
| the same good (verb) | the same verb |
| tool only | dwell-only |
| moving target offence | moving target defence |
| verbatone | verb it's on |
| White set / wait set | weight set |
| way to buy X amount | weighted by X amount |
| recurrent value | recurrence value |
| the taxes (distance) | the tactics |
| Sync Retrace | sink retrace |
| another quick | another quirk |
| 22nd (confusion penalty) | 20-second |
| defend a sportsy (attacker) | defender thwarts the (attacker) |
| attacker door | attacker dwell |
| cyber kill train | Cyber Kill Chain |
| encapture | capture |
| tackle (zero or one actions) | tactic |
| attack lines (precomputed) | attack timelines |
| the produce (of the movement layer) | the product |
| Tech Detective white set | tactic-to-tactic weight set |
| for the titan (ruling walk) | for the TIGHTEN |

### Danger minimal pairs — a mishear flips a claim, always verify-list these

- **tactic vs technique** — the resolution distinction the model turns on;
  check every instance against which level the sentence is about.
- **AND vs OR vs and/or** — join semantics in the graph.
- **NLP vs LLM** — distinct method families with distinct rulings.
- **weight vs wait**, **flows vs floors/flaws**, **dwell vs duel/do well**.
- Project names: GSPN / Petri / GAP / GASP / OGASP / MTDSim / HARM /
  Engenuity / CTID; people: Jin, Hong, Alshamrani, Rodríguez, Rahman,
  Büchel, Brown, Zhang, Ho, Tay.
- **Background speech (backchat).** Marc sometimes dictates with other
  people talking nearby; fragments that do not parse against the argument
  ("spend the money", "how does that react") are dropped and **listed in the
  change log as dropped backchat**, never repaired into text. Where a burst
  sits inside one of his sentences, repair the gap minimally and flag the
  seam as `[3b]` for him to confirm. Watch hardest for self-corrections that
  *look* like backchat ("No, not an issue, this is a feature") — keep those,
  resolved to the second form, and flag.
- **Drop disfluencies** ("um", "you know", "right", "yes so", false starts,
  self-corrections) — clean-verbatim. Keep rhetorical questions, emphasis,
  and spoken idiom: they are voice, not noise.
- **Add sentence punctuation following the spoken rhythm.** Never reorder
  clauses. Person: the standing global is **we** (first person plural; Marc,
  2026-08-20) — normalise dictated *I* to *we* in dissertation-bound prose and
  log each instance.
- **Honour spoken stage directions** ("insert paragraph", "insert reference
  here", "as per the prior amendment") as instructions, not text. Reference
  slots become citation placeholders or live keys if ratified keys exist.

## Step 2 — register sweep (pass 3a)

Four sweeps over the repaired text, in order:

1. **Pads — delete.** Marc's observed inventory (append as new ones appear):
   "you know", "right" (tag), "um(m)", "basically", "essentially", "sort of",
   "stuff" (flag if deletion breaks the sentence — replacement noun is
   Marc's), "just", "very, very" → "very", emphatic "did" ("did toss" →
   "tossed"), sentence-initial "So" / "And so" / "And yes" / "Yep OK so",
   "I would say", "what we did is", "OK", "Well" (sentence-initial), "the key with this is" (keep if
   load-bearing), doubled connectives ("So therefore" → keep one). Rule: if
   deleting leaves a grammatical sentence, delete and move on; else smallest
   word-level repair, logged.
2. **Run-ons — split at conjunctions only.** Clause order untouched; restored
   subjects limited to the sentence's own ("we", "this", "it" — capitalised,
   never invented).
3. **Meta-narration — behead** ("Now I'll talk about...") where the next
   sentence already works as the topic sentence; flag where it doesn't.
4. **Contractions — expand, mechanically.** Standing global ruling (Marc,
   2026-08-20, superseding the earlier preamble-scoped "contractions stay"):
   every contraction in dissertation-bound prose expands (*we're* → *we are*,
   *didn't* → *did not*, *they're* → *they are*). Not a 3b item; log the
   expansions in one bulk line. Possessive apostrophes (*the attacker's*) are
   not contractions — leave them.
5. **Hedges — flag, never resolve.** "I think", "we believe", "I guess",
   "a bit", "a certain X", vague scopes ("than usual", "across CTI") each get
   a marker: `% [3b] <quote> --- <the binary or scope question it poses>`.
   Each marker poses ONE decision — sure-or-scoped, name-it-or-soften-it,
   your-noun-here.

Allowed word-level repairs (each individually logged in the change log):
grammatical agreement ("there's lots" → "there are lots"), tense after a pad
deletion, one neutral conjunction to close a deletion gap. Nothing else.

## Step 3 — the return

- The repaired draft, written where Marc asked (the working `.tex` section, or
  chat) — his paragraphs, `[3b]` markers as comments at their sentences.
- **The verify watchlist**: every repair that changed a technical term or
  claim, quoted, for Marc to confirm — the highest-value part of the return.
- **The change log**: the word-level repairs, exhaustively.
- Word count vs the unit's ledger budget, stated once.
- The handoff line: "3b walk is yours (markers + global rulings + read-aloud);
  then `/scrutinise-draft` runs pass 4."

## What comes after (not this skill's job)

Pass 3b (Marc: hedge rulings, flagged recasts, read-aloud; the
contraction and person globals are ruled — expand, and *we* — and now run
mechanically in 3a) → pass 4 (`/scrutinise-draft` against the corpus pack) → pass 5
(Marc's compression to the ledger). The full pipeline — roles, sequencing,
gates — is the durable
[`docs/workflows/drafting_pipeline.md`](../../../docs/workflows/drafting_pipeline.md);
this skill is passes 2+3a of it, self-contained.
