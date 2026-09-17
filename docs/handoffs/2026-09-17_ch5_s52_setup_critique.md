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
