---
status: open                  # standing context for ch2 dictation sessions; retire with the ch2 drafting programme
created: 2026-08-21
---

# How the lineage describes its own simulator — precedents and anti-patterns for dictating ch2

**The bar Marc set for this chapter:** describe MTDSim better than Brown 2023,
Zhang 2023, Ho 2024 and Tay 2024 each described it. All four performed (or
dodged) exactly the job ch2 §2.2 must do — Brown describing his own artefact,
the other three describing an inherited platform before their extension — so
their simulator-description passages are the direct precedent base. This file is
the scrutiny of those passages: per-paper verdicts first, then the affinity
board of every move worth keeping, keyed to the ratified skeleton, then the
anti-pattern board of every move to refuse.

**Companion to** [`2026-08-21_ch2_background_context.md`](2026-08-21_ch2_background_context.md),
which is authoritative on the chapter's shape, budget and boundaries — nothing
here changes that skeleton. This file feeds *craft and content* into the
dictation sessions: what each unit's precedent looks like, which paper does it
best, and what failure it must dodge. Mode note as ever: Marc dictates; sessions
scaffold and scrutinise, never draft.

**Locators** are `file.md:line` into the tracked conversions in
[`../sources/lit_review/`](../sources/lit_review/) (`brown2023.md`,
`zhang2023.md`, `ho2024.md`, `tay2024.md`), with the paper's own section number
alongside so the locator survives a re-conversion.

## The one standing warning, before any precedent is adopted

