---
status: OPEN — the working surface for §5.1's drafting. Chapter 4's four amendments are applied (DRAFT STATE, ratify on read). Slots 1.1–4.3 are unwritten; work them in order, one dictation at a time.
created: 2026-09-18
owner: Marc (every sentence); session (facts, antecedent checks, the pipeline passes, the budget)
companion: 2026-09-17_ch5_s51_sensitivity_overhaul.md (the brief; its "Second cut" section is the structure this executes)
---

# §5.1 slot generator — fifteen sentences, one at a time

**Read this file alone.** It carries the audience, the conventions position,
the vocabulary register, the chapter 4 antecedents, the ceiling on what may be
claimed, the open decision, and the fifteen slots. The companion brief has the
diagnosis and the Table 5.1 cut; the numbers are in the findings record. No
context needed from a chat scrollback.

**What this is.** Marc's ask, 2026-09-18: *"set up a generator … go through each
paragraph, tick off the structure, and then go through line by line and produce
those in this session."* Taken as a drafting surface, not a `tools/` script: one
entry per sentence slot, carrying the slot's job, what it must not do, the facts
it may use, and where its objects were met in chapter 4 — so each dictation is
about wording only, and no number is guessed. (If "generator" meant a `tools/`
emitter instead, say so and this becomes that.)

**The working loop, per slot.** Session states the slot (job, facts, ceiling) →
Marc dictates → session runs repair-dictation → the slot's text lands here with
its word count → the budget line updates. Passes 4–6 (scrutinise, compress,
voice) run on the assembled paragraph, not on single slots.

**The section's job, in one sentence.** Chapter 4 told the reader three times
that a value could not be derived and pointed each time at this section; §5.1 is
where that debt is discharged, and its product is the sentence naming which
input the chapter's claims are exposed to.

## Budget

| ¶ | Target | Dictated | Status |
|---|---|---|---|
| 1 | ~75 | — | structure ticked, unwritten |
| 2 | ~95 | — | structure ticked, unwritten |
| 3 | ~85 | — | structure ticked, unwritten |
| 4 | ~45 | — | structure ticked, unwritten |
| **§5.1** | **~300** | **0** | |

## Standing constraints (every slot)

- **Never say how a value was produced.** Chapter 4 and the appendices do that;
  a re-deriving sentence is the register the 2026-09-13 draft was retired for.
- **Banned words** (the validation gate greps the block): *anchor, kernel,
  degenerate, operating region, mutation interval, screen, rank, one-at-a-time,
  OAT, Sargent, ten Broeke, seven, VERIFY, [3b]*.
- **Ceiling.** Three claims the record does *not* carry: that the scan-shaped
  and objective families are inert (they are not, at 400 runs per cell); the ×4
  shape corner (its interval sits on the boundary); any per-profile ordering.
- **The tier trap.** The two-tier provenance now in §4.4.2 (priced by MTDSim /
  extrapolated from the exploit shape) is *not* the sensitivity story. The
  objective family is extrapolated too and moves 0.6 hosts per doubling; the
  scan-shaped family is priced and moves 0.7. The concentration is in the
  low-and-slow family **specifically**. ¶2 must not generalise it to the
  extrapolated pair.
  **What carries ¶2's claim instead** (verified 2026-09-18 against
  `tactic_durations.json`): low-and-slow is the **only tier-3 family** — the
  only one resting on judgement with nothing else behind it. The objective
  family is tier 2 (breach and ransomware timings are named as calibration
  targets, none reproduced); the other two are tier 1, not tuned. So §4.4.2's
  "rests on our judgement alone" is ¶2.4's antecedent, and the claim is about
  **one** family, not a tier.
- **The preamble already said the job.** The chapter opening carries "checks
  that the declared numbers do not carry the conclusions". ¶1 opens on the
  question, in a different shape.
- Australian English; present tense, active; voice.md §d for the sentences.

## The audience, in full

Settled 2026-09-17 and carried forward; this is the context every slot is
written against, so it lives here rather than in a chat scrollback.

**Who reads §5.1.** A reader who has finished chapter 4 and has opened no
appendix — concretely, an examiner or Dr Hong: fluent in MTD research,
simulation and ATT&CK, familiar with the published MTDSim lineage, with no
knowledge of this project's internal vocabulary, its files or its runs. Every
sentence must be followable without leaving the page.

**What they arrive holding.** Chapter 4 told them three times that a value
could not be derived, and pointed each time at this section:

- §4.4.2 — the dwell times do not exist in the literature and do not exist in
  CTI vendor reports; prior work calls putting times on an attack inherently
  arbitrary (\citealt{bland2020, mcqueen2006, mendonca2023}).
