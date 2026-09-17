---
status: open
created: 2026-09-17
owner: Marc (rulings, prose); session (fragments, generators, re-run)
supersedes: nothing — this is the cold read of §5.2 that the ch5 design handoff §20.7b invited ("ratify on read"); §20.3 and §20.5 are the cue cards it was drafted from, and this file is the audit of what discharging them produced
---

# Critique §5.2 Experimental setup: why it does not read as an experimental setup, what the field puts in one, and the shape that follows

## The diagnosis, in one line

**§5.2 was drafted as a reconciliation of the record rather than as a declaration
of an experiment.** Almost every sentence is discharging a debt to another
document — a ruling ID, a terminology collision, a reviewer's objection, a
concession owed to a critique paper — and the debt is what reached the page. The
experiment did not. That is why it reads as a context compaction: it *is* one.

The test a setup section has to pass is the cold one. A reader who has finished
chapter 4 opens §5.2 to learn: what is run against what, on what terrain, for
how long, how many times, and what is measured. The current draft answers
"what is run against what" in a table cell, "for how long" in a table cell,
"how many times" in paragraph five, and **never answers "what is measured" at
all** — paragraph four defers it ("What is measured is named by the section that
reads it"). Marc's "I read it and I don't even know what experiment we're
setting up" is not an impression; it is a correct reading of a section that
defers its own content.

## A. What the field actually puts in a setup section

Evidence: the section-level anatomies under
`docs/implementation/evaluation_anatomies/`, and `docs/workflows/evaluation_conventions.md`
§a, §d, §g. Four papers in the corpus carry a titled or otherwise identifiable
setup movement, and all four have the same four-slot shape.

| Paper | Slots, in order | Length | Argument in it? |
|---|---|---|---|
| **Reti** §5 Experimental setup | scenario generation → fixed environment → termination rule (three items) → replication count. Table 1 *All Possible Varied Parameter Values*, Table 2 *All Fixed Parameter Values*, **identical columns** (Parameter · Description · Value) | one short section, no subsections | none |
| **He** §V Experiment setup | dataset → metrics. Nothing else: the threat model was declared earlier, in §III.A, as *Goal / Knowledge / Capability* | small by construction — conventions §a: "it is small and holds only what the model section did not already carry" | none |
| **Kim** §6.1 | testbed → attack scenario → Table 4 *Key design parameters and their default values* (Type · Variable · Description · Value) → **§6.1.2, a separate numbered part that justifies the rows one by one** | a page | yes, but quarantined in its own sub-part |
| **Ho** | *Experiment Setup* (conditions, fixed-parameter tables) **and a sibling *Evaluation Method*** (collection pipeline, metric calculation) | two headed sections | none |

Three conventions follow, and §5.2 breaks all three.

1. **A setup section declares; it does not argue.** No paper in the corpus
   concedes a limitation inside its setup. Brown owns its attacker's unrealism
   in §V; Zhang puts the concessions in a future-work chapter; He pairs each
   limitation with the future work that would lift it (conventions §g). The
   setup is where the run plan is stated flatly and then left alone.
2. **The metrics are a slot of the setup, or a sibling section — never a
   deferral.** He's §V.B, Ho's *Evaluation Method*, Kim's metric definitions.
   This is the slot §5.2 is missing, and C33 of the design record already ruled
   a table for it (Table 5.4, *Measure · What it is · Read from · Comparable
   across*) that was never drafted.
3. **The threat model lives in the model section, symmetric on both sides**
   (He's *Goal / Knowledge / Capability*, conventions §g). Chapter 4 is the
   attacker's half; the defender's three clauses are the only genuinely
   model-shaped thing §5.2 carries, and they are there because they have no
   other home — which is a fault in chapter 4's coverage, not in §5.2's.

And one that §5.2 honours and should keep: **paired varied/held tables are the
field's form** (Reti; Kim's Type row-group), and stating a run count with
dispersion and intervals **exceeds** every paper in this lineage (conventions
§d — no paper in the lineage reports a confidence interval). That is real and
should be claimed in one sentence, which it currently is.

## B. The audit, paragraph by paragraph

905 prose words against a two-unit ledger (~500). Six paragraphs at
129 / 270 / 143 / 165 / 149 / 49.

**¶1 (129 w) — "Carrying from the sensitivity analysis, three things are
fixed…"** Opens on continuity maintenance, not on the experiment. Three clauses
carrying §5.1's selection forward, then a meta-paragraph about the word
*baseline* doing two jobs. Conventions §f2 asks that the two references be
**named separately at first use**; it does not ask for a disclosure about the
collision. Brown simply writes "the No MTD control group". We wrote a paragraph
about a word. **Net: the first paragraph of the experimental setup says nothing
about the experiment.** The vivid closing sentence ("Neither is called by the
other's name") is a sentence about the thesis's own writing.

**¶2 (270 w) — the factor paragraph.** This is where the experiment actually
is, and it is the longest paragraph in the section, which is the one thing the
draft got right structurally. Three faults:
- **Undefined design vocabulary in its first clause.** "a crossed core of three
  factors … and three factors moved one at a time from that core". Conventions
  §d records that a census of the formal sensitivity/DOE vocabulary across the
  whole source tree returns **zero hits outside this repo**. A general computer
  science reader does not know that *crossed* means every combination. This is
  the terminology fault Marc named, and the field's answer is not a better term
  of art but **a plain sentence**: every combination of the first three is run;
  each of the other three is varied on its own from that grid.
- **Per-factor literature justification in prose, six times over.** "Every
  factor was set up in the literature review" followed by a clause and a
  §-reference per row. That is the *reason column's* job (where it already
  partly lives, duplicated) or Kim's quarantined §6.1.2's job. It is what makes
  the paragraph read as a seam between documents.
- **The one genuinely load-bearing design fact is a subordinate clause.** The
  operating-point argument — at the inherited interval neither attacker
  completes its objective, so a success-shaped measure is pinned at zero and
  cannot discriminate — is the chapter's transferable methodological result
  (it is what §5.2 owes ch6, per the chapter's own tie-in comment). It is
  currently buried mid-list, in a sentence shared with two other factors.

**¶3 (143 w) — the defender's half, fused with two concessions.** The first
three clauses belong (conventions §g; C16). The rest is Jalowski's third
guideline conceded, and the attacker-realism demand split into the half answered
and the half not. **This is pre-litigation**: arguing with a critic before the
run count has been stated. He's form — pair each limitation with the future work
that lifts it — puts both in ch6/ch7, where this thesis already has
`sec:fidelity-verdict` and a future-work chapter waiting for them.

**¶4 (165 w) — the measurement paragraph that does not name the measures.**
Opens with a deferral, then spends its length on Cho's taxonomy coverage
("strong on cost, adequate on containment and delay, silent on the attack
surface, on payoff and on service to users"). That coverage headline is an
honest and valuable claim — and it is a **verdict about the work**, which is
ch6's register, not a setup declaration. Meanwhile the backbone denominator and
the three-valued comparability boundary, which *are* setup, are compressed into
the last two sentences. The slot is inverted: the discussion content is expanded
and the setup content is compressed.

**¶5 (149 w) — replication and inference.** The most field-conventional
material in the section, modelled on Barach's four-sentence form, and largely
right. Two problems: two `[3b]` holes where a number should be (the tolerance,
C38; the per-claim effect floors, C7), so the paragraph currently commits to a
method and not to a value; and it pre-announces a negative result ("adjacent
ranks within a mechanism family are not separable at this count"), which is
honest but lands as the sixth concession in a row.

**¶6 (49 w) — the roadmap.** The chapter opener already carries the roadmap
(Tay's house pattern), and §20.1 point 2 of the design record explicitly said
§5.2 must not repeat it. The draft repeated it anyway. Marc's "that's the
preamble's job" is the design record's own ruling, unapplied.

**The measurable form of "you lose the reader in qualifications":** count the
concessions before a single number has been reported — the frozen defender; no
state-of-the-art comparison (Jalowski 3); half the realism demand unanswered;
silent on four metric families; every cross-arm comparison unpaired; adjacent
ranks not separable. **Six, in ~900 words.** Each is individually defensible and
several are genuinely creditable. Together they are the section's dominant
register, and a reader cannot tell a load-bearing constraint from a courtesy.

## C. Why it happened — three mechanisms, so it is not repeated

1. **The brief was a debt list, and the draft summed it instead of triaging
   it.** §20.3 and §20.5 of the design handoff are fourteen numbered content
   points, each anchored to a ruling ID. Every one is load-bearing *to the
   record*. The draft discharged all fourteen. The rule that was missing:
   **when every point in a brief is load-bearing to the record, none of them is
   load-bearing to the reader** — a brief is triaged against the reader before
   it is drafted, and the points that do not survive go to the document whose
   register they belong to.
2. **The register was calibrated on a faulty exemplar.** The DRAFT STATE comment
   says "Register calibrated on §5.1's draft." §5.2 was drafted 2026-09-15;
   §5.1's draft was diagnosed on 2026-09-17 as failing on seven counts,
   including the three §5.2 shares — written as retrieval keys to the record,
   half the prose defending the method, objects introduced that the reader has
   not met. The fault propagated forwards before it was found.
3. **Conventions §a was read for placement and not for size.** The finding was
   that where a paper titles a setup section, *it is small and holds only what
   the model section did not already carry*. We took the placement and inverted
   the size: §5.2 is the largest setup in the corpus and is filled with material
   chapters 2, 3 and 4 already carry.

## D. The tables

Both are hand-set (C39's generator pass is still owed). Two faults are shared
and one is per table.

**Shared fault 1 — the two tables do not read as a pair.** Reti's do, because
the columns are identical in both (Parameter · Description · Value). Ours are
*Factor · Levels · What the levels are for* against *Held · Value · Why it is
held*. Same object, two grammars. Cheapest high-value fix in this whole brief:
**one column grammar across both tables.**

**Shared fault 2 — the last column carries three registers.** This is exactly
the fault the §5.1 cold read found in Table 5.1 ("three kinds of row share one
table column"), unfixed here. In `tab:factors-varied` the fourth column is by
turns: a *definition* ("the comparison arm, and five instantiations of the
model"), a *design reason* ("no defence is the reference every effect is a
difference from"), and a *reporting instruction* ("read in separate panels").
A reader cannot learn the column's contract, so they stop reading it — which is
precisely what Marc reported ("what the levels are for — I just go off the deep
end"). One register per column: **the reason the level set is what it is**, and
nothing else. Reporting instructions go to the prose or the caption; definitions
go into the Levels cell.

**`tab:factors-varied` (varied).**
- The row-group labels *Crossed* / *One at a time* are unexplained DOE jargon
  (see §B ¶2). Either plain-language group labels (*Varied together* / *Varied
  singly*) or — better — no group labels and one sentence in the caption saying
  what the grouping means.
- The Levels column carries prose and one implementation internal: "the
  inherited draw is the mean plus an exponential term of half a second, a clock
  in effect". That is a description (belongs in the reason column) and it
  breaches the chapter's own no-internals rule, which the fixed table's footnote
  otherwise enforces.
- The attacker-arm Levels cell packs six levels plus a parenthetical taxonomy
  into one cell. Unscannable; the aggregate's gloss belongs in the reason
  column.

**`tab:factors-fixed` (held).**
- Thirteen rows, four row groups, and a footnote carrying three version pins —
  ambitious against Reti's Table 2 (nineteen rows, three columns, no
  justification column at all) and defensible, because the justification column
  is the honest upgrade. But the column currently carries *inferential
  arguments*: "shared seeds give no matched randomness across arms, so every
  comparison across attackers is unpaired" is an inference-model statement
  sitting in a table of held constants, **and it duplicates ¶5 verbatim in
  substance.**
- "Runs per cell | 100 | the interval on a cell mean sits inside the declared
  tolerance; adjacent ranks within a mechanism family are not separable at this
  count and are not reported" — two claims in one cell, the second of which is a
  result.

## E. The shape that follows (proposal — Marc's to rule, and his prose)

Two movements, no subsections, the tables carrying the internal structure
(C32, unchanged). **~450 words**, which brings the section inside its ledger
rather than 80 % over it.

| ¶ | Job | Content | Words |
|---|---|---|---|
| 1 | **what is run against what** | The arms and the conditions, flatly: the baseline attacker and the movement attacker on four profiles and the aggregate, against no defence, each of the seven mechanisms alone, and two schemes. One clause fixing *no defence* as the reference every effect is a difference from. Table 5.2 introduced in one sentence. | ~90 |
| 2 | **the terrain, the tempo, the horizon** | One terrain, held (Table 5.3). The two intervals, carrying the operating-point argument **as the paragraph's own sentence, not a clause**: at the inherited tempo neither attacker completes its objective, so a success-shaped measure cannot discriminate there, and every claim states the interval it was taken at. The horizon and why deployments per run are held with it. | ~110 |
| 3 | **what is held, and the defender** | Table 5.3 in one sentence. The defender's three clauses (goal: disrupt, not detect; knowledge: none, there being no detection channel; capability: the seven mechanisms on a schedule it never departs from). The negative scope in one clause: one terrain, scale and density not varied. | ~90 |
| 4 | **what is measured** | **The missing slot.** The outcome measures named, grouped by the section that reads them, with the backbone denominator stated and the three-valued comparability boundary as the table's last column rather than a paragraph. Table 5.4, generated. | ~80 + table |
| 5 | **how many times, and how it is summarised** | Barach's four-sentence form: replications, the same seeds on every arm, arms independent so unpaired, effect sizes with intervals — and the one sentence claiming that as an advance on the lineage. | ~80 |

**What leaves, and where it goes.**

| Leaves §5.2 | Goes to | Why |
|---|---|---|
| the §5.1 carry-over (¶1, three clauses) | nowhere, or half a clause | §5.1 already closes by naming its selection; Marc's own §5.1 ruling applies verbatim — "the preamble can carry that; the section stands on its own" |
| the *baseline* / *no defence* reconciliation (¶1) | deleted | Use the words. The collision is a drafting constraint, not a finding |
| Jalowski's third guideline conceded (¶3) | ch6 `sec:fidelity-verdict` | He's form: limitation paired with the future work that lifts it |
| the attacker-realism half-answered clause (¶3) | ch6 / ch7 | same |
| the Cho coverage headline, five of ten families (¶4) | ch6 `sec:evaluation-implications` | it is a verdict about the work |
| the closing roadmap (¶6) | the chapter preamble | already ruled, §20.1 |
| the "adjacent ranks not separable" rider (¶5, and a table cell) | **possibly nowhere** — see F1 | at a higher seed count the concession may not exist |

## F. Rulings owed

**F1 — the run count (Marc, this session: "you bump those numbers up").
Recommendation: 1 000 seeds per cell, and it removes a concession rather than
adding a number.**

The arithmetic, from the record (provenance, not values — re-derive before any
of it reaches the tex): the crossed core is 6 arms × 11 conditions × 2 intervals
= 132 cells; at 100 seeds that is ~13 200 runs, and the chapter's full plan
including the one-at-a-time extensions and the §5.1 re-run is ~31 500 runs. A
movement run costs ≈ 0.2 s, and the predesign priced the 100-seed matrix at
≈ 1.5–2 h on six workers. **At 1 000 seeds the chapter is ~315 000 runs, which
is an overnight batch, not a new budget.**

What it buys is not decoration. The predesign's normal-approximation power
requirement for the adjacent within-family pairs was ≈ 18, 22, 190 and 329 seeds
per cell, the two tight pairs driving the budget. At 100 seeds the tight pairs
fail, which is why ¶5 and a table cell both carry the "not separable, not
reported" rider and why the reportable object shrinks to a two-by-two family
contrast. **At 1 000 seeds the tightest pair clears by roughly threefold, the
rider is deleted from the prose and from the table, and the chapter can report
an ordering within a mechanism family.** The run count then has a better
sentence than the tolerance one: chosen so that the closest pair the chapter
compares separates. That is still Hoad's third method, it closes C38's `[3b]`
hole without Marc having to pick a tolerance from nothing, and it is a
declaration of strength where six declarations of weakness currently sit.

*Cost to check before committing:* the ≈ 0.2 s per-run figure is from the
pre-restoration substrate at the 15 000 s horizon. The 60 000 s horizon arm is
four times the simulated time, and the extended-horizon cells should be
wall-clocked on ~20 runs before the full batch is launched (the rate study's
"no silent caps" convention).

**F2 — the remaining rulings, each one line.**

| # | Question | Recommendation |
|---|---|---|
| S1 | Does §5.2 open on the experiment, with the §5.1 carry-over deleted? | Yes — Marc's own §5.1 ruling, applied to its neighbour |
| S2 | Do the two concessions and the coverage headline leave for ch6/ch7? | Yes; ch6 has the sections waiting |
| S3 | Table 5.4 (the measures), generated, as the fourth slot? | Yes — C33 ruled it and it was never drafted; it is the section's one content hole |
| S4 | One column grammar across Tables 5.2 and 5.3 (Reti's paired form)? | Yes |
| S5 | *Crossed* / *One at a time* row-group labels | Replace with plain words, or drop the labels and put the grouping in the caption in one sentence |
| S6 | Does the operating-point argument get its own sentence? | Yes — it is what §5.2 owes ch6 |
| S7 | Run count (F1) | 1 000 seeds, wall-clocked on the extended-horizon cells first |

## Validation gate

The redraft is done when, on a cold read of §5.2 alone, a reader can answer all
five without leaving the section: **what is run against what; on what terrain;
for how long; how many times; and what is measured.** And, mechanically:

- `grep` the section for *crossed*, *one at a time*, *baseline* (as the
  no-defence condition), *Jalowski*, *taxonomy* — all should be absent.
- No sentence in the section states a limitation that ch6 or ch7 does not also
  state.
- Both tables' last columns answer one question, stated in the caption.
- Prose word count ≤ 500.
- No `[3b]` marker left standing on a number that F1 has made derivable.

## Reading list

- `docs/thesis/dissertation.tex` §5.2 (`sec:dimensions`) and the two table
  fragments under `docs/thesis/tables/`.
- `docs/workflows/evaluation_conventions.md` §a, §c, §d, §f2, §g, §h.
- `docs/implementation/evaluation_anatomies/{reti2022,he2025,kim2026,ho2024}.md`
  — section B of each is the four-slot evidence.
- `docs/handoffs/2026-09-09_ch5_experiments_design.md` §20 (the cue cards this
  draft discharged) and §20.7b (what was drafted).
- `docs/handoffs/2026-09-17_ch5_s51_sensitivity_overhaul.md` — the sibling
  diagnosis; the register fault is shared and the fix is the same fix.

## Out of scope

Chapter 4's coverage of the defender (the three clauses have no home there and
arguably should); the §5.1 re-run, which is its own handoff; the generator pass
C39, which this brief assumes but does not specify.
