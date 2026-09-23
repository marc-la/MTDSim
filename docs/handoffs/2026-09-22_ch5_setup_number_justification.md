---
status: open (landed 2026-09-23; only the two-target reason owed)  # executes register E5; successor to the retired §5.2 setup critique for §5.1's remaining debts (the two-target reason; C39 generator)
created: 2026-09-22
executes: docs/implementation/pipeline/ogasp/supervisor_decision_register.md §E5
companions: 2026-09-22_ch5_defended_corpus_schemes_intervals_mtdshield.md (the interval levels that Table 5.1 will declare), ../workflows/evaluation_conventions.md §c, §d
---

# Defend every value in the experimental setup by pointing at prior use: a background table of the lineage's configurations, and one clause per value in §5.1

## Landed 2026-09-23 — what is left is Marc's

Executed on Marc's direction ("literally it needs to be visible that we're
citing where we got the numbers from"). Steps 1–4 are done; the table's home
was ruled by that direction (the background, ch2).

- **Table 2.2 `tab:lineage-configurations`** (§2.2, after Table 2.1), generated
  by `tools/ch2_lineage_configurations_table.py` from
  `data/misc/lineage_configurations.yaml`, one locator per cell in the
  fragment header. Brown, Zhang, Ho as columns, in Table 5.1's parameter order;
  Tay is not a column (states none — caption). **Kim and Masud not added**:
  a physical SDN testbed and an 8-host VM rig are not configurations of this
  simulator, so they would widen the range without defending a value.