**These passages are the papers' accounts of their code, and ch2 describes the
code.** The audit found the two are not the same: Zhang's §4.4.3
(`zhang2023.md:384`) describes an adversary whose exploit times halve on
re-encountered vulnerabilities and whose phase-2 durations are drawn per
attempt — but the substrate implements **no attacker learning (ATK-04)** and a
**deterministic exploit time (C7)**
([`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md)).
A dictation session that lifts a lineage sentence lifts its claims with it. The
rule: **structure and framing may come from these precedents; every fact comes
from the implementation records** (the substrate primer, the intent spec's
audited IS-IDs, the boundary records). Where a lineage description and the
record diverge, the record wins and the divergence stays out of ch2 — it is
ch4's comparability material.

---

## Part 1 — per-paper scrutiny

### Brown 2023 — §III (`brown2023.md:49–135`): the artefact described by its builder

The only paper describing MTDSim from scratch for a reader who has never seen
it — the closest analogue to ch2's actual task.

**What works:**

- **The four-sentence frame** (§III opening, `:51`). One sentence each for the
  three modelled things and the artefact capturing it: system → 3-layer HARM;
  attacker → flowchart "inspired by the Cyber Kill Chain and MITRE ATT&CK";
  defence → shuffle and diversity techniques at different layers. Frameworks
  are *named as attribution*, never taught — exactly the "a background chapter
  may name a framework it does not teach" ruling, executed in 1988.
- **Layer-by-layer network description with the generative model named**
  (§III-A, `:53–75`). Each HARM layer gets: what it holds, how it is generated
  (Barabási–Albert for the topology, Watts–Strogatz for services), and a
  one-clause justification ("mimics the characteristics of real-world
  networks"). The clause-length justification is the right altitude for ch2 —
  it explains without arguing.
- **The per-mechanism template** (§III-B, `:77–99`). Six mechanisms, one
  paragraph each, identical shape: *name → what the real-world technique is,
  with one deployment citation → "MTDSim implements X by…" → what it interrupts
  for the attacker.* The template's consistency is what makes six mechanisms
  readable in a page.
- **Mechanisms re-grouped by disruption channel** (§III-D, `:117–129`). A
  second pass over the same roster, organised by *what the attacker loses*:
  connection-to-host lost (IP / topology shuffle), connection-to-service lost
  (diversity + port shuffle), user access changed. This is the lineage's own
  precedent for the position-versus-surface reading ch4 and ch5 use, and the
  single most re-usable move in the corpus.
- **Constants to a float** (Table I, `:131`). Every parameter in one table;
  prose never enumerates them. Plus honest footnotes where a value is arbitrary
  (the 50 % cross-compatibility note) — the concession is a footnote, not a
  paragraph.

**What fails:** the attack procedure (§III-C-2, `:111–113`) is a single
run-on prose narration of the flowchart, unreadable without Figure 3 — the
negative print of the per-mechanism template's discipline. And the roster
carries no classification at all: no SDR labels, no trigger vocabulary, so the
six mechanisms arrive as a flat list a reader cannot organise. Marc's §2.1 →
§2.2.2 wiring is precisely the repair.

### Zhang 2023 — §2 + §4 (`zhang2023.md:134–415`): the fullest description, and the most padded

The thesis-length treatment: a background chapter of taxonomy, then a
methodology chapter describing the (partly inherited) framework.

**What works:**

- **The three-module overview** (§4.1, `:262`). One paragraph, one figure:
  Simulated Network / MTD Techniques / Adversary, each defined by its
  *interaction* with the others (the MTD operation writes the network; the
  adversary executes attack actions on it). The interaction-first definition is
  what makes the paragraph load-bearing rather than a table of contents.
- **Inheritance stated in one clause with a citation.** "We adopt the widely
  utilized 3-layer HARM model [17]" (`:270`); "In the previous work [17], seven
  MTD techniques were implemented. For this study, we selected four…" (`:292`);
  and the honest cut — "only the first attack scenario is selected to be
  refactored" (`:364`). Inherited-versus-changed is settled in a sentence each
  time, never a section. This is the clause-level attribution discipline the
  chapter README ratifies (*the execution schemes Zhang added*), demonstrated.
- **The adversary as four named capabilities** (§4.4.1, `:362–370`):
  objectives, vulnerability exploitation, command-and-control, credential use —
  each with its assumption stated in place ("compromised hosts will always stay
  compromised… regardless of any network changes"). Naming the assumptions
  inside the description is what lets a later chapter cite them without
  re-deriving them; Brown has no equivalent decomposition.
- **One worked example carrying an abstract rule** (§4.3.3, `:346`): the
  resource-occupancy rule is stated once, then run through a concrete
  three-mechanism, two-layer example. Cheaper and clearer than the two
  paragraphs of machinery before it.
- **Trigger semantics get their own unit** (§4.3.2, `:313–337`): the execution
  schemes are introduced by what distinguishes them (the register and trigger
  actions), with a per-scheme paragraph and one timeline visualisation. The
  content of §2.2.2's scheme sentences comes from here — compressed hard.

**What fails:** the padding is systemic — every section opens with a
signpost paragraph ("This section aims to provide a comprehensive
description…") and closes on filler ("providing valuable insights into the
application"); none of it survives contact with the register sweep. The
background chapter over-teaches: the full seven-step kill chain and ATT&CK's
three matrices (`:172–200`) are taught in ~500 words and then consumed by a
single clause ("follows the action flow of the Cyber Kill Chain", `:372`) — the
vocabulary-never-cashed anti-pattern, and the direct cautionary tale for §2.1.
And the taxonomy is barely worn later: the roster is labelled once ("two
shuffle-based… two diversity-based", `:292`) and the trigger vocabulary of
§2.1.2 never reappears at the schemes it describes.

### Ho 2024 — §3.1 (`ho2024.md:234–242`) + appendix (`:677–703`): the cautionary tale

The inherited platform compressed to five sentences, and the cost on display.

- **The whole simulator description** is §3.1.1 (`:242`): HARM named with its
  three graphs, then straight to a limitation framing — "Currently, the
  simulator can only deploy four MTD techniques either randomly, alternatively,
  or simultaneously against limited attacker types" — and the adversary in one
  sentence ("built using the Cyber Kill Chain and MITRE ATT&CK… to compromise
  as many hosts as possible"). A reader who has not read Zhang cannot follow
  the experiments from this; the document outsources its own background. This
  is what under-funding §2.2 buys.
- **Description by limitation** is the register failure worth naming: "can
  only deploy… against limited attacker types" is gap talk doing description's
  job. Ch2's rule — describe and hand over; where a component is later argued
  about, say what it is and stop — is the repair.
- **The taxonomy exiled to an appendix** (`:677–703`): the opposite pole from
  Zhang's front-loading. The main text wears shuffle/diversity labels it never
  defines; the definitions sit where no reading order visits them. Between
  Zhang (taught, never used) and Ho (used, never taught), Marc's §2.1-then-worn-
  in-§2.2.2 wiring is the only version that closes the loop.
- **One genuinely good move:** the built-versus-inherited split as the *first*
  cut of the system (§3.1, `:238` — "the system consists of the AI engine and
  the MTD simulator… used as the infrastructure"), one figure, before any
  detail. Tay does the same move better (below), but the instinct — separate
  what is yours from what you stand on before describing either — is the right
  opening instinct for §2.2's preamble and Table 2.1.

### Tay 2024 — §2 (`tay2024.md:134–156`) + §4 opening (`:202–210`): the best inherited-vs-built move, over a hollow platform

- **The green/orange paragraph pair** (`:206–208`) is the strongest single
  precedent in the corpus for §2.2's preamble. First paragraph: "The existing
  simulator framework… consists of three main components: the Network Module,
  MTD module and Attacker module [23]", each defined in one functional sentence
  (the network sentence packs topology *and* the five host attributes into one
  clause: "IP addresses, operating systems, services, vulnerabilities, and user
  access credentials"). Second paragraph: what the framework *is* ("time-based,
  deploying MTD… on a fixed schedule") and what the new work adds, with the
  figure colour-coding inherited green and built orange. Two paragraphs, one
  figure, and the seam is legible. Ch2 + Table 2.1 is the same move with the
  colour-coding done by a table column instead.
- **The vocabulary as three design questions** (§2, `:136–156`): what/how/when
  taught as the questions an MTD designer must answer, in ~350 words —
  the leanest of the corpus's three taxonomy treatments and the closest to
  §2.1's 250-word budget. Two register faults to strip on the way: it ends on a
  motivating hook for Tay's own contribution ("An optimal MTD interval,
  therefore, needs to be dynamically determined during runtime", `:156`) — gap
  talk closing a background section — and it never names redundancy's absence
  from the platform, which Marc's §2.2.2 scope note does honestly.
- **The platform behind the seam is hollow.** The attacker module never gets
  more than the §4 sentence — no phases, no scenarios, no exploit ordering
  anywhere in the document (the detection-rate machinery of §5.3 treats the
  attacker as a signal source, not a model). The review's asymmetry line —
  "the adversary against which it is evaluated is inherited, not modelled" — is
  visible in the document's own page allocation. Ch2's §2.2.3 exists so this
  thesis's document does not repeat that shape.
- **Metric prose padded with security-blog filler** (§4.1.1–4.1.2,
  `:228–250`): each metric's definition is followed by generic operational
  advice ("necessitating urgent actions such as patch management, system
  hardening, and user education") that no simulator computes or needs. The
  metrics ruling already keeps this material out of ch2; the precedent is why.

---

## Part 2 — the affinity board, keyed to the ratified skeleton

Each cluster: the move, its best exemplar, and where it lands in Marc's shape.

**Chapter opener (~60 w) + §2.2 preamble (~120 w)**

1. **Frame by the three modelled things and their interactions** — Brown's
   four-sentence §III opening for the *what each artefact captures* shape;
   Zhang's §4.1 for interaction-first module definitions; Tay's `:206` for the
   most compressed execution. The opener and preamble should read as: what the
   simulator is (discrete-event, three-layer HARM), then the three modules each
   defined by what they do to the others.
2. **Separate inherited from built before describing either** — Tay's
   green/orange pair, Ho's infrastructure/engine cut. In Marc's shape the seam
   is carried by Table 2.1's third column (*what this thesis inherits*), which
   does with a column what Tay does with colour.
3. **Attribution rides as a cited clause, never a section** — Zhang's three
   inheritance clauses (`:270`, `:292`, `:364`) are the template for the
   preamble's two lineage sentences and for every *the execution schemes Zhang
   added* clause downstream.

**§2.1 Moving target defence (250 w)**

4. **Teach the vocabulary as design questions, not taxonomy** — Tay's §2 is
   the length and framing precedent; strip the closing hook. Zhang's §2.1 shows
   the over-taught version (bullet lists per category, a table of movable
   elements); the corpus's lesson is that ~350 words was enough even before
   compression, so 250 is feasible.
5. **Every term taught must be cashed later** — the corpus proves both failure
   modes (Zhang teaches-never-uses; Ho uses-never-teaches). The chapter
   README's rule — §2.1's vocabulary earns its keep in §2.2.2's first two
   sentences — is what neither managed.

**§2.2.1 Network model (250 w)**

6. **Layer-by-layer, generative model named, one-clause justification** —
   Brown §III-A is the only real precedent (Zhang §4.2 re-describes it with
   formal symbols; Ho and Tay skip it). Order top-down (hosts → services →
   vulnerabilities), name Barabási–Albert and Watts–Strogatz, justify each in a
   clause. Facts from the substrate primer, not Brown's numbers.
7. **Pack host attributes into one sentence** — Tay's five-attribute clause
   (`:206`) shows the whole host model fitting in a line; Zhang's §4.2.2 shows
   the same content as a paragraph. At 250 words, the clause wins wherever ch4
   and ch5 do not lean on the detail.
8. **Constants to a float, arbitrariness to a footnote** — Brown's Table I and
   his arbitrary-value footnotes. Ch2 likely needs no parameter table (that is
   ch4's experimental setup), but the discipline — prose never enumerates
   constants — holds.

**§2.2.2 Defence mechanisms (~300 w)**

9. **The per-mechanism template, worn labels first** — Brown's *real-world
   grounding → implemented-as → what it interrupts* template, upgraded by
   opening each entry with its §2.1 class (the move the whole corpus missed).
   At four mechanisms and ~300 words the template compresses to a sentence or
   two each; the *what it interrupts* clause is the one to keep when cutting.
10. **Group by disruption channel** — Brown §III-D. The position-versus-surface
    organisation (which layer of terrain the operation mutates) is both the
    lineage's own precedent and the reading ch4/ch5 use; letting it organise
    the roster's presentation does §2.1-cashing and forward-wiring in one move.
    Facts from the boundary records
    ([`../implementation/mtd_write_surfaces.md`](../implementation/mtd_write_surfaces.md)),
    which are stronger than any lineage account of the same seam.
11. **Schemes by their distinguishing action, one clause each** — Zhang §4.3.2
    compressed: what varies between random / alternating / simultaneous is the
    register-and-trigger choice; the queue machinery and suspension detail stay
    in the implementation records. Zhang's worked-example move (`:346`) is the
    fallback if one abstract sentence will not carry the resource rule — but at
    this budget the example is a luxury.
12. **The reactive selector [→ MTDShield, classified hybrid; ruled 2026-09-02] in the Tay-paragraph shape** — the review's §II-C ¶3
    port (already flagged in the companion brief as the cleanest direct port):
    the DDQN, the five actions, no-op as learned restraint. Tay's own §4.1
    architecture detail (LSTM stacks, layer widths) stays out — that is the
    selector's manual, not its description.

**§2.2.3 Attacker model (250 w)**

13. **Named capabilities with assumptions stated in place** — Zhang §4.4.1's
    four-feature decomposition is the structural precedent: objectives,
    exploitation, command-and-control, credentials, each with its standing
    assumption (persistence of compromise) said where the capability is
    defined. This is the unit's skeleton; the six-phase procedure then needs
    only a compact narration.
14. **Phases as a named sequence, not a prose flowchart** — Brown's §III-C-2
    run-on is the anti-precedent; Zhang's §4.4.2 phase naming (scan → three
    compromise phases → scan-neighbour) is the readable version. If the
    narration wants a figure, the answer is no (ratified: ch2 has none) — so
    the sentence structure must do the flowchart's work: one sentence per
    phase, transitions as clause openers.
15. **Both scenarios, named cheaply** — Brown §III-C-1 describes general and
    targeted in a bullet each; Zhang then cut targeted with one honest
    sentence. Ch2 describes what the substrate carries (facts from the
    records, per the standing warning), with kill chain and ATT&CK named as
    attribution exactly as Brown's frame sentence does — named, not taught.

---

## Part 3 — the anti-pattern board

What the corpus proves not to do. Most have a named repair above; listed here
so a dictation session can sweep a draft unit against them directly.

1. **Vocabulary taught but never cashed** (Zhang) / **used but never taught**
   (Ho). The repair is the README's earn-its-keep rule.
2. **Description by limitation** (Ho's "can only deploy…"; Tay's §2.3 closing
   hook). Gap talk in a background register — ch2 describes and stops.
3. **Signpost-and-filler padding** (Zhang systemically: "comprehensive",
   "crucial", "valuable insights"). The register sweep exists for this; the
   precedent shows how much of a lineage sentence survives — often under half.
4. **Frameworks over-taught** (Zhang's seven CKC steps + three ATT&CK
   matrices for one clause of use). Brown's name-as-attribution frame is the
   whole treatment ch2 needs.
5. **The prose flowchart** (Brown §III-C-2). One phase per sentence, or it is
   unreadable without a figure the chapter does not have.
6. **The under-described attacker** (Ho's one sentence; Tay's zero model
   content). The corpus's own page allocation is the review's asymmetry
   argument made visible — §2.2.3 is where this thesis breaks the pattern.
7. **Metric definitions padded into operational advice** (Tay §4.1.1–4.1.2).
   Already excluded by the metrics-to-ch4 ruling; the precedent is the reason.
8. **Describing the papers' intent as the code's behaviour** (Zhang §4.4.3 vs
   ATK-04/C7). The standing warning above; the one failure mode with
   correctness stakes rather than craft stakes.

## Part 4 — where ch2 clears the corpus's bar

The moves no lineage paper makes, already ratified in Marc's shape — the
checklist for claiming the chapter has done its job:

- **The lineage as a lineage.** Each paper cites only its parent; none shows
  the four-work evolution or separates inherited from built across it. Table
  2.1's three columns do both — no precedent exists, which is the point.
- **A classification actually worn by the roster.** §2.1's labels opening each
  §2.2.2 entry closes the loop all four left open.
- **The honest scope note** — shuffle and diversity only, no redundancy
  ([`../implementation/substrate_primer.md`](../implementation/substrate_primer.md)
  §(c)). Tay teaches redundancy and never says the platform lacks it.
- **The disruption-channel reading grounded in verified records**, not paper
  claims — Brown invented the framing; ch2 is the first document able to state
  it against a measured write-surface census.
- **An attacker described in proportion to its load-bearing role** — the unit
  the corpus starves is the one this thesis's evaluation turns on.
- **Facts from the artefact, not its folklore** — every behavioural claim
  traceable to an implementation record, with the paper-code divergences left
  to ch4 where they are arguments.

## Reading list for a dictation session

1. [`2026-08-21_ch2_background_context.md`](2026-08-21_ch2_background_context.md) — the shape, budget, boundaries (authoritative).
2. [`../notes/ch2_background/README.md`](../notes/ch2_background/README.md) — the two placement tests and the ratified skeleton.
3. This file — precedents per unit, anti-patterns per sweep.
4. [`../implementation/substrate_primer.md`](../implementation/substrate_primer.md) + [`../implementation/metrics_semantics.md`](../implementation/metrics_semantics.md) — the facts, and the divergences to keep out.
5. The four source passages, only as needed per unit: `brown2023.md:49–135`, `zhang2023.md:260–415`, `tay2024.md:202–210`, `ho2024.md:234–242`.

**Retire** when the ch2 units are drafted and scrutinised — same trigger as the
companion brief.
