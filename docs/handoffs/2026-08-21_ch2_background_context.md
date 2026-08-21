---
status: open                  # standing context for the ch2 workshop + drafting passes; retire when the chapter is drafted and scrutinised
created: 2026-08-21
---

# Standing context for workshopping the background chapter (ch2) — what the chapter is, and exactly what the submitted literature review can supply it

> **Mode note, first.** Marc drafts the prose; sessions scaffold and scrutinise
> ([`../workflows/draft_scrutiny.md`](../workflows/draft_scrutiny.md)). A session
> that returns finished background paragraphs has failed the mode. Every unit
> travels [`../workflows/drafting_pipeline.md`](../workflows/drafting_pipeline.md).

Companion to the two ch3 briefs of the same date —
[`2026-08-21_ch3_lit_review_design.md`](2026-08-21_ch3_lit_review_design.md) (the
literature review's structure) and
[`2026-08-21_lit_review_scrutiny.md`](2026-08-21_lit_review_scrutiny.md) (the
verdicts on the source material). This file carries the **ch2 half of the same
split**: the passages of the 22 May 2026 review that belong to the background
chapter rather than the literature review, located precisely, plus an honest account
of how much of ch2 the review does *not* supply.

## What the chapter is, in one line

**The inherited platform, described so a reader can follow the rest of the
document** — the simulator's lineage, its network model, its defence mechanisms and
its baseline attacker. Existing things, presented for comprehension. The arguments
*about* those components (the comparability boundary, the baseline's fairness, the
scoring of its threat model) are ch3's and ch4's; ch2 describes and hands over.

## Budget and skeleton

**1 250 words / 5 units** (writing guide ledger; ch2 was cut 6→5 on 2026-08-12 to
fund the methodology's 11-unit skeleton). The four sections in
[`../thesis/dissertation.tex`](../thesis/dissertation.tex) plus a short opener is
already the full five, so **there is no spare section**: any new heading has to name
what it displaces.

| Unit | Section | Job |
|---|---|---|
| opener | — (rides §2.1) | what the simulator is, in two or three sentences |
| 1 | Prior work | Brown → Zhang → Ho → Tay, what each added |
| 2 | Network model | topology, host/service structure, exposure |
| 3 | Defence mechanisms | the mechanism family, the execution schemes, the reactive learner |
| 4 | Attacker model | the scripted six-phase attacker and the inherited metric suite |

One standing discipline against ch2's failure mode, which is bloat: **nothing enters
this chapter that a later chapter does not lean on.** If ch4 and ch5 never refer back
to it, it is not background, it is a manual.

---

## The port map — what the review supplies, by ch2 section

Locators are section references into the submitted review plus line numbers in the
tracked markdown, [`../sources/lit_review/LIT_REVIEW.md`](../sources/lit_review/LIT_REVIEW.md).
**Nothing here ports one-to-one** — every passage was written to argue toward the
review's gap and has to be re-aimed at description. Word counts are of the source
passage, not of what should survive.

### §2.1 Prior work — **half supplied**

- **Brown / MTDSim / HARM** — §II-B ¶5, `LIT_REVIEW.md:61` (~90 w). Carries the
  discrete-event-simulator-on-three-layer-HARM description and the combined-MTD
  contribution. The paragraph's last sentence is a forward pointer into the review's
  §IV and does not travel.
- **Tay** — §II-C ¶3, `LIT_REVIEW.md:87` (~110 w) and §IV-B-2, `LIT_REVIEW.md:183`
  (~170 w). Between them: the DDQN orchestrator, what it replaced (Brown's
  fixed-interval scheduler), and that the attacker module is inherited unchanged.
- **Zhang 2023 and Ho 2024 are absent from the review entirely.** Neither is cited;
  neither has prose. This is the single biggest hole in the port — **half the
  lineage this chapter exists to narrate has no source text**. It comes from the
  extractions (`zhang2023`, `ho2024`) and the implementation records, not from here.

*Register warning:* the review introduces Brown and Tay in order to score them later.
Ch2 describes them as the platform. The evaluative clauses ("its principal
contribution is enabling…", "the contribution is defender-side") are fine; the
fidelity verdicts are not — those belong to ch3.

### §2.2 Network model — **essentially unsupplied**

The review contains one clause of relevance: "a discrete-event simulator built on a
three-layer Hierarchical Attack Representation Model (HARM)" (`LIT_REVIEW.md:61`),
plus "agnostic to specific network configurations" in §V-A (`LIT_REVIEW.md:225`).
There is no description anywhere of the topology, the host and service structure, or
the exposure model — the review never needed one.

**This unit is written from scratch**, against the implementation records
(`substrate_primer`, and the network/topology material in the pipeline records) and
against Brown 2023 directly. Budget accordingly: it is a full unit of new prose, not
a port.

### §2.3 Defence mechanisms — **partially supplied, and this is the best of it**

- **The vocabulary** — §II-A, `LIT_REVIEW.md:43` (attack surface), `:45`
  (what / how / when), `:47` (shuffling / diversity / redundancy), `:49`
  (proactive / reactive / hybrid). ~330 w of source.
  **Compress hard.** The ruling that governs this port: SDR and the what/when/how
  questions enter ch2 as *labels applied to the inherited mechanisms*, cited to Cho,
  not as a taxonomy discussed for its own sake — the field's conventions expect each
  mechanism to arrive with its class and its trigger semantics, and that expectation
  is the whole reason the vocabulary is here rather than in ch3. Perhaps eighty words
  survive. **Fig. 1 (the SDR relationship diagram) does not travel** — it illustrates
  a taxonomy discussion the dissertation is no longer having.
- **The mechanism set** — the only place the review enumerates MTDSim's actual
  operations is inside Tay's action list at `LIT_REVIEW.md:87`: IP shuffle, OS
  diversity, service diversity, complete topology shuffle, no-op. Useful as a
  checklist; it is not a description of the mechanisms.
- **The reactive learner** — §II-C ¶3, `LIT_REVIEW.md:87`. **The cleanest direct
  port in the whole review.** The DDQN, the five actions, and the observation that
  the no-op encodes restraint as a policy choice rather than a global interval
  parameter — all of it is ch2 material as written, needing register work rather
  than re-argument.
- **Execution schemes are absent.** That is Zhang's contribution and the review never
  covers it; it comes from the extraction and the implementation records.

### §2.4 Attacker model — **partially supplied**

- **The scripted attacker** — §IV-B-1, `LIT_REVIEW.md:181` (~150 w). Carries the two
  scenarios (general = network-wide compromise, targeted = specific-host), the
  finite-state machine "inspired by the Cyber Kill Chain and MITRE ATT&CK", and the
  RoA priority ordering over scanned exploits derived from CVSS.
  **Take the description; leave the verdict.** The passage ends by placing Brown at
  parametric fidelity and quoting the skill-homogeneity concession — both are ch3's
  cross-section, and repeating them here spends the argument twice.
- **The inherited metric suite is not supplied.** MTTC appears in the review only as
  a cell in Cho's field-level metric table (Table I, `LIT_REVIEW.md:68`), which is
  ch3 §3.3.2 material, not a description of what MTDSim computes. The internal
  definition and its divergences live in `metrics_semantics`.

---

## The coverage verdict, stated plainly

Roughly **450 words** of the review's 6 002 are ch2 material, expanding to a
1 250-word chapter. Three of the five units — the network model, half the lineage,
and the inherited metric suite — **have no source prose at all**.

The practical consequence for the workshop: do not open this chapter expecting a
quarry. The review supplies the *defence side* of ch2 reasonably well and almost
nothing else, because the defence side was the only part it needed. The rest is
written against the implementation records and the primary papers. (Those records
are named here as signposts from the docs index, not vouched for — this session was
run grey-box on Marc's instruction and did not read them.)

## Boundaries

- **Descriptive register throughout.** Ch2 states what the inherited components are
  and do. Where a component is later argued about, ch2 says what it is and stops.
- **Describe once.** Brown's attacker and Tay's agent are described *here* and
  referred back to from ch3's cross-section — not re-described there. This is the
  main double-writing risk in the port, because both currently live inside the
  review's scored entries.
- **No ATT&CK section.** ATT&CK is not needed to describe MTDSim, and ch2 has no
  spare unit; it is introduced in ch3 §3.1.2 where it does argumentative work. A
  framework earns a place in background only when the background cannot be written
  without it — SDR clears that bar, ATT&CK does not.
- **No lineage headlines.** Zhang's shuffle-dominant and Ho's diversity-dominant
  results are comparison points for the evaluation, per the skeleton comment in the
  tex, and do not appear in §2.1.
- **No gap talk.** The asymmetry line at `LIT_REVIEW.md:89` ("the adversary against
  which it is evaluated is inherited, not modelled") is the review's best sentence
  and it is *not* ch2's — it belongs to ch1 or the ch3 preamble, and only once.

## Open questions for the workshop

1. **Does §2.1 Prior work carry the lineage, or does §2.1 carry Brown and the other
   three ride their own sections?** Four papers in one 250-word unit is tight, and
   Zhang and Ho have no source prose to compress from.
2. **How much network model does the dissertation actually need?** The unit is
   written from scratch, so its scope is set by what ch4 and ch5 refer back to —
   worth deciding against the methodology skeleton before drafting, not after.
3. **Where does the inherited metric suite land — §2.4 or ch4's experimental
   setup?** The tex comment puts the description here and the comparability argument
   in ch4; confirm the split holds once the metrics' divergences are on the page.
4. **Does the opener need the pipeline figure**, or is that ch4's alone? The
   methodology brief has a live ladder figure at its chapter opening.

## Out of scope (explicitly)

Drafting ch2 prose; editing `dissertation.tex`; reading or reconciling the
implementation records named above; the ch3 briefs' open CONFIRMs.
