---
status: RE-RUN LANDED 2026-09-17 (33 000 runs, zero errors, centre identical to the defended corpus); the four fragments, the App. C.1 figure, the App. C leads and the §5.1 skeleton are in the tex; findings record ch5_s51_sensitivity_findings.md. OWED: Marc's acceptance of the three ch4 insertions (comment blocks in place); the §5.1 dictation (three paragraphs, D2, the findings record §7 is the content); the caption voice passes; the re-launch at a thousand seeds when the defended corpus moves (findings §8); a one-clause §5.1 pointer in the redrafted §5.2 if Marc wants one (the redraft carries none)
created: 2026-09-17
owner: Marc (rulings, prose); session (re-run, fragments, placements)
supersedes: ch5 design handoff §3.2 (the re-run), §19 (the first cold read) and §20 (the second) — those sections are the diagnosis; this is the executing brief
---

# Overhaul §5.1 Sensitivity analysis so that a reader who has finished chapter 4 gets the one thing it owes them, in chapter 4's own words, in under a page

## State of play

**What §5.1 is for** (settled 2026-09-17, design handoff §20–§20.7). One question:
*does any conclusion of this chapter depend on where, inside its plausible band,
a value chapter 4 chose sits?* Chapter 4 and the appendix say how the values
were got; §5.1 says what it would cost to be wrong about them; chapter 6 says
what that means. §5.1 is the licence for §5.3–§5.5, not a result. It says one
new thing per family and repeats nothing chapter 4 said.

**What was done, and what was not.** The field calls two different things
"sensitivity analysis": calibration (bounds, a cost function, an optimum that
becomes the value) and robustness (choose by argument, then perturb the number
the choice produced and see whether the answer changes). Zhang claimed the first
and did neither. This project did the second, and only the second. So a
qualitative choice with no number — the mapping, the nine failure rules — is not
"swept"; it is compared against the alternative that was tried (the mapping) or
held with the reason stated (the rules).

**The draft as it stands** (`sec:sensitivity`, 2026-09-13; ~600 words, one
inline table, one figure, three `[3b]` markers, every number `[VERIFY]`) fails
on seven locatable counts (design handoff §20.4): written as retrieval keys to
the record; opens with inventory ("seven numbers") not the question; introduces
objects the reader has not met; three kinds of row share one table column; half
the prose defends the method; the figure has no antecedent sentence; the closing
paragraph selects a factor (the mutation interval) the section never swept.

**The abstraction test, applied to the tex body of ch2–ch4 (comments excluded):**

| Object the draft uses | Where the reader met it | Verdict |
|---|---|---|
| "four anchor families" | §4.4.2, once, unnamed | usable if ch4 names the four |
| "low-and-slow anchor" | never (ch3 §3.1.1 has "low-and-slow tempo"; App. B.4 has "Low-and-slow" as a family name) | "anchor" must go; "the low-and-slow family" is usable once ch4 names it |
| $\gamma$, $\delta$, $z$; "forward / backward decay", "floor" | the notation table only (`tab:gspn-notation`) | ch4 §4.4.4 must say in words what the distance term does before §5.1 can move it |
| "rule kernel", "distance kernel" | notation table; §4.4.4 says "distance, $d$" once | "kernel" stays out of §5.1; ch4's words are "the failure rules" and "distance" |
| "mutation interval", "degenerate region", "operating region" | nowhere in ch2–ch4 | out of §5.1 entirely; §5.2's factor |
| "screen", "rank", OAT, "cross through the input space", Sargent, ten Broeke | nowhere; conventions §d warns the vocabulary is foreign | out |

**The two sweeps on record do not share the chapter's configuration** (design
§3.2, unchanged): ten seeds, one scheme, pre-restoration substrate; the
failure-matrix sweep under the superseded fixed-dwell regime and around a
backward decay of 0.5 that was re-cut to 0.25 (band 0.25–0.75 → 0.1–0.5) after
the study. The chapter reports 100 seeds, the shifted regime, the targeted
objective, the failure-only overlay, 15 000 s, 200 s and 2 000 s
(`data/results/ch5_defended/run_corpus.py`). Every number in §5.1 and App. C is
therefore blocked on a re-run, and so is the one selection sentence.

**The seam for the re-run exists.** Anchor scaling:
`data/results/rate_feasibility_study/run_study.py` (`m[group] × relative_multiplier
× anchor.duration_s`; the Erlang-4 `TimingSource`). Decay parameters:
`data/results/s1_weight_sensitivity/run_sweep.py::run_cell` builds
`DistanceKernel(gamma, delta_ratio, z)` → `compile_values` → `OutcomeOverlay`.
The chapter's cell: `data/results/ch5_defended/run_corpus.py::_movement`. The
declared point is `gamma 0.25, delta_ratio 0.25, z 0.1`
(`data/ogasp/controller/lifecycle_consensus.json`; the loader reads it —
`rules.py:223`). Note the dataclass default `delta_ratio = 0.5` at `rules.py:97`
is stale and differs from the declared file; nothing on the declared path reads
the default, but flag it, do not fix it here.

## Marc's rulings on the first cut (2026-09-17, second reply)