- §4.4.3 — there is no real tactic-to-verb mapping, so best judgement was used.
- §4.4.4 — the failure side is the blind spot of the CTI; the matrix was
  declared, not reverse-engineered.

So the question they arrive with is not "what is a sensitivity analysis". It
is **"is the evaluation built on numbers you made up?"** §5.1 is where that
debt is discharged. Its product is the one sentence naming which input the
chapter's claims are exposed to — the sentence Table 5.3's declared-inputs row
forward-references and chapter 6's fidelity verdict consumes.

**What that rules out.** Explaining how a value was produced (chapter 4 and the
appendices do that); defending the method; a roadmap (the chapter preamble has
one); any sentence that reads as a retrieval key to the record, which is what
the 2026-09-13 draft was retired for.

**Where the field puts this** (`evaluation_conventions.md` §c). Almost nobody
in the corpus has a titled sensitivity section — Outkin's §5.1.2 is the only
one surveyed; elsewhere the sweep *is* the results section or an unlabelled
axis inside it. One-at-a-time is the universal design, and **range
justification is almost never given** — Hong, Anderson, Carroll, Zhang and
Reti state no rationale for any range; Bland says outright that his rates are
"notional". Deriving ranges from the model's own structure therefore exceeds
the corpus, and should be said once rather than assumed obvious. What the good
papers do instead is **name what they did not sweep**, which is the discipline
this section imports. And: *a sweep that selects the operating region for what
follows is stronger than one that only shows a verdict did not move* — which is
why ¶4 exists as its own paragraph rather than as a trailing clause.

## The vocabulary the reader has, and the standardised term for each

§5.1 may use a term only if the reader has met it in the body of chapters 2–4
(not in a caption, not in a notation table, not in an appendix). This is the
availability register; the ch5 antecedent rule says a missing object becomes a
chapter 4 insertion, never a chapter 5 first use.

| Concept | **The standardised term** | Where the reader met it | Rejected wordings |
|---|---|---|---|
| the three things declared to join the profiles to MTDSim | **the three inputs** | §4.4 opening | "assumptions" (ruled off 2026-09-13 — the assumptions are the sentences at each symbol); "parameters" |
| what was done to them | **chose** them; §5.1 **moves**, **compares** or **holds** each | §4.4 opening, §4.4.4 close | "swept" — wrong for a comparison and for a hold, and it misreports how the values were arrived at (removed 2026-09-18) |
| the timing groups | **family** (scan-shaped, exploit-shaped, low-and-slow, objective) | §4.4.2 | "anchor" — the appendix's and the code's word, banned in the body; the lifecycle names (see below) |
| the range a value was moved over | **band** | §4.4.2, last sentence but one | "sweep range", "interval" (reserved for the confidence interval) |
| the draw | **exponential**, around the **mean dwell** | §4.4.2 | — |
| the mapping | **at most one verb per tactic**; unmapped tactics are **dwell-only** | §4.4.3 | "partial" / "v2" — code words |
| its alternative | **forcing a total mapping** | §4.4.3 | "forced total" as a bare noun |
| the nine rules | **the failure rules**, A–I | §4.4.4 → Fig. B.6(a) | "rule kernel" |
| how far a transition travels | **distance**, in **stages** | §4.4.4 | "kernel" (appendix keeps it); "phase" (re-termed to "stage" 2026-09-08) |
| the four stages | **preparation, intrusion, post-intrusion operations, objective** | §4.4.4 | "CKC phases" |
| the decay | **a rate**, the same whether the jump is forward or a fall back | §4.4.4 | "forward decay / backward decay" as two quantities — the declared model sets both to 0.25 |
| the cut-off | **the floor**, below which a transition is too far to happen at all | §4.4.4 | "z", "zeroing" |
| the simulator | **MTDSim**, or **the simulator** | ch2 throughout | "the substrate" — repo-internal, never in the thesis |
| the attacker arms | **the four attack profiles** (exfiltration objective, impact objective, double extortion, no realised objective) | §4.2, named in the body | "profiles" unqualified where families are also in play |

**The two quartets are different objects.** Four attack *profiles* (§4.2) and
four dwell *families* (§4.4.2). They are unrelated partitions and §5.1 touches
only the families. Do not let a sentence blur them.

**Why the families cannot take the lifecycle names** (asked 2026-09-18,
answered): they are different partitions of the 15 tactics. Eight tactics sit
in the post-intrusion stage across three different families; only the objective
family coincides with its stage, and that is a convenience. The families are
priced by *what a tactic costs*, the stages order *where it sits in a
campaign*. Reusing the stage words would either force a membership change that
re-opens the dwell catalogue, App. B.4's tiers, the §5.1 re-run and every float
built on it, or leave two taxonomies sharing three words. The full 15-row
mismatch table is in the companion brief, §S6.

