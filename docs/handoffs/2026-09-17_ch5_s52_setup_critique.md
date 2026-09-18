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

---

# Part 2 — the fix (2026-09-17, after Marc's reply)

Marc's ratifications on the critique: do what the field does (environment /
arms and conditions / parameters / procedure, four paragraphs plus tables);
metrics are a slot, never a deferral; the concessions leave for the discussion
and future work; the word count is the primary symptom; the tables carry too
much jargon. On the run count: **write 1 000**, with the working protocol in
§J. What follows is the executing plan.

## G. The principle the redraft is held to

**An experimental setup is a run plan written for someone who has read the
preceding chapters and nothing else.** It declares; it does not reconcile, defer
or concede. The reader has followed the argument from chapter 2 to chapter 4 and
arrives wanting five answers, in this order, in the chapter's own established
words: *what is run against what; on what terrain; what varies and what is held;
what is measured; how many times and how it is summarised.* Anything in the
section that is not one of those five answers is in the wrong document.

Two corollaries, because they are what the current draft breaks:

- **A forward reference is not an answer.** "What is measured is named by the
  section that reads it" is the section declining to do its job. Every measure
  the chapter reports is named here, once, in a table.
- **A concession is not a declaration.** Each of the six now in §5.2 has a home
  in chapter 6 or chapter 7, where the field puts them and where this thesis
  already has the sections built.

## H. The new §5.2, paragraph by paragraph

Five paragraphs, ~470 words, three tables. Each paragraph answers exactly one of
the five questions and is named for it below; the *must not contain* line is the
operative half of each entry. Content points only — the prose is Marc's, or is
session-drafted to this skeleton and ratified (§L).

| ¶ | Answers | Content points | Must not contain | Words |
|---|---|---|---|---|
| 1 | **On what terrain** | One network for every run: 50 hosts, 5 exposed endpoints, 8 subnets, 4 levels, with the topology drawn fresh per seed. The target: the two database hosts at the deepest level. The run ends at the horizon or when the objective is reached. One clause of negative scope: one terrain only, scale and density not varied. | any justification of the network's realism; any reference to §5.1; the words *carrying from* | ~75 |
| 2 | **What is run against what** | The two attacker arms named plainly — the baseline attacker of §2.2.3, and the movement attacker of chapter 4 on each of the four attack profiles and on the aggregate. The defence conditions: **no defence**, each of the seven mechanisms alone, and the two deployment schemes. One clause fixing no defence as the reference every effect in the chapter is a difference from. The defender in three clauses: its goal is to disrupt, not to detect; it knows nothing of the attacker, there being no detection channel; its capability is the seven mechanisms on a schedule it never departs from. | the word *baseline* for the no-defence condition (use the words, do not discuss them); Jalowski; any concession about the defender being frozen | ~120 |
| 3 | **What varies, what is held** | Table 5.2 in one sentence, Table 5.3 in one sentence. The design in plain words: every combination of attacker arm, defence condition and mutation interval is run; each of the other three factors is varied on its own from that grid. **Then the operating-point sentence, standing alone**: at the inherited interval neither attacker completes its objective, so a success-shaped measure is pinned at zero and cannot discriminate there; it is read at the longer interval, and every claim states the interval it was taken at. | *crossed*, *one at a time* as terms of art; per-factor literature justification (that is the tables' *Why* column); any reference to §5.1's discipline | ~110 |
| 4 | **What is measured** | Table 5.4 in one sentence, grouped by the section that reads it. One clause scoping §5.3's instruments as model-validation measures rather than MTD metrics. The backbone denominator stated once: distinct hosts compromised, because it varies at every interval, with target reach reported beside it wherever it is non-degenerate. Comparability is the table's last column, not a paragraph. | Cho's taxonomy; the five-of-ten coverage headline; the word *silent*; any deferral of a measure to a later section | ~85 |
| 5 | **How many times, how summarised** | Barach's four-sentence form. A thousand seeds per cell, chosen so that the closest pair of conditions the chapter compares separates. The same seeds on every arm, arms independent, so every cross-arm comparison is unpaired. Effect sizes with 95 % intervals, and the one sentence claiming that as an advance: no evaluation in this lineage reports one. Tests attached to declared claims, adjusted within each family, each with a minimum effect of interest fixed before the run. | the *adjacent ranks are not separable* rider (§J deletes it); a `[3b]` hole where the tolerance used to be | ~80 |

No closing roadmap paragraph. The chapter preamble carries it, and §5.3's first
sentence picks the thread up.

## I. The relocation ledger — every sentence currently in §5.2

Nothing is discarded for being wrong; four things are moved because their
register belongs elsewhere.

| Currently in §5.2 | Disposition | Where it goes |
|---|---|---|
| "Carrying from the sensitivity analysis, three things are fixed…" | **dies** | — (meta) |
| low-and-slow held at its declared value, named in claims that turn on it | **moves** | already a Table 5.3 row (*Declared inputs*); prose clause dies |
| the exponential draw live only at long dwell under mutation | **dies from §5.2** | §5.1's finding; the factor is a Table 5.2 row |
| the inherited interval sits in a degenerate region | **stays, promoted** | ¶3's own sentence — this is what §5.2 owes ch6 |
| the *baseline* / no-defence reconciliation; "Neither is called by the other's name" | **dies** | use the words in ¶2 |
| "Every factor was set up in the literature review" + six per-factor §-references | **moves** | Table 5.2's *Why* column, one clause per row |
| the defender's three clauses | **stays** | ¶2 |
| Jalowski's third guideline conceded | **moves** | ch6 `sec:fidelity-verdict` |
| the attacker-realism half answered / half not | **moves** | ch6 `sec:fidelity-verdict`, paired with `ch:futurework` (He's form) |
| "What is measured is named by the section that reads it" | **dies** | replaced by Table 5.4 |
| the five-of-ten coverage headline | **moves** | ch6 `sec:evaluation-implications` |
| the backbone denominator; comparability three-valued | **stays** | ¶4 and Table 5.4's last column |
| replication, seeds, unpaired, intervals, tests, effect floors | **stays** | ¶5 |
| "adjacent ranks … not a total order" | **dies** | §J: at a thousand seeds the constraint does not exist |
| "Each section that follows reads a slice of this space" | **dies** | the chapter preamble |

Four `[3b]` markers currently standing: the vivid sentence and "floods a
network" die with their paragraphs; the tolerance (C38) is closed by §J; the
per-claim effect floors (C7) remain Marc's numbers and stay as one marker.

## J. The run count — what to write, and the working protocol

**In the thesis: a thousand seeds per cell.** The justifying sentence is better
than the tolerance one it replaces, because it names a capability rather than a
budget: *the count is chosen so that the closest pair of conditions the chapter
compares separates.* That is still Hoad, Robinson and Davies' third method (the
count is a consequence of a declared precision), it closes C38 without Marc
having to pick a tolerance from nothing, and it deletes the "adjacent ranks are
not separable, so no ordering is reported" rider from both the prose and Table
5.3 — one concession removed rather than a number inflated.

**The working protocol (Marc, this session), which stays in this handoff and
never reaches the tex.** A hundred seeds is the preliminary pass: it is what the
floats are read and argued from, and what goes to the supervisor. Once a
subsection is settled and signed off, the cell set is re-run at a thousand seeds
overnight and the floats are regenerated from that corpus. The thesis reports
the thousand-seed numbers only.

**The consequence to plan for, stated plainly.** `data/results/ch5_defended/run_corpus.py`
sets `SEEDS = tuple(range(100))`. Every §5.3–§5.5 float that landed on
2026-09-17 is a hundred-seed float. Raising the count is therefore not a text
change: **the whole float set is re-derived**, and the §5.1 re-run must be
launched from the same corpus so that its effect column and Table 5.2's tempo
row describe the same substrate. Cost, from the record and to be re-measured
rather than trusted: ~31 500 runs at a hundred seeds becomes ~315 000, at
≈ 0.2 s per run on six workers — an overnight batch. The 60 000 s horizon arm is
four times the simulated time per run and must be wall-clocked on ~20 runs
before the full batch is launched.

**Do not write "preliminary" anywhere in the chapter.** The thesis declares one
run count and reports numbers taken at it. The two-stage protocol is a working
practice, not a methodological disclosure.

## K. The tables

### K1. One column grammar across Tables 5.2 and 5.3

Reti's paired tables read as a pair because their columns are literally
identical. Ours should share the grammar **[the thing · its value · why]**, with
natural headers:

- **Table 5.2** — `Factor · Levels · Why these levels`
- **Table 5.3** — `Held fixed · Value · Why it is held`

Three columns each, the same widths, the same reading contract. The last column
answers **one** question — *why this setting and not another* — and nothing
else. Definitions move into the Levels/Value cell; reporting instructions
("read in separate panels") move to the prose or die; inferential arguments
("shared seeds give no matched randomness…") die from the table, since ¶5 says
it already.

### K2. Table 5.2 — the row groups in plain words

Replace the `\rowgroup` labels *Crossed* / *One at a time* with **Every
combination** / **One at a time**, and carry the meaning in the caption: *The
first three factors are run in every combination; each of the last three is
varied on its own, with the first three held at their first level.* A general
computer science reader needs no term of art for this, and per conventions §d
the field never uses one.

Row-level repairs:

| Row | Repair |
|---|---|
| Attacker arm | split the six levels so they scan; the aggregate's gloss ("the corpus unpartitioned by objective") moves to the *Why* column |
| Defence condition | "read in separate panels" leaves the table |
| Mutation interval | *Why*: the inherited tempo, and one above the boundary at which the objective becomes reachable — the prose carries the consequence |
| Timing regime | delete "an exponential term of half a second": an implementation internal, and the chapter's own no-internals rule bars it. Levels: *quasi-periodic (inherited)*; *exponential, same mean*. *Why*: whether a schedule that arrives on a clock is the pattern an APT learns |
| Horizon | *Why*: the lineage's horizon, and headroom for a campaign, with deployments per run held so a longer run is not silently more defence |
| Objective | *Why*: the APT pursues a specific objective against a specific target; the opportunistic level exists for the prior evaluations only |

### K3. Table 5.3 — the same treatment

Keep the four row groups (*Environment*, *Replication*, *Attacker*,
*Defender*) — those are plain words and they are the table's navigation. Repairs:

- **Runs per cell**: value becomes 1 000; the *Why* cell becomes one claim
  ("the closest pair the chapter compares separates at this count"), and the
  "adjacent ranks are not separable" clause is deleted.
- **Seeds**: *Why* becomes the fact, not the inference — "the same seed set on
  every arm; the arms are independent". ¶5 draws the consequence.
- **Deployment durations / confusion penalty**: unchanged; the dagger and the
  version-pin footnote stay, and stay only here.
- **Adaptive selector**: unchanged — this is the one *declared absence* that
  belongs in a setup table, because the reader has met MTDShield in chapter 2
  and would otherwise find the roster short.

### K4. Table 5.4 — the measures (the missing slot)

Columns `Measure · What it is · Read from · Comparable across`, row-grouped by
the section that reads it. The rows are the record's (design handoff §20.5),
each definition one clause; any measure needing an equation sends it to an
appendix. The last column is where the three-valued comparability boundary
lives, which turns a paragraph into a property of each row.

A measure enters this table only if the corpus run actually produces it.
Internal MTTC stays out until its brief is ruled; the compromise-checkpoint
measure stays out unless the horizon ruling takes it.

**Generation.** Tables 5.2 and 5.3 are hand-set and C39's generator is owed;
Table 5.4 should be born generated, emitted by the same reader that produces
the §5.3–§5.5 floats, so the declaration and the executed plan are one object.
A `tools/ch5_setup_tables.py` reading the run matrix in `run_corpus.py` emits
all three.

## L. Order of work

1. **Ratify §H's five-paragraph skeleton and §I's ledger** (Marc). Everything
   downstream depends on the ledger, since four items leave the section.
2. **Re-cut the two tables** (§K1–K3) — session, mechanical, no prose. These can
   land before the paragraphs are written and are the fastest visible
   improvement.
3. **Build Table 5.4** (§K4) from the records, generated where the reader
   supports it.
4. **Place the four relocated items** in ch6/ch7 as comment blocks at their
   sites, for Marc to accept item by item — the same method used for the
   chapter 4 insertions on 2026-09-17.
5. **The prose.** Either Marc dictates against §H and the session runs passes
   2–5 of the drafting pipeline, or the session drafts to the skeleton for
   ratification. **Recommendation: session-drafts-to-skeleton**, because the
   fault diagnosed in Part 1 was the *brief* (fourteen untriaged debt points),
   not the drafting, and §H is a triaged brief with an explicit exclusion list
   per paragraph. Marc's voice pass follows either way.
6. **The run count** (§J) — change `SEEDS` when a subsection is signed off, not
   before; wall-clock the extended-horizon cells first.

## Validation gate (Part 2)

Part 1's gate stands, plus:

- §5.2 contains no forward reference that stands in for a declaration; in
  particular every measure the chapter reports appears in Table 5.4.
- The four relocated items appear in ch6/ch7 and nowhere in ch5.
- Both factor tables have three columns, the same grammar, and a last column
  answering one question.
- No term of art for the design appears in the body; the caption says it in a
  sentence.
- The section reads, end to end, as five answers in the order a reader asks
  them.

---

## M. What landed (2026-09-17, same session)

Steps 2–5 of §L are done; step 1 was Marc's ratification and step 6 (the run
count) waits on a signed-off subsection.

