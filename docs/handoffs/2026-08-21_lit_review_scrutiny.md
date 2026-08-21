---
status: open                  # scrutiny record for the ch3 boil-down; retire when ch3 is drafted
created: 2026-08-21
---

# Scrutiny of the submitted literature review — what survives the boil-down into ch3, what has to be re-argued, and why the gap section reads weak

Companion to [`2026-08-21_ch3_lit_review_design.md`](2026-08-21_ch3_lit_review_design.md),
which sets the chapter's structure. This file judges the **source material**: the
22 May 2026 CITS4010 review (6 002 words of body prose), read under
[`../workflows/critique_protocol.md`](../workflows/critique_protocol.md) — section
verdicts, then paragraph and sentence findings, closing on three moves. Content
findings stop at naming the gap; no prose is drafted, per §(b) T3.

Marc's three priors going in: some content is no longer relevant (Pyramid of Pain
named); §IV (the gap) is weakly drafted and hard to follow; §II (MTD) and §III-D
(attack profiling) are strong. **Two of the three hold. The third — §II being
strong — is true as prose and misleading as a reuse estimate.**

---

## Section verdicts

| Section | Verdict | One line |
|---|---|---|
| §I Introduction | **rework** | Frame is built on the pyramid; falls with it |
| §II-A Concept and taxonomy | **relocate** (ch2) | Good prose, wrong chapter now |
| §II-B Evaluation paradigms | **keep** (split) | The ladder and Table I are ch3's; the MTDSim paragraph is ch2's |
| §II-C Orchestration | **cut to one sentence** | Payload is the asymmetry; the rest is double-counted |
| §III-A MITRE ATT&CK | **keep** | Best passage in the review |
| §III-B Pyramid of Pain | **rework** | Durability argument survives; the metaphor does not |
| §III-C Advanced persistent threats | **tighten + missing** | Single-source, and the "latest" slot is empty |
| §III-D Attack profiling | **keep** | The internal exemplar — measure everything else against it |
| §IV-A Surveys naming the gap | **cut to two sentences** | A subsection functioning as a runway |
| §IV-B Cross-section | **rework** | Right evidence, unearned instrument, buried headline |
| §V Gap and approach | **rework** | Repeats a conclusion already made twice, then introduces new evidence |

---

## (a) The Pyramid of Pain — right instinct, stronger reason

Cut it, but not because it is "no longer relevant". It is doing two jobs and only
one of them is sound.

**The sound job (keep the argument, probably drop the citation).** §III-B's
durability point — behavioural patterns persist as long as the adversary's
operational habits do, whereas an IP address decays within a day — is load-bearing.
It is what licenses modelling the adversary at technique-and-tactic level at all,
and the chapter design needs it at 3.1.2. But Sadlek et al. carry that claim in
peer-reviewed form, and the review already quotes them for it. Bianco is a blog
post carrying an abstract-level claim; the argument survives his removal intact.

**The unsound job (this is the cut).** The review's organising metaphor — MTD
locating its value "at the apex", attacker models sitting "near the base" — appears
in the abstract, the introduction, §III-B, §IV-A, §IV-B and §V ("Pyramid of Pain"
×10, "apex" ×8). Two defects, both of which an examiner who knows Bianco will reach
for:

1. **The direction is contestable and uncited.** The pyramid ranks indicator classes
   by the cost to the adversary *when a defender denies that class to them*. What
   MTD denies an attacker is knowledge of addresses, ports, versions and topology —
   base and middle rungs. Forcing an adversary to re-scan makes them re-run a
   technique, not learn a new one. "MTD locates its defensive value at the apex" is
   the review's own synthesis, attributed to no MTD paper, and on Bianco's own terms
   it may be inverted. *Flagged to verify, not asserted wrong* — but it is the
   abstract's first sentence, so it needs to be right.
2. **Two incommensurable scales are welded together.** The attacker-model half of
   the metaphor maps *model fidelity* onto a ranking of *indicator classes*. A fixed
   success probability is not a hash value; "scripted sequences" are not a rung of
   Bianco's pyramid. The review then builds the correct instrument — the four-rung
   ladder — and keeps bolting it back on: "a fidelity scale anchored to this rung",
   and in the abstract "the procedural or behavioural rungs at which MTD claims to
   operate". No MTD paper claims to operate at a rung of a ladder constructed in
   this review.