| Ruling | Outcome |
|---|---|
| position | §5.1 stays first. **No bridge from chapter 4**: "it doesn't seem encapsulated; the preamble can carry that; the section stands on its own." The chapter preamble carries the join; §5.1 opens with its question. |
| five paragraphs in 220 words | alarm bells, rightly: 44 words a paragraph is choppy. **Three paragraphs, ~250 words** (D2 below). |
| register | "calm down on the rhetoric; this is scientific writing." No *numbers the formalism could not supply*, no *we had to*, no triads for effect, no first-sentence flourish. Plain declaratives. |
| the middle paragraphs | Marc asked whether they say *how the three were produced*. They do not: chapter 4 and App. B say how; §5.1 says only what moved when each was perturbed. One sentence in the brief, none in the section. |
| figure | to the appendix. |
| "family" / "anchor" | left to the session ("go crazy with it"): **family** in the body, named in chapter 4 (insertion B); "anchor" stays the appendix's and the code's word. |
| symbols | out of Table 5.1. "Keep it simple." |
| the draw's corner | leaves §5.2. |
| the re-run | "what have we re-run? there's nothing to run" → answered in D7: two sweeps exist on record from July at ten seeds on an older configuration; the re-run repeats their perturbations at the chapter's pins. Green-lit: "do what you think you need to do." |
| chapter 4 insertions | "propose them in place with the context and I can accept item by item" → placed as comment blocks at the three sites (D5), 2026-09-17; not staged (the tex is under Marc's edit). |

## Recommended approach

Seven decisions, then the order of work. The rulings above are applied.

### D1. Keep §5.1 titled and first; no bridge; scientific register

The section stands on its own. It does not carry over from the method, count
its inputs, or say what the formalism could not supply. Its first sentence is
its question. The chapter preamble (Marc's dictation) is where chapter 4 is
joined to the evaluation.

*Alternative considered:* swap §5.1 and §5.2 so the setup is declared before
the robustness check uses it. Not taken; kept in reserve if ¶1's forward
references (the outcome measure, the defended condition) cannot be closed in a
clause each.

### D2. The body: three paragraphs, ~250 words, chapter 4's words only

Content points (Marc's prose; the session never drafts it). The paragraphs
report what moved when a value was perturbed, never how the value was produced.

| ¶ | Job | Content points | Words |
|---|---|---|---|
| 1 | the question and the test | The question in one plain sentence: whether any conclusion of this chapter depends on where a declared value of the model sits inside its band. The three declared inputs, by their §4.4 names, in one sentence. The test: each value is moved across its band with the others held at their declared values, and distinct hosts reached is read against its interval at the declared value; a value whose band ends stay inside that interval does not carry the chapter. One clause: the bands come from the evidence tiers (App. B.4) and from the distance term's structure (App. B.6). No method philosophy. | ~80 |
| 2 | the dwell times | The four families of §4.4.2. The two priced from the simulator move nothing at either band end, under no defence and under defence. The low-and-slow family moves hosts reached at both ends, and monotonically: the longer the quiet tactics dwell, the fewer hosts before the horizon. The thesis-level sentence: the model's timing sensitivity sits entirely in the values whose provenance is weakest; the inherited values carry none of it. The draw's shape: the same-mean concentrated alternative changes nothing across the cells the chapter reports; at the one corner where the low-and-slow dwell is at the top of its band under mutation, the concentrated shape reaches fewer hosts, so the more faithful shape is the worse one for the attacker. Numbers from the re-run. | ~100 |
| 3 | the mapping, the failure matrix, the hand-off | The mapping is not a band: the forced-total alternative of App. B.7 under-performs the partial mapping (one clause why), and the partial mapping stands as a declared input the effectiveness claims carry. The distance term's two rates and its floor (§4.4.4's words): the backward rate moves most; the forward rate moves outcomes only on the rejected mapping; the floor moves nothing, structurally, because no profile net carries a jump of three stages. The nine rules are held, each a single argued value. Closing sentence: the one input the chapter's claims are exposed to is the low-and-slow dwell; it is held at its declared value and every claim that could turn on it says so. | ~80 |

Every noun in ¶1–¶3 must have a chapter 4 antecedent (the validation gate greps
for the banned list). Madan is the only citation the section may carry, one
clause, optional.

### D3. Table 5.1: three row groups, four columns, in words, generated

Replace the inline `tab:parameter-register` with a generated fragment
`docs/thesis/tables/tab_5-1a_declared_inputs.tex` (label kept so every `\ref`
stands), emitted by the re-run's analyser:

| group (`\rowgroup`) | Input | Chosen value | Moved across | What moved |
|---|---|---|---|---|
| Dwell times | scan-shaped family | 35 s | ×0.5 – ×2 | inert |
| | exploit-shaped family | 4.5 s | ×0.5 – ×2 | inert |
| | low-and-slow family | 45 s | ×0.25 – ×4 | hosts reached, at both ends (App. C.1) |
| | objective-execution family | 36 s | ×0.5 – ×2 | inert |
| | the draw's shape | exponential | same-mean, concentrated | inert; one corner (App. C.2) |
| Mapping | tactic to verb | partial | forced total | the alternative under-performs (App. B.7) |
| Failure matrix | forward rate | 0.25 | 0.1 – 0.5 | *re-run* |
| | backward rate | 0.25 | 0.1 – 0.5 | *re-run* |
| | floor | 0.1 | 0, 0.05, 0.1 | zero by structure |
| | the nine rules | argued values | held | — |

Symbols leave the body; the caption binds them once ("$\mu_p$, $\tau_p$,
$\varphi$, $\gamma$, $\delta$, $z$, $R$ of Table 4.x"). The origin of each band
is one clause of the caption, not a column. "Anchor" does not appear; "family"
does (D5). "What moved" entries are the analyser's, computed against the
criterion below, never typed.

### D4. Figure 5.1 defaults to Appendix C.1

Rename the stem to `fig_C-1a_sens_dwell_family` and include it beside
`tab:anchor-sensitivity`. It re-enters the body only if the re-run shows a form
a sentence cannot carry (a threshold, a reversal), by Marc's figure ruling
(*a figure must communicate*). If it does re-enter, it keeps the corpus form
(x = multiple of the chosen value, y = hosts reached with interval, series =
no defence / defended) and gets its antecedent sentence in ¶2 first. The
generator `tools/ch5_sensitivity_figure.py` needs only `--csv` re-pointed and
`--anchor` renamed to `--family`; retire "anchor" from its prose names.

### D5. Chapter 4 insertions — the antecedents §5.1 needs (Marc's words; content points only)

| Site | Now | Content point |
|---|---|---|
| §4.4 opening, `sec:execution` (~l. 4508–4513) | "each is swept in the sensitivity analysis" | a verb that covers a band, a swap and a hold: whether the evaluation depends on any of them is Section 5.1's question |
| §4.4.2 dwell times (~l. 4682–4684) | "four anchor families ... the anchors are what the sensitivity analysis sweeps" | name the four in the clause (scan-shaped, exploit-shaped, low-and-slow, objective execution) and call them families; "anchor" may stay as the appendix's word |
| §4.4.4 failure matrix (~l. 4815–4825) | "The second is distance, $d$ ... the kernel's parameters are swept" | one sentence on what distance does: a move to an adjacent stage is unpenalised; a jump across two stages is scaled down by a rate, one rate forward and one backward; anything further is cut to zero by a floor. That is the whole antecedent ¶4 needs. Replace "kernel" with "distance term" in the body if Marc agrees; the appendix keeps "kernel" |
| §4.4.3 mapping (~l. 4772–4774) | "the mapping is swapped in the sensitivity analysis" | stands |
| §4.4.4 close (~l. 4885–4887) | "plausible, literature-bounded and sensitivity-swept" | stands |
| `tab:gspn-notation` rows for $R$, $d$, $\gamma$, $\delta$, $z$ | declared-in pointers | stand |

### D6. Downstream re-cuts (session proposals, ratify-on-read)

- **§5.2 opener** — SUPERSEDED 2026-09-17: §5.2 was redrafted concurrently
  (handoff `2026-09-17_ch5_s52_setup_critique.md`) and its opener no longer
  carries the three-things paragraph, the draw's corner or any reference to
  §5.1. Whether a one-clause pointer to the held input is owed there is Marc's
  call; Table 5.3's held-inputs row already carries it.
- **`tab:factors-fixed`, row "Declared inputs":** "the low-and-slow anchor is
  the one input ..." → the family wording of D5; the pointer to Table 5.1 stays.
- **§5.2 sentence "three factors moved one at a time from that core: the
  discipline of Section 5.1 applied to the experiment rather than to the
  model":** keep — it is the one sentence that carries the input/factor
  distinction, and it does so in the field's plain words.
- **Chapter 5 roadmap placeholder:** its §5.1 clause ("checks that the declared
  numbers do not carry the conclusions") is already right; Marc's dictation.
- **Appendix C:** an opening paragraph for `app:sensitivity` (what the appendix
  holds: the per-value expansion of Table 5.1, by resolution not importance) and
  a two-sentence lead per section — connective prose, green-lit, DRAFT STATE.
  Refresh `tab:anchor-sensitivity` and `tab:shape-substitution` from the re-run
  and convert both from inline to generated fragments; fill `tab:decay-sensitivity`
  from the re-run; retire "anchor" → "family" in captions.
- **`FLOATS.md`:** the §5.1 rows (table generated; figure moved to C.1 or kept),
  the three App. C fragments, the new generator names. Same commit as the move.
- **Bibliography:** dropping ten Broeke and Sargent from §5.1 orphans nothing
  the build needs; leave the entries.

### D7. The re-run — what it is, design, criterion, cost, outputs

**What exists, in plain terms.** Two sweeps were run in July and are on record:
the routing-weight sweep (`s1_weight_sensitivity`, 2 600 runs) and the dwell
and rate sweep (`rate_feasibility_study`, 1 740 runs after its S3-R repeat).
Both at ten seeds, one MTD scheme, the pre-restoration substrate; the weight
sweep under the since-superseded fixed-dwell regime and around a backward decay
of 0.5 that was later re-cut to 0.25. Every number the draft §5.1 and App. C
quote comes from those two. The rest of chapter 5 now reports at 100 seeds on
the current pins. **The re-run repeats the same perturbations at the chapter's
configuration** so §5.1's numbers are the chapter's numbers. It re-prosecutes
nothing: no value, band or rule changes; only the setting they are measured in.
It is the numbers' sole source, it costs under two hours, and it does not block
the ch4 insertions or the prose skeleton.

**Design.** One-at-a-time from the chapter's core cell, on the movement arm
only (the baseline consumes no chosen value). Points:

| family | points | count |
|---|---|---|
| dwell: four families at both band ends | ×0.5, ×2 for three; ×0.25, ×4 for low-and-slow | 8 |
| shape swap | Erlang-4 same-mean on the quiet family, at centre; and at low-and-slow ×4 (the corner) | 2 |
| mapping swap | `v1_ckc_total` at the declared point, if it still runs under the targeted objective (verify first; if not, App. B.7's record stands as the comparison and says so) | 1 |
| decays | $\gamma \in \{0.1, 0.5\}$, $\delta \in \{0.1, 0.5\}$, $z \in \{0, 0.05\}$, then the four corners of $(\gamma, \delta)$ | 10 |

21 points × 5 profiles × 100 seeds (0–99, shared) × 3 conditions (no defence;
`random` over the seven at 200 s; at 2 000 s) ≈ **31 500 runs**. The defended
corpus ran 30 200 in 5 820 s on 7 workers (`run.log`), so this is under two
hours. The centre cell is the defended corpus's own (`profile × no defence / random
× interval`), read from `runs.jsonl`, not re-run. The `random` scheme is the
defended condition because the sweep asks whether the chosen values move the
outcome, not which mechanism ranks where; single-mechanism cells are §5.4's.

**Criterion, fixed before running, in the runner's docstring as the record's
discipline requires:** a point is *inert* when the pooled mean of distinct hosts
reached at that point lies inside the 95 % interval of the centre cell, in both
defended conditions and under no defence; *moved* otherwise, with the direction
and the band-end values reported; the floor is reported *zero by structure* if
and only if the per-run statistics are bit-identical to centre (they will be:
no net carries a three-stage edge — `fig:distance-kernel-bands`). Pooled across
the four profiles (the chapter's arm set; the aggregate is a fifth series, not
pooled). Intervals are the chapter's (bootstrap on the seed set,
`_ch5_style.py` / `analyse.py` conventions).

**Runner.** `data/results/ch5_s51_sensitivity/run_sweep.py`, built on
`ch5_defended/run_corpus.py::_movement` (same pins) with the anchor arithmetic
and Erlang source imported from `rate_feasibility_study/run_study.py` and the
kernel construction from `s1_weight_sensitivity/run_sweep.py`. Do not copy the
old runners' seed sets, scheme or regime. `analyse.py` reads `runs.jsonl` plus
the defended corpus's centre cells and emits `numbers.json` and the four
fragments (D3, App. C.1–C.3) and the figure CSV.

**Findings record.** `docs/implementation/pipeline/ogasp/ch5_s51_sensitivity_findings.md`
in the form of the §5.3.1 / §5.3.2 records (results_section_workflow.md): the
design, the criterion, the per-family verdict, what may and may not be claimed,
and the selection sentence's content (which input moved). Numbers here, not in
chat.

### Order of work

1. **Marc rules D1–D7** (one message; a recommendation is stated for each).
2. **Session: the re-run** — runner, criterion, ~2 h compute, analyser,
   fragments, figure, findings record. Verify the mapping-swap point runs before
   including it; verify the kernel's declared point is read from
   `lifecycle_consensus.json` (0.25 / 0.25 / 0.1) in the chapter's cell.
3. **Marc: chapter 4 insertions** (D5), dictated; the session places them.
4. **Marc: §5.1 ¶1–¶5**, dictated from D2's content points and the findings
   record; the session runs the pipeline (repair → scrutinise → compress →
   voice) and swaps the tex block, deleting the draft, its three `[3b]` markers
   and the RE-CUT / DRAFT STATE comments.
5. **Session: D6 re-cuts**, ratify-on-read; App. C connective prose, DRAFT STATE.
6. **Build check; `FLOATS.md`; this handoff deleted in the landing commit.**

## Validation gate

- `latexmk` builds clean; every `\ref` to `sec:sensitivity`, `tab:parameter-register`,
  `app:sensitivity`, `app:dwell-robustness`, `app:exponential-shape`,
  `app:decay-robustness` resolves.
- §5.1's body is ≤ 250 words of prose and contains none of: *anchor, kernel,
  degenerate, operating region, mutation interval, screen, rank, one-at-a-time,
  OAT, Sargent, ten Broeke, seven, VERIFY, [3b]*. (A grep over the block.)
- Every object named in §5.1 has an antecedent in ch4's body: the four families
  named at §4.4.2; the distance term's two rates and floor stated at §4.4.4.
- Every number in §5.1, Table 5.1 and App. C.1–C.3 traces to
  `data/results/ch5_s51_sensitivity/numbers.json`; the four fragments carry the
  GENERATED header; no inline sensitivity table remains.
- Table 5.1's "What moved" column is complete: ten rows, no blank, no `[VERIFY]`.
- §5.2's opener picks up exactly one thing from §5.1; the draw's corner and the
  interval's justification appear once each in the chapter, in §5.1 ¶2 and
  §5.2's factor paragraph respectively.
- Figure 5.1 is either in App. C.1 or has its antecedent sentence in ¶2 and a
  form the findings record says a sentence cannot carry.
- `FLOATS.md` matches the build; this file is gone.

## Hard constraints

- Prose in §5.1, ch4 and the App. C section leads beyond connective is Marc's;
  the session supplies content points, fragments, captions (DRAFT STATE) and
  placements only (voice.md; the drafting pipeline).
- Nothing is tuned: the re-run reads the declared values from the tracked
  catalogue and the declared kernel file; the criterion is written before the
  first run; no criterion is revised after a result is seen.
- Chapter 5's pins are the re-run's pins (mapping, overlay, objective, regime,
  horizon, seeds, geometry); any departure is declared in the findings record
  and Table 5.1's caption.
- The `dissertation.tex` is under concurrent edit by Marc (dirty at session
  start); the session edits only the §5.1 block, the §5.2 opener sentence, the
  one `tab:factors-fixed` row and the App. C blocks, by line-level diff, after
  re-reading the current file.
- No new dependencies; determinism (SIM-05) holds on every cell; the stale
  `DistanceKernel.delta_ratio` default is flagged in the findings record, not
  changed.
- Australian English.

## Reading list

1. This file; then design handoff §16–§20.7 (the diagnosis and the rulings trail).
2. `docs/workflows/evaluation_conventions.md` §c, §d, §d2, §h — what the field
   does; `docs/workflows/figure_table_conventions.md` §b, §e — the float contract.
3. `docs/implementation/pipeline/ogasp/rate_feasibility_study.md` §3, §10 and
   `weight_sensitivity_study.md` §2, §5–§6 — the sweeps on record, their
   criteria and their arithmetic.
4. `data/results/ch5_defended/run_corpus.py`, `rate_feasibility_study/run_study.py`,
   `s1_weight_sensitivity/run_sweep.py` — the three seams the runner joins.
5. `docs/workflows/results_section_workflow.md` — the recorder / reader /
   findings / generator / swap path; `docs/workflows/voice.md` — the gate.

## Out of scope (explicitly)

- Re-opening the one-unit ruling (C30): §5.1 stays one section with no
  subsections; the three families are paragraphs.
- Any change to the declared values, bands or the nine rules.
- The 60 000 s horizon, the single-mechanism cells and the baseline arm in the
  sweep — none of them bears on whether a chosen value carries the chapter.
- Chapter 6's reading of the sensitivity result (the fidelity verdict table's
  "sensitivity-swept" wording) — a ch6 pass.
- Fixing `rules.py:97`.

## Return format

Thesis-framed and short: which input the chapter's claims are exposed to (the
selection sentence's content), whether any verdict on record changed at the
reported configuration, and what §5.1 may now say that the draft could not.
Point at the findings record for the numbers.

---

# Second cut, 2026-09-18 — the structure before the sentences

Marc's direction this session: settle the paragraphs' purpose, then the
sentence slots inside each, then dictate sentence by sentence. Table 5.1's
"structure is not clear and not well thought out". What follows replaces D2's
paragraph table and D3's table layout; D1, D4–D7 stand.

## S1. Who §5.1 is written for, and what it owes them

A reader who has finished chapter 4 and has opened no appendix. Chapter 4 told
them three times that a value could not be derived: the dwell times do not
exist in the literature or in CTI (§4.4.2), there is no real tactic-to-verb
mapping so best judgement was used (§4.4.3), and the failure side is the blind
spot of the CTI, so the matrix was declared rather than reverse-engineered
(§4.4.4). Each of those sentences ends with a pointer to this section.

So the reader arrives with one question, and it is not "what is a sensitivity
analysis": **is the evaluation built on numbers you made up?** §5.1 is where
that debt is discharged. Its product is not the sweep; it is the single
sentence naming which input the chapter's claims are exposed to, which §5.2's
`tab:factors-fixed` already forward-references and which chapter 6's fidelity
verdict consumes.

Two consequences for the drafting.

1. **Nothing in §5.1 explains how a value was produced.** Chapter 4 and the
   appendices do that. A sentence that re-derives is the retrieval-key register
   the 2026-09-13 draft was retired for.
2. **The chapter preamble already says what §5.1 does** ("checks that the
   declared numbers do not carry the conclusions"). ¶1 must not restate it in
   the same shape; it opens on the question, not on the job.

The conventions §c position, unchanged: almost no paper in the corpus has a
titled sensitivity section, deriving bands from the model's structure exceeds
the corpus, and **a sweep that selects is stronger than one that shows a
verdict did not move**. The selection is therefore the section's close, not a
trailing clause.

## S2. The paragraphs — four, ~300 words (a departure from D2, Marc to rule)

D2 ruled three paragraphs at ~250 words. The re-run's shape argues for four.
¶3 of D2 has to carry the mapping (a comparison), two decay rates (bands), a
floor (a structural argument) and nine held rules in ~80 words — four unlike
objects in one paragraph, which is the list-compression register Marc named.
Splitting the verdict off as a short fourth paragraph costs ~50 words, lands
the section on a short paragraph after a long build (voice §d), and makes the
selection findable by the two floats that point at it. Four paragraphs at ~75
words each is not the 44-words-a-paragraph choppiness that set off the alarm.

| ¶ | The claim it establishes | Words |
|---|---|---|
| 1 | the question, and what would count as an answer to it | ~75 |
| 2 | the timing sensitivity is concentrated, and in the family whose provenance is weakest | ~95 |
| 3 | the other two declared inputs move nothing the chapter reports | ~85 |
| 4 | the one input the conclusions are exposed to, and that it is held | ~45 |

## S3. The sentence slots — what each sentence does, with no content

Fifteen slots. Each names the sentence's job, its shape, and what it must not
do. The content for every slot is in the findings record
(`ch5_s51_sensitivity_findings.md` §3–§7); the words are Marc's.

### ¶1 — the question and the test (4 slots + 1 optional)

| # | Job | Shape | Must not |
|---|---|---|---|
| 1.1 | State the question the section answers: whether any conclusion of the evaluation depends on where a declared value sits inside its plausible range. | Plain declarative, the section's first sentence. | No inventory ("three inputs", "seven numbers"); no method noun; no carry-over clause from chapter 4; not the preamble's wording. |
| 1.2 | Name the three declared inputs by their §4.4 names. | One sentence, recall not introduction. | No symbols; no "assumptions"; no re-derivation. |
| 1.3 | State the test: each value is moved across its range with the others held at their declared values, and distinct hosts reached is read against the interval at the declared value. | One sentence. | No OAT/screen/rank vocabulary; no defence of the method. |
| 1.4 | State what counts as an answer: a value whose range ends stay inside that interval does not carry the chapter. | One sentence — the criterion, stated before any result (voice §c9). | Not a definition of "sensitivity"; no philosophy. |
| 1.5 *(optional, one clause on 1.3)* | Where the ranges come from: the evidence tiers of App. B.4 and the structure of the distance term, App. B.6. | A clause. | No claim that this exceeds the corpus — that reading is chapter 6's. |

### ¶2 — the dwell times (5 slots)

| # | Job | Shape | Must not |
|---|---|---|---|
| 2.1 | Claim-first: the model's timing sensitivity is concentrated in one of the four families. | Short declarative opening the paragraph. | Not "the dwell times were swept first"; no procedure. |
| 2.2 | The three families priced from the simulator: what they cost across their ranges, as a magnitude. | One sentence, one unit (hosts lost per doubling). | Do not call them inert — two of the three are not, at this power (findings §2). |
| 2.3 | The low-and-slow family: direction and magnitude, under no defence and under defence; monotone, no threshold. | One sentence, possibly two clauses. | No "anchor"; no threshold or reversal language. |
| 2.4 | The reading that matters: the sensitivity sits in the family whose provenance is weakest, and the simulator-priced families carry a fraction of it. | The section's one compressed sentence (voice §d, rationed). | No hype adjective; no "we had to". |
| 2.5 | The draw's shape: inert where no defence acts; under mutation pressure the concentrated draw costs the attacker a little and never helps it. | One sentence. | Do not claim the ×4 corner (its interval sits on the boundary, findings §4). |

### ¶3 — the two inputs that are not ranges (4 slots)

| # | Job | Shape | Must not |
|---|---|---|---|
| 3.1 | Claim-first: neither of the other two declared inputs moves what the chapter reports. | Short declarative. | No "similarly"/"moreover". |
| 3.2 | The mapping is a comparison, not a range: the alternative that was tried stalls, with one clause of why. | One sentence. | No "partial"/"forced total" as bare terms — say what each does. |
| 3.3 | The distance term's decay: moved across its range at both ends and at the corners, and nothing moved. | One sentence. | Do not present forward and backward as two swept quantities (see S4.2). No "kernel". |
| 3.4 | The floor and the nine rules: the floor can only act on a jump of three stages, which no profile net contains; the rules are single argued judgements and were held. | One sentence, two clauses. | The floor needs its chapter 4 antecedent first (S5, defect D-2). |

### ¶4 — what this licenses (2 slots)

| # | Job | Shape | Must not |
|---|---|---|---|
| 4.1 | Name the one input the chapter's claims are exposed to. | Short declarative. | No hedge stack; do not re-state the magnitude. |
| 4.2 | It is held at its declared value, and every claim that could turn on it says so. | One sentence — the negative scope (voice §c6). | Nothing about the mutation interval (a factor, §5.2's). |
| 4.3 *(optional clause on 4.2)* | Nothing here was calibrated: no range was searched for a fit, and the criterion was fixed before the runs. | A clause. | Sits in tension with D1's "no method philosophy" — Marc's call whether the circularity name (voice §c10) is worth the clause here or belongs in chapter 6. |

## S4. Table 5.1 — the grammar problem and the proposed cut

### S4.1 Why the current table does not read

The four columns encode a **procedure** — declare, move across, observe — but
only five of the ten rows were moved across anything. The other five are a
comparison, a structural zero and a hold, so "Moved across" is fudged for half
the table ("forced total", "held", "0, 0.05") and "What moved" carries four
incompatible registers in one column: a verdict (*inert*), a measurement
(*8.6 / 8.1 / 7.3*), a structural argument (*zero by structure*), a comparison
(*the alternative reaches 0.1 hosts*) and an em-dash.

The conventions already name the fix (§c, last rule): *every declared
parameter is listed; each row says either the range it was swept over and what
moved, or that it was held and why. One register, both kinds of row.* The
column that has to change is the third: it must declare **which kind of row
this is** before the last column speaks.

### S4.2 The proposed cut — four columns, one grammar, one unit

| group | Declared input | Declared | How it was tested | Effect on hosts reached |
|---|---|---|---|---|
| Dwell times | scan-shaped family (reconnaissance, discovery) | 35 s | moved ×0.5 to ×2 | 0.7 lost per doubling |
| | exploit-shaped family (initial access, privilege escalation, credential access, lateral movement) | 4.5 s | moved ×0.5 to ×2 | none detected |
| | low-and-slow family (persistence, stealth, command and control; execution and defence impairment at half) | 45 s | moved ×0.25 to ×4 | 2.6 lost per doubling |
| | objective family (collection, exfiltration, impact) | 36 s | moved ×0.5 to ×2 | 0.6 lost per doubling |
| | the draw around each mean | exponential | compared against a same-mean concentrated draw | none without defence; 0.2 fewer under mutation |
| Mapping | at most one verb per tactic, unmapped tactics dwell only | — | compared against a mapping that forces every tactic onto a verb | the alternative stalls: 0.1 against 8.1 |
| Failure matrix | decay per extra stage crossed | 0.25 | moved 0.1 to 0.5, in both directions and at their four corners | none detected |
| | floor below which a factor reads as zero | 0.1 | moved to 0.05 and 0 | none; it can only act on a jump of three stages, and no profile net carries one |
| | the nine failure rules | argued values | held — each is a single argued judgement, not a magnitude with a range | — |

Four changes from D3, each with its reason.

1. **One unit in the last column.** Hosts lost per doubling for every moved
   row; the low / declared / high triples go to App. C.1, which is what that
   appendix is for. The body table answers "how exposed am I", at a glance,
   in one number. ("Sharp and to the point" — Marc, this session.)
2. **The two decay rates collapse to one row.** The kernel is
   $\gamma^{\Delta-1}$ forward and $\delta^{\Delta-1}$ back, and the declared
   values are $\gamma = \delta = 0.25$ (`lifecycle_consensus.json`): adjacent
   unpenalised, two stages a quarter either way, three stages 0.0625, which
   the floor cuts to zero. **At the declared point the model makes no
   forward/backward distinction** — the split is a capability of the code that
   the declared values do not exercise. Marc's objection stands on the record:
   ATT&CK has no direction, the term is a decay away from the tactic, and
   logically it is one value. The sweep moved both separately and ran all four
   corners, so nothing is lost by presenting one row; App. C.3 keeps the two
   rates and the corners. Presentation change only, no re-run.
3. **The third column declares the kind of row.** *moved over …* / *compared
   against …* / *held — because …*. The reason a row was held lives here, which
   is where the convention puts it, and the last column is then homogeneous.
4. **Code words leave the table.** "Partial", "forced total" and "inert" are
   replaced by what each thing does. "Family" stays (body word); "anchor"
   stays out.

The caption shrinks to five clauses: what the table is, the criterion in one
clause, where the ranges come from, the pooling and run count, the symbol
binding. The current 200-word caption carries argument that belongs in ¶1.

## S5. Four defects in chapter 4 that block the draft

§5.1 cannot move an object the reader has not met. Three of the four
antecedents are still unaccepted comment blocks in the tex (insertions A, B, C
of D5), and one is a live dangling reference.

| # | Defect | Where | Blocks |
|---|---|---|---|
| D-1 | §4.4.4 sends the reader to Figure~\ref{fig:failure-weight-matrix} for "rules A to I"; that figure was regenerated plain on 2026-09-08 and carries no letters (verified against `fig_4-4b_failure_weight_matrix.tex`: no rule glyph in the source). The letters live only on App. B.6's decomposition figure. | `dissertation.tex` §4.4.4, the $R$ sentence | slot 3.4 and Table 5.1's last row. The reader's only encounter with the nine rules points at a figure that does not show them, which is exactly why "the nine rules" reads as an unmotivated concept. **Fix: re-point the reference at App. B.6.** |
| D-2 | The floor is stated nowhere in the body. The 2026-09-08 front-loading ruling cut the sentence; insertion C proposes it and is unaccepted. | §4.4.4, insertion C | slot 3.4 and the floor row. Marc's own framing this session is the content: distance is how far away, and the floor is where too far away is zeroed out. |
| D-3 | The four dwell families are never named in the body. §4.4.2 says "four anchor families" once, unnamed. | §4.4.2, insertion B | ¶2 entirely, and four rows of Table 5.1. |
| D-4 | §4.4's contract sentence says all three inputs are "swept" — the wrong verb for a comparison and for a hold. | §4.4 opening, insertion A | ¶1 slot 1.1, which states the question that sentence should be pointing at. |

## S6. The one question for Marc — can the dwell families take the lifecycle names?

Marc asked whether the families can be standardised onto the words already in
use for the stages: preparation, intrusion, post-intrusion operations,
objective. **They cannot without changing membership.** The two are different
partitions of the 15 tactics, and only one class coincides.

| Tactic | Dwell family | Lifecycle stage |
|---|---|---|
| Reconnaissance | scan-shaped | preparation |
| Resource development | — (0 s) | preparation |
| Initial access | exploit-shaped | intrusion |
| Execution | low-and-slow (half) | intrusion |
| Persistence | low-and-slow | post-intrusion |
| Privilege escalation | exploit-shaped | post-intrusion |
| Stealth | low-and-slow | post-intrusion |
| Defence impairment | low-and-slow (half) | post-intrusion |
| Credential access | exploit-shaped | post-intrusion |
| Discovery | scan-shaped | post-intrusion |
| Lateral movement | exploit-shaped | post-intrusion |
| Command and control | low-and-slow | post-intrusion |
| Collection | objective | objective |
| Exfiltration | objective | objective |
| Impact | objective | objective |

The families are priced by **what the tactic costs** (an enumeration pass, an
exploit, a long quiet dwell, an objective action); the stages order **where the
tactic sits in a campaign**. Eight of the fifteen tactics sit in the
post-intrusion stage across three different families, so one name cannot serve
both. Only the objective family coincides with its stage — which is a
convenience, not a pattern.

**Recommendation:** keep the shape-derived names, and name all four once in
§4.4.2 (insertion B). Reusing the stage words would either force a membership
change that re-opens the dwell catalogue, App. B.4's tiers, the whole §5.1
re-run and every float built on it, or leave two taxonomies sharing three
words — the synonym collision voice §e bans. The stage words stay the distance
term's, one section later, where they are already load-bearing.

## S7. Order of work after this cut

1. Marc rules S2 (four paragraphs), S4.2 (the table cut, above all the decay
   collapse) and S6 (the family names).
2. Marc accepts or reworks insertions A, B, C; the session places them and
   fixes D-1's reference in the same diff.
3. Marc dictates ¶1–¶4 against the fifteen slots; the session runs the pipeline
   (repair → scrutinise → compress → voice) and swaps the block.
4. The session regenerates Table 5.1 from `analyse.py` in the new grammar
   (the collapse is an analyser change, not a re-run) and re-cuts the caption.
5. D6's downstream re-cuts, the build check, `FLOATS.md`, this handoff deleted.

---

# Third cut, 2026-09-20 — why two cuts produced no section, and the restructure proposed

Marc's read of the placeholder and Table 5.1 this session: the three groups and
the inputs inside them are fine; the columns *Declared / Moved across / What
moved* do not make sense to an average computer science reader; what the table
communicates is "there are three things, they put a lot of things in and ran
some numbers"; the caption is too heavy. He asked for a top-down answer: what
the section is for to that reader, how the field goes about it, what the table
carries that text cannot. Nothing below is applied; every item is a
recommendation for Marc to rule on. Where it overturns an earlier ruling or a
convention-file rule, it says so.

## T1. Diagnosis — five faults, the first three not named before

1. **The question and the test do not match.** Both earlier cuts state the
   question as *does any conclusion of this chapter depend on a chosen value*,
   and then test something else: whether the *level* of hosts reached leaves
   the confidence interval at the chosen value. No cut ever lists the
   conclusions. The chapter's conclusions are comparisons (what a defence does
   to the attacker against no defence; one interval against the other), and a
   level can move a long way while a comparison holds, or the reverse. The
   reader is promised an answer about conclusions and handed a column about
   levels, which is why the last column reads as "some numbers".
2. **The inert/moved verdict is an artefact of the seed count.** Findings §2
   records it: at ten seeds three dwell families were inert, at a hundred one
   is. At the thousand seeds the thesis reports, the interval shrinks by
   another factor of three and the exploit-shaped family (0.2 hosts per
   doubling) and the largest decay shift (0.18 hosts) will very likely read
   *moved* as well. A verdict that flips with the run count cannot be the
   table's content. The size of the effect is stable across seed counts; the
   verdict is not. The second cut half-saw this (one unit, hosts per doubling)
   and kept the criterion in ¶1 anyway.
3. **The table is a register, and a register serves the author.** Its design
   rule is `evaluation_conventions.md` §c's *every declared parameter is
   listed; one register, both kinds of row*. That rule is this repo's own
   inference from the corpus, not a practice in it: the corpus's good papers
   name what they did not vary **in a clause of prose** (Hong, Bland, Kim),
   never as table rows. Forcing a comparison, a structural zero and a hold
   into the same columns as a numeric range is what produced *Moved across:
   forced total* and *What moved: ---*. **Overturned on merit:** the table
   holds only what was varied numerically; what was not varied is one
   sentence.
4. **The columns narrate a procedure** (declared → moved across → what moved),
   the second cut's own finding, kept here. A reader does not want the
   author's steps; they want to run an eye down one column and see which row
   is different.
5. **The process built apparatus instead of sentences.** Three paragraph
   tables, fifteen slots with a must-not list each, a banned-word grep and a
   validation gate, and no sentence. A section written against fifteen
   prohibitions reads like one. The slot file is superseded by T4 below,
   which is six content points.

## T2. What the reader is doing with this section

The reader is a computer science student who has read the results: the
movement attacker reaches about eight hosts undefended and about two under the
random scheme at the 200 s interval. They remember from chapter 4 that some of
the model's values were chosen by judgement. They want three things, in this
order, and nothing else:

1. **Which of the chosen values matter?** (One does.)
2. **By how much would the reported numbers change if it were wrong?** (A
   range they can hold in their head.)
3. **Would the chapter's conclusions change?** (Which do, which do not.)

That is also what the field's sensitivity analyses deliver when they are good
(conventions §c): one input at a time over a stated range, the rest at their
table values; the output at each end; what was not varied, in a clause. The
wider simulation literature's standard display for exactly this is the
low-end / chosen / high-end comparison per input, sorted by the size of the
swing.

## T3. The number the earlier cuts did not compute

Read from `numbers.json` this session (four profiles pooled, 400 runs per
cell). Suppression is one minus hosts reached under defence over hosts reached
under no defence, at the same input value:

| Input moved | End | No defence | 200 s | suppression | 2 000 s | suppression |
|---|---|---|---|---|---|---|
| (all at chosen values) | | 8.1 | 2.1 | 75 % | 7.4 | 9 % |
| scan-shaped | ×0.5 / ×2 | 8.6 / 7.3 | 2.7 / 1.5 | 69 / 80 % | 8.2 / 6.3 | 5 / 14 % |
| exploit-shaped | ×0.5 / ×2 | 8.3 / 7.9 | 2.2 / 1.9 | 74 / 76 % | 7.7 / 7.4 | 7 / 7 % |
| **low-and-slow** | ×0.25 / ×4 | 13.4 / 3.0 | 7.5 / 0.3 | **44 / 89 %** | 14.7 / 2.0 | **−10 / 32 %** |
| objective | ×0.5 / ×2 | 8.5 / 7.4 | 2.3 / 1.7 | 73 / 77 % | 8.4 / 6.6 | 2 / 10 % |

What this licenses, and no more (measurement, not attribution): the *size* of
the defence's effect is exposed to the low-and-slow dwell — the 200 s figure
runs from 44 % to 89 % across that one family's band, and stays within 69–80 %
for every other input. The *ordering* holds at every point tested: the 200 s
interval suppresses strongly and the 2 000 s interval weakly or not at all.
The −10 % cell (14.7 ± 0.7 against 13.4 ± 0.7) has intervals that touch; it is
not a claim that the defence helps the attacker. No interval has been
computed on the suppression figures themselves; the analyser owes one before
any of these reach the tex. The sweep ran the random scheme only, so nothing
here speaks to the ranking of single mechanisms, and the section must say so.

This is the section's payload. It answers reader questions 2 and 3 in one
sentence each, and it is what the "selection sentence" of the earlier cuts was
reaching for without the number.

## T4. The restructure proposed

**Position — after the results, not before the setup (overturns D1 and the
2026-09-17 position ruling).** A reader cannot care that 8.1 becomes 13.4
before they know 8.1 is the result. §5.1 as first section uses the network,
the defence conditions, the measure and the run count before §5.2 declares
them; the second cut spent a whole section ("the measure §5.1 reads") patching
that. The earlier reason for going first — §5.2 opens by picking up what §5.1
selected — no longer exists: the §5.2 that went through pass 6 refers to §5.1
nowhere. Outkin's titled section, the corpus's only one, sits inside the
results. Recommended: the chapter's last section. Fallback if Marc keeps it
early: directly after §5.2, never before it. Labels are symbolic, so the move
costs a renumbering of float stems and `FLOATS.md`; chapter 4's forward
references stand as written.

**The table — one grammar, numbers only.**

| Input | Chosen value | Range tested | Hosts reached, no defence | Hosts reached, 200 s | Suppression at 200 s |
|---|---|---|---|---|---|
| *all at chosen values* | | | 8.1 | 2.1 | 75 % |
| low-and-slow dwell | 45 s | ×0.25 to ×4 | 13.4 to 3.0 | 7.5 to 0.3 | 44 to 89 % |
| scan-shaped dwell | 35 s | ×0.5 to ×2 | 8.6 to 7.3 | 2.7 to 1.5 | 69 to 80 % |
| objective dwell | 36 s | ×0.5 to ×2 | 8.5 to 7.4 | 2.3 to 1.7 | 73 to 77 % |
| exploit-shaped dwell | 4.5 s | ×0.5 to ×2 | 8.3 to 7.9 | 2.2 to 1.9 | 74 to 76 % |
| distribution of the dwell | exponential | less variable, same mean | *from numbers.json* | | |
| distance rate | 0.25 | 0.1 to 0.5 | | | |
| distance floor | 0.1 | 0 to 0.1 | | | |

Rows sorted by the size of the swing, largest first, under a reference row.
Every cell in the last three columns is the same kind of thing, so the eye
does the comparison: one row is different and the rest repeat the reference
row. That is the job the text cannot do, and it is the only job the table is
given. The 2 000 s columns go to Appendix C. The two distance rates stay one
row (second cut S4.2, kept). The mapping and the nine rules leave the table.
Caption, two sentences: what the rows are and how they were produced (one
input at a time, the rest at their chosen values, four profiles pooled, runs
per cell); that the first row is the reference. No symbols, no appendix tour,
no criterion.

A figure of the same content (one horizontal bar per input from low-end to
high-end value, reference line at 8.1) is the alternative form. Recommended:
the table, because the suppression column does not fit a bar and is the
column that matters.

**The mapping is not a sensitivity result, and the section should stop
presenting it as one.** Swapping the mapping takes hosts reached from 8.1 to
0.1. Read as sensitivity, that is the largest effect in the study by an order
of magnitude, and "the alternative under-performs" understates it. Read
correctly, the alternative is not a plausible value of the same model; it is
a model that does not work, which chapter 4 and Appendix B.7 already say. It
is a structural choice with no range, as the nine rules are. One sentence
covers both: they were not varied, why, and where the one alternative tried
is reported. Chapter 4's "the mapping is swapped in the sensitivity analysis"
then wants re-pointing at Appendix B.7 (a chapter 4 edit, Marc's).

**The prose — three paragraphs, six content points.**

| ¶ | Content points |
|---|---|
| 1 | (a) Some of the model's values were chosen by judgement (chapter 4); this section reports how far the results move if they are wrong. (b) How: each varied alone over the range chapter 4 gave it, everything else as in the setup table; read on hosts reached, undefended and under the random scheme. |
| 2 | (c) One input matters: the low-and-slow dwell; the swing in hosts reached, and the direction (longer quiet dwell, fewer hosts in the time limit). Every other input moves the result by under a host. (d) What that does to the chapter's claims: the size of the defence's effect moves with it (the suppression range); the ordering of the two intervals does not. It is also the value with the least behind it, which chapter 4 said. |
| 3 | (e) Not varied: the mapping and the nine failure rules, structural choices without a range; pointer to B.7. (f) Not tested: single-mechanism rankings and the baseline attacker, which takes none of these inputs. |

No criterion sentence, no inert/moved vocabulary, no method defence. Marc's
words throughout; the session supplies numbers and runs the pipeline passes.

## T5. What Marc rules on, in order

1. Position: last section of the chapter (recommended), or directly after §5.2.
2. The table grammar of T4, including dropping the inert/moved verdict and
   the register rule.
3. The mapping and the rules leaving the analysis for one not-varied sentence.
4. Suppression as the section's reading (T3) — and with it an analyser
   change to emit the suppression figures with intervals. No re-run.
5. Retiring `2026-09-18_ch5_s51_slot_generator.md` in favour of T4's six points.

If 1–4 are accepted, `evaluation_conventions.md` §c's closing rule is amended
in the same commit to say what the corpus does (prose clause for what was not
varied), not what this repo inferred.