## The measure §5.1 reads — narrowed 2026-09-18, and closed

**The first statement of this gap was too wide, and is corrected here.** It
was raised as seven blocked slots; it is one term.

Two of the three claimed-missing objects were never missing — the grep used
the wrong words:

- **The defence conditions have an antecedent.** Chapter 2's
  Table~\ref{tab:deployment-strategies} names the four execution schemes,
  \emph{random} among them ("draws one mechanism from the pool at random on
  each interval"). The thesis says *deployment strategies* and *execution
  scheme*; the grep asked for "deployment scheme" and "random scheme" and so
  found nothing. Nothing is owed here.
- **The quantity has an antecedent.** Chapter 2 establishes that compromised
  hosts stay compromised (\citealt{brown2023, zhang2023}), and chapter 3's
  Table~\ref{tab:mtd-metrics} carries the host and network compromise ratios
  under the system-state family. A reader meeting "the distinct hosts the
  attacker compromises" in §5.1 is not meeting a new idea.

**What is actually owed is the name.** §5.2's Table~\ref{tab:metrics} declares
the chapter's measure as **host breadth** — "the distinct hosts compromised in
a run, and its suppression against no defence" — keyed to the system-state
family of Table~\ref{tab:mtd-metrics}. §5.1 precedes it, so §5.1 is the term's
first use, and voice §e forbids §5.1 saying "distinct hosts compromised" while
§5.2 says "host breadth" for the same thing.

**Not the chapter 3 table.** Table~\ref{tab:mtd-metrics} is a survey of metric
families in the literature (\citealt{cho2020}); putting this chapter's own
measure into it would file a result-side declaration inside a literature
review. §5.2's Table~\ref{tab:metrics} is the right home and already holds it.

**Resolution (recommended, and cheap):** §5.1 names **host breadth** at its
first use with its gloss in the same breath — define-before-use satisfied
inside the section, about eight words — and §5.2's table formalises it and
keys it to the family. For the conditions, §5.1 says *under every condition the
chapter runs* rather than enumerating them; the per-condition readings are
App. C.1–C.3's, where the conditions are declared. The ruled section order
stands, and the §5.1/§5.2 swap is not needed.

**Consequence for the slots:** 1.3 and 1.4 name host breadth once between them;
2.2, 2.3, 2.5, 3.2 and 3.3 then quote against it with no further apparatus.

## Chapter 4 antecedents — all four live as of 2026-09-18

| Object §5.1 uses | Where the reader now meets it | State |
|---|---|---|
| the question §5.1 answers, and that the three inputs were *chosen*, not swept | §4.4 opening (insertion A) | applied, DRAFT STATE |
| the four dwell families by name, which part of MTDSim prices each, and that the other two were extrapolated | §4.4.2 (insertion B, extended 2026-09-18) | applied, DRAFT STATE |
| the bands, and that they were chosen — half to twice, a quarter to four times for low-and-slow | §4.4.2, last sentence but one | applied, DRAFT STATE. ¶1 slot 1.5 may now be **dropped**: the reader has met the ranges and their asymmetry before §5.1 opens |
| that low-and-slow rests on judgement alone | §4.4.2, same sentence | applied — this is ¶2.4's antecedent |
| distance, the rate, the floor, and that the rate is the same either way | §4.4.4 (insertion C) | applied, DRAFT STATE |
| the nine failure rules A–I | §4.4.4 → Fig. B.6(a), Appendix~\ref{app:weight-sets} | reference fixed (was pointing at a figure carrying no letters) |
| the mapping and its alternative | §4.4.3, unchanged | stands |

**Closed 2026-09-18:** the §4.4.4 close was rescoped on Marc's reading
("literature-bounded with no citation reads as dangerous ... sensitivity-swept,
that's a stretch"). It now reads "a plausible set of values to feed into our
attacker model, and Section~\ref{sec:sensitivity} reports what it would cost to
be wrong about them" — which is also the cleanest one-line statement of what
§5.1 is for, so ¶1 slot 1.1 should not repeat its shape.

**Nothing open in ch4.** All five amendments are applied and the build is
clean; the slots can be dictated.

---

# ¶1 — the question and the test (~75 words)

**The claim the paragraph establishes:** the question, and what would count as
an answer to it.

### Slot 1.1 — the question
- **Job:** state the question the section answers: whether any conclusion of the
  evaluation depends on where a chosen value sits inside its plausible range.
- **Shape:** plain declarative, the section's first sentence.
- **Must not:** open on an inventory ("three inputs", "seven numbers"); use a
  method noun as the subject; carry over from chapter 4; reuse the preamble's
  wording.
- **Antecedent:** §4.4 opening now ends on this exact question (insertion A) —
  so the reader arrives expecting it. Do not restate that sentence; answer it.
- **Dictation:** *(pending)*

### Slot 1.2 — the three inputs
- **Job:** name the three declared inputs by their §4.4 names.
- **Shape:** one sentence, recall not introduction.
- **Facts:** the dwell times; the tactic-to-verb mapping; the failure matrix.
- **Must not:** use symbols; say "assumptions"; explain what any of them is.
- **Dictation:** *(pending)*

### Slot 1.3 — the test
- **Job:** each value is moved across its range with the others held at their
  declared values, and distinct hosts reached is read against the interval at
  the declared value.
- **Facts:** 100 seeds per cell at present, pooled over the four profiles, 400
  runs per cell; under no defence and under the random scheme at 200 s and
  2 000 s. (The chapter reports 1 000 seeds; this sweep re-launches from the
  defended corpus when that lands — findings §8.)
- **Must not:** name a sweep design in the field's vocabulary; defend the method.
- **The measure:** name **host breadth** here or at 1.4, with its gloss in the
  same breath (see the section above). For the conditions, "under every
  condition the chapter runs" — do not enumerate them.
- **Dictation:** *(pending)*

### Slot 1.4 — what counts as an answer
- **Job:** a value whose range ends stay inside that interval does not carry the
  chapter.
- **Shape:** one sentence — the criterion, stated before any result (voice §c9).
- **Facts:** the interval at the declared value is about ±0.4 hosts with no
  defence and ±0.2 under the 200 s defence, so the test detects a shift of half
  a host. The criterion was fixed in the recorder before the first run.
- **Dictation:** *(pending)*

### Slot 1.5 — where the ranges come from *(optional, a clause on 1.3)*
- **Job:** the evidence tiers of App. B.4 for the dwell times; the structure of
  the distance term for the failure matrix.
- **Must not:** claim this exceeds the corpus — that reading is chapter 6's.
- **RECOMMEND DROPPING** since 2026-09-18: §4.4.2 now states the bands and their
  asymmetry in the body ("half to twice the value, and a quarter to four times
  for the low-and-slow family, which rests on our judgement alone"), so the
  clause would restate what the reader has just read. Fifteen slots becomes
  fourteen and ¶1 comes in under budget.
- **Dictation:** *(pending / recommended dropped)*

---

# ¶2 — the dwell times (~95 words)

**The claim the paragraph establishes:** the model's timing sensitivity is
concentrated in one family, and it is the one whose provenance is weakest.

### Slot 2.1 — claim first
- **Job:** the sensitivity is concentrated in one of the four families.
- **Must not:** narrate the procedure ("the dwell times were moved first").
- **Dictation:** *(pending)*

### Slot 2.2 — the three families that are not it
- **Job:** what they cost across their ranges, as a magnitude.
- **Facts (hosts lost per doubling, no defence / 200 s / 2 000 s):**
  scan-shaped 0.7 / 0.6 / 1.0; exploit-shaped 0.2 / 0.1 / 0.1; objective
  0.6 / 0.3 / 0.9. Only the exploit-shaped family is inert under every
  condition; the other two separate at the ×2 end.
- **Must not:** call all three inert.
- **Dictation:** *(pending)*

### Slot 2.3 — the low-and-slow family
- **Job:** direction and magnitude, under no defence and under defence.
- **Facts:** hosts reached 13.4 / 8.1 / 3.0 at ×0.25 / declared / ×4 with no
  defence; 7.5 / 2.1 / 0.3 at 200 s; 14.7 / 7.4 / 2.0 at 2 000 s. 2.6 / 1.8 /
  3.2 hosts lost per doubling. Monotone, close to linear in the logarithm of the
  multiple; no threshold, no reversal. The longer the quiet tactics dwell, the
  fewer hosts before the horizon.
- **Must not:** use "anchor"; imply a threshold.
- **Dictation:** *(pending)*

### Slot 2.4 — the reading that matters
- **Job:** the sensitivity sits in the family whose provenance is weakest; the
  families the simulator priced carry a fraction of it.
- **Shape:** the section's one compressed sentence (voice §d — rationed).
- **Facts:** low-and-slow carries three to five times the per-doubling
  sensitivity of the next family and about fifteen times the exploit-shaped
  family's, under every condition.
- **Must not:** generalise to "the declared families" (see the tier trap); no
  hype adjective.
- **Dictation:** *(pending)*

### Slot 2.5 — the draw's shape
- **Job:** inert where no defence acts; under mutation pressure the concentrated
  draw costs the attacker a little and never helps it.
- **Facts:** paired Erlang-4 minus exponential. At the declared dwell: −0.01 ±
  0.06 with no defence; **−0.24 ± 0.22 at 200 s** (interval clear of zero, and
  13.3 fewer actions per run); −0.06 ± 0.38 at 2 000 s. Every defended
  difference is negative. Mechanism: a long draw is likelier to be cut by a
  mutation, and the exponential's mass of very short dwells is what lets the
  attacker slip an action between mutations.
- **Must not:** claim the ×4 corner (−0.15 ± 0.15, on the boundary).
- **Dictation:** *(pending)*

---

# ¶3 — the two inputs that are not ranges (~85 words)

**The claim the paragraph establishes:** neither of the other two declared
inputs moves what the chapter reports.

### Slot 3.1 — claim first
- **Job:** neither the mapping nor the failure matrix's numbers move anything.
- **Must not:** open with "moreover", "similarly", or a second inventory.
- **Dictation:** *(pending)*

### Slot 3.2 — the mapping
- **Job:** it is a comparison, not a range; the alternative that was tried
  stalls, with one clause of why.
- **Facts:** the forced-total mapping reaches 0.15 hosts against 8.13 with no
  defence (blocked fraction 0.58 against 0.24), 0.09 against 2.07 at 200 s, 0.12
  against 7.42 at 2 000 s, and never reaches the target. Why: it runs a tightly
  ordered machine in an unordered way and stalls on preconditions (§4.4.3's own
  words, App. B.7).
- **Must not:** use "partial" or "forced total" as bare terms — say what each does.
- **Dictation:** *(pending)*

### Slot 3.3 — the decay
- **Job:** moved across its range at both ends and at the corners, and nothing
  moved.
- **Facts:** 0.1 to 0.5 against a declared 0.25, in both directions and at all
  four corners of the pair; every pooled mean inside the interval at the
  declared value under every condition; the largest shift anywhere is 0.18 hosts.
- **Must not:** present forward and backward as two swept quantities — the
  declared model uses the same rate either way (§4.4.4, insertion C). No "kernel".
- **Dictation:** *(pending)*

### Slot 3.4 — the floor and the rules
- **Job:** the floor can only act on a jump of three stages, which no profile
  net contains; the nine rules are single argued judgements and were held.
- **Facts:** moving the floor to 0.05 and to 0 leaves every recorded field
  bit-identical to the declared value — zero by structure, not by measurement
  (Fig. B.6(b)). The nine rules are A–I; each is one argued value, not a
  magnitude with a range.
- **Antecedent:** the floor is now stated at §4.4.4 (insertion C); the rules now
  resolve to Fig. B.6(a).
- **Dictation:** *(pending)*

---

# ¶4 — what this licenses (~45 words)

**The claim the paragraph establishes:** the one input the chapter's claims are
exposed to.

### Slot 4.1 — name it
- **Job:** the low-and-slow family's dwell.
- **Shape:** short declarative, landing after ¶2–¶3's build (voice §d).
- **Must not:** hedge-stack; restate the magnitude.
- **Dictation:** *(pending)*

### Slot 4.2 — and it is held
- **Job:** it is held at its declared value, and every claim that could turn on
  it says so.
- **Facts:** Table 5.3's "Declared inputs" row already carries the forward
  reference, so this sentence is what that row points at.
- **Must not:** mention the mutation interval (a factor, §5.2's).
- **Dictation:** *(pending)*

### Slot 4.3 — nothing was calibrated *(optional clause on 4.2)*
- **Job:** no range was searched for a fit; the criterion was fixed before the
  runs (voice §c10, the circularity name).
- **Tension:** D1 ruled "no method philosophy" in this section. Marc's call
  whether the clause earns its place here or belongs in chapter 6.
- **Dictation:** *(pending / may be dropped)*

---

## After the fifteen slots

1. Assemble ¶1–¶4; run scrutinise-draft, then compress-to-ledger to ~300, then
   voice-pass.
2. Swap the tex block: delete the placeholder, the REDRAFT SKELETON comment and
   the three retired `[3b]` markers.
3. Regenerate Table 5.1 in the new grammar (brief §S4.2) — an `analyse.py`
   change, not a re-run — and re-cut its caption to five clauses.
4. Appendix C leads; `FLOATS.md`; build check; both handoffs deleted in the
   landing commit.