- **Table 5.1**: a citation after every value a prior study ran; the caption's
  last sentence covers the rest (the simulator's default, or argued in §5.1).
- **§5.1**: one clause each in Network, Defence, Runs; the numerals fixed;
  every session-written clause is under a `DRAFT STATE 2026-09-23 … RATIFY ON
  READ` comment. One ch2 sentence points at the new table, same marker.
- **Numerals rule** in `academic_register.md` §(b)8; the "held and why →
  cited prior run" rule in `evaluation_conventions.md` §c. The one ch5 body
  violation left (a caption's "sums to a hundred") fixed.
- **Correction to the table below:** Ho's `H-PAR-06` = 100 is *training
  episodes*, not evaluation runs; Ho states no run count. Zhang alone states
  100 per condition, so the Runs clause cites Zhang only.

**Resolved 2026-09-23 (Marc):** the four clauses are ratified ("that's
fine"); **2 000 s** is defended as the top of a range, 50 s to 2 000 s, so the
results carry the interval on the x axis, not by precedent (ruling recorded in
the tex comment under the Defence unit; the rewrite rides the corpus handoff's
sweep, which now says so).

**Still owed (Marc):** the two-target reason, `[3b]` under the Network unit.
Retire this file when it is in. C39 stays deferred to the sweep pass.

## State of play (as briefed 2026-09-22)

**The ruling (E5).** "Every hard-coded number, somebody will ask why that number." A value a prior study used is the easiest to defend: a summary table in the background of what prior studies ran, then §5.1 says its values sit in that range. Numbers greater than ten in numerals.

**Table 5.1 today** (`docs/thesis/tables/tab_5-1a_experiment.tex`; through pass 6, 2026-09-20; the justification column was deleted on 2026-09-18 — "what do I need them for?" — which E5 now answers: the reader needs them, once, as a pointer). What each value is and where it comes from, read from the evaluation anatomies (`docs/implementation/evaluation_anatomies/`) and the code:

| Row | Value | Provenance found | Locator to verify |
|---|---|---|---|
| Hosts / levels / subnets / endpoints | 50 / 4 / 8 / 5 | the simulator's defaults (`mtdnetwork/component/time_network.py:11-12`); **Zhang's network 2 is 50 nodes, 5 endpoints, 4 layers** (Table 2, p.33) — the middle of his 25–100 sweep; Brown ran 200 hosts / 20 exposed / 5 layers / 20 subnets (Table I, p.5); Ho 150 nodes (Table 2, p.19); Tay states none | `zhang2023.md` anatomy l.35; `brown2023.md` l.31, l.34; `ho2024.md` l.68 |
| Target | the two database hosts | narrowed from the default five (`run.py:67`); **the reason is Marc's and still open** (the standing `[3b]`, l.~5522); Brown's scenario 2 targets "a credential database" (p.4) | `tab_5-1a` comments |
| Objective | targeted | ruled 2026-09-20; Brown's scenario 2 | — |
| Condition | no defence; seven singles; random; alternative (+ MTDShield, corpus handoff) | Brown runs every single and combination with "None" (p.6); Zhang's three schemes (§4.3.2); Ho compares his selector to random / alternative / simultaneous (Table 8, p.24) | anatomies |
| Deployment interval | 200 s; 2 000 s → the sweep levels | **Zhang swept 50–200 s** (p.33); **Ho 50 / 100 / 200 s** (Table 6) with his comparator table at 200 s (Table 8); Brown Uniform(1000, 5000) ms; **2 000 s has no precedent** — with the sweep (corpus handoff) it becomes the top of a declared range | `zhang2023.md` l.38; `ho2024.md` l.73, l.75 |
| Timing distribution | near-periodic; exponential | Zhang §4.3.4 (exponential replaces Brown's uniform); the near-periodic shifted form is the code's default (D-08, `provenance.md` l.39) | — |
| Deployment durations | 110 / 100 / 100 / 80 / 70 / 70 / 20 s | Zhang Table 3 (p.34) for complete topology, IP, OS and service (110 / 100 / 80 / 70); host topology, port and user shuffle are inherited constants with no paper (`provenance.md`) — say so | `zhang2023.md` l.38 |
| Time limit | 15 000 s | Ho's `finish_time` (H-PAR-08; already cited) | — |
| Seeds | 1 000 | Zhang and Ho ran 100 per cell; Brown and Tay state none; 1 000 is ten times the lineage's count — the sentence is "ten times the lineage's 100", not a citation to a standard | `zhang2023.md` l.39; `ho2024.md` H-PAR-06 |

Chapter 4's declared values (dwell times, mapping, failure matrix) are already defended by Appendix C's robustness tables and are **not** this file's business.

## Recommended approach

1. **Build the background table** from the four anatomies, one paper per pass (guardrails): *Study · Hosts · Exposed endpoints · Levels · Subnets · Deployment interval · Termination / time limit · Runs per cell*, rows Brown 2023, Zhang 2023, Ho 2024, Tay 2024 ("not stated" where the anatomy says so — the absence census is itself a fact the thesis can use). Optionally two rows from the wider field (Kim 2026, Masud 2025) if their anatomies carry the values. House style §k; generated by a small `tools/` script that reads a YAML of the values with locators, so the caption's locators are checkable.
2. **Place it** in ch2 §2.2 (recommended — Jin: "in the background"; it describes existing work) beside Table 2.2, with one sentence of prose in the ch2 register; alternative: §5.1, which then argues, against conventions §a. Marc rules.
3. **§5.1, one clause per unit**, in Marc's dictation: the network unit already says "every value is the simulator's own default but one"; add "and the middle of the range the lineage has run (Table 2.x)"; the defence unit names the interval range as the lineage's 50–200 s extended to 2 000 s; the runs unit says ten times the lineage's count. The two-target reason is Marc's sentence and cannot be delegated.
4. **Numerals audit** (E5's house rule): "Fifty hosts" → "50 hosts", "a thousand runs" → "1 000 runs", across the ch5 prose; record the rule in `docs/workflows/academic_register.md` (numbers above ten in numerals; a number opening a sentence is recast) so pass 6 enforces it.
5. **C39** — Tables 5.1 and 5.2 born generated from the run matrix — is inherited from the retired setup critique; do it in the same pass if the corpus handoff changes the levels, else defer.

## Rulings owed (Marc)

The two-target reason (his sentence); the table's home (ch2 recommended); whether the field rows (Kim, Masud) are worth the space.

## Validation gate

Every Table 5.1 value has either a citation in its row, a pointer to the background table, or a stated reason in the unit's prose; the background table exists with a locator per cell in its generator's source; `grep -n '\bFifty\b\|a thousand' ` on the ch5 body returns nothing; `academic_register.md` carries the numerals rule; build clean.

## Hard constraints

- One paper per pass when reading the anatomies (guardrails).
- Never assert a paper is wrong; "not stated" is the record.
- §5.1 declares and does not argue (conventions §a) — the pointer is one clause, not a paragraph.

## Reading list

- `docs/thesis/tables/tab_5-1a_experiment.tex` — the comment trail.
- `docs/implementation/evaluation_anatomies/{brown2023,zhang2023,ho2024,tay2024}.md` — the "what it declares before a result" rows.
- `docs/implementation/provenance.md` — the constants' source rows.
- `docs/workflows/evaluation_conventions.md` §c (one register, both kinds of row), §d (replication).
- `docs/handoffs/2026-09-09_ch5_experiments_design.md` — the debt ledger, l.~2526 (the [3b] items §5.1 still owes).

## Out of scope

Chapter 4's declared values (Appendix C); the interval levels themselves (corpus handoff).
