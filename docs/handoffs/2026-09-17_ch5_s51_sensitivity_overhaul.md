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