| Artefact | State |
|---|---|
| §5.2 prose | **Redrafted** to §H's five-answer skeleton. **539 words in five paragraphs**, down from 905 in six. Each paragraph answers one question and carries its exclusion list in the `DRAFT STATE` comment. One `[3b]` left standing: the per-claim effect floors (C7), Marc's numbers |
| `tab_5-2a_factors_varied` | **Re-cut.** Three columns, `Factor · Levels · Why these levels`; row groups *In combination* / *One at a time*; the design stated in the caption; the half-second internal deleted; em-dashes in the attacker-arm cell swapped for parentheses |
| `tab_5-2b_factors_fixed` | **Re-cut.** Same grammar, `Held fixed · Value · Why it is held`; runs per cell 1 000; the unpaired argument and the not-separable rider removed to the prose and to nothing respectively; rotated labels set with multirow's `[vmove]` fixup, values measured off the built page |
| `tab_5-2c_measures` (Table 5.4) | **New.** `Measure · What it is · Read from · Comparable across`, twelve rows in three groups. Every row is a quantity `analyse.py` actually computes; blocked fraction is marked movement-arm because it is structurally zero on the baseline arm (`analyse.py:166`) |
| ch6 relocations | **Placed as proposed-insertion comment blocks** at `sec:fidelity-verdict` (Jalowski's third guideline; which half of the realism demand is answered) and `sec:evaluation-implications` (the coverage headline). Not drafted into prose — Marc accepts item by item |
| Build | `pdflatex` clean, 92 pages, no undefined references or citations; the three tables checked on the rendered page |

**Two corrections made against the design record while drafting**, both from the
runner rather than from the handoff: the conditions are **ten**, not eleven
(`run_corpus.py::CONDITIONS` — no defence, seven mechanisms, two schemes); and
the geometry, target set and intervals are transcribed from `GEOMETRY` and
`INTERVALS` rather than from §20.4's prose.

**One defect this redraft exposed, flagged and not fixed.** §5.1 still closes
"The sweep selected three things, and Section~\ref{sec:dimensions} picks them
up." §5.2 no longer picks them up — that carry-over paragraph is the first thing
§I cut, on the ground Marc ruled for §5.1 itself (the section stands on its own;
the preamble carries the join). The sentence is therefore a promise §5.2 does
not keep. It belongs to the §5.1 overhaul, whose D2 ¶3 already ends that section
on the exposed input with no forward reference, so it is **flagged in place at
the §5.1 site and left for that brief** — the tex of §5.1 is under Marc's hand.

**Still owed:** the C39 generator pass over all three tables; the ch6 insertions'
prose; the 60 000 s wall-clock probe before any thousand-seed batch; the effect
floors.

---

# Part 3 — the readability pass (2026-09-18, Marc's second read)

Part 2's redraft was ratified and landed (§M). Marc read the built pages and the
verdict is **not that the shape is wrong — it is that the prose is still doing
work the tables should do, and the tables are doing work nobody asked for.**
"It's clear how you set it up" is the part that now holds; "very verbose … we're
hiding the meat and bones behind trying to gel it all together" is the part that
does not. This part is the executing plan for that, and it **inverts two of
Part 2's own ratifications** (§N3, §N4) on evidence Marc supplied by reading the
page.

## N. The diagnosis, in four findings

**N1. The register is still connective when it should be declarative.** Part 1
diagnosed *what* §5.2 said; this is a diagnosis of *how* it says it. Every unit
is a paragraph whose sentences are joined into a flow, and a run plan is not
read in flow — it is scanned for five answers and then left. The joins are the
verbosity: "Two attackers are run against one defender, each across the same ten
conditions" spends a sentence establishing a relation the reader already holds
from chapter 4, before any of the three objects has been named. Marc's fix is
structural, not a word count: **name the object, then declare it** —
*Network. … Attacker. … Defender. … Metrics. … Runs.*

**N2. The section's logical objects are three, and the draft fuses two of
them.** The network is held; the attacker and the defence are what get switched.
The current ¶2 carries both attacker and defender in one paragraph because the
Part 1 brief filed the defender's three clauses as a debt to discharge rather
than as one of the experiment's three parties. Split them. The reader then meets
the same three objects §5.4 and §5.5 will vary.

**N3. The operating-point sentence is a result, and it is in the setup.
INVERTS §H ¶3 and §F2/S6.** Part 1 promoted it deliberately ("it is what §5.2
owes ch6"). Marc's read: *"200 seconds, neither attacker reaches objective —
that sounds like a result to me … this still sounds like a concession."* He is
right and the earlier ruling was wrong on its own principle: §G states that a
setup declares and does not concede, and *at the inherited interval a
success-shaped measure is pinned at zero and separates nothing* is a finding
about the substrate reported before a single number. The **declaration**
survives ("both intervals are run; every claim states the interval it was taken
at"); the **finding** goes where it is evidenced — §5.4's numbers show it — and
its methodological reading goes to ch6, which is where §5.2 was owing it anyway.

**N4. The tables' last column does not pay for itself, and the tables are two
thirds of the section. INVERTS §D's "the justification column is the honest
upgrade."** Measured on the built page (`dissertation.pdf`, 2026-09-17 build):
§5.2 runs from the foot of p. 41 to p. 44, with **p. 43 almost entirely
Table 5.3 and p. 44 entirely Table 5.4** — roughly 540 words of prose against
two and a half pages of table. Marc read the *Why* cells one by one and the
verdict was consistent: *"no defence is the reference every effect is a
difference from, and recent evaluations run mechanisms both alone and in
schemes"* — gives nothing; *"one terrain, so every difference is the attacker's
or the defence's"* — very little; *"why do we even have a citation"* on the
Jalowski cell. His principle, and it is the right one: **the justification lives
implicitly in the choice of what to vary.** A reader who has read chapters 2–4
knows why the attacker arm is a factor; saying it is not rigour, it is filler
that costs a page.

## O. Run-in labels — the convention evidence, and the one collision

**Marc's question: "could we write *Network* in bold and then just say how we
configure the network — is that something that we can do?" The answer is yes,
and the corpus attests it precisely in declarative passages.**

| Paper | Form | Locator |
|---|---|---|
| He 2025 | the threat model *and* the defence model are *Goal / Knowledge / Capability*, "each label italicised once" | `evaluation_anatomies/he2025.md` §B; §III.A, §IV.A |
| Zhang 2023 | the attacker profile "given as four bold-run-in features" | `evaluation_anatomies/zhang2023.md` |
| Cho–Ben-Asher 2018 | a transition-by-transition walkthrough "under seven bold run-in headings" | `evaluation_anatomies/chobenasher2018.md` §4.1 |
| Alavizadeh 2022 | limitation paragraphs "headed inline by the italic run-in word *Limitations.*" | `evaluation_anatomies/alavizadeh2022.md` |

He's is the on-point exemplar: it is the *model declaration*, the thing §5.2
is, and conventions §g already rules its Goal/Knowledge/Capability form as "the
tightest in the corpus". So this is not a formatting preference — it is the
field's form for exactly this content, and adopting it closes a gap rather than
opening one.

**The collision, stated rather than worked around.** `voice.md` §(h) bans
"**Bold-term-colon listicles as argument** (*"**Flexibility:** the system…"*)"
and §(d) says "in LaTeX, `\emph` only". A `\textbf{Network.}` run-in trips both.
The honest reading is that §(h)'s ban targets listicles **as argument** — a
section that argues by asserting bolded virtues — and §5.2 argues nothing by
construction (§G). But `voice.md` is a hard gate for `thesis/`, so this needs a
ruling rather than a session's reading of intent.

**Recommendation: italic run-in labels (`\emph{Network.}`), licensed only in
declarative setup passages.** It takes one carve-out (the §(h) row, scoped) in
place of two, it is He's own form, and it leaves bold free for the one thing
§(d) reserves it for. Bold is available if Marc wants maximum scannability and
will rule the §(d) line as well; the corpus carries both. Either way the
carve-out is written into `voice.md` §(h) with the scope clause — *declarative
setup and model-declaration passages; never in argued prose* — so it cannot
spread to ch6.

No `\paragraph{}` and no new macro: the label is `\emph{Word.}` at the head of
the unit, the sentence running on. (Census: `\paragraph{` appears 0 times in
`dissertation.tex`; this introduces no mechanism.)

## P. The new §5.2 — six run-in units, ~340 words

Same five answers as §H, re-cut so each is scanned rather than read, and with
§H ¶3's result removed. The *must not contain* line is again the operative half.

| Unit | Answers | Content | Must not contain | Words |
|---|---|---|---|---|
| **Network.** | on what terrain | the geometry, the target, the topology drawn per seed; one clause of negative scope | any justification of its realism; any reference to §5.1 | ~55 |
| **Attacker.** | what is run | the two arms named flatly; the declared absence (cost model and memory off) | the word *baseline* for the no-defence condition; any defence of the profile set | ~45 |
| **Defender.** | against what | the three clauses (goal, knowledge, capability); the declared absence (MTDShield); the ten conditions; no defence as the reference | Jalowski; any concession about the defender being frozen | ~85 |
| **Design.** | what varies, what is held | the two tables in one sentence each; the plain-words design; both intervals reported and every claim naming its interval | the operating-point finding (§N3); per-factor justification; *crossed*, *one at a time* as terms of art | ~55 |
| **Metrics.** | what is measured | the table in one sentence, keyed to Table 3.1's families; the backbone denominator; §5.3's instruments declared as validation and not as metrics | Cho's coverage headline; any deferral of a measure | ~65 |
| **Runs.** | how many times | Barach's four sentences, unchanged from the landed draft | the *not separable* rider; a `[3b]` on the tolerance | ~80 |

**Why *Design.* survives when Marc asked what ¶3 can do that the captions
cannot.** One fact is not a caption's to carry: that three factors are run in
every combination and three are varied singly *from that grid*. A caption
describes its own table; this describes the relationship between the two tables
and is the only sentence in the section a reader cannot reconstruct from the
floats. It is two sentences, not a paragraph — and with §N3's finding removed
that is all it was ever owed.

### The specimen draft

Not committed to the tex. It exists so the shape can be judged from words rather
than from a description of words; Marc's hand or a voice pass follows.

> \emph{Network.} Fifty hosts across four levels of depth, eight subnets and
> five exposed endpoints, with the topology drawn fresh for each seed and the
> two database hosts at the deepest level as the target. Every run in this
> chapter takes place on it, so nothing reported here speaks to how these
> results move with network size or density.
>
> \emph{Attacker.} Two arms: the baseline attacker of
> Section~\ref{subsec:attacker-model}, and the movement attacker of
> Chapter~\ref{ch:attacker-model} on each of the four attack profiles and on the
> aggregate. Its cost model and its memory are implemented and not exercised;
> the model runs on its corpus-derived routing alone.
>
> \emph{Defender.} The simulator's own, in three clauses. Its goal is to disrupt
> the attacker, not to detect it; it knows nothing of the attacker, there being
> no detection channel for that knowledge to arrive through; its capability is
> the seven mechanisms of Section~\ref{subsec:defence-mechanisms}, on a
> time-triggered schedule it never departs from. MTDShield is not exercised. The
> conditions are no defence, each of the seven mechanisms deployed alone, and
> the two execution schemes that draw from all seven; no defence is the
> reference that every effect in this chapter is a difference from.
>
> \emph{Design.} Table~\ref{tab:factors-varied} gives every factor the
> experiments vary and Table~\ref{tab:factors-fixed} everything they hold.
> Attacker arm, defence condition and deployment interval are run in every
> combination; the interval distribution, the run length and the objective are
> each varied on their own from that grid. Both intervals are reported, and
> every claim in this chapter states the interval it was taken at.
>
> \emph{Metrics.} Table~\ref{tab:measures} names every metric the chapter
> reports, keyed to the families of Table~\ref{tab:mtd-metrics} so that what
> judges a defence here is the field's measure and not this thesis's. Distinct
> hosts compromised is the denominator throughout, because it responds at every
> interval, and target reach is reported beside it wherever it is not
> degenerate. The instruments of
> Section~\ref{sec:attacker-in-operation} are not metrics: they are read against
> no defence to establish that the model behaves as
> Chapter~\ref{ch:attacker-model} declared \citep{sargent2011}, and no defence
> is scored with them.
>
> \emph{Runs.} Every cell runs a thousand seeds, the count at which the closest
> pair of conditions this chapter compares separates~\citep{hoad2007}. The same
> seeds are used on every arm, but the two arms consume randomness differently,
> so no comparison across attackers is paired. Effect sizes are reported with
> 95\,\% intervals, which no evaluation in this lineage does. Tests attach to
> declared claims only, are adjusted within each family of comparisons, and each
> carries a minimum effect of interest fixed before the run, because on a
> simulator this cheap any difference can be made significant by adding seeds.

341 words against the landed 539 and the original 905, with the five answers
intact and one result removed.

## Q. The tables — what the *Why* columns keep and what they lose

The corpus does not settle this in one direction, and pretending it does would
be dishonest. Both sides, then the split that honours both:

- **Against a justification column.** Reti's paired tables — the closest
  analogue in the corpus, a titled Experimental setup with a varied table and a
  held table — are `Parameter · Description · Value` in *both*, with **no
  justification column at all** (Table 2 is nineteen rows, three columns). Kim
  justifies row by row but **quarantines it in a separate numbered sub-part**,
  §6.1.2, never in the table. Conventions §c: "Range justification is almost
  never given."
- **For one.** Conventions §h records Tay — the local genre, the form the
  examiner has seen — justifying every swept range against the literature's
  default as "the single most reusable move in the document", and §c notes that
  a dissertation deriving its bands from the model's own structure exceeds the
  corpus and should say so once.

**The split: vary and justify; hold and declare.**

| Table | Columns | Why |
|---|---|---|
| Table 5.2 (varied) | `Factor · Levels · Reason` — **keeps** the reason, cut to one clause and only where the level set is not self-evident | Tay's move, and the level sets are genuinely chosen (why 2 000 s, why an exponential regime) |
| Table 5.3 (held) | `Held fixed · Value` — **drops** the reason column entirely; provenance and version pins stay in the footnote | Reti's Table 2 exactly; Marc's read of the cells one by one; and it is the page this section can give back |

**Table 5.2 row-level repairs.**

- **The Levels cell becomes scannable.** Level *names* only, semicolon
  separated, no parentheticals and no glosses. The attacker-arm cell loses "(exfiltration,
  impact, double extortion, no realised objective)" — the reader met the four
  profiles in chapter 4 — and loses "the corpus left unpartitioned by objective"
  to the reason column. Marc: *"the points are already in the thing."*
- **The Jalowski citation leaves the table.** A citation in a setup table is an
  argument, and this one is already made where it belongs: properties 7
  (Learning) and 8 (Scheme awareness) of Table~\ref{tab:attacker-properties}
  carry `jalowski2026` in chapter 3. The cell says what the level is for; the
  reader has the warrant already.
- **Row-group labels.** Keep plain words — *In combination* / *One at a time* —
  and leave the design sentence in the caption. Marc floated "arms, single and
  combinatoric": *arm* is taken (the attacker arm is a row of this very table),
  and conventions §d's census found **zero attestation** for the DOE vocabulary
  anywhere outside this repo. There is no conventional term of art to reach for
  because the field never names the design; plain words are the field's answer.
- **The caption.** Currently four sentences and dumbed down ("Any result in this
  chapter is a cell of this table"). Cut to the design sentence and nothing
  else.

## R. The metrics table, and the question underneath it

**R1. Rename: *measures* → *metrics*.** Marc: *"measures, metrics — why not."*
The chapter's own scaffolding comment already says the strands are "clustered by
INSTRUMENTED METRIC FAMILY (Cho's purpose axis, Table 3.1)", so *metric* is the
word the structure is built on. One registry row (§S).

**R2. Re-cut it in Table 3.1's own grammar, so it is visibly a selection from
the field's map rather than a bespoke list.** Marc: *"consider what metrics can
we tie back into the metric table that we produced in the literature review."*
Table 3.1 (`tab:mtd-metrics`) is row-grouped by **purpose** (Effectiveness /
Efficiency) and columned by **perspective** (attacker-side / defender-side),
with an inner key naming **the quantity measured** (success events, attacker
time, resource spent, …). The chapter's §5.4/§5.5 split *is* that purpose axis.
So:

> `Metric · What it is · Comparable across`, row-grouped **Effectiveness** /
> **Efficiency**, with the inner key being the Table 3.1 family the metric
> instantiates (*success events*, *attacker time*, *resource spent*, …).

The join is then literal — the inner key column of Table 5.4 is the inner key
column of Table 3.1 — and the caption says so in one clause. `Read from` is
dropped as a column: it is "every condition" for most rows, and the exceptions
("no defence", "under defence") fold into the comparability cell. Twelve rows
become nine or ten once §5.3's four instruments leave (R3), which is most of a
page back.

**R3. The self-measurement question, which is the real one Marc raised.**

> *"If you're measuring your attacker model using your own metrics you can do
> anything with it … you could fudge numbers and selectively discriminate —
> that's the sort of issue you encounter when you have something separate like
> an attacker model."*

This is `voice.md` §(c)10 — *name the circularity risk, and show what
independent grounding breaks the loop* — and it is a standing gate, not a
passing worry. The structural answer is available and costs nothing:

1. **Nothing this thesis invented ever scores a defence.** Every metric in
   §5.4 and §5.5 keys to a Table 3.1 family with the field's citations already
   attached in chapter 3. That is what R2's inner key makes visible on the page.
2. **§5.3's four instruments are not metrics and leave the metrics table.**
   Campaign coverage, opening variety, profile divergence and response to
   disruption are **model-validation** instruments: they are read against no
   defence, they establish that the model behaves as chapter 4 declared, and
   they judge no defence. Sargent's taxonomy names this exactly — *operational
   validation*, "the model's output behaviour has sufficient accuracy for the
   model's intended purpose" — and `sargent2011` is already in the bibliography
   and already cited by §5.1. One sentence in **Metrics.** says it; the
   instruments go either in a short second table or in §5.3's own opening,
   where conventions §f says attacker-characterisation belongs.
3. **The separation is then a property of the document's shape**, not a promise:
   the two instrument sets live in different tables, are read from different
   conditions, and only one of them is the field's.

The current caption already asserts point 2 in a sentence. The change is to make
the shape carry it, so a reader cannot miss it and an examiner cannot suggest it
was retrofitted.

**R4. One thing to flag, not to decide.** Keying each metric to a Table 3.1
family makes the chapter's *coverage* of the ten families readable straight off
the table — which partly duplicates the five-of-ten headline Part 2 relocated to
ch6 `sec:evaluation-implications`. That is an improvement (the coverage becomes
visible without being argued in the setup), but ch6's paragraph should then read
as the *interpretation* of a table the reader has already seen, not as its first
disclosure. Raise it when the ch6 insertion is drafted.

## S. Terminology — three re-keys, one of them a live registry breach

Marc: *"what is timing regime — so that we can be more specific … horizon is a
bit of a buzzword."* Correct on both, and the first one turns up a breach of a
ratified row.

| Current | Proposed | Ground |
|---|---|---|
| **mutation interval** | **deployment interval** | `terminology.md` ratified (Marc, 2026-09-02): the defensive move as a scheduling event is a **deployment**; *MTD mutation* survives "only inside Zhang's cited phrasing". Census 2026-09-18: *mutation interval* 4 in ch5 (prose l. 5498/5500, and the captions of Figures 5.3, 5.4, 5.5); *deployment interval* 0 |
| **timing regime** | **interval distribution** | says what actually varies — the distribution the interval is drawn from, quasi-periodic against exponential at the same mean — instead of a category word. *Regime* names nothing a reader can check |
| **horizon** | **run length** | the simulation-methodology literature's own word (Hoad, Robinson and Davies; `docs/sources/methodology/`), where *horizon* is ours. Census: 2 occurrences in ch5 prose, 1 in an appendix table, 1 in ch1 ("over an extended time horizon", about the APT — a different sense, left alone) |

All three are added to `terminology.md` as PROPOSED rows in the same pass as
this brief, per the registry's own mechanism (a session meeting an unregistered
cluster proposes; Marc rules; nothing auto-substitutes).

**Not changed: *factor*.** Marc asked whether it is the right header word. It
is: Reti and Kim both use *Parameter*, which is wrong here because our levels
are arms and conditions rather than numbers, and *factor* is the plain word for
a thing with levels. The pairing to aim at is the two headers read together —
*Factor · Levels* against *Held fixed · Value* — which is Reti's paired-grammar
effect without borrowing a term.

## T. Rulings owed

| # | Question | Recommendation |
|---|---|---|
| R1 | Run-in labels in §5.2 — adopt? | **Yes**, italic (`\emph{Network.}`), He's form; one scoped carve-out written into `voice.md` §(h) |
| R2 | Six units — Network / Attacker / Defender / Design / Metrics / Runs? | **Yes**; *Design.* survives at two sentences because the cross-table relation is not a caption's to carry |
| R3 | The operating-point finding leaves §5.2 (inverts §H ¶3 / S6) | **Yes** — Marc's read; the declaration stays, the finding goes to §5.4 where it is evidenced and to ch6 for its reading |
| R4 | Table 5.3 drops its *Why it is held* column (inverts §D) | **Yes** — Reti's Table 2 is exactly this, and it is the page the section gives back |
| R5 | Table 5.2 keeps a reason column, cut to one clause | **Yes** — Tay's move, the local genre; but level names only in the Levels cell |
| R6 | The Jalowski citation leaves Table 5.2 | **Yes** — already carried by Table 3.2's properties 7 and 8 |
| R7 | Table 5.4 re-cut on Table 3.1's grammar (purpose row-groups, family inner key), renamed to metrics | **Yes** — the chapter's section structure is already that axis |
| R8 | §5.3's four instruments leave the metrics table and are declared as validation | **Yes** — it is the structural answer to the circularity question, and `sargent2011` is already cited |
| R9 | *deployment interval* / *interval distribution* / *run length* | **Yes** on the first (a ratified row is being breached); the other two are Marc's call |
| R10 | Bold instead of italic for the run-in labels | Marc's, if he wants the scan; it costs a second `voice.md` carve-out (§(d) "in LaTeX, `\emph` only") |

## U. Order of work

1. **Rulings** (§T). R1, R3, R4 and R8 are the load-bearing four; the rest
   follow mechanically from them.
2. **`voice.md` §(h) carve-out** — one row, scoped to declarative setup
   passages. Nothing else in `voice.md` moves.
3. **Re-cut the three tables** (§Q, §R) — mechanical, no prose, and the visible
   win. Measure the built page after, per the conventions' own rule.
4. **The prose** — the §P specimen into the tex, then Marc's hand or a voice
   pass.
5. **The four ch5 re-keys** for *deployment interval* (prose + three figure
   captions) in one commit, once R9 is ruled.
6. **Flag to the ch6 insertion brief** that `sec:evaluation-implications` now
   interprets a coverage the reader can already see (§R4).

## Validation gate (Part 3)

Parts 1 and 2 stand, plus:

- Six run-in units; no unit exceeds four sentences.
- Prose word count ≤ 380.
- No sentence in §5.2 reports an outcome of a run.
- Table 5.3 has two content columns; Table 5.2's Levels cells carry names only,
  no parentheticals.
- Every row of the metrics table names the Table 3.1 family it instantiates, and
  no §5.3 instrument appears in it.
- `grep` the section for *mutation interval*, *timing regime*, *horizon* — all
  absent once R9 is ruled.

---

# Part 4 — the structure (2026-09-18, second reply)

Marc's ruling on Part 3, and the answer to *"how would you structure experimental
setup — as simple and short as possible, following convention."* Two of Part 3's
recommendations are overturned by it, one of them mine from the same day.

## V. What changed in this reply

**V1. The labels are the simulation's moving parts, and they are bold.** Marc:
*"what would the dimensions be, because that's the moving parts of our
simulation — the defence, the attacker, the network, the metrics that we use,
the things that we keep the same."* That list is the section's structure, not a
formatting choice, and the emphasis is **bold** on his ruling — stronger than
Part 3's italic recommendation, and the carve-out covers both `voice.md` §(h)
and §(d) rather than one of them.

**V2. The reason column goes from *both* tables. OVERTURNS Part 3 §Q and §T/R5.**
Part 3 split it — vary and justify (Tay), hold and declare (Reti). Marc rejected
the split and the authority it rested on: *"I wouldn't use his as a main
argument … I would just lose the column on each of them, because what do I need
them for? It's very hard to be like, this is why we chose it."* What replaces it
is better and is his: **the motivation is one high-level clause per prose unit —
why we vary the attacker, why we vary the defence — and the tables just print
what is at our disposal.** A per-row justification answers a question no reader
asks; a per-dimension one answers the only one they do.

**V3. Three tables become two, because the three did not distinguish
themselves.** Marc: *"the distinction between each of the three tables is not
clear."* He is right, and the fix was already in this repo's own conventions
rather than in Reti's paired form. `evaluation_conventions.md` §c states the
rule outright:

> "every declared parameter is listed; each row says either the band it was
> swept over and what moved, or that it was held and why. **One register, both
> kinds of row.** A parameter that appears in neither list is the failure the
> corpus keeps committing."

One register, both kinds of row — that is **one table**, not two. Reti's pair
reads as a pair only because its columns are identical, which is a workaround
for what a single table does natively; Kim's Table 4 is a single parameter table
with a Type row-group and is the closer precedent. So: **one setup table, one
metrics table.**

**V4. §5.3's four instruments leave §5.2 altogether, and are not called
validation.** Marc: *"it does seem like fudging the numbers in terms of model
validation, because you can be selective about it — that's the whole issue. But
if you want to say we did some little validation, here's the numbers, and we
have some juice to talk about in the discussion, then we can do that."* He is
naming a real limit on Part 3's §R8: *validation* is a claim of proof, and a
self-chosen instrument set cannot carry it. Conventions §f already gives the
honest word and it is his shape exactly:

> "attacker-property claims are legitimate results, they are taken from the
> no-defence arm, and they are reported in the results chapter as
> **observations**. The **verdict** they add up to belongs in the discussion."

So §5.3 **characterises** the attacker against no defence; §5.2 does not carry
its instruments at all (conventions §a: a parameter is declared where it is
first used); and what they add up to is ch6's. `sargent2011` is then cited once,
for its *ceiling* — an unobservable system does not admit a high degree of
confidence — not for a licence.

## W. The structure

**Five bold run-in units, two tables** (~330 words predicted; 450 measured once built — see below). One opening sentence for the
setup table, then the four moving parts and the replication.

| Unit | What it declares | Its one motivating clause | Words |
|---|---|---|---|
| — (lead) | Table 5.2 and how to read it | — | ~25 |
| **Network.** | geometry, topology, target; the negative scope | held so a difference is the attacker's or the defence's, not the ground's | ~55 |
| **Attacker.** | the two arms, the objective, the declared absences | because the question is whether the choice of attacker changes what an evaluation concludes | ~65 |
| **Defence.** | the ten conditions, no defence as reference, the defender's three clauses | because *when* a defence moves is as much a design choice as *which* moves | ~95 |
| **Metrics.** | Table 5.3, keyed to Table 3.1; the backbone denominator | because what judges a defence here should be the field's measure, not this thesis's | ~55 |
| **Runs.** | Barach's four sentences | — | ~80 |

No *Design.* unit: with the reason columns gone and both kinds of row in one
table, the design is one sentence in that table's caption, which is where
Part 3 §P could not yet put it.

### The specimen

Not committed to the tex.

> Table~\ref{tab:experiment} states the experiment: every element of the
> simulation, with either the levels it varies over or the value it is held at.
>
> \textbf{Network.} Fifty hosts across four levels of depth, eight subnets and
> five exposed endpoints, the topology drawn fresh for each seed, and the two
> database hosts at the deepest level as the target. It is held for every run in
> this chapter, so that a difference between runs is the attacker's or the
> defence's and not the ground's. Nothing reported here speaks to how these
> results move with network size or density.
>
> \textbf{Attacker.} Two arms, because what this chapter asks is whether the
> choice of attacker changes what an evaluation concludes: the baseline attacker
> of Section~\ref{subsec:attacker-model}, and the movement attacker of
> Chapter~\ref{ch:attacker-model} on each of the four attack profiles and on the
> aggregate. Its objective is varied with them, since a defence that denies one
> goal need not deny another. Its cost model and its memory are implemented and
> not exercised.
>
> \textbf{Defence.} Ten conditions: no defence, each of the seven mechanisms
> deployed alone, and the two execution schemes that draw from all seven. No
> defence is the reference that every effect in this chapter is a difference
> from. The interval and the distribution it is drawn from are varied as well,
> because when a defence moves is as much a design choice as which defence
> moves. The defender itself is the simulator's own: its goal is to disrupt the
> attacker, not to detect it; it knows nothing of the attacker, there being no
> detection channel for that knowledge to arrive through; and its capability is
> the seven mechanisms, on a time-triggered schedule it never departs from.
>
> \textbf{Metrics.} Table~\ref{tab:metrics} names every metric this chapter
> reports against the family of Table~\ref{tab:mtd-metrics} it instantiates, so
> that what judges a defence here is the field's measure and not this thesis's.
> Distinct hosts compromised is the denominator throughout, because it responds
> at every interval, and target reach is reported beside it wherever it is not
> degenerate.
>
> \textbf{Runs.} Every cell runs a thousand seeds, the count at which the
> closest pair of conditions this chapter compares separates~\citep{hoad2007}.
> The same seeds are used on every arm, but the two arms consume randomness
> differently, so no comparison across attackers is paired. Effect sizes are
> reported with 95\,\% intervals, which no evaluation in this lineage does.
> Tests attach to declared claims only, are adjusted within each family of
> comparisons, and each carries a minimum effect of interest fixed before the
> run, because on a simulator this cheap any difference can be made significant
> by adding seeds.

**Measured after execution: 450 words, against the 546 that stood here and 905 originally.** The ~330 predicted above was an undercount of this specimen — both figures are now counted by the same script with references expanded as a reader reads them, and the executed section is the number that stands.

### Table 5.2 — the experiment

`Element · Varies over · Held at`, row-grouped by the moving part. A row is in
one value column or the other, never both; an empty cell is the genre's own mark
for absent (conventions §e1). The varied rows read down one column, so the
experiment is visible as a shape rather than described as one.

| Group | Element | Varies over | Held at |
|---|---|---|---|
| **Network** | Geometry | | 50 hosts, 5 exposed endpoints, 8 subnets, 4 levels |
| | Topology | | drawn fresh for each seed |
| | Target | | the two database hosts, at the deepest level |
| **Attacker** | Arm | the baseline attacker; the movement attacker on each of the four attack profiles; the movement attacker on the aggregate | |
| | Objective | targeted; opportunistic | |
| | Declared inputs | | Table 5.1's values |
| | Sink retrace | | on |
| | Cost model, memory | | off |
| **Defence** | Condition | no defence; each of the seven mechanisms alone; the random and alternative execution schemes | |
| | Deployment interval | 200 s; 2 000 s | |
| | Interval distribution | quasi-periodic; exponential, same mean | |
| | Deployment durations † | | 20–110 s, per mechanism |
| | Confusion penalty † | | 20 s per interrupted action |
| | Adaptive selector | | not exercised |
| **Run** | Run length | 15 000 s; 60 000 s | deployments per run |
| | Seeds | | 1 000 per cell, the same set on every arm |

Caption: *Every element of the experiment: what it varies over, or the value it
is held at. Attacker arm, defence condition and deployment interval are run in
every combination; objective, interval distribution and run length are each
varied on their own from that grid, with the first three at their first level.*
Plus the existing dagger and version footnote, unchanged.

Geometry, tested: `@{}cP{2.6cm}P{5.6cm}P{5.2cm}@{}` at `\tabcolsep` 4 pt, no
overfull box.

### Table 5.3 — the metrics

`Family · Metric · What it is · Comparable across`, row-grouped
**Effectiveness** / **Efficiency**. The *Family* column is Table 3.1's own inner
key, so the join to the literature review is literal rather than asserted, and
the four §5.3 instruments are gone (V4). Twelve rows become eight.

Geometry, tested: `@{}cP{2.0cm}P{2.8cm}P{5.0cm}P{2.7cm}@{}`, no overfull box.

**One row to rule, not to decide silently.** *Deployment tempo* (deployments per
thousand seconds) is MTD execution frequency, which Table 3.1 files under
**Effectiveness** / network-state change; this chapter reports it in §5.5 as a
cost. Either the row sits in Effectiveness against the section that reports it,
or it sits in Efficiency against a family it does not belong to. Recommendation:
**keep it in Efficiency and say in the caption that the grouping is by the
section that reports the metric, not by Cho's filing** — the divergence is then
declared rather than hidden, and it is a legitimate point for ch6.

## X. The footprint, measured

Built both sets against the real class and geometry (`\textwidth` 455.24 pt,
`\textheight` 702.78 pt) and measured the tabular boxes rather than estimating:

| | Table bodies | As a page |
|---|---|---|
| Current three tables | 331 + 367 + 469 = **1 168 pt** | 1.66 pages |
| Proposed two | 427 + 283 = **710 pt** | 1.01 pages |

With the prose at 333 words against 539, **§5.2 goes from roughly three pages to
roughly one and a half**, and from three floats to two. The saving is not the
point but it is the measurable form of the complaint.

## Y. The standing instruction this reply carries

Marc, verbatim: *"just rule on merit — don't rule on what would exist prior,
unless it's very very recent, because some rulings can get stale and some
rulings can be made in not the best conditions."*

This is a working rule and it applies past §5.2. A ratified row, a landed
ruling or a convention file is **evidence**, not authority: where it was ruled
under different conditions, or where the current reading of the page contradicts
it, the recommendation is made on merit and the prior ruling is named as the
thing being overturned. Parts 3 and 4 both do this — §N3 and §N4 overturned
Part 2, and §V2 overturns Part 3 — and that is the intended behaviour, not drift.

The mechanical consequence for this brief: `voice.md` §(d) and §(h) are July's
and §(d) is described in that file as its "most provisional layer"; they get a
carve-out rather than a veto (§V1).

## Z. Order of work, revised

1. **Ruling on §W's structure** — five bold units, two tables. Everything else
   is mechanical from it.
2. **`voice.md` carve-out** — one row covering §(h) and §(d), scoped to
   declarative setup passages.
3. **Build the two tables** — `tab_5-2a_experiment.tex` and
   `tab_5-2b_metrics.tex`; `tab_5-2c_measures.tex` deleted, `tab_5-2b_factors_fixed.tex`
   and `tab_5-2a_factors_varied.tex` retired into them. `FLOATS.md` in the same
   commit (conventions §j).
4. **The prose** — §W's specimen into the tex.
5. **§5.3's opening** gains the four instruments it now declares for itself.
6. **The re-keys** — deployment interval, interval distribution, run length —
   once §S's rows are ruled.

## AA. What landed (2026-09-18, executed)

Steps 1–5 of §Z are done; step 6 (the terminology re-keys in the §5.4/§5.5
captions) waits on the ruling in §S.

| Artefact | State |
|---|---|
| §5.2 prose | **Restructured** to §W. Five bold run-in units — *Network / Attacker / Defence / Metrics / Runs* — under one lead sentence. **450 words** against the 546 that stood there and 905 originally, counted by the same script on both. No *Design* paragraph: the design is one sentence in Table 5.2's caption. No result reported |
| `tab_5-2a_experiment.tex` | **New.** `Element · Varies over · Held at`, sixteen rows in four row groups (the moving parts), each element in one value column only. Replaces `tab_5-2a_factors_varied` and `tab_5-2b_factors_fixed`, both deleted. The justification column is gone |
| `tab_5-2b_metrics.tex` | **New.** `Family · Metric · What it is · Comparable across`, eight rows in two groups; the *Family* cells are Table 3.1's own inner key. Replaces `tab_5-2c_measures`, deleted. The four §5.3 instruments removed |
| `voice.md` | **Carve-out added** to §(d) and §(h): bold run-in labels licensed in declarative passages only, with the corpus attestation and the scope clause |
| `terminology.md` | Four PROPOSED rows (§S). *deployment interval* applied in the new artefacts, since it enforces a ratified row ch5 had breached; *interval distribution* and *run length* applied in the new text only |
| §5.3 | **Comment placed** at the section head: it now owes the declaration of its four instruments, in conventions §f's register (observations from the no-defence arm; the verdict is ch6's) |
| `FLOATS.md` | Both rows re-keyed |
| Build | `pdflatex` clean, 92 pages (from 93), no undefined references or citations. §5.2 spans pp. 41–43 |

**Three defects found by reading the built page, and fixed.**

1. **The rotated group labels were not centred.** Fixed with multirow's
   `[vmove]`, and the values are *measured* rather than eyeballed: each page was
   rasterised, the label's pixel span compared against its group's rule
   boundaries, and the offset solved in one step. All six labels now sit within
   two pixels of their group's midpoint (Network $-0.52$, Attacker $-0.13$,
   Defence $+0.76$, Run $-0.28$, Effectiveness none, Efficiency $+0.18$ cm).
   The offsets differ per group because multirow estimates a group's height from
   `\baselineskip` and the error grows with the number of wrapped lines in it.
2. **One row filled both value columns**, contradicting the caption's "each
   element appears in one of the two columns only". *Run length* carried
   "deployments per run" in the held column; split into two rows.
3. **The floats drifted past the §5.3 heading** at `[htbp]`, because §5.3 is
   still a placeholder and offers nothing for a float to settle against.
   `[H]` was tried first — the fix Table 5.1 took — and stranded two thirds of a
   page as whitespace, exactly as the preamble's own note warns. Fixed instead by
   moving Table 5.2's `\input` up to its reference at the lead sentence, which
   places both tables in order with no gap.

**One dangling reference this restructure created, found by the build and
fixed:** `tab_5-4-2a_orderings.tex`'s footnote referenced `tab:factors-fixed`
for the seed count. Re-pointed at `tab:experiment`. The rider it sits in
("ranks within a family are not separable at this seed count") is a hundred-seed
statement that the thousand-seed ruling deletes — **flagged, not changed**: that
is §5.4's prose and its floats are still hundred-seed floats.

**Two things to know about the state of the repo.** The §5.2 tex reached `HEAD`
inside a **concurrent session's commit** (`5f23b9f1`, a §4.4.2 compression),
which staged `dissertation.tex` while this work was mid-flight — so for a while
`HEAD` referenced two table files that were not tracked and would not have
built. Committing them closes that. And `\citet{jalowski2026}` raises a natbib
"Author undefined" warning in ch4: `ieeetr.bst` is a numeric style that records
no author, so `\citet` cannot render one. **Pre-existing, not from this work,
and worth its own look** — it affects every `\citet` in the document.

**Still owed:** the C39 generator pass, now over two tables rather than three;
§5.3's declaration of its four instruments; the three §5.4/§5.5 caption re-keys
once §S is ruled; the effect floors; the ch6 insertions' prose.

## AB. The opening sentence (2026-09-18, third read)

Marc, on the lead: *"it reads like a caption — it basically is the caption for
Table 5.2. What is this first sentence doing before we devolve into network,
attacker, et cetera?"* Correct, and the corpus settles it rather than taste.

**The evidence.** Of the four setup sections with an anatomy on file, **not one
opens by introducing its own parameter table.** Kim opens on the testbed, Reti
on the network configuration, Ho on the simulator settings, He on the dataset;
the parameter table is referenced where its content is discussed (Kim's Table 4
in §6.1.2, Reti's Tables 1–2 in the parameter prose). A setup section opens on
its first object, not on its float.

**What the sentence is for, and the three ways to answer it.**

| | Lead | What it does | Cost |
|---|---|---|---|
| 1 | delete it; start at **Network.** | corpus-exact | Table 5.2 loses its prose reference, and the reader meets a bold label with no frame |
| 2 | **the experiment in one breath** — *one network, two attackers and ten defence conditions, run at two tempos and repeated a thousand times in every cell; its values are in Table 5.2* | says the one thing no unit and no caption says: the **size** of the experiment. Makes the five labels a walk of an announced enumeration (voice.md §c2) rather than a listicle. The table becomes a plain pointer | one sentence of overlap with the units that follow |
| 3 | the scope sentence — *every number in this chapter comes from one experiment* | frames the chapter | closer to signposting than declaration; voice.md §h territory |

**Taken: option 1 — cut (Marc, same read: "no, I think it's better, just cut it").**
Option 2 was drafted and built first; on the page it still read as a summary of
what the units were about to say, and the corpus's own form is to open on the
first object with nothing in front of it. The section now begins
*"\textbf{Network.} Fifty hosts across four levels of depth…"* directly under the
heading. Table 5.2 keeps a reference without a sentence spent on it: a
parenthetical pointer at the first value it holds, which is Kim's and Reti's
pattern — values in the prose, the table alongside.

**The same fault was in the Metrics unit and was not flagged.** It opened
"Table 5.3 names every metric this chapter reports against the family of
Table 3.1 it instantiates" — a caption again. Re-cut so the claim leads and the
table is subordinate: *"What judges a defence here is the field's measure and
not this thesis's: every metric this chapter reports is keyed in Table 5.3 to
the family of Table 3.1 it instantiates."* The other four units already open on
substance and are unchanged.

Section now **428 words**, against the 546 that stood there before the restructure. Build clean, 92 pages; §5.2 spans pp. 41–43 with both tables in order.

## AC. The Network unit (2026-09-18, fourth read)

Marc's three questions on it, answered against the corpus and the code.

**AC1 — does it want a diagram? No, it wants a cross-reference.** Two of the
four setup sections on file carry a testbed figure (Kim's Fig. 4, He's Fig. 3)
and two do not (Reti, Ho) — and the split is not stylistic: Kim and He describe
their environment nowhere else, while Reti's and Ho's are declared elsewhere.
This thesis is the second case. §2.2.1 already draws the network, at three
magnifications, in Figure 2.2. A §5.2 figure would redraw it. What the unit was
missing is the pointer, and it was missing it *inconsistently*: **Attacker**
referenced §2.2.3 and **Defence** §2.2.2, while **Network** referenced nothing.
Now it references both the section and the figure.

**AC2 — is the negative scope a necessary qualification here? No, and it is in
the wrong place three times over.** It is a true limitation and it is now an
insertion at `sec:fidelity-verdict` (item 3, alongside the two relocated on
2026-09-17). The reasons it leaves §5.2:

1. Table 5.2 already declares the geometry held, so the sentence restated the
   table in an apologetic register.
2. A setup declares and does not concede — the principle the whole section was
   rebuilt on (§G). It would have been the one surviving concession of the six.
3. `voice.md` §c6 wants negative scope "as a section or a closing move", and the
   corpus agrees: Reti flags its step limit in the **conclusion**.

**AC3 — what a Network unit must carry.** The four anatomies give four slots:
*what the environment is, concretely*; *where it came from or how it was
generated*; *what in it is the target*; *how many configurations*. The unit had
the first, third and fourth. It was missing the second — and that is the slot
the cut sentence's place was given to.

**What filling it turned up, and it is a finding rather than a phrasing.**
`GEOMETRY` (`src/mtdsim/l3_simulation/movement/run.py:61-69`) is
`TimeNetwork`'s own default for **every value except one**: total nodes 50,
endpoints 5, subnets 8, layers 4, target layer 4 and the compromise ratio 0.8
are the class's defaults (`mtdnetwork/component/time_network.py:11-13`), while
**the database set is 2 against a default of 5**. So the terrain is the
simulator's, unchanged but for the size of the target set — which is a stronger
thing to be able to say than the sentence it replaced, because it closes at the
terrain level the question a sceptical reader asks of any evaluation whose
contribution is the attacker: *was the network chosen to suit the model?* It was
not; it is the one that came with the simulator.

The narrowing itself is **real, verified, and declared nowhere in the
document** — the probe records note the value (`targeted_objective_probe.md`
§1) but no reason is recorded anywhere. A `[3b]` now stands at the sentence:
the fact is stated, the reason is Marc's. It is worth resolving rather than
leaving, since a target set that departs from the simulator's default is
precisely what a reader checks.

Network unit: three sentences to two, and the section is **438 words**.

### AC4 — the polish pass on the unit (same read)

Marc: *"why is that sentence so long ... it is held for every run in this
chapter — of course it is, that's the experimental setup, so why do we have that
qualifier ... it's not sharp, it's not polished."* Three faults, three fixes.

| Fault | Fix |
|---|---|
| **One sentence carried four jobs** — provenance, the divergence, the holding, and the reason for holding | Split into three: the values, the provenance, the purpose |
| ***topology* was the wrong noun.** "the topology drawn fresh for each seed" — what is redrawn is the network; the topology is one of its properties | "with the network regenerated for each seed", which is Marc's own word for it |
| **"it is held for every run in this chapter" is a statement of the obvious** and Table 5.2 says it in a column. What is *not* obvious is why it is held | The holding is dropped as a statement and kept only as the subject of the purpose sentence: *"The configuration never changes across this chapter, so every difference reported is the attacker's or the defence's."* Marc's own framing: "we kept the network the same, we used all the default values, so that any differences ... we could measure objectively" |

The shape now follows `voice.md` §d — "long sentences are allowed when
controlled; verdict sentences are short. After a long build, land on a short
one" — at 38 / 22 / 17 words, and the divergence is carried by the file's
signature paired opposition rather than by a subordinate clause: *"Every value
is the simulator's own default but one: the target set."*

**Not changed, but the same fault is in the Attacker unit.** It opens *"Two
arms, because what this chapter asks is whether the choice of attacker changes
what an evaluation concludes: the baseline attacker of §2.2.3, and …"* — the
motivation is spliced in before the two arms have been named, which is the
Network unit's fused-sentence fault in a different order. The naming should
land first and the motivation after it. Flagged for Marc's read rather than
changed, since he is working through the units one at a time. The Defence,
Metrics and Runs units do not show it.

Section is **433 words**.

## AD. The Attacker unit (2026-09-18, fifth read)

### AD1 — what an Attacker unit must carry

The four anatomies' *attacker model / scenarios* slot gives four things, and
only three of them belong in a setup:

| Slot | Attested | Ours |
|---|---|---|
| **Which attackers are run** | all four (Reti's three named agents; Kim's one scenario; Ho's one adversary; He's three knowledge levels) | the two arms |
| **What varies about them** | He (knowledge level, four delays); Reti (three agents) | the profiles, the aggregate, the objective |
| **Where each is defined** | He's §III.A, Kim's §5.2 | §2.2.3 and Chapter 4 |
| **What of the attacker is switched off** | **weakly attested in setup** — He states a capability bound inside its *model* section; Ho owns its single-adversary limitation in §5.1, not in the setup | was in the prose; **now the table's alone** |

So the declared absences leave the prose. Table 5.2 already carries them
(*Cost model, memory · off*), and a prose clause that repeats a table cell is
the same fault the Network unit's "it is held for every run" had.

### AD2 — the clause that was not merely redundant but wrong

The removed sentence read: *"the model runs on its corpus-derived routing
alone."* Marc: *"yes it does not, because we inputted our own [structure] which
we talk about in the model description."* **He is right, and §5.2 was
contradicting its own Table 5.1 two paragraphs earlier.**

- Table 5.1's caption is *"Each value the attacker model was **given rather than
  derived**"* — the dwell times, the failure matrix, the distance kernel and the
  nine failure rules are argued or declared values, not mined ones.
- The profile nets carry a **pre-intrusion overlay** (`terminology.md`, ratified
  2026-08-17): structure added because the corpus does not record it.

The routing is therefore corpus-derived **plus** declared inputs **plus** added
pre-intrusion structure. "Corpus-derived routing alone" overclaims the
derivation, and it is the exact claim the badge ceiling exists to stop. Deleted
rather than repaired: the honest version of it is Chapter 4's to make, and
Chapter 4 makes it.

### AD3 — the shape

Same three-sentence shape as the Network unit, and the fused opener Marc flagged
(*"Two arms, because what this chapter asks is whether …"*, motivation spliced in
before the arms are named) is unspliced: the arms land first, what varies second,
the purpose last.

> **Attacker.** Two arms: the baseline attacker of Section~2.2.3, and the
> movement attacker of Chapter~4 on each of its four attack profiles and on the
> aggregate. Their objective is varied as well, since a defence that denies one
> goal need not deny another. Whether that choice changes what an evaluation
> concludes is the chapter's question.

33 / 18 / 12 words, against 85 in three lines. Section is **411 words**.

### AD4 — the last clause was the research question, and it is cut

Marc: *"what is the last clause doing here … is this convention?"* It is not.

*"Whether that choice changes what an evaluation concludes is the chapter's
question"* is the study's question restated inside the run plan. **No setup
section in the corpus states its study's question** — Reti, He, Kim and Ho each
declare and stop; conventions §a is explicit that a setup declares and does not
argue; and §b puts the question-naming roadmap at the head of the **results**,
which for this chapter is the preamble. §20.1 of the design record had already
ruled that §5.2 must not repeat the roadmap, and this was that rule broken in a
single sentence.

**The distinction that keeps this from being over-applied.** The Network unit's
third sentence — *"the configuration never changes across this chapter, so every
difference reported is the attacker's or the defence's"* — is a **design
reason**, and design reasons are setup. This one was a **research question**.
The Attacker unit keeps its design reason in sentence two, where Marc ratified
the wording ("a defence that denies one goal need not deny another"), so nothing
motivating is lost by the cut.

The two objective levels are now named in the prose as well
("targeted and opportunistic"), for the same reason the Network unit names its
values: the unit's job is to state the configuration, and the table is the
reference rather than the substitute.

> **Attacker.** Two arms: the baseline attacker of Section~2.2.3, and the
> movement attacker of Chapter~4 on each of its four attack profiles and on the
> aggregate. Their objective is varied as well (targeted and opportunistic),
> since a defence that denies one goal need not deny another.

**One thing the cut hands to the chapter preamble, flagged in place.** With that
sentence gone, nothing in §5.2 says *why* two attackers are run. That is the
roadmap's job under Tay's house pattern, the preamble is still a placeholder,
and §5.4.2's figure caption is currently the only place the comparison's purpose
is stated ("this is the chapter's central comparison"). It needs to be in the
preamble when that is dictated.

Section is **396 words**, from 546.

## AE. The Defence unit (2026-09-18, sixth read)

### AE1 — what a Defence unit must carry

The four anatomies' *defence conditions* slot gives five things, and one of them
is not a setup's:

| Slot | Attested | Ours |
|---|---|---|
| **The conditions** — which defences run, combinations included | all four (Kim's five MTD systems; Ho's four techniques plus AnyMTD; He's FM/MP/DM; Reti's on/off) | the ten |
| **The no-defence reference, named** | Kim ("No-MTD", defined operationally), Ho ("trials with no MTD deployment will be run"), He ("vanilla Kitsune"); Zaffarano makes it definitional (conventions §f2) | one sentence |
| **When it moves — the scheduler and its interval** | Kim ("time-based, all techniques triggered every MTD interval"), Ho (the controller and its forced-trigger guard, interval swept 50/100/200) | the interval, its distribution, and the time-triggered regime |
| **Where the defences are defined** | Kim's §5.3, He's §IV.B | §2.2.2 |
| **The defender's Goal / Knowledge / Capability** | **He only — and in §IV.A, its *defence model* section, not in §V's setup** | **cut** |

### AE2 — two of the defender's three clauses were repeating chapter 2

Marc: *"this is a limitation which exists in the discussion maybe … that exists
already somewhere else in the background."* Right, and the second half is
checkable: §2.2.2 already closes *"There are no purely reactive deployment
strategies in the simulator: no detection channel is encoded, so a
detection-triggered strategy, such as an IDS-based scheme, is not possible."*
§5.2's *"it knows nothing of the attacker, there being no detection channel for
that knowledge to arrive through"* was ch2 restated in ch2's own terms, and the
goal clause ("disrupt, not detect") follows from the same fact.

**What stays is the scheduling regime**, because that is a run-plan fact and the
corpus puts it in the setup — Kim and Ho both declare their scheduler there. The
goal and knowledge clauses are model, and the one paper that writes them puts
them in its model section.

### AE3 — the answers to the three wording questions

- **Is *condition* the right word? Yes.** It is the corpus's own — He's three
  techniques are "treated as the compared conditions", Ho and Kim use it the
  same way — and it is the neutral experimental term for a level of the factor
  the chapter varies. It is also the table's row name, so prose and table agree.
- **Number them 1, 2–8, 9–10? No.** No paper in the corpus numbers its
  conditions in prose; all name them. The arithmetic Marc wanted is already
  carried by the count plus the three groups in that order, and Table 5.2's
  Condition cell lists them a second time. Numbering would be a third statement
  of one list.
- **"No defence is the reference that every effect in this chapter is a
  difference from"** — Marc: "a tough sentence, poorly written". Replaced with
  the active form, which is also closer to Zaffarano's own: *"Every effect this
  chapter reports is a difference from the no-defence runs."* 25 words to 12.

### AE4 — the unit

> **Defence.** Ten conditions: no defence, each of the seven defence mechanisms
> deployed alone, and the two execution schemes that draw from all seven
> (Section~2.2.2). Every effect this chapter reports is a difference from the
> no-defence runs. The deployment interval and its distribution are varied as
> well, since when a defence moves is as much a design choice as which one
> moves; either way it is time-triggered, and reacts to nothing the attacker
> does.

Three sentences at 33 / 12 / 36 against four at 110, and the last two clauses
are fused because both are about *when* the defence moves. The prose now uses
the table's own element names — *deployment interval*, *its distribution* — so
the two read as one object.

### AE5 — two things this hands on, flagged in place, neither drafted

1. **§2.2.2 owes the defender's half of the threat model.** Conventions §g asks
   for it symmetrically on both sides, He's Goal / Knowledge / Capability being
   the tightest form. Chapter 4 is the attacker's half in full; the defender's
   exists only as scattered facts. Three clauses at §2.2.2 would discharge it,
   and §5.2 would go on pointing at them as it now does.
2. **The reason MTDShield is not exercised is now recorded nowhere.** Dropping
   the tables' reason column took it with it: Table 5.2 declares the absence
   ("Adaptive selector · not exercised") but no longer says why, while ch2's
   Table 2.5 puts MTDShield in a roster of five this chapter runs none of. It is
   a limitation paired with its future work — He's form, ch7's register — and
   it should land there rather than return to the setup.

Section is **350 words**, from 546.

### AE6 — the second pass on the unit, and why it was awkward

Marc: *"I didn't understand everything after 'the deployment interval and its
distribution are varied as well'."* He was reading it correctly. Two unrelated
facts had been fused into one sentence on the strength of an antithesis that
obscured both — a "long controlled sentence" that was neither.

> **Defence.** Ten conditions: no defence, each of the seven defence mechanisms
> deployed alone, and the two execution schemes, random and alternative, that
> draw from all seven (Section~2.2.2). The no-defence runs are the reference:
> every effect this chapter reports is a difference from them. The deployment
> interval and its distribution are varied as well, since a defence is as much
> when it moves as what it moves; every deployment is time-triggered.

| Was | Now | Why |
|---|---|---|
| "since when a defence moves is as much a design choice as which one moves" | "since a defence is as much when it moves as what it moves" | the pairing is **ch2's own vocabulary**, which the reader has already met: Table 2.2 is headed *"**What** to move"* and §2.2.2 closes a paragraph with *"That is the when not to move."* The motivation lands because it is not new language |
| "either way it is time-triggered, and reacts to nothing the attacker does" | "every deployment is time-triggered" | the non-reaction is ch2's already ("no detection channel is encoded"). *Time-triggered* still earns its place: it is what separates these ten from MTDShield, which ch2 classifies as hybrid. **And note the correction**: "all ten conditions are time-triggered" would be **false** — one of the ten deploys nothing |
| the two schemes unnamed | "random and alternative" | Marc had to reach for the names while reading. Same rule as the Attacker unit's two objectives: the unit states the configuration, the table is the reference rather than the substitute |

### AE7 — why that sentence was awkward in the first place: *baseline* is unavailable

Marc, on *"every effect this chapter reports is a difference from the no-defence
runs"*: *"that could still be worded better — a difference from the baseline."*
The obvious word is the one word this chapter cannot use.

`evaluation_conventions.md` §f2: the corpus uses **baseline** for two different
objects — the **no-defence control** (Zaffarano's "runs with no MTD deployed
represent a baseline run"; Brown's "No MTD control group") and the **comparison
arm** (the prior model the contribution is set against). And: *"A chapter that
says 'the baseline' without saying which will be read as confusing a control
with a competitor."* The Attacker unit, two paragraphs above, says **the
baseline attacker**. So in this chapter the no-defence condition takes
**reference** and never *baseline* — here or anywhere. The sentence now names
the role before it uses it (*"The no-defence runs are the reference: every
effect this chapter reports is a difference from them"*), which is the clean way
to say it without the taken word.

### AE8 — *condition* re-examined on merit, not on convention

Marc asked twice, so it is worth the second look rather than a second citation.
The noun has to cover a control, seven mechanisms and two schemes at once.

- ***mechanism*** — wrong by extension: two of the ten are schemes and one is
  nothing.
- ***configuration*** — **taken.** The Network unit says *"the configuration
  never changes across this chapter"*. One word, two objects, one section apart.
- ***condition*** — covers a control and its treatments, which is the whole
  point of the word; it is the corpus's own (He's techniques are "the compared
  conditions"); and it is Table 5.2's row name, so prose and table agree.

It survives on merit, and the collision with the Network unit is the reason that
was not visible the first time.

Section is **347 words**.

---

## §AF — The Defence unit, third pass (2026-09-18)

Marc's read, in his words: the first sentence is "poorly constructed ... a hard
run through"; "the no defence runs are the reference, every effect this chapter
reports is a difference from them" is "so verbose when it doesn't need to be ...
it could just be one clause"; "a defence is as much when it moves as what it
moves — what does that point even mean to your average reader? I would cut it";
"every deployment is time-triggered — of course it is, it's in the background".
He also asked two naming questions: *MTD mechanisms* or *defence mechanisms*, and
whether the covering noun should be *MTD configurations*.

**Before → after.**

> Ten conditions: no defence, each of the seven defence mechanisms deployed
> alone, and the two execution schemes, random and alternative, that draw from
> all seven (§2.2.2). The no-defence runs are the reference: every effect this
> chapter reports is a difference from them. The deployment interval and its
> distribution are varied as well, since a defence is as much when it moves as
> what it moves; every deployment is time-triggered.

> Ten conditions: no defence, each of the seven defence mechanisms deployed
> alone, and the random and alternative execution schemes, which draw on the
> whole pool (§2.2.2). Each defended condition runs at both deployment intervals,
> and the interval distribution is varied separately (Table 5.2). The no-defence
> runs are the reference for every effect this chapter reports.

75 words → 54; the section 346 → 332, counted like for like
(`scratchpad/count52.py`, references expanded as a reader reads them).

**1. What made sentence one a run-through was its tail, not its length.** "The
two execution schemes, random and alternative, that draw from all seven" holds an
appositive open while a relative clause lands on a head noun two commas back, and
then ends on a bare number whose noun was never supplied — Marc read it exactly
that way ("all 7 — all 7 what?"). The names are now attributive and one clause
hangs off one noun. **The missing noun is *the pool*, and it is ch2's own**:
Table 2.3 says random "draws one mechanism from the pool at random" and
alternative "rotates through the pool in a fixed order". With the pool named the
number needs no repeating.

**2. Defence mechanisms, not MTD mechanisms.** §2.2.2 is titled "Defence
mechanisms" and Table 2.2 is "The seven defence mechanisms"; the document census
is 36 *defence mechanism* against 7 *MTD mechanism*, and **all seven of those are
generic** — the field's mechanisms in §1.1, §2.1 and §3.2, never this roster. The
acronym in ch5 would do work the noun already does. **"MTD configurations" is
rejected on merit**: a configuration is a setting of the *network*, which is how
the Network unit four lines above uses the word.

**3. The reference sentence said *reference*, then glossed it.** The colon and
the gloss go; 18 words → 12.

**4. Both motive clauses are cut.** The chiasmus was assembled from ch2's "*what*
to move" / "*when* to move" headings, and a figure that needs the headings in
front of you to parse is not a motive — Marc could not read it, which settles it.
The Network and Attacker units carry one motive clause each, and that is the
ration for a setup that conventions §a says declares rather than argues.
"Time-triggered" goes for his reason, that it is background: Table 2.3 files
random and alternative under the **proactive** regime, §2.2.2 states no detection
channel is encoded, and Table 5.2 declares the adaptive selector not exercised.
Three places already carry it.

**What replaces them is the fact they were decorating** — the interval is swept,
and the prose now says how, which Table 5.2's caption alone had been carrying.

**The truth condition, and it is the same trap as last pass.** "Every condition
runs at both deployment intervals" would be **false**: the no-defence cell never
reads the interval, so it is run once per arm and objective and serves as the
reference at both (`run_corpus.py:257-260`, and its module docstring says so).
Hence "each **defended** condition". Last pass the same shape made "all ten
conditions are time-triggered" false, because one of the ten deploys nothing.
**Any sentence quantifying over the ten crosses a control with no defence
parameters to quantify over.** "Varied separately" is exact: the exponential
regime runs over all nine defended conditions at 200 s only
(`run_corpus.py:268-271`).

**Flagged, not changed.** Table 5.2's caption says arm, condition and deployment
interval "are run in every combination", which collapses on the no-defence cell
for the same reason. The cell is interval-independent, so no reported number is
affected and the caption is not wrong about the design; if it is ever tightened,
"every combination" takes an "each defended" of its own.

**Standing from §AE and unchanged:** *baseline* stays unavailable for the
no-defence condition (conventions §f2, against "the baseline attacker" two
paragraphs up), and *condition* survives because it must cover a control and its
treatments and because *configuration* is spoken for.

---

## §AG — The Metrics unit (2026-09-18)

Marc had not read this unit before. His verdict on the opener: "what does that
even mean — it is so obviously not relevant, such a nothing of a sentence, and
it's two lines"; on *denominator*: "is that standard language we should be using?
No, I think not"; on *because it responds at every interval*: "so we're putting
justification into our experimental setup, is that what we're doing now?"; and
what it must carry instead: "these are the metrics, we've enumerated them in this
table, bang, this is what we're using to measure our research question, those
high-level things — but it's carried none of that."

**Before → after.**

> What judges a defence here is the field's measure and not this thesis's: every
> metric this chapter reports is keyed in Table 5.3 to the family of Table 3.1 it
> instantiates. Distinct hosts compromised is the denominator throughout, because
> it responds at every interval, and target reach is reported beside it wherever
> it is not degenerate.

> Table 5.3 lists every metric this chapter reports, grouped by purpose as
> Table 3.1 groups the field's: effectiveness, what a defence takes from the
> attacker, and efficiency, what it costs to run. Host breadth, the distinct hosts
> an attacker compromises, carries every comparison, with target reach beside it
> wherever the conditions differ on it.

**1. The opener is cut, not rewritten.** It was an **answer to an objection** —
Marc's own circularity worry, that scoring your own attacker model with your own
metrics lets you fudge the numbers — and answering it here fails twice.
Conventions §a: a setup declares and does not argue. And a sentence whose content
is "these are not self-serving" is the form of claim a reader discounts on sight.
**The objection is still answered, and better, by the thing that carries it**:
Table 5.3's *Family* column keys every metric to Table 3.1's own inner key, which
a reader checks rather than takes on trust. The verdict-level version belongs in
the discussion (conventions §f).

**2. The tie-back is now factual, and it does the enumerating he asked for.**
"Grouped by purpose as Table 3.1 groups the field's" is literally true of
Table 5.3's two row groups, and *purpose, effectiveness or efficiency* is
§3.2.2's own ratified sentence, so the reader meets no new axis. The two glosses
are the high-level statement: what a defence takes from the attacker, what it
costs to run.

**3. *Denominator* is not the word — and the odd part is that it was true of one
section only.** §5.5 reports actions and successes **per host reached**
(`tab:eff-cost`), so hosts reached is an actual denominator there; in §5.4 it is
the outcome axis of every float. **"Carries every comparison" is the one
statement true of both**, and it is checkable against FLOATS.md: every §5.4 float
is suppression of hosts reached, and §5.5's frontier plots that same suppression
against occupancy.

**4. The justification clause goes, for consistency as much as for itself.** The
Defence unit lost both of its motive clauses in §AF; the ration is one each in
Network and Attacker, none after that.

**5. *Degenerate* was jargon for a fact worth keeping.** Target reach is pinned
near zero on the database set under the targeted objective and at zero under the
opportunistic one (`targeted_attacker_findings.md` §4; `hypothesis_tree.md` §8e,
"no leaf denominated on objective achievement can be stated") — which is *why*
breadth is the through-line. "Wherever the conditions differ on it" says it in
the reader's words, and declaring that a tabled metric appears only sometimes is
a setup job (conventions §c).

**Flagged, not changed — two names for one metric.** Table 5.3 says **host
breadth**, every §5.4/§5.5 float caption says **hosts reached**, the records say
**host-compromise breadth**. The prose takes the table's name and glosses it
once. One of the three should win document-wide; the captions are generated, so
it is a one-line change in `tools/ch5_effectiveness_figures.py` plus a
terminology row. Marc's ruling.

§5.2 is 330 words. **Runs** is the last unit without this pass.

### §AG2 — Metrics, second pass

Marc on the first pass: the glosses — "do we need to state the definitions of
effectiveness and efficiency, was that already carried in the literature review?
because I'm pretty sure it is"; and sentence two — "I don't understand what the
point is ... I don't even know what that second sentence is, it's disjointed and
it's not in its context, so I don't really know what it's there for", with
"be mindful, long sentences are unreadable".

> Table 5.3 lists the metrics this chapter judges a defence by, grouped by
> effectiveness and efficiency as Table 3.1 groups the field's. Every comparison
> is made on host breadth, the distinct hosts an attacker compromises.

37 words, two sentences, neither longer than a line and a half. §5.2 is now
**311 words**, from 546.

**(a) The glosses go — and his instinct is right for a different reason than the
one he gave.** §3.2.2 *names* the split and cites Cho ("Metrics can be split on
perspective, attacker-side or defender-side, and purpose, effectiveness or
efficiency") but **never glosses either word in prose**; the gloss lives in a
source comment. What does gloss them is **the chapter preamble two pages up, in
Marc's own dictation**: "what the defences do to it (§5.4), and what that costs
(§5.5)". So they were redundant against the preamble, not the literature review,
and the preamble is where the reader meets them first. Dropping them also drops
the abstract word *purpose*, the sentence's only unexplained vocabulary.

**(b) "Judges a defence by" is scope, not boast, and it was load-bearing.** Marc
read sentence two as being about "metrics for attack validation" — the §5.3
instruments. **That confusion is the prose's fault: "every metric this chapter
reports" was false**, since §5.3 reports four more that are deliberately not in
Table 5.3. The cut opener had been carrying that scope inside its
objection-answer, and the scope was the half worth keeping. **Table 5.3's caption
said the same false thing and is fixed with it** ("Every metric this chapter
judges a defence by"), so caption and prose now agree.

**(c) Sentence two now states its job in its first four words.** "Host breadth
… carries every comparison" put the metric first and the job last, which is
exactly why it read as disjointed — nothing told the reader what the sentence was
for until it was over. **Target reach leaves the prose entirely**: the conditional
reporting is a results fact, the table already lists the metric, and the clause
was the second half of a two-clause sentence with no visible purpose.

### §AH — Do we carry the lineage's metric names? (Marc, 2026-09-18)

His question, of host breadth: "is that HCR, network compromise ratio? That was
something used in prior works — are we not carrying over the names of our
lineage's metrics?" **Checked, and the answer differs per row.** Nothing renamed:
this is a ruling of his, and it reaches the generated captions.

**Host breadth is not HCR/NCR, on two counts.**

1. **Not the same quantity.** HCR is Ho's Eq. 10 — `C_t / T_host` at a compromise
   **checkpoint**, bounded [0, 1], implemented as `compromised_num / host_num`
   (`evaluation.py:126`, `metrics_semantics.md` L98). Zhang's NCR is the
   **checkpoint metric** that terminates the run and fixes where MTTC is read
   (`zhang2023.md` L94). Ours is the distinct hosts reached across a **whole
   run**, and the number actually reported is its **suppression against the
   no-defence arm** (`analyse.py:227`). On a fixed 50-host network a count and a
   ratio differ by a constant — but a difference from a control is neither.
2. **Neither paper reports it as a result.** Ho declares **eleven selector
   features** and **four evaluation metrics** (ASR, RoA, APE, Risk); HCR is a
   feature, and one he finds "performed the worst" (`ho2024.md` L86, L132). Tay's
   five reported are ASR, MTTC, APE, RoA, Risk (`tay2024.md` L57). Carrying HCR
   over would import a label the lineage does not use for an outcome.

**The tie-back that is true is already in the table**: the *Family* cell says
**system state**, which is Table 3.1's row holding HCR and NCR.

**Where we do drop a lineage name, and it is worth his ruling.** Brown's two
metrics are **"attack actions blocked"** (Fig. 4) and **"the average attempts
required to compromise"** (Fig. 5) — both already carried under Brown's own names
in Table 3.1 (dissertation.tex:2404, :2425). They are this table's **blocked
fraction** and **effort per host**, renormalised: a share rather than a total,
per distinct host rather than per compromise. **Brown is the direct substrate
lineage and §5.4.3 re-runs his claim**, so different names for his own two
metrics cost something and buy nothing.

**The middle path has a precedent in this repo: "internal MTTC."** The lineage
name is kept, qualified in one word, and the divergence written down
(`metrics_semantics.md` §a, §c). "Attack actions blocked, as a share" is the same
move. Note that *delay to first compromise* should **not** take MTTC's name — the
repo's MTTC is a mean over attack-action durations at checkpoints, a different
quantity, and C7/ATK-04 already shift its magnitude.

**Recommendation.** Leave host breadth as it is and say the HCR relation nowhere
(the Family cell carries it). Rename the two Brown-derived rows to Brown's names
with the renormalisation in the *What it is* cell. Settle the host
breadth / hosts reached / host-compromise breadth split at the same time — one
ruling, one pass over `tools/ch5_effectiveness_figures.py`, `tab:eff-lineage` and
the terminology file.

---

## §AI — The Runs unit (2026-09-18)

Marc's verdict: "that reads like compaction for an LLM to read — it looks like
preserving context. This is not thesis-ready." His specific objections: *cell*
("what is the cell to the reader?"); the run-count justification and its citation
("none of that is relevant to a generalised computer scientist — why is there a
citation?"); "the two arms consume randomness differently" ("that's a descriptor,
not a setup ... that's pretty self-evident"); "no comparison across attackers is
paired" ("it comes across as randomness — we don't compare attackers for a
multitude of reasons"); "which no evaluation in this lineage does" ("why do I
need other lineages? this is our lineage, this is our timeline"); and the whole
last sentence — *declared claims*, *families of comparisons*, *minimum effect of
interest* — "I don't know what that means."

> Every combination in Table 5.2 is run a thousand times, each on its own seed.
> The same seeds are used on every arm, so every attacker meets the same thousand
> networks. Differences are reported as effect sizes with 95 % confidence
> intervals.

**85 words → 44.** §5.2 is **257 words**, from 546. Three sentences, no
justification, no citation, no scoreboard.

**The form is the one this repo's conventions file already nominates.**
`evaluation_conventions.md` §d calls Barach 2026 "the model declaration, and the
fullest in the whole source tree" — four sentences carrying repetitions,
dispersion, intervals and the test — and says to **copy the form**. Repetitions
and intervals are here; the test is not, for the reason below. And the corpus's
own register is this plain: Zhang declares "100 runs", Reti "each combination of
parameters was run 100 times". **"Combination" is Reti's word.**

***Cell* is design-of-experiments vocabulary, and §d's census is decisive**:
every term of art in formal sensitivity analysis returns **zero hits outside this
repo's own records**, and "the MTD literature practises one-at-a-time analysis
universally and names it never." Note that *configuration* — Barach's own word —
is unavailable: the Network unit uses it for the network. Same collision as
*baseline* and *condition*.

**The seed sentence keeps the fact and drops the mechanism.** "The two arms
consume randomness differently" was a descriptor and self-evident; what a reader
needs is the **consequence** of sharing seeds — the arms are compared on the same
networks rather than separately drawn ones. That consequence is also the only
thing in this unit Table 5.2 cannot carry, its *Seeds* row already reading
"1 000 per cell, the same set on every arm".

**All inference machinery leaves §5.2, and the conventions say where it goes.**
§d: "a minimum effect size of interest is declared **with each claim**." §e: the
success criterion is declared "at the definition site, one sentence, not a unit
of its own." So the effect floors, the multiplicity adjustment and the no-pairing
commitment belong at §5.4's claims, beside the numbers they govern — not in a
setup with no claims in front of it. **This discharges the [3b] that stood here.**

**Three things this unit hands on.**

1. **Why a thousand.** `hoad2007` is the method — replicate until the interval
   around the cumulative mean sits inside a declared tolerance, which makes the
   count a consequence rather than a round number (§d2). Marc is right that it
   read as justification in the setup, but it is worth one line to an examiner:
   §5.1's sensitivity material or a footnote. **Note the side effect: hoad2007 is
   now cited nowhere in the document and drops out of the bibliography.**
2. **That no comparison across attackers is paired.** It reads as an excuse here,
   but it is a real commitment — §d warns a paired test "is wrong wherever the
   arms do not actually share randomness" — so it must appear wherever the
   cross-arm test is named, which is §5.4.2.
3. **That intervals exceed the lineage.** §d records that **no paper in the
   lineage reports a confidence interval** and says the improvement should be
   stated deliberately rather than slipped in. Cutting the comparative clause
   from the setup is right — a setup that scores itself against others is
   arguing — so it lands in §5.4.3, which re-runs the published claims, or ch6.

**All five units of §5.2 have now had the pass.**