**Consequence to plan for:** this is a re-argument, not a trim. The abstract and the
introduction are built on the frame, and Fig. 3 goes with it. What replaces it is
already in the document — see (b).

## (b) Why §IV reads weak — four mechanisms, and one buried asset

Marc's read is right. The diagnosis matters more than the verdict, because three of
the four causes are structural and survive any amount of line-editing.

1. **It leads with authority and buries evidence.** §IV-A spends two paragraphs
   establishing that two surveys named the problem, then concedes that both "stop at
   diagnosis". A subsection whose function is to justify the next subsection is a
   runway. Booth's warrant test: the claim is carried by *who said it*, when the
   review holds evidence that carries it directly.
2. **The instrument is asserted, not earned.** "The first is drawn from Cho et al.
   [2]; the second is constructed here." The four-rung ladder —
   parametric / scripted / procedural / behavioural — is the most original thing in
   the review, and it arrives in half a sentence with no argument for why those
   rungs, why that order, or where the boundaries fall. Every placement in Table II
   then depends on it. Contrast §III-D, which spends a full page earning a
   two-option trade. **That asymmetry is the actual answer to "why is this section
   weaker": it carries the most original content on the least support.**
3. **Table II does not discriminate.** Twenty characteristic cells; eighteen are ✗
   (two of those ✗*). A table that is ninety per cent one value asserts rather than
   measures, and reads as a stacked deck. The only column that separates the papers
   is *Fidelity-level*. Worse, the single row carrying ticks — He et al. — is the row
   the prose itself rules out of population: "the attack class is detection-evasion
   of an ML classifier … not the APT-style network compromise the ladder is built
   around". The least comparable row is the most influential one.
4. **The conclusion arrives three times.** §IV-A ¶1, §IV-B-6, and §V ¶1 all state
   that attacker models cluster low. Roughly a page and a half in which no new
   information reaches the reader. That is the source of "hard to follow" — not
   confusion, *stall*. Reader-expectation terms: three consecutive units whose stress
   position holds the same proposition.

**The buried asset.** The strongest, most falsifiable, most memorable observation in
the review is the **rhetoric-versus-execution gap**: works invoke ATT&CK and the
kill chain as framing while their executed threat model carries none of it. Masud et
al. are "modeled after techniques in the cyber kill chain and MITRE ATT&CK" and run
a CVE-graph enumeration; Kim et al.'s multi-phase framework is, in execution, "a
sequential script across collapsed phases", which the authors themselves concede.
This is currently a half-sentence at the head of §IV-B and a pattern the reader must
assemble from five per-paper subsections. It is the claim an examiner will remember,
and it should be the section's spine rather than its residue.

## (c) The load-bearing claim carries selection exposure

