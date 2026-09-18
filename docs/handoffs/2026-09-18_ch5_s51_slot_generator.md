---
status: OPEN — the working surface for §5.1's drafting. Chapter 4's four amendments are applied (DRAFT STATE, ratify on read). Slots 1.1–4.3 are unwritten; work them in order, one dictation at a time.
created: 2026-09-18
owner: Marc (every sentence); session (facts, antecedent checks, the pipeline passes, the budget)
companion: 2026-09-17_ch5_s51_sensitivity_overhaul.md (the brief; its "Second cut" section is the structure this executes)
---

# §5.1 slot generator — fifteen sentences, one at a time

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
  declared as multiples) is *not* the sensitivity story. The objective family is
  declared and moves 0.6 hosts per doubling; the scan-shaped family is priced
  and moves 0.7. The concentration is in the low-and-slow family
  **specifically**. ¶2 must not generalise it to the declared tier.
- **The preamble already said the job.** The chapter opening carries "checks
  that the declared numbers do not carry the conclusions". ¶1 opens on the
  question, in a different shape.
- Australian English; present tense, active; voice.md §d for the sentences.

## Chapter 4 antecedents — all four live as of 2026-09-18

| Object §5.1 uses | Where the reader now meets it | State |
|---|---|---|
| the question §5.1 answers, and that the three inputs were *chosen*, not swept | §4.4 opening (insertion A) | applied, DRAFT STATE |
| the four dwell families by name, and why the split is what it is | §4.4.2 (insertion B) | applied, DRAFT STATE |
| distance, the rate, the floor, and that the rate is the same either way | §4.4.4 (insertion C) | applied, DRAFT STATE |
| the nine failure rules A–I | §4.4.4 → Fig. B.6(a), Appendix~\ref{app:weight-sets} | reference fixed (was pointing at a figure carrying no letters) |
| the mapping and its alternative | §4.4.3, unchanged | stands |

**Still open in ch4:** the §4.4.4 close still reads "plausible,
literature-bounded and sensitivity-swept". With insertion A and reword C2 in,
that blanket adjective now contradicts them — the nine rules are held, and the
mapping is compared. Marc's ruled close, so flagged rather than touched.

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
- **Dictation:** *(pending / may be dropped)*

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