Five papers, hand-picked, no stated inclusion criterion, no venue or date frame, no
search protocol — supporting a claim about what "the field" does. The stated
rationale ("spans the project's lineage, recent IoT-cloud orchestration,
state-of-the-art ML NIDS, a recent CKC-aware framework") argues *variety*, not
representativeness.

The fix is not a bigger sample; at 3 000 words there is no room for one. It is to
change the logical form of the claim. The set is already close to an **adverse
sample** — recent, well-regarded, and in several cases explicitly ATT&CK-framed, so
these are the works *most likely* to model an attacker well. An argument that says
so ("even among the works whose framing most invites it, none reach procedural") is
an existence argument over a favourable sample, and is far harder to attack than a
generalisation from n=5. The evidence does not change; the warrant does.

Related: **He et al. should leave the table.** By the review's own concession the
attack class does not transfer. As a prose contrast case — the one work that
formalises a defence-aware attacker, from an adjacent problem — it is valuable. As a
row in a table making a population claim, it contaminates the sample and supplies the
only ticks.

## (d) The review's gap is not the notes' gap — and that is now a decision

Three gap framings are live, and ch3 can close on only one:

| Framing | Where it lives | Evidence status |
|---|---|---|
| **Fidelity** — attacker models cluster at parametric/scripted | this review, §IV–§V | evidenced (the ladder + cross-section), externally marked |
| **Phase coverage** — surface-shifting under-defends the post-foothold campaign | `ch3_lit_review/post_ingress_mtd_gap.md` | asserted; the note itself flags three unreconciled citation anchors |
| **Evaluation altitude** — post-foothold performance is unasked | proposed in the design brief, 2026-08-21 | asserted |

The measurement that settles this: in 6 002 words the review contains
**"post-ingress" ×0, "dwell" ×1, "lateral" ×1**. The phase-coverage argument is
simply not in the submitted document — it was developed later, in the notes, and has
never been evidenced against the literature.

**Recommendation — this revises CONFIRM 2 of the design brief.** Make **fidelity the
spine** and derive coverage as its *consequence* rather than racing it: a threat
model that never leaves the scripted rung cannot represent a campaign that operates
past initial access, so MTD's performance against a footholded adversary is
unmeasured *because of* the fidelity ceiling. That keeps the one gap framing this
project has evidence and an external mark for, subordinates the two asserted
framings to it instead of substituting for them, and still delivers the post-foothold
motivation the introduction wants — as an implication, not a claim needing its own
survey. The design brief proposed the evaluation-altitude framing as the spine; on
this evidence that was the wrong call, and the sequence fidelity → coverage is
stronger than either alone.

## (e) What is genuinely strong, and why it is worth naming precisely

**§III-D is the internal exemplar.** It is the only section that runs the full chain:
names two strands, gives each its genuine strength, prices them against each other on
a single declared axis (coverage against fidelity), brings an external number to
adjudicate (the SoK's plateau near F1 = 0.70), and *converts the result into a
methodological commitment* — curated CTI. That is `voice.md` §c-3 executed without
prompting. Every other section in the review should be measured against this one, and
§IV-B in particular is what §III-D would look like with its warrant removed.

**§III-A is the best writing in the document.** The move from the ATT&CK-in-STIX
export recording "*which* techniques an adversary used without recording *how* they
fit together" to Attack Flow supplying exactly that structure is the cleanest single
argumentative step in the review. Fig. 2 (the Tesla incident) is the concrete worked
example that `voice.md` §c-8 demands and that the marker's feedback said was missing
— it earns its place and should carry into the dissertation. *Placement question:*
it illustrates the capture apparatus, so it can serve either ch3 §3.1.3 or ch4's
capture section; it should not appear twice.

**§II is strong prose and a weak reuse estimate.** Marc rates it strong and it reads
well, but most of it is no longer ch3's:

- §II-A (SDR, what/when/how, proactive/reactive/hybrid) → **ch2**, where the
  inherited mechanisms arrive and the field's conventions expect each to carry its
  taxonomy class.
- §II-B's MTDSim/HARM paragraph → **ch2**, explicitly: it describes the inherited
  platform.
- §II-C → its unique payload is the asymmetry sentence. Masud reappears in the
  cross-section; Tay is ch2 lineage. The rest is already counted elsewhere.
- Surviving into ch3: the four-way validation ladder and Table I. Those are 3.3.1
  and 3.3.2 and they are worth their space.

Of §II's ~1 400 words, roughly 350 are ch3 material. **This is the real reason the
boil-down is a rewrite rather than an edit**: the headline arithmetic (6 002 → 3 000)
understates it, because a further ~1 100 words of the source belong to ch2 before any
compression starts.

## (f) Citation practice — three failures against the field conventions

Measured against [`../workflows/literature_conventions.md`](../workflows/literature_conventions.md)
§(f), "cite a concept to its origin, not to whichever survey mentioned it":

1. **The Cyber Kill Chain is used five times and never cited.** It is the spine of
   Brown's FSM and Kim's framework, and it anchors the phase vocabulary. Hutchins
   appears nowhere in the reference list, though the extraction exists in the repo.
2. **NIST's characterisation of an APT is cited to Alshamrani [8]**, not to NIST.
3. **§III-C rests almost entirely on [8] (2019)** for the whole APT characterisation
   — a single-source dependency on the section that motivates the thesis, in a review
   whose own selection rule prizes currency. Volt Typhoon is named and not cited. The
   *latest* slot of the first / most-established / latest rule is **empty for the APT
   strand** — the one strand where the field has moved most since 2019. This is a
   **missing** verdict, not a tighten.

## (g) Terminology sprawl

Five phase vocabularies co-exist: the Lockheed kill chain, ATT&CK tactics, Bianco's
rungs, Alshamrani's five-phase APT lifecycle, and Brown's six-phase FSM — plus the
review's own four-rung fidelity ladder. Marc's own gap note already fixes the
discipline ("two kill-chain vocabularies are in play and must not blur"); the review
predates it and breaks it. At 3 000 words the chapter can afford exactly two: ATT&CK
tactics as the working vocabulary, the kill chain named once as lineage — plus the
fidelity ladder, which is an instrument rather than a phase model and should be
visibly distinguished as one.

## (h) Sentence-level findings

Measured, not impressionistic, and read against `voice.md` §(d) rather than a generic
banlist:

- **Em-dashes: 82 in 6 002 words** — one per 73 words, roughly one per three
  sentences. `voice.md` §(d) is explicit that the parenthesis is the authored device
  and the em-dash turn is "the rarer of the two". The ratio is inverted, and this is
  the loudest machine tell in the document.
- **15 of 84 paragraphs close on a forward pointer** to a later section ("that is
  what Section V takes up", "the asymmetry the rest of this review develops"). Nearly
  one in six. In a 3 000-word chapter this habit alone would cost most of a unit.
- **The signature line appears twice, near-verbatim**: "The defender has grown more
  sophisticated; the adversary against which it is evaluated has not" (§I) and "The
  defender's decision-making has advanced; the adversary against which it is
  evaluated is inherited, not modelled" (§II-C). `voice.md` licenses one compressing
  sentence per section and warns the device "dulls with overuse" — the same sentence
  twice is the overuse case.
- **Paired opposition and X-not-Y cluster heavily in §IV-B-6 and §V**: "structural,
  not incidental"; "That located asymmetry — not the absence of any one
  characteristic — is the gap"; "rationality without capability". This is Marc's
  licensed signature move, so the finding is density, not usage: three in two
  paragraphs reads as mannerism where one reads as voice.
- **Tricolons** recur at paragraph closes ("advanced tooling and tradecraft …, a
  persistent low-and-slow tempo …, and a threat defined by its objective";
  "Profiled behaviour, an agent to enact it, parameters grounded in real engagement
  data").

## (i) Two structural notes for the boil-down

- **Bland and Outkin arrive in §V** — new evidence doing real argumentative work
  inside the synthesis. They belong in the model strand (3.2.3), where they
  materially strengthen it: without them that unit is "learning-based attackers
  exist and are shallow", and with them it becomes "the components of a sequencing,
  cost-aware, empirically-parameterised attacker exist and are validated — they have
  simply never been brought to MTD evaluation". That is the review's best line and it
  is currently stranded two pages from the section it belongs to.
- **The stated research question predates the current framing.** The review's RQ
  ("How do existing MTD mechanisms perform against behaviourally-grounded adversarial
  profiles derived from cyber threat intelligence?") is close to the current one but
  precedes the capture / model / evaluate decomposition. The chapter must narrow onto
  the ratified box in `dissertation.tex`, not onto this sentence — worth a deliberate
  diff before drafting rather than an assumption either way.

---

## Priority summary — three moves

1. **Retire the pyramid as the organising frame and promote the fidelity ladder to
   the chapter's instrument — then earn its rungs.** The ladder is the review's real
   contribution, it is currently unargued, and it is what the pyramid was standing in
   front of. Keep the durability argument, carried by Sadlek. *(fixes (a), and the
   second cause in (b))*

2. **Rebuild the gap section around rhetoric-versus-execution.** Lead with the
   finding, evidence it with the ladder-scored cross-section, reframe the sample as
   adverse rather than representative, move He et al. out of the table into prose,
   and compress the two-survey subsection to the two sentences it is worth.
   *(fixes (b), (c))*

3. **Rule on the gap's altitude before drafting anything.** Recommended: fidelity as
   the spine, phase coverage as its consequence. This revises the design brief's
   CONFIRM 2, and it decides what the chapter's last unit — and therefore the
   introduction's opening — actually claims. *(fixes (d))*

Tier audit: clean. No T2 rephrasings applied; no citations supplied; no prose drafted.
